from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.dispersion_path_dependence_research_module_v1 import IMPLEMENTED_CANDIDATE_IDS
import pipelines.run_dispersion_path_dependence_ic_discovery_v1 as runner


EXPECTED_OUTPUTS = {
    "daily_ic.csv",
    "candidate_horizon_ic_scores.csv",
    "candidate_ic_summary.csv",
    "horizon_summary.csv",
    "family_summary.csv",
    "candidate_rankings.csv",
    "rolling_ic_diagnostics.csv",
    "approved_panel_manifest.csv",
    "manifest.json",
}


@pytest.fixture(scope="module")
def discovery_output(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out_dir = tmp_path_factory.mktemp("dpath_ic_discovery")
    runner.run_ic_discovery(out_dir=out_dir)
    return out_dir


def test_ic_discovery_writes_expected_artifacts_from_audited_panels(discovery_output: Path):
    assert {path.name for path in discovery_output.iterdir() if path.is_file()} == EXPECTED_OUTPUTS

    manifest = json.loads((discovery_output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_panel_root"] == str(runner.SOURCE_PANEL_ROOT)
    assert manifest["approved_candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert manifest["classification"] in {
        "IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES",
        "IC_DISCOVERY_COMPLETE_WITH_NOTES",
        "IC_DISCOVERY_INCONCLUSIVE",
    }
    assert manifest["panel_validation_executed_before_ic"] is True
    assert manifest["ic_discovery_executed"] is True
    assert manifest["panel_generation_executed"] is False
    assert manifest["panels_modified"] is False
    assert manifest["formulas_modified"] is False
    assert manifest["implementation_modified"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False


def test_candidate_horizon_scores_cover_exact_candidates_and_horizons(discovery_output: Path):
    scores = pd.read_csv(discovery_output / "candidate_horizon_ic_scores.csv")

    assert tuple(scores["candidate_id"].drop_duplicates()) == IMPLEMENTED_CANDIDATE_IDS
    assert set(scores["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert len(scores) == len(IMPLEMENTED_CANDIDATE_IDS) * 4
    assert set(scores["primary_horizon"]) == {"h10"}
    assert set(scores["secondary_horizons"]) == {"h5|h20"}
    assert set(scores["expected_sign"]) == {"positive"}
    assert scores["mean_ic"].notna().all()
    assert scores["ic_ir"].notna().all()
    assert scores["positive_ic_rate"].between(0, 1).all()
    assert scores["coverage_ratio"].between(0, 1).all()
    assert scores["turnover_proxy"].notna().all()


def test_candidate_rankings_use_research_review_recommendation_vocabulary(discovery_output: Path):
    rankings = pd.read_csv(discovery_output / "candidate_rankings.csv")

    assert tuple(rankings.sort_values("rank")["candidate_id"]) == tuple(rankings["candidate_id"])
    assert set(rankings["candidate_id"]) == set(IMPLEMENTED_CANDIDATE_IDS)
    assert set(rankings["recommendation"]) <= {"ADVANCE_TO_RESEARCH_REVIEW", "WATCH", "PARK", "REJECT"}
    assert set(rankings["hypothesis_consistency"]) <= {"MATCH", "PARTIAL_MATCH", "MISMATCH"}
    assert set(rankings["expected_primary_horizon"]) == {"h10"}
    assert rankings["observed_strongest_horizon"].isin(["h1", "h5", "h10", "h20"]).all()
    assert rankings["max_abs_internal_diagnostic_corr"].between(0, 1).all()


def test_lineage_and_contamination_metadata_are_preserved(discovery_output: Path):
    daily = pd.read_csv(discovery_output / "daily_ic.csv")
    rankings = pd.read_csv(discovery_output / "candidate_rankings.csv")

    required_daily = {
        "hypothesis",
        "scientific_question",
        "expected_evidence",
        "primary_falsification_criterion",
        "observable_implication",
        "expected_orthogonality",
        "contamination_controls",
        "anchor_comparators",
    }
    assert required_daily.issubset(daily.columns)
    assert daily.groupby("candidate_id")["hypothesis"].nunique().eq(1).all()
    assert daily.groupby("candidate_id")["scientific_question"].nunique().eq(1).all()
    assert rankings["expected_orthogonality"].str.len().gt(20).all()
    assert rankings["contamination_controls"].str.len().gt(20).all()
    assert rankings["anchor_comparators"].str.len().gt(10).all()


def test_approved_panel_manifest_is_copied_without_candidate_drift(discovery_output: Path):
    source_manifest = pd.read_csv(runner.SOURCE_PANEL_ROOT / "panel_manifest.csv")
    approved_manifest = pd.read_csv(discovery_output / "approved_panel_manifest.csv")

    pd.testing.assert_frame_equal(approved_manifest, source_manifest)
    assert tuple(approved_manifest["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert int(approved_manifest["duplicate_key_count"].sum()) == 0
    assert int(approved_manifest["blocked_candidate_count"].sum()) == 0
