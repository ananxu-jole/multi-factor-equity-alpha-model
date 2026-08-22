from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.event_clustering_research_module_v1 import IMPLEMENTED_CANDIDATE_IDS, MODULE_ID
import pipelines.run_event_clustering_panel_generation_v1 as runner


def _synthetic_ohlcv(n_dates: int = 150, n_tickers: int = 45) -> pd.DataFrame:
    dates = pd.date_range("2023-01-03", periods=n_dates, freq="B")
    rows = []
    for j in range(n_tickers):
        ticker = f"T{j:03d}"
        price = 20.0 + j * 0.35
        for i, date in enumerate(dates):
            base_ret = 0.0015 * np.sin(i / 5.0 + j / 7.0) + 0.0008 * np.cos(i / 11.0 + j)
            cluster_pulse = 0.0
            if i in {70, 71, 73, 95, 96, 101, 122, 123}:
                cluster_pulse += 0.030 * ((j % 5) - 2) / 2.0
            if i in {80, 81, 82, 110} and j % 3 == 0:
                cluster_pulse -= 0.025
            ret = base_ret + cluster_pulse
            open_ = price * (1.0 + 0.002 * np.cos(i / 4.0 + j))
            close = max(price * (1.0 + ret), 1.0)
            event_spread = 0.010 + 0.003 * (j % 4)
            if i in {70, 71, 73, 80, 81, 82, 95, 96, 101, 110, 122, 123}:
                event_spread += 0.035 + 0.002 * (j % 6)
            high = max(open_, close) * (1.0 + event_spread)
            low = min(open_, close) * (1.0 - event_spread)
            volume = 100_000 + 2_000 * j + 300 * i + 4_000 * abs(np.sin(i / 6.0 + j))
            if i in {70, 71, 73, 95, 96, 101, 122, 123}:
                volume *= 2.8 + 0.05 * (j % 7)
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
            price = close
    return pd.DataFrame(rows)


def test_write_event_clustering_panel_artifacts_creates_exact_panels_manifests_and_checksums(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)

    manifest, summary = runner.write_event_clustering_panel_artifacts(
        source_path,
        artifact_root=artifact_root,
        rank_min_count=15,
    )

    assert tuple(manifest["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert tuple(summary["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert {path.name for path in artifact_root.iterdir() if path.is_file()} == set(runner.REQUIRED_ARTIFACTS)

    panel_files = sorted(path.name for path in artifact_root.glob("*_signal_panel.parquet"))
    assert panel_files == [
        "ecluster_01_signal_panel.parquet",
        "ecluster_02_signal_panel.parquet",
        "ecluster_03_signal_panel.parquet",
        "ecluster_04_signal_panel.parquet",
        "ecluster_05_signal_panel.parquet",
    ]

    sample = pd.read_parquet(artifact_root / "ecluster_03_signal_panel.parquet")
    assert list(sample.columns) == list(runner.PANEL_COLUMNS)
    assert set(sample["candidate_id"]) == {"ecluster_03_fragmented_event_absorption"}
    assert set(sample["module_id"]) == {MODULE_ID}
    assert set(sample["source_spec_id"]) == {runner.PANEL_SPEC_ID}
    assert set(sample["after_close_policy"]) == {runner.TIMING_POLICY}
    assert not sample[["date", "ticker", "candidate_id"]].duplicated().any()
    assert sample["contamination_metadata"].str.contains("isolated_event_anchors").all()
    assert sample["signal_value"].notna().any()

    metadata = json.loads((artifact_root / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert metadata["candidate_count"] == 5
    assert metadata["artifact_root"] == str(artifact_root)
    assert metadata["panel_generation_executed"] is True
    assert metadata["guardrails"]["ic_scoring_executed"] is False
    assert metadata["guardrails"]["validation_executed"] is False
    assert metadata["guardrails"]["governance_modified"] is False
    assert metadata["guardrails"]["production_registration"] is False
    assert metadata["guardrails"]["thresholds_modified"] is False
    assert metadata["guardrails"]["ml_integration"] is False

    generation_manifest = json.loads((artifact_root / "panel_generation_manifest.json").read_text(encoding="utf-8"))
    checksum_paths = {Path(record["artifact_path"]).name for record in generation_manifest["checksums"]}
    assert {
        "ecluster_01_signal_panel.parquet",
        "ecluster_02_signal_panel.parquet",
        "ecluster_03_signal_panel.parquet",
        "ecluster_04_signal_panel.parquet",
        "ecluster_05_signal_panel.parquet",
        "metadata.json",
        "panel_manifest.csv",
    }.issubset(checksum_paths)
    assert all(record["checksum_algorithm"] == "SHA-256" for record in generation_manifest["checksums"])


def test_validate_event_clustering_panel_artifacts_passes_after_generation(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_event_clustering_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=15)

    ok, errors = runner.validate_event_clustering_panel_artifacts(artifact_root)

    assert ok, errors


def test_validate_only_mode_passes_after_generation(tmp_path, monkeypatch, capsys):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_event_clustering_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=15)

    monkeypatch.setattr(sys, "argv", ["runner", "--artifact-root", str(artifact_root), "--validate-only"])

    assert runner.main() == 0
    assert "validation passed" in capsys.readouterr().out


def test_duplicate_blocked_candidate_and_checksum_failures_are_detected(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_event_clustering_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=15)

    panel_path = artifact_root / "ecluster_01_signal_panel.parquet"
    panel = pd.read_parquet(panel_path)
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)
    assert any(
        "duplicate panel rows" in error
        for error in runner.validate_candidate_panel_frame(duplicated, "ecluster_01_concentrated_absorption")
    )

    bad_panel = panel.assign(candidate_id="dpath_01_relapse_resilience_after_calm")
    errors = runner.validate_candidate_panel_frame(bad_panel, "ecluster_01_concentrated_absorption")
    assert any("candidate_id values do not match" in error for error in errors)
    assert any("blocked candidate appeared" in error for error in errors)

    panel_manifest = artifact_root / "panel_manifest.csv"
    panel_manifest.write_text(panel_manifest.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    ok, checksum_errors = runner.validate_event_clustering_panel_artifacts(artifact_root)
    assert not ok
    assert any("checksum mismatch" in error for error in checksum_errors)


def test_activation_neutrality_and_schema_report_pass(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_event_clustering_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=15)

    panel = pd.read_parquet(artifact_root / "ecluster_05_signal_panel.parquet")
    inactive = panel[panel["activation_state"].eq("inactive_neutralized") & panel["pre_activation_raw_score"].notna()]
    warmup = panel[panel["warmup_state"].eq("rolling_warmup")]

    assert not inactive.empty
    assert (inactive["signal_value"] == 0.5).all()
    assert not warmup.empty
    assert warmup["signal_value"].isna().all()

    schema_report = pd.read_csv(artifact_root / "schema_validation_report.csv")
    assert (schema_report["status"] == "PASS").all()
