# Proxy-Relative Residual Alpha Batch v1

Date: 2026-05-23

Run id: `proxy_relative_residual_alpha_batch_v1`

Status: RESEARCH_ONLY_ALPHA_BATCH

## Research-Only Guardrail

This is a research-only proxy-relative residual alpha batch. It is not sector-relative research, does not fetch external metadata, does not modify detector code or labels, does not register production signals, does not mutate survivor/watchlist state, does not change gates, schemas, thresholds, validation logic, or governance, and does not route anything into portfolio, ML, blending, or optimization workflows.

This batch is proxy-relative, not sector-relative. No sector, industry, GICS, or external peer metadata was used.

## Executive Takeaway

This batch tested whether internally defined behavioral peer proxies can improve medium-horizon residual alpha quality.

Candidates tested: `6`
Status counts: `{"CONDITIONAL_ONLY_RESEARCH": 2, "REJECT_RESEARCH": 4}`

## Candidate Set

| signal_name                                   | family                            | proxy_bucket                        | mechanism_thesis                                                                                                                          | expected_horizon   | run_id                                 | research_status   | relative_label                     |
|:----------------------------------------------|:----------------------------------|:------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:-------------------|:---------------------------------------|:------------------|:-----------------------------------|
| proxy_relative_resilience_20                  | proxy_relative_resilience         | market_relative_behavior_bucket     | Residual resilience is more informative when compared against names with similar trailing market-relative behavior.                       | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |
| liquidity_bucket_relative_repair_20           | liquidity_bucket_repair           | liquidity_bucket                    | Liquidity repair should be judged against names with similar trailing liquidity, not the whole universe.                                  | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |
| volatility_bucket_residual_stability_20       | volatility_bucket_stability       | volatility_bucket                   | Residual stability may be cleaner when measured relative to similarly volatile names.                                                     | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |
| turnover_bucket_exhaustion_residual_10_20     | turnover_bucket_exhaustion        | turnover_bucket                     | Turnover exhaustion should be compared with names experiencing similar turnover intensity to avoid raw volume-event duplication.          | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |
| residual_vol_bucket_quality_recovery_20       | residual_vol_bucket_recovery      | residual_vol_bucket                 | Quality recovery among names with similar residual volatility may separate idiosyncratic repair from low-volatility carry.                | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |
| liquidity_volatility_peer_residual_quality_20 | liquidity_volatility_peer_quality | liquidity_x_volatility_proxy_bucket | Residual quality that survives joint liquidity and volatility proxy comparison may be less broad than absolute-state interaction signals. | h10-h20            | proxy_relative_residual_alpha_batch_v1 | RESEARCH_ONLY     | proxy_relative_not_sector_relative |

## Structural Quality And Active Coverage

| signal_name                                   |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:----------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| proxy_relative_resilience_20                  |     0.0403054 |     0.959695 |        0.971401 |        0.0552331 |       0.556699 |            0.971401 |                        1 |               0.987949 |
| liquidity_bucket_relative_repair_20           |     0.0406444 |     0.959356 |        0.971401 |        0.0537712 |       0.53924  |            0.971401 |                        1 |               0.9876   |
| volatility_bucket_residual_stability_20       |     0.0406145 |     0.959386 |        0.971401 |        0.0499662 |       0.499304 |            0.971401 |                        1 |               0.98763  |
| turnover_bucket_exhaustion_residual_10_20     |     0.0406444 |     0.959356 |        0.971401 |        0.0630927 |       0.632505 |            0.971401 |                        1 |               0.9876   |
| residual_vol_bucket_quality_recovery_20       |     0.0406444 |     0.959356 |        0.971401 |        0.048223  |       0.480922 |            0.971401 |                        1 |               0.9876   |
| liquidity_volatility_peer_residual_quality_20 |     0.0404749 |     0.959525 |        0.971401 |        0.0457235 |       0.456962 |            0.971401 |                        1 |               0.987774 |

## Multi-Horizon IC

