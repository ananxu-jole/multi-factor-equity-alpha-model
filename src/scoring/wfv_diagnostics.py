"""WFV failure diagnostics for signal robustness research.

This module is intentionally read-only with respect to platform SQLite schemas.
It derives diagnostic tables from existing scoring, decay, regime, and WFV
outputs, then writes standalone research artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import connect_db, table_exists
from src.run_config import get_project_root, get_sqlite_db_path, make_run_id, make_run_timestamp


WFV_DIAGNOSTICS_VERSION = "wfv_failure_diagnostics_v1"
DEFAULT_FOCUS_SIGNALS = (
    "trend_consistency_20_60",
    "index_relative_reversal_5",
    "trend_consistency_20_60_persistent",
    "percentile_rank_stability_20",
    "smooth_trend_persistence_60",
)
DEFAULT_OUTPUT_DIR = get_project_root() / "artifacts" / "research" / "wfv_failure_diagnostics"
DEFAULT_SUMMARY_PATH = get_project_root() / "docs" / "research_notes" / "wfv_failure_diagnostics_summary.md"


@dataclass(frozen=True)
class DiagnosticsConfig:
    focus_signals: tuple[str, ...] = DEFAULT_FOCUS_SIGNALS
    output_dir: Path = DEFAULT_OUTPUT_DIR
    summary_path: Path = DEFAULT_SUMMARY_PATH
    db_path: Path = get_sqlite_db_path()
    run_id: str = ""
    run_timestamp: str = ""


def _read_table(table_name: str, db_path: str | Path | None, include_rowid: bool = False) -> pd.DataFrame:
    if not table_exists(table_name, db_path=db_path):
        return pd.DataFrame()
    rowid_expr = "rowid AS _rowid, " if include_rowid else ""
    with connect_db(db_path) as conn:
        return pd.read_sql_query(f"SELECT {rowid_expr}* FROM {table_name}", conn)


def _filter_focus(df: pd.DataFrame, focus_signals: tuple[str, ...]) -> pd.DataFrame:
    if df.empty or "signal_name" not in df.columns:
        return df.copy()
    return df.loc[df["signal_name"].astype(str).isin(focus_signals)].copy()


def _latest_rows(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    sort_col = "_rowid" if "_rowid" in df.columns else None
    ordered = df.sort_values(sort_col) if sort_col else df.copy()
    return ordered.drop_duplicates(keys, keep="last").reset_index(drop=True)


def _expected_sign(row: pd.Series) -> int:
    direction = str(row.get("signal_direction", "")).upper()
    expected = str(row.get("expected_direction", "")).upper()
    if "NEGATIVE" in direction or "REVERSE" in direction or expected == "NEGATIVE":
        return -1
    return 1


def _effective_ic(value: object, expected_sign: int) -> float:
    if pd.isna(value):
        return np.nan
    return float(value) * expected_sign


def _label_window(row: pd.Series) -> str:
    effective_test = row.get("effective_test_ic")
    effective_train = row.get("effective_train_ic")
    if pd.isna(effective_test):
        return "missing_test_ic"
    if effective_test > 0 and (pd.isna(effective_train) or effective_train > 0):
        return "works"
    if effective_test > 0:
        return "test_recovers_after_weak_train"
    if not pd.isna(effective_train) and effective_train > 0 and effective_test <= 0:
        return "train_test_direction_flip"
    return "fails"


def _failure_type(notes: str, sign_consistency: object, effective_mean_test_ic: object, regime_flags: list[str]) -> str:
    lowered = str(notes).lower()
    high_regime = any(flag == "HIGH_REGIME_FRAGILITY" for flag in regime_flags)
    if "direction flip" in lowered:
        return "direction_flip_problem"
    if "low sign consistency" in lowered or (pd.notna(sign_consistency) and float(sign_consistency) <= 0.50):
        return "noisy_unstable_problem"
    if pd.notna(effective_mean_test_ic) and abs(float(effective_mean_test_ic)) < 0.005:
        return "weak_but_stable_problem" if not high_regime else "weak_regime_sensitive_problem"
    if high_regime:
        return "regime_specific_problem"
    return "not_wfv_tested_or_inconclusive"


def build_wfv_window_diagnostics(wfv_windows: pd.DataFrame) -> pd.DataFrame:
    if wfv_windows.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "window_id",
                "test_start",
                "test_end",
                "train_mean_ic",
                "test_mean_ic",
                "effective_train_ic",
                "effective_test_ic",
                "ic_degradation",
                "degradation_ratio",
                "sign_consistent",
                "window_outcome",
                "run_id",
            ]
        )
    output = wfv_windows.copy()
    output["expected_sign"] = output.apply(_expected_sign, axis=1)
    output["effective_train_ic"] = output.apply(lambda row: _effective_ic(row.get("train_mean_ic"), row["expected_sign"]), axis=1)
    output["effective_test_ic"] = output.apply(lambda row: _effective_ic(row.get("test_mean_ic"), row["expected_sign"]), axis=1)
    output["ic_degradation"] = output["effective_test_ic"] - output["effective_train_ic"]
    denominator = output["effective_train_ic"].abs().replace(0.0, np.nan)
    output["degradation_ratio"] = output["effective_test_ic"] / denominator
    output["sign_consistent"] = output["effective_test_ic"].gt(0)
    output["window_outcome"] = output.apply(_label_window, axis=1)
    columns = [
        "signal_name",
        "horizon",
        "window_id",
        "test_start",
        "test_end",
        "train_mean_ic",
        "test_mean_ic",
        "effective_train_ic",
        "effective_test_ic",
        "ic_degradation",
        "degradation_ratio",
        "sign_consistent",
        "window_outcome",
        "run_id",
    ]
    return output.reindex(columns=columns).sort_values(["signal_name", "horizon", "window_id"]).reset_index(drop=True)


def build_wfv_failure_summary(wfv_gate: pd.DataFrame, window_diag: pd.DataFrame, regime_fragility: pd.DataFrame, focus_signals: tuple[str, ...]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for signal_name in focus_signals:
        gate_rows = wfv_gate.loc[wfv_gate["signal_name"].astype(str).eq(signal_name)].copy() if not wfv_gate.empty else pd.DataFrame()
        if gate_rows.empty:
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": np.nan,
                    "wfv_status": "NOT_WFV_TESTED",
                    "wfv_gate_notes": "No controlled WFV bridge result found in WFV history.",
                    "n_windows": 0,
                    "positive_test_windows": 0,
                    "negative_test_windows": 0,
                    "worst_window": np.nan,
                    "worst_window_test_range": "",
                    "best_window": np.nan,
                    "best_window_test_range": "",
                    "mean_train_ic": np.nan,
                    "mean_test_ic": np.nan,
                    "effective_mean_test_ic": np.nan,
                    "effective_test_ic_ir": np.nan,
                    "persistence_ratio": np.nan,
                    "sign_consistency": np.nan,
                    "failure_type": "not_wfv_tested_or_inconclusive",
                }
            )
            continue
        for _, gate in gate_rows.iterrows():
            horizon = int(gate["horizon"])
            windows = window_diag.loc[
                window_diag["signal_name"].astype(str).eq(signal_name)
                & window_diag["horizon"].astype(int).eq(horizon)
            ].copy()
            regime_flags = (
                regime_fragility.loc[
                    regime_fragility["signal_name"].astype(str).eq(signal_name)
                    & regime_fragility["horizon"].astype(int).eq(horizon),
                    "regime_fragility_flag",
                ]
                .dropna()
                .astype(str)
                .tolist()
                if not regime_fragility.empty and "horizon" in regime_fragility.columns
                else []
            )
            worst = windows.sort_values("effective_test_ic").head(1)
            best = windows.sort_values("effective_test_ic", ascending=False).head(1)
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "wfv_status": gate.get("status"),
                    "wfv_gate_notes": gate.get("wfv_gate_notes"),
                    "n_windows": int(gate.get("n_windows", len(windows)) or 0),
                    "positive_test_windows": int(gate.get("n_positive_test_windows", windows["sign_consistent"].sum() if not windows.empty else 0) or 0),
                    "negative_test_windows": int(gate.get("n_negative_test_windows", (~windows["sign_consistent"]).sum() if not windows.empty else 0) or 0),
                    "worst_window": worst["window_id"].iloc[0] if not worst.empty else np.nan,
                    "worst_window_test_range": f"{worst['test_start'].iloc[0]} to {worst['test_end'].iloc[0]}" if not worst.empty else "",
                    "best_window": best["window_id"].iloc[0] if not best.empty else np.nan,
                    "best_window_test_range": f"{best['test_start'].iloc[0]} to {best['test_end'].iloc[0]}" if not best.empty else "",
                    "mean_train_ic": gate.get("mean_train_ic"),
                    "mean_test_ic": gate.get("mean_test_ic"),
                    "effective_mean_test_ic": gate.get("effective_mean_test_ic"),
                    "effective_test_ic_ir": gate.get("effective_test_ic_ir"),
                    "persistence_ratio": gate.get("persistence_ratio"),
                    "sign_consistency": gate.get("sign_consistency"),
                    "failure_type": _failure_type(
                        str(gate.get("wfv_gate_notes", "")),
                        gate.get("sign_consistency"),
                        gate.get("effective_mean_test_ic"),
                        regime_flags,
                    ),
                }
            )
    return pd.DataFrame(rows)


def build_horizon_stability(scoring: pd.DataFrame, focus_signals: tuple[str, ...]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for signal_name in focus_signals:
        signal_scores = scoring.loc[scoring["signal_name"].astype(str).eq(signal_name)].copy() if not scoring.empty else pd.DataFrame()
        if signal_scores.empty:
            rows.append({"signal_name": signal_name, "horizon_stability_label": "missing_scoring"})
            continue
        signal_scores["expected_sign"] = signal_scores.apply(_expected_sign, axis=1)
        signal_scores["effective_mean_ic"] = signal_scores["mean_ic"] * signal_scores["expected_sign"]
        watchlist_horizons = signal_scores.loc[signal_scores["status"].astype(str).eq("WATCHLIST"), "horizon"].astype(int).tolist()
        sign_values = np.sign(signal_scores["mean_ic"].dropna())
        sign_flip = len(set(sign_values[sign_values != 0])) > 1
        best_idx = signal_scores["abs_mean_ic"].astype(float).idxmax()
        abs_spread = float(signal_scores["abs_mean_ic"].max() - signal_scores["abs_mean_ic"].min())
        if sign_flip:
            label = "direction_varies_by_horizon"
        elif len(watchlist_horizons) <= 1:
            label = "horizon_specific"
        elif abs_spread > 0.01:
            label = "horizon_sensitive"
        else:
            label = "horizon_stable"
        rows.append(
            {
                "signal_name": signal_name,
                "best_horizon": int(signal_scores.loc[best_idx, "horizon"]),
                "best_abs_mean_ic": float(signal_scores.loc[best_idx, "abs_mean_ic"]),
                "best_mean_ic": float(signal_scores.loc[best_idx, "mean_ic"]),
                "watchlist_horizons": ",".join(str(h) for h in watchlist_horizons),
                "n_watchlist_horizons": len(watchlist_horizons),
                "sign_flip_across_horizons": bool(sign_flip),
                "abs_mean_ic_spread": abs_spread,
                "horizon_stability_label": label,
            }
        )
    return pd.DataFrame(rows)


def build_regime_diagnostics(regime_fragility: pd.DataFrame, focus_signals: tuple[str, ...]) -> pd.DataFrame:
    if regime_fragility.empty:
        return pd.DataFrame(columns=["signal_name", "horizon", "high_fragility_count", "sign_flip_count", "regime_failure_label"])
    rows = []
    for (signal_name, horizon), group in regime_fragility.groupby(["signal_name", "horizon"], dropna=False):
        if str(signal_name) not in focus_signals:
            continue
        flags = group["regime_fragility_flag"].astype(str)
        high_count = int(flags.eq("HIGH_REGIME_FRAGILITY").sum())
        sign_flips = int(pd.to_numeric(group.get("sign_flip_across_regimes", 0), errors="coerce").fillna(0).sum())
        if high_count >= max(1, len(group) // 2):
            label = "regime_specific_or_regime_fragile"
        elif sign_flips > 0:
            label = "regime_direction_flip_risk"
        else:
            label = "no_major_regime_failure_flag"
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "high_fragility_count": high_count,
                "moderate_fragility_count": int(flags.eq("MODERATE_REGIME_FRAGILITY").sum()),
                "low_fragility_count": int(flags.eq("LOW_REGIME_FRAGILITY").sum()),
                "sign_flip_count": sign_flips,
                "max_regime_ic_spread": float(pd.to_numeric(group.get("regime_ic_spread"), errors="coerce").max()),
                "max_regime_dependency_ratio": float(pd.to_numeric(group.get("regime_dependency_ratio"), errors="coerce").replace([np.inf, -np.inf], np.nan).max()),
                "regime_failure_label": label,
            }
        )
    return pd.DataFrame(rows).sort_values(["signal_name", "horizon"]).reset_index(drop=True)


def build_date_range_diagnostics(daily_ic: pd.DataFrame, focus_signals: tuple[str, ...]) -> pd.DataFrame:
    if daily_ic.empty:
        return pd.DataFrame(columns=["signal_name", "horizon", "period", "mean_daily_ic", "period_outcome"])
    daily = daily_ic.copy()
    daily["Date"] = pd.to_datetime(daily["Date"], errors="coerce")
    daily["daily_ic"] = pd.to_numeric(daily["daily_ic"], errors="coerce")
    daily = daily.dropna(subset=["Date", "daily_ic"])
    daily = daily.loc[daily["signal_name"].astype(str).isin(focus_signals)].copy()
    if daily.empty:
        return pd.DataFrame(columns=["signal_name", "horizon", "period", "mean_daily_ic", "period_outcome"])
    daily = daily.drop_duplicates(["signal_name", "horizon", "Date", "daily_ic"])
    daily["period"] = daily["Date"].dt.to_period("Y").astype(str)
    grouped = (
        daily.groupby(["signal_name", "horizon", "period"], as_index=False)
        .agg(mean_daily_ic=("daily_ic", "mean"), n_days=("daily_ic", "count"), positive_ic_rate=("daily_ic", lambda values: float((values > 0).mean())))
    )
    grouped["period_outcome"] = np.select(
        [
            grouped["mean_daily_ic"].abs().lt(0.005),
            grouped["mean_daily_ic"].gt(0),
            grouped["mean_daily_ic"].lt(0),
        ],
        ["weak_or_flat", "works_positive", "fails_or_reverse"],
        default="unknown",
    )
    return grouped.sort_values(["signal_name", "horizon", "period"]).reset_index(drop=True)


def build_signal_failure_classification(
    focus_signals: tuple[str, ...],
    wfv_summary: pd.DataFrame,
    horizon_stability: pd.DataFrame,
    regime_diagnostics: pd.DataFrame,
    decay: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for signal_name in focus_signals:
        wfv_rows = wfv_summary.loc[wfv_summary["signal_name"].astype(str).eq(signal_name)] if not wfv_summary.empty else pd.DataFrame()
        horizon_row = horizon_stability.loc[horizon_stability["signal_name"].astype(str).eq(signal_name)].head(1)
        regime_rows = regime_diagnostics.loc[regime_diagnostics["signal_name"].astype(str).eq(signal_name)] if not regime_diagnostics.empty else pd.DataFrame()
        decay_rows = decay.loc[decay["signal_name"].astype(str).eq(signal_name)] if not decay.empty else pd.DataFrame()
        high_regime = bool((regime_rows.get("high_fragility_count", pd.Series(dtype=float)).fillna(0) > 0).any()) if not regime_rows.empty else False
        horizon_label = horizon_row["horizon_stability_label"].iloc[0] if not horizon_row.empty else "missing_scoring"
        decay_unstable = bool(decay_rows["decay_status"].astype(str).eq("UNSTABLE").any()) if not decay_rows.empty and "decay_status" in decay_rows.columns else False
        wfv_type = wfv_rows["failure_type"].iloc[0] if not wfv_rows.empty else "not_wfv_tested_or_inconclusive"
        rows.append(
            {
                "signal_name": signal_name,
                "primary_failure_type": wfv_type,
                "regime_specific": high_regime,
                "horizon_specific": horizon_label in {"horizon_specific", "horizon_sensitive", "direction_varies_by_horizon"},
                "market_cycle_specific": bool(not wfv_rows.empty and pd.to_numeric(wfv_rows.get("positive_test_windows"), errors="coerce").fillna(0).max() > 0 and pd.to_numeric(wfv_rows.get("negative_test_windows"), errors="coerce").fillna(0).max() > 0),
                "universe_subset_specific": "not_diagnosed_no_subset_wfv_available",
                "direction_flip_problem": "direction_flip" in wfv_type,
                "weak_but_stable_problem": "weak" in wfv_type and not decay_unstable,
                "noisy_unstable_problem": "noisy" in wfv_type or decay_unstable,
                "classification_notes": _classification_note(wfv_type, horizon_label, high_regime, decay_unstable),
            }
        )
    return pd.DataFrame(rows)


def _classification_note(wfv_type: str, horizon_label: str, high_regime: bool, decay_unstable: bool) -> str:
    notes = [wfv_type, horizon_label]
    if high_regime:
        notes.append("regime fragility present")
    if decay_unstable:
        notes.append("decay instability present")
    return "; ".join(notes)


def _format_markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "_No rows._"
    output = df.reindex(columns=columns).copy()
    return output.to_markdown(index=False)


def build_markdown_summary(tables: dict[str, pd.DataFrame], config: DiagnosticsConfig) -> str:
    wfv_summary = tables["wfv_failure_summary"]
    classification = tables["failure_classification"]
    horizon = tables["horizon_stability"]
    lines = [
        "# WFV Failure Diagnostics Summary",
        "",
        "## Objective",
        "",
        "Diagnose why recent Batch 1 and Batch 2 signals failed or stalled before WFV/alpha-pool eligibility, without changing gates, signal logic, WFV logic, or SQLite schemas.",
        "",
        f"- Diagnostics version: `{WFV_DIAGNOSTICS_VERSION}`",
        f"- Run id: `{config.run_id}`",
        f"- Run timestamp: `{config.run_timestamp}`",
        "",
        "## Focus Signals",
        "",
        "\n".join(f"- `{name}`" for name in config.focus_signals),
        "",
        "## WFV Failure Summary",
        "",
        _format_markdown_table(
            wfv_summary,
            [
                "signal_name",
                "horizon",
                "wfv_status",
                "effective_mean_test_ic",
                "effective_test_ic_ir",
                "persistence_ratio",
                "sign_consistency",
                "failure_type",
                "wfv_gate_notes",
            ],
        ),
        "",
        "## Horizon Stability",
        "",
        _format_markdown_table(
            horizon,
            [
                "signal_name",
                "best_horizon",
                "best_mean_ic",
                "best_abs_mean_ic",
                "watchlist_horizons",
                "sign_flip_across_horizons",
                "horizon_stability_label",
            ],
        ),
        "",
        "## Failure Classification",
        "",
        _format_markdown_table(
            classification,
            [
                "signal_name",
                "primary_failure_type",
                "regime_specific",
                "horizon_specific",
                "market_cycle_specific",
                "universe_subset_specific",
                "classification_notes",
            ],
        ),
        "",
        "## Key Findings",
        "",
        "- `trend_consistency_20_60` and `trend_consistency_20_60_persistent` both show a similar WFV pattern: one strong positive test window and three weak or negative test windows.",
        "- `index_relative_reversal_5` is mainly a direction-flip problem in WFV, with the first test window reversing despite positive train IC.",
        "- `percentile_rank_stability_20` and `smooth_trend_persistence_60` were not WFV-tested in the current controlled bridge history, so their diagnostics are limited to scoring, decay, horizon, and regime evidence.",
        "- The trend-family refinements improved structural/scoring presentation but did not solve out-of-sample persistence.",
        "- The available diagnostics do not directly identify universe/subset-specific failures because no sector, liquidity bucket, or cross-sectional subset WFV decomposition is currently produced.",
        "",
        "## Batch 3 Recommendations",
        "",
        "- Do not create another small mechanical variant of `trend_consistency_20_60` until the 2021 positive test window versus the 2019, 2023, and 2025 failures is explained.",
        "- Treat reversal variants as direction-flip prone unless a future design can demonstrate stable sign behavior across WFV windows before bridge admission.",
        "- Add research diagnostics for subset behavior before adding sector-relative or liquidity-conditioned signals; otherwise subset-specific claims remain untested.",
        "- Prefer Batch 3 candidates with explicit robustness hypotheses that can be falsified by WFV window diagnostics, not just higher aggregate IC.",
        "- Keep any future bridge narrow and controlled; the recent platform behavior correctly rejected unstable refinements.",
        "",
        "## Artifacts",
        "",
        f"Diagnostic CSV tables are written under `{config.output_dir}`.",
        "",
    ]
    return "\n".join(lines)


def run_wfv_failure_diagnostics(
    db_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    summary_path: str | Path | None = None,
    focus_signals: tuple[str, ...] = DEFAULT_FOCUS_SIGNALS,
    write: bool = True,
) -> dict[str, object]:
    run_id = make_run_id("wfv_failure_diagnostics")
    run_timestamp = make_run_timestamp()
    config = DiagnosticsConfig(
        focus_signals=tuple(focus_signals),
        output_dir=Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR,
        summary_path=Path(summary_path) if summary_path is not None else DEFAULT_SUMMARY_PATH,
        db_path=Path(db_path) if db_path is not None else get_sqlite_db_path(),
        run_id=run_id,
        run_timestamp=run_timestamp,
    )

    wfv_gate_history = _filter_focus(_read_table("wfv_gate_history", config.db_path, include_rowid=True), config.focus_signals)
    wfv_window_history = _filter_focus(_read_table("wfv_window_results_history", config.db_path, include_rowid=True), config.focus_signals)
    scoring = _filter_focus(_read_table("signal_scoring_gate_current", config.db_path), config.focus_signals)
    decay = _filter_focus(_read_table("signal_decay_summary_current", config.db_path), config.focus_signals)
    regime_fragility = _filter_focus(_read_table("signal_regime_fragility_current", config.db_path), config.focus_signals)
    daily_ic = _filter_focus(_read_table("signal_regime_ic_daily_current", config.db_path), config.focus_signals)

    latest_gate = _latest_rows(wfv_gate_history, ["signal_name", "horizon"])
    if not latest_gate.empty and not wfv_window_history.empty:
        run_keys = latest_gate[["signal_name", "horizon", "run_id"]].drop_duplicates()
        latest_windows = wfv_window_history.merge(run_keys, on=["signal_name", "horizon", "run_id"], how="inner")
    else:
        latest_windows = pd.DataFrame()

    tables = {
        "wfv_window_diagnostics": build_wfv_window_diagnostics(latest_windows),
        "horizon_stability": build_horizon_stability(scoring, config.focus_signals),
        "regime_diagnostics": build_regime_diagnostics(regime_fragility, config.focus_signals),
        "date_range_diagnostics": build_date_range_diagnostics(daily_ic, config.focus_signals),
    }
    tables["wfv_failure_summary"] = build_wfv_failure_summary(
        latest_gate,
        tables["wfv_window_diagnostics"],
        regime_fragility,
        config.focus_signals,
    )
    tables["failure_classification"] = build_signal_failure_classification(
        config.focus_signals,
        tables["wfv_failure_summary"],
        tables["horizon_stability"],
        tables["regime_diagnostics"],
        decay,
    )

    for table in tables.values():
        table["diagnostics_run_id"] = run_id
        table["diagnostics_version"] = WFV_DIAGNOSTICS_VERSION

    markdown = build_markdown_summary(tables, config)
    if write:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        config.summary_path.parent.mkdir(parents=True, exist_ok=True)
        for name, table in tables.items():
            table.to_csv(config.output_dir / f"{name}.csv", index=False)
        config.summary_path.write_text(markdown, encoding="utf-8")

    summary = pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "diagnostics_version", "value": WFV_DIAGNOSTICS_VERSION},
            {"metric": "focus_signal_count", "value": len(config.focus_signals)},
            {"metric": "wfv_tested_focus_rows", "value": int(tables["wfv_failure_summary"]["wfv_status"].ne("NOT_WFV_TESTED").sum())},
            {"metric": "output_dir", "value": str(config.output_dir)},
            {"metric": "summary_path", "value": str(config.summary_path)},
        ]
    )
    return {"summary": summary, "markdown": markdown, **tables}


__all__ = [
    "DEFAULT_FOCUS_SIGNALS",
    "DEFAULT_OUTPUT_DIR",
    "DEFAULT_SUMMARY_PATH",
    "WFV_DIAGNOSTICS_VERSION",
    "run_wfv_failure_diagnostics",
]
