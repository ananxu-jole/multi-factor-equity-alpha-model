from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


COMPOSITE_TABLES = {
    "signals": ("composite_signals_current", "composite_signals_history"),
    "metadata": ("composite_metadata_current", "composite_metadata_history"),
    "quality": ("composite_quality_current", "composite_quality_history"),
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


def composite_signals_to_long(
    composite_signals: dict[str, pd.DataFrame],
    run_id: str,
    composite_version: str,
) -> pd.DataFrame:
    """Convert composite panels into SQLite long format."""
    long_frames: list[pd.DataFrame] = []

    for composite_name, composite_df in composite_signals.items():
        panel = composite_df.copy()
        panel.index.name = "Date"
        panel.columns.name = "ticker"
        long_composite = (
            panel.stack(future_stack=True)
            .rename("composite_value")
            .reset_index()
        )
        long_composite["composite_name"] = composite_name
        long_composite["run_id"] = run_id
        long_composite["composite_version"] = composite_version
        long_frames.append(long_composite)

    if not long_frames:
        return pd.DataFrame(
            columns=[
                "Date",
                "ticker",
                "composite_name",
                "composite_value",
                "run_id",
                "composite_version",
            ]
        )

    output = pd.concat(long_frames, ignore_index=True)
    return output[
        ["Date", "ticker", "composite_name", "composite_value", "run_id", "composite_version"]
    ]


def _prepare_table(
    df: pd.DataFrame,
    run_id: str,
    composite_version: str,
) -> pd.DataFrame:
    output = df.copy()
    if "run_id" not in output.columns:
        output["run_id"] = run_id
    if "composite_version" not in output.columns:
        output["composite_version"] = composite_version
    for date_column in ("Date", "first_valid_date", "last_valid_date", "created_timestamp"):
        if date_column in output.columns:
            output[date_column] = pd.to_datetime(output[date_column], errors="coerce").dt.strftime(
                "%Y-%m-%d %H:%M:%S"
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


def save_composite_outputs(
    composite_signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    quality: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    composite_version: str | None = None,
) -> dict[str, Path]:
    """Write composite signal outputs to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if composite_version is None:
        raise ValueError("composite_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "signals": composite_signals_to_long(composite_signals, run_id, composite_version),
        "metadata": _prepare_table(metadata, run_id, composite_version),
        "quality": _prepare_table(quality, run_id, composite_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = COMPOSITE_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in COMPOSITE_TABLES}


__all__ = [
    "COMPOSITE_TABLES",
    "composite_signals_to_long",
    "save_composite_outputs",
]
