# Project Underdog - Dispersion Path-Dependence Research Module Design v1

## SECTION 1 - Executive Summary

Classification: `DESIGN_READY_WITH_SCIENTIFIC_NOTES`

This note creates the Platform v2 research module design for Dispersion Path-Dependence after scientific gate approval in `dispersion_path_dependence_scientific_review_v1.md`.

This is a design task only. It does not write formulas, create executable candidates, finalize candidate code IDs, specify panels, implement code, generate artifacts, compute IC, run validation, change governance decisions, register production candidates, change thresholds, or introduce ML.

Design conclusion:

Dispersion Path-Dependence is ready for a future formula and panel specification phase with scientific notes. The module should test whether the path, memory, and transition behavior of cross-sectional disagreement contains forward information beyond static dispersion level, VoV, volatility compression, hostile/stress repair, volume shock reversal, persistence, rank coherence, and the parked non-hostile transition family.

The module should remain narrow: one primary mechanism, five mechanism-level concepts, h5/h10 primary scientific horizons, h20 as durability evidence only, and strict contamination controls.

## SECTION 2 - Lifecycle Reference

Platform status:

- Platform v1 established the engineering and governance lifecycle.
- Platform v2 added a scientific review gate before formula specification or implementation.
- Dispersion Path-Dependence passed the Platform v2 scientific gate with notes.

Input scientific gate:

- Note: `docs/research_notes/dispersion_path_dependence_scientific_review_v1.md`
- Classification: `SCIENTIFIC_GATE_APPROVED_WITH_NOTES`
- Recommendation: `ADVANCE_TO_DESIGN`

Current lifecycle phase:

- Phase 1B - Research Module Design under Platform v2.

This note is not:

- Phase 2 formula and panel specification;
- implementation;
- panel specification;
- panel generation;
- IC discovery;
- validation;
- governance decision;
- master state update.

The next phase may be formula and panel specification only if this design note is accepted.

## SECTION 3 - Materials Reviewed

Reviewed:

- `docs/research_notes/dispersion_path_dependence_scientific_review_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`
- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`
- `docs/research_notes/alpha_family_diversification_refinement_execution_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_results_review_and_candidate_registration_recommendation_v1.md`
- `docs/research_notes/rank_coherence_refinement_execution_v1.md`
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`

Key inherited constraints:

- Prior dispersion evidence was distinct but weak.
- Prior dispersion h20 evidence decayed.
- Narrow rising-dispersion activation damaged evidence.
- Rank coherence and persistence are major contamination risks.
- Hostile/stress repair and volatility compression remain mandatory contamination references.
- The module must not become another participation repair or non-hostile leadership continuation design.

## SECTION 4 - Hypothesis Freeze

Primary mechanism:

Dispersion Path-Dependence tests whether future cross-sectional returns depend on the sequence of market disagreement, not only the current level of dispersion. The mechanism is the path, memory, persistence, decay, relapse, and normalization of cross-sectional disagreement.

Economic intuition:

Cross-sectional repricing is not simultaneous. Incomplete information diffusion, staggered institutional repositioning, asynchronous repricing, delayed consensus formation, liquidity-provider adjustment, and possible sector/style rotation can make the recent path of disagreement meaningful.

Behavioral intuition:

Institutions, liquidity providers, ETF/passive flows, volatility-targeting or risk-controlled allocators, discretionary investors, and event-sensitive traders may adjust at different speeds. Their staggered actions can produce disagreement paths that resolve, relapse, or persist over h5/h10 horizons.

Expected information content:

The module should contribute information about:

- path of disagreement;
- memory of disagreement;
- transition behavior;
- disagreement resolution versus relapse;
- orderly versus fragile cross-sectional repricing;
- whether current dispersion means different things depending on recent history.

Expected primary horizons:

- h5 and h10.

Expected secondary horizon:

- h20 as durability evidence only.

Expected activation frequency:

- episodic and moderate;
- not continuous;
- not so sparse that a single crisis window dominates interpretation.

Expected orthogonality:

The module should be most distinct from participation repair and volume shock reversal, moderately distinct from VoV and volatility compression, and most at risk of contamination from rank coherence, persistence, static dispersion anchors, and hostile/stress repair.

Primary falsification criteria:

- no information beyond static dispersion level or prior dispersion anchors;
- evidence is dominated by rank coherence or persistence;
- evidence is dominated by hostile/stress repair or volatility compression;
- evidence is mostly VoV or volume shock reversal;
- h5/h10 evidence is flat, negative, or unstable;
- evidence appears only at h20 after horizon switching;
- active coverage is too sparse;
- one-window dominance controls fail;
- no coherent economic or behavioral interpretation survives review.

Key risks:

- redundancy with rank coherence and persistence;
- contamination with stress repair and volatility compression;
- overfitting path definitions;
- interpretation difficulty under OHLCV-only data;
- fragile activation or crisis-window concentration.

## SECTION 5 - Mechanism Decomposition

This section defines scientific dimensions only. It does not define formulas or executable candidates.

1. Memory of disagreement.

This dimension asks whether the market remembers recent disagreement. The same current dispersion state may have different meaning if it follows calm, follows elevated disagreement, or follows a failed normalization attempt.

2. Persistence and decay of disagreement.

This dimension asks whether disagreement is persistent, fading, or decaying too quickly to matter. A persistent disagreement state may imply unresolved repricing, while orderly decay may imply consensus formation.

3. Acceleration versus stabilization.

This dimension asks whether disagreement is becoming more chaotic or beginning to stabilize. Prior simple acceleration evidence was weak, so stabilization and transition shape must be separated from raw acceleration.

4. Low, medium, and high dispersion state transition.

This dimension asks whether transitions between disagreement regimes matter. The mechanism should distinguish calm-to-disagreement, high-to-normalizing, normalizing-to-relapse, and elevated-but-stabilizing paths.

5. Path shape.

Relevant path shapes include:

- spike then normalize;
- gradual climb;
- oscillation;
- compression then re-expansion;
- elevated then stable;
- relapse after temporary calm.

6. Burst versus smooth resolution.

This dimension asks whether disagreement resolves through abrupt burst-like repricing or smooth convergence. Burst resolution may indicate shock absorption or forced repositioning; smooth resolution may indicate gradual consensus formation.

## SECTION 6 - Candidate Design Space

The following are mechanism-level candidate concepts only. They are not executable candidate IDs, formulas, or panel specifications. Final candidate IDs must be created only in a later formula and panel specification task.

| concept name | scientific question | mechanism dimension | expected direction | expected horizon | expected activation profile | expected orthogonality | likely contamination risks | falsification condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Elevated Disagreement Stabilization | Do securities that remain orderly while market disagreement is elevated but stabilizing carry positive forward information? | persistence and decay; stabilization | Positive for orderly behavior during stabilizing elevated disagreement. | h5/h10 primary; h20 durability only. | Moderate; active during elevated but stabilizing disagreement states. | Should differ from static dispersion by requiring path stabilization. | Volatility compression, stress repair, rank coherence. | Park if evidence is explained by volatility calming, crisis recovery, or stable ranks alone. |
| Disagreement Relapse Resilience | Do securities resilient during a relapse of disagreement after temporary calm behave differently from securities that only looked strong during calm? | memory; relapse after calm | Positive for resilience through relapse without excessive extension. | h5/h10 primary. | Episodic; active around relapse states, not continuous. | Should differ from persistence by requiring disagreement relapse context. | Persistence, rank coherence, hostile/stress repair. | Park if prior winners explain the effect or if active dates are too sparse. |
| Consensus Formation Without Crowding | Does orderly disagreement normalization identify securities benefiting from delayed consensus formation without rewarding crowded leadership? | smooth resolution; normalization | Positive for low-crowding, orderly behavior during normalization. | h5/h10 primary; h20 secondary. | Moderate; active during normalization paths. | Should differ from parked non-hostile transition by avoiding leadership continuation claims. | Non-hostile transition, momentum, rank coherence. | Park if it becomes leadership continuation, momentum, or the parked non-hostile thesis under a new name. |
| Disagreement Path Divergence | Does a divergence between disagreement path and broader volatility/stress behavior reveal information that static volatility or VoV misses? | path shape; acceleration versus stabilization | Positive when disagreement path carries independent repricing information. | h5/h10 primary. | Moderate to low; active when disagreement path separates from volatility/stress path. | Should differ from VoV and volatility compression by focusing on cross-sectional disagreement path. | VoV, volatility compression, static dispersion level. | Park if VoV or volatility compression explains most behavior. |
| Smooth Versus Burst Resolution | Does smooth convergence of disagreement differ from abrupt burst-like resolution in forward return behavior? | burst versus smooth resolution | Positive for orderly smooth resolution if it indicates consensus formation; diagnostic if burst resolution dominates. | h5 primary, h10 secondary. | Episodic; active around resolution events. | Should differ from volume shock reversal by focusing on disagreement topology rather than a single event. | Volume shock reversal, plain reversal, event shock effects. | Park if behavior is just volume shock reversal or plain reversal after burst events. |

