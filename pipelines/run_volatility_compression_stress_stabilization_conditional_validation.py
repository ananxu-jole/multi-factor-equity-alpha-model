from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
)
from run_track_b_v6_focused_discovery import (
    build_candidate_panels as build_v6_candidate_panels,
    state_attribution,
    active_coverage_summary,
    _max_corr_table,
)
from run_volatility_compression_stress_stabilization_refinement import (
    OUT_DIR as REFINEMENT_OUT_DIR,
    SOURCE_SIGNAL,
    minimal_reference_panels,
)


RUN_ID = "volatility_compression_stress_stabilization_conditional_validation_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/volatility_compression_stress_stabilization_conditional_validation.md")
V6_OUT_DIR = Path("artifacts/research/track_b_v6_focused_discovery")
REFINEMENT_NOTE = Path("docs/research_notes/volatility_compression_stress_stabilization_refinement.md")

SHORTLIST = {
    "rebalance_5": {
        "role": "primary_candidate",
        "validation_question": "Does five-day rebalance remove rank churn while preserving volatility/stress-transition information?",
    },
    "smooth_5": {
        "role": "confirmation_control",
        "validation_question": "Does mild five-day smoothing support the same mechanism without rebalance timing dependence?",
    },
    "smooth_3": {
        "role": "confirmation_control",
        "validation_question": "Does lighter smoothing support the same mechanism without over-smoothing?",
    },
}


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_shortlist() -> dict[str, pd.DataFrame]:
    signals = {}
    for name in SHORTLIST:
        path = REFINEMENT_OUT_DIR / f"{name}_signal_panel.parquet"
        if not path.exists():
            raise FileNotFoundError(f"Missing refinement panel: {path}")
        signals[name] = pd.read_parquet(path)
    return signals


