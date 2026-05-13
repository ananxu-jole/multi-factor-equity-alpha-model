"""CLI for the 03F signal reproducibility engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.registry import get_stage  # noqa: E402
from src.scoring.reproducibility import (  # noqa: E402
    IC_METHOD,
    INCLUDE_ORTHOGONAL_WATCHLIST,
    INCLUDE_WATCHLIST,
    ORTHOGONAL_WATCHLIST_MIN_HEALTH_SCORE,
    ORTHOGONAL_WATCHLIST_VERSION,
    PASS_MIN_EFFECTIVE_IC,
    PASS_MIN_OBS,
    PASS_MIN_POSITIVE_RATE,
    REPRODUCIBILITY_VERSION,
    REQUIRED_INPUT_TABLES,
    run_03f_signal_reproducibility,
)
from src.scoring.reproducibility_storage import SIGNAL_REPRODUCIBILITY_TABLES  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("03f_signal_reproducibility")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("reproducibility_parameters:")
    print(f"  method: {IC_METHOD}")
    print(f"  include_watchlist: {INCLUDE_WATCHLIST}")
    print(f"  include_orthogonal_watchlist: {INCLUDE_ORTHOGONAL_WATCHLIST}")
    print(f"  orthogonal_watchlist_min_health_score: {ORTHOGONAL_WATCHLIST_MIN_HEALTH_SCORE}")
    print(f"  orthogonal_watchlist_version: {ORTHOGONAL_WATCHLIST_VERSION}")
    print(f"  pass_min_obs: {PASS_MIN_OBS}")
    print(f"  pass_min_effective_ic: {PASS_MIN_EFFECTIVE_IC}")
    print(f"  pass_min_positive_rate: {PASS_MIN_POSITIVE_RATE}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in SIGNAL_REPRODUCIBILITY_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 03F signal reproducibility stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print stage metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--reproducibility-version",
        default=REPRODUCIBILITY_VERSION,
        help="Signal reproducibility version label to stamp on outputs.",
    )
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id.")
    parser.add_argument("--quiet", action="store_true", help="Suppress engine progress logging.")
    parser.add_argument(
        "--use-panel-cache",
        action="store_true",
        help="Load cached Parquet signal panels instead of rebuilding panels from SQLite long rows.",
    )
    parser.add_argument("--panel-cache-dir", default=None, help="Optional signal panel cache directory.")
    parser.add_argument(
        "--rebuild-panel-cache",
        action="store_true",
        help="Rebuild selected signal panel cache artifacts before running.",
    )
    args = parser.parse_args()

    if args.describe:
        _print_stage_description()
        return 0

    result = run_03f_signal_reproducibility(
        db_path=args.db_path,
        reproducibility_version=args.reproducibility_version,
        run_id=args.run_id,
        use_panel_cache=args.use_panel_cache,
        panel_cache_dir=args.panel_cache_dir,
        rebuild_panel_cache=args.rebuild_panel_cache,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
