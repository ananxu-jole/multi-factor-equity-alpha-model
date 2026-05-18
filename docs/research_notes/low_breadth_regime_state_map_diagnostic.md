# LOW_BREADTH Regime / State Map Diagnostic

## 1. Executive Takeaway

This note documents the first research-only regime/state diagnostic for:

- `smooth_trend_persistence_60_low_breadth`

Final classification:

`context filter`

Secondary interpretation:

`stabilizer with conditional alpha evidence`

LOW_BREADTH contains useful conditional information, but the evidence does not support treating it as a standalone persistent alpha. It is most informative when used as a state descriptor around collapsed breadth, persistent downtrends, volatility spikes, and panic/liquidity stress. It also helps identify periods where several constructed alphas behave materially better.

The evidence is weaker for standalone deployment. Pure LOW_BREADTH sleeves remain sparse and high-turnover, while smoothed constructed alphas dilute the component's marginal contribution. LOW_BREADTH should remain a watchlist conditional layer and should be studied inside a separate Conditional-Alpha Framework rather than forced through the universal-alpha path.

This diagnostic did not change production pipelines, gates, schemas, thresholds, survivor lists, portfolio logic, or existing validation logic.

## 2. Data / Inputs Used

Inputs reviewed:

- `docs/research_notes/low_breadth_regime_state_map_design.md`
- `docs/research_notes/batch4_low_breadth_constructed_alpha_attribution.md`
- `artifacts/panels/signals/smooth_trend_persistence_60_low_breadth.parquet`
- `sql/project_underdog.db`
- `clean_close_prices_current`
- `benchmark_prices_current`
- `alpha_construction_metadata_current`
- `alpha_construction_quality_current`
- `alpha_construction_diagnostics_current`
- `alpha_constructed_candidates_current`
- `alpha_signal_pool_current`
- `wfv_gate_current`
- `constructed_alpha_wfv_gate_current`
- `constructed_alpha_wfv_windows_current`
- `alpha_stress_gate_current`
- `survivor_alpha_registry_current`

The isolated LOW_BREADTH signal is a `NEGATIVE_EDGE_REVERSE_SIGNAL` at h10 and h20. Isolated signal IC is therefore reported below as direction-adjusted effective IC, where more positive is better.

Constructed-alpha IC is reported directly from the constructed alpha panels.

## 3. LOW_BREADTH Isolated h20 / h10 Findings

Persisted scoring shows:

| Horizon | Raw Mean IC | Effective Mean IC | Effective IC IR | Direction | Status |
| --- | ---: | ---: | ---: | --- | --- |
| h10 | -0.031474 | 0.031474 | 0.155966 | `NEGATIVE_EDGE_REVERSE_SIGNAL` | `APPROVED_FOR_WFV` |
| h20 | -0.050074 | 0.050074 | 0.241726 | `NEGATIVE_EDGE_REVERSE_SIGNAL` | `APPROVED_FOR_WFV` |

The h20 bridge result was:

| Horizon | WFV Status | Effective Mean Test IC | Effective Test IC IR | Persistence | Sign Consistency |
| --- | --- | ---: | ---: | ---: | ---: |
| h20 | `APPROVED_WFV` | 0.051455 | 0.225597 | 0.75 | 0.75 |

Interpretation:

- LOW_BREADTH is strongest as a direction-adjusted h20 conditional signal.
- h10 is useful but less robust than h20.
- The signal is not always-on. It is an active-state component with meaningful inactive periods.

## 4. Constructed-Alpha Blend Findings

Four v4 smoothed constructed alphas contained LOW_BREADTH:

