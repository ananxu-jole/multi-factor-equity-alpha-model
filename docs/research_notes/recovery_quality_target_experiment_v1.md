# Recovery Quality Target Experiment v1

Date: 2026-05-25

Status: `RESEARCH_ONLY_DIAGNOSTIC_ONLY`

## Executive Takeaway

This experiment compares current inventory candidates and selected parked weak clues against raw h10/h20 forward-return targets and several recovery-oriented diagnostic targets.

Raw h10/h20 IC remains the validation anchor. Alternative targets in this run are diagnostic lenses only and do not change candidate status, gates, validation logic, production registration, portfolio routing, ML, blending, optimization, detector usage, metadata usage, or governance.

Candidate panels available: `6` / `6`.

## Candidates Evaluated

| signal_name                                       | candidate_group               | panel_path                                                                                                                                 | available   |   rows |   columns | status_change_allowed   |
|:--------------------------------------------------|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|:------------|-------:|----------:|:------------------------|
| participation_liquidity_state_shift_20_60         | current_inventory             | artifacts/research/robustness_first_discovery_expansion_v4/participation_liquidity_state_shift_20_60_signal_panel.parquet                  | True        |   2098 |       478 | False                   |
| participation_breadth_repair_under_hostile_trend  | current_inventory             | artifacts/research/track_b_v5_focused_discovery/participation_breadth_repair_under_hostile_trend_signal_panel.parquet                      | True        |   2098 |       478 | False                   |
| volatility_compression_after_stress_stabilization | current_inventory             | artifacts/research/track_b_v6_focused_discovery/volatility_compression_after_stress_stabilization_signal_panel.parquet                     | True        |   2098 |       478 | False                   |
| volatility_participation_asymmetry_20_original    | parked_weak_research_evidence | artifacts/research/volatility_participation_asymmetry_20_refinement_v1/volatility_participation_asymmetry_20_original_signal_panel.parquet | True        |   2098 |       478 | False                   |
| turnover_shock_exhaustion_repair_20               | parked_weak_research_evidence | artifacts/research/event_defined_liquidity_turnover_exhaustion_alpha_v1/turnover_shock_exhaustion_repair_20_signal_panel.parquet           | True        |   2098 |       478 | False                   |
| short_horizon_volatility_shock_absorption_10      | parked_weak_research_evidence | artifacts/research/short_horizon_volatility_shock_absorption_10_refinement/rebalance_5_zero_signal_panel.parquet                           | True        |   2098 |       478 | False                   |

## Target Families

- raw h10/h20 forward return
- drawdown-adjusted h10/h20 forward return
- downside-controlled h10/h20 return
- recovery-quality h10/h20 composite
- post-stress stabilization h10/h20 target

## Raw Target Anchor

