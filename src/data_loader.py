from __future__ import annotations

import pandas as pd
import yfinance as yf


def split_features_target(dataset: pd.DataFrame, target_col: str = "target"):
    """
    Split an ML-ready dataset into features (X) and target (y).
    """
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("dataset must be a pandas DataFrame.")

    if target_col not in dataset.columns:
        raise ValueError(
            f"'{target_col}' not found in dataset. "
            f"Available columns include: {list(dataset.columns[:10])}"
        )

    X = dataset.drop(columns=[target_col]).copy()
    y = dataset[target_col].copy()

    return X, y


def make_time_split_index(data, split_ratio: float = 0.8):
    """
    Create train/test date indexes from any time-indexed pandas object.
    """
    if not isinstance(data, (pd.DataFrame, pd.Series)):
        raise TypeError("data must be a pandas DataFrame or Series.")

    if not 0 < split_ratio < 1:
        raise ValueError("split_ratio must be between 0 and 1.")

    if len(data) < 2:
        raise ValueError("data must contain at least 2 rows.")

    data = data.sort_index()
    split_idx = int(len(data) * split_ratio)

    train_idx = data.index[:split_idx]
    test_idx = data.index[split_idx:]

    return train_idx, test_idx


def split_by_index(data, train_idx, test_idx):
    """
    Split a pandas object using precomputed train/test indexes.
    """
    if not isinstance(data, (pd.DataFrame, pd.Series)):
        raise TypeError("data must be a pandas DataFrame or Series.")

    train = data.loc[train_idx].copy()
    test = data.loc[test_idx].copy()

    return train, test


def time_based_split(X, y, split_ratio: float = 0.8):
    """
    Backward-compatible helper used by earlier notebooks.
    """
    train_idx, test_idx = make_time_split_index(X, split_ratio=split_ratio)
    X_train, X_test = split_by_index(X, train_idx, test_idx)
    y_train, y_test = split_by_index(y, train_idx, test_idx)
    return X_train, X_test, y_train, y_test


def get_benchmark_returns(price_df, tickers, index):
    if isinstance(tickers, str):
        tickers = [tickers]

    for ticker in tickers:
        if ticker not in price_df.columns:
            raise ValueError(f"{ticker} not found in price data")

    returns = price_df[tickers].pct_change(fill_method=None).dropna()
    returns = returns.loc[returns.index.intersection(index)]

    return returns.loc[index].copy()


def _standardize_ohlcv_download(raw_data: pd.DataFrame, requested_tickers: list[str]) -> pd.DataFrame:
    if raw_data.empty:
        raise ValueError("yfinance returned an empty OHLCV DataFrame.")

    if not isinstance(raw_data.columns, pd.MultiIndex):
        ticker = requested_tickers[0]
        raw_data.columns = pd.MultiIndex.from_product(
            [raw_data.columns.tolist(), [ticker]],
            names=["field", "ticker"],
        )
    else:
        first_level = set(raw_data.columns.get_level_values(0))
        second_level = set(raw_data.columns.get_level_values(1))
        requested_set = set(requested_tickers)

        if requested_set.intersection(first_level):
            raw_data = raw_data.swaplevel(0, 1, axis=1)

        raw_data.columns = raw_data.columns.set_names(["field", "ticker"])

    raw_data.index = pd.to_datetime(raw_data.index)
    raw_data = raw_data.sort_index().sort_index(axis=1)

    return raw_data


def build_download_status(raw_ohlcv: pd.DataFrame, requested_tickers: list[str]) -> pd.DataFrame:
    available_tickers = sorted(set(raw_ohlcv.columns.get_level_values("ticker")))
    close_panel = raw_ohlcv.xs("Close", axis=1, level="field")
    records = []

    for ticker in requested_tickers:
        if ticker not in available_tickers:
            status = "missing_from_download"
            rows = 0
            first_valid_date = pd.NaT
            last_valid_date = pd.NaT
        else:
            series = close_panel[ticker]
            non_null = series.dropna()
            status = "ok" if not non_null.empty else "all_close_missing"
            rows = int(non_null.shape[0])
            first_valid_date = non_null.index.min() if not non_null.empty else pd.NaT
            last_valid_date = non_null.index.max() if not non_null.empty else pd.NaT

        records.append(
            {
                "ticker": ticker,
                "status": status,
                "non_null_close_rows": rows,
                "first_valid_date": first_valid_date,
                "last_valid_date": last_valid_date,
            }
        )

    return pd.DataFrame.from_records(records)


def download_ohlcv_data(
    tickers: list[str],
    start_date: str,
    end_date: str | None = None,
    auto_adjust: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Download raw OHLCV data from yfinance and return a standardized MultiIndex DataFrame
    plus a per-ticker download status summary.
    """
    if not tickers:
        raise ValueError("tickers must not be empty.")

    requested_tickers = list(dict.fromkeys(tickers))

    raw_data = yf.download(
        tickers=requested_tickers,
        start=start_date,
        end=end_date,
        auto_adjust=auto_adjust,
        progress=False,
        group_by="column",
        threads=True,
    )

    raw_ohlcv = _standardize_ohlcv_download(raw_data=raw_data, requested_tickers=requested_tickers)
    download_status = build_download_status(raw_ohlcv=raw_ohlcv, requested_tickers=requested_tickers)

    return raw_ohlcv, download_status
