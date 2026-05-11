from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


CONSTRUCTED_ALPHA_WFV_TABLES = {
    "windows": (
        "constructed_alpha_wfv_windows_current",
        "constructed_alpha_wfv_windows_history",
    ),
    "window_results": (
        "constructed_alpha_wfv_window_results_current",
        "constructed_alpha_wfv_window_results_history",
    ),
    "summary": (
        "constructed_alpha_wfv_summary_current",
        "constructed_alpha_wfv_summary_history",
    ),
    "gate": (
        "constructed_alpha_wfv_gate_current",
        "constructed_alpha_wfv_gate_history",
    ),
    "failure_breakdown": (
        "constructed_alpha_wfv_failure_breakdown_current",
        "constructed_alpha_wfv_failure_breakdown_history",
    ),
    "winner_summary": (
        "constructed_alpha_wfv_winner_summary_current",
        "constructed_alpha_wfv_winner_summary_history",
    ),
}


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


def _prepare_table(df: pd.DataFrame, run_id: str, constructed_alpha_wfv_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["constructed_alpha_wfv_version"] = constructed_alpha_wfv_version
    for date_column in ("train_start", "train_end", "test_start", "test_end", "embargo_start", "embargo_end"):
        if date_column in output.columns:
            output[date_column] = pd.to_datetime(output[date_column], errors="coerce").dt.strftime(
                "%Y-%m-%d"
            )
    return output


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def save_constructed_alpha_wfv_outputs(
    windows: pd.DataFrame,
    window_results: pd.DataFrame,
    summary: pd.DataFrame,
    gate: pd.DataFrame,
    failure_breakdown: pd.DataFrame,
    winner_summary: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    constructed_alpha_wfv_version: str | None = None,
) -> dict[str, Path]:
    """Write constructed alpha WFV outputs to dedicated current/history tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if constructed_alpha_wfv_version is None:
        raise ValueError("constructed_alpha_wfv_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    outputs = {
        "windows": _prepare_table(windows, run_id, constructed_alpha_wfv_version),
        "window_results": _prepare_table(window_results, run_id, constructed_alpha_wfv_version),
        "summary": _prepare_table(summary, run_id, constructed_alpha_wfv_version),
        "gate": _prepare_table(gate, run_id, constructed_alpha_wfv_version),
        "failure_breakdown": _prepare_table(failure_breakdown, run_id, constructed_alpha_wfv_version),
        "winner_summary": _prepare_table(winner_summary, run_id, constructed_alpha_wfv_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = CONSTRUCTED_ALPHA_WFV_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in CONSTRUCTED_ALPHA_WFV_TABLES}


__all__ = ["CONSTRUCTED_ALPHA_WFV_TABLES", "save_constructed_alpha_wfv_outputs"]
