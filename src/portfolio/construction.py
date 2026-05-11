"""Engine entrypoint for 09 Portfolio Construction Execution Layer."""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_benchmark_prices, load_ohlcv_panels, load_table, table_exists
from src.portfolio_backtest import compute_portfolio_metrics, compute_strategy_returns
from src.portfolio_construction import *  # noqa: F401,F403
from src.portfolio_construction import (
    apply_rebalance_schedule,
    build_alpha_signal_stack,
    build_long_only_top_bucket_positions,
    build_survivor_weight_table,
    build_target_positions,
    cap_position_weights,
    combine_survivor_alphas,
    compute_turnover,
    filter_pre_ml_alpha_inputs_to_survivors,
    normalize_cross_sectional_scores,
    renormalize_long_short,
    select_promote_core_survivors,
)
from src.portfolio_storage import save_dynamic_portfolio_outputs
from src.run_config import get_sqlite_db_path, make_run_id, make_run_timestamp


MAX_ABS_WEIGHT = 0.05
TOP_QUANTILE = 0.20
BOTTOM_QUANTILE = 0.20
GROSS_EXPOSURE = 1.0
REBALANCE_FREQUENCY = 5
COST_BPS = 5
EXECUTION_LAG = 1
PORTFOLIO_MODES = ["long_only_top", "long_short_top_bottom"]
EXPECTED_PORTFOLIO_METHODS = {
    "equal_weight_survivors",
    "stress_score_weighted_survivors",
    "inverse_turnover_weighted_survivors",
    "hybrid_survivor_weighted_portfolio",
}
REQUIRED_INPUT_TABLES = [
    "survivor_alpha_registry_current",
    "pre_ml_alpha_inputs_current",
    "clean_close_prices_current",
    "benchmark_prices_current",
]


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required input tables are missing from {db_path}: {missing_tables}")


def _normalize_long_only(positions: pd.DataFrame, gross_exposure: float = 1.0) -> pd.DataFrame:
    output = positions.astype(float).fillna(0.0).clip(lower=0.0).copy()
    row_gross = output.sum(axis=1)
    active = row_gross.gt(0)
    output.loc[active] = output.loc[active].div(row_gross.loc[active], axis=0).mul(gross_exposure)
    output.loc[~active] = 0.0
    return output.sort_index().sort_index(axis=1)


def _panel_to_long(
    panel: pd.DataFrame,
    value_name: str,
    portfolio_method: str,
    portfolio_mode: str | None = None,
) -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="The previous implementation of stack is deprecated",
            category=FutureWarning,
        )
        output = panel.stack(dropna=False).rename(value_name).reset_index()
    output = output.rename(columns={"level_0": "Date", "level_1": "ticker"})
    if "Date" not in output.columns:
        output = output.rename(columns={output.columns[0]: "Date"})
    if "ticker" not in output.columns:
        output = output.rename(columns={output.columns[1]: "ticker"})
    output.insert(1, "portfolio_method", portfolio_method)
    if portfolio_mode is not None:
        output.insert(2, "portfolio_mode", portfolio_mode)
    return output


def _load_portfolio_inputs(db_path: Path) -> dict[str, pd.DataFrame]:
    survivor_registry_all = load_table("survivor_alpha_registry_current", db_path=db_path)
    if "date_frozen" in survivor_registry_all.columns:
        survivor_registry_all["date_frozen"] = pd.to_datetime(
            survivor_registry_all["date_frozen"],
            errors="coerce",
        )
    pre_ml_alpha_inputs_all = load_table("pre_ml_alpha_inputs_current", db_path=db_path)
    if "Date" in pre_ml_alpha_inputs_all.columns:
        pre_ml_alpha_inputs_all["Date"] = pd.to_datetime(pre_ml_alpha_inputs_all["Date"])
    return {
        "survivor_registry_all": survivor_registry_all,
        "pre_ml_alpha_inputs_all": pre_ml_alpha_inputs_all,
    }


