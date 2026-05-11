from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


ALPHA_TABLES = {
    "candidates": ("alpha_candidates_current", "alpha_candidates_history"),
    "metadata": ("alpha_metadata_current", "alpha_metadata_history"),
    "quality": ("alpha_quality_current", "alpha_quality_history"),
    "regime_features": ("regime_features_current", "regime_features_history"),
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


def alpha_candidates_to_long(
    alpha_candidates: dict[str, pd.DataFrame],
    run_id: str,
    alpha_version: str,
) -> pd.DataFrame:
    """Convert alpha panels into SQLite long format."""
    long_frames: list[pd.DataFrame] = []

    for alpha_name, alpha_df in alpha_candidates.items():
        panel = alpha_df.copy()
        panel.index.name = "Date"
        panel.columns.name = "ticker"

        long_alpha = (
            panel.stack(future_stack=True)
            .rename("alpha_value")
            .reset_index()
        )
        long_alpha["alpha_name"] = alpha_name
        long_alpha["run_id"] = run_id
        long_alpha["alpha_version"] = alpha_version
        long_frames.append(long_alpha)

    if not long_frames:
        return pd.DataFrame(
            columns=["Date", "ticker", "alpha_name", "alpha_value", "run_id", "alpha_version"]
        )

    output = pd.concat(long_frames, ignore_index=True)
    return output[["Date", "ticker", "alpha_name", "alpha_value", "run_id", "alpha_version"]]


def _with_run_columns(df: pd.DataFrame, run_id: str, alpha_version: str) -> pd.DataFrame:
    output = df.copy()
    output["run_id"] = run_id
    output["alpha_version"] = alpha_version
    return output


def _prepare_regime_features(
    regime_features: pd.DataFrame,
    run_id: str,
    alpha_version: str,
) -> pd.DataFrame:
    output = regime_features.copy()
    if "Date" not in output.columns:
        output = output.reset_index().rename(columns={output.index.name or "index": "Date"})
    output["run_id"] = run_id
    output["alpha_version"] = alpha_version
    return output


def save_alpha_outputs(
    alpha_candidates: dict[str, pd.DataFrame],
    alpha_metadata: pd.DataFrame,
    alpha_quality: pd.DataFrame,
    regime_features: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    alpha_version: str | None = None,
) -> dict[str, Path]:
    """Write conditional alpha artifacts to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if alpha_version is None:
        raise ValueError("alpha_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "candidates": alpha_candidates_to_long(
            alpha_candidates=alpha_candidates,
            run_id=run_id,
            alpha_version=alpha_version,
        ),
        "metadata": _with_run_columns(alpha_metadata, run_id=run_id, alpha_version=alpha_version),
        "quality": _with_run_columns(alpha_quality, run_id=run_id, alpha_version=alpha_version),
        "regime_features": _prepare_regime_features(
            regime_features,
            run_id=run_id,
            alpha_version=alpha_version,
        ),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = ALPHA_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in ALPHA_TABLES}


__all__ = [
    "ALPHA_TABLES",
    "alpha_candidates_to_long",
    "save_alpha_outputs",
]
