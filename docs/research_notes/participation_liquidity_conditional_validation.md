# Participation Liquidity Conditional Validation

## Executive Takeaway

This formal research-only conditional validation pass tested `participation_liquidity_state_shift_20_60` under `participation_liquidity_conditional_validation_v1`.

Final classification: `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`.

The strongest validated variant was `rank_persist_10_state_TREND_HOSTILE_zero` with h20 mean IC 0.028418, turnover 0.096397, active coverage 0.346997, effective WFV-style IC IR 2.623031, and baseline correlation 0.269307.

No production logic, gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, production registration, or Conditional-Alpha production paths were changed.

## Scope

- Selected variants: 18
- Source: focused refinement candidates marked `candidate_ready`, plus broad `rebalance_20` reference.
- Validation mode: research-only, isolated artifacts.

## Top Strict Validation Results

| variant_name                                           |   best_horizon |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   effective_test_ic_ir |   persistence |   sign_consistency |   h20_one_window_dominance |   turnover_proxy |   active_date_coverage |   active_window_coverage |   max_abs_baseline_corr |   max_abs_peer_corr | neighbor_support   | strict_pass   |   validation_score |
|:-------------------------------------------------------|---------------:|--------------:|------------:|-----------------------:|-----------------------:|--------------:|-------------------:|---------------------------:|-----------------:|-----------------------:|-------------------------:|------------------------:|--------------------:|:-------------------|:--------------|-------------------:|
| rank_persist_10_state_TREND_HOSTILE_zero               |             10 |     0.0284181 |    0.211294 |               0.568681 |               2.62303  |          1    |               1    |                   0.568812 |        0.096397  |               0.346997 |                        1 |                0.269307 |            0.833621 | True               | True          |            5.95529 |
| rebalance_10_state_WEAK_BREADTH_zero                   |             20 |     0.0244101 |    0.197244 |               0.590379 |               2.35292  |          1    |               1    |                   0.386955 |        0.0545552 |               0.327455 |                        1 |                0.198669 |            0.979701 | True               | True          |            5.60429 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero         |             20 |     0.0242128 |    0.19885  |               0.591608 |               2.24677  |          1    |               1    |                   0.40133  |        0.0592233 |               0.341277 |                        1 |                0.203465 |            0.979701 | True               | True          |            5.53797 |
| rebalance_20                                           |             20 |     0.0212341 |    0.201609 |               0.583906 |               1.62128  |          1    |               1    |                   0.486213 |        0.0329729 |               0.980934 |                        1 |                0.213316 |            0.565509 | True               | True          |            5.01359 |
| rebalance_10_state_HOSTILE_OR_WEAK_BREADTH_zero        |             20 |     0.0228371 |    0.188933 |               0.571114 |               2.91223  |          1    |               1    |                   0.395551 |        0.0710497 |               0.432793 |                        1 |                0.212403 |            0.998895 | False              | False         |            5.59797 |
| rebalance_10_state_TREND_HOSTILE_zero                  |             20 |     0.022271  |    0.180909 |               0.560109 |               2.93869  |          1    |               1    |                   0.351717 |        0.058323  |               0.348904 |                        1 |                0.193201 |            0.897476 | False              | False         |            5.5729  |
| rebalance_10_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero |             20 |     0.0226298 |    0.187292 |               0.569857 |               2.83023  |          1    |               1    |                   0.400621 |        0.0706026 |               0.433746 |                        1 |                0.212981 |            0.998895 | False              | False         |            5.54617 |
| smooth_5_state_TREND_HOSTILE_zero                      |             20 |     0.0279964 |    0.20847  |               0.55814  |               1.06028  |          1    |               1    |                   0.6567   |        0.0595669 |               0.348427 |                        1 |                0.307803 |            0.896949 | True               | False         |            5.35124 |
| smooth_5_state_HOSTILE_OR_WEAK_BREADTH_zero            |             20 |     0.0228874 |    0.168306 |               0.554084 |               1.2243   |          1    |               1    |                   0.594465 |        0.0735705 |               0.432316 |                        1 |                0.345361 |            0.998807 | False              | False         |            4.87646 |
| rank_persist_10_state_WEAK_BREADTH_zero                |             20 |     0.0227163 |    0.157187 |               0.549563 |               1.19277  |          1    |               1    |                   0.590216 |        0.0902015 |               0.327455 |                        1 |                0.273061 |            0.978348 | False              | False         |            4.86437 |
| smooth_5_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero     |             20 |     0.0226651 |    0.166753 |               0.552863 |               1.20681  |          1    |               1    |                   0.599558 |        0.0733218 |               0.43327  |                        1 |                0.345866 |            0.998807 | False              | False         |            4.84561 |
| rank_persist_10_state_STRESS_OR_WEAK_BREADTH_zero      |             20 |     0.0219877 |    0.154498 |               0.546985 |               1.16783  |          1    |               1    |                   0.591542 |        0.0959022 |               0.340324 |                        1 |                0.279807 |            0.978348 | False              | False         |            4.7708  |
| rank_persist_10_state_LOW_DISPERSION_zero              |             20 |     0.0248475 |    0.196527 |               0.56875  |               0.596519 |          0.75 |               0.75 |                   0.290193 |        0.0945384 |               0.305052 |                        1 |                0.278547 |            0.839631 | False              | False         |            4.45592 |
| rebalance_10_state_LOW_DISPERSION_zero                 |             20 |     0.0217925 |    0.181312 |               0.590625 |               0.528802 |          0.75 |               0.75 |                   0.32619  |        0.0642077 |               0.305052 |                        1 |                0.208978 |            0.649498 | False              | False         |            4.20471 |
| smooth_5_state_WEAK_BREADTH_zero                       |             20 |     0.0217112 |    0.153354 |               0.546647 |               0.905165 |          0.75 |               0.75 |                   0.543777 |        0.0561824 |               0.327455 |                        1 |                0.315711 |            0.978623 | False              | False         |            4.1846  |
| smooth_5_state_LOW_DISPERSION_zero                     |             20 |     0.0211921 |    0.161773 |               0.559375 |               0.468182 |          0.75 |               0.75 |                   0.293692 |        0.0622085 |               0.305052 |                        1 |                0.318427 |            0.839631 | False              | False         |            4.0476  |
| smooth_5_state_STRESS_OR_WEAK_BREADTH_zero             |             20 |     0.02048   |    0.14672  |               0.542017 |               0.893321 |          0.75 |               0.75 |                   0.538933 |        0.0605776 |               0.340801 |                        1 |                0.32269  |            0.978623 | False              | False         |            4.04602 |
| rebalance_10                                           |             20 |     0.0165177 |    0.147513 |               0.561335 |               1.2025   |          0.75 |               0.75 |                   0.489508 |        0.0591847 |               0.980934 |                        1 |                0.319812 |            0.664965 | False              | False         |            3.79251 |

