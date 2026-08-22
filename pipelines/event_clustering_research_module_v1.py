from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pipelines.utils.registry_validation import RegistryValidationError, validate_registry_df


MODULE_ID = "event_clustering_research_module_v1"
SPEC_ID = "event_clustering_formula_and_panel_specification_v1"
FAMILY = "event_clustering"
RESEARCH_STATUS = "RESEARCH_ONLY"
TIMING_POLICY = "after_close_t_forward_returns_after_t"
RANK_MIN_COUNT = 50
EPSILON = 1e-12
RAW_INPUT_COLUMNS = ("date", "ticker", "open", "high", "low", "close", "volume")
OPTIONAL_ADJUSTED_CLOSE_COLUMN = "adjusted_close"
IMPLEMENTED_CANDIDATE_IDS = (
    "ecluster_01_concentrated_absorption",
    "ecluster_02_aligned_pressure_resolution",
    "ecluster_03_fragmented_event_absorption",
    "ecluster_04_deteriorating_cluster_avoidance",
    "ecluster_05_aging_cluster_memory",
)
BLOCKED_FAMILY_PREFIXES = ("dpath_", "vov_")
BLOCKED_MECHANISMS = ("dispersion_path_dependence", "volatility_of_volatility", "refinement", "validation", "ml")
CONTAMINATION_CONTROLS = (
    "vov",
    "volatility_compression",
    "hostile_stress_repair",
    "volume_shock_reversal",
    "rank_coherence",
    "persistence",
    "dispersion_path_dependence",
    "non_hostile_transition",
    "static_dispersion",
    "isolated_event_anchors",
)


@dataclass(frozen=True)
class EventClusterCandidateDefinition:
    candidate_id: str
    candidate_name: str
    mechanism: str
    scientific_question: str
    expected_evidence: str
    primary_horizon: str
    secondary_horizons: tuple[str, ...]
    expected_sign: str
    formula_text: str
    activation_text: str
    required_features: tuple[str, ...]
    anchor_comparators: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    feature_group: str
    redundancy_risk: str


