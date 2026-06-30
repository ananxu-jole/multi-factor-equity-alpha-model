# Volatility Participation Asymmetry 20 Refinement v1

Date: 2026-05-22

Run id: `volatility_participation_asymmetry_20_refinement_v1`

Status: RESEARCH_ONLY_REFINEMENT_PASS

## Research-Only Guardrail

This is a research-only structural interaction alpha discovery batch. It does not modify detector code or labels, register production signals, mutate survivor/watchlist state, loosen gates or thresholds, change schemas/governance, or route anything into portfolio, ML, blending, or optimization workflows.

This pass refines only `volatility_participation_asymmetry_20`. It does not touch the three CONDITIONAL_ONLY_RESEARCH candidates from the structural interaction batch.

## Objective

Reduce broad activation while preserving h20 behavior, h10 support, WFV persistence, true interaction structure, low inventory overlap, and reversal/momentum separation.

## Executive Takeaway

Variants tested: `7`

Best refined variant: `volatility_participation_asymmetry_20_original`

Conservative classification: `CONDITIONAL_ONLY_RESEARCH`

h10 mean IC: `0.005843`

h20 mean IC: `0.012154`

Active date ratio: `0.971401`

Mean raw activation-filter coverage: `0.345800`

Interaction label: `true_interaction_behavior`

## Variants

| signal_name                                                  | variant_type                | description                                                                                               | run_id                                              | source_signal                         | research_status          |
|:-------------------------------------------------------------|:----------------------------|:----------------------------------------------------------------------------------------------------------|:----------------------------------------------------|:--------------------------------------|:-------------------------|
| volatility_participation_asymmetry_20_original               | source_formula              | Original structural interaction batch formulation.                                                        | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_participation_q60      | participation_tightening    | Require clearer up/down participation asymmetry while preserving original stabilization logic.            | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_vol_stab_q60           | volatility_confirmation     | Require stronger volatility stabilization confirmation while preserving original participation logic.     | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_dual_q55               | dual_confirmation           | Require both participation asymmetry and volatility stabilization to be above modest confirmation levels. | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_dual_close_q55         | quality_activation          | Add close-location quality to the dual confirmation filter.                                               | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_balanced_selective_q60 | balanced_selectivity        | Require the combined raw interaction score to sit above a moderate cross-sectional selectivity threshold. | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  | low_churn_dual_confirmation | Use dual confirmation with slower rebalance to test whether reduced churn preserves structure.            | volatility_participation_asymmetry_20_refinement_v1 | volatility_participation_asymmetry_20 | RESEARCH_ONLY_REFINEMENT |

## Original Vs Refined Comparison

| signal_name                                                  |   best_horizon |   best_mean_ic |   h10_mean_ic |   h20_mean_ic |   active_date_ratio |   active_ratio_delta_vs_original | interaction_decomposition_label   |
|:-------------------------------------------------------------|---------------:|---------------:|--------------:|--------------:|--------------------:|---------------------------------:|:----------------------------------|
| volatility_participation_asymmetry_20_vol_stab_q60           |              1 |    -0.00118948 |   0.000606428 |   0.00105817  |            0.971401 |                       0          | single_component_ic_dominates     |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |              1 |    -0.00157644 |   0.00148576  |  -0.000199454 |            0.971401 |                       0          | single_component_ic_dominates     |
| volatility_participation_asymmetry_20_dual_close_q55         |              5 |    -0.00420195 |  -0.00257334  |  -0.000794661 |            0.966635 |                      -0.00476644 | single_component_ic_dominates     |
| volatility_participation_asymmetry_20_original               |             20 |     0.0121536  |   0.00584314  |   0.0121536   |            0.971401 |                       0          | true_interaction_behavior         |
| volatility_participation_asymmetry_20_participation_q60      |             20 |     0.00848956 |   0.00431887  |   0.00848956  |            0.971401 |                       0          | single_component_ic_dominates     |
| volatility_participation_asymmetry_20_dual_q55               |             20 |     0.00300736 |   0.00169874  |   0.00300736  |            0.971401 |                       0          | single_component_ic_dominates     |
| volatility_participation_asymmetry_20_balanced_selective_q60 |             20 |     0.00881797 |   0.00392882  |   0.00881797  |            0.971401 |                       0          | mixed_or_inconclusive_interaction |

## Raw Activation Filter Summary

