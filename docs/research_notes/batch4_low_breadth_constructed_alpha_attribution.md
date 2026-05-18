# Batch 4 LOW_BREADTH Constructed Alpha Attribution Diagnostic

## Objective

This note documents a research-only attribution diagnostic for constructed alphas containing the Batch 4 conditional component:

- `smooth_trend_persistence_60_low_breadth`

The purpose is to understand how the LOW_BREADTH conditional component behaves after alpha construction, blending, inactive-date handling, constructed-alpha WFV, and stress testing.

This diagnostic is observational only. It does not modify production pipelines, gates, schemas, notebook flows, alpha construction logic, validation thresholds, promotion logic, or survivor lists.

## Methodology

The diagnostic used current persisted Project Underdog tables and temporary read-only panel analysis.

Tables reviewed:

- `alpha_construction_metadata_current`
- `alpha_construction_quality_current`
- `alpha_construction_diagnostics_current`
- `alpha_dynamic_weight_audit_current`
- `alpha_constructed_candidates_current`
- `constructed_alpha_wfv_gate_current`
- `constructed_alpha_wfv_windows_current`
- `alpha_stress_gate_current`
- `alpha_stress_results_current`
- `survivor_alpha_registry_current`
- `alpha_signal_pool_current`

Three variants were compared where feasible:

| Variant | Description |
| --- | --- |
| Full constructed alpha | The persisted constructed alpha panel. |
| Without LOW_BREADTH | A diagnostic counterfactual with `smooth_trend_persistence_60_low_breadth` components removed and remaining weights renormalized where possible. |
| LOW_BREADTH component alone | A diagnostic panel using only the LOW_BREADTH components relevant to that alpha. |

Important limitation: the "without LOW_BREADTH" variant is a research approximation, not an official reconstructed alpha. It uses available construction metadata and dynamic weight audit data. It is suitable for attribution direction, not for promotion or rejection decisions.

Metrics reviewed:

- mean IC
- IC IR
- turnover proxy
- exposure rate
- diagnostic rank-spread Sharpe
- diagnostic max drawdown
- WFV-like persistence across official constructed-alpha test windows
- directional consistency
- active vs inactive LOW_BREADTH date behavior
- stress and survivor outcomes

## Batch 4 Constructed Alpha Inventory

Fourteen constructed alphas contained `smooth_trend_persistence_60_low_breadth`.

Abbreviations:

- `LB20`: `smooth_trend_persistence_60_low_breadth_h20`
- `LB10`: `smooth_trend_persistence_60_low_breadth_h10`
- `Dist5`: `expanded_distance_ma_10_h5`
- `Rev5`: `expanded_reversal_5d_h5`
- `Dist1`: `expanded_distance_ma_10_h1`
- `VoV10`: `vol_of_vol_20_h10`
- `IRHD1`: `index_relative_reversal_5_high_drawdown_h1`
- `TC20`: `trend_consistency_20_60_h20`
- `Down1`: `smooth_trend_persistence_60_downtrend_h1`

| Alpha | Components | Construction Status | Turnover Risk | WFV / Stress / Survivor State |
| --- | --- | --- | --- | --- |
| `alpha_equal_weight_research_v1` | `LB20, LB10` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested; not in survivor registry |
| `alpha_health_weighted_research_v1` | `LB20, LB10` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested; not in survivor registry |
| `alpha_regime_aware_research_v1` | `LB20, LB10` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested; not in survivor registry |
| `alpha_smooth_regime_weighted_v2` | `LB20, LB10` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested; not in survivor registry |
| `alpha_diversified_research_v2` | `LB20, LB10, Dist5, Rev5, Dist1` | `APPROVED_FOR_ALPHA_VALIDATION` | `HIGH_TURNOVER_RISK` | WFV watchlist; `REJECT_HIGH_TURNOVER` |
| `alpha_persistence_blend_v2` | `LB20, LB10, Dist5, Rev5, Dist1` | `APPROVED_FOR_ALPHA_VALIDATION` | `HIGH_TURNOVER_RISK` | WFV approved/watchlist; `REJECT_HIGH_TURNOVER` |
| `alpha_decay_aware_dynamic_v3` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested |
| `alpha_regime_blend_dynamic_v3` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested |
| `alpha_rolling_ic_dynamic_v3` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested |
| `alpha_hybrid_adaptive_v3` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `REJECTED_ALPHA_CONSTRUCTION` | `HIGH_TURNOVER_RISK` | Not stress tested |
| `alpha_decay_aware_dynamic_v4_smooth` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | `WATCHLIST_STRESS`; `REVIEW_SATELLITE` |
| `alpha_regime_blend_dynamic_v4_smooth` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | `REJECTED_STRESS`; not in survivor registry |
| `alpha_rolling_ic_dynamic_v4_smooth` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | Not stress tested |
| `alpha_hybrid_adaptive_v4_smooth` | `LB20, LB10, VoV10, IRHD1, TC20, Down1` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | `WATCHLIST_STRESS`; `REVIEW_SATELLITE` |

