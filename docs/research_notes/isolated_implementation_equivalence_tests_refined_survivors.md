# Isolated Implementation-Equivalence Tests: Refined Survivors

## 1. Executive Takeaway

This note documents a research-only isolated implementation-equivalence test for two refined survivor draft signals:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

The test followed `docs/research_notes/isolated_implementation_equivalence_test_plan_refined_survivors.md` and was run in a separate research namespace:

`artifacts/research/refined_survivor_equivalence_v1/`

Final classifications:

| Signal | Equivalence Classification | Reason |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | `near-equivalent with minor review items` | Formula semantics, sign convention, h20 alignment, and turnover behavior were preserved, but raw sidecar matrices were unavailable and coverage drifted materially versus sidecar metric summaries. |
| `volatility_surprise_reversal_20_60_smooth` | `near-equivalent with minor review items` | Formula semantics, sign convention, h20/h10 behavior, and smoothing were preserved, but raw sidecar matrices were unavailable; metric/coverage drift and high baseline similarity require review. |

Recommended next step:

`proceed to isolated signal-factory integration test planning`

This recommendation is conditional: the integration plan should explicitly carry forward the review items below. These tests do not justify production registration yet.

No production signal-factory registration, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha paths were changed.

## 2. Research Namespace / Run Identifier

| Field | Value |
| --- | --- |
| `run_id` | `refined_survivor_equivalence_v1` |
| `research_only` | `true` |
| Output namespace | `artifacts/research/refined_survivor_equivalence_v1/` |
| Input data | `data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet` |
| Reference metric source | `/private/tmp/underdog_refinement_metrics/summary.csv` |
| Production registration | `false` |
| Production tables modified | `false` |

Artifacts written:

- `manifest.json`
- `implementation_equivalence_summary.csv`
- `equivalence_classification.csv`
- `horizon_metric_comparison.csv`
- `coverage_turnover_comparison.csv`
- `baseline_comparison.csv`
- `proxy_return_comparison.csv`
- `stress_regime_comparison.csv`
- `alignment_lookahead_checks.csv`
- `volume_shock_reversal_stable_20_signal_values.parquet`
- `volatility_surprise_reversal_20_60_smooth_signal_values.parquet`

## 3. Scope and Exclusions

In scope:

- isolated research implementations of the two draft formulas
- comparison against available sidecar metric summaries
- baseline diagnostic comparisons
- coverage, turnover, horizon, proxy-return, and stress/regime checks
- alignment and look-ahead review
- research-only classification

Out of scope:

- production signal-factory registration
- official scoring integration
- official WFV bridge
- 04A+ execution
- survivor/watchlist mutation
- portfolio construction
- schema, gate, threshold, or validation-logic changes
- ML usage
- Conditional-Alpha usage

Important limitation:

Raw sidecar signal matrices were not available. Therefore, this test could not perform bit-level raw-value, rank-value, or date/ticker matrix equality checks against the original sidecar run. The comparison uses regenerated isolated outputs and prior sidecar metric summaries.

## 4. Isolated Implementation Summary

### `volume_shock_reversal_stable_20`

The isolated implementation preserved the draft semantics:

- compute recent reversal component
- compute abnormal volume relative to a rolling volume baseline
- combine reversal with stabilized volume shock
- smooth the combined expression
- convert to cross-sectional rank score by date

Research implementation shape:

- volume shock baseline: 40 trading days
- smoothing window: 10 trading days
- reversal sign: higher score favors reversal after elevated-volume negative return
- primary horizon: h20

### `volatility_surprise_reversal_20_60_smooth`

The isolated implementation preserved the draft semantics:

- compute 20-day realized volatility
- compute 60-day realized volatility baseline
- compute short-vs-long realized-volatility surprise
- combine volatility surprise with return reversal
- smooth the combined expression
- convert to cross-sectional rank score by date

Research implementation shape:

- short realized volatility: 20 trading days
- long realized volatility: 60 trading days
- smoothing window: 5 trading days
- reversal sign: higher score favors volatility-surprise-weighted reversal
- primary horizon: h20
- diagnostic horizon: h10

## 5. Reference Artifacts Used

Reference artifacts available:

- `/private/tmp/underdog_refinement_metrics/summary.csv`
- `/private/tmp/underdog_refinement_metrics/structural.csv`
- `/private/tmp/underdog_refinement_metrics/best.csv`
- `/private/tmp/underdog_refinement_metrics/wfv.csv`
- `/private/tmp/underdog_refinement_metrics/regime.csv`
- `/private/tmp/underdog_refinement_metrics/corr.csv`

Reference limitations:

- Raw sidecar signal values were not available.
- Raw sidecar rank matrices were not available.
- Exact sidecar universe mask could not be reconstructed perfectly from the metric summaries.
- Sidecar missingness was materially higher than the isolated implementation, likely because the prior sidecar used a stricter universe or data-availability mask.

Reference variants used for metric comparison:

| Draft Signal | Reference Variant |
| --- | --- |
| `volume_shock_reversal_stable_20` | `volume_shock_reversal_stable_s40_sm10` |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_surprise_reversal_s20_l60_sm5` |

## 6. `volume_shock_reversal_stable_20` Equivalence Results

### Horizon Metrics

| Horizon | Mean IC | IC IR | Positive IC Rate | IC Dates |
| ---: | ---: | ---: | ---: | ---: |
| h1 | 0.005437 | 0.027643 | 0.506101 | 2049 |
| h5 | 0.010449 | 0.057256 | 0.518337 | 2045 |
| h10 | 0.011421 | 0.066956 | 0.517157 | 2040 |
| h20 | 0.011798 | 0.070228 | 0.513300 | 2030 |

Horizon interpretation:

- h20 remained the strongest horizon, consistent with the draft definition.
- IC direction remained positive across h1, h5, h10, and h20.
- The h20 mean IC was close to the sidecar reference value.

### Reference Metric Comparison

| Metric | Sidecar Reference | Isolated Implementation | Drift |
| --- | ---: | ---: | ---: |
| h20 mean IC | 0.009791 | 0.011798 | 0.002007 |
| h20 abs mean IC | 0.009791 | 0.011798 | 0.002007 |
| h20 abs IC IR | 0.084605 | 0.070228 | 0.014377 |
| h20 positive IC rate | 0.550490 | 0.513300 | 0.037190 |
| turnover proxy | 0.128510 | 0.098531 | 0.029979 |
| missing pct | 0.416277 | 0.034545 | 0.381732 |

Equivalence interpretation:

- Formula behavior and h20 direction are close enough for isolated integration planning.
- Turnover is lower than the sidecar reference, which is not automatically good; it must be checked for smoothing or stale-value effects in the next stage.
- Missingness drift is material and remains the main review item.

### Structural Results

| Metric | Value |
| --- | ---: |
| Missing pct | 0.034545 |
| Finite pct | 0.965455 |
| Date coverage | 0.977121 |
| Mean ticker coverage | 0.965455 |
| Turnover proxy | 0.098531 |

### Stress / Regime Results

Selected h20 state results:

| State | Dates | Mean IC | IC IR | Positive IC Rate |
| --- | ---: | ---: | ---: | ---: |
| drawdown acceleration | 843 | 0.029143 | 0.157260 | 0.533808 |
| volatility spike | 272 | 0.015921 | 0.076991 | 0.448529 |
| panic/liquidity stress | 205 | 0.070692 | 0.389327 | 0.673171 |
| recovery phase | 416 | 0.012952 | 0.085040 | 0.538462 |
| low breadth | 508 | 0.024581 | 0.140314 | 0.547244 |

Stress interpretation:

- The signal retained positive behavior in stress-like slices.
- Panic/liquidity stress was the strongest state in this isolated diagnostic.
- This is supportive, but not a substitute for official stress testing.

### Classification

`near-equivalent with minor review items`

Reason:

The isolated implementation preserved the intended formula semantics, sign convention, h20 horizon behavior, and lower-turnover refined shape. Raw sidecar matrices were unavailable, and missingness drift versus sidecar summaries remains unresolved.

## 7. `volatility_surprise_reversal_20_60_smooth` Equivalence Results

### Horizon Metrics

| Horizon | Mean IC | IC IR | Positive IC Rate | IC Dates |
| ---: | ---: | ---: | ---: | ---: |
| h1 | 0.003139 | 0.015350 | 0.495819 | 2033 |
| h5 | 0.009955 | 0.052427 | 0.510103 | 2029 |
| h10 | 0.014270 | 0.080512 | 0.517292 | 2024 |
| h20 | 0.016677 | 0.095470 | 0.519364 | 2014 |

Horizon interpretation:

- h20 remained strongest in the isolated implementation.
- h10 was also positive and coherent as a diagnostic horizon.
- Direction remained positive across all tested horizons.

### Reference Metric Comparison

| Metric | Sidecar Reference | Isolated Implementation | Drift |
| --- | ---: | ---: | ---: |
| h20 mean IC | 0.002123 | 0.016677 | 0.014554 |
| h20 abs mean IC | 0.002123 | 0.016677 | 0.014554 |
| h20 abs IC IR | 0.016039 | 0.095470 | 0.079430 |
| h20 positive IC rate | 0.497047 | 0.519364 | 0.022317 |
| turnover proxy | 0.085561 | 0.067001 | 0.018559 |
| missing pct | 0.430867 | 0.042149 | 0.388717 |

Equivalence interpretation:

- Direction and horizon shape are preserved.
- The isolated implementation is materially stronger than the sidecar reference on h20 mean IC and IC IR.
- This improvement is suspicious in an equivalence test and must be reviewed, not celebrated.
- Missingness drift is material.

### Structural Results

| Metric | Value |
| --- | ---: |
| Missing pct | 0.042149 |
| Finite pct | 0.957851 |
| Date coverage | 0.969495 |
| Mean ticker coverage | 0.957851 |
| Turnover proxy | 0.067001 |

### Stress / Regime Results

Selected h20 state results:

| State | Dates | Mean IC | IC IR | Positive IC Rate |
| --- | ---: | ---: | ---: | ---: |
| drawdown acceleration | 831 | 0.029087 | 0.153685 | 0.529483 |
| volatility spike | 272 | 0.030274 | 0.133014 | 0.540441 |
| panic/liquidity stress | 205 | positive in isolated artifact | positive in isolated artifact | reviewed in artifact |
| recovery phase | reviewed in artifact | reviewed in artifact | reviewed in artifact | reviewed in artifact |
| low breadth | reviewed in artifact | reviewed in artifact | reviewed in artifact | reviewed in artifact |

Stress interpretation:

- The candidate remained positive in drawdown acceleration and volatility spike states.
- Full state details are in `stress_regime_comparison.csv`.
- Stress behavior is coherent enough for the next isolated planning step, but baseline redundancy requires attention.

### Classification

`near-equivalent with minor review items`

Reason:

Formula semantics, h20/h10 behavior, sign direction, and smoothing were preserved. However, raw sidecar matrices were unavailable, h20 metric improvement versus sidecar was material, missingness drift was large, and baseline comparisons showed high similarity to simpler volatility/reversal proxies.

## 8. Alignment / Look-Ahead Test Results

| Check | Status | Note |
| --- | --- | --- |
| historical window check | `PASS` | Rolling returns, volume baselines, realized volatility, and smoothing used trailing windows. |
| forward return alignment check | `PASS` | Forward returns used `close.shift(-h) / close - 1` after signal construction. |
| window-end timing check | `PASS` | Rolling windows ended on the signal date. |
| smoothing leakage check | `PASS` | Smoothing used trailing rolling means. |
| ranking alignment check | `PASS` | Cross-sectional ranks were computed from same-date signal values. |
| same-bar leakage review | `REVIEW` | Signals use same-date close/volume; future official testing must assume after-close or next-rebalance tradability. |
| raw sidecar matrix availability | `REVIEW` | Raw sidecar matrices were unavailable; comparison used metric summaries and regenerated isolated outputs. |

No direct look-ahead was found in the isolated formulas. The remaining timing issue is execution semantics, not formula leakage: same-date close/volume use must be matched to the platform's assumed rebalance timing in future isolated integration testing.

## 9. Drift Review Summary

Primary drift items:

| Signal | Drift Item | Interpretation |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | Missingness drift of 0.381732 | Isolated panel coverage was much broader than sidecar metric coverage. Universe/mask equivalence should be reviewed. |
| `volatility_surprise_reversal_20_60_smooth` | h20 mean IC drift of 0.014554 | Isolated implementation was materially stronger than sidecar reference; this is suspicious and requires review. |
| `volatility_surprise_reversal_20_60_smooth` | Missingness drift of 0.388717 | Isolated panel coverage was much broader than sidecar metric coverage. Universe/mask equivalence should be reviewed. |
| both | raw matrix unavailable | Full raw-value and rank-order equivalence could not be proven. |

Interpretation:

- Neither candidate failed formula-semantic equivalence.
- Neither candidate should be called fully implementation-equivalent.
- The correct classification is near-equivalent with review items.

## 10. Baseline Diagnostic Comparisons

### Volume Candidate Baselines

| Comparison | Value Correlation |
| --- | ---: |
| simple volume spike reversal | 0.428076 |
| unweighted reversal | 0.721718 |
| no stability filter version | 0.428809 |

Baseline interpretation:

- The refined volume candidate is meaningfully related to reversal, as expected.
- It is not simply the raw volume-spike version.
- It has lower turnover than the simple volume-spike and no-stability versions.
- Correlation with unweighted reversal is high enough to require orthogonality review later.

Turnover comparison:

| Signal | Turnover Proxy |
| --- | ---: |
| `volume_shock_reversal_stable_20` | 0.098531 |
| simple volume spike reversal | 0.296222 |
| unweighted reversal | 0.153509 |
| no stability filter version | 0.294984 |

The stability/smoothing layer reduced churn as intended.

### Volatility Candidate Baselines

| Comparison | Value Correlation |
| --- | ---: |
| simple volatility reversal | 0.895939 |
| unsmoothed volatility-surprise reversal | 0.915953 |
| 20-only volatility reversal | 0.895939 |
| plain reversal 20 smooth5 | 0.986813 |

Baseline interpretation:

- This is the largest review item for the volatility candidate.
- The isolated implementation is highly similar to plain smoothed reversal and simple volatility reversal.
- This does not prove the formula is wrong, but it weakens the claim that the isolated implementation reproduced the sidecar uniqueness finding.
- Future integration planning should require a stricter orthogonality and counterfactual attribution audit before any registration step.

## 11. Failure or Review Items

Review items before isolated signal-factory integration:

1. Raw sidecar signal matrices were unavailable.
2. Sidecar universe/missingness mask could not be reproduced exactly.
3. Both candidates had much lower missingness in the isolated broad-panel implementation than in sidecar summaries.
4. `volatility_surprise_reversal_20_60_smooth` showed suspiciously stronger h20 metrics than its sidecar reference.
5. `volatility_surprise_reversal_20_60_smooth` was highly correlated with simple volatility/reversal baselines in this isolated test.
6. Same-date close/volume usage requires explicit after-close or next-rebalance timing assumptions in later testing.
7. The tests used regenerated formula outputs, not production signal-factory outputs.

No production rollback is required because no production objects were changed.

## 12. Final Equivalence Classification

| Signal | Final Classification | Decision |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | `near-equivalent with minor review items` | Suitable for isolated signal-factory integration test planning, with universe/missingness review carried forward. |
| `volatility_surprise_reversal_20_60_smooth` | `near-equivalent with minor review items` | Suitable for isolated signal-factory integration test planning only if baseline redundancy and suspicious metric improvement are explicitly reviewed. |

Neither signal is classified as fully `implementation-equivalent` because raw sidecar matrices were not available.

Neither signal is classified as `not implementation-equivalent` because the isolated implementations preserved the intended formula semantics, sign convention, trailing-window construction, and horizon direction.

## 13. Recommended Next Step

Recommended next move:

`proceed to isolated signal-factory integration test planning`

The next plan should:

- keep a separate research namespace
- implement these formulas only as isolated signal-factory candidates
- compare signal-factory outputs against the artifacts from `refined_survivor_equivalence_v1`
- preserve h20 primary metadata
- carry h10 as diagnostic for the volatility candidate
- explicitly review universe/missingness drift
- explicitly review baseline redundancy for the volatility candidate
- verify after-close or next-rebalance execution assumptions
- avoid production registration unless isolated integration reproduces these findings without new drift

Do not proceed directly to production registration.

## Final Conclusion

The isolated implementation-equivalence test was useful: both candidates can be implemented in a way that preserves their intended research semantics, but neither receives a clean full-equivalence pass.

`volume_shock_reversal_stable_20` is the cleaner of the two from an equivalence perspective because its h20 metric drift was small and smoothing reduced turnover as intended.

`volatility_surprise_reversal_20_60_smooth` remains viable for isolated integration planning, but its suspiciously improved h20 metrics and high similarity to simple reversal/volatility baselines must be treated as open review items.

The platform should continue cautiously: isolated signal-factory integration planning is justified, production registration is not.
