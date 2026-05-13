"""Run the full extracted research platform."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.orchestration import FULL_STAGE_SPECS, describe_pipeline, run_stage_specs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the full research platform.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print pipeline stage metadata.")
    mode.add_argument("--dry-run", action="store_true", help="Run all stages without writing outputs.")
    mode.add_argument("--run", action="store_true", help="Run all stages and write outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--quiet", action="store_true", help="Suppress stage progress logging.")
    args = parser.parse_args()

    if args.describe:
        describe_pipeline("full_research_platform", FULL_STAGE_SPECS)
        return 0

    output = run_stage_specs(
        FULL_STAGE_SPECS,
        db_path=args.db_path,
        write=args.run,
        verbose=not args.quiet,
    )
    return 0 if output["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
