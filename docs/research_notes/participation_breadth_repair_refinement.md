# Participation Breadth Repair Refinement

## Executive Takeaway

This research-only pass refines `participation_breadth_repair_under_hostile_trend` from the Track B v5 focused discovery run.

Final classification: `CANDIDATE_FOR_CONDITIONAL_VALIDATION`.

This was a narrow refinement diagnostics pass. It did not broaden discovery, run production registration, promote survivor/watchlist state, modify gates or schemas, change thresholds, use ML, alter portfolio logic, or wire production Conditional-Alpha paths.

Variants tested: 15

## Variant Set

| variant_name                             | category             | description                                                                                 | run_id                                     | source_signal                                    |
|:-----------------------------------------|:---------------------|:--------------------------------------------------------------------------------------------|:-------------------------------------------|:-------------------------------------------------|
| base                                     | source               | Original v5 focused-discovery signal.                                                       | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| smooth_3                                 | mild_smoothing       | 3-day rolling mean.                                                                         | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| smooth_5                                 | mild_smoothing       | 5-day rolling mean.                                                                         | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| rebalance_5                              | rebalance            | 5-day rebalance cadence with forward fill.                                                  | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| rebalance_10                             | rebalance            | 10-day rebalance cadence with forward fill.                                                 | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| rank_persist_5_zero                      | rank_persistence     | Keep values only when current and 5-day lag signs agree; zero inactive.                     | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| rank_persist_10_zero                     | rank_persistence     | Keep values only when current and 10-day lag signs agree; zero inactive.                    | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| threshold_0p20_zero                      | activation_threshold | Zero values with absolute score below 0.20.                                                 | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| threshold_0p20_nan                       | activation_threshold | Mask values with absolute score below 0.20.                                                 | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| threshold_0p35_zero                      | activation_threshold | Zero values with absolute score below 0.35.                                                 | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| strict_weak_breadth_zero                 | state_strictness     | Require weak breadth in addition to the source hostile-repair logic; zero inactive.         | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| strict_recent_stress_zero                | state_strictness     | Require recent stress in addition to the source hostile-repair logic; zero inactive.        | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| strict_low_extension_zero                | state_strictness     | Require low market extension in addition to the source hostile-repair logic; zero inactive. | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| strict_weak_breadth_rebalance_10         | combined_control     | Weak-breadth strictness plus 10-day rebalance cadence.                                      | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |
| strict_breadth_repair_recent_stress_zero | combined_control     | Require breadth repair and recent stress; zero inactive.                                    | participation_breadth_repair_refinement_v1 | participation_breadth_repair_under_hostile_trend |

## Structural Quality / Turnover / Active Coverage

| variant_name                             |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-----------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| base                                     |     0.0258864 |     0.974114 |        0.985701 |        0.0164583 |     0          |           0.181125  |                       54 |               0.988769 |
| smooth_3                                 |     0.026363  |     0.973637 |        0.985224 |        0.0168545 |     0.00210747 |           0.206864  |                       54 |               0.98887  |
| smooth_5                                 |     0.0268397 |     0.97316  |        0.984747 |        0.0169085 |     0.109796   |           0.232602  |                       54 |               0.988948 |
| rebalance_5                              |     0.0258864 |     0.974114 |        0.985701 |        0.0164583 |     0          |           0.181125  |                       54 |               0.988769 |
| rebalance_10                             |     0.0258864 |     0.974114 |        0.985701 |        0.0164583 |     0          |           0.181125  |                       54 |               0.988769 |
| rank_persist_5_zero                      |     0         |     1        |        1        |        0.0215755 |     0.131505   |           0.617255  |                       30 |               1        |
| rank_persist_10_zero                     |     0         |     1        |        1        |        0.0168178 |     0          |           0.648236  |                       24 |               1        |
| threshold_0p20_zero                      |     0         |     1        |        1        |        0.0156353 |     0          |           0.181125  |                       54 |               1        |
| threshold_0p20_nan                       |     0.85669   |     0.14331  |        0.189704 |        0.021207  |     0          |           0.181125  |                       54 |               0.791125 |
| threshold_0p35_zero                      |     0         |     1        |        1        |        0.0144507 |     0          |           0.181125  |                       54 |               1        |
| strict_weak_breadth_zero                 |     0.0258864 |     0.974114 |        0.985701 |        0.0160399 |     0          |           0.0981888 |                       60 |               0.989408 |
| strict_recent_stress_zero                |     0.0258864 |     0.974114 |        0.985701 |        0.0154907 |     0          |           0.169685  |                       50 |               0.988611 |
| strict_low_extension_zero                |     0.0258864 |     0.974114 |        0.985701 |        0.0146513 |     0          |           0.113918  |                       54 |               0.991185 |
| strict_weak_breadth_rebalance_10         |     0.0258864 |     0.974114 |        0.985701 |        0.0136189 |     0          |           0.142993  |                       50 |               0.989052 |
| strict_breadth_repair_recent_stress_zero |     0.0258864 |     0.974114 |        0.985701 |        0.022579  |     0          |           0.132984  |                       82 |               0.98849  |

