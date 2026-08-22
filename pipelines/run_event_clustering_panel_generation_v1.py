from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.event_clustering_research_module_v1 import (
    CONTAMINATION_CONTROLS,
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
    build_event_clustering_candidate_panel,
    candidate_registry,
    expected_panel_columns,
    validate_event_clustering_registry,
)


PANEL_SPEC_ID = "event_clustering_panel_specification_v1"
PANEL_GENERATION_ID = "event_clustering_panel_generation_v1"
PANEL_GENERATION_CLASSIFICATION = "PANEL_GENERATION_READY_FOR_AUDIT"
PANEL_VERSION = "panel_v1"
ARTIFACT_ROOT = Path("artifacts/research/event_clustering_research_module_v1/panel_v1")
RAW_OHLCV_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")

PANEL_FILE_STEMS = {
    "ecluster_01_concentrated_absorption": "ecluster_01",
    "ecluster_02_aligned_pressure_resolution": "ecluster_02",
    "ecluster_03_fragmented_event_absorption": "ecluster_03",
    "ecluster_04_deteriorating_cluster_avoidance": "ecluster_04",
    "ecluster_05_aging_cluster_memory": "ecluster_05",
}

REQUIRED_ARTIFACTS = (
    "ecluster_01_signal_panel.parquet",
    "ecluster_02_signal_panel.parquet",
    "ecluster_03_signal_panel.parquet",
    "ecluster_04_signal_panel.parquet",
    "ecluster_05_signal_panel.parquet",
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

CONTRACT_COLUMNS = (
    "date",
    "ticker",
    "candidate_id",
    "signal_value",
    "activation_state",
    "warmup_state",
    "missing_data_state",
    "scientific_lineage",
    "mechanism",
    "contamination_metadata",
    "isolated_event_anchor",
    "timing_metadata",
    "after_close_policy",
    "source_spec_id",
    "module_id",
    "candidate_version",
)

PANEL_COLUMNS = (
    *CONTRACT_COLUMNS,
    *[column for column in expected_panel_columns() if column not in set(CONTRACT_COLUMNS)],
)

MANIFEST_COLUMNS = [
    "panel_file",
    "panel_file_type",
    "module_id",
    "panel_version",
    "candidate_id",
    "candidate_name",
    "mechanism",
    "candidate_count",
    "row_count",
    "date_min",
    "date_max",
    "ticker_count",
    "duplicate_key_count",
    "schema_version",
    "schema_validation_status",
    "lineage_validation_status",
    "registry_validation_status",
    "contamination_metadata_status",
    "activation_neutrality_status",
    "checksum_sha256",
    "created_at_utc",
    "source_spec_id",
]

SUMMARY_COLUMNS = [
    "candidate_id",
    "candidate_name",
    "mechanism",
    "row_count",
    "active_row_count",
    "inactive_neutralized_row_count",
    "warmup_row_count",
    "missing_row_count",
    "insufficient_cross_section_row_count",
    "date_min",
    "date_max",
    "ticker_count",
    "primary_horizon",
    "secondary_horizons",
]

SCHEMA_REPORT_COLUMNS = [
    "candidate_id",
    "check_name",
    "check_scope",
    "status",
    "observed_value",
    "expected_value",
    "failure_count",
    "notes",
]

MISSING_REASON_VOCABULARY = {
    "raw_ohlcv_missing",
    "rolling_warmup",
    "insufficient_cross_section",
    "nonfinite_feature",
    "inactive_neutralized",
}

FORBIDDEN_ARTIFACT_TOKENS = ("ic", "validation")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _checksum_record(path: Path, artifact_type: str) -> dict[str, object]:
    return {
        "artifact_path": str(path),
        "artifact_type": artifact_type,
        "checksum_algorithm": "SHA-256",
        "checksum_sha256": _sha256(path),
        "byte_size": path.stat().st_size,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_phase": PANEL_GENERATION_ID,
    }


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


def _activation_state(panel: pd.DataFrame) -> pd.Series:
    state = pd.Series("active", index=panel.index, dtype="object")
    state.loc[panel["missing_reason"].eq("inactive_neutralized")] = "inactive_neutralized"
    state.loc[panel["missing_reason"].eq("rolling_warmup")] = "rolling_warmup"
    state.loc[panel["missing_reason"].eq("raw_ohlcv_missing")] = "raw_ohlcv_missing"
    state.loc[panel["missing_reason"].eq("nonfinite_feature")] = "nonfinite_feature"
    state.loc[panel["missing_reason"].eq("insufficient_cross_section")] = "insufficient_cross_section"
    state.loc[~panel["is_active"].astype(bool) & panel["feature_warmup_complete"].astype(bool)] = "inactive_neutralized"
    return state


def _warmup_state(panel: pd.DataFrame) -> pd.Series:
    return pd.Series(
        ["warmup_complete" if value else "rolling_warmup" for value in panel["feature_warmup_complete"].astype(bool)],
        index=panel.index,
        dtype="object",
    )


def _missing_data_state(panel: pd.DataFrame) -> pd.Series:
    return panel["missing_reason"].fillna("not_missing").astype("object")


def _scientific_lineage(panel: pd.DataFrame) -> pd.Series:
    return (
        "formula_spec="
        + panel["spec_id"].astype(str)
        + "|panel_spec="
        + PANEL_SPEC_ID
        + "|implementation_review=event_clustering_formula_implementation_review_v1"
    )


def _timing_metadata(panel: pd.DataFrame) -> pd.Series:
    return "signal_date_uses_ohlcv_through_close_t|forward_returns_begin_after_t|" + panel[
        "after_close_timing_policy"
    ].astype(str)


def _enrich_panel_contract(panel: pd.DataFrame) -> pd.DataFrame:
    enriched = panel.copy()
    enriched["activation_state"] = _activation_state(enriched)
    enriched["warmup_state"] = _warmup_state(enriched)
    enriched["missing_data_state"] = _missing_data_state(enriched)
    enriched["scientific_lineage"] = _scientific_lineage(enriched)
    enriched["contamination_metadata"] = enriched["contamination_reference_set"]
    enriched["isolated_event_anchor"] = enriched["isolated_event_anchor_20"]
    enriched["timing_metadata"] = _timing_metadata(enriched)
    enriched["after_close_policy"] = enriched["after_close_timing_policy"]
    enriched["source_spec_id"] = PANEL_SPEC_ID
    enriched["candidate_version"] = "v1"
    return enriched.loc[:, PANEL_COLUMNS]


def build_candidate_panels(
    ohlcv: pd.DataFrame,
    *,
    rank_min_count: int = RANK_MIN_COUNT,
) -> dict[str, pd.DataFrame]:
    validate_event_clustering_registry()
    panel = build_event_clustering_candidate_panel(ohlcv, min_cross_section_count=rank_min_count)
    panels: dict[str, pd.DataFrame] = {}
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        subset = panel.loc[panel["candidate_id"].eq(candidate_id)].copy()
        subset = _enrich_panel_contract(subset)
        subset = subset.sort_values(["date", "ticker", "candidate_id"]).reset_index(drop=True)
        panels[candidate_id] = subset
    return panels


def validate_candidate_panel_frame(panel: pd.DataFrame, candidate_id: str) -> list[str]:
    errors: list[str] = []
    if candidate_id not in IMPLEMENTED_CANDIDATE_IDS:
        errors.append(f"candidate_id is not approved for Event Clustering panel generation: {candidate_id}")
        return errors
    if list(panel.columns) != list(PANEL_COLUMNS):
        errors.append("panel schema does not match required Event Clustering long-form columns")
    if panel.empty:
        errors.append(f"panel is empty: {candidate_id}")
        return errors
    if set(panel["candidate_id"].astype(str)) != {candidate_id}:
        errors.append(f"panel candidate_id values do not match file candidate_id: {candidate_id}")
    if panel["candidate_id"].astype(str).str.startswith(("vov_", "dpath_")).any():
        errors.append(f"blocked candidate appeared in panel: {candidate_id}")
    if set(panel["module_id"].astype(str)) != {MODULE_ID}:
        errors.append(f"module_id mismatch for {candidate_id}")
    if set(panel["source_spec_id"].astype(str)) != {PANEL_SPEC_ID}:
        errors.append(f"source_spec_id mismatch for {candidate_id}")
    if set(panel["spec_id"].astype(str)) != {SPEC_ID}:
        errors.append(f"formula spec_id mismatch for {candidate_id}")
    if set(panel["after_close_policy"].astype(str)) != {TIMING_POLICY}:
        errors.append(f"after_close_policy mismatch for {candidate_id}")
    if set(panel["research_status"].astype(str)) != {RESEARCH_STATUS}:
        errors.append(f"research_status mismatch for {candidate_id}")
    if set(panel["candidate_version"].astype(str)) != {"v1"}:
        errors.append(f"candidate_version mismatch for {candidate_id}")
    if panel[["date", "ticker", "candidate_id"]].duplicated().any():
        errors.append(f"duplicate panel rows found for {candidate_id}")
    if not set(panel["missing_reason"].dropna().astype(str)).issubset(MISSING_REASON_VOCABULARY):
        errors.append(f"missing_reason contains values outside vocabulary for {candidate_id}")
    for column in CONTRACT_COLUMNS:
        if column not in panel.columns:
            errors.append(f"contract column missing for {candidate_id}: {column}")
    for column in (
        "scientific_lineage",
        "mechanism",
        "contamination_metadata",
        "timing_metadata",
        "formula_text",
        "activation_text",
        "scientific_question",
        "expected_evidence",
    ):
        if panel[column].isna().any():
            errors.append(f"lineage/metadata column is null for {candidate_id}: {column}")
    for control in CONTAMINATION_CONTROLS:
        if not panel["contamination_metadata"].astype(str).str.contains(control, regex=False).all():
            errors.append(f"contamination metadata missing {control} for {candidate_id}")

    inactive = panel["activation_state"].eq("inactive_neutralized") & panel["pre_activation_raw_score"].notna()
    if not (panel.loc[inactive, "signal_value"].dropna() == 0.5).all():
        errors.append(f"inactive rows were not neutralized to signal_value 0.5 for {candidate_id}")
    warmup = panel["warmup_state"].eq("rolling_warmup")
    if panel.loc[warmup, "signal_value"].notna().any():
        errors.append(f"warmup rows contain non-null signal_value for {candidate_id}")
    return errors


def _schema_report_rows(candidate_id: str, panel: pd.DataFrame, errors: Iterable[str]) -> list[dict[str, object]]:
    error_list = list(errors)
    duplicate_count = int(panel[["date", "ticker", "candidate_id"]].duplicated().sum()) if not panel.empty else -1
    checks = [
        ("schema", list(panel.columns) == list(PANEL_COLUMNS), len(panel.columns), len(PANEL_COLUMNS)),
        ("duplicate_keys", duplicate_count == 0, duplicate_count, 0),
        ("candidate_id", set(panel["candidate_id"].astype(str)) == {candidate_id}, "|".join(sorted(set(panel["candidate_id"].astype(str)))), candidate_id),
        ("lineage", not any("lineage" in err or "metadata" in err for err in error_list), "see_notes", "PASS"),
        ("registry", candidate_id in IMPLEMENTED_CANDIDATE_IDS, candidate_id, "approved_candidate"),
        ("contamination_metadata", not any("contamination metadata" in err for err in error_list), "see_notes", "PASS"),
        ("activation_neutrality", not any("neutralized" in err for err in error_list), "see_notes", "PASS"),
    ]
    rows = []
    for check_name, ok, observed, expected in checks:
        rows.append(
            {
                "candidate_id": candidate_id,
                "check_name": check_name,
                "check_scope": "candidate_panel",
                "status": "PASS" if ok else "FAIL",
                "observed_value": observed,
                "expected_value": expected,
                "failure_count": 0 if ok else 1,
                "notes": "panel check passed" if ok else "; ".join(error_list),
            }
        )
    return rows


def _registry_manifest() -> pd.DataFrame:
    registry = candidate_registry().copy()
    registry["module_id"] = MODULE_ID
    registry["candidate_version"] = "v1"
    registry["source_spec_id"] = PANEL_SPEC_ID
    registry["formula_spec_id"] = SPEC_ID
    registry["candidate_count"] = len(IMPLEMENTED_CANDIDATE_IDS)
    return registry


def _formula_manifest(registry: pd.DataFrame) -> pd.DataFrame:
    out = registry[
        [
            "candidate_id",
            "candidate_name",
            "formula_summary",
            "activation_summary",
            "expected_sign",
            "horizon",
            "secondary_horizons",
            "source_spec_id",
        ]
    ].copy()
    out = out.rename(
        columns={
            "formula_summary": "formula_text",
            "activation_summary": "activation_text",
            "horizon": "primary_horizon",
        }
    )
    out["formula_version"] = "v1"
    out["after_close_policy"] = TIMING_POLICY
    out["implementation_review"] = "docs/research_notes/event_clustering_formula_implementation_review_v1.md"
    return out


def _feature_manifest() -> pd.DataFrame:
    rows = []
    for column in RAW_INPUT_COLUMNS:
        rows.append(
            {
                "feature_name": column,
                "feature_type": "raw_input",
                "definition_text": "Required OHLCV input.",
                "raw_input_dependencies": column,
                "rolling_window": pd.NA,
                "cross_sectional_dependency": False,
                "warmup_requirement": "none",
                "missing_data_policy": "raw_ohlcv_missing",
                "used_by_candidate_ids": "|".join(IMPLEMENTED_CANDIDATE_IDS),
                "timing_policy": TIMING_POLICY,
            }
        )
    for column in DIAGNOSTIC_COLUMNS:
        rows.append(
            {
                "feature_name": column,
                "feature_type": "derived_or_diagnostic",
                "definition_text": "Implemented Event Clustering feature or diagnostic column.",
                "raw_input_dependencies": "|".join(RAW_INPUT_COLUMNS),
                "rolling_window": "varies_by_feature",
                "cross_sectional_dependency": column.endswith("_rank")
                or column
                in {
                    "alignment_score_5",
                    "fragmentation_score_5",
                    "absorption_5",
                    "deterioration_5",
                    "low_extension_20",
                    "low_churn_5",
                    "liquidity_rank_20",
                    "stress_proxy_20",
                },
                "warmup_requirement": "event_zscore_60_and_candidate_feature_maturity",
                "missing_data_policy": "nonfinite_feature",
                "used_by_candidate_ids": "|".join(IMPLEMENTED_CANDIDATE_IDS),
                "timing_policy": TIMING_POLICY,
            }
        )
    return pd.DataFrame(rows)


def _input_schema_manifest(source_path: Path, ohlcv: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in RAW_INPUT_COLUMNS:
        rows.append(
            {
                "input_field": column,
                "required": True,
                "type": "date" if column == "date" else "string" if column == "ticker" else "float",
                "point_in_time_policy": "OHLCV through close t only",
                "missing_data_policy": "no imputation; controlled missing state",
                "raw_source": str(source_path),
                "notes": f"input_row_count={len(ohlcv)}",
            }
        )
    return pd.DataFrame(rows)


def _panel_stats(candidate_id: str, panel: pd.DataFrame, panel_path: Path) -> dict[str, object]:
    duplicate_key_count = int(panel[["date", "ticker", "candidate_id"]].duplicated().sum())
    return {
        "panel_file": str(panel_path),
        "panel_file_type": "parquet",
        "module_id": MODULE_ID,
        "panel_version": PANEL_VERSION,
        "candidate_id": candidate_id,
        "candidate_name": str(panel["candidate_name"].iloc[0]),
        "mechanism": str(panel["mechanism"].iloc[0]),
        "candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "row_count": int(len(panel)),
        "date_min": str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": str(pd.to_datetime(panel["date"]).max().date()),
        "ticker_count": int(panel["ticker"].nunique()),
        "duplicate_key_count": duplicate_key_count,
        "schema_version": "event_clustering_panel_schema_v1",
        "schema_validation_status": "PASS",
        "lineage_validation_status": "PASS",
        "registry_validation_status": "PASS",
        "contamination_metadata_status": "PASS",
        "activation_neutrality_status": "PASS",
        "checksum_sha256": "",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_spec_id": PANEL_SPEC_ID,
    }


def _summary_row(candidate_id: str, panel: pd.DataFrame) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "candidate_name": str(panel["candidate_name"].iloc[0]),
        "mechanism": str(panel["mechanism"].iloc[0]),
        "row_count": int(len(panel)),
        "active_row_count": int(panel["is_active"].astype(bool).sum()),
        "inactive_neutralized_row_count": int(panel["activation_state"].eq("inactive_neutralized").sum()),
        "warmup_row_count": int(panel["warmup_state"].eq("rolling_warmup").sum()),
        "missing_row_count": int(panel["signal_value"].isna().sum()),
        "insufficient_cross_section_row_count": int(panel["missing_data_state"].eq("insufficient_cross_section").sum()),
        "date_min": str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": str(pd.to_datetime(panel["date"]).max().date()),
        "ticker_count": int(panel["ticker"].nunique()),
        "primary_horizon": str(panel["primary_horizon"].iloc[0]),
        "secondary_horizons": str(panel["secondary_horizons"].iloc[0]),
    }


def _metadata_payload(
    source_path: Path,
    artifact_root: Path,
    manifest_rows: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "module_id": MODULE_ID,
        "panel_version": PANEL_VERSION,
        "platform_version": "v2.0.0-platform-scientific-methodology",
        "source_spec_id": PANEL_SPEC_ID,
        "formula_spec_id": SPEC_ID,
        "implementation_review_classification": "IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES",
        "artifact_root": str(artifact_root),
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "candidate_version": "v1",
        "after_close_policy": TIMING_POLICY,
        "research_status": RESEARCH_STATUS,
        "guardrails": {
            "ic_scoring_executed": False,
            "validation_executed": False,
            "governance_modified": False,
            "production_registration": False,
            "thresholds_modified": False,
            "ml_integration": False,
        },
        "source_documents": [
            "docs/research_notes/event_clustering_panel_specification_v1.md",
            "docs/research_notes/event_clustering_formula_implementation_review_v1.md",
            "docs/research_notes/event_clustering_formula_implementation_v1.md",
            "docs/research_notes/event_clustering_formula_and_panel_specification_v1.md",
        ],
        "source_ohlcv_path": str(source_path),
        "contamination_controls": list(CONTAMINATION_CONTROLS),
        "checksum_policy": "SHA-256 for every parquet panel, metadata.json, and panel_manifest.csv",
        "panel_generation_executed": True,
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def _generation_manifest_payload(
    source_path: Path,
    artifact_root: Path,
    manifest_rows: list[dict[str, object]],
    checksums: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "module_id": MODULE_ID,
        "panel_version": PANEL_VERSION,
        "artifact_root": str(artifact_root),
        "generation_phase": PANEL_GENERATION_ID,
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "source_spec_id": PANEL_SPEC_ID,
        "formula_spec_id": SPEC_ID,
        "implementation_review": "docs/research_notes/event_clustering_formula_implementation_review_v1.md",
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "source_ohlcv_path": str(source_path),
        "input_schema_manifest": str(artifact_root / "input_schema_manifest.csv"),
        "registry_manifest": str(artifact_root / "registry_manifest.csv"),
        "formula_manifest": str(artifact_root / "formula_manifest.csv"),
        "feature_manifest": str(artifact_root / "feature_manifest.csv"),
        "panel_manifest": str(artifact_root / "panel_manifest.csv"),
        "metadata_json": str(artifact_root / "metadata.json"),
        "schema_validation_report": str(artifact_root / "schema_validation_report.csv"),
        "checksums": checksums,
        "validation_results": {
            "schema": "PASS",
            "duplicate_keys": int(sum(row["duplicate_key_count"] for row in manifest_rows)),
            "registry": "PASS",
            "lineage": "PASS",
            "contamination_metadata": "PASS",
            "activation_neutrality": "PASS",
            "manifest_reconciliation": "PASS",
            "checksum_reconciliation": "PASS",
        },
        "guardrail_results": {
            "blocked_candidates": "PASS",
            "ic_scoring_executed": False,
            "validation_executed": False,
            "governance_modified": False,
            "production_registration": False,
            "thresholds_modified": False,
            "ml_integration": False,
        },
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def write_event_clustering_panel_artifacts(
    source_path: Path = RAW_OHLCV_PATH,
    *,
    artifact_root: Path = ARTIFACT_ROOT,
    rank_min_count: int = RANK_MIN_COUNT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    registry = candidate_registry()
    validate_event_clustering_registry(registry)
    if tuple(registry["candidate_id"]) != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError("registry candidate IDs do not match approved Event Clustering IDs")

    ohlcv = load_ohlcv_source(source_path)
    panels = build_candidate_panels(ohlcv, rank_min_count=rank_min_count)
    if tuple(panels) != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError("built panel candidate IDs do not match approved Event Clustering candidate order")

    artifact_root.mkdir(parents=True, exist_ok=True)

    registry_manifest = _registry_manifest()
    formula_manifest = _formula_manifest(registry_manifest)
    feature_manifest = _feature_manifest()
    input_schema_manifest = _input_schema_manifest(source_path, ohlcv)
    registry_manifest.to_csv(artifact_root / "registry_manifest.csv", index=False)
    formula_manifest.to_csv(artifact_root / "formula_manifest.csv", index=False)
    feature_manifest.to_csv(artifact_root / "feature_manifest.csv", index=False)
    input_schema_manifest.to_csv(artifact_root / "input_schema_manifest.csv", index=False)

    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []
    checksum_records: list[dict[str, object]] = []

    for candidate_id, panel in panels.items():
        validation_errors = validate_candidate_panel_frame(panel, candidate_id)
        if validation_errors:
            raise ValueError(f"panel validation failed for {candidate_id}: " + "; ".join(validation_errors))
        panel_path = _panel_path(artifact_root, candidate_id)
        panel.to_parquet(panel_path, index=False)
        panel_checksum = _checksum_record(panel_path, "parquet_panel")
        checksum_records.append(panel_checksum)
        stats = _panel_stats(candidate_id, panel, panel_path)
        stats["checksum_sha256"] = panel_checksum["checksum_sha256"]
        manifest_rows.append({column: stats[column] for column in MANIFEST_COLUMNS})
        summary_rows.append(_summary_row(candidate_id, panel))
        schema_rows.extend(_schema_report_rows(candidate_id, panel, validation_errors))

    manifest = pd.DataFrame(manifest_rows, columns=MANIFEST_COLUMNS)
    summary = pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS)
    schema_report = pd.DataFrame(schema_rows, columns=SCHEMA_REPORT_COLUMNS)

    manifest_path = artifact_root / "panel_manifest.csv"
    summary_path = artifact_root / "panel_generation_summary.csv"
    schema_path = artifact_root / "schema_validation_report.csv"
    metadata_path = artifact_root / "metadata.json"
    generation_manifest_path = artifact_root / "panel_generation_manifest.json"

    manifest.to_csv(manifest_path, index=False)
    summary.to_csv(summary_path, index=False)
    schema_report.to_csv(schema_path, index=False)
    _write_json(metadata_path, _metadata_payload(source_path, artifact_root, manifest_rows))

    checksum_records.append(_checksum_record(metadata_path, "metadata_json"))
    checksum_records.append(_checksum_record(manifest_path, "panel_manifest_csv"))
    _write_json(
        generation_manifest_path,
        _generation_manifest_payload(source_path, artifact_root, manifest_rows, checksum_records),
    )

    return manifest, summary


def _read_generation_manifest(artifact_root: Path) -> dict[str, object] | None:
    path = artifact_root / "panel_generation_manifest.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_checksum_records(artifact_root: Path) -> list[str]:
    errors: list[str] = []
    payload = _read_generation_manifest(artifact_root)
    if payload is None:
        return ["missing panel_generation_manifest.json"]
    records = payload.get("checksums", [])
    required_paths = [*_expected_panel_files(artifact_root), artifact_root / "metadata.json", artifact_root / "panel_manifest.csv"]
    record_by_path = {str(record.get("artifact_path")): record for record in records if isinstance(record, dict)}
    for path in required_paths:
        record = record_by_path.get(str(path))
        if record is None:
            errors.append(f"missing checksum record for {path}")
            continue
        if record.get("checksum_algorithm") != "SHA-256":
            errors.append(f"checksum algorithm mismatch for {path}")
        if not path.exists():
            errors.append(f"checksum target missing: {path}")
            continue
        observed = _sha256(path)
        if observed != record.get("checksum_sha256"):
            errors.append(f"checksum mismatch for {path}")
    return errors


def validate_event_clustering_panel_artifacts(artifact_root: Path = ARTIFACT_ROOT) -> tuple[bool, list[str]]:
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
        for token in FORBIDDEN_ARTIFACT_TOKENS:
            for path in artifact_root.glob(f"*{token}*"):
                if path.name not in {"schema_validation_report.csv"}:
                    errors.append(f"forbidden artifact present: {path}")

    manifest_path = artifact_root / "panel_manifest.csv"
    if not manifest_path.exists():
        return False, errors
    manifest = pd.read_csv(manifest_path)
    if tuple(manifest["candidate_id"].astype(str)) != IMPLEMENTED_CANDIDATE_IDS:
        errors.append("panel manifest candidate IDs do not match approved Event Clustering IDs")
    if int(manifest["duplicate_key_count"].sum()) != 0:
        errors.append("panel manifest duplicate_key_count is nonzero")
    if not (manifest["schema_validation_status"] == "PASS").all():
        errors.append("panel manifest schema status is not PASS")
    if manifest["panel_file"].duplicated().any():
        errors.append("panel manifest contains duplicate panel files")

    total_rows = 0
    for _, row in manifest.iterrows():
        candidate_id = str(row["candidate_id"])
        panel_path = Path(str(row["panel_file"]))
        if not panel_path.exists():
            errors.append(f"missing candidate panel file: {panel_path}")
            continue
        panel = pd.read_parquet(panel_path)
        total_rows += len(panel)
        errors.extend(validate_candidate_panel_frame(panel, candidate_id))
        if int(row["row_count"]) != len(panel):
            errors.append(f"manifest row_count mismatch for {candidate_id}")
        if str(row["checksum_sha256"]) != _sha256(panel_path):
            errors.append(f"panel_manifest checksum mismatch for {candidate_id}")

    for csv_name, id_column in (
        ("registry_manifest.csv", "candidate_id"),
        ("formula_manifest.csv", "candidate_id"),
    ):
        path = artifact_root / csv_name
        if path.exists():
            frame = pd.read_csv(path)
            if tuple(frame[id_column].astype(str)) != IMPLEMENTED_CANDIDATE_IDS:
                errors.append(f"{csv_name} candidate IDs do not reconcile")

    schema_report_path = artifact_root / "schema_validation_report.csv"
    if schema_report_path.exists():
        schema_report = pd.read_csv(schema_report_path)
        if not (schema_report["status"] == "PASS").all():
            errors.append("schema validation report contains non-PASS rows")

    for json_name in ("metadata.json", "panel_generation_manifest.json"):
        path = artifact_root / json_name
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("candidate_ids") != list(IMPLEMENTED_CANDIDATE_IDS):
            errors.append(f"{json_name} candidate IDs mismatch")
        if int(payload.get("candidate_count", -1)) != len(IMPLEMENTED_CANDIDATE_IDS):
            errors.append(f"{json_name} candidate_count mismatch")
        if payload.get("module_id") != MODULE_ID:
            errors.append(f"{json_name} module_id mismatch")
        if payload.get("panel_version") != PANEL_VERSION:
            errors.append(f"{json_name} panel_version mismatch")
        for field in (
            "ic_scoring_executed",
            "validation_executed",
            "governance_modified",
            "production_registration",
            "thresholds_modified",
            "ml_integration",
        ):
            value = payload.get(field)
            if value is None and isinstance(payload.get("guardrails"), dict):
                value = payload["guardrails"].get(field)
            if value is None and isinstance(payload.get("guardrail_results"), dict):
                value = payload["guardrail_results"].get(field)
            if value is not False:
                errors.append(f"{json_name} forbidden action field is not fail-closed: {field}")
        if "row_count" in payload and int(payload["row_count"]) != int(total_rows):
            errors.append(f"{json_name} row_count mismatch")

    errors.extend(_validate_checksum_records(artifact_root))
    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Event Clustering research panel artifacts.")
    parser.add_argument("--source", type=Path, default=RAW_OHLCV_PATH)
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument("--rank-min-count", type=int, default=RANK_MIN_COUNT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        ok, errors = validate_event_clustering_panel_artifacts(args.artifact_root)
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"Event Clustering panel validation passed for {args.artifact_root}")
        return 0

    manifest, _summary = write_event_clustering_panel_artifacts(
        args.source,
        artifact_root=args.artifact_root,
        rank_min_count=args.rank_min_count,
    )
    print(f"Wrote {len(manifest)} Event Clustering candidate panels to {args.artifact_root}")
    print("No IC, validation, governance, production, threshold, or ML work executed.")
    print(PANEL_GENERATION_CLASSIFICATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
