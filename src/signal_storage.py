from __future__ import annotations

import sqlite3
import time
import gc
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path
from src.signal_quality import build_signal_family_summary, filter_signal_quality


SIGNAL_TABLES = {
    "signals": ("candidate_signals_current", "candidate_signals_history"),
    "metadata": ("candidate_signal_metadata_current", "candidate_signal_metadata_history"),
    "quality": ("candidate_signal_quality_current", "candidate_signal_quality_history"),
    "quality_gate": ("candidate_signal_quality_gate_current", "candidate_signal_quality_gate_history"),
    "family_summary": ("candidate_signal_family_summary_current", "candidate_signal_family_summary_history"),
}


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    query = """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
    """
    return conn.execute(query, (table_name,)).fetchone() is not None


def _sqlite_type_for_series(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    return "TEXT"


def _ensure_sqlite_columns(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
) -> None:
    existing_columns = {
        row[1]
        for row in conn.execute(f"PRAGMA table_info({_quote_identifier(table_name)})").fetchall()
    }
    missing_columns = [column for column in df.columns if column not in existing_columns]
    for column in missing_columns:
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(column)} {_sqlite_type_for_series(df[column])}"
        )


def signals_to_long(
    signals: dict[str, pd.DataFrame],
    run_id: str,
    signal_version: str,
) -> pd.DataFrame:
    """Convert signal panels into SQLite long format."""
    long_frames: list[pd.DataFrame] = []

    for signal_name, signal_df in signals.items():
        panel = signal_df.copy()
        panel.index.name = "Date"
        panel.columns.name = "ticker"

        long_signal = (
            panel.stack(future_stack=True)
            .rename("signal_value")
            .reset_index()
        )
        long_signal["signal_name"] = signal_name
        long_signal["run_id"] = run_id
        long_signal["signal_version"] = signal_version
        long_frames.append(long_signal)

    if not long_frames:
        return pd.DataFrame(
            columns=["Date", "ticker", "signal_name", "signal_value", "run_id", "signal_version"]
        )

    output = pd.concat(long_frames, ignore_index=True)
    return output[["Date", "ticker", "signal_name", "signal_value", "run_id", "signal_version"]]


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _resolve_table_name(table_key: str, current: bool) -> str:
    current_table, history_table = SIGNAL_TABLES[table_key]
    return current_table if current else history_table


def _load_sqlite_table(
    table_name: str,
    db_path: str | Path | None = None,
    parse_date_columns: tuple[str, ...] = (),
) -> pd.DataFrame:
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)

    for date_column in parse_date_columns:
        if date_column in df.columns:
            df[date_column] = pd.to_datetime(df[date_column], errors="raise", format="mixed")
    return df


def _memory_usage_mb() -> float | None:
    try:
        import psutil  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


def _duplicate_diagnostics(
    df: pd.DataFrame,
    key_cols: list[str],
    context: str,
    sample_size: int = 5,
) -> tuple[int, int, pd.DataFrame]:
    duplicate_mask = df.duplicated(key_cols, keep=False)
    duplicate_rows = df.loc[duplicate_mask].copy()
    duplicate_groups = (
        duplicate_rows.groupby(key_cols, dropna=False)
        .size()
        .reset_index(name="duplicate_count")
        .sort_values("duplicate_count", ascending=False)
    )
    n_duplicate_rows = int(duplicate_mask.sum())
    n_duplicate_groups = int(len(duplicate_groups))
    examples = duplicate_rows.merge(
        duplicate_groups.head(sample_size),
        on=key_cols,
        how="inner",
    ).sort_values(key_cols).head(sample_size)

    print(
        f"{context} duplicate diagnostics for {key_cols}: "
        f"duplicate_rows={n_duplicate_rows:,}, duplicate_groups={n_duplicate_groups:,}"
    )
    if not examples.empty:
        print(f"{context} duplicate examples:")
        print(examples.to_string(index=False))
    return n_duplicate_rows, n_duplicate_groups, examples


