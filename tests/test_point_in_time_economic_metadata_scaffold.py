import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_point_in_time_economic_metadata_scaffold_v1 import (
    ARTIFACT_DIRS,
    ALLOWED_USE_MAPPING,
    CANONICAL_ALLOWED_USE_CATEGORIES,
    CONDITIONAL_SCOPE_FIELDS,
    LEGAL_SOURCE_STATUS_TRANSITIONS,
    CONTROLLED_VOCABULARIES,
    DIAGNOSTIC_PLACEHOLDERS,
    MANIFESTS_DIR,
    OUT_DIR,
    SCHEMA_DEFINITIONS,
    SCHEMAS_DIR,
    SOURCE_ACCEPTANCE_MANIFEST_FIELDS,
    SOURCE_GATE_DIR,
    SOURCE_GATE_MANIFEST_PATH,
    SOURCE_GATE_REPORT_PATH,
    SOURCE_GATE_SCHEMA_PATH,
    SOURCE_GATE_TEMPLATE_PATH,
    SOURCE_GATE_VOCAB_PATH,
    SOURCE_GATE_ALLOWED_USE_MAPPING_PATH,
    SOURCE_GATE_CONDITIONAL_SCOPE_SCHEMA_PATH,
    SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH,
    SOURCE_GATE_SEMANTIC_MANIFEST_PATH,
    SOURCE_GATE_SEMANTIC_REPORT_PATH,
    SOURCE_GATE_TRANSITIONS_PATH,
    SEMANTIC_DIAGNOSTIC_OUTPUTS,
    TESTS_DIR,
    canonical_allowed_use,
    deliverable_inventory,
    evaluate_conditional_scope,
    semantic_eligibility_decision,
    validate_conditional_scope,
    validate_source_manifest,
    validate_semantic_rules,
    validate_status_transition,
)


