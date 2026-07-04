from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df


MODULE_ID = "ohlcv_volatility_of_volatility_refinement_v1"
CREATED_BY_SPEC = "ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1"
FAMILY = "volatility_of_volatility"
RESEARCH_STATUS = "RESEARCH_ONLY"
TIMING_POLICY = "after_close_t_forward_returns_after_t"
RAW_INPUT_COLUMNS = ("date", "ticker", "open", "high", "low", "close", "volume")
IMPLEMENTED_REFINEMENT_IDS = (
    "vov_01_ref_anchor",
    "vov_01_ref_strict_calm",
    "vov_01_ref_longer_memory",
    "vov_01_ref_smoothed_calm",
    "vov_03_ref_anchor",
    "vov_03_ref_strict_chop",
    "vov_03_ref_longer_chop",
    "vov_03_ref_extension_controlled",
)
BLOCKED_CANDIDATE_IDS = ("vov_05", "vov_02", "vov_04")
BLOCKED_FAMILY_PREFIXES = ("dpath_", "ecluster_")
LONG_FORM_PANEL_COLUMNS = (
    "date",
    "ticker",
    "candidate_id",
    "source_spec_id",
    "parent_candidate_id",
    "module_id",
    "family",
    "research_status",
    "primary_horizon",
    "secondary_horizons",
    "signal_value",
    "raw_score",
    "pre_activation_raw_score",
    "is_active",
    "feature_warmup_complete",
    "finite_cross_section_count",
    "rank_min_count",
    "missing_reason",
    "timing_policy",
    "created_by_spec",
)


@dataclass(frozen=True)
class VoVRefinementDefinition:
    candidate_id: str
    signal_name: str
    source_spec_id: str
    parent_candidate_id: str
    refinement_purpose: str
    primary_horizon: str
    secondary_horizons: tuple[str, ...]
    expected_sign: str
    formula_summary: str
    activation_summary: str
    contamination_checks: tuple[str, ...]


REFINEMENT_CANDIDATES: tuple[VoVRefinementDefinition, ...] = (
    VoVRefinementDefinition(
        candidate_id="vov_01_ref_anchor",
        signal_name="vov_01_ref_anchor",
        source_spec_id="vov_01_instability_calm_after_chop__ref_anchor",
        parent_candidate_id="vov_01",
        refinement_purpose="Preserve original anchor.",
        primary_horizon="h20",
        secondary_horizons=("h10", "h5"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) "
            "* rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(vov_5_20,5) > date q50 and vov_slope_5 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_01_ref_strict_calm",
        signal_name="vov_01_ref_strict_calm",
        source_spec_id="vov_01_instability_calm_after_chop__ref_strict_calm",
        parent_candidate_id="vov_01",
        refinement_purpose="Test stricter prior instability activation.",
        primary_horizon="h20",
        secondary_horizons=("h10",),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) "
            "* rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(vov_5_20,5) > date q66.7 and vov_slope_5 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_01_ref_longer_memory",
        signal_name="vov_01_ref_longer_memory",
        source_spec_id="vov_01_instability_calm_after_chop__ref_longer_memory",
        parent_candidate_id="vov_01",
        refinement_purpose="Test longer-memory VoV calm.",
        primary_horizon="h20",
        secondary_horizons=("h10",),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(vov_10_40,10)) * rank_cs(-vov_slope_10) "
            "* rank_cs(lag(range_chop_40,10)) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(vov_10_40,10) > date q50 and vov_slope_10 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_01_ref_smoothed_calm",
        signal_name="vov_01_ref_smoothed_calm",
        source_spec_id="vov_01_instability_calm_after_chop__ref_smoothed_calm",
        parent_candidate_id="vov_01",
        refinement_purpose="Test slope-noise reduction.",
        primary_horizon="h20",
        secondary_horizons=("h10", "h5"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5_smooth_3) "
            "* rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(vov_5_20,5) > date q50 and vov_slope_5_smooth_3 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_03_ref_anchor",
        signal_name="vov_03_ref_anchor",
        source_spec_id="vov_03_range_chop_exhaustion__ref_anchor",
        parent_candidate_id="vov_03",
        refinement_purpose="Preserve original anchor.",
        primary_horizon="h10",
        secondary_horizons=("h20", "h5"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) "
            "* rank_cs(-abs_ret_10) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(range_chop_20,5) > date q50 and range_chop_slope_5 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_03_ref_strict_chop",
        signal_name="vov_03_ref_strict_chop",
        source_spec_id="vov_03_range_chop_exhaustion__ref_strict_chop",
        parent_candidate_id="vov_03",
        refinement_purpose="Test stricter prior chop activation.",
        primary_horizon="h10",
        secondary_horizons=("h20",),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) "
            "* rank_cs(-abs_ret_10) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(range_chop_20,5) > date q66.7 and range_chop_slope_5 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_03_ref_longer_chop",
        signal_name="vov_03_ref_longer_chop",
        source_spec_id="vov_03_range_chop_exhaustion__ref_longer_chop",
        parent_candidate_id="vov_03",
        refinement_purpose="Test longer-memory chop exhaustion.",
        primary_horizon="h10",
        secondary_horizons=("h20", "h5"),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(range_chop_40,10)) * rank_cs(-range_chop_slope_10) "
            "* rank_cs(-abs_ret_10) * rank_cs(low_extension_20)"
        ),
        activation_summary="lag(range_chop_40,10) > date q50 and range_chop_slope_10 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
    VoVRefinementDefinition(
        candidate_id="vov_03_ref_extension_controlled",
        signal_name="vov_03_ref_extension_controlled",
        source_spec_id="vov_03_range_chop_exhaustion__ref_extension_controlled",
        parent_candidate_id="vov_03",
        refinement_purpose="Strengthen extension/reversal contamination control.",
        primary_horizon="h10",
        secondary_horizons=("h20",),
        expected_sign="positive",
        formula_summary=(
            "rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) "
            "* rank_cs(-abs_ret_10) * rank_cs(low_extension_20) * rank_cs(1 - rank_cs(abs_ret_10))"
        ),
        activation_summary="lag(range_chop_20,5) > date q50 and range_chop_slope_5 < 0",
        contamination_checks=(
            "volatility_compression",
            "hostile_stress_repair",
            "persistence_rank_stability",
            "rank_coherence",
            "plain_reversal",
            "volume_shock_reversal",
            "vov_05_watch",
        ),
    ),
)

