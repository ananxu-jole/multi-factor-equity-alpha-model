"""Controlled signal WFV bridge for selected expanded-discovery WATCHLIST signals."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_price_table, load_table  # noqa: E402
from src.run_config import get_sqlite_db_path, make_run_id  # noqa: E402
from src.signal_storage import load_candidate_signals_by_names  # noqa: E402
from src.walkforward import generate_walkforward_windows  # noqa: E402
from src.wfv_scoring import run_wfv_for_candidates  # noqa: E402
from src.wfv_storage import WFV_CANDIDATE_TABLES, save_wfv_diagnostics, save_wfv_outputs  # noqa: E402
from src.wfv_summary import (  # noqa: E402
    apply_wfv_gate,
    build_wfv_failure_breakdown,
    build_wfv_window_diagnostics,
    summarize_wfv_results,
)


BRIDGE_VERSION = "phase2_signal_wfv_bridge_v1"
EXPANSION_BATCH = "phase2_expansion_batch_v1"
PRIMARY_CANDIDATES = ("trend_consistency_20_60", "index_relative_reversal_5")
DIAGNOSTIC_CANDIDATES = ("percentile_rank_stability_20", "smooth_trend_persistence_60")
TRAIN_SIZE = 378
TEST_SIZE = 63
PURGE_SIZE = 20
EMBARGO_SIZE = 5
IC_METHOD = "spearman"


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
    for column in output.columns:
        if column.endswith("_start") or column.endswith("_end") or column == "Date":
            output[column] = pd.to_datetime(output[column], errors="coerce").dt.strftime("%Y-%m-%d")
    if if_exists == "append" and _table_exists(conn, table_name):
        _ensure_sqlite_columns(output, table_name, conn)
    output.to_sql(table_name, conn, if_exists=if_exists, index=False)


def _save_wfv_candidates(
    candidates: pd.DataFrame,
    db_path: str | Path | None,
    run_id: str,
    wfv_version: str,
) -> None:
    output = candidates.copy()
    output["run_id"] = run_id
    output["wfv_version"] = wfv_version
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(resolved_db_path) as conn:
        current_table, history_table = WFV_CANDIDATE_TABLES["candidates"]
        _write_sqlite_table(output, current_table, conn, if_exists="replace")
        _write_sqlite_table(output, history_table, conn, if_exists="append")


def build_bridge_candidates(
    db_path: str | Path | None = None,
    include_diagnostics: bool = False,
    candidate_names: tuple[str, ...] | None = None,
    expansion_batch: str = EXPANSION_BATCH,
    required_horizons: dict[str, int] | None = None,
    bridge_source: str | None = None,
    candidate_tiers: dict[str, str] | None = None,
    bridge_reasons: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Build an allowlisted expanded-discovery WFV bridge candidate set."""
    metadata = load_table("candidate_signal_metadata_current", db_path=db_path)
    quality_gate = load_table("candidate_signal_quality_gate_current", db_path=db_path)
    scoring_gate = load_table("signal_scoring_gate_current", db_path=db_path)
    best_horizon = load_table("signal_best_horizon_current", db_path=db_path)
    decay = load_table("signal_decay_summary_current", db_path=db_path)

    if candidate_names is None:
        allowed_names = list(PRIMARY_CANDIDATES)
        if include_diagnostics:
            allowed_names.extend(DIAGNOSTIC_CANDIDATES)
    else:
        allowed_names = list(candidate_names)

    batch_metadata = metadata.loc[
        metadata["signal_name"].astype(str).isin(allowed_names)
        & metadata.get("discovery_version", pd.Series("", index=metadata.index)).astype(str).ne("")
        & metadata.get("signal_version", pd.Series("", index=metadata.index)).astype(str).ne("")
    ].copy()
    if "expansion_batch" in batch_metadata.columns:
        batch_metadata = batch_metadata.loc[batch_metadata["expansion_batch"].astype(str).eq(expansion_batch)]
    else:
        expanded_metadata = load_table("expanded_discovery_metadata_current", db_path=db_path)
        batch_names = set(
            expanded_metadata.loc[
                expanded_metadata.get("expansion_batch", pd.Series("", index=expanded_metadata.index)).astype(str).eq(expansion_batch),
                "signal_name",
            ].astype(str)
        )
        batch_metadata = batch_metadata.loc[batch_metadata["signal_name"].astype(str).isin(batch_names)]

    if batch_metadata.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "expansion_batch",
                "candidate_tier",
                "signal_direction",
                "signal_family",
                "signal_strength",
                "source_status",
                "bridge_source",
                "bridge_reason",
            ]
        )

    candidates = (
        best_horizon[
            [
                "signal_name",
                "best_horizon",
                "signal_direction",
                "signal_family",
                "signal_strength",
            ]
        ]
        .rename(columns={"best_horizon": "horizon"})
        .merge(
            quality_gate[["signal_name", "status"]].rename(columns={"status": "quality_status"}),
            on="signal_name",
            how="inner",
        )
        .merge(
            scoring_gate[["signal_name", "horizon", "status"]].rename(columns={"status": "source_status"}),
            on=["signal_name", "horizon"],
            how="inner",
        )
        .merge(
            decay[["signal_name", "horizon", "decay_status", "decay_risk_flag"]],
            on=["signal_name", "horizon"],
            how="left",
        )
    )
    candidates = candidates.loc[
        candidates["signal_name"].astype(str).isin(batch_metadata["signal_name"].astype(str))
        & candidates["quality_status"].eq("APPROVED_FOR_SCORING")
    ].copy()
    if candidate_names is None:
        candidates = candidates.loc[
            candidates["source_status"].eq("WATCHLIST")
            & candidates["decay_status"].isin(["STABLE", "UNSTABLE"])
            & candidates["decay_risk_flag"].ne("HIGH_DECAY_RISK")
        ].copy()
    else:
        candidates = candidates.loc[
            candidates["source_status"].isin(["WATCHLIST", "APPROVED_FOR_WFV"])
            & candidates["decay_status"].notna()
        ].copy()
    if required_horizons:
        required = pd.Series(required_horizons, name="required_horizon")
        candidates = candidates.merge(required, left_on="signal_name", right_index=True, how="left")
        candidates = candidates.loc[
            candidates["required_horizon"].isna()
            | candidates["horizon"].astype(int).eq(candidates["required_horizon"].astype(int))
        ].drop(columns=["required_horizon"])

    if candidates.empty:
        return candidates

    if candidate_names is None:
        candidates["candidate_tier"] = candidates["signal_name"].map(
            {name: "EXPANSION_BRIDGE_PRIMARY" for name in PRIMARY_CANDIDATES}
            | {name: "EXPANSION_BRIDGE_DIAGNOSTIC" for name in DIAGNOSTIC_CANDIDATES}
        )
        reason_map = {
            "EXPANSION_BRIDGE_PRIMARY": "Allowlisted Batch 1 WATCHLIST signal for controlled signal WFV bridge.",
            "EXPANSION_BRIDGE_DIAGNOSTIC": "Allowlisted Batch 1 diagnostic WATCHLIST signal for controlled signal WFV bridge.",
        }
    else:
        candidates["candidate_tier"] = candidates["signal_name"].map(candidate_tiers or {}).fillna("EXPANSION_BRIDGE_PRIMARY")
        reason_map = {
            "EXPANSION_BRIDGE_PRIMARY": "Allowlisted WATCHLIST signal for controlled signal WFV bridge.",
        }
    candidates["expansion_batch"] = expansion_batch
    candidates["bridge_source"] = bridge_source or expansion_batch
    candidates["bridge_reason"] = candidates["signal_name"].map(bridge_reasons or {})
    candidates["bridge_reason"] = candidates["bridge_reason"].fillna(candidates["candidate_tier"].map(reason_map))
    columns = [
        "signal_name",
        "horizon",
        "expansion_batch",
        "candidate_tier",
        "signal_direction",
        "signal_family",
        "signal_strength",
        "source_status",
        "bridge_source",
        "bridge_reason",
    ]
    return candidates[columns].drop_duplicates(["signal_name", "horizon"]).sort_values(
        ["candidate_tier", "signal_name", "horizon"]
    ).reset_index(drop=True)


