# Volume Shock Reversal Isolated Production-Candidate Revalidation

## Executive Takeaway

The isolated production-candidate revalidation for `volume_shock_reversal_stable_20` completed under the research namespace `volume_shock_reversal_production_candidate_v1`.

The candidate reproduced prior isolated integration behavior with effectively zero metric drift, retained `h20` as the primary horizon, and preserved its liquidity-flow/reversal identity. It remains a plausible controlled production-candidate, but not a clean approval: WFV persistence and sign consistency were mixed, and overlap with unweighted reversal remains elevated.

Final research classification:

`production-candidate revalidation passed with review items`

Recommended next step:

`controlled production-registration decision memo`

This is not production registration. No production signal factory, gates, schemas, thresholds, survivor/watchlist lists, portfolio logic, validation logic, ML layer, or Conditional-Alpha path was modified.

## Isolated Namespace / Run Identifier

- Run namespace: `volume_shock_reversal_production_candidate_v1`
- Artifact directory: `artifacts/research/volume_shock_reversal_production_candidate_v1/`
- Candidate tested: `volume_shock_reversal_stable_20`
- Candidate family: `liquidity_flow`
- Primary horizon: `h20`
- Research mode: isolated production-candidate revalidation only

## Scope and Exclusions

Included:

- `volume_shock_reversal_stable_20`
- Candidate-only signal panel generation
- Metadata validation
- Multi-horizon scoring revalidation
- Isolated WFV diagnostics
- Stress/regime revalidation
- Turnover/tradability review
- Orthogonality/redundancy re-audit
- Drift monitoring versus prior isolated integration artifacts

Explicitly excluded:

- `volatility_surprise_reversal_20_60_smooth`
- `residual_momentum_stability_60`
- LOW_BREADTH Conditional-Alpha work
- Production signal-factory registration
- Official survivor/watchlist mutation
- Portfolio construction
- ML integration
- Any gate, schema, threshold, or validation-logic change

## Metadata Validation Results

Metadata validation passed. The candidate metadata package was complete for the isolated revalidation context.

Key metadata:

| Field | Value |
|---|---|
| signal_name | `volume_shock_reversal_stable_20` |
| signal_family | `liquidity_flow` |
| signal_version | `draft_v1_sidecar_refined` |
| research_status | `PRODUCTION_CANDIDATE_DRAFT_REVALIDATION` |
| proposed_registration_status | `PRODUCTION_CANDIDATE_DRAFT_NOT_REGISTERED` |
| intended_horizon | `h20` |
| expected_direction | `reversal` |

The formula description remained consistent with the draft definition: a smoothed abnormal-volume-weighted reversal using a rolling volume baseline and trailing smoothing. The metadata also carried forward the known risks around turnover, reversal overlap, missingness/universe mismatch, same-bar timing assumptions, and possible WFV instability.

## Generated Signal Panel Summary

The isolated production-candidate signal panel generated successfully.

| Metric | Value |
|---|---:|
| Rows | 2,098 |
| Columns | 478 |
| Missing pct | 0.034545 |
| Finite pct | 0.965455 |
| Date coverage | 0.977121 |
| Mean ticker coverage | 0.965455 |
| Inf count | 0 |
| Turnover proxy | 0.098531 |
| Turnover p95 | 0.153068 |
| Turnover max | 0.302848 |
| Concentration proxy | 0.004235 |

Panel quality remained consistent with prior isolated integration evidence. Missing-volume handling did not create infinities, and date/ticker coverage was stable.

## Multi-Horizon Scoring Revalidation

`h20` remained the strongest horizon by mean IC and absolute mean IC, consistent with the draft registration thesis.

| Horizon | Mean IC | Abs Mean IC | IC IR | Positive IC Rate | Valid Dates | Primary |
|---:|---:|---:|---:|---:|---:|---|
| h1 | 0.005437 | 0.005437 | 0.027643 | 0.506101 | 2,049 | No |
| h5 | 0.010449 | 0.010449 | 0.057256 | 0.518337 | 2,045 | No |
| h10 | 0.011421 | 0.011421 | 0.066956 | 0.517157 | 2,040 | No |
| h20 | 0.011798 | 0.011798 | 0.070228 | 0.513300 | 2,030 | Yes |

Interpretation:

- The scoring profile is coherent across horizons.
- IC increases from h1 to h20 rather than appearing as a single short-horizon spike.
- The effect remains modest, so the case depends on durability, orthogonality, and stress behavior rather than headline IC.

## WFV Revalidation Results

The isolated WFV revalidation was mixed.

| Metric | Value |
|---|---:|
| Horizon | h20 |
| WFV windows | 4 |
| Effective mean test IC | 0.004308 |
| Effective test IC IR | 0.346720 |
| Persistence | 0.500000 |
| Sign consistency | 0.500000 |
| Research classification | `WFV_REVALIDATION_MIXED_REVIEW` |

Interpretation:

- The WFV result is not a clean persistence result.
- Effective test IC remained positive, but only half of the windows showed favorable persistence/sign behavior.
- This does not reject the candidate outright in this isolated research stage, but it requires explicit review before any production-registration decision.

## Stress / Regime Revalidation Results

Stress and regime behavior remained generally consistent with the prior liquidity-flow thesis, with strongest behavior in panic/liquidity stress.

