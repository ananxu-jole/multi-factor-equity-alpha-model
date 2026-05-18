# Robustness-First Discovery Expansion v3

## Executive Takeaway

Track B ran an isolated robustness-first standalone discovery batch under `robustness_first_discovery_expansion_v3`.

This v3 batch deliberately searched farther away from the v2 reversal-like manifold. It emphasized continuation, participation, leadership persistence, volatility/dispersion transitions, liquidity persistence, and gap continuation rather than fade-the-move formulas.

This was a research-only sidecar batch. It did not register any signals, mutate survivor/watchlist lists, alter gates, change schemas, run portfolio construction, use ML, or touch Conditional-Alpha paths.

Candidates tested: 15
Status counts: `{"REJECT_RESEARCH": 15}`

Final recommendation: do not carry any v3 candidate into further validation. Use the batch as negative evidence that the tested continuation/participation structures either inverted direction, failed persistence, or remained too close to existing baselines.

## Scope And Isolation

- Run ID: `robustness_first_discovery_expansion_v3`
- Artifact directory: `artifacts/research/robustness_first_discovery_expansion_v3`
- Track A volume governance remained separate.
- `volume_shock_reversal_stable_20` was used only as an orthogonality baseline, not promoted or modified.

## Candidate Set

| signal_name                                   | family                       | intuition                                                                                       | structural_difference                                                                 | expected_horizon   | expected_failure_mode                                     | run_id                                  | research_status       |
|:----------------------------------------------|:-----------------------------|:------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:-------------------|:----------------------------------------------------------|:----------------------------------------|:----------------------|
| trend_leadership_persistence_20_60            | trend_persistence            | Continuation in names with persistent 20-day leadership confirmed by 60-day trend.              | Continuation and rank persistence, not a fade of prior return.                        | h10-h20            | May duplicate plain momentum or trend-quality signals.    | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| multi_horizon_trend_agreement_5_20_60         | multi_horizon_agreement      | Continuation when short, medium, and longer momentum ranks agree.                               | Agreement filter across horizons rather than overextension reversal.                  | h10-h20            | Can become a smoothed momentum proxy.                     | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| rank_persistence_quality_20_60                | rank_stability               | Stable cross-sectional leadership measured by low rank volatility and positive rank level.      | Uses stability of rank leadership, not price dislocation.                             | h20                | Hidden trend-quality duplication.                         | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| breadth_participation_quality_20              | breadth_participation        | Continuation in names participating consistently in up days over the last month.                | Participation count and consistency rather than reversal magnitude.                   | h10-h20            | May be too close to momentum.                             | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| relative_strength_acceleration_20_60          | relative_strength            | Acceleration of benchmark-relative strength from 60-day baseline to 20-day behavior.            | Acceleration/deceleration of relative strength, not mean reversion.                   | h10-h20            | Can become noisy momentum acceleration.                   | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| relative_strength_deceleration_risk_20_60     | relative_strength            | Penalizes names whose relative strength is decelerating despite still-positive longer trend.    | Deterioration signal based on loss of leadership, not reversal after overshoot.       | h10-h20            | Weak IC or sign instability.                              | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| vol_regime_transition_momentum_20_60          | volatility_transition        | Continuation when volatility normalizes from elevated 20-day volatility toward 60-day baseline. | Volatility regime transition with continuation behavior, not volatility reversal.     | h10-h20            | May be defensive quality or low-vol duplication.          | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| range_compression_breakout_continuation_20    | volatility_transition        | Continuation after price exits compressed range with supportive close location.                 | Breakout continuation from compression, not fade after range expansion.               | h10-h20            | False breakouts and trend-transition whipsaw.             | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| dispersion_transition_leadership_20_60        | dispersion_transition        | Leadership continuation during rising cross-sectional dispersion transitions.                   | State transition in dispersion plus leadership, not cross-sectional extreme reversal. | h10-h20            | May reduce to momentum during high dispersion.            | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| dispersion_compression_quality_20_60          | dispersion_transition        | Quality continuation when dispersion compresses and rank leadership remains stable.             | Compression/stabilization of dispersion rather than reversal of extremes.             | h20                | May be too smooth or weak.                                | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| liquidity_improvement_momentum_20_60          | liquidity_persistence        | Momentum confirmed by improving dollar-volume liquidity over medium-term baseline.              | Liquidity improvement confirmation, not abnormal-flow reversal.                       | h10-h20            | Momentum/liquidity-size proxy duplication.                | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| liquidity_deterioration_warning_20_60         | liquidity_persistence        | Avoids names with deteriorating liquidity participation and weakening price behavior.           | Deterioration persistence rather than reversal after flow shock.                      | h10-h20            | Weak standalone return relationship.                      | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| gap_continuation_confirmation_5_20            | gap_continuation             | Continuation after overnight gap that is confirmed by intraday close strength and volume.       | Separates gap continuation from the prior gap-reversal watchlist behavior.            | h5-h10             | High turnover or event noise.                             | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| relative_volume_confirmed_leadership_20       | relative_volume_confirmation | Continuation where price leadership is confirmed by relative volume participation.              | Volume confirmation of leadership, not volume shock fade.                             | h10-h20            | May correlate with momentum and liquidity-flow baselines. | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |
| participation_trend_quality_interaction_20_60 | interaction                  | Continuation when participation quality and trend persistence agree.                            | Interaction of participation and trend quality, not fade of a move.                   | h10-h20            | Blend camouflage or trend-quality redundancy.             | robustness_first_discovery_expansion_v3 | TRACK_B_RESEARCH_ONLY |

