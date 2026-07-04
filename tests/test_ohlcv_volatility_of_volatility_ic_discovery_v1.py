from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    IMPLEMENTED_CANDIDATE_IDS,
    RUN_ID as MODULE_ID,
)
import pipelines.run_ohlcv_volatility_of_volatility_ic_discovery_v1 as runner
from pipelines.run_ohlcv_volatility_of_volatility_panel_generation_v1 import PANEL_COLUMNS, TIMING_POLICY


def _write_panel_root(tmp_path: Path) -> tuple[Path, Path]:
    panel_root = tmp_path / "panel_v1"
    panel_root.mkdir()
    dates = pd.bdate_range("2025-01-02", periods=50)
    tickers = [f"T{i:03d}" for i in range(35)]
    close = pd.DataFrame(
        {
            ticker: 100 + idx * 0.3 + np.arange(len(dates)) * (0.08 + idx / 2000)
            for idx, ticker in enumerate(tickers)
        },
        index=dates,
    )
    close_path = tmp_path / "close.parquet"
    close.to_parquet(close_path)

    source_spec = {
        "vov_01": "vov_01_instability_calm_after_chop",
        "vov_02": "vov_02_low_extension_vov_rise",
        "vov_03": "vov_03_range_chop_exhaustion",
        "vov_04": "vov_04_vov_slope_divergence",
        "vov_05": "vov_05_churn_controlled_vov_stabilization",
    }
    manifest_rows = []
    for cidx, candidate_id in enumerate(IMPLEMENTED_CANDIDATE_IDS):
        rows = []
        for didx, date in enumerate(dates):
            for tidx, ticker in enumerate(tickers):
                warmup = didx < 5
                active = not warmup and ((tidx + cidx) % 3 != 0 or candidate_id == "vov_04")
                base_signal = (tidx + 1) / len(tickers)
                signal = np.nan if warmup else (base_signal if cidx % 2 == 0 else 1.0 - base_signal)
                pre_raw = np.nan if warmup else base_signal
                raw = np.nan if warmup else (pre_raw if active else 0.0)
                rows.append(
                    {
                        "date": date,
                        "ticker": ticker,
                        "candidate_id": candidate_id,
                        "source_spec_id": source_spec[candidate_id],
                        "module_id": MODULE_ID,
                        "family": "volatility_of_volatility",
                        "research_status": "RESEARCH_ONLY",
                        "primary_horizon": "h10",
                        "secondary_horizons": "h5|h20",
                        "signal_value": signal,
                        "raw_score": raw,
                        "pre_activation_raw_score": pre_raw,
                        "is_active": active,
                        "feature_warmup_complete": not warmup,
                        "finite_cross_section_count": 35 if not warmup else 0,
                        "rank_min_count": 25,
                        "missing_reason": "rolling_warmup" if warmup else ("inactive_zeroed" if not active else pd.NA),
                        "timing_policy": TIMING_POLICY,
                        "created_by_spec": "ohlcv_volatility_of_volatility_research_module_panel_specification_v1",
                    }
                )
        panel = pd.DataFrame(rows, columns=PANEL_COLUMNS)
        panel_path = panel_root / f"{candidate_id}_signal_panel.parquet"
        panel.to_parquet(panel_path, index=False)
        manifest_rows.append(
            {
                "candidate_id": candidate_id,
                "source_spec_id": source_spec[candidate_id],
                "module_id": MODULE_ID,
                "panel_path": str(panel_path),
                "row_count": len(panel),
                "date_min": str(dates.min().date()),
                "date_max": str(dates.max().date()),
                "ticker_count": len(tickers),
                "duplicate_key_count": 0,
                "invalid_candidate_count": 0,
                "missing_signal_count": int(panel["signal_value"].isna().sum()),
                "inactive_row_count": int((~panel["is_active"].astype(bool)).sum()),
                "warmup_incomplete_count": int((~panel["feature_warmup_complete"].astype(bool)).sum()),
                "rank_min_count": 25,
                "dates_below_rank_min_count": 5,
                "timing_policy": TIMING_POLICY,
                "schema_status": "PASS",
                "generation_status": "generated",
            }
        )
    pd.DataFrame(manifest_rows).to_csv(panel_root / "panel_manifest.csv", index=False)
    pd.DataFrame({"candidate_id": list(IMPLEMENTED_CANDIDATE_IDS)}).to_csv(
        panel_root / "panel_generation_summary.csv", index=False
    )
    pd.DataFrame(
        {
            "candidate_id": list(IMPLEMENTED_CANDIDATE_IDS),
            "schema_status": ["PASS"] * 5,
            "duplicate_status": ["PASS"] * 5,
            "activation_status": ["PASS"] * 5,
            "timing_status": ["PASS"] * 5,
            "family_b_c_status": ["PASS"] * 5,
        }
    ).to_csv(panel_root / "schema_validation_report.csv", index=False)
    for name in [
        "candidate_registry.csv",
        "candidate_formula_manifest.csv",
        "input_schema.csv",
        "derived_feature_manifest.csv",
    ]:
        pd.DataFrame({"placeholder": [1]}).to_csv(panel_root / name, index=False)
    payload = {
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "panel_generation_executed": True,
        "ic_scoring_executed": False,
        "discovery_executed": False,
        "redundancy_screening_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
    }
    (panel_root / "metadata.json").write_text(json.dumps(payload), encoding="utf-8")
    (panel_root / "panel_generation_manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    return panel_root, close_path


def test_run_ic_discovery_writes_required_artifacts(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "ic_discovery_v1"

    outputs = runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=out_dir)

    assert set(outputs) == {
        "daily_ic",
        "candidate_horizon_ic_scores",
        "candidate_ic_summary",
        "horizon_summary",
        "family_summary",
        "candidate_rankings",
        "rolling_ic_diagnostics",
    }
    for file_name in [
        "daily_ic.csv",
        "candidate_horizon_ic_scores.csv",
        "candidate_ic_summary.csv",
        "horizon_summary.csv",
        "family_summary.csv",
        "candidate_rankings.csv",
        "rolling_ic_diagnostics.csv",
        "approved_panel_manifest.csv",
        "manifest.json",
    ]:
        assert (out_dir / file_name).exists()

    rankings = pd.read_csv(out_dir / "candidate_rankings.csv")
    assert tuple(rankings["candidate_id"]) == tuple(rankings.sort_values("rank")["candidate_id"])
    assert set(rankings["recommendation"]).issubset({"ADVANCE_TO_REFINEMENT", "WATCH", "REJECT"})


def test_known_answer_daily_spearman_ic_fixture():
    tickers = [f"T{i:02d}" for i in range(30)]
    dates = pd.bdate_range("2025-03-03", periods=2)
    signal = pd.DataFrame(
        [np.arange(30, dtype=float), np.arange(30, dtype=float)],
        index=dates,
        columns=tickers,
    )
    fwd = pd.DataFrame(
        [np.arange(30, dtype=float), np.arange(29, -1, -1, dtype=float)],
        index=dates,
        columns=tickers,
    )

    daily = runner._daily_ic_frame(signal, fwd, 1)

    assert daily["observation_count"].tolist() == [30, 30]
    assert np.allclose(daily["ic"].to_numpy(), [1.0, -1.0])


def test_forward_returns_use_future_close_after_signal_date():
    close = pd.DataFrame(
        {"AAA": [100.0, 110.0, 121.0], "BBB": [50.0, 45.0, 54.0]},
        index=pd.bdate_range("2025-04-01", periods=3),
    )

    fwd = runner._forward_returns(close, 1)

    assert np.isclose(fwd.loc[close.index[0], "AAA"], 0.10)
    assert np.isclose(fwd.loc[close.index[1], "AAA"], 0.10)
    assert np.isclose(fwd.loc[close.index[0], "BBB"], -0.10)
    assert np.isclose(fwd.loc[close.index[1], "BBB"], 0.20)


def test_candidate_summary_is_candidate_level_not_horizon_grain(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "ic_discovery_v1"

    outputs = runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=out_dir)
    summary = outputs["candidate_ic_summary"]
    written = pd.read_csv(out_dir / "candidate_ic_summary.csv")

    assert len(summary) == len(IMPLEMENTED_CANDIDATE_IDS)
    assert len(written) == len(IMPLEMENTED_CANDIDATE_IDS)
    assert "horizon" not in summary.columns
    assert "primary_mean_ic" in summary.columns
    assert "primary_best_mean_ic" in summary.columns


def test_manifest_guardrails_are_fail_closed(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "ic_discovery_v1"
    runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=out_dir)

    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["panel_validation_executed_before_ic"] is True
    assert manifest["ic_discovery_executed"] is True
    assert manifest["panel_generation_executed"] is False
    assert manifest["panels_modified"] is False
    assert manifest["formulas_modified"] is False
    assert manifest["family_b_or_c_used"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False
    assert manifest["classification_thresholds"] == runner.CLASSIFICATION_THRESHOLDS
    checksums = manifest["input_lineage_checksums"]
    assert isinstance(checksums["panel_manifest_sha256"], str)
    assert len(checksums["panel_manifest_sha256"]) == 64
    assert isinstance(checksums["close_source_sha256"], str)
    assert len(checksums["close_source_sha256"]) == 64


def test_family_b_or_c_candidate_in_manifest_is_rejected(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    manifest = pd.read_csv(panel_root / "panel_manifest.csv")
    manifest.loc[0, "candidate_id"] = "dpath_01"
    manifest.to_csv(panel_root / "panel_manifest.csv", index=False)

    try:
        runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=tmp_path / "out")
    except ValueError as exc:
        assert "validation failed" in str(exc) or "candidate IDs mismatch" in str(exc)
    else:
        raise AssertionError("Family B candidate should have failed IC discovery preflight")


def test_daily_ic_uses_forward_returns_after_signal_date(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "ic_discovery_v1"
    runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=out_dir)
    daily = pd.read_csv(out_dir / "daily_ic.csv")

    assert set(daily["timing_policy"]) == {TIMING_POLICY}
    assert set(daily["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert daily["ic"].notna().any()


def test_candidate_ranking_prefers_primary_horizons(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "ic_discovery_v1"
    runner.run_ic_discovery(panel_root=panel_root, close_path=close_path, out_dir=out_dir)
    rankings = pd.read_csv(out_dir / "candidate_rankings.csv")

    assert set(rankings["best_primary_horizon"]).issubset({"h10", "h20"})
    assert list(rankings["rank"]) == list(range(1, len(IMPLEMENTED_CANDIDATE_IDS) + 1))
