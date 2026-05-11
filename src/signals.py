from __future__ import annotations

import json
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from src.signal_metadata import build_signal_metadata, build_signal_metadata_row


PHASE2_REQUIRED_PANELS = ("open", "high", "low", "close", "volume")

DISCOVERY_FAMILY_ORDER = [
    "cross_sectional_relative_return",
    "beta_neutral_return",
    "volatility_adjusted_momentum",
    "volatility_surprise",
    "reversal_overextension",
    "correlation_change",
    "liquidity_adjusted_return",
    "volume_return_interaction",
]

DISCOVERY_TRANSFORM_ORDER = ["rank", "zscore", "winsorized_zscore", "raw"]


PHASE2_SIGNAL_SPECS = [
    {
        "signal_name": "momentum_20",
        "signal_family": "momentum",
        "formula_type": "close_pct_change",
        "lookback": 20,
        "direction_convention": "higher_is_more_bullish",
        "input_fields": ["close"],
        "notes": "20-day close-to-close return, cross-sectionally standardized by date.",
    },
    {
        "signal_name": "momentum_60",
        "signal_family": "momentum",
        "formula_type": "close_pct_change",
        "lookback": 60,
        "direction_convention": "higher_is_more_bullish",
        "input_fields": ["close"],
        "notes": "60-day close-to-close return, cross-sectionally standardized by date.",
    },
    {
        "signal_name": "mean_reversion_5",
        "signal_family": "mean_reversion",
        "formula_type": "negative_distance_to_moving_average",
        "lookback": 5,
        "direction_convention": "higher_is_more_oversold",
        "input_fields": ["close"],
        "notes": "Negative price distance from 5-day moving average.",
    },
    {
        "signal_name": "mean_reversion_20",
        "signal_family": "mean_reversion",
        "formula_type": "negative_distance_to_moving_average",
        "lookback": 20,
        "direction_convention": "higher_is_more_oversold",
        "input_fields": ["close"],
        "notes": "Negative price distance from 20-day moving average.",
    },
    {
        "signal_name": "volatility_20",
        "signal_family": "volatility",
        "formula_type": "realized_return_volatility",
        "lookback": 20,
        "direction_convention": "higher_is_more_volatile",
        "input_fields": ["close"],
        "notes": "20-day realized close-to-close return volatility.",
    },
    {
        "signal_name": "volatility_60",
        "signal_family": "volatility",
        "formula_type": "realized_return_volatility",
        "lookback": 60,
        "direction_convention": "higher_is_more_volatile",
        "input_fields": ["close"],
        "notes": "60-day realized close-to-close return volatility.",
    },
    {
        "signal_name": "breakout_20",
        "signal_family": "breakout",
        "formula_type": "price_position_in_high_low_range",
        "lookback": 20,
        "direction_convention": "higher_is_closer_to_range_high",
        "input_fields": ["high", "low", "close"],
        "notes": "Close location within trailing 20-day high-low range.",
    },
    {
        "signal_name": "breakout_60",
        "signal_family": "breakout",
        "formula_type": "price_position_in_high_low_range",
        "lookback": 60,
        "direction_convention": "higher_is_closer_to_range_high",
        "input_fields": ["high", "low", "close"],
        "notes": "Close location within trailing 60-day high-low range.",
    },
    {
        "signal_name": "volume_zscore_20",
        "signal_family": "volume",
        "formula_type": "volume_zscore",
        "lookback": 20,
        "direction_convention": "higher_is_unusually_high_volume",
        "input_fields": ["volume"],
        "notes": "Volume z-score versus trailing 20-day ticker history.",
    },
    {
        "signal_name": "volume_zscore_60",
        "signal_family": "volume",
        "formula_type": "volume_zscore",
        "lookback": 60,
        "direction_convention": "higher_is_unusually_high_volume",
        "input_fields": ["volume"],
        "notes": "Volume z-score versus trailing 60-day ticker history.",
    },
    {
        "signal_name": "trend_strength_50_200",
        "signal_family": "trend_quality",
        "formula_type": "moving_average_spread",
        "parameters": {"fast_window": 50, "slow_window": 200},
        "lookback": 200,
        "direction_convention": "higher_is_stronger_uptrend",
        "input_fields": ["close"],
        "notes": "50-day moving average divided by 200-day moving average minus one.",
    },
    {
        "signal_name": "price_above_ma_200",
        "signal_family": "trend_quality",
        "formula_type": "price_above_moving_average_flag",
        "parameters": {"lookback": 200},
        "lookback": 200,
        "direction_convention": "higher_is_price_above_long_term_trend",
        "input_fields": ["close"],
        "notes": "Binary flag equal to one when close is above the trailing 200-day moving average.",
    },
    {
        "signal_name": "ma_slope_50",
        "signal_family": "trend_quality",
        "formula_type": "moving_average_pct_change",
        "parameters": {"lookback": 50, "slope_window": 5},
        "lookback": 50,
        "direction_convention": "higher_is_rising_intermediate_trend",
        "input_fields": ["close"],
        "notes": "Five-day percentage change of the trailing 50-day moving average.",
    },
    {
        "signal_name": "reversal_5d",
        "signal_family": "short_term_reversal",
        "formula_type": "negative_close_pct_change",
        "parameters": {"lookback": 5},
        "lookback": 5,
        "direction_convention": "higher_is_more_recent_pullback",
        "input_fields": ["close"],
        "notes": "Negative trailing 5-day close-to-close return.",
    },
    {
        "signal_name": "reversal_10d",
        "signal_family": "short_term_reversal",
        "formula_type": "negative_close_pct_change",
        "parameters": {"lookback": 10},
        "lookback": 10,
        "direction_convention": "higher_is_more_recent_pullback",
        "input_fields": ["close"],
        "notes": "Negative trailing 10-day close-to-close return.",
    },
    {
        "signal_name": "distance_from_ma_20",
        "signal_family": "short_term_reversal",
        "formula_type": "negative_distance_to_moving_average",
        "parameters": {"lookback": 20},
        "lookback": 20,
        "direction_convention": "higher_is_more_below_short_term_average",
        "input_fields": ["close"],
        "notes": "Negative close distance from the trailing 20-day moving average.",
    },
    {
        "signal_name": "risk_adjusted_momentum_20",
        "signal_family": "defensive_quality",
        "formula_type": "close_pct_change_divided_by_realized_volatility",
        "parameters": {"lookback": 20},
        "lookback": 20,
        "direction_convention": "higher_is_stronger_volatility_adjusted_momentum",
        "input_fields": ["close"],
        "notes": "20-day momentum divided by trailing 20-day realized return volatility.",
    },
    {
        "signal_name": "risk_adjusted_momentum_60",
        "signal_family": "defensive_quality",
        "formula_type": "close_pct_change_divided_by_realized_volatility",
        "parameters": {"lookback": 60},
        "lookback": 60,
        "direction_convention": "higher_is_stronger_volatility_adjusted_momentum",
        "input_fields": ["close"],
        "notes": "60-day momentum divided by trailing 60-day realized return volatility.",
    },
    {
        "signal_name": "low_vol_strength",
        "signal_family": "defensive_quality",
        "formula_type": "negative_realized_return_volatility",
        "parameters": {"lookback": 20},
        "lookback": 20,
        "direction_convention": "higher_is_lower_realized_volatility",
        "input_fields": ["close"],
        "notes": "Negative trailing 20-day realized return volatility.",
    },
]