## v2 Lessons Applied

Batch v2 showed that many plausible candidates collapsed into plain reversal, volume-shock reversal, or volatility-reversal baselines. Batch v3 therefore used those v2 panels, Track A volume governance panels, simple reversal/momentum baselines, and available current alpha-pool signal panels as redundancy references.

## Structural Quality Summary

| signal_name                                   |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |
|:----------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|
| trend_leadership_persistence_20_60            |     0.0426437 |     0.957356 |        0.969018 |        0.0374141 |      0.0575191 |
| multi_horizon_trend_agreement_5_20_60         |     0.0426437 |     0.957356 |        0.969018 |        0.0524002 |      0.0680389 |
| rank_persistence_quality_20_60                |     0.0421491 |     0.957851 |        0.969495 |        0.0186878 |      0.0235851 |
| breadth_participation_quality_20              |     0.0224192 |     0.977581 |        0.989514 |        0.0700368 |      0.102597  |
| relative_strength_acceleration_20_60          |     0.0412158 |     0.958784 |        0.970448 |        0.0704519 |      0.0983705 |
| relative_strength_deceleration_risk_20_60     |     0.0412158 |     0.958784 |        0.970448 |        0.0704519 |      0.0983705 |
| vol_regime_transition_momentum_20_60          |     0.0364493 |     0.963551 |        0.975214 |        0.0705183 |      0.0966318 |
| range_compression_breakout_continuation_20    |     0.0331128 |     0.966887 |        0.978551 |        0.0749345 |      0.131628  |
| dispersion_transition_leadership_20_60        |     0.0412158 |     0.958784 |        0.970448 |        0.0638406 |      0.0965419 |
| dispersion_compression_quality_20_60          |     0.0421491 |     0.957851 |        0.969495 |        0.0187647 |      0.0288261 |
| liquidity_improvement_momentum_20_60          |     0.0334708 |     0.966529 |        0.978551 |        0.0655714 |      0.0907341 |
| liquidity_deterioration_warning_20_60         |     0.0415488 |     0.958451 |        0.970448 |        0.0530908 |      0.0728547 |
| gap_continuation_confirmation_5_20            |     0.598506  |     0.401494 |        0.98999  |        0.24093   |      0.419218  |
| relative_volume_confirmed_leadership_20       |     0.0224252 |     0.977575 |        0.989514 |        0.07265   |      0.107677  |
| participation_trend_quality_interaction_20_60 |     0.0429768 |     0.957023 |        0.969018 |        0.037416  |      0.0573165 |

## IC / Horizon Behavior

