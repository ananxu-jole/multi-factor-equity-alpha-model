import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 import (
    APPROVED_CANDIDATE_IDS,
    CANDIDATE_REGISTRY_DIR,
    CANDIDATE_REGISTRY_FIELDS,
    REGISTRY_FINAL_CLASSIFICATION,
    REGISTRY_STATUS,
    candidate_registry_rows,
    validate_candidate_registry_rows,
)


RUNNER = ["python", "pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py"]


def test_candidate_registry_rows_are_nine_approved_concepts():
    rows = candidate_registry_rows()
    ids = [row["candidate_id"] for row in rows]

    assert len(rows) == 9
    assert ids == APPROVED_CANDIDATE_IDS
    assert "nhlr_06" not in ids

    for row in rows:
        for field in CANDIDATE_REGISTRY_FIELDS:
            assert field in row
            assert str(row[field]).strip()
        assert row["dependency_class"] == "OHLCV_ONLY"
        assert row["implementation_status"] == "REGISTRY_ONLY_NOT_IMPLEMENTED"
        assert row["formula_status"] == "NO_FORMULA_DEFINED"
        assert row["panel_status"] == "NO_PANEL_GENERATED"
        assert row["discovery_status"] == "DISCOVERY_NOT_EXECUTED"
        assert row["refinement_status"] == "REFINEMENT_NOT_EXECUTED"
        assert row["validation_status"] == "VALIDATION_NOT_EXECUTED"
        assert row["candidate_state"] == "REGISTRY_ONLY_NO_RESEARCH_OUTCOME"


