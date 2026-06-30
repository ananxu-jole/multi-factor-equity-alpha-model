# Transition-State Conditional Attribution v1

Date: 2026-05-21

Run id: `transition_state_conditional_attribution_v1`

Detector input: `transition_state_composite_detector_v1`

Status: RESEARCH_ONLY_CONDITIONAL_ATTRIBUTION

## Research-Only Guardrail

This is a research-only conditional attribution pass. It does not register, promote, validate, blend, optimize, route, or productionize the Transition-State Composite Detector or any candidate panel. Findings are explanatory diagnostics only and should be used, at most, to motivate future validation or monitoring work.

This pass does not tune detector labels, create candidates, or claim causal proof. It asks whether existing inventory candidates exhibit different behavior under pre-existing detector states.

## Attribution Targets

- `participation_liquidity_state_shift_20_60`
- `participation_breadth_repair_under_hostile_trend`
- `volatility_compression_after_stress_stabilization`

## h10 Candidate-By-State Attribution

| signal_name                                       | state_label       |   mean_ic |   positive_ic_rate |   n_ic_dates |   mean_long_short_return |   hit_rate |   mean_active_coverage |   mean_turnover |
|:--------------------------------------------------|:------------------|----------:|-------------------:|-------------:|-------------------------:|-----------:|-----------------------:|----------------:|
| participation_breadth_repair_under_hostile_trend  | ABSORPTION        |  0.005704 |           0.483871 |          155 |                -0.000242 |   0.516129 |               0.989380 |        0.039428 |
| participation_breadth_repair_under_hostile_trend  | NEUTRAL           |  0.019426 |           0.520000 |           25 |                 0.001185 |   0.440000 |               0.959371 |        0.002343 |
| participation_breadth_repair_under_hostile_trend  | NORMALIZATION     |  0.006996 |           0.488889 |           45 |                 0.001458 |   0.533333 |               0.990961 |        0.018771 |
| participation_breadth_repair_under_hostile_trend  | PROPAGATION       |  0.024709 |           0.609756 |           41 |                 0.008402 |   0.585366 |               0.989603 |        0.010865 |
| participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS |  0.030944 |           0.500000 |           34 |                 0.007938 |   0.500000 |               0.992686 |        0.030030 |
| participation_liquidity_state_shift_20_60         | ABSORPTION        |  0.008498 |           0.500000 |          354 |                 0.001284 |   0.522599 |               0.988943 |        0.243820 |
| participation_liquidity_state_shift_20_60         | NEUTRAL           |  0.002183 |           0.512845 |         1051 |                 0.000521 |   0.511893 |               0.950749 |        0.207024 |
| participation_liquidity_state_shift_20_60         | NORMALIZATION     |  0.008605 |           0.517123 |          292 |                 0.000196 |   0.496575 |               0.990547 |        0.212594 |
| participation_liquidity_state_shift_20_60         | PROPAGATION       | -0.006915 |           0.504348 |          230 |                -0.002824 |   0.473913 |               0.989240 |        0.219316 |
| participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS |  0.031420 |           0.598361 |          122 |                 0.002270 |   0.573770 |               0.992023 |        0.220615 |
| volatility_compression_after_stress_stabilization | ABSORPTION        |  0.063981 |           0.683099 |          142 |                 0.005646 |   0.563380 |               0.989167 |        0.043154 |
| volatility_compression_after_stress_stabilization | NEUTRAL           |  0.012191 |           0.576271 |          118 |                -0.001481 |   0.576271 |               0.945892 |        0.012308 |
| volatility_compression_after_stress_stabilization | NORMALIZATION     | -0.016219 |           0.448718 |           78 |                -0.005428 |   0.448718 |               0.990632 |        0.026431 |
| volatility_compression_after_stress_stabilization | PROPAGATION       |  0.021632 |           0.384615 |           13 |                 0.002498 |   0.461538 |               0.989358 |        0.014199 |
| volatility_compression_after_stress_stabilization | UNRESOLVED_STRESS | -0.014187 |           0.384615 |           39 |                -0.002888 |   0.461538 |               0.992227 |        0.049590 |

