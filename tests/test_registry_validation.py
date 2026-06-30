import subprocess
import sys
from pathlib import Path

import pandas as pd

# Ensure repository root is on sys.path when pytest runs
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.utils.registry_validation import validate_registry_df, RegistryValidationError


DATA_DIR = Path("artifacts/research/alpha_family_diversification_discovery_v1")


def test_registry_validation_passes_for_current_registry():
    registry_path = DATA_DIR / "candidate_inventory" / "candidate_registry.csv"
    df = pd.read_csv(registry_path)
    # should not raise
    validate_registry_df(df)


def test_missing_required_field_fails():
    df = pd.DataFrame([
        {
            "candidate_id": "x1",
            # missing signal_name
            "family": "dispersion",
            "theme": "t",
            "feature_group": "fg",
            "horizon": "h10-h20",
            "redundancy_risk": "medium",
            "research_status": "RESEARCH_ONLY",
            "run_id": "alpha_family_diversification_discovery_v1",
        }
    ])
    try:
        validate_registry_df(df)
    except RegistryValidationError:
        return
    raise AssertionError("Expected RegistryValidationError for missing required field")


def test_duplicate_candidate_id_fails():
    df = pd.DataFrame([
        {"candidate_id": "dup", "signal_name": "s1", "family": "dispersion", "theme": "t", "feature_group": "fg", "horizon": "h10-h20", "redundancy_risk": "medium", "research_status": "RESEARCH_ONLY", "run_id": "r"},
        {"candidate_id": "dup", "signal_name": "s2", "family": "dispersion", "theme": "t", "feature_group": "fg", "horizon": "h10-h20", "redundancy_risk": "medium", "research_status": "RESEARCH_ONLY", "run_id": "r"},
    ])
    try:
        validate_registry_df(df)
    except RegistryValidationError:
        return
    raise AssertionError("Expected RegistryValidationError for duplicate candidate_id")


def test_invalid_redundancy_risk_fails():
    df = pd.DataFrame([
        {"candidate_id": "c1", "signal_name": "s1", "family": "dispersion", "theme": "t", "feature_group": "fg", "horizon": "h10-h20", "redundancy_risk": "ultra", "research_status": "RESEARCH_ONLY", "run_id": "r"},
    ])
    try:
        validate_registry_df(df)
    except RegistryValidationError:
        return
    raise AssertionError("Expected RegistryValidationError for invalid redundancy_risk")


def test_runner_dry_run_succeeds():
    # run the runner's dry-run to ensure validation is wired and passes
    cmd = ["python", "pipelines/run_alpha_family_diversification_discovery_v1.py", "--dry-run"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"dry-run failed: {res.stderr}\n{res.stdout}"
