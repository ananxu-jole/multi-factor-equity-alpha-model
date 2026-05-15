# Conditional Edge Atlas v1

- Run ID: `conditional_edge_atlas_20260515_112250`
- Atlas version: `conditional_edge_atlas_v1`
- Run timestamp: `2026-05-15 11:22:50`
- Scope: research-only. No official WFV logic, gates, schemas, promotion rules, alpha construction, portfolio logic, or execution logic were changed.

## Objective

The Conditional Edge Atlas maps signal behavior across reusable OHLCV-only market states before further signal-family or universe expansion. It is designed to identify repeated conditional behavior, sparse episodic effects, and states where signals fail or flip direction.

## Market-State Taxonomy

The atlas currently evaluates benchmark trend, benchmark volatility, drawdown depth, cross-sectional dispersion, breadth level, breadth change, volatility expansion/compression, and participation concentration. These states are diagnostic contexts, not trading rules.

## Major Findings

- Total signal-state rows: 3324.
- Robust conditional edges: 5.
- Conditional watchlist edges: 161.
- Sparse conditional edges: 963.
- Conditional strength is often concentrated in stress-like states, but sparse active-window coverage remains a recurring limitation.

## Strongest Conditional States

| context_column                    | context_value      |   n_edges |   mean_effective_ic |
|:----------------------------------|:-------------------|----------:|--------------------:|
| breadth_change_state              | BREADTH_IMPROVING  |        21 |           0.0157063 |
| participation_concentration_state | LOW_CONCENTRATION  |        17 |           0.0220874 |
| breadth_level_state               | HIGH_BREADTH       |        14 |           0.0139037 |
| benchmark_vol_state               | HIGH_VOL           |        12 |           0.0278318 |
| dispersion_state                  | MID_DISPERSION     |        11 |           0.0131577 |
| breadth_level_state               | MID_BREADTH        |         8 |           0.0134632 |
| volatility_change_state           | VOL_COMPRESSION    |         8 |           0.0129403 |
| volatility_change_state           | VOL_STABLE         |         8 |           0.0123035 |
| breadth_level_state               | LOW_BREADTH        |         7 |           0.0301592 |
| drawdown_depth_state              | MODERATE_DRAWDOWN  |         7 |           0.0279167 |
| dispersion_state                  | HIGH_DISPERSION    |         7 |           0.0231759 |
| participation_concentration_state | HIGH_CONCENTRATION |         7 |           0.0139396 |

## Weakest / Failure-Prone States

| context_column                    | context_value         |   failure_count |
|:----------------------------------|:----------------------|----------------:|
| participation_concentration_state | MID_CONCENTRATION     |             124 |
| participation_concentration_state | HIGH_CONCENTRATION    |             121 |
| benchmark_trend_state             | UPTREND               |             116 |
| breadth_change_state              | BREADTH_NEUTRAL       |             116 |
| volatility_change_state           | VOL_COMPRESSION       |             115 |
| dispersion_state                  | HIGH_DISPERSION       |             115 |
| benchmark_vol_state               | MID_VOL               |             113 |
| dispersion_state                  | LOW_DISPERSION        |             112 |
| drawdown_depth_state              | SHALLOW_DRAWDOWN      |             110 |
| breadth_change_state              | BREADTH_DETERIORATING |             110 |
| volatility_change_state           | VOL_STABLE            |             107 |
| benchmark_vol_state               | LOW_VOL               |             106 |

## Top Conditional Edges

