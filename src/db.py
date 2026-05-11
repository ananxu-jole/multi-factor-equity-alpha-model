from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


PRICE_TABLES = {
    "open": ("clean_open_prices_current", "clean_open_prices_history"),
    "high": ("clean_high_prices_current", "clean_high_prices_history"),
    "low": ("clean_low_prices_current", "clean_low_prices_history"),
    "close": ("clean_close_prices_current", "clean_close_prices_history"),
    "volume": ("clean_volume_current", "clean_volume_history"),
}


PRICE_METADATA_COLUMNS = {
    "run_id",
    "run_timestamp",
    "timestamp",
    "timestamp_frozen",
    "universe_mode",
    "universe_version",
    "output_dir",
    "sqlite_path",
    "notes",
}


def get_db_path() -> Path:
    """Return the default project SQLite database path."""
    return get_sqlite_db_path()


def connect_db(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Return a SQLite connection to the project database."""
    return sqlite3.connect(Path(db_path) if db_path is not None else get_db_path())


def list_tables(db_path: str | Path | None = None) -> pd.DataFrame:
    """Return SQLite table names from sqlite_master."""
    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """
    with connect_db(db_path) as conn:
        return pd.read_sql_query(query, conn)


def table_exists(table_name: str, db_path: str | Path | None = None) -> bool:
    """Return whether a table exists in the SQLite database."""
    query = """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
    """
    with connect_db(db_path) as conn:
        result = conn.execute(query, (table_name,)).fetchone()
    return result is not None


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def list_table_indexes(
    db_path: str | Path | None,
    table_name: str,
) -> pd.DataFrame:
    """Return SQLite indexes and indexed columns for a table."""
    rows: list[dict[str, object]] = []
    with connect_db(db_path) as conn:
        index_list = conn.execute(
            f"PRAGMA index_list({_quote_identifier(table_name)})"
        ).fetchall()
        for index_row in index_list:
            index_name = str(index_row[1])
            index_columns = conn.execute(
                f"PRAGMA index_info({_quote_identifier(index_name)})"
            ).fetchall()
            rows.append(
                {
                    "table_name": table_name,
                    "index_name": index_name,
                    "unique": bool(index_row[2]),
                    "origin": index_row[3] if len(index_row) > 3 else None,
                    "partial": bool(index_row[4]) if len(index_row) > 4 else None,
                    "columns": ",".join(str(column_row[2]) for column_row in index_columns),
                }
            )
    return pd.DataFrame(
        rows,
        columns=["table_name", "index_name", "unique", "origin", "partial", "columns"],
    )


def ensure_candidate_signal_indexes(db_path: str | Path | None = None) -> pd.DataFrame:
    """Create targeted indexes for high-volume current candidate signal reads.

    These indexes intentionally target candidate_signals_current, not history:
    approved signal filtering uses signal_name, pivot validation uses
    signal_name/Date/ticker uniqueness, and panel operations often depend on
    Date/ticker alignment. History tables append runs and are not on the main
    notebook read path, so we avoid adding heavier history indexes without a
    clear query pattern.
    """
    resolved_db_path = Path(db_path) if db_path is not None else get_db_path()
    if not table_exists("candidate_signals_current", db_path=resolved_db_path):
        raise ValueError(f"Required table is missing: candidate_signals_current")

    statements = [
        """
        CREATE INDEX IF NOT EXISTS idx_candidate_signals_current_signal
        ON candidate_signals_current(signal_name)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_candidate_signals_current_signal_date_ticker
        ON candidate_signals_current(signal_name, Date, ticker)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_candidate_signals_current_date_ticker
        ON candidate_signals_current(Date, ticker)
        """,
    ]
    with connect_db(resolved_db_path) as conn:
        for statement in statements:
            conn.execute(statement)
        conn.commit()

    return list_table_indexes(resolved_db_path, "candidate_signals_current")


def _resolve_current_history_table(
    current: bool,
    current_table: str,
    history_table: str,
) -> str:
    return current_table if current else history_table


def _drop_metadata_columns(df: pd.DataFrame) -> pd.DataFrame:
    metadata_columns = [column for column in PRICE_METADATA_COLUMNS if column in df.columns]
    return df.drop(columns=metadata_columns) if metadata_columns else df


def load_table(table_name: str, db_path: str | Path | None = None) -> pd.DataFrame:
    """Load any SQLite table into a pandas DataFrame."""
    if not table_exists(table_name, db_path=db_path):
        resolved_db_path = get_db_path() if db_path is None else db_path
        raise ValueError(f"Table '{table_name}' does not exist in {resolved_db_path}.")

    query = f"SELECT * FROM {_quote_identifier(table_name)}"
    with connect_db(db_path) as conn:
        return pd.read_sql_query(query, conn)


def load_price_table(
    table_name: str,
    db_path: str | Path | None = None,
    date_col: str = "Date",
) -> pd.DataFrame:
    """Load a price-style table with a sorted datetime index when possible."""
    df = load_table(table_name, db_path=db_path)

    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()

    return _drop_metadata_columns(df)


def load_ohlcv_panels(
    current: bool = True,
    db_path: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """Load the canonical OHLCV price panels from SQLite."""
    return {
        name: load_price_table(
            _resolve_current_history_table(current, current_table, history_table),
            db_path=db_path,
        )
        for name, (current_table, history_table) in PRICE_TABLES.items()
    }


def load_benchmark_prices(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load benchmark prices from SQLite."""
    table_name = _resolve_current_history_table(
        current,
        "benchmark_prices_current",
        "benchmark_prices_history",
    )
    return load_price_table(table_name, db_path=db_path)


def load_universe_metadata(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load universe metadata from SQLite."""
    table_name = _resolve_current_history_table(
        current,
        "universe_metadata_current",
        "universe_metadata_history",
    )
    return load_table(table_name, db_path=db_path)


def load_run_log(db_path: str | Path | None = None) -> pd.DataFrame:
    """Load the project run log from SQLite."""
    return load_table("run_log", db_path=db_path)


def get_latest_run_id(db_path: str | Path | None = None) -> str | None:
    """Return the latest run_id from run_log, ordered by run_timestamp when available."""
    if not table_exists("run_log", db_path=db_path):
        return None

    run_log = load_run_log(db_path=db_path)
    if run_log.empty or "run_id" not in run_log:
        return None

    if "run_timestamp" in run_log.columns:
        run_log = run_log.copy()
        run_log["run_timestamp"] = pd.to_datetime(
            run_log["run_timestamp"],
            errors="coerce",
        )
        run_log = run_log.sort_values("run_timestamp", na_position="first")

    run_ids = run_log["run_id"].dropna()
    latest_run_id = run_ids.iloc[-1] if not run_ids.empty else None
    return str(latest_run_id) if latest_run_id is not None else None


__all__ = [
    "connect_db",
    "ensure_candidate_signal_indexes",
    "get_db_path",
    "get_latest_run_id",
    "list_table_indexes",
    "list_tables",
    "load_benchmark_prices",
    "load_ohlcv_panels",
    "load_price_table",
    "load_run_log",
    "load_table",
    "load_universe_metadata",
    "table_exists",
]
