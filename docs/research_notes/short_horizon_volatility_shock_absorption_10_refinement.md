# Short Horizon Volatility Shock Absorption 10 Refinement

## Executive Takeaway

This research-only refinement tested `short_horizon_volatility_shock_absorption_10` under isolated run `short_horizon_volatility_shock_absorption_10_refinement` using a small controlled set of interpretable variants.

Final classification: `CONDITIONAL_REFINEMENT_CANDIDATE`
Best variant: `rebalance_5_zero`
Best-variant issues: `best_horizon_h5_not_h10`

The pass supports a real short-horizon volatility-shock absorption effect, but it does not yet justify validation. The strongest profiles remain h5-led or h10-modest rather than clean h10 validation-quality candidates.

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, broad search, or implementation of other Expansion v5 concepts was performed.

## Source Context

- V1 note: `docs/research_notes/short_horizon_volatility_shock_absorption_10_v1.md`
- V1 artifact directory: `artifacts/research/short_horizon_volatility_shock_absorption_10_v1`
- Expansion v5 design screen: `docs/research_notes/track_b_expansion_v5_design_screening.md`
- Conditional Alpha Inventory Monitoring v2: `docs/research_notes/conditional_alpha_inventory_monitoring_v2.md`

## Variant Registry

| variant                             | description                                                                               |   smoothing |   rebalance |   shock_floor |   fast_q |   range_q |   recent_window |   market_vol_mult |   market_range_mult |   rank_stab_floor | h10_focus   | inactive_nan   |
|:------------------------------------|:------------------------------------------------------------------------------------------|------------:|------------:|--------------:|---------:|----------:|----------------:|------------------:|--------------------:|------------------:|:------------|:---------------|
| base_rebalance_10_zero              | V1 reference logic recreated for refinement comparability.                                |           1 |          10 |          0.55 |      0.5 |      0.45 |              10 |              1.15 |                1.1  |            nan    | False       | False          |
| smooth_3_rebalance_10_zero          | Mild 3-day smoothing to test h5 noise versus persistent short-horizon edge.               |           3 |          10 |          0.55 |      0.5 |      0.45 |              10 |              1.15 |                1.1  |            nan    | False       | False          |
| rebalance_5_zero                    | Shorter rebalance interval to test whether the h5 edge needs faster refresh.              |           1 |           5 |          0.55 |      0.5 |      0.45 |              10 |              1.15 |                1.1  |            nan    | False       | False          |
| strict_shock_rebalance_10_zero      | Stricter volatility shock activation to test over-broad shock states.                     |           1 |          10 |          0.65 |      0.5 |      0.45 |               8 |              1.1  |                1.05 |            nan    | False       | False          |
| strong_absorption_rebalance_10_zero | Stronger absorption confirmation to test whether h10 improves with cleaner stabilization. |           1 |          10 |          0.55 |      0.6 |      0.55 |              10 |              1.1  |                1.05 |            nan    | False       | False          |
| low_churn_rebalance_10_zero         | Adds a rank-stability floor to test whether lower churn improves h10.                     |           1 |          10 |          0.55 |      0.5 |      0.45 |              10 |              1.15 |                1.1  |              0.55 | False       | False          |
| h10_focus_rebalance_10_zero         | Adds h10 path stabilization emphasis without changing the concept family.                 |           3 |          10 |          0.55 |      0.5 |      0.45 |              12 |              1.15 |                1.1  |              0.5  | True        | False          |
| inactive_nan_rebalance_10           | Keeps inactive dates as NaN to test inactive-date handling.                               |           1 |          10 |          0.55 |      0.5 |      0.45 |              10 |              1.15 |                1.1  |            nan    | False       | True           |

## Candidate Decisions

