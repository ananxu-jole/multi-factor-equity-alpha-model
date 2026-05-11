"""CLI for the 04B constructed alpha WFV engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.constructed_wfv import (  # noqa: E402
    EMBARGO_SIZE,
    HORIZONS,
    IC_METHOD,
    PURGE_SIZE,
    REQUIRED_INPUT_TABLES,
    TEST_SIZE,
    TRAIN_SIZE,
    run_04b_alpha_wfv,
)
from src.constructed_alpha_wfv_storage import CONSTRUCTED_ALPHA_WFV_TABLES  # noqa: E402
from src.pipeline.registry import get_stage  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("04b_alpha_wfv")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("wfv_parameters:")
    print(f"  horizons: {HORIZONS}")
    print(f"  train_size: {TRAIN_SIZE}")
    print(f"  test_size: {TEST_SIZE}")
    print(f"  purge_size: {PURGE_SIZE}")
    print(f"  embargo_size: {EMBARGO_SIZE}")
    print(f"  ic_method: {IC_METHOD}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in CONSTRUCTED_ALPHA_WFV_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 04B constructed alpha WFV stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print stage metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--wfv-version",
        default="phase4b_alpha_wfv_v1",
        help="Constructed alpha WFV version label to stamp on outputs.",
    )
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id.")
    parser.add_argument("--quiet", action="store_true", help="Suppress engine progress logging.")
    args = parser.parse_args()

    if args.describe:
        _print_stage_description()
        return 0

    result = run_04b_alpha_wfv(
        db_path=args.db_path,
        wfv_version=args.wfv_version,
        run_id=args.run_id,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
