# Isolated Signal-Factory Integration Tests: Refined Survivors

## 1. Executive Takeaway

This note documents a research-only isolated signal-factory integration test for two refined survivor candidates:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

The test followed `docs/research_notes/isolated_signal_factory_integration_test_plan_refined_survivors.md` and used an isolated research namespace:

`artifacts/research/refined_survivor_signal_factory_integration_v1/`

Final integration decisions:

| Candidate | Final Decision | Reason |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | `integration-compatible with review items` | Metadata, isolated generation, panel shape, h20 scoring, WFV compatibility, and stress attribution completed cleanly. Main review item is meaningful overlap with unweighted reversal. |
| `volatility_surprise_reversal_20_60_smooth` | `integration-compatible with review items` | Metadata, isolated generation, h20/h10 scoring, WFV compatibility, and stress attribution completed, but high baseline similarity and suspiciously strong h20 behavior remain unresolved. |

Recommended next step:

`Split the next action by candidate: update controlled production-registration design for volume_shock_reversal_stable_20, and run additional drift/redundancy review for volatility_surprise_reversal_20_60_smooth before any registration planning.`

This test does not authorize production registration. No production signal factory, gates, schemas, thresholds, survivor/watchlist lists, portfolio logic, validation logic, ML layers, or Conditional-Alpha paths were changed.

## 2. Isolated Namespace / Run Identifier

| Field | Value |
| --- | --- |
| `run_id` | `refined_survivor_signal_factory_integration_v1` |
| Output namespace | `artifacts/research/refined_survivor_signal_factory_integration_v1/` |
| Input data | `data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet` |
| Equivalence artifact source | `artifacts/research/refined_survivor_equivalence_v1/` |
| Research only | `true` |
| Production registration | `false` |
| Production tables modified | `false` |
| Survivor/watchlist mutation | `false` |
| Portfolio usage | `false` |
| ML usage | `false` |
| Conditional-Alpha usage | `false` |

Artifacts written:

- `manifest.json`
- `isolated_candidate_registry.csv`
- `metadata_validation_summary.csv`
- `signal_generation_log.csv`
- `generated_signal_panel_summary.csv`
- `scoring_compatibility_summary.csv`
- `wfv_compatibility_summary.csv`
- `wfv_window_diagnostics.csv`
- `stress_regime_attribution_summary.csv`
- `orthogonality_redundancy_summary.csv`
- `drift_review_log.csv`
- `panel_equivalence_comparison.csv`
- `integration_decision_summary.csv`
- `integration_decision_note.md`
- candidate signal panel parquet files

## 3. Scope and Exclusions

In scope:

- isolated draft insertion using a local research-only registry
- metadata validation
- isolated candidate signal generation
- panel comparison against prior equivalence artifacts
- multi-horizon scoring compatibility
- isolated WFV compatibility diagnostics
- stress/regime attribution
- orthogonality and redundancy audit
- drift monitoring
- candidate-specific integration decisions

Explicitly excluded:

- production signal registration
- `residual_momentum_stability_60`
- LOW_BREADTH and Conditional-Alpha components
- official survivor/watchlist mutation
- production WFV writes
- alpha construction
- portfolio construction
- ML integration
- schema, gate, threshold, or validation-logic changes
- 04A+ execution

## 4. Isolated Draft Insertion Summary

The test used a local, research-only draft registry rather than modifying production signal-factory code.

Included candidates:

| Signal | Family | Version | Registration Status |
| --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | `draft_v1_sidecar_refined` | `DRAFT_RESEARCH_ONLY` |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | `draft_v1_sidecar_refined` | `DRAFT_RESEARCH_ONLY` |

The local registry preserved the intended formulas:

- `volume_shock_reversal_stable_20`: abnormal-volume-weighted reversal with 40-day volume baseline and 10-day trailing smoothing.
- `volatility_surprise_reversal_20_60_smooth`: 20/60 realized-volatility-surprise reversal with 5-day trailing smoothing.

No production factory registration was performed.

## 5. Metadata Validation Results

