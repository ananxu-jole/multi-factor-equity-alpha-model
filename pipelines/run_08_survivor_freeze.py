"""CLI for the 08 survivor-freeze engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.survivor_registry import (  # noqa: E402
    CLUSTER_MAX_ABS_CORRELATION,
    CORE_MAX_ABS_CORRELATION,
    MIN_CLUSTER_SCORE,
    REQUIRED_INPUT_TABLES,
    TARGET_MAX_CORE_SURVIVORS,
    run_08_survivor_freeze,
)
from src.pipeline.registry import get_stage  # noqa: E402
from src.survivor_storage import SURVIVOR_TABLES  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("08_survivor_freeze")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("engine_thresholds:")
    print(f"  core_max_abs_correlation: {CORE_MAX_ABS_CORRELATION}")
    print(f"  cluster_max_abs_correlation: {CLUSTER_MAX_ABS_CORRELATION}")
    print(f"  target_max_core_survivors: {TARGET_MAX_CORE_SURVIVORS}")
    print(f"  min_cluster_score: {MIN_CLUSTER_SCORE}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in SURVIVOR_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 08 survivor-freeze stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print registry metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--survivor-version",
        default="phase8_cluster_aware_survivor_v5",
        help="Survivor version label to stamp on outputs.",
    )
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id.")
    parser.add_argument("--quiet", action="store_true", help="Suppress engine progress logging.")
    args = parser.parse_args()

    if args.describe:
        _print_stage_description()
        return 0

    result = run_08_survivor_freeze(
        db_path=args.db_path,
        survivor_version=args.survivor_version,
        run_id=args.run_id,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
