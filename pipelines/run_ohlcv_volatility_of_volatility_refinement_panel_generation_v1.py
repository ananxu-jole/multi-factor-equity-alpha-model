from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    BLOCKED_CANDIDATE_IDS,
    BLOCKED_FAMILY_PREFIXES,
    FAMILY,
    IMPLEMENTED_REFINEMENT_IDS,
    MODULE_ID,
    RAW_INPUT_COLUMNS,
    RESEARCH_STATUS,
    TIMING_POLICY as REFINEMENT_TIMING_POLICY,
    build_refinement_candidate_panel,
    candidate_registry,
    validate_refinement_registry,
)
from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    RUN_ID as ORIGINAL_VOV_MODULE_ID,
    build_vov_candidate_panel,
)


PANEL_SPEC_ID = "ohlcv_volatility_of_volatility_bounded_refinement_panel_specification_v1"
FORMULA_SPEC_ID = "ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1"
PANEL_GENERATION_ID = "ohlcv_volatility_of_volatility_bounded_refinement_panel_generation_v1"
PANEL_GENERATION_CLASSIFICATION = "REFINEMENT_PANEL_GENERATION_READY_FOR_AUDIT"
TIMING_POLICY = REFINEMENT_TIMING_POLICY
ACTIVATION_NEUTRALIZATION = "inactive_pre_rank_raw_score_zero"
PANEL_SHAPE = "long_per_variant"
RANK_MIN_COUNT = 50

RAW_OHLCV_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")
ARTIFACT_ROOT = Path("artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1")

REFINEMENT_FAMILY_BY_PARENT = {
    "vov_01": "vov_01_refinement",
    "vov_03": "vov_03_refinement",
}

EXPECTED_PANEL_FILES = tuple(f"{candidate_id}_signal_panel.parquet" for candidate_id in IMPLEMENTED_REFINEMENT_IDS)

PANEL_COLUMNS = [
    "date",
    "ticker",
    "candidate_id",
    "source_spec_id",
    "parent_candidate_id",
    "module_id",
    "refinement_family",
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
]

PANEL_MANIFEST_COLUMNS = [
    "candidate_id",
    "parent_candidate_id",
    "source_spec_id",
    "refinement_family",
    "panel_path",
    "row_count",
    "date_min",
    "date_max",
    "ticker_count",
    "duplicate_key_count",
    "missing_signal_count",
    "inactive_row_count",
    "warmup_incomplete_count",
    "rank_min_count",
    "dates_below_rank_min_count",
    "timing_policy",
    "schema_status",
    "blocked_candidate_check",
    "anchor_equivalence_required",
    "anchor_equivalence_status",
]

SUMMARY_COLUMNS = [
    "artifact_root",
    "variant_count",
    "panel_file_count",
    "row_count",
    "duplicate_key_count",
    "missing_signal_count",
    "inactive_row_count",
    "warmup_incomplete_count",
    "date_min",
    "date_max",
    "schema_validation_status",
    "blocked_candidate_check",
    "anchor_equivalence_status",
    "classification",
]

SCHEMA_REPORT_COLUMNS = [
    "candidate_id",
    "schema_status",
    "candidate_id_status",
    "parent_candidate_id_status",
    "source_spec_id_status",
    "module_id_status",
    "refinement_family_status",
    "long_form_status",
    "duplicate_status",
    "activation_status",
    "timing_status",
    "blocked_candidate_status",
    "anchor_equivalence_status",
    "notes",
]

MISSING_REASON_VOCABULARY = {
    "rolling_warmup",
    "inactive_zeroed",
    "insufficient_cross_section",
    "missing_input",
    "nonfinite_feature",
}