ECLUSTER_CANDIDATES: tuple[EventClusterCandidateDefinition, ...] = (
    EventClusterCandidateDefinition(
        candidate_id="ecluster_01_concentrated_absorption",
        candidate_name="Concentrated Event Absorption",
        mechanism="Event Concentration",
        scientific_question=(
            "Do securities with concentrated nearby events and controlled response behave differently "
            "from isolated-event names?"
        ),
        expected_evidence=(
            "Positive h10 primary evidence, h5 support, h20 durability only; clustered-event behavior "
            "should improve over isolated-event anchors."
        ),
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank((rank_cs(cluster_count_5) * absorption_5 * low_extension_20 * "
            "liquidity_rank_20) - (0.5 * deterioration_5), concentration_active)"
        ),
        activation_text="concentration_active = cluster_count_5 >= 2",
        required_features=(
            "cluster_count_5",
            "absorption_5",
            "deterioration_5",
            "low_extension_20",
            "liquidity_rank_20",
        ),
        anchor_comparators=("static_event_anchor_20", "isolated_event_anchor_20", "isolated_absorption_anchor"),
        stop_conditions=(
            "clustered activation is indistinguishable from isolated-event anchors",
            "volume shock reversal explains the effect",
            "activation is crisis-only",
            "h10 fails while h20 is the only supportive horizon",
        ),
        feature_group="concentrated_absorption",
        redundancy_risk="medium-high",
    ),
    EventClusterCandidateDefinition(
        candidate_id="ecluster_02_aligned_pressure_resolution",
        candidate_name="Aligned Event Pressure Resolution",
        mechanism="Event Alignment And Fragmentation",
        scientific_question="Does coherent multi-event alignment followed by controlled response identify resolved event pressure?",
        expected_evidence="Positive h10 primary evidence when multiple event types align but deterioration remains contained.",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(alignment_score_5 * absorption_5 * low_churn_5 * liquidity_rank_20 * "
            "(1 - deterioration_5), alignment_active)"
        ),
        activation_text="alignment_active = cluster_count_5 >= 2 and event_type_count_5 >= 4 and alignment_score_5 >= 0.60",
        required_features=(
            "alignment_score_5",
            "absorption_5",
            "low_churn_5",
            "liquidity_rank_20",
            "deterioration_5",
            "cluster_count_5",
            "event_type_count_5",
        ),
        anchor_comparators=("same_event_type_mix_without_clustering", "static_event_anchor_20", "isolated_aligned_event_anchor"),
        stop_conditions=(
            "alignment is only volatility instability",
            "volume dominates all aligned states",
            "low churn explains the signal",
            "aligned clusters do not differ from isolated aligned events",
        ),
        feature_group="aligned_pressure_resolution",
        redundancy_risk="high",
    ),
    EventClusterCandidateDefinition(
        candidate_id="ecluster_03_fragmented_event_absorption",
        candidate_name="Fragmented Event Absorption",
        mechanism="Event Alignment And Fragmentation",
        scientific_question=(
            "Do fragmented event clusters that are absorbed carry short-to-medium horizon information "
            "distinct from noisy disagreement?"
        ),
        expected_evidence=(
            "Positive h5 primary evidence with h10 support if event-type disagreement reflects absorption "
            "rather than unresolved deterioration."
        ),
        primary_horizon="h5",
        secondary_horizons=("h10", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(fragmentation_score_5 * absorption_5 * low_extension_20 * liquidity_rank_20 * "
            "(1 - rank_cs(abs(ret_5))), fragmentation_active)"
        ),
        activation_text="fragmentation_active = cluster_count_5 >= 2 and fragmentation_score_5 >= 0.60 and alignment_score_5 < 0.80",
        required_features=(
            "fragmentation_score_5",
            "absorption_5",
            "low_extension_20",
            "liquidity_rank_20",
            "abs_ret_5_rank",
            "cluster_count_5",
            "alignment_score_5",
        ),
        anchor_comparators=("isolated_fragmented_event_anchor", "static_high_event_count_anchor"),
        stop_conditions=(
            "fragmentation is pure noise",
            "evidence is h1-only",
            "hostile/stress state explains the signal",
            "no h5/h10 distinction from isolated fragmented events exists",
        ),
        feature_group="fragmented_event_absorption",
        redundancy_risk="high",
    ),
    EventClusterCandidateDefinition(
        candidate_id="ecluster_04_deteriorating_cluster_avoidance",
        candidate_name="Deteriorating Cluster Avoidance",
        mechanism="Cluster Absorption Versus Deterioration",
        scientific_question="Does avoiding securities with deteriorating repeated-event pressure add information beyond stress repair and reversal?",
        expected_evidence="Positive h5 primary evidence because higher scores represent lower deterioration inside active cluster states.",
        primary_horizon="h5",
        secondary_horizons=("h10", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank((1 - deterioration_5) * rank_cs(cluster_count_5) * low_extension_20 * "
            "liquidity_rank_20 * (1 - stress_proxy_20), deterioration_active)"
        ),
        activation_text="deterioration_active = cluster_count_5 >= 2 and rank_cs(cluster_count_5) >= 0.60",
        required_features=(
            "deterioration_5",
            "cluster_count_5_rank",
            "low_extension_20",
            "liquidity_rank_20",
            "stress_proxy_20",
            "cluster_count_5",
        ),
        anchor_comparators=("isolated_deterioration_anchor", "static_stress_anchor", "static_event_count_anchor"),
        stop_conditions=(
            "candidate is just hostile/stress repair",
            "reversal explains the signal",
            "low stress alone explains the signal",
            "h5/h10 evidence does not differ from static deterioration anchors",
        ),
        feature_group="deteriorating_cluster_avoidance",
        redundancy_risk="high",
    ),
    EventClusterCandidateDefinition(
        candidate_id="ecluster_05_aging_cluster_memory",
        candidate_name="Aging Cluster Memory",
        mechanism="Cluster Aging And Market Memory",
        scientific_question="Does cluster age change the interpretation of repeated events beyond volatility compression or stress repair?",
        expected_evidence="Positive h10 primary evidence when aging or decaying clusters retain absorption quality without fresh deterioration.",
        primary_horizon="h10",
        secondary_horizons=("h5", "h20"),
        expected_sign="positive",
        formula_text=(
            "active_rank(((0.6 * decaying_cluster_10) + (0.4 * persistent_cluster_10)) * "
            "absorption_5 * low_churn_5 * liquidity_rank_20 * (1 - deterioration_5), aging_active)"
        ),
        activation_text="aging_active = persistent_cluster_10 = 1 or decaying_cluster_10 = 1",
        required_features=(
            "decaying_cluster_10",
            "persistent_cluster_10",
            "absorption_5",
            "low_churn_5",
            "liquidity_rank_20",
            "deterioration_5",
        ),
        anchor_comparators=("fresh_only_cluster_anchor", "static_event_count_anchor", "isolated_event_anchor", "volatility_compression_anchor"),
        stop_conditions=(
            "aging is plain volatility compression",
            "persistence or rank coherence explains the signal",
            "h20-only evidence is required",
            "fresh/persistent/decaying states are not distinguishable",
        ),
        feature_group="aging_cluster_memory",
        redundancy_risk="high",
    ),
)

REQUIRED_REGISTRY_COLUMNS = {
    "candidate_id",
    "signal_name",
    "source_spec_id",
    "candidate_name",
    "family",
    "theme",
    "feature_group",
    "horizon",
    "secondary_horizons",
    "research_status",
    "run_id",
    "expected_sign",
    "mechanism",
    "scientific_question",
    "expected_evidence",
    "contamination_checks",
    "anchor_comparators",
    "stop_conditions",
    "formula_summary",
    "activation_summary",
}

LONG_FORM_PANEL_COLUMNS = (
    "date",
    "ticker",
    "candidate_id",
    "candidate_name",
    "module_name",
    "module_id",
    "spec_id",
    "platform_version",
    "mechanism",
    "research_status",
    "primary_horizon",
    "secondary_horizons",
    "expected_sign",
    "signal_value",
    "raw_score",
    "pre_activation_raw_score",
    "is_active",
    "activation_reason",
    "feature_warmup_complete",
    "finite_cross_section_count",
    "rank_min_count",
    "missing_reason",
    "after_close_timing_policy",
    "formula_version",
    "formula_text",
    "activation_text",
    "source_specification",
    "source_review",
    "source_design",
    "anchor_comparators",
    "contamination_reference_set",
    "scientific_question",
    "expected_evidence",
    "stop_conditions",
    "created_by_spec",
)

DIAGNOSTIC_COLUMNS = (
    "cluster_count_5",
    "cluster_count_10",
    "event_type_count_5",
    "alignment_score_5",
    "fragmentation_score_5",
    "absorption_5",
    "deterioration_5",
    "cluster_age_state",
    "fresh_cluster_5",
    "persistent_cluster_10",
    "decaying_cluster_10",
    "static_event_anchor_20",
    "isolated_event_anchor_20",
    "price_event",
    "gap_event",
    "range_event",
    "volume_event",
    "vol_event",
    "event_any",
    "volume_intensity_5",
    "range_intensity_5",
    "price_intensity_5",
    "gap_intensity_5",
    "vol_intensity_5",
    "low_extension_20",
    "low_churn_5",
    "liquidity_rank_20",
    "stress_proxy_20",
    "security_vov_20",
    "vol_compression_20",
    "rank_coherence_proxy_20",
    "persistence_proxy_20",
    "static_dispersion_20",
    "dispersion_path_proxy_10",
    "non_hostile_transition_proxy_20",
)


def candidate_registry() -> pd.DataFrame:
    rows = []
    for candidate in ECLUSTER_CANDIDATES:
        rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "signal_name": candidate.candidate_id,
                "source_spec_id": candidate.candidate_id,
                "candidate_name": candidate.candidate_name,
                "family": FAMILY,
                "theme": "Event Clustering",
                "feature_group": candidate.feature_group,
                "horizon": candidate.primary_horizon,
                "secondary_horizons": "|".join(candidate.secondary_horizons),
                "research_status": RESEARCH_STATUS,
                "run_id": MODULE_ID,
                "expected_sign": candidate.expected_sign,
                "mechanism": candidate.mechanism,
                "scientific_question": candidate.scientific_question,
                "expected_evidence": candidate.expected_evidence,
                "contamination_checks": "|".join(CONTAMINATION_CONTROLS),
                "anchor_comparators": "|".join(candidate.anchor_comparators),
                "stop_conditions": "|".join(candidate.stop_conditions),
                "formula_summary": candidate.formula_text,
                "activation_summary": candidate.activation_text,
                "redundancy_risk": candidate.redundancy_risk,
            }
        )
    return pd.DataFrame(rows)


def validate_event_clustering_registry(registry: pd.DataFrame | None = None) -> None:
    registry = candidate_registry() if registry is None else registry.copy()
    validate_registry_df(registry)

    missing = REQUIRED_REGISTRY_COLUMNS - set(registry.columns)
    if missing:
        raise RegistryValidationError(f"Event Clustering registry missing columns: {sorted(missing)}")

    ids = tuple(registry["candidate_id"])
    if ids != IMPLEMENTED_CANDIDATE_IDS:
        raise RegistryValidationError(
            f"Event Clustering module must implement exactly {IMPLEMENTED_CANDIDATE_IDS}; observed {ids}"
        )
    if len(ids) != 5:
        raise RegistryValidationError("Event Clustering module must implement exactly five candidates")
    if any(str(cid).startswith(BLOCKED_FAMILY_PREFIXES) for cid in registry["candidate_id"]):
        raise RegistryValidationError("DPath and VoV candidates are blocked from the Event Clustering module")
    if set(registry["family"]) != {FAMILY}:
        raise RegistryValidationError("Event Clustering module must contain only event_clustering rows")
    allowed_mechanisms = {
        "Event Concentration",
        "Event Alignment And Fragmentation",
        "Cluster Absorption Versus Deterioration",
        "Cluster Aging And Market Memory",
    }
    if not set(registry["mechanism"]).issubset(allowed_mechanisms):
        raise RegistryValidationError("Event Clustering registry contains an unapproved mechanism")
    if set(registry["research_status"]) != {RESEARCH_STATUS}:
        raise RegistryValidationError("All Event Clustering candidates must be research-only")
    if not set(registry["horizon"]).issubset({"h5", "h10"}):
        raise RegistryValidationError("Event Clustering primary horizons must remain h5 or h10")


def _require_input_columns(ohlcv: pd.DataFrame) -> None:
    missing = set(RAW_INPUT_COLUMNS) - set(ohlcv.columns)
    if missing:
        raise ValueError(f"Event Clustering input panel missing required columns: {sorted(missing)}")


def _safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    out = numerator.astype("float64") / denominator.astype("float64").replace(0.0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)


def _rolling_by_ticker(frame: pd.DataFrame, values: pd.Series, window: int, fn: str) -> pd.Series:
    grouped = values.groupby(frame["ticker"], sort=False)
    if fn == "mean":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).mean())
    elif fn == "std":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).std())
    elif fn == "sum":
        out = grouped.transform(lambda s: s.rolling(window, min_periods=window).sum())
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


