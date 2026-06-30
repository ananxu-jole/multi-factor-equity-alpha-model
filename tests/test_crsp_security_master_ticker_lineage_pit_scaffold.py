import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_crsp_security_master_ticker_lineage_pit_v1 import (
    ARTIFACT_DIRS,
    ASSUMPTION_FIELDS,
    ASSUMPTIONS_DIR,
    EVIDENCE_FIELDS,
    DIAGNOSTIC_COLUMNS,
    DIAGNOSTIC_FILES,
    DIAGNOSTICS_DIR,
    MANIFESTS_DIR,
    OUT_DIR,
    SCHEMAS_DIR,
    SCHEMA_FIELDS,
    SOURCE_GATE_DIR,
    SOURCE_GATE_CONTROLLED_VOCABULARIES,
    SOURCE_GATE_DRY_RUN_CANDIDATES,
    SOURCE_GATE_MANIFEST_SCHEMA_FIELDS,
    SOURCE_GATE_RESULT_FIELDS,
    SOURCE_MANIFEST_FIELDS,
    VERIFICATION_CHECKLIST_FIELDS,
    VERIFICATION_ASSUMPTIONS,
    evaluate_source_gate,
    validate_all,
    validate_assumption_evidence,
    validate_source_gate_manifest,
    validate_source_gate_scaffold,
    write_scaffold,
    write_source_gate_scaffold,
    write_verification_scaffold,
)


RUNNER = ["python", "pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py"]


def test_dry_run_creates_artifact_tree_and_guardrail_manifests():
    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    assert "does not access CRSP data" in res.stdout
    assert "READY_FOR_ASSUMPTION_VERIFICATION" in res.stdout

    for path in ARTIFACT_DIRS:
        assert path.is_dir()

    manifest = json.loads((MANIFESTS_DIR / "crsp_scaffold_manifest.json").read_text(encoding="utf-8"))
    assert manifest["scaffold_only"] is True
    forbidden = [
        "crsp_data_accessed",
        "source_files_loaded",
        "data_ingested",
        "source_accepted",
        "metadata_constructed",
        "security_lineage_built",
        "ticker_lineage_built",
        "reconstruction_executed",
        "discovery_executed",
        "validation_executed",
        "governance_modified",
        "production_registered",
        "ml_implemented",
    ]
    assert all(manifest[field] is False for field in forbidden)
    assert (OUT_DIR / "crsp_scaffold_manifest.json").exists()


def test_runner_modes_succeed_without_crsp_access():
    for mode in [
        "--list-assumptions",
        "--validate-source-gate",
        "--list-source-gates",
        "--validate-source-gates",
        "--dry-run-source-gates",
        "--validate-schema-alignment",
        "--validate-assumptions",
        "--validate-diagnostics",
        "--list-verification-requirements",
        "--export-verification-checklist",
        "--validate-assumption-evidence",
        "--update-assumption-status",
    ]:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode == 0, f"{mode} failed: {res.stderr}\n{res.stdout}"


def test_assumption_register_structure_and_fail_closed_defaults():
    write_scaffold()
    path = ASSUMPTIONS_DIR / "crsp_assumption_register.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert list(df.columns) == ASSUMPTION_FIELDS
    assert {"subscription_scope", "licensing", "field_availability", "release_version", "known_date", "archival"}.issubset(
        set(df["assumption_area"])
    )
    critical_or_high = df[df["risk_level"].isin(["critical", "high"])]
    assert not critical_or_high.empty
    assert (critical_or_high["verification_status"] == "unverified").all()
    assert (critical_or_high["blocking_status"] == "blocking").all()


def test_source_gate_and_schema_alignment_placeholders_are_complete():
    write_scaffold()
    template = pd.read_csv(SOURCE_GATE_DIR / "crsp_source_acceptance_manifest_template.csv")
    assert list(template.columns) == SOURCE_MANIFEST_FIELDS
    assert template.empty

    for schema_name, expected_fields in SCHEMA_FIELDS.items():
        path = SCHEMAS_DIR / f"{schema_name}_alignment_checklist.csv"
        assert path.exists()
        df = pd.read_csv(path)
        assert set(df["field"]) == set(expected_fields)
        assert (df["required"].astype(bool)).all()
        assert (df["crsp_mapping_status"] == "unverified").all()
        assert (df["blocking_status"] == "blocking_until_verified").all()
        assert (df["placeholder_only"].astype(bool)).all()


