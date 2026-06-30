# Project Underdog - Rank-Coherence Validation Eligibility Audit v1

Date: 2026-06-19

Project: Project Underdog

Primary candidate: `rank_coherence_churn_avoidance_02_overlap_adjusted`

Representative signal: `relative_rank_turnover_resilience_overlap_adjusted_20`

Origin:
- Discovery parent: `rank_coherence_churn_avoidance_02`
- Discovery representative: `relative_rank_turnover_resilience_20`
- Family: Rank-Coherence
- Theme: Rank Churn Avoidance

Scope: review-only validation eligibility audit. No validation, additional refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Refinement improved the primary rank-coherence candidate in a meaningful but still research-stage way. The original discovery anchor, `rank_coherence_churn_avoidance_02` / `relative_rank_turnover_resilience_20`, was already the strongest h20 rank-coherence discovery candidate, with h20 mean IC 0.011587, h20 IC IR 0.064884, and h20 positive IC rate 0.549587.

The refined successor, `rank_coherence_churn_avoidance_02_overlap_adjusted` / `relative_rank_turnover_resilience_overlap_adjusted_20`, improved the primary h10/h20 evidence:

- h10 mean IC improved from 0.003643 to 0.004783.
- h10 IC IR improved from 0.019919 to 0.026354.
- h10 positive IC rate improved from 0.522267 to 0.532389.
- h20 mean IC improved from 0.011587 to 0.012843.
- h20 IC IR improved from 0.064884 to 0.072299.
- h20 positive IC rate improved from 0.549587 to 0.561983.

The improvement is meaningful because it occurred in the approved narrow refinement space, preserved the rank-turnover-resilience hypothesis, improved both primary horizons, and reduced measured persistence correlation from 0.2378 for the anchor to 0.1701 for the refined candidate.

The evidence remains candidate-level rather than family-level. The six-candidate refinement batch had positive family summaries across h1/h5/h10/h20, but the batch consisted only of two anchors and four close variants. This is not enough breadth to claim that rank-coherence is a validated or broadly established alpha family.

Validation consideration is justified. The correct classification is **READY FOR VALIDATION REVIEW** as a research process status. This does not mean validated, production-ready, governance-approved, threshold-qualified, promoted, or registered.

## SECTION 2 - Research Lineage Review

The research lineage is clean and auditable.

Original discovery candidate:

- Candidate: `rank_coherence_churn_avoidance_02`
- Signal: `relative_rank_turnover_resilience_20`
- Theme: Rank Churn Avoidance
- Discovery thesis: securities with rank turnover below universe rank turnover may retain more durable sponsorship.

IC discovery results for the original representative:

| horizon | mean IC | IC IR | positive IC rate |
| --- | ---: | ---: | ---: |
| h1 | 0.002049 | 0.010219 | 0.510934 |
| h5 | 0.005683 | 0.030090 | 0.545090 |
| h10 | 0.003643 | 0.019919 | 0.522267 |
| h20 | 0.011587 | 0.064884 | 0.549587 |

Discovery interpretation:

The discovery pass found useful candidate-level evidence. `rank_coherence_churn_avoidance_02` was positive across h1/h5/h10/h20 and was the strongest h20 candidate in the scored subset. The main unresolved issue was persistence-duplication risk because rank-turnover resilience is conceptually adjacent to persistence.

Refinement design:

The refinement design approved a deliberately small program: two eligible candidates, two preserved anchors, and at most four variants. For the churn-avoidance branch, allowable changes were limited to slight rank-turnover measurement adjustment, conservative churn-penalty adjustment, and one diagnostic variant to reduce overlap with regime-independent rank coherence. The design prohibited post-drawdown persistence inputs, hostile/stress-repair inputs, participation repair, dispersion ingredients, horizon expansion, ML, governance mutation, production registration, and candidate promotion/demotion.

Refinement execution:

The execution produced six total candidates:

- `rank_coherence_regime_independent_02_anchor`
- `rank_coherence_regime_independent_02_strict`
- `rank_coherence_regime_independent_02_smoothed`
- `rank_coherence_churn_avoidance_02_anchor`
- `rank_coherence_churn_avoidance_02_penalized`
- `rank_coherence_churn_avoidance_02_overlap_adjusted`

The strongest refined candidate was `rank_coherence_churn_avoidance_02_overlap_adjusted`. It preserved the rank-coherence family, the rank-churn theme, and the h10-h20 orientation while improving the anchor's h10/h20 evidence and reducing persistence redundancy.

Lineage assessment:

- Clean: yes. The candidate traces directly from discovery to approved refinement design to research-only refinement execution.
- Auditable: yes. The relevant artifacts are present under `artifacts/research/rank_coherence_refinement_v1/`.
- Scope disciplined: yes. The refinement stayed within the approved six-candidate maximum and did not introduce additional families, themes, horizons, governance changes, production paths, or ML.
- Remaining caveat: the refined candidate is still a close sibling of its anchor, with maximum refinement correlation of 0.9234. That is acceptable for lineage continuity, but it means validation must test robustness rather than treat the refinement result as independent confirmation.

## SECTION 3 - Core Evidence Review

Primary candidate metrics:

| horizon | mean IC | IC IR | positive IC rate |
| --- | ---: | ---: | ---: |
| h1 | 0.002811 | 0.014015 | 0.514911 |
| h5 | 0.005968 | 0.031813 | 0.537074 |
| h10 | 0.004783 | 0.026354 | 0.532389 |
| h20 | 0.012843 | 0.072299 | 0.561983 |

h10 evidence:

The h10 result is positive and improved versus the discovery anchor. Mean IC improved by 0.001140, IC IR improved by 0.006435, and positive IC rate improved by 0.010121. The h10 evidence remains more modest than h20, but it is directionally supportive and reduces concern that the candidate is purely h20-specific.

h20 evidence:

The h20 result is the strongest point in the candidate's evidence profile. Mean IC improved by 0.001255, IC IR improved by 0.007415, and positive IC rate improved by 0.012397 versus the discovery anchor. The refined h20 positive IC rate of 0.561983 is the best primary-horizon positive-rate result in the rank-coherence refinement set.

Horizon consistency:

The candidate is positive across h1/h5/h10/h20. The effect remains h20-led, but h10 improved alongside h20. That pattern is consistent with a medium-horizon rank-turnover-resilience signal rather than a one-horizon artifact. h5 is supportive but not the primary success basis.

Improvement versus anchor:

| horizon | mean IC delta | IC IR delta | positive IC rate delta |
| --- | ---: | ---: | ---: |
| h1 | 0.000762 | 0.003797 | 0.003976 |
| h5 | 0.000285 | 0.001723 | -0.008016 |
| h10 | 0.001140 | 0.006435 | 0.010121 |
| h20 | 0.001255 | 0.007415 | 0.012397 |

Refinement delta quality:

The delta quality is good enough for validation-review eligibility. The primary h10/h20 deltas are positive across mean IC, IC IR, and positive IC rate. The only negative delta is h5 positive IC rate, which is not the primary interpretation horizon and is offset by higher h5 mean IC and IC IR. The improvement is not dramatic, but it is coherent, predeclared, and aligned with the refinement objective.

Coverage:

The candidate had 504 active signal dates, active date ratio of 0.240229, mean active tickers of 459.68, minimum active tickers of 290, and maximum active tickers of 462. Coverage was sufficient for research-stage eligibility review. Validation should still test active coverage and concentration out of sample.

## SECTION 4 - Distinctiveness and Contamination Review

Persistence correlation:

The refined candidate's maximum persistence correlation was 0.1701, with `post_drawdown_persistence_smoothed_20` as the top persistence peer. This is lower than the anchor's maximum persistence correlation of 0.2378. The reduction is important because persistence duplication was the primary risk for rank-churn candidates.

Stress-repair correlation:

The maximum stress-proxy correlation was 0.3940, with `failed_breakout_reversal_20` as the top stress proxy. This is lower than the anchor's 0.4122 but still high enough that validation must include formal state attribution and stress-repair contamination diagnostics. At the refinement-review level, the candidate does not appear to be a direct hostile/stress-repair recreation.

Dispersion correlation:

The maximum dispersion correlation was 0.2260, with `dispersion_transition_acceleration_neutralized_20` as the top dispersion peer. This supports the view that the candidate is not a renamed dispersion signal.

Sibling and anchor redundancy:

The maximum refinement correlation was 0.9234 versus `relative_rank_turnover_resilience_20`, the original churn-avoidance anchor. This means the refined candidate remains close to its parent lineage. That is not disqualifying because the task was refinement, not independent family discovery, but it does limit the evidentiary breadth. The improvement should be treated as a cleaner successor to the anchor, not as independent corroboration.

Rank-coherence versus renamed persistence/stress-repair:

The candidate appears to be a true rank-coherence refinement candidate rather than a renamed persistence variant. The economic mechanism remains rank turnover resilience and overlap adjustment, not post-drawdown persistence or stress repair. The reduced persistence correlation supports this reading. The stress-proxy correlation is moderate, so validation must test whether the signal activates disproportionately during hostile/stress-repair states.

Distinctiveness conclusion:

Distinctiveness is sufficient for validation-review eligibility, but not sufficient for validation success. The candidate has earned formal validation-design consideration, where the major question should be whether the apparent rank-coherence behavior survives out-of-sample, walk-forward, state, and redundancy checks.

## SECTION 5 - Risk Assessment

Overfitting risk: medium.

The refinement program was small, predeclared, and limited to two anchors plus four variants, which reduces parameter-mining risk. However, the candidate was selected after discovery and refined on the same research history, so overfitting remains a material risk until formal validation tests out-of-sample and walk-forward behavior.

Refinement leakage risk: medium-low.

The overlap-adjusted variant was permitted by the design and did not emerge from a broad post-hoc search. Leakage risk remains because the parent candidate and refinement objective were chosen based on discovery evidence.

Horizon chasing risk: medium.

The candidate is h20-led, and the original discovery anchor was selected partly because of h20 strength. The risk is moderated by positive h10 improvement, positive h1/h5 behavior, and improvement in h10/h20 positive IC rates. Validation must test whether h20 strength survives without tuning.

Family concentration risk: medium-high.

The current rank-coherence evidence is concentrated in one refined churn-avoidance candidate. The regime-independent branch had useful IC behavior but unresolved persistence correlation, and other themes were weak, mixed, or rejected. Rank-coherence is a serious candidate-level contender, not yet a broad family.

False diversification risk: medium.

The candidate has lower persistence correlation than the anchor and no direct post-drawdown framing, but rank churn is economically adjacent to persistence. The stress-proxy correlation is also not negligible. Validation must test whether the signal truly represents rank-coherence rather than delayed persistence, rebound, or stress-repair exposure.

Candidate-level-only evidence risk: medium-high.

The refinement batch improved family summaries, but the family summary is composed of close variants, not independent themes. Validation should evaluate this candidate as a single refined lineage and avoid treating sibling variants as separate family breadth.

## SECTION 6 - Validation Readiness Classification

Classification: **READY FOR VALIDATION REVIEW**

Reasoning:

- The candidate improved h10 and h20 mean IC, IC IR, and positive IC rate versus the discovery anchor.
- The improvement occurred inside the approved narrow refinement design.
- The candidate preserved the rank-coherence family and rank-churn hypothesis.
- Persistence correlation decreased materially versus the anchor.
- Dispersion correlation remained low-to-moderate.
- Stress-proxy correlation improved modestly versus the anchor, though formal stress diagnostics remain required.
- Evidence is strong enough to justify validation-design work, but not validation success or governance action.

Limits of this classification:

- This audit does not execute validation.
- This audit does not establish validation pass.
- This audit does not modify governance.
- This audit does not change thresholds.
- This audit does not register the candidate to production.
- This audit does not implement ML.
- This audit does not promote or demote any candidate.

Required validation-review focus if a later design task is approved:

- Walk-forward behavior and out-of-sample robustness.
- h10/h20 durability without horizon selection.
- Active coverage and window concentration.
- State attribution and hostile/stress-repair contamination.
- Redundancy against persistence, hostile/stress-repair, dispersion, and the full active research inventory.
- Confirmation that rank-turnover resilience is the actual mechanism.

## SECTION 7 - Recommendation

1. Has rank-coherence produced meaningful refinement evidence?

Yes. Rank-coherence produced meaningful candidate-level refinement evidence through `rank_coherence_churn_avoidance_02_overlap_adjusted`. The evidence improved versus the discovery anchor and reduced the major persistence-duplication concern.

2. Is `rank_coherence_churn_avoidance_02_overlap_adjusted` ready for validation review?

Yes. It is **READY FOR VALIDATION REVIEW** as a process-readiness classification. It should not be treated as validated, promoted, governance-approved, threshold-qualified, or production-ready.

3. Is the evidence strong enough to treat rank-coherence as a serious alpha-family contender?

Yes, but only as a serious candidate-level contender. Rank-coherence has not yet established broad family-level evidence. Its best current path is one refined churn-avoidance lineage.

4. What risks must validation test?

Validation must test overfitting, h20 horizon concentration, walk-forward stability, active coverage, window concentration, persistence duplication, stress-repair contamination, dispersion overlap, and false diversification risk.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Rank-Coherence Validation Design v1**. It should design a disciplined formal validation program for `rank_coherence_churn_avoidance_02_overlap_adjusted`, including walk-forward validation, horizon review, active coverage diagnostics, window concentration review, state attribution, redundancy review, and stress-repair contamination checks. It should not execute validation, modify governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.

## Audit Caveat

This audit determines eligibility for formal validation review only. It does not execute validation, establish validation success, authorize production registration, alter governance, change thresholds, implement ML, or promote/demote any candidate.