REQUIRED_REGISTRY_COLUMNS = {
    "candidate_id",
    "signal_name",
    "source_spec_id",
    "parent_candidate_id",
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


def candidate_registry() -> pd.DataFrame:
    rows = []
    for candidate in REFINEMENT_CANDIDATES:
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "signal_name": candidate.signal_name,
                "source_spec_id": candidate.source_spec_id,
                "parent_candidate_id": candidate.parent_candidate_id,
                "family": FAMILY,
                "theme": "Volatility-of-Volatility bounded refinement",
                "feature_group": "vov_refinement_path_shape",
                "horizon": candidate.primary_horizon,
                "secondary_horizons": ",".join(candidate.secondary_horizons),
                "research_status": RESEARCH_STATUS,
                "run_id": MODULE_ID,
                "expected_sign": candidate.expected_sign,
                "candidate_name": candidate.refinement_purpose,
                "formula_summary": candidate.formula_summary,
                "activation_summary": candidate.activation_summary,
                "contamination_checks": ",".join(candidate.contamination_checks),
                "redundancy_risk": "medium-high",
            }
        )
    return pd.DataFrame(rows)


def validate_refinement_registry(registry: pd.DataFrame | None = None) -> None:
    registry = candidate_registry() if registry is None else registry.copy()
    validate_registry_df(registry)

    missing = REQUIRED_REGISTRY_COLUMNS - set(registry.columns)
    if missing:
        raise RegistryValidationError(f"VoV refinement registry missing columns: {sorted(missing)}")

    ids = tuple(registry["candidate_id"])
    if ids != IMPLEMENTED_REFINEMENT_IDS:
        raise RegistryValidationError(
            f"VoV refinement must implement exactly {IMPLEMENTED_REFINEMENT_IDS}; observed {ids}"
        )
    if any(cid in set(BLOCKED_CANDIDATE_IDS) for cid in registry["candidate_id"]):
        raise RegistryValidationError("Blocked VoV watch/park candidates are not refinement variants")
    if any(str(cid).startswith(BLOCKED_FAMILY_PREFIXES) for cid in registry["candidate_id"]):
        raise RegistryValidationError("Family B/C candidates are blocked from VoV refinement")
    if set(registry["parent_candidate_id"]) != {"vov_01", "vov_03"}:
        raise RegistryValidationError("VoV refinement may only use vov_01 and vov_03 parents")
    if set(registry["family"]) != {FAMILY}:
        raise RegistryValidationError("VoV refinement must contain only volatility_of_volatility rows")
    if set(registry["research_status"]) != {RESEARCH_STATUS}:
        raise RegistryValidationError("VoV refinement candidates must be research-only")


def _require_input_columns(ohlcv: pd.DataFrame) -> None:
    missing = set(RAW_INPUT_COLUMNS) - set(ohlcv.columns)
    if missing:
        raise ValueError(f"VoV refinement input panel missing required columns: {sorted(missing)}")


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


