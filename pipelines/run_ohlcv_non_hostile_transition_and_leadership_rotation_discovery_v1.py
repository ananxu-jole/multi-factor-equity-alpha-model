from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RUN_ID = "ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID

CANDIDATE_INVENTORY_DIR = OUT_DIR / "candidate_inventory"
CANDIDATE_REGISTRY_DIR = OUT_DIR / "candidate_registry"
CANDIDATE_IMPLEMENTATION_DIR = OUT_DIR / "candidate_implementation"
MANIFESTS_DIR = OUT_DIR / "manifests"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"
DISCOVERY_SUMMARY_DIR = OUT_DIR / "discovery_summary"
REDUNDANCY_SCREENING_DIR = OUT_DIR / "redundancy_screening"
IMPLEMENTATION_REVIEW_DIR = OUT_DIR / "implementation_review"
CANDIDATE_PANELS_DIR = OUT_DIR / "candidate_panels"
CANDIDATE_PANEL_GENERATION_DIR = OUT_DIR / "candidate_panel_generation"

RAW_OHLCV_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")

ARTIFACT_DIRS = [
    CANDIDATE_INVENTORY_DIR,
    CANDIDATE_REGISTRY_DIR,
    CANDIDATE_IMPLEMENTATION_DIR,
    MANIFESTS_DIR,
    DIAGNOSTICS_DIR,
    DISCOVERY_SUMMARY_DIR,
    REDUNDANCY_SCREENING_DIR,
    IMPLEMENTATION_REVIEW_DIR,
]

SCAFFOLD_STATUS = "SCAFFOLD_ONLY"
FINAL_CLASSIFICATION = "READY_FOR_DISCOVERY_REVIEW"
REGISTRY_STATUS = "REGISTRY_ONLY"
REGISTRY_FINAL_CLASSIFICATION = "READY_FOR_REGISTRY_REVIEW"
IMPLEMENTATION_STATUS = "CANDIDATE_IMPLEMENTATION_ONLY"
IMPLEMENTATION_FINAL_CLASSIFICATION = "READY_FOR_PANEL_GENERATION_REVIEW"
PANEL_GENERATION_STATUS = "PANEL_GENERATION_ONLY"
PANEL_GENERATION_FINAL_CLASSIFICATION = "PANEL_GENERATION_COMPLETE_READY_FOR_IC_DISCOVERY"

DISCOVERY_CATEGORIES = [
    {
        "category_id": "orderly_leadership_emergence",
        "category_name": "orderly leadership emergence",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Early non-hostile movement from neutral standing toward leadership.",
    },
    {
        "category_id": "healthy_leadership_persistence",
        "category_name": "healthy leadership persistence",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Durable leadership after a healthy transition without post-drawdown dependence.",
    },
    {
        "category_id": "smooth_trend_handoff",
        "category_name": "smooth trend handoff",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Controlled transition from consolidation or neutral trend into leadership.",
    },
    {
        "category_id": "gradual_participation_expansion",
        "category_name": "gradual participation expansion",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Orderly demand formation without panic rebound or stress-repair gating.",
    },
    {
        "category_id": "rotation_acceleration",
        "category_name": "rotation acceleration",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Increasing pace of leadership migration before broad momentum dominates.",
    },
    {
        "category_id": "rotation_deceleration",
        "category_name": "rotation deceleration",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Late-stage or slowing leadership migration and handoff quality.",
    },
    {
        "category_id": "volume_confirmed_leadership_shifts",
        "category_name": "volume-confirmed leadership shifts",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Leadership improvement supported by participation or volume quality.",
    },
    {
        "category_id": "healthy_breadth_transitions",
        "category_name": "healthy breadth transitions",
        "scaffold_status": SCAFFOLD_STATUS,
        "description": "Non-hostile broadening behavior without weak-breadth repair framing.",
    },
]

DELIVERABLES = [
    {
        "deliverable": "runner_scaffold",
        "path": "pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py",
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Fail-closed runner modes for scaffold creation and validation.",
    },
    {
        "deliverable": "candidate_inventory_manifest",
        "path": str(CANDIDATE_INVENTORY_DIR / "candidate_inventory_manifest.csv"),
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Placeholder inventory manifest; no candidates are generated.",
    },
    {
        "deliverable": "candidate_registry_artifacts",
        "path": str(CANDIDATE_REGISTRY_DIR),
        "scaffold_status": REGISTRY_STATUS,
        "purpose": "Authoritative metadata registry for approved concepts; no formulas or panels.",
    },
    {
        "deliverable": "candidate_implementation_artifacts",
        "path": str(CANDIDATE_IMPLEMENTATION_DIR),
        "scaffold_status": IMPLEMENTATION_STATUS,
        "purpose": "Registry-derived candidate implementation manifests and diagnostics; no panels or empirical results.",
    },
    {
        "deliverable": "artifact_manifest",
        "path": str(MANIFESTS_DIR / "artifact_manifest.csv"),
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Expected scaffold artifacts and placeholder status.",
    },
    {
        "deliverable": "diagnostics_placeholders",
        "path": str(DIAGNOSTICS_DIR),
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Scaffold-only diagnostics with no research results.",
    },
    {
        "deliverable": "discovery_readiness_report",
        "path": str(DISCOVERY_SUMMARY_DIR / "discovery_readiness_report.md"),
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Readiness placeholder confirming discovery remains blocked.",
    },
    {
        "deliverable": "implementation_review_note",
        "path": "docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold_implementation_v1.md",
        "scaffold_status": SCAFFOLD_STATUS,
        "purpose": "Review note for scaffold implementation and verification.",
    },
]

FORBIDDEN_ACTIONS = [
    "discovery_executed",
    "candidate_generation_executed",
    "candidate_panels_generated",
    "ic_calculated",
    "redundancy_screening_run",
    "refinement_executed",
    "validation_executed",
    "governance_modified",
    "thresholds_modified",
    "production_registered",
    "ml_implemented",
]

CANDIDATE_REGISTRY_FIELDS = [
    "candidate_id",
    "working_name",
    "family",
    "concept_category",
    "economic_mechanism",
    "implementation_priority",
    "dependency_class",
    "required_input_family",
    "required_ohlcv_inputs",
    "prohibited_dependencies",
    "artifact_namespace",
    "diagnostic_identifier",
    "research_status",
    "implementation_status",
    "formula_status",
    "panel_status",
    "discovery_status",
    "refinement_status",
    "validation_status",
    "candidate_state",
    "reviewer_notes",
]

APPROVED_CANDIDATE_IDS = [
    "nhlr_01",
    "nhlr_02",
    "nhlr_03",
    "nhlr_04",
    "nhlr_05",
    "nhlr_07",
    "nhlr_08",
    "nhlr_09",
    "nhlr_10",
]

ALLOWED_REGISTRY_VALUES = {
    "dependency_class": {"OHLCV_ONLY"},
    "required_input_family": {"OHLCV_DERIVED_ONLY"},
    "research_status": {"RESEARCH_ONLY"},
    "implementation_status": {"REGISTRY_ONLY_NOT_IMPLEMENTED"},
    "formula_status": {"NO_FORMULA_DEFINED"},
    "panel_status": {"NO_PANEL_GENERATED"},
    "discovery_status": {"DISCOVERY_NOT_EXECUTED"},
    "refinement_status": {"REFINEMENT_NOT_EXECUTED"},
    "validation_status": {"VALIDATION_NOT_EXECUTED"},
    "candidate_state": {"REGISTRY_ONLY_NO_RESEARCH_OUTCOME"},
}

