# Structural Interaction Alpha Discovery Batch v1

Date: 2026-05-22

Run id: `structural_interaction_alpha_discovery_batch_v1`

Status: RESEARCH_ONLY_ALPHA_DISCOVERY_BATCH

## Research-Only Guardrail

This is a research-only structural interaction alpha discovery batch. It does not modify detector code or labels, register production signals, mutate survivor/watchlist state, loosen gates or thresholds, change schemas/governance, or route anything into portfolio, ML, blending, or optimization workflows.

The Transition-State Detector branch was not modified or used as a conditioning input.

## Executive Takeaway

This batch tested richer medium-horizon structural interaction candidates after pausing active Transition-State Detector work.

Candidates tested: `8`
Status counts: `{"CONDITIONAL_ONLY_RESEARCH": 3, "CONDITIONAL_REFINEMENT_CANDIDATE": 1, "REJECT_RESEARCH": 4}`

## Candidate Set

| signal_name                                       | family                             | mechanism_thesis                                                                                                                     | expected_horizon   | run_id                                          | research_status   |
|:--------------------------------------------------|:-----------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|:-------------------|:------------------------------------------------|:------------------|
| residual_stress_liquidity_quality_20              | residual_stress_liquidity          | Stock-specific residual stress that is being contained while non-price liquidity quality improves may identify healthier repair.     | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| volatility_participation_asymmetry_20             | volatility_participation_asymmetry | Improving stock-level up/down participation balance during stabilizing volatility may capture repair without market breadth cloning. | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| dispersion_resilient_relative_stability_20        | dispersion_resilience              | Stable relative behavior during elevated dispersion may identify robust cross-sectional resilience rather than price-rank momentum.  | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| turnover_exhaustion_quality_repair_10_20          | turnover_exhaustion_quality        | Turnover pressure that exhausts while range and close quality improve may separate repair from noisy reversal.                       | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| volatility_of_volatility_stabilization_20         | volatility_of_volatility           | Declining volatility-of-volatility after elevated instability may indicate durable stabilization beyond fast h5 shock absorption.    | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| compression_expansion_efficiency_asymmetry_15_30  | compression_expansion_asymmetry    | Efficient expansion after compression, with low gap noise and low overextension, may capture quality without raw breakout chasing.   | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| breadth_deterioration_resilience_20               | breadth_deterioration_resilience   | Names resilient during deteriorating breadth with stable liquidity and controlled extension may offer robust standalone behavior.    | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |
| conditional_exhaustion_vs_continuation_quality_20 | continuation_exhaustion_quality    | Quality continuation should be separated from exhaustion by combining trend efficiency, turnover decay, and range containment.       | h10-h20            | structural_interaction_alpha_discovery_batch_v1 | RESEARCH_ONLY     |

## Structural Quality And Active Coverage

| signal_name                                       |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| residual_stress_liquidity_quality_20              |     0.0406444 |     0.959356 |        0.971401 |        0.0347509 |       0.422262 |            0.675882 |                       35 |               0.988994 |
| volatility_participation_asymmetry_20             |     0.0419706 |     0.958029 |        0.971401 |        0.0471619 |       0.489108 |            0.971401 |                        1 |               0.986234 |
| dispersion_resilient_relative_stability_20        |     0.0403054 |     0.959695 |        0.971401 |        0.0306872 |       0.406818 |            0.604385 |                       45 |               0.989292 |
| turnover_exhaustion_quality_repair_10_20          |     0.0406444 |     0.959356 |        0.971401 |        0.0424154 |       0.556547 |            0.675882 |                       35 |               0.988994 |
| volatility_of_volatility_stabilization_20         |     0.0403054 |     0.959695 |        0.971401 |        0.0353751 |       0.427676 |            0.675882 |                       35 |               0.98923  |
| compression_expansion_efficiency_asymmetry_15_30  |     0.0406145 |     0.959386 |        0.971401 |        0.0445505 |       0.444285 |            0.971401 |                        1 |               0.98763  |
| breadth_deterioration_resilience_20               |     0.0405048 |     0.959495 |        0.971401 |        0.0417635 |       0.438469 |            0.681602 |                       82 |               0.988179 |
| conditional_exhaustion_vs_continuation_quality_20 |     0.0406444 |     0.959356 |        0.971401 |        0.0445635 |       0.452202 |            0.971401 |                        1 |               0.9876   |

## Multi-Horizon IC

