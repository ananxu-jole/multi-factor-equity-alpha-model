# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Discovery Implementation Plan v1

## SECTION 1 - Executive Summary

This note defines the implementation roadmap for the OHLCV-only Non-Hostile Transition and Leadership Rotation discovery program. It translates the frozen specification in `ohlcv_non_hostile_transition_and_leadership_rotation_discovery_specification_v1.md` into a phased implementation plan covering runner structure, artifact organization, diagnostics, review gates, and risk controls.

This is an implementation-planning task only. No code was implemented, no candidate panels were generated, no discovery was executed, no refinement was run, no validation was run, no governance was modified, no thresholds were changed, nothing was registered to production, and no ML was implemented.

Implementation objective:

- Prepare a controlled discovery framework for a new OHLCV-only alpha-family program focused on healthy market transitions and leadership rotation.
- Preserve the economic distinction between non-hostile leadership rotation and existing stress-repair, persistence, rank-coherence, dispersion, and momentum-like families.
- Define the implementation sequence before any code, candidate panel generation, or scoring begins.

Implementation scope:

- Future research-only runner planning.
- Candidate inventory and panel-generation planning.
- Artifact and diagnostics planning.
- Review-gate and risk-control planning.
- Strict no-CRSP/PIT and no-ML boundary preservation.

Expected deliverables:

- A dedicated research-only discovery runner in a later implementation task.
- A candidate inventory structure for 8 to 12 exploratory concepts.
- Candidate panel and metadata artifacts after later authorized panel generation.
- Redundancy screening artifacts before IC discovery.
- Discovery summary and implementation review artifacts.
- Guardrail confirmations showing no governance, production, validation, refinement, or ML activity.

Implementation philosophy:

- Economic-first and small-panel-first.
- Prefer concept diversity over many close variants.
- Fail closed on unsupported modes, metadata dependencies, production routing, and governance mutation.
- Require review checkpoints before each stage advances.
- Treat discovery as research evidence only, not candidate promotion.

## SECTION 2 - Implementation Phases

This document authorizes planning only. It does not authorize implementation, panel generation, discovery scoring, refinement, validation, governance mutation, production registration, or ML.

Phase 1 - Discovery runner implementation:

- Implement a dedicated research-only runner for the program.
- Encode the frozen scope, guardrails, artifact root, runner modes, and registry validation rules.
- Provide scaffold and dry-run behavior before panel generation is allowed.
- Ensure the runner cannot write outside the research artifact namespace.

Phase 2 - Candidate panel generation:

- Generate the approved 8 to 12 exploratory concept panels only after candidate inventory review.
- Write candidate metadata, panel manifest, panel diagnostics, and generation summary.
- Confirm all concepts remain OHLCV-only and do not use PIT metadata, sector/industry labels, peer-relative calculations, or economic-context data.

Phase 3 - Redundancy screening:

- Screen concept metadata before IC discovery.
- Screen generated panels for statistical redundancy after panel generation.
- Compare against stress-repair, persistence, rank-coherence, dispersion, volatility-compression, and momentum-like references where available.
- Recommend a representative scoring subset if duplicate clusters appear.

Phase 4 - IC discovery:

- Score only the approved representative panel.
- Review horizon behavior, active coverage, state attribution, and family-level evidence.
- Do not refine during IC discovery.
- Do not modify governance or production state.

Phase 5 - Refinement eligibility review:

- Review whether any discovery candidate or concept family merits constrained refinement.
- Require economic plausibility, low redundancy, adequate coverage, and distinct state behavior.
- Classify concepts as discovery candidate, diagnostic only, redundant with existing family, or reject research.

Phase 6 - Constrained refinement:

- If justified by a separate review, refine only predeclared discovery survivors.
- Keep variant count small.
- Avoid horizon chasing, state mining, and same-lineage duplication.
- Preserve research-only status.

Phase 7 - Validation:

- If refinement succeeds, design a separate validation package.
- Validation is not part of this implementation plan.
- No candidate can move to production or governance action without a separate process.