RUNNER = ["python", "pipelines/run_point_in_time_economic_metadata_scaffold_v1.py"]
EXPECTED_SCHEMAS = {
    "source_acceptance_manifest",
    "security_master_pit",
    "ticker_lineage_pit",
    "sector_industry_history_pit",
    "size_bucket_history_pit",
    "peer_group_history_pit",
    "metadata_source_lineage",
    "pit_metadata_coverage_diagnostics",
    "pit_economic_context_panel",
}
EXPECTED_REQUIRED_FIELDS = {
    "source_acceptance_manifest": {
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
    },
    "security_master_pit": {
        "security_id",
        "issuer_id",
        "company_name",
        "security_type",
        "exchange",
        "country",
        "currency",
        "is_active",
        "effective_start",
        "effective_end",
        "as_of_date",
        "source",
        "source_version",
        "source_record_id",
        "metadata_version",
        "run_id",
        "collection_timestamp",
        "record_hash",
        "identity_confidence",
        "manual_override_flag",
        "point_in_time_quality",
        "security_event_id",
        "event_type",
        "event_effective_date",
        "event_as_of_date",
        "predecessor_security_id",
        "successor_security_id",
        "prior_ticker",
        "next_ticker",
        "event_confidence",
        "notes",
    },
    "ticker_lineage_pit": {
        "security_id",
        "ticker",
        "exchange",
        "ticker_namespace",
        "share_class",
        "primary_listing_flag",
        "ticker_effective_start",
        "ticker_effective_end",
        "as_of_date",
        "ticker_status",
        "change_reason",
        "prior_ticker",
        "next_ticker",
        "source",
        "source_version",
        "metadata_version",
        "run_id",
        "collection_timestamp",
        "record_hash",
        "ticker_mapping_confidence",
        "manual_override_flag",
        "point_in_time_quality",
    },
    "sector_industry_history_pit": {
        "security_id",
        "ticker_at_source",
        "sector",
        "industry",
        "subindustry",
        "classification_system",
        "classification_level",
        "taxonomy_version",
        "classification_provider_taxonomy_id",
        "taxonomy_effective_date",
        "taxonomy_change_flag",
        "taxonomy_change_reason",
        "effective_start",
        "effective_end",
        "as_of_date",
        "source_snapshot_date",
        "source",
        "source_version",
        "source_record_id",
        "metadata_version",
        "universe_version",
        "run_id",
        "collection_timestamp",
        "record_hash",
        "raw_record_hash",
        "classification_confidence",
        "manual_override_flag",
        "point_in_time_quality",
        "stale_metadata_flag",
        "notes",
    },
    "size_bucket_history_pit": {
        "security_id",
        "ticker_at_source",
        "market_cap",
        "market_cap_currency",
        "market_cap_as_of_date",
        "market_cap_source",
        "size_bucket",
        "market_cap_bucket",
        "effective_start",
        "effective_end",
        "as_of_date",
        "source",
        "source_version",
        "metadata_version",
        "run_id",
        "collection_timestamp",
        "record_hash",
        "size_confidence",
        "point_in_time_quality",
        "stale_metadata_flag",
        "manual_override_flag",
    },
    "peer_group_history_pit": {
        "signal_date",
        "security_id",
        "ticker",
        "sector",
        "industry",
        "size_bucket",
        "peer_group_label",
        "peer_group_level",
        "peer_group_method",
        "peer_group_size",
        "peer_group_min_size",
        "fallback_level",
        "fallback_reason",
        "blocked_for_peer_relative",
        "blocked_reason",
        "input_classification_version",
        "input_universe_version",
        "construction_rule_version",
        "source_metadata_version",
        "metadata_version",
        "run_id",
        "created_at",
        "peer_confidence_score",
        "point_in_time_quality",
        "fallback_quality_status",
    },
    "metadata_source_lineage": {
        "source_lineage_id",
        "run_id",
        "metadata_version",
        "source",
        "source_type",
        "source_version",
        "source_snapshot_date",
        "source_file_path",
        "source_url_or_reference",
        "source_file_hash",
        "record_count_raw",
        "record_count_clean",
        "collection_timestamp",
        "license_or_usage_notes",
        "normalization_rules",
        "created_by",
        "source_confidence",
        "point_in_time_quality",
        "manual_source_flag",
        "source_gate_score_summary",
        "notes",
    },
    "pit_metadata_coverage_diagnostics": {
        "run_id",
        "metadata_version",
        "universe_version",
        "diagnostic_scope",
        "diagnostic_start_date",
        "diagnostic_end_date",
        "total_active_tickers",
        "covered_active_tickers",
        "missing_active_tickers",
        "coverage_ratio",
        "sector_count",
        "industry_count",
        "peer_group_count",
        "thin_peer_group_count",
        "fallback_usage_rate",
        "broad_fallback_usage_rate",
        "fallback_dominance_flag",
        "stale_record_count",
        "stale_record_share",
        "stale_age_min",
        "stale_age_median",
        "stale_age_p75",
        "stale_age_p90",
        "stale_age_max",
        "unresolved_ticker_count",
        "duplicate_active_record_count",
        "eligible_ticker_date_count",
        "blocked_ticker_date_count",
        "eligible_ticker_date_share",
        "blocked_ticker_date_share",
        "point_in_time_quality",
        "coverage_quality_status",
        "created_at",
        "notes",
    },
    "pit_economic_context_panel": {
        "signal_date",
        "security_id",
        "ticker",
        "sector",
        "industry",
        "subindustry",
        "size_bucket",
        "peer_group_label",
        "peer_group_level",
        "peer_group_method",
        "peer_group_size",
        "peer_group_min_size",
        "fallback_level",
        "fallback_reason",
        "peer_confidence_score",
        "point_in_time_quality",
        "classification_metadata_version",
        "peer_group_metadata_version",
        "source_gate_run_id",
        "stale_age_days",
        "stale_record_flag",
        "discovery_eligible",
        "blocked_reason",
        "metadata_version",
        "created_at",
    },
}


def test_deliverable_inventory_declares_mvp_outputs():
    inventory = deliverable_inventory()
    assert set(EXPECTED_SCHEMAS).issubset(set(inventory["deliverable"]))
    assert "readiness_manifest" in set(inventory["deliverable"])
    assert len(inventory) == 10


