from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


OHLCV_FIELDS = ["Open", "High", "Low", "Close", "Volume"]


def _validate_ohlcv_columns(raw_ohlcv: pd.DataFrame) -> None:
    if not isinstance(raw_ohlcv, pd.DataFrame):
        raise TypeError("raw_ohlcv must be a pandas DataFrame.")

    if not isinstance(raw_ohlcv.columns, pd.MultiIndex) or raw_ohlcv.columns.nlevels != 2:
        raise ValueError(
            "raw_ohlcv must have two-level MultiIndex columns: level 0 = field, level 1 = ticker."
        )


def enforce_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.index = pd.to_datetime(cleaned.index)
    cleaned = cleaned.sort_index()
    cleaned.index.name = "Date"
    return cleaned


def enforce_panel_contract(
    df: pd.DataFrame,
    name: str,
    require_numeric: bool = True,
) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"{name} must be a pandas DataFrame.")

    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{name} must use a pandas DatetimeIndex.")

    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{name} index must be sorted ascending.")

    if df.index.has_duplicates:
        raise ValueError(f"{name} index must not contain duplicate dates.")

    if not df.columns.is_unique:
        raise ValueError(f"{name} columns must be unique.")

    if pd.Index(df.columns).isna().any():
        raise ValueError(f"{name} columns must not contain null labels.")

    if require_numeric:
        non_numeric = df.columns[~df.dtypes.apply(pd.api.types.is_numeric_dtype)]
        if len(non_numeric) > 0:
            raise TypeError(
                f"{name} must contain numeric data only. Non-numeric columns: {list(non_numeric)}"
            )

    return df


def extract_ohlcv_panel(raw_ohlcv: pd.DataFrame, field: str) -> pd.DataFrame:
    _validate_ohlcv_columns(raw_ohlcv)

    if field not in raw_ohlcv.columns.get_level_values(0):
        raise ValueError(f"Field '{field}' not found in OHLCV data.")

    panel = raw_ohlcv.xs(field, axis=1, level=0).copy()
    panel = enforce_datetime_index(panel)
    panel = panel.replace([np.inf, -np.inf], np.nan)
    panel = panel.sort_index(axis=1)
    panel.columns.name = "Ticker"
    return panel


def drop_all_empty_tickers(df: pd.DataFrame) -> pd.DataFrame:
    keep_cols = df.columns[~df.isna().all(axis=0)]
    return df.loc[:, keep_cols].copy()


