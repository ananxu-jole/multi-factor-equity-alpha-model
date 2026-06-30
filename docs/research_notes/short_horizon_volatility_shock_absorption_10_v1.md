# Short Horizon Volatility Shock Absorption 10 v1

## Executive Takeaway

This research-only run tested one simple formulation of `short_horizon_volatility_shock_absorption_10` under the isolated run namespace `short_horizon_volatility_shock_absorption_10_v1`.

The formulation tests whether assets that absorb a recent volatility shock can produce a true h10 repair/stabilization edge without becoming broad volatility compression, idiosyncratic stress containment, reversal, momentum, or participation/breadth repair.

Final classification: `CONDITIONAL_REFINEMENT_CANDIDATE`
Primary review issues: `h10_below_validation_ready_floor; best_horizon_h5_not_h10`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, large refinement search, broad discovery, or implementation of other Expansion v5 concepts was performed.

## Source Context

- Expansion v5 design screen: `docs/research_notes/track_b_expansion_v5_design_screening.md`
- Drawdown pressure stabilization v1: `docs/research_notes/drawdown_pressure_stabilization_10_v1.md`
- Idiosyncratic stress containment v1: `docs/research_notes/idiosyncratic_stress_containment_10_v1.md`
- Conditional Alpha Inventory Monitoring v2: `docs/research_notes/conditional_alpha_inventory_monitoring_v2.md`
- Conditional Alpha Inventory v2 Governance Update: `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Expansion v4 closeout review: `docs/research_notes/track_b_expansion_v4_closeout_review.md`
- Inventory Ecosystem Review v1: `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.

## Mechanism Definition

| Field | Definition |
| --- | --- |
| Mechanism thesis | After a volatility/range shock, stocks that quickly absorb the shock without disorderly follow-through may stabilize over h5-h10 before h20 compression signals dominate. |
| Volatility shock definition | Recent benchmark volatility spike or cross-sectional range expansion with elevated individual range/residual-volatility context. |
| Absorption/stabilization logic | Fast range contraction, residual volatility contraction, rank stabilization, non-extreme price path, close support, and sufficient liquidity. |
| Difference from broad volatility compression | This targets short-horizon shock absorption after a recent shock rather than h20 post-stress compression. |
| Difference from idiosyncratic stress containment | Activation is market/range-volatility-shock led, not broad asset-level residual stress exposure. |
| Difference from reversal/momentum | The signal avoids extreme loser/winner ranking and neutralizes reversal, momentum, and residual momentum exposures. |
| Difference from price momentum | Price-rank momentum and residual momentum exposures are neutralized. |
| Why it may reduce h20 concentration | The mechanism is explicitly h5-h10 shock absorption and uses a 10-day rebalance interval, with h20 treated as dependency risk. |
| Expected activation semantics | Recent volatility shock with fast range/residual-volatility absorption and without weak-breadth repair as the primary driver. |
| Expected horizon | h10 primary; h5 and h15 secondary; h20 diagnostic. |
| Expected turnover | Medium after fixed 10-day rebalance control. |
| Expected active coverage | Medium conditional coverage; sparsity or broad activation are review issues. |

## Candidate Registry

| signal_name                                  | family                                    | run_id                                          | research_status                    | mechanism_thesis                                                              | volatility_shock_definition                                                                                       | absorption_stabilization_logic                                                                                 | differs_from_inventory                                                             | differs_from_reversal_momentum                                                                     | expected_activation_state   | expected_horizon                              | expected_turnover_profile   | expected_active_coverage   |
|:---------------------------------------------|:------------------------------------------|:------------------------------------------------|:-----------------------------------|:------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|:----------------------------|:----------------------------------------------|:----------------------------|:---------------------------|
| short_horizon_volatility_shock_absorption_10 | short_horizon_volatility_shock_absorption | short_horizon_volatility_shock_absorption_10_v1 | TRACK_B_EXPANSION_V5_RESEARCH_ONLY | Shorter-horizon repair from absorption of recent volatility and range shocks. | Recent benchmark volatility spike or market range expansion with individual range and residual volatility stress. | Fast range contraction, residual vol contraction, rank stabilization, close support, and sufficient liquidity. | Short-horizon shock absorption rather than h20 post-stress volatility compression. | Avoids extreme winners/losers and neutralizes reversal, momentum, and residual momentum exposures. | VOLATILITY_SHOCK_ABSORBING  | h10 primary; h5/h15 secondary; h20 diagnostic | medium                      | medium                     |

