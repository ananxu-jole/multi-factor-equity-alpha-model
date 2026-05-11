from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_table, table_exists
from src.run_config import get_sqlite_db_path


DASHBOARD_TABLES = [
    "survivor_alpha_registry_current",
    "pre_ml_alpha_inputs_current",
    "portfolio_alpha_pool_current",
    "portfolio_weights_current",
    "portfolio_backtest_results_current",
    "portfolio_performance_summary_current",
    "alpha_dynamic_weight_audit_current",
    "alpha_stress_gate_current",
    "constructed_alpha_wfv_gate_current",
    "signal_diversity_selection_current",
    "survivor_cluster_summary_current",
]


def load_dashboard_tables(db_path: str | Path | None = None) -> dict[str, pd.DataFrame]:
    """Load dashboard inputs from SQLite without writing any pipeline artifacts."""
    resolved_db_path = get_sqlite_db_path() if db_path is None else Path(db_path)
    tables: dict[str, pd.DataFrame] = {}
    for table_name in DASHBOARD_TABLES:
        tables[table_name] = (
            load_table(table_name, db_path=resolved_db_path)
            if table_exists(table_name, db_path=resolved_db_path)
            else pd.DataFrame()
        )
    return tables


def get_final_survivors(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Return final core survivor rows from the current registry."""
    if survivor_registry.empty:
        return survivor_registry.copy()
    registry = survivor_registry.copy()
    if "promotion_decision_final" in registry.columns:
        mask = registry["promotion_decision_final"].astype(str).eq("PROMOTE_CORE")
    elif "final_status" in registry.columns:
        mask = registry["final_status"].astype(str).str.contains("CORE|APPROVED", case=False, na=False)
    else:
        mask = pd.Series(True, index=registry.index)
    return registry.loc[mask].drop_duplicates(["alpha_name", "horizon"]).reset_index(drop=True)


def system_overview(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Build a compact survivor overview table."""
    columns = [
        "alpha_name",
        "horizon",
        "alpha_behavior_cluster",
        "original_promotion_decision",
        "promotion_decision_final",
        "source_wfv_status",
        "stress_status",
        "survivor_selection_score",
        "final_status",
        "cluster_selection_reason",
    ]
    if survivor_registry.empty:
        return pd.DataFrame(columns=columns)
    output = survivor_registry.copy()
    return output[[column for column in columns if column in output.columns]].sort_values(
        ["promotion_decision_final", "survivor_selection_score", "alpha_name"],
        ascending=[True, False, True],
    ).reset_index(drop=True)


def performance_comparison(performance_summary: pd.DataFrame) -> pd.DataFrame:
    """Format portfolio performance metrics for dashboard display."""
    columns = [
        "portfolio_method",
        "portfolio_mode",
        "annualized_return",
        "annualized_volatility",
        "sharpe",
        "max_drawdown",
        "total_return",
        "excess_return",
        "avg_turnover",
    ]
    if performance_summary.empty:
        return pd.DataFrame(columns=columns)
    output = performance_summary[[column for column in columns if column in performance_summary.columns]].copy()
    return output.sort_values(["portfolio_mode", "sharpe"], ascending=[True, False]).reset_index(drop=True)


def best_portfolio_by_mode(performance_summary: pd.DataFrame, mode_pattern: str) -> pd.Series | None:
    """Return the best Sharpe portfolio row whose mode contains a case-insensitive pattern."""
    if performance_summary.empty or "portfolio_mode" not in performance_summary.columns:
        return None
    candidates = performance_summary.loc[
        performance_summary["portfolio_mode"].astype(str).str.contains(mode_pattern, case=False, na=False)
    ].copy()
    if candidates.empty:
        return None
    candidates["sharpe"] = pd.to_numeric(candidates.get("sharpe"), errors="coerce")
    return candidates.sort_values(["sharpe", "portfolio_method"], ascending=[False, True]).iloc[0]


def portfolio_return_series(backtest_results: pd.DataFrame, portfolio_row: pd.Series | None) -> pd.DataFrame:
    """Return sorted daily returns for a selected portfolio row."""
    if backtest_results.empty or portfolio_row is None:
        return pd.DataFrame()
    required = {"Date", "portfolio_method", "portfolio_mode", "net_return"}
    if not required.issubset(backtest_results.columns):
        return pd.DataFrame()
    returns = backtest_results.loc[
        backtest_results["portfolio_method"].eq(portfolio_row["portfolio_method"])
        & backtest_results["portfolio_mode"].eq(portfolio_row["portfolio_mode"])
    ].copy()
    returns["Date"] = pd.to_datetime(returns["Date"])
    returns["net_return"] = pd.to_numeric(returns["net_return"], errors="coerce").fillna(0.0)
    if "benchmark_return" in returns.columns:
        returns["benchmark_return"] = pd.to_numeric(returns["benchmark_return"], errors="coerce").fillna(0.0)
    return returns.sort_values("Date").reset_index(drop=True)


def cumulative_return_frame(returns: pd.DataFrame) -> pd.DataFrame:
    """Add portfolio and optional benchmark cumulative return columns."""
    if returns.empty or "net_return" not in returns.columns:
        return pd.DataFrame()
    output = returns.copy()
    output["portfolio_cumulative_return"] = (1.0 + output["net_return"]).cumprod() - 1.0
    if "benchmark_return" in output.columns:
        output["benchmark_cumulative_return"] = (1.0 + output["benchmark_return"]).cumprod() - 1.0
    return output


def drawdown_frame(returns: pd.DataFrame) -> pd.DataFrame:
    """Add portfolio and optional benchmark drawdown columns."""
    if returns.empty or "net_return" not in returns.columns:
        return pd.DataFrame()
    output = returns.copy()
    portfolio_curve = (1.0 + output["net_return"]).cumprod()
    output["portfolio_drawdown"] = portfolio_curve / portfolio_curve.cummax() - 1.0
    if "benchmark_return" in output.columns:
        benchmark_curve = (1.0 + output["benchmark_return"]).cumprod()
        output["benchmark_drawdown"] = benchmark_curve / benchmark_curve.cummax() - 1.0
    return output


def rolling_performance_frame(returns: pd.DataFrame) -> pd.DataFrame:
    """Add 63-day rolling return and 126-day Sharpe proxy columns."""
    if returns.empty or "net_return" not in returns.columns:
        return pd.DataFrame()
    output = returns.copy()
    daily = output["net_return"].astype(float)
    output["rolling_63d_return"] = (1.0 + daily).rolling(63).apply(np.prod, raw=True) - 1.0
    rolling_mean = daily.rolling(126).mean()
    rolling_std = daily.rolling(126).std()
    output["rolling_126d_sharpe_proxy"] = (rolling_mean / rolling_std.replace(0.0, np.nan)) * np.sqrt(252)
    return output


def survivor_alpha_values(pre_ml_alpha_inputs: pd.DataFrame, final_survivors: pd.DataFrame) -> pd.DataFrame:
    """Return survivor alpha values in wide Date/ticker x alpha_name form."""
    if pre_ml_alpha_inputs.empty or final_survivors.empty:
        return pd.DataFrame()
    names = final_survivors["alpha_name"].dropna().unique().tolist()
    values = pre_ml_alpha_inputs.loc[
        pre_ml_alpha_inputs["alpha_name"].isin(names),
        ["Date", "ticker", "alpha_name", "alpha_value"],
    ].copy()
    if values.empty:
        return pd.DataFrame()
    values["alpha_value"] = pd.to_numeric(values["alpha_value"], errors="coerce")
    return values.pivot_table(
        index=["Date", "ticker"],
        columns="alpha_name",
        values="alpha_value",
        aggfunc="first",
    )


def survivor_correlation_matrix(pre_ml_alpha_inputs: pd.DataFrame, final_survivors: pd.DataFrame) -> pd.DataFrame:
    """Compute the survivor alpha value correlation matrix."""
    wide = survivor_alpha_values(pre_ml_alpha_inputs, final_survivors)
    return wide.corr(min_periods=20) if not wide.empty else pd.DataFrame()


def rolling_survivor_correlation(
    pre_ml_alpha_inputs: pd.DataFrame,
    final_survivors: pd.DataFrame,
    window: int = 63,
) -> pd.DataFrame:
    """Compute average pairwise survivor correlation by date over a rolling window."""
    if pre_ml_alpha_inputs.empty or final_survivors.empty:
        return pd.DataFrame(columns=["Date", "rolling_avg_abs_corr"])
    names = final_survivors["alpha_name"].dropna().unique().tolist()
    if len(names) < 2:
        return pd.DataFrame(columns=["Date", "rolling_avg_abs_corr"])
    values = pre_ml_alpha_inputs.loc[
        pre_ml_alpha_inputs["alpha_name"].isin(names),
        ["Date", "ticker", "alpha_name", "alpha_value"],
    ].copy()
    if values.empty:
        return pd.DataFrame(columns=["Date", "rolling_avg_abs_corr"])
    values["Date"] = pd.to_datetime(values["Date"])
    daily = values.pivot_table(index=["Date", "ticker"], columns="alpha_name", values="alpha_value", aggfunc="first")
    daily_corr = daily.groupby(level=0).corr().reset_index()
    records = []
    for date, group in daily_corr.groupby("Date"):
        corr_matrix = group.set_index("alpha_name")[names]
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        records.append({"Date": date, "avg_abs_corr": upper.stack().abs().mean()})
    corr_by_date = pd.DataFrame(records).sort_values("Date")
    corr_by_date["rolling_avg_abs_corr"] = corr_by_date["avg_abs_corr"].rolling(window, min_periods=5).mean()
    return corr_by_date[["Date", "rolling_avg_abs_corr"]]


def portfolio_alpha_contribution(
    portfolio_alpha_pool: pd.DataFrame,
    final_survivors: pd.DataFrame,
) -> pd.DataFrame:
    """Return static portfolio component weights for final survivors."""
    columns = [
        "portfolio_method",
        "alpha_name",
        "horizon",
        "component_weight",
        "raw_weight_score",
        "weighting_rule",
        "survivor_tier",
        "alpha_role",
        "pass_rate",
        "worst_degradation",
        "avg_turnover_proxy",
    ]
    if portfolio_alpha_pool.empty or final_survivors.empty:
        return pd.DataFrame(columns=columns)
    names = final_survivors["alpha_name"].dropna().unique().tolist()
    output = portfolio_alpha_pool.loc[portfolio_alpha_pool["alpha_name"].isin(names)].copy()
    return output[[column for column in columns if column in output.columns]].sort_values(
        ["portfolio_method", "component_weight", "alpha_name"],
        ascending=[True, False, True],
    ).reset_index(drop=True)


def average_dynamic_weights(
    alpha_dynamic_weight_audit: pd.DataFrame,
    final_survivors: pd.DataFrame,
) -> pd.DataFrame:
    """Average dynamic component weights through time for final survivor alphas."""
    if alpha_dynamic_weight_audit.empty or final_survivors.empty:
        return pd.DataFrame()
    names = final_survivors["alpha_name"].dropna().unique().tolist()
    weights = alpha_dynamic_weight_audit.loc[alpha_dynamic_weight_audit["alpha_name"].isin(names)].copy()
    if weights.empty or "Date" not in weights.columns or "weight" not in weights.columns:
        return pd.DataFrame()
    weights["Date"] = pd.to_datetime(weights["Date"])
    weights["weight"] = pd.to_numeric(weights["weight"], errors="coerce")
    return (
        weights.groupby(["Date", "alpha_name"], as_index=False)["weight"]
        .mean()
        .sort_values(["alpha_name", "Date"])
        .reset_index(drop=True)
    )


def stress_wfv_interpretation(
    final_survivors: pd.DataFrame,
    alpha_stress_gate: pd.DataFrame,
    constructed_alpha_wfv_gate: pd.DataFrame,
) -> pd.DataFrame:
    """Join final survivors to stress and WFV status rows."""
    if final_survivors.empty:
        return pd.DataFrame()
    keys = ["alpha_name", "horizon"]
    output = final_survivors[keys + [c for c in ["interpretation_notes", "cluster_selection_reason"] if c in final_survivors.columns]].copy()
    if not alpha_stress_gate.empty:
        stress_cols = keys + [
            column
            for column in [
                "status",
                "promotion_decision",
                "survivor_tier",
                "pass_rate",
                "worst_degradation",
                "failure_notes",
                "stress_gate_notes",
                "failure_category",
            ]
            if column in alpha_stress_gate.columns
        ]
        output = output.merge(
            alpha_stress_gate[stress_cols].rename(columns={"status": "stress_gate_status"}),
            on=keys,
            how="left",
        )
    if not constructed_alpha_wfv_gate.empty:
        wfv_cols = keys + [
            column
            for column in [
                "status",
                "effective_mean_test_ic",
                "effective_test_ic_ir",
                "persistence_ratio",
                "sign_consistency",
                "constructed_alpha_wfv_notes",
            ]
            if column in constructed_alpha_wfv_gate.columns
        ]
        output = output.merge(
            constructed_alpha_wfv_gate[wfv_cols].rename(columns={"status": "wfv_status"}),
            on=keys,
            how="left",
        )
    return output


def expansion_readiness_summary(
    final_survivors: pd.DataFrame,
    performance_summary: pd.DataFrame,
    verification_checks_pass: bool,
) -> pd.DataFrame:
    """Build the current universe-expansion readiness summary."""
    best_long_only = best_portfolio_by_mode(performance_summary, "long_only")
    if best_long_only is None:
        values = {
            "current_best_portfolio_method": pd.NA,
            "current_best_portfolio_mode": pd.NA,
            "current_best_sharpe": pd.NA,
            "current_max_drawdown": pd.NA,
            "current_turnover": pd.NA,
        }
        ready = False
    else:
        sharpe = pd.to_numeric(pd.Series([best_long_only.get("sharpe")]), errors="coerce").iloc[0]
        max_drawdown = pd.to_numeric(pd.Series([best_long_only.get("max_drawdown")]), errors="coerce").iloc[0]
        avg_turnover = pd.to_numeric(pd.Series([best_long_only.get("avg_turnover")]), errors="coerce").iloc[0]
        values = {
            "current_best_portfolio_method": best_long_only.get("portfolio_method"),
            "current_best_portfolio_mode": best_long_only.get("portfolio_mode"),
            "current_best_sharpe": sharpe,
            "current_max_drawdown": max_drawdown,
            "current_turnover": avg_turnover,
        }
        ready = (
            len(final_survivors) >= 2
            and pd.notna(sharpe)
            and sharpe > 1.0
            and pd.notna(max_drawdown)
            and max_drawdown > -0.50
            and pd.notna(avg_turnover)
            and avg_turnover < 0.10
            and bool(verification_checks_pass)
        )
    values["n_final_survivors"] = int(len(final_survivors))
    values["verification_checks_pass"] = bool(verification_checks_pass)
    values["expansion_readiness_flag"] = "READY_FOR_UNIVERSE_EXPANSION" if ready else "NOT_READY_FOR_EXPANSION"
    return pd.DataFrame([values])


__all__ = [
    "average_dynamic_weights",
    "best_portfolio_by_mode",
    "cumulative_return_frame",
    "drawdown_frame",
    "expansion_readiness_summary",
    "get_final_survivors",
    "load_dashboard_tables",
    "performance_comparison",
    "portfolio_alpha_contribution",
    "portfolio_return_series",
    "rolling_performance_frame",
    "rolling_survivor_correlation",
    "stress_wfv_interpretation",
    "survivor_correlation_matrix",
    "system_overview",
]
