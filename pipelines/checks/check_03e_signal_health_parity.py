"""Compare current 03E notebook outputs with a dry-run engine result."""

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
from src.scoring.health import HEALTH_VERSION, run_03e_signal_health  # noqa: E402


STAMP_COLUMNS = ["run_id", "health_version"]


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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03E signal health.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--health-version",
        default=HEALTH_VERSION,
        help="Signal health version label for dry-run output.",
    )
    args = parser.parse_args()

    current_score = load_table("signal_health_score_current", db_path=args.db_path)
    current_summary = load_table("signal_health_summary_current", db_path=args.db_path)
    current_attribution = load_table("signal_health_attribution_current", db_path=args.db_path)

    dry_run = run_03e_signal_health(
        db_path=args.db_path,
        health_version=args.health_version,
        write=False,
        verbose=False,
    )
    dry_score = dry_run["signal_health_score"]
    dry_summary = dry_run["signal_health_summary"]
    dry_attribution = dry_run["signal_health_attribution"]

    comparison = pd.DataFrame(
        [
            _comparison_record("score_row_count", len(current_score), len(dry_score)),
            _comparison_record("summary_row_count", len(current_summary), len(dry_summary)),
            _comparison_record("attribution_row_count", len(current_attribution), len(dry_attribution)),
            _comparison_record(
                "health_gate_counts",
                _status_counts(current_score, "signal_health_gate"),
                _status_counts(dry_score, "signal_health_gate"),
            ),
            _comparison_record("score_records", _records(current_score), _records(dry_score)),
            _comparison_record("summary_records", _records(current_summary), _records(dry_summary)),
            _comparison_record("attribution_records", _records(current_attribution), _records(dry_attribution)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
