from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_structural_interaction_alpha_discovery_batch_v1 import (
    RESEARCH_ONLY_GUARDRAIL,
    _active_coverage_summary,
    _clean_panel,
    _finalize_signal,
    _market_state_panel,
    _max_corr_table,
    _rank01,
    _rank_cs,
    _safe_div,
    fragility_concentration_summary,
    interaction_component_summary,
    reference_panels,
    state_attribution,
)
from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
)


RUN_ID = "structural_interaction_alpha_expansion_v2"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/structural_interaction_alpha_expansion_v2.md")


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "relative_participation_quality_instability_adjusted_20",
        "family": "relative_participation_quality",
        "mechanism_thesis": "Persistent participation quality that improves relative to realized instability may capture structural repair without hard activation thresholds.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "asymmetric_stabilization_balance_20",
        "family": "asymmetric_stabilization",
        "mechanism_thesis": "Uneven downside pressure can be useful only when upside participation and range stabilization balance it rather than chase it.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "structural_recovery_efficiency_15_20",
        "family": "structural_recovery_efficiency",
        "mechanism_thesis": "Efficient recovery converts instability into close-quality improvement with less range and liquidity waste.",
        "expected_horizon": "h15-h20",
    },
    {
        "signal_name": "dispersion_constrained_recovery_quality_20",
        "family": "dispersion_constrained_recovery",
        "mechanism_thesis": "Recovery quality should be more durable when it occurs without broad speculative dispersion expansion.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "participation_persistence_quality_20",
        "family": "participation_persistence_quality",
        "mechanism_thesis": "Repeated moderate participation alignment with stable turnover may be more robust than a single intense participation event.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "volatility_structure_curvature_stabilization_20",
        "family": "volatility_structure_curvature",
        "mechanism_thesis": "A favorable short/intermediate/long volatility curve may identify stabilization shape, not merely level or spike decay.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "liquidity_adjusted_volatility_normalization_20",
        "family": "liquidity_adjusted_volatility_normalization",
        "mechanism_thesis": "Volatility normalization is more meaningful when confirmed by liquidity quality rather than raw volume intensity.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "moderate_interaction_persistence_score_20",
        "family": "interaction_persistence",
        "mechanism_thesis": "Repeated moderate alignment across stabilization, participation, and quality may outperform brittle extreme activation.",
        "expected_horizon": "h10-h20",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _zscore_ts(panel: pd.DataFrame, window: int = 60, min_periods: int = 30) -> pd.DataFrame:
    mean = panel.rolling(window, min_periods=min_periods).mean()
    std = panel.rolling(window, min_periods=min_periods).std()
    return (panel - mean) / std.replace(0.0, np.nan)


def _series_to_panel(series: pd.Series, columns: pd.Index) -> pd.DataFrame:
    return pd.DataFrame(np.repeat(series.to_numpy()[:, None], len(columns), axis=1), index=series.index, columns=columns)


def _soft_balance(*components: pd.DataFrame) -> pd.DataFrame:
    stacked = pd.concat([component.stack().rename(i) for i, component in enumerate(components)], axis=1)
    if stacked.empty:
        return components[0] * np.nan
    dispersion = stacked.std(axis=1)
    mean = stacked.mean(axis=1)
    balance = (mean - dispersion).unstack().reindex(index=components[0].index, columns=components[0].columns)
    return balance.clip(lower=0.0)


def _continuous_finalize(raw: pd.DataFrame, exposures: list[pd.DataFrame], rebalance: int = 10) -> pd.DataFrame:
    active = raw.notna() & raw.gt(0)
    return _finalize_signal(raw, active, exposures, rebalance=rebalance)


def _candidate_metadata() -> pd.DataFrame:
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "RESEARCH_ONLY"
    return registry


def build_candidate_panels(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, pd.DataFrame]], dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret15 = close.pct_change(15, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)

    ret5_rank = _rank_cs(ret5)
    ret20_rank = _rank_cs(ret20)
    ret60_rank = _rank_cs(ret60)
    exposures = [ret5_rank, ret20_rank, ret60_rank, _rank_cs(-ret5), _rank_cs(-ret20)]

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range10 = true_range.rolling(10, min_periods=7).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range40 = true_range.rolling(40, min_periods=25).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    range_normalization = (1.0 - _rank01(_safe_div(range10, range40))).clip(lower=0.0)
    range_curve = (1.0 - (_rank01(_safe_div(range5, range20)) - _rank01(_safe_div(range20, range60))).abs()).clip(lower=0.0)
    range_curvature = (range_curve * range_normalization).clip(lower=0.0)

    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    close_support = close_location.rolling(5, min_periods=3).mean()
    close_quality_persistence = close_support.rolling(10, min_periods=6).mean()
    low_extension = (1.0 - ret20_rank.sub(0.5).abs() * 2.0).clip(lower=0.0)
    low_short_extension = (1.0 - ret5_rank.sub(0.5).abs() * 2.0).clip(lower=0.0)

    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(benchmark.pct_change(5, fill_method=None), axis=0)
    residual15 = ret15.sub(benchmark.pct_change(15, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)
    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol40 = residual1.rolling(40, min_periods=25).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()
    vol_normalization = (1.0 - _rank01(_safe_div(residual_vol10, residual_vol40))).clip(lower=0.0)
    vol_curve = (1.0 - (_rank01(_safe_div(residual_vol5, residual_vol20)) - _rank01(_safe_div(residual_vol20, residual_vol60))).abs()).clip(lower=0.0)
    vol_curvature = (vol_curve * vol_normalization).clip(lower=0.0)
    instability_level = _rank01(_safe_div(residual_vol20, residual_vol60))
    instability_improvement = (1.0 - _rank01(_safe_div(residual_vol5, residual_vol20))).clip(lower=0.0)

    dollar_volume = close * volume
    dollar5 = dollar_volume.rolling(5, min_periods=4).mean()
    dollar10 = dollar_volume.rolling(10, min_periods=7).mean()
    dollar20 = dollar_volume.rolling(20, min_periods=12).mean()
    dollar60 = dollar_volume.rolling(60, min_periods=40).mean()
    dollar_quality = _rank01(_safe_div(dollar20, dollar60))
    liquidity_noise = _rank01(_safe_div(true_range, dollar_volume.replace(0.0, np.nan)).rolling(10, min_periods=6).mean())
    liquidity_quality = (dollar_quality * (1.0 - liquidity_noise)).clip(lower=0.0)
    turnover_intensity = _rank01(_safe_div(dollar5, dollar20).clip(0, 5))
    turnover_stability = (1.0 - _rank01(_safe_div(dollar5, dollar20).diff().abs())).clip(lower=0.0)
    volume_intensity_penalty = (1.0 - turnover_intensity).clip(lower=0.0)

    up_participation10 = (ret1 > 0).rolling(10, min_periods=7).mean()
    up_participation20 = (ret1 > 0).rolling(20, min_periods=12).mean()
    up_range = true_range.where(ret1 > 0).rolling(20, min_periods=8).mean()
    down_range = true_range.where(ret1 < 0).rolling(20, min_periods=8).mean()
    participation_asymmetry = (_rank01(up_participation10) * _rank01(_safe_div(up_range, down_range))).clip(lower=0.0)
    participation_persistence = up_participation10.rolling(10, min_periods=6).mean()
    participation_improvement = _rank01(up_participation10 - up_participation20.shift(5))
    participation_vs_instability = _rank01(_safe_div(participation_persistence, residual_vol10 + residual_vol20))
    participation_quality = _soft_balance(participation_asymmetry, participation_persistence, turnover_stability)

    recovery_efficiency = _rank01(_safe_div(close_support.diff(10).clip(lower=0.0), range10 + residual_vol10))
    recovery_without_extension = (recovery_efficiency * low_extension * liquidity_quality).clip(lower=0.0)
    relative_resilience = (_rank01(residual15) * low_extension).clip(lower=0.0)

    dispersion20 = ret20.std(axis=1)
    dispersion_mean = dispersion20.rolling(252, min_periods=100).mean()
    dispersion_std = dispersion20.rolling(252, min_periods=100).std()
    dispersion_z = ((dispersion20 - dispersion_mean) / dispersion_std.replace(0.0, np.nan)).clip(-3, 3)
    dispersion_rank = _series_to_panel(1.0 / (1.0 + np.exp(-dispersion_z)), close.columns)
    dispersion_stability_series = (1.0 - _rank01(dispersion20.diff(10).abs().to_frame("dispersion_churn"))["dispersion_churn"]).clip(lower=0.0)
    dispersion_stability = _series_to_panel(dispersion_stability_series, close.columns)
    dispersion_constraint = (1.0 - dispersion_rank).clip(lower=0.0)

    gap_noise = (open_ / close.shift(1) - 1.0).abs().rolling(10, min_periods=6).mean()
    low_gap_noise = (1.0 - _rank01(gap_noise)).clip(lower=0.0)
    downside_pressure = _rank01((-ret10).clip(lower=0.0) * _safe_div(range10, range40))
    upside_repair = (_rank01(ret5.clip(lower=0.0)) * close_support).clip(lower=0.0)
    asymmetric_balance = _soft_balance(downside_pressure, upside_repair, vol_normalization, low_short_extension)

    interaction_alignment = _soft_balance(vol_normalization, participation_quality, close_quality_persistence, low_extension)
    interaction_persistence = interaction_alignment.rolling(10, min_periods=6).mean()
    moderate_alignment = (1.0 - (interaction_alignment - 0.55).abs() * 2.0).clip(lower=0.0)

    raw_components: dict[str, dict[str, pd.DataFrame]] = {
        "relative_participation_quality_instability_adjusted_20": {
            "participation_vs_instability": participation_vs_instability,
            "participation_improvement": participation_improvement,
            "vol_normalization": vol_normalization,
            "turnover_stability": turnover_stability,
            "low_extension": low_extension,
        },
        "asymmetric_stabilization_balance_20": {
            "downside_pressure": downside_pressure,
            "upside_repair": upside_repair,
            "vol_normalization": vol_normalization,
            "low_short_extension": low_short_extension,
            "asymmetric_balance": asymmetric_balance,
        },
        "structural_recovery_efficiency_15_20": {
            "recovery_efficiency": recovery_efficiency,
            "close_quality_persistence": close_quality_persistence,
            "liquidity_quality": liquidity_quality,
            "range_normalization": range_normalization,
            "low_extension": low_extension,
        },
        "dispersion_constrained_recovery_quality_20": {
            "relative_resilience": relative_resilience,
            "dispersion_constraint": dispersion_constraint,
            "dispersion_stability": dispersion_stability,
            "close_quality_persistence": close_quality_persistence,
            "liquidity_quality": liquidity_quality,
        },
        "participation_persistence_quality_20": {
            "participation_quality": participation_quality,
            "participation_persistence": participation_persistence,
            "turnover_stability": turnover_stability,
            "close_quality_persistence": close_quality_persistence,
            "low_extension": low_extension,
        },
        "volatility_structure_curvature_stabilization_20": {
            "vol_curvature": vol_curvature,
            "range_curvature": range_curvature,
            "instability_improvement": instability_improvement,
            "close_quality_persistence": close_quality_persistence,
            "low_extension": low_extension,
        },
        "liquidity_adjusted_volatility_normalization_20": {
            "vol_normalization": vol_normalization,
            "liquidity_quality": liquidity_quality,
            "volume_intensity_penalty": volume_intensity_penalty,
            "turnover_stability": turnover_stability,
            "low_extension": low_extension,
        },
        "moderate_interaction_persistence_score_20": {
            "interaction_alignment": interaction_alignment,
            "interaction_persistence": interaction_persistence,
            "moderate_alignment": moderate_alignment,
            "low_gap_noise": low_gap_noise,
            "low_extension": low_extension,
        },
    }

    raw_scores = {
        "relative_participation_quality_instability_adjusted_20": _soft_balance(
            participation_vs_instability,
            participation_improvement,
            vol_normalization,
            turnover_stability,
            low_extension,
        ),
        "asymmetric_stabilization_balance_20": asymmetric_balance * close_quality_persistence,
        "structural_recovery_efficiency_15_20": _soft_balance(
            recovery_without_extension,
            close_quality_persistence,
            liquidity_quality,
            range_normalization,
        ),
        "dispersion_constrained_recovery_quality_20": _soft_balance(
            relative_resilience,
            dispersion_constraint,
            dispersion_stability,
            close_quality_persistence,
            liquidity_quality,
        ),
        "participation_persistence_quality_20": _soft_balance(
            participation_quality,
            participation_persistence,
            turnover_stability,
            close_quality_persistence,
            low_extension,
        ),
        "volatility_structure_curvature_stabilization_20": _soft_balance(
            vol_curvature,
            range_curvature,
            instability_improvement,
            close_quality_persistence,
            low_extension,
        ),
        "liquidity_adjusted_volatility_normalization_20": _soft_balance(
            vol_normalization,
            liquidity_quality,
            volume_intensity_penalty,
            turnover_stability,
            low_extension,
        ),
        "moderate_interaction_persistence_score_20": _soft_balance(
            interaction_persistence,
            moderate_alignment,
            low_gap_noise,
            low_extension,
        ),
    }

    signals = {
        name: _continuous_finalize(raw, exposures, rebalance=10)
        for name, raw in raw_scores.items()
    }

    stress = build_stress_states(close, benchmark)
    broad_stress = stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    states = pd.DataFrame(index=close.index)
    states["RECENT_STRESS"] = broad_stress.rolling(20, min_periods=1).max().fillna(False).astype(bool)
    states["VOLATILITY_SPIKE"] = stress["volatility_spike"].fillna(False)
    states["PANIC_LIQUIDITY_STRESS"] = stress["panic_liquidity_stress"].fillna(False)
    states["WEAK_BREADTH"] = stress["weak_breadth"].fillna(False)
    states["DRAWDOWN_ACCELERATION"] = stress["drawdown_acceleration"].fillna(False)
    states["HIGH_DISPERSION_ROTATION"] = stress["high_dispersion_rotation"].fillna(False)
    states["RECOVERY_PHASE"] = stress["recovery_phase"].fillna(False)
    states["BROAD_STRESS"] = broad_stress.fillna(False)
    states["LOW_DISPERSION"] = (dispersion20 < dispersion20.rolling(252, min_periods=100).quantile(0.35)).fillna(False)

    return {k: _clean_panel(v) for k, v in signals.items()}, raw_components, raw_scores, states, stress


def interaction_persistence_summary(
    raw_scores: dict[str, pd.DataFrame],
    signals: dict[str, pd.DataFrame],
    scores: pd.DataFrame,
    close: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    best_h = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    for name, raw in raw_scores.items():
        raw_rank = _rank_cs(raw)
        persistence = raw_rank.rolling(10, min_periods=6).mean()
        persistence_ratio = (persistence > 0.55).mean(axis=1)
        persistence_stability = persistence_ratio.rolling(20, min_periods=10).std()
        horizon = int(best_h.get(name, 20))
        fwd = forward_returns(close, horizon)
        raw_ic = daily_ic(raw_rank, fwd).dropna().mean()
        persistent_ic = daily_ic(_rank_cs(persistence), fwd).dropna().mean()
        rows.append(
            {
                "signal_name": name,
                "horizon": horizon,
                "raw_mean_ic": float(raw_ic) if pd.notna(raw_ic) else np.nan,
                "persistent_mean_ic": float(persistent_ic) if pd.notna(persistent_ic) else np.nan,
                "persistence_ic_delta": float(persistent_ic - raw_ic) if pd.notna(raw_ic) and pd.notna(persistent_ic) else np.nan,
                "mean_persistent_coverage": float(persistence_ratio.mean()),
                "p95_persistent_coverage": float(persistence_ratio.quantile(0.95)),
                "persistence_coverage_stability": float(persistence_stability.mean()),
                "interaction_persistence_label": "persistent_structure_supported"
                if pd.notna(persistent_ic) and pd.notna(raw_ic) and persistent_ic >= raw_ic - 0.001
                else "persistence_weakens_structure",
            }
        )
    return pd.DataFrame(rows)


def smoothness_activation_brittleness_summary(
    raw_scores: dict[str, pd.DataFrame],
    signals: dict[str, pd.DataFrame],
    scores: pd.DataFrame,
    close: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    best_h = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    for name, raw in raw_scores.items():
        horizon = int(best_h.get(name, 20))
        fwd = forward_returns(close, horizon)
        raw_rank = _rank_cs(raw)
        continuous_ic = daily_ic(raw_rank, fwd).dropna().mean()
        focused_raw = raw.where(raw.rank(axis=1, pct=True) >= 0.50)
        focused_signal = _rank_cs(focused_raw)
        focused_ic = daily_ic(focused_signal, fwd).dropna().mean()
        raw_daily_coverage = raw.notna().mean(axis=1)
        focused_daily_coverage = focused_raw.notna().mean(axis=1)
        abruptness = raw_rank.diff().abs().mean(axis=1).mean()
        rows.append(
            {
                "signal_name": name,
                "horizon": horizon,
                "continuous_raw_ic": float(continuous_ic) if pd.notna(continuous_ic) else np.nan,
                "focused_subset_ic": float(focused_ic) if pd.notna(focused_ic) else np.nan,
                "subset_ic_delta_vs_continuous": float(focused_ic - continuous_ic)
                if pd.notna(focused_ic) and pd.notna(continuous_ic)
                else np.nan,
                "mean_raw_daily_coverage": float(raw_daily_coverage.mean()),
                "mean_focused_daily_coverage": float(focused_daily_coverage.mean()),
                "mean_signal_abruptness": float(abruptness) if pd.notna(abruptness) else np.nan,
                "smoothness_brittleness_label": "subset_collapse_risk"
                if pd.notna(focused_ic) and pd.notna(continuous_ic) and focused_ic < continuous_ic - 0.004
                else "continuous_behavior_stable",
            }
        )
    return pd.DataFrame(rows)


def component_balance_summary(components: dict[str, dict[str, pd.DataFrame]]) -> pd.DataFrame:
    rows = []
    for name, comp_map in components.items():
        comp_panels = [_rank_cs(panel) for panel in comp_map.values()]
        stacked = pd.concat([panel.stack().rename(comp_name) for comp_name, panel in zip(comp_map, comp_panels)], axis=1)
        means = stacked.mean(axis=0).replace(0, np.nan)
        stds = stacked.std(axis=0)
        mean_abs_corr = stacked.corr().where(~np.eye(len(stacked.columns), dtype=bool)).abs().stack().mean()
        dominance_ratio = float((means.max() / means.min())) if means.min() and pd.notna(means.min()) else np.nan
        coeff_var = float((stds / means.abs()).replace([np.inf, -np.inf], np.nan).mean())
        label = "balanced_interaction"
        if pd.notna(dominance_ratio) and dominance_ratio > 2.5:
            label = "component_level_imbalance"
        elif pd.notna(mean_abs_corr) and mean_abs_corr > 0.70:
            label = "components_too_collinear"
        rows.append(
            {
                "signal_name": name,
                "component_count": len(comp_map),
                "component_mean_dominance_ratio": dominance_ratio,
                "component_mean_abs_corr": float(mean_abs_corr) if pd.notna(mean_abs_corr) else np.nan,
                "component_cv_mean": coeff_var,
                "component_balance_label": label,
            }
        )
    return pd.DataFrame(rows)


def classify_candidates(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    interaction: pd.DataFrame,
    fragility: pd.DataFrame,
    persistence: pd.DataFrame,
    smoothness: pd.DataFrame,
    balance: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    stress_counts = (
        stress_attr.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, left_on=["signal_name", "best_horizon"], right_on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(interaction[["signal_name", "interaction_decomposition_label", "dominant_component", "dominant_component_corr", "interaction_ic_lift_vs_best_component"]], on="signal_name", how="left")
        .merge(fragility[["signal_name", "stress_only_dependency_flag", "crisis_concentration_flag", "one_window_concentration_flag", "regime_exclusivity_flag"]], on="signal_name", how="left")
        .merge(persistence[["signal_name", "persistence_ic_delta", "interaction_persistence_label"]], on="signal_name", how="left")
        .merge(smoothness[["signal_name", "subset_ic_delta_vs_continuous", "smoothness_brittleness_label", "mean_signal_abruptness"]], on="signal_name", how="left")
        .merge(balance[["signal_name", "component_balance_label", "component_mean_dominance_ratio", "component_mean_abs_corr"]], on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["best_horizon"] in (1, 5):
            issues.append("short_horizon_led")
        if row["abs_mean_ic"] < 0.008:
            issues.append("weak_best_horizon_ic")
        if max(row.get("h10_mean_ic", np.nan), row.get("h20_mean_ic", np.nan)) < 0.008:
            issues.append("weak_medium_horizon_ic")
        if row["positive_ic_rate"] < 0.53:
            issues.append("weak_positive_ic_rate")
        if row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("one_window_dominance", 1) > 0.60:
            issues.append("one_window_concentration")
        if row.get("active_date_ratio", 0) > 0.80:
            issues.append("activation_too_broad")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")
        if row.get("max_inventory_corr", 0) > 0.30:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.30:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.30:
            issues.append("momentum_similarity_risk")
        if row.get("interaction_decomposition_label") != "true_interaction_behavior":
            issues.append("interaction_not_preserved")
        if row.get("interaction_persistence_label") != "persistent_structure_supported":
            issues.append("interaction_persistence_weak")
        if row.get("smoothness_brittleness_label") == "subset_collapse_risk":
            issues.append("subset_collapse_risk")
        if row.get("component_balance_label") != "balanced_interaction":
            issues.append(str(row.get("component_balance_label")))
        if row.get("stress_only_dependency_flag", False):
            issues.append("stress_only_dependency")
        if row.get("crisis_concentration_flag", False):
            issues.append("crisis_concentration")
        if row.get("one_window_concentration_flag", False):
            issues.append("one_window_concentration_flag")

        medium_ic = max(row.get("h10_mean_ic", -np.inf), row.get("h20_mean_ic", -np.inf))
        validation_ready = (
            medium_ic >= 0.018
            and row["best_horizon"] in (10, 15, 20)
            and row["positive_ic_rate"] >= 0.56
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and row.get("interaction_decomposition_label") == "true_interaction_behavior"
            and row.get("interaction_persistence_label") == "persistent_structure_supported"
            and row.get("smoothness_brittleness_label") != "subset_collapse_risk"
            and row.get("component_balance_label") == "balanced_interaction"
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_reversal_corr", 1) <= 0.30
            and row.get("max_momentum_corr", 1) <= 0.30
            and not row.get("stress_only_dependency_flag", True)
            and not row.get("crisis_concentration_flag", True)
        )
        refinement_ready = (
            medium_ic >= 0.010
            and row["best_horizon"] in (10, 15, 20)
            and row["positive_ic_rate"] >= 0.53
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("interaction_decomposition_label") == "true_interaction_behavior"
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_reversal_corr", 1) <= 0.35
            and row.get("max_momentum_corr", 1) <= 0.35
            and not row.get("crisis_concentration_flag", True)
        )
        conditional_only = (
            medium_ic >= 0.004
            and row["best_horizon"] in (10, 15, 20)
            and row.get("max_inventory_corr", 1) <= 0.45
        )
        if validation_ready:
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif refinement_ready:
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif conditional_only:
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"
        out = row.to_dict()
        out["status"] = status
        out["review_issues"] = "; ".join(dict.fromkeys(issues)) if issues else "none"
        rows.append(out)
    return pd.DataFrame(rows).sort_values(["status", "h20_mean_ic"], ascending=[True, False])


def write_note(
    registry: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    interaction: pd.DataFrame,
    persistence: pd.DataFrame,
    smoothness: pd.DataFrame,
    balance: pd.DataFrame,
    fragility: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    status_counts = decisions["status"].value_counts().to_dict()
    h10 = scores[scores["horizon"].eq(10)].sort_values("mean_ic", ascending=False)
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    promising = decisions[decisions["status"].isin(["CANDIDATE_FOR_CONDITIONAL_VALIDATION", "CONDITIONAL_REFINEMENT_CANDIDATE"])]
    if promising.empty:
        recommendation = "Do not advance to validation. Preserve the evidence and review whether a narrower design thesis is warranted."
    else:
        recommendation = "Keep promising candidates as research leads only; require one-by-one refinement or validation planning before any status change."
    lines = [
        "# Structural Interaction Alpha Expansion v2",
        "",
        "Date: 2026-05-22",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        "Status: RESEARCH_ONLY_ALPHA_EXPANSION",
        "",
        "## Research-Only Guardrail",
        "",
        RESEARCH_ONLY_GUARDRAIL,
        "",
        "The Transition-State Detector branch was not modified and detector states were not used as inputs.",
        "",
        "## Objective",
        "",
        "Test whether smoother, less brittle structural interaction formulations can capture medium-horizon behavior better than hard-threshold activation signals.",
        "",
        "## Executive Takeaway",
        "",
        f"Candidates tested: `{len(registry)}`",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h10 Ranking",
        "",
        h10[["signal_name", "mean_ic", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## h20 Ranking",
        "",
        h20[["signal_name", "mean_ic", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False),
        "",
        "## Active Coverage",
        "",
        active.to_markdown(index=False),
        "",
        "## Interaction Component Decomposition",
        "",
        interaction.to_markdown(index=False),
        "",
        "## Interaction Persistence",
        "",
        persistence.to_markdown(index=False),
        "",
        "## Smoothness / Activation Brittleness",
        "",
        smoothness.to_markdown(index=False),
        "",
        "## Component Balance",
        "",
        balance.to_markdown(index=False),
        "",
        "## Fragility / Concentration",
        "",
        fragility.to_markdown(index=False),
        "",
        "## Similarity / Redundancy",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions[[
            "signal_name",
            "status",
            "best_horizon",
            "mean_ic",
            "h10_mean_ic",
            "h20_mean_ic",
            "positive_ic_rate",
            "max_inventory_corr",
            "max_reversal_corr",
            "max_momentum_corr",
            "interaction_decomposition_label",
            "interaction_persistence_label",
            "smoothness_brittleness_label",
            "component_balance_label",
            "review_issues",
        ]].to_markdown(index=False),
        "",
        "## Recommendation",
        "",
        recommendation,
        "",
        "No production registration, survivor/watchlist mutation, detector modification, schema/gate/governance change, or portfolio/ML/blending/optimization route was made.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    close = panels["close"]
    signals, components, raw_scores, states, stress = build_candidate_panels(panels, benchmark)
    registry = _candidate_metadata()

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, close)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_attr = stress_attribution(daily_ics, scores, stress)
    state_attr = state_attribution(daily_ics, scores, states)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = _active_coverage_summary(signals)
    interaction = interaction_component_summary(signals, components, close, scores)
    fragility = fragility_concentration_summary(daily_ics, scores, stress, wfv_summary)
    persistence = interaction_persistence_summary(raw_scores, signals, scores, close)
    smoothness = smoothness_activation_brittleness_summary(raw_scores, signals, scores, close)
    balance = component_balance_summary(components)
    decisions = classify_candidates(
        structural,
        scores,
        wfv_summary,
        stress_attr,
        orth_summary,
        active,
        interaction,
        fragility,
        persistence,
        smoothness,
        balance,
    )

    files = [
        ("candidate_metadata.csv", registry),
        ("structural_summary.csv", structural),
        ("multi_horizon_scores.csv", scores),
        ("daily_ic_by_signal_horizon.csv", daily_ics),
        ("wfv_summary.csv", wfv_summary),
        ("wfv_windows.csv", wfv_windows),
        ("stress_attribution.csv", stress_attr),
        ("candidate_state_attribution.csv", state_attr),
        ("orthogonality_redundancy_audit.csv", orth),
        ("orthogonality_summary.csv", orth_summary),
        ("active_coverage_summary.csv", active),
        ("interaction_component_summary.csv", interaction),
        ("interaction_persistence_summary.csv", persistence),
        ("smoothness_activation_brittleness_summary.csv", smoothness),
        ("component_balance_summary.csv", balance),
        ("fragility_concentration_summary.csv", fragility),
        ("candidate_decisions.csv", decisions),
        ("market_state_flags.csv", states),
    ]
    artifact_files = []
    for name, frame in files:
        frame.to_csv(OUT_DIR / name, index=name == "market_state_flags.csv")
        artifact_files.append(name)
    for name, panel in signals.items():
        file_name = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / file_name)
        artifact_files.append(file_name)
    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": "RESEARCH_ONLY_ALPHA_EXPANSION",
                "candidate_count": len(signals),
                "candidate_names": list(signals),
                "artifact_files": sorted(artifact_files),
                "detector_modified": False,
                "detector_used_as_input": False,
                "production_registration_changed": False,
                "survivor_watchlist_changed": False,
                "gates_schemas_governance_changed": False,
                "portfolio_ml_blending_optimization_route_changed": False,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_note(
        registry,
        scores,
        wfv_summary,
        orth_summary,
        active,
        interaction,
        persistence,
        smoothness,
        balance,
        fragility,
        decisions,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions[["signal_name", "status", "best_horizon", "mean_ic", "h10_mean_ic", "h20_mean_ic", "review_issues"]].to_string(index=False))


if __name__ == "__main__":
    main()
