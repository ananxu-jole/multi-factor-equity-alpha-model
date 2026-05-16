# Phase 2 Expansion Batch v4 Research Log

## Objective

Batch 4 tested a narrow LOW_BREADTH conditional research set after the Conditional Edge Atlas v1 and LOW_BREADTH audit indicated that some edges may be more reliable when market participation is weak.

The goal was not to force a survivor. The goal was to test whether a small, interpretable conditional activation layer could improve WFV stability and downstream research eligibility while preserving the existing validation structure.

No code logic, gates, schemas, promotion rules, or portfolio construction rules were modified for this research log. No pipelines were rerun for this document.

## Why LOW_BREADTH Was Chosen

LOW_BREADTH was selected because Conditional Edge Atlas v1 showed it as a recurring conditional state across several signal families. The audit suggested that weak market participation was one of the few states where conditional behavior appeared repeatable enough to justify a narrow Batch 4 test.

The research premise was conservative:

- Weak participation may create cleaner conditional behavior for trend-quality and reversal-style signals.
- LOW_BREADTH should be tested with only a small implementation set.
- Evidence must still pass the standard scoring, WFV, health, reproducibility, diversity, alpha construction, stress, and survivor-freeze stack.

## Signals Implemented

Batch 4 implemented two LOW_BREADTH conditional variants:

| Signal | Family | Conditional Context | Intent |
| --- | --- | --- | --- |
| `failed_breakout_reversal_20_low_breadth` | `microstructure_lite` | `breadth_level_state=LOW_BREADTH` | Test whether failed-breakout reversal behavior is more stable when breadth is weak. |
| `smooth_trend_persistence_60_low_breadth` | `trend_quality` | `breadth_level_state=LOW_BREADTH` | Test whether smoothed trend persistence is more robust under weak participation. |

Both were tagged with:

- `expansion_batch = phase2_expansion_batch_v4`
- `conditional_source = conditional_edge_atlas_v1_low_breadth_audit`

The original unconditional formulas were preserved.

## Structural Results

Both Batch 4 signals passed structural quality.

| Signal | Missing % | Finite % | Structural Result | Discovery Best Horizon | Discovery Mean IC |
| --- | ---: | ---: | --- | ---: | ---: |
| `failed_breakout_reversal_20_low_breadth` | 0.001780 | 0.998220 | Passed | 1 | -0.011918 |
| `smooth_trend_persistence_60_low_breadth` | 0.036163 | 0.963837 | Passed | 1 | 0.002446 |

The LOW_BREADTH condition reduced active signal expression, but coverage remained high enough for the research stack to evaluate the candidates.

## 03 Scoring Results

Both signals showed their strongest 03 scoring evidence at horizon 20.

| Signal | Best Horizon | Mean IC | Abs Mean IC | IC IR | Best-Horizon 03 Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `failed_breakout_reversal_20_low_breadth` | 20 | -0.041866 | 0.041866 | -0.267534 | `APPROVED_FOR_WFV` |
| `smooth_trend_persistence_60_low_breadth` | 20 | -0.050074 | 0.050074 | -0.241726 | `APPROVED_FOR_WFV` |

Horizon-level scoring outcomes:

- `failed_breakout_reversal_20_low_breadth`: h10 and h20 reached `APPROVED_FOR_WFV`; h5 was `WATCHLIST`; h1 was `REJECTED_LOW_SIGNAL`.
- `smooth_trend_persistence_60_low_breadth`: h10 and h20 reached `APPROVED_FOR_WFV`; h1 and h5 were `REJECTED_LOW_SIGNAL`.

The sign direction at the strongest horizons was negative, so the downstream WFV bridge evaluated them as reverse-direction edges.

## Decay And Regime Observations

03C decay outputs were `INSUFFICIENT_DATA` with `LOW_DECAY_RISK` for both signals across the evaluated horizons. This should not be over-interpreted as strong decay stability; it primarily indicates that the rolling decay layer did not have enough evidence to flag a formal decay failure.

03D regime diagnostics remained conditional:

- `failed_breakout_reversal_20_low_breadth` showed moderate to high regime fragility depending on horizon and regime cut.
- `smooth_trend_persistence_60_low_breadth` showed high regime fragility, especially at h20.

This was consistent with the research premise: the candidates were conditional edges, not universal signals.

## 03B WFV Bridge Results

The controlled 03B signal-WFV bridge tested only the two Batch 4 LOW_BREADTH candidates at h20.

Bridge metadata:

- `expansion_batch = phase2_expansion_batch_v4`
- `bridge_source = conditional_edge_atlas_v1_low_breadth_audit`
- `failed_breakout_reversal_20_low_breadth`: `BATCH4_LOW_BREADTH_PRIMARY`
- `smooth_trend_persistence_60_low_breadth`: `BATCH4_LOW_BREADTH_DIAGNOSTIC`

| Signal | Horizon | WFV Status | Effective Mean Test IC | Effective Test IC IR | Persistence | Sign Consistency | Notes |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| `failed_breakout_reversal_20_low_breadth` | 20 | `REJECTED_WFV` | -0.001720 | -0.019087 | 0.750000 | 0.750000 | `direction flip; weak effective IC; weak effective IC IR` |
| `smooth_trend_persistence_60_low_breadth` | 20 | `APPROVED_WFV` | 0.051455 | 0.225597 | 0.750000 | 0.750000 | `Meets strict direction-adjusted WFV thresholds.` |

The failed-breakout candidate did not survive the bridge. The smooth trend candidate passed WFV despite being introduced as the diagnostic candidate.

## 03E / 03F / 03G Outcomes

After WFV, `smooth_trend_persistence_60_low_breadth` became the only Batch 4 signal to progress materially through downstream signal research.

| Signal | Horizon | 03E Health Score | 03E Gate | 03F Status | 03F Pass Rate | 03G Selected | 03G Rank |
| --- | ---: | ---: | --- | --- | ---: | ---: | ---: |
| `smooth_trend_persistence_60_low_breadth` | 20 | 87 | `APPROVED_FOR_RESEARCH` | `GLOBAL_PASS` | 0.857143 | 1 | 1 |
| `smooth_trend_persistence_60_low_breadth` | 10 | 72 | `APPROVED_FOR_RESEARCH` | `GLOBAL_PASS` | 0.928571 | 1 | 3 |
| `failed_breakout_reversal_20_low_breadth` | 20 | 52 | `WATCHLIST_RESEARCH` | Did not enter 03F | N/A | 0 | N/A |

The h20 smooth trend row was selected by 03G within the correlation threshold. The h10 row was also selected to meet the minimum selection set, but the h20 row remained the primary Batch 4 evidence item.

## Alpha Pool Outcome

`smooth_trend_persistence_60_low_breadth` reached `alpha_signal_pool_current`.

| Signal | Horizon | Selected Flag | Pool Eligible | Pool Weight Base | Pass Rate | Avg Effective Mean IC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `smooth_trend_persistence_60_low_breadth` | 20 | 1 | 1 | 0.172902 | 0.857143 | 0.049249 |
| `smooth_trend_persistence_60_low_breadth` | 10 | 1 | 1 | 0.143091 | 0.928571 | 0.041829 |

`failed_breakout_reversal_20_low_breadth` did not reach the alpha pool.

This clarified an important point from the earlier admission diagnostic: the Batch 4 smooth trend signal was not blocked at the alpha-pool stage. It reached the alpha pool and became available for alpha construction.

## 04A / 04B / 07 / 08 Diagnostic Outcome

### 04A Alpha Construction

`smooth_trend_persistence_60_low_breadth` entered constructed alphas. Current construction metadata shows it in 14 constructed alpha definitions, including:

- `alpha_equal_weight_research_v1`
- `alpha_health_weighted_research_v1`
- `alpha_regime_aware_research_v1`
- `alpha_diversified_research_v2`
- `alpha_smooth_regime_weighted_v2`
- `alpha_persistence_blend_v2`
- `alpha_decay_aware_dynamic_v3`
- `alpha_regime_blend_dynamic_v3`
- `alpha_rolling_ic_dynamic_v3`
- `alpha_hybrid_adaptive_v3`
- `alpha_decay_aware_dynamic_v4_smooth`
- `alpha_regime_blend_dynamic_v4_smooth`
- `alpha_rolling_ic_dynamic_v4_smooth`
- `alpha_hybrid_adaptive_v4_smooth`

### 04B Constructed Alpha WFV

Several constructed alphas containing `smooth_trend_persistence_60_low_breadth` reached watchlist or approved constructed-alpha WFV statuses at selected horizons.

Examples:

- `alpha_decay_aware_dynamic_v4_smooth h5`: `APPROVED_CONSTRUCTED_ALPHA_WFV`
- `alpha_regime_blend_dynamic_v4_smooth h5`: `APPROVED_CONSTRUCTED_ALPHA_WFV`
- `alpha_persistence_blend_v2 h10`: `APPROVED_CONSTRUCTED_ALPHA_WFV`
- `alpha_diversified_research_v2 h10/h20`: `WATCHLIST_CONSTRUCTED_ALPHA_WFV`

