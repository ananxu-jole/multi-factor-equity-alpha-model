# Project Underdog - Rank-Coherence Refinement Execution v1

## SECTION 1 - Executive Summary

The rank-coherence refinement execution completed as a research-only refinement pass using the approved scope from `rank_coherence_refinement_eligibility_and_design_v1.md`. The batch contained exactly six candidates: two preserved discovery anchors and four predeclared refinement variants. No validation, governance mutation, threshold change, production registration, ML integration, or candidate promotion/demotion was performed.

Refinement scope:

- Approved parent candidates: `rank_coherence_regime_independent_02` and `rank_coherence_churn_avoidance_02`.
- Anchor count: 2.
- New variant count: 4.
- Total candidate count: 6.
- Horizons evaluated: h1, h5, h10, h20.
- Artifact root: `artifacts/research/rank_coherence_refinement_v1/`.

The strongest candidate family thread was `rank_coherence_churn_avoidance_02`. The strongest refinement variant was `rank_coherence_churn_avoidance_02_overlap_adjusted` (`relative_rank_turnover_resilience_overlap_adjusted_20`), which improved h10 and h20 mean IC, IC IR, and positive IC rate versus the discovery anchor while reducing measured persistence correlation from the anchor's 0.2378 maximum to 0.1701.

Overall outcome: refinement improved the candidate-level evidence for rank-coherence, especially through the churn-avoidance overlap-adjusted variant. Evidence is stronger than the discovery pass but remains candidate-level rather than broad family-level proof.

## SECTION 2 - Candidate Results

| candidate_id | role | h1 mean IC / IR / pos | h5 mean IC / IR / pos | h10 mean IC / IR / pos | h20 mean IC / IR / pos |
| --- | --- | --- | --- | --- | --- |
| `rank_coherence_regime_independent_02_anchor` | original anchor | 0.001605 / 0.012391 / 0.497018 | 0.011849 / 0.091804 / 0.553106 | 0.008151 / 0.060306 / 0.520243 | 0.010040 / 0.075927 / 0.526860 |
| `rank_coherence_regime_independent_02_strict` | stricter non-hostile transition | 0.000393 / 0.002749 / 0.502982 | 0.010585 / 0.075502 / 0.555110 | 0.007143 / 0.048817 / 0.532389 | 0.010008 / 0.069597 / 0.528926 |
| `rank_coherence_regime_independent_02_smoothed` | light smoothing | 0.004478 / 0.033143 / 0.512974 | 0.008488 / 0.061486 / 0.507042 | 0.006276 / 0.045238 / 0.520325 | 0.008320 / 0.061602 / 0.508299 |
| `rank_coherence_churn_avoidance_02_anchor` | original anchor | 0.002049 / 0.010219 / 0.510934 | 0.005683 / 0.030090 / 0.545090 | 0.003643 / 0.019919 / 0.522267 | 0.011587 / 0.064884 / 0.549587 |
| `rank_coherence_churn_avoidance_02_penalized` | conservative churn penalty | 0.002016 / 0.010070 / 0.508946 | 0.005807 / 0.030829 / 0.549098 | 0.003873 / 0.021232 / 0.522267 | 0.011947 / 0.067018 / 0.551653 |
| `rank_coherence_churn_avoidance_02_overlap_adjusted` | overlap diagnostic | 0.002811 / 0.014015 / 0.514911 | 0.005968 / 0.031813 / 0.537074 | 0.004783 / 0.026354 / 0.532389 | 0.012843 / 0.072299 / 0.561983 |

Candidate-level interpretation:

- `rank_coherence_churn_avoidance_02_overlap_adjusted` was the strongest refined result. It improved the h20 mean IC to 0.012843, h20 IC IR to 0.072299, and h20 positive IC rate to 0.561983. It also improved h10 mean IC from 0.003643 to 0.004783.
- `rank_coherence_churn_avoidance_02_penalized` improved the anchor modestly at h5, h10, and h20, but remained nearly identical to the anchor in redundancy terms.
- `rank_coherence_churn_avoidance_02_anchor` remained a useful baseline with the strongest original h20 discovery result.
- `rank_coherence_regime_independent_02_anchor` remained robust across h5/h10/h20, but the refinement variants did not clearly improve it.
- `rank_coherence_regime_independent_02_strict` preserved h20 but weakened h10 and IC IR versus the anchor.
- `rank_coherence_regime_independent_02_smoothed` improved h1 but weakened h5/h10/h20 and reduced positive IC rate at h20.