| signal_name                                   |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:----------------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| proxy_relative_resilience_20                  |         1 | -0.00151498  |   0.00151498  | -0.0265044  |           0.495336 |      2037 | False             |
| liquidity_bucket_relative_repair_20           |         1 | -0.000865669 |   0.000865669 | -0.0124436  |           0.496318 |      2037 | False             |
| volatility_bucket_residual_stability_20       |         1 | -0.000188113 |   0.000188113 | -0.00231529 |           0.499755 |      2037 | False             |
| turnover_bucket_exhaustion_residual_10_20     |         1 | -0.000493672 |   0.000493672 | -0.00809509 |           0.489936 |      2037 | False             |
| residual_vol_bucket_quality_recovery_20       |         1 | -0.0022852   |   0.0022852   | -0.0325796  |           0.479627 |      2037 | False             |
| liquidity_volatility_peer_residual_quality_20 |         1 | -0.00211178  |   0.00211178  | -0.0298239  |           0.493373 |      2037 | False             |
| proxy_relative_resilience_20                  |         5 | -0.00274971  |   0.00274971  | -0.0477396  |           0.495819 |      2033 | True              |
| liquidity_bucket_relative_repair_20           |         5 | -0.00195421  |   0.00195421  | -0.0280547  |           0.480079 |      2033 | False             |
| volatility_bucket_residual_stability_20       |         5 |  0.00110972  |   0.00110972  |  0.0138487  |           0.492868 |      2033 | False             |
| turnover_bucket_exhaustion_residual_10_20     |         5 | -0.00122939  |   0.00122939  | -0.0201383  |           0.484506 |      2033 | True              |
| residual_vol_bucket_quality_recovery_20       |         5 | -0.00463973  |   0.00463973  | -0.0676961  |           0.466306 |      2033 | False             |
| liquidity_volatility_peer_residual_quality_20 |         5 | -0.0025724   |   0.0025724   | -0.0366547  |           0.490408 |      2033 | False             |
| proxy_relative_resilience_20                  |        10 | -0.00274142  |   0.00274142  | -0.048039   |           0.500986 |      2028 | False             |
| liquidity_bucket_relative_repair_20           |        10 | -0.00270999  |   0.00270999  | -0.040267   |           0.496548 |      2028 | False             |
| volatility_bucket_residual_stability_20       |        10 |  0.00247808  |   0.00247808  |  0.0317847  |           0.504438 |      2028 | False             |
| turnover_bucket_exhaustion_residual_10_20     |        10 |  0.000567887 |   0.000567887 |  0.00951585 |           0.500986 |      2028 | False             |
| residual_vol_bucket_quality_recovery_20       |        10 | -0.0058452   |   0.0058452   | -0.0892568  |           0.470414 |      2028 | True              |
| liquidity_volatility_peer_residual_quality_20 |        10 |  0.000670661 |   0.000670661 |  0.0097901  |           0.512327 |      2028 | False             |
| proxy_relative_resilience_20                  |        20 |  0.000149445 |   0.000149445 |  0.00271289 |           0.506442 |      2018 | False             |
| liquidity_bucket_relative_repair_20           |        20 | -0.00596813  |   0.00596813  | -0.0909386  |           0.485134 |      2018 | True              |
| volatility_bucket_residual_stability_20       |        20 |  0.00410607  |   0.00410607  |  0.0575306  |           0.529732 |      2018 | True              |
| turnover_bucket_exhaustion_residual_10_20     |        20 |  0.000346665 |   0.000346665 |  0.00570694 |           0.498513 |      2018 | False             |
| residual_vol_bucket_quality_recovery_20       |        20 | -0.00369306  |   0.00369306  | -0.0582863  |           0.485629 |      2018 | False             |
| liquidity_volatility_peer_residual_quality_20 |        20 |  0.00541824  |   0.00541824  |  0.0825949  |           0.526759 |      2018 | True              |

## h10 Ranking

| signal_name                                   |      mean_ic |   positive_ic_rate |   n_dates |
|:----------------------------------------------|-------------:|-------------------:|----------:|
| volatility_bucket_residual_stability_20       |  0.00247808  |           0.504438 |      2028 |
| liquidity_volatility_peer_residual_quality_20 |  0.000670661 |           0.512327 |      2028 |
| turnover_bucket_exhaustion_residual_10_20     |  0.000567887 |           0.500986 |      2028 |
| liquidity_bucket_relative_repair_20           | -0.00270999  |           0.496548 |      2028 |
| proxy_relative_resilience_20                  | -0.00274142  |           0.500986 |      2028 |
| residual_vol_bucket_quality_recovery_20       | -0.0058452   |           0.470414 |      2028 |

## h20 Ranking

| signal_name                                   |      mean_ic |   positive_ic_rate |   n_dates |
|:----------------------------------------------|-------------:|-------------------:|----------:|
| liquidity_volatility_peer_residual_quality_20 |  0.00541824  |           0.526759 |      2018 |
| volatility_bucket_residual_stability_20       |  0.00410607  |           0.529732 |      2018 |
| turnover_bucket_exhaustion_residual_10_20     |  0.000346665 |           0.498513 |      2018 |
| proxy_relative_resilience_20                  |  0.000149445 |           0.506442 |      2018 |
| residual_vol_bucket_quality_recovery_20       | -0.00369306  |           0.485629 |      2018 |
| liquidity_bucket_relative_repair_20           | -0.00596813  |           0.485134 |      2018 |

## WFV-Style Diagnostics

| signal_name                                   |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:----------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| proxy_relative_resilience_20                  |         5 |           4 |              -0.00274911 |              -0.802978 |          0.25 |               0.75 |               0.548429 |
| turnover_bucket_exhaustion_residual_10_20     |         5 |           4 |              -0.00123013 |              -0.60486  |          0.5  |               0.5  |               0.406683 |
| residual_vol_bucket_quality_recovery_20       |        10 |           4 |              -0.0058452  |              -0.782559 |          0.25 |               0.75 |               0.454262 |
| liquidity_bucket_relative_repair_20           |        20 |           4 |              -0.00597014 |              -2.38216  |          0    |               1    |               0.419684 |
| volatility_bucket_residual_stability_20       |        20 |           4 |               0.00410705 |               0.501572 |          0.75 |               0.75 |               0.43935  |
| liquidity_volatility_peer_residual_quality_20 |        20 |           4 |               0.00542542 |               0.670633 |          0.75 |               0.75 |               0.375599 |

