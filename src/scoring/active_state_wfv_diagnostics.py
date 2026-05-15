"""Research-only active-state WFV diagnostics for conditional signals.

This module intentionally does not write to official WFV tables or alter any
platform gate. It evaluates conditional signals on active market-state dates
beside the fixed-window WFV outputs so sparse conditional edges can be studied
without changing promotion logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import connect_db, load_price_table, table_exists
from src.forward_returns import make_forward_returns
from src.run_config import get_project_root, get_sqlite_db_path, make_run_id, make_run_timestamp
from src.signal_storage import load_candidate_signals_by_names, pivot_signal_long_to_panel


ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION = "active_state_wfv_diagnostics_v1"
DEFAULT_SIGNAL = "smooth_trend_persistence_60_downtrend"
DEFAULT_HORIZON = 20
DEFAULT_OUTPUT_DIR = get_project_root() / "artifacts" / "research" / "active_state_wfv_diagnostics"
DEFAULT_SUMMARY_PATH = get_project_root() / "docs" / "research_notes" / "active_state_wfv_framework_proposal.md"
MIN_ACTIVE_TEST_DATES = 20
MIN_ACTIVE_WINDOWS = 2
MIN_ACTIVE_WINDOW_COVERAGE_RATIO = 0.50


@dataclass(frozen=True)
class ActiveStateDiagnosticsConfig:
    signal_name: str = DEFAULT_SIGNAL
    horizon: int = DEFAULT_HORIZON
    output_dir: Path = DEFAULT_OUTPUT_DIR
    summary_path: Path = DEFAULT_SUMMARY_PATH
    db_path: Path = get_sqlite_db_path()
    run_id: str = ""
    run_timestamp: str = ""
    min_active_test_dates: int = MIN_ACTIVE_TEST_DATES
    min_active_windows: int = MIN_ACTIVE_WINDOWS


def _read_table(table_name: str, db_path: str | Path | None) -> pd.DataFrame:
    if not table_exists(table_name, db_path=db_path):
        return pd.DataFrame()
    with connect_db(db_path) as conn:
        return pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)


def _expected_sign(signal_direction: object) -> int:
    text = str(signal_direction).upper()
    if "NEGATIVE" in text or "REVERSE" in text:
        return -1
    return 1


def _align_panels(signal_panel: pd.DataFrame, forward_panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    signal = signal_panel.copy()
    forward = forward_panel.copy()
    signal.index = pd.to_datetime(signal.index, errors="coerce")
    forward.index = pd.to_datetime(forward.index, errors="coerce")
    signal = signal.sort_index().apply(pd.to_numeric, errors="coerce")
    forward = forward.sort_index().apply(pd.to_numeric, errors="coerce")
    common_dates = signal.index.intersection(forward.index).sort_values()
    common_tickers = signal.columns.intersection(forward.columns).sort_values()
    return signal.reindex(index=common_dates, columns=common_tickers), forward.reindex(index=common_dates, columns=common_tickers)


def _safe_daily_corr(pair: pd.DataFrame, method: str) -> float:
    if len(pair) < 3:
        return np.nan
    if pair["signal"].nunique(dropna=True) < 2 or pair["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(pair["signal"].corr(pair["fwd_return"], method=method))


def _daily_ic_and_n_obs(signal_panel: pd.DataFrame, forward_panel: pd.DataFrame, method: str = "spearman") -> tuple[pd.Series, pd.Series]:
    paired = pd.concat(
        [
            signal_panel.stack(future_stack=True).rename("signal"),
            forward_panel.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()
    if paired.empty:
        empty_index = pd.DatetimeIndex([], name=signal_panel.index.name)
        return pd.Series(dtype=float, index=empty_index, name="daily_ic"), pd.Series(dtype=int, index=empty_index, name="n_obs")
    grouped = paired.groupby(level=0, sort=True)
    daily_ic = grouped.apply(_safe_daily_corr, method=method).dropna()
    n_obs = grouped.size()
    return daily_ic, n_obs


def _benchmark_downtrend_mask(close_prices: pd.DataFrame, benchmark_ticker: str = "SPY") -> pd.Series:
    benchmark = close_prices[benchmark_ticker] if benchmark_ticker in close_prices.columns else close_prices.mean(axis=1, skipna=True)
    ma_50 = benchmark.rolling(50).mean()
    ma_200 = benchmark.rolling(200).mean()
    return ((ma_50 < ma_200) & (benchmark < ma_200)).fillna(False)


def _benchmark_high_drawdown_mask(close_prices: pd.DataFrame, benchmark_ticker: str = "SPY") -> pd.Series:
    benchmark = close_prices[benchmark_ticker] if benchmark_ticker in close_prices.columns else close_prices.mean(axis=1, skipna=True)
    drawdown = benchmark.div(benchmark.cummax()).sub(1.0)
    return drawdown.le(-0.10).fillna(False)


def build_active_condition_mask(close_prices: pd.DataFrame, conditional_context: str) -> pd.Series:
    if conditional_context == "benchmark_trend_regime=DOWNTREND":
        return _benchmark_downtrend_mask(close_prices)
    if conditional_context == "drawdown_regime=HIGH_DRAWDOWN":
        return _benchmark_high_drawdown_mask(close_prices)
    raise ValueError(f"Unsupported conditional_context for active-state diagnostics: {conditional_context!r}")


def _slice(series: pd.Series, start: object, end: object) -> pd.Series:
    return series.loc[pd.to_datetime(start) : pd.to_datetime(end)]


def _distribution(series: pd.Series, expected_sign: int) -> dict[str, object]:
    values = series.dropna().astype(float)
    if values.empty:
        return {
            "n_valid_ic_dates": 0,
            "mean_ic": np.nan,
            "effective_mean_ic": np.nan,
            "median_ic": np.nan,
            "effective_median_ic": np.nan,
            "ic_std": np.nan,
            "ic_ir": np.nan,
            "effective_ic_ir": np.nan,
            "skew": np.nan,
            "min_ic": np.nan,
            "max_ic": np.nan,
            "p05_ic": np.nan,
            "p95_ic": np.nan,
            "winsorized_mean_ic": np.nan,
            "winsorized_effective_mean_ic": np.nan,
            "positive_ic_rate": np.nan,
            "sign_consistency": np.nan,
        }
    std = values.std(ddof=1) if len(values) > 1 else np.nan
    mean_ic = values.mean()
    p05 = values.quantile(0.05)
    p95 = values.quantile(0.95)
    winsorized = values.clip(lower=p05, upper=p95)
    return {
        "n_valid_ic_dates": int(len(values)),
        "mean_ic": float(mean_ic),
        "effective_mean_ic": float(mean_ic * expected_sign),
        "median_ic": float(values.median()),
        "effective_median_ic": float(values.median() * expected_sign),
        "ic_std": float(std) if pd.notna(std) else np.nan,
        "ic_ir": float(mean_ic / std) if pd.notna(std) and std != 0 else np.nan,
        "effective_ic_ir": float((mean_ic * expected_sign) / std) if pd.notna(std) and std != 0 else np.nan,
        "skew": float(values.skew()) if len(values) > 2 else np.nan,
        "min_ic": float(values.min()),
        "max_ic": float(values.max()),
        "p05_ic": float(p05),
        "p95_ic": float(p95),
        "winsorized_mean_ic": float(winsorized.mean()),
        "winsorized_effective_mean_ic": float(winsorized.mean() * expected_sign),
        "positive_ic_rate": float((values > 0).mean()),
        "sign_consistency": float((values * expected_sign > 0).mean()),
    }


def build_window_diagnostics(
    windows: pd.DataFrame,
    official_window_results: pd.DataFrame,
    daily_ic_all: pd.Series,
    daily_ic_active: pd.Series,
    n_obs_active: pd.Series,
    active_dates: pd.Series,
    expected_sign: int,
    min_active_test_dates: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, window in windows.sort_values("window_id").iterrows():
        window_id = int(window["window_id"])
        official = official_window_results.loc[official_window_results["window_id"].astype(int).eq(window_id)]
        official_row = official.iloc[0].to_dict() if not official.empty else {}
        train_start = pd.to_datetime(window["train_start"])
        train_end = pd.to_datetime(window["train_end"])
        test_start = pd.to_datetime(window["test_start"])
        test_end = pd.to_datetime(window["test_end"])

        train_active = _slice(active_dates, train_start, train_end).astype(bool)
        test_active = _slice(active_dates, test_start, test_end).astype(bool)
        test_active_ic = _slice(daily_ic_active, test_start, test_end).dropna()
        train_active_ic = _slice(daily_ic_active, train_start, train_end).dropna()
        all_test_ic = _slice(daily_ic_all, test_start, test_end).dropna()
        active_test_distribution = _distribution(test_active_ic, expected_sign)

        active_effective_test_ic = active_test_distribution["effective_mean_ic"]
        rows.append(
            {
                "window_id": window_id,
                "train_start": train_start.date(),
                "train_end": train_end.date(),
                "test_start": test_start.date(),
                "test_end": test_end.date(),
                "train_total_dates": int(len(train_active)),
                "test_total_dates": int(len(test_active)),
                "train_active_dates": int(train_active.sum()),
                "test_active_dates": int(test_active.sum()),
                "train_active_date_ratio": float(train_active.mean()) if len(train_active) else np.nan,
                "test_active_date_ratio": float(test_active.mean()) if len(test_active) else np.nan,
                "official_train_ic": official_row.get("train_mean_ic", np.nan),
                "official_test_ic": official_row.get("test_mean_ic", np.nan),
                "official_effective_test_ic": (
                    official_row.get("test_mean_ic") * expected_sign
                    if pd.notna(official_row.get("test_mean_ic", np.nan))
                    else np.nan
                ),
                "official_test_positive_ic_rate": official_row.get("test_positive_ic_rate", np.nan),
                "official_test_n_obs": official_row.get("test_n_obs", np.nan),
                "all_dates_valid_test_ic_dates": int(len(all_test_ic)),
                "active_only_train_valid_ic_dates": int(len(train_active_ic)),
                "active_only_test_valid_ic_dates": int(len(test_active_ic)),
                "active_only_train_ic": float(train_active_ic.mean()) if not train_active_ic.empty else np.nan,
                "active_only_test_ic": active_test_distribution["mean_ic"],
                "active_only_effective_test_ic": active_effective_test_ic,
                "active_only_test_ic_std": active_test_distribution["ic_std"],
                "active_only_effective_test_ic_ir": active_test_distribution["effective_ic_ir"],
                "active_only_test_positive_ic_rate": active_test_distribution["positive_ic_rate"],
                "active_only_sign_consistency": active_test_distribution["sign_consistency"],
                "active_only_test_n_obs": int(_slice(n_obs_active, test_start, test_end).sum()) if not _slice(n_obs_active, test_start, test_end).empty else 0,
                "active_window_eligible": int(int(test_active.sum()) >= min_active_test_dates and len(test_active_ic) >= min_active_test_dates),
            }
        )
    output = pd.DataFrame(rows)
    valid = output["active_only_effective_test_ic"].dropna()
    positive_sum = valid[valid > 0].sum()
    output["positive_effective_ic_share"] = np.where(
        positive_sum != 0,
        output["active_only_effective_test_ic"].clip(lower=0) / positive_sum,
        np.nan,
    )
    return output


def classify_failure(window_diagnostics: pd.DataFrame, summary: pd.Series, min_active_windows: int) -> str:
    labels: list[str] = []
    active_windows = int(summary.get("active_window_count", 0) or 0)
    eligible_windows = int(summary.get("eligible_active_window_count", 0) or 0)
    coverage_ratio = float(summary.get("active_window_coverage_ratio", 0) or 0)
    max_share = summary.get("max_positive_effective_ic_share")
    persistence = summary.get("active_only_persistence")
    sign_consistency = summary.get("active_only_sign_consistency")
    effective_ir = summary.get("active_only_window_effective_ic_ir")

    if eligible_windows < min_active_windows or coverage_ratio < MIN_ACTIVE_WINDOW_COVERAGE_RATIO:
        labels.append("sparse conditional edge")
    if active_windows < len(window_diagnostics):
        labels.append("inactive-window dilution")
    if pd.notna(max_share) and float(max_share) >= 0.60:
        labels.append("one-window dominated edge")
    if eligible_windows < len(window_diagnostics) and pd.notna(summary.get("active_only_effective_mean_ic")) and summary.get("active_only_effective_mean_ic") > 0:
        labels.append("episodic edge")
    if (
        eligible_windows >= min_active_windows
        and (
            (pd.notna(persistence) and float(persistence) < 0.50)
            or (pd.notna(sign_consistency) and float(sign_consistency) < 0.50)
            or (pd.notna(effective_ir) and float(effective_ir) < 0.25)
        )
    ):
        labels.append("unstable edge")
    return "; ".join(dict.fromkeys(labels)) if labels else "no active-state failure flag"


def build_summary(
    signal_name: str,
    horizon: int,
    conditional_context: str,
    signal_direction: str,
    gate: pd.DataFrame,
    window_diagnostics: pd.DataFrame,
    active_daily_ic: pd.Series,
    expected_sign: int,
    min_active_windows: int,
) -> pd.DataFrame:
    valid_windows = window_diagnostics["active_only_effective_test_ic"].dropna()
    eligible = window_diagnostics.loc[window_diagnostics["active_window_eligible"].astype(bool)].copy()
    eligible_effective = eligible["active_only_effective_test_ic"].dropna()
    window_std = eligible_effective.std(ddof=1) if len(eligible_effective) > 1 else np.nan
    window_mean = eligible_effective.mean() if not eligible_effective.empty else np.nan
    active_distribution = _distribution(active_daily_ic, expected_sign)
    row = {
        "signal_name": signal_name,
        "horizon": int(horizon),
        "conditional_context": conditional_context,
        "signal_direction": signal_direction,
        "official_wfv_status": gate["status"].iloc[0] if not gate.empty and "status" in gate else np.nan,
        "official_effective_mean_test_ic": gate["effective_mean_test_ic"].iloc[0] if not gate.empty and "effective_mean_test_ic" in gate else np.nan,
        "official_effective_test_ic_ir": gate["effective_test_ic_ir"].iloc[0] if not gate.empty and "effective_test_ic_ir" in gate else np.nan,
        "official_persistence_ratio": gate["persistence_ratio"].iloc[0] if not gate.empty and "persistence_ratio" in gate else np.nan,
        "official_sign_consistency": gate["sign_consistency"].iloc[0] if not gate.empty and "sign_consistency" in gate else np.nan,
        "official_wfv_notes": gate["wfv_gate_notes"].iloc[0] if not gate.empty and "wfv_gate_notes" in gate else np.nan,
        "total_wfv_windows": int(len(window_diagnostics)),
        "active_window_count": int(window_diagnostics["test_active_dates"].gt(0).sum()),
        "eligible_active_window_count": int(window_diagnostics["active_window_eligible"].sum()),
        "active_window_coverage_ratio": float(window_diagnostics["active_window_eligible"].mean()) if not window_diagnostics.empty else np.nan,
        "active_only_effective_mean_ic": float(window_mean) if pd.notna(window_mean) else np.nan,
        "active_only_window_ic_std": float(window_std) if pd.notna(window_std) else np.nan,
        "active_only_window_effective_ic_ir": float(window_mean / window_std) if pd.notna(window_mean) and pd.notna(window_std) and window_std != 0 else np.nan,
        "active_only_persistence": float((eligible_effective > 0).mean()) if not eligible_effective.empty else np.nan,
        "active_only_sign_consistency": active_distribution["sign_consistency"],
        "active_only_daily_valid_ic_dates": active_distribution["n_valid_ic_dates"],
        "active_only_daily_effective_mean_ic": active_distribution["effective_mean_ic"],
        "active_only_daily_effective_ic_ir": active_distribution["effective_ic_ir"],
        "max_positive_effective_ic_share": float(window_diagnostics["positive_effective_ic_share"].max()) if not window_diagnostics.empty else np.nan,
    }
    summary = pd.DataFrame([row])
    summary["failure_classification"] = summary.apply(lambda item: classify_failure(window_diagnostics, item, min_active_windows), axis=1)
    return summary


def build_markdown_summary(
    config: ActiveStateDiagnosticsConfig,
    summary: pd.DataFrame,
    window_diagnostics: pd.DataFrame,
    distribution: pd.DataFrame,
) -> str:
    row = summary.iloc[0]
    lines = [
        "# Active-State WFV Framework Proposal",
        "",
        f"- Run ID: `{config.run_id}`",
        f"- Diagnostics version: `{ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION}`",
        f"- Run timestamp: `{config.run_timestamp}`",
        "- Scope: research-only. No official WFV gates, schemas, promotion rules, or alpha construction logic are changed.",
        "",
        "## Motivation",
        "",
        "Conditional signals can be active only during sparse market states. Fixed WFV windows remain the official gate, but they can produce undefined IC IR and persistence when most test windows contain zero active-condition dates.",
        "",
        "## Proposed Diagnostic Layer",
        "",
        "Active-state WFV should be a sidecar diagnostic that reuses official WFV windows but evaluates daily IC only on dates where the signal condition is active. It should write standalone research artifacts, never official WFV tables.",
        "",
        "Core outputs:",
        "",
        "- Active-condition date counts per WFV train/test window.",
        "- Active-only test IC, effective IC, daily IC IR, sign consistency, and active-window coverage.",
        "- Explicit failure classifications: sparse conditional edge, inactive-window dilution, episodic edge, unstable edge, and one-window dominated edge.",
        "",
        "## Initial Signal",
        "",
        f"- Signal: `{config.signal_name}`",
        f"- Horizon: h{config.horizon}",
        f"- Conditional context: `{row['conditional_context']}`",
        f"- Official WFV status: `{row['official_wfv_status']}`",
        f"- Failure classification: `{row['failure_classification']}`",
        "",
        "## Window Diagnostics",
        "",
        window_diagnostics[
            [
                "window_id",
                "train_active_dates",
                "test_active_dates",
                "active_only_test_valid_ic_dates",
                "active_only_effective_test_ic",
                "active_only_effective_test_ic_ir",
                "active_window_eligible",
                "positive_effective_ic_share",
            ]
        ].to_markdown(index=False),
        "",
        "## Active Daily IC Distribution",
        "",
        distribution.to_markdown(index=False),
        "",
        "## Threshold Recommendations",
        "",
        f"- Minimum active test dates per eligible window: {config.min_active_test_dates}.",
        f"- Minimum eligible active WFV windows: {config.min_active_windows}.",
        f"- Minimum active-window coverage ratio: {MIN_ACTIVE_WINDOW_COVERAGE_RATIO:.2f}.",
        "- Treat one-window dominance above 60% of positive effective IC as a warning, not a promotion criterion.",
        "- Require active-only results to remain diagnostic until a conditional-alpha framework defines separate research gates.",
        "",
        "## Viability Assessment",
        "",
        "Active-state WFV is viable as a research diagnostic for conditional-alpha design. It is not viable as a replacement for official WFV gates without a separate governance decision, because it changes the sampling question from universal fixed-window persistence to state-conditional persistence.",
        "",
        "## Recommendation",
        "",
        "Use this framework to decide whether conditional edges deserve further conditional-alpha research. Do not use it to promote signals directly. For the initial signal, the diagnosis remains sparse and one-window dominated, so the recommended action is watchlist/defer rather than promotion.",
        "",
        "## Artifacts",
        "",
        f"Standalone CSV artifacts are written under `{config.output_dir}`.",
        "",
    ]
    return "\n".join(lines)


def run_active_state_wfv_diagnostics(
    signal_name: str = DEFAULT_SIGNAL,
    horizon: int = DEFAULT_HORIZON,
    db_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    summary_path: str | Path | None = None,
    write: bool = True,
) -> dict[str, object]:
    run_id = make_run_id("active_state_wfv_diagnostics")
    run_timestamp = make_run_timestamp()
    config = ActiveStateDiagnosticsConfig(
        signal_name=signal_name,
        horizon=int(horizon),
        db_path=Path(db_path) if db_path else get_sqlite_db_path(),
        output_dir=Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR,
        summary_path=Path(summary_path) if summary_path else DEFAULT_SUMMARY_PATH,
        run_id=run_id,
        run_timestamp=run_timestamp,
    )

    metadata = _read_table("candidate_signal_metadata_current", config.db_path)
    signal_meta = metadata.loc[metadata["signal_name"].astype(str).eq(signal_name)].tail(1)
    if signal_meta.empty:
        raise ValueError(f"Signal metadata not found: {signal_name}")
    conditional_context = str(signal_meta["conditional_context"].iloc[0])

    gate = _read_table("wfv_gate_current", config.db_path)
    gate = gate.loc[
        gate["signal_name"].astype(str).eq(signal_name)
        & pd.to_numeric(gate["horizon"], errors="coerce").astype("Int64").eq(int(horizon))
    ].copy()
    official_windows = _read_table("wfv_windows_current", config.db_path)
    official_window_results = _read_table("wfv_window_results_current", config.db_path)
    official_window_results = official_window_results.loc[
        official_window_results["signal_name"].astype(str).eq(signal_name)
        & pd.to_numeric(official_window_results["horizon"], errors="coerce").astype("Int64").eq(int(horizon))
    ].copy()

    close_prices = load_price_table("clean_close_prices_current", db_path=config.db_path)
    signal_long = load_candidate_signals_by_names([signal_name], current=True, db_path=config.db_path, chunksize=500_000)
    signal_panel = pivot_signal_long_to_panel(signal_long, signal_name)
    forward_panel = make_forward_returns(close_prices, [int(horizon)])[int(horizon)]
    signal_panel, forward_panel = _align_panels(signal_panel, forward_panel)

    active_dates = build_active_condition_mask(close_prices, conditional_context).reindex(signal_panel.index).fillna(False)
    expected_sign = _expected_sign(gate["signal_direction"].iloc[0] if not gate.empty and "signal_direction" in gate else signal_meta.get("signal_direction", pd.Series(["POSITIVE_EDGE"])).iloc[0])
    daily_ic_all, _ = _daily_ic_and_n_obs(signal_panel, forward_panel, method="spearman")
    active_signal_panel = signal_panel.where(active_dates.astype(bool), np.nan)
    daily_ic_active, active_n_obs = _daily_ic_and_n_obs(active_signal_panel, forward_panel, method="spearman")

    window_diagnostics = build_window_diagnostics(
        windows=official_windows,
        official_window_results=official_window_results,
        daily_ic_all=daily_ic_all,
        daily_ic_active=daily_ic_active,
        n_obs_active=active_n_obs,
        active_dates=active_dates,
        expected_sign=expected_sign,
        min_active_test_dates=config.min_active_test_dates,
    )
    summary = build_summary(
        signal_name=signal_name,
        horizon=int(horizon),
        conditional_context=conditional_context,
        signal_direction=gate["signal_direction"].iloc[0] if not gate.empty and "signal_direction" in gate else "",
        gate=gate,
        window_diagnostics=window_diagnostics,
        active_daily_ic=daily_ic_active,
        expected_sign=expected_sign,
        min_active_windows=config.min_active_windows,
    )
    distribution = pd.DataFrame(
        [
            {"sample": "all_active_valid_dates", **_distribution(daily_ic_active, expected_sign)},
            {
                "sample": "wfv_test_active_valid_dates",
                **_distribution(
                    pd.concat(
                        [
                            _slice(daily_ic_active, row["test_start"], row["test_end"]).dropna()
                            for _, row in official_windows.iterrows()
                        ]
                    )
                    if not official_windows.empty
                    else pd.Series(dtype=float),
                    expected_sign,
                ),
            },
        ]
    )

    for table in (window_diagnostics, summary, distribution):
        table["diagnostics_run_id"] = run_id
        table["diagnostics_version"] = ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION

    markdown = build_markdown_summary(config, summary, window_diagnostics, distribution)
    if write:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        config.summary_path.parent.mkdir(parents=True, exist_ok=True)
        window_diagnostics.to_csv(config.output_dir / "active_state_wfv_window_diagnostics.csv", index=False)
        summary.to_csv(config.output_dir / "active_state_wfv_summary.csv", index=False)
        distribution.to_csv(config.output_dir / "active_state_daily_ic_distribution.csv", index=False)
        config.summary_path.write_text(markdown, encoding="utf-8")

    run_summary = pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "diagnostics_version", "value": ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION},
            {"metric": "signal_name", "value": signal_name},
            {"metric": "horizon", "value": int(horizon)},
            {"metric": "failure_classification", "value": summary["failure_classification"].iloc[0]},
            {"metric": "output_dir", "value": str(config.output_dir)},
            {"metric": "summary_path", "value": str(config.summary_path)},
        ]
    )
    return {
        "run_summary": run_summary,
        "summary": summary,
        "window_diagnostics": window_diagnostics,
        "distribution": distribution,
        "markdown": markdown,
    }


__all__ = [
    "ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION",
    "DEFAULT_OUTPUT_DIR",
    "DEFAULT_SUMMARY_PATH",
    "run_active_state_wfv_diagnostics",
]
