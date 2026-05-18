# Robustness-First Discovery Expansion v4

## Executive Takeaway

Track B ran an isolated mechanism-redesign discovery batch under `robustness_first_discovery_expansion_v4`.

This batch used the v3 failure diagnostics to avoid superficial continuation variants, simple inversions, and price-rank reversal proxies. Candidates were redesigned around early formation, non-price liquidity persistence, pre-extension participation, cleaner gap/range structures, rank stability before acceleration, and conditional low-overextension activation.

This was research-only. It did not register signals, mutate survivor/watchlist lists, alter gates, change schemas, run portfolio construction, use ML, or touch Conditional-Alpha production paths.

Candidates tested: 12
Status counts: `{"CONDITIONAL_ONLY_RESEARCH": 4, "REJECT_RESEARCH": 8}`

## v3 Diagnostics Used

- Failure diagnostics source: `artifacts/research/track_b_v3_failure_diagnostics`
- Key applied lesson: avoid mature price-rank leadership and do not treat sign inversion as a new mechanism.
- Track A `volume_shock_reversal_stable_20` remained an orthogonality baseline only.

## Candidate Set

| signal_name                                | family                    | redesigned_mechanism                                                                             | addresses_v3_failure                                                                                   | non_reversal_rationale                                                                                           | expected_horizon   | run_id                                  | research_status       |
|:-------------------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|:-------------------|:----------------------------------------|:----------------------|
| early_leadership_formation_5_20            | early_leadership          | New 5-day relative leadership forming before 20-day overextension.                               | Redesigns trend_leadership_persistence_20_60 away from mature trend chasing.                           | Scores early formation under a low-overextension filter rather than fading a prior move.                         | h5-h10             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| pre_extension_participation_improvement_20 | breadth_participation     | Improving up-day participation before large 20-day price extension.                              | Moves breadth_participation_quality_20 from price-confirmed leadership to pre-extension participation. | Uses participation acceleration with neutral/modest price move constraints, not reversal or mature continuation. | h5-h20             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| nonprice_liquidity_persistence_20_60       | liquidity_persistence     | Persistent dollar-volume improvement neutralized against 20-day return rank.                     | Rebuilds liquidity_improvement_momentum_20_60 around non-price liquidity persistence.                  | Removes direct price-rank multiplication and penalizes price exposure.                                           | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| liquidity_participation_accumulation_20    | liquidity_participation   | Volume participation accumulation on non-negative days without strong price extension.           | Separates accumulation from abnormal-flow reversal and price-rank leadership.                          | Looks for persistent participation quality, not a fade after volume shock.                                       | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| vol_compression_confirmation_20_60         | volatility_compression    | Stable volatility compression confirmed by range location and low jumpiness.                     | Redesigns range_compression_breakout_continuation_20 with stronger confirmation before expansion.      | Compression quality is the main primitive; price direction is only a mild confirmation.                          | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| clean_range_expansion_followthrough_20     | breakout_quality          | Clean range expansion after compression with low gap noise and close-location confirmation.      | Separates clean expansion from noisy chase behavior in breakout continuation.                          | Requires prior compression and low noise; does not invert breakout failures.                                     | h5-h10             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| gap_followthrough_low_churn_10             | gap_structure             | Smoothed gap follow-through with lower event threshold and persistence to reduce sparsity/churn. | Redesigns gap_continuation_confirmation_5_20 to reduce missingness and turnover.                       | Measures confirmed follow-through persistence, not gap reversal.                                                 | h5-h10             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| rank_stability_before_acceleration_20_60   | rank_stability            | Stable improving rank before top-decile acceleration and overextension.                          | Replaces relative_strength_acceleration_20_60 with pre-acceleration rank quality.                      | Avoids mature extremes and does not invert acceleration.                                                         | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| low_overextension_trend_resumption_10_40   | regime_gated_continuation | Trend resumption only when 40-day return is moderate and volatility is not elevated.             | Keeps continuation only when overextension risk is low.                                                | Conditional continuation gate avoids always-on reversal behavior and late chase entries.                         | h5-h20             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| dispersion_transition_nonprice_quality_20  | dispersion_transition     | Cross-sectional dispersion transition combined with low idiosyncratic volatility rank.           | Moves dispersion ideas away from price-rank leadership.                                                | State-transition and stability feature, not price-rank or reversal.                                              | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| participation_liquidity_state_shift_20_60  | state_shift               | Joint improvement in participation and liquidity, neutralized against 20-day return rank.        | Combines participation and liquidity without letting price rank dominate.                              | State-shift feature based on market participation primitives.                                                    | h10-h20            | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |
| conditional_low_overextension_breakout_20  | conditional_breakout      | Breakout quality active only when overextension and volatility-spike risk are low.               | Moves weak breakout continuation into conditional-only research.                                       | Conditional activation avoids always-on reversal behavior and noisy chase states.                                | h5-h10             | robustness_first_discovery_expansion_v4 | TRACK_B_RESEARCH_ONLY |

