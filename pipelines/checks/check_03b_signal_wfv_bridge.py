"""Sanity checks for the controlled 03B signal WFV bridge."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.run_03b_signal_wfv_bridge import (  # noqa: E402
    DIAGNOSTIC_CANDIDATES,
    PRIMARY_CANDIDATES,
    run_03b_signal_wfv_bridge,
)


def _record(check_name: str, passed: bool, details: str = "") -> dict[str, object]:
    return {"check_name": check_name, "passed": bool(passed), "details": details}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run dry-run checks for the 03B signal WFV bridge.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--include-diagnostics",
        action="store_true",
        help="Include diagnostic candidates in the dry-run check.",
    )
    args = parser.parse_args()

    result = run_03b_signal_wfv_bridge(
        db_path=args.db_path,
        include_diagnostics=args.include_diagnostics,
        write=False,
        verbose=False,
    )
    candidates = result["candidates"]
    windows = result["windows"]
    window_results = result["window_results"]
    gate = result["gate"]

    expected_names = set(PRIMARY_CANDIDATES)
    if args.include_diagnostics:
        expected_names.update(DIAGNOSTIC_CANDIDATES)
    candidate_names = set(candidates["signal_name"].astype(str)) if not candidates.empty else set()
    allowed_tiers = {"EXPANSION_BRIDGE_PRIMARY", "EXPANSION_BRIDGE_DIAGNOSTIC"}

    records = [
        _record("candidate_rows_non_empty", not candidates.empty, f"rows={len(candidates)}"),
        _record("only_allowlisted_names", candidate_names.issubset(expected_names), ",".join(sorted(candidate_names))),
        _record(
            "primary_candidates_present",
            set(PRIMARY_CANDIDATES).issubset(candidate_names),
            ",".join(sorted(candidate_names)),
        ),
        _record(
            "uses_best_horizon_once",
            candidates.empty or not candidates.duplicated(["signal_name", "horizon"]).any(),
            f"rows={len(candidates)}",
        ),
        _record(
            "bridge_metadata_present",
            {"candidate_tier", "bridge_source", "bridge_reason"}.issubset(candidates.columns),
            ",".join(candidates.columns),
        ),
        _record(
            "candidate_tiers_controlled",
            candidates.empty or set(candidates["candidate_tier"].dropna().astype(str)).issubset(allowed_tiers),
            ",".join(sorted(set(candidates.get("candidate_tier", pd.Series(dtype=str)).dropna().astype(str)))),
        ),
        _record("windows_non_empty", not windows.empty, f"rows={len(windows)}"),
        _record("window_results_match_candidates", len(window_results) == len(candidates) * len(windows), f"rows={len(window_results)}"),
        _record("gate_rows_match_candidates", len(gate) == len(candidates), f"rows={len(gate)}"),
        _record(
            "gate_status_known",
            gate.empty or set(gate["status"].dropna().astype(str)).issubset({"APPROVED_WFV", "WATCHLIST_WFV", "REJECTED_WFV"}),
            ",".join(sorted(set(gate.get("status", pd.Series(dtype=str)).dropna().astype(str)))),
        ),
    ]

    comparison = pd.DataFrame(records)
    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
