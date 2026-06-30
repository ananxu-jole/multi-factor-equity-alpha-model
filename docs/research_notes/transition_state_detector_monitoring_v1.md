# Transition-State Detector Monitoring Framework v1

Date: 2026-05-21

Run id: `transition_state_detector_monitoring_v1`

Detector input: `transition_state_composite_detector_v1`

Attribution input: `transition_state_conditional_attribution_v1`

Status: RESEARCH_ONLY_MONITORING_FRAMEWORK

## Research-Only Guardrail

This is a research-only longitudinal monitoring framework for detector-conditioned attribution. It does not modify detector labels, optimize thresholds, promote detector usage, change gates/schemas/governance, or route the detector into production, portfolio, ML, blending, or optimization logic.

This monitoring framework does not refine detector labels, optimize thresholds, create alpha candidates, or claim deployment readiness. It tracks whether detector-conditioned attribution relationships are stable enough to justify future conditional-validation research.

## Dashboard Summary

| metric                                           |      value | interpretation                                                                        |
|:-------------------------------------------------|-----------:|:--------------------------------------------------------------------------------------|
| max_abs_state_frequency_drift                    |   0.200454 | Lower is more stable; values above 0.10 are watch items.                              |
| candidate_state_pairs_with_thin_windows          |  40.000000 | Thin state/candidate slices should not be overinterpreted.                            |
| candidate_state_pairs_with_direction_instability |  37.000000 | Sign instability weakens claims of repeatable conditional behavior.                   |
| h10_or_h20_relationships_persistent              |   3.000000 | Persistent means differentiated enough and not purely one-window best/worst behavior. |
| total_monitoring_alerts                          | 136.000000 | Alerts are monitoring flags, not downgrade or promotion decisions.                    |

## Detector Usefulness Persistence

| signal_name                                       |   horizon |   window_count | modal_best_state   |   modal_best_state_rate | modal_worst_state   |   modal_worst_state_rate |   mean_state_ic_range |   min_state_ic_range |   max_state_ic_range | stable_best_worst_warning   |   mean_max_state_frequency_drift | detector_usefulness_persistent   |
|:--------------------------------------------------|----------:|---------------:|:-------------------|------------------------:|:--------------------|-------------------------:|----------------------:|---------------------:|---------------------:|:----------------------------|---------------------------------:|:---------------------------------|
| participation_breadth_repair_under_hostile_trend  |        10 |              4 | UNRESOLVED_STRESS  |                0.500000 | ABSORPTION          |                 0.250000 |              0.178608 |             0.071125 |             0.280160 | True                        |                         0.105615 | False                            |
| participation_breadth_repair_under_hostile_trend  |        20 |              4 | ABSORPTION         |                0.250000 | NORMALIZATION       |                 0.500000 |              0.217625 |             0.045669 |             0.380197 | True                        |                         0.105615 | False                            |
| participation_liquidity_state_shift_20_60         |        10 |              4 | UNRESOLVED_STRESS  |                0.750000 | PROPAGATION         |                 0.500000 |              0.091819 |             0.034076 |             0.224025 | True                        |                         0.105615 | True                             |
| participation_liquidity_state_shift_20_60         |        20 |              4 | ABSORPTION         |                0.250000 | PROPAGATION         |                 0.500000 |              0.096938 |             0.047012 |             0.236142 | True                        |                         0.105615 | False                            |
| volatility_compression_after_stress_stabilization |        10 |              4 | PROPAGATION        |                0.500000 | NORMALIZATION       |                 0.500000 |              0.175688 |             0.113470 |             0.266904 | True                        |                         0.105615 | True                             |
| volatility_compression_after_stress_stabilization |        20 |              4 | ABSORPTION         |                0.500000 | UNRESOLVED_STRESS   |                 0.500000 |              0.209373 |             0.081076 |             0.296930 | True                        |                         0.105615 | True                             |

## Candidate-State Stability