CANDIDATE_REGISTRY_RECORDS = [
    {
        "candidate_id": "nhlr_01",
        "working_name": "Emerging Leadership From Neutral Base",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "orderly leadership emergence",
        "economic_mechanism": "gradual leadership emergence",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, rank, trend, breadth-like OHLCV aggregates",
        "prohibited_dependencies": "PIT metadata, sector labels, peer groups, stress-repair gates, raw momentum-only framing",
        "diagnostic_identifier": "nhlr_01_neutral_emergence_diagnostic",
        "reviewer_notes": "Core early-stage non-hostile leadership-emergence concept; guard against raw momentum drift.",
    },
    {
        "candidate_id": "nhlr_02",
        "working_name": "Quiet Accumulation Before Leadership",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "orderly leadership emergence",
        "economic_mechanism": "orderly capital migration",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, volume, range, participation-like OHLCV proxies",
        "prohibited_dependencies": "PIT metadata, liquidity repair, volume shock reversal, stress recovery",
        "diagnostic_identifier": "nhlr_02_quiet_accumulation_diagnostic",
        "reviewer_notes": "Capital-migration concept; must not become participation repair or shock reversal.",
    },
    {
        "candidate_id": "nhlr_03",
        "working_name": "Post-Transition Leadership Durability",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "healthy leadership persistence",
        "economic_mechanism": "participation persistence / leadership confirmation",
        "implementation_priority": "Medium-high",
        "required_ohlcv_inputs": "price, return, rank, trend, participation-like OHLCV proxies",
        "prohibited_dependencies": "drawdown windows, post-drawdown persistence, rank-churn-only logic",
        "diagnostic_identifier": "nhlr_03_leadership_durability_diagnostic",
        "reviewer_notes": "Durability concept; guard against persistence and rank-coherence duplication.",
    },
    {
        "candidate_id": "nhlr_04",
        "working_name": "Smooth Trend Handoff",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "smooth trend handoff",
        "economic_mechanism": "trend handoff",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, trend, range, volatility-like OHLCV proxies",
        "prohibited_dependencies": "trend-following-only logic, stress absorption, volatility compression after stress",
        "diagnostic_identifier": "nhlr_04_trend_handoff_diagnostic",
        "reviewer_notes": "Transition-quality concept; must remain distinct from simple trend following.",
    },
    {
        "candidate_id": "nhlr_05",
        "working_name": "Broadening Participation Without Stress",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "gradual participation expansion",
        "economic_mechanism": "healthy participation expansion",
        "implementation_priority": "Medium-high",
        "required_ohlcv_inputs": "volume, participation-like OHLCV proxies, breadth-like OHLCV aggregates",
        "prohibited_dependencies": "weak-breadth repair, hostile trend, participation repair gates",
        "diagnostic_identifier": "nhlr_05_participation_expansion_diagnostic",
        "reviewer_notes": "Healthy broadening concept; explicit stress-repair drift controls required.",
    },
    {
        "candidate_id": "nhlr_07",
        "working_name": "Rotation Acceleration Leader",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "rotation acceleration",
        "economic_mechanism": "rotation acceleration",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, rank, trend, breadth-like OHLCV aggregates",
        "prohibited_dependencies": "momentum-only acceleration, transition-state stress absorption",
        "diagnostic_identifier": "nhlr_07_rotation_acceleration_diagnostic",
        "reviewer_notes": "Rotation-pace concept; must not collapse into momentum acceleration.",
    },
    {
        "candidate_id": "nhlr_08",
        "working_name": "Mature Leadership Deceleration Avoidance",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "rotation deceleration",
        "economic_mechanism": "rotation deceleration",
        "implementation_priority": "Medium",
        "required_ohlcv_inputs": "price, return, rank, trend, range, participation-like OHLCV proxies",
        "prohibited_dependencies": "short reversal, post-drawdown persistence, rank-coherence duplicate",
        "diagnostic_identifier": "nhlr_08_rotation_deceleration_diagnostic",
        "reviewer_notes": "Lower-priority rotation-phase quality concept; monitor persistence and reversal overlap.",
    },
    {
        "candidate_id": "nhlr_09",
        "working_name": "Volume-Confirmed Leadership Shift",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "volume-confirmed leadership shifts",
        "economic_mechanism": "leadership confirmation",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, volume, participation-like OHLCV proxies",
        "prohibited_dependencies": "volume shock reversal, liquidity repair, volume momentum-only logic",
        "diagnostic_identifier": "nhlr_09_volume_confirmation_diagnostic",
        "reviewer_notes": "Confirmation concept; volume must not become shock reversal or liquidity repair.",
    },
    {
        "candidate_id": "nhlr_10",
        "working_name": "Healthy Breadth Contributor",
        "family": "ohlcv_non_hostile_transition_leadership_rotation",
        "concept_category": "healthy breadth transitions",
        "economic_mechanism": "healthy participation expansion / breadth transition",
        "implementation_priority": "High",
        "required_ohlcv_inputs": "price, return, breadth-like OHLCV aggregates, participation-like OHLCV proxies",
        "prohibited_dependencies": "weak-breadth repair, sector rotation claims, PIT metadata",
        "diagnostic_identifier": "nhlr_10_breadth_contribution_diagnostic",
        "reviewer_notes": "Healthy breadth concept; must not become sector, peer, or weak-breadth repair logic.",
    },
]


def _write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def artifact_paths() -> list[Path]:
    return [
        CANDIDATE_INVENTORY_DIR / "discovery_categories.csv",
        CANDIDATE_INVENTORY_DIR / "candidate_inventory_manifest.csv",
        MANIFESTS_DIR / "scaffold_manifest.json",
        MANIFESTS_DIR / "artifact_manifest.csv",
        DIAGNOSTICS_DIR / "scaffold_diagnostics.csv",
        DIAGNOSTICS_DIR / "guardrail_diagnostics.csv",
        DIAGNOSTICS_DIR / "prohibited_action_diagnostics.csv",
        DISCOVERY_SUMMARY_DIR / "discovery_readiness_report.md",
        DISCOVERY_SUMMARY_DIR / "discovery_summary_placeholder.json",
        REDUNDANCY_SCREENING_DIR / "redundancy_screening_placeholder.csv",
        IMPLEMENTATION_REVIEW_DIR / "implementation_review_placeholder.md",
    ]


def candidate_registry_paths() -> list[Path]:
    return [
        CANDIDATE_REGISTRY_DIR / "candidate_registry.csv",
        CANDIDATE_REGISTRY_DIR / "candidate_registry_schema.json",
        CANDIDATE_REGISTRY_DIR / "candidate_registry_manifest.json",
        CANDIDATE_REGISTRY_DIR / "candidate_status_report.csv",
        CANDIDATE_REGISTRY_DIR / "candidate_dependency_report.csv",
        CANDIDATE_REGISTRY_DIR / "registry_validation_report.csv",
    ]


