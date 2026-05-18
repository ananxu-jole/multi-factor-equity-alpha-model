# Robustness-First Discovery Expansion v2

## Executive Takeaway

Track B ran an isolated robustness-first standalone discovery batch under `robustness_first_discovery_expansion_v2`.

This was a research-only sidecar batch. It did not register any signals, mutate survivor/watchlist lists, alter gates, change schemas, run portfolio construction, use ML, or touch Conditional-Alpha paths.

Candidates tested: 11
Status counts: `{"REJECT_RESEARCH": 7, "WATCHLIST_RESEARCH": 4}`

Final recommendation: carry forward only the research watchlist/further-validation candidates for deeper diagnostics; reject the rest as useful negative evidence.

## Scope And Isolation

- Run ID: `robustness_first_discovery_expansion_v2`
- Artifact directory: `artifacts/research/robustness_first_discovery_expansion_v2`
- Track A volume governance remained separate.
- `volume_shock_reversal_stable_20` was used only as an orthogonality baseline, not promoted or modified.

## Candidate Set

| signal_name                             | family                  | intuition                                                                                        | expected_horizon   | expected_failure_mode                                      | run_id                                  | research_status       |
|:----------------------------------------|:------------------------|:-------------------------------------------------------------------------------------------------|:-------------------|:-----------------------------------------------------------|:----------------------------------------|:----------------------|
| dollar_volume_pressure_reversal_20      | liquidity_flow          | Medium-horizon reversal after price moves accompanied by abnormal dollar-volume pressure.        | h10-h20            | May collapse into plain reversal or volume-shock reversal. | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| overnight_gap_flow_reversal_10          | liquidity_flow          | Reversal after large overnight gaps with abnormal volume confirmation.                           | h5-h10             | Gap noise and high turnover.                               | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| beta_residual_reversal_stability_20     | residual_relative_value | Reversal of benchmark-beta residual return, smoothed to reduce noisy beta leakage.               | h10-h20            | Hidden plain reversal or beta estimation noise.            | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| relative_value_mispricing_decay_20_60   | residual_relative_value | Mean reversion in short-term relative overextension versus longer relative trend.                | h10-h20            | Generic momentum/reversal duplication.                     | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| vol_compression_range_expansion_20_60   | volatility_structure    | Continuation after returns improve from compressed range and volatility structure.               | h10-h20            | Low signal strength from over-smoothing.                   | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| vol_expansion_reversal_quality_10_40    | volatility_structure    | Reversal after short volatility expansion and recent return stress.                              | h10-h20            | Similarity to simple volatility reversal.                  | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| dispersion_extreme_reversal_20          | dispersion_aware        | Reversal among names far from the cross-sectional return center during high dispersion.          | h10-h20            | Becomes plain cross-sectional reversal.                    | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| dispersion_stable_leadership_60         | dispersion_aware        | Continuation for stable leaders when cross-sectional dispersion is persistent rather than spiky. | h20                | Hidden momentum/trend exposure.                            | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| flow_volatility_interaction_reversal_20 | interaction             | Reversal when abnormal flow and volatility surprise jointly indicate overreaction.               | h10-h20            | Blend camouflage or duplicated reversal exposure.          | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| turnover_adjusted_relative_momentum_60  | turnover_aware          | Relative momentum quality penalized by unstable volume turnover.                                 | h20                | Momentum duplication or stale low-turnover bias.           | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |
| turnover_decay_reversal_quality_20      | turnover_aware          | Reversal where price dislocation persists while turnover pressure decays.                        | h10-h20            | Low coverage or redundant reversal behavior.               | robustness_first_discovery_expansion_v2 | TRACK_B_RESEARCH_ONLY |

## Structural Quality Summary

