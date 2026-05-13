"""Compare current 03C notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_table  # noqa: E402
from src.scoring.decay import DECAY_VERSION, run_03c_signal_decay  # noqa: E402


STAMP_COLUMNS = ["run_id", "decay_version"]


def _strip_storage_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[column for column in STAMP_COLUMNS if column in df.columns]).copy()


def _normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    normalized = _strip_storage_columns(df)
    for column in normalized.columns:
        if pd.api.types.is_datetime64_any_dtype(normalized[column]) or column.lower() == "date":
            normalized[column] = pd.to_datetime(normalized[column], errors="coerce").dt.strftime("%Y-%m-%d")
        elif pd.api.types.is_float_dtype(normalized[column]):
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").round(12)
    normalized = normalized.reindex(sorted(normalized.columns), axis=1)
    if normalized.empty:
        return normalized
    return normalized.sort_values(normalized.columns.tolist(), kind="mergesort", na_position="first").reset_index(drop=True)


def _frame_digest(df: pd.DataFrame) -> str:
    csv = _normalize_frame(df).to_csv(index=False, na_rep="<NA>")
    return hashlib.sha256(csv.encode("utf-8")).hexdigest()


def _status_counts(df: pd.DataFrame, column: str) -> dict[str, int]:
    if df.empty or column not in df.columns:
        return {}
    return df[column].value_counts(dropna=False).sort_index().astype(int).to_dict()


def _close_enough(current: object, dry_run: object) -> bool:
    if isinstance(current, float) or isinstance(dry_run, float):
        if pd.isna(current) and pd.isna(dry_run):
            return True
        return math.isclose(float(current), float(dry_run), rel_tol=1e-10, abs_tol=1e-12)
    return current == dry_run


def _comparison_record(check_name: str, current: object, dry_run: object) -> dict[str, object]:
    return {
        "check_name": check_name,
        "passed": _close_enough(current, dry_run),
        "current": current,
        "dry_run": dry_run,
    }


def _digest_record(check_name: str, current: pd.DataFrame, dry_run: pd.DataFrame) -> dict[str, object]:
    current_digest = _frame_digest(current)
    dry_digest = _frame_digest(dry_run)
    return {
        "check_name": check_name,
        "passed": current_digest == dry_digest,
        "current": current_digest,
        "dry_run": dry_digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03C signal decay.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--decay-version",
        default=DECAY_VERSION,
        help="Signal decay version label for dry-run output.",
    )
    args = parser.parse_args()

    current_curve = load_table("signal_decay_curve_current", db_path=args.db_path)
    current_summary = load_table("signal_decay_summary_current", db_path=args.db_path)

    dry_run = run_03c_signal_decay(
        db_path=args.db_path,
        decay_version=args.decay_version,
        write=False,
        verbose=False,
    )
    dry_curve = dry_run["decay_curve"]
    dry_summary = dry_run["decay_summary"]

    comparison = pd.DataFrame(
        [
            _comparison_record("curve_rows", len(current_curve), len(dry_curve)),
            _comparison_record("summary_rows", len(current_summary), len(dry_summary)),
            _comparison_record(
                "decay_status_counts",
                _status_counts(current_summary, "decay_status"),
                _status_counts(dry_summary, "decay_status"),
            ),
            _comparison_record(
                "decay_risk_counts",
                _status_counts(current_summary, "decay_risk_flag"),
                _status_counts(dry_summary, "decay_risk_flag"),
            ),
            _digest_record("curve_digest", current_curve, dry_curve),
            _digest_record("summary_digest", current_summary, dry_summary),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
