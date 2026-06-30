# Project Underdog - Standard Research Module Lifecycle and Governance Standard v1

## SECTION 1 - Purpose And Authority

This document defines the permanent Project Underdog research methodology for future alpha research modules.

Classification:

- `PROJECT_STANDARD_APPROVED`

This standard is authoritative for all future research modules unless superseded by a later approved Project Underdog standard. It converts the lessons from completed research cycles into a repeatable governance process that separates research planning, implementation, panel construction, IC discovery, research review, governance decision, and master-state update.

This is a governance standard only. No implementation, panel generation, IC computation, discovery, refinement, validation, production registration, threshold change, external access, metadata ingestion, or ML work was performed.

## SECTION 2 - Materials Reviewed

Core project-state notes reviewed:

- `project_underdog_master_status_recap_2026-06-17.md`
- `project_underdog_research_state_audit_v1.md`
- `candidate_consolidation_workplan_v1.md`
- `alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`

Representative module patterns reviewed:

- OHLCV Non-Hostile Transition and Leadership Rotation lifecycle, including design, implementation, panel generation, panel audit, IC discovery, and negative-result review.
- OHLCV Volatility-of-Volatility lifecycle, including frontier selection, design, formula specification, implementation, implementation review, panel specification, panel generation, and panel audit.
- PIT governance architecture work, including source-gate planning, source evidence review, license dependency closeout, and explicit pause pending external evidence.

## SECTION 3 - Research Module Definition

A Project Underdog research module is a bounded, research-only unit that tests one primary alpha mechanism or tightly coordinated mechanism family through a governed lifecycle.

Required module properties:

- One primary mechanism thesis.
- Explicit data dependency class, such as OHLCV-only, PIT-metadata-dependent, or diagnostic-only.
- A predeclared candidate set.
- A frozen formula and panel specification before implementation.
- Separate implementation review before panel generation.
- Separate panel audit before IC discovery.
- IC discovery separated from research review and governance decision.
- Clear non-goals and fail-closed guardrails.

A research module is not:

- a broad search sweep;
- a production registration path;
- an ML experiment;
- a governance threshold change;
- a portfolio construction task;
- a validation task unless explicitly scoped as validation after research review.

## SECTION 4 - Candidate Limits And Scope Discipline

Default candidate limits:

- One primary mechanism per module.
- Approximately 4 to 6 candidates per module.
- More than 6 candidates requires explicit design-stage justification.
- More than 10 candidates requires a separate governance exception note.
- One refinement cycle maximum unless explicitly approved after a research review.

Candidate design rules:

- One candidate equals one interpretable mechanism.
- Do not mix every available mechanism into every candidate.
- Avoid duplicating existing hostile/stress repair, volatility compression, persistence/rank-coherence, volume shock reversal, plain reversal, momentum, or simple dispersion anchors unless the module is explicitly a contamination diagnostic.
- Predeclare primary and secondary horizons.
- Predeclare expected sign.
- Predeclare contamination references.
- Freeze candidate IDs before implementation.

Candidate family size should be small enough that a negative result is interpretable and a positive result can be audited.

## SECTION 5 - Required Lifecycle

Every research module must follow this phase sequence:

1. Phase 0 - Research Frontier Selection
2. Phase 1 - Research Module Design
3. Phase 2 - Formula & Panel Specification
4. Phase 3 - Implementation
5. Phase 4 - Implementation Review
6. Phase 5 - Panel Specification
7. Phase 6 - Panel Generation
8. Phase 7 - Panel Audit
9. Phase 8 - IC Discovery
10. Phase 9 - Research Review
11. Phase 10 - Governance Decision
12. Phase 11 - Master Research State Update

No phase may be skipped. A later phase may be blocked or parked, but the reason must be documented.

## SECTION 6 - Phase Standards

### Phase 0 - Research Frontier Selection

Objective:

- Select the highest-value next research frontier relative to the current inventory, failed mechanisms, blockers, and available data.

