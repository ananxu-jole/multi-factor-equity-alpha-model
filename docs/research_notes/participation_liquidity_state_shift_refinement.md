# Participation Liquidity State Shift Refinement

## Executive Takeaway

This focused research-only pass refined `participation_liquidity_state_shift_20_60` under `participation_liquidity_state_shift_refinement_v1`.

Final classification: `CANDIDATE_FOR_CONDITIONAL_VALIDATION`.

The best validation-eligible variant was `rank_persist_10_state_TREND_HOSTILE_zero`. It improved turnover and h20 behavior enough to justify a formal research-only conditional-validation pass, but this is not a production promotion or survivor/watchlist registration.

No gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, production registration, or Conditional-Alpha production paths were changed.

## Inputs

- v4 source artifacts: `artifacts/research/robustness_first_discovery_expansion_v4`
- v4 conditional diagnostics: `artifacts/research/track_b_v4_conditional_diagnostics`
- Candidate panel: `participation_liquidity_state_shift_20_60_signal_panel.parquet`

## Prior v4 Conditional Evidence

| signal_name                               |   base_mean_ic |   base_positive_ic_rate |   base_turnover_proxy |   max_abs_baseline_corr | best_conditional_state   |   best_conditional_mean_ic |   best_conditional_dates | best_refinement_variant   |   best_refinement_mean_ic |   best_refinement_turnover_reduction_pct | classification                   | interpretation                                                                      |
|:------------------------------------------|---------------:|------------------------:|----------------------:|------------------------:|:-------------------------|---------------------------:|-------------------------:|:--------------------------|--------------------------:|-----------------------------------------:|:---------------------------------|:------------------------------------------------------------------------------------|
| participation_liquidity_state_shift_20_60 |     0.00842118 |                0.509564 |              0.216332 |                0.469409 | TREND_HOSTILE            |                  0.0235599 |                      749 | rebalance_10              |                 0.0165177 |                                 0.726418 | CONDITIONAL_REFINEMENT_CANDIDATE | Contains the clearest conditional structure, but turnover remains the main blocker. |

## Top Refinement Variants

| variant_name                                           |   best_horizon |   mean_ic |    ic_ir |   positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |   turnover_proxy |   active_date_coverage |   max_abs_baseline_corr |   persistence |   sign_consistency |   validation_score | candidate_ready   |
|:-------------------------------------------------------|---------------:|----------:|---------:|-------------------:|--------------:|-----------------------:|-----------------:|-----------------------:|------------------------:|--------------:|-------------------:|-------------------:|:------------------|
| rank_persist_10_state_TREND_HOSTILE_zero               |             10 | 0.0284187 | 0.205664 |           0.592033 |     0.0284181 |               0.568681 |        0.096397  |               0.346997 |                0.269307 |          1    |               1    |            5.24676 | True              |
| smooth_5_state_TREND_HOSTILE_zero                      |             20 | 0.0279964 | 0.20847  |           0.55814  |     0.0279964 |               0.55814  |        0.0595669 |               0.348427 |                0.307803 |          1    |               1    |            5.22126 | True              |
| rebalance_10_state_WEAK_BREADTH_zero                   |             20 | 0.0244101 | 0.197244 |           0.590379 |     0.0244101 |               0.590379 |        0.0545552 |               0.327455 |                0.198669 |          1    |               1    |            4.92717 | True              |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero         |             20 | 0.0242128 | 0.19885  |           0.591608 |     0.0242128 |               0.591608 |        0.0592233 |               0.341277 |                0.203465 |          1    |               1    |            4.9028  | True              |
| rebalance_10_state_HOSTILE_OR_WEAK_BREADTH_zero        |             20 | 0.0228371 | 0.188933 |           0.571114 |     0.0228371 |               0.571114 |        0.0710497 |               0.432793 |                0.212403 |          1    |               1    |            4.73068 | True              |
| rebalance_10_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero |             20 | 0.0226298 | 0.187292 |           0.569857 |     0.0226298 |               0.569857 |        0.0706026 |               0.433746 |                0.212981 |          1    |               1    |            4.70899 | True              |
| smooth_5_state_HOSTILE_OR_WEAK_BREADTH_zero            |             20 | 0.0228874 | 0.168306 |           0.554084 |     0.0228874 |               0.554084 |        0.0735705 |               0.432316 |                0.345361 |          1    |               1    |            4.68291 | True              |
| rebalance_10_state_TREND_HOSTILE_zero                  |             20 | 0.022271  | 0.180909 |           0.560109 |     0.022271  |               0.560109 |        0.058323  |               0.348904 |                0.193201 |          1    |               1    |            4.68059 | True              |
| rank_persist_10_state_WEAK_BREADTH_zero                |             20 | 0.0227163 | 0.157187 |           0.549563 |     0.0227163 |               0.549563 |        0.0902015 |               0.327455 |                0.273061 |          1    |               1    |            4.66272 | True              |
| smooth_5_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero     |             20 | 0.0226651 | 0.166753 |           0.552863 |     0.0226651 |               0.552863 |        0.0733218 |               0.43327  |                0.345866 |          1    |               1    |            4.65958 | True              |
| rebalance_20                                           |             20 | 0.0212341 | 0.201609 |           0.583906 |     0.0212341 |               0.583906 |        0.0329729 |               0.980934 |                0.213316 |          1    |               1    |            4.62102 | True              |
| rank_persist_10_state_STRESS_OR_WEAK_BREADTH_zero      |             20 | 0.0219877 | 0.154498 |           0.546985 |     0.0219877 |               0.546985 |        0.0959022 |               0.340324 |                0.279807 |          1    |               1    |            4.5799  | True              |
| rank_persist_10_state_LOW_DISPERSION_zero              |             20 | 0.0248475 | 0.196527 |           0.56875  |     0.0248475 |               0.56875  |        0.0945384 |               0.305052 |                0.278547 |          0.75 |               0.75 |            4.38932 | True              |
| rebalance_10_state_LOW_DISPERSION_zero                 |             20 | 0.0217925 | 0.181312 |           0.590625 |     0.0217925 |               0.590625 |        0.0642077 |               0.305052 |                0.208978 |          0.75 |               0.75 |            4.15342 | True              |
| smooth_5_state_WEAK_BREADTH_zero                       |             20 | 0.0217112 | 0.153354 |           0.546647 |     0.0217112 |               0.546647 |        0.0561824 |               0.327455 |                0.315711 |          0.75 |               0.75 |            4.08266 | True              |