| Alpha | Construction Status | Turnover Risk | Main WFV Result | Stress / Survivor Result |
| --- | --- | --- | --- | --- |
| `alpha_decay_aware_dynamic_v4_smooth` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | h5 `APPROVED_CONSTRUCTED_ALPHA_WFV` | `WATCHLIST_STRESS`, `REVIEW_SATELLITE` |
| `alpha_regime_blend_dynamic_v4_smooth` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | h5 `APPROVED_CONSTRUCTED_ALPHA_WFV` | `REJECTED_STRESS` |
| `alpha_rolling_ic_dynamic_v4_smooth` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | rejected across h1/h5/h10/h20 | not stress tested |
| `alpha_hybrid_adaptive_v4_smooth` | `APPROVED_FOR_ALPHA_VALIDATION` | `LOW_TURNOVER_RISK` | h5 `WATCHLIST_CONSTRUCTED_ALPHA_WFV` | `WATCHLIST_STRESS`, `REVIEW_SATELLITE` |

The v4 smooth alphas show stronger IC during LOW_BREADTH-active periods than inactive periods:

| Alpha | h20 Mean IC | h20 Active Mean IC | h20 Inactive Mean IC | Active - Inactive |
| --- | ---: | ---: | ---: | ---: |
| `alpha_decay_aware_dynamic_v4_smooth` | 0.018244 | 0.046317 | 0.005599 | +0.040718 |
| `alpha_regime_blend_dynamic_v4_smooth` | 0.019317 | 0.046754 | 0.006959 | +0.039795 |
| `alpha_rolling_ic_dynamic_v4_smooth` | 0.009426 | 0.021850 | 0.003830 | +0.018020 |
| `alpha_hybrid_adaptive_v4_smooth` | 0.016137 | 0.040004 | 0.005386 | +0.034618 |

At h5, the same active/inactive pattern remains but is smaller:

| Alpha | h5 Mean IC | h5 Active Mean IC | h5 Inactive Mean IC | Active - Inactive |
| --- | ---: | ---: | ---: | ---: |
| `alpha_decay_aware_dynamic_v4_smooth` | 0.009380 | 0.023100 | 0.003265 | +0.019835 |
| `alpha_regime_blend_dynamic_v4_smooth` | 0.010137 | 0.023843 | 0.004028 | +0.019815 |
| `alpha_rolling_ic_dynamic_v4_smooth` | 0.006598 | 0.019340 | 0.000919 | +0.018421 |
| `alpha_hybrid_adaptive_v4_smooth` | 0.008892 | 0.022397 | 0.002873 | +0.019524 |

Interpretation:

- LOW_BREADTH-active dates are consistently higher-quality dates for the v4 blends.
- The effect is more compelling at h20 than h5.
- LOW_BREADTH behaves more like a state/context descriptor than a direct h5 return engine inside smoothed constructed alphas.

## 5. No-LOW_BREADTH Counterfactual Findings

The prior constructed-alpha attribution diagnostic built research-only counterfactuals with LOW_BREADTH removed and remaining components renormalized where possible. These were diagnostic approximations, not official reconstructed alphas.

Key findings from that attribution work:

| Blend Group | Mean IC Effect From LOW_BREADTH | Persistence Effect | Sharpe Effect | Turnover Effect |
| --- | ---: | ---: | ---: | ---: |
| `alpha_diversified_research_v2` | +0.0040 | +0.50 | -0.1707 | +2.30 |
| `alpha_persistence_blend_v2` | +0.0032 | +0.50 | -0.1581 | -1.30 |
| raw v3 dynamic alphas | mostly small positive | mixed | mostly negative | mostly higher |
| v4 smooth alphas | small and mixed | mixed | small/mixed | near neutral |

Interpretation:

- LOW_BREADTH is not an accidental passenger; it improved active-period IC and contributed positive marginal IC in several blends.
- It is also not the dominant driver of v4 smoothed alpha performance.
- Smoothing and non-LOW_BREADTH components carry much of the constructed-alpha viability.

## 6. State-by-State Attribution Table

This table summarizes the most relevant state slices. Isolated LOW_BREADTH values are h20 effective IC. V4 blend values are average h20 constructed-alpha IC across the four v4 smoothed LOW_BREADTH-containing alphas.

