from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df
except Exception:
    import sys

    ROOT = Path(__file__).resolve().parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df


RUN_ID = "rank_coherence_family_discovery_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
CANDIDATE_INVENTORY_DIR = OUT_DIR / "candidate_inventory"
CANDIDATE_PANELS_DIR = OUT_DIR / "candidate_panels"
DISCOVERY_SUMMARY_DIR = OUT_DIR / "discovery_summary"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"
REDUNDANCY_SCREENING_DIR = OUT_DIR / "redundancy_screening"
IC_DISCOVERY_DIR = OUT_DIR / "ic_discovery"
GOVERNANCE_REVIEW_DIR = OUT_DIR / "governance_review"
SOURCE_PANEL_DIR = Path("artifacts/panels/signals")
PANEL_GENERATION_LOOKBACK_ROWS = 504
STATISTICAL_SCREENING_LOOKBACK_ROWS = 252

HARD_MAX_CANDIDATES = 12
INITIAL_CANDIDATE_COUNT = 10

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only scaffold for rank-coherence family discovery. Dry-run creates "
    "registry, manifest, scaffold summary, diagnostics, and metadata-only redundancy "
    "artifacts only. It does not generate panels, execute discovery, score IC, run "
    "refinement or validation, mutate governance, change thresholds, register "
    "production candidates, integrate ML, or promote/demote candidates."
)

SOURCE_PANEL_NAMES = [
    "relative_return_rank_20",
    "relative_return_zscore_60",
    "percentile_rank_stability_20",
    "trend_consistency_20_60",
    "trend_consistency_20_60_persistent",
    "smooth_trend_persistence_60",
    "residual_return_vs_universe_20",
    "expanded_reversal_5d",
    "close_position_reversal_5",
]

CANDIDATES: list[dict[str, str]] = [
    {
        "candidate_id": "rank_coherence_leadership_stability_01",
        "signal_name": "leadership_rank_retention_10_20",
        "family": "rank_coherence",
        "theme": "Leadership Stability",
        "horizon": "h10-h20",
        "feature_group": "leadership_stability",
        "intended_economic_hypothesis": "Durable top-ranked securities outperform when leadership remains orderly across adjacent windows.",
        "mechanism_thesis": "Durable top-ranked securities outperform when leadership remains orderly across adjacent windows.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus momentum and persistence controls",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "leadership_rank_retention_10_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_leadership_stability_02",
        "signal_name": "cross_window_rank_agreement_10_20",
        "family": "rank_coherence",
        "theme": "Leadership Stability",
        "horizon": "h10-h20",
        "feature_group": "leadership_stability",
        "intended_economic_hypothesis": "Securities with high cross-window rank agreement outperform because leadership is not transient.",
        "mechanism_thesis": "Securities with high cross-window rank agreement outperform because leadership is not transient.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus momentum and persistence controls",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "cross_window_rank_agreement_10_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_churn_avoidance_01",
        "signal_name": "churn_adjusted_rank_improvement_20",
        "family": "rank_coherence",
        "theme": "Rank Churn Avoidance",
        "horizon": "h10-h20",
        "feature_group": "rank_churn",
        "intended_economic_hypothesis": "Improving securities with low rank churn outperform noisy improvers.",
        "mechanism_thesis": "Improving securities with low rank churn outperform noisy improvers.",
        "redundancy_risk": "high",
        "redundancy_risk_detail": "high versus persistence lineage",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "churn_adjusted_rank_improvement_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_churn_avoidance_02",
        "signal_name": "relative_rank_turnover_resilience_20",
        "family": "rank_coherence",
        "theme": "Rank Churn Avoidance",
        "horizon": "h10-h20",
        "feature_group": "rank_churn",
        "intended_economic_hypothesis": "Securities with rank turnover below universe rank turnover retain more durable sponsorship.",
        "mechanism_thesis": "Securities with rank turnover below universe rank turnover retain more durable sponsorship.",
        "redundancy_risk": "high",
        "redundancy_risk_detail": "high versus persistence lineage",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "relative_rank_turnover_resilience_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_reversal_pressure_01",
        "signal_name": "rank_shock_reversion_pressure_5_20",
        "family": "rank_coherence",
        "theme": "Rank Reversal Pressure",
        "horizon": "h5-h10",
        "feature_group": "rank_reversal_pressure",
        "intended_economic_hypothesis": "Short-window rank shocks that disagree with medium-window rank structure mean-revert.",
        "mechanism_thesis": "Short-window rank shocks that disagree with medium-window rank structure mean-revert.",
        "redundancy_risk": "medium-high",
        "redundancy_risk_detail": "medium-high versus reversal baselines",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "rank_shock_reversion_pressure_5_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_reversal_pressure_02",
        "signal_name": "rank_acceleration_disagreement_5_20",
        "family": "rank_coherence",
        "theme": "Rank Reversal Pressure",
        "horizon": "h5-h10",
        "feature_group": "rank_reversal_pressure",
        "intended_economic_hypothesis": "Abrupt rank acceleration unsupported by broader rank order creates reversal pressure.",
        "mechanism_thesis": "Abrupt rank acceleration unsupported by broader rank order creates reversal pressure.",
        "redundancy_risk": "medium-high",
        "redundancy_risk_detail": "medium-high versus reversal baselines",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "rank_acceleration_disagreement_5_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_concentration_01",
        "signal_name": "leadership_concentration_quality_20",
        "family": "rank_coherence",
        "theme": "Leadership Concentration and Broadening",
        "horizon": "h10-h20",
        "feature_group": "leadership_concentration",
        "intended_economic_hypothesis": "Durable leaders outperform in concentrated leadership regimes when top-rank membership remains coherent.",
        "mechanism_thesis": "Durable leaders outperform in concentrated leadership regimes when top-rank membership remains coherent.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus momentum and breadth repair",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "leadership_concentration_quality_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_concentration_02",
        "signal_name": "leadership_broadening_entry_20",
        "family": "rank_coherence",
        "theme": "Leadership Concentration and Broadening",
        "horizon": "h10-h20",
        "feature_group": "leadership_concentration",
        "intended_economic_hypothesis": "New entrants into coherent leadership groups outperform during rank-map broadening.",
        "mechanism_thesis": "New entrants into coherent leadership groups outperform during rank-map broadening.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus breadth and participation repair",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "leadership_broadening_entry_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_regime_independent_01",
        "signal_name": "state_neutral_rank_coherence_20",
        "family": "rank_coherence",
        "theme": "Regime-Independent Rank Coherence",
        "horizon": "h10-h20",
        "feature_group": "regime_independent_coherence",
        "intended_economic_hypothesis": "Securities with stable rank agreement across ordinary states outperform without requiring stress repair.",
        "mechanism_thesis": "Securities with stable rank agreement across ordinary states outperform without requiring stress repair.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus prior transition-rank stability",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "state_neutral_rank_coherence_20.parquet"),
    },
    {
        "candidate_id": "rank_coherence_regime_independent_02",
        "signal_name": "nonhostile_transition_rank_coherence_20",
        "family": "rank_coherence",
        "theme": "Regime-Independent Rank Coherence",
        "horizon": "h10-h20",
        "feature_group": "regime_independent_coherence",
        "intended_economic_hypothesis": "Rank coherence that persists before and after non-hostile transitions identifies durable relative leadership.",
        "mechanism_thesis": "Rank coherence that persists before and after non-hostile transitions identifies durable relative leadership.",
        "redundancy_risk": "medium",
        "redundancy_risk_detail": "medium versus transition-state dynamics",
        "research_status": "RESEARCH_ONLY",
        "expected_artifact_path": str(CANDIDATE_PANELS_DIR / "nonhostile_transition_rank_coherence_20.parquet"),
    },
]

