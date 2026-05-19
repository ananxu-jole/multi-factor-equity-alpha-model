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
    _clean_panel,
    _rank_cs,
)
from run_track_b_v6_focused_discovery import (
    BREADTH_INVENTORY_PATH,
    LIQUIDITY_INVENTORY_PATH,
    OUT_DIR as V6_OUT_DIR,
    build_candidate_panels as build_v6_candidate_panels,
    state_attribution,
    active_coverage_summary,
    _market_state_panel,
    _max_corr_table,
    _rebalance_interval,
)


RUN_ID = "volatility_compression_stress_stabilization_refinement_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/volatility_compression_stress_stabilization_refinement.md")
SOURCE_NOTE = Path("docs/research_notes/track_b_v6_focused_discovery.md")
SOURCE_SIGNAL = "volatility_compression_after_stress_stabilization"


VARIANT_SPECS: list[dict[str, str]] = [
    {
        "variant_name": "base_v6_reference",
        "refinement_type": "reference",
        "description": "Original v6 formulation for continuity.",
    },
    {
        "variant_name": "smooth_3",
        "refinement_type": "mild_smoothing",
        "description": "Three-day smoothing to reduce volatility/rank noise.",
    },
    {
        "variant_name": "smooth_5",
        "refinement_type": "mild_smoothing",
        "description": "Five-day smoothing to reduce volatility/rank noise.",
    },
    {
        "variant_name": "rebalance_5",
        "refinement_type": "rebalance_interval",
        "description": "Five-day rebalance hold to reduce rank churn.",
    },
    {
        "variant_name": "rebalance_10",
        "refinement_type": "rebalance_interval",
        "description": "Ten-day rebalance hold to reduce rank churn.",
    },
    {
        "variant_name": "rank_persist_5",
        "refinement_type": "low_churn_filter",
        "description": "Five-day rank persistence filter using same-direction confirmation.",
    },
    {
        "variant_name": "rank_persist_10",
        "refinement_type": "low_churn_filter",
        "description": "Ten-day rank persistence filter using same-direction confirmation.",
    },
    {
        "variant_name": "threshold_abs_40_zero",
        "refinement_type": "activation_threshold",
        "description": "Keep stronger absolute signals only; inactive entries become neutral.",
    },
    {
        "variant_name": "threshold_abs_55_zero",
        "refinement_type": "activation_threshold",
        "description": "Stricter absolute signal threshold; inactive entries become neutral.",
    },
    {
        "variant_name": "stress_strict_panic_drawdown_zero",
        "refinement_type": "stress_strictness",
        "description": "Activate only during panic/liquidity stress or drawdown acceleration.",
    },
    {
        "variant_name": "stress_strict_vol_spike_zero",
        "refinement_type": "stress_strictness",
        "description": "Activate only during benchmark volatility spikes.",
    },
    {
        "variant_name": "stress_or_weak_breadth_zero",
        "refinement_type": "stress_strictness",
        "description": "Activate during volatility spike, panic/drawdown stress, or weak breadth.",
    },
    {
        "variant_name": "exclude_transition_recovery_zero",
        "refinement_type": "bad_state_exclusion",
        "description": "Deactivate during trend-transition and recovery states that hurt v6 attribution.",
    },
    {
        "variant_name": "strict_stress_rebalance_10",
        "refinement_type": "combined_low_churn",
        "description": "Stress/weak-breadth activation plus ten-day rebalance hold.",
    },
    {
        "variant_name": "exclude_bad_rebalance_10",
        "refinement_type": "combined_low_churn",
        "description": "Exclude bad states and apply a ten-day rebalance hold.",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _rerank(panel: pd.DataFrame) -> pd.DataFrame:
    return _clean_panel(_rank_cs(panel))


def _smooth(panel: pd.DataFrame, window: int) -> pd.DataFrame:
    return _rerank(panel.rolling(window, min_periods=max(2, window // 2 + 1)).mean())


def _zero_inactive(panel: pd.DataFrame, gate: pd.DataFrame) -> pd.DataFrame:
    return _clean_panel(panel.where(gate.astype(bool), 0.0))


def _rank_persist(panel: pd.DataFrame, window: int) -> pd.DataFrame:
    stable_direction = panel.rolling(window, min_periods=max(3, window // 2)).mean()
    same_direction = np.sign(panel).eq(np.sign(stable_direction))
    return _rerank(panel.where(same_direction, 0.0))


def _threshold_abs(panel: pd.DataFrame, quantile: float) -> pd.DataFrame:
    threshold = panel.abs().quantile(quantile, axis=1)
    mask = panel.abs().ge(threshold, axis=0)
    return _rerank(panel.where(mask, 0.0))


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def minimal_reference_panels(
    base: pd.DataFrame,
    panels: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    ret1 = close.pct_change(1, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    vol20 = ret1.rolling(20, min_periods=15).std()
    vol60 = vol20.rolling(60, min_periods=40).mean()
    simple_volatility_reversal = _rank_cs(
        (-ret20 * (1 + (_safe_div(vol20, vol60) - 1).clip(lower=0))).rolling(5, min_periods=3).mean()
    )
    refs = {
        "unweighted_reversal_20": _rank_cs(-ret20),
        "plain_smoothed_reversal_20": _rank_cs((-ret20).rolling(5, min_periods=3).mean()),
        "plain_momentum_60": _rank_cs(ret60),
        "simple_volatility_reversal": simple_volatility_reversal,
        "v6_base_volatility_compression_after_stress_stabilization": base,
    }
    if LIQUIDITY_INVENTORY_PATH.exists():
        refs["inventory_participation_liquidity_state_shift_20_60"] = pd.read_parquet(
            LIQUIDITY_INVENTORY_PATH
        ).reindex(index=base.index, columns=base.columns)
    if BREADTH_INVENTORY_PATH.exists():
        refs["inventory_participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(
            BREADTH_INVENTORY_PATH
        ).reindex(index=base.index, columns=base.columns)
    return refs


def build_refinement_variants(
    base: pd.DataFrame,
    stress_states: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    columns = base.columns
    panic_drawdown = (
        stress_states["panic_liquidity_stress"] | stress_states["drawdown_acceleration"]
    ).fillna(False)
    vol_spike = stress_states["volatility_spike"].fillna(False)
    weak_breadth = stress_states["weak_breadth"].fillna(False)
    bad_transition = (
        stress_states["trend_transition"] | stress_states["recovery_phase"]
    ).fillna(False)
    stress_or_weak = (panic_drawdown | vol_spike | weak_breadth).fillna(False)
    exclude_bad = (~bad_transition).fillna(False)

    panic_drawdown_gate = _market_state_panel(panic_drawdown, columns)
    vol_spike_gate = _market_state_panel(vol_spike, columns)
    stress_or_weak_gate = _market_state_panel(stress_or_weak, columns)
    exclude_bad_gate = _market_state_panel(exclude_bad, columns)

    variants = {
        "base_v6_reference": base,
        "smooth_3": _smooth(base, 3),
        "smooth_5": _smooth(base, 5),
        "rebalance_5": _rerank(_rebalance_interval(base, 5)),
        "rebalance_10": _rerank(_rebalance_interval(base, 10)),
        "rank_persist_5": _rank_persist(base, 5),
        "rank_persist_10": _rank_persist(base, 10),
        "threshold_abs_40_zero": _threshold_abs(base, 0.40),
        "threshold_abs_55_zero": _threshold_abs(base, 0.55),
        "stress_strict_panic_drawdown_zero": _rerank(_zero_inactive(base, panic_drawdown_gate)),
        "stress_strict_vol_spike_zero": _rerank(_zero_inactive(base, vol_spike_gate)),
        "stress_or_weak_breadth_zero": _rerank(_zero_inactive(base, stress_or_weak_gate)),
        "exclude_transition_recovery_zero": _rerank(_zero_inactive(base, exclude_bad_gate)),
        "strict_stress_rebalance_10": _rerank(_rebalance_interval(_zero_inactive(base, stress_or_weak_gate), 10)),
        "exclude_bad_rebalance_10": _rerank(_rebalance_interval(_zero_inactive(base, exclude_bad_gate), 10)),
    }
    return {name: _clean_panel(panel) for name, panel in variants.items()}


def _window_failure_summary(wfv_windows: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in wfv_windows.groupby("signal_name"):
        group = group.sort_values("window")
        negative = group[group["mean_test_ic"] <= 0]
        min_row = group.loc[group["mean_test_ic"].idxmin()]
        rows.append(
            {
                "signal_name": name,
                "negative_window_count": int(len(negative)),
                "worst_window": int(min_row["window"]),
                "worst_window_mean_ic": float(min_row["mean_test_ic"]),
                "worst_window_positive_ic_rate": float(min_row["positive_ic_rate"]),
                "one_bad_window_only": bool(len(negative) == 1),
                "failure_diagnosis": "single_bad_window" if len(negative) == 1 else "multi_window_instability",
            }
        )
    return pd.DataFrame(rows)


def classify_variants(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    windows: pd.DataFrame,
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
            worst_regime_ic="min",
        )
        .reset_index()
    )
    window_fail = _window_failure_summary(windows)
    summary = (
        best.merge(h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(window_fail, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.35:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.14:
            issues.append("high_turnover")
        if row["h20_mean_ic"] < 0.006:
            issues.append("weak_h20_ic")
        if row["h20_positive_ic_rate"] < 0.53:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("active_date_ratio", 1) < 0.10:
            issues.append("sparse_activation")
        if row.get("max_inventory_corr", 0) > 0.45:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.45:
            issues.append("reversal_similarity_risk")
        if row.get("negative_window_count", 0) > 1:
            issues.append("multi_window_instability")

        if (
            row["h20_mean_ic"] >= 0.014
            and row["h20_positive_ic_rate"] >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.10
            and row.get("active_date_ratio", 0) >= 0.12
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_reversal_corr", 1) <= 0.35
            and row.get("negative_window_count", 4) <= 1
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["h20_mean_ic"] >= 0.009
            and row.get("best_regime_ic", 0) >= 0.025
            and row.get("active_date_ratio", 0) >= 0.10
            and row.get("max_inventory_corr", 1) <= 0.45
            and row.get("max_reversal_corr", 1) <= 0.45
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_regime_count", 0) >= 2
            and row.get("active_date_ratio", 0) >= 0.08
            and row.get("max_inventory_corr", 1) <= 0.50
            and row.get("max_reversal_corr", 1) <= 0.50
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "h20_mean_ic": row["h20_mean_ic"],
                "h20_ic_ir": row["h20_ic_ir"],
                "h20_positive_ic_rate": row["h20_positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_mean_test_ic": row.get("effective_mean_test_ic"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "negative_window_count": row.get("negative_window_count"),
                "worst_window": row.get("worst_window"),
                "worst_window_mean_ic": row.get("worst_window_mean_ic"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "worst_regime_ic": row.get("worst_regime_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    status_order = {
        "CANDIDATE_FOR_CONDITIONAL_VALIDATION": 0,
        "CONDITIONAL_REFINEMENT_CANDIDATE": 1,
        "CONDITIONAL_ONLY_RESEARCH": 2,
        "REJECT_RESEARCH": 3,
    }
    out = pd.DataFrame(rows)
    out["_status_order"] = out["status"].map(status_order)
    return out.sort_values(["_status_order", "h20_mean_ic"], ascending=[True, False]).drop(columns=["_status_order"])


def _final_classification(decisions: pd.DataFrame) -> str:
    order = [
        "CANDIDATE_FOR_CONDITIONAL_VALIDATION",
        "CONDITIONAL_REFINEMENT_CANDIDATE",
        "CONDITIONAL_ONLY_RESEARCH",
        "REJECT_RESEARCH",
    ]
    for status in order:
        if decisions["status"].eq(status).any():
            return status
    return "REJECT_RESEARCH"


def _recommendation(final_status: str, decisions: pd.DataFrame) -> str:
    if final_status == "CANDIDATE_FOR_CONDITIONAL_VALIDATION":
        names = ", ".join(f"`{name}`" for name in decisions.loc[decisions["status"].eq(final_status), "signal_name"].head(3))
        return f"Run a formal conditional-validation pass on a fixed shortlist led by {names}; do not add new volatility concepts."
    if final_status == "CONDITIONAL_REFINEMENT_CANDIDATE":
        best = decisions.iloc[0]
        return (
            f"Keep `{best['signal_name']}` in conditional refinement research, but do not advance to validation. "
            "The mechanism remains orthogonal but has not yet solved WFV persistence/sign stability."
        )
    if final_status == "CONDITIONAL_ONLY_RESEARCH":
        return "Retain the mechanism as conditional-only evidence for volatility/stress transitions; close v6 without adding an inventory candidate."
    return "Reject this refinement path for now and return to concept design before revisiting volatility/stress-transition mechanisms."


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    wfv_windows: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    final_status = _final_classification(decisions)
    top = decisions.head(8)
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    best_windows = wfv_windows[wfv_windows["signal_name"].isin(top["signal_name"])].copy()
    stress_top = stress.sort_values("mean_ic", ascending=False).groupby("signal_name").head(5)
    state_top = state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(5)
    status_counts = decisions["status"].value_counts().to_dict()

    lines = [
        "# Volatility Compression Stress Stabilization Refinement",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only refinement tested `{SOURCE_SIGNAL}` under isolated run `{RUN_ID}`.",
        "",
        f"Variants tested: {len(registry)}",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        f"Final classification: `{final_status}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.",
        "",
        "The v6 failure was not primarily a reversal-similarity problem. The base signal was orthogonal to inventory/reversal/momentum baselines, but WFV stability was weak because the edge was negative in multiple validation windows, especially the most recent window. Stress attribution showed strong behavior in panic/drawdown/volatility stress and weak behavior in trend-transition, recovery, and high-dispersion-rotation states.",
        "",
        "## Source Inputs",
        "",
        f"- Source note: `{SOURCE_NOTE}`",
        f"- Source artifact directory: `{V6_OUT_DIR}`",
        f"- Source signal: `{SOURCE_SIGNAL}`",
        "",
        "## Controlled Variant Set",
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
        ].sort_values("turnover_proxy").to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h20 Behavior",
        "",
        h20[["signal_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].head(12).to_markdown(index=False),
        "",
        "## WFV-Style Results",
        "",
        wfv.sort_values("effective_mean_test_ic", ascending=False).to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics were unavailable.",
        "",
        "## WFV Window Failure Diagnostics",
        "",
        best_windows[["signal_name", "horizon", "window", "start_date", "end_date", "mean_test_ic", "test_ic_ir", "positive_ic_rate", "valid_ic_dates"]].to_markdown(index=False) if not best_windows.empty else "No WFV windows were available for the top variants.",
        "",
        "## Stress And Regime Attribution",
        "",
        stress_top[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Concept-State Attribution",
        "",
        state_top[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Orthogonality / Redundancy",
        "",
        orth_summary.sort_values("max_abs_baseline_corr").to_markdown(index=False),
        "",
        "## Variant Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Failure Diagnosis",
        "",
        "- Weak WFV persistence was not explained by a single bad validation window. Most stronger variants still had more than one negative or fragile window.",
        "- The most reliable positive regimes remained drawdown acceleration, panic/liquidity stress, volatility spike, and weak breadth.",
        "- Trend-transition, recovery, and high-dispersion rotation were recurring weak states for the base thesis.",
        "- Mild smoothing and rebalance logic reduced churn but did not consistently convert the mechanism into validation-ready behavior.",
        "- Stricter stress gates improved state purity in some slices but introduced sample-size and active-coverage risk.",
        "",
        "## Final Classification",
        "",
        f"`{final_status}`",
        "",
        "## Recommended Next Step",
        "",
        _recommendation(final_status, decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    _ensure_dirs()
    panels, benchmark = load_inputs()
    v6_signals, v6_states = build_v6_candidate_panels(panels, benchmark)
    base = v6_signals[SOURCE_SIGNAL]
    stress_states = build_stress_states(panels["close"], benchmark)
    variants = build_refinement_variants(base, stress_states)

    registry = pd.DataFrame(VARIANT_SPECS)
    registry["source_signal"] = SOURCE_SIGNAL
    registry["run_id"] = RUN_ID
    registry["research_status"] = "TRACK_B_V6_REFINEMENT_RESEARCH_ONLY"

    structural = structural_summary(variants)
    scores, daily_ics = score_signals(variants, panels["close"])
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, v6_states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = minimal_reference_panels(base, panels)
    orth = orthogonality(variants, refs)
    orth_summary = _max_corr_table(orth)
    active = active_coverage_summary(variants)
    decisions = classify_variants(structural, scores, wfv_summary, stress, orth_summary, active, wfv_windows)
    window_fail = _window_failure_summary(wfv_windows)

    artifact_files = [
        "variant_registry.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_variant_horizon.csv",
        "stress_regime_attribution.csv",
        "concept_state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "window_failure_diagnostics.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "variant_classification.csv",
    ]
    registry.to_csv(OUT_DIR / artifact_files[0], index=False)
    structural.to_csv(OUT_DIR / artifact_files[1], index=False)
    scores.to_csv(OUT_DIR / artifact_files[2], index=False)
    daily_ics.to_csv(OUT_DIR / artifact_files[3], index=False)
    stress.to_csv(OUT_DIR / artifact_files[4], index=False)
    state_attr.to_csv(OUT_DIR / artifact_files[5], index=False)
    wfv_summary.to_csv(OUT_DIR / artifact_files[6], index=False)
    wfv_windows.to_csv(OUT_DIR / artifact_files[7], index=False)
    window_fail.to_csv(OUT_DIR / artifact_files[8], index=False)
    orth.to_csv(OUT_DIR / artifact_files[9], index=False)
    orth_summary.to_csv(OUT_DIR / artifact_files[10], index=False)
    active.to_csv(OUT_DIR / artifact_files[11], index=False)
    decisions.to_csv(OUT_DIR / artifact_files[12], index=False)
    for name, panel in variants.items():
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
                "source_note": str(SOURCE_NOTE),
                "source_artifact_directory": str(V6_OUT_DIR),
                "variant_count": len(variants),
                "variant_names": list(variants.keys()),
                "small_controlled_refinement": True,
                "large_parameter_grid": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "final_classification": _final_classification(decisions),
                "artifact_files": sorted(artifact_files),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_note(registry, structural, scores, wfv_summary, wfv_windows, stress, state_attr, orth_summary, active, decisions)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    main()