## Structural Quality And Turnover

| signal_name                                |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |
|:-------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|
| early_leadership_formation_5_20            |     0.0245332 |     0.975467 |        0.987131 |        0.135237  |      0.173733  |
| pre_extension_participation_improvement_20 |     0.0239928 |     0.976007 |        0.987607 |        0.113453  |      0.186433  |
| nonprice_liquidity_persistence_20_60       |     0.0349027 |     0.965097 |        0.977121 |        0.142576  |      0.355926  |
| liquidity_participation_accumulation_20    |     0.0224322 |     0.977568 |        0.989514 |        0.0915706 |      0.117566  |
| vol_compression_confirmation_20_60         |     0.032005  |     0.967995 |        0.979981 |        0.0730068 |      0.122369  |
| clean_range_expansion_followthrough_20     |     0.0381884 |     0.961812 |        0.973785 |        0.0555763 |      0.135599  |
| gap_followthrough_low_churn_10             |     0.0183329 |     0.981667 |        0.993327 |        0.101866  |      0.127352  |
| rank_stability_before_acceleration_20_60   |     0.0421671 |     0.957833 |        0.969495 |        0.0662982 |      0.0883912 |
| low_overextension_trend_resumption_10_40   |     0.0316829 |     0.968317 |        0.979981 |        0.106076  |      0.146127  |
| dispersion_transition_nonprice_quality_20  |     0.02215   |     0.97785  |        0.989514 |        0.0454323 |      0.0707098 |
| participation_liquidity_state_shift_20_60  |     0.0306089 |     0.969391 |        0.981411 |        0.216332  |      0.336642  |
| conditional_low_overextension_breakout_20  |     0.0362858 |     0.963714 |        0.975691 |        0.0553322 |      0.16926   |

## IC / Horizon Behavior

| signal_name                                |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:-------------------------------------------|----------:|------------:|--------------:|-----------:|-------------------:|----------:|
| dispersion_transition_nonprice_quality_20  |        20 | -0.0243755  |    0.0243755  | -0.120092  |           0.482004 |      2056 |
| low_overextension_trend_resumption_10_40   |        20 | -0.0118005  |    0.0118005  | -0.0833164 |           0.472004 |      2036 |
| rank_stability_before_acceleration_20_60   |         5 | -0.00884402 |    0.00884402 | -0.0659352 |           0.472647 |      2029 |
| participation_liquidity_state_shift_20_60  |        20 |  0.00842118 |    0.00842118 |  0.072874  |           0.509564 |      2039 |
| conditional_low_overextension_breakout_20  |        20 | -0.00628854 |    0.00628854 | -0.068343  |           0.450806 |      1240 |
| vol_compression_confirmation_20_60         |        20 | -0.00593541 |    0.00593541 | -0.0605374 |           0.480731 |      2024 |
| pre_extension_participation_improvement_20 |         1 | -0.00578897 |    0.00578897 | -0.0459749 |           0.47803  |      2071 |
| clean_range_expansion_followthrough_20     |        20 | -0.00493606 |    0.00493606 | -0.0692742 |           0.457333 |      1957 |
| early_leadership_formation_5_20            |         1 | -0.00308332 |    0.00308332 | -0.0190787 |           0.504831 |      2070 |
| liquidity_participation_accumulation_20    |        10 | -0.00283476 |    0.00283476 | -0.0271422 |           0.50726  |      2066 |
| gap_followthrough_low_churn_10             |        10 | -0.00251565 |    0.00251565 | -0.0263586 |           0.485535 |      2074 |
| nonprice_liquidity_persistence_20_60       |        20 |  0.00231258 |    0.00231258 |  0.0271643 |           0.510837 |      2030 |