| signal_name                                       | target_name            | target_family      |   horizon |    mean_ic |     ic_ir |   positive_ic_rate |   n_dates | research_only   |
|:--------------------------------------------------|:-----------------------|:-------------------|----------:|-----------:|----------:|-------------------:|----------:|:----------------|
| short_horizon_volatility_shock_absorption_10      | raw_h10_forward_return | raw_forward_return |        10 | 0.0102596  | 0.142425  |           0.600515 |       388 | True            |
| volatility_compression_after_stress_stabilization | raw_h10_forward_return | raw_forward_return |        10 | 0.00762096 | 0.0480148 |           0.507772 |       386 | True            |
| volatility_participation_asymmetry_20_original    | raw_h10_forward_return | raw_forward_return |        10 | 0.00584314 | 0.0899614 |           0.551775 |      2028 | True            |
| participation_breadth_repair_under_hostile_trend  | raw_h10_forward_return | raw_forward_return |        10 | 0.00536315 | 0.0451351 |           0.5      |       380 | True            |
| participation_liquidity_state_shift_20_60         | raw_h10_forward_return | raw_forward_return |        10 | 0.00490851 | 0.0418654 |           0.515373 |      2049 | True            |
| turnover_shock_exhaustion_repair_20               | raw_h10_forward_return | raw_forward_return |        10 | 0.0028722  | 0.062681  |           0.508772 |      1938 | True            |
| participation_breadth_repair_under_hostile_trend  | raw_h20_forward_return | raw_forward_return |        20 | 0.0228754  | 0.196955  |           0.563492 |       378 | True            |
| volatility_participation_asymmetry_20_original    | raw_h20_forward_return | raw_forward_return |        20 | 0.0121536  | 0.193305  |           0.585233 |      2018 | True            |
| volatility_compression_after_stress_stabilization | raw_h20_forward_return | raw_forward_return |        20 | 0.0110712  | 0.0702201 |           0.53562  |       379 | True            |
| participation_liquidity_state_shift_20_60         | raw_h20_forward_return | raw_forward_return |        20 | 0.00842118 | 0.072874  |           0.509564 |      2039 | True            |
| turnover_shock_exhaustion_repair_20               | raw_h20_forward_return | raw_forward_return |        20 | 0.00492666 | 0.109164  |           0.511411 |      1928 | True            |
| short_horizon_volatility_shock_absorption_10      | raw_h20_forward_return | raw_forward_return |        20 | 0.00324326 | 0.0416154 |           0.536842 |       380 | True            |

## Alternative Target Comparison