| signal_name                             |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |
|:----------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|
| dollar_volume_pressure_reversal_20      |     0.0224252 |     0.977575 |        0.989514 |        0.0735752 |      0.106688  |
| overnight_gap_flow_reversal_10          |     0.0167145 |     0.983286 |        0.995234 |        0.354331  |      0.537972  |
| beta_residual_reversal_stability_20     |     0.0331108 |     0.966889 |        0.978551 |        0.0497444 |      0.0683309 |
| relative_value_mispricing_decay_20_60   |     0.0412158 |     0.958784 |        0.970448 |        0.0704519 |      0.0983705 |
| vol_compression_range_expansion_20_60   |     0.0316829 |     0.968317 |        0.979981 |        0.0570544 |      0.0759746 |
| vol_expansion_reversal_quality_10_40    |     0.0245332 |     0.975467 |        0.987131 |        0.0984535 |      0.141918  |
| dispersion_extreme_reversal_20          |     0.02215   |     0.97785  |        0.989514 |        0.0669091 |      0.097047  |
| dispersion_stable_leadership_60         |     0.0426437 |     0.957356 |        0.969018 |        0.0282573 |      0.044968  |
| flow_volatility_interaction_reversal_20 |     0.0262424 |     0.973758 |        0.985701 |        0.0530928 |      0.0792002 |
| turnover_adjusted_relative_momentum_60  |     0.0429638 |     0.957036 |        0.969018 |        0.0381659 |      0.048479  |
| turnover_decay_reversal_quality_20      |     0.0224731 |     0.977527 |        0.989514 |        0.147457  |      0.253222  |

## IC / Horizon Behavior

| signal_name                             |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:----------------------------------------|----------:|------------:|--------------:|-----------:|-------------------:|----------:|
| dispersion_extreme_reversal_20          |        20 |  0.0145784  |    0.0145784  |  0.0823706 |           0.5107   |      2056 |
| flow_volatility_interaction_reversal_20 |        20 |  0.0142774  |    0.0142774  |  0.083404  |           0.508301 |      2048 |
| dollar_volume_pressure_reversal_20      |        20 |  0.0142718  |    0.0142718  |  0.0826765 |           0.51216  |      2056 |
| turnover_adjusted_relative_momentum_60  |        20 | -0.013746   |    0.013746   | -0.0704671 |           0.510681 |      2013 |
| vol_compression_range_expansion_20_60   |        20 | -0.0131752  |    0.0131752  | -0.0808943 |           0.494106 |      2036 |
| turnover_decay_reversal_quality_20      |        20 |  0.0127871  |    0.0127871  |  0.0841268 |           0.514591 |      2056 |
| dispersion_stable_leadership_60         |        20 | -0.0127775  |    0.0127775  | -0.0646071 |           0.508197 |      2013 |
| vol_expansion_reversal_quality_10_40    |        20 |  0.0122695  |    0.0122695  |  0.0708923 |           0.518284 |      2051 |
| relative_value_mispricing_decay_20_60   |        20 |  0.011374   |    0.011374   |  0.0685914 |           0.537698 |      2016 |
| beta_residual_reversal_stability_20     |        20 |  0.0078002  |    0.0078002  |  0.0487047 |           0.513035 |      2033 |
| overnight_gap_flow_reversal_10          |         1 |  0.00710881 |    0.00710881 |  0.038607  |           0.502635 |      2087 |

## WFV-Style Diagnostics

| signal_name                             |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:----------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| overnight_gap_flow_reversal_10          |         1 |           4 |               0.00710846 |               1.01615  |          0.75 |               0.75 |               0.497632 |
| dollar_volume_pressure_reversal_20      |        20 |           4 |               0.0142718  |               0.705694 |          0.75 |               0.75 |               0.341169 |
| beta_residual_reversal_stability_20     |        20 |           4 |               0.00780344 |               0.340145 |          0.75 |               0.75 |               0.423435 |
| relative_value_mispricing_decay_20_60   |        20 |           4 |               0.011374   |               0.472459 |          0.75 |               0.75 |               0.372597 |
| vol_compression_range_expansion_20_60   |        20 |           4 |              -0.0131752  |              -1.74421  |          0    |               1    |               0.414835 |
| vol_expansion_reversal_quality_10_40    |        20 |           4 |               0.0122602  |               0.833719 |          0.75 |               0.75 |               0.54265  |
| dispersion_extreme_reversal_20          |        20 |           4 |               0.0145784  |               0.687589 |          0.75 |               0.75 |               0.344031 |
| dispersion_stable_leadership_60         |        20 |           4 |              -0.012778   |              -0.728552 |          0.25 |               0.75 |               0.617533 |
| flow_volatility_interaction_reversal_20 |        20 |           4 |               0.0142774  |               0.697042 |          0.75 |               0.75 |               0.280549 |
| turnover_adjusted_relative_momentum_60  |        20 |           4 |              -0.0137462  |              -0.748276 |          0.25 |               0.75 |               0.623993 |
| turnover_decay_reversal_quality_20      |        20 |           4 |               0.0127871  |               0.879414 |          0.75 |               0.75 |               0.294772 |

