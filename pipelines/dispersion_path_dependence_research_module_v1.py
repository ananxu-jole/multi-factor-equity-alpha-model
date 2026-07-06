from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df


MODULE_ID = "dispersion_path_dependence_research_module_v1"
SPEC_ID = "dispersion_path_dependence_formula_and_panel_specification_v1"
FAMILY = "dispersion_path_dependence"
RESEARCH_STATUS = "RESEARCH_ONLY"
TIMING_POLICY = "after_close_t_forward_returns_after_t"
RANK_MIN_COUNT = 50
RAW_INPUT_COLUMNS = ("date", "ticker", "open", "high", "low", "close", "volume")
IMPLEMENTED_CANDIDATE_IDS = (
    "dpath_01_relapse_resilience_after_calm",
    "dpath_02_disagreement_vol_stress_divergence",
    "dpath_03_elevated_disagreement_stabilization",
    "dpath_04_consensus_without_crowding",
)
BLOCKED_CANDIDATE_IDS = (
    "dpath_05_smooth_versus_burst_resolution",
    "dpath_05",
)
BLOCKED_FAMILY_PREFIXES = ("vov_", "ecluster_")
BLOCKED_MECHANISMS = ("smooth_versus_burst_resolution", "event_clustering")


@dataclass(frozen=True)
class DPathCandidateDefinition:
    candidate_id: str
    candidate_name: str
    mechanism_family: str
    scientific_question: str
    hypothesis: str
    expected_evidence: str
    primary_falsification_criterion: str
    observable_implication: str
    expected_orthogonality: str
    contamination_risks: tuple[str, ...]
    primary_horizon: str
    secondary_horizons: tuple[str, ...]
    expected_sign: str
    formula_text: str
    activation_text: str
    anchor_comparators: tuple[str, ...]
    feature_group: str
    redundancy_risk: str


