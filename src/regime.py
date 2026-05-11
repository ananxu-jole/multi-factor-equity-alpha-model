from __future__ import annotations

import numpy as np
import pandas as pd


LOW_VOL = "LOW_VOL"
MID_VOL = "MID_VOL"
HIGH_VOL = "HIGH_VOL"

UPTREND = "UPTREND"
DOWNTREND = "DOWNTREND"
SIDEWAYS = "SIDEWAYS"

LOW_DRAWDOWN = "LOW_DRAWDOWN"
HIGH_DRAWDOWN = "HIGH_DRAWDOWN"


def _coerce_price_series(
    prices: pd.Series | pd.DataFrame,
    preferred_column: str = "SPY",
) -> pd.Series:
    """Return one clean benchmark price series from a Series or wide DataFrame."""
    if isinstance(prices, pd.Series):
        series = prices.copy()
    elif isinstance(prices, pd.DataFrame):
        candidates = prices.copy()
        metadata_columns = {
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
        candidates = candidates.drop(
            columns=[column for column in metadata_columns if column in candidates.columns],
            errors="ignore",
        )
        if preferred_column in candidates.columns:
            series = candidates[preferred_column]
        else:
            numeric_columns = [
                column
                for column in candidates.columns
                if pd.api.types.is_numeric_dtype(pd.to_numeric(candidates[column], errors="coerce"))
            ]
            if not numeric_columns:
                raise ValueError("No numeric benchmark price column found.")
            series = candidates[numeric_columns[0]]
    else:
        raise TypeError("prices must be a pandas Series or DataFrame.")

    series = pd.to_numeric(series, errors="coerce")
    series.index = pd.to_datetime(series.index)
    return series.sort_index()


def classify_volatility_regime(
    benchmark_returns: pd.Series,
    lookback: int = 20,
) -> pd.Series:
    """Classify trailing benchmark return volatility into low/mid/high terciles."""
    returns = pd.to_numeric(benchmark_returns, errors="coerce").copy()
    returns.index = pd.to_datetime(returns.index)
    realized_vol = returns.sort_index().rolling(lookback).std()

    valid_vol = realized_vol.dropna()
    if valid_vol.empty:
        return pd.Series(index=realized_vol.index, dtype="object", name="benchmark_vol_regime")

    low_threshold = valid_vol.quantile(1 / 3)
    high_threshold = valid_vol.quantile(2 / 3)

    regime = pd.Series(MID_VOL, index=realized_vol.index, dtype="object")
    regime[realized_vol <= low_threshold] = LOW_VOL
    regime[realized_vol >= high_threshold] = HIGH_VOL
    regime[realized_vol.isna()] = np.nan
    regime.name = "benchmark_vol_regime"
    return regime


def classify_trend_regime(
    benchmark_prices: pd.Series | pd.DataFrame,
    short_window: int = 50,
    long_window: int = 200,
) -> pd.Series:
    """Classify benchmark trend from short/long moving-average alignment."""
    prices = _coerce_price_series(benchmark_prices)
    short_ma = prices.rolling(short_window).mean()
    long_ma = prices.rolling(long_window).mean()

    regime = pd.Series(SIDEWAYS, index=prices.index, dtype="object")
    regime[(short_ma > long_ma) & (prices > long_ma)] = UPTREND
    regime[(short_ma < long_ma) & (prices < long_ma)] = DOWNTREND
    regime[short_ma.isna() | long_ma.isna() | prices.isna()] = np.nan
    regime.name = "benchmark_trend_regime"
    return regime


def build_market_regime_features(
    close_prices: pd.DataFrame,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Build simple, explainable market regime features from a benchmark column."""
    benchmark_prices = _coerce_price_series(close_prices, preferred_column=benchmark_ticker)
    return _build_regime_table_from_benchmark(benchmark_prices)


def _build_regime_table_from_benchmark(benchmark_prices: pd.Series) -> pd.DataFrame:
    benchmark_prices = _coerce_price_series(benchmark_prices)
    benchmark_returns = benchmark_prices.pct_change(fill_method=None)
    benchmark_vol = benchmark_returns.rolling(20).std()
    running_peak = benchmark_prices.cummax()
    market_drawdown = benchmark_prices / running_peak - 1.0

    drawdown_regime = pd.Series(LOW_DRAWDOWN, index=benchmark_prices.index, dtype="object")
    drawdown_regime[market_drawdown <= -0.10] = HIGH_DRAWDOWN
    drawdown_regime[market_drawdown.isna()] = np.nan

    regime_table = pd.DataFrame(index=benchmark_prices.index)
    regime_table.index.name = "Date"
    regime_table["benchmark_return_1d"] = benchmark_returns
    regime_table["benchmark_vol_20d"] = benchmark_vol
    regime_table["benchmark_vol_regime"] = classify_volatility_regime(benchmark_returns, lookback=20)
    regime_table["benchmark_trend_regime"] = classify_trend_regime(benchmark_prices)
    regime_table["market_drawdown"] = market_drawdown
    regime_table["drawdown_regime"] = drawdown_regime
    return regime_table.reset_index()


def build_regime_table(
    close_prices: pd.DataFrame,
    benchmark_prices: pd.Series | pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build the canonical regime table, using explicit benchmark prices when provided."""
    if benchmark_prices is not None:
        benchmark = _coerce_price_series(benchmark_prices, preferred_column="SPY")
        return _build_regime_table_from_benchmark(benchmark)

    return build_market_regime_features(close_prices=close_prices, benchmark_ticker="SPY")


__all__ = [
    "DOWNTREND",
    "HIGH_DRAWDOWN",
    "HIGH_VOL",
    "LOW_DRAWDOWN",
    "LOW_VOL",
    "MID_VOL",
    "SIDEWAYS",
    "UPTREND",
    "build_market_regime_features",
    "build_regime_table",
    "classify_trend_regime",
    "classify_volatility_regime",
]
