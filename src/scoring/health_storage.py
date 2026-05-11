from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SIGNAL_HEALTH_TABLES = {
    "score": ("signal_health_score_current", "signal_health_score_history"),
    "summary": ("signal_health_summary_current", "signal_health_summary_history"),
    "attribution": (
        "signal_health_attribution_current",
        "signal_health_attribution_history",
    ),
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


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _prepare_output(df: pd.DataFrame, run_id: str, health_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["health_version"] = health_version
    return output


def save_signal_health_outputs(
    signal_health_score: pd.DataFrame,
    signal_health_summary: pd.DataFrame,
    signal_health_attribution: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    health_version: str | None = None,
) -> dict[str, Path]:
    """Write signal health score, summary, and attribution outputs to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if health_version is None:
        raise ValueError("health_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "score": _prepare_output(signal_health_score, run_id, health_version),
        "summary": _prepare_output(signal_health_summary, run_id, health_version),
        "attribution": _prepare_output(
            signal_health_attribution if signal_health_attribution is not None else pd.DataFrame(),
            run_id,
            health_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = SIGNAL_HEALTH_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in SIGNAL_HEALTH_TABLES}


__all__ = ["SIGNAL_HEALTH_TABLES", "save_signal_health_outputs"]