REQUIRED_REGISTRY_COLUMNS = {
    "candidate_id",
    "signal_name",
    "family",
    "theme",
    "horizon",
    "feature_group",
    "intended_economic_hypothesis",
    "redundancy_risk",
    "research_status",
    "expected_artifact_path",
    "run_id",
}

THEMES = {
    "Leadership Stability",
    "Rank Churn Avoidance",
    "Rank Reversal Pressure",
    "Leadership Concentration and Broadening",
    "Regime-Independent Rank Coherence",
}


def _artifact_dirs() -> tuple[Path, ...]:
    return (
        OUT_DIR,
        CANDIDATE_INVENTORY_DIR,
        CANDIDATE_PANELS_DIR,
        DISCOVERY_SUMMARY_DIR,
        DIAGNOSTICS_DIR,
        REDUNDANCY_SCREENING_DIR,
        IC_DISCOVERY_DIR,
        GOVERNANCE_REVIEW_DIR,
    )


def _ensure_dirs() -> None:
    for path in _artifact_dirs():
        path.mkdir(parents=True, exist_ok=True)


def candidate_registry() -> pd.DataFrame:
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    return registry


def validate_rank_coherence_registry(registry: pd.DataFrame) -> None:
    validate_registry_df(registry)
    missing = REQUIRED_REGISTRY_COLUMNS - set(registry.columns)
    if missing:
        raise RegistryValidationError(f"Rank-coherence registry missing columns: {sorted(missing)}")
    if len(registry) > HARD_MAX_CANDIDATES:
        raise RegistryValidationError(
            f"Rank-coherence registry has {len(registry)} candidates; hard max is {HARD_MAX_CANDIDATES}"
        )
    if len(registry) != INITIAL_CANDIDATE_COUNT:
        raise RegistryValidationError(
            f"Initial rank-coherence scaffold must contain exactly {INITIAL_CANDIDATE_COUNT} candidates"
        )
    if set(registry["family"]) != {"rank_coherence"}:
        raise RegistryValidationError("All rank-coherence scaffold candidates must use family=rank_coherence")
    if set(registry["research_status"]) != {"RESEARCH_ONLY"}:
        raise RegistryValidationError("All rank-coherence scaffold candidates must use research_status=RESEARCH_ONLY")
    unknown_themes = set(registry["theme"]) - THEMES
    if unknown_themes:
        raise RegistryValidationError(f"Unknown rank-coherence themes: {sorted(unknown_themes)}")
    theme_counts = registry["theme"].value_counts().to_dict()
    if any(count != 2 for count in theme_counts.values()) or set(theme_counts) != THEMES:
        raise RegistryValidationError("Initial rank-coherence scaffold must have exactly two candidates per theme")
    if registry["signal_name"].duplicated().any():
        raise RegistryValidationError("Duplicate signal_name in rank-coherence registry")