| signal_name                         |   best_horizon |     mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h20_mean_ic |   turnover_proxy |   active_date_ratio |   persistence |   sign_consistency |   one_window_dominance |   max_inventory_corr |   max_volatility_stress_corr |   max_price_reversal_corr |   max_price_momentum_corr | status                           | review_issues                                                                                                                                |
|:------------------------------------|---------------:|------------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|--------------:|-----------------:|--------------------:|--------------:|-------------------:|-----------------------:|---------------------:|-----------------------------:|--------------------------:|--------------------------:|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| strict_shock_rebalance_10_zero      |              5 |  0.00939901 |   0.00939901 |              0.539394 |    0.00731107 |               0.567073 |    0.00596981 |   0.00505592  |       0.0041118  |            0.157293 |          0.75 |               0.75 |               0.712168 |            0.101926  |                    0.101926  |                0.00514236 |                0.00889987 | CONDITIONAL_ONLY_RESEARCH        | h10_below_validation_quality; best_horizon_h5_not_h10; one_window_concentration                                                              |
| strong_absorption_rebalance_10_zero |              5 |  0.0112707  |   0.0112707  |              0.569697 |    0.0056796  |               0.564024 |    0.0018112  |  -0.00100001  |       0.00491562 |            0.157293 |          0.75 |               0.75 |               0.68889  |            0.110741  |                    0.110741  |                0.00527088 |                0.00800933 | CONDITIONAL_ONLY_RESEARCH        | h10_below_validation_quality; best_horizon_h5_not_h10; one_window_concentration                                                              |
| rebalance_5_zero                    |              5 |  0.0126393  |   0.0126393  |              0.582051 |    0.0102596  |               0.600515 |    0.00533318 |   0.00324326  |       0.0110028  |            0.185891 |          1    |               1    |               0.351775 |            0.123023  |                    0.123023  |                0.00621939 |                0.00688119 | CONDITIONAL_REFINEMENT_CANDIDATE | best_horizon_h5_not_h10                                                                                                                      |
| smooth_3_rebalance_10_zero          |              5 |  0.0111919  |   0.0111919  |              0.5825   |    0.00876176 |               0.570352 |    0.0064534  |   0.0042271   |       0.00664356 |            0.190658 |          0.75 |               0.75 |               0.505439 |            0.117549  |                    0.117549  |                0.00676484 |                0.00743206 | CONDITIONAL_REFINEMENT_CANDIDATE | h10_below_validation_quality; best_horizon_h5_not_h10                                                                                        |
| base_rebalance_10_zero              |              5 |  0.0110449  |   0.0110449  |              0.5825   |    0.00855832 |               0.572864 |    0.00603389 |   0.00352201  |       0.00664126 |            0.190658 |          0.75 |               0.75 |               0.493203 |            0.117222  |                    0.117222  |                0.00656897 |                0.00721618 | CONDITIONAL_REFINEMENT_CANDIDATE | h10_below_validation_quality; best_horizon_h5_not_h10                                                                                        |
| h10_focus_rebalance_10_zero         |              5 |  0.00480738 |   0.00480738 |              0.504255 |    0.00449211 |               0.50641  |    0.00118629 |  -0.000996041 |       0.00334408 |            0.224023 |          0.75 |               0.75 |               0.563705 |            0.0739145 |                    0.0739145 |                0.00757812 |                0.010353   | REJECT_RESEARCH                  | h10_below_validation_quality; h10_positive_rate_below_validation_quality; best_horizon_h5_not_h10                                            |
| low_churn_rebalance_10_zero         |              5 |  0.00396884 |   0.00396884 |              0.5125   |    0.00347348 |               0.492462 |    0.00261589 |   0.00194492  |       0.00260884 |            0.190658 |          0.75 |               0.75 |               0.586743 |            0.0680082 |                    0.0680082 |                0.00463865 |                0.00578821 | REJECT_RESEARCH                  | h10_below_validation_quality; h10_positive_rate_below_validation_quality; best_horizon_h5_not_h10                                            |
| inactive_nan_rebalance_10           |              5 | -0.030629   |  -0.030629   |              0.4225   |   -0.0211243  |               0.434673 |   -0.016843   |  -0.0190187   |       0.0229979  |            0.190658 |          0    |               1    |               0.491018 |            0.0523009 |                    0.24798   |                0.019873   |                0.0198741  | REJECT_RESEARCH                  | h10_below_validation_quality; h10_positive_rate_below_validation_quality; best_horizon_h5_not_h10; h20_dependency_risk; weak_wfv_persistence |

## Multi-Horizon IC

