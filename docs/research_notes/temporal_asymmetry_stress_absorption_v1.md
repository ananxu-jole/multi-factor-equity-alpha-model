# Temporal Asymmetry Stress Absorption v1

## Executive Takeaway

This research-only run tested one simple formulation of `temporal_asymmetry_stress_absorption` under the isolated run namespace `temporal_asymmetry_stress_absorption_v1`.

The formulation was designed to test whether healthier temporal path shape during and after stress can add a Conditional Alpha Inventory dimension beyond participation repair, breadth repair, liquidity repair, volatility compression, and event-quality concepts.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, or broad discovery was performed.

## Source Context

- Expansion v2 concept screen: `docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md`
- Prior event-quality test: `docs/research_notes/event_quality_persistence_after_gap_settlement_v1.md`
- Prior dispersion-recovery test: `docs/research_notes/dispersion_recovery_stability_after_stress_v1.md`
- Conditional Alpha Inventory reference: `docs/research_notes/conditional_alpha_inventory_v1.md`

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Assets that absorb stress through healthier temporal paths may have better forward behavior than assets with chaotic or fragile stress paths. |
| Temporal asymmetry logic | Score the quality of behavior during market-down pressure and recent stress, rather than the level of past return. |
| Stress absorption logic | Favor strong close-location on market down days, slower downside deterioration, faster volatility/range stabilization, and lower path chaos. |
| Path-shape definition | Combine close absorption, deterioration control, volatility stabilization, range stabilization, path orderliness, and a neutral price-rank guard. |
| Difference from reversal | It does not buy losers or fade prior returns; 20-day return rank is neutralized. |
| Difference from momentum | It does not chase price rank; both short and medium price-rank extension are penalized. |
| Difference from current inventory | It is temporal/path-shape based, not participation/liquidity/breadth repair or pure volatility/stress compression. |
| Expected activation semantics | Recent market stress with healthier asset-level absorption path shape. |
| Expected horizon | h10-h20, with h20 monitored for inventory comparability. |
| Expected turnover | Low to moderate due to 5-day rebalance hold. |
| Expected active coverage | Moderate; stress-conditioned but not rare-event-only. |

## Candidate Registry

| signal_name                          | family                               | run_id                                  | research_status                    | mechanism_thesis                                                                                  | state_transition_logic                                                 | differs_from_inventory                                                                             | differs_from_reversal_momentum                                              | expected_activation_state          | expected_horizon   | expected_turnover_profile   | expected_active_coverage   |
|:-------------------------------------|:-------------------------------------|:----------------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------|:-----------------------------------|:-------------------|:----------------------------|:---------------------------|
| temporal_asymmetry_stress_absorption | temporal_asymmetry_stress_absorption | temporal_asymmetry_stress_absorption_v1 | TRACK_B_EXPANSION_V2_RESEARCH_ONLY | Stress-conditioned temporal path quality through absorption, stabilization, and lower path chaos. | Recent stress plus healthier asset-level stress absorption path shape. | Path-shape mechanism rather than participation/liquidity/breadth repair or volatility compression. | Neutralizes price-rank exposure and penalizes short/medium price extension. | RECENT_STRESS_WITH_HIGH_ABSORPTION | h10-h20            | low_to_moderate             | moderate                   |

## Component Diagnostics

| component                |   finite_pct |   mean_abs |
|:-------------------------|-------------:|-----------:|
| close_absorption_score   |     0.66178  |   0.501263 |
| deterioration_control    |     0.453129 |   0.498038 |
| volatility_stabilization |     0.982615 |   0.499013 |
| range_stabilization      |     0.982475 |   0.499149 |
| path_orderliness         |     0.985002 |   0.497504 |
| neutral_rank_level       |     0.978801 |   0.26973  |
| stress_gate              |     1        |   0.557674 |
| final_signal             |     0.931624 |   0.35456  |

## Structural Quality

| signal_name                          |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| temporal_asymmetry_stress_absorption |     0.0683755 |     0.931624 |        0.942803 |        0.0336088 |       0.416687 |            0.666349 |                       19 |               0.988934 |

## Multi-Horizon IC