def _build_benchmark(close_prices: pd.DataFrame, db_path: Path) -> tuple[str, pd.Series | None]:
    benchmark_prices = load_benchmark_prices(current=True, db_path=db_path)
    if "SPY" in benchmark_prices.columns:
        return "benchmark_prices_current.SPY", benchmark_prices["SPY"].pct_change(fill_method=None)
    if "SPY" in close_prices.columns:
        return "clean_close_prices_current.SPY", close_prices["SPY"].pct_change(fill_method=None)
    return "SPY_unavailable", None


def _validate_alpha_selection(
    *,
    survivor_registry_all: pd.DataFrame,
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    db_path: Path,
) -> list[str]:
    if survivor_registry.empty:
        raise ValueError("survivor_alpha_registry_current has no final PROMOTE_CORE alpha rows.")

    survivor_names = set(survivor_registry["alpha_name"].dropna())
    input_alpha_names = set(pre_ml_alpha_inputs["alpha_name"].dropna())
    if input_alpha_names != survivor_names:
        missing_inputs = sorted(survivor_names.difference(input_alpha_names))
        extra_inputs = sorted(input_alpha_names.difference(survivor_names))
        raise ValueError(f"Pre-ML alpha input mismatch. Missing={missing_inputs}, extra={extra_inputs}")

    decision_col = (
        "promotion_decision_final"
        if "promotion_decision_final" in survivor_registry_all.columns
        else "promotion_decision"
    )
    non_core_names = set()
    if {"alpha_name", decision_col}.issubset(survivor_registry_all.columns):
        non_core_names = set(
            survivor_registry_all.loc[
                ~survivor_registry_all[decision_col].eq("PROMOTE_CORE"),
                "alpha_name",
            ].dropna()
        )
    leaked_non_core_names = sorted(input_alpha_names.intersection(non_core_names))
    if leaked_non_core_names:
        raise ValueError(f"Non-core survivor alpha names leaked into portfolio inputs: {leaked_non_core_names}")

    overlay_name_overlap: list[str] = []
    if table_exists("regime_context_alpha_metadata_current", db_path=db_path):
        overlay_metadata = load_table("regime_context_alpha_metadata_current", db_path=db_path)
        if "alpha_name" in overlay_metadata.columns:
            overlay_name_overlap = sorted(
                survivor_names.intersection(set(overlay_metadata["alpha_name"].dropna()))
            )
    if overlay_name_overlap:
        raise ValueError(f"Regime overlay names leaked into survivor selection: {overlay_name_overlap}")
    return overlay_name_overlap


