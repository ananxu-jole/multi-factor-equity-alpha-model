from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SIGNAL_DECAY_TABLES = {
    "curve": ("signal_decay_curve_current", "signal_decay_curve_history"),
    "summary": ("signal_decay_summary_current", "signal_decay_summary_history"),
}


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    query = """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
    """
    return conn.execute(query, (table_name,)).fetchone() is not None


def _sqlite_type_for_series(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    return "TEXT"


def _ensure_sqlite_columns(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
) -> None:
    existing_columns = {
        row[1]
        for row in conn.execute(f"PRAGMA table_info({_quote_identifier(table_name)})").fetchall()
    }
    missing_columns = [column for column in df.columns if column not in existing_columns]
    for column in missing_columns:
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(column)} {_sqlite_type_for_series(df[column])}"
        )


def _prepare_output(
    df: pd.DataFrame,
    run_id: str,
    decay_version: str,
) -> pd.DataFrame:
    output = df.copy()
    for date_column in ("Date",):
        if date_column in output.columns:
            output[date_column] = pd.to_datetime(output[date_column], errors="coerce").dt.strftime(
                "%Y-%m-%d"
            )
    output["run_id"] = run_id
    output["decay_version"] = decay_version
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


def save_signal_decay_outputs(
    decay_curve: pd.DataFrame,
    decay_summary: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    decay_version: str | None = None,
) -> dict[str, Path]:
    """Write signal decay curve and summary outputs to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if decay_version is None:
        raise ValueError("decay_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "curve": _prepare_output(decay_curve, run_id, decay_version),
        "summary": _prepare_output(decay_summary, run_id, decay_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = SIGNAL_DECAY_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in SIGNAL_DECAY_TABLES}


__all__ = [
    "SIGNAL_DECAY_TABLES",
    "save_signal_decay_outputs",
]