## Proxy Bucket Coverage

| proxy_bucket_name           |   bucket |   n_dates |   mean_names |   min_names |   p10_names |   thin_bucket_date_ratio_lt10 |   thin_bucket_date_ratio_lt25 |
|:----------------------------|---------:|----------:|-------------:|------------:|------------:|------------------------------:|------------------------------:|
| beta_bucket                 |        1 |      2057 |      157.157 |         154 |         154 |                             0 |                             0 |
| beta_bucket                 |        2 |      2057 |      157.355 |         154 |         154 |                             0 |                             0 |
| beta_bucket                 |        3 |      2057 |      157.81  |         154 |         154 |                             0 |                             0 |
| liquidity_bucket            |        1 |      2086 |      157.073 |         153 |         153 |                             0 |                             0 |
| liquidity_bucket            |        2 |      2086 |      157.373 |         154 |         154 |                             0 |                             0 |
| liquidity_bucket            |        3 |      2086 |      157.814 |         154 |         154 |                             0 |                             0 |
| liquidity_volatility_bucket |        1 |      2085 |      156.994 |         153 |         153 |                             0 |                             0 |
| liquidity_volatility_bucket |        2 |      2085 |      157.461 |         153 |         154 |                             0 |                             0 |
| liquidity_volatility_bucket |        3 |      2085 |      157.802 |         154 |         154 |                             0 |                             0 |
| market_relative_bucket      |        1 |      2077 |      157.174 |         153 |         154 |                             0 |                             0 |
| market_relative_bucket      |        2 |      2077 |      157.372 |         154 |         154 |                             0 |                             0 |
| market_relative_bucket      |        3 |      2077 |      157.822 |         154 |         154 |                             0 |                             0 |
| residual_vol_bucket         |        1 |      2085 |      157.182 |         154 |         154 |                             0 |                             0 |
| residual_vol_bucket         |        2 |      2085 |      157.377 |         154 |         154 |                             0 |                             0 |
| residual_vol_bucket         |        3 |      2085 |      157.834 |         154 |         154 |                             0 |                             0 |
| turnover_bucket             |        1 |      2058 |      157.039 |         153 |         153 |                             0 |                             0 |
| turnover_bucket             |        2 |      2058 |      157.351 |         154 |         154 |                             0 |                             0 |
| turnover_bucket             |        3 |      2058 |      157.757 |         154 |         154 |                             0 |                             0 |
| volatility_bucket           |        1 |      2085 |      157.182 |         154 |         154 |                             0 |                             0 |
| volatility_bucket           |        2 |      2085 |      157.377 |         154 |         154 |                             0 |                             0 |
| volatility_bucket           |        3 |      2085 |      157.834 |         154 |         154 |                             0 |                             0 |

## Proxy Bucket Stability / Drift

| proxy_bucket_name           |   mean_total_names |   mean_abs_bucket_share_drift |   p95_abs_bucket_share_drift |   max_abs_bucket_share_drift |   dominant_bucket_share_mean |   dominant_bucket_share_p95 | bucket_instability_flag   |
|:----------------------------|-------------------:|------------------------------:|-----------------------------:|-----------------------------:|-----------------------------:|----------------------------:|:--------------------------|
| beta_bucket                 |            472.323 |                   2.20452e-05 |                   0          |                   0.00287977 |                     0.334113 |                    0.334755 | False                     |
| liquidity_bucket            |            472.26  |                   3.69247e-05 |                   0          |                   0.00289226 |                     0.334165 |                    0.334755 | False                     |
| liquidity_volatility_bucket |            472.258 |                   0.00271215  |                   0.00843882 |                   0.0167364  |                     0.334576 |                    0.336152 | False                     |
| market_relative_bucket      |            472.368 |                   2.60014e-05 |                   0          |                   0.004329   |                     0.334106 |                    0.334755 | False                     |
| residual_vol_bucket         |            472.393 |                   2.17492e-05 |                   0          |                   0.00287977 |                     0.334113 |                    0.334755 | False                     |
| turnover_bucket             |            472.147 |                   2.34399e-05 |                   0          |                   0.00289226 |                     0.334125 |                    0.334755 | False                     |
| volatility_bucket           |            472.393 |                   2.17492e-05 |                   0          |                   0.00287977 |                     0.334113 |                    0.334755 | False                     |

## Bucket-Conditioned IC

