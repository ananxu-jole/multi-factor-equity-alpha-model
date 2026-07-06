from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.dispersion_path_dependence_research_module_v1 import (
    BLOCKED_CANDIDATE_IDS,
    IMPLEMENTED_CANDIDATE_IDS,
    RAW_INPUT_COLUMNS,
    build_dpath_candidate_panel,
    candidate_registry,
    compute_dpath_features,
    expected_panel_columns,
    module_guardrail_manifest,
    validate_dpath_registry,
)
from pipelines.utils.registry_validation import RegistryValidationError


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
            close = base + slow_trend + amplitude * local_wave + regime_wave + shock
            close = max(close, 2.0)
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


def test_registry_contains_exactly_four_dpath_candidates_with_lineage():
    registry = candidate_registry()
    validate_dpath_registry(registry)

    assert tuple(registry["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert len(registry) == 4
    assert set(registry["family"]) == {"dispersion_path_dependence"}
    assert set(registry["horizon"]) == {"h10"}
    assert set(registry["research_status"]) == {"RESEARCH_ONLY"}
    assert registry["mechanism_family"].nunique() == 4
    assert registry["hypothesis"].str.len().gt(20).all()
    assert registry["scientific_question"].str.len().gt(20).all()
    assert not registry["candidate_id"].isin(BLOCKED_CANDIDATE_IDS).any()
    assert not registry["candidate_id"].str.startswith(("vov_", "ecluster_")).any()
    assert not registry["candidate_id"].str.contains("burst", case=False).any()


def test_registry_rejects_deferred_or_extra_candidates():
    registry = candidate_registry()
    bad = pd.concat(
        [
            registry,
            registry.iloc[[0]].assign(
                candidate_id="dpath_05_smooth_versus_burst_resolution",
                signal_name="dpath_05_smooth_versus_burst_resolution",
            ),
        ],
        ignore_index=True,
    )
    with pytest.raises(RegistryValidationError):
        validate_dpath_registry(bad)


def test_build_dpath_panel_has_long_form_schema_and_no_extra_candidates():
    panel = build_dpath_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=20)

    assert set(expected_panel_columns()).issubset(panel.columns)
    assert tuple(panel["candidate_id"].drop_duplicates()) == IMPLEMENTED_CANDIDATE_IDS
    assert len(panel) == 560 * 60 * 4
    assert panel.duplicated(["date", "ticker", "candidate_id"]).sum() == 0
    assert set(panel["module_id"]) == {"dispersion_path_dependence_research_module_v1"}
    assert set(panel["spec_id"]) == {"dispersion_path_dependence_formula_and_panel_specification_v1"}
    assert set(panel["timing_policy"]) == {"after_close_t_forward_returns_after_t"}
    assert set(panel["primary_horizon"]) == {"h10"}
    assert set(panel["secondary_horizons"]) == {"h5|h20"}
    assert set(panel["expected_sign"]) == {"positive"}
    assert not panel["candidate_id"].str.startswith(("vov_", "ecluster_")).any()
    assert not panel["candidate_id"].str.contains("burst", case=False).any()


def test_warmup_missing_and_inactive_neutralization_are_distinct():
    data = _synthetic_ohlcv(n_dates=560, n_tickers=55)
    data.loc[(data["ticker"] == "T000") & (data["date"] == data["date"].min()), "close"] = np.nan
    panel = build_dpath_candidate_panel(data, min_cross_section_count=20)

    first_date = panel[panel["date"] == panel["date"].min()]
    assert first_date["signal_value"].isna().all()
    assert set(first_date["missing_reason"].dropna()) <= {"raw_ohlcv_missing", "rolling_warmup"}

    mature = panel[panel["feature_warmup_complete"]].copy()
    inactive = mature[mature["is_active"].eq(False) & mature["signal_value"].notna()]
    assert not inactive.empty
    assert set(inactive["signal_value"].dropna().unique()) == {0.5}
    assert set(inactive["missing_reason"].dropna().unique()) == {"inactive_neutralized"}


@pytest.mark.parametrize(
    "candidate_id",
    IMPLEMENTED_CANDIDATE_IDS,
)
def test_candidate_formula_and_activation_match_spec(candidate_id):
    data = _synthetic_ohlcv(n_dates=820, n_tickers=60)
    features = compute_dpath_features(data, min_cross_section_count=20)
    panel = build_dpath_candidate_panel(data, min_cross_section_count=20)

    candidate_panel = panel[(panel["candidate_id"] == candidate_id) & panel["pre_activation_raw_score"].notna()].copy()
    assert not candidate_panel.empty
    target_date = candidate_panel["date"].iloc[-1]

    feature_slice = features[features["date"].eq(target_date)].copy()
    if candidate_id == "dpath_01_relapse_resilience_after_calm":
        expected_raw = (
            feature_slice["rank_ret_5"]
            * feature_slice["low_extension_20"]
            * feature_slice["low_churn_5"]
            * feature_slice["liquidity_rank_20"]
        )
        active = (
            (feature_slice["lag_disp_z_20_5"] < 0)
            & (feature_slice["disp_z_20"] > 0)
            & (feature_slice["disp_slope_5"] > 0)
            & (feature_slice["disp_5"] > feature_slice["lag_disp_5_5"])
        )
    elif candidate_id == "dpath_02_disagreement_vol_stress_divergence":
        expected_raw = (
            feature_slice["divergence_intensity"]
            * feature_slice["low_extension_20"]
            * feature_slice["low_churn_5"]
            * (1.0 - feature_slice["abs_ret_10_rank"])
            * feature_slice["liquidity_rank_20"]
        )
        active = feature_slice["divergence_intensity"] > feature_slice["divergence_median_252"]
    elif candidate_id == "dpath_03_elevated_disagreement_stabilization":
        expected_raw = (
            feature_slice["low_churn_5"]
            * feature_slice["low_extension_20"]
            * (1.0 - feature_slice["abs_ret_10_rank"])
            * feature_slice["liquidity_rank_20"]
        )
        active = (
            (feature_slice["lag_disp_z_20_10"] > 0.5)
            & (feature_slice["disp_z_20"] > 0)
            & (feature_slice["disp_slope_10"] < 0)
            & (feature_slice["disp_slope_5"].abs() < feature_slice["lag_disp_slope_5_5"].abs())
        )
    else:
        expected_raw = (
            feature_slice["emerging_improvement_5_20"]
            * feature_slice["low_extension_20"]
            * (1.0 - feature_slice["leadership_crowding_60"])
            * feature_slice["low_churn_5"]
            * feature_slice["liquidity_rank_20"]
        )
        active = (
            (feature_slice["lag_disp_z_20_10"] > 0)
            & (feature_slice["disp_slope_10"] < 0)
            & (feature_slice["disp_z_20"] < feature_slice["lag_disp_z_20_10"])
            & (feature_slice["disp_z_20"] > -0.5)
        )
    expected_signal = expected_raw.where(active).rank(method="average", pct=True)

    actual_panel = (
        panel[
            (panel["date"].eq(target_date))
            & (panel["candidate_id"].eq(candidate_id))
        ]
        .set_index("ticker")
        .loc[feature_slice["ticker"]]
    )
    pd.testing.assert_series_equal(
        actual_panel["pre_activation_raw_score"].reset_index(drop=True),
        expected_raw.reset_index(drop=True),
        check_names=False,
        check_exact=False,
        rtol=1e-12,
        atol=1e-12,
    )
    pd.testing.assert_series_equal(
        actual_panel["is_active"].reset_index(drop=True),
        active.fillna(False).reset_index(drop=True),
        check_names=False,
    )
    if active.sum() >= 20:
        pd.testing.assert_series_equal(
            actual_panel["signal_value"].reset_index(drop=True),
            expected_signal.reset_index(drop=True),
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )
    else:
        expected_inactive_signal = pd.Series(0.5, index=expected_signal.index)
        pd.testing.assert_series_equal(
            actual_panel["signal_value"].reset_index(drop=True),
            expected_inactive_signal.reset_index(drop=True),
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )


def test_at_least_three_path_states_activate_in_synthetic_fixture():
    panel = build_dpath_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=20)
    active_counts = panel.groupby("candidate_id")["is_active"].sum()

    assert active_counts["dpath_01_relapse_resilience_after_calm"] > 0
    assert active_counts["dpath_03_elevated_disagreement_stabilization"] > 0
    assert active_counts["dpath_04_consensus_without_crowding"] > 0
    assert "dpath_02_disagreement_vol_stress_divergence" in active_counts.index


def test_module_guardrail_manifest_confirms_no_research_execution_paths():
    manifest = module_guardrail_manifest()
    assert manifest["implemented_candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert manifest["implemented_candidate_count"] == 4
    assert manifest["smooth_burst_implemented"] is False
    assert manifest["extra_dpath_candidates_implemented"] is False
    assert manifest["vov_candidates_implemented"] is False
    assert manifest["event_clustering_implemented"] is False
    assert manifest["panel_generation_executed"] is False
    assert manifest["ic_scoring_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False


def test_input_schema_is_enforced():
    data = _synthetic_ohlcv().drop(columns=[RAW_INPUT_COLUMNS[-1]])
    with pytest.raises(ValueError, match="missing required columns"):
        build_dpath_candidate_panel(data, min_cross_section_count=20)
