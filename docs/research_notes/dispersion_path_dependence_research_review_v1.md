# Project Underdog - Dispersion Path-Dependence Research Review v1

## SECTION 1 - Executive Summary

Classification: **RESEARCH_REVIEW_RECOMMEND_PARK**

Recommendation: **PARK_MODULE**

This note is an independent scientific review of the completed Dispersion Path-Dependence IC Discovery. It is review-only. No IC was recomputed, no panels were regenerated, no formulas were modified, no candidates were proposed, no refinement was performed, no validation was performed, no governance decision was made, and no production registry was changed.

Input classification:

`IC_DISCOVERY_COMPLETE_WITH_NOTES`

Reviewed materials:

- `docs/research_notes/dispersion_path_dependence_ic_discovery_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_mechanism_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_candidate_allocation_and_formula_planning_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_and_panel_specification_v1.md`
- Completed IC Discovery artifacts under `artifacts/research/dispersion_path_dependence_research_module_v1/ic_discovery_v1/`

Research review conclusion:

Dispersion Path-Dependence was a well-disciplined Platform v2 research module, but the first empirical evidence does not support advancing the module. The scientific concept remains coherent, yet the OHLCV-only implementation produced weak, horizon-inconsistent, or negative evidence across the four predeclared mechanisms. The best candidate, `dpath_01_relapse_resilience_after_calm`, showed limited h10 support but failed positive-rate and h20 durability checks. `dpath_03_elevated_disagreement_stabilization` had a constructive h5 result but failed the implemented h10 primary read. `dpath_02` and `dpath_04` were empirical mismatches.

The appropriate lifecycle outcome is to park the module and preserve the learning. This review does not authorize a second refinement cycle.

## SECTION 2 - Candidate Review

| candidate_id | IC Discovery recommendation | research-review conclusion |
| --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | PARK | Preserve as weak partial evidence; do not advance. |
| `dpath_02_disagreement_vol_stress_divergence` | REJECT | Empirically unsupported. |
| `dpath_03_elevated_disagreement_stabilization` | PARK | Preserve as h5-only diagnostic learning; do not advance. |
| `dpath_04_consensus_without_crowding` | REJECT | Empirically unsupported. |

### 2.1 `dpath_01_relapse_resilience_after_calm`

Hypothesis:

Securities resilient during renewed disagreement after temporary calm should carry positive medium-horizon information if disagreement memory matters.

Expected evidence:

Positive h10 primary evidence, h5 support, h20 durability only, and stable active coverage across multiple relapse episodes.

Observed evidence:

- h5 mean IC: 0.003713; IC IR: 0.029773; positive IC rate: 0.493976.
- h10 mean IC: 0.005919; IC IR: 0.043167; positive IC rate: 0.493976.
- h20 mean IC: -0.001747; IC IR: -0.012971; positive IC rate: 0.469880.
- Activation rate: 4.36%.
- Max internal diagnostic correlation: 0.082191 versus `low_churn_5`.

Hypothesis consistency: **PARTIAL_MATCH**

Strongest finding:

This was the only candidate with constructive h10 mean IC and IC IR, and it had the cleanest internal contamination read among the batch.

Weakest finding:

The positive IC rate stayed below 0.50 at h5 and h10, activation was below the originally expected "episodic but not rare" profile, and h20 durability was absent.

Scientific interpretation:

Relapse-after-calm is the most scientifically interesting mechanism in this batch. The result suggests that disagreement relapse may contain limited medium-horizon information, but not enough consistency to justify research-review advancement. The low contamination indicator is useful; the weak positive-rate profile is the blocker.

Recommendation:

Maintain **PARK**. Do not advance to governance or validation. Preserve as a possible future hypothesis-revision reference, not as an active refinement candidate.

### 2.2 `dpath_02_disagreement_vol_stress_divergence`

Hypothesis:

Cross-sectional disagreement path may add information when it diverges from volatility, VoV, or stress-state paths.

Expected evidence:

Positive h10 primary evidence with h5 support and lower contamination versus VoV and volatility compression than stabilization concepts.

Observed evidence:

- h1 mean IC: -0.003563; IC IR: -0.019158; positive IC rate: 0.500000.
- h5 mean IC: -0.014437; IC IR: -0.079044; positive IC rate: 0.444293.
- h10 mean IC: -0.022556; IC IR: -0.137782; positive IC rate: 0.414966.
- h20 mean IC: -0.023558; IC IR: -0.157030; positive IC rate: 0.418157.
- Activation rate: 38.82%.
- Max internal diagnostic correlation: 0.338411 versus `low_extension_20`.

