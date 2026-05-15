"""CLI for Conditional Edge Atlas v1 research artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scoring.conditional_edge_atlas import (  # noqa: E402
    ATLAS_VERSION,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SIGNALS,
    DEFAULT_SUMMARY_PATH,
    run_conditional_edge_atlas,
)


def _print_description() -> None:
    print("stage_id: conditional_edge_atlas")
    print(f"atlas_version: {ATLAS_VERSION}")
    print("default_focus_signals:")
    for signal in DEFAULT_SIGNALS:
        print(f"  - {signal}")
    print(f"default_output_dir: {DEFAULT_OUTPUT_DIR}")
    print(f"default_summary_path: {DEFAULT_SUMMARY_PATH}")
    print("policy: research-only standalone artifacts; no official gates, schemas, WFV, promotion, alpha, portfolio, or execution changes")


def _print_summary(result: dict[str, object]) -> None:
    print("summary:")
    for row in result["run_summary"].to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Conditional Edge Atlas v1 research framework.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print atlas metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Build atlas without writing artifacts.")
    mode.add_argument("--run", action="store_true", help="Build atlas and write standalone artifacts.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--output-dir", default=None, help="Optional artifact output directory.")
    parser.add_argument("--summary-path", default=None, help="Optional markdown summary path.")
    parser.add_argument("--focus-only", action="store_true", help="Use only the default focus signals instead of all current scored signals.")
    parser.add_argument("--signal", action="append", default=None, help="Optional focus signal; may be supplied more than once.")
    args = parser.parse_args()

    if args.describe:
        _print_description()
        return 0

    result = run_conditional_edge_atlas(
        db_path=args.db_path,
        output_dir=args.output_dir,
        summary_path=args.summary_path,
        include_all_current_signals=not args.focus_only,
        focus_signals=tuple(args.signal) if args.signal else DEFAULT_SIGNALS,
        write=args.run,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
