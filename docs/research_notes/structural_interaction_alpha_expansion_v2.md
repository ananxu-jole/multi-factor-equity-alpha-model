# Structural Interaction Alpha Expansion v2

Date: 2026-05-22

Run id: `structural_interaction_alpha_expansion_v2`

Status: RESEARCH_ONLY_ALPHA_EXPANSION

## Research-Only Guardrail

This is a research-only structural interaction alpha discovery batch. It does not modify detector code or labels, register production signals, mutate survivor/watchlist state, loosen gates or thresholds, change schemas/governance, or route anything into portfolio, ML, blending, or optimization workflows.

The Transition-State Detector branch was not modified and detector states were not used as inputs.

## Objective

Test whether smoother, less brittle structural interaction formulations can capture medium-horizon behavior better than hard-threshold activation signals.

## Executive Takeaway

Candidates tested: `8`
Status counts: `{"CONDITIONAL_ONLY_RESEARCH": 1, "REJECT_RESEARCH": 7}`

## Candidate Set

| signal_name                                            | family                                      | mechanism_thesis                                                                                                                                  | expected_horizon   | run_id                                    | research_status   |
|:-------------------------------------------------------|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------|:------------------------------------------|:------------------|
| relative_participation_quality_instability_adjusted_20 | relative_participation_quality              | Persistent participation quality that improves relative to realized instability may capture structural repair without hard activation thresholds. | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| asymmetric_stabilization_balance_20                    | asymmetric_stabilization                    | Uneven downside pressure can be useful only when upside participation and range stabilization balance it rather than chase it.                    | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| structural_recovery_efficiency_15_20                   | structural_recovery_efficiency              | Efficient recovery converts instability into close-quality improvement with less range and liquidity waste.                                       | h15-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| dispersion_constrained_recovery_quality_20             | dispersion_constrained_recovery             | Recovery quality should be more durable when it occurs without broad speculative dispersion expansion.                                            | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| participation_persistence_quality_20                   | participation_persistence_quality           | Repeated moderate participation alignment with stable turnover may be more robust than a single intense participation event.                      | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| volatility_structure_curvature_stabilization_20        | volatility_structure_curvature              | A favorable short/intermediate/long volatility curve may identify stabilization shape, not merely level or spike decay.                           | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| liquidity_adjusted_volatility_normalization_20         | liquidity_adjusted_volatility_normalization | Volatility normalization is more meaningful when confirmed by liquidity quality rather than raw volume intensity.                                 | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |
| moderate_interaction_persistence_score_20              | interaction_persistence                     | Repeated moderate alignment across stabilization, participation, and quality may outperform brittle extreme activation.                           | h10-h20            | structural_interaction_alpha_expansion_v2 | RESEARCH_ONLY     |

## Multi-Horizon IC

