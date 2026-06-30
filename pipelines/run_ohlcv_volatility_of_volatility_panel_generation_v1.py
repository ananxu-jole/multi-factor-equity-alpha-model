from __future__ import annotations

import argparse
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

from pipelines.ohlcv_volatility_of_volatility_research_module_v1 import (
    BLOCKED_FAMILY_PREFIXES,
    FAMILY,
    IMPLEMENTED_CANDIDATE_IDS,
    RAW_INPUT_COLUMNS,
    RUN_ID,
    SHARED_DIAGNOSTIC_COLUMNS,
    VOV_CANDIDATES,
    _candidate_raw_scores,
    _rank_cs_from_frame,
    candidate_registry,
    compute_vov_features,
    validate_vov_registry,
)


PANEL_SPEC_ID = "ohlcv_volatility_of_volatility_research_module_panel_specification_v1"
PANEL_GENERATION_ID = "ohlcv_volatility_of_volatility_research_module_panel_generation_v1"
PANEL_GENERATION_CLASSIFICATION = "PANEL_GENERATION_READY_FOR_AUDIT"
TIMING_POLICY = "after_close_t_forward_returns_after_t"
ACTIVATION_NEUTRALIZATION = "inactive_pre_rank_raw_score_zero"
PANEL_SHAPE = "long_per_candidate"
RESEARCH_STATUS = "RESEARCH_ONLY"
RANK_MIN_COUNT = 50

RAW_OHLCV_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")
ARTIFACT_ROOT = Path("artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1")

PANEL_COLUMNS = [
    "date",
    "ticker",
    "candidate_id",
    "source_spec_id",
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
]

SUMMARY_COLUMNS = [
    "candidate_id",
    "source_spec_id",
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
    "timing_policy",
    "generation_status",
]

MANIFEST_COLUMNS = [
    "candidate_id",
    "source_spec_id",
    "module_id",
    "panel_path",
    "row_count",
    "date_min",
    "date_max",
    "ticker_count",
    "duplicate_key_count",
    "invalid_candidate_count",
    "missing_signal_count",
    "inactive_row_count",
    "warmup_incomplete_count",
    "rank_min_count",
    "dates_below_rank_min_count",
    "timing_policy",
    "schema_status",
    "generation_status",
]

SCHEMA_REPORT_COLUMNS = [
    "candidate_id",
    "schema_status",
    "candidate_id_status",
    "source_spec_id_status",
    "module_id_status",
    "long_form_status",
    "duplicate_status",
    "activation_status",
    "timing_status",
    "family_b_c_status",
    "notes",
]

MISSING_REASON_VOCABULARY = {
    "raw_ohlcv_missing",
    "rolling_warmup",
    "insufficient_cross_section",
    "nonfinite_feature",
    "inactive_zeroed",
    "invalid_candidate_id",
    "duplicate_key",
    "schema_violation",
}


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


def _candidate_definitions() -> dict[str, object]:
    return {candidate.candidate_id: candidate for candidate in VOV_CANDIDATES}


def _finite_count_by_date(frame: pd.DataFrame, values: pd.Series) -> pd.Series:
    return values.notna().groupby(frame["date"], sort=False).transform("sum").astype("int64")


def _dates_below_rank_min(frame: pd.DataFrame, values: pd.Series, rank_min_count: int) -> int:
    counts = values.notna().groupby(frame["date"], sort=False).sum()
    return int((counts < rank_min_count).sum())


