# Project Underdog - First Module Detailed Implementation Design v1

Date: 2026-07-17

## 1. Executive Classification

Final classification: `DETAILED_IMPLEMENTATION_DESIGN_DEFINED`

This note defines the final pre-coding engineering design for:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

The classification refers only to implementation design readiness. It does not authorize production code, programming languages, classes, APIs, package structures, filenames, database schemas, source adapters, data retrieval, real peer construction, discovery, validation, formula optimization, candidates, registries, panels, IC, production artifacts, governance changes, scientific conclusion changes, survivor-status changes, or ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: the first-module scientific boundary is fixed.
- `docs/research_notes/project_underdog_first_module_source_independent_measurement_specification_v1.md`: approved measurement concepts are fixed.
- `docs/research_notes/project_underdog_first_module_formula_specification_v1.md`: approved symbols, temporal ordering, formula sequence, decomposition logic, and unresolved-state rules are fixed.
- `docs/research_notes/project_underdog_first_module_synthetic_fixture_and_acceptance_test_specification_v1.md`: synthetic fixture expectations and acceptance categories are fixed.
- `docs/research_notes/project_underdog_first_module_implementation_architecture_specification_v1.md`: conceptual architecture, components, allowed interactions, failure behavior, and invariants are fixed.
- Phase 5 WS1-WS9, contamination, falsification, integrated inventory, Platform v2, lifecycle governance, reproducibility, and artifact-lineage materials remain authoritative.

## 2. Design Philosophy

Detailed implementation design translates architecture into implementation-ready responsibilities without writing implementation.

Distinctions:

| Layer | Meaning | Status here |
|---|---|---|
| Scientific specification | Defines the scientific claim, measurements, formula, fixtures, and acceptance expectations. | Immutable foundation. |
| Architecture | Defines conceptual components and allowed interactions. | Immutable foundation. |
| Detailed design | Defines ordered responsibilities, conceptual interfaces, gates, diagnostics, and invariants. | Defined here. |
| Implementation | Concrete code and executable tests. | Not created here. |
| Validation | Empirical frozen-horizon evaluation. | Not authorized. |
| Production | Deployment, monitoring, thresholds, and operational artifacts. | Not authorized. |

The design goal is not algorithm invention. The design goal is to make any future implementation mechanically traceable to the approved scientific and architectural stack.

## 3. End-To-End Processing Lifecycle

Complete conceptual sequence:

1. Receive abstract observation roles for target, comparator context, market context, timing, and governance evidence.
2. Confirm that observation roles are source-independent and do not contain source-specific assumptions.
3. Map observation roles to measurement concepts: post-stress context, own-security repair basis, comparator repair basis, market-context control, contextual controls, and observability status.
4. Run identity and PIT gates for target, comparators, context, and timing.
5. Run temporal gates for \(B_t \prec H_t \preceq t \prec F_t\) and no future leakage.
6. Run comparator gates for accepted context, sufficiency, alignment, and ambiguity.
7. Run observation and coverage gates for own and comparator observations.
8. Produce deterministic validity status: pass, unresolved, diagnostic-only, or fail-closed.
9. If validity fails, terminate formula processing and emit unresolved result with diagnostics and traceability.
10. If validity passes, derive own repair \(R_i(t)\).
11. Derive valid comparator repair observations \(R_j(t)\) for accepted comparators.
12. Derive peer-common repair \(C_i(t)\) through the approved equal aggregation.
13. Derive security-idiosyncratic repair \(D_i(t)=R_i(t)-C_i(t)\).
14. Preserve the decomposition relationship \(R_i(t)=C_i(t)+D_i(t)\).
15. Interpret \(Z_i(t)\) as predominantly common, predominantly idiosyncratic, mixed, or unresolved using approved qualitative relation status.
16. Package the result as scientific interpretation, not candidate, panel, alpha, validation, or production output.
17. Attach diagnostics and traceability for every observation, gate, derived quantity, and interpretation.
18. Verify future implementation behavior against approved synthetic fixtures and acceptance categories before any real data is processed.