## WFV-Style Diagnostics For Top Variants

| variant_name                                           |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-------------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| rebalance_10_state_TREND_HOSTILE_zero                  |        20 |           4 |                0.022271  |                2.93869 |             1 |                  1 |               0.351717 |
| smooth_5_state_TREND_HOSTILE_zero                      |        20 |           4 |                0.0279742 |                1.06028 |             1 |                  1 |               0.6567   |
| rank_persist_10_state_TREND_HOSTILE_zero               |        10 |           4 |                0.0284187 |                2.62303 |             1 |                  1 |               0.378624 |
| rebalance_10_state_WEAK_BREADTH_zero                   |        20 |           4 |                0.0243859 |                2.35292 |             1 |                  1 |               0.386955 |
| rank_persist_10_state_WEAK_BREADTH_zero                |        20 |           4 |                0.0226706 |                1.19277 |             1 |                  1 |               0.590216 |
| rebalance_10_state_HOSTILE_OR_WEAK_BREADTH_zero        |        20 |           4 |                0.0228307 |                2.91223 |             1 |                  1 |               0.395551 |
| smooth_5_state_HOSTILE_OR_WEAK_BREADTH_zero            |        20 |           4 |                0.0228593 |                1.2243  |             1 |                  1 |               0.594465 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero         |        20 |           4 |                0.0242097 |                2.24677 |             1 |                  1 |               0.40133  |
| rebalance_10_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero |        20 |           4 |                0.0226323 |                2.83023 |             1 |                  1 |               0.400621 |
| smooth_5_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero     |        20 |           4 |                0.0226651 |                1.20681 |             1 |                  1 |               0.599558 |

## Interpretation

- Improvements were not only generic exposure reduction: the validation-eligible variants preserved practical active-date coverage and improved h20 IC while reducing churn.
- `rebalance_10` behavior from the v4 conditional diagnostics was confirmed and extended. It appears to reduce rank-churn noise rather than merely suppressing exposure.
- `rebalance_20` produced the cleanest broad turnover-smoothed profile, while weak-breadth and stress/weak-breadth activation variants produced the cleanest conditional profiles.
- Very narrow `HOSTILE_LOW_DISPERSION` slices showed high IC but only about 10% active-date coverage, so they should be treated as supporting evidence rather than the primary validation target.
- The strongest conditional state variants support the prior finding that the signal works best in hostile, weak-breadth, drawdown, and stress-like environments.
- The candidate is still research-only. Formal conditional validation should verify active-state WFV, window stability, and turnover under fixed conditional semantics.

## Final Recommendation

Proceed to a formal research-only conditional-validation design/pass for the best fixed variant. Do not promote, register, or add it to production alpha construction.
