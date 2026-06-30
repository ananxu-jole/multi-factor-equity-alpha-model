from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df


RUN_ID = "ohlcv_volatility_of_volatility_research_module_v1"
FAMILY = "volatility_of_volatility"
IMPLEMENTED_CANDIDATE_IDS = ("vov_01", "vov_02", "vov_03", "vov_04", "vov_05")
BLOCKED_FAMILY_PREFIXES = ("dpath_", "ecluster_")
RAW_INPUT_COLUMNS = ("date", "ticker", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class VoVCandidateDefinition:
    candidate_id: str
    signal_name: str
    source_spec_id: str
    candidate_name: str
    mechanism_group: str
    primary_horizon: str
    secondary_horizons: tuple[str, ...]
    expected_sign: str
    formula_summary: str
    activation_summary: str
    contamination_checks: tuple[str, ...]


VOV_CANDIDATES: tuple[VoVCandidateDefinition, ...] = (
    VoVCandidateDefinition(
        candidate_id="vov_01",
        signal_name="vov_01_instability_calm_after_chop",
        source_spec_id="vov_01_instability_calm_after_chop",
        candidate_name="Volatility instability calming after choppy risk",
        mechanism_group="Family A - Volatility-of-Volatility",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) "
            "* rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20))"
        ),
        activation_summary="lag(vov_5_20,5) above date median and vov_slope_5 < 0",
        contamination_checks=("volatility_compression", "stress_repair", "rank_coherence"),
    ),
    VoVCandidateDefinition(
        candidate_id="vov_02",
        signal_name="vov_02_low_extension_vov_rise",
        source_spec_id="vov_02_low_extension_vov_rise",
        candidate_name="Low-extension volatility-of-volatility rise",
        mechanism_group="Family A - Volatility-of-Volatility",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(rank_cs(vov_slope_5) * rank_cs(low_extension_20) "
            "* (1 - rank_cs(abs(ret_5))) * rank_cs(dollar_volume))"
        ),
        activation_summary="vov_slope_5 > 0 and abs(ret_20) below date median",
        contamination_checks=("momentum", "plain_reversal", "volatility_level"),
    ),
    VoVCandidateDefinition(
        candidate_id="vov_03",
        signal_name="vov_03_range_chop_exhaustion",
        source_spec_id="vov_03_range_chop_exhaustion",
        candidate_name="Range-chop exhaustion",
        mechanism_group="Family A - Volatility-of-Volatility",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) "
            "* rank_cs(-abs(ret_10)) * rank_cs(low_extension_20))"
        ),
        activation_summary="lag(range_chop_20,5) above date median and range_chop_slope_5 < 0",
        contamination_checks=("stress_repair", "volatility_compression", "reversal"),
    ),
    VoVCandidateDefinition(
        candidate_id="vov_04",
        signal_name="vov_04_vov_slope_divergence",
        source_spec_id="vov_04_vov_slope_divergence",
        candidate_name="Volatility level versus volatility-instability divergence",
        mechanism_group="Family A - Volatility-of-Volatility",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(abs(rank_cs(delta(vol_20,10)) - rank_cs(vov_slope_10)) "
            "* rank_cs(low_extension_20) * rank_cs(-abs(ret_20)))"
        ),
        activation_summary="continuous",
        contamination_checks=("volatility_level", "volatility_compression", "rank_coherence"),
    ),
    VoVCandidateDefinition(
        candidate_id="vov_05",
        signal_name="vov_05_churn_controlled_vov_stabilization",
        source_spec_id="vov_05_churn_controlled_vov_stabilization",
        candidate_name="Low-churn volatility-instability stabilization",
        mechanism_group="Family A - Volatility-of-Volatility",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(rank_cs(-vov_slope_10) * rank_cs(lag(vov_10_40,10)) "
            "* rank_cs(low_churn_5) * rank_cs(low_extension_20))"
        ),
        activation_summary="lag(vov_10_40,10) above date median and vov_slope_10 < 0",
        contamination_checks=("rank_coherence", "persistence", "volatility_compression"),
    ),
)

REQUIRED_REGISTRY_COLUMNS = {
    "candidate_id",
    "signal_name",
    "source_spec_id",
    "family",
    "theme",
    "feature_group",
    "horizon",
    "research_status",
    "run_id",
    "expected_sign",
    "formula_summary",
    "activation_summary",
    "contamination_checks",
}