def build_long_candidate_panels(
    ohlcv: pd.DataFrame,
    *,
    rank_min_count: int = RANK_MIN_COUNT,
) -> dict[str, pd.DataFrame]:
    validate_vov_registry()
    features = compute_vov_features(ohlcv, min_cross_section_count=rank_min_count)
    raw_scores = _candidate_raw_scores(features, min_cross_section_count=rank_min_count)
    definitions = _candidate_definitions()
    panels: dict[str, pd.DataFrame] = {}

    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        definition = definitions[candidate_id]
        pre_activation_raw_score, active = raw_scores[candidate_id]
        active = active.fillna(False)
        raw_score = pre_activation_raw_score.where(active, 0.0)
        raw_score = raw_score.where(pre_activation_raw_score.notna())
        signal_value = _rank_cs_from_frame(
            features,
            raw_score,
            min_cross_section_count=rank_min_count,
        ).where(pre_activation_raw_score.notna())
        finite_count = _finite_count_by_date(features, raw_score)
        feature_warmup_complete = pre_activation_raw_score.notna()

        missing_reason = pd.Series(pd.NA, index=features.index, dtype="object")
        missing_reason.loc[pre_activation_raw_score.isna()] = "rolling_warmup"
        missing_reason.loc[pre_activation_raw_score.notna() & ~active] = "inactive_zeroed"
        missing_reason.loc[
            pre_activation_raw_score.notna() & active & signal_value.isna()
        ] = "insufficient_cross_section"

        panel = pd.DataFrame(
            {
                "date": features["date"],
                "ticker": features["ticker"].astype(str),
                "candidate_id": candidate_id,
                "source_spec_id": definition.source_spec_id,
                "module_id": RUN_ID,
                "family": FAMILY,
                "research_status": RESEARCH_STATUS,
                "primary_horizon": definition.primary_horizon,
                "secondary_horizons": "|".join(definition.secondary_horizons),
                "signal_value": signal_value,
                "raw_score": raw_score,
                "pre_activation_raw_score": pre_activation_raw_score,
                "is_active": active.astype(bool),
                "feature_warmup_complete": feature_warmup_complete.astype(bool),
                "finite_cross_section_count": finite_count,
                "rank_min_count": rank_min_count,
                "missing_reason": missing_reason,
                "timing_policy": TIMING_POLICY,
                "created_by_spec": PANEL_SPEC_ID,
            }
        )
        panel = panel.loc[:, PANEL_COLUMNS].sort_values(["date", "ticker"]).reset_index(drop=True)
        panels[candidate_id] = panel

    return panels


def validate_candidate_panel_frame(panel: pd.DataFrame, candidate_id: str) -> list[str]:
    definitions = _candidate_definitions()
    errors: list[str] = []
    if candidate_id not in IMPLEMENTED_CANDIDATE_IDS:
        errors.append(f"candidate_id is not approved for VoV panel generation: {candidate_id}")
        return errors
    if list(panel.columns) != PANEL_COLUMNS:
        errors.append("panel schema does not match required long-form columns")
    if panel.empty:
        errors.append(f"panel is empty: {candidate_id}")
        return errors

    if set(panel["candidate_id"].astype(str)) != {candidate_id}:
        errors.append(f"panel candidate_id values do not match file candidate_id: {candidate_id}")
    if any(str(value).startswith(BLOCKED_FAMILY_PREFIXES) for value in panel["candidate_id"].dropna().unique()):
        errors.append("Family B/C candidate ID appeared in VoV panel")
    if set(panel["source_spec_id"].astype(str)) != {definitions[candidate_id].source_spec_id}:
        errors.append(f"source_spec_id mismatch for {candidate_id}")
    if set(panel["module_id"].astype(str)) != {RUN_ID}:
        errors.append(f"module_id mismatch for {candidate_id}")
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
    if not np.allclose(panel.loc[inactive_with_features, "raw_score"].fillna(np.nan), 0.0, equal_nan=False):
        errors.append(f"inactive rows were not neutralized to raw_score zero for {candidate_id}")
    missing_pre = panel["pre_activation_raw_score"].isna()
    if panel.loc[missing_pre, "raw_score"].notna().any():
        errors.append(f"missing pre-activation raw scores were converted to finite raw_score for {candidate_id}")
    if panel.loc[missing_pre, "signal_value"].notna().any():
        errors.append(f"missing pre-activation raw scores were converted to finite signal for {candidate_id}")
    if panel["rank_min_count"].astype(int).nunique() != 1:
        errors.append(f"rank_min_count is not constant for {candidate_id}")

    return errors


