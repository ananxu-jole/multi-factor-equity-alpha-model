from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from pipelines.run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1 import (
    APPROVED_CANDIDATE_IDS,
    candidate_registry_rows,
)


IMPLEMENTATION_STATUS = "CANDIDATE_IMPLEMENTED_RESEARCH_ONLY"
FORMULA_STATUS = "FORMULA_NOT_DEFINED_PANEL_BLOCKED"
PANEL_STATUS = "NO_PANEL_GENERATED"
DISCOVERY_STATUS = "DISCOVERY_NOT_EXECUTED"
IMPLEMENTATION_FINAL_CLASSIFICATION = "READY_FOR_PANEL_GENERATION_REVIEW"
FORMULA_IMPLEMENTATION_CLASSIFICATION = "IMPLEMENTATION_READY_FOR_PANEL_GENERATION_REVIEW"
FORMULA_VERSION = "v1"
WARMUP_WINDOW = 120
MIN_CROSS_SECTIONAL_COUNT = 30
REQUIRED_OHLCV_COLUMNS = ["date", "ticker", "open", "high", "low", "close", "volume"]
REQUIRED_PANEL_COLUMNS = [
    "date",
    "ticker",
    "candidate_id",
    "signal_value",
    "family",
    "theme",
    "horizon",
    "working_name",
    "economic_mechanism",
    "implementation_priority",
    "panel_role",
    "formula_name",
    "formula_version",
    "dependency_class",
    "required_input_family",
    "component_coverage_count",
    "warmup_complete",
    "non_hostile_market_state",
    "source_close_column",
    "missing_data_reason",
]


FORMULA_SPECS = {
    "nhlr_01": {
        "formula_name": "neutral_base_emergence_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10,h5",
        "panel_role": "core early-emergence candidate",
        "required_derived_features": (
            "leadership_delta_60,leadership_delta_20,rel_strength_20,trend_rank_50,"
            "range_control_20,rel_strength_60"
        ),
    },
    "nhlr_02": {
        "formula_name": "quiet_accumulation_before_leadership_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10,h5",
        "panel_role": "core accumulation candidate",
        "required_derived_features": (
            "participation_60,dv_z_60,dv_z_20,range_control_20,vol_control_20,ret_20"
        ),
    },
    "nhlr_03": {
        "formula_name": "post_transition_leadership_durability_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10",
        "panel_role": "durability support candidate",
        "required_derived_features": (
            "leadership_score,leadership_delta_20,rel_strength_60,participation_60,range_control_20"
        ),
    },
    "nhlr_04": {
        "formula_name": "smooth_trend_handoff_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10,h5",
        "panel_role": "core trend-handoff candidate",
        "required_derived_features": "trend_rank_50,range_control_20,vol_control_20,rel_strength_20",
    },
    "nhlr_05": {
        "formula_name": "broadening_participation_without_stress_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10",
        "panel_role": "breadth/participation support candidate",
        "required_derived_features": (
            "non_hostile_market_state,participation_60,breadth_contribution_20,"
            "range_control_20,rel_strength_20"
        ),
    },
    "nhlr_07": {
        "formula_name": "rotation_acceleration_leader_score",
        "primary_horizon": "h10",
        "secondary_review_horizons": "h20,h5",
        "panel_role": "rotation acceleration candidate",
        "required_derived_features": (
            "rank_acceleration_20,rank_velocity_20,rel_strength_20,trend_rank_50,range_control_20"
        ),
    },
    "nhlr_08": {
        "formula_name": "mature_leadership_deceleration_avoidance_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10",
        "panel_role": "lower-priority deceleration-avoidance candidate",
        "required_derived_features": (
            "leadership_score,rank_acceleration_20,rank_velocity_20,participation_60,range_control_20"
        ),
    },
    "nhlr_09": {
        "formula_name": "volume_confirmed_leadership_shift_score",
        "primary_horizon": "h10",
        "secondary_review_horizons": "h20,h5",
        "panel_role": "core confirmation candidate",
        "required_derived_features": (
            "rel_strength_20,leadership_delta_20,dv_z_60,dv_z_20,range_control_20,trend_rank_50"
        ),
    },
    "nhlr_10": {
        "formula_name": "healthy_breadth_contributor_score",
        "primary_horizon": "h20",
        "secondary_review_horizons": "h10",
        "panel_role": "core breadth-contribution candidate",
        "required_derived_features": (
            "non_hostile_market_state,breadth_contribution_20,above_ma_50,above_ma_100,"
            "rel_strength_20,participation_60,range_control_20"
        ),
    },
}