| signal_name                                   |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:----------------------------------------------|----------:|------------:|--------------:|-----------:|-------------------:|----------:|
| liquidity_deterioration_warning_20_60         |        20 | -0.0176588  |    0.0176588  | -0.0951285 |           0.487103 |      2016 |
| multi_horizon_trend_agreement_5_20_60         |        20 | -0.0173314  |    0.0173314  | -0.094713  |           0.493294 |      2013 |
| vol_regime_transition_momentum_20_60          |        20 | -0.0166397  |    0.0166397  | -0.0944396 |           0.478776 |      2026 |
| trend_leadership_persistence_20_60            |        20 | -0.0145526  |    0.0145526  | -0.0809824 |           0.505216 |      2013 |
| participation_trend_quality_interaction_20_60 |        20 | -0.0143194  |    0.0143194  | -0.0797805 |           0.505216 |      2013 |
| liquidity_improvement_momentum_20_60          |        20 | -0.0137547  |    0.0137547  | -0.0847988 |           0.484014 |      2033 |
| breadth_participation_quality_20              |        20 | -0.0131231  |    0.0131231  | -0.0770149 |           0.49465  |      2056 |
| relative_volume_confirmed_leadership_20       |        20 | -0.0129298  |    0.0129298  | -0.0762355 |           0.498541 |      2056 |
| dispersion_transition_leadership_20_60        |        20 | -0.0121978  |    0.0121978  | -0.0765331 |           0.514385 |      2016 |
| relative_strength_acceleration_20_60          |        20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |      2016 |
| relative_strength_deceleration_risk_20_60     |        20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |      2016 |
| rank_persistence_quality_20_60                |        20 | -0.0107812  |    0.0107812  | -0.0572333 |           0.519861 |      2014 |
| dispersion_compression_quality_20_60          |        20 | -0.0104348  |    0.0104348  | -0.0554264 |           0.521847 |      2014 |
| gap_continuation_confirmation_5_20            |         1 | -0.00609112 |    0.00609112 | -0.0354603 |           0.49245  |      2053 |
| range_compression_breakout_continuation_20    |        20 | -0.00469198 |    0.00469198 | -0.039584  |           0.483855 |      2013 |

## WFV-Style Diagnostics

| signal_name                                   |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:----------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| gap_continuation_confirmation_5_20            |         1 |           4 |              -0.00609353 |              -1.60497  |          0    |               1    |               0.447953 |
| trend_leadership_persistence_20_60            |        20 |           4 |              -0.0145513  |              -0.821636 |          0.25 |               0.75 |               0.569116 |
| multi_horizon_trend_agreement_5_20_60         |        20 |           4 |              -0.0173249  |              -0.939876 |          0.25 |               0.75 |               0.419482 |
| rank_persistence_quality_20_60                |        20 |           4 |              -0.0107946  |              -0.548101 |          0.25 |               0.75 |               0.623873 |
| breadth_participation_quality_20              |        20 |           4 |              -0.0131231  |              -0.677336 |          0.25 |               0.75 |               0.371331 |
| relative_strength_acceleration_20_60          |        20 |           4 |              -0.011374   |              -0.472459 |          0.25 |               0.75 |               0.372597 |
| relative_strength_deceleration_risk_20_60     |        20 |           4 |              -0.011374   |              -0.472459 |          0.25 |               0.75 |               0.372597 |
| vol_regime_transition_momentum_20_60          |        20 |           4 |              -0.0166276  |              -0.792022 |          0.25 |               0.75 |               0.354494 |
| range_compression_breakout_continuation_20    |        20 |           4 |              -0.00468572 |              -0.550577 |          0.5  |               0.5  |               0.570962 |
| dispersion_transition_leadership_20_60        |        20 |           4 |              -0.0121978  |              -0.774296 |          0    |               1    |               0.804086 |
| dispersion_compression_quality_20_60          |        20 |           4 |              -0.010448   |              -0.532731 |          0.25 |               0.75 |               0.628896 |
| liquidity_improvement_momentum_20_60          |        20 |           4 |              -0.0137475  |              -0.775097 |          0.25 |               0.75 |               0.322414 |
| liquidity_deterioration_warning_20_60         |        20 |           4 |              -0.0176588  |              -1.0349   |          0.25 |               0.75 |               0.437533 |
| relative_volume_confirmed_leadership_20       |        20 |           4 |              -0.0129298  |              -0.6783   |          0.25 |               0.75 |               0.372685 |
| participation_trend_quality_interaction_20_60 |        20 |           4 |              -0.0143181  |              -0.812446 |          0.25 |               0.75 |               0.567998 |

