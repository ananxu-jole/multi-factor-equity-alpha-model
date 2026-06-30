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


RUN_ID = "idiosyncratic_stress_containment_10_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/idiosyncratic_stress_containment_10_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v5_design_screening.md")
DRAWDOWN_NOTE = Path("docs/research_notes/drawdown_pressure_stabilization_10_v1.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v2.md")
GOVERNANCE_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md")
V4_CLOSEOUT_NOTE = Path("docs/research_notes/track_b_expansion_v4_closeout_review.md")
ECOSYSTEM_NOTE = Path("docs/research_notes/inventory_ecosystem_review_v1.md")

SIGNAL_NAME = "idiosyncratic_stress_containment_10"
HORIZONS = (1, 5, 10, 15, 20)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _score_signals(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
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
        scores = scores.merge(best.rename(columns={"horizon": "best_horizon"}), on="signal_name", how="left")
        scores["is_best_horizon"] = scores["horizon"].eq(scores["best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def _state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    stabilization_quality: pd.DataFrame,
) -> pd.DataFrame:
    close = panels["close"]
    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    stress = build_stress_states(close, benchmark)
    stress_core = stress[["volatility_spike", "panic_liquidity_stress", "drawdown_acceleration"]]
    stress_recent_20 = stress_core.rolling(20, min_periods=1).max().max(axis=1).astype(bool)

    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    breadth20 = (ret20 > 0).mean(axis=1)
    dispersion20 = ret20.std(axis=1)
    broad_hostile = (stress_recent_20 | stress["weak_breadth"].fillna(False) | ((benchmark < bench_ma60) & (bench_ret20 < 0))).fillna(False)
    not_breadth_repair_cluster = (~stress["weak_breadth"].fillna(False) | (breadth20.diff(10) <= 0.03)).fillna(False)
    contained_dispersion = (dispersion20 < _rolling_quantile(dispersion20, 0.85)).fillna(False)
    high_quality_dates = stabilization_quality.mean(axis=1, skipna=True) > stabilization_quality.stack().median()
    idio_shock_share = (
        ((ret5.sub(ret5.mean(axis=1), axis=0).abs()).rank(axis=1, pct=True) > 0.75)
        | ((ret10.sub(ret10.mean(axis=1), axis=0).abs()).rank(axis=1, pct=True) > 0.75)
    ).mean(axis=1)
    idiosyncratic_stress_state = (idio_shock_share > 0.20).fillna(False)

    states = pd.DataFrame(index=close.index)
    states["IDIOSYNCRATIC_STRESS_ACTIVE"] = idiosyncratic_stress_state
    states["IDIOSYNCRATIC_STRESS_CONTAINING"] = (
        idiosyncratic_stress_state & contained_dispersion & not_breadth_repair_cluster
    ).fillna(False)
    states["IDIOSYNCRATIC_STRESS_WITH_QUALITY"] = (
        idiosyncratic_stress_state & contained_dispersion & not_breadth_repair_cluster & high_quality_dates
    ).fillna(False)
    states["IDIOSYNCRATIC_STRESS_OUTSIDE_WEAK_BREADTH"] = (
        idiosyncratic_stress_state & ~stress["weak_breadth"].fillna(False)
    ).fillna(False)
    states["CONTAINED_DISPERSION_IDIOSYNCRATIC"] = (idiosyncratic_stress_state & contained_dispersion).fillna(False)
    states["BROAD_HOSTILE_OR_STRESS"] = broad_hostile
    states["ACTIVE_HOSTILE_OR_STRESS"] = broad_hostile
    states["HOSTILE_OR_STRESS"] = states["ACTIVE_HOSTILE_OR_STRESS"]
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_idiosyncratic_stress_signal(
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
    ret15 = close.pct_change(15, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(benchmark.pct_change(5, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)

    residual_vol5 = residual1.rolling(5, min_periods=4).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()
    stress_present = _safe_div(residual_vol20, residual_vol60).rank(axis=1, pct=True).clip(lower=0.0)
    stress_containment = (1.0 - _safe_div(residual_vol5, residual_vol20).rank(axis=1, pct=True)).clip(lower=0.0)
    residual_shock_present = (
        residual10.abs().rank(axis=1, pct=True) * (1.0 - residual10.rank(axis=1, pct=True).sub(0.35).abs() * 2.5).clip(lower=0.0)
    ).clip(lower=0.0)
    no_rebound_chase = (1.0 - residual5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    range_containment = (
        (1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True))
        * (1.0 - _safe_div(true_range.rolling(20, min_periods=12).mean(), true_range.rolling(60, min_periods=40).mean()).rank(axis=1, pct=True))
    ).clip(lower=0.0)
    residual_rank10 = residual10.rank(axis=1, pct=True)
    rank_stabilization = (1.0 - residual_rank10.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
    close_support = close_location.rolling(5, min_periods=3).mean().rank(axis=1, pct=True)
    liquidity_sufficient = dollar_volume.rolling(10, min_periods=7).mean().rank(axis=1, pct=True).clip(lower=0.0)

    stabilization_quality = (
        stress_present
        * stress_containment
        * residual_shock_present
        * no_rebound_chase
        * range_containment
        * rank_stabilization
        * close_support
        * liquidity_sufficient
    ).rolling(5, min_periods=3).mean()

    states = _state_flags(panels, benchmark, stabilization_quality)
    idio_gate_raw = (
        (stress_present > 0.65)
        & (stress_containment > 0.45)
        & (residual_shock_present > residual_shock_present.stack().quantile(0.45))
    ).astype(float)
    state_gate = _market_state_panel(states["IDIOSYNCRATIC_STRESS_CONTAINING"], close.columns)
    gate = idio_gate_raw * state_gate

    signal = _rank_cs(stabilization_quality * gate)
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
    ]:
        signal = _rank_cs(_cs_neutralize(signal, exposure))
    signal = _rank_cs(_rebalance_interval(signal * gate, 10))
    signal = _clean_panel(signal)

    diagnostics = pd.DataFrame(
        {
            "component": [
                "stress_present",
                "stress_containment",
                "residual_shock_present",
                "no_rebound_chase",
                "range_containment",
                "rank_stabilization",
                "close_support",
                "liquidity_sufficient",
                "idiosyncratic_stress_gate",
                "stabilization_quality",
                "final_signal",
            ],
            "finite_pct": [
                float(stress_present.notna().mean().mean()),
                float(stress_containment.notna().mean().mean()),
                float(residual_shock_present.notna().mean().mean()),
                float(no_rebound_chase.notna().mean().mean()),
                float(range_containment.notna().mean().mean()),
                float(rank_stabilization.notna().mean().mean()),
                float(close_support.notna().mean().mean()),
                float(liquidity_sufficient.notna().mean().mean()),
                float(gate.notna().mean().mean()),
                float(stabilization_quality.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(stress_present.abs().mean().mean()),
                float(stress_containment.abs().mean().mean()),
                float(residual_shock_present.abs().mean().mean()),
                float(no_rebound_chase.abs().mean().mean()),
                float(range_containment.abs().mean().mean()),
                float(rank_stabilization.abs().mean().mean()),
                float(close_support.abs().mean().mean()),
                float(liquidity_sufficient.abs().mean().mean()),
                float(gate.abs().mean().mean()),
                float(stabilization_quality.abs().mean().mean()),
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
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret15 = close.pct_change(15, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    residual1 = ret1.sub(benchmark.pct_change(1, fill_method=None), axis=0)
    residual10 = ret10.sub(benchmark.pct_change(10, fill_method=None), axis=0)
    residual20 = ret20.sub(benchmark.pct_change(20, fill_method=None), axis=0)
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)

    downside10 = residual1.clip(upper=0.0).rolling(10, min_periods=7).sum()
    downside30 = residual1.clip(upper=0.0).rolling(30, min_periods=20).sum()
    drawdown_pressure_proxy = _rank_cs(
        (
            (1.0 - _safe_div(downside10.abs(), downside30.abs() / 3.0).rank(axis=1, pct=True)).clip(lower=0.0)
            * (1.0 - residual20.rank(axis=1, pct=True).sub(0.35).abs() * 3.0).clip(lower=0.0)
        ).rolling(5, min_periods=3).mean()
    )
    idiosyncratic_stress_proxy = _rank_cs(
        (
            _safe_div(residual1.rolling(20, min_periods=12).std(), residual1.rolling(60, min_periods=40).std()).rank(axis=1, pct=True)
            * (
                1.0
                - _safe_div(residual1.rolling(5, min_periods=4).std(), residual1.rolling(20, min_periods=12).std()).rank(axis=1, pct=True)
            ).clip(lower=0.0)
            * residual10.abs().rank(axis=1, pct=True)
        ).rolling(5, min_periods=3).mean()
    )
    active_breadth_repair_proxy = _rank_cs(
        (
            _rank_cs(-ret20)
            * (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
        ).rolling(5, min_periods=3).mean()
    )
    volatility_stabilization_proxy = _rank_cs(
        (
            (1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True))
            * (1.0 - _safe_div(residual1.rolling(10, min_periods=7).std(), residual1.rolling(30, min_periods=20).std()).rank(axis=1, pct=True))
        ).rolling(5, min_periods=3).mean()
    )
    simple_low_volatility_20 = _rank_cs(-ret1.rolling(20, min_periods=15).std())
    simple_low_residual_volatility_20 = _rank_cs(-residual1.rolling(20, min_periods=15).std())

    refs["price_rank_momentum_5"] = _rank_cs(ret5).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_10"] = _rank_cs(ret10).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_15"] = _rank_cs(ret15).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_20"] = _rank_cs(ret20).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_60"] = _rank_cs(ret60).reindex(index=first.index, columns=first.columns)
    refs["price_rank_reversal_5"] = _rank_cs(-ret5).reindex(index=first.index, columns=first.columns)
    refs["price_rank_reversal_20"] = _rank_cs(-ret20).reindex(index=first.index, columns=first.columns)
    refs["residual_momentum_10"] = _rank_cs(residual10).reindex(index=first.index, columns=first.columns)
    refs["residual_momentum_20"] = _rank_cs(residual20).reindex(index=first.index, columns=first.columns)
    refs["drawdown_pressure_proxy"] = drawdown_pressure_proxy.reindex(index=first.index, columns=first.columns)
    refs["idiosyncratic_stress_proxy"] = idiosyncratic_stress_proxy.reindex(index=first.index, columns=first.columns)
    refs["active_breadth_repair_proxy"] = active_breadth_repair_proxy.reindex(index=first.index, columns=first.columns)
    refs["volatility_stabilization_proxy"] = volatility_stabilization_proxy.reindex(index=first.index, columns=first.columns)
    refs["simple_low_volatility_20"] = simple_low_volatility_20.reindex(index=first.index, columns=first.columns)
    refs["simple_low_residual_volatility_20"] = simple_low_residual_volatility_20.reindex(index=first.index, columns=first.columns)
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


def idiosyncratic_corr_summary(orth: pd.DataFrame) -> pd.DataFrame:
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
            "price_rank_reversal_5",
            "price_rank_reversal_20",
            "residual_momentum_10",
            "residual_momentum_20",
            "drawdown_pressure_proxy",
            "idiosyncratic_stress_proxy",
            "active_breadth_repair_proxy",
            "volatility_stabilization_proxy",
            "simple_low_volatility_20",
            "simple_low_residual_volatility_20",
        ]
        for comparison in comparisons:
            sample = group[group["comparison"].eq(comparison)]
            row[f"{comparison}_corr"] = float(sample["abs_value_corr"].max()) if not sample.empty else np.nan
        momentum_refs = group[group["comparison"].isin(["plain_momentum_60", "price_rank_momentum_5", "price_rank_momentum_10", "price_rank_momentum_15", "price_rank_momentum_20", "price_rank_momentum_60", "residual_momentum_10", "residual_momentum_20"])]
        reversal_refs = group[group["comparison"].isin(["short_reversal_5", "price_rank_reversal_5", "price_rank_reversal_20"])]
        breadth_refs = group[group["comparison"].isin(["active_breadth_repair_proxy", "inventory_participation_breadth_repair_under_hostile_trend", "inventory_participation_liquidity_state_shift_20_60"])]
        volatility_refs = group[group["comparison"].isin(["volatility_stabilization_proxy", "inventory_volatility_compression_after_stress_stabilization"])]
        drawdown_refs = group[group["comparison"].isin(["drawdown_pressure_proxy"])]
        low_vol_refs = group[group["comparison"].isin(["simple_low_volatility_20", "simple_low_residual_volatility_20"])]
        row["max_price_momentum_corr"] = float(momentum_refs["abs_value_corr"].max()) if not momentum_refs.empty else np.nan
        row["max_price_reversal_corr"] = float(reversal_refs["abs_value_corr"].max()) if not reversal_refs.empty else np.nan
        row["max_breadth_participation_repair_corr"] = float(breadth_refs["abs_value_corr"].max()) if not breadth_refs.empty else np.nan
        row["max_volatility_stress_corr"] = float(volatility_refs["abs_value_corr"].max()) if not volatility_refs.empty else np.nan
        row["max_drawdown_pressure_corr"] = float(drawdown_refs["abs_value_corr"].max()) if not drawdown_refs.empty else np.nan
        row["max_low_volatility_corr"] = float(low_vol_refs["abs_value_corr"].max()) if not low_vol_refs.empty else np.nan
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
    idio_counts = (
        state_attr[
            state_attr["state"].isin(
                [
                    "IDIOSYNCRATIC_STRESS_ACTIVE",
                    "IDIOSYNCRATIC_STRESS_CONTAINING",
                    "IDIOSYNCRATIC_STRESS_WITH_QUALITY",
                    "IDIOSYNCRATIC_STRESS_OUTSIDE_WEAK_BREADTH",
                    "CONTAINED_DISPERSION_IDIOSYNCRATIC",
                ]
            )
        ]
        .groupby("signal_name")["mean_ic"]
        .agg(positive_idiosyncratic_state_count=lambda s: int((s > 0.004).sum()), best_idiosyncratic_state_ic="max")
        .reset_index()
    )
    hostile_counts = (
        state_attr[
            state_attr["state"].isin(
                [
                    "ACTIVE_HOSTILE_OR_STRESS",
                    "HOSTILE_OR_STRESS",
                    "weak_breadth",
                    "drawdown_acceleration",
                    "volatility_spike",
                    "panic_liquidity_stress",
                ]
            )
        ]
        .groupby("signal_name")["mean_ic"]
        .agg(best_hostile_stress_state_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h5[["signal_name", "h5_mean_ic", "h5_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h15[["signal_name", "h15_mean_ic", "h15_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(idio_counts, on="signal_name", how="left")
        .merge(hostile_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        h10_mean = row.get("h10_mean_ic", np.nan)
        h10_pos = row.get("h10_positive_ic_rate", np.nan)
        primary_mean = max(row.get("h10_mean_ic", np.nan), row.get("h15_mean_ic", np.nan), row.get("mean_ic", np.nan))
        primary_pos = max(row.get("h10_positive_ic_rate", np.nan), row.get("h15_positive_ic_rate", np.nan), row.get("positive_ic_rate", np.nan))
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.12:
            issues.append("high_turnover")
        if h10_mean < 0.008:
            issues.append("weak_h10_ic")
        if h10_pos < 0.525:
            issues.append("weak_h10_positive_ic_rate")
        if primary_mean < 0.006:
            issues.append("weak_primary_ic")
        if primary_pos < 0.52:
            issues.append("weak_positive_ic_rate")
        if int(row["horizon"]) == 20 and row.get("h20_mean_ic", np.nan) > max(row.get("h10_mean_ic", np.nan), row.get("h15_mean_ic", np.nan)):
            issues.append("h20_dependency_risk")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("active_date_ratio", 1) < 0.08:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.60:
            issues.append("activation_too_broad")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_breadth_participation_repair_corr", 0) > 0.35:
            issues.append("breadth_participation_repair_similarity_risk")
        if row.get("max_volatility_stress_corr", 0) > 0.35:
            issues.append("volatility_stress_similarity_risk")
        if row.get("max_drawdown_pressure_corr", 0) > 0.35:
            issues.append("drawdown_pressure_similarity_risk")
        if row.get("max_price_reversal_corr", 0) > 0.45 or row.get("max_reversal_corr", 0) > 0.45:
            issues.append("reversal_similarity_risk")
        if row.get("max_price_momentum_corr", 0) > 0.45:
            issues.append("momentum_similarity_risk")
        if row.get("max_low_volatility_corr", 0) > 0.45:
            issues.append("low_volatility_similarity_risk")
        if row.get("positive_idiosyncratic_state_count", 0) < 2:
            issues.append("weak_idiosyncratic_state_support")

        if (
            h10_mean > 0.014
            and h10_pos >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.10
            and 0.08 <= row.get("active_date_ratio", 0) <= 0.50
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_breadth_participation_repair_corr", 1) <= 0.30
            and row.get("max_volatility_stress_corr", 1) <= 0.30
            and row.get("max_price_reversal_corr", 1) <= 0.40
            and row.get("max_price_momentum_corr", 1) <= 0.40
            and row.get("positive_idiosyncratic_state_count", 0) >= 3
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            h10_mean > 0.009
            and h10_pos >= 0.525
            and row.get("positive_idiosyncratic_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_breadth_participation_repair_corr", 1) <= 0.35
            and row.get("max_volatility_stress_corr", 1) <= 0.35
            and row.get("active_date_ratio", 0) >= 0.08
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_idiosyncratic_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.40
            and row.get("max_breadth_participation_repair_corr", 1) <= 0.40
            and row.get("max_volatility_stress_corr", 1) <= 0.40
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "idiosyncratic_stress_containment",
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
                "max_breadth_participation_repair_corr": row.get("max_breadth_participation_repair_corr"),
                "max_volatility_stress_corr": row.get("max_volatility_stress_corr"),
                "max_drawdown_pressure_corr": row.get("max_drawdown_pressure_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_price_reversal_corr": row.get("max_price_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "max_price_momentum_corr": row.get("max_price_momentum_corr"),
                "max_low_volatility_corr": row.get("max_low_volatility_corr"),
                "drawdown_pressure_proxy_corr": row.get("drawdown_pressure_proxy_corr"),
                "idiosyncratic_stress_proxy_corr": row.get("idiosyncratic_stress_proxy_corr"),
                "active_breadth_repair_proxy_corr": row.get("active_breadth_repair_proxy_corr"),
                "volatility_stabilization_proxy_corr": row.get("volatility_stabilization_proxy_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "inventory_volatility_corr": row.get("inventory_volatility_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_idiosyncratic_state_count": int(row.get("positive_idiosyncratic_state_count", 0) or 0),
                "best_idiosyncratic_state_ic": row.get("best_idiosyncratic_state_ic"),
                "best_hostile_stress_state_ic": row.get("best_hostile_stress_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def _fmt(value: object) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{float(value):.6f}"


def _decision_text(decision: pd.Series) -> str:
    status = str(decision["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return "`idiosyncratic_stress_containment_10` should move to formal conditional validation using this fixed single formulation."
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return "`idiosyncratic_stress_containment_10` should receive a narrow refinement diagnostics pass focused on h10 strength, activation breadth, drawdown-pressure separation, and reversal separation."
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return "`idiosyncratic_stress_containment_10` should remain conditional-only research evidence until h10 strength or idiosyncratic-state support improves."
    return "`idiosyncratic_stress_containment_10` should be rejected in this formulation before moving to the next Expansion v5 concept."


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
        "# Idiosyncratic Stress Containment 10 v1",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only run tested one simple formulation of `{SIGNAL_NAME}` under the isolated run namespace `{RUN_ID}`.",
        "",
        "The formulation tests whether assets with stock-specific stress that is being contained can produce a shorter-horizon repair/stabilization edge, especially around h10, without becoming broad drawdown pressure, breadth/participation repair, reversal, or momentum.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v5 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v5 design screen: `{SOURCE_NOTE}`",
        f"- Drawdown pressure stabilization v1: `{DRAWDOWN_NOTE}`",
        f"- Conditional Alpha Inventory Monitoring v2: `{MONITORING_NOTE}`",
        f"- Conditional Alpha Inventory v2 Governance Update: `{GOVERNANCE_NOTE}`",
        f"- Expansion v4 closeout review: `{V4_CLOSEOUT_NOTE}`",
        f"- Inventory Ecosystem Review v1: `{ECOSYSTEM_NOTE}`",
        "- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | Stock-specific stress containment may identify repair behavior that is not primarily a broad market drawdown or breadth-repair event. |",
        "| Idiosyncratic stress definition | Elevated residual volatility and residual shock magnitude at the asset level relative to each stock's recent residual baseline. |",
        "| Containment/stabilization logic | Residual volatility begins contracting, rank churn declines, range behavior contains, close support improves, and liquidity remains sufficient. |",
        "| Difference from broad drawdown pressure | Activation is stock-level and residual; broad drawdown pressure is included only as an attribution and similarity risk. |",
        "| Difference from active breadth/participation repair | The gate does not require weak breadth or participation recovery and explicitly tracks outside-weak-breadth support. |",
        "| Difference from simple reversal | The signal avoids pure residual losers and neutralizes reversal exposures after scoring. |",
        "| Difference from price momentum | Price-rank momentum and residual momentum exposures are neutralized. |",
        "| Why it may reduce h20 concentration | The mechanism is designed around h10 stock-level containment and uses a 10-day rebalance interval, with h20 treated as diagnostic risk. |",
        "| Expected activation semantics | Asset-level residual stress is present, near-term stress is containing, and market breadth repair is not the required activation driver. |",
        "| Expected horizon | h10 primary; h5 and h15 secondary; h20 diagnostic. |",
        "| Expected turnover | Medium after fixed 10-day rebalance control. |",
        "| Expected active coverage | Medium conditional coverage; sparsity or broad activation are review issues. |",
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
        "## Idiosyncratic Stress Attribution",
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
        f"- Genuinely idiosyncratic stress containment: positive idiosyncratic-state count was `{int(decision['positive_idiosyncratic_state_count'])}` and best idiosyncratic-state IC was `{_fmt(decision['best_idiosyncratic_state_ic'])}`.",
        f"- Broad drawdown-pressure risk: max drawdown-pressure correlation was `{_fmt(decision['max_drawdown_pressure_corr'])}`.",
        f"- Reversal risk: max price-reversal correlation was `{_fmt(decision['max_price_reversal_corr'])}` and max generic reversal correlation was `{_fmt(decision['max_reversal_corr'])}`.",
        f"- Momentum risk: max price-momentum correlation was `{_fmt(decision['max_price_momentum_corr'])}` and max generic momentum correlation was `{_fmt(decision['max_momentum_corr'])}`.",
        f"- Breadth/participation repair risk: max breadth/participation repair correlation was `{_fmt(decision['max_breadth_participation_repair_corr'])}`.",
        f"- Volatility/stress stabilization risk: max volatility/stress correlation was `{_fmt(decision['max_volatility_stress_corr'])}`.",
        f"- Inventory overlap risk: max inventory correlation was `{_fmt(decision['max_inventory_corr'])}`.",
        f"- h20 dependence risk: h10 IC was `{_fmt(decision['h10_mean_ic'])}` and h20 IC was `{_fmt(decision['h20_mean_ic'])}`.",
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
    signals, states, component_diagnostics = build_idiosyncratic_stress_signal(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "idiosyncratic_stress_containment",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V5_RESEARCH_ONLY",
                "mechanism_thesis": "Shorter-horizon repair from containment of stock-specific residual stress.",
                "idiosyncratic_stress_definition": "Elevated residual volatility and residual shock magnitude at the asset level.",
                "containment_stabilization_logic": "Residual vol contraction, rank stabilization, range containment, close support, and sufficient liquidity.",
                "differs_from_inventory": "Stock-level residual stress gate rather than participation, breadth, liquidity repair, or h20 volatility compression.",
                "differs_from_reversal_momentum": "Avoids pure residual losers and neutralizes reversal, momentum, and residual momentum exposures.",
                "expected_activation_state": "IDIOSYNCRATIC_STRESS_CONTAINING",
                "expected_horizon": "h10 primary; h5/h15 secondary; h20 diagnostic",
                "expected_turnover_profile": "medium",
                "expected_active_coverage": "medium",
            }
        ]
    )
    structural = structural_summary(signals)
    scores, daily_ics = _score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = idiosyncratic_corr_summary(orth)
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
                "drawdown_note": str(DRAWDOWN_NOTE),
                "monitoring_note": str(MONITORING_NOTE),
                "governance_note": str(GOVERNANCE_NOTE),
                "v4_closeout_note": str(V4_CLOSEOUT_NOTE),
                "candidate_count": 1,
                "broad_search": False,
                "parameter_grid": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "other_expansion_v5_concepts_implemented": False,
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
