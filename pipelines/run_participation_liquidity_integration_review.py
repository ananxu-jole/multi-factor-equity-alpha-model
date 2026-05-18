from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


RUN_ID = "participation_liquidity_integration_review_v1"
SIGNAL_NAME = "participation_liquidity_state_shift_20_60"
VALIDATION_DIR = Path("artifacts/research/participation_liquidity_conditional_validation_v1")
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md")

FIXED_VARIANTS = [
    "rank_persist_10_state_TREND_HOSTILE_zero",
    "rebalance_10_state_WEAK_BREADTH_zero",
    "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero",
    "rebalance_20",
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_fixed_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ranked = pd.read_csv(VALIDATION_DIR / "ranked_conditional_validation_summary.csv")
    windows = pd.read_csv(VALIDATION_DIR / "h20_window_diagnostics.csv")
    states = pd.read_csv(VALIDATION_DIR / "regime_stress_attribution.csv")
    peers = pd.read_csv(VALIDATION_DIR / "inter_variant_similarity_pairs.csv")
    fixed = ranked[ranked["variant_name"].isin(FIXED_VARIANTS)].copy()
    fixed["recommended_role"] = fixed["variant_name"].map(
        {
            "rank_persist_10_state_TREND_HOSTILE_zero": "PRIMARY_CONDITIONAL_VARIANT",
            "rebalance_10_state_WEAK_BREADTH_zero": "SECONDARY_STATE_CONFIRMATION",
            "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero": "STRESS_CONFIRMATION_VARIANT",
            "rebalance_20": "BROAD_FALLBACK_CONTROL",
        }
    )
    fixed["state_semantics"] = fixed["variant_name"].map(
        {
            "rank_persist_10_state_TREND_HOSTILE_zero": "Activates during hostile trend states with rank-persistence turnover control.",
            "rebalance_10_state_WEAK_BREADTH_zero": "Activates during weak breadth states with 10-day rebalance turnover control.",
            "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero": "Activates during weak breadth, drawdown, or panic/liquidity stress states.",
            "rebalance_20": "Broad always-available smoothed reference; not a conditional primary.",
        }
    )
    fixed = fixed.sort_values("validation_score", ascending=False)
    return fixed, windows[windows["variant_name"].isin(FIXED_VARIANTS)], states[states["variant_name"].isin(FIXED_VARIANTS)], peers


def _guardrails() -> pd.DataFrame:
    rows = [
        ("parameter_lock", "Freeze the four fixed variants exactly as validated; no further tuning before integration review.", "Required before any rebuild."),
        ("semantic_preservation", "Rebuild must preserve state labels, inactive handling, rebalance/rank-persistence logic, and sign convention.", "Fail on formula drift."),
        ("equivalence_rebuild_test", "Compare rebuilt panels against validation artifacts for values, ranks, coverage, turnover, h20 IC, and WFV-style metrics.", "Fail or hold on unexplained drift."),
        ("active_state_coverage", "Primary conditional variants should retain active-date coverage near or above 0.30 and active-window coverage of 1.00.", "Hold if sparse windows reappear."),
        ("turnover_ceiling", "Keep turnover at or below 0.10 for conditional variants; broad fallback should remain materially lower.", "Hold if churn returns."),
        ("similarity_ceiling", "Keep max baseline similarity below 0.45 during integration review.", "Hold if it collapses into a prior reversal/liquidity proxy."),
        ("peer_similarity_review", "High peer similarity is acceptable only as representation redundancy, not evidence for multiple independent alphas.", "Prefer one primary plus confirmations."),
        ("window_concentration", "Reject or hold if one-window dominance rises materially above 0.60.", "Prevents one-window dominated conditional edge."),
        ("rollback_trigger", "Rollback if h20 IC, WFV-style persistence/sign consistency, turnover, or baseline similarity materially deteriorate in rebuild.", "Research rollback only; no production mutation."),
        ("production_boundary", "No survivor/watchlist promotion, alpha pool mutation, portfolio use, ML use, or production Conditional-Alpha path changes.", "Hard boundary."),
    ]
    return pd.DataFrame(rows, columns=["guardrail", "requirement", "review_action"])


def _decision_options(fixed: pd.DataFrame) -> pd.DataFrame:
    primary = fixed.iloc[0]
    rows = [
        {
            "option": "one_primary_conditional_variant",
            "assessment": "Preferred",
            "rationale": f"`{primary['variant_name']}` has the strongest validation score and clean hostile-trend semantics, but should be checked against h20-only rebuild behavior because its best horizon is h10.",
        },
        {
            "option": "small_variant_ensemble",
            "assessment": "Not preferred for v1",
            "rationale": "The conditional variants are highly related. An ensemble risks double-counting the same participation/liquidity state information.",
        },
        {
            "option": "broad_fallback_version",
            "assessment": "Use as control/fallback",
            "rationale": "`rebalance_20` has broad coverage, low turnover, and stable h20 behavior, but it is less semantically conditional and should not be the primary conditional alpha representation.",
        },
        {
            "option": "hold_outside_integration",
            "assessment": "Not supported by current evidence",
            "rationale": "Four variants passed strict validation, sample sizes were adequate, and baseline similarity stayed moderate-low.",
        },
    ]
    return pd.DataFrame(rows)


def _classify(fixed: pd.DataFrame) -> str:
    primary = fixed.iloc[0]
    strict_count = int(fixed["strict_pass"].sum())
    if (
        strict_count >= 3
        and primary["h20_mean_ic"] >= 0.02
        and primary["persistence"] >= 1.0
        and primary["sign_consistency"] >= 1.0
        and primary["turnover_proxy"] <= 0.10
        and primary["max_abs_baseline_corr"] <= 0.45
    ):
        return "CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS"
    if strict_count >= 1:
        return "CONDITIONAL_ALPHA_REVIEW_READY"
    return "HOLD_OUTSIDE_INTEGRATION"


def _write_note(
    fixed: pd.DataFrame,
    windows: pd.DataFrame,
    states: pd.DataFrame,
    guardrails: pd.DataFrame,
    options: pd.DataFrame,
    final: str,
) -> None:
    primary = fixed.iloc[0]
    backup = fixed[fixed["variant_name"].eq("rebalance_10_state_WEAK_BREADTH_zero")].iloc[0]
    fallback = fixed[fixed["variant_name"].eq("rebalance_20")].iloc[0]
    focus_states = states[
        states["state"].isin(["TREND_HOSTILE", "WEAK_BREADTH", "DRAWDOWN", "PANIC_LIQUIDITY_STRESS", "VOLATILITY_SPIKE", "STRESS_OR_WEAK_BREADTH"])
    ].sort_values(["variant_name", "mean_ic"], ascending=[True, False])
    lines = [
        "# Participation Liquidity Conditional-Alpha Integration Review",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only integration review package evaluates `{SIGNAL_NAME}` after formal conditional validation.",
        "",
        f"Final classification: `{final}`.",
        "",
        f"Recommended representation: one primary conditional variant, `{primary['variant_name']}`, with `{backup['variant_name']}` as the first state-confirmation backup and `rebalance_20` as a broad fallback/control.",
        "",
        "This is not production registration, survivor/watchlist promotion, portfolio integration, ML integration, or a production Conditional-Alpha path change.",
        "",
        "## Fixed Candidate Set",
        "",
        fixed[[
            "variant_name",
            "recommended_role",
            "best_horizon",
            "h20_mean_ic",
            "h20_positive_ic_rate",
            "effective_test_ic_ir",
            "persistence",
            "sign_consistency",
            "h20_one_window_dominance",
            "turnover_proxy",
            "active_date_coverage",
            "active_window_coverage",
            "max_abs_baseline_corr",
            "max_abs_peer_corr",
            "state_semantics",
        ]].to_markdown(index=False),
        "",
        "## Representation Decision",
        "",
        options.to_markdown(index=False),
        "",
        "## Why The Choice Is State-Dependent",
        "",
        "- The strongest variants are explicitly activated by hostile trend, weak breadth, or stress/weak-breadth states.",
        "- `rebalance_20` is broadly stable and low turnover, but its broad coverage makes it more appropriate as a fallback/control than the main conditional representation.",
        "- High peer similarity among several state variants means they should not be treated as independent alpha sleeves at this stage.",
        "- The primary candidate has strong h20 behavior despite best horizon h10, so h20 alignment should be explicitly retested during any rebuild.",
        "",
        "## State And Stress Snapshot",
        "",
        focus_states[["variant_name", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Window Stability Snapshot",
        "",
        windows[["variant_name", "window", "start_date", "end_date", "h20_mean_ic", "h20_positive_ic_rate", "valid_ic_dates"]].to_markdown(index=False),
        "",
        "## Required Guardrails",
        "",
        guardrails.to_markdown(index=False),
        "",
        "## Risks",
        "",
        "- Selection risk remains because the validated variants are related and came from a focused refinement search.",
        "- Peer similarity is high among conditional rebalance variants, so an ensemble could create false diversification.",
        "- The primary variant has best horizon h10 while the integration target is h20; this needs explicit h20 preservation checks.",
        "- State definitions must be frozen before any integration review to avoid regime-label overfitting.",
        "- Broad fallback behavior may look cleaner because of smoothing and lower turnover; it should not be mistaken for proof of a universal alpha.",
        "",
        "## Required Tests Before Any Future Production Consideration",
        "",
        "- Isolated rebuild/equivalence test against the fixed validation artifacts.",
        "- Active-state WFV diagnostic with the frozen state definitions.",
        "- Recomputed baseline and peer-similarity audit against current Track A/Track B references.",
        "- Turnover and active-window coverage review under the exact intended inactive handling.",
        "- Side-by-side comparison of primary conditional variant, weak-breadth backup, stress/weak-breadth backup, and broad fallback.",
        "- Explicit rollback memo before any production-candidate registration design.",
        "",
        "## Final Recommendation",
        "",
        "Proceed to a research-only Conditional-Alpha integration review design using the fixed four-variant package. Do not register the signal, promote it, add it to survivor/watchlist state, or wire it into production alpha construction.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    fixed, windows, states, peers = _load_fixed_tables()
    guardrails = _guardrails()
    options = _decision_options(fixed)
    final = _classify(fixed)

    fixed.to_csv(OUT_DIR / "fixed_variant_integration_review.csv", index=False)
    windows.to_csv(OUT_DIR / "fixed_variant_window_review.csv", index=False)
    states.to_csv(OUT_DIR / "fixed_variant_state_attribution.csv", index=False)
    peers.to_csv(OUT_DIR / "source_peer_similarity_pairs.csv", index=False)
    guardrails.to_csv(OUT_DIR / "integration_guardrails.csv", index=False)
    options.to_csv(OUT_DIR / "representation_decision_options.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "signal_name": SIGNAL_NAME,
                "research_only": True,
                "production_logic_modified": False,
                "promotion_or_registration": False,
                "final_classification": final,
                "fixed_variant_count": len(fixed),
                "recommended_primary_variant": fixed.iloc[0]["variant_name"],
                "recommended_fallback_control": "rebalance_20",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(fixed, windows, states, guardrails, options, final)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"FINAL_CLASSIFICATION {final}")
    print(fixed[["variant_name", "recommended_role", "h20_mean_ic", "turnover_proxy", "active_date_coverage", "max_abs_baseline_corr"]].to_string(index=False))


if __name__ == "__main__":
    main()
