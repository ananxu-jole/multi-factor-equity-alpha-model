# LOW_BREADTH Exposure Modifier Sidecar Diagnostic

## 1. Executive Takeaway

This note documents a research-only sidecar diagnostic for the LOW_BREADTH exposure-modifier path.

Component:

- `smooth_trend_persistence_60_low_breadth`

Final classification:

`useful but mostly generic de-risking`

LOW_BREADTH exposure modification reduced drawdown and left-tail proxies relative to the no-modifier baseline. However, it did not outperform a constant equal-exposure reduction and did not outperform the average randomized equal-frequency exposure reduction on Sharpe, mean spread, or max drawdown.

The evidence suggests that LOW_BREADTH has real stress-aligned timing behavior, but most of the observed improvement comes from being less exposed, not from uniquely intelligent exposure timing. The exposure-modifier path should remain research-only and should not be promoted into construction, portfolio, or survivor logic.

No production pipelines, schemas, gates, thresholds, survivor lists, portfolio logic, validation logic, notebooks, ML layers, or expansion logic were changed.

## 2. Prior LOW_BREADTH Construction Semantics Summary

Prior notes classified LOW_BREADTH as:

- primary role: `context filter only`
- secondary research path: `exposure modifier`

The Conditional Construction Semantics Prototype found:

- LOW_BREADTH is strongest at h20.
- It improves active-period behavior inside v4 smoothed constructed alphas.
- It is not robust enough as a standalone constructed alpha.
- Active-only and state-gated variants sharpen IC but create sparse exposure and transition risk.
- Exposure modification modestly improved drawdown and left-tail proxies.
- That improvement required a sidecar test to separate timing value from generic de-risking.

This diagnostic addresses that last point.

## 3. Exposure-Modifier Variants Tested

The diagnostic used v4 smoothed constructed alpha spread-return proxies averaged across:

- `alpha_decay_aware_dynamic_v4_smooth`
- `alpha_regime_blend_dynamic_v4_smooth`
- `alpha_rolling_ic_dynamic_v4_smooth`
- `alpha_hybrid_adaptive_v4_smooth`

Variants:

| Variant | Description |
| --- | --- |
| No-modifier baseline | Original v4 smoothed alpha behavior. |
| LOW_BREADTH modifier | Exposure reduced to 50% during LOW_BREADTH-active dates. |
| Constant equal exposure | Constant scale matching the LOW_BREADTH modifier's average exposure. |
| Randomized equal frequency | Same reduction frequency and average exposure as LOW_BREADTH, randomly timed over 200 schedules. |
| Volatility-only modifier | Exposure reduced during rising-volatility or volatility-spike states. |
| Drawdown-only modifier | Exposure reduced during drawdown-acceleration or panic/liquidity stress states. |
| Full LOW_BREADTH blend/context reference | Existing LOW_BREADTH-containing v4 constructed alphas, included as the baseline source panels. |

Important methodological note:

This diagnostic is not an official backtest, WFV run, stress run, or portfolio test. It is a research-only spread-return proxy designed to compare exposure timing semantics.

## 4. LOW_BREADTH Modifier Findings

The LOW_BREADTH modifier reduced exposure during LOW_BREADTH-active dates.

| Metric | No Modifier | LOW_BREADTH Modifier | Change |
| --- | ---: | ---: | ---: |
| Mean spread | 0.000311 | 0.000249 | -0.000063 |
| Volatility | 0.009062 | 0.007977 | -0.001085 |
| Sharpe | 0.545462 | 0.494645 | -0.050816 |
| Max drawdown | -0.447314 | -0.389269 | +0.058045 |
| Left-tail CVaR 5% | -0.020047 | -0.017340 | +0.002707 |
| Average exposure scale | 1.000000 | 0.846228 | -0.153772 |
| Reduction frequency | 0.00% | 30.75% | +30.75% |
| Transition proxy | 0.000000 | 0.036750 | +0.036750 |

Interpretation:

- LOW_BREADTH reduced volatility, max drawdown, and left-tail loss.
- It also reduced mean spread and Sharpe.
- The improvement is defensive, not alpha-generating.
- The result is consistent with context-aware de-risking, but not sufficient to prove timing skill.

## 5. Constant Exposure Reduction Comparison

The constant equal-exposure variant used the same average exposure scale as the LOW_BREADTH modifier.

