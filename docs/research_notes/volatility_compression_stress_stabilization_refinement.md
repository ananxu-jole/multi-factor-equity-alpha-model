# Volatility Compression Stress Stabilization Refinement

## Executive Takeaway

This research-only refinement tested `volatility_compression_after_stress_stabilization` under isolated run `volatility_compression_stress_stabilization_refinement_v1`.

Variants tested: 15
Status counts: `{"CANDIDATE_FOR_CONDITIONAL_VALIDATION": 3, "CONDITIONAL_ONLY_RESEARCH": 7, "CONDITIONAL_REFINEMENT_CANDIDATE": 4, "REJECT_RESEARCH": 1}`
Final classification: `CANDIDATE_FOR_CONDITIONAL_VALIDATION`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.

The v6 failure was not primarily a reversal-similarity problem. The base signal was orthogonal to inventory/reversal/momentum baselines, but WFV stability was weak because the edge was negative in multiple validation windows, especially the most recent window. Stress attribution showed strong behavior in panic/drawdown/volatility stress and weak behavior in trend-transition, recovery, and high-dispersion-rotation states.

## Source Inputs

- Source note: `docs/research_notes/track_b_v6_focused_discovery.md`
- Source artifact directory: `artifacts/research/track_b_v6_focused_discovery`
- Source signal: `volatility_compression_after_stress_stabilization`

## Controlled Variant Set

| variant_name                      | refinement_type      | description                                                                      | source_signal                                     | run_id                                                    | research_status                     |
|:----------------------------------|:---------------------|:---------------------------------------------------------------------------------|:--------------------------------------------------|:----------------------------------------------------------|:------------------------------------|
| base_v6_reference                 | reference            | Original v6 formulation for continuity.                                          | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| smooth_3                          | mild_smoothing       | Three-day smoothing to reduce volatility/rank noise.                             | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| smooth_5                          | mild_smoothing       | Five-day smoothing to reduce volatility/rank noise.                              | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| rebalance_5                       | rebalance_interval   | Five-day rebalance hold to reduce rank churn.                                    | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| rebalance_10                      | rebalance_interval   | Ten-day rebalance hold to reduce rank churn.                                     | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| rank_persist_5                    | low_churn_filter     | Five-day rank persistence filter using same-direction confirmation.              | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| rank_persist_10                   | low_churn_filter     | Ten-day rank persistence filter using same-direction confirmation.               | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| threshold_abs_40_zero             | activation_threshold | Keep stronger absolute signals only; inactive entries become neutral.            | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| threshold_abs_55_zero             | activation_threshold | Stricter absolute signal threshold; inactive entries become neutral.             | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| stress_strict_panic_drawdown_zero | stress_strictness    | Activate only during panic/liquidity stress or drawdown acceleration.            | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| stress_strict_vol_spike_zero      | stress_strictness    | Activate only during benchmark volatility spikes.                                | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| stress_or_weak_breadth_zero       | stress_strictness    | Activate during volatility spike, panic/drawdown stress, or weak breadth.        | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| exclude_transition_recovery_zero  | bad_state_exclusion  | Deactivate during trend-transition and recovery states that hurt v6 attribution. | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| strict_stress_rebalance_10        | combined_low_churn   | Stress/weak-breadth activation plus ten-day rebalance hold.                      | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |
| exclude_bad_rebalance_10          | combined_low_churn   | Exclude bad states and apply a ten-day rebalance hold.                           | volatility_compression_after_stress_stabilization | volatility_compression_stress_stabilization_refinement_v1 | TRACK_B_V6_REFINEMENT_RESEARCH_ONLY |

## Structural Quality And Active Coverage

| signal_name                       |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:----------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| exclude_bad_rebalance_10          |    0.0238322  |     0.976168 |        0.976168 |       0.00781459 |     0          |           0.395615  |                       46 |               1        |
| strict_stress_rebalance_10        |    0          |     1        |        1        |       0.00857979 |     0          |           0.21449   |                       42 |               1        |
| rebalance_10                      |    0.0354193  |     0.964581 |        0.976168 |       0.0123517  |     0          |           0.180172  |                       27 |               0.987879 |
| stress_strict_panic_drawdown_zero |    0.0116778  |     0.988322 |        0.990467 |       0.0143125  |     4.0146e-05 |           0.0209724 |                       54 |               0.991727 |
| rebalance_5                       |    0.0330759  |     0.966924 |        0.978551 |       0.0220924  |     0.245686   |           0.189704  |                       53 |               0.989487 |
| smooth_5                          |    0.0326362  |     0.967364 |        0.979028 |       0.0313475  |     0.131308   |           0.2755    |                       43 |               0.990412 |
| smooth_3                          |    0.0321605  |     0.967839 |        0.979504 |       0.0361019  |     0.188756   |           0.248808  |                       63 |               0.990482 |
| stress_strict_vol_spike_zero      |    0.00201327 |     0.997987 |        1        |       0.0378171  |     0.499998   |           0.0905624 |                      112 |               0.990696 |
| stress_or_weak_breadth_zero       |    0.0131676  |     0.986832 |        0.990467 |       0.0402034  |     0.499998   |           0.0958055 |                      118 |               0.990799 |
| exclude_transition_recovery_zero  |    0.0278408  |     0.972159 |        0.979981 |       0.0417483  |     0.5        |           0.0929457 |                      140 |               0.991052 |
| threshold_abs_55_zero             |    0          |     1        |        1        |       0.0444034  |     0.353009   |           0.599619  |                      116 |               1        |
| rank_persist_10                   |    0          |     1        |        1        |       0.0467812  |     0.28496    |           0.679218  |                       15 |               1        |
| rank_persist_5                    |    0          |     1        |        1        |       0.0491818  |     0.284956   |           0.658723  |                       25 |               1        |
| threshold_abs_40_zero             |    0          |     1        |        1        |       0.051422   |     0.423907   |           0.599619  |                      116 |               1        |
| base_v6_reference                 |    0.0316849  |     0.968315 |        0.979981 |       0.0591406  |     0.5        |           0.187321  |                      162 |               0.98995  |

## Multi-Horizon IC

