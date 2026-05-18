# Parallel Research Tracks After Volume Registration Decision

## 1. Executive Takeaway

Project Underdog should now operate on two parallel research tracks:

- Track A: controlled registration governance for `volume_shock_reversal_stable_20`
- Track B: robustness-first standalone discovery expansion

Final immediate execution recommendation:

`both tracks in parallel with Track B first`

Track A should keep the volume candidate under controlled governance because it was approved for controlled registration consideration only with review items. It is not a clean production signal, not a survivor, not a portfolio component, and not an ML feature.

Track B should resume broader standalone alpha discovery because the onboarding protocol has now been exercised from draft definition through isolated production-candidate revalidation. The project does not need to freeze discovery while the volume candidate remains under governance review.

This note is research/planning only. It does not perform production registration and does not modify production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha paths.

## 2. Current Project State

The controlled decision memo for `volume_shock_reversal_stable_20` recommended:

`approve controlled registration with review items`

Meaning:

- The candidate has earned controlled registration consideration.
- The onboarding protocol is sufficiently validated to be reused.
- The signal is not approved for clean production use.
- The signal is not approved for portfolio deployment.
- The signal is not approved for automatic survivor promotion.

Key measured evidence from isolated production-candidate revalidation:

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
| Onboarding drift | effectively zero |

Current interpretation:

- The candidate is stable enough to govern through a controlled registration path.
- The candidate is not strong enough to bypass review controls.
- Broader discovery can resume because the platform rejected overclaiming and preserved separation between research, registration consideration, and deployment.

## 3. Track A — Controlled Registration Governance

### Focus

Track A governs only:

`volume_shock_reversal_stable_20`

Current status:

`APPROVED_FOR_CONTROLLED_REGISTRATION_CONSIDERATION_WITH_REVIEW_ITEMS`

It should be treated as a production-candidate under governance, not as a validated production alpha.

### Review Flags

Track A should carry forward these review flags:

- `WFV_PERSISTENCE_MIXED`
- `SIGN_CONSISTENCY_MIXED`
- `UNWEIGHTED_REVERSAL_OVERLAP_HIGH`
- `TIMING_SEMANTICS_REVIEW_REQUIRED`
- `TURNOVER_MONITORING_REQUIRED`
- `RAW_SIDECAR_MATRIX_PARITY_UNAVAILABLE`
- `ROLLBACK_REQUIREMENTS_REQUIRED`

### Required Monitoring

Monitoring should cover:

- h20 primary-horizon preservation
- h1/h5/h10 diagnostic drift
- mean IC and IC IR drift
- effective mean test IC drift
- WFV persistence and sign consistency
- stress behavior in panic/liquidity stress, drawdown acceleration, and trend-transition states
- turnover proxy, p95 turnover, and turnover spikes
- correlation and top/bottom overlap versus unweighted reversal
- correlation versus plain smoothed reversal and simple volume-shock reversal
- date/ticker coverage and missingness
- same-bar timing convention

### Rollback Triggers

Pause or roll back Track A if:

- h20 stops being the coherent primary horizon.
- Sign convention changes.
- WFV persistence weakens below the current mixed baseline.
- WFV sign consistency weakens below the current mixed baseline.
- Effective mean test IC becomes materially negative.
- Turnover increases materially versus the isolated proxy of 0.098531.
- Correlation with unweighted reversal rises enough to eliminate credible incremental identity.
- Stress behavior deteriorates materially in panic/liquidity stress.
- Registered output drifts from the isolated production-candidate artifact set.
- Same-bar timing cannot be resolved under a clean after-close or next-rebalance convention.
- Any production contamination risk appears.

### Same-Bar Timing Review Needs

The signal uses close and volume inputs. Before any actual production registration, Track A must document:

- whether signal values are formed after the close
- when ranks are available
- when trades would hypothetically rebalance
- whether the intended convention is next-close, next-open, or next-session rebalance
- whether volume is fully known at signal formation time
- whether smoothing and ranking introduce any same-bar leakage

This is not a reason to reject the signal now, but it is a hard blocker before deployment-style interpretation.

### Unweighted Reversal Overlap Monitoring

The current unweighted-reversal correlation is 0.721718. Track A should treat this as a live redundancy risk.

Required checks:

- monitor value correlation versus unweighted reversal
- monitor rank correlation by date
- monitor top/bottom overlap
- run marginal contribution diagnostics versus plain reversal
- verify whether panic/liquidity-stress behavior survives after controlling for generic reversal
- document whether the signal is best described as a liquidity-weighted reversal refinement rather than an independent liquidity-flow factor

### Turnover Monitoring

The current turnover proxy is 0.098531, with p95 turnover at 0.153068. Track A should monitor:

- average turnover
- p95 turnover
- max turnover
- turnover spikes around stress and transition states
- turnover drift after any registration-style integration
- whether smoothing continues to control churn

### WFV / Stress Monitoring

WFV and stress monitoring should remain explicit because WFV persistence and sign consistency are both mixed at 0.50.

Track A should not reinterpret mixed WFV as clean validation. The candidate remains under review until window behavior is better understood or accepted as a known limitation.

### Controlled Registration Boundaries

Track A does not permit:

- portfolio use
- ML use
- automatic survivor promotion
- automatic watchlist mutation
- clean production deployment
- 04A+ execution triggered by this memo
- threshold changes
- gate relaxation
- Conditional-Alpha integration
- registration of paused candidates

## 4. Track A Next Steps

Recommended Track A sequence:

1. Controlled registration implementation plan
2. Same-bar timing audit
3. Unweighted reversal overlap audit
4. Turnover and stress monitoring plan
5. Rollback decision checklist
6. Controlled registration readiness checklist

### 1. Controlled Registration Implementation Plan

Purpose:

Define how the signal would be introduced as a controlled production-candidate without automatic promotion or table contamination.

Required content:

- candidate metadata package
- isolated registration status
- expected artifact names
- run namespace
- comparison baseline against isolated production-candidate artifacts
- rollback procedure
- explicit non-promotion language

### 2. Same-Bar Timing Audit

Purpose:

Resolve the current timing review item before any registration-style use.

Key question:

Can close and volume inputs be used under an after-close or next-rebalance convention without look-ahead ambiguity?

### 3. Unweighted Reversal Overlap Audit

Purpose:

Determine whether abnormal-volume weighting contributes enough incremental behavior beyond plain reversal.

This should be a focused research audit, not a gate change.

### 4. Turnover and Stress Monitoring Plan

Purpose:

Define how turnover and stress drift will be monitored if the candidate enters a controlled registration step.

### 5. Rollback Decision Checklist

Purpose:

Create a short operational checklist for when to pause, revert, or reject onboarding research.

### 6. Controlled Registration Readiness Checklist

Purpose:

Confirm whether all Track A controls are in place before any actual registration request is made.

## 5. Track B — Robustness-First Discovery Expansion

Track B resumes broader standalone alpha discovery.

The goal is not to find flashy IC spikes. The goal is to find standalone, interpretable, robust alpha candidates with enough orthogonality and stress coherence to deserve the same controlled onboarding discipline used for the volume candidate.

### Priority Families

Track B should prioritize:

- liquidity-flow
- residual / relative-value
- volatility-structure redesign
- interaction structures
- dispersion-aware standalone signals
- turnover-aware standalone signals

### Research Emphasis

Each candidate should be designed around:

- orthogonality
- persistence
- stress robustness
- horizon stability
- turnover discipline
- attribution clarity
- implementation simplicity
- OHLCV-only feasibility unless explicitly expanded later

### What To Avoid

Track B should avoid:

- pure IC chasing
- Conditional-Alpha semantics
- weakly interpretable structures
- blend camouflage
- redundant momentum or trend proxies
- excessive parameter sprawl
- fragile high-turnover structures
- candidates that require relaxed gates to survive

### Family Notes

Liquidity-flow:

- Continue exploring volume/price-flow structures, but reduce plain reversal overlap.
- Favor turnover-controlled designs.
- Compare every candidate against simple volume-spike reversal and unweighted reversal.

Residual / relative-value:

- Redesign around cleaner orthogonality after `residual_momentum_stability_60` showed excessive trend/momentum entanglement.
- Avoid repackaged momentum.
- Use benchmark-relative or residual structures only when the residualization adds measurable uniqueness.

Volatility-structure redesign:

- Keep `volatility_surprise_reversal_20_60_smooth` paused.
- Future volatility candidates should address redundancy with simple volatility reversal and suspicious h20 improvement risk.
- Require baseline similarity checks early.

Interaction structures:

- Explore simple two-input interactions only when each term has clear economic meaning.
- Avoid complex blends that hide weak components.

Dispersion-aware standalone signals:

- Study whether cross-sectional dispersion can stabilize reversal or relative-value behavior without becoming a conditional gate.
- Keep the signal standalone and broadly active.

Turnover-aware standalone signals:

- Prefer smoother, slower candidates that maintain h10/h20 coherence.
- Treat lower turnover as useful only if the alpha identity is preserved.

## 6. Track B Next Discovery Batch Design

Recommended batch shape:

- Candidate count target: 8 to 12 standalone candidates
- Primary horizons: h10 and h20
- Diagnostic horizons: h1 and h5
- Families: 2 to 3 candidates each from liquidity-flow, residual/relative-value redesign, volatility-structure redesign, and dispersion/interaction structures
- Data scope: OHLCV-only unless explicitly justified later
- Conditional activation: excluded
- Production registration: excluded