| signal_name                                       |   horizon | state_label       |   window_count |   valid_window_count |   mean_window_ic |   ic_window_std |   same_sign_window_rate |   mean_window_long_short_return |   return_same_sign_window_rate |   min_window_ic_dates |   thin_window_count | stable_direction_warning   | thin_sample_warning   |
|:--------------------------------------------------|----------:|:------------------|---------------:|---------------------:|-----------------:|----------------:|------------------------:|--------------------------------:|-------------------------------:|----------------------:|--------------------:|:---------------------------|:----------------------|
| participation_breadth_repair_under_hostile_trend  |        10 | ABSORPTION        |              4 |                    4 |         0.008897 |        0.032741 |                0.500000 |                        0.000816 |                       0.500000 |                    32 |                   0 | True                       | False                 |
| participation_breadth_repair_under_hostile_trend  |        10 | NORMALIZATION     |              4 |                    0 |        -0.011674 |        0.057496 |                0.500000 |                       -0.000967 |                       0.500000 |                     7 |                   4 | True                       | True                  |
| participation_breadth_repair_under_hostile_trend  |        10 | PROPAGATION       |              3 |                    0 |         0.027921 |        0.086095 |                0.666667 |                        0.007810 |                       0.666667 |                     9 |                   3 | True                       | True                  |
| participation_breadth_repair_under_hostile_trend  |        10 | UNRESOLVED_STRESS |              4 |                    0 |         0.073520 |        0.118645 |                0.750000 |                        0.009184 |                       0.500000 |                     1 |                   4 | False                      | True                  |
| participation_breadth_repair_under_hostile_trend  |        20 | ABSORPTION        |              4 |                    4 |         0.017195 |        0.033470 |                0.500000 |                        0.004033 |                       0.500000 |                    32 |                   0 | True                       | False                 |
| participation_breadth_repair_under_hostile_trend  |        20 | NORMALIZATION     |              4 |                    0 |         0.003855 |        0.021826 |                0.500000 |                        0.000506 |                       0.500000 |                     7 |                   4 | True                       | True                  |
| participation_breadth_repair_under_hostile_trend  |        20 | PROPAGATION       |              3 |                    0 |         0.085262 |        0.063884 |                1.000000 |                        0.025679 |                       1.000000 |                     9 |                   3 | False                      | True                  |
| participation_breadth_repair_under_hostile_trend  |        20 | UNRESOLVED_STRESS |              4 |                    0 |         0.073234 |        0.172224 |                0.500000 |                        0.017945 |                       0.500000 |                     1 |                   4 | True                       | True                  |
| participation_liquidity_state_shift_20_60         |        10 | ABSORPTION        |              4 |                    4 |         0.016436 |        0.038096 |                0.500000 |                        0.002511 |                       0.500000 |                    59 |                   0 | True                       | False                 |
| participation_liquidity_state_shift_20_60         |        10 | NORMALIZATION     |              4 |                    4 |         0.019227 |        0.042405 |                0.500000 |                        0.001531 |                       0.500000 |                    43 |                   0 | True                       | False                 |
| participation_liquidity_state_shift_20_60         |        10 | PROPAGATION       |              4 |                    4 |        -0.010530 |        0.016576 |                0.500000 |                       -0.002373 |                       0.750000 |                    34 |                   0 | True                       | False                 |
| participation_liquidity_state_shift_20_60         |        10 | UNRESOLVED_STRESS |              4 |                    3 |         0.063270 |        0.082390 |                1.000000 |                        0.007045 |                       0.750000 |                     9 |                   1 | False                      | True                  |
| participation_liquidity_state_shift_20_60         |        20 | ABSORPTION        |              4 |                    4 |         0.022080 |        0.048196 |                0.500000 |                        0.003819 |                       0.500000 |                    59 |                   0 | True                       | False                 |
| participation_liquidity_state_shift_20_60         |        20 | NORMALIZATION     |              4 |                    4 |         0.012953 |        0.035178 |                0.750000 |                        0.001038 |                       0.750000 |                    43 |                   0 | False                      | False                 |
| participation_liquidity_state_shift_20_60         |        20 | PROPAGATION       |              4 |                    4 |         0.006220 |        0.017469 |                0.750000 |                        0.001498 |                       0.750000 |                    34 |                   0 | False                      | False                 |
| participation_liquidity_state_shift_20_60         |        20 | UNRESOLVED_STRESS |              4 |                    3 |         0.071246 |        0.105807 |                0.750000 |                        0.012962 |                       0.750000 |                     9 |                   1 | False                      | True                  |
| volatility_compression_after_stress_stabilization |        10 | ABSORPTION        |              4 |                    4 |         0.067378 |        0.047212 |                1.000000 |                        0.005759 |                       0.750000 |                    22 |                   0 | False                      | False                 |
| volatility_compression_after_stress_stabilization |        10 | NORMALIZATION     |              4 |                    1 |         0.006434 |        0.108865 |                0.500000 |                       -0.004558 |                       0.500000 |                    13 |                   3 | True                       | True                  |
| volatility_compression_after_stress_stabilization |        10 | PROPAGATION       |              4 |                    0 |         0.046817 |        0.092190 |                0.500000 |                        0.006166 |                       0.500000 |                     2 |                   4 | True                       | True                  |
| volatility_compression_after_stress_stabilization |        10 | UNRESOLVED_STRESS |              4 |                    0 |        -0.023701 |        0.042763 |                0.750000 |                       -0.003952 |                       0.500000 |                     5 |                   4 | False                      | True                  |
| volatility_compression_after_stress_stabilization |        20 | ABSORPTION        |              4 |                    4 |         0.091980 |        0.083253 |                0.750000 |                        0.013695 |                       0.750000 |                    22 |                   0 | False                      | False                 |
| volatility_compression_after_stress_stabilization |        20 | NORMALIZATION     |              4 |                    1 |         0.010382 |        0.074229 |                0.500000 |                        0.000122 |                       0.500000 |                    13 |                   3 | True                       | True                  |
| volatility_compression_after_stress_stabilization |        20 | PROPAGATION       |              4 |                    0 |         0.050297 |        0.058898 |                0.750000 |                        0.010576 |                       0.750000 |                     2 |                   4 | False                      | True                  |
| volatility_compression_after_stress_stabilization |        20 | UNRESOLVED_STRESS |              4 |                    0 |        -0.017645 |        0.099133 |                0.500000 |                       -0.009583 |                       0.500000 |                     5 |                   4 | True                       | True                  |