def _build_validation_report(
    *,
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    portfolio_alpha_pool: pd.DataFrame,
    portfolio_weights: pd.DataFrame,
    portfolio_backtest_results: pd.DataFrame,
    portfolio_performance_summary: pd.DataFrame,
    overlay_name_overlap: list[str],
) -> pd.DataFrame:
    decision_col = (
        "promotion_decision_final"
        if "promotion_decision_final" in portfolio_alpha_pool.columns
        else "promotion_decision"
        if "promotion_decision" in portfolio_alpha_pool.columns
        else None
    )
    decision_values = (
        sorted(portfolio_alpha_pool[decision_col].dropna().unique())
        if decision_col is not None and decision_col in portfolio_alpha_pool.columns
        else []
    )
    method_values = (
        set(portfolio_alpha_pool["portfolio_method"].dropna().unique())
        if "portfolio_method" in portfolio_alpha_pool.columns
        else set()
    )
    mode_values = (
        set(portfolio_performance_summary["portfolio_mode"].dropna().unique())
        if "portfolio_mode" in portfolio_performance_summary.columns
        else set()
    )
    survivor_names = set(survivor_registry["alpha_name"].dropna())
    input_names = set(pre_ml_alpha_inputs["alpha_name"].dropna())

    checks = [
        {
            "check_name": "final_promote_core_exists",
            "passed": len(survivor_names) > 0,
            "details": f"Final PROMOTE_CORE alpha rows: {len(survivor_names)}",
        },
        {
            "check_name": "pre_ml_only_final_core_names",
            "passed": input_names == survivor_names,
            "details": f"pre_ml_names={sorted(input_names)}; survivor_names={sorted(survivor_names)}",
        },
        {
            "check_name": "no_satellite_or_watchlist_used",
            "passed": set(decision_values).issubset({"PROMOTE_CORE"}),
            "details": f"Portfolio alpha pool decisions: {decision_values}",
        },
        {
            "check_name": "regime_overlays_excluded",
            "passed": len(overlay_name_overlap) == 0,
            "details": f"Overlay name overlap: {overlay_name_overlap}",
        },
        {
            "check_name": "portfolio_outputs_non_empty",
            "passed": all(
                not artifact.empty
                for artifact in [
                    portfolio_alpha_pool,
                    portfolio_weights,
                    portfolio_backtest_results,
                    portfolio_performance_summary,
                ]
            ),
            "details": (
                f"alpha_pool={len(portfolio_alpha_pool)}, weights={len(portfolio_weights)}, "
                f"returns={len(portfolio_backtest_results)}, summary={len(portfolio_performance_summary)}"
            ),
        },
        {
            "check_name": "portfolio_methods_created",
            "passed": method_values == EXPECTED_PORTFOLIO_METHODS,
            "details": f"Methods: {sorted(method_values)}",
        },
        {
            "check_name": "long_only_and_long_short_supported",
            "passed": mode_values == set(PORTFOLIO_MODES),
            "details": f"Modes: {sorted(mode_values)}",
        },
        {
            "check_name": "execution_lag_is_one_day",
            "passed": (
                "execution_lag" in portfolio_performance_summary.columns
                and set(portfolio_performance_summary["execution_lag"].dropna().astype(int)) == {EXECUTION_LAG}
            ),
            "details": f"Execution lag values: {sorted(portfolio_performance_summary.get('execution_lag', pd.Series(dtype=object)).dropna().unique().tolist())}",
        },
    ]
    return pd.DataFrame(checks, columns=["check_name", "passed", "details"])


def _build_summary(
    *,
    run_id: str,
    run_timestamp: str,
    portfolio_version: str,
    survivor_registry: pd.DataFrame,
    pre_ml_alpha_inputs: pd.DataFrame,
    portfolio_alpha_pool: pd.DataFrame,
    portfolio_weights: pd.DataFrame,
    portfolio_backtest_results: pd.DataFrame,
    portfolio_performance_summary: pd.DataFrame,
    benchmark_source: str,
) -> pd.DataFrame:
    alpha_names = (
        sorted(portfolio_alpha_pool["alpha_name"].dropna().unique().tolist())
        if "alpha_name" in portfolio_alpha_pool.columns
        else []
    )
    method_names = (
        sorted(portfolio_alpha_pool["portfolio_method"].dropna().unique().tolist())
        if "portfolio_method" in portfolio_alpha_pool.columns
        else []
    )
    mode_names = (
        sorted(portfolio_performance_summary["portfolio_mode"].dropna().unique().tolist())
        if "portfolio_mode" in portfolio_performance_summary.columns
        else []
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "portfolio_version", "value": portfolio_version},
            {"metric": "n_promote_core_survivors", "value": survivor_registry["alpha_name"].nunique()},
            {"metric": "pre_ml_alpha_input_rows", "value": len(pre_ml_alpha_inputs)},
            {"metric": "alpha_names_used", "value": ", ".join(alpha_names)},
            {"metric": "portfolio_methods", "value": ", ".join(method_names)},
            {"metric": "portfolio_modes", "value": ", ".join(mode_names)},
            {"metric": "portfolio_alpha_pool_rows", "value": len(portfolio_alpha_pool)},
            {"metric": "portfolio_weights_rows", "value": len(portfolio_weights)},
            {"metric": "portfolio_return_rows", "value": len(portfolio_backtest_results)},
            {"metric": "portfolio_result_rows", "value": len(portfolio_performance_summary)},
            {"metric": "cost_bps", "value": COST_BPS},
            {"metric": "execution_lag", "value": EXECUTION_LAG},
            {"metric": "benchmark_source", "value": benchmark_source},
        ]
    )


