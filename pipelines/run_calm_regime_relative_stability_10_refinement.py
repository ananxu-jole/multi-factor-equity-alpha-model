from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
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
    active_coverage_summary,
    state_attribution,
    _market_state_panel,
    _rebalance_interval,
)
from run_calm_regime_relative_stability_10_v1 import (
    NOTE_PATH as SOURCE_V1_NOTE,
    SIGNAL_NAME as BASE_SIGNAL_NAME,
    _rolling_quantile,
    _safe_div,
    calm_corr_summary,
    reference_panels,
)


RUN_ID = "calm_regime_relative_stability_10_refinement"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/calm_regime_relative_stability_10_refinement.md")
SOURCE_ARTIFACT_DIR = Path("artifacts/research/calm_regime_relative_stability_10_v1")
DESIGN_NOTE = Path("docs/research_notes/track_b_expansion_v3_design_screening.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v1.md")
GOVERNANCE_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md")


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _active_dates(panel: pd.DataFrame) -> pd.Series:
    return (panel.notna().sum(axis=1) >= 25) & (panel.abs().mean(axis=1, skipna=True) > 0.02)


def _build_state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    relative_stability: pd.DataFrame,
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
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    bench_vol20 = bench_ret.rolling(20, min_periods=15).std()
    dispersion20 = ret20.std(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    rank_churn_market = ret20.rank(axis=1, pct=True).diff().abs().mean(axis=1)

    trend_hostile = ((benchmark < bench_ma60) & (bench_20 < 0)).fillna(False)
    weak_breadth = stress["weak_breadth"].fillna(False)
    non_hostile = (~stress_recent & ~trend_hostile & ~weak_breadth).fillna(False)
    calm_vol = ((bench_vol20 < _rolling_quantile(bench_vol20, 0.60)) & (bench_vol20 > _rolling_quantile(bench_vol20, 0.08))).fillna(False)
    calm_vol_broad = (bench_vol20 < _rolling_quantile(bench_vol20, 0.70)).fillna(False)
    normal_dispersion = ((dispersion20 < _rolling_quantile(dispersion20, 0.65)) & (dispersion20 > _rolling_quantile(dispersion20, 0.10))).fillna(False)
    normal_dispersion_broad = (dispersion20 < _rolling_quantile(dispersion20, 0.75)).fillna(False)
    orderly_ranks = (rank_churn_market < _rolling_quantile(rank_churn_market, 0.60)).fillna(False)
    balanced_breadth = ((breadth20 > _rolling_quantile(breadth20, 0.30)) & (breadth20 < _rolling_quantile(breadth20, 0.85))).fillna(False)
    balanced_breadth_broad = ((breadth20 > _rolling_quantile(breadth20, 0.25)) & (breadth20 < _rolling_quantile(breadth20, 0.90))).fillna(False)
    high_stability = relative_stability.mean(axis=1, skipna=True) > relative_stability.stack().median()

    states = pd.DataFrame(index=close.index)
    states["CALM_REGIME_BASE"] = (non_hostile & calm_vol & normal_dispersion & balanced_breadth).fillna(False)
    states["CALM_REGIME_BROAD"] = (non_hostile & calm_vol_broad & normal_dispersion_broad & balanced_breadth_broad).fillna(False)
    states["CALM_REGIME_STRICT"] = (states["CALM_REGIME_BASE"] & orderly_ranks).fillna(False)
    states["NON_HOSTILE_REGIME"] = non_hostile
    states["CALM_NORMAL_VOL"] = (non_hostile & calm_vol).fillna(False)
    states["NORMAL_DISPERSION"] = (non_hostile & normal_dispersion).fillna(False)
    states["ORDERLY_CROSS_SECTION"] = (non_hostile & orderly_ranks).fillna(False)
    states["BALANCED_BREADTH"] = (non_hostile & balanced_breadth).fillna(False)
    states["CALM_WITH_HIGH_RELATIVE_STABILITY"] = (states["CALM_REGIME_BASE"] & high_stability).fillna(False)
    states["HOSTILE_OR_STRESS"] = (stress_recent | trend_hostile | weak_breadth).fillna(False)
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def _components(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual1 = ret1.sub(benchmark.pct_change(1, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    rank10 = residual10.rank(axis=1, pct=True)
    rank20 = ret20.rank(axis=1, pct=True)
    rank10_churn = rank10.diff().abs().rolling(10, min_periods=6).mean()
    rank20_churn = rank20.diff().abs().rolling(20, min_periods=12).mean()
    rank_stability_10 = (1.0 - rank10_churn.rank(axis=1, pct=True)).clip(lower=0.0)
    rank_stability_20 = (1.0 - rank20_churn.rank(axis=1, pct=True)).clip(lower=0.0)
    relative_rank_stability = (rank_stability_10 * rank_stability_20).clip(lower=0.0)
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol30 = residual1.rolling(30, min_periods=20).std()
    residual_vol_stability = (1.0 - _safe_div(residual_vol10, residual_vol30).rank(axis=1, pct=True)).clip(lower=0.0)
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range_orderliness = (
        1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True)
    ).clip(lower=0.0)
    path_orderliness = (1.0 - ret1.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
    neutral_extension = (
        (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
        * (1.0 - ret20.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
    ).clip(lower=0.0)
    relative_stability = (
        relative_rank_stability * residual_vol_stability * range_orderliness * path_orderliness * neutral_extension
    ).rolling(5, min_periods=3).mean()
    components = {
        "ret5_rank": _rank_cs(ret5),
        "ret10_rank": _rank_cs(ret10),
        "ret20_rank": _rank_cs(ret20),
        "ret60_rank": _rank_cs(ret60),
        "reversal20_rank": _rank_cs(-ret20),
        "rank_stability_10": rank_stability_10,
        "relative_rank_stability": relative_rank_stability,
        "residual_vol_stability": residual_vol_stability,
        "range_orderliness": range_orderliness,
        "path_orderliness": path_orderliness,
        "neutral_extension": neutral_extension,
        "relative_stability": relative_stability,
        "low_residual_vol": _rank_cs(-residual1.rolling(20, min_periods=15).std()),
    }
    states = _build_state_flags(panels, benchmark, relative_stability)
    return components, states


def _finalize(
    raw: pd.DataFrame,
    gate: pd.Series,
    components: dict[str, pd.DataFrame],
    rebalance: int,
    smooth: int | None = None,
    low_vol_neutralize: bool = False,
    inactive_nan: bool = False,
) -> pd.DataFrame:
    gate_panel = _market_state_panel(gate, raw.columns)
    gated = raw.where(gate_panel.astype(bool)) if inactive_nan else raw * gate_panel
    signal = _rank_cs(gated)
    exposures = [
        components["ret5_rank"],
        components["ret10_rank"],
        components["ret20_rank"],
        components["ret60_rank"],
        components["reversal20_rank"],
    ]
    if low_vol_neutralize:
        exposures.append(components["low_residual_vol"])
    for exposure in exposures:
        signal = _rank_cs(_cs_neutralize(signal, exposure))
    if smooth:
        signal = _rank_cs(signal.rolling(smooth, min_periods=max(2, smooth // 2)).mean())
    signal = _rank_cs(_rebalance_interval(signal * gate_panel, rebalance))
    return _clean_panel(signal)


def build_variants(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    components, states = _components(panels, benchmark)
    base = components["relative_stability"]
    strong = (components["relative_rank_stability"] ** 1.5 * components["residual_vol_stability"] * components["range_orderliness"] * components["neutral_extension"]).rolling(5, min_periods=3).mean()
    h10_raw = (components["rank_stability_10"] * components["range_orderliness"] * components["path_orderliness"] * components["neutral_extension"]).rolling(3, min_periods=2).mean()

    specs = [
        ("base_rebalance_10_zero", base, "CALM_REGIME_BASE", 10, None, False, False, "v1 baseline representation"),
        ("h10_focus_rebalance_5_zero", h10_raw, "CALM_REGIME_BASE", 5, None, False, False, "h10-focused rank-stability formulation with shorter rebalance"),
        ("smooth_3_rebalance_10_zero", base, "CALM_REGIME_BASE", 10, 3, False, False, "mild smoothing before 10-day rebalance"),
        ("rebalance_5_zero", base, "CALM_REGIME_BASE", 5, None, False, False, "same logic with 5-day rebalance"),
        ("rebalance_20_zero", base, "CALM_REGIME_BASE", 20, None, False, False, "same logic with 20-day rebalance"),
        ("broad_calm_rebalance_10_zero", base, "CALM_REGIME_BROAD", 10, None, False, False, "broader calm gate for active coverage protection"),
        ("strict_calm_rebalance_10_zero", base, "CALM_REGIME_STRICT", 10, None, False, False, "stricter calm/orderly cross-section confirmation"),
        ("strong_stability_rebalance_10_zero", strong, "CALM_REGIME_BASE", 10, None, False, False, "stronger relative-stability confirmation"),
        ("lowvol_neutralized_rebalance_10_zero", base, "CALM_REGIME_BASE", 10, None, True, False, "explicit low residual volatility neutralization"),
        ("inactive_nan_rebalance_10", base, "CALM_REGIME_BASE", 10, None, False, True, "NaN inactive handling instead of zero inactive handling"),
    ]
    signals = {
        name: _finalize(raw, states[gate], components, rebalance, smooth, lowvol, inactive_nan)
        for name, raw, gate, rebalance, smooth, lowvol, inactive_nan, _ in specs
    }
    registry = pd.DataFrame(
        [
            {
                "variant_name": name,
                "signal_name": name,
                "family": "calm_regime_relative_stability",
                "run_id": RUN_ID,
                "gate": gate,
                "rebalance_interval": rebalance,
                "smooth": smooth or 0,
                "low_vol_neutralized": lowvol,
                "inactive_handling": "nan" if inactive_nan else "zero",
                "description": desc,
            }
            for name, _, gate, rebalance, smooth, lowvol, inactive_nan, desc in specs
        ]
    )
    return signals, states, registry


def _sample_size_summary(states: pd.DataFrame, signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        active = _active_dates(panel)
        for state_name, mask in states.items():
            state_mask = mask.astype(bool)
            rows.append(
                {
                    "signal_name": signal_name,
                    "state": state_name,
                    "state_dates": int(state_mask.sum()),
                    "state_date_ratio": float(state_mask.mean()),
                    "signal_active_overlap_dates": int((state_mask & active).sum()),
                    "signal_active_overlap_ratio": float((state_mask & active).mean()),
                }
            )
        rows.append(
            {
                "signal_name": signal_name,
                "state": "SIGNAL_ACTIVE",
                "state_dates": int(active.sum()),
                "state_date_ratio": float(active.mean()),
                "signal_active_overlap_dates": int(active.sum()),
                "signal_active_overlap_ratio": float(active.mean()),
            }
        )
    return pd.DataFrame(rows)


def _window_concentration(wfv: pd.DataFrame, windows: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in wfv.iterrows():
        sample = windows[
            windows["signal_name"].eq(row["signal_name"])
            & windows["horizon"].eq(row["horizon"])
            & windows["mean_test_ic"].gt(0)
        ]
        total = sample["mean_test_ic"].sum()
        rows.append(
            {
                "signal_name": row["signal_name"],
                "horizon": int(row["horizon"]),
                "positive_window_count": int(sample.shape[0]),
                "one_window_dominance": float(sample["mean_test_ic"].max() / total) if total and total > 0 else np.nan,
            }
        )
    return pd.DataFrame(rows)


def classify_variants(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    concentration: pd.DataFrame,
) -> pd.DataFrame:
    h5 = scores[scores["horizon"].eq(5)].rename(columns={"mean_ic": "h5_mean_ic", "positive_ic_rate": "h5_positive_ic_rate"})
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    best = scores.loc[scores["is_best_horizon"]].copy()
    calm_counts = (
        state_attr[
            state_attr["state"].isin(
                ["CALM_REGIME_BASE", "CALM_REGIME_BROAD", "CALM_REGIME_STRICT", "CALM_WITH_HIGH_RELATIVE_STABILITY", "CALM_NORMAL_VOL", "NORMAL_DISPERSION"]
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
        registry.merge(best, on="signal_name", how="left")
        .merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(concentration, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(calm_counts, on="signal_name", how="left")
        .merge(hostile_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        one_window_dominance = row.get("one_window_dominance")
        if one_window_dominance is None or pd.isna(one_window_dominance):
            one_window_dominance = row.get("one_window_dominance_x")
        if one_window_dominance is None or pd.isna(one_window_dominance):
            one_window_dominance = row.get("one_window_dominance_y")
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.10:
            issues.append("high_turnover")
        if row.get("h10_mean_ic", np.nan) < 0.010:
            issues.append("weak_h10_ic")
        if row.get("h10_positive_ic_rate", np.nan) < 0.525:
            issues.append("weak_h10_positive_rate")
        if row.get("h20_mean_ic", np.nan) < 0.012:
            issues.append("h20_strength_not_preserved")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if pd.notna(one_window_dominance) and one_window_dominance > 0.65:
            issues.append("one_window_dominance_risk")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_price_momentum_corr", 0) > 0.40:
            issues.append("momentum_similarity_risk")
        if row.get("max_low_volatility_corr", 0) > 0.45:
            issues.append("low_volatility_similarity_risk")
        if row.get("positive_calm_state_count", 0) < 2:
            issues.append("weak_calm_state_support")
        if row.get("best_hostile_state_ic", -1) > row.get("best_calm_state_ic", np.nan):
            issues.append("hostile_state_dependence_risk")

        if (
            row.get("h10_mean_ic", 0) >= 0.014
            and row.get("h10_positive_ic_rate", 0) >= 0.54
            and row.get("h20_mean_ic", 0) >= 0.018
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("active_date_ratio", 0) >= 0.10
            and row.get("turnover_proxy", 1) <= 0.08
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_low_volatility_corr", 1) <= 0.40
            and pd.notna(one_window_dominance)
            and one_window_dominance <= 0.65
            and row.get("positive_calm_state_count", 0) >= 3
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif row.get("h10_mean_ic", 0) >= 0.010 and row.get("positive_calm_state_count", 0) >= 2:
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif row.get("positive_calm_state_count", 0) >= 2:
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "variant_name": row["variant_name"],
                "description": row["description"],
                "gate": row["gate"],
                "rebalance_interval": row["rebalance_interval"],
                "smooth": row["smooth"],
                "low_vol_neutralized": row["low_vol_neutralized"],
                "inactive_handling": row["inactive_handling"],
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h5_mean_ic": row.get("h5_mean_ic"),
                "h10_mean_ic": row.get("h10_mean_ic"),
                "h10_positive_ic_rate": row.get("h10_positive_ic_rate"),
                "h20_mean_ic": row.get("h20_mean_ic"),
                "h20_positive_ic_rate": row.get("h20_positive_ic_rate"),
                "turnover_proxy": row.get("turnover_proxy"),
                "active_date_ratio": row.get("active_date_ratio"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "one_window_dominance": one_window_dominance,
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "max_low_volatility_corr": row.get("max_low_volatility_corr"),
                "max_simple_stability_corr": row.get("max_simple_stability_corr"),
                "positive_calm_state_count": int(row.get("positive_calm_state_count", 0) or 0),
                "best_calm_state_ic": row.get("best_calm_state_ic"),
                "best_hostile_state_ic": row.get("best_hostile_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    decisions = pd.DataFrame(rows)
    decisions["selection_score"] = (
        decisions["h10_mean_ic"].fillna(0) * 100
        + decisions["h20_mean_ic"].fillna(0) * 40
        + decisions["h10_positive_ic_rate"].fillna(0)
        - decisions["max_low_volatility_corr"].fillna(1) * 0.5
        - decisions["max_inventory_corr"].fillna(1) * 0.5
    )
    return decisions.sort_values(["status", "selection_score"], ascending=[True, False])


def _overall_classification(decisions: pd.DataFrame) -> str:
    if (decisions["status"] == "CANDIDATE_FOR_CONDITIONAL_VALIDATION").any():
        return "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
    if (decisions["status"] == "CONDITIONAL_REFINEMENT_CANDIDATE").any():
        return "CONDITIONAL_REFINEMENT_CANDIDATE"
    if (decisions["status"] == "CONDITIONAL_ONLY_RESEARCH").any():
        return "CONDITIONAL_ONLY_RESEARCH"
    return "REJECT_RESEARCH"


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    windows: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    state_attr: pd.DataFrame,
    sample_sizes: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    def _fmt(value: object) -> str:
        if value is None or pd.isna(value):
            return "NA"
        return f"{float(value):.6f}"

    overall = _overall_classification(decisions)
    leader = decisions.sort_values("selection_score", ascending=False).iloc[0]
    h_table = scores[scores["horizon"].isin([5, 10, 20])][
        ["signal_name", "horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]
    ]
    top_state = state_attr.sort_values("mean_ic", ascending=False).head(18)
    lines = [
        "# Calm Regime Relative Stability 10 Refinement",
        "",
        "## Executive Takeaway",
        "",
        "This research-only refinement diagnostics pass tested a small controlled set of interpretable variants for `calm_regime_relative_stability_10`.",
        "",
        f"Final classification: `{overall}`",
        f"Selected refinement variant: `{leader['variant_name']}`",
        f"Selected variant issues: `{leader['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, broad search, or implementation of other Expansion v3 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- v1 note: `{SOURCE_V1_NOTE}`",
        f"- v1 artifacts: `{SOURCE_ARTIFACT_DIR}`",
        f"- Expansion v3 design screen: `{DESIGN_NOTE}`",
        f"- Inventory Monitoring v1: `{MONITORING_NOTE}`",
        f"- Inventory Governance v2: `{GOVERNANCE_NOTE}`",
        "",
        "## Refinement Scope",
        "",
        "Controlled areas tested: calm-regime strictness, relative-stability confirmation strength, h10-focused formulation, mild smoothing, rebalance interval, active coverage protection, low-volatility similarity control, and inactive-date handling.",
        "",
        "This is not a parameter grid. Each variant changes one interpretable design choice from the v1 formulation.",
        "",
        "## Variant Registry",
        "",
        registry.to_markdown(index=False),
        "",
        "## Candidate Decision Summary",
        "",
        decisions.to_markdown(index=False),
        "",
        "## h5 / h10 / h20 Behavior",
        "",
        h_table.to_markdown(index=False),
        "",
        "## Structural Quality And Active Coverage",
        "",
        structural.merge(active, on="signal_name", how="left").to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False),
        "",
        "## WFV Window Detail",
        "",
        windows.to_markdown(index=False),
        "",
        "## Similarity Summary",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Calm / Neutral Vs Hostile / Stress Attribution",
        "",
        top_state[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Sample-Size Sanity",
        "",
        sample_sizes[sample_sizes["state"].isin(["CALM_REGIME_BASE", "CALM_REGIME_BROAD", "CALM_REGIME_STRICT", "CALM_WITH_HIGH_RELATIVE_STABILITY", "HOSTILE_OR_STRESS", "SIGNAL_ACTIVE"])].to_markdown(index=False),
        "",
        "## Diagnostic Answers",
        "",
        f"- h10 improvement: selected variant h10 mean IC is `{_fmt(leader['h10_mean_ic'])}` with positive IC rate `{_fmt(leader['h10_positive_ic_rate'])}`.",
        f"- h20 preservation: selected variant h20 mean IC is `{_fmt(leader['h20_mean_ic'])}`.",
        f"- Active coverage: selected variant active date ratio is `{_fmt(leader['active_date_ratio'])}`.",
        f"- Low-volatility similarity: selected variant max low-volatility correlation is `{_fmt(leader['max_low_volatility_corr'])}`.",
        f"- Inventory overlap: selected variant max inventory correlation is `{_fmt(leader['max_inventory_corr'])}`.",
        f"- Window concentration: selected variant one-window dominance is `{_fmt(leader['one_window_dominance'])}`.",
        "",
        "## Final Recommendation",
        "",
    ]
    if overall == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        lines.append("Move the selected fixed variant to formal conditional validation. Do not add more variants before validation.")
    elif overall == "CONDITIONAL_REFINEMENT_CANDIDATE":
        lines.append("Keep this family in refinement. The evidence remains promising, but the package has not cleanly resolved h10-vs-h20 dependence, sparse activation, and/or low-volatility similarity.")
    elif overall == "CONDITIONAL_ONLY_RESEARCH":
        lines.append("Keep as conditional-only evidence. Do not advance until h10 behavior, coverage, and similarity controls improve.")
    else:
        lines.append("Reject this refinement package and move to the next Expansion v3 concept only if approved.")
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, registry = build_variants(panels, benchmark)
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
    sample_sizes = _sample_size_summary(states, signals)
    concentration = _window_concentration(wfv_summary, wfv_windows)
    decisions = classify_variants(registry, structural, scores, wfv_summary, stress, state_attr, orth_summary, active, concentration)

    files = [
        "variant_registry.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "calm_state_flags.csv",
        "stress_regime_attribution.csv",
        "calm_state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "window_concentration_summary.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "sample_size_sanity.csv",
        "candidate_decisions.csv",
        "manifest.json",
    ]
    registry.to_csv(OUT_DIR / "variant_registry.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    states.to_csv(OUT_DIR / "calm_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "calm_state_attribution.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    concentration.to_csv(OUT_DIR / "window_concentration_summary.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    sample_sizes.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decisions.csv", index=False)
    for name, panel in signals.items():
        panel.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")
        files.append(f"{name}_signal_panel.parquet")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "source_v1_note": str(SOURCE_V1_NOTE),
                "source_v1_artifacts": str(SOURCE_ARTIFACT_DIR),
                "candidate_family": BASE_SIGNAL_NAME,
                "variant_count": len(signals),
                "broad_search": False,
                "parameter_grid": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "other_expansion_v3_concepts_implemented": False,
                "final_classification": _overall_classification(decisions),
                "artifact_files": sorted(files),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_note(registry, structural, scores, wfv_summary, wfv_windows, orth_summary, active, state_attr, sample_sizes, decisions)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