| signal_name                                       |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| residual_stress_liquidity_quality_20              |         1 | -0.000805756 |   0.000805756 | -0.0114095  |           0.489982 |      1647 | False             |
| volatility_participation_asymmetry_20             |         1 | -0.00104673  |   0.00104673  | -0.0149496  |           0.505155 |      2037 | False             |
| dispersion_resilient_relative_stability_20        |         1 |  0.00158178  |   0.00158178  |  0.0173606  |           0.508287 |      1267 | False             |
| turnover_exhaustion_quality_repair_10_20          |         1 |  0.000417645 |   0.000417645 |  0.00610896 |           0.506704 |      1417 | False             |
| volatility_of_volatility_stabilization_20         |         1 |  0.000713468 |   0.000713468 |  0.00949445 |           0.507068 |      1627 | False             |
| compression_expansion_efficiency_asymmetry_15_30  |         1 | -0.000492437 |   0.000492437 | -0.00487161 |           0.500736 |      2037 | False             |
| breadth_deterioration_resilience_20               |         1 | -0.00238106  |   0.00238106  | -0.035355   |           0.485811 |      1480 | False             |
| conditional_exhaustion_vs_continuation_quality_20 |         1 | -0.00143081  |   0.00143081  | -0.0170135  |           0.4919   |      2037 | False             |
| residual_stress_liquidity_quality_20              |         5 | -0.00266954  |   0.00266954  | -0.0382498  |           0.471698 |      1643 | False             |
| volatility_participation_asymmetry_20             |         5 | -6.41591e-05 |   6.41591e-05 | -0.00093354 |           0.496311 |      2033 | False             |
| dispersion_resilient_relative_stability_20        |         5 |  0.0027425   |   0.0027425   |  0.0305442  |           0.505938 |      1263 | True              |
| turnover_exhaustion_quality_repair_10_20          |         5 | -0.000931224 |   0.000931224 | -0.0142648  |           0.493984 |      1413 | False             |
| volatility_of_volatility_stabilization_20         |         5 | -0.000229928 |   0.000229928 | -0.00306591 |           0.484904 |      1623 | False             |
| compression_expansion_efficiency_asymmetry_15_30  |         5 | -0.00335978  |   0.00335978  | -0.0331577  |           0.477619 |      2033 | False             |
| breadth_deterioration_resilience_20               |         5 | -0.00447769  |   0.00447769  | -0.068482   |           0.477703 |      1480 | False             |
| conditional_exhaustion_vs_continuation_quality_20 |         5 | -0.00460841  |   0.00460841  | -0.0562567  |           0.478603 |      2033 | False             |
| residual_stress_liquidity_quality_20              |        10 | -0.00380114  |   0.00380114  | -0.0569111  |           0.47558  |      1638 | False             |
| volatility_participation_asymmetry_20             |        10 |  0.0058405   |   0.0058405   |  0.0892576  |           0.550296 |      2028 | False             |
| dispersion_resilient_relative_stability_20        |        10 |  0.00164403  |   0.00164403  |  0.0197492  |           0.480922 |      1258 | False             |
| turnover_exhaustion_quality_repair_10_20          |        10 |  0.00168876  |   0.00168876  |  0.0264206  |           0.526278 |      1408 | False             |
| volatility_of_volatility_stabilization_20         |        10 | -0.000848852 |   0.000848852 | -0.0118541  |           0.476514 |      1618 | False             |
| compression_expansion_efficiency_asymmetry_15_30  |        10 | -0.00455073  |   0.00455073  | -0.0462027  |           0.462525 |      2028 | False             |
| breadth_deterioration_resilience_20               |        10 | -0.00635076  |   0.00635076  | -0.1018     |           0.443166 |      1478 | False             |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | -0.00487511  |   0.00487511  | -0.0605224  |           0.461538 |      2028 | True              |
| residual_stress_liquidity_quality_20              |        20 | -0.00467606  |   0.00467606  | -0.0744207  |           0.459459 |      1628 | True              |
| volatility_participation_asymmetry_20             |        20 |  0.012246    |   0.012246    |  0.193787   |           0.585233 |      2018 | True              |
| dispersion_resilient_relative_stability_20        |        20 |  0.00138528  |   0.00138528  |  0.0175112  |           0.500801 |      1248 | False             |
| turnover_exhaustion_quality_repair_10_20          |        20 |  0.00360062  |   0.00360062  |  0.0580824  |           0.534335 |      1398 | True              |
| volatility_of_volatility_stabilization_20         |        20 |  0.000853209 |   0.000853209 |  0.0133527  |           0.482587 |      1608 | True              |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | -0.00498369  |   0.00498369  | -0.052902   |           0.480674 |      2018 | True              |
| breadth_deterioration_resilience_20               |        20 | -0.00655933  |   0.00655933  | -0.109025   |           0.43188  |      1468 | True              |
| conditional_exhaustion_vs_continuation_quality_20 |        20 | -0.00478817  |   0.00478817  | -0.0603567  |           0.473736 |      2018 | False             |