| signal_name                                       | target_name                          | target_family                    |   horizon |     mean_ic |      ic_ir |   positive_ic_rate |   n_dates | research_only   |
|:--------------------------------------------------|:-------------------------------------|:---------------------------------|----------:|------------:|-----------:|-------------------:|----------:|:----------------|
| volatility_compression_after_stress_stabilization | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.018049   |  0.116141  |           0.528497 |       386 | True            |
| short_horizon_volatility_shock_absorption_10      | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.00870698 |  0.118879  |           0.592784 |       388 | True            |
| volatility_participation_asymmetry_20_original    | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.00814647 |  0.124206  |           0.565089 |      2028 | True            |
| participation_breadth_repair_under_hostile_trend  | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.0071923  |  0.0615241 |           0.513158 |       380 | True            |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.00543567 |  0.118676  |           0.53354  |      1938 | True            |
| participation_liquidity_state_shift_20_60         | downside_controlled_h10_return       | downside_controlled_return       |        10 |  0.00510456 |  0.0434491 |           0.515373 |      2049 | True            |
| volatility_compression_after_stress_stabilization | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.0270899  |  0.175826  |           0.591029 |       379 | True            |
| participation_breadth_repair_under_hostile_trend  | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.0236524  |  0.205865  |           0.550265 |       378 | True            |
| volatility_participation_asymmetry_20_original    | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.01567    |  0.247752  |           0.613479 |      2018 | True            |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.00938769 |  0.206813  |           0.557054 |      1928 | True            |
| participation_liquidity_state_shift_20_60         | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.00832839 |  0.0720317 |           0.511525 |      2039 | True            |
| short_horizon_volatility_shock_absorption_10      | downside_controlled_h20_return       | downside_controlled_return       |        20 |  0.0037975  |  0.0491083 |           0.560526 |       380 | True            |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.022889   |  0.148809  |           0.554404 |       386 | True            |
| short_horizon_volatility_shock_absorption_10      | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.00998512 |  0.135265  |           0.600515 |       388 | True            |
| participation_breadth_repair_under_hostile_trend  | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.00969524 |  0.0832526 |           0.5      |       380 | True            |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.00913114 |  0.136969  |           0.564103 |      2028 | True            |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.00703003 |  0.151308  |           0.552632 |      1938 | True            |
| participation_liquidity_state_shift_20_60         | drawdown_adjusted_h10_forward_return | drawdown_adjusted_forward_return |        10 |  0.00413718 |  0.0352901 |           0.507565 |      2049 | True            |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.0291066  |  0.188015  |           0.60686  |       379 | True            |
| participation_breadth_repair_under_hostile_trend  | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.0242557  |  0.208982  |           0.560847 |       378 | True            |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.0160357  |  0.247622  |           0.608028 |      2018 | True            |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.00965344 |  0.212874  |           0.559647 |      1928 | True            |
| participation_liquidity_state_shift_20_60         | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.00828612 |  0.0715788 |           0.514958 |      2039 | True            |
| short_horizon_volatility_shock_absorption_10      | drawdown_adjusted_h20_forward_return | drawdown_adjusted_forward_return |        20 |  0.00458805 |  0.0593324 |           0.552632 |       380 | True            |
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 |  0.146516   |  1.90203   |           0.953552 |       366 | True            |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 |  0.0898494  |  0.840549  |           0.795248 |      1431 | True            |
| turnover_shock_exhaustion_repair_20               | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 |  0.00439386 |  0.0846897 |           0.53913  |      1380 | True            |
| participation_breadth_repair_under_hostile_trend  | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 | -0.0153371  | -0.140776  |           0.418919 |       370 | True            |
| volatility_participation_asymmetry_20_original    | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 | -0.0454163  | -0.648946  |           0.248936 |      1410 | True            |
| volatility_compression_after_stress_stabilization | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 | -0.131163   | -0.905367  |           0.175573 |       393 | True            |
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 |  0.163104   |  2.13344   |           0.978142 |       366 | True            |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 |  0.109989   |  0.981154  |           0.849057 |      1431 | True            |
| turnover_shock_exhaustion_repair_20               | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 |  0.00552911 |  0.106829  |           0.532609 |      1380 | True            |
| participation_breadth_repair_under_hostile_trend  | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 | -0.0100458  | -0.0855178 |           0.451351 |       370 | True            |
| volatility_participation_asymmetry_20_original    | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 | -0.0484351  | -0.685512  |           0.246809 |      1410 | True            |
| volatility_compression_after_stress_stabilization | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 | -0.156843   | -0.971434  |           0.167939 |       393 | True            |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h10_composite       | recovery_quality_composite       |        10 |  0.12265    |  1.62431   |           0.930412 |       388 | True            |
| participation_liquidity_state_shift_20_60         | recovery_quality_h10_composite       | recovery_quality_composite       |        10 |  0.0701356  |  0.640283  |           0.755979 |      2049 | True            |
| turnover_shock_exhaustion_repair_20               | recovery_quality_h10_composite       | recovery_quality_composite       |        10 |  0.00441413 |  0.0876898 |           0.54644  |      1938 | True            |
| participation_breadth_repair_under_hostile_trend  | recovery_quality_h10_composite       | recovery_quality_composite       |        10 | -0.0128442  | -0.111756  |           0.426316 |       380 | True            |
| volatility_participation_asymmetry_20_original    | recovery_quality_h10_composite       | recovery_quality_composite       |        10 | -0.0212247  | -0.295088  |           0.378698 |      2028 | True            |
| volatility_compression_after_stress_stabilization | recovery_quality_h10_composite       | recovery_quality_composite       |        10 | -0.10045    | -0.709164  |           0.217617 |       386 | True            |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h20_composite       | recovery_quality_composite       |        20 |  0.135203   |  1.77277   |           0.947368 |       380 | True            |
| participation_liquidity_state_shift_20_60         | recovery_quality_h20_composite       | recovery_quality_composite       |        20 |  0.089397   |  0.801629  |           0.801373 |      2039 | True            |
| turnover_shock_exhaustion_repair_20               | recovery_quality_h20_composite       | recovery_quality_composite       |        20 |  0.00691132 |  0.139464  |           0.552905 |      1928 | True            |
| participation_breadth_repair_under_hostile_trend  | recovery_quality_h20_composite       | recovery_quality_composite       |        20 | -0.00509835 | -0.0419361 |           0.460317 |       378 | True            |
| volatility_participation_asymmetry_20_original    | recovery_quality_h20_composite       | recovery_quality_composite       |        20 | -0.0171761  | -0.233785  |           0.400396 |      2018 | True            |
| volatility_compression_after_stress_stabilization | recovery_quality_h20_composite       | recovery_quality_composite       |        20 | -0.117934   | -0.763083  |           0.184697 |       379 | True            |