| signal_name                         |   horizon |      mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:------------------------------------|----------:|-------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| base_rebalance_10_zero              |         5 |  0.0110449   |   0.0110449   |  0.14211   |   0.14211   |           0.5825   |       400 |              5 | True              |
| smooth_3_rebalance_10_zero          |         5 |  0.0111919   |   0.0111919   |  0.143905  |   0.143905  |           0.5825   |       400 |              5 | True              |
| rebalance_5_zero                    |         5 |  0.0126393   |   0.0126393   |  0.166104  |   0.166104  |           0.582051 |       390 |              5 | True              |
| strict_shock_rebalance_10_zero      |         5 |  0.00939901  |   0.00939901  |  0.128923  |   0.128923  |           0.539394 |       330 |              5 | True              |
| strong_absorption_rebalance_10_zero |         5 |  0.0112707   |   0.0112707   |  0.146821  |   0.146821  |           0.569697 |       330 |              5 | True              |
| low_churn_rebalance_10_zero         |         5 |  0.00396884  |   0.00396884  |  0.0705133 |   0.0705133 |           0.5125   |       400 |              5 | True              |
| h10_focus_rebalance_10_zero         |         5 |  0.00480738  |   0.00480738  |  0.0851095 |   0.0851095 |           0.504255 |       470 |              5 | True              |
| inactive_nan_rebalance_10           |         5 | -0.030629    |   0.030629    | -0.203477  |   0.203477  |           0.4225   |       400 |              5 | True              |
| base_rebalance_10_zero              |        10 |  0.00855832  |   0.00855832  |  0.109254  |   0.109254  |           0.572864 |       398 |              5 | False             |
| smooth_3_rebalance_10_zero          |        10 |  0.00876176  |   0.00876176  |  0.112024  |   0.112024  |           0.570352 |       398 |              5 | False             |
| rebalance_5_zero                    |        10 |  0.0102596   |   0.0102596   |  0.142425  |   0.142425  |           0.600515 |       388 |              5 | False             |
| strict_shock_rebalance_10_zero      |        10 |  0.00731107  |   0.00731107  |  0.097418  |   0.097418  |           0.567073 |       328 |              5 | False             |
| strong_absorption_rebalance_10_zero |        10 |  0.0056796   |   0.0056796   |  0.0744161 |   0.0744161 |           0.564024 |       328 |              5 | False             |
| low_churn_rebalance_10_zero         |        10 |  0.00347348  |   0.00347348  |  0.0602904 |   0.0602904 |           0.492462 |       398 |              5 | False             |
| h10_focus_rebalance_10_zero         |        10 |  0.00449211  |   0.00449211  |  0.0773175 |   0.0773175 |           0.50641  |       468 |              5 | False             |
| inactive_nan_rebalance_10           |        10 | -0.0211243   |   0.0211243   | -0.14794   |   0.14794   |           0.434673 |       398 |              5 | False             |
| base_rebalance_10_zero              |        15 |  0.00603389  |   0.00603389  |  0.0789551 |   0.0789551 |           0.569975 |       393 |              5 | False             |
| smooth_3_rebalance_10_zero          |        15 |  0.0064534   |   0.0064534   |  0.0844552 |   0.0844552 |           0.569975 |       393 |              5 | False             |
| rebalance_5_zero                    |        15 |  0.00533318  |   0.00533318  |  0.0746576 |   0.0746576 |           0.582245 |       383 |              5 | False             |
| strict_shock_rebalance_10_zero      |        15 |  0.00596981  |   0.00596981  |  0.0831231 |   0.0831231 |           0.544892 |       323 |              5 | False             |
| strong_absorption_rebalance_10_zero |        15 |  0.0018112   |   0.0018112   |  0.0245305 |   0.0245305 |           0.563467 |       323 |              5 | False             |
| low_churn_rebalance_10_zero         |        15 |  0.00261589  |   0.00261589  |  0.049013  |   0.049013  |           0.475827 |       393 |              5 | False             |
| h10_focus_rebalance_10_zero         |        15 |  0.00118629  |   0.00118629  |  0.0216324 |   0.0216324 |           0.468683 |       463 |              5 | False             |
| inactive_nan_rebalance_10           |        15 | -0.016843    |   0.016843    | -0.110533  |   0.110533  |           0.452926 |       393 |              5 | False             |
| base_rebalance_10_zero              |        20 |  0.00352201  |   0.00352201  |  0.0442991 |   0.0442991 |           0.533505 |       388 |              5 | False             |
| smooth_3_rebalance_10_zero          |        20 |  0.0042271   |   0.0042271   |  0.053229  |   0.053229  |           0.536082 |       388 |              5 | False             |
| rebalance_5_zero                    |        20 |  0.00324326  |   0.00324326  |  0.0416154 |   0.0416154 |           0.536842 |       380 |              5 | False             |
| strict_shock_rebalance_10_zero      |        20 |  0.00505592  |   0.00505592  |  0.0661902 |   0.0661902 |           0.477987 |       318 |              5 | False             |
| strong_absorption_rebalance_10_zero |        20 | -0.00100001  |   0.00100001  | -0.0130967 |   0.0130967 |           0.518868 |       318 |              5 | False             |
| low_churn_rebalance_10_zero         |        20 |  0.00194492  |   0.00194492  |  0.0365219 |   0.0365219 |           0.489691 |       388 |              5 | False             |
| h10_focus_rebalance_10_zero         |        20 | -0.000996041 |   0.000996041 | -0.0183555 |   0.0183555 |           0.478166 |       458 |              5 | False             |
| inactive_nan_rebalance_10           |        20 | -0.0190187   |   0.0190187   | -0.134513  |   0.134513  |           0.420103 |       388 |              5 | False             |

## WFV-Style Diagnostics

