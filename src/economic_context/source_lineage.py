from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from src.economic_context.schema import SNAPSHOT_WARNING, STATIC_SNAPSHOT_ONLY


def file_sha256(path: str | Path) -> str | None:
    source_path = Path(path)
    if not source_path.exists():
        return None
    digest = hashlib.sha256()
    with source_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_source_audit_frame(
    source_path: str | Path,
    source: str,
    metadata_version: str,
    run_id: str,
    collection_timestamp: str,
    record_count_raw: int,
    record_count_clean: int,
    source_version: str = "",
    source_url_or_reference: str = "",
    license_or_usage_notes: str = "research-only static metadata; no production or validation use",
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "metadata_version": metadata_version,
                "source": source,
                "source_version": source_version,
                "source_file_path": str(source_path),
                "source_url_or_reference": source_url_or_reference,
                "source_file_hash": file_sha256(source_path),
                "record_count_raw": int(record_count_raw),
                "record_count_clean": int(record_count_clean),
                "collection_timestamp": collection_timestamp,
                "point_in_time_quality": STATIC_SNAPSHOT_ONLY,
                "snapshot_warning": SNAPSHOT_WARNING,
                "license_or_usage_notes": license_or_usage_notes,
                "notes": "diagnostic-only source audit",
            }
        ]
    )