## WFV-Style Diagnostics

| signal_name                                |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| early_leadership_formation_5_20            |         1 |           4 |              -0.00308431 |              -0.76986  |          0.25 |               0.75 |               0.392926 |
| pre_extension_participation_improvement_20 |         1 |           4 |              -0.00578893 |              -5.7132   |          0    |               1    |               0.310641 |
| rank_stability_before_acceleration_20_60   |         5 |           4 |              -0.00883942 |              -1.48124  |          0    |               1    |               0.513777 |
| liquidity_participation_accumulation_20    |        10 |           4 |              -0.00283894 |              -0.501248 |          0.25 |               0.75 |               0.37943  |
| gap_followthrough_low_churn_10             |        10 |           4 |              -0.00251435 |              -0.318411 |          0.5  |               0.5  |               0.39527  |
| nonprice_liquidity_persistence_20_60       |        20 |           4 |               0.00230262 |               0.201817 |          0.5  |               0.5  |               0.409339 |
| vol_compression_confirmation_20_60         |        20 |           4 |              -0.00593541 |              -0.541247 |          0.5  |               0.5  |               0.392581 |
| clean_range_expansion_followthrough_20     |        20 |           4 |              -0.00494099 |              -0.840247 |          0.25 |               0.75 |               0.332121 |
| low_overextension_trend_resumption_10_40   |        20 |           4 |              -0.0118005  |              -1.20074  |          0    |               1    |               0.566929 |
| dispersion_transition_nonprice_quality_20  |        20 |           4 |              -0.0243755  |              -1.55337  |          0.25 |               0.75 |               0.380312 |
| participation_liquidity_state_shift_20_60  |        20 |           4 |               0.00840796 |               0.509123 |          0.75 |               0.75 |               0.367216 |
| conditional_low_overextension_breakout_20  |        20 |           4 |              -0.00628854 |              -0.42615  |          0.25 |               0.75 |               0.501165 |

## Orthogonality / Redundancy

| signal_name                                |   max_abs_corr |
|:-------------------------------------------|---------------:|
| dispersion_transition_nonprice_quality_20  |       0.769659 |
| low_overextension_trend_resumption_10_40   |       0.735066 |
| vol_compression_confirmation_20_60         |       0.584629 |
| rank_stability_before_acceleration_20_60   |       0.489297 |
| participation_liquidity_state_shift_20_60  |       0.469409 |
| early_leadership_formation_5_20            |       0.442444 |
| pre_extension_participation_improvement_20 |       0.408813 |
| conditional_low_overextension_breakout_20  |       0.340879 |
| clean_range_expansion_followthrough_20     |       0.293506 |
| nonprice_liquidity_persistence_20_60       |       0.271689 |
| liquidity_participation_accumulation_20    |       0.236251 |
| gap_followthrough_low_churn_10             |       0.109793 |

## Regime / Stress Behavior