## Component Diagnostics

| component                 |   finite_pct |    mean_abs |
|:--------------------------|-------------:|------------:|
| shock_present             |     0.968528 | 0.298677    |
| fast_absorption           |     0.981535 | 0.293       |
| no_panic_extension        |     0.983568 | 0.285261    |
| residual_shock_absorption |     0.983568 | 0.285261    |
| range_containment         |     0.969149 | 0.34357     |
| rank_stabilization        |     0.980712 | 0.498503    |
| close_support             |     0.98702  | 0.501034    |
| liquidity_sufficient      |     0.985161 | 0.501244    |
| volatility_shock_gate     |     1        | 0.0220144   |
| absorption_quality        |     0.967053 | 0.000856263 |
| final_signal              |     0.959386 | 0.0397843   |

## Structural Quality

| signal_name                                  |   rows |   columns |   missing_pct |   finite_pct |   date_coverage |   ticker_coverage_mean |   inf_count |   turnover_proxy |   turnover_p95 |   turnover_max |   concentration_proxy |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:---------------------------------------------|-------:|----------:|--------------:|-------------:|----------------:|-----------------------:|------------:|-----------------:|---------------:|---------------:|----------------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| short_horizon_volatility_shock_absorption_10 |   2098 |       478 |     0.0406145 |     0.959386 |        0.971401 |               0.959386 |           0 |       0.00664126 |              0 |          0.284 |              0.201892 |            400 |            0.190658 |                       56 |               0.989435 |

## Multi-Horizon IC

| signal_name                                  |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:---------------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| short_horizon_volatility_shock_absorption_10 |         1 | 0.00676453 |    0.00676453 | 0.0818507 |   0.0818507 |           0.545    |       400 |              5 | False             |
| short_horizon_volatility_shock_absorption_10 |         5 | 0.0110449  |    0.0110449  | 0.14211   |   0.14211   |           0.5825   |       400 |              5 | True              |
| short_horizon_volatility_shock_absorption_10 |        10 | 0.00855832 |    0.00855832 | 0.109254  |   0.109254  |           0.572864 |       398 |              5 | False             |
| short_horizon_volatility_shock_absorption_10 |        15 | 0.00603389 |    0.00603389 | 0.0789551 |   0.0789551 |           0.569975 |       393 |              5 | False             |
| short_horizon_volatility_shock_absorption_10 |        20 | 0.00352201 |    0.00352201 | 0.0442991 |   0.0442991 |           0.533505 |       388 |              5 | False             |

## h5 / h10 / h15 / h20 Behavior

| signal_name                                  |   horizon |    mean_ic |   abs_mean_ic |     ic_ir |   abs_ic_ir |   positive_ic_rate |   n_dates |   best_horizon | is_best_horizon   |
|:---------------------------------------------|----------:|-----------:|--------------:|----------:|------------:|-------------------:|----------:|---------------:|:------------------|
| short_horizon_volatility_shock_absorption_10 |         5 | 0.0110449  |    0.0110449  | 0.14211   |   0.14211   |           0.5825   |       400 |              5 | True              |
| short_horizon_volatility_shock_absorption_10 |        10 | 0.00855832 |    0.00855832 | 0.109254  |   0.109254  |           0.572864 |       398 |              5 | False             |
| short_horizon_volatility_shock_absorption_10 |        15 | 0.00603389 |    0.00603389 | 0.0789551 |   0.0789551 |           0.569975 |       393 |              5 | False             |
| short_horizon_volatility_shock_absorption_10 |        20 | 0.00352201 |    0.00352201 | 0.0442991 |   0.0442991 |           0.533505 |       388 |              5 | False             |

## WFV-Style Diagnostics

| signal_name                                  |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:---------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| short_horizon_volatility_shock_absorption_10 |         5 |           4 |                0.0110449 |                1.25322 |          0.75 |               0.75 |               0.493203 |

## WFV Window Detail

| signal_name                                  |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:---------------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| short_horizon_volatility_shock_absorption_10 |         5 |        1 | 2018-11-29   | 2020-07-02 |    -0.00145378 |   -0.0151661 |               0.49 |              100 |
| short_horizon_volatility_shock_absorption_10 |         5 |        2 | 2020-07-06   | 2022-06-13 |     0.0232236  |    0.297287  |               0.6  |              100 |
| short_horizon_volatility_shock_absorption_10 |         5 |        3 | 2022-06-14   | 2024-06-25 |     0.00945803 |    0.141908  |               0.6  |              100 |
| short_horizon_volatility_shock_absorption_10 |         5 |        4 | 2024-08-22   | 2026-04-27 |     0.0129519  |    0.201827  |               0.64 |              100 |