| signal_name                          |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| temporal_asymmetry_stress_absorption |         1 |  0.0027849   |   0.0027849   |  0.0165709  |           0.496063 |      1397 | False             |
| temporal_asymmetry_stress_absorption |         5 |  0.000682761 |   0.000682761 |  0.00411326 |           0.496052 |      1393 | False             |
| temporal_asymmetry_stress_absorption |        10 | -0.00405125  |   0.00405125  | -0.0246611  |           0.490634 |      1388 | False             |
| temporal_asymmetry_stress_absorption |        20 | -0.00759485  |   0.00759485  | -0.050456   |           0.475327 |      1378 | True              |

## h20 Behavior

| signal_name                          |     mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates |
|:-------------------------------------|------------:|--------------:|----------:|-------------------:|----------:|
| temporal_asymmetry_stress_absorption | -0.00759485 |    0.00759485 | -0.050456 |           0.475327 |      1378 |

## WFV-Style Diagnostics

| signal_name                          |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| temporal_asymmetry_stress_absorption |        20 |           4 |              -0.00762512 |              -0.210217 |          0.25 |               0.75 |               0.406781 |

## WFV Window Detail

| signal_name                          |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| temporal_asymmetry_stress_absorption |        20 |        1 | 2018-10-17   | 2020-10-19 |    -0.0217712  |   -0.175159  |           0.402899 |              345 |
| temporal_asymmetry_stress_absorption |        20 |        2 | 2020-10-20   | 2022-08-24 |     0.0482289  |    0.308389  |           0.631884 |              345 |
| temporal_asymmetry_stress_absorption |        20 |        3 | 2022-08-25   | 2024-01-08 |    -0.0516442  |   -0.346444  |           0.372093 |              344 |
| temporal_asymmetry_stress_absorption |        20 |        4 | 2024-01-09   | 2026-04-09 |    -0.00531402 |   -0.0348544 |           0.494186 |              344 |

## Baseline And Inventory Similarity

| signal_name                          | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   raw_close_absorption_on_down_days_corr |   downside_reversal_under_market_pressure_corr |   simple_temporal_volatility_stabilization_corr |   simple_range_stabilization_corr |
|:-------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------------------:|-----------------------------------------------:|------------------------------------------------:|----------------------------------:|
| temporal_asymmetry_stress_absorption | v2_vol_compression_range_expansion_20_60 |                0.321024 |                   0.030735 |                0.0301184 |                    0.153226 |             0.153226 |           0.0126711 |           0.0131556 |                                 0.226421 |                                      0.0138803 |                                       0.0369615 |                        0.00898553 |

## Stress / Regime Attribution

| signal_name                          |   horizon | state                    |   n_dates |    mean_ic |      ic_ir |   positive_ic_rate |
|:-------------------------------------|----------:|:-------------------------|----------:|-----------:|-----------:|-------------------:|
| temporal_asymmetry_stress_absorption |        20 | recovery_phase           |       195 |  0.0137058 |  0.0917087 |           0.54359  |
| temporal_asymmetry_stress_absorption |        20 | volatility_spike         |       382 |  0.0122826 |  0.0813084 |           0.507853 |
| temporal_asymmetry_stress_absorption |        20 | high_dispersion_rotation |       449 |  0.0118585 |  0.0860933 |           0.52784  |
| temporal_asymmetry_stress_absorption |        20 | trend_transition         |       474 | -0.0080941 | -0.0541268 |           0.474684 |
| temporal_asymmetry_stress_absorption |        20 | weak_breadth             |       422 | -0.014787  | -0.107321  |           0.443128 |
| temporal_asymmetry_stress_absorption |        20 | panic_liquidity_stress   |       187 | -0.0167863 | -0.141801  |           0.481283 |
| temporal_asymmetry_stress_absorption |        20 | drawdown_acceleration    |       319 | -0.0272314 | -0.222232  |           0.429467 |

## Temporal-State Attribution

