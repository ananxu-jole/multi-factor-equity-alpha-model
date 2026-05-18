# Controlled Production-Registration Decision Memo: Volume Shock Reversal

## 1. Executive Takeaway

This memo reviews whether `volume_shock_reversal_stable_20` should advance from isolated production-candidate revalidation into controlled production-registration consideration.

Final decision:

`approve controlled registration with review items`

This is not production registration. The recommendation is to allow a future controlled registration step to be planned for this signal only, with explicit monitoring, rollback, and no automatic promotion into survivor, portfolio, or ML workflows.

The decision is deliberately guarded. The candidate has a coherent evidence chain, stable h20 behavior, no onboarding drift, plausible turnover, and useful stress/regime behavior. However, WFV persistence and sign consistency remain mixed at 0.50, and correlation with unweighted reversal remains elevated at 0.721718. These issues are not severe enough to reject the candidate at this decision stage, but they are material enough to require registration controls.

No production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio logic, validation logic, ML layers, or Conditional-Alpha paths were modified.

## 2. Evidence Chain Summary

### Robustness-First Orthogonal Discovery

`volume_shock_reversal_stable_20` emerged from the robustness-first standalone discovery batch as one of three research survivor candidates.

Initial discovery evidence:

- Family: `liquidity_flow`
- Best horizon: h20
- Sidecar WFV effective test IC: 0.026315
- Sidecar WFV IR: 0.921072
- Positive window rate: 0.75
- Initial rationale: strongest orthogonal liquidity-flow window stability among the batch survivors

This evidence was sidecar-only and did not constitute production registration, official WFV admission, or survivor-list mutation.

### Robustness Refinement

The three-sidecar-survivor refinement classified `volume_shock_reversal_stable_20` as a `refined survivor candidate`.

Refinement evidence:

- Nearby volume-shock and smoothing variants were tested.
- 7 of 9 nearby variants passed sidecar robustness checks.
- Longer volume-shock lookbacks and stronger smoothing reduced turnover.
- The smoother lower-turnover variant was favored over higher-churn forms.
- The candidate remained a liquidity-flow reversal structure rather than a conditional-alpha component.

Primary refinement caveat:

- Turnover and reversal overlap required continued monitoring before production onboarding.

### Isolated Draft Definition

The draft definition preserved the research identity as:

- smoothed abnormal-volume-weighted reversal
- liquidity-flow family
- h20 primary horizon
- OHLCV-only
- no regime gate
- no sector dependency
- no Conditional-Alpha semantics

The draft also clarified that the trailing `20` in the name refers to the intended h20 research horizon, not necessarily a required volume-shock lookback.

### Implementation-Equivalence Tests

The isolated implementation-equivalence test classified the signal as:

`near-equivalent with minor review items`

Positive evidence:

- Formula semantics were preserved.
- Sign convention was preserved.
- h20 remained the intended primary horizon.
- Turnover behavior remained plausible.

Review limitation:

- Raw sidecar signal matrices were unavailable, so bit-level raw-value and rank-level parity against the original sidecar run could not be proven.
- Coverage differed materially versus the original sidecar metric summaries, likely due to stricter sidecar universe or availability masks.

### Isolated Signal-Factory Integration Tests

The isolated signal-factory integration test classified the signal as:

`integration-compatible with review items`

Positive evidence:

- Metadata validation passed.
- Isolated factory-style generation completed cleanly.
- Panel shape and coverage were stable.
- h20 scoring behavior matched the isolated equivalence artifacts.
- WFV-style logic consumed the signal without special handling.
- Stress/regime attribution remained coherent.

Primary review item:

- Meaningful overlap with unweighted reversal remained visible.

### Isolated Production-Candidate Revalidation

The isolated production-candidate revalidation classified the signal as:

`production-candidate revalidation passed with review items`

Key measured results:

| Metric | Value |
|---|---:|
| Primary horizon | h20 |
| h20 mean IC | 0.011798 |
| h20 IC IR | 0.070228 |
| Effective mean test IC | 0.004308 |
| Effective test IC IR | 0.346720 |
| WFV persistence | 0.500000 |
| WFV sign consistency | 0.500000 |
| Turnover proxy | 0.098531 |
| Unweighted reversal correlation | 0.721718 |
| Drift versus prior isolated integration | effectively zero |

