from __future__ import annotations

import numpy as np
import pandas as pd

# ============================================================================================================================================
# 1. Performance Metrics
# ============================================================================================================================================
def annualized_return(returns, periods_per_year=252):
    """
    Compute annualized return from a return series.
    """
    returns = pd.Series(returns).dropna()

    if len(returns) == 0:
        return np.nan

    total_return = (1 + returns).prod()
    n_periods = len(returns)
    return total_return ** (periods_per_year / n_periods) - 1


def annualized_volatility(returns, periods_per_year=252):
    """
    Compute annualized volatility from a return series.
    """
    returns = pd.Series(returns).dropna()

    if len(returns) == 0:
        return np.nan

    return returns.std() * np.sqrt(periods_per_year)


def sharpe_ratio(returns, periods_per_year=252):
    """
    Compute annualized Sharpe ratio from a return series.
    """
    vol = annualized_volatility(returns, periods_per_year)

    if pd.isna(vol) or vol == 0:
        return np.nan

    return annualized_return(returns, periods_per_year) / vol


def max_drawdown(cumulative_returns):
    """
    Compute maximum drawdown from a cumulative return series.
    Assumes cumulative_returns is already compounded.
    """
    cumulative_returns = pd.Series(cumulative_returns).dropna()

    if len(cumulative_returns) == 0:
        return np.nan

    drawdown = (cumulative_returns - cumulative_returns.cummax()) / cumulative_returns.cummax()
    return drawdown.min()


def hit_rate(returns):
    """
    Fraction of active trading periods with positive returns.
    """
    returns = pd.Series(returns).dropna()
    active_returns = returns[returns != 0]

    if len(active_returns) == 0:
        return np.nan

    return (active_returns > 0).mean()


def exposure_rate(position_series):
    """
    Fraction of periods with non-zero exposure.
    """
    position_series = pd.Series(position_series).dropna()

    if len(position_series) == 0:
        return np.nan

    return (position_series != 0).mean()


def turnover_rate(position_series):
    """
    Average absolute position change per period.
    """
    position_series = pd.Series(position_series).dropna()

    if len(position_series) == 0:
        return np.nan

    return position_series.diff().abs().fillna(0).mean()

# ============================================================================================================================================
# 2. Position & Strategy Logic:
# ============================================================================================================================================
def generate_positions_from_proba(
    probabilities,
    index=None,
    upper_threshold=None,
    lower_threshold=None,
    upper_quantile=None,
    lower_quantile=None,
):
    """
    Convert model probabilities into trading positions.
    """

    if isinstance(probabilities, pd.Series):
        prob_series = probabilities.dropna().copy()
    else:
        if index is None:
            raise ValueError("Please provide an index when probabilities is not a pandas Series.")
        prob_series = pd.Series(probabilities, index=index).dropna()

    if upper_quantile is not None and lower_quantile is not None:
        upper_threshold = prob_series.quantile(upper_quantile)
        lower_threshold = prob_series.quantile(lower_quantile)
    elif upper_threshold is None or lower_threshold is None:
        raise ValueError("Provide either both fixed thresholds or both quantiles.")

    positions = np.where(
        prob_series >= upper_threshold,
        1,
        np.where(prob_series <= lower_threshold, -1, 0)
    )

    positions = pd.Series(positions, index=prob_series.index, name="position")

    return positions, upper_threshold, lower_threshold

def strategy_returns_from_positions(positions, returns, lag=1, cost_per_trade=0.0):
    """
    Convert positions into strategy returns.

    Parameters
    ----------
    positions : pd.Series
        Trading positions indexed by date.
    returns : pd.Series or single-column pd.DataFrame
        Asset returns indexed by date.
    lag : int, default=1
        Number of periods to lag positions to avoid look-ahead bias.
    cost_per_trade : float, default=0.0
        Transaction cost applied per unit change in position.

    Returns
    -------
    pd.Series
        Net strategy return series after lag and transaction costs.
    """

    positions = pd.Series(positions).dropna()

    if isinstance(returns, pd.DataFrame):
        if returns.shape[1] != 1:
            raise ValueError("returns DataFrame must have exactly one column")
        returns = returns.iloc[:, 0]

    returns = pd.Series(returns).dropna()

    aligned_positions, aligned_returns = positions.align(returns, join="inner")

    lagged_positions = aligned_positions.shift(lag)
    gross_strategy_returns = lagged_positions * aligned_returns

    trades = lagged_positions.diff().abs().fillna(0)
    transaction_costs = cost_per_trade * trades

    net_strategy_returns = gross_strategy_returns - transaction_costs

    return net_strategy_returns.dropna()

def cumulative_returns(returns):
    """
    Compute cumulative compounded returns from a return series.
    Accepts either a pandas Series or single-column DataFrame.
    """

    # If DataFrame with one column → convert to Series
    if isinstance(returns, pd.DataFrame):
        if returns.shape[1] == 1:
            returns = returns.squeeze("columns")
        else:
            raise ValueError("cumulative_returns expects a 1D series or single-column DataFrame")

    returns = pd.Series(returns).dropna()
    return (1 + returns).cumprod()