PHASE2_SIGNAL_SPECS.extend(
    [
        {
            "signal_name": "intraday_reversal_1d",
            "signal_family": "mean_reversion",
            "formula_type": "negative_intraday_open_to_close_return",
            "parameters": {"lookback": 1},
            "lookback": 1,
            "direction_convention": "higher_is_larger_intraday_pullback",
            "input_fields": ["open", "close"],
            "notes": "Negative same-day open-to-close return: -(close / open - 1).",
        },
        {
            "signal_name": "gap_reversal_1d",
            "signal_family": "short_term_reversal",
            "formula_type": "negative_overnight_gap_return",
            "parameters": {"lookback": 1},
            "lookback": 1,
            "direction_convention": "higher_is_larger_negative_overnight_gap",
            "input_fields": ["open", "close"],
            "notes": "Negative overnight gap from previous close to current open: -(open / prior close - 1).",
        },
        {
            "signal_name": "up_down_volume_pressure_20",
            "signal_family": "volume_flow",
            "formula_type": "signed_volume_pressure",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_volume_on_up_days",
            "input_fields": ["close", "volume"],
            "notes": "Rolling 20-day signed volume divided by rolling total volume, where sign is daily close-to-close return sign.",
        },
        {
            "signal_name": "volume_acceleration_20",
            "signal_family": "volume_flow",
            "formula_type": "rolling_volume_mean_change",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_accelerating_volume",
            "input_fields": ["volume"],
            "notes": "Current 20-day average volume divided by the prior non-overlapping 20-day average volume minus one.",
        },
        {
            "signal_name": "price_volume_divergence_20",
            "signal_family": "volume_flow",
            "formula_type": "price_return_minus_volume_acceleration",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_price_strength_less_supported_by_volume_trend",
            "input_fields": ["close", "volume"],
            "notes": "20-day price return minus 20-day volume acceleration to detect price moves unsupported by participation.",
        },
        {
            "signal_name": "amihud_illiq_20",
            "signal_family": "liquidity",
            "formula_type": "rolling_amihud_illiquidity",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_illiquid_price_impact",
            "input_fields": ["close", "volume"],
            "notes": "20-day rolling mean of absolute daily return divided by dollar volume.",
        },
        {
            "signal_name": "market_beta_change_60",
            "signal_family": "correlation_dispersion",
            "formula_type": "rolling_beta_change_to_market",
            "parameters": {"lookback": 60, "change_window": 20},
            "lookback": 60,
            "direction_convention": "higher_is_increasing_market_beta",
            "input_fields": ["close"],
            "data_dependencies": ["close", "benchmark_or_equal_weight_market_return"],
            "notes": "60-day rolling beta to SPY if available, otherwise equal-weight market return, minus beta 20 days ago.",
        },
        {
            "signal_name": "relative_return_vs_universe_20",
            "signal_family": "cross_sectional_relative_value",
            "formula_type": "close_pct_change_minus_cross_sectional_average",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_stronger_universe_relative_return",
            "input_fields": ["close"],
            "notes": "20-day stock return minus same-date cross-sectional average 20-day return.",
        },
        {
            "signal_name": "idiosyncratic_return_20",
            "signal_family": "correlation_dispersion",
            "formula_type": "close_pct_change_minus_beta_adjusted_market_return",
            "parameters": {"lookback": 20, "beta_window": 60},
            "lookback": 60,
            "direction_convention": "higher_is_stronger_idiosyncratic_return",
            "input_fields": ["close"],
            "data_dependencies": ["close", "benchmark_or_equal_weight_market_return"],
            "notes": "20-day stock return minus trailing-beta-adjusted 20-day benchmark return; uses SPY if available, otherwise equal-weight universe return.",
        },
        {
            "signal_name": "rolling_corr_to_market_60",
            "signal_family": "correlation_dispersion",
            "formula_type": "rolling_correlation_to_market",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_more_correlated_to_market",
            "input_fields": ["close"],
            "data_dependencies": ["close", "benchmark_or_equal_weight_market_return"],
            "notes": "60-day rolling correlation of stock daily returns to SPY if available, otherwise equal-weight universe return.",
        },
        {
            "signal_name": "relative_strength_20",
            "signal_family": "cross_sectional_relative_strength",
            "formula_type": "close_pct_change_cross_sectional_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_stronger_recent_relative_return",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return is ranked cross-sectionally by Date; higher percentile means stronger relative strength.",
            "notes": "20-day close-to-close return ranked cross-sectionally by date.",
        },
        {
            "signal_name": "relative_strength_60",
            "signal_family": "cross_sectional_relative_strength",
            "formula_type": "close_pct_change_cross_sectional_rank",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_stronger_recent_relative_return",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return is ranked cross-sectionally by Date; higher percentile means stronger relative strength.",
            "notes": "60-day close-to-close return ranked cross-sectionally by date.",
        },
        {
            "signal_name": "relative_strength_120",
            "signal_family": "cross_sectional_relative_strength",
            "formula_type": "close_pct_change_cross_sectional_rank",
            "parameters": {"lookback": 120},
            "lookback": 120,
            "direction_convention": "higher_is_stronger_recent_relative_return",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return is ranked cross-sectionally by Date; higher percentile means stronger relative strength.",
            "notes": "120-day close-to-close return ranked cross-sectionally by date.",
        },
        {
            "signal_name": "residual_momentum_20",
            "signal_family": "residual_momentum",
            "formula_type": "close_pct_change_minus_cross_sectional_average_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_stronger_market_neutral_momentum",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return minus the same-date cross-sectional average is ranked cross-sectionally by Date.",
            "notes": "20-day return minus cross-sectional average return, ranked by date.",
        },
        {
            "signal_name": "residual_momentum_60",
            "signal_family": "residual_momentum",
            "formula_type": "close_pct_change_minus_cross_sectional_average_rank",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_stronger_market_neutral_momentum",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return minus the same-date cross-sectional average is ranked cross-sectionally by Date.",
            "notes": "60-day return minus cross-sectional average return, ranked by date.",
        },
        {
            "signal_name": "residual_momentum_120",
            "signal_family": "residual_momentum",
            "formula_type": "close_pct_change_minus_cross_sectional_average_rank",
            "parameters": {"lookback": 120},
            "lookback": 120,
            "direction_convention": "higher_is_stronger_market_neutral_momentum",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Past return minus the same-date cross-sectional average is ranked cross-sectionally by Date.",
            "notes": "120-day return minus cross-sectional average return, ranked by date.",
        },
        {
            "signal_name": "vol_adj_momentum_20",
            "signal_family": "volatility_normalized_momentum",
            "formula_type": "close_pct_change_divided_by_realized_volatility_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_stronger_volatility_normalized_momentum",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Volatility-normalized momentum is ranked cross-sectionally by Date after safe division by trailing daily volatility.",
            "notes": "20-day return divided by trailing 20-day daily return volatility, ranked by date.",
        },
        {
            "signal_name": "vol_adj_momentum_60",
            "signal_family": "volatility_normalized_momentum",
            "formula_type": "close_pct_change_divided_by_realized_volatility_rank",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_stronger_volatility_normalized_momentum",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Volatility-normalized momentum is ranked cross-sectionally by Date after safe division by trailing daily volatility.",
            "notes": "60-day return divided by trailing 60-day daily return volatility, ranked by date.",
        },
        {
            "signal_name": "reversal_3d",
            "signal_family": "short_term_reversal",
            "formula_type": "negative_close_pct_change_rank",
            "parameters": {"lookback": 3},
            "lookback": 3,
            "direction_convention": "higher_is_more_recent_pullback",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Negative past return is ranked cross-sectionally by Date; higher percentile means larger recent pullback.",
            "notes": "Negative trailing 3-day close-to-close return, ranked by date.",
        },
        {
            "signal_name": "reversal_20d",
            "signal_family": "short_term_reversal",
            "formula_type": "negative_close_pct_change_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_recent_pullback",
            "input_fields": ["close"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Negative past return is ranked cross-sectionally by Date; higher percentile means larger recent pullback.",
            "notes": "Negative trailing 20-day close-to-close return, ranked by date.",
        },
        {
            "signal_name": "price_above_ma_50",
            "signal_family": "trend_quality",
            "formula_type": "price_above_moving_average_flag",
            "parameters": {"lookback": 50},
            "lookback": 50,
            "direction_convention": "higher_is_price_above_intermediate_trend",
            "input_fields": ["close"],
            "notes": "Binary flag equal to one when close is above the trailing 50-day moving average.",
        },
        {
            "signal_name": "price_above_ma_100",
            "signal_family": "trend_quality",
            "formula_type": "price_above_moving_average_flag",
            "parameters": {"lookback": 100},
            "lookback": 100,
            "direction_convention": "higher_is_price_above_intermediate_trend",
            "input_fields": ["close"],
            "notes": "Binary flag equal to one when close is above the trailing 100-day moving average.",
        },
        {
            "signal_name": "ma_slope_20",
            "signal_family": "trend_quality",
            "formula_type": "moving_average_pct_change",
            "parameters": {"lookback": 20, "slope_window": 5},
            "lookback": 20,
            "direction_convention": "higher_is_rising_short_term_trend",
            "input_fields": ["close"],
            "notes": "Five-day percentage change of the trailing 20-day moving average.",
        },
        {
            "signal_name": "ma_slope_100",
            "signal_family": "trend_quality",
            "formula_type": "moving_average_pct_change",
            "parameters": {"lookback": 100, "slope_window": 5},
            "lookback": 100,
            "direction_convention": "higher_is_rising_longer_term_trend",
            "input_fields": ["close"],
            "notes": "Five-day percentage change of the trailing 100-day moving average.",
        },
        {
            "signal_name": "breakout_up_20",
            "signal_family": "breakout",
            "formula_type": "close_above_prior_rolling_high_flag",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_upside_breakout",
            "input_fields": ["high", "close"],
            "notes": "Binary flag equal to one when close is above the prior trailing 20-day high.",
        },
        {
            "signal_name": "breakout_up_60",
            "signal_family": "breakout",
            "formula_type": "close_above_prior_rolling_high_flag",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_upside_breakout",
            "input_fields": ["high", "close"],
            "notes": "Binary flag equal to one when close is above the prior trailing 60-day high.",
        },
        {
            "signal_name": "range_position_20",
            "signal_family": "breakout",
            "formula_type": "price_position_in_high_low_range",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_closer_to_range_high",
            "input_fields": ["high", "low", "close"],
            "notes": "Close location within trailing 20-day high-low range.",
        },
        {
            "signal_name": "range_position_60",
            "signal_family": "breakout",
            "formula_type": "price_position_in_high_low_range",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_closer_to_range_high",
            "input_fields": ["high", "low", "close"],
            "notes": "Close location within trailing 60-day high-low range.",
        },
        {
            "signal_name": "volume_trend_20",
            "signal_family": "volume_liquidity",
            "formula_type": "volume_to_rolling_average",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_stronger_volume_trend_but_return_direction_unknown",
            "input_fields": ["volume"],
            "notes": "Volume divided by trailing 20-day average volume minus one.",
        },
        {
            "signal_name": "volume_trend_60",
            "signal_family": "volume_liquidity",
            "formula_type": "volume_to_rolling_average",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_stronger_volume_trend_but_return_direction_unknown",
            "input_fields": ["volume"],
            "notes": "Volume divided by trailing 60-day average volume minus one.",
        },
        {
            "signal_name": "dollar_volume_20",
            "signal_family": "volume_liquidity",
            "formula_type": "rolling_dollar_volume_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_liquid_return_direction_unknown",
            "input_fields": ["close", "volume"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Trailing average dollar volume is ranked cross-sectionally by Date; higher percentile means more liquid.",
            "notes": "20-day average close times volume, ranked by date.",
        },
        {
            "signal_name": "liquidity_rank_20",
            "signal_family": "volume_liquidity",
            "formula_type": "rolling_dollar_volume_rank",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_liquid_return_direction_unknown",
            "input_fields": ["close", "volume"],
            "normalization": "cross_sectional_percentile_rank_by_date",
            "normalization_notes": "Trailing average dollar volume is ranked cross-sectionally by Date; higher percentile means more liquid.",
            "notes": "Cross-sectional liquidity rank based on trailing 20-day average dollar volume.",
        },
        {
            "signal_name": "return_stability_20",
            "signal_family": "defensive_stability",
            "formula_type": "rolling_mean_return_divided_by_realized_volatility",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_more_stable_positive_return_profile",
            "input_fields": ["close"],
            "notes": "Trailing 20-day average daily return divided by trailing 20-day daily return volatility.",
        },
        {
            "signal_name": "return_stability_60",
            "signal_family": "defensive_stability",
            "formula_type": "rolling_mean_return_divided_by_realized_volatility",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_more_stable_positive_return_profile",
            "input_fields": ["close"],
            "notes": "Trailing 60-day average daily return divided by trailing 60-day daily return volatility.",
        },
        {
            "signal_name": "downside_vol_20",
            "signal_family": "defensive_stability",
            "formula_type": "negative_downside_return_volatility",
            "parameters": {"lookback": 20},
            "lookback": 20,
            "direction_convention": "higher_is_lower_downside_volatility",
            "input_fields": ["close"],
            "notes": "Negative trailing 20-day volatility of downside daily returns.",
        },
        {
            "signal_name": "downside_vol_60",
            "signal_family": "defensive_stability",
            "formula_type": "negative_downside_return_volatility",
            "parameters": {"lookback": 60},
            "lookback": 60,
            "direction_convention": "higher_is_lower_downside_volatility",
            "input_fields": ["close"],
            "notes": "Negative trailing 60-day volatility of downside daily returns.",
        },
    ]
)


def _validate_phase2_panels(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    missing = [name for name in PHASE2_REQUIRED_PANELS if name not in panels]
    if missing:
        raise KeyError(f"Missing required OHLCV panels: {missing}")

    aligned: dict[str, pd.DataFrame] = {}
    base_index: pd.Index | None = None
    base_columns: pd.Index | None = None

    for name in PHASE2_REQUIRED_PANELS:
        panel = panels[name]
        if not isinstance(panel, pd.DataFrame):
            raise TypeError(f"panels['{name}'] must be a pandas DataFrame.")

        cleaned = panel.copy()
        cleaned.index = pd.to_datetime(cleaned.index)
        cleaned = cleaned.sort_index()
        cleaned = cleaned.apply(pd.to_numeric, errors="coerce")

        if base_index is None:
            base_index = cleaned.index
            base_columns = cleaned.columns
        elif not cleaned.index.equals(base_index) or not cleaned.columns.equals(base_columns):
            raise ValueError("All OHLCV panels must have identical Date indexes and ticker columns.")

        aligned[name] = cleaned

    return aligned


def _cross_sectional_zscore(df: pd.DataFrame) -> pd.DataFrame:
    row_mean = df.mean(axis=1, skipna=True)
    row_std = df.std(axis=1, skipna=True, ddof=0).replace(0, np.nan)
    return df.sub(row_mean, axis=0).div(row_std, axis=0)


def _cross_sectional_rank(df: pd.DataFrame) -> pd.DataFrame:
    return df.rank(axis=1, pct=True, method="average", na_option="keep")


def _finalize_signal(df: pd.DataFrame) -> pd.DataFrame:
    return _cross_sectional_zscore(df).replace([np.inf, -np.inf], np.nan)


def _apply_signal_normalization(df: pd.DataFrame, normalization: str) -> pd.DataFrame:
    cleaned = df.replace([np.inf, -np.inf], np.nan)
    if normalization == "cross_sectional_percentile_rank_by_date":
        return _cross_sectional_rank(cleaned).replace([np.inf, -np.inf], np.nan)
    if normalization == "cross_sectional_zscore_by_date":
        return _finalize_signal(cleaned)
    if normalization == "raw":
        return cleaned
    raise ValueError(f"Unknown signal normalization '{normalization}'.")


def _winsorize_cross_sectionally(df: pd.DataFrame, lower_pct: float = 0.01, upper_pct: float = 0.99) -> pd.DataFrame:
    lower = df.quantile(lower_pct, axis=1)
    upper = df.quantile(upper_pct, axis=1)
    return df.clip(lower=lower, upper=upper, axis=0)


def _apply_discovery_transform(df: pd.DataFrame, transform: str) -> pd.DataFrame:
    cleaned = df.replace([np.inf, -np.inf], np.nan)
    if transform == "rank":
        return _apply_signal_normalization(cleaned, "cross_sectional_percentile_rank_by_date")
    if transform == "winsorized_zscore":
        cleaned = _winsorize_cross_sectionally(cleaned)
    return _apply_signal_normalization(cleaned, "cross_sectional_zscore_by_date")


def momentum_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Close-to-close momentum over a trailing lookback window."""
    return close.pct_change(lookback)


def mean_reversion_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Negative distance from a trailing moving average."""
    moving_average = close.rolling(lookback).mean()
    return -(close / moving_average - 1.0)


def intraday_reversal_signal(open_prices: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    """Negative same-day open-to-close return for short-horizon pullback behavior."""
    open_safe = open_prices.replace(0, np.nan)
    intraday_return = close / open_safe - 1.0
    return -intraday_return


def volatility_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Realized return volatility over a trailing lookback window."""
    returns = close.pct_change()
    return returns.rolling(lookback).std()


def breakout_signal(high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Close location within a trailing high-low range."""
    rolling_high = high.rolling(lookback).max()
    rolling_low = low.rolling(lookback).min()
    rolling_range = (rolling_high - rolling_low).replace(0, np.nan)
    return (close - rolling_low) / rolling_range


def volume_signal(volume: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Ticker-level volume z-score over a trailing lookback window."""
    volume_mean = volume.rolling(lookback).mean()
    volume_std = volume.rolling(lookback).std().replace(0, np.nan)
    return (volume - volume_mean) / volume_std


def trend_strength_signal(close: pd.DataFrame, fast_window: int = 50, slow_window: int = 200) -> pd.DataFrame:
    """Intermediate moving-average strength versus a long-term moving average."""
    fast_ma = close.rolling(fast_window).mean()
    slow_ma = close.rolling(slow_window).mean().replace(0, np.nan)
    return fast_ma / slow_ma - 1.0


def price_above_moving_average_signal(close: pd.DataFrame, lookback: int = 200) -> pd.DataFrame:
    """Binary price-above-moving-average trend quality flag."""
    moving_average = close.rolling(lookback).mean()
    return close.gt(moving_average).astype(float).where(moving_average.notna())


def moving_average_slope_signal(
    close: pd.DataFrame,
    lookback: int = 50,
    slope_window: int = 5,
) -> pd.DataFrame:
    """Recent percentage slope of a trailing moving average."""
    moving_average = close.rolling(lookback).mean()
    return moving_average.pct_change(slope_window)


def reversal_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Negative trailing close-to-close return for pullback behavior."""
    return -close.pct_change(lookback)


def gap_reversal_signal(open_prices: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    """Negative overnight gap from previous close to current open."""
    previous_close = close.shift(1).replace(0, np.nan)
    overnight_gap = open_prices / previous_close - 1.0
    return -overnight_gap


def risk_adjusted_momentum_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Trailing momentum scaled by trailing realized return volatility."""
    momentum = close.pct_change(lookback)
    realized_volatility = close.pct_change().rolling(lookback).std().replace(0, np.nan)
    return momentum / realized_volatility


def low_vol_strength_signal(close: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """Negative trailing realized return volatility, so higher values are more defensive."""
    return -close.pct_change().rolling(lookback).std()


def residual_momentum_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Trailing return minus same-date cross-sectional average trailing return."""
    momentum = close.pct_change(lookback)
    return momentum.sub(momentum.mean(axis=1, skipna=True), axis=0)


def breakout_up_signal(high: pd.DataFrame, close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Binary flag for close above the prior trailing high."""
    prior_rolling_high = high.rolling(lookback).max().shift(1)
    return close.gt(prior_rolling_high).astype(float).where(prior_rolling_high.notna())


def volume_trend_signal(volume: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Volume relative to its trailing average."""
    average_volume = volume.rolling(lookback).mean().replace(0, np.nan)
    return volume / average_volume - 1.0


def dollar_volume_signal(close: pd.DataFrame, volume: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Trailing average dollar volume."""
    return close.mul(volume).rolling(lookback).mean()


def up_down_volume_pressure_signal(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    lookback: int,
) -> pd.DataFrame:
    """Rolling signed-volume pressure based on up/down close-to-close return sign."""
    return_sign = np.sign(close.pct_change())
    signed_volume = volume.mul(return_sign)
    rolling_signed_volume = signed_volume.rolling(lookback).sum()
    rolling_volume = volume.rolling(lookback).sum().replace(0, np.nan)
    return rolling_signed_volume / rolling_volume


def volume_acceleration_signal(volume: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Current trailing volume versus the prior non-overlapping trailing volume."""
    current_volume = volume.rolling(lookback).mean()
    prior_volume = volume.shift(lookback).rolling(lookback).mean().replace(0, np.nan)
    return (current_volume / prior_volume - 1.0).replace([np.inf, -np.inf], np.nan)


def price_volume_divergence_signal(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    lookback: int,
) -> pd.DataFrame:
    """Price return minus volume acceleration over matching trailing windows."""
    price_return = close.pct_change(lookback)
    volume_trend = volume_acceleration_signal(volume, lookback)
    return (price_return - volume_trend).replace([np.inf, -np.inf], np.nan)


def volume_return_interaction_signal(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    lookback: int,
    interaction: str,
) -> pd.DataFrame:
    """Transparent volume/return interaction formulas for discovery candidates."""
    price_return = close.pct_change(lookback)
    if interaction == "return_minus_volume_trend":
        return price_return - volume_acceleration_signal(volume, lookback)
    if interaction == "return_times_volume_zscore":
        return price_return * volume_signal(volume, lookback)
    if interaction == "signed_volume_pressure":
        return up_down_volume_pressure_signal(close, volume, lookback)
    raise ValueError(f"Unknown volume_return interaction '{interaction}'.")


def amihud_illiquidity_signal(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    lookback: int,
) -> pd.DataFrame:
    """Rolling Amihud-style illiquidity proxy: abs return divided by dollar volume."""
    dollar_volume = close.mul(volume).replace(0, np.nan)
    raw_illiquidity = close.pct_change().abs() / dollar_volume
    return raw_illiquidity.replace([np.inf, -np.inf], np.nan).rolling(lookback).mean()


def market_beta_change_signal(
    close: pd.DataFrame,
    lookback: int = 60,
    change_window: int = 20,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Change in rolling beta to SPY if present, otherwise equal-weight market return."""
    returns = close.pct_change()
    if benchmark_ticker in returns.columns:
        benchmark_returns = returns[benchmark_ticker]
    else:
        benchmark_returns = returns.mean(axis=1, skipna=True)

    benchmark_variance = benchmark_returns.rolling(lookback).var().replace(0, np.nan)
    rolling_covariance = returns.rolling(lookback).cov(benchmark_returns)
    rolling_beta = rolling_covariance.div(benchmark_variance, axis=0)
    return rolling_beta - rolling_beta.shift(change_window)


def _market_returns(close: pd.DataFrame, benchmark_ticker: str = "SPY") -> tuple[pd.DataFrame, pd.Series]:
    returns = close.pct_change()
    if benchmark_ticker in returns.columns:
        benchmark_returns = returns[benchmark_ticker]
    else:
        benchmark_returns = returns.mean(axis=1, skipna=True)
    return returns, benchmark_returns


def idiosyncratic_return_signal(
    close: pd.DataFrame,
    lookback: int = 20,
    beta_window: int = 60,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Trailing stock return net of trailing-beta-adjusted benchmark return."""
    returns, benchmark_returns = _market_returns(close, benchmark_ticker=benchmark_ticker)
    stock_return = close.pct_change(lookback)
    benchmark_return = (1.0 + benchmark_returns).rolling(lookback).apply(np.prod, raw=True) - 1.0
    benchmark_variance = benchmark_returns.rolling(beta_window).var().replace(0, np.nan)
    rolling_covariance = returns.rolling(beta_window).cov(benchmark_returns)
    rolling_beta = rolling_covariance.div(benchmark_variance, axis=0)
    return stock_return.sub(rolling_beta.mul(benchmark_return, axis=0))


def rolling_correlation_to_market_signal(
    close: pd.DataFrame,
    lookback: int = 60,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Rolling correlation of stock returns to SPY or equal-weight market return."""
    returns, benchmark_returns = _market_returns(close, benchmark_ticker=benchmark_ticker)
    return returns.rolling(lookback).corr(benchmark_returns)


def correlation_change_signal(
    close: pd.DataFrame,
    short_window: int,
    long_window: int,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Short rolling market correlation minus long rolling market correlation."""
    short_corr = rolling_correlation_to_market_signal(close, lookback=short_window, benchmark_ticker=benchmark_ticker)
    long_corr = rolling_correlation_to_market_signal(close, lookback=long_window, benchmark_ticker=benchmark_ticker)
    return short_corr - long_corr


def volatility_surprise_signal(close: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    """Short realized volatility divided by long realized volatility minus one."""
    short_vol = volatility_signal(close, short_window)
    long_vol = volatility_signal(close, long_window).replace(0, np.nan)
    return (short_vol / long_vol - 1.0).replace([np.inf, -np.inf], np.nan)


def reversal_overextension_signal(close: pd.DataFrame, lookback: int, measure: str) -> pd.DataFrame:
    """Short-horizon reversal/overextension variants normalized by trailing volatility when requested."""
    price_return = close.pct_change(lookback)
    if measure == "negative_return":
        return -price_return
    if measure == "negative_distance_to_ma":
        return mean_reversion_signal(close, lookback)
    if measure == "negative_return_zscore":
        realized_volatility = volatility_signal(close, lookback).replace(0, np.nan)
        return (-price_return / realized_volatility).replace([np.inf, -np.inf], np.nan)
    raise ValueError(f"Unknown reversal_overextension measure '{measure}'.")


def liquidity_adjusted_return_signal(
    close: pd.DataFrame,
    volume: pd.DataFrame,
    lookback: int,
    liquidity_measure: str,
) -> pd.DataFrame:
    """Return conditioned on simple trailing liquidity proxies."""
    price_return = close.pct_change(lookback)
    dollar_volume = dollar_volume_signal(close, volume, lookback).replace(0, np.nan)
    if liquidity_measure == "dollar_volume_rank":
        liquidity_rank = _cross_sectional_rank(dollar_volume).replace(0, np.nan)
        return (price_return / liquidity_rank).replace([np.inf, -np.inf], np.nan)
    if liquidity_measure == "amihud_illiq":
        illiquidity = amihud_illiquidity_signal(close, volume, lookback)
        illiquidity_rank = _cross_sectional_rank(illiquidity).replace(0, np.nan)
        return (price_return * illiquidity_rank).replace([np.inf, -np.inf], np.nan)
    if liquidity_measure == "volume_trend":
        return (price_return * volume_trend_signal(volume, lookback)).replace([np.inf, -np.inf], np.nan)
    raise ValueError(f"Unknown liquidity_adjusted_return measure '{liquidity_measure}'.")


def return_stability_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Trailing mean daily return divided by trailing daily return volatility."""
    returns = close.pct_change()
    volatility = returns.rolling(lookback).std().replace(0, np.nan)
    return returns.rolling(lookback).mean() / volatility


def downside_volatility_signal(close: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Negative trailing volatility of downside daily returns."""
    downside_returns = close.pct_change().clip(upper=0.0)
    return -downside_returns.rolling(lookback).std()


def _parse_discovery_grid(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = json.loads(value)
        if not isinstance(parsed, dict):
            raise ValueError("parameter_grid JSON must decode to an object.")
        return parsed
    raise TypeError("parameter_grid must be a dict or JSON string.")


def _ordered_values(grid: dict[str, object], key: str, fallback: Sequence[object]) -> list[object]:
    values = grid.get(key, fallback)
    if not isinstance(values, list):
        values = list(values) if isinstance(values, tuple) else [values]
    return values


def _ordered_transforms(grid: dict[str, object]) -> list[str]:
    available = [str(value) for value in _ordered_values(grid, "transforms", DISCOVERY_TRANSFORM_ORDER)]
    return [transform for transform in DISCOVERY_TRANSFORM_ORDER if transform in available]


def _transform_suffix(transform: str) -> str:
    return {
        "rank": "rank",
        "zscore": "z",
        "winsorized_zscore": "wz",
        "raw": "raw",
    }.get(transform, transform.replace("_", ""))


def _parameter_json(parameters: dict[str, object]) -> str:
    return json.dumps(parameters, sort_keys=True, separators=(",", ":"))


def _spec(
    signal_name: str,
    discovery_family: str,
    formula_type: str,
    parameters: dict[str, object],
    input_fields: list[str],
    signal_template_name: str,
    discovery_version: str,
) -> dict[str, object]:
    lookback_values = [
        int(value)
        for key, value in parameters.items()
        if "window" in key and isinstance(value, (int, np.integer))
    ]
    transform = str(parameters.get("transform", "zscore"))
    return {
        "signal_name": signal_name,
        "signal_family": discovery_family,
        "formula_type": formula_type,
        "parameters": parameters,
        "lookback": max(lookback_values) if lookback_values else None,
        "direction_convention": "higher_follows_discovery_hypothesis",
        "input_fields": input_fields,
        "normalization": "cross_sectional_percentile_rank_by_date"
        if transform == "rank"
        else "cross_sectional_zscore_by_date",
        "normalization_notes": (
            f"Discovery raw signal uses transform={transform}; final values are cross-sectionally normalized by Date."
        ),
        "notes": "Generated from 01C signal discovery search space.",
        "signal_source": "discovery_generated",
        "discovery_family": discovery_family,
        "discovery_version": discovery_version,
        "signal_template_name": signal_template_name,
        "parameter_config_json": _parameter_json(parameters),
    }


def _candidate_specs_for_discovery_row(row: pd.Series, discovery_version: str) -> list[dict[str, object]]:
    family = str(row["discovery_family"])
    template_name = str(row["signal_template_name"])
    grid = _parse_discovery_grid(row["parameter_grid"])
    transforms = _ordered_transforms(grid)
    specs: list[dict[str, object]] = []

    if family == "cross_sectional_relative_return":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for transform in transforms:
                parameters = {"window": int(window), "transform": transform}
                specs.append(
                    _spec(
                        signal_name=f"disc_relret_w{window}_{_transform_suffix(transform)}",
                        discovery_family=family,
                        formula_type="discovery_cross_sectional_relative_return",
                        parameters=parameters,
                        input_fields=["close"],
                        signal_template_name=template_name,
                        discovery_version=discovery_version,
                    )
                )
    elif family == "beta_neutral_return":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for beta_window in _ordered_values(grid, "beta_windows", [60, 120]):
                for transform in transforms:
                    parameters = {"window": int(window), "beta_window": int(beta_window), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_beta_neutral_w{window}_b{beta_window}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_beta_neutral_return",
                            parameters=parameters,
                            input_fields=["close"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "volatility_adjusted_momentum":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for vol_window in _ordered_values(grid, "vol_windows", [20, 60, 120]):
                for transform in transforms:
                    parameters = {"window": int(window), "vol_window": int(vol_window), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_voladj_mom_w{window}_v{vol_window}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_volatility_adjusted_momentum",
                            parameters=parameters,
                            input_fields=["close"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "volatility_surprise":
        for short_window in _ordered_values(grid, "short_windows", [5, 10, 20]):
            for long_window in _ordered_values(grid, "long_windows", [60, 120]):
                if int(short_window) >= int(long_window):
                    continue
                for transform in transforms:
                    parameters = {"short_window": int(short_window), "long_window": int(long_window), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_vol_surprise_s{short_window}_l{long_window}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_volatility_surprise",
                            parameters=parameters,
                            input_fields=["close"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "reversal_overextension":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for measure in _ordered_values(grid, "measures", ["negative_return_zscore"]):
                for transform in transforms:
                    parameters = {"window": int(window), "measure": str(measure), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_reversal_overext_w{window}_{str(measure).replace('negative_', '')}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_reversal_overextension",
                            parameters=parameters,
                            input_fields=["close"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "correlation_change":
        for short_window in _ordered_values(grid, "short_windows", [5, 10, 20]):
            for long_window in _ordered_values(grid, "long_windows", [60, 120]):
                if int(short_window) >= int(long_window):
                    continue
                for transform in transforms:
                    parameters = {"short_window": int(short_window), "long_window": int(long_window), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_corr_change_s{short_window}_l{long_window}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_correlation_change",
                            parameters=parameters,
                            input_fields=["close"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "liquidity_adjusted_return":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for liquidity_measure in _ordered_values(grid, "liquidity_measures", ["dollar_volume_rank"]):
                for transform in transforms:
                    parameters = {"window": int(window), "liquidity_measure": str(liquidity_measure), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_liq_adj_ret_w{window}_{str(liquidity_measure).replace('_', '')}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_liquidity_adjusted_return",
                            parameters=parameters,
                            input_fields=["close", "volume"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    elif family == "volume_return_interaction":
        for window in _ordered_values(grid, "windows", [5, 10, 20, 60]):
            for interaction in _ordered_values(grid, "interactions", ["return_times_volume_zscore"]):
                for transform in transforms:
                    parameters = {"window": int(window), "interaction": str(interaction), "transform": transform}
                    specs.append(
                        _spec(
                            signal_name=f"disc_volret_interact_w{window}_{str(interaction).replace('_', '')}_{_transform_suffix(transform)}",
                            discovery_family=family,
                            formula_type="discovery_volume_return_interaction",
                            parameters=parameters,
                            input_fields=["close", "volume"],
                            signal_template_name=template_name,
                            discovery_version=discovery_version,
                        )
                    )
    return specs


def build_discovery_signal_specs(
    discovery_search_space: pd.DataFrame,
    discovery_version: str,
    max_discovery_signals: int = 30,
) -> list[dict[str, object]]:
    """Build a capped, deterministic set of discovery-generated signal specs."""
    if discovery_search_space.empty or max_discovery_signals <= 0:
        return []

    space = discovery_search_space.copy()
    space["family_order"] = space["discovery_family"].map(
        {family: order for order, family in enumerate(DISCOVERY_FAMILY_ORDER)}
    ).fillna(len(DISCOVERY_FAMILY_ORDER))
    space["priority_order"] = space["priority"].map({"HIGH": 0, "MEDIUM": 1, "LOW": 2}).fillna(3)
    space = space.sort_values(["priority_order", "family_order", "discovery_family"]).reset_index(drop=True)

    family_candidates = [
        _candidate_specs_for_discovery_row(row, discovery_version=discovery_version)
        for _, row in space.iterrows()
    ]

    selected: list[dict[str, object]] = []
    seen_names: set[str] = set()
    max_family_len = max((len(candidates) for candidates in family_candidates), default=0)
    for candidate_index in range(max_family_len):
        for candidates in family_candidates:
            if candidate_index >= len(candidates):
                continue
            spec = candidates[candidate_index]
            signal_name = str(spec["signal_name"])
            if signal_name in seen_names:
                continue
            selected.append(spec)
            seen_names.add(signal_name)
            if len(selected) >= max_discovery_signals:
                return selected
    return selected


def _calculate_phase2_signal(spec: dict[str, object], panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    lookback = int(spec["lookback"])
    signal_family = str(spec["signal_family"])
    signal_name = str(spec["signal_name"])

    if signal_family == "momentum":
        raw = momentum_signal(panels["close"], lookback)
    elif signal_family == "mean_reversion":
        if signal_name == "intraday_reversal_1d":
            raw = intraday_reversal_signal(panels["open"], panels["close"])
        else:
            raw = mean_reversion_signal(panels["close"], lookback)
    elif signal_family == "volatility":
        raw = volatility_signal(panels["close"], lookback)
    elif signal_family == "breakout":
        if signal_name in {"breakout_up_20", "breakout_up_60"}:
            raw = breakout_up_signal(panels["high"], panels["close"], lookback)
        else:
            raw = breakout_signal(panels["high"], panels["low"], panels["close"], lookback)
    elif signal_family == "volume":
        raw = volume_signal(panels["volume"], lookback)
    elif signal_family == "trend_quality":
        if signal_name == "trend_strength_50_200":
            raw = trend_strength_signal(panels["close"], fast_window=50, slow_window=200)
        elif signal_name in {"price_above_ma_50", "price_above_ma_100", "price_above_ma_200"}:
            raw = price_above_moving_average_signal(panels["close"], lookback=lookback)
        elif signal_name in {"ma_slope_20", "ma_slope_50", "ma_slope_100"}:
            raw = moving_average_slope_signal(panels["close"], lookback=lookback, slope_window=5)
        else:
            raise ValueError(f"Unknown trend_quality signal '{signal_name}'.")
    elif signal_family == "short_term_reversal":
        if signal_name in {"reversal_3d", "reversal_5d", "reversal_10d", "reversal_20d"}:
            raw = reversal_signal(panels["close"], lookback)
        elif signal_name == "distance_from_ma_20":
            raw = mean_reversion_signal(panels["close"], lookback)
        elif signal_name == "gap_reversal_1d":
            raw = gap_reversal_signal(panels["open"], panels["close"])
        else:
            raise ValueError(f"Unknown short_term_reversal signal '{signal_name}'.")
    elif signal_family == "defensive_quality":
        if signal_name in {"risk_adjusted_momentum_20", "risk_adjusted_momentum_60"}:
            raw = risk_adjusted_momentum_signal(panels["close"], lookback)
        elif signal_name == "low_vol_strength":
            raw = low_vol_strength_signal(panels["close"], lookback)
        else:
            raise ValueError(f"Unknown defensive_quality signal '{signal_name}'.")
    elif signal_family == "cross_sectional_relative_strength":
        raw = momentum_signal(panels["close"], lookback)
    elif signal_family == "residual_momentum":
        raw = residual_momentum_signal(panels["close"], lookback)
    elif signal_family == "volatility_normalized_momentum":
        raw = risk_adjusted_momentum_signal(panels["close"], lookback)
    elif signal_family == "volume_liquidity":
        if signal_name in {"volume_trend_20", "volume_trend_60"}:
            raw = volume_trend_signal(panels["volume"], lookback)
        elif signal_name in {"dollar_volume_20", "liquidity_rank_20"}:
            raw = dollar_volume_signal(panels["close"], panels["volume"], lookback)
        else:
            raise ValueError(f"Unknown volume_liquidity signal '{signal_name}'.")
    elif signal_family == "volume_flow":
        if signal_name == "up_down_volume_pressure_20":
            raw = up_down_volume_pressure_signal(panels["close"], panels["volume"], lookback)
        elif signal_name == "volume_acceleration_20":
            raw = volume_acceleration_signal(panels["volume"], lookback)
        elif signal_name == "price_volume_divergence_20":
            raw = price_volume_divergence_signal(panels["close"], panels["volume"], lookback)
        else:
            raise ValueError(f"Unknown volume_flow signal '{signal_name}'.")
    elif signal_family == "liquidity":
        if signal_name == "amihud_illiq_20":
            raw = amihud_illiquidity_signal(panels["close"], panels["volume"], lookback)
        else:
            raise ValueError(f"Unknown liquidity signal '{signal_name}'.")
    elif signal_family == "correlation_dispersion":
        if signal_name == "market_beta_change_60":
            raw = market_beta_change_signal(panels["close"], lookback=lookback, change_window=20)
        elif signal_name == "idiosyncratic_return_20":
            raw = idiosyncratic_return_signal(panels["close"], lookback=20, beta_window=60)
        elif signal_name == "rolling_corr_to_market_60":
            raw = rolling_correlation_to_market_signal(panels["close"], lookback=lookback)
        else:
            raise ValueError(f"Unknown correlation_dispersion signal '{signal_name}'.")
    elif signal_family == "cross_sectional_relative_value":
        if signal_name == "relative_return_vs_universe_20":
            raw = residual_momentum_signal(panels["close"], lookback)
        else:
            raise ValueError(f"Unknown cross_sectional_relative_value signal '{signal_name}'.")
    elif signal_family == "defensive_stability":
        if signal_name in {"return_stability_20", "return_stability_60"}:
            raw = return_stability_signal(panels["close"], lookback)
        elif signal_name in {"downside_vol_20", "downside_vol_60"}:
            raw = downside_volatility_signal(panels["close"], lookback)
        else:
            raise ValueError(f"Unknown defensive_stability signal '{signal_name}'.")
    else:
        raise ValueError(f"Unknown signal_family '{signal_family}'.")

    return _apply_signal_normalization(
        raw,
        normalization=str(spec.get("normalization", "cross_sectional_zscore_by_date")),
    )


def _calculate_discovery_signal(spec: dict[str, object], panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    parameters = spec.get("parameters", {})
    if not isinstance(parameters, dict):
        raise TypeError("Discovery signal spec parameters must be a dictionary.")

    formula_type = str(spec["formula_type"])
    transform = str(parameters.get("transform", "zscore"))

    if formula_type == "discovery_cross_sectional_relative_return":
        raw = residual_momentum_signal(panels["close"], int(parameters["window"]))
    elif formula_type == "discovery_beta_neutral_return":
        raw = idiosyncratic_return_signal(
            panels["close"],
            lookback=int(parameters["window"]),
            beta_window=int(parameters["beta_window"]),
        )
    elif formula_type == "discovery_volatility_adjusted_momentum":
        price_return = panels["close"].pct_change(int(parameters["window"]))
        realized_volatility = volatility_signal(panels["close"], int(parameters["vol_window"])).replace(0, np.nan)
        raw = (price_return / realized_volatility).replace([np.inf, -np.inf], np.nan)
    elif formula_type == "discovery_volatility_surprise":
        raw = volatility_surprise_signal(
            panels["close"],
            short_window=int(parameters["short_window"]),
            long_window=int(parameters["long_window"]),
        )
    elif formula_type == "discovery_reversal_overextension":
        raw = reversal_overextension_signal(
            panels["close"],
            lookback=int(parameters["window"]),
            measure=str(parameters["measure"]),
        )
    elif formula_type == "discovery_correlation_change":
        raw = correlation_change_signal(
            panels["close"],
            short_window=int(parameters["short_window"]),
            long_window=int(parameters["long_window"]),
        )
    elif formula_type == "discovery_liquidity_adjusted_return":
        raw = liquidity_adjusted_return_signal(
            panels["close"],
            panels["volume"],
            lookback=int(parameters["window"]),
            liquidity_measure=str(parameters["liquidity_measure"]),
        )
    elif formula_type == "discovery_volume_return_interaction":
        raw = volume_return_interaction_signal(
            panels["close"],
            panels["volume"],
            lookback=int(parameters["window"]),
            interaction=str(parameters["interaction"]),
        )
    else:
        raise ValueError(f"Unknown discovery formula_type '{formula_type}'.")

    return _apply_discovery_transform(raw, transform=transform)


def generate_signal_library(
    panels: dict[str, pd.DataFrame],
    signal_version: str,
    run_id: str,
    timestamp: str,
    discovery_search_space: pd.DataFrame | None = None,
    discovery_version: str | None = None,
    max_discovery_signals: int = 30,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Generate Phase 2 candidate signal panels and standardized metadata."""
    aligned_panels = _validate_phase2_panels(panels)
    signals: dict[str, pd.DataFrame] = {}
    metadata_rows: list[dict[str, object]] = []

    for spec in PHASE2_SIGNAL_SPECS:
        signal_name = str(spec["signal_name"])
        signals[signal_name] = _calculate_phase2_signal(spec, aligned_panels)
        metadata_rows.append(
            build_signal_metadata_row(
                signal_name=signal_name,
                signal_family=str(spec["signal_family"]),
                formula_type=str(spec["formula_type"]),
                lookback=int(spec["lookback"]),
                direction_convention=str(spec["direction_convention"]),
                input_fields=spec["input_fields"],
                normalization=str(spec.get("normalization", "cross_sectional_zscore_by_date")),
                signal_version=signal_version,
                run_id=run_id,
                created_timestamp=timestamp,
                notes=str(spec.get("notes", "")),
                parameters=spec.get("parameters"),
                data_dependencies=spec.get("data_dependencies", spec["input_fields"]),
                normalization_notes=str(
                    spec.get(
                        "normalization_notes",
                        "Raw trailing signal is cross-sectionally z-scored by Date after replacing infinite values with NaN.",
                    )
                ),
            )
        )

    if discovery_search_space is not None:
        if discovery_version is None:
            raise ValueError("discovery_version is required when discovery_search_space is provided.")
        discovery_specs = build_discovery_signal_specs(
            discovery_search_space=discovery_search_space,
            discovery_version=discovery_version,
            max_discovery_signals=max_discovery_signals,
        )
        for spec in discovery_specs:
            signal_name = str(spec["signal_name"])
            signal_df = _calculate_discovery_signal(spec, aligned_panels)
            if signal_df.notna().sum().sum() == 0:
                continue
            signals[signal_name] = signal_df
            metadata_rows.append(
                build_signal_metadata_row(
                    signal_name=signal_name,
                    signal_family=str(spec["signal_family"]),
                    formula_type=str(spec["formula_type"]),
                    lookback=int(spec["lookback"]) if spec["lookback"] is not None else None,
                    direction_convention=str(spec["direction_convention"]),
                    input_fields=spec["input_fields"],
                    normalization=str(spec.get("normalization", "cross_sectional_zscore_by_date")),
                    signal_version=signal_version,
                    run_id=run_id,
                    created_timestamp=timestamp,
                    notes=str(spec.get("notes", "")),
                    parameters=spec.get("parameters"),
                    data_dependencies=spec.get("data_dependencies", spec["input_fields"]),
                    normalization_notes=str(spec.get("normalization_notes", "")),
                    signal_source=str(spec["signal_source"]),
                    discovery_family=str(spec["discovery_family"]),
                    discovery_version=str(spec["discovery_version"]),
                    signal_template_name=str(spec["signal_template_name"]),
                    parameter_config_json=str(spec["parameter_config_json"]),
                )
            )

    return signals, build_signal_metadata(metadata_rows)


def _validate_inputs(
    clean_close_prices: pd.DataFrame,
    returns: pd.DataFrame,
    volume: pd.DataFrame,
    benchmark_ticker: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Validate and align core inputs.
    Returns aligned copies with datetime index and identical shape/order.
    """
    if not isinstance(clean_close_prices, pd.DataFrame):
        raise TypeError("clean_close_prices must be a pandas DataFrame.")
    if not isinstance(returns, pd.DataFrame):
        raise TypeError("returns must be a pandas DataFrame.")
    if not isinstance(volume, pd.DataFrame):
        raise TypeError("volume must be a pandas DataFrame.")

    px = clean_close_prices.copy()
    rets = returns.copy()
    vol = volume.copy()

    px.index = pd.to_datetime(px.index)
    rets.index = pd.to_datetime(rets.index)
    vol.index = pd.to_datetime(vol.index)

    px = px.sort_index()
    rets = rets.sort_index()
    vol = vol.sort_index()

    if benchmark_ticker not in px.columns:
        raise ValueError(f"benchmark_ticker='{benchmark_ticker}' not found in clean_close_prices columns.")
    if benchmark_ticker not in rets.columns:
        raise ValueError(f"benchmark_ticker='{benchmark_ticker}' not found in returns columns.")

    # Force exact alignment to price panel
    rets = rets.reindex(index=px.index, columns=px.columns)
    vol = vol.reindex(index=px.index, columns=px.columns)

    if px.shape != rets.shape:
        raise ValueError("returns shape does not match clean_close_prices after alignment.")
    if px.shape != vol.shape:
        raise ValueError("volume shape does not match clean_close_prices after alignment.")

    return px, rets, vol


def _add_signal(
    pieces: list[pd.DataFrame],
    df: pd.DataFrame,
    signal_name: str,
) -> None:
    """
    Store a signal block with MultiIndex columns: (ticker, signal).
    """
    out = df.copy()
    out.columns = pd.MultiIndex.from_product(
        [out.columns, [signal_name]],
        names=["ticker", "signal"],
    )
    pieces.append(out)


def build_signal_library(
    clean_close_prices: pd.DataFrame,
    returns: pd.DataFrame,
    volume: pd.DataFrame,
    benchmark_ticker: str = "SPY",
    windows: Sequence[int] = (3, 5, 10, 20, 60),
    drop_benchmark_from_output: bool = True,
) -> pd.DataFrame:
    """
    Build a scalable signal library with MultiIndex columns.

    Output shape:
        index   = date
        columns = MultiIndex[ticker, signal]

    Example column:
        ('AAPL', 'mom_20')

    Notes:
    - Cross-sectional universe stays fixed to clean_close_prices.columns
    - Benchmark-relative / market-regime signals are broadcast across all tickers
    - Infinite values are replaced with NaN
    """
    px, rets, vol = _validate_inputs(
        clean_close_prices=clean_close_prices,
        returns=returns,
        volume=volume,
        benchmark_ticker=benchmark_ticker,
    )

    windows = tuple(sorted(set(int(w) for w in windows if int(w) > 0)))
    if not windows:
        raise ValueError("windows must contain at least one positive integer.")

    pieces: list[pd.DataFrame] = []

    benchmark_price = px[benchmark_ticker]
    benchmark_ret = rets[benchmark_ticker]

    # ================================================================================================================================================
    # 1. Momentum
    # ================================================================================================================================================
    for w in windows:
        _add_signal(pieces, px.pct_change(w), f"mom_{w}")

    # ================================================================================================================================================
    # 2. Reversal
    # ================================================================================================================================================
    _add_signal(pieces, -rets.shift(1), "rev_1")
    _add_signal(pieces, -px.pct_change(3).shift(1), "rev_3")
    _add_signal(pieces, -px.pct_change(5).shift(1), "rev_5")

    # ================================================================================================================================================
    # 3. Volatility Level
    # ================================================================================================================================================
    for w in windows:
        vol_level = rets.rolling(w).std()
        _add_signal(pieces, vol_level, f"vol_{w}")

    # ================================================================================================================================================
    # 4. Volatility Change / Shock
    # ================================================================================================================================================
    for w in windows:
        vol_level = rets.rolling(w).std()
        vol_change = vol_level / vol_level.shift(1)
        _add_signal(pieces, vol_change, f"volchg_{w}")

    # ================================================================================================================================================
    # 5. Trend
    # ================================================================================================================================================
    for w in windows:
        ma = px.rolling(w).mean()
        trend_flag = (px > ma).astype(float)
        dist_ma = px / ma - 1.0

        _add_signal(pieces, trend_flag, f"trend_{w}")
        _add_signal(pieces, dist_ma, f"dist_ma_{w}")

    # ================================================================================================================================================
    # 6. Mean Reversion
    # ================================================================================================================================================
    for w in windows:
        rolling_mean = rets.rolling(w).mean()
        rolling_std = rets.rolling(w).std()
        zscore = (rets - rolling_mean) / rolling_std
        _add_signal(pieces, zscore, f"zscore_{w}")

    # ================================================================================================================================================
    # 7. Relative Strength vs Benchmark
    # ================================================================================================================================================
    for w in windows:
        asset_mom = px.pct_change(w)
        bench_mom = benchmark_price.pct_change(w)
        rel_strength = asset_mom.sub(bench_mom, axis=0)
        _add_signal(pieces, rel_strength, f"relstr_{w}")

    # ================================================================================================================================================
    # 8. Price Location / Breakout
    # ================================================================================================================================================
    for w in windows:
        rolling_high = px.rolling(w).max()
        rolling_low = px.rolling(w).min()
        rolling_range = (rolling_high - rolling_low).replace(0, np.nan)

        breakout_up = (px >= rolling_high.shift(1)).astype(float)
        breakout_dn = (px <= rolling_low.shift(1)).astype(float)
        range_pos = (px - rolling_low) / rolling_range

        _add_signal(pieces, breakout_up, f"breakout_up_{w}")
        _add_signal(pieces, breakout_dn, f"breakout_dn_{w}")
        _add_signal(pieces, range_pos, f"range_pos_{w}")

    # ================================================================================================================================================
    # 9. Market Regime / Benchmark-Relative
    # ================================================================================================================================================
    # Broadcast market regime signals across all tickers so downstream modeling
    # can merge them uniformly with asset-level features.
    for w in windows:
        bench_ma = benchmark_price.rolling(w).mean()
        bench_vol = benchmark_ret.rolling(w).std()

        regime_trend = (benchmark_price > bench_ma).astype(float)
        regime_vol = bench_vol

        regime_trend_df = pd.DataFrame(
            {ticker: regime_trend for ticker in px.columns},
            index=px.index,
        )
        regime_vol_df = pd.DataFrame(
            {ticker: regime_vol for ticker in px.columns},
            index=px.index,
        )

        _add_signal(pieces, regime_trend_df, f"mkt_regime_trend_{w}")
        _add_signal(pieces, regime_vol_df, f"mkt_regime_vol_{w}")

    # ================================================================================================================================================
    # 10. Drawdown / Recovery
    # ================================================================================================================================================
    for w in windows:
        rolling_peak = px.rolling(w).max()
        rolling_trough = px.rolling(w).min()

        drawdown = px / rolling_peak - 1.0
        recovery = px / rolling_trough - 1.0

        _add_signal(pieces, drawdown, f"drawdown_{w}")
        _add_signal(pieces, recovery, f"recovery_{w}")

    # ================================================================================================================================================
    # 11. Risk-Adjusted Variants
    # ================================================================================================================================================
    for w in windows:
        mom = px.pct_change(w)
        vol_level = rets.rolling(w).std().replace(0, np.nan)
        momvol = mom / vol_level
        _add_signal(pieces, momvol, f"momvol_{w}")

    # ================================================================================================================================================
    # 12. Acceleration
    # ================================================================================================================================================
    for w in windows:
        mom = px.pct_change(w)
        accel = mom.diff()
        _add_signal(pieces, accel, f"accel_{w}")

    # ================================================================================================================================================
    # 13. Interaction Signals
    # ================================================================================================================================================
    for w in windows:
        mom = px.pct_change(w)
        vol_level = rets.rolling(w).std()
        rel = mom.sub(benchmark_price.pct_change(w), axis=0)

        mom_x_vol = mom * vol_level
        rel_x_vol = rel * vol_level

        _add_signal(pieces, mom_x_vol, f"mom_x_vol_{w}")
        _add_signal(pieces, rel_x_vol, f"rel_x_vol_{w}")

    # ================================================================================================================================================
    # 14. Volume / Liquidity Signals
    # ================================================================================================================================================
    dollar_vol = px * vol

    for w in windows:
        vol_mean = vol.rolling(w).mean()
        vol_std = vol.rolling(w).std().replace(0, np.nan)
        dollar_vol_mean = dollar_vol.rolling(w).mean()

        volavg = vol_mean
        volspike = vol / vol_mean.replace(0, np.nan)
        volz = (vol - vol_mean) / vol_std
        voltrend = (vol > vol_mean).astype(float)

        _add_signal(pieces, volavg, f"volavg_{w}")
        _add_signal(pieces, volspike, f"volspike_{w}")
        _add_signal(pieces, volz, f"volz_{w}")
        _add_signal(pieces, dollar_vol_mean, f"dollarvol_{w}")
        _add_signal(pieces, voltrend, f"voltrend_{w}")

    # ================================================================================================================================================
    # 15. Volume-Price Interaction Signals
    # ================================================================================================================================================
    for w in windows:
        vol_mean = vol.rolling(w).mean().replace(0, np.nan)
        vol_spike = vol / vol_mean
        mom = px.pct_change(w)

        ret_x_volspike = rets * vol_spike
        mom_x_volspike = mom * vol_spike

        _add_signal(pieces, ret_x_volspike, f"ret_x_volspike_{w}")
        _add_signal(pieces, mom_x_volspike, f"mom_x_volspike_{w}")

    signal_library = pd.concat(pieces, axis=1).sort_index(axis=1)
    signal_library = signal_library.replace([np.inf, -np.inf], np.nan)

    if drop_benchmark_from_output and benchmark_ticker in signal_library.columns.get_level_values("ticker"):
        signal_library = signal_library.drop(columns=benchmark_ticker, level="ticker")

    return signal_library


def signal_library_to_long(
    signal_library: pd.DataFrame,
    drop_all_nan_rows: bool = False,
) -> pd.DataFrame:
    """
    Convert wide MultiIndex signal library to ML-ready long format.

    Input:
        index   = date
        columns = MultiIndex[ticker, signal]

    Output columns:
        date, ticker, <signal_1>, <signal_2>, ...
    """
    if not isinstance(signal_library.columns, pd.MultiIndex):
        raise TypeError("signal_library must have MultiIndex columns: (ticker, signal).")

    long_df = signal_library.stack(level="ticker", future_stack=True)
    long_df.index.names = ["date", "ticker"]
    long_df = long_df.reset_index()

    if drop_all_nan_rows:
        signal_cols = [c for c in long_df.columns if c not in ["date", "ticker"]]
        long_df = long_df.dropna(subset=signal_cols, how="all")

    return long_df


def get_available_signals(signal_library: pd.DataFrame) -> list[str]:
    """
    Return sorted unique signal names from a MultiIndex-column library.
    """
    if not isinstance(signal_library.columns, pd.MultiIndex):
        raise TypeError("signal_library must have MultiIndex columns: (ticker, signal).")
    return sorted(signal_library.columns.get_level_values("signal").unique().tolist())


def select_signals(
    signal_library: pd.DataFrame,
    signal_names: Iterable[str],
) -> pd.DataFrame:
    """
    Select a subset of signals from a MultiIndex-column library.
    """
    if not isinstance(signal_library.columns, pd.MultiIndex):
        raise TypeError("signal_library must have MultiIndex columns: (ticker, signal).")

    signal_names = list(signal_names)
    mask = signal_library.columns.get_level_values("signal").isin(signal_names)
    return signal_library.loc[:, mask].copy()