| signal_name                         |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| base_rebalance_10_zero              |         5 |           4 |               0.0110449  |               1.25322  |          0.75 |               0.75 |               0.493203 |
| smooth_3_rebalance_10_zero          |         5 |           4 |               0.0111919  |               1.2254   |          0.75 |               0.75 |               0.505439 |
| rebalance_5_zero                    |         5 |           4 |               0.0126309  |               3.40287  |          1    |               1    |               0.351775 |
| strict_shock_rebalance_10_zero      |         5 |           4 |               0.00937439 |               0.875136 |          0.75 |               0.75 |               0.712168 |
| strong_absorption_rebalance_10_zero |         5 |           4 |               0.0112214  |               0.879442 |          0.75 |               0.75 |               0.68889  |
| low_churn_rebalance_10_zero         |         5 |           4 |               0.00396884 |               0.604115 |          0.75 |               0.75 |               0.586743 |
| h10_focus_rebalance_10_zero         |         5 |           4 |               0.00478945 |               0.654504 |          0.75 |               0.75 |               0.563705 |
| inactive_nan_rebalance_10           |         5 |           4 |              -0.030629   |              -1.28626  |          0    |               1    |               0.491018 |

## Active Coverage

| signal_name                         |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:------------------------------------|---------------:|--------------------:|-------------------------:|-----------------------:|
| base_rebalance_10_zero              |            400 |            0.190658 |                       56 |               0.989435 |
| smooth_3_rebalance_10_zero          |            400 |            0.190658 |                       56 |               0.989435 |
| rebalance_5_zero                    |            390 |            0.185891 |                       88 |               0.990049 |
| strict_shock_rebalance_10_zero      |            330 |            0.157293 |                       48 |               0.989286 |
| strong_absorption_rebalance_10_zero |            330 |            0.157293 |                       48 |               0.989286 |
| low_churn_rebalance_10_zero         |            400 |            0.190658 |                       56 |               0.989435 |
| h10_focus_rebalance_10_zero         |            470 |            0.224023 |                       66 |               0.989184 |
| inactive_nan_rebalance_10           |            400 |            0.190658 |                       56 |               0.109885 |

## Similarity Summary