def _empty_statistical_redundancy_placeholder() -> pd.DataFrame:
    try:
        from pipelines.utils.redundancy_screening import STATISTICAL_REDUNDANCY_COLUMNS
    except Exception:
        import sys

        ROOT = Path(__file__).resolve().parent.parent
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from pipelines.utils.redundancy_screening import STATISTICAL_REDUNDANCY_COLUMNS

    return pd.DataFrame(columns=STATISTICAL_REDUNDANCY_COLUMNS)


def _write_manifest(registry: pd.DataFrame) -> None:
    manifest = {
        "run_id": RUN_ID,
        "research_only": True,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "candidate_count": int(len(registry)),
        "hard_max_candidate_count": HARD_MAX_CANDIDATES,
        "panel_generation_executed": False,
        "discovery_executed": False,
        "ic_scoring_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "production_registration": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "ml_integration": False,
        "candidate_promotion_or_demotion": False,
        "artifact_directories": {
            "candidate_inventory": str(CANDIDATE_INVENTORY_DIR),
            "candidate_panels": str(CANDIDATE_PANELS_DIR),
            "discovery_summary": str(DISCOVERY_SUMMARY_DIR),
            "diagnostics": str(DIAGNOSTICS_DIR),
            "redundancy_screening": str(REDUNDANCY_SCREENING_DIR),
            "ic_discovery": str(IC_DISCOVERY_DIR),
            "governance_review": str(GOVERNANCE_REVIEW_DIR),
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _write_research_manifest(registry: pd.DataFrame, panel_generation_executed: bool) -> None:
    manifest = {
        "run_id": RUN_ID,
        "research_only": True,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "candidate_count": int(len(registry)),
        "hard_max_candidate_count": HARD_MAX_CANDIDATES,
        "panel_generation_executed": bool(panel_generation_executed),
        "discovery_executed": False,
        "ic_scoring_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "production_registration": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "ml_integration": False,
        "candidate_promotion_or_demotion": False,
        "source_panel_dir": str(SOURCE_PANEL_DIR),
        "source_panel_names": SOURCE_PANEL_NAMES,
        "panel_generation_lookback_rows": PANEL_GENERATION_LOOKBACK_ROWS,
        "statistical_screening_lookback_rows": STATISTICAL_SCREENING_LOOKBACK_ROWS,
        "artifact_directories": {
            "candidate_inventory": str(CANDIDATE_INVENTORY_DIR),
            "candidate_panels": str(CANDIDATE_PANELS_DIR),
            "discovery_summary": str(DISCOVERY_SUMMARY_DIR),
            "diagnostics": str(DIAGNOSTICS_DIR),
            "redundancy_screening": str(REDUNDANCY_SCREENING_DIR),
            "ic_discovery": str(IC_DISCOVERY_DIR),
            "governance_review": str(GOVERNANCE_REVIEW_DIR),
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _write_scaffold_summary() -> None:
    (DISCOVERY_SUMMARY_DIR / "framework_scaffold_summary.md").write_text(
        """# Rank-Coherence Family Discovery Scaffold Summary

This scaffold prepares the research-only framework for rank-coherence family discovery.

- `candidate_inventory/candidate_registry.csv`: exact approved 10-candidate registry.
- `manifest.json`: research-only guardrails and artifact directory map.
- `redundancy_screening/metadata_redundancy_screening.csv`: metadata-only advisory screening.
- `redundancy_screening/statistical_redundancy_screening.csv`: empty compatibility placeholder; no panels are generated in dry-run.
- `diagnostics/guardrail_checklist.csv`: confirmation that dry-run did not execute discovery, panel generation, IC scoring, refinement, validation, governance mutation, threshold mutation, production registration, ML, or candidate promotion/demotion.
- `governance_review/`: research-only confirmation artifacts, not governance mutations.

`--dry-run` is scaffold-only. Candidate panels are intentionally not generated.
""",
        encoding="utf-8",
    )


def _write_guardrail_artifacts(panel_generation_executed: bool = False) -> None:
    guardrail_rows = [
        ("panel_generation_executed", bool(panel_generation_executed), "research-only --run generates panels; dry-run does not"),
        ("discovery_executed", False, "runner does not execute discovery scoring"),
        ("ic_scoring_executed", False, "runner does not score IC"),
        ("refinement_executed", False, "runner does not run refinement"),
        ("validation_executed", False, "runner does not run validation"),
        ("governance_modified", False, "runner does not mutate governance"),
        ("thresholds_modified", False, "runner does not modify thresholds"),
        ("production_registration", False, "runner does not register production candidates"),
        ("ml_integration", False, "runner does not implement ML"),
        ("candidate_promotion_or_demotion", False, "runner does not promote or demote candidates"),
    ]
    pd.DataFrame(guardrail_rows, columns=["check", "executed_or_modified", "notes"]).to_csv(
        DIAGNOSTICS_DIR / "guardrail_checklist.csv",
        index=False,
    )
    pd.DataFrame(
        [
            {"review_item": "governance_mutation", "status": "not_performed", "notes": "research-only scaffold"},
            {"review_item": "production_registration", "status": "not_performed", "notes": "research-only scaffold"},
            {"review_item": "threshold_mutation", "status": "not_performed", "notes": "research-only scaffold"},
            {"review_item": "validation_execution", "status": "not_performed", "notes": "research-only scaffold"},
            {"review_item": "ml_integration", "status": "not_performed", "notes": "research-only scaffold"},
        ]
    ).to_csv(GOVERNANCE_REVIEW_DIR / "research_only_guardrail_review.csv", index=False)
    pd.DataFrame(
        [{"confirmation": "no_governance_mutation", "status": True, "notes": "no governance files changed by runner"}]
    ).to_csv(GOVERNANCE_REVIEW_DIR / "no_governance_mutation_confirmation.csv", index=False)
    pd.DataFrame(
        [{"confirmation": "no_production_registration", "status": True, "notes": "no production paths are used"}]
    ).to_csv(GOVERNANCE_REVIEW_DIR / "no_production_registration_confirmation.csv", index=False)


def _write_schema_check(registry: pd.DataFrame) -> None:
    rows = [
        {"check": "candidate_count", "status": "pass", "observed": len(registry), "expected": INITIAL_CANDIDATE_COUNT},
        {"check": "hard_max_candidate_count", "status": "pass", "observed": len(registry), "expected": HARD_MAX_CANDIDATES},
        {
            "check": "required_columns",
            "status": "pass",
            "observed": ";".join(sorted(registry.columns)),
            "expected": ";".join(sorted(REQUIRED_REGISTRY_COLUMNS)),
        },
        {
            "check": "theme_count",
            "status": "pass",
            "observed": ";".join(f"{k}:{v}" for k, v in sorted(registry["theme"].value_counts().to_dict().items())),
            "expected": "two candidates per approved theme",
        },
    ]
    pd.DataFrame(rows).to_csv(CANDIDATE_INVENTORY_DIR / "candidate_registry_schema_check.csv", index=False)
    (CANDIDATE_INVENTORY_DIR / "candidate_registry_readme.md").write_text(
        "# Rank-Coherence Candidate Registry\n\n"
        "This registry contains the exact approved 10-candidate research-only scaffold. "
        "It is not a production registry and does not imply validation, promotion, or governance status.\n",
        encoding="utf-8",
    )


def _write_placeholder_outputs() -> None:
    pd.DataFrame(
        columns=[
            "candidate_id",
            "signal_name",
            "family",
            "theme",
            "horizon",
            "panel_path",
            "metadata_path",
            "row_count",
            "date_min",
            "date_max",
            "ticker_count",
            "generation_status",
        ]
    ).to_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv", index=False)
    pd.DataFrame(
        columns=["candidate_id", "signal_name", "non_null_observations", "research_status", "notes"]
    ).to_csv(DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv", index=False)
    pd.DataFrame(columns=["family", "theme", "candidate_count", "notes"]).to_csv(
        DISCOVERY_SUMMARY_DIR / "family_theme_summary.csv",
        index=False,
    )
    pd.DataFrame(columns=["source_panel", "status", "notes"]).to_csv(DIAGNOSTICS_DIR / "source_panel_inputs.csv", index=False)
    pd.DataFrame(columns=["signal_name", "diagnostic_type", "status", "notes"]).to_csv(
        DIAGNOSTICS_DIR / "panel_diagnostics.csv",
        index=False,
    )
    pd.DataFrame(columns=["signal_name", "diagnostic_type", "status", "notes"]).to_csv(
        DIAGNOSTICS_DIR / "structural_quality_diagnostics.csv",
        index=False,
    )
    pd.DataFrame(
        [
            {"prohibited_feature": "drawdown/post_drawdown", "status": "not_used_in_scaffold", "notes": "no formulas executed"},
            {"prohibited_feature": "hostile/stress repair", "status": "not_used_in_scaffold", "notes": "no formulas executed"},
            {"prohibited_feature": "participation/liquidity repair", "status": "not_used_in_scaffold", "notes": "no formulas executed"},
            {"prohibited_feature": "dispersion/volatility compression", "status": "not_used_in_scaffold", "notes": "no formulas executed"},
        ]
    ).to_csv(DIAGNOSTICS_DIR / "prohibited_feature_review.csv", index=False)
    for name in (
        "approved_scoring_subset.csv",
        "candidate_horizon_ic_scores.csv",
        "candidate_ic_summary.csv",
        "daily_ic_by_candidate_horizon.csv",
        "family_theme_ic_summary.csv",
        "horizon_ic_summary.csv",
    ):
        pd.DataFrame().to_csv(IC_DISCOVERY_DIR / name, index=False)
    (IC_DISCOVERY_DIR / "manifest.json").write_text(
        json.dumps({"ic_scoring_executed": False, "notes": "IC discovery is intentionally not run by scaffold dry-run."}, indent=2),
        encoding="utf-8",
    )


def _rank_cs(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.rank(axis=1, pct=True).sub(0.5).mul(2.0)


def _clean_panel(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.replace([np.inf, -np.inf], np.nan).clip(lower=-1.0, upper=1.0)


def _load_source_panels() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, object]] = []
    for name in SOURCE_PANEL_NAMES:
        path = SOURCE_PANEL_DIR / f"{name}.parquet"
        metadata_path = SOURCE_PANEL_DIR / f"{name}.metadata.json"
        if not path.exists():
            rows.append({"source_signal": name, "status": "missing", "path": str(path)})
            continue
        panel = pd.read_parquet(path)
        panel.index = pd.to_datetime(panel.index)
        panel = panel.sort_index()
        if PANEL_GENERATION_LOOKBACK_ROWS > 0:
            panel = panel.tail(PANEL_GENERATION_LOOKBACK_ROWS)
        metadata = {}
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        panels[name] = panel.astype(float)
        rows.append(
            {
                "source_signal": name,
                "status": "loaded",
                "path": str(path),
                "metadata_path": str(metadata_path),
                "rows": int(len(panel)),
                "tickers": int(len(panel.columns)),
                "date_min": str(panel.index.min().date()) if len(panel) else None,
                "date_max": str(panel.index.max().date()) if len(panel) else None,
                "source_created_at": metadata.get("created_at"),
            }
        )
    missing = [row["source_signal"] for row in rows if row["status"] == "missing"]
    if missing:
        raise FileNotFoundError(f"Missing required source signal panels: {', '.join(missing)}")
    return panels, pd.DataFrame(rows)


def _align_sources(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    common_index = None
    common_columns = None
    for panel in panels.values():
        common_index = panel.index if common_index is None else common_index.intersection(panel.index)
        common_columns = panel.columns if common_columns is None else common_columns.intersection(panel.columns)
    if common_index is None or common_columns is None or len(common_index) == 0 or len(common_columns) == 0:
        raise ValueError("Rank-coherence source panels do not share a usable date/ticker intersection.")
    return {
        name: panel.reindex(index=common_index, columns=common_columns).astype(float)
        for name, panel in panels.items()
    }


def _candidate_signal_panels(source: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    rr = _rank_cs(source["relative_return_rank_20"])
    rz = _rank_cs(source["relative_return_zscore_60"])
    stability = _rank_cs(source["percentile_rank_stability_20"])
    trend = _rank_cs(source["trend_consistency_20_60"])
    trend_persistent = _rank_cs(source["trend_consistency_20_60_persistent"])
    smooth = _rank_cs(source["smooth_trend_persistence_60"])
    residual = _rank_cs(source["residual_return_vs_universe_20"])
    reversal_5 = _rank_cs(source["expanded_reversal_5d"])
    close_reversal_5 = _rank_cs(source["close_position_reversal_5"])

    rank_churn = rr.diff().abs().rolling(20, min_periods=10).mean()
    universe_churn = rank_churn.mean(axis=1)
    relative_churn_resilience = rank_churn.rsub(universe_churn, axis=0)
    rank_improvement = rr.diff(20)
    short_shock = rr.diff(5).clip(lower=-1.0, upper=1.0)
    medium_anchor = trend.add(smooth, fill_value=0.0).div(2.0)
    rank_accel = rr.diff(5).sub(rr.diff(20), fill_value=0.0)
    top_rr = rr.ge(0.6).astype(float)
    top_trend = trend.ge(0.5).astype(float)
    leadership_retention = top_rr.rolling(10, min_periods=5).mean().add(
        top_trend.rolling(20, min_periods=10).mean(),
        fill_value=0.0,
    )
    leadership_concentration = top_rr.mean(axis=1)
    leadership_broadening = top_rr.mean(axis=1).diff(20).clip(lower=0.0)
    new_leadership_entry = top_rr.where(top_rr.shift(20).lt(0.5), 0.0)
    cross_window_disagreement = rr.sub(medium_anchor, fill_value=0.0).abs()
    state_neutral_agreement = (
        rr.add(trend, fill_value=0.0)
        .add(smooth, fill_value=0.0)
        .add(stability, fill_value=0.0)
        .sub(cross_window_disagreement, fill_value=0.0)
    )
    transition_coherence = (
        stability.add(trend.diff(20), fill_value=0.0)
        .add(smooth.diff(20), fill_value=0.0)
        .add(trend_persistent, fill_value=0.0)
        .sub(rr.diff(5).abs(), fill_value=0.0)
    )

    return {
        "leadership_rank_retention_10_20": _clean_panel(
            _rank_cs(leadership_retention.add(stability, fill_value=0.0).add(trend_persistent, fill_value=0.0))
        ),
        "cross_window_rank_agreement_10_20": _clean_panel(
            _rank_cs(
                rr.add(trend, fill_value=0.0)
                .add(smooth, fill_value=0.0)
                .sub(rr.sub(trend, fill_value=0.0).abs(), fill_value=0.0)
                .sub(rr.sub(smooth, fill_value=0.0).abs(), fill_value=0.0)
            )
        ),
        "churn_adjusted_rank_improvement_20": _clean_panel(
            _rank_cs(rank_improvement.add(stability, fill_value=0.0).sub(rank_churn, fill_value=0.0))
        ),
        "relative_rank_turnover_resilience_20": _clean_panel(
            _rank_cs(relative_churn_resilience.add(stability, fill_value=0.0).add(smooth, fill_value=0.0))
        ),
        "rank_shock_reversion_pressure_5_20": _clean_panel(
            _rank_cs(medium_anchor.sub(short_shock, fill_value=0.0).add(reversal_5, fill_value=0.0))
        ),
        "rank_acceleration_disagreement_5_20": _clean_panel(
            _rank_cs(
                rank_accel.mul(-1.0)
                .sub(cross_window_disagreement, fill_value=0.0)
                .add(close_reversal_5, fill_value=0.0)
            )
        ),
        "leadership_concentration_quality_20": _clean_panel(
            _rank_cs(rr.mul(leadership_concentration, axis=0).add(stability, fill_value=0.0).add(trend, fill_value=0.0))
        ),
        "leadership_broadening_entry_20": _clean_panel(
            _rank_cs(
                new_leadership_entry.mul(leadership_broadening, axis=0)
                .add(rank_improvement.clip(lower=0.0), fill_value=0.0)
                .add(residual, fill_value=0.0)
            )
        ),
        "state_neutral_rank_coherence_20": _clean_panel(_rank_cs(state_neutral_agreement)),
        "nonhostile_transition_rank_coherence_20": _clean_panel(_rank_cs(transition_coherence)),
    }


def _panel_to_long(panel: pd.DataFrame, candidate: pd.Series) -> pd.DataFrame:
    long_panel = panel.stack(future_stack=True).dropna().rename("signal_value").reset_index()
    long_panel.columns = ["date", "ticker", "signal_value"]
    long_panel["candidate_id"] = candidate["candidate_id"]
    long_panel["family"] = candidate["family"]
    long_panel["theme"] = candidate["theme"]
    long_panel["horizon"] = candidate["horizon"]
    return long_panel[["date", "ticker", "candidate_id", "signal_value", "family", "theme", "horizon"]]


def _write_candidate_panels(registry: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_panels, source_summary = _load_source_panels()
    source_panels = _align_sources(source_panels)
    generated = _candidate_signal_panels(source_panels)
    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    registry.to_csv(CANDIDATE_INVENTORY_DIR / "candidate_registry.csv", index=False)
    _write_schema_check(registry)
    for rec in registry.to_dict(orient="records"):
        signal_name = rec["signal_name"]
        panel = generated.get(signal_name)
        if panel is None:
            raise KeyError(f"No rank-coherence panel generation method registered for {signal_name}")
        candidate = pd.Series(rec)
        long_panel = _panel_to_long(panel, candidate)
        panel_path = CANDIDATE_PANELS_DIR / f"{signal_name}.parquet"
        metadata_path = CANDIDATE_PANELS_DIR / f"{signal_name}.metadata.json"
        long_panel.to_parquet(panel_path, index=False)
        metadata_path.write_text(
            json.dumps(
                {
                    "run_id": RUN_ID,
                    "candidate_id": rec["candidate_id"],
                    "signal_name": signal_name,
                    "research_only": True,
                    "panel_generation_only": True,
                    "source_panel_dir": str(SOURCE_PANEL_DIR),
                    "source_panel_names": SOURCE_PANEL_NAMES,
                    "lookback_rows": PANEL_GENERATION_LOOKBACK_ROWS,
                    "panel_format": "long",
                    "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                    "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                    "row_count": int(len(long_panel)),
                    "ticker_count": int(long_panel["ticker"].nunique()) if not long_panel.empty else 0,
                    "guardrails": {
                        "ic_scoring_executed": False,
                        "refinement_executed": False,
                        "validation_executed": False,
                        "governance_modified": False,
                        "thresholds_modified": False,
                        "production_registration": False,
                        "ml_integration": False,
                        "candidate_promotion_or_demotion": False,
                    },
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        manifest_rows.append(
            {
                "candidate_id": rec["candidate_id"],
                "signal_name": signal_name,
                "family": rec["family"],
                "theme": rec["theme"],
                "horizon": rec["horizon"],
                "feature_group": rec["feature_group"],
                "panel_path": str(panel_path),
                "metadata_path": str(metadata_path),
                "row_count": int(len(long_panel)),
                "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                "ticker_count": int(long_panel["ticker"].nunique()) if not long_panel.empty else 0,
                "generation_status": "generated",
            }
        )
        summary_rows.append(
            {
                "candidate_id": rec["candidate_id"],
                "signal_name": signal_name,
                "non_null_observations": int(len(long_panel)),
                "mean_signal_value": float(long_panel["signal_value"].mean()) if not long_panel.empty else np.nan,
                "std_signal_value": float(long_panel["signal_value"].std()) if len(long_panel) > 1 else np.nan,
                "min_signal_value": float(long_panel["signal_value"].min()) if not long_panel.empty else np.nan,
                "max_signal_value": float(long_panel["signal_value"].max()) if not long_panel.empty else np.nan,
                "research_status": rec["research_status"],
                "notes": "research-only candidate panel; no IC scoring, validation, refinement, or candidate decision applied",
            }
        )

    manifest = pd.DataFrame(manifest_rows)
    summary = pd.DataFrame(summary_rows)
    family_theme = registry.groupby(["family", "theme"], as_index=False).agg(candidate_count=("candidate_id", "count"))
    family_theme["notes"] = "panel generation only; no IC scoring"
    manifest.to_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv", index=False)
    summary.to_csv(DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv", index=False)
    source_summary.to_csv(DISCOVERY_SUMMARY_DIR / "source_input_diagnostics.csv", index=False)
    source_summary.to_csv(DIAGNOSTICS_DIR / "source_input_diagnostics.csv", index=False)
    source_summary.to_csv(DIAGNOSTICS_DIR / "source_panel_inputs.csv", index=False)
    family_theme.to_csv(DISCOVERY_SUMMARY_DIR / "family_theme_summary.csv", index=False)
    return manifest, summary, source_summary


def run_panel_generation() -> tuple[pd.DataFrame, pd.DataFrame]:
    registry = candidate_registry()
    validate_rank_coherence_registry(registry)
    _ensure_dirs()
    manifest, summary, _ = _write_candidate_panels(registry)
    metadata_screening = _run_metadata_screening(registry)
    metadata_screening.to_csv(REDUNDANCY_SCREENING_DIR / "metadata_redundancy_screening.csv", index=False)
    metadata_screening.to_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening.csv", index=False)

    try:
        from pipelines.utils.redundancy_screening import (
            StatisticalRedundancyConfig,
            screen_statistical_redundancy_from_cache,
        )
    except Exception:
        import sys

        ROOT = Path(__file__).resolve().parent.parent
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from pipelines.utils.redundancy_screening import (
            StatisticalRedundancyConfig,
            screen_statistical_redundancy_from_cache,
        )

    statistical = screen_statistical_redundancy_from_cache(
        registry,
        comparison_signal_names=registry["signal_name"].sort_values().tolist(),
        config=StatisticalRedundancyConfig(
            panel_dir=CANDIDATE_PANELS_DIR,
            lookback_rows=STATISTICAL_SCREENING_LOOKBACK_ROWS,
        ),
    )
    statistical.to_csv(REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv", index=False)
    for name in (
        "persistence_lineage_redundancy.csv",
        "stress_repair_redundancy.csv",
        "dispersion_reference_redundancy.csv",
        "approved_scoring_subset_recommendation.csv",
    ):
        path = REDUNDANCY_SCREENING_DIR / name
        if not path.exists():
            pd.DataFrame().to_csv(path, index=False)
    _write_research_manifest(registry, panel_generation_executed=True)
    _write_scaffold_summary()
    _write_guardrail_artifacts(panel_generation_executed=True)
    _write_placeholder_ic_manifest()
    return manifest, summary


def _write_placeholder_ic_manifest() -> None:
    for name in (
        "approved_scoring_subset.csv",
        "candidate_horizon_ic_scores.csv",
        "candidate_ic_summary.csv",
        "daily_ic_by_candidate_horizon.csv",
        "family_theme_ic_summary.csv",
        "horizon_ic_summary.csv",
    ):
        path = IC_DISCOVERY_DIR / name
        if not path.exists():
            pd.DataFrame().to_csv(path, index=False)
    (IC_DISCOVERY_DIR / "manifest.json").write_text(
        json.dumps({"ic_scoring_executed": False, "notes": "IC discovery is intentionally not run by panel generation."}, indent=2),
        encoding="utf-8",
    )


def _run_metadata_screening(registry: pd.DataFrame) -> pd.DataFrame:
    try:
        from pipelines.utils.redundancy_screening import screen_registry_df
    except Exception:
        import sys

        ROOT = Path(__file__).resolve().parent.parent
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from pipelines.utils.redundancy_screening import screen_registry_df

    return screen_registry_df(registry)


def dry_run() -> None:
    registry = candidate_registry()
    validate_rank_coherence_registry(registry)
    _ensure_dirs()
    registry.to_csv(CANDIDATE_INVENTORY_DIR / "candidate_registry.csv", index=False)
    _write_schema_check(registry)
    metadata_screening = _run_metadata_screening(registry)
    metadata_screening.to_csv(REDUNDANCY_SCREENING_DIR / "metadata_redundancy_screening.csv", index=False)
    metadata_screening.to_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening.csv", index=False)
    _empty_statistical_redundancy_placeholder().to_csv(
        REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv",
        index=False,
    )
    for name in (
        "persistence_lineage_redundancy.csv",
        "stress_repair_redundancy.csv",
        "dispersion_reference_redundancy.csv",
        "approved_scoring_subset_recommendation.csv",
    ):
        pd.DataFrame().to_csv(REDUNDANCY_SCREENING_DIR / name, index=False)
    _write_placeholder_outputs()
    _write_manifest(registry)
    _write_scaffold_summary()
    _write_guardrail_artifacts()


def list_candidates() -> None:
    registry = candidate_registry()
    print(
        registry[
            [
                "candidate_id",
                "signal_name",
                "family",
                "theme",
                "feature_group",
                "horizon",
                "redundancy_risk",
                "research_status",
                "expected_artifact_path",
            ]
        ].to_string(index=False)
    )


def describe() -> None:
    print("Rank-Coherence Family Discovery Framework Scaffold")
    print(f"run_id: {RUN_ID}")
    print(f"candidate_count: {INITIAL_CANDIDATE_COUNT}")
    print(f"hard_max_candidate_count: {HARD_MAX_CANDIDATES}")
    print(RESEARCH_ONLY_GUARDRAIL)
    print("")
    print("Artifact directories:")
    for path in _artifact_dirs():
        print(f"  - {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Research-only scaffold for rank-coherence family discovery.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--describe", action="store_true", help="Describe the scaffold and guardrails.")
    group.add_argument("--list-candidates", action="store_true", help="List the approved candidate registry.")
    group.add_argument("--dry-run", action="store_true", help="Create scaffold artifacts only; no panels or discovery.")
    group.add_argument("--run", action="store_true", help="Reserved for later panel generation; disabled in scaffold v1.")
    args = parser.parse_args()

    if args.describe:
        describe()
        return 0
    if args.list_candidates:
        list_candidates()
        return 0
    if args.dry_run:
        try:
            dry_run()
        except RegistryValidationError as exc:
            print("Registry validation failed:", str(exc))
            return 2
        print(f"Wrote rank-coherence scaffold artifacts to {OUT_DIR}")
        print("Dry-run guardrail: no panel generation, discovery, IC scoring, refinement, validation, governance mutation, threshold mutation, production registration, ML, promotion, or demotion executed.")
        return 0
    if args.run:
        try:
            manifest, _ = run_panel_generation()
        except RegistryValidationError as exc:
            print("Registry validation failed:", str(exc))
            return 2
        except Exception as exc:
            print("Research-only rank-coherence panel generation failed:", str(exc))
            return 1
        print(f"Wrote {len(manifest)} research-only rank-coherence candidate panels to {CANDIDATE_PANELS_DIR}")
        print("Wrote panel manifest to", DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
        print(
            "Research-only guardrail: no discovery scoring, IC scoring, refinement, validation, "
            "governance mutation, threshold mutation, production registration, ML, promotion, or demotion executed."
        )
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
