import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
    FORMULA_STATUS,
    IMPLEMENTATION_FINAL_CLASSIFICATION,
    IMPLEMENTATION_STATUS,
    PANEL_STATUS,
    build_candidate_implementations,
    implementation_rows,
    registered_candidate_ids,
    validate_candidate_implementations,
)
from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 import (
    APPROVED_CANDIDATE_IDS,
    CANDIDATE_IMPLEMENTATION_DIR,
    REGISTRY_STATUS,
)


RUNNER = ["python", "pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py"]


def test_candidate_implementations_are_registry_aligned():
    implementations = build_candidate_implementations()
    ids = [implementation.candidate_id for implementation in implementations]

    assert len(implementations) == 9
    assert ids == APPROVED_CANDIDATE_IDS
    assert "nhlr_06" not in ids

    for implementation in implementations:
        assert implementation.registration_source == "authoritative_candidate_registry"
        assert implementation.implementation_status == IMPLEMENTATION_STATUS
        assert implementation.formula_status == FORMULA_STATUS
        assert implementation.panel_status == PANEL_STATUS
        assert implementation.discovery_status == "DISCOVERY_NOT_EXECUTED"


def test_candidate_registration_helper_exposes_exact_ids():
    assert registered_candidate_ids() == APPROVED_CANDIDATE_IDS
    assert len(set(registered_candidate_ids())) == len(APPROVED_CANDIDATE_IDS)


def test_validate_candidate_implementations_passes_and_detects_drift():
    ok, errors, report = validate_candidate_implementations()
    assert ok, errors
    assert {row["status"] for row in report} == {"PASS"}

    rows = implementation_rows()
    rows[0] = dict(rows[0])
    rows[0]["candidate_id"] = "nhlr_06"

    ok, errors, report = validate_candidate_implementations(rows)
    assert not ok
    assert any("registry_alignment" in error for error in errors)
    assert any("excluded_candidate_not_implemented" in error for error in errors)
    assert any(row["status"] == "FAIL" for row in report)

    rows = implementation_rows()
    rows[0] = dict(rows[0])
    rows[0]["working_name"] = "Drifted Candidate Name"

    ok, errors, report = validate_candidate_implementations(rows)
    assert not ok
    assert any("registry_metadata_consistency" in error for error in errors)
    assert any(row["check_name"] == "registry_metadata_consistency" and row["status"] == "FAIL" for row in report)


def test_export_candidate_implementations_creates_manifest_and_diagnostics():
    res = subprocess.run([*RUNNER, "--export-candidate-implementations"], capture_output=True, text=True)
    assert res.returncode == 0, f"--export-candidate-implementations failed: {res.stderr}\n{res.stdout}"
    assert "CANDIDATE_IMPLEMENTATION_ONLY" in res.stdout
    assert IMPLEMENTATION_FINAL_CLASSIFICATION in res.stdout
    assert "No candidate panels" in res.stdout

    expected_paths = [
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.csv",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.json",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_diagnostics.csv",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_summary.json",
        CANDIDATE_IMPLEMENTATION_DIR / "candidate_registration_map.csv",
    ]
    for path in expected_paths:
        assert path.exists()

    manifest = pd.read_csv(CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.csv")
    assert list(manifest["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert set(manifest["implementation_status"]) == {IMPLEMENTATION_STATUS}
    assert set(manifest["formula_status"]) == {FORMULA_STATUS}
    assert set(manifest["panel_status"]) == {PANEL_STATUS}
    assert "nhlr_06" not in set(manifest["candidate_id"])

    diagnostics = pd.read_csv(CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_diagnostics.csv")
    assert set(diagnostics["status"]) == {"PASS"}

    summary = json.loads(
        (CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_summary.json").read_text(encoding="utf-8")
    )
    assert summary["implemented_candidate_count"] == 9
    assert summary["registry_alignment"] is True
    assert summary["implementation_completeness"] is True
    assert summary["missing_implementations"] == []
    assert summary["excluded_candidate_implemented"] is False

    json_manifest = json.loads(
        (CANDIDATE_IMPLEMENTATION_DIR / "candidate_implementation_manifest.json").read_text(encoding="utf-8")
    )
    assert json_manifest["source_registry_status"] == REGISTRY_STATUS
    assert json_manifest["candidate_panels_generated"] is False
    assert json_manifest["discovery_executed"] is False
    assert json_manifest["ic_calculated"] is False
    assert json_manifest["redundancy_screening_run"] is False
    assert json_manifest["refinement_executed"] is False
    assert json_manifest["validation_executed"] is False
    assert json_manifest["governance_modified"] is False
    assert json_manifest["thresholds_modified"] is False
    assert json_manifest["production_registered"] is False
    assert json_manifest["ml_implemented"] is False


def test_runner_lists_and_validates_candidate_implementations():
    subprocess.run([*RUNNER, "--export-candidate-implementations"], capture_output=True, text=True, check=True)

    list_res = subprocess.run([*RUNNER, "--list-candidate-implementations"], capture_output=True, text=True)
    assert list_res.returncode == 0, list_res.stderr
    for candidate_id in APPROVED_CANDIDATE_IDS:
        assert candidate_id in list_res.stdout
    assert IMPLEMENTATION_STATUS in list_res.stdout

    validate_res = subprocess.run([*RUNNER, "--validate-candidate-implementations"], capture_output=True, text=True)
    assert validate_res.returncode == 0, validate_res.stderr
    assert "validation passed" in validate_res.stdout


def test_candidate_implementation_modes_remain_fail_closed():
    unsupported_modes = [
        "--generate-candidate-panels",
        "--run-discovery",
        "--calculate-ic",
        "--run-redundancy-screening",
        "--run-refinement",
        "--run-validation",
        "--register-production",
        "--implement-ml",
    ]
    for mode in unsupported_modes:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode != 0, f"{mode} unexpectedly succeeded"
        assert "unrecognized arguments" in res.stderr or "usage:" in res.stderr