| signal_name                                   |   horizon | proxy_bucket_name           |   bucket |   n_dates |      mean_ic |   positive_ic_rate |
|:----------------------------------------------|----------:|:----------------------------|---------:|----------:|-------------:|-------------------:|
| liquidity_volatility_peer_residual_quality_20 |        20 | turnover_bucket             |        2 |      2018 |  0.0197022   |           0.576809 |
| liquidity_volatility_peer_residual_quality_20 |        20 | liquidity_volatility_bucket |        1 |      2018 |  0.0125714   |           0.542616 |
| liquidity_volatility_peer_residual_quality_20 |        20 | residual_vol_bucket         |        1 |      2018 |  0.00955777  |           0.532706 |
| liquidity_volatility_peer_residual_quality_20 |        20 | liquidity_bucket            |        2 |      2018 |  0.00939454  |           0.523786 |
| liquidity_volatility_peer_residual_quality_20 |        20 | liquidity_bucket            |        1 |      2018 |  0.0093749   |           0.527255 |
| volatility_bucket_residual_stability_20       |        20 | volatility_bucket           |        2 |      2018 |  0.00825124  |           0.535679 |
| volatility_bucket_residual_stability_20       |        20 | liquidity_bucket            |        1 |      2018 |  0.00816638  |           0.543112 |
| volatility_bucket_residual_stability_20       |        20 | liquidity_volatility_bucket |        2 |      2018 |  0.00708464  |           0.543112 |
| volatility_bucket_residual_stability_20       |        20 | residual_vol_bucket         |        3 |      2018 |  0.00703489  |           0.524777 |
| volatility_bucket_residual_stability_20       |        20 | market_relative_bucket      |        2 |      2018 |  0.00695968  |           0.534192 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | liquidity_volatility_bucket |        1 |      2033 |  0.0050071   |           0.515002 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | liquidity_bucket            |        2 |      2033 |  0.00361246  |           0.506149 |
| liquidity_bucket_relative_repair_20           |        20 | liquidity_bucket            |        3 |      2018 |  0.00336408  |           0.505451 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | volatility_bucket           |        1 |      2033 |  0.00330439  |           0.51697  |
| liquidity_bucket_relative_repair_20           |        20 | residual_vol_bucket         |        2 |      2018 |  0.00250845  |           0.518335 |
| liquidity_bucket_relative_repair_20           |        20 | turnover_bucket             |        2 |      2018 |  0.00243664  |           0.515857 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | residual_vol_bucket         |        1 |      2033 |  0.00241749  |           0.518938 |
| residual_vol_bucket_quality_recovery_20       |        10 | turnover_bucket             |        2 |      2028 |  0.00223573  |           0.516765 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | residual_vol_bucket         |        2 |      2033 |  0.00162239  |           0.508116 |
| proxy_relative_resilience_20                  |         5 | turnover_bucket             |        2 |      2033 |  0.00139758  |           0.516478 |
| liquidity_bucket_relative_repair_20           |        20 | beta_bucket                 |        2 |      2018 |  0.000777799 |           0.49108  |
| proxy_relative_resilience_20                  |         5 | turnover_bucket             |        3 |      2033 |  0.000751705 |           0.495819 |
| proxy_relative_resilience_20                  |         5 | market_relative_bucket      |        3 |      2033 |  0.000717552 |           0.508116 |
| liquidity_bucket_relative_repair_20           |        20 | liquidity_volatility_bucket |        2 |      2018 |  0.00061946  |           0.499504 |
| proxy_relative_resilience_20                  |         5 | beta_bucket                 |        3 |      2033 |  0.00014722  |           0.521397 |
| residual_vol_bucket_quality_recovery_20       |        10 | liquidity_bucket            |        1 |      2028 | -7.31287e-05 |           0.515286 |
| proxy_relative_resilience_20                  |         5 | residual_vol_bucket         |        2 |      2033 | -0.000382816 |           0.488933 |
| residual_vol_bucket_quality_recovery_20       |        10 | beta_bucket                 |        3 |      2028 | -0.00159729  |           0.497041 |
| residual_vol_bucket_quality_recovery_20       |        10 | residual_vol_bucket         |        2 |      2028 | -0.00163242  |           0.484221 |
| residual_vol_bucket_quality_recovery_20       |        10 | market_relative_bucket      |        2 |      2028 | -0.00211165  |           0.495562 |

## Baseline / Inventory / Reversal / Momentum Similarity

| signal_name                                   | top_comparison                           |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   max_low_vol_volcarry_corr | hidden_low_vol_overlap_flag   |
|:----------------------------------------------|:-----------------------------------------|------------------------:|---------------------:|--------------------:|--------------------:|----------------------------:|:------------------------------|
| liquidity_bucket_relative_repair_20           | plain_liquidity_quality                  |               0.256308  |            0.0770636 |          0.0234762  |          0.024165   |                   0.0892871 | False                         |
| liquidity_volatility_peer_residual_quality_20 | plain_liquidity_quality                  |               0.249688  |            0.0775551 |          0.0108679  |          0.0287966  |                   0.09538   | False                         |
| proxy_relative_resilience_20                  | v2_vol_compression_range_expansion_20_60 |               0.0597874 |            0.0250797 |          0.0128051  |          0.0112964  |                   0.0157423 | False                         |
| residual_vol_bucket_quality_recovery_20       | plain_liquidity_quality                  |               0.407495  |            0.0446013 |          0.0383415  |          0.0215361  |                   0.095088  | False                         |
| turnover_bucket_exhaustion_residual_10_20     | plain_liquidity_quality                  |               0.133718  |            0.0702153 |          0.00341845 |          0.011761   |                   0.0836209 | False                         |
| volatility_bucket_residual_stability_20       | plain_beta_60                            |               0.131058  |            0.0524007 |          0.0248108  |          0.00238447 |                   0.0741476 | False                         |

