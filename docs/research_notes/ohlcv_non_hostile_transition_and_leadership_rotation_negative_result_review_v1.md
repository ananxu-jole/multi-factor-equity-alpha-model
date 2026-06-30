# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Negative Result Review v1

## SECTION 1 - Executive Summary

This note reviews the negative first-pass IC discovery result for the OHLCV Non-Hostile Transition and Leadership Rotation family.

Final classification: `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.

The first IC discovery pass classified all nine approved candidates as `REJECT`. No candidate produced positive primary-horizon evidence across `h10`/`h20`. The least weak candidate was `nhlr_05`, with best primary-horizon mean IC of -0.000173 at h10, but that is not enough for watchlist or refinement consideration.

The negative result is broad-based across the medium horizons that the family was designed to target. The family should be parked as currently implemented. A separate direction-inversion diagnostic may be useful later because several candidates show mild h1 behavior while h10/h20 deteriorate, and because the medium-horizon signs are consistently adverse. That diagnostic should be design-only or explicitly diagnostic if pursued, not a refinement or validation run.

No formulas, panels, governance files, production registration, thresholds, or ML artifacts were changed in this review.

## SECTION 2 - Materials Reviewed

Reviewed note:

- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1.md`

Reviewed artifacts:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/daily_ic.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_ic_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_horizon_ic_scores.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/horizon_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/family_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_rankings.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/rolling_ic_diagnostics.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/manifest.json`

## SECTION 3 - Summary of IC Outcome

Candidate classifications:

- `ADVANCE_TO_REFINEMENT`: 0
- `WATCH`: 0
- `REJECT`: 9

Candidate ranking by best primary-horizon mean IC:

| rank | candidate_id | best primary horizon | best primary mean IC | best any horizon | best any mean IC | classification |
| ---: | --- | --- | ---: | --- | ---: | --- |
| 1 | `nhlr_05` | h10 | -0.000173 | h1 | 0.004618 | `REJECT` |
| 2 | `nhlr_10` | h20 | -0.003871 | h1 | 0.001173 | `REJECT` |
| 3 | `nhlr_08` | h10 | -0.009261 | h1 | 0.002693 | `REJECT` |
| 4 | `nhlr_07` | h20 | -0.011374 | h1 | -0.007093 | `REJECT` |
| 5 | `nhlr_09` | h10 | -0.012459 | h1 | -0.003874 | `REJECT` |
| 6 | `nhlr_02` | h10 | -0.015638 | h1 | 0.002453 | `REJECT` |
| 7 | `nhlr_03` | h10 | -0.015651 | h1 | 0.000771 | `REJECT` |
| 8 | `nhlr_01` | h10 | -0.016849 | h1 | -0.007162 | `REJECT` |
| 9 | `nhlr_04` | h10 | -0.017945 | h1 | -0.005442 | `REJECT` |

Family-level mean IC:

| horizon | mean IC | median IC | mean IC IR | mean positive IC rate |
| --- | ---: | ---: | ---: | ---: |
| h1 | -0.001318 | 0.000771 | -0.005077 | 0.507879 |
| h5 | -0.006609 | -0.007991 | -0.031519 | 0.504013 |
| h10 | -0.011925 | -0.014466 | -0.062512 | 0.493745 |
| h20 | -0.014564 | -0.015146 | -0.080399 | 0.488678 |

## SECTION 4 - Candidate-Level Interpretation

The negative result is broad rather than isolated.

Candidate observations:

- `nhlr_05` is the least negative primary-horizon candidate. It has h10 mean IC of -0.000173 and h10 positive IC rate of 0.533333, but the mean IC and IC IR are effectively flat-to-negative. It should not be watchlisted because the primary mean IC does not clear zero.
- `nhlr_10` is second best by primary-horizon ranking, but h20 mean IC is -0.003871 and h10 mean IC is -0.004884. Its breadth-related behavior may be less adverse than most candidates, but it is still not positive.
- `nhlr_08` has mild h1 evidence and acceptable h10/h20 positive IC rates, but the h10/h20 mean ICs are materially negative.
- `nhlr_01`, `nhlr_02`, `nhlr_03`, and `nhlr_04` are the clearest rejects because primary-horizon mean ICs range from roughly -0.0156 to -0.0257.
- `nhlr_07` and `nhlr_09`, the faster rotation/confirmation candidates, also fail at h10/h20 and do not rescue the family through shorter-horizon behavior.

No candidate is close enough to justify watchlist status under the discovery criteria. `nhlr_05` and `nhlr_10` may be useful only as references if a later inversion or redesign discussion is authorized.

## SECTION 5 - Horizon-Level Interpretation

The horizon pattern is important:

- h1 is least negative, with family mean IC of -0.001318.
- h5 is more negative, with family mean IC of -0.006609.
- h10 is clearly negative, with family mean IC of -0.011925.
- h20 is the weakest, with family mean IC of -0.014564.

This pattern suggests one of three possibilities:

- any useful information in these formulas decays quickly and does not survive to the intended medium horizon;
- the formulas are picking up crowded leadership behavior that mean-reverts at h10/h20;
- the intended non-hostile transition thesis may be directionally inverted in the available OHLCV universe.

h1 being least negative is not enough to save the family. The approved economic thesis was medium-horizon non-hostile transition and leadership rotation, not same-day or next-day microstructure behavior.

## SECTION 6 - Family-Level Interpretation

The family is not supported as currently designed.

The medium-horizon evidence is not merely weak; it is consistently adverse. All approved candidates failed the primary h10/h20 mean IC test, and the family summary worsens as the horizon lengthens. That is directly contrary to the original mechanism, which expected orderly leadership transition, healthy breadth contribution, and durable rotation behavior to express over h10/h20.

The family should not proceed to refinement. Refinement would risk optimizing around a failed first-pass sign rather than improving a promising mechanism.

## SECTION 7 - Possible Explanations

Possible explanations for the negative result:

- The formulas may be selecting already-recognized leadership rather than early leadership transition.
- Non-hostile breadth/participation gates may identify crowded or late-cycle behavior that underperforms after the signal date.
- The current OHLCV-only features may lack enough context to distinguish healthy transition from mature leadership exhaustion.
- The family may overlap with stress-repair or hostile-transition concepts, but without explicit stress-state context the formulas may mix constructive transition with adverse rebound or exhaustion states.
- The target horizon may not match the information half-life; the mild h1/h5 behavior in `nhlr_05` and h1 behavior in several candidates suggests any usable signal may be short-lived.
- The economic direction may be inverted: high formula values may correspond to over-owned or overextended names rather than future leadership.

These are hypotheses for review only. This note does not test new formulas, new targets, or inverted panels.

## SECTION 8 - Inversion Diagnostic Discussion

A direction-inversion diagnostic is optional but defensible.

Reasons inversion might be worth testing later:

- all best primary-horizon mean IC values are negative;
- family-level mean IC becomes more negative from h1 to h20;
- h10/h20 weakness is broad across candidates;
- some candidates show positive hit rates despite negative mean IC, suggesting payoff asymmetry or sign/scale mismatch.

Reasons inversion should not be treated as automatic rescue:

- inverted signals would be a different economic claim from the approved family;
- inversion could simply convert a failed leadership-transition family into a late-leadership avoidance or anti-crowding family;
- any inversion test would need predeclared diagnostic status and should not become stealth refinement;
- inverted results would still need contamination review against reversal, stress-repair, and rank-coherence families.

Recommended handling:

- Do not run inversion now.
- If pursued, create a separate **direction-inversion diagnostic design** note first.
- Treat inversion output as diagnostic only, not validation, not refinement, and not production-eligible.

## SECTION 9 - Concept Redesign Discussion

Full redesign is not the immediate next step, but may become appropriate after review.

Potential redesign directions:

- Separate early transition from mature leadership more sharply.
- Add explicit anti-extension controls so leadership emergence is not confused with already-crowded leadership.
- Reconsider whether breadth-contribution candidates should be framed as short-horizon diagnostic signals rather than h20 candidates.
- Require clearer distinction from hostile-transition and stress-repair mechanisms before reimplementation.
- Consider whether the correct family is not non-hostile leadership continuation, but late-leadership avoidance, controlled de-risking, or anti-crowding.

Redesign should not reuse the current rejected formulas as a parameter-tuning starting point. If redesign is authorized, it should reopen the concept at the specification layer.

## SECTION 10 - Stress-Repair and Hostile-Transition Overlap

Conceptual overlap remains a concern.

The family was intentionally designed to avoid hostile/stress-repair framing, but the negative evidence suggests the current OHLCV formulas may not cleanly isolate non-hostile transition. They may be mixing:

- leadership after broad market repair;
- participation rebound;
- mature trend sponsorship;
- breadth expansion after prior weakness;
- crowded leadership continuation.

Because no stress-state attribution or redundancy screen was run in this review, this remains a conceptual concern rather than a measured contamination result. Any future redesign should explicitly test separation from hostile-transition, stress-repair, persistence, and rank-coherence families before implementation.

## SECTION 11 - Governance Recommendation

Recommended governance outcome: `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.