## h20 Refinement Results

| variant_name                             |   mean_ic |   abs_mean_ic |    ic_ir |   positive_ic_rate |   n_dates |
|:-----------------------------------------|----------:|--------------:|---------:|-------------------:|----------:|
| strict_weak_breadth_zero                 | 0.0372266 |     0.0372266 | 0.313499 |           0.592233 |       206 |
| strict_weak_breadth_rebalance_10         | 0.0307203 |     0.0307203 | 0.259466 |           0.580537 |       298 |
| threshold_0p20_nan                       | 0.0253984 |     0.0253984 | 0.195693 |           0.539683 |       378 |
| strict_breadth_repair_recent_stress_zero | 0.0253616 |     0.0253616 | 0.234831 |           0.588448 |       277 |
| smooth_5                                 | 0.0251565 |     0.0251565 | 0.225503 |           0.580321 |       498 |
| smooth_3                                 | 0.023818  |     0.023818  | 0.208468 |           0.573059 |       438 |
| base                                     | 0.0228754 |     0.0228754 | 0.196955 |           0.563492 |       378 |
| rebalance_5                              | 0.0228754 |     0.0228754 | 0.196955 |           0.563492 |       378 |
| rebalance_10                             | 0.0228754 |     0.0228754 | 0.196955 |           0.563492 |       378 |
| strict_recent_stress_zero                | 0.0223458 |     0.0223458 | 0.202859 |           0.567797 |       354 |
| threshold_0p20_zero                      | 0.0222292 |     0.0222292 | 0.192155 |           0.547619 |       378 |
| threshold_0p35_zero                      | 0.022183  |     0.022183  | 0.194231 |           0.550265 |       378 |
| strict_low_extension_zero                | 0.0208351 |     0.0208351 | 0.197079 |           0.552743 |       237 |
| rank_persist_10_zero                     | 0.0169591 |     0.0169591 | 0.177772 |           0.556977 |       860 |
| rank_persist_5_zero                      | 0.0127755 |     0.0127755 | 0.131718 |           0.529574 |       727 |

## Multi-Horizon IC