| signal_name                                                  |   raw_filter_active_dates |   raw_filter_active_date_ratio |   raw_filter_material_active_dates |   raw_filter_material_active_date_ratio |   mean_raw_filter_coverage |   median_raw_filter_coverage |   p95_raw_filter_coverage |
|:-------------------------------------------------------------|--------------------------:|-------------------------------:|-----------------------------------:|----------------------------------------:|---------------------------:|-----------------------------:|--------------------------:|
| volatility_participation_asymmetry_20_original               |                      1450 |                       0.691134 |                               1450 |                              0.691134   |                 0.3458     |                   0.361925   |                 0.441423  |
| volatility_participation_asymmetry_20_participation_q60      |                      1448 |                       0.690181 |                                777 |                              0.370353   |                 0.0535582  |                   0.0523013  |                 0.100418  |
| volatility_participation_asymmetry_20_vol_stab_q60           |                      1450 |                       0.691134 |                               1445 |                              0.688751   |                 0.120085   |                   0.121339   |                 0.150628  |
| volatility_participation_asymmetry_20_dual_q55               |                      1395 |                       0.664919 |                                  4 |                              0.00190658 |                 0.0139785  |                   0.0125523  |                 0.0313808 |
| volatility_participation_asymmetry_20_dual_close_q55         |                      1190 |                       0.567207 |                                  0 |                              0          |                 0.00750501 |                   0.00627615 |                 0.0188285 |
| volatility_participation_asymmetry_20_balanced_selective_q60 |                      1450 |                       0.691134 |                               1450 |                              0.691134   |                 0.3659     |                   0.311715   |                 0.682008  |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |                      1395 |                       0.664919 |                                  4 |                              0.00190658 |                 0.0139785  |                   0.0125523  |                 0.0313808 |

## Multi-Horizon IC

| signal_name                                                  |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:-------------------------------------------------------------|----------:|-------------:|--------------:|------------:|------------:|-------------------:|----------:|---------------:|:------------------|
| volatility_participation_asymmetry_20_original               |         1 | -0.000828002 |   0.000828002 | -0.0118353  |  0.0118353  |           0.504664 |      2037 |             20 | False             |
| volatility_participation_asymmetry_20_participation_q60      |         1 | -0.00109437  |   0.00109437  | -0.0150198  |  0.0150198  |           0.488463 |      2037 |             20 | False             |
| volatility_participation_asymmetry_20_vol_stab_q60           |         1 | -0.00118948  |   0.00118948  | -0.0176825  |  0.0176825  |           0.493373 |      2037 |              1 | True              |
| volatility_participation_asymmetry_20_dual_q55               |         1 | -0.00170726  |   0.00170726  | -0.0223098  |  0.0223098  |           0.483554 |      2037 |             20 | False             |
| volatility_participation_asymmetry_20_dual_close_q55         |         1 | -0.00266019  |   0.00266019  | -0.0347077  |  0.0347077  |           0.490918 |      2037 |              5 | False             |
| volatility_participation_asymmetry_20_balanced_selective_q60 |         1 | -0.00100757  |   0.00100757  | -0.0153592  |  0.0153592  |           0.505646 |      2037 |             20 | False             |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |         1 | -0.00157644  |   0.00157644  | -0.0207879  |  0.0207879  |           0.485518 |      2037 |              1 | True              |
| volatility_participation_asymmetry_20_original               |         5 | -0.000203416 |   0.000203416 | -0.00296177 |  0.00296177 |           0.49877  |      2033 |             20 | False             |
| volatility_participation_asymmetry_20_participation_q60      |         5 |  0.000812577 |   0.000812577 |  0.0113038  |  0.0113038  |           0.49877  |      2033 |             20 | False             |
| volatility_participation_asymmetry_20_vol_stab_q60           |         5 | -0.0011422   |   0.0011422   | -0.0169088  |  0.0169088  |           0.485981 |      2033 |              1 | False             |
| volatility_participation_asymmetry_20_dual_q55               |         5 | -0.000515908 |   0.000515908 | -0.00678362 |  0.00678362 |           0.496311 |      2033 |             20 | False             |
| volatility_participation_asymmetry_20_dual_close_q55         |         5 | -0.00420195  |   0.00420195  | -0.0552001  |  0.0552001  |           0.462863 |      2033 |              5 | True              |
| volatility_participation_asymmetry_20_balanced_selective_q60 |         5 | -0.000363138 |   0.000363138 | -0.00549169 |  0.00549169 |           0.508116 |      2033 |             20 | False             |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |         5 | -0.000232174 |   0.000232174 | -0.00305086 |  0.00305086 |           0.489916 |      2033 |              1 | False             |
| volatility_participation_asymmetry_20_original               |        10 |  0.00584314  |   0.00584314  |  0.0899614  |  0.0899614  |           0.551775 |      2028 |             20 | False             |
| volatility_participation_asymmetry_20_participation_q60      |        10 |  0.00431887  |   0.00431887  |  0.0610756  |  0.0610756  |           0.526134 |      2028 |             20 | False             |
| volatility_participation_asymmetry_20_vol_stab_q60           |        10 |  0.000606428 |   0.000606428 |  0.00918028 |  0.00918028 |           0.486686 |      2028 |              1 | False             |
| volatility_participation_asymmetry_20_dual_q55               |        10 |  0.00169874  |   0.00169874  |  0.0228818  |  0.0228818  |           0.506903 |      2028 |             20 | False             |
| volatility_participation_asymmetry_20_dual_close_q55         |        10 | -0.00257334  |   0.00257334  | -0.035143   |  0.035143   |           0.481262 |      2028 |              5 | False             |
| volatility_participation_asymmetry_20_balanced_selective_q60 |        10 |  0.00392882  |   0.00392882  |  0.0615393  |  0.0615393  |           0.533037 |      2028 |             20 | False             |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |        10 |  0.00148576  |   0.00148576  |  0.020001   |  0.020001   |           0.494576 |      2028 |              1 | False             |
| volatility_participation_asymmetry_20_original               |        20 |  0.0121536   |   0.0121536   |  0.193305   |  0.193305   |           0.585233 |      2018 |             20 | True              |
| volatility_participation_asymmetry_20_participation_q60      |        20 |  0.00848956  |   0.00848956  |  0.129362   |  0.129362   |           0.560951 |      2018 |             20 | True              |
| volatility_participation_asymmetry_20_vol_stab_q60           |        20 |  0.00105817  |   0.00105817  |  0.0156911  |  0.0156911  |           0.497027 |      2018 |              1 | False             |
| volatility_participation_asymmetry_20_dual_q55               |        20 |  0.00300736  |   0.00300736  |  0.0424818  |  0.0424818  |           0.509911 |      2018 |             20 | True              |
| volatility_participation_asymmetry_20_dual_close_q55         |        20 | -0.000794661 |   0.000794661 | -0.011095   |  0.011095   |           0.489594 |      2018 |              5 | False             |
| volatility_participation_asymmetry_20_balanced_selective_q60 |        20 |  0.00881797  |   0.00881797  |  0.143837   |  0.143837   |           0.549554 |      2018 |             20 | True              |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |        20 | -0.000199454 |   0.000199454 | -0.0028392  |  0.0028392  |           0.466303 |      2018 |              1 | False             |

