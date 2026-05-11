from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SURVIVOR_TABLES = {
    "registry": ("survivor_alpha_registry_current", "survivor_alpha_registry_history"),
    "pre_ml_inputs": ("pre_ml_alpha_inputs_current", "pre_ml_alpha_inputs_history"),
    "correlation": (
        "survivor_alpha_correlation_current",
        "survivor_alpha_correlation_history",
    ),
    "cluster_summary": (
        "survivor_cluster_summary_current",
        "survivor_cluster_summary_history",
    ),
    "freeze_report": ("survivor_freeze_report_current", "survivor_freeze_report_history"),
    "validation_report": (
        "survivor_validation_report_current",
        "survivor_validation_report_history",
    ),
    "lineage_report": ("survivor_lineage_report_current", "survivor_lineage_report_history"),
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


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _with_freeze_columns(df: pd.DataFrame, run_id: str, survivor_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["survivor_version"] = survivor_version
    return output


def save_survivor_outputs(
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    survivor_freeze_report: pd.DataFrame,
    survivor_validation_report: pd.DataFrame,
    survivor_lineage_report: pd.DataFrame,
    survivor_alpha_correlation: pd.DataFrame | None = None,
    survivor_cluster_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    survivor_version: str | None = None,
) -> dict[str, Path]:
    """Write survivor freeze outputs to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if survivor_version is None:
        raise ValueError("survivor_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "registry": _with_freeze_columns(
            survivor_registry,
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "pre_ml_inputs": _with_freeze_columns(
            pre_ml_alpha_inputs,
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "correlation": _with_freeze_columns(
            survivor_alpha_correlation if survivor_alpha_correlation is not None else pd.DataFrame(),
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "cluster_summary": _with_freeze_columns(
            survivor_cluster_summary if survivor_cluster_summary is not None else pd.DataFrame(),
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "freeze_report": _with_freeze_columns(
            survivor_freeze_report,
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "validation_report": _with_freeze_columns(
            survivor_validation_report,
            run_id=run_id,
            survivor_version=survivor_version,
        ),
        "lineage_report": _with_freeze_columns(
            survivor_lineage_report,
            run_id=run_id,
            survivor_version=survivor_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = SURVIVOR_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in SURVIVOR_TABLES}


__all__ = [
    "SURVIVOR_TABLES",
    "save_survivor_outputs",
]
