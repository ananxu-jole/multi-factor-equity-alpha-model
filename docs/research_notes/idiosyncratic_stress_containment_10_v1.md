# Idiosyncratic Stress Containment 10 v1

## Executive Takeaway

This research-only run tested one simple formulation of `idiosyncratic_stress_containment_10` under the isolated run namespace `idiosyncratic_stress_containment_10_v1`.

The formulation tests whether assets with stock-specific stress that is being contained can produce a shorter-horizon repair/stabilization edge, especially around h10, without becoming broad drawdown pressure, breadth/participation repair, reversal, or momentum.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `weak_h10_ic; weak_h10_positive_ic_rate; h20_dependency_risk; activation_too_broad`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v5 concepts was performed.

## Source Context

- Expansion v5 design screen: `docs/research_notes/track_b_expansion_v5_design_screening.md`
- Drawdown pressure stabilization v1: `docs/research_notes/drawdown_pressure_stabilization_10_v1.md`
- Conditional Alpha Inventory Monitoring v2: `docs/research_notes/conditional_alpha_inventory_monitoring_v2.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Expansion v4 closeout review: `docs/research_notes/track_b_expansion_v4_closeout_review.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Stock-specific stress containment may identify repair behavior that is not primarily a broad market drawdown or breadth-repair event. |
| Idiosyncratic stress definition | Elevated residual volatility and residual shock magnitude at the asset level relative to each stock's recent residual baseline. |
| Containment/stabilization logic | Residual volatility begins contracting, rank churn declines, range behavior contains, close support improves, and liquidity remains sufficient. |
| Difference from broad drawdown pressure | Activation is stock-level and residual; broad drawdown pressure is included only as an attribution and similarity risk. |
| Difference from active breadth/participation repair | The gate does not require weak breadth or participation recovery and explicitly tracks outside-weak-breadth support. |
| Difference from simple reversal | The signal avoids pure residual losers and neutralizes reversal exposures after scoring. |
| Difference from price momentum | Price-rank momentum and residual momentum exposures are neutralized. |
| Why it may reduce h20 concentration | The mechanism is designed around h10 stock-level containment and uses a 10-day rebalance interval, with h20 treated as diagnostic risk. |
| Expected activation semantics | Asset-level residual stress is present, near-term stress is containing, and market breadth repair is not the required activation driver. |
| Expected horizon | h10 primary; h5 and h15 secondary; h20 diagnostic. |
| Expected turnover | Medium after fixed 10-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparsity or broad activation are review issues. |

## Candidate Registry

| signal_name                         | family                           | run_id                                 | research_status                    | mechanism_thesis                                                           | idiosyncratic_stress_definition                                               | containment_stabilization_logic                                                                           | differs_from_inventory                                                                                                | differs_from_reversal_momentum                                                                   | expected_activation_state       | expected_horizon                              | expected_turnover_profile   | expected_active_coverage   |
|:------------------------------------|:---------------------------------|:---------------------------------------|:-----------------------------------|:---------------------------------------------------------------------------|:------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|:--------------------------------|:----------------------------------------------|:----------------------------|:---------------------------|
| idiosyncratic_stress_containment_10 | idiosyncratic_stress_containment | idiosyncratic_stress_containment_10_v1 | TRACK_B_EXPANSION_V5_RESEARCH_ONLY | Shorter-horizon repair from containment of stock-specific residual stress. | Elevated residual volatility and residual shock magnitude at the asset level. | Residual vol contraction, rank stabilization, range containment, close support, and sufficient liquidity. | Stock-level residual stress gate rather than participation, breadth, liquidity repair, or h20 volatility compression. | Avoids pure residual losers and neutralizes reversal, momentum, and residual momentum exposures. | IDIOSYNCRATIC_STRESS_CONTAINING | h10 primary; h5/h15 secondary; h20 diagnostic | medium                      | medium                     |

## Component Diagnostics

| component                 |   finite_pct |    mean_abs |
|:--------------------------|-------------:|------------:|
| stress_present            |     0.968528 | 0.500801    |
| stress_containment        |     0.981675 | 0.49908     |
| residual_shock_present    |     0.983568 | 0.150027    |
| no_rebound_chase          |     0.985951 | 0.499287    |
| range_containment         |     0.969149 | 0.247826    |
| rank_stabilization        |     0.980712 | 0.498503    |
| close_support             |     0.98702  | 0.501034    |
| liquidity_sufficient      |     0.985161 | 0.501244    |
| idiosyncratic_stress_gate |     1        | 0.0803146   |
| stabilization_quality     |     0.967053 | 0.000505947 |
| final_signal              |     0.959386 | 0.14368     |

