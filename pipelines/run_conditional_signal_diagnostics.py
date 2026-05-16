"""CLI for Batch 3 conditional signal diagnostics research artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scoring.conditional_signal_diagnostics import (  # noqa: E402
    CONDITIONAL_DIAGNOSTICS_VERSION,
    DEFAULT_FOCUS_SIGNALS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SUMMARY_PATH,
    run_conditional_signal_diagnostics,
)


def _print_description() -> None:
    print("stage_id: conditional_signal_diagnostics")
    print(f"diagnostics_version: {CONDITIONAL_DIAGNOSTICS_VERSION}")
    print("default_focus_signals:")
    for signal_name in DEFAULT_FOCUS_SIGNALS:
        print(f"  - {signal_name}")
    print(f"default_output_dir: {DEFAULT_OUTPUT_DIR}")
    print(f"default_summary_path: {DEFAULT_SUMMARY_PATH}")
    print("schema_policy: read existing SQLite outputs; write standalone CSV/Markdown artifacts only")
    print("pipeline_policy: no gates, formulas, WFV logic, schemas, or 04A+ stages are changed")


def _print_summary(result: dict[str, object]) -> None:
    print("summary:")
    for row in result["summary"].to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Batch 3 conditional signal diagnostics.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print diagnostic metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Build diagnostics without writing artifacts.")
    mode.add_argument("--run", action="store_true", help="Build diagnostics and write CSV/Markdown artifacts.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--output-dir", default=None, help="Optional output directory for diagnostic CSV tables.")
    parser.add_argument("--summary-path", default=None, help="Optional markdown summary path.")
    parser.add_argument(
        "--signal",
        action="append",
        default=None,
        help="Optional focus signal. May be supplied more than once; defaults to Batch 1/2 focus list.",
    )
    args = parser.parse_args()

    if args.describe:
        _print_description()
        return 0

    result = run_conditional_signal_diagnostics(
        db_path=args.db_path,
        output_dir=args.output_dir,
        summary_path=args.summary_path,
        focus_signals=tuple(args.signal) if args.signal else DEFAULT_FOCUS_SIGNALS,
        write=args.run,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
