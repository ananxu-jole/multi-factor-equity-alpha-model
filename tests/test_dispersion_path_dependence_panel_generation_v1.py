from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.dispersion_path_dependence_research_module_v1 import (
    IMPLEMENTED_CANDIDATE_IDS,
    MODULE_ID,
    SPEC_ID,
)
import pipelines.run_dispersion_path_dependence_panel_generation_v1 as runner


def _synthetic_ohlcv(n_dates: int = 560, n_tickers: int = 60) -> pd.DataFrame:
    dates = pd.date_range("2022-01-03", periods=n_dates, freq="B")
    rows = []
    for j in range(n_tickers):
        ticker = f"T{j:03d}"
        base = 25.0 + j * 0.4
        amplitude = 0.35 + (j % 11) * 0.045
        for i, date in enumerate(dates):
            regime_wave = np.sin(i / 13.0) * np.cos(j / 9.0)
            local_wave = np.sin(i / (4.0 + (j % 5) * 0.3) + j / 6.0)
            slow_trend = 0.012 * i + 0.004 * j * np.sin(i / 41.0)
            shock = 0.35 * np.sin(i / 29.0 + j / 4.0) if 260 <= i <= 430 else 0.0
            close = max(base + slow_trend + amplitude * local_wave + regime_wave + shock, 2.0)
            open_ = close * (1.0 + 0.0025 * np.cos(i / 7.0 + j))
            spread = 0.008 + 0.0015 * (j % 7) + 0.002 * abs(np.sin(i / 17.0))
            high = max(open_, close) * (1.0 + spread)
            low = min(open_, close) * (1.0 - spread)
            volume = 150_000 + 1_500 * j + 400 * i + 3_000 * abs(local_wave) + 1_500 * abs(shock)
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


def test_write_dpath_panel_artifacts_creates_exact_panels_and_manifests(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)

    manifest, summary = runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    assert tuple(manifest["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert tuple(summary["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert {path.name for path in artifact_root.iterdir() if path.is_file()} == set(runner.REQUIRED_ARTIFACTS)

    panel_files = sorted(artifact_root.glob("*_signal_panel.parquet"))
    assert [path.name for path in panel_files] == [
        "dpath_01_signal_panel.parquet",
        "dpath_02_signal_panel.parquet",
        "dpath_03_signal_panel.parquet",
        "dpath_04_signal_panel.parquet",
    ]

    sample = pd.read_parquet(artifact_root / "dpath_02_signal_panel.parquet")
    assert list(sample.columns) == runner.PANEL_COLUMNS
    assert set(sample["candidate_id"]) == {"dpath_02_disagreement_vol_stress_divergence"}
    assert set(sample["module_id"]) == {MODULE_ID}
    assert set(sample["spec_id"]) == {SPEC_ID}
    assert set(sample["created_by_spec"]) == {SPEC_ID}
    assert set(sample["timing_policy"]) == {runner.TIMING_POLICY}
    assert not sample[["date", "ticker", "candidate_id"]].duplicated().any()
    assert sample["signal_value"].notna().any()

    metadata = json.loads((artifact_root / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert metadata["candidate_count"] == 4
    assert metadata["artifact_root"] == str(artifact_root)
    assert metadata["panel_generation_executed"] is True
    assert metadata["ic_scoring_executed"] is False
    assert metadata["discovery_executed"] is False
    assert metadata["refinement_executed"] is False
    assert metadata["validation_executed"] is False
    assert metadata["governance_modified"] is False
    assert metadata["production_registration"] is False
    assert metadata["thresholds_modified"] is False
    assert metadata["ml_integration"] is False


def test_validate_dpath_panel_artifacts_passes_after_generation(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    ok, errors = runner.validate_dpath_panel_artifacts(artifact_root)

    assert ok, errors


def test_validation_fails_on_unexpected_or_blocked_artifacts(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "dpath_01_signal_panel.parquet")
    panel.to_parquet(artifact_root / "dpath_05_signal_panel.parquet", index=False)

    ok, errors = runner.validate_dpath_panel_artifacts(artifact_root)

    assert not ok
    assert any("unexpected panel parquet" in error for error in errors)
    assert any("unexpected artifact file" in error for error in errors)


def test_duplicate_prevention_rejects_duplicate_candidate_rows(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "dpath_01_signal_panel.parquet")
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)

    errors = runner.validate_candidate_panel_frame(duplicated, "dpath_01_relapse_resilience_after_calm")

    assert any("duplicate panel rows" in error for error in errors)


def test_blocked_candidate_rows_are_rejected(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "dpath_01_signal_panel.parquet")
    bad_panel = panel.assign(candidate_id="dpath_05_smooth_versus_burst_resolution")

    errors = runner.validate_candidate_panel_frame(bad_panel, "dpath_01_relapse_resilience_after_calm")

    assert any("candidate_id values do not match" in error for error in errors)
    assert any("blocked candidate appeared" in error for error in errors)


def test_activation_neutralization_and_warmup_semantics(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "dpath_03_signal_panel.parquet")
    inactive = panel[(~panel["is_active"]) & panel["pre_activation_raw_score"].notna()]
    warmup = panel[~panel["feature_warmup_complete"]]

    assert not inactive.empty
    assert (inactive["signal_value"] == 0.5).all()
    assert (inactive["raw_score"] == 0.5).all()
    assert set(inactive["missing_reason"].dropna()) == {"inactive_neutralized"}
    assert not warmup.empty
    assert warmup["signal_value"].isna().all()


def test_runner_validate_only_mode_passes_after_generation(tmp_path, monkeypatch, capsys):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_dpath_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    monkeypatch.setattr(sys, "argv", ["runner", "--artifact-root", str(artifact_root), "--validate-only"])

    assert runner.main() == 0
    assert "validation passed" in capsys.readouterr().out