SHARED_DIAGNOSTIC_COLUMNS = (
    "ret_1",
    "ret_5",
    "ret_10",
    "ret_20",
    "vol_5",
    "vol_20",
    "vov_5_20",
    "vov_10_40",
    "vov_slope_5",
    "vov_slope_10",
    "range_chop_20",
    "range_chop_slope_5",
    "low_extension_20",
    "rank_churn_5",
    "low_churn_5",
)


def candidate_registry() -> pd.DataFrame:
    rows = []
    for candidate in VOV_CANDIDATES:
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "signal_name": candidate.signal_name,
                "source_spec_id": candidate.source_spec_id,
                "family": FAMILY,
                "theme": "Volatility-of-Volatility",
                "feature_group": "vov_path_shape",
                "horizon": candidate.primary_horizon,
                "secondary_horizons": ",".join(candidate.secondary_horizons),
                "research_status": "RESEARCH_ONLY",
                "run_id": RUN_ID,
                "expected_sign": candidate.expected_sign,
                "candidate_name": candidate.candidate_name,
                "formula_summary": candidate.formula_summary,
                "activation_summary": candidate.activation_summary,
                "contamination_checks": ",".join(candidate.contamination_checks),
                "redundancy_risk": "medium-high",
            }
        )
    return pd.DataFrame(rows)


def validate_vov_registry(registry: pd.DataFrame | None = None) -> None:
    registry = candidate_registry() if registry is None else registry.copy()
    validate_registry_df(registry)

    missing = REQUIRED_REGISTRY_COLUMNS - set(registry.columns)
    if missing:
        raise RegistryValidationError(f"VoV registry missing columns: {sorted(missing)}")

    ids = tuple(registry["candidate_id"])
    if ids != IMPLEMENTED_CANDIDATE_IDS:
        raise RegistryValidationError(
            f"VoV module must implement exactly {IMPLEMENTED_CANDIDATE_IDS}; observed {ids}"
        )
    if any(str(cid).startswith(BLOCKED_FAMILY_PREFIXES) for cid in registry["candidate_id"]):
        raise RegistryValidationError("Dispersion/Event candidates are blocked from the VoV module")
    if set(registry["family"]) != {FAMILY}:
        raise RegistryValidationError("VoV module must contain only volatility_of_volatility family rows")
    if set(registry["horizon"]) != {"h10"}:
        raise RegistryValidationError("All VoV candidates must preserve h10 as primary horizon")
    if set(registry["research_status"]) != {"RESEARCH_ONLY"}:
        raise RegistryValidationError("All VoV candidates must be research-only")


def _require_input_columns(ohlcv: pd.DataFrame) -> None:
    missing = set(RAW_INPUT_COLUMNS) - set(ohlcv.columns)
    if missing:
        raise ValueError(f"VoV input panel missing required columns: {sorted(missing)}")


def _rank_cs_from_frame(
    frame: pd.DataFrame,
    values: pd.Series,
    *,
    min_cross_section_count: int,
) -> pd.Series:
    values = pd.Series(values, index=frame.index, dtype="float64")
    ranked = pd.Series(np.nan, index=frame.index, dtype="float64")
    grouped = values.groupby(frame["date"], sort=False)
    for _, idx in grouped.groups.items():
        subset = values.loc[idx]
        if subset.notna().sum() >= min_cross_section_count:
            ranked.loc[idx] = subset.rank(method="average", pct=True)
    return ranked


def _date_median(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    return values.groupby(frame["date"], sort=False).transform("median")


def _rolling_by_ticker(frame: pd.DataFrame, values: pd.Series, window: int, fn: str) -> pd.Series:
    grouped = values.groupby(frame["ticker"], sort=False)
    if fn == "std":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).std())
    elif fn == "mean":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).mean())
    else:
        raise ValueError(f"Unsupported rolling function: {fn}")
    return out.astype("float64")


def _lag_by_ticker(frame: pd.DataFrame, values: pd.Series, periods: int) -> pd.Series:
    return values.groupby(frame["ticker"], sort=False).shift(periods).astype("float64")