## 4. Implementation Responsibilities

| Responsibility | Objective | Required inputs | Produced outputs | Dependencies | Diagnostics | Failure behavior | Prohibited behavior |
|---|---|---|---|---|---|---|---|
| Specification conformance | Ensure every stage follows approved science. | Boundary, measurement, formula, fixture, architecture specs. | Conformance obligations. | Full specification stack. | Spec mismatch. | Stop design or implementation path. | Changing science. |
| Observation intake | Accept abstract observation roles. | Target, comparator, market, timing, governance roles. | Source-independent observation bundle. | Architecture Observation Boundary. | Source-specific assumption found. | Reject bundle. | Source adapters, retrieval, field mapping. |
| Measurement mapping | Map roles to approved measurements. | Observation bundle. | Measurement concept bundle. | Measurement spec. | Missing or unsupported measurement role. | Unresolved or reject. | Formula derivation, validation. |
| Validity gating | Evaluate all gates. | Measurement concepts, context roles, governance evidence roles. | Validity status and gate diagnostics. | Architecture Validity Layer. | Gate-specific failure. | Fail closed or unresolved. | Imputation, optimization. |
| Comparator preparation | Prepare accepted comparator observation set. | Comparator context role, comparator observations, validity status. | Valid comparator set or unresolved status. | Comparator architecture and formula spec. | Insufficiency, ambiguity, PIT issue. | Comparator unresolved. | Real peer construction, source selection. |
| Formula derivation | Produce approved derived quantities. | Valid own repair basis and comparator observations. | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\). | Formula spec. | Formula unavailable reason. | Unresolved. | New formula, optimization, validation. |
| Decomposition interpretation | Assign interpretive status. | Derived quantities and qualitative relation status. | \(Z_i(t)\). | Formula and fixture specs. | Ambiguous relation. | Unresolved. | Alpha promotion, threshold estimation. |
| Result packaging | Preserve scientific output semantics. | Derived quantities, decomposition status, diagnostics. | Scientific result concept. | Result architecture. | Output-role violation. | Reject or unresolved. | Candidate, panel, production output. |
| Traceability capture | Record lineage of every decision. | Observations, gates, formula components, diagnostics, result. | End-to-end trace bundle. | Traceability architecture. | Missing lineage. | Reject result for research use. | Decorative or optional trace. |
| Fixture conformance | Ensure behavior can satisfy approved fixtures. | Fixture and acceptance expectations. | Verification obligations. | Synthetic fixture spec. | Missing coverage. | Hold before implementation. | Executable tests in this note. |

## 5. Conceptual Interfaces

| Interface | Information exchanged | Preconditions | Postconditions | Invariants | Prohibited assumptions |
|---|---|---|---|---|---|
| Observation intake -> Measurement mapping | Abstract observation bundle. | Inputs are source-independent roles. | Roles map to approved measurement concepts or fail. | No source fields or schemas. | Vendor behavior, field names, file formats. |
| Measurement mapping -> Validity gating | Measurement concept bundle. | Concepts trace to measurement spec. | Each concept receives gate evaluation. | Measurement meaning unchanged. | Missing concepts can be filled silently. |
| Validity gating -> Comparator preparation | Comparator gate status and context roles. | Identity, PIT, timing, and context evidence roles are available. | Comparator set is accepted or unresolved. | Comparator remains contextual. | Peer construction or optimization occurs here. |
| Validity gating -> Formula derivation | Validity status and approved measurements. | Required gates pass. | Formula derivation may proceed or halt. | Fail-closed behavior. | Formula can repair invalid inputs. |
| Comparator preparation -> Formula derivation | Valid comparator observation set. | Comparator context accepted. | \(C_i(t)\) can be derived. | No hidden membership changes. | Default peers, future-known peers. |
| Formula derivation -> Decomposition interpretation | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\). | Formula quantities valid and traceable. | \(Z_i(t)\) can be interpreted or unresolved. | Formula unchanged. | New thresholds or learned rules. |
| Decomposition interpretation -> Result packaging | Decomposition status and diagnostics. | Status follows approved qualitative relation. | Result remains interpretive. | No alpha promotion. | Candidate or production semantics. |
| All stages -> Traceability capture | Decisions, inputs, outputs, diagnostics. | Each stage emits traceable decision context. | End-to-end lineage exists. | Traceability is mandatory. | Untraceable output can be accepted. |
| All stages -> Fixture conformance | Stage behavior expectations. | Fixture category applies. | Future tests can verify behavior. | Fixture-first development. | Fixture behavior can be deferred until after real data. |

