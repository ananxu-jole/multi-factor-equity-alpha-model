from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


ORTHOGONAL_SIGNAL_TABLES = {
    "signals": ("orthogonal_candidate_signals_current", "orthogonal_candidate_signals_history"),
    "metadata": ("orthogonal_candidate_metadata_current", "orthogonal_candidate_metadata_history"),
    "quality": ("orthogonal_candidate_quality_current", "orthogonal_candidate_quality_history"),
    "family_summary": (
        "orthogonal_candidate_family_summary_current",
        "orthogonal_candidate_family_summary_history",
    ),
    "integration_report": (
        "orthogonal_signal_integration_report_current",
        "orthogonal_signal_integration_report_history",
    ),
}

MAIN_SIGNAL_TABLES = {
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


def _ensure_sqlite_columns(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection) -> None:
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


def _write_sqlite_table(
    df: pd.DataFrame,
    table_name: str,
    conn: sqlite3.Connection,
    if_exists: str,
) -> None:
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(df, table_name, conn)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def orthogonal_signals_to_long(
    signals: dict[str, pd.DataFrame],
    run_id: str,
    orthogonal_version: str,
) -> pd.DataFrame:
    """Convert orthogonal signal panels into long SQLite format."""
    long_frames: list[pd.DataFrame] = []
    for signal_name, signal_df in signals.items():
        panel = signal_df.copy()
        panel.index.name = "Date"
        panel.columns.name = "ticker"
        long_signal = panel.stack(future_stack=True).rename("signal_value").reset_index()
        long_signal["signal_name"] = signal_name
        long_signal["run_id"] = run_id
        long_signal["orthogonal_version"] = orthogonal_version
        long_signal["signal_source"] = "orthogonal_generated"
        long_frames.append(long_signal)

    if not long_frames:
        return pd.DataFrame(
            columns=[
                "Date",
                "ticker",
                "signal_name",
                "signal_value",
                "run_id",
                "orthogonal_version",
                "signal_source",
            ]
        )

    output = pd.concat(long_frames, ignore_index=True)
    return output[
        ["Date", "ticker", "signal_name", "signal_value", "run_id", "orthogonal_version", "signal_source"]
    ]


def save_orthogonal_signal_outputs(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    quality: pd.DataFrame,
    family_summary: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    orthogonal_version: str | None = None,
) -> dict[str, Path]:
    """Write orthogonal signal outputs to separate current/history SQLite tables."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    resolved_run_id = run_id if run_id is not None else str(metadata["run_id"].iloc[0])
    resolved_version = (
        orthogonal_version
        if orthogonal_version is not None
        else str(metadata["orthogonal_version"].iloc[0])
    )
    signals_long = orthogonal_signals_to_long(
        signals=signals,
        run_id=resolved_run_id,
        orthogonal_version=resolved_version,
    )

    with sqlite3.connect(db_path) as conn:
        for artifact, output in {
            "signals": signals_long,
            "metadata": metadata,
            "quality": quality,
            "family_summary": family_summary,
        }.items():
            current_table, history_table = ORTHOGONAL_SIGNAL_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")

    return {artifact: db_path for artifact in ORTHOGONAL_SIGNAL_TABLES}


def _read_sqlite_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(table_name)}", conn)


def _count_rows(conn: sqlite3.Connection, table_name: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) FROM {_quote_identifier(table_name)}").fetchone()[0])


def _count_distinct_signal_names(conn: sqlite3.Connection, table_name: str) -> int:
    return int(
        conn.execute(
            f"SELECT COUNT(DISTINCT signal_name) FROM {_quote_identifier(table_name)}"
        ).fetchone()[0]
    )


def _main_metadata_from_orthogonal(
    orthogonal_metadata: pd.DataFrame,
    main_columns: list[str],
    orthogonal_version: str,
) -> pd.DataFrame:
    output = orthogonal_metadata.copy()
    output["parameters"] = output["lookback"].apply(lambda value: f"lookback={value}")
    output["data_dependencies"] = output["required_inputs"]
    output["input_fields"] = output["required_inputs"]
    output["normalization_notes"] = output.get("normalization", "")
    output["signal_version"] = orthogonal_version
    output["timestamp"] = output.get("created_timestamp", pd.NA)
    output["notes"] = (
        "Generated by 02C Orthogonal Signal Factory and promoted to the main candidate universe."
    )
    output["signal_source"] = "orthogonal_generated"
    output["orthogonal_version"] = orthogonal_version
    for column in main_columns:
        if column not in output.columns:
            output[column] = ""
    return output.reindex(columns=main_columns)


def _main_quality_from_orthogonal(
    orthogonal_quality: pd.DataFrame,
    main_columns: list[str],
    orthogonal_version: str,
) -> pd.DataFrame:
    output = orthogonal_quality.copy()
    output["signal_version"] = orthogonal_version
    output["signal_source"] = "orthogonal_generated"
    output["orthogonal_version"] = orthogonal_version
    for column in main_columns:
        if column not in output.columns:
            output[column] = pd.NA
    return output.reindex(columns=main_columns)


def _build_main_family_summary(metadata: pd.DataFrame, quality: pd.DataFrame) -> pd.DataFrame:
    joined = quality.merge(
        metadata[["signal_name", "signal_family"]].drop_duplicates("signal_name"),
        on="signal_name",
        how="left",
        suffixes=("", "_metadata"),
    )
    if "signal_family_metadata" in joined.columns:
        joined["signal_family"] = joined["signal_family"].combine_first(joined["signal_family_metadata"])
    joined["first_valid_date"] = pd.to_datetime(joined["first_valid_date"], errors="coerce")
    joined["last_valid_date"] = pd.to_datetime(joined["last_valid_date"], errors="coerce")
    return (
        joined.groupby("signal_family", dropna=False)
        .agg(
            n_signals=("signal_name", "nunique"),
            avg_missing_pct=("missing_pct", "mean"),
            avg_finite_pct=("finite_pct", "mean"),
            min_first_valid_date=("first_valid_date", "min"),
            max_first_valid_date=("first_valid_date", "max"),
        )
        .reset_index()
    )


def promote_approved_orthogonal_signals_to_main_universe(
    db_path: str | Path | None = None,
    run_id: str | None = None,
    orthogonal_version: str = "phase2_orthogonal_signals_v2",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Promote approved orthogonal signals into main candidate tables with safe dedupe."""
    if run_id is None:
        raise ValueError("run_id is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        main_metadata = _read_sqlite_table(conn, MAIN_SIGNAL_TABLES["metadata"][0])
        main_quality = _read_sqlite_table(conn, MAIN_SIGNAL_TABLES["quality"][0])
        main_quality_gate = _read_sqlite_table(conn, MAIN_SIGNAL_TABLES["quality_gate"][0])
        orthogonal_metadata = _read_sqlite_table(conn, ORTHOGONAL_SIGNAL_TABLES["metadata"][0])
        orthogonal_quality = _read_sqlite_table(conn, ORTHOGONAL_SIGNAL_TABLES["quality"][0])
        orthogonal_family_summary = _read_sqlite_table(conn, ORTHOGONAL_SIGNAL_TABLES["family_summary"][0])

        approved_quality = orthogonal_quality.loc[
            orthogonal_quality["status"].eq("APPROVED_FOR_SCORING")
        ].copy()
        approved_names = approved_quality["signal_name"].dropna().astype(str).unique().tolist()
        existing_names = set(main_metadata["signal_name"].dropna().astype(str))
        existing_orthogonal_names = set(
            main_metadata.loc[
                main_metadata["signal_name"].astype(str).isin(approved_names)
                & main_metadata.get("signal_source", pd.Series("", index=main_metadata.index)).astype(str).eq("orthogonal_generated"),
                "signal_name",
            ].astype(str)
        )
        replace_names = [name for name in approved_names if name in existing_orthogonal_names]
        duplicate_signal_names_skipped = sorted(set(approved_names).intersection(existing_names).difference(replace_names))
        add_names = [name for name in approved_names if name not in existing_names]
        integration_names = add_names + replace_names

        n_main_signals_before = int(main_metadata["signal_name"].nunique())
        n_orthogonal_approved = len(approved_names)
        n_orthogonal_added = len(add_names)

        updated_metadata = main_metadata.copy()
        updated_quality = main_quality.copy()
        updated_quality_gate = main_quality_gate.copy()
        if "orthogonal_version" not in updated_metadata.columns:
            updated_metadata["orthogonal_version"] = pd.NA
        if "signal_source" not in updated_metadata.columns:
            updated_metadata["signal_source"] = pd.NA
        if "signal_source" not in updated_quality.columns:
            updated_quality["signal_source"] = pd.NA
        if "orthogonal_version" not in updated_quality.columns:
            updated_quality["orthogonal_version"] = pd.NA
        if "orthogonal_cluster" not in updated_quality.columns:
            updated_quality["orthogonal_cluster"] = pd.NA
        if "status" not in updated_quality.columns:
            updated_quality["status"] = pd.NA
        if replace_names:
            updated_metadata = updated_metadata.loc[
                ~updated_metadata["signal_name"].astype(str).isin(replace_names)
            ].copy()
            updated_quality = updated_quality.loc[
                ~updated_quality["signal_name"].astype(str).isin(replace_names)
            ].copy()
            updated_quality_gate = updated_quality_gate.loc[
                ~updated_quality_gate["signal_name"].astype(str).isin(replace_names)
            ].copy()

        if integration_names:
            metadata_to_add = _main_metadata_from_orthogonal(
                orthogonal_metadata.loc[orthogonal_metadata["signal_name"].isin(integration_names)].copy(),
                main_columns=updated_metadata.columns.tolist(),
                orthogonal_version=orthogonal_version,
            )
            quality_to_add = _main_quality_from_orthogonal(
                approved_quality.loc[approved_quality["signal_name"].isin(integration_names)].copy(),
                main_columns=updated_quality.columns.tolist(),
                orthogonal_version=orthogonal_version,
            )
            quality_gate_to_add = _main_quality_from_orthogonal(
                approved_quality.loc[approved_quality["signal_name"].isin(integration_names)].copy(),
                main_columns=updated_quality_gate.columns.tolist(),
                orthogonal_version=orthogonal_version,
            )
            if "quality_gate_notes" in quality_gate_to_add.columns:
                quality_gate_to_add["quality_gate_notes"] = "Meets orthogonal structural quality thresholds."
            updated_metadata = (
                pd.concat([updated_metadata, metadata_to_add], ignore_index=True)
                .drop_duplicates("signal_name", keep="first")
                .reset_index(drop=True)
            )
            updated_quality = (
                pd.concat([updated_quality, quality_to_add], ignore_index=True)
                .drop_duplicates("signal_name", keep="first")
                .reset_index(drop=True)
            )
            updated_quality_gate = (
                pd.concat([updated_quality_gate, quality_gate_to_add], ignore_index=True)
                .drop_duplicates("signal_name", keep="first")
                .reset_index(drop=True)
            )

        updated_family_summary = _build_main_family_summary(updated_metadata, updated_quality)
        n_main_signals_after = int(updated_metadata["signal_name"].nunique())

        if integration_names:
            placeholders = ",".join("?" for _ in integration_names)
            signal_columns = [
                row[1] for row in conn.execute(
                    f"PRAGMA table_info({_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])})"
                ).fetchall()
            ]
            orthogonal_signal_columns = [
                row[1] for row in conn.execute(
                    f"PRAGMA table_info({_quote_identifier(ORTHOGONAL_SIGNAL_TABLES['signals'][0])})"
                ).fetchall()
            ]
            selected_columns = [column for column in signal_columns if column in orthogonal_signal_columns]
            if "signal_version" in selected_columns:
                select_expr = ", ".join(
                    f"'{orthogonal_version}' AS signal_version" if column == "signal_version" else _quote_identifier(column)
                    for column in selected_columns
                )
            else:
                select_expr = ", ".join(_quote_identifier(column) for column in selected_columns)
            column_expr = ", ".join(_quote_identifier(column) for column in selected_columns)
            insert_sql = (
                f"INSERT INTO {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])} ({column_expr}) "
                f"SELECT {select_expr} FROM {_quote_identifier(ORTHOGONAL_SIGNAL_TABLES['signals'][0])} "
                f"WHERE signal_name IN ({placeholders})"
            )
            current_delete_placeholders = ",".join("?" for _ in integration_names)
            conn.execute(
                f"DELETE FROM {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])} "
                f"WHERE signal_name IN ({current_delete_placeholders})",
                integration_names,
            )
            conn.execute(insert_sql, integration_names)
            history_insert_sql = insert_sql.replace(
                _quote_identifier(MAIN_SIGNAL_TABLES["signals"][0]),
                _quote_identifier(MAIN_SIGNAL_TABLES["signals"][1]),
                1,
            )
            conn.execute(history_insert_sql, integration_names)

        _write_sqlite_table(updated_metadata, MAIN_SIGNAL_TABLES["metadata"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_metadata, MAIN_SIGNAL_TABLES["metadata"][1], conn, if_exists="append")
        _write_sqlite_table(updated_quality, MAIN_SIGNAL_TABLES["quality"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_quality, MAIN_SIGNAL_TABLES["quality"][1], conn, if_exists="append")
        _write_sqlite_table(updated_quality_gate, MAIN_SIGNAL_TABLES["quality_gate"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_quality_gate, MAIN_SIGNAL_TABLES["quality_gate"][1], conn, if_exists="append")
        _write_sqlite_table(updated_family_summary, MAIN_SIGNAL_TABLES["family_summary"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_family_summary, MAIN_SIGNAL_TABLES["family_summary"][1], conn, if_exists="append")

        if approved_names:
            approved_placeholders = ",".join("?" for _ in approved_names)
            duplicate_candidate_rows = int(
                conn.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM (
                        SELECT signal_name, Date, ticker, COUNT(*) AS n_rows
                        FROM {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])}
                        WHERE signal_name IN ({approved_placeholders})
                        GROUP BY signal_name, Date, ticker
                        HAVING n_rows > 1
                    )
                    """,
                    approved_names,
                ).fetchone()[0]
            )
        else:
            duplicate_candidate_rows = 0
        duplicate_metadata_names = int(
            conn.execute(
                f"""
                SELECT COUNT(*)
                FROM (
                    SELECT signal_name, COUNT(*) AS n_rows
                    FROM {_quote_identifier(MAIN_SIGNAL_TABLES['metadata'][0])}
                    GROUP BY signal_name
                    HAVING n_rows > 1
                )
                """
            ).fetchone()[0]
        )

        integration_report = pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "orthogonal_version": orthogonal_version,
                    "n_main_signals_before": n_main_signals_before,
                    "n_orthogonal_approved": n_orthogonal_approved,
                    "n_orthogonal_added": n_orthogonal_added,
                    "n_main_signals_after": n_main_signals_after,
                    "duplicate_signal_names_skipped": ",".join(duplicate_signal_names_skipped),
                    "integration_status": "SUCCESS",
                    "notes": (
                        f"Approved orthogonal signals promoted to main candidate universe; "
                        f"added={len(add_names)}, refreshed_existing_orthogonal={len(replace_names)}."
                    ),
                }
            ]
        )
        _write_sqlite_table(
            integration_report,
            ORTHOGONAL_SIGNAL_TABLES["integration_report"][0],
            conn,
            if_exists="replace",
        )
        _write_sqlite_table(
            integration_report,
            ORTHOGONAL_SIGNAL_TABLES["integration_report"][1],
            conn,
            if_exists="append",
        )

        diagnostics = pd.DataFrame(
            [
                {"check": "approved_orthogonal_names_present_in_main_metadata", "passed": set(approved_names).issubset(set(updated_metadata["signal_name"]))},
                {"check": "no_duplicate_signal_names_in_main_metadata", "passed": duplicate_metadata_names == 0},
                {"check": "no_duplicate_approved_orthogonal_signal_date_ticker_rows_in_main_candidates", "passed": duplicate_candidate_rows == 0},
                {"check": "main_signal_count_changed_by_added_non_duplicates", "passed": n_main_signals_after == n_main_signals_before + n_orthogonal_added},
                {"check": "orthogonal_family_summary_loaded", "passed": not orthogonal_family_summary.empty},
            ]
        )

    return integration_report, diagnostics


__all__ = [
    "ORTHOGONAL_SIGNAL_TABLES",
    "MAIN_SIGNAL_TABLES",
    "orthogonal_signals_to_long",
    "promote_approved_orthogonal_signals_to_main_universe",
    "save_orthogonal_signal_outputs",
]