def _finite_cross_section_count(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    values = pd.Series(values, index=frame.index)
    return values.notna().groupby(frame["date"], sort=False).transform("sum").astype("int64")


def _date_quantile(frame: pd.DataFrame, values: pd.Series, q: float) -> pd.Series:
    return values.groupby(frame["date"], sort=False).transform(lambda s: s.quantile(q))


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


def compute_refinement_features(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = 50,
) -> pd.DataFrame:
    frame = prepare_ohlcv_frame(ohlcv)
    close_lag_1 = _lag_by_ticker(frame, frame["close"], 1)
    close_lag_10 = _lag_by_ticker(frame, frame["close"], 10)
    close_lag_20 = _lag_by_ticker(frame, frame["close"], 20)

    frame["ret_1"] = _safe_div(frame["close"], close_lag_1) - 1.0
    frame["ret_10"] = _safe_div(frame["close"], close_lag_10) - 1.0
    frame["ret_20"] = _safe_div(frame["close"], close_lag_20) - 1.0
    frame["abs_ret_10"] = frame["ret_10"].abs()
    frame["abs_ret_20"] = frame["ret_20"].abs()
    frame["range_1"] = _safe_div(frame["high"] - frame["low"], frame["close"])

    frame["vol_5"] = _rolling_by_ticker(frame, frame["ret_1"], 5, "std")
    frame["vol_10"] = _rolling_by_ticker(frame, frame["ret_1"], 10, "std")
    frame["vov_5_20"] = _rolling_by_ticker(frame, frame["vol_5"], 20, "std")
    frame["vov_10_40"] = _rolling_by_ticker(frame, frame["vol_10"], 40, "std")
    frame["vov_slope_5"] = frame["vov_5_20"] - _lag_by_ticker(frame, frame["vov_5_20"], 5)
    frame["vov_slope_10"] = frame["vov_10_40"] - _lag_by_ticker(frame, frame["vov_10_40"], 10)
    frame["vov_slope_5_smooth_3"] = _rolling_by_ticker(frame, frame["vov_slope_5"], 3, "mean")

    frame["range_chop_20"] = _rolling_by_ticker(frame, frame["range_1"], 20, "std")
    frame["range_chop_40"] = _rolling_by_ticker(frame, frame["range_1"], 40, "std")
    frame["range_chop_slope_5"] = frame["range_chop_20"] - _lag_by_ticker(frame, frame["range_chop_20"], 5)
    frame["range_chop_slope_10"] = frame["range_chop_40"] - _lag_by_ticker(
        frame, frame["range_chop_40"], 10
    )
    frame["low_extension_20"] = 1.0 - _rank_cs_from_frame(
        frame, frame["abs_ret_20"], min_cross_section_count=min_cross_section_count
    )
    return frame


def _variant_raw_scores(
    features: pd.DataFrame,
    *,
    min_cross_section_count: int,
) -> dict[str, tuple[pd.Series, pd.Series]]:
    rank = lambda values: _rank_cs_from_frame(  # noqa: E731
        features, values, min_cross_section_count=min_cross_section_count
    )
    q = lambda values, quantile: _date_quantile(features, values, quantile)  # noqa: E731

    lag_vov_5 = _lag_by_ticker(features, features["vov_5_20"], 5)
    lag_vov_10 = _lag_by_ticker(features, features["vov_10_40"], 10)
    lag_chop_20 = _lag_by_ticker(features, features["range_chop_20"], 5)
    lag_chop_40 = _lag_by_ticker(features, features["range_chop_40"], 10)
    low_ext = features["low_extension_20"]

    raw_vov_01 = rank(lag_vov_5) * rank(-features["vov_slope_5"]) * rank(lag_chop_20) * rank(low_ext)
    active_vov_01 = (lag_vov_5 > q(lag_vov_5, 0.50)) & (features["vov_slope_5"] < 0)

    raw_vov_01_long = (
        rank(lag_vov_10) * rank(-features["vov_slope_10"]) * rank(lag_chop_40) * rank(low_ext)
    )
    active_vov_01_long = (lag_vov_10 > q(lag_vov_10, 0.50)) & (features["vov_slope_10"] < 0)

    raw_vov_01_smooth = (
        rank(lag_vov_5) * rank(-features["vov_slope_5_smooth_3"]) * rank(lag_chop_20) * rank(low_ext)
    )
    active_vov_01_smooth = (lag_vov_5 > q(lag_vov_5, 0.50)) & (
        features["vov_slope_5_smooth_3"] < 0
    )

    raw_vov_03 = (
        rank(lag_chop_20) * rank(-features["range_chop_slope_5"]) * rank(-features["abs_ret_10"]) * rank(low_ext)
    )
    active_vov_03 = (lag_chop_20 > q(lag_chop_20, 0.50)) & (features["range_chop_slope_5"] < 0)

    raw_vov_03_long = (
        rank(lag_chop_40) * rank(-features["range_chop_slope_10"]) * rank(-features["abs_ret_10"]) * rank(low_ext)
    )
    active_vov_03_long = (lag_chop_40 > q(lag_chop_40, 0.50)) & (
        features["range_chop_slope_10"] < 0
    )

    raw_vov_03_ext = raw_vov_03 * rank(1.0 - rank(features["abs_ret_10"]))

    return {
        "vov_01_ref_anchor": (raw_vov_01, active_vov_01),
        "vov_01_ref_strict_calm": (
            raw_vov_01,
            (lag_vov_5 > q(lag_vov_5, 0.667)) & (features["vov_slope_5"] < 0),
        ),
        "vov_01_ref_longer_memory": (raw_vov_01_long, active_vov_01_long),
        "vov_01_ref_smoothed_calm": (raw_vov_01_smooth, active_vov_01_smooth),
        "vov_03_ref_anchor": (raw_vov_03, active_vov_03),
        "vov_03_ref_strict_chop": (
            raw_vov_03,
            (lag_chop_20 > q(lag_chop_20, 0.667)) & (features["range_chop_slope_5"] < 0),
        ),
        "vov_03_ref_longer_chop": (raw_vov_03_long, active_vov_03_long),
        "vov_03_ref_extension_controlled": (raw_vov_03_ext, active_vov_03),
    }


def _missing_reason(pre_raw: pd.Series, active: pd.Series, signal: pd.Series) -> pd.Series:
    reason = pd.Series(pd.NA, index=pre_raw.index, dtype="object")
    reason.loc[pre_raw.isna()] = "rolling_warmup"
    reason.loc[pre_raw.notna() & ~active.fillna(False)] = "inactive_zeroed"
    reason.loc[pre_raw.notna() & active.fillna(False) & signal.isna()] = "insufficient_cross_section"
    return reason


def build_refinement_candidate_panel(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = 50,
) -> pd.DataFrame:
    validate_refinement_registry()
    features = compute_refinement_features(ohlcv, min_cross_section_count=min_cross_section_count)
    raw_scores = _variant_raw_scores(features, min_cross_section_count=min_cross_section_count)
    definitions = {candidate.candidate_id: candidate for candidate in REFINEMENT_CANDIDATES}

    panels = []
    for candidate_id in IMPLEMENTED_REFINEMENT_IDS:
        pre_raw, active = raw_scores[candidate_id]
        active = active.fillna(False)
        raw_score = pre_raw.where(active, 0.0)
        signal = _rank_cs_from_frame(features, raw_score, min_cross_section_count=min_cross_section_count)
        signal = signal.where(pre_raw.notna())
        finite_count = _finite_cross_section_count(features, raw_score.where(pre_raw.notna()))
        definition = definitions[candidate_id]
        panel = pd.DataFrame(
            {
                "date": features["date"],
                "ticker": features["ticker"],
                "candidate_id": candidate_id,
                "source_spec_id": definition.source_spec_id,
                "parent_candidate_id": definition.parent_candidate_id,
                "module_id": MODULE_ID,
                "family": FAMILY,
                "research_status": RESEARCH_STATUS,
                "primary_horizon": definition.primary_horizon,
                "secondary_horizons": ",".join(definition.secondary_horizons),
                "signal_value": signal,
                "raw_score": raw_score.where(pre_raw.notna()),
                "pre_activation_raw_score": pre_raw,
                "is_active": active,
                "feature_warmup_complete": pre_raw.notna(),
                "finite_cross_section_count": finite_count,
                "rank_min_count": min_cross_section_count,
                "missing_reason": _missing_reason(pre_raw, active, signal),
                "timing_policy": TIMING_POLICY,
                "created_by_spec": CREATED_BY_SPEC,
            }
        )
        panels.append(panel)

    combined = pd.concat(panels, ignore_index=True)
    combined["_candidate_order"] = pd.Categorical(
        combined["candidate_id"],
        categories=list(IMPLEMENTED_REFINEMENT_IDS),
        ordered=True,
    )
    combined = combined.sort_values(["_candidate_order", "date", "ticker"]).drop(
        columns=["_candidate_order"]
    )
    return combined.reset_index(drop=True)


def expected_panel_columns() -> tuple[str, ...]:
    return LONG_FORM_PANEL_COLUMNS


def implemented_refinement_ids() -> tuple[str, ...]:
    return IMPLEMENTED_REFINEMENT_IDS


def module_guardrail_manifest() -> dict[str, object]:
    return {
        "module_id": MODULE_ID,
        "implemented_refinement_ids": list(IMPLEMENTED_REFINEMENT_IDS),
        "implemented_family": FAMILY,
        "parent_candidates": ["vov_01", "vov_03"],
        "blocked_candidates": [*BLOCKED_CANDIDATE_IDS, "dpath_*", "ecluster_*"],
        "original_vov_formulas_modified": False,
        "original_vov_panels_modified": False,
        "panel_generation_executed": False,
        "ic_scoring_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
    }
