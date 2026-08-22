# Project Underdog - Phase 5 Prepared Observations Implementation Design v1

Date: 2026-07-22

## 1. Executive Classification

Final classification: `PREPARED_OBSERVATIONS_IMPLEMENTATION_DESIGN_DEFINED`

This note defines the implementation architecture for the Project Underdog Phase 5 Prepared Observations platform layer. Prepared Observations sits after Source Authority, PIT Identity and Context Evidence, and Comparator Construction, and before scientific modules. Its purpose is to assemble deterministic, traceable, metadata-qualified observation packages from already-authorized, already-identified, already-time-qualified, and already-comparator-qualified upstream records.

This is an implementation-design document only. It does not implement code, modify tests, modify specifications, retrieve data, select vendors, define external APIs, define production databases, construct identities, construct comparators, interpret context, define formulas, define signals, define factors, define hypotheses, generate candidates, construct panels, calculate IC, validate, optimize, productionize, or introduce ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_source_authority_executable_conformance_rereview_v1.md`: final classification `SOURCE_AUTHORITY_IMPLEMENTATION_FULLY_CONFORMANT`; Source Authority provides role-specific authority state, diagnostics, limitations, and traceability while refusing raw values, retrieval, identity construction, peer construction, formulas, candidates, panels, IC, validation, production, and ML.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_executable_conformance_review_v1.md`: final classification `PIT_IDENTITY_AND_CONTEXT_EVIDENCE_IMPLEMENTATION_CONFORMANT_WITH_MINOR_OBSERVATIONS`; PIT Identity and Context Evidence represents identity, lineage, context applicability, interval metadata, coverage, limitations, diagnostics, Source Authority trace propagation, and deterministic serialization.
- `docs/research_notes/project_underdog_phase5_comparator_construction_executable_conformance_review_v1.md`: final classification `COMPARATOR_CONSTRUCTION_IMPLEMENTATION_FULLY_CONFORMANT`; Comparator Construction represents metadata-qualified comparator relationships, temporal applicability, eligibility states, coverage, context support, diagnostics, inherited traces, and bounded information contracts.
- `docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md`: explicitly positions Prepared Observations as the downstream layer that should convert eligible comparator relationships and governed observations into source-independent observation packages while not measuring observations or deciding scientific meaning.
- `docs/research_notes/project_underdog_first_module_implementation_architecture_specification_v1.md`: scientific modules must receive prepared observations and must not construct comparator sets inside formula logic.
- `docs/research_notes/project_underdog_first_module_reference_implementation_v1.md` and `docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md`: the completed First Module consumes prepared source-independent synthetic inputs, gates identity/PIT/comparator/observation/coverage/traceability, and preserves formula and decomposition responsibilities inside the module.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: information roles and evidence maturity remain distinct; diagnostic, explanatory, contextual, comparator, negative, hypothetical, and alpha information cannot be silently interchanged.
- Platform v2, artifact-lineage, reproducibility, contamination, falsification, negative-evidence, and existing-family reinterpretation governance remain authoritative.

Final classification applies only to implementation design readiness for the Prepared Observations layer.

## 2. Purpose

Prepared Observations is the final bounded platform layer before scientific modules consume externally informed data structures.

It answers:

- What evidence is being packaged for a target observation?
- Which target identity applicability interval governs the package?
- Which observation time or approved observation interval governs the package?
- Which Source Authority, PIT Identity and Context Evidence, and Comparator Construction traces govern every included element?
- Which comparator relationships are available, unavailable, conditional, unresolved, excluded, or missing?
- Which context evidence attachments are included and which information roles they carry?
- What coverage, missingness, limitations, diagnostics, and upstream fatal conditions remain active?
- Is the package structurally ready for a downstream scientific module to inspect?

It does not answer:

- Is the evidence predictive?
- Is the evidence economically meaningful?
- Which observation is better?
- Which formula should use it?
- Does alpha exist?
- Is a hypothesis supported?
- Does a candidate, panel, validation result, production signal, or ML feature exist?

Prepared Observations packages evidence. It does not interpret evidence.

## 3. Platform Position

Conceptual platform flow:

```text
External Information
        |
        v
Source Authority
        |
        v
PIT Identity & Context Evidence
        |
        v
Comparator Construction
        |
        v
Prepared Observations
        |
        v
Scientific Modules
```

Upstream boundaries:

- Source Authority decides role-specific authority states and traceability; Prepared Observations consumes those traces and must not re-evaluate source authority.
- PIT Identity and Context Evidence decides identity/context applicability metadata; Prepared Observations consumes identity interval and context attachment metadata and must not construct or repair identity.
- Comparator Construction decides comparator relationship eligibility and temporal applicability; Prepared Observations consumes comparator relationship metadata and must not reconstruct peers or score similarity.

Downstream boundaries:

- Scientific modules receive package metadata, observations, comparator attachments, role declarations, readiness states, limitations, diagnostics, and trace references.
- Scientific modules remain responsible for their approved measurement, formula, interpretation, hypothesis, contamination, falsification, and later validation boundaries.
- Prepared Observations must not force immediate retrofitting of the completed First Module. It defines a stable general contract future modules can consume.

## 4. Core Philosophy

Structural readiness is not scientific validity.

A structurally ready package means the metadata contract is complete enough for a downstream module to inspect without violating Project Underdog's platform boundaries. It does not mean the observation has alpha value, predictive content, statistical significance, scientific novelty, validation status, production utility, or ML readiness.

Prepared Observations therefore preserves three separations:

| Separation | Design rule |
|---|---|
| Packaging versus interpretation | The layer assembles traceable packages but does not infer scientific meaning. |
| Structural readiness versus alpha evidence | Readiness depends on metadata completeness, not returns, IC, Sharpe, rank, or performance. |
| Upstream qualification versus downstream use | Source, identity, context, and comparator decisions remain upstream; formulas and decomposition remain downstream. |

This protects the repository from a subtle failure mode: an implementation layer becoming an accidental scientific judge because it assembled convenient inputs.

## 5. Architecture Overview

Conceptual component flow:

```text
Upstream Contract Intake
        |
        v
Trace Validation
        |
        v
Target Observation Registration
        |
        v
Context and Comparator Attachment
        |
        v
Temporal Alignment Evaluation
        |
        v
Information-Role Validation
        |
        v
Coverage and Missingness Evaluation
        |
        v
Diagnostic Accumulation
        |
        v
Structural Readiness Evaluation
        |
        v
Prepared Observation Information Contract
        |
        v
Traceability and Artifact Lineage
```

Component responsibilities:

| Component | Primary responsibility |
|---|---|
| Upstream Contract Intake | Accept only bounded outputs from Source Authority, PIT Identity and Context Evidence, and Comparator Construction. |
| Trace Validation | Confirm required inherited traces exist and remain attached to each evidence element. |
| Target Observation Registration | Represent the target observation and its governing identity applicability interval. |
| Context and Comparator Attachment | Attach already-qualified context evidence and comparator relationships without reconstructing or scoring them. |
| Temporal Alignment Evaluation | Represent whether observation, identity, context, comparator, and source-known timing align safely. |
| Information-Role Validation | Preserve declared information roles and block prohibited role conversion. |
| Coverage and Missingness Evaluation | Represent required/optional coverage, unavailable evidence, and explicit exclusions. |
| Diagnostic Accumulation | Emit deterministic metadata diagnostics without repairing evidence. |
| Structural Readiness Evaluation | Assign a metadata-only readiness state after fatal, unresolved, and conditional conditions are preserved. |
| Information Contract | Expose only prepared-observation metadata and explicit refusal flags. |
| Traceability and Artifact Lineage | Link package outputs to upstream artifacts, governing design versions, diagnostics, limitations, and future module references. |

This architecture defines responsibilities and information flow only. It does not define classes, APIs, schemas, storage, source queries, file formats, formulas, or tests.

## 6. Responsibility Model

Approved responsibilities:

| Responsibility | Purpose | Inputs | Outputs | Dependencies | Prohibited responsibilities |
|---|---|---|---|---|---|
| Prepared-observation registration | Create a package-level metadata object for one target and one observation time or interval. | Target identity applicability metadata and observation-time metadata. | Prepared observation package metadata. | PIT Identity and Context Evidence. | Creating identities, constructing PIT metadata, measuring values. |
| Observation-package assembly | Assemble target, context, comparator, trace, coverage, missingness, limitations, and diagnostics. | Upstream metadata contracts. | Source-independent package. | Source Authority, PIT, Comparator Construction. | Formula execution, signal calculation, interpretation. |
| Target observation representation | Represent the target observation role and applicability boundary. | Target interval, observation role, observation-time metadata. | Target observation metadata. | PIT identity and information-role governance. | Creating raw observation values or alpha quantities. |
| Comparator observation representation | Attach eligible or conditional comparator relationships as package metadata. | Comparator Construction outputs. | Comparator observation attachment metadata. | Comparator Construction. | Rebuilding comparator sets, ranking comparators, optimizing membership. |
| Context-evidence attachment | Preserve approved context evidence attachments and roles. | PIT context evidence records. | Context attachment metadata. | PIT Identity and Context Evidence. | Context interpretation or classification selection. |
| Observation-time representation | Preserve point, interval, open, unavailable, unknown, or superseded timing states. | Observation timing metadata. | Observation-time metadata and diagnostics. | Temporal governance. | Interpolation, resampling, forward filling, backfilling, date repair. |
| Temporal alignment representation | Represent alignment among target, context, comparator, and observation timing. | Interval metadata from all upstream layers. | Temporal-alignment state and limitations. | PIT and Comparator Construction. | Executable PIT panel construction. |
| Information-role representation | Preserve approved information roles per evidence element. | Integrated Scientific Information Inventory role labels. | Role metadata or role diagnostic. | Information-role inventory. | Reclassifying diagnostic/explanatory evidence as alpha input. |
| Upstream eligibility propagation | Preserve upstream states and fatal diagnostics. | Source, PIT, and comparator traces. | Inherited eligibility metadata. | All upstream layers. | Downgrading fatal upstream conditions. |
| Coverage representation | Preserve target, context, comparator, temporal, role, and trace coverage. | Upstream coverage metadata and package requirements. | Coverage metadata and diagnostics. | Upstream contracts. | Treating partial coverage as complete readiness. |
| Missingness representation | Distinguish required, optional, unavailable, and intentionally excluded evidence. | Package requirements and upstream metadata. | Missingness metadata and limitations. | Platform v2 fail-closed discipline. | Imputation, zero-filling, silent dropping. |
| Observation limitations | Preserve limitations from upstream layers and package evaluation. | Upstream limitations and package diagnostics. | Limitation set. | Governance. | Clearing limitations through convenience. |
| Observation diagnostics | Explain metadata and contract failures. | Package metadata. | Deterministic diagnostic set. | Platform v2 diagnostic discipline. | Scientific-quality diagnostics or alpha claims. |
| Trace propagation | Carry Source Authority, PIT, and Comparator traces into package output. | Upstream trace bundles. | Upstream trace bundle. | Artifact lineage and reproducibility. | Recomputing upstream decisions. |
| Information-contract packaging | Bound downstream outputs. | Prepared package and diagnostics. | Restricted information contract. | Integrated inventory and First Module contract pattern. | Raw values, source retrieval, formulas, candidates, panels, validation, production, ML. |
| Structural readiness classification | Classify package contract state. | Diagnostics, limitations, coverage, traces, temporal alignment, roles. | Readiness state. | Upstream governance and fail-closed discipline. | Scientific validation, prediction, ranking, IC, Sharpe, production utility. |