def validate_signal_long_uniqueness(
    signal_df: pd.DataFrame,
    key_cols: list[str] | None = None,
    strict: bool = True,
    context: str = "signal_long",
) -> pd.DataFrame:
    """Validate that long-format signal rows are unique at the requested key."""
    resolved_key_cols = key_cols if key_cols is not None else ["signal_name", "Date", "ticker"]
    missing_columns = [column for column in resolved_key_cols if column not in signal_df.columns]
    if missing_columns:
        raise ValueError(
            f"{context} is missing required uniqueness key columns: {missing_columns}"
        )

    duplicate_mask = signal_df.duplicated(resolved_key_cols, keep=False)
    if not duplicate_mask.any():
        print(
            f"{context} duplicate diagnostics for {resolved_key_cols}: "
            "duplicate_rows=0, duplicate_groups=0"
        )
        return pd.DataFrame(columns=resolved_key_cols + ["duplicate_count"])

    n_duplicate_rows, n_duplicate_groups, _ = _duplicate_diagnostics(
        signal_df,
        resolved_key_cols,
        context,
    )
    duplicate_counts = (
        signal_df.loc[duplicate_mask]
        .groupby(resolved_key_cols, dropna=False)
        .size()
        .reset_index(name="duplicate_count")
        .sort_values("duplicate_count", ascending=False)
    )
    if strict:
        raise ValueError(
            f"{context} contains duplicate rows at key {resolved_key_cols}: "
            f"duplicate_rows={n_duplicate_rows:,}, duplicate_groups={n_duplicate_groups:,}"
        )
    return duplicate_counts


def validate_signal_date_quality(
    signal_df: pd.DataFrame,
    context: str = "",
    max_null_rate: float = 0.0,
) -> pd.DataFrame:
    """Validate Date quality for long-format signal panels."""
    required_columns = ["signal_name", "Date", "ticker"]
    missing_columns = [column for column in required_columns if column not in signal_df.columns]
    resolved_context = context or "signal_long"
    if missing_columns:
        raise ValueError(
            f"{resolved_context} is missing required Date quality columns: {missing_columns}"
        )

    date_quality = (
        signal_df.groupby("signal_name", dropna=False)
        .agg(
            rows=("signal_name", "size"),
            date_nulls=("Date", lambda values: int(values.isna().sum())),
            unique_dates=("Date", "nunique"),
            unique_tickers=("ticker", "nunique"),
        )
        .reset_index()
    )
    date_quality["date_null_rate"] = (
        date_quality["date_nulls"] / date_quality["rows"].where(date_quality["rows"].ne(0), 1)
    )
    date_quality = date_quality.sort_values(
        ["date_nulls", "signal_name"],
        ascending=[False, True],
    )

    print(f"{resolved_context} Date quality by signal_name:")
    print(date_quality.to_string(index=False))

    failing = date_quality.loc[date_quality["date_null_rate"] > max_null_rate]
    if not failing.empty:
        raise ValueError(
            f"{resolved_context} has Date nulls above max_null_rate={max_null_rate:.2%}: "
            f"{failing[['signal_name', 'rows', 'date_nulls', 'date_null_rate']].to_dict('records')}"
        )
    return date_quality