def _z_ts_by_ticker(frame: pd.DataFrame, values: pd.Series, window: int) -> pd.Series:
    mean = _rolling_by_ticker(frame, values, window, "mean")
    std = _rolling_by_ticker(frame, values, window, "std")
    centered = values.astype("float64") - mean
    z_score = _safe_div(centered, std)
    return z_score.where(~((std == 0.0) & (centered == 0.0)), 0.0)


def _date_level_mad(values: pd.Series) -> float:
    finite = values.dropna()
    if finite.empty:
        return np.nan
    median = finite.median()
    return float((finite - median).abs().median())


def prepare_ohlcv_frame(ohlcv: pd.DataFrame) -> pd.DataFrame:
    _require_input_columns(ohlcv)
    columns = list(RAW_INPUT_COLUMNS)
    if OPTIONAL_ADJUSTED_CLOSE_COLUMN in ohlcv.columns:
        columns.append(OPTIONAL_ADJUSTED_CLOSE_COLUMN)
    frame = ohlcv.loc[:, columns].copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values(["ticker", "date"]).reset_index(drop=True)
    for col in ("open", "high", "low", "close", "volume", OPTIONAL_ADJUSTED_CLOSE_COLUMN):
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame["px"] = frame[OPTIONAL_ADJUSTED_CLOSE_COLUMN] if OPTIONAL_ADJUSTED_CLOSE_COLUMN in frame.columns else frame["close"]
    return frame