def _panel_stats(candidate_id: str, panel: pd.DataFrame, panel_path: Path) -> dict[str, object]:
    duplicate_key_count = int(panel[["date", "ticker", "candidate_id"]].duplicated().sum())
    return {
        "candidate_id": candidate_id,
        "source_spec_id": str(panel["source_spec_id"].iloc[0]),
        "module_id": RUN_ID,
        "panel_path": str(panel_path),
        "row_count": int(len(panel)),
        "date_min": str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": str(pd.to_datetime(panel["date"]).max().date()),
        "ticker_count": int(panel["ticker"].nunique()),
        "duplicate_key_count": duplicate_key_count,
        "invalid_candidate_count": int(candidate_id not in IMPLEMENTED_CANDIDATE_IDS),
        "missing_signal_count": int(panel["signal_value"].isna().sum()),
        "non_null_signal_count": int(panel["signal_value"].notna().sum()),
        "inactive_row_count": int((~panel["is_active"].astype(bool)).sum()),
        "warmup_incomplete_count": int((~panel["feature_warmup_complete"].astype(bool)).sum()),
        "rank_min_count": int(panel["rank_min_count"].iloc[0]),
        "dates_below_rank_min_count": int(
            panel.groupby("date", sort=False)["signal_value"].apply(lambda s: s.notna().sum()).lt(panel["rank_min_count"].iloc[0]).sum()
        ),
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
        "source_spec_id_status": "PASS" if not any("source_spec_id" in e for e in error_list) else "FAIL",
        "module_id_status": "PASS" if not any("module_id" in e for e in error_list) else "FAIL",
        "long_form_status": "PASS" if list(panel.columns) == PANEL_COLUMNS else "FAIL",
        "duplicate_status": "PASS" if not panel[["date", "ticker", "candidate_id"]].duplicated().any() else "FAIL",
        "activation_status": "PASS" if not any("neutralized" in e or "pre-activation" in e for e in error_list) else "FAIL",
        "timing_status": "PASS" if set(panel["timing_policy"].astype(str)) == {TIMING_POLICY} else "FAIL",
        "family_b_c_status": "PASS"
        if not any(str(value).startswith(BLOCKED_FAMILY_PREFIXES) for value in panel["candidate_id"].dropna().unique())
        else "FAIL",
        "notes": "panel validation passed" if ok else "; ".join(error_list),
    }


def _metadata_payload(source_path: Path, manifest_rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "run_id": PANEL_GENERATION_ID,
        "module_id": RUN_ID,
        "spec_id": PANEL_SPEC_ID,
        "implementation_note": "ohlcv_volatility_of_volatility_research_module_implementation_v1",
        "implementation_review_note": "ohlcv_volatility_of_volatility_research_module_implementation_review_v1",
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_prefixes": list(BLOCKED_FAMILY_PREFIXES),
        "family": FAMILY,
        "research_status": RESEARCH_STATUS,
        "timing_policy": TIMING_POLICY,
        "rank_min_count": RANK_MIN_COUNT,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
        "panel_shape": PANEL_SHAPE,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
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
        "candidate_count": len(manifest_rows),
        "row_count": int(sum(row["row_count"] for row in manifest_rows)),
    }