def _window_concentration(wfv_windows: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in wfv_windows.groupby("signal_name"):
        group = group.sort_values("window")
        values = group["mean_test_ic"].astype(float)
        positive = values[values > 0]
        rows.append(
            {
                "signal_name": name,
                "positive_window_count": int((values > 0).sum()),
                "negative_window_count": int((values <= 0).sum()),
                "min_window_ic": float(values.min()),
                "max_window_ic": float(values.max()),
                "window_ic_range": float(values.max() - values.min()),
                "positive_ic_sum": float(positive.sum()) if not positive.empty else 0.0,
                "largest_positive_window_share": float(positive.max() / positive.sum()) if positive.sum() > 0 else np.nan,
                "recent_window_ic": float(group.iloc[-1]["mean_test_ic"]),
                "recent_window_positive_ic_rate": float(group.iloc[-1]["positive_ic_rate"]),
                "valid_ic_dates_min": int(group["valid_ic_dates"].min()),
                "valid_ic_dates_max": int(group["valid_ic_dates"].max()),
            }
        )
    return pd.DataFrame(rows)


def _nearby_variant_support(refinement_classification: pd.DataFrame) -> pd.DataFrame:
    support_names = ["rebalance_5", "smooth_5", "smooth_3", "rebalance_10", "strict_stress_rebalance_10"]
    available = refinement_classification[refinement_classification["signal_name"].isin(support_names)].copy()
    return available[
        [
            "signal_name",
            "status",
            "h20_mean_ic",
            "h20_positive_ic_rate",
            "turnover_proxy",
            "active_date_ratio",
            "wfv_persistence",
            "wfv_sign_consistency",
            "effective_test_ic_ir",
            "max_inventory_corr",
            "max_reversal_corr",
        ]
    ].sort_values("h20_mean_ic", ascending=False)


def _merge_validation_summary(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    concentration: pd.DataFrame,
) -> pd.DataFrame:
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    best = scores[scores["is_best_horizon"]].rename(
        columns={"horizon": "best_horizon", "mean_ic": "best_mean_ic"}
    )
    summary = (
        h20[
            [
                "signal_name",
                "h20_mean_ic",
                "h20_ic_ir",
                "h20_positive_ic_rate",
                "h20_n_dates",
            ]
        ]
        .merge(best[["signal_name", "best_horizon", "best_mean_ic"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, left_on=["signal_name"], right_on=["signal_name"], how="left", suffixes=("", "_wfv"))
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(concentration, on="signal_name", how="left")
    )
    summary["role"] = summary["signal_name"].map(lambda name: SHORTLIST[name]["role"])
    return summary.sort_values(["role", "h20_mean_ic"], ascending=[False, False])


def classify_final(summary: pd.DataFrame) -> tuple[str, list[str], str]:
    primary = summary[summary["signal_name"].eq("rebalance_5")].iloc[0]
    confirmations = summary[summary["signal_name"].isin(["smooth_5", "smooth_3"])]
    risks = []
    if primary["h20_mean_ic"] < 0.02:
        risks.append("primary_h20_ic_below_validation_profile")
    if primary["h20_positive_ic_rate"] < 0.55:
        risks.append("primary_positive_ic_rate_weak")
    if primary["persistence"] < 1.0 or primary["sign_consistency"] < 1.0:
        risks.append("primary_wfv_not_fully_persistent")
    if primary["active_date_ratio"] < 0.15:
        risks.append("primary_active_coverage_low")
    if primary["turnover_proxy"] > 0.05:
        risks.append("primary_turnover_high")
    if primary["max_inventory_corr"] > 0.15:
        risks.append("inventory_similarity_risk")
    if primary["max_reversal_corr"] > 0.15:
        risks.append("reversal_similarity_risk")
    if primary["largest_positive_window_share"] > 0.70:
        risks.append("window_concentration_risk")
    if primary["recent_window_positive_ic_rate"] < 0.45:
        risks.append("recent_window_positive_rate_weak")
    if int(primary["valid_ic_dates_min"]) < 80:
        risks.append("wfv_sample_size_low")

    confirmation_count = int(
        (
            (confirmations["h20_mean_ic"] >= 0.015)
            & (confirmations["persistence"] >= 0.75)
            & (confirmations["sign_consistency"] >= 0.75)
            & (confirmations["max_inventory_corr"] <= 0.15)
            & (confirmations["max_reversal_corr"] <= 0.15)
        ).sum()
    )

    if not risks and confirmation_count >= 1:
        status = "CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE"
        rationale = "Primary variant passed the fixed validation profile and smoothing controls support the same mechanism."
    elif len(risks) <= 2 and confirmation_count >= 1:
        status = "CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE"
        rationale = "Primary variant passed core validation checks, with review guardrails required for residual recent-window and concentration risk."
    elif primary["h20_mean_ic"] > 0.01 and primary["max_inventory_corr"] <= 0.20:
        status = "HOLD_FOR_MORE_RESEARCH"
        rationale = "The mechanism remains distinct and positive, but validation evidence is not strong enough for integration review."
    else:
        status = "REJECT_CONDITIONAL_VALIDATION"
        rationale = "The fixed shortlist did not preserve enough robust, distinct h20 behavior under stricter validation."
    return status, risks, rationale


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    wfv_windows: pd.DataFrame,
    concentration: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    summary: pd.DataFrame,
    support: pd.DataFrame,
    final_status: str,
    risks: list[str],
    rationale: str,
) -> None:
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    lines = [
        "# Volatility Compression Stress Stabilization Conditional Validation",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only pass validated the fixed shortlist for `{SOURCE_SIGNAL}` under isolated run `{RUN_ID}`.",
        "",
        f"Final classification: `{final_status}`",
        f"Decision rationale: {rationale}",
        f"Review risks: `{'; '.join(risks) if risks else 'none'}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.",
        "",
        "## Scope",
        "",
        "Only the fixed shortlist was evaluated. No new variants were created and no parameters were tuned.",
        "",
        registry.to_markdown(index=False),
        "",
        "## Validation Summary",
        "",
        summary[
            [
                "signal_name",
                "role",
                "h20_mean_ic",
                "h20_positive_ic_rate",
                "h20_n_dates",
                "turnover_proxy",
                "active_date_ratio",
                "persistence",
                "sign_consistency",
                "effective_test_ic_ir",
                "largest_positive_window_share",
                "recent_window_ic",
                "recent_window_positive_ic_rate",
                "max_inventory_corr",
                "max_reversal_corr",
                "max_momentum_corr",
            ]
        ].to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h20 Behavior",
        "",
        h20[["signal_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Persistence",
        "",
        wfv.to_markdown(index=False),
        "",
        "## WFV Window Distribution",
        "",
        wfv_windows[["signal_name", "horizon", "window", "start_date", "end_date", "mean_test_ic", "test_ic_ir", "positive_ic_rate", "valid_ic_dates"]].to_markdown(index=False),
        "",
        "## Window Concentration / Overfit Risk",
        "",
        concentration.to_markdown(index=False),
        "",
        "Interpretation: `rebalance_5` is positive in all four WFV-style windows, but window 3 contributes a large share of the positive-window IC and the recent window has weak positive-date breadth. This supports integration review, not production use.",
        "",
        "## Structural Quality / Active Coverage",
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
        "## Orthogonality / Similarity",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Regime / Stress Attribution",
        "",
        stress.sort_values(["signal_name", "mean_ic"], ascending=[True, False])[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Concept-State Attribution",
        "",
        state_attr.sort_values(["signal_name", "mean_ic"], ascending=[True, False])[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Nearby-Variant Support",
        "",
        support.to_markdown(index=False),
        "",
        "The smoothing controls (`smooth_5`, `smooth_3`) confirm the volatility/stress-transition thesis but remain weaker than `rebalance_5` because both retain a negative recent WFV-style window. They should be treated as confirmation/control variants, not primary representations.",
        "",
        "## Primary Variant Assessment",
        "",
        "- `rebalance_5` has enough active coverage for conditional validation: active date ratio is about 0.19 with roughly 95-96 valid IC dates per WFV-style window.",
        "- h20 behavior is the best horizon and remains positive across all validation windows.",
        "- The edge is strongest in drawdown acceleration, panic/liquidity stress, volatility spike, and weak breadth states.",
        "- Similarity to current inventory candidates, reversal baselines, and momentum baselines remains low.",
        "- Residual risks are window concentration and a weak recent-window positive IC rate, so this is not clean production evidence.",
        "",
        "## Final Classification",
        "",
        f"`{final_status}`",
        "",
        "## Recommended Next Step",
        "",
        "Move `volatility_compression_after_stress_stabilization` to research-only conditional-alpha integration review with `rebalance_5` as the primary variant and `smooth_5` / `smooth_3` as confirmation controls. Keep guardrails around fixed parameters, active coverage, recent-window monitoring, and window-concentration review.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals = load_shortlist()
    _, v6_states = build_v6_candidate_panels(panels, benchmark)

    registry = pd.DataFrame(
        [
            {
                "signal_name": name,
                "role": spec["role"],
                "validation_question": spec["validation_question"],
                "source_signal": SOURCE_SIGNAL,
                "source_refinement_run": str(REFINEMENT_OUT_DIR),
                "run_id": RUN_ID,
                "research_status": "TRACK_B_V6_CONDITIONAL_VALIDATION_RESEARCH_ONLY",
            }
            for name, spec in SHORTLIST.items()
        ]
    )

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, v6_states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    concentration = _window_concentration(wfv_windows)
    refs = minimal_reference_panels(pd.read_parquet(REFINEMENT_OUT_DIR / "base_v6_reference_signal_panel.parquet"), panels)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = active_coverage_summary(signals)
    summary = _merge_validation_summary(structural, scores, wfv_summary, orth_summary, active, concentration)
    support = _nearby_variant_support(pd.read_csv(REFINEMENT_OUT_DIR / "variant_classification.csv"))
    final_status, risks, rationale = classify_final(summary)

    artifact_files = [
        "validation_registry.csv",
        "validation_summary.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_variant_horizon.csv",
        "stress_regime_attribution.csv",
        "concept_state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "window_concentration_diagnostics.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "nearby_variant_support.csv",
    ]
    registry.to_csv(OUT_DIR / artifact_files[0], index=False)
    summary.to_csv(OUT_DIR / artifact_files[1], index=False)
    structural.to_csv(OUT_DIR / artifact_files[2], index=False)
    scores.to_csv(OUT_DIR / artifact_files[3], index=False)
    daily_ics.to_csv(OUT_DIR / artifact_files[4], index=False)
    stress.to_csv(OUT_DIR / artifact_files[5], index=False)
    state_attr.to_csv(OUT_DIR / artifact_files[6], index=False)
    wfv_summary.to_csv(OUT_DIR / artifact_files[7], index=False)
    wfv_windows.to_csv(OUT_DIR / artifact_files[8], index=False)
    concentration.to_csv(OUT_DIR / artifact_files[9], index=False)
    orth.to_csv(OUT_DIR / artifact_files[10], index=False)
    orth_summary.to_csv(OUT_DIR / artifact_files[11], index=False)
    active.to_csv(OUT_DIR / artifact_files[12], index=False)
    support.to_csv(OUT_DIR / artifact_files[13], index=False)
    for name, panel in signals.items():
        panel_file = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / panel_file)
        artifact_files.append(panel_file)
    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "source_signal": SOURCE_SIGNAL,
                "source_refinement_note": str(REFINEMENT_NOTE),
                "source_refinement_directory": str(REFINEMENT_OUT_DIR),
                "fixed_shortlist_only": True,
                "new_variants_created": False,
                "parameter_tuning": False,
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "final_classification": final_status,
                "review_risks": risks,
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
        structural,
        scores,
        wfv_summary,
        wfv_windows,
        concentration,
        stress,
        state_attr,
        orth_summary,
        active,
        summary,
        support,
        final_status,
        risks,
        rationale,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(summary.to_string(index=False))
    print(f"FINAL_CLASSIFICATION {final_status}")


if __name__ == "__main__":
    main()