This confirms that the Batch 4 smooth trend signal did not stop at signal research. It entered constructed-alpha experiments and contributed to downstream candidates.

### 07 Stress

The sole 07 `APPROVED_STRESS` alpha was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`

Its component signals were:

- `vol_surprise_20_60`
- `price_impact_proxy_20`
- `range_expansion_failure_5`
- `liquidity_adjusted_reversal_5`

It did not include `smooth_trend_persistence_60_low_breadth`.

Constructed alphas that did include `smooth_trend_persistence_60_low_breadth` did not become the sole stress-approved survivor:

| Alpha | Horizon | 07 Status | Promotion Decision | Pass Rate | Worst Degradation | Turnover Risk |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `alpha_regime_blend_dynamic_v4_smooth` | 5 | `REJECTED_STRESS` | `REJECT` | 0.722222 | 0.803514 | `LOW_TURNOVER_RISK` |
| `alpha_persistence_blend_v2` | 10 | `REJECTED_STRESS` | `REJECT_HIGH_TURNOVER` | 0.666667 | 3.481160 | `HIGH_TURNOVER_RISK` |
| `alpha_diversified_research_v2` | 20 | `REJECTED_STRESS` | `REJECT_HIGH_TURNOVER` | 0.611111 | 3.473657 | `HIGH_TURNOVER_RISK` |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `WATCHLIST_STRESS` | `REVIEW_SATELLITE` | 0.555556 | 0.601208 | `LOW_TURNOVER_RISK` |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `WATCHLIST_STRESS` | `REVIEW_SATELLITE` | 0.555556 | 0.641822 | `LOW_TURNOVER_RISK` |

### 08 Survivor Freeze

The sole 07 stress-approved alpha became:

- final decision: `REVIEW_SATELLITE`
- final status: `SATELLITE_WATCHLIST`
- survivor tier: `WATCH_STRESS_SURVIVOR`

It did not become `PROMOTE_CORE`.

Exact 08 blockers:

- `pass_rate = 0.777778`, below the `0.90` core survivor-tier threshold
- `turnover_risk_flag = MODERATE_TURNOVER_RISK`, not `LOW_TURNOVER_RISK`
- `survivor_selection_score = 28.377197`, below `MIN_CLUSTER_SCORE = 40`
- `worst_degradation = 0.788569`, close to the catastrophic degradation boundary

The survivor-freeze stage therefore produced zero final core survivors. This was a conservative validation outcome, not an alpha-pool admission failure.

## Final Conclusion

Batch 4 validated the conditional research path but did not produce a core survivor.

The strongest Batch 4 signal, `smooth_trend_persistence_60_low_breadth`, passed signal WFV, passed health, passed reproducibility, passed diversity selection, reached the alpha pool, and entered constructed alphas. That is meaningful progress for the conditional research program.

However, the constructed alphas that included it did not become the sole 07 stress-approved survivor. The only stress-approved survivor was an orthogonal diversifier that did not include `smooth_trend_persistence_60_low_breadth`, and that survivor was classified as `REVIEW_SATELLITE` rather than `PROMOTE_CORE`.

The platform behaved as intended: it allowed promising conditional evidence to advance, but it did not convert that evidence into a core survivor without sufficient downstream stress robustness.

## Lessons Learned

- LOW_BREADTH is a credible conditional research state, but not automatically a core-alpha path.
- Signal-level success can be real while constructed-alpha stress survival still fails.
- `smooth_trend_persistence_60_low_breadth` is the first Batch 4 candidate to validate the full signal-research bridge into alpha construction.
- Alpha construction can dilute or transform conditional signal behavior; downstream stress must be evaluated independently.
- The survivor-freeze layer remains broad-core oriented and conservative.
- Conditional signals may need a dedicated conditional-alpha framework rather than being forced into universal survivor expectations.

## Recommended Next Research Direction

The next research step should focus on conditional-alpha construction rather than adding many new raw conditional signals.

Recommended direction:

- Study how conditional signals behave after blending, smoothing, and dynamic weighting inside constructed alphas.
- Build research diagnostics that separate active-state performance from inactive-state dilution at the constructed-alpha level.
- Keep LOW_BREADTH as a primary conditional research state, but limit new Batch 5 candidates to a small set.
- Compare LOW_BREADTH trend-quality components against orthogonal diversifier components to understand why the final stress survivor came from a different sleeve.
- Do not relax survivor-freeze or portfolio-construction gates to force conditional survivors.

Batch 4 should be treated as a successful research iteration, not a production-ready survivor result.