These are conceptual interfaces only, not APIs or programming-language interfaces.

## 6. Validity And Gating Sequence

Processing terminates at the first gate that makes scientific interpretation invalid, unless the approved fixture behavior explicitly allows governed exclusion.

Gating order:

1. Specification conformance gate: requested behavior must match approved science.
2. Observation role gate: inputs must be source-independent abstract roles.
3. Identity validity gate: target and comparator identities must be accepted or unresolved.
4. PIT validity gate: all roles must be valid for the historical relationship.
5. Temporal validity gate: \(B_t \prec H_t \preceq t \prec F_t\), and \(F_t\) must not enter explanatory inputs.
6. Post-stress gate: \(S_i(t)\) must be eligible; unresolved stress halts decomposition.
7. Comparator validity gate: comparator context must be accepted, aligned, sufficient, and non-conflicted.
8. Observation validity gate: own and comparator observations must be present and governed.
9. Coverage validity gate: missingness, terminal states, and delistings must not invalidate interpretation.
10. Formula availability gate: \(R_i(t)\), \(C_i(t)\), and \(D_i(t)\) may be derived only after prior gates pass.
11. Decomposition validity gate: qualitative relation must support common, idiosyncratic, mixed, or unresolved status.
12. Traceability gate: result must have complete lineage.

Termination states:

- fail-closed;
- unresolved;
- diagnostic-only;
- valid for interpretive output.

## 7. Formula Execution Sequence

The design preserves the approved formula without redefining it.

Observed quantities:

- target observation basis \(X_i(B_t,H_t)\);
- comparator repair bases for valid comparators;
- comparator context \(P_i(t)\);
- market context \(M(t)\);
- governance evidence roles.

Derived quantities:

- own repair \(R_i(t)\);
- valid comparator repair observations \(R_j(t)\);
- peer-common repair \(C_i(t)\);
- security-idiosyncratic repair \(D_i(t)\).

Decomposition:

- preserve \(D_i(t)=R_i(t)-C_i(t)\);
- preserve \(R_i(t)=C_i(t)+D_i(t)\).

Interpretation:

- assign \(Z_i(t)\) as predominantly common, predominantly idiosyncratic, mixed, or unresolved;
- keep \(Z_i(t)\) interpretive, not alpha or production status.

## 8. Diagnostics Design

Diagnostics are deterministic explanations attached to outputs. They never alter outputs.

| Diagnostic class | Meaning | Output effect |
|---|---|---|
| Unresolved outcome | Interpretation could not be assigned scientifically. | \(Z_i(t)\) unresolved with reason. |
| Invalid observation | Required observation role is absent, invalid, or unsupported. | Halt relevant processing. |
| Comparator failure | Comparator context is missing, insufficient, invalid, conflicted, or unstable. | Comparator unresolved; decomposition unresolved. |
| Ambiguity | Qualitative relation does not support a status. | Preserve unresolved. |
| Source conflict | Role authority or context evidence conflicts. | Unresolved unless future authority resolves. |
| Timing failure | Temporal ordering or no-future-leakage rule fails. | Fail closed. |
| Unsupported situation | Input relationship is outside approved scope. | Reject or diagnostic-only. |
| Traceability failure | A decision cannot be traced to approved specification. | Result cannot be accepted for research use. |

Diagnostics must be stable for identical conceptual inputs.

## 9. Traceability Design

Every implementation responsibility must trace to:

- Phase 5 scientific philosophy;
- first-module boundary;
- measurement specification;
- formula specification;
- implementation architecture;
- synthetic fixtures and acceptance categories.

Traceability chain:

Responsibility -> architectural component -> formula component or measurement concept -> fixture category -> scientific claim -> governance requirement.

Minimum trace obligations:

- observation role lineage;
- validity-gate lineage;
- comparator-context lineage;
- formula-quantity lineage;
- decomposition-status lineage;
- diagnostic lineage;
- unresolved-state lineage;
- fixture and acceptance-category lineage.

If a future implementation cannot preserve this lineage, it must not process real market data.

## 10. Acceptance-Test Mapping

| Responsibility | Synthetic fixtures | Acceptance-test categories | Architectural component | Formula component |
|---|---|---|---|---|
| Specification conformance | All fixture groups | Traceability, implementation independence | Scientific Specification Boundary | All components |
| Observation intake | F13, F15, fail-closed group | Reproducibility, unresolved-state behavior | Observation Boundary | \(X_i(B_t,H_t)\), governance roles |
| Measurement mapping | F1-F4, F13 | Traceability, decomposition consistency | Measurement Layer | \(S_i(t)\), \(R_i(t)\) basis |
| Validity gating | F6-F8, T1-T6, fail-closed group | Temporal consistency, fail-closed behavior | Validity Layer | \(V_i(t)\), \(V_j(t)\) |
| Comparator preparation | F5, F7, C1-C6 | Comparator correctness, contamination visibility | Comparator Context Layer | \(P_i(t)\), \(P_i^{*}(t)\), \(R_j(t)\) |
| Formula derivation | F1-F3, F10-F12, F15 | Algebraic consistency | Formula Layer | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\) |
| Decomposition interpretation | F1-F4, F14, D1-D4 | Decomposition consistency | Decomposition Layer | \(Z_i(t)\) |
| Result packaging | F9-F12, fail-closed group | Unresolved-state behavior, contamination visibility | Result Layer | \(Z_i(t)\), diagnostics |
| Traceability capture | All fixture groups | Traceability, reproducibility | Traceability Layer | All components |
| Fixture conformance | F1-F15, T1-T6, C1-C6, D1-D4, X1-X7 | All acceptance categories | Fixture Acceptance Boundary | All components |

Every responsibility has explicit verification coverage.

## 11. Engineering Invariants

Every implementation must preserve:

- deterministic behavior;
- source independence;
- reproducibility;
- mandatory traceability;
- fail-closed behavior;
- no hidden optimization;
- no hidden learning;
- no hidden prediction;
- no future leakage;
- no source-specific assumptions;
- no hidden peer construction;
- no hidden formula changes;
- no hidden measurement changes;
- no validation behavior inside implementation responsibilities;
- no production semantics;
- fixture compliance;
- acceptance-test compliance;
- separation of Alpha Information, Contextual Information, Governance Information, and interpretive outcomes.

## 12. Failure Handling

Failure handling includes termination condition, unresolved state, diagnostic, traceability, and downstream behavior.

| Failure mode | Termination condition | Result state | Diagnostic | Traceability | Downstream behavior |
|---|---|---|---|---|---|
| Specification mismatch | Requested behavior changes approved science. | Reject. | Spec conformance failure. | Link to violated spec. | No processing. |
| Source-specific assumption | Input role depends on source field/schema/vendor. | Reject. | Source-independence failure. | Observation boundary. | No processing. |
| Invalid identity | Target or comparator identity invalid. | Unresolved. | Identity gate failure. | Validity gate. | No formula use. |
| PIT violation | Future/current metadata enters historical role. | Fail closed. | PIT failure. | Temporal and validity gates. | No formula use. |
| Timing failure | \(B_t\), \(H_t\), \(t\), \(F_t\) ordering invalid. | Fail closed. | Timing failure. | Temporal gate. | No formula use. |
| Comparator failure | Comparator unavailable, insufficient, or conflicted. | Unresolved. | Comparator failure. | Comparator layer. | No decomposition. |
| Missing observations | Required own or comparator observations missing. | Unresolved unless governed exclusion applies. | Missing observation. | Observation gate. | No imputation. |
| Coverage failure | Missingness, delisting, or terminal-state issue invalidates interpretation. | Unresolved or diagnostic-only. | Coverage failure. | Coverage gate. | No research input. |
| Ambiguous decomposition | Qualitative relation cannot assign status. | Unresolved. | Ambiguity. | Decomposition layer. | Preserve negative/diagnostic evidence. |
| Traceability failure | Output cannot be linked to approved lineage. | Reject. | Traceability failure. | Trace layer. | No research use. |
| Unsupported situation | Request falls outside first-module scope. | Reject or diagnostic-only. | Scope failure. | Boundary spec. | No invented behavior. |