DERIVED_FEATURES = [
    ("ret_1", "daily close-to-close return"),
    ("ret_10", "10-day close-to-close return"),
    ("ret_20", "20-day close-to-close return"),
    ("abs_ret_10", "absolute 10-day return"),
    ("abs_ret_20", "absolute 20-day return"),
    ("range_1", "daily high-low range scaled by close"),
    ("vol_5", "5-day rolling standard deviation of ret_1"),
    ("vol_10", "10-day rolling standard deviation of ret_1"),
    ("vov_5_20", "20-day rolling standard deviation of vol_5"),
    ("vov_10_40", "40-day rolling standard deviation of vol_10"),
    ("vov_slope_5", "vov_5_20 minus 5-day lag"),
    ("vov_slope_10", "vov_10_40 minus 10-day lag"),
    ("vov_slope_5_smooth_3", "3-day rolling mean of vov_slope_5"),
    ("range_chop_20", "20-day rolling standard deviation of range_1"),
    ("range_chop_40", "40-day rolling standard deviation of range_1"),
    ("range_chop_slope_5", "range_chop_20 minus 5-day lag"),
    ("range_chop_slope_10", "range_chop_40 minus 10-day lag"),
    ("low_extension_20", "inverse cross-sectional rank of abs_ret_20"),
]


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _formula_hash(formula_summary: str) -> str:
    return hashlib.sha256(formula_summary.encode("utf-8")).hexdigest()


def _normalize_ohlcv_source(raw: pd.DataFrame) -> pd.DataFrame:
    if set(RAW_INPUT_COLUMNS).issubset(raw.columns):
        return raw.loc[:, RAW_INPUT_COLUMNS].copy()

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError("OHLCV source must be long-form or a two-level wide OHLCV parquet")

    field_lookup = {
        str(field).strip().lower().replace(" ", "_"): field
        for field in raw.columns.get_level_values(0).unique()
    }
    missing_fields = [field for field in RAW_INPUT_COLUMNS[2:] if field not in field_lookup]
    if missing_fields:
        raise ValueError("wide OHLCV source is missing fields: " + ", ".join(missing_fields))

    stacked_fields = []
    for field in RAW_INPUT_COLUMNS[2:]:
        stacked_fields.append(raw[field_lookup[field]].stack(dropna=False).rename(field))
    out = pd.concat(stacked_fields, axis=1).reset_index()
    out = out.rename(columns={out.columns[0]: "date", out.columns[1]: "ticker"})
    return out.loc[:, RAW_INPUT_COLUMNS]


def load_ohlcv_source(source_path: Path = RAW_OHLCV_PATH) -> pd.DataFrame:
    if not source_path.exists():
        raise FileNotFoundError(f"missing OHLCV source parquet: {source_path}")
    return _normalize_ohlcv_source(pd.read_parquet(source_path))


def _registry_by_candidate() -> dict[str, pd.Series]:
    registry = candidate_registry()
    return {str(row["candidate_id"]): row for _, row in registry.iterrows()}


def _refinement_family(parent_candidate_id: str) -> str:
    try:
        return REFINEMENT_FAMILY_BY_PARENT[parent_candidate_id]
    except KeyError as exc:
        raise ValueError(f"unexpected parent candidate for refinement panel: {parent_candidate_id}") from exc


def _blocked_candidate_present(values: Iterable[object]) -> bool:
    for value in values:
        candidate_id = str(value)
        if candidate_id in BLOCKED_CANDIDATE_IDS:
            return True
        if candidate_id.startswith(BLOCKED_FAMILY_PREFIXES):
            return True
    return False


def _candidate_panel_path(artifact_root: Path, candidate_id: str) -> Path:
    return artifact_root / f"{candidate_id}_signal_panel.parquet"


def _ensure_artifact_root_compatible(artifact_root: Path) -> None:
    if not artifact_root.exists():
        return
    existing_parquets = {path.name for path in artifact_root.glob("*.parquet")}
    unexpected = sorted(existing_parquets - set(EXPECTED_PANEL_FILES))
    if unexpected:
        raise ValueError(
            "refinement panel root contains unexpected parquet artifacts: " + ", ".join(unexpected)
        )


