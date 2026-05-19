# Event Quality Persistence After Gap Settlement v1

## Executive Takeaway

This research-only run tested one simple formulation of `event_quality_persistence_after_gap_settlement` under the isolated run namespace `event_quality_persistence_after_gap_settlement_v1`.

The formulation was designed to test whether event-quality stabilization after a recent gap/event can add a new Conditional Alpha Inventory dimension without becoming raw gap continuation, gap reversal, momentum, or reversal.

Final classification: `CONDITIONAL_ONLY_RESEARCH`
Primary review issues: `high_missingness; high_turnover; weak_h20_ic; weak_positive_ic_rate`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, or broad discovery was performed.

## Source Context

- Expansion v2 concept screen: `docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md`
- Prior rejected dispersion concept: `docs/research_notes/dispersion_recovery_stability_after_stress_v1.md`
- Conditional Alpha Inventory reference: `docs/research_notes/conditional_alpha_inventory_v1.md`
- Volatility/stress inventory reference: `volatility_compression_after_stress_stabilization` primary `rebalance_5` panel.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Some gap/event shocks settle into controlled range, stable volume, and supportive close behavior. That settlement quality may persist beyond the event without requiring raw gap continuation or reversal. |
| Event/gap settlement logic | A material overnight gap must have occurred within the last five sessions. The event direction is carried only briefly to evaluate post-event settlement. |
| Quality confirmation logic | Require aftershock range decay, controlled relative volume, close-location support in the event direction, and a no-chase guard. |
| Persistence after settlement thesis | If settlement quality is orderly after the event, the event direction may retain conditional information at h5-h20. |
| Difference from raw gap continuation | The score is not the gap sign alone; it requires post-event range, volume, close-location, and no-chase quality. |
| Difference from gap reversal | The signal does not fade the gap; it asks whether the event direction survived settlement quality checks. |
| Difference from current inventory | It is event-time based rather than participation/liquidity/breadth repair or volatility/stress stabilization. |
| Expected activation semantics | Recent material gap plus orderly settlement quality. |
| Expected horizon | h5-h20, with h20 monitored for inventory comparability. |
| Expected turnover | Moderate, with event sparsity and churn as risks. |
| Expected active coverage | Moderate to sparse. |

## Candidate Registry

| signal_name                                    | family                    | run_id                                            | research_status                    | mechanism_thesis                                                                                  | state_transition_logic                                                                                                   | differs_from_inventory                                                                                      | differs_from_reversal_momentum                                                                              | expected_activation_state                       | expected_horizon   | expected_turnover_profile   | expected_active_coverage   |
|:-----------------------------------------------|:--------------------------|:--------------------------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:------------------------------------------------|:-------------------|:----------------------------|:---------------------------|
| event_quality_persistence_after_gap_settlement | event_quality_persistence | event_quality_persistence_after_gap_settlement_v1 | TRACK_B_EXPANSION_V2_RESEARCH_ONLY | Recent material gap followed by orderly settlement quality and short-lived direction persistence. | Gap/event shock followed by range aftershock decay, controlled volume, supportive close location, and no-chase behavior. | Event-time mechanism rather than participation/liquidity/breadth repair or volatility/stress stabilization. | Neutralizes raw gap and h20 price-rank exposure; requires settlement quality rather than fading or chasing. | RECENT_EVENT_ACTIVE_AND_HIGH_SETTLEMENT_QUALITY | h5-h20             | moderate                    | moderate_to_sparse         |

## Component Diagnostics

| component           |   finite_pct |   mean_abs |
|:--------------------|-------------:|-----------:|
| material_gap        |     1        | 0.190725   |
| recent_event_active |     1        | 0.591635   |
| aftershock_decay    |     0.982475 | 0.105774   |
| controlled_volume   |     0.983764 | 0.498375   |
| close_support       |     0.591367 | 0.266238   |
| no_chase            |     0.985951 | 0.499287   |
| settlement_quality  |     0.594152 | 0.00494735 |
| final_signal        |     0.551929 | 0.49696    |

## Structural Quality

| signal_name                                    |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-----------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| event_quality_persistence_after_gap_settlement |      0.448071 |     0.551929 |        0.990467 |         0.416584 |       0.594326 |            0.985224 |                        7 |               0.557597 |