### Candidate Requirements

Each candidate should document:

- signal name
- family
- formula intuition
- intended horizon
- expected sign
- expected orthogonality
- expected failure mode
- baseline comparisons
- turnover risk
- stress/regime hypothesis

### Scoring Expectations

Track B scoring should evaluate:

- h1/h5/h10/h20 mean IC
- abs mean IC
- IC IR
- positive IC rate
- sign consistency
- horizon stability
- missingness and coverage
- turnover proxy

The batch should not promote candidates for single-horizon spikes. h20 can be primary, but adjacent horizon behavior should remain coherent.

### WFV Expectations

WFV-style research should emphasize:

- effective mean test IC
- effective test IC IR
- persistence
- sign consistency
- window-level behavior
- one-window dominance
- train/test degradation

Moderate stable edges are preferable to unstable high-IC bursts.

### Stress / Regime Attribution Expectations

Every promising candidate should be reviewed across:

- drawdown acceleration
- volatility spike
- panic/liquidity stress
- trend transition
- recovery phase
- high dispersion / rotation

State-specific strength is useful, but candidates should not become hidden conditional-alpha candidates unless explicitly moved into the side framework later.

### Orthogonality Expectations

Track B should compare candidates against:

- existing pool/watchlist signals
- simple family baselines
- plain reversal
- plain momentum
- volatility reversal
- volume-shock reversal
- benchmark-relative proxies where relevant

Candidates with high baseline similarity should not advance without a clear marginal contribution story.

### Rejection Philosophy

Reject candidates early for:

- direction flips
- weak persistence
- weak sign consistency
- one-window dominance
- suspicious metric improvement
- excessive turnover
- hidden beta/trend/momentum duplication
- high baseline similarity
- poor interpretability
- conditional behavior masquerading as standalone robustness

Failures should be documented as useful evidence, not treated as wasted work.

## 7. Separation Rules

Track A and Track B must remain separate.

Required separation:

- separate run IDs
- separate artifact directories
- separate research notes
- separate candidate registries or draft definitions
- no shared promotion logic
- no survivor/watchlist mutation
- no portfolio integration
- no ML integration
- no Conditional-Alpha integration
- no table overwrites
- no gate, threshold, or schema changes

Suggested namespaces:

- Track A: `volume_shock_reversal_controlled_governance_v1`
- Track B: `robustness_first_discovery_expansion_v2`

The volume candidate may be used as a comparison baseline in Track B, but Track B should not mutate its status or rely on it as a production signal.

## 8. Shared Lessons From Onboarding Cycle

Reusable lessons:

- Semantic preservation matters before implementation.
- Draft definitions reduce formula drift.
- Implementation-equivalence testing should happen before integration-style tests.
- Raw matrix parity is valuable; if unavailable, the limitation must be carried forward.
- Suspicious improvement is a warning, not a success.
- Baseline similarity must be treated seriously.
- Candidates can advance asymmetrically.
- Controlled registration needs rollback logic before registration.
- Stress/regime behavior helps interpretation but does not replace WFV.
- Turnover improvements are only useful if signal identity is preserved.
- The onboarding protocol is reusable for future refined survivors.

The volume candidate advanced because its evidence chain was cleaner than paused alternatives. The volatility candidate paused because suspicious h20 improvement and baseline similarity remained unresolved. That asymmetry is a strength of the process.

## 9. Immediate Execution Recommendation

Recommend:

`both tracks in parallel with Track B first`

Execution order:

1. Start Track B with a robustness-first standalone discovery expansion batch.
2. Keep Track A active as governance documentation, not as immediate production registration.
3. Run Track A audits only when the project is ready to convert the memo into a controlled registration implementation plan.

Reasoning:

- The onboarding protocol is now validated enough to support future candidates.
- The volume candidate remains under review, so immediate production registration would be premature.
- Track B can generate new standalone evidence without contaminating Track A.
- The project needs more orthogonal standalone candidates before portfolio or survivor work becomes more meaningful.

Do not choose production registration as the next immediate task. The correct next move is research expansion with the volume candidate governed, not deployed.

## 10. Strategic Outlook

Project Underdog has reached a useful operating structure:

- Conditional-Alpha remains a side framework.
- The volume candidate becomes a governed onboarding case.
- Core research returns to standalone alpha discovery.
- The platform keeps strict rejection discipline and avoids forced survivors.

The next phase should use the validated onboarding discipline as a reusable standard. New candidates should not only score well; they should preserve semantics, reproduce cleanly, survive WFV-style review, show stress coherence, avoid excessive redundancy, and remain interpretable.

The project should now widen the research funnel again, but with better filters at every step.
