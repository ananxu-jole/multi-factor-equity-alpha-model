# Participation Liquidity Conditional-Alpha Integration Review

## Executive Takeaway

This research-only integration review package evaluates `participation_liquidity_state_shift_20_60` after formal conditional validation.

Final classification: `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

Recommended representation: one primary conditional variant, `rank_persist_10_state_TREND_HOSTILE_zero`, with `rebalance_10_state_WEAK_BREADTH_zero` as the first state-confirmation backup and `rebalance_20` as a broad fallback/control.

This is not production registration, survivor/watchlist promotion, portfolio integration, ML integration, or a production Conditional-Alpha path change.

## Fixed Candidate Set

| variant_name                                   | recommended_role             |   best_horizon |   h20_mean_ic |   h20_positive_ic_rate |   effective_test_ic_ir |   persistence |   sign_consistency |   h20_one_window_dominance |   turnover_proxy |   active_date_coverage |   active_window_coverage |   max_abs_baseline_corr |   max_abs_peer_corr | state_semantics                                                               |
|:-----------------------------------------------|:-----------------------------|---------------:|--------------:|-----------------------:|-----------------------:|--------------:|-------------------:|---------------------------:|-----------------:|-----------------------:|-------------------------:|------------------------:|--------------------:|:------------------------------------------------------------------------------|
| rank_persist_10_state_TREND_HOSTILE_zero       | PRIMARY_CONDITIONAL_VARIANT  |             10 |     0.0284181 |               0.568681 |                2.62303 |             1 |                  1 |                   0.568812 |        0.096397  |               0.346997 |                        1 |                0.269307 |            0.833621 | Activates during hostile trend states with rank-persistence turnover control. |
| rebalance_10_state_WEAK_BREADTH_zero           | SECONDARY_STATE_CONFIRMATION |             20 |     0.0244101 |               0.590379 |                2.35292 |             1 |                  1 |                   0.386955 |        0.0545552 |               0.327455 |                        1 |                0.198669 |            0.979701 | Activates during weak breadth states with 10-day rebalance turnover control.  |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | STRESS_CONFIRMATION_VARIANT  |             20 |     0.0242128 |               0.591608 |                2.24677 |             1 |                  1 |                   0.40133  |        0.0592233 |               0.341277 |                        1 |                0.203465 |            0.979701 | Activates during weak breadth, drawdown, or panic/liquidity stress states.    |
| rebalance_20                                   | BROAD_FALLBACK_CONTROL       |             20 |     0.0212341 |               0.583906 |                1.62128 |             1 |                  1 |                   0.486213 |        0.0329729 |               0.980934 |                        1 |                0.213316 |            0.565509 | Broad always-available smoothed reference; not a conditional primary.         |

## Representation Decision

| option                          | assessment                        | rationale                                                                                                                                                                                                 |
|:--------------------------------|:----------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| one_primary_conditional_variant | Preferred                         | `rank_persist_10_state_TREND_HOSTILE_zero` has the strongest validation score and clean hostile-trend semantics, but should be checked against h20-only rebuild behavior because its best horizon is h10. |
| small_variant_ensemble          | Not preferred for v1              | The conditional variants are highly related. An ensemble risks double-counting the same participation/liquidity state information.                                                                        |
| broad_fallback_version          | Use as control/fallback           | `rebalance_20` has broad coverage, low turnover, and stable h20 behavior, but it is less semantically conditional and should not be the primary conditional alpha representation.                         |
| hold_outside_integration        | Not supported by current evidence | Four variants passed strict validation, sample sizes were adequate, and baseline similarity stayed moderate-low.                                                                                          |

## Why The Choice Is State-Dependent

- The strongest variants are explicitly activated by hostile trend, weak breadth, or stress/weak-breadth states.
- `rebalance_20` is broadly stable and low turnover, but its broad coverage makes it more appropriate as a fallback/control than the main conditional representation.
- High peer similarity among several state variants means they should not be treated as independent alpha sleeves at this stage.
- The primary candidate has strong h20 behavior despite best horizon h10, so h20 alignment should be explicitly retested during any rebuild.

## State And Stress Snapshot

| variant_name                                   | state                  |   n_dates |   mean_ic |    ic_ir |   positive_ic_rate |
|:-----------------------------------------------|:-----------------------|----------:|----------:|---------:|-------------------:|
| rank_persist_10_state_TREND_HOSTILE_zero       | WEAK_BREADTH           |       511 | 0.0302451 | 0.208629 |           0.561644 |
| rank_persist_10_state_TREND_HOSTILE_zero       | STRESS_OR_WEAK_BREADTH |       536 | 0.029158  | 0.204929 |           0.559701 |
| rank_persist_10_state_TREND_HOSTILE_zero       | TREND_HOSTILE          |       728 | 0.0284181 | 0.211294 |           0.568681 |
| rank_persist_10_state_TREND_HOSTILE_zero       | DRAWDOWN               |       348 | 0.0271912 | 0.182365 |           0.554598 |
| rank_persist_10_state_TREND_HOSTILE_zero       | PANIC_LIQUIDITY_STRESS |       186 | 0.0268966 | 0.169906 |           0.516129 |
| rank_persist_10_state_TREND_HOSTILE_zero       | VOLATILITY_SPIKE       |       299 | 0.0180805 | 0.126552 |           0.521739 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | DRAWDOWN               |       357 | 0.0305562 | 0.246363 |           0.596639 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | VOLATILITY_SPIKE       |       261 | 0.027901  | 0.25081  |           0.574713 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | PANIC_LIQUIDITY_STRESS |       187 | 0.0278762 | 0.230025 |           0.572193 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | WEAK_BREADTH           |       686 | 0.0244101 | 0.197244 |           0.590379 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | TREND_HOSTILE          |       538 | 0.0242455 | 0.193754 |           0.585502 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | STRESS_OR_WEAK_BREADTH |       715 | 0.0242128 | 0.19885  |           0.591608 |
| rebalance_10_state_WEAK_BREADTH_zero           | DRAWDOWN               |       328 | 0.0315298 | 0.245863 |           0.594512 |
| rebalance_10_state_WEAK_BREADTH_zero           | PANIC_LIQUIDITY_STRESS |       173 | 0.0305622 | 0.245095 |           0.589595 |
| rebalance_10_state_WEAK_BREADTH_zero           | VOLATILITY_SPIKE       |       247 | 0.0297837 | 0.262744 |           0.587045 |
| rebalance_10_state_WEAK_BREADTH_zero           | WEAK_BREADTH           |       686 | 0.0244101 | 0.197244 |           0.590379 |
| rebalance_10_state_WEAK_BREADTH_zero           | STRESS_OR_WEAK_BREADTH |       686 | 0.0244101 | 0.197244 |           0.590379 |
| rebalance_10_state_WEAK_BREADTH_zero           | TREND_HOSTILE          |       511 | 0.0241379 | 0.188835 |           0.581213 |
| rebalance_20                                   | VOLATILITY_SPIKE       |       393 | 0.0329783 | 0.308793 |           0.613232 |
| rebalance_20                                   | PANIC_LIQUIDITY_STRESS |       187 | 0.0248791 | 0.225226 |           0.609626 |
| rebalance_20                                   | TREND_HOSTILE          |       732 | 0.0200697 | 0.177457 |           0.565574 |
| rebalance_20                                   | WEAK_BREADTH           |       686 | 0.0188992 | 0.165435 |           0.581633 |
| rebalance_20                                   | STRESS_OR_WEAK_BREADTH |       715 | 0.018017  | 0.159965 |           0.573427 |
| rebalance_20                                   | DRAWDOWN               |       357 | 0.0117942 | 0.105745 |           0.546218 |

## Window Stability Snapshot

| variant_name                                   |   window | start_date   | end_date   |   h20_mean_ic |   h20_positive_ic_rate |   valid_ic_dates |
|:-----------------------------------------------|---------:|:-------------|:-----------|--------------:|-----------------------:|-----------------:|
| rank_persist_10_state_TREND_HOSTILE_zero       |        1 | 2018-03-07   | 2020-03-10 |    0.0646581  |               0.642857 |              182 |
| rank_persist_10_state_TREND_HOSTILE_zero       |        2 | 2020-03-11   | 2022-05-16 |    0.0178348  |               0.554945 |              182 |
| rank_persist_10_state_TREND_HOSTILE_zero       |        3 | 2022-05-17   | 2023-10-04 |    0.0220086  |               0.549451 |              182 |
| rank_persist_10_state_TREND_HOSTILE_zero       |        4 | 2023-10-05   | 2026-04-07 |    0.00917071 |               0.527473 |              182 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |        1 | 2018-03-01   | 2020-07-13 |    0.0271209  |               0.636872 |              179 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |        2 | 2020-09-03   | 2022-03-03 |    0.0388644  |               0.597765 |              179 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |        3 | 2022-03-04   | 2024-05-02 |    0.00883448 |               0.513966 |              179 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |        4 | 2024-05-03   | 2026-04-07 |    0.0220191  |               0.617978 |              178 |
| rebalance_10_state_WEAK_BREADTH_zero           |        1 | 2018-09-27   | 2020-09-16 |    0.0276724  |               0.633721 |              172 |
| rebalance_10_state_WEAK_BREADTH_zero           |        2 | 2020-09-17   | 2022-03-07 |    0.037745   |               0.587209 |              172 |
| rebalance_10_state_WEAK_BREADTH_zero           |        3 | 2022-03-08   | 2024-04-24 |    0.00892684 |               0.502924 |              171 |
| rebalance_10_state_WEAK_BREADTH_zero           |        4 | 2024-04-25   | 2026-04-07 |    0.0231992  |               0.637427 |              171 |
| rebalance_20                                   |        1 | 2018-03-01   | 2020-03-10 |    0.0238233  |               0.607843 |              510 |
| rebalance_20                                   |        2 | 2020-03-11   | 2022-03-17 |    0.0412756  |               0.688235 |              510 |
| rebalance_20                                   |        3 | 2022-03-18   | 2024-03-27 |    0.0130568  |               0.557957 |              509 |
| rebalance_20                                   |        4 | 2024-03-28   | 2026-04-09 |    0.00673638 |               0.481336 |              509 |

## Required Guardrails

| guardrail                | requirement                                                                                                                     | review_action                                               |
|:-------------------------|:--------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------|
| parameter_lock           | Freeze the four fixed variants exactly as validated; no further tuning before integration review.                               | Required before any rebuild.                                |
| semantic_preservation    | Rebuild must preserve state labels, inactive handling, rebalance/rank-persistence logic, and sign convention.                   | Fail on formula drift.                                      |
| equivalence_rebuild_test | Compare rebuilt panels against validation artifacts for values, ranks, coverage, turnover, h20 IC, and WFV-style metrics.       | Fail or hold on unexplained drift.                          |
| active_state_coverage    | Primary conditional variants should retain active-date coverage near or above 0.30 and active-window coverage of 1.00.          | Hold if sparse windows reappear.                            |
| turnover_ceiling         | Keep turnover at or below 0.10 for conditional variants; broad fallback should remain materially lower.                         | Hold if churn returns.                                      |
| similarity_ceiling       | Keep max baseline similarity below 0.45 during integration review.                                                              | Hold if it collapses into a prior reversal/liquidity proxy. |
| peer_similarity_review   | High peer similarity is acceptable only as representation redundancy, not evidence for multiple independent alphas.             | Prefer one primary plus confirmations.                      |
| window_concentration     | Reject or hold if one-window dominance rises materially above 0.60.                                                             | Prevents one-window dominated conditional edge.             |
| rollback_trigger         | Rollback if h20 IC, WFV-style persistence/sign consistency, turnover, or baseline similarity materially deteriorate in rebuild. | Research rollback only; no production mutation.             |
| production_boundary      | No survivor/watchlist promotion, alpha pool mutation, portfolio use, ML use, or production Conditional-Alpha path changes.      | Hard boundary.                                              |

## Risks

- Selection risk remains because the validated variants are related and came from a focused refinement search.
- Peer similarity is high among conditional rebalance variants, so an ensemble could create false diversification.
- The primary variant has best horizon h10 while the integration target is h20; this needs explicit h20 preservation checks.
- State definitions must be frozen before any integration review to avoid regime-label overfitting.
- Broad fallback behavior may look cleaner because of smoothing and lower turnover; it should not be mistaken for proof of a universal alpha.

## Required Tests Before Any Future Production Consideration

- Isolated rebuild/equivalence test against the fixed validation artifacts.
- Active-state WFV diagnostic with the frozen state definitions.
- Recomputed baseline and peer-similarity audit against current Track A/Track B references.
- Turnover and active-window coverage review under the exact intended inactive handling.
- Side-by-side comparison of primary conditional variant, weak-breadth backup, stress/weak-breadth backup, and broad fallback.
- Explicit rollback memo before any production-candidate registration design.

## Final Recommendation

Proceed to a research-only Conditional-Alpha integration review design using the fixed four-variant package. Do not register the signal, promote it, add it to survivor/watchlist state, or wire it into production alpha construction.