## Multi-Horizon IC

| signal_name                                    |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-----------------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| event_quality_persistence_after_gap_settlement |         1 | -0.00191957  |   0.00191957  | -0.0197892  |           0.500484 |      2066 | False             |
| event_quality_persistence_after_gap_settlement |         5 |  0.000242822 |   0.000242822 |  0.00258885 |           0.500485 |      2062 | False             |
| event_quality_persistence_after_gap_settlement |        10 |  0.00458323  |   0.00458323  |  0.0495162  |           0.515314 |      2057 | True              |
| event_quality_persistence_after_gap_settlement |        20 |  0.00259573  |   0.00259573  |  0.0283935  |           0.520274 |      2047 | False             |

## h20 Behavior

| signal_name                                    |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   n_dates |
|:-----------------------------------------------|-----------:|--------------:|----------:|-------------------:|----------:|
| event_quality_persistence_after_gap_settlement | 0.00259573 |    0.00259573 | 0.0283935 |           0.520274 |      2047 |

## WFV-Style Diagnostics

| signal_name                                    |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-----------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| event_quality_persistence_after_gap_settlement |        10 |           4 |               0.00458463 |               0.874483 |          0.75 |               0.75 |               0.487619 |

## WFV Window Detail

| signal_name                                    |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-----------------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| event_quality_persistence_after_gap_settlement |        10 |        1 | 2018-01-31   | 2020-02-18 |     0.00171402 |    0.0194184 |           0.502913 |              515 |
| event_quality_persistence_after_gap_settlement |        10 |        2 | 2020-02-19   | 2022-03-11 |    -0.0023292  |   -0.0228138 |           0.486381 |              514 |
| event_quality_persistence_after_gap_settlement |        10 |        3 | 2022-03-14   | 2024-03-28 |     0.00773997 |    0.0885385 |           0.542802 |              514 |
| event_quality_persistence_after_gap_settlement |        10 |        4 | 2024-04-01   | 2026-04-23 |     0.0112137  |    0.123055  |           0.529183 |              514 |

## Baseline And Inventory Similarity

| signal_name                                    | top_comparison   |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   raw_gap_continuation_corr |   raw_gap_reversal_corr |   gap_volume_continuation_corr |
|:-----------------------------------------------|:-----------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|----------------------------:|------------------------:|-------------------------------:|
| event_quality_persistence_after_gap_settlement | raw_gap_reversal |                0.268485 |                  0.0123963 |              0.000520824 |                  0.00589951 |            0.0123963 |           0.0123294 |           0.0162167 |                    0.268485 |                0.268485 |                       0.243835 |

## Stress / Regime Attribution

| signal_name                                    |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:-----------------------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| event_quality_persistence_after_gap_settlement |        10 | recovery_phase           |       196 |  0.011536    |  0.119474   |           0.576531 |
| event_quality_persistence_after_gap_settlement |        10 | high_dispersion_rotation |       567 |  0.00940745  |  0.102172   |           0.530864 |
| event_quality_persistence_after_gap_settlement |        10 | drawdown_acceleration    |       365 |  0.000637069 |  0.00585532 |           0.484932 |
| event_quality_persistence_after_gap_settlement |        10 | trend_transition         |       565 |  0.000146751 |  0.00154152 |           0.497345 |
| event_quality_persistence_after_gap_settlement |        10 | weak_breadth             |       497 | -0.00050075  | -0.00493801 |           0.488934 |
| event_quality_persistence_after_gap_settlement |        10 | volatility_spike         |       392 | -0.00124555  | -0.0121041  |           0.487245 |
| event_quality_persistence_after_gap_settlement |        10 | panic_liquidity_stress   |       177 | -0.00247803  | -0.021829   |           0.468927 |

## Event-State Attribution