| Signal | Metadata Complete | Intended Horizon | Family | Version | Registration Status |
| --- | --- | --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `true` | h20 | `liquidity_flow` | `draft_v1_sidecar_refined` | `DRAFT_RESEARCH_ONLY` |
| `volatility_surprise_reversal_20_60_smooth` | `true` | h20 primary; h10 diagnostic | `volatility_structure` | `draft_v1_sidecar_refined` | `DRAFT_RESEARCH_ONLY` |

Validation covered:

- signal name
- family
- version
- intended horizon
- expected direction
- input data requirements
- formula description
- smoothing notes
- known risks
- research source note
- registration status

No metadata schema change was required.

## 6. Generated Signal Panel Summary

| Signal | Rows | Tickers | Missing Pct | Finite Pct | Date Coverage | Turnover Proxy | Inf Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `volume_shock_reversal_stable_20` | 2098 | 478 | 0.034545 | 0.965455 | 0.977121 | 0.098531 | 0 |
| `volatility_surprise_reversal_20_60_smooth` | 2098 | 478 | 0.042171 | 0.957829 | 0.969495 | 0.067001 | 0 |

Panel equivalence versus prior isolated implementation artifacts:

| Signal | Reference Available | Value Corr | Mean Rank Corr by Date | Max Abs Value Diff |
| --- | --- | ---: | ---: | ---: |
| `volume_shock_reversal_stable_20` | `true` | 1.000000 | 1.000000 | 0.000000 |
| `volatility_surprise_reversal_20_60_smooth` | `true` | 1.000000 | 1.000000 | 0.002982 |

Interpretation:

- The isolated factory-style generation reproduced the equivalence artifacts closely.
- The small max absolute difference for the volatility candidate did not affect aggregate scoring drift, but it remains a minor review item.
- No NaN/inf issue appeared beyond expected rolling-window missingness.

## 7. Multi-Horizon Scoring Compatibility

### `volume_shock_reversal_stable_20`

| Horizon | Mean IC | IC IR | Positive IC Rate | Dates |
| ---: | ---: | ---: | ---: | ---: |
| h1 | 0.005437 | 0.027643 | 0.506101 | 2049 |
| h5 | 0.010449 | 0.057256 | 0.518337 | 2045 |
| h10 | 0.011421 | 0.066956 | 0.517157 | 2040 |
| h20 | 0.011798 | 0.070228 | 0.513300 | 2030 |

Result:

- h20 remained the primary horizon.
- Direction was positive across all horizons.
- Scoring behavior matched the prior equivalence artifact.

### `volatility_surprise_reversal_20_60_smooth`

| Horizon | Mean IC | IC IR | Positive IC Rate | Dates |
| ---: | ---: | ---: | ---: | ---: |
| h1 | 0.003139 | 0.015350 | 0.495819 | 2033 |
| h5 | 0.009955 | 0.052427 | 0.510103 | 2029 |
| h10 | 0.014270 | 0.080512 | 0.517292 | 2024 |
| h20 | 0.016677 | 0.095470 | 0.519364 | 2014 |

Result:

- h20 remained strongest.
- h10 remained positive and useful as a diagnostic horizon.
- The suspicious h20 strength versus the older sidecar reference remains unresolved.

## 8. WFV Compatibility Results

This was an isolated WFV compatibility diagnostic, not an official WFV gate or production write.

| Signal | Horizon | Windows | Effective Mean Test IC | Effective Test IC IR | Persistence | Sign Consistency | Research Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `volume_shock_reversal_stable_20` | h20 | 4 | 0.004308 | 0.346720 | 0.500000 | 0.500000 | `WFV_COMPATIBLE_REVIEW` |
| `volatility_surprise_reversal_20_60_smooth` | h10 | 4 | 0.008824 | 0.560419 | 1.000000 | 1.000000 | `WFV_COMPATIBLE_REVIEW` |
| `volatility_surprise_reversal_20_60_smooth` | h20 | 4 | 0.006575 | 0.301337 | 0.500000 | 0.500000 | `WFV_COMPATIBLE_REVIEW` |

