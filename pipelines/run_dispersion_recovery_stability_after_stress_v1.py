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


RUN_ID = "dispersion_recovery_stability_after_stress_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/dispersion_recovery_stability_after_stress_v1.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md")
INVENTORY_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v1.md")
VOLATILITY_INVENTORY_PATH = Path(
    "artifacts/research/volatility_compression_stress_stabilization_conditional_validation_v1/"
    "rebalance_5_signal_panel.parquet"
)

SIGNAL_NAME = "dispersion_recovery_stability_after_stress"
HORIZONS = (1, 5, 10, 20)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _build_state_flags(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> pd.DataFrame:
    close = panels["close"]
    ret1 = close.pct_change(1, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    benchmark_ret = benchmark.pct_change(1, fill_method=None)
    benchmark_vol20 = benchmark_ret.rolling(20, min_periods=15).std()
    benchmark_vol60 = benchmark_ret.rolling(60, min_periods=40).std()
    stress = build_stress_states(close, benchmark)

    dispersion20 = ret20.std(axis=1)
    dispersion20_mean60 = dispersion20.rolling(60, min_periods=40).mean()
    dispersion_recent_peak = dispersion20.rolling(20, min_periods=10).max()
    dispersion_elevated_recent = dispersion_recent_peak > _rolling_quantile(dispersion20, 0.75)
    dispersion_normalizing = (dispersion20 < dispersion20_mean60) & (dispersion20.diff(10) < 0)
    dispersion_recovery = (dispersion_elevated_recent & dispersion_normalizing).fillna(False)

    stress_recent = (
        stress[["volatility_spike", "panic_liquidity_stress", "drawdown_acceleration"]]
        .rolling(20, min_periods=1)
        .max()
        .max(axis=1)
        .astype(bool)
    )
    volatility_normalizing = ((benchmark_vol20 < benchmark_vol60) & (benchmark_vol20.diff(10) < 0)).fillna(False)
    stress_then_dispersion_recovery = (stress_recent & dispersion_recovery).fillna(False)

    states = pd.DataFrame(index=close.index)
    states["STRESS_RECENT"] = stress_recent
    states["DISPERSION_ELEVATED_RECENT"] = dispersion_elevated_recent.fillna(False)
    states["DISPERSION_NORMALIZING"] = dispersion_normalizing.fillna(False)
    states["DISPERSION_RECOVERY"] = dispersion_recovery
    states["VOLATILITY_NORMALIZING"] = volatility_normalizing
    states["STRESS_THEN_DISPERSION_RECOVERY"] = stress_then_dispersion_recovery
    states["STRESS_RECENT_NO_DISPERSION_RECOVERY"] = (stress_recent & ~dispersion_recovery).fillna(False)
    states["DISPERSION_RECOVERY_NO_STRESS"] = (dispersion_recovery & ~stress_recent).fillna(False)
    for column in stress.columns:
        states[column] = stress[column].fillna(False)
    return states


def build_dispersion_recovery_signal(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    ret1 = close.pct_change(1, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    ret20_rank = _rank_cs(ret20)
    states = _build_state_flags(panels, benchmark)
    active_gate = _market_state_panel(states["STRESS_THEN_DISPERSION_RECOVERY"], close.columns)

    rank20 = ret20.rank(axis=1, pct=True)
    rank_churn20 = rank20.diff().abs().rolling(20, min_periods=12).mean()
    rank_stability = (1.0 - rank_churn20.rank(axis=1, pct=True)).clip(lower=0.0)

    idio_ret = ret1.sub(ret1.mean(axis=1), axis=0)
    idio_vol20 = idio_ret.rolling(20, min_periods=15).std()
    idio_vol60 = idio_ret.rolling(60, min_periods=40).std()
    idio_vol_repair = (1.0 - _safe_div(idio_vol20, idio_vol60).rank(axis=1, pct=True)).clip(lower=0.0)

    neutral_rank_level = (1.0 - ret60.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
    topology_score = (rank_stability * idio_vol_repair * neutral_rank_level).rolling(5, min_periods=3).mean()
    signal = _rank_cs(topology_score)
    signal = _rank_cs(_cs_neutralize(signal, ret20_rank))
    signal = _rank_cs(signal * active_gate)
    signal = _rank_cs(_rebalance_interval(signal, 10))

    diagnostics = pd.DataFrame(
        {
            "component": [
                "rank_stability",
                "idio_vol_repair",
                "neutral_rank_level",
                "active_gate",
                "final_signal",
            ],
            "finite_pct": [
                float(rank_stability.notna().mean().mean()),
                float(idio_vol_repair.notna().mean().mean()),
                float(neutral_rank_level.notna().mean().mean()),
                float(active_gate.notna().mean().mean()),
                float(signal.notna().mean().mean()),
            ],
            "mean_abs": [
                float(rank_stability.abs().mean().mean()),
                float(idio_vol_repair.abs().mean().mean()),
                float(neutral_rank_level.abs().mean().mean()),
                float(active_gate.abs().mean().mean()),
                float(signal.abs().mean().mean()),
            ],
        }
    )
    return {SIGNAL_NAME: _clean_panel(signal)}, states, diagnostics


def reference_panels(
    signals: dict[str, pd.DataFrame],
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
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


def max_corr_table(orth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in orth.groupby("signal_name"):
        group = group.dropna(subset=["abs_value_corr"])
        if group.empty:
            continue
        top = group.loc[group["abs_value_corr"].idxmax()]
        liquidity = group[group["comparison"].eq("inventory_participation_liquidity_state_shift_20_60")]
        breadth = group[group["comparison"].eq("inventory_participation_breadth_repair_under_hostile_trend")]
        volatility = group[group["comparison"].eq("inventory_volatility_compression_after_stress_stabilization")]
        reversal = group[group["comparison"].isin(["unweighted_reversal_20", "plain_smoothed_reversal_20"])]
        momentum = group[group["comparison"].isin(["plain_momentum_60"])]
        inventory_corrs = pd.concat(
            [
                liquidity["abs_value_corr"],
                breadth["abs_value_corr"],
                volatility["abs_value_corr"],
            ]
        )
        rows.append(
            {
                "signal_name": name,
                "top_comparison": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "inventory_liquidity_corr": float(liquidity["abs_value_corr"].max()) if not liquidity.empty else np.nan,
                "inventory_breadth_corr": float(breadth["abs_value_corr"].max()) if not breadth.empty else np.nan,
                "inventory_volatility_corr": float(volatility["abs_value_corr"].max()) if not volatility.empty else np.nan,
                "max_inventory_corr": float(inventory_corrs.max()) if not inventory_corrs.empty else np.nan,
                "max_reversal_corr": float(reversal["abs_value_corr"].max()) if not reversal.empty else np.nan,
                "max_momentum_corr": float(momentum["abs_value_corr"].max()) if not momentum.empty else np.nan,
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
        .agg(
            positive_regime_count=lambda s: int((s > 0.004).sum()),
            best_regime_ic="max",
        )
        .reset_index()
    )
    state_counts = (
        state_attr.groupby("signal_name")["mean_ic"]
        .agg(
            positive_state_count=lambda s: int((s > 0.004).sum()),
            best_state_ic="max",
        )
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
        if row.get("active_date_ratio", 1) < 0.12:
            issues.append("sparse_activation")

        if (
            row["h20_mean_ic"] > 0.014
            and row["h20_positive_ic_rate"] >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.12
            and row.get("active_date_ratio", 0) >= 0.15
            and row.get("max_inventory_corr", 1) <= 0.45
            and row.get("max_reversal_corr", 1) <= 0.50
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["h20_mean_ic"] > 0.008
            and row.get("positive_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.50
            and row.get("max_reversal_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.12
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_regime_count", 0) >= 2
            and row.get("positive_state_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.10
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": "dispersion_recovery_topology",
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


def _decision_text(decisions: pd.DataFrame) -> str:
    status = str(decisions.iloc[0]["status"])
    if status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        return (
            "`dispersion_recovery_stability_after_stress` should move to a formal conditional-validation pass "
            "using this fixed formulation as the primary candidate. Do not add a parameter grid."
        )
    if status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        return (
            "`dispersion_recovery_stability_after_stress` should receive a narrow refinement diagnostics pass only. "
            "Any refinement should focus on activation coverage, rank-churn control, and dispersion-vs-volatility separation."
        )
    if status == "CONDITIONAL_ONLY_RESEARCH":
        return (
            "`dispersion_recovery_stability_after_stress` contains conditional evidence but should remain research-only. "
            "Do not advance until a clearer active-state thesis is shown."
        )
    return (
        "`dispersion_recovery_stability_after_stress` should be rejected in this formulation. Treat the result as evidence "
        "about dispersion recovery topology before considering a different concept."
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
    h20 = scores[scores["horizon"].eq(20)].copy()
    top_states = state_attr.sort_values("mean_ic", ascending=False).head(8)
    top_stress = stress.sort_values("mean_ic", ascending=False).head(8)
    decision = decisions.iloc[0]
    lines = [
        "# Dispersion Recovery Stability After Stress v1",
        "",
        "## Executive Takeaway",
        "",
        "This research-only run tested one simple formulation of `dispersion_recovery_stability_after_stress` under the isolated run namespace `dispersion_recovery_stability_after_stress_v1`.",
        "",
        "The formulation was designed to test whether dispersion recovery topology after stress can add a new Conditional Alpha Inventory dimension beyond participation/liquidity/breadth repair and volatility/stress stabilization.",
        "",
        f"Final classification: `{decision['status']}`",
        f"Primary review issues: `{decision['review_issues']}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or broad discovery was performed.",
        "",
        "## Source Context",
        "",
        f"- Expansion v2 concept screen: `{SOURCE_NOTE}`",
        f"- Conditional Alpha Inventory reference: `{INVENTORY_NOTE}`",
        "- Volatility/stress inventory reference: `volatility_compression_after_stress_stabilization` primary `rebalance_5` panel.",
        "",
        "## Mechanism Definition",
        "",
        "| Field | Definition |",
        "| --- | --- |",
        "| Mechanism thesis | After stress, elevated cross-sectional dispersion that begins to normalize may create a cleaner stock-selection topology. Names with stable ranks and repaired idiosyncratic volatility, without price-rank extension, may carry useful conditional information. |",
        "| Dispersion recovery logic | Market-level 20-day return dispersion must have been elevated recently and must be normalizing versus its 60-day mean with negative 10-day dispersion change. |",
        "| Stress-state precondition | The dispersion recovery state must follow recent volatility spike, panic/liquidity stress, or drawdown acceleration. |",
        "| Stability confirmation logic | Combine low 20-day rank churn, improving idiosyncratic volatility repair, and neutral 60-day price-rank level. |",
        "| Inactive-date handling | Inactive dates are neutralized through a zero gate and then cross-sectionally reranked, consistent with prior conditional research conventions. |",
        "| Turnover control | A simple 10-day rebalance hold is used to reduce rank churn without adding a parameter grid. |",
        "| Expected horizon | h10-h20, with h20 as the primary evaluation horizon. |",
        "| Expected turnover | Low to moderate. |",
        "| Expected active coverage | Moderate; too-sparse activation is a rejection risk. |",
        "",
        "## Why This Differs From Current Inventory",
        "",
        "- It does not use participation repair, liquidity repair, or weak-breadth repair as the primary mechanism.",
        "- It does not rely only on volatility compression after stress; dispersion recovery is the required topology state.",
        "- It explicitly neutralizes price-rank extension to reduce momentum/reversal manifold collapse.",
        "- It tests cross-sectional order and stability after stress, not just stress stabilization itself.",
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
        "## Dispersion-State Attribution",
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
        f"- Genuinely dispersion-recovery topology: assessed through `STRESS_THEN_DISPERSION_RECOVERY` active-state sample behavior and similarity to the current inventory. Max inventory correlation was `{decision['max_inventory_corr']:.6f}`.",
        f"- Volatility/stress proxy risk: monitored through the direct similarity reference to `inventory_volatility_compression_after_stress_stabilization`; see the orthogonality table.",
        f"- Participation/breadth repair risk: monitored through direct similarity references to the two participation/breadth inventory candidates; see the orthogonality table.",
        f"- Sparse activation risk: active date ratio was `{decision['active_date_ratio']:.6f}`.",
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
    signals, states, component_diagnostics = build_dispersion_recovery_signal(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": SIGNAL_NAME,
                "family": "dispersion_recovery_topology",
                "run_id": RUN_ID,
                "research_status": "TRACK_B_EXPANSION_V2_RESEARCH_ONLY",
                "mechanism_thesis": "Stress-conditioned dispersion recovery with rank-stability and idiosyncratic-volatility repair.",
                "state_transition_logic": "Recent stress plus recent elevated dispersion followed by dispersion normalization.",
                "differs_from_inventory": "Tests cross-sectional dispersion topology instead of participation/liquidity/breadth repair or pure volatility compression.",
                "differs_from_reversal_momentum": "Neutralizes price-rank extension and does not fade or chase prior returns.",
                "expected_activation_state": "STRESS_THEN_DISPERSION_RECOVERY",
                "expected_horizon": "h10-h20",
                "expected_turnover_profile": "low_to_moderate",
                "expected_active_coverage": "moderate",
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
    orth_summary = max_corr_table(orth)
    active = active_coverage_summary(signals)
    sample_sizes = sample_size_summary(states, signals)
    decisions = classify_candidate(structural, scores, wfv_summary, stress, state_attr, orth_summary, active)

    artifact_files = [
        "candidate_registry.csv",
        "component_diagnostics.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "market_state_flags.csv",
        "stress_regime_attribution.csv",
        "dispersion_state_attribution.csv",
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
    states.to_csv(OUT_DIR / "market_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "dispersion_state_attribution.csv", index=False)
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