## Structural Quality

| signal_name                         |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| idiosyncratic_stress_containment_10 |   2098 |       478 |     0.0406145 |     0.959386 |        0.971401 |               0.959386 |           0 |        0.0181349 |       0.197181 |       0.305965 |              0.751265 |           1530 |            0.729266 |                       56 |               0.987899 |

## Multi-Horizon IC

| signal_name                         |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| idiosyncratic_stress_containment_10 |         1 | 0.0024113  |    0.0024113  | 0.0308484 |   0.0308484 |           0.508497 |      1530 |             20 | False             |
| idiosyncratic_stress_containment_10 |         5 | 0.00539023 |    0.00539023 | 0.0716835 |   0.0716835 |           0.521569 |      1530 |             20 | False             |
| idiosyncratic_stress_containment_10 |        10 | 0.00541512 |    0.00541512 | 0.0743604 |   0.0743604 |           0.510471 |      1528 |             20 | False             |
| idiosyncratic_stress_containment_10 |        15 | 0.00529824 |    0.00529824 | 0.0746149 |   0.0746149 |           0.538411 |      1523 |             20 | False             |
| idiosyncratic_stress_containment_10 |        20 | 0.00904624 |    0.00904624 | 0.126106  |   0.126106  |           0.562582 |      1518 |             20 | True              |

## h5 / h10 / h15 / h20 Behavior

| signal_name                         |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| idiosyncratic_stress_containment_10 |         5 | 0.00539023 |    0.00539023 | 0.0716835 |   0.0716835 |           0.521569 |      1530 |             20 | False             |
| idiosyncratic_stress_containment_10 |        10 | 0.00541512 |    0.00541512 | 0.0743604 |   0.0743604 |           0.510471 |      1528 |             20 | False             |
| idiosyncratic_stress_containment_10 |        15 | 0.00529824 |    0.00529824 | 0.0746149 |   0.0746149 |           0.538411 |      1523 |             20 | False             |
| idiosyncratic_stress_containment_10 |        20 | 0.00904624 |    0.00904624 | 0.126106  |   0.126106  |           0.562582 |      1518 |             20 | True              |

## WFV-Style Diagnostics

| signal_name                         |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| idiosyncratic_stress_containment_10 |        20 |           4 |               0.00905038 |                1.23398 |          0.75 |               0.75 |               0.526715 |

## WFV Window Detail

| signal_name                         |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| idiosyncratic_stress_containment_10 |        20 |        1 | 2018-06-25   | 2020-06-04 |    0.0120223   |   0.160095   |           0.578947 |              380 |
| idiosyncratic_stress_containment_10 |        20 |        2 | 2020-06-19   | 2022-01-04 |   -0.000213596 |  -0.00302117 |           0.536842 |              380 |
| idiosyncratic_stress_containment_10 |        20 |        3 | 2022-01-05   | 2024-01-30 |    0.0192929   |   0.271944   |           0.617414 |              379 |
| idiosyncratic_stress_containment_10 |        20 |        4 | 2024-01-31   | 2026-04-09 |    0.00509996  |   0.0744158  |           0.51715  |              379 |

## Baseline And Inventory Similarity

| signal_name                         | top_comparison             |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   price_rank_reversal_5_corr |   price_rank_reversal_20_corr |   residual_momentum_10_corr |   residual_momentum_20_corr |   drawdown_pressure_proxy_corr |   idiosyncratic_stress_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   max_price_momentum_corr |   max_price_reversal_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_drawdown_pressure_corr |   max_low_volatility_corr |
|:------------------------------------|:---------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-----------------------------:|------------------------------:|----------------------------:|----------------------------:|-------------------------------:|----------------------------------:|-----------------------------------:|--------------------------------------:|--------------------------------:|-----------------------------------------:|--------------------------:|--------------------------:|----------------------------------------:|-----------------------------:|-----------------------------:|--------------------------:|
| idiosyncratic_stress_containment_10 | idiosyncratic_stress_proxy |                0.256437 |                  0.0947071 |                 0.016974 |                    0.036757 |            0.0947071 |            0.135736 |           0.0801594 |                    0.0337709 |                      0.109294 |                      0.152046 |                      0.135736 |                     0.0801594 |                    0.0337709 |                      0.135736 |                    0.109294 |                    0.135736 |                      0.0495174 |                          0.256437 |                           0.126124 |                              0.127422 |                        0.090611 |                                 0.119034 |                  0.152046 |                  0.135736 |                                0.126124 |                     0.127422 |                    0.0495174 |                  0.119034 |

