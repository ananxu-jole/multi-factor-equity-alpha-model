# Participation Breadth Repair Conditional Validation

## Executive Takeaway

This formal research-only conditional validation pass evaluated `participation_breadth_repair_under_hostile_trend` using the locked four-variant shortlist from the v5 refinement pass.

Final classification: `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`.

The strongest validation candidate was `strict_weak_breadth_rebalance_10` with h20 mean IC 0.030720, positive IC rate 0.580537, turnover 0.013619, active coverage 0.142993, effective WFV-style IC IR 1.503675, persistence/sign consistency 1.00/1.00, prior participation/liquidity correlation 0.034492, and max reversal correlation 0.015265.

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or new parameter tuning was performed.

## Scope

- Source: `participation_breadth_repair_refinement_v1` artifacts.
- Fixed shortlist only: `strict_weak_breadth_rebalance_10`, `strict_breadth_repair_recent_stress_zero`, `smooth_5`, `smooth_3`.
- Validation mode: research-only, isolated artifact namespace.

## Validation Summary

| variant_name                             |   best_horizon |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   effective_test_ic_ir |   persistence |   sign_consistency |   turnover_proxy |   active_date_coverage |   active_window_coverage |   min_active_window_dates |   one_window_dominance |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr | nearby_variant_support   | sample_size_adequate   | window_concentration_ok   | strict_validation_pass   |   validation_score |
|:-----------------------------------------|---------------:|--------------:|------------:|-----------------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------------:|-------------------------:|--------------------------:|-----------------------:|------------------------:|-------------------------------------:|--------------------:|--------------------:|:-------------------------|:-----------------------|:--------------------------|:-------------------------|-------------------:|
| strict_weak_breadth_rebalance_10         |             20 |     0.0307203 |    0.259466 |               0.580537 |               1.50367  |          1    |               1    |        0.0136189 |               0.142993 |                        1 |                        50 |               0.421774 |               0.0943045 |                           0.034492   |           0.0152653 |           0.0745735 | True                     | True                   | True                      | True                     |            4.64688 |
| smooth_5                                 |             20 |     0.0251565 |    0.225503 |               0.580321 |               1.74738  |          1    |               1    |        0.0169085 |               0.232602 |                        1 |                        90 |               0.486436 |               0.0918441 |                           0.00976061 |           0.0369652 |           0.0862917 | True                     | True                   | True                      | True                     |            4.14493 |
| smooth_3                                 |             20 |     0.023818  |    0.208468 |               0.573059 |               1.37858  |          1    |               1    |        0.0168545 |               0.206864 |                        1 |                        80 |               0.546792 |               0.0857794 |                           0.0179906  |           0.0322461 |           0.080824  | True                     | True                   | True                      | True                     |            3.88057 |
| strict_breadth_repair_recent_stress_zero |             20 |     0.0253616 |    0.234831 |               0.588448 |               0.919889 |          0.75 |               0.75 |        0.022579  |               0.132984 |                        1 |                        44 |               0.54362  |               0.0832269 |                           0.0383121  |           0.0129054 |           0.0704017 | True                     | True                   | True                      | True                     |            3.7338  |

## Primary Variant Active-Coverage Check

`strict_weak_breadth_rebalance_10` active date coverage was 0.142993, with active-window coverage 1.000000 and minimum active-window dates 50. This is sparse enough to require conditional-alpha guardrails, but it is not a zero-or-one-window artifact.

## Window Concentration

