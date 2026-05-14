"""Run the extracted Phase 2 scoring stack."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.orchestration import SCORING_STAGE_SPECS, describe_pipeline, run_stage_specs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run or describe the Phase 2 scoring stack.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print pipeline stage metadata.")
    mode.add_argument("--dry-run", action="store_true", help="Run all stages without writing outputs.")
    mode.add_argument("--run", action="store_true", help="Run all stages and write outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--quiet", action="store_true", help="Suppress stage progress logging.")
    parser.add_argument("--use-panel-cache", action="store_true", help="Use cached signal panels for 03C, 03D, and 03F.")
    parser.add_argument("--panel-cache-dir", default=None, help="Optional signal panel cache directory.")
    parser.add_argument("--rebuild-panel-cache", action="store_true", help="Rebuild selected panel cache artifacts before running.")
    parser.add_argument("--use-daily-ic-cache", action="store_true", help="Use cached full-universe signal daily IC for 03, 03C, and 03D.")
    parser.add_argument("--daily-ic-cache-dir", default=None, help="Optional daily IC cache directory.")
    parser.add_argument("--rebuild-daily-ic-cache", action="store_true", help="Rebuild selected daily IC cache artifacts before running.")
    args = parser.parse_args()

    if args.describe:
        describe_pipeline("phase2_scoring_stack", SCORING_STAGE_SPECS)
        return 0

    output = run_stage_specs(
        SCORING_STAGE_SPECS,
        db_path=args.db_path,
        write=args.run,
        verbose=not args.quiet,
        stage_kwargs={
            "03_signal_scoring": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "rebuild_panel_cache": args.rebuild_panel_cache,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
                "rebuild_daily_ic_cache": args.rebuild_daily_ic_cache,
            },
            "03c_signal_decay": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "rebuild_panel_cache": args.rebuild_panel_cache,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
                "rebuild_daily_ic_cache": args.rebuild_daily_ic_cache,
            },
            "03d_regime_ic": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "rebuild_panel_cache": args.rebuild_panel_cache,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
                "rebuild_daily_ic_cache": args.rebuild_daily_ic_cache,
            },
            "03f_signal_reproducibility": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "rebuild_panel_cache": args.rebuild_panel_cache,
            },
        },
    )
    return 0 if output["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