| signal_name                                            |   horizon |      mean_ic |   abs_mean_ic |        ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-------------------------------------------------------|----------:|-------------:|--------------:|-------------:|-------------------:|----------:|:------------------|
| relative_participation_quality_instability_adjusted_20 |         1 | -0.000468024 |   0.000468024 | -0.00598868  |           0.499264 |      2037 | False             |
| asymmetric_stabilization_balance_20                    |         1 |  6.05531e-05 |   6.05531e-05 |  0.000689581 |           0.490427 |      2037 | False             |
| structural_recovery_efficiency_15_20                   |         1 | -0.00109064  |   0.00109064  | -0.0144221   |           0.491409 |      2037 | False             |
| dispersion_constrained_recovery_quality_20             |         1 | -0.00100613  |   0.00100613  | -0.0116487   |           0.499755 |      2037 | False             |
| participation_persistence_quality_20                   |         1 | -0.000716422 |   0.000716422 | -0.00952023  |           0.499755 |      2037 | False             |
| volatility_structure_curvature_stabilization_20        |         1 | -0.00100361  |   0.00100361  | -0.0139613   |           0.5027   |      2037 | False             |
| liquidity_adjusted_volatility_normalization_20         |         1 | -0.000751214 |   0.000751214 | -0.0104346   |           0.488463 |      2037 | False             |
| moderate_interaction_persistence_score_20              |         1 | -0.000877906 |   0.000877906 | -0.0113465   |           0.503191 |      2037 | False             |
| relative_participation_quality_instability_adjusted_20 |         5 | -0.00252312  |   0.00252312  | -0.0324526   |           0.478111 |      2033 | True              |
| asymmetric_stabilization_balance_20                    |         5 |  0.00147492  |   0.00147492  |  0.0172737   |           0.490408 |      2033 | False             |
| structural_recovery_efficiency_15_20                   |         5 | -0.00322113  |   0.00322113  | -0.0461648   |           0.482538 |      2033 | False             |
| dispersion_constrained_recovery_quality_20             |         5 | -0.00287837  |   0.00287837  | -0.0347411   |           0.481062 |      2033 | False             |
| participation_persistence_quality_20                   |         5 | -0.000271221 |   0.000271221 | -0.0036751   |           0.49336  |      2033 | False             |
| volatility_structure_curvature_stabilization_20        |         5 |  0.000792906 |   0.000792906 |  0.0108155   |           0.515002 |      2033 | False             |
| liquidity_adjusted_volatility_normalization_20         |         5 | -0.00157713  |   0.00157713  | -0.0224252   |           0.495327 |      2033 | False             |
| moderate_interaction_persistence_score_20              |         5 | -0.00232819  |   0.00232819  | -0.0298941   |           0.4909   |      2033 | True              |
| relative_participation_quality_instability_adjusted_20 |        10 | -0.00126028  |   0.00126028  | -0.0164301   |           0.487673 |      2028 | False             |
| asymmetric_stabilization_balance_20                    |        10 |  0.00361907  |   0.00361907  |  0.0445532   |           0.511341 |      2028 | True              |
| structural_recovery_efficiency_15_20                   |        10 | -0.00517688  |   0.00517688  | -0.0763627   |           0.482742 |      2028 | False             |
| dispersion_constrained_recovery_quality_20             |        10 | -0.00520583  |   0.00520583  | -0.0676863   |           0.468935 |      2028 | True              |
| participation_persistence_quality_20                   |        10 |  0.00152511  |   0.00152511  |  0.0212285   |           0.50789  |      2028 | False             |
| volatility_structure_curvature_stabilization_20        |        10 |  0.0031138   |   0.0031138   |  0.0434595   |           0.533037 |      2028 | False             |
| liquidity_adjusted_volatility_normalization_20         |        10 | -0.00164181  |   0.00164181  | -0.0248209   |           0.502959 |      2028 | False             |
| moderate_interaction_persistence_score_20              |        10 | -0.000745832 |   0.000745832 | -0.0101171   |           0.484221 |      2028 | False             |
| relative_participation_quality_instability_adjusted_20 |        20 | -0.000395207 |   0.000395207 | -0.00530114  |           0.473241 |      2018 | False             |
| asymmetric_stabilization_balance_20                    |        20 |  0.00344885  |   0.00344885  |  0.0456686   |           0.529732 |      2018 | False             |
| structural_recovery_efficiency_15_20                   |        20 | -0.00536366  |   0.00536366  | -0.0795206   |           0.478692 |      2018 | True              |
| dispersion_constrained_recovery_quality_20             |        20 | -0.00440447  |   0.00440447  | -0.060045    |           0.484638 |      2018 | False             |
| participation_persistence_quality_20                   |        20 |  0.00351897  |   0.00351897  |  0.0485184   |           0.511397 |      2018 | True              |
| volatility_structure_curvature_stabilization_20        |        20 |  0.00606553  |   0.00606553  |  0.0919763   |           0.576313 |      2018 | True              |
| liquidity_adjusted_volatility_normalization_20         |        20 | -0.00297214  |   0.00297214  | -0.0468273   |           0.482161 |      2018 | True              |
| moderate_interaction_persistence_score_20              |        20 |  0.00135379  |   0.00135379  |  0.0194237   |           0.511397 |      2018 | False             |