## Stress / Regime Observations

Best-state slices by absolute mean IC:

| signal_name                                   |   horizon | state                  |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|:----------------------------------------------|----------:|:-----------------------|----------:|-----------:|----------:|-------------------:|
| liquidity_deterioration_warning_20_60         |        20 | panic_liquidity_stress |       187 | -0.0648603 | -0.235224 |           0.481283 |
| multi_horizon_trend_agreement_5_20_60         |        20 | panic_liquidity_stress |       187 | -0.0615971 | -0.226097 |           0.486631 |
| trend_leadership_persistence_20_60            |        20 | panic_liquidity_stress |       187 | -0.0565888 | -0.220647 |           0.491979 |
| participation_trend_quality_interaction_20_60 |        20 | panic_liquidity_stress |       187 | -0.055689  | -0.217291 |           0.491979 |
| rank_persistence_quality_20_60                |        20 | panic_liquidity_stress |       187 | -0.0546657 | -0.242655 |           0.486631 |
| liquidity_improvement_momentum_20_60          |        20 | panic_liquidity_stress |       187 | -0.0536322 | -0.235311 |           0.433155 |
| dispersion_compression_quality_20_60          |        20 | panic_liquidity_stress |       187 | -0.0535551 | -0.236025 |           0.486631 |
| vol_regime_transition_momentum_20_60          |        20 | panic_liquidity_stress |       187 | -0.0532576 | -0.21903  |           0.438503 |
| dispersion_transition_leadership_20_60        |        20 | panic_liquidity_stress |       187 | -0.0530617 | -0.22856  |           0.470588 |
| relative_volume_confirmed_leadership_20       |        20 | panic_liquidity_stress |       187 | -0.0507952 | -0.215843 |           0.454545 |
| breadth_participation_quality_20              |        20 | panic_liquidity_stress |       187 | -0.0501603 | -0.212942 |           0.454545 |
| liquidity_deterioration_warning_20_60         |        20 | volatility_spike       |       393 | -0.0482873 | -0.202678 |           0.455471 |
| dispersion_transition_leadership_20_60        |        20 | volatility_spike       |       393 | -0.0453651 | -0.214346 |           0.465649 |
| trend_leadership_persistence_20_60            |        20 | volatility_spike       |       393 | -0.0439633 | -0.189873 |           0.473282 |
| multi_horizon_trend_agreement_5_20_60         |        20 | volatility_spike       |       393 | -0.0437358 | -0.188767 |           0.447837 |
| participation_trend_quality_interaction_20_60 |        20 | volatility_spike       |       393 | -0.0434976 | -0.187951 |           0.470738 |
| multi_horizon_trend_agreement_5_20_60         |        20 | drawdown_acceleration  |       349 | -0.0424478 | -0.179604 |           0.504298 |
| liquidity_deterioration_warning_20_60         |        20 | drawdown_acceleration  |       350 | -0.0412952 | -0.17475  |           0.482857 |
| liquidity_deterioration_warning_20_60         |        20 | weak_breadth           |       508 | -0.0394816 | -0.174414 |           0.440945 |
| multi_horizon_trend_agreement_5_20_60         |        20 | weak_breadth           |       508 | -0.0393115 | -0.173864 |           0.456693 |

## Orthogonality Summary

| signal_name                                   |   max_abs_corr |
|:----------------------------------------------|---------------:|
| relative_strength_acceleration_20_60          |       1        |
| relative_strength_deceleration_risk_20_60     |       1        |
| vol_regime_transition_momentum_20_60          |       0.982599 |
| breadth_participation_quality_20              |       0.95268  |
| relative_volume_confirmed_leadership_20       |       0.946133 |
| liquidity_improvement_momentum_20_60          |       0.939264 |
| liquidity_deterioration_warning_20_60         |       0.874198 |
| multi_horizon_trend_agreement_5_20_60         |       0.866103 |
| trend_leadership_persistence_20_60            |       0.827186 |
| participation_trend_quality_interaction_20_60 |       0.824701 |
| dispersion_transition_leadership_20_60        |       0.750829 |
| dispersion_compression_quality_20_60          |       0.747629 |
| rank_persistence_quality_20_60                |       0.747214 |
| range_compression_breakout_continuation_20    |       0.450169 |
| gap_continuation_confirmation_5_20            |       0.322287 |