def build_refinement_panel_frames(
    ohlcv: pd.DataFrame,
    *,
    rank_min_count: int = RANK_MIN_COUNT,
) -> dict[str, pd.DataFrame]:
    validate_refinement_registry()
    combined = build_refinement_candidate_panel(ohlcv, min_cross_section_count=rank_min_count)
    registry = _registry_by_candidate()
    panels: dict[str, pd.DataFrame] = {}

    for candidate_id in IMPLEMENTED_REFINEMENT_IDS:
        panel = combined.loc[combined["candidate_id"].astype(str) == candidate_id].copy()
        if panel.empty:
            raise ValueError(f"refinement implementation produced no panel rows for {candidate_id}")

        registry_row = registry[candidate_id]
        parent_candidate_id = str(registry_row["parent_candidate_id"])
        panel["refinement_family"] = _refinement_family(parent_candidate_id)
        panel["secondary_horizons"] = panel["secondary_horizons"].astype(str).str.replace(",", "|", regex=False)
        panel["ticker"] = panel["ticker"].astype(str)
        panel["created_by_spec"] = PANEL_SPEC_ID
        panel = panel.loc[:, PANEL_COLUMNS].sort_values(["date", "ticker", "candidate_id"])
        panels[candidate_id] = panel.reset_index(drop=True)

    return panels


def _anchor_equivalence_status(
    ohlcv: pd.DataFrame,
    panels: dict[str, pd.DataFrame],
    *,
    rank_min_count: int,
) -> dict[str, str]:
    original = build_vov_candidate_panel(ohlcv, min_cross_section_count=rank_min_count)
    statuses = {candidate_id: "NA" for candidate_id in IMPLEMENTED_REFINEMENT_IDS}
    anchor_map = {
        "vov_01_ref_anchor": "vov_01",
        "vov_03_ref_anchor": "vov_03",
    }

    for refinement_id, original_id in anchor_map.items():
        panel = panels[refinement_id].loc[
            :, ["date", "ticker", "raw_score", "signal_value", "is_active"]
        ].copy()
        expected = original.loc[
            :, ["date", "ticker", f"{original_id}_raw_score", f"{original_id}_signal", f"{original_id}_active"]
        ].rename(
            columns={
                f"{original_id}_raw_score": "expected_raw_score",
                f"{original_id}_signal": "expected_signal_value",
                f"{original_id}_active": "expected_is_active",
            }
        )
        merged = panel.merge(expected, on=["date", "ticker"], how="inner", validate="one_to_one")
        if len(merged) != len(panel):
            statuses[refinement_id] = "FAIL"
            continue
        raw_match = np.allclose(
            merged["raw_score"].to_numpy(dtype="float64"),
            merged["expected_raw_score"].to_numpy(dtype="float64"),
            equal_nan=True,
        )
        signal_match = np.allclose(
            merged["signal_value"].to_numpy(dtype="float64"),
            merged["expected_signal_value"].to_numpy(dtype="float64"),
            equal_nan=True,
        )
        active_match = (
            merged["is_active"].astype(bool).to_numpy()
            == merged["expected_is_active"].astype(bool).to_numpy()
        ).all()
        statuses[refinement_id] = "PASS" if raw_match and signal_match and active_match else "FAIL"

    return statuses


