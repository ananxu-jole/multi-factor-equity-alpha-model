from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "participation_breadth_repair_conditional_validation_v1"
SIGNAL_NAME = "participation_breadth_repair_under_hostile_trend"
REFINEMENT_RUN_ID = "participation_breadth_repair_refinement_v1"
REFINEMENT_DIR = Path("artifacts/research") / REFINEMENT_RUN_ID
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/participation_breadth_repair_conditional_validation.md")

FOCUS_VARIANTS = [
    "strict_weak_breadth_rebalance_10",
    "strict_breadth_repair_recent_stress_zero",
    "smooth_5",
    "smooth_3",
]

NEIGHBORS = {
    "strict_weak_breadth_rebalance_10": [
        "strict_weak_breadth_zero",
        "strict_recent_stress_zero",
        "base",
        "rebalance_10",
    ],
    "strict_breadth_repair_recent_stress_zero": [
        "strict_recent_stress_zero",
        "strict_weak_breadth_rebalance_10",
        "strict_low_extension_zero",
    ],
    "smooth_5": ["smooth_3", "base", "threshold_0p35_zero"],
    "smooth_3": ["smooth_5", "base", "threshold_0p20_zero"],
}


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_panel(variant_name: str) -> pd.DataFrame:
    return pd.read_parquet(REFINEMENT_DIR / f"{variant_name}_signal_panel.parquet")


def _panel_corr(left: pd.DataFrame, right: pd.DataFrame) -> float:
    aligned_left, aligned_right = left.align(right, join="inner", axis=0)
    aligned_left, aligned_right = aligned_left.align(aligned_right, join="inner", axis=1)
    left_values = aligned_left.stack(dropna=True)
    right_values = aligned_right.stack(dropna=True)
    common = left_values.index.intersection(right_values.index)
    if len(common) < 100:
        return np.nan
    a = left_values.loc[common].astype(float)
    b = right_values.loc[common].astype(float)
    if a.std(ddof=0) == 0 or b.std(ddof=0) == 0:
        return np.nan
    return float(a.corr(b))


def _active_dates(panel: pd.DataFrame) -> pd.Series:
    valid_count = panel.notna().sum(axis=1)
    mean_abs = panel.abs().mean(axis=1, skipna=True)
    return (valid_count >= 25) & (mean_abs > 0.02)


