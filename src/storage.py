from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


PHASE2_NB01_SQLITE_TABLES = {
    "close": ("clean_close_prices_current", "clean_close_prices_history"),
    "open": ("clean_open_prices_current", "clean_open_prices_history"),
    "high": ("clean_high_prices_current", "clean_high_prices_history"),
    "low": ("clean_low_prices_current", "clean_low_prices_history"),
    "volume": ("clean_volume_current", "clean_volume_history"),
    "benchmark": ("benchmark_prices_current", "benchmark_prices_history"),
    "universe_metadata": ("universe_metadata_current", "universe_metadata_history"),
    "raw_ticker_pool": ("raw_ticker_pool_current", "raw_ticker_pool_history"),
    "dynamic_top300_membership": (
        "universe_membership_dynamic_top300_current",
        "universe_membership_dynamic_top300_history",
    ),
    "dynamic_top300_diagnostics": (
        "universe_diagnostics_dynamic_top300_current",
        "universe_diagnostics_dynamic_top300_history",
    ),
}


def _prepare_for_storage(df: pd.DataFrame, run_id: str | None = None) -> pd.DataFrame:
    output = df.copy()

    if isinstance(output.index, pd.MultiIndex):
        output = output.reset_index()
    elif output.index.name is not None or not isinstance(output.index, pd.RangeIndex):
        output = output.reset_index()

    if run_id is not None and "run_id" not in output.columns:
        output.insert(0, "run_id", run_id)

    return output


def save_dataframe_csv(df: pd.DataFrame, path: str | Path, index: bool = True) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
    return path


def save_dataframe_parquet(df: pd.DataFrame, path: str | Path, index: bool = True) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=index)
    return path


def write_table_to_sqlite(
    df: pd.DataFrame,
    table_name: str,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    if_exists: str = "replace",
) -> Path:
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    output = _prepare_for_storage(df, run_id=run_id)

    with sqlite3.connect(db_path) as conn:
        if if_exists == "append":
            _ensure_append_schema(conn, table_name=table_name, df=output)
        output.to_sql(table_name, conn, if_exists=if_exists, index=False)

    return db_path


def _sqlite_column_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    return "TEXT"


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _ensure_append_schema(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    existing_columns = {
        row[1]
        for row in conn.execute(f"PRAGMA table_info({_quote_identifier(table_name)})").fetchall()
    }
    if not existing_columns:
        return

    for column in df.columns:
        if column in existing_columns:
            continue
        column_type = _sqlite_column_type(df[column])
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(str(column))} {column_type}"
        )


def write_canonical_and_history_tables(
    df: pd.DataFrame,
    canonical_table: str,
    history_table: str | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
) -> Path:
    db_path = write_table_to_sqlite(
        df=df,
        table_name=canonical_table,
        db_path=db_path,
        run_id=run_id,
        if_exists="replace",
    )

    if history_table:
        write_table_to_sqlite(
            df=df,
            table_name=history_table,
            db_path=db_path,
            run_id=run_id,
            if_exists="append",
        )

    return db_path


def get_phase2_nb01_table_names(dataset_name: str) -> tuple[str, str]:
    if dataset_name not in PHASE2_NB01_SQLITE_TABLES:
        raise KeyError(f"Unknown dataset_name '{dataset_name}'.")
    return PHASE2_NB01_SQLITE_TABLES[dataset_name]


def log_phase2_data_run(
    run_id: str,
    metadata: dict[str, object],
    sqlite_path: str | Path | None = None,
) -> Path:
    sqlite_path = Path(sqlite_path) if sqlite_path is not None else get_sqlite_db_path()

    log_row = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "run_timestamp": metadata.get("run_timestamp"),
                "universe_name": metadata.get("universe_name"),
                "benchmark_tickers": metadata.get("benchmark_tickers"),
                "n_tickers": metadata.get("n_tickers"),
                "n_dates": metadata.get("n_dates"),
                "start_date": metadata.get("start_date"),
                "end_date": metadata.get("end_date"),
                "output_dir": metadata.get("output_dir"),
                "sqlite_path": str(sqlite_path),
                "notes": metadata.get("notes"),
            }
        ]
    )

    return write_table_to_sqlite(
        df=log_row,
        table_name="run_log",
        db_path=sqlite_path,
        run_id=None,
        if_exists="append",
    )