## SECTION 3 - Runner Plan

Expected future runner:

`pipelines/run_ohlcv_non_hostile_transition_leadership_rotation_discovery_v1.py`

The exact file name may be adjusted during implementation if repository naming conventions require it, but the runner should remain dedicated to this discovery program.

Expected responsibilities:

- Candidate generation: hold the approved candidate registry and concept metadata once formulas are separately authorized.
- Panel creation: generate candidate panels only in a later authorized panel-generation phase.
- Manifest creation: write candidate inventory, panel manifest, run manifest, and guardrail confirmation artifacts.
- Diagnostics: produce implementation completeness, candidate-balance, artifact-completeness, and guardrail diagnostics.
- Redundancy reporting: produce conceptual, metadata, and statistical redundancy reports before IC scoring proceeds.

Expected initial modes:

- `--describe`: print scope, run id, artifact root, and guardrails.
- `--list-candidates`: list candidate registry after candidates are separately specified.
- `--dry-run`: validate runner configuration and artifact scaffold without generating panels.
- `--validate-registry`: validate candidate inventory structure once a registry exists.
- `--validate-artifacts`: validate expected artifact paths and required placeholder/report files.
- `--run-panel-generation`: future mode only after candidate panel generation is authorized.
- `--run-redundancy-screening`: future mode only after panels exist.
- `--run-ic-discovery`: future mode only after redundancy review approves the scoring subset.

Unsupported modes must fail closed:

- No production.
- No validation.
- No refinement.
- No ingestion.
- No metadata construction.
- No lineage construction.
- No ML.
- No portfolio routing.
- No governance mutation.

Runner guardrails:

- Require `research_status = RESEARCH_ONLY` for all candidates.
- Enforce OHLCV-only metadata declaration.
- Enforce artifact writes under the research artifact root.
- Emit a no-governance/no-production/no-ML confirmation in the manifest.
- Refuse candidate counts outside the approved 8 to 12 range unless a later planning note updates the scope.

## SECTION 4 - Artifact Plan

Planned artifact root:

`artifacts/research/ohlcv_non_hostile_transition_leadership_rotation_discovery_v1/`

Expected artifact organization:

`candidate_inventory/`

- `candidate_inventory.csv`
- `candidate_category_balance.csv`
- `candidate_registry_schema_check.csv`
- `candidate_inventory_review.md`

`candidate_panels/`

- Future candidate panel files.
- Future candidate metadata files.
- No panels should exist before authorized panel generation.

`manifests/`

- `run_manifest.json`
- `panel_manifest.csv`
- `guardrail_manifest.json`
- `artifact_manifest.csv`

`diagnostics/`

- `implementation_completeness_diagnostics.csv`
- `artifact_completeness_diagnostics.csv`
- `candidate_balance_diagnostics.csv`
- `guardrail_diagnostics.csv`
- `prohibited_dependency_review.csv`

`redundancy/`

- `conceptual_redundancy_review.csv`
- `metadata_redundancy_report.csv`
- `statistical_redundancy_report.csv`
- `reference_family_overlap_report.csv`
- `approved_scoring_subset_recommendation.csv`

`discovery/`

- `ic_discovery_summary.csv`
- `candidate_horizon_scores.csv`
- `daily_ic_by_candidate_horizon.csv`
- `family_category_summary.csv`
- These files are future IC discovery outputs and should not exist until IC discovery is separately authorized.

`review/`

- `implementation_review.md`
- `discovery_readiness_review.md`
- `redundancy_review.md`
- `ic_discovery_review.md`
- `refinement_eligibility_review.md`

Expected major artifacts:

- Candidate inventory.
- Panel manifest.
- Discovery summary.
- Redundancy report.
- Diagnostics.
- Candidate metadata.
- Implementation review.

Artifact principle:

- Scaffold and diagnostic artifacts may be created during implementation.
- Candidate panels and IC outputs must remain absent until the relevant phase is explicitly authorized.

## SECTION 5 - Candidate Balance Plan

The planned discovery inventory should contain 8 to 12 exploratory concepts.