DPATH_CANDIDATES: tuple[DPathCandidateDefinition, ...] = (
    DPathCandidateDefinition(
        candidate_id="dpath_01_relapse_resilience_after_calm",
        candidate_name="Relapse Resilience After Temporary Calm",
        mechanism_family="Disagreement Relapse Resilience",
        scientific_question=(
            "Do securities resilient during renewed disagreement after temporary calm behave differently "
            "from securities that only appeared strong during calm?"
        ),
        hypothesis=(
            "Securities resilient during renewed disagreement after temporary calm should carry positive "
            "medium-horizon information if disagreement memory matters."
        ),
        expected_evidence=(
            "Positive h10 primary evidence, h5 support, h20 durability only; stable active coverage "
            "across multiple relapse episodes."
        ),
        primary_falsification_criterion=(
            "Park or revise if prior winners, rank persistence, or simple rising dispersion explains the signal."
        ),
        observable_implication=(
            "A calm or partially normalized disagreement state must precede renewed disagreement, and "
            "security-level resilience must be observed during the relapse."
        ),
        expected_orthogonality=(
            "Should differ from static dispersion, rank coherence, persistence, and hostile/stress repair "
            "because the activation is relapse-after-calm."
        ),
        contamination_risks=(
            "persistence",
            "rank_coherence",
            "hostile_stress_repair",
            "static_dispersion_acceleration",
            "volatility_compression",
            "vov",
            "volume_shock_reversal",
        ),
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text="active_rank(rank_ret_5 * low_extension_20 * low_churn_5 * liquidity_rank_20, relapse_active)",
        activation_text=(
            "relapse_active = (lag(disp_z_20, 5) < 0) and (disp_z_20 > 0) and "
            "(disp_slope_5 > 0) and (disp_5 > lag(disp_5, 5))"
        ),
        anchor_comparators=("static_dispersion_anchor_20", "dispersion_relapse_anchor_without_security_resilience"),
        feature_group="disagreement_relapse_resilience",
        redundancy_risk="medium",
    ),
    DPathCandidateDefinition(
        candidate_id="dpath_02_disagreement_vol_stress_divergence",
        candidate_name="Disagreement Path Divergence From Volatility/Stress",
        mechanism_family="Disagreement Path Divergence",
        scientific_question=(
            "Does disagreement path contribute forward information when volatility and stress paths tell a different story?"
        ),
        hypothesis=(
            "Cross-sectional disagreement path may add information when it diverges from volatility, VoV, "
            "or stress-state paths."
        ),
        expected_evidence=(
            "Positive h10 primary evidence with h5 support and lower contamination versus VoV and volatility "
            "compression than stabilization concepts."
        ),
        primary_falsification_criterion=(
            "Park or revise if VoV, volatility compression, or stress repair explains most behavior."
        ),
        observable_implication=(
            "Date-level disagreement path must separate from volatility or stress path, and the security score "
            "must not be a static dispersion level proxy."
        ),
        expected_orthogonality=(
            "Highest expected module orthogonality because the candidate directly tests disagreement path "
            "versus other state paths."
        ),
        contamination_risks=("vov", "volatility_compression", "hostile_stress_repair", "indicator_engineering"),
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(divergence_intensity * low_extension_20 * low_churn_5 * "
            "(1 - rank_cs(abs(ret_10))) * liquidity_rank_20, divergence_active)"
        ),
        activation_text=(
            "divergence_intensity = abs(z_ts(disp_slope_10, 252) - z_ts(mkt_vol_slope_10, 252)) "
            "+ abs(z_ts(disp_slope_10, 252) - z_ts(mkt_stress_slope_10, 252)); "
            "divergence_active = divergence_intensity > median_ts(divergence_intensity, 252)"
        ),
        anchor_comparators=(
            "static_dispersion_anchor_20",
            "dispersion_slope_anchor_10",
            "volatility_path_anchor_20",
            "stress_path_anchor_20",
        ),
        feature_group="disagreement_path_divergence",
        redundancy_risk="medium-high",
    ),
    DPathCandidateDefinition(
        candidate_id="dpath_03_elevated_disagreement_stabilization",
        candidate_name="Elevated Disagreement Stabilization",
        mechanism_family="Elevated Disagreement Stabilization",
        scientific_question=(
            "Do securities that remain orderly while market disagreement is elevated but stabilizing carry "
            "positive forward information?"
        ),
        hypothesis=(
            "Securities that remain orderly while disagreement is elevated but stabilizing should benefit "
            "from orderly repricing."
        ),
        expected_evidence="Positive h10 primary evidence, h5 support, and no h20-only rescue.",
        primary_falsification_criterion=(
            "Park or revise if volatility compression or stress repair explains the behavior."
        ),
        observable_implication=(
            "Disagreement must have been elevated and must now be stabilizing; current low dispersion alone "
            "is not sufficient."
        ),
        expected_orthogonality=(
            "Should differ from static dispersion level by requiring elevated prior disagreement plus current "
            "stabilization path."
        ),
        contamination_risks=("volatility_compression", "hostile_stress_repair", "vov_calming", "rank_coherence"),
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(low_churn_5 * low_extension_20 * (1 - rank_cs(abs(ret_10))) "
            "* liquidity_rank_20, stabilization_active)"
        ),
        activation_text=(
            "stabilization_active = (lag(disp_z_20, 10) > 0.5) and (disp_z_20 > 0) "
            "and (disp_slope_10 < 0) and (abs(disp_slope_5) < abs(lag(disp_slope_5, 5)))"
        ),
        anchor_comparators=("static_dispersion_anchor_20", "elevated_dispersion_level_anchor"),
        feature_group="elevated_disagreement_stabilization",
        redundancy_risk="high",
    ),
    DPathCandidateDefinition(
        candidate_id="dpath_04_consensus_without_crowding",
        candidate_name="Consensus Formation Without Crowding",
        mechanism_family="Consensus Formation Without Crowding",
        scientific_question=(
            "Does disagreement normalization identify securities benefiting from delayed consensus formation "
            "without rewarding crowded leadership?"
        ),
        hypothesis=(
            "Orderly disagreement normalization may identify emerging consensus if it avoids mature leadership crowding."
        ),
        expected_evidence=(
            "Positive h10 primary evidence, h5 support, and separation from parked non-hostile transition "
            "and rank persistence."
        ),
        primary_falsification_criterion=(
            "Park or revise if mature leadership, momentum, or prior winners explain the signal."
        ),
        observable_implication=(
            "Prior disagreement must normalize gradually, and the security score must favor emerging "
            "improvement without mature crowding."
        ),
        expected_orthogonality=(
            "Should differ from parked non-hostile transition by making disagreement normalization primary "
            "and leadership crowding a penalty."
        ),
        contamination_risks=(
            "parked_non_hostile_transition",
            "momentum",
            "rank_coherence",
            "persistence",
            "leadership_crowding",
        ),
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(emerging_improvement_5_20 * low_extension_20 * (1 - leadership_crowding_60) "
            "* low_churn_5 * liquidity_rank_20, consensus_active)"
        ),
        activation_text=(
            "consensus_active = (lag(disp_z_20, 10) > 0) and (disp_slope_10 < 0) "
            "and (disp_z_20 < lag(disp_z_20, 10)) and (disp_z_20 > -0.5)"
        ),
        anchor_comparators=("static_dispersion_anchor_20", "dispersion_normalization_anchor"),
        feature_group="consensus_without_crowding",
        redundancy_risk="high",
    ),
)