## Best Alternative Target Clues

| signal_name                                  | target_name                          | target_family                    |   horizon |   mean_ic |    ic_ir |   positive_ic_rate |   n_dates | research_only   |
|:---------------------------------------------|:-------------------------------------|:---------------------------------|----------:|----------:|---------:|-------------------:|----------:|:----------------|
| short_horizon_volatility_shock_absorption_10 | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 | 0.163104  | 2.13344  |           0.978142 |       366 | True            |
| short_horizon_volatility_shock_absorption_10 | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 | 0.146516  | 1.90203  |           0.953552 |       366 | True            |
| short_horizon_volatility_shock_absorption_10 | recovery_quality_h20_composite       | recovery_quality_composite       |        20 | 0.135203  | 1.77277  |           0.947368 |       380 | True            |
| short_horizon_volatility_shock_absorption_10 | recovery_quality_h10_composite       | recovery_quality_composite       |        10 | 0.12265   | 1.62431  |           0.930412 |       388 | True            |
| participation_liquidity_state_shift_20_60    | post_stress_stabilization_h20_target | post_stress_stabilization_target |        20 | 0.109989  | 0.981154 |           0.849057 |      1431 | True            |
| participation_liquidity_state_shift_20_60    | post_stress_stabilization_h10_target | post_stress_stabilization_target |        10 | 0.0898494 | 0.840549 |           0.795248 |      1431 | True            |
| participation_liquidity_state_shift_20_60    | recovery_quality_h20_composite       | recovery_quality_composite       |        20 | 0.089397  | 0.801629 |           0.801373 |      2039 | True            |
| participation_liquidity_state_shift_20_60    | recovery_quality_h10_composite       | recovery_quality_composite       |        10 | 0.0701356 | 0.640283 |           0.755979 |      2049 | True            |

## Preliminary Interpretation

- The most visible alternative-target lift appears in `short_horizon_volatility_shock_absorption_10` and `participation_liquidity_state_shift_20_60` under recovery-quality and post-stress stabilization targets.
- `volatility_compression_after_stress_stabilization` improves more under drawdown-adjusted and downside-controlled return than under the recovery-quality composite.
- `participation_breadth_repair_under_hostile_trend` remains strongest on raw h20; alternative targets do not materially improve it in this run.
- `volatility_participation_asymmetry_20_original` and `turnover_shock_exhaustion_repair_20` show only modest drawdown-adjusted improvement and remain parked weak evidence.
- The largest recovery/post-stress effects should be treated as target-feature proximity clues, not alpha evidence, because those target definitions intentionally include stabilization and path-quality terms.
- Drawdown-adjusted targets are highly correlated with raw forward-return targets, so they may be best interpreted as a supplement rather than a distinct target family.

## Candidate Behavior Profiles

| signal_name                                       | candidate_group               | best_raw_target        |   best_raw_mean_ic | best_alternative_target              |   best_alternative_mean_ic |   max_target_minus_raw_ic | alternative_lens_helped   | status_change_allowed   |
|:--------------------------------------------------|:------------------------------|:-----------------------|-------------------:|:-------------------------------------|---------------------------:|--------------------------:|:--------------------------|:------------------------|
| participation_breadth_repair_under_hostile_trend  | current_inventory             | raw_h20_forward_return |         0.0228754  | drawdown_adjusted_h20_forward_return |                 0.0242557  |                0.00433209 | False                     | False                   |
| participation_liquidity_state_shift_20_60         | current_inventory             | raw_h20_forward_return |         0.00842118 | post_stress_stabilization_h20_target |                 0.109989   |                0.101568   | True                      | False                   |
| short_horizon_volatility_shock_absorption_10      | parked_weak_research_evidence | raw_h10_forward_return |         0.0102596  | post_stress_stabilization_h20_target |                 0.163104   |                0.159861   | True                      | False                   |
| turnover_shock_exhaustion_repair_20               | parked_weak_research_evidence | raw_h20_forward_return |         0.00492666 | drawdown_adjusted_h20_forward_return |                 0.00965344 |                0.00472678 | False                     | False                   |
| volatility_compression_after_stress_stabilization | current_inventory             | raw_h20_forward_return |         0.0110712  | drawdown_adjusted_h20_forward_return |                 0.0291066  |                0.0180354  | True                      | False                   |
| volatility_participation_asymmetry_20_original    | parked_weak_research_evidence | raw_h20_forward_return |         0.0121536  | drawdown_adjusted_h20_forward_return |                 0.0160357  |                0.00388215 | False                     | False                   |