| signal_name                                |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:-------------------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| conditional_low_overextension_breakout_20  |        20 | volatility_spike         |        44 |  0.0323855   |  0.376086   |           0.636364 |
| participation_liquidity_state_shift_20_60  |        20 | drawdown_acceleration    |       358 |  0.0199288   |  0.141398   |           0.53352  |
| participation_liquidity_state_shift_20_60  |        20 | panic_liquidity_stress   |       187 |  0.0191612   |  0.128804   |           0.491979 |
| gap_followthrough_low_churn_10             |        10 | recovery_phase           |       196 |  0.0176821   |  0.178408   |           0.530612 |
| nonprice_liquidity_persistence_20_60       |        20 | trend_transition         |       559 |  0.0176455   |  0.216552   |           0.572451 |
| conditional_low_overextension_breakout_20  |        20 | panic_liquidity_stress   |        24 |  0.0147179   |  0.240606   |           0.541667 |
| nonprice_liquidity_persistence_20_60       |        20 | high_dispersion_rotation |       570 |  0.0101477   |  0.112897   |           0.515789 |
| clean_range_expansion_followthrough_20     |        20 | trend_transition         |       533 |  0.00576545  |  0.0855111  |           0.514071 |
| gap_followthrough_low_churn_10             |        10 | high_dispersion_rotation |       574 |  0.00575739  |  0.0609844  |           0.527875 |
| early_leadership_formation_5_20            |         1 | panic_liquidity_stress   |       187 |  0.0035456   |  0.0207651  |           0.540107 |
| clean_range_expansion_followthrough_20     |        20 | drawdown_acceleration    |       349 | -0.000802513 | -0.00900591 |           0.504298 |
| low_overextension_trend_resumption_10_40   |        20 | high_dispersion_rotation |       570 | -0.000847157 | -0.00550588 |           0.5      |
| rank_stability_before_acceleration_20_60   |         5 | high_dispersion_rotation |       579 | -0.0025692   | -0.0183112  |           0.497409 |
| early_leadership_formation_5_20            |         1 | weak_breadth             |       508 | -0.0030284   | -0.0183586  |           0.511811 |
| pre_extension_participation_improvement_20 |         1 | panic_liquidity_stress   |       187 | -0.0031719   | -0.0214863  |           0.513369 |
| low_overextension_trend_resumption_10_40   |        20 | recovery_phase           |       196 | -0.00444483  | -0.0351589  |           0.47449  |
| liquidity_participation_accumulation_20    |        10 | high_dispersion_rotation |       574 | -0.00467593  | -0.0431996  |           0.494774 |
| pre_extension_participation_improvement_20 |         1 | weak_breadth             |       508 | -0.00488686  | -0.03552    |           0.482283 |
| liquidity_participation_accumulation_20    |        10 | volatility_spike         |       403 | -0.00542626  | -0.0481317  |           0.523573 |
| dispersion_transition_nonprice_quality_20  |        20 | high_dispersion_rotation |       570 | -0.00646796  | -0.0311025  |           0.515789 |
| rank_stability_before_acceleration_20_60   |         5 | recovery_phase           |       196 | -0.00691049  | -0.0476185  |           0.454082 |
| vol_compression_confirmation_20_60         |        20 | high_dispersion_rotation |       558 | -0.0112951   | -0.130339   |           0.462366 |
| vol_compression_confirmation_20_60         |        20 | weak_breadth             |       496 | -0.0129967   | -0.130285   |           0.439516 |
| dispersion_transition_nonprice_quality_20  |        20 | recovery_phase           |       196 | -0.0218268   | -0.0943596  |           0.505102 |

## Candidate Decisions

