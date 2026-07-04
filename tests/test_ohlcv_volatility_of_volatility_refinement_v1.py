from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    BLOCKED_CANDIDATE_IDS,
    IMPLEMENTED_REFINEMENT_IDS,
    RAW_INPUT_COLUMNS,
    build_refinement_candidate_panel,
    candidate_registry,
    expected_panel_columns,
    module_guardrail_manifest,
    validate_refinement_registry,
)
from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    build_vov_candidate_panel,
    implemented_candidate_ids,
)
from pipelines.utils.registry_validation import RegistryValidationError


def _synthetic_ohlcv(n_dates: int = 120, n_tickers: int = 65) -> pd.DataFrame:
    dates = pd.date_range("2024-01-02", periods=n_dates, freq="B")
    rows = []
    for j in range(n_tickers):
        ticker = f"T{j:03d}"
        base = 20.0 + j * 0.25
        for i, date in enumerate(dates):
            wave = np.sin(i / 4.0 + j / 7.0)
            chop = np.cos(i / 3.0 + j / 5.0)
            drift = 0.012 * i
            close = base + drift + wave * (0.5 + j / 200.0)
            open_ = close * (1.0 + 0.002 * np.cos(i / 5.0 + j))
            high = max(open_, close) * (1.0 + 0.01 + 0.003 * abs(chop))
            low = min(open_, close) * (1.0 - 0.01 - 0.002 * abs(wave))
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


def test_registry_contains_exactly_eight_refinement_variants():
    registry = candidate_registry()
    validate_refinement_registry(registry)

    assert tuple(registry["candidate_id"]) == IMPLEMENTED_REFINEMENT_IDS
    assert len(registry) == 8
    assert set(registry["parent_candidate_id"]) == {"vov_01", "vov_03"}
    assert set(registry["family"]) == {"volatility_of_volatility"}
    assert set(registry["research_status"]) == {"RESEARCH_ONLY"}
    assert set(registry["horizon"]) == {"h10", "h20"}
    assert not registry["candidate_id"].isin(BLOCKED_CANDIDATE_IDS).any()
    assert not registry["candidate_id"].str.startswith(("dpath_", "ecluster_")).any()


def test_registry_rejects_blocked_candidates_and_family_b_or_c_ids():
    registry = candidate_registry()

    with pytest.raises(RegistryValidationError):
        validate_refinement_registry(
            pd.concat(
                [registry, registry.iloc[[0]].assign(candidate_id="vov_05")],
                ignore_index=True,
            )
        )

    with pytest.raises(RegistryValidationError):
        validate_refinement_registry(
            pd.concat(
                [registry, registry.iloc[[0]].assign(candidate_id="dpath_01_ref")],
                ignore_index=True,
            )
        )


def test_refinement_panel_uses_long_form_schema_and_expected_ids():
    panel = build_refinement_candidate_panel(_synthetic_ohlcv(), min_cross_section_count=20)

    assert tuple(panel.columns) == expected_panel_columns()
    assert len(panel) == 120 * 65 * 8
    assert tuple(panel["candidate_id"].drop_duplicates()) == IMPLEMENTED_REFINEMENT_IDS
    assert set(panel["module_id"]) == {"ohlcv_volatility_of_volatility_refinement_v1"}
    assert set(panel["family"]) == {"volatility_of_volatility"}
    assert set(panel["research_status"]) == {"RESEARCH_ONLY"}
    assert set(panel["timing_policy"]) == {"after_close_t_forward_returns_after_t"}
    assert not panel["candidate_id"].isin(BLOCKED_CANDIDATE_IDS).any()
    assert not panel["candidate_id"].str.startswith(("dpath_", "ecluster_")).any()
    assert panel.duplicated(["date", "ticker", "candidate_id"]).sum() == 0
    assert panel["signal_value"].notna().any()


def test_anchor_variants_match_original_vov_module_outputs():
    data = _synthetic_ohlcv(n_dates=120, n_tickers=65)
    original = build_vov_candidate_panel(data, min_cross_section_count=20)
    refinement = build_refinement_candidate_panel(data, min_cross_section_count=20)

    for parent_id, refinement_id in (
        ("vov_01", "vov_01_ref_anchor"),
        ("vov_03", "vov_03_ref_anchor"),
    ):
        ref_wide = refinement[refinement["candidate_id"] == refinement_id].sort_values(["date", "ticker"])
        orig_wide = original.sort_values(["date", "ticker"])

        pd.testing.assert_series_equal(
            ref_wide["signal_value"].reset_index(drop=True),
            orig_wide[f"{parent_id}_signal"].reset_index(drop=True),
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )
        pd.testing.assert_series_equal(
            ref_wide["raw_score"].reset_index(drop=True),
            orig_wide[f"{parent_id}_raw_score"].reset_index(drop=True),
            check_names=False,
            check_exact=False,
            rtol=1e-12,
            atol=1e-12,
        )


def test_warmup_and_inactive_semantics_are_preserved():
    data = _synthetic_ohlcv(n_dates=120, n_tickers=65)
    data.loc[(data["ticker"] == "T000") & (data["date"] == data["date"].min()), "close"] = np.nan
    panel = build_refinement_candidate_panel(data, min_cross_section_count=20)

    early = panel[panel["date"] == panel["date"].min()]
    assert early["signal_value"].isna().all()
    assert (early["missing_reason"] == "rolling_warmup").all()

    later = panel[(panel["date"] == panel["date"].max()) & (~panel["is_active"])]
    assert not later.empty
    assert later["raw_score"].eq(0.0).all()
    assert (later["missing_reason"] == "inactive_zeroed").all()


def test_module_guardrails_confirm_no_execution_or_original_mutation():
    manifest = module_guardrail_manifest()
    assert manifest["implemented_refinement_ids"] == list(IMPLEMENTED_REFINEMENT_IDS)
    assert manifest["parent_candidates"] == ["vov_01", "vov_03"]
    assert manifest["blocked_candidates"] == ["vov_05", "vov_02", "vov_04", "dpath_*", "ecluster_*"]
    assert manifest["original_vov_formulas_modified"] is False
    assert manifest["original_vov_panels_modified"] is False
    assert manifest["panel_generation_executed"] is False
    assert manifest["ic_scoring_executed"] is False
    assert manifest["refinement_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["governance_modified"] is False
    assert manifest["production_registration"] is False
    assert manifest["thresholds_modified"] is False
    assert manifest["ml_integration"] is False
    assert implemented_candidate_ids() == ("vov_01", "vov_02", "vov_03", "vov_04", "vov_05")


def test_input_schema_is_enforced():
    data = _synthetic_ohlcv().drop(columns=[RAW_INPUT_COLUMNS[-1]])
    with pytest.raises(ValueError, match="missing required columns"):
        build_refinement_candidate_panel(data, min_cross_section_count=20)