| signal_name                       |   horizon |      mean_ic |   abs_mean_ic |        ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:----------------------------------|----------:|-------------:|--------------:|-------------:|-------------------:|----------:|:------------------|
| base_v6_reference                 |         1 | -0.00030666  |   0.00030666  | -0.00203101  |           0.478372 |       393 | False             |
| smooth_3                          |         1 |  0.00207275  |   0.00207275  |  0.0137287   |           0.506591 |       531 | False             |
| smooth_5                          |         1 |  0.00273957  |   0.00273957  |  0.0184928   |           0.514901 |       604 | False             |
| rebalance_5                       |         1 |  0.00568142  |   0.00568142  |  0.0383347   |           0.496222 |       397 | False             |
| rebalance_10                      |         1 |  0.00400462  |   0.00400462  |  0.0269476   |           0.490716 |       377 | False             |
| rank_persist_5                    |         1 |  0.00224496  |   0.00224496  |  0.0188813   |           0.517685 |       933 | False             |
| rank_persist_10                   |         1 |  0.00365268  |   0.00365268  |  0.0303139   |           0.528246 |      1009 | False             |
| threshold_abs_40_zero             |         1 |  0.00154261  |   0.00154261  |  0.0135237   |           0.509881 |       759 | False             |
| threshold_abs_55_zero             |         1 |  0.00192802  |   0.00192802  |  0.0177694   |           0.512516 |       759 | False             |
| stress_strict_panic_drawdown_zero |         1 | -0.017126    |   0.017126    | -0.0907005   |           0.409091 |        44 | False             |
| stress_strict_vol_spike_zero      |         1 |  0.000857823 |   0.000857823 |  0.00505736  |           0.494737 |       190 | False             |
| stress_or_weak_breadth_zero       |         1 |  0.000333732 |   0.000333732 |  0.00200253  |           0.497512 |       201 | False             |
| exclude_transition_recovery_zero  |         1 |  0.00536309  |   0.00536309  |  0.0394076   |           0.523077 |       195 | False             |
| strict_stress_rebalance_10        |         1 |  0.00271454  |   0.00271454  |  0.020585    |           0.520124 |       323 | False             |
| exclude_bad_rebalance_10          |         1 |  0.0083334   |   0.0083334   |  0.0799151   |           0.556582 |       433 | False             |
| base_v6_reference                 |         5 | -0.00079617  |   0.00079617  | -0.00503269  |           0.502564 |       390 | False             |
| smooth_3                          |         5 |  0.00962834  |   0.00962834  |  0.0617965   |           0.523719 |       527 | False             |
| smooth_5                          |         5 |  0.0133937   |   0.0133937   |  0.087202    |           0.536667 |       600 | False             |
| rebalance_5                       |         5 |  0.01602     |   0.01602     |  0.107167    |           0.559796 |       393 | False             |
| rebalance_10                      |         5 |  0.0214477   |   0.0214477   |  0.13443     |           0.576408 |       373 | False             |
| rank_persist_5                    |         5 |  0.00382444  |   0.00382444  |  0.0305256   |           0.502691 |       929 | False             |
| rank_persist_10                   |         5 |  0.00448774  |   0.00448774  |  0.0353539   |           0.513433 |      1005 | False             |
| threshold_abs_40_zero             |         5 | -0.00266928  |   0.00266928  | -0.0225721   |           0.48545  |       756 | True              |
| threshold_abs_55_zero             |         5 | -0.00225184  |   0.00225184  | -0.0199221   |           0.488095 |       756 | True              |
| stress_strict_panic_drawdown_zero |         5 |  0.00202479  |   0.00202479  |  0.00878997  |           0.431818 |        44 | False             |
| stress_strict_vol_spike_zero      |         5 |  0.00678725  |   0.00678725  |  0.0401836   |           0.505263 |       190 | False             |
| stress_or_weak_breadth_zero       |         5 |  0.00703878  |   0.00703878  |  0.0424932   |           0.512438 |       201 | False             |
| exclude_transition_recovery_zero  |         5 |  0.0186293   |   0.0186293   |  0.129146    |           0.558974 |       195 | False             |
| strict_stress_rebalance_10        |         5 |  0.0162642   |   0.0162642   |  0.115573    |           0.578947 |       323 | False             |
| exclude_bad_rebalance_10          |         5 |  0.0139122   |   0.0139122   |  0.130091    |           0.551963 |       433 | False             |
| base_v6_reference                 |        10 |  0.00762096  |   0.00762096  |  0.0480148   |           0.507772 |       386 | False             |
| smooth_3                          |        10 |  0.0143742   |   0.0143742   |  0.0916144   |           0.507663 |       522 | False             |
| smooth_5                          |        10 |  0.0167728   |   0.0167728   |  0.109316    |           0.529412 |       595 | False             |
| rebalance_5                       |        10 |  0.0230429   |   0.0230429   |  0.150949    |           0.564103 |       390 | False             |
| rebalance_10                      |        10 |  0.0277282   |   0.0277282   |  0.170388    |           0.567935 |       368 | True              |
| rank_persist_5                    |        10 |  0.00572673  |   0.00572673  |  0.0461469   |           0.502165 |       924 | False             |
| rank_persist_10                   |        10 |  0.00547946  |   0.00547946  |  0.044306    |           0.495    |      1000 | False             |
| threshold_abs_40_zero             |        10 |  3.16324e-05 |   3.16324e-05 |  0.000268181 |           0.477394 |       752 | False             |
| threshold_abs_55_zero             |        10 | -0.000109206 |   0.000109206 | -0.000967192 |           0.476064 |       752 | False             |
| stress_strict_panic_drawdown_zero |        10 |  0.0272465   |   0.0272465   |  0.132869    |           0.477273 |        44 | False             |
| stress_strict_vol_spike_zero      |        10 |  0.0217861   |   0.0217861   |  0.135613    |           0.529101 |       189 | False             |
| stress_or_weak_breadth_zero       |        10 |  0.023457    |   0.023457    |  0.148279    |           0.535    |       200 | False             |
| exclude_transition_recovery_zero  |        10 |  0.0405533   |   0.0405533   |  0.312356    |           0.610256 |       195 | False             |
| strict_stress_rebalance_10        |        10 |  0.0285549   |   0.0285549   |  0.200842    |           0.579439 |       321 | True              |
| exclude_bad_rebalance_10          |        10 |  0.0143352   |   0.0143352   |  0.140789    |           0.52194  |       433 | True              |
| base_v6_reference                 |        20 |  0.0110712   |   0.0110712   |  0.0702201   |           0.53562  |       379 | True              |
| smooth_3                          |        20 |  0.0192425   |   0.0192425   |  0.125225    |           0.556641 |       512 | True              |
| smooth_5                          |        20 |  0.0202484   |   0.0202484   |  0.135921    |           0.565812 |       585 | True              |
| rebalance_5                       |        20 |  0.0283914   |   0.0283914   |  0.183032    |           0.574413 |       383 | True              |
| rebalance_10                      |        20 |  0.0276599   |   0.0276599   |  0.191231    |           0.55     |       360 | False             |
| rank_persist_5                    |        20 |  0.00791489  |   0.00791489  |  0.065105    |           0.530635 |       914 | True              |
| rank_persist_10                   |        20 |  0.00709355  |   0.00709355  |  0.0589411   |           0.527273 |       990 | True              |
| threshold_abs_40_zero             |        20 |  0.00156142  |   0.00156142  |  0.0133557   |           0.499329 |       745 | False             |
| threshold_abs_55_zero             |        20 |  0.00138408  |   0.00138408  |  0.0124414   |           0.495302 |       745 | False             |
| stress_strict_panic_drawdown_zero |        20 |  0.0994455   |   0.0994455   |  0.45818     |           0.659091 |        44 | True              |
| stress_strict_vol_spike_zero      |        20 |  0.0321338   |   0.0321338   |  0.178555    |           0.598901 |       182 | True              |
| stress_or_weak_breadth_zero       |        20 |  0.0332634   |   0.0332634   |  0.188589    |           0.601036 |       193 | True              |
| exclude_transition_recovery_zero  |        20 |  0.0485528   |   0.0485528   |  0.355909    |           0.605128 |       195 | True              |
| strict_stress_rebalance_10        |        20 |  0.0228627   |   0.0228627   |  0.164353    |           0.536741 |       313 | False             |
| exclude_bad_rebalance_10          |        20 |  0.0119829   |   0.0119829   |  0.123772    |           0.498845 |       433 | False             |