## Stress / Regime Attribution

| signal_name                                   |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:----------------------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| liquidity_volatility_peer_residual_quality_20 |        20 | volatility_spike         |       393 |  0.0102924   |  0.159242   |           0.536896 |
| liquidity_volatility_peer_residual_quality_20 |        20 | weak_breadth             |       508 |  0.00856906  |  0.127415   |           0.55315  |
| liquidity_volatility_peer_residual_quality_20 |        20 | panic_liquidity_stress   |       187 |  0.00731988  |  0.121108   |           0.524064 |
| volatility_bucket_residual_stability_20       |        20 | drawdown_acceleration    |       351 |  0.004431    |  0.0667324  |           0.538462 |
| volatility_bucket_residual_stability_20       |        20 | weak_breadth             |       508 |  0.00370756  |  0.0565561  |           0.529528 |
| proxy_relative_resilience_20                  |         5 | trend_transition         |       570 |  0.00313472  |  0.0548343  |           0.52807  |
| volatility_bucket_residual_stability_20       |        20 | trend_transition         |       555 |  0.00287108  |  0.0400303  |           0.533333 |
| volatility_bucket_residual_stability_20       |        20 | recovery_phase           |       196 |  0.00284087  |  0.0451271  |           0.510204 |
| proxy_relative_resilience_20                  |         5 | drawdown_acceleration    |       351 |  0.0021528   |  0.04185    |           0.524217 |
| proxy_relative_resilience_20                  |         5 | panic_liquidity_stress   |       187 |  0.00125066  |  0.028029   |           0.497326 |
| liquidity_bucket_relative_repair_20           |        20 | panic_liquidity_stress   |       187 |  0.0010908   |  0.0162401  |           0.491979 |
| liquidity_volatility_peer_residual_quality_20 |        20 | high_dispersion_rotation |       570 |  0.000912097 |  0.0151664  |           0.492982 |
| proxy_relative_resilience_20                  |         5 | high_dispersion_rotation |       579 | -6.85958e-05 | -0.00121837 |           0.519862 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | weak_breadth             |       508 | -0.000524651 | -0.00823932 |           0.48622  |
| turnover_bucket_exhaustion_residual_10_20     |         5 | recovery_phase           |       196 | -0.00178091  | -0.033679   |           0.479592 |
| liquidity_bucket_relative_repair_20           |        20 | volatility_spike         |       393 | -0.00219665  | -0.0348762  |           0.503817 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | drawdown_acceleration    |       351 | -0.00230116  | -0.0356744  |           0.470085 |
| liquidity_bucket_relative_repair_20           |        20 | drawdown_acceleration    |       351 | -0.00276683  | -0.0412139  |           0.48433  |
| turnover_bucket_exhaustion_residual_10_20     |         5 | volatility_spike         |       404 | -0.00450754  | -0.0719403  |           0.462871 |
| residual_vol_bucket_quality_recovery_20       |        10 | weak_breadth             |       508 | -0.00453329  | -0.073547   |           0.470472 |
| liquidity_bucket_relative_repair_20           |        20 | weak_breadth             |       508 | -0.00485553  | -0.0691578  |           0.507874 |
| residual_vol_bucket_quality_recovery_20       |        10 | panic_liquidity_stress   |       187 | -0.00543068  | -0.0830477  |           0.470588 |
| residual_vol_bucket_quality_recovery_20       |        10 | drawdown_acceleration    |       351 | -0.006326    | -0.0995245  |           0.45584  |
| residual_vol_bucket_quality_recovery_20       |        10 | trend_transition         |       565 | -0.00634951  | -0.0990482  |           0.461947 |

## Proxy State Attribution