def _safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    out = numerator.astype("float64") / denominator.astype("float64").replace(0.0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)


def prepare_ohlcv_frame(ohlcv: pd.DataFrame) -> pd.DataFrame:
    _require_input_columns(ohlcv)
    frame = ohlcv.loc[:, RAW_INPUT_COLUMNS].copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values(["ticker", "date"]).reset_index(drop=True)
    for col in ("open", "high", "low", "close", "volume"):
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    return frame


def compute_vov_features(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = 50,
) -> pd.DataFrame:
    frame = prepare_ohlcv_frame(ohlcv)
    close_lag_1 = _lag_by_ticker(frame, frame["close"], 1)
    close_lag_5 = _lag_by_ticker(frame, frame["close"], 5)
    close_lag_10 = _lag_by_ticker(frame, frame["close"], 10)
    close_lag_20 = _lag_by_ticker(frame, frame["close"], 20)

    frame["ret_1"] = _safe_div(frame["close"], close_lag_1) - 1.0
    frame["ret_5"] = _safe_div(frame["close"], close_lag_5) - 1.0
    frame["ret_10"] = _safe_div(frame["close"], close_lag_10) - 1.0
    frame["ret_20"] = _safe_div(frame["close"], close_lag_20) - 1.0
    frame["abs_ret_1"] = frame["ret_1"].abs()
    frame["range_1"] = _safe_div(frame["high"] - frame["low"], frame["close"])
    frame["dollar_volume"] = frame["close"] * frame["volume"]

    frame["vol_5"] = _rolling_by_ticker(frame, frame["ret_1"], 5, "std")
    frame["vol_10"] = _rolling_by_ticker(frame, frame["ret_1"], 10, "std")
    frame["vol_20"] = _rolling_by_ticker(frame, frame["ret_1"], 20, "std")
    frame["vov_5_20"] = _rolling_by_ticker(frame, frame["vol_5"], 20, "std")
    frame["vov_10_40"] = _rolling_by_ticker(frame, frame["vol_10"], 40, "std")
    frame["vov_slope_5"] = frame["vov_5_20"] - _lag_by_ticker(frame, frame["vov_5_20"], 5)
    frame["vov_slope_10"] = frame["vov_10_40"] - _lag_by_ticker(frame, frame["vov_10_40"], 10)
    frame["range_chop_20"] = _rolling_by_ticker(frame, frame["range_1"], 20, "std")
    frame["range_chop_slope_5"] = frame["range_chop_20"] - _lag_by_ticker(frame, frame["range_chop_20"], 5)

    frame["low_extension_20"] = 1.0 - _rank_cs_from_frame(
        frame, frame["ret_20"].abs(), min_cross_section_count=min_cross_section_count
    )
    ret20_rank = _rank_cs_from_frame(frame, frame["ret_20"], min_cross_section_count=min_cross_section_count)
    frame["rank_churn_5"] = (ret20_rank - _lag_by_ticker(frame, ret20_rank, 5)).abs()
    frame["low_churn_5"] = 1.0 - _rank_cs_from_frame(
        frame, frame["rank_churn_5"], min_cross_section_count=min_cross_section_count
    )

    return frame