def test_pit_source_gate_scaffold_templates_vocabularies_and_manifest_are_fail_closed():
    write_source_gate_scaffold()
    template = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_manifest_template.csv")
    assert list(template.columns) == SOURCE_GATE_MANIFEST_SCHEMA_FIELDS
    assert template.empty

    schema = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_manifest_schema.csv")
    assert set(schema["field"]) == set(SOURCE_GATE_MANIFEST_SCHEMA_FIELDS)
    assert schema["scaffold_only"].astype(bool).all()

    vocab = json.loads((SOURCE_GATE_DIR / "pit_source_gate_controlled_vocabularies.json").read_text(encoding="utf-8"))
    assert vocab == SOURCE_GATE_CONTROLLED_VOCABULARIES
    assert "static_snapshot_only" in vocab["pit_readiness"]
    assert "stable_security_and_ticker_lineage" in vocab["lineage_readiness"]

    manifest = json.loads((SOURCE_GATE_DIR / "pit_source_gate_scaffold_manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_gate_scaffold_only"] is True
    assert manifest["classification"] == "SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES"
    forbidden = [
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
    assert all(manifest[field] is False for field in forbidden)


def test_pit_source_gate_dry_run_outputs_and_scoring_are_deterministic():
    write_source_gate_scaffold()
    report = pd.read_csv(SOURCE_GATE_DIR / "pit_source_gate_dry_run_report.csv")
    assert list(report.columns) == SOURCE_GATE_RESULT_FIELDS
    assert len(report) == len(SOURCE_GATE_DRY_RUN_CANDIDATES)
    assert report["dry_run_only"].astype(bool).all()

    accepted = report[report["source_id"] == "candidate_pit_security_master_full"].iloc[0]
    assert bool(accepted["pass_source_gate"]) is True
    assert accepted["source_status"] == "accepted"
    assert accepted["allowed_use"] == "source_gate_only_future_implementation_review_required"

    static = report[report["source_id"] == "candidate_static_profile_api"].iloc[0]
    assert bool(static["pass_source_gate"]) is False
    assert static["source_status"] == "manual_review_required"
    assert "pit_capability:static_snapshot_only" in static["blocking_reasons"]
    assert "lineage_capability:ticker_only" in static["blocking_reasons"]


def test_pit_source_gate_manifest_validation_and_fail_closed_behavior():
    valid_errors = validate_source_gate_manifest(SOURCE_GATE_DRY_RUN_CANDIDATES)
    assert valid_errors == []

    bad_source = dict(SOURCE_GATE_DRY_RUN_CANDIDATES[0])
    bad_source["pit_capability"] = "magic_future_lookup"
    errors = validate_source_gate_manifest([bad_source])
    assert errors
    assert "invalid pit_capability" in errors[0]

    result = evaluate_source_gate(bad_source)
    assert result["pass_source_gate"] is False
    assert result["source_status"] == "rejected"
    assert result["pit_readiness"] == "blocked"
    assert result["allowed_use"] == "blocked_invalid_manifest"

    assert validate_source_gate_scaffold() == []


def test_diagnostics_placeholder_generation():
    write_scaffold()
    manifest = json.loads((DIAGNOSTICS_DIR / "crsp_diagnostic_manifest.json").read_text(encoding="utf-8"))
    assert manifest["scaffold_only"] is True
    assert manifest["crsp_data_accessed"] is False
    assert manifest["source_rows_evaluated"] is False

    for filename in DIAGNOSTIC_FILES:
        path = DIAGNOSTICS_DIR / filename
        assert path.exists()
        df = pd.read_csv(path)
        assert set(DIAGNOSTIC_COLUMNS).issubset(df.columns)
        assert (df["placeholder_only"].astype(bool)).all()
        assert (df["status"] == "blocked_unverified_scaffold").all()


def test_verification_scaffold_artifacts_are_created_and_blocking():
    write_verification_scaffold()
    expected_files = {
        "crsp_assumption_verification_checklist.csv",
        "crsp_assumption_evidence_register.csv",
        "crsp_subscription_scope_review.csv",
        "crsp_license_retention_review.csv",
        "crsp_field_availability_review.csv",
        "crsp_date_semantics_review.csv",
        "crsp_archive_hash_feasibility_review.csv",
        "crsp_source_gate_eligibility_update.json",
        "crsp_assumption_status_placeholder.csv",
    }
    for filename in expected_files:
        assert (ASSUMPTIONS_DIR / filename).exists()

    checklist = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_verification_checklist.csv")
    assert list(checklist.columns) == VERIFICATION_CHECKLIST_FIELDS
    assert set(checklist["assumption_id"]) == {row["assumption_id"] for row in VERIFICATION_ASSUMPTIONS}
    critical_or_high = checklist[checklist["risk_level"].isin(["critical", "high"])]
    assert (critical_or_high["verification_status"] == "unverified").all()
    assert (critical_or_high["blocker_status"] == "blocking").all()
    assert (checklist["scaffold_only"].astype(bool)).all()

    evidence = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_evidence_register.csv")
    assert list(evidence.columns) == EVIDENCE_FIELDS
    assert (evidence["evidence_type"] == "placeholder").all()
    assert (evidence["verification_status"] == "unverified").all()
    assert (evidence["blocker_status"] == "blocking").all()
    assert (evidence["scaffold_only"].astype(bool)).all()

    eligibility = json.loads((ASSUMPTIONS_DIR / "crsp_source_gate_eligibility_update.json").read_text(encoding="utf-8"))
    assert eligibility["source_gate_status"] == "manual_review_required"
    assert eligibility["allowed_use"] == "diagnostics_only"
    assert eligibility["ingestion_authorized"] is False
    assert eligibility["metadata_construction_authorized"] is False
    assert eligibility["lineage_construction_authorized"] is False


def test_update_assumption_status_is_scaffold_only_noop():
    res = subprocess.run([*RUNNER, "--update-assumption-status"], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    assert "No real assumption statuses updated" in res.stdout

    status = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_status_placeholder.csv")
    assert (status["requested_status"] == "verified").all()
    assert (status["applied_status"] == "unverified").all()
    assert not status["update_applied"].astype(bool).any()
    assert (status["blocker_status"] == "blocking").all()
    assert (status["scaffold_only"].astype(bool)).all()

    register = pd.read_csv(ASSUMPTIONS_DIR / "crsp_assumption_register.csv")
    assert "verified" not in set(register["verification_status"])
    assert validate_assumption_evidence() == []


def test_fail_closed_unsupported_modes_and_no_ingestion_guardrails():
    unsupported_modes = [
        "--ingest",
        "--load-source",
        "--build-lineage",
        "--construct-metadata",
        "--run-discovery",
        "--run-validation",
        "--source-file",
        "--build",
    ]
    for mode in unsupported_modes:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode != 0

    assert validate_all() == []
