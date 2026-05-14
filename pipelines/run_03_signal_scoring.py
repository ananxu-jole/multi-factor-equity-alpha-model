"""CLI for the 03 multi-horizon signal scoring engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.registry import get_stage  # noqa: E402
from src.scoring.signal_scoring import (  # noqa: E402
    GATE_MIN_ABS_IC_IR,
    GATE_MIN_ABS_MEAN_IC,
    GATE_POSITIVE_IC_RATE_LOWER,
    GATE_POSITIVE_IC_RATE_UPPER,
    GATE_WATCHLIST_ABS_MEAN_IC,
    HORIZONS,
    IC_METHOD,
    MIN_GATE_OBS,
    MIN_SCORE_OBS,
    REQUIRED_INPUT_TABLES,
    SCORING_VERSION,
    run_03_signal_scoring,
)
from src.scoring.signal_scoring_storage import SCORING_TABLES  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("03_signal_scoring")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("scoring_parameters:")
    print(f"  scoring_version: {SCORING_VERSION}")
    print(f"  horizons: {HORIZONS}")
    print(f"  ic_method: {IC_METHOD}")
    print(f"  min_score_obs: {MIN_SCORE_OBS}")
    print(f"  min_gate_obs: {MIN_GATE_OBS}")
    print(f"  min_abs_mean_ic: {GATE_MIN_ABS_MEAN_IC}")
    print(f"  min_abs_ic_ir: {GATE_MIN_ABS_IC_IR}")
    print(f"  positive_ic_rate_upper: {GATE_POSITIVE_IC_RATE_UPPER}")
    print(f"  positive_ic_rate_lower: {GATE_POSITIVE_IC_RATE_LOWER}")
    print(f"  watchlist_abs_mean_ic: {GATE_WATCHLIST_ABS_MEAN_IC}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in SCORING_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 03 signal scoring stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print stage metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--scoring-version",
        default=SCORING_VERSION,
        help="Signal scoring version label to stamp on outputs.",
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
    parser.add_argument(
        "--use-daily-ic-cache",
        action="store_true",
        help="Use cached full-universe daily IC stats for 03 signal scoring.",
    )
    parser.add_argument("--daily-ic-cache-dir", default=None, help="Optional daily IC cache directory.")
    parser.add_argument(
        "--rebuild-daily-ic-cache",
        action="store_true",
        help="Rebuild selected daily IC cache artifacts before running.",
    )
    args = parser.parse_args()

    if args.describe:
        _print_stage_description()
        return 0

    result = run_03_signal_scoring(
        db_path=args.db_path,
        scoring_version=args.scoring_version,
        run_id=args.run_id,
        use_panel_cache=args.use_panel_cache,
        panel_cache_dir=args.panel_cache_dir,
        rebuild_panel_cache=args.rebuild_panel_cache,
        use_daily_ic_cache=args.use_daily_ic_cache,
        daily_ic_cache_dir=args.daily_ic_cache_dir,
        rebuild_daily_ic_cache=args.rebuild_daily_ic_cache,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
