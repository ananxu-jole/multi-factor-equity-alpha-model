from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.event_clustering_research_module_v1 import (
    CONTAMINATION_CONTROLS,
    IMPLEMENTED_CANDIDATE_IDS,
    RAW_INPUT_COLUMNS,
    build_event_clustering_candidate_panel,
    candidate_registry,
    compute_event_clustering_features,
    expected_panel_columns,
    module_guardrail_manifest,
    validate_event_clustering_registry,
)
from pipelines.utils.registry_validation import RegistryValidationError


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


def test_registry_contains_exactly_five_event_clustering_candidates_with_lineage():
    registry = candidate_registry()
    validate_event_clustering_registry(registry)

    assert tuple(registry["candidate_id"]) == IMPLEMENTED_CANDIDATE_IDS
    assert len(registry) == 5
    assert set(registry["family"]) == {"event_clustering"}
    assert set(registry["research_status"]) == {"RESEARCH_ONLY"}
    assert set(registry["expected_sign"]) == {"positive"}
    assert set(registry["horizon"]) == {"h5", "h10"}
    assert registry["scientific_question"].str.len().gt(20).all()
    assert registry["expected_evidence"].str.len().gt(20).all()
    assert not registry["candidate_id"].str.startswith(("dpath_", "vov_")).any()


def test_registry_rejects_extra_or_foreign_candidates():
    registry = candidate_registry()
    bad_extra = pd.concat(
        [
            registry,
            registry.iloc[[0]].assign(
                candidate_id="ecluster_06_unapproved_extra",
                signal_name="ecluster_06_unapproved_extra",
                source_spec_id="ecluster_06_unapproved_extra",
            ),
        ],
        ignore_index=True,
    )
    with pytest.raises(RegistryValidationError):
        validate_event_clustering_registry(bad_extra)

    bad_foreign = registry.copy()
    bad_foreign.loc[0, "candidate_id"] = "dpath_01_relapse_resilience_after_calm"
    with pytest.raises(RegistryValidationError):
        validate_event_clustering_registry(bad_foreign)


def test_build_event_clustering_panel_has_long_form_schema_and_no_extra_candidates():
    panel = build_event_clustering_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=15)

    assert set(expected_panel_columns()).issubset(panel.columns)
    assert tuple(panel["candidate_id"].drop_duplicates()) == IMPLEMENTED_CANDIDATE_IDS
    assert len(panel) == 150 * 45 * 5
    assert panel.duplicated(["date", "ticker", "candidate_id"]).sum() == 0
    assert set(panel["module_id"]) == {"event_clustering_research_module_v1"}
    assert set(panel["spec_id"]) == {"event_clustering_formula_and_panel_specification_v1"}
    assert set(panel["after_close_timing_policy"]) == {"after_close_t_forward_returns_after_t"}
    assert set(panel["expected_sign"]) == {"positive"}
    assert not panel["candidate_id"].str.startswith(("dpath_", "vov_")).any()
    for control in CONTAMINATION_CONTROLS:
        assert panel["contamination_reference_set"].str.contains(control).all()


def test_warmup_missing_and_inactive_neutralization_are_distinct():
    data = _synthetic_ohlcv(n_dates=150, n_tickers=45)
    data.loc[(data["ticker"] == "T000") & (data["date"] == data["date"].min()), "close"] = np.nan
    panel = build_event_clustering_candidate_panel(data, min_cross_section_count=15)

    first_date = panel[panel["date"] == panel["date"].min()]
    assert first_date["signal_value"].isna().all()
    assert set(first_date["missing_reason"].dropna()) <= {"raw_ohlcv_missing", "rolling_warmup"}

    mature = panel[panel["feature_warmup_complete"]].copy()
    inactive = mature[mature["is_active"].eq(False) & mature["signal_value"].notna()]
    assert not inactive.empty
    assert set(inactive["signal_value"].dropna().unique()) == {0.5}
    assert set(inactive["missing_reason"].dropna().unique()) == {"inactive_neutralized"}


def test_price_and_gap_events_use_absolute_z_score_not_z_score_of_absolute_value():
    data = _synthetic_ohlcv(n_dates=150, n_tickers=45)
    features = compute_event_clustering_features(data, min_cross_section_count=15)
    sorted_features = features.sort_values(["ticker", "date"]).copy()

    ret_mean = sorted_features.groupby("ticker")["ret_1"].transform(lambda s: s.rolling(60, min_periods=60).mean())
    ret_std = sorted_features.groupby("ticker")["ret_1"].transform(lambda s: s.rolling(60, min_periods=60).std())
    gap_mean = sorted_features.groupby("ticker")["gap_1"].transform(lambda s: s.rolling(60, min_periods=60).mean())
    gap_std = sorted_features.groupby("ticker")["gap_1"].transform(lambda s: s.rolling(60, min_periods=60).std())

    expected_price_event = ((sorted_features["ret_1"] - ret_mean) / ret_std.replace(0.0, np.nan)).abs() >= 1.5
    expected_gap_event = ((sorted_features["gap_1"] - gap_mean) / gap_std.replace(0.0, np.nan)).abs() >= 1.5
    mature = sorted_features["ticker_observation_index"] >= 60

    pd.testing.assert_series_equal(
        sorted_features.loc[mature, "price_event"].reset_index(drop=True),
        expected_price_event.loc[mature].astype("float64").reset_index(drop=True),
        check_names=False,
    )
    pd.testing.assert_series_equal(
        sorted_features.loc[mature, "gap_event"].reset_index(drop=True),
        expected_gap_event.loc[mature].astype("float64").reset_index(drop=True),
        check_names=False,
    )


