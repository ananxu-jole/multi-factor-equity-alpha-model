"""Read-through Parquet cache for full-universe signal daily IC series."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd

from src.run_config import get_project_root
from src.scoring.panel_cache import parquet_supported


DAILY_IC_CACHE_METADATA_VERSION = "signal_daily_ic_cache_v1"
DEFAULT_DAILY_IC_CACHE_DIR = get_project_root() / "artifacts" / "ic"
DEFAULT_SOURCE_TABLE = "candidate_signals_current"


def _safe_path_part(value: str) -> str:
    quoted = quote(str(value), safe="")
    return re.sub(r"[^A-Za-z0-9_.%-]", "_", quoted)


def _cache_dir(cache_dir: str | Path | None = None) -> Path:
    return Path(cache_dir) if cache_dir is not None else DEFAULT_DAILY_IC_CACHE_DIR


def panel_checksum(panel: pd.DataFrame) -> str:
    normalized = panel.copy()
    normalized.index = pd.to_datetime(normalized.index, errors="raise")
    normalized = normalized.sort_index().sort_index(axis=1)
    hashed = pd.util.hash_pandas_object(normalized, index=True).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()


def forward_return_config_hash(forward_returns_panel: pd.DataFrame, horizon: int) -> str:
    index = pd.to_datetime(forward_returns_panel.index, errors="raise")
    payload = {
        "horizon": int(horizon),
        "date_min": index.min().strftime("%Y-%m-%d") if len(index) else None,
        "date_max": index.max().strftime("%Y-%m-%d") if len(index) else None,
        "n_dates": int(len(index)),
        "columns": [str(column) for column in forward_returns_panel.columns],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def daily_ic_config_hash(
    signal_name: str,
    horizon: int,
    ic_method: str,
    panel_checksum_sha256: str,
    forward_config_hash: str,
    source_table: str = DEFAULT_SOURCE_TABLE,
    universe_version: str | None = None,
) -> str:
    payload = {
        "signal_name": signal_name,
        "horizon": int(horizon),
        "ic_method": ic_method,
        "panel_checksum_sha256": panel_checksum_sha256,
        "forward_return_config_hash": forward_config_hash,
        "source_table": source_table,
        "universe_version": universe_version,
        "metadata_version": DAILY_IC_CACHE_METADATA_VERSION,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def daily_ic_cache_paths(
    signal_name: str,
    horizon: int,
    ic_method: str,
    config_hash: str,
    cache_dir: str | Path | None = None,
) -> dict[str, Path]:
    base = (
        _cache_dir(cache_dir)
        / "signal"
        / _safe_path_part(signal_name)
        / f"h{int(horizon)}"
        / _safe_path_part(ic_method)
    )
    return {
        "daily_ic": base / f"{config_hash}.parquet",
        "metadata": base / f"{config_hash}.metadata.json",
    }


def _read_metadata(metadata_path: Path) -> dict[str, object]:
    return json.loads(metadata_path.read_text())


def _write_metadata(metadata: dict[str, object], metadata_path: Path) -> None:
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def _metadata_for_daily_ic(
    daily_ic: pd.DataFrame,
    signal_name: str,
    horizon: int,
    ic_method: str,
    config_hash: str,
    panel_checksum_sha256: str,
    forward_config_hash: str,
    source_table: str,
    universe_version: str | None,
    cache_path: Path,
) -> dict[str, object]:
    dates = pd.to_datetime(daily_ic["Date"], errors="raise") if not daily_ic.empty else pd.Series(dtype="datetime64[ns]")
    return {
        "metadata_version": DAILY_IC_CACHE_METADATA_VERSION,
        "signal_name": signal_name,
        "horizon": int(horizon),
        "ic_method": ic_method,
        "source_table": source_table,
        "universe_version": universe_version,
        "panel_checksum_sha256": panel_checksum_sha256,
        "forward_return_config_hash": forward_config_hash,
        "config_hash": config_hash,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "date_min": dates.min().strftime("%Y-%m-%d") if len(dates) else None,
        "date_max": dates.max().strftime("%Y-%m-%d") if len(dates) else None,
        "n_dates": int(len(daily_ic)),
        "cache_path": str(cache_path),
    }


def _metadata_matches(
    metadata: dict[str, object],
    daily_ic: pd.DataFrame | None,
    signal_name: str,
    horizon: int,
    ic_method: str,
    config_hash: str,
    panel_checksum_sha256: str,
    forward_config_hash: str,
    source_table: str,
) -> bool:
    if (
        metadata.get("metadata_version") != DAILY_IC_CACHE_METADATA_VERSION
        or metadata.get("signal_name") != signal_name
        or int(metadata.get("horizon") or -1) != int(horizon)
        or metadata.get("ic_method") != ic_method
        or metadata.get("config_hash") != config_hash
        or metadata.get("panel_checksum_sha256") != panel_checksum_sha256
        or metadata.get("forward_return_config_hash") != forward_config_hash
        or metadata.get("source_table") != source_table
    ):
        return False
    if daily_ic is None:
        return True
    dates = pd.to_datetime(daily_ic["Date"], errors="raise") if not daily_ic.empty else pd.Series(dtype="datetime64[ns]")
    return (
        int(metadata.get("n_dates") or -1) == int(len(daily_ic))
        and metadata.get("date_min") == (dates.min().strftime("%Y-%m-%d") if len(dates) else None)
        and metadata.get("date_max") == (dates.max().strftime("%Y-%m-%d") if len(dates) else None)
    )


def load_daily_ic_cache(
    signal_name: str,
    horizon: int,
    ic_method: str,
    config_hash: str,
    panel_checksum_sha256: str,
    forward_config_hash: str,
    source_table: str = DEFAULT_SOURCE_TABLE,
    cache_dir: str | Path | None = None,
) -> pd.DataFrame | None:
    if not parquet_supported():
        raise ImportError("Parquet support requires pyarrow or fastparquet.")
    paths = daily_ic_cache_paths(signal_name, horizon, ic_method, config_hash, cache_dir=cache_dir)
    if not paths["daily_ic"].exists() or not paths["metadata"].exists():
        return None
    metadata = _read_metadata(paths["metadata"])
    if not _metadata_matches(
        metadata,
        None,
        signal_name,
        horizon,
        ic_method,
        config_hash,
        panel_checksum_sha256,
        forward_config_hash,
        source_table,
    ):
        return None
    daily_ic = pd.read_parquet(paths["daily_ic"])
    daily_ic["Date"] = pd.to_datetime(daily_ic["Date"], errors="raise")
    daily_ic = daily_ic.sort_values("Date", kind="mergesort").reset_index(drop=True)
    if not _metadata_matches(
        metadata,
        daily_ic,
        signal_name,
        horizon,
        ic_method,
        config_hash,
        panel_checksum_sha256,
        forward_config_hash,
        source_table,
    ):
        return None
    return daily_ic


def write_daily_ic_cache(
    daily_ic: pd.DataFrame,
    signal_name: str,
    horizon: int,
    ic_method: str,
    config_hash: str,
    panel_checksum_sha256: str,
    forward_config_hash: str,
    source_table: str = DEFAULT_SOURCE_TABLE,
    universe_version: str | None = None,
    cache_dir: str | Path | None = None,
) -> dict[str, Path]:
    if not parquet_supported():
        raise ImportError("Parquet support requires pyarrow or fastparquet.")
    paths = daily_ic_cache_paths(signal_name, horizon, ic_method, config_hash, cache_dir=cache_dir)
    paths["daily_ic"].parent.mkdir(parents=True, exist_ok=True)
    output = daily_ic.copy()
    output["Date"] = pd.to_datetime(output["Date"], errors="raise")
    output = output.sort_values("Date", kind="mergesort").reset_index(drop=True)
    output.to_parquet(paths["daily_ic"], index=False)
    metadata = _metadata_for_daily_ic(
        daily_ic=output,
        signal_name=signal_name,
        horizon=horizon,
        ic_method=ic_method,
        config_hash=config_hash,
        panel_checksum_sha256=panel_checksum_sha256,
        forward_config_hash=forward_config_hash,
        source_table=source_table,
        universe_version=universe_version,
        cache_path=paths["daily_ic"],
    )
    _write_metadata(metadata, paths["metadata"])
    return paths


def daily_ic_frame_from_series(
    daily_ic: pd.Series,
    signal_name: str,
    horizon: int,
    ic_method: str,
    n_pairs: pd.Series | None = None,
    source_table: str = DEFAULT_SOURCE_TABLE,
    universe_version: str | None = None,
    panel_checksum_sha256: str | None = None,
    forward_config_hash: str | None = None,
    config_hash: str | None = None,
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "signal_name": signal_name,
            "Date": pd.to_datetime(daily_ic.index, errors="raise"),
            "horizon": int(horizon),
            "ic_method": ic_method,
            "daily_ic": pd.to_numeric(daily_ic.to_numpy(), errors="coerce"),
        }
    )
    if n_pairs is None:
        frame["n_pairs"] = np.nan
    else:
        aligned_pairs = n_pairs.reindex(daily_ic.index)
        frame["n_pairs"] = pd.to_numeric(aligned_pairs.to_numpy(), errors="coerce")
    frame["universe_version"] = universe_version
    frame["source_table"] = source_table
    frame["panel_checksum_sha256"] = panel_checksum_sha256
    frame["forward_return_config_hash"] = forward_config_hash
    frame["config_hash"] = config_hash
    frame["created_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return frame


def daily_ic_series_from_frame(daily_ic: pd.DataFrame) -> pd.Series:
    frame = daily_ic.copy()
    frame["Date"] = pd.to_datetime(frame["Date"], errors="raise")
    series = pd.Series(
        pd.to_numeric(frame["daily_ic"], errors="coerce").to_numpy(),
        index=frame["Date"],
        name="ic",
    )
    return series.sort_index()


__all__ = [
    "DAILY_IC_CACHE_METADATA_VERSION",
    "DEFAULT_DAILY_IC_CACHE_DIR",
    "DEFAULT_SOURCE_TABLE",
    "daily_ic_cache_paths",
    "daily_ic_config_hash",
    "daily_ic_frame_from_series",
    "daily_ic_series_from_frame",
    "forward_return_config_hash",
    "load_daily_ic_cache",
    "panel_checksum",
    "write_daily_ic_cache",
]