## Largest State Frequency Drift

|   window_id | state_label       |   window_state_ratio |   full_state_ratio |   ratio_drift |   abs_ratio_drift |   window_state_dates | thin_state_warning   |
|------------:|:------------------|---------------------:|-------------------:|--------------:|------------------:|---------------------:|:---------------------|
|           1 | NEUTRAL           |             0.723810 |           0.523356 |      0.200454 |          0.200454 |                  380 | False                |
|           4 | NEUTRAL           |             0.409524 |           0.523356 |     -0.113832 |          0.113832 |                  215 | False                |
|           2 | NEUTRAL           |             0.429389 |           0.523356 |     -0.093966 |          0.093966 |                  225 | False                |
|           1 | NORMALIZATION     |             0.081905 |           0.139657 |     -0.057752 |          0.057752 |                   43 | False                |
|           1 | ABSORPTION        |             0.112381 |           0.168732 |     -0.056351 |          0.056351 |                   59 | False                |
|           1 | PROPAGATION       |             0.064762 |           0.109628 |     -0.044866 |          0.044866 |                   34 | False                |
|           1 | UNRESOLVED_STRESS |             0.017143 |           0.058627 |     -0.041484 |          0.041484 |                    9 | True                 |
|           2 | ABSORPTION        |             0.206107 |           0.168732 |      0.037375 |          0.037375 |                  108 | False                |
|           2 | PROPAGATION       |             0.146947 |           0.109628 |      0.037318 |          0.037318 |                   77 | False                |
|           4 | UNRESOLVED_STRESS |             0.095238 |           0.058627 |      0.036611 |          0.036611 |                   50 | False                |
|           4 | NORMALIZATION     |             0.173333 |           0.139657 |      0.033677 |          0.033677 |                   91 | False                |
|           2 | NORMALIZATION     |             0.166031 |           0.139657 |      0.026374 |          0.026374 |                   87 | False                |

## Monitoring Alerts