def candidate_registry_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for record in CANDIDATE_REGISTRY_RECORDS:
        row = dict(record)
        candidate_id = str(row["candidate_id"])
        row.update(
            {
                "dependency_class": "OHLCV_ONLY",
                "required_input_family": "OHLCV_DERIVED_ONLY",
                "artifact_namespace": str(CANDIDATE_REGISTRY_DIR / candidate_id),
                "research_status": "RESEARCH_ONLY",
                "implementation_status": "REGISTRY_ONLY_NOT_IMPLEMENTED",
                "formula_status": "NO_FORMULA_DEFINED",
                "panel_status": "NO_PANEL_GENERATED",
                "discovery_status": "DISCOVERY_NOT_EXECUTED",
                "refinement_status": "REFINEMENT_NOT_EXECUTED",
                "validation_status": "VALIDATION_NOT_EXECUTED",
                "candidate_state": "REGISTRY_ONLY_NO_RESEARCH_OUTCOME",
            }
        )
        rows.append(row)
    return rows


def candidate_registry_schema() -> dict[str, object]:
    return {
        "schema_name": "ohlcv_non_hostile_transition_leadership_rotation_candidate_registry_v1",
        "registry_status": REGISTRY_STATUS,
        "required_fields": CANDIDATE_REGISTRY_FIELDS,
        "approved_candidate_ids": APPROVED_CANDIDATE_IDS,
        "allowed_values": {key: sorted(values) for key, values in ALLOWED_REGISTRY_VALUES.items()},
        "field_groups": {
            "identity": ["candidate_id", "working_name", "concept_category", "economic_mechanism"],
            "research_metadata": [
                "implementation_priority",
                "dependency_class",
                "required_input_family",
                "required_ohlcv_inputs",
                "prohibited_dependencies",
                "artifact_namespace",
                "diagnostic_identifier",
            ],
            "lifecycle_status": [
                "implementation_status",
                "formula_status",
                "panel_status",
                "discovery_status",
                "refinement_status",
                "validation_status",
            ],
            "research_outcome": ["candidate_state", "reviewer_notes"],
        },
        "guardrail": "Metadata only. No formulas, panels, discovery, IC, refinement, validation, governance, production, or ML.",
    }


def validate_candidate_registry_rows(
    rows: list[dict[str, object]],
) -> tuple[bool, list[str], list[dict[str, object]]]:
    errors: list[str] = []
    report: list[dict[str, object]] = []

    def add_check(check_name: str, passed: bool, notes: str) -> None:
        report.append(
            {
                "check_name": check_name,
                "status": "PASS" if passed else "FAIL",
                "registry_status": REGISTRY_STATUS,
                "notes": notes,
            }
        )
        if not passed:
            errors.append(f"{check_name}: {notes}")

    row_count_ok = len(rows) == len(APPROVED_CANDIDATE_IDS)
    add_check(
        "registry_completeness",
        row_count_ok,
        f"expected {len(APPROVED_CANDIDATE_IDS)} approved candidates, found {len(rows)}",
    )

    ids = [str(row.get("candidate_id", "")).strip() for row in rows]
    duplicate_ids = sorted({candidate_id for candidate_id in ids if ids.count(candidate_id) > 1})
    add_check(
        "unique_candidate_ids",
        not duplicate_ids,
        "no duplicate candidate IDs" if not duplicate_ids else f"duplicate candidate IDs: {', '.join(duplicate_ids)}",
    )

    expected_ids_ok = set(ids) == set(APPROVED_CANDIDATE_IDS)
    missing_ids = sorted(set(APPROVED_CANDIDATE_IDS) - set(ids))
    unexpected_ids = sorted(set(ids) - set(APPROVED_CANDIDATE_IDS))
    id_notes = "approved candidate ID set matches frozen inventory"
    if missing_ids or unexpected_ids:
        id_notes = f"missing: {missing_ids}; unexpected: {unexpected_ids}"
    add_check("approved_candidate_ids", expected_ids_ok, id_notes)

    required_metadata_ok = True
    metadata_errors: list[str] = []
    for row in rows:
        candidate_id = str(row.get("candidate_id", "<missing>"))
        for field in CANDIDATE_REGISTRY_FIELDS:
            if field not in row or str(row.get(field, "")).strip() == "":
                required_metadata_ok = False
                metadata_errors.append(f"{candidate_id}.{field}")
    add_check(
        "required_metadata_present",
        required_metadata_ok,
        "all required registry fields are populated"
        if required_metadata_ok
        else f"missing required metadata: {', '.join(metadata_errors)}",
    )

    diagnostic_ids = [str(row.get("diagnostic_identifier", "")).strip() for row in rows]
    duplicate_diagnostics = sorted(
        {diagnostic_id for diagnostic_id in diagnostic_ids if diagnostic_ids.count(diagnostic_id) > 1}
    )
    add_check(
        "unique_diagnostic_identifiers",
        not duplicate_diagnostics,
        "diagnostic identifiers are unique"
        if not duplicate_diagnostics
        else f"duplicate diagnostic identifiers: {', '.join(duplicate_diagnostics)}",
    )

    lifecycle_ok = True
    lifecycle_errors: list[str] = []
    for row in rows:
        candidate_id = str(row.get("candidate_id", "<missing>"))
        for field, allowed_values in ALLOWED_REGISTRY_VALUES.items():
            value = str(row.get(field, "")).strip()
            if value not in allowed_values:
                lifecycle_ok = False
                lifecycle_errors.append(f"{candidate_id}.{field}={value}")
    add_check(
        "lifecycle_status_consistency",
        lifecycle_ok,
        "all lifecycle and dependency statuses remain fail-closed"
        if lifecycle_ok
        else f"unexpected status values: {', '.join(lifecycle_errors)}",
    )

    outcome_ok = all(
        str(row.get("candidate_state", "")).strip() == "REGISTRY_ONLY_NO_RESEARCH_OUTCOME" for row in rows
    )
    add_check(
        "research_outcome_consistency",
        outcome_ok,
        "no registry row indicates research execution"
        if outcome_ok
        else "one or more rows indicate a non-placeholder research outcome",
    )

    no_removed_candidate = "nhlr_06" not in ids
    add_check(
        "removed_candidate_excluded",
        no_removed_candidate,
        "nhlr_06 remains excluded from the approved registry",
    )

    return not errors, errors, report


