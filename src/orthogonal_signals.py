from __future__ import annotations

import numpy as np
import pandas as pd


ORTHOGONAL_VERSION = "phase2_orthogonal_signals_v2"
ORTHOGONAL_SIGNAL_SOURCE = "orthogonal_generated"
APPROVED_FOR_SCORING = "APPROVED_FOR_SCORING"
ZSCORE_CLIP_VALUE = 3.0

ORTHOGONAL_SIGNAL_SPECS = [
    {
        "signal_name": "relative_return_rank_20",
        "signal_family": "cross_sectional_relative_value",
        "orthogonal_cluster": "cross_sectional_relative_value",
        "formula_type": "cross_sectional_rank_of_20d_return",
        "required_inputs": ["close"],
        "lookback": 20,
        "expected_horizon": "5d_to_20d",
        "direction_convention": "higher_is_stronger_relative_return",
    },
    {
        "signal_name": "relative_return_zscore_60",
        "signal_family": "cross_sectional_relative_value",
        "orthogonal_cluster": "cross_sectional_relative_value",
        "formula_type": "cross_sectional_zscore_of_60d_return",
        "required_inputs": ["close"],
        "lookback": 60,
        "expected_horizon": "20d_to_60d",
        "direction_convention": "higher_is_stronger_relative_return",
    },
    {
        "signal_name": "residual_return_vs_universe_20",
        "signal_family": "cross_sectional_relative_value",
        "orthogonal_cluster": "cross_sectional_relative_value",
        "formula_type": "20d_return_minus_universe_mean_return",
        "required_inputs": ["close"],
        "lookback": 20,
        "expected_horizon": "5d_to_20d",
        "direction_convention": "higher_is_positive_universe_relative_residual",
    },
    {
        "signal_name": "overnight_gap_reversal_1",
        "signal_family": "true_short_term_reversal",
        "orthogonal_cluster": "true_short_term_reversal",
        "formula_type": "negative_open_to_prior_close_gap",
        "required_inputs": ["open", "close"],
        "lookback": 1,
        "expected_horizon": "1d_to_5d",
        "direction_convention": "higher_is_larger_gap_down_reversal_candidate",
    },
    {
        "signal_name": "intraday_reversal_strength_1",
        "signal_family": "true_short_term_reversal",
        "orthogonal_cluster": "true_short_term_reversal",
        "formula_type": "negative_open_to_close_return",
        "required_inputs": ["open", "close"],
        "lookback": 1,
        "expected_horizon": "1d_to_5d",
        "direction_convention": "higher_is_larger_intraday_selloff_reversal_candidate",
    },
    {
        "signal_name": "three_day_overextension_reversal",
        "signal_family": "true_short_term_reversal",
        "orthogonal_cluster": "true_short_term_reversal",
        "formula_type": "negative_3d_return_scaled_by_20d_volatility",
        "required_inputs": ["close"],
        "lookback": 20,
        "expected_horizon": "1d_to_5d",
        "direction_convention": "higher_is_more_overextended_downward",
    },
    {
        "signal_name": "vol_surprise_20_60",
        "signal_family": "volatility_structure",
        "orthogonal_cluster": "volatility_structure",
        "formula_type": "20d_realized_vol_minus_60d_realized_vol",
        "required_inputs": ["close"],
        "lookback": 60,
        "expected_horizon": "5d_to_20d",
        "direction_convention": "higher_is_positive_short_vol_surprise",
    },
    {
        "signal_name": "vol_of_vol_20",
        "signal_family": "volatility_structure",
        "orthogonal_cluster": "volatility_structure",
        "formula_type": "20d_std_of_absolute_daily_returns",
        "required_inputs": ["close"],
        "lookback": 20,
        "expected_horizon": "5d_to_20d",
        "direction_convention": "higher_is_more_unstable_realized_volatility",
    },
    {
        "signal_name": "range_expansion_failure_5",
        "signal_family": "volatility_structure",
        "orthogonal_cluster": "volatility_structure",
        "formula_type": "wide_5d_range_with_weak_close_location",
        "required_inputs": ["high", "low", "close"],
        "lookback": 20,
        "expected_horizon": "1d_to_10d",
        "direction_convention": "higher_is_failed_range_expansion",
    },
    {
        "signal_name": "dollar_volume_shock_20",
        "signal_family": "liquidity_flow",
        "orthogonal_cluster": "liquidity_flow",
        "formula_type": "dollar_volume_vs_trailing_20d_mean",
        "required_inputs": ["close", "volume"],
        "lookback": 20,
        "expected_horizon": "1d_to_10d",
        "direction_convention": "higher_is_unusual_dollar_volume",
    },
    {
        "signal_name": "liquidity_adjusted_reversal_5",
        "signal_family": "liquidity_flow",
        "orthogonal_cluster": "liquidity_flow",
        "formula_type": "negative_5d_return_scaled_by_dollar_volume_rank",
        "required_inputs": ["close", "volume"],
        "lookback": 20,
        "expected_horizon": "1d_to_10d",
        "direction_convention": "higher_is_liquid_short_term_pullback",
    },
    {
        "signal_name": "price_impact_proxy_20",
        "signal_family": "liquidity_flow",
        "orthogonal_cluster": "liquidity_flow",
        "formula_type": "20d_mean_abs_return_per_dollar_volume",
        "required_inputs": ["close", "volume"],
        "lookback": 20,
        "expected_horizon": "5d_to_20d",
        "direction_convention": "higher_is_higher_price_impact",
    },
    {
        "signal_name": "range_compression_breakout_10",
        "signal_family": "microstructure_lite",
        "orthogonal_cluster": "microstructure_lite",
        "formula_type": "low_10d_range_followed_by_close_near_range_high",
        "required_inputs": ["high", "low", "close"],
        "lookback": 20,
        "expected_horizon": "1d_to_10d",
        "direction_convention": "higher_is_compression_breakout",
    },
    {
        "signal_name": "close_position_reversal_5",
        "signal_family": "microstructure_lite",
        "orthogonal_cluster": "microstructure_lite",
        "formula_type": "close_near_5d_low_reversal_setup",
        "required_inputs": ["high", "low", "close"],
        "lookback": 5,
        "expected_horizon": "1d_to_5d",
        "direction_convention": "higher_is_close_near_recent_low",
    },
    {
        "signal_name": "failed_breakout_reversal_20",
        "signal_family": "microstructure_lite",
        "orthogonal_cluster": "microstructure_lite",
        "formula_type": "prior_20d_high_break_with_weak_close",
        "required_inputs": ["high", "low", "close"],
        "lookback": 20,
        "expected_horizon": "1d_to_10d",
        "direction_convention": "higher_is_failed_breakout_reversal_candidate",
    },
]


