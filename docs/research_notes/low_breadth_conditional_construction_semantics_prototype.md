# LOW_BREADTH Conditional Construction Semantics Prototype

## 1. Executive Takeaway

This note documents a research-only Conditional Construction Semantics Prototype for:

- `smooth_trend_persistence_60_low_breadth`

Final decision:

`context filter only`

Secondary research candidate:

`exposure modifier`

LOW_BREADTH continues to look informative, but not as a standalone constructed alpha. The strongest evidence is contextual: it identifies dates and states where v4 smoothed constructed alphas behave better, especially around collapsed breadth, downtrends, volatility spikes, and panic/liquidity stress.

Active-only and state-gated variants improve IC diagnostics, but they also create sparse exposure and transition risk. Exposure-modifier and risk-suppressor variants improve drawdown and left-tail proxies, but those improvements mostly come from scaling exposure, not from proving stronger asset ranking. Blended variants remain useful for context attribution, but can camouflage the component's standalone weakness.

The appropriate next step is not promotion or rejection. LOW_BREADTH should remain a research-only context filter while a narrower exposure-modifier diagnostic is designed.

No production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, notebooks, ML layers, or additional conditional alphas were changed.

## 2. Prior Classification Summary

Prior research classified LOW_BREADTH as:

`context filter`

Supporting evidence:

- real conditional information
- strongest at h20
- useful during collapsed breadth, persistent downtrend, volatility spike, and panic/liquidity stress states
- improves active-period behavior inside v4 smoothed constructed alphas
- not standalone robust enough as a constructed alpha
- not part of the sole 07 stress-approved survivor
- transition-heavy activation profile

Prior signal-level evidence:

| Horizon | Direction | Effective Mean IC | Effective IC IR | WFV Status |
| --- | --- | ---: | ---: | --- |
| h10 | `NEGATIVE_EDGE_REVERSE_SIGNAL` | 0.031474 | 0.155966 | `APPROVED_FOR_WFV` |
| h20 | `NEGATIVE_EDGE_REVERSE_SIGNAL` | 0.050074 | 0.241726 | `APPROVED_WFV` at h20 bridge |

## 3. Prototype Variants Tested

The prototype compared seven research-only semantics:

| Variant | Diagnostic Meaning |
| --- | --- |
| Neutral inactive | Current-compatible LOW_BREADTH signal with inactive dates neutral/flat. |
| Masked active-only | LOW_BREADTH evaluated only when active. |
| State-gated | LOW_BREADTH retained only when active inside confirmed fragile states. |
| Exposure modifier | V4 smoothed alpha exposure scaled up during LOW_BREADTH active dates and down otherwise. |
| Risk suppressor | V4 smoothed alpha exposure reduced during weak breadth/stress states. |
| Blended | Existing v4 smoothed constructed alphas containing LOW_BREADTH. |
| No-LOW_BREADTH counterfactual | Prior diagnostic counterfactuals with LOW_BREADTH removed or approximated away. |

Important methodological note:

Date-level positive exposure scaling does not change same-day cross-sectional Spearman IC, because ranks are unchanged. Exposure-modifier and risk-suppressor variants are therefore evaluated mainly through spread-return, Sharpe, drawdown, left-tail, exposure, and transition proxies.

## 4. Neutral Inactive Findings

The neutral inactive signal matched the current-compatible LOW_BREADTH representation.

| Horizon | Effective Mean IC | Effective IC IR | Positive Effective IC Rate | Exposure Rate | Turnover Proxy |
| --- | ---: | ---: | ---: | ---: | ---: |
| h10 | 0.031474 | 0.155966 | 54.72% | 30.31% | 0.0955 |
| h20 | 0.050074 | 0.241726 | 57.55% | 30.31% | 0.0955 |

Interpretation:

- Neutral inactive handling preserves compatibility and confirms h20 superiority.
- It does not create full economic exposure; only about 30% of dates contain active signal content.
- It may understate active-state behavior in broad diagnostics while still creating rank/dispersion artifacts in pure sleeves.

Observed risk:

