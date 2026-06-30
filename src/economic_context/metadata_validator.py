from __future__ import annotations

import pandas as pd

from src.economic_context.schema import (
    POINT_IN_TIME_VALIDATED,
    REQUIRED_STATIC_SEED_COLUMNS,
    SNAPSHOT_WARNING,
)
from src.economic_context.metadata_loader import OVERRIDE_REQUIRED_COLUMNS


def validate_required_columns(frame: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    rows = []
    columns = set(frame.columns)
    for column in required_columns:
        rows.append(
            {
                "check": "required_column_present",
                "field": column,
                "passed": column in columns,
                "message": "" if column in columns else f"Missing required column: {column}",
            }
        )
    return pd.DataFrame(rows)


def validate_static_seed(frame: pd.DataFrame) -> pd.DataFrame:
    checks = [validate_required_columns(frame, REQUIRED_STATIC_SEED_COLUMNS)]
    checks.append(validate_snapshot_warning(frame))
    checks.append(validate_no_duplicate_tickers(frame))
    checks.append(validate_required_field_completeness(frame, REQUIRED_STATIC_SEED_COLUMNS))
    return pd.concat(checks, ignore_index=True)


def validate_overrides(frame: pd.DataFrame) -> pd.DataFrame:
    checks = [validate_required_columns(frame, OVERRIDE_REQUIRED_COLUMNS)]
    checks.append(validate_no_duplicate_tickers(frame))
    checks.append(
        validate_required_field_completeness(
            frame,
            ["ticker", "normalized_ticker", "sector", "industry", "source", "source_date"],
        )
    )
    checks.append(validate_override_usage_flags(frame))
    checks.append(validate_snapshot_warning(frame))
    return pd.concat(checks, ignore_index=True)


def validate_override_usage_flags(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    allowed_bool_strings = {"true", "false", "0", "1", "yes", "no"}
    for column in ["is_static_snapshot", "validation_usage_allowed", "diagnostic_usage_allowed"]:
        if column not in frame.columns:
            rows.append(
                {
                    "check": "override_usage_flag_valid",
                    "field": column,
                    "passed": False,
                    "message": "Column missing",
                }
            )
            continue
        values = frame[column].fillna("").astype(str).str.strip().str.lower()
        invalid = int((~values.isin(allowed_bool_strings)).sum())
        if column == "validation_usage_allowed":
            validation_true = int(values.isin({"true", "1", "yes"}).sum())
            passed = invalid == 0 and validation_true == 0
            message = f"{invalid} invalid values; {validation_true} rows allow validation"
        elif column == "diagnostic_usage_allowed":
            diagnostic_false = int(values.isin({"false", "0", "no"}).sum())
            passed = invalid == 0 and diagnostic_false == 0
            message = f"{invalid} invalid values; {diagnostic_false} rows block diagnostics"
        elif column == "is_static_snapshot":
            static_false = int(values.isin({"false", "0", "no"}).sum())
            passed = invalid == 0 and static_false == 0
            message = f"{invalid} invalid values; {static_false} rows not marked static"
        rows.append(
            {
                "check": "override_usage_flag_valid",
                "field": column,
                "passed": passed,
                "message": message,
            }
        )
    return pd.DataFrame(rows)


def validate_snapshot_warning(frame: pd.DataFrame) -> pd.DataFrame:
    if "snapshot_warning" not in frame.columns:
        return pd.DataFrame(
            [
                {
                    "check": "snapshot_warning_exact",
                    "field": "snapshot_warning",
                    "passed": False,
                    "message": "Missing snapshot_warning column",
                }
            ]
        )
    bad_count = int(frame["snapshot_warning"].astype(str).ne(SNAPSHOT_WARNING).sum())
    return pd.DataFrame(
        [
            {
                "check": "snapshot_warning_exact",
                "field": "snapshot_warning",
                "passed": bad_count == 0,
                "message": f"{bad_count} rows do not equal {SNAPSHOT_WARNING}",
            }
        ]
    )


def validate_no_duplicate_tickers(frame: pd.DataFrame) -> pd.DataFrame:
    if "ticker" not in frame.columns:
        return pd.DataFrame(
            [{"check": "duplicate_ticker", "field": "ticker", "passed": False, "message": "Missing ticker column"}]
        )
    tickers = frame["ticker"].fillna("").astype(str).str.strip().str.upper()
    duplicate_count = int(tickers[tickers.ne("")].duplicated().sum())
    return pd.DataFrame(
        [
            {
                "check": "duplicate_ticker",
                "field": "ticker",
                "passed": duplicate_count == 0,
                "message": f"{duplicate_count} duplicate ticker rows",
            }
        ]
    )


def validate_required_field_completeness(
    frame: pd.DataFrame,
    required_columns: list[str],
) -> pd.DataFrame:
    rows = []
    total = len(frame)
    for column in required_columns:
        if column not in frame.columns:
            rows.append(
                {
                    "check": "required_field_non_missing",
                    "field": column,
                    "passed": False,
                    "message": "Column missing",
                    "missing_rows": total,
                    "missing_ratio": 1.0 if total else 0.0,
                }
            )
            continue
        missing = int(frame[column].fillna("").astype(str).str.strip().eq("").sum())
        rows.append(
            {
                "check": "required_field_non_missing",
                "field": column,
                "passed": missing == 0,
                "message": f"{missing} missing rows",
                "missing_rows": missing,
                "missing_ratio": float(missing / total) if total else 0.0,
            }
        )
    return pd.DataFrame(rows)


def assert_validation_use_allowed(frame: pd.DataFrame) -> None:
    """Block alpha/validation usage unless all rows are explicitly point-in-time validated."""
    if "point_in_time_quality" not in frame.columns:
        raise PermissionError("Economic context frame has no point_in_time_quality column.")
    bad = frame["point_in_time_quality"].astype(str).ne(POINT_IN_TIME_VALIDATED)
    if bool(bad.any()):
        raise PermissionError(
            "Economic context data is not point-in-time validated; alpha validation use is blocked."
        )
