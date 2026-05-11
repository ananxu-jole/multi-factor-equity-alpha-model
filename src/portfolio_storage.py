from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


PORTFOLIO_TABLES = {
    "alpha_score": ("portfolio_alpha_score_current", "portfolio_alpha_score_history"),
    "target_positions": (
        "portfolio_target_positions_current",
        "portfolio_target_positions_history",
    ),
    "smoothed_positions": (
        "portfolio_smoothed_positions_current",
        "portfolio_smoothed_positions_history",
    ),
    "turnover": ("portfolio_turnover_current", "portfolio_turnover_history"),
    "returns": ("portfolio_returns_current", "portfolio_returns_history"),
    "metrics": ("portfolio_metrics_current", "portfolio_metrics_history"),
    "exposure_stats": (
        "portfolio_exposure_stats_current",
        "portfolio_exposure_stats_history",
    ),
    "concentration": (
        "portfolio_concentration_current",
        "portfolio_concentration_history",
    ),
    "activity_stats": (
        "portfolio_activity_stats_current",
        "portfolio_activity_stats_history",
    ),
    "return_diagnostics": (
        "portfolio_return_diagnostics_current",
        "portfolio_return_diagnostics_history",
    ),
    "rolling_metrics": (
        "portfolio_rolling_metrics_current",
        "portfolio_rolling_metrics_history",
    ),
    "monthly_returns": (
        "portfolio_monthly_returns_current",
        "portfolio_monthly_returns_history",
    ),
}


DYNAMIC_PORTFOLIO_TABLES = {
    "alpha_pool": ("portfolio_alpha_pool_current", "portfolio_alpha_pool_history"),
    "weights": ("portfolio_weights_current", "portfolio_weights_history"),
    "backtest_results": (
        "portfolio_backtest_results_current",
        "portfolio_backtest_results_history",
    ),
    "performance_summary": (
        "portfolio_performance_summary_current",
        "portfolio_performance_summary_history",
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


def _prepare_output(
    obj: pd.DataFrame | pd.Series | None,
    run_id: str,
    portfolio_version: str,
) -> pd.DataFrame:
    if obj is None:
        output = pd.DataFrame()
    elif isinstance(obj, pd.Series):
        output = obj.to_frame()
    else:
        output = obj.copy()

    if output.empty and len(output.columns) == 0:
        output = pd.DataFrame([{}])

    if isinstance(output.index, pd.MultiIndex):
        output = output.reset_index()
    elif output.index.name is not None or not isinstance(output.index, pd.RangeIndex):
        output = output.reset_index()

    if "index" in output.columns and "Date" not in output.columns:
        output = output.rename(columns={"index": "Date"})

    if "Date" in output.columns:
        output["Date"] = pd.to_datetime(output["Date"]).dt.strftime("%Y-%m-%d")

    output["run_id"] = run_id
    output["portfolio_version"] = portfolio_version
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


def save_portfolio_outputs(
    alpha_score: pd.DataFrame,
    target_positions: pd.DataFrame,
    smoothed_positions: pd.DataFrame,
    turnover: pd.Series | pd.DataFrame,
    returns: pd.DataFrame,
    metrics: pd.DataFrame,
    exposure_stats: pd.DataFrame | None = None,
    concentration: pd.DataFrame | None = None,
    activity_stats: pd.DataFrame | None = None,
    return_diagnostics: pd.DataFrame | None = None,
    rolling_metrics: pd.DataFrame | None = None,
    monthly_returns: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    portfolio_version: str | None = None,
) -> dict[str, Path]:
    """Write Phase 3 portfolio outputs to current and history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if portfolio_version is None:
        raise ValueError("portfolio_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "alpha_score": _prepare_output(alpha_score, run_id, portfolio_version),
        "target_positions": _prepare_output(target_positions, run_id, portfolio_version),
        "smoothed_positions": _prepare_output(smoothed_positions, run_id, portfolio_version),
        "turnover": _prepare_output(turnover, run_id, portfolio_version),
        "returns": _prepare_output(returns, run_id, portfolio_version),
        "metrics": _prepare_output(metrics, run_id, portfolio_version),
        "exposure_stats": _prepare_output(exposure_stats, run_id, portfolio_version),
        "concentration": _prepare_output(concentration, run_id, portfolio_version),
        "activity_stats": _prepare_output(activity_stats, run_id, portfolio_version),
        "return_diagnostics": _prepare_output(return_diagnostics, run_id, portfolio_version),
        "rolling_metrics": _prepare_output(rolling_metrics, run_id, portfolio_version),
        "monthly_returns": _prepare_output(monthly_returns, run_id, portfolio_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = PORTFOLIO_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in PORTFOLIO_TABLES}


def save_dynamic_portfolio_outputs(
    alpha_pool: pd.DataFrame,
    weights: pd.DataFrame,
    backtest_results: pd.DataFrame,
    performance_summary: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    portfolio_version: str | None = None,
) -> dict[str, Path]:
    """Write survivor-count agnostic portfolio outputs to SQLite."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if portfolio_version is None:
        raise ValueError("portfolio_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    outputs = {
        "alpha_pool": _prepare_output(alpha_pool, run_id, portfolio_version),
        "weights": _prepare_output(weights, run_id, portfolio_version),
        "backtest_results": _prepare_output(backtest_results, run_id, portfolio_version),
        "performance_summary": _prepare_output(performance_summary, run_id, portfolio_version),
    }

    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = DYNAMIC_PORTFOLIO_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in DYNAMIC_PORTFOLIO_TABLES}


__all__ = [
    "DYNAMIC_PORTFOLIO_TABLES",
    "PORTFOLIO_TABLES",
    "save_dynamic_portfolio_outputs",
    "save_portfolio_outputs",
]
