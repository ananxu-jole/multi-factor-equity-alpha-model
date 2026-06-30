from __future__ import annotations

import pandas as pd

from src.economic_context.quality_checks import group_size_summary


def normalize_label(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.replace(r"\s+", " ", regex=True)


def standardize_sector_industry_labels(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    for column in ["sector", "industry", "subindustry", "peer_group_label"]:
        if column in output.columns:
            output[column] = normalize_label(output[column])
    return output


def sector_distribution(frame: pd.DataFrame, min_group_size: int = 10) -> pd.DataFrame:
    return group_size_summary(frame, "sector", min_group_size=min_group_size)


def industry_distribution(frame: pd.DataFrame, min_group_size: int = 8) -> pd.DataFrame:
    return group_size_summary(frame, "industry", min_group_size=min_group_size)


def peer_group_distribution(frame: pd.DataFrame, min_group_size: int = 8) -> pd.DataFrame:
    return group_size_summary(frame, "peer_group_label", min_group_size=min_group_size)