## Detector Usefulness Summary

| signal_name                                       | h10_best_state    | h10_worst_state   |   h10_state_ic_range | h20_best_state    | h20_worst_state   |   h20_state_ic_range | h10_best_return_state   | h10_worst_return_state   | largest_h10_tail_loss_concentration_state   |   largest_h10_tail_loss_concentration_ratio |   min_state_ic_dates | detector_appears_contextually_useful   |
|:--------------------------------------------------|:------------------|:------------------|---------------------:|:------------------|:------------------|---------------------:|:------------------------|:-------------------------|:--------------------------------------------|--------------------------------------------:|---------------------:|:---------------------------------------|
| participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS | ABSORPTION        |             0.025239 | PROPAGATION       | NORMALIZATION     |             0.081974 | PROPAGATION             | ABSORPTION               | ABSORPTION                                  |                                    1.354839 |                   25 | True                                   |
| participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS | PROPAGATION       |             0.038336 | UNRESOLVED_STRESS | NORMALIZATION     |             0.021989 | UNRESOLVED_STRESS       | PROPAGATION              | PROPAGATION                                 |                                    1.738282 |                  119 | True                                   |
| volatility_compression_after_stress_stabilization | ABSORPTION        | NORMALIZATION     |             0.080200 | ABSORPTION        | UNRESOLVED_STRESS |             0.100218 | ABSORPTION              | NORMALIZATION            | NORMALIZATION                               |                                    1.282051 |                   13 | True                                   |

## Conditional IC Summary

| signal_name                                       |   horizon | best_state        |   best_state_mean_ic | worst_state       |   worst_state_mean_ic |   neutral_mean_ic |   state_ic_range |   state_positive_rate_range |   min_state_ic_dates |
|:--------------------------------------------------|----------:|:------------------|---------------------:|:------------------|----------------------:|------------------:|-----------------:|----------------------------:|---------------------:|
| participation_breadth_repair_under_hostile_trend  |        10 | UNRESOLVED_STRESS |             0.030944 | ABSORPTION        |              0.005704 |          0.019426 |         0.025239 |                    0.125885 |                   25 |
| participation_breadth_repair_under_hostile_trend  |        20 | PROPAGATION       |             0.088171 | NORMALIZATION     |              0.006196 |          0.042740 |         0.081974 |                    0.280488 |                   25 |
| participation_liquidity_state_shift_20_60         |        10 | UNRESOLVED_STRESS |             0.031420 | PROPAGATION       |             -0.006915 |          0.002183 |         0.038336 |                    0.098361 |                  122 |
| participation_liquidity_state_shift_20_60         |        20 | UNRESOLVED_STRESS |             0.027450 | NORMALIZATION     |              0.005460 |          0.005938 |         0.021989 |                    0.130885 |                  119 |
| volatility_compression_after_stress_stabilization |        10 | ABSORPTION        |             0.063981 | NORMALIZATION     |             -0.016219 |          0.012191 |         0.080200 |                    0.298483 |                   13 |
| volatility_compression_after_stress_stabilization |        20 | ABSORPTION        |             0.085878 | UNRESOLVED_STRESS |             -0.014340 |          0.000422 |         0.100218 |                    0.267806 |                   13 |

## Conditional Return Summary

| signal_name                                       |   horizon | best_return_state   |   best_state_mean_long_short_return | worst_return_state   |   worst_state_mean_long_short_return |   state_return_range |   state_hit_rate_range |   min_state_return_dates |
|:--------------------------------------------------|----------:|:--------------------|------------------------------------:|:---------------------|-------------------------------------:|---------------------:|-----------------------:|-------------------------:|
| participation_breadth_repair_under_hostile_trend  |        10 | PROPAGATION         |                            0.008402 | ABSORPTION           |                            -0.000242 |             0.008645 |               0.145366 |                       25 |
| participation_breadth_repair_under_hostile_trend  |        20 | PROPAGATION         |                            0.027317 | NORMALIZATION        |                             0.002079 |             0.025237 |               0.358266 |                       25 |
| participation_liquidity_state_shift_20_60         |        10 | UNRESOLVED_STRESS   |                            0.002270 | PROPAGATION          |                            -0.002824 |             0.005094 |               0.099857 |                      122 |
| participation_liquidity_state_shift_20_60         |        20 | UNRESOLVED_STRESS   |                            0.004419 | NORMALIZATION        |                            -0.000300 |             0.004719 |               0.105390 |                      119 |
| volatility_compression_after_stress_stabilization |        10 | ABSORPTION          |                            0.005646 | NORMALIZATION        |                            -0.005428 |             0.011074 |               0.127553 |                       13 |
| volatility_compression_after_stress_stabilization |        20 | ABSORPTION          |                            0.014197 | UNRESOLVED_STRESS    |                            -0.010896 |             0.025093 |               0.219943 |                       13 |

