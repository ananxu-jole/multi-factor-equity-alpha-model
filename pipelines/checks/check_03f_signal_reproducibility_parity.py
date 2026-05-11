"""Compare current 03F notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_table  # noqa: E402
from src.scoring.reproducibility import (  # noqa: E402
    REPRODUCIBILITY_VERSION,
    run_03f_signal_reproducibility,
)


STAMP_COLUMNS = ["run_id", "reproducibility_version"]


def _strip_storage_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[column for column in STAMP_COLUMNS if column in df.columns]).copy()


def _normalize_scalar(value: object) -> object:
    if pd.isna(value):
        return None
    if isinstance(value, float):
        return round(value, 12)
    return value


def _records(df: pd.DataFrame) -> list[tuple[object, ...]]:
    if df.empty:
        return []
    normalized = _strip_storage_columns(df)
    normalized = normalized.reindex(sorted(normalized.columns), axis=1)
    rows = [
        tuple(_normalize_scalar(value) for value in row)
        for row in normalized.itertuples(index=False, name=None)
    ]
    return sorted(rows, key=lambda row: tuple(str(value) for value in row))


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03F signal reproducibility.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--reproducibility-version",
        default=REPRODUCIBILITY_VERSION,
        help="Signal reproducibility version label for dry-run output.",
    )
    args = parser.parse_args()

    current_results = load_table("signal_reproducibility_results_current", db_path=args.db_path)
    current_summary = load_table("signal_reproducibility_summary_current", db_path=args.db_path)
    current_gate = load_table("signal_reproducibility_gate_current", db_path=args.db_path)

    dry_run = run_03f_signal_reproducibility(
        db_path=args.db_path,
        reproducibility_version=args.reproducibility_version,
        write=False,
        verbose=False,
    )
    dry_results = dry_run["reproducibility_results"]
    dry_summary = dry_run["reproducibility_summary"]
    dry_gate = dry_run["reproducibility_gate"]

    comparison = pd.DataFrame(
        [
            _comparison_record("results_row_count", len(current_results), len(dry_results)),
            _comparison_record("summary_row_count", len(current_summary), len(dry_summary)),
            _comparison_record("gate_row_count", len(current_gate), len(dry_gate)),
            _comparison_record(
                "reproducibility_status_counts",
                _status_counts(current_summary, "reproducibility_status"),
                _status_counts(dry_summary, "reproducibility_status"),
            ),
            _comparison_record(
                "final_research_gate_counts",
                _status_counts(current_gate, "final_research_gate"),
                _status_counts(dry_gate, "final_research_gate"),
            ),
            _comparison_record("result_records", _records(current_results), _records(dry_results)),
            _comparison_record("summary_records", _records(current_summary), _records(dry_summary)),
            _comparison_record("gate_records", _records(current_gate), _records(dry_gate)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