def validate_candidate_panel_frame(
    panel: pd.DataFrame,
    candidate_id: str,
    *,
    anchor_equivalence_status: str = "NA",
) -> list[str]:
    registry = _registry_by_candidate()
    errors: list[str] = []
    if candidate_id not in IMPLEMENTED_REFINEMENT_IDS:
        errors.append(f"candidate_id is not an approved VoV refinement variant: {candidate_id}")
        return errors
    if list(panel.columns) != PANEL_COLUMNS:
        errors.append("panel schema does not match required refinement long-form columns")
    if panel.empty:
        errors.append(f"panel is empty: {candidate_id}")
        return errors

    row = registry[candidate_id]
    parent_candidate_id = str(row["parent_candidate_id"])
    expected_refinement_family = _refinement_family(parent_candidate_id)

    if set(panel["candidate_id"].astype(str)) != {candidate_id}:
        errors.append(f"panel candidate_id values do not match file candidate_id: {candidate_id}")
    if _blocked_candidate_present(panel["candidate_id"].dropna().unique()):
        errors.append("blocked candidate appeared in refinement panel")
    if set(panel["parent_candidate_id"].astype(str)) != {parent_candidate_id}:
        errors.append(f"parent_candidate_id mismatch for {candidate_id}")
    if set(panel["source_spec_id"].astype(str)) != {str(row['source_spec_id'])}:
        errors.append(f"source_spec_id mismatch for {candidate_id}")
    if set(panel["module_id"].astype(str)) != {MODULE_ID}:
        errors.append(f"module_id mismatch for {candidate_id}")
    if set(panel["refinement_family"].astype(str)) != {expected_refinement_family}:
        errors.append(f"refinement_family mismatch for {candidate_id}")
    if set(panel["family"].astype(str)) != {FAMILY}:
        errors.append(f"family mismatch for {candidate_id}")
    if set(panel["research_status"].astype(str)) != {RESEARCH_STATUS}:
        errors.append(f"research_status mismatch for {candidate_id}")
    if set(panel["timing_policy"].astype(str)) != {TIMING_POLICY}:
        errors.append(f"timing_policy mismatch for {candidate_id}")
    if set(panel["created_by_spec"].astype(str)) != {PANEL_SPEC_ID}:
        errors.append(f"created_by_spec mismatch for {candidate_id}")
    if panel[["date", "ticker", "candidate_id"]].duplicated().any():
        errors.append(f"duplicate panel rows found for {candidate_id}")
    if not set(panel["missing_reason"].dropna().astype(str)).issubset(MISSING_REASON_VOCABULARY):
        errors.append(f"missing_reason contains values outside vocabulary for {candidate_id}")

    inactive = ~panel["is_active"].astype(bool)
    inactive_with_features = inactive & panel["pre_activation_raw_score"].notna()
    if not np.allclose(panel.loc[inactive_with_features, "raw_score"], 0.0, equal_nan=False):
        errors.append(f"inactive rows were not neutralized to raw_score zero for {candidate_id}")
    missing_pre = panel["pre_activation_raw_score"].isna()
    if panel.loc[missing_pre, "raw_score"].notna().any():
        errors.append(f"missing pre-activation raw scores were converted to finite raw_score for {candidate_id}")
    if panel.loc[missing_pre, "signal_value"].notna().any():
        errors.append(f"missing pre-activation raw scores were converted to finite signal for {candidate_id}")
    if panel["rank_min_count"].astype(int).nunique() != 1:
        errors.append(f"rank_min_count is not constant for {candidate_id}")
    if candidate_id.endswith("_ref_anchor") and anchor_equivalence_status != "PASS":
        errors.append(f"anchor equivalence failed for {candidate_id}")

    return errors


def _panel_stats(
    candidate_id: str,
    panel: pd.DataFrame,
    panel_path: Path,
    *,
    anchor_equivalence_status: str,
) -> dict[str, object]:
    duplicate_key_count = int(panel[["date", "ticker", "candidate_id"]].duplicated().sum())
    return {
        "candidate_id": candidate_id,
        "parent_candidate_id": str(panel["parent_candidate_id"].iloc[0]),
        "source_spec_id": str(panel["source_spec_id"].iloc[0]),
        "refinement_family": str(panel["refinement_family"].iloc[0]),
        "panel_path": str(panel_path),
        "row_count": int(len(panel)),
        "date_min": str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": str(pd.to_datetime(panel["date"]).max().date()),
        "ticker_count": int(panel["ticker"].nunique()),
        "duplicate_key_count": duplicate_key_count,
        "missing_signal_count": int(panel["signal_value"].isna().sum()),
        "inactive_row_count": int((~panel["is_active"].astype(bool)).sum()),
        "warmup_incomplete_count": int((~panel["feature_warmup_complete"].astype(bool)).sum()),
        "rank_min_count": int(panel["rank_min_count"].iloc[0]),
        "dates_below_rank_min_count": int(
            panel.groupby("date", sort=False)["signal_value"]
            .apply(lambda s: s.notna().sum())
            .lt(int(panel["rank_min_count"].iloc[0]))
            .sum()
        ),
        "timing_policy": TIMING_POLICY,
        "schema_status": "PASS",
        "blocked_candidate_check": "PASS",
        "anchor_equivalence_required": bool(candidate_id.endswith("_ref_anchor")),
        "anchor_equivalence_status": anchor_equivalence_status,
    }


