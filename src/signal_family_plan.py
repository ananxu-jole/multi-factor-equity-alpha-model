from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from src.run_config import get_sqlite_db_path


SIGNAL_FAMILY_PLAN_TABLES = {
    "plan": (
        "signal_family_expansion_plan_current",
        "signal_family_expansion_plan_history",
    ),
}


SIGNAL_FAMILY_PLAN_COLUMNS = [
    "expansion_wave",
    "family_name",
    "proposed_signal_name",
    "implementation_status",
    "formula_description",
    "required_inputs",
    "expected_horizon",
    "expected_diversification_role",
    "implementation_priority",
    "implementation_batch",
    "reason_added",
    "economic_intuition",
    "expected_correlation_behavior_vs_volatility",
    "risk_of_redundancy",
    "notes",
]


WAVE_1_IMPLEMENTED_SIGNALS = {
    "intraday_reversal_1d",
    "gap_reversal_1d",
    "up_down_volume_pressure_20",
    "amihud_illiq_20",
    "market_beta_change_60",
}

WAVE_2_REASON_ADDED = (
    "Added after 03E/03G showed approved pool still dominated by "
    "volatility/defensive/liquidity cluster."
)


def build_signal_family_expansion_plan() -> pd.DataFrame:
    """Return the Phase 2 signal-family expansion roadmap as a structured table."""
    rows = [
        {
            "family_name": "mean_reversion",
            "proposed_signal_name": "intraday_reversal_1d",
            "formula_description": "Negative same-day open-to-close return, ranked cross-sectionally by Date.",
            "required_inputs": "open,close",
            "expected_horizon": "1-5d",
            "expected_diversification_role": "Adds very short-horizon pullback behavior distinct from realized-volatility ranking.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Short-term overreaction and liquidity-demand shocks can reverse when pressure fades.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; may overlap during selloffs but should differ on normal pullbacks.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Keep simple and avoid using future intraday information beyond the same completed bar.",
        },
        {
            "family_name": "short_term_reversal",
            "proposed_signal_name": "gap_reversal_1d",
            "formula_description": "Negative overnight gap from prior close to current open, ranked cross-sectionally.",
            "required_inputs": "open,close",
            "expected_horizon": "1-5d",
            "expected_diversification_role": "Separates overnight dislocation reversal from close-to-close volatility effects.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Large overnight repricing can overshoot before intraday liquidity normalizes.",
            "expected_correlation_behavior_vs_volatility": "Moderate in stress, lower in normal regimes.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Use only current open and previous close, with execution lag handled downstream.",
        },
        {
            "family_name": "volume_flow",
            "proposed_signal_name": "up_down_volume_pressure_20",
            "formula_description": "Rolling difference between volume on up days and volume on down days divided by rolling total volume.",
            "required_inputs": "close,volume",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Adds participation/flow information not captured by price volatility alone.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Persistent accumulation or distribution can reveal informed demand before price trend is obvious.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; flow pressure can be positive or negative independent of volatility level.",
            "risk_of_redundancy": "LOW",
            "notes": "Do not dollar-weight by future prices; use contemporaneous close and trailing windows only.",
        },
        {
            "family_name": "volume_flow",
            "proposed_signal_name": "volume_price_confirmation_20",
            "formula_description": "20-day return multiplied by rolling volume z-score, ranked cross-sectionally.",
            "required_inputs": "close,volume",
            "expected_horizon": "10-20d",
            "expected_diversification_role": "Tests whether moves supported by unusual volume behave differently from pure momentum.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Price moves with participation may be more durable than low-volume moves.",
            "expected_correlation_behavior_vs_volatility": "Moderate; volume spikes can accompany volatility but sign should depend on return direction.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Clip or rank to reduce domination by single extreme volume events.",
        },
        {
            "family_name": "liquidity",
            "proposed_signal_name": "amihud_illiq_20",
            "formula_description": "Rolling mean of abs daily return divided by dollar volume, direction documented before scoring.",
            "required_inputs": "close,volume",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Adds tradability/liquidity-premium behavior distinct from volatility ranking.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Illiquid names may require compensation or experience stronger price impact after shocks.",
            "expected_correlation_behavior_vs_volatility": "Moderate; related to volatility but scaled by trading capacity.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Handle zero dollar volume safely and leave missing values as NaN.",
        },
        {
            "family_name": "liquidity",
            "proposed_signal_name": "dollar_volume_change_20",
            "formula_description": "20-day rolling dollar volume divided by 60-day rolling dollar volume minus one.",
            "required_inputs": "close,volume",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Captures changing investor attention and liquidity regime.",
            "implementation_priority": "LOW",
            "economic_intuition": "Rising trading activity can precede repricing or improve signal reliability.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; activity changes need not imply high realized volatility.",
            "risk_of_redundancy": "LOW",
            "notes": "Use trailing averages only.",
        },
        {
            "family_name": "correlation_dispersion",
            "proposed_signal_name": "market_beta_change_60",
            "formula_description": "Rolling 20-day beta to benchmark minus rolling 60-day beta, ranked cross-sectionally.",
            "required_inputs": "close,benchmark_close",
            "expected_horizon": "10-20d",
            "expected_diversification_role": "Identifies changing market sensitivity rather than standalone volatility.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Rapid beta changes can reveal crowding, de-risking, or idiosyncratic repricing.",
            "expected_correlation_behavior_vs_volatility": "Moderate; beta instability may rise in stress but differs from low/high vol.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Use benchmark returns from existing clean benchmark panels.",
        },
        {
            "family_name": "correlation_dispersion",
            "proposed_signal_name": "idiosyncratic_vol_ratio_20_60",
            "formula_description": "20-day residual volatility to benchmark divided by 60-day residual volatility minus one.",
            "required_inputs": "close,benchmark_close",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Separates idiosyncratic shock behavior from broad market volatility.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Firm-specific risk shocks can mean-revert or persist independently of market stress.",
            "expected_correlation_behavior_vs_volatility": "Moderate to high in stress, but more stock-specific than raw volatility.",
            "risk_of_redundancy": "MEDIUM_HIGH",
            "notes": "Treat as diagnostic candidate; 03G should decide whether it adds true diversity.",
        },
        {
            "family_name": "volatility_change",
            "proposed_signal_name": "volatility_shock_5_20",
            "formula_description": "5-day realized volatility divided by 20-day realized volatility minus one.",
            "required_inputs": "close",
            "expected_horizon": "1-10d",
            "expected_diversification_role": "Captures volatility acceleration rather than persistent high-volatility level.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Fresh volatility shocks may behave differently from names that are simply always volatile.",
            "expected_correlation_behavior_vs_volatility": "Moderate; intentionally related but less level-dominated.",
            "risk_of_redundancy": "MEDIUM_HIGH",
            "notes": "Include only if 03G shows it is not a clone of volatility_20.",
        },
        {
            "family_name": "volatility_shock",
            "proposed_signal_name": "range_expansion_5_20",
            "formula_description": "5-day average high-low range divided by 20-day average high-low range minus one.",
            "required_inputs": "high,low,close",
            "expected_horizon": "1-10d",
            "expected_diversification_role": "Uses intraday range expansion to capture fresh information shocks.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Range expansion can indicate uncertainty or informed trading before close-to-close vol fully adjusts.",
            "expected_correlation_behavior_vs_volatility": "Moderate; related but not identical to close-to-close realized volatility.",
            "risk_of_redundancy": "MEDIUM_HIGH",
            "notes": "Use normalized range such as high-low divided by close to control price scale.",
        },
        {
            "family_name": "selective_momentum",
            "proposed_signal_name": "low_vol_momentum_60",
            "formula_description": "60-day return divided by 60-day realized volatility, with separate family label from defensive quality.",
            "required_inputs": "close",
            "expected_horizon": "20d",
            "expected_diversification_role": "Targets smoother trend continuation rather than crisis-volatility reversal.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Persistent trends with lower noise may be more stable than high-beta momentum.",
            "expected_correlation_behavior_vs_volatility": "Negative to moderate; should favor lower noise but may overlap with low-vol strength.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Only useful if metadata and 03G distinguish it from existing risk-adjusted momentum.",
        },
        {
            "family_name": "selective_trend",
            "proposed_signal_name": "trend_consistency_20",
            "formula_description": "Share of positive daily returns over 20 days times 20-day return sign/magnitude.",
            "required_inputs": "close",
            "expected_horizon": "10-20d",
            "expected_diversification_role": "Captures trend smoothness and breadth of daily participation.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Consistent incremental buying can be more reliable than one jump-driven return.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; smooth trends should not require high realized volatility.",
            "risk_of_redundancy": "LOW_MEDIUM",
            "notes": "Keep transparent and rank cross-sectionally.",
        },
    ]
    wave_2_rows = [
        {
            "family_name": "volume_flow",
            "proposed_signal_name": "volume_acceleration_20",
            "formula_description": "Current 20-day average volume divided by prior 20-day average volume minus one.",
            "required_inputs": "volume",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Captures flow acceleration independent of volatility level.",
            "implementation_priority": "HIGH",
            "economic_intuition": "A step-change in participation can indicate attention or positioning before price-only signals diversify.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; activity can accelerate without a realized-volatility spike.",
            "risk_of_redundancy": "LOW_MEDIUM",
            "notes": "Use trailing averages only; avoid same-row forward volume information.",
        },
        {
            "family_name": "volume_flow",
            "proposed_signal_name": "price_volume_divergence_20",
            "formula_description": "20-day price return minus 20-day volume trend or rank.",
            "required_inputs": "close,volume",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Detects moves unsupported by participation.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Price moves with weak participation may be more prone to reversal or lower persistence.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; explicitly contrasts price direction with participation.",
            "risk_of_redundancy": "LOW_MEDIUM",
            "notes": "Define volume trend/rank transparently before implementation.",
        },
        {
            "family_name": "correlation_dispersion",
            "proposed_signal_name": "rolling_corr_to_market_60",
            "formula_description": "60-day rolling correlation of stock returns to benchmark or equal-weight market return.",
            "required_inputs": "close,benchmark_close",
            "expected_horizon": "10-20d",
            "expected_diversification_role": "Measures market-crowding/systematic exposure directly.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Stocks moving tightly with the market can behave differently from idiosyncratic movers.",
            "expected_correlation_behavior_vs_volatility": "Moderate; related in stress but measures co-movement rather than volatility level.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Use SPY if available, otherwise equal-weight market return from the clean universe.",
        },
        {
            "family_name": "correlation_dispersion",
            "proposed_signal_name": "idiosyncratic_return_20",
            "formula_description": "Stock 20-day return minus beta-adjusted benchmark 20-day return.",
            "required_inputs": "close,benchmark_close",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Separates stock-specific move from broad market move.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Idiosyncratic strength or weakness can survive even when raw returns are market-regime driven.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; removes a broad market component before ranking.",
            "risk_of_redundancy": "LOW_MEDIUM",
            "notes": "Estimate beta using trailing data only.",
        },
        {
            "family_name": "selective_momentum",
            "proposed_signal_name": "momentum_quality_60",
            "formula_description": "60-day return divided by 60-day realized volatility and penalized by large drawdowns.",
            "required_inputs": "close",
            "expected_horizon": "10-20d",
            "expected_diversification_role": "Trend continuation with quality filter instead of raw momentum.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Smooth positive trends may persist more reliably than jumpy or drawdown-heavy momentum.",
            "expected_correlation_behavior_vs_volatility": "Negative to moderate; penalizes noisy and drawdown-heavy names.",
            "risk_of_redundancy": "MEDIUM",
            "notes": "Keep drawdown penalty simple and trailing-only.",
        },
        {
            "family_name": "volatility_change",
            "proposed_signal_name": "realized_vol_change_20_60",
            "formula_description": "20-day realized volatility divided by 60-day realized volatility minus one.",
            "required_inputs": "close",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Captures volatility regime transition rather than volatility level.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "Volatility acceleration or normalization can differ from persistently high volatility.",
            "expected_correlation_behavior_vs_volatility": "Moderate; related to volatility but change-based rather than level-based.",
            "risk_of_redundancy": "MEDIUM_HIGH",
            "notes": "Treat as a controlled volatility-adjacent candidate and require 03G confirmation.",
        },
        {
            "family_name": "cross_sectional_relative_value",
            "proposed_signal_name": "relative_return_vs_universe_20",
            "formula_description": "Stock 20-day return minus cross-sectional average 20-day return.",
            "required_inputs": "close",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Relative performance not purely market-regime driven.",
            "implementation_priority": "HIGH",
            "economic_intuition": "Cross-sectional excess return can isolate relative winners and losers from broad market direction.",
            "expected_correlation_behavior_vs_volatility": "Low to moderate; centers returns by the same-date universe average.",
            "risk_of_redundancy": "LOW_MEDIUM",
            "notes": "Similar to residual momentum concept; use 03G to test incremental value.",
        },
        {
            "family_name": "cross_sectional_relative_value",
            "proposed_signal_name": "relative_vol_vs_universe_20",
            "formula_description": "Stock 20-day realized volatility minus cross-sectional average 20-day realized volatility.",
            "required_inputs": "close",
            "expected_horizon": "5-20d",
            "expected_diversification_role": "Relative risk positioning rather than absolute volatility level.",
            "implementation_priority": "MEDIUM",
            "economic_intuition": "A stock can become relatively risky even when broad market volatility is stable.",
            "expected_correlation_behavior_vs_volatility": "Moderate; still volatility-related but cross-sectionally centered.",
            "risk_of_redundancy": "MEDIUM_HIGH",
            "notes": "Use only if relative centering reduces redundancy versus volatility_20.",
        },
    ]

    plan = pd.DataFrame(rows)
    plan["expansion_wave"] = "wave_1"
    plan["implementation_status"] = plan["proposed_signal_name"].map(
        lambda name: "implemented" if name in WAVE_1_IMPLEMENTED_SIGNALS else "planned"
    )
    plan["reason_added"] = (
        "Initial diversity expansion roadmap from 01B after 03G identified volatility-cluster concentration."
    )

    wave_2 = pd.DataFrame(wave_2_rows)
    wave_2["expansion_wave"] = "wave_2"
    wave_2["implementation_status"] = "planned"
    wave_2["reason_added"] = WAVE_2_REASON_ADDED

    output = pd.concat([plan, wave_2], ignore_index=True)
    batch_by_signal = {
        "relative_return_vs_universe_20": "batch_1",
        "idiosyncratic_return_20": "batch_1",
        "rolling_corr_to_market_60": "batch_1",
        "volume_acceleration_20": "batch_2",
        "price_volume_divergence_20": "batch_2",
        "momentum_quality_60": "batch_3",
        "realized_vol_change_20_60": "batch_3",
    }
    output["implementation_batch"] = output["proposed_signal_name"].map(batch_by_signal)
    output.loc[
        output["implementation_status"].eq("implemented") & output["implementation_batch"].isna(),
        "implementation_batch",
    ] = "already_implemented"
    output["implementation_batch"] = output["implementation_batch"].fillna("later_or_low")
    return output.reindex(columns=SIGNAL_FAMILY_PLAN_COLUMNS)


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


def save_signal_family_expansion_plan(
    plan: pd.DataFrame,
    db_path: str | Path | None = None,
    run_id: str | None = None,
    plan_version: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Path]:
    """Save the signal-family expansion plan to current/history SQLite tables."""
    if run_id is None:
        raise ValueError("run_id is required.")
    if plan_version is None:
        raise ValueError("plan_version is required.")
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    output = plan.copy()
    output["run_id"] = run_id
    output["plan_version"] = plan_version
    output["timestamp"] = timestamp

    current_table, history_table = SIGNAL_FAMILY_PLAN_TABLES["plan"]
    with sqlite3.connect(db_path) as conn:
        output.to_sql(current_table, conn, if_exists="replace", index=False)
        if _table_exists(conn, history_table):
            _ensure_sqlite_columns(output, history_table, conn)
        output.to_sql(history_table, conn, if_exists="append", index=False)
    return {"plan": db_path}


__all__ = [
    "SIGNAL_FAMILY_PLAN_COLUMNS",
    "SIGNAL_FAMILY_PLAN_TABLES",
    "build_signal_family_expansion_plan",
    "save_signal_family_expansion_plan",
]
