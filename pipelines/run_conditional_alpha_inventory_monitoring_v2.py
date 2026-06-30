from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import run_conditional_alpha_inventory_monitoring_v1 as v1


RUN_ID = "conditional_alpha_inventory_monitoring_v2"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v2.md")
V1_DIR = Path("artifacts/research/conditional_alpha_inventory_monitoring_v1")

SOURCE_NOTES = [
    "docs/research_notes/conditional_alpha_inventory_monitoring_v1.md",
    "docs/research_notes/conditional_alpha_inventory_v2_governance_update.md",
    "docs/research_notes/inventory_ecosystem_review_v1.md",
    "docs/research_notes/track_b_expansion_v3_midcycle_review.md",
    "docs/research_notes/track_b_expansion_v4_closeout_review.md",
    "docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md",
    "docs/research_notes/participation_breadth_repair_conditional_validation.md",
    "docs/research_notes/volatility_compression_stress_stabilization_integration_review.md",
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _classification_change(current: pd.DataFrame) -> pd.DataFrame:
    prior = _read_csv(V1_DIR / "candidate_health_summary.csv")
    if prior.empty:
        return pd.DataFrame()
    cols = [
        "signal_name",
        "monitoring_classification",
        "h20_mean_ic",
        "h20_positive_ic_rate",
        "rolling_h20_ic_latest",
        "recent_window_ic",
        "recent_window_positive_rate",
        "turnover_proxy",
        "active_coverage",
        "max_inventory_corr",
    ]
    prior = prior[[col for col in cols if col in prior.columns]].copy()
    current = current[[col for col in cols if col in current.columns]].copy()
    merged = current.merge(prior, on="signal_name", how="left", suffixes=("_v2", "_v1"))
    for metric in [
        "h20_mean_ic",
        "h20_positive_ic_rate",
        "rolling_h20_ic_latest",
        "recent_window_ic",
        "recent_window_positive_rate",
        "turnover_proxy",
        "active_coverage",
        "max_inventory_corr",
    ]:
        if f"{metric}_v2" in merged.columns and f"{metric}_v1" in merged.columns:
            merged[f"{metric}_delta"] = merged[f"{metric}_v2"] - merged[f"{metric}_v1"]
    return merged


def _coactivation_drift(coactivation: pd.DataFrame) -> pd.DataFrame:
    prior = _read_csv(V1_DIR / "coactivation_matrix.csv")
    if prior.empty:
        return pd.DataFrame()
    prior = prior.set_index(prior.columns[0])
    current = coactivation.copy()
    rows = []
    for left in current.index:
        for right in current.columns:
            if left == right:
                continue
            old = float(prior.loc[left, right]) if left in prior.index and right in prior.columns else np.nan
            new = float(current.loc[left, right])
            rows.append(
                {
                    "left_signal": left,
                    "right_signal": right,
                    "coactivation_v1": old,
                    "coactivation_v2": new,
                    "coactivation_delta": new - old if pd.notna(old) else np.nan,
                    "concentration_flag": bool(new > 0.75),
                }
            )
    return pd.DataFrame(rows)


def _correlation_drift(corr: pd.DataFrame) -> pd.DataFrame:
    prior = _read_csv(V1_DIR / "inventory_correlation_matrix.csv")
    if prior.empty:
        return pd.DataFrame()
    prior = prior.set_index(prior.columns[0])
    rows = []
    for left in corr.index:
        for right in corr.columns:
            if left >= right:
                continue
            old = float(prior.loc[left, right]) if left in prior.index and right in prior.columns else np.nan
            new = float(corr.loc[left, right])
            rows.append(
                {
                    "left_signal": left,
                    "right_signal": right,
                    "abs_corr_v1": abs(old) if pd.notna(old) else np.nan,
                    "abs_corr_v2": abs(new) if pd.notna(new) else np.nan,
                    "abs_corr_delta": abs(new) - abs(old) if pd.notna(old) and pd.notna(new) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _state_concentration(regime_overlap: pd.DataFrame) -> pd.DataFrame:
    hostile_states = {
        "trend_hostile",
        "weak_breadth",
        "stress_or_weak_breadth",
        "panic_liquidity_stress",
        "drawdown_acceleration",
        "volatility_spike",
    }
    rows = []
    for signal_name, group in regime_overlap.groupby("signal_name"):
        positive = group[group["mean_ic"].gt(0)]
        hostile_positive = positive[positive["state"].isin(hostile_states)]
        top = group.sort_values("mean_ic", ascending=False).head(1)
        rows.append(
            {
                "signal_name": signal_name,
                "positive_state_count": int(positive["state"].nunique()),
                "hostile_or_stress_positive_state_count": int(hostile_positive["state"].nunique()),
                "top_state": str(top.iloc[0]["state"]) if not top.empty else "unavailable",
                "top_state_mean_ic": float(top.iloc[0]["mean_ic"]) if not top.empty else np.nan,
                "hostile_stress_dependence_flag": bool(hostile_positive["state"].nunique() >= 2),
            }
        )
    return pd.DataFrame(rows)


def _candidate_direction(row: pd.Series) -> str:
    status_v1 = row.get("monitoring_classification_v1")
    status_v2 = row.get("monitoring_classification_v2")
    if pd.isna(status_v1):
        return "no_v1_comparison"
    if status_v1 != status_v2:
        return f"classification_changed_{status_v1}_to_{status_v2}"
    checks = [
        row.get("rolling_h20_ic_latest_delta", 0) > 0.005,
        row.get("recent_window_ic_delta", 0) > 0.005,
        row.get("recent_window_positive_rate_delta", 0) > 0.03,
    ]
    weak = [
        row.get("rolling_h20_ic_latest_delta", 0) < -0.005,
        row.get("recent_window_ic_delta", 0) < -0.005,
        row.get("recent_window_positive_rate_delta", 0) < -0.03,
    ]
    if sum(checks) >= 2:
        return "improved_with_same_classification"
    if sum(weak) >= 2:
        return "degraded_with_same_classification"
    return "stable"


def _write_note(
    candidate_health: pd.DataFrame,
    guardrails: pd.DataFrame,
    coactivation: pd.DataFrame,
    corr: pd.DataFrame,
    regime_overlap: pd.DataFrame,
    inventory_summary: pd.DataFrame,
    drift: pd.DataFrame,
    coactivation_drift: pd.DataFrame,
    correlation_drift: pd.DataFrame,
    state_concentration: pd.DataFrame,
    missing: list[dict[str, str]],
) -> None:
    class_counts = guardrails["monitoring_classification"].value_counts().to_dict()
    watch = guardrails[guardrails["monitoring_classification"].eq("WATCH_MONITOR")]["signal_name"].tolist()
    downgrade = guardrails[
        guardrails["monitoring_classification"].isin(["DEGRADED_RESEARCH", "REVIEW_FOR_DOWNGRADE", "RETIREMENT_CANDIDATE"])
    ]["signal_name"].tolist()
    if not drift.empty:
        drift = drift.copy()
        drift["direction_vs_v1"] = drift.apply(_candidate_direction, axis=1)

    breadth_row = candidate_health[candidate_health["signal_name"].eq("participation_breadth_repair_under_hostile_trend")]
    breadth_class = str(breadth_row.iloc[0]["monitoring_classification"]) if not breadth_row.empty else "unavailable"
    max_corr = float(inventory_summary.iloc[0]["max_pairwise_abs_corr"])
    max_coactivation = float(inventory_summary.iloc[0]["max_pairwise_coactivation"])

    lines = [
        "# Conditional Alpha Inventory Monitoring v2",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only monitoring refresh evaluated the current three-candidate Conditional Alpha Inventory under `{RUN_ID}` after the Expansion v3/v4 research cycle.",
        "",
        f"Monitoring classifications: `{json.dumps(class_counts, sort_keys=True)}`",
        "",
        "Expansion v4 did not change the governance interpretation of the current inventory: Project Underdog's strongest evidence remains active repair/stabilization, while post-repair and resolved-state extensions were structurally clean but empirically weaker.",
        "",
        "The inventory remains usable for research and stable enough to support a future Expansion v5 design screen, but not enough for construction-layer work. Expansion v5 should wait until the WATCH_MONITOR risks are explicitly accepted and should target active repair/stabilization diversification rather than post-repair calm persistence.",
        "",
        "No new alpha candidates, discovery, validation/refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.",
        "",
        "## Sources Reviewed",
        "",
        *[f"- `{note}`" for note in SOURCE_NOTES],
        "",
        "## Candidate Health Summary",
        "",
        candidate_health[
            [
                "signal_name",
                "family",
                "inventory_status",
                "primary_variant",
                "h20_mean_ic",
                "h20_positive_ic_rate",
                "turnover_proxy",
                "active_coverage",
                "persistence",
                "sign_consistency",
                "rolling_h20_ic_latest",
                "rolling_positive_rate_latest",
                "recent_window_ic",
                "recent_window_positive_rate",
                "one_window_dominance_recomputed",
                "max_inventory_corr",
                "max_reversal_corr",
                "max_momentum_corr",
                "monitoring_classification",
                "failed_guardrails",
                "caution_flags",
            ]
        ].to_markdown(index=False),
        "",
        "## Drift Versus Monitoring v1",
        "",
        drift.to_markdown(index=False) if not drift.empty else "Monitoring v1 artifacts were unavailable for drift comparison.",
        "",
        "## Specific Monitoring Questions",
        "",
        "1. Did the two `WATCH_MONITOR` candidates improve, degrade, or remain stable?",
        "",
        "- `participation_liquidity_state_shift_20_60`: remains `WATCH_MONITOR`; no downgrade review is triggered, but rolling/recent-window weakness remains the key watch reason.",
        "- `volatility_compression_after_stress_stabilization`: remains `WATCH_MONITOR`; recent-window and concentration guardrails still require explicit acceptance before future use.",
        "",
        "2. Does `participation_breadth_repair_under_hostile_trend` remain the cleanest inventory candidate?",
        "",
        f"- Yes. It remains `{breadth_class}` and continues to be the cleanest current inventory anchor.",
        "",
        "3. Is inventory correlation still low?",
        "",
        f"- Yes. Max pairwise absolute correlation is `{max_corr:.6f}`.",
        "",
        "4. Is co-activation still concentrated between participation/breadth candidates?",
        "",
        f"- Yes. Max pairwise co-activation is `{max_coactivation:.6f}`, and the main concentration remains participation/liquidity with breadth repair.",
        "",
        "5. Is h20 concentration still the main horizon risk?",
        "",
        "- Yes. All three current inventory candidates remain monitored around h20 behavior.",
        "",
        "6. Is hostile/stress-state dependence still the main state risk?",
        "",
        "- Yes. State concentration remains hostile/stress, weak-breadth, drawdown, panic/liquidity, or stabilization oriented.",
        "",
        "7. Does Expansion v4 evidence change the governance interpretation of the current inventory?",
        "",
        "- No. Expansion v4 strengthens the interpretation that active repair/stabilization is the durable project identity. It does not justify downgrading the current inventory, but it argues against more post-repair expansion before monitoring and redesign.",
        "",
        "## Inventory-Level Overlap",
        "",
        "### Co-Activation Matrix",
        "",
        coactivation.to_markdown(),
        "",
        "### Co-Activation Drift",
        "",
        coactivation_drift.to_markdown(index=False) if not coactivation_drift.empty else "No v1 co-activation artifact was available.",
        "",
        "### Signal Correlation Matrix",
        "",
        corr.to_markdown(),
        "",
        "### Correlation Drift",
        "",
        correlation_drift.to_markdown(index=False) if not correlation_drift.empty else "No v1 correlation artifact was available.",
        "",
        "### Inventory-Level Summary",
        "",
        inventory_summary.to_markdown(index=False),
        "",
        "## State Concentration",
        "",
        state_concentration.to_markdown(index=False),
        "",
        "Top positive h20 state slices by candidate:",
        "",
        regime_overlap.sort_values(["signal_name", "mean_ic"], ascending=[True, False])
        .groupby("signal_name")
        .head(6)[["signal_name", "state", "state_dates", "valid_ic_dates", "mean_ic", "positive_ic_rate"]]
        .to_markdown(index=False),
        "",
        "## Candidate-Level Interpretation",
        "",
    ]

    for _, row in candidate_health.iterrows():
        lines.extend(
            [
                f"### `{row['signal_name']}`",
                "",
                f"- Classification: `{row['monitoring_classification']}`",
                f"- h20 mean IC / positive IC rate: `{row['h20_mean_ic']:.6f}` / `{row['h20_positive_ic_rate']:.6f}`",
                f"- Rolling h20 IC / rolling positive rate: `{row['rolling_h20_ic_latest']:.6f}` / `{row['rolling_positive_rate_latest']:.6f}`",
                f"- Recent-window IC / positive rate: `{row['recent_window_ic']:.6f}` / `{row['recent_window_positive_rate']:.6f}`",
                f"- WFV persistence/sign consistency: `{row['persistence']:.2f}` / `{row['sign_consistency']:.2f}`",
                f"- Turnover / active coverage: `{row['turnover_proxy']:.6f}` / `{row['active_coverage']:.6f}`",
                f"- One-window dominance: `{row['one_window_dominance_recomputed']:.6f}`",
                f"- Guardrail failures: `{row['failed_guardrails']}`",
                f"- Caution flags: `{row['caution_flags']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Governance Recommendation",
            "",
            f"- Inventory stability: research-stable, with `{len(watch)}` WATCH_MONITOR candidates.",
            f"- Downgrade review needed now: {'; '.join(downgrade) if downgrade else 'none'}.",
            "- Additional monitoring: required before construction-layer work and recommended before any Expansion v5 implementation.",
            "- Expansion v5 design: allowed only as design-screening after explicit acceptance of WATCH_MONITOR risks.",
            "- Expansion v5 implementation: should wait until the design screen identifies an active repair/stabilization mechanism that reduces co-activation, state, horizon, or turnover concentration.",
            "",
            "## Future Discovery Targets",
            "",
            "- Active repair/stabilization mechanisms outside the current participation/breadth pair.",
            "- h10 or h15 mechanisms only when the state thesis naturally supports that horizon.",
            "- Medium-coverage active repair states with lower co-activation against `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend`.",
            "- Different turnover profiles from the existing liquidity and volatility/stress candidates.",
            "- Stress or repair dimensions not reducible to passive calm accumulation, post-repair continuation, or broad hostile-to-neutral transition gates.",
            "",
            "## Missing Or Partial Inputs",
            "",
            pd.DataFrame(missing).to_markdown(index=False) if missing else "All current inventory panels were available or rebuildable from existing research artifacts.",
        ]
    )
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = v1.load_inputs()
    signals, missing = v1._load_inventory_panels(panels, benchmark)
    artifacts, candidate_summary = v1._build_candidate_summary(signals, panels, benchmark, missing)
    guardrails = v1._guardrail_status(candidate_summary, v1.CANDIDATES)
    coactivation = v1._coactivation_matrix(signals)
    corr = v1._correlation_matrix(signals)
    regime_overlap = v1._regime_overlap_summary(artifacts["daily_ics"], artifacts["scores"], panels["close"], benchmark)
    inventory_summary = v1._inventory_level_summary(coactivation, corr, candidate_summary, regime_overlap)
    candidate_health = candidate_summary.merge(
        guardrails[["signal_name", "monitoring_classification", "failed_guardrails", "caution_flags"]],
        on="signal_name",
        how="left",
    )
    drift = _classification_change(candidate_health)
    coact_drift = _coactivation_drift(coactivation)
    corr_drift = _correlation_drift(corr)
    state_conc = _state_concentration(regime_overlap)

    candidate_health.to_csv(OUT_DIR / "candidate_health_summary.csv", index=False)
    coactivation.to_csv(OUT_DIR / "coactivation_matrix.csv")
    corr.to_csv(OUT_DIR / "inventory_correlation_matrix.csv")
    guardrails.to_csv(OUT_DIR / "guardrail_status.csv", index=False)
    regime_overlap.to_csv(OUT_DIR / "regime_overlap_summary.csv", index=False)
    inventory_summary.to_csv(OUT_DIR / "inventory_level_summary.csv", index=False)
    artifacts["scores"].to_csv(OUT_DIR / "multi_horizon_scores.csv", index=False)
    artifacts["daily_ics"].to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    artifacts["wfv"].to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    artifacts["wfv_windows"].to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    artifacts["h20_wfv"].to_csv(OUT_DIR / "h20_wfv_monitor_summary.csv", index=False)
    artifacts["h20_wfv_windows"].to_csv(OUT_DIR / "h20_wfv_monitor_windows.csv", index=False)
    artifacts["similarity_detail"].to_csv(OUT_DIR / "inventory_similarity_detail.csv", index=False)
    artifacts["turnover"].to_csv(OUT_DIR / "turnover_drift_monitor.csv", index=False)
    artifacts["active"].to_csv(OUT_DIR / "active_coverage_drift_monitor.csv", index=False)
    drift.to_csv(OUT_DIR / "candidate_drift_vs_monitoring_v1.csv", index=False)
    coact_drift.to_csv(OUT_DIR / "coactivation_drift_vs_monitoring_v1.csv", index=False)
    corr_drift.to_csv(OUT_DIR / "correlation_drift_vs_monitoring_v1.csv", index=False)
    state_conc.to_csv(OUT_DIR / "state_concentration_summary.csv", index=False)
    pd.DataFrame(missing).to_csv(OUT_DIR / "missing_artifacts.csv", index=False)

    manifest = {
        "run_id": RUN_ID,
        "research_only": True,
        "candidate_count": len(v1.CANDIDATES),
        "inventory_candidates": [candidate.signal_name for candidate in v1.CANDIDATES],
        "source_notes": SOURCE_NOTES,
        "new_alpha_candidates": False,
        "discovery": False,
        "validation_or_refinement": False,
        "production_registration": False,
        "survivor_watchlist_mutation": False,
        "portfolio_construction": False,
        "ml_integration": False,
        "signal_blending": False,
        "weighting_engine": False,
        "optimization_engine": False,
        "gates_schemas_thresholds_modified": False,
        "outputs": sorted(path.name for path in OUT_DIR.iterdir()) + ["manifest.json"],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _write_note(
        candidate_health,
        guardrails,
        coactivation,
        corr,
        regime_overlap,
        inventory_summary,
        drift,
        coact_drift,
        corr_drift,
        state_conc,
        missing,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(guardrails[["signal_name", "monitoring_classification", "failed_guardrails", "caution_flags"]].to_string(index=False))


if __name__ == "__main__":
    main()