## Baseline And Inventory Similarity

| signal_name                                  | top_comparison                   |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   price_rank_momentum_5_corr |   price_rank_momentum_10_corr |   price_rank_momentum_15_corr |   price_rank_momentum_20_corr |   price_rank_momentum_60_corr |   price_rank_reversal_5_corr |   price_rank_reversal_20_corr |   residual_momentum_10_corr |   residual_momentum_20_corr |   drawdown_pressure_proxy_corr |   idiosyncratic_stress_proxy_corr |   short_vol_shock_absorption_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   simple_low_volatility_20_corr |   simple_low_residual_volatility_20_corr |   max_price_momentum_corr |   max_price_reversal_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_drawdown_pressure_corr |   max_idiosyncratic_stress_corr |   max_vol_shock_absorption_corr |   max_low_volatility_corr |
|:---------------------------------------------|:---------------------------------|------------------------:|---------------------------:|-------------------------:|----------------------------:|---------------------:|--------------------:|--------------------:|-----------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-----------------------------:|------------------------------:|----------------------------:|----------------------------:|-------------------------------:|----------------------------------:|----------------------------------------:|-----------------------------------:|--------------------------------------:|--------------------------------:|-----------------------------------------:|--------------------------:|--------------------------:|----------------------------------------:|-----------------------------:|-----------------------------:|--------------------------------:|--------------------------------:|--------------------------:|
| short_horizon_volatility_shock_absorption_10 | short_vol_shock_absorption_proxy |                0.168854 |                  0.0390882 |               0.00212861 |                    0.117222 |             0.117222 |           0.0028978 |          0.00636768 |                   0.00656899 |                    0.00721618 |                    0.00468613 |                    0.00087044 |                    0.00636768 |                   0.00656897 |                   0.000870415 |                  0.00721618 |                  0.00087044 |                     0.00240985 |                          0.133234 |                                0.168854 |                          0.0039903 |                             0.0931009 |                       0.0624277 |                                0.0768115 |                0.00721618 |                0.00656897 |                               0.0390882 |                     0.117222 |                   0.00240985 |                        0.133234 |                        0.168854 |                 0.0768115 |

## Volatility-Shock Attribution

| signal_name                                  |   horizon | state                                    |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|:---------------------------------------------|----------:|:-----------------------------------------|----------:|-----------:|----------:|-------------------:|
| short_horizon_volatility_shock_absorption_10 |         5 | recovery_phase                           |        55 | 0.0264746  | 0.27619   |           0.563636 |
| short_horizon_volatility_shock_absorption_10 |         5 | trend_transition                         |       140 | 0.025215   | 0.344488  |           0.664286 |
| short_horizon_volatility_shock_absorption_10 |         5 | drawdown_acceleration                    |        75 | 0.0247187  | 0.31746   |           0.64     |
| short_horizon_volatility_shock_absorption_10 |         5 | VOLATILITY_SHOCK_ABSORBING               |       259 | 0.0157611  | 0.197559  |           0.602317 |
| short_horizon_volatility_shock_absorption_10 |         5 | VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |       259 | 0.0157611  | 0.197559  |           0.602317 |
| short_horizon_volatility_shock_absorption_10 |         5 | CONTAINED_DISPERSION_VOL_SHOCK           |       270 | 0.0154791  | 0.194961  |           0.607407 |
| short_horizon_volatility_shock_absorption_10 |         5 | VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |       221 | 0.0151272  | 0.183772  |           0.59276  |
| short_horizon_volatility_shock_absorption_10 |         5 | MARKET_VOL_ABSORBING                     |       301 | 0.0142998  | 0.17946   |           0.601329 |
| short_horizon_volatility_shock_absorption_10 |         5 | ACTIVE_HOSTILE_OR_STRESS                 |       367 | 0.0136605  | 0.175379  |           0.599455 |
| short_horizon_volatility_shock_absorption_10 |         5 | BROAD_HOSTILE_OR_STRESS                  |       367 | 0.0136605  | 0.175379  |           0.599455 |
| short_horizon_volatility_shock_absorption_10 |         5 | HOSTILE_OR_STRESS                        |       367 | 0.0136605  | 0.175379  |           0.599455 |
| short_horizon_volatility_shock_absorption_10 |         5 | RECENT_VOLATILITY_SHOCK                  |       366 | 0.0135981  | 0.17436   |           0.598361 |
| short_horizon_volatility_shock_absorption_10 |         5 | weak_breadth                             |       120 | 0.0127547  | 0.183948  |           0.625    |
| short_horizon_volatility_shock_absorption_10 |         5 | high_dispersion_rotation                 |       111 | 0.0126754  | 0.159184  |           0.576577 |
| short_horizon_volatility_shock_absorption_10 |         5 | panic_liquidity_stress                   |        51 | 0.00562223 | 0.0786063 |           0.529412 |
| short_horizon_volatility_shock_absorption_10 |         5 | VOLATILITY_SHOCK_ACTIVE                  |       183 | 0.00422099 | 0.0549894 |           0.562842 |