## h20 Behavior

| signal_name                       |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates |
|:----------------------------------|-----------:|--------------:|----------:|-------------------:|----------:|
| stress_strict_panic_drawdown_zero | 0.0994455  |    0.0994455  | 0.45818   |           0.659091 |        44 |
| exclude_transition_recovery_zero  | 0.0485528  |    0.0485528  | 0.355909  |           0.605128 |       195 |
| stress_or_weak_breadth_zero       | 0.0332634  |    0.0332634  | 0.188589  |           0.601036 |       193 |
| stress_strict_vol_spike_zero      | 0.0321338  |    0.0321338  | 0.178555  |           0.598901 |       182 |
| rebalance_5                       | 0.0283914  |    0.0283914  | 0.183032  |           0.574413 |       383 |
| rebalance_10                      | 0.0276599  |    0.0276599  | 0.191231  |           0.55     |       360 |
| strict_stress_rebalance_10        | 0.0228627  |    0.0228627  | 0.164353  |           0.536741 |       313 |
| smooth_5                          | 0.0202484  |    0.0202484  | 0.135921  |           0.565812 |       585 |
| smooth_3                          | 0.0192425  |    0.0192425  | 0.125225  |           0.556641 |       512 |
| exclude_bad_rebalance_10          | 0.0119829  |    0.0119829  | 0.123772  |           0.498845 |       433 |
| base_v6_reference                 | 0.0110712  |    0.0110712  | 0.0702201 |           0.53562  |       379 |
| rank_persist_5                    | 0.00791489 |    0.00791489 | 0.065105  |           0.530635 |       914 |

## WFV-Style Results

| signal_name                |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:---------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| strict_stress_rebalance_10 |        10 |           4 |               0.0283694  |               0.78964  |          0.75 |               0.75 |               0.675506 |
| rebalance_5                |        20 |           4 |               0.0283235  |               1.00841  |          1    |               1    |               0.652705 |
| rebalance_10               |        10 |           4 |               0.0277282  |               0.470439 |          0.5  |               0.5  |               0.490774 |
| smooth_5                   |        20 |           4 |               0.0202317  |               0.833225 |          0.75 |               0.75 |               0.32738  |
| smooth_3                   |        20 |           4 |               0.0192425  |               0.755212 |          0.75 |               0.75 |               0.400154 |
| exclude_bad_rebalance_10   |        10 |           4 |               0.0142794  |               0.64605  |          0.75 |               0.75 |               0.397805 |
| base_v6_reference          |        20 |           4 |               0.0109317  |               0.303031 |          0.5  |               0.5  |               0.355608 |
| rank_persist_5             |        20 |           4 |               0.00792013 |               0.233179 |          0.5  |               0.5  |               0.338565 |
| rank_persist_10            |        20 |           4 |               0.00709924 |               0.255621 |          0.5  |               0.5  |               0.350177 |
| threshold_abs_55_zero      |         5 |           4 |              -0.00225184 |              -0.122914 |          0.5  |               0.5  |               0.325496 |
| threshold_abs_40_zero      |         5 |           4 |              -0.00266928 |              -0.134527 |          0.5  |               0.5  |               0.334493 |

## WFV Window Failure Diagnostics

| signal_name                |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:---------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| rebalance_10               |        10 |        1 | 2018-11-29   | 2020-04-24 |     0.108593   |    0.616566  |           0.673913 |               92 |
| rebalance_10               |        10 |        2 | 2020-04-27   | 2022-04-06 |    -0.0408345  |   -0.22636   |           0.434783 |               92 |
| rebalance_10               |        10 |        3 | 2022-04-07   | 2024-08-29 |     0.0574977  |    0.516282  |           0.673913 |               92 |
| rebalance_10               |        10 |        4 | 2024-08-30   | 2026-04-23 |    -0.0143434  |   -0.113149  |           0.48913  |               92 |
| strict_stress_rebalance_10 |        10 |        1 | 2018-12-14   | 2020-04-17 |     0.0878878  |    0.506788  |           0.679012 |               81 |
| strict_stress_rebalance_10 |        10 |        2 | 2020-04-20   | 2022-03-15 |    -0.00831441 |   -0.0587106 |           0.525    |               80 |
| strict_stress_rebalance_10 |        10 |        3 | 2022-03-16   | 2024-04-24 |     0.0142913  |    0.137324  |           0.5375   |               80 |
| strict_stress_rebalance_10 |        10 |        4 | 2024-04-25   | 2026-04-23 |     0.0196131  |    0.162517  |           0.575    |               80 |
| exclude_bad_rebalance_10   |        10 |        1 | 2018-11-29   | 2019-07-17 |     0.0384303  |    0.367271  |           0.605505 |              109 |
| exclude_bad_rebalance_10   |        10 |        2 | 2019-07-18   | 2021-01-19 |    -0.0197442  |   -0.241514  |           0.305556 |              108 |
| exclude_bad_rebalance_10   |        10 |        3 | 2021-01-20   | 2023-05-09 |     0.0101466  |    0.0990634 |           0.537037 |              108 |
| exclude_bad_rebalance_10   |        10 |        4 | 2023-05-10   | 2025-06-25 |     0.0282849  |    0.265127  |           0.638889 |              108 |
| base_v6_reference          |        20 |        1 | 2018-11-23   | 2020-06-03 |    -0.00263542 |   -0.0122468 |           0.578947 |               95 |
| base_v6_reference          |        20 |        2 | 2020-06-04   | 2022-06-10 |     0.0410496  |    0.356978  |           0.621053 |               95 |
| base_v6_reference          |        20 |        3 | 2022-06-21   | 2024-09-19 |     0.0472514  |    0.390632  |           0.642105 |               95 |
| base_v6_reference          |        20 |        4 | 2024-09-20   | 2026-04-07 |    -0.0419386  |   -0.296227  |           0.297872 |               94 |
| smooth_3                   |        20 |        1 | 2018-11-23   | 2020-06-15 |     0.0273991  |    0.133449  |           0.640625 |              128 |
| smooth_3                   |        20 |        2 | 2020-06-16   | 2022-07-07 |     0.0481821  |    0.378711  |           0.648438 |              128 |
| smooth_3                   |        20 |        3 | 2022-07-08   | 2024-09-26 |     0.0231083  |    0.190816  |           0.585938 |              128 |
| smooth_3                   |        20 |        4 | 2024-09-27   | 2026-04-09 |    -0.0217193  |   -0.158209  |           0.351562 |              128 |
| smooth_5                   |        20 |        1 | 2018-11-23   | 2020-06-18 |     0.0299769  |    0.14969   |           0.646259 |              147 |
| smooth_5                   |        20 |        2 | 2020-06-19   | 2022-07-06 |     0.0404181  |    0.324272  |           0.59589  |              146 |
| smooth_5                   |        20 |        3 | 2022-07-07   | 2024-09-23 |     0.0317981  |    0.26407   |           0.636986 |              146 |
| smooth_5                   |        20 |        4 | 2024-09-24   | 2026-04-09 |    -0.0212662  |   -0.167348  |           0.383562 |              146 |
| rebalance_5                |        20 |        1 | 2018-11-29   | 2020-05-21 |     0.00840823 |    0.038723  |           0.614583 |               96 |
| rebalance_5                |        20 |        2 | 2020-05-22   | 2022-06-01 |     0.0286402  |    0.24136   |           0.5625   |               96 |
| rebalance_5                |        20 |        3 | 2022-06-02   | 2024-09-17 |     0.0739475  |    0.702775  |           0.760417 |               96 |
| rebalance_5                |        20 |        4 | 2024-09-18   | 2026-04-09 |     0.00229807 |    0.0159488 |           0.357895 |               95 |

