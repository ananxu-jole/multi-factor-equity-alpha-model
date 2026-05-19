from __future__ import annotations

import json
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
    _clean_panel,
    _rank_cs,
)
from run_track_b_v5_focused_discovery import reference_panels, state_attribution


RUN_ID = "participation_breadth_repair_refinement_v1"
SOURCE_RUN_ID = "track_b_v5_focused_discovery"
SIGNAL_NAME = "participation_breadth_repair_under_hostile_trend"
SOURCE_DIR = Path("artifacts/research") / SOURCE_RUN_ID
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/participation_breadth_repair_refinement.md")


VARIANT_SPECS: list[dict[str, str]] = [
    {"variant_name": "base", "category": "source", "description": "Original v5 focused-discovery signal."},
    {"variant_name": "smooth_3", "category": "mild_smoothing", "description": "3-day rolling mean."},
    {"variant_name": "smooth_5", "category": "mild_smoothing", "description": "5-day rolling mean."},
    {"variant_name": "rebalance_5", "category": "rebalance", "description": "5-day rebalance cadence with forward fill."},
    {"variant_name": "rebalance_10", "category": "rebalance", "description": "10-day rebalance cadence with forward fill."},
    {"variant_name": "rank_persist_5_zero", "category": "rank_persistence", "description": "Keep values only when current and 5-day lag signs agree; zero inactive."},
    {"variant_name": "rank_persist_10_zero", "category": "rank_persistence", "description": "Keep values only when current and 10-day lag signs agree; zero inactive."},
    {"variant_name": "threshold_0p20_zero", "category": "activation_threshold", "description": "Zero values with absolute score below 0.20."},
    {"variant_name": "threshold_0p20_nan", "category": "activation_threshold", "description": "Mask values with absolute score below 0.20."},
    {"variant_name": "threshold_0p35_zero", "category": "activation_threshold", "description": "Zero values with absolute score below 0.35."},
    {"variant_name": "strict_weak_breadth_zero", "category": "state_strictness", "description": "Require weak breadth in addition to the source hostile-repair logic; zero inactive."},
    {"variant_name": "strict_recent_stress_zero", "category": "state_strictness", "description": "Require recent stress in addition to the source hostile-repair logic; zero inactive."},
    {"variant_name": "strict_low_extension_zero", "category": "state_strictness", "description": "Require low market extension in addition to the source hostile-repair logic; zero inactive."},
    {"variant_name": "strict_weak_breadth_rebalance_10", "category": "combined_control", "description": "Weak-breadth strictness plus 10-day rebalance cadence."},
    {"variant_name": "strict_breadth_repair_recent_stress_zero", "category": "combined_control", "description": "Require breadth repair and recent stress; zero inactive."},
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_source_panel() -> pd.DataFrame:
    return pd.read_parquet(SOURCE_DIR / f"{SIGNAL_NAME}_signal_panel.parquet")


def _load_states() -> pd.DataFrame:
    states = pd.read_csv(SOURCE_DIR / "market_state_flags.csv", index_col=0)
    states.index = pd.to_datetime(states.index)
    for col in states.columns:
        states[col] = states[col].astype(bool)
    return states


def _state_panel(states: pd.DataFrame, state: str, columns: pd.Index) -> pd.DataFrame:
    series = states[state].astype(float)
    return pd.DataFrame(
        np.repeat(series.values[:, None], len(columns), axis=1),
        index=states.index,
        columns=columns,
    )


def _rebalance_interval(panel: pd.DataFrame, interval: int) -> pd.DataFrame:
    out = panel.copy() * np.nan
    out.iloc[::interval] = panel.iloc[::interval]
    return out.ffill()


def _threshold(panel: pd.DataFrame, threshold: float, inactive: str) -> pd.DataFrame:
    mask = panel.abs() >= threshold
    if inactive == "zero":
        return panel.where(mask, 0.0)
    return panel.where(mask)


def _rank_persist(panel: pd.DataFrame, lag: int) -> pd.DataFrame:
    keep = (np.sign(panel) == np.sign(panel.shift(lag))) & panel.notna() & panel.shift(lag).notna()
    return panel.where(keep, 0.0)


def _rerank(panel: pd.DataFrame) -> pd.DataFrame:
    return _clean_panel(_rank_cs(panel))


def build_variants(base: pd.DataFrame, states: pd.DataFrame) -> dict[str, pd.DataFrame]:
    weak_breadth = _state_panel(states, "WEAK_BREADTH", base.columns).reindex(base.index)
    recent_stress = _state_panel(states, "RECENT_STRESS", base.columns).reindex(base.index)
    low_extension = _state_panel(states, "LOW_EXTENSION_MARKET", base.columns).reindex(base.index)
    breadth_repair = _state_panel(states, "BREADTH_REPAIR", base.columns).reindex(base.index)
    variants = {
        "base": base,
        "smooth_3": base.rolling(3, min_periods=2).mean(),
        "smooth_5": base.rolling(5, min_periods=3).mean(),
        "rebalance_5": _rebalance_interval(base, 5),
        "rebalance_10": _rebalance_interval(base, 10),
        "rank_persist_5_zero": _rank_persist(base, 5),
        "rank_persist_10_zero": _rank_persist(base, 10),
        "threshold_0p20_zero": _threshold(base, 0.20, "zero"),
        "threshold_0p20_nan": _threshold(base, 0.20, "nan"),
        "threshold_0p35_zero": _threshold(base, 0.35, "zero"),
        "strict_weak_breadth_zero": base * weak_breadth,
        "strict_recent_stress_zero": base * recent_stress,
        "strict_low_extension_zero": base * low_extension,
        "strict_weak_breadth_rebalance_10": _rebalance_interval(base * weak_breadth, 10),
        "strict_breadth_repair_recent_stress_zero": base * breadth_repair * recent_stress,
    }
    return {name: _rerank(panel) for name, panel in variants.items()}


def active_coverage_summary(variants: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in variants.items():
        valid_count = panel.notna().sum(axis=1)
        mean_abs = panel.abs().mean(axis=1, skipna=True)
        active = (valid_count >= 25) & (mean_abs > 0.02)
        transitions = active.astype(int).diff().abs().fillna(0)
        rows.append(
            {
                "variant_name": name,
                "active_dates": int(active.sum()),
                "active_date_ratio": float(active.mean()),
                "activation_transitions": int(transitions.sum()),
                "mean_active_coverage": float(panel[active].notna().mean(axis=1).mean()) if active.any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _max_corr_table(orth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in orth.groupby("signal_name"):
        group = group.dropna(subset=["abs_value_corr"])
        if group.empty:
            continue
        top = group.loc[group["abs_value_corr"].idxmax()]
        prior = group[group["comparison"].str.contains("participation_liquidity_state_shift_20_60", na=False)]
        reversal = group[group["comparison"].isin(["unweighted_reversal_20", "plain_smoothed_reversal_20"])]
        momentum = group[group["comparison"].isin(["plain_momentum_60"])]
        rows.append(
            {
                "variant_name": name,
                "top_comparison": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "prior_participation_liquidity_corr": float(prior["abs_value_corr"].max()) if not prior.empty else np.nan,
                "max_reversal_corr": float(reversal["abs_value_corr"].max()) if not reversal.empty else np.nan,
                "max_momentum_corr": float(momentum["abs_value_corr"].max()) if not momentum.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _h20_summary(scores: pd.DataFrame) -> pd.DataFrame:
    return scores[scores["horizon"].eq(20)].rename(columns={"signal_name": "variant_name"})


def classify_variants(
    scores: pd.DataFrame,
    structural: pd.DataFrame,
    active: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    state_attr: pd.DataFrame,
) -> pd.DataFrame:
    h20 = _h20_summary(scores)
    state_counts = (
        state_attr.groupby("signal_name")["mean_ic"]
        .agg(positive_state_count=lambda s: int((s > 0.010).sum()), best_state_ic="max")
        .reset_index()
        .rename(columns={"signal_name": "variant_name"})
    )
    summary = (
        h20.merge(structural.rename(columns={"signal_name": "variant_name"}), on="variant_name", how="left")
        .merge(active, on="variant_name", how="left")
        .merge(wfv.rename(columns={"signal_name": "variant_name"}), on=["variant_name", "horizon"], how="left")
        .merge(orth_summary, on="variant_name", how="left")
        .merge(state_counts, on="variant_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.35:
            issues.append("high_missingness")
        if row["active_date_ratio"] < 0.12:
            issues.append("sparse_activation")
        if row["turnover_proxy"] > 0.08:
            issues.append("high_turnover")
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["mean_ic"] < 0.018:
            issues.append("weak_h20_ic")
        if row["positive_ic_rate"] < 0.55:
            issues.append("weak_positive_ic_rate")
        if pd.isna(row.get("persistence")) or row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.isna(row.get("sign_consistency")) or row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("prior_participation_liquidity_corr", 0) > 0.25:
            issues.append("prior_participation_liquidity_similarity")
        if row.get("max_reversal_corr", 0) > 0.45:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.45:
            issues.append("momentum_similarity_risk")

        if (
            row["mean_ic"] >= 0.020
            and row["positive_ic_rate"] >= 0.56
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and 0.12 <= row["active_date_ratio"] <= 0.60
            and row["turnover_proxy"] <= 0.08
            and row.get("prior_participation_liquidity_corr", 1) <= 0.25
            and row.get("max_reversal_corr", 1) <= 0.45
            and row.get("max_momentum_corr", 1) <= 0.45
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["mean_ic"] >= 0.012
            and row.get("best_state_ic", 0) >= 0.020
            and row["active_date_ratio"] >= 0.10
            and row.get("prior_participation_liquidity_corr", 1) <= 0.35
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif row.get("positive_state_count", 0) >= 2 and row.get("max_reversal_corr", 1) <= 0.50:
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "variant_name": row["variant_name"],
                "h20_mean_ic": row["mean_ic"],
                "h20_ic_ir": row["ic_ir"],
                "h20_positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "active_date_ratio": row["active_date_ratio"],
                "missing_pct": row["missing_pct"],
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "one_window_dominance": row.get("one_window_dominance"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "prior_participation_liquidity_corr": row.get("prior_participation_liquidity_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "positive_state_count": int(row.get("positive_state_count", 0) or 0),
                "best_state_ic": row.get("best_state_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows).sort_values(["status", "h20_mean_ic"], ascending=[True, False])


def _write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    active: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    orth_summary: pd.DataFrame,
    state_attr: pd.DataFrame,
    decisions: pd.DataFrame,
    final_classification: str,
) -> None:
    h20 = _h20_summary(scores).sort_values("mean_ic", ascending=False)
    best_states = state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)
    advanced = decisions[decisions["status"].isin(["CANDIDATE_FOR_CONDITIONAL_VALIDATION", "CONDITIONAL_REFINEMENT_CANDIDATE"])]
    lines = [
        "# Participation Breadth Repair Refinement",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only pass refines `{SIGNAL_NAME}` from the Track B v5 focused discovery run.",
        "",
        f"Final classification: `{final_classification}`.",
        "",
        "This was a narrow refinement diagnostics pass. It did not broaden discovery, run production registration, promote survivor/watchlist state, modify gates or schemas, change thresholds, use ML, alter portfolio logic, or wire production Conditional-Alpha paths.",
        "",
        f"Variants tested: {len(registry)}",
        "",
        "## Variant Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Structural Quality / Turnover / Active Coverage",
        "",
        structural.rename(columns={"signal_name": "variant_name"}).merge(active, on="variant_name", how="left")[
            [
                "variant_name",
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
        "## h20 Refinement Results",
        "",
        h20[["variant_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores.rename(columns={"signal_name": "variant_name"})[
            ["variant_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]
        ].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.rename(columns={"signal_name": "variant_name"}).to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics unavailable.",
        "",
        "## Orthogonality / Similarity",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Regime / State Attribution",
        "",
        best_states[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Low-Turnover Interpretation",
        "",
        "The source signal's low turnover should not automatically be treated as tradability evidence. This pass explicitly compares turnover against active coverage and stricter activation variants. Variants with very low turnover but sparse activation are treated cautiously because low churn can come from inactivity rather than stable rank behavior.",
        "",
        "## Distinctness From Prior Participation/Liquidity Candidate",
        "",
        "The main orthogonality test is similarity to `participation_liquidity_state_shift_20_60`, alongside reversal and momentum baselines. Variants that improve h20 IC but converge toward the prior participation/liquidity candidate are not considered clean validation candidates.",
        "",
        "## Advanced / Watch Items",
        "",
        advanced.to_markdown(index=False) if not advanced.empty else "No variants advanced beyond conditional-only research.",
        "",
        "## Recommended Next Step",
        "",
        _recommendation(final_classification, decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _recommendation(final_classification: str, decisions: pd.DataFrame) -> str:
    validation = decisions[decisions["status"].eq("CANDIDATE_FOR_CONDITIONAL_VALIDATION")]
    if final_classification == "CANDIDATE_FOR_CONDITIONAL_VALIDATION" and not validation.empty:
        names = ", ".join(f"`{name}`" for name in validation["variant_name"].head(4))
        return f"Proceed to a formal research-only conditional validation pass using a small fixed set led by {names}. Do not add new parameter variants before validation."
    refinement = decisions[decisions["status"].eq("CONDITIONAL_REFINEMENT_CANDIDATE")]
    if not refinement.empty:
        names = ", ".join(f"`{name}`" for name in refinement["variant_name"].head(4))
        return f"Keep in refinement with a fixed shortlist around {names}. Do not broaden the search until sample-size and similarity risks are resolved."
    return "Do not advance this candidate. Treat the pass as useful evidence and return to concept design."


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    base = _load_source_panel()
    states = _load_states()
    variants = build_variants(base, states)
    registry = pd.DataFrame(VARIANT_SPECS)
    registry["run_id"] = RUN_ID
    registry["source_signal"] = SIGNAL_NAME

    structural = structural_summary(variants)
    active = active_coverage_summary(variants)
    scores, daily_ics = score_signals(variants, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    refs = reference_panels({"base": base}, panels, benchmark)
    orth = orthogonality(variants, refs)
    orth_summary = _max_corr_table(orth)
    decisions = classify_variants(scores, structural, active, wfv_summary, orth_summary, state_attr)
    if (decisions["status"] == "CANDIDATE_FOR_CONDITIONAL_VALIDATION").any():
        final_classification = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
    elif (decisions["status"] == "CONDITIONAL_REFINEMENT_CANDIDATE").any():
        final_classification = "CONDITIONAL_REFINEMENT_CANDIDATE"
    elif (decisions["status"] == "CONDITIONAL_ONLY_RESEARCH").any():
        final_classification = "CONDITIONAL_ONLY_RESEARCH"
    else:
        final_classification = "REJECT_RESEARCH"

    artifact_files = [
        "variant_registry.csv",
        "structural_quality_summary.csv",
        "active_coverage_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_variant_horizon.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "stress_regime_attribution.csv",
        "state_attribution.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "variant_classification.csv",
    ]
    registry.to_csv(OUT_DIR / artifact_files[0], index=False)
    structural.to_csv(OUT_DIR / artifact_files[1], index=False)
    active.to_csv(OUT_DIR / artifact_files[2], index=False)
    scores.to_csv(OUT_DIR / artifact_files[3], index=False)
    daily_ics.to_csv(OUT_DIR / artifact_files[4], index=False)
    wfv_summary.to_csv(OUT_DIR / artifact_files[5], index=False)
    wfv_windows.to_csv(OUT_DIR / artifact_files[6], index=False)
    stress.to_csv(OUT_DIR / artifact_files[7], index=False)
    state_attr.to_csv(OUT_DIR / artifact_files[8], index=False)
    orth.to_csv(OUT_DIR / artifact_files[9], index=False)
    orth_summary.to_csv(OUT_DIR / artifact_files[10], index=False)
    decisions.to_csv(OUT_DIR / artifact_files[11], index=False)
    for name, panel in variants.items():
        panel_file = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / panel_file)
        artifact_files.append(panel_file)
    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "source_signal": SIGNAL_NAME,
                "research_only": True,
                "variant_count": len(variants),
                "final_classification": final_classification,
                "production_registration": False,
                "survivor_watchlist_mutation": False,
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
    _write_note(registry, structural, active, scores, wfv_summary, orth_summary, state_attr, decisions, final_classification)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"FINAL {final_classification}")
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    main()