| State Axis | State | LOW_BREADTH h20 Effective IC | V4 Blend Avg h20 IC | Interpretation |
| --- | --- | ---: | ---: | --- |
| Stress | `PANIC_LIQUIDITY_STRESS` | 0.123087 | 0.096089 | Strongest evidence; LOW_BREADTH aligns with stress behavior. |
| Trend | `PERSISTENT_DOWNTREND` | 0.109939 | 0.083607 | Strong conditional context; consistent with h20 best-regime metadata. |
| Volatility | `VOLATILITY_SPIKE` | 0.095885 | 0.060559 | Useful in stress volatility, but must be stress-tested carefully. |
| Trend | `SIDEWAYS_CHOPPY` | 0.080453 | 0.016313 | Isolated signal helps more than blends. |
| Dispersion | `LOW_DISPERSION` | 0.061583 | 0.006497 | Isolated effect exists; blend effect weak. |
| Dispersion | `ROTATIONAL_MARKET` | 0.060321 | 0.016844 | Moderate evidence; likely context-sensitive. |
| Volatility | `VOLATILITY_NORMALIZATION` | 0.055757 | 0.021075 | Signal may persist after stress begins to normalize. |
| Breadth | `COLLAPSED_BREADTH` | 0.050100 | 0.041188 | Intended condition works, but not uniquely enough by itself. |
| Trend | `PERSISTENT_UPTREND` | 0.049795 | -0.000334 | Isolated signal not harmful, but blends do not benefit in broad uptrends. |
| Breadth | `BREADTH_RECOVERY` | 0.049430 | 0.007278 | LOW_BREADTH may remain useful, but blend contribution weakens. |
| Stress | `POST_STRESS_STABILIZATION` | 0.012904 | 0.005480 | Weak positive; not a strong post-stress return engine. |
| Stress | `DRAWDOWN_ACCELERATION` | 0.014000 | 0.011096 | Less convincing than panic/deep stress. |
| Volatility | `RISING_VOLATILITY` | -0.002035 | 0.007583 | Isolated signal weak; blends carry behavior. |

For the v4 smoothed constructed alphas, h20 state behavior was strongest in:

- `PANIC_LIQUIDITY_STRESS`: average h20 IC 0.096089
- `PERSISTENT_DOWNTREND`: average h20 IC 0.083607
- `VOLATILITY_SPIKE`: average h20 IC 0.060559
- `COLLAPSED_BREADTH`: average h20 IC 0.041188
- `WEAKENING_BREADTH`: average h20 IC 0.038663

The weakest h20 blend states were:

- `STRONG_BREADTH`: average h20 IC -0.007994
- `RECOVERY_PHASE`: average h20 IC -0.007412
- `LOW_VOLATILITY`: average h20 IC -0.004203
- `PERSISTENT_UPTREND`: average h20 IC -0.000334

## 7. Active / Inactive Diagnostics

Activation profile:

| Metric | Value |
| --- | ---: |
| Active dates | 636 |
| Inactive dates | 1,462 |
| Active date ratio | 30.31% |
| Activation episodes | 76 |
| Transition count | 152 |
| Average episode length | 8.37 trading days |
| Median episode length | 3 trading days |
| Maximum episode length | 49 trading days |

Active WFV-window coverage:

| Window | Test Start | Test End | Active Dates | Test Dates | Active Ratio |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | 2019-08-02 | 2019-10-30 | 33 | 63 | 52.38% |
| 2 | 2021-06-09 | 2021-09-07 | 9 | 63 | 14.29% |
| 3 | 2023-04-17 | 2023-07-17 | 22 | 63 | 34.92% |
| 4 | 2025-02-25 | 2025-05-23 | 47 | 63 | 74.60% |

Activation alignment:

| State Axis | Main Active Overlap | Active Share of State |
| --- | --- | ---: |
| Breadth | `COLLAPSED_BREADTH` | 92.0% |
| Trend | `PERSISTENT_DOWNTREND` | 83.6% |
| Stress | `PANIC_LIQUIDITY_STRESS` | 77.9% |
| Stress | `DRAWDOWN_ACCELERATION` | 70.0% |
| Volatility | `VOLATILITY_SPIKE` | 61.0% |
| Volatility | `RISING_VOLATILITY` | 55.4% |