## h10 Ranking

| signal_name                                            |      mean_ic |   positive_ic_rate |   n_dates |
|:-------------------------------------------------------|-------------:|-------------------:|----------:|
| asymmetric_stabilization_balance_20                    |  0.00361907  |           0.511341 |      2028 |
| volatility_structure_curvature_stabilization_20        |  0.0031138   |           0.533037 |      2028 |
| participation_persistence_quality_20                   |  0.00152511  |           0.50789  |      2028 |
| moderate_interaction_persistence_score_20              | -0.000745832 |           0.484221 |      2028 |
| relative_participation_quality_instability_adjusted_20 | -0.00126028  |           0.487673 |      2028 |
| liquidity_adjusted_volatility_normalization_20         | -0.00164181  |           0.502959 |      2028 |
| structural_recovery_efficiency_15_20                   | -0.00517688  |           0.482742 |      2028 |
| dispersion_constrained_recovery_quality_20             | -0.00520583  |           0.468935 |      2028 |

## h20 Ranking

| signal_name                                            |      mean_ic |   positive_ic_rate |   n_dates |
|:-------------------------------------------------------|-------------:|-------------------:|----------:|
| volatility_structure_curvature_stabilization_20        |  0.00606553  |           0.576313 |      2018 |
| participation_persistence_quality_20                   |  0.00351897  |           0.511397 |      2018 |
| asymmetric_stabilization_balance_20                    |  0.00344885  |           0.529732 |      2018 |
| moderate_interaction_persistence_score_20              |  0.00135379  |           0.511397 |      2018 |
| relative_participation_quality_instability_adjusted_20 | -0.000395207 |           0.473241 |      2018 |
| liquidity_adjusted_volatility_normalization_20         | -0.00297214  |           0.482161 |      2018 |
| dispersion_constrained_recovery_quality_20             | -0.00440447  |           0.484638 |      2018 |
| structural_recovery_efficiency_15_20                   | -0.00536366  |           0.478692 |      2018 |

## WFV-Style Diagnostics

| signal_name                                            |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| relative_participation_quality_instability_adjusted_20 |         5 |           4 |              -0.00252034 |              -0.680546 |          0.25 |               0.75 |               0.572851 |
| moderate_interaction_persistence_score_20              |         5 |           4 |              -0.00232412 |              -0.363527 |          0.5  |               0.5  |               0.42574  |
| asymmetric_stabilization_balance_20                    |        10 |           4 |               0.00361907 |               0.645419 |          0.5  |               0.5  |               0.466836 |
| dispersion_constrained_recovery_quality_20             |        10 |           4 |              -0.00520583 |              -1.02132  |          0.25 |               0.75 |               0.442767 |
| structural_recovery_efficiency_15_20                   |        20 |           4 |              -0.00535715 |              -0.628793 |          0.25 |               0.75 |               0.498463 |
| participation_persistence_quality_20                   |        20 |           4 |               0.00351391 |               0.404194 |          0.5  |               0.5  |               0.66034  |
| volatility_structure_curvature_stabilization_20        |        20 |           4 |               0.00606703 |               2.19017  |          1    |               1    |               0.442826 |
| liquidity_adjusted_volatility_normalization_20         |        20 |           4 |              -0.00296689 |              -0.366721 |          0.25 |               0.75 |               0.338377 |

## Active Coverage

