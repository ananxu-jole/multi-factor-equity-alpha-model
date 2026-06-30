from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


RUN_ID = "point_in_time_economic_metadata_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
SOURCE_GATE_DIR = OUT_DIR / "source_gate"
SCHEMAS_DIR = OUT_DIR / "schemas"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"
READINESS_REVIEW_DIR = OUT_DIR / "readiness_review"
MANIFESTS_DIR = OUT_DIR / "manifests"
TESTS_DIR = OUT_DIR / "tests"

SCHEMA_SPEC_PATH = Path("docs/research_notes/point_in_time_economic_metadata_implementation_specification_v1.md")

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only point-in-time economic metadata scaffold. This runner writes schema templates, "
    "placeholder diagnostics, manifests, and scaffold validation outputs only. It does not ingest "
    "metadata, select sources, reconstruct sector or industry history, reconstruct peer groups, "
    "create PIT classifications, run discovery, run refinement, run validation, mutate governance, "
    "change thresholds, register production outputs, implement ML, or create alpha candidates."
)

ARTIFACT_DIRS = (
    OUT_DIR,
    SOURCE_GATE_DIR,
    SCHEMAS_DIR,
    DIAGNOSTICS_DIR,
    READINESS_REVIEW_DIR,
    MANIFESTS_DIR,
    TESTS_DIR,
)