## Component Weight Context

In the alpha pool, the LOW_BREADTH components had meaningful base weights:

| Component | Horizon | Health Score | Pool Weight | Pass Rate | Avg Effective Mean IC | Best Regime |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `LB20` | 20 | 87 | 0.172902 | 0.857143 | 0.049249 | `benchmark_trend_regime=DOWNTREND` |
| `LB10` | 10 | 72 | 0.143091 | 0.928571 | 0.041829 | `drawdown_regime=HIGH_DRAWDOWN` |

Average dynamic weights:

| Dynamic Alpha | LB20 Avg Weight | LB10 Avg Weight |
| --- | ---: | ---: |
| `alpha_decay_aware_dynamic_v3` | 0.172902 | 0.143091 |
| `alpha_hybrid_adaptive_v3` | 0.172902 | 0.143091 |
| `alpha_regime_blend_dynamic_v3` | 0.164341 | 0.140167 |
| `alpha_rolling_ic_dynamic_v3` | 0.029621 | 0.023668 |

The rolling-IC dynamic alpha assigned very small weights to LOW_BREADTH, so in that blend the component was mostly a passenger.

## Active / Inactive State Coverage

The LOW_BREADTH component had:

- active dates: 636
- inactive dates: 1,462
- active/inactive transition dates: 153

This is not an extremely rare state, but it is still conditional. Active dates represent roughly 30% of the observed date range.

Inactive handling had an important construction effect:

- At the raw signal level, inactive dates were neutralized.
- In pure LOW_BREADTH constructed alphas, neutral inactive rows often became no-dispersion rows after cross-sectional z-scoring, effectively producing no usable exposure.
- In blended alphas, non-LOW_BREADTH components continued to provide exposure during LOW_BREADTH-inactive periods.

This means inactive handling did not behave identically across alpha types. Pure conditional sleeves became sparse; blended alphas became broad alphas with a conditional component.

## Attribution Findings

### Pure LOW_BREADTH Alphas

The pure LOW_BREADTH alphas were:

- `alpha_equal_weight_research_v1`
- `alpha_health_weighted_research_v1`
- `alpha_regime_aware_research_v1`
- `alpha_smooth_regime_weighted_v2`

For equal-weight and health-weighted versions, the full alpha and LOW_BREADTH-only component were effectively the same:

| Metric | Approximate Result |
| --- | ---: |
| Mean IC at h20 | 0.0501 |
| IC IR | 0.2417 |
| WFV-like persistence | 0.75 |
| Diagnostic Sharpe | 0.3023 |
| Diagnostic max drawdown | -0.4032 |
| Turnover proxy | 5.30 |

Interpretation:

- LOW_BREADTH showed real signal-level conditional IC.
- Pure conditional sleeves were not construction-viable because of high missingness / sparse exposure and high turnover.
- The regime-aware pure version had stronger active-period IC but even lower exposure.

This supports LOW_BREADTH as a conditional research component, not as a standalone universal alpha.

### Diversified And Persistence Blends

For `alpha_diversified_research_v2`:

| Comparison | Full | Without LOW_BREADTH | Marginal Effect |
| --- | ---: | ---: | ---: |
| Mean IC | 0.0124 | 0.0084 | +0.0040 |
| IC IR | 0.0665 | 0.0450 | +0.0215 |
| WFV-like persistence | 0.75 | 0.25 | +0.50 |
| Turnover proxy | 20.24 | 17.95 | +2.30 |
| Diagnostic Sharpe | 0.2748 | 0.4455 | -0.1707 |

For `alpha_persistence_blend_v2`:

| Comparison | Full | Without LOW_BREADTH | Marginal Effect |
| --- | ---: | ---: | ---: |
| Mean IC | 0.0122 | 0.0090 | +0.0032 |
| IC IR | 0.0648 | 0.0457 | +0.0190 |
| WFV-like persistence | 0.75 | 0.25 | +0.50 |
| Turnover proxy | 17.12 | 18.42 | -1.30 |
| Diagnostic Sharpe | 0.2592 | 0.4173 | -0.1581 |

Interpretation:

- LOW_BREADTH improved IC and WFV-like persistence in these blends.
- It did not improve diagnostic rank-spread Sharpe.
- The blends still failed stress because of high turnover and cost sensitivity.
- LOW_BREADTH was additive for IC but not sufficient for construction or stress robustness.

