# Calm Regime Relative Stability 10 Refinement

## Executive Takeaway

This research-only refinement diagnostics pass tested a small controlled set of interpretable variants for `calm_regime_relative_stability_10`.

Final classification: `CONDITIONAL_REFINEMENT_CANDIDATE`
Selected refinement variant: `smooth_3_rebalance_10_zero`
Selected variant issues: `none`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, broad search, or implementation of other Expansion v3 concepts was performed.

## Source Context

- v1 note: `docs/research_notes/calm_regime_relative_stability_10_v1.md`
- v1 artifacts: `artifacts/research/calm_regime_relative_stability_10_v1`
- Expansion v3 design screen: `docs/research_notes/track_b_expansion_v3_design_screening.md`
- Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Inventory Governance v2: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`

## Refinement Scope

Controlled areas tested: calm-regime strictness, relative-stability confirmation strength, h10-focused formulation, mild smoothing, rebalance interval, active coverage protection, low-volatility similarity control, and inactive-date handling.

This is not a parameter grid. Each variant changes one interpretable design choice from the v1 formulation.

## Variant Registry

| variant_name                         | signal_name                          | family                         | run_id                                       | gate               |   rebalance_interval |   smooth | low_vol_neutralized   | inactive_handling   | description                                                   |
|:-------------------------------------|:-------------------------------------|:-------------------------------|:---------------------------------------------|:-------------------|---------------------:|---------:|:----------------------|:--------------------|:--------------------------------------------------------------|
| base_rebalance_10_zero               | base_rebalance_10_zero               | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   10 |        0 | False                 | zero                | v1 baseline representation                                    |
| h10_focus_rebalance_5_zero           | h10_focus_rebalance_5_zero           | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                    5 |        0 | False                 | zero                | h10-focused rank-stability formulation with shorter rebalance |
| smooth_3_rebalance_10_zero           | smooth_3_rebalance_10_zero           | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   10 |        3 | False                 | zero                | mild smoothing before 10-day rebalance                        |
| rebalance_5_zero                     | rebalance_5_zero                     | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                    5 |        0 | False                 | zero                | same logic with 5-day rebalance                               |
| rebalance_20_zero                    | rebalance_20_zero                    | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   20 |        0 | False                 | zero                | same logic with 20-day rebalance                              |
| broad_calm_rebalance_10_zero         | broad_calm_rebalance_10_zero         | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BROAD  |                   10 |        0 | False                 | zero                | broader calm gate for active coverage protection              |
| strict_calm_rebalance_10_zero        | strict_calm_rebalance_10_zero        | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_STRICT |                   10 |        0 | False                 | zero                | stricter calm/orderly cross-section confirmation              |
| strong_stability_rebalance_10_zero   | strong_stability_rebalance_10_zero   | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   10 |        0 | False                 | zero                | stronger relative-stability confirmation                      |
| lowvol_neutralized_rebalance_10_zero | lowvol_neutralized_rebalance_10_zero | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   10 |        0 | True                  | zero                | explicit low residual volatility neutralization               |
| inactive_nan_rebalance_10            | inactive_nan_rebalance_10            | calm_regime_relative_stability | calm_regime_relative_stability_10_refinement | CALM_REGIME_BASE   |                   10 |        0 | False                 | nan                 | NaN inactive handling instead of zero inactive handling       |

## Candidate Decision Summary

| signal_name                          | variant_name                         | description                                                   | gate               |   rebalance_interval |   smooth | low_vol_neutralized   | inactive_handling   |   best_horizon |     mean_ic |   h5_mean_ic |   h10_mean_ic |   h10_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |   turnover_proxy |   active_date_ratio |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   one_window_dominance |   max_inventory_corr |   max_reversal_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |   positive_calm_state_count |   best_calm_state_ic |   best_hostile_state_ic | status                           | review_issues                                                                                                                             |   selection_score |
|:-------------------------------------|:-------------------------------------|:--------------------------------------------------------------|:-------------------|---------------------:|---------:|:----------------------|:--------------------|---------------:|------------:|-------------:|--------------:|-----------------------:|--------------:|-----------------------:|-----------------:|--------------------:|------------------:|-----------------------:|-----------------------:|-----------------------:|---------------------:|--------------------:|--------------------------:|--------------------------:|----------------------------:|----------------------------:|---------------------:|------------------------:|:---------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|------------------:|
| strict_calm_rebalance_10_zero        | strict_calm_rebalance_10_zero        | stricter calm/orderly cross-section confirmation              | CALM_REGIME_STRICT |                   10 |        0 | False                 | zero                |             20 |  0.0179784  | -0.00563842  |    0.00851017 |               0.52     |   0.0179784   |               0.573333 |       0.00598776 |           0.0714967 |            nan    |                 nan    |             nan        |             nan        |            0.0231498 |         0.00261344  |                0.00315459 |                 0.184603  |                   0.0619423 |                           6 |           0.0339099  |              0.0372395  | CONDITIONAL_ONLY_RESEARCH        | weak_h10_ic; weak_h10_positive_rate; sparse_activation; hostile_state_dependence_risk                                                     |          1.98628  |
| broad_calm_rebalance_10_zero         | broad_calm_rebalance_10_zero         | broader calm gate for active coverage protection              | CALM_REGIME_BROAD  |                   10 |        0 | False                 | zero                |             20 |  0.00739432 | -0.000267803 |    0.00239475 |               0.548134 |   0.00739432  |               0.580357 |       0.0203805  |           0.276454  |              0.75 |                   0.75 |               0.341637 |               0.392825 |            0.0454895 |         0.00311025  |                0.00423935 |                 0.355755  |                   0.122545  |                           5 |           0.0172969  |              0.00877653 | CONDITIONAL_ONLY_RESEARCH        | weak_h10_ic; h20_strength_not_preserved                                                                                                   |          0.882759 |
| rebalance_5_zero                     | rebalance_5_zero                     | same logic with 5-day rebalance                               | CALM_REGIME_BASE   |                    5 |        0 | False                 | zero                |             20 |  0.00940921 | -0.00501936  |   -0.00404393 |               0.454167 |   0.00940921  |               0.545833 |       0.0158668  |           0.114395  |              0.75 |                   0.75 |               0.290727 |               0.523016 |            0.029243  |         0.00180646  |                0.00273167 |                 0.231863  |                   0.0807688 |                           5 |           0.00800772 |              0.0822079  | CONDITIONAL_ONLY_RESEARCH        | weak_h10_ic; weak_h10_positive_rate; h20_strength_not_preserved; hostile_state_dependence_risk                                            |          0.295589 |
| h10_focus_rebalance_5_zero           | h10_focus_rebalance_5_zero           | h10-focused rank-stability formulation with shorter rebalance | CALM_REGIME_BASE   |                    5 |        0 | False                 | zero                |             20 |  0.0120163  | -0.0118475   |   -0.00618906 |               0.445833 |   0.0120163   |               0.570833 |       0.0164183  |           0.114395  |              0.75 |                   0.75 |               0.377791 |               0.432631 |            0.0362398 |         0.0017855   |                0.00210798 |                 0.22733   |                   0.0714135 |                           5 |           0.0107915  |              0.0848894  | CONDITIONAL_ONLY_RESEARCH        | weak_h10_ic; weak_h10_positive_rate; hostile_state_dependence_risk                                                                        |          0.175796 |
| smooth_3_rebalance_10_zero           | smooth_3_rebalance_10_zero           | mild smoothing before 10-day rebalance                        | CALM_REGIME_BASE   |                   10 |        3 | False                 | zero                |             20 |  0.0233945  |  0.00184339  |    0.0137653  |               0.546429 |   0.0233945   |               0.628571 |       0.0106302  |           0.13346   |              0.75 |                   0.75 |               0.590035 |               0.609014 |            0.0317579 |         0.00475931  |                0.0047593  |                 0.249905  |                   0.0864799 |                           6 |           0.0291613  |              0.0169867  | CONDITIONAL_REFINEMENT_CANDIDATE | none                                                                                                                                      |          2.71791  |
| lowvol_neutralized_rebalance_10_zero | lowvol_neutralized_rebalance_10_zero | explicit low residual volatility neutralization               | CALM_REGIME_BASE   |                   10 |        0 | True                  | zero                |             20 |  0.0228462  |  0.00730095  |    0.0126108  |               0.575    |   0.0228462   |               0.578571 |       0.011553   |           0.13346   |              0.75 |                   0.75 |               1.24697  |               0.47591  |            0.0193776 |         0.00543577  |                0.0159359  |                 0.0679947 |                   0.0212422 |                           6 |           0.0241923  |              0.0392418  | CONDITIONAL_REFINEMENT_CANDIDATE | hostile_state_dependence_risk                                                                                                             |          2.70624  |
| base_rebalance_10_zero               | base_rebalance_10_zero               | v1 baseline representation                                    | CALM_REGIME_BASE   |                   10 |        0 | False                 | zero                |             20 |  0.0220788  |  0.00162324  |    0.0135587  |               0.546429 |   0.0220788   |               0.603571 |       0.0106398  |           0.13346   |              0.75 |                   0.75 |               0.598608 |               0.585449 |            0.0322375 |         0.00271683  |                0.00271682 |                 0.247124  |                   0.0854175 |                           6 |           0.0271578  |              0.0149822  | CONDITIONAL_REFINEMENT_CANDIDATE | none                                                                                                                                      |          2.64577  |
| strong_stability_rebalance_10_zero   | strong_stability_rebalance_10_zero   | stronger relative-stability confirmation                      | CALM_REGIME_BASE   |                   10 |        0 | False                 | zero                |             20 |  0.0161113  |  0.000229441 |    0.0105636  |               0.546429 |   0.0161113   |               0.610714 |       0.0106083  |           0.13346   |              0.75 |                   0.75 |               0.677667 |               0.743076 |            0.0283415 |         0.00221523  |                0.00221522 |                 0.226584  |                   0.0896109 |                           6 |           0.0197383  |              0.0194312  | CONDITIONAL_REFINEMENT_CANDIDATE | one_window_dominance_risk                                                                                                                 |          2.11978  |
| rebalance_20_zero                    | rebalance_20_zero                    | same logic with 20-day rebalance                              | CALM_REGIME_BASE   |                   20 |        0 | False                 | zero                |             10 |  0.0101014  |  6.45228e-05 |    0.0101014  |               0.529167 |   0.000373408 |               0.554167 |       0.0056552  |           0.114395  |              0.5  |                   0.5  |               0.360752 |               0.620432 |            0.020046  |         0.00910134  |                0.00910133 |                 0.196426  |                   0.0827986 |                           6 |           0.0106182  |              0.0945993  | CONDITIONAL_REFINEMENT_CANDIDATE | h20_strength_not_preserved; weak_wfv_persistence; weak_wfv_sign_consistency; hostile_state_dependence_risk                                |          1.44601  |
| inactive_nan_rebalance_10            | inactive_nan_rebalance_10            | NaN inactive handling instead of zero inactive handling       | CALM_REGIME_BASE   |                   10 |        0 | False                 | nan                 |             20 | -0.00932878 | -0.00390056  |   -0.00630545 |               0.488313 |  -0.00932878  |               0.47906  |       0.0071215  |           0.942803  |              0.25 |                   0.75 |              -0.830028 |               0.736799 |            0.0433629 |         0.000533479 |                0.013126   |                 0.416854  |                   0.165901  |                           0 |          -0.00250696 |             -0.00747054 | REJECT_RESEARCH                  | weak_h10_ic; weak_h10_positive_rate; h20_strength_not_preserved; weak_wfv_persistence; one_window_dominance_risk; weak_calm_state_support |         -0.745492 |

## h5 / h10 / h20 Behavior

| signal_name                          |   horizon |      mean_ic |        ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-------------------------------------|----------:|-------------:|-------------:|-------------------:|----------:|:------------------|
| base_rebalance_10_zero               |         5 |  0.00162324  |  0.0148289   |           0.514286 |       280 | False             |
| h10_focus_rebalance_5_zero           |         5 | -0.0118475   | -0.102599    |           0.429167 |       240 | False             |
| smooth_3_rebalance_10_zero           |         5 |  0.00184339  |  0.0168337   |           0.510714 |       280 | False             |
| rebalance_5_zero                     |         5 | -0.00501936  | -0.0463152   |           0.470833 |       240 | False             |
| rebalance_20_zero                    |         5 |  6.45228e-05 |  0.000601694 |           0.529167 |       240 | False             |
| broad_calm_rebalance_10_zero         |         5 | -0.000267803 | -0.00314886  |           0.515152 |      1023 | False             |
| strict_calm_rebalance_10_zero        |         5 | -0.00563842  | -0.050935    |           0.506667 |       150 | False             |
| strong_stability_rebalance_10_zero   |         5 |  0.000229441 |  0.00242534  |           0.507143 |       280 | False             |
| lowvol_neutralized_rebalance_10_zero |         5 |  0.00730095  |  0.0771808   |           0.517857 |       280 | False             |
| inactive_nan_rebalance_10            |         5 | -0.00390056  | -0.0301287   |           0.480993 |      1973 | False             |
| base_rebalance_10_zero               |        10 |  0.0135587   |  0.135665    |           0.546429 |       280 | False             |
| h10_focus_rebalance_5_zero           |        10 | -0.00618906  | -0.0550017   |           0.445833 |       240 | False             |
| smooth_3_rebalance_10_zero           |        10 |  0.0137653   |  0.13779     |           0.546429 |       280 | False             |
| rebalance_5_zero                     |        10 | -0.00404393  | -0.0389679   |           0.454167 |       240 | False             |
| rebalance_20_zero                    |        10 |  0.0101014   |  0.0984655   |           0.529167 |       240 | True              |
| broad_calm_rebalance_10_zero         |        10 |  0.00239475  |  0.0290903   |           0.548134 |      1018 | False             |
| strict_calm_rebalance_10_zero        |        10 |  0.00851017  |  0.0824681   |           0.52     |       150 | False             |
| strong_stability_rebalance_10_zero   |        10 |  0.0105636   |  0.121957    |           0.546429 |       280 | False             |
| lowvol_neutralized_rebalance_10_zero |        10 |  0.0126108   |  0.148741    |           0.575    |       280 | False             |
| inactive_nan_rebalance_10            |        10 | -0.00630545  | -0.0496595   |           0.488313 |      1968 | False             |
| base_rebalance_10_zero               |        20 |  0.0220788   |  0.228774    |           0.603571 |       280 | True              |
| h10_focus_rebalance_5_zero           |        20 |  0.0120163   |  0.109638    |           0.570833 |       240 | True              |
| smooth_3_rebalance_10_zero           |        20 |  0.0233945   |  0.2374      |           0.628571 |       280 | True              |
| rebalance_5_zero                     |        20 |  0.00940921  |  0.0882405   |           0.545833 |       240 | True              |
| rebalance_20_zero                    |        20 |  0.000373408 |  0.00341489  |           0.554167 |       240 | False             |
| broad_calm_rebalance_10_zero         |        20 |  0.00739432  |  0.0879378   |           0.580357 |      1008 | True              |
| strict_calm_rebalance_10_zero        |        20 |  0.0179784   |  0.195549    |           0.573333 |       150 | True              |
| strong_stability_rebalance_10_zero   |        20 |  0.0161113   |  0.19213     |           0.610714 |       280 | True              |
| lowvol_neutralized_rebalance_10_zero |        20 |  0.0228462   |  0.263521    |           0.578571 |       280 | True              |
| inactive_nan_rebalance_10            |        20 | -0.00932878  | -0.0753854   |           0.47906  |      1958 | True              |

## Structural Quality And Active Coverage

| signal_name                          |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| base_rebalance_10_zero               |   2098 |       478 |     0.0403353 |     0.959665 |        0.971401 |               0.959665 |           0 |       0.0106398  |              0 |       0.568804 |             0.139216  |            280 |           0.13346   |                       30 |               0.985281 |
| h10_focus_rebalance_5_zero           |   2098 |       478 |     0.0403054 |     0.959695 |        0.971401 |               0.959695 |           0 |       0.0164183  |              0 |       0.5      |             0.11963   |            240 |           0.114395  |                       46 |               0.984658 |
| smooth_3_rebalance_10_zero           |   2098 |       478 |     0.0449621 |     0.955038 |        0.966635 |               0.955038 |           0 |       0.0106302  |              0 |       0.539126 |             0.139871  |            280 |           0.13346   |                       30 |               0.985281 |
| rebalance_5_zero                     |   2098 |       478 |     0.0403054 |     0.959695 |        0.971401 |               0.959695 |           0 |       0.0158668  |              0 |       0.5      |             0.11963   |            240 |           0.114395  |                       46 |               0.984658 |
| rebalance_20_zero                    |   2098 |       478 |     0.040425  |     0.959575 |        0.971401 |               0.959575 |           0 |       0.0056552  |              0 |       0.520952 |             0.119631  |            240 |           0.114395  |                       22 |               0.985356 |
| broad_calm_rebalance_10_zero         |   2098 |       478 |     0.0403353 |     0.959665 |        0.971401 |               0.959665 |           0 |       0.0203805  |              0 |       0.587578 |             0.505468  |            580 |           0.276454  |                       48 |               0.986366 |
| strict_calm_rebalance_10_zero        |   2098 |       478 |     0.0403353 |     0.959665 |        0.971401 |               0.959665 |           0 |       0.00598776 |              0 |       0.568804 |             0.0755631 |            150 |           0.0714967 |                       18 |               0.984937 |
| strong_stability_rebalance_10_zero   |   2098 |       478 |     0.0403353 |     0.959665 |        0.971401 |               0.959665 |           0 |       0.0106083  |              0 |       0.552608 |             0.139216  |            280 |           0.13346   |                       30 |               0.985281 |
| lowvol_neutralized_rebalance_10_zero |   2098 |       478 |     0.0403353 |     0.959665 |        0.971401 |               0.959665 |           0 |       0.011553   |              0 |       0.71181  |             0.139216  |            280 |           0.13346   |                       30 |               0.985281 |
| inactive_nan_rebalance_10            |   2098 |       478 |     0.0687545 |     0.931246 |        0.942803 |               0.931246 |           0 |       0.0071215  |              0 |       0.567256 |             1         |           1978 |           0.942803  |                        1 |               0.987742 |

## WFV-Style Diagnostics

| signal_name                          |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| rebalance_20_zero                    |        10 |           4 |               0.0101014  |               0.360752 |          0.5  |               0.5  |               0.620432 |
| base_rebalance_10_zero               |        20 |           4 |               0.0220788  |               0.598608 |          0.75 |               0.75 |               0.585449 |
| h10_focus_rebalance_5_zero           |        20 |           4 |               0.0120163  |               0.377791 |          0.75 |               0.75 |               0.432631 |
| smooth_3_rebalance_10_zero           |        20 |           4 |               0.0233945  |               0.590035 |          0.75 |               0.75 |               0.609014 |
| rebalance_5_zero                     |        20 |           4 |               0.00940921 |               0.290727 |          0.75 |               0.75 |               0.523016 |
| broad_calm_rebalance_10_zero         |        20 |           4 |               0.00739432 |               0.341637 |          0.75 |               0.75 |               0.392825 |
| strong_stability_rebalance_10_zero   |        20 |           4 |               0.0161113  |               0.677667 |          0.75 |               0.75 |               0.743076 |
| lowvol_neutralized_rebalance_10_zero |        20 |           4 |               0.0228462  |               1.24697  |          0.75 |               0.75 |               0.47591  |
| inactive_nan_rebalance_10            |        20 |           4 |              -0.00933423 |              -0.830028 |          0.25 |               0.75 |               0.736799 |

## WFV Window Detail

| signal_name                          |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| rebalance_20_zero                    |        10 |        1 | 2018-06-25   | 2019-05-09 |    0.054057    |   0.672909   |           0.733333 |               60 |
| rebalance_20_zero                    |        10 |        2 | 2019-10-30   | 2020-09-14 |   -0.000387898 |  -0.00631794 |           0.45     |               60 |
| rebalance_20_zero                    |        10 |        3 | 2021-01-08   | 2024-04-12 |   -0.0229733   |  -0.163383   |           0.366667 |               60 |
| rebalance_20_zero                    |        10 |        4 | 2025-06-26   | 2025-11-14 |    0.00970977  |   0.102539   |           0.566667 |               60 |
| base_rebalance_10_zero               |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.0790201   |   1.01138    |           0.8      |               70 |
| base_rebalance_10_zero               |        20 |        2 | 2019-10-30   | 2020-09-14 |    0.0222647   |   0.263747   |           0.628571 |               70 |
| base_rebalance_10_zero               |        20 |        3 | 2021-01-08   | 2024-03-28 |   -0.0233292   |  -0.202169   |           0.428571 |               70 |
| base_rebalance_10_zero               |        20 |        4 | 2024-04-01   | 2025-10-31 |    0.0103594   |   0.142731   |           0.557143 |               70 |
| h10_focus_rebalance_5_zero           |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.05253     |   0.509874   |           0.633333 |               60 |
| h10_focus_rebalance_5_zero           |        20 |        2 | 2019-10-23   | 2020-08-28 |    0.0154697   |   0.159358   |           0.65     |               60 |
| h10_focus_rebalance_5_zero           |        20 |        3 | 2020-08-31   | 2022-08-31 |   -0.0366772   |  -0.304369   |           0.416667 |               60 |
| h10_focus_rebalance_5_zero           |        20 |        4 | 2024-03-15   | 2025-12-30 |    0.0167428   |   0.172296   |           0.583333 |               60 |
| smooth_3_rebalance_10_zero           |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.0860333   |   1.18374    |           0.857143 |               70 |
| smooth_3_rebalance_10_zero           |        20 |        2 | 2019-10-30   | 2020-09-14 |    0.0183964   |   0.21999    |           0.628571 |               70 |
| smooth_3_rebalance_10_zero           |        20 |        3 | 2021-01-08   | 2024-03-28 |   -0.0238442   |  -0.199119   |           0.457143 |               70 |
| smooth_3_rebalance_10_zero           |        20 |        4 | 2024-04-01   | 2025-10-31 |    0.0129927   |   0.168563   |           0.571429 |               70 |
| rebalance_5_zero                     |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.0559477   |   0.576835   |           0.666667 |               60 |
| rebalance_5_zero                     |        20 |        2 | 2019-10-23   | 2020-08-28 |    0.00192419  |   0.0213822  |           0.533333 |               60 |
| rebalance_5_zero                     |        20 |        3 | 2020-08-31   | 2022-08-31 |   -0.0346672   |  -0.276065   |           0.433333 |               60 |
| rebalance_5_zero                     |        20 |        4 | 2024-03-15   | 2025-12-30 |    0.0144321   |   0.161191   |           0.55     |               60 |
| broad_calm_rebalance_10_zero         |        20 |        1 | 2018-06-25   | 2020-01-29 |    0.0231877   |   0.26867    |           0.634921 |              252 |
| broad_calm_rebalance_10_zero         |        20 |        2 | 2020-01-30   | 2023-08-01 |   -0.0245187   |  -0.224312   |           0.440476 |              252 |
| broad_calm_rebalance_10_zero         |        20 |        3 | 2023-08-02   | 2025-04-07 |    0.0308818   |   0.460185   |           0.65873  |              252 |
| broad_calm_rebalance_10_zero         |        20 |        4 | 2025-04-08   | 2026-04-09 |    2.64503e-05 |   0.00052816 |           0.587302 |              252 |
| strong_stability_rebalance_10_zero   |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.0559609   |   0.737244   |           0.757143 |               70 |
| strong_stability_rebalance_10_zero   |        20 |        2 | 2019-10-30   | 2020-09-14 |    0.0114994   |   0.150188   |           0.585714 |               70 |
| strong_stability_rebalance_10_zero   |        20 |        3 | 2021-01-08   | 2024-03-28 |   -0.00543237  |  -0.056081   |           0.5      |               70 |
| strong_stability_rebalance_10_zero   |        20 |        4 | 2024-04-01   | 2025-10-31 |    0.00241711  |   0.0346746  |           0.6      |               70 |
| lowvol_neutralized_rebalance_10_zero |        20 |        1 | 2018-06-25   | 2019-08-05 |    0.0156822   |   0.202309   |           0.542857 |               70 |
| lowvol_neutralized_rebalance_10_zero |        20 |        2 | 2019-10-30   | 2020-09-14 |    0.0461564   |   0.642188   |           0.728571 |               70 |
| lowvol_neutralized_rebalance_10_zero |        20 |        3 | 2021-01-08   | 2024-03-28 |    0.0323465   |   0.295368   |           0.585714 |               70 |
| lowvol_neutralized_rebalance_10_zero |        20 |        4 | 2024-04-01   | 2025-10-31 |   -0.00280036  |  -0.0375741  |           0.457143 |               70 |
| inactive_nan_rebalance_10            |        20 |        1 | 2018-06-25   | 2020-06-04 |    0.000324359 |   0.00292566 |           0.510204 |              490 |
| inactive_nan_rebalance_10            |        20 |        2 | 2020-06-05   | 2022-05-13 |   -0.00831267  |  -0.0658753  |           0.506122 |              490 |
| inactive_nan_rebalance_10            |        20 |        3 | 2022-05-16   | 2024-04-25 |   -0.00136084  |  -0.0104939  |           0.490798 |              489 |
| inactive_nan_rebalance_10            |        20 |        4 | 2024-04-26   | 2026-04-09 |   -0.0279878   |  -0.223216   |           0.408998 |              489 |

## Similarity Summary

| signal_name                          | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_10_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   simple_rank_stability_10_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   simple_range_stability_corr |   raw_calm_stability_composite_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |
|:-------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|------------------------------:|------------------------------:|------------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|------------------------------:|------------------------------------:|--------------------------:|--------------------------:|----------------------------:|
| base_rebalance_10_zero               | simple_low_residual_volatility_20        |               0.247124  |                 0.0322375  |              2.70713e-08 |                 1.89723e-08 |            0.0322375 |         0.00271683  |         0.00107615  |                   0.00167465  |                   0.00271682  |                   0.00107615  |                      0.0854175  |                       0.237147  |                                0.247124  |                     0.057277  |                          0.00668669 |                0.00271682 |                 0.247124  |                   0.0854175 |
| broad_calm_rebalance_10_zero         | simple_low_residual_volatility_20        |               0.355755  |                 0.0454895  |              0.000518282 |                 0.000387957 |            0.0454895 |         0.00311025  |         0.00250714  |                   0.00423935  |                   0.00311024  |                   0.00250714  |                      0.122545   |                       0.338656  |                                0.355755  |                     0.0787284 |                          0.0105932  |                0.00423935 |                 0.355755  |                   0.122545  |
| h10_focus_rebalance_5_zero           | simple_low_residual_volatility_20        |               0.22733   |                 0.0362398  |              0.000192808 |                 2.05133e-08 |            0.0362398 |         0.0017855   |         0.00146789  |                   0.00210798  |                   0.00178549  |                   0.00146789  |                      0.0714135  |                       0.224107  |                                0.22733   |                     0.0143403 |                          0.0397805  |                0.00210798 |                 0.22733   |                   0.0714135 |
| inactive_nan_rebalance_10            | simple_low_volatility_20                 |               0.416854  |                 0.00973483 |              0.00249997  |                 0.0433629   |            0.0433629 |         0.000533479 |         0.013126    |                   0.00309877  |                   0.000533478 |                   0.013126    |                      0.165901   |                       0.416854  |                                0.402236  |                     0.0304736 |                          0.00681241 |                0.013126   |                 0.416854  |                   0.165901  |
| lowvol_neutralized_rebalance_10_zero | v2_vol_compression_range_expansion_20_60 |               0.0682051 |                 0.0193776  |              2.70713e-08 |                 1.89723e-08 |            0.0193776 |         0.00543577  |         0.0159359   |                   0.000295435 |                   0.00431615  |                   0.0159359   |                      0.00712298 |                       0.0679947 |                                0.0543284 |                     0.0212422 |                          0.00710466 |                0.0159359  |                 0.0679947 |                   0.0212422 |
| rebalance_20_zero                    | simple_low_residual_volatility_20        |               0.196426  |                 0.020046   |              3.44333e-08 |                 1.89654e-08 |            0.020046  |         0.00910134  |         0.00351601  |                   0.00489828  |                   0.00910133  |                   0.00351601  |                      0.0827986  |                       0.188899  |                                0.196426  |                     0.047161  |                          0.00185129 |                0.00910133 |                 0.196426  |                   0.0827986 |
| rebalance_5_zero                     | simple_low_residual_volatility_20        |               0.231863  |                 0.029243   |              0.00088222  |                 2.05133e-08 |            0.029243  |         0.00180646  |         0.00273167  |                   0.00124502  |                   0.00180646  |                   0.00273167  |                      0.0807688  |                       0.221255  |                                0.231863  |                     0.0194752 |                          0.027051   |                0.00273167 |                 0.231863  |                   0.0807688 |
| smooth_3_rebalance_10_zero           | simple_low_residual_volatility_20        |               0.249905  |                 0.0317579  |              3.17705e-08 |                 1.64422e-08 |            0.0317579 |         0.00475931  |         9.78793e-05 |                   0.00385284  |                   0.0047593   |                   9.78793e-05 |                      0.0864799  |                       0.239113  |                                0.249905  |                     0.0654935 |                          0.00251869 |                0.0047593  |                 0.249905  |                   0.0864799 |
| strict_calm_rebalance_10_zero        | simple_low_residual_volatility_20        |               0.184603  |                 0.0231498  |              3.69929e-08 |                 2.59257e-08 |            0.0231498 |         0.00261344  |         0.00179618  |                   0.00315459  |                   0.00261343  |                   0.00179618  |                      0.0619423  |                       0.173093  |                                0.184603  |                     0.0394132 |                          0.00743922 |                0.00315459 |                 0.184603  |                   0.0619423 |
| strong_stability_rebalance_10_zero   | simple_low_residual_volatility_20        |               0.226584  |                 0.0283415  |              2.70713e-08 |                 1.89723e-08 |            0.0283415 |         0.00221523  |         0.00178039  |                   0.00145179  |                   0.00221522  |                   0.00178039  |                      0.0896109  |                       0.207039  |                                0.226584  |                     0.0488954 |                          0.00470525 |                0.00221522 |                 0.226584  |                   0.0896109 |

## Calm / Neutral Vs Hostile / Stress Attribution

| signal_name                          |   horizon | state                    |   n_dates |   mean_ic |      ic_ir |   positive_ic_rate |
|:-------------------------------------|----------:|:-------------------------|----------:|----------:|-----------:|-------------------:|
| h10_focus_rebalance_5_zero           |        20 | recovery_phase           |         1 | 0.277553  | nan        |           1        |
| base_rebalance_10_zero               |        20 | recovery_phase           |         1 | 0.276599  | nan        |           1        |
| rebalance_5_zero                     |        20 | recovery_phase           |         1 | 0.276599  | nan        |           1        |
| smooth_3_rebalance_10_zero           |        20 | recovery_phase           |         1 | 0.262176  | nan        |           1        |
| strong_stability_rebalance_10_zero   |        20 | recovery_phase           |         1 | 0.211787  | nan        |           1        |
| lowvol_neutralized_rebalance_10_zero |        20 | recovery_phase           |         1 | 0.187167  | nan        |           1        |
| rebalance_20_zero                    |        10 | weak_breadth             |        16 | 0.0945993 |   0.935267 |           0.875    |
| h10_focus_rebalance_5_zero           |        20 | weak_breadth             |        10 | 0.0848894 |   1.47275  |           0.9      |
| rebalance_5_zero                     |        20 | weak_breadth             |        10 | 0.0822079 |   1.63503  |           0.9      |
| h10_focus_rebalance_5_zero           |        20 | HOSTILE_OR_STRESS        |        12 | 0.0752047 |   1.2851   |           0.833333 |
| rebalance_5_zero                     |        20 | HOSTILE_OR_STRESS        |        12 | 0.0746026 |   1.4858   |           0.916667 |
| h10_focus_rebalance_5_zero           |        20 | high_dispersion_rotation |         8 | 0.0547061 |   0.639188 |           0.625    |
| rebalance_5_zero                     |        20 | drawdown_acceleration    |         5 | 0.0541279 |   0.805216 |           0.8      |
| rebalance_5_zero                     |        20 | high_dispersion_rotation |         8 | 0.0470023 |   0.383035 |           0.625    |
| h10_focus_rebalance_5_zero           |        20 | drawdown_acceleration    |         5 | 0.0414426 |   0.70177  |           0.6      |
| lowvol_neutralized_rebalance_10_zero |        20 | HOSTILE_OR_STRESS        |        33 | 0.0392418 |   0.380689 |           0.484848 |
| strict_calm_rebalance_10_zero        |        20 | weak_breadth             |         3 | 0.0372395 |   1.2942   |           0.666667 |
| strict_calm_rebalance_10_zero        |        20 | HOSTILE_OR_STRESS        |         3 | 0.0372395 |   1.2942   |           0.666667 |

## Sample-Size Sanity

| signal_name                          | state                             |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:-------------------------------------|:----------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| base_rebalance_10_zero               | CALM_REGIME_BASE                  |           255 |          0.121544  |                           167 |                    0.0795996  |
| base_rebalance_10_zero               | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           227 |                    0.108198   |
| base_rebalance_10_zero               | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            90 |                    0.042898   |
| base_rebalance_10_zero               | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           167 |                    0.0795996  |
| base_rebalance_10_zero               | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            33 |                    0.0157293  |
| base_rebalance_10_zero               | SIGNAL_ACTIVE                     |           280 |          0.13346   |                           280 |                    0.13346    |
| h10_focus_rebalance_5_zero           | CALM_REGIME_BASE                  |           255 |          0.121544  |                           180 |                    0.085796   |
| h10_focus_rebalance_5_zero           | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           218 |                    0.103908   |
| h10_focus_rebalance_5_zero           | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            99 |                    0.0471878  |
| h10_focus_rebalance_5_zero           | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           180 |                    0.085796   |
| h10_focus_rebalance_5_zero           | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            12 |                    0.00571973 |
| h10_focus_rebalance_5_zero           | SIGNAL_ACTIVE                     |           240 |          0.114395  |                           240 |                    0.114395   |
| smooth_3_rebalance_10_zero           | CALM_REGIME_BASE                  |           255 |          0.121544  |                           167 |                    0.0795996  |
| smooth_3_rebalance_10_zero           | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           227 |                    0.108198   |
| smooth_3_rebalance_10_zero           | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            90 |                    0.042898   |
| smooth_3_rebalance_10_zero           | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           167 |                    0.0795996  |
| smooth_3_rebalance_10_zero           | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            33 |                    0.0157293  |
| smooth_3_rebalance_10_zero           | SIGNAL_ACTIVE                     |           280 |          0.13346   |                           280 |                    0.13346    |
| rebalance_5_zero                     | CALM_REGIME_BASE                  |           255 |          0.121544  |                           180 |                    0.085796   |
| rebalance_5_zero                     | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           218 |                    0.103908   |
| rebalance_5_zero                     | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            99 |                    0.0471878  |
| rebalance_5_zero                     | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           180 |                    0.085796   |
| rebalance_5_zero                     | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            12 |                    0.00571973 |
| rebalance_5_zero                     | SIGNAL_ACTIVE                     |           240 |          0.114395  |                           240 |                    0.114395   |
| rebalance_20_zero                    | CALM_REGIME_BASE                  |           255 |          0.121544  |                           127 |                    0.0605338  |
| rebalance_20_zero                    | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           179 |                    0.0853194  |
| rebalance_20_zero                    | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            73 |                    0.034795   |
| rebalance_20_zero                    | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           127 |                    0.0605338  |
| rebalance_20_zero                    | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            24 |                    0.0114395  |
| rebalance_20_zero                    | SIGNAL_ACTIVE                     |           240 |          0.114395  |                           240 |                    0.114395   |
| broad_calm_rebalance_10_zero         | CALM_REGIME_BASE                  |           255 |          0.121544  |                           219 |                    0.104385   |
| broad_calm_rebalance_10_zero         | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           457 |                    0.217827   |
| broad_calm_rebalance_10_zero         | CALM_REGIME_STRICT                |           138 |          0.0657769 |                           120 |                    0.0571973  |
| broad_calm_rebalance_10_zero         | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           219 |                    0.104385   |
| broad_calm_rebalance_10_zero         | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            73 |                    0.034795   |
| broad_calm_rebalance_10_zero         | SIGNAL_ACTIVE                     |           580 |          0.276454  |                           580 |                    0.276454   |
| strict_calm_rebalance_10_zero        | CALM_REGIME_BASE                  |           255 |          0.121544  |                            89 |                    0.0424214  |
| strict_calm_rebalance_10_zero        | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           129 |                    0.0614871  |
| strict_calm_rebalance_10_zero        | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            53 |                    0.0252622  |
| strict_calm_rebalance_10_zero        | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                            89 |                    0.0424214  |
| strict_calm_rebalance_10_zero        | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                             3 |                    0.00142993 |
| strict_calm_rebalance_10_zero        | SIGNAL_ACTIVE                     |           150 |          0.0714967 |                           150 |                    0.0714967  |
| strong_stability_rebalance_10_zero   | CALM_REGIME_BASE                  |           255 |          0.121544  |                           167 |                    0.0795996  |
| strong_stability_rebalance_10_zero   | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           227 |                    0.108198   |
| strong_stability_rebalance_10_zero   | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            90 |                    0.042898   |
| strong_stability_rebalance_10_zero   | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           167 |                    0.0795996  |
| strong_stability_rebalance_10_zero   | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            33 |                    0.0157293  |
| strong_stability_rebalance_10_zero   | SIGNAL_ACTIVE                     |           280 |          0.13346   |                           280 |                    0.13346    |
| lowvol_neutralized_rebalance_10_zero | CALM_REGIME_BASE                  |           255 |          0.121544  |                           167 |                    0.0795996  |
| lowvol_neutralized_rebalance_10_zero | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           227 |                    0.108198   |
| lowvol_neutralized_rebalance_10_zero | CALM_REGIME_STRICT                |           138 |          0.0657769 |                            90 |                    0.042898   |
| lowvol_neutralized_rebalance_10_zero | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           167 |                    0.0795996  |
| lowvol_neutralized_rebalance_10_zero | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            33 |                    0.0157293  |
| lowvol_neutralized_rebalance_10_zero | SIGNAL_ACTIVE                     |           280 |          0.13346   |                           280 |                    0.13346    |
| inactive_nan_rebalance_10            | CALM_REGIME_BASE                  |           255 |          0.121544  |                           254 |                    0.121068   |
| inactive_nan_rebalance_10            | CALM_REGIME_BROAD                 |           581 |          0.27693   |                           580 |                    0.276454   |
| inactive_nan_rebalance_10            | CALM_REGIME_STRICT                |           138 |          0.0657769 |                           138 |                    0.0657769  |
| inactive_nan_rebalance_10            | CALM_WITH_HIGH_RELATIVE_STABILITY |           255 |          0.121544  |                           254 |                    0.121068   |
| inactive_nan_rebalance_10            | HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                          1196 |                    0.570067   |
| inactive_nan_rebalance_10            | SIGNAL_ACTIVE                     |          1978 |          0.942803  |                          1978 |                    0.942803   |

## Diagnostic Answers

- h10 improvement: selected variant h10 mean IC is `0.013765` with positive IC rate `0.546429`.
- h20 preservation: selected variant h20 mean IC is `0.023395`.
- Active coverage: selected variant active date ratio is `0.133460`.
- Low-volatility similarity: selected variant max low-volatility correlation is `0.249905`.
- Inventory overlap: selected variant max inventory correlation is `0.031758`.
- Window concentration: selected variant one-window dominance is `0.609014`.

## Final Recommendation

Keep this family in refinement. The evidence remains promising, but the package has not cleanly resolved h10-vs-h20 dependence, sparse activation, and/or low-volatility similarity.
