# Track B v5 Focused Discovery

## Executive Takeaway

This research-only run implemented the three highest-priority concepts from the Track B v5 concept screen under `track_b_v5_focused_discovery`.

This was a small focused batch, not broad discovery. It did not productionize `participation_liquidity_state_shift_20_60`, register new signals, promote survivor/watchlist state, alter gates or schemas, change thresholds, use ML, modify portfolio logic, or wire production Conditional-Alpha paths.

Candidates tested: 3
Status counts: `{"CONDITIONAL_ONLY_RESEARCH": 1, "CONDITIONAL_REFINEMENT_CANDIDATE": 1, "REJECT_RESEARCH": 1}`

## Source Notes

- Concept screen: `docs/research_notes/track_b_v5_concept_screening.md`
- Track B closeout: `docs/research_notes/track_b_conditional_alpha_cycle_closeout.md`
- Prior governed candidate remains frozen: `participation_liquidity_state_shift_20_60` -> `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

## Candidate Set

| signal_name                                       | family                             | mechanism_thesis                                                  | state_transition_logic                                                                           | non_reversal_rationale                                                                            | non_momentum_rationale                                                                         | expected_activation_state                                                    | expected_horizon   | expected_turnover_profile                        | run_id                       | research_status          |
|:--------------------------------------------------|:-----------------------------------|:------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|:-------------------|:-------------------------------------------------|:-----------------------------|:-------------------------|
| participation_breadth_repair_under_hostile_trend  | participation_breadth_transition   | Participation breadth repair during hostile trend states.         | Activates when the benchmark trend is hostile and market breadth is repairing.                   | Uses participation repair under hostile state rather than fading a large prior price move.        | Controls price extension and neutralizes 20-day return rank instead of chasing mature leaders. | TREND_HOSTILE plus breadth repair.                                           | h10-h20            | Medium-low after rank persistence and smoothing. | track_b_v5_focused_discovery | TRACK_B_V5_RESEARCH_ONLY |
| nonprice_liquidity_repair_without_price_extension | nonprice_liquidity_transition      | Non-price liquidity repair with explicit low-extension control.   | Targets securities with improving liquidity while price extension remains modest.                | Does not require prior price underperformance or abnormal price shock.                            | Liquidity repair is neutralized against recent return rank and penalizes price extension.      | Improving liquidity with low-to-moderate price extension.                    | h10-h20            | Medium-low after smoothing.                      | track_b_v5_focused_discovery | TRACK_B_V5_RESEARCH_ONLY |
| stress_to_normalization_participation_repair      | stress_normalization_participation | Participation and liquidity repair as stress begins to normalize. | Activates after recent stress when breadth/liquidity repair and volatility normalization appear. | Requires stress-state transition and participation repair rather than simply buying prior losers. | Avoids mature post-stress leaders by controlling price extension and neutralizing return rank. | Recent drawdown/volatility stress with improving participation or liquidity. | h10-h20            | Medium with explicit state activation.           | track_b_v5_focused_discovery | TRACK_B_V5_RESEARCH_ONLY |

## Structural Quality And Active Coverage

| signal_name                                       |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| participation_breadth_repair_under_hostile_trend  |     0.0258864 |     0.974114 |        0.985701 |       0.0164583  |       0        |           0.181125  |                       54 |               0.988769 |
| nonprice_liquidity_repair_without_price_extension |     0.0325135 |     0.967486 |        0.979504 |       0.051523   |       0.176592 |           0.388465  |                       86 |               0.988084 |
| stress_to_normalization_participation_repair      |     0.0357483 |     0.964252 |        0.976168 |       0.00390819 |       0        |           0.0381316 |                       16 |               0.993724 |

## Multi-Horizon IC

| signal_name                                       |   horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------------------------------------------|----------:|------------:|--------------:|-----------:|-------------------:|----------:|:------------------|
| participation_breadth_repair_under_hostile_trend  |         1 |  0.0067164  |    0.0067164  |  0.0566985 |           0.521053 |       380 | False             |
| nonprice_liquidity_repair_without_price_extension |         1 |  0.00426452 |    0.00426452 |  0.0467617 |           0.504294 |       815 | True              |
| stress_to_normalization_participation_repair      |         1 | -0.00210169 |    0.00210169 | -0.0204644 |           0.5375   |        80 | False             |
| participation_breadth_repair_under_hostile_trend  |         5 |  0.00891255 |    0.00891255 |  0.0740551 |           0.502632 |       380 | False             |
| nonprice_liquidity_repair_without_price_extension |         5 |  0.00403588 |    0.00403588 |  0.0431011 |           0.51411  |       815 | False             |
| stress_to_normalization_participation_repair      |         5 |  0.0145918  |    0.0145918  |  0.153811  |           0.5375   |        80 | False             |
| participation_breadth_repair_under_hostile_trend  |        10 |  0.00536315 |    0.00536315 |  0.0451351 |           0.5      |       380 | False             |
| nonprice_liquidity_repair_without_price_extension |        10 | -0.00137759 |    0.00137759 | -0.0156014 |           0.506748 |       815 | False             |
| stress_to_normalization_participation_repair      |        10 |  0.0463779  |    0.0463779  |  0.473413  |           0.725    |        80 | True              |
| participation_breadth_repair_under_hostile_trend  |        20 |  0.0228754  |    0.0228754  |  0.196955  |           0.563492 |       378 | True              |
| nonprice_liquidity_repair_without_price_extension |        20 | -0.00155084 |    0.00155084 | -0.0191172 |           0.511656 |       815 | False             |
| stress_to_normalization_participation_repair      |        20 |  0.0447     |    0.0447     |  0.435479  |           0.6625   |        80 | False             |

## h20 Behavior

| signal_name                                       |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:--------------------------------------------------|------------:|--------------:|-----------:|-------------------:|----------:|
| stress_to_normalization_participation_repair      |  0.0447     |    0.0447     |  0.435479  |           0.6625   |        80 |
| participation_breadth_repair_under_hostile_trend  |  0.0228754  |    0.0228754  |  0.196955  |           0.563492 |       378 |
| nonprice_liquidity_repair_without_price_extension | -0.00155084 |    0.00155084 | -0.0191172 |           0.511656 |       815 |

## WFV-Style Diagnostics

| signal_name                                       |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| nonprice_liquidity_repair_without_price_extension |         1 |           4 |               0.00425904 |               0.547864 |           0.5 |                0.5 |               0.660871 |
| participation_breadth_repair_under_hostile_trend  |        20 |           4 |               0.0228358  |               1.08218  |           1   |                1   |               0.620385 |

## Orthogonality / Redundancy

| signal_name                                       | top_comparison                                       |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |
|:--------------------------------------------------|:-----------------------------------------------------|------------------------:|-------------------------------------:|--------------------:|--------------------:|
| nonprice_liquidity_repair_without_price_extension | prior_participation_liquidity_state_shift_20_60      |               0.1331    |                            0.1331    |           0.0628703 |           0.0416624 |
| participation_breadth_repair_under_hostile_trend  | current_pool_smooth_trend_persistence_60_low_breadth |               0.0823959 |                            0.0288482 |           0.0235211 |           0.0750165 |
| stress_to_normalization_participation_repair      | prior_participation_liquidity_state_shift_20_60      |               0.0890588 |                            0.0890588 |           0.0703172 |           0.0462623 |

## Stress / Regime Attribution

| signal_name                                       |   horizon | state                    |   n_dates |   mean_ic |      ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:-------------------------|----------:|----------:|-----------:|-------------------:|
| stress_to_normalization_participation_repair      |        10 | high_dispersion_rotation |        28 | 0.0815959 |   0.801393 |           0.785714 |
| stress_to_normalization_participation_repair      |        10 | trend_transition         |        30 | 0.0781193 |   0.700852 |           0.733333 |
| stress_to_normalization_participation_repair      |        10 | recovery_phase           |        16 | 0.0703157 |   0.542846 |           0.6875   |
| stress_to_normalization_participation_repair      |        10 | drawdown_acceleration    |         1 | 0.0582976 | nan        |           1        |
| participation_breadth_repair_under_hostile_trend  |        20 | volatility_spike         |       195 | 0.0548294 |   0.432465 |           0.65641  |
| participation_breadth_repair_under_hostile_trend  |        20 | weak_breadth             |       178 | 0.0435575 |   0.356072 |           0.601124 |
| participation_breadth_repair_under_hostile_trend  |        20 | panic_liquidity_stress   |        88 | 0.0381917 |   0.356319 |           0.625    |
| nonprice_liquidity_repair_without_price_extension |         1 | recovery_phase           |        66 | 0.0225484 |   0.235534 |           0.545455 |
| participation_breadth_repair_under_hostile_trend  |        20 | drawdown_acceleration    |       125 | 0.0216211 |   0.205715 |           0.584    |
| nonprice_liquidity_repair_without_price_extension |         1 | volatility_spike         |       210 | 0.0145382 |   0.135086 |           0.533333 |
| nonprice_liquidity_repair_without_price_extension |         1 | trend_transition         |       228 | 0.0138759 |   0.149535 |           0.570175 |
| nonprice_liquidity_repair_without_price_extension |         1 | weak_breadth             |       279 | 0.0137393 |   0.141042 |           0.569892 |

## Concept State Attribution

| signal_name                                       |   horizon | state                        |   n_dates |   mean_ic |    ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:-----------------------------|----------:|----------:|---------:|-------------------:|
| stress_to_normalization_participation_repair      |        10 | PARTICIPATION_REPAIR_HOSTILE |        13 | 0.112289  | 1.64963  |           0.923077 |
| stress_to_normalization_participation_repair      |        10 | DRAWDOWN                     |        30 | 0.11165   | 1.04545  |           0.833333 |
| stress_to_normalization_participation_repair      |        10 | TREND_HOSTILE                |        19 | 0.0805897 | 1.07692  |           0.789474 |
| stress_to_normalization_participation_repair      |        10 | WEAK_BREADTH                 |        24 | 0.0644191 | 0.976166 |           0.833333 |
| stress_to_normalization_participation_repair      |        10 | BREADTH_REPAIR               |        37 | 0.0625358 | 0.633454 |           0.756757 |
| participation_breadth_repair_under_hostile_trend  |        20 | WEAK_BREADTH                 |       206 | 0.0372266 | 0.313499 |           0.592233 |
| participation_breadth_repair_under_hostile_trend  |        20 | BREADTH_REPAIR               |       293 | 0.0287865 | 0.253097 |           0.590444 |
| participation_breadth_repair_under_hostile_trend  |        20 | RECENT_STRESS                |       354 | 0.0223458 | 0.202859 |           0.567797 |
| participation_breadth_repair_under_hostile_trend  |        20 | LOW_EXTENSION_MARKET         |       237 | 0.0208351 | 0.197079 |           0.552743 |
| participation_breadth_repair_under_hostile_trend  |        20 | PARTICIPATION_REPAIR_HOSTILE |       230 | 0.0188842 | 0.168399 |           0.53913  |
| nonprice_liquidity_repair_without_price_extension |         1 | PARTICIPATION_REPAIR_HOSTILE |       195 | 0.0146476 | 0.144576 |           0.548718 |
| nonprice_liquidity_repair_without_price_extension |         1 | TREND_HOSTILE                |       359 | 0.0119049 | 0.126087 |           0.543175 |
| nonprice_liquidity_repair_without_price_extension |         1 | BREADTH_REPAIR               |       374 | 0.0114938 | 0.119679 |           0.545455 |
| nonprice_liquidity_repair_without_price_extension |         1 | DRAWDOWN                     |       318 | 0.0113048 | 0.112909 |           0.540881 |
| nonprice_liquidity_repair_without_price_extension |         1 | RECENT_STRESS                |       462 | 0.0112876 | 0.120766 |           0.536797 |

## Candidate Decisions

| signal_name                                       | family                             |   best_horizon |    mean_ic |   abs_mean_ic |     ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status                           | review_issues                                                                                |
|:--------------------------------------------------|:-----------------------------------|---------------:|-----------:|--------------:|----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|-------------------------------------:|--------------------:|--------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:---------------------------------|:---------------------------------------------------------------------------------------------|
| nonprice_liquidity_repair_without_price_extension | nonprice_liquidity_transition      |              1 | 0.00426452 |    0.00426452 | 0.0467617 |           0.504294 |       0.051523   |     0.0325135 |           0.388465  |               0.1331    |                            0.1331    |           0.0628703 |           0.0416624 |               0.5 |                    0.5 |                       7 |        0.0225484 | CONDITIONAL_ONLY_RESEARCH        | weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |
| participation_breadth_repair_under_hostile_trend  | participation_breadth_transition   |             20 | 0.0228754  |    0.0228754  | 0.196955  |           0.563492 |       0.0164583  |     0.0258864 |           0.181125  |               0.0823959 |                            0.0288482 |           0.0235211 |           0.0750165 |               1   |                    1   |                       5 |        0.0548294 | CONDITIONAL_REFINEMENT_CANDIDATE | none                                                                                         |
| stress_to_normalization_participation_repair      | stress_normalization_participation |             10 | 0.0463779  |    0.0463779  | 0.473413  |           0.725    |       0.00390819 |     0.0357483 |           0.0381316 |               0.0890588 |                            0.0890588 |           0.0703172 |           0.0462623 |             nan   |                  nan   |                       6 |        0.0815959 | REJECT_RESEARCH                  | sparse_activation                                                                            |

## Interpretation

At least one v5 concept produced enough conditional structure for follow-up research. Any follow-up should remain narrow and should not reuse this first pass as permission for broad parameter search.

| signal_name                                      | family                           |   best_horizon |   mean_ic |   abs_mean_ic |    ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   prior_participation_liquidity_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status                           | review_issues   |
|:-------------------------------------------------|:---------------------------------|---------------:|----------:|--------------:|---------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|-------------------------------------:|--------------------:|--------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:---------------------------------|:----------------|
| participation_breadth_repair_under_hostile_trend | participation_breadth_transition |             20 | 0.0228754 |     0.0228754 | 0.196955 |           0.563492 |        0.0164583 |     0.0258864 |            0.181125 |               0.0823959 |                            0.0288482 |           0.0235211 |           0.0750165 |                 1 |                      1 |                       5 |        0.0548294 | CONDITIONAL_REFINEMENT_CANDIDATE | none            |

## Concept Notes

### participation_breadth_repair_under_hostile_trend

This concept tests whether participation repair inside hostile trend states can extend the successful Track B state-transition pattern. It is closest to the prior governed candidate but intentionally emphasizes breadth repair rather than the original liquidity/participation state shift.

### nonprice_liquidity_repair_without_price_extension

This concept tests whether non-price liquidity repair can stand farther away from price-rank and reversal baselines. It should be rejected or redesigned if it behaves like generic liquidity/size exposure or converges back to the prior participation/liquidity signal.

### stress_to_normalization_participation_repair

This concept tests whether participation repair after stress normalization is a distinct conditional mechanism rather than a delayed rebound/reversal proxy. Sparse activation and crisis-window overfit are the key risks.

## Recommended Next Step

Run a focused refinement diagnostics pass only for `participation_breadth_repair_under_hostile_trend`; keep parameter exploration small and pre-declared.