| alert_type                | severity    | signal_name                                      |    horizon | state_label        |   window_id | detail                                     |
|:--------------------------|:------------|:-------------------------------------------------|-----------:|:-------------------|------------:|:-------------------------------------------|
| STATE_FREQUENCY_DRIFT     | WATCH       |                                                  | nan        | NEUTRAL            |    1.000000 | state ratio drift 0.200                    |
| STATE_FREQUENCY_DRIFT     | WATCH       |                                                  | nan        | NEUTRAL            |    4.000000 | state ratio drift -0.114                   |
| STATE_TRANSITION_DRIFT    | WATCH       |                                                  | nan        | NEUTRAL_TO_NEUTRAL |    1.000000 | transition ratio drift 0.219               |
| STATE_TRANSITION_DRIFT    | WATCH       |                                                  | nan        | NEUTRAL_TO_NEUTRAL |    2.000000 | transition ratio drift -0.110              |
| STATE_TRANSITION_DRIFT    | WATCH       |                                                  | nan        | NEUTRAL_TO_NEUTRAL |    4.000000 | transition ratio drift -0.120              |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   1.000000 | NEUTRAL            |  nan        | same-sign rate 0.500; min window dates 2   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   1.000000 | NORMALIZATION      |  nan        | same-sign rate 1.000; min window dates 7   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   1.000000 | PROPAGATION        |  nan        | same-sign rate 0.667; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   1.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 1.000; min window dates 1   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   5.000000 | NEUTRAL            |  nan        | same-sign rate 0.500; min window dates 2   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   5.000000 | NORMALIZATION      |  nan        | same-sign rate 0.500; min window dates 7   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   5.000000 | PROPAGATION        |  nan        | same-sign rate 0.667; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |   5.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.500; min window dates 1   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_breadth_repair_under_hostile_trend |  10.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 32  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  10.000000 | NEUTRAL            |  nan        | same-sign rate 0.500; min window dates 2   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  10.000000 | NORMALIZATION      |  nan        | same-sign rate 0.500; min window dates 7   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  10.000000 | PROPAGATION        |  nan        | same-sign rate 0.667; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  10.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.750; min window dates 1   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_breadth_repair_under_hostile_trend |  15.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 32  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  15.000000 | NEUTRAL            |  nan        | same-sign rate 0.750; min window dates 2   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  15.000000 | NORMALIZATION      |  nan        | same-sign rate 0.500; min window dates 7   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  15.000000 | PROPAGATION        |  nan        | same-sign rate 0.667; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  15.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.750; min window dates 1   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_breadth_repair_under_hostile_trend |  20.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 32  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  20.000000 | NEUTRAL            |  nan        | same-sign rate 0.750; min window dates 2   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  20.000000 | NORMALIZATION      |  nan        | same-sign rate 0.500; min window dates 7   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  20.000000 | PROPAGATION        |  nan        | same-sign rate 1.000; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_breadth_repair_under_hostile_trend |  20.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.500; min window dates 1   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_liquidity_state_shift_20_60        |   1.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.500; min window dates 9   |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_liquidity_state_shift_20_60        |   5.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 1.000; min window dates 9   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  10.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 59  |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  10.000000 | NEUTRAL            |  nan        | same-sign rate 0.500; min window dates 207 |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  10.000000 | NORMALIZATION      |  nan        | same-sign rate 0.500; min window dates 43  |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  10.000000 | PROPAGATION        |  nan        | same-sign rate 0.500; min window dates 34  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_liquidity_state_shift_20_60        |  10.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 1.000; min window dates 9   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  15.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 59  |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  15.000000 | PROPAGATION        |  nan        | same-sign rate 0.500; min window dates 34  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_liquidity_state_shift_20_60        |  15.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 1.000; min window dates 9   |
| CANDIDATE_STATE_STABILITY | WATCH       | participation_liquidity_state_shift_20_60        |  20.000000 | ABSORPTION         |  nan        | same-sign rate 0.500; min window dates 59  |
| CANDIDATE_STATE_STABILITY | THIN_SAMPLE | participation_liquidity_state_shift_20_60        |  20.000000 | UNRESOLVED_STRESS  |  nan        | same-sign rate 0.750; min window dates 9   |

## Interpretation

The detector continues to look behaviorally meaningful only where candidate-state relationships are directionally repeatable, supported by adequate samples, and not dominated by one monitoring window. Thin slices and unstable best/worst states should remain watch items.

## Recommendation

Keep the Transition-State Composite Detector in research-only monitoring. The next appropriate step is to rerun this monitor after the next inventory monitoring cycle and compare alert persistence. Do not route the detector into production, validation, portfolio, ML, blending, or optimization from this monitoring pass.

## Artifacts

- `rolling_attribution_stability.csv`
- `state_frequency_drift.csv`
- `state_transition_drift.csv`
- `detector_consistency_diagnostics.csv`
- `candidate_state_stability_summary.csv`
- `instability_alerts.csv`
- `rolling_conditional_rankings.csv`
- `transition_persistence_diagnostics.csv`
- `drawdown_clustering_drift.csv`
- `monitoring_dashboard_summary.csv`
- `window_metadata.csv`
- `manifest.json`
