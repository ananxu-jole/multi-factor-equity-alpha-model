from __future__ import annotations

import numpy as np
import pandas as pd

from src.portfolio_construction import compute_turnover


TRADING_DAYS_PER_YEAR = 252


def compute_strategy_returns(
    positions: pd.DataFrame,
    close_prices: pd.DataFrame,
    cost_bps: float = 5,
    execution_lag: int = 1,
) -> pd.DataFrame:
    """Compute conservative lagged gross and net strategy returns."""
    if execution_lag < 0:
        raise ValueError("execution_lag must be non-negative.")
    if positions.empty or close_prices.empty:
        return pd.DataFrame(
            columns=["gross_return", "turnover", "transaction_cost", "net_return"]
        )

    aligned_positions, aligned_close = positions.align(close_prices, join="inner", axis=1)
    common_index = aligned_positions.index.intersection(aligned_close.index)
    aligned_positions = aligned_positions.loc[common_index].sort_index().fillna(0.0)
    aligned_close = aligned_close.loc[common_index].sort_index()

    asset_returns = aligned_close.pct_change(fill_method=None)
    executed_positions = aligned_positions.shift(execution_lag).fillna(0.0)
    gross_returns = executed_positions.mul(asset_returns).sum(axis=1).fillna(0.0)

    turnover = compute_turnover(executed_positions)
    transaction_cost = turnover.mul(cost_bps / 10_000.0)
    net_returns = gross_returns.sub(transaction_cost, fill_value=0.0)

    return pd.DataFrame(
        {
            "gross_return": gross_returns,
            "turnover": turnover,
            "transaction_cost": transaction_cost,
            "net_return": net_returns,
        }
    )


def _annualized_return(returns: pd.Series, periods_per_year: int = TRADING_DAYS_PER_YEAR) -> float:
    returns = pd.Series(returns).dropna()
    if returns.empty:
        return np.nan
    total_return = (1.0 + returns).prod() - 1.0
    return (1.0 + total_return) ** (periods_per_year / len(returns)) - 1.0


def _annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    returns = pd.Series(returns).dropna()
    if returns.empty:
        return np.nan
    return returns.std() * np.sqrt(periods_per_year)


def _max_drawdown(returns: pd.Series) -> float:
    returns = pd.Series(returns).dropna()
    if returns.empty:
        return np.nan
    equity_curve = (1.0 + returns).cumprod()
    drawdown = equity_curve.div(equity_curve.cummax()).sub(1.0)
    return float(drawdown.min())


def _extract_return_series(strategy_returns: pd.Series | pd.DataFrame) -> pd.Series:
    if isinstance(strategy_returns, pd.DataFrame):
        if "net_return" in strategy_returns.columns:
            returns = strategy_returns["net_return"]
        elif strategy_returns.shape[1] == 1:
            returns = strategy_returns.iloc[:, 0]
        else:
            raise ValueError("strategy_returns DataFrame must include net_return or one column.")
    else:
        returns = pd.Series(strategy_returns)
    return pd.Series(returns, dtype=float).dropna()


def compute_portfolio_metrics(
    strategy_returns: pd.Series | pd.DataFrame,
    benchmark_returns: pd.Series | None = None,
) -> pd.DataFrame:
    """Compute a compact portfolio metric table."""
    returns = _extract_return_series(strategy_returns)
    total_return = (1.0 + returns).prod() - 1.0 if not returns.empty else np.nan
    annualized_return = _annualized_return(returns)
    annualized_volatility = _annualized_volatility(returns)
    sharpe = (
        annualized_return / annualized_volatility
        if annualized_volatility and not pd.isna(annualized_volatility)
        else np.nan
    )

    metrics = {
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe": sharpe,
        "max_drawdown": _max_drawdown(returns),
        "hit_rate": float((returns > 0).mean()) if not returns.empty else np.nan,
        "total_return": total_return,
    }

    if benchmark_returns is not None:
        benchmark = pd.Series(benchmark_returns).dropna()
        _, benchmark = returns.align(benchmark, join="inner")
        benchmark_total_return = (
            (1.0 + benchmark).prod() - 1.0
            if not benchmark.empty
            else np.nan
        )
        metrics["benchmark_total_return"] = benchmark_total_return
        metrics["excess_return"] = (
            total_return - benchmark_total_return
            if not pd.isna(total_return) and not pd.isna(benchmark_total_return)
            else np.nan
        )

    return pd.DataFrame(
        [{"metric": metric, "value": value} for metric, value in metrics.items()]
    )


