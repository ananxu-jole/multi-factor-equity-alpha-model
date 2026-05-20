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


RUN_ID = "neutral_accumulation_without_breakout_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/neutral_accumulation_without_breakout_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v3_design_screening.md")
MONITORING_NOTE = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v1.md")
GOVERNANCE_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v2_governance_update.md")
ECOSYSTEM_NOTE = Path("docs/research_notes/inventory_ecosystem_review_v1.md")

SIGNAL_NAME = "neutral_accumulation_without_breakout"


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _neutral_state_flags(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    accumulation_quality: pd.DataFrame,
    breakout_flag: pd.DataFrame,
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

    trend_hostile = ((benchmark < bench_ma60) & (bench_20 < 0)).fillna(False)
    weak_breadth = stress["weak_breadth"].fillna(False)
    calm_normal_vol = (
        (bench_vol20 < _rolling_quantile(bench_vol20, 0.65))
        & (bench_vol20 > _rolling_quantile(bench_vol20, 0.10))
    ).fillna(False)
    normal_dispersion = (dispersion20 < _rolling_quantile(dispersion20, 0.70)).fillna(False)
    neutral_market = (~stress_recent & ~trend_hostile & ~weak_breadth).fillna(False)
    constructive_not_euphoric = (
        (breadth20 > _rolling_quantile(breadth20, 0.35))
        & (breadth20 < _rolling_quantile(breadth20, 0.85))
    ).fillna(False)
    quality_dates = accumulation_quality.mean(axis=1, skipna=True) > accumulation_quality.stack().median()
    breakout_share = breakout_flag.mean(axis=1)
    breakout_pressure = (
        breakout_share > breakout_share.rolling(252, min_periods=100).quantile(0.75)
    ).fillna(False)

    states = pd.DataFrame(index=close.index)
    states["NEUTRAL_MARKET_STATE"] = neutral_market
    states["CALM_NORMAL_VOL"] = (neutral_market & calm_normal_vol).fillna(False)
    states["NORMAL_DISPERSION"] = (neutral_market & normal_dispersion).fillna(False)
    states["NON_HOSTILE_NOT_WEAK_BREADTH"] = (~trend_hostile & ~weak_breadth).fillna(False)
    states["CONSTRUCTIVE_NOT_EUPHORIC"] = (neutral_market & constructive_not_euphoric).fillna(False)
    states["QUIET_ACCUMULATION_STATE"] = (neutral_market & quality_dates & ~breakout_pressure).fillna(False)
    states["BREAKOUT_PRESSURE"] = breakout_pressure
    states["HOSTILE_OR_STRESS"] = (stress_recent | trend_hostile | weak_breadth).fillna(False)
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_neutral_accumulation_signal(
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
    ret10_rank01 = ret10.rank(axis=1, pct=True)
    ret20_rank01 = ret20.rank(axis=1, pct=True)
    ret20_rank = _rank_cs(ret20)
    ret60_rank = _rank_cs(ret60)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()

    dv5 = dollar_volume.rolling(5, min_periods=4).mean()
    dv20 = dollar_volume.rolling(20, min_periods=12).mean()
    dv60 = dollar_volume.rolling(60, min_periods=40).mean()
    volume_ratio_5_20 = _safe_div(dv5, dv20).clip(0.0, 5.0)
    volume_ratio_20_60 = _safe_div(dv20, dv60).clip(0.0, 5.0)
    controlled_participation = (
        (1.0 - (volume_ratio_5_20 - 1.15).abs().rank(axis=1, pct=True))
        * (1.0 - (volume_ratio_20_60 - 1.05).abs().rank(axis=1, pct=True))
    ).clip(lower=0.0)

    close_support = close_location.rolling(5, min_periods=3).mean().rank(axis=1, pct=True)
    range_containment = (
        (1.0 - _safe_div(range5, range20).rank(axis=1, pct=True))
        * (1.0 - _safe_div(range20, range60).rank(axis=1, pct=True))
    ).clip(lower=0.0)
    path_orderliness = (1.0 - ret1.diff().abs().rolling(10, min_periods=6).mean().rank(axis=1, pct=True)).clip(lower=0.0)
    neutral_price_rank = (
        (1.0 - ret10_rank01.sub(0.5).abs() * 2.0)
        * (1.0 - ret20_rank01.sub(0.5).abs() * 2.0)
    ).clip(lower=0.0)

    rolling_high20 = close.rolling(20, min_periods=12).max().shift(1)
    distance_to_high20 = close / rolling_high20 - 1.0
    breakout_flag = (
        (distance_to_high20 >= -0.005)
        | (ret10_rank01 >= 0.80)
        | (ret20_rank01 >= 0.80)
    ).fillna(False)
    no_breakout_score = (1.0 - distance_to_high20.rank(axis=1, pct=True)).clip(lower=0.0)
    no_breakout_gate = (~breakout_flag).astype(float)

    accumulation_quality = (
        controlled_participation
        * close_support
        * range_containment
        * path_orderliness
        * neutral_price_rank
        * no_breakout_score
    ).rolling(5, min_periods=3).mean()

    states = _neutral_state_flags(panels, benchmark, accumulation_quality, breakout_flag)
    neutral_gate = _market_state_panel(states["NEUTRAL_MARKET_STATE"], close.columns)

    signal = _rank_cs(accumulation_quality * no_breakout_gate * neutral_gate)
    signal = _rank_cs(_cs_neutralize(signal, ret20_rank))
    signal = _rank_cs(_cs_neutralize(signal, ret60_rank))
    signal = _rank_cs(_cs_neutralize(signal, _rank_cs(ret5)))
    signal = _rank_cs(_rebalance_interval(signal * neutral_gate, 5))
    signal = _clean_panel(signal)

    diagnostics = pd.DataFrame(
        {
            "component": [
                "controlled_participation",
                "close_support",
                "range_containment",
                "path_orderliness",
                "neutral_price_rank",
                "no_breakout_score",
                "no_breakout_gate",
                "neutral_gate",
                "accumulation_quality",
                "final_signal",
            ],
            "finite_pct": [
                float(controlled_participation.notna().mean().mean()),
                float(close_support.notna().mean().mean()),
                float(range_containment.notna().mean().mean()),
                float(path_orderliness.notna().mean().mean()),
                float(neutral_price_rank.notna().mean().mean()),
                float(no_breakout_score.notna().mean().mean()),
                float(no_breakout_gate.notna().mean().mean()),
                float(neutral_gate.notna().mean().mean()),
                float(accumulation_quality.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(controlled_participation.abs().mean().mean()),
                float(close_support.abs().mean().mean()),
                float(range_containment.abs().mean().mean()),
                float(path_orderliness.abs().mean().mean()),
                float(neutral_price_rank.abs().mean().mean()),
                float(no_breakout_score.abs().mean().mean()),
                float(no_breakout_gate.abs().mean().mean()),
                float(neutral_gate.abs().mean().mean()),
                float(accumulation_quality.abs().mean().mean()),
                float(signal.abs().mean().mean()),
            ],
        }
    )
    return {SIGNAL_NAME: signal}, states, diagnostics


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    high = panels["high"]
    low = panels["low"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    dollar_volume = close * volume
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    rolling_high20 = close.rolling(20, min_periods=12).max().shift(1)
    distance_to_high20 = close / rolling_high20 - 1.0
    breakout_continuation = _rank_cs(
        (
            (distance_to_high20 >= -0.005).astype(float)
            * ret20.rank(axis=1, pct=True)
            * close_location.rolling(3, min_periods=2).mean()
        ).rolling(3, min_periods=2).mean()
    )
    range_compression_breakout = _rank_cs(
        (
            (1.0 - _safe_div(true_range.rolling(5, min_periods=4).mean(), true_range.rolling(20, min_periods=12).mean()).rank(axis=1, pct=True))
            * ret10.rank(axis=1, pct=True)
            * close_location
        ).rolling(5, min_periods=3).mean()
    )
    quiet_liquidity = _rank_cs(
        (
            (1.0 - _safe_div(dollar_volume.rolling(5, min_periods=4).mean(), dollar_volume.rolling(20, min_periods=12).mean()).sub(1.15).abs().rank(axis=1, pct=True))
            * (1.0 - ret20.rank(axis=1, pct=True).sub(0.5).abs() * 2.0)
        ).rolling(5, min_periods=3).mean()
    )
    refs["price_rank_momentum_5"] = _rank_cs(ret5).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_10"] = _rank_cs(ret10).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_20"] = _rank_cs(ret20).reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_60"] = _rank_cs(ret60).reindex(index=first.index, columns=first.columns)
    refs["raw_breakout_continuation_20"] = breakout_continuation.reindex(index=first.index, columns=first.columns)
    refs["range_compression_breakout_proxy"] = range_compression_breakout.reindex(index=first.index, columns=first.columns)
    refs["quiet_liquidity_accumulation_proxy"] = quiet_liquidity.reindex(index=first.index, columns=first.columns)
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


def neutral_corr_summary(orth: pd.DataFrame) -> pd.DataFrame:
    summary = max_corr_table(orth)
    rows = []
    for name, group in orth.groupby("signal_name"):
        row = {"signal_name": name}
        for comparison in [
            "price_rank_momentum_5",
            "price_rank_momentum_10",
            "price_rank_momentum_20",
            "price_rank_momentum_60",
            "raw_breakout_continuation_20",
            "range_compression_breakout_proxy",
            "quiet_liquidity_accumulation_proxy",
        ]:
            sample = group[group["comparison"].eq(comparison)]
            row[f"{comparison}_corr"] = float(sample["abs_value_corr"].max()) if not sample.empty else np.nan
        momentum_refs = group[group["comparison"].isin(["plain_momentum_60", "price_rank_momentum_5", "price_rank_momentum_10", "price_rank_momentum_20", "price_rank_momentum_60"])]
        breakout_refs = group[group["comparison"].isin(["raw_breakout_continuation_20", "range_compression_breakout_proxy"])]
        row["max_price_momentum_corr"] = float(momentum_refs["abs_value_corr"].max()) if not momentum_refs.empty else np.nan
        row["max_breakout_continuation_corr"] = float(breakout_refs["abs_value_corr"].max()) if not breakout_refs.empty else np.nan
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
    h10 = scores[scores["horizon"].eq(10)].rename(
        columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate", "n_dates": "h10_n_dates"}
    )
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate", "n_dates": "h20_n_dates"}
    )
    neutral_counts = (
        state_attr[state_attr["state"].isin(["NEUTRAL_MARKET_STATE", "CALM_NORMAL_VOL", "NORMAL_DISPERSION", "QUIET_ACCUMULATION_STATE", "CONSTRUCTIVE_NOT_EUPHORIC"])]
        .groupby("signal_name")["mean_ic"]
        .agg(positive_neutral_state_count=lambda s: int((s > 0.004).sum()), best_neutral_state_ic="max")
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
        best.merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate", "h10_n_dates"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(neutral_counts, on="signal_name", how="left")
        .merge(hostile_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        primary_mean = max(row.get("h10_mean_ic", np.nan), row.get("mean_ic", np.nan))
        primary_pos = row.get("h10_positive_ic_rate", row.get("positive_ic_rate", np.nan))
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.14:
            issues.append("high_turnover")
        if primary_mean < 0.006:
            issues.append("weak_primary_ic")
        if primary_pos < 0.52:
            issues.append("weak_positive_ic_rate")
        if row.get("h20_mean_ic", 0) < 0:
            issues.append("negative_h20_ic")
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
        if row.get("max_breakout_continuation_corr", 0) > 0.45:
            issues.append("breakout_continuation_similarity")
        if row.get("active_date_ratio", 1) < 0.15:
            issues.append("sparse_activation")
        if row.get("active_date_ratio", 0) > 0.80:
            issues.append("activation_too_broad")
        if row.get("positive_neutral_state_count", 0) < 2:
            issues.append("weak_neutral_state_support")
        if row.get("best_hostile_state_ic", -1) > row.get("best_neutral_state_ic", np.nan):
            issues.append("hostile_state_dependence_risk")

        if (
            primary_mean > 0.014
            and primary_pos >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.10
            and row.get("active_date_ratio", 0) >= 0.15
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_price_momentum_corr", 1) <= 0.40
            and row.get("max_breakout_continuation_corr", 1) <= 0.40
            and row.get("positive_neutral_state_count", 0) >= 3
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            primary_mean > 0.009
            and primary_pos >= 0.525
            and row.get("positive_neutral_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_breakout_continuation_corr", 1) <= 0.45
            and row.get("active_date_ratio", 0) >= 0.12
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_neutral_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.40
            and row.get("max_breakout_continuation_corr", 1) <= 0.50
            and row.get("active_date_ratio", 0) >= 0.10
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "neutral_state_accumulation",
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
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
                "max_breakout_continuation_corr": row.get("max_breakout_continuation_corr"),
                "raw_breakout_continuation_20_corr": row.get("raw_breakout_continuation_20_corr"),
                "range_compression_breakout_proxy_corr": row.get("range_compression_breakout_proxy_corr"),
                "quiet_liquidity_accumulation_proxy_corr": row.get("quiet_liquidity_accumulation_proxy_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "inventory_volatility_corr": row.get("inventory_volatility_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "positive_neutral_state_count": int(row.get("positive_neutral_state_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "best_neutral_state_ic": row.get("best_neutral_state_ic"),
                "best_hostile_state_ic": row.get("best_hostile_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def _decision_text(decisions: pd.DataFrame) -> str:
    status = str(decisions.iloc[0]["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return (
            "`neutral_accumulation_without_breakout` should move to formal conditional validation "
            "using this fixed single formulation. Do not add a parameter grid."
        )
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return (
            "`neutral_accumulation_without_breakout` should receive a narrow refinement diagnostics pass only, "
            "focused on neutral-state support, no-breakout preservation, turnover, and baseline separation."
        )
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return (
            "`neutral_accumulation_without_breakout` should remain conditional-only research evidence. "
            "Do not advance until neutral-state behavior is stronger and cleaner versus breakout and momentum baselines."
        )
    return (
        "`neutral_accumulation_without_breakout` should be rejected in this formulation. "
        "Treat the result as evidence about neutral-state accumulation before testing another Expansion v3 concept."
    )


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
    h10 = scores[scores["horizon"].eq(10)].copy()
    h20 = scores[scores["horizon"].eq(20)].copy()
    top_states = state_attr.sort_values("mean_ic", ascending=False).head(12)
    top_stress = stress.sort_values("mean_ic", ascending=False).head(8)
    lines = [
        "# Neutral Accumulation Without Breakout v1",
        "",
        "## Executive Takeaway",
        "",
        "This research-only run tested one simple formulation of `neutral_accumulation_without_breakout` under the isolated run namespace `neutral_accumulation_without_breakout_v1`.",
        "",
        "The formulation was designed to test whether quiet accumulation in neutral, non-hostile market states can add a calmer-state Conditional Alpha Inventory dimension without collapsing into breakout continuation, momentum, reversal, or existing participation/liquidity repair.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v3 concepts was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v3 design screen: `{SOURCE_NOTE}`",
        f"- Conditional Alpha Inventory Monitoring v1: `{MONITORING_NOTE}`",
        f"- Conditional Alpha Inventory v2 Governance Update: `{GOVERNANCE_NOTE}`",
        f"- Inventory Ecosystem Review v1: `{ECOSYSTEM_NOTE}`",
        "- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | Some names may accumulate quietly during neutral market states before visible breakout or stress repair. Controlled participation, stable closes, contained range, and neutral price rank can indicate accumulation without price-rank chase. |",
        "| Neutral-state accumulation logic | The signal requires non-hostile, non-panic, non-weak-breadth market context, controlled dollar-volume participation, supportive close location, range containment, path orderliness, and neutral short/medium price rank. |",
        "| No-breakout filter | Candidate exposure is penalized or vetoed when the name is near its recent 20-day high or sits in the top cross-sectional ranks of 10-day or 20-day return. |",
        "| Difference from breakout continuation | It does not reward being near a breakout high; that condition is a veto. It also neutralizes short and medium price-rank exposure. |",
        "| Difference from reversal/momentum | It does not buy losers, fade prior returns, or chase winners. The price-rank component is intentionally centered near neutral. |",
        "| Difference from current inventory | It activates in neutral/calm states rather than hostile trend, weak breadth, drawdown, panic/liquidity stress, or post-stress stabilization. |",
        "| Expected activation semantics | Neutral market state with quiet accumulation quality and no breakout risk. |",
        "| Expected horizon | h5-h10 primary; h20 monitored for inventory comparability. |",
        "| Expected turnover | Low to medium after fixed five-day rebalance control. |",
        "| Expected active coverage | Medium; too sparse or always-on behavior is a review issue. |",
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
        scores[
            ["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]
        ].to_markdown(index=False),
        "",
        "## h10 Behavior",
        "",
        h10[["signal_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## h20 Behavior",
        "",
        h20[["signal_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
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
        f"- Genuinely neutral-state accumulation: assessed through neutral-state attribution and `QUIET_ACCUMULATION_STATE`; positive neutral-state count was `{decision['positive_neutral_state_count']}` and best neutral-state IC was `{decision['best_neutral_state_ic']:.6f}`.",
        f"- Breakout continuation risk: max breakout-continuation correlation was `{decision['max_breakout_continuation_corr']:.6f}`; raw breakout and range-compression breakout correlations were `{decision['raw_breakout_continuation_20_corr']:.6f}` / `{decision['range_compression_breakout_proxy_corr']:.6f}`.",
        f"- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `{decision['max_price_momentum_corr']:.6f}` / `{decision['max_reversal_corr']:.6f}`.",
        f"- Participation/liquidity repair overlap risk: inventory liquidity/breadth/volatility correlations were `{decision['inventory_liquidity_corr']:.6f}` / `{decision['inventory_breadth_corr']:.6f}` / `{decision['inventory_volatility_corr']:.6f}`.",
        f"- Sparse or broad activation risk: active date ratio was `{decision['active_date_ratio']:.6f}`.",
        f"- Turnover risk: turnover proxy was `{decision['turnover_proxy']:.6f}`.",
        f"- Directional stability: WFV-style persistence/sign consistency were `{decision['wfv_persistence']}` / `{decision['wfv_sign_consistency']}`.",
        f"- h10/h20 profile: h10 mean IC was `{decision['h10_mean_ic']:.6f}` and h20 mean IC was `{decision['h20_mean_ic']:.6f}`.",
        "",
        "## Recommended Next Step",
        "",
        _decision_text(decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, component_diagnostics = build_neutral_accumulation_signal(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "neutral_state_accumulation",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V3_RESEARCH_ONLY",
                "mechanism_thesis": "Neutral-state quiet accumulation with no breakout continuation.",
                "state_transition_logic": "Non-hostile non-stress market state plus controlled participation, stable closes, contained range, neutral price rank, and no-breakout veto.",
                "differs_from_inventory": "Targets neutral/calm accumulation instead of hostile/stress h20 repair.",
                "differs_from_reversal_momentum": "Neutralizes price rank and vetoes breakout/extension rather than fading or chasing price moves.",
                "expected_activation_state": "NEUTRAL_MARKET_STATE_AND_QUIET_ACCUMULATION",
                "expected_horizon": "h5-h10 primary; h20 diagnostic",
                "expected_turnover_profile": "low_to_medium",
                "expected_active_coverage": "medium",
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
    orth_summary = neutral_corr_summary(orth)
    active = active_coverage_summary(signals)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidate(structural, scores, wfv_summary, stress, state_attr, orth_summary, active)

    artifact_files = [
        "candidate_registry.csv",
        "component_diagnostics.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "neutral_state_flags.csv",
        "stress_regime_attribution.csv",
        "neutral_state_attribution.csv",
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
    states.to_csv(OUT_DIR / "neutral_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "neutral_state_attribution.csv", index=False)
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
                "monitoring_note": str(MONITORING_NOTE),
                "governance_note": str(GOVERNANCE_NOTE),
                "ecosystem_note": str(ECOSYSTEM_NOTE),
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