Interpretation:

- Activation aligns well with collapsed breadth and stress states.
- It is not extremely sparse by date count, but episodes are short and transition-heavy.
- Median activation episode length of three trading days creates transition instability risk.
- LOW_BREADTH has a strong state-labeling function, but not necessarily a clean exposure-management function.

## 8. Transition Behavior

Isolated LOW_BREADTH h20 effective IC around activation episodes:

| Transition Segment | Observations | Effective IC | IC IR | Positive Effective IC Rate |
| --- | ---: | ---: | ---: | ---: |
| 20 to 11 days before activation | 111 | -0.016269 | -0.091189 | 43.24% |
| 10 to 1 days before activation | 79 | 0.027704 | 0.146806 | 58.23% |
| first 10 active days | 157 | 0.015083 | 0.076642 | 55.41% |
| last 10 active days | 211 | 0.111061 | 0.526103 | 67.77% |
| 11 to 20 days after deactivation | 6 | 0.114769 | 0.727423 | 83.33% |

Average v4 smoothed constructed-alpha h20 IC around activation episodes:

| Transition Segment | Avg Observations | Avg IC | Avg IC IR | Avg Positive IC Rate |
| --- | ---: | ---: | ---: | ---: |
| 20 to 11 days before activation | 593 | -0.015140 | -0.118596 | 46.88% |
| 10 to 1 days before activation | 417 | 0.014402 | 0.090419 | 56.83% |
| first 10 active days | 157 | 0.073377 | 0.539400 | 72.13% |
| last 10 active days | 211 | 0.040012 | 0.210344 | 61.97% |
| 1 to 10 days after deactivation | 248 | 0.038935 | 0.252045 | 60.18% |
| 11 to 20 days after deactivation | 133 | 0.050260 | 0.485125 | 67.11% |

Interpretation:

- There is some evidence of pre-activation improvement in the 10 days immediately before activation.
- The signal does not appear to anticipate deterioration 20 days early.
- The first 10 active days are strong for constructed alphas, suggesting activation is directionally useful after construction.
- Isolated LOW_BREADTH h20 is strongest late in active episodes, which raises delayed-timing risk.
- Post-deactivation constructed-alpha behavior remains positive, suggesting deactivation may sometimes happen before the broader opportunity has fully decayed.

## 9. Stress Behavior

Stress outcomes for LOW_BREADTH-containing v4 smoothed constructed alphas:

| Alpha | Horizon | Stress Status | Pass Rate | Worst Degradation | Turnover Risk |
| --- | ---: | --- | ---: | ---: | --- |
| `alpha_regime_blend_dynamic_v4_smooth` | 5 | `REJECTED_STRESS` | 0.722222 | 0.803514 | `LOW_TURNOVER_RISK` |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `WATCHLIST_STRESS` | 0.555556 | 0.601208 | `LOW_TURNOVER_RISK` |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `WATCHLIST_STRESS` | 0.555556 | 0.641822 | `LOW_TURNOVER_RISK` |

