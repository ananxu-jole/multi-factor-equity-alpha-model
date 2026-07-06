from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.dispersion_path_dependence_research_module_v1 import (
    BLOCKED_CANDIDATE_IDS,
    BLOCKED_FAMILY_PREFIXES,
    BLOCKED_MECHANISMS,
    DIAGNOSTIC_COLUMNS,
    FAMILY,
    IMPLEMENTED_CANDIDATE_IDS,
    LONG_FORM_PANEL_COLUMNS,
    MODULE_ID,
    RANK_MIN_COUNT,
    RAW_INPUT_COLUMNS,
    RESEARCH_STATUS,
    SPEC_ID,
    TIMING_POLICY,
    build_dpath_candidate_panel,
    candidate_registry,
    expected_panel_columns,
    validate_dpath_registry,
)


PANEL_SPEC_ID = "dispersion_path_dependence_panel_specification_v1"
PANEL_GENERATION_ID = "dispersion_path_dependence_panel_generation_v1"
PANEL_GENERATION_CLASSIFICATION = "PANEL_GENERATION_READY_WITH_SCIENTIFIC_NOTES"
ACTIVATION_NEUTRALIZATION = "inactive_signal_value_0_5_with_is_active_false"
ZERO_VARIANCE_Z_SCORE_POLICY = "centered_zero_and_std_zero_maps_to_0_0"
PANEL_SHAPE = "long_per_candidate"
RAW_OHLCV_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")
ARTIFACT_ROOT = Path("artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1")

PANEL_FILE_STEMS = {
    "dpath_01_relapse_resilience_after_calm": "dpath_01",
    "dpath_02_disagreement_vol_stress_divergence": "dpath_02",
    "dpath_03_elevated_disagreement_stabilization": "dpath_03",
    "dpath_04_consensus_without_crowding": "dpath_04",
}

PANEL_COLUMNS = list(expected_panel_columns())

REQUIRED_ARTIFACTS = (
    "dpath_01_signal_panel.parquet",
    "dpath_02_signal_panel.parquet",
    "dpath_03_signal_panel.parquet",
    "dpath_04_signal_panel.parquet",
    "metadata.json",
    "panel_manifest.csv",
    "panel_generation_summary.csv",
    "panel_generation_manifest.json",
    "schema_validation_report.csv",
    "registry_manifest.csv",
    "formula_manifest.csv",
    "feature_manifest.csv",
    "input_schema_manifest.csv",
)

MANIFEST_COLUMNS = [
    "candidate_id",
    "candidate_name",
    "mechanism_family",
    "module_id",
    "panel_path",
    "row_count",
    "date_min",
    "date_max",
    "ticker_count",
    "duplicate_key_count",
    "invalid_candidate_count",
    "blocked_candidate_count",
    "missing_signal_count",
    "non_null_signal_count",
    "inactive_row_count",
    "warmup_incomplete_count",
    "rank_min_count",
    "dates_below_rank_min_count",
    "timing_policy",
    "schema_status",
    "generation_status",
]

SUMMARY_COLUMNS = [
    "candidate_id",
    "panel_path",
    "row_count",
    "non_null_signal_count",
    "missing_signal_count",
    "inactive_row_count",
    "warmup_incomplete_count",
    "duplicate_key_count",
    "date_min",
    "date_max",
    "ticker_count",
    "generation_status",
]

SCHEMA_REPORT_COLUMNS = [
    "candidate_id",
    "schema_status",
    "candidate_id_status",
    "module_id_status",
    "long_form_status",
    "duplicate_status",
    "lineage_status",
    "activation_status",
    "timing_status",
    "blocked_candidate_status",
    "notes",
]

MISSING_REASON_VOCABULARY = {
    "raw_ohlcv_missing",
    "rolling_warmup",
    "insufficient_cross_section",
    "nonfinite_feature",
    "inactive_neutralized",
    "date_level_feature_missing",
    "invalid_candidate_id",
    "blocked_deferred_mechanism",
}