## Focus Variant Comparison

| variant_name                                   |   best_horizon |   h20_mean_ic |   h20_positive_ic_rate |   effective_test_ic_ir |   persistence |   sign_consistency |   turnover_proxy |   active_date_coverage |   max_abs_baseline_corr | strict_pass   |
|:-----------------------------------------------|---------------:|--------------:|-----------------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------------:|------------------------:|:--------------|
| rank_persist_10_state_TREND_HOSTILE_zero       |             10 |     0.0284181 |               0.568681 |                2.62303 |             1 |                  1 |        0.096397  |               0.346997 |                0.269307 | True          |
| rebalance_10_state_WEAK_BREADTH_zero           |             20 |     0.0244101 |               0.590379 |                2.35292 |             1 |                  1 |        0.0545552 |               0.327455 |                0.198669 | True          |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |             20 |     0.0242128 |               0.591608 |                2.24677 |             1 |                  1 |        0.0592233 |               0.341277 |                0.203465 | True          |
| rebalance_20                                   |             20 |     0.0212341 |               0.583906 |                1.62128 |             1 |                  1 |        0.0329729 |               0.980934 |                0.213316 | True          |
| smooth_5_state_TREND_HOSTILE_zero              |             20 |     0.0279964 |               0.55814  |                1.06028 |             1 |                  1 |        0.0595669 |               0.348427 |                0.307803 | False         |

## Nearby Parameter / Selection-Risk Diagnostics

| variant_name                                   |   neighbor_count |   h20_mean_ic |   neighbor_mean_h20_ic |   neighbor_min_h20_ic | neighbor_support   |
|:-----------------------------------------------|-----------------:|--------------:|-----------------------:|----------------------:|:-------------------|
| rank_persist_10_state_TREND_HOSTILE_zero       |                3 |     0.0284181 |              0.0243279 |             0.022271  | True               |
| smooth_5_state_TREND_HOSTILE_zero              |                3 |     0.0279964 |              0.0218795 |             0.02048   | True               |
| rebalance_10_state_WEAK_BREADTH_zero           |                3 |     0.0244101 |              0.0228801 |             0.0217112 | True               |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero |                3 |     0.0242128 |              0.0230092 |             0.0219877 | True               |
| rebalance_20                                   |                1 |     0.0212341 |              0.0165177 |             0.0165177 | True               |