| signal_name                                            |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-------------------------------------------------------|---------------:|--------------------:|-------------------------:|-----------------------:|
| relative_participation_quality_instability_adjusted_20 |           2038 |            0.971401 |                        1 |               0.987949 |
| asymmetric_stabilization_balance_20                    |           2038 |            0.971401 |                        1 |               0.98763  |
| structural_recovery_efficiency_15_20                   |           2038 |            0.971401 |                        1 |               0.98763  |
| dispersion_constrained_recovery_quality_20             |           2038 |            0.971401 |                        1 |               0.987949 |
| participation_persistence_quality_20                   |           2038 |            0.971401 |                        1 |               0.987949 |
| volatility_structure_curvature_stabilization_20        |           2038 |            0.971401 |                        1 |               0.987949 |
| liquidity_adjusted_volatility_normalization_20         |           2038 |            0.971401 |                        1 |               0.987949 |
| moderate_interaction_persistence_score_20              |           2038 |            0.971401 |                        1 |               0.987949 |

## Interaction Component Decomposition

| signal_name                                            |   horizon |   final_mean_ic |   best_component_mean_ic |   interaction_ic_lift_vs_best_component | dominant_component           |   dominant_component_corr | interaction_decomposition_label   | component_corr_detail                                                                                                                        | component_ic_detail                                                                                                                                         |
|:-------------------------------------------------------|----------:|----------------:|-------------------------:|----------------------------------------:|:-----------------------------|--------------------------:|:----------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| relative_participation_quality_instability_adjusted_20 |         5 |     -0.00252312 |             -0.000645273 |                             -0.00187785 | participation_vs_instability |                  0.414758 | mixed_or_inconclusive_interaction | participation_vs_instability:0.415; participation_improvement:-0.042; vol_normalization:0.101; turnover_stability:0.012; low_extension:0.099 | participation_vs_instability:-0.00930; participation_improvement:-0.00754; vol_normalization:-0.00266; turnover_stability:-0.00065; low_extension:-0.00734  |
| asymmetric_stabilization_balance_20                    |        10 |      0.00361907 |              0.015404    |                             -0.0117849  | vol_normalization            |                  0.082711 | single_component_ic_dominates     | downside_pressure:-0.065; upside_repair:-0.017; vol_normalization:0.083; low_short_extension:0.007; asymmetric_balance:0.038                 | downside_pressure:0.01540; upside_repair:-0.00904; vol_normalization:-0.00641; low_short_extension:-0.00857; asymmetric_balance:-0.01047                    |
| structural_recovery_efficiency_15_20                   |        20 |     -0.00536366 |             -0.00420643  |                             -0.00115723 | liquidity_quality            |                  0.513923 | mixed_or_inconclusive_interaction | recovery_efficiency:0.003; close_quality_persistence:0.036; liquidity_quality:0.514; range_normalization:0.109; low_extension:0.049          | recovery_efficiency:-0.00989; close_quality_persistence:-0.00421; liquidity_quality:-0.01415; range_normalization:-0.00694; low_extension:-0.01224          |
| dispersion_constrained_recovery_quality_20             |        10 |     -0.00520583 |             -0.00866117  |                              0.00345533 | liquidity_quality            |                  0.451835 | true_interaction_behavior         | relative_resilience:0.097; close_quality_persistence:0.010; liquidity_quality:0.452                                                          | relative_resilience:-0.01098; close_quality_persistence:-0.00866; liquidity_quality:-0.00923                                                                |
| participation_persistence_quality_20                   |        20 |      0.00351897 |             -0.00199107  |                              0.00551003 | participation_persistence    |                  0.176536 | true_interaction_behavior         | participation_quality:0.099; participation_persistence:0.177; turnover_stability:0.026; close_quality_persistence:0.031; low_extension:0.110 | participation_quality:-0.00335; participation_persistence:-0.00478; turnover_stability:-0.00199; close_quality_persistence:-0.00421; low_extension:-0.01224 |
| volatility_structure_curvature_stabilization_20        |        20 |      0.00606553 |             -0.00268853  |                              0.00875406 | range_curvature              |                  0.205317 | true_interaction_behavior         | vol_curvature:0.197; range_curvature:0.205; instability_improvement:-0.125; close_quality_persistence:0.005; low_extension:0.044             | vol_curvature:-0.00269; range_curvature:-0.00444; instability_improvement:-0.00393; close_quality_persistence:-0.00421; low_extension:-0.01224              |
| liquidity_adjusted_volatility_normalization_20         |        20 |     -0.00297214 |             -0.000641975 |                             -0.00233017 | liquidity_quality            |                  0.260339 | mixed_or_inconclusive_interaction | vol_normalization:0.168; liquidity_quality:0.260; volume_intensity_penalty:0.083; turnover_stability:0.049; low_extension:0.038              | vol_normalization:-0.00721; liquidity_quality:-0.01415; volume_intensity_penalty:-0.00064; turnover_stability:-0.00199; low_extension:-0.01224              |
| moderate_interaction_persistence_score_20              |         5 |     -0.00232819 |             -0.00733968  |                              0.00501149 | interaction_persistence      |                  0.401188 | true_interaction_behavior         | interaction_alignment:0.187; interaction_persistence:0.401; moderate_alignment:0.192; low_gap_noise:0.159; low_extension:0.193               | interaction_alignment:-0.00883; interaction_persistence:-0.01036; moderate_alignment:-0.00795; low_gap_noise:-0.01199; low_extension:-0.00734               |

