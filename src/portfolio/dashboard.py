"""Engine entrypoint for 09B Alpha System Dashboard data assembly."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.alpha_dashboard import *  # noqa: F401,F403
from src.alpha_dashboard import (
    DASHBOARD_TABLES,
    average_dynamic_weights,
    best_portfolio_by_mode,
    cumulative_return_frame,
    drawdown_frame,
    expansion_readiness_summary,
    get_final_survivors,
    load_dashboard_tables,
    performance_comparison,
    portfolio_alpha_contribution,
    portfolio_return_series,
    rolling_performance_frame,
    rolling_survivor_correlation,
    stress_wfv_interpretation,
    survivor_correlation_matrix,
    system_overview,
)
from src.db import table_exists
from src.run_config import get_sqlite_db_path, make_run_id, make_run_timestamp


DASHBOARD_OUTPUT_TABLES = {
    "dashboard_summary": ("dashboard_summary_current", "dashboard_summary_history"),
    "survivor_summary": ("dashboard_survivor_summary_current", "dashboard_survivor_summary_history"),
    "portfolio_summary": ("dashboard_portfolio_summary_current", "dashboard_portfolio_summary_history"),
    "benchmark_summary": ("dashboard_benchmark_summary_current", "dashboard_benchmark_summary_history"),
    "method_comparison": ("dashboard_method_comparison_current", "dashboard_method_comparison_history"),
    "validation_report": ("dashboard_validation_report_current", "dashboard_validation_report_history"),
}

REQUIRED_INPUT_TABLES = [
    "survivor_alpha_registry_current",
    "pre_ml_alpha_inputs_current",
    "portfolio_alpha_pool_current",
    "portfolio_weights_current",
    "portfolio_backtest_results_current",
    "portfolio_performance_summary_current",
]


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


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


def _sqlite_table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    query = """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
    """
    return conn.execute(query, (table_name,)).fetchone() is not None


def _prepare_dashboard_output(
    df: pd.DataFrame,
    run_id: str,
    dashboard_version: str,
    run_timestamp: str,
) -> pd.DataFrame:
    output = df.copy()
    if output.empty and len(output.columns) == 0:
        output = pd.DataFrame([{}])
    if isinstance(output.index, pd.MultiIndex):
        output = output.reset_index()
    elif output.index.name is not None or not isinstance(output.index, pd.RangeIndex):
        output = output.reset_index()
    if "index" in output.columns and "Date" not in output.columns:
        output = output.rename(columns={"index": "Date"})
    if "Date" in output.columns:
        output["Date"] = pd.to_datetime(output["Date"]).dt.strftime("%Y-%m-%d")
    output["run_id"] = run_id
    output["dashboard_version"] = dashboard_version
    output["run_timestamp"] = run_timestamp
    return output


def _write_dashboard_outputs(
    outputs: dict[str, pd.DataFrame],
    db_path: Path,
    run_id: str,
    dashboard_version: str,
    run_timestamp: str,
) -> dict[str, Path]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        for artifact, (current_table, history_table) in DASHBOARD_OUTPUT_TABLES.items():
            output = _prepare_dashboard_output(
                outputs[artifact],
                run_id=run_id,
                dashboard_version=dashboard_version,
                run_timestamp=run_timestamp,
            )
            output.to_sql(current_table, conn, if_exists="replace", index=False)
            if _sqlite_table_exists(conn, history_table):
                _ensure_sqlite_columns(output, history_table, conn)
            output.to_sql(history_table, conn, if_exists="append", index=False)
    return {artifact: db_path for artifact in DASHBOARD_OUTPUT_TABLES}


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required dashboard input tables are missing from {db_path}: {missing_tables}")


def _loaded_tables_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"table_name": name, "rows": len(df), "columns": len(df.columns)}
            for name, df in tables.items()
        ]
    )


def _overview_metrics(final_survivors: pd.DataFrame) -> pd.DataFrame:
    survivor_names = (
        final_survivors["alpha_name"].dropna().tolist()
        if "alpha_name" in final_survivors.columns
        else []
    )
    clusters = (
        ", ".join(
            final_survivors.get("alpha_behavior_cluster", pd.Series(dtype=object))
            .dropna()
            .astype(str)
            .unique()
        )
        if not final_survivors.empty
        else ""
    )
    return pd.DataFrame(
        [
            {"metric": "n_final_survivors", "value": len(final_survivors)},
            {"metric": "survivor_names", "value": ", ".join(survivor_names)},
            {"metric": "alpha_behavior_clusters", "value": clusters},
        ]
    )


def _best_portfolio_table(best_long_only: pd.Series | None, best_long_short: pd.Series | None) -> pd.DataFrame:
    rows = []
    for label, row in [
        ("best_long_only", best_long_only),
        ("best_long_short", best_long_short),
    ]:
        if row is not None:
            record = {"dashboard_selection": label, **row.to_dict()}
            rows.append(record)
    return pd.DataFrame(rows)


def _benchmark_summary(portfolio_performance_summary: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "portfolio_method",
        "portfolio_mode",
        "benchmark_source",
        "benchmark_total_return",
        "excess_return",
    ]
    if portfolio_performance_summary.empty:
        return pd.DataFrame(columns=columns)
    return portfolio_performance_summary[
        [column for column in columns if column in portfolio_performance_summary.columns]
    ].copy()


def _verification_table(
    *,
    final_survivors: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    portfolio_performance_summary: pd.DataFrame,
    portfolio_backtest_results: pd.DataFrame,
) -> pd.DataFrame:
    survivor_names = (
        final_survivors["alpha_name"].dropna().tolist()
        if "alpha_name" in final_survivors.columns
        else []
    )
    pre_ml_names = set(
        pre_ml_alpha_inputs.get("alpha_name", pd.Series(dtype=object)).dropna().unique()
    )
    verification_checks = {
        "has_final_survivors": len(final_survivors) > 0,
        "has_pre_ml_rows_for_final_survivors": (
            not pre_ml_alpha_inputs.empty
            and set(survivor_names).issubset(pre_ml_names)
        ),
        "has_portfolio_performance": not portfolio_performance_summary.empty,
        "has_portfolio_backtest_returns": not portfolio_backtest_results.empty,
        "pre_ml_only_final_core": pre_ml_names.issubset(set(survivor_names)),
    }
    return pd.DataFrame(
        [{"check_name": name, "passed": bool(passed)} for name, passed in verification_checks.items()]
    )


def _validation_report(
    *,
    final_survivors: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    portfolio_alpha_pool: pd.DataFrame,
    portfolio_weights: pd.DataFrame,
    portfolio_backtest_results: pd.DataFrame,
    portfolio_performance_summary: pd.DataFrame,
    dashboard_outputs: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    survivor_names = set(final_survivors.get("alpha_name", pd.Series(dtype=object)).dropna())
    pre_ml_names = set(pre_ml_alpha_inputs.get("alpha_name", pd.Series(dtype=object)).dropna())
    portfolio_alpha_names = set(portfolio_alpha_pool.get("alpha_name", pd.Series(dtype=object)).dropna())
    method_names = sorted(portfolio_alpha_pool.get("portfolio_method", pd.Series(dtype=object)).dropna().unique())
    mode_names = sorted(
        portfolio_performance_summary.get("portfolio_mode", pd.Series(dtype=object)).dropna().unique()
    )
    checks = [
        {
            "check_name": "has_final_promote_core_survivors",
            "passed": len(survivor_names) > 0,
            "details": f"Final survivor alpha names: {sorted(survivor_names)}",
        },
        {
            "check_name": "portfolio_results_non_empty",
            "passed": not portfolio_performance_summary.empty,
            "details": f"Rows: {len(portfolio_performance_summary)}",
        },
        {
            "check_name": "portfolio_returns_non_empty",
            "passed": not portfolio_backtest_results.empty,
            "details": f"Rows: {len(portfolio_backtest_results)}",
        },
        {
            "check_name": "portfolio_weights_non_empty",
            "passed": not portfolio_weights.empty,
            "details": f"Rows: {len(portfolio_weights)}",
        },
        {
            "check_name": "dashboard_outputs_non_empty",
            "passed": all(not output.empty for output in dashboard_outputs.values()),
            "details": ", ".join(f"{name}={len(output)}" for name, output in dashboard_outputs.items()),
        },
        {
            "check_name": "dashboard_alpha_names_match_portfolio_alpha_names",
            "passed": survivor_names == portfolio_alpha_names and pre_ml_names.issubset(survivor_names),
            "details": (
                f"survivor_names={sorted(survivor_names)}; "
                f"portfolio_alpha_names={sorted(portfolio_alpha_names)}; "
                f"pre_ml_names={sorted(pre_ml_names)}"
            ),
        },
        {
            "check_name": "portfolio_methods_available",
            "passed": len(method_names) > 0,
            "details": f"Methods: {method_names}",
        },
        {
            "check_name": "long_only_and_long_short_metrics_available",
            "passed": {"long_only_top", "long_short_top_bottom"}.issubset(set(mode_names)),
            "details": f"Modes: {mode_names}",
        },
    ]
    return pd.DataFrame(checks, columns=["check_name", "passed", "details"])


def _summary(
    *,
    run_id: str,
    run_timestamp: str,
    dashboard_version: str,
    final_survivors: pd.DataFrame,
    portfolio_alpha_pool: pd.DataFrame,
    portfolio_performance_summary: pd.DataFrame,
    validation_report: pd.DataFrame,
) -> pd.DataFrame:
    survivor_names = sorted(final_survivors.get("alpha_name", pd.Series(dtype=object)).dropna().unique())
    method_names = sorted(portfolio_alpha_pool.get("portfolio_method", pd.Series(dtype=object)).dropna().unique())
    mode_names = sorted(
        portfolio_performance_summary.get("portfolio_mode", pd.Series(dtype=object)).dropna().unique()
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "dashboard_version", "value": dashboard_version},
            {"metric": "n_final_survivors", "value": len(survivor_names)},
            {"metric": "final_survivor_alpha_names", "value": ", ".join(survivor_names)},
            {"metric": "portfolio_methods", "value": ", ".join(method_names)},
            {"metric": "portfolio_modes", "value": ", ".join(mode_names)},
            {"metric": "portfolio_result_rows", "value": len(portfolio_performance_summary)},
            {"metric": "validation_checks_pass", "value": bool(validation_report["passed"].all())},
        ]
    )


def run_09b_dashboard(
    db_path=None,
    dashboard_version: str = "phase9b_dashboard_v1",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run 09B dashboard data assembly as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    resolved_run_id = run_id or make_run_id(prefix="phase9b_dashboard")
    run_timestamp = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    tables = load_dashboard_tables(resolved_db_path)

    survivor_registry = tables["survivor_alpha_registry_current"]
    pre_ml_alpha_inputs = tables["pre_ml_alpha_inputs_current"]
    portfolio_alpha_pool = tables["portfolio_alpha_pool_current"]
    portfolio_weights = tables["portfolio_weights_current"]
    portfolio_backtest_results = tables["portfolio_backtest_results_current"]
    portfolio_performance_summary = tables["portfolio_performance_summary_current"]
    alpha_dynamic_weight_audit = tables["alpha_dynamic_weight_audit_current"]
    alpha_stress_gate = tables["alpha_stress_gate_current"]
    constructed_alpha_wfv_gate = tables["constructed_alpha_wfv_gate_current"]
    signal_diversity_selection = tables["signal_diversity_selection_current"]
    survivor_cluster_summary = tables["survivor_cluster_summary_current"]

    final_survivors = get_final_survivors(survivor_registry)
    overview = system_overview(survivor_registry)
    overview_metrics = _overview_metrics(final_survivors)

    method_comparison = performance_comparison(portfolio_performance_summary)
    best_long_only = best_portfolio_by_mode(portfolio_performance_summary, "long_only")
    best_long_short = best_portfolio_by_mode(portfolio_performance_summary, "long_short")
    best_portfolios = _best_portfolio_table(best_long_only, best_long_short)

    best_long_only_returns = portfolio_return_series(portfolio_backtest_results, best_long_only)
    best_long_short_returns = portfolio_return_series(portfolio_backtest_results, best_long_short)
    long_only_curve = cumulative_return_frame(best_long_only_returns)
    long_short_curve = cumulative_return_frame(best_long_short_returns)
    long_only_drawdown = drawdown_frame(best_long_only_returns)
    rolling_perf = rolling_performance_frame(best_long_only_returns)

    contribution_table = portfolio_alpha_contribution(portfolio_alpha_pool, final_survivors)
    dynamic_weights = average_dynamic_weights(alpha_dynamic_weight_audit, final_survivors)
    corr_matrix = survivor_correlation_matrix(pre_ml_alpha_inputs, final_survivors)
    rolling_corr = rolling_survivor_correlation(pre_ml_alpha_inputs, final_survivors)
    stress_wfv_table = stress_wfv_interpretation(
        final_survivors,
        alpha_stress_gate,
        constructed_alpha_wfv_gate,
    )
    if not signal_diversity_selection.empty and "selected_flag" in signal_diversity_selection.columns:
        diversity_summary = (
            signal_diversity_selection.groupby(["diversity_group", "selected_flag"], dropna=False)
            .size()
            .reset_index(name="n_signal_horizons")
            .sort_values(["diversity_group", "selected_flag"])
        )
    else:
        diversity_summary = pd.DataFrame(columns=["diversity_group", "selected_flag", "n_signal_horizons"])

    verification_table = _verification_table(
        final_survivors=final_survivors,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        portfolio_performance_summary=portfolio_performance_summary,
        portfolio_backtest_results=portfolio_backtest_results,
    )
    readiness_summary = expansion_readiness_summary(
        final_survivors=final_survivors,
        performance_summary=portfolio_performance_summary,
        verification_checks_pass=bool(verification_table["passed"].all()),
    )
    benchmark_summary = _benchmark_summary(portfolio_performance_summary)
    survivor_summary = pd.concat(
        [
            overview_metrics.assign(section="overview_metrics"),
        ],
        ignore_index=True,
    )
    portfolio_summary = portfolio_performance_summary.copy()
    dashboard_summary = pd.concat(
        [
            _loaded_tables_summary(tables).assign(section="loaded_tables"),
            readiness_summary.assign(section="readiness_summary"),
        ],
        ignore_index=True,
        sort=False,
    )

    dashboard_outputs = {
        "dashboard_summary": dashboard_summary,
        "survivor_summary": survivor_summary,
        "portfolio_summary": portfolio_summary,
        "benchmark_summary": benchmark_summary,
        "method_comparison": method_comparison,
    }
    validation_report = _validation_report(
        final_survivors=final_survivors,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        portfolio_alpha_pool=portfolio_alpha_pool,
        portfolio_weights=portfolio_weights,
        portfolio_backtest_results=portfolio_backtest_results,
        portfolio_performance_summary=portfolio_performance_summary,
        dashboard_outputs=dashboard_outputs,
    )
    dashboard_outputs["validation_report"] = validation_report
    if not validation_report["passed"].all():
        failed = validation_report.loc[
            ~validation_report["passed"],
            ["check_name", "details"],
        ].to_dict("records")
        raise ValueError(f"Dashboard validation failed: {failed}")

    summary = _summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        dashboard_version=dashboard_version,
        final_survivors=final_survivors,
        portfolio_alpha_pool=portfolio_alpha_pool,
        portfolio_performance_summary=portfolio_performance_summary,
        validation_report=validation_report,
    )

    saved_paths = None
    if write:
        saved_paths = _write_dashboard_outputs(
            dashboard_outputs,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            dashboard_version=dashboard_version,
            run_timestamp=run_timestamp,
        )

    _log(verbose, f"Loaded 09B dashboard inputs from {resolved_db_path}")
    for table_name, df in tables.items():
        _log(verbose, f"  {table_name}: {len(df):,} rows x {len(df.columns):,} columns")
    _log(verbose, "09B dashboard output rows")
    for artifact_name, artifact in [
        ("dashboard_summary", dashboard_summary),
        ("survivor_summary", survivor_summary),
        ("portfolio_summary", portfolio_summary),
        ("benchmark_summary", benchmark_summary),
        ("method_comparison", method_comparison),
        ("validation_report", validation_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "dashboard_summary": dashboard_summary,
        "survivor_summary": survivor_summary,
        "portfolio_summary": portfolio_summary,
        "benchmark_summary": benchmark_summary,
        "method_comparison": method_comparison,
        "validation_report": validation_report,
        "summary": summary,
        "overview": overview,
        "best_portfolios": best_portfolios,
        "long_only_curve": long_only_curve,
        "long_short_curve": long_short_curve,
        "long_only_drawdown": long_only_drawdown,
        "rolling_performance": rolling_perf,
        "contribution_table": contribution_table,
        "dynamic_weights": dynamic_weights,
        "survivor_correlation_matrix": corr_matrix,
        "rolling_survivor_correlation": rolling_corr,
        "survivor_cluster_summary": survivor_cluster_summary,
        "stress_wfv_table": stress_wfv_table,
        "diversity_summary": diversity_summary,
        "verification_table": verification_table,
        "readiness_summary": readiness_summary,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
