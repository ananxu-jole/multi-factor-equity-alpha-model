from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.expanded_discovery import EXPANDED_DISCOVERY_SOURCE
from src.run_config import get_sqlite_db_path
from src.signal_quality import build_signal_family_summary
from src.signal_storage import signals_to_long


EXPANDED_DISCOVERY_TABLES = {
    "signals": ("expanded_discovery_candidate_signals_current", "expanded_discovery_candidate_signals_history"),
    "metadata": ("expanded_discovery_metadata_current", "expanded_discovery_metadata_history"),
    "quality": ("expanded_discovery_quality_current", "expanded_discovery_quality_history"),
    "core_corr": ("expanded_discovery_core_corr_current", "expanded_discovery_core_corr_history"),
    "selection": ("expanded_discovery_selection_current", "expanded_discovery_selection_history"),
    "integration_report": ("expanded_discovery_integration_report_current", "expanded_discovery_integration_report_history"),
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
    return (
        conn.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            LIMIT 1
            """,
            (table_name,),
        ).fetchone()
        is not None
    )


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
    for column in [column for column in df.columns if column not in existing_columns]:
        conn.execute(
            f"ALTER TABLE {_quote_identifier(table_name)} "
            f"ADD COLUMN {_quote_identifier(column)} {_sqlite_type_for_series(df[column])}"
        )


def _write_sqlite_table(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection, if_exists: str) -> None:
    output = df.copy()
    for date_column in ("Date", "first_valid_date", "last_valid_date", "created_timestamp"):
        if date_column in output.columns:
            output[date_column] = pd.to_datetime(output[date_column], errors="coerce").dt.strftime("%Y-%m-%d")
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(output, table_name, conn)
    output.to_sql(table_name, conn, if_exists=if_exists, index=False)


def save_expanded_discovery_outputs(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    quality: pd.DataFrame,
    core_corr: pd.DataFrame,
    selection: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    discovery_version: str | None = None,
) -> dict[str, Path]:
    if run_id is None:
        raise ValueError("run_id is required.")
    if discovery_version is None:
        raise ValueError("discovery_version is required.")

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    signals_long = signals_to_long(signals, run_id=run_id, signal_version=discovery_version)
    signals_long["signal_source"] = EXPANDED_DISCOVERY_SOURCE
    signals_long["discovery_version"] = discovery_version

    outputs = {
        "signals": signals_long,
        "metadata": metadata,
        "quality": quality,
        "core_corr": core_corr,
        "selection": selection,
    }
    with sqlite3.connect(db_path) as conn:
        for artifact, output in outputs.items():
            current_table, history_table = EXPANDED_DISCOVERY_TABLES[artifact]
            _write_sqlite_table(output, current_table, conn, if_exists="replace")
            _write_sqlite_table(output, history_table, conn, if_exists="append")
    return {artifact: db_path for artifact in EXPANDED_DISCOVERY_TABLES}


def _read_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    if not _table_exists(conn, table_name):
        return pd.DataFrame()
    return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(table_name)}", conn)


def _main_metadata_from_expanded(metadata: pd.DataFrame, main_columns: list[str], discovery_version: str) -> pd.DataFrame:
    output = metadata.copy()
    output["input_fields"] = output["data_dependencies"]
    output["normalization_notes"] = output.get("normalization", "")
    output["signal_version"] = discovery_version
    output["timestamp"] = output.get("created_timestamp", pd.NA)
    output["signal_source"] = EXPANDED_DISCOVERY_SOURCE
    output["discovery_version"] = discovery_version
    for column in main_columns:
        if column not in output.columns:
            output[column] = pd.NA
    return output.reindex(columns=main_columns)


def _main_quality_from_expanded(quality: pd.DataFrame, main_columns: list[str], discovery_version: str) -> pd.DataFrame:
    output = quality.copy()
    output["signal_version"] = discovery_version
    output["signal_source"] = EXPANDED_DISCOVERY_SOURCE
    output["status"] = "APPROVED_FOR_SCORING"
    output["quality_gate_notes"] = "Meets expanded-discovery structural and selection gates."
    for column in main_columns:
        if column not in output.columns:
            output[column] = pd.NA
    return output.reindex(columns=main_columns)


def promote_selected_expanded_discovery_to_main_universe(
    db_path: str | Path | None = None,
    run_id: str | None = None,
    discovery_version: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if run_id is None:
        raise ValueError("run_id is required.")
    if discovery_version is None:
        raise ValueError("discovery_version is required.")
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()

    with sqlite3.connect(db_path) as conn:
        metadata = _read_table(conn, EXPANDED_DISCOVERY_TABLES["metadata"][0])
        quality = _read_table(conn, EXPANDED_DISCOVERY_TABLES["quality"][0])
        selection = _read_table(conn, EXPANDED_DISCOVERY_TABLES["selection"][0])
        selected_names = sorted(
            selection.loc[
                selection.get("selection_status", pd.Series(dtype=str)).astype(str).eq("PROMOTE_EXPANDED_DISCOVERY"),
                "signal_name",
            ].dropna().astype(str).unique()
        )

        main_metadata = _read_table(conn, MAIN_SIGNAL_TABLES["metadata"][0])
        main_quality = _read_table(conn, MAIN_SIGNAL_TABLES["quality"][0])
        main_quality_gate = _read_table(conn, MAIN_SIGNAL_TABLES["quality_gate"][0])
        existing_names = set(main_metadata.get("signal_name", pd.Series(dtype=str)).dropna().astype(str))
        existing_expanded_names = set(
            main_metadata.loc[
                main_metadata.get("signal_name", pd.Series(dtype=str)).astype(str).isin(selected_names)
                & main_metadata.get("signal_source", pd.Series("", index=main_metadata.index)).astype(str).eq(EXPANDED_DISCOVERY_SOURCE),
                "signal_name",
            ].astype(str)
        )
        replace_names = sorted(existing_expanded_names)
        add_names = sorted(set(selected_names).difference(existing_names))
        skipped_existing_non_expanded = sorted(set(selected_names).intersection(existing_names).difference(existing_expanded_names))
        integration_names = add_names + replace_names

        updated_metadata = main_metadata.loc[
            ~main_metadata.get("signal_name", pd.Series(dtype=str)).astype(str).isin(replace_names)
        ].copy()
        updated_quality = main_quality.loc[
            ~main_quality.get("signal_name", pd.Series(dtype=str)).astype(str).isin(replace_names)
        ].copy()
        updated_quality_gate = main_quality_gate.loc[
            ~main_quality_gate.get("signal_name", pd.Series(dtype=str)).astype(str).isin(replace_names)
        ].copy()

        if integration_names:
            metadata_to_add = _main_metadata_from_expanded(
                metadata.loc[metadata["signal_name"].astype(str).isin(integration_names)].copy(),
                updated_metadata.columns.tolist(),
                discovery_version,
            )
            quality_to_add = _main_quality_from_expanded(
                quality.loc[quality["signal_name"].astype(str).isin(integration_names)].copy(),
                updated_quality.columns.tolist(),
                discovery_version,
            )
            quality_gate_to_add = _main_quality_from_expanded(
                quality.loc[quality["signal_name"].astype(str).isin(integration_names)].copy(),
                updated_quality_gate.columns.tolist(),
                discovery_version,
            )
            updated_metadata = pd.concat([updated_metadata, metadata_to_add], ignore_index=True).drop_duplicates("signal_name", keep="last")
            updated_quality = pd.concat([updated_quality, quality_to_add], ignore_index=True).drop_duplicates("signal_name", keep="last")
            updated_quality_gate = pd.concat([updated_quality_gate, quality_gate_to_add], ignore_index=True).drop_duplicates("signal_name", keep="last")

            placeholders = ",".join("?" for _ in integration_names)
            current_delete_placeholders = ",".join("?" for _ in integration_names)
            conn.execute(
                f"DELETE FROM {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])} "
                f"WHERE signal_name IN ({current_delete_placeholders})",
                integration_names,
            )
            signal_columns = [
                row[1] for row in conn.execute(
                    f"PRAGMA table_info({_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])})"
                ).fetchall()
            ]
            expanded_columns = [
                row[1] for row in conn.execute(
                    f"PRAGMA table_info({_quote_identifier(EXPANDED_DISCOVERY_TABLES['signals'][0])})"
                ).fetchall()
            ]
            selected_columns = [column for column in signal_columns if column in expanded_columns]
            select_expr = ", ".join(
                f"'{discovery_version}' AS signal_version" if column == "signal_version" else _quote_identifier(column)
                for column in selected_columns
            )
            column_expr = ", ".join(_quote_identifier(column) for column in selected_columns)
            insert_sql = (
                f"INSERT INTO {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])} ({column_expr}) "
                f"SELECT {select_expr} FROM {_quote_identifier(EXPANDED_DISCOVERY_TABLES['signals'][0])} "
                f"WHERE signal_name IN ({placeholders})"
            )
            conn.execute(insert_sql, integration_names)
            conn.execute(
                insert_sql.replace(
                    _quote_identifier(MAIN_SIGNAL_TABLES["signals"][0]),
                    _quote_identifier(MAIN_SIGNAL_TABLES["signals"][1]),
                    1,
                ),
                integration_names,
            )

        family_summary = build_signal_family_summary(updated_quality)
        _write_sqlite_table(updated_metadata, MAIN_SIGNAL_TABLES["metadata"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_metadata, MAIN_SIGNAL_TABLES["metadata"][1], conn, if_exists="append")
        _write_sqlite_table(updated_quality, MAIN_SIGNAL_TABLES["quality"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_quality, MAIN_SIGNAL_TABLES["quality"][1], conn, if_exists="append")
        _write_sqlite_table(updated_quality_gate, MAIN_SIGNAL_TABLES["quality_gate"][0], conn, if_exists="replace")
        _write_sqlite_table(updated_quality_gate, MAIN_SIGNAL_TABLES["quality_gate"][1], conn, if_exists="append")
        _write_sqlite_table(family_summary, MAIN_SIGNAL_TABLES["family_summary"][0], conn, if_exists="replace")
        _write_sqlite_table(family_summary, MAIN_SIGNAL_TABLES["family_summary"][1], conn, if_exists="append")

        if selected_names:
            duplicate_placeholders = ",".join("?" for _ in selected_names)
            duplicate_candidate_rows = int(
                conn.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM (
                        SELECT signal_name, Date, ticker, COUNT(*) AS n_rows
                        FROM {_quote_identifier(MAIN_SIGNAL_TABLES['signals'][0])}
                        WHERE signal_name IN ({duplicate_placeholders})
                        GROUP BY signal_name, Date, ticker
                        HAVING n_rows > 1
                    )
                    """,
                    selected_names,
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

        report = pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "discovery_version": discovery_version,
                    "n_selected": len(selected_names),
                    "n_added": len(add_names),
                    "n_refreshed": len(replace_names),
                    "skipped_existing_non_expanded": ",".join(skipped_existing_non_expanded),
                    "integration_status": "SUCCESS",
                    "notes": "Selected expanded discovery candidates promoted with signal-name dedupe.",
                }
            ]
        )
        diagnostics = pd.DataFrame(
            [
                {"check": "no_duplicate_signal_names_in_metadata", "passed": duplicate_metadata_names == 0},
                {"check": "no_duplicate_selected_signal_date_ticker_rows", "passed": duplicate_candidate_rows == 0},
                {"check": "selected_names_promoted_or_skipped_by_dedupe", "passed": len(selected_names) == len(integration_names) + len(skipped_existing_non_expanded)},
            ]
        )
        _write_sqlite_table(report, EXPANDED_DISCOVERY_TABLES["integration_report"][0], conn, if_exists="replace")
        _write_sqlite_table(report, EXPANDED_DISCOVERY_TABLES["integration_report"][1], conn, if_exists="append")

    return report, diagnostics


__all__ = [
    "EXPANDED_DISCOVERY_TABLES",
    "MAIN_SIGNAL_TABLES",
    "promote_selected_expanded_discovery_to_main_universe",
    "save_expanded_discovery_outputs",
]