## h10 Ranking

| signal_name                                       |      mean_ic |   positive_ic_rate |   n_dates |
|:--------------------------------------------------|-------------:|-------------------:|----------:|
| volatility_participation_asymmetry_20             |  0.0058405   |           0.550296 |      2028 |
| turnover_exhaustion_quality_repair_10_20          |  0.00168876  |           0.526278 |      1408 |
| dispersion_resilient_relative_stability_20        |  0.00164403  |           0.480922 |      1258 |
| volatility_of_volatility_stabilization_20         | -0.000848852 |           0.476514 |      1618 |
| residual_stress_liquidity_quality_20              | -0.00380114  |           0.47558  |      1638 |
| compression_expansion_efficiency_asymmetry_15_30  | -0.00455073  |           0.462525 |      2028 |
| conditional_exhaustion_vs_continuation_quality_20 | -0.00487511  |           0.461538 |      2028 |
| breadth_deterioration_resilience_20               | -0.00635076  |           0.443166 |      1478 |

## h20 Ranking

| signal_name                                       |      mean_ic |   positive_ic_rate |   n_dates |
|:--------------------------------------------------|-------------:|-------------------:|----------:|
| volatility_participation_asymmetry_20             |  0.012246    |           0.585233 |      2018 |
| turnover_exhaustion_quality_repair_10_20          |  0.00360062  |           0.534335 |      1398 |
| dispersion_resilient_relative_stability_20        |  0.00138528  |           0.500801 |      1248 |
| volatility_of_volatility_stabilization_20         |  0.000853209 |           0.482587 |      1608 |
| residual_stress_liquidity_quality_20              | -0.00467606  |           0.459459 |      1628 |
| conditional_exhaustion_vs_continuation_quality_20 | -0.00478817  |           0.473736 |      2018 |
| compression_expansion_efficiency_asymmetry_15_30  | -0.00498369  |           0.480674 |      2018 |
| breadth_deterioration_resilience_20               | -0.00655933  |           0.43188  |      1468 |

## WFV-Style Diagnostics

| signal_name                                       |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| dispersion_resilient_relative_stability_20        |         5 |           4 |              0.00273631  |               0.378242 |          0.5  |               0.5  |               0.461292 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 |           4 |             -0.00487511  |              -0.519506 |          0.25 |               0.75 |               0.457728 |
| residual_stress_liquidity_quality_20              |        20 |           4 |             -0.00467606  |              -1.0117   |          0.25 |               0.75 |               0.493628 |
| volatility_participation_asymmetry_20             |        20 |           4 |              0.0122394   |               1.18637  |          1    |               1    |               0.594737 |
| turnover_exhaustion_quality_repair_10_20          |        20 |           4 |              0.00359694  |               0.524045 |          0.5  |               0.5  |               0.664768 |
| volatility_of_volatility_stabilization_20         |        20 |           4 |              0.000853209 |               0.339231 |          0.75 |               0.75 |               0.708713 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 |           4 |             -0.00499074  |              -0.64623  |          0.5  |               0.5  |               0.571763 |
| breadth_deterioration_resilience_20               |        20 |           4 |             -0.00655933  |              -0.915966 |          0    |               1    |               0.721395 |

## Interaction Decomposition

