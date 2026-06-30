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
    WARMUP_WINDOW,
    _rank_cs,
    _shift_by_ticker,
    _z_cs,
    build_candidate_formula_outputs,
    build_ohlcv_formula_features,
    formula_manifest_rows,
    validate_formula_manifest_rows,
)


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


def test_formula_manifest_is_registry_aligned_and_excludes_removed_candidate():
    rows = formula_manifest_rows()
    ids = [row["candidate_id"] for row in rows]

    assert ids == APPROVED_CANDIDATE_IDS
    assert "nhlr_06" not in ids
    assert set(FORMULA_SPECS) == set(APPROVED_CANDIDATE_IDS)

    ok, errors = validate_formula_manifest_rows(rows)
    assert ok, errors

    drifted = [dict(row) for row in rows]
    drifted[0]["working_name"] = "Drifted Formula Name"
    ok, errors = validate_formula_manifest_rows(drifted)
    assert not ok
    assert any("formula metadata drift" in error for error in errors)


def test_formula_outputs_have_expected_schema_and_no_excluded_candidate():
    outputs = build_candidate_formula_outputs(_synthetic_ohlcv())

    assert list(outputs.columns) == REQUIRED_PANEL_COLUMNS
    assert set(outputs["candidate_id"]) == set(APPROVED_CANDIDATE_IDS)
    assert "nhlr_06" not in set(outputs["candidate_id"])
    assert outputs.groupby("candidate_id")["formula_name"].nunique().eq(1).all()
    assert outputs.groupby("candidate_id")["horizon"].nunique().eq(1).all()
    assert set(outputs["dependency_class"]) == {"OHLCV_ONLY"}
    assert set(outputs["required_input_family"]) == {"OHLCV_DERIVED_ONLY"}


def test_warmup_behavior_blocks_early_signal_values():
    outputs = build_candidate_formula_outputs(_synthetic_ohlcv())
    first_date = outputs["date"].min()
    warm_date = outputs["date"].drop_duplicates().iloc[WARMUP_WINDOW + 5]

    early = outputs[outputs["date"].eq(first_date)]
    warmed = outputs[outputs["date"].eq(warm_date)]

    assert early["warmup_complete"].eq(False).all()
    assert early["signal_value"].isna().all()
    assert set(early["missing_data_reason"]) == {"warmup_incomplete"}
    assert warmed["warmup_complete"].eq(True).all()
    assert warmed["signal_value"].notna().any()


def test_invalid_ohlcv_row_produces_nan_without_forward_fill():
    raw = _synthetic_ohlcv()
    bad_date = raw["date"].drop_duplicates().iloc[WARMUP_WINDOW + 10]
    mask = raw["date"].eq(bad_date) & raw["ticker"].eq("T000")
    raw.loc[mask, "high"] = raw.loc[mask, "low"] - 1

    features = build_ohlcv_formula_features(raw)
    bad_feature_row = features[features["date"].eq(bad_date) & features["ticker"].eq("T000")].iloc[0]
    same_date = features[features["date"].eq(bad_date)]

    assert pd.isna(bad_feature_row["above_ma_50"])
    assert pd.isna(bad_feature_row["above_ma_100"])
    assert same_date["universe_breadth_50"].iloc[0] == same_date["above_ma_50"].mean()

    outputs = build_candidate_formula_outputs(raw)
    bad_rows = outputs[outputs["date"].eq(bad_date) & outputs["ticker"].eq("T000")]
    peer_rows = outputs[outputs["date"].eq(bad_date) & outputs["ticker"].eq("T001")]

    assert bad_rows["signal_value"].isna().all()
    assert set(bad_rows["missing_data_reason"]) == {"invalid_or_missing_ohlcv"}
    assert peer_rows["signal_value"].notna().any()


def test_rotation_acceleration_formula_matches_specified_weighted_sum():
    raw = _synthetic_ohlcv()
    features = build_ohlcv_formula_features(raw)
    outputs = build_candidate_formula_outputs(raw)

    manual_raw = (
        0.35 * _rank_cs(features, features["rank_acceleration_20"])
        + 0.25 * _rank_cs(features, features["rank_velocity_20"])
        + 0.20 * features["rel_strength_20"]
        + 0.10 * features["trend_rank_50"]
        + 0.10 * features["range_control_20"]
    )
    manual_signal = _z_cs(features, manual_raw).where(features["warmup_complete"] & features["valid_ohlcv"])
    candidate = outputs[outputs["candidate_id"].eq("nhlr_07")].reset_index(drop=True)

    pd.testing.assert_series_equal(
        candidate["signal_value"].reset_index(drop=True),
        manual_signal.reset_index(drop=True),
        check_names=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )


def test_formula_features_use_trailing_date_alignment():
    features = build_ohlcv_formula_features(_synthetic_ohlcv())
    ticker_features = features[features["ticker"].eq("T010")].reset_index(drop=True)
    idx = WARMUP_WINDOW + 5

    expected_velocity = ticker_features.loc[idx, "rel_strength_20"] - ticker_features.loc[idx - 20, "rel_strength_20"]
    expected_acceleration = expected_velocity - (
        ticker_features.loc[idx - 20, "rel_strength_20"] - ticker_features.loc[idx - 40, "rel_strength_20"]
    )

    assert ticker_features.loc[idx, "rank_velocity_20"] == expected_velocity
    assert ticker_features.loc[idx, "rank_acceleration_20"] == expected_acceleration
    assert _shift_by_ticker(features, features["rel_strength_20"], 20).notna().any()
