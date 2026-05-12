from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


REGIME_IC_TABLES = {
    "features": ("regime_features_ic_current", "regime_features_ic_history"),
    "daily": ("signal_regime_ic_daily_current", "signal_regime_ic_daily_history"),
    "summary": ("signal_regime_ic_summary_current", "signal_regime_ic_summary_history"),
    "fragility": ("signal_regime_fragility_current", "signal_regime_fragility_history"),
    "opportunity": (
        "signal_regime_opportunity_summary_current",
        "signal_regime_opportunity_summary_history",
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


def _prepare_output(df: pd.DataFrame, run_id: str, regime_ic_version: str) -> pd.DataFrame:
    output = df.copy()
    if "Date" in output.columns:
        output["Date"] = pd.to_datetime(output["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    output["run_id"] = run_id
    output["regime_ic_version"] = regime_ic_version
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


def save_regime_ic_outputs(
    regime_features: pd.DataFrame,
    daily_regime_ic: pd.DataFrame,
    regime_summary: pd.DataFrame,
    regime_fragility: pd.DataFrame,
    regime_opportunity_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    regime_ic_version: str | None = None,
) -> dict[str, Path]:
    """Write regime-conditioned IC diagnostics to current/history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if regime_ic_version is None:
        raise ValueError("regime_ic_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "features": _prepare_output(regime_features, run_id, regime_ic_version),
        "daily": _prepare_output(daily_regime_ic, run_id, regime_ic_version),
        "summary": _prepare_output(regime_summary, run_id, regime_ic_version),
        "fragility": _prepare_output(regime_fragility, run_id, regime_ic_version),
        "opportunity": _prepare_output(
            regime_opportunity_summary if regime_opportunity_summary is not None else pd.DataFrame(),
            run_id,
            regime_ic_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = REGIME_IC_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in REGIME_IC_TABLES}


__all__ = ["REGIME_IC_TABLES", "save_regime_ic_outputs"]
