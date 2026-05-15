from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd


EXPANDED_DISCOVERY_VERSION = "phase2_expanded_discovery_v1"
EXPANSION_BATCH_VERSION = "phase2_expansion_batch_v1"
EXPANSION_BATCH_V2_VERSION = "phase2_expansion_batch_v2"
EXPANDED_DISCOVERY_SOURCE = "expanded_discovery"
CORE_ALPHA_NAME = "alpha_regime_blend_dynamic_v4_smooth"
DISCOVERY_HORIZONS = [1, 5, 10, 20]


@dataclass(frozen=True)
class ExpandedSignalSpec:
    signal_name: str
    signal_family: str
    formula_type: str
    lookback: int
    direction_convention: str
    data_dependencies: tuple[str, ...]
    intended_alpha_sleeve: str = "ORTHOGONAL_DIVERSIFIER"
    parameters: dict[str, object] | None = None
    description: str = ""
    expected_direction: str = ""
    economic_intuition: str = ""
    required_inputs: tuple[str, ...] = ()
    known_risks: str = ""
    expansion_batch: str = ""
    refinement_source: str = ""
    targeted_failure_mode: str = ""
    expected_improvement: str = ""


EXPANDED_SIGNAL_SPECS = [
    ExpandedSignalSpec("expanded_reversal_1d", "mean_reversion", "negative_close_return", 1, "higher_is_more_oversold", ("close",)),
    ExpandedSignalSpec("expanded_reversal_3d", "mean_reversion", "negative_close_return", 3, "higher_is_more_oversold", ("close",)),
    ExpandedSignalSpec("expanded_reversal_5d", "mean_reversion", "negative_close_return", 5, "higher_is_more_oversold", ("close",)),
    ExpandedSignalSpec("expanded_distance_ma_10", "mean_reversion", "negative_distance_to_ma", 10, "higher_is_farther_below_ma", ("close",)),
    ExpandedSignalSpec("expanded_distance_ma_20", "mean_reversion", "negative_distance_to_ma", 20, "higher_is_farther_below_ma", ("close",)),
    ExpandedSignalSpec("expanded_zscore_reversal_20", "mean_reversion", "negative_price_zscore", 20, "higher_is_more_oversold_vs_20d_mean", ("close",)),
    ExpandedSignalSpec("expanded_residual_market_return_20", "residual_relative_value", "negative_market_residual_return", 20, "higher_is_negative_market_residual", ("close",)),
    ExpandedSignalSpec("expanded_beta_adjusted_residual_20", "residual_relative_value", "negative_beta_adjusted_residual", 60, "higher_is_negative_beta_adjusted_residual", ("close",)),
    ExpandedSignalSpec("expanded_residual_zscore_20", "residual_relative_value", "negative_market_residual_zscore", 20, "higher_is_negative_residual_zscore", ("close",)),
    ExpandedSignalSpec("expanded_abnormal_volume_20", "liquidity_flow", "volume_zscore", 20, "higher_is_abnormal_volume", ("volume",)),
    ExpandedSignalSpec("expanded_volume_acceleration_5_20", "liquidity_flow", "volume_acceleration", 20, "higher_is_accelerating_volume", ("volume",), parameters={"fast": 5, "slow": 20}),
    ExpandedSignalSpec("expanded_price_volume_divergence_20", "liquidity_flow", "negative_return_volume_divergence", 20, "higher_is_price_down_volume_up", ("close", "volume")),
    ExpandedSignalSpec("expanded_amihud_change_20", "liquidity_flow", "amihud_illiquidity_change", 20, "higher_is_improving_liquidity", ("close", "volume")),
    ExpandedSignalSpec("expanded_vol_compression_20", "volatility_structure", "negative_realized_volatility_zscore", 20, "higher_is_volatility_compression", ("close",)),
    ExpandedSignalSpec("expanded_vol_ratio_5_20", "volatility_structure", "realized_vol_ratio", 20, "higher_is_short_vol_expansion", ("close",), parameters={"fast": 5, "slow": 20}),
    ExpandedSignalSpec("expanded_range_expansion_failure_10", "volatility_structure", "range_expansion_failure", 10, "higher_is_failed_range_expansion", ("high", "low", "close")),
    ExpandedSignalSpec("expanded_downside_vol_asymmetry_20", "volatility_structure", "negative_downside_vol_asymmetry", 20, "higher_is_less_downside_vol_dominance", ("close",)),
    ExpandedSignalSpec("expanded_low_vol_strength_20", "quality_stability", "low_vol_positive_return", 20, "higher_is_positive_return_low_vol", ("close",)),
    ExpandedSignalSpec("expanded_drawdown_recovery_20", "quality_stability", "drawdown_recovery", 20, "higher_is_recovering_from_drawdown", ("close",)),
    ExpandedSignalSpec("expanded_trend_stability_20", "quality_stability", "trend_stability", 20, "higher_is_stable_positive_trend", ("close",)),
    ExpandedSignalSpec("expanded_return_consistency_20", "quality_stability", "return_consistency", 20, "higher_is_consistent_positive_returns", ("close",)),
    ExpandedSignalSpec(
        "vol_compression_breakout_20_60",
        "volatility_structure",
        "vol_compression_breakout",
        60,
        "higher_is_volatility_compression_vs_60d_baseline",
        ("close",),
        parameters={"fast": 20, "slow": 60},
        description="Realized volatility compression using 20-day volatility versus a 60-day baseline.",
        expected_direction="Higher values indicate compressed realized volatility; expected positive convexity/continuation candidate.",
        economic_intuition="Sustained compression can precede tradable volatility expansion and fresh directional information.",
        required_inputs=("close",),
        known_risks="May overlap with range-compression signals and can be regime dependent.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "downside_vol_asymmetry_20",
        "volatility_structure",
        "downside_vol_asymmetry",
        20,
        "higher_is_lower_downside_vol_dominance",
        ("close",),
        description="Downside realized volatility share over a 20-day window, oriented so lower downside dominance ranks higher.",
        expected_direction="Higher values are expected to be more favorable because downside volatility is less dominant.",
        economic_intuition="Names with less downside volatility concentration may have cleaner risk-adjusted continuation behavior.",
        required_inputs=("close",),
        known_risks="May behave defensively and overlap with low-volatility quality effects.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "index_relative_reversal_5",
        "residual_relative_value",
        "index_relative_reversal",
        5,
        "higher_is_more_oversold_vs_universe",
        ("close",),
        description="Negative 5-day stock return residual versus the equal-weight universe return.",
        expected_direction="Higher values indicate recent underperformance versus the universe and a possible reversal edge.",
        economic_intuition="Short-horizon idiosyncratic underperformance can mean-revert after broad market movement is removed.",
        required_inputs=("close",),
        known_risks="Can overlap with existing mean-reversion and residual-return signals.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "smooth_trend_persistence_60",
        "trend_quality",
        "smooth_trend_persistence",
        60,
        "higher_is_smoother_positive_trend",
        ("close",),
        description="60-day return divided by 60-day absolute-return path length.",
        expected_direction="Higher values indicate smoother positive trend persistence.",
        economic_intuition="A smoother path may indicate more durable institutional accumulation than jumpy raw momentum.",
        required_inputs=("close",),
        known_risks="May lag sharp reversals and overlap with momentum quality.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "trend_consistency_20_60",
        "trend_quality",
        "trend_consistency_20_60",
        60,
        "higher_is_consistent_intermediate_positive_trend",
        ("close",),
        parameters={"return_window": 5, "consistency_window": 60},
        description="Share of positive rolling 5-day returns over 60 days, signed by the 60-day return direction.",
        expected_direction="Higher values indicate consistent positive intermediate trend.",
        economic_intuition="Persistent smaller wins may be more robust than a single large trailing return.",
        required_inputs=("close",),
        known_risks="Can be slow to react near regime turns.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "percentile_rank_stability_20",
        "breadth_cross_sectional_context",
        "percentile_rank_stability",
        20,
        "higher_is_stable_relative_strength_leadership",
        ("close",),
        description="Cross-sectional 20-day return percentile minus recent instability of that percentile rank.",
        expected_direction="Higher values indicate stable relative-strength leadership.",
        economic_intuition="Stable leadership may identify names with persistent sponsorship rather than noisy one-day jumps.",
        required_inputs=("close",),
        known_risks="May overlap with relative strength and can penalize emerging breakouts.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "volume_flow_ratio_5_20",
        "liquidity_flow",
        "volume_flow_ratio",
        20,
        "higher_is_rising_recent_dollar_volume",
        ("close", "volume"),
        parameters={"fast": 5, "slow": 20},
        description="5-day average dollar volume divided by 20-day average dollar volume.",
        expected_direction="Higher values indicate recent participation is rising versus the trailing baseline.",
        economic_intuition="Rising participation can confirm attention and reduce sparsity versus acceleration-style volume signals.",
        required_inputs=("close", "volume"),
        known_risks="Can flag crowdedness or event-driven volume spikes rather than persistent edge.",
        expansion_batch=EXPANSION_BATCH_VERSION,
    ),
    ExpandedSignalSpec(
        "trend_consistency_20_60_persistent",
        "trend_quality",
        "trend_consistency_20_60_persistent",
        60,
        "higher_is_consistent_intermediate_positive_trend_with_confirmation",
        ("close",),
        parameters={"return_window": 5, "consistency_window": 60, "confirmation_window": 3},
        description="Batch 2 refinement of trend consistency that keeps the 20/60 trend-consistency core and adds a minimal recent same-sign confirmation filter.",
        expected_direction="Higher values indicate consistent positive intermediate trend with recent trend-sign confirmation.",
        economic_intuition="Requiring recent trend agreement should reduce one-off trend consistency readings that do not persist out of sample.",
        required_inputs=("close",),
        known_risks="May lag turning points and reduce signal amplitude when trend transitions are abrupt.",
        expansion_batch=EXPANSION_BATCH_V2_VERSION,
        refinement_source="trend_consistency_20_60",
        targeted_failure_mode="low persistence; low sign consistency; weak effective IC",
        expected_improvement="Improve WFV persistence and sign consistency by retaining only recently confirmed trend-consistency readings.",
    ),
    ExpandedSignalSpec(
        "index_relative_reversal_5_vol_adj",
        "residual_relative_value",
        "index_relative_reversal_vol_adj",
        5,
        "higher_is_more_oversold_vs_universe_after_vol_adjustment",
        ("close",),
        parameters={"reversal_window": 5, "vol_window": 20},
        description="Batch 2 refinement of index-relative reversal that scales 5-day relative underperformance by recent realized volatility.",
        expected_direction="Higher values indicate volatility-adjusted underperformance versus the equal-weight universe and a possible reversal edge.",
        economic_intuition="Volatility scaling should reduce noisy high-volatility reversals that can flip direction out of sample.",
        required_inputs=("close",),
        known_risks="May dampen genuine high-volatility reversal opportunities and overlap with residual reversal signals.",
        expansion_batch=EXPANSION_BATCH_V2_VERSION,
        refinement_source="index_relative_reversal_5",
        targeted_failure_mode="direction flip; weak effective IC IR; regime instability",
        expected_improvement="Improve effective IC robustness by normalizing residual reversal magnitude by trailing realized volatility.",
    ),
    ExpandedSignalSpec(
        "index_relative_reversal_5_confirmed",
        "residual_relative_value",
        "index_relative_reversal_confirmed",
        5,
        "higher_is_recently_stabilized_oversold_vs_universe",
        ("close",),
        parameters={"reversal_window": 5, "confirmation_window": 1},
        description="Batch 2 refinement of index-relative reversal that requires a minimal one-day stabilization confirmation after relative underperformance.",
        expected_direction="Higher values indicate recent relative underperformance that has stopped worsening on the latest day.",
        economic_intuition="A small delayed-entry confirmation should reduce catching falling names before reversal pressure stabilizes.",
        required_inputs=("close",),
        known_risks="Delayed confirmation may miss fast rebounds and reduce the number of active reversal observations.",
        expansion_batch=EXPANSION_BATCH_V2_VERSION,
        refinement_source="index_relative_reversal_5",
        targeted_failure_mode="direction flip; low sign consistency; weak effective IC",
        expected_improvement="Improve sign consistency by requiring oversold names to show minimal recent relative stabilization before ranking strongly.",
    ),
]