def write_candidate_registry() -> None:
    CANDIDATE_REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    rows = candidate_registry_rows()
    ok, errors, validation_report = validate_candidate_registry_rows(rows)
    if not ok:
        raise ValueError("candidate registry metadata failed validation: " + "; ".join(errors))

    _write_csv(CANDIDATE_REGISTRY_DIR / "candidate_registry.csv", rows, CANDIDATE_REGISTRY_FIELDS)
    _write_json(CANDIDATE_REGISTRY_DIR / "candidate_registry_schema.json", candidate_registry_schema())

    manifest = {
        "run_id": RUN_ID,
        "registry_status": REGISTRY_STATUS,
        "final_classification": REGISTRY_FINAL_CLASSIFICATION,
        "artifact_root": str(CANDIDATE_REGISTRY_DIR),
        "candidate_count": len(rows),
        "approved_candidate_ids": APPROVED_CANDIDATE_IDS,
        "candidate_formulas_defined": False,
        "candidate_code_implemented": False,
        "candidate_panels_generated": False,
        "discovery_executed": False,
        "ic_calculated": False,
        "redundancy_screening_run": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "production_registered": False,
        "ml_implemented": False,
    }
    _write_json(CANDIDATE_REGISTRY_DIR / "candidate_registry_manifest.json", manifest)

    status_rows = [
        {
            "candidate_id": row["candidate_id"],
            "implementation_status": row["implementation_status"],
            "formula_status": row["formula_status"],
            "panel_status": row["panel_status"],
            "discovery_status": row["discovery_status"],
            "refinement_status": row["refinement_status"],
            "validation_status": row["validation_status"],
            "candidate_state": row["candidate_state"],
        }
        for row in rows
    ]
    _write_csv(
        CANDIDATE_REGISTRY_DIR / "candidate_status_report.csv",
        status_rows,
        [
            "candidate_id",
            "implementation_status",
            "formula_status",
            "panel_status",
            "discovery_status",
            "refinement_status",
            "validation_status",
            "candidate_state",
        ],
    )

    dependency_rows = [
        {
            "candidate_id": row["candidate_id"],
            "dependency_class": row["dependency_class"],
            "required_input_family": row["required_input_family"],
            "required_ohlcv_inputs": row["required_ohlcv_inputs"],
            "prohibited_dependencies": row["prohibited_dependencies"],
        }
        for row in rows
    ]
    _write_csv(
        CANDIDATE_REGISTRY_DIR / "candidate_dependency_report.csv",
        dependency_rows,
        [
            "candidate_id",
            "dependency_class",
            "required_input_family",
            "required_ohlcv_inputs",
            "prohibited_dependencies",
        ],
    )
    _write_csv(
        CANDIDATE_REGISTRY_DIR / "registry_validation_report.csv",
        validation_report,
        ["check_name", "status", "registry_status", "notes"],
    )


def validate_candidate_registry() -> tuple[bool, list[str]]:
    registry_path = CANDIDATE_REGISTRY_DIR / "candidate_registry.csv"
    rows: list[dict[str, object]]
    if registry_path.exists():
        rows = _read_csv(registry_path)
    else:
        rows = candidate_registry_rows()

    errors: list[str] = []
    for path in candidate_registry_paths():
        if registry_path.exists() and not path.exists():
            errors.append(f"missing registry artifact: {path}")

    ok, row_errors, _report = validate_candidate_registry_rows(rows)
    errors.extend(row_errors)

    manifest_path = CANDIDATE_REGISTRY_DIR / "candidate_registry_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        fail_closed_fields = [
            "candidate_formulas_defined",
            "candidate_code_implemented",
            "candidate_panels_generated",
            "discovery_executed",
            "ic_calculated",
            "redundancy_screening_run",
            "refinement_executed",
            "validation_executed",
            "governance_modified",
            "thresholds_modified",
            "production_registered",
            "ml_implemented",
        ]
        for field in fail_closed_fields:
            if manifest.get(field) is not False:
                errors.append(f"registry manifest field is not fail-closed: {field}")
        if manifest.get("registry_status") != REGISTRY_STATUS:
            errors.append("registry manifest status is not REGISTRY_ONLY")

    return ok and not errors, errors


def candidate_implementation_paths() -> list[Path]:
    return [
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.csv",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.json",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_diagnostics.csv",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_summary.json",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_registration_map.csv",
    ]