Important: high baseline correlation is treated as a review or rejection reason even when IC is positive.

## Candidate Decisions

| signal_name                                   | family                       |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency | status          | review_issues                                                                                                    |
|:----------------------------------------------|:-----------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|:----------------|:-----------------------------------------------------------------------------------------------------------------|
| liquidity_deterioration_warning_20_60         | liquidity_persistence        |             20 | -0.0176588  |    0.0176588  | -0.0951285 |           0.487103 |        0.0530908 |     0.0415488 |                0.874198 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| multi_horizon_trend_agreement_5_20_60         | multi_horizon_agreement      |             20 | -0.0173314  |    0.0173314  | -0.094713  |           0.493294 |        0.0524002 |     0.0426437 |                0.866103 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| vol_regime_transition_momentum_20_60          | volatility_transition        |             20 | -0.0166397  |    0.0166397  | -0.0944396 |           0.478776 |        0.0705183 |     0.0364493 |                0.982599 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| trend_leadership_persistence_20_60            | trend_persistence            |             20 | -0.0145526  |    0.0145526  | -0.0809824 |           0.505216 |        0.0374141 |     0.0426437 |                0.827186 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| participation_trend_quality_interaction_20_60 | interaction                  |             20 | -0.0143194  |    0.0143194  | -0.0797805 |           0.505216 |        0.037416  |     0.0429768 |                0.824701 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| liquidity_improvement_momentum_20_60          | liquidity_persistence        |             20 | -0.0137547  |    0.0137547  | -0.0847988 |           0.484014 |        0.0655714 |     0.0334708 |                0.939264 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| breadth_participation_quality_20              | breadth_participation        |             20 | -0.0131231  |    0.0131231  | -0.0770149 |           0.49465  |        0.0700368 |     0.0224192 |                0.95268  |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| relative_volume_confirmed_leadership_20       | relative_volume_confirmation |             20 | -0.0129298  |    0.0129298  | -0.0762355 |           0.498541 |        0.07265   |     0.0224252 |                0.946133 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| dispersion_transition_leadership_20_60        | dispersion_transition        |             20 | -0.0121978  |    0.0121978  | -0.0765331 |           0.514385 |        0.0638406 |     0.0412158 |                0.750829 |              0    |                   1    | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; high_baseline_similarity                                               |
| relative_strength_acceleration_20_60          | relative_strength            |             20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |        0.0704519 |     0.0412158 |                1        |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| relative_strength_deceleration_risk_20_60     | relative_strength            |             20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |        0.0704519 |     0.0412158 |                1        |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| rank_persistence_quality_20_60                | rank_stability               |             20 | -0.0107812  |    0.0107812  | -0.0572333 |           0.519861 |        0.0186878 |     0.0421491 |                0.747214 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; moderate_baseline_similarity                                           |
| dispersion_compression_quality_20_60          | dispersion_transition        |             20 | -0.0104348  |    0.0104348  | -0.0554264 |           0.521847 |        0.0187647 |     0.0421491 |                0.747629 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; moderate_baseline_similarity                                           |
| gap_continuation_confirmation_5_20            | gap_continuation             |              1 | -0.00609112 |    0.00609112 | -0.0354603 |           0.49245  |        0.24093   |     0.598506  |                0.322287 |              0    |                   1    | REJECT_RESEARCH | high_missingness; high_turnover; direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                 |
| range_compression_breakout_continuation_20    | volatility_transition        |             20 | -0.00469198 |    0.00469198 | -0.039584  |           0.483855 |        0.0749345 |     0.0331128 |                0.450169 |              0.5  |                   0.5  | REJECT_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |

## Watchlist / Further Validation Candidates

No candidates advanced to watchlist or further-validation status.

## Rejected Candidates

