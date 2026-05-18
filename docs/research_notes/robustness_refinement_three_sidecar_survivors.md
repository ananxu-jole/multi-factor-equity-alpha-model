# Robustness Refinement: Three Sidecar Survivor Candidates

## 1. Executive Takeaway

This note documents a research-only robustness refinement diagnostic for the three sidecar survivor candidates from the robustness-first orthogonal discovery batch:

- `volume_shock_reversal_stable_20`
- `residual_momentum_stability_60`
- `volatility_surprise_reversal_20_60_smooth`

Final classifications:

| Candidate | Final Research Classification | Reason |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | `refined survivor candidate` | Robust across nearby volume-shock/smoothing settings, highly orthogonal, but needs turnover-aware implementation. |
| `residual_momentum_stability_60` | `needs redesign` | Strong WFV-style behavior, but too highly correlated with plain momentum and LOW_BREADTH/trend-quality exposure. |
| `volatility_surprise_reversal_20_60_smooth` | `refined survivor candidate` | All nearby variants passed sidecar WFV-style checks, baselines failed, correlations remained low. |

Final recommendation:

`Prepare a narrow controlled production-registration design for two candidates only: volume_shock_reversal_stable_20 and volatility_surprise_reversal_20_60_smooth.`

Do not register yet from this note. The next step should define exact formulas, metadata, expected failure modes, and official pipeline plan. `residual_momentum_stability_60` should be redesigned before any production implementation.

No production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha implementation paths were changed.

## 2. Candidate Summary Table

| Candidate | Family | Economic Intuition | Expected Horizon | Prior Sidecar Survival Reason | Expected Failure Mode |
| --- | --- | --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | Return moves amplified by volume shocks may mean-revert when smoothed enough to avoid one-day noise. | h10-h20 | Low correlation to pool and strong sidecar WFV window behavior. | Turnover and transaction-cost sensitivity. |
| `residual_momentum_stability_60` | `residual_relative_value` | Stable residual momentum may identify persistent idiosyncratic return structure after benchmark adjustment. | h20 | Strong stress/downtrend sidecar WFV behavior. | Hidden trend/beta exposure and plain momentum duplication. |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | Returns under elevated short-vs-long realized volatility may reverse in a more robust, volatility-aware way. | h10-h20 | Strong sidecar WFV behavior with very low pool correlation. | Generic risk-off or plain reversal duplication. |

## 3. Parameter Sensitivity Findings

### `volume_shock_reversal_stable_20`

Nearby variants tested:

- volume shock lookbacks: 10, 20, 40
- smoothing windows: 3, 5, 10
- simple volume-spike reversal baseline
- plain reversal baseline

Summary:

| Metric | Result |
| --- | ---: |
| Variants tested | 9 |
| Variants passing sidecar robustness checks | 7 |
| Median effective test IC | 0.024214 |
| Median sidecar WFV IR | 0.893190 |
| Median turnover proxy | 0.200658 |

Best variants:

| Variant | Best Horizon | Abs Mean IC | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `volume_shock_reversal_stable_s40_sm10` | h20 | 0.009791 | 0.037534 | 0.765515 | 0.75 | 0.128510 |
| `volume_shock_reversal_stable_s40_sm5` | h20 | 0.008180 | 0.026826 | 0.904152 | 0.75 | 0.198883 |
| `volume_shock_reversal_stable_s20_sm5` | h20 | 0.008604 | 0.025990 | 0.893190 | 0.75 | 0.200658 |

Counterfactual baselines:

| Baseline | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: |
| `simple_volume_spike_reversal_20` | 0.018613 | 1.111392 | 0.75 | 0.491144 |
| `plain_reversal_5_smooth5` | -0.007014 | -0.239468 | 0.25 | 0.152910 |

Interpretation:

- The family is not a one-parameter artifact.
- Longer volume-shock lookbacks and stronger smoothing materially reduce turnover.
- Simple volume-spike reversal also has some window evidence, but turnover is extreme.
- The refined formula adds value mainly by stabilizing a noisy volume-shock reversal idea.

Classification implication:

`refined survivor candidate`, preferably using a longer shock lookback and smoothing variant.

### `residual_momentum_stability_60`