## 7. Prepared-Observation Invariant

Every prepared observation package must reference exactly:

- one target identity applicability interval;
- one observation time or approved observation interval;
- one governing Source Authority trace set;
- one governing PIT Identity and Context Evidence trace set;
- zero or more comparator relationships already approved or conditionally approved by Comparator Construction;
- zero or more context-evidence records already approved or conditionally approved for the target identity interval;
- one declared information role for each included evidence element.

The package must not attach raw evidence directly to an identity without:

- identity applicability;
- temporal applicability;
- source traceability;
- information-role metadata.

Where comparators are present, they must be inherited from Comparator Construction rather than reconstructed. Where context is present, it must be inherited from PIT Identity and Context Evidence rather than reinterpreted. Where source trust is referenced, it must be inherited from Source Authority rather than re-evaluated.

Invariant failure is a structural package failure, not a scientific finding.

## 8. Observation-Package Model

Conceptual records:

| Record | Required metadata | Design meaning |
|---|---|---|
| `PreparedObservationPackage` | package id, target observation, observation time or interval, readiness state, diagnostics, limitations, trace bundle, artifact-lineage reference. | Top-level package for downstream module intake. |
| `TargetObservationMetadata` | target identity id, target identity applicability interval id, target role, observation role, observation availability status, PIT trace. | The subject whose observation is being packaged. |
| `ComparatorObservationAttachment` | comparator relationship id, comparator identity id, comparator applicability interval, comparator eligibility state, comparator diagnostics, comparator trace. | Already-qualified comparator metadata attached to the package. |
| `ContextEvidenceAttachment` | context id, context role, identity interval id, context applicability interval, context evidence status, information role, PIT trace. | Already-applicable contextual evidence attached to the target or comparator role. |
| `ObservationTimeMetadata` | point time or interval, open/unknown/unavailable/superseded/duplicate markers, package-construction time if governed as metadata only. | Temporal description of the observation package. |
| `TemporalAlignmentMetadata` | alignment state, aligned interval references, stale/superseded/expired/discontinuous markers, timing diagnostics. | Whether package elements overlap or align as metadata. |
| `InformationRoleAssignment` | evidence element id, approved role, role source, role limitations, prohibited conversion marker. | Role preservation and role-boundary enforcement. |
| `InheritedEligibilityMetadata` | upstream states from Source Authority, PIT, and Comparator Construction. | Shows upstream eligibility without recomputing it. |
| `CoverageMetadata` | target, comparator, context, temporal, role, and traceability coverage. | Explicit completeness and partiality representation. |
| `MissingnessMetadata` | required missing, optional missing, unavailable, intentionally excluded, unresolved missingness. | Prevents silent zeros, imputation, or drops. |
| `ObservationLimitation` | limitation id, inherited or package-local source, affected element, permitted restriction. | Bounded use warning attached to the package. |
| `ObservationDiagnostic` | diagnostic code, affected element, severity class, inherited flag, deterministic ordering key. | Metadata and contract failure explanation. |
| `UpstreamTraceBundle` | Source Authority trace, PIT trace, Comparator Construction trace, governing design ids, fixture ids if synthetic. | Reconstructable lineage across platform layers. |
| `PreparedObservationInformationContract` | allowed outputs, refused outputs, readiness state, package metadata, traces. | Downstream boundary. |
| `ArtifactLineageReference` | upstream artifact references, package artifact reference, future module output reference placeholder. | Links platform package to artifacts without constructing module outputs. |

Synthetic placeholders may be used in a future reference implementation to demonstrate contract shape. This design does not define numerical values, transformations, formulas, or measurement algorithms.

## 9. Observation-Time And Temporal-Alignment Model

Time semantics must remain distinct:

| Time concept | Meaning | Design constraint |
|---|---|---|
| Source effective time | When the source says the underlying fact became effective. | Inherited from source/PIT authority; not inferred here. |
| Identity applicability time | When the identity interval applies. | Inherited from PIT Identity and Context Evidence. |
| Context applicability time | When context evidence applies to the identity interval. | Inherited from PIT Identity and Context Evidence. |
| Comparator applicability time | When the comparator relationship applies. | Inherited from Comparator Construction. |
| Observation time | When the target observation is represented for downstream use. | Must be explicit, interval-bounded, or explicitly unknown/unavailable. |
| Package-construction time | When the package was assembled. | May be metadata only; never substitutes for PIT applicability. |

Observation granularity:

| Granularity | Representation | Required behavior |
|---|---|---|
| Point-in-time observation | One observation timestamp. | Use only if identity, context, comparator, and source-known metadata can be aligned or limitations preserved. |
| Interval observation | Start and end of approved observation interval. | Preserve interval; do not collapse to a point. |
| Open interval | Known start and no known end. | Conditional at most and explicitly limited. |
| Unknown observation time | Required observation timing absent or ambiguous. | Unresolved or structurally incomplete depending materiality. |
| Unavailable observation time | Evidence known unavailable for the package. | Missingness and diagnostic; no imputation. |
| Superseded observation package | Package replaced by later package lineage. | Preserve supersession; do not overwrite. |
| Duplicate observation package | Same target/time/role exposure appears more than once. | Emit duplicate diagnostic; do not silently deduplicate. |
| Incomplete observation package | Required metadata missing. | Structurally incomplete or insufficient evidence. |

