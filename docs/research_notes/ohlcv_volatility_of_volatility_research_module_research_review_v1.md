# Project Underdog - OHLCV Volatility-of-Volatility Research Module Research Review v1

## SECTION 1 - Review Objective

This note executes Phase 9 - Research Review for the OHLCV Volatility-of-Volatility research module.

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_ic_discovery_v1.md`
- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/ic_discovery_v1/`

Input classification:

- `IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`

Research review classification:

- `REFINEMENT_APPROVED`

This review did not perform refinement, regenerate panels, recompute IC, run validation, mutate governance, change production files, change thresholds, or introduce ML.

## SECTION 2 - Review Conclusion

Refinement is scientifically justified for a narrow subset of the VoV module:

- `vov_01` - approve for refinement design.
- `vov_03` - approve for refinement design.

The module should not advance as a broad family claim. The evidence is constructive but candidate-concentrated. `vov_05` has strong mean IC evidence but a weaker positive-rate profile and should remain `WATCH`. `vov_02` and `vov_04` should be rejected from the active refinement path.

The appropriate Phase 10 governance outcome should be:

- `ADVANCE` for `vov_01` and `vov_03`.
- `WATCH` for `vov_05`.
- `PARK` for `vov_02` and `vov_04`.
- Module-level outcome: bounded refinement design approved for two candidates only.

## SECTION 3 - Candidate Interpretations

| candidate_id | IC discovery recommendation | research review outcome | interpretation |
| --- | --- | --- | --- |
| `vov_01` | `ADVANCE_TO_REFINEMENT` | `ADVANCE` | Cleanest h20 profile. Positive h10/h20 evidence, h20 mean IC 0.010405, h20 IC IR 0.093197, h20 positive IC rate 0.535383, and supportive rolling h20 evidence. |
| `vov_03` | `ADVANCE_TO_REFINEMENT` | `ADVANCE` | Strongest h10 positive-rate profile. Positive h5/h10/h20 shape, h10 mean IC 0.008204, h10 IC IR 0.074103, h10 positive IC rate 0.546996, and supportive rolling h10/h20 behavior. |
| `vov_05` | `WATCH` | `WATCH` | Strongest h20 mean IC and IC IR, but weaker positive IC rate. Interesting candidate, but not clean enough for immediate refinement. |
| `vov_02` | `REJECT` | `PARK` | Mild h1 behavior does not survive h10/h20. Medium-horizon mean IC is negative. |
| `vov_04` | `REJECT` | `PARK` | Negative h5/h10/h20 evidence and adverse rolling medium-horizon behavior. |

## SECTION 4 - Horizon-Level Behavior

Family-level horizon summary:

| horizon | candidate count | family mean IC | mean positive IC rate | mean coverage ratio |
| --- | ---: | ---: | ---: | ---: |
| h1 | 5 | 0.002264 | 0.506899 | 0.631681 |
| h5 | 5 | 0.003089 | 0.510586 | 0.618416 |
| h10 | 5 | 0.002925 | 0.514388 | 0.606000 |
| h20 | 5 | 0.002668 | 0.505411 | 0.588206 |

Interpretation:

- The family-level signal is positive across all horizons, but modest.
- h5 has the highest family mean IC, but h10/h20 remain positive and are the governing review horizons.
- The primary-horizon evidence is not evenly distributed. It is concentrated in `vov_01`, `vov_03`, and `vov_05`.
- h1 behavior is not central to the decision and does not rescue `vov_02` or `vov_04`.

## SECTION 5 - Family-Level Behavior

The VoV module produced enough evidence to justify a refinement design, but not enough to declare broad family-level proof.

Strengths:

- Positive family mean IC across h1/h5/h10/h20.
- Two candidates clear conservative primary-horizon advance criteria.
- The best candidates have interpretable mechanism identities.
- Rolling diagnostics support the two candidates selected for refinement design.

Weaknesses:

- Two of five candidates are clear rejects.
- The family mean IC is modest because candidate outcomes are mixed.
- `vov_05` shows high mean IC but weaker positive-rate evidence, suggesting payoff asymmetry or instability.
- Redundancy against volatility compression, stress repair, persistence, and rank-coherence has not yet been measured in this module.

Family interpretation:

- VoV is a credible alpha research frontier.
- The evidence is candidate-level, not family-level validation evidence.
- Refinement should be restricted to `vov_01` and `vov_03`.

## SECTION 6 - Rolling IC Stability

Latest rolling 252-day medium-horizon highlights:

| candidate_id | h10 rolling 252 mean IC | h20 rolling 252 mean IC | h20 rolling 252 positive IC rate | interpretation |
| --- | ---: | ---: | ---: | --- |
| `vov_01` | 0.021965 | 0.045991 | 0.626984 | Strong recent support. |
| `vov_03` | 0.011816 | 0.031769 | 0.579365 | Constructive recent support. |
| `vov_05` | 0.043184 | 0.060650 | 0.503968 | Strong recent mean IC, weak hit-rate cleanliness. |
| `vov_02` | -0.018664 | -0.033617 | 0.289683 | Adverse recent medium-horizon behavior. |
| `vov_04` | -0.040280 | -0.058783 | 0.269841 | Strongly adverse recent medium-horizon behavior. |

Rolling stability interpretation:

- `vov_01` has the best combined h20 level and rolling stability profile.
- `vov_03` is stable enough to justify refinement design, especially at h10.
- `vov_05` is watch-worthy but needs review for payoff asymmetry before any refinement.
- `vov_02` and `vov_04` should not be refined.

## SECTION 7 - Mechanism Interpretation

`vov_01` tests volatility instability calming after elevated chop. Its result supports the idea that resolution of prior volatility instability can contain medium-horizon information when paired with low extension and prior chop context.

`vov_03` tests range-chop exhaustion. Its result supports the idea that disorder exhaustion, especially when range chop begins to compress, can predict medium-horizon recovery or normalization.

`vov_05` tests churn-controlled VoV stabilization. Its strong h20 mean IC suggests the mechanism may matter, but the weaker positive-rate profile implies that returns may be driven by fewer larger episodes or unstable payoff distribution.

`vov_02` tests rising VoV in low-extension names. The weak h10/h20 evidence suggests that rising instability is not constructive in this form and may represent unresolved risk rather than early repricing.

`vov_04` tests divergence between volatility level and VoV path. The negative medium-horizon result suggests the divergence formulation may be capturing confusion or adverse instability rather than useful path information.

## SECTION 8 - Redundancy Assessment

Measured redundancy was not run in Phase 9 and should not be inferred as solved.

Likely redundancy risks:

- `vov_01` may overlap with volatility compression after stress stabilization because both reward calming instability.
- `vov_03` may overlap with stress-repair or reversal if range-chop exhaustion is mostly a rebound proxy.
- `vov_05` may overlap with rank-coherence or persistence because it combines low churn with VoV stabilization.
- All advancing/watch candidates may have some exposure to hostile/stress-repair regimes.

Required refinement-design controls:

- Include volatility compression/stress stabilization references.
- Include hostile/stress-repair references.
- Include persistence and rank-coherence references.
- Include plain reversal and volume-shock reversal references.
- Report pairwise signal correlation, active-date overlap, and horizon concentration before any refined candidate can advance.

## SECTION 9 - Reasons For Classifications

Reasons for `ADVANCE`:

- `vov_01` clears h20 mean IC, IC IR, and positive IC rate standards and has positive h10 support.
- `vov_03` clears h10 mean IC, IC IR, and positive IC rate standards and has positive h20 support.
- Both have mechanism interpretations that can be refined without changing the family thesis.

Reasons for `WATCH`:

- `vov_05` has the strongest h20 mean IC and IC IR, but it does not clear the positive-rate threshold.
- Its rolling h20 mean is strong, but hit-rate evidence is not clean enough for refinement authorization.
- It may become diagnostic or refinement-eligible only after redundancy/payoff-asymmetry review.

Reasons for `PARK`:

- `vov_02` has negative h10/h20 mean IC and only mild h1 evidence.
- `vov_04` has negative h5/h10/h20 evidence and strongly adverse rolling medium-horizon behavior.
- Neither should consume refinement budget.

## SECTION 10 - Refinement Recommendation

Refinement is approved in principle, but only as a Phase 10 governance-authorized next step and only for two candidates:

- `vov_01`
- `vov_03`

Recommended refinement scope:

- Small, predeclared variant set.
- Preserve original mechanism identity.
- Include the original `vov_01` and `vov_03` anchors.
- Add no more than 2 to 4 variants per advancing candidate unless Phase 10 explicitly approves more.
- Include anti-redundancy diagnostics against volatility compression, stress repair, persistence, rank-coherence, plain reversal, and volume-shock reversal.
- Do not include `vov_02` or `vov_04`.
- Keep `vov_05` as a watch/reference candidate, not a refinement seed.

Refinement is not execution-authorized by this note. The next required step is Phase 10 governance decision.

## SECTION 11 - Recommended Phase 10 Governance Outcome

Recommended Phase 10 outcome:

| item | recommended outcome | next action |
| --- | --- | --- |
| `vov_01` | `ADVANCE` | Approve refinement design. |
| `vov_03` | `ADVANCE` | Approve refinement design. |
| `vov_05` | `WATCH` | Keep as watch/reference for payoff-asymmetry and redundancy review. |
| `vov_02` | `PARK` | Archive as negative evidence. |
| `vov_04` | `PARK` | Archive as negative evidence. |
| VoV module | bounded `ADVANCE` | Proceed to governance decision for two-candidate refinement design only. |

Recommended next task:

**Project Underdog - OHLCV Volatility-of-Volatility Governance Decision v1**

## SECTION 12 - Guardrail Confirmation

This review did not:

- perform refinement;
- regenerate panels;
- recompute IC;
- run validation;
- modify formulas;
- modify panel artifacts;
- modify IC artifacts;
- implement or touch Family B/C candidates;
- change governance files;
- modify production registry;
- change thresholds;
- introduce ML.

## SECTION 13 - Verification

Verified for this review:

- IC discovery note reviewed.
- IC discovery artifacts reviewed.
- Candidate rankings reviewed.
- Candidate-horizon scores reviewed.
- Horizon and family summaries reviewed.
- Rolling IC diagnostics reviewed.
- Manifest guardrail flags reviewed.
- No implementation files were changed by this review.
- No research artifacts were changed by this review.

Final classification:

- `REFINEMENT_APPROVED`