# ============================================================================================================================================
# 3. Strategy Evaluation:
# ============================================================================================================================================
def evaluate_strategy(returns, positions=None, periods_per_year=252):
    """
    Build a summary dictionary for a strategy return series.
    """
    if isinstance(returns, pd.DataFrame):
        if returns.shape[1] != 1:
            raise ValueError("returns DataFrame must have exactly one column")
        returns = returns.iloc[:, 0]

    returns = pd.Series(returns).dropna()
    cum_returns = cumulative_returns(returns)

    summary = {
        "Annualized Return": annualized_return(returns, periods_per_year),
        "Annualized Volatility": annualized_volatility(returns, periods_per_year),
        "Sharpe Ratio": sharpe_ratio(returns, periods_per_year),
        "Max Drawdown": max_drawdown(cum_returns),
        "Hit Rate": hit_rate(returns)
    }

    if positions is not None:
        if isinstance(positions, pd.DataFrame):
            if positions.shape[1] != 1:
                raise ValueError("positions DataFrame must have exactly one column")
            positions = positions.iloc[:, 0]

        positions = pd.Series(positions).dropna()
        positions = positions.loc[positions.index.intersection(returns.index)]

        summary["Exposure Rate"] = exposure_rate(positions)
        summary["Turnover"] = turnover_rate(positions)

    return summary

# ============================================================================================================================================
# 4. Threshold Optimization:
# ============================================================================================================================================
def optimize_probability_thresholds(
        probabilities,
        returns,
        threshold_pairs,
        lag=1,
        periods_per_year=252
):
    """
    Test multiple (upper, lower) probability threshold pairs and return a
    performance table sorted by Sharpe Ratio.
    """
    probabilities = pd.Series(probabilities).dropna()
    returns = pd.Series(returns).dropna()

    results = []

    for upper, lower in threshold_pairs:
        if lower >= upper:
            continue

        positions, _, _ = generate_positions_from_proba(
            probabilities=probabilities,
            upper_threshold=upper,
            lower_threshold=lower
        )

        strat_returns = strategy_returns_from_positions(
            positions=positions,
            returns=returns,
            lag=lag
        )

        if len(strat_returns) == 0:
            continue

        summary = evaluate_strategy(
            strat_returns,
            positions=positions,
            periods_per_year=periods_per_year
        )

        summary["Upper Threshold"] = upper
        summary["Lower Threshold"] = lower

        results.append(summary)

    results_df = pd.DataFrame(results)

    if not results_df.empty:
        ordered_cols = ["Upper Threshold", "Lower Threshold"] + [
            c for c in results_df.columns
            if c not in ["Upper Threshold", "Lower Threshold"]
        ]
        results_df = results_df[ordered_cols].sort_values(
            by="Sharpe Ratio",
            ascending=False
        ).reset_index(drop=True)

    return results_df

# ============================================================================================================================================
# 5. Continuous Strategy Backtest Engine (Risk-Controlled):
# ============================================================================================================================================

