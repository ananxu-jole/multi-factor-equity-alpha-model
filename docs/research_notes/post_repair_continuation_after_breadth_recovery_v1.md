# Post Repair Continuation After Breadth Recovery v1

## Executive Takeaway

This research-only run tested one simple formulation of `post_repair_continuation_after_breadth_recovery` under the isolated run namespace `post_repair_continuation_after_breadth_recovery_v1`.

The formulation tests whether the project repair/stabilization edge extends into a post-repair continuation phase after breadth recovery has already occurred.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `weak_primary_ic; active_repair_dependence_risk`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v4 concepts was performed.

## Source Context

- Expansion v4 design screen: `docs/research_notes/track_b_expansion_v4_design_screening.md`
- Expansion v3 mid-cycle review: `docs/research_notes/track_b_expansion_v3_midcycle_review.md`
- Conditional Alpha Inventory Monitoring v1: `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Breadth repair may have a second phase after weak breadth and hostile pressure clear; names with orderly participation and stable residual behavior may continue as forced selling fades. |
| Breadth-repair completion logic | Requires recent weak-breadth/hostile repair activity, current breadth recovery, no current weak breadth, no hostile benchmark trend, and no recent panic/stress flag. |
| Resolved-stress continuation logic | Selects moderate positive residual participation, relative rank stability, range orderliness, close support, residual volatility order, and participation normalization only inside the post-repair gate. |
| Difference from active hostile-state repair | The signal is gated off when weak breadth, hostile trend, or recent stress is active; it requires those conditions to have recently occurred and then cleared. |
| Difference from raw continuation/momentum | It vetoes extreme price extension and neutralizes h5/h10/h20/h60 return ranks plus 20-day reversal exposure. |
| Difference from current inventory | Current breadth and liquidity candidates activate during hostile/weak-breadth repair; this candidate attempts to activate after breadth repair has completed. |
| Expected activation semantics | Recent repair state, breadth recovered, hostile/stress inactive, orderly post-repair participation. |
| Expected horizon | h10-h15 primary; h20 diagnostic for inventory comparability. |
| Expected turnover | Low-medium after fixed 10-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparse behavior is a review issue. |

## Candidate Registry

| signal_name                                     | family                   | run_id                                             | research_status                    | mechanism_thesis                                                            | state_transition_logic                                                                                                    | differs_from_inventory                                                           | differs_from_reversal_momentum                                               | expected_activation_state    | expected_horizon                | expected_turnover_profile   | expected_active_coverage   |
|:------------------------------------------------|:-------------------------|:---------------------------------------------------|:-----------------------------------|:----------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|:-----------------------------|:--------------------------------|:----------------------------|:---------------------------|
| post_repair_continuation_after_breadth_recovery | post_repair_continuation | post_repair_continuation_after_breadth_recovery_v1 | TRACK_B_EXPANSION_V4_RESEARCH_ONLY | Post-repair continuation after weak-breadth recovery has already completed. | Recent weak-breadth/hostile repair, current breadth recovery, hostile/stress inactive, orderly post-repair participation. | Activates after repair completion instead of during hostile/weak-breadth repair. | Neutralizes return-rank and reversal exposures and vetoes extreme extension. | POST_REPAIR_BREADTH_RECOVERY | h10-h15 primary; h20 diagnostic | low_to_medium               | medium                     |

## Component Diagnostics

| component                       |   finite_pct |   mean_abs |
|:--------------------------------|-------------:|-----------:|
| moderate_positive_participation |     0.978801 | 0.29498    |
| relative_stability              |     0.973086 | 0.498454   |
| range_orderliness               |     0.969149 | 0.247826   |
| close_support                   |     0.985592 | 0.501004   |
| residual_vol_order              |     0.977943 | 0.499126   |
| participation_normalization     |     0.982774 | 0.498291   |
| no_extension                    |     1        | 0.533457   |
| post_repair_gate                |     1        | 0.123928   |
| continuation_quality            |     0.96713  | 0.00737672 |
| final_signal                    |     0.959376 | 0.0731905  |

## Structural Quality

| signal_name                                     |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:------------------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| post_repair_continuation_after_breadth_recovery |   2098 |       478 |     0.0406245 |     0.959376 |        0.971401 |               0.959376 |           0 |        0.0115394 |              0 |        0.62798 |              0.397751 |            290 |            0.138227 |                       34 |               0.990694 |

## Multi-Horizon IC

| signal_name                                     |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:------------------------------------------------|----------:|-------------:|--------------:|------------:|------------:|-------------------:|----------:|---------------:|:------------------|
| post_repair_continuation_after_breadth_recovery |         1 |  0.00014699  |   0.00014699  |  0.00293982 |  0.00293982 |           0.501859 |       807 |             15 | False             |
| post_repair_continuation_after_breadth_recovery |         5 | -0.000452616 |   0.000452616 | -0.00995463 |  0.00995463 |           0.516812 |       803 |             15 | False             |
| post_repair_continuation_after_breadth_recovery |        10 |  0.00340574  |   0.00340574  |  0.0823693  |  0.0823693  |           0.576441 |       798 |             15 | False             |
| post_repair_continuation_after_breadth_recovery |        15 |  0.00451038  |   0.00451038  |  0.112592   |  0.112592   |           0.580076 |       793 |             15 | True              |
| post_repair_continuation_after_breadth_recovery |        20 |  0.00304806  |   0.00304806  |  0.0736761  |  0.0736761  |           0.598985 |       788 |             15 | False             |

## h5 / h10 / h15 / h20 Behavior

| signal_name                                     |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:------------------------------------------------|----------:|-------------:|--------------:|------------:|------------:|-------------------:|----------:|---------------:|:------------------|
| post_repair_continuation_after_breadth_recovery |         5 | -0.000452616 |   0.000452616 | -0.00995463 |  0.00995463 |           0.516812 |       803 |             15 | False             |
| post_repair_continuation_after_breadth_recovery |        10 |  0.00340574  |   0.00340574  |  0.0823693  |  0.0823693  |           0.576441 |       798 |             15 | False             |
| post_repair_continuation_after_breadth_recovery |        15 |  0.00451038  |   0.00451038  |  0.112592   |  0.112592   |           0.580076 |       793 |             15 | True              |
| post_repair_continuation_after_breadth_recovery |        20 |  0.00304806  |   0.00304806  |  0.0736761  |  0.0736761  |           0.598985 |       788 |             15 | False             |

## WFV-Style Diagnostics

| signal_name                                     |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| post_repair_continuation_after_breadth_recovery |        15 |           4 |               0.00451233 |               0.495936 |          0.75 |               0.75 |               0.458468 |

## WFV Window Detail

| signal_name                                     |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:------------------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| post_repair_continuation_after_breadth_recovery |        15 |        1 | 2019-07-09   | 2020-08-27 |     0.00296812 |     0.10637  |           0.60804  |              199 |
| post_repair_continuation_after_breadth_recovery |        15 |        2 | 2020-08-28   | 2024-09-16 |    -0.00884899 |    -0.145403 |           0.419192 |              198 |
| post_repair_continuation_after_breadth_recovery |        15 |        3 | 2024-09-17   | 2025-07-02 |     0.00754119 |     0.39356  |           0.666667 |              198 |
| post_repair_continuation_after_breadth_recovery |        15 |        4 | 2025-07-03   | 2026-04-16 |     0.016389   |     0.464944 |           0.626263 |              198 |

## Baseline And Inventory Similarity

| signal_name                                     | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   post_repair_participation_proxy_corr |   active_breadth_repair_proxy_corr |   max_price_momentum_corr |   max_breadth_repair_corr |
|:------------------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|---------------------------------------:|-----------------------------------:|--------------------------:|--------------------------:|
| post_repair_continuation_after_breadth_recovery | v2_vol_compression_range_expansion_20_60 |                0.138087 |                  0.0306344 |              0.000171383 |                 0.000545856 |            0.0306344 |          0.00791541 |          0.00188831 |                   0.00050213 |                    0.00321748 |                     0.0104767 |                     0.0079154 |                    0.00188831 |                              0.0917759 |                         0.00255948 |                 0.0104767 |                0.00255948 |

## Hostile / Stress Vs Resolved / Neutral Attribution

| signal_name                                     |   horizon | state                            |   n_dates |      mean_ic |      ic_ir |   positive_ic_rate |
|:------------------------------------------------|----------:|:---------------------------------|----------:|-------------:|-----------:|-------------------:|
| post_repair_continuation_after_breadth_recovery |        15 | recovery_phase                   |        25 |  0.0153633   |  0.306421  |           0.56     |
| post_repair_continuation_after_breadth_recovery |        15 | volatility_spike                 |       163 |  0.00792014  |  0.413284  |           0.650307 |
| post_repair_continuation_after_breadth_recovery |        15 | POST_REPAIR_BREADTH_RECOVERY     |       212 |  0.00628578  |  0.107501  |           0.54717  |
| post_repair_continuation_after_breadth_recovery |        15 | POST_REPAIR_QUALITY_CONFIRMATION |       212 |  0.00628578  |  0.107501  |           0.54717  |
| post_repair_continuation_after_breadth_recovery |        15 | panic_liquidity_stress           |        81 |  0.00619539  |  0.379861  |           0.654321 |
| post_repair_continuation_after_breadth_recovery |        15 | BREADTH_CONFIRMED_RECOVERY       |       201 |  0.00586771  |  0.101889  |           0.532338 |
| post_repair_continuation_after_breadth_recovery |        15 | high_dispersion_rotation         |       233 |  0.00580438  |  0.177499  |           0.575107 |
| post_repair_continuation_after_breadth_recovery |        15 | RESOLVED_STRESS_OR_REPAIR        |       382 |  0.00543764  |  0.101346  |           0.570681 |
| post_repair_continuation_after_breadth_recovery |        15 | drawdown_acceleration            |       113 |  0.00443775  |  0.2359    |           0.610619 |
| post_repair_continuation_after_breadth_recovery |        15 | HOSTILE_OR_STRESS                |       396 |  0.00371268  |  0.183785  |           0.588384 |
| post_repair_continuation_after_breadth_recovery |        15 | weak_breadth                     |       173 |  0.00123679  |  0.0642924 |           0.50289  |
| post_repair_continuation_after_breadth_recovery |        15 | ACTIVE_HOSTILE_BREADTH_REPAIR    |       215 |  0.000959231 |  0.0470453 |           0.516279 |
| post_repair_continuation_after_breadth_recovery |        15 | trend_transition                 |       183 | -0.000880594 | -0.0329694 |           0.551913 |

## Stress / Regime Attribution

| signal_name                                     |   horizon | state                    |   n_dates |      mean_ic |      ic_ir |   positive_ic_rate |
|:------------------------------------------------|----------:|:-------------------------|----------:|-------------:|-----------:|-------------------:|
| post_repair_continuation_after_breadth_recovery |        15 | recovery_phase           |        25 |  0.0153633   |  0.306421  |           0.56     |
| post_repair_continuation_after_breadth_recovery |        15 | volatility_spike         |       163 |  0.00792014  |  0.413284  |           0.650307 |
| post_repair_continuation_after_breadth_recovery |        15 | panic_liquidity_stress   |        81 |  0.00619539  |  0.379861  |           0.654321 |
| post_repair_continuation_after_breadth_recovery |        15 | high_dispersion_rotation |       233 |  0.00580438  |  0.177499  |           0.575107 |
| post_repair_continuation_after_breadth_recovery |        15 | drawdown_acceleration    |       113 |  0.00443775  |  0.2359    |           0.610619 |
| post_repair_continuation_after_breadth_recovery |        15 | weak_breadth             |       173 |  0.00123679  |  0.0642924 |           0.50289  |
| post_repair_continuation_after_breadth_recovery |        15 | trend_transition         |       183 | -0.000880594 | -0.0329694 |           0.551913 |

## Sample-Size Sanity

| state                            |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:---------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| ACTIVE_HOSTILE_BREADTH_REPAIR    |           660 |          0.314585  |                            20 |                   0.00953289  |
| POST_REPAIR_BREADTH_RECOVERY     |           260 |          0.123928  |                           170 |                   0.0810296   |
| POST_REPAIR_QUALITY_CONFIRMATION |           260 |          0.123928  |                           170 |                   0.0810296   |
| BREADTH_CONFIRMED_RECOVERY       |           304 |          0.1449    |                           153 |                   0.0729266   |
| RESOLVED_STRESS_OR_REPAIR        |           643 |          0.306482  |                           259 |                   0.123451    |
| HOSTILE_OR_STRESS                |          1264 |          0.602479  |                            25 |                   0.0119161   |
| drawdown_acceleration            |           375 |          0.178742  |                             9 |                   0.0042898   |
| volatility_spike                 |           404 |          0.192564  |                             1 |                   0.000476644 |
| panic_liquidity_stress           |           187 |          0.0891325 |                             1 |                   0.000476644 |
| trend_transition                 |           580 |          0.276454  |                            22 |                   0.0104862   |
| recovery_phase                   |           196 |          0.0934223 |                            19 |                   0.00905624  |
| high_dispersion_rotation         |           584 |          0.27836   |                            56 |                   0.0266921   |
| weak_breadth                     |           508 |          0.242135  |                            11 |                   0.00524309  |
| SIGNAL_ACTIVE                    |           290 |          0.138227  |                           290 |                   0.138227    |

## Candidate Decision

| signal_name                                     | family                   |   best_horizon |    mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |    ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_breadth_repair_corr |   max_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   post_repair_participation_proxy_corr |   active_breadth_repair_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_resolved_state_count |   best_resolved_state_ic |   best_active_repair_state_ic | status                    | review_issues                                  |
|:------------------------------------------------|:-------------------------|---------------:|-----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|---------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------------:|--------------------:|--------------------:|--------------------------:|---------------------------------------:|-----------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|--------------------------------:|-------------------------:|------------------------------:|:--------------------------|:-----------------------------------------------|
| post_repair_continuation_after_breadth_recovery | post_repair_continuation |             15 | 0.00451038 | -0.000452616 |              0.516812 |    0.00340574 |               0.576441 |    0.00451038 |               0.580076 |    0.00304806 |               0.598985 | 0.112592 |           0.580076 |        0.0115394 |     0.0406245 |            0.138227 |                0.138087 |            0.0306344 |                0.00255948 |          0.00791541 |          0.00188831 |                 0.0104767 |                              0.0917759 |                         0.00255948 |                  0.0306344 |              0.000171383 |                 0.000545856 |              0.75 |                   0.75 |               0.495936 |                               4 |               0.00628578 |                    0.00792014 | CONDITIONAL_ONLY_RESEARCH | weak_primary_ic; active_repair_dependence_risk |

## Specific Diagnostic Answers

- Genuinely post-repair continuation: positive resolved-state count was `4` and best resolved-state IC was `0.006286`.
- Active hostile-state breadth repair risk: max breadth-repair correlation was `0.002559`; inventory breadth correlation was `0.000171`.
- Momentum/reversal proxy risk: max price-momentum/reversal correlations were `0.010477` / `0.007915`.
- Inventory overlap risk: max inventory correlation was `0.030634`.
- Sparse or broad activation risk: active date ratio was `0.138227`.
- Turnover risk: turnover proxy was `0.011539`.
- Directional stability: WFV-style persistence/sign consistency were `0.750000` / `0.750000`.
- h5/h10/h15/h20 profile: h5 `-0.000453`, h10 `0.003406`, h15 `0.004510`, h20 `0.003048`.

## Recommended Next Step

`post_repair_continuation_after_breadth_recovery` should remain conditional-only evidence until edge quality and resolved-state attribution improve.