Hypothesis consistency: **MISMATCH**

Strongest finding:

The candidate did activate broadly enough to be measurable, which means the negative result is informative rather than merely sparse.

Weakest finding:

All primary and secondary horizons were negative, with the worst behavior at h10/h20 where the hypothesis expected support.

Scientific interpretation:

The disagreement-versus-volatility/stress divergence idea did not translate into positive OHLCV-only evidence. The result suggests that the divergence construction may collapse into noise or into an indicator-engineering boundary rather than capturing a durable economic path concept.

Recommendation:

Maintain **REJECT**. Treat this as a falsified first-batch implementation of the divergence mechanism.

### 2.3 `dpath_03_elevated_disagreement_stabilization`

Hypothesis:

Securities that remain orderly while disagreement is elevated but stabilizing should benefit from orderly repricing.

Expected evidence:

Positive h10 primary evidence, h5 support, and no h20-only rescue.

Observed evidence:

- h1 mean IC: -0.009583; IC IR: -0.052702; positive IC rate: 0.462687.
- h5 mean IC: 0.008365; IC IR: 0.048794; positive IC rate: 0.541353.
- h10 mean IC: -0.009952; IC IR: -0.061098; positive IC rate: 0.469697.
- h20 mean IC: -0.016816; IC IR: -0.108689; positive IC rate: 0.507812.
- Activation rate: 7.10%.
- Max internal diagnostic correlation: 0.127906 versus `low_extension_20`.

Hypothesis consistency: **PARTIAL_MATCH**

Strongest finding:

The h5 result was the strongest single positive discovery result in the module and aligned with the lower end of the expected h5/h10 horizon band.

Weakest finding:

The h10 primary result was negative, h20 was negative, and the pattern looks like a short-lived h5 effect rather than the planned medium-horizon stabilization mechanism.

Scientific interpretation:

Elevated stabilization may contain short-horizon information, but this first batch does not support the primary h10 mechanism. The h5 result is scientifically useful because it narrows where any effect might live, but it is not enough to justify refinement under this lifecycle.

Recommendation:

Maintain **PARK**. Preserve the result as diagnostic evidence that elevated stabilization may be short-horizon and underpowered in this formulation.

### 2.4 `dpath_04_consensus_without_crowding`

Hypothesis:

Orderly disagreement normalization may identify emerging consensus if it avoids mature leadership crowding.

Expected evidence:

Positive h10 primary evidence, h5 support, and separation from parked non-hostile transition and rank persistence.

Observed evidence:

- h1 mean IC: -0.011720; IC IR: -0.068164; positive IC rate: 0.464646.
- h5 mean IC: -0.009601; IC IR: -0.055226; positive IC rate: 0.515152.
- h10 mean IC: -0.008041; IC IR: -0.048668; positive IC rate: 0.481481.
- h20 mean IC: -0.025330; IC IR: -0.163569; positive IC rate: 0.456081.
- Activation rate: 15.58%.
- Max internal diagnostic correlation: 0.176567 versus `low_extension_20`.

Hypothesis consistency: **MISMATCH**

Strongest finding:

The candidate had a reasonable activation rate and measurable coverage, so the mismatch is interpretable.

Weakest finding:

Mean IC was negative across every evaluated horizon, including h10 and h20.

Scientific interpretation:

The consensus-without-crowding hypothesis did not generalize in this implementation. The result suggests that orderly disagreement normalization may not be enough to identify emerging consensus in OHLCV-only data, or that the anti-crowding controls remove the very exposure needed for positive forward evidence.

Recommendation:

Maintain **REJECT**. Do not revive through immediate formula adjustment.

## SECTION 3 - Mechanism Review

| mechanism | evidence status | conclusion |
| --- | --- | --- |
| Relapse Resilience | partially supported but weak | Scientifically interesting but underpowered. |
| Disagreement Path Divergence | unsupported | Clearly contradicted in this implementation. |
| Elevated Stabilization | partially supported at h5 only | Scientifically interesting but horizon-inconsistent. |
| Consensus Formation Without Crowding | unsupported | Clearly contradicted in this implementation. |

Relapse Resilience:

This remains the strongest mechanism concept in the batch. It was the cleanest path-dependent idea before implementation and produced the only positive h10 candidate read. However, activation was sparse, positive IC rate was weak, and durability failed. The mechanism is not validated and should not advance, but it produced a meaningful negative/partial learning: relapse may be real but too weak or too conditional in OHLCV-only form.

Disagreement Path Divergence:

This was expected to be the highest-orthogonality test. Empirically it failed. The broad activation rate means the result was not simply starved of observations. The mechanism appears unsupported and potentially contradicted by the completed IC evidence.

