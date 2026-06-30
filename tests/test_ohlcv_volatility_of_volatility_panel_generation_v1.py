from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    IMPLEMENTED_CANDIDATE_IDS,
    RUN_ID,
)
import pipelines.run_ohlcv_volatility_of_volatility_panel_generation_v1 as runner


def _synthetic_ohlcv(n_dates: int = 95, n_tickers: int = 60) -> pd.DataFrame:
    dates = pd.bdate_range("2025-01-02", periods=n_dates)
    rows = []
    for ticker_idx in range(n_tickers):
        ticker = f"T{ticker_idx:03d}"
        base = 25.0 + ticker_idx * 0.2
        for date_idx, date in enumerate(dates):
            wave = np.sin(date_idx / 5.0 + ticker_idx / 9.0)
            fast_wave = np.cos(date_idx / 2.5 + ticker_idx / 11.0)
            trend = 0.018 * date_idx * (1.0 + ticker_idx / 300.0)
            close = base + trend + wave * (0.8 + ticker_idx / 250.0) + fast_wave * 0.12
            open_ = close * (1.0 + 0.0015 * np.cos(date_idx / 4.0 + ticker_idx))
            high = max(open_, close) * (1.0 + 0.012 + 0.001 * (ticker_idx % 4))
            low = min(open_, close) * (1.0 - 0.011 - 0.001 * (ticker_idx % 5))
            volume = 120_000 + 800 * ticker_idx + 150 * date_idx + 500 * abs(wave)
            rows.append(
                {
                    "date": date,
                    "ticker": ticker,
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                }
            )
    return pd.DataFrame(rows)


def test_write_vov_panel_artifacts_creates_per_candidate_panels_and_manifests(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)

    manifest, summary = runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    assert tuple(manifest["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert tuple(summary["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert (artifact_root / "metadata.json").exists()
    assert (artifact_root / "panel_manifest.csv").exists()
    assert (artifact_root / "panel_generation_summary.csv").exists()
    assert (artifact_root / "panel_generation_manifest.json").exists()
    assert (artifact_root / "schema_validation_report.csv").exists()

    panel_files = sorted(artifact_root.glob("vov_*_signal_panel.parquet"))
    assert len(panel_files) == 5
    assert {path.name.split("_signal_panel.parquet")[0] for path in panel_files} == set(IMPLEMENTED_CANDIDATE_IDS)

    sample = pd.read_parquet(artifact_root / "vov_04_signal_panel.parquet")
    assert list(sample.columns) == runner.PANEL_COLUMNS
    assert set(sample["candidate_id"]) == {"vov_04"}
    assert set(sample["source_spec_id"]) == {"vov_04_vov_slope_divergence"}
    assert set(sample["module_id"]) == {RUN_ID}
    assert set(sample["timing_policy"]) == {runner.TIMING_POLICY}
    assert not sample[["date", "ticker", "candidate_id"]].duplicated().any()
    assert sample["signal_value"].notna().any()

    metadata = json.loads((artifact_root / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert metadata["panel_generation_executed"] is True
    assert metadata["ic_scoring_executed"] is False
    assert metadata["discovery_executed"] is False
    assert metadata["validation_executed"] is False
    assert metadata["governance_modified"] is False
    assert metadata["production_registration"] is False
    assert metadata["ml_integration"] is False

    generation_manifest = json.loads((artifact_root / "panel_generation_manifest.json").read_text(encoding="utf-8"))
    assert generation_manifest["classification"] == runner.PANEL_GENERATION_CLASSIFICATION
    assert generation_manifest["panel_shape"] == runner.PANEL_SHAPE
    assert generation_manifest["timing_policy"] == runner.TIMING_POLICY
    assert generation_manifest["activation_neutralization"] == runner.ACTIVATION_NEUTRALIZATION


def test_validate_vov_panel_artifacts_passes_after_generation(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    ok, errors = runner.validate_vov_panel_artifacts(artifact_root)

    assert ok, errors


def test_duplicate_prevention_rejects_duplicate_candidate_rows(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "vov_01_signal_panel.parquet")
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)

    errors = runner.validate_candidate_panel_frame(duplicated, "vov_01")

    assert any("duplicate panel rows" in error for error in errors)


def test_activation_semantics_distinguish_inactive_zero_from_missing(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "vov_01_signal_panel.parquet")
    inactive = panel[(~panel["is_active"]) & panel["pre_activation_raw_score"].notna()]
    warmup = panel[panel["pre_activation_raw_score"].isna()]

    assert not inactive.empty
    assert (inactive["raw_score"] == 0.0).all()
    assert set(inactive["missing_reason"].dropna()) == {"inactive_zeroed"}
    assert not warmup.empty
    assert warmup["raw_score"].isna().all()
    assert warmup["signal_value"].isna().all()


def test_timing_policy_and_family_b_c_guardrails_are_manifested(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    manifest = pd.read_csv(artifact_root / "panel_manifest.csv")
    validation = pd.read_csv(artifact_root / "schema_validation_report.csv")

    assert set(manifest["timing_policy"]) == {runner.TIMING_POLICY}
    assert not manifest["candidate_id"].str.startswith(("dpath_", "ecluster_")).any()
    assert set(validation["family_b_c_status"]) == {"PASS"}
    assert set(validation["timing_status"]) == {"PASS"}


def test_validation_fails_if_panel_manifest_references_family_b_candidate(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)
    panel = pd.read_parquet(artifact_root / "vov_01_signal_panel.parquet")
    bad_panel = panel.assign(candidate_id="dpath_01")

    errors = runner.validate_candidate_panel_frame(bad_panel, "vov_01")

    assert any("candidate_id values do not match" in error for error in errors)
    assert any("Family B/C" in error for error in errors)


def test_runner_validate_only_mode_passes_after_generation(tmp_path, monkeypatch, capsys):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_vov_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    monkeypatch.setattr(sys, "argv", ["runner", "--artifact-root", str(artifact_root), "--validate-only"])

    assert runner.main() == 0
    assert "validation passed" in capsys.readouterr().out