Temporal-alignment states:

- `fully_aligned`: required target, context, comparator, observation, and trace intervals align for the package role.
- `partially_aligned`: alignment is limited but governed and visible.
- `non_overlapping`: required intervals do not overlap; fail closed for structural readiness.
- `unknown_alignment`: required timing cannot be established.
- `stale_contextual_evidence`: context may be outdated but disclosed and allowed only if upstream governance permits conditional handling.
- `superseded_contextual_evidence`: context is replaced; preserve lineage and condition or block use.
- `expired_comparator_applicability`: comparator relationship ended before observation use.
- `discontinuous_identity_applicability`: identity interval has gaps; preserve limitation or block continuous use.
- `mixed_frequency`: package elements have different observation cadences; represent only, without synchronization.
- `incomplete_temporal_traceability`: timing trace is missing or insufficient.

Prepared Observations must not invent interpolation, forward filling, backfilling, carry-forward, imputation, synchronization, or resampling policies.

## 10. Information-Role Model

Prepared Observations preserves approved information roles from the Integrated Scientific Information Inventory. The layer may expose roles and validate that every evidence element declares a role. It must not reclassify roles without explicit upstream authorization.

Approved role vocabulary to preserve:

- `VALIDATED_ALPHA_INFORMATION`
- `SUPPORTED_ALPHA_INFORMATION`
- `CONTEXTUAL_CONTROL_INFORMATION`
- `CONDITIONING_INFORMATION`
- `COMPARATOR_OR_BENCHMARK_INFORMATION`
- `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION`
- `EXPLANATORY_ONLY_INFORMATION`
- `FAMILY_REFINEMENT_INFORMATION`
- `DIAGNOSTIC_INFORMATION`
- `NEGATIVE_INFORMATION`
- `REJECTED_OR_RETIRED_INFORMATION`
- `HYPOTHETICAL_INFORMATION`
- `MISSING_REQUIRED_INFORMATION`
- `INSUFFICIENT_EVIDENCE`

Role rules:

- A package may contain multiple information roles, but every evidence element must have exactly one declared role.
- Comparator attachments must preserve `COMPARATOR_OR_BENCHMARK_INFORMATION` or another explicitly authorized role; mere comparator existence is not alpha evidence.
- Context attachments may remain `CONTEXTUAL_CONTROL_INFORMATION`, `CONDITIONING_INFORMATION`, `EXPLANATORY_ONLY_INFORMATION`, `DIAGNOSTIC_INFORMATION`, or another approved role as inherited.
- `DIAGNOSTIC_INFORMATION`, `EXPLANATORY_ONLY_INFORMATION`, `NEGATIVE_INFORMATION`, `REJECTED_OR_RETIRED_INFORMATION`, `HYPOTHETICAL_INFORMATION`, `MISSING_REQUIRED_INFORMATION`, and `INSUFFICIENT_EVIDENCE` must not be exposed as alpha input.
- Prepared Observations may reject or mark structurally incomplete a package that requests prohibited role conversion.

## 11. Structural-Readiness Model

Structural readiness is metadata-only. It may depend on traces, intervals, declared roles, coverage, missingness, alignment, diagnostics, limitations, and upstream fatal states. It must not depend on return behavior, factor performance, predictive accuracy, IC, Sharpe ratio, statistical significance, scientific attractiveness, production utility, or ML utility.

Readiness states:

| State | Meaning | Permitted downstream meaning |
|---|---|---|
| `PREPARED_OBSERVATION_STRUCTURALLY_READY` | Required traces, target interval, observation time, temporal alignment, required roles, coverage, and fatal-diagnostic checks pass. | Module may inspect the package subject to its own gates. |
| `PREPARED_OBSERVATION_CONDITIONALLY_READY` | Required elements exist but limitations such as partial coverage, open interval, governed stale metadata, or optional comparator incompleteness must remain visible. | Module may inspect only if its own scientific contract permits conditional inputs. |
| `PREPARED_OBSERVATION_UNRESOLVED` | Material ambiguity exists, but a fatal structural defect has not been established. | Module must treat the package as unresolved unless separately governed. |
| `PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE` | Required package metadata is absent or invalid. | Module must not use as authoritative input. |
| `PREPARED_OBSERVATION_EXCLUDED` | Package or evidence element is explicitly excluded or duplicated/superseded in a way that blocks use. | Module must not use except as diagnostic or lineage record where permitted. |
| `INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE` | Evidence is not enough to decide readiness safely. | Hold or diagnostic-only use. |

No state implies source acceptance, identity construction, comparator construction, formula readiness, candidate readiness, panel readiness, IC readiness, validation readiness, production readiness, or ML readiness.

## 12. Decision-Precedence Model

Decision precedence should be deterministic and ordered so fatal conditions cannot be masked by conditional readiness.

Recommended precedence:

1. Explicit exclusion, supersession conflict, prohibited duplicate package conflict, or prohibited role use produces `PREPARED_OBSERVATION_EXCLUDED`.
2. Missing target identity interval, invalid observation time, missing Source Authority trace, missing PIT trace, missing required Comparator trace, inherited fatal upstream diagnostic, non-overlapping temporal applicability, conflicting evidence attachment, undeclared information role, incomplete required traceability, or raw evidence attachment produces `PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE`.
3. Unknown alignment, unresolved upstream state, required context missing, required comparator missing, insufficient role coverage, incomplete temporal traceability, or unresolved duplicate exposure produces `INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE` or `PREPARED_OBSERVATION_UNRESOLVED` depending whether the package can still state the ambiguity.
4. Partial coverage, partial temporal alignment, optional context missing, approved open interval, approved stale-but-disclosed metadata, incomplete optional comparator set, or inherited conditional limitation produces `PREPARED_OBSERVATION_CONDITIONALLY_READY` if no higher-precedence condition exists.
5. No diagnostics and no limitations produces `PREPARED_OBSERVATION_STRUCTURALLY_READY`.

Fatal or blocking conditions:

- missing target identity interval;
- invalid observation time or observation interval;
- missing Source Authority trace;
- missing PIT trace;
- missing required Comparator trace;
- inherited fatal upstream diagnostic;
- non-overlapping temporal applicability where overlap is required;
- conflicting evidence attachment;
- undeclared information role;
- incomplete required traceability;
- prohibited evidence role use;
- duplicate package conflict;
- raw evidence attachment without upstream qualification.

Conditional limitations:

- partial coverage;
- partial temporal alignment;
- optional context missing;
- approved open interval;
- approved stale-but-disclosed metadata;
- incomplete optional comparator set;
- governed missingness;
- inherited conditional upstream limitation.

Unresolved ambiguity: repository evidence supports the need for deterministic precedence, but final implementation-level mapping between `PREPARED_OBSERVATION_UNRESOLVED` and `INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE` should be covered by future synthetic fixtures.

## 13. Coverage And Missingness Model

Coverage metadata:

| Coverage type | Required representation |
|---|---|
| Target coverage | Whether target observation metadata is available for the required identity interval and observation time. |
| Comparator coverage | Whether required comparator relationships are present, conditional, missing, excluded, or insufficient. |
| Contextual-evidence coverage | Whether required context evidence attachments exist for the target and comparator roles. |
| Temporal coverage | Whether required intervals cover the observation relationship. |
| Role coverage | Whether every evidence element carries a permitted information role. |
| Traceability coverage | Whether every evidence element can be traced to Source Authority, PIT, Comparator Construction where applicable, design lineage, and artifact lineage. |

Missingness metadata:

| Missingness type | Required behavior |
|---|---|
| Required-field missingness | Emit diagnostic and block structural readiness. |
| Optional-field missingness | Preserve limitation; do not silently promote to fully ready. |
| Unavailable evidence | Represent as unavailable rather than zero or absent. |
| Intentionally excluded evidence | Preserve exclusion reason and trace. |
| Governed missingness | May be conditionally ready only when upstream and package rules preserve the limitation. |
| Unresolved missingness | Hold as unresolved or insufficient evidence. |

Prepared Observations must not treat missingness as zero, impute missing elements, silently drop missing evidence, or automatically convert partial coverage into full readiness.

## 14. Duplicate And Supersession Model

Duplicate handling:

- Duplicate prepared-observation packages must be diagnosed and preserved as separate lineage records unless future governance authorizes an explicit resolution rule.
- Duplicate evidence attachments must not be silently deduplicated, merged, prioritized, or overwritten.
- Duplicate comparator exposure must preserve Comparator Construction diagnostics such as duplicate exposure or self-comparison limitations.
- Duplicate role exposure must be visible when the same evidence appears under incompatible roles.

Supersession handling:

- Superseded source evidence must preserve Source Authority lineage and revision/reconstruction metadata.
- Superseded identity intervals must preserve PIT lineage and must not be silently merged into current identity states.
- Superseded comparator relationships must preserve Comparator Construction lineage and must not be used as active relationships unless conditionally governed.
- Superseded prepared-observation packages must retain prior package lineage, replacement metadata, diagnostic history, and artifact references.

No silent deduplication, overwrite, merge, priority ranking, source preference, or current-state replacement is authorized by this design.

## 15. Diagnostic Model

Diagnostics describe metadata and contract conditions only. They must not diagnose scientific quality, predictive strength, formula fitness, or validation likelihood.

Recommended diagnostic vocabulary:

| Diagnostic | Meaning | Required behavior |
|---|---|---|
| `MISSING_TARGET_APPLICABILITY` | Target identity applicability interval is absent or not exactly one. | Structural incomplete. |
| `MISSING_OBSERVATION_TIME` | Required observation time or interval is absent. | Structural incomplete or unresolved. |
| `INVALID_OBSERVATION_INTERVAL` | Observation interval ordering or boundary is invalid. | Structural incomplete. |
| `UNRESOLVED_TEMPORAL_ALIGNMENT` | Required temporal alignment cannot be determined. | Unresolved or insufficient evidence. |
| `NON_OVERLAPPING_TEMPORAL_APPLICABILITY` | Required identity, context, comparator, or observation intervals do not overlap. | Structural incomplete or excluded depending role. |
| `CONFLICTING_EVIDENCE_ATTACHMENT` | Evidence attachments conflict across identity, context, role, or interval. | Structural incomplete or unresolved. |
| `MISSING_SOURCE_AUTHORITY_TRACE` | Required inherited Source Authority trace is absent. | Structural incomplete. |
| `MISSING_PIT_TRACE` | Required inherited PIT trace is absent. | Structural incomplete. |
| `MISSING_COMPARATOR_TRACE` | Required inherited Comparator Construction trace is absent. | Structural incomplete when comparator required. |
| `INHERITED_FATAL_UPSTREAM_DIAGNOSTIC` | Source, PIT, or Comparator layer emitted fatal diagnostic. | Preserve and block readiness. |
| `INSUFFICIENT_OBSERVATION_COVERAGE` | Required target, context, comparator, temporal, role, or trace coverage is insufficient. | Insufficient evidence or conditional if governed. |
| `MISSING_REQUIRED_CONTEXT` | Required context attachment is absent. | Unresolved or insufficient evidence. |
| `MISSING_REQUIRED_COMPARATOR` | Required comparator relationship is absent. | Unresolved or insufficient evidence. |
| `UNDECLARED_INFORMATION_ROLE` | Evidence element has no role. | Structural incomplete. |
| `PROHIBITED_INFORMATION_ROLE_USE` | Evidence role is being converted or exposed in a prohibited way. | Excluded or structural incomplete. |
| `DUPLICATE_OBSERVATION_EXPOSURE` | Duplicate package, attachment, comparator, or role exposure is unresolved. | Excluded, unresolved, or insufficient evidence. |
| `SUPERSEDED_OBSERVATION_PACKAGE` | Package has been replaced or is no longer current for the package lineage. | Excluded or conditional lineage-only use. |
| `INCOMPLETE_OBSERVATION_TRACEABILITY` | Required package reconstruction metadata is incomplete. | Structural incomplete. |
| `STRUCTURALLY_INCOMPLETE_PACKAGE` | Package cannot satisfy the minimum invariant. | Structural incomplete. |
| `RAW_EVIDENCE_ATTACHMENT_PROHIBITED` | Evidence bypasses upstream qualification and traceability. | Structural incomplete or excluded. |

Ordering principles:

- Emit inherited diagnostics before package-local diagnostics when explaining upstream blockers.
- Preserve deterministic branch order.
- Preserve all diagnostics in combined-failure cases.
- Do not allow a conditional limitation to suppress a fatal diagnostic.
- Do not collapse materially distinct package failures into a generic message unless the generic message is additive.

## 16. Upstream Trace-Propagation Model

Prepared Observations must propagate, not recompute:

- Source Authority traces;
- PIT Identity and Context Evidence traces;
- Comparator Construction traces.

The propagated trace bundle must be sufficient to reconstruct:

- which source authority decision governed each evidence element;
- which identity applicability interval governed each target, comparator, or context element;
- which context applicability interval governed each attachment;
- which comparator relationship governed each comparator observation attachment;
- which upstream diagnostics and limitations remained active;
- which governing design and reference-implementation version produced upstream metadata where available;
- whether the package is synthetic, design-only, or future evidence-backed.

Upstream fatal diagnostics must not be erased, downgraded, or converted into conditional readiness. Upstream conditional limitations must remain active unless a later governed process explicitly supersedes them.

## 17. Information Contract

Prepared Observations may expose only:

- prepared-observation metadata;
- target observation metadata;
- comparator observation metadata;
- context-attachment metadata;
- observation-time metadata;
- temporal-alignment metadata;
- information-role metadata;
- inherited eligibility metadata;
- coverage metadata;
- missingness metadata;
- limitations;
- diagnostics;
- inherited Source Authority trace;
- inherited PIT trace;
- inherited Comparator trace;
- reproducibility metadata;
- artifact-lineage metadata;
- governing design and implementation versions.

Prepared Observations must explicitly refuse:

- source retrieval;
- raw vendor integration;
- source-authority evaluation;
- identity construction;
- identity resolution;
- comparator construction;
- peer discovery;
- scientific similarity;
- value transformation;
- normalization;
- ranking;
- winsorization;
- imputation;
- resampling;
- formula execution;
- signal calculation;
- factor calculation;
- candidate generation;
- panel construction;
- IC calculation;
- statistical testing;
- scientific validation;
- portfolio construction;
- optimization;
- production decisions;
- ML features;
- ML labels;
- model training.

The downstream contract may tell a scientific module:

- what evidence is included;
- who and when it applies to;
- which comparator relationships are available;
- which information roles govern each element;
- which limitations and diagnostics remain active;
- whether the package is structurally ready.

The downstream contract may not tell a scientific module:

- how to calculate a signal;
- which formula to use;
- which observation is better;
- whether alpha exists;
- whether a hypothesis is supported;
- whether a candidate passes validation.

## 18. Traceability And Reproducibility Model

Prepared-observation traceability must permit deterministic reconstruction of the package from metadata alone.

Required traceability and reproducibility elements:

| Element | Requirement |
|---|---|
| Stable package identity | A deterministic package id or synthetic fixture id where applicable. |
| Governing design identity | This design id and later reference implementation id if created. |
| Upstream design lineage | Source Authority, PIT Identity and Context Evidence, and Comparator Construction governing design ids. |
| Upstream result lineage | Authority state, PIT applicability state, comparator eligibility state, limitations, diagnostics, and trace bundles. |
| Observation timing lineage | Observation time or interval and distinction from package-construction time. |
| Role lineage | Declared information role per evidence element and role source. |
| Coverage lineage | Target, comparator, context, temporal, role, and traceability coverage states. |
| Missingness lineage | Required, optional, unavailable, intentionally excluded, governed, and unresolved missingness. |
| Deterministic serialization | Stable ordering of diagnostics, limitations, attachments, traces, and metadata. |
| Artifact reference | Controlled reference, checksum, row count, package version, or synthetic fixture reference where permitted by upstream governance. |
| Reproducibility limitations | Retention, reconstruction, restricted-evidence, or post-access limitations inherited from upstream records. |