## Idiosyncratic Stress Attribution

| signal_name                         |   horizon | state                                     |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|:------------------------------------|----------:|:------------------------------------------|----------:|-----------:|----------:|-------------------:|
| idiosyncratic_stress_containment_10 |        20 | panic_liquidity_stress                    |        87 | 0.0511415  | 0.644824  |           0.678161 |
| idiosyncratic_stress_containment_10 |        20 | recovery_phase                            |        99 | 0.0390637  | 0.486724  |           0.707071 |
| idiosyncratic_stress_containment_10 |        20 | volatility_spike                          |       204 | 0.0248535  | 0.2703    |           0.598039 |
| idiosyncratic_stress_containment_10 |        20 | drawdown_acceleration                     |       216 | 0.0229581  | 0.302884  |           0.583333 |
| idiosyncratic_stress_containment_10 |        20 | high_dispersion_rotation                  |       253 | 0.0188759  | 0.247467  |           0.624506 |
| idiosyncratic_stress_containment_10 |        20 | trend_transition                          |       352 | 0.0103779  | 0.143242  |           0.5625   |
| idiosyncratic_stress_containment_10 |        20 | IDIOSYNCRATIC_STRESS_OUTSIDE_WEAK_BREADTH |      1145 | 0.00997226 | 0.141352  |           0.567686 |
| idiosyncratic_stress_containment_10 |        20 | IDIOSYNCRATIC_STRESS_ACTIVE               |      1518 | 0.00904624 | 0.126106  |           0.562582 |
| idiosyncratic_stress_containment_10 |        20 | BROAD_HOSTILE_OR_STRESS                   |       831 | 0.00803277 | 0.103212  |           0.558363 |
| idiosyncratic_stress_containment_10 |        20 | ACTIVE_HOSTILE_OR_STRESS                  |       831 | 0.00803277 | 0.103212  |           0.558363 |
| idiosyncratic_stress_containment_10 |        20 | HOSTILE_OR_STRESS                         |       831 | 0.00803277 | 0.103212  |           0.558363 |
| idiosyncratic_stress_containment_10 |        20 | CONTAINED_DISPERSION_IDIOSYNCRATIC        |      1407 | 0.00793875 | 0.112209  |           0.556503 |
| idiosyncratic_stress_containment_10 |        20 | IDIOSYNCRATIC_STRESS_CONTAINING           |      1368 | 0.00789811 | 0.111204  |           0.557018 |
| idiosyncratic_stress_containment_10 |        20 | IDIOSYNCRATIC_STRESS_WITH_QUALITY         |      1368 | 0.00789811 | 0.111204  |           0.557018 |
| idiosyncratic_stress_containment_10 |        20 | weak_breadth                              |       373 | 0.00620361 | 0.0825061 |           0.546917 |

## Stress / Regime Attribution

| signal_name                         |   horizon | state                    |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|:------------------------------------|----------:|:-------------------------|----------:|-----------:|----------:|-------------------:|
| idiosyncratic_stress_containment_10 |        20 | panic_liquidity_stress   |        87 | 0.0511415  | 0.644824  |           0.678161 |
| idiosyncratic_stress_containment_10 |        20 | recovery_phase           |        99 | 0.0390637  | 0.486724  |           0.707071 |
| idiosyncratic_stress_containment_10 |        20 | volatility_spike         |       204 | 0.0248535  | 0.2703    |           0.598039 |
| idiosyncratic_stress_containment_10 |        20 | drawdown_acceleration    |       216 | 0.0229581  | 0.302884  |           0.583333 |
| idiosyncratic_stress_containment_10 |        20 | high_dispersion_rotation |       253 | 0.0188759  | 0.247467  |           0.624506 |
| idiosyncratic_stress_containment_10 |        20 | trend_transition         |       352 | 0.0103779  | 0.143242  |           0.5625   |
| idiosyncratic_stress_containment_10 |        20 | weak_breadth             |       373 | 0.00620361 | 0.0825061 |           0.546917 |

## Sample-Size Sanity

