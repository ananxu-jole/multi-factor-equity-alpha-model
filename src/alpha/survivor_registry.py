"""Engine entrypoint for 08 Survivor Freeze Pre-ML Alpha Library.

This module keeps the notebook-level survivor-freeze orchestration callable
without changing the underlying selection helpers or storage schemas.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.db import load_table, table_exists
from src.run_config import get_sqlite_db_path, make_run_id, make_run_timestamp
from src.survivor_registry import *  # noqa: F401,F403
from src.survivor_registry import (
    CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS,
    add_alpha_behavior_clusters,
    add_survivor_selection_scores,
    build_constructed_pre_ml_alpha_inputs,
    build_constructed_survivor_lineage_report,
    build_correlation_aware_survivor_registry,
    build_survivor_candidate_pool,
    build_survivor_cluster_summary,
    build_survivor_freeze_report,
    compute_survivor_alpha_correlations,
    validate_correlation_aware_survivor_registry,
)
from src.survivor_storage import save_survivor_outputs


CORE_MAX_ABS_CORRELATION = 0.90
CLUSTER_MAX_ABS_CORRELATION = 0.95
TARGET_MAX_CORE_SURVIVORS = 4
MIN_CLUSTER_SCORE = 40
PRIMARY_PROMOTION_DECISIONS = ["PROMOTE_CORE", "PROMOTE_BALANCED", "REVIEW_SATELLITE"]

REQUIRED_INPUT_TABLES = [
    "alpha_stress_gate_current",
    "alpha_stress_audit_summary_current",
    "alpha_constructed_candidates_current",
    "alpha_construction_metadata_current",
    "alpha_construction_diagnostics_current",
    "constructed_alpha_wfv_gate_current",
    "constructed_alpha_wfv_winner_summary_current",
]


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required input tables are missing from {db_path}: {missing_tables}")


def _load_survivor_freeze_inputs(db_path: Path) -> dict[str, pd.DataFrame]:
    return {
        "alpha_stress_gate": load_table("alpha_stress_gate_current", db_path=db_path),
        "alpha_stress_audit": load_table("alpha_stress_audit_summary_current", db_path=db_path),
        "alpha_constructed_candidates": load_table("alpha_constructed_candidates_current", db_path=db_path),
        "alpha_construction_metadata": load_table("alpha_construction_metadata_current", db_path=db_path),
        "alpha_construction_diagnostics": load_table("alpha_construction_diagnostics_current", db_path=db_path),
        "constructed_alpha_wfv_gate": load_table("constructed_alpha_wfv_gate_current", db_path=db_path),
        "constructed_alpha_wfv_winner_summary": load_table(
            "constructed_alpha_wfv_winner_summary_current",
            db_path=db_path,
        ),
    }


def _build_summary(
    *,
    run_id: str,
    timestamp_frozen: str,
    survivor_version: str,
    primary_candidate_pool: pd.DataFrame,
    survivor_alpha_correlation: pd.DataFrame,
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    pre_ml_core_only_check: bool,
    pre_ml_with_non_core: list[str],
) -> pd.DataFrame:
    pre_ml_alpha_names = (
        sorted(pre_ml_alpha_inputs["alpha_name"].dropna().unique().tolist())
        if not pre_ml_alpha_inputs.empty
        else []
    )
    regime_overlay_name_count = int(
        survivor_registry["alpha_name"]
        .astype(str)
        .str.contains("__|regime_context", case=False, na=False)
        .sum()
    )
    n_behavior_clusters = (
        int(primary_candidate_pool["alpha_behavior_cluster"].nunique())
        if "alpha_behavior_cluster" in primary_candidate_pool.columns
        else 0
    )
    final_core_count = int(
        survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE").sum()
        if "promotion_decision_final" in survivor_registry.columns
        else 0
    )

    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "timestamp_frozen", "value": timestamp_frozen},
            {"metric": "survivor_version", "value": survivor_version},
            {"metric": "core_max_abs_correlation", "value": CORE_MAX_ABS_CORRELATION},
            {"metric": "cluster_max_abs_correlation", "value": CLUSTER_MAX_ABS_CORRELATION},
            {"metric": "target_max_core_survivors", "value": TARGET_MAX_CORE_SURVIVORS},
            {"metric": "min_cluster_score", "value": MIN_CLUSTER_SCORE},
            {"metric": "n_primary_candidates", "value": len(primary_candidate_pool)},
            {"metric": "n_pairwise_correlations", "value": len(survivor_alpha_correlation)},
            {"metric": "n_behavior_clusters", "value": n_behavior_clusters},
            {"metric": "n_final_core_survivors", "value": final_core_count},
            {"metric": "n_registry_rows", "value": len(survivor_registry)},
            {"metric": "pre_ml_alpha_input_rows", "value": len(pre_ml_alpha_inputs)},
            {"metric": "pre_ml_alpha_names", "value": ", ".join(pre_ml_alpha_names)},
            {
                "metric": "pre_ml_only_final_promote_core",
                "value": pre_ml_core_only_check and not pre_ml_with_non_core,
            },
            {"metric": "regime_overlay_alpha_name_count", "value": regime_overlay_name_count},
        ]
    )


def _validate_outputs(
    *,
    stress_gate: pd.DataFrame,
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    final_core_registry: pd.DataFrame,
) -> None:
    if stress_gate.empty:
        raise ValueError("alpha_stress_gate_current is empty.")

    missing_registry_columns = [
        column
        for column in CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS
        if column not in survivor_registry.columns
    ]
    if missing_registry_columns:
        raise ValueError(
            "survivor_registry is missing required columns: "
            f"{missing_registry_columns}"
        )

    final_core_names = set(final_core_registry["alpha_name"].dropna())
    pre_ml_names = set(pre_ml_alpha_inputs["alpha_name"].dropna())
    non_core_names = sorted(pre_ml_names.difference(final_core_names))
    if non_core_names:
        raise ValueError(
            "pre_ml_alpha_inputs contains names outside final PROMOTE_CORE registry: "
            f"{non_core_names}"
        )


def run_08_survivor_freeze(
    db_path=None,
    survivor_version: str = "phase8_cluster_aware_survivor_v5",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 08 survivor-freeze notebook core logic as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    resolved_run_id = run_id or make_run_id(prefix="phase8_cluster_aware_survivor")
    timestamp_frozen = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    inputs = _load_survivor_freeze_inputs(resolved_db_path)
    alpha_stress_gate = inputs["alpha_stress_gate"]
    alpha_stress_audit = inputs["alpha_stress_audit"]
    alpha_constructed_candidates = inputs["alpha_constructed_candidates"]
    alpha_construction_metadata = inputs["alpha_construction_metadata"]
    alpha_construction_diagnostics = inputs["alpha_construction_diagnostics"]
    constructed_alpha_wfv_winner_summary = inputs["constructed_alpha_wfv_winner_summary"]

    if alpha_stress_gate.empty:
        raise ValueError("alpha_stress_gate_current is empty.")

    _log(verbose, f"Loaded 08 survivor-freeze inputs from {resolved_db_path}")
    for artifact_name, artifact in inputs.items():
        _log(verbose, f"  {artifact_name}: {len(artifact):,} rows x {len(artifact.columns):,} columns")

    all_stress_labeled_candidates = build_survivor_candidate_pool(
        stress_gate=alpha_stress_gate,
        stress_audit=alpha_stress_audit,
        construction_metadata=alpha_construction_metadata,
        construction_diagnostics=alpha_construction_diagnostics,
        constructed_alpha_wfv_winner_summary=constructed_alpha_wfv_winner_summary,
    )
    tracked_candidate_mask = (
        all_stress_labeled_candidates["promotion_decision"].isin(PRIMARY_PROMOTION_DECISIONS)
        | all_stress_labeled_candidates["promotion_decision"].eq("REJECT_HIGH_TURNOVER")
        | all_stress_labeled_candidates["turnover_risk_flag"].astype(str).eq("HIGH_TURNOVER_RISK")
    )
    all_stress_labeled_candidates = all_stress_labeled_candidates.loc[tracked_candidate_mask].copy()
    all_stress_labeled_candidates = add_alpha_behavior_clusters(
        add_survivor_selection_scores(all_stress_labeled_candidates)
    )
    primary_candidate_pool = all_stress_labeled_candidates.loc[
        all_stress_labeled_candidates["promotion_decision"].isin(PRIMARY_PROMOTION_DECISIONS)
    ].copy()

    survivor_alpha_correlation = compute_survivor_alpha_correlations(
        alpha_candidates_long=alpha_constructed_candidates,
        candidates=primary_candidate_pool,
        survivor_version=survivor_version,
        run_id=resolved_run_id,
    )
    survivor_registry = build_correlation_aware_survivor_registry(
        candidates=all_stress_labeled_candidates,
        alpha_correlations=survivor_alpha_correlation,
        survivor_version=survivor_version,
        run_id=resolved_run_id,
        timestamp_frozen=timestamp_frozen,
        core_max_abs_correlation=CORE_MAX_ABS_CORRELATION,
        cluster_max_abs_correlation=CLUSTER_MAX_ABS_CORRELATION,
        target_max_core_survivors=TARGET_MAX_CORE_SURVIVORS,
        min_cluster_score=MIN_CLUSTER_SCORE,
    )
    survivor_cluster_summary = build_survivor_cluster_summary(
        survivor_registry=survivor_registry,
        alpha_correlations=survivor_alpha_correlation,
        survivor_version=survivor_version,
        run_id=resolved_run_id,
    )
    final_core_registry = survivor_registry.loc[
        survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE")
    ].copy()
    survivor_validation_report = validate_correlation_aware_survivor_registry(survivor_registry)
    survivor_lineage_report = build_constructed_survivor_lineage_report(
        survivor_registry=survivor_registry,
        construction_metadata=None,
        stress_audit=alpha_stress_audit,
    )
    survivor_freeze_report = build_survivor_freeze_report(final_core_registry)
    pre_ml_alpha_inputs = build_constructed_pre_ml_alpha_inputs(
        alpha_candidates_long=alpha_constructed_candidates,
        survivor_registry=final_core_registry,
    )

    final_core_names = set(final_core_registry["alpha_name"].dropna())
    pre_ml_alpha_names = (
        sorted(pre_ml_alpha_inputs["alpha_name"].dropna().unique().tolist())
        if not pre_ml_alpha_inputs.empty
        else []
    )
    pre_ml_with_non_core = sorted(set(pre_ml_alpha_names).difference(final_core_names))
    pre_ml_core_only_check = set(pre_ml_alpha_names).issubset(final_core_names)

    _validate_outputs(
        stress_gate=alpha_stress_gate,
        survivor_registry=survivor_registry,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        final_core_registry=final_core_registry,
    )

    summary = _build_summary(
        run_id=resolved_run_id,
        timestamp_frozen=timestamp_frozen,
        survivor_version=survivor_version,
        primary_candidate_pool=primary_candidate_pool,
        survivor_alpha_correlation=survivor_alpha_correlation,
        survivor_registry=survivor_registry,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        pre_ml_core_only_check=pre_ml_core_only_check,
        pre_ml_with_non_core=pre_ml_with_non_core,
    )

    saved_paths = None
    if write:
        saved_paths = save_survivor_outputs(
            survivor_registry=survivor_registry,
            pre_ml_alpha_inputs=pre_ml_alpha_inputs,
            survivor_freeze_report=survivor_freeze_report,
            survivor_validation_report=survivor_validation_report,
            survivor_lineage_report=survivor_lineage_report,
            survivor_alpha_correlation=survivor_alpha_correlation,
            survivor_cluster_summary=survivor_cluster_summary,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            survivor_version=survivor_version,
        )

    _log(verbose, "08 survivor-freeze output rows")
    for artifact_name, artifact in [
        ("survivor_registry", survivor_registry),
        ("pre_ml_alpha_inputs", pre_ml_alpha_inputs),
        ("survivor_alpha_correlation", survivor_alpha_correlation),
        ("survivor_cluster_summary", survivor_cluster_summary),
        ("survivor_freeze_report", survivor_freeze_report),
        ("survivor_validation_report", survivor_validation_report),
        ("survivor_lineage_report", survivor_lineage_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "survivor_registry": survivor_registry,
        "pre_ml_alpha_inputs": pre_ml_alpha_inputs,
        "survivor_alpha_correlation": survivor_alpha_correlation,
        "survivor_cluster_summary": survivor_cluster_summary,
        "survivor_freeze_report": survivor_freeze_report,
        "survivor_validation_report": survivor_validation_report,
        "survivor_lineage_report": survivor_lineage_report,
        "summary": summary,
        "all_stress_labeled_candidates": all_stress_labeled_candidates,
        "primary_candidate_pool": primary_candidate_pool,
        "final_core_registry": final_core_registry,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "timestamp_frozen": timestamp_frozen,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