## Stress / Regime Observations

Best-state slices by absolute mean IC:

| signal_name                             |   horizon | state                    |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|:----------------------------------------|----------:|:-------------------------|----------:|-----------:|----------:|-------------------:|
| turnover_adjusted_relative_momentum_60  |        20 | panic_liquidity_stress   |       187 | -0.0618673 | -0.234627 |           0.475936 |
| dispersion_stable_leadership_60         |        20 | panic_liquidity_stress   |       187 | -0.0582245 | -0.217359 |           0.497326 |
| dispersion_extreme_reversal_20          |        20 | panic_liquidity_stress   |       187 |  0.0557637 |  0.227426 |           0.55615  |
| dollar_volume_pressure_reversal_20      |        20 | panic_liquidity_stress   |       187 |  0.0520625 |  0.219591 |           0.540107 |
| vol_compression_range_expansion_20_60   |        20 | drawdown_acceleration    |       355 | -0.0477294 | -0.268255 |           0.44507  |
| turnover_adjusted_relative_momentum_60  |        20 | volatility_spike         |       393 | -0.0474422 | -0.193046 |           0.475827 |
| flow_volatility_interaction_reversal_20 |        20 | panic_liquidity_stress   |       187 |  0.0467    |  0.207688 |           0.550802 |
| dispersion_stable_leadership_60         |        20 | volatility_spike         |       393 | -0.0460176 | -0.184406 |           0.483461 |
| vol_compression_range_expansion_20_60   |        20 | panic_liquidity_stress   |       187 | -0.0454863 | -0.211529 |           0.470588 |
| turnover_adjusted_relative_momentum_60  |        20 | weak_breadth             |       508 | -0.0411993 | -0.193526 |           0.462598 |
| dispersion_stable_leadership_60         |        20 | weak_breadth             |       508 | -0.0402203 | -0.186496 |           0.468504 |
| turnover_decay_reversal_quality_20      |        20 | panic_liquidity_stress   |       187 |  0.0370108 |  0.18015  |           0.55615  |
| turnover_adjusted_relative_momentum_60  |        20 | drawdown_acceleration    |       349 | -0.0367265 | -0.163786 |           0.489971 |
| turnover_adjusted_relative_momentum_60  |        20 | high_dispersion_rotation |       570 | -0.034985  | -0.163757 |           0.449123 |
| dispersion_stable_leadership_60         |        20 | drawdown_acceleration    |       349 | -0.0342409 | -0.15041  |           0.504298 |
| dispersion_stable_leadership_60         |        20 | high_dispersion_rotation |       570 | -0.0339513 | -0.156568 |           0.449123 |
| vol_compression_range_expansion_20_60   |        20 | weak_breadth             |       508 | -0.0339305 | -0.196733 |           0.44685  |
| vol_expansion_reversal_quality_10_40    |        20 | panic_liquidity_stress   |       187 |  0.0331893 |  0.148788 |           0.524064 |
| turnover_adjusted_relative_momentum_60  |        20 | trend_transition         |       555 | -0.0317084 | -0.159479 |           0.446847 |
| turnover_adjusted_relative_momentum_60  |        20 | recovery_phase           |       196 | -0.0311775 | -0.149207 |           0.438776 |

## Orthogonality Summary

| signal_name                             |   max_abs_corr |
|:----------------------------------------|---------------:|
| dispersion_extreme_reversal_20          |      0.999593  |
| dollar_volume_pressure_reversal_20      |      0.995616  |
| vol_expansion_reversal_quality_10_40    |      0.970144  |
| dispersion_stable_leadership_60         |      0.934959  |
| flow_volatility_interaction_reversal_20 |      0.933822  |
| turnover_adjusted_relative_momentum_60  |      0.926127  |
| beta_residual_reversal_stability_20     |      0.895481  |
| turnover_decay_reversal_quality_20      |      0.799396  |
| relative_value_mispricing_decay_20_60   |      0.755963  |
| overnight_gap_flow_reversal_10          |      0.140696  |
| vol_compression_range_expansion_20_60   |      0.0544107 |