def write_candidate_implementations() -> None:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        IMPLEMENTATION_FINAL_CLASSIFICATION as CANDIDATE_IMPLEMENTATION_FINAL_CLASSIFICATION,
        IMPLEMENTATION_STATUS as CANDIDATE_ROW_IMPLEMENTATION_STATUS,
        implementation_rows,
        validate_candidate_implementations,
    )

    CANDIDATE_IMPLEMENTATION_DIR.mkdir(parents=True, exist_ok=True)
    rows = implementation_rows()
    ok, errors, diagnostics = validate_candidate_implementations(rows)
    if not ok:
        raise ValueError("candidate implementation metadata failed validation: " + "; ".join(errors))

    manifest_fields = list(rows[0].keys()) if rows else []
    _write_csv(CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.csv", rows, manifest_fields)
    _write_csv(
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_diagnostics.csv",
        diagnostics,
        ["check_name", "status", "implementation_status", "notes"],
    )
    _write_csv(
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_registration_map.csv",
        [
            {
                "candidate_id": row["candidate_id"],
                "registry_artifact_namespace": row["registry_artifact_namespace"],
                "implementation_status": row["implementation_status"],
                "source_registry_status": REGISTRY_STATUS,
                "source_registry_path": str(CANDIDATE_REGISTRY_DIR / "candidate_registry.csv"),
            }
            for row in rows
        ],
        [
            "candidate_id",
            "registry_artifact_namespace",
            "implementation_status",
            "source_registry_status",
            "source_registry_path",
        ],
    )

    manifest = {
        "run_id": RUN_ID,
        "implementation_status": IMPLEMENTATION_STATUS,
        "candidate_row_implementation_status": CANDIDATE_ROW_IMPLEMENTATION_STATUS,
        "final_classification": CANDIDATE_IMPLEMENTATION_FINAL_CLASSIFICATION,
        "artifact_root": str(CANDIDATE_IMPLEMENTATION_DIR),
        "source_registry_status": REGISTRY_STATUS,
        "source_registry_path": str(CANDIDATE_REGISTRY_DIR / "candidate_registry.csv"),
        "implemented_candidate_count": len(rows),
        "implemented_candidate_ids": [row["candidate_id"] for row in rows],
        "excluded_candidate_ids": ["nhlr_06"],
        "candidate_panels_generated": False,
        "discovery_executed": False,
        "ic_calculated": False,
        "redundancy_screening_run": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "production_registered": False,
        "ml_implemented": False,
    }
    _write_json(CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.json", manifest)
    _write_json(
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_summary.json",
        {
            "implemented_candidate_count": len(rows),
            "registry_alignment": True,
            "implementation_completeness": True,
            "missing_implementations": [],
            "duplicate_implementations": [],
            "excluded_candidate_implemented": False,
            "final_classification": CANDIDATE_IMPLEMENTATION_FINAL_CLASSIFICATION,
        },
    )


def validate_candidate_implementation_artifacts() -> tuple[bool, list[str]]:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        IMPLEMENTATION_FINAL_CLASSIFICATION as CANDIDATE_IMPLEMENTATION_FINAL_CLASSIFICATION,
        implementation_rows,
        validate_candidate_implementations,
    )

    errors: list[str] = []
    manifest_path = CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.csv"
    if manifest_path.exists():
        rows: list[dict[str, object]] = _read_csv(manifest_path)
    else:
        rows = implementation_rows()

    for path in candidate_implementation_paths():
        if manifest_path.exists() and not path.exists():
            errors.append(f"missing implementation artifact: {path}")

    ok, implementation_errors, _diagnostics = validate_candidate_implementations(rows)
    errors.extend(implementation_errors)

    summary_path = CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_summary.json"
    if summary_path.exists():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("final_classification") != CANDIDATE_IMPLEMENTATION_FINAL_CLASSIFICATION:
            errors.append("implementation summary final classification is not ready for panel generation review")
        if summary.get("excluded_candidate_implemented") is not False:
            errors.append("implementation summary indicates excluded candidate implementation")

    json_manifest_path = CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.json"
    if json_manifest_path.exists():
        manifest = json.loads(json_manifest_path.read_text(encoding="utf-8"))
        fail_closed_fields = [
            "candidate_panels_generated",
            "discovery_executed",
            "ic_calculated",
            "redundancy_screening_run",
            "refinement_executed",
            "validation_executed",
            "governance_modified",
            "thresholds_modified",
            "production_registered",
            "ml_implemented",
        ]
        for field in fail_closed_fields:
            if manifest.get(field) is not False:
                errors.append(f"implementation manifest field is not fail-closed: {field}")

    return ok and not errors, errors


def _normalize_ohlcv_source(raw: pd.DataFrame) -> pd.DataFrame:
    required_long_columns = {"date", "ticker", "open", "high", "low", "close", "volume"}
    if required_long_columns.issubset(raw.columns):
        return raw[["date", "ticker", "open", "high", "low", "close", "volume"]].copy()

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError("OHLCV source must be long-form or a two-level wide OHLCV parquet")

    field_lookup = {
        str(field).strip().lower().replace(" ", "_"): field
        for field in raw.columns.get_level_values(0).unique()
    }
    required_fields = ["open", "high", "low", "close", "volume"]
    missing_fields = [field for field in required_fields if field not in field_lookup]
    if missing_fields:
        raise ValueError("wide OHLCV source is missing fields: " + ", ".join(missing_fields))

    stacked_fields = []
    for field in required_fields:
        series = raw[field_lookup[field]].stack(dropna=False).rename(field)
        stacked_fields.append(series)
    out = pd.concat(stacked_fields, axis=1).reset_index()
    out = out.rename(columns={out.columns[0]: "date", out.columns[1]: "ticker"})
    return out[["date", "ticker", "open", "high", "low", "close", "volume"]]


def load_ohlcv_source_for_panel_generation(source_path: Path = RAW_OHLCV_PATH) -> pd.DataFrame:
    if not source_path.exists():
        raise FileNotFoundError(f"missing OHLCV source parquet: {source_path}")
    return _normalize_ohlcv_source(pd.read_parquet(source_path))


def candidate_panel_generation_paths() -> list[Path]:
    return [
        CANDIDATE_PANEL_GENERATION_DIR / "panel_manifest.csv",
        CANDIDATE_PANEL_GENERATION_DIR / "candidate_panel_generation_summary.csv",
        CANDIDATE_PANEL_GENERATION_DIR / "panel_generation_manifest.json",
        CANDIDATE_PANEL_GENERATION_DIR / "panel_schema_validation_report.csv",
    ]


def validate_candidate_panel_frame(panel: pd.DataFrame, candidate_id: str) -> list[str]:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        FORMULA_VERSION,
        REQUIRED_PANEL_COLUMNS,
        WARMUP_WINDOW,
        formula_manifest_rows,
        validate_formula_manifest_rows,
    )

    errors: list[str] = []
    formula_ok, formula_errors = validate_formula_manifest_rows()
    if not formula_ok:
        errors.extend(formula_errors)
    if candidate_id not in APPROVED_CANDIDATE_IDS:
        errors.append(f"panel candidate_id is not approved: {candidate_id}")
    if candidate_id == "nhlr_06":
        errors.append("excluded candidate nhlr_06 has a panel")
    if list(panel.columns) != REQUIRED_PANEL_COLUMNS:
        errors.append("panel schema does not match required panel columns")
    if panel.empty:
        errors.append(f"panel is empty: {candidate_id}")
        return errors

    ids = set(panel["candidate_id"].astype(str))
    if ids != {candidate_id}:
        errors.append(f"panel candidate_id values do not match file candidate_id: {sorted(ids)}")
    if panel[["date", "ticker", "candidate_id"]].duplicated().any():
        errors.append(f"duplicate panel rows found for {candidate_id}")
    if not panel["warmup_complete"].astype(bool).all():
        errors.append(f"warmup-incomplete rows were not trimmed for {candidate_id}")
    if "nhlr_06" in ids:
        errors.append("excluded candidate nhlr_06 is present in panel rows")

    manifest_by_id = {str(row["candidate_id"]): row for row in formula_manifest_rows()}
    manifest_row = manifest_by_id.get(candidate_id)
    if manifest_row is not None:
        if set(panel["horizon"].astype(str)) != {str(manifest_row["primary_horizon"])}:
            errors.append(f"horizon mismatch for {candidate_id}")
        if set(panel["formula_name"].astype(str)) != {str(manifest_row["formula_name"])}:
            errors.append(f"formula_name mismatch for {candidate_id}")
    if set(panel["formula_version"].astype(str)) != {FORMULA_VERSION}:
        errors.append(f"formula_version mismatch for {candidate_id}")
    if set(panel["dependency_class"].astype(str)) != {"OHLCV_ONLY"}:
        errors.append(f"dependency_class mismatch for {candidate_id}")
    if set(panel["required_input_family"].astype(str)) != {"OHLCV_DERIVED_ONLY"}:
        errors.append(f"required_input_family mismatch for {candidate_id}")
    if panel["date"].isna().any() or panel["ticker"].isna().any():
        errors.append(f"date or ticker contains null values for {candidate_id}")
    if int(panel["warmup_complete"].astype(bool).sum()) != len(panel):
        errors.append(f"warmup trimming failed for {candidate_id}; warmup_window={WARMUP_WINDOW}")
    return errors


def _panel_metadata(candidate_id: str, panel: pd.DataFrame, source_path: Path, warmup_excluded_rows: int) -> dict[str, object]:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        WARMUP_WINDOW,
    )

    return {
        "run_id": RUN_ID,
        "candidate_id": candidate_id,
        "panel_generation_status": PANEL_GENERATION_STATUS,
        "final_classification": PANEL_GENERATION_FINAL_CLASSIFICATION,
        "row_count": int(len(panel)),
        "non_null_signal_count": int(panel["signal_value"].notna().sum()),
        "null_signal_count": int(panel["signal_value"].isna().sum()),
        "start_date": str(pd.to_datetime(panel["date"]).min().date()),
        "end_date": str(pd.to_datetime(panel["date"]).max().date()),
        "horizon": str(panel["horizon"].iloc[0]),
        "formula_name": str(panel["formula_name"].iloc[0]),
        "formula_version": str(panel["formula_version"].iloc[0]),
        "family": str(panel["family"].iloc[0]),
        "theme": str(panel["theme"].iloc[0]),
        "working_name": str(panel["working_name"].iloc[0]),
        "panel_role": str(panel["panel_role"].iloc[0]),
        "source_ohlcv_path": str(source_path),
        "warmup_window": WARMUP_WINDOW,
        "warmup_rows_excluded": int(warmup_excluded_rows),
        "warmup_trimmed": True,
        "schema_status": "PASS",
        "registry_status": "PASS",
        "candidate_panels_generated": True,
        "discovery_executed": False,
        "ic_calculated": False,
        "redundancy_screening_run": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "production_registered": False,
        "ml_implemented": False,
    }


