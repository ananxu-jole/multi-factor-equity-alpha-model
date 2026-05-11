"""Compare current 08 notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.survivor_registry import run_08_survivor_freeze  # noqa: E402
from src.db import load_table  # noqa: E402


def _names(df: pd.DataFrame, column: str = "alpha_name") -> list[str]:
    if df.empty or column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique().tolist())


def _status_pairs(df: pd.DataFrame) -> list[tuple[str, str]]:
    required = {"alpha_name", "final_status"}
    if df.empty or not required.issubset(df.columns):
        return []
    return sorted(
        (str(row.alpha_name), str(row.final_status))
        for row in df[["alpha_name", "final_status"]].dropna().itertuples(index=False)
    )


def _comparison_record(check_name: str, current: object, dry_run: object) -> dict[str, object]:
    return {
        "check_name": check_name,
        "passed": current == dry_run,
        "current": current,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 08 survivor freeze.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--survivor-version",
        default="phase8_cluster_aware_survivor_v5",
        help="Survivor version label for dry-run output.",
    )
    args = parser.parse_args()

    current_registry = load_table("survivor_alpha_registry_current", db_path=args.db_path)
    current_pre_ml = load_table("pre_ml_alpha_inputs_current", db_path=args.db_path)

    dry_run = run_08_survivor_freeze(
        db_path=args.db_path,
        survivor_version=args.survivor_version,
        write=False,
        verbose=False,
    )
    dry_registry = dry_run["survivor_registry"]
    dry_pre_ml = dry_run["pre_ml_alpha_inputs"]

    current_core = current_registry.loc[
        current_registry["promotion_decision_final"].eq("PROMOTE_CORE")
    ].copy()
    dry_core = dry_registry.loc[dry_registry["promotion_decision_final"].eq("PROMOTE_CORE")].copy()

    comparison = pd.DataFrame(
        [
            _comparison_record("registry_row_count", len(current_registry), len(dry_registry)),
            _comparison_record("pre_ml_row_count", len(current_pre_ml), len(dry_pre_ml)),
            _comparison_record("registry_alpha_names", _names(current_registry), _names(dry_registry)),
            _comparison_record("final_core_alpha_names", _names(current_core), _names(dry_core)),
            _comparison_record("final_status_by_alpha", _status_pairs(current_registry), _status_pairs(dry_registry)),
            _comparison_record("pre_ml_alpha_names", _names(current_pre_ml), _names(dry_pre_ml)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