REQUIRED_REGISTRY_COLUMNS = {
    "candidate_id",
    "signal_name",
    "candidate_name",
    "family",
    "theme",
    "feature_group",
    "horizon",
    "secondary_horizons",
    "research_status",
    "run_id",
    "expected_sign",
    "mechanism_family",
    "hypothesis",
    "scientific_question",
    "expected_evidence",
    "primary_falsification_criterion",
    "observable_implication",
    "expected_orthogonality",
    "contamination_checks",
    "anchor_comparators",
    "formula_summary",
    "activation_summary",
}

LONG_FORM_PANEL_COLUMNS = (
    "date",
    "ticker",
    "candidate_id",
    "candidate_name",
    "module_id",
    "spec_id",
    "mechanism_family",
    "research_status",
    "primary_horizon",
    "secondary_horizons",
    "expected_sign",
    "signal_value",
    "raw_score",
    "pre_activation_raw_score",
    "is_active",
    "feature_warmup_complete",
    "finite_cross_section_count",
    "rank_min_count",
    "missing_reason",
    "timing_policy",
    "formula_text",
    "activation_text",
    "anchor_comparators",
    "contamination_controls",
    "hypothesis",
    "scientific_question",
    "expected_evidence",
    "primary_falsification_criterion",
    "observable_implication",
    "expected_orthogonality",
    "created_by_spec",
)

DIAGNOSTIC_COLUMNS = (
    "disp_20",
    "disp_z_20",
    "disp_slope_5",
    "disp_slope_10",
    "divergence_intensity",
    "mkt_vol_20",
    "mkt_vol_slope_10",
    "mkt_stress_20",
    "mkt_stress_slope_10",
    "vov_5_20",
    "rank_churn_5",
    "low_churn_5",
    "low_extension_20",
    "leadership_crowding_60",
    "emerging_improvement_5_20",
)