def load_candidate_signals(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate signals in long format from SQLite."""
    return _load_sqlite_table(
        _resolve_table_name("signals", current=current),
        db_path=db_path,
        parse_date_columns=("Date",),
    )


def load_candidate_signals_by_names(
    signal_names: list[str] | tuple[str, ...] | pd.Series,
    current: bool = True,
    db_path: str | Path | None = None,
    chunksize: int | None = None,
) -> pd.DataFrame:
    """Load selected candidate signals in long format from SQLite by signal_name."""
    requested_signal_names = pd.Series(signal_names, dtype="object").dropna().astype(str)
    unique_signal_names = requested_signal_names.drop_duplicates().tolist()
    table_name = _resolve_table_name("signals", current=current)
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()

    start_time = time.perf_counter()
    memory_before_mb = _memory_usage_mb()

    with sqlite3.connect(db_path) as conn:
        if not unique_signal_names:
            query = f"SELECT * FROM {_quote_identifier(table_name)} WHERE 1 = 0"
            output = pd.read_sql_query(query, conn)
        else:
            placeholders = ",".join("?" for _ in unique_signal_names)
            query = (
                f"SELECT * FROM {_quote_identifier(table_name)} "
                f"WHERE signal_name IN ({placeholders})"
            )
            if chunksize is None:
                output = pd.read_sql_query(query, conn, params=unique_signal_names)
            else:
                chunks = pd.read_sql_query(
                    query,
                    conn,
                    params=unique_signal_names,
                    chunksize=chunksize,
                )
                chunk_frames = []
                for chunk_index, chunk in enumerate(chunks, start=1):
                    chunk_signal_names = (
                        chunk["signal_name"].dropna().astype(str).drop_duplicates().tolist()
                        if "signal_name" in chunk.columns
                        else []
                    )
                    if "Date" in chunk.columns:
                        raw_date_sample = chunk["Date"].head(5).tolist()
                        try:
                            chunk["Date"] = pd.to_datetime(
                                chunk["Date"],
                                errors="raise",
                                format="mixed",
                            )
                        except Exception as exc:
                            raise ValueError(
                                "Failed to parse Date in "
                                f"load_candidate_signals_by_names chunk {chunk_index} "
                                f"for signals={chunk_signal_names}; "
                                f"raw Date sample={raw_date_sample}"
                            ) from exc
                        chunk_date_nulls = int(chunk["Date"].isna().sum())
                    else:
                        chunk_date_nulls = 0
                    print(
                        "load_candidate_signals_by_names chunk "
                        f"{chunk_index}: signals={chunk_signal_names}, "
                        f"rows={len(chunk):,}, Date nulls={chunk_date_nulls:,}"
                    )
                    chunk_frames.append(chunk)
                output = (
                    pd.concat(chunk_frames, ignore_index=True)
                    if chunk_frames
                    else pd.read_sql_query(
                        f"SELECT * FROM {_quote_identifier(table_name)} WHERE 1 = 0",
                        conn,
                    )
                )

    if "Date" in output.columns:
        output["Date"] = pd.to_datetime(output["Date"], errors="raise", format="mixed")

    elapsed_seconds = time.perf_counter() - start_time
    memory_after_mb = _memory_usage_mb()
    memory_message = ""
    if memory_before_mb is not None and memory_after_mb is not None:
        memory_message = (
            f", memory_before_mb={memory_before_mb:,.1f}, "
            f"memory_after_mb={memory_after_mb:,.1f}"
        )
    print(
        f"load_candidate_signals_by_names: table={table_name}, "
        f"requested_signal_names={len(unique_signal_names):,}, "
        f"rows_returned={len(output):,}, elapsed_seconds={elapsed_seconds:.3f}"
        f"{memory_message}"
    )
    return output


def load_and_pivot_signal_panels_by_names(
    signal_names: list[str] | tuple[str, ...] | pd.Series,
    current: bool = True,
    db_path: str | Path | None = None,
    duplicate_policy: str = "raise",
    chunksize: int = 500_000,
    memory_warning_mb: float = 10_000,
) -> dict[str, pd.DataFrame]:
    """Load, validate, and pivot selected signals one at a time."""
    requested_signal_names = (
        pd.Series(signal_names, dtype="object")
        .dropna()
        .astype(str)
        .drop_duplicates()
        .tolist()
    )
    signal_panels: dict[str, pd.DataFrame] = {}
    overall_start = time.perf_counter()

    for index, signal_name in enumerate(requested_signal_names, start=1):
        signal_start = time.perf_counter()
        signal_long = load_candidate_signals_by_names(
            [signal_name],
            current=current,
            db_path=db_path,
            chunksize=chunksize,
        )
        load_elapsed = time.perf_counter() - signal_start

        validate_signal_long_uniqueness(
            signal_long,
            key_cols=["signal_name", "Date", "ticker"],
            strict=True,
            context=f"approved_signal_long[{signal_name}]",
        )

        pivot_start = time.perf_counter()
        signal_panels[signal_name] = pivot_signal_long_to_panel(
            signal_long,
            signal_name,
            duplicate_policy=duplicate_policy,
        )
        pivot_elapsed = time.perf_counter() - pivot_start

        del signal_long
        gc.collect()
        memory_after_mb = _memory_usage_mb()
        memory_message = (
            f", memory_after_mb={memory_after_mb:,.1f}"
            if memory_after_mb is not None
            else ""
        )
        print(
            f"load_and_pivot_signal_panels_by_names: "
            f"signal={index:,}/{len(requested_signal_names):,} {signal_name}, "
            f"load_seconds={load_elapsed:.3f}, pivot_seconds={pivot_elapsed:.3f}, "
            f"panel_shape={signal_panels[signal_name].shape}{memory_message}"
        )
        if memory_after_mb is not None and memory_after_mb > memory_warning_mb:
            print(
                "WARNING: load_and_pivot_signal_panels_by_names RSS memory "
                f"{memory_after_mb:,.1f} MB exceeds threshold "
                f"{memory_warning_mb:,.1f} MB after signal '{signal_name}'."
            )

    total_elapsed = time.perf_counter() - overall_start
    final_memory_mb = _memory_usage_mb()
    final_memory_message = (
        f", final_memory_mb={final_memory_mb:,.1f}"
        if final_memory_mb is not None
        else ""
    )
    print(
        f"load_and_pivot_signal_panels_by_names: "
        f"panels_built={len(signal_panels):,}, "
        f"elapsed_seconds={total_elapsed:.3f}"
        f"{final_memory_message}"
    )
    return signal_panels


def load_candidate_signal_metadata(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate signal metadata from SQLite."""
    return _load_sqlite_table(
        _resolve_table_name("metadata", current=current),
        db_path=db_path,
        parse_date_columns=("created_timestamp",),
    )


def load_candidate_signal_quality(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate signal quality from SQLite."""
    return _load_sqlite_table(
        _resolve_table_name("quality", current=current),
        db_path=db_path,
        parse_date_columns=("first_valid_date", "last_valid_date"),
    )


def load_candidate_signal_quality_gate(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate signal quality gate results from SQLite."""
    return _load_sqlite_table(
        _resolve_table_name("quality_gate", current=current),
        db_path=db_path,
        parse_date_columns=("first_valid_date", "last_valid_date"),
    )


def load_candidate_signal_family_summary(
    current: bool = True,
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate signal family summary from SQLite."""
    return _load_sqlite_table(
        _resolve_table_name("family_summary", current=current),
        db_path=db_path,
        parse_date_columns=("min_first_valid_date", "max_first_valid_date"),
    )


def pivot_signal_long_to_panel(
    signal_df: pd.DataFrame,
    signal_name: str,
    duplicate_policy: str = "raise",
) -> pd.DataFrame:
    """Pivot one long-format signal into a Date x ticker panel."""
    valid_duplicate_policies = {"raise", "last", "mean"}
    if duplicate_policy not in valid_duplicate_policies:
        raise ValueError(
            f"duplicate_policy must be one of {sorted(valid_duplicate_policies)}; "
            f"got {duplicate_policy!r}."
        )

    required_columns = {"Date", "ticker", "signal_name", "signal_value"}
    missing_columns = required_columns.difference(signal_df.columns)
    if missing_columns:
        raise ValueError(f"signal_df is missing required columns: {sorted(missing_columns)}")

    signal_df_for_validation = signal_df.copy()
    signal_df_for_validation["Date"] = pd.to_datetime(
        signal_df_for_validation["Date"],
        errors="coerce",
    )
    approved_duplicate_counts = validate_signal_long_uniqueness(
        signal_df_for_validation,
        key_cols=["signal_name", "Date", "ticker"],
        strict=False,
        context="approved_signal_long",
    )

    selected = signal_df.loc[signal_df["signal_name"] == signal_name].copy()
    if selected.empty:
        raise ValueError(f"signal_name '{signal_name}' not found in signal_df.")

    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["signal_value"] = pd.to_numeric(selected["signal_value"], errors="coerce")
    pivot_duplicate_mask = selected.duplicated(["Date", "ticker"], keep=False)
    if pivot_duplicate_mask.any():
        n_duplicate_rows, n_duplicate_groups, _ = _duplicate_diagnostics(
            selected,
            ["Date", "ticker"],
            f"pivot_signal_long_to_panel({signal_name})",
        )
        if duplicate_policy == "raise":
            raise ValueError(
                f"Cannot pivot signal_name '{signal_name}' because duplicate Date/ticker "
                f"rows were found: duplicate_rows={n_duplicate_rows:,}, "
                f"duplicate_groups={n_duplicate_groups:,}. "
                "Use duplicate_policy='last' for temporary recovery or "
                "duplicate_policy='mean' only when averaging duplicates is intended."
            )
        if duplicate_policy == "last":
            print(
                f"WARNING: duplicate_policy='last' is dropping duplicate rows for "
                f"signal_name '{signal_name}' and keeping the last row per Date/ticker."
            )
            selected = selected.drop_duplicates(["Date", "ticker"], keep="last")
        elif duplicate_policy == "mean":
            print(
                f"WARNING: duplicate_policy='mean' is averaging duplicate signal_value "
                f"rows for signal_name '{signal_name}'."
            )
            selected = (
                selected.groupby(["Date", "ticker"], dropna=False, as_index=False)["signal_value"]
                .mean()
            )
    elif duplicate_policy == "raise" and not approved_duplicate_counts.empty:
        raise ValueError(
            "approved_signal_long contains duplicate signal_name/Date/ticker rows. "
            "See duplicate diagnostics above."
        )

    panel = selected.pivot(index="Date", columns="ticker", values="signal_value")
    panel = panel.sort_index().sort_index(axis=1)
    panel.columns.name = None
    return panel


def save_signal_factory_outputs(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    quality: pd.DataFrame,
    quality_gate: pd.DataFrame | None = None,
    family_summary: pd.DataFrame | None = None,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    signal_version: str | None = None,
) -> dict[str, Path]:
    """Write candidate signals, metadata, and quality outputs to SQLite."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_run_id = run_id if run_id is not None else str(metadata["run_id"].iloc[0])
    resolved_signal_version = (
        signal_version if signal_version is not None else str(metadata["signal_version"].iloc[0])
    )
    signals_long = signals_to_long(
        signals=signals,
        run_id=resolved_run_id,
        signal_version=resolved_signal_version,
    )
    validate_signal_long_uniqueness(
        signals_long,
        key_cols=["signal_name", "Date", "ticker"],
        strict=True,
        context="candidate_signals_current write",
    )
    if quality_gate is None:
        approved_quality, rejected_quality = filter_signal_quality(quality)
        quality_gate = pd.concat([approved_quality, rejected_quality], ignore_index=True)
    if family_summary is None:
        family_summary = build_signal_family_summary(quality)

    with sqlite3.connect(db_path) as conn:
        _write_sqlite_table(signals_long, SIGNAL_TABLES["signals"][0], conn, if_exists="replace")
        _write_sqlite_table(signals_long, SIGNAL_TABLES["signals"][1], conn, if_exists="append")
        _write_sqlite_table(metadata, SIGNAL_TABLES["metadata"][0], conn, if_exists="replace")
        _write_sqlite_table(metadata, SIGNAL_TABLES["metadata"][1], conn, if_exists="append")
        _write_sqlite_table(quality, SIGNAL_TABLES["quality"][0], conn, if_exists="replace")
        _write_sqlite_table(quality, SIGNAL_TABLES["quality"][1], conn, if_exists="append")
        _write_sqlite_table(quality_gate, SIGNAL_TABLES["quality_gate"][0], conn, if_exists="replace")
        _write_sqlite_table(quality_gate, SIGNAL_TABLES["quality_gate"][1], conn, if_exists="append")
        _write_sqlite_table(family_summary, SIGNAL_TABLES["family_summary"][0], conn, if_exists="replace")
        _write_sqlite_table(family_summary, SIGNAL_TABLES["family_summary"][1], conn, if_exists="append")

    return {name: db_path for name in SIGNAL_TABLES}


__all__ = [
    "SIGNAL_TABLES",
    "load_candidate_signal_family_summary",
    "load_candidate_signal_metadata",
    "load_candidate_signal_quality",
    "load_candidate_signal_quality_gate",
    "load_and_pivot_signal_panels_by_names",
    "load_candidate_signals",
    "load_candidate_signals_by_names",
    "pivot_signal_long_to_panel",
    "save_signal_factory_outputs",
    "signals_to_long",
    "validate_signal_date_quality",
    "validate_signal_long_uniqueness",
]