| signal_name                                       |   horizon |   final_mean_ic |   best_component_mean_ic |   interaction_ic_lift_vs_best_component | dominant_component   |   dominant_component_corr | interaction_decomposition_label   | component_corr_detail                                                                                              | component_ic_detail                                                                                                              |
|:--------------------------------------------------|----------:|----------------:|-------------------------:|----------------------------------------:|:---------------------|--------------------------:|:----------------------------------|:-------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| residual_stress_liquidity_quality_20              |        20 |    -0.00467606  |              0.00408075  |                            -0.00875681  | liquidity_quality    |                  0.249166 | single_component_ic_dominates     | residual_stress:0.115; stress_containment:0.052; liquidity_quality:0.249; low_extension:0.079                      | residual_stress:0.00408; stress_containment:-0.00393; liquidity_quality:-0.01415; low_extension:-0.01224                         |
| volatility_participation_asymmetry_20             |        20 |     0.012246    |             -0.00418957  |                             0.0164356   | low_extension        |                  0.067746 | true_interaction_behavior         | volatility_stabilization:0.010; participation_asymmetry:0.067; close_support:0.002; low_extension:0.068            | volatility_stabilization:-0.00531; participation_asymmetry:-0.00419; close_support:-0.00798; low_extension:-0.01224              |
| dispersion_resilient_relative_stability_20        |         5 |     0.0027425   |              0.000571121 |                             0.00217138  | idio_stability       |                  0.335857 | true_interaction_behavior         | rank_stability:0.141; idio_stability:0.336; relative_resilience:0.116                                              | rank_stability:0.00057; idio_stability:-0.00754; relative_resilience:-0.00771                                                    |
| turnover_exhaustion_quality_repair_10_20          |        20 |     0.00360062  |             -0.000641975 |                             0.0042426   | turnover_decay       |                  0.126748 | true_interaction_behavior         | turnover_pressure:0.086; turnover_decay:0.127; range_repair:0.075; close_support:0.013; low_short_extension:0.033  | turnover_pressure:-0.00669; turnover_decay:-0.00064; range_repair:-0.00580; close_support:-0.00798; low_short_extension:-0.00835 |
| volatility_of_volatility_stabilization_20         |        20 |     0.000853209 |              0.00412549  |                            -0.00327228  | vov_decay            |                  0.130786 | single_component_ic_dominates     | vov_elevated:-0.026; vov_decay:0.131; rank_stability:0.092; low_extension:0.112                                    | vov_elevated:-0.00968; vov_decay:-0.00163; rank_stability:0.00413; low_extension:-0.01224                                        |
| compression_expansion_efficiency_asymmetry_15_30  |        20 |    -0.00498369  |              0.00243569  |                            -0.00741938  | low_gap_noise        |                  0.2629   | single_component_ic_dominates     | compression:0.261; expansion_efficiency:-0.001; close_confirmation:0.036; low_gap_noise:0.263; low_extension:0.149 | compression:0.00000; expansion_efficiency:0.00244; close_confirmation:0.00191; low_gap_noise:-0.03149; low_extension:-0.01224    |
| breadth_deterioration_resilience_20               |        20 |    -0.00655933  |             -0.00199107  |                            -0.00456826  | low_extension        |                  0.130254 | mixed_or_inconclusive_interaction | relative_resilience:0.119; liquidity_stability:0.019; low_extension:0.130                                          | relative_resilience:-0.01260; liquidity_stability:-0.00199; low_extension:-0.01224                                               |
| conditional_exhaustion_vs_continuation_quality_20 |        10 |    -0.00487511  |             -0.0039797   |                            -0.000895414 | low_extension        |                  0.186119 | mixed_or_inconclusive_interaction | continuation_quality:0.082; exhaustion_pressure_inverse:0.100; range_repair:0.008; low_extension:0.186             | continuation_quality:-0.01412; exhaustion_pressure_inverse:-0.00398; range_repair:-0.00681; low_extension:-0.01118               |

## Anti-Fragility / Concentration Diagnostics

