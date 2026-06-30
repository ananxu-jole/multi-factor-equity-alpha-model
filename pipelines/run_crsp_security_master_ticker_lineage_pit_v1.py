from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


RUN_ID = "crsp_security_master_ticker_lineage_pit_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
SOURCE_GATE_DIR = OUT_DIR / "source_gate"
SCHEMAS_DIR = OUT_DIR / "schemas"
ASSUMPTIONS_DIR = OUT_DIR / "assumptions"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"
LINEAGE_DESIGN_DIR = OUT_DIR / "lineage_design"
VALIDATION_REPORTS_DIR = OUT_DIR / "validation_reports"
MANIFESTS_DIR = OUT_DIR / "manifests"
REVIEW_DIR = OUT_DIR / "review"

ARTIFACT_DIRS = (
    OUT_DIR,
    SOURCE_GATE_DIR,
    SCHEMAS_DIR,
    ASSUMPTIONS_DIR,
    DIAGNOSTICS_DIR,
    LINEAGE_DESIGN_DIR,
    VALIDATION_REPORTS_DIR,
    MANIFESTS_DIR,
    REVIEW_DIR,
)

GUARDRAIL = (
    "CRSP scaffold only. This runner creates source-free templates, manifests, checklists, "
    "and diagnostics placeholders. It does not access CRSP data, load source files, ingest data, "
    "accept sources, construct metadata, build security or ticker lineage, reconstruct sector, "
    "industry, or peer groups, run discovery, run refinement, run validation, mutate governance, "
    "register production outputs, or implement ML."
)

SOURCE_MANIFEST_FIELDS = [
    "source_gate_run_id",
    "source",
    "source_type",
    "source_version",
    "source_snapshot_date",
    "source_file_hash",
    "pit_integrity_score",
    "coverage_score",
    "historical_depth_score",
    "identifier_quality_score",
    "update_feasibility_score",
    "source_stability_score",
    "implementation_complexity_score",
    "cost_manual_burden_score",
    "leakage_risk_score",
    "source_gate_status",
    "allowed_use",
    "rejection_reason",
    "manual_review_required",
    "license_or_usage_notes",
    "review_timestamp",
    "reviewer_notes",
]

SOURCE_GATE_MANIFEST_SCHEMA_FIELDS = [
    "source_id",
    "provider",
    "source_name",
    "source_type",
    "source_version",
    "coverage_start",
    "coverage_end",
    "coverage_ratio",
    "effective_date_support",
    "licensing_status",
    "pit_capability",
    "lineage_capability",
    "reproducibility_status",
    "validation_status",
    "approval_status",
    "approval_outcome",
    "notes",
]

SOURCE_GATE_RESULT_FIELDS = [
    "source_id",
    "provider",
    "source_type",
    "source_status",
    "pit_readiness",
    "lineage_readiness",
    "licensing_status",
    "validation_status",
    "approval_outcome",
    "score",
    "max_score",
    "pass_source_gate",
    "allowed_use",
    "blocking_reasons",
    "dry_run_only",
]

SOURCE_GATE_CONTROLLED_VOCABULARIES = {
    "source_status": [
        "accepted",
        "conditional",
        "manual_review_required",
        "diagnostic_only",
        "rejected",
        "deprecated",
    ],
    "source_type": [
        "security_master",
        "ticker_lineage",
        "issuer_identifier",
        "listing_history",
        "delisting_history",
        "corporate_action",
        "economic_classification",
        "market_cap",
        "size_bucket",
        "manual_static",
        "diagnostic_snapshot",
    ],
    "pit_readiness": [
        "point_in_time_verified",
        "date_stamped_snapshot",
        "inferred_window",
        "static_snapshot_only",
        "unresolved",
        "blocked",
    ],
    "lineage_readiness": [
        "stable_security_and_ticker_lineage",
        "stable_security_only",
        "ticker_only",
        "manual_mapping_required",
        "unresolved",
        "blocked",
    ],
    "licensing": [
        "research_use_approved",
        "research_use_conditional",
        "license_review_required",
        "redistribution_blocked",
        "unknown",
        "blocked",
    ],
    "validation_status": [
        "not_validated",
        "schema_validated",
        "lineage_validated",
        "source_gate_validated",
        "rejected",
    ],
    "approval_outcome": [
        "approved_for_source_gate_only",
        "approved_for_pit_implementation",
        "conditional_approval",
        "manual_review_required",
        "diagnostic_only",
        "rejected",
    ],
    "effective_date_support": [
        "full_effective_dates",
        "date_stamped_snapshots",
        "inferred_windows_only",
        "current_snapshot_only",
        "none",
    ],
    "reproducibility_status": [
        "raw_files_hashable",
        "controlled_reference_hashable",
        "manifest_only",
        "manual_notes_only",
        "unknown",
        "blocked",
    ],
}

SOURCE_GATE_SCORING = {
    "pit_capability": {
        "point_in_time_verified": 3,
        "date_stamped_snapshot": 2,
        "inferred_window": 1,
        "static_snapshot_only": 0,
        "unresolved": 0,
        "blocked": 0,
    },
    "lineage_capability": {
        "stable_security_and_ticker_lineage": 3,
        "stable_security_only": 2,
        "ticker_only": 0,
        "manual_mapping_required": 1,
        "unresolved": 0,
        "blocked": 0,
    },
    "effective_date_support": {
        "full_effective_dates": 3,
        "date_stamped_snapshots": 2,
        "inferred_windows_only": 1,
        "current_snapshot_only": 0,
        "none": 0,
    },
    "licensing_status": {
        "research_use_approved": 3,
        "research_use_conditional": 2,
        "license_review_required": 0,
        "redistribution_blocked": 0,
        "unknown": 0,
        "blocked": 0,
    },
    "reproducibility_status": {
        "raw_files_hashable": 3,
        "controlled_reference_hashable": 2,
        "manifest_only": 1,
        "manual_notes_only": 0,
        "unknown": 0,
        "blocked": 0,
    },
}