Nearby variants tested:

- residual momentum windows: 40, 60, 80
- stability windows: 40, 60, 90
- plain momentum stability baseline
- raw residual momentum baseline

Summary:

| Metric | Result |
| --- | ---: |
| Variants tested | 9 |
| Variants passing sidecar robustness checks | 7 |
| Median effective test IC | 0.048915 |
| Median sidecar WFV IR | 0.567508 |
| Median turnover proxy | 0.084624 |

Best variants:

| Variant | Best Horizon | Abs Mean IC | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `residual_momentum_stability_m60_s40` | h20 | 0.012066 | 0.054965 | 0.575356 | 0.75 | 0.082555 |
| `residual_momentum_stability_m60_s90` | h20 | 0.009928 | 0.052120 | 0.568243 | 0.75 | 0.084624 |
| `residual_momentum_stability_m80_s40` | h20 | 0.007881 | 0.051506 | 0.567508 | 0.75 | 0.073279 |

Counterfactual baselines:

| Baseline | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: |
| `plain_momentum_stability_60` | 0.040187 | 0.395188 | 0.75 | 0.090024 |
| `residual_raw_momentum_60` | 0.012399 | 0.191123 | 0.75 | 0.078710 |

Interpretation:

- The family is robust numerically across nearby settings.
- But the strongest variants are highly correlated with plain momentum.
- The residual/stability layer improves over raw residual momentum, but may not add enough unique information versus a simpler momentum baseline.

Classification implication:

`needs redesign`, not production registration yet.

### `volatility_surprise_reversal_20_60_smooth`

Nearby variants tested:

- volatility surprise windows: 10/40, 20/60, 20/80, 30/90
- smoothing windows: 5 and 10
- simple volatility reversal baseline
- plain 20d reversal baseline

Summary:

| Metric | Result |
| --- | ---: |
| Variants tested | 5 |
| Variants passing sidecar robustness checks | 5 |
| Median effective test IC | 0.044312 |
| Median sidecar WFV IR | 0.704639 |
| Median turnover proxy | 0.083101 |

Best variants:

| Variant | Best Horizon | Abs Mean IC | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `volatility_surprise_reversal_s30_l90_sm5` | h10 | 0.004411 | 0.063969 | 1.220540 | 0.75 | 0.082010 |
| `volatility_surprise_reversal_s10_l40_sm5` | h20 | 0.001427 | 0.058626 | 0.911822 | 0.75 | 0.110172 |
| `volatility_surprise_reversal_s20_l60_sm5` | h20 | 0.002123 | 0.044312 | 0.625678 | 0.75 | 0.085561 |
| `volatility_surprise_reversal_s20_l60_sm10` | h20 | 0.003364 | 0.043565 | 0.599928 | 0.75 | 0.062907 |
| `volatility_surprise_reversal_s20_l80_sm5` | h10 | 0.003577 | 0.037334 | 0.704639 | 0.75 | 0.083101 |

Counterfactual baselines:

| Baseline | Effective Test IC | Effective Test IC IR | Positive Window Rate | Turnover |
| --- | ---: | ---: | ---: | ---: |
| `simple_volatility_reversal_20` | -0.004649 | -0.065606 | 0.25 | 0.067885 |
| `plain_reversal_20_smooth5` | -0.010603 | -0.137413 | 0.50 | 0.067080 |

Interpretation:

- This is the cleanest family-level result.
- Every nearby variant passed sidecar robustness checks.
- Simple volatility reversal and plain reversal failed, which supports uniqueness.
- Full-sample IC remains weak, so official scoring may be challenging, but WFV-style behavior is consistent.

Classification implication:

`refined survivor candidate`.

## 4. Horizon Stability Findings

The refinement confirmed h20 as the dominant robust horizon for the batch, with one nuance: the volatility surprise family also produced credible h10 variants.

Key findings:

- `volume_shock_reversal_stable_20`: h20 remained the preferred horizon for longer, smoother variants. Shorter variants sometimes shifted to h10 but with weaker window persistence.
- `residual_momentum_stability_60`: h20 dominated all strong variants.
- `volatility_surprise_reversal_20_60_smooth`: h20 remained credible, but 30/90 and 20/80 style variants showed h10 strength.

