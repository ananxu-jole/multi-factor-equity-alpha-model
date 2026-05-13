"""Optional signal panel cache artifacts for scoring engines.

SQLite remains the source of truth. This module writes reusable Date x ticker
panel artifacts derived from selected rows in candidate_signals_current.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import nullcontext, redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from urllib.parse import quote

import pandas as pd

from src.run_config import get_project_root, get_sqlite_db_path
from src.signal_storage import (
    load_candidate_signals_by_names,
    pivot_signal_long_to_panel,
    validate_signal_date_quality,
    validate_signal_long_uniqueness,
)


PANEL_CACHE_METADATA_VERSION = "signal_panel_cache_v1"
DEFAULT_PANEL_CACHE_DIR = get_project_root() / "artifacts" / "panels" / "signals"
DEFAULT_SOURCE_TABLE = "candidate_signals_current"


def parquet_supported() -> bool:
    try:
        import pyarrow  # noqa: F401
    except ImportError:
        try:
            import fastparquet  # noqa: F401
        except ImportError:
            return False
    return True


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _cache_dir(cache_dir: str | Path | None = None) -> Path:
    return Path(cache_dir) if cache_dir is not None else DEFAULT_PANEL_CACHE_DIR


def _safe_signal_stem(signal_name: str) -> str:
    quoted = quote(signal_name, safe="")
    return re.sub(r"[^A-Za-z0-9_.%-]", "_", quoted)


def panel_cache_paths(signal_name: str, cache_dir: str | Path | None = None) -> dict[str, Path]:
    base = _cache_dir(cache_dir)
    stem = _safe_signal_stem(signal_name)
    return {
        "panel": base / f"{stem}.parquet",
        "metadata": base / f"{stem}.metadata.json",
    }


def _source_signal_metadata(
    signal_name: str,
    source_table: str = DEFAULT_SOURCE_TABLE,
    db_path: str | Path | None = None,
) -> dict[str, object]:
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    query = f"""
        SELECT
            COUNT(*) AS source_row_count,
            MIN(Date) AS date_min,
            MAX(Date) AS date_max,
            COUNT(DISTINCT Date) AS n_dates,
            COUNT(DISTINCT ticker) AS n_tickers,
            COUNT(DISTINCT run_id) AS run_id_count,
            MIN(run_id) AS run_id,
            COUNT(DISTINCT signal_version) AS signal_version_count,
            MIN(signal_version) AS signal_version
        FROM {_quote_identifier(source_table)}
        WHERE signal_name = ?
    """
    with sqlite3.connect(resolved_db_path) as conn:
        row = conn.execute(query, (signal_name,)).fetchone()
    if row is None:
        raise ValueError(f"signal_name {signal_name!r} not found in {source_table}.")
    columns = [
        "source_row_count",
        "date_min",
        "date_max",
        "n_dates",
        "n_tickers",
        "run_id_count",
        "run_id",
        "signal_version_count",
        "signal_version",
    ]
    return dict(zip(columns, row, strict=True))


def _source_signal_metadata_by_names(
    signal_names: list[str],
    source_table: str = DEFAULT_SOURCE_TABLE,
    db_path: str | Path | None = None,
) -> dict[str, dict[str, object]]:
    if not signal_names:
        return {}
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    placeholders = ",".join("?" for _ in signal_names)
    query = f"""
        SELECT
            signal_name,
            COUNT(*) AS source_row_count,
            MIN(Date) AS date_min,
            MAX(Date) AS date_max,
            COUNT(DISTINCT Date) AS n_dates,
            COUNT(DISTINCT ticker) AS n_tickers,
            COUNT(DISTINCT run_id) AS run_id_count,
            MIN(run_id) AS run_id,
            COUNT(DISTINCT signal_version) AS signal_version_count,
            MIN(signal_version) AS signal_version
        FROM {_quote_identifier(source_table)}
        WHERE signal_name IN ({placeholders})
        GROUP BY signal_name
    """
    with sqlite3.connect(resolved_db_path) as conn:
        rows = conn.execute(query, signal_names).fetchall()
    columns = [
        "signal_name",
        "source_row_count",
        "date_min",
        "date_max",
        "n_dates",
        "n_tickers",
        "run_id_count",
        "run_id",
        "signal_version_count",
        "signal_version",
    ]
    return {
        str(row[0]): dict(zip(columns[1:], row[1:], strict=True))
        for row in rows
    }


def _panel_checksum(panel: pd.DataFrame) -> str:
    normalized = panel.copy()
    normalized.index = pd.to_datetime(normalized.index, errors="raise")
    normalized = normalized.sort_index().sort_index(axis=1)
    hashed = pd.util.hash_pandas_object(normalized, index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()


def _metadata_for_panel(
    signal_name: str,
    panel: pd.DataFrame,
    source_metadata: dict[str, object],
    source_table: str,
    panel_path: Path,
) -> dict[str, object]:
    index = pd.to_datetime(panel.index, errors="raise")
    run_id = source_metadata.get("run_id") if source_metadata.get("run_id_count") == 1 else None
    signal_version = (
        source_metadata.get("signal_version")
        if source_metadata.get("signal_version_count") == 1
        else None
    )
    return {
        "metadata_version": PANEL_CACHE_METADATA_VERSION,
        "signal_name": signal_name,
        "source_table": source_table,
        "source_row_count": int(source_metadata.get("source_row_count") or 0),
        "signal_version": signal_version,
        "run_id": run_id,
        "universe_version": None,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "date_min": index.min().strftime("%Y-%m-%d") if len(index) else None,
        "date_max": index.max().strftime("%Y-%m-%d") if len(index) else None,
        "n_dates": int(panel.shape[0]),
        "n_tickers": int(panel.shape[1]),
        "checksum_sha256": _panel_checksum(panel),
        "panel_path": str(panel_path),
    }


def _write_metadata(metadata: dict[str, object], metadata_path: Path) -> None:
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def _read_metadata(metadata_path: Path) -> dict[str, object]:
    return json.loads(metadata_path.read_text())


def cache_is_fresh(
    signal_name: str,
    source_table: str = DEFAULT_SOURCE_TABLE,
    db_path: str | Path | None = None,
    cache_dir: str | Path | None = None,
) -> bool:
    paths = panel_cache_paths(signal_name, cache_dir=cache_dir)
    if not paths["panel"].exists() or not paths["metadata"].exists():
        return False
    metadata = _read_metadata(paths["metadata"])
    if metadata.get("metadata_version") != PANEL_CACHE_METADATA_VERSION:
        return False
    if metadata.get("signal_name") != signal_name or metadata.get("source_table") != source_table:
        return False
    source_metadata = _source_signal_metadata(signal_name, source_table=source_table, db_path=db_path)
    return _metadata_matches_source(metadata, signal_name, source_table, source_metadata)


def _metadata_matches_source(
    metadata: dict[str, object],
    signal_name: str,
    source_table: str,
    source_metadata: dict[str, object],
) -> bool:
    return (
        metadata.get("metadata_version") == PANEL_CACHE_METADATA_VERSION
        and metadata.get("signal_name") == signal_name
        and metadata.get("source_table") == source_table
        and int(metadata.get("source_row_count") or -1) == int(source_metadata.get("source_row_count") or 0)
        and metadata.get("date_min") == str(pd.to_datetime(source_metadata.get("date_min")).date())
        and metadata.get("date_max") == str(pd.to_datetime(source_metadata.get("date_max")).date())
        and int(metadata.get("n_dates") or -1) == int(source_metadata.get("n_dates") or 0)
        and int(metadata.get("n_tickers") or -1) == int(source_metadata.get("n_tickers") or 0)
    )


def load_signal_panel_from_cache(
    signal_name: str,
    cache_dir: str | Path | None = None,
    validate_checksum: bool = False,
) -> pd.DataFrame:
    if not parquet_supported():
        raise ImportError("Parquet support requires pyarrow or fastparquet.")
    paths = panel_cache_paths(signal_name, cache_dir=cache_dir)
    if not paths["panel"].exists() or not paths["metadata"].exists():
        raise FileNotFoundError(f"Panel cache missing for signal_name={signal_name!r}.")
    panel = pd.read_parquet(paths["panel"])
    panel.index = pd.to_datetime(panel.index, errors="raise")
    panel = panel.sort_index().sort_index(axis=1)
    panel.columns.name = None
    if validate_checksum:
        metadata = _read_metadata(paths["metadata"])
        checksum = _panel_checksum(panel)
        if checksum != metadata.get("checksum_sha256"):
            raise ValueError(
                f"Panel cache checksum mismatch for signal_name={signal_name!r}: "
                f"{checksum} != {metadata.get('checksum_sha256')}"
            )
    return panel


def build_signal_panel_cache(
    signal_names: list[str] | tuple[str, ...] | pd.Series,
    source_table: str = DEFAULT_SOURCE_TABLE,
    db_path: str | Path | None = None,
    cache_dir: str | Path | None = None,
    force: bool = False,
    chunksize: int = 500_000,
    verbose: bool = True,
) -> pd.DataFrame:
    """Build Parquet panel cache artifacts for selected signal names."""
    if not parquet_supported():
        raise ImportError("Parquet support requires pyarrow or fastparquet.")

    requested_signal_names = (
        pd.Series(signal_names, dtype="object").dropna().astype(str).drop_duplicates().tolist()
    )
    output_dir = _cache_dir(cache_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    source_metadata_by_signal = _source_signal_metadata_by_names(
        requested_signal_names,
        source_table=source_table,
        db_path=db_path,
    )

    for index, signal_name in enumerate(requested_signal_names, start=1):
        paths = panel_cache_paths(signal_name, cache_dir=output_dir)
        source_metadata = source_metadata_by_signal.get(signal_name)
        if source_metadata is None:
            raise ValueError(f"signal_name {signal_name!r} not found in {source_table}.")
        if (
            not force
            and paths["panel"].exists()
            and paths["metadata"].exists()
            and _metadata_matches_source(_read_metadata(paths["metadata"]), signal_name, source_table, source_metadata)
        ):
            metadata = _read_metadata(paths["metadata"])
            metadata["cache_status"] = "fresh_existing"
            rows.append(metadata)
            if verbose:
                print(f"panel_cache: {index}/{len(requested_signal_names)} {signal_name} fresh")
            continue

        if verbose:
            print(f"panel_cache: {index}/{len(requested_signal_names)} building {signal_name}")
        quiet_context = nullcontext() if verbose else redirect_stdout(StringIO())
        with quiet_context:
            signal_long = load_candidate_signals_by_names(
                [signal_name],
                current=(source_table == DEFAULT_SOURCE_TABLE),
                db_path=db_path,
                chunksize=chunksize,
            )
            validate_signal_date_quality(
                signal_long,
                context=f"panel_cache[{signal_name}]",
                max_null_rate=0.0,
            )
            validate_signal_long_uniqueness(
                signal_long,
                key_cols=["signal_name", "Date", "ticker"],
                strict=True,
                context=f"panel_cache[{signal_name}]",
            )
            panel = pivot_signal_long_to_panel(signal_long, signal_name, duplicate_policy="raise")
        panel.to_parquet(paths["panel"], index=True)
        metadata = _metadata_for_panel(
            signal_name=signal_name,
            panel=panel,
            source_metadata=source_metadata,
            source_table=source_table,
            panel_path=paths["panel"],
        )
        metadata["cache_status"] = "rebuilt"
        _write_metadata(metadata, paths["metadata"])
        rows.append(metadata)

    return pd.DataFrame(rows)


def validate_signal_panel_cache(
    signal_names: list[str] | tuple[str, ...] | pd.Series,
    source_table: str = DEFAULT_SOURCE_TABLE,
    db_path: str | Path | None = None,
    cache_dir: str | Path | None = None,
    validate_checksum: bool = False,
) -> pd.DataFrame:
    """Validate existence, freshness, and optionally checksum for selected panel caches."""
    requested_signal_names = (
        pd.Series(signal_names, dtype="object").dropna().astype(str).drop_duplicates().tolist()
    )
    source_metadata_by_signal = _source_signal_metadata_by_names(
        requested_signal_names,
        source_table=source_table,
        db_path=db_path,
    )
    rows: list[dict[str, object]] = []
    for signal_name in requested_signal_names:
        paths = panel_cache_paths(signal_name, cache_dir=cache_dir)
        exists = paths["panel"].exists() and paths["metadata"].exists()
        fresh = False
        error = ""
        try:
            if signal_name not in source_metadata_by_signal:
                raise ValueError(f"signal_name {signal_name!r} not found in {source_table}.")
            if exists:
                fresh = _metadata_matches_source(
                    _read_metadata(paths["metadata"]),
                    signal_name,
                    source_table,
                    source_metadata_by_signal[signal_name],
                )
            if exists and validate_checksum:
                load_signal_panel_from_cache(
                    signal_name,
                    cache_dir=cache_dir,
                    validate_checksum=True,
                )
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        rows.append(
            {
                "signal_name": signal_name,
                "panel_path": str(paths["panel"]),
                "metadata_path": str(paths["metadata"]),
                "exists": exists,
                "fresh": fresh,
                "error": error,
            }
        )
    return pd.DataFrame(rows)


def load_signal_panels_from_cache(
    signal_names: list[str] | tuple[str, ...] | pd.Series,
    cache_dir: str | Path | None = None,
    validate_checksum: bool = False,
) -> dict[str, pd.DataFrame]:
    return {
        str(signal_name): load_signal_panel_from_cache(
            str(signal_name),
            cache_dir=cache_dir,
            validate_checksum=validate_checksum,
        )
        for signal_name in pd.Series(signal_names, dtype="object").dropna().astype(str).drop_duplicates()
    }


__all__ = [
    "DEFAULT_PANEL_CACHE_DIR",
    "DEFAULT_SOURCE_TABLE",
    "PANEL_CACHE_METADATA_VERSION",
    "build_signal_panel_cache",
    "cache_is_fresh",
    "load_signal_panel_from_cache",
    "load_signal_panels_from_cache",
    "panel_cache_paths",
    "parquet_supported",
    "validate_signal_panel_cache",
]