| variant_name                             |   horizon |      mean_ic |   abs_mean_ic |        ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-----------------------------------------|----------:|-------------:|--------------:|-------------:|-------------------:|----------:|:------------------|
| base                                     |         1 |  0.0067164   |   0.0067164   |  0.0566985   |           0.521053 |       380 | False             |
| smooth_3                                 |         1 |  0.00262681  |   0.00262681  |  0.0225318   |           0.504525 |       442 | False             |
| smooth_5                                 |         1 | -0.00010155  |   0.00010155  | -0.000869934 |           0.492063 |       504 | False             |
| rebalance_5                              |         1 |  0.0067164   |   0.0067164   |  0.0566985   |           0.521053 |       380 | False             |
| rebalance_10                             |         1 |  0.0067164   |   0.0067164   |  0.0566985   |           0.521053 |       380 | False             |
| rank_persist_5_zero                      |         1 | -0.00112776  |   0.00112776  | -0.0111237   |           0.499314 |       729 | False             |
| rank_persist_10_zero                     |         1 |  0.000107049 |   0.000107049 |  0.00105361  |           0.5058   |       862 | False             |
| threshold_0p20_zero                      |         1 |  0.00684987  |   0.00684987  |  0.0579902   |           0.515789 |       380 | False             |
| threshold_0p20_nan                       |         1 |  0.00818502  |   0.00818502  |  0.0621682   |           0.515789 |       380 | False             |
| threshold_0p35_zero                      |         1 |  0.00678852  |   0.00678852  |  0.0581937   |           0.513158 |       380 | False             |
| strict_weak_breadth_zero                 |         1 |  0.0144152   |   0.0144152   |  0.110721    |           0.548544 |       206 | False             |
| strict_recent_stress_zero                |         1 |  0.00781457  |   0.00781457  |  0.0659853   |           0.525281 |       356 | False             |
| strict_low_extension_zero                |         1 |  0.00751314  |   0.00751314  |  0.0660866   |           0.531381 |       239 | False             |
| strict_weak_breadth_rebalance_10         |         1 |  0.00966466  |   0.00966466  |  0.0758521   |           0.53     |       300 | False             |
| strict_breadth_repair_recent_stress_zero |         1 |  0.00818094  |   0.00818094  |  0.067282    |           0.519713 |       279 | False             |
| base                                     |         5 |  0.00891255  |   0.00891255  |  0.0740551   |           0.502632 |       380 | False             |
| smooth_3                                 |         5 |  0.00198947  |   0.00198947  |  0.0162713   |           0.488688 |       442 | False             |
| smooth_5                                 |         5 | -0.000295874 |   0.000295874 | -0.00241537  |           0.484127 |       504 | False             |
| rebalance_5                              |         5 |  0.00891255  |   0.00891255  |  0.0740551   |           0.502632 |       380 | False             |
| rebalance_10                             |         5 |  0.00891255  |   0.00891255  |  0.0740551   |           0.502632 |       380 | False             |
| rank_persist_5_zero                      |         5 | -0.00315077  |   0.00315077  | -0.0301399   |           0.45679  |       729 | False             |
| rank_persist_10_zero                     |         5 |  0.00251902  |   0.00251902  |  0.024241    |           0.486079 |       862 | False             |
| threshold_0p20_zero                      |         5 |  0.009205    |   0.009205    |  0.0768927   |           0.510526 |       380 | False             |
| threshold_0p20_nan                       |         5 |  0.0121971   |   0.0121971   |  0.0906668   |           0.494737 |       380 | False             |
| threshold_0p35_zero                      |         5 |  0.009188    |   0.009188    |  0.0768447   |           0.489474 |       380 | False             |
| strict_weak_breadth_zero                 |         5 |  0.0105709   |   0.0105709   |  0.0794701   |           0.529126 |       206 | False             |
| strict_recent_stress_zero                |         5 |  0.00956222  |   0.00956222  |  0.079791    |           0.505618 |       356 | False             |
| strict_low_extension_zero                |         5 |  0.00944969  |   0.00944969  |  0.081671    |           0.502092 |       239 | False             |
| strict_weak_breadth_rebalance_10         |         5 |  0.0133363   |   0.0133363   |  0.103706    |           0.52     |       300 | False             |
| strict_breadth_repair_recent_stress_zero |         5 |  0.0114341   |   0.0114341   |  0.0949886   |           0.53405  |       279 | False             |
| base                                     |        10 |  0.00536315  |   0.00536315  |  0.0451351   |           0.5      |       380 | False             |
| smooth_3                                 |        10 |  0.00265339  |   0.00265339  |  0.0224701   |           0.484163 |       442 | False             |
| smooth_5                                 |        10 |  0.0033009   |   0.0033009   |  0.028117    |           0.482143 |       504 | False             |
| rebalance_5                              |        10 |  0.00536315  |   0.00536315  |  0.0451351   |           0.5      |       380 | False             |
| rebalance_10                             |        10 |  0.00536315  |   0.00536315  |  0.0451351   |           0.5      |       380 | False             |
| rank_persist_5_zero                      |        10 | -0.00186559  |   0.00186559  | -0.0186007   |           0.459534 |       729 | False             |
| rank_persist_10_zero                     |        10 |  0.00703878  |   0.00703878  |  0.0702914   |           0.512761 |       862 | False             |
| threshold_0p20_zero                      |        10 |  0.0052365   |   0.0052365   |  0.0442642   |           0.513158 |       380 | False             |
| threshold_0p20_nan                       |        10 |  0.00719301  |   0.00719301  |  0.0543193   |           0.510526 |       380 | False             |
| threshold_0p35_zero                      |        10 |  0.00509283  |   0.00509283  |  0.0436462   |           0.507895 |       380 | False             |
| strict_weak_breadth_zero                 |        10 |  0.0111664   |   0.0111664   |  0.0903356   |           0.514563 |       206 | False             |
| strict_recent_stress_zero                |        10 |  0.00550279  |   0.00550279  |  0.0470162   |           0.505618 |       356 | False             |
| strict_low_extension_zero                |        10 |  0.00697554  |   0.00697554  |  0.0626303   |           0.502092 |       239 | False             |
| strict_weak_breadth_rebalance_10         |        10 |  0.0124992   |   0.0124992   |  0.101775    |           0.506667 |       300 | False             |
| strict_breadth_repair_recent_stress_zero |        10 |  0.0123696   |   0.0123696   |  0.107128    |           0.526882 |       279 | False             |
| base                                     |        20 |  0.0228754   |   0.0228754   |  0.196955    |           0.563492 |       378 | True              |
| smooth_3                                 |        20 |  0.023818    |   0.023818    |  0.208468    |           0.573059 |       438 | True              |
| smooth_5                                 |        20 |  0.0251565   |   0.0251565   |  0.225503    |           0.580321 |       498 | True              |
| rebalance_5                              |        20 |  0.0228754   |   0.0228754   |  0.196955    |           0.563492 |       378 | True              |
| rebalance_10                             |        20 |  0.0228754   |   0.0228754   |  0.196955    |           0.563492 |       378 | True              |
| rank_persist_5_zero                      |        20 |  0.0127755   |   0.0127755   |  0.131718    |           0.529574 |       727 | True              |
| rank_persist_10_zero                     |        20 |  0.0169591   |   0.0169591   |  0.177772    |           0.556977 |       860 | True              |
| threshold_0p20_zero                      |        20 |  0.0222292   |   0.0222292   |  0.192155    |           0.547619 |       378 | True              |
| threshold_0p20_nan                       |        20 |  0.0253984   |   0.0253984   |  0.195693    |           0.539683 |       378 | True              |
| threshold_0p35_zero                      |        20 |  0.022183    |   0.022183    |  0.194231    |           0.550265 |       378 | True              |
| strict_weak_breadth_zero                 |        20 |  0.0372266   |   0.0372266   |  0.313499    |           0.592233 |       206 | True              |
| strict_recent_stress_zero                |        20 |  0.0223458   |   0.0223458   |  0.202859    |           0.567797 |       354 | True              |
| strict_low_extension_zero                |        20 |  0.0208351   |   0.0208351   |  0.197079    |           0.552743 |       237 | True              |
| strict_weak_breadth_rebalance_10         |        20 |  0.0307203   |   0.0307203   |  0.259466    |           0.580537 |       298 | True              |
| strict_breadth_repair_recent_stress_zero |        20 |  0.0253616   |   0.0253616   |  0.234831    |           0.588448 |       277 | True              |

