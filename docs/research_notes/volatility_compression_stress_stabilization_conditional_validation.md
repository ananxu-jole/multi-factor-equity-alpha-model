# Volatility Compression Stress Stabilization Conditional Validation

## Executive Takeaway

This research-only pass validated the fixed shortlist for `volatility_compression_after_stress_stabilization` under isolated run `volatility_compression_stress_stabilization_conditional_validation_v1`.

Final classification: `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`
Decision rationale: Primary variant passed core validation checks, with review guardrails required for residual recent-window and concentration risk.
Review risks: `recent_window_positive_rate_weak`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.

## Scope

Only the fixed shortlist was evaluated. No new variants were created and no parameters were tuned.

| signal_name   | role                 | validation_question                                                                                  | source_signal                                     | source_refinement_run                                                        | run_id                                                                | research_status                                 |
|:--------------|:---------------------|:-----------------------------------------------------------------------------------------------------|:--------------------------------------------------|:-----------------------------------------------------------------------------|:----------------------------------------------------------------------|:------------------------------------------------|
| rebalance_5   | primary_candidate    | Does five-day rebalance remove rank churn while preserving volatility/stress-transition information? | volatility_compression_after_stress_stabilization | artifacts/research/volatility_compression_stress_stabilization_refinement_v1 | volatility_compression_stress_stabilization_conditional_validation_v1 | TRACK_B_V6_CONDITIONAL_VALIDATION_RESEARCH_ONLY |
| smooth_5      | confirmation_control | Does mild five-day smoothing support the same mechanism without rebalance timing dependence?         | volatility_compression_after_stress_stabilization | artifacts/research/volatility_compression_stress_stabilization_refinement_v1 | volatility_compression_stress_stabilization_conditional_validation_v1 | TRACK_B_V6_CONDITIONAL_VALIDATION_RESEARCH_ONLY |
| smooth_3      | confirmation_control | Does lighter smoothing support the same mechanism without over-smoothing?                            | volatility_compression_after_stress_stabilization | artifacts/research/volatility_compression_stress_stabilization_refinement_v1 | volatility_compression_stress_stabilization_conditional_validation_v1 | TRACK_B_V6_CONDITIONAL_VALIDATION_RESEARCH_ONLY |

## Validation Summary

| signal_name   | role                 |   h20_mean_ic |   h20_positive_ic_rate |   h20_n_dates |   turnover_proxy |   active_date_ratio |   persistence |   sign_consistency |   effective_test_ic_ir |   largest_positive_window_share |   recent_window_ic |   recent_window_positive_ic_rate |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:--------------|:---------------------|--------------:|-----------------------:|--------------:|-----------------:|--------------------:|--------------:|-------------------:|-----------------------:|--------------------------------:|-------------------:|---------------------------------:|---------------------:|--------------------:|--------------------:|
| rebalance_5   | primary_candidate    |     0.0283914 |               0.574413 |           383 |        0.0220924 |            0.189704 |          1    |               1    |               1.00841  |                        0.652705 |         0.00229807 |                         0.357895 |            0.0474302 |           0.0577811 |          0.00517082 |
| smooth_5      | confirmation_control |     0.0202484 |               0.565812 |           585 |        0.0313475 |            0.2755   |          0.75 |               0.75 |               0.833225 |                        0.395507 |        -0.0212662  |                         0.383562 |            0.045892  |           0.100002  |          0.0288664  |
| smooth_3      | confirmation_control |     0.0192425 |               0.556641 |           512 |        0.0361019 |            0.248808 |          0.75 |               0.75 |               0.755212 |                        0.488219 |        -0.0217193  |                         0.351562 |            0.0523766 |           0.0890608 |          0.0231838  |

## Multi-Horizon IC

