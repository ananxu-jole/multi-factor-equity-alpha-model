from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SIGNAL_DIVERSITY_TABLES = {
    "similarity": (
        "signal_diversity_similarity_current",
        "signal_diversity_similarity_history",
    ),
    "diagnostics": (
        "signal_diversity_diagnostics_current",
        "signal_diversity_diagnostics_history",
    ),
    "selection": (
        "signal_diversity_selection_current",
        "signal_diversity_selection_history",
    ),
    "family_report": (
        "signal_diversity_family_report_current",
        "signal_diversity_family_report_history",
    ),
    "cluster_report": (
        "signal_diversity_cluster_report_current",
        "signal_diversity_cluster_report_history",
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


def _write_sqlite_table(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection, if_exists: str) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _prepare_output(df: pd.DataFrame, run_id: str, diversity_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["diversity_version"] = diversity_version
    return output


def save_signal_diversity_outputs(
    similarity: pd.DataFrame,
    diagnostics: pd.DataFrame,
    selection: pd.DataFrame,
    family_report: pd.DataFrame,
    cluster_report: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    diversity_version: str | None = None,
) -> dict[str, Path]:
    """Write signal diversity artifacts to current/history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if diversity_version is None:
        raise ValueError("diversity_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    outputs = {
        "similarity": _prepare_output(similarity, run_id, diversity_version),
        "diagnostics": _prepare_output(diagnostics, run_id, diversity_version),
        "selection": _prepare_output(selection, run_id, diversity_version),
        "family_report": _prepare_output(family_report, run_id, diversity_version),
        "cluster_report": _prepare_output(
            cluster_report if cluster_report is not None else pd.DataFrame(),
            run_id,
            diversity_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = SIGNAL_DIVERSITY_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in SIGNAL_DIVERSITY_TABLES}


__all__ = ["SIGNAL_DIVERSITY_TABLES", "save_signal_diversity_outputs"]