`neutral inactive smoothing illusion`

Neutral inactive dates can make the series look structurally compatible while pure conditional sleeves still behave sparsely.

## 5. Masked Active-Only Findings

Masked active-only used only LOW_BREADTH active dates.

| Horizon | Effective Mean IC | Effective IC IR | Positive Effective IC Rate | Exposure Rate | Turnover Proxy |
| --- | ---: | ---: | ---: | ---: | ---: |
| h10 | 0.031474 | 0.155966 | 54.72% | 30.31% | 0.1326 |
| h20 | 0.050074 | 0.241726 | 57.55% | 30.31% | 0.1326 |

Interpretation:

- Active-only masking does not change IC because the neutral inactive version already has no usable rank dispersion on inactive dates.
- It does expose the true sparse nature of the component.
- Turnover proxy rises versus neutral inactive because masked panels create sharper on/off boundaries.

Observed risk:

`active-only survivorship bias`

Active-only evaluation is useful diagnostically, but it must be paired with active-window coverage and transition analysis.

## 6. State-Gated Findings

The state-gated signal required active LOW_BREADTH plus one of:

- collapsed breadth
- persistent downtrend
- volatility spike
- panic/liquidity stress

Gate overlap:

| Metric | Value |
| --- | ---: |
| Fragile-gate dates | 819 |
| LOW_BREADTH active and gated dates | 636 |
| Share of LOW_BREADTH active dates captured by gate | 100.00% |
| Share of fragile-gate dates with LOW_BREADTH active | 77.66% |

Isolated state-gated signal results were identical to neutral inactive IC because all active LOW_BREADTH dates were captured by the fragile gate:

| Horizon | Effective Mean IC | Effective IC IR | Positive Effective IC Rate | Exposure Rate | Turnover Proxy |
| --- | ---: | ---: | ---: | ---: | ---: |
| h10 | 0.031474 | 0.155966 | 54.72% | 30.31% | 0.0926 |
| h20 | 0.050074 | 0.241726 | 57.55% | 30.31% | 0.0926 |

When applied as a gated exposure diagnostic to v4 smoothed alphas:

| Horizon | Avg Mean IC | Avg IC IR | Avg Sharpe | Avg Max Drawdown | Exposure Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| h10 | 0.044029 | 0.280514 | 0.706885 | -0.277654 | 37.61% |
| h20 | 0.044085 | 0.277810 | 0.706885 | -0.277654 | 37.61% |

Interpretation:

- State gating sharpens IC and reduces drawdown in the constructed-alpha diagnostic.
- The benefit comes with sparse exposure: roughly 62% zero-exposure dates in the proxy.
- It may be useful for research, but it is not yet a complete construction answer.

Observed risk:

`state-gating overfit`

The gate captures all current LOW_BREADTH active dates. That is convenient but may be too fitted to the current context definition.

## 7. Exposure Modifier Findings

The exposure-modifier proxy scaled v4 smoothed alpha exposure up during LOW_BREADTH active dates and down otherwise. This was a research proxy, not a portfolio implementation.

| Variant | Mean Spread | Sharpe | Max Drawdown | Left-Tail CVaR 5% | Avg Exposure Scalar |
| --- | ---: | ---: | ---: | ---: | ---: |
| Blended current | 0.000311 | 0.533358 | -0.446583 | -0.020475 | 1.000000 |
| Exposure modifier | 0.000296 | 0.547425 | -0.417493 | -0.019725 | 0.903772 |

Interpretation:

- Exposure modification slightly improved Sharpe, max drawdown, and left-tail behavior.
- Mean spread declined modestly.
- The result is consistent with LOW_BREADTH as a context filter, not as a rank signal.
- The improvement may partly reflect lower average exposure, so it should not be called alpha.

Observed risk:

`accidental risk reduction mistaken for alpha`

This variant is promising enough to study next, but only with explicit exposure and benchmark beta attribution.

## 8. Risk Suppressor Findings

The risk-suppressor proxy reduced v4 smoothed alpha exposure during weak breadth or stress states.