LINEAGE_COLUMNS = (
    "candidate_name",
    "mechanism_family",
    "hypothesis",
    "scientific_question",
    "expected_evidence",
    "primary_falsification_criterion",
    "observable_implication",
    "expected_orthogonality",
    "contamination_controls",
    "anchor_comparators",
    "formula_text",
    "activation_text",
    "primary_horizon",
    "secondary_horizons",
    "expected_sign",
    "research_status",
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def _panel_path(artifact_root: Path, candidate_id: str) -> Path:
    return artifact_root / f"{PANEL_FILE_STEMS[candidate_id]}_signal_panel.parquet"


def _expected_panel_files(artifact_root: Path) -> set[Path]:
    return {_panel_path(artifact_root, candidate_id) for candidate_id in IMPLEMENTED_CANDIDATE_IDS}


def _blocked_candidate_mask(values: pd.Series) -> pd.Series:
    as_str = values.fillna("").astype(str)
    return (
        as_str.isin(BLOCKED_CANDIDATE_IDS)
        | as_str.str.startswith(BLOCKED_FAMILY_PREFIXES)
        | as_str.str.contains("smooth", case=False, regex=False)
        | as_str.str.contains("burst", case=False, regex=False)
    )


def build_candidate_panels(
    ohlcv: pd.DataFrame,
    *,
    rank_min_count: int = RANK_MIN_COUNT,
) -> dict[str, pd.DataFrame]:
    validate_dpath_registry()
    panel = build_dpath_candidate_panel(ohlcv, min_cross_section_count=rank_min_count)
    panels: dict[str, pd.DataFrame] = {}
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        subset = panel.loc[panel["candidate_id"].eq(candidate_id), PANEL_COLUMNS].copy()
        subset = subset.sort_values(["date", "ticker", "candidate_id"]).reset_index(drop=True)
        panels[candidate_id] = subset
    return panels


def validate_candidate_panel_frame(panel: pd.DataFrame, candidate_id: str) -> list[str]:
    errors: list[str] = []
    if candidate_id not in IMPLEMENTED_CANDIDATE_IDS:
        errors.append(f"candidate_id is not approved for DPath panel generation: {candidate_id}")
        return errors
    if list(panel.columns) != PANEL_COLUMNS:
        errors.append("panel schema does not match required long-form columns")
    if panel.empty:
        errors.append(f"panel is empty: {candidate_id}")
        return errors

    if set(panel["candidate_id"].astype(str)) != {candidate_id}:
        errors.append(f"panel candidate_id values do not match file candidate_id: {candidate_id}")
    if _blocked_candidate_mask(panel["candidate_id"]).any():
        errors.append(f"blocked candidate appeared in panel: {candidate_id}")
    if set(panel["module_id"].astype(str)) != {MODULE_ID}:
        errors.append(f"module_id mismatch for {candidate_id}")
    if set(panel["spec_id"].astype(str)) != {SPEC_ID}:
        errors.append(f"formula spec_id mismatch for {candidate_id}")
    if set(panel["research_status"].astype(str)) != {RESEARCH_STATUS}:
        errors.append(f"research_status mismatch for {candidate_id}")
    if set(panel["timing_policy"].astype(str)) != {TIMING_POLICY}:
        errors.append(f"timing_policy mismatch for {candidate_id}")
    if set(panel["created_by_spec"].astype(str)) != {SPEC_ID}:
        errors.append(f"created_by_spec mismatch for {candidate_id}")
    if set(panel["rank_min_count"].astype(int)) != {int(panel["rank_min_count"].iloc[0])}:
        errors.append(f"rank_min_count is not constant for {candidate_id}")
    if panel[["date", "ticker", "candidate_id"]].duplicated().any():
        errors.append(f"duplicate panel rows found for {candidate_id}")
    if not set(panel["missing_reason"].dropna().astype(str)).issubset(MISSING_REASON_VOCABULARY):
        errors.append(f"missing_reason contains values outside vocabulary for {candidate_id}")
    for column in LINEAGE_COLUMNS:
        if column not in panel.columns or panel[column].isna().any():
            errors.append(f"lineage column is missing or null for {candidate_id}: {column}")

    inactive_with_features = (~panel["is_active"].astype(bool)) & panel["pre_activation_raw_score"].notna()
    if not (panel.loc[inactive_with_features, "signal_value"].dropna() == 0.5).all():
        errors.append(f"inactive rows were not neutralized to signal_value 0.5 for {candidate_id}")
    if not (panel.loc[inactive_with_features, "raw_score"].dropna() == 0.5).all():
        errors.append(f"inactive rows were not neutralized to raw_score 0.5 for {candidate_id}")
    warmup = ~panel["feature_warmup_complete"].astype(bool)
    if panel.loc[warmup, "signal_value"].notna().any():
        errors.append(f"warmup-incomplete rows contain non-null signal_value for {candidate_id}")

    return errors


def _dates_below_rank_min(panel: pd.DataFrame) -> int:
    rank_min_count = int(panel["rank_min_count"].iloc[0])
    counts = panel.groupby("date", sort=False)["signal_value"].apply(lambda s: s.notna().sum())
    return int((counts < rank_min_count).sum())


def _panel_stats(candidate_id: str, panel: pd.DataFrame, panel_path: Path) -> dict[str, object]:
    duplicate_key_count = int(panel[["date", "ticker", "candidate_id"]].duplicated().sum())
    return {
        "candidate_id": candidate_id,
        "candidate_name": str(panel["candidate_name"].iloc[0]),
        "mechanism_family": str(panel["mechanism_family"].iloc[0]),
        "module_id": MODULE_ID,
        "panel_path": str(panel_path),
        "row_count": int(len(panel)),
        "date_min": str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": str(pd.to_datetime(panel["date"]).max().date()),
        "ticker_count": int(panel["ticker"].nunique()),
        "duplicate_key_count": duplicate_key_count,
        "invalid_candidate_count": int(candidate_id not in IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_count": int(_blocked_candidate_mask(panel["candidate_id"]).sum()),
        "missing_signal_count": int(panel["signal_value"].isna().sum()),
        "non_null_signal_count": int(panel["signal_value"].notna().sum()),
        "inactive_row_count": int((~panel["is_active"].astype(bool)).sum()),
        "warmup_incomplete_count": int((~panel["feature_warmup_complete"].astype(bool)).sum()),
        "rank_min_count": int(panel["rank_min_count"].iloc[0]),
        "dates_below_rank_min_count": _dates_below_rank_min(panel),
        "timing_policy": TIMING_POLICY,
        "schema_status": "PASS",
        "generation_status": "generated",
    }


def _schema_report_row(candidate_id: str, panel: pd.DataFrame, errors: Iterable[str]) -> dict[str, object]:
    error_list = list(errors)
    ok = not error_list
    return {
        "candidate_id": candidate_id,
        "schema_status": "PASS" if ok else "FAIL",
        "candidate_id_status": "PASS" if set(panel.get("candidate_id", pd.Series(dtype=str)).astype(str)) == {candidate_id} else "FAIL",
        "module_id_status": "PASS" if not any("module_id" in e for e in error_list) else "FAIL",
        "long_form_status": "PASS" if list(panel.columns) == PANEL_COLUMNS else "FAIL",
        "duplicate_status": "PASS" if not panel[["date", "ticker", "candidate_id"]].duplicated().any() else "FAIL",
        "lineage_status": "PASS" if not any("lineage" in e for e in error_list) else "FAIL",
        "activation_status": "PASS" if not any("neutralized" in e or "warmup" in e for e in error_list) else "FAIL",
        "timing_status": "PASS" if set(panel["timing_policy"].astype(str)) == {TIMING_POLICY} else "FAIL",
        "blocked_candidate_status": "PASS" if not _blocked_candidate_mask(panel["candidate_id"]).any() else "FAIL",
        "notes": "panel validation passed" if ok else "; ".join(error_list),
    }


def _registry_manifest() -> pd.DataFrame:
    registry = candidate_registry().copy()
    registry["module_id"] = MODULE_ID
    registry["panel_spec_id"] = PANEL_SPEC_ID
    return registry


def _formula_manifest(registry: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "candidate_id",
        "candidate_name",
        "mechanism_family",
        "formula_summary",
        "activation_summary",
        "horizon",
        "secondary_horizons",
        "expected_sign",
        "contamination_checks",
        "anchor_comparators",
        "hypothesis",
        "scientific_question",
        "primary_falsification_criterion",
    ]
    out = registry.loc[:, columns].copy()
    out = out.rename(
        columns={
            "formula_summary": "formula_text",
            "activation_summary": "activation_text",
            "horizon": "primary_horizon",
        }
    )
    out["created_by_spec"] = PANEL_SPEC_ID
    return out


def _feature_manifest() -> pd.DataFrame:
    rows = []
    for column in RAW_INPUT_COLUMNS:
        rows.append(
            {
                "feature_name": column,
                "feature_scope": "raw",
                "definition": "Required raw OHLCV input.",
                "lookback_window": pd.NA,
                "min_periods": pd.NA,
                "uses_cross_section": False,
                "uses_date_level_history": False,
                "uses_future_data": False,
                "required_for_candidates": "|".join(IMPLEMENTED_CANDIDATE_IDS),
                "missing_policy": "raw_ohlcv_missing",
                "warmup_policy": "none",
                "timing_policy": TIMING_POLICY,
            }
        )
    for column in DIAGNOSTIC_COLUMNS:
        rows.append(
            {
                "feature_name": column,
                "feature_scope": "diagnostic",
                "definition": "Implemented DPath feature or diagnostic column.",
                "lookback_window": pd.NA,
                "min_periods": pd.NA,
                "uses_cross_section": column
                in {
                    "rank_churn_5",
                    "low_churn_5",
                    "low_extension_20",
                    "leadership_crowding_60",
                    "emerging_improvement_5_20",
                },
                "uses_date_level_history": column.startswith("disp_")
                or column.startswith("mkt_")
                or column in {"divergence_intensity"},
                "uses_future_data": False,
                "required_for_candidates": "|".join(IMPLEMENTED_CANDIDATE_IDS),
                "missing_policy": "nonfinite_feature",
                "warmup_policy": "security_60_and_date_252_where_applicable",
                "timing_policy": TIMING_POLICY,
            }
        )
    return pd.DataFrame(rows)


def _input_schema_manifest() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "column": column,
                "type": "date" if column == "date" else "string" if column == "ticker" else "float",
                "required": True,
                "rule": "required OHLCV input; no imputation",
            }
            for column in RAW_INPUT_COLUMNS
        ]
    )


