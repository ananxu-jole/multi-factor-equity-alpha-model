"""Compare current 09 notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_table, table_exists  # noqa: E402
from src.portfolio.construction import run_09_portfolio_construction  # noqa: E402


def _names(df: pd.DataFrame, column: str) -> list[str]:
    if df.empty or column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())


def _metric_rows(df: pd.DataFrame) -> list[tuple[object, ...]]:
    metric_columns = [
        "portfolio_method",
        "portfolio_mode",
        "annualized_return",
        "sharpe",
        "max_drawdown",
        "benchmark_total_return",
    ]
    if df.empty or not set(metric_columns).issubset(df.columns):
        return []
    rounded = df[metric_columns].copy()
    for column in metric_columns[2:]:
        rounded[column] = pd.to_numeric(rounded[column], errors="coerce").round(12)
    return sorted(tuple(row) for row in rounded.itertuples(index=False, name=None))


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


def _non_core_used(alpha_pool: pd.DataFrame) -> int:
    decision_col = (
        "promotion_decision_final"
        if "promotion_decision_final" in alpha_pool.columns
        else "promotion_decision"
        if "promotion_decision" in alpha_pool.columns
        else None
    )
    if decision_col is None:
        return 0
    return int(alpha_pool[decision_col].astype(str).ne("PROMOTE_CORE").sum())


def _regime_overlay_used(alpha_pool: pd.DataFrame, db_path: str | None) -> list[str]:
    if alpha_pool.empty or "alpha_name" not in alpha_pool.columns:
        return []
    if table_exists("regime_context_alpha_metadata_current", db_path=db_path):
        overlay_metadata = load_table("regime_context_alpha_metadata_current", db_path=db_path)
        if "alpha_name" in overlay_metadata.columns:
            return sorted(
                set(alpha_pool["alpha_name"].dropna()).intersection(
                    set(overlay_metadata["alpha_name"].dropna())
                )
            )
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 09 portfolio construction.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--portfolio-version",
        default="phase9_portfolio_v1",
        help="Portfolio version label for dry-run output.",
    )
    args = parser.parse_args()

    current_alpha_pool = load_table("portfolio_alpha_pool_current", db_path=args.db_path)
    current_weights = load_table("portfolio_weights_current", db_path=args.db_path)
    current_returns = load_table("portfolio_backtest_results_current", db_path=args.db_path)
    current_summary = load_table("portfolio_performance_summary_current", db_path=args.db_path)

    dry_run = run_09_portfolio_construction(
        db_path=args.db_path,
        portfolio_version=args.portfolio_version,
        write=False,
        verbose=False,
    )
    dry_alpha_pool = dry_run["portfolio_alpha_pool"]
    dry_weights = dry_run["portfolio_weights"]
    dry_returns = dry_run["portfolio_returns"]
    dry_summary = dry_run["portfolio_results"]

    comparison = pd.DataFrame(
        [
            _comparison_record(
                "portfolio_method_names",
                _names(current_alpha_pool, "portfolio_method"),
                _names(dry_alpha_pool, "portfolio_method"),
            ),
            _comparison_record("alpha_pool_row_count", len(current_alpha_pool), len(dry_alpha_pool)),
            _comparison_record("weights_row_count", len(current_weights), len(dry_weights)),
            _comparison_record("returns_row_count", len(current_returns), len(dry_returns)),
            _comparison_record("summary_row_count", len(current_summary), len(dry_summary)),
            _comparison_record("performance_metrics", _metric_rows(current_summary), _metric_rows(dry_summary)),
            _comparison_record(
                "alpha_names_used",
                _names(current_alpha_pool, "alpha_name"),
                _names(dry_alpha_pool, "alpha_name"),
            ),
            _comparison_record("review_satellite_excluded", _non_core_used(current_alpha_pool), _non_core_used(dry_alpha_pool)),
            _comparison_record(
                "regime_overlays_excluded",
                _regime_overlay_used(current_alpha_pool, args.db_path),
                _regime_overlay_used(dry_alpha_pool, args.db_path),
            ),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