| Variant | Mean Spread | Sharpe | Max Drawdown | Left-Tail CVaR 5% | Avg Exposure Scalar |
| --- | ---: | ---: | ---: | ---: | ---: |
| Blended current | 0.000311 | 0.533358 | -0.446583 | -0.020475 | 1.000000 |
| Risk suppressor | 0.000240 | 0.532061 | -0.323694 | -0.015772 | 0.774662 |

Interpretation:

- Risk suppression materially improved max drawdown and left-tail behavior.
- Mean spread declined meaningfully.
- Sharpe was essentially unchanged.
- This is useful evidence for defensive semantics, but it may simply be exposure reduction.

Observed risk:

`improves drawdown but destroys return`

The variant reduced damage, but at a cost to average spread. It should not be preferred until return sacrifice and beta reduction are decomposed.

## 9. Blended Findings

The blended variant is the current v4 smoothed constructed-alpha behavior.

Average v4 smoothed alpha results:

| Horizon | Avg Mean IC | Avg IC IR | Avg Sharpe | Avg Max Drawdown | Active Mean IC | Inactive Mean IC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| h10 | 0.015034 | 0.100726 | 0.533358 | -0.446583 | 0.036151 | 0.005589 |
| h20 | 0.015781 | 0.108056 | 0.533358 | -0.446583 | 0.038731 | 0.005444 |

Interpretation:

- Blended alphas retain a clear active/inactive improvement.
- LOW_BREADTH-active dates are better than inactive dates for the blends.
- The blended construction dilutes the pure conditional signal.
- Existing blend behavior is useful for attribution but insufficient for proving standalone component value.

Observed risk:

`blend camouflage`

The blend can look viable while stronger non-LOW_BREADTH components or smoothing carry the constructed alpha.

## 10. No-LOW_BREADTH Counterfactual Findings

Prior attribution work compared full alphas against no-LOW_BREADTH approximations.

| Blend Group | Mean IC Effect From LOW_BREADTH | Persistence Effect | Sharpe Effect | Turnover Effect |
| --- | ---: | ---: | ---: | ---: |
| `alpha_diversified_research_v2` | +0.0040 | +0.50 | -0.1707 | +2.30 |
| `alpha_persistence_blend_v2` | +0.0032 | +0.50 | -0.1581 | -1.30 |
| raw v3 dynamic alphas | mostly small positive | mixed | mostly negative | mostly higher |
| v4 smooth alphas | small and mixed | mixed | small/mixed | near neutral |

Interpretation:

- LOW_BREADTH is not an accidental passenger.
- It improves active-period behavior and contributes marginal IC in several blends.
- It is not the dominant source of v4 constructed-alpha viability.
- Its value depends heavily on construction semantics.

## 11. h20 vs h10 Comparison

Isolated LOW_BREADTH:

| Horizon | Effective Mean IC | Effective IC IR | Positive Effective IC Rate |
| --- | ---: | ---: | ---: |
| h10 | 0.031474 | 0.155966 | 54.72% |
| h20 | 0.050074 | 0.241726 | 57.55% |

V4 blended active-period behavior:

| Horizon | Avg Mean IC | Active Mean IC | Inactive Mean IC |
| --- | ---: | ---: | ---: |
| h10 | 0.015034 | 0.036151 | 0.005589 |
| h20 | 0.015781 | 0.038731 | 0.005444 |

Interpretation:

- h20 remains structurally better than h10.
- h10 is not invalid, but it is weaker and less compelling.
- Any next LOW_BREADTH semantics prototype should use h20 as primary and h10 only as a secondary robustness check.

## 12. State / Regime Attribution Table

The table below summarizes h20 state attribution for current blended v4 alphas and the state-gated exposure diagnostic.