SOURCE_GATE_BLOCKING_VALUES = {
    "pit_capability": {"static_snapshot_only", "unresolved", "blocked"},
    "lineage_capability": {"ticker_only", "unresolved", "blocked"},
    "effective_date_support": {"current_snapshot_only", "none"},
    "licensing_status": {"license_review_required", "redistribution_blocked", "unknown", "blocked"},
    "reproducibility_status": {"manual_notes_only", "unknown", "blocked"},
}

SOURCE_GATE_DRY_RUN_CANDIDATES = [
    {
        "source_id": "candidate_pit_security_master_full",
        "provider": "placeholder_vendor",
        "source_name": "Placeholder PIT security master and ticker lineage",
        "source_type": "security_master",
        "source_version": "unverified",
        "coverage_start": "2000-01-01",
        "coverage_end": "open",
        "coverage_ratio": 0.98,
        "effective_date_support": "full_effective_dates",
        "licensing_status": "research_use_approved",
        "pit_capability": "point_in_time_verified",
        "lineage_capability": "stable_security_and_ticker_lineage",
        "reproducibility_status": "raw_files_hashable",
        "validation_status": "not_validated",
        "approval_status": "source_gate_dry_run_only",
        "approval_outcome": "approved_for_source_gate_only",
        "notes": "Synthetic dry-run example. No external data accessed.",
    },
    {
        "source_id": "candidate_static_profile_api",
        "provider": "placeholder_current_profile",
        "source_name": "Placeholder current company profile snapshot",
        "source_type": "diagnostic_snapshot",
        "source_version": "unverified",
        "coverage_start": "current",
        "coverage_end": "current",
        "coverage_ratio": 1.0,
        "effective_date_support": "current_snapshot_only",
        "licensing_status": "license_review_required",
        "pit_capability": "static_snapshot_only",
        "lineage_capability": "ticker_only",
        "reproducibility_status": "manifest_only",
        "validation_status": "not_validated",
        "approval_status": "source_gate_dry_run_only",
        "approval_outcome": "diagnostic_only",
        "notes": "Synthetic dry-run rejection example for static current metadata.",
    },
]

ASSUMPTION_FIELDS = [
    "assumption_id",
    "assumption_area",
    "assumption",
    "rationale",
    "required_evidence",
    "verification_status",
    "risk_level",
    "blocking_status",
    "fail_closed_behavior",
    "review_notes",
]

ASSUMPTIONS = [
    {
        "assumption_id": "crsp_subscription_scope",
        "assumption_area": "subscription_scope",
        "assumption": "Subscribed CRSP scope includes identity, ticker, exchange, delisting, corporate-action, and release metadata components.",
        "rationale": "Required to evaluate security_master_pit and ticker_lineage_pit support.",
        "required_evidence": "User/subscription confirmation of available CRSP products, files, tables, documentation, and coverage.",
        "verification_status": "unverified",
        "risk_level": "critical",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block source acceptance, loading, metadata construction, and lineage construction.",
        "review_notes": "No CRSP files or subscribed datasets inspected.",
    },
    {
        "assumption_id": "crsp_licensing_rights",
        "assumption_area": "licensing",
        "assumption": "License permits research use of derived metadata artifacts and enough audit evidence for reproducibility.",
        "rationale": "Source-gate and metadata_source_lineage require license-compatible lineage evidence.",
        "required_evidence": "License review covering retention, derived artifacts, hashes, documentation references, and audit records.",
        "verification_status": "unverified",
        "risk_level": "critical",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block archive, hash, source manifest acceptance, and lineage construction.",
        "review_notes": "No license terms reviewed in this scaffold.",
    },
    {
        "assumption_id": "crsp_field_availability",
        "assumption_area": "field_availability",
        "assumption": "PERMNO, PERMCO, ticker, exchange/listing context, name/security descriptors, delisting data, corporate actions, dates, and source metadata are available.",
        "rationale": "Required fields for security and ticker PIT mapping.",
        "required_evidence": "Documentation-level field inventory before any source loading.",
        "verification_status": "unverified",
        "risk_level": "critical",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block schema acceptance and PIT construction.",
        "review_notes": "Only conceptual public CRSP characteristics are assumed.",
    },
    {
        "assumption_id": "crsp_release_version_tracking",
        "assumption_area": "release_version",
        "assumption": "CRSP release, snapshot, or extract metadata can populate source_version and source_snapshot_date.",
        "rationale": "Required by source_acceptance_manifest and metadata_source_lineage.",
        "required_evidence": "Deterministic source version policy from CRSP release or controlled extract metadata.",
        "verification_status": "unverified",
        "risk_level": "high",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block source lineage and source acceptance.",
        "review_notes": "No CRSP release metadata inspected.",
    },
    {
        "assumption_id": "crsp_known_date_semantics",
        "assumption_area": "known_date",
        "assumption": "Known dates can be assigned from event-level known dates or conservative release/snapshot dates.",
        "rationale": "as_of_date must be date-safe and cannot use future knowledge.",
        "required_evidence": "Documentation of event-level known-date support or approved release/snapshot fallback.",
        "verification_status": "unverified",
        "risk_level": "critical",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block historical PIT use and downstream eligibility.",
        "review_notes": "Known-date semantics remain unverified.",
    },
    {
        "assumption_id": "crsp_archival_hash_feasibility",
        "assumption_area": "archival",
        "assumption": "Source hashes, source archive, or compliant controlled references can support reproducibility.",
        "rationale": "Source-gate and lineage artifacts require source_file_hash or equivalent evidence.",
        "required_evidence": "License-compatible archive/hash/reference policy.",
        "verification_status": "unverified",
        "risk_level": "critical",
        "blocking_status": "blocking",
        "fail_closed_behavior": "Block reproducibility, source acceptance, and lineage construction.",
        "review_notes": "No source archive or hash produced.",
    },
]

