from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
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
    active_coverage_summary,
    state_attribution,
    _market_state_panel,
    _rebalance_interval,
)
from run_short_horizon_volatility_shock_absorption_10_v1 import (
    _safe_div,
    reference_panels,
    volatility_shock_corr_summary,
)


RUN_ID = "transition_state_alpha_discovery_batch"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/transition_state_alpha_discovery_batch.md")
SOURCE_NOTES = [
    Path("docs/research_notes/track_b_expansion_v5_mini_closeout_review.md"),
    Path("docs/research_notes/short_horizon_volatility_shock_absorption_10_refinement.md"),
    Path("docs/research_notes/conditional_alpha_inventory_monitoring_v2.md"),
    Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md"),
]

RESEARCH_ONLY_GUARDRAIL = (
    "This batch may identify promising transition-state candidates, but no candidate from this run should be "
    "promoted, registered, added to survivor/watchlist, or routed into portfolio/ML/blending logic from this "
    "batch alone. Strong candidates should only be labeled for future conditional validation or refinement."
)


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "volatility_spike_decay_absorption_5_10",
        "family": "shock_absorption",
        "mechanism_thesis": "Recent volatility spikes that decay quickly may identify absorbed stress rather than propagating instability.",
        "transition_logic": "Recent market/range volatility shock with fast residual-volatility and range decay.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "range_expansion_to_containment_5_10",
        "family": "shock_absorption",
        "mechanism_thesis": "Range expansion followed by contained near-term range behavior may identify stabilization after disorder.",
        "transition_logic": "Elevated 20-day range context with 5-day range containment and non-extreme price path.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "shock_return_normalization_5_10",
        "family": "shock_absorption",
        "mechanism_thesis": "Large short-horizon residual shocks that normalize without reversal or chase may precede stabilization.",
        "transition_logic": "Recent residual shock with lower follow-through magnitude and neutralized return-rank exposure.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "liquidity_recovery_after_vol_shock_5_10",
        "family": "liquidity_recovery",
        "mechanism_thesis": "Liquidity recovery after volatility shock may mark stress absorption instead of fragile dislocation.",
        "transition_logic": "Recent volatility shock with improving dollar-volume support and falling price-impact pressure.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "volume_shock_exhaustion_stabilization_5_10",
        "family": "liquidity_recovery",
        "mechanism_thesis": "Volume shocks that exhaust while price/range disorder stabilizes may indicate absorbed flow stress.",
        "transition_logic": "Elevated recent volume shock, declining volume pressure, contained range, and non-extreme returns.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "participation_repair_after_instability_5_10",
        "family": "liquidity_recovery",
        "mechanism_thesis": "Participation repair after instability may reveal local stabilization without cloning weak-breadth repair.",
        "transition_logic": "Recent stress with improving stock-level up-day participation and controlled extension.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "dispersion_spike_normalization_5_10",
        "family": "dispersion_breadth_normalization",
        "mechanism_thesis": "Cross-sectional dispersion spikes that normalize may identify contained market-wide instability.",
        "transition_logic": "Recent elevated dispersion with current dispersion decline and stable stock-level residual behavior.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "breadth_stabilization_after_panic_diffusion_5_10",
        "family": "dispersion_breadth_normalization",
        "mechanism_thesis": "Panic diffusion that stops broadening and shows breadth stabilization may precede short-horizon repair.",
        "transition_logic": "Recent weak breadth or panic state with breadth stabilization and stock-level close support.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "shock_absorption_vs_propagation_quality_5_10",
        "family": "propagation_vs_absorption",
        "mechanism_thesis": "Explicit separation of absorbed shocks from cascading shocks may identify healthier transition states.",
        "transition_logic": "Positive absorption quality minus propagation pressure during recent shock windows.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
    {
        "signal_name": "instability_resolution_to_stabilization_5_10",
        "family": "propagation_vs_absorption",
        "mechanism_thesis": "Short-horizon instability that resolves into rank and residual-volatility stability may carry into h10 stabilization.",
        "transition_logic": "Recent instability with falling rank churn, falling residual volatility, and close-location support.",
        "expected_horizon": "h5-to-h10",
        "expected_active_coverage": "medium",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _rank01(df: pd.DataFrame) -> pd.DataFrame:
    return df.rank(axis=1, pct=True).replace([np.inf, -np.inf], np.nan)


def _neutralize_basic(signal: pd.DataFrame, exposures: list[pd.DataFrame]) -> pd.DataFrame:
    out = signal.copy()
    for exposure in exposures:
        out = _rank_cs(_cs_neutralize(out, exposure))
    return _clean_panel(out)


def _state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    absorption_quality: pd.DataFrame,
    propagation_pressure: pd.DataFrame,
) -> pd.DataFrame:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    bench_vol5 = bench_ret1.rolling(5, min_periods=4).std()
    bench_vol20 = bench_ret1.rolling(20, min_periods=12).std()
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    avg_range5 = true_range.rolling(5, min_periods=4).mean().mean(axis=1)
    avg_range20 = true_range.rolling(20, min_periods=12).mean().mean(axis=1)
    dollar_volume = close * volume
    market_liquidity = dollar_volume.sum(axis=1, min_count=25)
    liquidity20 = market_liquidity.rolling(20, min_periods=12).mean()
    liquidity60 = market_liquidity.rolling(60, min_periods=40).mean()
    breadth5 = (ret5 > 0).mean(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    dispersion20 = ret20.std(axis=1)
    stress = build_stress_states(close, benchmark)

    vol_shock = (
        stress["volatility_spike"].fillna(False)
        | (bench_vol5 > _rolling_quantile(bench_vol5, 0.80))
        | (avg_range5 > _rolling_quantile(avg_range5, 0.80))
    ).fillna(False)
    recent_shock = vol_shock.rolling(10, min_periods=1).max().astype(bool)
    shock_absorbing = (
        recent_shock
        & (bench_vol5 <= bench_vol20 * 1.15)
        & (avg_range5 <= avg_range20 * 1.10)
        & (absorption_quality.mean(axis=1, skipna=True) > absorption_quality.stack().median())
    ).fillna(False)
    shock_propagating = (
        recent_shock
        & (
            (bench_vol5 > bench_vol20 * 1.25)
            | (avg_range5 > avg_range20 * 1.25)
            | (propagation_pressure.mean(axis=1, skipna=True) > propagation_pressure.stack().median())
        )
    ).fillna(False)
    liquidity_recovering = (
        recent_shock
        & (liquidity20 > liquidity60)
        & (liquidity20.pct_change(5, fill_method=None) > 0)
    ).fillna(False)
    dispersion_spike = (dispersion20 > _rolling_quantile(dispersion20, 0.75)).fillna(False)
    dispersion_normalizing = (
        dispersion_spike.rolling(20, min_periods=1).max().astype(bool)
        & (dispersion20.diff(10) < 0)
        & (dispersion20 < dispersion20.rolling(60, min_periods=40).mean() * 1.10)
    ).fillna(False)
    breadth_stabilizing = (
        (stress["weak_breadth"].fillna(False).rolling(20, min_periods=1).max().astype(bool) | recent_shock)
        & (breadth5 >= breadth20)
        & (breadth20.diff(10) >= -0.02)
    ).fillna(False)
    broad_hostile = (
        recent_shock
        | stress["weak_breadth"].fillna(False)
        | ((benchmark < bench_ma60) & (bench_ret20 < 0))
    ).fillna(False)
    instability_resolving = (
        recent_shock
        & shock_absorbing
        & ~shock_propagating
        & (breadth_stabilizing | dispersion_normalizing | liquidity_recovering)
    ).fillna(False)

    states = pd.DataFrame(index=close.index)
    states["RECENT_SHOCK"] = recent_shock
    states["SHOCK_ABSORBING"] = shock_absorbing
    states["SHOCK_PROPAGATING"] = shock_propagating
    states["LIQUIDITY_RECOVERING_AFTER_SHOCK"] = liquidity_recovering
    states["DISPERSION_NORMALIZING_AFTER_SHOCK"] = dispersion_normalizing
    states["BREADTH_STABILIZING_AFTER_PANIC"] = breadth_stabilizing
    states["INSTABILITY_RESOLVING"] = instability_resolving
    states["ACTIVE_HOSTILE_OR_STRESS"] = broad_hostile
    states["HOSTILE_OR_STRESS"] = broad_hostile
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_candidate_panels(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    dollar_volume = close * volume

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(benchmark.pct_change(5, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range10 = true_range.rolling(10, min_periods=7).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()
    dollar_vol5 = dollar_volume.rolling(5, min_periods=4).mean()
    dollar_vol20 = dollar_volume.rolling(20, min_periods=12).mean()
    dollar_vol60 = dollar_volume.rolling(60, min_periods=40).mean()

    shock_present = (
        _rank01(_safe_div(range20, range60)) * _rank01(_safe_div(residual_vol20, residual_vol60))
    ).clip(lower=0.0)
    vol_decay = (
        (1.0 - _rank01(_safe_div(residual_vol5, residual_vol20)))
        * (1.0 - _rank01(_safe_div(range5, range20)))
    ).clip(lower=0.0)
    range_containment = (
        (1.0 - _rank01(_safe_div(range5, range20)))
        * (1.0 - _rank01(_safe_div(range10, range20)))
    ).clip(lower=0.0)
    return_normalization = (
        (1.0 - _rank01(residual5.abs()))
        * (1.0 - _rank01(residual10.abs()))
        * _rank01(residual20.abs())
    ).clip(lower=0.0)
    rank_churn = residual10.rank(axis=1, pct=True).diff().abs().rolling(10, min_periods=6).mean()
    rank_stability = (1.0 - _rank01(rank_churn)).clip(lower=0.0)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    close_support = close_location.rolling(5, min_periods=3).mean().rank(axis=1, pct=True)
    no_extension = (
        (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
        * (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
    ).clip(lower=0.0)
    liquidity_support = dollar_vol10 = dollar_volume.rolling(10, min_periods=7).mean()
    liquidity_recovery = (
        _rank01(_safe_div(dollar_vol5, dollar_vol20))
        * _rank01(_safe_div(dollar_vol20, dollar_vol60))
        * (1.0 - _rank01(_safe_div(true_range, dollar_volume.replace(0.0, np.nan)).rolling(5, min_periods=4).mean()))
    ).clip(lower=0.0)
    volume_ratio5 = _safe_div(dollar_vol5, dollar_vol20).clip(0, 5)
    volume_ratio20 = _safe_div(dollar_vol20, dollar_vol60).clip(0, 5)
    volume_exhaustion = (
        _rank01(volume_ratio20)
        * (1.0 - _rank01(volume_ratio5))
        * range_containment
    ).clip(lower=0.0)
    up_participation5 = (ret1 > 0).rolling(5, min_periods=4).mean()
    up_participation20 = (ret1 > 0).rolling(20, min_periods=12).mean()
    participation_repair = (
        _rank01(up_participation5 - up_participation20)
        * rank_stability
        * no_extension
    ).clip(lower=0.0)
    dispersion20 = ret20.std(axis=1)
    dispersion_gate_series = (
        (dispersion20.rolling(20, min_periods=10).max() > _rolling_quantile(dispersion20, 0.75))
        & (dispersion20.diff(10) < 0)
    ).fillna(False)
    idio_stability = (1.0 - _rank01(residual_vol10)).clip(lower=0.0)
    dispersion_normalization_quality = (
        rank_stability * idio_stability * no_extension
    ).clip(lower=0.0)
    breadth5 = (ret5 > 0).mean(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    breadth_stability_series = ((breadth5 >= breadth20) & (breadth20.diff(10) >= -0.02)).fillna(False)
    breadth_stability_quality = (
        close_support * rank_stability * no_extension
    ).clip(lower=0.0)
    propagation_pressure = (
        _rank01(_safe_div(residual_vol5, residual_vol20))
        * _rank01(_safe_div(range5, range20))
        * _rank01(rank_churn)
        * _rank01(residual5.abs())
    ).clip(lower=0.0)
    absorption_quality = (
        shock_present
        * vol_decay
        * range_containment
        * return_normalization.fillna(0.5)
        * rank_stability
        * close_support
        * no_extension
        * _rank01(liquidity_support)
    ).rolling(5, min_periods=3).mean()

    states = _state_flags(panels, benchmark, absorption_quality, propagation_pressure)
    gates = {
        "recent_shock": _market_state_panel(states["RECENT_SHOCK"], close.columns),
        "shock_absorbing": _market_state_panel(states["SHOCK_ABSORBING"], close.columns),
        "liquidity": _market_state_panel(states["LIQUIDITY_RECOVERING_AFTER_SHOCK"], close.columns),
        "dispersion": _market_state_panel(states["DISPERSION_NORMALIZING_AFTER_SHOCK"] | dispersion_gate_series, close.columns),
        "breadth": _market_state_panel(states["BREADTH_STABILIZING_AFTER_PANIC"] | breadth_stability_series, close.columns),
        "instability": _market_state_panel(states["INSTABILITY_RESOLVING"], close.columns),
    }
    exposures = [_rank_cs(ret5), _rank_cs(ret10), _rank_cs(ret20), _rank_cs(ret60), _rank_cs(-ret5), _rank_cs(-ret20)]

    raw_signals = {
        "volatility_spike_decay_absorption_5_10": shock_present * vol_decay * rank_stability * close_support * gates["shock_absorbing"],
        "range_expansion_to_containment_5_10": shock_present * range_containment * close_support * no_extension * gates["recent_shock"],
        "shock_return_normalization_5_10": shock_present * return_normalization * rank_stability * gates["recent_shock"],
        "liquidity_recovery_after_vol_shock_5_10": shock_present * liquidity_recovery * range_containment * gates["liquidity"],
        "volume_shock_exhaustion_stabilization_5_10": shock_present * volume_exhaustion * close_support * no_extension * gates["recent_shock"],
        "participation_repair_after_instability_5_10": shock_present * participation_repair * close_support * gates["breadth"],
        "dispersion_spike_normalization_5_10": shock_present * dispersion_normalization_quality * gates["dispersion"],
        "breadth_stabilization_after_panic_diffusion_5_10": shock_present * breadth_stability_quality * gates["breadth"],
        "shock_absorption_vs_propagation_quality_5_10": (absorption_quality - propagation_pressure).clip(lower=0.0) * gates["recent_shock"],
        "instability_resolution_to_stabilization_5_10": absorption_quality * rank_stability * close_support * gates["instability"],
    }

    signals: dict[str, pd.DataFrame] = {}
    diagnostics = []
    for name, raw in raw_signals.items():
        signal = _rank_cs(raw.rolling(3, min_periods=2).mean())
        signal = _neutralize_basic(signal, exposures)
        signal = _rank_cs(_rebalance_interval(signal * (raw.notna() & (raw.abs() > 0)).astype(float), 5))
        signal = _clean_panel(signal)
        signals[name] = signal
        diagnostics.append(
            {
                "signal_name": name,
                "family": _family_for(name),
                "raw_finite_pct": float(raw.notna().mean().mean()),
                "raw_mean_abs": float(raw.abs().mean().mean()),
                "signal_finite_pct": float(signal.notna().mean().mean()),
                "signal_mean_abs": float(signal.abs().mean().mean()),
            }
        )
    return signals, states, pd.DataFrame(diagnostics)


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def sample_size_summary(states: pd.DataFrame, signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        active = (panel.notna().sum(axis=1) >= 25) & (panel.abs().mean(axis=1, skipna=True) > 0.02)
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


def score_transition_signals(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_rows = []
    daily_rows = []
    for horizon in (1, 5, 10, 15, 20):
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
        best_rows = []
        for name, group in scores.groupby("signal_name"):
            filled = group["abs_mean_ic"].fillna(-np.inf)
            if np.isneginf(filled.max()):
                best_horizon = 5
            else:
                best_horizon = int(group.loc[filled.idxmax(), "horizon"])
            best_rows.append({"signal_name": name, "best_horizon": best_horizon})
        scores = scores.merge(pd.DataFrame(best_rows), on="signal_name", how="left")
        scores["is_best_horizon"] = scores["horizon"].eq(scores["best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def classify_candidates(
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
    transition_counts = (
        state_attr[
            state_attr["state"].isin(
                [
                    "RECENT_SHOCK",
                    "SHOCK_ABSORBING",
                    "LIQUIDITY_RECOVERING_AFTER_SHOCK",
                    "DISPERSION_NORMALIZING_AFTER_SHOCK",
                    "BREADTH_STABILIZING_AFTER_PANIC",
                    "INSTABILITY_RESOLVING",
                ]
            )
        ]
        .groupby("signal_name")["mean_ic"]
        .agg(
            positive_transition_state_count=lambda s: int((s > 0.004).sum()),
            best_transition_state_ic="max",
        )
        .reset_index()
    )
    summary = (
        best.merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h15[["signal_name", "h15_mean_ic", "h15_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(transition_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        h5_mean = row.get("h5_mean_ic", np.nan)
        h10_mean = row.get("h10_mean_ic", np.nan)
        h10_pos = row.get("h10_positive_ic_rate", np.nan)
        h20_mean = row.get("h20_mean_ic", np.nan)
        max_inv = row.get("max_inventory_corr", np.nan)
        max_vol = row.get("max_volatility_stress_corr", np.nan)
        if row["missing_pct"] > 0.30:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.14:
            issues.append("high_turnover")
        if h5_mean < 0.006:
            issues.append("weak_h5_ic")
        if h10_mean < 0.006:
            issues.append("weak_h10_ic")
        elif h10_mean < 0.010:
            issues.append("h10_below_validation_quality")
        if h10_pos < 0.54:
            issues.append("weak_h10_positive_ic_rate")
        if h20_mean > max(h5_mean, h10_mean):
            issues.append("h20_dependency_risk")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("one_window_dominance", 0) > 0.60:
            issues.append("one_window_concentration")
        if row.get("active_date_ratio", 0) < 0.08:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.60:
            issues.append("activation_too_broad")
        if pd.notna(max_inv) and max_inv > 0.35:
            issues.append("inventory_similarity_risk")
        if pd.notna(max_vol) and max_vol > 0.35:
            issues.append("volatility_stress_similarity_risk")
        if row.get("max_price_reversal_corr", 0) > 0.40:
            issues.append("reversal_similarity_risk")
        if row.get("max_price_momentum_corr", 0) > 0.40:
            issues.append("momentum_similarity_risk")
        if row.get("positive_transition_state_count", 0) < 2:
            issues.append("weak_transition_state_support")

        validation_ready = (
            h10_mean >= 0.014
            and h10_pos >= 0.57
            and h5_mean >= 0.010
            and h20_mean <= h10_mean
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and 0.08 <= row.get("active_date_ratio", 0) <= 0.45
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_volatility_stress_corr", 1) <= 0.30
            and row.get("max_price_reversal_corr", 1) <= 0.35
            and row.get("max_price_momentum_corr", 1) <= 0.35
            and row.get("positive_transition_state_count", 0) >= 3
        )
        refinement_ready = (
            h5_mean >= 0.009
            and h10_mean >= 0.008
            and h10_pos >= 0.55
            and h20_mean <= max(h5_mean, h10_mean) + 0.001
            and row.get("active_date_ratio", 0) >= 0.08
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_volatility_stress_corr", 1) <= 0.35
            and row.get("positive_transition_state_count", 0) >= 2
        )
        conditional_only = (
            max(h5_mean, h10_mean) >= 0.006
            and row.get("positive_transition_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.40
            and row.get("max_volatility_stress_corr", 1) <= 0.40
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
                "h5_mean_ic": h5_mean,
                "h5_positive_ic_rate": row.get("h5_positive_ic_rate"),
                "h10_mean_ic": h10_mean,
                "h10_positive_ic_rate": h10_pos,
                "h15_mean_ic": row.get("h15_mean_ic"),
                "h15_positive_ic_rate": row.get("h15_positive_ic_rate"),
                "h20_mean_ic": h20_mean,
                "h20_positive_ic_rate": row.get("h20_positive_ic_rate"),
                "turnover_proxy": row.get("turnover_proxy"),
                "active_date_ratio": row.get("active_date_ratio"),
                "persistence": row.get("persistence"),
                "sign_consistency": row.get("sign_consistency"),
                "one_window_dominance": row.get("one_window_dominance"),
                "max_inventory_corr": max_inv,
                "max_volatility_stress_corr": max_vol,
                "max_vol_shock_absorption_corr": row.get("max_vol_shock_absorption_corr"),
                "max_breadth_participation_repair_corr": row.get("max_breadth_participation_repair_corr"),
                "max_price_reversal_corr": row.get("max_price_reversal_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "positive_transition_state_count": int(row.get("positive_transition_state_count", 0) or 0),
                "best_transition_state_ic": row.get("best_transition_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    status_rank = {
        "CANDIDATE_FOR_CONDITIONAL_VALIDATION": 0,
        "CONDITIONAL_REFINEMENT_CANDIDATE": 1,
        "CONDITIONAL_ONLY_RESEARCH": 2,
        "REJECT_RESEARCH": 3,
    }
    out = pd.DataFrame(rows)
    out["status_rank"] = out["status"].map(status_rank)
    return out.sort_values(["status_rank", "h10_mean_ic", "h5_mean_ic"], ascending=[True, False, False]).drop(columns=["status_rank"])


def _write_note(
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
    status_counts = decisions["status"].value_counts().to_dict()
    top_transition = state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)
    h_table = scores[scores["horizon"].isin([5, 10, 15, 20])].copy()
    lines = [
        "# Transition-State Alpha Discovery Batch",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only Track B batch implemented 10 transition-state candidate structures under `{RUN_ID}`.",
        "",
        "The batch asks whether signals can identify a transition from h5 instability to h10 stabilization, with emphasis on shock absorption, volatility digestion, liquidity recovery, dispersion normalization, and shock propagation versus absorption.",
        "",
        f"Research-only guardrail: {RESEARCH_ONLY_GUARDRAIL}",
        "",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, signal blending, weighting engine, optimization engine, validation logic change, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.",
        "",
        "## Sources Reviewed",
        "",
        *[f"- `{path}`" for path in SOURCE_NOTES],
        "",
        "## Candidate Families",
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
        "## Component Diagnostics",
        "",
        component_diagnostics.to_markdown(index=False),
        "",
        "## h5 / h10 / h15 / h20 Behavior",
        "",
        h_table[["signal_name", "horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "best_horizon", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics were unavailable.",
        "",
        "## Orthogonality / Redundancy",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Transition-State Attribution",
        "",
        top_transition[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        stress.sort_values("mean_ic", ascending=False).groupby("signal_name").head(3)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Sample-Size Sanity",
        "",
        sample_sizes.groupby("signal_name").head(8).to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- Candidates labeled `CANDIDATE_FOR_CONDITIONAL_VALIDATION` are not promoted by this batch; they are only eligible for a future formal conditional-validation run.",
        "- Candidates labeled `CONDITIONAL_REFINEMENT_CANDIDATE` should only receive narrow, predeclared refinement diagnostics.",
        "- Candidates labeled `CONDITIONAL_ONLY_RESEARCH` are useful evidence about transition-state behavior but should not be advanced without redesign or stronger diagnostics.",
        "- Rejected candidates should be treated as negative evidence for their simple formulation, not inverted or forced into a new signal.",
        "",
        "## Recommended Next Step",
        "",
        "Review the highest-ranked `CONDITIONAL_REFINEMENT_CANDIDATE` and `CANDIDATE_FOR_CONDITIONAL_VALIDATION` labels, if any, then choose at most one candidate for a future isolated validation or refinement pass. Do not route any batch output into production, survivor/watchlist, portfolio, ML, blending, or construction workflows from this batch alone.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, component_diagnostics = build_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(CANDIDATES)

    for name, panel in signals.items():
        panel.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")

    structural = structural_summary(signals)
    scores, daily_ics = score_transition_signals(signals, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = volatility_shock_corr_summary(orth)
    active = active_coverage_summary(signals)
    state_attr = state_attribution(daily_ics, scores, states)
    stress = stress_attribution(daily_ics, scores, states)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidates(structural, scores, wfv_summary, state_attr, orth_summary, active)

    registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    component_diagnostics.to_csv(OUT_DIR / "component_diagnostics.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    state_attr.to_csv(OUT_DIR / "transition_state_attribution.csv", index=False)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    sample_sizes.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decisions.csv", index=False)

    manifest = {
        "run_id": RUN_ID,
        "research_only": True,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "candidate_count": len(CANDIDATES),
        "candidate_names": [spec["signal_name"] for spec in CANDIDATES],
        "status_counts": decisions["status"].value_counts().to_dict(),
        "production_registration": False,
        "survivor_watchlist_promotion": False,
        "portfolio_integration": False,
        "ml_integration": False,
        "signal_blending": False,
        "weighting_engine": False,
        "optimization_engine": False,
        "validation_logic_change": False,
        "gates_schemas_thresholds_modified": False,
        "production_conditional_alpha_wiring": False,
        "direct_promotion_allowed_from_batch": False,
        "artifact_files": sorted(path.name for path in OUT_DIR.iterdir()) + ["manifest.json"],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    _write_note(
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
