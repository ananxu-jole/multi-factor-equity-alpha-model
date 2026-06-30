# Drawdown Pressure Stabilization 10 v1

## Executive Takeaway

This research-only run tested one simple formulation of `drawdown_pressure_stabilization_10` under the isolated run namespace `drawdown_pressure_stabilization_10_v1`.

The formulation tests whether assets whose downside pressure is stabilizing during active drawdown-pressure regimes can produce a shorter-horizon repair/stabilization edge, especially around h10, without becoming breadth/participation repair, reversal, or momentum.

Final classification: `REJECT_RESEARCH`
Primary review issues: `weak_h10_ic; weak_h10_positive_ic_rate; weak_primary_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_drawdown_state_support`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v5 concepts was performed.

## Source Context

- Expansion v5 design screen: `docs/research_notes/track_b_expansion_v5_design_screening.md`
- Conditional Alpha Inventory Monitoring v2: `docs/research_notes/conditional_alpha_inventory_monitoring_v2.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Expansion v4 closeout review: `docs/research_notes/track_b_expansion_v4_closeout_review.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | Downside-pressure containment during active drawdown regimes may identify stocks where repair is starting before broad participation or breadth recovery dominates. |
| Drawdown-pressure definition | Market-level drawdown acceleration, benchmark drawdown versus its recent peak, or negative benchmark trend pressure. |
| Stabilization confirmation logic | Reduced residual downside pressure, non-extreme prior damage, no short-horizon chase, range containment, residual volatility normalization, close support, and sufficient liquidity. |
| Difference from active breadth/participation repair | Activation is drawdown-pressure based and explicitly does not require weak-breadth repair or participation recovery. |
| Difference from simple reversal | The signal avoids extreme losers and neutralizes reversal exposures after scoring. |
| Difference from price momentum | Price-rank momentum and residual momentum exposures are neutralized. |
| Why it may reduce h20 concentration | The mechanism is designed around h10 pressure stabilization and uses a 10-day rebalance interval, with h20 treated as diagnostic risk. |
| Expected activation semantics | Active drawdown pressure with reducing downside pressure and contained dispersion. |
| Expected horizon | h10 primary; h5 and h15 secondary; h20 diagnostic. |
| Expected turnover | Medium after fixed 10-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparsity or broad activation are review issues. |

## Candidate Registry

| signal_name                        | family                          | run_id                                | research_status                    | mechanism_thesis                                                                            | drawdown_pressure_definition                                                   | stabilization_confirmation_logic                                                                                            | differs_from_inventory                                                                                      | differs_from_reversal_momentum                                                             | expected_activation_state     | expected_horizon                              | expected_turnover_profile   | expected_active_coverage   |
|:-----------------------------------|:--------------------------------|:--------------------------------------|:-----------------------------------|:--------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:------------------------------|:----------------------------------------------|:----------------------------|:---------------------------|
| drawdown_pressure_stabilization_10 | drawdown_pressure_stabilization | drawdown_pressure_stabilization_10_v1 | TRACK_B_EXPANSION_V5_RESEARCH_ONLY | Shorter-horizon repair from stabilizing downside pressure during drawdown-pressure regimes. | Benchmark drawdown acceleration or negative benchmark drawdown/trend pressure. | Residual downside pressure reduction, contained range, residual vol normalization, close support, and sufficient liquidity. | Drawdown-pressure gate rather than participation, breadth, liquidity repair, or h20 volatility compression. | Avoids extreme damage and neutralizes reversal, momentum, and residual momentum exposures. | DRAWDOWN_PRESSURE_STABILIZING | h10 primary; h5/h15 secondary; h20 diagnostic | medium                      | medium                     |

## Component Diagnostics

| component                    |   finite_pct |   mean_abs |
|:-----------------------------|-------------:|-----------:|
| downside_pressure_reduction  |     0.977922 | 0.499043   |
| pressure_present_not_extreme |     0.978801 | 0.332953   |
| not_short_chase              |     0.985951 | 0.499287   |
| range_containment            |     0.969149 | 0.247826   |
| residual_vol_normalization   |     0.977943 | 0.499126   |
| close_support                |     0.98702  | 0.501034   |
| liquidity_sufficient         |     0.985161 | 0.501244   |
| drawdown_pressure_gate       |     1        | 0.0843661  |
| stabilization_quality        |     0.967113 | 0.00371259 |
| final_signal                 |     0.959386 | 0.0535702  |