| Metric | LOW_BREADTH Modifier | Constant Equal Exposure | LOW_BREADTH - Constant |
| --- | ---: | ---: | ---: |
| Mean spread | 0.000249 | 0.000263 | -0.000015 |
| Volatility | 0.007977 | 0.007669 | +0.000308 |
| Sharpe | 0.494645 | 0.545462 | -0.050816 |
| Max drawdown | -0.389269 | -0.392217 | +0.002948 |
| Left-tail CVaR 5% | -0.017340 | -0.016964 | -0.000376 |
| Transition proxy | 0.036750 | 0.000000 | +0.036750 |

Interpretation:

- LOW_BREADTH did not outperform constant exposure reduction on Sharpe or mean spread.
- Max drawdown was only marginally better than constant exposure.
- Left-tail CVaR was slightly worse than constant exposure.
- This is the strongest evidence that much of the improvement is generic de-risking.

## 6. Randomized Exposure Reduction Comparison

The randomized variant matched the LOW_BREADTH modifier's average exposure and reduction frequency, but randomized timing over 200 schedules.

| Metric | LOW_BREADTH Modifier | Random Equal Frequency Avg | LOW_BREADTH - Random |
| --- | ---: | ---: | ---: |
| Mean spread | 0.000249 | 0.000264 | -0.000015 |
| Volatility | 0.007977 | 0.007930 | +0.000047 |
| Sharpe | 0.494645 | 0.527677 | -0.033032 |
| Max drawdown | -0.389269 | -0.389367 | +0.000099 |
| Left-tail CVaR 5% | -0.017340 | -0.017694 | +0.000354 |
| Transition proxy | 0.036750 | 0.213673 | -0.176923 |

Interpretation:

- LOW_BREADTH had similar max drawdown to random timing.
- LOW_BREADTH had better left-tail CVaR than random timing.
- LOW_BREADTH had lower Sharpe and mean spread than random timing.
- LOW_BREADTH had much lower transition instability than random timing.

This supports a narrow conclusion: LOW_BREADTH timing is cleaner than random switching, but it does not generate superior overall risk-adjusted spread-return behavior.

## 7. Volatility-Only Comparison

The volatility-only modifier reduced exposure during rising-volatility and volatility-spike states.

| Metric | LOW_BREADTH Modifier | Volatility-Only Modifier |
| --- | ---: | ---: |
| Mean spread | 0.000249 | 0.000218 |
| Sharpe | 0.494645 | 0.441540 |
| Max drawdown | -0.389269 | -0.417569 |
| Left-tail CVaR 5% | -0.017340 | -0.016767 |
| Average exposure scale | 0.846228 | 0.860977 |
| Reduction frequency | 30.75% | 27.80% |

Interpretation:

- LOW_BREADTH outperformed volatility-only on mean spread, Sharpe, and max drawdown.
- Volatility-only had slightly better left-tail CVaR.
- LOW_BREADTH is not simply a volatility-spike proxy.

## 8. Drawdown-Only Comparison

The drawdown-only modifier reduced exposure during drawdown acceleration and panic/liquidity stress states.

| Metric | LOW_BREADTH Modifier | Drawdown-Only Modifier |
| --- | ---: | ---: |
| Mean spread | 0.000249 | 0.000244 |
| Sharpe | 0.494645 | 0.483857 |
| Max drawdown | -0.389269 | -0.402028 |
| Left-tail CVaR 5% | -0.017340 | -0.017185 |
| Average exposure scale | 0.846228 | 0.886122 |
| Reduction frequency | 30.75% | 22.78% |

Interpretation:

- LOW_BREADTH was slightly better than drawdown-only on mean spread, Sharpe, and max drawdown.
- Drawdown-only had slightly better left-tail CVaR.
- LOW_BREADTH is not fully redundant with drawdown-only de-risking, but the difference is modest.

## 9. No-Modifier Baseline Comparison

The no-modifier baseline had the highest mean spread and Sharpe among the deterministic variants, but the worst drawdown.

| Metric | No Modifier | LOW_BREADTH Modifier |
| --- | ---: | ---: |
| Mean spread | 0.000311 | 0.000249 |
| Sharpe | 0.545462 | 0.494645 |
| Max drawdown | -0.447314 | -0.389269 |
| Left-tail CVaR 5% | -0.020047 | -0.017340 |
| Average exposure scale | 1.000000 | 0.846228 |

Interpretation:

- LOW_BREADTH improves defensive metrics.
- It sacrifices return and Sharpe.
- It should not be described as improving alpha quality.
- It may be useful only if the research objective is defensive context control.