| variant_name                             |   horizon |   window | start_date   | end_date   |   window_mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-----------------------------------------|----------:|---------:|:-------------|:-----------|----------------------:|-------------:|-------------------:|-----------------:|
| smooth_3                                 |        20 |        1 | 2018-10-31   | 2020-04-15 |            0.0078762  |    0.0594838 |           0.427273 |              110 |
| smooth_3                                 |        20 |        2 | 2020-04-16   | 2022-03-30 |            0.0520323  |    0.42207   |           0.736364 |              110 |
| smooth_3                                 |        20 |        3 | 2022-03-31   | 2023-10-24 |            0.0119555  |    0.15806   |           0.550459 |              109 |
| smooth_3                                 |        20 |        4 | 2023-10-25   | 2026-04-09 |            0.0232953  |    0.208346  |           0.577982 |              109 |
| smooth_5                                 |        20 |        1 | 2018-10-31   | 2020-04-15 |            0.0129953  |    0.103034  |           0.456    |              125 |
| smooth_5                                 |        20 |        2 | 2020-04-16   | 2022-03-29 |            0.0489027  |    0.385401  |           0.696    |              125 |
| smooth_5                                 |        20 |        3 | 2022-03-30   | 2023-10-23 |            0.0144415  |    0.195125  |           0.580645 |              124 |
| smooth_5                                 |        20 |        4 | 2023-10-24   | 2026-04-09 |            0.0241932  |    0.226557  |           0.58871  |              124 |
| strict_weak_breadth_rebalance_10         |        20 |        1 | 2018-10-31   | 2020-04-15 |            0.022042   |    0.15356   |           0.453333 |               75 |
| strict_weak_breadth_rebalance_10         |        20 |        2 | 2020-04-16   | 2022-02-16 |            0.0517576  |    0.403299  |           0.733333 |               75 |
| strict_weak_breadth_rebalance_10         |        20 |        3 | 2022-03-04   | 2023-10-25 |            0.00134123 |    0.0183296 |           0.5      |               74 |
| strict_weak_breadth_rebalance_10         |        20 |        4 | 2023-10-26   | 2026-04-09 |            0.0475733  |    0.437019  |           0.635135 |               74 |
| strict_breadth_repair_recent_stress_zero |        20 |        1 | 2018-10-31   | 2020-07-07 |           -0.0107645  |   -0.0891071 |           0.371429 |               70 |
| strict_breadth_repair_recent_stress_zero |        20 |        2 | 2020-07-08   | 2022-03-10 |            0.0671365  |    0.591216  |           0.797101 |               69 |
| strict_breadth_repair_recent_stress_zero |        20 |        3 | 2022-03-11   | 2023-03-16 |            0.0207196  |    0.255071  |           0.594203 |               69 |
| strict_breadth_repair_recent_stress_zero |        20 |        4 | 2023-09-08   | 2026-04-09 |            0.0248784  |    0.256127  |           0.594203 |               69 |

## Nearby Variant Support

| variant_name                             |   neighbor_count |   neighbor_mean_h20_ic |   neighbor_min_h20_ic |   neighbor_mean_positive_ic_rate | nearby_variant_support   |
|:-----------------------------------------|-----------------:|-----------------------:|----------------------:|---------------------------------:|:-------------------------|
| strict_weak_breadth_rebalance_10         |                4 |              0.0263308 |             0.0223458 |                         0.571753 | True                     |
| strict_breadth_repair_recent_stress_zero |                3 |              0.0246337 |             0.0208351 |                         0.567025 | True                     |
| smooth_5                                 |                3 |              0.0229588 |             0.022183  |                         0.562272 | True                     |
| smooth_3                                 |                3 |              0.0234204 |             0.0222292 |                         0.563811 | True                     |

## Peer Similarity Among Shortlist

| left_variant                             | right_variant                            |   value_corr |   abs_value_corr |
|:-----------------------------------------|:-----------------------------------------|-------------:|-----------------:|
| smooth_3                                 | smooth_5                                 |     0.934797 |         0.934797 |
| smooth_3                                 | strict_breadth_repair_recent_stress_zero |     0.782499 |         0.782499 |
| smooth_3                                 | strict_weak_breadth_rebalance_10         |     0.822916 |         0.822916 |
| smooth_5                                 | strict_breadth_repair_recent_stress_zero |     0.720308 |         0.720308 |
| smooth_5                                 | strict_weak_breadth_rebalance_10         |     0.767082 |         0.767082 |
| strict_breadth_repair_recent_stress_zero | strict_weak_breadth_rebalance_10         |     0.801577 |         0.801577 |

## Regime / State Attribution Snapshot

