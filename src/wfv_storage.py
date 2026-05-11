from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


WFV_TABLES = {
    "windows": ("wfv_windows_current", "wfv_windows_history"),
    "window_results": ("wfv_window_results_current", "wfv_window_results_history"),
    "summary": ("wfv_summary_current", "wfv_summary_history"),
    "gate": ("wfv_gate_current", "wfv_gate_history"),
}

WFV_CANDIDATE_TABLES = {
    "candidates": ("signal_wfv_candidates_current", "signal_wfv_candidates_history"),
}

WFV_DIAGNOSTIC_TABLES = {
    "failure_breakdown": ("wfv_failure_breakdown_current", "wfv_failure_breakdown_history"),
    "window_diagnostics": ("wfv_window_diagnostics_current", "wfv_window_diagnostics_history"),
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


def _with_run_columns(df: pd.DataFrame, run_id: str, wfv_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["wfv_version"] = wfv_version
    return output


def build_wfv_candidates_from_scoring_gate(scoring_gate: pd.DataFrame) -> pd.DataFrame:
    """Build Option B WFV candidates from Notebook 3 scoring gate output."""
    required_columns = {"signal_name", "horizon", "status", "signal_direction"}
    missing_columns = required_columns.difference(scoring_gate.columns)
    if missing_columns:
        raise ValueError(f"scoring_gate is missing required columns: {sorted(missing_columns)}")

    candidates = scoring_gate.loc[
        scoring_gate["status"].isin(["APPROVED_FOR_WFV", "WATCHLIST"])
    ].copy()
    if candidates.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "candidate_tier",
                "signal_direction",
                "signal_family",
                "signal_strength",
                "source_status",
            ]
        )

    candidates["candidate_tier"] = candidates["status"].map(
        {"APPROVED_FOR_WFV": "PRIMARY", "WATCHLIST": "SECONDARY"}
    )
    candidates["source_status"] = candidates["status"]

    columns = [
        "signal_name",
        "horizon",
        "candidate_tier",
        "signal_direction",
        "signal_family",
        "signal_strength",
        "source_status",
    ]
    available_columns = [column for column in columns if column in candidates.columns]
    return (
        candidates[available_columns]
        .drop_duplicates(["signal_name", "horizon"])
        .sort_values(["candidate_tier", "signal_name", "horizon"])
        .reset_index(drop=True)
    )


def load_or_create_wfv_candidates(
    db_path: str | Path | None = None,
    run_id: str | None = None,
    wfv_version: str | None = None,
) -> pd.DataFrame:
    """Load signal_wfv_candidates_current, creating it from signal_scoring_gate_current if absent."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    current_table, history_table = WFV_CANDIDATE_TABLES["candidates"]

    with sqlite3.connect(db_path) as conn:
        if _table_exists(conn, current_table):
            return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(current_table)}", conn)

        if not _table_exists(conn, "signal_scoring_gate_current"):
            raise ValueError(
                "signal_wfv_candidates_current does not exist, and signal_scoring_gate_current "
                "is unavailable for Option B candidate construction."
            )

        scoring_gate = pd.read_sql_query('SELECT * FROM "signal_scoring_gate_current"', conn)
        candidates = build_wfv_candidates_from_scoring_gate(scoring_gate)
        if run_id is not None:
            candidates["run_id"] = run_id
        if wfv_version is not None:
            candidates["wfv_version"] = wfv_version

        _write_sqlite_table(candidates, current_table, conn, if_exists="replace")
        _write_sqlite_table(candidates, history_table, conn, if_exists="append")
        return candidates


def save_wfv_outputs(
    windows: pd.DataFrame,
    window_results: pd.DataFrame,
    summary: pd.DataFrame,
    gate: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    wfv_version: str | None = None,
) -> dict[str, Path]:
    """Write WFV windows, window results, summary, and gate outputs to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if wfv_version is None:
        raise ValueError("wfv_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "windows": _with_run_columns(windows, run_id=run_id, wfv_version=wfv_version),
        "window_results": _with_run_columns(window_results, run_id=run_id, wfv_version=wfv_version),
        "summary": _with_run_columns(summary, run_id=run_id, wfv_version=wfv_version),
        "gate": _with_run_columns(gate, run_id=run_id, wfv_version=wfv_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = WFV_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in WFV_TABLES}


def save_wfv_diagnostics(
    failure_breakdown: pd.DataFrame,
    window_diagnostics: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    wfv_version: str | None = None,
) -> dict[str, Path]:
    """Write WFV diagnostic sidecar outputs to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if wfv_version is None:
        raise ValueError("wfv_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "failure_breakdown": _with_run_columns(
            failure_breakdown,
            run_id=run_id,
            wfv_version=wfv_version,
        ),
        "window_diagnostics": _with_run_columns(
            window_diagnostics,
            run_id=run_id,
            wfv_version=wfv_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = WFV_DIAGNOSTIC_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in WFV_DIAGNOSTIC_TABLES}


__all__ = [
    "WFV_CANDIDATE_TABLES",
    "WFV_DIAGNOSTIC_TABLES",
    "WFV_TABLES",
    "build_wfv_candidates_from_scoring_gate",
    "load_or_create_wfv_candidates",
    "save_wfv_diagnostics",
    "save_wfv_outputs",
]
