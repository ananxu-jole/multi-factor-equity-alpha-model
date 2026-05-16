# Batch 3 Conditional Signal Research

- Run ID: `conditional_signal_diagnostics_20260515_081608`
- Diagnostics version: `batch3_conditional_signal_diagnostics_v1`
- Run timestamp: `2026-05-15 08:16:08`
- Scope: research artifacts only. No gates, formulas, WFV logic, schemas, or 04A+ stages were changed.

## Objective

Batch 3 investigates whether recent Batch 1/2 failures are better understood as conditional edges rather than universal signals. The goal is to identify market states where the focus signals have stronger sign consistency, persistence, and effective IC without relaxing any platform gate.

## Focus Signals

- `trend_consistency_20_60`
- `trend_consistency_20_60_persistent`
- `index_relative_reversal_5`
- `percentile_rank_stability_20`
- `smooth_trend_persistence_60`

## Conditional Contexts

All contexts are OHLCV-only and derived from current clean close prices. Existing benchmark trend, volatility, drawdown, and correlation regimes are reused; additional research-only labels cover cross-sectional dispersion, breadth, participation, and a simple risk-on/risk-off proxy.

Important caveat: these are in-sample conditional diagnostics. Strong conditional IC is a hypothesis for a controlled Batch 3 experiment, not evidence of deployability or a reason to relax WFV.

## Classification Rules

- `INSUFFICIENT_SAMPLE`: fewer than 126 daily IC observations in the condition.
- `DIRECTION_FLIP_RISK`: condition has negative effective mean IC or materially poor sign consistency.
- `PROMISING_CONDITIONAL_EDGE`: positive effective IC, sign consistency, and window persistence all clear conservative research thresholds.
- `WEAK_CONDITIONAL_EDGE`: positive but less convincing conditional behavior.
- `AVOID`: enough sample but insufficient robustness.

These labels are diagnostic only and are not platform gates.

## Top Promising Conditional Edges

| signal_name                  |   horizon | context_column         | context_value     |   n_days |   effective_mean_ic |   sign_consistency |   window_persistence |   degradation_vs_unconditional_ic |
|:-----------------------------|----------:|:-----------------------|:------------------|---------:|--------------------:|-------------------:|---------------------:|----------------------------------:|
| smooth_trend_persistence_60  |        20 | benchmark_trend_regime | DOWNTREND         |      281 |           0.148629  |           0.740214 |                 1    |                         0.133707  |
| smooth_trend_persistence_60  |        20 | drawdown_regime        | HIGH_DRAWDOWN     |      388 |           0.123665  |           0.71134  |                 1    |                         0.108744  |
| smooth_trend_persistence_60  |        10 | benchmark_trend_regime | DOWNTREND         |      281 |           0.10862   |           0.654804 |                 1    |                         0.094973  |
| smooth_trend_persistence_60  |        10 | drawdown_regime        | HIGH_DRAWDOWN     |      388 |           0.0896319 |           0.631443 |                 1    |                         0.0759854 |
| percentile_rank_stability_20 |        20 | benchmark_trend_regime | DOWNTREND         |      281 |           0.0834338 |           0.658363 |                 1    |                         0.065934  |
| percentile_rank_stability_20 |        20 | drawdown_regime        | HIGH_DRAWDOWN     |      388 |           0.0805483 |           0.615979 |                 1    |                         0.0630485 |
| smooth_trend_persistence_60  |         5 | benchmark_trend_regime | DOWNTREND         |      281 |           0.0791576 |           0.654804 |                 1    |                         0.0717757 |
| percentile_rank_stability_20 |        20 | correlation_regime     | HIGH_CORR         |      679 |           0.071976  |           0.614138 |                 1    |                         0.0544762 |
| smooth_trend_persistence_60  |        20 | correlation_regime     | HIGH_CORR         |      648 |           0.0702096 |           0.591049 |                 1    |                         0.0552877 |
| smooth_trend_persistence_60  |        20 | benchmark_vol_regime   | HIGH_VOL          |      640 |           0.063653  |           0.578125 |                 0.75 |                         0.0487311 |
| percentile_rank_stability_20 |        20 | participation_regime   | LOW_PARTICIPATION |      656 |           0.057742  |           0.585366 |                 0.75 |                         0.0402421 |
| smooth_trend_persistence_60  |         5 | drawdown_regime        | HIGH_DRAWDOWN     |      388 |           0.0557576 |           0.595361 |                 1    |                         0.0483757 |

## Weak Conditional Edges