def compute_event_clustering_features(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = RANK_MIN_COUNT,
) -> pd.DataFrame:
    frame = prepare_ohlcv_frame(ohlcv)
    px_lag_1 = _lag_by_ticker(frame, frame["px"], 1)
    px_lag_5 = _lag_by_ticker(frame, frame["px"], 5)
    px_lag_20 = _lag_by_ticker(frame, frame["px"], 20)

    frame["ret_1"] = _safe_div(frame["px"], px_lag_1) - 1.0
    frame["ret_5"] = _safe_div(frame["px"], px_lag_5) - 1.0
    frame["ret_20"] = _safe_div(frame["px"], px_lag_20) - 1.0
    frame["gap_1"] = _safe_div(frame["open"], px_lag_1) - 1.0
    frame["intraday_ret_1"] = _safe_div(frame["close"], frame["open"]) - 1.0
    frame["range_1"] = _safe_div(frame["high"] - frame["low"], px_lag_1)
    close_loc_denominator = (frame["high"] - frame["low"]).clip(lower=EPSILON)
    frame["close_loc_1"] = _safe_div(frame["close"] - frame["low"], close_loc_denominator).clip(0.0, 1.0)
    frame["log_volume_1p"] = np.log1p(frame["volume"].where(frame["volume"] >= 0.0))
    frame["vol_5"] = _rolling_by_ticker(frame, frame["ret_1"], 5, "std")
    frame["dollar_volume_20"] = _rolling_by_ticker(frame, frame["px"] * frame["volume"], 20, "mean")
    frame["ticker_observation_index"] = frame.groupby("ticker", sort=False).cumcount()

    frame["price_event"] = (_z_ts_by_ticker(frame, frame["ret_1"], 60).abs() >= 1.5).astype("float64")
    frame["gap_event"] = (_z_ts_by_ticker(frame, frame["gap_1"], 60).abs() >= 1.5).astype("float64")
    frame["range_event"] = (_z_ts_by_ticker(frame, frame["range_1"], 60) >= 1.5).astype("float64")
    frame["volume_event"] = (_z_ts_by_ticker(frame, frame["log_volume_1p"], 60) >= 1.5).astype("float64")
    frame["vol_event"] = (_z_ts_by_ticker(frame, frame["vol_5"], 60) >= 1.5).astype("float64")
    event_cols = ["price_event", "gap_event", "range_event", "volume_event", "vol_event"]
    frame.loc[frame[event_cols].isna().any(axis=1), event_cols] = np.nan
    frame["event_any"] = frame[event_cols].max(axis=1)
    frame["event_type_count_1"] = frame[event_cols].sum(axis=1)
    frame["cluster_count_5"] = _rolling_by_ticker(frame, frame["event_any"], 5, "sum")
    frame["cluster_count_10"] = _rolling_by_ticker(frame, frame["event_any"], 10, "sum")
    frame["event_type_count_5"] = _rolling_by_ticker(frame, frame["event_type_count_1"], 5, "sum")
    frame["event_any_20"] = _rolling_by_ticker(frame, frame["event_any"], 20, "sum")
    frame["isolated_event_anchor_20"] = (
        (frame["event_any"] == 1.0) & (frame["cluster_count_5"] == 1.0) & (frame["event_any_20"] <= 2.0)
    ).astype("float64")
    frame["static_event_anchor_20"] = _rank_cs_from_frame(
        frame, frame["event_any_20"], min_cross_section_count=min_cross_section_count
    )

    frame["abs_ret_5_rank"] = _rank_cs_from_frame(
        frame, frame["ret_5"].abs(), min_cross_section_count=min_cross_section_count
    )
    frame["absorption_5"] = (
        (1.0 - frame["abs_ret_5_rank"]).clip(0.0, 1.0)
        * _rank_cs_from_frame(
            frame,
            _rolling_by_ticker(frame, frame["close_loc_1"], 5, "mean"),
            min_cross_section_count=min_cross_section_count,
        )
    )
    frame["deterioration_5"] = (
        _rank_cs_from_frame(frame, -frame["ret_5"], min_cross_section_count=min_cross_section_count)
        * _rank_cs_from_frame(
            frame,
            _rolling_by_ticker(frame, frame["range_1"], 5, "mean"),
            min_cross_section_count=min_cross_section_count,
        )
        * (
            1.0
            - _rank_cs_from_frame(
                frame,
                _rolling_by_ticker(frame, frame["close_loc_1"], 5, "mean"),
                min_cross_section_count=min_cross_section_count,
            )
        )
    )
    for event_name in ("volume", "range", "price", "gap", "vol"):
        frame[f"{event_name}_intensity_5"] = _rank_cs_from_frame(
            frame,
            _rolling_by_ticker(frame, frame[f"{event_name}_event"], 5, "sum"),
            min_cross_section_count=min_cross_section_count,
        )
    frame["cluster_count_5_rank"] = _rank_cs_from_frame(
        frame, frame["cluster_count_5"], min_cross_section_count=min_cross_section_count
    )
    frame["alignment_score_5"] = (
        _rank_cs_from_frame(frame, frame["event_type_count_5"], min_cross_section_count=min_cross_section_count)
        * frame["cluster_count_5_rank"]
    )
    fragmentation_raw = (
        (frame["volume_intensity_5"] - frame["price_intensity_5"]).abs()
        + (frame["range_intensity_5"] - frame["gap_intensity_5"]).abs()
        + (frame["vol_intensity_5"] - frame["price_intensity_5"]).abs()
    )
    frame["fragmentation_score_5"] = frame["cluster_count_5_rank"] * _rank_cs_from_frame(
        frame, fragmentation_raw, min_cross_section_count=min_cross_section_count
    )
    lag_cluster_count_5 = _lag_by_ticker(frame, frame["cluster_count_5"], 5)
    frame["fresh_cluster_5"] = ((frame["cluster_count_5"] >= 2.0) & (lag_cluster_count_5 <= 1.0)).astype("float64")
    frame["persistent_cluster_10"] = (
        (frame["cluster_count_10"] >= 4.0) & (frame["cluster_count_5"] >= 2.0)
    ).astype("float64")
    frame["decaying_cluster_10"] = ((lag_cluster_count_5 >= 2.0) & (frame["cluster_count_5"] <= 1.0)).astype("float64")
    frame["cluster_age_state"] = "none"
    frame.loc[frame["fresh_cluster_5"] == 1.0, "cluster_age_state"] = "fresh"
    frame.loc[frame["persistent_cluster_10"] == 1.0, "cluster_age_state"] = "persistent"
    frame.loc[frame["decaying_cluster_10"] == 1.0, "cluster_age_state"] = "decaying"

    ret5_rank = _rank_cs_from_frame(frame, frame["ret_5"], min_cross_section_count=min_cross_section_count)
    frame["rank_churn_5"] = (ret5_rank - _lag_by_ticker(frame, ret5_rank, 5)).abs()
    frame["low_churn_5"] = 1.0 - _rank_cs_from_frame(
        frame, frame["rank_churn_5"], min_cross_section_count=min_cross_section_count
    )
    frame["low_extension_20"] = 1.0 - _rank_cs_from_frame(
        frame, frame["ret_20"].abs(), min_cross_section_count=min_cross_section_count
    )
    frame["liquidity_rank_20"] = _rank_cs_from_frame(
        frame, frame["dollar_volume_20"], min_cross_section_count=min_cross_section_count
    )

    range_20 = _rolling_by_ticker(frame, frame["range_1"], 20, "mean")
    close_loc_20 = _rolling_by_ticker(frame, frame["close_loc_1"], 20, "mean")
    frame["stress_proxy_20"] = (
        _rank_cs_from_frame(frame, -frame["ret_20"], min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, range_20, min_cross_section_count=min_cross_section_count)
        + _rank_cs_from_frame(frame, -close_loc_20, min_cross_section_count=min_cross_section_count)
    ) / 3.0
    frame["security_vov_20"] = _rolling_by_ticker(frame, frame["vol_5"], 20, "std")
    lag_vol_5_10 = _lag_by_ticker(frame, frame["vol_5"], 10)
    frame["vol_compression_20"] = (
        _rank_cs_from_frame(frame, -frame["vol_5"], min_cross_section_count=min_cross_section_count)
        * _rank_cs_from_frame(frame, lag_vol_5_10 - frame["vol_5"], min_cross_section_count=min_cross_section_count)
    )
    frame["rank_coherence_proxy_20"] = frame["low_churn_5"] * _rank_cs_from_frame(
        frame, frame["ret_20"].abs(), min_cross_section_count=min_cross_section_count
    )
    frame["persistence_proxy_20"] = _rank_cs_from_frame(
        frame, frame["ret_20"], min_cross_section_count=min_cross_section_count
    )
    frame["non_hostile_transition_proxy_20"] = frame["persistence_proxy_20"] * frame["low_churn_5"] * (
        1.0 - frame["stress_proxy_20"]
    )

    date_features = (
        frame.groupby("date", sort=True)
        .agg(static_dispersion_1=("ret_1", _date_level_mad))
        .reset_index()
    )
    date_features["date_observation_index"] = np.arange(len(date_features), dtype=int)
    date_features["static_dispersion_20"] = (
        date_features["static_dispersion_1"].rolling(20, min_periods=20).mean().astype("float64")
    )
    date_features["dispersion_path_proxy_10"] = (
        date_features["static_dispersion_20"] - date_features["static_dispersion_20"].shift(10)
    )
    frame = frame.merge(
        date_features[["date", "date_observation_index", "static_dispersion_20", "dispersion_path_proxy_10"]],
        on="date",
        how="left",
        validate="many_to_one",
    )

    return frame.sort_values(["date", "ticker"]).reset_index(drop=True)