## Interaction Persistence

| signal_name                                            |   horizon |   raw_mean_ic |   persistent_mean_ic |   persistence_ic_delta |   mean_persistent_coverage |   p95_persistent_coverage |   persistence_coverage_stability | interaction_persistence_label   |
|:-------------------------------------------------------|----------:|--------------:|---------------------:|-----------------------:|---------------------------:|--------------------------:|---------------------------------:|:--------------------------------|
| relative_participation_quality_instability_adjusted_20 |         5 |   -0.0106767  |          -0.0129422  |           -0.00226547  |                  0.133029  |                 0.161088  |                       0.0136993  | persistence_weakens_structure   |
| asymmetric_stabilization_balance_20                    |        10 |   -0.0108795  |          -0.0141509  |           -0.0032714   |                  0.0571694 |                 0.0920502 |                       0.0153531  | persistence_weakens_structure   |
| structural_recovery_efficiency_15_20                   |        20 |   -0.0180716  |          -0.0185362  |           -0.000464596 |                  0.18046   |                 0.200837  |                       0.00935565 | persistent_structure_supported  |
| dispersion_constrained_recovery_quality_20             |        10 |   -0.0117253  |          -0.0147799  |           -0.00305467  |                  0.158207  |                 0.190377  |                       0.0141421  | persistence_weakens_structure   |
| participation_persistence_quality_20                   |        20 |   -0.00954634 |          -0.0121161  |           -0.00256973  |                  0.103071  |                 0.132113  |                       0.0137598  | persistence_weakens_structure   |
| volatility_structure_curvature_stabilization_20        |        20 |   -0.00994997 |          -0.00726127 |            0.00268871  |                  0.128412  |                 0.154812  |                       0.0127782  | persistent_structure_supported  |
| liquidity_adjusted_volatility_normalization_20         |        20 |   -0.0159507  |          -0.0192443  |           -0.00329357  |                  0.133962  |                 0.158996  |                       0.0120549  | persistence_weakens_structure   |
| moderate_interaction_persistence_score_20              |         5 |   -0.00651463 |          -0.00944949 |           -0.00293486  |                  0.14604   |                 0.177824  |                       0.014944   | persistence_weakens_structure   |

## Smoothness / Activation Brittleness