No failure mode may produce a default value, candidate, panel record, validation input, production output, or alpha claim.

## 13. Extensibility Design

Future modules may integrate by adding separate responsibilities adjacent to the first module, never by mutating the first-module responsibilities.

| Future module or layer | Integration rule | Protection |
|---|---|---|
| Asymmetry | Add separate asymmetry interpretation after scientific approval. | Do not change \(Z_i(t)\) v1 status logic. |
| Macro conditioning | Add macro-context responsibility after authority and known-date review. | Keep macro out of v1 formula. |
| VoV | Add VoV-specific responsibility only after contamination review. | No hidden VoV input to repair. |
| Stabilization | Add stabilization responsibility only if scientifically distinct. | Keep stabilization as confounder. |
| Participation | Add participation context/control separately. | No implicit participation input. |
| Liquidity | Add liquidity context/control separately. | No implicit liquidity input. |
| Additional contextual layers | Add through validity, traceability, and fixture-extension gates. | No bypass of context authority. |

Extensibility must preserve backward compatibility of the first-module scientific meaning.

## 14. Out-Of-Scope Engineering

Outside this design:

- source adapters;
- database schemas;
- APIs;
- package layout;
- filenames;
- programming languages;
- deployment;
- performance optimization;
- empirical discovery;
- validation;
- production monitoring;
- production artifacts;
- source access;
- data retrieval;
- real peer construction;
- formula optimization;
- parameter estimation;
- candidates;
- registries;
- panels;
- IC;
- governance changes;
- scientific conclusion changes;
- survivor-status changes;
- ML.

## 15. Pre-Coding Readiness Assessment

All conceptual engineering decisions required before writing code have now been completed.

Repository support:

- the scientific boundary defines the module;
- the measurement specification defines observable concepts;
- the formula specification defines symbolic execution and decomposition;
- the synthetic fixture specification defines expected behavior;
- the implementation architecture defines components and interactions;
- this note defines processing lifecycle, implementation responsibilities, conceptual interfaces, gating sequence, formula sequence, diagnostics, traceability, acceptance mapping, invariants, failure handling, extensibility, and out-of-scope engineering.

This assessment does not authorize production code. It supports only a bounded reference implementation in a separate lifecycle step.

Final classification restated: `DETAILED_IMPLEMENTATION_DESIGN_DEFINED`

## 16. Recommended Implementation Strategy

Recommended bounded implementation strategy:

1. Implement fixture-first behavior before any real market data path exists.
2. Implement deterministic validity gates before formula derivation.
3. Implement traceability capture alongside every responsibility, not after results.
4. Implement unresolved and fail-closed behavior before valid-path behavior is considered complete.
5. Implement formula derivation only from approved measurement concepts.
6. Implement decomposition interpretation only after formula quantities and validity gates are satisfied.
7. Verify acceptance-test categories before any source adapter, real data path, peer construction, discovery, or validation is considered.

No implementation technology is recommended.

## 17. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - First Module Reference Implementation v1`

This next step may begin a bounded reference implementation under the approved scientific specification stack. It must not retrieve data, construct real peers, perform discovery, perform validation, optimize formulas, create candidates, create registries, create panels, compute IC, modify governance, modify scientific conclusions, create production artifacts, alter survivor status, or introduce ML.