def candidate_registry() -> pd.DataFrame:
    rows = []
    for candidate in DPATH_CANDIDATES:
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "signal_name": candidate.candidate_id,
                "source_spec_id": candidate.candidate_id,
                "candidate_name": candidate.candidate_name,
                "family": FAMILY,
                "theme": "Dispersion Path-Dependence",
                "feature_group": candidate.feature_group,
                "horizon": candidate.primary_horizon,
                "secondary_horizons": "|".join(candidate.secondary_horizons),
                "research_status": RESEARCH_STATUS,
                "run_id": MODULE_ID,
                "expected_sign": candidate.expected_sign,
                "mechanism_family": candidate.mechanism_family,
                "hypothesis": candidate.hypothesis,
                "scientific_question": candidate.scientific_question,
                "expected_evidence": candidate.expected_evidence,
                "primary_falsification_criterion": candidate.primary_falsification_criterion,
                "observable_implication": candidate.observable_implication,
                "expected_orthogonality": candidate.expected_orthogonality,
                "contamination_checks": "|".join(candidate.contamination_risks),
                "anchor_comparators": "|".join(candidate.anchor_comparators),
                "formula_summary": candidate.formula_text,
                "activation_summary": candidate.activation_text,
                "redundancy_risk": candidate.redundancy_risk,
            }
        )
    return pd.DataFrame(rows)


def validate_dpath_registry(registry: pd.DataFrame | None = None) -> None:
    registry = candidate_registry() if registry is None else registry.copy()
    validate_registry_df(registry)

    missing = REQUIRED_REGISTRY_COLUMNS - set(registry.columns)
    if missing:
        raise RegistryValidationError(f"DPath registry missing columns: {sorted(missing)}")

    ids = tuple(registry["candidate_id"])
    if ids != IMPLEMENTED_CANDIDATE_IDS:
        raise RegistryValidationError(
            f"DPath module must implement exactly {IMPLEMENTED_CANDIDATE_IDS}; observed {ids}"
        )
    if any(str(cid).startswith(BLOCKED_FAMILY_PREFIXES) for cid in registry["candidate_id"]):
        raise RegistryValidationError("VoV/Event candidates are blocked from the DPath module")
    if any(cid in set(BLOCKED_CANDIDATE_IDS) for cid in registry["candidate_id"].astype(str)):
        raise RegistryValidationError("Deferred Smooth/Burst candidate is blocked from this batch")
    if set(registry["family"]) != {FAMILY}:
        raise RegistryValidationError("DPath module must contain only dispersion_path_dependence rows")
    if set(registry["horizon"]) != {"h10"}:
        raise RegistryValidationError("All DPath candidates must preserve h10 as primary horizon")
    if set(registry["research_status"]) != {RESEARCH_STATUS}:
        raise RegistryValidationError("All DPath candidates must be research-only")
    if registry["mechanism_family"].nunique() != len(IMPLEMENTED_CANDIDATE_IDS):
        raise RegistryValidationError("Each DPath candidate must map to exactly one distinct approved mechanism")


def _require_input_columns(ohlcv: pd.DataFrame) -> None:
    missing = set(RAW_INPUT_COLUMNS) - set(ohlcv.columns)
    if missing:
        raise ValueError(f"DPath input panel missing required columns: {sorted(missing)}")


def _safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    out = numerator.astype("float64") / denominator.astype("float64").replace(0.0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)


def _rolling_by_ticker(frame: pd.DataFrame, values: pd.Series, window: int, fn: str) -> pd.Series:
    grouped = values.groupby(frame["ticker"], sort=False)
    if fn == "mean":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).mean())
    elif fn == "std":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).std())
    elif fn == "max":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).max())
    else:
        raise ValueError(f"Unsupported rolling function: {fn}")
    return out.astype("float64")


def _lag_by_ticker(frame: pd.DataFrame, values: pd.Series, periods: int) -> pd.Series:
    return values.groupby(frame["ticker"], sort=False).shift(periods).astype("float64")


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


def _date_level_rolling(values: pd.Series, window: int, fn: str) -> pd.Series:
    if fn == "mean":
        return values.rolling(window, min_periods=window).mean().astype("float64")
    if fn == "std":
        return values.rolling(window, min_periods=window).std().astype("float64")
    if fn == "median":
        return values.rolling(window, min_periods=window).median().astype("float64")
    raise ValueError(f"Unsupported date-level rolling function: {fn}")