## 10. Full LOW_BREADTH Blend / Context Reference

The full LOW_BREADTH-containing v4 blends remain the relevant context reference:

- LOW_BREADTH-active dates previously showed stronger IC than inactive dates.
- h20 behavior was strongest in panic/liquidity stress, persistent downtrend, volatility spike, and collapsed breadth.
- LOW_BREADTH-containing alphas did not become the sole 07 stress-approved survivor.
- Current blend behavior is useful for attribution, but not proof of standalone LOW_BREADTH quality.

This sidecar confirms the same pattern from a different angle: LOW_BREADTH is contextually meaningful, but its exposure-modifier contribution is mostly defensive.

## 11. Equal-Exposure Test Results

The equal-exposure test compares LOW_BREADTH against the constant exposure reduction with identical average exposure.

Result:

- LOW_BREADTH did not outperform constant exposure reduction on Sharpe.
- LOW_BREADTH did not outperform constant exposure reduction on mean spread.
- LOW_BREADTH had only a tiny max-drawdown advantage.
- LOW_BREADTH had worse left-tail CVaR.
- LOW_BREADTH introduced transition changes that constant scaling did not.

Interpretation:

The equal-exposure test does not support strong context-aware timing value. Most of the improvement versus baseline appears explainable by lower average exposure.

## 12. Exposure Timing Test Results

Average exposure scale around stress episodes:

| Variant | Pre-Stress 10 Days | During Stress | Post-Stress 10 Days |
| --- | ---: | ---: | ---: |
| No modifier | 1.000000 | 1.000000 | 1.000000 |
| LOW_BREADTH modifier | 0.831250 | 0.676662 | 0.746296 |
| Constant equal exposure | 0.846228 | 0.846228 | 0.846228 |
| Volatility-only modifier | 0.852500 | 0.784778 | 0.750617 |
| Drawdown-only modifier | 0.906667 | 0.500000 | 0.901852 |

Interpretation:

- LOW_BREADTH does de-risk more during stress than constant scaling.
- It begins de-risking before stress episodes on average.
- It remains somewhat defensive after stress.
- Timing is directionally sensible, but the outcome metrics do not beat equal-exposure alternatives enough to call it a genuine exposure-timing edge.

## 13. Upside Preservation Results

Upside and downside behavior:

| Variant | Up-Market Mean | Down-Market Mean | Up Capture | Down Capture |
| --- | ---: | ---: | ---: | ---: |
| No modifier | 0.001538 | -0.001219 | 0.197153 | -0.147544 |
| LOW_BREADTH modifier | 0.001275 | -0.001035 | 0.163380 | -0.125235 |
| Constant equal exposure | 0.001302 | -0.001032 | 0.166836 | -0.124856 |
| Random equal frequency avg | 0.001300 | -0.001029 | 0.166585 | -0.124502 |
| Volatility-only modifier | 0.001085 | -0.000868 | 0.139065 | -0.105086 |
| Drawdown-only modifier | 0.001195 | -0.000945 | 0.153183 | -0.114394 |

Interpretation:

- LOW_BREADTH reduces downside exposure, but also reduces upside capture.
- It does not preserve upside better than constant or random equal-exposure alternatives.
- This weakens the case for unique context-aware timing.

## 14. Left-Tail Behavior Results

Left-tail CVaR 5%:

| Variant | Left-Tail CVaR 5% |
| --- | ---: |
| No modifier | -0.020047 |
| LOW_BREADTH modifier | -0.017340 |
| Constant equal exposure | -0.016964 |
| Random equal frequency avg | -0.017694 |
| Volatility-only modifier | -0.016767 |
| Drawdown-only modifier | -0.017185 |

Interpretation:

- LOW_BREADTH improves left-tail behavior versus no modifier and random timing.
- It does not beat constant equal exposure or volatility-only de-risking.
- Left-tail improvement is real but not uniquely LOW_BREADTH-specific.

## 15. Transition Cost / Whipsaw Findings

Transition proxy:

| Variant | Transition Proxy |
| --- | ---: |
| No modifier | 0.000000 |
| Constant equal exposure | 0.000000 |
| LOW_BREADTH modifier | 0.036750 |
| Volatility-only modifier | 0.015232 |
| Drawdown-only modifier | 0.038926 |
| Random equal frequency avg | 0.213673 |

Interpretation:

- LOW_BREADTH has much lower transition instability than random timing.
- It has more transition activity than volatility-only de-risking.
- It is comparable to drawdown-only de-risking.
- Transition cost is not catastrophic in this proxy, but it is a real cost versus constant exposure reduction.

## 16. h20 vs h10 Modifier Test

Persisted LOW_BREADTH signal evidence:

| Horizon | Raw Mean IC | Absolute Mean IC | Absolute IC IR | Status |
| --- | ---: | ---: | ---: | --- |
| h10 | -0.031474 | 0.031474 | 0.155966 | `APPROVED_FOR_WFV` |
| h20 | -0.050074 | 0.050074 | 0.241726 | `APPROVED_FOR_WFV` |

Interpretation:

- h20 remains the stronger signal horizon.
- The exposure modifier schedule itself is based on LOW_BREADTH activation, so h10/h20 do not create materially different de-risking calendars in this sidecar.
- If exposure-modifier research continues, h20 should remain primary and h10 should remain a secondary robustness reference.

## 17. Failure Modes Observed

| Failure Mode | Evidence | Assessment |
| --- | --- | --- |
| Exposure reduction mistaken for alpha | Constant equal exposure explains most defensive improvement. | Present. |
| Generic de-risking effect | LOW_BREADTH does not beat constant exposure on Sharpe or mean spread. | Present. |
| Poor timing but lower volatility | LOW_BREADTH lowers volatility but lowers Sharpe. | Present. |
| Delayed defensive activation | Prior diagnostics showed strongest isolated signal late in active episodes. | Still a concern. |
| Over-defensive behavior during recovery | LOW_BREADTH remains defensive post-stress on average. | Present risk. |
| Upside destruction | Up capture declines similarly to constant/random exposure cuts. | Present. |
| Transition whipsaw | Transition proxy is nonzero, though far below random timing. | Moderate. |
| Turnover explosion | Not observed in this scale proxy, but portfolio-level cost remains untested. | Watch item. |
| h20/h10 instability | h20 remains stronger; h10 is weaker but not contradictory. | Manageable. |
| Volatility proxy duplication | LOW_BREADTH outperforms volatility-only on Sharpe/drawdown, so not fully duplicated. | Limited. |
| Drawdown proxy duplication | LOW_BREADTH modestly outperforms drawdown-only on Sharpe/drawdown. | Limited. |
| No improvement versus randomized timing | LOW_BREADTH loses to random timing on Sharpe/mean, ties max drawdown, wins left-tail and transitions. | Mixed but unfavorable. |

## 18. Final Interpretation

LOW_BREADTH has some context-aware timing behavior:

- It reduces exposure more during stress than constant scaling.
- It begins reducing exposure before stress on average.
- It has lower transition instability than randomized schedules.
- It is not fully redundant with volatility-only or drawdown-only filters.

However, the strongest equal-exposure tests are not favorable:

- It does not outperform constant equal exposure on Sharpe.
- It does not outperform constant equal exposure on mean spread.
- It does not outperform randomized equal-frequency timing on Sharpe or mean spread.
- Its drawdown improvement is mostly explained by lower exposure.
- Its left-tail improvement is useful but not uniquely better than simple alternatives.

Therefore, the exposure-modifier path is not currently strong enough to justify implementation or architecture expansion.

## 19. Recommended Next Step

Recommended action:

`pause exposure-modifier implementation research`

Keep LOW_BREADTH classified as:

`context filter only`

Recommended future use:

- Retain LOW_BREADTH in research notes and diagnostics as a context/state descriptor.
- Do not implement an exposure-modifier layer yet.
- Do not promote LOW_BREADTH into construction, portfolio, survivor, or validation logic.
- Use the findings to design stricter exposure-modifier diagnostics before testing other context filters.

If this path is revisited, the next diagnostic should require:

- beta-adjusted spread-return analysis,
- transaction-cost-aware transition testing,
- equal-exposure matched comparisons as a default,
- stress-window timing decomposition,
- recovery-period upside preservation checks,
- and WFV-window-level exposure-timing attribution.

## Final Conclusion

LOW_BREADTH's exposure-modifier behavior is useful but mostly generic de-risking. It is not random, and it is not simply a volatility or drawdown proxy, but it does not add enough value beyond matched exposure reduction to justify an exposure-modifier implementation path.

The correct research interpretation is conservative: LOW_BREADTH remains a context filter, not an exposure modifier ready for construction. The platform should continue preserving strict separation between contextual diagnostics and production alpha behavior.