def test_schema_constants_include_required_lineage_and_diagnostic_fields():
    assert set(SCHEMA_DEFINITIONS) == EXPECTED_SCHEMAS

    def fields(schema_name):
        return {row["field"] for row in SCHEMA_DEFINITIONS[schema_name]}

    for schema_name, expected_required_fields in EXPECTED_REQUIRED_FIELDS.items():
        observed_required_fields = {
            row["field"] for row in SCHEMA_DEFINITIONS[schema_name] if row["required"]
        }
        assert observed_required_fields == expected_required_fields

    assert {"event_type", "event_effective_date", "successor_security_id"}.issubset(
        fields("security_master_pit")
    )
    assert {"taxonomy_version", "taxonomy_effective_date", "taxonomy_change_flag"}.issubset(
        fields("sector_industry_history_pit")
    )
    assert {"fallback_level", "blocked_for_peer_relative", "peer_group_size"}.issubset(
        fields("peer_group_history_pit")
    )
    assert {"fallback_dominance_flag", "stale_age_p90", "blocked_ticker_date_count"}.issubset(
        fields("pit_metadata_coverage_diagnostics")
    )
    assert {"source_gate_run_id", "discovery_eligible", "blocked_reason"}.issubset(
        fields("pit_economic_context_panel")
    )


def test_list_deliverables_works_without_writing_data():
    res = subprocess.run([*RUNNER, "--list-deliverables"], capture_output=True, text=True)
    assert res.returncode == 0, f"--list-deliverables failed: {res.stderr}\n{res.stdout}"
    assert "source_acceptance_manifest" in res.stdout
    assert "pit_economic_context_panel" in res.stdout


def test_controlled_vocabularies_are_unique_and_include_policy_values():
    expected_vocab_names = {
        "source_status_values",
        "pit_quality_classes",
        "confidence_tiers",
        "security_event_types",
        "blocked_reason_codes",
        "inferred_window_policy",
        "stale_age_policy",
        "manual_override_policy",
    }
    assert expected_vocab_names.issubset(CONTROLLED_VOCABULARIES)

    def values_for(name):
        values = CONTROLLED_VOCABULARIES[name]
        if values and isinstance(values[0], dict):
            return [row["value"] for row in values]
        return list(values)

    expected_values = {
        "source_status_values": {"accepted", "conditional", "manual_review_required", "diagnostic_only", "rejected", "deprecated"},
        "pit_quality_classes": {"point_in_time_verified", "inferred_window", "static_snapshot_only", "unresolved", "blocked"},
        "confidence_tiers": {"high", "medium", "low", "blocked", "unknown"},
        "security_event_types": {"ticker_change", "delisting", "merger", "spin_off", "ticker_reuse", "unknown_event"},
        "blocked_reason_codes": {"missing_effective_date", "duplicate_active_mapping", "unresolved_security_identity", "source_rejected"},
    }
    for name, expected in expected_values.items():
        observed = values_for(name)
        assert len(observed) == len(set(observed))
        assert expected.issubset(set(observed))


def test_list_vocab_works_without_writing_data():
    res = subprocess.run([*RUNNER, "--list-vocab"], capture_output=True, text=True)
    assert res.returncode == 0, f"--list-vocab failed: {res.stderr}\n{res.stdout}"
    assert "source_status_values" in res.stdout
    assert "accepted" in res.stdout
    assert "ticker_reuse" in res.stdout


def test_allowed_use_mapping_and_status_transitions_are_defined():
    assert set(CANONICAL_ALLOWED_USE_CATEGORIES) == {
        "diagnostics_only",
        "lineage_only",
        "reconstruction_allowed",
        "discovery_allowed",
        "research_only",
        "blocked",
    }
    assert canonical_allowed_use("identity_ticker_lineage") == "lineage_only"
    assert canonical_allowed_use("diagnostic_only") == "diagnostics_only"
    assert canonical_allowed_use("deprecated_no_new_builds") == "blocked"
    with pytest.raises(ValueError, match="Invalid allowed_use"):
        canonical_allowed_use("anything_goes")

    assert ("diagnostic_only", "manual_review_required") in LEGAL_SOURCE_STATUS_TRANSITIONS
    assert ("diagnostic_only", "accepted") in LEGAL_SOURCE_STATUS_TRANSITIONS
    assert validate_status_transition("diagnostic_only", "accepted") is True
    assert validate_status_transition("accepted", "rejected") is False