| state                                     |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:------------------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| IDIOSYNCRATIC_STRESS_ACTIVE               |          2093 |          0.997617  |                          1530 |                     0.729266  |
| IDIOSYNCRATIC_STRESS_CONTAINING           |          1541 |          0.734509  |                          1377 |                     0.656339  |
| IDIOSYNCRATIC_STRESS_WITH_QUALITY         |          1541 |          0.734509  |                          1377 |                     0.656339  |
| IDIOSYNCRATIC_STRESS_OUTSIDE_WEAK_BREADTH |          1585 |          0.755481  |                          1157 |                     0.551478  |
| CONTAINED_DISPERSION_IDIOSYNCRATIC        |          1595 |          0.760248  |                          1416 |                     0.674929  |
| BROAD_HOSTILE_OR_STRESS                   |          1264 |          0.602479  |                           843 |                     0.401811  |
| ACTIVE_HOSTILE_OR_STRESS                  |          1264 |          0.602479  |                           843 |                     0.401811  |
| HOSTILE_OR_STRESS                         |          1264 |          0.602479  |                           843 |                     0.401811  |
| drawdown_acceleration                     |           375 |          0.178742  |                           216 |                     0.102955  |
| volatility_spike                          |           404 |          0.192564  |                           215 |                     0.102479  |
| panic_liquidity_stress                    |           187 |          0.0891325 |                            87 |                     0.0414681 |
| trend_transition                          |           580 |          0.276454  |                           364 |                     0.173499  |
| recovery_phase                            |           196 |          0.0934223 |                            99 |                     0.0471878 |
| high_dispersion_rotation                  |           584 |          0.27836   |                           259 |                     0.123451  |
| weak_breadth                              |           508 |          0.242135  |                           373 |                     0.177788  |
| SIGNAL_ACTIVE                             |          1530 |          0.729266  |                          1530 |                     0.729266  |

## Candidate Decision

| signal_name                         | family                           |   best_horizon |    mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |    ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_drawdown_pressure_corr |   max_reversal_corr |   max_price_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   drawdown_pressure_proxy_corr |   idiosyncratic_stress_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_idiosyncratic_state_count |   best_idiosyncratic_state_ic |   best_hostile_stress_state_ic | status                    | review_issues                                                                     |
|:------------------------------------|:---------------------------------|---------------:|-----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|---------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|----------------------------------------:|-----------------------------:|-----------------------------:|--------------------:|--------------------------:|--------------------:|--------------------------:|--------------------------:|-------------------------------:|----------------------------------:|-----------------------------------:|--------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|-------------------------------------:|------------------------------:|-------------------------------:|:--------------------------|:----------------------------------------------------------------------------------|
| idiosyncratic_stress_containment_10 | idiosyncratic_stress_containment |             20 | 0.00904624 |   0.00539023 |              0.521569 |    0.00541512 |               0.510471 |    0.00529824 |               0.538411 |    0.00904624 |               0.562582 | 0.126106 |           0.562582 |        0.0181349 |     0.0406145 |            0.729266 |                0.256437 |            0.0947071 |                                0.126124 |                     0.127422 |                    0.0495174 |            0.135736 |                  0.135736 |           0.0801594 |                  0.152046 |                  0.119034 |                      0.0495174 |                          0.256437 |                           0.126124 |                              0.127422 |                  0.0947071 |                 0.016974 |                    0.036757 |              0.75 |                   0.75 |                1.23398 |                                    5 |                    0.00997226 |                      0.0511415 | CONDITIONAL_ONLY_RESEARCH | weak_h10_ic; weak_h10_positive_ic_rate; h20_dependency_risk; activation_too_broad |

## Specific Diagnostic Answers

- Genuinely idiosyncratic stress containment: positive idiosyncratic-state count was `5` and best idiosyncratic-state IC was `0.009972`.
- Broad drawdown-pressure risk: max drawdown-pressure correlation was `0.049517`.
- Reversal risk: max price-reversal correlation was `0.135736` and max generic reversal correlation was `0.135736`.
- Momentum risk: max price-momentum correlation was `0.152046` and max generic momentum correlation was `0.080159`.
- Breadth/participation repair risk: max breadth/participation repair correlation was `0.126124`.
- Volatility/stress stabilization risk: max volatility/stress correlation was `0.127422`.
- Inventory overlap risk: max inventory correlation was `0.094707`.
- h20 dependence risk: h10 IC was `0.005415` and h20 IC was `0.009046`.
- Sparse or broad activation risk: active date ratio was `0.729266`.
- Turnover risk: turnover proxy was `0.018135`.
- Directional stability: WFV-style persistence/sign consistency were `0.750000` / `0.750000`.
- h5/h10/h15/h20 profile: h5 `0.005390`, h10 `0.005415`, h15 `0.005298`, h20 `0.009046`.

## Recommended Next Step

`idiosyncratic_stress_containment_10` should remain conditional-only research evidence until h10 strength or idiosyncratic-state support improves.
