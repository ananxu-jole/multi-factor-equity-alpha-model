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
    FORMULA_SPECS,
    REQUIRED_PANEL_COLUMNS,
)
from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1 import (
    HORIZONS,
    run_ic_discovery,
)
from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 import (
    candidate_registry_rows,
)


def _synthetic_close(n_dates: int = 80, n_tickers: int = 30) -> pd.DataFrame:
    dates = pd.bdate_range("2025-01-02", periods=n_dates)
    data = {}
    for ticker_idx in range(n_tickers):
        drift = 0.001 * (ticker_idx + 1)
        data[f"T{ticker_idx:03d}"] = 50 + ticker_idx + np.arange(n_dates) * drift
    return pd.DataFrame(data, index=dates)


def _write_temp_panels(source_dir: Path, close: pd.DataFrame) -> None:
    panel_dir = source_dir / "candidate_panels"
    generation_dir = source_dir / "candidate_panel_generation"
    panel_dir.mkdir(parents=True)
    generation_dir.mkdir(parents=True)
    registry = {row["candidate_id"]: row for row in candidate_registry_rows()}
    manifest_rows = []
    for candidate_id in APPROVED_CANDIDATE_IDS:
        registry_row = registry[candidate_id]
        spec = FORMULA_SPECS[candidate_id]
        rows = []
        for date_idx, date in enumerate(close.index):
            for ticker_idx, ticker in enumerate(close.columns):
                rows.append(
                    {
                        "date": date,
                        "ticker": ticker,
                        "candidate_id": candidate_id,
                        "signal_value": ticker_idx + date_idx / 1000,
                        "family": registry_row["family"],
                        "theme": registry_row["concept_category"],
                        "horizon": spec["primary_horizon"],
                        "working_name": registry_row["working_name"],
                        "economic_mechanism": registry_row["economic_mechanism"],
                        "implementation_priority": registry_row["implementation_priority"],
                        "panel_role": spec["panel_role"],
                        "formula_name": spec["formula_name"],
                        "formula_version": "v1",
                        "dependency_class": registry_row["dependency_class"],
                        "required_input_family": registry_row["required_input_family"],
                        "component_coverage_count": 5,
                        "warmup_complete": True,
                        "non_hostile_market_state": 1.0,
                        "source_close_column": "close",
                        "missing_data_reason": "",
                    }
                )
        panel = pd.DataFrame(rows)[REQUIRED_PANEL_COLUMNS]
        panel_path = panel_dir / f"{candidate_id}.parquet"
        metadata_path = panel_dir / f"{candidate_id}.metadata.json"
        panel.to_parquet(panel_path, index=False)
        metadata_path.write_text(json.dumps({"candidate_id": candidate_id, "row_count": len(panel)}) + "\n")
        manifest_rows.append(
            {
                "candidate_id": candidate_id,
                "panel_path": str(panel_path),
                "metadata_path": str(metadata_path),
                "row_count": len(panel),
                "non_null_signal_count": int(panel["signal_value"].notna().sum()),
                "null_signal_count": int(panel["signal_value"].isna().sum()),
                "start_date": str(close.index.min().date()),
                "end_date": str(close.index.max().date()),
                "horizon": spec["primary_horizon"],
                "formula_name": spec["formula_name"],
                "formula_version": "v1",
                "warmup_window": 120,
                "warmup_rows_excluded": 0,
                "warmup_trimmed": True,
                "schema_status": "PASS",
                "registry_status": "PASS",
                "generation_status": "generated",
            }
        )
    pd.DataFrame(manifest_rows).to_csv(generation_dir / "panel_manifest.csv", index=False)


def test_ic_discovery_writes_required_artifacts(tmp_path):
    source_dir = tmp_path / "source"
    out_dir = tmp_path / "ic_discovery"
    close = _synthetic_close()
    close_path = tmp_path / "close.parquet"
    close.to_parquet(close_path)
    _write_temp_panels(source_dir, close)

    outputs = run_ic_discovery(source_dir=source_dir, close_path=close_path, out_dir=out_dir)

    expected_files = [
        "daily_ic.csv",
        "candidate_ic_summary.csv",
        "horizon_summary.csv",
        "family_summary.csv",
        "candidate_rankings.csv",
        "rolling_ic_diagnostics.csv",
        "candidate_horizon_ic_scores.csv",
        "manifest.json",
    ]
    for filename in expected_files:
        assert (out_dir / filename).exists()

    daily = pd.read_csv(out_dir / "daily_ic.csv")
    summary = pd.read_csv(out_dir / "candidate_ic_summary.csv")
    rankings = pd.read_csv(out_dir / "candidate_rankings.csv")
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))

    assert set(outputs) == {
        "daily_ic",
        "candidate_ic_summary",
        "rolling_ic_diagnostics",
        "horizon_summary",
        "family_summary",
        "candidate_rankings",
    }
    assert set(daily["candidate_id"]) == set(APPROVED_CANDIDATE_IDS)
    assert set(daily["horizon"]) == {f"h{horizon}" for horizon in HORIZONS}
    assert len(summary) == len(APPROVED_CANDIDATE_IDS) * len(HORIZONS)
    assert list(rankings["candidate_id"]) == APPROVED_CANDIDATE_IDS
    assert set(rankings["classification"]).issubset({"ADVANCE_TO_REFINEMENT", "WATCH", "REJECT"})
    assert manifest["ic_discovery_executed"] is True
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["formulas_modified"] is False
    assert manifest["panels_modified"] is False


def test_ic_discovery_rejects_manifest_with_excluded_candidate(tmp_path):
    source_dir = tmp_path / "source"
    out_dir = tmp_path / "ic_discovery"
    close = _synthetic_close()
    close_path = tmp_path / "close.parquet"
    close.to_parquet(close_path)
    _write_temp_panels(source_dir, close)

    manifest_path = source_dir / "candidate_panel_generation" / "panel_manifest.csv"
    manifest = pd.read_csv(manifest_path)
    manifest.loc[0, "candidate_id"] = "nhlr_06"
    manifest.to_csv(manifest_path, index=False)

    try:
        run_ic_discovery(source_dir=source_dir, close_path=close_path, out_dir=out_dir)
    except ValueError as exc:
        assert "approved registry order" in str(exc)
    else:
        raise AssertionError("run_ic_discovery unexpectedly accepted nhlr_06")
