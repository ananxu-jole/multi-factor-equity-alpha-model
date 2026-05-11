from __future__ import annotations

import pandas as pd


def generate_walkforward_windows(
    dates,
    train_size: int,
    test_size: int,
    purge_size: int = 0,
    embargo_size: int = 0,
) -> pd.DataFrame:
    """Generate rolling walk-forward windows using date positions, not calendar days."""
    if train_size <= 0:
        raise ValueError("train_size must be positive.")
    if test_size <= 0:
        raise ValueError("test_size must be positive.")
    if purge_size < 0:
        raise ValueError("purge_size must be non-negative.")
    if embargo_size < 0:
        raise ValueError("embargo_size must be non-negative.")

    date_index = pd.DatetimeIndex(pd.to_datetime(pd.Index(dates), errors="coerce")).dropna()
    date_index = date_index.drop_duplicates().sort_values()
    if date_index.empty:
        raise ValueError("dates must contain at least one valid date.")

    rows: list[dict[str, object]] = []
    start_pos = 0
    window_id = 1
    n_dates = len(date_index)

    while True:
        train_start_pos = start_pos
        train_end_pos = train_start_pos + train_size - 1
        test_start_pos = train_end_pos + purge_size + 1
        test_end_pos = test_start_pos + test_size - 1
        embargo_start_pos = test_end_pos + 1
        embargo_end_pos = embargo_start_pos + embargo_size - 1

        if test_end_pos >= n_dates:
            break

        rows.append(
            {
                "window_id": window_id,
                "train_start": date_index[train_start_pos],
                "train_end": date_index[train_end_pos],
                "test_start": date_index[test_start_pos],
                "test_end": date_index[test_end_pos],
                "purge_size": int(purge_size),
                "embargo_size": int(embargo_size),
                "embargo_start": date_index[embargo_start_pos] if embargo_size > 0 and embargo_start_pos < n_dates else pd.NaT,
                "embargo_end": date_index[min(embargo_end_pos, n_dates - 1)] if embargo_size > 0 and embargo_start_pos < n_dates else pd.NaT,
                "n_train_dates": int(train_size),
                "n_test_dates": int(test_size),
            }
        )

        start_pos = test_end_pos + embargo_size + 1
        window_id += 1

    return pd.DataFrame(
        rows,
        columns=[
            "window_id",
            "train_start",
            "train_end",
            "test_start",
            "test_end",
            "purge_size",
            "embargo_size",
            "embargo_start",
            "embargo_end",
            "n_train_dates",
            "n_test_dates",
        ],
    )


__all__ = ["generate_walkforward_windows"]
