# Persistence Validation Eligibility Audit v1

Date: 2026-06-18

Project: Project Underdog

Primary candidate: `post_drawdown_persistence_churn_adjusted_20`

Origin:
- Parent candidate: `rank_stability_after_drawdown_02`
- Parent representative: `post_drawdown_persistence_20`
- Family: Persistence
- Theme: Rank Stability After Drawdown

Scope: review-only validation eligibility audit. No validation, additional refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Refinement improved the persistence candidate in a meaningful but still research-stage way. The original discovery representative, `post_drawdown_persistence_20`, already had the strongest IC profile in the diversification discovery subset: h10 mean IC 0.0125, h10 IC IR 0.1208, h10 positive IC rate 0.5951, and low approved-subset redundancy. The refinement successor, `post_drawdown_persistence_churn_adjusted_20`, improved the primary h10 profile to mean IC 0.0172, IC IR 0.1734, and positive IC rate 0.6012. It also improved h20 mean IC from 0.0059 to 0.0099.

The candidate appears stable enough for formal validation review consideration, not because it is broadly proven, but because the improvement survived a disciplined refinement space and was supported by a near-identical core variant. The strongest persistence results were not isolated to one formula: `post_drawdown_persistence_core_20` had h10 mean IC 0.0171, IC IR 0.1730, positive IC rate 0.6032, and h20 mean IC 0.0099.

The candidate remains distinct from hostile/stress-repair families at the artifact level. Its maximum stress-proxy correlation in the refinement redundancy context was 0.0633, with `percentile_rank_stability_20_downtrend` as the top stress proxy. Correlations versus failed-breakout stress proxies were lower. This does not fully eliminate contamination risk, because the candidate still uses downtrend/rank context, but the reviewed artifacts do not show direct recreation of hostile/stress-repair behavior.

Validation consideration is justified. The correct classification is **READY FOR VALIDATION REVIEW** as a research workflow status. This does not mean validated, production-ready, governance-approved, or threshold-qualified.

## SECTION 2 - Research Lineage Review

The original discovery candidate was `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`. It was selected because it was the strongest individual result in the 8-candidate IC discovery subset and combined positive h5/h10 behavior with low redundancy.

IC discovery results for the original representative:
- h1 mean IC: 0.0047
- h5 mean IC: 0.0137
- h10 mean IC: 0.0125
- h20 mean IC: 0.0059
- h10 IC IR: 0.1208
- h10 positive IC rate: 0.5951
- max approved-subset absolute correlation: 0.1815

The refinement design approved only a small persistence variant set. It allowed changes to rank-stability measurement, rank-churn handling, light smoothing, and drawdown-context strictness while keeping the family, theme, directional thesis, h10-h20 orientation, and research-only status fixed. Broad parameter expansion was explicitly prohibited.

The refinement successor `post_drawdown_persistence_churn_adjusted_20` penalized post-drawdown rank churn while preserving the post-drawdown rank-persistence thesis. It did not add participation, liquidity, weak-breadth, hostile-state, production, or ML machinery.

Refinement outcome for the successor:
- h1 mean IC: 0.0063
- h5 mean IC: 0.0184
- h10 mean IC: 0.0172
- h20 mean IC: 0.0099
- h10 IC IR: 0.1734
- h10 positive IC rate: 0.6012
- h20 positive IC rate: 0.5372

Assessment of improvement:
- Meaningful: yes. The h10 mean IC improved by roughly 0.0047, and h20 mean IC improved by roughly 0.0040 versus the original anchor.
- Marginal: not merely. The improvement was accompanied by stronger IC IR and was echoed by the core variant.
- Potentially noise-driven: still possible. The refinement was conducted on the same research sample and does not substitute for formal validation. The high similarity among persistence variants means the evidence is best read as a stronger version of one candidate thread, not as multiple independent confirmations.

## SECTION 3 - Robustness Assessment

Primary candidate metrics:
- h5 mean IC: 0.0184
- h10 mean IC: 0.0172
- h20 mean IC: 0.0099
- h10 IC IR: 0.1734
- h10 positive IC rate: 0.6012
- h20 positive IC rate: 0.5372
- h10/h20 date count: 494 at h10 and 494 at the best h10/h20 horizon

Horizon consistency:
- Strongest evidence remains h5/h10.
- h20 is positive and improved versus the original anchor, but still weaker than h5/h10.
- The profile is consistent with a medium-horizon persistence effect rather than a fully established h20 family anchor.

Redundancy context:
- High correlation with parent and sibling persistence variants is expected: max refinement absolute correlation was 0.9947 versus `post_drawdown_persistence_core_20`.
- High correlation with the original discovery parent was also expected: max discovery absolute correlation was 0.9932 versus `post_drawdown_persistence_20`.
- Low correlation versus stress proxies is favorable: max stress-proxy absolute correlation was 0.0633.
- Low correlation versus the dispersion transition anchor is favorable: correlation with `dispersion_transition_acceleration_20` was about 0.031-0.032 in the refinement/discovery contexts.

Refinement sensitivity:
- Positive evidence strengthened in the core and churn-adjusted variants.
- Smoothing weakened evidence, with h10 mean IC falling to 0.0102 and h20 mean IC to 0.0034.
- Strict context preserved the anchor-like result but did not materially improve it.

Strengths:
- Best result in the persistence refinement set.
- Improvement was not dependent on a complex new construction.
- Positive h5/h10 evidence is coherent and improved.
- h20 improved enough to reduce, though not eliminate, horizon-decay concern.
- Stress-proxy redundancy is low.