DELIVERABLES = [
    {
        "deliverable": "source_acceptance_manifest",
        "artifact": str(SOURCE_GATE_DIR / "source_acceptance_manifest_schema.csv"),
        "required_status": "required_before_ingestion_or_construction",
        "purpose": "records source-gate scoring and accepted/rejected/diagnostic-only status",
        "dependency": "source-gate rubric and candidate source metadata",
    },
    {
        "deliverable": "security_master_pit",
        "artifact": str(SCHEMAS_DIR / "security_master_pit_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "stores stable security identity windows for historical joins",
        "dependency": "accepted source with security identifiers or reconstructable identity fields",
    },
    {
        "deliverable": "ticker_lineage_pit",
        "artifact": str(SCHEMAS_DIR / "ticker_lineage_pit_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "maps tickers to securities over time",
        "dependency": "security_master_pit and ticker history source",
    },
    {
        "deliverable": "sector_industry_history_pit",
        "artifact": str(SCHEMAS_DIR / "sector_industry_history_pit_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "stores sector and industry classification history with PIT lineage",
        "dependency": "accepted classification source and security/ticker mapping",
    },
    {
        "deliverable": "size_bucket_history_pit",
        "artifact": str(SCHEMAS_DIR / "size_bucket_history_pit_schema.csv"),
        "required_status": "recommended_not_blocking_if_size_aware_fallback_disabled",
        "purpose": "stores date-safe size and market-cap bucket history",
        "dependency": "PIT market-cap or size source",
    },
    {
        "deliverable": "peer_group_history_pit",
        "artifact": str(SCHEMAS_DIR / "peer_group_history_pit_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "stores derived peer assignments by signal date and construction method",
        "dependency": "sector_industry_history_pit, ticker/security lineage, active universe dates",
    },
    {
        "deliverable": "metadata_source_lineage",
        "artifact": str(SCHEMAS_DIR / "metadata_source_lineage_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "stores source references, hashes, versions, timestamps, and usage notes",
        "dependency": "raw source archive or controlled source references",
    },
    {
        "deliverable": "pit_metadata_coverage_diagnostics",
        "artifact": str(SCHEMAS_DIR / "pit_metadata_coverage_diagnostics_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "stores date/window coverage, fallback, stale, and blocked/eligible diagnostics",
        "dependency": "PIT history outputs and active universe membership",
    },
    {
        "deliverable": "pit_economic_context_panel",
        "artifact": str(SCHEMAS_DIR / "pit_economic_context_panel_schema.csv"),
        "required_status": "required_mvp",
        "purpose": "research-facing date/ticker context panel with discovery eligibility flags",
        "dependency": "classification history, ticker lineage, peer reconstruction, diagnostics",
    },
    {
        "deliverable": "readiness_manifest",
        "artifact": str(MANIFESTS_DIR / "readiness_manifest_placeholder.json"),
        "required_status": "required_mvp",
        "purpose": "declares diagnostic-only, discovery-design-ready, or PIT discovery ready status",
        "dependency": "diagnostics and source manifest",
    },
]

SCHEMA_DEFINITIONS: dict[str, list[dict[str, str | bool]]] = {
    "source_acceptance_manifest": [
        {"field": "source_gate_run_id", "required": True, "category": "key", "notes": "source-gate review id"},
        {"field": "source", "required": True, "category": "key", "notes": "source name"},
        {"field": "source_type", "required": True, "category": "lineage", "notes": "vendor, snapshot, manual, diagnostic"},
        {"field": "source_version", "required": True, "category": "key", "notes": "source version or release"},
        {"field": "source_snapshot_date", "required": True, "category": "effective_date", "notes": "date source snapshot represents"},
        {"field": "source_file_hash", "required": True, "category": "lineage", "notes": "hash for local source file"},
        {"field": "pit_integrity_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "coverage_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "historical_depth_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "identifier_quality_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "update_feasibility_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "source_stability_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "implementation_complexity_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "cost_manual_burden_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "leakage_risk_score", "required": True, "category": "validation", "notes": "0-3 source-gate score"},
        {"field": "source_gate_status", "required": True, "category": "validation", "notes": "accepted, diagnostic-only, rejected, manual review"},
        {"field": "allowed_use", "required": True, "category": "validation", "notes": "allowed metadata use"},
        {"field": "rejection_reason", "required": True, "category": "validation", "notes": "required when rejected"},
        {"field": "manual_review_required", "required": True, "category": "validation", "notes": "manual review flag"},
        {"field": "license_or_usage_notes", "required": True, "category": "lineage", "notes": "research use notes"},
        {"field": "review_timestamp", "required": True, "category": "lineage", "notes": "review timestamp"},
        {"field": "reviewer_notes", "required": True, "category": "lineage", "notes": "review notes"},
    ],
    "security_master_pit": [
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "issuer_id", "required": True, "category": "lineage", "notes": "issuer id if available"},
        {"field": "company_name", "required": True, "category": "lineage", "notes": "company name"},
        {"field": "security_type", "required": True, "category": "lineage", "notes": "common stock, ADR, share class, etc."},
        {"field": "exchange", "required": True, "category": "lineage", "notes": "listing venue"},
        {"field": "country", "required": True, "category": "lineage", "notes": "country if available"},
        {"field": "currency", "required": True, "category": "lineage", "notes": "trading currency if available"},
        {"field": "is_active", "required": True, "category": "validation", "notes": "active flag for window"},
        {"field": "effective_start", "required": True, "category": "effective_date", "notes": "identity window start"},
        {"field": "effective_end", "required": True, "category": "effective_date", "notes": "identity window end"},
        {"field": "as_of_date", "required": True, "category": "effective_date", "notes": "known date"},
        {"field": "source", "required": True, "category": "lineage", "notes": "source name"},
        {"field": "source_version", "required": True, "category": "lineage", "notes": "source version"},
        {"field": "source_record_id", "required": True, "category": "lineage", "notes": "source row id"},
        {"field": "metadata_version", "required": True, "category": "lineage", "notes": "project metadata version"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "collection_timestamp", "required": True, "category": "lineage", "notes": "collection timestamp"},
        {"field": "record_hash", "required": True, "category": "lineage", "notes": "normalized record hash"},
        {"field": "identity_confidence", "required": True, "category": "confidence", "notes": "identity confidence score/status"},
        {"field": "manual_override_flag", "required": True, "category": "validation", "notes": "manual override flag"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality class"},
        {"field": "security_event_id", "required": True, "category": "lineage", "notes": "linked event id if available"},
        {"field": "event_type", "required": True, "category": "lineage", "notes": "ticker_change, merger, spin_off, delisting, etc."},
        {"field": "event_effective_date", "required": True, "category": "effective_date", "notes": "event effective date"},
        {"field": "event_as_of_date", "required": True, "category": "effective_date", "notes": "event known date"},
        {"field": "predecessor_security_id", "required": True, "category": "lineage", "notes": "predecessor id if available"},
        {"field": "successor_security_id", "required": True, "category": "lineage", "notes": "successor id if available"},
        {"field": "prior_ticker", "required": True, "category": "lineage", "notes": "prior ticker"},
        {"field": "next_ticker", "required": True, "category": "lineage", "notes": "next ticker"},
        {"field": "event_confidence", "required": True, "category": "confidence", "notes": "event confidence"},
        {"field": "notes", "required": True, "category": "lineage", "notes": "notes"},
    ],
    "ticker_lineage_pit": [
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "ticker", "required": True, "category": "key", "notes": "ticker"},
        {"field": "exchange", "required": True, "category": "key", "notes": "exchange"},
        {"field": "ticker_namespace", "required": True, "category": "key", "notes": "ticker namespace/source"},
        {"field": "share_class", "required": True, "category": "lineage", "notes": "share class"},
        {"field": "primary_listing_flag", "required": True, "category": "validation", "notes": "primary listing flag"},
        {"field": "ticker_effective_start", "required": True, "category": "effective_date", "notes": "ticker window start"},
        {"field": "ticker_effective_end", "required": True, "category": "effective_date", "notes": "ticker window end"},
        {"field": "as_of_date", "required": True, "category": "effective_date", "notes": "known date"},
        {"field": "ticker_status", "required": True, "category": "validation", "notes": "active/inactive/suspended/etc."},
        {"field": "change_reason", "required": True, "category": "lineage", "notes": "ticker change reason"},
        {"field": "prior_ticker", "required": True, "category": "lineage", "notes": "prior ticker"},
        {"field": "next_ticker", "required": True, "category": "lineage", "notes": "next ticker"},
        {"field": "source", "required": True, "category": "lineage", "notes": "source"},
        {"field": "source_version", "required": True, "category": "lineage", "notes": "source version"},
        {"field": "metadata_version", "required": True, "category": "lineage", "notes": "metadata version"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "collection_timestamp", "required": True, "category": "lineage", "notes": "collection timestamp"},
        {"field": "record_hash", "required": True, "category": "lineage", "notes": "record hash"},
        {"field": "ticker_mapping_confidence", "required": True, "category": "confidence", "notes": "mapping confidence"},
        {"field": "manual_override_flag", "required": True, "category": "validation", "notes": "manual override flag"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
    ],
    "sector_industry_history_pit": [
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "ticker_at_source", "required": True, "category": "lineage", "notes": "source ticker"},
        {"field": "sector", "required": True, "category": "lineage", "notes": "sector"},
        {"field": "industry", "required": True, "category": "lineage", "notes": "industry"},
        {"field": "subindustry", "required": True, "category": "lineage", "notes": "subindustry if available"},
        {"field": "classification_system", "required": True, "category": "lineage", "notes": "classification system"},
        {"field": "classification_level", "required": True, "category": "lineage", "notes": "classification level"},
        {"field": "taxonomy_version", "required": True, "category": "lineage", "notes": "taxonomy version if available"},
        {"field": "classification_provider_taxonomy_id", "required": True, "category": "lineage", "notes": "provider taxonomy id"},
        {"field": "taxonomy_effective_date", "required": True, "category": "effective_date", "notes": "taxonomy effective date"},
        {"field": "taxonomy_change_flag", "required": True, "category": "validation", "notes": "taxonomy change flag"},
        {"field": "taxonomy_change_reason", "required": True, "category": "lineage", "notes": "taxonomy change reason"},
        {"field": "effective_start", "required": True, "category": "effective_date", "notes": "classification start"},
        {"field": "effective_end", "required": True, "category": "effective_date", "notes": "classification end"},
        {"field": "as_of_date", "required": True, "category": "effective_date", "notes": "known date"},
        {"field": "source_snapshot_date", "required": True, "category": "effective_date", "notes": "source snapshot date"},
        {"field": "source", "required": True, "category": "lineage", "notes": "source"},
        {"field": "source_version", "required": True, "category": "lineage", "notes": "source version"},
        {"field": "source_record_id", "required": True, "category": "lineage", "notes": "source row id"},
        {"field": "metadata_version", "required": True, "category": "lineage", "notes": "metadata version"},
        {"field": "universe_version", "required": True, "category": "lineage", "notes": "universe version"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "collection_timestamp", "required": True, "category": "lineage", "notes": "collection timestamp"},
        {"field": "record_hash", "required": True, "category": "lineage", "notes": "record hash"},
        {"field": "raw_record_hash", "required": True, "category": "lineage", "notes": "raw record hash"},
        {"field": "classification_confidence", "required": True, "category": "confidence", "notes": "classification confidence"},
        {"field": "manual_override_flag", "required": True, "category": "validation", "notes": "manual override flag"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "stale_metadata_flag", "required": True, "category": "validation", "notes": "stale metadata flag"},
        {"field": "notes", "required": True, "category": "lineage", "notes": "notes"},
    ],
    "size_bucket_history_pit": [
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "ticker_at_source", "required": True, "category": "lineage", "notes": "source ticker"},
        {"field": "market_cap", "required": True, "category": "lineage", "notes": "market cap"},
        {"field": "market_cap_currency", "required": True, "category": "lineage", "notes": "currency"},
        {"field": "market_cap_as_of_date", "required": True, "category": "effective_date", "notes": "market cap as-of date"},
        {"field": "market_cap_source", "required": True, "category": "lineage", "notes": "market cap source"},
        {"field": "size_bucket", "required": True, "category": "lineage", "notes": "size bucket if implemented"},
        {"field": "market_cap_bucket", "required": True, "category": "lineage", "notes": "market cap bucket"},
        {"field": "effective_start", "required": True, "category": "effective_date", "notes": "bucket start"},
        {"field": "effective_end", "required": True, "category": "effective_date", "notes": "bucket end"},
        {"field": "as_of_date", "required": True, "category": "effective_date", "notes": "known date"},
        {"field": "source", "required": True, "category": "lineage", "notes": "source"},
        {"field": "source_version", "required": True, "category": "lineage", "notes": "source version"},
        {"field": "metadata_version", "required": True, "category": "lineage", "notes": "metadata version"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "collection_timestamp", "required": True, "category": "lineage", "notes": "collection timestamp"},
        {"field": "record_hash", "required": True, "category": "lineage", "notes": "record hash"},
        {"field": "size_confidence", "required": True, "category": "confidence", "notes": "size confidence"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "stale_metadata_flag", "required": True, "category": "validation", "notes": "stale flag"},
        {"field": "manual_override_flag", "required": True, "category": "validation", "notes": "manual override flag"},
    ],
    "peer_group_history_pit": [
        {"field": "signal_date", "required": True, "category": "key", "notes": "signal date"},
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "ticker", "required": True, "category": "lineage", "notes": "ticker"},
        {"field": "sector", "required": True, "category": "lineage", "notes": "sector on signal date"},
        {"field": "industry", "required": True, "category": "lineage", "notes": "industry on signal date"},
        {"field": "size_bucket", "required": True, "category": "lineage", "notes": "date-safe size bucket if available"},
        {"field": "peer_group_label", "required": True, "category": "lineage", "notes": "peer group label"},
        {"field": "peer_group_level", "required": True, "category": "validation", "notes": "industry/sector/etc."},
        {"field": "peer_group_method", "required": True, "category": "validation", "notes": "construction method"},
        {"field": "peer_group_size", "required": True, "category": "validation", "notes": "active group size"},
        {"field": "peer_group_min_size", "required": True, "category": "validation", "notes": "minimum group size"},
        {"field": "fallback_level", "required": True, "category": "validation", "notes": "fallback level"},
        {"field": "fallback_reason", "required": True, "category": "validation", "notes": "fallback reason"},
        {"field": "blocked_for_peer_relative", "required": True, "category": "validation", "notes": "blocked flag"},
        {"field": "blocked_reason", "required": True, "category": "validation", "notes": "blocked reason"},
        {"field": "input_classification_version", "required": True, "category": "lineage", "notes": "input classification version"},
        {"field": "input_universe_version", "required": True, "category": "lineage", "notes": "input universe version"},
        {"field": "construction_rule_version", "required": True, "category": "lineage", "notes": "rule version"},
        {"field": "source_metadata_version", "required": True, "category": "lineage", "notes": "source metadata version"},
        {"field": "metadata_version", "required": True, "category": "key", "notes": "metadata version"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "created_at", "required": True, "category": "lineage", "notes": "created timestamp"},
        {"field": "peer_confidence_score", "required": True, "category": "confidence", "notes": "peer confidence"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "fallback_quality_status", "required": True, "category": "confidence", "notes": "fallback quality"},
    ],
    "metadata_source_lineage": [
        {"field": "source_lineage_id", "required": True, "category": "key", "notes": "lineage id"},
        {"field": "run_id", "required": True, "category": "lineage", "notes": "runner id"},
        {"field": "metadata_version", "required": True, "category": "lineage", "notes": "metadata version"},
        {"field": "source", "required": True, "category": "lineage", "notes": "source"},
        {"field": "source_type", "required": True, "category": "lineage", "notes": "source type"},
        {"field": "source_version", "required": True, "category": "lineage", "notes": "source version"},
        {"field": "source_snapshot_date", "required": True, "category": "effective_date", "notes": "snapshot date"},
        {"field": "source_file_path", "required": True, "category": "lineage", "notes": "source file path"},
        {"field": "source_url_or_reference", "required": True, "category": "lineage", "notes": "source reference"},
        {"field": "source_file_hash", "required": True, "category": "lineage", "notes": "source hash"},
        {"field": "record_count_raw", "required": True, "category": "validation", "notes": "raw count"},
        {"field": "record_count_clean", "required": True, "category": "validation", "notes": "clean count"},
        {"field": "collection_timestamp", "required": True, "category": "lineage", "notes": "collection timestamp"},
        {"field": "license_or_usage_notes", "required": True, "category": "lineage", "notes": "license notes"},
        {"field": "normalization_rules", "required": True, "category": "lineage", "notes": "normalization rules"},
        {"field": "created_by", "required": True, "category": "lineage", "notes": "created by"},
        {"field": "source_confidence", "required": True, "category": "confidence", "notes": "source confidence"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "manual_source_flag", "required": True, "category": "validation", "notes": "manual source flag"},
        {"field": "source_gate_score_summary", "required": True, "category": "validation", "notes": "source gate score summary"},
        {"field": "notes", "required": True, "category": "lineage", "notes": "notes"},
    ],
    "pit_metadata_coverage_diagnostics": [
        {"field": "run_id", "required": True, "category": "key", "notes": "runner id"},
        {"field": "metadata_version", "required": True, "category": "key", "notes": "metadata version"},
        {"field": "universe_version", "required": True, "category": "lineage", "notes": "universe version"},
        {"field": "diagnostic_scope", "required": True, "category": "key", "notes": "diagnostic scope"},
        {"field": "diagnostic_start_date", "required": True, "category": "key", "notes": "start date"},
        {"field": "diagnostic_end_date", "required": True, "category": "key", "notes": "end date"},
        {"field": "total_active_tickers", "required": True, "category": "validation", "notes": "active tickers"},
        {"field": "covered_active_tickers", "required": True, "category": "validation", "notes": "covered active tickers"},
        {"field": "missing_active_tickers", "required": True, "category": "validation", "notes": "missing active tickers"},
        {"field": "coverage_ratio", "required": True, "category": "validation", "notes": "coverage ratio"},
        {"field": "sector_count", "required": True, "category": "validation", "notes": "sector count"},
        {"field": "industry_count", "required": True, "category": "validation", "notes": "industry count"},
        {"field": "peer_group_count", "required": True, "category": "validation", "notes": "peer group count"},
        {"field": "thin_peer_group_count", "required": True, "category": "validation", "notes": "thin group count"},
        {"field": "fallback_usage_rate", "required": True, "category": "validation", "notes": "fallback usage rate"},
        {"field": "broad_fallback_usage_rate", "required": True, "category": "validation", "notes": "broad fallback usage rate"},
        {"field": "fallback_dominance_flag", "required": True, "category": "validation", "notes": "fallback dominance flag"},
        {"field": "stale_record_count", "required": True, "category": "validation", "notes": "stale record count"},
        {"field": "stale_record_share", "required": True, "category": "validation", "notes": "stale record share"},
        {"field": "stale_age_min", "required": True, "category": "validation", "notes": "stale age min"},
        {"field": "stale_age_median", "required": True, "category": "validation", "notes": "stale age median"},
        {"field": "stale_age_p75", "required": True, "category": "validation", "notes": "stale age p75"},
        {"field": "stale_age_p90", "required": True, "category": "validation", "notes": "stale age p90"},
        {"field": "stale_age_max", "required": True, "category": "validation", "notes": "stale age max"},
        {"field": "unresolved_ticker_count", "required": True, "category": "validation", "notes": "unresolved ticker count"},
        {"field": "duplicate_active_record_count", "required": True, "category": "validation", "notes": "duplicate active record count"},
        {"field": "eligible_ticker_date_count", "required": True, "category": "validation", "notes": "eligible ticker-date count"},
        {"field": "blocked_ticker_date_count", "required": True, "category": "validation", "notes": "blocked ticker-date count"},
        {"field": "eligible_ticker_date_share", "required": True, "category": "validation", "notes": "eligible ticker-date share"},
        {"field": "blocked_ticker_date_share", "required": True, "category": "validation", "notes": "blocked ticker-date share"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "coverage_quality_status", "required": True, "category": "confidence", "notes": "coverage quality status"},
        {"field": "created_at", "required": True, "category": "lineage", "notes": "created timestamp"},
        {"field": "notes", "required": True, "category": "lineage", "notes": "notes"},
    ],
    "pit_economic_context_panel": [
        {"field": "signal_date", "required": True, "category": "key", "notes": "signal date"},
        {"field": "security_id", "required": True, "category": "key", "notes": "stable security id"},
        {"field": "ticker", "required": True, "category": "key", "notes": "ticker"},
        {"field": "sector", "required": True, "category": "lineage", "notes": "PIT sector"},
        {"field": "industry", "required": True, "category": "lineage", "notes": "PIT industry"},
        {"field": "subindustry", "required": True, "category": "lineage", "notes": "PIT subindustry if available"},
        {"field": "size_bucket", "required": True, "category": "lineage", "notes": "PIT size bucket if available"},
        {"field": "peer_group_label", "required": True, "category": "lineage", "notes": "peer group label"},
        {"field": "peer_group_level", "required": True, "category": "validation", "notes": "peer group level"},
        {"field": "peer_group_method", "required": True, "category": "validation", "notes": "peer group method"},
        {"field": "peer_group_size", "required": True, "category": "validation", "notes": "peer group size"},
        {"field": "peer_group_min_size", "required": True, "category": "validation", "notes": "minimum peer group size"},
        {"field": "fallback_level", "required": True, "category": "validation", "notes": "fallback level"},
        {"field": "fallback_reason", "required": True, "category": "validation", "notes": "fallback reason"},
        {"field": "peer_confidence_score", "required": True, "category": "confidence", "notes": "peer confidence score"},
        {"field": "point_in_time_quality", "required": True, "category": "validation", "notes": "PIT quality"},
        {"field": "classification_metadata_version", "required": True, "category": "lineage", "notes": "classification version"},
        {"field": "peer_group_metadata_version", "required": True, "category": "lineage", "notes": "peer group version"},
        {"field": "source_gate_run_id", "required": True, "category": "lineage", "notes": "source gate run id"},
        {"field": "stale_age_days", "required": True, "category": "validation", "notes": "stale age"},
        {"field": "stale_record_flag", "required": True, "category": "validation", "notes": "stale flag"},
        {"field": "discovery_eligible", "required": True, "category": "validation", "notes": "fail-closed eligibility flag"},
        {"field": "blocked_reason", "required": True, "category": "validation", "notes": "blocked reason"},
        {"field": "metadata_version", "required": True, "category": "key", "notes": "metadata version"},
        {"field": "created_at", "required": True, "category": "lineage", "notes": "created timestamp"},
    ],
}

DIAGNOSTIC_PLACEHOLDERS = {
    "coverage_placeholder.csv": [
        "diagnostic_scope",
        "diagnostic_start_date",
        "diagnostic_end_date",
        "total_active_tickers",
        "covered_active_tickers",
        "missing_active_tickers",
        "coverage_ratio",
        "placeholder_only",
    ],
    "fallback_placeholder.csv": [
        "diagnostic_start_date",
        "diagnostic_end_date",
        "fallback_level",
        "ticker_date_count",
        "ticker_date_share",
        "broad_fallback_share",
        "fallback_dominance_flag",
        "placeholder_only",
    ],
    "stale_age_placeholder.csv": [
        "diagnostic_start_date",
        "diagnostic_end_date",
        "stale_age_min",
        "stale_age_median",
        "stale_age_p75",
        "stale_age_p90",
        "stale_age_max",
        "placeholder_only",
    ],
    "lineage_placeholder.csv": [
        "lineage_check",
        "source",
        "source_version",
        "source_file_hash",
        "record_count_raw",
        "record_count_clean",
        "placeholder_only",
    ],
    "blocked_eligible_placeholder.csv": [
        "diagnostic_start_date",
        "diagnostic_end_date",
        "total_ticker_dates",
        "eligible_ticker_dates",
        "blocked_ticker_dates",
        "blocked_reason",
        "placeholder_only",
    ],
}

VALIDATION_SCAFFOLD_CHECKS = [
    ("required_fields", "schema_only", "required fields are declared in schema templates"),
    ("schema_requiredness_alignment", "schema_only", "all declared schema fields are required per frozen specification"),
    ("effective_date_requirements", "schema_only", "effective-date fields are declared where required"),
    ("lineage_requirements", "schema_only", "lineage fields are declared in every schema template"),
    ("taxonomy_version_requirements", "schema_only", "taxonomy fields are declared in sector_industry_history_pit"),
    ("stale_record_diagnostics", "placeholder_only", "stale-age diagnostic placeholder exists"),
    ("fallback_diagnostics", "placeholder_only", "fallback diagnostic placeholder exists"),
    ("blocked_eligible_diagnostics", "placeholder_only", "blocked/eligible diagnostic placeholder exists"),
    ("no_ingestion", "pass", "runner has no ingestion mode"),
    ("no_discovery", "pass", "runner has no discovery mode"),
    ("no_validation", "pass", "runner has no alpha validation mode"),
]

CONTROLLED_VOCABULARIES = {
    "source_status_values": [
        {"value": "accepted", "blocking": False, "notes": "Accepted for declared research-only PIT source-gate use."},
        {"value": "conditional", "blocking": "partial", "notes": "Allowed only for declared subset/domain/date range."},
        {"value": "manual_review_required", "blocking": True, "notes": "Blocks lineage construction until review closes."},
        {"value": "diagnostic_only", "blocking": True, "notes": "Diagnostic reports only; no PIT construction."},
        {"value": "rejected", "blocking": True, "notes": "Rejected source; audit record only."},
        {"value": "deprecated", "blocking": True, "notes": "No new builds from this source version."},
    ],
    "pit_quality_classes": [
        {"value": "point_in_time_verified", "blocking": False, "notes": "Dated, accepted, reproducible, sufficient confidence."},
        {"value": "date_stamped_snapshot", "blocking": "conditional", "notes": "Eligible only if stale and inference policies pass."},
        {"value": "inferred_window", "blocking": "conditional", "notes": "Eligible only with confidence penalty and lineage support."},
        {"value": "static_snapshot_only", "blocking": True, "notes": "Always blocks historical PIT use."},
        {"value": "unresolved", "blocking": True, "notes": "Insufficient evidence for identity/date/source continuity."},
        {"value": "blocked", "blocking": True, "notes": "Explicitly excluded by validation or policy."},
    ],
    "confidence_tiers": [
        {"value": "high", "min_score": 0.90, "max_score": 1.00, "blocking": False},
        {"value": "medium", "min_score": 0.70, "max_score": 0.8999, "blocking": False},
        {"value": "low", "min_score": 0.50, "max_score": 0.6999, "blocking": True},
        {"value": "blocked", "min_score": 0.00, "max_score": 0.4999, "blocking": True},
        {"value": "unknown", "min_score": None, "max_score": None, "blocking": True},
    ],
    "security_event_types": [
        "ticker_change",
        "name_change",
        "exchange_change",
        "delisting",
        "merger",
        "acquisition",
        "spin_off",
        "split_off",
        "relisting",
        "ticker_reuse",
        "unknown_event",
    ],
    "blocked_reason_codes": [
        {"value": "missing_effective_date", "severity": "critical"},
        {"value": "missing_as_of_date", "severity": "critical"},
        {"value": "future_dated_record", "severity": "critical"},
        {"value": "overlapping_ticker_window", "severity": "critical"},
        {"value": "duplicate_active_mapping", "severity": "critical"},
        {"value": "unresolved_security_identity", "severity": "critical"},
        {"value": "recycled_ticker_ambiguity", "severity": "critical"},
        {"value": "low_confidence_lineage", "severity": "high"},
        {"value": "stale_record", "severity": "high"},
        {"value": "source_rejected", "severity": "critical"},
        {"value": "manual_review_required", "severity": "high"},
        {"value": "static_snapshot_only", "severity": "critical"},
        {"value": "unresolved_event_lineage", "severity": "high"},
        {"value": "manual_override_dominance", "severity": "medium_high"},
        {"value": "unsupported_domain", "severity": "high"},
    ],
    "inferred_window_policy": {
        "allowed_when": [
            "repeatable_dated_snapshots_exist",
            "adjacent_snapshots_support_window",
            "source_lineage_recorded",
            "no_conflicting_identity_or_ticker_evidence",
            "confidence_after_penalty_at_least_0_70",
        ],
        "blocked_when": [
            "uses_static_current_metadata",
            "snapshot_cadence_unknown_or_unreproducible",
            "stale_span_exceeds_blocking_threshold",
            "crosses_event_boundary_without_lineage",
            "confidence_after_penalty_below_0_70",
        ],
        "minimum_confidence_penalty": 0.10,
        "sparse_snapshot_confidence_penalty": 0.20,
    },
    "stale_age_policy": {
        "fresh_max_days": 365,
        "warning_min_days": 366,
        "warning_max_days": 730,
        "high_stale_min_days": 731,
        "high_stale_max_days": 1095,
        "blocking_min_days": 1096,
        "warning_confidence_penalty": 0.05,
        "high_stale_confidence_penalty": 0.10,
    },
    "manual_override_policy": {
        "warning_dominance_share": 0.05,
        "blocking_dominance_share": 0.10,
        "allowed_uses": [
            "correct_identity_break_with_dated_evidence",
            "resolve_ticker_reuse_with_dated_reference",
            "link_predecessor_successor_security_ids",
            "close_or_open_effective_window_from_dated_evidence",
        ],
        "prohibited_uses": [
            "improve_alpha_results",
            "fill_sector_industry_size_or_peer_labels",
            "backfill_current_identity_without_dated_evidence",
            "bypass_rejected_source_status",
        ],
    },
}

SOURCE_ACCEPTANCE_MANIFEST_FIELDS = [row["field"] for row in SCHEMA_DEFINITIONS["source_acceptance_manifest"]]
SOURCE_GATE_TEMPLATE_PATH = SOURCE_GATE_DIR / "source_acceptance_manifest_template.csv"
SOURCE_GATE_SCHEMA_PATH = SOURCE_GATE_DIR / "source_acceptance_manifest_schema.json"
SOURCE_GATE_VOCAB_PATH = SOURCE_GATE_DIR / "controlled_vocabularies.json"
SOURCE_GATE_REPORT_PATH = SOURCE_GATE_DIR / "source_gate_validation_report.csv"
SOURCE_GATE_MANIFEST_PATH = SOURCE_GATE_DIR / "source_gate_manifest.json"
SOURCE_GATE_ALLOWED_USE_MAPPING_PATH = SOURCE_GATE_DIR / "allowed_use_mapping.csv"
SOURCE_GATE_TRANSITIONS_PATH = SOURCE_GATE_DIR / "source_status_transition_rules.csv"
SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH = SOURCE_GATE_DIR / "conditional_scope_template.csv"
SOURCE_GATE_CONDITIONAL_SCOPE_SCHEMA_PATH = SOURCE_GATE_DIR / "conditional_scope_schema.json"
SOURCE_GATE_SEMANTIC_REPORT_PATH = SOURCE_GATE_DIR / "semantic_validation_report.csv"
SOURCE_GATE_SEMANTIC_MANIFEST_PATH = SOURCE_GATE_DIR / "semantic_validation_manifest.json"

CANONICAL_ALLOWED_USE_CATEGORIES = {
    "diagnostics_only": {
        "description": "Source may be inspected and scored but cannot feed construction.",
        "permits_construction": False,
        "permits_reconstruction": False,
        "permits_discovery": False,
    },
    "lineage_only": {
        "description": "Source may support security master or ticker lineage construction if all semantic checks pass.",
        "permits_construction": True,
        "permits_reconstruction": False,
        "permits_discovery": False,
    },
    "reconstruction_allowed": {
        "description": "Source may support later reconstruction layers after separate readiness approval.",
        "permits_construction": False,
        "permits_reconstruction": True,
        "permits_discovery": False,
    },
    "discovery_allowed": {
        "description": "Source may support research discovery after PIT readiness approval.",
        "permits_construction": False,
        "permits_reconstruction": False,
        "permits_discovery": True,
    },
    "research_only": {
        "description": "Umbrella research label requiring a narrower category before eligibility.",
        "permits_construction": False,
        "permits_reconstruction": False,
        "permits_discovery": False,
    },
    "blocked": {
        "description": "Source retained only for audit or historical reference.",
        "permits_construction": False,
        "permits_reconstruction": False,
        "permits_discovery": False,
    },
}

ALLOWED_USE_MAPPING = {
    "identity_ticker_lineage": "lineage_only",
    "diagnostic_only": "diagnostics_only",
    "rejected": "blocked",
    "manual_review_only": "diagnostics_only",
    "deprecated_no_new_builds": "blocked",
    "diagnostics_only": "diagnostics_only",
    "lineage_only": "lineage_only",
    "reconstruction_allowed": "reconstruction_allowed",
    "discovery_allowed": "discovery_allowed",
    "research_only": "research_only",
    "blocked": "blocked",
}

CONDITIONAL_SCOPE_FIELDS = [
    "conditional_scope_id",
    "source_gate_run_id",
    "source",
    "source_version",
    "source_snapshot_date",
    "status",
    "permitted_uses",
    "prohibited_uses",
    "permitted_domains",
    "prohibited_domains",
    "effective_start",
    "effective_end",
    "supported_universe",
    "unsupported_universe",
    "required_confidence_floor",
    "required_review_flags",
    "expiration_or_review_date",
    "rationale",
    "blocked_reason_if_violated",
    "review_timestamp",
    "reviewer_notes",
]

CONDITIONAL_SCOPE_STATUS_VALUES = {"active", "expired", "superseded", "revoked"}
CONDITIONAL_SCOPE_DOMAIN_VALUES = {
    "security_identity",
    "ticker_lineage",
    "exchange_history",
    "name_history",
    "diagnostics",
    "sector_history",
    "industry_history",
    "peer_reconstruction",
    "discovery_support",
    "production",
}

LEGAL_SOURCE_STATUS_TRANSITIONS = {
    ("manual_review_required", "accepted"),
    ("manual_review_required", "conditional"),
    ("manual_review_required", "rejected"),
    ("conditional", "accepted"),
    ("conditional", "rejected"),
    ("accepted", "conditional"),
    ("accepted", "deprecated"),
    ("accepted", "manual_review_required"),
    ("deprecated", "accepted"),
    ("rejected", "manual_review_required"),
    ("rejected", "accepted"),
    ("diagnostic_only", "manual_review_required"),
    ("diagnostic_only", "rejected"),
    ("diagnostic_only", "conditional"),
    ("diagnostic_only", "accepted"),
    ("accepted", "diagnostic_only"),
    ("conditional", "diagnostic_only"),
    ("manual_review_required", "diagnostic_only"),
    ("deprecated", "diagnostic_only"),
}

SEMANTIC_DIAGNOSTIC_OUTPUTS = {
    "accepted_source_inventory.csv": ["source", "source_version", "canonical_allowed_use", "eligibility_decision", "placeholder_only"],
    "conditional_source_inventory.csv": ["source", "source_version", "conditional_scope_id", "status", "placeholder_only"],
    "rejected_source_inventory.csv": ["source", "source_version", "rejection_reason", "placeholder_only"],
    "manual_review_queue.csv": ["source", "source_version", "review_trigger", "review_timestamp", "placeholder_only"],
    "source_status_transition_history.csv": ["source", "source_version", "prior_status", "new_status", "transition_valid", "placeholder_only"],
    "semantic_eligibility_decisions.csv": ["source", "source_version", "requested_use", "requested_domain", "eligibility_decision", "blocked_reason", "placeholder_only"],
    "allowed_use_violations.csv": ["source", "source_version", "raw_allowed_use", "canonical_allowed_use", "violation", "placeholder_only"],
    "conditional_scope_violations.csv": ["source", "source_version", "conditional_scope_id", "violation", "blocked_reason", "placeholder_only"],
}


def artifact_dirs() -> tuple[Path, ...]:
    return ARTIFACT_DIRS


def deliverable_inventory() -> pd.DataFrame:
    return pd.DataFrame(DELIVERABLES)


def schema_definitions() -> dict[str, pd.DataFrame]:
    return {name: pd.DataFrame(rows) for name, rows in SCHEMA_DEFINITIONS.items()}


def _values_for(vocab_name: str) -> set[str]:
    values = CONTROLLED_VOCABULARIES[vocab_name]
    if values and isinstance(values[0], dict):
        return {str(row["value"]) for row in values}
    return {str(value) for value in values}


def _ensure_dirs() -> None:
    for path in artifact_dirs():
        path.mkdir(parents=True, exist_ok=True)


def _write_schema_templates() -> None:
    for name, df in schema_definitions().items():
        target_dir = SOURCE_GATE_DIR if name == "source_acceptance_manifest" else SCHEMAS_DIR
        df.to_csv(target_dir / f"{name}_schema.csv", index=False)

    pd.DataFrame(
        [
            {"schema": name, "field_count": len(rows), "required_field_count": sum(bool(row["required"]) for row in rows)}
            for name, rows in SCHEMA_DEFINITIONS.items()
        ]
    ).to_csv(SCHEMAS_DIR / "schema_inventory.csv", index=False)


def _source_acceptance_manifest_schema() -> dict[str, object]:
    return {
        "schema_name": "source_acceptance_manifest",
        "required_fields": SOURCE_ACCEPTANCE_MANIFEST_FIELDS,
        "allowed_values": {
            "source_gate_status": sorted(_values_for("source_status_values")),
            "allowed_use": [
                "identity_ticker_lineage",
                "diagnostic_only",
                "rejected",
                "manual_review_only",
                "deprecated_no_new_builds",
            ],
            "manual_review_required": ["True", "False", True, False],
            "point_in_time_quality": sorted(_values_for("pit_quality_classes")),
            "confidence_tier": sorted(_values_for("confidence_tiers")),
            "event_type": sorted(_values_for("security_event_types")),
            "blocked_reason": sorted(_values_for("blocked_reason_codes")),
        },
        "score_fields": [
            "pit_integrity_score",
            "coverage_score",
            "historical_depth_score",
            "identifier_quality_score",
            "update_feasibility_score",
            "source_stability_score",
            "implementation_complexity_score",
            "cost_manual_burden_score",
            "leakage_risk_score",
        ],
        "score_range": [0, 3],
        "scaffold_only": True,
        "real_sources_loaded": False,
        "metadata_ingested": False,
    }


def _conditional_scope_schema() -> dict[str, object]:
    return {
        "schema_name": "conditional_scope",
        "required_fields": CONDITIONAL_SCOPE_FIELDS,
        "allowed_values": {
            "status": sorted(CONDITIONAL_SCOPE_STATUS_VALUES),
            "permitted_uses": sorted(CANONICAL_ALLOWED_USE_CATEGORIES),
            "prohibited_uses": sorted(CANONICAL_ALLOWED_USE_CATEGORIES),
            "permitted_domains": sorted(CONDITIONAL_SCOPE_DOMAIN_VALUES),
            "prohibited_domains": sorted(CONDITIONAL_SCOPE_DOMAIN_VALUES),
            "blocked_reason_if_violated": sorted(_values_for("blocked_reason_codes")),
        },
        "scaffold_only": True,
        "real_sources_loaded": False,
        "metadata_ingested": False,
    }


def _allowed_use_mapping_rows() -> list[dict[str, object]]:
    rows = []
    for raw_value, canonical_value in sorted(ALLOWED_USE_MAPPING.items()):
        category = CANONICAL_ALLOWED_USE_CATEGORIES[canonical_value]
        rows.append(
            {
                "raw_allowed_use": raw_value,
                "canonical_allowed_use": canonical_value,
                "permits_construction": category["permits_construction"],
                "permits_reconstruction": category["permits_reconstruction"],
                "permits_discovery": category["permits_discovery"],
                "description": category["description"],
            }
        )
    return rows


def _source_status_transition_rows() -> list[dict[str, object]]:
    rows = []
    for prior_status, new_status in sorted(LEGAL_SOURCE_STATUS_TRANSITIONS):
        rows.append(
            {
                "prior_status": prior_status,
                "new_status": new_status,
                "transition_valid": True,
                "requires_review": True,
                "scaffold_only": True,
            }
        )
    return rows


def _write_semantic_scaffold() -> None:
    pd.DataFrame(_allowed_use_mapping_rows()).to_csv(SOURCE_GATE_ALLOWED_USE_MAPPING_PATH, index=False)
    pd.DataFrame(_source_status_transition_rows()).to_csv(SOURCE_GATE_TRANSITIONS_PATH, index=False)
    pd.DataFrame(columns=CONDITIONAL_SCOPE_FIELDS).to_csv(
        SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH,
        index=False,
    )
    SOURCE_GATE_CONDITIONAL_SCOPE_SCHEMA_PATH.write_text(
        json.dumps(_conditional_scope_schema(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    for filename, columns in SEMANTIC_DIAGNOSTIC_OUTPUTS.items():
        pd.DataFrame(columns=columns).to_csv(SOURCE_GATE_DIR / filename, index=False)
    report = validate_semantic_rules()
    pd.DataFrame(
        [{"check": check, "status": "pass", "detail": detail} for check, detail in report]
    ).to_csv(SOURCE_GATE_SEMANTIC_REPORT_PATH, index=False)
    SOURCE_GATE_SEMANTIC_MANIFEST_PATH.write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "semantic_validation_scaffold_only": True,
                "canonical_allowed_use_mapping_written": True,
                "conditional_scope_template_written": True,
                "conditional_scope_schema_written": True,
                "source_status_transition_rules_written": True,
                "semantic_diagnostic_placeholders_written": True,
                "real_sources_loaded": False,
                "metadata_ingested": False,
                "source_accepted": False,
                "metadata_constructed": False,
                "lineage_constructed": False,
                "sector_history_reconstructed": False,
                "industry_history_reconstructed": False,
                "peer_groups_reconstructed": False,
                "discovery_executed": False,
                "validation_executed": False,
                "governance_modified": False,
                "thresholds_modified": False,
                "production_registration": False,
                "ml_integration": False,
                "alpha_candidates_created": False,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _write_source_gate_scaffold() -> None:
    SOURCE_GATE_VOCAB_PATH.write_text(
        json.dumps(CONTROLLED_VOCABULARIES, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    pd.DataFrame(columns=SOURCE_ACCEPTANCE_MANIFEST_FIELDS).to_csv(SOURCE_GATE_TEMPLATE_PATH, index=False)
    SOURCE_GATE_SCHEMA_PATH.write_text(
        json.dumps(_source_acceptance_manifest_schema(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    report = validate_source_manifest(SOURCE_GATE_TEMPLATE_PATH)
    pd.DataFrame(
        [{"check": check, "status": "pass", "detail": detail} for check, detail in report]
    ).to_csv(SOURCE_GATE_REPORT_PATH, index=False)
    SOURCE_GATE_MANIFEST_PATH.write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_gate_scaffold_only": True,
                "controlled_vocabularies_written": True,
                "source_acceptance_manifest_template_written": True,
                "source_acceptance_manifest_schema_written": True,
                "real_sources_loaded": False,
                "metadata_ingested": False,
                "lineage_constructed": False,
                "sector_history_reconstructed": False,
                "industry_history_reconstructed": False,
                "peer_groups_reconstructed": False,
                "discovery_executed": False,
                "validation_executed": False,
                "governance_modified": False,
                "thresholds_modified": False,
                "production_registration": False,
                "ml_integration": False,
                "alpha_candidates_created": False,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _write_manifests() -> None:
    deliverable_inventory().to_csv(MANIFESTS_DIR / "deliverable_inventory.csv", index=False)
    deliverable_inventory().to_csv(OUT_DIR / "deliverable_inventory.csv", index=False)

    readiness_rows = [
        {
            "gate": "implementation_start",
            "required_state": "source gate and schema scaffold finalized",
            "current_scaffold_status": "placeholder_ready",
            "authorizes_discovery": False,
        },
        {
            "gate": "implementation_complete",
            "required_state": "schemas/artifacts created under research paths",
            "current_scaffold_status": "not_started",
            "authorizes_discovery": False,
        },
        {
            "gate": "diagnostic_ready",
            "required_state": "date-level diagnostics produced from accepted PIT source",
            "current_scaffold_status": "placeholder_only",
            "authorizes_discovery": False,
        },
        {
            "gate": "discovery_design_ready",
            "required_state": "post-implementation diagnostics reviewed",
            "current_scaffold_status": "blocked",
            "authorizes_discovery": False,
        },
        {
            "gate": "point_in_time_discovery_ready",
            "required_state": "readiness audit certifies PIT quality",
            "current_scaffold_status": "blocked",
            "authorizes_discovery": False,
        },
    ]
    pd.DataFrame(readiness_rows).to_csv(MANIFESTS_DIR / "readiness_gate_inventory.csv", index=False)
    pd.DataFrame(readiness_rows).to_csv(OUT_DIR / "readiness_gate_inventory.csv", index=False)

    scaffold_manifest = {
        "run_id": RUN_ID,
        "research_only": True,
        "scaffold_only": True,
        "schema_templates_written": True,
        "placeholder_outputs_only": True,
        "metadata_ingested": False,
        "source_selected": False,
        "sector_history_reconstructed": False,
        "industry_history_reconstructed": False,
        "peer_groups_reconstructed": False,
        "pit_classifications_created": False,
        "discovery_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "thresholds_modified": False,
        "production_registration": False,
        "ml_integration": False,
        "alpha_candidates_created": False,
        "candidate_promotion_or_demotion": False,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "specification_path": str(SCHEMA_SPEC_PATH),
        "artifact_directories": {path.name: str(path) for path in ARTIFACT_DIRS if path != OUT_DIR},
        "deliverable_count": len(DELIVERABLES),
        "schema_count": len(SCHEMA_DEFINITIONS),
    }
    (MANIFESTS_DIR / "scaffold_manifest.json").write_text(
        json.dumps(scaffold_manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (OUT_DIR / "scaffold_manifest.json").write_text(
        json.dumps(scaffold_manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    readiness_manifest = {
        "run_id": RUN_ID,
        "readiness_state": "SCAFFOLD_ONLY_NOT_DISCOVERY_READY",
        "point_in_time_discovery_ready": False,
        "discovery_design_ready": False,
        "metadata_ingested": False,
        "pit_economic_context_panel_contains_records": False,
        "notes": "Placeholder readiness manifest. No PIT data exists from this scaffold.",
    }
    (MANIFESTS_DIR / "readiness_manifest_placeholder.json").write_text(
        json.dumps(readiness_manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _write_validation_scaffold() -> None:
    pd.DataFrame(VALIDATION_SCAFFOLD_CHECKS, columns=["check", "scaffold_status", "notes"]).to_csv(
        DIAGNOSTICS_DIR / "validation_scaffold_checks.csv",
        index=False,
    )
    pd.DataFrame(
        [
            {"guardrail": "no_metadata_ingestion", "status": True},
            {"guardrail": "no_source_selection", "status": True},
            {"guardrail": "no_sector_history_reconstruction", "status": True},
            {"guardrail": "no_industry_history_reconstruction", "status": True},
            {"guardrail": "no_peer_group_reconstruction", "status": True},
            {"guardrail": "no_discovery", "status": True},
            {"guardrail": "no_validation", "status": True},
            {"guardrail": "no_governance_mutation", "status": True},
            {"guardrail": "no_production_registration", "status": True},
            {"guardrail": "no_ml", "status": True},
        ]
    ).to_csv(DIAGNOSTICS_DIR / "guardrail_confirmation.csv", index=False)


def _write_diagnostic_placeholders() -> None:
    for filename, columns in DIAGNOSTIC_PLACEHOLDERS.items():
        pd.DataFrame(columns=columns).to_csv(DIAGNOSTICS_DIR / filename, index=False)

    pd.DataFrame(
        [
            {
                "review_item": "scaffold_status",
                "status": "scaffold_only",
                "notes": "No metadata source accepted; no data ingested; no reconstruction performed.",
            }
        ]
    ).to_csv(READINESS_REVIEW_DIR / "scaffold_readiness_placeholder.csv", index=False)

    (TESTS_DIR / "test_placeholder_manifest.json").write_text(
        json.dumps({"test_artifacts_placeholder_only": True, "data_dependent_tests": False}, indent=2),
        encoding="utf-8",
    )


def write_scaffold() -> None:
    _ensure_dirs()
    _write_schema_templates()
    _write_source_gate_scaffold()
    _write_semantic_scaffold()
    _write_manifests()
    _write_validation_scaffold()
    _write_diagnostic_placeholders()


def validate_source_manifest(path: Path | str = SOURCE_GATE_TEMPLATE_PATH) -> list[tuple[str, str]]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing source acceptance manifest: {manifest_path}")

    df = pd.read_csv(manifest_path)
    observed_fields = set(df.columns.astype(str))
    missing_fields = set(SOURCE_ACCEPTANCE_MANIFEST_FIELDS) - observed_fields
    if missing_fields:
        raise ValueError(f"Source acceptance manifest missing required fields: {sorted(missing_fields)}")

    allowed_status = _values_for("source_status_values")
    invalid_status = set(df.get("source_gate_status", pd.Series(dtype=str)).dropna().astype(str)) - allowed_status
    if invalid_status:
        raise ValueError(f"Invalid source_gate_status values: {sorted(invalid_status)}")

    if "point_in_time_quality" in df.columns:
        invalid_quality = set(df["point_in_time_quality"].dropna().astype(str)) - _values_for("pit_quality_classes")
        if invalid_quality:
            raise ValueError(f"Invalid point_in_time_quality values: {sorted(invalid_quality)}")

    if "confidence_tier" in df.columns:
        invalid_confidence = set(df["confidence_tier"].dropna().astype(str)) - _values_for("confidence_tiers")
        if invalid_confidence:
            raise ValueError(f"Invalid confidence_tier values: {sorted(invalid_confidence)}")

    if "event_type" in df.columns:
        invalid_events = set(df["event_type"].dropna().astype(str)) - _values_for("security_event_types")
        if invalid_events:
            raise ValueError(f"Invalid event_type values: {sorted(invalid_events)}")

    if "blocked_reason" in df.columns:
        invalid_blocked = set(df["blocked_reason"].dropna().astype(str)) - _values_for("blocked_reason_codes")
        if invalid_blocked:
            raise ValueError(f"Invalid blocked_reason values: {sorted(invalid_blocked)}")

    score_fields = _source_acceptance_manifest_schema()["score_fields"]
    for field in score_fields:
        if field in df.columns and not df.empty:
            numeric = pd.to_numeric(df[field], errors="coerce")
            invalid_scores = numeric.dropna()[(numeric.dropna() < 0) | (numeric.dropna() > 3)]
            if not invalid_scores.empty:
                raise ValueError(f"Invalid source-gate score range in {field}")

    return [
        ("required_manifest_fields", f"{len(SOURCE_ACCEPTANCE_MANIFEST_FIELDS)} fields present"),
        ("allowed_source_status_values", "validated"),
        ("allowed_pit_quality_values", "validated when column present"),
        ("allowed_confidence_tier_values", "validated when column present"),
        ("allowed_event_type_values", "validated when column present"),
        ("allowed_blocked_reason_values", "validated when column present"),
        ("score_fields", "validated for 0-3 range when rows present"),
        ("real_source_rows", str(len(df))),
    ]


def canonical_allowed_use(raw_allowed_use: object) -> str:
    raw_value = "" if pd.isna(raw_allowed_use) else str(raw_allowed_use).strip()
    if raw_value not in ALLOWED_USE_MAPPING:
        raise ValueError(f"Invalid allowed_use value: {raw_value}")
    return ALLOWED_USE_MAPPING[raw_value]


def _parse_bool(value: object) -> bool | None:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def _parse_list_field(value: object) -> list[str]:
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("["):
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            raise ValueError(f"Expected JSON list, received: {text}")
        return [str(item) for item in parsed]
    return [item.strip() for item in text.split(";") if item.strip()]


def _row_text(row: pd.Series, field: str) -> str:
    value = row.get(field, "")
    if pd.isna(value):
        return ""
    return str(value).strip()


def validate_conditional_scope(path: Path | str = SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH) -> list[tuple[str, str]]:
    scope_path = Path(path)
    if not scope_path.exists():
        raise FileNotFoundError(f"Missing conditional scope manifest: {scope_path}")

    df = pd.read_csv(scope_path)
    missing_fields = set(CONDITIONAL_SCOPE_FIELDS) - set(df.columns.astype(str))
    if missing_fields:
        raise ValueError(f"Conditional scope missing required fields: {sorted(missing_fields)}")

    for idx, row in df.iterrows():
        row_label = f"row {idx}"
        status = _row_text(row, "status")
        if status not in CONDITIONAL_SCOPE_STATUS_VALUES:
            raise ValueError(f"Invalid conditional scope status at {row_label}: {status}")

        for field in ("conditional_scope_id", "source_gate_run_id", "source", "source_version", "source_snapshot_date"):
            if not _row_text(row, field):
                raise ValueError(f"Missing {field} in conditional scope at {row_label}")

        permitted_uses = _parse_list_field(row.get("permitted_uses"))
        prohibited_uses = _parse_list_field(row.get("prohibited_uses"))
        invalid_uses = (set(permitted_uses) | set(prohibited_uses)) - set(CANONICAL_ALLOWED_USE_CATEGORIES)
        if invalid_uses:
            raise ValueError(f"Invalid conditional scope allowed-use values at {row_label}: {sorted(invalid_uses)}")
        if not permitted_uses:
            raise ValueError(f"Conditional scope must declare permitted_uses at {row_label}")

        permitted_domains = _parse_list_field(row.get("permitted_domains"))
        prohibited_domains = _parse_list_field(row.get("prohibited_domains"))
        invalid_domains = (set(permitted_domains) | set(prohibited_domains)) - CONDITIONAL_SCOPE_DOMAIN_VALUES
        if invalid_domains:
            raise ValueError(f"Invalid conditional scope domain values at {row_label}: {sorted(invalid_domains)}")
        if not permitted_domains:
            raise ValueError(f"Conditional scope must declare permitted_domains at {row_label}")

        floor = pd.to_numeric(pd.Series([row.get("required_confidence_floor")]), errors="coerce").iloc[0]
        if pd.isna(floor) or floor < 0 or floor > 1:
            raise ValueError(f"Invalid required_confidence_floor at {row_label}")

        blocked_reason = _row_text(row, "blocked_reason_if_violated")
        if blocked_reason not in _values_for("blocked_reason_codes"):
            raise ValueError(f"Invalid blocked_reason_if_violated at {row_label}: {blocked_reason}")

        for field in ("effective_start", "effective_end", "expiration_or_review_date", "rationale", "review_timestamp", "reviewer_notes"):
            if not _row_text(row, field):
                raise ValueError(f"Missing {field} in conditional scope at {row_label}")

    return [
        ("conditional_scope_required_fields", f"{len(CONDITIONAL_SCOPE_FIELDS)} fields present"),
        ("conditional_scope_rows", str(len(df))),
        ("conditional_scope_values", "validated"),
    ]


def validate_status_transition(prior_status: str, new_status: str) -> bool:
    allowed_status = _values_for("source_status_values")
    if prior_status not in allowed_status:
        raise ValueError(f"Invalid prior source status: {prior_status}")
    if new_status not in allowed_status:
        raise ValueError(f"Invalid new source status: {new_status}")
    return (prior_status, new_status) in LEGAL_SOURCE_STATUS_TRANSITIONS


def evaluate_conditional_scope(
    scope: dict[str, object],
    requested_use: str = "lineage_only",
    requested_domain: str = "security_identity",
    confidence: float = 0.70,
) -> tuple[str, str]:
    if str(scope.get("status", "")).strip() != "active":
        return ("blocked", str(scope.get("blocked_reason_if_violated") or "unsupported_domain"))
    permitted_uses = set(_parse_list_field(scope.get("permitted_uses")))
    prohibited_uses = set(_parse_list_field(scope.get("prohibited_uses")))
    permitted_domains = set(_parse_list_field(scope.get("permitted_domains")))
    prohibited_domains = set(_parse_list_field(scope.get("prohibited_domains")))
    if requested_use not in permitted_uses or requested_use in prohibited_uses:
        return ("blocked", str(scope.get("blocked_reason_if_violated") or "unsupported_domain"))
    if requested_domain not in permitted_domains or requested_domain in prohibited_domains:
        return ("blocked", str(scope.get("blocked_reason_if_violated") or "unsupported_domain"))
    floor = float(scope.get("required_confidence_floor", 0.70))
    if confidence < floor:
        return ("blocked", "low_confidence_lineage")
    if _parse_list_field(scope.get("required_review_flags")):
        return ("manual_review_required", "manual_review_required")
    return ("eligible_with_conditions", "")


def semantic_eligibility_decision(
    row: dict[str, object] | pd.Series,
    requested_use: str = "lineage_only",
    requested_domain: str = "security_identity",
    conditional_scope: dict[str, object] | None = None,
) -> dict[str, object]:
    series = pd.Series(row)
    status = _row_text(series, "source_gate_status")
    raw_allowed_use = _row_text(series, "allowed_use")
    try:
        canonical_use = canonical_allowed_use(raw_allowed_use)
    except ValueError:
        return {
            "raw_allowed_use": raw_allowed_use,
            "canonical_allowed_use": "",
            "eligibility_decision": "blocked",
            "blocked_reason": "unsupported_domain",
        }

    manual_review = _parse_bool(series.get("manual_review_required"))
    pit_quality = _row_text(series, "point_in_time_quality")
    confidence_tier = _row_text(series, "confidence_tier")
    blocked_pit_quality = {"static_snapshot_only", "unresolved", "blocked"}
    blocked_confidence = {"low", "blocked", "unknown"}

    decision = "eligible"
    blocked_reason = ""
    if status in {"rejected", "deprecated"}:
        decision = "blocked"
        blocked_reason = "source_rejected"
    elif status == "diagnostic_only":
        decision = "diagnostics_only" if requested_use == "diagnostics_only" else "blocked"
        blocked_reason = "" if decision == "diagnostics_only" else "source_rejected"
    elif status == "manual_review_required" or manual_review is True:
        decision = "manual_review_required"
        blocked_reason = "manual_review_required"
    elif status == "conditional":
        if conditional_scope is None:
            decision = "blocked"
            blocked_reason = "unsupported_domain"
        else:
            decision, blocked_reason = evaluate_conditional_scope(
                conditional_scope,
                requested_use=requested_use,
                requested_domain=requested_domain,
            )
    elif status != "accepted":
        decision = "blocked"
        blocked_reason = "unsupported_domain"
    elif canonical_use != "lineage_only" and requested_use == "lineage_only":
        decision = "blocked"
        blocked_reason = "unsupported_domain"

    if decision == "eligible":
        if pit_quality in blocked_pit_quality:
            decision = "blocked"
            blocked_reason = pit_quality if pit_quality in _values_for("blocked_reason_codes") else "static_snapshot_only"
        elif confidence_tier in blocked_confidence:
            decision = "blocked"
            blocked_reason = "low_confidence_lineage"
        else:
            score_fields = _source_acceptance_manifest_schema()["score_fields"]
            required_score_fields = {
                "pit_integrity_score",
                "identifier_quality_score",
                "historical_depth_score",
                "leakage_risk_score",
            }
            for field in score_fields:
                value = pd.to_numeric(pd.Series([series.get(field)]), errors="coerce").iloc[0]
                if pd.isna(value):
                    decision = "manual_review_required"
                    blocked_reason = "manual_review_required"
                    break
                if field in required_score_fields and value < 2:
                    decision = "blocked"
                    blocked_reason = "low_confidence_lineage"
                    break

    return {
        "raw_allowed_use": raw_allowed_use,
        "canonical_allowed_use": canonical_use,
        "eligibility_decision": decision,
        "blocked_reason": blocked_reason,
    }


def validate_semantic_rules(
    source_manifest_path: Path | str = SOURCE_GATE_TEMPLATE_PATH,
    conditional_scope_path: Path | str = SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH,
) -> list[tuple[str, str]]:
    validate_source_manifest(source_manifest_path)
    validate_conditional_scope(conditional_scope_path)

    manifest_df = pd.read_csv(source_manifest_path)
    for idx, row in manifest_df.iterrows():
        try:
            canonical_allowed_use(row.get("allowed_use"))
        except ValueError as exc:
            raise ValueError(f"Invalid semantic allowed_use at row {idx}: {exc}") from exc
        manual_review = _parse_bool(row.get("manual_review_required"))
        if manual_review is None:
            raise ValueError(f"Invalid manual_review_required value at row {idx}")
        status = _row_text(row, "source_gate_status")
        rejection_reason = _row_text(row, "rejection_reason")
        if status == "rejected" and not rejection_reason:
            raise ValueError(f"Rejected source missing rejection_reason at row {idx}")
        if status == "accepted" and manual_review:
            raise ValueError(f"Accepted source cannot require manual review at row {idx}")
        if status == "accepted":
            decision = semantic_eligibility_decision(row)
            if decision["eligibility_decision"] != "eligible":
                raise ValueError(f"Accepted source failed semantic eligibility at row {idx}: {decision}")

    return [
        ("allowed_use_mapping", f"{len(ALLOWED_USE_MAPPING)} mappings validated"),
        ("canonical_allowed_use_categories", f"{len(CANONICAL_ALLOWED_USE_CATEGORIES)} categories declared"),
        ("conditional_scope_schema", f"{len(CONDITIONAL_SCOPE_FIELDS)} fields validated"),
        ("source_status_transition_rules", f"{len(LEGAL_SOURCE_STATUS_TRANSITIONS)} legal transitions declared"),
        ("semantic_diagnostics", f"{len(SEMANTIC_DIAGNOSTIC_OUTPUTS)} placeholders declared"),
        ("source_manifest_semantic_rows", str(len(manifest_df))),
    ]


def validate_scaffold() -> list[str]:
    messages: list[str] = []
    missing_dirs = [str(path) for path in ARTIFACT_DIRS if not path.is_dir()]
    if missing_dirs:
        raise FileNotFoundError(f"Missing scaffold artifact directories: {missing_dirs}")
    messages.append("artifact_directories_present")

    expected_schema_files = []
    for name in SCHEMA_DEFINITIONS:
        target_dir = SOURCE_GATE_DIR if name == "source_acceptance_manifest" else SCHEMAS_DIR
        expected_schema_files.append(target_dir / f"{name}_schema.csv")
    missing_schema_files = [str(path) for path in expected_schema_files if not path.exists()]
    if missing_schema_files:
        raise FileNotFoundError(f"Missing schema template files: {missing_schema_files}")
    messages.append("schema_templates_present")

    required_source_gate_files = [
        SOURCE_GATE_VOCAB_PATH,
        SOURCE_GATE_TEMPLATE_PATH,
        SOURCE_GATE_SCHEMA_PATH,
        SOURCE_GATE_REPORT_PATH,
        SOURCE_GATE_MANIFEST_PATH,
    ]
    missing_source_gate_files = [str(path) for path in required_source_gate_files if not path.exists()]
    if missing_source_gate_files:
        raise FileNotFoundError(f"Missing source-gate scaffold files: {missing_source_gate_files}")
    validate_source_manifest(SOURCE_GATE_TEMPLATE_PATH)
    messages.append("source_gate_scaffold_present")

    required_semantic_files = [
        SOURCE_GATE_ALLOWED_USE_MAPPING_PATH,
        SOURCE_GATE_TRANSITIONS_PATH,
        SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH,
        SOURCE_GATE_CONDITIONAL_SCOPE_SCHEMA_PATH,
        SOURCE_GATE_SEMANTIC_REPORT_PATH,
        SOURCE_GATE_SEMANTIC_MANIFEST_PATH,
    ]
    required_semantic_files.extend(SOURCE_GATE_DIR / filename for filename in SEMANTIC_DIAGNOSTIC_OUTPUTS)
    missing_semantic_files = [str(path) for path in required_semantic_files if not path.exists()]
    if missing_semantic_files:
        raise FileNotFoundError(f"Missing semantic validation scaffold files: {missing_semantic_files}")
    validate_semantic_rules()
    messages.append("semantic_validation_scaffold_present")

    required_manifest_files = [
        MANIFESTS_DIR / "scaffold_manifest.json",
        OUT_DIR / "scaffold_manifest.json",
        MANIFESTS_DIR / "deliverable_inventory.csv",
        MANIFESTS_DIR / "readiness_gate_inventory.csv",
        MANIFESTS_DIR / "readiness_manifest_placeholder.json",
    ]
    missing_manifest_files = [str(path) for path in required_manifest_files if not path.exists()]
    if missing_manifest_files:
        raise FileNotFoundError(f"Missing manifest files: {missing_manifest_files}")
    messages.append("manifests_present")

    missing_placeholders = [str(DIAGNOSTICS_DIR / name) for name in DIAGNOSTIC_PLACEHOLDERS if not (DIAGNOSTICS_DIR / name).exists()]
    if missing_placeholders:
        raise FileNotFoundError(f"Missing diagnostic placeholder files: {missing_placeholders}")
    messages.append("diagnostic_placeholders_present")

    for name, rows in SCHEMA_DEFINITIONS.items():
        df = pd.read_csv((SOURCE_GATE_DIR if name == "source_acceptance_manifest" else SCHEMAS_DIR) / f"{name}_schema.csv")
        required_fields = {str(row["field"]) for row in rows if bool(row["required"])}
        observed_fields = set(df.loc[df["required"].astype(bool), "field"].astype(str))
        missing_required = required_fields - observed_fields
        if missing_required:
            raise ValueError(f"Schema {name} missing required fields: {sorted(missing_required)}")
        optional_fields = set(df.loc[~df["required"].astype(bool), "field"].astype(str))
        if optional_fields:
            raise ValueError(f"Schema {name} has optional fields after alignment: {sorted(optional_fields)}")
    messages.append("required_fields_declared")
    messages.append("schema_required_flags_aligned")

    manifest = json.loads((MANIFESTS_DIR / "scaffold_manifest.json").read_text(encoding="utf-8"))
    forbidden_flags = [
        "metadata_ingested",
        "source_selected",
        "sector_history_reconstructed",
        "industry_history_reconstructed",
        "peer_groups_reconstructed",
        "pit_classifications_created",
        "discovery_executed",
        "refinement_executed",
        "validation_executed",
        "governance_modified",
        "thresholds_modified",
        "production_registration",
        "ml_integration",
        "alpha_candidates_created",
        "candidate_promotion_or_demotion",
    ]
    bad_flags = [flag for flag in forbidden_flags if manifest.get(flag) is not False]
    if bad_flags:
        raise ValueError(f"Scaffold manifest has forbidden flags not false: {bad_flags}")
    messages.append("guardrail_flags_false")

    source_gate_manifest = json.loads(SOURCE_GATE_MANIFEST_PATH.read_text(encoding="utf-8"))
    source_gate_forbidden_flags = [
        "real_sources_loaded",
        "metadata_ingested",
        "lineage_constructed",
        "sector_history_reconstructed",
        "industry_history_reconstructed",
        "peer_groups_reconstructed",
        "discovery_executed",
        "validation_executed",
        "governance_modified",
        "thresholds_modified",
        "production_registration",
        "ml_integration",
        "alpha_candidates_created",
    ]
    source_gate_bad_flags = [
        flag for flag in source_gate_forbidden_flags if source_gate_manifest.get(flag) is not False
    ]
    if source_gate_bad_flags:
        raise ValueError(f"Source-gate manifest has forbidden flags not false: {source_gate_bad_flags}")
    messages.append("source_gate_guardrail_flags_false")

    semantic_manifest = json.loads(SOURCE_GATE_SEMANTIC_MANIFEST_PATH.read_text(encoding="utf-8"))
    semantic_forbidden_flags = [
        "real_sources_loaded",
        "metadata_ingested",
        "source_accepted",
        "metadata_constructed",
        "lineage_constructed",
        "sector_history_reconstructed",
        "industry_history_reconstructed",
        "peer_groups_reconstructed",
        "discovery_executed",
        "validation_executed",
        "governance_modified",
        "thresholds_modified",
        "production_registration",
        "ml_integration",
        "alpha_candidates_created",
    ]
    semantic_bad_flags = [
        flag for flag in semantic_forbidden_flags if semantic_manifest.get(flag) is not False
    ]
    if semantic_bad_flags:
        raise ValueError(f"Semantic validation manifest has forbidden flags not false: {semantic_bad_flags}")
    messages.append("semantic_guardrail_flags_false")

    return messages


def list_deliverables() -> str:
    rows = [f"{row['deliverable']}: {row['required_status']}" for row in DELIVERABLES]
    return "\n".join(rows)


def list_vocab() -> str:
    rows: list[str] = []
    for name, values in CONTROLLED_VOCABULARIES.items():
        if isinstance(values, list):
            if values and isinstance(values[0], dict):
                rendered_values = [str(row["value"]) for row in values]
            else:
                rendered_values = [str(value) for value in values]
            rows.append(f"{name}: {', '.join(rendered_values)}")
        elif isinstance(values, dict):
            rows.append(f"{name}: {', '.join(values.keys())}")
        else:
            rows.append(f"{name}: {values}")
    return "\n".join(rows)


def list_allowed_use() -> str:
    rows = []
    for raw_value, canonical_value in sorted(ALLOWED_USE_MAPPING.items()):
        category = CANONICAL_ALLOWED_USE_CATEGORIES[canonical_value]
        rows.append(
            f"{raw_value} -> {canonical_value} "
            f"(construction={category['permits_construction']}, "
            f"reconstruction={category['permits_reconstruction']}, "
            f"discovery={category['permits_discovery']})"
        )
    return "\n".join(rows)


def list_status_transitions() -> str:
    rows = [f"{prior_status} -> {new_status}" for prior_status, new_status in sorted(LEGAL_SOURCE_STATUS_TRANSITIONS)]
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Point-in-time economic metadata scaffold runner.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Write scaffold templates, manifests, and placeholders only.")
    group.add_argument("--validate-scaffold", action="store_true", help="Validate scaffold files and guardrails.")
    group.add_argument("--list-deliverables", action="store_true", help="List required scaffold deliverables.")
    group.add_argument("--list-vocab", action="store_true", help="List controlled source-gate vocabulary values.")
    group.add_argument("--list-allowed-use", action="store_true", help="List canonical allowed-use mappings.")
    group.add_argument("--list-status-transitions", action="store_true", help="List legal source-status transitions.")
    group.add_argument(
        "--validate-source-manifest",
        action="store_true",
        help="Validate the source acceptance manifest template or provided manifest path.",
    )
    group.add_argument(
        "--validate-semantic-rules",
        action="store_true",
        help="Validate source-gate semantic scaffold rules and optional manifest paths.",
    )
    parser.add_argument(
        "--source-manifest-path",
        default=str(SOURCE_GATE_TEMPLATE_PATH),
        help="Manifest path used with --validate-source-manifest.",
    )
    parser.add_argument(
        "--conditional-scope-path",
        default=str(SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH),
        help="Conditional scope path used with --validate-semantic-rules.",
    )
    args = parser.parse_args()

    if args.list_deliverables:
        print(list_deliverables())
        return 0
    if args.list_vocab:
        print(list_vocab())
        return 0
    if args.list_allowed_use:
        print(list_allowed_use())
        return 0
    if args.list_status_transitions:
        print(list_status_transitions())
        return 0
    if args.validate_source_manifest:
        messages = validate_source_manifest(args.source_manifest_path)
        print("Source manifest validation passed: " + ", ".join(f"{check}={detail}" for check, detail in messages))
        return 0
    if args.validate_semantic_rules:
        messages = validate_semantic_rules(args.source_manifest_path, args.conditional_scope_path)
        print("Semantic validation passed: " + ", ".join(f"{check}={detail}" for check, detail in messages))
        return 0
    if args.dry_run:
        write_scaffold()
        print(
            "Dry-run complete: scaffold templates, manifests, and placeholders written; "
            "no metadata ingestion, no source selection, no reconstruction, no discovery, no validation."
        )
        return 0
    if args.validate_scaffold:
        messages = validate_scaffold()
        print("Scaffold validation passed: " + ", ".join(messages))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
