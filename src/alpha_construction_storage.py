from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


ALPHA_CONSTRUCTION_TABLES = {
    "candidates": (
        "alpha_constructed_candidates_current",
        "alpha_constructed_candidates_history",
    ),
    "metadata": (
        "alpha_construction_metadata_current",
        "alpha_construction_metadata_history",
    ),
    "quality": (
        "alpha_construction_quality_current",
        "alpha_construction_quality_history",
    ),
    "diagnostics": (
        "alpha_construction_diagnostics_current",
        "alpha_construction_diagnostics_history",
    ),
    "correlation": (
        "alpha_construction_correlation_current",
        "alpha_construction_correlation_history",
    ),
    "signal_pool": (
        "alpha_signal_pool_current",
        "alpha_signal_pool_history",
    ),
    "dynamic_weight_audit": (
        "alpha_dynamic_weight_audit_current",
        "alpha_dynamic_weight_audit_history",
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


def alpha_candidates_to_long(
    alpha_candidates: dict[str, pd.DataFrame],
    run_id: str,
    alpha_construction_version: str,
) -> pd.DataFrame:
    long_frames: list[pd.DataFrame] = []
    for alpha_name, panel in alpha_candidates.items():
        alpha = panel.copy()
        alpha.index.name = "Date"
        alpha.columns.name = "ticker"
        long_alpha = alpha.stack(future_stack=True).rename("alpha_value").reset_index()
        long_alpha["alpha_name"] = alpha_name
        long_alpha["run_id"] = run_id
        long_alpha["alpha_construction_version"] = alpha_construction_version
        long_frames.append(long_alpha)

    if not long_frames:
        return pd.DataFrame(
            columns=[
                "Date",
                "ticker",
                "alpha_name",
                "alpha_value",
                "run_id",
                "alpha_construction_version",
            ]
        )
    output = pd.concat(long_frames, ignore_index=True)
    return output[
        ["Date", "ticker", "alpha_name", "alpha_value", "run_id", "alpha_construction_version"]
    ]


def _prepare_table(df: pd.DataFrame, run_id: str, alpha_construction_version: str) -> pd.DataFrame:
    output = df.copy()
    if "run_id" not in output.columns:
        output["run_id"] = run_id
    if "alpha_construction_version" not in output.columns:
        output["alpha_construction_version"] = alpha_construction_version
    for date_column in ("Date", "first_valid_date", "last_valid_date"):
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


def save_alpha_construction_outputs(
    alpha_candidates: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    quality: pd.DataFrame,
    diagnostics: pd.DataFrame | None = None,
    correlation: pd.DataFrame | None = None,
    signal_pool: pd.DataFrame | None = None,
    dynamic_weight_audit: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    alpha_construction_version: str | None = None,
) -> dict[str, Path]:
    """Write Phase 4A constructed alpha outputs to current/history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if alpha_construction_version is None:
        raise ValueError("alpha_construction_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "candidates": _prepare_table(
            alpha_candidates_to_long(alpha_candidates, run_id, alpha_construction_version),
            run_id,
            alpha_construction_version,
        ),
        "metadata": _prepare_table(metadata, run_id, alpha_construction_version),
        "quality": _prepare_table(quality, run_id, alpha_construction_version),
        "diagnostics": _prepare_table(
            diagnostics if diagnostics is not None else pd.DataFrame(),
            run_id,
            alpha_construction_version,
        ),
        "correlation": _prepare_table(
            correlation if correlation is not None else pd.DataFrame(),
            run_id,
            alpha_construction_version,
        ),
        "signal_pool": _prepare_table(
            signal_pool if signal_pool is not None else pd.DataFrame(),
            run_id,
            alpha_construction_version,
        ),
        "dynamic_weight_audit": _prepare_table(
            dynamic_weight_audit if dynamic_weight_audit is not None else pd.DataFrame(),
            run_id,
            alpha_construction_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = ALPHA_CONSTRUCTION_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in ALPHA_CONSTRUCTION_TABLES}


__all__ = [
    "ALPHA_CONSTRUCTION_TABLES",
    "alpha_candidates_to_long",
    "save_alpha_construction_outputs",
]
