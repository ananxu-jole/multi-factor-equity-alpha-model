from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.economic_context.schema import SNAPSHOT_WARNING, STATIC_SNAPSHOT_ONLY, REQUIRED_STATIC_SEED_COLUMNS


def normalize_ticker(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.upper()


def load_static_seed_csv(path: str | Path) -> pd.DataFrame:
    """Load the research-only static metadata seed without granting validation use."""
    seed_path = Path(path)
    if not seed_path.exists():
        raise FileNotFoundError(f"Missing economic context seed CSV: {seed_path}")

    frame = pd.read_csv(seed_path, dtype=str, keep_default_na=False)
    missing = [column for column in REQUIRED_STATIC_SEED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Seed CSV is missing required columns: {missing}")

    frame = frame.copy()
    frame["ticker"] = normalize_ticker(frame["ticker"])
    frame["point_in_time_quality"] = STATIC_SNAPSHOT_ONLY
    if "snapshot_warning" not in frame.columns:
        frame["snapshot_warning"] = SNAPSHOT_WARNING
    return frame


OVERRIDE_REQUIRED_COLUMNS = [
    "ticker",
    "normalized_ticker",
    "sector",
    "industry",
    "source",
    "source_date",
    "effective_date",
    "is_static_snapshot",
    "validation_usage_allowed",
    "diagnostic_usage_allowed",
    "notes",
]


def load_override_csv(path: str | Path) -> pd.DataFrame:
    """Load controlled manual overrides as diagnostic-only metadata."""
    override_path = Path(path)
    if not override_path.exists():
        return pd.DataFrame(columns=OVERRIDE_REQUIRED_COLUMNS)

    frame = pd.read_csv(override_path, dtype=str, keep_default_na=False)
    missing = [column for column in OVERRIDE_REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Override CSV is missing required columns: {missing}")
    frame = frame.copy()
    frame["ticker"] = normalize_ticker(frame["ticker"])
    frame["normalized_ticker"] = normalize_ticker(frame["normalized_ticker"])
    if "snapshot_warning" not in frame.columns:
        frame["snapshot_warning"] = SNAPSHOT_WARNING
    return frame


def overrides_to_seed_rows(
    overrides: pd.DataFrame,
    universe_version: str,
    metadata_version: str,
    collection_timestamp: str,
) -> pd.DataFrame:
    """Convert validated diagnostic-only overrides into seed-compatible rows."""
    if overrides.empty:
        return pd.DataFrame(columns=REQUIRED_STATIC_SEED_COLUMNS)

    output = pd.DataFrame(
        {
            "ticker": normalize_ticker(overrides["normalized_ticker"]),
            "company_name": overrides.get("company_name", ""),
            "sector": overrides["sector"],
            "industry": overrides["industry"],
            "peer_group_label": overrides.get("peer_group_label", "industry:" + overrides["industry"].astype(str)),
            "market_cap_bucket": overrides.get("market_cap_bucket", ""),
            "size_bucket": overrides.get("size_bucket", ""),
            "source": overrides["source"],
            "source_url_or_reference": overrides.get(
                "source_url_or_reference",
                "economic_context_overrides_v1_internal_review_no_external_fetch",
            ),
            "as_of_date": overrides["source_date"],
            "effective_date": overrides["effective_date"],
            "collection_timestamp": collection_timestamp,
            "universe_version": universe_version,
            "metadata_version": metadata_version,
            "snapshot_warning": overrides.get("snapshot_warning", SNAPSHOT_WARNING),
        }
    )
    return output[REQUIRED_STATIC_SEED_COLUMNS]


def merge_seed_with_overrides(seed: pd.DataFrame, overrides_seed_rows: pd.DataFrame) -> pd.DataFrame:
    """Merge seed and overrides without overwriting existing seed rows."""
    if overrides_seed_rows.empty:
        return seed.copy()

    seed_tickers = set(normalize_ticker(seed["ticker"]))
    additions = overrides_seed_rows.loc[
        ~normalize_ticker(overrides_seed_rows["ticker"]).isin(seed_tickers)
    ].copy()
    merged = pd.concat([seed.copy(), additions], ignore_index=True)
    merged["ticker"] = normalize_ticker(merged["ticker"])
    return merged


def static_seed_to_classification_frame(seed: pd.DataFrame, run_id: str) -> pd.DataFrame:
    """Convert the existing seed format into the enrichment classification schema."""
    output = pd.DataFrame(
        {
            "ticker": normalize_ticker(seed["ticker"]),
            "company_name": seed.get("company_name", ""),
            "sector": seed.get("sector", ""),
            "industry": seed.get("industry", ""),
            "subindustry": seed.get("subindustry", ""),
            "peer_group_label": seed.get("peer_group_label", ""),
            "peer_group_level": "industry",
            "classification_system": "manual_static_snapshot",
            "source": seed.get("source", ""),
            "source_version": seed.get("metadata_version", ""),
            "source_record_id": "",
            "as_of_date": seed.get("as_of_date", ""),
            "effective_start": seed.get("effective_date", ""),
            "effective_end": "",
            "is_current": True,
            "point_in_time_quality": STATIC_SNAPSHOT_ONLY,
            "snapshot_warning": seed.get("snapshot_warning", SNAPSHOT_WARNING),
            "universe_version": seed.get("universe_version", ""),
            "metadata_version": seed.get("metadata_version", ""),
            "run_id": run_id,
            "collection_timestamp": seed.get("collection_timestamp", ""),
            "record_hash": "",
            "notes": "static snapshot diagnostic metadata; blocked from alpha validation",
        }
    )
    return output


def static_seed_to_size_frame(seed: pd.DataFrame, run_id: str) -> pd.DataFrame:
    """Convert static size buckets into the enrichment size schema."""
    return pd.DataFrame(
        {
            "ticker": normalize_ticker(seed["ticker"]),
            "market_cap": "",
            "market_cap_bucket": seed.get("market_cap_bucket", ""),
            "size_bucket": seed.get("size_bucket", ""),
            "currency": "",
            "market_cap_as_of_date": seed.get("as_of_date", ""),
            "effective_start": seed.get("effective_date", ""),
            "effective_end": "",
            "source": seed.get("source", ""),
            "source_version": seed.get("metadata_version", ""),
            "point_in_time_quality": STATIC_SNAPSHOT_ONLY,
            "snapshot_warning": seed.get("snapshot_warning", SNAPSHOT_WARNING),
            "universe_version": seed.get("universe_version", ""),
            "metadata_version": seed.get("metadata_version", ""),
            "run_id": run_id,
            "collection_timestamp": seed.get("collection_timestamp", ""),
            "record_hash": "",
            "notes": "static size bucket diagnostic metadata; blocked from alpha validation",
        }
    )