def test_list_allowed_use_and_transitions_work_without_writing_data():
    allowed_use = subprocess.run([*RUNNER, "--list-allowed-use"], capture_output=True, text=True)
    assert allowed_use.returncode == 0, f"--list-allowed-use failed: {allowed_use.stderr}\n{allowed_use.stdout}"
    assert "identity_ticker_lineage -> lineage_only" in allowed_use.stdout
    assert "deprecated_no_new_builds -> blocked" in allowed_use.stdout

    transitions = subprocess.run([*RUNNER, "--list-status-transitions"], capture_output=True, text=True)
    assert transitions.returncode == 0, f"--list-status-transitions failed: {transitions.stderr}\n{transitions.stdout}"
    assert "diagnostic_only -> accepted" in transitions.stdout
    assert "accepted -> deprecated" in transitions.stdout


def test_dry_run_creates_scaffold_artifacts_and_no_data_records():
    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--dry-run failed: {res.stderr}\n{res.stdout}"
    assert "no metadata ingestion" in res.stdout
    assert "no reconstruction" in res.stdout

    for path in ARTIFACT_DIRS:
        assert path.is_dir()

    for schema_name in EXPECTED_SCHEMAS:
        target_dir = SOURCE_GATE_DIR if schema_name == "source_acceptance_manifest" else SCHEMAS_DIR
        schema_path = target_dir / f"{schema_name}_schema.csv"
        assert schema_path.exists()
        schema_df = pd.read_csv(schema_path)
        assert {"field", "required", "category", "notes"}.issubset(schema_df.columns)
        observed_required_fields = set(schema_df.loc[schema_df["required"].astype(bool), "field"])
        assert observed_required_fields == EXPECTED_REQUIRED_FIELDS[schema_name]
        assert schema_df["required"].astype(bool).all()

    for filename in DIAGNOSTIC_PLACEHOLDERS:
        placeholder_path = OUT_DIR / "diagnostics" / filename
        assert placeholder_path.exists()
        placeholder_df = pd.read_csv(placeholder_path)
        assert placeholder_df.empty

    assert (MANIFESTS_DIR / "scaffold_manifest.json").exists()
    assert (OUT_DIR / "scaffold_manifest.json").exists()
    assert (MANIFESTS_DIR / "deliverable_inventory.csv").exists()
    assert (MANIFESTS_DIR / "readiness_gate_inventory.csv").exists()
    assert (TESTS_DIR / "test_placeholder_manifest.json").exists()
    assert SOURCE_GATE_VOCAB_PATH.exists()
    assert SOURCE_GATE_TEMPLATE_PATH.exists()
    assert SOURCE_GATE_SCHEMA_PATH.exists()
    assert SOURCE_GATE_REPORT_PATH.exists()
    assert SOURCE_GATE_MANIFEST_PATH.exists()
    assert SOURCE_GATE_ALLOWED_USE_MAPPING_PATH.exists()
    assert SOURCE_GATE_TRANSITIONS_PATH.exists()
    assert SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH.exists()
    assert SOURCE_GATE_CONDITIONAL_SCOPE_SCHEMA_PATH.exists()
    assert SOURCE_GATE_SEMANTIC_REPORT_PATH.exists()
    assert SOURCE_GATE_SEMANTIC_MANIFEST_PATH.exists()
    for filename in SEMANTIC_DIAGNOSTIC_OUTPUTS:
        assert (SOURCE_GATE_DIR / filename).exists()
        assert pd.read_csv(SOURCE_GATE_DIR / filename).empty

    template_df = pd.read_csv(SOURCE_GATE_TEMPLATE_PATH)
    assert list(template_df.columns) == SOURCE_ACCEPTANCE_MANIFEST_FIELDS
    assert template_df.empty

    source_gate_schema = json.loads(SOURCE_GATE_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert source_gate_schema["scaffold_only"] is True
    assert source_gate_schema["metadata_ingested"] is False
    assert "accepted" in source_gate_schema["allowed_values"]["source_gate_status"]
    assert "point_in_time_verified" in source_gate_schema["allowed_values"]["point_in_time_quality"]

    manifest = json.loads((MANIFESTS_DIR / "scaffold_manifest.json").read_text(encoding="utf-8"))
    assert manifest["scaffold_only"] is True
    assert manifest["placeholder_outputs_only"] is True

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
    assert all(manifest[flag] is False for flag in forbidden_flags)

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
    assert all(source_gate_manifest[flag] is False for flag in source_gate_forbidden_flags)

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
    assert all(semantic_manifest[flag] is False for flag in semantic_forbidden_flags)

    conditional_scope_df = pd.read_csv(SOURCE_GATE_CONDITIONAL_SCOPE_TEMPLATE_PATH)
    assert list(conditional_scope_df.columns) == CONDITIONAL_SCOPE_FIELDS
    assert conditional_scope_df.empty


def _source_manifest_row(**overrides):
    row = {field: "" for field in SOURCE_ACCEPTANCE_MANIFEST_FIELDS}
    row.update(
        {
            "source_gate_run_id": "unit_test",
            "source": "placeholder_source",
            "source_type": "manual",
            "source_version": "v0",
            "source_snapshot_date": "2026-06-21",
            "source_file_hash": "placeholder_hash",
            "pit_integrity_score": 2,
            "coverage_score": 2,
            "historical_depth_score": 2,
            "identifier_quality_score": 2,
            "update_feasibility_score": 2,
            "source_stability_score": 2,
            "implementation_complexity_score": 2,
            "cost_manual_burden_score": 2,
            "leakage_risk_score": 2,
            "source_gate_status": "accepted",
            "allowed_use": "identity_ticker_lineage",
            "rejection_reason": "",
            "manual_review_required": False,
            "license_or_usage_notes": "research only",
            "review_timestamp": "2026-06-21T00:00:00Z",
            "reviewer_notes": "unit test",
            "point_in_time_quality": "point_in_time_verified",
            "confidence_tier": "high",
        }
    )
    row.update(overrides)
    return row


def _conditional_scope_row(**overrides):
    row = {
        "conditional_scope_id": "scope_unit_test",
        "source_gate_run_id": "unit_test",
        "source": "placeholder_source",
        "source_version": "v0",
        "source_snapshot_date": "2026-06-21",
        "status": "active",
        "permitted_uses": '["lineage_only"]',
        "prohibited_uses": '["reconstruction_allowed", "discovery_allowed"]',
        "permitted_domains": '["security_identity", "ticker_lineage"]',
        "prohibited_domains": '["sector_history", "industry_history", "peer_reconstruction", "discovery_support"]',
        "effective_start": "2020-01-01",
        "effective_end": "2025-12-31",
        "supported_universe": "declared_us_equity_universe",
        "unsupported_universe": "non_us_equities",
        "required_confidence_floor": 0.70,
        "required_review_flags": "[]",
        "expiration_or_review_date": "2026-12-31",
        "rationale": "unit test conditional source",
        "blocked_reason_if_violated": "unsupported_domain",
        "review_timestamp": "2026-06-21T00:00:00Z",
        "reviewer_notes": "unit test",
    }
    row.update(overrides)
    return row


def test_conditional_scope_validation_and_enforcement(tmp_path):
    scope_path = tmp_path / "conditional_scope.csv"
    pd.DataFrame([_conditional_scope_row()]).to_csv(scope_path, index=False)
    validate_conditional_scope(scope_path)

    decision, reason = evaluate_conditional_scope(
        _conditional_scope_row(),
        requested_use="lineage_only",
        requested_domain="security_identity",
        confidence=0.80,
    )
    assert decision == "eligible_with_conditions"
    assert reason == ""

    blocked_decision, blocked_reason = evaluate_conditional_scope(
        _conditional_scope_row(),
        requested_use="discovery_allowed",
        requested_domain="discovery_support",
        confidence=0.80,
    )
    assert blocked_decision == "blocked"
    assert blocked_reason == "unsupported_domain"

    bad_scope_path = tmp_path / "bad_scope.csv"
    pd.DataFrame([_conditional_scope_row(status="unknown")]).to_csv(bad_scope_path, index=False)
    with pytest.raises(ValueError, match="Invalid conditional scope status"):
        validate_conditional_scope(bad_scope_path)


def test_semantic_eligibility_engine_decisions():
    accepted = semantic_eligibility_decision(_source_manifest_row())
    assert accepted["eligibility_decision"] == "eligible"
    assert accepted["canonical_allowed_use"] == "lineage_only"

    manual_review = semantic_eligibility_decision(_source_manifest_row(manual_review_required=True))
    assert manual_review["eligibility_decision"] == "manual_review_required"
    assert manual_review["blocked_reason"] == "manual_review_required"

    rejected = semantic_eligibility_decision(
        _source_manifest_row(source_gate_status="rejected", allowed_use="rejected", rejection_reason="static snapshot")
    )
    assert rejected["eligibility_decision"] == "blocked"
    assert rejected["canonical_allowed_use"] == "blocked"

    diagnostic = semantic_eligibility_decision(
        _source_manifest_row(source_gate_status="diagnostic_only", allowed_use="diagnostic_only")
    )
    assert diagnostic["eligibility_decision"] == "blocked"

    conditional = semantic_eligibility_decision(
        _source_manifest_row(source_gate_status="conditional"),
        conditional_scope=_conditional_scope_row(),
    )
    assert conditional["eligibility_decision"] == "eligible_with_conditions"


def test_validate_semantic_rules_rejects_invalid_configurations(tmp_path):
    def write_manifest(filename, rows):
        path = tmp_path / filename
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    scope_path = tmp_path / "scope.csv"
    pd.DataFrame([_conditional_scope_row()]).to_csv(scope_path, index=False)

    valid_manifest = write_manifest("valid.csv", [_source_manifest_row()])
    validate_semantic_rules(valid_manifest, scope_path)

    with pytest.raises(ValueError, match="Invalid semantic allowed_use"):
        validate_semantic_rules(write_manifest("bad_use.csv", [_source_manifest_row(allowed_use="anything")]), scope_path)
    with pytest.raises(ValueError, match="Invalid manual_review_required"):
        validate_semantic_rules(write_manifest("bad_review.csv", [_source_manifest_row(manual_review_required="maybe")]), scope_path)
    with pytest.raises(ValueError, match="Rejected source missing rejection_reason"):
        validate_semantic_rules(
            write_manifest("bad_rejected.csv", [_source_manifest_row(source_gate_status="rejected", allowed_use="rejected", rejection_reason="")]),
            scope_path,
        )
    with pytest.raises(ValueError, match="Accepted source cannot require manual review"):
        validate_semantic_rules(write_manifest("bad_accepted_review.csv", [_source_manifest_row(manual_review_required=True)]), scope_path)
    with pytest.raises(ValueError, match="Accepted source failed semantic eligibility"):
        validate_semantic_rules(
            write_manifest("bad_quality.csv", [_source_manifest_row(point_in_time_quality="static_snapshot_only")]),
            scope_path,
        )


def test_validate_source_manifest_succeeds_on_template_after_dry_run():
    dry_run = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert dry_run.returncode == 0, f"--dry-run failed: {dry_run.stderr}\n{dry_run.stdout}"

    res = subprocess.run([*RUNNER, "--validate-source-manifest"], capture_output=True, text=True)
    assert res.returncode == 0, f"--validate-source-manifest failed: {res.stderr}\n{res.stdout}"
    assert "Source manifest validation passed" in res.stdout
    assert "real_source_rows=0" in res.stdout


def test_source_manifest_validation_rejects_invalid_controlled_values(tmp_path):
    row = {field: "" for field in SOURCE_ACCEPTANCE_MANIFEST_FIELDS}
    row.update(
        {
            "source_gate_run_id": "unit_test",
            "source": "placeholder_source",
            "source_type": "manual",
            "source_version": "v0",
            "source_snapshot_date": "2026-06-20",
            "source_file_hash": "placeholder_hash",
            "pit_integrity_score": 0,
            "coverage_score": 0,
            "historical_depth_score": 0,
            "identifier_quality_score": 0,
            "update_feasibility_score": 0,
            "source_stability_score": 0,
            "implementation_complexity_score": 0,
            "cost_manual_burden_score": 0,
            "leakage_risk_score": 0,
            "source_gate_status": "accepted",
            "allowed_use": "identity_ticker_lineage",
            "manual_review_required": False,
            "review_timestamp": "2026-06-20T00:00:00Z",
        }
    )

    def write_manifest(filename, **overrides):
        rows = [{**row, **overrides}]
        path = tmp_path / filename
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    valid_path = write_manifest(
        "valid.csv",
        point_in_time_quality="point_in_time_verified",
        confidence_tier="high",
        event_type="ticker_change",
        blocked_reason="missing_effective_date",
    )
    validate_source_manifest(valid_path)

    with pytest.raises(ValueError, match="Invalid source_gate_status"):
        validate_source_manifest(write_manifest("bad_status.csv", source_gate_status="not_a_status"))
    with pytest.raises(ValueError, match="Invalid point_in_time_quality"):
        validate_source_manifest(write_manifest("bad_quality.csv", point_in_time_quality="future_clean"))
    with pytest.raises(ValueError, match="Invalid confidence_tier"):
        validate_source_manifest(write_manifest("bad_confidence.csv", confidence_tier="certain"))
    with pytest.raises(ValueError, match="Invalid event_type"):
        validate_source_manifest(write_manifest("bad_event.csv", event_type="magic_rename"))
    with pytest.raises(ValueError, match="Invalid blocked_reason"):
        validate_source_manifest(write_manifest("bad_blocked_reason.csv", blocked_reason="because"))


def test_validate_scaffold_succeeds_after_dry_run():
    dry_run = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert dry_run.returncode == 0, f"--dry-run failed: {dry_run.stderr}\n{dry_run.stdout}"

    res = subprocess.run([*RUNNER, "--validate-scaffold"], capture_output=True, text=True)
    assert res.returncode == 0, f"--validate-scaffold failed: {res.stderr}\n{res.stdout}"
    assert "Scaffold validation passed" in res.stdout
    assert "guardrail_flags_false" in res.stdout
    assert "source_gate_guardrail_flags_false" in res.stdout
    assert "source_gate_scaffold_present" in res.stdout
    assert "semantic_validation_scaffold_present" in res.stdout
    assert "semantic_guardrail_flags_false" in res.stdout
    assert "schema_required_flags_aligned" in res.stdout


def test_validate_semantic_rules_succeeds_after_dry_run():
    dry_run = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert dry_run.returncode == 0, f"--dry-run failed: {dry_run.stderr}\n{dry_run.stdout}"

    res = subprocess.run([*RUNNER, "--validate-semantic-rules"], capture_output=True, text=True)
    assert res.returncode == 0, f"--validate-semantic-rules failed: {res.stderr}\n{res.stdout}"
    assert "Semantic validation passed" in res.stdout
    assert "allowed_use_mapping" in res.stdout
    assert "source_status_transition_rules" in res.stdout


def test_runner_has_no_ingestion_or_reconstruction_mode():
    res = subprocess.run([*RUNNER, "--run"], capture_output=True, text=True)
    assert res.returncode != 0

    help_res = subprocess.run([*RUNNER, "--help"], capture_output=True, text=True)
    assert help_res.returncode == 0
    assert "--dry-run" in help_res.stdout
    assert "--validate-scaffold" in help_res.stdout
    assert "--validate-source-manifest" in help_res.stdout
    assert "--validate-semantic-rules" in help_res.stdout
    assert "--list-deliverables" in help_res.stdout
    assert "--list-vocab" in help_res.stdout
    assert "--list-allowed-use" in help_res.stdout
    assert "--list-status-transitions" in help_res.stdout
    assert "--run" not in help_res.stdout