def _schema_report_row(
    candidate_id: str,
    panel: pd.DataFrame,
    errors: Iterable[str],
    *,
    anchor_equivalence_status: str,
) -> dict[str, object]:
    error_list = list(errors)
    ok = not error_list
    registry = _registry_by_candidate()
    row = registry.get(candidate_id)
    parent = str(row["parent_candidate_id"]) if row is not None else ""
    expected_refinement_family = _refinement_family(parent) if parent else ""
    return {
        "candidate_id": candidate_id,
        "schema_status": "PASS" if ok else "FAIL",
        "candidate_id_status": "PASS" if set(panel.get("candidate_id", pd.Series(dtype=str)).astype(str)) == {candidate_id} else "FAIL",
        "parent_candidate_id_status": "PASS" if set(panel.get("parent_candidate_id", pd.Series(dtype=str)).astype(str)) == {parent} else "FAIL",
        "source_spec_id_status": "PASS" if not any("source_spec_id" in error for error in error_list) else "FAIL",
        "module_id_status": "PASS" if set(panel.get("module_id", pd.Series(dtype=str)).astype(str)) == {MODULE_ID} else "FAIL",
        "refinement_family_status": "PASS"
        if set(panel.get("refinement_family", pd.Series(dtype=str)).astype(str)) == {expected_refinement_family}
        else "FAIL",
        "long_form_status": "PASS" if list(panel.columns) == PANEL_COLUMNS else "FAIL",
        "duplicate_status": "PASS" if not panel[["date", "ticker", "candidate_id"]].duplicated().any() else "FAIL",
        "activation_status": "PASS"
        if not any("neutralized" in error or "pre-activation" in error for error in error_list)
        else "FAIL",
        "timing_status": "PASS" if set(panel["timing_policy"].astype(str)) == {TIMING_POLICY} else "FAIL",
        "blocked_candidate_status": "PASS"
        if not _blocked_candidate_present(panel["candidate_id"].dropna().unique())
        else "FAIL",
        "anchor_equivalence_status": anchor_equivalence_status,
        "notes": "panel validation passed" if ok else "; ".join(error_list),
    }


def _guardrail_flags() -> dict[str, bool]:
    return {
        "panel_generation_executed": True,
        "ic_scoring_executed": False,
        "refinement_scoring_executed": False,
        "validation_executed": False,
        "original_vov_panels_modified": False,
        "original_vov_formulas_modified": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
    }


def _formula_hashes(registry: pd.DataFrame) -> dict[str, str]:
    return {
        str(row["candidate_id"]): _formula_hash(str(row["formula_summary"]))
        for _, row in registry.iterrows()
    }


def _metadata_payload(
    source_path: Path,
    registry: pd.DataFrame,
    manifest_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "run_id": PANEL_GENERATION_ID,
        "module_id": MODULE_ID,
        "spec_id": PANEL_SPEC_ID,
        "formula_spec_id": FORMULA_SPEC_ID,
        "implementation_note": "ohlcv_volatility_of_volatility_bounded_refinement_implementation_v1",
        "implementation_review_note": "ohlcv_volatility_of_volatility_bounded_refinement_implementation_review_v1",
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "candidate_ids": list(IMPLEMENTED_REFINEMENT_IDS),
        "parent_candidate_ids": ["vov_01", "vov_03"],
        "blocked_candidates": [*BLOCKED_CANDIDATE_IDS, "dpath_*", "ecluster_*"],
        "family": FAMILY,
        "refinement_families": ["vov_01_refinement", "vov_03_refinement"],
        "research_status": RESEARCH_STATUS,
        "timing_policy": TIMING_POLICY,
        "rank_min_count": RANK_MIN_COUNT,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
        "panel_shape": PANEL_SHAPE,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_data_access": "existing_local_ohlcv_only",
        "source_ohlcv_path": str(source_path),
        "external_data_accessed": False,
        "formula_hashes": _formula_hashes(registry),
        "guardrail_flags": _guardrail_flags(),
        "variant_count": len(manifest_rows),
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
    }