| State Axis | State | Blended Avg h20 IC | State-Gated Avg h20 IC | Interpretation |
| --- | --- | ---: | ---: | --- |
| Stress | `PANIC_LIQUIDITY_STRESS` | 0.096089 | 0.096089 | Strongest recurring fragile state. |
| Trend | `PERSISTENT_DOWNTREND` | 0.083607 | 0.083607 | Strong match to LOW_BREADTH context-filter role. |
| Volatility | `VOLATILITY_SPIKE` | 0.060559 | 0.060559 | Useful stress-volatility context. |
| Breadth | `COLLAPSED_BREADTH` | 0.041188 | 0.041188 | Intended state works, but not standalone. |
| Breadth | `WEAKENING_BREADTH` | 0.038663 | 0.242697 | High gated IC but only about 10 observations; sample-risk warning. |
| Volatility | `VOLATILITY_NORMALIZATION` | 0.021075 | 0.100164 | Positive post-stress signal, but needs transition validation. |
| Trend | `TREND_TRANSITION` | 0.022630 | 0.039505 | Moderate evidence. |
| Stress | `DRAWDOWN_ACCELERATION` | 0.011096 | 0.018416 | Less compelling than panic/liquidity stress. |
| Stress | `RECOVERY_PHASE` | -0.007412 | 0.050965 | Gated result improves, but sample and deactivation timing matter. |
| Breadth | `STRONG_BREADTH` | -0.007994 | 0.087350 | Possible false-state artifact; gated sample is small and not a target state. |

Interpretation:

- The robust states remain panic/liquidity stress, persistent downtrend, volatility spike, and collapsed breadth.
- Some state-gated results look strong in non-target states because gating leaves only selected dates; these should be treated as sample-conditioned diagnostics, not evidence of broad robustness.

## 13. Stress Behavior Summary

Existing stress outcomes for LOW_BREADTH-containing v4 smoothed alphas:

| Alpha | Horizon | Stress Status | Pass Rate | Worst Degradation | Turnover Risk |
| --- | ---: | --- | ---: | ---: | --- |
| `alpha_regime_blend_dynamic_v4_smooth` | 5 | `REJECTED_STRESS` | 0.722222 | 0.803514 | `LOW_TURNOVER_RISK` |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `WATCHLIST_STRESS` | 0.555556 | 0.601208 | `LOW_TURNOVER_RISK` |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `WATCHLIST_STRESS` | 0.555556 | 0.641822 | `LOW_TURNOVER_RISK` |

Prototype stress interpretation:

- Risk suppressor improved max drawdown proxy from -0.446583 to -0.323694.
- Exposure modifier improved max drawdown proxy from -0.446583 to -0.417493.
- State-gated exposure improved max drawdown proxy to -0.277654 but introduced sparse exposure.
- None of these diagnostics replaces official stress testing.
- Improvements should be treated as risk-scaling evidence, not alpha evidence.

## 14. Turnover And Transition Stability Summary

Activation profile:

| Metric | Value |
| --- | ---: |
| Active dates | 636 |
| Inactive dates | 1,462 |
| Active ratio | 30.31% |
| Activation episodes | 76 |
| Transitions | 152 |
| Average episode length | 8.37 days |
| Median episode length | 3 days |
| Maximum episode length | 49 days |

Turnover / exposure diagnostics:

| Variant | Exposure Rate / Scalar | Turnover / Stability Observation |
| --- | ---: | --- |
| Neutral inactive | 30.31% exposure rate | Lower isolated turnover proxy than masked active-only. |
| Masked active-only | 30.31% exposure rate | Higher isolated turnover proxy due sharper on/off boundaries. |
| State-gated isolated | 30.31% exposure rate | Similar to neutral because gate captures all active dates. |
| Blended current | 98.57% exposure rate | Broad exposure remains through non-LOW_BREADTH components. |
| State-gated exposure | 37.61% exposure rate | Better drawdown/IC diagnostics but sparse and episodic. |
| Exposure modifier | 0.9038 avg exposure scalar | Slight drawdown improvement without zero exposure. |
| Risk suppressor | 0.7747 avg exposure scalar | Larger drawdown improvement with meaningful return sacrifice. |

Interpretation:

- Sparse/gated variants improve some metrics but increase semantic complexity.
- Exposure modifier is less disruptive than state gating.
- Risk suppression is defensive but may over-suppress returns.

