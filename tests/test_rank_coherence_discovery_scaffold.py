import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.run_rank_coherence_family_discovery_v1 import (
    HARD_MAX_CANDIDATES,
    REQUIRED_REGISTRY_COLUMNS,
    candidate_registry,
)


RUNNER = ["python", "pipelines/run_rank_coherence_family_discovery_v1.py"]
OUT_DIR = Path("artifacts/research/rank_coherence_family_discovery_v1")
REQUIRED_DIRS = [
    "candidate_inventory",
    "candidate_panels",
    "discovery_summary",
    "diagnostics",
    "redundancy_screening",
    "ic_discovery",
    "governance_review",
]


def test_candidate_registry_shape_and_required_columns():
    registry = candidate_registry()
    assert len(registry) == 10
    assert len(registry) <= HARD_MAX_CANDIDATES
    assert REQUIRED_REGISTRY_COLUMNS.issubset(registry.columns)
    assert set(registry["family"]) == {"rank_coherence"}
    assert set(registry["research_status"]) == {"RESEARCH_ONLY"}


def test_list_candidates_works():
    res = subprocess.run([*RUNNER, "--list-candidates"], capture_output=True, text=True)
    assert res.returncode == 0, f"--list-candidates failed: {res.stderr}\n{res.stdout}"
    assert "rank_coherence_leadership_stability_01" in res.stdout
    assert "rank_coherence_regime_independent_02" in res.stdout


def test_dry_run_creates_scaffold_artifacts_without_panels():
    before_panel_files = sorted((OUT_DIR / "candidate_panels").glob("*.parquet"))
    before_panel_mtimes = {path.name: path.stat().st_mtime for path in before_panel_files}

    res = subprocess.run([*RUNNER, "--dry-run"], capture_output=True, text=True)
    assert res.returncode == 0, f"--dry-run failed: {res.stderr}\n{res.stdout}"
    assert "no panel generation" in res.stdout

    for name in REQUIRED_DIRS:
        assert (OUT_DIR / name).is_dir()

    registry_path = OUT_DIR / "candidate_inventory" / "candidate_registry.csv"
    manifest_path = OUT_DIR / "manifest.json"
    summary_path = OUT_DIR / "discovery_summary" / "framework_scaffold_summary.md"
    metadata_screening_path = OUT_DIR / "redundancy_screening" / "metadata_redundancy_screening.csv"
    stat_screening_path = OUT_DIR / "redundancy_screening" / "statistical_redundancy_screening.csv"

    assert registry_path.exists()
    assert manifest_path.exists()
    assert summary_path.exists()
    assert metadata_screening_path.exists()
    assert stat_screening_path.exists()

    registry = pd.read_csv(registry_path)
    assert len(registry) == 10
    assert REQUIRED_REGISTRY_COLUMNS.issubset(registry.columns)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["candidate_count"] == 10
    assert manifest["hard_max_candidate_count"] == 12
    assert manifest["panel_generation_executed"] is False
    assert manifest["discovery_executed"] is False
    assert manifest["ic_scoring_executed"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["ml_integration"] is False
    assert manifest["candidate_promotion_or_demotion"] is False

    after_panel_files = sorted((OUT_DIR / "candidate_panels").glob("*.parquet"))
    after_panel_mtimes = {path.name: path.stat().st_mtime for path in after_panel_files}
    assert [path.name for path in after_panel_files] == [path.name for path in before_panel_files]
    assert after_panel_mtimes == before_panel_mtimes