| signal_name                                | family                    |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status                    | review_issues                                                                                                    |
|:-------------------------------------------|:--------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:--------------------------|:-----------------------------------------------------------------------------------------------------------------|
| participation_liquidity_state_shift_20_60  | state_shift               |             20 |  0.00842118 |    0.00842118 |  0.072874  |           0.509564 |        0.216332  |     0.0306089 |                0.469409 |              0.75 |                   0.75 |                       5 |      0.0199288   | CONDITIONAL_ONLY_RESEARCH | high_turnover; weak_positive_ic_rate                                                                             |
| conditional_low_overextension_breakout_20  | conditional_breakout      |             20 | -0.00628854 |    0.00628854 | -0.068343  |           0.450806 |        0.0553322 |     0.0362858 |                0.340879 |              0.25 |                   0.75 |                       2 |      0.0323855   | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| gap_followthrough_low_churn_10             | gap_structure             |             10 | -0.00251565 |    0.00251565 | -0.0263586 |           0.485535 |        0.101866  |     0.0183329 |                0.109793 |              0.5  |                   0.5  |                       4 |      0.0176821   | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |
| nonprice_liquidity_persistence_20_60       | liquidity_persistence     |             20 |  0.00231258 |    0.00231258 |  0.0271643 |           0.510837 |        0.142576  |     0.0349027 |                0.271689 |              0.5  |                   0.5  |                       2 |      0.0176455   | CONDITIONAL_ONLY_RESEARCH | weak_best_horizon_ic; weak_wfv_persistence; weak_wfv_sign_consistency                                            |
| dispersion_transition_nonprice_quality_20  | dispersion_transition     |             20 | -0.0243755  |    0.0243755  | -0.120092  |           0.482004 |        0.0454323 |     0.02215   |                0.769659 |              0.25 |                   0.75 |                       0 |     -0.00646796  | REJECT_RESEARCH           | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| low_overextension_trend_resumption_10_40   | regime_gated_continuation |             20 | -0.0118005  |    0.0118005  | -0.0833164 |           0.472004 |        0.106076  |     0.0316829 |                0.735066 |              0    |                   1    |                       0 |     -0.000847157 | REJECT_RESEARCH           | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; moderate_baseline_similarity                    |
| rank_stability_before_acceleration_20_60   | rank_stability            |              5 | -0.00884402 |    0.00884402 | -0.0659352 |           0.472647 |        0.0662982 |     0.0421671 |                0.489297 |              0    |                   1    |                       0 |     -0.0025692   | REJECT_RESEARCH           | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| vol_compression_confirmation_20_60         | volatility_compression    |             20 | -0.00593541 |    0.00593541 | -0.0605374 |           0.480731 |        0.0730068 |     0.032005  |                0.584629 |              0.5  |                   0.5  |                       0 |     -0.0112951   | REJECT_RESEARCH           | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency                       |
| pre_extension_participation_improvement_20 | breadth_participation     |              1 | -0.00578897 |    0.00578897 | -0.0459749 |           0.47803  |        0.113453  |     0.0239928 |                0.408813 |              0    |                   1    |                       0 |     -0.0031719   | REJECT_RESEARCH           | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| clean_range_expansion_followthrough_20     | breakout_quality          |             20 | -0.00493606 |    0.00493606 | -0.0692742 |           0.457333 |        0.0555763 |     0.0381884 |                0.293506 |              0.25 |                   0.75 |                       1 |      0.00576545  | REJECT_RESEARCH           | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence                            |
| early_leadership_formation_5_20            | early_leadership          |              1 | -0.00308332 |    0.00308332 | -0.0190787 |           0.504831 |        0.135237  |     0.0245332 |                0.442444 |              0.25 |                   0.75 |                       1 |      0.0035456   | REJECT_RESEARCH           | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence                            |
| liquidity_participation_accumulation_20    | liquidity_participation   |             10 | -0.00283476 |    0.00283476 | -0.0271422 |           0.50726  |        0.0915706 |     0.0224322 |                0.236251 |              0.25 |                   0.75 |                       0 |     -0.00467593  | REJECT_RESEARCH           | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence                            |

## Actionable Research Candidates