## 15. Failure Modes Observed

| Failure Mode | Evidence | Assessment |
| --- | --- | --- |
| Neutral inactive smoothing illusion | Neutral version is compatible, but exposure exists on only 30.31% of dates. | Present. |
| Active-only survivorship bias | Active-only IC improves clarity but ignores inactive opportunity cost. | Present risk. |
| State-gating overfit | Fragile gate captures 100% of LOW_BREADTH active dates. | Present risk. |
| False defensive activation | Strong breadth gated result appears positive but sample-conditioned and not target-state evidence. | Watch item. |
| Delayed activation | Prior transition analysis showed strongest isolated h20 behavior late in active episodes. | Present. |
| Transition whipsaw | 76 episodes, 152 transitions, median episode length 3 days. | Present. |
| Excessive turnover | Masked/gated semantics can sharpen on/off boundaries. | Present risk. |
| Hidden beta exposure | Stress/downtrend states dominate benefit. | Needs beta/state attribution. |
| Accidental risk reduction mistaken for alpha | Exposure/risk suppressor benefits mostly come from scaling exposure. | Present. |
| Blend camouflage | Blended alphas show value, but LOW_BREADTH is not the dominant viability source. | Present. |
| Improves drawdown but destroys return | Risk suppressor improves drawdown but lowers mean spread. | Present. |
| Improves IC but worsens stress behavior | State-gated IC improves but sparse exposure would need stress validation. | Present risk. |
| h20/h10 instability | h20 is consistently better; h10 is useful but weaker. | Manageable. |

## 16. Recommended Construction Semantics

Primary recommendation:

`context filter only`

Rationale:

- LOW_BREADTH's strongest evidence is state identification, not standalone alpha construction.
- Active periods are consistently higher quality for v4 blends.
- h20 signal-level evidence is real, but pure conditional construction remains sparse and transition-heavy.
- Exposure/risk variants improve drawdown proxies, but do not yet prove alpha selection.
- Blended variants show usefulness but can camouflage the source of improvement.

Secondary research path:

`exposure modifier`

Why:

- It improved Sharpe modestly and reduced drawdown/left-tail proxies without fully zeroing exposure.
- It fits the context-filter identity better than direct standalone ranking.
- It is less sparse than state-gated exposure and less return-destructive than broad risk suppression.

Do not select yet:

- `active-state signal`: useful diagnostically, but too sparse/transition-heavy.
- `state-gated context filter`: promising but too fitted to current active dates.
- `risk suppressor`: drawdown improvement is real, but return sacrifice and beta effects need decomposition.
- `blend-only stabilizer`: useful as a baseline, but not enough to understand semantics.
- `reject from Conditional-Alpha Framework`: too harsh; the context evidence is meaningful.

## 17. Next Research Step

Next concrete diagnostic:

`LOW_BREADTH Exposure Modifier Sidecar Diagnostic`

Scope:

- research-only
- h20 primary, h10 secondary
- no production integration
- no gate/schema/promotion changes
- no survivor or portfolio changes

Questions to answer:

- Does exposure modification improve left-tail risk after controlling for average exposure?
- Is the improvement still present after benchmark beta attribution?
- Does it reduce stress degradation without suppressing recovery returns?
- Can transition smoothing reduce whipsaw without erasing the context benefit?
- Does exposure modification remain useful across WFV windows, or is it one-window dominated?

Recommended comparison set:

- blended current v4 alphas
- exposure modifier with mild scaling
- exposure modifier with transition smoothing
- no-LOW_BREADTH counterfactual
- risk suppressor as defensive benchmark

## Final Conclusion

LOW_BREADTH should remain in the Conditional-Alpha Framework as a context filter, not as a standalone conditional alpha. The prototype confirms that its value is most visible when it describes the environment around other alphas.

The most promising future semantic is an exposure-modifier sidecar, but only as research. The current evidence is not sufficient to change construction logic, promote a new sleeve, or alter stress/survivor rules.

Project Underdog should continue treating LOW_BREADTH as useful conditional information while keeping the official validation and survivor standards unchanged.