## Structural Quality

| signal_name                        |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:-----------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| drawdown_pressure_stabilization_10 |   2098 |       478 |     0.0406145 |     0.959386 |        0.971401 |               0.959386 |           0 |       0.00925897 |              0 |       0.602877 |               0.20287 |            210 |            0.100095 |                       32 |               0.989839 |

## Multi-Horizon IC

| signal_name                        |   horizon |     mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:-----------------------------------|----------:|------------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| drawdown_pressure_stabilization_10 |         1 | -0.00249814 |    0.00249814 | -0.039831 |    0.039831 |           0.490244 |       410 |             10 | False             |
| drawdown_pressure_stabilization_10 |         5 | -0.0062444  |    0.0062444  | -0.105198 |    0.105198 |           0.443902 |       410 |             10 | False             |
| drawdown_pressure_stabilization_10 |        10 | -0.0104918  |    0.0104918  | -0.173918 |    0.173918 |           0.441463 |       410 |             10 | True              |
| drawdown_pressure_stabilization_10 |        15 | -0.0102204  |    0.0102204  | -0.173009 |    0.173009 |           0.44878  |       410 |             10 | False             |
| drawdown_pressure_stabilization_10 |        20 | -0.0100256  |    0.0100256  | -0.185962 |    0.185962 |           0.453659 |       410 |             10 | False             |

## h5 / h10 / h15 / h20 Behavior

| signal_name                        |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:-----------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| drawdown_pressure_stabilization_10 |         5 | -0.0062444 |     0.0062444 | -0.105198 |    0.105198 |           0.443902 |       410 |             10 | False             |
| drawdown_pressure_stabilization_10 |        10 | -0.0104918 |     0.0104918 | -0.173918 |    0.173918 |           0.441463 |       410 |             10 | True              |
| drawdown_pressure_stabilization_10 |        15 | -0.0102204 |     0.0102204 | -0.173009 |    0.173009 |           0.44878  |       410 |             10 | False             |
| drawdown_pressure_stabilization_10 |        20 | -0.0100256 |     0.0100256 | -0.185962 |    0.185962 |           0.453659 |       410 |             10 | False             |

## WFV-Style Diagnostics

| signal_name                        |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:-----------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| drawdown_pressure_stabilization_10 |        10 |           4 |               -0.0105037 |               -1.09675 |             0 |                  1 |               0.559295 |

## WFV Window Detail

| signal_name                        |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:-----------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| drawdown_pressure_stabilization_10 |        10 |        1 | 2018-11-29   | 2020-09-02 |   -0.0158142   |   -0.251272  |           0.456311 |              103 |
| drawdown_pressure_stabilization_10 |        10 |        2 | 2020-09-03   | 2021-02-01 |   -0.000286005 |   -0.0204931 |           0.456311 |              103 |
| drawdown_pressure_stabilization_10 |        10 |        3 | 2021-02-02   | 2022-07-25 |   -0.002416    |   -0.0427065 |           0.441176 |              102 |
| drawdown_pressure_stabilization_10 |        10 |        4 | 2022-07-26   | 2025-12-30 |   -0.0234988   |   -0.283651  |           0.411765 |              102 |

## Baseline And Inventory Similarity

| signal_name                        | top_comparison          |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   price_rank_reversal_5_corr |   price_rank_reversal_20_corr |   residual_momentum_10_corr |   residual_momentum_20_corr |   drawdown_pressure_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   max_price_momentum_corr |   max_price_reversal_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_low_volatility_corr |
|:-----------------------------------|:------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-----------------------------:|------------------------------:|----------------------------:|----------------------------:|-------------------------------:|-----------------------------------:|--------------------------------------:|--------------------------------:|-----------------------------------------:|--------------------------:|--------------------------:|----------------------------------------:|-----------------------------:|--------------------------:|
| drawdown_pressure_stabilization_10 | drawdown_pressure_proxy |                0.114586 |                  0.0332745 |                0.0661934 |                    0.109334 |             0.109334 |           0.0146874 |          0.00492345 |                  0.000264845 |                     0.0111696 |                     0.0204505 |                     0.0146874 |                    0.00492345 |                  0.000264835 |                     0.0146874 |                   0.0111696 |                   0.0146874 |                       0.114586 |                         0.00932393 |                             0.0297921 |                       0.0575929 |                                0.0865155 |                 0.0204505 |                 0.0146874 |                               0.0661934 |                     0.109334 |                 0.0865155 |