Interpretation:

- Both candidates can be consumed by WFV-style logic without special handling.
- h20 WFV compatibility is mixed for both candidates, with persistence/sign consistency at 0.50.
- The volatility candidate has a stronger h10 WFV diagnostic profile, but h10 remains diagnostic rather than a new primary horizon.
- These results support compatibility review, not promotion.

## 9. Stress / Regime Attribution Results

### `volume_shock_reversal_stable_20` at h20

| State | Dates | Mean IC | IC IR | Positive IC Rate |
| --- | ---: | ---: | ---: | ---: |
| drawdown acceleration | 843 | 0.029143 | 0.157260 | 0.533808 |
| volatility spike | 272 | 0.015921 | 0.076991 | 0.448529 |
| panic/liquidity stress | 205 | 0.070692 | 0.389327 | 0.673171 |
| trend transition | 1371 | 0.016176 | 0.095652 | 0.517141 |
| recovery phase | 416 | 0.012952 | 0.085040 | 0.538462 |
| high dispersion / rotation | 525 | 0.007620 | 0.044404 | 0.527619 |

Interpretation:

- Stress behavior remained coherent.
- Panic/liquidity stress was the strongest regime slice.
- Volatility spike positive IC rate was below 0.50 despite positive mean IC, so window consistency should remain under review.

### `volatility_surprise_reversal_20_60_smooth` at h20

| State | Dates | Mean IC | IC IR | Positive IC Rate |
| --- | ---: | ---: | ---: | ---: |
| drawdown acceleration | 831 | 0.029087 | 0.153685 | 0.529483 |
| volatility spike | 272 | 0.030274 | 0.133014 | 0.540441 |
| panic/liquidity stress | 205 | 0.085736 | 0.434348 | 0.648780 |
| trend transition | 1367 | 0.018080 | 0.103450 | 0.522312 |
| recovery phase | 410 | 0.012560 | 0.079649 | 0.534146 |
| high dispersion / rotation | 525 | 0.016060 | 0.089960 | 0.544762 |

Interpretation:

- Stress/regime slices were coherent and strongest in panic/liquidity stress.
- The strength of these slices does not resolve baseline redundancy.
- The candidate may still be capturing generic smoothed reversal behavior during stress.

## 10. Orthogonality / Redundancy Audit

### `volume_shock_reversal_stable_20`

| Baseline | Value Corr | Rank Corr | Top/Bottom Overlap |
| --- | ---: | ---: | ---: |
| simple volume spike reversal | 0.428076 | 0.428002 | 0.286796 |
| no-stability volume version | 0.428809 | 0.428741 | 0.292593 |
| unweighted reversal | 0.721718 | 0.721652 | 0.471053 |
| simple volatility reversal | 0.706612 | 0.706559 | 0.451531 |
| unsmoothed volatility surprise | 0.720447 | 0.720387 | 0.457740 |
| plain 20-day smoothed reversal | 0.684895 | 0.684857 | 0.424063 |

Interpretation:

- The candidate is not just the raw volume-spike version.
- The stability layer materially differentiates it from the no-stability variant.
- There is meaningful overlap with broader reversal-style proxies, especially unweighted reversal.
- This is a review item, not a rejection.

### `volatility_surprise_reversal_20_60_smooth`

| Baseline | Value Corr | Rank Corr | Top/Bottom Overlap |
| --- | ---: | ---: | ---: |
| simple volume spike reversal | 0.275410 | 0.275369 | 0.211570 |
| no-stability volume version | 0.274796 | 0.274760 | 0.215854 |
| unweighted reversal | 0.479165 | 0.479137 | 0.306335 |
| simple volatility reversal | 0.895941 | 0.895927 | 0.643339 |
| unsmoothed volatility surprise | 0.915954 | 0.915941 | 0.683058 |
| plain 20-day smoothed reversal | 0.986812 | 0.986802 | 0.848759 |

Interpretation:

- Baseline similarity remains very high.
- The candidate is nearly indistinguishable from plain 20-day smoothed reversal in this isolated setup.
- This materially weakens the argument for production-registration planning.
- It should not proceed to registration design until a stricter redundancy/drift review explains whether the 20/60 volatility-surprise term adds independent information.

## 11. Drift Monitoring Findings

Versus the prior equivalence artifacts:

- `volume_shock_reversal_stable_20` had exact panel reproduction and negligible scoring/turnover drift.
- `volatility_surprise_reversal_20_60_smooth` had exact stacked/rank correlation against equivalence artifacts, but a small max absolute panel difference of 0.002982 and negligible aggregate metric drift.
- No horizon behavior change occurred.
- No sign flip occurred.
- h20 remained primary for both candidates.
- The volatility candidate's earlier suspicious h20 improvement versus the sidecar summary remains unresolved because the integration test reproduced the equivalence artifact rather than the older sidecar metric profile.

Primary drift risks carried forward:

| Signal | Drift Risk |
| --- | --- |
| `volume_shock_reversal_stable_20` | reversal proxy overlap; universe/missingness mismatch versus older sidecar summary |
| `volatility_surprise_reversal_20_60_smooth` | persistent baseline convergence; suspicious h20 strength versus sidecar reference; minor panel difference versus equivalence artifact |

## 12. Candidate-Specific Integration Decisions

| Candidate | Decision | Review Items | Recommended Candidate-Specific Next Step |
| --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `integration-compatible with review items` | meaningful unweighted reversal overlap, but factory-style generation and h20 behavior are stable | controlled production-registration design update |
| `volatility_surprise_reversal_20_60_smooth` | `integration-compatible with review items` | high baseline similarity, suspicious h20 strength, minor panel drift versus equivalence artifact | additional drift/redundancy review before registration planning |

Neither candidate should be registered into production from this test.

## 13. Review Items Carried Forward

For `volume_shock_reversal_stable_20`:

- Review overlap with unweighted reversal.
- Confirm production-style universe/missingness expectations before any official candidate registration.
- Preserve h20 primary metadata.
- Preserve lower-turnover 40-day volume baseline and 10-day smoothing.

For `volatility_surprise_reversal_20_60_smooth`:

- Explain high correlation with plain 20-day smoothed reversal.
- Explain high correlation with simple volatility reversal.
- Determine whether 20/60 volatility surprise adds independent information.
- Resolve suspicious h20 improvement versus older sidecar reference.
- Keep h10 diagnostic only unless a separate research note changes the horizon thesis.

Shared:

- Keep production separation.
- Do not relax gates or thresholds.
- Do not mutate survivor/watchlist lists.
- Treat suspicious improvement as a review item.

## 14. Recommended Next Step

Recommended next move:

`Split-path follow-up`

1. `volume_shock_reversal_stable_20`: prepare a controlled production-registration design update, still without registering the signal.
2. `volatility_surprise_reversal_20_60_smooth`: run additional drift/redundancy review before any production-registration design update.

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Immediate production registration | Rejected | Integration compatibility is not promotion eligibility. |
| Register both as production candidates | Rejected | Volatility candidate has unresolved baseline redundancy. |
| Pause both candidates | Rejected | Volume candidate remains sufficiently clean for the next planning layer. |
| Revise isolated implementation immediately | Not primary | Factory-style outputs reproduced equivalence artifacts. |
| Revise draft definitions immediately | Not primary | Current definitions were implementable; review items are empirical, not definitional. |

## Final Conclusion

The isolated signal-factory integration test succeeded as a compatibility test: both candidates can be generated, scored, stress-sliced, and evaluated through WFV-style diagnostics in an isolated factory-style flow without production contamination.

The research decision is not symmetric:

- `volume_shock_reversal_stable_20` is the stronger onboarding candidate and can move to a controlled production-registration design update.
- `volatility_surprise_reversal_20_60_smooth` remains viable but should pause before registration planning until redundancy and suspicious metric drift are explained.

The platform is behaving as intended: compatibility evidence is being separated from promotion evidence, and unresolved redundancy is not being waved through.