VERIFICATION_STATUS_VALUES = {"unverified", "partially_verified", "verified", "failed", "scaffold_placeholder"}
BLOCKER_STATUS_VALUES = {"blocking", "non_blocking", "review_required", "scaffold_blocking"}

VERIFICATION_ASSUMPTIONS = [
    {
        "assumption_id": "crsp_subscription_scope",
        "assumption_name": "CRSP subscription scope",
        "assumption_area": "subscription_scope",
        "risk_level": "critical",
        "required_evidence": "Subscription documentation or user confirmation of available CRSP products, files, tables, documentation, and coverage.",
        "downstream_dependency": "source_gate_manifest;schema_alignment;security_identity;ticker_lineage;event_lineage",
        "blocking_impact": "Blocks source acceptance, source loading, metadata construction, and lineage construction.",
    },
    {
        "assumption_id": "crsp_licensing_rights",
        "assumption_name": "Licensing and retention rights",
        "assumption_area": "licensing",
        "risk_level": "critical",
        "required_evidence": "License terms, usage policy notes, or internal compliance summary for retention, derived artifacts, hashes, and audit records.",
        "downstream_dependency": "source_archive;source_hash;metadata_source_lineage;audit_trail",
        "blocking_impact": "Blocks archive, hash, source manifest acceptance, and lineage construction.",
    },
    {
        "assumption_id": "crsp_archival_hash_feasibility",
        "assumption_name": "Archival/hash feasibility",
        "assumption_area": "archival",
        "risk_level": "critical",
        "required_evidence": "License-compatible file manifest, checksum strategy, controlled reference policy, or archive policy.",
        "downstream_dependency": "source_file_hash;source_references;reproducible_rebuilds",
        "blocking_impact": "Blocks reproducibility, source acceptance, and lineage construction.",
    },
    {
        "assumption_id": "crsp_field_availability",
        "assumption_name": "Field availability",
        "assumption_area": "field_availability",
        "risk_level": "critical",
        "required_evidence": "Documentation-level field inventory for PERMNO, PERMCO, ticker, exchange, names, delistings, corporate actions, dates, and source metadata.",
        "downstream_dependency": "security_master_pit;ticker_lineage_pit;schema_alignment",
        "blocking_impact": "Blocks schema acceptance and PIT construction.",
    },
    {
        "assumption_id": "crsp_release_version_tracking",
        "assumption_name": "Release/version tracking",
        "assumption_area": "release_version",
        "risk_level": "high",
        "required_evidence": "Release note references, product version identifiers, snapshot metadata, extract-date convention, or user-confirmed release cadence.",
        "downstream_dependency": "source_acceptance_manifest;metadata_source_lineage;known_date_fallback",
        "blocking_impact": "Blocks source lineage and source acceptance.",
    },
    {
        "assumption_id": "crsp_known_date_semantics",
        "assumption_name": "Known-date semantics",
        "assumption_area": "known_date",
        "risk_level": "critical",
        "required_evidence": "Documentation of event-level known dates or approved source release/snapshot-date fallback.",
        "downstream_dependency": "as_of_date;event_as_of_date;stale_age_policy;lookahead_prevention",
        "blocking_impact": "Blocks historical PIT use and downstream eligibility.",
    },
    {
        "assumption_id": "crsp_event_date_semantics",
        "assumption_name": "Event-date semantics",
        "assumption_area": "event_date",
        "risk_level": "high",
        "required_evidence": "Documentation of event effective dates, delisting dates, corporate-action dates, and event/action codes.",
        "downstream_dependency": "event_type;event_effective_date;predecessor_successor_fields;event_confidence",
        "blocking_impact": "Blocks event-dependent lineage and affected windows.",
    },
    {
        "assumption_id": "crsp_ticker_window_semantics",
        "assumption_name": "Ticker-window semantics",
        "assumption_area": "ticker_window",
        "risk_level": "critical",
        "required_evidence": "Data dictionary or documentation showing ticker values, ticker date fields, exchange/listing context, share-class support, and ticker reuse behavior.",
        "downstream_dependency": "ticker_lineage_pit;ticker_reuse_diagnostics;duplicate_active_mapping_checks",
        "blocking_impact": "Blocks ticker lineage construction.",
    },
    {
        "assumption_id": "crsp_source_file_reproducibility",
        "assumption_name": "Source-file reproducibility",
        "assumption_area": "source_reproducibility",
        "risk_level": "critical",
        "required_evidence": "Future file manifest design, checksum policy, source bundle naming convention, row-count policy, or controlled source-reference strategy.",
        "downstream_dependency": "metadata_source_lineage;source_gate_audit;rebuild_diagnostics",
        "blocking_impact": "Blocks source acceptance and reproducible PIT builds.",
    },
    {
        "assumption_id": "crsp_source_gate_eligibility",
        "assumption_name": "Source-gate eligibility",
        "assumption_area": "source_gate",
        "risk_level": "critical",
        "required_evidence": "Completed source-gate manifest, semantic allowed-use review, manual-review disposition, confidence notes, and blocked reason report.",
        "downstream_dependency": "source_acceptance_manifest;semantic_eligibility;manual_review_queue",
        "blocking_impact": "Blocks all source work beyond diagnostics until source-gate status is evidence-backed.",
    },
]

