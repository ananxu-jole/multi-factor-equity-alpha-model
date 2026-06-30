from __future__ import annotations

import pandas as pd

from src.economic_context.quality_checks import crosstab_summary, group_size_summary
from src.economic_context.schema import MARKET_CAP_TO_SIZE_BUCKET


def validate_size_bucket_mapping(frame: pd.DataFrame) -> pd.DataFrame:
    if "market_cap_bucket" not in frame.columns or "size_bucket" not in frame.columns:
        return pd.DataFrame(
            [{"check": "market_cap_to_size_bucket", "passed": False, "bad_rows": len(frame), "message": "missing bucket columns"}]
        )
    expected = frame["market_cap_bucket"].map(MARKET_CAP_TO_SIZE_BUCKET).fillna("")
    bad = expected.ne("") & frame["size_bucket"].astype(str).ne(expected)
    return pd.DataFrame(
        [
            {
                "check": "market_cap_to_size_bucket",
                "passed": int(bad.sum()) == 0,
                "bad_rows": int(bad.sum()),
                "message": "static bucket consistency check; diagnostic only",
            }
        ]
    )


def size_bucket_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    return group_size_summary(frame, "size_bucket", min_group_size=10)


def market_cap_bucket_distribution(frame: pd.DataFrame) -> pd.DataFrame:
    return group_size_summary(frame, "market_cap_bucket", min_group_size=10)


def sector_size_crosstab(frame: pd.DataFrame) -> pd.DataFrame:
    return crosstab_summary(frame, "sector", "size_bucket")