## Stress / Regime Attribution

| signal_name                                  |   horizon | state                    |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:---------------------------------------------|----------:|:-------------------------|----------:|------------:|-----------:|-------------------:|
| short_horizon_volatility_shock_absorption_10 |         5 | recovery_phase           |        55 |  0.0264746  |  0.27619   |           0.563636 |
| short_horizon_volatility_shock_absorption_10 |         5 | trend_transition         |       140 |  0.025215   |  0.344488  |           0.664286 |
| short_horizon_volatility_shock_absorption_10 |         5 | drawdown_acceleration    |        75 |  0.0247187  |  0.31746   |           0.64     |
| short_horizon_volatility_shock_absorption_10 |         5 | weak_breadth             |       120 |  0.0127547  |  0.183948  |           0.625    |
| short_horizon_volatility_shock_absorption_10 |         5 | high_dispersion_rotation |       111 |  0.0126754  |  0.159184  |           0.576577 |
| short_horizon_volatility_shock_absorption_10 |         5 | panic_liquidity_stress   |        51 |  0.00562223 |  0.0786063 |           0.529412 |
| short_horizon_volatility_shock_absorption_10 |         5 | volatility_spike         |       147 | -0.00321714 | -0.0436488 |           0.503401 |

## Sample-Size Sanity

| state                                    |   state_dates |   state_date_ratio |   signal_active_overlap_dates |   signal_active_overlap_ratio |
|:-----------------------------------------|--------------:|-------------------:|------------------------------:|------------------------------:|
| VOLATILITY_SHOCK_ACTIVE                  |           663 |          0.316015  |                           183 |                     0.0872259 |
| RECENT_VOLATILITY_SHOCK                  |          1042 |          0.496663  |                           366 |                     0.174452  |
| VOLATILITY_SHOCK_ABSORBING               |           421 |          0.200667  |                           259 |                     0.123451  |
| VOLATILITY_SHOCK_ABSORPTION_WITH_QUALITY |           421 |          0.200667  |                           259 |                     0.123451  |
| VOLATILITY_SHOCK_OUTSIDE_WEAK_BREADTH    |           457 |          0.217827  |                           221 |                     0.105338  |
| CONTAINED_DISPERSION_VOL_SHOCK           |           455 |          0.216873  |                           270 |                     0.128694  |
| MARKET_VOL_ABSORBING                     |           639 |          0.304576  |                           301 |                     0.14347   |
| BROAD_HOSTILE_OR_STRESS                  |          1187 |          0.565777  |                           367 |                     0.174929  |
| ACTIVE_HOSTILE_OR_STRESS                 |          1187 |          0.565777  |                           367 |                     0.174929  |
| HOSTILE_OR_STRESS                        |          1187 |          0.565777  |                           367 |                     0.174929  |
| drawdown_acceleration                    |           375 |          0.178742  |                            75 |                     0.0357483 |
| volatility_spike                         |           404 |          0.192564  |                           147 |                     0.0700667 |
| panic_liquidity_stress                   |           187 |          0.0891325 |                            51 |                     0.0243089 |
| trend_transition                         |           580 |          0.276454  |                           140 |                     0.0667302 |
| recovery_phase                           |           196 |          0.0934223 |                            55 |                     0.0262154 |
| high_dispersion_rotation                 |           584 |          0.27836   |                           111 |                     0.0529075 |
| weak_breadth                             |           508 |          0.242135  |                           120 |                     0.0571973 |
| SIGNAL_ACTIVE                            |           400 |          0.190658  |                           400 |                     0.190658  |

