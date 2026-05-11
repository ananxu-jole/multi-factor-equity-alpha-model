"""CLI for the 07 alpha stress engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.stress import (  # noqa: E402
    COST_BPS_LIST,
    DEGRADATION_MULTIPLIERS,
    EXECUTION_DELAYS,
    PRIORITY_ALPHAS,
    REQUIRED_INPUT_TABLES,
    run_07_alpha_stress,
)
from src.alpha_stress_storage import ALPHA_STRESS_TABLES  # noqa: E402
from src.pipeline.registry import get_stage  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("07_alpha_stress")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("stress_parameters:")
    print(f"  cost_bps_list: {COST_BPS_LIST}")
    print(f"  execution_delays: {EXECUTION_DELAYS}")
    print(f"  degradation_multipliers: {DEGRADATION_MULTIPLIERS}")
    print(f"  priority_alphas: {', '.join(PRIORITY_ALPHAS)}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in ALPHA_STRESS_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 07 alpha stress stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print stage metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--stress-version",
        default="phase7_alpha_stress_v1",
        help="Stress version label to stamp on outputs.",
    )
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id.")
    parser.add_argument("--quiet", action="store_true", help="Suppress engine progress logging.")
    args = parser.parse_args()

    if args.describe:
        _print_stage_description()
        return 0

    result = run_07_alpha_stress(
        db_path=args.db_path,
        stress_version=args.stress_version,
        run_id=args.run_id,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