| signal_name                                       |   horizon |   full_mean_ic |   crisis_mean_ic |   non_crisis_mean_ic |   crisis_positive_ic_rate |   non_crisis_positive_ic_rate |   crisis_valid_dates |   non_crisis_valid_dates |   crisis_positive_contribution_share |   one_window_dominance | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | regime_exclusivity_flag   |
|:--------------------------------------------------|----------:|---------------:|-----------------:|---------------------:|--------------------------:|------------------------------:|---------------------:|-------------------------:|-------------------------------------:|-----------------------:|:------------------------------|:----------------------------|:--------------------------------|:--------------------------|
| dispersion_resilient_relative_stability_20        |         5 |    0.0027425   |       0.0125137  |         -0.00359731  |                  0.529175 |                      0.490862 |                  497 |                      766 |                             0.480847 |               0.461292 | True                          | False                       | False                           | True                      |
| conditional_exhaustion_vs_continuation_quality_20 |        10 |   -0.00487511  |      -0.00411712 |         -0.00528788  |                  0.471329 |                      0.456207 |                  715 |                     1313 |                             0.397445 |               0.457728 | False                         | False                       | False                           | False                     |
| residual_stress_liquidity_quality_20              |        20 |   -0.00467606  |      -0.00787455 |         -0.00239334  |                  0.439528 |                      0.473684 |                  678 |                      950 |                             0.392886 |               0.493628 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20             |        20 |    0.012246    |       0.0120329  |          0.0123605   |                  0.577305 |                      0.58949  |                  705 |                     1313 |                             0.338334 |               0.594737 | False                         | False                       | False                           | False                     |
| turnover_exhaustion_quality_repair_10_20          |        20 |    0.00360062  |       0.0028731  |          0.00423102  |                  0.51926  |                      0.547397 |                  649 |                      749 |                             0.461952 |               0.664768 | False                         | False                       | True                            | False                     |
| volatility_of_volatility_stabilization_20         |        20 |    0.000853209 |       0.00160408 |          0.000309972 |                  0.487407 |                      0.4791   |                  675 |                      933 |                             0.434277 |               0.708713 | False                         | False                       | True                            | False                     |
| compression_expansion_efficiency_asymmetry_15_30  |        20 |   -0.00498369  |      -0.00865295 |         -0.00301352  |                  0.460993 |                      0.491241 |                  705 |                     1313 |                             0.339103 |               0.571763 | False                         | False                       | False                           | False                     |
| breadth_deterioration_resilience_20               |        20 |   -0.00655933  |      -0.00504693 |         -0.00760182  |                  0.407346 |                      0.448792 |                  599 |                      869 |                             0.405448 |               0.721395 | False                         | False                       | True                            | False                     |

## Orthogonality / Redundancy

| signal_name                                       | top_comparison                                      |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:--------------------------------------------------|:----------------------------------------------------|------------------------:|---------------------:|--------------------:|--------------------:|
| breadth_deterioration_resilience_20               | v2_vol_compression_range_expansion_20_60            |               0.148343  |            0.0617644 |           0.0275754 |          0.0105142  |
| compression_expansion_efficiency_asymmetry_15_30  | v2_vol_compression_range_expansion_20_60            |               0.383226  |            0.119882  |           0.0391446 |          0.0328893  |
| conditional_exhaustion_vs_continuation_quality_20 | v2_vol_compression_range_expansion_20_60            |               0.251196  |            0.122527  |           0.124768  |          0.0657169  |
| dispersion_resilient_relative_stability_20        | v2_vol_compression_range_expansion_20_60            |               0.309563  |            0.108704  |           0.0162368 |          0.0239738  |
| residual_stress_liquidity_quality_20              | current_pool_vol_of_vol_20                          |               0.0720021 |            0.0507946 |           0.0203173 |          0.0245853  |
| turnover_exhaustion_quality_repair_10_20          | inventory_participation_liquidity_state_shift_20_60 |               0.0411469 |            0.0411469 |           0.0119798 |          0.00302907 |
| volatility_of_volatility_stabilization_20         | v2_vol_compression_range_expansion_20_60            |               0.246835  |            0.0942491 |           0.014257  |          0.00735954 |
| volatility_participation_asymmetry_20             | v2_vol_compression_range_expansion_20_60            |               0.108306  |            0.0517503 |           0.0339055 |          0.00731049 |

## Stress / Regime Attribution

