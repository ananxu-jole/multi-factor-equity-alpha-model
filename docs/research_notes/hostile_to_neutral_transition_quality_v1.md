# Hostile To Neutral Transition Quality v1

## Executive Takeaway

This research-only run tested one simple formulation of `hostile_to_neutral_transition_quality` under the isolated run namespace `hostile_to_neutral_transition_quality_v1`.

The formulation tests whether the boundary transition from hostile/stress into neutral/resolved conditions carries more usable alpha information than active repair alone or fully resolved-state stability alone.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `best_horizon_not_h10_h15; active_repair_dependence_risk`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v4 concepts was performed.

## Source Context

- Expansion v4 design screen: `docs/research_notes/track_b_expansion_v4_design_screening.md`
- Post-repair continuation v1: `docs/research_notes/post_repair_continuation_after_breadth_recovery_v1.md`
- Resolved stress relative stability v1: `docs/research_notes/resolved_stress_relative_stability_15_v1.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Assets that move cleanly from hostile/stress conditions into neutral/resolved conditions may show stronger forward behavior than names with noisy or incomplete transitions. |
| Hostile-state exit logic | Requires hostile/stress to have been present in the recent past, but not in the latest exit window. |
| Neutral/resolved-state entry logic | Requires inactive current hostile/stress, improving breadth, reduced benchmark drawdown pressure, normalizing volatility, and contained dispersion. |
| Transition-quality definition | Combines moderate residual support without chase, rank stabilization, range containment, residual volatility normalization, close support, and normal liquidity. |
| Difference from active repair | The signal is gated off when active hostile/stress remains present. |
| Difference from resolved-state stability | The signal requires a boundary transition window after hostile exit, not merely a fully resolved state. |
| Difference from raw continuation/momentum | Return-rank exposures are neutralized and asset support is centered away from extreme winners. |
| Difference from current inventory | Current inventory is active repair/stress h20-centered; this tests the hostile-to-neutral boundary state with h10-h15 intent. |
| Expected activation semantics | Recent hostile/stress, current neutral entry, improving breadth/drawdown pressure, clean transition quality. |
| Expected horizon | h10-h15 primary; h20 diagnostic. |
| Expected turnover | Medium after fixed 10-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparsity is a review issue. |

## Candidate Registry

| signal_name                           | family                                | run_id                                   | research_status                    | mechanism_thesis                                                                         | state_transition_logic                                                                                             | differs_from_inventory                                               | differs_from_reversal_momentum                                                   | expected_activation_state     | expected_horizon                | expected_turnover_profile   | expected_active_coverage   |
|:--------------------------------------|:--------------------------------------|:-----------------------------------------|:-----------------------------------|:-----------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------|:---------------------------------------------------------------------------------|:------------------------------|:--------------------------------|:----------------------------|:---------------------------|
| hostile_to_neutral_transition_quality | hostile_to_neutral_transition_quality | hostile_to_neutral_transition_quality_v1 | TRACK_B_EXPANSION_V4_RESEARCH_ONLY | Quality of the boundary transition from hostile/stress into neutral/resolved conditions. | Recent hostile/stress present, current neutral entry, improving breadth/drawdown pressure, clean asset transition. | Activates after hostile exit instead of during active repair/stress. | Neutralizes price-rank and reversal exposures and avoids extreme winners/losers. | HOSTILE_TO_NEUTRAL_TRANSITION | h10-h15 primary; h20 diagnostic | medium                      | medium                     |

## Component Diagnostics

| component                  |   finite_pct |   mean_abs |
|:---------------------------|-------------:|-----------:|
| support_not_chase          |     0.978801 | 0.282501   |
| rank_stabilization         |     0.973086 | 0.498454   |
| range_containment          |     0.969149 | 0.247826   |
| residual_vol_normalization |     0.977943 | 0.499126   |
| close_support              |     0.98702  | 0.501034   |
| liquidity_normal           |     0.982774 | 0.498291   |
| transition_gate            |     1        | 0.0896092  |
| transition_quality         |     0.96713  | 0.00656993 |
| final_signal               |     0.959376 | 0.0509984  |

## Structural Quality

| signal_name                           |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| hostile_to_neutral_transition_quality |   2098 |       478 |     0.0406245 |     0.959376 |        0.971401 |               0.959376 |           0 |       0.00849315 |              0 |       0.657317 |              0.168594 |            200 |           0.0953289 |                       26 |               0.987762 |

## Multi-Horizon IC

| signal_name                           |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:--------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| hostile_to_neutral_transition_quality |         1 | 0.00102344 |    0.00102344 | 0.016447  |   0.016447  |           0.497059 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |         5 | 0.00274474 |    0.00274474 | 0.0451815 |   0.0451815 |           0.502941 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        10 | 0.00175969 |    0.00175969 | 0.0287424 |   0.0287424 |           0.535294 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        15 | 0.00309658 |    0.00309658 | 0.0467214 |   0.0467214 |           0.526471 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        20 | 0.00642522 |    0.00642522 | 0.0925041 |   0.0925041 |           0.573529 |       340 |             20 | True              |

## h5 / h10 / h15 / h20 Behavior

| signal_name                           |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:--------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| hostile_to_neutral_transition_quality |         5 | 0.00274474 |    0.00274474 | 0.0451815 |   0.0451815 |           0.502941 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        10 | 0.00175969 |    0.00175969 | 0.0287424 |   0.0287424 |           0.535294 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        15 | 0.00309658 |    0.00309658 | 0.0467214 |   0.0467214 |           0.526471 |       340 |             20 | False             |
| hostile_to_neutral_transition_quality |        20 | 0.00642522 |    0.00642522 | 0.0925041 |   0.0925041 |           0.573529 |       340 |             20 | True              |

## WFV-Style Diagnostics

| signal_name                           |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| hostile_to_neutral_transition_quality |        20 |           4 |               0.00642522 |               0.296728 |          0.75 |               0.75 |               0.446069 |

## WFV Window Detail

| signal_name                           |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:--------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| hostile_to_neutral_transition_quality |        20 |        1 | 2018-07-24   | 2019-09-24 |    -0.0260633  |   -0.5729    |           0.282353 |               85 |
| hostile_to_neutral_transition_quality |        20 |        2 | 2019-09-25   | 2020-01-27 |     0.0108483  |    0.167551  |           0.670588 |               85 |
| hostile_to_neutral_transition_quality |        20 |        3 | 2020-01-28   | 2023-02-23 |     0.0347165  |    0.408005  |           0.764706 |               85 |
| hostile_to_neutral_transition_quality |        20 |        4 | 2023-02-24   | 2026-01-29 |     0.00619948 |    0.0990074 |           0.576471 |               85 |

## Baseline And Inventory Similarity

| signal_name                           | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   active_repair_proxy_corr |   resolved_stability_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   max_price_momentum_corr |   max_active_repair_corr |   max_resolved_stability_corr |   max_low_volatility_corr |
|:--------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|---------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|--------------------------:|-------------------------:|------------------------------:|--------------------------:|
| hostile_to_neutral_transition_quality | v2_vol_compression_range_expansion_20_60 |               0.0693045 |                  0.0355633 |              0.000284271 |                 0.000114789 |            0.0355633 |           0.0104015 |           0.0014422 |                    0.0131736 |                     0.0185634 |                    0.00915605 |                    0.00208172 |                     0.0014422 |                  0.0219166 |                       0.0190875 |                       0.0234769 |                                0.0244977 |                 0.0185634 |                0.0355633 |                     0.0190875 |                 0.0244977 |

## Hostile / Stress Vs Transition / Neutral Attribution

| signal_name                           |   horizon | state                         |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:------------------------------|----------:|------------:|-----------:|-------------------:|
| hostile_to_neutral_transition_quality |        20 | ACTIVE_HOSTILE_OR_STRESS      |        87 | 0.0200369   | 0.325818   |           0.655172 |
| hostile_to_neutral_transition_quality |        20 | HOSTILE_OR_STRESS             |        87 | 0.0200369   | 0.325818   |           0.655172 |
| hostile_to_neutral_transition_quality |        20 | weak_breadth                  |        55 | 0.0146792   | 0.359832   |           0.672727 |
| hostile_to_neutral_transition_quality |        20 | drawdown_acceleration         |        38 | 0.0119025   | 0.365244   |           0.631579 |
| hostile_to_neutral_transition_quality |        20 | panic_liquidity_stress        |        29 | 0.0086111   | 0.593868   |           0.655172 |
| hostile_to_neutral_transition_quality |        20 | HOSTILE_RECENTLY_PRESENT      |       325 | 0.00647135  | 0.0911625  |           0.569231 |
| hostile_to_neutral_transition_quality |        20 | volatility_spike              |        35 | 0.00619292  | 0.415721   |           0.571429 |
| hostile_to_neutral_transition_quality |        20 | NEUTRAL_ENTRY                 |       168 | 0.00492577  | 0.0666523  |           0.52381  |
| hostile_to_neutral_transition_quality |        20 | RESOLVED_NEUTRAL_STATE        |       156 | 0.0047764   | 0.0623651  |           0.512821 |
| hostile_to_neutral_transition_quality |        20 | HOSTILE_TO_NEUTRAL_TRANSITION |       139 | 0.00470321  | 0.0579752  |           0.47482  |
| hostile_to_neutral_transition_quality |        20 | TRANSITION_WITH_QUALITY       |       139 | 0.00470321  | 0.0579752  |           0.47482  |
| hostile_to_neutral_transition_quality |        20 | BREADTH_IMPROVING_TRANSITION  |       175 | 0.00457318  | 0.0630139  |           0.542857 |
| hostile_to_neutral_transition_quality |        20 | VOL_DISPERSION_NEUTRAL_ENTRY  |       205 | 0.00186058  | 0.0237919  |           0.502439 |
| hostile_to_neutral_transition_quality |        20 | DRAWDOWN_PRESSURE_REDUCED     |       237 | 0.00182033  | 0.0247552  |           0.540084 |
| hostile_to_neutral_transition_quality |        20 | high_dispersion_rotation      |        88 | 0.00109252  | 0.0456455  |           0.670455 |
| hostile_to_neutral_transition_quality |        20 | trend_transition              |        66 | 0.000126214 | 0.00606252 |           0.666667 |

## Stress / Regime Attribution

| signal_name                           |   horizon | state                    |   n_dates |      mean_ic |        ic_ir |   positive_ic_rate |
|:--------------------------------------|----------:|:-------------------------|----------:|-------------:|-------------:|-------------------:|
| hostile_to_neutral_transition_quality |        20 | weak_breadth             |        55 |  0.0146792   |   0.359832   |           0.672727 |
| hostile_to_neutral_transition_quality |        20 | drawdown_acceleration    |        38 |  0.0119025   |   0.365244   |           0.631579 |
| hostile_to_neutral_transition_quality |        20 | panic_liquidity_stress   |        29 |  0.0086111   |   0.593868   |           0.655172 |
| hostile_to_neutral_transition_quality |        20 | volatility_spike         |        35 |  0.00619292  |   0.415721   |           0.571429 |
| hostile_to_neutral_transition_quality |        20 | high_dispersion_rotation |        88 |  0.00109252  |   0.0456455  |           0.670455 |
| hostile_to_neutral_transition_quality |        20 | trend_transition         |        66 |  0.000126214 |   0.00606252 |           0.666667 |
| hostile_to_neutral_transition_quality |        20 | recovery_phase           |         1 | -0.0852701   | nan          |           0        |

## Sample-Size Sanity

| state                         |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| ACTIVE_HOSTILE_OR_STRESS      |          1048 |          0.499523  |                            15 |                   0.00714967  |
| HOSTILE_RECENTLY_PRESENT      |          1934 |          0.92183   |                           194 |                   0.092469    |
| NEUTRAL_ENTRY                 |           469 |          0.223546  |                           144 |                   0.0686368   |
| HOSTILE_TO_NEUTRAL_TRANSITION |           188 |          0.0896092 |                           138 |                   0.0657769   |
| TRANSITION_WITH_QUALITY       |           188 |          0.0896092 |                           138 |                   0.0657769   |
| BREADTH_IMPROVING_TRANSITION  |           513 |          0.244519  |                           141 |                   0.0672069   |
| DRAWDOWN_PRESSURE_REDUCED     |           878 |          0.418494  |                           178 |                   0.0848427   |
| VOL_DISPERSION_NEUTRAL_ENTRY  |           690 |          0.328885  |                           169 |                   0.0805529   |
| RESOLVED_NEUTRAL_STATE        |           396 |          0.188751  |                           138 |                   0.0657769   |
| HOSTILE_OR_STRESS             |          1048 |          0.499523  |                            15 |                   0.00714967  |
| drawdown_acceleration         |           375 |          0.178742  |                             2 |                   0.000953289 |
| volatility_spike              |           404 |          0.192564  |                             1 |                   0.000476644 |
| panic_liquidity_stress        |           187 |          0.0891325 |                             1 |                   0.000476644 |
| trend_transition              |           580 |          0.276454  |                             6 |                   0.00285987  |
| recovery_phase                |           196 |          0.0934223 |                             1 |                   0.000476644 |
| high_dispersion_rotation      |           584 |          0.27836   |                            15 |                   0.00714967  |
| weak_breadth                  |           508 |          0.242135  |                             6 |                   0.00285987  |
| SIGNAL_ACTIVE                 |           200 |          0.0953289 |                           200 |                   0.0953289   |

## Candidate Decision

| signal_name                           | family                                |   best_horizon |    mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |     ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_active_repair_corr |   max_resolved_stability_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   active_repair_proxy_corr |   resolved_stability_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_transition_state_count |   best_transition_state_ic |   best_active_state_ic |   best_resolved_state_ic | status                    | review_issues                                           |
|:--------------------------------------|:--------------------------------------|---------------:|-----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|-------------------------:|------------------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|---------------------------:|--------------------------------:|--------------------------------:|-----------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|----------------------------------:|---------------------------:|-----------------------:|-------------------------:|:--------------------------|:--------------------------------------------------------|
| hostile_to_neutral_transition_quality | hostile_to_neutral_transition_quality |             20 | 0.00642522 |   0.00274474 |              0.502941 |    0.00175969 |               0.535294 |    0.00309658 |               0.526471 |    0.00642522 |               0.573529 | 0.0925041 |           0.573529 |       0.00849315 |     0.0406245 |           0.0953289 |               0.0693045 |            0.0355633 |                0.0355633 |                     0.0190875 |           0.0104015 |           0.0014422 |                 0.0185634 |                 0.0244977 |                  0.0219166 |                       0.0190875 |                       0.0234769 |                                0.0244977 |                  0.0355633 |              0.000284271 |                 0.000114789 |              0.75 |                   0.75 |               0.296728 |                                 4 |                 0.00492577 |              0.0200369 |               0.00492577 | CONDITIONAL_ONLY_RESEARCH | best_horizon_not_h10_h15; active_repair_dependence_risk |

## Specific Diagnostic Answers

- Genuinely hostile-to-neutral transition quality: positive transition-state count was `4` and best transition-state IC was `0.004926`.
- Active hostile repair risk: best active-state IC was `0.020037` and max active-repair correlation was `0.035563`.
- Resolved-state stability risk: best resolved-state IC was `0.004926` and max resolved-stability correlation was `0.019087`.
- Low-volatility beta risk: max low-volatility correlation was `0.024498`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.018563` / `0.010402`.
- Inventory overlap risk: max inventory correlation was `0.035563`.
- Sparse or broad activation risk: active date ratio was `0.095329`.
- Turnover risk: turnover proxy was `0.008493`.
- Directional stability: WFV-style persistence/sign consistency were `0.750000` / `0.750000`.
- h5/h10/h15/h20 profile: h5 `0.002745`, h10 `0.001760`, h15 `0.003097`, h20 `0.006425`.

## Recommended Next Step

`hostile_to_neutral_transition_quality` should remain conditional-only research evidence until transition-state edge quality improves.
