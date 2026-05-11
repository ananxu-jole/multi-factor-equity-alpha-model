"""Engine entrypoint for 04B Alpha Walk-Forward Validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.constructed_alpha_wfv import *  # noqa: F401,F403
from src.constructed_alpha_wfv import (
    APPROVED_CONSTRUCTED_ALPHA_WFV,
    WATCHLIST_CONSTRUCTED_ALPHA_WFV,
    apply_constructed_alpha_wfv_gate,
    build_constructed_alpha_wfv_failure_breakdown,
    build_constructed_alpha_wfv_winner_summary,
    load_constructed_alpha_candidates,
    run_constructed_alpha_wfv,
    summarize_constructed_alpha_wfv,
)
from src.constructed_alpha_wfv_storage import save_constructed_alpha_wfv_outputs
from src.db import load_price_table, load_table, table_exists
from src.run_config import get_sqlite_db_path, make_run_id, make_run_timestamp
from src.walkforward import generate_walkforward_windows


HORIZONS = [1, 5, 10, 20]
TRAIN_SIZE = 378
TEST_SIZE = 63
PURGE_SIZE = 20
EMBARGO_SIZE = 5
IC_METHOD = "spearman"

REQUIRED_INPUT_TABLES = [
    "alpha_constructed_candidates_current",
    "alpha_construction_quality_current",
    "clean_close_prices_current",
]


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required 04B input tables are missing from {db_path}: {missing_tables}")


def _load_filtered_alpha_inputs(
    approved_constructed_alphas: pd.DataFrame,
    db_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    alpha_long_all = load_table("alpha_constructed_candidates_current", db_path=db_path)
    alpha_names_found_in_long_table = (
        sorted(alpha_long_all["alpha_name"].dropna().astype(str).unique().tolist())
        if "alpha_name" in alpha_long_all.columns
        else []
    )
    approved_alpha_names = (
        approved_constructed_alphas["alpha_name"].dropna().astype(str).tolist()
        if not approved_constructed_alphas.empty
        else []
    )
    approved_alpha_names_found = [
        name for name in approved_alpha_names if name in alpha_names_found_in_long_table
    ]
    approved_alpha_names_missing = sorted(set(approved_alpha_names).difference(alpha_names_found_in_long_table))

    alpha_long = (
        alpha_long_all.loc[alpha_long_all["alpha_name"].isin(approved_alpha_names_found)].copy()
        if approved_alpha_names_found
        else pd.DataFrame(columns=alpha_long_all.columns)
    )
    if not alpha_long.empty:
        alpha_long["Date"] = pd.to_datetime(alpha_long["Date"], errors="coerce")
        alpha_long["alpha_value"] = pd.to_numeric(alpha_long["alpha_value"], errors="coerce")
    alpha_names_sent_to_wfv = (
        sorted(alpha_long["alpha_name"].dropna().astype(str).unique().tolist())
        if "alpha_name" in alpha_long.columns
        else []
    )

    validation = pd.DataFrame(
        [
            {
                "check": "approved_from_quality",
                "alpha_names": approved_alpha_names,
                "n_alpha_names": len(approved_alpha_names),
            },
            {
                "check": "found_in_alpha_long_table",
                "alpha_names": alpha_names_found_in_long_table,
                "n_alpha_names": len(alpha_names_found_in_long_table),
            },
            {
                "check": "sent_to_wfv",
                "alpha_names": alpha_names_sent_to_wfv,
                "n_alpha_names": len(alpha_names_sent_to_wfv),
            },
            {
                "check": "approved_missing_from_long_table",
                "alpha_names": approved_alpha_names_missing,
                "n_alpha_names": len(approved_alpha_names_missing),
            },
        ]
    )

    if approved_alpha_names_missing:
        raise ValueError(
            "Approved alpha candidates missing from alpha_constructed_candidates_current: "
            f"{approved_alpha_names_missing}"
        )
    if approved_alpha_names and sorted(approved_alpha_names) != alpha_names_sent_to_wfv:
        raise ValueError("Mismatch between approved alpha candidates and alpha names sent to WFV.")

    return alpha_long, validation


def _build_validation_report(
    *,
    approved_constructed_alphas: pd.DataFrame,
    alpha_wfv_gate: pd.DataFrame,
) -> pd.DataFrame:
    valid_statuses = {APPROVED_CONSTRUCTED_ALPHA_WFV, WATCHLIST_CONSTRUCTED_ALPHA_WFV}
    approved_or_watch_count = (
        int(alpha_wfv_gate["status"].isin(valid_statuses).sum())
        if "status" in alpha_wfv_gate.columns
        else 0
    )
    checks = [
        {
            "check_name": "validation_candidates_non_empty",
            "passed": not approved_constructed_alphas.empty,
            "details": f"Candidate rows: {len(approved_constructed_alphas)}",
        },
        {
            "check_name": "wfv_gate_non_empty",
            "passed": not alpha_wfv_gate.empty,
            "details": f"WFV gate rows: {len(alpha_wfv_gate)}",
        },
        {
            "check_name": "approved_or_watchlist_exists",
            "passed": approved_or_watch_count > 0,
            "details": f"Approved/watchlist rows: {approved_or_watch_count}",
        },
        {
            "check_name": "wfv_gate_has_status_column",
            "passed": "status" in alpha_wfv_gate.columns,
            "details": f"Columns: {list(alpha_wfv_gate.columns)}",
        },
    ]
    return pd.DataFrame(checks, columns=["check_name", "passed", "details"])


def _build_summary(
    *,
    run_id: str,
    run_timestamp: str,
    wfv_version: str,
    approved_constructed_alphas: pd.DataFrame,
    alpha_wfv_windows: pd.DataFrame,
    alpha_wfv_results: pd.DataFrame,
    alpha_wfv_summary: pd.DataFrame,
    alpha_wfv_gate: pd.DataFrame,
) -> pd.DataFrame:
    alpha_names = (
        sorted(approved_constructed_alphas["alpha_name"].dropna().astype(str).unique().tolist())
        if "alpha_name" in approved_constructed_alphas.columns
        else []
    )
    status_counts = (
        alpha_wfv_gate["status"].value_counts(dropna=False).to_dict()
        if "status" in alpha_wfv_gate.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "constructed_alpha_wfv_version", "value": wfv_version},
            {"metric": "validation_candidate_count", "value": len(alpha_names)},
            {"metric": "validation_candidate_names", "value": ", ".join(alpha_names)},
            {"metric": "wfv_window_rows", "value": len(alpha_wfv_windows)},
            {"metric": "wfv_result_rows", "value": len(alpha_wfv_results)},
            {"metric": "wfv_summary_rows", "value": len(alpha_wfv_summary)},
            {"metric": "wfv_gate_rows", "value": len(alpha_wfv_gate)},
            {
                "metric": "approved_constructed_alpha_wfv_count",
                "value": int(status_counts.get(APPROVED_CONSTRUCTED_ALPHA_WFV, 0)),
            },
            {
                "metric": "watchlist_constructed_alpha_wfv_count",
                "value": int(status_counts.get(WATCHLIST_CONSTRUCTED_ALPHA_WFV, 0)),
            },
            {"metric": "horizons", "value": ", ".join(str(horizon) for horizon in HORIZONS)},
            {"metric": "train_size", "value": TRAIN_SIZE},
            {"metric": "test_size", "value": TEST_SIZE},
            {"metric": "purge_size", "value": PURGE_SIZE},
            {"metric": "embargo_size", "value": EMBARGO_SIZE},
            {"metric": "ic_method", "value": IC_METHOD},
        ]
    )


def run_04b_alpha_wfv(
    db_path=None,
    wfv_version: str = "phase4b_alpha_wfv_v1",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 04B constructed alpha WFV notebook core logic as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    resolved_run_id = run_id or make_run_id("constructed_alpha_wfv")
    run_timestamp = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    approved_constructed_alphas = load_constructed_alpha_candidates(db_path=resolved_db_path)
    if approved_constructed_alphas.empty:
        raise ValueError("No constructed alpha candidates approved for alpha validation.")

    alpha_long, alpha_candidate_validation = _load_filtered_alpha_inputs(
        approved_constructed_alphas,
        resolved_db_path,
    )
    close_prices = load_price_table("clean_close_prices_current", db_path=resolved_db_path)
    alpha_wfv_windows = generate_walkforward_windows(
        close_prices.index,
        train_size=TRAIN_SIZE,
        test_size=TEST_SIZE,
        purge_size=PURGE_SIZE,
        embargo_size=EMBARGO_SIZE,
    )
    if alpha_wfv_windows.empty:
        raise ValueError("WFV configuration produced no windows.")

    alpha_wfv_results = run_constructed_alpha_wfv(
        approved_alphas=approved_constructed_alphas,
        alpha_long_df=alpha_long,
        close_prices=close_prices,
        windows=alpha_wfv_windows,
        horizons=HORIZONS,
        method=IC_METHOD,
    )
    alpha_wfv_summary = summarize_constructed_alpha_wfv(alpha_wfv_results)
    alpha_wfv_gate = apply_constructed_alpha_wfv_gate(alpha_wfv_summary)
    alpha_wfv_failure_breakdown = build_constructed_alpha_wfv_failure_breakdown(alpha_wfv_gate)
    alpha_wfv_winner_summary = build_constructed_alpha_wfv_winner_summary(alpha_wfv_gate)
    validation_report = _build_validation_report(
        approved_constructed_alphas=approved_constructed_alphas,
        alpha_wfv_gate=alpha_wfv_gate,
    )
    if not validation_report["passed"].all():
        failed = validation_report.loc[
            ~validation_report["passed"],
            ["check_name", "details"],
        ].to_dict("records")
        raise ValueError(f"Constructed alpha WFV validation failed: {failed}")

    summary = _build_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        wfv_version=wfv_version,
        approved_constructed_alphas=approved_constructed_alphas,
        alpha_wfv_windows=alpha_wfv_windows,
        alpha_wfv_results=alpha_wfv_results,
        alpha_wfv_summary=alpha_wfv_summary,
        alpha_wfv_gate=alpha_wfv_gate,
    )

    saved_paths = None
    if write:
        saved_paths = save_constructed_alpha_wfv_outputs(
            windows=alpha_wfv_windows,
            window_results=alpha_wfv_results,
            summary=alpha_wfv_summary,
            gate=alpha_wfv_gate,
            failure_breakdown=alpha_wfv_failure_breakdown,
            winner_summary=alpha_wfv_winner_summary,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            constructed_alpha_wfv_version=wfv_version,
        )

    _log(verbose, f"Loaded 04B alpha WFV inputs from {resolved_db_path}")
    _log(verbose, f"  approved_constructed_alphas: {len(approved_constructed_alphas):,}")
    _log(verbose, f"  alpha_long_filtered: {len(alpha_long):,}")
    _log(verbose, f"  close_prices shape: {close_prices.shape}")
    _log(verbose, "04B alpha WFV output rows")
    for artifact_name, artifact in [
        ("alpha_wfv_windows", alpha_wfv_windows),
        ("alpha_wfv_results", alpha_wfv_results),
        ("alpha_wfv_summary", alpha_wfv_summary),
        ("alpha_wfv_gate", alpha_wfv_gate),
        ("alpha_wfv_failure_breakdown", alpha_wfv_failure_breakdown),
        ("alpha_wfv_winner_summary", alpha_wfv_winner_summary),
        ("validation_report", validation_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    if "status" in alpha_wfv_gate.columns:
        for status, count in alpha_wfv_gate["status"].value_counts(dropna=False).items():
            _log(verbose, f"  status[{status}]: {count}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "alpha_wfv_windows": alpha_wfv_windows,
        "alpha_wfv_results": alpha_wfv_results,
        "alpha_wfv_summary": alpha_wfv_summary,
        "alpha_wfv_gate": alpha_wfv_gate,
        "alpha_wfv_failure_breakdown": alpha_wfv_failure_breakdown,
        "alpha_wfv_winner_summary": alpha_wfv_winner_summary,
        "validation_report": validation_report,
        "summary": summary,
        "approved_constructed_alphas": approved_constructed_alphas,
        "alpha_candidate_validation": alpha_candidate_validation,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
