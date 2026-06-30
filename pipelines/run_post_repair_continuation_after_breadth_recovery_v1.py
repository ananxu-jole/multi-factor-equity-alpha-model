from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    baseline_panels,
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
    orthogonality,
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


RUN_ID = "post_repair_continuation_after_breadth_recovery_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/post_repair_continuation_after_breadth_recovery_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v4_design_screening.md")
V3_REVIEW_NOTE = Path("docs/research_notes/track_b_expansion_v3_midcycle_review.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v1.md")
GOVERNANCE_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md")
ECOSYSTEM_NOTE = Path("docs/research_notes/inventory_ecosystem_review_v1.md")

SIGNAL_NAME = "post_repair_continuation_after_breadth_recovery"
HORIZONS = (1, 5, 10, 15, 20)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def score_signals_h15(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_rows = []
    daily_rows = []
    for horizon in HORIZONS:
        fwd = forward_returns(close, horizon)
        for name, panel in signals.items():
            ic = daily_ic(panel, fwd)
            valid_ic = ic.dropna()
            mean_ic = float(valid_ic.mean()) if not valid_ic.empty else np.nan
            std_ic = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            score_rows.append(
                {
                    "signal_name": name,
                    "horizon": horizon,
                    "mean_ic": mean_ic,
                    "abs_mean_ic": abs(mean_ic) if pd.notna(mean_ic) else np.nan,
                    "ic_ir": mean_ic / std_ic if std_ic and std_ic > 0 else np.nan,
                    "abs_ic_ir": abs(mean_ic / std_ic) if std_ic and std_ic > 0 else np.nan,
                    "positive_ic_rate": float((valid_ic > 0).mean()) if not valid_ic.empty else np.nan,
                    "n_dates": int(valid_ic.shape[0]),
                }
            )
            daily_rows.extend(
                {"Date": date, "signal_name": name, "horizon": horizon, "ic": value}
                for date, value in valid_ic.items()
            )
    scores = pd.DataFrame(score_rows)
    if not scores.empty:
        best = scores.loc[scores.groupby("signal_name")["abs_mean_ic"].idxmax(), ["signal_name", "horizon"]]
        best = best.rename(columns={"horizon": "best_horizon"})
        scores = scores.merge(best, on="signal_name", how="left")
        scores["is_best_horizon"] = scores["horizon"].eq(scores["best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def _state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    continuation_quality: pd.DataFrame,
) -> pd.DataFrame:
    close = panels["close"]
    ret20 = close.pct_change(20, fill_method=None)
    stress = build_stress_states(close, benchmark)
    stress_recent = (
        stress[["volatility_spike", "panic_liquidity_stress", "drawdown_acceleration"]]
        .rolling(20, min_periods=1)
        .max()
        .max(axis=1)
        .astype(bool)
    )
    bench_20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    breadth20 = (ret20 > 0).mean(axis=1)
    breadth_q35 = _rolling_quantile(breadth20, 0.35)
    breadth_q55 = _rolling_quantile(breadth20, 0.55)

    trend_hostile = ((benchmark < bench_ma60) & (bench_20 < 0)).fillna(False)
    weak_breadth = stress["weak_breadth"].fillna(False)
    active_repair = (weak_breadth | trend_hostile | stress["drawdown_acceleration"].fillna(False)).fillna(False)
    repair_recent_60 = active_repair.rolling(60, min_periods=1).max().astype(bool)
    weak_recent_60 = weak_breadth.rolling(60, min_periods=1).max().astype(bool)
    breadth_recovered = ((breadth20 > breadth_q35) & (breadth20.diff(20) > -0.02)).fillna(False)
    breadth_confirmed = (breadth20 > breadth_q55).fillna(False)
    hostile_cleared = (~weak_breadth & ~trend_hostile & ~stress_recent).fillna(False)
    non_euphoric = (breadth20 < _rolling_quantile(breadth20, 0.90)).fillna(False)
    quality_dates = continuation_quality.mean(axis=1, skipna=True) > continuation_quality.stack().median()

    states = pd.DataFrame(index=close.index)
    states["ACTIVE_HOSTILE_BREADTH_REPAIR"] = active_repair
    states["POST_REPAIR_BREADTH_RECOVERY"] = (
        weak_recent_60 & breadth_recovered & hostile_cleared & non_euphoric
    ).fillna(False)
    states["POST_REPAIR_QUALITY_CONFIRMATION"] = (
        states["POST_REPAIR_BREADTH_RECOVERY"] & quality_dates
    ).fillna(False)
    states["BREADTH_CONFIRMED_RECOVERY"] = (
        repair_recent_60 & breadth_confirmed & hostile_cleared & non_euphoric
    ).fillna(False)
    states["RESOLVED_STRESS_OR_REPAIR"] = (
        repair_recent_60 & hostile_cleared
    ).fillna(False)
    states["HOSTILE_OR_STRESS"] = (stress_recent | trend_hostile | weak_breadth).fillna(False)
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_post_repair_signal(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    high = panels["high"]
    low = panels["low"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    dollar_volume = close * volume

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)
    residual1 = ret1.sub(benchmark.pct_change(1, fill_method=None), axis=0)

    ret10_pct = ret10.rank(axis=1, pct=True)
    ret20_pct = ret20.rank(axis=1, pct=True)
    no_extension = ((ret10_pct < 0.82) & (ret20_pct < 0.82) & (ret20_pct > 0.20)).astype(float)
    moderate_positive_participation = (
        residual20.rank(axis=1, pct=True)
        * (1.0 - ret20_pct.sub(0.62).abs() * 2.0).clip(lower=0.0)
    ).clip(lower=0.0)

    rank20 = residual20.rank(axis=1, pct=True)
    rank10 = residual10.rank(axis=1, pct=True)
    rank_churn = (
        rank20.diff().abs().rolling(20, min_periods=12).mean()
        + rank10.diff().abs().rolling(10, min_periods=6).mean()
    ) / 2.0
    relative_stability = (1.0 - rank_churn.rank(axis=1, pct=True)).clip(lower=0.0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    range_orderliness = (
        (1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True))
        * (1.0 - _safe_div(true_range.rolling(20, min_periods=12).mean(), true_range.rolling(60, min_periods=40).mean()).rank(axis=1, pct=True))
    ).clip(lower=0.0)
    close_support = close_location.rolling(10, min_periods=6).mean().rank(axis=1, pct=True)
    residual_vol_order = (
        1.0
        - _safe_div(residual1.rolling(10, min_periods=7).std(), residual1.rolling(30, min_periods=20).std()).rank(axis=1, pct=True)
    ).clip(lower=0.0)
    participation_normalization = (
        1.0
        - _safe_div(dollar_volume.rolling(10, min_periods=7).mean(), dollar_volume.rolling(20, min_periods=12).mean()).sub(1.0).abs().rank(axis=1, pct=True)
    ).clip(lower=0.0)

    continuation_quality = (
        moderate_positive_participation
        * relative_stability
        * range_orderliness
        * close_support
        * residual_vol_order
        * participation_normalization
    ).rolling(5, min_periods=3).mean()
    states = _state_flags(panels, benchmark, continuation_quality)
    gate = _market_state_panel(states["POST_REPAIR_BREADTH_RECOVERY"], close.columns)

    signal = _rank_cs(continuation_quality * no_extension * gate)
    for exposure in [_rank_cs(ret5), _rank_cs(ret10), _rank_cs(ret20), _rank_cs(ret60), _rank_cs(-ret20)]:
        signal = _rank_cs(_cs_neutralize(signal, exposure))
    signal = _rank_cs(_rebalance_interval(signal * gate, 10))
    signal = _clean_panel(signal)

    diagnostics = pd.DataFrame(
        {
            "component": [
                "moderate_positive_participation",
                "relative_stability",
                "range_orderliness",
                "close_support",
                "residual_vol_order",
                "participation_normalization",
                "no_extension",
                "post_repair_gate",
                "continuation_quality",
                "final_signal",
            ],
            "finite_pct": [
                float(moderate_positive_participation.notna().mean().mean()),
                float(relative_stability.notna().mean().mean()),
                float(range_orderliness.notna().mean().mean()),
                float(close_support.notna().mean().mean()),
                float(residual_vol_order.notna().mean().mean()),
                float(participation_normalization.notna().mean().mean()),
                float(no_extension.notna().mean().mean()),
                float(gate.notna().mean().mean()),
                float(continuation_quality.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(moderate_positive_participation.abs().mean().mean()),
                float(relative_stability.abs().mean().mean()),
                float(range_orderliness.abs().mean().mean()),
                float(close_support.abs().mean().mean()),
                float(residual_vol_order.abs().mean().mean()),
                float(participation_normalization.abs().mean().mean()),
                float(no_extension.abs().mean().mean()),
                float(gate.abs().mean().mean()),
                float(continuation_quality.abs().mean().mean()),
                float(signal.abs().mean().mean()),
            ],
        }
    )
    return {SIGNAL_NAME: signal}, states, diagnostics


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    close = panels["close"]
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret15 = close.pct_change(15, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)
    rank20 = residual20.rank(axis=1, pct=True)
    repair_participation_proxy = _rank_cs(
        (
            rank20
            * (1.0 - ret20.rank(axis=1, pct=True).sub(0.62).abs() * 2.0).clip(lower=0.0)
        ).rolling(5, min_periods=3).mean()
    )
    active_breadth_repair_proxy = _rank_cs(
        (
            _rank_cs(-ret20)
            * (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
        ).rolling(5, min_periods=3).mean()
    )
    refs["price_rank_momentum_5"] = _rank_cs(ret5).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_10"] = _rank_cs(ret10).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_15"] = _rank_cs(ret15).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_20"] = _rank_cs(ret20).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_60"] = _rank_cs(ret60).reindex(index=first.index, columns=first.columns)
    refs["post_repair_participation_proxy"] = repair_participation_proxy.reindex(index=first.index, columns=first.columns)
    refs["active_breadth_repair_proxy"] = active_breadth_repair_proxy.reindex(index=first.index, columns=first.columns)
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


def post_repair_corr_summary(orth: pd.DataFrame) -> pd.DataFrame:
    summary = max_corr_table(orth)
    rows = []
    for name, group in orth.groupby("signal_name"):
        row = {"signal_name": name}
        comparisons = [
            "price_rank_momentum_5",
            "price_rank_momentum_10",
            "price_rank_momentum_15",
            "price_rank_momentum_20",
            "price_rank_momentum_60",
            "post_repair_participation_proxy",
            "active_breadth_repair_proxy",
        ]
        for comparison in comparisons:
            sample = group[group["comparison"].eq(comparison)]
            row[f"{comparison}_corr"] = float(sample["abs_value_corr"].max()) if not sample.empty else np.nan
        momentum_refs = group[group["comparison"].isin(["plain_momentum_60", "price_rank_momentum_5", "price_rank_momentum_10", "price_rank_momentum_15", "price_rank_momentum_20", "price_rank_momentum_60"])]
        breadth_repair_refs = group[group["comparison"].isin(["active_breadth_repair_proxy", "inventory_participation_breadth_repair_under_hostile_trend"])]
        row["max_price_momentum_corr"] = float(momentum_refs["abs_value_corr"].max()) if not momentum_refs.empty else np.nan
        row["max_breadth_repair_corr"] = float(breadth_repair_refs["abs_value_corr"].max()) if not breadth_repair_refs.empty else np.nan
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
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    h5 = scores[scores["horizon"].eq(5)].rename(columns={"mean_ic": "h5_mean_ic", "positive_ic_rate": "h5_positive_ic_rate"})
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h15 = scores[scores["horizon"].eq(15)].rename(columns={"mean_ic": "h15_mean_ic", "positive_ic_rate": "h15_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    resolved_counts = (
        state_attr[state_attr["state"].isin(["POST_REPAIR_BREADTH_RECOVERY", "POST_REPAIR_QUALITY_CONFIRMATION", "BREADTH_CONFIRMED_RECOVERY", "RESOLVED_STRESS_OR_REPAIR"])]
        .groupby("signal_name")["mean_ic"]
        .agg(positive_resolved_state_count=lambda s: int((s > 0.004).sum()), best_resolved_state_ic="max")
        .reset_index()
    )
    active_counts = (
        state_attr[state_attr["state"].isin(["ACTIVE_HOSTILE_BREADTH_REPAIR", "HOSTILE_OR_STRESS", "weak_breadth", "drawdown_acceleration", "volatility_spike", "panic_liquidity_stress"])]
        .groupby("signal_name")["mean_ic"]
        .agg(best_active_repair_state_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h15[["signal_name", "h15_mean_ic", "h15_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(resolved_counts, on="signal_name", how="left")
        .merge(active_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        primary_mean = max(row.get("h10_mean_ic", np.nan), row.get("h15_mean_ic", np.nan), row.get("mean_ic", np.nan))
        primary_pos = max(row.get("h10_positive_ic_rate", np.nan), row.get("h15_positive_ic_rate", np.nan), row.get("positive_ic_rate", np.nan))
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.14:
            issues.append("high_turnover")
        if primary_mean < 0.006:
            issues.append("weak_primary_ic")
        if primary_pos < 0.52:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.65:
            issues.append("activation_too_broad")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_breadth_repair_corr", 0) > 0.35:
            issues.append("breadth_repair_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.45:
            issues.append("reversal_similarity_risk")
        if row.get("max_price_momentum_corr", 0) > 0.45:
            issues.append("momentum_similarity_risk")
        if row.get("positive_resolved_state_count", 0) < 2:
            issues.append("weak_resolved_state_support")
        if row.get("best_active_repair_state_ic", -1) > row.get("best_resolved_state_ic", np.nan):
            issues.append("active_repair_dependence_risk")

        if (
            primary_mean > 0.014
            and primary_pos >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.10
            and 0.10 <= row.get("active_date_ratio", 0) <= 0.55
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_breadth_repair_corr", 1) <= 0.30
            and row.get("max_price_momentum_corr", 1) <= 0.40
            and row.get("positive_resolved_state_count", 0) >= 3
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            primary_mean > 0.009
            and primary_pos >= 0.525
            and row.get("positive_resolved_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_breadth_repair_corr", 1) <= 0.35
            and row.get("active_date_ratio", 0) >= 0.10
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_resolved_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.40
            and row.get("max_breadth_repair_corr", 1) <= 0.40
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "post_repair_continuation",
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h5_mean_ic": row.get("h5_mean_ic"),
                "h5_positive_ic_rate": row.get("h5_positive_ic_rate"),
                "h10_mean_ic": row.get("h10_mean_ic"),
                "h10_positive_ic_rate": row.get("h10_positive_ic_rate"),
                "h15_mean_ic": row.get("h15_mean_ic"),
                "h15_positive_ic_rate": row.get("h15_positive_ic_rate"),
                "h20_mean_ic": row.get("h20_mean_ic"),
                "h20_positive_ic_rate": row.get("h20_positive_ic_rate"),
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_breadth_repair_corr": row.get("max_breadth_repair_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "post_repair_participation_proxy_corr": row.get("post_repair_participation_proxy_corr"),
                "active_breadth_repair_proxy_corr": row.get("active_breadth_repair_proxy_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "inventory_volatility_corr": row.get("inventory_volatility_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_resolved_state_count": int(row.get("positive_resolved_state_count", 0) or 0),
                "best_resolved_state_ic": row.get("best_resolved_state_ic"),
                "best_active_repair_state_ic": row.get("best_active_repair_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def _decision_text(decision: pd.Series) -> str:
    status = str(decision["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return "`post_repair_continuation_after_breadth_recovery` should move to formal conditional validation using this fixed single formulation."
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return "`post_repair_continuation_after_breadth_recovery` should receive a narrow refinement diagnostics pass focused on h10-h15 behavior, resolved-state support, and breadth-repair separation."
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return "`post_repair_continuation_after_breadth_recovery` should remain conditional-only evidence until edge quality and resolved-state attribution improve."
    return "`post_repair_continuation_after_breadth_recovery` should be rejected in this formulation before moving to another Expansion v4 concept."


def _fmt(value: object) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{float(value):.6f}"


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
    h_table = scores[scores["horizon"].isin([5, 10, 15, 20])].copy()
    top_states = state_attr.sort_values("mean_ic", ascending=False).head(16)
    top_stress = stress.sort_values("mean_ic", ascending=False).head(8)
    lines = [
        "# Post Repair Continuation After Breadth Recovery v1",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only run tested one simple formulation of `{SIGNAL_NAME}` under the isolated run namespace `{RUN_ID}`.",
        "",
        "The formulation tests whether the project repair/stabilization edge extends into a post-repair continuation phase after breadth recovery has already occurred.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v4 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v4 design screen: `{SOURCE_NOTE}`",
        f"- Expansion v3 mid-cycle review: `{V3_REVIEW_NOTE}`",
        f"- Conditional Alpha Inventory Monitoring v1: `{MONITORING_NOTE}`",
        f"- Conditional Alpha Inventory v2 Governance Update: `{GOVERNANCE_NOTE}`",
        f"- Inventory Ecosystem Review v1: `{ECOSYSTEM_NOTE}`",
        "- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | Breadth repair may have a second phase after weak breadth and hostile pressure clear; names with orderly participation and stable residual behavior may continue as forced selling fades. |",
        "| Breadth-repair completion logic | Requires recent weak-breadth/hostile repair activity, current breadth recovery, no current weak breadth, no hostile benchmark trend, and no recent panic/stress flag. |",
        "| Resolved-stress continuation logic | Selects moderate positive residual participation, relative rank stability, range orderliness, close support, residual volatility order, and participation normalization only inside the post-repair gate. |",
        "| Difference from active hostile-state repair | The signal is gated off when weak breadth, hostile trend, or recent stress is active; it requires those conditions to have recently occurred and then cleared. |",
        "| Difference from raw continuation/momentum | It vetoes extreme price extension and neutralizes h5/h10/h20/h60 return ranks plus 20-day reversal exposure. |",
        "| Difference from current inventory | Current breadth and liquidity candidates activate during hostile/weak-breadth repair; this candidate attempts to activate after breadth repair has completed. |",
        "| Expected activation semantics | Recent repair state, breadth recovered, hostile/stress inactive, orderly post-repair participation. |",
        "| Expected horizon | h10-h15 primary; h20 diagnostic for inventory comparability. |",
        "| Expected turnover | Low-medium after fixed 10-day rebalance control. |",
        "| Expected active coverage | Medium conditional coverage; sparse behavior is a review issue. |",
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
        structural.merge(active, on="signal_name", how="left").to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores.to_markdown(index=False),
        "",
        "## h5 / h10 / h15 / h20 Behavior",
        "",
        h_table.to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False),
        "",
        "## WFV Window Detail",
        "",
        wfv_windows.to_markdown(index=False),
        "",
        "## Baseline And Inventory Similarity",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Hostile / Stress Vs Resolved / Neutral Attribution",
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
        f"- Genuinely post-repair continuation: positive resolved-state count was `{int(decision['positive_resolved_state_count'])}` and best resolved-state IC was `{_fmt(decision['best_resolved_state_ic'])}`.",
        f"- Active hostile-state breadth repair risk: max breadth-repair correlation was `{_fmt(decision['max_breadth_repair_corr'])}`; inventory breadth correlation was `{_fmt(decision['inventory_breadth_corr'])}`.",
        f"- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `{_fmt(decision['max_price_momentum_corr'])}` / `{_fmt(decision['max_reversal_corr'])}`.",
        f"- Inventory overlap risk: max inventory correlation was `{_fmt(decision['max_inventory_corr'])}`.",
        f"- Sparse or broad activation risk: active date ratio was `{_fmt(decision['active_date_ratio'])}`.",
        f"- Turnover risk: turnover proxy was `{_fmt(decision['turnover_proxy'])}`.",
        f"- Directional stability: WFV-style persistence/sign consistency were `{_fmt(decision['wfv_persistence'])}` / `{_fmt(decision['wfv_sign_consistency'])}`.",
        f"- h5/h10/h15/h20 profile: h5 `{_fmt(decision['h5_mean_ic'])}`, h10 `{_fmt(decision['h10_mean_ic'])}`, h15 `{_fmt(decision['h15_mean_ic'])}`, h20 `{_fmt(decision['h20_mean_ic'])}`.",
        "",
        "## Recommended Next Step",
        "",
        _decision_text(decision),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, component_diagnostics = build_post_repair_signal(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "post_repair_continuation",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V4_RESEARCH_ONLY",
                "mechanism_thesis": "Post-repair continuation after weak-breadth recovery has already completed.",
                "state_transition_logic": "Recent weak-breadth/hostile repair, current breadth recovery, hostile/stress inactive, orderly post-repair participation.",
                "differs_from_inventory": "Activates after repair completion instead of during hostile/weak-breadth repair.",
                "differs_from_reversal_momentum": "Neutralizes return-rank and reversal exposures and vetoes extreme extension.",
                "expected_activation_state": "POST_REPAIR_BREADTH_RECOVERY",
                "expected_horizon": "h10-h15 primary; h20 diagnostic",
                "expected_turnover_profile": "low_to_medium",
                "expected_active_coverage": "medium",
            }
        ]
    )
    structural = structural_summary(signals)
    scores, daily_ics = score_signals_h15(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = post_repair_corr_summary(orth)
    active = active_coverage_summary(signals)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidate(structural, scores, wfv_summary, state_attr, orth_summary, active)

    registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    component_diagnostics.to_csv(OUT_DIR / "component_diagnostics.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    states.to_csv(OUT_DIR / "state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "state_attribution.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    sample_sizes.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decision.csv", index=False)
    signals[SIGNAL_NAME].to_parquet(OUT_DIR / f"{SIGNAL_NAME}_signal_panel.parquet")

    artifact_files = [
        "candidate_registry.csv",
        "component_diagnostics.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "state_flags.csv",
        "stress_regime_attribution.csv",
        "state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "sample_size_sanity.csv",
        "candidate_decision.csv",
        f"{SIGNAL_NAME}_signal_panel.parquet",
        "manifest.json",
    ]
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "signal_name": SIGNAL_NAME,
                "research_only": True,
                "source_note": str(SOURCE_NOTE),
                "v3_review_note": str(V3_REVIEW_NOTE),
                "candidate_count": 1,
                "broad_search": False,
                "parameter_grid": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "other_expansion_v4_concepts_implemented": False,
                "final_classification": str(decisions.iloc[0]["status"]),
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