| signal_name   |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------|----------:|-----------:|--------------:|----------:|-------------------:|----------:|:------------------|
| rebalance_5   |         1 | 0.00568142 |    0.00568142 | 0.0383347 |           0.496222 |       397 | False             |
| smooth_5      |         1 | 0.00273957 |    0.00273957 | 0.0184928 |           0.514901 |       604 | False             |
| smooth_3      |         1 | 0.00207275 |    0.00207275 | 0.0137287 |           0.506591 |       531 | False             |
| rebalance_5   |         5 | 0.01602    |    0.01602    | 0.107167  |           0.559796 |       393 | False             |
| smooth_5      |         5 | 0.0133937  |    0.0133937  | 0.087202  |           0.536667 |       600 | False             |
| smooth_3      |         5 | 0.00962834 |    0.00962834 | 0.0617965 |           0.523719 |       527 | False             |
| rebalance_5   |        10 | 0.0230429  |    0.0230429  | 0.150949  |           0.564103 |       390 | False             |
| smooth_5      |        10 | 0.0167728  |    0.0167728  | 0.109316  |           0.529412 |       595 | False             |
| smooth_3      |        10 | 0.0143742  |    0.0143742  | 0.0916144 |           0.507663 |       522 | False             |
| rebalance_5   |        20 | 0.0283914  |    0.0283914  | 0.183032  |           0.574413 |       383 | True              |
| smooth_5      |        20 | 0.0202484  |    0.0202484  | 0.135921  |           0.565812 |       585 | True              |
| smooth_3      |        20 | 0.0192425  |    0.0192425  | 0.125225  |           0.556641 |       512 | True              |

## h20 Behavior

| signal_name   |   mean_ic |   abs_mean_ic |    ic_ir |   positive_ic_rate |   n_dates |
|:--------------|----------:|--------------:|---------:|-------------------:|----------:|
| rebalance_5   | 0.0283914 |     0.0283914 | 0.183032 |           0.574413 |       383 |
| smooth_5      | 0.0202484 |     0.0202484 | 0.135921 |           0.565812 |       585 |
| smooth_3      | 0.0192425 |     0.0192425 | 0.125225 |           0.556641 |       512 |

## WFV-Style Persistence

| signal_name   |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| rebalance_5   |        20 |           4 |                0.0283235 |               1.00841  |          1    |               1    |               0.652705 |
| smooth_5      |        20 |           4 |                0.0202317 |               0.833225 |          0.75 |               0.75 |               0.32738  |
| smooth_3      |        20 |           4 |                0.0192425 |               0.755212 |          0.75 |               0.75 |               0.400154 |

## WFV Window Distribution

| signal_name   |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:--------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| rebalance_5   |        20 |        1 | 2018-11-29   | 2020-05-21 |     0.00840823 |    0.038723  |           0.614583 |               96 |
| rebalance_5   |        20 |        2 | 2020-05-22   | 2022-06-01 |     0.0286402  |    0.24136   |           0.5625   |               96 |
| rebalance_5   |        20 |        3 | 2022-06-02   | 2024-09-17 |     0.0739475  |    0.702775  |           0.760417 |               96 |
| rebalance_5   |        20 |        4 | 2024-09-18   | 2026-04-09 |     0.00229807 |    0.0159488 |           0.357895 |               95 |
| smooth_5      |        20 |        1 | 2018-11-23   | 2020-06-18 |     0.0299769  |    0.14969   |           0.646259 |              147 |
| smooth_5      |        20 |        2 | 2020-06-19   | 2022-07-06 |     0.0404181  |    0.324272  |           0.59589  |              146 |
| smooth_5      |        20 |        3 | 2022-07-07   | 2024-09-23 |     0.0317981  |    0.26407   |           0.636986 |              146 |
| smooth_5      |        20 |        4 | 2024-09-24   | 2026-04-09 |    -0.0212662  |   -0.167348  |           0.383562 |              146 |
| smooth_3      |        20 |        1 | 2018-11-23   | 2020-06-15 |     0.0273991  |    0.133449  |           0.640625 |              128 |
| smooth_3      |        20 |        2 | 2020-06-16   | 2022-07-07 |     0.0481821  |    0.378711  |           0.648438 |              128 |
| smooth_3      |        20 |        3 | 2022-07-08   | 2024-09-26 |     0.0231083  |    0.190816  |           0.585938 |              128 |
| smooth_3      |        20 |        4 | 2024-09-27   | 2026-04-09 |    -0.0217193  |   -0.158209  |           0.351562 |              128 |