Required inputs:

- Master status recap.
- Research state audit.
- Candidate consolidation workplan.
- Alpha family inventory or frontier reassessment notes.
- Major completed family outcomes.

Required outputs:

- Ranked frontier table.
- Exactly one recommended next research frontier.
- Readiness classification.

Deliverables:

- Research note under `docs/research_notes/`.

Required verification:

- Confirm no implementation, panel generation, IC, validation, governance mutation, production change, threshold change, or ML work occurred.

Required artifacts:

- Documentation only unless a manifest-only review is explicitly requested.

Exit criteria:

- One frontier is selected and classified as ready, ready with risks, or blocked.

Blocking conditions:

- Frontier depends on unavailable external data or unresolved license blockers.
- Frontier is redundant with a recently saturated family.
- Research inventory is too unstable to justify new discovery.

Non-goals:

- Candidate formulas.
- Implementation.
- IC.
- Refinement.

### Phase 1 - Research Module Design

Objective:

- Translate the selected frontier into a bounded module design and candidate concept space.

Required inputs:

- Phase 0 frontier note.
- Current research state.
- Candidate consolidation notes.
- Successful and parked family outcomes.

Required outputs:

- Mechanism motivation.
- Candidate concept groups.
- Expected orthogonality.
- Overlap risks.
- State dependence.
- Horizons of interest.
- Failure modes.
- Staged roadmap.

Deliverables:

- Design note under `docs/research_notes/`.

Required verification:

- Confirm design-only status and no code or research artifacts changed.

Required artifacts:

- Documentation only.

Exit criteria:

- Candidate design space is narrow enough for formula specification.

Blocking conditions:

- Mechanism cannot be separated from known references.
- Candidate budget is too broad.
- Required data are unavailable.

Non-goals:

- Exact formulas.
- Panel generation.
- IC.

### Phase 2 - Formula & Panel Specification

Objective:

- Freeze candidate IDs, formulas, raw inputs, derived features, horizons, expected sign, panel schema, artifact plan, and stop conditions before implementation.

Required inputs:

- Phase 1 design note.
- Current alpha inventory and consolidation references.
- Prior successful and parked family notes as needed.

Required outputs:

- Candidate ID table.
- Formula table.
- Required input schema.
- Derived feature definitions.
- Panel output schema.
- Artifact path plan.
- Warmup, missing-data, date-alignment, ranking, and z-score rules.
- Contamination and redundancy controls.
- Stop conditions.

Deliverables:

- Formula and panel specification note under `docs/research_notes/`.

Required verification:

- Confirm every candidate is specified.
- Confirm classification appears.
- Confirm no implementation, panels, IC, validation, governance, production, threshold, or ML files changed.

Required artifacts:

- Documentation only.

Exit criteria:

- Specification is ready for implementation or explicitly ready with research risks.

Blocking conditions:

- Candidate IDs are not frozen.
- Formulas are ambiguous.
- Same-bar timing or PIT semantics are unresolved.
- Panel schema is not auditable.

Non-goals:

- Formula implementation.
- Candidate execution.
- IC.

### Phase 3 - Implementation

Objective:

- Implement only the approved candidate formulas and registry-derived definitions from the frozen specification.

Required inputs:

- Phase 2 formula and panel specification.
- Current governance documents.
- Existing local helper APIs and patterns.

Required outputs:

- Research module code.
- Registry-derived candidate definitions.
- Formula implementation.
- Derived features.
- Warmup, missing-data, date-alignment, and schema handling.
- Focused implementation tests.
- Implementation note.

Deliverables:

- Module code under the appropriate research pipeline/module path.
- Focused tests.
- Implementation note under `docs/research_notes/`.

Required verification:

- `python -m py_compile` for changed Python files.
- Focused module tests.
- Relevant registry/scaffold tests.
- Confirmation no panels, IC, discovery, validation, governance mutation, production change, threshold change, or ML occurred.

Required artifacts:

- No research result artifacts unless explicitly implementation-manifest-only.

Exit criteria:

- Implementation compiles, tests pass, and implemented candidate IDs exactly match the approved specification.

Blocking conditions:

- Extra candidates implemented.
- Candidate formulas drift from specification.
- Warmup or missing-data behavior creates look-ahead or hidden fills.
- Implementation mutates governance or production files.

Non-goals:

- Panel writing.
- IC.
- Refinement.
- Validation.

### Phase 4 - Implementation Review

Objective:

- Independently review the implementation before any panel writing.

Required inputs:

- Phase 3 module code.
- Phase 3 tests.
- Phase 3 implementation note.
- Phase 2 specification.

Required outputs:

- Readiness conclusion.
- Review findings.
- Canonical ID decision.
- Formula/spec match assessment.
- Same-bar timing review.
- Panel shape recommendation.
- Blocking issues and minor review items.

Deliverables:

- Implementation review note under `docs/research_notes/`.

Required verification:

- Compile check.
- Focused implementation tests.
- Relevant scaffold/registry tests.
- Confirmation no panel generation, IC, discovery, validation, governance, production, threshold, or ML changes.

Required artifacts:

- Documentation only unless small review fixes are explicitly required.

Exit criteria:

- Implementation is approved for panel specification, or minor items are documented and bounded.

Blocking conditions:

- Formula mismatch.
- Unauthorized candidates.
- Look-ahead risk.
- Missing tests for core formula behavior.

Non-goals:

- Panel writing.
- IC.
- Candidate status decisions.

### Phase 5 - Panel Specification

Objective:

- Freeze the panel-generation contract before any panel-writing implementation.

Required inputs:

- Phase 4 implementation review.
- Phase 3 implementation note.
- Phase 2 formula and panel specification.

Required outputs:

- Canonical panel schema.
- Metadata JSON schema.
- Panel manifest schema.
- Artifact directory structure.
- Activation-neutralization semantics.
- Timing policy.
- Warmup and missing-data rules.
- Duplicate prevention.
- Identifier policy.
- Validation rules.
- Stop conditions before panel generation.

Deliverables:

- Panel specification note under `docs/research_notes/`.

Required verification:

- Confirm required sections and classification.
- Confirm no implementation or research artifacts changed.

Required artifacts:

- Documentation only.

Exit criteria:

- Panel writer can be implemented without interpretation.

Blocking conditions:

- Panel grain is ambiguous.
- Missing-data semantics are ambiguous.
- Timing policy is not explicit.
- Artifact root or manifest fields are not frozen.

Non-goals:

- Panel generation.
- IC.
- Research review.

### Phase 6 - Panel Generation

Objective:

- Serialize approved candidate outputs into research panel artifacts exactly according to the frozen panel specification.

Required inputs:

- Phase 5 panel specification.
- Phase 4 implementation review.
- Phase 3 implementation.
- Approved local source data.

Required outputs:

- Candidate panel artifacts.
- Metadata JSON.
- Panel manifest.
- Panel generation summary.
- Schema validation report.
- Panel generation manifest.
- Panel generation note.

Deliverables:

- Research panel artifacts under `artifacts/research/<module_id>/panel_v1/`.
- Panel-generation runner or approved serialization code.
- Focused panel-generation tests.
- Panel generation note under `docs/research_notes/`.

Required verification:

- Compile check.
- Focused panel tests.
- Module tests.
- Registry/scaffold tests.
- Artifact validate-only mode when available.
- Confirmation no IC, discovery, refinement, validation, governance mutation, production change, threshold change, or ML occurred.

Required artifacts:

- Per-candidate panel files or one canonical panel, as specified.
- `metadata.json`.
- `panel_manifest.csv` or `panel_manifest.json`.
- `panel_generation_summary.csv`.
- `panel_generation_manifest.json`.
- `schema_validation_report.csv`.
- Candidate registry and formula manifest where applicable.

Exit criteria:

- All approved panels are generated and validate cleanly.

Blocking conditions:

- Unexpected candidate IDs.
- Duplicate panel keys.
- Schema mismatch.
- Manifest mismatch.
- Family leakage from unrelated modules.
- Any IC or discovery output produced in the same task.

Non-goals:

- IC.
- Discovery.
- Research validation.
- Governance decision.

### Phase 7 - Panel Audit

Objective:

- Audit generated panels before IC discovery.

Required inputs:

- Phase 6 panel artifacts.
- Phase 6 panel generation note.
- Phase 5 panel specification.
- Phase 4 implementation review.

Required outputs:

- Artifact inventory.
- Manifest-to-parquet reconciliation.
- Metadata and identifier audit.
- Long-form or wide-form schema audit.
- Duplicate key audit.
- Warmup and missing-data audit.
- Activation and timing audit.
- Determinism and reproducibility assessment.
- Approval or rejection for IC discovery.

Deliverables:

- Panel audit note under `docs/research_notes/`.

Required verification:

- Artifact validate-only mode.
- Focused panel tests.
- Module tests.
- Relevant registry/scaffold tests.
- Confirmation panels were not rewritten unless a blocking defect was explicitly fixed.

Required artifacts:

- Documentation only, unless a blocking repair is separately authorized and documented.

Exit criteria:

- Panels are approved for IC discovery, approved with minor notes, or not approved.

Blocking conditions:

- Missing panel files.
- Manifest mismatch.
- Duplicate keys.
- Incorrect timing policy.
- Missing source lineage.
- Family leakage.

Non-goals:

- IC.
- Candidate research validation.
- Governance decision.

### Phase 8 - IC Discovery

Objective:

- Compute predeclared IC diagnostics for audited panels.

Required inputs:

- Phase 7 panel audit approval.
- Approved panel artifacts.
- Approved forward-return source and horizon definitions.
- Frozen candidate and horizon list.

Required outputs:

- Candidate horizon IC scores.
- Daily IC by candidate and horizon.
- Horizon and family summaries.
- Candidate rankings.
- Rolling/window diagnostics.
- Guardrail manifest.
- IC discovery note.

Deliverables:

- IC artifacts under `artifacts/research/<module_id>/ic_discovery_v1/`.
- IC discovery note under `docs/research_notes/`.

Required verification:

- Compile/test checks for IC runner.
- Input panel manifest match.
- Horizon alignment checks.
- Confirmation no refinement, validation, governance mutation, production registration, threshold change, or ML occurred.

Required artifacts:

- `daily_ic.csv`.
- `candidate_horizon_ic_scores.csv`.
- `candidate_ic_summary.csv`.
- `horizon_summary.csv`.
- `family_summary.csv`.
- `candidate_rankings.csv`.
- `rolling_ic_diagnostics.csv`.
- `approved_panel_manifest.csv`.
- `manifest.json`.

Exit criteria:

- IC results are complete and classified for research review.

Blocking conditions:

- Panel audit absent.
- Forward returns start on or before signal date.
- Candidate or horizon mismatch.
- IC task begins refining or validating candidates.

Non-goals:

- Refinement.
- Validation.
- Governance decision.

### Phase 9 - Research Review

Objective:

- Interpret IC discovery results and decide whether the family or candidates merit refinement, watch status, diagnostics, or parking.

Required inputs:

- Phase 8 IC artifacts.
- Phase 8 IC discovery note.
- Prior family benchmarks and contamination references.
- Current research inventory.

Required outputs:

- Candidate-level interpretation.
- Family-level interpretation.
- Horizon pattern assessment.
- Redundancy and contamination assessment.
- Overfitting and concentration risks.
- Recommended governance outcome per candidate or family.

Deliverables:

- Research review note under `docs/research_notes/`.

Required verification:

- Confirm required IC artifacts exist.
- Confirm no new IC, refinement, validation, panel rewrite, governance mutation, production registration, threshold change, or ML occurred.