## Drawdown / Stress Attribution

| signal_name                        |   horizon | state                                     |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-----------------------------------|----------:|:------------------------------------------|----------:|------------:|-----------:|-------------------:|
| drawdown_pressure_stabilization_10 |        10 | panic_liquidity_stress                    |        25 |  0.0150846  |  0.267963  |           0.64     |
| drawdown_pressure_stabilization_10 |        10 | drawdown_acceleration                     |        53 | -0.00222121 | -0.0324166 |           0.490566 |
| drawdown_pressure_stabilization_10 |        10 | volatility_spike                          |        99 | -0.00321539 | -0.0531037 |           0.505051 |
| drawdown_pressure_stabilization_10 |        10 | CONTAINED_DISPERSION_DRAWDOWN             |       187 | -0.00905475 | -0.125525  |           0.459893 |
| drawdown_pressure_stabilization_10 |        10 | DRAWDOWN_PRESSURE_NOT_WEAK_BREADTH_REPAIR |       211 | -0.011378   | -0.165222  |           0.440758 |
| drawdown_pressure_stabilization_10 |        10 | ACTIVE_HOSTILE_OR_STRESS                  |       312 | -0.0114621  | -0.179667  |           0.410256 |
| drawdown_pressure_stabilization_10 |        10 | HOSTILE_OR_STRESS                         |       312 | -0.0114621  | -0.179667  |           0.410256 |
| drawdown_pressure_stabilization_10 |        10 | ACTIVE_DRAWDOWN_PRESSURE                  |       227 | -0.0119325  | -0.169528  |           0.444934 |
| drawdown_pressure_stabilization_10 |        10 | DRAWDOWN_PRESSURE_STABILIZING             |       111 | -0.0133043  | -0.156116  |           0.495495 |
| drawdown_pressure_stabilization_10 |        10 | DRAWDOWN_STABILIZATION_WITH_QUALITY       |       111 | -0.0133043  | -0.156116  |           0.495495 |
| drawdown_pressure_stabilization_10 |        10 | weak_breadth                              |        75 | -0.0155923  | -0.211925  |           0.4      |
| drawdown_pressure_stabilization_10 |        10 | DOWNSIDE_PRESSURE_REDUCING                |       143 | -0.0176728  | -0.218227  |           0.454545 |
| drawdown_pressure_stabilization_10 |        10 | recovery_phase                            |        70 | -0.020776   | -0.281123  |           0.428571 |
| drawdown_pressure_stabilization_10 |        10 | high_dispersion_rotation                  |        92 | -0.0264832  | -0.383635  |           0.423913 |
| drawdown_pressure_stabilization_10 |        10 | trend_transition                          |       106 | -0.0351979  | -0.462189  |           0.301887 |

## Stress / Regime Attribution

| signal_name                        |   horizon | state                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:-----------------------------------|----------:|:-------------------------|----------:|------------:|-----------:|-------------------:|
| drawdown_pressure_stabilization_10 |        10 | panic_liquidity_stress   |        25 |  0.0150846  |  0.267963  |           0.64     |
| drawdown_pressure_stabilization_10 |        10 | drawdown_acceleration    |        53 | -0.00222121 | -0.0324166 |           0.490566 |
| drawdown_pressure_stabilization_10 |        10 | volatility_spike         |        99 | -0.00321539 | -0.0531037 |           0.505051 |
| drawdown_pressure_stabilization_10 |        10 | weak_breadth             |        75 | -0.0155923  | -0.211925  |           0.4      |
| drawdown_pressure_stabilization_10 |        10 | recovery_phase           |        70 | -0.020776   | -0.281123  |           0.428571 |
| drawdown_pressure_stabilization_10 |        10 | high_dispersion_rotation |        92 | -0.0264832  | -0.383635  |           0.423913 |
| drawdown_pressure_stabilization_10 |        10 | trend_transition         |       106 | -0.0351979  | -0.462189  |           0.301887 |

## Sample-Size Sanity