def clean_panel(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = enforce_datetime_index(df)
    cleaned = cleaned.replace([np.inf, -np.inf], np.nan)
    cleaned = cleaned.sort_index(axis=1)
    cleaned = drop_all_empty_tickers(cleaned)
    return enforce_panel_contract(cleaned, "panel")


def build_ohlcv_panels(raw_ohlcv: pd.DataFrame) -> dict[str, pd.DataFrame]:
    panels = {}
    for field in OHLCV_FIELDS:
        panel_name = field.lower()
        panels[panel_name] = enforce_panel_contract(
            clean_panel(extract_ohlcv_panel(raw_ohlcv, field)),
            panel_name,
        )
    return panels


def align_panels(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    if not panels:
        raise ValueError("panels must not be empty.")

    cleaned_panels = {name: clean_panel(panel) for name, panel in panels.items()}

    common_index = None
    common_columns = None

    for panel in cleaned_panels.values():
        common_index = panel.index if common_index is None else common_index.intersection(panel.index)
        common_columns = (
            panel.columns if common_columns is None else common_columns.intersection(panel.columns)
        )

    aligned = {
        name: enforce_panel_contract(
            panel.loc[common_index, common_columns].copy(),
            name,
        )
        for name, panel in cleaned_panels.items()
    }
    return aligned


def ticker_health_report(df: pd.DataFrame, panel_name: str) -> pd.DataFrame:
    validated = enforce_panel_contract(df, panel_name)

    records = []
    for ticker in validated.columns:
        series = validated[ticker]
        non_null = series.dropna()
        records.append(
            {
                "panel_name": panel_name,
                "ticker": ticker,
                "n_obs": int(non_null.shape[0]),
                "missing_count": int(series.isna().sum()),
                "missing_pct": float(series.isna().mean()),
                "first_valid_date": non_null.index.min() if not non_null.empty else pd.NaT,
                "last_valid_date": non_null.index.max() if not non_null.empty else pd.NaT,
            }
        )

    return pd.DataFrame.from_records(records).sort_values(["panel_name", "ticker"]).reset_index(drop=True)


def build_ticker_health_reports(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        panel_name: ticker_health_report(panel, panel_name)
        for panel_name, panel in panels.items()
    }


def missingness_summary(df: pd.DataFrame) -> pd.DataFrame:
    validated = enforce_panel_contract(df, "missingness_panel")

    summary = pd.DataFrame(
        {
            "ticker": validated.columns,
            "missing_count": validated.isna().sum(axis=0).values,
            "missing_pct": validated.isna().mean(axis=0).values,
            "non_null_count": validated.notna().sum(axis=0).values,
        }
    )
    return summary.sort_values(["missing_pct", "ticker"], ascending=[False, True]).reset_index(drop=True)


def summarize_panel_collection(panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    records = []
    for panel_name, panel in panels.items():
        validated = enforce_panel_contract(panel, panel_name)
        records.append(
            {
                "panel": panel_name,
                "row_count": len(validated),
                "ticker_count": validated.shape[1],
                "start_date": validated.index.min(),
                "end_date": validated.index.max(),
                "total_missing": int(validated.isna().sum().sum()),
                "missing_pct": float(validated.isna().stack().mean()) if validated.size else 0.0,
            }
        )
    return pd.DataFrame.from_records(records)


def basic_data_quality_checks(
    panels: dict[str, pd.DataFrame],
    expected_tickers: Iterable[str] | None = None,
) -> pd.DataFrame:
    if not panels:
        raise ValueError("panels must not be empty.")

    expected_tickers = list(expected_tickers or [])
    records = []

    for panel_name, panel in panels.items():
        validated = enforce_panel_contract(panel, panel_name)
        index_is_datetime = isinstance(validated.index, pd.DatetimeIndex)
        index_is_sorted = validated.index.is_monotonic_increasing
        duplicate_dates = int(validated.index.duplicated().sum())
        duplicate_tickers = int(validated.columns.duplicated().sum())
        inf_count = int(np.isinf(validated.select_dtypes(include=[np.number])).sum().sum())
        empty_tickers = int(validated.isna().all(axis=0).sum())
        missing_tickers = sorted(set(expected_tickers) - set(validated.columns)) if expected_tickers else []

        records.append(
            {
                "panel": panel_name,
                "row_count": len(validated),
                "ticker_count": validated.shape[1],
                "index_is_datetime": index_is_datetime,
                "index_is_sorted": index_is_sorted,
                "duplicate_dates": duplicate_dates,
                "duplicate_tickers": duplicate_tickers,
                "inf_count": inf_count,
                "all_empty_tickers": empty_tickers,
                "null_column_labels": int(pd.Index(validated.columns).isna().sum()),
                "numeric_columns_only": bool(validated.dtypes.apply(pd.api.types.is_numeric_dtype).all()),
                "missing_expected_tickers": ", ".join(missing_tickers),
                "passed": all(
                    [
                        index_is_datetime,
                        index_is_sorted,
                        duplicate_dates == 0,
                        duplicate_tickers == 0,
                        inf_count == 0,
                        empty_tickers == 0,
                        int(pd.Index(validated.columns).isna().sum()) == 0,
                        bool(validated.dtypes.apply(pd.api.types.is_numeric_dtype).all()),
                    ]
                ),
            }
        )

    return pd.DataFrame.from_records(records)