## Stress And Regime Attribution

| signal_name                       |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:----------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| exclude_transition_recovery_zero  |        20 | panic_liquidity_stress   |        28 |  0.171896    |  0.967782   |           0.785714 |
| rebalance_5                       |        20 | panic_liquidity_stress   |        48 |  0.170419    |  1.01118    |           0.791667 |
| rebalance_5                       |        20 | drawdown_acceleration    |        49 |  0.165135    |  0.966968   |           0.77551  |
| exclude_transition_recovery_zero  |        20 | drawdown_acceleration    |        29 |  0.161794    |  0.88639    |           0.758621 |
| rebalance_5                       |        20 | weak_breadth             |        79 |  0.127372    |  0.794293   |           0.708861 |
| stress_strict_panic_drawdown_zero |        20 | high_dispersion_rotation |        18 |  0.116609    |  0.584746   |           0.666667 |
| stress_strict_panic_drawdown_zero |        20 | panic_liquidity_stress   |        43 |  0.104573    |  0.482121   |           0.674419 |
| stress_strict_panic_drawdown_zero |        20 | volatility_spike         |        43 |  0.104573    |  0.482121   |           0.674419 |
| base_v6_reference                 |        20 | panic_liquidity_stress   |        43 |  0.104573    |  0.482121   |           0.674419 |
| stress_strict_vol_spike_zero      |        20 | drawdown_acceleration    |        43 |  0.104573    |  0.482121   |           0.674419 |
| stress_strict_vol_spike_zero      |        20 | panic_liquidity_stress   |        43 |  0.104573    |  0.482121   |           0.674419 |
| stress_or_weak_breadth_zero       |        20 | panic_liquidity_stress   |        43 |  0.104573    |  0.482121   |           0.674419 |
| exclude_transition_recovery_zero  |        20 | weak_breadth             |        59 |  0.101479    |  0.632788   |           0.677966 |
| smooth_3                          |        20 | panic_liquidity_stress   |        74 |  0.101045    |  0.485674   |           0.662162 |
| base_v6_reference                 |        20 | drawdown_acceleration    |        44 |  0.0994455   |  0.45818    |           0.659091 |
| stress_strict_panic_drawdown_zero |        20 | drawdown_acceleration    |        44 |  0.0994455   |  0.45818    |           0.659091 |
| stress_or_weak_breadth_zero       |        20 | drawdown_acceleration    |        44 |  0.0994455   |  0.45818    |           0.659091 |
| stress_strict_panic_drawdown_zero |        20 | weak_breadth             |        40 |  0.0953143   |  0.42691    |           0.65     |
| smooth_3                          |        20 | drawdown_acceleration    |        79 |  0.0944754   |  0.463263   |           0.658228 |
| exclude_transition_recovery_zero  |        20 | volatility_spike         |       105 |  0.0870318   |  0.581401   |           0.733333 |
| smooth_5                          |        20 | panic_liquidity_stress   |        86 |  0.083679    |  0.425007   |           0.604651 |
| stress_strict_vol_spike_zero      |        20 | weak_breadth             |        63 |  0.0769604   |  0.399675   |           0.634921 |
| rebalance_10                      |        10 | weak_breadth             |        87 |  0.0757553   |  0.497551   |           0.643678 |
| rebalance_10                      |        10 | panic_liquidity_stress   |        61 |  0.0748003   |  0.460505   |           0.606557 |
| smooth_3                          |        20 | weak_breadth             |       127 |  0.0743526   |  0.424635   |           0.637795 |
| base_v6_reference                 |        20 | weak_breadth             |        74 |  0.0732431   |  0.402745   |           0.635135 |
| stress_or_weak_breadth_zero       |        20 | weak_breadth             |        74 |  0.0732431   |  0.402745   |           0.635135 |
| smooth_5                          |        20 | drawdown_acceleration    |        97 |  0.0725282   |  0.380207   |           0.597938 |
| rebalance_10                      |        10 | drawdown_acceleration    |        63 |  0.0693651   |  0.426214   |           0.587302 |
| strict_stress_rebalance_10        |        10 | panic_liquidity_stress   |        88 |  0.0678647   |  0.496303   |           0.681818 |
| smooth_5                          |        20 | weak_breadth             |       150 |  0.0652515   |  0.391742   |           0.62     |
| exclude_transition_recovery_zero  |        20 | high_dispersion_rotation |        48 |  0.0642858   |  0.431988   |           0.625    |
| rank_persist_5                    |        20 | panic_liquidity_stress   |       120 |  0.0637096   |  0.381883   |           0.616667 |
| rebalance_5                       |        20 | volatility_spike         |       177 |  0.0633418   |  0.358786   |           0.649718 |
| exclude_bad_rebalance_10          |        10 | panic_liquidity_stress   |        69 |  0.0610393   |  0.510035   |           0.681159 |
| rank_persist_10                   |        20 | panic_liquidity_stress   |       130 |  0.0589031   |  0.365861   |           0.6      |
| rebalance_10                      |        10 | volatility_spike         |       172 |  0.0555783   |  0.351721   |           0.622093 |
| exclude_bad_rebalance_10          |        10 | drawdown_acceleration    |        84 |  0.0511086   |  0.450682   |           0.654762 |
| exclude_bad_rebalance_10          |        10 | weak_breadth             |       114 |  0.04944     |  0.474112   |           0.657895 |
| strict_stress_rebalance_10        |        10 | drawdown_acceleration    |       120 |  0.0482364   |  0.384716   |           0.641667 |
| strict_stress_rebalance_10        |        10 | weak_breadth             |       161 |  0.0477097   |  0.398466   |           0.658385 |
| strict_stress_rebalance_10        |        10 | volatility_spike         |       213 |  0.0463547   |  0.320704   |           0.619718 |
| rank_persist_5                    |        20 | drawdown_acceleration    |       165 |  0.0438016   |  0.293443   |           0.575758 |
| exclude_bad_rebalance_10          |        10 | volatility_spike         |       154 |  0.0425889   |  0.33798    |           0.616883 |
| smooth_5                          |        20 | volatility_spike         |       270 |  0.0407406   |  0.230516   |           0.611111 |
| rank_persist_5                    |        20 | weak_breadth             |       250 |  0.0396285   |  0.301543   |           0.608    |
| smooth_3                          |        20 | volatility_spike         |       250 |  0.039042    |  0.218296   |           0.6      |
| rank_persist_10                   |        20 | drawdown_acceleration    |       180 |  0.0389346   |  0.266876   |           0.577778 |
| exclude_bad_rebalance_10          |        10 | recovery_phase           |        43 |  0.036033    |  0.308348   |           0.55814  |
| rank_persist_10                   |        20 | weak_breadth             |       283 |  0.0358021   |  0.284728   |           0.597173 |
| rank_persist_10                   |        20 | volatility_spike         |       326 |  0.0334878   |  0.214642   |           0.595092 |
| stress_or_weak_breadth_zero       |        20 | volatility_spike         |       182 |  0.0321338   |  0.178555   |           0.598901 |
| stress_strict_vol_spike_zero      |        20 | volatility_spike         |       182 |  0.0321338   |  0.178555   |           0.598901 |
| base_v6_reference                 |        20 | volatility_spike         |       182 |  0.0321338   |  0.178555   |           0.598901 |
| rank_persist_5                    |        20 | volatility_spike         |       312 |  0.0314598   |  0.198337   |           0.605769 |
| strict_stress_rebalance_10        |        10 | recovery_phase           |        52 |  0.0136531   |  0.0850103  |           0.5      |
| threshold_abs_40_zero             |         5 | panic_liquidity_stress   |        90 |  0.00976661  |  0.0615168  |           0.577778 |
| threshold_abs_55_zero             |         5 | panic_liquidity_stress   |        90 |  0.00869702  |  0.0598337  |           0.577778 |
| threshold_abs_40_zero             |         5 | volatility_spike         |       250 |  0.00777299  |  0.053903   |           0.532    |
| threshold_abs_55_zero             |         5 | volatility_spike         |       250 |  0.00769795  |  0.056604   |           0.544    |
| rank_persist_10                   |        20 | recovery_phase           |       159 |  0.00671393  |  0.045281   |           0.660377 |
| smooth_5                          |        20 | high_dispersion_rotation |       220 |  0.00519095  |  0.0300385  |           0.572727 |
| rebalance_10                      |        10 | high_dispersion_rotation |       138 |  0.00474569  |  0.0267669  |           0.536232 |
| rebalance_5                       |        20 | high_dispersion_rotation |       140 |  0.00431183  |  0.0230982  |           0.564286 |
| rank_persist_5                    |        20 | recovery_phase           |       153 |  0.0029788   |  0.0202956  |           0.640523 |
| threshold_abs_40_zero             |         5 | weak_breadth             |       193 |  0.00228417  |  0.0194857  |           0.512953 |
| threshold_abs_40_zero             |         5 | drawdown_acceleration    |       129 |  0.00140639  |  0.0102876  |           0.527132 |
| threshold_abs_55_zero             |         5 | weak_breadth             |       193 |  0.000884885 |  0.00819837 |           0.507772 |
| threshold_abs_55_zero             |         5 | drawdown_acceleration    |       129 |  0.000268947 |  0.00213367 |           0.527132 |
| smooth_3                          |        20 | high_dispersion_rotation |       196 | -0.00316833  | -0.0178901  |           0.52551  |
| stress_strict_vol_spike_zero      |        20 | high_dispersion_rotation |        81 | -0.00668606  | -0.0322952  |           0.493827 |
| stress_or_weak_breadth_zero       |        20 | high_dispersion_rotation |        81 | -0.00668606  | -0.0322952  |           0.493827 |
| threshold_abs_55_zero             |         5 | recovery_phase           |       133 | -0.0077242   | -0.0552877  |           0.466165 |
| threshold_abs_40_zero             |         5 | recovery_phase           |       133 | -0.00929098  | -0.0627859  |           0.473684 |
| base_v6_reference                 |        20 | recovery_phase           |       110 | -0.0168556   | -0.103148   |           0.527273 |