| signal_name                                       |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| volatility_participation_asymmetry_20             |        20 | recovery_phase           |       196 |  0.0183696   |  0.291192   |           0.658163 |
| volatility_participation_asymmetry_20             |        20 | volatility_spike         |       393 |  0.015609    |  0.243671   |           0.569975 |
| volatility_of_volatility_stabilization_20         |        20 | recovery_phase           |       152 |  0.0145997   |  0.207552   |           0.532895 |
| breadth_deterioration_resilience_20               |        20 | recovery_phase           |       112 |  0.0135748   |  0.189942   |           0.482143 |
| volatility_participation_asymmetry_20             |        20 | trend_transition         |       555 |  0.0123762   |  0.207255   |           0.603604 |
| dispersion_resilient_relative_stability_20        |         5 | weak_breadth             |       322 |  0.0109218   |  0.115221   |           0.524845 |
| volatility_participation_asymmetry_20             |        20 | high_dispersion_rotation |       570 |  0.0108637   |  0.177539   |           0.573684 |
| dispersion_resilient_relative_stability_20        |         5 | volatility_spike         |       362 |  0.010263    |  0.104933   |           0.516575 |
| turnover_exhaustion_quality_repair_10_20          |        20 | high_dispersion_rotation |       459 |  0.00679547  |  0.104008   |           0.570806 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | recovery_phase           |       196 |  0.00580012  |  0.0727019  |           0.464286 |
| turnover_exhaustion_quality_repair_10_20          |        20 | weak_breadth             |       455 |  0.00443982  |  0.0709845  |           0.536264 |
| dispersion_resilient_relative_stability_20        |         5 | drawdown_acceleration    |       232 |  0.00431169  |  0.0477004  |           0.49569  |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | volatility_spike         |       403 |  0.00423817  |  0.044365   |           0.511166 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | high_dispersion_rotation |       570 |  0.00365499  |  0.0398058  |           0.485965 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | recovery_phase           |       196 |  0.003502    |  0.0385514  |           0.47449  |
| breadth_deterioration_resilience_20               |        20 | volatility_spike         |       324 |  0.00342942  |  0.0557211  |           0.459877 |
| turnover_exhaustion_quality_repair_10_20          |        20 | volatility_spike         |       393 |  0.00304298  |  0.0478725  |           0.503817 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | high_dispersion_rotation |       574 |  0.00249879  |  0.0292995  |           0.506969 |
| dispersion_resilient_relative_stability_20        |         5 | high_dispersion_rotation |       495 |  0.00243906  |  0.0276072  |           0.505051 |
| volatility_of_volatility_stabilization_20         |        20 | volatility_spike         |       393 |  0.00207451  |  0.029602   |           0.450382 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | volatility_spike         |       393 |  0.00151635  |  0.0152948  |           0.534351 |
| volatility_of_volatility_stabilization_20         |        20 | high_dispersion_rotation |       505 |  0.0005651   |  0.00861648 |           0.459406 |
| turnover_exhaustion_quality_repair_10_20          |        20 | panic_liquidity_stress   |       187 | -0.000346935 | -0.0057337  |           0.524064 |
| volatility_of_volatility_stabilization_20         |        20 | trend_transition         |       514 | -0.00163988  | -0.026389   |           0.459144 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | trend_transition         |       565 | -0.00352084  | -0.0423128  |           0.481416 |
| breadth_deterioration_resilience_20               |        20 | panic_liquidity_stress   |       157 | -0.00542688  | -0.0953703  |           0.394904 |
| residual_stress_liquidity_quality_20              |        20 | volatility_spike         |       393 | -0.0079499   | -0.118552   |           0.447837 |
| residual_stress_liquidity_quality_20              |        20 | trend_transition         |       515 | -0.00892868  | -0.136326   |           0.469903 |
| breadth_deterioration_resilience_20               |        20 | trend_transition         |       405 | -0.00934279  | -0.160346   |           0.355556 |
| residual_stress_liquidity_quality_20              |        20 | high_dispersion_rotation |       505 | -0.00981396  | -0.147163   |           0.439604 |
| residual_stress_liquidity_quality_20              |        20 | weak_breadth             |       481 | -0.0123006   | -0.216584   |           0.417879 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | trend_transition         |       555 | -0.0131486   | -0.142958   |           0.428829 |

## Candidate State Attribution