| signal_name                              | state                        |   n_dates |   mean_ic |    ic_ir |   positive_ic_rate |
|:-----------------------------------------|:-----------------------------|----------:|----------:|---------:|-------------------:|
| smooth_3                                 | WEAK_BREADTH                 |       220 | 0.0425885 | 0.354945 |           0.618182 |
| smooth_3                                 | BREADTH_REPAIR               |       312 | 0.0273889 | 0.24744  |           0.596154 |
| smooth_3                                 | LOW_EXTENSION_MARKET         |       276 | 0.023726  | 0.222774 |           0.568841 |
| smooth_3                                 | RECENT_STRESS                |       403 | 0.0231612 | 0.213596 |           0.580645 |
| smooth_3                                 | PARTICIPATION_REPAIR_HOSTILE |       233 | 0.019465  | 0.175226 |           0.553648 |
| smooth_5                                 | WEAK_BREADTH                 |       232 | 0.0460304 | 0.386347 |           0.642241 |
| smooth_5                                 | BREADTH_REPAIR               |       333 | 0.0268291 | 0.246158 |           0.591592 |
| smooth_5                                 | LOW_EXTENSION_MARKET         |       321 | 0.0253522 | 0.24173  |           0.576324 |
| smooth_5                                 | RECENT_STRESS                |       452 | 0.0243869 | 0.229074 |           0.59292  |
| smooth_5                                 | LIQUIDITY_REPAIR             |       232 | 0.0214396 | 0.170017 |           0.521552 |
| strict_breadth_repair_recent_stress_zero | WEAK_BREADTH                 |       178 | 0.0367096 | 0.306194 |           0.595506 |
| strict_breadth_repair_recent_stress_zero | BREADTH_REPAIR               |       277 | 0.0253616 | 0.234831 |           0.588448 |
| strict_breadth_repair_recent_stress_zero | RECENT_STRESS                |       277 | 0.0253616 | 0.234831 |           0.588448 |
| strict_breadth_repair_recent_stress_zero | LIQUIDITY_REPAIR             |       150 | 0.0243888 | 0.19527  |           0.526667 |
| strict_breadth_repair_recent_stress_zero | LOW_EXTENSION_MARKET         |       173 | 0.020885  | 0.222281 |           0.578035 |
| strict_weak_breadth_rebalance_10         | WEAK_BREADTH                 |       204 | 0.0362962 | 0.305143 |           0.588235 |
| strict_weak_breadth_rebalance_10         | BREADTH_REPAIR               |       242 | 0.0323364 | 0.276653 |           0.595041 |
| strict_weak_breadth_rebalance_10         | LOW_EXTENSION_MARKET         |       180 | 0.0318087 | 0.292312 |           0.566667 |
| strict_weak_breadth_rebalance_10         | LIQUIDITY_REPAIR             |       162 | 0.0314952 | 0.250163 |           0.567901 |
| strict_weak_breadth_rebalance_10         | RECENT_STRESS                |       284 | 0.0241734 | 0.210599 |           0.566901 |

## Interpretation

- The edge remains h20-oriented; shorter horizons are weaker and should not be optimized here.
- The leading strict weak-breadth rebalance variant has adequate active-window coverage for formal conditional validation, though it remains a conditional signal rather than a universal alpha.
- IC strength is not concentrated in a single WFV-style window for the leading candidate; one-window dominance is acceptable relative to the refinement pass.
- `smooth_5` and `smooth_3` are useful broader confirmation/control variants because they preserve direction, maintain low baseline similarity, and avoid stricter activation sparsity.
- Similarity to `participation_liquidity_state_shift_20_60`, reversal, and momentum baselines remains low, supporting the second-candidate thesis.
- Selection risk is still present because the shortlisted variants are related. The next stage should freeze parameters and evaluate representation semantics rather than tune further.

## Final Recommendation

Move `participation_breadth_repair_under_hostile_trend` to a research-only Conditional-Alpha integration review design step. Use `strict_weak_breadth_rebalance_10` as the primary representation, `smooth_5` and `smooth_3` as broader confirmation/control variants, and `strict_breadth_repair_recent_stress_zero` as a stress-confirmation variant. Do not promote, register, or productionize it.