def write_candidate_panels(source_path: Path = RAW_OHLCV_PATH) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        REQUIRED_PANEL_COLUMNS,
        build_candidate_formula_outputs,
        formula_manifest_rows,
        validate_formula_manifest_rows,
    )

    formula_ok, formula_errors = validate_formula_manifest_rows()
    if not formula_ok:
        raise ValueError("formula manifest failed validation: " + "; ".join(formula_errors))

    raw_ohlcv = load_ohlcv_source_for_panel_generation(source_path)
    outputs = build_candidate_formula_outputs(raw_ohlcv)
    if list(outputs.columns) != REQUIRED_PANEL_COLUMNS:
        raise ValueError("formula output schema does not match required panel schema")

    output_ids = list(outputs["candidate_id"].drop_duplicates().astype(str))
    if output_ids != APPROVED_CANDIDATE_IDS:
        raise ValueError("formula output candidate IDs do not match authoritative registry order")
    if "nhlr_06" in set(output_ids):
        raise ValueError("excluded candidate nhlr_06 appeared in formula outputs")
    if outputs[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError("duplicate in-memory formula output rows detected")

    CANDIDATE_PANELS_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATE_PANEL_GENERATION_DIR.mkdir(parents=True, exist_ok=True)

    manifest_by_id = {str(row["candidate_id"]): row for row in formula_manifest_rows()}
    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    validation_rows: list[dict[str, object]] = []

    for candidate_id in APPROVED_CANDIDATE_IDS:
        candidate_output = outputs[outputs["candidate_id"].eq(candidate_id)].copy()
        panel = candidate_output[candidate_output["warmup_complete"].astype(bool)].copy()
        panel = panel.sort_values(["date", "ticker"]).reset_index(drop=True)
        validation_errors = validate_candidate_panel_frame(panel, candidate_id)
        if validation_errors:
            raise ValueError(f"candidate panel validation failed for {candidate_id}: " + "; ".join(validation_errors))

        panel_path = CANDIDATE_PANELS_DIR / f"{candidate_id}.parquet"
        metadata_path = CANDIDATE_PANELS_DIR / f"{candidate_id}.metadata.json"
        panel.to_parquet(panel_path, index=False)
        warmup_excluded_rows = int(len(candidate_output) - len(panel))
        metadata = _panel_metadata(candidate_id, panel, source_path, warmup_excluded_rows)
        _write_json(metadata_path, metadata)

        manifest_row = manifest_by_id[candidate_id]
        manifest_rows.append(
            {
                "candidate_id": candidate_id,
                "panel_path": str(panel_path),
                "metadata_path": str(metadata_path),
                "row_count": int(len(panel)),
                "non_null_signal_count": int(panel["signal_value"].notna().sum()),
                "null_signal_count": int(panel["signal_value"].isna().sum()),
                "start_date": metadata["start_date"],
                "end_date": metadata["end_date"],
                "horizon": manifest_row["primary_horizon"],
                "formula_name": manifest_row["formula_name"],
                "formula_version": manifest_row["formula_version"],
                "warmup_window": metadata["warmup_window"],
                "warmup_rows_excluded": warmup_excluded_rows,
                "warmup_trimmed": True,
                "schema_status": "PASS",
                "registry_status": "PASS",
                "generation_status": "generated",
            }
        )
        summary_rows.append(
            {
                "candidate_id": candidate_id,
                "working_name": manifest_row["working_name"],
                "family": manifest_row["family"],
                "theme": manifest_row["concept_category"],
                "horizon": manifest_row["primary_horizon"],
                "panel_role": manifest_row["panel_role"],
                "row_count": int(len(panel)),
                "non_null_signal_count": int(panel["signal_value"].notna().sum()),
                "null_signal_count": int(panel["signal_value"].isna().sum()),
                "warmup_rows_excluded": warmup_excluded_rows,
                "duplicate_rows": int(panel[["date", "ticker", "candidate_id"]].duplicated().sum()),
                "panel_generation_status": PANEL_GENERATION_STATUS,
                "generation_status": "generated",
            }
        )
        validation_rows.append(
            {
                "candidate_id": candidate_id,
                "schema_status": "PASS",
                "registry_status": "PASS",
                "duplicate_status": "PASS",
                "warmup_trim_status": "PASS",
                "notes": "panel schema, registry ID, duplicate, and warmup checks passed",
            }
        )

    _write_csv(
        CANDIDATE_PANEL_GENERATION_DIR / "panel_manifest.csv",
        manifest_rows,
        [
            "candidate_id",
            "panel_path",
            "metadata_path",
            "row_count",
            "non_null_signal_count",
            "null_signal_count",
            "start_date",
            "end_date",
            "horizon",
            "formula_name",
            "formula_version",
            "warmup_window",
            "warmup_rows_excluded",
            "warmup_trimmed",
            "schema_status",
            "registry_status",
            "generation_status",
        ],
    )
    _write_csv(
        CANDIDATE_PANEL_GENERATION_DIR / "candidate_panel_generation_summary.csv",
        summary_rows,
        [
            "candidate_id",
            "working_name",
            "family",
            "theme",
            "horizon",
            "panel_role",
            "row_count",
            "non_null_signal_count",
            "null_signal_count",
            "warmup_rows_excluded",
            "duplicate_rows",
            "panel_generation_status",
            "generation_status",
        ],
    )
    _write_csv(
        CANDIDATE_PANEL_GENERATION_DIR / "panel_schema_validation_report.csv",
        validation_rows,
        [
            "candidate_id",
            "schema_status",
            "registry_status",
            "duplicate_status",
            "warmup_trim_status",
            "notes",
        ],
    )
    _write_json(
        CANDIDATE_PANEL_GENERATION_DIR / "panel_generation_manifest.json",
        {
            "run_id": RUN_ID,
            "panel_generation_status": PANEL_GENERATION_STATUS,
            "final_classification": PANEL_GENERATION_FINAL_CLASSIFICATION,
            "artifact_root": str(OUT_DIR),
            "candidate_panel_dir": str(CANDIDATE_PANELS_DIR),
            "candidate_panel_generation_dir": str(CANDIDATE_PANEL_GENERATION_DIR),
            "source_ohlcv_path": str(source_path),
            "candidate_count": len(manifest_rows),
            "approved_candidate_ids": APPROVED_CANDIDATE_IDS,
            "excluded_candidate_ids": ["nhlr_06"],
            "candidate_panels_generated": True,
            "panel_generation_executed": True,
            "discovery_executed": False,
            "ic_calculated": False,
            "redundancy_screening_run": False,
            "refinement_executed": False,
            "validation_executed": False,
            "governance_modified": False,
            "thresholds_modified": False,
            "production_registered": False,
            "ml_implemented": False,
        },
    )
    return manifest_rows, summary_rows


def validate_candidate_panels() -> tuple[bool, list[str]]:
    errors: list[str] = []
    manifest_path = CANDIDATE_PANEL_GENERATION_DIR / "panel_manifest.csv"
    summary_path = CANDIDATE_PANEL_GENERATION_DIR / "candidate_panel_generation_summary.csv"
    generation_manifest_path = CANDIDATE_PANEL_GENERATION_DIR / "panel_generation_manifest.json"

    for path in candidate_panel_generation_paths():
        if not path.exists():
            errors.append(f"missing panel-generation artifact: {path}")
    if not manifest_path.exists():
        return False, errors

    manifest_rows = _read_csv(manifest_path)
    manifest_ids = [str(row.get("candidate_id", "")) for row in manifest_rows]
    if manifest_ids != APPROVED_CANDIDATE_IDS:
        errors.append("panel manifest candidate IDs do not match authoritative registry order")
    if "nhlr_06" in manifest_ids:
        errors.append("excluded candidate nhlr_06 appears in panel manifest")
    panel_paths = [str(row.get("panel_path", "")) for row in manifest_rows]
    if len(panel_paths) != len(set(panel_paths)):
        errors.append("duplicate panel paths found in panel manifest")

    for row in manifest_rows:
        candidate_id = str(row.get("candidate_id", ""))
        panel_path = Path(str(row.get("panel_path", "")))
        metadata_path = Path(str(row.get("metadata_path", "")))
        if not panel_path.exists():
            errors.append(f"missing candidate panel: {panel_path}")
            continue
        panel = pd.read_parquet(panel_path)
        errors.extend(validate_candidate_panel_frame(panel, candidate_id))
        if not metadata_path.exists():
            errors.append(f"missing candidate panel metadata: {metadata_path}")
        else:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("candidate_id") != candidate_id:
                errors.append(f"metadata candidate_id mismatch for {candidate_id}")
            if int(metadata.get("row_count", -1)) != len(panel):
                errors.append(f"metadata row_count mismatch for {candidate_id}")
            if metadata.get("candidate_panels_generated") is not True:
                errors.append(f"metadata does not mark panel generation for {candidate_id}")
            for field in [
                "discovery_executed",
                "ic_calculated",
                "redundancy_screening_run",
                "refinement_executed",
                "validation_executed",
                "governance_modified",
                "thresholds_modified",
                "production_registered",
                "ml_implemented",
            ]:
                if metadata.get(field) is not False:
                    errors.append(f"metadata forbidden action field is not fail-closed for {candidate_id}: {field}")

    if summary_path.exists():
        summary_ids = [str(row.get("candidate_id", "")) for row in _read_csv(summary_path)]
        if summary_ids != APPROVED_CANDIDATE_IDS:
            errors.append("panel generation summary candidate IDs do not match authoritative registry order")

    if generation_manifest_path.exists():
        generation_manifest = json.loads(generation_manifest_path.read_text(encoding="utf-8"))
        if generation_manifest.get("final_classification") != PANEL_GENERATION_FINAL_CLASSIFICATION:
            errors.append("panel generation manifest final classification mismatch")
        if generation_manifest.get("candidate_panels_generated") is not True:
            errors.append("panel generation manifest does not mark candidate panels generated")
        for field in [
            "discovery_executed",
            "ic_calculated",
            "redundancy_screening_run",
            "refinement_executed",
            "validation_executed",
            "governance_modified",
            "thresholds_modified",
            "production_registered",
            "ml_implemented",
        ]:
            if generation_manifest.get(field) is not False:
                errors.append(f"panel generation manifest forbidden action field is not fail-closed: {field}")

    return not errors, errors


def write_scaffold() -> None:
    for directory in ARTIFACT_DIRS:
        directory.mkdir(parents=True, exist_ok=True)

    _write_csv(
        CANDIDATE_INVENTORY_DIR / "discovery_categories.csv",
        DISCOVERY_CATEGORIES,
        ["category_id", "category_name", "scaffold_status", "description"],
    )
    _write_csv(
        CANDIDATE_INVENTORY_DIR / "candidate_inventory_manifest.csv",
        [
            {
                "inventory_status": SCAFFOLD_STATUS,
                "candidate_count": 0,
                "candidate_generation_executed": False,
                "panel_generation_executed": False,
                "notes": "No candidates are defined or generated in scaffold v1.",
            }
        ],
        [
            "inventory_status",
            "candidate_count",
            "candidate_generation_executed",
            "panel_generation_executed",
            "notes",
        ],
    )

    manifest = {
        "run_id": RUN_ID,
        "scaffold_status": SCAFFOLD_STATUS,
        "final_classification": FINAL_CLASSIFICATION,
        "artifact_root": str(OUT_DIR),
        "category_count": len(DISCOVERY_CATEGORIES),
        "candidate_count": 0,
        "research_results_present": False,
        "candidate_generation_executed": False,
        "candidate_panels_generated": False,
        "discovery_executed": False,
        "ic_calculated": False,
        "redundancy_screening_run": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "production_registered": False,
        "ml_implemented": False,
    }
    _write_json(MANIFESTS_DIR / "scaffold_manifest.json", manifest)

    artifact_rows = [
        {
            "artifact": str(path.relative_to(OUT_DIR)),
            "scaffold_status": SCAFFOLD_STATUS,
            "placeholder_only": True,
            "research_results": False,
        }
        for path in artifact_paths()
    ]
    _write_csv(
        MANIFESTS_DIR / "artifact_manifest.csv",
        artifact_rows,
        ["artifact", "scaffold_status", "placeholder_only", "research_results"],
    )

    diagnostic_rows = [
        {
            "diagnostic": "artifact_tree_created",
            "scaffold_status": SCAFFOLD_STATUS,
            "status": "PASS",
            "research_results": False,
            "notes": "Required scaffold directories are created.",
        },
        {
            "diagnostic": "discovery_categories_declared",
            "scaffold_status": SCAFFOLD_STATUS,
            "status": "PASS",
            "research_results": False,
            "notes": "Eight approved high-level categories are listed without formulas.",
        },
        {
            "diagnostic": "candidate_inventory_empty",
            "scaffold_status": SCAFFOLD_STATUS,
            "status": "PASS",
            "research_results": False,
            "notes": "No candidates are generated or defined.",
        },
    ]
    _write_csv(
        DIAGNOSTICS_DIR / "scaffold_diagnostics.csv",
        diagnostic_rows,
        ["diagnostic", "scaffold_status", "status", "research_results", "notes"],
    )

    guardrail_rows = [
        {
            "guardrail": action,
            "scaffold_status": SCAFFOLD_STATUS,
            "executed": False,
            "status": "BLOCKED_BY_SCAFFOLD",
        }
        for action in FORBIDDEN_ACTIONS
    ]
    _write_csv(
        DIAGNOSTICS_DIR / "guardrail_diagnostics.csv",
        guardrail_rows,
        ["guardrail", "scaffold_status", "executed", "status"],
    )
    _write_csv(
        DIAGNOSTICS_DIR / "prohibited_action_diagnostics.csv",
        guardrail_rows,
        ["guardrail", "scaffold_status", "executed", "status"],
    )

    readiness_report = f"""# OHLCV Non-Hostile Transition and Leadership Rotation Discovery Readiness Report

Status: {SCAFFOLD_STATUS}

This placeholder report contains no research results. Discovery, candidate generation,
panel generation, IC calculation, redundancy screening, refinement, validation,
governance mutation, production registration, and ML remain blocked.

Readiness classification: {FINAL_CLASSIFICATION}
"""
    _write_text(DISCOVERY_SUMMARY_DIR / "discovery_readiness_report.md", readiness_report)
    _write_json(
        DISCOVERY_SUMMARY_DIR / "discovery_summary_placeholder.json",
        {
            "run_id": RUN_ID,
            "scaffold_status": SCAFFOLD_STATUS,
            "research_results_present": False,
            "summary": "No discovery has been executed. Placeholder only.",
        },
    )
    _write_csv(
        REDUNDANCY_SCREENING_DIR / "redundancy_screening_placeholder.csv",
        [
            {
                "screening_type": "conceptual_metadata_statistical",
                "scaffold_status": SCAFFOLD_STATUS,
                "screening_executed": False,
                "research_results": False,
                "notes": "Redundancy screening is not run in scaffold v1.",
            }
        ],
        ["screening_type", "scaffold_status", "screening_executed", "research_results", "notes"],
    )
    _write_text(
        IMPLEMENTATION_REVIEW_DIR / "implementation_review_placeholder.md",
        f"""# Implementation Review Placeholder

Status: {SCAFFOLD_STATUS}

This placeholder records scaffold creation only. It contains no candidate formulas,
no candidate panels, no discovery results, no IC results, no redundancy results,
no refinement results, no validation results, and no production or governance action.
""",
    )


def validate_scaffold() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for directory in ARTIFACT_DIRS:
        if not directory.is_dir():
            errors.append(f"missing directory: {directory}")
    for path in artifact_paths():
        if not path.exists():
            errors.append(f"missing artifact: {path}")

    manifest_path = MANIFESTS_DIR / "scaffold_manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for field in FORBIDDEN_ACTIONS:
            if manifest.get(field) is not False:
                errors.append(f"manifest field is not fail-closed: {field}")
        if manifest.get("scaffold_status") != SCAFFOLD_STATUS:
            errors.append("manifest scaffold_status is not SCAFFOLD_ONLY")
        if manifest.get("candidate_count") != 0:
            errors.append("manifest candidate_count is not 0")

    categories_path = CANDIDATE_INVENTORY_DIR / "discovery_categories.csv"
    if categories_path.exists():
        with categories_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != len(DISCOVERY_CATEGORIES):
            errors.append("unexpected discovery category count")
        if any(row.get("scaffold_status") != SCAFFOLD_STATUS for row in rows):
            errors.append("category scaffold_status must be SCAFFOLD_ONLY")

    return not errors, errors


def list_discovery_categories() -> None:
    for category in DISCOVERY_CATEGORIES:
        print(f"{category['category_id']}: {category['category_name']} [{SCAFFOLD_STATUS}]")


def list_candidates() -> None:
    for row in candidate_registry_rows():
        print(
            f"{row['candidate_id']}: {row['working_name']} | "
            f"{row['concept_category']} | {row['implementation_priority']} | {row['candidate_state']}"
        )


def list_candidate_implementations() -> None:
    from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
        implementation_rows,
    )

    for row in implementation_rows():
        print(
            f"{row['candidate_id']}: {row['working_name']} | "
            f"{row['concept_category']} | {row['implementation_priority']} | {row['implementation_status']}"
        )


