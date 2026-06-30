# Persistence Conditional Validation Review v1

Date: 2026-06-18

Project: Project Underdog

Primary candidate: `post_drawdown_persistence_churn_adjusted_20`

Current outcome: `CONDITIONAL VALIDATION CANDIDATE`

Scope: review-only conditional validation review. No refinement execution, validation execution, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

The persistence track is best frozen as a conditional validation candidate rather than given one final refinement attempt now.

The validation result is not a failure. `post_drawdown_persistence_churn_adjusted_20` retained positive h10 and h20 evidence, preserved 3-of-4 positive walk-forward-style windows at both primary horizons, maintained broad active coverage on active dates, and did not show artifact-level stress-repair contamination. This is enough to keep persistence alive as a credible diversification thread.

The result is also not strong enough to justify more tuning. The h20 profile is positive but thin, the h20 positive IC rate is only `0.518595`, recent h20 behavior is barely above neutral, and the best horizon remains h5 rather than the pre-declared h10/h20 validation objective. A final refinement would likely chase horizon shape or state exclusions after seeing validation evidence, which would weaken Project Underdog's research discipline.

Classification recommendation: `freeze as conditional validation candidate`.

## SECTION 2 - Validation Result Diagnosis

Primary validation metrics for `post_drawdown_persistence_churn_adjusted_20`:

| Horizon | Mean IC | IC IR | Positive IC rate | Dates |
|---:|---:|---:|---:|---:|
| h1 | 0.003769 | 0.048392 | 0.512922 | 503 |
| h5 | 0.012780 | 0.163326 | 0.589178 | 499 |
| h10 | 0.010952 | 0.138566 | 0.570850 | 494 |
| h20 | 0.006532 | 0.089364 | 0.518595 | 484 |

h10 strength:

The h10 result is the strongest validation-quality evidence for the candidate. It remains positive after freezing the refined formulation, with mean IC `0.010952`, IC IR `0.138566`, and positive IC rate `0.570850`. The h10 walk-forward-style profile had three positive windows and one negative first window. The most recent h10 window was constructive, with mean IC `0.012474` and positive IC rate `0.650407`.

h20 weakness:

h20 remains the limiting horizon. Mean IC stayed positive at `0.006532`, but IC IR fell to `0.089364` and positive IC rate fell to `0.518595`. The recent h20 window had mean IC `0.005903` and positive IC rate `0.504132`, which is positive but close to neutral. This is not a collapse, but it is not a robust long-horizon confirmation.

WFV sign consistency:

Both h10 and h20 showed 3 positive windows and 1 negative window, producing WFV persistence/sign consistency of `0.750000` at each primary horizon. This supports conditional survival, especially because the negative window was the first validation window rather than the most recent one. However, one negative window at both horizons prevents a clean robustness read.

Positive IC rate:

Positive-rate behavior is acceptable at h10 and weak at h20. h10 positive IC rate of `0.570850` is consistent with the persistence thesis. h20 positive IC rate of `0.518595` is the main validation risk and was the explicit reason the validation execution classified the candidate as conditional.

Active coverage:

Active coverage is not the main weakness. The candidate had `504` active dates, active date ratio `0.240229`, and mean active coverage `0.994649` on active dates. The signal is episodic by design because it activates around post-drawdown persistence context, but when active it covers nearly the full available universe. The low active date ratio should be monitored, not treated as a fatal flaw.

Stress-repair correlation:

Stress-repair contamination was not observed at the artifact level. Maximum stress-repair reference absolute correlation was `0.117322`, with top reference `stress_proxy_percentile_rank_stability_20_downtrend`, and `contamination_flag` was `False`. The strongest concept state was `RANGE_NORMALIZING`, which is consistent with persistence after drawdown rather than direct hostile/stress-repair replication.

Degradation versus refinement:

The candidate degraded from refinement to validation, but not catastrophically:

| Stage | h10 mean IC | h10 IC IR | h10 positive IC rate | h20 mean IC | h20 positive IC rate |
|---|---:|---:|---:|---:|---:|
| Refinement | 0.0172 | 0.1734 | 0.6012 | 0.0099 | 0.5372 |
| Validation | 0.010952 | 0.138566 | 0.570850 | 0.006532 | 0.518595 |

The degradation looks like validation shrinkage in a medium-horizon research signal. It does not erase the candidate, but it reduces the case for further same-lineage tuning.

## SECTION 3 - Limit vs Refinement Assessment

The weakness appears more structural than refinement-fixable.

Structural evidence:
- Best horizon is h5, while validation was designed around h10/h20.
- h20 remains positive but consistently weaker than h5/h10 across discovery, refinement, and validation.
- State attribution shows negative h20 behavior in `RECENT_VOL_STRESS`, `DISPERSION_NORMALIZING`, and `DISPERSION_STABILITY_TRANSITION`.
- The recent h20 positive IC rate is only `0.504132`, suggesting weak long-horizon persistence rather than a single missing adjustment.

Noise-driven evidence:
- The first validation window was negative at both h10 and h20, while later windows were positive.
- h10/h20 aggregate evidence remained positive, so the candidate was not simply invalidated by validation.
- The core lineage control produced nearly identical validation behavior, which reduces one-off formula concern but also confirms that the weakness belongs to the mechanism.