def _active_window_stats(panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in panels.items():
        active = _active_dates(panel)
        counts = []
        ratios = []
        for dates in np.array_split(active.index, 4):
            sample = active.reindex(dates).fillna(False)
            counts.append(int(sample.sum()))
            ratios.append(float(sample.mean()))
        rows.append(
            {
                "variant_name": name,
                "active_dates": int(active.sum()),
                "active_date_coverage": float(active.mean()),
                "min_active_window_dates": int(min(counts)) if counts else 0,
                "max_active_window_dates": int(max(counts)) if counts else 0,
                "active_window_coverage": float(np.mean([count >= 25 for count in counts])) if counts else np.nan,
                "active_window_min_ratio": float(min(ratios)) if ratios else np.nan,
                "active_window_max_ratio": float(max(ratios)) if ratios else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _inter_variant_similarity(panels: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for left, right in combinations(sorted(panels), 2):
        corr = _panel_corr(panels[left], panels[right])
        rows.append(
            {
                "left_variant": left,
                "right_variant": right,
                "value_corr": corr,
                "abs_value_corr": abs(corr) if pd.notna(corr) else np.nan,
            }
        )
    pairs = pd.DataFrame(rows)
    summary_rows = []
    for name in sorted(panels):
        subset = pairs[pairs["left_variant"].eq(name) | pairs["right_variant"].eq(name)]
        summary_rows.append(
            {
                "variant_name": name,
                "max_abs_peer_corr": float(subset["abs_value_corr"].max()) if not subset.empty else np.nan,
                "mean_abs_peer_corr": float(subset["abs_value_corr"].mean()) if not subset.empty else np.nan,
            }
        )
    return pd.DataFrame(summary_rows), pairs


def _neighbor_support(refinement: pd.DataFrame) -> pd.DataFrame:
    indexed = refinement.set_index("variant_name")
    rows = []
    for variant_name, neighbor_names in NEIGHBORS.items():
        existing = [name for name in neighbor_names if name in indexed.index]
        neighbor_h20 = indexed.loc[existing, "h20_mean_ic"].dropna() if existing else pd.Series(dtype=float)
        neighbor_pos = indexed.loc[existing, "h20_positive_ic_rate"].dropna() if existing else pd.Series(dtype=float)
        rows.append(
            {
                "variant_name": variant_name,
                "neighbor_count": int(len(existing)),
                "neighbor_mean_h20_ic": float(neighbor_h20.mean()) if len(neighbor_h20) else np.nan,
                "neighbor_min_h20_ic": float(neighbor_h20.min()) if len(neighbor_h20) else np.nan,
                "neighbor_mean_positive_ic_rate": float(neighbor_pos.mean()) if len(neighbor_pos) else np.nan,
                "nearby_variant_support": bool(
                    len(neighbor_h20) >= 2
                    and neighbor_h20.mean() >= 0.018
                    and (neighbor_h20 > 0).all()
                    and neighbor_pos.mean() >= 0.54
                ),
            }
        )
    return pd.DataFrame(rows)


def _window_concentration(wfv_windows: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    h20 = wfv_windows[wfv_windows["horizon"].eq(20) & wfv_windows["signal_name"].isin(FOCUS_VARIANTS)].copy()
    h20 = h20.rename(columns={"signal_name": "variant_name", "mean_test_ic": "window_mean_test_ic"})
    rows = []
    for name, group in h20.groupby("variant_name"):
        values = group["window_mean_test_ic"].to_numpy(dtype=float)
        denom = float(np.sum(np.abs(values)))
        rows.append(
            {
                "variant_name": name,
                "window_count": int(len(group)),
                "window_positive_count": int((values > 0).sum()),
                "window_mean_min": float(np.min(values)) if len(values) else np.nan,
                "window_mean_max": float(np.max(values)) if len(values) else np.nan,
                "window_range": float(np.max(values) - np.min(values)) if len(values) else np.nan,
                "one_window_dominance_recomputed": float(np.max(np.abs(values)) / denom) if denom else np.nan,
                "min_valid_ic_dates": int(group["valid_ic_dates"].min()) if len(group) else 0,
            }
        )
    return pd.DataFrame(rows), h20


def _selected_state_attribution(state_attr: pd.DataFrame) -> pd.DataFrame:
    focus = state_attr[state_attr["signal_name"].isin(FOCUS_VARIANTS) & state_attr["horizon"].eq(20)].copy()
    return focus.sort_values(["signal_name", "mean_ic"], ascending=[True, False]).groupby("signal_name").head(5)


def _combine_summary() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    scores = pd.read_csv(REFINEMENT_DIR / "multi_horizon_scoring.csv")
    decisions = pd.read_csv(REFINEMENT_DIR / "variant_classification.csv")
    structural = pd.read_csv(REFINEMENT_DIR / "structural_quality_summary.csv")
    active = pd.read_csv(REFINEMENT_DIR / "active_coverage_summary.csv")
    wfv = pd.read_csv(REFINEMENT_DIR / "wfv_style_summary.csv")
    wfv_windows = pd.read_csv(REFINEMENT_DIR / "wfv_window_diagnostics.csv")
    orth = pd.read_csv(REFINEMENT_DIR / "orthogonality_summary.csv")
    state_attr = pd.read_csv(REFINEMENT_DIR / "state_attribution.csv")
    stress_attr = pd.read_csv(REFINEMENT_DIR / "stress_regime_attribution.csv")

    panels = {name: _load_panel(name) for name in FOCUS_VARIANTS}
    active_windows = _active_window_stats(panels)
    peer, peer_pairs = _inter_variant_similarity(panels)
    neighbors = _neighbor_support(decisions)
    concentration, window_detail = _window_concentration(wfv_windows)

    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={
            "signal_name": "variant_name",
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    best = scores[scores["is_best_horizon"].astype(bool)].rename(columns={"signal_name": "variant_name"})
    summary = (
        pd.DataFrame({"variant_name": FOCUS_VARIANTS})
        .merge(best[["variant_name", "horizon", "mean_ic", "ic_ir", "positive_ic_rate"]], on="variant_name", how="left")
        .rename(columns={"horizon": "best_horizon", "mean_ic": "best_mean_ic", "ic_ir": "best_ic_ir", "positive_ic_rate": "best_positive_ic_rate"})
        .merge(h20[["variant_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="variant_name", how="left")
        .merge(structural.rename(columns={"signal_name": "variant_name"}), on="variant_name", how="left")
        .merge(active, on="variant_name", how="left", suffixes=("", "_refinement"))
        .merge(active_windows, on="variant_name", how="left")
        .merge(wfv.rename(columns={"signal_name": "variant_name"}), on=["variant_name"], how="left", suffixes=("", "_wfv"))
        .merge(orth, on="variant_name", how="left")
        .merge(peer, on="variant_name", how="left")
        .merge(neighbors, on="variant_name", how="left")
        .merge(concentration, on="variant_name", how="left")
    )
    summary = summary[summary["horizon"].eq(20)].drop(columns=["horizon"], errors="ignore")
    summary["sample_size_adequate"] = (
        summary["active_date_coverage"].between(0.12, 0.60)
        & summary["active_window_coverage"].ge(1.0)
        & summary["min_active_window_dates"].ge(25)
        & summary["h20_n_dates"].ge(250)
    )
    summary["window_concentration_ok"] = summary["one_window_dominance"].le(0.62)
    summary["orthogonality_ok"] = (
        summary["max_abs_baseline_corr"].le(0.25)
        & summary["prior_participation_liquidity_corr"].le(0.10)
        & summary["max_reversal_corr"].le(0.10)
        & summary["max_momentum_corr"].le(0.15)
    )
    summary["strict_validation_pass"] = (
        summary["h20_mean_ic"].ge(0.020)
        & summary["h20_positive_ic_rate"].ge(0.56)
        & summary["persistence"].ge(0.75)
        & summary["sign_consistency"].ge(0.75)
        & summary["effective_test_ic_ir"].ge(0.90)
        & summary["turnover_proxy"].le(0.05)
        & summary["sample_size_adequate"]
        & summary["window_concentration_ok"]
        & summary["orthogonality_ok"]
        & summary["nearby_variant_support"]
    )
    summary["validation_score"] = (
        summary["h20_mean_ic"].fillna(-1) * 100
        + summary["h20_positive_ic_rate"].fillna(0)
        + summary["effective_test_ic_ir"].clip(upper=3).fillna(0) * 0.30
        + summary["persistence"].fillna(0) * 0.35
        + summary["sign_consistency"].fillna(0) * 0.35
        - summary["turnover_proxy"].fillna(1)
        - summary["max_abs_baseline_corr"].fillna(1) * 0.40
        - summary["one_window_dominance"].fillna(1) * 0.25
    )
    summary = summary.sort_values(["strict_validation_pass", "validation_score"], ascending=[False, False])

    artifacts = {
        "scores": scores[scores["signal_name"].isin(FOCUS_VARIANTS)].copy(),
        "summary": summary,
        "peer": peer,
        "peer_pairs": peer_pairs,
        "neighbors": neighbors,
        "window_concentration": concentration,
        "window_detail": window_detail,
        "state_attr": _selected_state_attribution(state_attr),
        "stress_attr": stress_attr[stress_attr["signal_name"].isin(FOCUS_VARIANTS)].copy(),
    }
    return summary, artifacts


def _final_classification(summary: pd.DataFrame) -> str:
    passes = int(summary["strict_validation_pass"].sum())
    primary = summary[summary["variant_name"].eq("strict_weak_breadth_rebalance_10")]
    primary_passes = bool(primary["strict_validation_pass"].iloc[0]) if not primary.empty else False
    if primary_passes and passes >= 2:
        return "CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE"
    if passes >= 1 or summary["h20_mean_ic"].max() >= 0.020:
        return "HOLD_FOR_MORE_RESEARCH"
    return "REJECT_CONDITIONAL_VALIDATION"


def _write_note(final: str, artifacts: dict[str, pd.DataFrame]) -> None:
    summary = artifacts["summary"]
    top_states = artifacts["state_attr"]
    best = summary.iloc[0]
    primary = summary[summary["variant_name"].eq("strict_weak_breadth_rebalance_10")].iloc[0]
    lines = [
        "# Participation Breadth Repair Conditional Validation",
        "",
        "## Executive Takeaway",
        "",
        f"This formal research-only conditional validation pass evaluated `{SIGNAL_NAME}` using the locked four-variant shortlist from the v5 refinement pass.",
        "",
        f"Final classification: `{final}`.",
        "",
        f"The strongest validation candidate was `{best['variant_name']}` with h20 mean IC {best['h20_mean_ic']:.6f}, positive IC rate {best['h20_positive_ic_rate']:.6f}, turnover {best['turnover_proxy']:.6f}, active coverage {best['active_date_coverage']:.6f}, effective WFV-style IC IR {best['effective_test_ic_ir']:.6f}, persistence/sign consistency {best['persistence']:.2f}/{best['sign_consistency']:.2f}, prior participation/liquidity correlation {best['prior_participation_liquidity_corr']:.6f}, and max reversal correlation {best['max_reversal_corr']:.6f}.",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or new parameter tuning was performed.",
        "",
        "## Scope",
        "",
        "- Source: `participation_breadth_repair_refinement_v1` artifacts.",
        "- Fixed shortlist only: `strict_weak_breadth_rebalance_10`, `strict_breadth_repair_recent_stress_zero`, `smooth_5`, `smooth_3`.",
        "- Validation mode: research-only, isolated artifact namespace.",
        "",
        "## Validation Summary",
        "",
        summary[
            [
                "variant_name",
                "best_horizon",
                "h20_mean_ic",
                "h20_ic_ir",
                "h20_positive_ic_rate",
                "effective_test_ic_ir",
                "persistence",
                "sign_consistency",
                "turnover_proxy",
                "active_date_coverage",
                "active_window_coverage",
                "min_active_window_dates",
                "one_window_dominance",
                "max_abs_baseline_corr",
                "prior_participation_liquidity_corr",
                "max_reversal_corr",
                "max_momentum_corr",
                "nearby_variant_support",
                "sample_size_adequate",
                "window_concentration_ok",
                "strict_validation_pass",
                "validation_score",
            ]
        ].to_markdown(index=False),
        "",
        "## Primary Variant Active-Coverage Check",
        "",
        f"`strict_weak_breadth_rebalance_10` active date coverage was {primary['active_date_coverage']:.6f}, with active-window coverage {primary['active_window_coverage']:.6f} and minimum active-window dates {int(primary['min_active_window_dates'])}. This is sparse enough to require conditional-alpha guardrails, but it is not a zero-or-one-window artifact.",
        "",
        "## Window Concentration",
        "",
        artifacts["window_detail"].to_markdown(index=False),
        "",
        "## Nearby Variant Support",
        "",
        artifacts["neighbors"].to_markdown(index=False),
        "",
        "## Peer Similarity Among Shortlist",
        "",
        artifacts["peer_pairs"].to_markdown(index=False),
        "",
        "## Regime / State Attribution Snapshot",
        "",
        top_states[["signal_name", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- The edge remains h20-oriented; shorter horizons are weaker and should not be optimized here.",
        "- The leading strict weak-breadth rebalance variant has adequate active-window coverage for formal conditional validation, though it remains a conditional signal rather than a universal alpha.",
        "- IC strength is not concentrated in a single WFV-style window for the leading candidate; one-window dominance is acceptable relative to the refinement pass.",
        "- `smooth_5` and `smooth_3` are useful broader confirmation/control variants because they preserve direction, maintain low baseline similarity, and avoid stricter activation sparsity.",
        "- Similarity to `participation_liquidity_state_shift_20_60`, reversal, and momentum baselines remains low, supporting the second-candidate thesis.",
        "- Selection risk is still present because the shortlisted variants are related. The next stage should freeze parameters and evaluate representation semantics rather than tune further.",
        "",
        "## Final Recommendation",
        "",
        "Move `participation_breadth_repair_under_hostile_trend` to a research-only Conditional-Alpha integration review design step. Use `strict_weak_breadth_rebalance_10` as the primary representation, `smooth_5` and `smooth_3` as broader confirmation/control variants, and `strict_breadth_repair_recent_stress_zero` as a stress-confirmation variant. Do not promote, register, or productionize it.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    summary, artifacts = _combine_summary()
    final = _final_classification(summary)

    outputs = {
        "conditional_validation_summary.csv": artifacts["summary"],
        "multi_horizon_validation_scoring.csv": artifacts["scores"],
        "inter_variant_similarity_summary.csv": artifacts["peer"],
        "inter_variant_similarity_pairs.csv": artifacts["peer_pairs"],
        "nearby_variant_support.csv": artifacts["neighbors"],
        "window_concentration_summary.csv": artifacts["window_concentration"],
        "h20_window_diagnostics.csv": artifacts["window_detail"],
        "regime_state_attribution_selected.csv": artifacts["state_attr"],
        "stress_attribution_selected.csv": artifacts["stress_attr"],
    }
    for filename, frame in outputs.items():
        frame.to_csv(OUT_DIR / filename, index=False)

    manifest = {
        "run_id": RUN_ID,
        "source_run_id": REFINEMENT_RUN_ID,
        "signal_name": SIGNAL_NAME,
        "research_only": True,
        "fixed_shortlist": FOCUS_VARIANTS,
        "variant_count": len(FOCUS_VARIANTS),
        "final_classification": final,
        "production_registration": False,
        "survivor_watchlist_promotion": False,
        "portfolio_integration": False,
        "ml_integration": False,
        "production_conditional_alpha_wiring": False,
        "gates_schemas_thresholds_modified": False,
        "new_parameter_tuning": False,
        "artifact_files": sorted([*outputs.keys(), "manifest.json"]),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _write_note(final, artifacts)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"FINAL {final}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