| signal_name                                    |   horizon | state                         |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-----------------------------------------------|----------:|:------------------------------|----------:|------------:|-----------:|-------------------:|
| event_quality_persistence_after_gap_settlement |        10 | RANGE_AFTERSHOCK              |       851 |  0.0113299  |  0.118918  |           0.511163 |
| event_quality_persistence_after_gap_settlement |        10 | HIGH_SETTLEMENT_QUALITY       |      2034 |  0.00497288 |  0.0542803 |           0.515733 |
| event_quality_persistence_after_gap_settlement |        10 | EVENT_AND_HIGH_QUALITY        |      2034 |  0.00497288 |  0.0542803 |           0.515733 |
| event_quality_persistence_after_gap_settlement |        10 | RECENT_EVENT_ACTIVE           |      2057 |  0.00458323 |  0.0495162 |           0.515314 |
| event_quality_persistence_after_gap_settlement |        10 | LARGE_GAP_CROSS_SECTION       |      2057 |  0.00458323 |  0.0495162 |           0.515314 |
| event_quality_persistence_after_gap_settlement |        10 | CONTROLLED_VOLUME_EVENT_STATE |      1509 |  0.00220499 |  0.0239003 |           0.505633 |
| event_quality_persistence_after_gap_settlement |        10 | LOW_QUALITY_EVENT_STATE       |        23 | -0.0298747  | -0.197984  |           0.478261 |

## Sample-Size Sanity

| state                         |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| RECENT_EVENT_ACTIVE           |          2097 |          0.999523  |                          2067 |                     0.985224  |
| HIGH_SETTLEMENT_QUALITY       |          2051 |          0.977598  |                          2044 |                     0.974261  |
| EVENT_AND_HIGH_QUALITY        |          2051 |          0.977598  |                          2044 |                     0.974261  |
| LARGE_GAP_CROSS_SECTION       |          2097 |          0.999523  |                          2067 |                     0.985224  |
| RANGE_AFTERSHOCK              |           865 |          0.412297  |                           854 |                     0.407054  |
| CONTROLLED_VOLUME_EVENT_STATE |          1516 |          0.722593  |                          1514 |                     0.72164   |
| LOW_QUALITY_EVENT_STATE       |            46 |          0.0219256 |                            23 |                     0.0109628 |
| SIGNAL_ACTIVE                 |          2067 |          0.985224  |                          2067 |                     0.985224  |

## Candidate Decision

| signal_name                                    | family                    |   best_horizon |    mean_ic |   h20_mean_ic |   h20_positive_ic_rate |     ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   raw_gap_continuation_corr |   raw_gap_reversal_corr |   gap_volume_continuation_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   positive_state_count |   best_regime_ic |   best_state_ic | status                    | review_issues                                                       |
|:-----------------------------------------------|:--------------------------|---------------:|-----------:|--------------:|-----------------------:|----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------:|--------------------:|----------------------------:|------------------------:|-------------------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-----------------------:|-----------------:|----------------:|:--------------------------|:--------------------------------------------------------------------|
| event_quality_persistence_after_gap_settlement | event_quality_persistence |             10 | 0.00458323 |    0.00259573 |               0.520274 | 0.0495162 |           0.515314 |         0.416584 |      0.448071 |            0.985224 |                0.268485 |            0.0123963 |           0.0123294 |           0.0162167 |                    0.268485 |                0.268485 |                       0.243835 |              0.75 |                   0.75 |               0.874483 |                       2 |                      5 |         0.011536 |       0.0113299 | CONDITIONAL_ONLY_RESEARCH | high_missingness; high_turnover; weak_h20_ic; weak_positive_ic_rate |

## Specific Diagnostic Answers

- Genuinely event-quality persistence: assessed through `EVENT_AND_HIGH_QUALITY` behavior and raw-gap baseline correlations. Raw gap continuation/reversal correlations were `0.268485` / `0.268485`.
- Momentum/reversal proxy risk: max reversal/momentum correlations were `0.012329` / `0.016217`.
- Inventory overlap risk: max inventory correlation was `0.012396`.
- Sparse activation risk: active date ratio was `0.985224`.
- Turnover risk: turnover proxy was `0.416584`.
- Directional stability: WFV-style persistence/sign consistency were `0.75` / `0.75`.

## Recommended Next Step

`event_quality_persistence_after_gap_settlement` should remain conditional-only research evidence. Do not advance until event-quality behavior separates more cleanly from raw gap baselines.