| signal_name                                            |   horizon |   continuous_raw_ic |   focused_subset_ic |   subset_ic_delta_vs_continuous |   mean_raw_daily_coverage |   mean_focused_daily_coverage |   mean_signal_abruptness | smoothness_brittleness_label   |
|:-------------------------------------------------------|----------:|--------------------:|--------------------:|--------------------------------:|--------------------------:|------------------------------:|-------------------------:|:-------------------------------|
| relative_participation_quality_instability_adjusted_20 |         5 |         -0.0106767  |         -0.00327852 |                     0.00739819  |                  0.982613 |                      0.492981 |                 0.284139 | continuous_behavior_stable     |
| asymmetric_stabilization_balance_20                    |        10 |         -0.0108795  |         -0.00524703 |                     0.0056325   |                  0.984636 |                      0.49353  |                 0.316788 | continuous_behavior_stable     |
| structural_recovery_efficiency_15_20                   |        20 |         -0.0180716  |         -0.0104014  |                     0.00767017  |                  0.976079 |                      0.489603 |                 0.11974  | continuous_behavior_stable     |
| dispersion_constrained_recovery_quality_20             |        10 |         -0.0117253  |         -0.00904921 |                     0.00267606  |                  0.988878 |                      0.443711 |                 0.156189 | continuous_behavior_stable     |
| participation_persistence_quality_20                   |        20 |         -0.00954634 |         -0.00912827 |                     0.000418063 |                  0.983149 |                      0.493248 |                 0.380202 | continuous_behavior_stable     |
| volatility_structure_curvature_stabilization_20        |        20 |         -0.00994997 |         -0.00457833 |                     0.00537164  |                  0.982607 |                      0.492975 |                 0.225441 | continuous_behavior_stable     |
| liquidity_adjusted_volatility_normalization_20         |        20 |         -0.0159507  |         -0.00787397 |                     0.00807673  |                  0.982604 |                      0.492972 |                 0.274318 | continuous_behavior_stable     |
| moderate_interaction_persistence_score_20              |         5 |         -0.00651463 |         -0.0102375  |                    -0.00372286  |                  0.98261  |                      0.416009 |                 0.164747 | continuous_behavior_stable     |

## Component Balance

| signal_name                                            |   component_count |   component_mean_dominance_ratio |   component_mean_abs_corr |   component_cv_mean | component_balance_label   |
|:-------------------------------------------------------|------------------:|---------------------------------:|--------------------------:|--------------------:|:--------------------------|
| relative_participation_quality_instability_adjusted_20 |                 5 |                          1.01284 |                 0.100747  |             269.481 | balanced_interaction      |
| asymmetric_stabilization_balance_20                    |                 5 |                          1.00094 |                 0.400808  |             260.667 | balanced_interaction      |
| structural_recovery_efficiency_15_20                   |                 5 |                          1.00047 |                 0.0845428 |             263.366 | balanced_interaction      |
| dispersion_constrained_recovery_quality_20             |                 5 |                          1.0124  |                 0.154336  |             160.032 | balanced_interaction      |
| participation_persistence_quality_20                   |                 5 |                          1.01221 |                 0.255652  |             269.737 | balanced_interaction      |
| volatility_structure_curvature_stabilization_20        |                 5 |                          1.00109 |                 0.155537  |             269.025 | balanced_interaction      |
| liquidity_adjusted_volatility_normalization_20         |                 5 |                          1.00086 |                 0.0831422 |             269.059 | balanced_interaction      |
| moderate_interaction_persistence_score_20              |                 5 |                          1.00008 |                 0.493583  |             265.627 | balanced_interaction      |

## Fragility / Concentration

