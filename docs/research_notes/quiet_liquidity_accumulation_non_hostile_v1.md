# Quiet Liquidity Accumulation Non-Hostile v1

## Executive Takeaway

This research-only run tested one simple formulation of `quiet_liquidity_accumulation_non_hostile` under the isolated run namespace `quiet_liquidity_accumulation_non_hostile_v1`.

The formulation tests whether quiet dollar-volume accumulation with contained impact during non-hostile states predicts forward returns without requiring breakout behavior, panic repair, stress activation, or price-rank momentum.

Final classification: `REJECT_RESEARCH`
Primary review issues: `weak_primary_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_quiet_state_support; hostile_state_dependence_risk`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v3 concepts was performed.

## Source Context

- Expansion v3 design screen: `docs/research_notes/track_b_expansion_v3_design_screening.md`
- Calm regime relative stability v1: `docs/research_notes/calm_regime_relative_stability_10_v1.md`
- Calm regime relative stability refinement: `docs/research_notes/calm_regime_relative_stability_10_refinement.md`
- Neutral accumulation without breakout v1: `docs/research_notes/neutral_accumulation_without_breakout_v1.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Quiet liquidity accumulation during non-hostile states may identify names where participation improves without stress repair, panic volume, or price extension. |
| Quiet liquidity accumulation logic | The signal combines moderate dollar-volume improvement, short-vs-medium volume confirmation, low turnover shock, range/impact containment, supportive close location, orderly path behavior, and neutral price extension. |
| Non-hostile regime filter | The market gate excludes recent volatility spike, panic liquidity stress, drawdown acceleration, hostile benchmark trend, and weak breadth. |
| No-breakout / no-panic logic | Asset-level breakout flags veto names near 20-day highs or top 10/20-day return ranks; market-level panic/stress states are excluded by the non-hostile gate. |
| Difference from hostile liquidity repair | It does not require weak breadth, panic liquidity stress, drawdown, or post-stress repair; it explicitly tracks similarity to the existing liquidity repair inventory candidate and a hostile liquidity repair proxy. |
| Difference from momentum/reversal | The signal neutralizes h5/h10/h20/h60 return ranks and 20-day reversal rank, while neutral extension penalizes price-rank extremes. |
| Difference from current inventory | It is a non-hostile, h5-h10 intended liquidity-quality mechanism rather than hostile/stress h20 repair or post-stress stabilization. |
| Expected activation semantics | Non-hostile calm/normal dispersion state with quiet liquidity accumulation and no breakout pressure. |
| Expected horizon | h5-h10 primary; h20 diagnostic for inventory comparability. |
| Expected turnover | Medium after fixed five-day rebalance control. |
| Expected active coverage | Medium; sparse or always-on behavior is a review issue. |

## Candidate Registry

| signal_name                              | family                       | run_id                                      | research_status                    | mechanism_thesis                                                                      | state_transition_logic                                                                                                                                 | differs_from_inventory                                                                     | differs_from_reversal_momentum                                                                       | expected_activation_state                | expected_horizon               | expected_turnover_profile   | expected_active_coverage   |
|:-----------------------------------------|:-----------------------------|:--------------------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:-----------------------------------------|:-------------------------------|:----------------------------|:---------------------------|
| quiet_liquidity_accumulation_non_hostile | quiet_liquidity_accumulation | quiet_liquidity_accumulation_non_hostile_v1 | TRACK_B_EXPANSION_V3_RESEARCH_ONLY | Quiet non-hostile liquidity accumulation with no breakout or panic repair dependency. | Non-hostile market state plus moderate dollar-volume accumulation, impact containment, orderly path behavior, neutral extension, and no-breakout veto. | Targets non-hostile liquidity quality rather than hostile/stress h20 participation repair. | Neutralizes price-rank and reversal exposures and penalizes extension rather than fading or chasing. | NON_HOSTILE_QUIET_LIQUIDITY_ACCUMULATION | h5-h10 primary; h20 diagnostic | medium                      | medium                     |

## Component Diagnostics

| component                    |   finite_pct |   mean_abs |
|:-----------------------------|-------------:|-----------:|
| quiet_dv_accumulation        |     0.969391 | 0.132314   |
| liquidity_impact_containment |     0.969021 | 0.128388   |
| close_support                |     0.98702  | 0.501034   |
| path_orderliness             |     0.985002 | 0.497504   |
| neutral_extension            |     0.978801 | 0.284436   |
| no_breakout_gate             |     1        | 0.631196   |
| quiet_liquidity_gate         |     1        | 0.117255   |
| liquidity_quality            |     0.967963 | 0.00177168 |
| final_signal                 |     0.959386 | 0.0621008  |

## Structural Quality

| signal_name                              |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-----------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| quiet_liquidity_accumulation_non_hostile |   2098 |       478 |     0.0406145 |     0.959386 |        0.971401 |               0.959386 |           0 |        0.0201034 |              0 |       0.683558 |               0.12208 |            245 |            0.116778 |                       60 |               0.988344 |

## Multi-Horizon IC

| signal_name                              |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:-----------------------------------------|----------:|------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| quiet_liquidity_accumulation_non_hostile |         1 | -0.00166312 |    0.00166312 | -0.0231111 |   0.0231111 |           0.506122 |       245 |              5 | False             |
| quiet_liquidity_accumulation_non_hostile |         5 | -0.00486592 |    0.00486592 | -0.0716149 |   0.0716149 |           0.473469 |       245 |              5 | True              |
| quiet_liquidity_accumulation_non_hostile |        10 | -0.00284053 |    0.00284053 | -0.0490492 |   0.0490492 |           0.481633 |       245 |              5 | False             |
| quiet_liquidity_accumulation_non_hostile |        20 |  0.00327795 |    0.00327795 |  0.051964  |   0.051964  |           0.510204 |       245 |              5 | False             |

## h5 / h10 / h20 Behavior

| signal_name                              |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:-----------------------------------------|----------:|------------:|--------------:|-----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| quiet_liquidity_accumulation_non_hostile |         5 | -0.00486592 |    0.00486592 | -0.0716149 |   0.0716149 |           0.473469 |       245 |              5 | True              |
| quiet_liquidity_accumulation_non_hostile |        10 | -0.00284053 |    0.00284053 | -0.0490492 |   0.0490492 |           0.481633 |       245 |              5 | False             |
| quiet_liquidity_accumulation_non_hostile |        20 |  0.00327795 |    0.00327795 |  0.051964  |   0.051964  |           0.510204 |       245 |              5 | False             |

## WFV-Style Diagnostics

| signal_name                              |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-----------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| quiet_liquidity_accumulation_non_hostile |         5 |           4 |              -0.00472448 |              -0.198122 |          0.25 |               0.75 |               0.528157 |

## WFV Window Detail

| signal_name                              |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-----------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| quiet_liquidity_accumulation_non_hostile |         5 |        1 | 2018-06-25   | 2020-01-07 |    -0.0393763  |   -0.690207  |           0.241935 |               62 |
| quiet_liquidity_accumulation_non_hostile |         5 |        2 | 2020-01-08   | 2021-07-20 |    -0.00612107 |   -0.114018  |           0.508197 |               61 |
| quiet_liquidity_accumulation_non_hostile |         5 |        3 | 2021-07-21   | 2024-07-23 |     0.0278282  |    0.391844  |           0.688525 |               61 |
| quiet_liquidity_accumulation_non_hostile |         5 |        4 | 2024-07-24   | 2026-01-29 |    -0.00122867 |   -0.0173516 |           0.459016 |               61 |

## Baseline And Inventory Similarity

| signal_name                              | top_comparison                     |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   raw_breakout_continuation_20_corr |   quiet_liquidity_accumulation_proxy_corr |   hostile_liquidity_repair_proxy_corr |   max_price_momentum_corr |   max_breakout_continuation_corr |   max_liquidity_repair_corr |
|:-----------------------------------------|:-----------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------------:|------------------------------------------:|--------------------------------------:|--------------------------:|---------------------------------:|----------------------------:|
| quiet_liquidity_accumulation_non_hostile | quiet_liquidity_accumulation_proxy |                0.104167 |                 0.00230954 |              0.000962022 |                 9.89484e-09 |           0.00230954 |           0.0014013 |          0.00321274 |                    0.0290049 |                     0.0343082 |                    0.00140131 |                    0.00321274 |                           0.0267981 |                                  0.104167 |                           3.74708e-05 |                 0.0343082 |                        0.0267981 |                  0.00230954 |

## Calm / Neutral Vs Hostile / Stress Attribution

| signal_name                              |   horizon | state                              |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:-----------------------------------------|----------:|:-----------------------------------|----------:|------------:|------------:|-------------------:|
| quiet_liquidity_accumulation_non_hostile |         5 | recovery_phase                     |         1 |  0.0934065  | nan         |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | volatility_spike                   |         1 |  0.0689188  | nan         |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | panic_liquidity_stress             |         1 |  0.0689188  | nan         |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | weak_breadth                       |        10 |  0.0288228  |   0.696498  |           0.8      |
| quiet_liquidity_accumulation_non_hostile |         5 | HOSTILE_OR_STRESS                  |        16 |  0.00996908 |   0.176993  |           0.6875   |
| quiet_liquidity_accumulation_non_hostile |         5 | QUIET_LIQUIDITY_ACCUMULATION_STATE |       160 | -0.00195916 |  -0.0272501 |           0.475    |
| quiet_liquidity_accumulation_non_hostile |         5 | NORMAL_DISPERSION                  |       212 | -0.00442235 |  -0.0638476 |           0.471698 |
| quiet_liquidity_accumulation_non_hostile |         5 | NON_HOSTILE_LIQUIDITY_STATE        |       229 | -0.00590242 |  -0.0860861 |           0.458515 |
| quiet_liquidity_accumulation_non_hostile |         5 | CONSTRUCTIVE_NOT_EUPHORIC          |       216 | -0.0070223  |  -0.103612  |           0.444444 |
| quiet_liquidity_accumulation_non_hostile |         5 | CALM_NORMAL_VOL                    |       215 | -0.00712611 |  -0.102962  |           0.455814 |
| quiet_liquidity_accumulation_non_hostile |         5 | drawdown_acceleration              |         7 | -0.00738116 |  -0.144211  |           0.571429 |
| quiet_liquidity_accumulation_non_hostile |         5 | high_dispersion_rotation           |        17 | -0.0243598  |  -0.435405  |           0.294118 |
| quiet_liquidity_accumulation_non_hostile |         5 | BREAKOUT_PRESSURE                  |        37 | -0.0325603  |  -0.63441   |           0.324324 |
| quiet_liquidity_accumulation_non_hostile |         5 | trend_transition                   |         9 | -0.0591914  |  -1.33231   |           0.111111 |

## Stress / Regime Attribution

| signal_name                              |   horizon | state                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-----------------------------------------|----------:|:-------------------------|----------:|------------:|-----------:|-------------------:|
| quiet_liquidity_accumulation_non_hostile |         5 | recovery_phase           |         1 |  0.0934065  | nan        |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | volatility_spike         |         1 |  0.0689188  | nan        |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | panic_liquidity_stress   |         1 |  0.0689188  | nan        |           1        |
| quiet_liquidity_accumulation_non_hostile |         5 | weak_breadth             |        10 |  0.0288228  |   0.696498 |           0.8      |
| quiet_liquidity_accumulation_non_hostile |         5 | drawdown_acceleration    |         7 | -0.00738116 |  -0.144211 |           0.571429 |
| quiet_liquidity_accumulation_non_hostile |         5 | high_dispersion_rotation |        17 | -0.0243598  |  -0.435405 |           0.294118 |
| quiet_liquidity_accumulation_non_hostile |         5 | trend_transition         |         9 | -0.0591914  |  -1.33231  |           0.111111 |

## Sample-Size Sanity

| state                              |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:-----------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| NON_HOSTILE_LIQUIDITY_STATE        |           834 |          0.397521  |                           229 |                   0.109152    |
| QUIET_LIQUIDITY_ACCUMULATION_STATE |           246 |          0.117255  |                           160 |                   0.0762631   |
| CALM_NORMAL_VOL                    |           512 |          0.244042  |                           215 |                   0.102479    |
| NORMAL_DISPERSION                  |           631 |          0.300763  |                           212 |                   0.101049    |
| CONSTRUCTIVE_NOT_EUPHORIC          |           655 |          0.312202  |                           216 |                   0.102955    |
| BREAKOUT_PRESSURE                  |           514 |          0.244995  |                            37 |                   0.0176358   |
| HOSTILE_OR_STRESS                  |          1264 |          0.602479  |                            16 |                   0.00762631  |
| drawdown_acceleration              |           375 |          0.178742  |                             7 |                   0.00333651  |
| volatility_spike                   |           404 |          0.192564  |                             1 |                   0.000476644 |
| panic_liquidity_stress             |           187 |          0.0891325 |                             1 |                   0.000476644 |
| trend_transition                   |           580 |          0.276454  |                             9 |                   0.0042898   |
| recovery_phase                     |           196 |          0.0934223 |                             1 |                   0.000476644 |
| high_dispersion_rotation           |           584 |          0.27836   |                            17 |                   0.00810296  |
| weak_breadth                       |           508 |          0.242135  |                            10 |                   0.00476644  |
| SIGNAL_ACTIVE                      |           245 |          0.116778  |                           245 |                   0.116778    |

## Candidate Decision

| signal_name                              | family                       |   best_horizon |     mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_liquidity_repair_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_breakout_continuation_corr |   quiet_liquidity_accumulation_proxy_corr |   hostile_liquidity_repair_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_quiet_state_count |   best_quiet_state_ic |   best_hostile_state_ic | status          | review_issues                                                                                                         |
|:-----------------------------------------|:-----------------------------|---------------:|------------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|-----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|----------------------------:|--------------------:|--------------------:|--------------------------:|---------------------------------:|------------------------------------------:|--------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|-----------------------------:|----------------------:|------------------------:|:----------------|:----------------------------------------------------------------------------------------------------------------------|
| quiet_liquidity_accumulation_non_hostile | quiet_liquidity_accumulation |              5 | -0.00486592 |  -0.00486592 |              0.473469 |   -0.00284053 |               0.481633 |    0.00327795 |               0.510204 | -0.0716149 |           0.473469 |        0.0201034 |     0.0406145 |            0.116778 |                0.104167 |           0.00230954 |                  0.00230954 |           0.0014013 |          0.00321274 |                 0.0343082 |                        0.0267981 |                                  0.104167 |                           3.74708e-05 |                 0.00230954 |              0.000962022 |                 9.89484e-09 |              0.25 |                   0.75 |              -0.198122 |                            0 |           -0.00195916 |               0.0689188 | REJECT_RESEARCH | weak_primary_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_quiet_state_support; hostile_state_dependence_risk |

## Specific Diagnostic Answers

- Genuinely quiet liquidity accumulation: assessed through `QUIET_LIQUIDITY_ACCUMULATION_STATE`; positive quiet-state count was `0` and best quiet-state IC was `-0.001959`.
- Hostile liquidity repair risk: max liquidity-repair correlation was `0.002310`; inventory liquidity correlation was `0.002310`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.034308` / `0.001401`.
- Breakout continuation risk: max breakout-continuation correlation was `0.026798`.
- Inventory overlap risk: max inventory correlation was `0.002310`.
- Sparse or broad activation risk: active date ratio was `0.116778`.
- Turnover risk: turnover proxy was `0.020103`.
- Directional stability: WFV-style persistence/sign consistency were `0.250000` / `0.750000`.
- h5/h10/h20 profile: h5 mean IC was `-0.004866`, h10 mean IC was `-0.002841`, and h20 mean IC was `0.003278`.

## Recommended Next Step

`quiet_liquidity_accumulation_non_hostile` should be rejected in this formulation before moving to any other Expansion v3 concept.
