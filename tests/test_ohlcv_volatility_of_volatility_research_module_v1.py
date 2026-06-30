from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    BLOCKED_FAMILY_PREFIXES,
    IMPLEMENTED_CANDIDATE_IDS,
    RAW_INPUT_COLUMNS,
    build_vov_candidate_panel,
    candidate_registry,
    expected_panel_columns,
    module_guardrail_manifest,
    validate_vov_registry,
)
from pipelines.utils.registry_validation import RegistryValidationError


def _synthetic_ohlcv(n_dates: int = 90, n_tickers: int = 60) -> pd.DataFrame:
    dates = pd.date_range("2024-01-02", periods=n_dates, freq="B")
    rows = []
    for j in range(n_tickers):
        ticker = f"T{j:03d}"
        base = 20.0 + j * 0.25
        for i, date in enumerate(dates):
            wave = np.sin(i / 4.0 + j / 7.0)
            drift = 0.015 * i
            close = base + drift + wave * (0.5 + j / 200.0)
            open_ = close * (1.0 + 0.002 * np.cos(i / 5.0 + j))
            high = max(open_, close) * (1.0 + 0.01 + 0.001 * (j % 3))
            low = min(open_, close) * (1.0 - 0.01 - 0.001 * (j % 5))
            volume = 100_000 + 1_000 * j + 250 * i + 500 * abs(wave)
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


def test_registry_contains_exactly_family_a_candidates():
    registry = candidate_registry()
    validate_vov_registry(registry)

    assert tuple(registry["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert len(registry) == 5
    assert set(registry["family"]) == {"volatility_of_volatility"}
    assert set(registry["horizon"]) == {"h10"}
    assert not registry["candidate_id"].str.startswith(BLOCKED_FAMILY_PREFIXES).any()
    assert not registry["source_spec_id"].str.startswith(("dpath_", "ecluster_")).any()


def test_registry_rejects_dispersion_or_event_candidates():
    registry = candidate_registry()
    bad = pd.concat(
        [
            registry,
            registry.iloc[[0]].assign(candidate_id="dpath_01", source_spec_id="dpath_01"),
        ],
        ignore_index=True,
    )
    with pytest.raises(RegistryValidationError):
        validate_vov_registry(bad)


def test_build_vov_panel_has_expected_schema_and_no_family_b_or_c_columns():
    panel = build_vov_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=20)

    assert set(expected_panel_columns()).issubset(panel.columns)
    assert len(panel) == 90 * 60
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        assert panel[f"{candidate_id}_signal"].notna().any()
        assert set(panel[f"{candidate_id}_family"].dropna()) == {"volatility_of_volatility"}
        assert set(panel[f"{candidate_id}_primary_horizon"].dropna()) == {"h10"}

    blocked_cols = [c for c in panel.columns if c.startswith(("dpath_", "ecluster_"))]
    assert blocked_cols == []


def test_warmup_and_missing_data_remain_missing_not_backfilled():
    data = _synthetic_ohlcv(n_dates=90, n_tickers=55)
    data.loc[(data["ticker"] == "T000") & (data["date"] == data["date"].min()), "close"] = np.nan
    panel = build_vov_candidate_panel(data, min_cross_section_count=20)

    early = panel[panel["date"] == panel["date"].min()]
    assert early["vov_01_signal"].isna().all()
    assert (early["vov_01_missing_reason"] == "rolling_warmup").all()

    later = panel[panel["date"] == panel["date"].max()]
    assert later["vov_04_signal"].notna().any()


def test_vov_04_divergence_formula_matches_spec_for_last_date():
    data = _synthetic_ohlcv(n_dates=90, n_tickers=60)
    panel = build_vov_candidate_panel(data, min_cross_section_count=20)
    last = panel[panel["date"] == panel["date"].max()].copy()

    # vov_04 raw score is:
    # abs(rank_cs(delta(vol_20,10)) - rank_cs(vov_slope_10))
    # * rank_cs(low_extension_20) * rank_cs(-abs(ret_20)).
    # Recompute from exposed diagnostic fields plus vol_20 lag on the built panel.
    hist = panel.sort_values(["ticker", "date"]).copy()
    hist["delta_vol_20_10"] = hist["vol_20"] - hist.groupby("ticker")["vol_20"].shift(10)
    last_hist = hist[hist["date"] == hist["date"].max()].copy()
    component = (
        (last_hist["delta_vol_20_10"].rank(pct=True) - last_hist["vov_slope_10"].rank(pct=True)).abs()
        * last_hist["low_extension_20"].rank(pct=True)
        * (-last_hist["ret_20"].abs()).rank(pct=True)
    )
    expected_signal = component.rank(pct=True)
    actual_signal = last.set_index("ticker")["vov_04_signal"].loc[last_hist["ticker"]].reset_index(drop=True)
    pd.testing.assert_series_equal(
        actual_signal.reset_index(drop=True),
        expected_signal.reset_index(drop=True),
        check_names=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )


def test_module_guardrail_manifest_confirms_no_execution_paths():
    manifest = module_guardrail_manifest()
    assert manifest["implemented_candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert manifest["dispersion_path_dependence_implemented"] is False
    assert manifest["event_clustering_implemented"] is False
    assert manifest["panel_generation_executed"] is False
    assert manifest["ic_scoring_executed"] is False
    assert manifest["discovery_executed"] is False
    assert manifest["redundancy_screening_executed"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False


def test_input_schema_is_enforced():
    data = _synthetic_ohlcv().drop(columns=[RAW_INPUT_COLUMNS[-1]])
    with pytest.raises(ValueError, match="missing required columns"):
        build_vov_candidate_panel(data, min_cross_section_count=20)
