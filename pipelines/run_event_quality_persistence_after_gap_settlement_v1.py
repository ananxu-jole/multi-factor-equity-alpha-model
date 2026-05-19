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
)
from run_dispersion_recovery_stability_after_stress_v1 import (
    VOLATILITY_INVENTORY_PATH,
    max_corr_table,
)


RUN_ID = "event_quality_persistence_after_gap_settlement_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/event_quality_persistence_after_gap_settlement_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md")
DISPERSION_NOTE = Path("docs/research_notes/dispersion_recovery_stability_after_stress_v1.md")
INVENTORY_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v1.md")

SIGNAL_NAME = "event_quality_persistence_after_gap_settlement"


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _event_state_flags(
    panels: dict[str, pd.DataFrame],
    recent_event_active: pd.DataFrame,
    settlement_quality: pd.DataFrame,
) -> pd.DataFrame:
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    prev_close = close.shift(1)
    gap = open_ / prev_close - 1.0
    true_range = ((high - low) / prev_close).replace([np.inf, -np.inf], np.nan)
    volume_ratio = _safe_div(volume, volume.rolling(20, min_periods=10).mean()).replace([np.inf, -np.inf], np.nan)
    abs_gap_rank = gap.abs().rank(axis=1, pct=True)

    event_dates = (recent_event_active.sum(axis=1) >= 25)
    high_quality_dates = (settlement_quality.mean(axis=1, skipna=True) > settlement_quality.stack().median())
    large_gap_dates = (abs_gap_rank.ge(0.80).sum(axis=1) >= 10)
    range_aftershock_dates = (true_range.mean(axis=1) > true_range.mean(axis=1).rolling(60, min_periods=40).mean())
    controlled_volume_dates = (volume_ratio.mean(axis=1) < volume_ratio.mean(axis=1).rolling(60, min_periods=40).quantile(0.75))

    states = pd.DataFrame(index=close.index)
    states["RECENT_EVENT_ACTIVE"] = event_dates.fillna(False)
    states["HIGH_SETTLEMENT_QUALITY"] = high_quality_dates.fillna(False)
    states["EVENT_AND_HIGH_QUALITY"] = (event_dates & high_quality_dates).fillna(False)
    states["LARGE_GAP_CROSS_SECTION"] = large_gap_dates.fillna(False)
    states["RANGE_AFTERSHOCK"] = range_aftershock_dates.fillna(False)
    states["CONTROLLED_VOLUME_EVENT_STATE"] = (event_dates & controlled_volume_dates).fillna(False)
    states["LOW_QUALITY_EVENT_STATE"] = (event_dates & ~high_quality_dates).fillna(False)
    return states


