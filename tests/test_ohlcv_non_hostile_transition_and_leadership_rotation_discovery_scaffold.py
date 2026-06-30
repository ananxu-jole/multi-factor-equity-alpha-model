import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 import (
    ARTIFACT_DIRS,
    CANDIDATE_INVENTORY_DIR,
    DIAGNOSTICS_DIR,
    DISCOVERY_CATEGORIES,
    DISCOVERY_SUMMARY_DIR,
    FINAL_CLASSIFICATION,
    MANIFESTS_DIR,
    OUT_DIR,
    REDUNDANCY_SCREENING_DIR,
    SCAFFOLD_STATUS,
    validate_scaffold,
    write_scaffold,
)


RUNNER = ["python", "pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py"]


def test_dry_run_creates_scaffold_artifacts_only():
    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--dry-run failed: {res.stderr}\n{res.stdout}"
    assert SCAFFOLD_STATUS in res.stdout
    assert FINAL_CLASSIFICATION in res.stdout
    assert "No discovery" in res.stdout

    for directory in ARTIFACT_DIRS:
        assert directory.is_dir()

    manifest = json.loads((MANIFESTS_DIR / "scaffold_manifest.json").read_text(encoding="utf-8"))
    assert manifest["scaffold_status"] == SCAFFOLD_STATUS
    assert manifest["final_classification"] == FINAL_CLASSIFICATION
    assert manifest["candidate_count"] == 0
    assert manifest["research_results_present"] is False
    assert manifest["candidate_generation_executed"] is False
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


def test_list_discovery_categories_outputs_all_categories():
    res = subprocess.run([*RUNNER, "--list-discovery-categories"], capture_output=True, text=True)
    assert res.returncode == 0, f"--list-discovery-categories failed: {res.stderr}\n{res.stdout}"
    for category in DISCOVERY_CATEGORIES:
        assert category["category_id"] in res.stdout
        assert SCAFFOLD_STATUS in res.stdout


def test_list_deliverables_outputs_scaffold_deliverables():
    res = subprocess.run([*RUNNER, "--list-deliverables"], capture_output=True, text=True)
    assert res.returncode == 0, f"--list-deliverables failed: {res.stderr}\n{res.stdout}"
    assert "runner_scaffold" in res.stdout
    assert "candidate_inventory_manifest" in res.stdout
    assert "diagnostics_placeholders" in res.stdout
    assert SCAFFOLD_STATUS in res.stdout


def test_validate_modes_pass_after_scaffold_write():
    write_scaffold()
    for mode in ["--validate-scaffold", "--validate-artifact-structure"]:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode == 0, f"{mode} failed: {res.stderr}\n{res.stdout}"
        assert "validation passed" in res.stdout

    ok, errors = validate_scaffold()
    assert ok, errors


def test_discovery_categories_and_inventory_manifest_are_placeholders():
    write_scaffold()

    categories = pd.read_csv(CANDIDATE_INVENTORY_DIR / "discovery_categories.csv")
    assert len(categories) == len(DISCOVERY_CATEGORIES)
    assert set(categories["scaffold_status"]) == {SCAFFOLD_STATUS}

    inventory = pd.read_csv(CANDIDATE_INVENTORY_DIR / "candidate_inventory_manifest.csv")
    assert len(inventory) == 1
    assert inventory.loc[0, "inventory_status"] == SCAFFOLD_STATUS
    assert int(inventory.loc[0, "candidate_count"]) == 0
    assert inventory.loc[0, "candidate_generation_executed"] == False
    assert inventory.loc[0, "panel_generation_executed"] == False


def test_diagnostics_placeholders_are_fail_closed():
    write_scaffold()

    scaffold = pd.read_csv(DIAGNOSTICS_DIR / "scaffold_diagnostics.csv")
    assert set(scaffold["scaffold_status"]) == {SCAFFOLD_STATUS}
    assert set(scaffold["research_results"].astype(bool)) == {False}

    guardrails = pd.read_csv(DIAGNOSTICS_DIR / "guardrail_diagnostics.csv")
    assert not guardrails.empty
    assert set(guardrails["scaffold_status"]) == {SCAFFOLD_STATUS}
    assert set(guardrails["executed"].astype(bool)) == {False}
    assert set(guardrails["status"]) == {"BLOCKED_BY_SCAFFOLD"}


def test_redundancy_and_discovery_outputs_are_placeholders_not_results():
    write_scaffold()

    readiness = (DISCOVERY_SUMMARY_DIR / "discovery_readiness_report.md").read_text(encoding="utf-8")
    assert SCAFFOLD_STATUS in readiness
    assert "contains no research results" in readiness
    assert FINAL_CLASSIFICATION in readiness

    summary = json.loads((DISCOVERY_SUMMARY_DIR / "discovery_summary_placeholder.json").read_text(encoding="utf-8"))
    assert summary["scaffold_status"] == SCAFFOLD_STATUS
    assert summary["research_results_present"] is False

    redundancy = pd.read_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening_placeholder.csv")
    assert len(redundancy) == 1
    assert redundancy.loc[0, "scaffold_status"] == SCAFFOLD_STATUS
    assert redundancy.loc[0, "screening_executed"] == False
    assert redundancy.loc[0, "research_results"] == False


def test_fail_closed_unsupported_modes():
    unsupported_modes = [
        "--run-discovery",
        "--generate-candidates",
        "--generate-panels",
        "--calculate-ic",
        "--run-refinement",
        "--run-validation",
        "--production",
    ]
    for mode in unsupported_modes:
        res = subprocess.run([*RUNNER, mode], capture_output=True, text=True)
        assert res.returncode != 0, f"{mode} unexpectedly succeeded"
        assert "unrecognized arguments" in res.stderr or "usage:" in res.stderr


def test_no_candidate_panel_or_ic_artifacts_are_created():
    panel_dir = OUT_DIR / "candidate_panels"
    panel_files_before = sorted(panel_dir.glob("*.parquet")) if panel_dir.exists() else []
    write_scaffold()
    panel_files_after = sorted(panel_dir.glob("*.parquet")) if panel_dir.exists() else []
    assert panel_files_after == panel_files_before

    forbidden_dirs = [OUT_DIR / "ic_discovery", OUT_DIR / "production", OUT_DIR / "validation", OUT_DIR / "refinement"]
    for path in forbidden_dirs:
        assert not path.exists()