## Candidate Decision

| signal_name                                  | family                                    |   best_horizon |   mean_ic |   h5_mean_ic |   h5_positive_ic_rate |   h10_mean_ic |   h10_positive_ic_rate |   h15_mean_ic |   h15_positive_ic_rate |   h20_mean_ic |   h20_positive_ic_rate |   ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   max_inventory_corr |   max_breadth_participation_repair_corr |   max_volatility_stress_corr |   max_drawdown_pressure_corr |   max_idiosyncratic_stress_corr |   max_vol_shock_absorption_corr |   max_reversal_corr |   max_price_reversal_corr |   max_momentum_corr |   max_price_momentum_corr |   max_low_volatility_corr |   drawdown_pressure_proxy_corr |   idiosyncratic_stress_proxy_corr |   short_vol_shock_absorption_proxy_corr |   active_breadth_repair_proxy_corr |   volatility_stabilization_proxy_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   inventory_volatility_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_volatility_shock_state_count |   best_volatility_shock_state_ic |   best_hostile_stress_state_ic | status                           | review_issues                                             |
|:---------------------------------------------|:------------------------------------------|---------------:|----------:|-------------:|----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------------:|-----------------------:|--------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------:|----------------------------------------:|-----------------------------:|-----------------------------:|--------------------------------:|--------------------------------:|--------------------:|--------------------------:|--------------------:|--------------------------:|--------------------------:|-------------------------------:|----------------------------------:|----------------------------------------:|-----------------------------------:|--------------------------------------:|---------------------------:|-------------------------:|----------------------------:|------------------:|-----------------------:|-----------------------:|----------------------------------------:|---------------------------------:|-------------------------------:|:---------------------------------|:----------------------------------------------------------|
| short_horizon_volatility_shock_absorption_10 | short_horizon_volatility_shock_absorption |              5 | 0.0110449 |    0.0110449 |                0.5825 |    0.00855832 |               0.572864 |    0.00603389 |               0.569975 |    0.00352201 |               0.533505 | 0.14211 |             0.5825 |       0.00664126 |     0.0406145 |            0.190658 |                0.168854 |             0.117222 |                               0.0390882 |                     0.117222 |                   0.00240985 |                        0.133234 |                        0.168854 |           0.0028978 |                0.00656897 |          0.00636768 |                0.00721618 |                 0.0768115 |                     0.00240985 |                          0.133234 |                                0.168854 |                          0.0039903 |                             0.0931009 |                  0.0390882 |               0.00212861 |                    0.117222 |              0.75 |                   0.75 |                1.25322 |                                       7 |                        0.0157611 |                      0.0247187 | CONDITIONAL_REFINEMENT_CANDIDATE | h10_below_validation_ready_floor; best_horizon_h5_not_h10 |

## Specific Diagnostic Answers

- Genuinely short-horizon volatility shock absorption: positive volatility-shock state count was `7` and best volatility-shock state IC was `0.015761`.
- Broad drawdown-pressure risk: max drawdown-pressure correlation was `0.002410`.
- Idiosyncratic stress similarity risk: max idiosyncratic-stress correlation was `0.133234`.
- Reversal risk: max price-reversal correlation was `0.006569` and max generic reversal correlation was `0.002898`.
- Momentum risk: max price-momentum correlation was `0.007216` and max generic momentum correlation was `0.006368`.
- Breadth/participation repair risk: max breadth/participation repair correlation was `0.039088`.
- Volatility/stress stabilization risk: max volatility/stress correlation was `0.117222`.
- Inventory overlap risk: max inventory correlation was `0.117222`.
- h20 dependence risk: h10 IC was `0.008558` and h20 IC was `0.003522`.
- Sparse or broad activation risk: active date ratio was `0.190658`.
- Turnover risk: turnover proxy was `0.006641`.
- Directional stability: WFV-style persistence/sign consistency were `0.750000` / `0.750000`.
- h5/h10/h15/h20 profile: h5 `0.011045`, h10 `0.008558`, h15 `0.006034`, h20 `0.003522`.

## Recommended Next Step

`short_horizon_volatility_shock_absorption_10` should receive a narrow refinement diagnostics pass focused on h10 strength, volatility-inventory separation, and activation coverage.