| signal_name                  |   horizon | context_column         | context_value     |   n_days |   effective_mean_ic |   sign_consistency |   window_persistence |   degradation_vs_unconditional_ic |
|:-----------------------------|----------:|:-----------------------|:------------------|---------:|--------------------:|-------------------:|---------------------:|----------------------------------:|
| smooth_trend_persistence_60  |        10 | benchmark_vol_regime   | HIGH_VOL          |      650 |           0.0465514 |           0.538462 |                 1    |                         0.0329049 |
| percentile_rank_stability_20 |         5 | benchmark_vol_regime   | HIGH_VOL          |      672 |           0.0365147 |           0.528274 |                 1    |                         0.0269157 |
| trend_consistency_20_60      |        20 | benchmark_trend_regime | DOWNTREND         |      281 |           0.0350402 |           0.576512 |                 0.5  |                         0.0169006 |
| percentile_rank_stability_20 |         5 | correlation_regime     | HIGH_CORR         |      679 |           0.0350238 |           0.539028 |                 0.75 |                         0.0254248 |
| percentile_rank_stability_20 |         5 | drawdown_regime        | HIGH_DRAWDOWN     |      388 |           0.0317774 |           0.530928 |                 0.75 |                         0.0221784 |
| percentile_rank_stability_20 |         5 | risk_regime            | RISK_OFF          |      999 |           0.0309215 |           0.537538 |                 1    |                         0.0213225 |
| index_relative_reversal_5    |         1 | drawdown_regime        | HIGH_DRAWDOWN     |      389 |           0.0263647 |           0.529563 |                 1    |                         0.0164013 |
| percentile_rank_stability_20 |        10 | dispersion_regime      | HIGH_DISPERSION   |      682 |           0.0247516 |           0.526393 |                 1    |                         0.0107693 |
| index_relative_reversal_5    |         1 | dispersion_regime      | HIGH_DISPERSION   |      693 |           0.0247017 |           0.535354 |                 0.75 |                         0.0147383 |
| index_relative_reversal_5    |         1 | benchmark_trend_regime | SIDEWAYS          |      240 |           0.0243474 |           0.533333 |                 0.75 |                         0.014384  |
| index_relative_reversal_5    |         5 | participation_regime   | LOW_PARTICIPATION |      681 |           0.0237346 |           0.522761 |                 0.75 |                         0.0115603 |
| smooth_trend_persistence_60  |         5 | risk_regime            | RISK_OFF          |      976 |           0.0236678 |           0.538934 |                 1    |                         0.0162859 |

## Direction-Flip / Avoid Evidence

| signal_name                  |   horizon | context_column         | context_value   |   n_days |   effective_mean_ic |   sign_consistency |   window_persistence |
|:-----------------------------|----------:|:-----------------------|:----------------|---------:|--------------------:|-------------------:|---------------------:|
| smooth_trend_persistence_60  |        20 | benchmark_trend_regime | SIDEWAYS        |      240 |          -0.0360493 |           0.379167 |                 0.25 |
| smooth_trend_persistence_60  |        20 | benchmark_vol_regime   | LOW_VOL         |      689 |          -0.0312645 |           0.41074  |                 0.25 |
| smooth_trend_persistence_60  |        20 | risk_regime            | RISK_ON         |      977 |          -0.0246009 |           0.409417 |                 0.25 |
| smooth_trend_persistence_60  |        10 | benchmark_vol_regime   | LOW_VOL         |      689 |          -0.0226233 |           0.455733 |                 0.25 |
| smooth_trend_persistence_60  |        10 | benchmark_trend_regime | SIDEWAYS        |      240 |          -0.0210656 |           0.441667 |                 0    |
| smooth_trend_persistence_60  |        20 | correlation_regime     | LOW_CORR        |      674 |          -0.0203376 |           0.439169 |                 0.25 |
| percentile_rank_stability_20 |        10 | benchmark_vol_regime   | LOW_VOL         |      689 |          -0.019936  |           0.4209   |                 0.25 |
| smooth_trend_persistence_60  |         1 | benchmark_trend_regime | DOWNTREND       |      281 |          -0.0191697 |           0.512456 |                 0    |
| smooth_trend_persistence_60  |        10 | correlation_regime     | LOW_CORR        |      678 |          -0.0186377 |           0.461652 |                 0    |
| smooth_trend_persistence_60  |         5 | benchmark_vol_regime   | LOW_VOL         |      689 |          -0.016269  |           0.468795 |                 0.25 |
| percentile_rank_stability_20 |        20 | benchmark_vol_regime   | LOW_VOL         |      689 |          -0.0155889 |           0.465893 |                 0.5  |
| percentile_rank_stability_20 |        20 | correlation_regime     | LOW_CORR        |      674 |          -0.015106  |           0.470326 |                 0.25 |

## Batch 3 Recommendation

| recommended_variant                                      | source_signal                |   horizon | condition_column       | condition_value   | edge_classification        |   n_days |   effective_mean_ic |   sign_consistency |   window_persistence |
|:---------------------------------------------------------|:-----------------------------|----------:|:-----------------------|:------------------|:---------------------------|---------:|--------------------:|-------------------:|---------------------:|
| smooth_trend_persistence_60__conditioned_on__downtrend   | smooth_trend_persistence_60  |        20 | benchmark_trend_regime | DOWNTREND         | PROMISING_CONDITIONAL_EDGE |      281 |           0.148629  |           0.740214 |                    1 |
| percentile_rank_stability_20__conditioned_on__downtrend  | percentile_rank_stability_20 |        20 | benchmark_trend_regime | DOWNTREND         | PROMISING_CONDITIONAL_EDGE |      281 |           0.0834338 |           0.658363 |                    1 |
| index_relative_reversal_5__conditioned_on__high_drawdown | index_relative_reversal_5    |         5 | drawdown_regime        | HIGH_DRAWDOWN     | PROMISING_CONDITIONAL_EDGE |      389 |           0.0469832 |           0.580977 |                    1 |

Recommended variants should preserve the source signal formula and add only the listed OHLCV-only condition. They should be treated as a small controlled Batch 3 set, not as evidence to relax WFV or admission gates.

## Research Conclusion

The diagnostic pass moves the investigation from broad universal signals toward explicit market-state hypotheses. Conditions that improve effective IC but still show low persistence or sign instability should remain research observations, not implementation candidates.

## Artifacts

- `conditional_ic_by_context.csv`: full signal/regime diagnostics under `/Users/AnyiXu_1/Desktop/multi-factor-equity-alpha-model/artifacts/research/conditional_signal_diagnostics`.
- `signal_context_summary.csv`: per-signal classification counts and best context.
- `context_features.csv`: OHLCV-only market-state labels used in the analysis.
- `batch3_candidate_recommendations.csv`: max-three implementation proposal set.
