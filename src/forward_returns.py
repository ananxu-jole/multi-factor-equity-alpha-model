from __future__ import annotations

import numpy as np
import pandas as pd


def _normalize_close_prices(close_prices: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(close_prices, pd.DataFrame):
        raise TypeError("close_prices must be a pandas DataFrame.")
    if close_prices.empty:
        raise ValueError("close_prices must not be empty.")

    close = close_prices.copy()
    close.index = pd.to_datetime(close.index, errors="coerce")
    if close.index.isna().any():
        raise ValueError("close_prices index contains values that cannot be parsed as dates.")
    if close.index.has_duplicates:
        raise ValueError("close_prices index must be unique.")

    close = close.sort_index()
    close = close.apply(pd.to_numeric, errors="coerce")
    return close


def make_forward_returns(
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...],
) -> dict[int, pd.DataFrame]:
    """Compute forward returns from clean close price panels for multiple horizons."""
    close = _normalize_close_prices(close_prices)

    if isinstance(horizons, int):
        raise TypeError("horizons must be an iterable of positive integers, not a single int.")

    horizon_values = [int(horizon) for horizon in horizons]
    if not horizon_values:
        raise ValueError("horizons must contain at least one horizon.")
    if any(horizon <= 0 for horizon in horizon_values):
        raise ValueError("all horizons must be positive integers.")
    if len(set(horizon_values)) != len(horizon_values):
        raise ValueError("horizons must not contain duplicate values.")

    return {
        horizon: (close.shift(-horizon) / close - 1.0).replace([np.inf, -np.inf], np.nan)
        for horizon in horizon_values
    }


def validate_forward_return_panels(
    forward_returns: dict[int, pd.DataFrame],
    close_prices: pd.DataFrame,
) -> None:
    """Validate that forward return panels preserve the close price panel shape and labels."""
    close = _normalize_close_prices(close_prices)

    if not isinstance(forward_returns, dict) or not forward_returns:
        raise ValueError("forward_returns must be a non-empty dict of horizon -> DataFrame.")

    for horizon, panel in forward_returns.items():
        if not isinstance(horizon, int) or horizon <= 0:
            raise ValueError(f"Invalid forward return horizon: {horizon!r}.")
        if not isinstance(panel, pd.DataFrame):
            raise TypeError(f"Forward return panel for horizon {horizon} must be a DataFrame.")
        if not panel.index.equals(close.index):
            raise ValueError(f"Forward return panel for horizon {horizon} does not preserve Date index.")
        if not panel.columns.equals(close.columns):
            raise ValueError(f"Forward return panel for horizon {horizon} does not preserve ticker columns.")

        values = panel.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
        if np.isinf(values).any():
            raise ValueError(f"Forward return panel for horizon {horizon} contains inf values.")


__all__ = [
    "make_forward_returns",
    "validate_forward_return_panels",
]
