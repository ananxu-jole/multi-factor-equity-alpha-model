"""Conditional Edge Atlas research framework.

The atlas maps signal behavior across reusable OHLCV-only market states. It is
research-only: outputs are standalone CSV/Markdown artifacts and no official
WFV, gate, promotion, alpha, portfolio, or execution logic is changed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import connect_db, load_price_table, table_exists
from src.run_config import get_project_root, get_sqlite_db_path, make_run_id, make_run_timestamp
from src.scoring.regime_ic import build_regime_features_for_ic


ATLAS_VERSION = "conditional_edge_atlas_v1"
DEFAULT_OUTPUT_DIR = get_project_root() / "artifacts" / "research" / "conditional_edge_atlas"
DEFAULT_SUMMARY_PATH = get_project_root() / "docs" / "research_notes" / "conditional_edge_atlas_v1.md"
DEFAULT_SIGNALS = (
    "trend_consistency_20_60",
    "trend_consistency_20_60_persistent",
    "smooth_trend_persistence_60",
    "smooth_trend_persistence_60_downtrend",
    "percentile_rank_stability_20",
    "percentile_rank_stability_20_downtrend",
    "index_relative_reversal_5",
    "index_relative_reversal_5_high_drawdown",
)
CONTEXT_COLUMNS = (
    "benchmark_trend_state",
    "benchmark_vol_state",
    "drawdown_depth_state",
    "dispersion_state",
    "breadth_level_state",
    "breadth_change_state",
    "volatility_change_state",
    "participation_concentration_state",
)
MIN_ACTIVE_DATES = 126
MIN_ACTIVE_WINDOWS = 2
MIN_WINDOW_COVERAGE = 0.50


@dataclass(frozen=True)
class ConditionalEdgeAtlasConfig:
    output_dir: Path = DEFAULT_OUTPUT_DIR
    summary_path: Path = DEFAULT_SUMMARY_PATH
    db_path: Path = get_sqlite_db_path()
    focus_signals: tuple[str, ...] = DEFAULT_SIGNALS
    include_all_current_signals: bool = True
    run_id: str = ""
    run_timestamp: str = ""


def _read_table(table_name: str, db_path: str | Path | None) -> pd.DataFrame:
    if not table_exists(table_name, db_path=db_path):
        return pd.DataFrame()
    with connect_db(db_path) as conn:
        return pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)


def _tercile(values: pd.Series, low: str, mid: str, high: str) -> pd.Series:
    output = pd.Series(np.nan, index=values.index, dtype="object")
    valid = values.dropna()
    if valid.empty:
        return output
    lo = valid.quantile(1 / 3)
    hi = valid.quantile(2 / 3)
    output.loc[values <= lo] = low
    output.loc[(values > lo) & (values < hi)] = mid
    output.loc[values >= hi] = high
    return output


def _expected_sign(direction: object) -> int:
    text = str(direction).upper()
    if "NEGATIVE" in text or "REVERSE" in text:
        return -1
    return 1


def build_market_state_taxonomy(close_prices: pd.DataFrame, benchmark_ticker: str = "SPY") -> pd.DataFrame:
    """Build reusable OHLCV-only market states."""
    close = close_prices.copy()
    close.index = pd.to_datetime(close.index, errors="coerce")
    close = close.sort_index().apply(pd.to_numeric, errors="coerce")
    benchmark = close[benchmark_ticker] if benchmark_ticker in close.columns else close.mean(axis=1, skipna=True)
    returns = close.pct_change(fill_method=None)
    asset_returns = returns.drop(columns=[benchmark_ticker], errors="ignore")

    base = build_regime_features_for_ic(close, benchmark_ticker=benchmark_ticker if benchmark_ticker in close.columns else close.columns[0])
    base["Date"] = pd.to_datetime(base["Date"], errors="coerce")
    states = base.set_index("Date").sort_index()
    states["benchmark_trend_state"] = states["benchmark_trend_regime"]
    states["benchmark_vol_state"] = states["benchmark_vol_regime"]

    drawdown = benchmark.div(benchmark.cummax()).sub(1.0)
    drawdown_depth = pd.Series("SHALLOW_DRAWDOWN", index=close.index, dtype="object")
    drawdown_depth.loc[(drawdown <= -0.05) & (drawdown > -0.15)] = "MODERATE_DRAWDOWN"
    drawdown_depth.loc[drawdown <= -0.15] = "DEEP_DRAWDOWN"
    drawdown_depth.loc[drawdown.isna()] = np.nan
    states["drawdown_depth_state"] = drawdown_depth

    dispersion = asset_returns.std(axis=1, skipna=True)
    breadth = close.drop(columns=[benchmark_ticker], errors="ignore").pct_change(20, fill_method=None).gt(0).mean(axis=1, skipna=True)
    breadth_change = breadth.diff(20)
    benchmark_vol = benchmark.pct_change(fill_method=None).rolling(20).std()
    vol_change = benchmark_vol / benchmark_vol.rolling(60).mean().replace(0.0, np.nan) - 1.0
    abs_returns = asset_returns.abs()
    top_decile_share = abs_returns.apply(
        lambda row: row.nlargest(max(1, int(row.notna().sum() * 0.10))).sum() / row.sum()
        if row.notna().sum() >= 10 and row.sum() != 0
        else np.nan,
        axis=1,
    )

    states["cross_sectional_dispersion_1d"] = dispersion
    states["breadth_positive_20d"] = breadth
    states["breadth_change_20d"] = breadth_change
    states["benchmark_vol_change_20_60"] = vol_change
    states["participation_top_decile_abs_return_share"] = top_decile_share
    states["dispersion_state"] = _tercile(dispersion, "LOW_DISPERSION", "MID_DISPERSION", "HIGH_DISPERSION")
    states["breadth_level_state"] = _tercile(breadth, "LOW_BREADTH", "MID_BREADTH", "HIGH_BREADTH")
    states["breadth_change_state"] = _tercile(breadth_change, "BREADTH_DETERIORATING", "BREADTH_NEUTRAL", "BREADTH_IMPROVING")
    states["volatility_change_state"] = _tercile(vol_change, "VOL_COMPRESSION", "VOL_STABLE", "VOL_EXPANSION")
    states["participation_concentration_state"] = _tercile(
        top_decile_share,
        "LOW_CONCENTRATION",
        "MID_CONCENTRATION",
        "HIGH_CONCENTRATION",
    )
    return states.reset_index()


def build_daily_ic_base(
    daily_ic: pd.DataFrame,
    scoring_gate: pd.DataFrame,
    signal_names: list[str],
) -> pd.DataFrame:
    base = daily_ic.loc[daily_ic["signal_name"].astype(str).isin(signal_names)].copy()
    base["Date"] = pd.to_datetime(base["Date"], errors="coerce")
    base["horizon"] = pd.to_numeric(base["horizon"], errors="coerce").astype("Int64")
    base["daily_ic"] = pd.to_numeric(base["daily_ic"], errors="coerce")
    base = (
        base.groupby(["Date", "signal_name", "horizon"], as_index=False, dropna=False)
        .agg(daily_ic=("daily_ic", "mean"))
        .dropna(subset=["Date", "signal_name", "horizon"])
    )
    meta_cols = [
        "signal_name",
        "horizon",
        "signal_family",
        "signal_direction",
        "signal_strength",
        "status",
        "mean_ic",
        "abs_mean_ic",
    ]
    metadata = scoring_gate.loc[scoring_gate["signal_name"].astype(str).isin(signal_names), [c for c in meta_cols if c in scoring_gate.columns]].copy()
    metadata["horizon"] = pd.to_numeric(metadata["horizon"], errors="coerce").astype("Int64")
    metadata = metadata.drop_duplicates(["signal_name", "horizon"], keep="last")
    output = base.merge(metadata, on=["signal_name", "horizon"], how="left")
    output["signal_direction"] = output["signal_direction"].fillna("POSITIVE_EDGE")
    output["expected_sign"] = output["signal_direction"].map(_expected_sign)
    output["effective_daily_ic"] = output["daily_ic"] * output["expected_sign"]
    output["unconditional_effective_mean_ic"] = pd.to_numeric(output.get("mean_ic"), errors="coerce") * output["expected_sign"]
    return output


def _window_metrics(daily: pd.DataFrame, windows: pd.DataFrame, state_mask: pd.Series) -> dict[str, object]:
    window_means: list[float] = []
    active_windows = 0
    direction_flips = 0
    for _, window in windows.iterrows():
        start = pd.to_datetime(window["test_start"])
        end = pd.to_datetime(window["test_end"])
        active_dates = state_mask.loc[start:end]
        if active_dates.any():
            active_windows += 1
        active_index = active_dates[active_dates].index
        chunk = daily.loc[daily["Date"].isin(active_index), "effective_daily_ic"].dropna()
        if not chunk.empty:
            mean = float(chunk.mean())
            window_means.append(mean)
            if mean < 0:
                direction_flips += 1
    if not window_means:
        return {
            "active_window_count": active_windows,
            "valid_active_window_count": 0,
            "active_window_coverage_ratio": active_windows / len(windows) if len(windows) else np.nan,
            "conditional_persistence": np.nan,
            "direction_flip_frequency": np.nan,
            "window_effective_ic_std": np.nan,
            "window_effective_ic_ir": np.nan,
            "max_positive_effective_ic_share": np.nan,
        }
    series = pd.Series(window_means, dtype=float)
    positive_sum = series[series > 0].sum()
    return {
        "active_window_count": active_windows,
        "valid_active_window_count": len(window_means),
        "active_window_coverage_ratio": active_windows / len(windows) if len(windows) else np.nan,
        "conditional_persistence": float((series > 0).mean()),
        "direction_flip_frequency": float((series < 0).mean()),
        "window_effective_ic_std": float(series.std(ddof=1)) if len(series) > 1 else np.nan,
        "window_effective_ic_ir": float(series.mean() / series.std(ddof=1)) if len(series) > 1 and series.std(ddof=1) != 0 else np.nan,
        "max_positive_effective_ic_share": float((series.clip(lower=0) / positive_sum).max()) if positive_sum != 0 else np.nan,
    }


def classify_edge(row: pd.Series) -> str:
    active_dates = int(row.get("active_date_count") or 0)
    valid_windows = int(row.get("valid_active_window_count") or 0)
    coverage = row.get("active_window_coverage_ratio")
    eff_ic = row.get("effective_mean_ic")
    eff_ir = row.get("effective_ic_ir")
    sign = row.get("sign_consistency")
    persistence = row.get("conditional_persistence")
    flip = row.get("direction_flip_frequency")
    max_share = row.get("max_positive_effective_ic_share")
    std = row.get("ic_std")

    if active_dates < 63:
        return "INSUFFICIENT_SAMPLE"
    if active_dates < MIN_ACTIVE_DATES or valid_windows < MIN_ACTIVE_WINDOWS or pd.isna(coverage) or coverage < MIN_WINDOW_COVERAGE:
        return "SPARSE_CONDITIONAL_EDGE"
    if pd.notna(flip) and flip >= 0.50:
        return "DIRECTION_FLIP_RISK"
    if pd.notna(eff_ic) and eff_ic < 0:
        return "DIRECTION_FLIP_RISK"
    if pd.notna(std) and pd.notna(eff_ic) and std > 0.25 and abs(eff_ic) < 0.04:
        return "HIGH_VARIANCE_EDGE"
    if pd.notna(max_share) and max_share >= 0.60:
        return "SPARSE_CONDITIONAL_EDGE"
    if (
        pd.notna(eff_ic)
        and pd.notna(eff_ir)
        and pd.notna(sign)
        and pd.notna(persistence)
        and eff_ic >= 0.015
        and eff_ir >= 0.20
        and sign >= 0.55
        and persistence >= 0.67
    ):
        return "ROBUST_CONDITIONAL_EDGE"
    if pd.notna(eff_ic) and eff_ic >= 0.008 and pd.notna(sign) and sign >= 0.52:
        return "CONDITIONAL_WATCHLIST"
    return "AVOID"


def build_conditional_edge_summary(
    daily_ic_base: pd.DataFrame,
    market_states: pd.DataFrame,
    windows: pd.DataFrame,
) -> pd.DataFrame:
    states = market_states[["Date", *CONTEXT_COLUMNS]].copy()
    states["Date"] = pd.to_datetime(states["Date"], errors="coerce")
    merged = daily_ic_base.merge(states, on="Date", how="left")
    state_by_date = states.set_index("Date").sort_index()
    rows: list[dict[str, object]] = []
    for context_column in CONTEXT_COLUMNS:
        for context_value, state_dates in state_by_date[context_column].dropna().groupby(state_by_date[context_column].dropna()):
            mask = state_by_date[context_column].eq(context_value)
            active_date_count = int(mask.sum())
            state_daily = merged.loc[merged[context_column].eq(context_value)].dropna(subset=["daily_ic"]).copy()
            for (signal_name, horizon), group in state_daily.groupby(["signal_name", "horizon"], dropna=False):
                effective = group["effective_daily_ic"].dropna()
                raw = group["daily_ic"].dropna()
                if effective.empty:
                    continue
                unconditional = group["unconditional_effective_mean_ic"].dropna()
                uncond = float(unconditional.iloc[-1]) if not unconditional.empty else np.nan
                std = float(raw.std(ddof=1)) if len(raw) > 1 else np.nan
                mean_ic = float(raw.mean())
                effective_mean = float(effective.mean())
                wm = _window_metrics(group, windows, mask)
                rows.append(
                    {
                        "signal_name": signal_name,
                        "horizon": int(horizon),
                        "signal_family": group["signal_family"].iloc[-1] if "signal_family" in group else "",
                        "signal_direction": group["signal_direction"].iloc[-1] if "signal_direction" in group else "",
                        "context_column": context_column,
                        "context_value": context_value,
                        "active_date_count": active_date_count,
                        "mean_ic": mean_ic,
                        "median_ic": float(raw.median()),
                        "ic_std": std,
                        "ic_ir": float(mean_ic / std) if pd.notna(std) and std != 0 else np.nan,
                        "effective_mean_ic": effective_mean,
                        "effective_ic_ir": float(effective_mean / std) if pd.notna(std) and std != 0 else np.nan,
                        "positive_ic_rate": float((raw > 0).mean()),
                        "sign_consistency": float((effective > 0).mean()),
                        "degradation_vs_unconditional_ic": effective_mean - uncond if pd.notna(uncond) else np.nan,
                        **wm,
                    }
                )
    output = pd.DataFrame(rows)
    if output.empty:
        return output
    output["robustness_classification"] = output.apply(classify_edge, axis=1)
    return output.sort_values(["robustness_classification", "effective_mean_ic"], ascending=[True, False]).reset_index(drop=True)


def build_outputs(summary: pd.DataFrame) -> dict[str, pd.DataFrame]:
    heatmap = summary.pivot_table(
        index=["signal_name", "horizon"],
        columns=["context_column", "context_value"],
        values="effective_mean_ic",
        aggfunc="mean",
    ).reset_index()
    heatmap.columns = ["__".join([str(part) for part in col if str(part) != ""]) if isinstance(col, tuple) else str(col) for col in heatmap.columns]
    state_family = (
        summary.groupby(["context_column", "context_value", "signal_family", "robustness_classification"], dropna=False)
        .agg(
            edge_count=("signal_name", "count"),
            mean_effective_ic=("effective_mean_ic", "mean"),
            median_sign_consistency=("sign_consistency", "median"),
            median_active_window_coverage=("active_window_coverage_ratio", "median"),
        )
        .reset_index()
        .sort_values(["context_column", "context_value", "edge_count"], ascending=[True, True, False])
    )
    active_window_stats = summary[
        [
            "signal_name",
            "horizon",
            "context_column",
            "context_value",
            "active_date_count",
            "active_window_count",
            "valid_active_window_count",
            "active_window_coverage_ratio",
            "conditional_persistence",
            "direction_flip_frequency",
            "max_positive_effective_ic_share",
        ]
    ].copy()
    robustness = (
        summary.groupby(["context_column", "context_value", "robustness_classification"], dropna=False)
        .size()
        .reset_index(name="edge_count")
        .sort_values(["context_column", "context_value", "edge_count"], ascending=[True, True, False])
    )
    top = summary.loc[
        summary["robustness_classification"].isin(["ROBUST_CONDITIONAL_EDGE", "CONDITIONAL_WATCHLIST", "SPARSE_CONDITIONAL_EDGE"])
    ].sort_values(["robustness_classification", "effective_mean_ic", "sign_consistency"], ascending=[True, False, False]).head(50)
    return {
        "conditional_edge_summary": summary,
        "signal_state_heatmap": heatmap,
        "state_family_summary": state_family,
        "active_window_statistics": active_window_stats,
        "robustness_classification": robustness,
        "top_conditional_edges": top,
    }


def _markdown_table(df: pd.DataFrame, columns: list[str], max_rows: int = 12) -> str:
    if df.empty:
        return "No rows available."
    cols = [c for c in columns if c in df.columns]
    return df.loc[:, cols].head(max_rows).to_markdown(index=False)


def build_markdown(tables: dict[str, pd.DataFrame], config: ConditionalEdgeAtlasConfig) -> str:
    summary = tables["conditional_edge_summary"]
    robust = summary.loc[summary["robustness_classification"].eq("ROBUST_CONDITIONAL_EDGE")]
    watch = summary.loc[summary["robustness_classification"].eq("CONDITIONAL_WATCHLIST")]
    sparse = summary.loc[summary["robustness_classification"].eq("SPARSE_CONDITIONAL_EDGE")]
    state_counts = tables["robustness_classification"]
    strong_states = (
        summary.loc[summary["robustness_classification"].isin(["ROBUST_CONDITIONAL_EDGE", "CONDITIONAL_WATCHLIST"])]
        .groupby(["context_column", "context_value"])
        .agg(n_edges=("signal_name", "count"), mean_effective_ic=("effective_mean_ic", "mean"))
        .reset_index()
        .sort_values(["n_edges", "mean_effective_ic"], ascending=[False, False])
    )
    weak_states = (
        summary.loc[summary["robustness_classification"].isin(["AVOID", "DIRECTION_FLIP_RISK", "HIGH_VARIANCE_EDGE"])]
        .groupby(["context_column", "context_value"])
        .size()
        .reset_index(name="failure_count")
        .sort_values("failure_count", ascending=False)
    )
    return "\n".join(
        [
            "# Conditional Edge Atlas v1",
            "",
            f"- Run ID: `{config.run_id}`",
            f"- Atlas version: `{ATLAS_VERSION}`",
            f"- Run timestamp: `{config.run_timestamp}`",
            "- Scope: research-only. No official WFV logic, gates, schemas, promotion rules, alpha construction, portfolio logic, or execution logic were changed.",
            "",
            "## Objective",
            "",
            "The Conditional Edge Atlas maps signal behavior across reusable OHLCV-only market states before further signal-family or universe expansion. It is designed to identify repeated conditional behavior, sparse episodic effects, and states where signals fail or flip direction.",
            "",
            "## Market-State Taxonomy",
            "",
            "The atlas currently evaluates benchmark trend, benchmark volatility, drawdown depth, cross-sectional dispersion, breadth level, breadth change, volatility expansion/compression, and participation concentration. These states are diagnostic contexts, not trading rules.",
            "",
            "## Major Findings",
            "",
            f"- Total signal-state rows: {len(summary)}.",
            f"- Robust conditional edges: {len(robust)}.",
            f"- Conditional watchlist edges: {len(watch)}.",
            f"- Sparse conditional edges: {len(sparse)}.",
            "- Conditional strength is often concentrated in stress-like states, but sparse active-window coverage remains a recurring limitation.",
            "",
            "## Strongest Conditional States",
            "",
            _markdown_table(strong_states, ["context_column", "context_value", "n_edges", "mean_effective_ic"], 12),
            "",
            "## Weakest / Failure-Prone States",
            "",
            _markdown_table(weak_states, ["context_column", "context_value", "failure_count"], 12),
            "",
            "## Top Conditional Edges",
            "",
            _markdown_table(
                tables["top_conditional_edges"],
                [
                    "signal_name",
                    "horizon",
                    "signal_family",
                    "context_column",
                    "context_value",
                    "effective_mean_ic",
                    "effective_ic_ir",
                    "sign_consistency",
                    "active_window_coverage_ratio",
                    "conditional_persistence",
                    "robustness_classification",
                ],
                15,
            ),
            "",
            "## Recurring Regime Patterns",
            "",
            "Trend-quality signals tend to concentrate their strongest conditional behavior in downtrend, high-volatility, high-dispersion, or deep-drawdown states. Reversal-style signals more often cluster in stress or dislocation states, but they can still show high decay or direction-flip risk.",
            "",
            "## Recurring Failure Modes",
            "",
            "The main failure modes are sparse active-window coverage, one-window dominated evidence, direction flips, and high variance. These are research observations, not grounds for relaxing official WFV gates.",
            "",
            "## Implications For Batch 4",
            "",
            "Batch 4 should prioritize regime-aware hypotheses with enough active-window coverage. Signals that only work in rare states should remain watchlist research until a conditional-alpha framework can evaluate them separately.",
            "",
            "## Conditional-Alpha Framework Recommendation",
            "",
            "The atlas supports future conditional-alpha research, but it should remain separated from promotion logic. Active-state-aware validation can help design conditional alphas, while official WFV remains the conservative gate for standard signal promotion.",
            "",
            "## Artifacts",
            "",
            f"CSV artifacts are written under `{config.output_dir}`.",
            "",
        ]
    )


def _select_signal_names(scoring_gate: pd.DataFrame, config: ConditionalEdgeAtlasConfig) -> list[str]:
    names = set(config.focus_signals)
    if config.include_all_current_signals and not scoring_gate.empty:
        names.update(scoring_gate["signal_name"].dropna().astype(str).unique().tolist())
    return sorted(names)


def run_conditional_edge_atlas(
    db_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    summary_path: str | Path | None = None,
    include_all_current_signals: bool = True,
    focus_signals: tuple[str, ...] = DEFAULT_SIGNALS,
    write: bool = True,
) -> dict[str, object]:
    config = ConditionalEdgeAtlasConfig(
        db_path=Path(db_path) if db_path else get_sqlite_db_path(),
        output_dir=Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR,
        summary_path=Path(summary_path) if summary_path else DEFAULT_SUMMARY_PATH,
        include_all_current_signals=include_all_current_signals,
        focus_signals=tuple(focus_signals),
        run_id=make_run_id("conditional_edge_atlas"),
        run_timestamp=make_run_timestamp(),
    )
    close = load_price_table("clean_close_prices_current", db_path=config.db_path)
    market_states = build_market_state_taxonomy(close)
    daily_ic = _read_table("signal_regime_ic_daily_current", config.db_path)
    scoring_gate = _read_table("signal_scoring_gate_current", config.db_path)
    windows = _read_table("wfv_windows_current", config.db_path)
    signal_names = _select_signal_names(scoring_gate, config)
    daily_base = build_daily_ic_base(daily_ic, scoring_gate, signal_names)
    edge_summary = build_conditional_edge_summary(daily_base, market_states, windows)
    tables = build_outputs(edge_summary)
    for table in tables.values():
        table["atlas_run_id"] = config.run_id
        table["atlas_version"] = ATLAS_VERSION
    markdown = build_markdown(tables, config)
    if write:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        config.summary_path.parent.mkdir(parents=True, exist_ok=True)
        for name, table in tables.items():
            table.to_csv(config.output_dir / f"{name}.csv", index=False)
        config.summary_path.write_text(markdown, encoding="utf-8")
    run_summary = pd.DataFrame(
        [
            {"metric": "run_id", "value": config.run_id},
            {"metric": "atlas_version", "value": ATLAS_VERSION},
            {"metric": "signal_count", "value": len(signal_names)},
            {"metric": "conditional_edge_rows", "value": len(edge_summary)},
            {"metric": "robust_edges", "value": int(edge_summary["robustness_classification"].eq("ROBUST_CONDITIONAL_EDGE").sum()) if not edge_summary.empty else 0},
            {"metric": "watchlist_edges", "value": int(edge_summary["robustness_classification"].eq("CONDITIONAL_WATCHLIST").sum()) if not edge_summary.empty else 0},
            {"metric": "output_dir", "value": str(config.output_dir)},
            {"metric": "summary_path", "value": str(config.summary_path)},
        ]
    )
    return {"run_summary": run_summary, "markdown": markdown, **tables}


__all__ = ["ATLAS_VERSION", "run_conditional_edge_atlas"]