This stage is the strongest evidence that onboarding mechanics are stable, but it also confirms that the candidate is not free of review risk.

## 3. Registration Readiness Assessment

### h20 Stability

Readiness assessment: favorable.

`h20` remained the strongest horizon in the isolated production-candidate revalidation:

| Horizon | Mean IC | IC IR | Positive IC Rate |
|---:|---:|---:|---:|
| h1 | 0.005437 | 0.027643 | 0.506101 |
| h5 | 0.010449 | 0.057256 | 0.518337 |
| h10 | 0.011421 | 0.066956 | 0.517157 |
| h20 | 0.011798 | 0.070228 | 0.513300 |

The horizon profile is coherent: h20 leads, and shorter horizons remain directionally positive rather than contradictory.

### Onboarding Drift

Readiness assessment: favorable.

Drift versus prior isolated signal-factory integration evidence was effectively zero. There was no suspicious metric improvement and no material degradation in mean IC, IC IR, positive IC rate, missingness, finite coverage, or turnover proxy.

This supports the view that the isolated production-candidate implementation preserved the prior isolated integration behavior.

### WFV Persistence

Readiness assessment: review required.

The isolated WFV revalidation was mixed:

- Effective mean test IC: 0.004308
- Effective test IC IR: 0.346720
- Persistence: 0.50
- Sign consistency: 0.50
- Windows: 4

This is not strong enough to call the WFV evidence clean. It does not invalidate the candidate by itself because this memo concerns controlled registration consideration rather than promotion, but it should prevent any automatic survivor or portfolio use.

### Sign Consistency

Readiness assessment: review required.

Sign consistency at 0.50 means the candidate does not yet show broad window-level directional reliability under the isolated WFV diagnostic. The signal is directionally coherent across full-sample horizons, but window-level behavior remains uneven.

Controlled registration is only appropriate if the next step treats this as a monitored risk, not as a solved issue.

### IC / IR Strength

Readiness assessment: modest but acceptable for controlled registration consideration.

The h20 full-sample mean IC and IC IR are positive but not large:

- h20 mean IC: 0.011798
- h20 IC IR: 0.070228

This candidate should not be advanced because of headline IC. The stronger case is that it offers a stable, interpretable liquidity-flow variant with reproducible isolated metrics and plausible stress behavior.

### Turnover Plausibility

Readiness assessment: favorable with monitoring.

The isolated turnover proxy was 0.098531, with p95 turnover at 0.153068. This is plausible for a production-candidate draft and materially less concerning than earlier high-churn volume-shock variants.

Turnover should still be monitored because volume-shock reversal structures can become costly when implemented with less smoothing or during unstable transition periods.

### Stress / Regime Behavior

Readiness assessment: supportive, not decisive.

The stress/regime revalidation showed coherent behavior, especially in panic/liquidity stress:

| State | Mean IC | IC IR | Positive IC Rate |
|---|---:|---:|---:|
| drawdown_acceleration | 0.029143 | 0.157260 | 0.533808 |
| volatility_spike | 0.015921 | 0.076991 | 0.448529 |
| panic_liquidity_stress | 0.070692 | 0.389327 | 0.673171 |
| trend_transition | 0.016176 | 0.095652 | 0.517141 |
| recovery_phase | 0.012952 | 0.085040 | 0.538462 |
| high_dispersion_rotation | 0.007620 | 0.044404 | 0.527619 |

The signal appears most useful in panic/liquidity stress, which is consistent with a liquidity-flow reversal interpretation. The volatility-spike positive rate below 0.50 remains a caution.

### Orthogonality

Readiness assessment: mixed.

The candidate remains meaningfully distinct from simple volume-shock baselines:

| Comparison | Value Corr | Top/Bottom Overlap |
|---|---:|---:|
| simple_volume_spike_reversal | 0.428076 | 0.286796 |
| no_stability_volume_reversal | 0.428809 | 0.292593 |

This supports the view that the abnormal-volume/stability construction adds structure beyond the most naive volume-shock variants.

However, overlap with broader reversal structures remains material:

| Comparison | Value Corr | Top/Bottom Overlap |
|---|---:|---:|
| unweighted_reversal | 0.721718 | 0.471053 |
| liquidity_flow_slow_proxy | 0.690231 | 0.451869 |
| plain_reversal20_smooth5 | 0.684895 | 0.424063 |

The signal should therefore be treated as a liquidity-weighted reversal refinement, not as a wholly orthogonal standalone family.

## 4. Main Review Issue: Unweighted Reversal Overlap

The main unresolved question is whether the abnormal-volume/stability-weighted construction adds enough incremental value beyond unweighted reversal.

Evidence supporting incremental value:

- The signal is materially less correlated with simple volume-shock reversal than with plain reversal, suggesting the volume/stability layer is changing the construction.
- The smoother refined version reduced turnover compared with noisier sidecar variants.
- Stress/regime behavior is strongest in panic/liquidity stress, which is consistent with liquidity-flow economics rather than generic reversal alone.
- Drift through the onboarding chain was essentially zero, which reduces the risk that the apparent behavior is an implementation artifact.

Evidence against a clean orthogonality claim:

- Correlation with unweighted reversal is high at 0.721718.
- Top/bottom overlap with unweighted reversal is 0.471053.
- The candidate may be best interpreted as a controlled refinement of reversal exposure, not a fully independent liquidity-flow alpha.
- WFV persistence and sign consistency are only 0.50, which weakens the argument that the volume layer stabilizes window-level behavior enough on its own.

Conclusion:

The abnormal-volume/stability construction appears to add some incremental structure, but not enough to treat the candidate as strongly orthogonal. The signal is suitable for controlled registration consideration only if the registration decision explicitly labels it as a liquidity-weighted reversal candidate with redundancy monitoring. It should not be sold internally as a clean new factor family.

## 5. Decision Options

### A. Approve Controlled Registration With Review Items

Pros:

- h20 behavior is stable and reproduced.
- Onboarding drift is effectively zero.
- Metadata and isolated generation are clean.
- Turnover is plausible.
- Stress/regime behavior is coherent.
- The candidate is the cleanest survivor from the volume/liquidity-flow side of the robustness-first restart.

Cons:

- WFV persistence is mixed.
- WFV sign consistency is mixed.
- Reversal overlap remains elevated.
- Production timing semantics still need explicit after-close or next-rebalance handling.

Assessment:

This is the recommended option. It keeps the candidate moving through a controlled process without allowing premature promotion or portfolio use.

### B. Defer Registration Pending Orthogonality Review

Pros:

- Directly addresses the main unresolved risk.
- Avoids registering a signal that may mostly duplicate unweighted reversal.

Cons:

- The current evidence is already sufficient to design a controlled registration path with orthogonality flags.
- Deferral may stall the onboarding protocol even though drift, metadata, and isolated scoring behavior are clean.

Assessment:

Reasonable but too conservative for the current stage. Orthogonality review should be carried forward as a control, not used to stop controlled registration consideration.

### C. Reject Registration

Pros:

- Avoids possible redundancy and weak WFV persistence.

Cons:

- Discards a reproducible, interpretable, h20-stable candidate with plausible turnover and stress behavior.
- Overweights review issues that are better handled by controlled registration limits.

Assessment:

Not recommended. The evidence does not justify rejection.

### D. Keep as Research-Only Candidate

Pros:

- Maintains maximum conservatism.
- Avoids any risk of production-candidate contamination.

Cons:

- The candidate has already passed enough isolated onboarding checks to warrant a controlled registration decision path.
- Keeping it indefinitely research-only would reduce the value of the onboarding protocol just validated.

Assessment:

Not recommended as the primary decision. It remains research-only until an explicit later registration step, but this memo should advance the controlled-registration decision process.

## 6. Final Recommendation

Recommend:

`approve controlled registration with review items`

This means Project Underdog may proceed to a controlled registration step for `volume_shock_reversal_stable_20` only, provided the step is explicitly scoped, reversible, and separated from promotion.

This recommendation does not authorize:

- automatic survivor/watchlist mutation
- alpha-pool admission
- portfolio construction use
- ML feature use
- threshold changes
- gate relaxation
- Conditional-Alpha integration
- promotion to core or satellite status

The candidate should enter any future registration step as:

`PRODUCTION_CANDIDATE_WITH_REVIEW_ITEMS`