| signal_name                                   |   horizon | state                   |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:----------------------------------------------|----------:|:------------------------|----------:|-------------:|------------:|-------------------:|
| liquidity_volatility_peer_residual_quality_20 |        20 | VOLATILITY_SPIKE        |       393 |  0.0102924   |  0.159242   |           0.536896 |
| liquidity_volatility_peer_residual_quality_20 |        20 | WEAK_BREADTH            |       508 |  0.00856906  |  0.127415   |           0.55315  |
| liquidity_volatility_peer_residual_quality_20 |        20 | HIGH_VOLATILITY_PROXY   |      2018 |  0.00541824  |  0.0825949  |           0.526759 |
| liquidity_volatility_peer_residual_quality_20 |        20 | HIGH_BETA_PROXY         |      2018 |  0.00541824  |  0.0825949  |           0.526759 |
| volatility_bucket_residual_stability_20       |        20 | HIGH_VOLATILITY_PROXY   |      2018 |  0.00410607  |  0.0575306  |           0.529732 |
| volatility_bucket_residual_stability_20       |        20 | HIGH_RESIDUAL_VOL_PROXY |      2018 |  0.00410607  |  0.0575306  |           0.529732 |
| volatility_bucket_residual_stability_20       |        20 | HIGH_TURNOVER_PROXY     |      2018 |  0.00410607  |  0.0575306  |           0.529732 |
| volatility_bucket_residual_stability_20       |        20 | HIGH_BETA_PROXY         |      2018 |  0.00410607  |  0.0575306  |           0.529732 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | WEAK_BREADTH            |       508 | -0.000524651 | -0.00823932 |           0.48622  |
| turnover_bucket_exhaustion_residual_10_20     |         5 | HIGH_TURNOVER_PROXY     |      2033 | -0.00122939  | -0.0201383  |           0.484506 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | HIGH_RESIDUAL_VOL_PROXY |      2033 | -0.00122939  | -0.0201383  |           0.484506 |
| turnover_bucket_exhaustion_residual_10_20     |         5 | HIGH_VOLATILITY_PROXY   |      2033 | -0.00122939  | -0.0201383  |           0.484506 |
| liquidity_bucket_relative_repair_20           |        20 | VOLATILITY_SPIKE        |       393 | -0.00219665  | -0.0348762  |           0.503817 |
| proxy_relative_resilience_20                  |         5 | VOLATILITY_SPIKE        |       404 | -0.00259543  | -0.0472768  |           0.475248 |
| proxy_relative_resilience_20                  |         5 | HIGH_LIQUIDITY_PROXY    |      2033 | -0.00274971  | -0.0477396  |           0.495819 |
| proxy_relative_resilience_20                  |         5 | HIGH_RESIDUAL_VOL_PROXY |      2033 | -0.00274971  | -0.0477396  |           0.495819 |
| proxy_relative_resilience_20                  |         5 | HIGH_TURNOVER_PROXY     |      2033 | -0.00274971  | -0.0477396  |           0.495819 |
| residual_vol_bucket_quality_recovery_20       |        10 | WEAK_BREADTH            |       508 | -0.00453329  | -0.073547   |           0.470472 |
| liquidity_bucket_relative_repair_20           |        20 | WEAK_BREADTH            |       508 | -0.00485553  | -0.0691578  |           0.507874 |
| liquidity_bucket_relative_repair_20           |        20 | BROAD_STRESS            |       705 | -0.0048911   | -0.07187    |           0.503546 |
| residual_vol_bucket_quality_recovery_20       |        10 | HIGH_TURNOVER_PROXY     |      2028 | -0.0058452   | -0.0892568  |           0.470414 |
| residual_vol_bucket_quality_recovery_20       |        10 | HIGH_BETA_PROXY         |      2028 | -0.0058452   | -0.0892568  |           0.470414 |
| residual_vol_bucket_quality_recovery_20       |        10 | HIGH_RESIDUAL_VOL_PROXY |      2028 | -0.0058452   | -0.0892568  |           0.470414 |
| liquidity_bucket_relative_repair_20           |        20 | HIGH_VOLATILITY_PROXY   |      2018 | -0.00596813  | -0.0909386  |           0.485134 |

## Fragility / Concentration Summary

| signal_name                                   |   horizon |   full_mean_ic |   crisis_mean_ic |   non_crisis_mean_ic |   crisis_positive_ic_rate |   non_crisis_positive_ic_rate |   crisis_valid_dates |   non_crisis_valid_dates |   crisis_positive_contribution_share |   one_window_dominance | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | regime_exclusivity_flag   |
|:----------------------------------------------|----------:|---------------:|-----------------:|---------------------:|--------------------------:|------------------------------:|---------------------:|-------------------------:|-------------------------------------:|-----------------------:|:------------------------------|:----------------------------|:--------------------------------|:--------------------------|
| proxy_relative_resilience_20                  |         5 |    -0.00274971 |      -0.00364789 |         -0.00226141  |                  0.490223 |                      0.498861 |                  716 |                     1317 |                             0.333835 |               0.548429 | False                         | False                       | False                           | False                     |
| turnover_bucket_exhaustion_residual_10_20     |         5 |    -0.00122939 |      -0.00224828 |         -0.000675451 |                  0.473464 |                      0.490509 |                  716 |                     1317 |                             0.350866 |               0.406683 | False                         | False                       | False                           | False                     |
| residual_vol_bucket_quality_recovery_20       |        10 |    -0.0058452  |      -0.0067054  |         -0.00537678  |                  0.462937 |                      0.474486 |                  715 |                     1313 |                             0.330421 |               0.454262 | False                         | False                       | False                           | False                     |
| liquidity_bucket_relative_repair_20           |        20 |    -0.00596813 |      -0.0048911  |         -0.00654643  |                  0.503546 |                      0.475248 |                  705 |                     1313 |                             0.375917 |               0.419684 | False                         | False                       | False                           | False                     |
| volatility_bucket_residual_stability_20       |        20 |     0.00410607 |       0.0020722  |          0.00519813  |                  0.526241 |                      0.531607 |                  705 |                     1313 |                             0.322799 |               0.43935  | False                         | False                       | False                           | False                     |
| liquidity_volatility_peer_residual_quality_20 |        20 |     0.00541824 |       0.00529939 |          0.00548206  |                  0.52766  |                      0.526276 |                  705 |                     1313 |                             0.351635 |               0.375599 | False                         | False                       | False                           | False                     |