def _generation_manifest_payload(
    source_path: Path,
    registry: pd.DataFrame,
    manifest_rows: list[dict[str, object]],
    *,
    artifact_root: Path,
) -> dict[str, object]:
    parent_map = {
        str(row["candidate_id"]): str(row["parent_candidate_id"])
        for _, row in registry.iterrows()
    }
    source_map = {
        str(row["candidate_id"]): str(row["source_spec_id"])
        for _, row in registry.iterrows()
    }
    refinement_family_map = {
        candidate_id: _refinement_family(parent)
        for candidate_id, parent in parent_map.items()
    }
    schema_status = "PASS" if all(row["schema_status"] == "PASS" for row in manifest_rows) else "FAIL"
    duplicate_status = "PASS" if sum(int(row["duplicate_key_count"]) for row in manifest_rows) == 0 else "FAIL"
    blocked_status = "PASS" if all(row["blocked_candidate_check"] == "PASS" for row in manifest_rows) else "FAIL"
    anchor_statuses = [
        str(row["anchor_equivalence_status"])
        for row in manifest_rows
        if bool(row["anchor_equivalence_required"])
    ]
    anchor_status = "PASS" if anchor_statuses and all(status == "PASS" for status in anchor_statuses) else "FAIL"
    return {
        "manifest_version": "v1",
        "run_id": PANEL_GENERATION_ID,
        "module_id": MODULE_ID,
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "specification_note": "docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_panel_specification_v1.md",
        "formula_specification_note": "docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md",
        "implementation_review_note": "docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_implementation_review_v1.md",
        "artifact_root": str(artifact_root),
        "source_ohlcv_path": str(source_path),
        "variant_count": len(manifest_rows),
        "candidate_ids": list(IMPLEMENTED_REFINEMENT_IDS),
        "parent_candidate_map": parent_map,
        "source_spec_map": source_map,
        "refinement_family_map": refinement_family_map,
        "formula_hashes": _formula_hashes(registry),
        "panel_files": [str(row["panel_path"]) for row in manifest_rows],
        "timing_policy": TIMING_POLICY,
        "blocked_candidate_check": blocked_status,
        "schema_validation_status": schema_status,
        "duplicate_key_status": duplicate_status,
        "anchor_equivalence_status": anchor_status,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
        "panel_shape": PANEL_SHAPE,
        "guardrail_flags": _guardrail_flags(),
        "original_vov_module_id": ORIGINAL_VOV_MODULE_ID,
    }


def _write_support_manifests(artifact_root: Path, registry: pd.DataFrame) -> None:
    registry.to_csv(artifact_root / "registry_manifest.csv", index=False)
    formula_manifest = registry.loc[
        :, ["candidate_id", "parent_candidate_id", "source_spec_id", "formula_summary", "activation_summary"]
    ].copy()
    formula_manifest["formula_hash"] = formula_manifest["formula_summary"].map(_formula_hash)
    formula_manifest.to_csv(artifact_root / "formula_manifest.csv", index=False)
    pd.DataFrame(
        [{"feature": feature, "description": description} for feature, description in DERIVED_FEATURES]
    ).to_csv(artifact_root / "feature_manifest.csv", index=False)
    pd.DataFrame(
        [{"column": column, "required": True, "source": "raw_ohlcv"} for column in RAW_INPUT_COLUMNS]
    ).to_csv(artifact_root / "input_schema_manifest.csv", index=False)