## Target Sensitivity Versus Raw Return

| signal_name                                       | target_name                          |   horizon |   target_mean_ic |   raw_mean_ic |   target_minus_raw_ic |   target_positive_ic_rate |   raw_positive_ic_rate | raw_validation_anchor_replaced   |
|:--------------------------------------------------|:-------------------------------------|----------:|-----------------:|--------------:|----------------------:|--------------------------:|-----------------------:|:---------------------------------|
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h20_target |        20 |       0.163104   |    0.00324326 |            0.159861   |                  0.978142 |               0.536842 | False                            |
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h10_target |        10 |       0.146516   |    0.0102596  |            0.136257   |                  0.953552 |               0.600515 | False                            |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h20_composite       |        20 |       0.135203   |    0.00324326 |            0.13196    |                  0.947368 |               0.536842 | False                            |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h10_composite       |        10 |       0.12265    |    0.0102596  |            0.112391   |                  0.930412 |               0.600515 | False                            |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h20_target |        20 |       0.109989   |    0.00842118 |            0.101568   |                  0.849057 |               0.509564 | False                            |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h10_target |        10 |       0.0898494  |    0.00490851 |            0.0849409  |                  0.795248 |               0.515373 | False                            |
| participation_liquidity_state_shift_20_60         | recovery_quality_h20_composite       |        20 |       0.089397   |    0.00842118 |            0.0809758  |                  0.801373 |               0.509564 | False                            |
| participation_liquidity_state_shift_20_60         | recovery_quality_h10_composite       |        10 |       0.0701356  |    0.00490851 |            0.0652271  |                  0.755979 |               0.515373 | False                            |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h20_forward_return |        20 |       0.0291066  |    0.0110712  |            0.0180354  |                  0.60686  |               0.53562  | False                            |
| volatility_compression_after_stress_stabilization | downside_controlled_h20_return       |        20 |       0.0270899  |    0.0110712  |            0.0160187  |                  0.591029 |               0.53562  | False                            |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h10_forward_return |        10 |       0.022889   |    0.00762096 |            0.015268   |                  0.554404 |               0.507772 | False                            |
| volatility_compression_after_stress_stabilization | downside_controlled_h10_return       |        10 |       0.018049   |    0.00762096 |            0.010428   |                  0.528497 |               0.507772 | False                            |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h20_forward_return |        20 |       0.00965344 |    0.00492666 |            0.00472678 |                  0.559647 |               0.511411 | False                            |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h20_return       |        20 |       0.00938769 |    0.00492666 |            0.00446104 |                  0.557054 |               0.511411 | False                            |
| participation_breadth_repair_under_hostile_trend  | drawdown_adjusted_h10_forward_return |        10 |       0.00969524 |    0.00536315 |            0.00433209 |                  0.5      |               0.5      | False                            |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h10_forward_return |        10 |       0.00703003 |    0.0028722  |            0.00415784 |                  0.552632 |               0.508772 | False                            |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h20_forward_return |        20 |       0.0160357  |    0.0121536  |            0.00388215 |                  0.608028 |               0.585233 | False                            |
| volatility_participation_asymmetry_20_original    | downside_controlled_h20_return       |        20 |       0.01567    |    0.0121536  |            0.0035164  |                  0.613479 |               0.585233 | False                            |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h10_forward_return |        10 |       0.00913114 |    0.00584314 |            0.003288   |                  0.564103 |               0.551775 | False                            |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h10_return       |        10 |       0.00543567 |    0.0028722  |            0.00256348 |                  0.53354  |               0.508772 | False                            |