| signal_name                                            |   horizon |   full_mean_ic |   crisis_mean_ic |   non_crisis_mean_ic |   crisis_positive_ic_rate |   non_crisis_positive_ic_rate |   crisis_valid_dates |   non_crisis_valid_dates |   crisis_positive_contribution_share |   one_window_dominance | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | regime_exclusivity_flag   |
|:-------------------------------------------------------|----------:|---------------:|-----------------:|---------------------:|--------------------------:|------------------------------:|---------------------:|-------------------------:|-------------------------------------:|-----------------------:|:------------------------------|:----------------------------|:--------------------------------|:--------------------------|
| relative_participation_quality_instability_adjusted_20 |         5 |    -0.00252312 |      -0.00100569 |          -0.00334809 |                  0.484637 |                      0.474563 |                  716 |                     1317 |                             0.358613 |               0.572851 | False                         | False                       | False                           | False                     |
| moderate_interaction_persistence_score_20              |         5 |    -0.00232819 |       0.00172883 |          -0.00453383 |                  0.506983 |                      0.482156 |                  716 |                     1317 |                             0.400037 |               0.42574  | False                         | False                       | False                           | False                     |
| asymmetric_stabilization_balance_20                    |        10 |     0.00361907 |       0.00245177 |           0.00425472 |                  0.506294 |                      0.51409  |                  715 |                     1313 |                             0.336962 |               0.466836 | False                         | False                       | False                           | False                     |
| dispersion_constrained_recovery_quality_20             |        10 |    -0.00520583 |       0.00586988 |          -0.0112372  |                  0.532867 |                      0.43412  |                  715 |                     1313 |                             0.466769 |               0.442767 | False                         | False                       | False                           | False                     |
| structural_recovery_efficiency_15_20                   |        20 |    -0.00536366 |      -0.00443096 |          -0.00586446 |                  0.504965 |                      0.464585 |                  705 |                     1313 |                             0.347033 |               0.498463 | False                         | False                       | False                           | False                     |
| participation_persistence_quality_20                   |        20 |     0.00351897 |       0.01318    |          -0.00166842 |                  0.563121 |                      0.483625 |                  705 |                     1313 |                             0.414151 |               0.66034  | True                          | False                       | True                            | True                      |
| volatility_structure_curvature_stabilization_20        |        20 |     0.00606553 |       0.00436154 |           0.00698047 |                  0.541844 |                      0.594821 |                  705 |                     1313 |                             0.367515 |               0.442826 | False                         | False                       | False                           | False                     |
| liquidity_adjusted_volatility_normalization_20         |        20 |    -0.00297214 |      -0.00457612 |          -0.00211091 |                  0.492199 |                      0.476771 |                  705 |                     1313 |                             0.347107 |               0.338377 | False                         | False                       | False                           | False                     |

## Similarity / Redundancy

| signal_name                                            | top_comparison                           |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:-------------------------------------------------------|:-----------------------------------------|------------------------:|---------------------:|--------------------:|--------------------:|
| asymmetric_stabilization_balance_20                    | v2_vol_compression_range_expansion_20_60 |                0.166677 |            0.0745836 |           0.0632204 |          0.0128786  |
| dispersion_constrained_recovery_quality_20             | current_pool_vol_of_vol_20               |                0.124185 |            0.0644233 |           0.0428873 |          0.037642   |
| liquidity_adjusted_volatility_normalization_20         | v2_vol_compression_range_expansion_20_60 |                0.180725 |            0.0305378 |           0.037142  |          0.00588802 |
| moderate_interaction_persistence_score_20              | v2_vol_compression_range_expansion_20_60 |                0.298289 |            0.12053   |           0.120349  |          0.07906    |
| participation_persistence_quality_20                   | v2_vol_compression_range_expansion_20_60 |                0.175924 |            0.0789968 |           0.0391016 |          0.00583791 |
| relative_participation_quality_instability_adjusted_20 | v2_vol_compression_range_expansion_20_60 |                0.35526  |            0.113867  |           0.0311527 |          0.0133309  |
| structural_recovery_efficiency_15_20                   | current_pool_vol_of_vol_20               |                0.109958 |            0.0714948 |           0.030696  |          0.034258   |
| volatility_structure_curvature_stabilization_20        | v2_vol_compression_range_expansion_20_60 |                0.31305  |            0.112149  |           0.0201798 |          0.00378143 |

## Candidate Decisions