def _date_level_z(values: pd.Series, window: int) -> pd.Series:
    mean = _date_level_rolling(values, window, "mean")
    std = _date_level_rolling(values, window, "std")
    centered = values - mean
    z_score = _safe_div(centered, std)
    return z_score.where(~((std == 0.0) & (centered == 0.0)), 0.0)


def _date_level_mad(values: pd.Series) -> float:
    values = values.dropna()
    if values.empty:
        return np.nan
    median = values.median()
    return float((values - median).abs().median())


def prepare_ohlcv_frame(ohlcv: pd.DataFrame) -> pd.DataFrame:
    _require_input_columns(ohlcv)
    frame = ohlcv.loc[:, RAW_INPUT_COLUMNS].copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values(["ticker", "date"]).reset_index(drop=True)
    for col in ("open", "high", "low", "close", "volume"):
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    return frame


def compute_dpath_features(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = RANK_MIN_COUNT,
) -> pd.DataFrame:
    frame = prepare_ohlcv_frame(ohlcv)
    close_lag_1 = _lag_by_ticker(frame, frame["close"], 1)
    close_lag_5 = _lag_by_ticker(frame, frame["close"], 5)
    close_lag_10 = _lag_by_ticker(frame, frame["close"], 10)
    close_lag_20 = _lag_by_ticker(frame, frame["close"], 20)
    close_lag_60 = _lag_by_ticker(frame, frame["close"], 60)

    frame["ret_1"] = _safe_div(frame["close"], close_lag_1) - 1.0
    frame["ret_5"] = _safe_div(frame["close"], close_lag_5) - 1.0
    frame["ret_10"] = _safe_div(frame["close"], close_lag_10) - 1.0
    frame["ret_20"] = _safe_div(frame["close"], close_lag_20) - 1.0
    frame["ret_60"] = _safe_div(frame["close"], close_lag_60) - 1.0
    frame["range_1"] = _safe_div(frame["high"] - frame["low"], frame["close"])
    frame["range_20"] = _rolling_by_ticker(frame, frame["range_1"], 20, "mean")
    frame["vol_5"] = _rolling_by_ticker(frame, frame["ret_1"], 5, "std")
    frame["vol_20"] = _rolling_by_ticker(frame, frame["ret_1"], 20, "std")
    frame["vov_5_20"] = _rolling_by_ticker(frame, frame["vol_5"], 20, "std")
    frame["drawdown_20"] = _safe_div(frame["close"], _rolling_by_ticker(frame, frame["close"], 20, "max")) - 1.0
    frame["dollar_volume_20"] = _rolling_by_ticker(frame, frame["close"] * frame["volume"], 20, "mean")
    frame["ticker_observation_index"] = frame.groupby("ticker", sort=False).cumcount()

    frame["rank_ret_5"] = _rank_cs_from_frame(frame, frame["ret_5"], min_cross_section_count=min_cross_section_count)
    frame["low_extension_20"] = 1.0 - _rank_cs_from_frame(
        frame, frame["ret_20"].abs(), min_cross_section_count=min_cross_section_count
    )
    frame["abs_ret_10_rank"] = _rank_cs_from_frame(
        frame, frame["ret_10"].abs(), min_cross_section_count=min_cross_section_count
    )
    ret5_rank = _rank_cs_from_frame(frame, frame["ret_5"], min_cross_section_count=min_cross_section_count)
    frame["rank_churn_5"] = (ret5_rank - _lag_by_ticker(frame, ret5_rank, 5)).abs()
    frame["low_churn_5"] = 1.0 - _rank_cs_from_frame(
        frame, frame["rank_churn_5"], min_cross_section_count=min_cross_section_count
    )
    frame["liquidity_rank_20"] = _rank_cs_from_frame(
        frame, frame["dollar_volume_20"], min_cross_section_count=min_cross_section_count
    )
    frame["leadership_crowding_60"] = (
        _rank_cs_from_frame(frame, frame["ret_60"], min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, frame["ret_60"].abs(), min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, frame["low_churn_5"], min_cross_section_count=min_cross_section_count)
    ) / 3.0
    frame["emerging_improvement_5_20"] = _rank_cs_from_frame(
        frame, frame["ret_5"] - frame["ret_20"] / 4.0, min_cross_section_count=min_cross_section_count
    )
    frame["stress_score_i"] = (
        _rank_cs_from_frame(frame, -frame["ret_5"], min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, frame["range_20"], min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, -frame["drawdown_20"], min_cross_section_count=min_cross_section_count)
    ) / 3.0

    date_features = (
        frame.groupby("date", sort=True)
        .agg(
            disp_1=("ret_1", _date_level_mad),
            mkt_vol_20=("vol_20", "median"),
            mkt_range_20=("range_20", "median"),
            mkt_stress_20=("stress_score_i", "mean"),
            median_vov_5_20=("vov_5_20", "median"),
        )
        .reset_index()
    )
    date_features["date_observation_index"] = np.arange(len(date_features), dtype=int)
    date_features["disp_5"] = _date_level_rolling(date_features["disp_1"], 5, "mean")
    date_features["disp_10"] = _date_level_rolling(date_features["disp_1"], 10, "mean")
    date_features["disp_20"] = _date_level_rolling(date_features["disp_1"], 20, "mean")
    date_features["disp_z_20"] = _date_level_z(date_features["disp_20"], 252)
    date_features["disp_slope_5"] = date_features["disp_5"] - date_features["disp_5"].shift(5)
    date_features["disp_slope_10"] = date_features["disp_10"] - date_features["disp_10"].shift(10)
    date_features["disp_accel_5_10"] = date_features["disp_slope_5"] - date_features["disp_slope_5"].shift(5)
    date_features["mkt_vol_slope_10"] = date_features["mkt_vol_20"] - date_features["mkt_vol_20"].shift(10)
    date_features["mkt_stress_slope_10"] = date_features["mkt_stress_20"] - date_features["mkt_stress_20"].shift(10)
    date_features["vov_path_10"] = date_features["median_vov_5_20"] - date_features["median_vov_5_20"].shift(10)
    date_features["disp_slope_10_z_252"] = _date_level_z(date_features["disp_slope_10"], 252)
    date_features["mkt_vol_slope_10_z_252"] = _date_level_z(date_features["mkt_vol_slope_10"], 252)
    date_features["mkt_stress_slope_10_z_252"] = _date_level_z(date_features["mkt_stress_slope_10"], 252)
    date_features["divergence_intensity"] = (
        (date_features["disp_slope_10_z_252"] - date_features["mkt_vol_slope_10_z_252"]).abs()
        + (date_features["disp_slope_10_z_252"] - date_features["mkt_stress_slope_10_z_252"]).abs()
    )
    date_features["divergence_median_252"] = _date_level_rolling(
        date_features["divergence_intensity"], 252, "median"
    )
    date_features["lag_disp_z_20_5"] = date_features["disp_z_20"].shift(5)
    date_features["lag_disp_z_20_10"] = date_features["disp_z_20"].shift(10)
    date_features["lag_disp_5_5"] = date_features["disp_5"].shift(5)
    date_features["lag_disp_slope_5_5"] = date_features["disp_slope_5"].shift(5)

    frame = frame.merge(date_features, on="date", how="left", validate="many_to_one")
    return frame.sort_values(["date", "ticker"]).reset_index(drop=True)