Horizon risk:

- Volume shock reversal is sensitive to smoothing and can become noisy at shorter horizons.
- Residual momentum is structurally h20 and should not be treated as a short-horizon signal.
- Volatility surprise is not pure h20; official implementation should either choose one clear h20 formula or explicitly justify h10/h20 testing.

## 5. Turnover / Tradability Findings

Turnover proxy by family:

| Family | Median Turnover Proxy | Turnover Interpretation |
| --- | ---: | --- |
| `volume_shock_reversal_stable_20` variants | 0.200658 | highest turnover; must be refined before official use |
| `residual_momentum_stability_60` variants | 0.084624 | low and stable |
| `volatility_surprise_reversal_20_60_smooth` variants | 0.083101 | low and stable |

Turnover conclusions:

- Volume shock reversal is the only candidate with material tradability concern.
- The best volume variant by balance is `volume_shock_reversal_stable_s40_sm10`, because it had the highest effective test IC and lower turnover than the original s20/sm5 shape.
- Residual momentum and volatility surprise have acceptable turnover profiles in sidecar diagnostics.

Tradability risk:

Volume shock reversal could fail official stress if transaction-cost sensitivity is harsh. Any production registration design should use the smoother lower-turnover variant, not the highest-churn version.

## 6. Stress / Regime Attribution Findings

Top stress/regime findings:

| Candidate Family | Key Stress / Regime Result | Interpretation |
| --- | --- | --- |
| `volume_shock_reversal_stable_20` | meaningful WFV persistence, but less dominant in top regime slices | broad window behavior is more important than one stress state |
| `residual_momentum_stability_60` | panic/liquidity stress effective IC around 0.10 across many variants | stress behavior is strong but may reflect plain momentum/trend exposure |
| `volatility_surprise_reversal_20_60_smooth` | downtrend and panic/liquidity stress slices are strong; simple baselines also have strong slices but fail WFV | volatility-surprise interaction is needed for window robustness |

Important observation:

Some simple baselines showed excellent stress slices, especially plain momentum and plain volatility reversal. They did not consistently pass WFV-style checks. This reinforces that regime slices alone are not enough.

Stress coherence:

- Volume shock reversal: moderate but broad.
- Residual momentum: strongest but most suspicious due redundancy.
- Volatility surprise: coherent and less redundant.

## 7. Orthogonality Findings

### Volume Shock Reversal

Largest correlations were with broad reversal proxies:

- max observed correlation to plain reversal proxy: about 0.325
- correlations to current alpha-pool signals remained low

Interpretation:

The signal is related to reversal, but not dominated by the existing alpha pool. Orthogonality remains strong.

### Residual Momentum Stability

This family showed major redundancy:

- correlation with `proxy_plain_momentum_60` ranged roughly 0.72 to 0.90
- correlation with `smooth_trend_persistence_60_low_breadth` was around 0.43 to 0.53 for many variants
- correlation with `smooth_trend_persistence_60_downtrend` was around 0.35 for the 60-day variants

Interpretation:

The candidate is not cleanly orthogonal. It is likely a momentum/trend-quality adjacent structure, despite residual framing.

### Volatility Surprise Reversal

This family remained highly orthogonal:

- max observed correlation to plain reversal proxy about 0.114
- correlation to trend-consistency about 0.100 for the strongest 30/90 variant
- correlation to LOW_BREADTH components stayed below 0.09 for the standard 20/60 variants

Interpretation:

This is the cleanest orthogonal survivor candidate in the refinement.

## 8. Counterfactual Attribution Findings

### Volume Shock Reversal

Counterfactual:

- simple volume-spike reversal had some WFV evidence but very high turnover
- plain reversal failed

Conclusion:

The refined signal adds value by stabilizing volume-shock reversal and reducing churn relative to the naive volume-spike formulation.

### Residual Momentum Stability

Counterfactual:

- plain momentum stability performed strongly
- raw residual momentum was weaker
- residual stability variants were highly correlated with plain momentum

Conclusion:

The apparent edge may mostly be momentum stability, not residual-relative-value uniqueness. This needs redesign before production registration.

### Volatility Surprise Reversal

Counterfactual:

- simple volatility reversal failed sidecar WFV
- plain 20d reversal failed sidecar WFV
- all volatility-surprise variants passed

Conclusion:

The volatility-surprise interaction appears to add unique value beyond simple volatility or reversal proxies.

## 9. Failure Modes Observed

| Failure Mode | Volume Shock | Residual Momentum | Volatility Surprise |
| --- | --- | --- | --- |
| Parameter fragility | Low to moderate | Low | Low |
| Horizon luck | Moderate | Low | Low to moderate |
| Hidden beta exposure | Low to moderate | High | Moderate |
| Family redundancy | Moderate with reversal | High with momentum | Low |
| Turnover fragility | High | Low | Low |
| Stress collapse | Not observed in sidecar | Not observed, but stress exposure may explain strength | Not observed in sidecar |
| Recovery underperformance | Not fully tested | Not fully tested | Not fully tested |
| Sign instability | Low for main variants | Short-vs-long horizon issue | Some short-horizon instability |
| Sparse signal illusion | Low | Low | Low |
| Blend/correlation camouflage | Low | High | Low |
| Weak standalone economics | Moderate | Moderate | Moderate due low full-sample IC |

## 10. Candidate-by-Candidate Classification

### `volume_shock_reversal_stable_20`

Classification:

`refined survivor candidate`

Recommended refined form:

- longer volume shock lookback
- stronger smoothing
- h20 primary
- turnover-aware metadata and stress-cost warning

Best sidecar refinement:

- `volume_shock_reversal_stable_s40_sm10`

Why:

- effective test IC 0.037534
- effective test IC IR 0.765515
- positive window rate 0.75
- turnover proxy 0.128510, lower than the original-style s20/sm5 variant

Production-readiness interpretation:

Durable enough to deserve a controlled production-registration design, but not yet direct registration from this note.

### `residual_momentum_stability_60`

Classification:

`needs redesign`

Why:

- strong numerical robustness across variants
- low turnover
- strong stress-state behavior
- but high correlation with plain 60d momentum
- meaningful overlap with LOW_BREADTH/trend-quality components

Production-readiness interpretation:

Not clean enough for production registration research in current form. It needs a redesign that reduces plain momentum duplication and demonstrates unique residual/relative-value contribution.

Potential redesign direction:

- stronger beta-neutralization
- residualization versus universe common return, not only benchmark beta
- explicit comparison against plain momentum as a mandatory control
- possibly residual reversal rather than residual momentum

### `volatility_surprise_reversal_20_60_smooth`

Classification:

`refined survivor candidate`

Recommended refined form:

- keep volatility-surprise interaction
- retain smoothing
- evaluate h20 primary with h10 secondary
- avoid collapsing to simple volatility reversal

Best sidecar variants:

- `volatility_surprise_reversal_s30_l90_sm5`
- `volatility_surprise_reversal_s20_l60_sm10`
- `volatility_surprise_reversal_s20_l60_sm5`

Why:

- all nearby variants passed sidecar robustness checks
- baselines failed
- low turnover
- low correlation to alpha-pool signals and broad proxies

Production-readiness interpretation:

Durable enough to deserve a controlled production-registration design.

## 11. Recommended Next Step

Recommended next move:

`Design a controlled production-registration plan for two refined survivor candidates.`

Candidates:

1. `volume_shock_reversal_stable_20`, using a lower-turnover long-lookback/smoothed version.
2. `volatility_surprise_reversal_20_60_smooth`, using the volatility-surprise interaction with smoothing.

Do not include:

- `residual_momentum_stability_60` in its current form.

The next plan should specify:

- exact formula definitions
- metadata
- expected horizon
- expected failure modes
- structural expectations
- official 03/03C/03D run plan
- controlled WFV criteria if candidates earn it
- no 04A+ unless standard eligibility is reached

## Final Conclusion

Two of the three sidecar survivors appear durable enough to justify later production-registration research:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

The third candidate, `residual_momentum_stability_60`, is numerically strong but insufficiently distinct. It should be redesigned rather than registered.

The batch successfully did its job: it filtered sidecar promise into a narrower, cleaner set of standalone alpha candidates while preserving Project Underdog's validation discipline.