## Regime And Stress Attribution Snapshot

| variant_name                                   | state                  |   n_dates |   mean_ic |      ic_ir |   positive_ic_rate |
|:-----------------------------------------------|:-----------------------|----------:|----------:|-----------:|-------------------:|
| rank_persist_10_state_TREND_HOSTILE_zero       | LOW_DISPERSION         |       214 | 0.0455908 |   0.310509 |           0.626168 |
| rank_persist_10_state_TREND_HOSTILE_zero       | HOSTILE_LOW_DISPERSION |       214 | 0.0455908 |   0.310509 |           0.626168 |
| rank_persist_10_state_TREND_HOSTILE_zero       | WEAK_BREADTH           |       511 | 0.0302451 |   0.208629 |           0.561644 |
| rank_persist_10_state_TREND_HOSTILE_zero       | STRESS_OR_WEAK_BREADTH |       536 | 0.029158  |   0.204929 |           0.559701 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | recovery_phase         |         1 | 0.111457  | nan        |           1        |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | DRAWDOWN               |       357 | 0.0305562 |   0.246363 |           0.596639 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | drawdown_acceleration  |       357 | 0.0305562 |   0.246363 |           0.596639 |
| rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero | VOLATILITY_SPIKE       |       261 | 0.027901  |   0.25081  |           0.574713 |
| rebalance_10_state_WEAK_BREADTH_zero           | recovery_phase         |         1 | 0.111457  | nan        |           1        |
| rebalance_10_state_WEAK_BREADTH_zero           | DRAWDOWN               |       328 | 0.0315298 |   0.245863 |           0.594512 |
| rebalance_10_state_WEAK_BREADTH_zero           | drawdown_acceleration  |       328 | 0.0315298 |   0.245863 |           0.594512 |
| rebalance_10_state_WEAK_BREADTH_zero           | PANIC_LIQUIDITY_STRESS |       173 | 0.0305622 |   0.245095 |           0.589595 |
| rebalance_20                                   | VOLATILITY_SPIKE       |       393 | 0.0329783 |   0.308793 |           0.613232 |
| rebalance_20                                   | volatility_spike       |       393 | 0.0329783 |   0.308793 |           0.613232 |
| rebalance_20                                   | recovery_phase         |       196 | 0.0305863 |   0.32055  |           0.612245 |
| rebalance_20                                   | PANIC_LIQUIDITY_STRESS |       187 | 0.0248791 |   0.225226 |           0.609626 |
| smooth_5_state_TREND_HOSTILE_zero              | LOW_DISPERSION         |       214 | 0.0366975 |   0.23642  |           0.551402 |
| smooth_5_state_TREND_HOSTILE_zero              | HOSTILE_LOW_DISPERSION |       214 | 0.0366975 |   0.23642  |           0.551402 |
| smooth_5_state_TREND_HOSTILE_zero              | PANIC_LIQUIDITY_STRESS |       186 | 0.029387  |   0.197771 |           0.510753 |
| smooth_5_state_TREND_HOSTILE_zero              | panic_liquidity_stress |       186 | 0.029387  |   0.197771 |           0.510753 |

## Interpretation

- Robustness survives stricter validation for multiple variants, not just the single top-ranked refinement.
- The edge is mostly state-dependent. `TREND_HOSTILE`, `WEAK_BREADTH`, and `STRESS_OR_WEAK_BREADTH` variants dominate the conditional results.
- The broad `rebalance_20` reference remains useful and stable, but the strongest evidence is conditional rather than universal.
- Turnover remains acceptable after smoothing/rebalance/rank-persistence handling; improvements appear consistent with reduced rank churn rather than simple exposure suppression.
- Baseline similarity remains moderate-low against the bounded v2/v3/v4 and Track A reference set.
- Selection risk is present because variants are related and peer correlations are high, but nearby variants generally support the same direction rather than showing a one-off winner.

## Final Recommendation

Move `participation_liquidity_state_shift_20_60` to a research-only Conditional-Alpha integration review design step. Use a small fixed candidate set centered on `rank_persist_10_state_TREND_HOSTILE_zero`, `smooth_5_state_TREND_HOSTILE_zero`, `rebalance_10_state_WEAK_BREADTH_zero`, `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero`, and `rebalance_20`. Do not promote or register the signal.
