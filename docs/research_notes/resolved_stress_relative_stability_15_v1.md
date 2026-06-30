# Resolved Stress Relative Stability 15 v1

## Executive Takeaway

This research-only run tested one simple formulation of `resolved_stress_relative_stability_15` under the isolated run namespace `resolved_stress_relative_stability_15_v1`.

The formulation tests whether stable cross-sectional behavior after stress normalization predicts medium-horizon forward returns without becoming active repair, raw continuation, low-volatility beta, momentum, or reversal.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `intended_h15_not_supported; weak_wfv_persistence; weak_wfv_sign_consistency`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v4 concepts was performed.

## Source Context

- Expansion v4 design screen: `docs/research_notes/track_b_expansion_v4_design_screening.md`
- Post-repair continuation v1: `docs/research_notes/post_repair_continuation_after_breadth_recovery_v1.md`
- Calm regime relative stability v1: `docs/research_notes/calm_regime_relative_stability_10_v1.md`
- Calm regime relative stability refinement: `docs/research_notes/calm_regime_relative_stability_10_refinement.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | After stress has normalized, stocks with stable relative ranks, orderly residual volatility, and contained range behavior may preserve a repair/stabilization edge through persistence rather than continuation. |
| Resolved-stress logic | Requires volatility spike, panic/liquidity stress, or drawdown acceleration to have been present recently while current stress, hostile trend, and weak breadth are inactive. |
| Relative stability definition | Combines h10/h15/h20 residual rank stability, residual volatility stability, range orderliness, path orderliness, and neutral price extension. |
| Post-normalization stabilization logic | Requires benchmark volatility, dispersion, and breadth to have normalized after stress, with an explicit state attribution check for post-normalization stabilization. |
| Difference from active hostile-state repair | The candidate is gated off during active stress, hostile trend, or weak breadth and only activates after stress has cleared. |
| Difference from raw continuation/momentum | Return-rank exposure is neutralized at h5/h10/h15/h20/h60 and extreme extension is penalized rather than rewarded. |
| Difference from current inventory | Current inventory is active repair/stress h20-centered; this tests resolved-stress stability persistence with h15 as the intended horizon. |
| Expected activation semantics | Recent stress, current stress cleared, volatility/dispersion normalized, breadth no longer weak, stable relative behavior. |
| Expected horizon | h15 primary; h10 and h20 diagnostic. |
| Expected turnover | Low after fixed 15-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparse or overly broad activation is a review issue. |

## Candidate Registry

| signal_name                           | family                             | run_id                                   | research_status                    | mechanism_thesis                                                     | state_transition_logic                                                                                                                    | differs_from_inventory                                                         | differs_from_reversal_momentum                                                | expected_activation_state   | expected_horizon                | expected_turnover_profile   | expected_active_coverage   |
|:--------------------------------------|:-----------------------------------|:-----------------------------------------|:-----------------------------------|:---------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|:------------------------------------------------------------------------------|:----------------------------|:--------------------------------|:----------------------------|:---------------------------|
| resolved_stress_relative_stability_15 | resolved_stress_relative_stability | resolved_stress_relative_stability_15_v1 | TRACK_B_EXPANSION_V4_RESEARCH_ONLY | Relative stability after stress normalization and stress resolution. | Recent stress present, current stress cleared, volatility/dispersion normalized, breadth no longer weak, stable cross-sectional behavior. | Activates after stress clears rather than during active hostile/stress repair. | Neutralizes return-rank and reversal exposures and penalizes price extension. | RESOLVED_STRESS_STATE       | h15 primary; h10/h20 diagnostic | low                         | medium                     |

## Component Diagnostics

| component               |   finite_pct |   mean_abs |
|:------------------------|-------------:|-----------:|
| rank_stability_10       |     0.980712 | 0.498503   |
| rank_stability_15       |     0.976901 | 0.498542   |
| rank_stability_20       |     0.97309  | 0.498589   |
| relative_rank_stability |     0.973086 | 0.186058   |
| residual_vol_stability  |     0.977943 | 0.499126   |
| range_orderliness       |     0.969149 | 0.247826   |
| path_orderliness        |     0.983574 | 0.497391   |
| no_extension            |     0.978801 | 0.284436   |
| resolved_stress_gate    |     1        | 0.137274   |
| relative_stability      |     0.967338 | 0.00570896 |
| final_signal            |     0.9596   | 0.0719753  |

## Structural Quality

| signal_name                           |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| resolved_stress_relative_stability_15 |   2098 |       478 |     0.0404001 |       0.9596 |        0.971401 |                 0.9596 |           0 |       0.00876796 |              0 |       0.636668 |              0.141665 |            285 |            0.135844 |                       32 |                0.98954 |

## Multi-Horizon IC

| signal_name                           |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:--------------------------------------|----------:|------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| resolved_stress_relative_stability_15 |         1 | -0.00289673 |    0.00289673 | -0.0313164 |   0.0313164 |           0.484211 |       285 |             10 | False             |
| resolved_stress_relative_stability_15 |         5 |  0.00331986 |    0.00331986 |  0.0404383 |   0.0404383 |           0.508772 |       285 |             10 | False             |
| resolved_stress_relative_stability_15 |        10 |  0.00883113 |    0.00883113 |  0.121823  |   0.121823  |           0.550877 |       285 |             10 | True              |
| resolved_stress_relative_stability_15 |        15 |  0.00220717 |    0.00220717 |  0.0313254 |   0.0313254 |           0.533333 |       285 |             10 | False             |
| resolved_stress_relative_stability_15 |        20 | -0.00140001 |    0.00140001 | -0.0204362 |   0.0204362 |           0.470175 |       285 |             10 | False             |

## h5 / h10 / h15 / h20 Behavior

| signal_name                           |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:--------------------------------------|----------:|------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| resolved_stress_relative_stability_15 |         5 |  0.00331986 |    0.00331986 |  0.0404383 |   0.0404383 |           0.508772 |       285 |             10 | False             |
| resolved_stress_relative_stability_15 |        10 |  0.00883113 |    0.00883113 |  0.121823  |   0.121823  |           0.550877 |       285 |             10 | True              |
| resolved_stress_relative_stability_15 |        15 |  0.00220717 |    0.00220717 |  0.0313254 |   0.0313254 |           0.533333 |       285 |             10 | False             |
| resolved_stress_relative_stability_15 |        20 | -0.00140001 |    0.00140001 | -0.0204362 |   0.0204362 |           0.470175 |       285 |             10 | False             |

## WFV-Style Diagnostics

| signal_name                           |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| resolved_stress_relative_stability_15 |        10 |           4 |               0.00886519 |               0.785417 |           0.5 |                0.5 |               0.513871 |

## WFV Window Detail

| signal_name                           |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:--------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| resolved_stress_relative_stability_15 |        10 |        1 | 2018-06-25   | 2020-11-25 |   -0.000842561 |   -0.0101371 |           0.513889 |               72 |
| resolved_stress_relative_stability_15 |        10 |        2 | 2020-11-27   | 2022-09-06 |    0.0171163   |    0.220491  |           0.56338  |               71 |
| resolved_stress_relative_stability_15 |        10 |        3 | 2022-09-07   | 2024-07-09 |   -0.0035637   |   -0.0568414 |           0.464789 |               71 |
| resolved_stress_relative_stability_15 |        10 |        4 | 2024-07-10   | 2026-02-12 |    0.0227507   |    0.378088  |           0.661972 |               71 |

## Baseline And Inventory Similarity

| signal_name                           | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   simple_rank_stability_15_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   simple_range_stability_corr |   raw_resolved_stability_proxy_corr |   active_breadth_repair_proxy_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |   max_breadth_repair_corr |
|:--------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|------------------------------:|------------------------------------:|-----------------------------------:|--------------------------:|--------------------------:|----------------------------:|--------------------------:|
| resolved_stress_relative_stability_15 | v2_vol_compression_range_expansion_20_60 |                 0.07467 |                  0.0134537 |              0.000583268 |                 1.79006e-08 |            0.0134537 |           0.0043853 |          0.00190731 |                   0.00278686 |                    0.00104439 |                    0.00264953 |                    0.00335402 |                    0.00190731 |                       0.0408637 |                       0.0497148 |                                0.0452665 |                     0.0437632 |                           0.0104103 |                         0.00353276 |                0.00335402 |                 0.0497148 |                   0.0437632 |                0.00353276 |

## Hostile / Stress Vs Resolved / Neutral Attribution

| signal_name                           |   horizon | state                             |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:----------------------------------|----------:|------------:|-----------:|-------------------:|
| resolved_stress_relative_stability_15 |        10 | BREADTH_NOT_WEAK_POST_STRESS      |       197 |  0.0115045  |  0.151636  |           0.568528 |
| resolved_stress_relative_stability_15 |        10 | ACTIVE_HOSTILE_OR_STRESS          |        59 |  0.0112868  |  0.180732  |           0.59322  |
| resolved_stress_relative_stability_15 |        10 | HOSTILE_OR_STRESS                 |        59 |  0.0112868  |  0.180732  |           0.59322  |
| resolved_stress_relative_stability_15 |        10 | STRESS_RECENTLY_PRESENT           |       265 |  0.0107015  |  0.147251  |           0.566038 |
| resolved_stress_relative_stability_15 |        10 | DISPERSION_NORMALIZED             |       173 |  0.0103224  |  0.140717  |           0.572254 |
| resolved_stress_relative_stability_15 |        10 | VOL_NORMALIZED                    |       192 |  0.0102253  |  0.133247  |           0.5625   |
| resolved_stress_relative_stability_15 |        10 | RESOLVED_STRESS_WITH_STABILITY    |       154 |  0.00913689 |  0.122924  |           0.577922 |
| resolved_stress_relative_stability_15 |        10 | RESOLVED_STRESS_STATE             |       154 |  0.00913689 |  0.122924  |           0.577922 |
| resolved_stress_relative_stability_15 |        10 | STRESS_CLEARED                    |       226 |  0.00819003 |  0.109378  |           0.539823 |
| resolved_stress_relative_stability_15 |        10 | drawdown_acceleration             |        23 |  0.00741029 |  0.116245  |           0.565217 |
| resolved_stress_relative_stability_15 |        10 | high_dispersion_rotation          |        43 |  0.00581285 |  0.0733548 |           0.44186  |
| resolved_stress_relative_stability_15 |        10 | weak_breadth                      |        44 |  0.00573082 |  0.0956519 |           0.568182 |
| resolved_stress_relative_stability_15 |        10 | POST_NORMALIZATION_STABILIZATION  |        91 |  0.00435623 |  0.0695955 |           0.604396 |
| resolved_stress_relative_stability_15 |        10 | ORDERLY_CROSS_SECTION_POST_STRESS |        91 |  0.00435623 |  0.0695955 |           0.604396 |
| resolved_stress_relative_stability_15 |        10 | trend_transition                  |        29 | -0.00751889 | -0.145949  |           0.482759 |
| resolved_stress_relative_stability_15 |        10 | recovery_phase                    |         7 | -0.0121708  | -0.282771  |           0.571429 |

## Stress / Regime Attribution

| signal_name                           |   horizon | state                    |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:-------------------------|----------:|------------:|------------:|-------------------:|
| resolved_stress_relative_stability_15 |        10 | drawdown_acceleration    |        23 |  0.00741029 |   0.116245  |           0.565217 |
| resolved_stress_relative_stability_15 |        10 | high_dispersion_rotation |        43 |  0.00581285 |   0.0733548 |           0.44186  |
| resolved_stress_relative_stability_15 |        10 | weak_breadth             |        44 |  0.00573082 |   0.0956519 |           0.568182 |
| resolved_stress_relative_stability_15 |        10 | trend_transition         |        29 | -0.00751889 |  -0.145949  |           0.482759 |
| resolved_stress_relative_stability_15 |        10 | recovery_phase           |         7 | -0.0121708  |  -0.282771  |           0.571429 |
| resolved_stress_relative_stability_15 |        10 | panic_liquidity_stress   |         1 | -0.0535929  | nan         |           0        |
| resolved_stress_relative_stability_15 |        10 | volatility_spike         |         3 | -0.0761927  |  -3.7031    |           0        |

## Sample-Size Sanity

| state                             |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:----------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| ACTIVE_HOSTILE_OR_STRESS          |          1264 |          0.602479  |                            59 |                   0.028122    |
| RESOLVED_STRESS_STATE             |           288 |          0.137274  |                           154 |                   0.0734032   |
| RESOLVED_STRESS_WITH_STABILITY    |           288 |          0.137274  |                           154 |                   0.0734032   |
| POST_NORMALIZATION_STABILIZATION  |           180 |          0.085796  |                            91 |                   0.0433746   |
| STRESS_RECENTLY_PRESENT           |          1715 |          0.817445  |                           265 |                   0.126311    |
| STRESS_CLEARED                    |           834 |          0.397521  |                           226 |                   0.107722    |
| VOL_NORMALIZED                    |           433 |          0.206387  |                           192 |                   0.0915157   |
| DISPERSION_NORMALIZED             |           359 |          0.171115  |                           173 |                   0.0824595   |
| BREADTH_NOT_WEAK_POST_STRESS      |           446 |          0.212583  |                           197 |                   0.093899    |
| ORDERLY_CROSS_SECTION_POST_STRESS |           180 |          0.085796  |                            91 |                   0.0433746   |
| HOSTILE_OR_STRESS                 |          1264 |          0.602479  |                            59 |                   0.028122    |
| drawdown_acceleration             |           375 |          0.178742  |                            23 |                   0.0109628   |
| volatility_spike                  |           404 |          0.192564  |                             3 |                   0.00142993  |
| panic_liquidity_stress            |           187 |          0.0891325 |                             1 |                   0.000476644 |
| trend_transition                  |           580 |          0.276454  |                            29 |                   0.0138227   |
| recovery_phase                    |           196 |          0.0934223 |                             7 |                   0.00333651  |
| high_dispersion_rotation          |           584 |          0.27836   |                            43 |                   0.0204957   |
| weak_breadth                      |           508 |          0.242135  |                            44 |                   0.0209724   |
| SIGNAL_ACTIVE                     |           285 |          0.135844  |                           285 |                   0.135844    |

## Candidate Decision

| signal_name                           | family                             |   best_horizon |    mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |    ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_breadth_repair_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   max_simple_stability_corr |   simple_rank_stability_15_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   raw_resolved_stability_proxy_corr |   active_breadth_repair_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_resolved_state_count |   best_resolved_state_ic |   best_active_stress_state_ic | status                    | review_issues                                                               |
|:--------------------------------------|:-----------------------------------|---------------:|-----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|---------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|----------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|------------------------------------:|-----------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|--------------------------------:|-------------------------:|------------------------------:|:--------------------------|:----------------------------------------------------------------------------|
| resolved_stress_relative_stability_15 | resolved_stress_relative_stability |             10 | 0.00883113 |   0.00331986 |              0.508772 |    0.00883113 |               0.550877 |    0.00220717 |               0.533333 |   -0.00140001 |               0.470175 | 0.121823 |           0.550877 |       0.00876796 |     0.0404001 |            0.135844 |                 0.07467 |            0.0134537 |                0.00353276 |           0.0043853 |          0.00190731 |                0.00335402 |                 0.0497148 |                   0.0437632 |                       0.0408637 |                       0.0497148 |                                0.0452665 |                           0.0104103 |                         0.00353276 |                  0.0134537 |              0.000583268 |                 1.79006e-08 |               0.5 |                    0.5 |               0.785417 |                               7 |                0.0115045 |                     0.0112868 | CONDITIONAL_ONLY_RESEARCH | intended_h15_not_supported; weak_wfv_persistence; weak_wfv_sign_consistency |

## Specific Diagnostic Answers

- Genuinely resolved-stress relative stability: positive resolved-state count was `7` and best resolved-state IC was `0.011505`.
- Active hostile-state repair risk: best active stress-state IC was `0.011287` and max breadth-repair correlation was `0.003533`.
- Low-volatility beta risk: max low-volatility correlation was `0.049715`; low-vol and residual-low-vol correlations were `0.049715` / `0.045266`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.003354` / `0.004385`.
- Simple stability duplication risk: max simple-stability correlation was `0.043763`.
- Inventory overlap risk: max inventory correlation was `0.013454`.
- Sparse or broad activation risk: active date ratio was `0.135844`.
- Turnover risk: turnover proxy was `0.008768`.
- Directional stability: WFV-style persistence/sign consistency were `0.500000` / `0.500000`.
- h5/h10/h15/h20 profile: h5 `0.003320`, h10 `0.008831`, h15 `0.002207`, h20 `-0.001400`.

## Recommended Next Step

`resolved_stress_relative_stability_15` should remain conditional-only research evidence until h15 support and WFV stability improve.
