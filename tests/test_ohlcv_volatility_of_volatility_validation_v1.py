from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    IMPLEMENTED_REFINEMENT_IDS,
    MODULE_ID,
)
from pipelines.run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1 import (
    PANEL_COLUMNS,
    PANEL_SPEC_ID,
    TIMING_POLICY,
)
import pipelines.run_ohlcv_volatility_of_volatility_validation_v1 as runner


def _write_panel_root(tmp_path: Path) -> tuple[Path, Path]:
    panel_root = tmp_path / "panel_v1"
    panel_root.mkdir()
    dates = pd.bdate_range("2025-01-02", periods=80)
    tickers = [f"T{i:03d}" for i in range(35)]
    close = pd.DataFrame(
        {
            ticker: 100 + idx * 0.25 + np.arange(len(dates)) * (0.05 + idx / 2000)
            for idx, ticker in enumerate(tickers)
        },
        index=dates,
    )
    close_path = tmp_path / "close.parquet"
    close.to_parquet(close_path)

    source_spec = {
        "vov_01_ref_anchor": "vov_01_instability_calm_after_chop__ref_anchor",
        "vov_01_ref_strict_calm": "vov_01_instability_calm_after_chop__ref_strict_calm",
        "vov_01_ref_longer_memory": "vov_01_instability_calm_after_chop__ref_longer_memory",
        "vov_01_ref_smoothed_calm": "vov_01_instability_calm_after_chop__ref_smoothed_calm",
        "vov_03_ref_anchor": "vov_03_range_chop_exhaustion__ref_anchor",
        "vov_03_ref_strict_chop": "vov_03_range_chop_exhaustion__ref_strict_chop",
        "vov_03_ref_longer_chop": "vov_03_range_chop_exhaustion__ref_longer_chop",
        "vov_03_ref_extension_controlled": "vov_03_range_chop_exhaustion__ref_extension_controlled",
    }
    manifest_rows = []
    schema_rows = []
    for cidx, candidate_id in enumerate(IMPLEMENTED_REFINEMENT_IDS):
        parent = "vov_01" if candidate_id.startswith("vov_01") else "vov_03"
        family = f"{parent}_refinement"
        rows = []
        for didx, date in enumerate(dates):
            for tidx, ticker in enumerate(tickers):
                warmup = didx < 5
                active = not warmup and ((tidx + cidx) % 5 != 0)
                base_signal = (tidx + 1) / len(tickers)
                if candidate_id == "vov_03_ref_strict_chop":
                    signal = 1.0 - base_signal
                elif candidate_id == "vov_01_ref_smoothed_calm":
                    signal = base_signal * 0.75 + 0.15
                elif candidate_id.endswith("_ref_anchor"):
                    signal = base_signal * 0.9 + 0.05
                else:
                    signal = base_signal
                signal = np.nan if warmup else signal
                pre_raw = np.nan if warmup else signal
                raw = np.nan if warmup else (pre_raw if active else 0.0)
                rows.append(
                    {
                        "date": date,
                        "ticker": ticker,
                        "candidate_id": candidate_id,
                        "source_spec_id": source_spec[candidate_id],
                        "parent_candidate_id": parent,
                        "module_id": MODULE_ID,
                        "refinement_family": family,
                        "family": "volatility_of_volatility",
                        "research_status": "RESEARCH_ONLY",
                        "primary_horizon": "h20" if parent == "vov_01" else "h10",
                        "secondary_horizons": "h10|h5" if parent == "vov_01" else "h20|h5",
                        "signal_value": signal,
                        "raw_score": raw,
                        "pre_activation_raw_score": pre_raw,
                        "is_active": active,
                        "feature_warmup_complete": not warmup,
                        "finite_cross_section_count": 35 if not warmup else 0,
                        "rank_min_count": 25,
                        "missing_reason": "rolling_warmup" if warmup else ("inactive_zeroed" if not active else pd.NA),
                        "timing_policy": TIMING_POLICY,
                        "created_by_spec": PANEL_SPEC_ID,
                    }
                )
        panel = pd.DataFrame(rows, columns=PANEL_COLUMNS)
        panel_path = panel_root / f"{candidate_id}_signal_panel.parquet"
        panel.to_parquet(panel_path, index=False)
        manifest_rows.append(
            {
                "candidate_id": candidate_id,
                "parent_candidate_id": parent,
                "source_spec_id": source_spec[candidate_id],
                "refinement_family": family,
                "panel_path": str(panel_path),
                "row_count": len(panel),
                "date_min": str(dates.min().date()),
                "date_max": str(dates.max().date()),
                "ticker_count": len(tickers),
                "duplicate_key_count": 0,
                "missing_signal_count": int(panel["signal_value"].isna().sum()),
                "inactive_row_count": int((~panel["is_active"].astype(bool)).sum()),
                "warmup_incomplete_count": int((~panel["feature_warmup_complete"].astype(bool)).sum()),
                "rank_min_count": 25,
                "dates_below_rank_min_count": 5,
                "timing_policy": TIMING_POLICY,
                "schema_status": "PASS",
                "blocked_candidate_check": "PASS",
                "anchor_equivalence_required": candidate_id.endswith("_ref_anchor"),
                "anchor_equivalence_status": "PASS" if candidate_id.endswith("_ref_anchor") else "NA",
            }
        )
        schema_rows.append(
            {
                "candidate_id": candidate_id,
                "schema_status": "PASS",
                "candidate_id_status": "PASS",
                "parent_candidate_id_status": "PASS",
                "source_spec_id_status": "PASS",
                "module_id_status": "PASS",
                "refinement_family_status": "PASS",
                "long_form_status": "PASS",
                "duplicate_status": "PASS",
                "activation_status": "PASS",
                "timing_status": "PASS",
                "blocked_candidate_status": "PASS",
                "anchor_equivalence_status": "PASS" if candidate_id.endswith("_ref_anchor") else "NA",
                "notes": "panel validation passed",
            }
        )

    pd.DataFrame(manifest_rows).to_csv(panel_root / "panel_manifest.csv", index=False)
    pd.DataFrame({"variant_count": [8], "row_count": [sum(row["row_count"] for row in manifest_rows)]}).to_csv(
        panel_root / "panel_generation_summary.csv", index=False
    )
    pd.DataFrame(schema_rows).to_csv(panel_root / "schema_validation_report.csv", index=False)
    for name in [
        "registry_manifest.csv",
        "formula_manifest.csv",
        "feature_manifest.csv",
        "input_schema_manifest.csv",
    ]:
        pd.DataFrame({"placeholder": [1]}).to_csv(panel_root / name, index=False)
    guardrail_flags = {
        "panel_generation_executed": True,
        "ic_scoring_executed": False,
        "refinement_scoring_executed": False,
        "validation_executed": False,
        "original_vov_panels_modified": False,
        "original_vov_formulas_modified": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
    }
    payload = {"candidate_ids": list(IMPLEMENTED_REFINEMENT_IDS), "guardrail_flags": guardrail_flags}
    (panel_root / "metadata.json").write_text(json.dumps(payload), encoding="utf-8")
    manifest_payload = {
        "candidate_ids": list(IMPLEMENTED_REFINEMENT_IDS),
        "guardrail_flags": guardrail_flags,
        "duplicate_key_status": "PASS",
        "schema_validation_status": "PASS",
        "anchor_equivalence_status": "PASS",
    }
    (panel_root / "panel_generation_manifest.json").write_text(json.dumps(manifest_payload), encoding="utf-8")
    return panel_root, close_path


