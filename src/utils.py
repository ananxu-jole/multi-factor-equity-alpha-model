from __future__ import annotations

import numpy as np
import pandas as pd

# ============================================================================================================================================
# 1. Continuous Strategy Backtest Engine (Risk-Controlled):
# ============================================================================================================================================

def generate_rolling_windows(
    index: pd.Index,
    train_size: int,
    test_size: int,
    step_size: int,
    purge_size: int = 0,
    embargo_size: int = 0,
) -> list[tuple[pd.Index, pd.Index]]:
    """
    Generate rolling train/test windows from a time index.

    Parameters
    ----------
    index : pd.Index
        Full date index in time order.
    train_size : int
        Number of observations in each training window.
    test_size : int
        Number of observations in each test window.
    step_size : int
        Number of observations to move forward each iteration.
    purge_size : int, default 0
        Number of rows to skip between train and test to prevent label overlap.
        In this implementation, purge_size contributes to the train/test gap.
    embargo_size : int, default 0
        Additional number of rows to skip after the purge gap before test starts.
        In this implementation, embargo_size also contributes to the train/test gap.

    Returns
    -------
    list[tuple[pd.Index, pd.Index]]
        List of (train_idx, test_idx) tuples.
    """
    if train_size <= 0 or test_size <= 0 or step_size <= 0:
        raise ValueError("train_size, test_size, and step_size must all be > 0.")
    if purge_size < 0 or embargo_size < 0:
        raise ValueError("purge_size and embargo_size must both be >= 0.")

    required = train_size + purge_size + embargo_size + test_size
    if len(index) < required:
        raise ValueError(
            "Index is too short for the requested train/test/purge/embargo sizes. "
            f"len(index)={len(index)}, required={required}."
        )

    windows: list[tuple[pd.Index, pd.Index]] = []
    max_start = len(index) - required + 1

    for start in range(0, max_start, step_size):
        train_end = start + train_size
        test_start = train_end + purge_size + embargo_size
        test_end = test_start + test_size

        train_idx = index[start:train_end]
        test_idx = index[test_start:test_end]
        windows.append((train_idx, test_idx))

    return windows


def compute_ic_weights(
    alpha_library: pd.DataFrame,
    forward_returns: pd.DataFrame,
    alpha_signals: list[str],
    score_signal_library_func,
    summarize_signal_names_func,
    min_obs: int = 60,
) -> pd.DataFrame:
    """
    Compute train-window IC-based weights for the selected alpha signals.

    Parameters
    ----------
    alpha_library : pd.DataFrame
        MultiIndex-column signal library with levels including "signal".
    forward_returns : pd.DataFrame
        Forward return matrix aligned to alpha_library.
    alpha_signals : list[str]
        Signals to keep in the weight calculation.
    score_signal_library_func : callable
        Existing scoring function from your project.
    summarize_signal_names_func : callable
        Existing summary function from your project.
    min_obs : int, default 60
        Minimum observations required for signal scoring.

    Returns
    -------
    pd.DataFrame
        Columns: signal, mean_ic, raw_weight, weight
    """
    if not isinstance(alpha_library, pd.DataFrame):
        raise TypeError("alpha_library must be a pandas DataFrame.")
    if not isinstance(forward_returns, pd.DataFrame):
        raise TypeError("forward_returns must be a pandas DataFrame.")
    if not alpha_signals:
        raise ValueError("alpha_signals must not be empty.")

    scores = score_signal_library_func(
        alpha_library,
        forward_returns,
        min_obs=min_obs,
    )

    summary = summarize_signal_names_func(scores, min_obs=min_obs)
    summary = summary[summary["signal"].isin(alpha_signals)].copy()

    if summary.empty:
        raise ValueError("No alpha signals survived IC scoring in this window.")

    summary["raw_weight"] = summary["mean_ic"].clip(lower=0)

    # Fallback: if all IC values are <= 0, use equal weights
    if summary["raw_weight"].sum() == 0:
        summary["raw_weight"] = 1.0

    summary["weight"] = summary["raw_weight"] / summary["raw_weight"].sum()

    return summary[["signal", "mean_ic", "raw_weight", "weight"]].sort_values(
        "weight",
        ascending=False,
    ).reset_index(drop=True)


def build_weighted_alpha_rank(
    alpha_library: pd.DataFrame,
    weights: dict[str, float],
) -> pd.DataFrame:
    """
    Build weighted alpha score and convert it into cross-sectional percentile rank.

    Parameters
    ----------
    alpha_library : pd.DataFrame
        MultiIndex-column alpha library with levels including "signal".
    weights : dict[str, float]
        Mapping from signal name to weight.

    Returns
    -------
    pd.DataFrame
        Cross-sectional alpha rank in [0, 1], indexed by date, columns=tickers.
    """
    if not isinstance(alpha_library, pd.DataFrame):
        raise TypeError("alpha_library must be a pandas DataFrame.")
    if not weights:
        raise ValueError("weights must not be empty.")

    missing = [
        sig for sig in weights.keys()
        if sig not in alpha_library.columns.get_level_values("signal")
    ]
    if missing:
        raise ValueError(f"Missing signals in alpha_library: {missing}")

    weighted_score = sum(
        alpha_library.xs(sig, level="signal", axis=1) * weight
        for sig, weight in weights.items()
    )

    return weighted_score.rank(axis=1, pct=True)


def build_context_rank(
    context_library: pd.DataFrame,
    context_signals: list[str],
) -> pd.DataFrame:
    """
    Build average context score and convert it into cross-sectional percentile rank.

    Parameters
    ----------
    context_library : pd.DataFrame
        MultiIndex-column context library with levels including "signal".
    context_signals : list[str]
        Context signals to include.

    Returns
    -------
    pd.DataFrame
        Cross-sectional context rank in [0, 1], indexed by date, columns=tickers.
    """
    if not isinstance(context_library, pd.DataFrame):
        raise TypeError("context_library must be a pandas DataFrame.")
    if not context_signals:
        raise ValueError("context_signals must not be empty.")

    missing = [
        sig for sig in context_signals
        if sig not in context_library.columns.get_level_values("signal")
    ]
    if missing:
        raise ValueError(f"Missing signals in context_library: {missing}")

    context_score = sum(
        context_library.xs(sig, level="signal", axis=1)
        for sig in context_signals
    ) / len(context_signals)

    return context_score.rank(axis=1, pct=True)
