from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_dispersion_recovery_stability_after_stress_v1 import VOLATILITY_INVENTORY_PATH
from run_track_b_robustness_discovery_v3 import (
    baseline_panels,
    build_stress_states,
    daily_ic,
    forward_returns,
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
    _market_state_panel,
    _rebalance_interval,
)


RUN_ID = "structural_interaction_alpha_discovery_batch_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/structural_interaction_alpha_discovery_batch_v1.md")
HORIZONS = (1, 5, 10, 15, 20)

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only structural interaction alpha discovery batch. It does not modify detector code or "
    "labels, register production signals, mutate survivor/watchlist state, loosen gates or thresholds, change "
    "schemas/governance, or route anything into portfolio, ML, blending, or optimization workflows."
)


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "residual_stress_liquidity_quality_20",
        "family": "residual_stress_liquidity",
        "mechanism_thesis": "Stock-specific residual stress that is being contained while non-price liquidity quality improves may identify healthier repair.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20",
        "family": "volatility_participation_asymmetry",
        "mechanism_thesis": "Improving stock-level up/down participation balance during stabilizing volatility may capture repair without market breadth cloning.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "dispersion_resilient_relative_stability_20",
        "family": "dispersion_resilience",
        "mechanism_thesis": "Stable relative behavior during elevated dispersion may identify robust cross-sectional resilience rather than price-rank momentum.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "turnover_exhaustion_quality_repair_10_20",
        "family": "turnover_exhaustion_quality",
        "mechanism_thesis": "Turnover pressure that exhausts while range and close quality improve may separate repair from noisy reversal.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "volatility_of_volatility_stabilization_20",
        "family": "volatility_of_volatility",
        "mechanism_thesis": "Declining volatility-of-volatility after elevated instability may indicate durable stabilization beyond fast h5 shock absorption.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "compression_expansion_efficiency_asymmetry_15_30",
        "family": "compression_expansion_asymmetry",
        "mechanism_thesis": "Efficient expansion after compression, with low gap noise and low overextension, may capture quality without raw breakout chasing.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "breadth_deterioration_resilience_20",
        "family": "breadth_deterioration_resilience",
        "mechanism_thesis": "Names resilient during deteriorating breadth with stable liquidity and controlled extension may offer robust standalone behavior.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "conditional_exhaustion_vs_continuation_quality_20",
        "family": "continuation_exhaustion_quality",
        "mechanism_thesis": "Quality continuation should be separated from exhaustion by combining trend efficiency, turnover decay, and range containment.",
        "expected_horizon": "h10-h20",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame | pd.Series, denominator: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _rank01(df: pd.DataFrame) -> pd.DataFrame:
    return df.rank(axis=1, pct=True).replace([np.inf, -np.inf], np.nan)


def _neutralize_against(signal: pd.DataFrame, exposures: list[pd.DataFrame]) -> pd.DataFrame:
    out = signal.copy()
    for exposure in exposures:
        out = _rank_cs(_cs_neutralize(out, exposure))
    return _clean_panel(out)


def _finalize_signal(
    raw: pd.DataFrame,
    active_mask: pd.DataFrame,
    exposures: list[pd.DataFrame],
    rebalance: int = 10,
) -> pd.DataFrame:
    signal = _rank_cs(raw.rolling(5, min_periods=3).mean())
    signal = _neutralize_against(signal, exposures)
    signal = _rank_cs(signal * active_mask.astype(float))
    signal = _rank_cs(_rebalance_interval(signal, rebalance))
    return _clean_panel(signal)