| signal_name                         | top_comparison                   |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   price_rank_reversal_5_corr |   price_rank_reversal_20_corr |   residual_momentum_10_corr |   residual_momentum_20_corr |   drawdown_pressure_proxy_corr |   idiosyncratic_stress_proxy_corr |   short_vol_shock_absorption_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   max_price_momentum_corr |   max_price_reversal_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_drawdown_pressure_corr |   max_idiosyncratic_stress_corr |   max_vol_shock_absorption_corr |   max_low_volatility_corr |
|:------------------------------------|:---------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-----------------------------:|------------------------------:|----------------------------:|----------------------------:|-------------------------------:|----------------------------------:|----------------------------------------:|-----------------------------------:|--------------------------------------:|--------------------------------:|-----------------------------------------:|--------------------------:|--------------------------:|----------------------------------------:|-----------------------------:|-----------------------------:|--------------------------------:|--------------------------------:|--------------------------:|
| base_rebalance_10_zero              | short_vol_shock_absorption_proxy |                0.168854 |                 0.0390882  |               0.00212861 |                   0.117222  |            0.117222  |          0.0028978  |          0.00636768 |                  0.00656899  |                   0.00721618  |                   0.00468613  |                    0.00087044 |                    0.00636768 |                  0.00656897  |                   0.000870415 |                 0.00721618  |                  0.00087044 |                     0.00240985 |                         0.133234  |                              0.168854   |                         0.0039903  |                             0.0931009 |                       0.0624277 |                                0.0768115 |                0.00721618 |                0.00656897 |                               0.0390882 |                    0.117222  |                   0.00240985 |                       0.133234  |                      0.168854   |                 0.0768115 |
| h10_focus_rebalance_10_zero         | short_vol_shock_absorption_proxy |                0.116248 |                 0.0352344  |               0.00615667 |                   0.0739145 |            0.0739145 |          0.0101619  |          0.010353   |                  0.000311808 |                   0.000908192 |                   0.00329307  |                    0.00757809 |                    0.010353   |                  0.000311774 |                   0.00757812  |                 0.000908192 |                  0.00757809 |                     0.0281929  |                         0.0979476 |                              0.116248   |                         0.00968507 |                             0.0581965 |                       0.0362773 |                                0.0446034 |                0.010353   |                0.00757812 |                               0.0352344 |                    0.0739145 |                   0.0281929  |                       0.0979476 |                      0.116248   |                 0.0446034 |
| inactive_nan_rebalance_10           | volatility_stabilization_proxy   |                0.24798  |                 0.00920491 |               0.0523009  |                   0.0194893 |            0.0523009 |          0.00806928 |          0.0114377  |                  0.0198741   |                   0.0083729   |                   0.000237167 |                    0.00730311 |                    0.0114377  |                  0.019873    |                   0.00730202  |                 0.0083729   |                  0.00730311 |                     0.115443   |                         0.178168  |                              0.00183475 |                         0.0118448  |                             0.24798   |                       0.147965  |                                0.169478  |                0.0198741  |                0.019873   |                               0.0523009 |                    0.24798   |                   0.115443   |                       0.178168  |                      0.00183475 |                 0.169478  |
| low_churn_rebalance_10_zero         | short_vol_shock_absorption_proxy |                0.101752 |                 0.0292485  |               0.00781265 |                   0.0680082 |            0.0680082 |          0.00672005 |          0.00578821 |                  0.000628294 |                   0.000751463 |                   0.00234938  |                    0.00463861 |                    0.00578821 |                  0.000628256 |                   0.00463865  |                 0.000751463 |                  0.00463861 |                     0.0284993  |                         0.0850225 |                              0.101752   |                         0.00677579 |                             0.0486646 |                       0.0321941 |                                0.0412682 |                0.00578821 |                0.00463865 |                               0.0292485 |                    0.0680082 |                   0.0284993  |                       0.0850225 |                      0.101752   |                 0.0412682 |
| rebalance_5_zero                    | short_vol_shock_absorption_proxy |                0.19292  |                 0.0494083  |               0.00512197 |                   0.123023  |            0.123023  |          0.00832173 |          0.00688119 |                  0.0062194   |                   0.00505741  |                   0.00141992  |                    0.004147   |                    0.00688119 |                  0.00621939  |                   0.00414701  |                 0.00505741  |                  0.004147   |                     0.0187565  |                         0.166936  |                              0.19292    |                         0.00892327 |                             0.0685424 |                       0.0862019 |                                0.103677  |                0.00688119 |                0.00621939 |                               0.0494083 |                    0.123023  |                   0.0187565  |                       0.166936  |                      0.19292    |                 0.103677  |
| smooth_3_rebalance_10_zero          | short_vol_shock_absorption_proxy |                0.169118 |                 0.0390233  |               0.00194395 |                   0.117549  |            0.117549  |          0.0028267  |          0.00649154 |                  0.00676486  |                   0.00743206  |                   0.0049104   |                    0.00102923 |                    0.00649154 |                  0.00676484  |                   0.0010292   |                 0.00743206  |                  0.00102923 |                     0.00227262 |                         0.133489  |                              0.169118   |                         0.00402921 |                             0.09329   |                       0.0627326 |                                0.0771245 |                0.00743206 |                0.00676484 |                               0.0390233 |                    0.117549  |                   0.00227262 |                       0.133489  |                      0.169118   |                 0.0771245 |
| strict_shock_rebalance_10_zero      | short_vol_shock_absorption_proxy |                0.136279 |                 0.034938   |               0.00278752 |                   0.101926  |            0.101926  |          0.00882577 |          0.00889987 |                  0.00414839  |                   0.00454232  |                   0.0010982   |                    0.00514234 |                    0.00889987 |                  0.00414838  |                   0.00514236  |                 0.00454232  |                  0.00514234 |                     0.00112266 |                         0.106333  |                              0.136279   |                         0.00842394 |                             0.0777272 |                       0.0572214 |                                0.0671618 |                0.00889987 |                0.00514236 |                               0.034938  |                    0.101926  |                   0.00112266 |                       0.106333  |                      0.136279   |                 0.0671618 |
| strong_absorption_rebalance_10_zero | short_vol_shock_absorption_proxy |                0.144735 |                 0.0315008  |               0.00153522 |                   0.110741  |            0.110741  |          0.00645057 |          0.00800933 |                  0.00527089  |                   0.00610617  |                   0.00366565  |                    0.00229037 |                    0.00800933 |                  0.00527088  |                   0.00229039  |                 0.00610617  |                  0.00229037 |                     0.00163211 |                         0.113374  |                              0.144735   |                         0.00642899 |                             0.0889149 |                       0.0544354 |                                0.0661674 |                0.00800933 |                0.00527088 |                               0.0315008 |                    0.110741  |                   0.00163211 |                       0.113374  |                      0.144735   |                 0.0661674 |

## Sample-Size Sanity