@pytest.mark.parametrize("candidate_id", IMPLEMENTED_CANDIDATE_IDS)
def test_candidate_formula_and_activation_match_frozen_spec(candidate_id):
    data = _synthetic_ohlcv(n_dates=150, n_tickers=45)
    features = compute_event_clustering_features(data, min_cross_section_count=15)
    panel = build_event_clustering_candidate_panel(data, min_cross_section_count=15)

    candidate_panel = panel[(panel["candidate_id"] == candidate_id) & panel["pre_activation_raw_score"].notna()]
    assert not candidate_panel.empty
    target_date = candidate_panel["date"].iloc[-1]
    feature_slice = features[features["date"].eq(target_date)].copy()

    if candidate_id == "ecluster_01_concentrated_absorption":
        expected_raw = (
            feature_slice["cluster_count_5_rank"]
            * feature_slice["absorption_5"]
            * feature_slice["low_extension_20"]
            * feature_slice["liquidity_rank_20"]
        ) - (0.5 * feature_slice["deterioration_5"])
        active = feature_slice["cluster_count_5"] >= 2.0
    elif candidate_id == "ecluster_02_aligned_pressure_resolution":
        expected_raw = (
            feature_slice["alignment_score_5"]
            * feature_slice["absorption_5"]
            * feature_slice["low_churn_5"]
            * feature_slice["liquidity_rank_20"]
            * (1.0 - feature_slice["deterioration_5"])
        )
        active = (
            (feature_slice["cluster_count_5"] >= 2.0)
            & (feature_slice["event_type_count_5"] >= 4.0)
            & (feature_slice["alignment_score_5"] >= 0.60)
        )
    elif candidate_id == "ecluster_03_fragmented_event_absorption":
        expected_raw = (
            feature_slice["fragmentation_score_5"]
            * feature_slice["absorption_5"]
            * feature_slice["low_extension_20"]
            * feature_slice["liquidity_rank_20"]
            * (1.0 - feature_slice["abs_ret_5_rank"])
        )
        active = (
            (feature_slice["cluster_count_5"] >= 2.0)
            & (feature_slice["fragmentation_score_5"] >= 0.60)
            & (feature_slice["alignment_score_5"] < 0.80)
        )
    elif candidate_id == "ecluster_04_deteriorating_cluster_avoidance":
        expected_raw = (
            (1.0 - feature_slice["deterioration_5"])
            * feature_slice["cluster_count_5_rank"]
            * feature_slice["low_extension_20"]
            * feature_slice["liquidity_rank_20"]
            * (1.0 - feature_slice["stress_proxy_20"])
        )
        active = (feature_slice["cluster_count_5"] >= 2.0) & (feature_slice["cluster_count_5_rank"] >= 0.60)
    else:
        expected_raw = (
            ((0.6 * feature_slice["decaying_cluster_10"]) + (0.4 * feature_slice["persistent_cluster_10"]))
            * feature_slice["absorption_5"]
            * feature_slice["low_churn_5"]
            * feature_slice["liquidity_rank_20"]
            * (1.0 - feature_slice["deterioration_5"])
        )
        active = (feature_slice["persistent_cluster_10"] == 1.0) | (feature_slice["decaying_cluster_10"] == 1.0)

    expected_signal = expected_raw.where(active).rank(method="average", pct=True)
    actual_panel = (
        panel[(panel["date"].eq(target_date)) & (panel["candidate_id"].eq(candidate_id))]
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
        (active & expected_raw.notna()).fillna(False).reset_index(drop=True),
        check_names=False,
    )
    if active.sum() >= 15:
        pd.testing.assert_series_equal(
            actual_panel["signal_value"].reset_index(drop=True),
            expected_signal.reset_index(drop=True),
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )


def test_event_cluster_features_include_anchor_and_age_states():
    panel = build_event_clustering_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=15)
    mature = panel[panel["feature_warmup_complete"]]

    assert mature["static_event_anchor_20"].notna().any()
    assert set(mature["isolated_event_anchor_20"].dropna().unique()).issubset({0.0, 1.0})
    assert {"none", "fresh", "persistent", "decaying"}.intersection(set(mature["cluster_age_state"].dropna()))
    assert mature.groupby("candidate_id")["pre_activation_raw_score"].apply(lambda s: s.notna().any()).all()


def test_module_guardrail_manifest_confirms_no_execution_paths():
    manifest = module_guardrail_manifest()
    assert manifest["implemented_candidate_ids"] == list(IMPLEMENTED_CANDIDATE_IDS)
    assert manifest["implemented_candidate_count"] == 5
    assert manifest["extra_ecluster_candidates_implemented"] is False
    assert manifest["dpath_candidates_implemented"] is False
    assert manifest["vov_candidates_implemented"] is False
    assert manifest["refinement_variants_implemented"] is False
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
        build_event_clustering_candidate_panel(data, min_cross_section_count=15)
