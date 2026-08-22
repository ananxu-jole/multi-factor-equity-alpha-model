from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.event_clustering_research_module_v1 import IMPLEMENTED_CANDIDATE_IDS
import pipelines.run_event_clustering_ic_discovery_v1 as runner


EXPECTED_OUTPUTS = {
    "daily_ic.csv",
    "candidate_ic_summary.csv",
    "candidate_horizon_summary.csv",
    "candidate_rankings.csv",
    "rolling_stability_summary.csv",
    "ic_discovery_manifest.json",
}


@pytest.fixture(scope="module")
def discovery_output(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out_dir = tmp_path_factory.mktemp("event_clustering_ic_discovery")
    runner.run_ic_discovery(out_dir=out_dir)
    return out_dir


def test_ic_discovery_writes_only_expected_artifacts_from_audited_panels(discovery_output: Path):
    assert {path.name for path in discovery_output.iterdir() if path.is_file()} == EXPECTED_OUTPUTS

    manifest = json.loads((discovery_output / "ic_discovery_manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_panel_root"] == str(runner.SOURCE_PANEL_ROOT)
    assert manifest["approved_audit"] == str(runner.APPROVED_AUDIT_PATH)
    assert manifest["approved_candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert manifest["classification"] in {"IC_DISCOVERY_COMPLETE", "IC_DISCOVERY_INCOMPLETE"}
    assert manifest["panel_audit_approved_before_ic"] is True
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
    assert set(manifest["input_lineage_checksums"]["approved_panel_parquet_sha256"]) == {
        "ecluster_01_signal_panel.parquet",
        "ecluster_02_signal_panel.parquet",
        "ecluster_03_signal_panel.parquet",
        "ecluster_04_signal_panel.parquet",
        "ecluster_05_signal_panel.parquet",
    }


def test_candidate_horizon_summary_covers_exact_candidates_and_horizons(discovery_output: Path):
    scores = pd.read_csv(discovery_output / "candidate_horizon_summary.csv")

    assert tuple(scores["candidate_id"].drop_duplicates()) == IMPLEMENTED_CANDIDATE_IDS
    assert set(scores["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert len(scores) == len(IMPLEMENTED_CANDIDATE_IDS) * 4
    assert set(scores["expected_sign"]) == {"positive"}
    assert scores["mean_ic"].notna().all()
    assert scores["ic_ir"].notna().all()
    assert scores["positive_ic_rate"].between(0, 1).all()
    assert scores["coverage_ratio"].between(0, 1).all()
    assert scores["turnover_proxy"].notna().all()


def test_rankings_use_required_mechanical_recommendation_vocabulary(discovery_output: Path):
    rankings = pd.read_csv(discovery_output / "candidate_rankings.csv")

    assert tuple(rankings.sort_values("rank")["candidate_id"]) == tuple(rankings["candidate_id"])
    assert set(rankings["candidate_id"]) == set(IMPLEMENTED_CANDIDATE_IDS)
    assert set(rankings["recommendation"]) <= {"ADVANCE_TO_RESEARCH_REVIEW", "WATCH", "PARK", "REJECT"}
    assert set(rankings["hypothesis_consistency"]) <= {"MATCH", "PARTIAL_MATCH", "MISMATCH"}
    assert rankings["expected_primary_horizon"].isin(["h5", "h10"]).all()
    assert rankings["observed_primary_horizon"].isin(["h1", "h5", "h10", "h20"]).all()
    assert rankings["max_abs_internal_diagnostic_corr"].between(0, 1).all()


def test_lineage_contamination_and_anchor_metadata_are_preserved(discovery_output: Path):
    daily = pd.read_csv(discovery_output / "daily_ic.csv")
    rankings = pd.read_csv(discovery_output / "candidate_rankings.csv")

    required_daily = {
        "scientific_lineage",
        "contamination_metadata",
        "isolated_event_anchor",
        "scientific_question",
        "expected_evidence",
        "stop_conditions",
        "anchor_comparators",
    }
    assert required_daily.issubset(daily.columns)
    assert daily.groupby("candidate_id")["scientific_lineage"].nunique().eq(1).all()
    assert daily.groupby("candidate_id")["scientific_question"].nunique().eq(1).all()
    assert rankings["contamination_metadata"].str.contains("vov", regex=False).all()
    assert rankings["contamination_metadata"].str.contains("dispersion_path_dependence", regex=False).all()
    assert rankings["isolated_event_anchor"].notna().all()
    assert rankings["anchor_comparators"].str.len().gt(10).all()


def test_daily_ic_and_rolling_stability_shapes(discovery_output: Path):
    daily = pd.read_csv(discovery_output / "daily_ic.csv")
    rolling = pd.read_csv(discovery_output / "rolling_stability_summary.csv")

    assert set(daily["candidate_id"]) == set(IMPLEMENTED_CANDIDATE_IDS)
    assert set(daily["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert daily["ic"].notna().any()
    assert set(rolling["candidate_id"]) == set(IMPLEMENTED_CANDIDATE_IDS)
    assert set(rolling["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert "rolling_252_mean_ic_latest" in rolling.columns
    assert rolling["scored_date_count"].gt(0).all()