| State | Dates | Mean IC | IC IR | Positive IC Rate |
|---|---:|---:|---:|---:|
| drawdown_acceleration | 843 | 0.029143 | 0.157260 | 0.533808 |
| volatility_spike | 272 | 0.015921 | 0.076991 | 0.448529 |
| panic_liquidity_stress | 205 | 0.070692 | 0.389327 | 0.673171 |
| trend_transition | 1,371 | 0.016176 | 0.095652 | 0.517141 |
| recovery_phase | 416 | 0.012952 | 0.085040 | 0.538462 |
| high_dispersion_rotation | 525 | 0.007620 | 0.044404 | 0.527619 |

Interpretation:

- Panic/liquidity stress remains the most favorable diagnostic state.
- Drawdown acceleration and trend transition also remain positive.
- Volatility spike behavior is positive on mean IC but weaker on positive IC rate.
- The stress profile supports continued review, but does not remove the WFV persistence concern.

## Turnover / Tradability Review

The turnover profile remained plausible for a research candidate.

| Metric | Value |
|---|---:|
| Average turnover proxy | 0.098531 |
| p95 turnover | 0.153068 |
| Max turnover | 0.302848 |
| Concentration proxy | 0.004235 |

Interpretation:

- Turnover is not the dominant concern in this revalidation.
- The signal does show some turnover spikes, so turnover should remain a monitored item in the decision memo.
- No evidence was found that the isolated implementation created operationally implausible churn.

## Orthogonality / Redundancy Re-Audit

The candidate retained distinct behavior versus simple volume-shock reversal variants, but overlap with broader reversal proxies remains a review item.

| Comparison | Value Corr | Mean Rank Corr | Top/Bottom Overlap |
|---|---:|---:|---:|
| simple_volume_spike_reversal | 0.428076 | 0.428002 | 0.286796 |
| no_stability_volume_reversal | 0.428809 | 0.428741 | 0.292593 |
| unweighted_reversal | 0.721718 | 0.721652 | 0.471053 |
| liquidity_flow_slow_proxy | 0.690231 | 0.690218 | 0.451869 |
| plain_reversal20_smooth5 | 0.684895 | 0.684857 | 0.424063 |

Interpretation:

- The candidate is not merely the simple volume spike baseline.
- The stability and abnormal-volume weighting appear to add structure versus simple volume-shock variants.
- However, correlation with unweighted reversal is high enough that future review must verify that the candidate contributes distinct liquidity-flow information rather than a disguised reversal exposure.

## Drift Monitoring Findings

Drift versus prior isolated signal-factory integration evidence was effectively zero.

Observed drift:

- h1/h5/h10/h20 mean IC: negligible numerical drift only
- h1/h5/h10/h20 IC IR: negligible numerical drift only
- Positive IC rates: no drift
- Missingness / finite coverage: no material drift
- Turnover proxy: no material drift

Interpretation:

- The isolated production-candidate revalidation reproduced the prior isolated integration artifacts.
- No suspicious metric improvement appeared in this run.
- No material metric degradation appeared in this run.

## Alignment / Look-Ahead Review

The alignment review passed the research checks for trailing windows and forward-return construction.

| Check | Status | Note |
|---|---|---|
| historical_window_check | PASS | Trailing returns, rolling volume baseline, and smoothing use current/past data only. |
| forward_return_alignment_check | PASS | Forward returns are computed after signal generation. |
| smoothing_leakage_check | PASS | Smoothing is trailing, not centered. |
| ranking_alignment_check | PASS | Cross-sectional ranks are same-date only. |
| same_bar_timing_review | REVIEW | Same-date close/volume inputs require after-close or next-rebalance convention in future production review. |
| paused_candidates_excluded | PASS | Volatility, residual momentum, LOW_BREADTH, portfolio, ML, and Conditional-Alpha paths were not included. |

The remaining timing issue is not evidence of leakage in the research diagnostic, but it must be resolved explicitly before production registration.

## Candidate Decision

Final classification:

`production-candidate revalidation passed with review items`

Primary reasons:

- h20 remained the primary horizon.
- Multi-horizon scoring remained coherent.
- Panel quality and missingness remained stable.
- Stress/regime behavior remained consistent with the prior liquidity-flow thesis.
- Drift versus prior isolated integration artifacts was effectively zero.

Review items:

- WFV persistence remained mixed at 0.50.
- WFV sign consistency remained mixed at 0.50.
- Correlation with unweighted reversal remained high at 0.721718.
- Same-bar timing convention requires explicit production review.
- The historical near-equivalence limitation remains because raw sidecar signal matrices were unavailable in earlier parity work.

## Review Items Carried Forward

Carry forward the following items into the controlled production-registration decision memo:

- Confirm whether mixed WFV persistence is acceptable for a production-candidate draft or requires another isolated WFV review.
- Determine whether the high unweighted-reversal overlap is conceptually acceptable given the liquidity-flow weighting.
- Preserve h20 as the primary horizon and treat h1/h5/h10 as diagnostics.
- Monitor turnover spikes, especially around stress and transition periods.
- Require explicit after-close or next-rebalance timing semantics before registration.
- Keep the rollback trail tied to `volume_shock_reversal_production_candidate_v1`.
- Continue excluding paused candidates until their separate review issues are resolved.

## Recommended Next Step

Proceed to a `controlled production-registration decision memo` for `volume_shock_reversal_stable_20` only.

That memo should decide whether the remaining WFV, reversal-overlap, and timing review items are acceptable for an explicitly controlled production-candidate registration step. It should not register the signal by itself, mutate survivor/watchlist lists, or alter any validation threshold.