## Low-Volatility / Passive Reward Check

| target_name                          |   mean_lowvol_rank_corr |   abs_mean_lowvol_rank_corr |   positive_corr_rate |   n_dates | lowvol_reward_warning   |
|:-------------------------------------|------------------------:|----------------------------:|---------------------:|----------:|:------------------------|
| post_stress_stabilization_h20_target |             -0.196212   |                  0.196212   |             0.118785 |      1448 | False                   |
| recovery_quality_h20_composite       |             -0.183211   |                  0.183211   |             0.127299 |      2066 | False                   |
| post_stress_stabilization_h10_target |             -0.159311   |                  0.159311   |             0.15953  |      1448 | False                   |
| recovery_quality_h10_composite       |             -0.149921   |                  0.149921   |             0.188825 |      2076 | False                   |
| drawdown_adjusted_h10_forward_return |              0.0310001  |                  0.0310001  |             0.572736 |      2076 | False                   |
| drawdown_adjusted_h20_forward_return |              0.0297673  |                  0.0297673  |             0.584221 |      2066 | False                   |
| raw_h20_forward_return               |             -0.0273986  |                  0.0273986  |             0.487415 |      2066 | False                   |
| raw_h10_forward_return               |             -0.0209415  |                  0.0209415  |             0.483622 |      2076 | False                   |
| downside_controlled_h20_return       |              0.0193202  |                  0.0193202  |             0.56486  |      2066 | False                   |
| downside_controlled_h10_return       |              0.00470683 |                  0.00470683 |             0.524085 |      2076 | False                   |

## Fragility Review

