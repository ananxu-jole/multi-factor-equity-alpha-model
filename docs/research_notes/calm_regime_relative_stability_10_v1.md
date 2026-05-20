# Calm Regime Relative Stability 10 v1

## Executive Takeaway

This research-only run tested one simple formulation of `calm_regime_relative_stability_10` under the isolated run namespace `calm_regime_relative_stability_10_v1`.

The formulation was designed to test whether stocks with cleaner cross-sectional relative stability during calm, non-hostile regimes exhibit stronger h10 behavior without becoming low-volatility beta, momentum, reversal, breakout continuation, or hostile-state repair.

Final classification: `CONDITIONAL_REFINEMENT_CANDIDATE`
Primary review issues: `best_horizon_not_h10; sparse_activation`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v3 concepts was performed.

## Source Context

- Expansion v3 design screen: `docs/research_notes/track_b_expansion_v3_design_screening.md`
- Prior v3 isolated test: `docs/research_notes/neutral_accumulation_without_breakout_v1.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | In calm regimes, stable relative ordering and low cross-sectional rank churn may carry information because stock-specific quality can be expressed without stress-driven noise. |
| Calm-regime logic | Activate only when the market is non-hostile, recent stress is absent, benchmark volatility is low-to-normal, dispersion is normal, and breadth is balanced rather than weak or euphoric. |
| Relative stability definition | Combine low residual rank churn, stable residual volatility ratio, orderly range behavior, path orderliness, and neutral price extension. |
| Non-hostile regime filter | Exclude recent volatility spike, panic/liquidity stress, drawdown acceleration, hostile trend, and weak breadth. |
| Difference from low-volatility factors | Low volatility is only a baseline and one component-adjacent risk; the candidate requires relative rank stability and is checked directly against low-volatility references. |
| Difference from momentum/reversal | Short, medium, and longer price-rank exposures are neutralized; the mechanism is stability, not direction of prior return. |
| Difference from current inventory | It tests orderly calm-state behavior rather than hostile trend, weak breadth, drawdown, panic/liquidity stress, or post-stress stabilization. |
| Expected activation semantics | Calm non-hostile regime with high relative stability. |
| Expected horizon | h10 primary; h5 and h20 diagnostic. |
| Expected turnover | Low after fixed 10-day rebalance control. |
| Expected active coverage | Medium to medium-high. |

## Candidate Registry

| signal_name                       | family                         | run_id                               | research_status                    | mechanism_thesis                                                                                         | state_transition_logic                                                                                                        | differs_from_inventory                                            | differs_from_reversal_momentum                                                            | expected_activation_state                | expected_horizon               | expected_turnover_profile   | expected_active_coverage   |
|:----------------------------------|:-------------------------------|:-------------------------------------|:-----------------------------------|:---------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|:------------------------------------------------------------------------------------------|:-----------------------------------------|:-------------------------------|:----------------------------|:---------------------------|
| calm_regime_relative_stability_10 | calm_regime_relative_stability | calm_regime_relative_stability_10_v1 | TRACK_B_EXPANSION_V3_RESEARCH_ONLY | Calm-regime relative stability without low-volatility, momentum, reversal, or hostile-repair dependence. | Non-hostile calm regime plus low relative rank churn, residual-vol stability, range orderliness, and neutral price extension. | Targets calm orderly states instead of hostile/stress h20 repair. | Neutralizes return-rank exposures and tests stability rather than prior-return direction. | CALM_REGIME_WITH_HIGH_RELATIVE_STABILITY | h10 primary; h5/h20 diagnostic | low                         | medium_to_medium_high      |

## Component Diagnostics

| component               |   finite_pct |   mean_abs |
|:------------------------|-------------:|-----------:|
| relative_rank_stability |     0.973086 |  0.276782  |
| residual_vol_stability  |     0.977943 |  0.499126  |
| range_orderliness       |     0.982475 |  0.499149  |
| path_orderliness        |     0.985002 |  0.497504  |
| neutral_extension       |     0.978801 |  0.284436  |
| calm_gate               |     1        |  0.121544  |
| relative_stability      |     0.971151 |  0.0147891 |
| final_signal            |     0.959665 |  0.0703348 |

## Structural Quality

| signal_name                       |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:----------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| calm_regime_relative_stability_10 |     0.0403353 |     0.959665 |        0.971401 |        0.0106398 |              0 |             0.13346 |                       30 |               0.985281 |

## Multi-Horizon IC

| signal_name                       |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:----------------------------------|----------:|-----------:|--------------:|----------:|-------------------:|----------:|:------------------|
| calm_regime_relative_stability_10 |         1 | 0.0019978  |    0.0019978  | 0.0175402 |           0.525    |       280 | False             |
| calm_regime_relative_stability_10 |         5 | 0.00162324 |    0.00162324 | 0.0148289 |           0.514286 |       280 | False             |
| calm_regime_relative_stability_10 |        10 | 0.0135587  |    0.0135587  | 0.135665  |           0.546429 |       280 | False             |
| calm_regime_relative_stability_10 |        20 | 0.0220788  |    0.0220788  | 0.228774  |           0.603571 |       280 | True              |

## h5 / h10 / h20 Behavior

| signal_name                       |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates |
|:----------------------------------|----------:|-----------:|--------------:|----------:|-------------------:|----------:|
| calm_regime_relative_stability_10 |         5 | 0.00162324 |    0.00162324 | 0.0148289 |           0.514286 |       280 |
| calm_regime_relative_stability_10 |        10 | 0.0135587  |    0.0135587  | 0.135665  |           0.546429 |       280 |
| calm_regime_relative_stability_10 |        20 | 0.0220788  |    0.0220788  | 0.228774  |           0.603571 |       280 |

## WFV-Style Diagnostics

| signal_name                       |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:----------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| calm_regime_relative_stability_10 |        20 |           4 |                0.0220788 |               0.598608 |          0.75 |               0.75 |               0.585449 |

## WFV Window Detail

| signal_name                       |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:----------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| calm_regime_relative_stability_10 |        20 |        1 | 2018-06-25   | 2019-08-05 |      0.0790201 |     1.01138  |           0.8      |               70 |
| calm_regime_relative_stability_10 |        20 |        2 | 2019-10-30   | 2020-09-14 |      0.0222647 |     0.263747 |           0.628571 |               70 |
| calm_regime_relative_stability_10 |        20 |        3 | 2021-01-08   | 2024-03-28 |     -0.0233292 |    -0.202169 |           0.428571 |               70 |
| calm_regime_relative_stability_10 |        20 |        4 | 2024-04-01   | 2025-10-31 |      0.0103594 |     0.142731 |           0.557143 |               70 |

## Baseline And Inventory Similarity

| signal_name                       | top_comparison                    |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_10_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   simple_rank_stability_10_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   simple_range_stability_corr |   raw_calm_stability_composite_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |
|:----------------------------------|:----------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|------------------------------:|------------------------------:|------------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|------------------------------:|------------------------------------:|--------------------------:|--------------------------:|----------------------------:|
| calm_regime_relative_stability_10 | simple_low_residual_volatility_20 |                0.247124 |                  0.0322375 |              2.70713e-08 |                 1.89723e-08 |            0.0322375 |          0.00271683 |          0.00107615 |                    0.00167465 |                    0.00271682 |                    0.00107615 |                       0.0854175 |                        0.237147 |                                 0.247124 |                      0.057277 |                          0.00668669 |                0.00271682 |                  0.247124 |                   0.0854175 |

## Calm / Neutral Vs Hostile / Stress Attribution

| signal_name                       |   horizon | state                             |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:----------------------------------|----------:|:----------------------------------|----------:|------------:|-----------:|-------------------:|
| calm_regime_relative_stability_10 |        20 | recovery_phase                    |         1 |  0.276599   | nan        |           1        |
| calm_regime_relative_stability_10 |        20 | NORMAL_DISPERSION                 |       211 |  0.0271578  |   0.271727 |           0.635071 |
| calm_regime_relative_stability_10 |        20 | CALM_NORMAL_VOL                   |       203 |  0.0269102  |   0.274776 |           0.605911 |
| calm_regime_relative_stability_10 |        20 | CALM_REGIME                       |       167 |  0.0253489  |   0.255545 |           0.616766 |
| calm_regime_relative_stability_10 |        20 | CALM_WITH_HIGH_RELATIVE_STABILITY |       167 |  0.0253489  |   0.255545 |           0.616766 |
| calm_regime_relative_stability_10 |        20 | NON_HOSTILE_REGIME                |       247 |  0.0238036  |   0.238575 |           0.59919  |
| calm_regime_relative_stability_10 |        20 | BALANCED_BREADTH                  |       223 |  0.0229309  |   0.224933 |           0.596413 |
| calm_regime_relative_stability_10 |        20 | weak_breadth                      |        24 |  0.0149822  |   0.211943 |           0.625    |
| calm_regime_relative_stability_10 |        20 | ORDERLY_CROSS_SECTION             |       142 |  0.0114254  |   0.110064 |           0.570423 |
| calm_regime_relative_stability_10 |        20 | HOSTILE_OR_STRESS                 |        33 |  0.00916847 |   0.139355 |           0.636364 |
| calm_regime_relative_stability_10 |        20 | drawdown_acceleration             |        14 | -0.0143459  |  -0.180066 |           0.428571 |
| calm_regime_relative_stability_10 |        20 | high_dispersion_rotation          |        13 | -0.0148396  |  -0.154343 |           0.384615 |

## Stress / Regime Attribution

| signal_name                       |   horizon | state                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:----------------------------------|----------:|:-------------------------|----------:|------------:|-----------:|-------------------:|
| calm_regime_relative_stability_10 |        20 | recovery_phase           |         1 |   0.276599  | nan        |           1        |
| calm_regime_relative_stability_10 |        20 | weak_breadth             |        24 |   0.0149822 |   0.211943 |           0.625    |
| calm_regime_relative_stability_10 |        20 | drawdown_acceleration    |        14 |  -0.0143459 |  -0.180066 |           0.428571 |
| calm_regime_relative_stability_10 |        20 | high_dispersion_rotation |        13 |  -0.0148396 |  -0.154343 |           0.384615 |
| calm_regime_relative_stability_10 |        20 | trend_transition         |        11 |  -0.0393966 |  -0.412075 |           0.363636 |
| calm_regime_relative_stability_10 |        20 | volatility_spike         |         0 | nan         | nan        |         nan        |
| calm_regime_relative_stability_10 |        20 | panic_liquidity_stress   |         0 | nan         | nan        |         nan        |

## Sample-Size Sanity

| state                             |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:----------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| CALM_REGIME                       |           255 |          0.121544  |                           167 |                   0.0795996   |
| NON_HOSTILE_REGIME                |           834 |          0.397521  |                           247 |                   0.117731    |
| CALM_NORMAL_VOL                   |           488 |          0.232602  |                           203 |                   0.0967588   |
| NORMAL_DISPERSION                 |           467 |          0.222593  |                           211 |                   0.100572    |
| ORDERLY_CROSS_SECTION             |           460 |          0.219256  |                           142 |                   0.0676835   |
| BALANCED_BREADTH                  |           632 |          0.301239  |                           223 |                   0.106292    |
| CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           167 |                   0.0795996   |
| HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            33 |                   0.0157293   |
| drawdown_acceleration             |           375 |          0.178742  |                            14 |                   0.00667302  |
| volatility_spike                  |           404 |          0.192564  |                             0 |                   0           |
| panic_liquidity_stress            |           187 |          0.0891325 |                             0 |                   0           |
| trend_transition                  |           580 |          0.276454  |                            11 |                   0.00524309  |
| recovery_phase                    |           196 |          0.0934223 |                             1 |                   0.000476644 |
| high_dispersion_rotation          |           584 |          0.27836   |                            13 |                   0.00619638  |
| weak_breadth                      |           508 |          0.242135  |                            24 |                   0.0114395   |
| SIGNAL_ACTIVE                     |           280 |          0.13346   |                           280 |                   0.13346     |

## Candidate Decision

| signal_name                       | family                         |   best_horizon |   mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |    ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |   simple_rank_stability_10_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   raw_calm_stability_composite_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   positive_calm_state_count |   best_regime_ic |   best_calm_state_ic |   best_hostile_state_ic | status                           | review_issues                           |
|:----------------------------------|:-------------------------------|---------------:|----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|---------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|----------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|----------------------------:|-----------------:|---------------------:|------------------------:|:---------------------------------|:----------------------------------------|
| calm_regime_relative_stability_10 | calm_regime_relative_stability |             20 | 0.0220788 |   0.00162324 |              0.514286 |     0.0135587 |               0.546429 |     0.0220788 |               0.603571 | 0.228774 |           0.603571 |        0.0106398 |     0.0403353 |             0.13346 |                0.247124 |            0.0322375 |          0.00271683 |          0.00107615 |                0.00271682 |                  0.247124 |                   0.0854175 |                       0.0854175 |                        0.237147 |                                 0.247124 |                          0.00668669 |                  0.0322375 |              2.70713e-08 |                 1.89723e-08 |              0.75 |                   0.75 |               0.598608 |                       2 |                           5 |         0.276599 |            0.0271578 |               0.0149822 | CONDITIONAL_REFINEMENT_CANDIDATE | best_horizon_not_h10; sparse_activation |

## Specific Diagnostic Answers

- Genuinely calm-regime relative stability: assessed through calm-state attribution; positive calm-state count was `5` and best calm-state IC was `0.027158`.
- Low-volatility beta risk: max low-volatility correlation was `0.247124`; low-vol and residual-low-vol correlations were `0.237147` / `0.247124`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.002717` / `0.002717`.
- Simple stability duplication risk: max simple-stability correlation was `0.085418`.
- Inventory overlap risk: inventory liquidity/breadth/volatility correlations were `0.032237` / `0.000000` / `0.000000`.
- Sparse or broad activation risk: active date ratio was `0.133460`.
- Turnover risk: turnover proxy was `0.010640`.
- Directional stability: WFV-style persistence/sign consistency were `0.75` / `0.75`.
- h10 profile: h10 mean IC was `0.013559` with positive IC rate `0.546429`.

## Recommended Next Step

`calm_regime_relative_stability_10` should receive a narrow refinement diagnostics pass focused on h10 stability, calm-state support, and low-volatility separation.
