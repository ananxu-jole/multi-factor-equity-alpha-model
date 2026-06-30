import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
    APPROVED_CANDIDATE_IDS,
    REQUIRED_PANEL_COLUMNS,
    WARMUP_WINDOW,
)
import pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 as runner


RUNNER = ["python", "pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py"]


def _synthetic_ohlcv(n_dates: int = 150, n_tickers: int = 35) -> pd.DataFrame:
    dates = pd.bdate_range("2025-01-02", periods=n_dates)
    rows = []
    for ticker_idx in range(n_tickers):
        ticker = f"T{ticker_idx:03d}"
        for date_idx, date in enumerate(dates):
            trend = 0.08 * date_idx * (1 + ticker_idx / 200)
            cycle = np.sin(date_idx / 7 + ticker_idx / 5) * 0.6
            close = 40 + ticker_idx * 0.35 + trend + cycle
            volume = 100_000 + ticker_idx * 1_500 + date_idx * (200 + ticker_idx)
            rows.append(
                {
                    "date": date,
                    "ticker": ticker,
                    "open": close * 0.997,
                    "high": close * 1.012,
                    "low": close * 0.988,
                    "close": close,
                    "volume": volume,
                }
            )
    return pd.DataFrame(rows)


def _wide_ohlcv(raw: pd.DataFrame) -> pd.DataFrame:
    return pd.concat(
        {
            "Open": raw.pivot(index="date", columns="ticker", values="open"),
            "High": raw.pivot(index="date", columns="ticker", values="high"),
            "Low": raw.pivot(index="date", columns="ticker", values="low"),
            "Close": raw.pivot(index="date", columns="ticker", values="close"),
            "Volume": raw.pivot(index="date", columns="ticker", values="volume"),
        },
        axis=1,
    )