def _raw_scores(features: pd.DataFrame) -> dict[str, tuple[pd.Series, pd.Series, pd.Series]]:
    finite_base = pd.Series(True, index=features.index)

    relapse_active = (
        (features["lag_disp_z_20_5"] < 0)
        & (features["disp_z_20"] > 0)
        & (features["disp_slope_5"] > 0)
        & (features["disp_5"] > features["lag_disp_5_5"])
    )
    raw_01 = (
        features["rank_ret_5"]
        * features["low_extension_20"]
        * features["low_churn_5"]
        * features["liquidity_rank_20"]
    )

    divergence_active = features["divergence_intensity"] > features["divergence_median_252"]
    raw_02 = (
        features["divergence_intensity"]
        * features["low_extension_20"]
        * features["low_churn_5"]
        * (1.0 - features["abs_ret_10_rank"])
        * features["liquidity_rank_20"]
    )

    stabilization_active = (
        (features["lag_disp_z_20_10"] > 0.5)
        & (features["disp_z_20"] > 0)
        & (features["disp_slope_10"] < 0)
        & (features["disp_slope_5"].abs() < features["lag_disp_slope_5_5"].abs())
    )
    raw_03 = (
        features["low_churn_5"]
        * features["low_extension_20"]
        * (1.0 - features["abs_ret_10_rank"])
        * features["liquidity_rank_20"]
    )

    consensus_active = (
        (features["lag_disp_z_20_10"] > 0)
        & (features["disp_slope_10"] < 0)
        & (features["disp_z_20"] < features["lag_disp_z_20_10"])
        & (features["disp_z_20"] > -0.5)
    )
    raw_04 = (
        features["emerging_improvement_5_20"]
        * features["low_extension_20"]
        * (1.0 - features["leadership_crowding_60"])
        * features["low_churn_5"]
        * features["liquidity_rank_20"]
    )

    return {
        "dpath_01_relapse_resilience_after_calm": (raw_01, relapse_active, finite_base),
        "dpath_02_disagreement_vol_stress_divergence": (raw_02, divergence_active, finite_base),
        "dpath_03_elevated_disagreement_stabilization": (raw_03, stabilization_active, finite_base),
        "dpath_04_consensus_without_crowding": (raw_04, consensus_active, finite_base),
    }