def _metadata_payload(
    source_path: Path,
    artifact_root: Path,
    manifest_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "run_id": PANEL_GENERATION_ID,
        "module_id": MODULE_ID,
        "spec_id": PANEL_SPEC_ID,
        "formula_spec_id": SPEC_ID,
        "implementation_note": "dispersion_path_dependence_formula_implementation_v1.md",
        "implementation_review_note": "dispersion_path_dependence_formula_implementation_review_v1.md",
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_ids": list(BLOCKED_CANDIDATE_IDS),
        "blocked_candidate_prefixes": list(BLOCKED_FAMILY_PREFIXES),
        "blocked_mechanisms": list(BLOCKED_MECHANISMS),
        "candidate_count": len(manifest_rows),
        "family": FAMILY,
        "research_status": RESEARCH_STATUS,
        "timing_policy": TIMING_POLICY,
        "rank_min_count": RANK_MIN_COUNT,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
        "zero_variance_z_score_policy": ZERO_VARIANCE_Z_SCORE_POLICY,
        "panel_shape": PANEL_SHAPE,
        "artifact_root": str(artifact_root),
        "source_data_access": "existing_local_ohlcv_only",
        "source_ohlcv_path": str(source_path),
        "external_data_accessed": False,
        "panel_generation_executed": True,
        "ic_scoring_executed": False,
        "discovery_executed": False,
        "redundancy_screening_executed": False,
        "refinement_executed": False,
        "validation_executed": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
    }