| signal_name                                   | family                       |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency | status          | review_issues                                                                                                    |
|:----------------------------------------------|:-----------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|:----------------|:-----------------------------------------------------------------------------------------------------------------|
| liquidity_deterioration_warning_20_60         | liquidity_persistence        |             20 | -0.0176588  |    0.0176588  | -0.0951285 |           0.487103 |        0.0530908 |     0.0415488 |                0.874198 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| multi_horizon_trend_agreement_5_20_60         | multi_horizon_agreement      |             20 | -0.0173314  |    0.0173314  | -0.094713  |           0.493294 |        0.0524002 |     0.0426437 |                0.866103 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| vol_regime_transition_momentum_20_60          | volatility_transition        |             20 | -0.0166397  |    0.0166397  | -0.0944396 |           0.478776 |        0.0705183 |     0.0364493 |                0.982599 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| trend_leadership_persistence_20_60            | trend_persistence            |             20 | -0.0145526  |    0.0145526  | -0.0809824 |           0.505216 |        0.0374141 |     0.0426437 |                0.827186 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| participation_trend_quality_interaction_20_60 | interaction                  |             20 | -0.0143194  |    0.0143194  | -0.0797805 |           0.505216 |        0.037416  |     0.0429768 |                0.824701 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| liquidity_improvement_momentum_20_60          | liquidity_persistence        |             20 | -0.0137547  |    0.0137547  | -0.0847988 |           0.484014 |        0.0655714 |     0.0334708 |                0.939264 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| breadth_participation_quality_20              | breadth_participation        |             20 | -0.0131231  |    0.0131231  | -0.0770149 |           0.49465  |        0.0700368 |     0.0224192 |                0.95268  |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| relative_volume_confirmed_leadership_20       | relative_volume_confirmation |             20 | -0.0129298  |    0.0129298  | -0.0762355 |           0.498541 |        0.07265   |     0.0224252 |                0.946133 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| dispersion_transition_leadership_20_60        | dispersion_transition        |             20 | -0.0121978  |    0.0121978  | -0.0765331 |           0.514385 |        0.0638406 |     0.0412158 |                0.750829 |              0    |                   1    | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; high_baseline_similarity                                               |
| relative_strength_acceleration_20_60          | relative_strength            |             20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |        0.0704519 |     0.0412158 |                1        |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| relative_strength_deceleration_risk_20_60     | relative_strength            |             20 | -0.011374   |    0.011374   | -0.0685914 |           0.462302 |        0.0704519 |     0.0412158 |                1        |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity                        |
| rank_persistence_quality_20_60                | rank_stability               |             20 | -0.0107812  |    0.0107812  | -0.0572333 |           0.519861 |        0.0186878 |     0.0421491 |                0.747214 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; moderate_baseline_similarity                                           |
| dispersion_compression_quality_20_60          | dispersion_transition        |             20 | -0.0104348  |    0.0104348  | -0.0554264 |           0.521847 |        0.0187647 |     0.0421491 |                0.747629 |              0.25 |                   0.75 | REJECT_RESEARCH | direction_mismatch; weak_wfv_persistence; moderate_baseline_similarity                                           |
| gap_continuation_confirmation_5_20            | gap_continuation             |              1 | -0.00609112 |    0.00609112 | -0.0354603 |           0.49245  |        0.24093   |     0.598506  |                0.322287 |              0    |                   1    | REJECT_RESEARCH | high_missingness; high_turnover; direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                 |
| range_compression_breakout_continuation_20    | volatility_transition        |             20 | -0.00469198 |    0.00469198 | -0.039584  |           0.483855 |        0.0749345 |     0.0331128 |                0.450169 |              0.5  |                   0.5  | REJECT_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |

## Lessons Learned

- Track B can move faster without loosening rejection discipline.
- Orthogonality checks should remain early in discovery, especially versus plain reversal, momentum, and Track A volume reversal.
- Several candidates can show plausible IC while still failing persistence, sign consistency, or redundancy checks.
- State-specific strength remains diagnostic only; it does not turn a standalone candidate into a conditional-alpha path.

## Recommended Next Batch

Do not refine these v3 candidates directly. The next Track B batch should move farther from price-rank continuation and reversal-adjacent structure, with emphasis on sector/peer-relative mechanisms, fundamental-quality proxies if available, or cleaner non-price liquidity/participation primitives before any onboarding-style work.