def _generation_manifest_payload(source_path: Path, manifest_rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "run_id": PANEL_GENERATION_ID,
        "module_id": RUN_ID,
        "spec_id": PANEL_SPEC_ID,
        "classification": PANEL_GENERATION_CLASSIFICATION,
        "artifact_root": str(ARTIFACT_ROOT),
        "source_ohlcv_path": str(source_path),
        "candidate_count": len(manifest_rows),
        "candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "blocked_candidate_prefixes": list(BLOCKED_FAMILY_PREFIXES),
        "panel_shape": PANEL_SHAPE,
        "candidate_panel_files": [str(row["panel_path"]) for row in manifest_rows],
        "duplicate_key_count": int(sum(row["duplicate_key_count"] for row in manifest_rows)),
        "invalid_candidate_count": int(sum(row["invalid_candidate_count"] for row in manifest_rows)),
        "missing_signal_count": int(sum(row["missing_signal_count"] for row in manifest_rows)),
        "inactive_row_count": int(sum(row["inactive_row_count"] for row in manifest_rows)),
        "warmup_incomplete_count": int(sum(row["warmup_incomplete_count"] for row in manifest_rows)),
        "timing_policy": TIMING_POLICY,
        "activation_neutralization": ACTIVATION_NEUTRALIZATION,
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


def write_vov_panel_artifacts(
    source_path: Path = RAW_OHLCV_PATH,
    *,
    artifact_root: Path = ARTIFACT_ROOT,
    rank_min_count: int = RANK_MIN_COUNT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    registry = candidate_registry()
    validate_vov_registry(registry)
    if any(str(cid).startswith(BLOCKED_FAMILY_PREFIXES) for cid in registry["candidate_id"]):
        raise ValueError("Family B/C candidate IDs are not allowed in VoV panel generation")

    ohlcv = load_ohlcv_source(source_path)
    panels = build_long_candidate_panels(ohlcv, rank_min_count=rank_min_count)
    if tuple(panels) != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError("built panel candidate IDs do not match approved VoV candidate order")

    artifact_root.mkdir(parents=True, exist_ok=True)

    registry.to_csv(artifact_root / "candidate_registry.csv", index=False)
    registry.loc[:, ["candidate_id", "source_spec_id", "formula_summary", "activation_summary"]].to_csv(
        artifact_root / "candidate_formula_manifest.csv",
        index=False,
    )
    pd.DataFrame(
        [{"column": column, "required": True} for column in RAW_INPUT_COLUMNS]
    ).to_csv(artifact_root / "input_schema.csv", index=False)
    pd.DataFrame(
        [{"feature": column, "role": "shared_diagnostic"} for column in SHARED_DIAGNOSTIC_COLUMNS]
    ).to_csv(artifact_root / "derived_feature_manifest.csv", index=False)

    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    schema_rows: list[dict[str, object]] = []

    for candidate_id, panel in panels.items():
        validation_errors = validate_candidate_panel_frame(panel, candidate_id)
        if validation_errors:
            raise ValueError(f"panel validation failed for {candidate_id}: " + "; ".join(validation_errors))

        panel_path = artifact_root / f"{candidate_id}_signal_panel.parquet"
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
    _write_json(artifact_root / "metadata.json", _metadata_payload(source_path, manifest_rows))
    _write_json(
        artifact_root / "panel_generation_manifest.json",
        _generation_manifest_payload(source_path, manifest_rows),
    )

    return manifest, summary


def validate_vov_panel_artifacts(artifact_root: Path = ARTIFACT_ROOT) -> tuple[bool, list[str]]:
    errors: list[str] = []
    required_files = [
        "metadata.json",
        "panel_manifest.csv",
        "panel_generation_summary.csv",
        "panel_generation_manifest.json",
        "schema_validation_report.csv",
        "candidate_registry.csv",
        "candidate_formula_manifest.csv",
        "input_schema.csv",
        "derived_feature_manifest.csv",
    ]
    for file_name in required_files:
        if not (artifact_root / file_name).exists():
            errors.append(f"missing panel artifact: {artifact_root / file_name}")

    manifest_path = artifact_root / "panel_manifest.csv"
    if not manifest_path.exists():
        return False, errors

    manifest = pd.read_csv(manifest_path)
    if tuple(manifest["candidate_id"].astype(str)) != IMPLEMENTED_CANDIDATE_IDS:
        errors.append("panel manifest candidate IDs do not match approved VoV IDs")
    if manifest["panel_path"].duplicated().any():
        errors.append("panel manifest contains duplicate panel paths")

    for _, row in manifest.iterrows():
        candidate_id = str(row["candidate_id"])
        panel_path = Path(str(row["panel_path"]))
        if not panel_path.exists():
            errors.append(f"missing candidate panel file: {panel_path}")
            continue
        panel = pd.read_parquet(panel_path)
        panel_errors = validate_candidate_panel_frame(panel, candidate_id)
        errors.extend(panel_errors)
        if int(row["row_count"]) != len(panel):
            errors.append(f"manifest row_count mismatch for {candidate_id}")
        if int(row["duplicate_key_count"]) != 0:
            errors.append(f"manifest duplicate_key_count is nonzero for {candidate_id}")

    for json_name in ("metadata.json", "panel_generation_manifest.json"):
        path = artifact_root / json_name
        if path.exists():
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

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate VoV-only research panel artifacts.")
    parser.add_argument("--source", type=Path, default=RAW_OHLCV_PATH)
    parser.add_argument("--artifact-root", type=Path, default=ARTIFACT_ROOT)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if args.validate_only:
        ok, errors = validate_vov_panel_artifacts(args.artifact_root)
        if not ok:
            for error in errors:
                print(error)
            return 1
        print(f"VoV panel validation passed for {args.artifact_root}")
        return 0

    manifest, _summary = write_vov_panel_artifacts(args.source, artifact_root=args.artifact_root)
    print(f"Wrote {len(manifest)} VoV candidate panels to {args.artifact_root}")
    print("No IC, discovery, redundancy screening, refinement, validation, governance, production, threshold, or ML work executed.")
    print(PANEL_GENERATION_CLASSIFICATION)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