| signal_name                          |   horizon | state                       |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-------------------------------------|----------:|:----------------------------|----------:|------------:|-----------:|-------------------:|
| temporal_asymmetry_stress_absorption |        20 | recovery_phase              |       195 |  0.0137058  |  0.0917087 |           0.54359  |
| temporal_asymmetry_stress_absorption |        20 | volatility_spike            |       382 |  0.0122826  |  0.0813084 |           0.507853 |
| temporal_asymmetry_stress_absorption |        20 | high_dispersion_rotation    |       449 |  0.0118585  |  0.0860933 |           0.52784  |
| temporal_asymmetry_stress_absorption |        20 | trend_transition            |       474 | -0.0080941  | -0.0541268 |           0.474684 |
| temporal_asymmetry_stress_absorption |        20 | VOL_STABILIZING             |       507 | -0.00913117 | -0.0594094 |           0.4714   |
| temporal_asymmetry_stress_absorption |        20 | STRESS_WITH_HIGH_ABSORPTION |       653 | -0.00927917 | -0.0610902 |           0.454824 |
| temporal_asymmetry_stress_absorption |        20 | HIGH_ABSORPTION_QUALITY     |       688 | -0.0107122  | -0.0694737 |           0.454942 |
| temporal_asymmetry_stress_absorption |        20 | STRESS_RECENT               |      1027 | -0.0114859  | -0.0773299 |           0.451801 |

## Sample-Size Sanity

| state                       |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:----------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| STRESS_RECENT               |          1170 |          0.557674  |                          1047 |                     0.499047  |
| MARKET_DOWN_PRESSURE        |           694 |          0.330791  |                           495 |                     0.235939  |
| VOL_STABILIZING             |           826 |          0.393708  |                           516 |                     0.245949  |
| HIGH_ABSORPTION_QUALITY     |           893 |          0.425643  |                           688 |                     0.327931  |
| STRESS_WITH_HIGH_ABSORPTION |           679 |          0.323642  |                           653 |                     0.311249  |
| STRESS_WITH_LOW_ABSORPTION  |           491 |          0.234032  |                           394 |                     0.187798  |
| drawdown_acceleration       |           375 |          0.178742  |                           319 |                     0.15205   |
| volatility_spike            |           404 |          0.192564  |                           393 |                     0.187321  |
| panic_liquidity_stress      |           187 |          0.0891325 |                           187 |                     0.0891325 |
| trend_transition            |           580 |          0.276454  |                           492 |                     0.234509  |
| recovery_phase              |           196 |          0.0934223 |                           195 |                     0.0929457 |
| high_dispersion_rotation    |           584 |          0.27836   |                           463 |                     0.220686  |
| weak_breadth                |           508 |          0.242135  |                           422 |                     0.201144  |
| SIGNAL_ACTIVE               |          1398 |          0.666349  |                          1398 |                     0.666349  |

## Candidate Decision

| signal_name                          | family                               |   best_horizon |     mean_ic |   h20_mean_ic |   h20_positive_ic_rate |     ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   raw_close_absorption_corr |   downside_reversal_pressure_corr |   simple_temporal_volatility_stabilization_corr |   simple_range_stabilization_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   positive_state_count |   best_regime_ic |   best_state_ic | status                    | review_issues                                            |
|:-------------------------------------|:-------------------------------------|---------------:|------------:|--------------:|-----------------------:|----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------:|--------------------:|----------------------------:|----------------------------------:|------------------------------------------------:|----------------------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-----------------------:|-----------------:|----------------:|:--------------------------|:---------------------------------------------------------|
| temporal_asymmetry_stress_absorption | temporal_asymmetry_stress_absorption |             20 | -0.00759485 |   -0.00759485 |               0.475327 | -0.050456 |           0.475327 |        0.0336088 |     0.0683755 |            0.666349 |                0.321024 |             0.153226 |           0.0126711 |           0.0131556 |                    0.226421 |                         0.0138803 |                                       0.0369615 |                        0.00898553 |              0.25 |                   0.75 |              -0.210217 |                       3 |                      3 |        0.0137058 |       0.0137058 | CONDITIONAL_ONLY_RESEARCH | weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence |

## Specific Diagnostic Answers

- Temporal/path-shape behavior: assessed through `STRESS_WITH_HIGH_ABSORPTION`, raw close absorption correlation `0.226421`, and path-shape component diagnostics.
- Reversal/momentum proxy risk: max reversal/momentum correlations were `0.012671` / `0.013156`.
- Volatility/stress proxy risk: inventory max correlation was `0.153226` and simple volatility-stabilization correlation was `0.036961`.
- Sparse activation risk: active date ratio was `0.666349`.
- Turnover risk: turnover proxy was `0.033609`.
- Directional stability: WFV-style persistence/sign consistency were `0.25` / `0.75`.

## Recommended Next Step

`temporal_asymmetry_stress_absorption` should remain conditional-only research evidence. Do not advance until temporal path-shape behavior is stronger and less noisy.
