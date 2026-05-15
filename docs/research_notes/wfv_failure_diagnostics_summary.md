# WFV Failure Diagnostics Summary

## Objective

Diagnose why recent Batch 1 and Batch 2 signals failed or stalled before WFV/alpha-pool eligibility, without changing gates, signal logic, WFV logic, or SQLite schemas.

- Diagnostics version: `wfv_failure_diagnostics_v1`
- Run id: `wfv_failure_diagnostics_20260515_080248`
- Run timestamp: `2026-05-15 08:02:48`

## Focus Signals

- `trend_consistency_20_60`
- `index_relative_reversal_5`
- `trend_consistency_20_60_persistent`
- `percentile_rank_stability_20`
- `smooth_trend_persistence_60`

## WFV Failure Summary

| signal_name                        |   horizon | wfv_status     |   effective_mean_test_ic |   effective_test_ic_ir |   persistence_ratio |   sign_consistency | failure_type                   | wfv_gate_notes                                                                 |
|:-----------------------------------|----------:|:---------------|-------------------------:|-----------------------:|--------------------:|-------------------:|:-------------------------------|:-------------------------------------------------------------------------------|
| trend_consistency_20_60            |        20 | REJECTED_WFV   |              0.00362554  |              0.054964  |                0.25 |               0.25 | noisy_unstable_problem         | weak effective IC; low persistence; low sign consistency                       |
| index_relative_reversal_5          |         5 | REJECTED_WFV   |             -0.00103739  |             -0.0486187 |                0.75 |               0.75 | direction_flip_problem         | direction flip; weak effective IC; weak effective IC IR                        |
| trend_consistency_20_60_persistent |        20 | REJECTED_WFV   |              0.000734014 |              0.0124604 |                0.25 |               0.25 | noisy_unstable_problem         | weak effective IC; weak effective IC IR; low persistence; low sign consistency |
| percentile_rank_stability_20       |       nan | NOT_WFV_TESTED |            nan           |            nan         |              nan    |             nan    | not_wfv_tested_or_inconclusive | No controlled WFV bridge result found in WFV history.                          |
| smooth_trend_persistence_60        |       nan | NOT_WFV_TESTED |            nan           |            nan         |              nan    |             nan    | not_wfv_tested_or_inconclusive | No controlled WFV bridge result found in WFV history.                          |

## Horizon Stability

| signal_name                        |   best_horizon |   best_mean_ic |   best_abs_mean_ic | watchlist_horizons   | sign_flip_across_horizons   | horizon_stability_label     |
|:-----------------------------------|---------------:|---------------:|-------------------:|:---------------------|:----------------------------|:----------------------------|
| trend_consistency_20_60            |             20 |      0.0181396 |          0.0181396 | 10,20                | False                       | horizon_sensitive           |
| index_relative_reversal_5          |              5 |      0.0121742 |          0.0121742 | 5                    | False                       | horizon_specific            |
| trend_consistency_20_60_persistent |             20 |      0.0128149 |          0.0128149 | 20                   | False                       | horizon_specific            |
| percentile_rank_stability_20       |             20 |     -0.0174998 |          0.0174998 | 10,20                | False                       | horizon_sensitive           |
| smooth_trend_persistence_60        |             20 |     -0.0149218 |          0.0149218 | 10,20                | True                        | direction_varies_by_horizon |

## Failure Classification

| signal_name                        | primary_failure_type           | regime_specific   | horizon_specific   | market_cycle_specific   | universe_subset_specific              | classification_notes                                                                                             |
|:-----------------------------------|:-------------------------------|:------------------|:-------------------|:------------------------|:--------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| trend_consistency_20_60            | noisy_unstable_problem         | True              | True               | True                    | not_diagnosed_no_subset_wfv_available | noisy_unstable_problem; horizon_sensitive; regime fragility present                                              |
| index_relative_reversal_5          | direction_flip_problem         | True              | True               | True                    | not_diagnosed_no_subset_wfv_available | direction_flip_problem; horizon_specific; regime fragility present; decay instability present                    |
| trend_consistency_20_60_persistent | noisy_unstable_problem         | True              | True               | True                    | not_diagnosed_no_subset_wfv_available | noisy_unstable_problem; horizon_specific; regime fragility present                                               |
| percentile_rank_stability_20       | not_wfv_tested_or_inconclusive | True              | True               | False                   | not_diagnosed_no_subset_wfv_available | not_wfv_tested_or_inconclusive; horizon_sensitive; regime fragility present; decay instability present           |
| smooth_trend_persistence_60        | not_wfv_tested_or_inconclusive | True              | True               | False                   | not_diagnosed_no_subset_wfv_available | not_wfv_tested_or_inconclusive; direction_varies_by_horizon; regime fragility present; decay instability present |

## Key Findings

- `trend_consistency_20_60` and `trend_consistency_20_60_persistent` both show a similar WFV pattern: one strong positive test window and three weak or negative test windows.
- `index_relative_reversal_5` is mainly a direction-flip problem in WFV, with the first test window reversing despite positive train IC.
- `percentile_rank_stability_20` and `smooth_trend_persistence_60` were not WFV-tested in the current controlled bridge history, so their diagnostics are limited to scoring, decay, horizon, and regime evidence.
- The trend-family refinements improved structural/scoring presentation but did not solve out-of-sample persistence.
- The available diagnostics do not directly identify universe/subset-specific failures because no sector, liquidity bucket, or cross-sectional subset WFV decomposition is currently produced.

## Batch 3 Recommendations

- Do not create another small mechanical variant of `trend_consistency_20_60` until the 2021 positive test window versus the 2019, 2023, and 2025 failures is explained.
- Treat reversal variants as direction-flip prone unless a future design can demonstrate stable sign behavior across WFV windows before bridge admission.
- Add research diagnostics for subset behavior before adding sector-relative or liquidity-conditioned signals; otherwise subset-specific claims remain untested.
- Prefer Batch 3 candidates with explicit robustness hypotheses that can be falsified by WFV window diagnostics, not just higher aggregate IC.
- Keep any future bridge narrow and controlled; the recent platform behavior correctly rejected unstable refinements.

## Artifacts

Diagnostic CSV tables are written under `/Users/AnyiXu_1/Desktop/multi-factor-equity-alpha-model/artifacts/research/wfv_failure_diagnostics`.
