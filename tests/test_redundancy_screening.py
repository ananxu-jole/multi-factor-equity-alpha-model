import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.utils.redundancy_screening import (
    HIGH_METADATA_REDUNDANCY,
    LOW_METADATA_REDUNDANCY,
    REVIEW_REQUIRED,
    STATISTICAL_REDUNDANCY_COLUMNS,
    StatisticalRedundancyConfig,
    screen_registry_df,
    screen_statistical_redundancy_from_cache,
)


def test_low_risk_candidate_is_low():
    df = pd.DataFrame([
        {"candidate_id": "c1", "signal_name": "s1", "family": "fA", "theme": "t1", "feature_group": "fg1", "horizon": "h1", "redundancy_risk": "low", "research_status": "RESEARCH_ONLY", "run_id": "r"},
        {"candidate_id": "c2", "signal_name": "s2", "family": "fB", "theme": "t2", "feature_group": "fg2", "horizon": "h2", "redundancy_risk": "low", "research_status": "RESEARCH_ONLY", "run_id": "r"},
    ])
    out = screen_registry_df(df)
    assert set(out.columns).issuperset({"candidate_id","advisory_redundancy_class","triggered_checks","review_required"})
    assert out.loc[out.candidate_id == "c1", "advisory_redundancy_class"].iloc[0] == LOW_METADATA_REDUNDANCY


def test_stress_participation_triggers_review():
    df = pd.DataFrame([
        {"candidate_id": "c_stress", "signal_name": "s_stress", "family": "fA", "theme": "stress_recovery", "feature_group": "fg", "horizon": "h1", "redundancy_risk": "low", "research_status": "RESEARCH_ONLY", "run_id": "r"},
        {"candidate_id": "c_other", "signal_name": "s_other", "family": "fB", "theme": "t2", "feature_group": "fg2", "horizon": "h2", "redundancy_risk": "low", "research_status": "RESEARCH_ONLY", "run_id": "r"},
    ])
    out = screen_registry_df(df)
    assert out.loc[out.candidate_id == "c_stress", "advisory_redundancy_class"].iloc[0] == REVIEW_REQUIRED
    assert bool(out.loc[out.candidate_id == "c_stress", "review_required"].iloc[0]) is True


def test_overlapping_family_increases_redundancy():
    df = pd.DataFrame([
        {"candidate_id": "a1", "signal_name": "s1", "family": "dispersion", "theme": "X", "feature_group": "fg", "horizon": "h1", "redundancy_risk": "low", "research_status": "RESEARCH_ONLY", "run_id": "r"},
        {"candidate_id": "a2", "signal_name": "s2", "family": "dispersion", "theme": "X", "feature_group": "fg", "horizon": "h1", "redundancy_risk": "medium", "research_status": "RESEARCH_ONLY", "run_id": "r"},
    ])
    out = screen_registry_df(df)
    # at least one should be moderate or high
    classes = set(out["advisory_redundancy_class"].tolist())
    assert HIGH_METADATA_REDUNDANCY in classes or "MODERATE_METADATA_REDUNDANCY" in classes


def test_runner_dry_run_writes_screening_file():
    import subprocess
    cmd = ["python", "pipelines/run_alpha_family_diversification_discovery_v1.py", "--dry-run"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    out_path = Path("artifacts/research/alpha_family_diversification_discovery_v1/redundancy_screening/redundancy_screening.csv")
    assert out_path.exists()
    df = pd.read_csv(out_path)
    assert set(["candidate_id","family","theme","horizon","feature_group","redundancy_risk","advisory_redundancy_class","triggered_checks","review_required","notes"]).issubset(set(df.columns))


def test_statistical_screening_computes_value_and_rank_correlations(tmp_path):
    panel_dir = tmp_path / "panels"
    panel_dir.mkdir()
    dates = pd.date_range("2024-01-01", periods=3, freq="D", name="Date")
    base = pd.DataFrame(
        {
            "AAA": [1.0, 2.0, 3.0],
            "BBB": [2.0, 3.0, 4.0],
            "CCC": [3.0, 4.0, 5.0],
        },
        index=dates,
    )
    same_rank_scaled = base * 10.0
    base.to_parquet(panel_dir / "candidate_signal.parquet")
    same_rank_scaled.to_parquet(panel_dir / "comparison_signal.parquet")
    (panel_dir / "candidate_signal.metadata.json").write_text('{"created_at":"2026-06-17T00:00:00Z"}')
    (panel_dir / "comparison_signal.metadata.json").write_text('{"created_at":"2026-06-17T00:00:00Z"}')

    registry = pd.DataFrame(
        [
            {
                "candidate_id": "candidate_1",
                "signal_name": "candidate_signal",
            }
        ]
    )

    out = screen_statistical_redundancy_from_cache(
        registry,
        comparison_signal_names=["comparison_signal"],
        config=StatisticalRedundancyConfig(panel_dir=panel_dir, min_overlap_observations=2),
    )

    assert list(out.columns) == STATISTICAL_REDUNDANCY_COLUMNS
    row = out.iloc[0]
    assert row["diagnostic_status"] == "computed"
    assert row["overlap_observations"] == 9
    assert row["overlap_dates"] == 3
    assert row["overlap_tickers"] == 3
    assert abs(row["value_correlation"] - 1.0) < 1e-12
    assert abs(row["rank_correlation"] - 1.0) < 1e-12
    assert "threshold" not in row["notes"]


def test_statistical_screening_reports_missing_candidate_panel(tmp_path):
    registry = pd.DataFrame(
        [
            {
                "candidate_id": "candidate_1",
                "signal_name": "not_cached_yet",
            }
        ]
    )

    out = screen_statistical_redundancy_from_cache(
        registry,
        comparison_signal_names=["comparison_signal"],
        config=StatisticalRedundancyConfig(panel_dir=tmp_path),
    )

    assert list(out.columns) == STATISTICAL_REDUNDANCY_COLUMNS
    row = out.iloc[0]
    assert row["diagnostic_status"] == "missing_candidate_panel"
    assert row["value_correlation"] is None
    assert row["rank_correlation"] is None
    assert row["overlap_observations"] == 0


def test_runner_dry_run_writes_statistical_screening_file():
    import subprocess
    cmd = ["python", "pipelines/run_alpha_family_diversification_discovery_v1.py", "--dry-run"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    out_path = Path("artifacts/research/alpha_family_diversification_discovery_v1/redundancy_screening/statistical_redundancy_screening.csv")
    assert out_path.exists()
    df = pd.read_csv(out_path)
    assert set(STATISTICAL_REDUNDANCY_COLUMNS).issubset(set(df.columns))
    assert "promotion_decision" not in df.columns
    assert "validation_status" not in df.columns
