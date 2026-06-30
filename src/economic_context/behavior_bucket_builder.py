from __future__ import annotations

import pandas as pd


def assign_cross_sectional_quantile_buckets(
    values: pd.DataFrame,
    labels: list[str],
    min_names: int = 20,
) -> pd.DataFrame:
    """Assign date-wise quantile buckets to a precomputed historical metric panel.

    The caller is responsible for providing values computed only from information
    available before the intended signal date. This utility intentionally performs
    no alpha scoring and no validation routing.
    """
    if not labels:
        raise ValueError("At least one bucket label is required.")

    def bucket_row(row: pd.Series) -> pd.Series:
        valid = row.dropna()
        if len(valid) < min_names:
            return pd.Series(index=row.index, dtype=object)
        ranked = valid.rank(method="first")
        bucket_ids = pd.qcut(ranked, q=len(labels), labels=labels, duplicates="drop")
        output = pd.Series(index=row.index, dtype=object)
        output.loc[bucket_ids.index] = bucket_ids.astype(str)
        return output

    return values.apply(bucket_row, axis=1)


def build_behavior_bucket_frame(
    bucket_panels: dict[str, pd.DataFrame],
    run_id: str,
    metadata_version: str,
    lookback_window: int,
    calculation_method: str,
    min_history_days: int,
    created_at: str,
) -> pd.DataFrame:
    rows = []
    for bucket_name, panel in bucket_panels.items():
        stacked = panel.stack(dropna=True).reset_index()
        if stacked.empty:
            continue
        stacked.columns = ["date", "ticker", bucket_name]
        rows.append(stacked)
    if not rows:
        return pd.DataFrame()

    merged = rows[0]
    for frame in rows[1:]:
        merged = merged.merge(frame, on=["date", "ticker"], how="outer")

    for column in [
        "liquidity_bucket",
        "volatility_bucket",
        "residual_vol_bucket",
        "turnover_bucket",
        "beta_bucket",
        "style_bucket",
    ]:
        if column not in merged.columns:
            merged[column] = ""

    merged["lookback_window"] = lookback_window
    merged["calculation_method"] = calculation_method
    merged["min_history_days"] = min_history_days
    merged["as_of_date"] = merged["date"]
    merged["metadata_version"] = metadata_version
    merged["run_id"] = run_id
    merged["created_at"] = created_at
    merged["notes"] = "date-aware behavioral bucket scaffold; diagnostic/control use only"
    return merged