def _safe_divide(numerator: pd.DataFrame, denominator: pd.DataFrame | pd.Series) -> pd.DataFrame:
    output = numerator.div(denominator.replace(0, np.nan), axis=0 if isinstance(denominator, pd.Series) else "columns")
    return output.replace([np.inf, -np.inf], np.nan)


def cross_sectional_zscore(panel: pd.DataFrame, clip_value: float = ZSCORE_CLIP_VALUE) -> pd.DataFrame:
    """Cross-sectionally z-score a Date x ticker panel using same-date values only."""
    cleaned = panel.replace([np.inf, -np.inf], np.nan).astype(float)
    row_mean = cleaned.mean(axis=1, skipna=True)
    row_std = cleaned.std(axis=1, skipna=True).replace(0, np.nan)
    zscored = cleaned.sub(row_mean, axis=0).div(row_std, axis=0)
    return zscored.replace([np.inf, -np.inf], np.nan).clip(-clip_value, clip_value)


def _cross_sectional_rank_centered(panel: pd.DataFrame) -> pd.DataFrame:
    ranked = panel.replace([np.inf, -np.inf], np.nan).rank(axis=1, pct=True)
    return (ranked - 0.5) * 2.0


def _rolling_percentile_rank(panel: pd.DataFrame, window: int = 126, min_periods: int = 40) -> pd.DataFrame:
    ranked = panel.replace([np.inf, -np.inf], np.nan).rolling(window, min_periods=min_periods).rank(pct=True)
    return (ranked - 0.5) * 2.0


