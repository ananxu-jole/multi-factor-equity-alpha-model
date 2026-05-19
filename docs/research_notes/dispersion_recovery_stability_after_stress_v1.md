# Dispersion Recovery Stability After Stress v1

## Executive Takeaway

This research-only run tested one simple formulation of `dispersion_recovery_stability_after_stress` under the isolated run namespace `dispersion_recovery_stability_after_stress_v1`.

The formulation was designed to test whether dispersion recovery topology after stress can add a new Conditional Alpha Inventory dimension beyond participation/liquidity/breadth repair and volatility/stress stabilization.

Final classification: `REJECT_RESEARCH`
Primary review issues: `weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or broad discovery was performed.

## Source Context

- Expansion v2 concept screen: `docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md`
- Conditional Alpha Inventory reference: `docs/research_notes/conditional_alpha_inventory_v1.md`
- Volatility/stress inventory reference: `volatility_compression_after_stress_stabilization` primary `rebalance_5` panel.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | After stress, elevated cross-sectional dispersion that begins to normalize may create a cleaner stock-selection topology. Names with stable ranks and repaired idiosyncratic volatility, without price-rank extension, may carry useful conditional information. |
| Dispersion recovery logic | Market-level 20-day return dispersion must have been elevated recently and must be normalizing versus its 60-day mean with negative 10-day dispersion change. |
| Stress-state precondition | The dispersion recovery state must follow recent volatility spike, panic/liquidity stress, or drawdown acceleration. |
| Stability confirmation logic | Combine low 20-day rank churn, improving idiosyncratic volatility repair, and neutral 60-day price-rank level. |
| Inactive-date handling | Inactive dates are neutralized through a zero gate and then cross-sectionally reranked, consistent with prior conditional research conventions. |
| Turnover control | A simple 10-day rebalance hold is used to reduce rank churn without adding a parameter grid. |
| Expected horizon | h10-h20, with h20 as the primary evaluation horizon. |
| Expected turnover | Low to moderate. |
| Expected active coverage | Moderate; too-sparse activation is a rejection risk. |

## Why This Differs From Current Inventory

- It does not use participation repair, liquidity repair, or weak-breadth repair as the primary mechanism.
- It does not rely only on volatility compression after stress; dispersion recovery is the required topology state.
- It explicitly neutralizes price-rank extension to reduce momentum/reversal manifold collapse.
- It tests cross-sectional order and stability after stress, not just stress stabilization itself.

## Candidate Registry

| signal_name                                | family                       | run_id                                        | research_status                    | mechanism_thesis                                                                                | state_transition_logic                                                              | differs_from_inventory                                                                                                      | differs_from_reversal_momentum                                             | expected_activation_state       | expected_horizon   | expected_turnover_profile   | expected_active_coverage   |
|:-------------------------------------------|:-----------------------------|:----------------------------------------------|:-----------------------------------|:------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------|:--------------------------------|:-------------------|:----------------------------|:---------------------------|
| dispersion_recovery_stability_after_stress | dispersion_recovery_topology | dispersion_recovery_stability_after_stress_v1 | TRACK_B_EXPANSION_V2_RESEARCH_ONLY | Stress-conditioned dispersion recovery with rank-stability and idiosyncratic-volatility repair. | Recent stress plus recent elevated dispersion followed by dispersion normalization. | Tests cross-sectional dispersion topology instead of participation/liquidity/breadth repair or pure volatility compression. | Neutralizes price-rank extension and does not fade or chase prior returns. | STRESS_THEN_DISPERSION_RECOVERY | h10-h20            | low_to_moderate             | moderate                   |

## Component Diagnostics

| component          |   finite_pct |   mean_abs |
|:-------------------|-------------:|-----------:|
| rank_stability     |     0.97309  |  0.498589  |
| idio_vol_repair    |     0.969273 |  0.499183  |
| neutral_rank_level |     0.959736 |  0.499053  |
| active_gate        |     1        |  0.128694  |
| final_signal       |     0.955048 |  0.0862321 |

## Structural Quality

| signal_name                                |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| dispersion_recovery_stability_after_stress |     0.0449522 |     0.955048 |        0.966635 |        0.0131419 |              0 |            0.162059 |                       44 |               0.990401 |

## Multi-Horizon IC

| signal_name                                |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:-------------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| dispersion_recovery_stability_after_stress |         1 |  0.000835464 |   0.000835464 |  0.00818619 |           0.514706 |       340 | False             |
| dispersion_recovery_stability_after_stress |         5 | -6.80783e-05 |   6.80783e-05 | -0.00066568 |           0.511765 |       340 | False             |
| dispersion_recovery_stability_after_stress |        10 | -0.00193919  |   0.00193919  | -0.0205015  |           0.482249 |       338 | False             |
| dispersion_recovery_stability_after_stress |        20 | -0.00858451  |   0.00858451  | -0.0921535  |           0.429878 |       328 | True              |

## h20 Behavior

| signal_name                                |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:-------------------------------------------|------------:|--------------:|-----------:|-------------------:|----------:|
| dispersion_recovery_stability_after_stress | -0.00858451 |    0.00858451 | -0.0921535 |           0.429878 |       328 |

## WFV-Style Diagnostics

| signal_name                                |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| dispersion_recovery_stability_after_stress |        20 |           4 |              -0.00858451 |              -0.641802 |          0.25 |               0.75 |                0.61297 |

## WFV Window Detail

| signal_name                                |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-------------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| dispersion_recovery_stability_after_stress |        20 |        1 | 2018-12-14   | 2021-03-24 |    -0.00754406 |   -0.0895434 |           0.414634 |               82 |
| dispersion_recovery_stability_after_stress |        20 |        2 | 2021-03-25   | 2022-06-03 |     0.00710852 |    0.0627613 |           0.47561  |               82 |
| dispersion_recovery_stability_after_stress |        20 |        3 | 2022-06-06   | 2024-12-23 |    -0.0297628  |   -0.306891  |           0.378049 |               82 |
| dispersion_recovery_stability_after_stress |        20 |        4 | 2024-12-24   | 2026-04-09 |    -0.0041397  |   -0.0606206 |           0.45122  |               82 |

## Baseline And Inventory Similarity

| signal_name                                | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:-------------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|
| dispersion_recovery_stability_after_stress | v2_vol_compression_range_expansion_20_60 |                 0.17215 |                  0.0273203 |                0.0146389 |                    0.124088 |             0.124088 |          0.00295756 |          0.00260052 |

## Stress / Regime Attribution

| signal_name                                |   horizon | state                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-------------------------------------------|----------:|:-------------------------|----------:|------------:|-----------:|-------------------:|
| dispersion_recovery_stability_after_stress |        20 | recovery_phase           |        39 |  0.00125675 |  0.014025  |           0.435897 |
| dispersion_recovery_stability_after_stress |        20 | volatility_spike         |       157 | -0.00657538 | -0.0703168 |           0.407643 |
| dispersion_recovery_stability_after_stress |        20 | trend_transition         |       130 | -0.0247493  | -0.248141  |           0.384615 |
| dispersion_recovery_stability_after_stress |        20 | weak_breadth             |       121 | -0.0251218  | -0.282732  |           0.38843  |
| dispersion_recovery_stability_after_stress |        20 | high_dispersion_rotation |        60 | -0.0277871  | -0.261056  |           0.35     |
| dispersion_recovery_stability_after_stress |        20 | drawdown_acceleration    |        76 | -0.0528179  | -0.551144  |           0.315789 |
| dispersion_recovery_stability_after_stress |        20 | panic_liquidity_stress   |        51 | -0.0611928  | -0.816343  |           0.215686 |

## Dispersion-State Attribution

| signal_name                                |   horizon | state                                |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-------------------------------------------|----------:|:-------------------------------------|----------:|------------:|-----------:|-------------------:|
| dispersion_recovery_stability_after_stress |        20 | DISPERSION_RECOVERY_NO_STRESS        |        11 |  0.0463428  |  0.546131  |           0.636364 |
| dispersion_recovery_stability_after_stress |        20 | recovery_phase                       |        39 |  0.00125675 |  0.014025  |           0.435897 |
| dispersion_recovery_stability_after_stress |        20 | volatility_spike                     |       157 | -0.00657538 | -0.0703168 |           0.407643 |
| dispersion_recovery_stability_after_stress |        20 | STRESS_RECENT_NO_DISPERSION_RECOVERY |       120 | -0.00844475 | -0.0749313 |           0.491667 |
| dispersion_recovery_stability_after_stress |        20 | DISPERSION_NORMALIZING               |       234 | -0.0089711  | -0.0976751 |           0.431624 |
| dispersion_recovery_stability_after_stress |        20 | DISPERSION_RECOVERY                  |       194 | -0.0101642  | -0.129669  |           0.391753 |
| dispersion_recovery_stability_after_stress |        20 | DISPERSION_ELEVATED_RECENT           |       277 | -0.0105364  | -0.124097  |           0.400722 |
| dispersion_recovery_stability_after_stress |        20 | STRESS_RECENT                        |       303 | -0.0115346  | -0.124481  |           0.422442 |

## Sample-Size Sanity

| state                                |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:-------------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| STRESS_RECENT                        |          1170 |          0.557674  |                           315 |                    0.150143   |
| DISPERSION_ELEVATED_RECENT           |          1258 |          0.599619  |                           289 |                    0.13775    |
| DISPERSION_NORMALIZING               |           781 |          0.372259  |                           237 |                    0.112965   |
| DISPERSION_RECOVERY                  |           469 |          0.223546  |                           197 |                    0.093899   |
| VOLATILITY_NORMALIZING               |           826 |          0.393708  |                           109 |                    0.0519542  |
| STRESS_THEN_DISPERSION_RECOVERY      |           270 |          0.128694  |                           186 |                    0.0886559  |
| STRESS_RECENT_NO_DISPERSION_RECOVERY |           900 |          0.42898   |                           129 |                    0.0614871  |
| DISPERSION_RECOVERY_NO_STRESS        |           199 |          0.0948522 |                            11 |                    0.00524309 |
| drawdown_acceleration                |           375 |          0.178742  |                            76 |                    0.036225   |
| volatility_spike                     |           404 |          0.192564  |                           168 |                    0.0800763  |
| panic_liquidity_stress               |           187 |          0.0891325 |                            51 |                    0.0243089  |
| trend_transition                     |           580 |          0.276454  |                           142 |                    0.0676835  |
| recovery_phase                       |           196 |          0.0934223 |                            39 |                    0.0185891  |
| high_dispersion_rotation             |           584 |          0.27836   |                            66 |                    0.0314585  |
| weak_breadth                         |           508 |          0.242135  |                           121 |                    0.057674   |
| SIGNAL_ACTIVE                        |           340 |          0.162059  |                           340 |                    0.162059   |

## Candidate Decision

| signal_name                                | family                       |   best_horizon |     mean_ic |   h20_mean_ic |   h20_positive_ic_rate |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   positive_state_count |   best_regime_ic |   best_state_ic | status          | review_issues                                            |
|:-------------------------------------------|:-----------------------------|---------------:|------------:|--------------:|-----------------------:|-----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|--------------------:|--------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-----------------------:|-----------------:|----------------:|:----------------|:---------------------------------------------------------|
| dispersion_recovery_stability_after_stress | dispersion_recovery_topology |             20 | -0.00858451 |   -0.00858451 |               0.429878 | -0.0921535 |           0.429878 |        0.0131419 |     0.0449522 |            0.162059 |                 0.17215 |             0.124088 |          0.00295756 |          0.00260052 |              0.25 |                   0.75 |              -0.641802 |                       0 |                      1 |       0.00125675 |       0.0463428 | REJECT_RESEARCH | weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence |

## Specific Diagnostic Answers

- Genuinely dispersion-recovery topology: assessed through `STRESS_THEN_DISPERSION_RECOVERY` active-state sample behavior and similarity to the current inventory. Max inventory correlation was `0.124088`.
- Volatility/stress proxy risk: monitored through the direct similarity reference to `inventory_volatility_compression_after_stress_stabilization`; see the orthogonality table.
- Participation/breadth repair risk: monitored through direct similarity references to the two participation/breadth inventory candidates; see the orthogonality table.
- Sparse activation risk: active date ratio was `0.162059`.
- Directional stability: WFV-style persistence/sign consistency were `0.25` / `0.75`.

## Recommended Next Step

`dispersion_recovery_stability_after_stress` should be rejected in this formulation. Treat the result as evidence about dispersion recovery topology before considering a different concept.