Weaknesses:
- Evidence remains research-only and in-sample to the refinement workflow.
- The candidate is highly similar to the parent and core variants, so the refinement does not provide independent family breadth.
- h20 remains weaker than h5/h10.
- Downtrend/rank context still requires formal contamination checks before any later validation interpretation.

Unresolved concerns:
- Whether the effect survives formal validation windows and walk-forward review.
- Whether active coverage is broad enough outside the reviewed sample.
- Whether the candidate activates disproportionately in post-drawdown or stress-adjacent episodes.
- Whether the persistence family can produce more than one credible nonduplicative candidate.

## SECTION 4 - Family Distinctiveness Assessment

Does this candidate strengthen the persistence family?

Yes. It strengthens the persistence family more than any prior diversification candidate because it improves the strongest discovery representative while preserving the rank-stability-after-drawdown thesis. The persistence family summary from refinement was positive at h5, h10, and h20, with h10 family mean IC 0.0139 and h10 mean positive IC rate 0.5928 across the small persistence refinement set.

Is it economically different from hostile/stress-repair behavior?

Mostly yes, with caveats. The economic story is rank persistence after drawdown: securities with stable/improving rank behavior after drawdown appear more durable than peers with higher rank churn. That is different from buying damaged names because they are recovering, repairing liquidity, or normalizing participation. The low stress-proxy correlations support this distinction. However, because the signal still uses downtrend/rank context, formal validation review should include explicit hostile/stress-repair contamination diagnostics.

Does it represent genuine diversification progress?

Yes, at the candidate-thread level. It offers a non-production research axis outside the dominant hostile/stress-repair family and remains low-correlated to stress proxies and dispersion candidates. The progress is not yet broad family diversification, but it is enough to advance the persistence thread into formal validation review consideration.

Is the family evidence broader than a single candidate?

Only partially. The original discovery persistence family was not broadly strong: `drawdown_rank_stability_20` was materially negative and `transition_rank_stability_20` was weak. The refinement set improved the persistence thread, but the successful variants are highly correlated siblings of the same parent. This is evidence for a refined candidate lineage, not evidence for a broad independent persistence family.

## SECTION 5 - Validation Readiness Assessment

Classification: **READY FOR VALIDATION REVIEW**

Reasoning:
- The candidate improved meaningfully versus the discovery anchor.
- The improvement is supported by a nearby core variant, reducing concern that the result is a one-off formula artifact.
- The candidate preserved the approved economic thesis and did not add prohibited hostile/stress-repair, liquidity-repair, participation-repair, production, governance, threshold, or ML elements.
- Stress-proxy redundancy remains low.
- h10 evidence is stronger and h20 evidence improved enough to justify formal validation review.

Limits of this classification:
- This is not validation execution.
- This is not validation success.
- This is not production eligibility.
- This is not a governance decision.
- This does not promote or demote the candidate.
- This does not modify thresholds or register the candidate anywhere.

Required validation-review focus if a later task is approved:
- Out-of-sample and walk-forward robustness.
- Active coverage and concentration.
- Regime/date concentration.
- Hostile/stress-repair contamination diagnostics.
- Redundancy against the full current alpha inventory, not only the refinement artifacts.
- Confirmation that the effect remains rank-persistence-driven rather than rebound-driven.

## SECTION 6 - Risk Assessment

Overfitting risk: medium.

The refinement was intentionally small and disciplined, which reduces parameter-mining risk. However, the candidate was selected after discovery and refined on the same research history, so formal validation is needed before treating the improvement as robust.

Refinement leakage risk: medium-low.

The variant was pre-specified inside the approved refinement design and did not involve broad horizon or threshold search. Leakage risk remains because the refinement decision used discovery evidence to choose the parent candidate.

Redundancy risk: mixed.

Redundancy with parent/sibling persistence variants is high by design and not a problem for lineage continuity. Redundancy versus stress proxies is low, which is favorable. Redundancy versus the full project inventory remains unresolved and should be included in validation review.

Family concentration risk: medium-high.

The persistence family evidence is concentrated in this one refined lineage. The broader family is not yet established by multiple independent candidates.

False diversification risk: medium.

The candidate looks distinct from hostile/stress-repair artifacts, but its drawdown/downtrend context means false diversification remains a real risk. Validation review must test whether it is truly rank persistence after drawdown rather than delayed stress repair.

## SECTION 7 - Recommendation

1. Has the persistence thread demonstrated meaningful progress?

Yes. The persistence thread moved from a promising discovery candidate to a stronger refined candidate with improved h10 and h20 evidence, coherent positive-rate behavior, and low stress-proxy redundancy.

2. Is the candidate validation-ready?

Yes, for formal validation review consideration. The classification is **READY FOR VALIDATION REVIEW**. This is a process-readiness conclusion only, not a validation result or governance action.

3. Is another refinement cycle warranted?

No, not before validation review. Another refinement cycle would increase overfitting and parameter-mining risk. The next step should test robustness, not continue tuning.

4. Should the persistence family remain an active research track?

Yes. Persistence should remain active, but the project should treat the current evidence as candidate-lineage strength rather than broad family proof. Future persistence work should emphasize distinct rank-stability mechanisms rather than more near-duplicates of the same post-drawdown construction.

5. What should the next Codex task be?

The next Codex task should be a research-only validation review design for `post_drawdown_persistence_churn_adjusted_20`. It should define validation scope, out-of-sample checks, walk-forward checks, active coverage diagnostics, stress-repair contamination diagnostics, and full-inventory redundancy checks. It should not execute validation, modify governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.

## Audit Caveat

This audit determines eligibility for formal validation review only. It does not execute validation, establish validation success, authorize production registration, alter governance, change thresholds, implement ML, or promote/demote any candidate.