## SECTION 3 - Refinement Assessment

Refinement deltas versus discovery anchors:

| candidate_id | h10 mean IC delta | h10 IR delta | h10 pos-rate delta | h20 mean IC delta | h20 IR delta | h20 pos-rate delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `rank_coherence_regime_independent_02_strict` | -0.001009 | -0.011489 | 0.012146 | -0.000033 | -0.006330 | 0.002066 |
| `rank_coherence_regime_independent_02_smoothed` | -0.001875 | -0.015068 | 0.000082 | -0.001720 | -0.014324 | -0.018561 |
| `rank_coherence_churn_avoidance_02_penalized` | 0.000229 | 0.001313 | 0.000000 | 0.000360 | 0.002134 | 0.002066 |
| `rank_coherence_churn_avoidance_02_overlap_adjusted` | 0.001140 | 0.006435 | 0.010121 | 0.001255 | 0.007415 | 0.012397 |

Improvement versus anchor:

The churn-avoidance branch improved. The overlap-adjusted variant was the only candidate that produced a meaningful h10/h20 improvement while also reducing persistence redundancy. The penalized variant showed smaller positive deltas but was almost a duplicate of the anchor.

The regime-independent branch did not improve. The strict variant preserved the broad h10/h20 shape but weakened mean IC and IC IR. The smoothed variant increased h1 behavior but reduced primary-horizon evidence.

Robustness versus anchor:

The strongest robustness profile belongs to `rank_coherence_churn_avoidance_02_overlap_adjusted`, which was positive across h1/h5/h10/h20 and strongest at h20. The family-level h20 mean IC across the six-candidate refinement batch was 0.010791, with mean positive IC rate of 0.537885. The h10 family mean IC was 0.005645, with mean positive IC rate of 0.524980.

Horizon concentration risk:

Horizon concentration remains present. The best evidence is still h20-led, especially in the churn-avoidance branch. However, the overlap-adjusted variant improved h10 as well as h20, which reduces the concern that the result is only a single-horizon artifact.

Overfitting concerns:

The refinement was intentionally small and predeclared, limiting parameter-mining risk. The largest overfitting concern is not batch size, but redundancy: several variants are highly correlated with their anchors or sibling variants. The penalized churn variant had maximum refinement correlation of 0.9984, making it mostly diagnostic. The overlap-adjusted churn variant was also related to the anchor at 0.9234, but it produced the cleanest improvement and reduced persistence correlation.

## SECTION 4 - Family Assessment

1. Does rank-coherence remain distinct from persistence?

Partially. The churn-avoidance overlap-adjusted variant improved the persistence contamination profile, with maximum persistence correlation of 0.1701 versus 0.2378 for the churn anchor. This supports the case that the best refined churn candidate is not merely post-drawdown persistence. The regime-independent branch is more concerning: its anchor had maximum persistence correlation of 0.6381, the smoothed variant 0.6536, and the strict variant 0.6026. Those values are too high for a clean validation-readiness claim.

2. Does rank-coherence remain distinct from hostile/stress-repair?

Yes, with caveats. The strongest churn refinement had maximum stress-proxy correlation of 0.3940, lower than the churn anchor's 0.4122. The regime-independent variants had lower stress-proxy correlations, ranging from 0.2701 to 0.3118. No artifact indicates validation execution or stress-repair state attribution, so this remains a refinement-stage contamination review rather than a formal validation result.

3. Is evidence becoming family-level or still candidate-level?

Evidence remains candidate-level. The six-candidate refinement batch has positive family summaries across h1/h5/h10/h20, but the batch consists only of two anchors and four close variants. That is not enough breadth to claim family-level validation evidence.

4. Does rank-coherence remain a credible diversification frontier?