Candidate budget:

- Default concept count: 5.
- The later formula specification may narrow this set.
- The later formula specification must not expand beyond 6 candidates without a separate scientific exception.

## SECTION 7 - Inclusion Criteria

A future candidate may be included only if it satisfies all of the following:

- measures path, memory, transition, relapse, normalization, stabilization, or resolution behavior of cross-sectional disagreement;
- has a predeclared expected direction;
- has h5 or h10 as a primary scientific horizon;
- defines how it differs from static dispersion level;
- defines how it differs from rank coherence and persistence;
- defines how it differs from hostile/stress repair and volatility compression;
- can be falsified by a specific contamination or incremental-information test;
- preserves the Platform v2 learning objective if it fails.

A future candidate must be excluded if its only scientific claim is that current dispersion is high, low, rising, or falling.

## SECTION 8 - Exclusion Criteria

The module must exclude:

- pure dispersion level;
- simple rising dispersion alone;
- simple falling dispersion alone;
- plain reversal;
- plain momentum;
- volatility compression duplicate;
- VoV duplicate;
- hostile/stress repair duplicate;
- participation repair duplicate;
- volume shock reversal duplicate;
- rank-coherence duplicate;
- persistence duplicate;
- parked non-hostile transition or leadership-rotation continuation;
- event clustering concepts unless separately scoped;
- any concept whose success would require post-hoc horizon switching.

Any future formula or candidate concept that violates these exclusions should be rejected before implementation.

## SECTION 9 - Orthogonality Controls

Future formula and panel specification must define contamination tests against the following references:

| reference | required control |
| --- | --- |
| VoV | Test whether dispersion-path behavior remains distinct from volatility-instability path behavior. |
| Participation repair | Test whether the signal requires weak breadth, hostile trend, or participation/liquidity repair conditions. |
| Hostile/stress repair | Test whether evidence is concentrated in panic, drawdown, broad recovery, or stress-repair states. |
| Volatility compression | Test whether positive behavior appears only when volatility is compressing or stabilizing. |
| Volume shock reversal | Test whether burst or event-heavy disagreement paths reduce to volume shock or plain reversal behavior. |
| Rank coherence / persistence | Test whether stable ranks, low churn, or prior winners explain the signal. |
| Static dispersion anchors | Test incremental information beyond simple dispersion level and prior dispersion acceleration anchors. |
| Parked non-hostile transition | Test whether low-extension or orderly behavior is merely leadership continuation or late-cycle crowding. |

Required design principle:

Low churn, low extension, or stability controls may be used later only as controls. They must not become the primary mechanism.

## SECTION 10 - Falsifiability Plan

The module should later be parked or revised if:

- h5/h10 primary evidence is non-positive, directionally wrong, or unstable;
- apparent evidence exists only at h20 or only after horizon switching;
- evidence adds no incremental information beyond static dispersion level;
- evidence adds no incremental information beyond prior dispersion anchors;
- rank coherence or persistence explains the strongest behavior;
- hostile/stress repair explains the strongest behavior;
- volatility compression or VoV explains the strongest behavior;
- volume shock reversal or plain reversal explains burst-resolution behavior;
- active coverage is too sparse for stable cross-sectional interpretation;
- one crisis or transition window dominates results;
- the concept cannot be tied back to incomplete information diffusion, staggered repositioning, asynchronous repricing, delayed consensus formation, or liquidity-provider adjustment;
- the future candidate set expands beyond the approved mechanism scope.

Park versus revise logic:

- Park if the mechanism fails at the family level or is fully explained by existing families.
- Revise if only one concept fails but the broader disagreement-path thesis remains scientifically coherent.
- Diagnostic-only if the module produces useful negative evidence about dispersion but no candidate-level advancement.

## SECTION 11 - Learning Objective

If the module fails, Project Underdog should learn:

- whether dispersion should remain an active alpha-family frontier;
- whether h5/h10 is the only plausible horizon for dispersion mechanisms;
- whether h20 decay is structural for dispersion in the current OHLCV universe;
- whether rank coherence and persistence already capture the useful part of orderly cross-sectional structure;
- whether stress repair and volatility compression explain most high-dispersion behavior;
- whether future dispersion research needs point-in-time sector, industry, peer, or flow context;
- whether event clustering should remain separate from dispersion path-dependence.

This learning objective justifies a narrow design even if future IC discovery is weak.

## SECTION 12 - Staged Roadmap

Future phases only:

1. Formula and panel specification.
   - Freeze candidate IDs, formulas, expected horizons, contamination references, and artifact plan.
   - Must preserve this design's hypothesis freeze and exclusion criteria.

2. Implementation.
   - Implement only approved formula-specification candidates.
   - No extra candidates.

3. Implementation review.
   - Confirm implementation matches specification and no hidden mechanism drift occurred.

4. Panel specification.
   - Freeze panel schema, timing, metadata, and manifest requirements.

5. Panel generation.
   - Generate only approved research panels.

6. Panel audit.
   - Confirm schema, timing, duplicate-key, coverage, and manifest integrity before IC.

7. IC discovery.
   - Score only the approved candidate set at predeclared horizons.

8. Research review.
   - Interpret evidence against the frozen hypothesis, orthogonality controls, and falsifiability plan.

9. Governance decision.
   - Classify candidates as advance, watch, park, or diagnostic according to predeclared logic.

10. Master state update.
   - Synchronize final research state and archive evidence.

No validation, refinement, registration, production, or ML work is authorized by this design note.

## SECTION 13 - Explicit Non-Goals

This note does not:

- write formulas;
- create executable candidate IDs;
- finalize candidate code IDs;
- specify panels;
- implement code;
- generate artifacts;
- compute IC;
- run validation;
- refine candidates;
- modify governance decisions;
- modify registry files;
- change thresholds;
- make production changes;
- introduce ML;
- reopen parked candidates;
- promote or demote any candidate.

## SECTION 14 - Verification

Verification:

- Required sections exist: lifecycle reference, hypothesis freeze, mechanism decomposition, candidate design space, inclusion criteria, exclusion criteria, orthogonality controls, falsifiability plan, learning objective, staged roadmap, explicit non-goals, and classification.
- Hypothesis freeze exists.
- Five mechanism-level candidate concepts are included.
- No formulas are written.
- No executable candidate code IDs are finalized.
- No panel specification is included.
- No implementation files were changed.
- No panel files were changed.
- No IC work was performed.
- No validation was performed.
- No governance decision was modified.
- No production files were changed.
- No threshold files were changed.
- No ML files were changed.

## SECTION 15 - Final Classification

Final classification:

- `DESIGN_READY_WITH_SCIENTIFIC_NOTES`

Dispersion Path-Dependence is ready for a future formula and panel specification phase, subject to the scientific notes and contamination controls in this design. The next task should be formula and panel specification only, not implementation or IC discovery.