Elevated Stabilization:

The h5 result keeps the mechanism scientifically interesting, but the h10 failure is decisive under the frozen expectations. This mechanism may capture a short-lived stabilization response, not a stable h5/h10 path-dependence effect.

Consensus Formation Without Crowding:

The mechanism is unsupported. It was contamination-prone in the original mechanism review, and the empirical evidence did not compensate for that risk. The review does not find a basis to keep this as an active research thread.

## SECTION 4 - Scientific Learning

The central learning is that Dispersion Path-Dependence is scientifically coherent but empirically weak in this OHLCV-only first batch.

Project Underdog learned:

- Path dependence may be harder to extract from OHLCV-only dispersion features than the prior scientific rationale suggested.
- The market's recent disagreement path did not broadly translate into positive h5/h10 cross-sectional IC.
- Relapse-after-calm contains the most credible weak evidence, but the effect was not broad or consistent enough to promote.
- Elevated disagreement stabilization may contain short-horizon h5 information, but the failure at h10 argues against the intended medium-horizon mechanism.
- Disagreement divergence from volatility/stress did not behave like a useful orthogonal mechanism; it may collapse into noisy indicator separation.
- Consensus formation without crowding did not generalize; anti-crowding and normalization logic did not produce positive forward evidence.
- Negative h20 behavior across the family is informative. The module did not find durability evidence, and h20 should not be used to rescue the family.
- The contamination-control discipline was useful even where alpha evidence was poor. It clarified that weak performance was not merely hidden by uncontrolled rank-churn contamination in `dpath_01`.

The negative evidence is valuable. It narrows the research frontier by showing that not every conceptually distinct market-state path deserves active candidate development.

## SECTION 5 - Platform v2 Assessment

Platform v2 improved research quality in this module.

Hypothesis discipline:

The module began with frozen scientific questions, predeclared horizons, expected activation behavior, contamination risks, stop conditions, and candidate limits. This prevented h20 rescue, candidate expansion, and post-hoc reinterpretation.

Orthogonality evaluation:

The research process forced each mechanism to explain how it differed from static dispersion, VoV, volatility compression, hostile/stress repair, rank coherence, persistence, volume shock reversal, and parked non-hostile transition. That made the eventual negative evidence cleaner.

Contamination control:

The IC Discovery preserved internal diagnostic indicators and contamination metadata. The review could distinguish weak but cleaner evidence in `dpath_01` from broader mismatches in `dpath_02` and `dpath_04`.

Scientific traceability:

Every candidate retained hypothesis, scientific question, expected evidence, mechanism family, activation text, formula text, and comparator metadata. This made the review about scientific learning rather than winner selection.

Prevention of unnecessary refinement:

Platform v2 did its job. A less disciplined process might chase the h5 result in `dpath_03` or the h10 mean IC in `dpath_01`. Under the frozen standards, neither result is strong enough to justify refinement.

## SECTION 6 - Future Recommendation

Recommendation: **PARK_MODULE**

Scientific justification:

The module expanded Project Underdog's scientific understanding, but it did not produce enough empirical support to advance. Two candidates were rejected, two were parked, no candidate advanced to research review by IC Discovery standards, and family-level h10/h20 evidence was negative.

This is not a recommendation to discard the idea permanently. It is a recommendation to stop the current lifecycle path here. Any future return to dispersion path-dependence should be framed as a new hypothesis-revision effort, not as a second refinement cycle of this batch.

Not authorized:

- No second refinement cycle.
- No new formulas.
- No new candidates.
- No validation.
- No governance decision.
- No production registration.

Recommended next lifecycle phase:

**Project Underdog - Dispersion Path-Dependence Governance Review v1**, review-only, to record the park decision formally. The governance review should not reverse this research conclusion without new evidence.

## SECTION 7 - Verification

Confirmed for this research-review phase:

- No implementation files changed.
- No formulas changed.
- No panel regeneration was performed.
- No IC recomputation was performed.
- No refinement was performed.
- No validation was performed.
- No governance mutation was performed.
- No production registry changes were made.
- No threshold changes were made.
- No ML work was performed.

Only this review note was created:

`docs/research_notes/dispersion_path_dependence_research_review_v1.md`

## SECTION 8 - Final Classification

Classification: **RESEARCH_REVIEW_RECOMMEND_PARK**

Final recommendation: **PARK_MODULE**

Dispersion Path-Dependence remains a useful scientific negative result. It should be archived as Platform v2 evidence that a coherent, traceable, contamination-aware module can still fail empirically, and that failure can improve the research map without consuming a refinement cycle.
