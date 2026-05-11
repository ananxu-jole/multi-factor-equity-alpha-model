from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.alpha_wfv import build_alpha_wfv_failure_breakdown, build_alpha_wfv_winner_summary
from src.run_config import get_sqlite_db_path


REGIME_CONTEXT_ALPHA_VALIDATION_TABLES = {
    "scores": (
        "regime_context_alpha_scores_current",
        "regime_context_alpha_scores_history",
    ),
    "scoring_gate": (
        "regime_context_alpha_scoring_gate_current",
        "regime_context_alpha_scoring_gate_history",
    ),
    "best_horizon": (
        "regime_context_alpha_best_horizon_current",
        "regime_context_alpha_best_horizon_history",
    ),
    "wfv_windows": (
        "regime_context_alpha_wfv_windows_current",
        "regime_context_alpha_wfv_windows_history",
    ),
    "wfv_window_results": (
        "regime_context_alpha_wfv_window_results_current",
        "regime_context_alpha_wfv_window_results_history",
    ),
    "wfv_summary": (
        "regime_context_alpha_wfv_summary_current",
        "regime_context_alpha_wfv_summary_history",
    ),
    "wfv_gate": (
        "regime_context_alpha_wfv_gate_current",
        "regime_context_alpha_wfv_gate_history",
    ),
    "wfv_failure_breakdown": (
        "regime_context_alpha_wfv_failure_breakdown_current",
        "regime_context_alpha_wfv_failure_breakdown_history",
    ),
    "wfv_winner_summary": (
        "regime_context_alpha_wfv_winner_summary_current",
        "regime_context_alpha_wfv_winner_summary_history",
    ),
}

REGIME_OVERLAY_DIAGNOSTIC_DECISION_TABLES = (
    "regime_overlay_diagnostic_decision_current",
    "regime_overlay_diagnostic_decision_history",
)


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    return (
        conn.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            LIMIT 1
            """,
            (table_name,),
        ).fetchone()
        is not None
    )


def _sqlite_type_for_series(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    return "TEXT"


def _ensure_sqlite_columns(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection) -> None:
    existing_columns = {
        row[1]
        for row in conn.execute(f"PRAGMA table_info({_quote_identifier(table_name)})").fetchall()
    }
    for column in [column for column in df.columns if column not in existing_columns]:
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(column)} {_sqlite_type_for_series(df[column])}"
        )


def _write_sqlite_table(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection, if_exists: str) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _with_run_columns(
    df: pd.DataFrame,
    run_id: str,
    scoring_version: str,
    wfv_version: str,
) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["regime_context_alpha_scoring_version"] = scoring_version
    output["regime_context_alpha_wfv_version"] = wfv_version
    for date_column in ("train_start", "train_end", "test_start", "test_end", "embargo_start", "embargo_end"):
        if date_column in output.columns:
            output[date_column] = pd.to_datetime(output[date_column], errors="coerce").dt.strftime("%Y-%m-%d")
    return output


def save_regime_context_alpha_validation_outputs(
    scores: pd.DataFrame,
    scoring_gate: pd.DataFrame,
    best_horizon: pd.DataFrame,
    wfv_windows: pd.DataFrame,
    wfv_window_results: pd.DataFrame,
    wfv_summary: pd.DataFrame,
    wfv_gate: pd.DataFrame,
    wfv_failure_breakdown: pd.DataFrame | None = None,
    wfv_winner_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    scoring_version: str | None = None,
    wfv_version: str | None = None,
) -> dict[str, Path]:
    """Write regime-context alpha scoring/WFV artifacts to separate SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if scoring_version is None:
        raise ValueError("scoring_version is required.")
    if wfv_version is None:
        raise ValueError("wfv_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_failure_breakdown = (
        build_alpha_wfv_failure_breakdown(wfv_gate)
        if wfv_failure_breakdown is None
        else wfv_failure_breakdown
    )
    resolved_winner_summary = (
        build_alpha_wfv_winner_summary(wfv_gate)
        if wfv_winner_summary is None
        else wfv_winner_summary
    )
    outputs = {
        "scores": scores,
        "scoring_gate": scoring_gate,
        "best_horizon": best_horizon,
        "wfv_windows": wfv_windows,
        "wfv_window_results": wfv_window_results,
        "wfv_summary": wfv_summary,
        "wfv_gate": wfv_gate,
        "wfv_failure_breakdown": resolved_failure_breakdown,
        "wfv_winner_summary": resolved_winner_summary,
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = REGIME_CONTEXT_ALPHA_VALIDATION_TABLES[artifact]
            prepared = _with_run_columns(
                output,
                run_id=run_id,
                scoring_version=scoring_version,
                wfv_version=wfv_version,
            )
            _write_sqlite_table(prepared, current_table, conn, if_exists="replace")
            _write_sqlite_table(prepared, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in REGIME_CONTEXT_ALPHA_VALIDATION_TABLES}


def save_regime_overlay_diagnostic_decision(
    decision: pd.DataFrame,
    db_path: str | Path | None = None,
) -> dict[str, Path]:
    """Write the diagnostic-only regime overlay decision table."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    current_table, history_table = REGIME_OVERLAY_DIAGNOSTIC_DECISION_TABLES

    with sqlite3.connect(db_path) as conn:
        _write_sqlite_table(decision, current_table, conn, if_exists="replace")
        _write_sqlite_table(decision, history_table, conn, if_exists="append")

    return {"diagnostic_decision": db_path}


__all__ = [
    "REGIME_CONTEXT_ALPHA_VALIDATION_TABLES",
    "REGIME_OVERLAY_DIAGNOSTIC_DECISION_TABLES",
    "save_regime_overlay_diagnostic_decision",
    "save_regime_context_alpha_validation_outputs",
]