## Interaction Decomposition

| signal_name                                                  |   horizon |   final_mean_ic |   best_component_mean_ic |   interaction_ic_lift_vs_best_component | dominant_component   |   dominant_component_corr | interaction_decomposition_label   | component_corr_detail                                                                                                              | component_ic_detail                                                                                                                            |
|:-------------------------------------------------------------|----------:|----------------:|-------------------------:|----------------------------------------:|:---------------------|--------------------------:|:----------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| volatility_participation_asymmetry_20_original               |        20 |      0.0121536  |               0.00977944 |                              0.00237412 | low_extension        |                 0.106558  | true_interaction_behavior         | volatility_stabilization:0.085; participation_asymmetry:0.068; close_support:-0.016; low_extension:0.107; activation_filter:0.051  | volatility_stabilization:0.00898; participation_asymmetry:0.00978; close_support:-0.00629; low_extension:-0.00735; activation_filter:-0.01179  |
| volatility_participation_asymmetry_20_participation_q60      |        20 |      0.00848956 |               0.0286488  |                             -0.0201593  | low_extension        |                 0.153576  | single_component_ic_dominates     | volatility_stabilization:0.112; participation_asymmetry:-0.010; close_support:-0.014; low_extension:0.154; activation_filter:0.018 | volatility_stabilization:0.02865; participation_asymmetry:-0.00094; close_support:-0.01376; low_extension:-0.01190; activation_filter:0.00477  |
| volatility_participation_asymmetry_20_vol_stab_q60           |         1 |     -0.00118948 |               0.00104727 |                             -0.00223675 | low_extension        |                 0.175429  | single_component_ic_dominates     | volatility_stabilization:-0.004; participation_asymmetry:0.106; close_support:-0.003; low_extension:0.175; activation_filter:0.022 | volatility_stabilization:-0.00134; participation_asymmetry:-0.00660; close_support:-0.01203; low_extension:-0.00855; activation_filter:0.00105 |
| volatility_participation_asymmetry_20_dual_q55               |        20 |      0.00300736 |               0.0976212  |                             -0.0946138  | low_extension        |                 0.140977  | single_component_ic_dominates     | volatility_stabilization:0.002; participation_asymmetry:0.029; close_support:0.003; low_extension:0.141; activation_filter:0.026   | volatility_stabilization:0.09762; participation_asymmetry:-0.13355; close_support:-0.13114; low_extension:0.02848; activation_filter:0.00482   |
| volatility_participation_asymmetry_20_dual_close_q55         |         5 |     -0.00420195 |               0.00324128 |                             -0.00744323 | low_extension        |                 0.0978622 | single_component_ic_dominates     | volatility_stabilization:0.004; participation_asymmetry:0.027; close_support:-0.009; low_extension:0.098; activation_filter:0.016  | activation_filter:0.00324                                                                                                                      |
| volatility_participation_asymmetry_20_balanced_selective_q60 |        20 |      0.00881797 |               0.00737282 |                              0.00144515 | low_extension        |                 0.0858254 | mixed_or_inconclusive_interaction | volatility_stabilization:0.036; participation_asymmetry:0.050; close_support:-0.026; low_extension:0.086; activation_filter:0.069  | volatility_stabilization:0.00510; participation_asymmetry:0.00737; close_support:-0.00862; low_extension:-0.00632; activation_filter:-0.00742  |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |         1 |     -0.00157644 |               0.0770954  |                             -0.0786718  | low_extension        |                 0.0582433 | single_component_ic_dominates     | volatility_stabilization:0.003; participation_asymmetry:0.007; close_support:-0.001; low_extension:0.058; activation_filter:0.011  | volatility_stabilization:0.07710; participation_asymmetry:-0.02329; close_support:-0.05593; low_extension:-0.04003; activation_filter:-0.00021 |