| state                                     |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:------------------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| ACTIVE_DRAWDOWN_PRESSURE                  |           836 |          0.398475  |                           172 |                     0.0819828 |
| DRAWDOWN_PRESSURE_STABILIZING             |           177 |          0.0843661 |                           105 |                     0.0500477 |
| DRAWDOWN_STABILIZATION_WITH_QUALITY       |           177 |          0.0843661 |                           105 |                     0.0500477 |
| DRAWDOWN_PRESSURE_NOT_WEAK_BREADTH_REPAIR |           780 |          0.371783  |                           156 |                     0.0743565 |
| DOWNSIDE_PRESSURE_REDUCING                |           287 |          0.136797  |                           133 |                     0.0633937 |
| CONTAINED_DISPERSION_DRAWDOWN             |           556 |          0.265014  |                           138 |                     0.0657769 |
| ACTIVE_HOSTILE_OR_STRESS                  |          1264 |          0.602479  |                           199 |                     0.0948522 |
| HOSTILE_OR_STRESS                         |          1264 |          0.602479  |                           199 |                     0.0948522 |
| drawdown_acceleration                     |           375 |          0.178742  |                            32 |                     0.0152526 |
| volatility_spike                          |           404 |          0.192564  |                            91 |                     0.0433746 |
| panic_liquidity_stress                    |           187 |          0.0891325 |                            25 |                     0.0119161 |
| trend_transition                          |           580 |          0.276454  |                            85 |                     0.0405148 |
| recovery_phase                            |           196 |          0.0934223 |                            57 |                     0.0271687 |
| high_dispersion_rotation                  |           584 |          0.27836   |                            72 |                     0.0343184 |
| weak_breadth                              |           508 |          0.242135  |                            46 |                     0.0219256 |
| SIGNAL_ACTIVE                             |           210 |          0.100095  |                           210 |                     0.100095  |

## Candidate Decision

| signal_name                        | family                          |   best_horizon |    mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |     ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_reversal_corr |   max_price_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   drawdown_pressure_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_drawdown_state_count |   best_drawdown_state_ic |   best_hostile_stress_state_ic | status          | review_issues                                                                                                                     |
|:-----------------------------------|:--------------------------------|---------------:|-----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|----------------------------------------:|-----------------------------:|--------------------:|--------------------------:|--------------------:|--------------------------:|--------------------------:|-------------------------------:|-----------------------------------:|--------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|--------------------------------:|-------------------------:|-------------------------------:|:----------------|:----------------------------------------------------------------------------------------------------------------------------------|
| drawdown_pressure_stabilization_10 | drawdown_pressure_stabilization |             10 | -0.0104918 |   -0.0062444 |              0.443902 |    -0.0104918 |               0.441463 |    -0.0102204 |                0.44878 |    -0.0100256 |               0.453659 | -0.173918 |           0.441463 |       0.00925897 |     0.0406145 |            0.100095 |                0.114586 |             0.109334 |                               0.0661934 |                     0.109334 |           0.0146874 |                 0.0146874 |          0.00492345 |                 0.0204505 |                 0.0865155 |                       0.114586 |                         0.00932393 |                             0.0297921 |                  0.0332745 |                0.0661934 |                    0.109334 |                 0 |                      1 |               -1.09675 |                               0 |              -0.00905475 |                      0.0150846 | REJECT_RESEARCH | weak_h10_ic; weak_h10_positive_ic_rate; weak_primary_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_drawdown_state_support |

## Specific Diagnostic Answers

- Genuinely drawdown-pressure stabilization: positive drawdown-state count was `0` and best drawdown-state IC was `-0.009055`.
- Reversal risk: max price-reversal correlation was `0.014687` and max generic reversal correlation was `0.014687`.
- Momentum risk: max price-momentum correlation was `0.020451` and max generic momentum correlation was `0.004923`.
- Breadth/participation repair risk: max breadth/participation repair correlation was `0.066193`.
- Volatility/stress stabilization risk: max volatility/stress correlation was `0.109334`.
- Inventory overlap risk: max inventory correlation was `0.109334`.
- h20 dependence risk: h10 IC was `-0.010492` and h20 IC was `-0.010026`.
- Sparse or broad activation risk: active date ratio was `0.100095`.
- Turnover risk: turnover proxy was `0.009259`.
- Directional stability: WFV-style persistence/sign consistency were `0.000000` / `1.000000`.
- h5/h10/h15/h20 profile: h5 `-0.006244`, h10 `-0.010492`, h15 `-0.010220`, h20 `-0.010026`.

## Recommended Next Step

`drawdown_pressure_stabilization_10` should be rejected in this formulation before moving to the next Expansion v5 concept.
