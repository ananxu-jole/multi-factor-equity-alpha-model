# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Discovery Post-Scaffold Review v1

## 1. Executive Summary

This note reviews the completed scaffold implementation for the OHLCV Non-Hostile Transition and Leadership Rotation discovery program. It is review-only. No code was implemented, no candidates were generated, no panels were generated, no discovery was executed, no IC was calculated, no redundancy screening was run, no refinement was run, no validation was run, no governance was modified, no thresholds were changed, nothing was registered to production, and no ML was implemented.

Review scope:

- Scaffold implementation note.
- Frozen implementation plan and discovery specification.
- Scaffold runner.
- Scaffold tests.
- Scaffold artifacts under `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/`.

Scaffold completeness:

The scaffold is complete for the approved post-implementation review boundary. It provides the required runner, allowed modes, artifact tree, manifests, diagnostics placeholders, discovery category listing, and fail-closed unsupported-mode behavior.

Implementation quality:

Implementation quality is sufficient for the next planning step. The runner is intentionally narrow, deterministic, and scaffold-only. It avoids candidate formulas, candidate panels, IC scoring, redundancy execution, refinement, validation, production routing, governance mutation, and ML. Tests cover the main scaffold modes, artifact generation, placeholder status, and fail-closed unsupported modes.

Readiness for candidate generation:

The project is ready to begin a separate candidate-generation design or candidate-concept specification task. This does not authorize candidate generation directly from this note. It means the scaffold faithfully implements the approved design closely enough that the next controlled step can define exploratory concepts.

Major findings:

- Required scaffold modes are implemented.
- Required artifact folders and placeholder reports exist.
- The manifest records `candidate_count = 0` and `research_results_present = false`.
- Guardrails explicitly block discovery, candidate generation, panel generation, IC calculation, redundancy screening, refinement, validation, governance mutation, threshold mutation, production registration, and ML.
- The approved discovery categories remain conceptually aligned with the specification.
- Focused tests and full pytest passed according to the implementation note.

Classification: `READY_FOR_CANDIDATE_GENERATION`.

This classification means ready for a controlled candidate-concept generation task, not ready for panel generation, discovery execution, IC calculation, refinement, validation, production use, governance mutation, or ML.

## 2. Runner Review

Implemented modes:

- `--dry-run`
- `--list-discovery-categories`
- `--validate-scaffold`
- `--validate-artifact-structure`
- `--list-deliverables`

The implemented modes match the scaffold requirement. They support artifact creation, category listing, scaffold validation, artifact-structure validation, and deliverable listing.

Fail-closed behavior:

The runner does not expose execution modes for discovery, candidate generation, panel generation, IC calculation, redundancy screening, refinement, validation, production, governance mutation, or ML. Unsupported modes fail through argument parsing. This is appropriate for scaffold review because it prevents accidental progression beyond the approved boundary.

Unsupported-mode handling:

The test suite checks unsupported examples including `--run-discovery`, `--generate-candidates`, `--generate-panels`, `--calculate-ic`, `--run-refinement`, `--run-validation`, and `--production`. These are expected to return non-zero status. This is a strong scaffold guardrail.

Future extensibility:

The runner is simple enough to extend later, but extension should occur only through a separate approved task. Candidate generation should not be bolted onto the current scaffold without a candidate-generation design or candidate-concept specification. Future additions should preserve:

- explicit mode separation;
- scaffold and execution mode separation;
- artifact namespace separation;
- no production or governance writes;
- no hidden candidate or panel generation in validation modes.

Runner review conclusion:

The runner is complete for scaffold purposes and ready to support the next review-controlled candidate-concept step.

## 3. Artifact Review

Artifact tree reviewed:

- `candidate_inventory/`
- `manifests/`
- `diagnostics/`
- `discovery_summary/`
- `redundancy_screening/`
- `implementation_review/`

The artifact tree matches the required scaffold folders. No candidate-panel, IC-discovery, refinement, validation, production, or ML folders were created by the scaffold.

Manifests:

- `manifests/scaffold_manifest.json`
- `manifests/artifact_manifest.csv`

The scaffold manifest is internally consistent. It records:

- `scaffold_status = SCAFFOLD_ONLY`
- `final_classification = READY_FOR_DISCOVERY_REVIEW`
- `category_count = 8`
- `candidate_count = 0`
- `research_results_present = false`
- prohibited execution fields set to `false`

Diagnostics placeholders:

- `diagnostics/scaffold_diagnostics.csv`
- `diagnostics/guardrail_diagnostics.csv`
- `diagnostics/prohibited_action_diagnostics.csv`

The diagnostics are sufficient for scaffold review. They confirm artifact creation, discovery category declaration, empty candidate inventory, and blocked prohibited actions.

Discovery summary placeholders:

- `discovery_summary/discovery_readiness_report.md`
- `discovery_summary/discovery_summary_placeholder.json`

These are clearly marked as placeholder-only and contain no research results. The readiness report explicitly states that discovery, candidate generation, panel generation, IC calculation, redundancy screening, refinement, validation, governance mutation, production registration, and ML remain blocked.

Implementation review artifacts:

- `implementation_review/implementation_review_placeholder.md`

The placeholder is sufficient for scaffold stage. The completed human-readable implementation note also exists at `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold_implementation_v1.md`.

Artifact review conclusion:

Artifacts are complete and consistent for scaffold purposes. No artifact indicates unauthorized research execution.

## 4. Discovery Category Review

Approved categories:

- orderly leadership emergence
- healthy leadership persistence
- smooth trend handoff
- gradual participation expansion
- rotation acceleration
- rotation deceleration
- volume-confirmed leadership shifts
- healthy breadth transitions