not as a validated production alpha.

## 7. If-Approved Controls

If the candidate proceeds to a future controlled registration step, the following controls should be mandatory.

### Review Flags

- `WFV_PERSISTENCE_MIXED`
- `SIGN_CONSISTENCY_MIXED`
- `UNWEIGHTED_REVERSAL_OVERLAP_HIGH`
- `TIMING_SEMANTICS_REVIEW_REQUIRED`
- `RAW_SIDECAR_MATRIX_PARITY_UNAVAILABLE`
- `TURNOVER_MONITORING_REQUIRED`

### Monitoring Requirements

- Reconfirm h20 as the primary horizon after registration.
- Monitor h1/h5/h10 only as diagnostics.
- Compare registered output against the isolated production-candidate artifact set.
- Track drift in mean IC, IC IR, positive IC rate, coverage, missingness, turnover, WFV windows, and stress slices.
- Monitor correlation and top/bottom overlap versus unweighted reversal and plain smoothed reversal.
- Monitor stress behavior in panic/liquidity stress, drawdown acceleration, and trend-transition states.

### Rollback Triggers

Pause or roll back registration research if any of the following occur:

- h20 stops being the primary coherent horizon.
- Sign convention changes or flips.
- WFV persistence weakens further.
- WFV sign consistency weakens further.
- Effective mean test IC turns materially negative.
- Turnover increases materially versus the isolated proxy of 0.098531.
- Correlation with unweighted reversal increases enough that incremental identity is no longer credible.
- Stress behavior deteriorates, especially in panic/liquidity stress.
- Implementation creates suspicious metric improvement.
- Same-bar timing cannot be resolved under a clean after-close or next-rebalance convention.
- Any production contamination risk appears.

### Usage Restrictions

- No automatic portfolio use.
- No ML use.
- No survivor promotion without later explicit approval.
- No watchlist mutation without later explicit approval.
- No 04A+ or downstream alpha construction triggered solely by registration.
- No registration of paused candidates through this memo.

## 8. If-Deferred Requirements

If the project chooses to defer rather than approve controlled registration, the minimum additional evidence needed would be:

- A focused orthogonality review against unweighted reversal, plain smoothed reversal, and existing reversal-like signals.
- A marginal contribution test showing whether abnormal-volume weighting improves behavior after controlling for plain reversal exposure.
- A WFV window decomposition explaining why persistence and sign consistency are only 0.50.
- A timing-semantics review confirming whether same-date close/volume inputs can be used under the intended rebalance convention.
- A stress-specific attribution check focused on whether panic/liquidity-stress strength survives after controlling for generic reversal.

These are useful future controls, but the current recommendation is to carry them into controlled registration rather than block the next step.

## 9. Expansion Readiness Assessment

Project Underdog can resume broader alpha discovery after this memo.

Rationale:

- The controlled onboarding protocol has now been exercised from draft definition through isolated production-candidate revalidation.
- The process successfully separated one advancing candidate from paused candidates.
- The system identified review items without relaxing gates or forcing promotion.
- The current signal remains under review, but its unresolved issues do not require freezing broader discovery.

Recommended discovery posture:

- Resume robustness-first standalone discovery expansion.
- Prioritize orthogonal standalone families rather than Conditional-Alpha semantics.
- Continue emphasizing h20 stability, WFV persistence, stress coherence, turnover plausibility, and attribution clarity.
- Give priority to liquidity-flow, residual/relative-value redesign, dispersion-aware standalone structures, and turnover-aware reversal refinements.
- Keep `volatility_surprise_reversal_20_60_smooth` paused until its h20 drift and baseline similarity issues are resolved.
- Keep LOW_BREADTH Conditional-Alpha work paused as a side framework.

Expansion should not wait for this candidate to become fully registered. The candidate can proceed through its controlled decision path while research resumes in parallel.

## 10. Recommended Next Step

Recommended next move:

`controlled registration with review items`

Operationally, the next artifact should be a controlled registration implementation plan for `volume_shock_reversal_stable_20` only, explicitly preserving the controls in this memo and still avoiding automatic survivor, portfolio, ML, or Conditional-Alpha use.

Broader alpha discovery can resume in parallel under the robustness-first standalone framework.
