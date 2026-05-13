from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path
from src.scoring.signal_scoring import (
    build_best_horizon_summary,
    build_scoring_family_summary,
    build_signal_score_summary,
)


SCORING_TABLES = {
    "scores": ("signal_scores_current", "signal_scores_history"),
    "summary": ("signal_score_summary_current", "signal_score_summary_history"),
    "gate": ("signal_scoring_gate_current", "signal_scoring_gate_history"),
    "best_horizon": ("signal_best_horizon_current", "signal_best_horizon_history"),
    "family_summary": (
        "signal_scoring_family_summary_current",
        "signal_scoring_family_summary_history",
    ),
}


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


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
        sqlite_type = _sqlite_type_for_series(df[column])
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(column)} {sqlite_type}"
        )


def _with_run_columns(df: pd.DataFrame, run_id: str, scoring_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["scoring_version"] = scoring_version
    return output


def save_signal_scoring_outputs(
    scores: pd.DataFrame,
    gate: pd.DataFrame,
    summary: pd.DataFrame | None = None,
    best_horizon: pd.DataFrame | None = None,
    family_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    scoring_version: str | None = None,
) -> dict[str, Path]:
    """Write signal scoring outputs to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if scoring_version is None:
        raise ValueError("scoring_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_summary = build_signal_score_summary(scores) if summary is None else summary
    resolved_best_horizon = (
        build_best_horizon_summary(scores) if best_horizon is None else best_horizon
    )
    resolved_family_summary = (
        build_scoring_family_summary(scores) if family_summary is None else family_summary
    )

    scores_out = _with_run_columns(scores, run_id=run_id, scoring_version=scoring_version)
    summary_out = _with_run_columns(resolved_summary, run_id=run_id, scoring_version=scoring_version)
    gate_out = _with_run_columns(gate, run_id=run_id, scoring_version=scoring_version)
    best_horizon_out = _with_run_columns(
        resolved_best_horizon,
        run_id=run_id,
        scoring_version=scoring_version,
    )
    family_summary_out = _with_run_columns(
        resolved_family_summary,
        run_id=run_id,
        scoring_version=scoring_version,
    )

    with sqlite3.connect(db_path) as conn:
        _write_sqlite_table(scores_out, SCORING_TABLES["scores"][0], conn, if_exists="replace")
        _write_sqlite_table(scores_out, SCORING_TABLES["scores"][1], conn, if_exists="append")
        _write_sqlite_table(summary_out, SCORING_TABLES["summary"][0], conn, if_exists="replace")
        _write_sqlite_table(summary_out, SCORING_TABLES["summary"][1], conn, if_exists="append")
        _write_sqlite_table(gate_out, SCORING_TABLES["gate"][0], conn, if_exists="replace")
        _write_sqlite_table(gate_out, SCORING_TABLES["gate"][1], conn, if_exists="append")
        _write_sqlite_table(
            best_horizon_out,
            SCORING_TABLES["best_horizon"][0],
            conn,
            if_exists="replace",
        )
        _write_sqlite_table(
            best_horizon_out,
            SCORING_TABLES["best_horizon"][1],
            conn,
            if_exists="append",
        )
        _write_sqlite_table(
            family_summary_out,
            SCORING_TABLES["family_summary"][0],
            conn,
            if_exists="replace",
        )
        _write_sqlite_table(
            family_summary_out,
            SCORING_TABLES["family_summary"][1],
            conn,
            if_exists="append",
        )

    return {name: db_path for name in SCORING_TABLES}


def save_scoring_outputs(*args, **kwargs) -> dict[str, Path]:
    """Compatibility wrapper for the shorter Phase 2 scoring storage name."""
    return save_signal_scoring_outputs(*args, **kwargs)


__all__ = [
    "SCORING_TABLES",
    "save_scoring_outputs",
    "save_signal_scoring_outputs",
]
