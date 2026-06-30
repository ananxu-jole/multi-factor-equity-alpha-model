import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_rank_coherence_family_discovery_v1 import HARD_MAX_CANDIDATES, candidate_registry


RUNNER = ["python", "pipelines/run_rank_coherence_family_discovery_v1.py"]
OUT_DIR = Path("artifacts/research/rank_coherence_family_discovery_v1")
CANDIDATE_PANELS_DIR = OUT_DIR / "candidate_panels"
DISCOVERY_SUMMARY_DIR = OUT_DIR / "discovery_summary"
REDUNDANCY_SCREENING_DIR = OUT_DIR / "redundancy_screening"
GOVERNANCE_REVIEW_PATH = OUT_DIR / "governance_review" / "research_only_guardrail_review.csv"
REQUIRED_PANEL_COLUMNS = {"date", "ticker", "candidate_id", "signal_value", "family", "theme", "horizon"}


def _mtime(path: Path) -> float | None:
    return path.stat().st_mtime if path.exists() else None


@pytest.fixture(scope="module")
def panel_generation_result():
    governance_mtime_before = _mtime(GOVERNANCE_REVIEW_PATH)
    res = subprocess.run([*RUNNER, "--run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--run failed: {res.stderr}\n{res.stdout}"
    return {
        "stdout": res.stdout,
        "governance_mtime_before": governance_mtime_before,
        "governance_mtime_after": _mtime(GOVERNANCE_REVIEW_PATH),
    }


def test_run_creates_exactly_10_candidate_panel_files(panel_generation_result):
    registry = candidate_registry()
    assert len(registry) == 10
    assert len(registry) <= HARD_MAX_CANDIDATES

    panel_files = sorted(CANDIDATE_PANELS_DIR.glob("*.parquet"))
    metadata_files = sorted(CANDIDATE_PANELS_DIR.glob("*.metadata.json"))
    assert len(panel_files) == 10
    assert len(metadata_files) == 10

    manifest = pd.read_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
    summary = pd.read_csv(DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv")
    assert len(manifest) == 10
    assert len(summary) == 10
    assert set(manifest["generation_status"]) == {"generated"}


def test_panel_files_have_required_long_form_columns(panel_generation_result):
    manifest = pd.read_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
    for panel_path in manifest["panel_path"]:
        panel = pd.read_parquet(panel_path)
        assert REQUIRED_PANEL_COLUMNS.issubset(panel.columns)
        assert panel["candidate_id"].nunique() == 1
        assert panel["signal_value"].notna().any()


def test_statistical_redundancy_screening_uses_generated_panels(panel_generation_result):
    stat_path = REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv"
    assert stat_path.exists()
    stat = pd.read_csv(stat_path)
    assert not stat.empty
    assert "missing_candidate_panel" not in set(stat["diagnostic_status"])
    assert (stat["diagnostic_status"] == "computed").any()
    assert stat["value_correlation"].notna().any()
    assert stat["rank_correlation"].notna().any()


def test_dry_run_does_not_generate_or_rewrite_panels_after_run(panel_generation_result):
    panel_files = sorted(CANDIDATE_PANELS_DIR.glob("*.parquet"))
    mtimes_before = {path.name: path.stat().st_mtime for path in panel_files}
    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--dry-run failed: {res.stderr}\n{res.stdout}"
    panel_files_after = sorted(CANDIDATE_PANELS_DIR.glob("*.parquet"))
    mtimes_after = {path.name: path.stat().st_mtime for path in panel_files_after}
    assert mtimes_after == mtimes_before


def test_guardrails_and_production_paths(panel_generation_result):
    res = subprocess.run([*RUNNER, "--run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--run failed: {res.stderr}\n{res.stdout}"
    assert "no discovery scoring" in res.stdout
    assert "production registration" in res.stdout

    manifest = json.loads((OUT_DIR / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["panel_generation_executed"] is True
    assert manifest["discovery_executed"] is False
    assert manifest["ic_scoring_executed"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["ml_integration"] is False
    assert manifest["candidate_promotion_or_demotion"] is False

    panel_manifest = pd.read_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
    assert panel_manifest["panel_path"].str.startswith(str(CANDIDATE_PANELS_DIR)).all()
    assert not panel_manifest["panel_path"].str.startswith("configs/").any()
    assert not panel_manifest["panel_path"].str.startswith("sql/").any()
