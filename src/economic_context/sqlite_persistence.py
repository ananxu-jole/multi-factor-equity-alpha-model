from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.db import connect_db, get_db_path
from src.economic_context.schema import (
    BEHAVIOR_BUCKET_COLUMNS,
    BEHAVIOR_BUCKET_TABLES,
    CLASSIFICATION_COLUMNS,
    CLASSIFICATION_TABLES,
    COVERAGE_DIAGNOSTIC_COLUMNS,
    COVERAGE_DIAGNOSTICS_TABLES,
    PEER_GROUP_COLUMNS,
    PEER_GROUP_TABLES,
    QUALITY_ALERT_COLUMNS,
    QUALITY_ALERTS_TABLES,
    SIZE_COLUMNS,
    SIZE_TABLES,
    SOURCE_AUDIT_COLUMNS,
    SOURCE_AUDIT_TABLES,
    TablePair,
)
from src.storage import write_canonical_and_history_tables


TABLE_COLUMNS = {
    CLASSIFICATION_TABLES: CLASSIFICATION_COLUMNS,
    SIZE_TABLES: SIZE_COLUMNS,
    BEHAVIOR_BUCKET_TABLES: BEHAVIOR_BUCKET_COLUMNS,
    PEER_GROUP_TABLES: PEER_GROUP_COLUMNS,
    COVERAGE_DIAGNOSTICS_TABLES: COVERAGE_DIAGNOSTIC_COLUMNS,
    SOURCE_AUDIT_TABLES: SOURCE_AUDIT_COLUMNS,
    QUALITY_ALERTS_TABLES: QUALITY_ALERT_COLUMNS,
}


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _sqlite_type(column: str) -> str:
    if column in {
        "is_current",
        "fallback_used",
        "diagnostic_only",
    }:
        return "INTEGER"
    if column.endswith("_count") or column in {
        "total_universe_tickers",
        "covered_tickers",
        "missing_tickers",
        "peer_group_size",
        "peer_group_min_size",
        "thin_group_count",
        "record_count_raw",
        "record_count_clean",
        "lookback_window",
        "min_history_days",
    }:
        return "INTEGER"
    if column in {"coverage_ratio", "market_cap"}:
        return "REAL"
    return "TEXT"


def create_table_pair(
    conn: sqlite3.Connection,
    table_pair: TablePair,
    columns: list[str],
) -> None:
    column_sql = ", ".join(f"{_quote_identifier(column)} {_sqlite_type(column)}" for column in columns)
    for table_name in [table_pair.current, table_pair.history]:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {_quote_identifier(table_name)} ({column_sql})")


def create_economic_context_tables(db_path: str | Path | None = None) -> Path:
    """Create enrichment metadata tables only; does not write alpha or validation tables."""
    resolved = Path(db_path) if db_path is not None else get_db_path()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with connect_db(resolved) as conn:
        for table_pair, columns in TABLE_COLUMNS.items():
            create_table_pair(conn, table_pair, columns)
        conn.commit()
    return resolved


def persist_current_and_history(
    frame: pd.DataFrame,
    table_pair: TablePair,
    db_path: str | Path | None = None,
    run_id: str | None = None,
) -> Path:
    return write_canonical_and_history_tables(
        df=frame,
        canonical_table=table_pair.current,
        history_table=table_pair.history,
        db_path=db_path,
        run_id=run_id,
    )