## Proxy Fragility / One-Bucket Dominance

| signal_name                                   | best_proxy_bucket_name      |   best_proxy_bucket |   best_bucket_mean_ic |   best_bucket_positive_ic_rate |   one_bucket_dominance | one_bucket_dominance_flag   |   unstable_proxy_count | peer_group_drift_flag   |
|:----------------------------------------------|:----------------------------|--------------------:|----------------------:|-------------------------------:|-----------------------:|:----------------------------|-----------------------:|:------------------------|
| liquidity_bucket_relative_repair_20           | liquidity_bucket            |                   3 |            0.00336408 |                       0.505451 |              0.346583  | False                       |                      0 | False                   |
| liquidity_volatility_peer_residual_quality_20 | turnover_bucket             |                   2 |            0.0197022  |                       0.576809 |              0.174668  | False                       |                      0 | False                   |
| proxy_relative_resilience_20                  | turnover_bucket             |                   2 |            0.00139758 |                       0.516478 |              0.463687  | False                       |                      0 | False                   |
| residual_vol_bucket_quality_recovery_20       | turnover_bucket             |                   2 |            0.00223573 |                       0.516765 |              1         | True                        |                      0 | False                   |
| turnover_bucket_exhaustion_residual_10_20     | liquidity_volatility_bucket |                   1 |            0.0050071  |                       0.515002 |              0.282857  | False                       |                      0 | False                   |
| volatility_bucket_residual_stability_20       | volatility_bucket           |                   2 |            0.00825124 |                       0.535679 |              0.0976338 | False                       |                      0 | False                   |

## Candidate Decisions

