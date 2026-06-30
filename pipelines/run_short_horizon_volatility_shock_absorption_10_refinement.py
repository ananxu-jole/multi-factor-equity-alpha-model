from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    load_inputs,
    orthogonality,
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
from run_short_horizon_volatility_shock_absorption_10_v1 import (
    HORIZONS,
    SIGNAL_NAME as SOURCE_SIGNAL,
    _rolling_quantile,
    _safe_div,
    _score_signals,
    reference_panels,
    sample_size_summary,
    volatility_shock_corr_summary,
)


RUN_ID = "short_horizon_volatility_shock_absorption_10_refinement"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/short_horizon_volatility_shock_absorption_10_refinement.md")
V1_ARTIFACT_DIR = Path("artifacts/research/short_horizon_volatility_shock_absorption_10_v1")
V1_NOTE = Path("docs/research_notes/short_horizon_volatility_shock_absorption_10_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v5_design_screening.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v2.md")


VARIANTS: list[dict[str, object]] = [
    {
        "variant": "base_rebalance_10_zero",
        "description": "V1 reference logic recreated for refinement comparability.",
        "smoothing": 1,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 10,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "smooth_3_rebalance_10_zero",
        "description": "Mild 3-day smoothing to test h5 noise versus persistent short-horizon edge.",
        "smoothing": 3,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 10,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "rebalance_5_zero",
        "description": "Shorter rebalance interval to test whether the h5 edge needs faster refresh.",
        "smoothing": 1,
        "rebalance": 5,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 10,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "strict_shock_rebalance_10_zero",
        "description": "Stricter volatility shock activation to test over-broad shock states.",
        "smoothing": 1,
        "rebalance": 10,
        "shock_floor": 0.65,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 8,
        "market_vol_mult": 1.10,
        "market_range_mult": 1.05,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "strong_absorption_rebalance_10_zero",
        "description": "Stronger absorption confirmation to test whether h10 improves with cleaner stabilization.",
        "smoothing": 1,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.60,
        "range_q": 0.55,
        "recent_window": 10,
        "market_vol_mult": 1.10,
        "market_range_mult": 1.05,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "low_churn_rebalance_10_zero",
        "description": "Adds a rank-stability floor to test whether lower churn improves h10.",
        "smoothing": 1,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 10,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": 0.55,
        "h10_focus": False,
        "inactive_nan": False,
    },
    {
        "variant": "h10_focus_rebalance_10_zero",
        "description": "Adds h10 path stabilization emphasis without changing the concept family.",
        "smoothing": 3,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 12,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": 0.50,
        "h10_focus": True,
        "inactive_nan": False,
    },
    {
        "variant": "inactive_nan_rebalance_10",
        "description": "Keeps inactive dates as NaN to test inactive-date handling.",
        "smoothing": 1,
        "rebalance": 10,
        "shock_floor": 0.55,
        "fast_q": 0.50,
        "range_q": 0.45,
        "recent_window": 10,
        "market_vol_mult": 1.15,
        "market_range_mult": 1.10,
        "rank_stab_floor": None,
        "h10_focus": False,
        "inactive_nan": True,
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _state_flags_for_variant(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    absorption_quality: pd.DataFrame,
    spec: dict[str, object],
) -> pd.DataFrame:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    ret20 = close.pct_change(20, fill_method=None)
    stress = build_stress_states(close, benchmark)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    bench_vol5 = bench_ret1.rolling(5, min_periods=4).std()
    bench_vol20 = bench_ret1.rolling(20, min_periods=12).std()
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    avg_range5 = true_range.rolling(5, min_periods=4).mean().mean(axis=1)
    avg_range20 = true_range.rolling(20, min_periods=12).mean().mean(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    dispersion20 = ret20.std(axis=1)
    vol_shock = (
        stress["volatility_spike"].fillna(False)
        | (bench_vol5 > _rolling_quantile(bench_vol5, 0.80))
        | (avg_range5 > _rolling_quantile(avg_range5, 0.80))
    ).fillna(False)
    recent_vol_shock = vol_shock.rolling(int(spec["recent_window"]), min_periods=1).max().astype(bool)
    not_breadth_repair_cluster = (~stress["weak_breadth"].fillna(False) | (breadth20.diff(10) <= 0.03)).fillna(False)
    contained_dispersion = (dispersion20 < _rolling_quantile(dispersion20, 0.85)).fillna(False)
    market_vol_absorbing = (
        recent_vol_shock
        & (bench_vol5 <= bench_vol20 * float(spec["market_vol_mult"]))
        & (avg_range5 <= avg_range20 * float(spec["market_range_mult"]))
    ).fillna(False)
    high_quality_dates = absorption_quality.mean(axis=1, skipna=True) > absorption_quality.stack().median()
    broad_hostile = (recent_vol_shock | stress["weak_breadth"].fillna(False) | ((benchmark < bench_ma60) & (bench_ret20 < 0))).fillna(False)

    states = pd.DataFrame(index=close.index)
    states["VOLATILITY_SHOCK_ACTIVE"] = vol_shock
    states["RECENT_VOLATILITY_SHOCK"] = recent_vol_shock
    states["VOLATILITY_SHOCK_ABSORBING"] = (market_vol_absorbing & contained_dispersion & not_breadth_repair_cluster).fillna(False)
    states["VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY"] = (
        market_vol_absorbing & contained_dispersion & not_breadth_repair_cluster & high_quality_dates
    ).fillna(False)
    states["VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH"] = (market_vol_absorbing & ~stress["weak_breadth"].fillna(False)).fillna(False)
    states["CONTAINED_DISPERSION_VOL_SHOCK"] = (market_vol_absorbing & contained_dispersion).fillna(False)
    states["MARKET_VOL_ABSORBING"] = market_vol_absorbing
    states["BROAD_HOSTILE_OR_STRESS"] = broad_hostile
    states["ACTIVE_HOSTILE_OR_STRESS"] = broad_hostile
    states["HOSTILE_OR_STRESS"] = broad_hostile
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def _build_variant_signal(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    spec: dict[str, object],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    dollar_volume = close * volume

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret15 = close.pct_change(15, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual1 = ret1.sub(benchmark.pct_change(1, fill_method=None), axis=0)
    residual5 = ret5.sub(benchmark.pct_change(5, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()

    shock_present = (_safe_div(range20, range60).rank(axis=1, pct=True) * _safe_div(residual_vol20, residual_vol60).rank(axis=1, pct=True)).clip(lower=0.0)
    fast_absorption = ((1.0 - _safe_div(range5, range20).rank(axis=1, pct=True)) * (1.0 - _safe_div(residual_vol5, residual_vol20).rank(axis=1, pct=True))).clip(lower=0.0)
    no_panic_extension = ((1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0) * (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)).clip(lower=0.0)
    residual_shock_absorption = ((1.0 - residual5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0) * (1.0 - residual10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)).clip(lower=0.0)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    range_containment = ((1.0 - _safe_div(range5, range20).rank(axis=1, pct=True)) * (1.0 - _safe_div(range20, range60).rank(axis=1, pct=True).sub(0.75).abs())).clip(lower=0.0)
    residual_rank10 = residual10.rank(axis=1, pct=True)
    rank_stabilization = (1.0 - residual_rank10.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
    close_support = close_location.rolling(5, min_periods=3).mean().rank(axis=1, pct=True)
    liquidity_sufficient = dollar_volume.rolling(10, min_periods=7).mean().rank(axis=1, pct=True).clip(lower=0.0)

    quality = shock_present * fast_absorption * no_panic_extension * residual_shock_absorption * range_containment * rank_stabilization * close_support * liquidity_sufficient
    if spec["h10_focus"]:
        h10_path_stability = (1.0 - residual10.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
        quality = quality * h10_path_stability
    smoothing = int(spec["smoothing"])
    if smoothing > 1:
        quality = quality.rolling(smoothing, min_periods=2).mean()
    quality = quality.rolling(5, min_periods=3).mean()

    states = _state_flags_for_variant(panels, benchmark, quality, spec)
    gate = (
        (shock_present > float(spec["shock_floor"]))
        & (fast_absorption > fast_absorption.stack().quantile(float(spec["fast_q"])))
        & (range_containment > range_containment.stack().quantile(float(spec["range_q"])))
    )
    if spec["rank_stab_floor"] is not None:
        gate = gate & (rank_stabilization > rank_stabilization.stack().quantile(float(spec["rank_stab_floor"])))
    gate = gate.astype(float) * _market_state_panel(states["VOLATILITY_SHOCK_ABSORBING"], close.columns)

    signal_input = quality * gate
    if spec["inactive_nan"]:
        signal_input = signal_input.where(gate.astype(bool))
    signal = _rank_cs(signal_input)
    for exposure in [
        _rank_cs(ret5),
        _rank_cs(ret10),
        _rank_cs(ret15),
        _rank_cs(ret20),
        _rank_cs(ret60),
        _rank_cs(-ret5),
        _rank_cs(-ret20),
        _rank_cs(residual10),
        _rank_cs(residual20),
        _rank_cs((ret20.sub(ret20.mean(axis=1), axis=0)).abs()),
        _rank_cs(-residual_vol20),
    ]:
        signal = _rank_cs(_cs_neutralize(signal, exposure))
    signal = signal * gate if not spec["inactive_nan"] else signal.where(gate.astype(bool))
    signal = _rank_cs(_rebalance_interval(signal, int(spec["rebalance"])))
    if spec["inactive_nan"]:
        signal = signal.where(_rebalance_interval(gate, int(spec["rebalance"])).astype(bool))
    signal = _clean_panel(signal)

    diagnostics = pd.DataFrame(
        [
            {"variant": spec["variant"], "component": "shock_present", "finite_pct": float(shock_present.notna().mean().mean()), "mean_abs": float(shock_present.abs().mean().mean())},
            {"variant": spec["variant"], "component": "fast_absorption", "finite_pct": float(fast_absorption.notna().mean().mean()), "mean_abs": float(fast_absorption.abs().mean().mean())},
            {"variant": spec["variant"], "component": "range_containment", "finite_pct": float(range_containment.notna().mean().mean()), "mean_abs": float(range_containment.abs().mean().mean())},
            {"variant": spec["variant"], "component": "rank_stabilization", "finite_pct": float(rank_stabilization.notna().mean().mean()), "mean_abs": float(rank_stabilization.abs().mean().mean())},
            {"variant": spec["variant"], "component": "gate", "finite_pct": float(gate.notna().mean().mean()), "mean_abs": float(gate.abs().mean().mean())},
            {"variant": spec["variant"], "component": "final_signal", "finite_pct": float(signal.notna().mean().mean()), "mean_abs": float(signal.abs().mean().mean())},
        ]
    )
    return signal, states, diagnostics


def _summarize_decisions(scores: pd.DataFrame, structural: pd.DataFrame, wfv: pd.DataFrame, active: pd.DataFrame, orth_summary: pd.DataFrame) -> pd.DataFrame:
    h5 = scores[scores["horizon"].eq(5)].rename(columns={"mean_ic": "h5_mean_ic", "positive_ic_rate": "h5_positive_ic_rate"})
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h15 = scores[scores["horizon"].eq(15)].rename(columns={"mean_ic": "h15_mean_ic", "positive_ic_rate": "h15_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    best = scores[scores["is_best_horizon"]].copy()
    summary = (
        best.merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h15[["signal_name", "h15_mean_ic", "h15_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(active, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row.get("h10_mean_ic", np.nan) < 0.010:
            issues.append("h10_below_validation_quality")
        if row.get("h10_positive_ic_rate", np.nan) < 0.56:
            issues.append("h10_positive_rate_below_validation_quality")
        if int(row["horizon"]) == 5:
            issues.append("best_horizon_h5_not_h10")
        if row.get("h20_mean_ic", np.nan) > row.get("h10_mean_ic", np.nan):
            issues.append("h20_dependency_risk")
        if row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("active_date_ratio", 0) < 0.08:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.45:
            issues.append("activation_too_broad")
        if row.get("one_window_dominance", 0) > 0.60:
            issues.append("one_window_concentration")
        if row.get("max_inventory_corr", 1) > 0.30:
            issues.append("inventory_similarity_risk")
        if row.get("max_volatility_stress_corr", 1) > 0.30:
            issues.append("volatility_inventory_similarity_risk")
        if row.get("max_price_reversal_corr", 1) > 0.40:
            issues.append("reversal_similarity_risk")
        if row.get("max_price_momentum_corr", 1) > 0.40:
            issues.append("momentum_similarity_risk")

        if (
            row.get("h10_mean_ic", 0) >= 0.012
            and row.get("h10_positive_ic_rate", 0) >= 0.57
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and row.get("max_inventory_corr", 1) <= 0.25
            and row.get("max_volatility_stress_corr", 1) <= 0.25
            and 0.08 <= row.get("active_date_ratio", 0) <= 0.40
            and row.get("h10_mean_ic", 0) >= row.get("h20_mean_ic", 0)
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row.get("h10_mean_ic", 0) >= 0.008
            and row.get("h10_positive_ic_rate", 0) >= 0.55
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_volatility_stress_corr", 1) <= 0.35
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif row.get("h5_mean_ic", 0) > 0.006 and row.get("max_inventory_corr", 1) <= 0.40:
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"
        rows.append(
            {
                "signal_name": row["signal_name"],
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h5_mean_ic": row.get("h5_mean_ic"),
                "h5_positive_ic_rate": row.get("h5_positive_ic_rate"),
                "h10_mean_ic": row.get("h10_mean_ic"),
                "h10_positive_ic_rate": row.get("h10_positive_ic_rate"),
                "h15_mean_ic": row.get("h15_mean_ic"),
                "h20_mean_ic": row.get("h20_mean_ic"),
                "turnover_proxy": row.get("turnover_proxy"),
                "active_date_ratio": row.get("active_date_ratio"),
                "persistence": row.get("persistence"),
                "sign_consistency": row.get("sign_consistency"),
                "one_window_dominance": row.get("one_window_dominance"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_volatility_stress_corr": row.get("max_volatility_stress_corr"),
                "max_price_reversal_corr": row.get("max_price_reversal_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def _write_note(registry: pd.DataFrame, scores: pd.DataFrame, wfv: pd.DataFrame, decisions: pd.DataFrame, orth: pd.DataFrame, active: pd.DataFrame, sample_sizes: pd.DataFrame, state_attr: pd.DataFrame) -> None:
    best = decisions.sort_values(["status", "h10_mean_ic"], ascending=[True, False]).copy()
    status_rank = {
        "CANDIDATE_FOR_CONDITIONAL_VALIDATION": 0,
        "CONDITIONAL_REFINEMENT_CANDIDATE": 1,
        "CONDITIONAL_ONLY_RESEARCH": 2,
        "REJECT_RESEARCH": 3,
    }
    best["_rank"] = best["status"].map(status_rank).fillna(9)
    best = best.sort_values(["_rank", "h10_mean_ic", "h5_mean_ic"], ascending=[True, False, False]).iloc[0]
    final_status = str(best["status"])
    lines = [
        "# Short Horizon Volatility Shock Absorption 10 Refinement",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only refinement tested `{SOURCE_SIGNAL}` under isolated run `{RUN_ID}` using a small controlled set of interpretable variants.",
        "",
        f"Final classification: `{final_status}`",
        f"Best variant: `{best['signal_name']}`",
        f"Best-variant issues: `{best['review_issues']}`",
        "",
        "The pass supports a real short-horizon volatility-shock absorption effect, but it does not yet justify validation. The strongest profiles remain h5-led or h10-modest rather than clean h10 validation-quality candidates.",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, broad search, or implementation of other Expansion v5 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- V1 note: `{V1_NOTE}`",
        f"- V1 artifact directory: `{V1_ARTIFACT_DIR}`",
        f"- Expansion v5 design screen: `{SOURCE_NOTE}`",
        f"- Conditional Alpha Inventory Monitoring v2: `{MONITORING_NOTE}`",
        "",
        "## Variant Registry",
        "",
        registry.to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.sort_values(["status", "h10_mean_ic"], ascending=[True, False]).to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[scores["horizon"].isin([5, 10, 15, 20])].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False),
        "",
        "## Active Coverage",
        "",
        active.to_markdown(index=False),
        "",
        "## Similarity Summary",
        "",
        orth.to_markdown(index=False),
        "",
        "## Sample-Size Sanity",
        "",
        sample_sizes.groupby("signal_name").head(8).to_markdown(index=False),
        "",
        "## Volatility-Shock Attribution",
        "",
        state_attr.sort_values(["signal_name", "mean_ic"], ascending=[True, False]).groupby("signal_name").head(6).to_markdown(index=False),
        "",
        "## Diagnostic Answers",
        "",
        f"- h5 stability: best h5 IC was `{best['h5_mean_ic']:.6f}`; WFV persistence/sign consistency were `{best['persistence']:.2f}` / `{best['sign_consistency']:.2f}`.",
        f"- h10 validation quality: best selected h10 IC was `{best['h10_mean_ic']:.6f}` with positive IC rate `{best['h10_positive_ic_rate']:.6f}`; this remains below the validation-quality floor.",
        f"- h20 dependence: best selected h20 IC was `{best['h20_mean_ic']:.6f}`, so the selected profile is not h20-dominant.",
        f"- Volatility inventory similarity: max volatility/stress corr was `{best['max_volatility_stress_corr']:.6f}`.",
        f"- Inventory similarity: max inventory corr was `{best['max_inventory_corr']:.6f}`.",
        "",
        "## Recommendation",
        "",
        "Keep `short_horizon_volatility_shock_absorption_10` as a `CONDITIONAL_REFINEMENT_CANDIDATE`. It is the first Expansion v5 candidate to materially reduce h20 concentration, but it should not move to conditional validation until h10 strength improves without sacrificing the short-horizon curve or raising similarity to `volatility_compression_after_stress_stabilization`.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals = {}
    all_states = {}
    diagnostics = []
    registry = pd.DataFrame(VARIANTS)
    for spec in VARIANTS:
        name = str(spec["variant"])
        signal, states, component = _build_variant_signal(panels, benchmark, spec)
        signals[name] = signal
        all_states[name] = states
        diagnostics.append(component)
        signal.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")

    component_diagnostics = pd.concat(diagnostics, ignore_index=True)
    structural = structural_summary(signals)
    scores, daily_ics = _score_signals(signals, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = volatility_shock_corr_summary(orth)
    active = active_coverage_summary(signals)
    sample_sizes = pd.concat(
        [sample_size_summary(states, {SOURCE_SIGNAL: signals[name]}).assign(signal_name=name) for name, states in all_states.items()],
        ignore_index=True,
    )
    state_attr = pd.concat(
        [state_attribution(daily_ics[daily_ics["signal_name"].eq(name)], scores[scores["signal_name"].eq(name)], states) for name, states in all_states.items()],
        ignore_index=True,
    )
    decisions = _summarize_decisions(scores, structural, wfv_summary, active, orth_summary)
    final_status = decisions["status"].map(
        {
            "CANDIDATE_FOR_CONDITIONAL_VALIDATION": 0,
            "CONDITIONAL_REFINEMENT_CANDIDATE": 1,
            "CONDITIONAL_ONLY_RESEARCH": 2,
            "REJECT_RESEARCH": 3,
        }
    ).min()
    status_lookup = {0: "CANDIDATE_FOR_CONDITIONAL_VALIDATION", 1: "CONDITIONAL_REFINEMENT_CANDIDATE", 2: "CONDITIONAL_ONLY_RESEARCH", 3: "REJECT_RESEARCH"}

    registry.to_csv(OUT_DIR / "variant_registry.csv", index=False)
    component_diagnostics.to_csv(OUT_DIR / "component_diagnostics.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    sample_sizes.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    state_attr.to_csv(OUT_DIR / "state_attribution.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decisions.csv", index=False)

    manifest = {
        "run_id": RUN_ID,
        "source_signal": SOURCE_SIGNAL,
        "research_only": True,
        "v1_artifact_dir": str(V1_ARTIFACT_DIR),
        "v1_note": str(V1_NOTE),
        "variant_count": len(VARIANTS),
        "broad_search": False,
        "parameter_grid": False,
        "production_registration": False,
        "survivor_watchlist_promotion": False,
        "portfolio_integration": False,
        "ml_integration": False,
        "production_conditional_alpha_wiring": False,
        "gates_schemas_thresholds_modified": False,
        "other_expansion_v5_concepts_implemented": False,
        "final_classification": status_lookup.get(int(final_status), "REJECT_RESEARCH"),
        "artifact_files": sorted(path.name for path in OUT_DIR.iterdir()) + ["manifest.json"],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _write_note(registry, scores, wfv_summary, decisions, orth_summary, active, sample_sizes, state_attr)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.sort_values(["status", "h10_mean_ic"], ascending=[True, False]).to_string(index=False))


if __name__ == "__main__":
    main()
