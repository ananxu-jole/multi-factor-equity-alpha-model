from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.alpha_wfv import build_alpha_wfv_failure_breakdown, build_alpha_wfv_winner_summary
from src.run_config import get_sqlite_db_path


ALPHA_SCORING_TABLES = {
    "scores": ("alpha_scores_current", "alpha_scores_history"),
    "scoring_gate": ("alpha_scoring_gate_current", "alpha_scoring_gate_history"),
    "best_horizon": ("alpha_best_horizon_current", "alpha_best_horizon_history"),
    "wfv_windows": ("alpha_wfv_windows_current", "alpha_wfv_windows_history"),
    "wfv_window_results": (
        "alpha_wfv_window_results_current",
        "alpha_wfv_window_results_history",
    ),
    "wfv_summary": ("alpha_wfv_summary_current", "alpha_wfv_summary_history"),
    "wfv_gate": ("alpha_wfv_gate_current", "alpha_wfv_gate_history"),
    "wfv_failure_breakdown": (
        "alpha_wfv_failure_breakdown_current",
        "alpha_wfv_failure_breakdown_history",
    ),
    "wfv_winner_summary": (
        "alpha_wfv_winner_summary_current",
        "alpha_wfv_winner_summary_history",
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


def _with_run_columns(
    df: pd.DataFrame,
    run_id: str,
    alpha_scoring_version: str,
    alpha_wfv_version: str,
) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["alpha_scoring_version"] = alpha_scoring_version
    output["alpha_wfv_version"] = alpha_wfv_version
    return output


def save_alpha_scoring_wfv_outputs(
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
    alpha_scoring_version: str | None = None,
    alpha_wfv_version: str | None = None,
) -> dict[str, Path]:
    """Write alpha scoring and alpha WFV artifacts to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if alpha_scoring_version is None:
        raise ValueError("alpha_scoring_version is required.")
    if alpha_wfv_version is None:
        raise ValueError("alpha_wfv_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_wfv_failure_breakdown = (
        build_alpha_wfv_failure_breakdown(wfv_gate)
        if wfv_failure_breakdown is None
        else wfv_failure_breakdown
    )
    resolved_wfv_winner_summary = (
        build_alpha_wfv_winner_summary(wfv_gate)
        if wfv_winner_summary is None
        else wfv_winner_summary
    )

    outputs = {
        "scores": _with_run_columns(
            scores,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "scoring_gate": _with_run_columns(
            scoring_gate,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "best_horizon": _with_run_columns(
            best_horizon,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_windows": _with_run_columns(
            wfv_windows,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_window_results": _with_run_columns(
            wfv_window_results,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_summary": _with_run_columns(
            wfv_summary,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_gate": _with_run_columns(
            wfv_gate,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_failure_breakdown": _with_run_columns(
            resolved_wfv_failure_breakdown,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
        "wfv_winner_summary": _with_run_columns(
            resolved_wfv_winner_summary,
            run_id=run_id,
            alpha_scoring_version=alpha_scoring_version,
            alpha_wfv_version=alpha_wfv_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = ALPHA_SCORING_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in ALPHA_SCORING_TABLES}


__all__ = [
    "ALPHA_SCORING_TABLES",
    "save_alpha_scoring_wfv_outputs",
]