def run_09_portfolio_construction(
    db_path=None,
    portfolio_version: str = "phase9_portfolio_v1",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 09 portfolio construction notebook core logic as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    resolved_run_id = run_id or make_run_id(prefix="phase9_nb09_portfolio")
    run_timestamp = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    inputs = _load_portfolio_inputs(resolved_db_path)
    survivor_registry_all = inputs["survivor_registry_all"]
    pre_ml_alpha_inputs_all = inputs["pre_ml_alpha_inputs_all"]

    survivor_registry = select_promote_core_survivors(survivor_registry_all)
    pre_ml_alpha_inputs = filter_pre_ml_alpha_inputs_to_survivors(
        pre_ml_alpha_inputs_all,
        survivor_registry,
    )
    overlay_name_overlap = _validate_alpha_selection(
        survivor_registry_all=survivor_registry_all,
        survivor_registry=survivor_registry,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        db_path=resolved_db_path,
    )

    ohlcv = load_ohlcv_panels(current=True, db_path=resolved_db_path)
    close_prices = ohlcv["close"].sort_index().sort_index(axis=1)
    benchmark_source, spy_returns = _build_benchmark(close_prices, resolved_db_path)

    survivor_names = sorted(survivor_registry["alpha_name"].dropna().unique())
    alpha_panels = build_alpha_signal_stack(pre_ml_alpha_inputs) if not pre_ml_alpha_inputs.empty else {}
    alpha_panels = {name: panel for name, panel in alpha_panels.items() if name in survivor_names}
    portfolio_alpha_pool = build_survivor_weight_table(survivor_registry)

    portfolio_score_records = []
    portfolio_weight_records = []
    portfolio_return_records = []
    portfolio_summary_records = []

    for portfolio_method in sorted(portfolio_alpha_pool["portfolio_method"].unique()):
        method_weights = portfolio_alpha_pool.loc[
            portfolio_alpha_pool["portfolio_method"].eq(portfolio_method)
        ].set_index("alpha_name")["component_weight"]
        raw_score = combine_survivor_alphas(alpha_panels, method="custom_weight", weights=method_weights)
        normalized_score = normalize_cross_sectional_scores(raw_score)
        portfolio_score_records.append(
            _panel_to_long(normalized_score, "combined_alpha_score", portfolio_method)
        )

        target_long_only = build_long_only_top_bucket_positions(
            normalized_score,
            top_quantile=TOP_QUANTILE,
            gross_exposure=GROSS_EXPOSURE,
        )
        target_long_short = build_target_positions(
            normalized_score,
            top_quantile=TOP_QUANTILE,
            bottom_quantile=BOTTOM_QUANTILE,
            gross_exposure=GROSS_EXPOSURE,
        )

        target_by_mode = {
            "long_only_top": target_long_only,
            "long_short_top_bottom": target_long_short,
        }

        for portfolio_mode, target_positions in target_by_mode.items():
            scheduled_positions = apply_rebalance_schedule(
                target_positions,
                rebalance_frequency=REBALANCE_FREQUENCY,
            )
            capped_positions = cap_position_weights(scheduled_positions, max_abs_weight=MAX_ABS_WEIGHT)
            if portfolio_mode == "long_only_top":
                final_positions = _normalize_long_only(capped_positions, gross_exposure=GROSS_EXPOSURE)
            else:
                final_positions = renormalize_long_short(capped_positions, gross_exposure=GROSS_EXPOSURE)

            returns = compute_strategy_returns(
                positions=final_positions,
                close_prices=close_prices,
                cost_bps=COST_BPS,
                execution_lag=EXECUTION_LAG,
            )
            metrics_long = compute_portfolio_metrics(
                strategy_returns=returns,
                benchmark_returns=spy_returns,
            )
            metrics = metrics_long.set_index("metric")["value"].to_dict()
            turnover = compute_turnover(final_positions)
            active_weights = final_positions.abs().sum(axis=1).gt(0)

            portfolio_weight_records.append(
                _panel_to_long(final_positions, "weight", portfolio_method, portfolio_mode)
            )

            returns_output = returns.reset_index().rename(columns={"index": "Date"})
            if "Date" not in returns_output.columns:
                returns_output = returns_output.rename(columns={returns_output.columns[0]: "Date"})
            returns_output.insert(1, "portfolio_method", portfolio_method)
            returns_output.insert(2, "portfolio_mode", portfolio_mode)
            if spy_returns is not None:
                returns_output["benchmark_return"] = spy_returns.reindex(returns.index).to_numpy()
            else:
                returns_output["benchmark_return"] = np.nan
            portfolio_return_records.append(returns_output)

            portfolio_summary_records.append(
                {
                    "portfolio_method": portfolio_method,
                    "portfolio_mode": portfolio_mode,
                    "n_survivor_alphas": len(alpha_panels),
                    "n_dates": int(final_positions.shape[0]),
                    "n_tickers": int(final_positions.shape[1]),
                    "annualized_return": metrics.get("annualized_return"),
                    "annualized_volatility": metrics.get("annualized_volatility"),
                    "sharpe": metrics.get("sharpe"),
                    "max_drawdown": metrics.get("max_drawdown"),
                    "hit_rate": metrics.get("hit_rate"),
                    "total_return": metrics.get("total_return"),
                    "benchmark_total_return": metrics.get("benchmark_total_return"),
                    "excess_return": metrics.get("excess_return"),
                    "avg_turnover": float(turnover.mean()) if not turnover.empty else np.nan,
                    "median_turnover": float(turnover.median()) if not turnover.empty else np.nan,
                    "max_turnover": float(turnover.max()) if not turnover.empty else np.nan,
                    "mean_gross_exposure": float(final_positions.abs().sum(axis=1).mean()),
                    "mean_net_exposure": float(final_positions.sum(axis=1).mean()),
                    "active_day_pct": float(active_weights.mean()) if len(active_weights) else np.nan,
                    "cost_bps": COST_BPS,
                    "execution_lag": EXECUTION_LAG,
                    "benchmark_source": benchmark_source,
                }
            )

    portfolio_alpha_scores = (
        pd.concat(portfolio_score_records, ignore_index=True)
        if portfolio_score_records
        else pd.DataFrame(columns=["Date", "portfolio_method", "ticker", "combined_alpha_score"])
    )
    portfolio_weights = (
        pd.concat(portfolio_weight_records, ignore_index=True)
        if portfolio_weight_records
        else pd.DataFrame(columns=["Date", "portfolio_method", "portfolio_mode", "ticker", "weight"])
    )
    portfolio_backtest_results = (
        pd.concat(portfolio_return_records, ignore_index=True)
        if portfolio_return_records
        else pd.DataFrame(
            columns=[
                "Date",
                "portfolio_method",
                "portfolio_mode",
                "gross_return",
                "turnover",
                "transaction_cost",
                "net_return",
                "benchmark_return",
            ]
        )
    )
    portfolio_performance_summary = (
        pd.DataFrame(portfolio_summary_records)
        .sort_values(["portfolio_mode", "sharpe", "total_return"], ascending=[True, False, False])
        .reset_index(drop=True)
        if portfolio_summary_records
        else pd.DataFrame(
            columns=[
                "portfolio_method",
                "portfolio_mode",
                "n_survivor_alphas",
                "n_dates",
                "n_tickers",
                "annualized_return",
                "annualized_volatility",
                "sharpe",
                "max_drawdown",
                "hit_rate",
                "total_return",
                "benchmark_total_return",
                "excess_return",
                "avg_turnover",
                "median_turnover",
                "max_turnover",
                "mean_gross_exposure",
                "mean_net_exposure",
                "active_day_pct",
                "cost_bps",
                "execution_lag",
                "benchmark_source",
            ]
        )
    )
    benchmark_comparison = portfolio_performance_summary[
        [
            column
            for column in [
                "portfolio_method",
                "portfolio_mode",
                "benchmark_source",
                "benchmark_total_return",
                "excess_return",
            ]
            if column in portfolio_performance_summary.columns
        ]
    ].copy()
    portfolio_validation_report = _build_validation_report(
        survivor_registry=survivor_registry,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        portfolio_alpha_pool=portfolio_alpha_pool,
        portfolio_weights=portfolio_weights,
        portfolio_backtest_results=portfolio_backtest_results,
        portfolio_performance_summary=portfolio_performance_summary,
        overlay_name_overlap=overlay_name_overlap,
    )
    if not portfolio_validation_report["passed"].all():
        failed = portfolio_validation_report.loc[
            ~portfolio_validation_report["passed"],
            ["check_name", "details"],
        ].to_dict("records")
        raise ValueError(f"Portfolio validation failed: {failed}")

    summary = _build_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        portfolio_version=portfolio_version,
        survivor_registry=survivor_registry,
        pre_ml_alpha_inputs=pre_ml_alpha_inputs,
        portfolio_alpha_pool=portfolio_alpha_pool,
        portfolio_weights=portfolio_weights,
        portfolio_backtest_results=portfolio_backtest_results,
        portfolio_performance_summary=portfolio_performance_summary,
        benchmark_source=benchmark_source,
    )

    saved_paths = None
    if write:
        saved_paths = save_dynamic_portfolio_outputs(
            alpha_pool=portfolio_alpha_pool,
            weights=portfolio_weights,
            backtest_results=portfolio_backtest_results,
            performance_summary=portfolio_performance_summary,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            portfolio_version=portfolio_version,
        )

    _log(verbose, f"Loaded 09 portfolio inputs from {resolved_db_path}")
    _log(verbose, f"  survivor_registry_all: {len(survivor_registry_all):,}")
    _log(verbose, f"  final PROMOTE_CORE survivors: {len(survivor_names):,}")
    _log(verbose, f"  pre_ml_alpha_inputs: {len(pre_ml_alpha_inputs):,}")
    _log(verbose, f"  close_prices shape: {close_prices.shape}")
    _log(verbose, f"  benchmark_source: {benchmark_source}")
    _log(verbose, "09 portfolio output rows")
    for artifact_name, artifact in [
        ("portfolio_alpha_pool", portfolio_alpha_pool),
        ("portfolio_alpha_scores", portfolio_alpha_scores),
        ("portfolio_weights", portfolio_weights),
        ("portfolio_backtest_results", portfolio_backtest_results),
        ("portfolio_performance_summary", portfolio_performance_summary),
        ("benchmark_comparison", benchmark_comparison),
        ("portfolio_validation_report", portfolio_validation_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "portfolio_results": portfolio_performance_summary,
        "portfolio_performance_summary": portfolio_performance_summary,
        "portfolio_alpha_pool": portfolio_alpha_pool,
        "portfolio_alpha_scores": portfolio_alpha_scores,
        "portfolio_weights": portfolio_weights,
        "portfolio_returns": portfolio_backtest_results,
        "portfolio_backtest_results": portfolio_backtest_results,
        "benchmark_comparison": benchmark_comparison,
        "portfolio_validation_report": portfolio_validation_report,
        "summary": summary,
        "survivor_registry": survivor_registry,
        "pre_ml_alpha_inputs": pre_ml_alpha_inputs,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