def _ema_smooth(panel: pd.DataFrame, span: int = 5) -> pd.DataFrame:
    return panel.replace([np.inf, -np.inf], np.nan).ewm(span=span, min_periods=max(2, span // 2)).mean()


def _blend_panels(panels: list[pd.DataFrame], weights: list[float]) -> pd.DataFrame:
    total_weight = sum(weights)
    blended = sum(panel * weight for panel, weight in zip(panels, weights)) / total_weight
    return blended.replace([np.inf, -np.inf], np.nan)


def _soft_condition(panel: pd.DataFrame, condition: pd.DataFrame, inactive_scale: float = 0.25) -> pd.DataFrame:
    return panel.where(condition, panel * inactive_scale)


def _range_position(close: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, window: int) -> pd.DataFrame:
    trailing_high = high.rolling(window, min_periods=max(2, window // 2)).max()
    trailing_low = low.rolling(window, min_periods=max(2, window // 2)).min()
    return _safe_divide(close - trailing_low, trailing_high - trailing_low)


def _metadata_frame(run_id: str, created_timestamp: str) -> pd.DataFrame:
    rows = []
    for spec in ORTHOGONAL_SIGNAL_SPECS:
        rows.append(
            {
                **spec,
                "required_inputs": ",".join(spec["required_inputs"]),
                "signal_source": ORTHOGONAL_SIGNAL_SOURCE,
                "orthogonal_version": ORTHOGONAL_VERSION,
                "run_id": run_id,
                "created_timestamp": created_timestamp,
                "normalization": "cross_sectional_zscore_by_date_clipped_3"
                if "rank" not in spec["formula_type"]
                else "cross_sectional_rank_centered_by_date",
            }
        )
    return pd.DataFrame(rows)


def build_orthogonal_signal_candidates(
    ohlcv: dict[str, pd.DataFrame],
    benchmark_prices: pd.DataFrame | None,
    run_id: str,
    created_timestamp: str,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Generate controlled orthogonal signal panels from OHLCV and benchmark data."""
    del benchmark_prices

    open_ = ohlcv["open"].astype(float).sort_index()
    high = ohlcv["high"].astype(float).sort_index()
    low = ohlcv["low"].astype(float).sort_index()
    close = ohlcv["close"].astype(float).sort_index()
    volume = ohlcv["volume"].astype(float).sort_index()

    returns_1d = close.pct_change()
    returns_3d = close.pct_change(3)
    returns_5d = close.pct_change(5)
    returns_10d = close.pct_change(10)
    returns_20d = close.pct_change(20)
    returns_60d = close.pct_change(60)
    realized_vol_20 = returns_1d.rolling(20, min_periods=10).std()
    realized_vol_60 = returns_1d.rolling(60, min_periods=30).std()
    dollar_volume = close * volume
    dollar_volume_mean_20 = dollar_volume.rolling(20, min_periods=10).mean()
    dollar_volume_rank_20 = _cross_sectional_rank_centered(dollar_volume_mean_20).add(1.0).div(2.0)
    range_5 = high.rolling(5, min_periods=3).max() - low.rolling(5, min_periods=3).min()
    range_10 = high.rolling(10, min_periods=5).max() - low.rolling(10, min_periods=5).min()
    range_20 = high.rolling(20, min_periods=10).max() - low.rolling(20, min_periods=10).min()
    range_pos_5 = _range_position(close, high, low, 5)
    range_pos_10 = _range_position(close, high, low, 10)
    range_pos_20 = _range_position(close, high, low, 20)
    prior_20_high = high.shift(1).rolling(20, min_periods=10).max()
    trend_strength_20 = close / close.rolling(20, min_periods=10).mean() - 1.0
    trend_strength_50 = close / close.rolling(50, min_periods=25).mean() - 1.0
    trend_rank_50 = _cross_sectional_rank_centered(trend_strength_50)
    trend_up = trend_rank_50 > 0.10
    trend_down = trend_rank_50 < -0.10
    high_vol = _cross_sectional_rank_centered(realized_vol_20) > 0.10
    low_vol = _cross_sectional_rank_centered(realized_vol_20) < -0.10
    liquid = dollar_volume_rank_20 > 0.45
    vol_interaction = _cross_sectional_rank_centered(realized_vol_20 - realized_vol_60).add(1.0).div(2.0)

    relative_return_blend = _blend_panels(
        [
            returns_5d.sub(returns_5d.mean(axis=1), axis=0),
            returns_10d.sub(returns_10d.mean(axis=1), axis=0),
            returns_20d.sub(returns_20d.mean(axis=1), axis=0),
        ],
        [0.25, 0.35, 0.40],
    )
    vol_adjusted_relative_return = _safe_divide(relative_return_blend, realized_vol_20)
    reversal_blend = _blend_panels([-returns_5d, -returns_10d, -returns_20d], [0.50, 0.30, 0.20])
    vol_adjusted_reversal = _safe_divide(reversal_blend, realized_vol_20)
    volume_shock_blend = _blend_panels(
        [
            _safe_divide(dollar_volume, dollar_volume.rolling(5, min_periods=3).mean()) - 1.0,
            _safe_divide(dollar_volume, dollar_volume.rolling(10, min_periods=5).mean()) - 1.0,
            _safe_divide(dollar_volume, dollar_volume_mean_20) - 1.0,
        ],
        [0.20, 0.30, 0.50],
    )
    range_compression = -_safe_divide(range_10, range_20)
    breakout_pressure = range_pos_10 * trend_rank_50
    failed_breakout = high.gt(prior_20_high).astype(float) * (1.0 - range_pos_20)
    range_failure = _safe_divide(range_5, range_20) * (1.0 - range_pos_5) * high_vol.astype(float)

    raw_signals = {
        "relative_return_rank_20": _soft_condition(_rolling_percentile_rank(relative_return_blend, 126, 40), trend_up | low_vol),
        "relative_return_zscore_60": _soft_condition(_rolling_percentile_rank(_safe_divide(returns_60d, realized_vol_60), 126, 40), trend_up),
        "residual_return_vs_universe_20": _soft_condition(_rolling_percentile_rank(vol_adjusted_relative_return, 126, 40), trend_up | high_vol),
        "overnight_gap_reversal_1": _soft_condition(_rolling_percentile_rank(_ema_smooth(-(open_ / close.shift(1) - 1.0), 3), 63, 20), high_vol | trend_down),
        "intraday_reversal_strength_1": _soft_condition(_rolling_percentile_rank(_ema_smooth(-(close / open_ - 1.0), 3), 63, 20), high_vol | trend_down),
        "three_day_overextension_reversal": _soft_condition(_rolling_percentile_rank(_ema_smooth(_safe_divide(-returns_3d, realized_vol_20), 5), 63, 20), high_vol | trend_down),
        "vol_surprise_20_60": _soft_condition(_rolling_percentile_rank(_ema_smooth(realized_vol_20 - realized_vol_60, 5), 126, 40), high_vol),
        "vol_of_vol_20": _soft_condition(_rolling_percentile_rank(_ema_smooth(returns_1d.abs().rolling(20, min_periods=10).std(), 5), 126, 40), high_vol),
        "range_expansion_failure_5": _soft_condition(_rolling_percentile_rank(_ema_smooth(range_failure, 5), 63, 20), high_vol | trend_down),
        "dollar_volume_shock_20": _soft_condition(_rolling_percentile_rank(_ema_smooth(volume_shock_blend * (0.5 + vol_interaction), 5), 126, 40), high_vol | liquid),
        "liquidity_adjusted_reversal_5": _soft_condition(_rolling_percentile_rank(_ema_smooth(vol_adjusted_reversal * dollar_volume_rank_20, 5), 63, 20), liquid & (high_vol | trend_down)),
        "price_impact_proxy_20": _soft_condition(_rolling_percentile_rank(_ema_smooth(_safe_divide(returns_1d.abs(), dollar_volume).rolling(20, min_periods=10).mean() * (0.5 + vol_interaction), 5), 126, 40), high_vol),
        "range_compression_breakout_10": _soft_condition(_rolling_percentile_rank(_ema_smooth(range_compression + breakout_pressure, 5), 63, 20), low_vol & trend_up),
        "close_position_reversal_5": _soft_condition(_rolling_percentile_rank(_ema_smooth((1.0 - range_pos_5) * (1.0 - trend_rank_50.clip(lower=-1.0, upper=1.0)), 5), 63, 20), high_vol | trend_down),
        "failed_breakout_reversal_20": _soft_condition(_rolling_percentile_rank(_ema_smooth(failed_breakout * (1.0 + trend_strength_20.abs()), 5), 63, 20), high_vol | trend_down),
    }

    signals = {}
    for spec in ORTHOGONAL_SIGNAL_SPECS:
        name = spec["signal_name"]
        raw = raw_signals[name].replace([np.inf, -np.inf], np.nan)
        if name == "relative_return_rank_20":
            signal = raw
        else:
            signal = cross_sectional_zscore(raw)
        signals[name] = signal.sort_index().sort_index(axis=1)

    return signals, _metadata_frame(run_id=run_id, created_timestamp=created_timestamp)


def build_orthogonal_signal_quality(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    run_id: str,
) -> pd.DataFrame:
    """Build structural quality diagnostics with all-NaN and near-constant rejection flags."""
    metadata_lookup = metadata.set_index("signal_name").to_dict("index")
    rows = []
    for signal_name, panel in signals.items():
        values = panel.replace([np.inf, -np.inf], np.nan)
        finite = np.isfinite(values)
        valid_dates = finite.any(axis=1)
        finite_values = values.where(finite).stack(future_stack=True)
        finite_pct = float(finite.sum().sum() / values.size) if values.size else np.nan
        missing_pct = float(values.isna().sum().sum() / values.size) if values.size else np.nan
        is_all_nan = bool(finite.sum().sum() == 0)
        near_constant = bool(finite_values.std(skipna=True) < 1e-8) if not finite_values.empty else True
        status = "REJECTED_ALL_NAN" if is_all_nan else "REJECTED_NEAR_CONSTANT" if near_constant else APPROVED_FOR_SCORING
        rows.append(
            {
                "signal_name": signal_name,
                "signal_family": metadata_lookup.get(signal_name, {}).get("signal_family"),
                "orthogonal_cluster": metadata_lookup.get(signal_name, {}).get("orthogonal_cluster"),
                "finite_pct": finite_pct,
                "missing_pct": missing_pct,
                "n_dates": int(values.shape[0]),
                "n_tickers": int(values.shape[1]),
                "first_valid_date": values.index[valid_dates].min() if valid_dates.any() else pd.NaT,
                "last_valid_date": values.index[valid_dates].max() if valid_dates.any() else pd.NaT,
                "is_all_nan": is_all_nan,
                "is_near_constant": near_constant,
                "status": status,
                "quality_notes": "Passes basic finite and variation checks."
                if status == APPROVED_FOR_SCORING
                else "Rejected by orthogonal signal structural quality checks.",
                "orthogonal_version": ORTHOGONAL_VERSION,
                "run_id": run_id,
            }
        )
    return pd.DataFrame(rows)


def build_orthogonal_family_summary(quality: pd.DataFrame, run_id: str) -> pd.DataFrame:
    """Summarize orthogonal signal counts and quality by cluster."""
    summary = (
        quality.groupby("orthogonal_cluster", dropna=False)
        .agg(
            n_signals=("signal_name", "nunique"),
            n_approved=("status", lambda s: int(s.eq(APPROVED_FOR_SCORING).sum())),
            n_rejected=("status", lambda s: int(s.ne(APPROVED_FOR_SCORING).sum())),
            avg_finite_pct=("finite_pct", "mean"),
            avg_missing_pct=("missing_pct", "mean"),
            first_valid_date=("first_valid_date", "min"),
            last_valid_date=("last_valid_date", "max"),
        )
        .reset_index()
    )
    summary["orthogonal_version"] = ORTHOGONAL_VERSION
    summary["run_id"] = run_id
    return summary


__all__ = [
    "APPROVED_FOR_SCORING",
    "ORTHOGONAL_SIGNAL_SPECS",
    "ORTHOGONAL_SIGNAL_SOURCE",
    "ORTHOGONAL_VERSION",
    "build_orthogonal_family_summary",
    "build_orthogonal_signal_candidates",
    "build_orthogonal_signal_quality",
    "cross_sectional_zscore",
]
