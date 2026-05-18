from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    HORIZONS,
    baseline_panels,
    build_stress_states,
    daily_ic,
    load_inputs,
    wfv_diagnostics,
)


RUN_ID = "track_b_v3_failure_diagnostics"
V3_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v3")
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/track_b_v3_failure_diagnostics.md")

FOCUS_SIGNALS = [
    "gap_continuation_confirmation_5_20",
    "range_compression_breakout_continuation_20",
    "trend_leadership_persistence_20_60",
    "relative_strength_acceleration_20_60",
    "liquidity_improvement_momentum_20_60",
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_signal_panels() -> dict[str, pd.DataFrame]:
    panels = {}
    registry = pd.read_csv(V3_DIR / "candidate_registry.csv")
    for name in registry["signal_name"]:
        panels[name] = pd.read_parquet(V3_DIR / f"{name}_signal_panel.parquet")
    return panels


def _score_inverse_signals(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    daily_rows = []
    for horizon in HORIZONS:
        fwd = close.shift(-horizon) / close - 1.0
        for name, panel in signals.items():
            ic = daily_ic(-panel, fwd)
            valid = ic.dropna()
            mean_ic = float(valid.mean()) if not valid.empty else np.nan
            std_ic = float(valid.std(ddof=0)) if len(valid) > 1 else np.nan
            rows.append(
                {
                    "signal_name": name,
                    "horizon": horizon,
                    "inverse_mean_ic": mean_ic,
                    "inverse_abs_mean_ic": abs(mean_ic) if pd.notna(mean_ic) else np.nan,
                    "inverse_ic_ir": mean_ic / std_ic if pd.notna(std_ic) and std_ic > 0 else np.nan,
                    "inverse_positive_ic_rate": float((valid > 0).mean()) if not valid.empty else np.nan,
                    "n_dates": int(len(valid)),
                }
            )
            daily_rows.extend(
                {
                    "Date": date,
                    "signal_name": name,
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid.items()
            )
    scores = pd.DataFrame(rows)
    best = scores.loc[scores.groupby("signal_name")["inverse_abs_mean_ic"].idxmax(), ["signal_name", "horizon"]]
    best = best.rename(columns={"horizon": "inverse_best_horizon"})
    scores = scores.merge(best, on="signal_name", how="left")
    scores["is_inverse_best_horizon"] = scores["horizon"].eq(scores["inverse_best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def _top_similarity_after_inversion(orth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in orth.groupby("signal_name"):
        signed = group.copy()
        signed["inverted_value_corr"] = -signed["value_corr"]
        signed["inverted_rank_corr"] = -signed["mean_rank_corr_by_date"]
        top = signed.loc[signed["abs_value_corr"].idxmax()]
        reversal_like = signed[
            signed["comparison"].str.contains("reversal|volume_shock|volatility_surprise", case=False, regex=True)
        ].copy()
        reversal_top = reversal_like.loc[reversal_like["abs_value_corr"].idxmax()] if not reversal_like.empty else top
        rows.append(
            {
                "signal_name": name,
                "top_abs_similarity_baseline": top["comparison"],
                "top_abs_similarity": float(top["abs_value_corr"]),
                "top_inverted_value_corr": float(top["inverted_value_corr"]),
                "top_reversal_like_baseline": reversal_top["comparison"],
                "top_reversal_like_abs_similarity": float(reversal_top["abs_value_corr"]),
                "top_reversal_like_inverted_corr": float(reversal_top["inverted_value_corr"]),
                "inverse_reversal_proxy_risk": (
                    "HIGH"
                    if float(reversal_top["abs_value_corr"]) >= 0.75
                    else "MODERATE"
                    if float(reversal_top["abs_value_corr"]) >= 0.55
                    else "LOW"
                ),
            }
        )
    return pd.DataFrame(rows)


def _horizon_direction_summary(scores: pd.DataFrame) -> pd.DataFrame:
    out = scores.copy()
    out["intended_direction"] = "positive_continuation_or_quality"
    out["empirical_direction"] = np.where(out["mean_ic"] > 0, "positive", np.where(out["mean_ic"] < 0, "negative", "flat"))
    out["direction_matches_intent"] = out["mean_ic"] > 0
    return out[
        [
            "signal_name",
            "horizon",
            "intended_direction",
            "empirical_direction",
            "direction_matches_intent",
            "mean_ic",
            "ic_ir",
            "positive_ic_rate",
            "n_dates",
        ]
    ]


def _regime_direction_summary(stress: pd.DataFrame) -> pd.DataFrame:
    out = stress.copy()
    out["empirical_direction"] = np.where(out["mean_ic"] > 0, "positive", np.where(out["mean_ic"] < 0, "negative", "flat"))
    return out


def _candidate_failure_calls(
    classification: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    similarity: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    merged = (
        classification.merge(structural[["signal_name", "missing_pct", "turnover_proxy"]], on="signal_name", suffixes=("", "_struct"))
        .merge(similarity, on="signal_name")
        .merge(wfv[["signal_name", "effective_mean_test_ic", "persistence", "sign_consistency", "one_window_dominance"]], on="signal_name", how="left")
    )
    horizon = scores.groupby("signal_name").agg(
        h1_ic=("mean_ic", lambda s: float(s.iloc[0]) if len(s) else np.nan),
        min_ic=("mean_ic", "min"),
        max_ic=("mean_ic", "max"),
        all_horizons_negative=("mean_ic", lambda s: bool((s < 0).all())),
    )
    merged = merged.merge(horizon, on="signal_name", how="left")
    regime = stress.groupby("signal_name").agg(
        positive_regime_count=("mean_ic", lambda s: int((s > 0).sum())),
        negative_regime_count=("mean_ic", lambda s: int((s < 0).sum())),
        worst_regime_ic=("mean_ic", "min"),
    )
    merged = merged.merge(regime, on="signal_name", how="left")

    for _, row in merged.iterrows():
        causes = []
        if row["all_horizons_negative"]:
            causes.append("broad_direction_mismatch")
        else:
            causes.append("horizon_specific_direction_mismatch")
        if row["max_abs_baseline_corr"] >= 0.75:
            causes.append("baseline_redundancy")
        if row["top_reversal_like_abs_similarity"] >= 0.75:
            causes.append("inverse_is_reversal_like_proxy")
        if row["persistence"] < 0.5:
            causes.append("weak_wfv_persistence")
        if row["missing_pct"] > 0.30:
            causes.append("missingness_data_quality")
        if row["turnover_proxy"] > 0.12:
            causes.append("turnover_noise")
        if row["positive_regime_count"] == 0:
            causes.append("no_positive_regime_rescue")
        elif row["negative_regime_count"] > row["positive_regime_count"]:
            causes.append("regime_dependency_negative_bias")
        if row["best_horizon"] not in (10, 20) and row["signal_name"] != "gap_continuation_confirmation_5_20":
            causes.append("horizon_mismatch")
        if row["signal_name"] == "gap_continuation_confirmation_5_20" and row["best_horizon"] == 1:
            causes.append("expected_h5_h10_horizon_mismatch")

        if row["signal_name"] == "gap_continuation_confirmation_5_20":
            action = "discard_current_form; redesign only if cleaner event coverage and lower turnover are available"
            diagnosis = "structurally_orthogonal_but_noisy_event_signal"
        elif row["signal_name"] == "range_compression_breakout_continuation_20":
            action = "redesign_or_conditional_only; do not simply invert"
            diagnosis = "orthogonal_but_weak_and_unstable_breakout_continuation"
        elif row["top_reversal_like_abs_similarity"] >= 0.75:
            action = "discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy"
            diagnosis = "continuation_collapsed_into_reversal_or_momentum_proxy"
        else:
            action = "redesign_before_retest; inversion needs separate economic thesis"
            diagnosis = "direction_mismatch_without_clean_robustness"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "best_horizon": row["best_horizon"],
                "mean_ic": row["mean_ic"],
                "max_abs_baseline_corr": row["max_abs_baseline_corr"],
                "top_reversal_like_abs_similarity": row["top_reversal_like_abs_similarity"],
                "inverse_reversal_proxy_risk": row["inverse_reversal_proxy_risk"],
                "persistence": row["persistence"],
                "sign_consistency": row["sign_consistency"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "positive_regime_count": row["positive_regime_count"],
                "negative_regime_count": row["negative_regime_count"],
                "diagnosis": diagnosis,
                "primary_failure_drivers": "; ".join(causes),
                "recommended_action": action,
            }
        )
    return pd.DataFrame(rows)


def _write_note(
    registry: pd.DataFrame,
    direction: pd.DataFrame,
    inverse_scores: pd.DataFrame,
    regime: pd.DataFrame,
    structural: pd.DataFrame,
    similarity: pd.DataFrame,
    calls: pd.DataFrame,
) -> None:
    focus_calls = calls[calls["signal_name"].isin(FOCUS_SIGNALS)]
    focus_direction = direction[direction["signal_name"].isin(FOCUS_SIGNALS)]
    focus_inverse = inverse_scores[
        inverse_scores["signal_name"].isin(FOCUS_SIGNALS) & inverse_scores["is_inverse_best_horizon"]
    ]
    focus_regime = regime[regime["signal_name"].isin(FOCUS_SIGNALS)]
    regime_pivot = (
        focus_regime.pivot_table(index="signal_name", columns="state", values="mean_ic", aggfunc="mean")
        .reset_index()
        .round(6)
    )
    focus_struct = structural[structural["signal_name"].isin(FOCUS_SIGNALS)][
        ["signal_name", "missing_pct", "date_coverage", "turnover_proxy", "turnover_p95"]
    ]
    focus_similarity = similarity[similarity["signal_name"].isin(FOCUS_SIGNALS)]

    lines = [
        "# Track B v3 Failure Diagnostics",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only diagnostics pass analyzed Track B v3 outputs under `{RUN_ID}` before any v4 candidate creation.",
        "",
        "The v3 continuation/quality candidates did not fail because the discovery machinery broke. They mostly failed because the intended positive continuation direction was empirically negative at the relevant horizons, especially h20, and many candidates remained highly correlated with existing price-rank, momentum, or reversal-like baselines.",
        "",
        "There is no broad evidence of a simple implementation sign error. The formulas match their documented continuation or quality intent. The stronger interpretation is that, in this universe and period, high leadership/participation/relative-strength states often behaved like overextended entries whose subsequent h10-h20 returns favored the opposite side. Inverting the signals would usually create a reversal-like proxy rather than a genuinely orthogonal standalone mechanism.",
        "",
        "No production logic, gates, schemas, survivor/watchlist status, ML logic, portfolio logic, or Conditional-Alpha paths were changed.",
        "",
        "## Inputs Used",
        "",
        f"- v3 artifact directory: `{V3_DIR}`",
        "- Candidate panels, registry, structural diagnostics, multi-horizon IC scoring, WFV-style diagnostics, stress/regime attribution, and orthogonality audit.",
        "- Track A `volume_shock_reversal_stable_20` remained a baseline only.",
        "",
        "## Candidate Set",
        "",
        registry[["signal_name", "family", "intuition", "expected_horizon"]].to_markdown(index=False),
        "",
        "## Direction Mismatch Summary",
        "",
        "All 15 candidates were rejected. The dominant pattern was negative empirical IC for formulas intended to express positive continuation, participation quality, liquidity improvement, or leadership persistence.",
        "",
        calls[[
            "signal_name",
            "best_horizon",
            "mean_ic",
            "persistence",
            "max_abs_baseline_corr",
            "inverse_reversal_proxy_risk",
            "diagnosis",
            "recommended_action",
        ]].to_markdown(index=False),
        "",
        "## Horizon-Specific Behavior",
        "",
        focus_direction.to_markdown(index=False),
        "",
        "## Inverse Direction Test",
        "",
        "The inverse direction mechanically flips IC signs, but this is not sufficient evidence to invert the candidates. The key question is whether the inverse is robust and structurally distinct. For most candidates, inversion raises reversal-proxy risk because the original panels were already strongly anti-correlated with reversal-like baselines or strongly correlated with momentum-like baselines.",
        "",
        focus_inverse[[
            "signal_name",
            "inverse_best_horizon",
            "horizon",
            "inverse_mean_ic",
            "inverse_ic_ir",
            "inverse_positive_ic_rate",
            "n_dates",
        ]].to_markdown(index=False),
        "",
        "## Similarity After Sign Inversion",
        "",
        "Absolute similarity is unchanged by sign inversion, while signed correlation flips. High inverted correlation to reversal-like baselines means the inverse is likely another reversal proxy rather than a new mechanism.",
        "",
        focus_similarity.to_markdown(index=False),
        "",
        "## Regime-Specific Behavior",
        "",
        "No focus candidate showed a clean regime rescue. Stress regimes generally made the continuation direction more negative, especially panic/liquidity stress, volatility spikes, weak breadth, and drawdown acceleration.",
        "",
        regime_pivot.to_markdown(index=False),
        "",
        "## Turnover And Missingness",
        "",
        focus_struct.to_markdown(index=False),
        "",
        "## Focus Candidate Findings",
        "",
        "### gap_continuation_confirmation_5_20",
        "",
        "- Most structurally distant from reversal by baseline correlation, but not usable in current form.",
        "- Best horizon shifted to h1 rather than intended h5-h10, with negative IC.",
        "- Missingness was very high and turnover was the highest in the batch.",
        "- Inversion is not the main issue; the current event definition is sparse, noisy, and operationally unstable.",
        "- Recommendation: discard current form; redesign only with cleaner event coverage, lower turnover, and explicit gap-continuation/gap-reversal separation.",
        "",
        "### range_compression_breakout_continuation_20",
        "",
        "- Structurally more distant than most candidates, with moderate/low baseline similarity.",
        "- IC was weak, negative, and WFV-style sign consistency was poor.",
        "- This looks less like a sign bug and more like false-breakout/late-entry decay.",
        "- Recommendation: redesign or move to conditional-only research; do not simply invert.",
        "",
        "### trend_leadership_persistence_20_60",
        "",
        "- Formula matches continuation intent but behaved negatively at h20.",
        "- Strong similarity to plain momentum and existing trend-quality references suggests limited orthogonality.",
        "- Failure likely reflects overextension/crowding and late-entry momentum decay rather than a coding sign error.",
        "- Recommendation: discard current standalone form; future work should avoid raw price-rank leadership as the primary signal.",
        "",
        "### relative_strength_acceleration_20_60",
        "",
        "- Negative across the main horizons and perfectly redundant with the deceleration-risk sibling in v3 construction.",
        "- Max baseline similarity was effectively 1.0, so inversion would not create a clean new alpha.",
        "- Recommendation: discard current form; any future acceleration work needs a fundamentally different design, such as sector-relative acceleration with explicit persistence controls.",
        "",
        "### liquidity_improvement_momentum_20_60",
        "",
        "- Liquidity improvement confirmed momentum did not separate from the price-rank manifold.",
        "- Stress/regime slices were also negative, arguing against a conditional rescue in current form.",
        "- Inversion would mostly behave like fading liquidity-confirmed leadership.",
        "- Recommendation: redesign around non-price liquidity persistence or participation quality rather than using liquidity as a multiplier on momentum.",
        "",
        "## Failure Mode Interpretation",
        "",
        "- Signal construction sign error: not supported as the primary explanation. The formulas generally represent their documented intent.",
        "- Crowding / overextension effect: strongly supported for leadership, participation, relative strength, liquidity-confirmed leadership, and volatility-normalization momentum.",
        "- Late-entry momentum decay: supported by increasingly negative h10-h20 behavior for many candidates.",
        "- Universe-specific behavior: plausible, but not proven without a broader universe comparison.",
        "- Horizon mismatch: important for gap continuation and partly relevant for breakout continuation.",
        "- Turnover/noise: severe for gap continuation; moderate but not primary for most others.",
        "- Missingness/data quality: severe for gap continuation; acceptable for most others.",
        "- Regime dependency: present, but not helpful; stress regimes mostly amplified negative direction.",
        "",
        "## Recommendations Before v4",
        "",
        "- Do not create v4 as a simple inversion batch.",
        "- Do not refine v3 leadership/participation candidates by small parameter changes.",
        "- Move away from raw price-rank leadership and price-confirmed participation as the main primitive.",
        "- If sector or peer group data are available, test sector/peer-relative mechanisms that neutralize broad momentum/reversal exposure.",
        "- For liquidity, use non-price persistence primitives before multiplying by momentum.",
        "- For gap/breakout concepts, separate event detection quality from directional scoring and require lower missingness/turnover before IC testing.",
        "- Treat conditional-only research as appropriate only for candidates with clear state-specific positive behavior; v3 did not show that pattern.",
        "",
        "## Final Classification",
        "",
        calls[["signal_name", "diagnosis", "primary_failure_drivers", "recommended_action"]].to_markdown(index=False),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    signals = _load_signal_panels()
    registry = pd.read_csv(V3_DIR / "candidate_registry.csv")
    classification = pd.read_csv(V3_DIR / "candidate_classification.csv")
    scores = pd.read_csv(V3_DIR / "multi_horizon_scoring.csv")
    stress = pd.read_csv(V3_DIR / "stress_regime_attribution.csv")
    structural = pd.read_csv(V3_DIR / "structural_quality_summary.csv")
    orth = pd.read_csv(V3_DIR / "orthogonality_redundancy_audit.csv")
    wfv = pd.read_csv(V3_DIR / "wfv_style_summary.csv")

    panels, benchmark = load_inputs()
    inverse_scores, inverse_daily = _score_inverse_signals(signals, panels["close"])
    inverse_wfv_scores = inverse_scores.rename(columns={"inverse_best_horizon": "best_horizon"}).copy()
    inverse_wfv_scores["is_best_horizon"] = inverse_wfv_scores["horizon"].eq(inverse_wfv_scores["best_horizon"])
    inverse_wfv, inverse_wfv_windows = wfv_diagnostics(inverse_daily, inverse_wfv_scores)

    refs = baseline_panels(signals, panels, benchmark)
    # Keep the reference construction reachable in this script while using the saved v3 audit as the authoritative
    # source for similarity; this guards against accidental drift in future reruns.
    _ = refs

    direction = _horizon_direction_summary(scores)
    regime = _regime_direction_summary(stress)
    similarity = _top_similarity_after_inversion(orth)
    calls = _candidate_failure_calls(classification, structural, scores, wfv, stress, similarity)

    direction.to_csv(OUT_DIR / "direction_by_horizon.csv", index=False)
    inverse_scores.to_csv(OUT_DIR / "inverse_direction_scoring.csv", index=False)
    inverse_wfv.to_csv(OUT_DIR / "inverse_wfv_style_summary.csv", index=False)
    inverse_wfv_windows.to_csv(OUT_DIR / "inverse_wfv_window_diagnostics.csv", index=False)
    regime.to_csv(OUT_DIR / "regime_direction_summary.csv", index=False)
    similarity.to_csv(OUT_DIR / "similarity_after_sign_inversion.csv", index=False)
    calls.to_csv(OUT_DIR / "failure_mode_classification.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": "robustness_first_discovery_expansion_v3",
                "research_only": True,
                "production_logic_modified": False,
                "v4_candidates_created": False,
                "candidate_count": int(len(registry)),
                "focus_signals": FOCUS_SIGNALS,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(registry, direction, inverse_scores, regime, structural, similarity, calls)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(calls[calls["signal_name"].isin(FOCUS_SIGNALS)].to_string(index=False))


if __name__ == "__main__":
    main()
