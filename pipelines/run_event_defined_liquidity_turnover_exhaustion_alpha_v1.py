from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_dispersion_recovery_stability_after_stress_v1 import VOLATILITY_INVENTORY_PATH
from run_structural_interaction_alpha_discovery_batch_v1 import (
    _active_coverage_summary,
    _clean_panel,
    _finalize_signal,
    _market_state_panel,
    _max_corr_table,
    _rank01,
    _rank_cs,
    _safe_div,
    fragility_concentration_summary,
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
from run_track_b_v6_focused_discovery import BREADTH_INVENTORY_PATH, LIQUIDITY_INVENTORY_PATH


RUN_ID = "event_defined_liquidity_turnover_exhaustion_alpha_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/event_defined_liquidity_turnover_exhaustion_alpha_v1_results.md")
HORIZONS = (1, 5, 10, 15, 20)

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only event-defined liquidity/turnover exhaustion alpha batch. It does not "
    "modify detector files, fetch external metadata, register production signals, mutate survivor/"
    "watchlist state, change gates, schemas, thresholds, validation logic, or governance, and does "
    "not route anything into portfolio, ML, blending, or optimization workflows. h1/h5-led evidence "
    "is diagnostic only and cannot justify promotion from this batch."
)


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "turnover_shock_exhaustion_repair_20",
        "family": "turnover_shock_exhaustion",
        "event_trigger": "abnormal 5-day dollar-volume turnover versus 60-day baseline",
        "exhaustion_confirmation": "turnover intensity fades while range pressure repairs",
        "mechanism_thesis": "Extreme turnover events may become informative only when pressure fades and range behavior stops deteriorating.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "liquidity_vacuum_repair_after_turnover_stress_20",
        "family": "liquidity_vacuum_repair",
        "event_trigger": "high range-per-dollar-volume liquidity cost with turnover stress",
        "exhaustion_confirmation": "liquidity quality normalizes and range compresses",
        "mechanism_thesis": "Liquidity vacuum stress may be useful only after adequate liquidity returns and range behavior narrows.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "high_participation_stress_fade_quality_20",
        "family": "participation_stress_fade",
        "event_trigger": "high participation/volume during stress-like range pressure",
        "exhaustion_confirmation": "participation fades without renewed close-location disorder",
        "mechanism_thesis": "High participation stress should require fading disorder rather than active hostile-state repair cloning.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "event_volume_exhaustion_vol_stabilization_20",
        "family": "volume_exhaustion_vol_stabilization",
        "event_trigger": "abnormal volume participation event",
        "exhaustion_confirmation": "volume intensity fades and residual volatility stabilizes",
        "mechanism_thesis": "Volume events may contain information when volume intensity fades and volatility stabilizes instead of propagating.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "failed_propagation_after_liquidity_shock_20",
        "family": "failed_liquidity_propagation",
        "event_trigger": "liquidity shock with range/turnover expansion",
        "exhaustion_confirmation": "instability fails to persist over the next several observations",
        "mechanism_thesis": "The useful event may be a liquidity shock that fails to propagate into continuing instability.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "turnover_stress_recovery_efficiency_10_20",
        "family": "turnover_stress_recovery_efficiency",
        "event_trigger": "recent turnover stress event",
        "exhaustion_confirmation": "recovery per unit of volatility/range cost improves",
        "mechanism_thesis": "Some names recover more efficiently after turnover stress, with less range and volatility cost per unit of normalized liquidity.",
        "expected_horizon": "h10-h20",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _candidate_metadata() -> pd.DataFrame:
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "RESEARCH_ONLY"
    registry["framework"] = "event_defined_liquidity_turnover_exhaustion"
    return registry


def _rolling_panel_quantile(panel: pd.DataFrame, q: float, window: int = 252, min_periods: int = 100) -> pd.DataFrame:
    return panel.rolling(window, min_periods=min_periods).quantile(q).shift(1)