def _safe_divide(numerator: pd.DataFrame, denominator: pd.DataFrame | float) -> pd.DataFrame:
    return numerator / pd.DataFrame(denominator, index=numerator.index, columns=numerator.columns).replace(0.0, np.nan) if not np.isscalar(denominator) else numerator / denominator


def cross_sectional_zscore(panel: pd.DataFrame, clip_value: float = 3.0) -> pd.DataFrame:
    values = panel.copy().apply(pd.to_numeric, errors="coerce")
    mean = values.mean(axis=1, skipna=True)
    std = values.std(axis=1, skipna=True).replace(0.0, np.nan)
    z = values.sub(mean, axis=0).div(std, axis=0)
    return z.clip(lower=-clip_value, upper=clip_value).replace([np.inf, -np.inf], np.nan)


def _returns(close: pd.DataFrame) -> pd.DataFrame:
    return close.pct_change(fill_method=None)


def _market_return(close: pd.DataFrame) -> pd.Series:
    return _returns(close).mean(axis=1, skipna=True)


def _rolling_beta(stock_returns: pd.DataFrame, market_returns: pd.Series, window: int) -> pd.DataFrame:
    market = pd.DataFrame({column: market_returns for column in stock_returns.columns}, index=stock_returns.index)
    covariance = stock_returns.rolling(window, min_periods=max(5, window // 2)).cov(market)
    variance = market.rolling(window, min_periods=max(5, window // 2)).var()
    return covariance / variance.replace(0.0, np.nan)


def _raw_signal_panel(spec: ExpandedSignalSpec, ohlcv: dict[str, pd.DataFrame]) -> pd.DataFrame:
    close = ohlcv["close"].copy().apply(pd.to_numeric, errors="coerce")
    high = ohlcv.get("high", close).copy().apply(pd.to_numeric, errors="coerce")
    low = ohlcv.get("low", close).copy().apply(pd.to_numeric, errors="coerce")
    volume = ohlcv.get("volume", pd.DataFrame(index=close.index, columns=close.columns)).copy().apply(pd.to_numeric, errors="coerce")
    returns = _returns(close)
    lookback = spec.lookback

    if spec.formula_type == "negative_close_return":
        return -close.pct_change(lookback, fill_method=None)
    if spec.formula_type == "negative_distance_to_ma":
        ma = close.rolling(lookback, min_periods=max(3, lookback // 2)).mean()
        return -(close / ma - 1.0)
    if spec.formula_type == "negative_price_zscore":
        ma = close.rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        sd = close.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return -((close - ma) / sd.replace(0.0, np.nan))
    if spec.formula_type == "negative_market_residual_return":
        stock_ret = close.pct_change(lookback, fill_method=None)
        market_ret = stock_ret.mean(axis=1, skipna=True)
        return stock_ret.sub(market_ret, axis=0).mul(-1.0)
    if spec.formula_type == "negative_beta_adjusted_residual":
        market = _market_return(close)
        beta = _rolling_beta(returns, market, lookback)
        residual = returns.sub(beta.mul(market, axis=0), axis=0).rolling(20, min_periods=10).sum()
        return -residual
    if spec.formula_type == "negative_market_residual_zscore":
        residual = returns.sub(_market_return(close), axis=0)
        mean = residual.rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        sd = residual.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return -((residual - mean) / sd.replace(0.0, np.nan))
    if spec.formula_type == "volume_zscore":
        mean = volume.rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        sd = volume.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return (volume - mean) / sd.replace(0.0, np.nan)
    if spec.formula_type == "volume_acceleration":
        fast = int((spec.parameters or {}).get("fast", 5))
        slow = int((spec.parameters or {}).get("slow", lookback))
        fast_mean = volume.rolling(fast, min_periods=max(2, fast // 2)).mean()
        slow_mean = volume.rolling(slow, min_periods=max(5, slow // 2)).mean()
        return fast_mean / slow_mean.replace(0.0, np.nan) - 1.0
    if spec.formula_type == "negative_return_volume_divergence":
        ret = close.pct_change(lookback, fill_method=None)
        vol_accel = volume.rolling(5, min_periods=3).mean() / volume.rolling(lookback, min_periods=max(5, lookback // 2)).mean().replace(0.0, np.nan) - 1.0
        return -ret * vol_accel
    if spec.formula_type == "amihud_illiquidity_change":
        dollar_volume = (close * volume).replace(0.0, np.nan)
        illiq = returns.abs() / dollar_volume
        recent = illiq.rolling(5, min_periods=3).mean()
        base = illiq.rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        return -(recent / base.replace(0.0, np.nan) - 1.0)
    if spec.formula_type == "negative_realized_volatility_zscore":
        vol = returns.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        vol_mean = vol.rolling(60, min_periods=20).mean()
        vol_sd = vol.rolling(60, min_periods=20).std()
        return -((vol - vol_mean) / vol_sd.replace(0.0, np.nan))
    if spec.formula_type == "realized_vol_ratio":
        fast = int((spec.parameters or {}).get("fast", 5))
        slow = int((spec.parameters or {}).get("slow", lookback))
        return returns.rolling(fast, min_periods=max(2, fast // 2)).std() / returns.rolling(slow, min_periods=max(5, slow // 2)).std().replace(0.0, np.nan)
    if spec.formula_type == "range_expansion_failure":
        intraday_range = (high - low) / close.replace(0.0, np.nan)
        range_z = (intraday_range - intraday_range.rolling(lookback, min_periods=max(5, lookback // 2)).mean()) / intraday_range.rolling(lookback, min_periods=max(5, lookback // 2)).std().replace(0.0, np.nan)
        close_position = (close - low) / (high - low).replace(0.0, np.nan)
        return range_z * (0.5 - close_position)
    if spec.formula_type == "negative_downside_vol_asymmetry":
        downside = returns.where(returns < 0).rolling(lookback, min_periods=max(5, lookback // 2)).std()
        total = returns.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return -(downside / total.replace(0.0, np.nan))
    if spec.formula_type == "low_vol_positive_return":
        ret = close.pct_change(lookback, fill_method=None)
        vol = returns.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return ret / vol.replace(0.0, np.nan)
    if spec.formula_type == "drawdown_recovery":
        rolling_high = close.rolling(lookback, min_periods=max(5, lookback // 2)).max()
        drawdown = close / rolling_high.replace(0.0, np.nan) - 1.0
        recent_recovery = close.pct_change(5, fill_method=None)
        return recent_recovery - drawdown.abs()
    if spec.formula_type == "trend_stability":
        ret = returns.rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        vol = returns.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return ret / vol.replace(0.0, np.nan)
    if spec.formula_type == "return_consistency":
        positive_rate = returns.gt(0).rolling(lookback, min_periods=max(5, lookback // 2)).mean()
        ret = close.pct_change(lookback, fill_method=None)
        return positive_rate * np.sign(ret)
    if spec.formula_type == "vol_compression_breakout":
        fast = int((spec.parameters or {}).get("fast", 20))
        slow = int((spec.parameters or {}).get("slow", lookback))
        fast_vol = returns.rolling(fast, min_periods=max(5, fast // 2)).std()
        slow_vol = returns.rolling(slow, min_periods=max(10, slow // 2)).std()
        return -(fast_vol / slow_vol.replace(0.0, np.nan) - 1.0)
    if spec.formula_type == "downside_vol_asymmetry":
        downside = returns.where(returns < 0).rolling(lookback, min_periods=max(5, lookback // 2)).std()
        total = returns.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return -(downside / total.replace(0.0, np.nan))
    if spec.formula_type == "index_relative_reversal":
        stock_ret = close.pct_change(lookback, fill_method=None)
        universe_ret = stock_ret.mean(axis=1, skipna=True)
        return -(stock_ret.sub(universe_ret, axis=0))
    if spec.formula_type == "smooth_trend_persistence":
        ret = close.pct_change(lookback, fill_method=None)
        path_length = returns.abs().rolling(lookback, min_periods=max(10, lookback // 2)).sum()
        return ret / path_length.replace(0.0, np.nan)
    if spec.formula_type == "trend_consistency_20_60":
        return_window = int((spec.parameters or {}).get("return_window", 5))
        consistency_window = int((spec.parameters or {}).get("consistency_window", lookback))
        rolling_ret = close.pct_change(return_window, fill_method=None)
        positive_rate = rolling_ret.gt(0).rolling(
            consistency_window,
            min_periods=max(10, consistency_window // 2),
        ).mean()
        trend_ret = close.pct_change(lookback, fill_method=None)
        return (positive_rate - 0.5) * np.sign(trend_ret)
    if spec.formula_type == "trend_consistency_20_60_persistent":
        return_window = int((spec.parameters or {}).get("return_window", 5))
        consistency_window = int((spec.parameters or {}).get("consistency_window", lookback))
        confirmation_window = int((spec.parameters or {}).get("confirmation_window", 3))
        rolling_ret = close.pct_change(return_window, fill_method=None)
        positive_rate = rolling_ret.gt(0).rolling(
            consistency_window,
            min_periods=max(10, consistency_window // 2),
        ).mean()
        trend_ret = close.pct_change(lookback, fill_method=None)
        startup_trend_ret = close.pct_change(20, fill_method=None)
        trend_direction = np.sign(trend_ret).where(trend_ret.notna(), np.sign(startup_trend_ret))
        base = (positive_rate - 0.5) * trend_direction
        recent_direction = rolling_ret.gt(0).rolling(
            confirmation_window,
            min_periods=1,
        ).mean()
        confirmed_positive = (trend_ret > 0) & recent_direction.ge(0.5)
        confirmed_negative = (trend_ret < 0) & recent_direction.le(0.5)
        confirmation = (confirmed_positive | confirmed_negative).astype(float)
        return base * (0.5 + 0.5 * confirmation)
    if spec.formula_type == "index_relative_reversal_vol_adj":
        reversal_window = int((spec.parameters or {}).get("reversal_window", lookback))
        vol_window = int((spec.parameters or {}).get("vol_window", 20))
        stock_ret = close.pct_change(reversal_window, fill_method=None)
        universe_ret = stock_ret.mean(axis=1, skipna=True)
        residual_reversal = -(stock_ret.sub(universe_ret, axis=0))
        realized_vol = returns.rolling(vol_window, min_periods=max(5, vol_window // 2)).std()
        fallback_vol = returns.abs().rolling(reversal_window, min_periods=1).mean()
        denominator = realized_vol.fillna(fallback_vol).replace(0.0, np.nan)
        adjusted = residual_reversal / denominator
        return adjusted.where(np.isfinite(adjusted), residual_reversal)
    if spec.formula_type == "index_relative_reversal_confirmed":
        reversal_window = int((spec.parameters or {}).get("reversal_window", lookback))
        confirmation_window = int((spec.parameters or {}).get("confirmation_window", 1))
        stock_ret = close.pct_change(reversal_window, fill_method=None)
        universe_ret = stock_ret.mean(axis=1, skipna=True)
        residual_reversal = -(stock_ret.sub(universe_ret, axis=0))
        recent_stock_ret = close.pct_change(confirmation_window, fill_method=None)
        recent_universe_ret = recent_stock_ret.mean(axis=1, skipna=True)
        recent_residual = recent_stock_ret.sub(recent_universe_ret, axis=0)
        stabilization = recent_residual.ge(0).astype(float)
        return residual_reversal * (0.5 + 0.5 * stabilization)
    if spec.formula_type == "percentile_rank_stability":
        ret = close.pct_change(lookback, fill_method=None)
        rank = ret.rank(axis=1, pct=True, method="average", na_option="keep")
        rank_stability_penalty = rank.rolling(lookback, min_periods=max(5, lookback // 2)).std()
        return rank - rank_stability_penalty
    if spec.formula_type == "volume_flow_ratio":
        fast = int((spec.parameters or {}).get("fast", 5))
        slow = int((spec.parameters or {}).get("slow", lookback))
        dollar_volume = close * volume
        fast_flow = dollar_volume.rolling(fast, min_periods=max(2, fast // 2)).mean()
        slow_flow = dollar_volume.rolling(slow, min_periods=max(5, slow // 2)).mean()
        return fast_flow / slow_flow.replace(0.0, np.nan) - 1.0
    raise ValueError(f"Unknown expanded discovery formula_type: {spec.formula_type}")


def build_expanded_discovery_candidates(
    ohlcv: dict[str, pd.DataFrame],
    run_id: str,
    created_timestamp: str,
    discovery_version: str = EXPANDED_DISCOVERY_VERSION,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    signals = {spec.signal_name: cross_sectional_zscore(_raw_signal_panel(spec, ohlcv)) for spec in EXPANDED_SIGNAL_SPECS}
    metadata_rows = []
    for spec in EXPANDED_SIGNAL_SPECS:
        metadata_rows.append(
            {
                "signal_name": spec.signal_name,
                "signal_family": spec.signal_family,
                "formula_type": spec.formula_type,
                "lookback": spec.lookback,
                "direction_convention": spec.direction_convention,
                "data_dependencies": ",".join(spec.data_dependencies),
                "parameters": json.dumps(spec.parameters or {}, sort_keys=True),
                "signal_source": EXPANDED_DISCOVERY_SOURCE,
                "discovery_version": discovery_version,
                "intended_alpha_sleeve": spec.intended_alpha_sleeve,
                "normalization": "cross_sectional_zscore_by_date_clipped_-3_3",
                "notes": "Expanded discovery candidate; trailing-only rolling inputs, no future data.",
                "description": spec.description,
                "expected_direction": spec.expected_direction or spec.direction_convention,
                "economic_intuition": spec.economic_intuition,
                "required_inputs": ",".join(spec.required_inputs or spec.data_dependencies),
                "known_risks": spec.known_risks,
                "expansion_batch": spec.expansion_batch,
                "refinement_source": spec.refinement_source,
                "targeted_failure_mode": spec.targeted_failure_mode,
                "expected_improvement": spec.expected_improvement,
                "run_id": run_id,
                "created_timestamp": created_timestamp,
            }
        )
    return signals, pd.DataFrame(metadata_rows)


def _daily_rank_ic(signal_panel: pd.DataFrame, forward_return: pd.DataFrame) -> pd.Series:
    aligned_signal, aligned_return = signal_panel.align(forward_return, join="inner", axis=0)
    aligned_signal, aligned_return = aligned_signal.align(aligned_return, join="inner", axis=1)
    values = {}
    for date in aligned_signal.index:
        pair = pd.DataFrame({"signal": aligned_signal.loc[date], "fwd": aligned_return.loc[date]}).apply(
            pd.to_numeric,
            errors="coerce",
        )
        pair = pair[np.isfinite(pair["signal"]) & np.isfinite(pair["fwd"])].dropna()
        values[date] = pair["signal"].corr(pair["fwd"], method="spearman") if len(pair) >= 5 else np.nan
    return pd.Series(values, name="daily_ic")


def _smooth_for_turnover(
    signal_panel: pd.DataFrame,
    smoothing_window: int = 10,
    rebalance_frequency: int = 5,
    update_rate: float = 0.10,
) -> pd.DataFrame:
    smoothed = signal_panel.rolling(smoothing_window, min_periods=1).mean()
    output = pd.DataFrame(np.nan, index=smoothed.index, columns=smoothed.columns, dtype=float)
    previous = pd.Series(np.nan, index=smoothed.columns, dtype=float)
    for position, date in enumerate(smoothed.index):
        if position % rebalance_frequency == 0:
            target = smoothed.loc[date]
            if previous.notna().any():
                updated = previous.copy()
                existing = previous.notna() & target.notna()
                updated.loc[existing] = previous.loc[existing] + update_rate * (target.loc[existing] - previous.loc[existing])
                newly_valid = previous.isna() & target.notna()
                updated.loc[newly_valid] = target.loc[newly_valid]
                previous = updated
            else:
                previous = target
        output.loc[date] = previous
    return output.apply(pd.to_numeric, errors="coerce")


def _turnover_proxy(signal_panel: pd.DataFrame) -> float:
    ranks = _smooth_for_turnover(signal_panel).rank(axis=1, pct=True) - 0.5
    turnover = ranks.diff().abs().sum(axis=1, min_count=1) / 2.0
    return float(turnover.dropna().mean()) if not turnover.dropna().empty else np.nan


def build_expanded_discovery_quality(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    close_prices: pd.DataFrame,
    run_id: str,
    discovery_version: str = EXPANDED_DISCOVERY_VERSION,
    horizons: list[int] | None = None,
    eligible_mask: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if horizons is None:
        horizons = DISCOVERY_HORIZONS
    family_lookup = metadata.set_index("signal_name")["signal_family"].to_dict()
    rows = []
    forward_returns = {h: close_prices.shift(-h) / close_prices - 1.0 for h in horizons}
    for signal_name, panel in signals.items():
        numeric = panel.apply(pd.to_numeric, errors="coerce")
        finite = np.isfinite(numeric.to_numpy(dtype=float))
        if eligible_mask is not None:
            aligned_mask = eligible_mask.reindex(index=numeric.index, columns=numeric.columns, fill_value=False).astype(bool)
            denominator_mask = aligned_mask.to_numpy(dtype=bool)
        else:
            denominator_mask = np.ones_like(finite, dtype=bool)
        total_cells = int(denominator_mask.sum())
        finite_eligible = finite & denominator_mask
        valid_dates = pd.Series(finite.any(axis=1), index=numeric.index)
        horizon_metrics = []
        window_metrics = []
        for horizon, fwd in forward_returns.items():
            daily_ic = _daily_rank_ic(numeric, fwd).dropna()
            mean_ic = float(daily_ic.mean()) if not daily_ic.empty else np.nan
            ic_std = float(daily_ic.std(ddof=1)) if len(daily_ic) > 1 else np.nan
            ic_ir = mean_ic / ic_std if pd.notna(ic_std) and ic_std != 0 else np.nan
            positive_ic_rate = float(daily_ic.gt(0).mean()) if not daily_ic.empty else np.nan
            if not daily_ic.empty:
                chunks = np.array_split(daily_ic.sort_index(), 4)
                window_means = [chunk.mean() for chunk in chunks if not chunk.empty]
                persistence = float(np.mean([value > 0 for value in window_means])) if window_means else np.nan
            else:
                persistence = np.nan
            horizon_metrics.append((horizon, mean_ic, ic_ir, positive_ic_rate, persistence))
            window_metrics.extend(
                {
                    "horizon": horizon,
                    "window_index": idx + 1,
                    "window_mean_ic": float(chunk.mean()) if not chunk.empty else np.nan,
                }
                for idx, chunk in enumerate(np.array_split(daily_ic.sort_index(), 4))
            )
        best = max(
            horizon_metrics,
            key=lambda item: (-np.inf if pd.isna(item[1]) else item[1], -np.inf if pd.isna(item[2]) else item[2]),
        )
        rows.append(
            {
                "signal_name": signal_name,
                "signal_family": family_lookup.get(signal_name),
                "n_dates": int(numeric.shape[0]),
                "n_tickers": int(numeric.shape[1]),
                "missing_pct": float(1.0 - finite_eligible.sum() / total_cells) if total_cells else np.nan,
                "finite_pct": float(finite_eligible.sum() / total_cells) if total_cells else np.nan,
                "first_valid_date": numeric.index[valid_dates].min() if valid_dates.any() else pd.NaT,
                "last_valid_date": numeric.index[valid_dates].max() if valid_dates.any() else pd.NaT,
                "best_horizon": int(best[0]),
                "mean_ic": best[1],
                "ic_ir": best[2],
                "positive_ic_rate": best[3],
                "persistence_proxy": best[4],
                "turnover_proxy": _turnover_proxy(numeric),
                "window_metrics_json": json.dumps(window_metrics, sort_keys=True),
                "run_id": run_id,
                "discovery_version": discovery_version,
            }
        )
    quality = pd.DataFrame(rows)
    quality["structural_quality_pass"] = quality["finite_pct"].ge(0.90) & quality["missing_pct"].le(0.20)
    return quality


def build_expanded_discovery_core_corr(
    signals: dict[str, pd.DataFrame],
    core_alpha_panel: pd.DataFrame,
    run_id: str,
    discovery_version: str = EXPANDED_DISCOVERY_VERSION,
    core_alpha_name: str = CORE_ALPHA_NAME,
) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        aligned_signal, aligned_core = panel.align(core_alpha_panel, join="inner", axis=0)
        aligned_signal, aligned_core = aligned_signal.align(aligned_core, join="inner", axis=1)
        pair = pd.DataFrame(
            {
                "signal_value": aligned_signal.to_numpy(dtype=float).ravel(),
                "core_alpha_value": aligned_core.to_numpy(dtype=float).ravel(),
            }
        ).dropna()
        correlation = pair["signal_value"].corr(pair["core_alpha_value"]) if len(pair) >= 2 else np.nan
        abs_corr = abs(correlation) if pd.notna(correlation) else np.nan
        if pd.isna(abs_corr):
            corr_flag = "UNKNOWN_CORR"
        elif abs_corr <= 0.40:
            corr_flag = "LOW_CORR"
        elif abs_corr <= 0.70:
            corr_flag = "MID_CORR"
        else:
            corr_flag = "HIGH_CORR"
        rows.append(
            {
                "signal_name": signal_name,
                "core_alpha_name": core_alpha_name,
                "correlation_to_core": correlation,
                "abs_corr_to_core": abs_corr,
                "core_corr_flag": corr_flag,
                "n_overlap": int(len(pair)),
                "run_id": run_id,
                "discovery_version": discovery_version,
            }
        )
    return pd.DataFrame(rows)


def build_expanded_discovery_selection(
    quality: pd.DataFrame,
    core_corr: pd.DataFrame,
    metadata: pd.DataFrame,
    run_id: str,
    discovery_version: str = EXPANDED_DISCOVERY_VERSION,
) -> pd.DataFrame:
    selected = quality.merge(core_corr, on=["signal_name", "run_id", "discovery_version"], how="left").merge(
        metadata[["signal_name", "signal_family", "formula_type", "intended_alpha_sleeve"]],
        on="signal_name",
        how="left",
        suffixes=("", "_metadata"),
    )
    selected["selection_score"] = (
        selected["mean_ic"].clip(lower=0).fillna(0) * 100.0
        + selected["ic_ir"].clip(lower=0).fillna(0) * 10.0
        + selected["persistence_proxy"].fillna(0) * 5.0
        + (1.0 - selected["abs_corr_to_core"].clip(upper=1).fillna(1.0)) * 5.0
        - selected["turnover_proxy"].fillna(10.0)
    )
    selected["selection_status"] = np.where(
        selected["structural_quality_pass"].fillna(False)
        & selected["abs_corr_to_core"].le(0.40)
        & selected["mean_ic"].ge(0.008)
        & selected["ic_ir"].ge(0.04)
        & selected["persistence_proxy"].ge(0.50)
        & selected["turnover_proxy"].le(2.50),
        "PROMOTE_EXPANDED_DISCOVERY",
        "REVIEW_OR_REJECT_EXPANDED_DISCOVERY",
    )
    selected["selection_reason"] = np.where(
        selected["selection_status"].eq("PROMOTE_EXPANDED_DISCOVERY"),
        "Passes structural, low-correlation, IC, persistence, and turnover discovery gates.",
        "Does not pass one or more discovery preference gates.",
    )
    return selected.sort_values(["selection_status", "selection_score"], ascending=[True, False]).reset_index(drop=True)


__all__ = [
    "CORE_ALPHA_NAME",
    "DISCOVERY_HORIZONS",
    "EXPANSION_BATCH_V2_VERSION",
    "EXPANSION_BATCH_VERSION",
    "EXPANDED_DISCOVERY_SOURCE",
    "EXPANDED_DISCOVERY_VERSION",
    "EXPANDED_SIGNAL_SPECS",
    "build_expanded_discovery_candidates",
    "build_expanded_discovery_core_corr",
    "build_expanded_discovery_quality",
    "build_expanded_discovery_selection",
]