| signal_name                                   |   horizon_x |     mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |   h10_mean_ic |   h10_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   horizon_y |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |   positive_regime_count |   best_regime_ic | top_comparison                           |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage | stress_only_dependency_flag   | crisis_concentration_flag   | one_window_concentration_flag   | regime_exclusivity_flag   | best_proxy_bucket_name      |   best_proxy_bucket |   best_bucket_mean_ic |   best_bucket_positive_ic_rate |   one_bucket_dominance | one_bucket_dominance_flag   |   unstable_proxy_count | peer_group_drift_flag   |   max_low_vol_volcarry_corr | hidden_low_vol_overlap_flag   | status                    | review_issues                                                                                                                                                                              |
|:----------------------------------------------|------------:|------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|--------------:|-----------------------:|--------------:|-----------------------:|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|------------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|------------------------:|-----------------:|:-----------------------------------------|------------------------:|---------------------:|--------------------:|--------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|:------------------------------|:----------------------------|:--------------------------------|:--------------------------|:----------------------------|--------------------:|----------------------:|-------------------------------:|-----------------------:|:----------------------------|-----------------------:|:------------------------|----------------------------:|:------------------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| liquidity_volatility_peer_residual_quality_20 |          20 |  0.00541824 |    0.00541824 |  0.0825949 |   0.0825949 |           0.526759 |      2018 |             20 | True              |   0.000670661 |               0.512327 |   0.00541824  |               0.526759 |   2098 |       478 |     0.0404749 |     0.959525 |        0.971401 |               0.959525 |           0 |        0.0457235 |       0.456962 |       0.539145 |                     1 |          20 |           4 |               0.00542542 |               0.670633 |          0.75 |               0.75 |               0.375599 |                       3 |      0.0102924   | plain_liquidity_quality                  |               0.249688  |            0.0775551 |          0.0108679  |          0.0287966  |           2038 |            0.971401 |                        1 |               0.987774 | False                         | False                       | False                           | False                     | turnover_bucket             |                   2 |            0.0197022  |                       0.576809 |              0.174668  | False                       |                      0 | False                   |                   0.09538   | False                         | CONDITIONAL_ONLY_RESEARCH | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; broad_activation_with_weak_ic                                                                                         |
| volatility_bucket_residual_stability_20       |          20 |  0.00410607 |    0.00410607 |  0.0575306 |   0.0575306 |           0.529732 |      2018 |             20 | True              |   0.00247808  |               0.504438 |   0.00410607  |               0.529732 |   2098 |       478 |     0.0406145 |     0.959386 |        0.971401 |               0.959386 |           0 |        0.0499662 |       0.499304 |       0.59268  |                     1 |          20 |           4 |               0.00410705 |               0.501572 |          0.75 |               0.75 |               0.43935  |                       1 |      0.004431    | plain_beta_60                            |               0.131058  |            0.0524007 |          0.0248108  |          0.00238447 |           2038 |            0.971401 |                        1 |               0.98763  | False                         | False                       | False                           | False                     | volatility_bucket           |                   2 |            0.00825124 |                       0.535679 |              0.0976338 | False                       |                      0 | False                   |                   0.0741476 | False                         | CONDITIONAL_ONLY_RESEARCH | weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; broad_activation_with_weak_ic                                                                                         |
| turnover_bucket_exhaustion_residual_10_20     |           5 | -0.00122939 |    0.00122939 | -0.0201383 |   0.0201383 |           0.484506 |      2033 |              5 | True              |   0.000567887 |               0.500986 |   0.000346665 |               0.498513 |   2098 |       478 |     0.0406444 |     0.959356 |        0.971401 |               0.959356 |           0 |        0.0630927 |       0.632505 |       0.689259 |                     1 |           5 |           4 |              -0.00123013 |              -0.60486  |          0.5  |               0.5  |               0.406683 |                       0 |     -0.000524651 | plain_liquidity_quality                  |               0.133718  |            0.0702153 |          0.00341845 |          0.011761   |           2038 |            0.971401 |                        1 |               0.9876   | False                         | False                       | False                           | False                     | liquidity_volatility_bucket |                   1 |            0.0050071  |                       0.515002 |              0.282857  | False                       |                      0 | False                   |                   0.0836209 | False                         | REJECT_RESEARCH           | direction_mismatch; short_horizon_led; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency; broad_activation_with_weak_ic |
| proxy_relative_resilience_20                  |           5 | -0.00274971 |    0.00274971 | -0.0477396 |   0.0477396 |           0.495819 |      2033 |              5 | True              |  -0.00274142  |               0.500986 |   0.000149445 |               0.506442 |   2098 |       478 |     0.0403054 |     0.959695 |        0.971401 |               0.959695 |           0 |        0.0552331 |       0.556699 |       0.630994 |                     1 |           5 |           4 |              -0.00274911 |              -0.802978 |          0.25 |               0.75 |               0.548429 |                       0 |      0.00313472  | v2_vol_compression_range_expansion_20_60 |               0.0597874 |            0.0250797 |          0.0128051  |          0.0112964  |           2038 |            0.971401 |                        1 |               0.987949 | False                         | False                       | False                           | False                     | turnover_bucket             |                   2 |            0.00139758 |                       0.516478 |              0.463687  | False                       |                      0 | False                   |                   0.0157423 | False                         | REJECT_RESEARCH           | direction_mismatch; short_horizon_led; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; broad_activation_with_weak_ic                            |
| residual_vol_bucket_quality_recovery_20       |          10 | -0.0058452  |    0.0058452  | -0.0892568 |   0.0892568 |           0.470414 |      2028 |             10 | True              |  -0.0058452   |               0.470414 |  -0.00369306  |               0.485629 |   2098 |       478 |     0.0406444 |     0.959356 |        0.971401 |               0.959356 |           0 |        0.048223  |       0.480922 |       0.553662 |                     1 |          10 |           4 |              -0.0058452  |              -0.782559 |          0.25 |               0.75 |               0.454262 |                       0 |     -0.00453329  | plain_liquidity_quality                  |               0.407495  |            0.0446013 |          0.0383415  |          0.0215361  |           2038 |            0.971401 |                        1 |               0.9876   | False                         | False                       | False                           | False                     | turnover_bucket             |                   2 |            0.00223573 |                       0.516765 |              1         | True                        |                      0 | False                   |                   0.095088  | False                         | REJECT_RESEARCH           | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; broad_activation_with_weak_ic; one_bucket_dominance                         |
| liquidity_bucket_relative_repair_20           |          20 | -0.00596813 |    0.00596813 | -0.0909386 |   0.0909386 |           0.485134 |      2018 |             20 | True              |  -0.00270999  |               0.496548 |  -0.00596813  |               0.485134 |   2098 |       478 |     0.0406444 |     0.959356 |        0.971401 |               0.959356 |           0 |        0.0537712 |       0.53924  |       0.608314 |                     1 |          20 |           4 |              -0.00597014 |              -2.38216  |          0    |               1    |               0.419684 |                       0 |      0.0010908   | plain_liquidity_quality                  |               0.256308  |            0.0770636 |          0.0234762  |          0.024165   |           2038 |            0.971401 |                        1 |               0.9876   | False                         | False                       | False                           | False                     | liquidity_bucket            |                   3 |            0.00336408 |                       0.505451 |              0.346583  | False                       |                      0 | False                   |                   0.0892871 | False                         | REJECT_RESEARCH           | direction_mismatch; weak_best_horizon_ic; weak_medium_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; broad_activation_with_weak_ic                                               |

## Recommendation

Do not advance to validation or refinement from this batch. Preserve any weak clues as research evidence only.

No candidate should be promoted, registered, added to survivor/watchlist, or routed into validation, portfolio, ML, blending, or optimization from this batch alone.