| signal_name                                            | status                    |   best_horizon |     mean_ic |   h10_mean_ic |   h20_mean_ic |   positive_ic_rate |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr | interaction_decomposition_label   | interaction_persistence_label   | smoothness_brittleness_label   | component_balance_label   | review_issues                                                                                                                                                                                                                                             |
|:-------------------------------------------------------|:--------------------------|---------------:|------------:|--------------:|--------------:|-------------------:|---------------------:|--------------------:|--------------------:|:----------------------------------|:--------------------------------|:-------------------------------|:--------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| volatility_structure_curvature_stabilization_20        | CONDITIONAL_ONLY_RESEARCH |             20 |  0.00606553 |   0.0031138   |   0.00606553  |           0.576313 |            0.112149  |           0.0201798 |          0.00378143 | true_interaction_behavior         | persistent_structure_supported  | continuous_behavior_stable     | balanced_interaction      | weak_best_horizon_ic; weak_medium_horizon_ic; activation_too_broad                                                                                                                                                                                        |
| participation_persistence_quality_20                   | REJECT_RESEARCH           |             20 |  0.00351897 |   0.00152511  |   0.00351897  |           0.511397 |            0.0789968 |           0.0391016 |          0.00583791 | true_interaction_behavior         | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; one_window_concentration; activation_too_broad; interaction_persistence_weak; stress_only_dependency; one_window_concentration_flag |
| asymmetric_stabilization_balance_20                    | REJECT_RESEARCH           |             10 |  0.00361907 |   0.00361907  |   0.00344885  |           0.511341 |            0.0745836 |           0.0632204 |          0.0128786  | single_component_ic_dominates     | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; activation_too_broad; interaction_not_preserved; interaction_persistence_weak                                                       |
| moderate_interaction_persistence_score_20              | REJECT_RESEARCH           |              5 | -0.00232819 |  -0.000745832 |   0.00135379  |           0.4909   |            0.12053   |           0.120349  |          0.07906    | true_interaction_behavior         | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | direction_mismatch; short_horizon_led; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; activation_too_broad; interaction_persistence_weak                                           |
| relative_participation_quality_instability_adjusted_20 | REJECT_RESEARCH           |              5 | -0.00252312 |  -0.00126028  |  -0.000395207 |           0.478111 |            0.113867  |           0.0311527 |          0.0133309  | mixed_or_inconclusive_interaction | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | direction_mismatch; short_horizon_led; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; activation_too_broad; interaction_not_preserved; interaction_persistence_weak                                           |
| liquidity_adjusted_volatility_normalization_20         | REJECT_RESEARCH           |             20 | -0.00297214 |  -0.00164181  |  -0.00297214  |           0.482161 |            0.0305378 |           0.037142  |          0.00588802 | mixed_or_inconclusive_interaction | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; activation_too_broad; interaction_not_preserved; interaction_persistence_weak                                                              |
| dispersion_constrained_recovery_quality_20             | REJECT_RESEARCH           |             10 | -0.00520583 |  -0.00520583  |  -0.00440447  |           0.468935 |            0.0644233 |           0.0428873 |          0.037642   | true_interaction_behavior         | persistence_weakens_structure   | continuous_behavior_stable     | balanced_interaction      | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; activation_too_broad; interaction_persistence_weak                                                                                         |
| structural_recovery_efficiency_15_20                   | REJECT_RESEARCH           |             20 | -0.00536366 |  -0.00517688  |  -0.00536366  |           0.478692 |            0.0714948 |           0.030696  |          0.034258   | mixed_or_inconclusive_interaction | persistent_structure_supported  | continuous_behavior_stable     | balanced_interaction      | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; activation_too_broad; interaction_not_preserved                                                                                            |

## Recommendation

Do not advance to validation. Preserve the evidence and review whether a narrower design thesis is warranted.

No production registration, survivor/watchlist mutation, detector modification, schema/gate/governance change, or portfolio/ML/blending/optimization route was made.
