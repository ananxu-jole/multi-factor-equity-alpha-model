"""Compare current 04B notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.constructed_wfv import run_04b_alpha_wfv  # noqa: E402
from src.db import load_table  # noqa: E402


def _names(df: pd.DataFrame) -> list[str]:
    if df.empty or "alpha_name" not in df.columns:
        return []
    return sorted(df["alpha_name"].dropna().astype(str).unique().tolist())


def _horizons(df: pd.DataFrame) -> list[int]:
    if df.empty or "horizon" not in df.columns:
        return []
    return sorted(pd.to_numeric(df["horizon"], errors="coerce").dropna().astype(int).unique().tolist())


def _gate_records(df: pd.DataFrame) -> list[tuple[object, ...]]:
    columns = [
        "alpha_name",
        "horizon",
        "status",
        "effective_mean_test_ic",
        "effective_test_ic_ir",
        "persistence_ratio",
        "sign_consistency",
    ]
    if df.empty or not set(columns).issubset(df.columns):
        return []
    output = df[columns].copy()
    for column in columns[3:]:
        output[column] = pd.to_numeric(output[column], errors="coerce").round(12)
    return sorted(tuple(row) for row in output.itertuples(index=False, name=None))


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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 04B constructed alpha WFV.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--wfv-version",
        default="phase4b_alpha_wfv_v1",
        help="Constructed alpha WFV version label for dry-run output.",
    )
    args = parser.parse_args()

    current_windows = load_table("constructed_alpha_wfv_windows_current", db_path=args.db_path)
    current_results = load_table("constructed_alpha_wfv_window_results_current", db_path=args.db_path)
    current_summary = load_table("constructed_alpha_wfv_summary_current", db_path=args.db_path)
    current_gate = load_table("constructed_alpha_wfv_gate_current", db_path=args.db_path)

    dry_run = run_04b_alpha_wfv(
        db_path=args.db_path,
        wfv_version=args.wfv_version,
        write=False,
        verbose=False,
    )
    dry_windows = dry_run["alpha_wfv_windows"]
    dry_results = dry_run["alpha_wfv_results"]
    dry_summary = dry_run["alpha_wfv_summary"]
    dry_gate = dry_run["alpha_wfv_gate"]

    comparison = pd.DataFrame(
        [
            _comparison_record("wfv_windows_row_count", len(current_windows), len(dry_windows)),
            _comparison_record("wfv_result_row_count", len(current_results), len(dry_results)),
            _comparison_record("summary_row_count", len(current_summary), len(dry_summary)),
            _comparison_record("gate_row_count", len(current_gate), len(dry_gate)),
            _comparison_record("alpha_names", _names(current_gate), _names(dry_gate)),
            _comparison_record("horizons", _horizons(current_gate), _horizons(dry_gate)),
            _comparison_record("wfv_gate_records", _gate_records(current_gate), _gate_records(dry_gate)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