def test_export_candidate_registry_creates_required_artifacts():
    res = subprocess.run([*RUNNER, "--export-candidate-registry"], capture_output=True, text=True)
    assert res.returncode == 0, f"--export-candidate-registry failed: {res.stderr}\n{res.stdout}"
    assert REGISTRY_STATUS in res.stdout
    assert REGISTRY_FINAL_CLASSIFICATION in res.stdout
    assert "No formulas" in res.stdout

    expected_paths = [
        CANDIDATE_REGISTRY_DIR / "candidate_registry.csv",
        CANDIDATE_REGISTRY_DIR / "candidate_registry_schema.json",
        CANDIDATE_REGISTRY_DIR / "candidate_registry_manifest.json",
        CANDIDATE_REGISTRY_DIR / "candidate_status_report.csv",
        CANDIDATE_REGISTRY_DIR / "candidate_dependency_report.csv",
        CANDIDATE_REGISTRY_DIR / "registry_validation_report.csv",
    ]
    for path in expected_paths:
        assert path.exists()

    registry = pd.read_csv(CANDIDATE_REGISTRY_DIR / "candidate_registry.csv")
    assert len(registry) == 9
    assert list(registry["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert set(CANDIDATE_REGISTRY_FIELDS).issubset(registry.columns)

    schema = json.loads((CANDIDATE_REGISTRY_DIR / "candidate_registry_schema.json").read_text(encoding="utf-8"))
    assert schema["registry_status"] == REGISTRY_STATUS
    assert schema["approved_candidate_ids"] == APPROVED_CANDIDATE_IDS
    assert schema["required_fields"] == CANDIDATE_REGISTRY_FIELDS

    manifest = json.loads((CANDIDATE_REGISTRY_DIR / "candidate_registry_manifest.json").read_text(encoding="utf-8"))
    assert manifest["registry_status"] == REGISTRY_STATUS
    assert manifest["final_classification"] == REGISTRY_FINAL_CLASSIFICATION
    assert manifest["candidate_count"] == 9
    assert manifest["candidate_formulas_defined"] is False
    assert manifest["candidate_code_implemented"] is False
    assert manifest["candidate_panels_generated"] is False
    assert manifest["discovery_executed"] is False
    assert manifest["ic_calculated"] is False
    assert manifest["redundancy_screening_run"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["production_registered"] is False
    assert manifest["ml_implemented"] is False

    validation_report = pd.read_csv(CANDIDATE_REGISTRY_DIR / "registry_validation_report.csv")
    assert not validation_report.empty
    assert set(validation_report["status"]) == {"PASS"}


def test_registry_support_runner_modes_pass():
    export_res = subprocess.run([*RUNNER, "--export-candidate-registry"], capture_output=True, text=True)
    assert export_res.returncode == 0, export_res.stderr

    list_res = subprocess.run([*RUNNER, "--list-candidates"], capture_output=True, text=True)
    assert list_res.returncode == 0, f"--list-candidates failed: {list_res.stderr}\n{list_res.stdout}"
    for candidate_id in APPROVED_CANDIDATE_IDS:
        assert candidate_id in list_res.stdout
    assert "REGISTRY_ONLY_NO_RESEARCH_OUTCOME" in list_res.stdout

    validate_res = subprocess.run([*RUNNER, "--validate-candidate-registry"], capture_output=True, text=True)
    assert validate_res.returncode == 0, (
        f"--validate-candidate-registry failed: {validate_res.stderr}\n{validate_res.stdout}"
    )
    assert "validation passed" in validate_res.stdout
    assert REGISTRY_STATUS in validate_res.stdout


def test_duplicate_candidate_id_detection():
    rows = candidate_registry_rows()
    rows[1] = dict(rows[0])

    ok, errors, report = validate_candidate_registry_rows(rows)

    assert not ok
    assert any("unique_candidate_ids" in error for error in errors)
    assert any(row["check_name"] == "unique_candidate_ids" and row["status"] == "FAIL" for row in report)


def test_lifecycle_status_validation_rejects_execution_drift():
    rows = candidate_registry_rows()
    rows[0] = dict(rows[0])
    rows[0]["discovery_status"] = "DISCOVERY_EXECUTED"
    rows[0]["candidate_state"] = "RESEARCH_RESULT_AVAILABLE"

    ok, errors, report = validate_candidate_registry_rows(rows)

    assert not ok
    assert any("lifecycle_status_consistency" in error for error in errors)
    assert any("research_outcome_consistency" in error for error in errors)
    assert any(row["status"] == "FAIL" for row in report)


def test_registry_reports_preserve_metadata_only_statuses():
    subprocess.run([*RUNNER, "--export-candidate-registry"], capture_output=True, text=True, check=True)

    status = pd.read_csv(CANDIDATE_REGISTRY_DIR / "candidate_status_report.csv")
    assert set(status["implementation_status"]) == {"REGISTRY_ONLY_NOT_IMPLEMENTED"}
    assert set(status["formula_status"]) == {"NO_FORMULA_DEFINED"}
    assert set(status["panel_status"]) == {"NO_PANEL_GENERATED"}
    assert set(status["discovery_status"]) == {"DISCOVERY_NOT_EXECUTED"}
    assert set(status["refinement_status"]) == {"REFINEMENT_NOT_EXECUTED"}
    assert set(status["validation_status"]) == {"VALIDATION_NOT_EXECUTED"}
    assert set(status["candidate_state"]) == {"REGISTRY_ONLY_NO_RESEARCH_OUTCOME"}

    dependency = pd.read_csv(CANDIDATE_REGISTRY_DIR / "candidate_dependency_report.csv")
    assert set(dependency["dependency_class"]) == {"OHLCV_ONLY"}
    assert set(dependency["required_input_family"]) == {"OHLCV_DERIVED_ONLY"}


def test_fail_closed_unsupported_registry_adjacent_modes():
    unsupported_modes = [
        "--implement-candidates",
        "--generate-candidate-panels",
        "--run-discovery",
        "--calculate-ic",
        "--run-redundancy-screening",
        "--run-refinement",
        "--run-validation",
        "--register-production",
    ]
    for mode in unsupported_modes:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode != 0, f"{mode} unexpectedly succeeded"
        assert "unrecognized arguments" in res.stderr or "usage:" in res.stderr