| signal_name                                       |   horizon | state                    |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:-------------------------|----------:|------------:|------------:|-------------------:|
| volatility_participation_asymmetry_20             |        20 | RECOVERY_PHASE           |       196 |  0.0183696  |  0.291192   |           0.658163 |
| volatility_participation_asymmetry_20             |        20 | DISPERSION_ELEVATED      |      1238 |  0.0157663  |  0.25594    |           0.603393 |
| volatility_participation_asymmetry_20             |        20 | VOLATILITY_SPIKE         |       393 |  0.015609   |  0.243671   |           0.569975 |
| volatility_of_volatility_stabilization_20         |        20 | RECOVERY_PHASE           |       152 |  0.0145997  |  0.207552   |           0.532895 |
| breadth_deterioration_resilience_20               |        20 | RECOVERY_PHASE           |       112 |  0.0135748  |  0.189942   |           0.482143 |
| volatility_participation_asymmetry_20             |        20 | BREADTH_DETERIORATING    |       840 |  0.0129392  |  0.207268   |           0.590476 |
| dispersion_resilient_relative_stability_20        |         5 | BROAD_STRESS             |       497 |  0.0125137  |  0.127735   |           0.529175 |
| dispersion_resilient_relative_stability_20        |         5 | WEAK_BREADTH             |       322 |  0.0109218  |  0.115221   |           0.524845 |
| dispersion_resilient_relative_stability_20        |         5 | VOLATILITY_SPIKE         |       362 |  0.010263   |  0.104933   |           0.516575 |
| dispersion_resilient_relative_stability_20        |         5 | BREADTH_DETERIORATING    |       517 |  0.00999497 |  0.111795   |           0.539652 |
| turnover_exhaustion_quality_repair_10_20          |        20 | HIGH_DISPERSION_ROTATION |       459 |  0.00679547 |  0.104008   |           0.570806 |
| turnover_exhaustion_quality_repair_10_20          |        20 | DISPERSION_ELEVATED      |       885 |  0.00600408 |  0.0925216  |           0.551412 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | RECOVERY_PHASE           |       196 |  0.00580012 |  0.0727019  |           0.464286 |
| turnover_exhaustion_quality_repair_10_20          |        20 | WEAK_BREADTH             |       455 |  0.00443982 |  0.0709845  |           0.536264 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | VOLATILITY_SPIKE         |       403 |  0.00423817 |  0.044365   |           0.511166 |
| turnover_exhaustion_quality_repair_10_20          |        20 | BREADTH_DETERIORATING    |       586 |  0.00377354 |  0.0626478  |           0.517065 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | HIGH_DISPERSION_ROTATION |       570 |  0.00365499 |  0.0398058  |           0.485965 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | RECOVERY_PHASE           |       196 |  0.003502   |  0.0385514  |           0.47449  |
| breadth_deterioration_resilience_20               |        20 | VOLATILITY_SPIKE         |       324 |  0.00342942 |  0.0557211  |           0.459877 |
| volatility_of_volatility_stabilization_20         |        20 | DISPERSION_ELEVATED      |      1014 |  0.00325123 |  0.0500047  |           0.468442 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | HIGH_DISPERSION_ROTATION |       574 |  0.00249879 |  0.0292995  |           0.506969 |
| volatility_of_volatility_stabilization_20         |        20 | VOLATILITY_SPIKE         |       393 |  0.00207451 |  0.029602   |           0.450382 |
| volatility_of_volatility_stabilization_20         |        20 | RECENT_STRESS            |      1354 |  0.00161564 |  0.0239277  |           0.493353 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | VOLATILITY_SPIKE         |       393 |  0.00151635 |  0.0152948  |           0.534351 |
| conditional_exhaustion_vs_continuation_quality_20 |        10 | DISPERSION_ELEVATED      |      1248 |  0.00059444 |  0.00695652 |           0.487981 |
| compression_expansion_efficiency_asymmetry_15_30  |        20 | DISPERSION_ELEVATED      |      1238 | -0.00237945 | -0.0249903  |           0.47496  |
| breadth_deterioration_resilience_20               |        20 | RECENT_STRESS            |      1127 | -0.00449904 | -0.0742158  |           0.43567  |
| breadth_deterioration_resilience_20               |        20 | BROAD_STRESS             |       599 | -0.00504693 | -0.085512   |           0.407346 |
| residual_stress_liquidity_quality_20              |        20 | RECENT_STRESS            |      1357 | -0.00505665 | -0.0768229  |           0.464996 |
| residual_stress_liquidity_quality_20              |        20 | DISPERSION_ELEVATED      |      1014 | -0.00598409 | -0.0915584  |           0.431953 |
| residual_stress_liquidity_quality_20              |        20 | BROAD_STRESS             |       678 | -0.00787455 | -0.125301   |           0.439528 |
| residual_stress_liquidity_quality_20              |        20 | VOLATILITY_SPIKE         |       393 | -0.0079499  | -0.118552   |           0.447837 |

## Candidate Decisions