def compute_return_diagnostics(strategy_returns: pd.Series | pd.DataFrame) -> pd.DataFrame:
    """Compute audit diagnostics for daily strategy returns."""
    returns = _extract_return_series(strategy_returns)
    if returns.empty:
        return pd.DataFrame(
            [
                {
                    "n_days": 0,
                    "active_return_days": 0,
                    "active_return_pct": np.nan,
                    "best_day": np.nan,
                    "worst_day": np.nan,
                    "top_5_day_contribution": np.nan,
                    "top_10_day_contribution": np.nan,
                    "return_concentration_ratio": np.nan,
                    "skew": np.nan,
                    "kurtosis": np.nan,
                }
            ]
        )

    active_return_days = int(returns.ne(0).sum())
    abs_returns = returns.abs().sort_values(ascending=False)
    total_abs_return = abs_returns.sum()
    top_5_contribution = (
        abs_returns.head(5).sum() / total_abs_return if total_abs_return > 0 else np.nan
    )
    top_10_contribution = (
        abs_returns.head(10).sum() / total_abs_return if total_abs_return > 0 else np.nan
    )

    return pd.DataFrame(
        [
            {
                "n_days": len(returns),
                "active_return_days": active_return_days,
                "active_return_pct": active_return_days / len(returns),
                "best_day": returns.max(),
                "worst_day": returns.min(),
                "top_5_day_contribution": top_5_contribution,
                "top_10_day_contribution": top_10_contribution,
                "return_concentration_ratio": top_10_contribution,
                "skew": returns.skew(),
                "kurtosis": returns.kurtosis(),
            }
        ]
    )


def compute_rolling_metrics(
    strategy_returns: pd.Series | pd.DataFrame,
    window: int = 63,
) -> pd.DataFrame:
    """Compute rolling return, volatility, Sharpe, and max drawdown."""
    if window < 1:
        raise ValueError("window must be at least 1.")

    returns = _extract_return_series(strategy_returns)
    if returns.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "rolling_return",
                "rolling_volatility",
                "rolling_sharpe",
                "rolling_max_drawdown",
            ]
        )

    rolling_return = (1.0 + returns).rolling(window=window, min_periods=window).apply(
        np.prod,
        raw=True,
    ).sub(1.0)
    rolling_volatility = returns.rolling(window=window, min_periods=window).std().mul(
        np.sqrt(TRADING_DAYS_PER_YEAR)
    )
    annualized_rolling_return = (1.0 + rolling_return).pow(
        TRADING_DAYS_PER_YEAR / window
    ).sub(1.0)
    rolling_sharpe = annualized_rolling_return.div(rolling_volatility)
    rolling_max_drawdown = returns.rolling(window=window, min_periods=window).apply(
        _max_drawdown,
        raw=False,
    )

    return pd.DataFrame(
        {
            "Date": returns.index,
            "rolling_return": rolling_return.to_numpy(),
            "rolling_volatility": rolling_volatility.to_numpy(),
            "rolling_sharpe": rolling_sharpe.to_numpy(),
            "rolling_max_drawdown": rolling_max_drawdown.to_numpy(),
        }
    )


def compute_monthly_returns(strategy_returns: pd.Series | pd.DataFrame) -> pd.DataFrame:
    """Compound daily strategy returns into calendar monthly returns."""
    returns = _extract_return_series(strategy_returns)
    if returns.empty:
        return pd.DataFrame(columns=["Date", "monthly_return"])

    monthly_returns = returns.resample("ME").apply(lambda x: (1.0 + x).prod() - 1.0)
    return pd.DataFrame(
        {
            "Date": monthly_returns.index,
            "monthly_return": monthly_returns.to_numpy(),
        }
    )


__all__ = [
    "TRADING_DAYS_PER_YEAR",
    "compute_monthly_returns",
    "compute_portfolio_metrics",
    "compute_return_diagnostics",
    "compute_rolling_metrics",
    "compute_strategy_returns",
]