The sole 07 `APPROVED_STRESS` survivor was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`

That survivor did not include `smooth_trend_persistence_60_low_breadth`.

Interpretation:

- LOW_BREADTH aligns with stress states, but did not produce a stress-approved survivor after construction.
- It did not reliably reduce drawdowns enough to clear current stress/survivor standards.
- The state map supports LOW_BREADTH as a stress context indicator, not yet as a stress-robust alpha sleeve.

## 10. Failure Modes Observed

| Failure Mode | Evidence | Assessment |
| --- | --- | --- |
| Correct regime idea, delayed timing | h20 isolated IC strongest in late active episodes, not early episodes. | Present. |
| Activation instability | 76 episodes, 152 transitions, median episode length 3 days. | Present. |
| Sparse but excessively costly | Pure LOW_BREADTH sleeves had high turnover and sparse/no-dispersion inactive rows. | Present for standalone use. |
| Stress collapse | LOW_BREADTH-containing alphas did not become the 07 stress-approved survivor. | Partially present. |
| Works only blended | Active-state IC improves in blends; pure sleeves are not construction-viable. | Present. |
| Inactive-state leakage | Inactive neutral rows behave differently in pure sleeves versus blended alphas. | Present as construction artifact risk. |
| Hidden beta exposure | Strongest states are downtrend/panic/vol spike; beta/stress context likely contributes. | Needs further decomposition. |
| Regime overfitting | WFV active coverage ranges from 14% to 75% across windows. | Watch item. |
| Transition whipsaw | Short episodes and high transition count create turnover risk. | Present. |
| False defensive signaling | Active overlap with persistent uptrend is low at 7.5% of uptrend dates; strong breadth behavior is weak for blends. | Limited but should be monitored. |
| Blended passenger behavior | v4 smoothing reduces LOW_BREADTH marginal effect; rolling-IC blend gives LOW_BREADTH small weight. | Present in some blends. |

## 11. Classification Of LOW_BREADTH's Role

Chosen classification:

`context filter`

Rationale:

- LOW_BREADTH clearly identifies market states where constructed alphas behave better.
- Activation is strongly aligned with collapsed breadth, downtrend, volatility spike, and panic/liquidity stress states.
- Active-period IC is consistently better than inactive-period IC in the v4 smoothed blends.
- The component does not yet stand alone as a robust constructed alpha.
- The downstream survivor evidence does not support classifying it as a core alpha or true standalone conditional alpha.

Why not `true conditional alpha`:

- Pure LOW_BREADTH sleeves were too sparse/high-turnover under current construction standards.
- Stress validation did not produce a LOW_BREADTH-containing approved survivor.
- Transition timing is imperfect, with strongest isolated h20 behavior late in active episodes.

Why not `blended passenger`:

- Active-period IC improvement is too consistent to dismiss.
- LOW_BREADTH improved mean IC and WFV-like persistence in several prior counterfactual comparisons.
- Activation aligns with economically plausible fragile-market states.

Why not `unstable defensive signal`:

- WFV h20 passed for the isolated signal.
- Sign consistency and persistence were acceptable at the controlled bridge stage.
- The weakness is mostly construction/stress translation, not a complete absence of signal information.

## 12. Recommendation For Next Step

Recommended action:

`keep as watchlist conditional layer and isolate into the Conditional-Alpha Framework prototype`

Next diagnostic:

- Build a research-only LOW_BREADTH conditional-alpha prototype comparing:
  - neutral inactive sleeve,
  - masked active-only sleeve,
  - state-gated sleeve,
  - v4 smoothed blend,
  - and no-LOW_BREADTH counterfactual.

Specific questions for that prototype:

- Can LOW_BREADTH preserve h20 active-state benefit while reducing transition turnover?
- Does active-only evaluation remain stable across WFV windows after excluding inactive/no-dispersion dates?
- Can deactivation be studied without creating new promotion rules?
- Does LOW_BREADTH reduce stress drawdown in a dedicated conditional sleeve, or only label stress states after the fact?
- Is the component useful as a satellite/context overlay even if it never qualifies as a core survivor?

Do not do yet:

- Do not promote LOW_BREADTH as a standalone alpha.
- Do not relax WFV or stress gates.
- Do not alter survivor-freeze logic.
- Do not expand to additional conditional components until this prototype produces a repeatable output format.
- Do not treat constructed-alpha blend performance as proof of component quality.

## Final Conclusion

LOW_BREADTH is best understood as a context filter with stabilizer-like behavior. It identifies fragile market states where h20 trend-quality behavior is materially better, especially under collapsed breadth, persistent downtrends, volatility spikes, and panic/liquidity stress.

The component is not a core survivor and not yet a standalone conditional alpha. Its activation is useful but transition-heavy, its pure sleeves are difficult to construct cleanly, and its blended versions can dilute or hide the original conditional edge.

The platform is behaving correctly by not promoting this evidence directly into survivor status. The right next step is a research-only Conditional-Alpha prototype that studies active-state construction and stress attribution without changing gates, schemas, promotion logic, or portfolio construction.
