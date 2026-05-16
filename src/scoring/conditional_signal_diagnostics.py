"""Conditional signal diagnostics for Batch 3 research.

This module is intentionally research-only. It reads existing scoring outputs
and OHLCV panels, derives market-state labels, and writes standalone artifacts.
It does not modify signal formulas, gates, WFV logic, or SQLite schemas.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import connect_db, load_price_table, table_exists
from src.run_config import get_project_root, get_sqlite_db_path, make_run_id, make_run_timestamp
from src.scoring.regime_ic import build_regime_features_for_ic


CONDITIONAL_DIAGNOSTICS_VERSION = "batch3_conditional_signal_diagnostics_v1"
DEFAULT_FOCUS_SIGNALS = (
    "trend_consistency_20_60",
    "trend_consistency_20_60_persistent",
    "index_relative_reversal_5",
    "percentile_rank_stability_20",
    "smooth_trend_persistence_60",
)
DEFAULT_OUTPUT_DIR = get_project_root() / "artifacts" / "research" / "conditional_signal_diagnostics"
DEFAULT_SUMMARY_PATH = get_project_root() / "docs" / "research_notes" / "batch3_conditional_signal_research.md"
HORIZONS = (1, 5, 10, 20)
MIN_SAMPLE_DAYS = 126
PROMISING_EFFECTIVE_IC = 0.015
WEAK_EFFECTIVE_IC = 0.008

CONTEXT_COLUMNS = (
    "benchmark_trend_regime",
    "benchmark_vol_regime",
    "drawdown_regime",
    "correlation_regime",
    "dispersion_regime",
    "breadth_regime",
    "participation_regime",
    "risk_regime",
)


@dataclass(frozen=True)
class ConditionalDiagnosticsConfig:
    focus_signals: tuple[str, ...] = DEFAULT_FOCUS_SIGNALS
    output_dir: Path = DEFAULT_OUTPUT_DIR
    summary_path: Path = DEFAULT_SUMMARY_PATH
    db_path: Path = get_sqlite_db_path()
    run_id: str = ""
    run_timestamp: str = ""


def _read_table(table_name: str, db_path: str | Path | None) -> pd.DataFrame:
    if not table_exists(table_name, db_path=db_path):
        return pd.DataFrame()
    with connect_db(db_path) as conn:
        return pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)


def _tercile_label(values: pd.Series, low_label: str, mid_label: str, high_label: str) -> pd.Series:
    valid = values.dropna()
    output = pd.Series(np.nan, index=values.index, dtype="object")
    if valid.empty:
        return output
    low_threshold = valid.quantile(1 / 3)
    high_threshold = valid.quantile(2 / 3)
    output.loc[values <= low_threshold] = low_label
    output.loc[(values > low_threshold) & (values < high_threshold)] = mid_label
    output.loc[values >= high_threshold] = high_label
    return output


def _expected_sign(signal_direction: object) -> int:
    direction = str(signal_direction).upper()
    if "NEGATIVE" in direction or "REVERSE" in direction:
        return -1
    return 1


def _window_persistence(effective_ic: pd.Series, n_windows: int = 4) -> float:
    values = effective_ic.dropna()
    if values.empty:
        return np.nan
    ordered = values.sort_index()
    chunk_count = min(n_windows, len(ordered))
    split_points = np.linspace(0, len(ordered), chunk_count + 1, dtype=int)
    chunks = [ordered.iloc[split_points[i] : split_points[i + 1]] for i in range(chunk_count)]
    window_means = [chunk.mean() for chunk in chunks if len(chunk) > 0]
    if not window_means:
        return np.nan
    return float(np.mean([mean > 0 for mean in window_means]))


def build_context_features(close_prices: pd.DataFrame, benchmark_ticker: str = "SPY") -> pd.DataFrame:
    """Build OHLCV-only conditional market-state labels."""
    close = close_prices.copy()
    close.index = pd.to_datetime(close.index, errors="coerce")
    close = close.sort_index().apply(pd.to_numeric, errors="coerce")
    if benchmark_ticker not in close.columns:
        raise ValueError(f"benchmark_ticker '{benchmark_ticker}' not found in close prices.")

    base = build_regime_features_for_ic(close, benchmark_ticker=benchmark_ticker)
    base["Date"] = pd.to_datetime(base["Date"], errors="coerce")
    features = base.set_index("Date").sort_index()

    assets = close.drop(columns=[benchmark_ticker], errors="ignore")
    returns_1d = assets.pct_change(fill_method=None)
    dispersion_1d = returns_1d.std(axis=1, skipna=True)
    breadth_20d = assets.pct_change(20, fill_method=None).gt(0).mean(axis=1, skipna=True)
    ma_50 = assets.rolling(50).mean()
    participation_50d = assets.gt(ma_50).mean(axis=1, skipna=True)

    features["cross_sectional_dispersion_1d"] = dispersion_1d
    features["positive_return_breadth_20d"] = breadth_20d
    features["above_ma50_participation"] = participation_50d
    features["dispersion_regime"] = _tercile_label(
        dispersion_1d,
        "LOW_DISPERSION",
        "MID_DISPERSION",
        "HIGH_DISPERSION",
    )
    features["breadth_regime"] = _tercile_label(
        breadth_20d,
        "LOW_BREADTH",
        "MID_BREADTH",
        "HIGH_BREADTH",
    )
    features["participation_regime"] = _tercile_label(
        participation_50d,
        "LOW_PARTICIPATION",
        "MID_PARTICIPATION",
        "HIGH_PARTICIPATION",
    )

    benchmark = close[benchmark_ticker]
    benchmark_return_20d = benchmark.pct_change(20, fill_method=None)
    high_vol_threshold = features["benchmark_vol_20d"].dropna().quantile(2 / 3)
    risk_regime = pd.Series("MIXED_RISK", index=features.index, dtype="object")
    risk_regime.loc[
        (benchmark_return_20d > 0)
        & (features["market_drawdown"] > -0.05)
        & (features["benchmark_vol_20d"] < high_vol_threshold)
    ] = "RISK_ON"
    risk_regime.loc[
        (benchmark_return_20d < 0)
        | (features["market_drawdown"] <= -0.10)
        | (features["benchmark_vol_20d"] >= high_vol_threshold)
    ] = "RISK_OFF"
    risk_regime.loc[benchmark_return_20d.isna() | features["benchmark_vol_20d"].isna()] = np.nan
    features["benchmark_return_20d"] = benchmark_return_20d
    features["risk_regime"] = risk_regime

    return features.reset_index()


def build_daily_ic_base(
    daily_ic: pd.DataFrame,
    scoring_gate: pd.DataFrame,
    focus_signals: tuple[str, ...],
) -> pd.DataFrame:
    if daily_ic.empty:
        return pd.DataFrame()
    base = daily_ic.loc[daily_ic["signal_name"].astype(str).isin(focus_signals)].copy()
    base["Date"] = pd.to_datetime(base["Date"], errors="coerce")
    base["horizon"] = pd.to_numeric(base["horizon"], errors="coerce").astype("Int64")
    base["daily_ic"] = pd.to_numeric(base["daily_ic"], errors="coerce")
    base = (
        base.groupby(["Date", "signal_name", "horizon"], dropna=False, as_index=False)
        .agg(daily_ic=("daily_ic", "mean"))
        .dropna(subset=["Date", "signal_name", "horizon"])
    )

    metadata = scoring_gate.loc[scoring_gate["signal_name"].astype(str).isin(focus_signals)].copy()
    if metadata.empty:
        base["signal_direction"] = "POSITIVE_EDGE"
        base["unconditional_mean_ic"] = np.nan
        base["unconditional_effective_mean_ic"] = np.nan
        return base

    metadata["horizon"] = pd.to_numeric(metadata["horizon"], errors="coerce").astype("Int64")
    metadata["mean_ic"] = pd.to_numeric(metadata["mean_ic"], errors="coerce")
    metadata = metadata[
        [
            "signal_name",
            "horizon",
            "signal_family",
            "signal_direction",
            "status",
            "mean_ic",
            "abs_mean_ic",
            "positive_ic_rate",
        ]
    ].drop_duplicates(["signal_name", "horizon"], keep="last")

    output = base.merge(metadata, on=["signal_name", "horizon"], how="left")
    output["signal_direction"] = output["signal_direction"].fillna("POSITIVE_EDGE")
    output["expected_sign"] = output["signal_direction"].map(_expected_sign)
    output["effective_daily_ic"] = output["daily_ic"] * output["expected_sign"]
    output["unconditional_mean_ic"] = output["mean_ic"]
    output["unconditional_effective_mean_ic"] = output["mean_ic"] * output["expected_sign"]
    return output


def classify_conditional_edge(row: pd.Series) -> str:
    n_days = int(row.get("n_days") or 0)
    effective_mean_ic = row.get("effective_mean_ic")
    sign_consistency = row.get("sign_consistency")
    persistence = row.get("window_persistence")
    if n_days < MIN_SAMPLE_DAYS:
        return "INSUFFICIENT_SAMPLE"
    if pd.notna(effective_mean_ic) and effective_mean_ic < -0.005:
        return "DIRECTION_FLIP_RISK"
    if pd.notna(sign_consistency) and sign_consistency < 0.45:
        return "DIRECTION_FLIP_RISK"
    if (
        pd.notna(effective_mean_ic)
        and pd.notna(sign_consistency)
        and pd.notna(persistence)
        and effective_mean_ic >= PROMISING_EFFECTIVE_IC
        and sign_consistency >= 0.54
        and persistence >= 0.75
    ):
        return "PROMISING_CONDITIONAL_EDGE"
    if (
        pd.notna(effective_mean_ic)
        and pd.notna(sign_consistency)
        and pd.notna(persistence)
        and effective_mean_ic >= WEAK_EFFECTIVE_IC
        and sign_consistency >= 0.51
        and persistence >= 0.50
    ):
        return "WEAK_CONDITIONAL_EDGE"
    return "AVOID"


def build_conditional_ic_diagnostics(daily_ic_base: pd.DataFrame, context_features: pd.DataFrame) -> pd.DataFrame:
    if daily_ic_base.empty or context_features.empty:
        return pd.DataFrame()
    contexts = context_features[["Date", *CONTEXT_COLUMNS]].copy()
    contexts["Date"] = pd.to_datetime(contexts["Date"], errors="coerce")
    merged = daily_ic_base.merge(contexts, on="Date", how="left")

    rows: list[dict[str, object]] = []
    for context_column in CONTEXT_COLUMNS:
        valid = merged.dropna(subset=[context_column, "daily_ic"]).copy()
        for keys, group in valid.groupby(["signal_name", "horizon", context_column], dropna=False):
            signal_name, horizon, context_value = keys
            ordered = group.sort_values("Date")
            daily_ic = ordered["daily_ic"]
            effective_ic = ordered["effective_daily_ic"]
            unconditional = ordered["unconditional_effective_mean_ic"].dropna()
            unconditional_effective = unconditional.iloc[-1] if not unconditional.empty else np.nan
            mean_ic = float(daily_ic.mean()) if not daily_ic.empty else np.nan
            effective_mean_ic = float(effective_ic.mean()) if not effective_ic.empty else np.nan
            degradation = (
                effective_mean_ic - float(unconditional_effective)
                if pd.notna(effective_mean_ic) and pd.notna(unconditional_effective)
                else np.nan
            )
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "context_column": context_column,
                    "context_value": context_value,
                    "n_days": int(daily_ic.notna().sum()),
                    "sample_start": ordered["Date"].min(),
                    "sample_end": ordered["Date"].max(),
                    "mean_ic": mean_ic,
                    "median_ic": float(daily_ic.median()) if not daily_ic.empty else np.nan,
                    "ic_std": float(daily_ic.std(ddof=1)) if len(daily_ic.dropna()) > 1 else np.nan,
                    "ic_ir": (
                        float(mean_ic / daily_ic.std(ddof=1))
                        if len(daily_ic.dropna()) > 1 and daily_ic.std(ddof=1) not in (0, np.nan)
                        else np.nan
                    ),
                    "positive_ic_rate": float(daily_ic.gt(0).mean()) if not daily_ic.empty else np.nan,
                    "effective_mean_ic": effective_mean_ic,
                    "sign_consistency": float(effective_ic.gt(0).mean()) if not effective_ic.empty else np.nan,
                    "window_persistence": _window_persistence(effective_ic),
                    "unconditional_effective_mean_ic": unconditional_effective,
                    "degradation_vs_unconditional_ic": degradation,
                    "signal_direction": ordered["signal_direction"].iloc[-1],
                    "signal_family": ordered.get("signal_family", pd.Series(dtype=object)).iloc[-1]
                    if "signal_family" in ordered.columns
                    else np.nan,
                    "scoring_status": ordered.get("status", pd.Series(dtype=object)).iloc[-1]
                    if "status" in ordered.columns
                    else np.nan,
                }
            )

    output = pd.DataFrame(rows)
    if output.empty:
        return output
    output["edge_classification"] = output.apply(classify_conditional_edge, axis=1)
    return output.sort_values(
        ["signal_name", "horizon", "context_column", "effective_mean_ic"],
        ascending=[True, True, True, False],
    ).reset_index(drop=True)


def build_signal_context_summary(conditional: pd.DataFrame) -> pd.DataFrame:
    if conditional.empty:
        return pd.DataFrame()
    counts = (
        conditional.groupby(["signal_name", "horizon", "edge_classification"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for column in [
        "PROMISING_CONDITIONAL_EDGE",
        "WEAK_CONDITIONAL_EDGE",
        "DIRECTION_FLIP_RISK",
        "INSUFFICIENT_SAMPLE",
        "AVOID",
    ]:
        if column not in counts.columns:
            counts[column] = 0
    best = conditional.sort_values("effective_mean_ic", ascending=False).drop_duplicates(["signal_name", "horizon"])
    return counts.merge(
        best[
            [
                "signal_name",
                "horizon",
                "context_column",
                "context_value",
                "effective_mean_ic",
                "sign_consistency",
                "window_persistence",
                "n_days",
            ]
        ],
        on=["signal_name", "horizon"],
        how="left",
    ).rename(
        columns={
            "context_column": "best_context_column",
            "context_value": "best_context_value",
            "effective_mean_ic": "best_effective_mean_ic",
        }
    )


def build_batch3_recommendations(conditional: pd.DataFrame) -> pd.DataFrame:
    if conditional.empty:
        return pd.DataFrame()
    candidates = conditional.loc[
        conditional["edge_classification"].isin(["PROMISING_CONDITIONAL_EDGE", "WEAK_CONDITIONAL_EDGE"])
        & conditional["n_days"].ge(MIN_SAMPLE_DAYS)
    ].copy()
    candidates["classification_rank"] = candidates["edge_classification"].map(
        {"PROMISING_CONDITIONAL_EDGE": 0, "WEAK_CONDITIONAL_EDGE": 1}
    )
    candidates = candidates.sort_values(
        [
            "classification_rank",
            "effective_mean_ic",
            "sign_consistency",
            "window_persistence",
            "n_days",
        ],
        ascending=[True, False, False, False, False],
    )
    selected = candidates.drop_duplicates("signal_name").head(3).copy()
    rows: list[dict[str, object]] = []
    for _, row in selected.iterrows():
        rows.append(
            {
                "recommended_variant": f"{row['signal_name']}__conditioned_on__{row['context_value']}".lower(),
                "source_signal": row["signal_name"],
                "horizon": int(row["horizon"]),
                "condition_column": row["context_column"],
                "condition_value": row["context_value"],
                "edge_classification": row["edge_classification"],
                "n_days": int(row["n_days"]),
                "effective_mean_ic": row["effective_mean_ic"],
                "sign_consistency": row["sign_consistency"],
                "window_persistence": row["window_persistence"],
                "degradation_vs_unconditional_ic": row["degradation_vs_unconditional_ic"],
                "formula_policy": "Do not change source formula; only research a minimal OHLCV-only condition.",
                "targeted_failure_mode": "WFV instability, direction flips, weak persistence, or low sign consistency.",
            }
        )
    return pd.DataFrame(rows)


def _format_float(value: object, digits: int = 4) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{float(value):.{digits}f}"


def _markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int = 12) -> list[str]:
    if df.empty:
        return ["No rows available."]
    frame = df.loc[:, [column for column in columns if column in df.columns]].head(max_rows).copy()
    return frame.to_markdown(index=False).splitlines()


def build_markdown_summary(tables: dict[str, pd.DataFrame], config: ConditionalDiagnosticsConfig) -> str:
    conditional = tables["conditional_ic_by_context"]
    recommendations = tables["batch3_candidate_recommendations"]
    promising = conditional.loc[conditional["edge_classification"].eq("PROMISING_CONDITIONAL_EDGE")].sort_values(
        "effective_mean_ic",
        ascending=False,
    )
    weak = conditional.loc[conditional["edge_classification"].eq("WEAK_CONDITIONAL_EDGE")].sort_values(
        "effective_mean_ic",
        ascending=False,
    )
    flip = conditional.loc[conditional["edge_classification"].eq("DIRECTION_FLIP_RISK")].sort_values(
        "effective_mean_ic",
        ascending=True,
    )

    lines = [
        "# Batch 3 Conditional Signal Research",
        "",
        f"- Run ID: `{config.run_id}`",
        f"- Diagnostics version: `{CONDITIONAL_DIAGNOSTICS_VERSION}`",
        f"- Run timestamp: `{config.run_timestamp}`",
        "- Scope: research artifacts only. No gates, formulas, WFV logic, schemas, or 04A+ stages were changed.",
        "",
        "## Objective",
        "",
        "Batch 3 investigates whether recent Batch 1/2 failures are better understood as conditional edges rather than universal signals. The goal is to identify market states where the focus signals have stronger sign consistency, persistence, and effective IC without relaxing any platform gate.",
        "",
        "## Focus Signals",
        "",
        *[f"- `{signal}`" for signal in config.focus_signals],
        "",
        "## Conditional Contexts",
        "",
        "All contexts are OHLCV-only and derived from current clean close prices. Existing benchmark trend, volatility, drawdown, and correlation regimes are reused; additional research-only labels cover cross-sectional dispersion, breadth, participation, and a simple risk-on/risk-off proxy.",
        "",
        "Important caveat: these are in-sample conditional diagnostics. Strong conditional IC is a hypothesis for a controlled Batch 3 experiment, not evidence of deployability or a reason to relax WFV.",
        "",
        "## Classification Rules",
        "",
        f"- `INSUFFICIENT_SAMPLE`: fewer than {MIN_SAMPLE_DAYS} daily IC observations in the condition.",
        "- `DIRECTION_FLIP_RISK`: condition has negative effective mean IC or materially poor sign consistency.",
        "- `PROMISING_CONDITIONAL_EDGE`: positive effective IC, sign consistency, and window persistence all clear conservative research thresholds.",
        "- `WEAK_CONDITIONAL_EDGE`: positive but less convincing conditional behavior.",
        "- `AVOID`: enough sample but insufficient robustness.",
        "",
        "These labels are diagnostic only and are not platform gates.",
        "",
        "## Top Promising Conditional Edges",
        "",
        *_markdown_table(
            promising,
            [
                "signal_name",
                "horizon",
                "context_column",
                "context_value",
                "n_days",
                "effective_mean_ic",
                "sign_consistency",
                "window_persistence",
                "degradation_vs_unconditional_ic",
            ],
        ),
        "",
        "## Weak Conditional Edges",
        "",
        *_markdown_table(
            weak,
            [
                "signal_name",
                "horizon",
                "context_column",
                "context_value",
                "n_days",
                "effective_mean_ic",
                "sign_consistency",
                "window_persistence",
                "degradation_vs_unconditional_ic",
            ],
        ),
        "",
        "## Direction-Flip / Avoid Evidence",
        "",
        *_markdown_table(
            flip,
            [
                "signal_name",
                "horizon",
                "context_column",
                "context_value",
                "n_days",
                "effective_mean_ic",
                "sign_consistency",
                "window_persistence",
            ],
        ),
        "",
        "## Batch 3 Recommendation",
        "",
    ]

    if recommendations.empty:
        lines.extend(
            [
                "No Batch 3 implementation candidate is recommended from this diagnostic pass. The conditional analysis did not find enough robust, high-sample conditional edges to justify new formulas.",
                "",
            ]
        )
    else:
        lines.extend(
            _markdown_table(
                recommendations,
                [
                    "recommended_variant",
                    "source_signal",
                    "horizon",
                    "condition_column",
                    "condition_value",
                    "edge_classification",
                    "n_days",
                    "effective_mean_ic",
                    "sign_consistency",
                    "window_persistence",
                ],
                max_rows=3,
            )
        )
        lines.extend(
            [
                "",
                "Recommended variants should preserve the source signal formula and add only the listed OHLCV-only condition. They should be treated as a small controlled Batch 3 set, not as evidence to relax WFV or admission gates.",
                "",
            ]
        )

    lines.extend(
        [
            "## Research Conclusion",
            "",
            "The diagnostic pass moves the investigation from broad universal signals toward explicit market-state hypotheses. Conditions that improve effective IC but still show low persistence or sign instability should remain research observations, not implementation candidates.",
            "",
            "## Artifacts",
            "",
            f"- `conditional_ic_by_context.csv`: full signal/regime diagnostics under `{config.output_dir}`.",
            "- `signal_context_summary.csv`: per-signal classification counts and best context.",
            "- `context_features.csv`: OHLCV-only market-state labels used in the analysis.",
            "- `batch3_candidate_recommendations.csv`: max-three implementation proposal set.",
            "",
        ]
    )
    return "\n".join(lines)


def run_conditional_signal_diagnostics(
    db_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    summary_path: str | Path | None = None,
    focus_signals: tuple[str, ...] = DEFAULT_FOCUS_SIGNALS,
    write: bool = True,
) -> dict[str, object]:
    run_id = make_run_id("conditional_signal_diagnostics")
    run_timestamp = make_run_timestamp()
    config = ConditionalDiagnosticsConfig(
        focus_signals=tuple(focus_signals),
        output_dir=Path(output_dir) if output_dir is not None else DEFAULT_OUTPUT_DIR,
        summary_path=Path(summary_path) if summary_path is not None else DEFAULT_SUMMARY_PATH,
        db_path=Path(db_path) if db_path is not None else get_sqlite_db_path(),
        run_id=run_id,
        run_timestamp=run_timestamp,
    )

    close_prices = load_price_table("clean_close_prices_current", db_path=config.db_path)
    context_features = build_context_features(close_prices)
    daily_ic = _read_table("signal_regime_ic_daily_current", config.db_path)
    scoring_gate = _read_table("signal_scoring_gate_current", config.db_path)
    daily_ic_base = build_daily_ic_base(daily_ic, scoring_gate, config.focus_signals)
    conditional = build_conditional_ic_diagnostics(daily_ic_base, context_features)
    summary = build_signal_context_summary(conditional)
    recommendations = build_batch3_recommendations(conditional)

    tables = {
        "context_features": context_features,
        "conditional_ic_by_context": conditional,
        "signal_context_summary": summary,
        "batch3_candidate_recommendations": recommendations,
    }
    for table in tables.values():
        if not table.empty:
            table["diagnostics_run_id"] = run_id
            table["diagnostics_version"] = CONDITIONAL_DIAGNOSTICS_VERSION

    markdown = build_markdown_summary(tables, config)
    if write:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        config.summary_path.parent.mkdir(parents=True, exist_ok=True)
        for name, table in tables.items():
            table.to_csv(config.output_dir / f"{name}.csv", index=False)
        config.summary_path.write_text(markdown, encoding="utf-8")

    run_summary = pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "diagnostics_version", "value": CONDITIONAL_DIAGNOSTICS_VERSION},
            {"metric": "focus_signal_count", "value": len(config.focus_signals)},
            {"metric": "conditional_rows", "value": int(len(conditional))},
            {
                "metric": "promising_edges",
                "value": int(conditional["edge_classification"].eq("PROMISING_CONDITIONAL_EDGE").sum())
                if not conditional.empty
                else 0,
            },
            {
                "metric": "weak_edges",
                "value": int(conditional["edge_classification"].eq("WEAK_CONDITIONAL_EDGE").sum())
                if not conditional.empty
                else 0,
            },
            {"metric": "recommended_candidate_count", "value": int(len(recommendations))},
            {"metric": "output_dir", "value": str(config.output_dir)},
            {"metric": "summary_path", "value": str(config.summary_path)},
        ]
    )
    return {"summary": run_summary, "markdown": markdown, **tables}


__all__ = [
    "CONDITIONAL_DIAGNOSTICS_VERSION",
    "DEFAULT_FOCUS_SIGNALS",
    "DEFAULT_OUTPUT_DIR",
    "DEFAULT_SUMMARY_PATH",
    "run_conditional_signal_diagnostics",
]