def test_validate_only_manifest_is_fail_closed_and_does_not_score(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "validation"

    runner.write_validate_only_manifest(panel_root=panel_root, close_path=close_path, out_dir=out_dir)

    manifest = json.loads((out_dir / "validation_manifest.json").read_text(encoding="utf-8"))
    assert manifest["validate_only"] is True
    assert manifest["validation_executed"] is False
    assert manifest["panel_validation_executed"] is True
    assert manifest["historical_ic_artifacts_recomputed"] is False
    assert manifest["approved_panels_modified"] is False
    assert manifest["formulas_modified"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False
    assert manifest["validation_candidate_ids"] == list(runner.VALIDATION_CANDIDATE_IDS)
    assert manifest["baseline_comparator_ids"] == list(runner.BASELINE_COMPARATOR_IDS)
    assert "vov_01_ref_longer_memory" in manifest["excluded_candidate_ids"]
    assert not (out_dir / "daily_validation_ic.csv").exists()


def test_run_validation_writes_contract_outputs_for_approved_scope_only(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    out_dir = tmp_path / "validation"

    outputs = runner.run_validation(panel_root=panel_root, close_path=close_path, out_dir=out_dir)

    assert set(outputs) == {
        "daily_validation_ic",
        "candidate_horizon_validation_scores",
        "rolling_validation_diagnostics",
        "anchor_comparison",
        "coverage_turnover_diagnostics",
        "contamination_correlation_matrix",
        "contamination_overlap_summary",
        "stability_window_summary",
        "validation_decision_inputs",
    }
    for file_name in [
        "validation_manifest.json",
        "daily_validation_ic.csv",
        "candidate_horizon_validation_scores.csv",
        "rolling_validation_diagnostics.csv",
        "anchor_comparison.csv",
        "coverage_turnover_diagnostics.csv",
        "contamination_correlation_matrix.csv",
        "contamination_overlap_summary.csv",
        "stability_window_summary.csv",
        "validation_decision_inputs.csv",
        "approved_panel_manifest_copy.csv",
        "reference_manifest.csv",
    ]:
        assert (out_dir / file_name).exists()

    daily = pd.read_csv(out_dir / "daily_validation_ic.csv")
    assert set(daily["candidate_id"]) == set(runner.VALIDATION_SCOPE_IDS)
    assert set(daily["horizon"]) == {"h1", "h5", "h10", "h20"}
    assert not set(daily["candidate_id"]).intersection({"vov_01_ref_longer_memory", "vov_03_ref_longer_chop"})

    decisions = pd.read_csv(out_dir / "validation_decision_inputs.csv")
    assert set(decisions["candidate_id"]) == set(runner.VALIDATION_CANDIDATE_IDS)
    assert set(decisions["anchor_candidate_id"]) == set(runner.BASELINE_COMPARATOR_IDS)
    assert set(decisions["validation_decision"]) == {"PENDING_VALIDATION_REVIEW"}

    anchor = pd.read_csv(out_dir / "anchor_comparison.csv")
    assert set(anchor["candidate_id"]) == set(runner.VALIDATION_CANDIDATE_IDS)
    assert set(anchor["anchor_candidate_id"]) == set(runner.BASELINE_COMPARATOR_IDS)

    manifest = json.loads((out_dir / "validation_manifest.json").read_text(encoding="utf-8"))
    assert manifest["validation_executed"] is True
    assert manifest["baseline_comparators_promoted"] is False
    assert manifest["watch_or_park_candidates_included"] is False
    assert manifest["validation_thresholds"] == runner.VALIDATION_THRESHOLDS
    assert len(manifest["input_lineage_checksums"]["panel_manifest_sha256"]) == 64
    assert len(manifest["input_lineage_checksums"]["close_source_sha256"]) == 64


def test_watch_or_park_scope_drift_is_rejected(tmp_path):
    panel_root, close_path = _write_panel_root(tmp_path)
    manifest = pd.read_csv(panel_root / "panel_manifest.csv")
    manifest.loc[manifest["candidate_id"].eq("vov_01_ref_smoothed_calm"), "candidate_id"] = "vov_01_ref_longer_memory"
    manifest.to_csv(panel_root / "panel_manifest.csv", index=False)

    try:
        runner.run_validation(panel_root=panel_root, close_path=close_path, out_dir=tmp_path / "validation")
    except ValueError as exc:
        assert "validation failed" in str(exc) or "candidate IDs" in str(exc)
    else:
        raise AssertionError("watch/park scope drift should fail validation preflight")


def test_daily_ic_known_answer_fixture():
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
