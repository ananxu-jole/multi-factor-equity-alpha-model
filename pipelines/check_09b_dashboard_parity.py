"""Compare current 09B dashboard state with a dry-run dashboard result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_table, table_exists  # noqa: E402
from src.portfolio.dashboard import DASHBOARD_OUTPUT_TABLES, run_09b_dashboard  # noqa: E402


def _names(df: pd.DataFrame, column: str) -> list[str]:
    if df.empty or column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())


def _metric_rows(df: pd.DataFrame) -> list[tuple[object, ...]]:
    columns = [
        "portfolio_method",
        "portfolio_mode",
        "annualized_return",
        "sharpe",
        "max_drawdown",
        "benchmark_total_return",
    ]
    if df.empty or not set(columns).issubset(df.columns):
        return []
    output = df[columns].copy()
    for column in columns[2:]:
        output[column] = pd.to_numeric(output[column], errors="coerce").round(12)
    return sorted(tuple(row) for row in output.itertuples(index=False, name=None))


def _status_fields(df: pd.DataFrame) -> list[tuple[str, str]]:
    if df.empty or not {"check_name", "passed"}.issubset(df.columns):
        return []
    return sorted(
        (str(row.check_name), str(bool(row.passed)))
        for row in df[["check_name", "passed"]].itertuples(index=False)
    )


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


def _saved_dashboard_counts(db_path: str | None, dry_run: dict[str, object]) -> list[dict[str, object]]:
    records = []
    for artifact, (current_table, _) in DASHBOARD_OUTPUT_TABLES.items():
        if table_exists(current_table, db_path=db_path):
            current_rows = len(load_table(current_table, db_path=db_path))
            dry_rows = len(dry_run[artifact])
            records.append(_comparison_record(f"saved_{artifact}_row_count", current_rows, dry_rows))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 09B dashboard.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--dashboard-version",
        default="phase9b_dashboard_v1",
        help="Dashboard version label for dry-run output.",
    )
    args = parser.parse_args()

    current_registry = load_table("survivor_alpha_registry_current", db_path=args.db_path)
    current_alpha_pool = load_table("portfolio_alpha_pool_current", db_path=args.db_path)
    current_portfolio_summary = load_table("portfolio_performance_summary_current", db_path=args.db_path)

    dry_run = run_09b_dashboard(
        db_path=args.db_path,
        dashboard_version=args.dashboard_version,
        write=False,
        verbose=False,
    )
    dry_survivor_summary = dry_run["survivor_summary"]
    dry_portfolio_summary = dry_run["portfolio_summary"]
    dry_benchmark_summary = dry_run["benchmark_summary"]
    dry_validation_report = dry_run["validation_report"]

    decision_col = (
        "promotion_decision_final"
        if "promotion_decision_final" in current_registry.columns
        else "promotion_decision"
        if "promotion_decision" in current_registry.columns
        else None
    )
    current_core = (
        current_registry.loc[current_registry[decision_col].eq("PROMOTE_CORE")]
        if decision_col is not None
        else current_registry
    )

    dry_final_names = []
    if not dry_survivor_summary.empty and {"metric", "value"}.issubset(dry_survivor_summary.columns):
        survivor_rows = dry_survivor_summary.loc[dry_survivor_summary["metric"].eq("survivor_names"), "value"]
        if not survivor_rows.empty and survivor_rows.iloc[0]:
            dry_final_names = sorted(str(survivor_rows.iloc[0]).split(", "))

    comparisons = [
        _comparison_record("dashboard_summary_row_count", None, len(dry_run["dashboard_summary"])),
        _comparison_record("survivor_summary_row_count", None, len(dry_survivor_summary)),
        _comparison_record("portfolio_summary_row_count", len(current_portfolio_summary), len(dry_portfolio_summary)),
        _comparison_record("benchmark_summary_row_count", len(current_portfolio_summary), len(dry_benchmark_summary)),
        _comparison_record("final_core_alpha_names", _names(current_core, "alpha_name"), dry_final_names),
        _comparison_record(
            "portfolio_method_names",
            _names(current_alpha_pool, "portfolio_method"),
            _names(dry_run["method_comparison"], "portfolio_method"),
        ),
        _comparison_record("long_only_and_long_short_metrics", _metric_rows(current_portfolio_summary), _metric_rows(dry_portfolio_summary)),
        _comparison_record(
            "benchmark_total_return",
            sorted(pd.to_numeric(current_portfolio_summary["benchmark_total_return"], errors="coerce").round(12).dropna().unique().tolist()),
            sorted(pd.to_numeric(dry_benchmark_summary["benchmark_total_return"], errors="coerce").round(12).dropna().unique().tolist()),
        ),
        _comparison_record("dashboard_status_fields", [], _status_fields(dry_validation_report)),
    ]
    comparisons.extend(_saved_dashboard_counts(args.db_path, dry_run))

    comparison = pd.DataFrame(comparisons)

    passthrough_checks = {"dashboard_summary_row_count", "survivor_summary_row_count", "dashboard_status_fields"}
    comparison.loc[
        comparison["check_name"].isin(passthrough_checks),
        "passed",
    ] = comparison.loc[
        comparison["check_name"].isin(passthrough_checks),
        "dry_run",
    ].apply(lambda value: len(value) > 0 if isinstance(value, list) else int(value) > 0)

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
