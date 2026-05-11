"""Compare current 04A notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.construction import run_04a_alpha_construction  # noqa: E402
from src.db import load_table  # noqa: E402


def _names(df: pd.DataFrame) -> list[str]:
    if df.empty or "alpha_name" not in df.columns:
        return []
    return sorted(df["alpha_name"].dropna().astype(str).unique().tolist())


def _quality_records(quality: pd.DataFrame, diagnostics: pd.DataFrame) -> list[tuple[object, ...]]:
    columns = [
        "alpha_name",
        "status",
        "finite_pct",
        "missing_pct",
        "avg_turnover_proxy",
        "median_turnover_proxy",
        "max_turnover_proxy",
    ]
    if quality.empty or "alpha_name" not in quality.columns:
        return []
    merged = quality.copy()
    if not diagnostics.empty and "alpha_name" in diagnostics.columns:
        diagnostic_columns = [
            column
            for column in ["alpha_name", "median_turnover_proxy", "max_turnover_proxy"]
            if column in diagnostics.columns
        ]
        merged = merged.merge(diagnostics[diagnostic_columns], on="alpha_name", how="left")
    for column in columns:
        if column not in merged.columns:
            merged[column] = pd.NA
    output = merged[columns].copy()
    for column in columns[2:]:
        output[column] = pd.to_numeric(output[column], errors="coerce").round(12)
    return sorted(tuple(row) for row in output.itertuples(index=False, name=None))


def _status_counts(df: pd.DataFrame) -> dict[str, int]:
    if df.empty or "status" not in df.columns:
        return {}
    return df["status"].value_counts(dropna=False).sort_index().astype(int).to_dict()


def _family_counts(signal_pool: pd.DataFrame) -> list[tuple[object, ...]]:
    if signal_pool.empty or not {"source_role", "signal_family", "component_id"}.issubset(signal_pool.columns):
        return []
    counts = (
        signal_pool.groupby(["source_role", "signal_family"], dropna=False)["component_id"]
        .nunique()
        .reset_index(name="n_components")
    )
    return sorted(tuple(row) for row in counts.itertuples(index=False, name=None))


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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 04A alpha construction.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--construction-version",
        default="phase4a_alpha_construction_v1",
        help="Alpha construction version label for dry-run output.",
    )
    args = parser.parse_args()

    current_candidates = load_table("alpha_constructed_candidates_current", db_path=args.db_path)
    current_quality = load_table("alpha_construction_quality_current", db_path=args.db_path)
    current_diagnostics = load_table("alpha_construction_diagnostics_current", db_path=args.db_path)
    current_signal_pool = load_table("alpha_signal_pool_current", db_path=args.db_path)

    dry_run = run_04a_alpha_construction(
        db_path=args.db_path,
        construction_version=args.construction_version,
        write=False,
        verbose=False,
    )
    dry_candidates = dry_run["constructed_alpha_candidates"]
    dry_quality = dry_run["alpha_construction_quality"]
    dry_diagnostics = dry_run["alpha_construction_diagnostics"]
    dry_signal_pool = dry_run["alpha_signal_pool"]

    comparison = pd.DataFrame(
        [
            _comparison_record("constructed_alpha_row_count", len(current_candidates), len(dry_candidates)),
            _comparison_record("alpha_names", _names(current_quality), _names(dry_quality)),
            _comparison_record("quality_gate_records", _quality_records(current_quality, current_diagnostics), _quality_records(dry_quality, dry_diagnostics)),
            _comparison_record("approved_rejected_counts", _status_counts(current_quality), _status_counts(dry_quality)),
            _comparison_record("family_summary_counts", _family_counts(current_signal_pool), _family_counts(dry_signal_pool)),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