Important: high baseline correlation is treated as a review or rejection reason even when IC is positive.

## Candidate Decisions

| signal_name                             | family                  |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency | status             | review_issues                                                         |
|:----------------------------------------|:------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|:-------------------|:----------------------------------------------------------------------|
| dispersion_extreme_reversal_20          | dispersion_aware        |             20 |  0.0145784  |    0.0145784  |  0.0823706 |           0.5107   |        0.0669091 |     0.02215   |               0.999593  |              0.75 |                   0.75 | REJECT_RESEARCH    | high_baseline_similarity                                              |
| flow_volatility_interaction_reversal_20 | interaction             |             20 |  0.0142774  |    0.0142774  |  0.083404  |           0.508301 |        0.0530928 |     0.0262424 |               0.933822  |              0.75 |                   0.75 | REJECT_RESEARCH    | weak_positive_ic_rate; high_baseline_similarity                       |
| dollar_volume_pressure_reversal_20      | liquidity_flow          |             20 |  0.0142718  |    0.0142718  |  0.0826765 |           0.51216  |        0.0735752 |     0.0224252 |               0.995616  |              0.75 |                   0.75 | REJECT_RESEARCH    | high_baseline_similarity                                              |
| turnover_adjusted_relative_momentum_60  | turnover_aware          |             20 | -0.013746   |    0.013746   | -0.0704671 |           0.510681 |        0.0381659 |     0.0429638 |               0.926127  |              0.25 |                   0.75 | REJECT_RESEARCH    | weak_wfv_persistence; high_baseline_similarity                        |
| dispersion_stable_leadership_60         | dispersion_aware        |             20 | -0.0127775  |    0.0127775  | -0.0646071 |           0.508197 |        0.0282573 |     0.0426437 |               0.934959  |              0.25 |                   0.75 | REJECT_RESEARCH    | weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity |
| vol_expansion_reversal_quality_10_40    | volatility_structure    |             20 |  0.0122695  |    0.0122695  |  0.0708923 |           0.518284 |        0.0984535 |     0.0245332 |               0.970144  |              0.75 |                   0.75 | REJECT_RESEARCH    | high_baseline_similarity                                              |
| beta_residual_reversal_stability_20     | residual_relative_value |             20 |  0.0078002  |    0.0078002  |  0.0487047 |           0.513035 |        0.0497444 |     0.0331108 |               0.895481  |              0.75 |                   0.75 | REJECT_RESEARCH    | high_baseline_similarity                                              |
| vol_compression_range_expansion_20_60   | volatility_structure    |             20 | -0.0131752  |    0.0131752  | -0.0808943 |           0.494106 |        0.0570544 |     0.0316829 |               0.0544107 |              0    |                   1    | WATCHLIST_RESEARCH | weak_positive_ic_rate; weak_wfv_persistence                           |
| turnover_decay_reversal_quality_20      | turnover_aware          |             20 |  0.0127871  |    0.0127871  |  0.0841268 |           0.514591 |        0.147457  |     0.0224731 |               0.799396  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_baseline_similarity                                              |
| relative_value_mispricing_decay_20_60   | residual_relative_value |             20 |  0.011374   |    0.011374   |  0.0685914 |           0.537698 |        0.0704519 |     0.0412158 |               0.755963  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_baseline_similarity                                              |
| overnight_gap_flow_reversal_10          | liquidity_flow          |              1 |  0.00710881 |    0.00710881 |  0.038607  |           0.502635 |        0.354331  |     0.0167145 |               0.140696  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_turnover; weak_positive_ic_rate                                  |

## Watchlist / Further Validation Candidates