def write_refinement_panel_artifacts(
    source_path: Path = RAW_OHLCV_PATH,
    *,
    artifact_root: Path = ARTIFACT_ROOT,
    rank_min_count: int = RANK_MIN_COUNT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    registry = candidate_registry()
    validate_refinement_registry(registry)
    if tuple(registry["candidate_id"].astype(str)) != IMPLEMENTED_REFINEMENT_IDS:
        raise ValueError("refinement registry candidate order does not match frozen panel specification")
    if _blocked_candidate_present(registry["candidate_id"]):
        raise ValueError("blocked candidate IDs are not allowed in VoV refinement panel generation")
    if set(registry["parent_candidate_id"].astype(str)) != {"vov_01", "vov_03"}:
        raise ValueError("VoV refinement panels may only use vov_01 and vov_03 parents")

    _ensure_artifact_root_compatible(artifact_root)
    ohlcv = load_ohlcv_source(source_path)
    panels = build_refinement_panel_frames(ohlcv, rank_min_count=rank_min_count)
    if tuple(panels) != IMPLEMENTED_REFINEMENT_IDS:
        raise ValueError("built panel candidate IDs do not match approved refinement variant order")

    anchor_statuses = _anchor_equivalence_status(ohlcv, panels, rank_min_count=rank_min_count)
    if any(status != "PASS" for cid, status in anchor_statuses.items() if cid.endswith("_ref_anchor")):
        raise ValueError(f"anchor equivalence failed before writing panels: {anchor_statuses}")

    artifact_root.mkdir(parents=True, exist_ok=True)
    _write_support_manifests(artifact_root, registry)

    manifest_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []

    for candidate_id, panel in panels.items():
        anchor_status = anchor_statuses[candidate_id]
        validation_errors = validate_candidate_panel_frame(
            panel,
            candidate_id,
            anchor_equivalence_status=anchor_status,
        )
        if validation_errors:
            raise ValueError(f"panel validation failed for {candidate_id}: " + "; ".join(validation_errors))

        panel_path = _candidate_panel_path(artifact_root, candidate_id)
        panel.to_parquet(panel_path, index=False)
        stats = _panel_stats(
            candidate_id,
            panel,
            panel_path,
            anchor_equivalence_status=anchor_status,
        )
        manifest_rows.append({column: stats[column] for column in PANEL_MANIFEST_COLUMNS})
        schema_rows.append(
            _schema_report_row(
                candidate_id,
                panel,
                validation_errors,
                anchor_equivalence_status=anchor_status,
            )
        )

    manifest = pd.DataFrame(manifest_rows, columns=PANEL_MANIFEST_COLUMNS)
    schema_report = pd.DataFrame(schema_rows, columns=SCHEMA_REPORT_COLUMNS)
    summary = pd.DataFrame(
        [
            {
                "artifact_root": str(artifact_root),
                "variant_count": len(manifest),
                "panel_file_count": len(list(artifact_root.glob("*_signal_panel.parquet"))),
                "row_count": int(manifest["row_count"].sum()),
                "duplicate_key_count": int(manifest["duplicate_key_count"].sum()),
                "missing_signal_count": int(manifest["missing_signal_count"].sum()),
                "inactive_row_count": int(manifest["inactive_row_count"].sum()),
                "warmup_incomplete_count": int(manifest["warmup_incomplete_count"].sum()),
                "date_min": manifest["date_min"].min(),
                "date_max": manifest["date_max"].max(),
                "schema_validation_status": "PASS" if set(manifest["schema_status"]) == {"PASS"} else "FAIL",
                "blocked_candidate_check": "PASS" if set(manifest["blocked_candidate_check"]) == {"PASS"} else "FAIL",
                "anchor_equivalence_status": "PASS"
                if set(manifest.loc[manifest["anchor_equivalence_required"], "anchor_equivalence_status"]) == {"PASS"}
                else "FAIL",
                "classification": PANEL_GENERATION_CLASSIFICATION,
            }
        ],
        columns=SUMMARY_COLUMNS,
    )

    manifest.to_csv(artifact_root / "panel_manifest.csv", index=False)
    summary.to_csv(artifact_root / "panel_generation_summary.csv", index=False)
    schema_report.to_csv(artifact_root / "schema_validation_report.csv", index=False)
    _write_json(artifact_root / "metadata.json", _metadata_payload(source_path, registry, manifest_rows))
    _write_json(
        artifact_root / "panel_generation_manifest.json",
        _generation_manifest_payload(source_path, registry, manifest_rows, artifact_root=artifact_root),
    )

    return manifest, summary


def validate_refinement_panel_artifacts(artifact_root: Path = ARTIFACT_ROOT) -> tuple[bool, list[str]]:
    errors: list[str] = []
    required_files = [
        "metadata.json",
        "panel_manifest.csv",
        "panel_generation_summary.csv",
        "panel_generation_manifest.json",
        "schema_validation_report.csv",
        "registry_manifest.csv",
        "formula_manifest.csv",
        "feature_manifest.csv",
        "input_schema_manifest.csv",
        *EXPECTED_PANEL_FILES,
    ]
    for file_name in required_files:
        if not (artifact_root / file_name).exists():
            errors.append(f"missing refinement panel artifact: {artifact_root / file_name}")

    extra_parquets = sorted(path.name for path in artifact_root.glob("*.parquet") if path.name not in EXPECTED_PANEL_FILES)
    if extra_parquets:
        errors.append("unexpected refinement panel parquet artifacts: " + ", ".join(extra_parquets))

    manifest_path = artifact_root / "panel_manifest.csv"
    if not manifest_path.exists():
        return False, errors

    manifest = pd.read_csv(manifest_path)
    if tuple(manifest["candidate_id"].astype(str)) != IMPLEMENTED_REFINEMENT_IDS:
        errors.append("panel manifest candidate IDs do not match approved refinement IDs")
    if len(manifest) != len(IMPLEMENTED_REFINEMENT_IDS):
        errors.append("panel manifest does not contain exactly eight rows")
    if manifest["panel_path"].duplicated().any():
        errors.append("panel manifest contains duplicate panel paths")
    if _blocked_candidate_present(manifest["candidate_id"]):
        errors.append("panel manifest contains blocked candidate IDs")

    for _, row in manifest.iterrows():
        candidate_id = str(row["candidate_id"])
        panel_path = Path(str(row["panel_path"]))
        if not panel_path.exists():
            errors.append(f"missing refinement candidate panel file: {panel_path}")
            continue
        panel = pd.read_parquet(panel_path)
        anchor_status = str(row.get("anchor_equivalence_status", "NA"))
        panel_errors = validate_candidate_panel_frame(
            panel,
            candidate_id,
            anchor_equivalence_status=anchor_status,
        )
        errors.extend(panel_errors)
        if int(row["row_count"]) != len(panel):
            errors.append(f"manifest row_count mismatch for {candidate_id}")
        if int(row["duplicate_key_count"]) != 0:
            errors.append(f"manifest duplicate_key_count is nonzero for {candidate_id}")
        if bool(row["anchor_equivalence_required"]) and anchor_status != "PASS":
            errors.append(f"manifest anchor equivalence status is not PASS for {candidate_id}")

    for json_name in ("metadata.json", "panel_generation_manifest.json"):
        path = artifact_root / json_name
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        guardrail_flags = payload.get("guardrail_flags", {})
        for field in (
            "ic_scoring_executed",
            "refinement_scoring_executed",
            "validation_executed",
            "original_vov_panels_modified",
            "original_vov_formulas_modified",
            "governance_modified",
            "production_registration",
            "thresholds_modified",
            "ml_integration",
        ):
            if guardrail_flags.get(field) is not False:
                errors.append(f"{json_name} forbidden guardrail field is not fail-closed: {field}")
        if guardrail_flags.get("panel_generation_executed") is not True:
            errors.append(f"{json_name} does not mark panel generation executed")
        if payload.get("candidate_ids") != list(IMPLEMENTED_REFINEMENT_IDS):
            errors.append(f"{json_name} candidate IDs mismatch")

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate bounded VoV refinement panel artifacts.")
    parser.add_argument("--source", type=Path, default=RAW_OHLCV_PATH)
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        ok, errors = validate_refinement_panel_artifacts(args.artifact_root)
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"VoV refinement panel validation passed for {args.artifact_root}")
        return 0

    manifest, _summary = write_refinement_panel_artifacts(args.source, artifact_root=args.artifact_root)
    print(f"Wrote {len(manifest)} VoV refinement panels to {args.artifact_root}")
    print("No IC, refinement scoring, validation, governance, production, threshold, or ML work executed.")
    print(PANEL_GENERATION_CLASSIFICATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
