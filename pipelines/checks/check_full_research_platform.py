"""Validation check for the full extracted research platform."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.orchestration import FULL_STAGE_SPECS, run_stage_specs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run full research platform checks.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    args = parser.parse_args()
    output = run_stage_specs(FULL_STAGE_SPECS, db_path=args.db_path, write=False, verbose=False)
    return 0 if output["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