## Concept-State Attribution

| signal_name                       |   horizon | state                           |   n_dates |      mean_ic |         ic_ir |   positive_ic_rate |
|:----------------------------------|----------:|:--------------------------------|----------:|-------------:|--------------:|-------------------:|
| stress_strict_panic_drawdown_zero |        20 | VOL_NORMALIZING                 |         1 |  0.264227    | nan           |           1        |
| stress_strict_panic_drawdown_zero |        20 | DISPERSION_ELEVATED_RECENT      |        38 |  0.111465    |   0.505192    |           0.684211 |
| stress_strict_panic_drawdown_zero |        20 | EVENT_GAP_DAY                   |        44 |  0.0994455   |   0.45818     |           0.659091 |
| stress_strict_panic_drawdown_zero |        20 | RECENT_VOL_STRESS               |        44 |  0.0994455   |   0.45818     |           0.659091 |
| stress_strict_panic_drawdown_zero |        20 | RANGE_NORMALIZING               |        44 |  0.0994455   |   0.45818     |           0.659091 |
| exclude_transition_recovery_zero  |        20 | DISPERSION_ELEVATED_RECENT      |       149 |  0.0648191   |   0.458081    |           0.657718 |
| exclude_transition_recovery_zero  |        20 | EVENT_GAP_DAY                   |       195 |  0.0485528   |   0.355909    |           0.605128 |
| exclude_transition_recovery_zero  |        20 | RECENT_VOL_STRESS               |       195 |  0.0485528   |   0.355909    |           0.605128 |
| exclude_transition_recovery_zero  |        20 | RANGE_NORMALIZING               |       195 |  0.0485528   |   0.355909    |           0.605128 |
| exclude_bad_rebalance_10          |        10 | DISPERSION_STABILITY_TRANSITION |       115 |  0.0392769   |   0.347969    |           0.643478 |
| exclude_bad_rebalance_10          |        10 | RECENT_VOL_STRESS               |       210 |  0.0378843   |   0.295396    |           0.614286 |
| strict_stress_rebalance_10        |        10 | DISPERSION_ELEVATED_RECENT      |       247 |  0.0363698   |   0.236386    |           0.582996 |
| exclude_transition_recovery_zero  |        20 | DISPERSION_STABILITY_TRANSITION |        76 |  0.0360783   |   0.260966    |           0.552632 |
| rebalance_10                      |        10 | DISPERSION_ELEVATED_RECENT      |       326 |  0.0342025   |   0.204395    |           0.58589  |
| exclude_bad_rebalance_10          |        10 | DISPERSION_ELEVATED_RECENT      |       275 |  0.0333097   |   0.302474    |           0.618182 |
| stress_or_weak_breadth_zero       |        20 | RECENT_VOL_STRESS               |       193 |  0.0332634   |   0.188589    |           0.601036 |
| stress_or_weak_breadth_zero       |        20 | RANGE_NORMALIZING               |       193 |  0.0332634   |   0.188589    |           0.601036 |
| stress_or_weak_breadth_zero       |        20 | EVENT_GAP_DAY                   |       193 |  0.0332634   |   0.188589    |           0.601036 |
| strict_stress_rebalance_10        |        10 | RECENT_VOL_STRESS               |       263 |  0.0324764   |   0.210058    |           0.570342 |
| rebalance_5                       |        20 | DISPERSION_ELEVATED_RECENT      |       335 |  0.0323168   |   0.202167    |           0.59403  |
| stress_strict_vol_spike_zero      |        20 | EVENT_GAP_DAY                   |       182 |  0.0321338   |   0.178555    |           0.598901 |
| stress_strict_vol_spike_zero      |        20 | RECENT_VOL_STRESS               |       182 |  0.0321338   |   0.178555    |           0.598901 |
| stress_strict_vol_spike_zero      |        20 | RANGE_NORMALIZING               |       182 |  0.0321338   |   0.178555    |           0.598901 |
| stress_or_weak_breadth_zero       |        20 | DISPERSION_ELEVATED_RECENT      |       171 |  0.0291578   |   0.159307    |           0.578947 |
| rebalance_5                       |        20 | RECENT_VOL_STRESS               |       365 |  0.0288161   |   0.18322     |           0.572603 |
| strict_stress_rebalance_10        |        10 | EVENT_GAP_DAY                   |       321 |  0.0285549   |   0.200842    |           0.579439 |
| rebalance_5                       |        20 | EVENT_GAP_DAY                   |       383 |  0.0283914   |   0.183032    |           0.574413 |
| rebalance_10                      |        10 | EVENT_GAP_DAY                   |       368 |  0.0277282   |   0.170388    |           0.567935 |
| rebalance_10                      |        10 | RECENT_VOL_STRESS               |       349 |  0.0266688   |   0.161225    |           0.561605 |
| stress_strict_vol_spike_zero      |        20 | DISPERSION_ELEVATED_RECENT      |       161 |  0.0266673   |   0.142496    |           0.571429 |
| strict_stress_rebalance_10        |        10 | RANGE_NORMALIZING               |       183 |  0.0263434   |   0.166676    |           0.557377 |
| smooth_5                          |        20 | DISPERSION_ELEVATED_RECENT      |       493 |  0.0238881   |   0.153756    |           0.584178 |
| rebalance_5                       |        20 | RANGE_NORMALIZING               |       318 |  0.0235476   |   0.148998    |           0.572327 |
| rebalance_10                      |        10 | RANGE_NORMALIZING               |       291 |  0.0221277   |   0.13575     |           0.56701  |
| smooth_3                          |        20 | DISPERSION_ELEVATED_RECENT      |       436 |  0.0220769   |   0.138037    |           0.575688 |
| smooth_5                          |        20 | RECENT_VOL_STRESS               |       526 |  0.0209977   |   0.135761    |           0.568441 |
| smooth_5                          |        20 | EVENT_GAP_DAY                   |       585 |  0.0202484   |   0.135921    |           0.565812 |
| smooth_3                          |        20 | EVENT_GAP_DAY                   |       512 |  0.0192425   |   0.125225    |           0.556641 |
| exclude_bad_rebalance_10          |        10 | DISPERSION_NORMALIZING          |       165 |  0.0191105   |   0.181699    |           0.533333 |
| smooth_3                          |        20 | RECENT_VOL_STRESS               |       486 |  0.0189628   |   0.120886    |           0.55144  |
| smooth_5                          |        20 | RANGE_NORMALIZING               |       427 |  0.0170471   |   0.110502    |           0.564403 |
| rank_persist_5                    |        20 | DISPERSION_ELEVATED_RECENT      |       679 |  0.0160327   |   0.120639    |           0.569956 |
| rank_persist_10                   |        20 | DISPERSION_ELEVATED_RECENT      |       735 |  0.0157966   |   0.12128     |           0.567347 |
| exclude_bad_rebalance_10          |        10 | RANGE_NORMALIZING               |       273 |  0.0154154   |   0.142072    |           0.501832 |
| rank_persist_5                    |        20 | RECENT_VOL_STRESS               |       574 |  0.0148967   |   0.102783    |           0.557491 |
| rank_persist_10                   |        20 | RECENT_VOL_STRESS               |       600 |  0.0138453   |   0.0959568   |           0.55     |
| base_v6_reference                 |        20 | DISPERSION_ELEVATED_RECENT      |       330 |  0.013574    |   0.0829198   |           0.551515 |
| smooth_3                          |        20 | RANGE_NORMALIZING               |       402 |  0.0131921   |   0.0851674   |           0.549751 |
| base_v6_reference                 |        20 | EVENT_GAP_DAY                   |       379 |  0.0110712   |   0.0702201   |           0.53562  |
| base_v6_reference                 |        20 | RECENT_VOL_STRESS               |       379 |  0.0110712   |   0.0702201   |           0.53562  |
| base_v6_reference                 |        20 | RANGE_NORMALIZING               |       379 |  0.0110712   |   0.0702201   |           0.53562  |
| rebalance_10                      |        10 | DISPERSION_STABILITY_TRANSITION |       161 |  0.00812642  |   0.0483838   |           0.52795  |
| rank_persist_5                    |        20 | EVENT_GAP_DAY                   |       914 |  0.00791489  |   0.065105    |           0.530635 |
| rank_persist_10                   |        20 | EVENT_GAP_DAY                   |       990 |  0.00709355  |   0.0589411   |           0.527273 |
| rank_persist_5                    |        20 | RANGE_NORMALIZING               |       582 |  0.00474885  |   0.0353103   |           0.513746 |
| rank_persist_10                   |        20 | RANGE_NORMALIZING               |       622 |  0.00431216  |   0.0325523   |           0.508039 |
| stress_or_weak_breadth_zero       |        20 | DISPERSION_NORMALIZING          |        83 |  0.00403707  |   0.0228002   |           0.542169 |
| strict_stress_rebalance_10        |        10 | DISPERSION_STABILITY_TRANSITION |        78 |  0.00322948  |   0.0202107   |           0.461538 |
| threshold_abs_55_zero             |         5 | DISPERSION_ELEVATED_RECENT      |       558 |  0.00306525  |   0.0247712   |           0.523297 |
| stress_strict_vol_spike_zero      |        20 | DISPERSION_NORMALIZING          |        79 |  0.00304503  |   0.016962    |           0.556962 |
| rebalance_5                       |        20 | DISPERSION_STABILITY_TRANSITION |       167 |  0.00276817  |   0.0171964   |           0.520958 |
| threshold_abs_40_zero             |         5 | DISPERSION_ELEVATED_RECENT      |       558 |  0.00268505  |   0.020662    |           0.523297 |
| threshold_abs_55_zero             |         5 | DISPERSION_STABILITY_TRANSITION |       218 |  0.00056841  |   0.00429542  |           0.53211  |
| rank_persist_10                   |        20 | DISPERSION_STABILITY_TRANSITION |       303 |  0.000415044 |   0.00306761  |           0.49505  |
| threshold_abs_55_zero             |         5 | RECENT_VOL_STRESS               |       458 |  0.000290793 |   0.00214097  |           0.508734 |
| rank_persist_5                    |        20 | DISPERSION_STABILITY_TRANSITION |       278 |  1.92639e-05 |   0.000137719 |           0.517986 |
| threshold_abs_40_zero             |         5 | DISPERSION_STABILITY_TRANSITION |       218 | -4.57027e-05 |  -0.000326254 |           0.53211  |
| threshold_abs_40_zero             |         5 | RECENT_VOL_STRESS               |       458 | -0.000398259 |  -0.00278527  |           0.504367 |
| smooth_5                          |        20 | DISPERSION_STABILITY_TRANSITION |       220 | -0.00153382  |  -0.00967933  |           0.513636 |
| threshold_abs_55_zero             |         5 | EVENT_GAP_DAY                   |       756 | -0.00225184  |  -0.0199221   |           0.488095 |
| threshold_abs_40_zero             |         5 | EVENT_GAP_DAY                   |       756 | -0.00266928  |  -0.0225721   |           0.48545  |
| threshold_abs_55_zero             |         5 | RANGE_NORMALIZING               |       557 | -0.00279336  |  -0.0222091   |           0.481149 |
| threshold_abs_40_zero             |         5 | RANGE_NORMALIZING               |       557 | -0.00335994  |  -0.0254289   |           0.477558 |
| smooth_3                          |        20 | DISPERSION_STABILITY_TRANSITION |       199 | -0.00544196  |  -0.033668    |           0.502513 |
| base_v6_reference                 |        20 | DISPERSION_STABILITY_TRANSITION |       146 | -0.00884976  |  -0.0517332   |           0.5      |