@dataclass(frozen=True)
class CandidateImplementation:
    candidate_id: str
    working_name: str
    family: str
    concept_category: str
    economic_mechanism: str
    implementation_priority: str
    dependency_class: str
    required_input_family: str
    required_ohlcv_inputs: str
    prohibited_dependencies: str
    registry_artifact_namespace: str
    diagnostic_identifier: str
    implementation_status: str
    formula_status: str
    panel_status: str
    discovery_status: str
    implementation_scope: str
    registration_source: str
    implementation_notes: str


def build_candidate_implementations() -> list[CandidateImplementation]:
    implementations: list[CandidateImplementation] = []
    for row in candidate_registry_rows():
        implementations.append(
            CandidateImplementation(
                candidate_id=str(row["candidate_id"]),
                working_name=str(row["working_name"]),
                family=str(row["family"]),
                concept_category=str(row["concept_category"]),
                economic_mechanism=str(row["economic_mechanism"]),
                implementation_priority=str(row["implementation_priority"]),
                dependency_class=str(row["dependency_class"]),
                required_input_family=str(row["required_input_family"]),
                required_ohlcv_inputs=str(row["required_ohlcv_inputs"]),
                prohibited_dependencies=str(row["prohibited_dependencies"]),
                registry_artifact_namespace=str(row["artifact_namespace"]),
                diagnostic_identifier=str(row["diagnostic_identifier"]),
                implementation_status=IMPLEMENTATION_STATUS,
                formula_status=FORMULA_STATUS,
                panel_status=PANEL_STATUS,
                discovery_status=DISCOVERY_STATUS,
                implementation_scope="registry_derived_candidate_shell",
                registration_source="authoritative_candidate_registry",
                implementation_notes=str(row["reviewer_notes"]),
            )
        )
    return implementations


def implementation_rows() -> list[dict[str, object]]:
    return [implementation.__dict__.copy() for implementation in build_candidate_implementations()]


def registered_candidate_ids() -> list[str]:
    return [implementation.candidate_id for implementation in build_candidate_implementations()]