def build_event_quality_signal(
    panels: dict[str, pd.DataFrame],
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    prev_close = close.shift(1)
    gap = open_ / prev_close - 1.0
    ret5 = close.pct_change(5, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret20_rank = _rank_cs(ret20)
    true_range = ((high - low) / prev_close).replace([np.inf, -np.inf], np.nan)
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)

    gap_abs_rank = gap.abs().rank(axis=1, pct=True)
    material_gap = ((gap_abs_rank >= 0.80) & (gap.abs() >= 0.005)).astype(float)
    event_direction = np.sign(gap).where(material_gap.astype(bool))
    recent_event_direction = event_direction.ffill(limit=5)
    recent_event_active = recent_event_direction.notna().astype(float)

    range3 = true_range.rolling(3, min_periods=2).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    aftershock_decay = (1.0 - _safe_div(range3, range20)).clip(lower=0.0, upper=1.0)

    volume_ratio3 = _safe_div(volume.rolling(3, min_periods=2).mean(), volume.rolling(20, min_periods=10).mean()).clip(0.0, 5.0)
    controlled_volume = (1.0 - (volume_ratio3 - 1.25).abs().rank(axis=1, pct=True)).clip(lower=0.0)

    close_support = (np.sign(recent_event_direction) * (close_location - 0.5) * 2.0).clip(lower=0.0)
    no_chase = (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
    settlement_quality = (
        aftershock_decay * controlled_volume * close_support * no_chase
    ).rolling(3, min_periods=2).mean()

    signal = _rank_cs(np.sign(recent_event_direction) * settlement_quality * recent_event_active)
    signal = _rank_cs(_cs_neutralize(signal, _rank_cs(gap)))
    signal = _rank_cs(_cs_neutralize(signal, ret20_rank))
    signal = _clean_panel(signal)

    states = _event_state_flags(panels, recent_event_active, settlement_quality)
    diagnostics = pd.DataFrame(
        {
            "component": [
                "material_gap",
                "recent_event_active",
                "aftershock_decay",
                "controlled_volume",
                "close_support",
                "no_chase",
                "settlement_quality",
                "final_signal",
            ],
            "finite_pct": [
                float(material_gap.notna().mean().mean()),
                float(recent_event_active.notna().mean().mean()),
                float(aftershock_decay.notna().mean().mean()),
                float(controlled_volume.notna().mean().mean()),
                float(close_support.notna().mean().mean()),
                float(no_chase.notna().mean().mean()),
                float(settlement_quality.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(material_gap.abs().mean().mean()),
                float(recent_event_active.abs().mean().mean()),
                float(aftershock_decay.abs().mean().mean()),
                float(controlled_volume.abs().mean().mean()),
                float(close_support.abs().mean().mean()),
                float(no_chase.abs().mean().mean()),
                float(settlement_quality.abs().mean().mean()),
                float(signal.abs().mean().mean()),
            ],
        }
    )
    return {SIGNAL_NAME: signal}, states, diagnostics


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    open_ = panels["open"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    gap = open_ / close.shift(1) - 1.0
    ret20 = close.pct_change(20, fill_method=None)
    gap_abs_rank = gap.abs().rank(axis=1, pct=True)
    material_gap = ((gap_abs_rank >= 0.80) & (gap.abs() >= 0.005)).astype(float)
    raw_gap_continuation = _rank_cs((np.sign(gap) * material_gap).rolling(3, min_periods=1).mean())
    raw_gap_reversal = _rank_cs((-np.sign(gap) * material_gap).rolling(3, min_periods=1).mean())
    volume_ratio = _safe_div(volume, volume.rolling(20, min_periods=10).mean()).clip(0.0, 5.0)
    gap_volume_continuation = _rank_cs((np.sign(gap) * material_gap * volume_ratio).rolling(3, min_periods=1).mean())
    refs["raw_gap_continuation"] = raw_gap_continuation.reindex(index=first.index, columns=first.columns)
    refs["raw_gap_reversal"] = raw_gap_reversal.reindex(index=first.index, columns=first.columns)
    refs["gap_volume_continuation"] = gap_volume_continuation.reindex(index=first.index, columns=first.columns)
    refs["price_rank_momentum_20"] = _rank_cs(ret20).reindex(index=first.index, columns=first.columns)
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
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    stress_counts = (
        stress.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    state_counts = (
        state_attr.groupby("signal_name")["mean_ic"]
        .agg(positive_state_count=lambda s: int((s > 0.004).sum()), best_state_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(
            h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]],
            on="signal_name",
            how="left",
        )
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(state_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.35:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.16:
            issues.append("high_turnover")
        if row["h20_mean_ic"] < 0.006:
            issues.append("weak_h20_ic")
        if row["positive_ic_rate"] < 0.52:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_inventory_corr", 0) > 0.45:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.50:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.50:
            issues.append("momentum_similarity_risk")
        if row.get("raw_gap_continuation_corr", 0) > 0.55:
            issues.append("raw_gap_continuation_similarity")
        if row.get("raw_gap_reversal_corr", 0) > 0.55:
            issues.append("raw_gap_reversal_similarity")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")

        if (
            row["h20_mean_ic"] > 0.014
            and row["h20_positive_ic_rate"] >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.12
            and row.get("active_date_ratio", 0) >= 0.10
            and row.get("max_inventory_corr", 1) <= 0.45
            and row.get("max_reversal_corr", 1) <= 0.50
            and row.get("raw_gap_continuation_corr", 1) <= 0.55
            and row.get("raw_gap_reversal_corr", 1) <= 0.55
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["h20_mean_ic"] > 0.008
            and row.get("positive_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.50
            and row.get("max_reversal_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.10
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_regime_count", 0) >= 2
            and row.get("positive_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.08
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "event_quality_persistence",
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h20_mean_ic": row["h20_mean_ic"],
                "h20_positive_ic_rate": row["h20_positive_ic_rate"],
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "raw_gap_continuation_corr": row.get("raw_gap_continuation_corr"),
                "raw_gap_reversal_corr": row.get("raw_gap_reversal_corr"),
                "gap_volume_continuation_corr": row.get("gap_volume_continuation_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "positive_state_count": int(row.get("positive_state_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "best_state_ic": row.get("best_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows)


def event_corr_summary(orth: pd.DataFrame) -> pd.DataFrame:
    summary = max_corr_table(orth)
    rows = []
    for name, group in orth.groupby("signal_name"):
        row = {"signal_name": name}
        for comparison in ["raw_gap_continuation", "raw_gap_reversal", "gap_volume_continuation"]:
            sample = group[group["comparison"].eq(comparison)]
            row[f"{comparison}_corr"] = float(sample["abs_value_corr"].max()) if not sample.empty else np.nan
        rows.append(row)
    event = pd.DataFrame(rows)
    return summary.merge(event, on="signal_name", how="left")


def _decision_text(decisions: pd.DataFrame) -> str:
    status = str(decisions.iloc[0]["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return (
            "`event_quality_persistence_after_gap_settlement` should move to formal conditional validation "
            "using this fixed formulation. Do not add a grid."
        )
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return (
            "`event_quality_persistence_after_gap_settlement` should receive a narrow refinement diagnostics pass only, "
            "focused on event-settlement timing, missingness, turnover, and raw-gap similarity."
        )
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return (
            "`event_quality_persistence_after_gap_settlement` should remain conditional-only research evidence. "
            "Do not advance until event-quality behavior separates more cleanly from raw gap baselines."
        )
    return (
        "`event_quality_persistence_after_gap_settlement` should be rejected in this formulation. "
        "Treat the result as evidence about event/gap mechanism viability before testing another concept."
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
    h20 = scores[scores["horizon"].eq(20)].copy()
    top_states = state_attr.sort_values("mean_ic", ascending=False).head(8)
    top_stress = stress.sort_values("mean_ic", ascending=False).head(8)
    lines = [
        "# Event Quality Persistence After Gap Settlement v1",
        "",
        "## Executive Takeaway",
        "",
        "This research-only run tested one simple formulation of `event_quality_persistence_after_gap_settlement` under the isolated run namespace `event_quality_persistence_after_gap_settlement_v1`.",
        "",
        "The formulation was designed to test whether event-quality stabilization after a recent gap/event can add a new Conditional Alpha Inventory dimension without becoming raw gap continuation, gap reversal, momentum, or reversal.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, or broad discovery was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v2 concept screen: `{SOURCE_NOTE}`",
        f"- Prior rejected dispersion concept: `{DISPERSION_NOTE}`",
        f"- Conditional Alpha Inventory reference: `{INVENTORY_NOTE}`",
        "- Volatility/stress inventory reference: `volatility_compression_after_stress_stabilization` primary `rebalance_5` panel.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | Some gap/event shocks settle into controlled range, stable volume, and supportive close behavior. That settlement quality may persist beyond the event without requiring raw gap continuation or reversal. |",
        "| Event/gap settlement logic | A material overnight gap must have occurred within the last five sessions. The event direction is carried only briefly to evaluate post-event settlement. |",
        "| Quality confirmation logic | Require aftershock range decay, controlled relative volume, close-location support in the event direction, and a no-chase guard. |",
        "| Persistence after settlement thesis | If settlement quality is orderly after the event, the event direction may retain conditional information at h5-h20. |",
        "| Difference from raw gap continuation | The score is not the gap sign alone; it requires post-event range, volume, close-location, and no-chase quality. |",
        "| Difference from gap reversal | The signal does not fade the gap; it asks whether the event direction survived settlement quality checks. |",
        "| Difference from current inventory | It is event-time based rather than participation/liquidity/breadth repair or volatility/stress stabilization. |",
        "| Expected activation semantics | Recent material gap plus orderly settlement quality. |",
        "| Expected horizon | h5-h20, with h20 monitored for inventory comparability. |",
        "| Expected turnover | Moderate, with event sparsity and churn as risks. |",
        "| Expected active coverage | Moderate to sparse. |",
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
        "## Stress / Regime Attribution",
        "",
        top_stress[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Event-State Attribution",
        "",
        top_states[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
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
        f"- Genuinely event-quality persistence: assessed through `EVENT_AND_HIGH_QUALITY` behavior and raw-gap baseline correlations. Raw gap continuation/reversal correlations were `{decision['raw_gap_continuation_corr']:.6f}` / `{decision['raw_gap_reversal_corr']:.6f}`.",
        f"- Momentum/reversal proxy risk: max reversal/momentum correlations were `{decision['max_reversal_corr']:.6f}` / `{decision['max_momentum_corr']:.6f}`.",
        f"- Inventory overlap risk: max inventory correlation was `{decision['max_inventory_corr']:.6f}`.",
        f"- Sparse activation risk: active date ratio was `{decision['active_date_ratio']:.6f}`.",
        f"- Turnover risk: turnover proxy was `{decision['turnover_proxy']:.6f}`.",
        f"- Directional stability: WFV-style persistence/sign consistency were `{decision['wfv_persistence']}` / `{decision['wfv_sign_consistency']}`.",
        "",
        "## Recommended Next Step",
        "",
        _decision_text(decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states, component_diagnostics = build_event_quality_signal(panels)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "event_quality_persistence",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V2_RESEARCH_ONLY",
                "mechanism_thesis": "Recent material gap followed by orderly settlement quality and short-lived direction persistence.",
                "state_transition_logic": "Gap/event shock followed by range aftershock decay, controlled volume, supportive close location, and no-chase behavior.",
                "differs_from_inventory": "Event-time mechanism rather than participation/liquidity/breadth repair or volatility/stress stabilization.",
                "differs_from_reversal_momentum": "Neutralizes raw gap and h20 price-rank exposure; requires settlement quality rather than fading or chasing.",
                "expected_activation_state": "RECENT_EVENT_ACTIVE_AND_HIGH_SETTLEMENT_QUALITY",
                "expected_horizon": "h5-h20",
                "expected_turnover_profile": "moderate",
                "expected_active_coverage": "moderate_to_sparse",
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
    orth_summary = event_corr_summary(orth)
    active = active_coverage_summary(signals)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidate(structural, scores, wfv_summary, stress, state_attr, orth_summary, active)

    artifact_files = [
        "candidate_registry.csv",
        "component_diagnostics.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "event_state_flags.csv",
        "stress_regime_attribution.csv",
        "event_state_attribution.csv",
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
    states.to_csv(OUT_DIR / "event_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "event_state_attribution.csv", index=False)
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
                "prior_rejected_dispersion_note": str(DISPERSION_NOTE),
                "source_inventory_note": str(INVENTORY_NOTE),
                "candidate_count": 1,
                "candidate_names": [SIGNAL_NAME],
                "one_simple_formulation": True,
                "parameter_grid": False,
                "broad_discovery": False,
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