## WFV-Style Diagnostics

| variant_name                             |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-----------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| base                                     |        20 |           4 |                0.0228358 |               1.08218  |          1    |               1    |               0.620385 |
| smooth_3                                 |        20 |           4 |                0.0237898 |               1.37858  |          1    |               1    |               0.546792 |
| smooth_5                                 |        20 |           4 |                0.0251332 |               1.74738  |          1    |               1    |               0.486436 |
| rebalance_5                              |        20 |           4 |                0.0228358 |               1.08218  |          1    |               1    |               0.620385 |
| rebalance_10                             |        20 |           4 |                0.0228358 |               1.08218  |          1    |               1    |               0.620385 |
| rank_persist_5_zero                      |        20 |           4 |                0.0127817 |               1.2378   |          0.75 |               0.75 |               0.346672 |
| rank_persist_10_zero                     |        20 |           4 |                0.0169591 |               1.47556  |          0.75 |               0.75 |               0.42035  |
| threshold_0p20_zero                      |        20 |           4 |                0.0221883 |               1.06722  |          1    |               1    |               0.632361 |
| threshold_0p20_nan                       |        20 |           4 |                0.0253538 |               1.13938  |          1    |               1    |               0.612151 |
| threshold_0p35_zero                      |        20 |           4 |                0.0221458 |               1.00015  |          1    |               1    |               0.649192 |
| strict_weak_breadth_zero                 |        20 |           4 |                0.0370424 |               0.950276 |          0.75 |               0.75 |               0.626418 |
| strict_recent_stress_zero                |        20 |           4 |                0.0223698 |               0.640782 |          0.75 |               0.75 |               0.441872 |
| strict_low_extension_zero                |        20 |           4 |                0.0208661 |               1.0208   |          0.75 |               0.75 |               0.630789 |
| strict_weak_breadth_rebalance_10         |        20 |           4 |                0.0306785 |               1.50367  |          1    |               1    |               0.421774 |
| strict_breadth_repair_recent_stress_zero |        20 |           4 |                0.0254925 |               0.919889 |          0.75 |               0.75 |               0.54362  |

## Orthogonality / Similarity

| variant_name                             | top_comparison                                       |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |
|:-----------------------------------------|:-----------------------------------------------------|------------------------:|-------------------------------------:|--------------------:|--------------------:|
| base                                     | current_pool_smooth_trend_persistence_60_low_breadth |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |
| rank_persist_10_zero                     | v2_relative_value_mispricing_decay_20_60             |               0.110056  |                           0.00669565 |           0.0482392 |           0.075759  |
| rank_persist_5_zero                      | v2_relative_value_mispricing_decay_20_60             |               0.0988396 |                           0.0015635  |           0.0467783 |           0.0747849 |
| rebalance_10                             | current_pool_smooth_trend_persistence_60_low_breadth |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |
| rebalance_5                              | current_pool_smooth_trend_persistence_60_low_breadth |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |
| smooth_3                                 | v2_dispersion_stable_leadership_60                   |               0.0857794 |                           0.0179906  |           0.0322461 |           0.080824  |
| smooth_5                                 | v2_relative_value_mispricing_decay_20_60             |               0.0918441 |                           0.00976061 |           0.0369652 |           0.0862917 |
| strict_breadth_repair_recent_stress_zero | current_pool_smooth_trend_persistence_60_low_breadth |               0.0832269 |                           0.0383121  |           0.0129054 |           0.0704017 |
| strict_low_extension_zero                | v2_relative_value_mispricing_decay_20_60             |               0.0654717 |                           0.0117554  |           0.035499  |           0.0523978 |
| strict_recent_stress_zero                | current_pool_smooth_trend_persistence_60_low_breadth |               0.082636  |                           0.0268303  |           0.02313   |           0.0736801 |
| strict_weak_breadth_rebalance_10         | current_pool_smooth_trend_persistence_60_low_breadth |               0.0943045 |                           0.034492   |           0.0152653 |           0.0745735 |
| strict_weak_breadth_zero                 | current_pool_smooth_trend_persistence_60_low_breadth |               0.114339  |                           0.0446555  |           0.0169547 |           0.0651116 |
| threshold_0p20_nan                       | v2_dispersion_stable_leadership_60                   |               0.22673   |                           0.0871244  |           0.0351638 |           0.21434   |
| threshold_0p20_zero                      | current_pool_smooth_trend_persistence_60_low_breadth |               0.0825772 |                           0.0289869  |           0.0227996 |           0.0748906 |
| threshold_0p35_zero                      | current_pool_smooth_trend_persistence_60_low_breadth |               0.0855573 |                           0.0306133  |           0.016549  |           0.0785437 |