def _candidate_raw_scores(
    features: pd.DataFrame,
    *,
    min_cross_section_count: int,
) -> dict[str, tuple[pd.Series, pd.Series]]:
    rank = lambda values: _rank_cs_from_frame(  # noqa: E731
        features, values, min_cross_section_count=min_cross_section_count
    )
    med = lambda values: _date_median(features, values)  # noqa: E731

    lag_vov_5 = _lag_by_ticker(features, features["vov_5_20"], 5)
    lag_range_chop = _lag_by_ticker(features, features["range_chop_20"], 5)
    lag_vov_10 = _lag_by_ticker(features, features["vov_10_40"], 10)
    delta_vol_20_10 = features["vol_20"] - _lag_by_ticker(features, features["vol_20"], 10)

    active_01 = (lag_vov_5 > med(lag_vov_5)) & (features["vov_slope_5"] < 0)
    raw_01 = (
        rank(lag_vov_5)
        * rank(-features["vov_slope_5"])
        * rank(lag_range_chop)
        * rank(features["low_extension_20"])
    )

    active_02 = (features["vov_slope_5"] > 0) & (features["ret_20"].abs() < med(features["ret_20"].abs()))
    raw_02 = (
        rank(features["vov_slope_5"])
        * rank(features["low_extension_20"])
        * (1.0 - rank(features["ret_5"].abs()))
        * rank(features["dollar_volume"])
    )

    active_03 = (lag_range_chop > med(lag_range_chop)) & (features["range_chop_slope_5"] < 0)
    raw_03 = (
        rank(lag_range_chop)
        * rank(-features["range_chop_slope_5"])
        * rank(-features["ret_10"].abs())
        * rank(features["low_extension_20"])
    )

    active_04 = pd.Series(True, index=features.index)
    raw_04 = (
        (rank(delta_vol_20_10) - rank(features["vov_slope_10"])).abs()
        * rank(features["low_extension_20"])
        * rank(-features["ret_20"].abs())
    )

    active_05 = (lag_vov_10 > med(lag_vov_10)) & (features["vov_slope_10"] < 0)
    raw_05 = (
        rank(-features["vov_slope_10"])
        * rank(lag_vov_10)
        * rank(features["low_churn_5"])
        * rank(features["low_extension_20"])
    )

    return {
        "vov_01": (raw_01, active_01),
        "vov_02": (raw_02, active_02),
        "vov_03": (raw_03, active_03),
        "vov_04": (raw_04, active_04),
        "vov_05": (raw_05, active_05),
    }


def _missing_reason(raw: pd.Series, active: pd.Series, signal: pd.Series) -> pd.Series:
    reason = pd.Series(pd.NA, index=raw.index, dtype="object")
    reason.loc[raw.isna()] = "rolling_warmup"
    reason.loc[raw.notna() & ~active.fillna(False)] = "inactive_zeroed"
    reason.loc[raw.notna() & active.fillna(False) & signal.isna()] = "insufficient_cross_section"
    return reason


def build_vov_candidate_panel(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = 50,
) -> pd.DataFrame:
    validate_vov_registry()
    features = compute_vov_features(ohlcv, min_cross_section_count=min_cross_section_count)
    outputs = features[["date", "ticker", *SHARED_DIAGNOSTIC_COLUMNS]].copy()
    raw_scores = _candidate_raw_scores(features, min_cross_section_count=min_cross_section_count)

    definitions = {candidate.candidate_id: candidate for candidate in VOV_CANDIDATES}
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        raw, active = raw_scores[candidate_id]
        active = active.fillna(False)
        active_raw = raw.where(active, 0.0)
        signal = _rank_cs_from_frame(
            features,
            active_raw,
            min_cross_section_count=min_cross_section_count,
        )
        signal = signal.where(raw.notna())
        definition = definitions[candidate_id]
        outputs[f"{candidate_id}_raw_score"] = active_raw.where(raw.notna())
        outputs[f"{candidate_id}_signal"] = signal
        outputs[f"{candidate_id}_active"] = active
        outputs[f"{candidate_id}_family"] = FAMILY
        outputs[f"{candidate_id}_primary_horizon"] = definition.primary_horizon
        outputs[f"{candidate_id}_missing_reason"] = _missing_reason(raw, active, signal)

    return outputs.sort_values(["date", "ticker"]).reset_index(drop=True)


def expected_panel_columns() -> tuple[str, ...]:
    cols = ["date", "ticker", *SHARED_DIAGNOSTIC_COLUMNS]
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        cols.extend(
            [
                f"{candidate_id}_raw_score",
                f"{candidate_id}_signal",
                f"{candidate_id}_active",
                f"{candidate_id}_family",
                f"{candidate_id}_primary_horizon",
                f"{candidate_id}_missing_reason",
            ]
        )
    return tuple(cols)


def implemented_candidate_ids() -> tuple[str, ...]:
    return IMPLEMENTED_CANDIDATE_IDS


def blocked_family_prefixes() -> tuple[str, ...]:
    return BLOCKED_FAMILY_PREFIXES


def module_guardrail_manifest() -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "implemented_candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "implemented_family": FAMILY,
        "dispersion_path_dependence_implemented": False,
        "event_clustering_implemented": False,
        "panel_generation_executed": False,
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
