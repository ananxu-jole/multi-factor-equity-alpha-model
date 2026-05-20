from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    baseline_panels,
    build_stress_states,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
    _clean_panel,
    _rank_cs,
)
from run_track_b_robustness_discovery_v4 import _cs_neutralize
from run_track_b_v6_focused_discovery import (
    BREADTH_INVENTORY_PATH,
    LIQUIDITY_INVENTORY_PATH,
    active_coverage_summary,
    state_attribution,
    _market_state_panel,
    _rebalance_interval,
)
from run_dispersion_recovery_stability_after_stress_v1 import (
    VOLATILITY_INVENTORY_PATH,
    max_corr_table,
)


RUN_ID = "calm_regime_relative_stability_10_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/calm_regime_relative_stability_10_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v3_design_screening.md")
NEUTRAL_NOTE = Path("docs/research_notes/neutral_accumulation_without_breakout_v1.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v1.md")
GOVERNANCE_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md")

SIGNAL_NAME = "calm_regime_relative_stability_10"


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _calm_state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    relative_stability: pd.DataFrame,
) -> pd.DataFrame:
    close = panels["close"]
    ret1 = close.pct_change(1, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    stress = build_stress_states(close, benchmark)
    stress_recent = (
        stress[["volatility_spike", "panic_liquidity_stress", "drawdown_acceleration"]]
        .rolling(20, min_periods=1)
        .max()
        .max(axis=1)
        .astype(bool)
    )
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    bench_vol20 = bench_ret.rolling(20, min_periods=15).std()
    dispersion20 = ret20.std(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    rank_churn_market = ret20.rank(axis=1, pct=True).diff().abs().mean(axis=1)

    trend_hostile = ((benchmark < bench_ma60) & (bench_20 < 0)).fillna(False)
    weak_breadth = stress["weak_breadth"].fillna(False)
    calm_vol = (
        (bench_vol20 < _rolling_quantile(bench_vol20, 0.60))
        & (bench_vol20 > _rolling_quantile(bench_vol20, 0.08))
    ).fillna(False)
    normal_dispersion = (
        (dispersion20 < _rolling_quantile(dispersion20, 0.65))
        & (dispersion20 > _rolling_quantile(dispersion20, 0.10))
    ).fillna(False)
    orderly_ranks = (rank_churn_market < _rolling_quantile(rank_churn_market, 0.60)).fillna(False)
    balanced_breadth = (
        (breadth20 > _rolling_quantile(breadth20, 0.30))
        & (breadth20 < _rolling_quantile(breadth20, 0.85))
    ).fillna(False)
    non_hostile = (~stress_recent & ~trend_hostile & ~weak_breadth).fillna(False)
    calm_regime = (non_hostile & calm_vol & normal_dispersion & balanced_breadth).fillna(False)
    high_stability = relative_stability.mean(axis=1, skipna=True) > relative_stability.stack().median()

    states = pd.DataFrame(index=close.index)
    states["CALM_REGIME"] = calm_regime
    states["NON_HOSTILE_REGIME"] = non_hostile
    states["CALM_NORMAL_VOL"] = (non_hostile & calm_vol).fillna(False)
    states["NORMAL_DISPERSION"] = (non_hostile & normal_dispersion).fillna(False)
    states["ORDERLY_CROSS_SECTION"] = (non_hostile & orderly_ranks).fillna(False)
    states["BALANCED_BREADTH"] = (non_hostile & balanced_breadth).fillna(False)
    states["CALM_WITH_HIGH_RELATIVE_STABILITY"] = (calm_regime & high_stability).fillna(False)
    states["HOSTILE_OR_STRESS"] = (stress_recent | trend_hostile | weak_breadth).fillna(False)
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_calm_stability_signal(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    residual1 = ret1.sub(bench_ret1, axis=0)
    residual10 = close.pct_change(10, fill_method=None).sub(benchmark.pct_change(10, fill_method=None), axis=0)

    rank10 = residual10.rank(axis=1, pct=True)
    rank20 = ret20.rank(axis=1, pct=True)
    rank10_churn = rank10.diff().abs().rolling(10, min_periods=6).mean()
    rank20_churn = rank20.diff().abs().rolling(20, min_periods=12).mean()
    relative_rank_stability = (
        (1.0 - rank10_churn.rank(axis=1, pct=True))
        * (1.0 - rank20_churn.rank(axis=1, pct=True))
    ).clip(lower=0.0)

    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol30 = residual1.rolling(30, min_periods=20).std()
    residual_vol_stability = (1.0 - _safe_div(residual_vol10, residual_vol30).rank(axis=1, pct=True)).clip(lower=0.0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range_orderliness = (
        1.0
        - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True)
    ).clip(lower=0.0)
    path_orderliness = (1.0 - ret1.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
    neutral_extension = (
        (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
        * (1.0 - ret20.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
    ).clip(lower=0.0)

    relative_stability = (
        relative_rank_stability
        * residual_vol_stability
        * range_orderliness
        * path_orderliness
        * neutral_extension
    ).rolling(5, min_periods=3).mean()
    states = _calm_state_flags(panels, benchmark, relative_stability)
    calm_gate = _market_state_panel(states["CALM_REGIME"], close.columns)

    signal = _rank_cs(relative_stability * calm_gate)
    for exposure in [_rank_cs(ret5), _rank_cs(ret10), _rank_cs(ret20), _rank_cs(ret60), _rank_cs(-ret20)]:
        signal = _rank_cs(_cs_neutralize(signal, exposure))
    signal = _rank_cs(_rebalance_interval(signal * calm_gate, 10))
    signal = _clean_panel(signal)

    diagnostics = pd.DataFrame(
        {
            "component": [
                "relative_rank_stability",
                "residual_vol_stability",
                "range_orderliness",
                "path_orderliness",
                "neutral_extension",
                "calm_gate",
                "relative_stability",
                "final_signal",
            ],
            "finite_pct": [
                float(relative_rank_stability.notna().mean().mean()),
                float(residual_vol_stability.notna().mean().mean()),
                float(range_orderliness.notna().mean().mean()),
                float(path_orderliness.notna().mean().mean()),
                float(neutral_extension.notna().mean().mean()),
                float(calm_gate.notna().mean().mean()),
                float(relative_stability.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(relative_rank_stability.abs().mean().mean()),
                float(residual_vol_stability.abs().mean().mean()),
                float(range_orderliness.abs().mean().mean()),
                float(path_orderliness.abs().mean().mean()),
                float(neutral_extension.abs().mean().mean()),
                float(calm_gate.abs().mean().mean()),
                float(relative_stability.abs().mean().mean()),
                float(signal.abs().mean().mean()),
            ],
        }
    )
    return {SIGNAL_NAME: signal}, states, diagnostics


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    ret1 = close.pct_change(1, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual1 = ret1.sub(benchmark.pct_change(1, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    rank10 = residual10.rank(axis=1, pct=True)
    rank_stability = _rank_cs(1.0 - rank10.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True))
    low_volatility = _rank_cs(-ret1.rolling(20, min_periods=15).std())
    low_residual_vol = _rank_cs(-residual1.rolling(20, min_periods=15).std())
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range_stability = _rank_cs(1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True))
    calm_stability_raw = _rank_cs((rank_stability * low_residual_vol * range_stability).rolling(5, min_periods=3).mean())
    refs["price_rank_momentum_10"] = _rank_cs(ret10).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_20"] = _rank_cs(ret20).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_60"] = _rank_cs(ret60).reindex(index=first.index, columns=first.columns)
    refs["simple_rank_stability_10"] = rank_stability.reindex(index=first.index, columns=first.columns)
    refs["simple_low_volatility_20"] = low_volatility.reindex(index=first.index, columns=first.columns)
    refs["simple_low_residual_volatility_20"] = low_residual_vol.reindex(index=first.index, columns=first.columns)
    refs["simple_range_stability"] = range_stability.reindex(index=first.index, columns=first.columns)
    refs["raw_calm_stability_composite"] = calm_stability_raw.reindex(index=first.index, columns=first.columns)
    if LIQUIDITY_INVENTORY_PATH.exists():
        refs["inventory_participation_liquidity_state_shift_20_60"] = pd.read_parquet(
            LIQUIDITY_INVENTORY_PATH
        ).reindex(index=first.index, columns=first.columns)
    if BREADTH_INVENTORY_PATH.exists():
        refs["inventory_participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(
            BREADTH_INVENTORY_PATH
        ).reindex(index=first.index, columns=first.columns)
    if VOLATILITY_INVENTORY_PATH.exists():
        refs["inventory_volatility_compression_after_stress_stabilization"] = pd.read_parquet(
            VOLATILITY_INVENTORY_PATH
        ).reindex(index=first.index, columns=first.columns)
    return refs


def calm_corr_summary(orth: pd.DataFrame) -> pd.DataFrame:
    summary = max_corr_table(orth)
    rows = []
    for name, group in orth.groupby("signal_name"):
        row = {"signal_name": name}
        for comparison in [
            "price_rank_momentum_10",
            "price_rank_momentum_20",
            "price_rank_momentum_60",
            "simple_rank_stability_10",
            "simple_low_volatility_20",
            "simple_low_residual_volatility_20",
            "simple_range_stability",
            "raw_calm_stability_composite",
        ]:
            sample = group[group["comparison"].eq(comparison)]
            row[f"{comparison}_corr"] = float(sample["abs_value_corr"].max()) if not sample.empty else np.nan
        momentum_refs = group[group["comparison"].isin(["plain_momentum_60", "price_rank_momentum_10", "price_rank_momentum_20", "price_rank_momentum_60"])]
        low_vol_refs = group[group["comparison"].isin(["simple_low_volatility_20", "simple_low_residual_volatility_20"])]
        stability_refs = group[group["comparison"].isin(["simple_rank_stability_10", "simple_range_stability", "raw_calm_stability_composite"])]
        row["max_price_momentum_corr"] = float(momentum_refs["abs_value_corr"].max()) if not momentum_refs.empty else np.nan
        row["max_low_volatility_corr"] = float(low_vol_refs["abs_value_corr"].max()) if not low_vol_refs.empty else np.nan
        row["max_simple_stability_corr"] = float(stability_refs["abs_value_corr"].max()) if not stability_refs.empty else np.nan
        rows.append(row)
    return summary.merge(pd.DataFrame(rows), on="signal_name", how="left")


def sample_size_summary(states: pd.DataFrame, signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    panel = signals[SIGNAL_NAME]
    active_by_signal = (panel.notna().sum(axis=1) >= 25) & (panel.abs().mean(axis=1, skipna=True) > 0.02)
    rows = []
    for state_name, mask in states.items():
        state_mask = mask.astype(bool)
        rows.append(
            {
                "state": state_name,
                "state_dates": int(state_mask.sum()),
                "state_date_ratio": float(state_mask.mean()),
                "signal_active_overlap_dates": int((state_mask & active_by_signal).sum()),
                "signal_active_overlap_ratio": float((state_mask & active_by_signal).mean()),
            }
        )
    rows.append(
        {
            "state": "SIGNAL_ACTIVE",
            "state_dates": int(active_by_signal.sum()),
            "state_date_ratio": float(active_by_signal.mean()),
            "signal_active_overlap_dates": int(active_by_signal.sum()),
            "signal_active_overlap_ratio": float(active_by_signal.mean()),
        }
    )
    return pd.DataFrame(rows)


def classify_candidate(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    h5 = scores[scores["horizon"].eq(5)].rename(columns={"mean_ic": "h5_mean_ic", "positive_ic_rate": "h5_positive_ic_rate"})
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    calm_counts = (
        state_attr[
            state_attr["state"].isin(
                [
                    "CALM_REGIME",
                    "CALM_NORMAL_VOL",
                    "NORMAL_DISPERSION",
                    "ORDERLY_CROSS_SECTION",
                    "CALM_WITH_HIGH_RELATIVE_STABILITY",
                ]
            )
        ]
        .groupby("signal_name")["mean_ic"]
        .agg(positive_calm_state_count=lambda s: int((s > 0.004).sum()), best_calm_state_ic="max")
        .reset_index()
    )
    hostile_counts = (
        state_attr[state_attr["state"].isin(["HOSTILE_OR_STRESS", "weak_breadth", "drawdown_acceleration", "volatility_spike", "panic_liquidity_stress"])]
        .groupby("signal_name")["mean_ic"]
        .agg(best_hostile_state_ic="max")
        .reset_index()
    )
    stress_counts = (
        stress.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(calm_counts, on="signal_name", how="left")
        .merge(hostile_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.10:
            issues.append("high_turnover")
        if row.get("h10_mean_ic", np.nan) < 0.008:
            issues.append("weak_h10_ic")
        if row.get("h10_positive_ic_rate", np.nan) < 0.525:
            issues.append("weak_h10_positive_ic_rate")
        if int(row["horizon"]) != 10:
            issues.append("best_horizon_not_h10")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.45:
            issues.append("reversal_similarity_risk")
        if row.get("max_price_momentum_corr", 0) > 0.45:
            issues.append("momentum_similarity_risk")
        if row.get("max_low_volatility_corr", 0) > 0.45:
            issues.append("low_volatility_similarity_risk")
        if row.get("max_simple_stability_corr", 0) > 0.60:
            issues.append("simple_stability_similarity_risk")
        if row.get("active_date_ratio", 1) < 0.15:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.80:
            issues.append("activation_too_broad")
        if row.get("positive_calm_state_count", 0) < 2:
            issues.append("weak_calm_state_support")
        if row.get("best_hostile_state_ic", -1) > row.get("best_calm_state_ic", np.nan):
            issues.append("hostile_state_dependence_risk")

        if (
            row.get("h10_mean_ic", 0) > 0.016
            and row.get("h10_positive_ic_rate", 0) >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.08
            and row.get("active_date_ratio", 0) >= 0.15
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_price_momentum_corr", 1) <= 0.40
            and row.get("max_low_volatility_corr", 1) <= 0.40
            and row.get("positive_calm_state_count", 0) >= 3
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row.get("h10_mean_ic", 0) > 0.010
            and row.get("h10_positive_ic_rate", 0) >= 0.525
            and row.get("positive_calm_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_low_volatility_corr", 1) <= 0.45
            and row.get("active_date_ratio", 0) >= 0.12
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_calm_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.40
            and row.get("max_low_volatility_corr", 1) <= 0.50
            and row.get("active_date_ratio", 0) >= 0.10
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "calm_regime_relative_stability",
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h5_mean_ic": row.get("h5_mean_ic"),
                "h5_positive_ic_rate": row.get("h5_positive_ic_rate"),
                "h10_mean_ic": row.get("h10_mean_ic"),
                "h10_positive_ic_rate": row.get("h10_positive_ic_rate"),
                "h20_mean_ic": row.get("h20_mean_ic"),
                "h20_positive_ic_rate": row.get("h20_positive_ic_rate"),
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "max_low_volatility_corr": row.get("max_low_volatility_corr"),
                "max_simple_stability_corr": row.get("max_simple_stability_corr"),
                "simple_rank_stability_10_corr": row.get("simple_rank_stability_10_corr"),
                "simple_low_volatility_20_corr": row.get("simple_low_volatility_20_corr"),
                "simple_low_residual_volatility_20_corr": row.get("simple_low_residual_volatility_20_corr"),
                "raw_calm_stability_composite_corr": row.get("raw_calm_stability_composite_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "inventory_volatility_corr": row.get("inventory_volatility_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "positive_calm_state_count": int(row.get("positive_calm_state_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "best_calm_state_ic": row.get("best_calm_state_ic"),
                "best_hostile_state_ic": row.get("best_hostile_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def _decision_text(decisions: pd.DataFrame) -> str:
    status = str(decisions.iloc[0]["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return "`calm_regime_relative_stability_10` should move to formal conditional validation using this fixed single formulation."
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return "`calm_regime_relative_stability_10` should receive a narrow refinement diagnostics pass focused on h10 stability, calm-state support, and low-volatility separation."
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return "`calm_regime_relative_stability_10` should remain conditional-only research evidence until h10 behavior and calm-state support are stronger."
    return "`calm_regime_relative_stability_10` should be rejected in this formulation. Treat the result as evidence before testing another Expansion v3 concept."


def write_note(
    registry: pd.DataFrame,
    component_diagnostics: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    wfv_windows: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    sample_sizes: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    decision = decisions.iloc[0]
    h5 = scores[scores["horizon"].eq(5)].copy()
    h10 = scores[scores["horizon"].eq(10)].copy()
    h20 = scores[scores["horizon"].eq(20)].copy()
    top_states = state_attr.sort_values("mean_ic", ascending=False).head(12)
    top_stress = stress.sort_values("mean_ic", ascending=False).head(8)
    lines = [
        "# Calm Regime Relative Stability 10 v1",
        "",
        "## Executive Takeaway",
        "",
        "This research-only run tested one simple formulation of `calm_regime_relative_stability_10` under the isolated run namespace `calm_regime_relative_stability_10_v1`.",
        "",
        "The formulation was designed to test whether stocks with cleaner cross-sectional relative stability during calm, non-hostile regimes exhibit stronger h10 behavior without becoming low-volatility beta, momentum, reversal, breakout continuation, or hostile-state repair.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v3 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v3 design screen: `{SOURCE_NOTE}`",
        f"- Prior v3 isolated test: `{NEUTRAL_NOTE}`",
        f"- Conditional Alpha Inventory Monitoring v1: `{MONITORING_NOTE}`",
        f"- Conditional Alpha Inventory v2 Governance Update: `{GOVERNANCE_NOTE}`",
        "- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | In calm regimes, stable relative ordering and low cross-sectional rank churn may carry information because stock-specific quality can be expressed without stress-driven noise. |",
        "| Calm-regime logic | Activate only when the market is non-hostile, recent stress is absent, benchmark volatility is low-to-normal, dispersion is normal, and breadth is balanced rather than weak or euphoric. |",
        "| Relative stability definition | Combine low residual rank churn, stable residual volatility ratio, orderly range behavior, path orderliness, and neutral price extension. |",
        "| Non-hostile regime filter | Exclude recent volatility spike, panic/liquidity stress, drawdown acceleration, hostile trend, and weak breadth. |",
        "| Difference from low-volatility factors | Low volatility is only a baseline and one component-adjacent risk; the candidate requires relative rank stability and is checked directly against low-volatility references. |",
        "| Difference from momentum/reversal | Short, medium, and longer price-rank exposures are neutralized; the mechanism is stability, not direction of prior return. |",
        "| Difference from current inventory | It tests orderly calm-state behavior rather than hostile trend, weak breadth, drawdown, panic/liquidity stress, or post-stress stabilization. |",
        "| Expected activation semantics | Calm non-hostile regime with high relative stability. |",
        "| Expected horizon | h10 primary; h5 and h20 diagnostic. |",
        "| Expected turnover | Low after fixed 10-day rebalance control. |",
        "| Expected active coverage | Medium to medium-high. |",
        "",
        "## Candidate Registry",
        "",
        registry.to_markdown(index=False),
        "",
        "## Component Diagnostics",
        "",
        component_diagnostics.to_markdown(index=False),
        "",
        "## Structural Quality",
        "",
        structural.merge(active, on="signal_name", how="left")[
            ["signal_name", "missing_pct", "finite_pct", "date_coverage", "turnover_proxy", "turnover_p95", "active_date_ratio", "activation_transitions", "mean_active_coverage"]
        ].to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h5 / h10 / h20 Behavior",
        "",
        pd.concat([h5, h10, h20])[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics were unavailable.",
        "",
        "## WFV Window Detail",
        "",
        wfv_windows.to_markdown(index=False) if not wfv_windows.empty else "WFV window diagnostics were unavailable.",
        "",
        "## Baseline And Inventory Similarity",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Calm / Neutral Vs Hostile / Stress Attribution",
        "",
        top_states[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        top_stress[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Sample-Size Sanity",
        "",
        sample_sizes.to_markdown(index=False),
        "",
        "## Candidate Decision",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Specific Diagnostic Answers",
        "",
        f"- Genuinely calm-regime relative stability: assessed through calm-state attribution; positive calm-state count was `{decision['positive_calm_state_count']}` and best calm-state IC was `{decision['best_calm_state_ic']:.6f}`.",
        f"- Low-volatility beta risk: max low-volatility correlation was `{decision['max_low_volatility_corr']:.6f}`; low-vol and residual-low-vol correlations were `{decision['simple_low_volatility_20_corr']:.6f}` / `{decision['simple_low_residual_volatility_20_corr']:.6f}`.",
        f"- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `{decision['max_price_momentum_corr']:.6f}` / `{decision['max_reversal_corr']:.6f}`.",
        f"- Simple stability duplication risk: max simple-stability correlation was `{decision['max_simple_stability_corr']:.6f}`.",
        f"- Inventory overlap risk: inventory liquidity/breadth/volatility correlations were `{decision['inventory_liquidity_corr']:.6f}` / `{decision['inventory_breadth_corr']:.6f}` / `{decision['inventory_volatility_corr']:.6f}`.",
        f"- Sparse or broad activation risk: active date ratio was `{decision['active_date_ratio']:.6f}`.",
        f"- Turnover risk: turnover proxy was `{decision['turnover_proxy']:.6f}`.",
        f"- Directional stability: WFV-style persistence/sign consistency were `{decision['wfv_persistence']}` / `{decision['wfv_sign_consistency']}`.",
        f"- h10 profile: h10 mean IC was `{decision['h10_mean_ic']:.6f}` with positive IC rate `{decision['h10_positive_ic_rate']:.6f}`.",
        "",
        "## Recommended Next Step",
        "",
        _decision_text(decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, component_diagnostics = build_calm_stability_signal(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "calm_regime_relative_stability",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V3_RESEARCH_ONLY",
                "mechanism_thesis": "Calm-regime relative stability without low-volatility, momentum, reversal, or hostile-repair dependence.",
                "state_transition_logic": "Non-hostile calm regime plus low relative rank churn, residual-vol stability, range orderliness, and neutral price extension.",
                "differs_from_inventory": "Targets calm orderly states instead of hostile/stress h20 repair.",
                "differs_from_reversal_momentum": "Neutralizes return-rank exposures and tests stability rather than prior-return direction.",
                "expected_activation_state": "CALM_REGIME_WITH_HIGH_RELATIVE_STABILITY",
                "expected_horizon": "h10 primary; h5/h20 diagnostic",
                "expected_turnover_profile": "low",
                "expected_active_coverage": "medium_to_medium_high",
            }
        ]
    )

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = calm_corr_summary(orth)
    active = active_coverage_summary(signals)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidate(structural, scores, wfv_summary, stress, state_attr, orth_summary, active)

    artifact_files = [
        "candidate_registry.csv",
        "component_diagnostics.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "calm_state_flags.csv",
        "stress_regime_attribution.csv",
        "calm_state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "sample_size_sanity.csv",
        "candidate_classification.csv",
        f"{SIGNAL_NAME}_signal_panel.parquet",
        "manifest.json",
    ]
    registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    component_diagnostics.to_csv(OUT_DIR / "component_diagnostics.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    states.to_csv(OUT_DIR / "calm_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "calm_state_attribution.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    sample_sizes.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_classification.csv", index=False)
    signals[SIGNAL_NAME].to_parquet(OUT_DIR / f"{SIGNAL_NAME}_signal_panel.parquet")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "source_note": str(SOURCE_NOTE),
                "prior_neutral_accumulation_note": str(NEUTRAL_NOTE),
                "monitoring_note": str(MONITORING_NOTE),
                "governance_note": str(GOVERNANCE_NOTE),
                "candidate_count": 1,
                "candidate_names": [SIGNAL_NAME],
                "one_simple_formulation": True,
                "parameter_grid": False,
                "broad_discovery": False,
                "other_expansion_v3_concepts_implemented": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "artifact_files": sorted(artifact_files),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_note(
        registry,
        component_diagnostics,
        structural,
        scores,
        wfv_summary,
        wfv_windows,
        stress,
        state_attr,
        orth_summary,
        active,
        sample_sizes,
        decisions,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    main()