## Regime / State Attribution

| signal_name                              |   horizon | state                        |   n_dates |   mean_ic |    ic_ir |   positive_ic_rate |
|:-----------------------------------------|----------:|:-----------------------------|----------:|----------:|---------:|-------------------:|
| strict_weak_breadth_zero                 |        20 | LIQUIDITY_REPAIR             |       127 | 0.0478567 | 0.365386 |           0.614173 |
| smooth_5                                 |        20 | WEAK_BREADTH                 |       232 | 0.0460304 | 0.386347 |           0.642241 |
| threshold_0p20_nan                       |        20 | WEAK_BREADTH                 |       206 | 0.0435505 | 0.328275 |           0.592233 |
| smooth_3                                 |        20 | WEAK_BREADTH                 |       220 | 0.0425885 | 0.354945 |           0.618182 |
| threshold_0p35_zero                      |        20 | WEAK_BREADTH                 |       206 | 0.0378629 | 0.325356 |           0.587379 |
| strict_low_extension_zero                |        20 | VOL_NORMALIZING              |        27 | 0.0374713 | 0.459737 |           0.666667 |
| strict_weak_breadth_zero                 |        20 | BREADTH_REPAIR               |       183 | 0.0373237 | 0.313038 |           0.595628 |
| base                                     |        20 | WEAK_BREADTH                 |       206 | 0.0372266 | 0.313499 |           0.592233 |
| rebalance_10                             |        20 | WEAK_BREADTH                 |       206 | 0.0372266 | 0.313499 |           0.592233 |
| strict_weak_breadth_zero                 |        20 | WEAK_BREADTH                 |       206 | 0.0372266 | 0.313499 |           0.592233 |
| rebalance_5                              |        20 | WEAK_BREADTH                 |       206 | 0.0372266 | 0.313499 |           0.592233 |
| strict_breadth_repair_recent_stress_zero |        20 | WEAK_BREADTH                 |       178 | 0.0367096 | 0.306194 |           0.595506 |
| strict_weak_breadth_zero                 |        20 | RECENT_STRESS                |       201 | 0.0366803 | 0.307412 |           0.59204  |
| strict_recent_stress_zero                |        20 | WEAK_BREADTH                 |       201 | 0.0366803 | 0.307412 |           0.59204  |
| threshold_0p20_zero                      |        20 | WEAK_BREADTH                 |       206 | 0.0365551 | 0.30934  |           0.582524 |
| strict_weak_breadth_rebalance_10         |        20 | WEAK_BREADTH                 |       204 | 0.0362962 | 0.305143 |           0.588235 |
| strict_weak_breadth_rebalance_10         |        20 | BREADTH_REPAIR               |       242 | 0.0323364 | 0.276653 |           0.595041 |
| strict_weak_breadth_rebalance_10         |        20 | LOW_EXTENSION_MARKET         |       180 | 0.0318087 | 0.292312 |           0.566667 |
| threshold_0p20_nan                       |        20 | BREADTH_REPAIR               |       293 | 0.0316708 | 0.248952 |           0.569966 |
| strict_weak_breadth_rebalance_10         |        20 | LIQUIDITY_REPAIR             |       162 | 0.0314952 | 0.250163 |           0.567901 |
| rebalance_5                              |        20 | BREADTH_REPAIR               |       293 | 0.0287865 | 0.253097 |           0.590444 |
| base                                     |        20 | BREADTH_REPAIR               |       293 | 0.0287865 | 0.253097 |           0.590444 |
| rebalance_10                             |        20 | BREADTH_REPAIR               |       293 | 0.0287865 | 0.253097 |           0.590444 |
| threshold_0p20_zero                      |        20 | BREADTH_REPAIR               |       293 | 0.0279313 | 0.246117 |           0.569966 |
| threshold_0p35_zero                      |        20 | BREADTH_REPAIR               |       293 | 0.0278227 | 0.249365 |           0.576792 |
| rank_persist_5_zero                      |        20 | WEAK_BREADTH                 |       312 | 0.0276927 | 0.264632 |           0.560897 |
| smooth_3                                 |        20 | BREADTH_REPAIR               |       312 | 0.0273889 | 0.24744  |           0.596154 |
| rank_persist_10_zero                     |        20 | WEAK_BREADTH                 |       340 | 0.0271149 | 0.265513 |           0.561765 |
| smooth_5                                 |        20 | BREADTH_REPAIR               |       333 | 0.0268291 | 0.246158 |           0.591592 |
| strict_low_extension_zero                |        20 | BREADTH_REPAIR               |       188 | 0.0255079 | 0.2441   |           0.579787 |
| strict_breadth_repair_recent_stress_zero |        20 | RECENT_STRESS                |       277 | 0.0253616 | 0.234831 |           0.588448 |
| strict_recent_stress_zero                |        20 | BREADTH_REPAIR               |       277 | 0.0253616 | 0.234831 |           0.588448 |
| strict_breadth_repair_recent_stress_zero |        20 | BREADTH_REPAIR               |       277 | 0.0253616 | 0.234831 |           0.588448 |
| smooth_5                                 |        20 | LOW_EXTENSION_MARKET         |       321 | 0.0253522 | 0.24173  |           0.576324 |
| strict_low_extension_zero                |        20 | WEAK_BREADTH                 |       115 | 0.024975  | 0.233631 |           0.547826 |
| strict_breadth_repair_recent_stress_zero |        20 | LIQUIDITY_REPAIR             |       150 | 0.0243888 | 0.19527  |           0.526667 |
| smooth_5                                 |        20 | RECENT_STRESS                |       452 | 0.0243869 | 0.229074 |           0.59292  |
| threshold_0p20_nan                       |        20 | RECENT_STRESS                |       354 | 0.0240841 | 0.194356 |           0.542373 |
| threshold_0p20_nan                       |        20 | LOW_EXTENSION_MARKET         |       237 | 0.024004  | 0.207437 |           0.518987 |
| smooth_3                                 |        20 | LOW_EXTENSION_MARKET         |       276 | 0.023726  | 0.222774 |           0.568841 |
| smooth_3                                 |        20 | RECENT_STRESS                |       403 | 0.0231612 | 0.213596 |           0.580645 |
| rank_persist_10_zero                     |        20 | RECENT_STRESS                |       636 | 0.0224491 | 0.231578 |           0.580189 |
| strict_recent_stress_zero                |        20 | RECENT_STRESS                |       354 | 0.0223458 | 0.202859 |           0.567797 |
| base                                     |        20 | RECENT_STRESS                |       354 | 0.0223458 | 0.202859 |           0.567797 |
| rebalance_10                             |        20 | RECENT_STRESS                |       354 | 0.0223458 | 0.202859 |           0.567797 |
| rebalance_5                              |        20 | RECENT_STRESS                |       354 | 0.0223458 | 0.202859 |           0.567797 |
| threshold_0p35_zero                      |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0217406 | 0.213922 |           0.540084 |
| threshold_0p20_zero                      |        20 | RECENT_STRESS                |       354 | 0.0215926 | 0.196788 |           0.550847 |
| threshold_0p35_zero                      |        20 | RECENT_STRESS                |       354 | 0.0212822 | 0.195102 |           0.553672 |
| base                                     |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0208351 | 0.197079 |           0.552743 |
| rebalance_10                             |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0208351 | 0.197079 |           0.552743 |
| rebalance_5                              |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0208351 | 0.197079 |           0.552743 |
| strict_low_extension_zero                |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0208351 | 0.197079 |           0.552743 |
| strict_recent_stress_zero                |        20 | LIQUIDITY_REPAIR             |       178 | 0.020824  | 0.165947 |           0.516854 |
| rank_persist_10_zero                     |        20 | LIQUIDITY_REPAIR             |       362 | 0.020589  | 0.19565  |           0.530387 |
| rank_persist_10_zero                     |        20 | BREADTH_REPAIR               |       450 | 0.0203036 | 0.19845  |           0.557778 |
| threshold_0p20_zero                      |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0195397 | 0.185415 |           0.535865 |
| rank_persist_5_zero                      |        20 | BREADTH_REPAIR               |       411 | 0.0192555 | 0.189597 |           0.564477 |
| rank_persist_5_zero                      |        20 | RECENT_STRESS                |       543 | 0.0191962 | 0.197068 |           0.559853 |
| rank_persist_5_zero                      |        20 | PARTICIPATION_REPAIR_HOSTILE |       255 | 0.0143383 | 0.137783 |           0.52549  |