Required artifacts:

- Documentation only unless review-only summary tables are explicitly produced.

Exit criteria:

- Clear recommendation for Phase 10 governance decision.

Blocking conditions:

- IC artifacts incomplete.
- Results are interpreted without checking horizon concentration or redundancy risk.
- Review attempts to promote candidates directly.

Non-goals:

- Candidate validation.
- Production registration.
- Threshold changes.

### Phase 10 - Governance Decision

Objective:

- Assign official research-governance outcomes based on the research review.

Required inputs:

- Phase 9 research review.
- Candidate consolidation standards.
- Current master research state.
- Relevant validation-readiness standards.

Required outputs:

- Candidate or family governance outcome.
- Required evidence for next step.
- Explicit blocked work.
- Approval or rejection of refinement, validation-review eligibility, watch status, diagnostic status, or parking.

Deliverables:

- Governance decision note under `docs/research_notes/`.

Required verification:

- Confirm no unapproved implementation, IC, validation, production, threshold, or ML changes occurred.

Required artifacts:

- Documentation-only governance decision unless manifest-only governance artifacts are explicitly requested.

Exit criteria:

- Every candidate or family receives a standard outcome.

Blocking conditions:

- Evidence is insufficient to classify.
- Candidate status would conflict with prior governance without explicit rationale.
- Production implications are introduced.

Non-goals:

- Production registration.
- Portfolio construction.
- ML.

### Phase 11 - Master Research State Update

Objective:

- Update the project-level research map so future work begins from the correct state.

Required inputs:

- Phase 10 governance decision.
- Phase 9 research review.
- Current master status recap or research inventory.
- Candidate consolidation notes as applicable.

Required outputs:

- Updated inventory status.
- Updated active, watch, parked, diagnostic, and blocked lists.
- Updated recommended next task.
- Updated blockers and guardrails.

Deliverables:

- Master research state update or recap note under `docs/research_notes/`.

Required verification:

- Confirm the update is documentation-only unless a separately approved state artifact update is requested.
- Confirm no production registry or governance threshold files changed.

Required artifacts:

- Documentation-only, unless a governed inventory artifact is explicitly in scope.

Exit criteria:

- Future research tasks can cite one current state-of-record note.

Blocking conditions:

- Governance decision not complete.
- Candidate statuses are inconsistent across notes.
- Blocked external dependencies are ignored.

Non-goals:

- New discovery.
- Validation.
- Production changes.

## SECTION 7 - Governance Outcomes

Standard candidate or family outcomes:

| outcome | meaning | required evidence | allowed next step |
| --- | --- | --- | --- |
| `ADVANCE` | Evidence justifies the next research lifecycle phase, such as refinement eligibility review, validation-readiness review, or IC discovery after panel audit. | Positive primary-horizon evidence, acceptable data integrity, no blocking contamination, and documented review. | Proceed only to the named next phase. |
| `WATCH` | Evidence is promising but carries unresolved risks such as horizon concentration, recent-window weakness, turnover, sparse activation, or redundancy. | Positive or useful evidence plus explicit watch reasons and monitoring criteria. | Monitoring, focused diagnostics, or a bounded review. No promotion. |
| `PARK` | Evidence is negative, blocked, externally dependent, or not worth active continuation under current assumptions. | Clear reason such as broad negative IC, license blocker, data readiness blocker, or mechanism failure. | Archive, pause, or design-only diagnostic if explicitly justified. |
| `DIAGNOSTIC` | Result or candidate is useful as a reference, failure-mode clue, contamination benchmark, or sensitivity check but not a candidate for advancement. | Documented interpretive value without sufficient candidate evidence. | Use as a reference in future reviews. No validation or promotion. |

Outcome constraints:

- `ADVANCE` never means production-ready.
- `WATCH` never means validation-ready.
- `PARK` does not delete evidence; it archives it.
- `DIAGNOSTIC` must not become stealth refinement.