def _generation_manifest_payload(
    source_path: Path,
    artifact_root: Path,
    manifest_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "run_id": PANEL_GENERATION_ID,
        "module_id": MODULE_ID,
        "spec_id": PANEL_SPEC_ID,
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "artifact_root": str(artifact_root),
        "source_ohlcv_path": str(source_path),
        "candidate_count": len(manifest_rows),
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_ids": list(BLOCKED_CANDIDATE_IDS),
        "blocked_candidate_prefixes": list(BLOCKED_FAMILY_PREFIXES),
        "blocked_mechanisms": list(BLOCKED_MECHANISMS),
        "candidate_panel_files": [str(row["panel_path"]) for row in manifest_rows],
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
        "duplicate_key_count": int(sum(row["duplicate_key_count"] for row in manifest_rows)),
        "invalid_candidate_count": int(sum(row["invalid_candidate_count"] for row in manifest_rows)),
        "blocked_candidate_count": int(sum(row["blocked_candidate_count"] for row in manifest_rows)),
        "missing_signal_count": int(sum(row["missing_signal_count"] for row in manifest_rows)),
        "inactive_row_count": int(sum(row["inactive_row_count"] for row in manifest_rows)),
        "warmup_incomplete_count": int(sum(row["warmup_incomplete_count"] for row in manifest_rows)),
        "timing_policy": TIMING_POLICY,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
        "zero_variance_z_score_policy": ZERO_VARIANCE_Z_SCORE_POLICY,
        "stop_condition_triggered": False,
        "stop_condition_reason": None,
        "panel_generation_executed": True,
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


def write_dpath_panel_artifacts(
    source_path: Path = RAW_OHLCV_PATH,
    *,
    artifact_root: Path = ARTIFACT_ROOT,
    rank_min_count: int = RANK_MIN_COUNT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    registry = candidate_registry()
    validate_dpath_registry(registry)
    if tuple(registry["candidate_id"]) != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError("registry candidate IDs do not match approved DPath IDs")

    ohlcv = load_ohlcv_source(source_path)
    panels = build_candidate_panels(ohlcv, rank_min_count=rank_min_count)
    if tuple(panels) != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError("built panel candidate IDs do not match approved DPath candidate order")

    artifact_root.mkdir(parents=True, exist_ok=True)

    registry_manifest = _registry_manifest()
    formula_manifest = _formula_manifest(registry_manifest)
    feature_manifest = _feature_manifest()
    input_schema_manifest = _input_schema_manifest()
    registry_manifest.to_csv(artifact_root / "registry_manifest.csv", index=False)
    formula_manifest.to_csv(artifact_root / "formula_manifest.csv", index=False)
    feature_manifest.to_csv(artifact_root / "feature_manifest.csv", index=False)
    input_schema_manifest.to_csv(artifact_root / "input_schema_manifest.csv", index=False)

    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []

    for candidate_id, panel in panels.items():
        validation_errors = validate_candidate_panel_frame(panel, candidate_id)
        if validation_errors:
            raise ValueError(f"panel validation failed for {candidate_id}: " + "; ".join(validation_errors))
        panel_path = _panel_path(artifact_root, candidate_id)
        panel.to_parquet(panel_path, index=False)
        stats = _panel_stats(candidate_id, panel, panel_path)
        manifest_rows.append({column: stats[column] for column in MANIFEST_COLUMNS})
        summary_rows.append({column: stats[column] for column in SUMMARY_COLUMNS})
        schema_rows.append(_schema_report_row(candidate_id, panel, validation_errors))

    manifest = pd.DataFrame(manifest_rows, columns=MANIFEST_COLUMNS)
    summary = pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS)
    schema_report = pd.DataFrame(schema_rows, columns=SCHEMA_REPORT_COLUMNS)

    manifest.to_csv(artifact_root / "panel_manifest.csv", index=False)
    summary.to_csv(artifact_root / "panel_generation_summary.csv", index=False)
    schema_report.to_csv(artifact_root / "schema_validation_report.csv", index=False)
    _write_json(artifact_root / "metadata.json", _metadata_payload(source_path, artifact_root, manifest_rows))
    _write_json(
        artifact_root / "panel_generation_manifest.json",
        _generation_manifest_payload(source_path, artifact_root, manifest_rows),
    )

    return manifest, summary


def validate_dpath_panel_artifacts(artifact_root: Path = ARTIFACT_ROOT) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for file_name in REQUIRED_ARTIFACTS:
        if not (artifact_root / file_name).exists():
            errors.append(f"missing panel artifact: {artifact_root / file_name}")

    if artifact_root.exists():
        actual_files = {path.name for path in artifact_root.iterdir() if path.is_file()}
        unexpected_files = actual_files - set(REQUIRED_ARTIFACTS)
        for file_name in sorted(unexpected_files):
            errors.append(f"unexpected artifact file: {artifact_root / file_name}")
        actual_panel_files = set(artifact_root.glob("*_signal_panel.parquet"))
        unexpected = actual_panel_files - _expected_panel_files(artifact_root)
        missing = _expected_panel_files(artifact_root) - actual_panel_files
        for path in sorted(unexpected):
            errors.append(f"unexpected panel parquet: {path}")
        for path in sorted(missing):
            errors.append(f"missing expected panel parquet: {path}")

    manifest_path = artifact_root / "panel_manifest.csv"
    if not manifest_path.exists():
        return False, errors

    manifest = pd.read_csv(manifest_path)
    if tuple(manifest["candidate_id"].astype(str)) != IMPLEMENTED_CANDIDATE_IDS:
        errors.append("panel manifest candidate IDs do not match approved DPath IDs")
    if manifest["panel_path"].duplicated().any():
        errors.append("panel manifest contains duplicate panel paths")

    total_rows = 0
    for _, row in manifest.iterrows():
        candidate_id = str(row["candidate_id"])
        panel_path = Path(str(row["panel_path"]))
        if not panel_path.exists():
            errors.append(f"missing candidate panel file: {panel_path}")
            continue
        panel = pd.read_parquet(panel_path)
        total_rows += len(panel)
        errors.extend(validate_candidate_panel_frame(panel, candidate_id))
        if int(row["row_count"]) != len(panel):
            errors.append(f"manifest row_count mismatch for {candidate_id}")
        if int(row["duplicate_key_count"]) != 0:
            errors.append(f"manifest duplicate_key_count is nonzero for {candidate_id}")
        if int(row["blocked_candidate_count"]) != 0:
            errors.append(f"manifest blocked_candidate_count is nonzero for {candidate_id}")

    for csv_name, id_column in (
        ("registry_manifest.csv", "candidate_id"),
        ("formula_manifest.csv", "candidate_id"),
        ("schema_validation_report.csv", "candidate_id"),
    ):
        path = artifact_root / csv_name
        if path.exists():
            frame = pd.read_csv(path)
            if tuple(frame[id_column].astype(str)) != IMPLEMENTED_CANDIDATE_IDS:
                errors.append(f"{csv_name} candidate IDs do not reconcile")

    for json_name in ("metadata.json", "panel_generation_manifest.json"):
        path = artifact_root / json_name
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for field in (
            "ic_scoring_executed",
            "discovery_executed",
            "redundancy_screening_executed",
            "refinement_executed",
            "validation_executed",
            "governance_modified",
            "production_registration",
            "thresholds_modified",
            "ml_integration",
        ):
            if payload.get(field) is not False:
                errors.append(f"{json_name} forbidden action field is not fail-closed: {field}")
        if payload.get("panel_generation_executed") is not True:
            errors.append(f"{json_name} does not mark panel generation executed")
        if payload.get("candidate_ids") != list(IMPLEMENTED_CANDIDATE_IDS):
            errors.append(f"{json_name} candidate IDs mismatch")
        if int(payload.get("candidate_count", -1)) != len(IMPLEMENTED_CANDIDATE_IDS):
            errors.append(f"{json_name} candidate_count mismatch")
        if "row_count" in payload and int(payload["row_count"]) != int(total_rows):
            errors.append(f"{json_name} row_count mismatch")

    for forbidden in ("ic", "validation"):
        forbidden_paths = [
            path for path in artifact_root.glob(f"*{forbidden}*")
            if path.name not in {"schema_validation_report.csv"}
        ]
        for path in forbidden_paths:
            errors.append(f"forbidden artifact present: {path}")

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate DPath research panel artifacts.")
    parser.add_argument("--source", type=Path, default=RAW_OHLCV_PATH)
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        ok, errors = validate_dpath_panel_artifacts(args.artifact_root)
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"DPath panel validation passed for {args.artifact_root}")
        return 0

    manifest, _summary = write_dpath_panel_artifacts(args.source, artifact_root=args.artifact_root)
    print(f"Wrote {len(manifest)} DPath candidate panels to {args.artifact_root}")
    print("No IC, discovery, refinement, validation, governance, production, threshold, or ML work executed.")
    print(PANEL_GENERATION_CLASSIFICATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
