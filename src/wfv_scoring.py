from __future__ import annotations

import numpy as np
import pandas as pd

from src.forward_returns import make_forward_returns
from src.signal_storage import pivot_signal_long_to_panel


def _align_panels(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    signal = signal_panel.copy()
    fwd = fwd_return_panel.copy()
    signal.index = pd.to_datetime(signal.index, errors="coerce")
    fwd.index = pd.to_datetime(fwd.index, errors="coerce")

    common_dates = signal.index.intersection(fwd.index).sort_values()
    common_tickers = signal.columns.intersection(fwd.columns).sort_values()
    if common_dates.empty:
        raise ValueError("signal_panel and fwd_return_panel have no overlapping dates.")
    if common_tickers.empty:
        raise ValueError("signal_panel and fwd_return_panel have no overlapping tickers.")

    return (
        signal.reindex(index=common_dates, columns=common_tickers).apply(pd.to_numeric, errors="coerce"),
        fwd.reindex(index=common_dates, columns=common_tickers).apply(pd.to_numeric, errors="coerce"),
    )


def _safe_corr(df: pd.DataFrame, method: str) -> float:
    if len(df) < 2:
        return np.nan
    if df["signal"].nunique(dropna=True) < 2 or df["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(df["signal"].corr(df["fwd_return"], method=method))


def _score_period(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    start_date,
    end_date,
    method: str,
) -> dict[str, object]:
    signal_slice = signal_panel.loc[start_date:end_date]
    fwd_slice = fwd_return_panel.loc[start_date:end_date]

    paired = pd.concat(
        [
            signal_slice.stack(future_stack=True).rename("signal"),
            fwd_slice.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    if paired.empty:
        return {"mean_ic": np.nan, "positive_ic_rate": np.nan, "n_obs": 0}

    ic_by_date = paired.groupby(level=0, sort=True).apply(_safe_corr, method=method).dropna()
    return {
        "mean_ic": float(ic_by_date.mean()) if not ic_by_date.empty else np.nan,
        "positive_ic_rate": float((ic_by_date > 0).mean()) if not ic_by_date.empty else np.nan,
        "n_obs": int(len(paired)),
    }


def _daily_ic_and_n_obs(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    method: str,
) -> tuple[pd.Series, pd.Series]:
    paired = pd.concat(
        [
            signal_panel.stack(future_stack=True).rename("signal"),
            fwd_return_panel.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    if paired.empty:
        empty_index = pd.DatetimeIndex([], name=signal_panel.index.name)
        return (
            pd.Series(dtype=float, index=empty_index, name="mean_ic"),
            pd.Series(dtype=int, index=empty_index, name="n_obs"),
        )

    grouped = paired.groupby(level=0, sort=True)
    daily_ic = grouped.apply(_safe_corr, method=method).dropna()
    n_obs = grouped.size()
    return daily_ic, n_obs


def _score_period_from_daily(
    daily_ic: pd.Series,
    n_obs_by_date: pd.Series,
    start_date,
    end_date,
) -> dict[str, object]:
    n_obs_slice = n_obs_by_date.loc[start_date:end_date]
    n_obs = int(n_obs_slice.sum()) if not n_obs_slice.empty else 0
    if n_obs == 0:
        return {"mean_ic": np.nan, "positive_ic_rate": np.nan, "n_obs": 0}

    ic_slice = daily_ic.loc[start_date:end_date].dropna()
    return {
        "mean_ic": float(ic_slice.mean()) if not ic_slice.empty else np.nan,
        "positive_ic_rate": float((ic_slice > 0).mean()) if not ic_slice.empty else np.nan,
        "n_obs": n_obs,
    }


def score_signal_wfv(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    windows: pd.DataFrame,
    signal_name: str,
    horizon: int,
    method: str = "spearman",
) -> pd.DataFrame:
    """Score one signal/horizon across walk-forward windows using date-level cross-sectional IC."""
    if method not in {"spearman", "pearson", "kendall"}:
        raise ValueError("method must be one of: spearman, pearson, kendall.")

    signal, fwd = _align_panels(signal_panel, fwd_return_panel)
    daily_ic, n_obs_by_date = _daily_ic_and_n_obs(signal, fwd, method=method)
    rows: list[dict[str, object]] = []

    for _, window in windows.iterrows():
        train = _score_period_from_daily(
            daily_ic,
            n_obs_by_date,
            window["train_start"],
            window["train_end"],
        )
        test = _score_period_from_daily(
            daily_ic,
            n_obs_by_date,
            window["test_start"],
            window["test_end"],
        )
        rows.append(
            {
                "window_id": int(window["window_id"]),
                "signal_name": signal_name,
                "horizon": int(horizon),
                "method": method,
                "train_start": window["train_start"],
                "train_end": window["train_end"],
                "test_start": window["test_start"],
                "test_end": window["test_end"],
                "train_mean_ic": train["mean_ic"],
                "test_mean_ic": test["mean_ic"],
                "train_positive_ic_rate": train["positive_ic_rate"],
                "test_positive_ic_rate": test["positive_ic_rate"],
                "train_n_obs": train["n_obs"],
                "test_n_obs": test["n_obs"],
            }
        )

    return pd.DataFrame(rows)


def run_wfv_for_candidates(
    candidates: pd.DataFrame,
    signal_long_df: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...],
    windows: pd.DataFrame,
    method: str = "spearman",
) -> pd.DataFrame:
    """Run WFV scoring for candidate signal/horizon rows."""
    required_columns = {"signal_name", "horizon"}
    missing_columns = required_columns.difference(candidates.columns)
    if missing_columns:
        raise ValueError(f"candidates is missing required columns: {sorted(missing_columns)}")

    horizon_values = sorted({int(horizon) for horizon in horizons})
    forward_returns = make_forward_returns(close_prices, horizon_values)
    rows: list[pd.DataFrame] = []
    panel_cache: dict[str, pd.DataFrame] = {}

    candidates_to_run = candidates.copy()
    candidates_to_run["horizon"] = candidates_to_run["horizon"].astype(int)
    candidates_to_run = candidates_to_run[candidates_to_run["horizon"].isin(horizon_values)]

    metadata_columns = [
        column
        for column in ["candidate_tier", "signal_direction", "signal_family", "signal_strength", "source_status"]
        if column in candidates_to_run.columns
    ]

    for _, candidate in candidates_to_run.iterrows():
        signal_name = str(candidate["signal_name"])
        horizon = int(candidate["horizon"])

        if signal_name not in panel_cache:
            panel_cache[signal_name] = pivot_signal_long_to_panel(signal_long_df, signal_name)

        scored = score_signal_wfv(
            signal_panel=panel_cache[signal_name],
            fwd_return_panel=forward_returns[horizon],
            windows=windows,
            signal_name=signal_name,
            horizon=horizon,
            method=method,
        )
        for column in metadata_columns:
            scored[column] = candidate[column]
        rows.append(scored)

    if not rows:
        return pd.DataFrame()

    output = pd.concat(rows, ignore_index=True)
    leading_columns = [
        "window_id",
        "signal_name",
        "horizon",
        "candidate_tier",
        "signal_direction",
        "signal_family",
        "signal_strength",
        "source_status",
        "method",
        "train_start",
        "train_end",
        "test_start",
        "test_end",
        "train_mean_ic",
        "test_mean_ic",
        "train_positive_ic_rate",
        "test_positive_ic_rate",
        "train_n_obs",
        "test_n_obs",
    ]
    ordered = [column for column in leading_columns if column in output.columns]
    remaining = [column for column in output.columns if column not in ordered]
    return output[ordered + remaining].sort_values(["signal_name", "horizon", "window_id"]).reset_index(drop=True)


__all__ = [
    "run_wfv_for_candidates",
    "score_signal_wfv",
]