## Fragility / Concentration

| signal_name                                                  |   horizon |   full_mean_ic |   crisis_mean_ic |   non_crisis_mean_ic |   crisis_positive_ic_rate |   non_crisis_positive_ic_rate |   crisis_valid_dates |   non_crisis_valid_dates |   crisis_positive_contribution_share |   one_window_dominance | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | regime_exclusivity_flag   |
|:-------------------------------------------------------------|----------:|---------------:|-----------------:|---------------------:|--------------------------:|------------------------------:|---------------------:|-------------------------:|-------------------------------------:|-----------------------:|:------------------------------|:----------------------------|:--------------------------------|:--------------------------|
| volatility_participation_asymmetry_20_vol_stab_q60           |         1 |    -0.00118948 |      -0.00289303 |          -0.00026613 |                  0.486034 |                      0.49735  |                  716 |                     1321 |                             0.331867 |               0.529867 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  |         1 |    -0.00157644 |      -0.00245893 |          -0.00109812 |                  0.484637 |                      0.485995 |                  716 |                     1321 |                             0.325091 |               0.379619 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20_dual_close_q55         |         5 |    -0.00420195 |      -0.00519199 |          -0.0036637  |                  0.465084 |                      0.461655 |                  716 |                     1317 |                             0.347249 |               0.403078 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20_original               |        20 |     0.0121536  |       0.011453   |           0.0125297  |                  0.575887 |                      0.590251 |                  705 |                     1313 |                             0.336425 |               0.589666 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20_participation_q60      |        20 |     0.00848956 |       0.00374855 |           0.0110352  |                  0.51773  |                      0.584158 |                  705 |                     1313 |                             0.29401  |               0.550899 | False                         | False                       | False                           | False                     |
| volatility_participation_asymmetry_20_dual_q55               |        20 |     0.00300736 |       0.00261532 |           0.00321786 |                  0.496454 |                      0.517136 |                  705 |                     1313 |                             0.313451 |               0.969495 | False                         | False                       | True                            | False                     |
| volatility_participation_asymmetry_20_balanced_selective_q60 |        20 |     0.00881797 |       0.00627313 |           0.0101844  |                  0.50922  |                      0.571211 |                  705 |                     1313 |                             0.326784 |               0.456294 | False                         | False                       | False                           | False                     |

## Similarity / Redundancy