## h10 Drawdown Clustering

Tail-loss clustering uses each candidate/horizon's 10th percentile long-short return as the tail threshold. Concentration ratios above 1.0 indicate tail losses are more common in that state than its date share.

| signal_name                                       |   horizon | state_label       |   tail_loss_threshold |   state_dates |   tail_loss_dates |   tail_loss_rate |   tail_loss_share |   state_date_share |   tail_loss_concentration_ratio |   worst_long_short_return |
|:--------------------------------------------------|----------:|:------------------|----------------------:|--------------:|------------------:|-----------------:|------------------:|-------------------:|--------------------------------:|--------------------------:|
| participation_breadth_repair_under_hostile_trend  |        10 | ABSORPTION        |             -0.021801 |           155 |                21 |         0.135484 |          0.700000 |           0.516667 |                        1.354839 |                 -0.061252 |
| participation_breadth_repair_under_hostile_trend  |        10 | NEUTRAL           |             -0.021801 |            25 |                 3 |         0.120000 |          0.100000 |           0.083333 |                        1.200000 |                 -0.025727 |
| participation_breadth_repair_under_hostile_trend  |        10 | UNRESOLVED_STRESS |             -0.021801 |            34 |                 4 |         0.117647 |          0.133333 |           0.113333 |                        1.176471 |                 -0.030656 |
| participation_breadth_repair_under_hostile_trend  |        10 | PROPAGATION       |             -0.021801 |            41 |                 1 |         0.024390 |          0.033333 |           0.136667 |                        0.243902 |                 -0.022768 |
| participation_breadth_repair_under_hostile_trend  |        10 | NORMALIZATION     |             -0.021801 |            45 |                 1 |         0.022222 |          0.033333 |           0.150000 |                        0.222222 |                 -0.029520 |
| participation_liquidity_state_shift_20_60         |        10 | PROPAGATION       |             -0.019956 |           230 |                40 |         0.173913 |          0.195122 |           0.112250 |                        1.738282 |                 -0.170085 |
| participation_liquidity_state_shift_20_60         |        10 | UNRESOLVED_STRESS |             -0.019956 |           122 |                16 |         0.131148 |          0.078049 |           0.059541 |                        1.310836 |                 -0.076844 |
| participation_liquidity_state_shift_20_60         |        10 | ABSORPTION        |             -0.019956 |           354 |                44 |         0.124294 |          0.214634 |           0.172767 |                        1.242332 |                 -0.071563 |
| participation_liquidity_state_shift_20_60         |        10 | NEUTRAL           |             -0.019956 |          1051 |                83 |         0.078972 |          0.404878 |           0.512933 |                        0.789339 |                 -0.063449 |
| participation_liquidity_state_shift_20_60         |        10 | NORMALIZATION     |             -0.019956 |           292 |                22 |         0.075342 |          0.107317 |           0.142509 |                        0.753057 |                 -0.042660 |
| volatility_compression_after_stress_stabilization |        10 | NORMALIZATION     |             -0.025153 |            78 |                10 |         0.128205 |          0.256410 |           0.200000 |                        1.282051 |                 -0.180894 |
| volatility_compression_after_stress_stabilization |        10 | UNRESOLVED_STRESS |             -0.025153 |            39 |                 5 |         0.128205 |          0.128205 |           0.100000 |                        1.282051 |                 -0.097009 |
| volatility_compression_after_stress_stabilization |        10 | NEUTRAL           |             -0.025153 |           118 |                11 |         0.093220 |          0.282051 |           0.302564 |                        0.932203 |                 -0.101494 |
| volatility_compression_after_stress_stabilization |        10 | ABSORPTION        |             -0.025153 |           142 |                12 |         0.084507 |          0.307692 |           0.364103 |                        0.845070 |                 -0.061597 |
| volatility_compression_after_stress_stabilization |        10 | PROPAGATION       |             -0.025153 |            13 |                 1 |         0.076923 |          0.025641 |           0.033333 |                        0.769231 |                 -0.030904 |