def validate_candidate_implementations(
    rows: list[dict[str, object]] | None = None,
) -> tuple[bool, list[str], list[dict[str, object]]]:
    implementation_rows_to_validate = implementation_rows() if rows is None else rows
    errors: list[str] = []
    report: list[dict[str, object]] = []

    def add_check(check_name: str, passed: bool, notes: str) -> None:
        report.append(
            {
                "check_name": check_name,
                "status": "PASS" if passed else "FAIL",
                "implementation_status": IMPLEMENTATION_STATUS,
                "notes": notes,
            }
        )
        if not passed:
            errors.append(f"{check_name}: {notes}")

    ids = [str(row.get("candidate_id", "")).strip() for row in implementation_rows_to_validate]
    duplicate_ids = sorted({candidate_id for candidate_id in ids if ids.count(candidate_id) > 1})
    missing_ids = sorted(set(APPROVED_CANDIDATE_IDS) - set(ids))
    unexpected_ids = sorted(set(ids) - set(APPROVED_CANDIDATE_IDS))
    required_fields = list(CandidateImplementation.__dataclass_fields__)

    add_check(
        "implemented_candidate_count",
        len(implementation_rows_to_validate) == len(APPROVED_CANDIDATE_IDS),
        f"expected {len(APPROVED_CANDIDATE_IDS)} implementations, found {len(implementation_rows_to_validate)}",
    )
    add_check(
        "registry_alignment",
        not missing_ids and not unexpected_ids,
        "implementation IDs match authoritative registry"
        if not missing_ids and not unexpected_ids
        else f"missing: {missing_ids}; unexpected: {unexpected_ids}",
    )

    registry_rows_by_id = {str(row["candidate_id"]): row for row in candidate_registry_rows()}
    metadata_field_map = {
        "working_name": "working_name",
        "family": "family",
        "concept_category": "concept_category",
        "economic_mechanism": "economic_mechanism",
        "implementation_priority": "implementation_priority",
        "dependency_class": "dependency_class",
        "required_input_family": "required_input_family",
        "required_ohlcv_inputs": "required_ohlcv_inputs",
        "prohibited_dependencies": "prohibited_dependencies",
        "registry_artifact_namespace": "artifact_namespace",
        "diagnostic_identifier": "diagnostic_identifier",
    }
    metadata_mismatches: list[str] = []
    for row in implementation_rows_to_validate:
        candidate_id = str(row.get("candidate_id", "")).strip()
        registry_row = registry_rows_by_id.get(candidate_id)
        if registry_row is None:
            continue
        for implementation_field, registry_field in metadata_field_map.items():
            if str(row.get(implementation_field, "")).strip() != str(registry_row.get(registry_field, "")).strip():
                metadata_mismatches.append(f"{candidate_id}.{implementation_field}")
    add_check(
        "registry_metadata_consistency",
        not metadata_mismatches,
        "implementation metadata matches authoritative registry values"
        if not metadata_mismatches
        else "metadata mismatches: " + ", ".join(metadata_mismatches),
    )
    add_check(
        "no_duplicate_implementations",
        not duplicate_ids,
        "no duplicate implementation IDs"
        if not duplicate_ids
        else f"duplicate implementation IDs: {', '.join(duplicate_ids)}",
    )
    add_check(
        "excluded_candidate_not_implemented",
        "nhlr_06" not in ids,
        "nhlr_06 is not implemented",
    )

    missing_field_refs: list[str] = []
    for row in implementation_rows_to_validate:
        candidate_id = str(row.get("candidate_id", "<missing>"))
        for field in required_fields:
            if field not in row or str(row.get(field, "")).strip() == "":
                missing_field_refs.append(f"{candidate_id}.{field}")
    add_check(
        "implementation_manifest_complete",
        not missing_field_refs,
        "all implementation manifest fields are populated"
        if not missing_field_refs
        else "missing fields: " + ", ".join(missing_field_refs),
    )

    fail_closed_ok = all(
        str(row.get("panel_status", "")) == PANEL_STATUS
        and str(row.get("discovery_status", "")) == DISCOVERY_STATUS
        and str(row.get("formula_status", "")) == FORMULA_STATUS
        for row in implementation_rows_to_validate
    )
    add_check(
        "implementation_fail_closed",
        fail_closed_ok,
        "all implementations block formulas, panels, and discovery"
        if fail_closed_ok
        else "one or more implementations indicate forbidden execution readiness",
    )

    return not errors, errors, report


def formula_manifest_rows() -> list[dict[str, object]]:
    registry_by_id = {str(row["candidate_id"]): row for row in candidate_registry_rows()}
    rows: list[dict[str, object]] = []
    for candidate_id in APPROVED_CANDIDATE_IDS:
        spec = FORMULA_SPECS[candidate_id]
        registry_row = registry_by_id[candidate_id]
        rows.append(
            {
                "candidate_id": candidate_id,
                "working_name": registry_row["working_name"],
                "family": registry_row["family"],
                "concept_category": registry_row["concept_category"],
                "economic_mechanism": registry_row["economic_mechanism"],
                "implementation_priority": registry_row["implementation_priority"],
                "formula_name": spec["formula_name"],
                "formula_version": FORMULA_VERSION,
                "primary_horizon": spec["primary_horizon"],
                "secondary_review_horizons": spec["secondary_review_horizons"],
                "panel_role": spec["panel_role"],
                "required_raw_inputs": ",".join(REQUIRED_OHLCV_COLUMNS),
                "required_derived_features": spec["required_derived_features"],
                "registry_source_path": (
                    "artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/"
                    "candidate_registry/candidate_registry.csv"
                ),
                "registry_alignment_status": "REGISTRY_ALIGNED",
                "formula_status": "FORMULA_IMPLEMENTED_PANEL_NOT_GENERATED",
                "panel_generation_status": PANEL_STATUS,
            }
        )
    return rows