### Raw Dynamic Alphas

Raw v3 dynamic alphas showed modest IC contribution from LOW_BREADTH:

| Alpha | Mean IC Delta vs No LOW_BREADTH | IC IR Delta | Sharpe Delta | Turnover Delta |
| --- | ---: | ---: | ---: | ---: |
| `alpha_decay_aware_dynamic_v3` | +0.0030 | +0.0019 | -0.2792 | +1.3520 |
| `alpha_regime_blend_dynamic_v3` | +0.0031 | +0.0000 | -0.2877 | +1.3642 |
| `alpha_rolling_ic_dynamic_v3` | +0.0013 | +0.0110 | -0.0122 | +0.2921 |
| `alpha_hybrid_adaptive_v3` | +0.0004 | -0.0118 | -0.2490 | +0.5553 |

Interpretation:

- LOW_BREADTH contributed small positive IC to most raw dynamic blends.
- It generally increased turnover.
- It did not improve diagnostic Sharpe.
- Raw v3 alphas remained high-turnover and were rejected at construction quality.

### Turnover-Controlled v4 Smooth Alphas

The v4 smooth alphas reduced turnover substantially, but LOW_BREADTH's marginal contribution became smaller and more mixed:

| Alpha | Primary Horizon | Mean IC Delta vs No LOW_BREADTH | IC IR Delta | Sharpe Delta | Turnover Delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | +0.0003 | -0.0029 | -0.0733 | +0.0028 |
| `alpha_regime_blend_dynamic_v4_smooth` | 5 | +0.0006 | -0.0018 | -0.1147 | +0.0008 |
| `alpha_rolling_ic_dynamic_v4_smooth` | 20 | +0.0015 | +0.0105 | +0.0191 | -0.0013 |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | -0.0002 | -0.0045 | -0.0541 | -0.0224 |

Interpretation:

- Smoothing and turnover control made the alphas more construction-viable.
- After smoothing, LOW_BREADTH's marginal signal contribution was small.
- LOW_BREADTH did not explain downstream stress survival.
- In h5 stress-selected v4 alphas, the LOW_BREADTH component alone was weak or negative at that horizon.

This suggests that LOW_BREADTH is more useful as an h10/h20 conditional trend-quality component than as a contributor to h5 constructed-alpha stress candidates.

## Active vs Inactive Diagnostics

Across full constructed alphas, active LOW_BREADTH dates generally had better IC than inactive dates.

| Alpha | Active Mean IC | Inactive Mean IC | Active - Inactive | Active Sharpe | Inactive Sharpe |
| --- | ---: | ---: | ---: | ---: | ---: |
| `alpha_diversified_research_v2` | 0.0524 | -0.0055 | +0.0579 | 0.3778 | 0.2143 |
| `alpha_persistence_blend_v2` | 0.0320 | 0.0034 | +0.0286 | 0.4022 | 0.1726 |
| `alpha_decay_aware_dynamic_v3` | 0.0502 | 0.0225 | +0.0277 | 0.5650 | 0.5094 |
| `alpha_regime_blend_dynamic_v3` | 0.0516 | 0.0246 | +0.0271 | 0.6212 | 0.6044 |
| `alpha_hybrid_adaptive_v3` | 0.0459 | 0.0208 | +0.0251 | 0.6362 | 0.5011 |
| `alpha_decay_aware_dynamic_v4_smooth` | 0.0231 | 0.0033 | +0.0198 | 1.0080 | 0.3097 |
| `alpha_regime_blend_dynamic_v4_smooth` | 0.0238 | 0.0040 | +0.0198 | 0.9969 | 0.3331 |
| `alpha_rolling_ic_dynamic_v4_smooth` | 0.0218 | 0.0038 | +0.0180 | 1.3183 | 0.2591 |
| `alpha_hybrid_adaptive_v4_smooth` | 0.0224 | 0.0029 | +0.0195 | 1.1289 | 0.2900 |

Interpretation:

- LOW_BREADTH-active periods were consistently better than inactive periods for full alphas.
- The v4 smooth alphas had much better diagnostic Sharpe during LOW_BREADTH-active periods than inactive periods.
- This supports LOW_BREADTH as a context/stabilizer layer.
- It does not prove that LOW_BREADTH alone is sufficient as an alpha sleeve.

## Stress Attribution

Five LOW_BREADTH-containing alphas reached 07 stress:

| Alpha | Horizon | Stress Status | Promotion Decision | Pass Rate | Worst Degradation | Turnover Risk |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `alpha_regime_blend_dynamic_v4_smooth` | 5 | `REJECTED_STRESS` | `REJECT` | 0.722222 | 0.803514 | `LOW_TURNOVER_RISK` |
| `alpha_persistence_blend_v2` | 10 | `REJECTED_STRESS` | `REJECT_HIGH_TURNOVER` | 0.666667 | 3.481160 | `HIGH_TURNOVER_RISK` |
| `alpha_diversified_research_v2` | 20 | `REJECTED_STRESS` | `REJECT_HIGH_TURNOVER` | 0.611111 | 3.473657 | `HIGH_TURNOVER_RISK` |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `WATCHLIST_STRESS` | `REVIEW_SATELLITE` | 0.555556 | 0.601208 | `LOW_TURNOVER_RISK` |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `WATCHLIST_STRESS` | `REVIEW_SATELLITE` | 0.555556 | 0.641822 | `LOW_TURNOVER_RISK` |

Stress observations:

- LOW_BREADTH did not produce an approved stress survivor in any constructed alpha that contained it.
- The unsmoothed blends failed mostly because of high turnover and cost sensitivity.
- The smoothed v4 blends reduced turnover but still had low stress pass rates or catastrophic degradation.
- LOW_BREADTH did not reliably reduce drawdowns after construction.
- It improved active-state IC, but that did not translate into sufficient stress robustness.

The sole 07 `APPROVED_STRESS` survivor was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`

That alpha did not include `smooth_trend_persistence_60_low_breadth`.

## Blend Interaction Analysis

### Does LOW_BREADTH improve another component?

Partially. In diversified, persistence, and raw dynamic blends, LOW_BREADTH improved mean IC and WFV-like persistence. Active-date diagnostics also showed better behavior during LOW_BREADTH periods.

### Does another component carry LOW_BREADTH?

Yes, in several constructed alphas. The dynamic alphas retained broad exposure through non-LOW_BREADTH components during inactive periods. In v4 smooth alphas, LOW_BREADTH's marginal contribution became small, while the broader blend and turnover controls dominated final behavior.

### Is LOW_BREADTH independently useful?

It is independently useful as a signal-level conditional component at h10/h20. It is not independently viable as a standalone constructed alpha under current construction/stress standards because pure LOW_BREADTH sleeves were sparse and high-turnover.

### Does blending hide instability?

Sometimes. Blending hides the pure conditional component's sparse exposure problem, but it also dilutes the active-state edge. The result is a broader alpha that may look construction-viable but no longer clearly preserves the original conditional behavior.

## Behavioral Summary

Structurally, LOW_BREADTH appears to act as:

- a conditional trend-quality layer,
- an active-state IC stabilizer,
- a weak-to-moderate contributor to WFV-like persistence,
- and a component whose benefits are sensitive to construction method and horizon.

It does not currently behave like:

- a standalone core alpha,
- a robust stress reducer,
- or an independently sufficient survivor component.

## Conditionality Assessment

Best classification:

`context filter / stabilizer with conditional alpha evidence`

Secondary classification:

`not a standalone core candidate`

LOW_BREADTH is not best described as an accidental passenger, because active-period IC consistently improved and several blends showed positive marginal IC contribution. However, it is also not a proven true conditional alpha sleeve, because pure LOW_BREADTH constructions failed construction quality and LOW_BREADTH-containing alphas did not survive 07 stress as core candidates.

## Research Recommendation

Recommended action:

`isolate into separate conditional framework`

Rationale:

- Continue researching LOW_BREADTH, but not by forcing it through the current universal-alpha construction path.
- Treat it as a conditional component that needs active-state constructed-alpha diagnostics.
- Avoid promoting it as core or using constructed-alpha performance as proof of component quality.
- Require additional stress validation before any portfolio or survivor-framework consideration.

The next research step should be a dedicated conditional-alpha prototype for LOW_BREADTH that compares:

- state-gated sleeve,
- neutral inactive sleeve,
- masked inactive diagnostic,
- and blended broad-alpha versions.

The objective should be to determine whether LOW_BREADTH can preserve its active-state benefit while reducing turnover and avoiding stress degradation.

## Final Conclusion

LOW_BREADTH contributed genuine conditional signal behavior before construction and retained some active-state value after construction. It improved active-period IC across most alphas and modestly improved marginal IC in several blends.

However, after construction it did not become a core survivor. Pure LOW_BREADTH alphas were too sparse or high-turnover, while blended alphas either failed stress, were carried by other components, or diluted the original conditional edge.

The correct interpretation is not rejection and not promotion. LOW_BREADTH should remain a watchlist conditional layer and be isolated into the future Conditional-Alpha Framework for cleaner active-state construction, stress attribution, and satellite classification research.