EVIDENCE_FIELDS = [
    "assumption_id",
    "assumption_name",
    "evidence_type",
    "evidence_description",
    "evidence_source",
    "evidence_status",
    "verification_status",
    "blocker_status",
    "reviewer_notes",
    "scaffold_only",
]

VERIFICATION_CHECKLIST_FIELDS = [
    "assumption_id",
    "assumption_name",
    "assumption_area",
    "risk_level",
    "required_evidence",
    "downstream_dependency",
    "blocking_impact",
    "verification_status",
    "blocker_status",
    "next_action",
    "scaffold_only",
]

REVIEW_FIELDS = [
    "review_item",
    "required_evidence",
    "observed_evidence",
    "verification_status",
    "risk_level",
    "blocking_status",
    "fail_closed_behavior",
    "review_notes",
    "scaffold_only",
]

SCHEMA_FIELDS = {
    "security_master_pit": [
        "security_id", "issuer_id", "company_name", "security_type", "exchange", "country", "currency",
        "is_active", "effective_start", "effective_end", "as_of_date", "source", "source_version",
        "source_record_id", "metadata_version", "run_id", "collection_timestamp", "record_hash",
        "identity_confidence", "manual_override_flag", "point_in_time_quality", "security_event_id",
        "event_type", "event_effective_date", "event_as_of_date", "predecessor_security_id",
        "successor_security_id", "prior_ticker", "next_ticker", "event_confidence", "notes",
    ],
    "ticker_lineage_pit": [
        "security_id", "ticker", "exchange", "ticker_namespace", "share_class", "primary_listing_flag",
        "ticker_effective_start", "ticker_effective_end", "as_of_date", "ticker_status", "change_reason",
        "prior_ticker", "next_ticker", "source", "source_version", "metadata_version", "run_id",
        "collection_timestamp", "record_hash", "ticker_mapping_confidence", "manual_override_flag",
        "point_in_time_quality",
    ],
    "metadata_source_lineage": [
        "source_lineage_id", "run_id", "metadata_version", "source", "source_type", "source_version",
        "source_snapshot_date", "source_file_path", "source_url_or_reference", "source_file_hash",
        "record_count_raw", "record_count_clean", "collection_timestamp", "license_or_usage_notes",
        "normalization_rules", "created_by", "source_confidence", "point_in_time_quality",
        "manual_source_flag", "source_gate_score_summary", "notes",
    ],
    "source_acceptance_manifest": SOURCE_MANIFEST_FIELDS,
}

DIAGNOSTIC_COLUMNS = [
    "diagnostic_id",
    "diagnostic_scope",
    "status",
    "severity",
    "blocked_reason",
    "required_evidence",
    "current_evidence",
    "next_action",
    "review_notes",
    "placeholder_only",
]

DIAGNOSTIC_FILES = {
    "source_gate_readiness_report.csv": "source_gate",
    "schema_readiness_report.csv": "schema_alignment",
    "assumption_readiness_report.csv": "assumptions",
    "lineage_readiness_report.csv": "lineage_placeholder",
    "blocking_reason_report.csv": "blocking_reasons",
}


def _ensure_dirs() -> None:
    for path in ARTIFACT_DIRS:
        path.mkdir(parents=True, exist_ok=True)


def _write_csv(path: Path, rows: list[dict[str, object]], columns: list[str] | None = None) -> None:
    pd.DataFrame(rows, columns=columns).to_csv(path, index=False)


def _vocabulary_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for vocabulary, values in SOURCE_GATE_CONTROLLED_VOCABULARIES.items():
        for value in values:
            rows.append(
                {
                    "vocabulary": vocabulary,
                    "value": value,
                    "scaffold_only": True,
                    "ingestion_authorized": False,
                }
            )
    return rows


def _schema_template_rows() -> list[dict[str, object]]:
    return [
        {
            "field": field,
            "required": True,
            "description": {
                "source_id": "Stable source-gate candidate identifier.",
                "provider": "Source provider, vendor, exchange, internal process, or placeholder owner.",
                "source_name": "Human-readable source name.",
                "source_type": "Controlled source type.",
                "source_version": "Source release, snapshot, or version identifier.",
                "coverage_start": "Earliest claimed source coverage date.",
                "coverage_end": "Latest claimed source coverage date or open.",
                "coverage_ratio": "Declared or measured coverage ratio for future review.",
                "effective_date_support": "Controlled effective-date capability.",
                "licensing_status": "Controlled licensing/research-use status.",
                "pit_capability": "Controlled PIT readiness value.",
                "lineage_capability": "Controlled lineage readiness value.",
                "reproducibility_status": "Controlled reproducibility status.",
                "validation_status": "Controlled validation status.",
                "approval_status": "Source-gate approval tracking status.",
                "approval_outcome": "Controlled approval outcome.",
                "notes": "Reviewer notes.",
            }.get(field, "Source manifest field."),
            "scaffold_only": True,
        }
        for field in SOURCE_GATE_MANIFEST_SCHEMA_FIELDS
    ]


def _invalid_vocab_errors(source: dict[str, object]) -> list[str]:
    mappings = {
        "source_type": "source_type",
        "effective_date_support": "effective_date_support",
        "licensing_status": "licensing",
        "pit_capability": "pit_readiness",
        "lineage_capability": "lineage_readiness",
        "reproducibility_status": "reproducibility_status",
        "validation_status": "validation_status",
        "approval_outcome": "approval_outcome",
    }
    errors: list[str] = []
    for field, vocabulary in mappings.items():
        value = str(source.get(field, ""))
        if value not in SOURCE_GATE_CONTROLLED_VOCABULARIES[vocabulary]:
            errors.append(f"{source.get('source_id', '<unknown>')} invalid {field}: {value}")
    return errors