Package-construction time may appear as metadata only if it is controlled and deterministic enough for future audit. It must never substitute for observation time, source-known time, identity applicability time, context applicability time, or comparator applicability time.

## 19. Artifact-Lineage Model

Prepared Observations should create a conceptual lineage bridge:

```text
Source Authority artifact(s)
        |
        v
PIT Identity and Context Evidence artifact(s)
        |
        v
Comparator Construction artifact(s)
        |
        v
Prepared Observation package artifact
        |
        v
Future scientific-module result artifact(s)
```

Package artifact lineage should preserve:

- package id;
- target identity interval id;
- observation time or interval;
- included context evidence ids;
- included comparator relationship ids;
- information-role assignments;
- readiness state;
- diagnostics and limitations;
- source authority trace ids or controlled trace bundles;
- PIT trace ids or controlled trace bundles;
- comparator trace ids or controlled trace bundles;
- governing design and implementation ids;
- serialization or checksum metadata where permitted;
- future downstream module reference placeholders.

Future module outputs may cite prepared observation packages. Prepared Observations does not create those module outputs, candidate records, panels, validation artifacts, production artifacts, or ML features.

## 20. First Module Compatibility Assessment

The completed First Module already consumes an analogous prepared input contract. Its reference implementation accepts source-independent synthetic inputs through `FirstModuleInput`, `RepairObservation`, `ComparatorObservation`, `TimeBounds`, comparator validity flags, observation availability flags, coverage flags, and traceability flags. Its conformance review confirms it fails closed for source-specific input, invalid identity, PIT failure, temporal failure, comparator failure, missing observations, coverage failure, unstable input, and traceability failure.

Conceptual mapping:

| Prepared Observations concept | First Module analogous concept | Mapping status |
|---|---|---|
| Prepared package | `FirstModuleInput` | Compatible conceptually; no integration performed. |
| Target observation metadata | `target_observation` / target identity role | Compatible conceptually. |
| Comparator attachments | `comparator_observations` and comparator validity flags | Compatible conceptually, but First Module keeps formula-specific comparator handling. |
| Observation-time metadata | `TimeBounds` and observation time | Compatible conceptually; module-specific timing logic remains downstream. |
| Information roles | requested output roles and approved measurement roles | Compatible conceptually; role conversion remains prohibited. |
| Coverage and missingness | observation and coverage gates | Compatible conceptually; package layer would expose metadata before module gates. |
| Trace bundle | `traceability` | Compatible conceptually; First Module trace includes its frozen specification stack. |
| Structural readiness | validity preconditions | Compatible conceptually; First Module still performs its own validity gates. |

Responsibilities that must remain inside the First Module:

- measurement mapping for the approved module;
- formula derivation;
- common/idiosyncratic/mixed/unresolved decomposition;
- formula-specific unresolved-state handling;
- module-specific diagnostics;
- module-specific traceability to the frozen scientific specification stack.

Responsibilities that must remain inside Prepared Observations:

- upstream trace packaging;
- target/context/comparator attachment metadata;
- observation-time and alignment metadata;
- role preservation;
- coverage and missingness metadata;
- structural readiness;
- information-contract refusal of scientific interpretation.

No First Module artifact is modified by this design. No integration is claimed.

## 21. Future Scientific-Module Compatibility

Prepared Observations defines a stable downstream contract for future modules:

- modules receive target observations as source-independent packages;
- modules receive comparator relationships only as inherited, traceable, metadata-qualified attachments;
- modules receive context evidence only as role-qualified metadata;
- modules receive readiness, missingness, limitations, diagnostics, and traceability;
- modules perform their own approved scientific measurements, formulas, interpretations, contamination checks, falsification rules, and later validation boundaries.

Future modules should not depend directly on Source Authority, PIT Identity and Context Evidence, or Comparator Construction internals when a prepared package can provide the required traceable contract. This prevents formula code from becoming a hidden source adapter, identity resolver, peer constructor, context interpreter, or validation engine.

## 22. Scope Boundaries

This design does not:

- implement code;
- modify tests;
- modify specifications;
- retrieve data;
- select vendors;
- define external APIs;
- define production databases;
- construct identities;
- construct comparators;
- interpret context;
- define numerical formulas;
- define signals;
- define factors;
- define scientific hypotheses;
- generate candidates;
- construct panels;
- calculate IC;
- validate;
- optimize;
- productionize;
- introduce machine learning.

It also does not change Source Authority, PIT Identity and Context Evidence, Comparator Construction, First Module, Platform v2, artifact-lineage, reproducibility, contamination, falsification, negative-evidence, existing-family reinterpretation, integrated-inventory, thresholds, survivor status, or production governance.

## 23. Known Limitations

- No executable code, fixtures, tests, package structures, APIs, schemas, storage files, or production databases are created.
- No real observations, identities, contexts, comparators, peer groups, values, panels, candidates, or validation artifacts are created.
- No source is accepted or reviewed for acceptance.
- No source retrieval, proprietary documentation, or data inspection occurred.
- No formula, signal, factor, statistic, IC, threshold, ranking, normalization, imputation, or resampling rule is defined.
- Structural-readiness state names are design-level recommendations. A future reference implementation should prove exact enum behavior through synthetic fixtures and acceptance tests.
- The mapping between `PREPARED_OBSERVATION_UNRESOLVED` and `INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE` requires fixture-level exercise before implementation conformance can be claimed.
- First Module compatibility is conceptual because the completed First Module is not modified.

## 24. Implementation-Readiness Assessment

Implementation readiness assessment: `READY_FOR_BOUNDED_PREPARED_OBSERVATIONS_REFERENCE_IMPLEMENTATION`

