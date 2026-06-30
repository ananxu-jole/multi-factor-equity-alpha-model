import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


RUNNER = ["python", "pipelines/run_alpha_family_diversification_discovery_v1.py"]
OUT_DIR = Path("artifacts/research/alpha_family_diversification_discovery_v1")
CANDIDATE_PANELS_DIR = OUT_DIR / "candidate_panels"
DISCOVERY_SUMMARY_DIR = OUT_DIR / "discovery_summary"
REDUNDANCY_SCREENING_DIR = OUT_DIR / "redundancy_screening"
GOVERNANCE_REVIEW_PATH = OUT_DIR / "governance_review" / "framework_governance_review.csv"
REQUIRED_PANEL_COLUMNS = {"date", "ticker", "candidate_id", "signal_value", "family", "theme", "horizon"}


def _mtime(path: Path) -> float | None:
    return path.stat().st_mtime if path.exists() else None


@pytest.fixture(scope="module")
def research_run_result():
    governance_mtime_before = _mtime(GOVERNANCE_REVIEW_PATH)
    res = subprocess.run([*RUNNER, "--run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--run failed: {res.stderr}\n{res.stdout}"
    return {
        "stdout": res.stdout,
        "governance_mtime_before": governance_mtime_before,
        "governance_mtime_after": _mtime(GOVERNANCE_REVIEW_PATH),
    }


def test_run_creates_candidate_panel_files_with_required_columns(research_run_result):
    manifest_path = DISCOVERY_SUMMARY_DIR / "panel_manifest.csv"
    summary_path = DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv"
    assert manifest_path.exists()
    assert summary_path.exists()

    manifest = pd.read_csv(manifest_path)
    summary = pd.read_csv(summary_path)
    panel_files = sorted(CANDIDATE_PANELS_DIR.glob("*.parquet"))

    assert len(manifest) == 17
    assert len(summary) == 17
    assert len(panel_files) == 17
    assert set(manifest["generation_status"]) == {"generated"}

    sample_panel = pd.read_parquet(manifest.loc[0, "panel_path"])
    assert REQUIRED_PANEL_COLUMNS.issubset(sample_panel.columns)
    assert sample_panel["candidate_id"].nunique() == 1
    assert sample_panel["signal_value"].notna().any()


def test_run_refreshes_statistical_screening_from_generated_panels(research_run_result):
    stat_path = REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv"
    assert stat_path.exists()
    stat = pd.read_csv(stat_path)

    assert not stat.empty
    assert "missing_candidate_panel" not in set(stat["diagnostic_status"])
    assert (stat["diagnostic_status"] == "computed").any()
    assert stat["value_correlation"].notna().any()
    assert stat["rank_correlation"].notna().any()


def test_run_does_not_touch_governance_or_production_paths(research_run_result):
    assert research_run_result["governance_mtime_before"] == research_run_result["governance_mtime_after"]
    manifest = pd.read_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")

    assert manifest["panel_path"].str.startswith(str(CANDIDATE_PANELS_DIR)).all()
    assert not manifest["panel_path"].str.startswith("configs/").any()
    assert not manifest["panel_path"].str.startswith("sql/").any()
    assert "no validation" in research_run_result["stdout"]
    assert "production registration" in research_run_result["stdout"]


def test_dry_run_does_not_rewrite_candidate_panel_outputs(research_run_result):
    manifest_path = DISCOVERY_SUMMARY_DIR / "panel_manifest.csv"
    manifest_mtime_before = _mtime(manifest_path)
    panel_mtime_before = _mtime(next(iter(sorted(CANDIDATE_PANELS_DIR.glob("*.parquet")))))

    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--dry-run failed: {res.stderr}\n{res.stdout}"

    assert _mtime(manifest_path) == manifest_mtime_before
    assert _mtime(next(iter(sorted(CANDIDATE_PANELS_DIR.glob("*.parquet"))))) == panel_mtime_before