def _finite_cross_section_count(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    return values.notna().groupby(frame["date"], sort=False).transform("sum").astype("int64")


def _missing_reason(
    features: pd.DataFrame,
    raw: pd.Series,
    active: pd.Series,
    signal: pd.Series,
    warmup_complete: pd.Series,
) -> pd.Series:
    reason = pd.Series(pd.NA, index=features.index, dtype="object")
    raw_missing = features[list(RAW_INPUT_COLUMNS[2:])].isna().any(axis=1)
    reason.loc[raw_missing] = "raw_ohlcv_missing"
    reason.loc[reason.isna() & ~warmup_complete] = "rolling_warmup"
    reason.loc[reason.isna() & raw.isna()] = "nonfinite_feature"
    reason.loc[reason.isna() & active.fillna(False) & signal.isna()] = "insufficient_cross_section"
    reason.loc[reason.isna() & ~active.fillna(False)] = "inactive_neutralized"
    return reason


def _candidate_rows(
    features: pd.DataFrame,
    candidate: DPathCandidateDefinition,
    raw: pd.Series,
    active: pd.Series,
    *,
    min_cross_section_count: int,
) -> pd.DataFrame:
    warmup_complete = (features["ticker_observation_index"] >= 60) & (features["date_observation_index"] >= 252)
    active = active.fillna(False) & warmup_complete & raw.notna()
    pre_activation_raw = raw.where(warmup_complete)
    active_signal = _rank_cs_from_frame(
        features,
        pre_activation_raw.where(active),
        min_cross_section_count=min_cross_section_count,
    )
    signal = active_signal.where(active, 0.5)
    signal = signal.where(warmup_complete & pre_activation_raw.notna())
    raw_score = pre_activation_raw.where(active, 0.5).where(warmup_complete & pre_activation_raw.notna())
    finite_count = _finite_cross_section_count(features, pre_activation_raw.where(active))
    missing_reason = _missing_reason(features, pre_activation_raw, active, signal, warmup_complete)

    rows = features[["date", "ticker", *DIAGNOSTIC_COLUMNS]].copy()
    rows["candidate_id"] = candidate.candidate_id
    rows["candidate_name"] = candidate.candidate_name
    rows["module_id"] = MODULE_ID
    rows["spec_id"] = SPEC_ID
    rows["mechanism_family"] = candidate.mechanism_family
    rows["research_status"] = RESEARCH_STATUS
    rows["primary_horizon"] = candidate.primary_horizon
    rows["secondary_horizons"] = "|".join(candidate.secondary_horizons)
    rows["expected_sign"] = candidate.expected_sign
    rows["signal_value"] = signal
    rows["raw_score"] = raw_score
    rows["pre_activation_raw_score"] = pre_activation_raw
    rows["is_active"] = active
    rows["feature_warmup_complete"] = warmup_complete
    rows["finite_cross_section_count"] = finite_count
    rows["rank_min_count"] = min_cross_section_count
    rows["missing_reason"] = missing_reason
    rows["timing_policy"] = TIMING_POLICY
    rows["formula_text"] = candidate.formula_text
    rows["activation_text"] = candidate.activation_text
    rows["anchor_comparators"] = "|".join(candidate.anchor_comparators)
    rows["contamination_controls"] = "|".join(candidate.contamination_risks)
    rows["hypothesis"] = candidate.hypothesis
    rows["scientific_question"] = candidate.scientific_question
    rows["expected_evidence"] = candidate.expected_evidence
    rows["primary_falsification_criterion"] = candidate.primary_falsification_criterion
    rows["observable_implication"] = candidate.observable_implication
    rows["expected_orthogonality"] = candidate.expected_orthogonality
    rows["created_by_spec"] = SPEC_ID
    return rows


def build_dpath_candidate_panel(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = RANK_MIN_COUNT,
) -> pd.DataFrame:
    validate_dpath_registry()
    features = compute_dpath_features(ohlcv, min_cross_section_count=min_cross_section_count)
    raw_scores = _raw_scores(features)
    definitions = {candidate.candidate_id: candidate for candidate in DPATH_CANDIDATES}
    panels = []
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        raw, active, _ = raw_scores[candidate_id]
        panels.append(
            _candidate_rows(
                features,
                definitions[candidate_id],
                raw,
                active,
                min_cross_section_count=min_cross_section_count,
            )
        )
    panel = pd.concat(panels, ignore_index=True)
    ordered = [*LONG_FORM_PANEL_COLUMNS, *DIAGNOSTIC_COLUMNS]
    return panel.loc[:, ordered].sort_values(["date", "candidate_id", "ticker"]).reset_index(drop=True)


def expected_panel_columns() -> tuple[str, ...]:
    return (*LONG_FORM_PANEL_COLUMNS, *DIAGNOSTIC_COLUMNS)


def implemented_candidate_ids() -> tuple[str, ...]:
    return IMPLEMENTED_CANDIDATE_IDS


def blocked_candidate_ids() -> tuple[str, ...]:
    return BLOCKED_CANDIDATE_IDS


def module_guardrail_manifest() -> dict[str, object]:
    return {
        "module_id": MODULE_ID,
        "spec_id": SPEC_ID,
        "classification": "IMPLEMENTATION_READY_WITH_SCIENTIFIC_NOTES",
        "implemented_candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "implemented_candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_ids": list(BLOCKED_CANDIDATE_IDS),
        "blocked_mechanisms": list(BLOCKED_MECHANISMS),
        "smooth_burst_implemented": False,
        "extra_dpath_candidates_implemented": False,
        "vov_candidates_implemented": False,
        "event_clustering_implemented": False,
        "panel_generation_executed": False,
        "ic_scoring_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
        "timing_policy": TIMING_POLICY,
        "research_status": RESEARCH_STATUS,
    }