Refinement-fixable evidence:
- A narrow final attempt could theoretically reduce h20 weakness by changing the churn penalty or active-state strictness.
- State diagnostics imply that the signal works better in range-normalizing and elevated-dispersion-recent states than in dispersion-normalizing or stress states.

Overfit-risk evidence:
- Any adjustment made now would be informed by validation h20 weakness and state attribution, creating horizon-chasing and state-mining risk.
- The successful persistence variants are already highly correlated siblings, not independent family members.
- A final refinement would most likely create another close variant of `post_drawdown_persistence_churn_adjusted_20`, not a broader persistence family proof.

Conclusion: the practical limit has likely been reached for this lineage under the current research sample. The candidate should be frozen as conditional and used as evidence for persistence-family potential, while new alpha-family exploration moves elsewhere.

## SECTION 4 - Final Refinement Risk Review

If one final refinement were considered, it would have to be extremely narrow:
- It could only adjust the existing rank-churn penalty within the same post-drawdown rank-persistence formula.
- It could only compare against the frozen parent and core lineage controls.
- It could not introduce new horizons, new states, new filters, new production features, new stress-repair inputs, or new candidate families.
- It could not select a winner based on h20 alone.
- It could not use validation state attribution as a shopping list for exclusions.

What must not be changed:
- Family: persistence.
- Candidate mechanism: post-drawdown rank persistence with churn discipline.
- Primary validation orientation: h10/h20.
- Research-only status.
- Existing governance standards, thresholds, schemas, and production wiring.
- No hostile, participation-repair, liquidity-repair, weak-breadth, ML, or stress-repair machinery.

Why this would still be risky:

Even with tight rules, a final refinement would occur after a conditional validation read. The most obvious changes would be attempts to improve h20 positive-rate behavior or remove weak states. That is precisely the kind of post-validation tuning that can convert a disciplined research thread into parameter mining. Because the candidate already survived as conditional and the failure mode is a structural horizon limitation, the marginal information value of one more refinement is low.

Recommendation: do not run another persistence refinement cycle at this time.

## SECTION 5 - Research Track Recommendation

Classification: `freeze as conditional validation candidate`.

Rationale:
- Persistence survived validation as a credible candidate lineage.
- The h10 profile remains useful and economically coherent.
- h20 is positive but too thin for a clean pass.
- Stress-repair contamination remains low.
- Additional tuning would likely chase validation diagnostics rather than test a fresh hypothesis.
- The broader persistence family is still not proven beyond one close lineage.

Persistence should remain in the research inventory as conditional evidence, not as an active refinement target. Future persistence work should only reopen if a genuinely distinct persistence mechanism is proposed, not if the goal is to polish this same post-drawdown lineage.

## SECTION 6 - Next Family Frontier

Recommended next frontier: `rank-coherence`.

Reasoning:

Rank-coherence is the cleanest next alpha-family frontier because it is adjacent enough to reuse what persistence taught but different enough to avoid another near-duplicate post-drawdown refinement. The persistence result suggests that cross-sectional rank structure contains useful information, but the current post-drawdown version is horizon-limited. A rank-coherence family could test whether stable agreement across rank signals, peer groups, or time-sliced rank behavior creates a broader and less state-dependent alpha axis.

Relative to the alternatives:
- `transition-state dynamics` is attractive but risks overlapping the already fragile dispersion-transition work.
- `peer-relative behavior` is promising and could be a later branch of rank-coherence, but it should be framed carefully to avoid becoming sector or industry residual tinkering.
- `dispersion continuation` remains distinct but weak; prior dispersion refinement did not improve evidence quality and h20 decay remained unresolved.
- Other frontier ideas should wait until the project has tested whether rank structure can generalize beyond the post-drawdown persistence lineage.

Recommended framing for the next frontier:
- Explore rank-coherence as a fresh family discovery design.
- Keep it independent from `post_drawdown_persistence_churn_adjusted_20`.
- Prohibit direct reuse of validation diagnostics from the persistence candidate.
- Include redundancy checks against hostile/stress-repair and persistence lineage controls from the start.

## SECTION 7 - Final Recommendation

1. Has persistence reached its practical current limit?

Yes, for this lineage. `post_drawdown_persistence_churn_adjusted_20` has likely reached its practical current limit as a medium-horizon, post-drawdown rank-persistence candidate. The remaining weakness is h20 robustness and positive-rate thinness, not an obvious defect that a disciplined micro-refinement can safely repair.

2. Should we attempt one final refinement?

No. A final refinement is not recommended. The candidate has already been discovered, refined, and validated as conditional. Further tuning would risk horizon chasing and validation leakage.

3. Should persistence remain active or frozen?

Persistence should be frozen as a conditional validation candidate. It should remain available for interpretation, comparison, and future family-level context, but not remain an active same-lineage refinement track.

4. Which new family should be explored next?

Explore `rank-coherence` next. It offers the best balance between evidence continuity and true diversification potential.

5. What should the next Codex task be?

The next Codex task should be a design-only `rank_coherence_alpha_family_discovery_design_v1` memo. It should define a small, disciplined discovery program for rank-coherence candidates, specify anti-mining controls, require redundancy checks versus persistence and hostile/stress-repair references, and explicitly prohibit validation execution, refinement execution, governance mutation, threshold changes, production registration, ML, and candidate promotion/demotion.

## Review Caveat

This memo is a review-only assessment. It does not execute refinement or validation, does not modify governance or thresholds, does not register anything to production, does not implement ML, and does not promote or demote any candidate.