| state                                    |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio | signal_name                         |
|:-----------------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|:------------------------------------|
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           183 |                     0.0872259 | base_rebalance_10_zero              |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           366 |                     0.174452  | base_rebalance_10_zero              |
| VOLATILITY_SHOCK_ABSORBING               |           421 |           0.200667 |                           259 |                     0.123451  | base_rebalance_10_zero              |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |           0.200667 |                           259 |                     0.123451  | base_rebalance_10_zero              |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |           0.217827 |                           221 |                     0.105338  | base_rebalance_10_zero              |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |           0.216873 |                           270 |                     0.128694  | base_rebalance_10_zero              |
| MARKET_VOL_ABSORBING                     |           639 |           0.304576 |                           301 |                     0.14347   | base_rebalance_10_zero              |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           367 |                     0.174929  | base_rebalance_10_zero              |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           183 |                     0.0872259 | smooth_3_rebalance_10_zero          |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           366 |                     0.174452  | smooth_3_rebalance_10_zero          |
| VOLATILITY_SHOCK_ABSORBING               |           421 |           0.200667 |                           259 |                     0.123451  | smooth_3_rebalance_10_zero          |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |           0.200667 |                           259 |                     0.123451  | smooth_3_rebalance_10_zero          |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |           0.217827 |                           221 |                     0.105338  | smooth_3_rebalance_10_zero          |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |           0.216873 |                           270 |                     0.128694  | smooth_3_rebalance_10_zero          |
| MARKET_VOL_ABSORBING                     |           639 |           0.304576 |                           301 |                     0.14347   | smooth_3_rebalance_10_zero          |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           367 |                     0.174929  | smooth_3_rebalance_10_zero          |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           159 |                     0.0757865 | rebalance_5_zero                    |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           361 |                     0.172069  | rebalance_5_zero                    |
| VOLATILITY_SHOCK_ABSORBING               |           421 |           0.200667 |                           291 |                     0.138704  | rebalance_5_zero                    |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |           0.200667 |                           291 |                     0.138704  | rebalance_5_zero                    |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |           0.217827 |                           244 |                     0.116301  | rebalance_5_zero                    |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |           0.216873 |                           303 |                     0.144423  | rebalance_5_zero                    |
| MARKET_VOL_ABSORBING                     |           639 |           0.304576 |                           326 |                     0.155386  | rebalance_5_zero                    |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           362 |                     0.172545  | rebalance_5_zero                    |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           156 |                     0.0743565 | strict_shock_rebalance_10_zero      |
| RECENT_VOLATILITY_SHOCK                  |           985 |           0.469495 |                           271 |                     0.129171  | strict_shock_rebalance_10_zero      |
| VOLATILITY_SHOCK_ABSORBING               |           312 |           0.148713 |                           157 |                     0.0748332 | strict_shock_rebalance_10_zero      |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           312 |           0.148713 |                           157 |                     0.0748332 | strict_shock_rebalance_10_zero      |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           364 |           0.173499 |                           147 |                     0.0700667 | strict_shock_rebalance_10_zero      |
| CONTAINED_DISPERSION_VOL_SHOCK           |           340 |           0.162059 |                           164 |                     0.0781697 | strict_shock_rebalance_10_zero      |
| MARKET_VOL_ABSORBING                     |           493 |           0.234986 |                           189 |                     0.0900858 | strict_shock_rebalance_10_zero      |
| BROAD_HOSTILE_OR_STRESS                  |          1139 |           0.542898 |                           276 |                     0.131554  | strict_shock_rebalance_10_zero      |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           156 |                     0.0743565 | strong_absorption_rebalance_10_zero |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           299 |                     0.142517  | strong_absorption_rebalance_10_zero |
| VOLATILITY_SHOCK_ABSORBING               |           350 |           0.166826 |                           176 |                     0.0838894 | strong_absorption_rebalance_10_zero |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           350 |           0.166826 |                           176 |                     0.0838894 | strong_absorption_rebalance_10_zero |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           404 |           0.192564 |                           167 |                     0.0795996 | strong_absorption_rebalance_10_zero |
| CONTAINED_DISPERSION_VOL_SHOCK           |           378 |           0.180172 |                           183 |                     0.0872259 | strong_absorption_rebalance_10_zero |
| MARKET_VOL_ABSORBING                     |           537 |           0.255958 |                           211 |                     0.100572  | strong_absorption_rebalance_10_zero |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           300 |                     0.142993  | strong_absorption_rebalance_10_zero |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           183 |                     0.0872259 | low_churn_rebalance_10_zero         |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           366 |                     0.174452  | low_churn_rebalance_10_zero         |
| VOLATILITY_SHOCK_ABSORBING               |           421 |           0.200667 |                           259 |                     0.123451  | low_churn_rebalance_10_zero         |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |           0.200667 |                           259 |                     0.123451  | low_churn_rebalance_10_zero         |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |           0.217827 |                           221 |                     0.105338  | low_churn_rebalance_10_zero         |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |           0.216873 |                           270 |                     0.128694  | low_churn_rebalance_10_zero         |
| MARKET_VOL_ABSORBING                     |           639 |           0.304576 |                           301 |                     0.14347   | low_churn_rebalance_10_zero         |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           367 |                     0.174929  | low_churn_rebalance_10_zero         |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           183 |                     0.0872259 | h10_focus_rebalance_10_zero         |
| RECENT_VOLATILITY_SHOCK                  |          1092 |           0.520496 |                           399 |                     0.190181  | h10_focus_rebalance_10_zero         |
| VOLATILITY_SHOCK_ABSORBING               |           462 |           0.22021  |                           289 |                     0.13775   | h10_focus_rebalance_10_zero         |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           462 |           0.22021  |                           289 |                     0.13775   | h10_focus_rebalance_10_zero         |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           502 |           0.239276 |                           251 |                     0.119638  | h10_focus_rebalance_10_zero         |
| CONTAINED_DISPERSION_VOL_SHOCK           |           496 |           0.236416 |                           300 |                     0.142993  | h10_focus_rebalance_10_zero         |
| MARKET_VOL_ABSORBING                     |           687 |           0.327455 |                           333 |                     0.158723  | h10_focus_rebalance_10_zero         |
| BROAD_HOSTILE_OR_STRESS                  |          1233 |           0.587703 |                           407 |                     0.193994  | h10_focus_rebalance_10_zero         |
| VOLATILITY_SHOCK_ACTIVE                  |           663 |           0.316015 |                           183 |                     0.0872259 | inactive_nan_rebalance_10           |
| RECENT_VOLATILITY_SHOCK                  |          1042 |           0.496663 |                           366 |                     0.174452  | inactive_nan_rebalance_10           |
| VOLATILITY_SHOCK_ABSORBING               |           421 |           0.200667 |                           259 |                     0.123451  | inactive_nan_rebalance_10           |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |           0.200667 |                           259 |                     0.123451  | inactive_nan_rebalance_10           |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |           0.217827 |                           221 |                     0.105338  | inactive_nan_rebalance_10           |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |           0.216873 |                           270 |                     0.128694  | inactive_nan_rebalance_10           |
| MARKET_VOL_ABSORBING                     |           639 |           0.304576 |                           301 |                     0.14347   | inactive_nan_rebalance_10           |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |           0.565777 |                           367 |                     0.174929  | inactive_nan_rebalance_10           |