def _raw_scores(features: pd.DataFrame) -> dict[str, tuple[pd.Series, pd.Series]]:
    concentration_active = features["cluster_count_5"] >= 2.0
    raw_01 = (
        features["cluster_count_5_rank"]
        * features["absorption_5"]
        * features["low_extension_20"]
        * features["liquidity_rank_20"]
    ) - (0.5 * features["deterioration_5"])

    alignment_active = (
        (features["cluster_count_5"] >= 2.0)
        & (features["event_type_count_5"] >= 4.0)
        & (features["alignment_score_5"] >= 0.60)
    )
    raw_02 = (
        features["alignment_score_5"]
        * features["absorption_5"]
        * features["low_churn_5"]
        * features["liquidity_rank_20"]
        * (1.0 - features["deterioration_5"])
    )

    fragmentation_active = (
        (features["cluster_count_5"] >= 2.0)
        & (features["fragmentation_score_5"] >= 0.60)
        & (features["alignment_score_5"] < 0.80)
    )
    raw_03 = (
        features["fragmentation_score_5"]
        * features["absorption_5"]
        * features["low_extension_20"]
        * features["liquidity_rank_20"]
        * (1.0 - features["abs_ret_5_rank"])
    )

    deterioration_active = (features["cluster_count_5"] >= 2.0) & (features["cluster_count_5_rank"] >= 0.60)
    raw_04 = (
        (1.0 - features["deterioration_5"])
        * features["cluster_count_5_rank"]
        * features["low_extension_20"]
        * features["liquidity_rank_20"]
        * (1.0 - features["stress_proxy_20"])
    )

    aging_active = (features["persistent_cluster_10"] == 1.0) | (features["decaying_cluster_10"] == 1.0)
    raw_05 = (
        ((0.6 * features["decaying_cluster_10"]) + (0.4 * features["persistent_cluster_10"]))
        * features["absorption_5"]
        * features["low_churn_5"]
        * features["liquidity_rank_20"]
        * (1.0 - features["deterioration_5"])
    )

    return {
        "ecluster_01_concentrated_absorption": (raw_01, concentration_active),
        "ecluster_02_aligned_pressure_resolution": (raw_02, alignment_active),
        "ecluster_03_fragmented_event_absorption": (raw_03, fragmentation_active),
        "ecluster_04_deteriorating_cluster_avoidance": (raw_04, deterioration_active),
        "ecluster_05_aging_cluster_memory": (raw_05, aging_active),
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
    raw_missing = features[["open", "high", "low", "close", "volume", "px"]].isna().any(axis=1)
    invalid_raw = (
        (features["open"] <= 0.0)
        | (features["high"] <= 0.0)
        | (features["low"] <= 0.0)
        | (features["close"] <= 0.0)
        | (features["px"] <= 0.0)
        | (features["volume"] < 0.0)
    )
    reason.loc[raw_missing | invalid_raw] = "raw_ohlcv_missing"
    reason.loc[reason.isna() & ~warmup_complete] = "rolling_warmup"
    reason.loc[reason.isna() & raw.isna()] = "nonfinite_feature"
    reason.loc[reason.isna() & active.fillna(False) & signal.isna()] = "insufficient_cross_section"
    reason.loc[reason.isna() & ~active.fillna(False)] = "inactive_neutralized"
    return reason


def _candidate_rows(
    features: pd.DataFrame,
    candidate: EventClusterCandidateDefinition,
    raw: pd.Series,
    active: pd.Series,
    *,
    min_cross_section_count: int,
) -> pd.DataFrame:
    warmup_complete = (features["ticker_observation_index"] >= 64) & (features["date_observation_index"] >= 20)
    pre_activation_raw = raw.where(warmup_complete)
    active = active.fillna(False) & warmup_complete & pre_activation_raw.notna()
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
    rows["module_name"] = MODULE_ID
    rows["module_id"] = MODULE_ID
    rows["spec_id"] = SPEC_ID
    rows["platform_version"] = "v2.0.0-platform-scientific-methodology"
    rows["mechanism"] = candidate.mechanism
    rows["research_status"] = RESEARCH_STATUS
    rows["primary_horizon"] = candidate.primary_horizon
    rows["secondary_horizons"] = "|".join(candidate.secondary_horizons)
    rows["expected_sign"] = candidate.expected_sign
    rows["signal_value"] = signal
    rows["raw_score"] = raw_score
    rows["pre_activation_raw_score"] = pre_activation_raw
    rows["is_active"] = active
    rows["activation_reason"] = np.where(active, "active", "inactive_or_unavailable")
    rows["feature_warmup_complete"] = warmup_complete
    rows["finite_cross_section_count"] = finite_count
    rows["rank_min_count"] = min_cross_section_count
    rows["missing_reason"] = missing_reason
    rows["after_close_timing_policy"] = TIMING_POLICY
    rows["formula_version"] = "v1"
    rows["formula_text"] = candidate.formula_text
    rows["activation_text"] = candidate.activation_text
    rows["source_specification"] = "docs/research_notes/event_clustering_formula_and_panel_specification_v1.md"
    rows["source_review"] = "docs/research_notes/event_clustering_scientific_review_v1.md"
    rows["source_design"] = "docs/research_notes/event_clustering_research_module_design_v1.md"
    rows["anchor_comparators"] = "|".join(candidate.anchor_comparators)
    rows["contamination_reference_set"] = "|".join(CONTAMINATION_CONTROLS)
    rows["scientific_question"] = candidate.scientific_question
    rows["expected_evidence"] = candidate.expected_evidence
    rows["stop_conditions"] = "|".join(candidate.stop_conditions)
    rows["created_by_spec"] = SPEC_ID
    return rows


def build_event_clustering_candidate_panel(
    ohlcv: pd.DataFrame,
    *,
    min_cross_section_count: int = RANK_MIN_COUNT,
) -> pd.DataFrame:
    validate_event_clustering_registry()
    features = compute_event_clustering_features(ohlcv, min_cross_section_count=min_cross_section_count)
    raw_scores = _raw_scores(features)
    definitions = {candidate.candidate_id: candidate for candidate in ECLUSTER_CANDIDATES}
    panels = []
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        raw, active = raw_scores[candidate_id]
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


def blocked_family_prefixes() -> tuple[str, ...]:
    return BLOCKED_FAMILY_PREFIXES


def module_guardrail_manifest() -> dict[str, object]:
    return {
        "module_id": MODULE_ID,
        "spec_id": SPEC_ID,
        "classification": "IMPLEMENTATION_READY_WITH_NOTES",
        "implemented_candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "implemented_candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_family_prefixes": list(BLOCKED_FAMILY_PREFIXES),
        "blocked_mechanisms": list(BLOCKED_MECHANISMS),
        "extra_ecluster_candidates_implemented": False,
        "dpath_candidates_implemented": False,
        "vov_candidates_implemented": False,
        "refinement_variants_implemented": False,
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
