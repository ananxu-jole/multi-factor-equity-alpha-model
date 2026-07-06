# Project Underdog - Platform v2 Scientific Research Standard v1

## SECTION 1 - Purpose And Authority

Classification: `PLATFORM_V2_SCIENTIFIC_STANDARD_APPROVED`

This document defines the Platform v2 scientific research standard for all future Project Underdog alpha research modules.

Platform v2 extends the released Platform v1 engineering and governance lifecycle by adding a stricter scientific review gate before formula specification and implementation. Platform v1 proved that Project Underdog can execute disciplined research modules with lifecycle gates, panel audits, IC discovery, bounded refinement, validation, integrity checks, and reproducibility standards. Platform v2 raises the entry bar for new alpha families so implementation effort is spent only on modules with a clear hypothesis, economic mechanism, behavioral story, orthogonality thesis, falsifiability plan, and learning objective.

This is a documentation and governance standard only. No implementation, formula specification, panel generation, IC computation, validation execution, governance decision mutation, production registration, threshold change, artifact regeneration, or ML work was performed.

## SECTION 2 - Relationship To Platform v1

Platform v1 remains the baseline lifecycle authority for engineering, artifact, governance, validation, and integrity controls. Platform v2 does not replace the Platform v1 lifecycle. It adds a scientific gate before a module may proceed to formula and panel specification.

Platform v1 answered:

- Can research be executed through auditable phases?
- Can implementation, panel generation, IC discovery, review, governance, validation, and closeout be separated?
- Can artifacts, manifests, checksums, and guardrails preserve research integrity?

Platform v2 requires every future module to answer first:

- What market behavior is being tested?
- Why should the behavior exist?
- Who is making the mistake or supplying the opportunity?
- Why is the mechanism distinct from existing validated, watched, parked, or failed families?
- What evidence would falsify the hypothesis?
- What will the project learn if the module fails?

Platform v2 inserts the following mandatory scientific gate:

1. Phase 0 - Research Frontier Selection.
2. Phase 1A - Scientific Hypothesis And Orthogonality Review.
3. Phase 1B - Research Module Design.
4. Phase 2 - Formula And Panel Specification.
5. Existing Platform v1 phases continue unchanged.

A module may not proceed to Phase 2 formula and panel specification unless Phase 1A is classified as scientifically ready.

## SECTION 3 - Materials Reviewed

Reviewed for this standard:

- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`
- `docs/research_notes/project_underdog_platform_v1_independent_release_review.md`
- `docs/research_notes/project_underdog_platform_v1_closeout_and_vov_registration_preparation_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_results_review_and_candidate_registration_recommendation_v1.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`
- `docs/research_notes/ohlcv_vov_dispersion_path_dependence_event_clustering_discovery_program_design_v1.md`

Key Platform v1 lessons incorporated:

- Process discipline worked.
- Bounded refinement worked better than broad variant search.
- Anchor comparators improved interpretability.
- Contamination-reference evidence must be real before stronger governance claims.
- Candidate families can be process-clean but scientifically redundant.
- Some negative results are valuable only if the learning objective is explicit before implementation.

## SECTION 4 - Platform v2 Required Scientific Sections

Every future research module must include the following sections before formula specification.

### 1. Scientific Hypothesis

The module must state:

- what market behavior is being tested;
- why the behavior should exist;
- the expected direction of the signal;
- the expected primary horizon and secondary horizons;
- whether the expected evidence is candidate-level, family-level, or diagnostic-only.

The hypothesis must be narrow enough that a negative result is interpretable. A thesis such as "volatility matters" is not sufficient. A thesis such as "securities resilient during dispersion relapse after temporary calm should outperform over h5/h10 if dispersion path contains information beyond static stress repair" is acceptable.

### 2. Economic Intuition

The module must explain:

- what structural market condition creates the opportunity;
- why the mechanism should create cross-sectional return differences;
- why the signal is not merely another transformation of existing OHLCV features;
- why the mechanism should survive transaction, turnover, coverage, or activation constraints at research scale.

Economic intuition may be OHLCV-only, but it cannot be purely algebraic. The note must explain the market condition being proxied by the features.

### 3. Behavioral Intuition

The module must identify the plausible behavior or constraint behind the opportunity.

Examples of acceptable actors or flows:

- institutions adjusting risk budgets;
- retail overreaction or delayed reaction;
- liquidity providers widening or tightening provision;
- volatility-targeting or risk-parity de-risking;
- ETF or passive-flow pressure;
- market-maker inventory and hedging behavior;
- crowded active managers;
- short-horizon event traders;
- slow-moving discretionary allocators.

The behavioral story does not need to prove causality, but it must make the expected sign and horizon plausible.

### 4. Orthogonality Thesis

The module must state why the proposed mechanism should differ from existing Project Underdog families.

At minimum, every new module must compare against:

- VoV and validated VoV refinement candidates;
- participation repair and participation/breadth repair;
- volatility compression and stress stabilization;
- volume shock reversal;
- hostile/stress repair;
- rank coherence and persistence;
- dispersion anchors and prior dispersion acceleration work;
- parked non-hostile transition and leadership rotation.

The orthogonality thesis must include both semantic and empirical expectations:

- semantic: how the mechanism is conceptually different;
- empirical: what correlation, co-activation, horizon, state-slice, or anchor-comparison evidence would support or refute distinctiveness.

### 5. Falsifiability

The module must predefine what evidence would cause the module to be parked.

Required falsification categories:

- primary horizon fails the predeclared direction;
- evidence is h1-only or one-window dominated when medium-horizon behavior was claimed;
- active coverage is too sparse for stable interpretation;
- turnover or rank churn is too high for research usefulness;
- candidate evidence is explained by an existing family;
- contamination references dominate signal behavior;
- anchor/comparator deltas fail;
- panel or timing integrity fails;
- apparent success depends on post-hoc horizon switching or target hacking.

Falsifiability must be specific enough that the research review can park the module without renegotiating the standards after results are known.

### 6. Learning Objective

Every module must define what Project Underdog will learn even if the module fails.

Examples:

- whether dispersion path-dependence is worth further investment;
- whether event clustering is just disguised volume-shock reversal;
- whether non-hostile transition failure reflected wrong direction, wrong horizon, or crowding;
- whether volatility-state effects are independent of hostile/stress repair;
- whether rank coherence contaminates low-churn state designs.

A module with no learning objective is not ready, even if candidates are easy to implement.

### 7. Candidate Discipline

Platform v2 candidate discipline:

- one primary mechanism per module;
- 4 to 6 candidates by default;
- more than 6 candidates requires explicit scientific justification;
- no broad search;
- no target hacking;
- no horizon shopping;
- no candidate generation from results;
- one bounded refinement cycle maximum unless separately approved after research review;
- anchors and comparators must be predeclared;
- candidate IDs must be frozen before implementation;
- every candidate must map to the module's primary mechanism or be labeled comparator/diagnostic.

If a proposed module requires many mechanism groups, it should be split into separate modules unless a scientific note justifies a coordinated family design.

### 8. Predefined Success Criteria

Before implementation, every module must predefine:

- primary horizon for each candidate;
- allowed secondary horizons;
- expected sign;
- mean IC, IC IR, positive IC-rate, active coverage, turnover, and stability requirements;
- anchor and comparator rules;
- contamination-reference rules;
- watch, park, diagnostic, and advance logic;
- conditions under which family-level evidence may be claimed;
- conditions under which only candidate-level evidence may be claimed.

Success criteria must be written before scoring. They may not be weakened during IC discovery or research review.

### 9. Scientific Review Gate

The scientific review gate must explicitly decide whether the module is ready to proceed to formula specification.

The review must evaluate:

- scientific hypothesis;
- economic intuition;
- behavioral intuition;
- orthogonality thesis;
- falsifiability;
- learning objective;
- candidate discipline;
- predefined success criteria;
- data feasibility;
- known contamination and redundancy risks.

If any of scientific hypothesis, orthogonality thesis, falsifiability, or learning objective is missing or weak, the module must not proceed to formula specification.

### 10. Platform v2 Module-Readiness Classifications

Scientific review notes must use one of:

| classification | meaning |
| --- | --- |
| `SCIENTIFIC_STANDARD_APPROVED` | The module has a clear hypothesis, mechanism, orthogonality thesis, falsification plan, learning objective, candidate discipline, and success criteria. It may proceed to formula and panel specification under Platform v1 engineering controls. |
| `SCIENTIFIC_STANDARD_APPROVED_WITH_NOTES` | The module may proceed, but specific scientific risks must be carried into formula specification, panel audit, IC discovery, and research review. |
| `SCIENTIFIC_STANDARD_NOT_READY` | The module may not proceed to formula specification. It must be redesigned, narrowed, or parked. |

## SECTION 5 - Orthogonality Requirements

Orthogonality is not optional in Platform v2.

Each new module must include a comparison table against the current Project Underdog inventory and diagnostic archives.

Required comparison fields:

- reference family;
- current status of reference family;
- expected overlap channel;
- why the new mechanism should differ;
- required contamination diagnostic;
- maximum acceptable correlation or co-activation expectation where predefinable;
- expected horizon distinction;
- expected state-slice distinction;
- action if the reference explains the new candidate.

Required references:

| reference | current role in Platform v2 |
| --- | --- |
| VoV | validated candidate-registration-review lineage; contamination review pending |
| Participation repair | established conditional repair umbrella and active redundancy benchmark |
| Volatility compression | watch/monitor and stress-stabilization benchmark |
| Volume shock reversal | controlled reference; reversal/liquidity-flow contamination benchmark |
| Hostile/stress repair | dominant existing umbrella; mandatory contamination benchmark |
| Rank coherence / persistence | conditional lineage and rank-stability contamination benchmark |
| Dispersion anchors | distinct but fragile prior evidence; mandatory comparator for dispersion-like modules |
| Parked non-hostile transition | negative-evidence archive; prevents stealth leadership-continuation rescue |

If a module cannot explain its difference from these references, it should be classified `SCIENTIFIC_STANDARD_NOT_READY`.

## SECTION 6 - Falsifiability Requirements

Every future module must include a falsification table before formulas are specified.

Required fields:

- falsification test;
- evidence source;
- threshold or qualitative stop condition;
- affected candidate or family;
- governance consequence.

Minimum stop conditions:

- primary-horizon mean IC is non-positive or directionally wrong for most candidates;
- IC IR and positive IC rate do not support the mean IC;
- positive result exists only at an undeclared horizon;
- active coverage is below the predeclared minimum;
- result is dominated by one short sample window or crisis window;
- maximum contamination correlation or co-activation exceeds the predeclared tolerance;
- anchor comparison is negative for the refined candidate;
- candidate behavior is indistinguishable from a known family;
- panel lineage, timing, checksum, or duplicate-key audit fails.

The review must not invent new rescue interpretations after a falsification trigger is met. A separately scoped redesign may be proposed, but the current module should be parked or downgraded.

## SECTION 7 - Candidate Discipline And Search Control

Platform v2 forbids broad research sweeps disguised as modules.

Permitted:

- small mechanism-led candidate sets;
- one primary mechanism with 4 to 6 candidates;
- predeclared anchors and comparators;
- one bounded refinement cycle after research review;
- diagnostic references that are clearly labeled and not ranked as candidates.

Not permitted:

- dozens of loosely related candidates;
- selecting primary horizons after seeing results;
- adding variants during IC discovery;
- using validation to rescue watch/park candidates not approved for validation;
- mixing unrelated mechanisms to improve headline IC;
- using ML or automated search to generate formula candidates under this standard;
- treating a parked family as active through renaming.

## SECTION 8 - Success Criteria Discipline

Every module must predefine success criteria at three levels.

Candidate-level criteria:

- primary horizon;
- expected sign;
- minimum mean IC direction and practical magnitude;
- IC IR support;
- positive IC-rate support;
- active coverage range;
- turnover or rank-churn tolerance;
- recent-window or stability-slice expectation;
- anchor/comparator delta expectation.

Family-level criteria:

- minimum number of candidates with coherent evidence;
- horizon coherence across candidates;
- evidence that success is not only one candidate with sibling duplicates;
- acceptable family-level contamination profile;
- decision rule for candidate-level versus family-level claims.

Governance criteria:

- `ADVANCE` only when candidate-level evidence, stability, and contamination controls support a next phase;
- `WATCH` only when evidence is useful but incomplete or contaminated;
- `PARK` when primary evidence, falsifiability, or distinctiveness fails;
- `DIAGNOSTIC` when a candidate teaches a useful failure mode but should not advance.

Success criteria must be included in the scientific review and restated in formula specification.

## SECTION 9 - Scientific Review Gate Procedure

The scientific review gate is a required documentation phase after frontier selection and before formula specification.

Required inputs:

- selected frontier note;
- current master status and research-state audit;
- candidate consolidation or inventory notes;
- relevant validation, watch, parked, and negative-result notes;
- Platform v1 release review and closeout caveats;
- available data feasibility notes.

Required outputs:

- scientific hypothesis;
- economic intuition;
- behavioral intuition;
- orthogonality thesis;
- falsification table;
- learning objective;
- candidate budget;
- predefined success criteria;
- contamination reference plan;
- readiness classification.

Exit criteria:

- `SCIENTIFIC_STANDARD_APPROVED` or `SCIENTIFIC_STANDARD_APPROVED_WITH_NOTES`.

Blocking conditions:

- mechanism is redundant with an existing family;
- expected sign or horizon is unclear;
- no behavioral or economic reason is stated;
- candidate budget is too broad;
- falsification standards are missing;
- learning objective is missing;
- required contamination references are ignored;
- data dependency is unavailable or PIT-unsafe.

## SECTION 10 - Example: VoV Under Platform v2

VoV is the strongest Platform v1 example of a module that mostly satisfies the Platform v2 scientific bar.

Scientific hypothesis:

- Volatility-of-volatility path behavior may predict medium-horizon cross-sectional returns beyond simple volatility level or compression.

Economic intuition:

- Erratic volatility dynamics can indicate unstable risk perception, liquidity provision, and crowding.
- Calming after prior instability can indicate resolution before broad price leadership is visible.

Behavioral intuition:

- Institutions, volatility-sensitive allocators, liquidity providers, and crowded holders may adjust at different speeds after volatility instability.

Orthogonality thesis:

- VoV differs from volatility compression by measuring instability of volatility rather than only volatility level decline.
- It differs from hostile/stress repair if it remains informative outside panic/drawdown recovery windows.
- It differs from rank coherence if low churn is a control rather than the full mechanism.

Falsifiability:

- Park if results are explained by volatility compression, stress repair, rank coherence, or `vov_05`-like longer-memory stabilization.
- Park if h10/h20 evidence does not improve anchor comparators.

Platform v1 outcome under this lens:

- `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` passed validation execution and were recommended for active research inventory registration review.
- Both remain non-production and contamination-review-pending.

Platform v2 lesson:

- Future VoV-like modules must include actual contamination-reference diagnostics before stronger claims than active research registration review.

## SECTION 11 - Example: Dispersion Path-Dependence Under Platform v2

The upcoming Dispersion Path-Dependence module may begin under Platform v2 only if it passes a scientific review gate before any new formula specification or implementation.

Acceptable Platform v2 hypothesis:

- Cross-sectional returns may depend on the sequence of dispersion elevation, stabilization, relapse, or normalization, not merely on static dispersion level or simple dispersion acceleration.

Economic intuition:

- Dispersion paths can reveal whether cross-sectional repricing is orderly, fragile, relapsing, or stabilizing.
- Names resilient during dispersion relapse or orderly normalization may carry different information from names that are merely high-ranked or recovering from stress.

Behavioral intuition:

- Crowded managers, liquidity providers, risk-controlled institutions, and event-driven traders may react differently to repeated dispersion shocks than to isolated volatility or volume events.

Required orthogonality:

- Must differ from VoV by focusing on cross-sectional dispersion paths, not volatility-instability paths.
- Must differ from participation repair by avoiding weak-breadth or hostile-repair gates as the primary mechanism.
- Must differ from volatility compression by not relying on simple volatility calming.
- Must differ from volume shock reversal by avoiding single-event reversal logic.
- Must differ from hostile/stress repair by showing state-path information outside panic recovery.
- Must differ from rank coherence and persistence by making dispersion path the primary conditioning variable, not stable ranks.
- Must differ from prior dispersion anchors by avoiding simple rising or falling dispersion alone.
- Must not revive the parked non-hostile transition family through low-extension leadership language.

Required falsifiability:

- Park if h5/h10 evidence is flat and h20 decays as in prior dispersion work.
- Park if the best candidate is mostly rank coherence, persistence, stress repair, or volume shock reversal.
- Park if active coverage is too sparse or one crisis window dominates.
- Park if dispersion path terms add no value beyond static dispersion anchors.

Learning objective:

- Even if the module fails, Project Underdog should learn whether dispersion is worth revisiting as a path-dependent state mechanism or should remain only a diagnostic reference.

Readiness implication:

- Dispersion Path-Dependence may begin as a scientific review/design task under Platform v2.
- It may not proceed directly to implementation unless the scientific review is classified `SCIENTIFIC_STANDARD_APPROVED` or `SCIENTIFIC_STANDARD_APPROVED_WITH_NOTES`.

## SECTION 12 - Explicit Non-Goals

This standard does not:

- implement any research module;
- specify candidate formulas;
- generate panels;
- compute IC;
- run validation;
- rerun research;
- regenerate artifacts;
- change existing governance decisions;
- modify the active research registry;
- modify the production registry;
- change thresholds;
- authorize production deployment;
- authorize ML;
- resolve PIT metadata blockers;
- promote any candidate;
- reopen parked candidates.

## SECTION 13 - Verification

Verification for this standard:

- Required sections exist: purpose, relationship to Platform v1, required scientific sections, orthogonality requirements, falsifiability requirements, candidate discipline, success criteria discipline, scientific review gate, VoV example, Dispersion Path-Dependence example, explicit non-goals, and classification.
- Classification appears as `PLATFORM_V2_SCIENTIFIC_STANDARD_APPROVED`.
- No implementation files were changed.
- No formulas were changed.
- No panels were generated or modified.
- No IC was computed or recomputed.
- No validation was run or rerun.
- No governance decision was modified.
- No production file was changed.
- No threshold was changed.
- No ML file was changed.

## SECTION 14 - Final Classification

Final classification:

- `PLATFORM_V2_SCIENTIFIC_STANDARD_APPROVED`

Platform v2 is approved as the scientific research standard for future Project Underdog alpha research modules. Future modules must satisfy the scientific review gate before formula specification or implementation.