def _recent_event(event: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    return event.astype(float).rolling(lookback, min_periods=1).max().shift(1).fillna(0).astype(bool)


def _event_score(intensity: pd.DataFrame, confirmation: pd.DataFrame, active: pd.DataFrame) -> pd.DataFrame:
    raw = _rank01(intensity).clip(lower=0.0) * _rank01(confirmation).clip(lower=0.0)
    return raw.where(active)


def _event_counts_panel(events: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frames = []
    for name, panel in events.items():
        counts = panel.fillna(False).sum(axis=1).rename(name)
        frames.append(counts)
    return pd.concat(frames, axis=1) if frames else pd.DataFrame()


def build_candidate_panels(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[
    dict[str, pd.DataFrame],
    dict[str, dict[str, pd.DataFrame]],
    dict[str, pd.DataFrame],
    dict[str, pd.DataFrame],
    pd.DataFrame,
    pd.DataFrame,
]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    bench_ret5 = benchmark.pct_change(5, fill_method=None)
    bench_ret10 = benchmark.pct_change(10, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)

    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(bench_ret5, axis=0)
    residual10 = ret10.sub(bench_ret10, axis=0)
    residual20 = ret20.sub(bench_ret20, axis=0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range3 = true_range.rolling(3, min_periods=2).mean()
    range5 = true_range.rolling(5, min_periods=4).mean()
    range10 = true_range.rolling(10, min_periods=7).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    range_pressure = _safe_div(range5, range60).clip(0, 5)
    range_repair = (1.0 - _rank01(_safe_div(range5, range20))).clip(lower=0.0)
    range_normalization = (1.0 - _rank01(_safe_div(range10, range60))).clip(lower=0.0)

    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    close_support = close_location.rolling(5, min_periods=3).mean()
    close_disorder_repair = (1.0 - close_location.sub(0.5).abs().rolling(5, min_periods=3).mean() * 2.0).clip(lower=0.0)

    dollar_volume = close * volume
    dollar3 = dollar_volume.rolling(3, min_periods=2).mean()
    dollar5 = dollar_volume.rolling(5, min_periods=4).mean()
    dollar20 = dollar_volume.rolling(20, min_periods=12).mean()
    dollar60 = dollar_volume.rolling(60, min_periods=40).mean()
    volume_participation = _safe_div(dollar5, dollar60).clip(0, 6)
    short_volume_ratio = _safe_div(dollar3, dollar20).clip(0, 6)
    volume_decay = (1.0 - _rank01(short_volume_ratio)).clip(lower=0.0)
    turnover_decay = (1.0 - _rank01(_safe_div(dollar5, dollar20))).clip(lower=0.0)
    liquidity_cost = _safe_div(true_range.rolling(5, min_periods=4).mean(), dollar5.replace(0.0, np.nan))
    liquidity_cost_pressure = _rank01(liquidity_cost)
    liquidity_quality = (
        _rank01(_safe_div(dollar20, dollar60))
        * (1.0 - _rank01(liquidity_cost.rolling(10, min_periods=6).mean()))
    ).clip(lower=0.0)
    liquidity_quality_improvement = _rank01(liquidity_quality.diff(5).clip(lower=0.0))

    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()
    vol_stabilization = (
        (1.0 - _rank01(_safe_div(residual_vol5, residual_vol20)))
        * (1.0 - _rank01(_safe_div(residual_vol10, residual_vol60)))
    ).clip(lower=0.0)
    instability_persistence = _rank01(_safe_div(range3, range20) + _safe_div(residual_vol5, residual_vol20))
    failed_propagation_quality = (
        (1.0 - instability_persistence).clip(lower=0.0)
        * range_repair
        * vol_stabilization
    )

    recovery_efficiency = _rank01(
        _safe_div(
            close_support.diff(5).clip(lower=0.0) + residual10.clip(lower=0.0),
            range10 + residual_vol10 + liquidity_cost_pressure,
        )
    )
    low_extension20 = (1.0 - ret20.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
    low_extension5 = (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)

    turnover_spike = (
        volume_participation.gt(_rolling_panel_quantile(volume_participation, 0.80))
        & _rank01(volume_participation).gt(0.65)
    )
    volume_shock = (
        short_volume_ratio.gt(_rolling_panel_quantile(short_volume_ratio, 0.80))
        & _rank01(short_volume_ratio).gt(0.65)
    )
    range_volume_pressure = (
        _rank01(volume_participation).gt(0.60)
        & _rank01(range_pressure).gt(0.60)
    )
    liquidity_vacuum = (
        liquidity_cost.gt(_rolling_panel_quantile(liquidity_cost, 0.80))
        & _rank01(range_pressure).gt(0.60)
        & _rank01(volume_participation).gt(0.55)
    )
    participation_stress = (
        _rank01(volume_participation).gt(0.70)
        & _rank01(range_pressure).gt(0.55)
        & (ret5.rank(axis=1, pct=True).lt(0.55))
    )
    liquidity_shock = (
        (_rank01(volume_participation) + _rank01(range_pressure) + liquidity_cost_pressure).div(3).gt(0.68)
    )

    recent_turnover_spike = _recent_event(turnover_spike)
    recent_volume_shock = _recent_event(volume_shock)
    recent_range_volume_pressure = _recent_event(range_volume_pressure)
    recent_liquidity_vacuum = _recent_event(liquidity_vacuum)
    recent_participation_stress = _recent_event(participation_stress)
    recent_liquidity_shock = _recent_event(liquidity_shock)

    active_masks = {
        "turnover_shock_exhaustion_repair_20": recent_turnover_spike & turnover_decay.gt(0.55) & range_repair.gt(0.50),
        "liquidity_vacuum_repair_after_turnover_stress_20": recent_liquidity_vacuum
        & liquidity_quality_improvement.gt(0.50)
        & range_normalization.gt(0.45),
        "high_participation_stress_fade_quality_20": recent_participation_stress
        & volume_decay.gt(0.50)
        & close_disorder_repair.gt(0.45),
        "event_volume_exhaustion_vol_stabilization_20": recent_volume_shock
        & volume_decay.gt(0.50)
        & vol_stabilization.gt(0.45),
        "failed_propagation_after_liquidity_shock_20": recent_liquidity_shock
        & failed_propagation_quality.gt(0.20)
        & low_extension5.gt(0.35),
        "turnover_stress_recovery_efficiency_10_20": recent_range_volume_pressure
        & recovery_efficiency.gt(0.50)
        & turnover_decay.gt(0.45),
    }

    raw_scores = {
        "turnover_shock_exhaustion_repair_20": _event_score(
            volume_participation,
            turnover_decay * range_repair * close_support * low_extension20,
            active_masks["turnover_shock_exhaustion_repair_20"],
        ),
        "liquidity_vacuum_repair_after_turnover_stress_20": _event_score(
            liquidity_cost_pressure,
            liquidity_quality_improvement * range_normalization * close_support,
            active_masks["liquidity_vacuum_repair_after_turnover_stress_20"],
        ),
        "high_participation_stress_fade_quality_20": _event_score(
            volume_participation * range_pressure,
            volume_decay * close_disorder_repair * low_extension20,
            active_masks["high_participation_stress_fade_quality_20"],
        ),
        "event_volume_exhaustion_vol_stabilization_20": _event_score(
            short_volume_ratio,
            volume_decay * vol_stabilization * range_repair,
            active_masks["event_volume_exhaustion_vol_stabilization_20"],
        ),
        "failed_propagation_after_liquidity_shock_20": _event_score(
            (_rank01(volume_participation) + _rank01(range_pressure) + liquidity_cost_pressure) / 3.0,
            failed_propagation_quality * low_extension20,
            active_masks["failed_propagation_after_liquidity_shock_20"],
        ),
        "turnover_stress_recovery_efficiency_10_20": _event_score(
            volume_participation * range_pressure,
            recovery_efficiency * turnover_decay * liquidity_quality,
            active_masks["turnover_stress_recovery_efficiency_10_20"],
        ),
    }

    components = {
        "turnover_shock_exhaustion_repair_20": {
            "trigger": turnover_spike,
            "recent_trigger": recent_turnover_spike,
            "confirmation": turnover_decay * range_repair,
            "active_mask": active_masks["turnover_shock_exhaustion_repair_20"],
        },
        "liquidity_vacuum_repair_after_turnover_stress_20": {
            "trigger": liquidity_vacuum,
            "recent_trigger": recent_liquidity_vacuum,
            "confirmation": liquidity_quality_improvement * range_normalization,
            "active_mask": active_masks["liquidity_vacuum_repair_after_turnover_stress_20"],
        },
        "high_participation_stress_fade_quality_20": {
            "trigger": participation_stress,
            "recent_trigger": recent_participation_stress,
            "confirmation": volume_decay * close_disorder_repair,
            "active_mask": active_masks["high_participation_stress_fade_quality_20"],
        },
        "event_volume_exhaustion_vol_stabilization_20": {
            "trigger": volume_shock,
            "recent_trigger": recent_volume_shock,
            "confirmation": volume_decay * vol_stabilization,
            "active_mask": active_masks["event_volume_exhaustion_vol_stabilization_20"],
        },
        "failed_propagation_after_liquidity_shock_20": {
            "trigger": liquidity_shock,
            "recent_trigger": recent_liquidity_shock,
            "confirmation": failed_propagation_quality,
            "active_mask": active_masks["failed_propagation_after_liquidity_shock_20"],
        },
        "turnover_stress_recovery_efficiency_10_20": {
            "trigger": range_volume_pressure,
            "recent_trigger": recent_range_volume_pressure,
            "confirmation": recovery_efficiency * turnover_decay,
            "active_mask": active_masks["turnover_stress_recovery_efficiency_10_20"],
        },
    }

    exposures = [
        _rank_cs(ret5),
        _rank_cs(ret20),
        _rank_cs(ret60),
        _rank_cs(-ret5),
        _rank_cs(-ret20),
        _rank_cs(residual_vol20),
        _rank_cs(volume_participation),
        _rank_cs(liquidity_quality),
    ]
    signals = {
        name: _finalize_signal(raw, active_masks[name], exposures, rebalance=10)
        for name, raw in raw_scores.items()
    }
    for name, panel in list(signals.items()):
        if int(panel.notna().sum().sum()) == 0:
            fallback = _rank_cs(raw_scores[name].rolling(3, min_periods=1).mean())
            fallback = _rank_cs(fallback.where(active_masks[name]))
            signals[name] = _clean_panel(fallback)

    stress_states = build_stress_states(close, benchmark)
    event_counts = _event_counts_panel({name: comp["trigger"] for name, comp in components.items()})
    states = pd.DataFrame(index=close.index)
    states["ANY_EVENT_TRIGGER"] = event_counts.sum(axis=1).gt(0)
    states["TURNOVER_SPIKE_EVENT"] = turnover_spike.sum(axis=1).ge(25)
    states["LIQUIDITY_VACUUM_EVENT"] = liquidity_vacuum.sum(axis=1).ge(25)
    states["VOLUME_SHOCK_EVENT"] = volume_shock.sum(axis=1).ge(25)
    states["RANGE_VOLUME_PRESSURE_EVENT"] = range_volume_pressure.sum(axis=1).ge(25)
    states["BROAD_STRESS"] = stress_states[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)

    refs = {
        "plain_turnover_intensity": _rank_cs(volume_participation),
        "plain_turnover_decay": _rank_cs(turnover_decay),
        "plain_volume_decay": _rank_cs(volume_decay),
        "plain_liquidity_quality": _rank_cs(liquidity_quality),
        "plain_liquidity_cost_pressure": _rank_cs(liquidity_cost_pressure),
        "plain_range_repair": _rank_cs(range_repair),
        "plain_vol_stabilization": _rank_cs(vol_stabilization),
        "plain_residual_momentum_20": _rank_cs(residual20),
        "plain_residual_reversal_20": _rank_cs(-residual20),
        "plain_low_residual_volatility_20": _rank_cs(-residual_vol20),
        "plain_low_volatility_range_20": _rank_cs(-range20),
    }

    return (
        {k: _clean_panel(v) for k, v in signals.items()},
        components,
        refs,
        states.fillna(False).astype(bool),
        stress_states,
        event_counts,
    )


def event_quality_summary(components: dict[str, dict[str, pd.DataFrame]], stress_states: pd.DataFrame) -> pd.DataFrame:
    broad_stress = stress_states[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    rows = []
    for name, comp in components.items():
        trigger = comp["trigger"].fillna(False)
        recent = comp["recent_trigger"].fillna(False)
        active = comp["active_mask"].fillna(False)
        trigger_dates = trigger.sum(axis=1).gt(0)
        recent_dates = recent.sum(axis=1).gt(0)
        active_dates = active.sum(axis=1).gt(0)
        trigger_names = trigger.sum(axis=1)
        active_names = active.sum(axis=1)
        yearly_trigger = trigger_dates.groupby(trigger_dates.index.year).sum()
        yearly_active = active_dates.groupby(active_dates.index.year).sum()
        trigger_date_count = int(trigger_dates.sum())
        active_date_count = int(active_dates.sum())
        stress_active = active_dates & broad_stress.reindex(active_dates.index).fillna(False)
        rows.append(
            {
                "signal_name": name,
                "trigger_dates": trigger_date_count,
                "trigger_date_ratio": float(trigger_dates.mean()),
                "recent_trigger_dates": int(recent_dates.sum()),
                "active_dates": active_date_count,
                "active_date_ratio_event": float(active_dates.mean()),
                "mean_trigger_names": float(trigger_names[trigger_dates].mean()) if trigger_dates.any() else np.nan,
                "mean_active_names": float(active_names[active_dates].mean()) if active_dates.any() else np.nan,
                "trigger_to_active_conversion": float(active_date_count / trigger_date_count) if trigger_date_count else np.nan,
                "min_yearly_trigger_dates": int(yearly_trigger.min()) if not yearly_trigger.empty else 0,
                "min_yearly_active_dates": int(yearly_active.min()) if not yearly_active.empty else 0,
                "max_yearly_active_share": float(yearly_active.max() / max(active_date_count, 1)) if not yearly_active.empty else np.nan,
                "stress_active_share": float(stress_active.sum() / active_date_count) if active_date_count else np.nan,
                "too_sparse_event_flag": bool(active_date_count < 80 or (not yearly_active.empty and yearly_active.gt(0).sum() < 4)),
                "too_broad_event_flag": bool(active_dates.mean() > 0.55),
                "crisis_only_event_flag": bool(active_date_count > 0 and stress_active.sum() / active_date_count > 0.75),
                "one_year_event_dominance_flag": bool((not yearly_active.empty) and yearly_active.max() / max(active_date_count, 1) > 0.45),
            }
        )
    return pd.DataFrame(rows)


def event_component_summary(components: dict[str, dict[str, pd.DataFrame]]) -> pd.DataFrame:
    rows = []
    for name, comp in components.items():
        active = comp["active_mask"].fillna(False)
        confirmation = comp["confirmation"].where(active)
        trigger_intensity = comp["recent_trigger"].astype(float).where(active)
        active_points = int(active.sum().sum())
        confirmation_mean = float(confirmation.stack().mean()) if active_points else np.nan
        trigger_share = float(trigger_intensity.stack().mean()) if active_points else np.nan
        rows.append(
            {
                "signal_name": name,
                "active_points": active_points,
                "mean_confirmation_score": confirmation_mean,
                "mean_recent_trigger_flag": trigger_share,
                "event_structure_label": "event_plus_confirmation" if active_points and confirmation_mean > 0 else "insufficient_event_structure",
            }
        )
    return pd.DataFrame(rows)


def low_vol_liquidity_overlap_summary(orth: pd.DataFrame) -> pd.DataFrame:
    low_vol_refs = {"plain_low_residual_volatility_20", "plain_low_volatility_range_20", "simple_volatility_reversal"}
    liquidity_refs = {"plain_liquidity_quality", "plain_liquidity_cost_pressure", "plain_turnover_intensity", "plain_turnover_decay", "plain_volume_decay"}
    rows = []
    for name, group in orth.groupby("signal_name"):
        low_vol = group[group["comparison"].isin(low_vol_refs)]
        liquidity = group[group["comparison"].isin(liquidity_refs)]
        rows.append(
            {
                "signal_name": name,
                "max_low_vol_volcarry_corr": float(low_vol["abs_value_corr"].max()) if not low_vol.empty else np.nan,
                "hidden_low_vol_overlap_flag": bool((not low_vol.empty) and low_vol["abs_value_corr"].max() > 0.35),
                "max_liquidity_factor_corr": float(liquidity["abs_value_corr"].max()) if not liquidity.empty else np.nan,
                "liquidity_factor_duplication_flag": bool((not liquidity.empty) and liquidity["abs_value_corr"].max() > 0.45),
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
    fragility: pd.DataFrame,
    event_quality: pd.DataFrame,
    overlap: pd.DataFrame,
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
        .merge(
            fragility[
                [
                    "signal_name",
                    "stress_only_dependency_flag",
                    "crisis_concentration_flag",
                    "one_window_concentration_flag",
                    "regime_exclusivity_flag",
                ]
            ],
            on="signal_name",
            how="left",
        )
        .merge(event_quality, on="signal_name", how="left")
        .merge(overlap, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        h10_ic = row.get("h10_mean_ic", -np.inf)
        h20_ic = row.get("h20_mean_ic", -np.inf)
        medium_ic = max(h10_ic, h20_ic)
        if row.get("mean_ic", np.nan) < 0:
            issues.append("direction_mismatch")
        if row.get("best_horizon") in (1, 5):
            issues.append("short_horizon_led_diagnostic_only")
        if row.get("abs_mean_ic", 0) < 0.008:
            issues.append("weak_best_horizon_ic")
        if medium_ic < 0.008:
            issues.append("weak_medium_horizon_ic")
        if row.get("positive_ic_rate", 0) < 0.53:
            issues.append("weak_positive_ic_rate")
        if row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("one_window_dominance", 1) > 0.60:
            issues.append("one_window_dominance")
        if row.get("active_date_ratio", 0) > 0.65 or row.get("too_broad_event_flag", False):
            issues.append("broad_activation_with_weak_ic")
        if row.get("active_date_ratio", 1) < 0.05 or row.get("too_sparse_event_flag", False):
            issues.append("sparse_event_fragility")
        if row.get("crisis_only_event_flag", False) or row.get("crisis_concentration_flag", False):
            issues.append("crisis_window_concentration")
        if row.get("stress_only_dependency_flag", False):
            issues.append("stress_only_dependency")
        if row.get("one_year_event_dominance_flag", False):
            issues.append("one_year_event_dominance")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.35:
            issues.append("hidden_reversal_overlap")
        if row.get("max_momentum_corr", 0) > 0.35:
            issues.append("hidden_momentum_overlap")
        if row.get("hidden_low_vol_overlap_flag", False):
            issues.append("hidden_low_vol_volcarry_overlap")
        if row.get("liquidity_factor_duplication_flag", False):
            issues.append("liquidity_factor_duplication")

        validation_ready = (
            medium_ic >= 0.018
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_ic_rate", 0) >= 0.56
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_reversal_corr", 1) <= 0.30
            and row.get("max_momentum_corr", 1) <= 0.30
            and not row.get("hidden_low_vol_overlap_flag", True)
            and not row.get("liquidity_factor_duplication_flag", True)
            and not row.get("crisis_only_event_flag", True)
            and not row.get("too_sparse_event_flag", True)
            and not row.get("too_broad_event_flag", True)
        )
        refinement_ready = (
            medium_ic >= 0.010
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_ic_rate", 0) >= 0.53
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_reversal_corr", 1) <= 0.35
            and row.get("max_momentum_corr", 1) <= 0.35
            and not row.get("crisis_only_event_flag", True)
            and not row.get("too_sparse_event_flag", True)
            and not row.get("too_broad_event_flag", True)
        )
        conditional_only = (
            medium_ic >= 0.004
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_regime_count", 0) >= 1
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
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress_attr: pd.DataFrame,
    event_state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    event_quality: pd.DataFrame,
    event_components: pd.DataFrame,
    fragility: pd.DataFrame,
    overlap: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    status_counts = decisions["status"].value_counts().to_dict()
    h10 = scores[scores["horizon"].eq(10)].sort_values("mean_ic", ascending=False)
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    live = decisions[decisions["status"].isin(["CANDIDATE_FOR_CONDITIONAL_VALIDATION", "CONDITIONAL_REFINEMENT_CANDIDATE"])]
    if live.empty:
        recommendation = "Do not advance to validation or immediate refinement. Preserve any conditional-only names as event-defined research evidence only."
    else:
        recommendation = "Review live names one-by-one before any refinement; do not promote from this batch alone."

    lines = [
        "# Event-Defined Liquidity / Turnover Exhaustion Alpha v1 Results",
        "",
        "Date: 2026-05-23",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        "Status: RESEARCH_ONLY_ALPHA_BATCH",
        "",
        "## Research-Only Guardrail",
        "",
        RESEARCH_ONLY_GUARDRAIL,
        "",
        "## Executive Takeaway",
        "",
        "This batch tested discrete liquidity/turnover event triggers followed by exhaustion or repair confirmation. h10/h20 were the primary horizons; h1/h5 behavior was diagnostic only.",
        "",
        f"Candidates tested: `{len(registry)}`",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Event Quality",
        "",
        event_quality.to_markdown(index=False),
        "",
        "## Event Component Summary",
        "",
        event_components.to_markdown(index=False),
        "",
        "## Structural Quality And Active Coverage",
        "",
        structural.merge(active, on="signal_name", how="left")[
            [
                "signal_name",
                "missing_pct",
                "finite_pct",
                "date_coverage",
                "turnover_proxy",
                "turnover_p95",
                "active_date_ratio",
                "activation_transitions",
                "mean_active_coverage",
            ]
        ].to_markdown(index=False),
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
        wfv.to_markdown(index=False) if not wfv.empty else "WFV diagnostics unavailable.",
        "",
        "## Baseline / Inventory / Reversal / Momentum Similarity",
        "",
        orth_summary.merge(overlap, on="signal_name", how="left").to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        stress_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Event-State Attribution",
        "",
        event_state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Fragility / Concentration Summary",
        "",
        fragility.to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Recommendation",
        "",
        recommendation,
        "",
        "No candidate should be promoted, registered, added to survivor/watchlist, or routed into validation, portfolio, ML, blending, or optimization from this batch alone.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, components, event_refs, event_states, stress_states, event_counts = build_candidate_panels(panels, benchmark)
    registry = _candidate_metadata()

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_attr = stress_attribution(daily_ics, scores, stress_states)
    event_state_attr = state_attribution(daily_ics, scores, event_states)
    refs = reference_panels(signals, panels, benchmark)
    refs.update(event_refs)
    if LIQUIDITY_INVENTORY_PATH.exists():
        refs["inventory_participation_liquidity_state_shift_20_60"] = pd.read_parquet(LIQUIDITY_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    if BREADTH_INVENTORY_PATH.exists():
        refs["inventory_participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(BREADTH_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    if VOLATILITY_INVENTORY_PATH.exists():
        refs["inventory_volatility_compression_after_stress_stabilization"] = pd.read_parquet(VOLATILITY_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = _active_coverage_summary(signals)
    event_quality = event_quality_summary(components, stress_states)
    event_components = event_component_summary(components)
    fragility = fragility_concentration_summary(daily_ics, scores, stress_states, wfv_summary)
    overlap = low_vol_liquidity_overlap_summary(orth)
    decisions = classify_candidates(
        structural,
        scores,
        wfv_summary,
        stress_attr,
        orth_summary,
        active,
        fragility,
        event_quality,
        overlap,
    )

    artifact_files = [
        "candidate_metadata.csv",
        "candidate_score_summary.csv",
        "daily_ic_by_signal_horizon.csv",
        "wfv_summary.csv",
        "wfv_windows.csv",
        "active_coverage_summary.csv",
        "stress_regime_attribution.csv",
        "event_state_attribution.csv",
        "baseline_similarity_summary.csv",
        "orthogonality_redundancy_audit.csv",
        "event_quality_summary.csv",
        "event_component_summary.csv",
        "event_counts_by_date.csv",
        "event_state_flags.csv",
        "fragility_concentration_summary.csv",
        "low_vol_liquidity_overlap_summary.csv",
        "candidate_decisions.csv",
        "structural_summary.csv",
    ]
    registry.to_csv(OUT_DIR / "candidate_metadata.csv", index=False)
    scores.to_csv(OUT_DIR / "candidate_score_summary.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_windows.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    stress_attr.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    event_state_attr.to_csv(OUT_DIR / "event_state_attribution.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "baseline_similarity_summary.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    event_quality.to_csv(OUT_DIR / "event_quality_summary.csv", index=False)
    event_components.to_csv(OUT_DIR / "event_component_summary.csv", index=False)
    event_counts.to_csv(OUT_DIR / "event_counts_by_date.csv", index=True)
    event_states.to_csv(OUT_DIR / "event_state_flags.csv", index=True)
    fragility.to_csv(OUT_DIR / "fragility_concentration_summary.csv", index=False)
    overlap.to_csv(OUT_DIR / "low_vol_liquidity_overlap_summary.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decisions.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_summary.csv", index=False)

    for name, panel in signals.items():
        signal_file = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / signal_file)
        artifact_files.append(signal_file)
        comp = components[name]
        for comp_name in ["trigger", "recent_trigger", "confirmation", "active_mask"]:
            comp_file = f"{name}_{comp_name}_panel.parquet"
            panel_to_write = comp[comp_name].astype(float) if comp_name != "confirmation" else comp[comp_name]
            panel_to_write.to_parquet(OUT_DIR / comp_file)
            artifact_files.append(comp_file)

    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": "RESEARCH_ONLY_ALPHA_BATCH",
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "primary_horizons": [10, 20],
                "diagnostic_only_horizons": [1, 5],
                "detector_modified": False,
                "external_metadata_fetched": False,
                "production_registration_changed": False,
                "survivor_watchlist_changed": False,
                "gates_schemas_thresholds_validation_governance_changed": False,
                "portfolio_ml_blending_optimization_route_changed": False,
                "artifact_files": sorted(artifact_files),
            },
            indent=2,
            sort_keys=True,
        )
    )
    write_note(
        registry,
        structural,
        scores,
        wfv_summary,
        stress_attr,
        event_state_attr,
        orth_summary,
        active,
        event_quality,
        event_components,
        fragility,
        overlap,
        decisions,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions[["signal_name", "status", "best_horizon", "mean_ic", "h10_mean_ic", "h20_mean_ic", "review_issues"]].to_string(index=False))


if __name__ == "__main__":
    main()