## Candidate Decisions

| variant_name                             |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   turnover_proxy |   active_date_ratio |   missing_pct |   wfv_persistence |   wfv_sign_consistency |   one_window_dominance |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |   positive_state_count |   best_state_ic | status                               | review_issues                           |
|:-----------------------------------------|--------------:|------------:|-----------------------:|-----------------:|--------------------:|--------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-------------------------------------:|--------------------:|--------------------:|-----------------------:|----------------:|:-------------------------------------|:----------------------------------------|
| strict_weak_breadth_rebalance_10         |     0.0307203 |    0.259466 |               0.580537 |        0.0136189 |           0.142993  |     0.0258864 |              1    |                   1    |               0.421774 |               0.0943045 |                           0.034492   |           0.0152653 |           0.0745735 |                      9 |       0.0362962 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| strict_breadth_repair_recent_stress_zero |     0.0253616 |    0.234831 |               0.588448 |        0.022579  |           0.132984  |     0.0258864 |              0.75 |                   0.75 |               0.54362  |               0.0832269 |                           0.0383121  |           0.0129054 |           0.0704017 |                      8 |       0.0367096 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| smooth_5                                 |     0.0251565 |    0.225503 |               0.580321 |        0.0169085 |           0.232602  |     0.0268397 |              1    |                   1    |               0.486436 |               0.0918441 |                           0.00976061 |           0.0369652 |           0.0862917 |                      9 |       0.0460304 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| smooth_3                                 |     0.023818  |    0.208468 |               0.573059 |        0.0168545 |           0.206864  |     0.026363  |              1    |                   1    |               0.546792 |               0.0857794 |                           0.0179906  |           0.0322461 |           0.080824  |                      9 |       0.0425885 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| base                                     |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |           0.181125  |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| rebalance_5                              |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |           0.181125  |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| rebalance_10                             |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |           0.181125  |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| strict_recent_stress_zero                |     0.0223458 |    0.202859 |               0.567797 |        0.0154907 |           0.169685  |     0.0258864 |              0.75 |                   0.75 |               0.441872 |               0.082636  |                           0.0268303  |           0.02313   |           0.0736801 |                      8 |       0.0366803 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| strict_weak_breadth_zero                 |     0.0372266 |    0.313499 |               0.592233 |        0.0160399 |           0.0981888 |     0.0258864 |              0.75 |                   0.75 |               0.626418 |               0.114339  |                           0.0446555  |           0.0169547 |           0.0651116 |                     10 |       0.0478567 | CONDITIONAL_ONLY_RESEARCH            | sparse_activation                       |
| threshold_0p20_nan                       |     0.0253984 |    0.195693 |               0.539683 |        0.021207  |           0.181125  |     0.85669   |              1    |                   1    |               0.612151 |               0.22673   |                           0.0871244  |           0.0351638 |           0.21434   |                      9 |       0.0435505 | CONDITIONAL_REFINEMENT_CANDIDATE     | high_missingness; weak_positive_ic_rate |
| threshold_0p20_zero                      |     0.0222292 |    0.192155 |               0.547619 |        0.0156353 |           0.181125  |     0         |              1    |                   1    |               0.632361 |               0.0825772 |                           0.0289869  |           0.0227996 |           0.0748906 |                      8 |       0.0365551 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_positive_ic_rate                   |
| threshold_0p35_zero                      |     0.022183  |    0.194231 |               0.550265 |        0.0144507 |           0.181125  |     0         |              1    |                   1    |               0.649192 |               0.0855573 |                           0.0306133  |           0.016549  |           0.0785437 |                      9 |       0.0378629 | CONDITIONAL_REFINEMENT_CANDIDATE     | none                                    |
| strict_low_extension_zero                |     0.0208351 |    0.197079 |               0.552743 |        0.0146513 |           0.113918  |     0.0258864 |              0.75 |                   0.75 |               0.630789 |               0.0654717 |                           0.0117554  |           0.035499  |           0.0523978 |                      7 |       0.0374713 | CONDITIONAL_REFINEMENT_CANDIDATE     | sparse_activation                       |
| rank_persist_10_zero                     |     0.0169591 |    0.177772 |               0.556977 |        0.0168178 |           0.648236  |     0         |              0.75 |                   0.75 |               0.42035  |               0.110056  |                           0.00669565 |           0.0482392 |           0.075759  |                      9 |       0.0271149 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_h20_ic                             |
| rank_persist_5_zero                      |     0.0127755 |    0.131718 |               0.529574 |        0.0215755 |           0.617255  |     0         |              0.75 |                   0.75 |               0.346672 |               0.0988396 |                           0.0015635  |           0.0467783 |           0.0747849 |                      7 |       0.0276927 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_h20_ic; weak_positive_ic_rate      |