| signal_name                                       | target_name                          |   score_n_dates |    mean_ic |   persistence |   one_window_dominance |   abs_mean_lowvol_rank_corr | fragility_warnings   | diagnostic_only   |
|:--------------------------------------------------|:-------------------------------------|----------------:|-----------:|--------------:|-----------------------:|----------------------------:|:---------------------|:------------------|
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h20_target |             366 | 0.163104   |          1    |               0.274919 |                  0.196212   | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | post_stress_stabilization_h10_target |             366 | 0.146516   |          1    |               0.284876 |                  0.159311   | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h20_composite       |             380 | 0.135203   |          1    |               0.280603 |                  0.183211   | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | recovery_quality_h10_composite       |             388 | 0.12265    |          1    |               0.291322 |                  0.149921   | none                 | True              |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h20_target |            1431 | 0.109989   |          1    |               0.333274 |                  0.196212   | none                 | True              |
| participation_liquidity_state_shift_20_60         | post_stress_stabilization_h10_target |            1431 | 0.0898494  |          1    |               0.331925 |                  0.159311   | none                 | True              |
| participation_liquidity_state_shift_20_60         | recovery_quality_h20_composite       |            2039 | 0.089397   |          1    |               0.319676 |                  0.183211   | none                 | True              |
| participation_liquidity_state_shift_20_60         | recovery_quality_h10_composite       |            2049 | 0.0701356  |          1    |               0.310295 |                  0.149921   | none                 | True              |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h20_forward_return |             379 | 0.0291066  |          0.75 |               0.351118 |                  0.0297673  | none                 | True              |
| volatility_compression_after_stress_stabilization | downside_controlled_h20_return       |             379 | 0.0270899  |          0.75 |               0.338074 |                  0.0193202  | none                 | True              |
| volatility_compression_after_stress_stabilization | drawdown_adjusted_h10_forward_return |             386 | 0.022889   |          0.75 |               0.453344 |                  0.0310001  | none                 | True              |
| volatility_compression_after_stress_stabilization | downside_controlled_h10_return       |             386 | 0.018049   |          0.75 |               0.453229 |                  0.00470683 | none                 | True              |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h20_forward_return |            2018 | 0.0160357  |          1    |               0.468308 |                  0.0297673  | none                 | True              |
| volatility_participation_asymmetry_20_original    | downside_controlled_h20_return       |            2018 | 0.01567    |          1    |               0.488028 |                  0.0193202  | none                 | True              |
| volatility_participation_asymmetry_20_original    | raw_h20_forward_return               |            2018 | 0.0121536  |          1    |               0.589666 |                  0.0273986  | none                 | True              |
| volatility_compression_after_stress_stabilization | raw_h20_forward_return               |             379 | 0.0110712  |          0.5  |               0.355608 |                  0.0273986  | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | raw_h10_forward_return               |             388 | 0.0102596  |          1    |               0.311045 |                  0.0209415  | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | drawdown_adjusted_h10_forward_return |             388 | 0.00998512 |          1    |               0.369942 |                  0.0310001  | none                 | True              |
| participation_breadth_repair_under_hostile_trend  | drawdown_adjusted_h10_forward_return |             380 | 0.00969524 |          0.5  |               0.416899 |                  0.0310001  | none                 | True              |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h20_forward_return |            1928 | 0.00965344 |          1    |               0.475462 |                  0.0297673  | none                 | True              |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h20_return       |            1928 | 0.00938769 |          1    |               0.456064 |                  0.0193202  | none                 | True              |
| volatility_participation_asymmetry_20_original    | drawdown_adjusted_h10_forward_return |            2028 | 0.00913114 |          0.75 |               0.370052 |                  0.0310001  | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | downside_controlled_h10_return       |             388 | 0.00870698 |          1    |               0.386712 |                  0.00470683 | none                 | True              |
| participation_liquidity_state_shift_20_60         | raw_h20_forward_return               |            2039 | 0.00842118 |          0.75 |               0.367216 |                  0.0273986  | none                 | True              |
| participation_liquidity_state_shift_20_60         | downside_controlled_h20_return       |            2039 | 0.00832839 |          0.75 |               0.331232 |                  0.0193202  | none                 | True              |
| participation_liquidity_state_shift_20_60         | drawdown_adjusted_h20_forward_return |            2039 | 0.00828612 |          0.75 |               0.351183 |                  0.0297673  | none                 | True              |
| volatility_participation_asymmetry_20_original    | downside_controlled_h10_return       |            2028 | 0.00814647 |          0.75 |               0.413773 |                  0.00470683 | none                 | True              |
| volatility_compression_after_stress_stabilization | raw_h10_forward_return               |             386 | 0.00762096 |          0.5  |               0.432679 |                  0.0209415  | none                 | True              |
| participation_breadth_repair_under_hostile_trend  | downside_controlled_h10_return       |             380 | 0.0071923  |          0.5  |               0.398754 |                  0.00470683 | none                 | True              |
| turnover_shock_exhaustion_repair_20               | drawdown_adjusted_h10_forward_return |            1938 | 0.00703003 |          0.75 |               0.543683 |                  0.0310001  | none                 | True              |
| turnover_shock_exhaustion_repair_20               | recovery_quality_h20_composite       |            1928 | 0.00691132 |          1    |               0.467633 |                  0.183211   | none                 | True              |
| volatility_participation_asymmetry_20_original    | raw_h10_forward_return               |            2028 | 0.00584314 |          0.75 |               0.47249  |                  0.0209415  | none                 | True              |
| turnover_shock_exhaustion_repair_20               | post_stress_stabilization_h20_target |            1380 | 0.00552911 |          1    |               0.338044 |                  0.196212   | none                 | True              |
| turnover_shock_exhaustion_repair_20               | downside_controlled_h10_return       |            1938 | 0.00543567 |          0.75 |               0.598218 |                  0.00470683 | none                 | True              |
| participation_breadth_repair_under_hostile_trend  | raw_h10_forward_return               |             380 | 0.00536315 |          0.75 |               0.330063 |                  0.0209415  | none                 | True              |
| participation_liquidity_state_shift_20_60         | downside_controlled_h10_return       |            2049 | 0.00510456 |          0.5  |               0.504253 |                  0.00470683 | none                 | True              |
| turnover_shock_exhaustion_repair_20               | raw_h20_forward_return               |            1928 | 0.00492666 |          0.75 |               0.471617 |                  0.0273986  | none                 | True              |
| participation_liquidity_state_shift_20_60         | raw_h10_forward_return               |            2049 | 0.00490851 |          0.5  |               0.487504 |                  0.0209415  | none                 | True              |
| short_horizon_volatility_shock_absorption_10      | drawdown_adjusted_h20_forward_return |             380 | 0.00458805 |          0.5  |               0.577447 |                  0.0297673  | none                 | True              |
| turnover_shock_exhaustion_repair_20               | recovery_quality_h10_composite       |            1938 | 0.00441413 |          0.75 |               0.498286 |                  0.149921   | none                 | True              |

