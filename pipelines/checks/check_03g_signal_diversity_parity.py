"""Compare current 03G notebook outputs with a dry-run engine result."""

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
from src.scoring.diversity import DIVERSITY_VERSION, run_03g_signal_diversity  # noqa: E402


STAMP_COLUMNS = ["run_id", "diversity_version"]


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


def _selected_keys(df: pd.DataFrame) -> list[str]:
    if df.empty or not {"signal_key", "selected_flag"}.issubset(df.columns):
        return []
    return sorted(df.loc[df["selected_flag"].eq(1), "signal_key"].dropna().astype(str).tolist())


def _diagnostic_tuple(df: pd.DataFrame) -> tuple[object, ...]:
    columns = [
        "n_candidates",
        "avg_abs_correlation",
        "max_abs_correlation",
        "median_abs_correlation",
        "effective_signal_count",
    ]
    if df.empty:
        return tuple()
    row = _strip_storage_columns(df).iloc[0]
    return tuple(_normalize_scalar(row.get(column)) for column in columns)


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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03G signal diversity.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--diversity-version",
        default=DIVERSITY_VERSION,
        help="Signal diversity version label for dry-run output.",
    )
    args = parser.parse_args()

    current_similarity = load_table("signal_diversity_similarity_current", db_path=args.db_path)
    current_diagnostics = load_table("signal_diversity_diagnostics_current", db_path=args.db_path)
    current_selection = load_table("signal_diversity_selection_current", db_path=args.db_path)
    current_family = load_table("signal_diversity_family_report_current", db_path=args.db_path)
    current_cluster = load_table("signal_diversity_cluster_report_current", db_path=args.db_path)

    dry_run = run_03g_signal_diversity(
        db_path=args.db_path,
        diversity_version=args.diversity_version,
        write=False,
        verbose=False,
    )
    dry_similarity = dry_run["signal_diversity_similarity"]
    dry_diagnostics = dry_run["signal_diversity_diagnostics"]
    dry_selection = dry_run["signal_diversity_selection"]
    dry_family = dry_run["signal_diversity_family_report"]
    dry_cluster = dry_run["signal_diversity_cluster_report"]

    comparison = pd.DataFrame(
        [
            _comparison_record("similarity_row_count", len(current_similarity), len(dry_similarity)),
            _comparison_record("diagnostics_row_count", len(current_diagnostics), len(dry_diagnostics)),
            _comparison_record("selection_row_count", len(current_selection), len(dry_selection)),
            _comparison_record("family_row_count", len(current_family), len(dry_family)),
            _comparison_record("cluster_row_count", len(current_cluster), len(dry_cluster)),
            _comparison_record("selected_signal_keys", _selected_keys(current_selection), _selected_keys(dry_selection)),
            _comparison_record("diagnostic_metrics", _diagnostic_tuple(current_diagnostics), _diagnostic_tuple(dry_diagnostics)),
            _comparison_record("similarity_records", _records(current_similarity), _records(dry_similarity)),
            _comparison_record("selection_records", _records(current_selection), _records(dry_selection)),
            _comparison_record("family_records", _records(current_family), _records(dry_family)),
            _comparison_record("cluster_records", _records(current_cluster), _records(dry_cluster)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