## Orthogonality / Redundancy

| signal_name                       | top_comparison                                            |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:----------------------------------|:----------------------------------------------------------|------------------------:|---------------------------:|-------------------------:|---------------------:|--------------------:|--------------------:|
| exclude_bad_rebalance_10          | v6_base_volatility_compression_after_stress_stabilization |                0.281263 |                0.000654974 |               0.0223586  |            0.0223586 |           0.0809861 |          0.0474735  |
| stress_strict_panic_drawdown_zero | v6_base_volatility_compression_after_stress_stabilization |                0.334903 |                0.00671693  |               0.010966   |            0.010966  |           0.0590844 |          0.0399273  |
| strict_stress_rebalance_10        | v6_base_volatility_compression_after_stress_stabilization |                0.351591 |                0.00117864  |               0.0172268  |            0.0172268 |           0.0860186 |          0.0395903  |
| rebalance_10                      | v6_base_volatility_compression_after_stress_stabilization |                0.518105 |                0.0231713   |               0.0126806  |            0.0231713 |           0.0682407 |          0.0179724  |
| rebalance_5                       | v6_base_volatility_compression_after_stress_stabilization |                0.684536 |                0.0474302   |               0.0172333  |            0.0474302 |           0.0577811 |          0.00517082 |
| stress_strict_vol_spike_zero      | v6_base_volatility_compression_after_stress_stabilization |                0.695575 |                0.0326773   |               0.00400752 |            0.0326773 |           0.0682766 |          0.0240083  |
| exclude_transition_recovery_zero  | v6_base_volatility_compression_after_stress_stabilization |                0.704795 |                0.0446491   |               0.00502783 |            0.0446491 |           0.0554938 |          0.0203661  |
| stress_or_weak_breadth_zero       | v6_base_volatility_compression_after_stress_stabilization |                0.715464 |                0.0347393   |               0.00424891 |            0.0347393 |           0.0675037 |          0.0237413  |
| smooth_5                          | v6_base_volatility_compression_after_stress_stabilization |                0.754716 |                0.045892    |               0.0140237  |            0.045892  |           0.100002  |          0.0288664  |
| rank_persist_10                   | v6_base_volatility_compression_after_stress_stabilization |                0.777245 |                0.0433395   |               0.0115932  |            0.0433395 |           0.0885661 |          0.0264023  |
| smooth_3                          | v6_base_volatility_compression_after_stress_stabilization |                0.829031 |                0.0523766   |               0.0098393  |            0.0523766 |           0.0890608 |          0.0231838  |
| rank_persist_5                    | v6_base_volatility_compression_after_stress_stabilization |                0.84473  |                0.0510086   |               0.00979475 |            0.0510086 |           0.0849876 |          0.0221343  |
| threshold_abs_55_zero             | v6_base_volatility_compression_after_stress_stabilization |                0.912091 |                0.0572029   |               0.00383028 |            0.0572029 |           0.0551057 |          0.00183681 |
| threshold_abs_40_zero             | v6_base_volatility_compression_after_stress_stabilization |                0.966661 |                0.0575354   |               0.00410601 |            0.0575354 |           0.0587239 |          0.00364509 |
| base_v6_reference                 | v6_base_volatility_compression_after_stress_stabilization |                1        |                0.0582247   |               0.00406553 |            0.0582247 |           0.0606091 |          0.0044578  |