| signal_name                                                  | top_comparison                                             |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:-------------------------------------------------------------|:-----------------------------------------------------------|------------------------:|---------------------:|--------------------:|--------------------:|
| volatility_participation_asymmetry_20_balanced_selective_q60 | v2_vol_compression_range_expansion_20_60                   |               0.0960246 |            0.0392499 |          0.0521495  |          0.0234571  |
| volatility_participation_asymmetry_20_dual_close_q55         | v2_beta_residual_reversal_stability_20                     |               0.0703541 |            0.0383751 |          0.0623044  |          0.060021   |
| volatility_participation_asymmetry_20_dual_q55               | v2_beta_residual_reversal_stability_20                     |               0.0506529 |            0.0351032 |          0.0401339  |          0.0443293  |
| volatility_participation_asymmetry_20_original               | v2_vol_compression_range_expansion_20_60                   |               0.109888  |            0.0527171 |          0.0317136  |          0.00576543 |
| volatility_participation_asymmetry_20_participation_q60      | inventory_participation_breadth_repair_under_hostile_trend |               0.0411942 |            0.0411942 |          0.00383154 |          0.0216317  |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  | v2_beta_residual_reversal_stability_20                     |               0.038671  |            0.0225645 |          0.0280686  |          0.0366552  |
| volatility_participation_asymmetry_20_vol_stab_q60           | v2_turnover_adjusted_relative_momentum_60                  |               0.0185954 |            0.0118634 |          0.0128379  |          0.0169015  |

## Candidate Decisions

| signal_name                                                  | status                    |   best_horizon |   best_mean_ic |   h10_mean_ic |   h20_mean_ic |   active_date_ratio |   mean_raw_filter_coverage |   raw_filter_material_active_date_ratio |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr | review_issues                                                                                                                                                                               |
|:-------------------------------------------------------------|:--------------------------|---------------:|---------------:|--------------:|--------------:|--------------------:|---------------------------:|----------------------------------------:|---------------------:|--------------------:|--------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| volatility_participation_asymmetry_20_vol_stab_q60           | REJECT_RESEARCH           |              1 |    -0.00118948 |   0.000606428 |   0.00105817  |            0.971401 |                 0.120085   |                              0.688751   |            0.0118634 |          0.0128379  |          0.0169015  | h20_not_preserved; weak_h10_support; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; interaction_not_preserved                                |
| volatility_participation_asymmetry_20_rebalance_20_dual_q55  | REJECT_RESEARCH           |              1 |    -0.00157644 |   0.00148576  |  -0.000199454 |            0.971401 |                 0.0139785  |                              0.00190658 |            0.0225645 |          0.0280686  |          0.0366552  | raw_filter_too_sparse; h20_not_preserved; weak_h10_support; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; interaction_not_preserved                                    |
| volatility_participation_asymmetry_20_dual_close_q55         | REJECT_RESEARCH           |              5 |    -0.00420195 |  -0.00257334  |  -0.000794661 |            0.966635 |                 0.00750501 |                              0          |            0.0383751 |          0.0623044  |          0.060021   | raw_filter_too_sparse; h20_not_preserved; weak_h10_support; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; interaction_not_preserved                                    |
| volatility_participation_asymmetry_20_original               | CONDITIONAL_ONLY_RESEARCH |             20 |     0.0121536  |   0.00584314  |   0.0121536   |            0.971401 |                 0.3458     |                              0.691134   |            0.0527171 |          0.0317136  |          0.00576543 | activation_not_improved_enough                                                                                                                                                              |
| volatility_participation_asymmetry_20_participation_q60      | CONDITIONAL_ONLY_RESEARCH |             20 |     0.00848956 |   0.00431887  |   0.00848956  |            0.971401 |                 0.0535582  |                              0.370353   |            0.0411942 |          0.00383154 |          0.0216317  | h20_not_preserved; weak_best_horizon_ic; interaction_not_preserved                                                                                                                          |
| volatility_participation_asymmetry_20_dual_q55               | CONDITIONAL_ONLY_RESEARCH |             20 |     0.00300736 |   0.00169874  |   0.00300736  |            0.971401 |                 0.0139785  |                              0.00190658 |            0.0351032 |          0.0401339  |          0.0443293  | raw_filter_too_sparse; h20_not_preserved; weak_h10_support; weak_best_horizon_ic; weak_positive_ic_rate; one_window_concentration; interaction_not_preserved; one_window_concentration_flag |
| volatility_participation_asymmetry_20_balanced_selective_q60 | CONDITIONAL_ONLY_RESEARCH |             20 |     0.00881797 |   0.00392882  |   0.00881797  |            0.971401 |                 0.3659     |                              0.691134   |            0.0392499 |          0.0521495  |          0.0234571  | h20_not_preserved; weak_h10_support; weak_best_horizon_ic; weak_positive_ic_rate; interaction_not_preserved                                                                                 |

## Recommendation

Do not advance to validation. Preserve the artifacts for research history and consider a separate redesign only if future inventory monitoring supports it.

No production registration, survivor/watchlist mutation, detector modification, schema/gate/governance change, or portfolio/ML/blending/optimization route was made.