Yes. The churn-avoidance overlap-adjusted result gives rank-coherence a serious candidate-level path forward. The broader family remains immature, and the regime-independent branch should not be treated as independently validation-ready without more separation from persistence.

Redundancy and contamination review:

| candidate_id | max refinement corr | max persistence corr | max dispersion corr | max stress-proxy corr | interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `rank_coherence_churn_avoidance_02_anchor` | 0.9984 | 0.2378 | 0.2352 | 0.4122 | Useful anchor, but sibling duplicate risk is high. |
| `rank_coherence_churn_avoidance_02_penalized` | 0.9984 | 0.2372 | 0.2364 | 0.4125 | Diagnostic variant; too close to anchor. |
| `rank_coherence_churn_avoidance_02_overlap_adjusted` | 0.9234 | 0.1701 | 0.2260 | 0.3940 | Best distinctiveness profile among refined candidates. |
| `rank_coherence_regime_independent_02_anchor` | 0.9590 | 0.6381 | 0.2550 | 0.2727 | Strong IC profile but persistence contamination risk is high. |
| `rank_coherence_regime_independent_02_strict` | 0.9590 | 0.6026 | 0.2795 | 0.3118 | Preserves h20 but still persistence-adjacent. |
| `rank_coherence_regime_independent_02_smoothed` | 0.8256 | 0.6536 | 0.2519 | 0.2701 | Lower sibling redundancy but weaker primary-horizon performance and high persistence correlation. |

## SECTION 5 - Validation Eligibility Review

| candidate_id | classification | rationale |
| --- | --- | --- |
| `rank_coherence_churn_avoidance_02_overlap_adjusted` | ready for validation review | Strongest refined candidate. Improved h10/h20 mean IC, IC IR, and positive IC rate versus the discovery anchor while reducing persistence and stress-proxy correlations. |
| `rank_coherence_churn_avoidance_02_anchor` | watchlist only | Original anchor remains useful, but the overlap-adjusted variant supersedes it for validation-review consideration. |
| `rank_coherence_churn_avoidance_02_penalized` | diagnostic only | Small improvements, but extremely high redundancy with the anchor makes it a diagnostic sensitivity check rather than a candidate for validation review. |
| `rank_coherence_regime_independent_02_anchor` | watchlist only | IC profile remains useful, but persistence correlation is too high for clean validation-review eligibility. |
| `rank_coherence_regime_independent_02_strict` | diagnostic only | Preserves some h20 behavior but does not improve the anchor and remains persistence-adjacent. |
| `rank_coherence_regime_independent_02_smoothed` | diagnostic only | Weakens h5/h10/h20 versus anchor and retains high persistence correlation. |

Validation should not be executed from this note. The appropriate next step is a review-only validation eligibility audit for `rank_coherence_churn_avoidance_02_overlap_adjusted`.

## SECTION 6 - Final Recommendation

1. Did refinement improve the family?

Yes, but narrowly. Refinement improved the rank-coherence evidence through the churn-avoidance overlap-adjusted variant. It did not establish broad family-level proof.

2. Which candidate is strongest?

`rank_coherence_churn_avoidance_02_overlap_adjusted` is the strongest candidate. It had h20 mean IC of 0.012843, h20 IC IR of 0.072299, and h20 positive IC rate of 0.561983, with positive h10 improvement versus the discovery anchor.

3. Is validation review justified?

Yes, for one candidate only: `rank_coherence_churn_avoidance_02_overlap_adjusted`. The recommendation is validation-review eligibility audit, not validation execution.

4. Has rank-coherence become a serious alpha-family contender?

Yes. Rank-coherence has become a serious candidate-level alpha-family contender, but it has not yet matured into a validated family. Its best evidence is concentrated in one refined churn-avoidance candidate.

5. What should the next Codex task be?

The next task should be **Project Underdog - Rank-Coherence Validation Eligibility Audit v1**. It should review `rank_coherence_churn_avoidance_02_overlap_adjusted` against the refinement artifacts, discovery lineage, persistence redundancy context, hostile/stress-repair contamination context, and existing validation-readiness standards. It should be review-only and should not run validation, modify governance, change thresholds, register production candidates, implement ML, or promote/demote candidates.