## Variant Decisions

| signal_name                       |   best_horizon |     mean_ic |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   effective_mean_test_ic |   effective_test_ic_ir |   negative_window_count |   worst_window |   worst_window_mean_ic |   positive_regime_count |   best_regime_ic |   worst_regime_ic | status                               | review_issues                                                                                                 |
|:----------------------------------|---------------:|------------:|--------------:|------------:|-----------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------------:|-------------------------:|---------------------:|--------------------:|--------------------:|------------------:|-----------------------:|-------------------------:|-----------------------:|------------------------:|---------------:|-----------------------:|------------------------:|-----------------:|------------------:|:-------------------------------------|:--------------------------------------------------------------------------------------------------------------|
| rebalance_5                       |             20 |  0.0283914  |    0.0283914  |   0.183032  |               0.574413 |       0.0220924  |    0.0330759  |           0.189704  |                0.684536 |                0.0474302   |               0.0172333  |            0.0474302 |           0.0577811 |          0.00517082 |              1    |                   1    |               0.0283235  |               1.00841  |                       0 |              4 |             0.00229807 |                       5 |       0.170419   |       -0.0152662  | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                                                                                          |
| smooth_5                          |             20 |  0.0202484  |    0.0202484  |   0.135921  |               0.565812 |       0.0313475  |    0.0326362  |           0.2755    |                0.754716 |                0.045892    |               0.0140237  |            0.045892  |           0.100002  |          0.0288664  |              0.75 |                   0.75 |               0.0202317  |               0.833225 |                       1 |              4 |            -0.0212662  |                       5 |       0.083679   |       -0.0155405  | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                                                                                          |
| smooth_3                          |             20 |  0.0192425  |    0.0192425  |   0.125225  |               0.556641 |       0.0361019  |    0.0321605  |           0.248808  |                0.829031 |                0.0523766   |               0.0098393  |            0.0523766 |           0.0890608 |          0.0231838  |              0.75 |                   0.75 |               0.0192425  |               0.755212 |                       1 |              4 |            -0.0217193  |                       4 |       0.101045   |       -0.0225902  | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                                                                                          |
| rebalance_10                      |             10 |  0.0277282  |    0.0276599  |   0.191231  |               0.55     |       0.0123517  |    0.0354193  |           0.180172  |                0.518105 |                0.0231713   |               0.0126806  |            0.0231713 |           0.0682407 |          0.0179724  |              0.5  |                   0.5  |               0.0277282  |               0.470439 |                       2 |              2 |            -0.0408345  |                       5 |       0.0757553  |       -0.0096709  | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability                                     |
| strict_stress_rebalance_10        |             10 |  0.0285549  |    0.0228627  |   0.164353  |               0.536741 |       0.00857979 |    0          |           0.21449   |                0.351591 |                0.00117864  |               0.0172268  |            0.0172268 |           0.0860186 |          0.0395903  |              0.75 |                   0.75 |               0.0283694  |               0.78964  |                       1 |              2 |            -0.00831441 |                       7 |       0.0678647  |        0.00410558 | CONDITIONAL_REFINEMENT_CANDIDATE     | none                                                                                                          |
| exclude_bad_rebalance_10          |             10 |  0.0143352  |    0.0119829  |   0.123772  |               0.498845 |       0.00781459 |    0.0238322  |           0.395615  |                0.281263 |                0.000654974 |               0.0223586  |            0.0223586 |           0.0809861 |          0.0474735  |              0.75 |                   0.75 |               0.0142794  |               0.64605  |                       1 |              2 |            -0.0197442  |                       7 |       0.0610393  |        0.00653912 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_positive_ic_rate                                                                                         |
| base_v6_reference                 |             20 |  0.0110712  |    0.0110712  |   0.0702201 |               0.53562  |       0.0591406  |    0.0316849  |           0.187321  |                1        |                0.0582247   |               0.00406553 |            0.0582247 |           0.0606091 |          0.0044578  |              0.5  |                   0.5  |               0.0109317  |               0.303031 |                       2 |              4 |            -0.0419386  |                       4 |       0.104573   |       -0.0412692  | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability                                     |
| exclude_transition_recovery_zero  |             20 |  0.0485528  |    0.0485528  |   0.355909  |               0.605128 |       0.0417483  |    0.0278408  |           0.0929457 |                0.704795 |                0.0446491   |               0.00502783 |            0.0446491 |           0.0554938 |          0.0203661  |            nan    |                 nan    |             nan          |             nan        |                     nan |            nan |           nan          |                       5 |       0.171896   |        0.0642858  | CONDITIONAL_ONLY_RESEARCH            | sparse_activation                                                                                             |
| stress_or_weak_breadth_zero       |             20 |  0.0332634  |    0.0332634  |   0.188589  |               0.601036 |       0.0402034  |    0.0131676  |           0.0958055 |                0.715464 |                0.0347393   |               0.00424891 |            0.0347393 |           0.0675037 |          0.0237413  |            nan    |                 nan    |             nan          |             nan        |                     nan |            nan |           nan          |                       4 |       0.104573   |       -0.0634736  | CONDITIONAL_ONLY_RESEARCH            | sparse_activation                                                                                             |
| stress_strict_vol_spike_zero      |             20 |  0.0321338  |    0.0321338  |   0.178555  |               0.598901 |       0.0378171  |    0.00201327 |           0.0905624 |                0.695575 |                0.0326773   |               0.00400752 |            0.0326773 |           0.0682766 |          0.0240083  |            nan    |                 nan    |             nan          |             nan        |                     nan |            nan |           nan          |                       4 |       0.104573   |       -0.0634736  | CONDITIONAL_ONLY_RESEARCH            | sparse_activation                                                                                             |
| rank_persist_5                    |             20 |  0.00791489 |    0.00791489 |   0.065105  |               0.530635 |       0.0491818  |    0          |           0.658723  |                0.84473  |                0.0510086   |               0.00979475 |            0.0510086 |           0.0849876 |          0.0221343  |              0.5  |                   0.5  |               0.00792013 |               0.233179 |                       2 |              2 |            -0.0340447  |                       4 |       0.0637096  |       -0.0176628  | CONDITIONAL_ONLY_RESEARCH            | weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability                                     |
| rank_persist_10                   |             20 |  0.00709355 |    0.00709355 |   0.0589411 |               0.527273 |       0.0467812  |    0          |           0.679218  |                0.777245 |                0.0433395   |               0.0115932  |            0.0433395 |           0.0885661 |          0.0264023  |              0.5  |                   0.5  |               0.00709924 |               0.255621 |                       2 |              2 |            -0.0290522  |                       5 |       0.0589031  |       -0.0199224  | CONDITIONAL_ONLY_RESEARCH            | weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability              |
| threshold_abs_40_zero             |              5 | -0.00266928 |    0.00156142 |   0.0133557 |               0.499329 |       0.051422   |    0          |           0.599619  |                0.966661 |                0.0575354   |               0.00410601 |            0.0575354 |           0.0587239 |          0.00364509 |              0.5  |                   0.5  |              -0.00266928 |              -0.134527 |                       2 |              4 |            -0.0258563  |                       2 |       0.00976661 |       -0.0176283  | CONDITIONAL_ONLY_RESEARCH            | weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability |
| threshold_abs_55_zero             |              5 | -0.00225184 |    0.00138408 |   0.0124414 |               0.495302 |       0.0444034  |    0          |           0.599619  |                0.912091 |                0.0572029   |               0.00383028 |            0.0572029 |           0.0551057 |          0.00183681 |              0.5  |                   0.5  |              -0.00225184 |              -0.122914 |                       2 |              4 |            -0.0234203  |                       2 |       0.00869702 |       -0.0155245  | CONDITIONAL_ONLY_RESEARCH            | weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; multi_window_instability |
| stress_strict_panic_drawdown_zero |             20 |  0.0994455  |    0.0994455  |   0.45818   |               0.659091 |       0.0143125  |    0.0116778  |           0.0209724 |                0.334903 |                0.00671693  |               0.010966   |            0.010966  |           0.0590844 |          0.0399273  |            nan    |                 nan    |             nan          |             nan        |                     nan |            nan |           nan          |                       5 |       0.116609   |       -0.0210949  | REJECT_RESEARCH                      | sparse_activation                                                                                             |

## Failure Diagnosis

- Weak WFV persistence was not explained by a single bad validation window. Most stronger variants still had more than one negative or fragile window.
- The most reliable positive regimes remained drawdown acceleration, panic/liquidity stress, volatility spike, and weak breadth.
- Trend-transition, recovery, and high-dispersion rotation were recurring weak states for the base thesis.
- Mild smoothing and rebalance logic reduced churn but did not consistently convert the mechanism into validation-ready behavior.
- Stricter stress gates improved state purity in some slices but introduced sample-size and active-coverage risk.

## Final Classification

`CANDIDATE_FOR_CONDITIONAL_VALIDATION`

## Recommended Next Step

Run a formal conditional-validation pass on a fixed shortlist led by `rebalance_5`, `smooth_5`, `smooth_3`; do not add new volatility concepts.