def backtest_continuous_strategy(
    alpha_rank: pd.DataFrame,
    forward_returns: pd.DataFrame,
    context_rank: pd.DataFrame | None = None,
    context_mode: str = "scale",
    context_threshold: float = 0.6,
    position_cap: float | None = 0.03,
    smooth_window: int | None = 3,
    rebalance_every: int | None = None,
    min_trade_threshold: float | None = None,
    market_neutral: bool = True,
    normalize_gross: bool = True,
    target_vol: float | None = 0.10,
    vol_lookback: int = 60,
    max_leverage_scale: float = 2.0,
    cost_per_turnover: float = 0.0005,
    execution_lag: int = 1,
) -> dict:
    """
    Backtest a continuous long-short strategy using cross-sectional alpha ranks.

    Parameters
    ----------
    alpha_rank : pd.DataFrame
        Cross-sectional percentile ranks in [0, 1], indexed by date, columns=tickers.
    forward_returns : pd.DataFrame
        Forward returns aligned by date and ticker.
    context_rank : pd.DataFrame or None
        Optional context percentile ranks in [0, 1], same shape as alpha_rank.
    context_mode : {"scale", "filter", "none"}
        How context modifies exposure.
    context_threshold : float
        Threshold used when context_mode="filter".
    position_cap : float or None
        Per-name cap on raw positions before normalization.
    smooth_window : int or None
        Rolling window for smoothing positions. Use None or 1 to disable.
    rebalance_every : int or None
        Rebalance frequency in trading days. Example: 5 means rebalance every 5 days.
        Use None or 1 for daily rebalancing.
    min_trade_threshold : float or None
        Minimum absolute position change required to trade. Smaller changes are ignored.
    market_neutral : bool
        If True, demean positions cross-sectionally each day.
    normalize_gross : bool
        If True, normalize daily gross exposure to 1.
    target_vol : float or None
        Annualized target volatility for portfolio returns. Use None to disable.
    vol_lookback : int
        Lookback window for realized vol targeting.
    max_leverage_scale : float
        Maximum scaling multiplier for vol targeting.
    cost_per_turnover : float
        Linear transaction cost per unit turnover.
    execution_lag : int, default 1
        Number of bars to lag target positions before applying returns.
        Use 1 when signals are built using end-of-day information and are
        only tradable on the next bar.

    Returns
    -------
    dict
        Dictionary containing positions, gross returns, net returns,
        cumulative returns, sharpe, max drawdown, total return, turnover, costs.
    """
    if not isinstance(alpha_rank, pd.DataFrame):
        raise TypeError("alpha_rank must be a pandas DataFrame.")
    if not isinstance(forward_returns, pd.DataFrame):
        raise TypeError("forward_returns must be a pandas DataFrame.")

    if context_mode not in {"scale", "filter", "none"}:
        raise ValueError("context_mode must be one of: 'scale', 'filter', 'none'.")

    if rebalance_every is not None and rebalance_every < 1:
        raise ValueError("rebalance_every must be None or an integer >= 1.")

    if min_trade_threshold is not None and min_trade_threshold < 0:
        raise ValueError("min_trade_threshold must be None or >= 0.")
    if execution_lag < 0:
        raise ValueError("execution_lag must be >= 0.")

    # Align all inputs
    positions = alpha_rank.copy()
    if not forward_returns.index.equals(positions.index) or not forward_returns.columns.equals(positions.columns):
        raise ValueError("forward_returns must exactly match alpha_rank index and columns.")
    returns = forward_returns.reindex(index=positions.index, columns=positions.columns)

    if context_rank is not None:
        if not context_rank.index.equals(positions.index) or not context_rank.columns.equals(positions.columns):
            raise ValueError("context_rank must exactly match alpha_rank index and columns.")
        context = context_rank.reindex(index=positions.index, columns=positions.columns)
    else:
        context = None

    # Map rank [0,1] -> position [-1,1]
    positions = 2.0 * (positions - 0.5)

    # Apply context
    if context_mode == "scale":
        if context is None:
            raise ValueError("context_rank is required when context_mode='scale'.")
        context_scale = 1.0 - context
        positions = positions * context_scale

    elif context_mode == "filter":
        if context is None:
            raise ValueError("context_rank is required when context_mode='filter'.")
        good_context = (context <= context_threshold).astype(float)
        positions = positions * good_context

    # Cap per-name exposure
    if position_cap is not None:
        positions = positions.clip(lower=-position_cap, upper=position_cap)

    # Smooth positions
    if smooth_window is not None and smooth_window > 1:
        positions = positions.rolling(smooth_window, min_periods=1).mean()

    # Rebalance less frequently
    if rebalance_every is not None and rebalance_every > 1:
        rebalance_mask = pd.Series(
            np.arange(len(positions)) % rebalance_every == 0,
            index=positions.index,
        )
        positions = positions.where(rebalance_mask, np.nan).ffill()

    # Ignore tiny trades
    if min_trade_threshold is not None and min_trade_threshold > 0:
        executed_positions = positions.copy()
        prev_positions = executed_positions.shift(1)

        position_change = (executed_positions - prev_positions).abs()
        small_trade_mask = position_change < min_trade_threshold

        # keep first row as-is
        small_trade_mask.iloc[0, :] = False

        executed_positions = executed_positions.mask(small_trade_mask, prev_positions)
        positions = executed_positions

    # Market neutralize
    if market_neutral:
        positions = positions.sub(positions.mean(axis=1), axis=0)

    # Normalize daily gross exposure
    if normalize_gross:
        gross = positions.abs().sum(axis=1).replace(0, np.nan)
        positions = positions.div(gross, axis=0)

    # Lag positions so signals observed at t are only traded after the chosen delay.
    executed_positions = positions.shift(execution_lag) if execution_lag > 0 else positions.copy()

    # Gross returns
    scaled_positions = executed_positions
    gross_returns = (scaled_positions * returns).sum(axis=1)

    # Volatility targeting
    if target_vol is not None:
        realized_vol = gross_returns.rolling(vol_lookback).std().shift(1) * np.sqrt(252)
        vol_scale = (target_vol / realized_vol).clip(upper=max_leverage_scale)
        scaled_positions = executed_positions.mul(vol_scale, axis=0)
        gross_returns = (scaled_positions * returns).sum(axis=1)

    # Turnover and costs
    turnover = scaled_positions.diff().abs().sum(axis=1)
    costs = turnover * cost_per_turnover

    net_returns = (gross_returns - costs).dropna()

    cumulative = (1.0 + net_returns).cumprod()
    max_drawdown = (cumulative / cumulative.cummax() - 1.0).min()

    sharpe = np.nan
    if net_returns.std() != 0 and not np.isnan(net_returns.std()):
        sharpe = (net_returns.mean() / net_returns.std()) * np.sqrt(252)

    total_return = cumulative.iloc[-1] - 1.0 if len(cumulative) > 0 else np.nan

    return {
        "positions": positions,
        "executed_positions": executed_positions,
        "gross_returns": gross_returns,
        "net_returns": net_returns,
        "cumulative": cumulative,
        "turnover": turnover,
        "costs": costs,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "total_return": total_return,
    }

# ============================================================================================================================================
# 6. Continuous Strategy Backtest Engine (Risk-Controlled):
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