Rationale:

- Source Authority is fully conformant and can provide upstream role-specific authority traces.
- PIT Identity and Context Evidence is conformant with minor observations and can provide identity/context applicability metadata, diagnostics, limitations, and traceability.
- Comparator Construction is fully conformant and can provide comparator relationship metadata, eligibility states, temporal applicability, coverage, context support, diagnostics, limitations, and inherited traces.
- The First Module is implemented as a source-independent prepared-input consumer and remains separated from upstream platform internals.
- The Integrated Scientific Information Inventory provides approved information-role vocabulary and role separation.
- This design defines Prepared Observations purpose, position, architecture, responsibilities, invariant, package model, temporal alignment, role model, readiness states, precedence, coverage, missingness, duplicates, supersession, diagnostics, trace propagation, information contract, reproducibility, artifact lineage, and module compatibility without expanding scope.

Reference implementation readiness is bounded:

- synthetic metadata only;
- no real source use;
- no data retrieval;
- no source acceptance;
- no identity construction;
- no context interpretation;
- no comparator construction;
- no peer construction;
- no formula execution;
- no candidates, panels, IC, validation, production, optimization, or ML.

Final classification restated: `PREPARED_OBSERVATIONS_IMPLEMENTATION_DESIGN_DEFINED`

## 25. Exactly One Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - Phase 5 Prepared Observations Reference Implementation v1`

Rationale:

The implementation design is defined and bounded. The next smallest platform step is a synthetic-only reference implementation that realizes deterministic prepared-observation registration, observation-package assembly, observation-time metadata, temporal-alignment metadata, role preservation, coverage and missingness metadata, duplicate and supersession diagnostics, inherited Source Authority/PIT/Comparator trace propagation, structural-readiness states, information-contract refusal behavior, deterministic serialization, and artifact-lineage metadata.

That next step must not retrieve data, select vendors, define external APIs, define production databases, construct identities, construct comparators, interpret context, define formulas, define signals, define factors, define hypotheses, generate candidates, construct panels, calculate IC, validate, optimize, productionize, or introduce ML.

## Verification Commands Executed

```text
sed -n '1,240p' /Users/AnyiXu_1/.codex/attachments/fd034890-41ac-44d9-9965-e3c8a2f529b5/pasted-text.txt
sed -n '241,520p' /Users/AnyiXu_1/.codex/attachments/fd034890-41ac-44d9-9965-e3c8a2f529b5/pasted-text.txt
sed -n '521,900p' /Users/AnyiXu_1/.codex/attachments/fd034890-41ac-44d9-9965-e3c8a2f529b5/pasted-text.txt
rg -n "SOURCE_AUTHORITY|source authority|Information Role|VALIDATED_ALPHA|DIAGNOSTIC|artifact lineage|reproducib|Prepared Observation|prepared observation" docs/research_notes src tests
rg -n "PIT_IDENTITY|Comparator Construction|COMPARATOR_CONSTRUCTION|First Module|FirstModule|source-independent|trace|lineage|conformance" docs/research_notes src tests
rg --files docs/research_notes | rg "(source_authority|pit_identity_and_context|comparator_construction|first_module|integrated_scientific_information|artifact|reproduc|contamination|falsification|scientific_philosophy|platform_v2)"
sed -n '1,220p' docs/research_notes/project_underdog_phase5_source_authority_executable_conformance_rereview_v1.md
sed -n '1,280p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_executable_conformance_review_v1.md
sed -n '1,430p' docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
sed -n '1,260p' docs/research_notes/project_underdog_phase5_comparator_construction_executable_conformance_review_v1.md
sed -n '260,430p' docs/research_notes/project_underdog_phase5_comparator_construction_executable_conformance_review_v1.md
sed -n '1,260p' docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md
sed -n '1,380p' docs/research_notes/project_underdog_first_module_implementation_architecture_specification_v1.md
sed -n '1,280p' docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md
sed -n '1,260p' docs/research_notes/project_underdog_phase5_source_authority_implementation_design_v1.md
sed -n '1,300p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1.md
sed -n '1,260p' docs/research_notes/project_underdog_first_module_source_independent_measurement_specification_v1.md
sed -n '1,260p' docs/research_notes/project_underdog_first_module_reference_implementation_v1.md
test -e docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
git status --short
rg -n "^## [0-9]+\\." docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
rg -n "Final classification|PREPARED_OBSERVATIONS_IMPLEMENTATION_DESIGN_DEFINED|READY_FOR_BOUNDED_PREPARED_OBSERVATIONS_REFERENCE_IMPLEMENTATION|Project Underdog - Phase 5 Prepared Observations Reference Implementation v1" docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
rg -n "source retrieval|raw vendor integration|source-authority evaluation|identity construction|comparator construction|peer discovery|formula execution|candidate generation|panel construction|IC calculation|scientific validation|production decisions|ML features|model training" docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
git diff --check -- docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
rg -n "import (requests|yfinance|sklearn|wrds|sqlite3|sqlalchemy)|read_csv\\(|to_csv\\(|urlopen|urllib|httpx|download\\(|RandomForest|KMeans|NearestNeighbors|fit\\(|predict\\(|corr\\(|rank\\(|winsor|resample|fillna|ffill|bfill" docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
rg -n "(implemented|created|modified|retrieved|selected|constructed|defined formula|generated candidates|constructed panels|calculated IC|validated|optimized|productionized|introduced ML)" docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
git status --short docs/research_notes/project_underdog_phase5_prepared_observations_implementation_design_v1.md
git status --short
```
