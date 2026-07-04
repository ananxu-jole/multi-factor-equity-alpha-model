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

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    IMPLEMENTED_REFINEMENT_IDS,
    MODULE_ID,
)
import pipelines.run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1 as runner


def _synthetic_ohlcv(n_dates: int = 115, n_tickers: int = 60) -> pd.DataFrame:
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


def test_write_refinement_panel_artifacts_creates_exact_panels_and_manifests(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)

    manifest, summary = runner.write_refinement_panel_artifacts(
        source_path,
        artifact_root=artifact_root,
        rank_min_count=20,
    )

    assert tuple(manifest["candidate_id"]) == IMPLEMENTED_REFINEMENT_IDS
    assert int(summary["variant_count"].iloc[0]) == 8
    for file_name in (
        "metadata.json",
        "panel_manifest.csv",
        "panel_generation_summary.csv",
        "panel_generation_manifest.json",
        "schema_validation_report.csv",
        "registry_manifest.csv",
        "formula_manifest.csv",
        "feature_manifest.csv",
        "input_schema_manifest.csv",
    ):
        assert (artifact_root / file_name).exists()

    panel_files = sorted(artifact_root.glob("vov_*_signal_panel.parquet"))
    assert len(panel_files) == 8
    assert {path.name.removesuffix("_signal_panel.parquet") for path in panel_files} == set(
        IMPLEMENTED_REFINEMENT_IDS
    )

    sample = pd.read_parquet(artifact_root / "vov_01_ref_anchor_signal_panel.parquet")
    assert list(sample.columns) == runner.PANEL_COLUMNS
    assert set(sample["candidate_id"]) == {"vov_01_ref_anchor"}
    assert set(sample["parent_candidate_id"]) == {"vov_01"}
    assert set(sample["refinement_family"]) == {"vov_01_refinement"}
    assert set(sample["source_spec_id"]) == {"vov_01_instability_calm_after_chop__ref_anchor"}
    assert set(sample["module_id"]) == {MODULE_ID}
    assert set(sample["timing_policy"]) == {runner.TIMING_POLICY}
    assert set(sample["created_by_spec"]) == {runner.PANEL_SPEC_ID}
    assert not sample[["date", "ticker", "candidate_id"]].duplicated().any()
    assert sample["signal_value"].notna().any()

    metadata = json.loads((artifact_root / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["candidate_ids"] == list(IMPLEMENTED_REFINEMENT_IDS)
    assert metadata["classification"] == runner.PANEL_GENERATION_CLASSIFICATION
    assert metadata["guardrail_flags"]["panel_generation_executed"] is True
    assert metadata["guardrail_flags"]["ic_scoring_executed"] is False
    assert metadata["guardrail_flags"]["refinement_scoring_executed"] is False
    assert metadata["guardrail_flags"]["validation_executed"] is False
    assert metadata["guardrail_flags"]["original_vov_panels_modified"] is False
    assert metadata["guardrail_flags"]["original_vov_formulas_modified"] is False
    assert metadata["guardrail_flags"]["production_registration"] is False
    assert metadata["guardrail_flags"]["ml_integration"] is False


def test_validate_refinement_panel_artifacts_passes_after_generation(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    ok, errors = runner.validate_refinement_panel_artifacts(artifact_root)

    assert ok, errors


def test_anchor_equivalence_is_manifested_as_pass(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    manifest = pd.read_csv(artifact_root / "panel_manifest.csv")
    anchors = manifest.loc[manifest["anchor_equivalence_required"].astype(bool)]

    assert set(anchors["candidate_id"]) == {"vov_01_ref_anchor", "vov_03_ref_anchor"}
    assert set(anchors["anchor_equivalence_status"]) == {"PASS"}


def test_duplicate_prevention_rejects_duplicate_refinement_rows(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "vov_03_ref_longer_chop_signal_panel.parquet")
    duplicated = pd.concat([panel, panel.iloc[[0]]], ignore_index=True)

    errors = runner.validate_candidate_panel_frame(duplicated, "vov_03_ref_longer_chop")

    assert any("duplicate panel rows" in error for error in errors)


def test_blocked_candidate_and_family_prefix_are_rejected(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "vov_01_ref_anchor_signal_panel.parquet")
    blocked_watch = panel.assign(candidate_id="vov_05")
    blocked_family = panel.assign(candidate_id="dpath_01")

    watch_errors = runner.validate_candidate_panel_frame(blocked_watch, "vov_01_ref_anchor")
    family_errors = runner.validate_candidate_panel_frame(blocked_family, "vov_01_ref_anchor")

    assert any("candidate_id values do not match" in error for error in watch_errors)
    assert any("blocked candidate" in error for error in watch_errors)
    assert any("candidate_id values do not match" in error for error in family_errors)
    assert any("blocked candidate" in error for error in family_errors)


def test_activation_semantics_preserve_inactive_zero_and_missing(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    panel = pd.read_parquet(artifact_root / "vov_03_ref_extension_controlled_signal_panel.parquet")
    inactive = panel[(~panel["is_active"]) & panel["pre_activation_raw_score"].notna()]
    warmup = panel[panel["pre_activation_raw_score"].isna()]

    assert not inactive.empty
    assert (inactive["raw_score"] == 0.0).all()
    assert set(inactive["missing_reason"].dropna()) == {"inactive_zeroed"}
    assert not warmup.empty
    assert warmup["raw_score"].isna().all()
    assert warmup["signal_value"].isna().all()


def test_validate_only_mode_passes_after_generation(tmp_path, monkeypatch, capsys):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)

    monkeypatch.setattr(sys, "argv", ["runner", "--artifact-root", str(artifact_root), "--validate-only"])

    assert runner.main() == 0
    assert "validation passed" in capsys.readouterr().out


def test_validation_fails_on_unexpected_extra_refinement_parquet(tmp_path):
    source_path = tmp_path / "raw_ohlcv.parquet"
    artifact_root = tmp_path / "panel_v1"
    _synthetic_ohlcv().to_parquet(source_path, index=False)
    runner.write_refinement_panel_artifacts(source_path, artifact_root=artifact_root, rank_min_count=20)
    (artifact_root / "vov_05_signal_panel.parquet").write_bytes(
        (artifact_root / "vov_01_ref_anchor_signal_panel.parquet").read_bytes()
    )

    ok, errors = runner.validate_refinement_panel_artifacts(artifact_root)

    assert not ok
    assert any("unexpected refinement panel parquet" in error for error in errors)
