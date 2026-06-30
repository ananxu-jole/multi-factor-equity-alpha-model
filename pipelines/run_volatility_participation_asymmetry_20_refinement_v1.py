from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_structural_interaction_alpha_discovery_batch_v1 import (
    HORIZONS,
    RESEARCH_ONLY_GUARDRAIL,
    _active_coverage_summary,
    _clean_panel,
    _finalize_signal,
    _market_state_panel,
    _max_corr_table,
    _rank_cs,
    build_candidate_panels,
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


RUN_ID = "volatility_participation_asymmetry_20_refinement_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/volatility_participation_asymmetry_20_refinement_v1.md")
SOURCE_RUN_ID = "structural_interaction_alpha_discovery_batch_v1"
SOURCE_SIGNAL = "volatility_participation_asymmetry_20"


VARIANT_SPECS = [
    {
        "signal_name": "volatility_participation_asymmetry_20_original",
        "variant_type": "source_formula",
        "description": "Original structural interaction batch formulation.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_participation_q60",
        "variant_type": "participation_tightening",
        "description": "Require clearer up/down participation asymmetry while preserving original stabilization logic.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_vol_stab_q60",
        "variant_type": "volatility_confirmation",
        "description": "Require stronger volatility stabilization confirmation while preserving original participation logic.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_dual_q55",
        "variant_type": "dual_confirmation",
        "description": "Require both participation asymmetry and volatility stabilization to be above modest confirmation levels.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_dual_close_q55",
        "variant_type": "quality_activation",
        "description": "Add close-location quality to the dual confirmation filter.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_balanced_selective_q60",
        "variant_type": "balanced_selectivity",
        "description": "Require the combined raw interaction score to sit above a moderate cross-sectional selectivity threshold.",
    },
    {
        "signal_name": "volatility_participation_asymmetry_20_rebalance_20_dual_q55",
        "variant_type": "low_churn_dual_confirmation",
        "description": "Use dual confirmation with slower rebalance to test whether reduced churn preserves structure.",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _row_quantile_mask(panel: pd.DataFrame, q: float) -> pd.DataFrame:
    threshold = panel.quantile(q, axis=1)
    return panel.ge(threshold, axis=0)


def _variant_metadata() -> pd.DataFrame:
    rows = []
    for spec in VARIANT_SPECS:
        row = dict(spec)
        row["run_id"] = RUN_ID
        row["source_signal"] = SOURCE_SIGNAL
        row["research_status"] = "RESEARCH_ONLY_REFINEMENT"
        rows.append(row)
    return pd.DataFrame(rows)


def build_refinement_variants(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, pd.DataFrame]], pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    source_signals, source_components, source_states, stress = build_candidate_panels(panels, benchmark)
    components = source_components[SOURCE_SIGNAL]

    volatility_stabilization = components["volatility_stabilization"]
    participation_asymmetry = components["participation_asymmetry"]
    close_support = components["close_support"]
    low_extension = components["low_extension"]
    raw = volatility_stabilization * participation_asymmetry * close_support * low_extension

    source_stress = build_stress_states(close, benchmark)
    broad_stress = source_stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    recent_stress = broad_stress.rolling(20, min_periods=1).max().astype(bool)
    active_stress_panel = _market_state_panel(recent_stress, close.columns)

    ret5 = close.pct_change(5, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    exposures = [_rank_cs(ret5), _rank_cs(ret20), _rank_cs(ret60), _rank_cs(-ret5), _rank_cs(-ret20)]

    masks = {
        "volatility_participation_asymmetry_20_original": raw.notna() & raw.gt(0) & active_stress_panel.astype(bool),
        "volatility_participation_asymmetry_20_participation_q60": (
            raw.notna() & participation_asymmetry.gt(0.60) & active_stress_panel.astype(bool)
        ),
        "volatility_participation_asymmetry_20_vol_stab_q60": (
            raw.notna() & volatility_stabilization.gt(0.60) & active_stress_panel.astype(bool)
        ),
        "volatility_participation_asymmetry_20_dual_q55": (
            raw.notna()
            & participation_asymmetry.gt(0.55)
            & volatility_stabilization.gt(0.55)
            & active_stress_panel.astype(bool)
        ),
        "volatility_participation_asymmetry_20_dual_close_q55": (
            raw.notna()
            & participation_asymmetry.gt(0.55)
            & volatility_stabilization.gt(0.55)
            & close_support.gt(0.55)
            & active_stress_panel.astype(bool)
        ),
        "volatility_participation_asymmetry_20_balanced_selective_q60": (
            raw.notna() & _row_quantile_mask(raw, 0.60) & active_stress_panel.astype(bool)
        ),
        "volatility_participation_asymmetry_20_rebalance_20_dual_q55": (
            raw.notna()
            & participation_asymmetry.gt(0.55)
            & volatility_stabilization.gt(0.55)
            & active_stress_panel.astype(bool)
        ),
    }

    signals: dict[str, pd.DataFrame] = {}
    components_by_variant: dict[str, dict[str, pd.DataFrame]] = {}
    for spec in VARIANT_SPECS:
        name = spec["signal_name"]
        rebalance = 20 if name.endswith("rebalance_20_dual_q55") else 10
        signal = _finalize_signal(raw, masks[name], exposures, rebalance=rebalance)
        signals[name] = _clean_panel(signal)
        components_by_variant[name] = {
            "volatility_stabilization": volatility_stabilization.where(masks[name]),
            "participation_asymmetry": participation_asymmetry.where(masks[name]),
            "close_support": close_support.where(masks[name]),
            "low_extension": low_extension.where(masks[name]),
            "activation_filter": masks[name].astype(float),
        }

    states = source_states.copy()
    states["REFINEMENT_ACTIVE_STRESS"] = recent_stress.reindex(states.index).fillna(False)
    return signals, components_by_variant, states, stress


def original_vs_refined(scores: pd.DataFrame, active: pd.DataFrame, interaction: pd.DataFrame, fragility: pd.DataFrame) -> pd.DataFrame:
    h10 = scores[scores["horizon"].eq(10)][["signal_name", "mean_ic", "positive_ic_rate"]].rename(
        columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"}
    )
    h20 = scores[scores["horizon"].eq(20)][["signal_name", "mean_ic", "positive_ic_rate"]].rename(
        columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"}
    )
    best = scores[scores["is_best_horizon"]][
        ["signal_name", "horizon", "mean_ic", "positive_ic_rate", "n_dates"]
    ].rename(columns={"horizon": "best_horizon", "mean_ic": "best_mean_ic", "positive_ic_rate": "best_positive_ic_rate"})
    out = (
        best.merge(h10, on="signal_name", how="left")
        .merge(h20, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(
            interaction[
                [
                    "signal_name",
                    "interaction_decomposition_label",
                    "dominant_component",
                    "dominant_component_corr",
                    "interaction_ic_lift_vs_best_component",
                ]
            ],
            on="signal_name",
            how="left",
        )
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
    )
    original = out[out["signal_name"].eq("volatility_participation_asymmetry_20_original")]
    if not original.empty:
        original_active = float(original["active_date_ratio"].iloc[0])
        original_h20 = float(original["h20_mean_ic"].iloc[0])
        original_h10 = float(original["h10_mean_ic"].iloc[0])
        out["active_ratio_delta_vs_original"] = out["active_date_ratio"] - original_active
        out["h20_mean_ic_delta_vs_original"] = out["h20_mean_ic"] - original_h20
        out["h10_mean_ic_delta_vs_original"] = out["h10_mean_ic"] - original_h10
    return out


def activation_filter_summary(components: dict[str, dict[str, pd.DataFrame]]) -> pd.DataFrame:
    rows = []
    for signal_name, comp in components.items():
        mask = comp["activation_filter"].astype(float)
        date_coverage = mask.gt(0).mean(axis=1)
        active_dates = date_coverage.gt(0)
        material_active_dates = date_coverage.gt(0.05)
        rows.append(
            {
                "signal_name": signal_name,
                "raw_filter_active_dates": int(active_dates.sum()),
                "raw_filter_active_date_ratio": float(active_dates.mean()),
                "raw_filter_material_active_dates": int(material_active_dates.sum()),
                "raw_filter_material_active_date_ratio": float(material_active_dates.mean()),
                "mean_raw_filter_coverage": float(date_coverage[active_dates].mean()) if active_dates.any() else np.nan,
                "median_raw_filter_coverage": float(date_coverage[active_dates].median()) if active_dates.any() else np.nan,
                "p95_raw_filter_coverage": float(date_coverage[active_dates].quantile(0.95)) if active_dates.any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def classify_variants(
    comparison: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    activation: pd.DataFrame,
) -> pd.DataFrame:
    summary = comparison.merge(wfv, left_on=["signal_name", "best_horizon"], right_on=["signal_name", "horizon"], how="left")
    summary = summary.merge(orth_summary, on="signal_name", how="left")
    summary = summary.merge(activation, on="signal_name", how="left")
    original = summary[summary["signal_name"].eq("volatility_participation_asymmetry_20_original")]
    original_coverage = float(original["mean_raw_filter_coverage"].iloc[0]) if not original.empty else np.nan
    original_material_dates = float(original["raw_filter_material_active_date_ratio"].iloc[0]) if not original.empty else np.nan
    rows = []
    for _, row in summary.iterrows():
        issues = []
        panel_active = row.get("active_date_ratio", np.nan)
        raw_coverage = row.get("mean_raw_filter_coverage", np.nan)
        raw_material_dates = row.get("raw_filter_material_active_date_ratio", np.nan)
        if pd.notna(raw_coverage) and raw_coverage > 0.55:
            issues.append("raw_filter_too_broad")
        if pd.notna(panel_active) and panel_active < 0.10:
            issues.append("activation_too_sparse")
        if pd.notna(raw_material_dates) and raw_material_dates < 0.10:
            issues.append("raw_filter_too_sparse")
        if row.get("h20_mean_ic", -np.inf) < 0.010:
            issues.append("h20_not_preserved")
        if row.get("h10_mean_ic", -np.inf) < 0.004:
            issues.append("weak_h10_support")
        if row.get("best_mean_ic", -np.inf) < 0.010:
            issues.append("weak_best_horizon_ic")
        if row.get("best_positive_ic_rate", 0) < 0.55:
            issues.append("weak_positive_ic_rate")
        if row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("one_window_dominance", 1) > 0.60:
            issues.append("one_window_concentration")
        if row.get("max_inventory_corr", 0) > 0.30:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.30:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.30:
            issues.append("momentum_similarity_risk")
        if row.get("interaction_decomposition_label") != "true_interaction_behavior":
            issues.append("interaction_not_preserved")
        if row.get("stress_only_dependency_flag", False):
            issues.append("stress_only_dependency")
        if row.get("crisis_concentration_flag", False):
            issues.append("crisis_concentration")
        if row.get("one_window_concentration_flag", False):
            issues.append("one_window_concentration_flag")

        coverage_improved = (
            pd.notna(original_coverage)
            and pd.notna(raw_coverage)
            and raw_coverage <= original_coverage - 0.10
        )
        material_dates_preserved = (
            pd.isna(original_material_dates)
            or pd.isna(raw_material_dates)
            or raw_material_dates >= max(0.10, original_material_dates * 0.50)
        )
        activation_improved = coverage_improved and material_dates_preserved
        validation_ready = (
            row.get("h20_mean_ic", 0) >= 0.015
            and row.get("h10_mean_ic", 0) >= 0.008
            and row.get("best_positive_ic_rate", 0) >= 0.57
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and 0.10 <= row.get("raw_filter_material_active_date_ratio", 0) <= 0.75
            and row.get("mean_raw_filter_coverage", 1) <= 0.50
            and row.get("interaction_decomposition_label") == "true_interaction_behavior"
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_reversal_corr", 1) <= 0.30
            and row.get("max_momentum_corr", 1) <= 0.30
            and not row.get("stress_only_dependency_flag", True)
            and not row.get("crisis_concentration_flag", True)
        )
        refinement_ready = (
            row.get("h20_mean_ic", 0) >= 0.010
            and row.get("h10_mean_ic", 0) >= 0.004
            and row.get("best_positive_ic_rate", 0) >= 0.55
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("interaction_decomposition_label") == "true_interaction_behavior"
            and not row.get("crisis_concentration_flag", True)
        )
        if validation_ready:
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif refinement_ready and activation_improved:
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif refinement_ready:
            status = "CONDITIONAL_ONLY_RESEARCH"
            issues.append("activation_not_improved_enough")
        elif row.get("best_mean_ic", -np.inf) < 0:
            status = "REJECT_RESEARCH"
        else:
            status = "CONDITIONAL_ONLY_RESEARCH"
        out = row.to_dict()
        out["status"] = status
        out["review_issues"] = "; ".join(dict.fromkeys(issues))
        rows.append(out)
    return pd.DataFrame(rows)


def write_note(
    metadata: pd.DataFrame,
    scores: pd.DataFrame,
    comparison: pd.DataFrame,
    decisions: pd.DataFrame,
    interaction: pd.DataFrame,
    fragility: pd.DataFrame,
    orth_summary: pd.DataFrame,
    activation: pd.DataFrame,
) -> None:
    best = decisions.sort_values(
        ["status", "h20_mean_ic", "active_date_ratio"],
        ascending=[True, False, True],
    )
    live = decisions[decisions["status"].eq("CONDITIONAL_REFINEMENT_CANDIDATE")]
    if not live.empty:
        best_name = live.sort_values(["h20_mean_ic", "h10_mean_ic"], ascending=False)["signal_name"].iloc[0]
    else:
        best_name = decisions.sort_values(["h20_mean_ic", "h10_mean_ic"], ascending=False)["signal_name"].iloc[0]
    best_row = decisions[decisions["signal_name"].eq(best_name)].iloc[0]

    lines = [
        "# Volatility Participation Asymmetry 20 Refinement v1",
        "",
        "Date: 2026-05-22",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        "Status: RESEARCH_ONLY_REFINEMENT_PASS",
        "",
        "## Research-Only Guardrail",
        "",
        RESEARCH_ONLY_GUARDRAIL,
        "",
        "This pass refines only `volatility_participation_asymmetry_20`. It does not touch the three CONDITIONAL_ONLY_RESEARCH candidates from the structural interaction batch.",
        "",
        "## Objective",
        "",
        "Reduce broad activation while preserving h20 behavior, h10 support, WFV persistence, true interaction structure, low inventory overlap, and reversal/momentum separation.",
        "",
        "## Executive Takeaway",
        "",
        f"Variants tested: `{len(metadata)}`",
        "",
        f"Best refined variant: `{best_name}`",
        "",
        f"Conservative classification: `{best_row['status']}`",
        "",
        f"h10 mean IC: `{best_row['h10_mean_ic']:.6f}`",
        "",
        f"h20 mean IC: `{best_row['h20_mean_ic']:.6f}`",
        "",
        f"Active date ratio: `{best_row['active_date_ratio']:.6f}`",
        "",
        f"Mean raw activation-filter coverage: `{best_row['mean_raw_filter_coverage']:.6f}`",
        "",
        f"Interaction label: `{best_row['interaction_decomposition_label']}`",
        "",
        "## Variants",
        "",
        metadata.to_markdown(index=False),
        "",
        "## Original Vs Refined Comparison",
        "",
        comparison[
            [
                "signal_name",
                "best_horizon",
                "best_mean_ic",
                "h10_mean_ic",
                "h20_mean_ic",
                "active_date_ratio",
                "active_ratio_delta_vs_original",
                "interaction_decomposition_label",
            ]
        ].to_markdown(index=False),
        "",
        "## Raw Activation Filter Summary",
        "",
        activation.to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores.to_markdown(index=False),
        "",
        "## Interaction Decomposition",
        "",
        interaction.to_markdown(index=False),
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
        decisions[
            [
                "signal_name",
                "status",
                "best_horizon",
                "best_mean_ic",
                "h10_mean_ic",
                "h20_mean_ic",
                "active_date_ratio",
                "mean_raw_filter_coverage",
                "raw_filter_material_active_date_ratio",
                "max_inventory_corr",
                "max_reversal_corr",
                "max_momentum_corr",
                "review_issues",
            ]
        ].to_markdown(index=False),
        "",
        "## Recommendation",
        "",
    ]
    if best_row["status"] == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        lines.append("Treat the best variant as a future conditional-validation candidate only after independent governance review. Do not promote from this refinement pass alone.")
    elif best_row["status"] == "CONDITIONAL_REFINEMENT_CANDIDATE":
        lines.append("Keep the best variant as a refinement candidate. It improved selectivity enough to remain live, but it is not validation-ready from this pass alone.")
    else:
        lines.append("Do not advance to validation. Preserve the artifacts for research history and consider a separate redesign only if future inventory monitoring supports it.")
    lines.extend(
        [
            "",
            "No production registration, survivor/watchlist mutation, detector modification, schema/gate/governance change, or portfolio/ML/blending/optimization route was made.",
            "",
        ]
    )
    NOTE_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    close = panels["close"]
    signals, components, states, stress = build_refinement_variants(panels, benchmark)

    metadata = _variant_metadata()
    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, close)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_attr = stress_attribution(daily_ics, scores, stress)
    state_attr = state_attribution(daily_ics, scores, states)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = _active_coverage_summary(signals)
    activation = activation_filter_summary(components)
    interaction = interaction_component_summary(signals, components, close, scores)
    fragility = fragility_concentration_summary(daily_ics, scores, stress, wfv_summary)
    comparison = original_vs_refined(scores, active, interaction, fragility)
    decisions = classify_variants(comparison, wfv_summary, orth_summary, activation)

    metadata.to_csv(OUT_DIR / "variant_metadata.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scores.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_variant_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_windows.csv", index=False)
    stress_attr.to_csv(OUT_DIR / "stress_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "candidate_state_attribution.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    activation.to_csv(OUT_DIR / "activation_filter_summary.csv", index=False)
    interaction.to_csv(OUT_DIR / "interaction_component_summary.csv", index=False)
    fragility.to_csv(OUT_DIR / "fragility_concentration_summary.csv", index=False)
    comparison.to_csv(OUT_DIR / "original_vs_refined_comparison.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decision_summary.csv", index=False)
    states.to_csv(OUT_DIR / "market_state_flags.csv", index=True)
    for name, panel in signals.items():
        panel.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")

    manifest = {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_signal": SOURCE_SIGNAL,
        "status": "RESEARCH_ONLY_REFINEMENT_PASS",
        "variant_count": len(signals),
        "variant_names": list(signals),
        "artifact_files": sorted(path.name for path in OUT_DIR.iterdir() if path.is_file()),
        "production_registration_changed": False,
        "survivor_watchlist_changed": False,
        "detector_modified": False,
        "detector_used_as_conditioning_input": False,
        "gates_schemas_governance_changed": False,
        "portfolio_ml_blending_optimization_route_changed": False,
        "touched_conditional_only_candidates": False,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_note(metadata, scores, comparison, decisions, interaction, fragility, orth_summary, activation)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions[["signal_name", "status", "best_horizon", "best_mean_ic", "h10_mean_ic", "h20_mean_ic", "active_date_ratio", "review_issues"]].to_string(index=False))


if __name__ == "__main__":
    main()