Preferred initial balance:

| category | target concepts | role |
| --- | ---: | --- |
| orderly leadership emergence | 1-2 | Core early-leadership thesis. |
| healthy leadership persistence | 1-2 | Tests durable leadership after non-hostile transition. |
| smooth trend handoff | 1-2 | Tests transition quality rather than raw trend strength. |
| gradual participation expansion | 1-2 | Tests orderly demand formation without stress repair. |
| rotation acceleration | 1 | Tests early acceleration in capital migration. |
| rotation deceleration | 1 | Tests late-stage or slowing leadership migration. |
| volume-confirmed leadership shifts | 1-2 | Tests whether participation confirms transition quality. |
| healthy breadth transitions | 1 | Tests non-hostile broadening behavior. |

Balance rules:

- At least 4 categories must be represented.
- No single category may exceed 2 close concepts in the initial panel.
- The full panel should include at least one leadership-emergence concept, one trend-handoff concept, one participation or volume-confirmation concept, and one rotation-pace or breadth-transition concept.
- Diagnostic controls should be minimized and clearly labeled.

Expected diversity:

- Concepts should vary by mechanism, not merely by window length.
- Concepts should vary between early-transition, transition-confirmation, and post-transition-persistence behavior.
- Concepts should not cluster around one rank, volume, or trend expression.

Avoided imbalances:

- Do not let the panel become a rank-coherence sibling batch.
- Do not let the panel become participation repair.
- Do not let the panel become ordinary momentum.
- Do not let the panel become volatility compression or stress absorption.

## SECTION 6 - Anti-Redundancy Controls

Overlap with momentum:

- Require every concept to describe transition quality or leadership handoff, not merely recent strength.
- Include momentum-like reference diagnostics where available.
- Flag concepts whose expected behavior is indistinguishable from raw trend continuation.

Overlap with persistence:

- Prohibit post-drawdown activation as a primary mechanism.
- Compare future candidate panels against persistence conditional candidates.
- Flag concepts that primarily reward rank stability without transition or leadership-handoff logic.

Overlap with rank coherence:

- Avoid using low rank churn or rank-turnover resilience as the whole thesis.
- Require leadership emergence, handoff, breadth, participation, or rotation-phase content.
- Compare future outputs against rank-coherence conditional candidates.

Overlap with stress repair:

- Prohibit hostile, panic, weak-breadth, stress-repair, and damage-recovery framing as primary activation logic.
- Include stress-repair anchor comparisons in redundancy review.
- Require state attribution to confirm that positive evidence is not dominated by hostile/recovery states.

Conceptual screening principles:

- Each concept must have a one-paragraph economic thesis.
- Each concept must state its expected distinction from stress repair, persistence, rank coherence, and momentum.
- Concepts failing this screen should be revised before panel generation or rejected from the initial panel.

Implementation controls:

- Candidate registry should include `category`, `mechanism_thesis`, `expected_distinction`, `known_overlap_risks`, and `prohibited_dependencies`.
- Redundancy artifacts should be generated before IC scoring.
- Highly redundant candidates should be held back from scoring or treated as diagnostic siblings.

## SECTION 7 - Diagnostics Plan

Implementation diagnostics:

- Candidate counts by category.
- Candidate count versus approved 8 to 12 range.
- Required metadata field completeness.
- Artifact path completeness.
- Runner mode availability.
- Guardrail confirmation.

Category coverage diagnostics:

- Number of represented categories.
- Maximum concepts per category.
- Required category coverage flags.
- Diagnostic-control count.
- Balance warning if one category dominates.

Redundancy coverage diagnostics:

- Conceptual redundancy coverage.
- Metadata redundancy coverage.
- Statistical redundancy coverage after panels exist.
- Reference-family overlap coverage.
- Momentum-like overlap coverage where available.

Implementation completeness diagnostics:

- Runner scaffold exists.
- Artifact root exists.
- Required folders exist.
- Manifest files exist.
- Candidate inventory exists when candidate specification is authorized.
- No forbidden output folders are written.