## SECTION 8 - Required Independent Reviews

Independent review is required before continuing after these phases:

- Phase 4 Implementation Review before panel specification or panel generation.
- Phase 7 Panel Audit before IC discovery.
- Phase 9 Research Review before governance decision.
- Phase 10 Governance Decision before master state update or validation-readiness work.

Additional review is mandatory when:

- External licensed data or PIT metadata is involved.
- A family has broad negative evidence but possible inversion behavior.
- A candidate is highly correlated with an existing research anchor.
- A candidate would change inventory status.
- Any refinement cycle beyond one pass is proposed.
- Any validation-readiness claim is proposed.

## SECTION 9 - Artifact Conventions

Standard artifact root:

- `artifacts/research/<module_id>/`

Recommended subdirectories:

- `design_v1/` for optional manifest-only design inventories.
- `implementation_v1/` for implementation manifests if needed.
- `panel_v1/` for panel artifacts.
- `ic_discovery_v1/` for IC artifacts.
- `research_review_v1/` for review-only summaries if needed.
- `refinement_v1/` for one approved refinement cycle.
- `validation_review_v1/` for validation-readiness review.

Standard panel artifacts:

- Candidate panel parquet files or one canonical panel parquet.
- `metadata.json`.
- `panel_manifest.csv` or `panel_manifest.json`.
- `panel_generation_summary.csv`.
- `panel_generation_manifest.json`.
- `schema_validation_report.csv`.
- `candidate_registry.csv`.
- `candidate_formula_manifest.csv`.
- `input_schema.csv`.
- `derived_feature_manifest.csv`.

Standard IC artifacts:

- `daily_ic.csv`.
- `candidate_horizon_ic_scores.csv`.
- `candidate_ic_summary.csv`.
- `horizon_summary.csv`.
- `family_summary.csv`.
- `candidate_rankings.csv`.
- `rolling_ic_diagnostics.csv`.
- `approved_panel_manifest.csv`.
- `manifest.json`.

Standard metadata fields:

- `run_id`.
- `module_id`.
- `spec_id`.
- `candidate_ids`.
- `source_spec_id`.
- `family`.
- `research_status`.
- `timing_policy`.
- `panel_generation_executed`.
- `ic_scoring_executed`.
- `discovery_executed`.
- `refinement_executed`.
- `validation_executed`.
- `governance_modified`.
- `production_registration`.
- `thresholds_modified`.
- `ml_integration`.

All forbidden-action flags must be fail-closed and explicit.

## SECTION 10 - Naming Conventions

Module IDs:

- Use lowercase snake case.
- Include mechanism family and lifecycle target.
- Example: `ohlcv_volatility_of_volatility_research_module_v1`.

Candidate IDs:

- Use short, stable, lowercase IDs for code and artifacts.
- Use descriptive `source_spec_id` for formula lineage.
- Example: `vov_01` with `source_spec_id = vov_01_instability_calm_after_chop`.

Research notes:

- Use descriptive lowercase snake case with version suffix.
- Example: `ohlcv_volatility_of_volatility_research_module_panel_audit_v1.md`.

Artifact directories:

- Use `<module_id>/<phase_v#>/`.
- Avoid ambiguous shared directories for unrelated modules.

Classifications:

- Use uppercase snake case.
- Classification must appear in every lifecycle note.

## SECTION 11 - Required Guardrails

Universal guardrails:

- No look-ahead.
- PIT discipline for any identity, metadata, or classification feature.
- No static-snapshot metadata for alpha validation.
- No source data access without license and entitlement evidence.
- No production contamination.
- No production registry changes.
- No threshold changes during research modules.
- No ML during discovery.
- Research-only execution unless a later phase explicitly says otherwise.
- No panel writing before panel specification.
- No IC before panel audit.
- No refinement during IC discovery.
- No validation during discovery or research review.
- No candidate promotion without governance decision.

Timing guardrails:

- Signal date `t` may use only information available at or before the declared availability time.
- If OHLCV through close `t` is used, signals are after-close and forward returns must start strictly after `t`.
- Same-bar intraday assumptions must be explicitly prohibited unless separately designed and reviewed.

PIT metadata guardrails:

- Known-date semantics must be documented.
- Effective dates and source availability dates must not be conflated.
- Ticker lineage, delisting, security identity, sector, industry, peer group, and size metadata require source lineage before alpha use.
- License, entitlement, retention, archive, and reproducibility policies are prerequisites for ingestion.

## SECTION 12 - Quality Standards

Documentation standards:

- Every phase must have a note.
- Every note must include objective, scope, classification, non-goals, verification, and next-step recommendation.
- Reviews must distinguish evidence from inference.
- Negative results must be archived, not hand-waved.

Test standards:

- Implementation phases require focused tests.
- Panel generation requires schema, metadata, manifest, duplicate-prevention, timing, and activation/missing-data tests.
- IC discovery requires horizon-alignment and input-manifest tests.
- Registry or scaffold tests must be run when candidate identity or module inventory is involved.

Audit standards:

- Audit artifacts must reconcile manifests to actual files.
- Duplicate keys must be checked.
- Candidate ID and source-spec lineage must be checked.
- Guardrail flags must be inspected.
- Artifact validation must be deterministic and repeatable.

Reproducibility standards:

- Artifact roots must be deterministic.
- Source paths or source references must be recorded.
- Candidate registry and formula manifest must be preserved.
- Metadata must include fail-closed guardrail flags.
- Reruns must not overwrite non-draft artifacts without explicit approval.

## SECTION 13 - Refinement Standard

Refinement is not automatic.

Refinement is allowed only after:

- IC discovery is complete.
- Research review identifies a candidate or family with positive evidence.
- Redundancy and contamination risks are bounded.
- Governance decision explicitly authorizes a refinement eligibility or design phase.

Default refinement limit:

- One refinement cycle maximum.

Refinement must:

- Preserve the original mechanism.
- Use a small predeclared variant set.
- Include original anchors where useful.
- Avoid parameter mining.
- Avoid adding unrelated mechanisms.
- End with a research review and governance decision.

Refinement must not:

- rescue a broadly negative family without an explicitly separate diagnostic design;
- become validation;
- change production registry;
- change thresholds;
- introduce ML.

## SECTION 14 - Validation And Production Boundary

Discovery evidence is not validation evidence.

Validation-readiness requires:

- A completed research review.
- A governance decision authorizing validation-readiness review.
- Evidence of panel integrity.
- Evidence of formula stability.
- Evidence of redundancy and contamination review.
- Evidence that the candidate is not merely a duplicate of an existing anchor.

Production work requires a separate production-governance process and is outside standard research-module discovery. No research module may register production candidates, modify production registries, change thresholds, or imply portfolio construction readiness.

## SECTION 15 - PIT And External Dependency Standard

Any module depending on PIT metadata, security master, ticker lineage, sector/industry, peer group, fundamentals, or external licensed data must complete an external evidence gate before implementation.

Required evidence:

- License.
- Entitlement.
- Field inventory.
- Table inventory.
- Retention policy.
- Archive requirements.
- Reproducibility policy.
- Known-date semantics.

If evidence is missing, the correct outcome is `PARK` or external dependency pause, not placeholder implementation.

The PIT implementation order remains:

1. Security Master
2. Ticker Lineage
3. Economic Metadata
4. Peer Groups
5. Alpha Discovery

## SECTION 16 - Standard Classifications By Phase

Common readiness classifications:

| phase | example classifications |
| --- | --- |
| Frontier selection | `NEXT_DISCOVERY_PROGRAM_READY`, `NEXT_DISCOVERY_PROGRAM_READY_WITH_RESEARCH_RISKS`, `ADDITIONAL_REVIEW_REQUIRED` |
| Design | `DESIGN_READY_FOR_SPECIFICATION`, `DESIGN_READY_WITH_RESEARCH_RISKS`, `DESIGN_NOT_READY` |
| Formula specification | `FORMULA_SPEC_READY_FOR_IMPLEMENTATION`, `FORMULA_SPEC_READY_WITH_RESEARCH_RISKS`, `FORMULA_SPEC_NOT_READY` |
| Implementation | `IMPLEMENTATION_READY_FOR_MODULE_REVIEW`, `IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`, `IMPLEMENTATION_NOT_READY` |
| Implementation review | `MODULE_IMPLEMENTATION_READY_FOR_PANEL_SPEC`, `MODULE_IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`, `MODULE_IMPLEMENTATION_NOT_READY` |
| Panel specification | `PANEL_SPEC_READY_FOR_IMPLEMENTATION`, `PANEL_SPEC_READY_WITH_MINOR_REVIEW_ITEMS`, `PANEL_SPEC_NOT_READY` |
| Panel generation | `PANEL_GENERATION_READY_FOR_AUDIT`, `PANEL_GENERATION_READY_WITH_MINOR_REVIEW_ITEMS`, `PANEL_GENERATION_NOT_READY` |
| Panel audit | `PANELS_APPROVED_FOR_IC_DISCOVERY`, `PANELS_APPROVED_WITH_MINOR_NOTES`, `PANELS_NOT_APPROVED` |
| IC discovery | `IC_DISCOVERY_COMPLETE`, `IC_DISCOVERY_COMPLETE_WITH_RESEARCH_RISKS`, `IC_DISCOVERY_NOT_READY` |
| Research review | `RESEARCH_REVIEW_READY_FOR_GOVERNANCE_DECISION`, `RESEARCH_REVIEW_INCONCLUSIVE`, `RESEARCH_REVIEW_BLOCKED` |
| Governance decision | `ADVANCE`, `WATCH`, `PARK`, `DIAGNOSTIC` |
| Master state update | `MASTER_RESEARCH_STATE_UPDATED`, `MASTER_RESEARCH_STATE_UPDATE_REQUIRED`, `MASTER_RESEARCH_STATE_BLOCKED` |

## SECTION 17 - Blocking Conditions That Override Momentum

Any of the following blocks continuation:

- Evidence of look-ahead.
- Missing or ambiguous timing policy.
- PIT metadata without source lineage.
- License or entitlement uncertainty for external data.
- Candidate IDs not matching specification.
- Unauthorized candidates in code or artifacts.
- Panel manifest mismatch.
- Duplicate panel keys.
- IC run before panel audit.
- Refinement run during discovery.
- Validation claim before governance decision.
- Production or threshold change during research.
- ML introduced during discovery.
- Broad negative IC result being treated as refinement-ready without separate diagnostic design.

When blocked, the next deliverable must be a review, audit, closeout, or redesign note. It must not be more execution.

## SECTION 18 - Verification

Verified for this standard:

- Required lifecycle phases 0 through 11 are present.
- Each phase defines objective, required inputs, required outputs, deliverables, verification, artifacts, exit criteria, blocking conditions, and non-goals.
- Research module definition is present.
- Candidate limits are defined.
- Governance outcomes `ADVANCE`, `WATCH`, `PARK`, and `DIAGNOSTIC` are defined.
- Required independent reviews are defined.
- Artifact conventions are defined.
- Naming conventions are defined.
- Required guardrails are defined.
- Quality standards are defined.
- Classification appears as `PROJECT_STANDARD_APPROVED`.
- No implementation files were changed.
- No research execution was performed.
- No panel generation or IC computation was performed.
- No production, governance threshold, or ML changes were made.

## SECTION 19 - Final Standard

Project Underdog research modules must proceed through the full lifecycle in this standard. The process is intentionally conservative: small modules, explicit specifications, independent reviews, deterministic artifacts, audited panels, separated IC discovery, and governance decisions before state changes.

Final classification:

- `PROJECT_STANDARD_APPROVED`