## Window Concentration / Overfit Risk

| signal_name   |   positive_window_count |   negative_window_count |   min_window_ic |   max_window_ic |   window_ic_range |   positive_ic_sum |   largest_positive_window_share |   recent_window_ic |   recent_window_positive_ic_rate |   valid_ic_dates_min |   valid_ic_dates_max |
|:--------------|------------------------:|------------------------:|----------------:|----------------:|------------------:|------------------:|--------------------------------:|-------------------:|---------------------------------:|---------------------:|---------------------:|
| rebalance_5   |                       4 |                       0 |      0.00229807 |       0.0739475 |         0.0716494 |         0.113294  |                        0.652705 |         0.00229807 |                         0.357895 |                   95 |                   96 |
| smooth_3      |                       3 |                       1 |     -0.0217193  |       0.0481821 |         0.0699014 |         0.0986894 |                        0.488219 |        -0.0217193  |                         0.351562 |                  128 |                  128 |
| smooth_5      |                       3 |                       1 |     -0.0212662  |       0.0404181 |         0.0616843 |         0.102193  |                        0.395507 |        -0.0212662  |                         0.383562 |                  146 |                  147 |

Interpretation: `rebalance_5` is positive in all four WFV-style windows, but window 3 contributes a large share of the positive-window IC and the recent window has weak positive-date breadth. This supports integration review, not production use.

## Structural Quality / Active Coverage

| signal_name   |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| rebalance_5   |     0.0330759 |     0.966924 |        0.978551 |        0.0220924 |       0.245686 |            0.189704 |                       53 |               0.989487 |
| smooth_5      |     0.0326362 |     0.967364 |        0.979028 |        0.0313475 |       0.131308 |            0.2755   |                       43 |               0.990412 |
| smooth_3      |     0.0321605 |     0.967839 |        0.979504 |        0.0361019 |       0.188756 |            0.248808 |                       63 |               0.990482 |

## Orthogonality / Similarity

| signal_name   | top_comparison                                            |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:--------------|:----------------------------------------------------------|------------------------:|---------------------------:|-------------------------:|---------------------:|--------------------:|--------------------:|
| rebalance_5   | v6_base_volatility_compression_after_stress_stabilization |                0.684536 |                  0.0474302 |                0.0172333 |            0.0474302 |           0.0577811 |          0.00517082 |
| smooth_3      | v6_base_volatility_compression_after_stress_stabilization |                0.829031 |                  0.0523766 |                0.0098393 |            0.0523766 |           0.0890608 |          0.0231838  |
| smooth_5      | v6_base_volatility_compression_after_stress_stabilization |                0.754716 |                  0.045892  |                0.0140237 |            0.045892  |           0.100002  |          0.0288664  |

## Regime / Stress Attribution