Artifact completeness diagnostics:

- Candidate inventory present.
- Panel manifest present after panel generation.
- Redundancy reports present after redundancy phase.
- Discovery summaries present after IC discovery.
- Review notes present at each checkpoint.

No IC diagnostics yet:

- This implementation plan does not define IC result diagnostics.
- IC diagnostics belong to the later discovery execution and review phases.

## SECTION 8 - Review Gates

Implementation review:

- Confirms runner scaffold, artifact root, manifest outputs, diagnostics, and guardrails.
- Confirms no candidate formulas or panels were generated unless separately authorized.

Discovery readiness review:

- Confirms candidate inventory balance, metadata completeness, prohibited-dependency review, and concept-screening pass.
- Confirms candidate panel generation can proceed.

Redundancy review:

- Confirms conceptual and metadata redundancy before scoring.
- Confirms statistical redundancy after panel generation.
- Defines approved scoring subset or holdback list.

IC discovery review:

- Reviews discovery results after IC scoring.
- Determines whether any concept produced credible research evidence.
- Does not refine or validate.

Refinement eligibility review:

- Determines whether any discovery candidate merits constrained refinement.
- Requires distinct mechanism, adequate coverage, manageable redundancy, and plausible horizon behavior.
- Does not run refinement.

No execution:

- This note freezes review checkpoints only.
- Each phase requires separate authorization before execution.

## SECTION 9 - Risks

Implementation drift:

- Risk: the runner or artifacts may expand beyond the frozen OHLCV-only scope.
- Mitigation: encode guardrails in runner manifests, diagnostics, and review notes.

Concept imbalance:

- Risk: the panel may overrepresent leadership persistence, rank behavior, or volume confirmation.
- Mitigation: enforce category coverage and maximum concepts per category.

Accidental redundancy:

- Risk: concepts may become close variants of rank-coherence, persistence, or stress-repair candidates.
- Mitigation: require pre-scoring redundancy review and reference-family overlap diagnostics.

Hidden momentum bias:

- Risk: leadership emergence may become recent-strength momentum.
- Mitigation: require economic thesis review and momentum-like reference comparison where available.

Hidden stress bias:

- Risk: positive evidence may concentrate in recovery or stress-normalization states.
- Mitigation: require state attribution and stress-repair anchor comparisons before refinement eligibility.

False readiness:

- Risk: implementation completion may be mistaken for discovery evidence.
- Mitigation: separate implementation review from panel generation, redundancy screening, IC discovery, refinement, and validation.

Research sprawl:

- Risk: the program may add too many concepts to cover every leadership-transition idea.
- Mitigation: cap initial concepts at 8 to 12 and require a later scope review for expansion.

## SECTION 10 - Final Recommendation

1. Is the implementation sequence complete?

Yes. The sequence covers discovery runner implementation, candidate panel generation, redundancy screening, IC discovery, refinement eligibility review, constrained refinement, and validation, with explicit review gates between phases.

2. Are implementation risks adequately controlled?

Yes, at the planning level. The plan defines OHLCV-only guardrails, candidate-balance controls, redundancy screening, artifact separation, and fail-closed boundaries against CRSP/PIT, governance, production, validation, refinement, and ML drift.

3. Is the project ready to implement the discovery program?

Yes, for implementation of the research-only discovery scaffold and diagnostics. The project is not yet authorized to generate candidate panels, execute discovery, run refinement, run validation, mutate governance, register production artifacts, or implement ML.

4. What should the next Codex task be?

The next Codex task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Discovery Scaffold Implementation v1**. It should implement the research-only runner scaffold, artifact tree, manifests, diagnostics placeholders, guardrail checks, and tests. It should not define formulas, generate candidate panels, execute discovery, run refinement, run validation, modify governance, register production artifacts, or implement ML.

## Planning Caveat

This note is planning-only. It does not implement code, create alpha candidates, generate panels, execute discovery, execute refinement, execute validation, modify governance, change thresholds, register production candidates, or implement ML.