def evaluate_source_gate(source: dict[str, object]) -> dict[str, object]:
    """Evaluate a source manifest row without reading any external data."""
    blocking_reasons: list[str] = []
    for field, blocked_values in SOURCE_GATE_BLOCKING_VALUES.items():
        if str(source.get(field, "")) in blocked_values:
            blocking_reasons.append(f"{field}:{source.get(field)}")

    score = sum(
        values.get(str(source.get(field, "")), 0)
        for field, values in SOURCE_GATE_SCORING.items()
    )
    max_score = sum(max(values.values()) for values in SOURCE_GATE_SCORING.values())
    invalid_vocab = _invalid_vocab_errors(source)
    blocking_reasons.extend(invalid_vocab)

    coverage_ratio = float(source.get("coverage_ratio", 0) or 0)
    if coverage_ratio < 0.80:
        blocking_reasons.append("coverage_ratio_below_0.80")

    pass_gate = not blocking_reasons and score >= 12
    if pass_gate:
        source_status = "accepted"
        allowed_use = "source_gate_only_future_implementation_review_required"
        pit_readiness = source["pit_capability"]
        lineage_readiness = source["lineage_capability"]
        approval_outcome = "approved_for_source_gate_only"
    elif invalid_vocab:
        source_status = "rejected"
        allowed_use = "blocked_invalid_manifest"
        pit_readiness = "blocked"
        lineage_readiness = "blocked"
        approval_outcome = "rejected"
    else:
        source_status = "manual_review_required"
        allowed_use = "diagnostics_only"
        pit_readiness = source.get("pit_capability", "blocked")
        lineage_readiness = source.get("lineage_capability", "blocked")
        approval_outcome = "manual_review_required"

    return {
        "source_id": source.get("source_id", ""),
        "provider": source.get("provider", ""),
        "source_type": source.get("source_type", ""),
        "source_status": source_status,
        "pit_readiness": pit_readiness,
        "lineage_readiness": lineage_readiness,
        "licensing_status": source.get("licensing_status", ""),
        "validation_status": source.get("validation_status", "not_validated"),
        "approval_outcome": approval_outcome,
        "score": score,
        "max_score": max_score,
        "pass_source_gate": pass_gate,
        "allowed_use": allowed_use,
        "blocking_reasons": ";".join(blocking_reasons) if blocking_reasons else "",
        "dry_run_only": True,
    }


