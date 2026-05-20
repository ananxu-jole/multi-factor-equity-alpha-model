# Neutral Accumulation Without Breakout v1

## Executive Takeaway

This research-only run tested one simple formulation of `neutral_accumulation_without_breakout` under the isolated run namespace `neutral_accumulation_without_breakout_v1`.

The formulation was designed to test whether quiet accumulation in neutral, non-hostile market states can add a calmer-state Conditional Alpha Inventory dimension without collapsing into breakout continuation, momentum, reversal, or existing participation/liquidity repair.

Final classification: `REJECT_RESEARCH`
Primary review issues: `weak_primary_ic; weak_wfv_persistence; weak_neutral_state_support; hostile_state_dependence_risk`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v3 concepts was performed.

## Source Context

- Expansion v3 design screen: `docs/research_notes/track_b_expansion_v3_design_screening.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Some names may accumulate quietly during neutral market states before visible breakout or stress repair. Controlled participation, stable closes, contained range, and neutral price rank can indicate accumulation without price-rank chase. |
| Neutral-state accumulation logic | The signal requires non-hostile, non-panic, non-weak-breadth market context, controlled dollar-volume participation, supportive close location, range containment, path orderliness, and neutral short/medium price rank. |
| No-breakout filter | Candidate exposure is penalized or vetoed when the name is near its recent 20-day high or sits in the top cross-sectional ranks of 10-day or 20-day return. |
| Difference from breakout continuation | It does not reward being near a breakout high; that condition is a veto. It also neutralizes short and medium price-rank exposure. |
| Difference from reversal/momentum | It does not buy losers, fade prior returns, or chase winners. The price-rank component is intentionally centered near neutral. |
| Difference from current inventory | It activates in neutral/calm states rather than hostile trend, weak breadth, drawdown, panic/liquidity stress, or post-stress stabilization. |
| Expected activation semantics | Neutral market state with quiet accumulation quality and no breakout risk. |
| Expected horizon | h5-h10 primary; h20 monitored for inventory comparability. |
| Expected turnover | Low to medium after fixed five-day rebalance control. |
| Expected active coverage | Medium; too sparse or always-on behavior is a review issue. |

## Candidate Registry

| signal_name                           | family                     | run_id                                   | research_status                    | mechanism_thesis                                                | state_transition_logic                                                                                                                       | differs_from_inventory                                                  | differs_from_reversal_momentum                                                                  | expected_activation_state                   | expected_horizon               | expected_turnover_profile   | expected_active_coverage   |
|:--------------------------------------|:---------------------------|:-----------------------------------------|:-----------------------------------|:----------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------|:--------------------------------------------|:-------------------------------|:----------------------------|:---------------------------|
| neutral_accumulation_without_breakout | neutral_state_accumulation | neutral_accumulation_without_breakout_v1 | TRACK_B_EXPANSION_V3_RESEARCH_ONLY | Neutral-state quiet accumulation with no breakout continuation. | Non-hostile non-stress market state plus controlled participation, stable closes, contained range, neutral price rank, and no-breakout veto. | Targets neutral/calm accumulation instead of hostile/stress h20 repair. | Neutralizes price rank and vetoes breakout/extension rather than fading or chasing price moves. | NEUTRAL_MARKET_STATE_AND_QUIET_ACCUMULATION | h5-h10 primary; h20 diagnostic | low_to_medium               | medium                     |

## Component Diagnostics

| component                |   finite_pct |   mean_abs |
|:-------------------------|-------------:|-----------:|
| controlled_participation |     0.969391 | 0.249873   |
| close_support            |     0.98702  | 0.501034   |
| range_containment        |     0.969149 | 0.247826   |
| path_orderliness         |     0.985002 | 0.497504   |
| neutral_price_rank       |     0.978801 | 0.284436   |
| no_breakout_score        |     0.982614 | 0.499363   |
| no_breakout_gate         |     1        | 0.631196   |
| neutral_gate             |     1        | 0.397521   |
| accumulation_quality     |     0.967964 | 0.00199596 |
| final_signal             |     0.959386 | 0.194615   |

## Structural Quality

| signal_name                           |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| neutral_accumulation_without_breakout |     0.0406145 |     0.959386 |        0.971401 |        0.0490795 |       0.531802 |            0.376549 |                       46 |               0.986071 |

## Multi-Horizon IC

| signal_name                           |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| neutral_accumulation_without_breakout |         1 | -0.000638135 |   0.000638135 | -0.00895299 |           0.510127 |       790 | False             |
| neutral_accumulation_without_breakout |         5 | -0.00496254  |   0.00496254  | -0.0694879  |           0.488608 |       790 | True              |
| neutral_accumulation_without_breakout |        10 | -0.000486772 |   0.000486772 | -0.00688269 |           0.520253 |       790 | False             |
| neutral_accumulation_without_breakout |        20 |  0.00064444  |   0.00064444  |  0.00884614 |           0.501266 |       790 | False             |

## h10 Behavior

| signal_name                           |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates |
|:--------------------------------------|-------------:|--------------:|------------:|-------------------:|----------:|
| neutral_accumulation_without_breakout | -0.000486772 |   0.000486772 | -0.00688269 |           0.520253 |       790 |

## h20 Behavior

| signal_name                           |    mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:--------------------------------------|-----------:|--------------:|-----------:|-------------------:|----------:|
| neutral_accumulation_without_breakout | 0.00064444 |    0.00064444 | 0.00884614 |           0.501266 |       790 |

## WFV-Style Diagnostics

| signal_name                           |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| neutral_accumulation_without_breakout |         5 |           4 |              -0.00494638 |               -0.69691 |          0.25 |               0.75 |                0.49873 |

## WFV Window Detail

| signal_name                           |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:--------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| neutral_accumulation_without_breakout |         5 |        1 | 2018-05-11   | 2019-11-15 |    -0.0144138  |   -0.195022  |           0.454545 |              198 |
| neutral_accumulation_without_breakout |         5 |        2 | 2019-11-18   | 2021-08-20 |    -0.00824657 |   -0.114711  |           0.449495 |              198 |
| neutral_accumulation_without_breakout |         5 |        3 | 2021-08-23   | 2024-02-12 |    -0.00168291 |   -0.0219216 |           0.51269  |              197 |
| neutral_accumulation_without_breakout |         5 |        4 | 2024-02-13   | 2026-02-12 |     0.00455778 |    0.0752097 |           0.538071 |              197 |

## Baseline And Inventory Similarity

| signal_name                           | top_comparison                     |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   raw_breakout_continuation_20_corr |   range_compression_breakout_proxy_corr |   quiet_liquidity_accumulation_proxy_corr |   max_price_momentum_corr |   max_breakout_continuation_corr |
|:--------------------------------------|:-----------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------------:|----------------------------------------:|------------------------------------------:|--------------------------:|---------------------------------:|
| neutral_accumulation_without_breakout | quiet_liquidity_accumulation_proxy |                0.133417 |                  0.0475597 |              6.47574e-05 |                 5.51669e-09 |            0.0475597 |           0.0595713 |           0.0336593 |                    0.0260088 |                       0.02809 |                      0.035805 |                     0.0336593 |                            0.108226 |                              0.00140453 |                                  0.133417 |                  0.035805 |                         0.108226 |

## Calm / Neutral Vs Hostile / Stress Attribution

| signal_name                           |   horizon | state                        |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:-----------------------------|----------:|------------:|------------:|-------------------:|
| neutral_accumulation_without_breakout |         5 | volatility_spike             |         1 |  0.0363247  | nan         |           1        |
| neutral_accumulation_without_breakout |         5 | panic_liquidity_stress       |         1 |  0.0363247  | nan         |           1        |
| neutral_accumulation_without_breakout |         5 | drawdown_acceleration        |        14 |  0.00202902 |   0.0330326 |           0.5      |
| neutral_accumulation_without_breakout |         5 | high_dispersion_rotation     |       140 |  0.00189935 |   0.0263695 |           0.514286 |
| neutral_accumulation_without_breakout |         5 | QUIET_ACCUMULATION_STATE     |       506 | -0.00264013 |  -0.0389608 |           0.496047 |
| neutral_accumulation_without_breakout |         5 | CALM_NORMAL_VOL              |       421 | -0.00325054 |  -0.0457838 |           0.494062 |
| neutral_accumulation_without_breakout |         5 | NORMAL_DISPERSION            |       555 | -0.00331793 |  -0.0482158 |           0.49009  |
| neutral_accumulation_without_breakout |         5 | NON_HOSTILE_NOT_WEAK_BREADTH |       756 | -0.00454683 |  -0.0640524 |           0.488095 |
| neutral_accumulation_without_breakout |         5 | NEUTRAL_MARKET_STATE         |       750 | -0.0046341  |  -0.0653169 |           0.486667 |
| neutral_accumulation_without_breakout |         5 | CONSTRUCTIVE_NOT_EUPHORIC    |       574 | -0.00781026 |  -0.112746  |           0.463415 |
| neutral_accumulation_without_breakout |         5 | trend_transition             |        63 | -0.00793354 |  -0.131743  |           0.47619  |
| neutral_accumulation_without_breakout |         5 | BREAKOUT_PRESSURE            |       246 | -0.00872076 |  -0.113712  |           0.46748  |

## Stress / Regime Attribution

| signal_name                           |   horizon | state                    |   n_dates |     mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:-------------------------|----------:|------------:|------------:|-------------------:|
| neutral_accumulation_without_breakout |         5 | volatility_spike         |         1 |  0.0363247  | nan         |           1        |
| neutral_accumulation_without_breakout |         5 | panic_liquidity_stress   |         1 |  0.0363247  | nan         |           1        |
| neutral_accumulation_without_breakout |         5 | drawdown_acceleration    |        14 |  0.00202902 |   0.0330326 |           0.5      |
| neutral_accumulation_without_breakout |         5 | high_dispersion_rotation |       140 |  0.00189935 |   0.0263695 |           0.514286 |
| neutral_accumulation_without_breakout |         5 | trend_transition         |        63 | -0.00793354 |  -0.131743  |           0.47619  |
| neutral_accumulation_without_breakout |         5 | weak_breadth             |        31 | -0.0125845  |  -0.152768  |           0.516129 |
| neutral_accumulation_without_breakout |         5 | recovery_phase           |        51 | -0.0145293  |  -0.226279  |           0.45098  |

## Sample-Size Sanity

| state                        |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:-----------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| NEUTRAL_MARKET_STATE         |           834 |          0.397521  |                           750 |                   0.357483    |
| CALM_NORMAL_VOL              |           470 |          0.224023  |                           421 |                   0.200667    |
| NORMAL_DISPERSION            |           593 |          0.28265   |                           555 |                   0.264538    |
| NON_HOSTILE_NOT_WEAK_BREADTH |          1470 |          0.700667  |                           756 |                   0.360343    |
| CONSTRUCTIVE_NOT_EUPHORIC    |           604 |          0.287893  |                           574 |                   0.273594    |
| QUIET_ACCUMULATION_STATE     |           551 |          0.262631  |                           506 |                   0.241182    |
| BREAKOUT_PRESSURE            |           514 |          0.244995  |                           246 |                   0.117255    |
| HOSTILE_OR_STRESS            |          1264 |          0.602479  |                            40 |                   0.0190658   |
| drawdown_acceleration        |           375 |          0.178742  |                            14 |                   0.00667302  |
| volatility_spike             |           404 |          0.192564  |                             1 |                   0.000476644 |
| panic_liquidity_stress       |           187 |          0.0891325 |                             1 |                   0.000476644 |
| trend_transition             |           580 |          0.276454  |                            63 |                   0.0300286   |
| recovery_phase               |           196 |          0.0934223 |                            51 |                   0.0243089   |
| high_dispersion_rotation     |           584 |          0.27836   |                           140 |                   0.0667302   |
| weak_breadth                 |           508 |          0.242135  |                            31 |                   0.014776    |
| SIGNAL_ACTIVE                |           790 |          0.376549  |                           790 |                   0.376549    |

## Candidate Decision

| signal_name                           | family                     |   best_horizon |     mean_ic |   h10_mean_ic |   h10_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_breakout_continuation_corr |   raw_breakout_continuation_20_corr |   range_compression_breakout_proxy_corr |   quiet_liquidity_accumulation_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   positive_neutral_state_count |   best_regime_ic |   best_neutral_state_ic |   best_hostile_state_ic | status          | review_issues                                                                                    |
|:--------------------------------------|:---------------------------|---------------:|------------:|--------------:|-----------------------:|--------------:|-----------------------:|-----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------:|--------------------:|--------------------------:|---------------------------------:|------------------------------------:|----------------------------------------:|------------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-------------------------------:|-----------------:|------------------------:|------------------------:|:----------------|:-------------------------------------------------------------------------------------------------|
| neutral_accumulation_without_breakout | neutral_state_accumulation |              5 | -0.00496254 |  -0.000486772 |               0.520253 |    0.00064444 |               0.501266 | -0.0694879 |           0.488608 |        0.0490795 |     0.0406145 |            0.376549 |                0.133417 |            0.0475597 |           0.0595713 |           0.0336593 |                  0.035805 |                         0.108226 |                            0.108226 |                              0.00140453 |                                  0.133417 |                  0.0475597 |              6.47574e-05 |                 5.51669e-09 |              0.25 |                   0.75 |               -0.69691 |                       2 |                              0 |        0.0363247 |             -0.00264013 |               0.0363247 | REJECT_RESEARCH | weak_primary_ic; weak_wfv_persistence; weak_neutral_state_support; hostile_state_dependence_risk |

## Specific Diagnostic Answers

- Genuinely neutral-state accumulation: assessed through neutral-state attribution and `QUIET_ACCUMULATION_STATE`; positive neutral-state count was `0` and best neutral-state IC was `-0.002640`.
- Breakout continuation risk: max breakout-continuation correlation was `0.108226`; raw breakout and range-compression breakout correlations were `0.108226` / `0.001405`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.035805` / `0.059571`.
- Participation/liquidity repair overlap risk: inventory liquidity/breadth/volatility correlations were `0.047560` / `0.000065` / `0.000000`.
- Sparse or broad activation risk: active date ratio was `0.376549`.
- Turnover risk: turnover proxy was `0.049079`.
- Directional stability: WFV-style persistence/sign consistency were `0.25` / `0.75`.
- h10/h20 profile: h10 mean IC was `-0.000487` and h20 mean IC was `0.000644`.

## Recommended Next Step

`neutral_accumulation_without_breakout` should be rejected in this formulation. Treat the result as evidence about neutral-state accumulation before testing another Expansion v3 concept.