| signal_name                                       | family                             |   best_horizon |      mean_ic |   h10_mean_ic |   h20_mean_ic |   positive_ic_rate |   turnover_proxy |   active_date_ratio |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   one_window_dominance |   positive_regime_count |   best_regime_ic | interaction_decomposition_label   | dominant_component   |   dominant_component_corr | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | status                           | review_issues                                                                                                                                                  |
|:--------------------------------------------------|:-----------------------------------|---------------:|-------------:|--------------:|--------------:|-------------------:|-----------------:|--------------------:|---------------------:|--------------------:|--------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-----------------:|:----------------------------------|:---------------------|--------------------------:|:------------------------------|:----------------------------|:--------------------------------|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| turnover_exhaustion_quality_repair_10_20          | turnover_exhaustion_quality        |             20 |  0.00360062  |   0.00168876  |   0.00360062  |           0.534335 |        0.0424154 |            0.675882 |            0.0411469 |           0.0119798 |          0.00302907 |              0.5  |                   0.5  |               0.664768 |                       2 |       0.00679547 | true_interaction_behavior         | turnover_decay       |                  0.126748 | False                         | False                       | True                            | CONDITIONAL_ONLY_RESEARCH        | weak_best_horizon_ic; weak_medium_horizon_ic; weak_wfv_persistence; weak_wfv_sign_consistency; one_window_concentration                                        |
| dispersion_resilient_relative_stability_20        | dispersion_resilience              |              5 |  0.0027425   |   0.00164403  |   0.00138528  |           0.505938 |        0.0306872 |            0.604385 |            0.108704  |           0.0162368 |          0.0239738  |              0.5  |                   0.5  |               0.461292 |                       3 |       0.0109218  | true_interaction_behavior         | idio_stability       |                  0.335857 | True                          | False                       | False                           | CONDITIONAL_ONLY_RESEARCH        | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; stress_only_dependency                   |
| conditional_exhaustion_vs_continuation_quality_20 | continuation_exhaustion_quality    |             10 | -0.00487511  |  -0.00487511  |  -0.00478817  |           0.461538 |        0.0445635 |            0.971401 |            0.122527  |           0.124768  |          0.0657169  |              0.25 |                   0.75 |               0.457728 |                       2 |       0.00580012 | mixed_or_inconclusive_interaction | low_extension        |                  0.186119 | False                         | False                       | False                           | CONDITIONAL_ONLY_RESEARCH        | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; activation_too_broad                            |
| volatility_participation_asymmetry_20             | volatility_participation_asymmetry |             20 |  0.012246    |   0.0058405   |   0.012246    |           0.585233 |        0.0471619 |            0.971401 |            0.0517503 |           0.0339055 |          0.00731049 |              1    |                   1    |               0.594737 |                       5 |       0.0183696  | true_interaction_behavior         | low_extension        |                  0.067746 | False                         | False                       | False                           | CONDITIONAL_REFINEMENT_CANDIDATE | activation_too_broad                                                                                                                                           |
| volatility_of_volatility_stabilization_20         | volatility_of_volatility           |             20 |  0.000853209 |  -0.000848852 |   0.000853209 |           0.482587 |        0.0353751 |            0.675882 |            0.0942491 |           0.014257  |          0.00735954 |              0.75 |                   0.75 |               0.708713 |                       1 |       0.0145997  | single_component_ic_dominates     | vov_decay            |                  0.130786 | False                         | False                       | True                            | REJECT_RESEARCH                  | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; one_window_concentration                                                                  |
| residual_stress_liquidity_quality_20              | residual_stress_liquidity          |             20 | -0.00467606  |  -0.00380114  |  -0.00467606  |           0.459459 |        0.0347509 |            0.675882 |            0.0507946 |           0.0203173 |          0.0245853  |              0.25 |                   0.75 |               0.493628 |                       0 |      -0.0079499  | single_component_ic_dominates     | liquidity_quality    |                  0.249166 | False                         | False                       | False                           | REJECT_RESEARCH                  | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| compression_expansion_efficiency_asymmetry_15_30  | compression_expansion_asymmetry    |             20 | -0.00498369  |  -0.00455073  |  -0.00498369  |           0.480674 |        0.0445505 |            0.971401 |            0.119882  |           0.0391446 |          0.0328893  |              0.5  |                   0.5  |               0.571763 |                       0 |       0.00365499 | single_component_ic_dominates     | low_gap_noise        |                  0.2629   | False                         | False                       | False                           | REJECT_RESEARCH                  | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; activation_too_broad |
| breadth_deterioration_resilience_20               | breadth_deterioration_resilience   |             20 | -0.00655933  |  -0.00635076  |  -0.00655933  |           0.43188  |        0.0417635 |            0.681602 |            0.0617644 |           0.0275754 |          0.0105142  |              0    |                   1    |               0.721395 |                       1 |       0.0135748  | mixed_or_inconclusive_interaction | low_extension        |                  0.130254 | False                         | False                       | True                            | REJECT_RESEARCH                  | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; one_window_concentration                        |

## Recommendation

Run a narrow follow-up only for `volatility_participation_asymmetry_20`.

Do not route any candidate into production, survivor/watchlist, validation, portfolio, ML, blending, or optimization from this batch alone.