| signal_name                               | family                |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status                    | review_issues                                                                                                    |
|:------------------------------------------|:----------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:--------------------------|:-----------------------------------------------------------------------------------------------------------------|
| participation_liquidity_state_shift_20_60 | state_shift           |             20 |  0.00842118 |    0.00842118 |  0.072874  |           0.509564 |        0.216332  |     0.0306089 |                0.469409 |              0.75 |                   0.75 |                       5 |        0.0199288 | CONDITIONAL_ONLY_RESEARCH | high_turnover; weak_positive_ic_rate                                                                             |
| conditional_low_overextension_breakout_20 | conditional_breakout  |             20 | -0.00628854 |    0.00628854 | -0.068343  |           0.450806 |        0.0553322 |     0.0362858 |                0.340879 |              0.25 |                   0.75 |                       2 |        0.0323855 | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| gap_followthrough_low_churn_10            | gap_structure         |             10 | -0.00251565 |    0.00251565 | -0.0263586 |           0.485535 |        0.101866  |     0.0183329 |                0.109793 |              0.5  |                   0.5  |                       4 |        0.0176821 | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |
| nonprice_liquidity_persistence_20_60      | liquidity_persistence |             20 |  0.00231258 |    0.00231258 |  0.0271643 |           0.510837 |        0.142576  |     0.0349027 |                0.271689 |              0.5  |                   0.5  |                       2 |        0.0176455 | CONDITIONAL_ONLY_RESEARCH | weak_best_horizon_ic; weak_wfv_persistence; weak_wfv_sign_consistency                                            |

## Rejected Candidates

| signal_name                                | family                    |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status          | review_issues                                                                                 |
|:-------------------------------------------|:--------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:----------------|:----------------------------------------------------------------------------------------------|
| dispersion_transition_nonprice_quality_20  | dispersion_transition     |             20 | -0.0243755  |    0.0243755  | -0.120092  |           0.482004 |        0.0454323 |     0.02215   |                0.769659 |              0.25 |                   0.75 |                       0 |     -0.00646796  | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity     |
| low_overextension_trend_resumption_10_40   | regime_gated_continuation |             20 | -0.0118005  |    0.0118005  | -0.0833164 |           0.472004 |        0.106076  |     0.0316829 |                0.735066 |              0    |                   1    |                       0 |     -0.000847157 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; moderate_baseline_similarity |
| rank_stability_before_acceleration_20_60   | rank_stability            |              5 | -0.00884402 |    0.00884402 | -0.0659352 |           0.472647 |        0.0662982 |     0.0421671 |                0.489297 |              0    |                   1    |                       0 |     -0.0025692   | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                               |
| vol_compression_confirmation_20_60         | volatility_compression    |             20 | -0.00593541 |    0.00593541 | -0.0605374 |           0.480731 |        0.0730068 |     0.032005  |                0.584629 |              0.5  |                   0.5  |                       0 |     -0.0112951   | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency    |
| pre_extension_participation_improvement_20 | breadth_participation     |              1 | -0.00578897 |    0.00578897 | -0.0459749 |           0.47803  |        0.113453  |     0.0239928 |                0.408813 |              0    |                   1    |                       0 |     -0.0031719   | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                               |
| clean_range_expansion_followthrough_20     | breakout_quality          |             20 | -0.00493606 |    0.00493606 | -0.0692742 |           0.457333 |        0.0555763 |     0.0381884 |                0.293506 |              0.25 |                   0.75 |                       1 |      0.00576545  | REJECT_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence         |
| early_leadership_formation_5_20            | early_leadership          |              1 | -0.00308332 |    0.00308332 | -0.0190787 |           0.504831 |        0.135237  |     0.0245332 |                0.442444 |              0.25 |                   0.75 |                       1 |      0.0035456   | REJECT_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence         |
| liquidity_participation_accumulation_20    | liquidity_participation   |             10 | -0.00283476 |    0.00283476 | -0.0271422 |           0.50726  |        0.0915706 |     0.0224322 |                0.236251 |              0.25 |                   0.75 |                       0 |     -0.00467593  | REJECT_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence         |

## Lessons Learned

- Mechanism redesign reduced some reversal similarity, but orthogonality alone is still not enough.
- Gap and breakout redesigns should be judged first on coverage and turnover before IC.
- Non-price liquidity and participation features should remain separated from direct price-rank multipliers.
- Conditional-only status is research-only and does not create a promotion path.

## Recommended Next Step

Carry forward only candidates with `WATCHLIST_RESEARCH`, `CONDITIONAL_ONLY_RESEARCH`, or `CANDIDATE_FOR_FURTHER_VALIDATION` for targeted diagnostics. Do not register or promote any v4 signal without a separate controlled validation step.