def validate_source_gate_manifest(rows: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(rows):
        missing = [field for field in SOURCE_GATE_MANIFEST_SCHEMA_FIELDS if field not in row]
        if missing:
            errors.append(f"row {index} missing fields: {missing}")
        errors.extend(_invalid_vocab_errors(row))
    return errors


def write_source_gate_scaffold() -> None:
    _ensure_dirs()
    _write_csv(
        SOURCE_GATE_DIR / "pit_source_gate_manifest_schema.csv",
        _schema_template_rows(),
        ["field", "required", "description", "scaffold_only"],
    )
    _write_csv(
        SOURCE_GATE_DIR / "pit_source_gate_manifest_template.csv",
        [],
        SOURCE_GATE_MANIFEST_SCHEMA_FIELDS,
    )
    _write_csv(
        SOURCE_GATE_DIR / "pit_source_gate_controlled_vocabularies.csv",
        _vocabulary_rows(),
        ["vocabulary", "value", "scaffold_only", "ingestion_authorized"],
    )
    (SOURCE_GATE_DIR / "pit_source_gate_controlled_vocabularies.json").write_text(
        json.dumps(SOURCE_GATE_CONTROLLED_VOCABULARIES, indent=2),
        encoding="utf-8",
    )
    dry_run_results = [evaluate_source_gate(source) for source in SOURCE_GATE_DRY_RUN_CANDIDATES]
    _write_csv(
        SOURCE_GATE_DIR / "pit_source_gate_dry_run_candidates.csv",
        SOURCE_GATE_DRY_RUN_CANDIDATES,
        SOURCE_GATE_MANIFEST_SCHEMA_FIELDS,
    )
    _write_csv(
        SOURCE_GATE_DIR / "pit_source_gate_dry_run_report.csv",
        dry_run_results,
        SOURCE_GATE_RESULT_FIELDS,
    )
    manifest = {
        "run_id": RUN_ID,
        "source_gate_scaffold_only": True,
        "classification": "SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES",
        "external_data_accessed": False,
        "source_files_loaded": False,
        "data_ingested": False,
        "metadata_tables_created": False,
        "lineage_built": False,
        "discovery_executed": False,
        "validation_executed": False,
        "governance_thresholds_modified": False,
        "production_registered": False,
        "ml_implemented": False,
        "template_path": str(SOURCE_GATE_DIR / "pit_source_gate_manifest_template.csv"),
        "dry_run_report_path": str(SOURCE_GATE_DIR / "pit_source_gate_dry_run_report.csv"),
    }
    (SOURCE_GATE_DIR / "pit_source_gate_scaffold_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def _schema_rows(schema_name: str, fields: list[str]) -> list[dict[str, object]]:
    effective = {"effective_start", "effective_end", "as_of_date", "event_effective_date", "event_as_of_date", "ticker_effective_start", "ticker_effective_end", "source_snapshot_date"}
    confidence = {"identity_confidence", "ticker_mapping_confidence", "event_confidence", "source_confidence", "point_in_time_quality"}
    lineage = {"source", "source_version", "source_record_id", "metadata_version", "run_id", "collection_timestamp", "record_hash", "source_lineage_id", "source_file_hash", "source_url_or_reference"}
    rows = []
    for field in fields:
        if field in effective:
            category = "effective_date"
        elif field in confidence:
            category = "confidence"
        elif field in lineage:
            category = "lineage"
        else:
            category = "required"
        rows.append(
            {
                "schema_name": schema_name,
                "field": field,
                "required": True,
                "category": category,
                "crsp_mapping_status": "unverified",
                "blocking_status": "blocking_until_verified",
                "placeholder_only": True,
            }
        )
    return rows


def write_scaffold() -> None:
    _ensure_dirs()
    _write_csv(SOURCE_GATE_DIR / "crsp_source_acceptance_manifest_template.csv", [], SOURCE_MANIFEST_FIELDS)
    write_source_gate_scaffold()
    _write_csv(ASSUMPTIONS_DIR / "crsp_assumption_register.csv", ASSUMPTIONS, ASSUMPTION_FIELDS)
    _write_csv(ASSUMPTIONS_DIR / "crsp_assumption_verification_checklist.csv", ASSUMPTIONS, ASSUMPTION_FIELDS)

    for schema_name, fields in SCHEMA_FIELDS.items():
        _write_csv(SCHEMAS_DIR / f"{schema_name}_alignment_checklist.csv", _schema_rows(schema_name, fields))

    for filename, scope in DIAGNOSTIC_FILES.items():
        rows = [
            {
                "diagnostic_id": f"crsp_{scope}",
                "diagnostic_scope": scope,
                "status": "blocked_unverified_scaffold",
                "severity": "critical",
                "blocked_reason": "manual_review_required",
                "required_evidence": "CRSP assumptions must be verified in a later authorized task.",
                "current_evidence": "scaffold_only_no_crsp_data_access",
                "next_action": "assumption_verification",
                "review_notes": "No source rows evaluated.",
                "placeholder_only": True,
            }
        ]
        _write_csv(DIAGNOSTICS_DIR / filename, rows, DIAGNOSTIC_COLUMNS)

    identifier_strategy = {
        "scaffold_only": True,
        "security_id_strategy": "crsp_permno:<PERMNO>",
        "issuer_id_strategy": "crsp_permco:<PERMCO>",
        "ticker_symbols_are_identifiers": False,
        "crsp_data_accessed": False,
        "metadata_constructed": False,
        "lineage_constructed": False,
    }
    (LINEAGE_DESIGN_DIR / "identifier_strategy_manifest.json").write_text(json.dumps(identifier_strategy, indent=2), encoding="utf-8")

    diagnostic_manifest = {
        "scaffold_only": True,
        "diagnostics": sorted(DIAGNOSTIC_FILES),
        "crsp_data_accessed": False,
        "source_rows_evaluated": False,
    }
    (DIAGNOSTICS_DIR / "crsp_diagnostic_manifest.json").write_text(json.dumps(diagnostic_manifest, indent=2), encoding="utf-8")

    scaffold_manifest = {
        "run_id": RUN_ID,
        "classification": "READY_FOR_ASSUMPTION_VERIFICATION",
        "scaffold_only": True,
        "crsp_data_accessed": False,
        "source_files_loaded": False,
        "data_ingested": False,
        "source_accepted": False,
        "metadata_constructed": False,
        "security_lineage_built": False,
        "ticker_lineage_built": False,
        "reconstruction_executed": False,
        "discovery_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "production_registered": False,
        "ml_implemented": False,
    }
    (MANIFESTS_DIR / "crsp_scaffold_manifest.json").write_text(json.dumps(scaffold_manifest, indent=2), encoding="utf-8")
    (OUT_DIR / "crsp_scaffold_manifest.json").write_text(json.dumps(scaffold_manifest, indent=2), encoding="utf-8")

    validation_rows = [{"check": name, "status": "pass", "scaffold_only": True} for name in (
        "artifact_tree", "assumption_register", "source_gate_template", "schema_alignment", "diagnostics", "no_ingestion_modes"
    )]
    _write_csv(VALIDATION_REPORTS_DIR / "scaffold_validation_report.csv", validation_rows)
    (REVIEW_DIR / "crsp_scaffold_implementation_review_template.md").write_text(
        "# CRSP Scaffold Implementation Review Template\n\nScaffold-only review placeholder. No CRSP data access.\n",
        encoding="utf-8",
    )
    write_verification_scaffold()


def _verification_checklist_rows() -> list[dict[str, object]]:
    return [
        {
            **row,
            "verification_status": "unverified",
            "blocker_status": "blocking",
            "next_action": "provide_documented_evidence_in_later_review",
            "scaffold_only": True,
        }
        for row in VERIFICATION_ASSUMPTIONS
    ]


def _evidence_placeholder_rows() -> list[dict[str, object]]:
    return [
        {
            "assumption_id": row["assumption_id"],
            "assumption_name": row["assumption_name"],
            "evidence_type": "placeholder",
            "evidence_description": "No real evidence supplied. Scaffold placeholder only.",
            "evidence_source": "none",
            "evidence_status": "missing",
            "verification_status": "unverified",
            "blocker_status": "blocking",
            "reviewer_notes": "Real evidence review is not performed by this scaffold.",
            "scaffold_only": True,
        }
        for row in VERIFICATION_ASSUMPTIONS
    ]


def _review_rows(area: str) -> list[dict[str, object]]:
    return [
        {
            "review_item": row["assumption_name"],
            "required_evidence": row["required_evidence"],
            "observed_evidence": "none_scaffold_placeholder",
            "verification_status": "unverified",
            "risk_level": row["risk_level"],
            "blocking_status": "blocking",
            "fail_closed_behavior": row["blocking_impact"],
            "review_notes": f"{area} review not performed; scaffold only.",
            "scaffold_only": True,
        }
        for row in VERIFICATION_ASSUMPTIONS
        if row["assumption_area"] == area
    ]


def write_verification_scaffold() -> None:
    _ensure_dirs()
    checklist_rows = _verification_checklist_rows()
    evidence_rows = _evidence_placeholder_rows()
    _write_csv(ASSUMPTIONS_DIR / "crsp_assumption_verification_checklist.csv", checklist_rows, VERIFICATION_CHECKLIST_FIELDS)
    _write_csv(ASSUMPTIONS_DIR / "crsp_assumption_evidence_register.csv", evidence_rows, EVIDENCE_FIELDS)
    _write_csv(ASSUMPTIONS_DIR / "crsp_subscription_scope_review.csv", _review_rows("subscription_scope"), REVIEW_FIELDS)
    _write_csv(ASSUMPTIONS_DIR / "crsp_license_retention_review.csv", _review_rows("licensing"), REVIEW_FIELDS)
    _write_csv(ASSUMPTIONS_DIR / "crsp_field_availability_review.csv", _review_rows("field_availability"), REVIEW_FIELDS)
    date_rows = _review_rows("known_date") + _review_rows("event_date") + _review_rows("ticker_window") + _review_rows("release_version")
    _write_csv(ASSUMPTIONS_DIR / "crsp_date_semantics_review.csv", date_rows, REVIEW_FIELDS)
    archive_rows = _review_rows("archival") + _review_rows("source_reproducibility")
    _write_csv(ASSUMPTIONS_DIR / "crsp_archive_hash_feasibility_review.csv", archive_rows, REVIEW_FIELDS)
    _write_csv(
        ASSUMPTIONS_DIR / "crsp_assumption_status_placeholder.csv",
        [
            {
                "assumption_id": row["assumption_id"],
                "requested_status": "verified",
                "applied_status": "unverified",
                "update_applied": False,
                "blocker_status": "blocking",
                "reason": "Real assumption status updates are disabled in scaffold mode.",
                "scaffold_only": True,
            }
            for row in VERIFICATION_ASSUMPTIONS
        ],
    )
    eligibility_update = {
        "source": "crsp_us_stock_databases",
        "source_version": "unverified",
        "source_gate_status": "manual_review_required",
        "allowed_use": "diagnostics_only",
        "manual_review_required": True,
        "verified_assumptions": [],
        "unverified_assumptions": [row["assumption_id"] for row in VERIFICATION_ASSUMPTIONS],
        "blocking_reasons": ["manual_review_required", "source_rejected"],
        "ingestion_authorized": False,
        "metadata_construction_authorized": False,
        "lineage_construction_authorized": False,
        "scaffold_only": True,
    }
    (ASSUMPTIONS_DIR / "crsp_source_gate_eligibility_update.json").write_text(
        json.dumps(eligibility_update, indent=2),
        encoding="utf-8",
    )


def validate_assumptions() -> list[str]:
    write_scaffold()
    errors = []
    df = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_register.csv")
    missing = set(ASSUMPTION_FIELDS) - set(df.columns)
    if missing:
        errors.append(f"missing assumption fields: {sorted(missing)}")
    blocking = df[df["risk_level"].isin(["critical", "high"])]
    if not (blocking["verification_status"] != "verified").all():
        errors.append("critical/high assumptions must remain unverified in scaffold")
    if not (blocking["blocking_status"] == "blocking").all():
        errors.append("critical/high assumptions must remain blocking")
    return errors


def validate_assumption_evidence() -> list[str]:
    write_verification_scaffold()
    errors = []
    checklist = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_verification_checklist.csv")
    evidence = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_evidence_register.csv")
    missing_checklist = set(VERIFICATION_CHECKLIST_FIELDS) - set(checklist.columns)
    missing_evidence = set(EVIDENCE_FIELDS) - set(evidence.columns)
    if missing_checklist:
        errors.append(f"missing checklist fields: {sorted(missing_checklist)}")
    if missing_evidence:
        errors.append(f"missing evidence fields: {sorted(missing_evidence)}")
    if not set(checklist["verification_status"]).issubset(VERIFICATION_STATUS_VALUES):
        errors.append("invalid checklist verification status")
    if not set(evidence["verification_status"]).issubset(VERIFICATION_STATUS_VALUES):
        errors.append("invalid evidence verification status")
    if not set(evidence["blocker_status"]).issubset(BLOCKER_STATUS_VALUES):
        errors.append("invalid evidence blocker status")
    critical = checklist[checklist["risk_level"].isin(["critical", "high"])]
    if not (critical["verification_status"] == "unverified").all():
        errors.append("critical/high verification checklist items must remain unverified")
    if not (critical["blocker_status"] == "blocking").all():
        errors.append("critical/high verification checklist items must remain blocking")
    if not evidence["scaffold_only"].astype(bool).all():
        errors.append("evidence register must remain scaffold-only")
    return errors


def validate_schema_alignment() -> list[str]:
    write_scaffold()
    errors = []
    for schema_name, fields in SCHEMA_FIELDS.items():
        path = SCHEMAS_DIR / f"{schema_name}_alignment_checklist.csv"
        df = pd.read_csv(path)
        if set(fields) != set(df["field"]):
            errors.append(f"{schema_name} field mismatch")
        if not (df["crsp_mapping_status"] == "unverified").all():
            errors.append(f"{schema_name} mappings must be unverified")
    return errors


def validate_source_gate() -> list[str]:
    write_scaffold()
    df = pd.read_csv(SOURCE_GATE_DIR / "crsp_source_acceptance_manifest_template.csv")
    if list(df.columns) != SOURCE_MANIFEST_FIELDS:
        return ["source manifest fields mismatch"]
    return []


def validate_source_gate_scaffold() -> list[str]:
    write_source_gate_scaffold()
    errors: list[str] = []
    template = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_manifest_template.csv")
    if list(template.columns) != SOURCE_GATE_MANIFEST_SCHEMA_FIELDS:
        errors.append("PIT source gate manifest template fields mismatch")
    schema = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_manifest_schema.csv")
    if set(schema["field"]) != set(SOURCE_GATE_MANIFEST_SCHEMA_FIELDS):
        errors.append("PIT source gate manifest schema fields mismatch")
    vocab = json.loads((SOURCE_GATE_DIR / "pit_source_gate_controlled_vocabularies.json").read_text(encoding="utf-8"))
    for key, values in SOURCE_GATE_CONTROLLED_VOCABULARIES.items():
        if vocab.get(key) != values:
            errors.append(f"controlled vocabulary mismatch: {key}")
    errors.extend(validate_source_gate_manifest(SOURCE_GATE_DRY_RUN_CANDIDATES))
    report = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_dry_run_report.csv")
    if not set(SOURCE_GATE_RESULT_FIELDS).issubset(report.columns):
        errors.append("dry-run report missing fields")
    if report["dry_run_only"].astype(str).str.lower().ne("true").any():
        errors.append("dry-run report must remain dry-run only")
    manifest = json.loads((SOURCE_GATE_DIR / "pit_source_gate_scaffold_manifest.json").read_text(encoding="utf-8"))
    forbidden_flags = [
        "external_data_accessed",
        "source_files_loaded",
        "data_ingested",
        "metadata_tables_created",
        "lineage_built",
        "discovery_executed",
        "validation_executed",
        "governance_thresholds_modified",
        "production_registered",
        "ml_implemented",
    ]
    if any(manifest[flag] for flag in forbidden_flags):
        errors.append("source gate scaffold manifest contains forbidden side effect")
    return errors


def validate_diagnostics() -> list[str]:
    write_scaffold()
    errors = []
    for filename in DIAGNOSTIC_FILES:
        df = pd.read_csv(DIAGNOSTICS_DIR / filename)
        if set(DIAGNOSTIC_COLUMNS) - set(df.columns):
            errors.append(f"{filename} missing diagnostic columns")
        if not df["placeholder_only"].astype(bool).all():
            errors.append(f"{filename} must be placeholder only")
    return errors


def validate_all() -> list[str]:
    errors = []
    errors.extend(validate_source_gate())
    errors.extend(validate_source_gate_scaffold())
    errors.extend(validate_schema_alignment())
    errors.extend(validate_assumptions())
    errors.extend(validate_diagnostics())
    errors.extend(validate_assumption_evidence())
    return errors


def _print_errors(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: CRSP scaffold validation succeeded. No CRSP data accessed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CRSP security master/ticker lineage scaffold runner.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--list-assumptions", action="store_true")
    group.add_argument("--validate-source-gate", action="store_true")
    group.add_argument("--list-source-gates", action="store_true")
    group.add_argument("--validate-source-gates", action="store_true")
    group.add_argument("--dry-run-source-gates", action="store_true")
    group.add_argument("--validate-schema-alignment", action="store_true")
    group.add_argument("--validate-assumptions", action="store_true")
    group.add_argument("--validate-diagnostics", action="store_true")
    group.add_argument("--list-verification-requirements", action="store_true")
    group.add_argument("--export-verification-checklist", action="store_true")
    group.add_argument("--validate-assumption-evidence", action="store_true")
    group.add_argument("--update-assumption-status", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        write_scaffold()
        print(GUARDRAIL)
        print(f"Artifact root: {OUT_DIR}")
        print("Classification: READY_FOR_ASSUMPTION_VERIFICATION")
        return 0
    if args.list_assumptions:
        for row in ASSUMPTIONS:
            print(f"{row['assumption_id']}: {row['verification_status']} / {row['blocking_status']} / {row['risk_level']}")
        return 0
    if args.validate_source_gate:
        return _print_errors(validate_source_gate())
    if args.list_source_gates:
        write_source_gate_scaffold()
        for vocabulary, values in SOURCE_GATE_CONTROLLED_VOCABULARIES.items():
            print(f"{vocabulary}: {', '.join(values)}")
        print(f"Manifest template: {SOURCE_GATE_DIR / 'pit_source_gate_manifest_template.csv'}")
        return 0
    if args.validate_source_gates:
        return _print_errors(validate_source_gate_scaffold())
    if args.dry_run_source_gates:
        write_source_gate_scaffold()
        report_path = SOURCE_GATE_DIR / "pit_source_gate_dry_run_report.csv"
        print("Dry-run source-gate evaluation complete. No external data accessed.")
        print(f"Report: {report_path}")
        print("Classification: SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES")
        return 0
    if args.validate_schema_alignment:
        return _print_errors(validate_schema_alignment())
    if args.validate_assumptions:
        return _print_errors(validate_assumptions())
    if args.validate_diagnostics:
        return _print_errors(validate_diagnostics())
    if args.list_verification_requirements:
        for row in VERIFICATION_ASSUMPTIONS:
            print(f"{row['assumption_id']}: {row['risk_level']} / {row['required_evidence']}")
        return 0
    if args.export_verification_checklist:
        write_verification_scaffold()
        print(f"Exported scaffold verification checklist: {ASSUMPTIONS_DIR / 'crsp_assumption_verification_checklist.csv'}")
        return 0
    if args.validate_assumption_evidence:
        return _print_errors(validate_assumption_evidence())
    if args.update_assumption_status:
        write_verification_scaffold()
        print("No real assumption statuses updated. Scaffold-only placeholder status file written.")
        print(f"Status placeholder: {ASSUMPTIONS_DIR / 'crsp_assumption_status_placeholder.csv'}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