## Volatility-Shock Attribution

| signal_name                         |   horizon | state                                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:------------------------------------|----------:|:-----------------------------------------|----------:|------------:|-----------:|-------------------:|
| base_rebalance_10_zero              |         5 | recovery_phase                           |        55 |  0.0264746  |  0.27619   |           0.563636 |
| base_rebalance_10_zero              |         5 | trend_transition                         |       140 |  0.025215   |  0.344488  |           0.664286 |
| base_rebalance_10_zero              |         5 | drawdown_acceleration                    |        75 |  0.0247187  |  0.31746   |           0.64     |
| base_rebalance_10_zero              |         5 | VOLATILITY_SHOCK_ABSORBING               |       259 |  0.0157611  |  0.197559  |           0.602317 |
| base_rebalance_10_zero              |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       259 |  0.0157611  |  0.197559  |           0.602317 |
| base_rebalance_10_zero              |         5 | CONTAINED_DISPERSION_VOL_SHOCK           |       270 |  0.0154791  |  0.194961  |           0.607407 |
| h10_focus_rebalance_10_zero         |         5 | recovery_phase                           |        62 |  0.0231565  |  0.384326  |           0.677419 |
| h10_focus_rebalance_10_zero         |         5 | trend_transition                         |       146 |  0.0145287  |  0.249052  |           0.575342 |
| h10_focus_rebalance_10_zero         |         5 | high_dispersion_rotation                 |       116 |  0.0104673  |  0.182459  |           0.508621 |
| h10_focus_rebalance_10_zero         |         5 | drawdown_acceleration                    |        78 |  0.0101094  |  0.178894  |           0.551282 |
| h10_focus_rebalance_10_zero         |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       251 |  0.00775462 |  0.132511  |           0.50996  |
| h10_focus_rebalance_10_zero         |         5 | MARKET_VOL_ABSORBING                     |       333 |  0.0069591  |  0.119353  |           0.510511 |
| inactive_nan_rebalance_10           |         5 | recovery_phase                           |        55 |  0.00852144 |  0.0698525 |           0.563636 |
| inactive_nan_rebalance_10           |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       221 | -0.0117068  | -0.0874971 |           0.466063 |
| inactive_nan_rebalance_10           |         5 | VOLATILITY_SHOCK_ABSORBING               |       259 | -0.0217419  | -0.15415   |           0.436293 |
| inactive_nan_rebalance_10           |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       259 | -0.0217419  | -0.15415   |           0.436293 |
| inactive_nan_rebalance_10           |         5 | CONTAINED_DISPERSION_VOL_SHOCK           |       270 | -0.025003   | -0.171826  |           0.425926 |
| inactive_nan_rebalance_10           |         5 | MARKET_VOL_ABSORBING                     |       301 | -0.0282272  | -0.193399  |           0.421927 |
| low_churn_rebalance_10_zero         |         5 | recovery_phase                           |        55 |  0.0175917  |  0.271258  |           0.6      |
| low_churn_rebalance_10_zero         |         5 | trend_transition                         |       140 |  0.0125302  |  0.222757  |           0.585714 |
| low_churn_rebalance_10_zero         |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       221 |  0.0110323  |  0.184713  |           0.556561 |
| low_churn_rebalance_10_zero         |         5 | drawdown_acceleration                    |        75 |  0.0108088  |  0.185778  |           0.56     |
| low_churn_rebalance_10_zero         |         5 | MARKET_VOL_ABSORBING                     |       301 |  0.00900474 |  0.151947  |           0.551495 |
| low_churn_rebalance_10_zero         |         5 | VOLATILITY_SHOCK_ABSORBING               |       259 |  0.00842161 |  0.145038  |           0.559846 |
| rebalance_5_zero                    |         5 | drawdown_acceleration                    |        60 |  0.0323824  |  0.41105   |           0.683333 |
| rebalance_5_zero                    |         5 | trend_transition                         |       132 |  0.0283736  |  0.394171  |           0.651515 |
| rebalance_5_zero                    |         5 | high_dispersion_rotation                 |        86 |  0.0234869  |  0.313934  |           0.651163 |
| rebalance_5_zero                    |         5 | recovery_phase                           |        54 |  0.0209179  |  0.23267   |           0.611111 |
| rebalance_5_zero                    |         5 | weak_breadth                             |       104 |  0.0175098  |  0.261099  |           0.673077 |
| rebalance_5_zero                    |         5 | MARKET_VOL_ABSORBING                     |       326 |  0.0144618  |  0.190688  |           0.595092 |
| smooth_3_rebalance_10_zero          |         5 | recovery_phase                           |        55 |  0.0269105  |  0.281489  |           0.563636 |
| smooth_3_rebalance_10_zero          |         5 | trend_transition                         |       140 |  0.0252388  |  0.34487   |           0.664286 |
| smooth_3_rebalance_10_zero          |         5 | drawdown_acceleration                    |        75 |  0.0250534  |  0.3215    |           0.64     |
| smooth_3_rebalance_10_zero          |         5 | VOLATILITY_SHOCK_ABSORBING               |       259 |  0.0159751  |  0.200279  |           0.602317 |
| smooth_3_rebalance_10_zero          |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       259 |  0.0159751  |  0.200279  |           0.602317 |
| smooth_3_rebalance_10_zero          |         5 | CONTAINED_DISPERSION_VOL_SHOCK           |       270 |  0.015684   |  0.197566  |           0.607407 |
| strict_shock_rebalance_10_zero      |         5 | recovery_phase                           |        52 |  0.034404   |  0.381981  |           0.634615 |
| strict_shock_rebalance_10_zero      |         5 | trend_transition                         |       119 |  0.0187826  |  0.23983   |           0.588235 |
| strict_shock_rebalance_10_zero      |         5 | drawdown_acceleration                    |        66 |  0.0167083  |  0.219603  |           0.575758 |
| strict_shock_rebalance_10_zero      |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       147 |  0.0140089  |  0.182842  |           0.537415 |
| strict_shock_rebalance_10_zero      |         5 | VOLATILITY_SHOCK_ABSORBING               |       157 |  0.0124154  |  0.168973  |           0.522293 |
| strict_shock_rebalance_10_zero      |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       157 |  0.0124154  |  0.168973  |           0.522293 |
| strong_absorption_rebalance_10_zero |         5 | recovery_phase                           |        52 |  0.043549   |  0.478706  |           0.615385 |
| strong_absorption_rebalance_10_zero |         5 | trend_transition                         |       119 |  0.0229519  |  0.306663  |           0.630252 |
| strong_absorption_rebalance_10_zero |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       167 |  0.0157919  |  0.199109  |           0.556886 |
| strong_absorption_rebalance_10_zero |         5 | VOLATILITY_SHOCK_ABSORBING               |       176 |  0.0149154  |  0.192011  |           0.5625   |
| strong_absorption_rebalance_10_zero |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       176 |  0.0149154  |  0.192011  |           0.5625   |
| strong_absorption_rebalance_10_zero |         5 | CONTAINED_DISPERSION_VOL_SHOCK           |       183 |  0.0145146  |  0.185375  |           0.557377 |

## Diagnostic Answers

- h5 stability: best h5 IC was `0.012639`; WFV persistence/sign consistency were `1.00` / `1.00`.
- h10 validation quality: best selected h10 IC was `0.010260` with positive IC rate `0.600515`; this remains below the validation-quality floor.
- h20 dependence: best selected h20 IC was `0.003243`, so the selected profile is not h20-dominant.
- Volatility inventory similarity: max volatility/stress corr was `0.123023`.
- Inventory similarity: max inventory corr was `0.123023`.

## Recommendation

Keep `short_horizon_volatility_shock_absorption_10` as a `CONDITIONAL_REFINEMENT_CANDIDATE`. It is the first Expansion v5 candidate to materially reduce h20 concentration, but it should not move to conditional validation until h10 strength improves without sacrificing the short-horizon curve or raising similarity to `volatility_compression_after_stress_stabilization`.