Economic distinctiveness:

The categories remain economically coherent. They focus on orderly capital migration, healthy leadership emergence, trend handoff, participation confirmation, rotation phase, and non-hostile breadth expansion. This aligns with the frozen design and specification.

Conceptual balance:

The categories cover early-transition, transition-confirmation, post-transition persistence, rotation speed, volume confirmation, and breadth expansion. The set is balanced enough to support later candidate-concept generation without forcing the program into one narrow expression.

Independence from existing alpha families:

- Stress repair: The category descriptions avoid hostile, panic, weak-breadth repair, and damage-recovery framing. Hidden stress bias remains a future risk, but it is not embedded in the scaffold.
- Persistence: Healthy leadership persistence has some conceptual adjacency to persistence, but the scaffold description explicitly avoids post-drawdown dependence.
- Rank coherence: Orderly leadership and trend handoff may eventually use rank-derived OHLCV measures, but the category set is broader than rank-turnover resilience.
- Momentum: Leadership emergence and trend handoff can drift into momentum if poorly implemented. The scaffold itself does not create that bias, but future candidate generation must include momentum-overlap controls.

Category review conclusion:

The categories remain sufficiently distinct and balanced for the next candidate-concept step. No category should be removed before candidate generation, but future concept review must watch for hidden momentum and rank-coherence drift.

## 5. Diagnostics Review

Current scaffold diagnostics are sufficient for scaffold validation and review. They confirm:

- artifact tree creation;
- category declaration;
- empty candidate inventory;
- placeholder-only status;
- blocked prohibited actions;
- no research results.

Missing or future diagnostics:

- Candidate balance diagnostics are not yet populated because no candidates exist.
- Concept-level overlap diagnostics are not yet possible because no concepts exist.
- Momentum, persistence, rank-coherence, and stress-repair overlap diagnostics are not yet possible because no candidate panels exist.
- Candidate metadata completeness diagnostics will be needed after candidate-concept generation.

These are not scaffold deficiencies. They are naturally deferred until the project has candidate concepts or panels to review.

Diagnostics review conclusion:

Diagnostics are adequate for scaffold completion. The next task should add candidate-concept review diagnostics, not panel-level or IC-level diagnostics.

## 6. Gap Analysis

| deficiency | severity | does it block candidate generation? | does it require scaffold patch? | review |
| --- | --- | --- | --- | --- |
| No candidate-balance diagnostics populated yet | Minor | No | No | Expected because candidate concepts do not exist yet. |
| No concept-level overlap review artifact yet | Minor | No | No | Should be added during candidate-concept generation/review. |
| No momentum-reference diagnostic yet | Minor | No | No | Cannot be meaningful until candidates or panels exist. |
| No candidate metadata schema yet | Moderate | No, if next task is candidate-concept specification | No | Should be defined in the next candidate-generation task before panels are generated. |
| Artifact root name differs from shortened implementation-plan example but matches required deliverable path | Minor | No | No | Current path matches the user's required artifact root and runner naming. |

Critical deficiencies:

- None.

Moderate deficiencies:

- Candidate metadata schema is not yet frozen. This does not block candidate-concept generation but must be resolved before panel generation.

Minor deficiencies:

- Deferred diagnostics are expected and non-blocking.

Gap analysis conclusion:

No deficiency blocks candidate-concept generation. Candidate panel generation should remain blocked until a candidate inventory, metadata schema, and pre-panel review exist.

## 7. Readiness Assessment

Can Project Underdog safely begin generating exploratory candidate concepts for this family?

Yes, with a precise boundary: Project Underdog can begin a controlled exploratory candidate-concept generation or candidate inventory specification task. The scaffold is complete enough to support that next step because it has:

- a fail-closed runner;
- approved category placeholders;
- artifact and manifest structure;
- guardrail diagnostics;
- tests covering scaffold behavior;
- explicit absence of candidate, panel, discovery, IC, refinement, validation, governance, production, and ML outputs.

Candidate generation is justified only as a concept/registry design step. It should not yet generate panels, calculate IC, run redundancy screening, or execute discovery. The next task should define the candidate inventory, candidate metadata schema, category balance, and conceptual redundancy screen before any panel generation occurs.

Readiness boundary:

- Ready: candidate-concept generation / candidate inventory specification.
- Not ready: panel generation.
- Not ready: IC discovery.
- Not ready: refinement.
- Not ready: validation.
- Not ready: governance or production action.
- Not ready: ML.

## 8. Final Recommendation

1. Is the scaffold complete?

Yes. The scaffold is complete for post-implementation review. It includes the required runner modes, artifact tree, manifests, diagnostics placeholders, discovery category registry, implementation review artifacts, and tests.

2. Are any changes required?

No scaffold patch is required before candidate-concept generation. The only moderate gap is the future candidate metadata schema, which belongs in the next candidate inventory task rather than in the scaffold.

3. Is candidate generation justified?

Yes, candidate-concept generation is justified. This should be limited to generating a controlled exploratory candidate inventory and metadata schema. It should not generate panels, execute discovery, calculate IC, run redundancy screening, refine, validate, mutate governance, register production artifacts, or implement ML.

4. What should the next Codex task be?

The next Codex task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Candidate Concept Generation v1**. It should create a pre-panel candidate concept inventory with 8 to 12 exploratory concepts, category balance, economic thesis, expected distinction from stress repair, persistence, rank coherence, and momentum, and a metadata schema suitable for later review. It should not implement formulas, generate panels, execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, register production artifacts, or implement ML.

## Review Caveat

This review does not authorize discovery execution. It only confirms readiness for a controlled candidate-concept generation step.