Rationale:

- `FAMILY_PARKED_NEGATIVE_EVIDENCE` is too final because the consistent negative h10/h20 sign may contain diagnostic information.
- `FAMILY_REDESIGN_REQUIRED` is premature because no redesign should occur before a targeted review of inversion and conceptual overlap.
- `FAMILY_REVIEW_INCONCLUSIVE` is too weak because the IC evidence is clear enough to block refinement.

Operational recommendation:

- Park the current implemented family.
- Do not advance any candidate to refinement.
- Do not place any candidate on watchlist for validation or production.
- Permit only a future, separately scoped inversion diagnostic design if the research team wants to understand whether the current formulas are anti-predictive.

## SECTION 12 - Explicit Non-Goals

This review did not:

- refine candidates;
- modify formulas;
- modify panels;
- compute new IC;
- run validation;
- change governance registration;
- change production registry;
- change thresholds;
- introduce ML;
- promote or demote candidates;
- run redundancy screening;
- execute a direction-inversion test.

## SECTION 13 - Verification

Verification performed:

- Confirmed all required IC artifacts exist under `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/`.
- Confirmed `candidate_rankings.csv` contains 9 `REJECT` classifications and no `WATCH` or `ADVANCE_TO_REFINEMENT` classifications.
- Confirmed `manifest.json` guardrail flags remain false for refinement, validation, governance mutation, threshold changes, production registration, ML, formula modification, and panel modification.
- Confirmed this review did not rewrite panel files or formula files.

Required IC artifacts present:

- `daily_ic.csv`
- `candidate_ic_summary.csv`
- `candidate_horizon_ic_scores.csv`
- `horizon_summary.csv`
- `family_summary.csv`
- `candidate_rankings.csv`
- `rolling_ic_diagnostics.csv`
- `approved_panel_manifest.csv`
- `manifest.json`

## SECTION 14 - Next-Step Recommendation

Recommended next step: no execution.

If the research team wants to continue learning from this negative result, the next task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Direction-Inversion Diagnostic Design v1**.

That task should be design-only and should specify:

- whether inversion is economically interpretable;
- which candidates, if any, are eligible for diagnostic inversion;
- how to prevent overlap with reversal, stress-repair, and rank-coherence families;
- what artifacts would be produced;
- why the diagnostic would not constitute refinement, validation, governance change, or production registration.

Final classification: `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.