def _active_coverage_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        active = (panel.notna().sum(axis=1) >= 25) & (panel.abs().mean(axis=1, skipna=True) > 0.02)
        rows.append(
            {
                "signal_name": name,
                "active_dates": int(active.sum()),
                "active_date_ratio": float(active.mean()),
                "activation_transitions": int(active.astype(int).diff().abs().fillna(0).sum()),
                "mean_active_coverage": float(panel[active].notna().mean(axis=1).mean()) if active.any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def build_candidate_panels(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, pd.DataFrame]], pd.DataFrame, pd.DataFrame]:
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
    ret30 = close.pct_change(30, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)

    ret5_rank = _rank_cs(ret5)
    ret10_rank = _rank_cs(ret10)
    ret20_rank = _rank_cs(ret20)
    ret60_rank = _rank_cs(ret60)
    exposures = [ret5_rank, ret20_rank, ret60_rank, _rank_cs(-ret5), _rank_cs(-ret20)]

    stress = build_stress_states(close, benchmark)
    broad_stress = stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    recent_stress = broad_stress.rolling(20, min_periods=1).max().astype(bool)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range10 = true_range.rolling(10, min_periods=7).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    close_support = close_location.rolling(5, min_periods=3).mean()
    low_extension = (1.0 - ret20_rank.sub(0.5).abs() * 2.0).clip(lower=0.0)
    low_short_extension = (1.0 - ret5_rank.sub(0.5).abs() * 2.0).clip(lower=0.0)

    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(benchmark.pct_change(5, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)
    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()
    idio_stress = _rank01(_safe_div(residual_vol20, residual_vol60))
    stress_containment = (1.0 - _rank01(_safe_div(residual_vol5, residual_vol20))).clip(lower=0.0)

    dollar_volume = close * volume
    dollar5 = dollar_volume.rolling(5, min_periods=4).mean()
    dollar20 = dollar_volume.rolling(20, min_periods=12).mean()
    dollar60 = dollar_volume.rolling(60, min_periods=40).mean()
    liquidity_quality = (
        _rank01(_safe_div(dollar20, dollar60))
        * (1.0 - _rank01(_safe_div(true_range, dollar_volume.replace(0.0, np.nan)).rolling(10, min_periods=6).mean()))
    ).clip(lower=0.0)

    up_participation10 = (ret1 > 0).rolling(10, min_periods=7).mean()
    down_range = true_range.where(ret1 < 0).rolling(20, min_periods=8).mean()
    up_range = true_range.where(ret1 > 0).rolling(20, min_periods=8).mean()
    participation_asymmetry = _rank01(up_participation10) * _rank01(_safe_div(up_range, down_range))
    volatility_stabilization = (
        (1.0 - _rank01(_safe_div(range10, range20)))
        * (1.0 - _rank01(_safe_div(residual_vol10, residual_vol20)))
    ).clip(lower=0.0)

    rank20 = ret20.rank(axis=1, pct=True)
    rank_churn20 = rank20.diff().abs().rolling(20, min_periods=12).mean()
    rank_stability = (1.0 - _rank01(rank_churn20)).clip(lower=0.0)
    idio_stability = (1.0 - _rank01(residual_vol20)).clip(lower=0.0)
    dispersion20 = ret20.std(axis=1)
    dispersion_elevated = (
        dispersion20.rolling(20, min_periods=10).max() > _rolling_quantile(dispersion20, 0.75)
    ).fillna(False)
    dispersion_gate = _market_state_panel(dispersion_elevated, close.columns)
    relative_resilience = _rank01(residual20) * low_extension

    volume_ratio20 = _safe_div(dollar20, dollar60).clip(0, 5)
    volume_ratio5 = _safe_div(dollar5, dollar20).clip(0, 5)
    turnover_pressure = _rank01(volume_ratio20)
    turnover_decay = (1.0 - _rank01(volume_ratio5)).clip(lower=0.0)
    range_repair = (1.0 - _rank01(_safe_div(range5, range20))).clip(lower=0.0)

    vol_of_vol20 = residual_vol5.rolling(20, min_periods=12).std()
    vol_of_vol60 = residual_vol5.rolling(60, min_periods=40).std()
    vov_elevated = _rank01(_safe_div(vol_of_vol20.rolling(20, min_periods=10).max(), vol_of_vol60))
    vov_decay = (1.0 - _rank01(_safe_div(vol_of_vol20, vol_of_vol60))).clip(lower=0.0)

    compression30 = (1.0 - _rank01(_safe_div(range30 := true_range.rolling(30, min_periods=20).mean(), range60))).clip(lower=0.0)
    expansion_efficiency = _rank01(_safe_div(ret15.abs(), range10.replace(0.0, np.nan)))
    close_confirmation = _rank01(np.sign(ret15) * (close_support - 0.5))
    gap_noise = (open_ / close.shift(1) - 1.0).abs().rolling(10, min_periods=6).mean()
    low_gap_noise = (1.0 - _rank01(gap_noise)).clip(lower=0.0)

    breadth20 = (ret20 > 0).mean(axis=1)
    breadth_deteriorating = (breadth20.diff(20) < -0.08).fillna(False)
    breadth_gate = _market_state_panel(breadth_deteriorating.rolling(10, min_periods=1).max().astype(bool), close.columns)
    liquidity_stability = (1.0 - _rank01(_safe_div(dollar5, dollar20).diff().abs())).clip(lower=0.0)

    trend_efficiency = _rank01(_safe_div(ret20.abs(), range20.replace(0.0, np.nan)))
    continuation_quality = _rank01(ret20) * trend_efficiency * close_support
    exhaustion_pressure = _rank01(volume_ratio20) * _rank01(_safe_div(range5, range20)) * (1.0 - close_support)
    continuation_minus_exhaustion = (continuation_quality - exhaustion_pressure).clip(lower=0.0)

    active_stress_panel = _market_state_panel(recent_stress, close.columns)
    broad_panel = pd.DataFrame(1.0, index=close.index, columns=close.columns)

    raw_components: dict[str, dict[str, pd.DataFrame]] = {
        "residual_stress_liquidity_quality_20": {
            "residual_stress": idio_stress,
            "stress_containment": stress_containment,
            "liquidity_quality": liquidity_quality,
            "low_extension": low_extension,
        },
        "volatility_participation_asymmetry_20": {
            "volatility_stabilization": volatility_stabilization,
            "participation_asymmetry": participation_asymmetry,
            "close_support": close_support,
            "low_extension": low_extension,
        },
        "dispersion_resilient_relative_stability_20": {
            "dispersion_gate": dispersion_gate,
            "rank_stability": rank_stability,
            "idio_stability": idio_stability,
            "relative_resilience": relative_resilience,
        },
        "turnover_exhaustion_quality_repair_10_20": {
            "turnover_pressure": turnover_pressure,
            "turnover_decay": turnover_decay,
            "range_repair": range_repair,
            "close_support": close_support,
            "low_short_extension": low_short_extension,
        },
        "volatility_of_volatility_stabilization_20": {
            "vov_elevated": vov_elevated,
            "vov_decay": vov_decay,
            "rank_stability": rank_stability,
            "low_extension": low_extension,
        },
        "compression_expansion_efficiency_asymmetry_15_30": {
            "compression": compression30,
            "expansion_efficiency": expansion_efficiency,
            "close_confirmation": close_confirmation,
            "low_gap_noise": low_gap_noise,
            "low_extension": low_extension,
        },
        "breadth_deterioration_resilience_20": {
            "breadth_deterioration_gate": breadth_gate,
            "relative_resilience": relative_resilience,
            "liquidity_stability": liquidity_stability,
            "low_extension": low_extension,
        },
        "conditional_exhaustion_vs_continuation_quality_20": {
            "continuation_quality": continuation_quality,
            "exhaustion_pressure_inverse": (1.0 - exhaustion_pressure).clip(lower=0.0),
            "range_repair": range_repair,
            "low_extension": low_extension,
        },
    }

    raw_scores = {
        "residual_stress_liquidity_quality_20": (
            idio_stress * stress_containment * liquidity_quality * low_extension * active_stress_panel
        ),
        "volatility_participation_asymmetry_20": (
            volatility_stabilization * participation_asymmetry * close_support * low_extension * active_stress_panel
        ),
        "dispersion_resilient_relative_stability_20": (
            rank_stability * idio_stability * relative_resilience * dispersion_gate
        ),
        "turnover_exhaustion_quality_repair_10_20": (
            turnover_pressure * turnover_decay * range_repair * close_support * low_short_extension * active_stress_panel
        ),
        "volatility_of_volatility_stabilization_20": (
            vov_elevated * vov_decay * rank_stability * low_extension * active_stress_panel
        ),
        "compression_expansion_efficiency_asymmetry_15_30": (
            compression30 * expansion_efficiency * close_confirmation * low_gap_noise * low_extension * broad_panel
        ),
        "breadth_deterioration_resilience_20": (
            relative_resilience * liquidity_stability * low_extension * breadth_gate
        ),
        "conditional_exhaustion_vs_continuation_quality_20": (
            continuation_minus_exhaustion * range_repair * low_extension * broad_panel
        ),
    }

    signals = {
        name: _finalize_signal(raw, raw.notna() & raw.gt(0), exposures, rebalance=10)
        for name, raw in raw_scores.items()
    }

    states = pd.DataFrame(index=close.index)
    states["RECENT_STRESS"] = recent_stress
    states["DISPERSION_ELEVATED"] = dispersion_elevated
    states["BREADTH_DETERIORATING"] = breadth_deteriorating
    states["VOLATILITY_SPIKE"] = stress["volatility_spike"].fillna(False)
    states["PANIC_LIQUIDITY_STRESS"] = stress["panic_liquidity_stress"].fillna(False)
    states["WEAK_BREADTH"] = stress["weak_breadth"].fillna(False)
    states["DRAWDOWN_ACCELERATION"] = stress["drawdown_acceleration"].fillna(False)
    states["HIGH_DISPERSION_ROTATION"] = stress["high_dispersion_rotation"].fillna(False)
    states["RECOVERY_PHASE"] = stress["recovery_phase"].fillna(False)
    states["BROAD_STRESS"] = broad_stress.fillna(False)

    return {k: _clean_panel(v) for k, v in signals.items()}, raw_components, states, stress


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    paths = {
        "inventory_participation_liquidity_state_shift_20_60": LIQUIDITY_INVENTORY_PATH,
        "inventory_participation_breadth_repair_under_hostile_trend": BREADTH_INVENTORY_PATH,
        "inventory_volatility_compression_after_stress_stabilization": VOLATILITY_INVENTORY_PATH,
    }
    for name, path in paths.items():
        if path.exists():
            refs[name] = pd.read_parquet(path).reindex(index=first.index, columns=first.columns)
    return refs


def state_attribution(daily_ics: pd.DataFrame, scores: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    rows = []
    for signal_name, horizon in best.items():
        series = daily_ics[
            daily_ics["signal_name"].eq(signal_name) & daily_ics["horizon"].eq(horizon)
        ].set_index("Date")["ic"]
        for state in states.columns:
            sample = series.reindex(states.index[states[state].astype(bool)]).dropna()
            std = sample.std(ddof=0) if len(sample) > 1 else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "state": state,
                    "n_dates": int(len(sample)),
                    "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                    "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def _max_corr_table(orth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in orth.groupby("signal_name"):
        group = group.dropna(subset=["abs_value_corr"])
        if group.empty:
            continue
        inventory = group[group["comparison"].str.startswith("inventory_")]
        reversal = group[group["comparison"].isin(["unweighted_reversal_20", "plain_smoothed_reversal_20"])]
        momentum = group[group["comparison"].isin(["plain_momentum_60"])]
        top = group.loc[group["abs_value_corr"].idxmax()]
        rows.append(
            {
                "signal_name": name,
                "top_comparison": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "max_inventory_corr": float(inventory["abs_value_corr"].max()) if not inventory.empty else np.nan,
                "max_reversal_corr": float(reversal["abs_value_corr"].max()) if not reversal.empty else np.nan,
                "max_momentum_corr": float(momentum["abs_value_corr"].max()) if not momentum.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def interaction_component_summary(
    signals: dict[str, pd.DataFrame],
    components: dict[str, dict[str, pd.DataFrame]],
    close: pd.DataFrame,
    scores: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    best_h = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    for signal_name, signal in signals.items():
        horizon = int(best_h.get(signal_name, 20))
        fwd = forward_returns(close, horizon)
        final_ic = daily_ic(signal, fwd).dropna().mean()
        comp_rows = []
        for component_name, component in components[signal_name].items():
            comp_panel = _rank_cs(component).reindex(index=signal.index, columns=signal.columns)
            value_corr = signal.stack().corr(comp_panel.stack())
            comp_ic = daily_ic(comp_panel, fwd).dropna().mean()
            comp_rows.append((component_name, value_corr, comp_ic))
        valid_corrs = [(name, corr, ic) for name, corr, ic in comp_rows if pd.notna(corr)]
        dominant = max(valid_corrs, key=lambda item: abs(item[1])) if valid_corrs else (None, np.nan, np.nan)
        best_comp_ic = max([item[2] for item in comp_rows if pd.notna(item[2])], default=np.nan)
        if pd.notna(dominant[1]) and abs(dominant[1]) >= 0.75:
            behavior = f"mostly_{dominant[0]}"
        elif pd.notna(best_comp_ic) and pd.notna(final_ic) and best_comp_ic >= final_ic * 1.15 and best_comp_ic > 0:
            behavior = "single_component_ic_dominates"
        elif pd.notna(final_ic) and pd.notna(best_comp_ic) and final_ic > best_comp_ic + 0.002:
            behavior = "true_interaction_behavior"
        else:
            behavior = "mixed_or_inconclusive_interaction"
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": horizon,
                "final_mean_ic": float(final_ic) if pd.notna(final_ic) else np.nan,
                "best_component_mean_ic": float(best_comp_ic) if pd.notna(best_comp_ic) else np.nan,
                "interaction_ic_lift_vs_best_component": float(final_ic - best_comp_ic)
                if pd.notna(final_ic) and pd.notna(best_comp_ic)
                else np.nan,
                "dominant_component": dominant[0],
                "dominant_component_corr": float(dominant[1]) if pd.notna(dominant[1]) else np.nan,
                "interaction_decomposition_label": behavior,
                "component_corr_detail": "; ".join(
                    f"{name}:{corr:.3f}" for name, corr, _ in comp_rows if pd.notna(corr)
                ),
                "component_ic_detail": "; ".join(
                    f"{name}:{ic:.5f}" for name, _, ic in comp_rows if pd.notna(ic)
                ),
            }
        )
    return pd.DataFrame(rows)


def fragility_concentration_summary(
    daily_ics: pd.DataFrame,
    scores: pd.DataFrame,
    stress_states: pd.DataFrame,
    wfv_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    best_h = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    crisis_mask = stress_states[
        ["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]
    ].any(axis=1)
    crisis_mask = crisis_mask.reindex(stress_states.index).fillna(False)
    for signal_name, horizon in best_h.items():
        series = daily_ics[
            daily_ics["signal_name"].eq(signal_name) & daily_ics["horizon"].eq(horizon)
        ].set_index("Date")["ic"].dropna()
        if series.empty:
            continue
        crisis = series.reindex(crisis_mask.index[crisis_mask]).dropna()
        non_crisis = series.reindex(crisis_mask.index[~crisis_mask]).dropna()
        window = wfv_summary[
            wfv_summary["signal_name"].eq(signal_name) & wfv_summary["horizon"].eq(int(horizon))
        ]
        one_window = float(window["one_window_dominance"].iloc[0]) if not window.empty else np.nan
        crisis_positive_contrib = crisis[crisis > 0].sum()
        total_positive_contrib = series[series > 0].sum()
        crisis_contrib_share = (
            float(crisis_positive_contrib / total_positive_contrib)
            if pd.notna(total_positive_contrib) and total_positive_contrib != 0
            else np.nan
        )
        stress_dependency = (
            pd.notna(crisis.mean())
            and pd.notna(non_crisis.mean())
            and crisis.mean() > 0.006
            and non_crisis.mean() <= 0
        )
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "full_mean_ic": float(series.mean()),
                "crisis_mean_ic": float(crisis.mean()) if not crisis.empty else np.nan,
                "non_crisis_mean_ic": float(non_crisis.mean()) if not non_crisis.empty else np.nan,
                "crisis_positive_ic_rate": float((crisis > 0).mean()) if not crisis.empty else np.nan,
                "non_crisis_positive_ic_rate": float((non_crisis > 0).mean()) if not non_crisis.empty else np.nan,
                "crisis_valid_dates": int(crisis.shape[0]),
                "non_crisis_valid_dates": int(non_crisis.shape[0]),
                "crisis_positive_contribution_share": crisis_contrib_share,
                "one_window_dominance": one_window,
                "stress_only_dependency_flag": bool(stress_dependency),
                "crisis_concentration_flag": bool(pd.notna(crisis_contrib_share) and crisis_contrib_share > 0.65),
                "one_window_concentration_flag": bool(pd.notna(one_window) and one_window > 0.60),
                "regime_exclusivity_flag": bool(stress_dependency or (pd.notna(crisis_contrib_share) and crisis_contrib_share > 0.75)),
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
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(interaction[["signal_name", "interaction_decomposition_label", "dominant_component", "dominant_component_corr", "interaction_ic_lift_vs_best_component"]], on="signal_name", how="left")
        .merge(fragility[["signal_name", "stress_only_dependency_flag", "crisis_concentration_flag", "one_window_concentration_flag", "regime_exclusivity_flag"]], on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.35:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.16:
            issues.append("high_turnover")
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["abs_mean_ic"] < 0.008:
            issues.append("weak_best_horizon_ic")
        if max(row.get("h10_mean_ic", np.nan), row.get("h20_mean_ic", np.nan)) < 0.008:
            issues.append("weak_medium_horizon_ic")
        if row["positive_ic_rate"] < 0.53:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.75:
            issues.append("activation_too_broad")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.35:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.35:
            issues.append("momentum_similarity_risk")
        if str(row.get("interaction_decomposition_label", "")).startswith("mostly_"):
            issues.append("single_component_dominance")
        if row.get("stress_only_dependency_flag", False):
            issues.append("stress_only_dependency")
        if row.get("crisis_concentration_flag", False):
            issues.append("crisis_concentration")
        if row.get("one_window_concentration_flag", False):
            issues.append("one_window_concentration")

        medium_ic = max(row.get("h10_mean_ic", -np.inf), row.get("h20_mean_ic", -np.inf))
        validation_ready = (
            medium_ic >= 0.018
            and row["positive_ic_rate"] >= 0.56
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and 0.10 <= row.get("active_date_ratio", 0) <= 0.60
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_reversal_corr", 1) <= 0.30
            and row.get("max_momentum_corr", 1) <= 0.30
            and not row.get("stress_only_dependency_flag", True)
            and not row.get("crisis_concentration_flag", True)
        )
        refinement_ready = (
            medium_ic >= 0.010
            and row["positive_ic_rate"] >= 0.53
            and row.get("active_date_ratio", 0) >= 0.10
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_reversal_corr", 1) <= 0.35
            and row.get("max_momentum_corr", 1) <= 0.35
            and not row.get("regime_exclusivity_flag", True)
        )
        conditional_only = (
            row.get("positive_regime_count", 0) >= 2
            and row.get("active_date_ratio", 0) >= 0.08
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
        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": _family_for(row["signal_name"]),
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h10_mean_ic": row.get("h10_mean_ic"),
                "h20_mean_ic": row.get("h20_mean_ic"),
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "one_window_dominance": row.get("one_window_dominance"),
                "positive_regime_count": row.get("positive_regime_count"),
                "best_regime_ic": row.get("best_regime_ic"),
                "interaction_decomposition_label": row.get("interaction_decomposition_label"),
                "dominant_component": row.get("dominant_component"),
                "dominant_component_corr": row.get("dominant_component_corr"),
                "stress_only_dependency_flag": row.get("stress_only_dependency_flag"),
                "crisis_concentration_flag": row.get("crisis_concentration_flag"),
                "one_window_concentration_flag": row.get("one_window_concentration_flag"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows).sort_values(["status", "h20_mean_ic"], ascending=[True, False])


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    stress_attr: pd.DataFrame,
    state_attr: pd.DataFrame,
    active: pd.DataFrame,
    interaction: pd.DataFrame,
    fragility: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    status_counts = decisions["status"].value_counts().to_dict()
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    h10 = scores[scores["horizon"].eq(10)].sort_values("mean_ic", ascending=False)
    promising = decisions[decisions["status"].isin(["CANDIDATE_FOR_CONDITIONAL_VALIDATION", "CONDITIONAL_REFINEMENT_CANDIDATE"])]
    recommendation = (
        "Run a narrow follow-up only for "
        + ", ".join(f"`{name}`" for name in promising["signal_name"])
        + "."
        if not promising.empty
        else "Do not refine immediately. Use this batch as structural evidence and return to design before another implementation wave."
    )
    lines = [
        "# Structural Interaction Alpha Discovery Batch v1",
        "",
        f"Date: 2026-05-22",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        "Status: RESEARCH_ONLY_ALPHA_DISCOVERY_BATCH",
        "",
        "## Research-Only Guardrail",
        "",
        RESEARCH_ONLY_GUARDRAIL,
        "",
        "The Transition-State Detector branch was not modified or used as a conditioning input.",
        "",
        "## Executive Takeaway",
        "",
        "This batch tested richer medium-horizon structural interaction candidates after pausing active Transition-State Detector work.",
        "",
        f"Candidates tested: `{len(registry)}`",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
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
        "## Interaction Decomposition",
        "",
        interaction.to_markdown(index=False),
        "",
        "## Anti-Fragility / Concentration Diagnostics",
        "",
        fragility.to_markdown(index=False),
        "",
        "## Orthogonality / Redundancy",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        stress_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Candidate State Attribution",
        "",
        state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Recommendation",
        "",
        recommendation,
        "",
        "Do not route any candidate into production, survivor/watchlist, validation, portfolio, ML, blending, or optimization from this batch alone.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, components, states, stress_states = build_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "RESEARCH_ONLY"

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_attr = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = _active_coverage_summary(signals)
    interaction = interaction_component_summary(signals, components, panels["close"], scores)
    fragility = fragility_concentration_summary(daily_ics, scores, stress_states, wfv_summary)
    decisions = classify_candidates(structural, scores, wfv_summary, stress_attr, orth_summary, active, interaction, fragility)

    artifact_files = [
        "candidate_metadata.csv",
        "structural_summary.csv",
        "multi_horizon_scores.csv",
        "daily_ic_by_signal_horizon.csv",
        "wfv_summary.csv",
        "wfv_windows.csv",
        "stress_attribution.csv",
        "candidate_state_attribution.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "interaction_component_summary.csv",
        "fragility_concentration_summary.csv",
        "candidate_decisions.csv",
        "market_state_flags.csv",
    ]
    registry.to_csv(OUT_DIR / artifact_files[0], index=False)
    structural.to_csv(OUT_DIR / artifact_files[1], index=False)
    scores.to_csv(OUT_DIR / artifact_files[2], index=False)
    daily_ics.to_csv(OUT_DIR / artifact_files[3], index=False)
    wfv_summary.to_csv(OUT_DIR / artifact_files[4], index=False)
    wfv_windows.to_csv(OUT_DIR / artifact_files[5], index=False)
    stress_attr.to_csv(OUT_DIR / artifact_files[6], index=False)
    state_attr.to_csv(OUT_DIR / artifact_files[7], index=False)
    orth.to_csv(OUT_DIR / artifact_files[8], index=False)
    orth_summary.to_csv(OUT_DIR / artifact_files[9], index=False)
    active.to_csv(OUT_DIR / artifact_files[10], index=False)
    interaction.to_csv(OUT_DIR / artifact_files[11], index=False)
    fragility.to_csv(OUT_DIR / artifact_files[12], index=False)
    decisions.to_csv(OUT_DIR / artifact_files[13], index=False)
    states.to_csv(OUT_DIR / artifact_files[14], index=True)
    for name, panel in signals.items():
        file_name = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / file_name)
        artifact_files.append(file_name)
    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": "RESEARCH_ONLY_ALPHA_DISCOVERY_BATCH",
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "detector_modified": False,
                "detector_used_as_conditioning_input": False,
                "production_registration_changed": False,
                "survivor_watchlist_changed": False,
                "gates_schemas_governance_changed": False,
                "portfolio_ml_blending_optimization_route_changed": False,
                "forced_survivor_promotion": False,
                "artifact_files": sorted(artifact_files),
            },
            indent=2,
            sort_keys=True,
        )
    )
    write_note(registry, structural, scores, wfv_summary, orth_summary, stress_attr, state_attr, active, interaction, fragility, decisions)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions[["signal_name", "status", "best_horizon", "mean_ic", "h10_mean_ic", "h20_mean_ic", "review_issues"]].to_string(index=False))


if __name__ == "__main__":
    main()