## Research Questions

1. Do current inventory candidates improve materially under recovery-quality-oriented targets?

- Diagnostic answer: `3` candidate profiles showed a target-minus-raw improvement above the simple review threshold of 0.005. This is not a status change and must be reviewed alongside low-volatility and fragility warnings.

2. Do weak repair/stabilization candidates express value missed by raw IC?

- Diagnostic answer: alternative targets can surface different behavior, but this run does not convert weak clues into validation candidates. Any apparent improvement is a research clue only.

3. Which targets best align with surviving signal behavior?

- Use the target comparison and sensitivity tables. Preference should go to targets that improve interpretation without large low-volatility overlap or one-window dominance.

4. Are alternative targets identifying true structure or rewarding low-volatility/passive behavior?

- `0` target definitions crossed the low-volatility reward warning threshold. These require skepticism before any future target work.

5. Should future research separate alpha return prediction, recovery quality, stabilization quality, downside containment, and context usefulness?

- Yes. This experiment reinforces object-type separation: raw-return alpha prediction remains separate from recovery/risk diagnostics and context usefulness.

## Target Correlation Summary

The full target correlation matrix is saved as `target_correlation_matrix.csv`. High correlations between alternative targets and raw return should be treated as a sign that the alternative lens may not add much information.

## Interpretation Standard

A stronger alternative-target IC is not an alpha pass. It only suggests that a mechanism may be more naturally described as recovery quality, stabilization quality, or downside containment. Any future use would need pre-registered target formulas, anti-duplication diagnostics, sample-size checks, and separate governance.

## Recommended Next Step

Do not change validation standards. Review the diagnostic artifacts first. If one target family shows consistent, interpretable improvement without passive low-volatility reward or fragility, the next step should be a design-only governance note for target experiment standards before any additional implementation.

## Artifacts

- `candidate_registry.csv`
- `target_metadata.csv`
- `target_comparison_table.csv`
- `daily_ic_by_candidate_target.csv`
- `target_sensitivity_analysis.csv`
- `target_correlation_matrix.csv`
- `target_lowvol_overlap.csv`
- `wfv_target_summary.csv`
- `wfv_target_windows.csv`
- `drawdown_adjusted_ranking_comparison.csv`
- `recovery_quality_ranking_comparison.csv`
- `candidate_behavior_profiles.csv`
- `target_fragility_review.csv`
- `structural_summary.csv`
- `manifest.json`

## Intentional Non-Changes

This experiment did not:

- modify validation logic
- modify gates or thresholds
- change candidate statuses
- promote weak candidates
- replace raw h10/h20 IC as the primary validation anchor
- change portfolio, ML, blending, optimization, metadata, detector, governance, or production paths
- make production claims