| signal_name   |   horizon | state                    |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------|----------:|:-------------------------|----------:|------------:|------------:|-------------------:|
| rebalance_5   |        20 | panic_liquidity_stress   |        48 |  0.170419   |  1.01118    |           0.791667 |
| rebalance_5   |        20 | drawdown_acceleration    |        49 |  0.165135   |  0.966968   |           0.77551  |
| rebalance_5   |        20 | weak_breadth             |        79 |  0.127372   |  0.794293   |           0.708861 |
| rebalance_5   |        20 | volatility_spike         |       177 |  0.0633418  |  0.358786   |           0.649718 |
| rebalance_5   |        20 | high_dispersion_rotation |       140 |  0.00431183 |  0.0230982  |           0.564286 |
| rebalance_5   |        20 | recovery_phase           |       103 | -0.0027896  | -0.016244   |           0.582524 |
| rebalance_5   |        20 | trend_transition         |       141 | -0.0152662  | -0.0898317  |           0.48227  |
| smooth_3      |        20 | panic_liquidity_stress   |        74 |  0.101045   |  0.485674   |           0.662162 |
| smooth_3      |        20 | drawdown_acceleration    |        79 |  0.0944754  |  0.463263   |           0.658228 |
| smooth_3      |        20 | weak_breadth             |       127 |  0.0743526  |  0.424635   |           0.637795 |
| smooth_3      |        20 | volatility_spike         |       250 |  0.039042   |  0.218296   |           0.6      |
| smooth_3      |        20 | high_dispersion_rotation |       196 | -0.00316833 | -0.0178901  |           0.52551  |
| smooth_3      |        20 | recovery_phase           |       124 | -0.00741944 | -0.0470146  |           0.572581 |
| smooth_3      |        20 | trend_transition         |       186 | -0.0225902  | -0.132544   |           0.451613 |
| smooth_5      |        20 | panic_liquidity_stress   |        86 |  0.083679   |  0.425007   |           0.604651 |
| smooth_5      |        20 | drawdown_acceleration    |        97 |  0.0725282  |  0.380207   |           0.597938 |
| smooth_5      |        20 | weak_breadth             |       150 |  0.0652515  |  0.391742   |           0.62     |
| smooth_5      |        20 | volatility_spike         |       270 |  0.0407406  |  0.230516   |           0.611111 |
| smooth_5      |        20 | high_dispersion_rotation |       220 |  0.00519095 |  0.0300385  |           0.572727 |
| smooth_5      |        20 | recovery_phase           |       131 | -0.00057429 | -0.00359042 |           0.59542  |
| smooth_5      |        20 | trend_transition         |       207 | -0.0155405  | -0.0945157  |           0.478261 |

## Concept-State Attribution

| signal_name   |   horizon | state                           |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------|----------:|:--------------------------------|----------:|------------:|------------:|-------------------:|
| rebalance_5   |        20 | DISPERSION_ELEVATED_RECENT      |       335 |  0.0323168  |  0.202167   |           0.59403  |
| rebalance_5   |        20 | RECENT_VOL_STRESS               |       365 |  0.0288161  |  0.18322    |           0.572603 |
| rebalance_5   |        20 | EVENT_GAP_DAY                   |       383 |  0.0283914  |  0.183032   |           0.574413 |
| rebalance_5   |        20 | RANGE_NORMALIZING               |       318 |  0.0235476  |  0.148998   |           0.572327 |
| rebalance_5   |        20 | DISPERSION_STABILITY_TRANSITION |       167 |  0.00276817 |  0.0171964  |           0.520958 |
| rebalance_5   |        20 | DISPERSION_NORMALIZING          |       187 | -0.00232656 | -0.0150084  |           0.508021 |
| rebalance_5   |        20 | VOL_NORMALIZING                 |       183 | -0.0329441  | -0.212364   |           0.431694 |
| smooth_3      |        20 | DISPERSION_ELEVATED_RECENT      |       436 |  0.0220769  |  0.138037   |           0.575688 |
| smooth_3      |        20 | EVENT_GAP_DAY                   |       512 |  0.0192425  |  0.125225   |           0.556641 |
| smooth_3      |        20 | RECENT_VOL_STRESS               |       486 |  0.0189628  |  0.120886   |           0.55144  |
| smooth_3      |        20 | RANGE_NORMALIZING               |       402 |  0.0131921  |  0.0851674  |           0.549751 |
| smooth_3      |        20 | DISPERSION_STABILITY_TRANSITION |       199 | -0.00544196 | -0.033668   |           0.502513 |
| smooth_3      |        20 | DISPERSION_NORMALIZING          |       227 | -0.00672618 | -0.0433012  |           0.493392 |
| smooth_3      |        20 | VOL_NORMALIZING                 |       221 | -0.0434041  | -0.303296   |           0.39819  |
| smooth_5      |        20 | DISPERSION_ELEVATED_RECENT      |       493 |  0.0238881  |  0.153756   |           0.584178 |
| smooth_5      |        20 | RECENT_VOL_STRESS               |       526 |  0.0209977  |  0.135761   |           0.568441 |
| smooth_5      |        20 | EVENT_GAP_DAY                   |       585 |  0.0202484  |  0.135921   |           0.565812 |
| smooth_5      |        20 | RANGE_NORMALIZING               |       427 |  0.0170471  |  0.110502   |           0.564403 |
| smooth_5      |        20 | DISPERSION_STABILITY_TRANSITION |       220 | -0.00153382 | -0.00967933 |           0.513636 |
| smooth_5      |        20 | DISPERSION_NORMALIZING          |       254 | -0.00367681 | -0.0242445  |           0.503937 |
| smooth_5      |        20 | VOL_NORMALIZING                 |       253 | -0.0371311  | -0.261815   |           0.418972 |