def validate_formula_manifest_rows(rows: list[dict[str, object]] | None = None) -> tuple[bool, list[str]]:
    manifest_rows = formula_manifest_rows() if rows is None else rows
    ids = [str(row.get("candidate_id", "")).strip() for row in manifest_rows]
    errors: list[str] = []
    if ids != APPROVED_CANDIDATE_IDS:
        errors.append("formula candidate IDs do not match authoritative registry order")
    if "nhlr_06" in ids:
        errors.append("excluded candidate nhlr_06 has a formula row")
    if sorted(set(ids)) != sorted(ids):
        errors.append("duplicate formula candidate IDs found")
    registry_by_id = {str(row["candidate_id"]): row for row in candidate_registry_rows()}
    for row in manifest_rows:
        candidate_id = str(row.get("candidate_id", "")).strip()
        registry_row = registry_by_id.get(candidate_id)
        if registry_row is None:
            errors.append(f"formula row has unknown candidate_id: {candidate_id}")
            continue
        for field in ["working_name", "family", "concept_category", "economic_mechanism", "implementation_priority"]:
            if str(row.get(field, "")).strip() != str(registry_row.get(field, "")).strip():
                errors.append(f"formula metadata drift: {candidate_id}.{field}")
    return not errors, errors


def _require_ohlcv_columns(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_OHLCV_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError("missing required OHLCV columns: " + ", ".join(missing))


def _prepare_ohlcv_base(frame: pd.DataFrame) -> pd.DataFrame:
    _require_ohlcv_columns(frame)
    out = frame.copy()
    out["date"] = pd.to_datetime(out["date"]).dt.normalize()
    out["ticker"] = out["ticker"].astype(str)
    source_close_column = "adjusted_close" if "adjusted_close" in out.columns else "close"
    out["_close"] = pd.to_numeric(out[source_close_column], errors="coerce")
    for column in ["open", "high", "low", "close", "volume"]:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    if "dollar_volume" in out.columns:
        out["dollar_volume"] = pd.to_numeric(out["dollar_volume"], errors="coerce")
    else:
        out["dollar_volume"] = out["_close"] * out["volume"]
    out["source_close_column"] = source_close_column
    valid = (
        out["_close"].gt(0)
        & out["open"].gt(0)
        & out["high"].gt(0)
        & out["low"].gt(0)
        & out["volume"].ge(0)
        & out["high"].ge(out["low"])
        & out[["date", "ticker", "_close", "open", "high", "low", "volume"]].notna().all(axis=1)
    )
    out["valid_ohlcv"] = valid
    out["missing_data_reason"] = np.where(valid, "", "invalid_or_missing_ohlcv")
    out = out.sort_values(["ticker", "date"]).reset_index(drop=True)
    out["warmup_count"] = out.groupby("ticker").cumcount() + 1
    out["warmup_complete"] = out["warmup_count"].ge(WARMUP_WINDOW)
    return out


def _shift_by_ticker(frame: pd.DataFrame, values: pd.Series, periods: int) -> pd.Series:
    return values.groupby(frame["ticker"], sort=False).shift(periods)


def _rolling_by_ticker(frame: pd.DataFrame, values: pd.Series, window: int, op: str) -> pd.Series:
    grouped = values.groupby(frame["ticker"], sort=False)
    if op == "mean":
        return grouped.transform(lambda series: series.rolling(window, min_periods=window).mean())
    if op == "std":
        return grouped.transform(lambda series: series.rolling(window, min_periods=window).std(ddof=0))
    raise ValueError(f"unsupported rolling op: {op}")


def _ts_z(frame: pd.DataFrame, values: pd.Series, window: int) -> pd.Series:
    mean = _rolling_by_ticker(frame, values, window, "mean")
    std = _rolling_by_ticker(frame, values, window, "std").replace(0, np.nan)
    return (values - mean) / std


def _rank_cs(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    counts = values.groupby(frame["date"]).transform("count")
    ranks = values.groupby(frame["date"]).rank(method="average", pct=True)
    return ranks.where(counts.ge(MIN_CROSS_SECTIONAL_COUNT))


def _z_cs(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    def zscore(group: pd.Series) -> pd.Series:
        if group.count() < MIN_CROSS_SECTIONAL_COUNT:
            return pd.Series(np.nan, index=group.index)
        lower = group.quantile(0.01)
        upper = group.quantile(0.99)
        winsorized = group.clip(lower=lower, upper=upper)
        std = winsorized.std(ddof=0)
        if pd.isna(std) or std == 0:
            return pd.Series(np.nan, index=group.index)
        return ((winsorized - winsorized.mean()) / std).clip(-5, 5)

    return values.groupby(frame["date"], group_keys=False).apply(zscore)


def _safe_mean(components: list[pd.Series], min_count: int) -> tuple[pd.Series, pd.Series]:
    component_frame = pd.concat(components, axis=1)
    coverage = component_frame.notna().sum(axis=1)
    return component_frame.mean(axis=1).where(coverage.ge(min_count)), coverage


def _safe_sum(components: list[pd.Series], min_count: int) -> tuple[pd.Series, pd.Series]:
    component_frame = pd.concat(components, axis=1)
    coverage = component_frame.notna().sum(axis=1)
    return component_frame.sum(axis=1, min_count=min_count), coverage


def build_ohlcv_formula_features(raw_ohlcv: pd.DataFrame) -> pd.DataFrame:
    features = _prepare_ohlcv_base(raw_ohlcv)
    valid_close = features["_close"].where(features["valid_ohlcv"])
    valid_high = features["high"].where(features["valid_ohlcv"])
    valid_low = features["low"].where(features["valid_ohlcv"])
    valid_volume = features["volume"].where(features["valid_ohlcv"])
    valid_dollar_volume = features["dollar_volume"].where(features["valid_ohlcv"])

    features["log_ret_1"] = np.log(valid_close / _shift_by_ticker(features, valid_close, 1))
    for window in [20, 60]:
        features[f"ret_{window}"] = valid_close / _shift_by_ticker(features, valid_close, window) - 1
        features[f"rel_strength_{window}"] = _rank_cs(features, features[f"ret_{window}"])

    for window in [50, 100]:
        features[f"ma_{window}"] = _rolling_by_ticker(features, valid_close, window, "mean")

    features["trend_rank_50"] = _rank_cs(features, valid_close / features["ma_50"] - 1)
    features["vol_20"] = _rolling_by_ticker(features, features["log_ret_1"], 20, "std")
    features["vol_control_20"] = 1 - _rank_cs(features, features["vol_20"])
    features["range_pct"] = (valid_high - valid_low) / valid_close
    features["range_20"] = _rolling_by_ticker(features, features["range_pct"], 20, "mean")
    features["range_control_20"] = 1 - _rank_cs(features, features["range_20"])
    log_dollar_volume = np.log1p(valid_dollar_volume)
    features["dv_z_20"] = _ts_z(features, log_dollar_volume, 20)
    features["dv_z_60"] = _ts_z(features, log_dollar_volume, 60)
    features["participation_60"] = _rank_cs(features, features["dv_z_60"])
    features["leadership_score"], features["leadership_component_coverage"] = _safe_mean(
        [features["rel_strength_20"], features["rel_strength_60"], features["trend_rank_50"]],
        min_count=3,
    )
    features["leadership_delta_20"] = features["leadership_score"] - _shift_by_ticker(
        features, features["leadership_score"], 20
    )
    features["leadership_delta_60"] = features["leadership_score"] - _shift_by_ticker(
        features, features["leadership_score"], 60
    )
    features["rank_velocity_20"] = features["rel_strength_20"] - _shift_by_ticker(
        features, features["rel_strength_20"], 20
    )
    features["rank_acceleration_20"] = features["rank_velocity_20"] - _shift_by_ticker(
        features, features["rank_velocity_20"], 20
    )
    features["above_ma_50"] = valid_close.gt(features["ma_50"]).astype(float).where(
        valid_close.notna() & features["ma_50"].notna()
    )
    features["above_ma_100"] = valid_close.gt(features["ma_100"]).astype(float).where(
        valid_close.notna() & features["ma_100"].notna()
    )
    breadth_by_date = features.groupby("date")["above_ma_50"].mean()
    breadth_delta = breadth_by_date - breadth_by_date.shift(20)
    features["universe_breadth_50"] = features["date"].map(breadth_by_date)
    features["universe_breadth_delta_20"] = features["date"].map(breadth_delta)
    features["breadth_contribution_20"] = features["above_ma_50"] * _rank_cs(features, features["ret_20"])
    features["non_hostile_market_state"] = (
        features["universe_breadth_50"].ge(0.35) & features["universe_breadth_delta_20"].ge(-0.10)
    ).astype(float)
    features.loc[~features["warmup_complete"], "missing_data_reason"] = "warmup_incomplete"
    return features


def _formula_components(features: pd.DataFrame, candidate_id: str) -> list[pd.Series]:
    if candidate_id == "nhlr_01":
        return [
            0.30 * _rank_cs(features, features["leadership_delta_60"]),
            0.25 * _rank_cs(features, features["leadership_delta_20"]),
            0.20 * features["rel_strength_20"],
            0.15 * features["trend_rank_50"],
            0.10 * features["range_control_20"],
            -0.20 * _rank_cs(features, (_shift_by_ticker(features, features["rel_strength_60"], 60) - 0.50).abs()),
        ]
    if candidate_id == "nhlr_02":
        return [
            0.30 * features["participation_60"],
            0.25 * _rank_cs(features, features["dv_z_60"] - features["dv_z_20"].abs()),
            0.20 * features["range_control_20"],
            0.15 * features["vol_control_20"],
            0.10 * _rank_cs(features, features["ret_20"]),
            -0.20 * _rank_cs(features, features["ret_20"].abs()),
        ]
    if candidate_id == "nhlr_03":
        return [
            0.30 * features["leadership_score"],
            0.25 * _rank_cs(features, -features["leadership_delta_20"].abs()),
            0.20 * features["rel_strength_60"],
            0.15 * features["participation_60"],
            0.10 * features["range_control_20"],
        ]
    if candidate_id == "nhlr_04":
        return [
            0.30 * _rank_cs(features, features["trend_rank_50"] - _shift_by_ticker(features, features["trend_rank_50"], 20)),
            0.25 * features["trend_rank_50"],
            0.20 * features["range_control_20"],
            0.15 * features["vol_control_20"],
            0.10 * features["rel_strength_20"],
        ]
    if candidate_id == "nhlr_05":
        gated = features["non_hostile_market_state"]
        return [
            gated * 0.30 * features["participation_60"],
            gated * 0.25 * _rank_cs(features, features["participation_60"] - _shift_by_ticker(features, features["participation_60"], 20)),
            gated * 0.20 * features["breadth_contribution_20"],
            gated * 0.15 * features["range_control_20"],
            gated * 0.10 * features["rel_strength_20"],
        ]
    if candidate_id == "nhlr_07":
        return [
            0.35 * _rank_cs(features, features["rank_acceleration_20"]),
            0.25 * _rank_cs(features, features["rank_velocity_20"]),
            0.20 * features["rel_strength_20"],
            0.10 * features["trend_rank_50"],
            0.10 * features["range_control_20"],
        ]
    if candidate_id == "nhlr_08":
        return [
            0.30 * features["leadership_score"],
            0.30 * _rank_cs(features, -features["rank_acceleration_20"].clip(upper=0)),
            0.20 * _rank_cs(features, -features["rank_velocity_20"].abs()),
            0.10 * features["participation_60"],
            0.10 * features["range_control_20"],
        ]
    if candidate_id == "nhlr_09":
        shock_penalty = (features["dv_z_20"] > 3.0).astype(float)
        return [
            0.30 * features["rel_strength_20"],
            0.25 * _rank_cs(features, features["leadership_delta_20"]),
            0.25 * _rank_cs(features, features["dv_z_60"].clip(-1.0, 2.0)),
            0.10 * features["range_control_20"],
            0.10 * features["trend_rank_50"],
            -0.20 * _rank_cs(features, shock_penalty),
        ]
    if candidate_id == "nhlr_10":
        gated = features["non_hostile_market_state"]
        return [
            gated * 0.30 * features["breadth_contribution_20"],
            gated * 0.25 * _rank_cs(features, features["above_ma_50"] + features["above_ma_100"]),
            gated * 0.20 * features["rel_strength_20"],
            gated * 0.15 * features["participation_60"],
            gated * 0.10 * features["range_control_20"],
        ]
    raise ValueError(f"unsupported candidate_id: {candidate_id}")


def build_candidate_formula_outputs(raw_ohlcv: pd.DataFrame) -> pd.DataFrame:
    features = build_ohlcv_formula_features(raw_ohlcv)
    registry_by_id = {str(row["candidate_id"]): row for row in candidate_registry_rows()}
    manifest_by_id = {str(row["candidate_id"]): row for row in formula_manifest_rows()}
    panels: list[pd.DataFrame] = []
    for candidate_id in APPROVED_CANDIDATE_IDS:
        components = _formula_components(features, candidate_id)
        raw_score, coverage = _safe_sum(components, min_count=3)
        signal_value = _z_cs(features, raw_score).where(features["warmup_complete"] & features["valid_ohlcv"])
        missing_reason = features["missing_data_reason"].copy()
        missing_reason = missing_reason.where(signal_value.isna(), "")
        missing_reason = missing_reason.mask(
            signal_value.isna() & features["warmup_complete"] & features["valid_ohlcv"] & coverage.lt(3),
            "insufficient_formula_components",
        )
        registry_row = registry_by_id[candidate_id]
        manifest_row = manifest_by_id[candidate_id]
        panel = pd.DataFrame(
            {
                "date": features["date"],
                "ticker": features["ticker"],
                "candidate_id": candidate_id,
                "signal_value": signal_value,
                "family": registry_row["family"],
                "theme": registry_row["concept_category"],
                "horizon": manifest_row["primary_horizon"],
                "working_name": registry_row["working_name"],
                "economic_mechanism": registry_row["economic_mechanism"],
                "implementation_priority": registry_row["implementation_priority"],
                "panel_role": manifest_row["panel_role"],
                "formula_name": manifest_row["formula_name"],
                "formula_version": FORMULA_VERSION,
                "dependency_class": registry_row["dependency_class"],
                "required_input_family": registry_row["required_input_family"],
                "component_coverage_count": coverage,
                "warmup_complete": features["warmup_complete"],
                "non_hostile_market_state": features["non_hostile_market_state"],
                "source_close_column": features["source_close_column"],
                "missing_data_reason": missing_reason,
            }
        )
        panels.append(panel[REQUIRED_PANEL_COLUMNS])
    return pd.concat(panels, ignore_index=True)
