from __future__ import annotations

import numpy as np
import pandas as pd


def make_forward_returns(
    clean_close_prices: pd.DataFrame,
    horizon: int = 1,
) -> pd.DataFrame:
    """
    Compute forward returns from a panel of strictly positive price levels.

    Parameters
    ----------
    clean_close_prices : pd.DataFrame
        Price panel indexed by date with tickers in columns.
    horizon : int, default 1
        Number of rows forward to use when computing returns.

    Returns
    -------
    pd.DataFrame
        Forward return from t to t+horizon, aligned to timestamp t.
    """
    if not isinstance(clean_close_prices, pd.DataFrame):
        raise TypeError("clean_close_prices must be a pandas DataFrame of price levels.")

    if not isinstance(horizon, int) or horizon <= 0:
        raise ValueError("horizon must be a positive integer.")

    px = clean_close_prices.copy()
    px.index = pd.to_datetime(px.index)
    px = px.sort_index()

    if px.empty:
        raise ValueError("clean_close_prices must not be empty.")

    if px.index.has_duplicates:
        raise ValueError("clean_close_prices index must be unique.")

    px = px.apply(pd.to_numeric, errors="coerce")

    non_null_values = px.to_numpy(dtype=float)
    valid_mask = ~np.isnan(non_null_values)
    if valid_mask.any() and (non_null_values[valid_mask] <= 0).any():
        raise ValueError(
            "make_forward_returns expects strictly positive price levels. "
            "Detected non-positive values, which usually means returns were passed in by mistake."
        )

    fwd_returns = px.shift(-horizon) / px - 1.0
    return fwd_returns.replace([np.inf, -np.inf], np.nan)


def score_signal_pair(
    signal_series: pd.Series,
    forward_return_series: pd.Series,
    min_obs: int = 30,
) -> dict:
    """
    Score one signal series against one forward return series.
    """
    df = pd.concat(
        [signal_series.rename("signal"), forward_return_series.rename("fwd_ret")],
        axis=1,
    ).dropna()

    if len(df) < min_obs:
        return {
            "n_obs": len(df),
            "ic": np.nan,
            "hit_rate": np.nan,
            "signal_std": np.nan,
            "fwd_ret_mean": np.nan,
            "top_bucket_mean": np.nan,
            "bottom_bucket_mean": np.nan,
            "spread_top_minus_bottom": np.nan,
        }

    signal_std = df["signal"].std()
    if pd.isna(signal_std) or signal_std == 0:
        return {
            "n_obs": len(df),
            "ic": np.nan,
            "hit_rate": np.nan,
            "signal_std": signal_std,
            "fwd_ret_mean": df["fwd_ret"].mean(),
            "top_bucket_mean": np.nan,
            "bottom_bucket_mean": np.nan,
            "spread_top_minus_bottom": np.nan,
        }

    ic = df["signal"].corr(df["fwd_ret"])

    signal_sign = np.sign(df["signal"])
    return_sign = np.sign(df["fwd_ret"])
    valid_sign_mask = (signal_sign != 0) & (return_sign != 0)
    if valid_sign_mask.sum() > 0:
        hit_rate = (signal_sign[valid_sign_mask] == return_sign[valid_sign_mask]).mean()
    else:
        hit_rate = np.nan

    q20 = df["signal"].quantile(0.2)
    q80 = df["signal"].quantile(0.8)

    bottom_bucket_mean = df.loc[df["signal"] <= q20, "fwd_ret"].mean()
    top_bucket_mean = df.loc[df["signal"] >= q80, "fwd_ret"].mean()
    spread = top_bucket_mean - bottom_bucket_mean

    return {
        "n_obs": len(df),
        "ic": ic,
        "hit_rate": hit_rate,
        "signal_std": signal_std,
        "fwd_ret_mean": df["fwd_ret"].mean(),
        "top_bucket_mean": top_bucket_mean,
        "bottom_bucket_mean": bottom_bucket_mean,
        "spread_top_minus_bottom": spread,
    }


def score_signal_library(
    signal_library: pd.DataFrame,
    forward_returns: pd.DataFrame,
    min_obs: int = 30,
) -> pd.DataFrame:
    """
    Score every (ticker, signal) pair in a MultiIndex-column signal library.

    signal_library columns:
        MultiIndex[ticker, signal]
    forward_returns columns:
        ticker
    """
    if not isinstance(signal_library.columns, pd.MultiIndex):
        raise TypeError("signal_library must have MultiIndex columns: (ticker, signal).")

    results = []

    tickers = signal_library.columns.get_level_values("ticker").unique()

    for ticker in tickers:
        if ticker not in forward_returns.columns:
            continue

        signal_block = signal_library[ticker]
        fwd_ret = forward_returns[ticker]

        for signal_name in signal_block.columns:
            metrics = score_signal_pair(
                signal_series=signal_block[signal_name],
                forward_return_series=fwd_ret,
                min_obs=min_obs,
            )
            metrics["ticker"] = ticker
            metrics["signal"] = signal_name
            results.append(metrics)

    scores = pd.DataFrame(results)

    if scores.empty:
        return scores

    cols = [
        "ticker",
        "signal",
        "n_obs",
        "ic",
        "hit_rate",
        "signal_std",
        "fwd_ret_mean",
        "top_bucket_mean",
        "bottom_bucket_mean",
        "spread_top_minus_bottom",
    ]
    scores = scores[cols]

    return scores.sort_values(
        by=["ic", "spread_top_minus_bottom"],
        ascending=[False, False],
    ).reset_index(drop=True)


def summarize_signal_names(
    scores: pd.DataFrame,
    min_obs: int = 30,
) -> pd.DataFrame:
    """
    Aggregate scores across tickers to see which signal names are strongest overall.
    """
    df = scores.copy()
    df = df[df["n_obs"] >= min_obs]

    summary = (
        df.groupby("signal", dropna=False)
        .agg(
            n_ticker_signal_pairs=("signal", "size"),
            mean_ic=("ic", "mean"),
            median_ic=("ic", "median"),
            mean_hit_rate=("hit_rate", "mean"),
            mean_spread=("spread_top_minus_bottom", "mean"),
            median_spread=("spread_top_minus_bottom", "median"),
        )
        .sort_values(by=["mean_ic", "mean_spread"], ascending=[False, False])
        .reset_index()
    )

    return summary