def list_deliverables() -> None:
    for deliverable in DELIVERABLES:
        print(f"{deliverable['deliverable']}: {deliverable['path']} [{deliverable['scaffold_status']}]")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold-only runner for OHLCV non-hostile transition and leadership rotation discovery."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Create scaffold artifacts only.")
    group.add_argument("--list-discovery-categories", action="store_true", help="List approved discovery categories.")
    group.add_argument("--validate-scaffold", action="store_true", help="Validate scaffold artifacts and guardrails.")
    group.add_argument("--validate-artifact-structure", action="store_true", help="Validate required artifact structure.")
    group.add_argument("--list-deliverables", action="store_true", help="List scaffold deliverables.")
    group.add_argument("--list-candidates", action="store_true", help="List approved registry candidates only.")
    group.add_argument(
        "--export-candidate-registry",
        action="store_true",
        help="Export metadata-only candidate registry artifacts.",
    )
    group.add_argument(
        "--validate-candidate-registry",
        action="store_true",
        help="Validate metadata-only candidate registry artifacts.",
    )
    group.add_argument(
        "--list-candidate-implementations",
        action="store_true",
        help="List registry-derived candidate implementations only.",
    )
    group.add_argument(
        "--export-candidate-implementations",
        action="store_true",
        help="Export implementation-only candidate manifests and diagnostics.",
    )
    group.add_argument(
        "--validate-candidate-implementations",
        action="store_true",
        help="Validate implementation-only candidate manifests and diagnostics.",
    )
    group.add_argument(
        "--write-candidate-panels",
        action="store_true",
        help="Serialize formula outputs into research-only candidate panel artifacts.",
    )
    group.add_argument(
        "--validate-candidate-panels",
        action="store_true",
        help="Validate research-only candidate panel artifacts.",
    )
    parser.add_argument(
        "--candidate-panel-source",
        type=Path,
        default=RAW_OHLCV_PATH,
        help="OHLCV parquet source for --write-candidate-panels.",
    )
    args = parser.parse_args()

    if args.dry_run:
        write_scaffold()
        print(f"Wrote {SCAFFOLD_STATUS} artifacts to {OUT_DIR}")
        print("No discovery, candidate generation, panel generation, IC calculation, redundancy screening, refinement, validation, governance mutation, production registration, or ML executed.")
        print(FINAL_CLASSIFICATION)
        return 0
    if args.list_discovery_categories:
        list_discovery_categories()
        return 0
    if args.list_candidates:
        list_candidates()
        return 0
    if args.list_candidate_implementations:
        list_candidate_implementations()
        return 0
    if args.export_candidate_registry:
        write_candidate_registry()
        print(f"Wrote {REGISTRY_STATUS} candidate registry artifacts to {CANDIDATE_REGISTRY_DIR}")
        print("No formulas, candidate code, panels, discovery, IC calculation, redundancy screening, refinement, validation, governance mutation, production registration, or ML executed.")
        print(REGISTRY_FINAL_CLASSIFICATION)
        return 0
    if args.export_candidate_implementations:
        write_candidate_implementations()
        print(f"Wrote {IMPLEMENTATION_STATUS} candidate implementation artifacts to {CANDIDATE_IMPLEMENTATION_DIR}")
        print("No candidate panels, discovery, IC calculation, redundancy screening, refinement, validation, governance mutation, production registration, or ML executed.")
        print(IMPLEMENTATION_FINAL_CLASSIFICATION)
        return 0
    if args.validate_candidate_registry:
        ok, errors = validate_candidate_registry()
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"{REGISTRY_STATUS} validation passed for {CANDIDATE_REGISTRY_DIR}")
        return 0
    if args.validate_candidate_implementations:
        ok, errors = validate_candidate_implementation_artifacts()
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"{IMPLEMENTATION_STATUS} validation passed for {CANDIDATE_IMPLEMENTATION_DIR}")
        return 0
    if args.write_candidate_panels:
        manifest_rows, _summary_rows = write_candidate_panels(args.candidate_panel_source)
        print(f"Wrote {PANEL_GENERATION_STATUS} candidate panels to {CANDIDATE_PANELS_DIR}")
        print(f"Wrote panel manifest to {CANDIDATE_PANEL_GENERATION_DIR / 'panel_manifest.csv'}")
        print(f"Candidate panel count: {len(manifest_rows)}")
        print("No discovery, IC calculation, redundancy screening, refinement, validation, governance mutation, production registration, threshold changes, or ML executed.")
        print(PANEL_GENERATION_FINAL_CLASSIFICATION)
        return 0
    if args.validate_candidate_panels:
        ok, errors = validate_candidate_panels()
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"{PANEL_GENERATION_STATUS} validation passed for {CANDIDATE_PANELS_DIR}")
        return 0
    if args.list_deliverables:
        list_deliverables()
        return 0
    if args.validate_scaffold or args.validate_artifact_structure:
        ok, errors = validate_scaffold()
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"{SCAFFOLD_STATUS} validation passed for {OUT_DIR}")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
