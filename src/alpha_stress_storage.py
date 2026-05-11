from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.alpha_stress import (
    apply_alpha_stress_gate,
    build_alpha_stress_audit_summary,
    build_alpha_stress_case_matrix,
    build_alpha_stress_degradation_matrix,
    summarize_alpha_stress_results,
)
from src.run_config import get_sqlite_db_path


ALPHA_STRESS_TABLES = {
    "results": ("alpha_stress_results_current", "alpha_stress_results_history"),
    "summary": ("alpha_stress_summary_current", "alpha_stress_summary_history"),
    "gate": ("alpha_stress_gate_current", "alpha_stress_gate_history"),
    "case_matrix": ("alpha_stress_case_matrix_current", "alpha_stress_case_matrix_history"),
    "degradation_matrix": (
        "alpha_stress_degradation_matrix_current",
        "alpha_stress_degradation_matrix_history",
    ),
    "audit_summary": ("alpha_stress_audit_summary_current", "alpha_stress_audit_summary_history"),
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


def _with_run_columns(df: pd.DataFrame, run_id: str, stress_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["stress_version"] = stress_version
    return output


def save_alpha_stress_outputs(
    stress_results: pd.DataFrame,
    stress_summary: pd.DataFrame | None = None,
    stress_gate: pd.DataFrame | None = None,
    stress_case_matrix: pd.DataFrame | None = None,
    stress_degradation_matrix: pd.DataFrame | None = None,
    stress_audit_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    stress_version: str | None = None,
) -> dict[str, Path]:
    """Write alpha stress results, gate decisions, and audit diagnostics to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if stress_version is None:
        raise ValueError("stress_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_summary = (
        summarize_alpha_stress_results(stress_results) if stress_summary is None else stress_summary
    )
    resolved_gate = apply_alpha_stress_gate(resolved_summary) if stress_gate is None else stress_gate
    resolved_case_matrix = (
        build_alpha_stress_case_matrix(stress_results)
        if stress_case_matrix is None
        else stress_case_matrix
    )
    resolved_degradation_matrix = (
        build_alpha_stress_degradation_matrix(stress_results)
        if stress_degradation_matrix is None
        else stress_degradation_matrix
    )
    resolved_audit_summary = (
        build_alpha_stress_audit_summary(stress_results, resolved_gate)
        if stress_audit_summary is None
        else stress_audit_summary
    )

    outputs = {
        "results": _with_run_columns(stress_results, run_id=run_id, stress_version=stress_version),
        "summary": _with_run_columns(resolved_summary, run_id=run_id, stress_version=stress_version),
        "gate": _with_run_columns(resolved_gate, run_id=run_id, stress_version=stress_version),
        "case_matrix": _with_run_columns(
            resolved_case_matrix,
            run_id=run_id,
            stress_version=stress_version,
        ),
        "degradation_matrix": _with_run_columns(
            resolved_degradation_matrix,
            run_id=run_id,
            stress_version=stress_version,
        ),
        "audit_summary": _with_run_columns(
            resolved_audit_summary,
            run_id=run_id,
            stress_version=stress_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = ALPHA_STRESS_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in ALPHA_STRESS_TABLES}


__all__ = [
    "ALPHA_STRESS_TABLES",
    "save_alpha_stress_outputs",
]