## Sample-Size Sanity

| signal_name                                       | state_label       |   detector_state_dates |   min_ic_dates_across_horizons |   min_return_dates_across_horizons |   mean_active_coverage |   mean_turnover |
|:--------------------------------------------------|:------------------|-----------------------:|-------------------------------:|-----------------------------------:|-----------------------:|----------------:|
| participation_breadth_repair_under_hostile_trend  | ABSORPTION        |                    354 |                            153 |                                153 |               0.989380 |        0.039428 |
| participation_breadth_repair_under_hostile_trend  | PROPAGATION       |                    230 |                             41 |                                 41 |               0.989603 |        0.010865 |
| participation_breadth_repair_under_hostile_trend  | NORMALIZATION     |                    293 |                             45 |                                 45 |               0.990961 |        0.018771 |
| participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS |                    123 |                             34 |                                 34 |               0.992686 |        0.030030 |
| participation_breadth_repair_under_hostile_trend  | NEUTRAL           |                   1098 |                             25 |                                 25 |               0.959371 |        0.002343 |
| participation_liquidity_state_shift_20_60         | ABSORPTION        |                    354 |                            347 |                                347 |               0.988943 |        0.243820 |
| participation_liquidity_state_shift_20_60         | PROPAGATION       |                    230 |                            230 |                                230 |               0.989240 |        0.219316 |
| participation_liquidity_state_shift_20_60         | NORMALIZATION     |                    293 |                            292 |                                292 |               0.990547 |        0.212594 |
| participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS |                    123 |                            119 |                                119 |               0.992023 |        0.220615 |
| participation_liquidity_state_shift_20_60         | NEUTRAL           |                   1098 |                           1051 |                               1051 |               0.950749 |        0.207024 |
| volatility_compression_after_stress_stabilization | ABSORPTION        |                    354 |                            135 |                                135 |               0.989167 |        0.043154 |
| volatility_compression_after_stress_stabilization | PROPAGATION       |                    230 |                             13 |                                 13 |               0.989358 |        0.014199 |
| volatility_compression_after_stress_stabilization | NORMALIZATION     |                    293 |                             78 |                                 78 |               0.990632 |        0.026431 |
| volatility_compression_after_stress_stabilization | UNRESOLVED_STRESS |                    123 |                             39 |                                 39 |               0.992227 |        0.049590 |
| volatility_compression_after_stress_stabilization | NEUTRAL           |                   1098 |                            118 |                                118 |               0.945892 |        0.012308 |

## Interpretation

The detector appears useful only if state slices repeatedly explain changing candidate behavior while maintaining adequate samples. Strong state IC differences are attribution evidence, not promotion evidence. Thin slices, especially for sparse candidates, should be treated as provisional.

## Recommendation

Keep this as a research-only attribution artifact. If the state-conditioned relationships remain stable in a future monitoring pass, the next appropriate step is a formal conditional validation design for attribution use, not production routing or alpha promotion.

## Artifacts

- `candidate_by_state_attribution.csv`
- `conditional_ic_summary.csv`
- `conditional_return_summary.csv`
- `drawdown_clustering.csv`
- `state_conditioned_rankings.csv`
- `state_transition_interaction.csv`
- `sample_size_sanity.csv`
- `window_stability.csv`
- `stress_overlap_by_state.csv`
- `detector_usefulness_summary.csv`
- `daily_ic_by_candidate.csv`
- `daily_long_short_by_candidate.csv`
- `manifest.json`
