"""Compare current 07 notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.stress import run_07_alpha_stress  # noqa: E402
from src.db import load_table  # noqa: E402


def _names(df: pd.DataFrame) -> list[str]:
    if df.empty or "alpha_name" not in df.columns:
        return []
    return sorted(df["alpha_name"].dropna().astype(str).unique().tolist())


def _rounded_records(df: pd.DataFrame, columns: list[str]) -> list[tuple[object, ...]]:
    if df.empty or not set(columns).issubset(df.columns):
        return []
    output = df[columns].copy()
    for column in ["pass_rate", "worst_degradation"]:
        if column in output.columns:
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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 07 alpha stress.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--stress-version",
        default="phase7_alpha_stress_v1",
        help="Stress version label for dry-run output.",
    )
    args = parser.parse_args()

    current_results = load_table("alpha_stress_results_current", db_path=args.db_path)
    current_summary = load_table("alpha_stress_summary_current", db_path=args.db_path)
    current_gate = load_table("alpha_stress_gate_current", db_path=args.db_path)

    dry_run = run_07_alpha_stress(
        db_path=args.db_path,
        stress_version=args.stress_version,
        write=False,
        verbose=False,
    )
    dry_results = dry_run["stress_results"]
    dry_summary = dry_run["stress_summary"]
    dry_gate = dry_run["stress_gate"]

    gate_columns = [
        "alpha_name",
        "horizon",
        "status",
        "survivor_tier",
        "promotion_decision",
        "alpha_role",
        "pass_rate",
        "worst_degradation",
        "catastrophic_degradation",
    ]
    summary_columns = [
        "alpha_name",
        "horizon",
        "pass_rate",
        "worst_degradation",
        "catastrophic_degradation",
    ]

    comparison = pd.DataFrame(
        [
            _comparison_record("stress_results_row_count", len(current_results), len(dry_results)),
            _comparison_record("stress_summary_row_count", len(current_summary), len(dry_summary)),
            _comparison_record("stress_gate_row_count", len(current_gate), len(dry_gate)),
            _comparison_record("stress_candidate_names", _names(current_gate), _names(dry_gate)),
            _comparison_record("stress_gate_decisions", _rounded_records(current_gate, gate_columns), _rounded_records(dry_gate, gate_columns)),
            _comparison_record("stress_summary_metrics", _rounded_records(current_summary, summary_columns), _rounded_records(dry_summary, summary_columns)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