| signal_name                             |   horizon | signal_family                  | context_column                    | context_value     |   effective_mean_ic |   effective_ic_ir |   sign_consistency |   active_window_coverage_ratio |   conditional_persistence | robustness_classification   |
|:----------------------------------------|----------:|:-------------------------------|:----------------------------------|:------------------|--------------------:|------------------:|-------------------:|-------------------------------:|--------------------------:|:----------------------------|
| smooth_trend_persistence_60             |        20 | trend_quality                  | participation_concentration_state | LOW_CONCENTRATION |           0.0441558 |          0.202974 |           0.537178 |                           1    |                  0.75     | CONDITIONAL_WATCHLIST       |
| index_relative_reversal_5_high_drawdown |         1 | residual_relative_value        | dispersion_state                  | HIGH_DISPERSION   |           0.0440519 |          0.15666  |           0.536458 |                           1    |                  1        | CONDITIONAL_WATCHLIST       |
| expanded_distance_ma_10                 |        10 | mean_reversion                 | benchmark_vol_state               | HIGH_VOL          |           0.0355841 |          0.156511 |           0.571429 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| range_expansion_failure_5               |        20 | volatility_structure           | drawdown_depth_state              | MODERATE_DRAWDOWN |           0.0344466 |          0.243689 |           0.584762 |                           0.75 |                  0.666667 | CONDITIONAL_WATCHLIST       |
| vol_surprise_20_60                      |        20 | volatility_structure           | drawdown_depth_state              | MODERATE_DRAWDOWN |           0.0341237 |          0.235102 |           0.591463 |                           0.75 |                  0.666667 | CONDITIONAL_WATCHLIST       |
| smooth_trend_persistence_60             |        10 | trend_quality                  | breadth_level_state               | LOW_BREADTH       |           0.0314741 |          0.155966 |           0.54717  |                           1    |                  0.75     | CONDITIONAL_WATCHLIST       |
| range_compression_breakout_10           |        10 | microstructure_lite            | volatility_change_state           | VOL_EXPANSION     |           0.0311751 |          0.183022 |           0.578869 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| index_relative_reversal_5_vol_adj       |        10 | residual_relative_value        | benchmark_vol_state               | HIGH_VOL          |           0.0304374 |          0.133647 |           0.55267  |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| expanded_reversal_5d                    |        10 | mean_reversion                 | benchmark_vol_state               | HIGH_VOL          |           0.0304105 |          0.134211 |           0.568543 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| index_relative_reversal_5               |        10 | residual_relative_value        | benchmark_vol_state               | HIGH_VOL          |           0.0304105 |          0.134211 |           0.568543 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| residual_return_vs_universe_20          |        10 | cross_sectional_relative_value | participation_concentration_state | LOW_CONCENTRATION |           0.0300452 |          0.143445 |           0.568182 |                           1    |                  0.75     | CONDITIONAL_WATCHLIST       |
| expanded_distance_ma_20                 |        10 | mean_reversion                 | participation_concentration_state | LOW_CONCENTRATION |           0.0298721 |          0.135218 |           0.568741 |                           1    |                  0.75     | CONDITIONAL_WATCHLIST       |
| index_relative_reversal_5_confirmed     |        10 | residual_relative_value        | benchmark_vol_state               | HIGH_VOL          |           0.0298253 |          0.133828 |           0.569986 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| price_impact_proxy_20                   |        10 | liquidity_flow                 | benchmark_vol_state               | HIGH_VOL          |           0.0287164 |          0.174452 |           0.56677  |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |
| expanded_reversal_3d                    |        10 | mean_reversion                 | benchmark_vol_state               | HIGH_VOL          |           0.0279999 |          0.12362  |           0.546898 |                           0.5  |                  1        | CONDITIONAL_WATCHLIST       |

## Recurring Regime Patterns

Trend-quality signals tend to concentrate their strongest conditional behavior in downtrend, high-volatility, high-dispersion, or deep-drawdown states. Reversal-style signals more often cluster in stress or dislocation states, but they can still show high decay or direction-flip risk.

## Recurring Failure Modes

The main failure modes are sparse active-window coverage, one-window dominated evidence, direction flips, and high variance. These are research observations, not grounds for relaxing official WFV gates.

## Implications For Batch 4

Batch 4 should prioritize regime-aware hypotheses with enough active-window coverage. Signals that only work in rare states should remain watchlist research until a conditional-alpha framework can evaluate them separately.

## Conditional-Alpha Framework Recommendation

The atlas supports future conditional-alpha research, but it should remain separated from promotion logic. Active-state-aware validation can help design conditional alphas, while official WFV remains the conservative gate for standard signal promotion.

## Artifacts

CSV artifacts are written under `/Users/AnyiXu_1/Desktop/multi-factor-equity-alpha-model/artifacts/research/conditional_edge_atlas`.