def _use_temp_panel_artifacts(monkeypatch, tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    monkeypatch.setattr(runner, "CANDIDATE_PANELS_DIR", root / "candidate_panels")
    monkeypatch.setattr(runner, "CANDIDATE_PANEL_GENERATION_DIR", root / "candidate_panel_generation")


def test_write_candidate_panels_creates_parquet_manifest_and_metadata(tmp_path, monkeypatch):
    _use_temp_panel_artifacts(monkeypatch, tmp_path)
    source_path = tmp_path / "raw_ohlcv.parquet"
    _wide_ohlcv(_synthetic_ohlcv()).to_parquet(source_path)

    manifest_rows, summary_rows = runner.write_candidate_panels(source_path)

    assert [row["candidate_id"] for row in manifest_rows] == APPROVED_CANDIDATE_IDS
    assert [row["candidate_id"] for row in summary_rows] == APPROVED_CANDIDATE_IDS
    assert "nhlr_06" not in {row["candidate_id"] for row in manifest_rows}

    manifest_path = runner.CANDIDATE_PANEL_GENERATION_DIR / "panel_manifest.csv"
    summary_path = runner.CANDIDATE_PANEL_GENERATION_DIR / "candidate_panel_generation_summary.csv"
    generation_manifest_path = runner.CANDIDATE_PANEL_GENERATION_DIR / "panel_generation_manifest.json"
    validation_report_path = runner.CANDIDATE_PANEL_GENERATION_DIR / "panel_schema_validation_report.csv"

    assert manifest_path.exists()
    assert summary_path.exists()
    assert generation_manifest_path.exists()
    assert validation_report_path.exists()

    manifest = pd.read_csv(manifest_path)
    summary = pd.read_csv(summary_path)
    validation = pd.read_csv(validation_report_path)

    assert list(manifest["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert list(summary["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert list(validation["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert set(manifest["generation_status"]) == {"generated"}
    assert set(manifest["schema_status"]) == {"PASS"}
    assert set(manifest["registry_status"]) == {"PASS"}
    assert manifest["warmup_trimmed"].astype(bool).all()

    expected_rows_per_candidate = (150 - (WARMUP_WINDOW - 1)) * 35
    assert set(manifest["row_count"].astype(int)) == {expected_rows_per_candidate}
    assert set(manifest["warmup_rows_excluded"].astype(int)) == {(WARMUP_WINDOW - 1) * 35}

    panel_files = sorted(runner.CANDIDATE_PANELS_DIR.glob("nhlr_*.parquet"))
    metadata_files = sorted(runner.CANDIDATE_PANELS_DIR.glob("nhlr_*.metadata.json"))
    assert len(panel_files) == len(APPROVED_CANDIDATE_IDS)
    assert len(metadata_files) == len(APPROVED_CANDIDATE_IDS)

    sample = pd.read_parquet(runner.CANDIDATE_PANELS_DIR / "nhlr_07.parquet")
    assert list(sample.columns) == REQUIRED_PANEL_COLUMNS
    assert set(sample["candidate_id"]) == {"nhlr_07"}
    assert sample["warmup_complete"].astype(bool).all()
    assert sample["signal_value"].notna().any()
    assert not sample[["date", "ticker", "candidate_id"]].duplicated().any()

    metadata = json.loads((runner.CANDIDATE_PANELS_DIR / "nhlr_07.metadata.json").read_text(encoding="utf-8"))
    assert metadata["candidate_id"] == "nhlr_07"
    assert metadata["row_count"] == len(sample)
    assert metadata["warmup_trimmed"] is True
    assert metadata["candidate_panels_generated"] is True
    assert metadata["discovery_executed"] is False
    assert metadata["ic_calculated"] is False
    assert metadata["redundancy_screening_run"] is False

    generation_manifest = json.loads(generation_manifest_path.read_text(encoding="utf-8"))
    assert generation_manifest["panel_generation_status"] == runner.PANEL_GENERATION_STATUS
    assert generation_manifest["final_classification"] == runner.PANEL_GENERATION_FINAL_CLASSIFICATION
    assert generation_manifest["candidate_panels_generated"] is True
    assert generation_manifest["panel_generation_executed"] is True
    assert generation_manifest["discovery_executed"] is False
    assert generation_manifest["ic_calculated"] is False
    assert generation_manifest["redundancy_screening_run"] is False
    assert generation_manifest["validation_executed"] is False


def test_validate_candidate_panels_and_runner_modes_pass_after_generation(tmp_path, monkeypatch, capsys):
    _use_temp_panel_artifacts(monkeypatch, tmp_path)
    source_path = tmp_path / "raw_ohlcv.parquet"
    _wide_ohlcv(_synthetic_ohlcv()).to_parquet(source_path)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            RUNNER[1],
            "--write-candidate-panels",
            "--candidate-panel-source",
            str(source_path),
        ],
    )
    assert runner.main() == 0
    write_stdout = capsys.readouterr().out
    assert runner.PANEL_GENERATION_STATUS in write_stdout
    assert runner.PANEL_GENERATION_FINAL_CLASSIFICATION in write_stdout
    assert "No discovery" in write_stdout

    monkeypatch.setattr(sys, "argv", [RUNNER[1], "--validate-candidate-panels"])
    assert runner.main() == 0
    validate_stdout = capsys.readouterr().out
    assert "validation passed" in validate_stdout

    ok, errors = runner.validate_candidate_panels()
    assert ok, errors


def test_panel_validation_detects_duplicate_rows(tmp_path, monkeypatch):
    _use_temp_panel_artifacts(monkeypatch, tmp_path)
    source_path = tmp_path / "raw_ohlcv.parquet"
    _wide_ohlcv(_synthetic_ohlcv()).to_parquet(source_path)
    runner.write_candidate_panels(source_path)

    panel = pd.read_parquet(runner.CANDIDATE_PANELS_DIR / "nhlr_01.parquet")
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)

    errors = runner.validate_candidate_panel_frame(duplicated, "nhlr_01")

    assert any("duplicate panel rows" in error for error in errors)