## Nearby-Variant Support

| signal_name                | status                               |   h20_mean_ic |   h20_positive_ic_rate |   turnover_proxy |   active_date_ratio |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   max_inventory_corr |   max_reversal_corr |
|:---------------------------|:-------------------------------------|--------------:|-----------------------:|-----------------:|--------------------:|------------------:|-----------------------:|-----------------------:|---------------------:|--------------------:|
| rebalance_5                | CANDIDATE_FOR_CONDITIONAL_VALIDATION |     0.0283914 |               0.574413 |       0.0220924  |            0.189704 |              1    |                   1    |               1.00841  |            0.0474302 |           0.0577811 |
| rebalance_10               | CONDITIONAL_REFINEMENT_CANDIDATE     |     0.0276599 |               0.55     |       0.0123517  |            0.180172 |              0.5  |                   0.5  |               0.470439 |            0.0231713 |           0.0682407 |
| strict_stress_rebalance_10 | CONDITIONAL_REFINEMENT_CANDIDATE     |     0.0228627 |               0.536741 |       0.00857979 |            0.21449  |              0.75 |                   0.75 |               0.78964  |            0.0172268 |           0.0860186 |
| smooth_5                   | CANDIDATE_FOR_CONDITIONAL_VALIDATION |     0.0202484 |               0.565812 |       0.0313475  |            0.2755   |              0.75 |                   0.75 |               0.833225 |            0.045892  |           0.100002  |
| smooth_3                   | CANDIDATE_FOR_CONDITIONAL_VALIDATION |     0.0192425 |               0.556641 |       0.0361019  |            0.248808 |              0.75 |                   0.75 |               0.755212 |            0.0523766 |           0.0890608 |

The smoothing controls (`smooth_5`, `smooth_3`) confirm the volatility/stress-transition thesis but remain weaker than `rebalance_5` because both retain a negative recent WFV-style window. They should be treated as confirmation/control variants, not primary representations.

## Primary Variant Assessment

- `rebalance_5` has enough active coverage for conditional validation: active date ratio is about 0.19 with roughly 95-96 valid IC dates per WFV-style window.
- h20 behavior is the best horizon and remains positive across all validation windows.
- The edge is strongest in drawdown acceleration, panic/liquidity stress, volatility spike, and weak breadth states.
- Similarity to current inventory candidates, reversal baselines, and momentum baselines remains low.
- Residual risks are window concentration and a weak recent-window positive IC rate, so this is not clean production evidence.

## Final Classification

`CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`

## Recommended Next Step

Move `volatility_compression_after_stress_stabilization` to research-only conditional-alpha integration review with `rebalance_5` as the primary variant and `smooth_5` / `smooth_3` as confirmation controls. Keep guardrails around fixed parameters, active coverage, recent-window monitoring, and window-concentration review.