## Low-Turnover Interpretation

The source signal's low turnover should not automatically be treated as tradability evidence. This pass explicitly compares turnover against active coverage and stricter activation variants. Variants with very low turnover but sparse activation are treated cautiously because low churn can come from inactivity rather than stable rank behavior.

## Distinctness From Prior Participation/Liquidity Candidate

The main orthogonality test is similarity to `participation_liquidity_state_shift_20_60`, alongside reversal and momentum baselines. Variants that improve h20 IC but converge toward the prior participation/liquidity candidate are not considered clean validation candidates.

## Advanced / Watch Items

| variant_name                             |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   turnover_proxy |   active_date_ratio |   missing_pct |   wfv_persistence |   wfv_sign_consistency |   one_window_dominance |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |   positive_state_count |   best_state_ic | status                               | review_issues                           |
|:-----------------------------------------|--------------:|------------:|-----------------------:|-----------------:|--------------------:|--------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-------------------------------------:|--------------------:|--------------------:|-----------------------:|----------------:|:-------------------------------------|:----------------------------------------|
| strict_weak_breadth_rebalance_10         |     0.0307203 |    0.259466 |               0.580537 |        0.0136189 |            0.142993 |     0.0258864 |              1    |                   1    |               0.421774 |               0.0943045 |                           0.034492   |           0.0152653 |           0.0745735 |                      9 |       0.0362962 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| strict_breadth_repair_recent_stress_zero |     0.0253616 |    0.234831 |               0.588448 |        0.022579  |            0.132984 |     0.0258864 |              0.75 |                   0.75 |               0.54362  |               0.0832269 |                           0.0383121  |           0.0129054 |           0.0704017 |                      8 |       0.0367096 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| smooth_5                                 |     0.0251565 |    0.225503 |               0.580321 |        0.0169085 |            0.232602 |     0.0268397 |              1    |                   1    |               0.486436 |               0.0918441 |                           0.00976061 |           0.0369652 |           0.0862917 |                      9 |       0.0460304 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| smooth_3                                 |     0.023818  |    0.208468 |               0.573059 |        0.0168545 |            0.206864 |     0.026363  |              1    |                   1    |               0.546792 |               0.0857794 |                           0.0179906  |           0.0322461 |           0.080824  |                      9 |       0.0425885 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| base                                     |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |            0.181125 |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| rebalance_5                              |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |            0.181125 |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| rebalance_10                             |     0.0228754 |    0.196955 |               0.563492 |        0.0164583 |            0.181125 |     0.0258864 |              1    |                   1    |               0.620385 |               0.0823959 |                           0.0288482  |           0.0235211 |           0.0750165 |                      9 |       0.0372266 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| strict_recent_stress_zero                |     0.0223458 |    0.202859 |               0.567797 |        0.0154907 |            0.169685 |     0.0258864 |              0.75 |                   0.75 |               0.441872 |               0.082636  |                           0.0268303  |           0.02313   |           0.0736801 |                      8 |       0.0366803 | CANDIDATE_FOR_CONDITIONAL_VALIDATION | none                                    |
| threshold_0p20_nan                       |     0.0253984 |    0.195693 |               0.539683 |        0.021207  |            0.181125 |     0.85669   |              1    |                   1    |               0.612151 |               0.22673   |                           0.0871244  |           0.0351638 |           0.21434   |                      9 |       0.0435505 | CONDITIONAL_REFINEMENT_CANDIDATE     | high_missingness; weak_positive_ic_rate |
| threshold_0p20_zero                      |     0.0222292 |    0.192155 |               0.547619 |        0.0156353 |            0.181125 |     0         |              1    |                   1    |               0.632361 |               0.0825772 |                           0.0289869  |           0.0227996 |           0.0748906 |                      8 |       0.0365551 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_positive_ic_rate                   |
| threshold_0p35_zero                      |     0.022183  |    0.194231 |               0.550265 |        0.0144507 |            0.181125 |     0         |              1    |                   1    |               0.649192 |               0.0855573 |                           0.0306133  |           0.016549  |           0.0785437 |                      9 |       0.0378629 | CONDITIONAL_REFINEMENT_CANDIDATE     | none                                    |
| strict_low_extension_zero                |     0.0208351 |    0.197079 |               0.552743 |        0.0146513 |            0.113918 |     0.0258864 |              0.75 |                   0.75 |               0.630789 |               0.0654717 |                           0.0117554  |           0.035499  |           0.0523978 |                      7 |       0.0374713 | CONDITIONAL_REFINEMENT_CANDIDATE     | sparse_activation                       |
| rank_persist_10_zero                     |     0.0169591 |    0.177772 |               0.556977 |        0.0168178 |            0.648236 |     0         |              0.75 |                   0.75 |               0.42035  |               0.110056  |                           0.00669565 |           0.0482392 |           0.075759  |                      9 |       0.0271149 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_h20_ic                             |
| rank_persist_5_zero                      |     0.0127755 |    0.131718 |               0.529574 |        0.0215755 |            0.617255 |     0         |              0.75 |                   0.75 |               0.346672 |               0.0988396 |                           0.0015635  |           0.0467783 |           0.0747849 |                      7 |       0.0276927 | CONDITIONAL_REFINEMENT_CANDIDATE     | weak_h20_ic; weak_positive_ic_rate      |

## Recommended Next Step

Proceed to a formal research-only conditional validation pass using a small fixed set led by `strict_weak_breadth_rebalance_10`, `strict_breadth_repair_recent_stress_zero`, `smooth_5`, `smooth_3`. Do not add new parameter variants before validation.