def run_03b_signal_wfv_bridge(
    db_path: str | Path | None = None,
    run_id: str | None = None,
    wfv_version: str = BRIDGE_VERSION,
    include_diagnostics: bool = False,
    candidate_names: tuple[str, ...] | None = None,
    expansion_batch: str = EXPANSION_BATCH,
    required_horizons: dict[str, int] | None = None,
    bridge_source: str | None = None,
    candidate_tiers: dict[str, str] | None = None,
    bridge_reasons: dict[str, str] | None = None,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    resolved_run_id = run_id or make_run_id(prefix="phase2_signal_wfv_bridge")
    candidates = build_bridge_candidates(
        db_path=db_path,
        include_diagnostics=include_diagnostics,
        candidate_names=candidate_names,
        expansion_batch=expansion_batch,
        required_horizons=required_horizons,
        bridge_source=bridge_source,
        candidate_tiers=candidate_tiers,
        bridge_reasons=bridge_reasons,
    )

    close_prices = load_price_table("clean_close_prices_current", db_path=db_path)
    windows = generate_walkforward_windows(
        close_prices.index,
        train_size=TRAIN_SIZE,
        test_size=TEST_SIZE,
        purge_size=PURGE_SIZE,
        embargo_size=EMBARGO_SIZE,
    )

    if candidates.empty:
        window_results = pd.DataFrame()
    else:
        signal_long = load_candidate_signals_by_names(
            candidates["signal_name"].dropna().astype(str).unique().tolist(),
            current=True,
            db_path=db_path,
            chunksize=500_000,
        )
        window_results = run_wfv_for_candidates(
            candidates=candidates,
            signal_long_df=signal_long,
            close_prices=close_prices,
            horizons=sorted(candidates["horizon"].astype(int).unique().tolist()),
            windows=windows,
            method=IC_METHOD,
        )

    summary = summarize_wfv_results(window_results)
    gate = apply_wfv_gate(summary) if not summary.empty else summary.copy()
    failure_breakdown = build_wfv_failure_breakdown(gate)
    window_diagnostics = build_wfv_window_diagnostics(window_results)

    if write:
        _save_wfv_candidates(candidates, db_path=db_path, run_id=resolved_run_id, wfv_version=wfv_version)
        save_wfv_outputs(
            windows=windows,
            window_results=window_results,
            summary=summary,
            gate=gate,
            db_path=db_path,
            run_id=resolved_run_id,
            wfv_version=wfv_version,
        )
        save_wfv_diagnostics(
            failure_breakdown=failure_breakdown,
            window_diagnostics=window_diagnostics,
            db_path=db_path,
            run_id=resolved_run_id,
            wfv_version=wfv_version,
        )

    pipeline_summary = pd.DataFrame(
        [
            {"metric": "run_id", "value": resolved_run_id},
            {"metric": "wfv_version", "value": wfv_version},
            {"metric": "include_diagnostics", "value": bool(include_diagnostics)},
            {"metric": "expansion_batch", "value": expansion_batch},
            {"metric": "candidate_rows", "value": len(candidates)},
            {"metric": "window_rows", "value": len(windows)},
            {"metric": "window_result_rows", "value": len(window_results)},
            {"metric": "summary_rows", "value": len(summary)},
            {"metric": "gate_rows", "value": len(gate)},
            {
                "metric": "wfv_status_counts",
                "value": gate["status"].value_counts(dropna=False).sort_index().astype(int).to_dict()
                if not gate.empty and "status" in gate.columns
                else {},
            },
        ]
    )

    if verbose:
        print("03B signal WFV bridge candidates:")
        print(candidates.to_string(index=False) if not candidates.empty else "  <none>")
        print("03B signal WFV bridge gate:")
        print(
            gate[
                [
                    column
                    for column in [
                        "signal_name",
                        "horizon",
                        "candidate_tier",
                        "effective_mean_test_ic",
                        "effective_test_ic_ir",
                        "persistence_ratio",
                        "sign_consistency",
                        "status",
                    ]
                    if column in gate.columns
                ]
            ].to_string(index=False)
            if not gate.empty
            else "  <none>"
        )

    return {
        "run_id": resolved_run_id,
        "wfv_version": wfv_version,
        "candidates": candidates,
        "windows": windows,
        "window_results": window_results,
        "summary": summary,
        "gate": gate,
        "failure_breakdown": failure_breakdown,
        "window_diagnostics": window_diagnostics,
        "pipeline_summary": pipeline_summary,
    }


def _print_summary(result: dict[str, object]) -> None:
    print("summary:")
    for row in result["pipeline_summary"].to_dict("records"):
        print(f"  {row['metric']}: {row['value']}")


def _print_description() -> None:
    print("stage_id: 03b_signal_wfv_bridge")
    print("stage_version: " + BRIDGE_VERSION)
    print("candidate_source: " + EXPANSION_BATCH)
    print("primary_candidates:")
    for name in PRIMARY_CANDIDATES:
        print(f"  - {name}")
    print("diagnostic_candidates:")
    for name in DIAGNOSTIC_CANDIDATES:
        print(f"  - {name}")
    print("wfv_parameters:")
    print(f"  train_size: {TRAIN_SIZE}")
    print(f"  test_size: {TEST_SIZE}")
    print(f"  purge_size: {PURGE_SIZE}")
    print(f"  embargo_size: {EMBARGO_SIZE}")
    print(f"  method: {IC_METHOD}")
    print("output_tables:")
    print("  - signal_wfv_candidates_current/history")
    print("  - wfv_windows_current/history")
    print("  - wfv_window_results_current/history")
    print("  - wfv_summary_current/history")
    print("  - wfv_gate_current/history")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the controlled 03B signal WFV bridge.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print bridge metadata only.")
    mode.add_argument("--dry-run", action="store_true", help="Run bridge logic without writing SQLite outputs.")
    mode.add_argument("--run", action="store_true", help="Run bridge and write existing WFV SQLite outputs.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id.")
    parser.add_argument("--wfv-version", default=BRIDGE_VERSION, help="WFV bridge version label.")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed bridge logging.")
    parser.add_argument(
        "--include-diagnostics",
        action="store_true",
        help="Include diagnostic Batch 1 WATCHLIST signals in addition to primary bridge candidates.",
    )
    parser.add_argument(
        "--candidate-name",
        action="append",
        default=None,
        help="Optional explicit allowlisted signal name. May be supplied more than once.",
    )
    parser.add_argument(
        "--expansion-batch",
        default=EXPANSION_BATCH,
        help="Expansion batch label required for bridge candidate admission.",
    )
    parser.add_argument(
        "--required-horizon",
        action="append",
        default=None,
        help="Optional required horizon in signal_name:horizon form, e.g. trend_consistency_20_60_persistent:20.",
    )
    parser.add_argument(
        "--bridge-source",
        default=None,
        help="Optional bridge_source metadata value for explicit candidates.",
    )
    parser.add_argument(
        "--candidate-tier",
        action="append",
        default=None,
        help="Optional candidate tier in signal_name:tier form. May be supplied more than once.",
    )
    parser.add_argument(
        "--bridge-reason",
        action="append",
        default=None,
        help="Optional bridge reason in signal_name:reason form. May be supplied more than once.",
    )
    args = parser.parse_args()

    if args.describe:
        _print_description()
        return 0

    required_horizons = {}
    for item in args.required_horizon or []:
        if ":" not in item:
            raise ValueError("--required-horizon must be in signal_name:horizon form.")
        name, horizon = item.split(":", 1)
        required_horizons[name] = int(horizon)
    candidate_tiers = {}
    for item in args.candidate_tier or []:
        if ":" not in item:
            raise ValueError("--candidate-tier must be in signal_name:tier form.")
        name, tier = item.split(":", 1)
        candidate_tiers[name] = tier
    bridge_reasons = {}
    for item in args.bridge_reason or []:
        if ":" not in item:
            raise ValueError("--bridge-reason must be in signal_name:reason form.")
        name, reason = item.split(":", 1)
        bridge_reasons[name] = reason

    result = run_03b_signal_wfv_bridge(
        db_path=args.db_path,
        run_id=args.run_id,
        wfv_version=args.wfv_version,
        include_diagnostics=args.include_diagnostics,
        candidate_names=tuple(args.candidate_name) if args.candidate_name else None,
        expansion_batch=args.expansion_batch,
        required_horizons=required_horizons or None,
        bridge_source=args.bridge_source,
        candidate_tiers=candidate_tiers or None,
        bridge_reasons=bridge_reasons or None,
        write=args.run,
        verbose=not args.quiet,
    )
    _print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
