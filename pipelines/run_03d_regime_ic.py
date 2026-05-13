"""CLI for the 03D regime-conditioned IC engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.registry import get_stage  # noqa: E402
from src.scoring.regime_ic import (  # noqa: E402
    HORIZONS,
    IC_METHOD,
    REGIME_COLUMNS,
    REGIME_IC_VERSION,
    REQUIRED_INPUT_TABLES,
    run_03d_regime_ic,
)
from src.scoring.regime_ic_storage import REGIME_IC_TABLES  # noqa: E402


def _print_stage_description() -> None:
    stage = get_stage("03d_regime_ic")
    print(f"stage_id: {stage.stage_id}")
    print(f"notebook_path: {stage.notebook_path}")
    print(f"current_module: {stage.current_module}")
    print(f"current_function: {stage.current_function}")
    print("regime_ic_parameters:")
    print(f"  regime_ic_version: {REGIME_IC_VERSION}")
    print(f"  horizons: {HORIZONS}")
    print(f"  regime_columns: {REGIME_COLUMNS}")
    print(f"  ic_method: {IC_METHOD}")
    print("expected_input_tables:")
    for table in REQUIRED_INPUT_TABLES:
        print(f"  - {table}")
    print("expected_output_tables:")
    for artifact, (current_table, history_table) in REGIME_IC_TABLES.items():
        print(f"  - {artifact}: {current_table}, {history_table}")
    print(f"required: {stage.required}")
    print(f"diagnostic: {stage.diagnostic}")


def _print_summary(result: dict[str, object]) -> None:
    summary = result["summary"]
    print("summary:")
    for row in summary.to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the 03D regime-conditioned IC stage.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print stage metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run logic and write SQLite current/history outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--regime-ic-version",
        default=REGIME_IC_VERSION,
        help="Regime IC version label to stamp on outputs.",
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

    result = run_03d_regime_ic(
        db_path=args.db_path,
        regime_ic_version=args.regime_ic_version,
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
