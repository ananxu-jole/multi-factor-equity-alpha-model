"""CLI for research-only active-state WFV diagnostics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scoring.active_state_wfv_diagnostics import (  # noqa: E402
    ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SUMMARY_PATH,
    DEFAULT_SIGNAL,
    DEFAULT_HORIZON,
    run_active_state_wfv_diagnostics,
)


def _print_description() -> None:
    print("stage_id: active_state_wfv_diagnostics")
    print(f"diagnostics_version: {ACTIVE_STATE_WFV_DIAGNOSTICS_VERSION}")
    print(f"default_signal: {DEFAULT_SIGNAL}")
    print(f"default_horizon: {DEFAULT_HORIZON}")
    print(f"default_output_dir: {DEFAULT_OUTPUT_DIR}")
    print(f"default_summary_path: {DEFAULT_SUMMARY_PATH}")
    print("schema_policy: standalone research CSV/Markdown outputs only")
    print("gate_policy: does not change official WFV gates, promotion rules, schemas, or alpha construction")


def _print_summary(result: dict[str, object]) -> None:
    print("summary:")
    for row in result["run_summary"].to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run active-state WFV diagnostics for a conditional signal.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print diagnostic metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Build diagnostics without writing artifacts.")
    mode.add_argument("--run", action="store_true", help="Build diagnostics and write standalone artifacts.")
    parser.add_argument("--signal-name", default=DEFAULT_SIGNAL, help="Conditional signal name to diagnose.")
    parser.add_argument("--horizon", type=int, default=DEFAULT_HORIZON, help="Signal horizon to diagnose.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--output-dir", default=None, help="Optional standalone CSV output directory.")
    parser.add_argument("--summary-path", default=None, help="Optional markdown summary path.")
    args = parser.parse_args()

    if args.describe:
        _print_description()
        return 0

    result = run_active_state_wfv_diagnostics(
        signal_name=args.signal_name,
        horizon=args.horizon,
        db_path=args.db_path,
        output_dir=args.output_dir,
        summary_path=args.summary_path,
        write=args.run,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
