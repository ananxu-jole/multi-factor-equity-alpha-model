from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SIGNAL_DISCOVERY_SPACE_TABLES = {
    "search_space": (
        "signal_discovery_search_space_current",
        "signal_discovery_search_space_history",
    ),
}


SIGNAL_DISCOVERY_SPACE_COLUMNS = [
    "discovery_family",
    "base_formula",
    "signal_template_name",
    "parameter_grid",
    "required_inputs",
    "transform_options",
    "direction_hypotheses",
    "expected_horizons",
    "expected_diversification_role",
    "priority",
    "notes",
]


DEFAULT_TRANSFORMS = ["raw", "rank", "zscore", "winsorized_zscore"]
DEFAULT_DIRECTIONS = ["positive_edge", "negative_edge_reverse"]


def _json_text(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def build_signal_discovery_search_space() -> pd.DataFrame:
    """Return the machine-readable Phase 2 signal discovery search space."""
    rows = [
        {
            "discovery_family": "cross_sectional_relative_return",
            "base_formula": "close.pct_change(window) - cross_sectional_mean(close.pct_change(window))",
            "signal_template_name": "relative_return_{window}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["5d", "10d", "20d"],
            "expected_diversification_role": "Adds same-date universe-relative price information distinct from broad market direction.",
            "priority": "HIGH",
            "notes": "Use trailing returns only; center by same-date available universe before transform.",
        },
        {
            "discovery_family": "beta_neutral_return",
            "base_formula": "close.pct_change(window) - rolling_beta(beta_window) * benchmark_return(window)",
            "signal_template_name": "beta_neutral_return_{window}_{beta_window}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "beta_windows": [60, 120], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close", "benchmark_close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["5d", "10d", "20d"],
            "expected_diversification_role": "Separates stock-specific return from broad systematic exposure.",
            "priority": "HIGH",
            "notes": "Use SPY when present; otherwise equal-weight universe return fallback in implementation metadata.",
        },
        {
            "discovery_family": "volatility_adjusted_momentum",
            "base_formula": "close.pct_change(window) / rolling_std(daily_return, vol_window)",
            "signal_template_name": "vol_adj_momentum_{window}_{vol_window}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "vol_windows": [20, 60, 120], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["10d", "20d"],
            "expected_diversification_role": "Tests smoother momentum variants without relying only on raw volatility level.",
            "priority": "MEDIUM",
            "notes": "Handle zero realized volatility as missing before cross-sectional transforms.",
        },
        {
            "discovery_family": "volatility_surprise",
            "base_formula": "rolling_std(daily_return, short_window) / rolling_std(daily_return, long_window) - 1",
            "signal_template_name": "vol_surprise_{short_window}_{long_window}",
            "parameter_grid": {"short_windows": [5, 10, 20], "long_windows": [60, 120], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["5d", "10d", "20d"],
            "expected_diversification_role": "Captures volatility regime transitions rather than persistent high-volatility names.",
            "priority": "MEDIUM",
            "notes": "Treat as volatility-adjacent and require diversity checks before promotion.",
        },
        {
            "discovery_family": "volume_return_interaction",
            "base_formula": "return(window) combined with volume trend, acceleration, or z-score over matching windows",
            "signal_template_name": "volume_return_interaction_{window}_{interaction}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "interactions": ["return_minus_volume_trend", "return_times_volume_zscore", "signed_volume_pressure"], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close", "volume"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["5d", "10d", "20d"],
            "expected_diversification_role": "Adds participation context to price moves and helps identify unsupported trends.",
            "priority": "HIGH",
            "notes": "Use trailing volume windows only; replace zero-volume denominators with missing.",
        },
        {
            "discovery_family": "reversal_overextension",
            "base_formula": "negative return(window), distance from moving average, or return z-score after overextension",
            "signal_template_name": "reversal_overextension_{window}_{measure}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "measures": ["negative_return", "negative_distance_to_ma", "negative_return_zscore"], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["1d", "5d", "10d"],
            "expected_diversification_role": "Expands short-horizon pullback behavior beyond raw volatility survivors.",
            "priority": "MEDIUM",
            "notes": "Keep formulas trailing-only; execution lag remains downstream.",
        },
        {
            "discovery_family": "correlation_change",
            "base_formula": "rolling_corr(stock_return, benchmark_return, short_window) - rolling_corr(..., long_window)",
            "signal_template_name": "corr_change_{short_window}_{long_window}",
            "parameter_grid": {"short_windows": [5, 10, 20], "long_windows": [60, 120], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close", "benchmark_close"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["10d", "20d"],
            "expected_diversification_role": "Targets changing market co-movement and crowding rather than return or volatility level.",
            "priority": "HIGH",
            "notes": "Use SPY if available, otherwise equal-weight market return fallback.",
        },
        {
            "discovery_family": "liquidity_adjusted_return",
            "base_formula": "return(window) scaled or conditioned by dollar volume, Amihud illiquidity, or liquidity rank",
            "signal_template_name": "liquidity_adjusted_return_{window}_{liquidity_measure}",
            "parameter_grid": {"windows": [5, 10, 20, 60], "liquidity_measures": ["dollar_volume_rank", "amihud_illiq", "volume_trend"], "transforms": DEFAULT_TRANSFORMS, "directions": DEFAULT_DIRECTIONS},
            "required_inputs": ["close", "volume"],
            "transform_options": DEFAULT_TRANSFORMS,
            "direction_hypotheses": DEFAULT_DIRECTIONS,
            "expected_horizons": ["5d", "10d", "20d"],
            "expected_diversification_role": "Separates return effects that depend on tradability and price impact.",
            "priority": "MEDIUM",
            "notes": "Guard dollar-volume denominators and keep liquidity direction explicit in metadata.",
        },
    ]

    output = pd.DataFrame(rows)
    for column in ["parameter_grid", "required_inputs", "transform_options", "direction_hypotheses", "expected_horizons"]:
        output[column] = output[column].map(_json_text)
    return output.reindex(columns=SIGNAL_DISCOVERY_SPACE_COLUMNS)


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


def save_signal_discovery_search_space(
    search_space: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    search_space_version: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Path]:
    """Save the signal discovery search space to current/history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if search_space_version is None:
        raise ValueError("search_space_version is required.")
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    output = search_space.copy()
    output["run_id"] = run_id
    output["search_space_version"] = search_space_version
    output["timestamp"] = timestamp

    current_table, history_table = SIGNAL_DISCOVERY_SPACE_TABLES["search_space"]
    with sqlite3.connect(db_path) as conn:
        output.to_sql(current_table, conn, if_exists="replace", index=False)
        if _table_exists(conn, history_table):
            _ensure_sqlite_columns(output, history_table, conn)
        output.to_sql(history_table, conn, if_exists="append", index=False)
    return {"search_space": db_path}


__all__ = [
    "SIGNAL_DISCOVERY_SPACE_COLUMNS",
    "SIGNAL_DISCOVERY_SPACE_TABLES",
    "build_signal_discovery_search_space",
    "save_signal_discovery_search_space",
]
