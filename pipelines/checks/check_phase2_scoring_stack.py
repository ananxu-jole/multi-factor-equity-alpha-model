"""Validation check for the extracted Phase 2 scoring stack."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.orchestration import SCORING_STAGE_SPECS, run_stage_specs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2 scoring stack checks.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--use-panel-cache", action="store_true", help="Use cached signal panels for 03C, 03D, and 03F.")
    parser.add_argument("--panel-cache-dir", default=None, help="Optional signal panel cache directory.")
    parser.add_argument("--use-daily-ic-cache", action="store_true", help="Use cached full-universe signal daily IC for 03, 03C, and 03D.")
    parser.add_argument("--daily-ic-cache-dir", default=None, help="Optional daily IC cache directory.")
    args = parser.parse_args()
    output = run_stage_specs(
        SCORING_STAGE_SPECS,
        db_path=args.db_path,
        write=False,
        verbose=False,
        stage_kwargs={
            "03_signal_scoring": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
            },
            "03c_signal_decay": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
            },
            "03d_regime_ic": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
                "use_daily_ic_cache": args.use_daily_ic_cache,
                "daily_ic_cache_dir": args.daily_ic_cache_dir,
            },
            "03f_signal_reproducibility": {
                "use_panel_cache": args.use_panel_cache,
                "panel_cache_dir": args.panel_cache_dir,
            },
        },
    )
    return 0 if output["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