| signal_name                           | family                  |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency | status             | review_issues                               |
|:--------------------------------------|:------------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|:-------------------|:--------------------------------------------|
| vol_compression_range_expansion_20_60 | volatility_structure    |             20 | -0.0131752  |    0.0131752  | -0.0808943 |           0.494106 |        0.0570544 |     0.0316829 |               0.0544107 |              0    |                   1    | WATCHLIST_RESEARCH | weak_positive_ic_rate; weak_wfv_persistence |
| turnover_decay_reversal_quality_20    | turnover_aware          |             20 |  0.0127871  |    0.0127871  |  0.0841268 |           0.514591 |        0.147457  |     0.0224731 |               0.799396  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_baseline_similarity                    |
| relative_value_mispricing_decay_20_60 | residual_relative_value |             20 |  0.011374   |    0.011374   |  0.0685914 |           0.537698 |        0.0704519 |     0.0412158 |               0.755963  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_baseline_similarity                    |
| overnight_gap_flow_reversal_10        | liquidity_flow          |              1 |  0.00710881 |    0.00710881 |  0.038607  |           0.502635 |        0.354331  |     0.0167145 |               0.140696  |              0.75 |                   0.75 | WATCHLIST_RESEARCH | high_turnover; weak_positive_ic_rate        |

## Rejected Candidates

| signal_name                             | family                  |   best_horizon |    mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency | status          | review_issues                                                         |
|:----------------------------------------|:------------------------|---------------:|-----------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|:----------------|:----------------------------------------------------------------------|
| dispersion_extreme_reversal_20          | dispersion_aware        |             20 |  0.0145784 |     0.0145784 |  0.0823706 |           0.5107   |        0.0669091 |     0.02215   |                0.999593 |              0.75 |                   0.75 | REJECT_RESEARCH | high_baseline_similarity                                              |
| flow_volatility_interaction_reversal_20 | interaction             |             20 |  0.0142774 |     0.0142774 |  0.083404  |           0.508301 |        0.0530928 |     0.0262424 |                0.933822 |              0.75 |                   0.75 | REJECT_RESEARCH | weak_positive_ic_rate; high_baseline_similarity                       |
| dollar_volume_pressure_reversal_20      | liquidity_flow          |             20 |  0.0142718 |     0.0142718 |  0.0826765 |           0.51216  |        0.0735752 |     0.0224252 |                0.995616 |              0.75 |                   0.75 | REJECT_RESEARCH | high_baseline_similarity                                              |
| turnover_adjusted_relative_momentum_60  | turnover_aware          |             20 | -0.013746  |     0.013746  | -0.0704671 |           0.510681 |        0.0381659 |     0.0429638 |                0.926127 |              0.25 |                   0.75 | REJECT_RESEARCH | weak_wfv_persistence; high_baseline_similarity                        |
| dispersion_stable_leadership_60         | dispersion_aware        |             20 | -0.0127775 |     0.0127775 | -0.0646071 |           0.508197 |        0.0282573 |     0.0426437 |                0.934959 |              0.25 |                   0.75 | REJECT_RESEARCH | weak_positive_ic_rate; weak_wfv_persistence; high_baseline_similarity |
| vol_expansion_reversal_quality_10_40    | volatility_structure    |             20 |  0.0122695 |     0.0122695 |  0.0708923 |           0.518284 |        0.0984535 |     0.0245332 |                0.970144 |              0.75 |                   0.75 | REJECT_RESEARCH | high_baseline_similarity                                              |
| beta_residual_reversal_stability_20     | residual_relative_value |             20 |  0.0078002 |     0.0078002 |  0.0487047 |           0.513035 |        0.0497444 |     0.0331108 |                0.895481 |              0.75 |                   0.75 | REJECT_RESEARCH | high_baseline_similarity                                              |

## Lessons Learned

- Track B can move faster without loosening rejection discipline.
- Orthogonality checks should remain early in discovery, especially versus plain reversal, momentum, and Track A volume reversal.
- Several candidates can show plausible IC while still failing persistence, sign consistency, or redundancy checks.
- State-specific strength remains diagnostic only; it does not turn a standalone candidate into a conditional-alpha path.

## Recommended Next Batch

Run a targeted refinement only around candidates that reached `WATCHLIST_RESEARCH` or `CANDIDATE_FOR_FURTHER_VALIDATION`. Focus on reducing baseline redundancy and improving WFV persistence before any onboarding-style draft definition work.
