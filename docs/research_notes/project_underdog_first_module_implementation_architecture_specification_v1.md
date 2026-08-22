# Project Underdog - First Module Implementation Architecture Specification v1

Date: 2026-07-17

## 1. Executive Classification

Final classification: `IMPLEMENTATION_ARCHITECTURE_DEFINED`

This note defines the source-independent implementation architecture required to preserve the approved scientific specification for:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

This classification refers only to implementation architecture readiness. It does not authorize coding, APIs, class hierarchies, package structures, database schemas, filenames, source access, data retrieval, real peer construction, discovery, validation, formula optimization, candidates, registries, panels, IC, production artifacts, governance changes, scientific conclusion changes, survivor-status changes, or ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: first-module boundary is common-versus-idiosyncratic post-stress repair decomposition.
- `docs/research_notes/project_underdog_first_module_source_independent_measurement_specification_v1.md`: measurement concepts and observation boundaries are defined.
- `docs/research_notes/project_underdog_first_module_formula_specification_v1.md`: symbol registry, temporal ordering, preferred formula, decomposition logic, and unresolved-state behavior are defined.
- `docs/research_notes/project_underdog_first_module_synthetic_fixture_and_acceptance_test_specification_v1.md`: conceptual fixtures, acceptance categories, invariants, and coverage are defined.
- `docs/research_notes/project_underdog_phase5_scientific_consistency_and_terminology_harmonization_review_v1.md`: Alpha Information, Contextual Information, Governance Information, maturity, readiness, and interpretive-outcome terminology are harmonized.
- `docs/research_notes/project_underdog_phase5_bounded_formula_and_implementation_readiness_review_v1.md`: implementation must follow source-independent scientific specification and preserve lifecycle gates.
- Phase 5 WS1-WS9 define authority, identity, context, hypothesis, contamination, falsification, reinterpretation, inventory, and ML constraints.
- Platform v2 and lifecycle governance preserve hypothesis-first discipline, reproducibility, artifact lineage, frozen horizons, bounded refinement, candidate discipline, validation separation, and negative-evidence preservation.

## 2. Architectural Philosophy

The architectural purpose is to make scientific violation difficult. Architecture is the separation of responsibilities, information flow, validity gates, traceability obligations, and failure behavior required before code can be designed.

Lifecycle distinctions:

| Layer | Meaning | Status here |
|---|---|---|
| Scientific specification | Defines the hypothesis, measurement concepts, formula, fixtures, and acceptance expectations. | Preserved as authoritative. |
| Architecture | Defines conceptual responsibilities and allowed component interactions. | Defined here. |
| Implementation | Concrete code, data structures, source adapters, execution behavior, and tests. | Not authorized. |
| Discovery | Empirical search, panels, IC, candidate evaluation, or threshold estimation. | Not authorized. |
| Validation | Frozen-horizon validation and survivor-status review. | Not authorized. |
| Production | Operational deployment, monitoring, thresholds, and production artifacts. | Not authorized. |

Architecture must privilege scientific correctness over engineering convenience. No component may silently introduce new scientific assumptions, hidden optimization, hidden prediction, source-specific behavior, or validation behavior.

## 3. High-Level Architecture

The complete conceptual architecture contains these major responsibilities:

| Component | Primary responsibility |
|---|---|
| Scientific Specification Boundary | Preserve the approved boundary, measurement, formula, fixture, and acceptance-test expectations. |
| Observation Boundary | Receive abstract observation roles without binding to sources or schemas. |
| Measurement Layer | Convert approved observation roles into measurement-level concepts. |
| Validity Layer | Evaluate identity, PIT, comparator, observation, temporal, coverage, and unresolved-state gates. |
| Comparator Context Layer | Hold accepted comparator context as contextual information without constructing peers inside formula logic. |
| Formula Layer | Produce source-independent derived quantities from valid measurement concepts. |
| Decomposition Layer | Interpret own repair, peer-common repair, and idiosyncratic repair into decomposition status. |
| Result Layer | Represent scientific outputs and unresolved outcomes without promotion to alpha, candidate, or production status. |
| Traceability Layer | Preserve lineage from scientific claim to observation, validity gates, formula components, fixture expectations, and future artifacts. |
| Fixture Acceptance Boundary | Ensure future implementations can be checked against synthetic fixture and acceptance-test expectations. |

The architecture is conceptual only. It does not define classes, APIs, database schemas, package layout, filenames, file formats, source adapters, or execution algorithms.

## 4. Responsibility Allocation

| Component | Responsibility | Inputs | Outputs | Dependencies | Prohibited responsibilities |
|---|---|---|---|---|---|
| Scientific Specification Boundary | Keep implementation aligned with approved science. | Boundary note, measurement spec, formula spec, fixture spec, governance notes. | Architectural constraints and traceability obligations. | Phase 5 philosophy and Platform v2. | Changing scientific conclusions or expanding module scope. |
| Observation Boundary | Accept only abstract observation roles. | Target observation role, comparator observation role, market context role, governance evidence role. | Source-independent observation package. | Measurement spec and formula symbol registry. | Source binding, data retrieval, field mapping, schema definition. |
| Measurement Layer | Express observations as approved measurement concepts. | Source-independent observation package. | Post-stress context, own repair basis, comparator repair basis, contextual controls. | Measurement spec. | Formula execution, validation, peer construction, source adaptation. |
| Validity Layer | Decide whether each observation relationship may be interpreted. | Measurement concepts, context roles, identity/context/timing evidence roles. | Pass, fail-closed, diagnostic-only, or unresolved validity status. | WS1 authority, WS2 identity, WS3 context, formula unresolved logic. | Imputation, optimization, forced decomposition. |
| Comparator Context Layer | Hold comparator context as contextual information. | Accepted comparator context role and comparator observation roles. | Valid comparator observation set or unresolved comparator status. | Economic-context science and formula spec. | Constructing real peers, choosing vendors, selecting taxonomies, optimizing membership. |
| Formula Layer | Derive formula quantities. | Valid own repair, valid comparator repair, accepted comparator set, validity status. | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\), and formula availability status. | Formula spec. | Source logic, comparator construction, validation, optimization, prediction. |
| Decomposition Layer | Assign interpretive decomposition status. | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\), validity status, qualitative relation status. | \(Z_i(t)\): common, idiosyncratic, mixed, or unresolved. | Formula spec and fixture spec. | Alpha promotion, threshold estimation, candidate creation. |
| Result Layer | Preserve final scientific result semantics. | Derived quantities, decomposition status, validity status, traceability references. | Scientific result record concept. | Decomposition layer and traceability layer. | Production signal, panel output, validation result, portfolio action. |
| Traceability Layer | Preserve scientific lineage. | All component decisions and source-independent evidence roles. | Trace path from philosophy through measurement, formula, architecture, and future verification. | Fixture spec, Platform v2, lifecycle governance. | Hiding assumptions or accepting untraceable outputs. |
| Fixture Acceptance Boundary | Ensure architecture can satisfy fixtures later. | Fixture cases, acceptance categories, invariants. | Future check requirements and architectural conformance expectations. | Synthetic fixture spec. | Executable tests, code generation, implementation benchmarks. |

Each component has exactly one primary responsibility.

## 5. Information Flow Architecture

Conceptual flow:

1. Input observations enter as abstract roles.
2. The Observation Boundary rejects source-specific assumptions and passes only source-independent observation roles.
3. The Measurement Layer maps observation roles to approved measurement concepts.
4. The Validity Layer evaluates identity, PIT, comparator, observation, temporal, coverage, and reproducibility gates.
5. The Comparator Context Layer supplies valid contextual comparator observations, or unresolved comparator status.
6. The Formula Layer derives own repair, peer-common repair, and idiosyncratic contrast only when validity permits.
7. The Decomposition Layer assigns common, idiosyncratic, mixed, or unresolved interpretation.
8. The Result Layer preserves the scientific result as interpretive output, not alpha status.
9. The Traceability Layer records the scientific lineage of every input, gate, derived quantity, and result.
10. Future validation may later consume approved implementation artifacts only after separate lifecycle authorization.

Every transition must preserve source independence and fail-closed behavior.

## 6. Measurement Architecture

The Measurement Layer interfaces with later components by providing only approved scientific observation concepts:

- post-stress context;
- own-security repair basis;
- comparator repair basis;
- market-context control;
- contextual-control markers;
- observability status.

It must remain completely source-independent. It must not know vendor fields, source schemas, storage formats, source access paths, database layout, or implementation mechanics.

The Measurement Layer must not:

- construct comparator sets;
- run formulas;
- assign decomposition status;
- perform validation;
- create candidates;
- estimate thresholds;
- fill missing observations;
- promote context to alpha.

Its architecture exists to preserve the measurement specification before formula logic appears.

## 7. Formula Architecture

The Formula Layer receives only valid measurement concepts and comparator context already cleared by the Validity Layer.

Allowed responsibility:

- represent \(R_i(t)\), \(C_i(t)\), and \(D_i(t)\) according to the formula specification;
- preserve \(R_i(t)=C_i(t)+D_i(t)\) where valid;
- preserve formula unavailable status when prerequisites fail.

The Formula Layer must remain isolated from:

- source adapters or source-specific logic;
- comparator construction;
- validation and discovery;
- optimization;
- threshold estimation;
- candidate or registry logic;
- production behavior.

This isolation prevents formula code, when later designed, from becoming a hidden source adapter, peer optimizer, or prediction engine.

## 8. Comparator Architecture

Comparator information is contextual. Its architectural role is to supply accepted economic comparator observations to the formula, not to create an alpha signal.

Architectural boundaries:

- Comparator construction is outside the Formula Layer.
- Comparator authority and identity checks are handled by the Validity Layer.
- Comparator context enters the Formula Layer only after being accepted as valid for the observation relationship.
- Comparator failures must produce unresolved comparator status, not default idiosyncratic repair.
- Comparator ambiguity must remain visible to the Result and Traceability Layers.

Prohibited comparator behavior:

- constructing real peer groups inside this architecture note;
- choosing a source or taxonomy;
- optimizing membership;
- using current-state labels historically;
- allowing future-known peers;
- letting comparator repair become a hidden alpha mechanism;
- allowing peer insufficiency to be ignored.

## 9. Validity Architecture

The Validity Layer is the central fail-closed gate.

Conceptual gates:

| Gate | Purpose | Failure behavior |
|---|---|---|
| Identity validity | Confirm target and comparators refer to accepted identities. | Unresolved before formula use. |
| PIT validity | Confirm all identity, context, and membership evidence is valid for the historical relationship. | Fail closed. |
| Comparator validity | Confirm comparator context is accepted, sufficient, aligned, and non-conflicted. | Comparator unresolved; decomposition unresolved. |
| Observation validity | Confirm required own and comparator observations are present and governed. | Governed exclusion or unresolved. |
| Temporal validity | Confirm \(B_t \prec H_t \preceq t \prec F_t\) and no future leakage. | Fail closed. |
| Coverage validity | Confirm missingness and terminal-state issues do not invalidate interpretation. | Unresolved or diagnostic-only. |
| Reproducibility validity | Confirm observation lineage can be preserved or reconstructed in future accepted evidence. | Unresolved or diagnostic-only. |
| Decomposition validity | Confirm qualitative relations can support common, idiosyncratic, mixed, or unresolved status. | Unresolved when ambiguous. |

Validity output must be deterministic. Invalid evidence may never be repaired through hidden imputation, default peers, current metadata, fallback taxonomies, or after-the-fact interpretation.

## 10. Traceability Architecture

Traceability must preserve the full lineage:

Scientific philosophy -> first-module boundary -> measurement specification -> formula specification -> synthetic fixture specification -> implementation architecture -> future detailed design -> future implementation -> future validation.

Traceability obligations:

- every observation must map to an approved observable concept;
- every derived quantity must map to a formula component;
- every validity decision must map to a governance requirement;
- every unresolved result must map to a specific failed or ambiguous prerequisite;
- every decomposition result must map to the formula and qualitative interpretation basis;
- every future fixture or acceptance test must map to the fixture specification;
- every future implementation artifact must preserve this lineage before empirical use.

Traceability must not become decorative metadata. It is the architecture's protection against silent scientific drift.

## 11. Failure Architecture

Failure handling is deterministic and fail-closed.

| Failure class | Architectural handling |
|---|---|
| Invalid observations | Block formula use and return unresolved or diagnostic-only status. |
| Comparator failures | Block \(C_i(t)\), \(D_i(t)\), and \(Z_i(t)\) unless governed exclusion leaves valid context. |
| Timing failures | Fail closed before formula use. |
| Ambiguity | Preserve unresolved status; do not force classification. |
| Source conflicts | Unresolved unless future source-role authority resolves the conflict. |
| Unresolved decomposition | Return unresolved result with traceable cause. |
| Unsupported situations | Reject or diagnostic-only; do not invent behavior. |
| Missing observations | Governed exclusion only where scientifically allowed; otherwise unresolved. |
| Current-state metadata use | Fail closed for historical interpretation. |
| Future-known evidence | Fail closed. |

No failure path may produce a default alpha signal, candidate, panel value, validation input, or production output.

## 12. Component Interaction Matrix

Allowed interactions:

| Component A | Allowed interaction | Component B |
|---|---|---|
| Scientific Specification Boundary | constrains | Observation Boundary |
| Scientific Specification Boundary | constrains | Measurement Layer |
| Scientific Specification Boundary | constrains | Formula Layer |
| Scientific Specification Boundary | constrains | Decomposition Layer |
| Observation Boundary | provides source-independent roles to | Measurement Layer |
| Measurement Layer | provides approved measurement concepts to | Validity Layer |
| Measurement Layer | provides valid measurement concepts to | Formula Layer |
| Validity Layer | gates | Comparator Context Layer |
| Validity Layer | gates | Formula Layer |
| Validity Layer | gates | Decomposition Layer |
| Comparator Context Layer | provides valid comparator observations to | Formula Layer |
| Formula Layer | provides derived quantities to | Decomposition Layer |
| Decomposition Layer | provides interpretive status to | Result Layer |
| Result Layer | provides output semantics to | Traceability Layer |
| Fixture Acceptance Boundary | constrains expected behavior of | all architecture components |
| Traceability Layer | records lineage from | all architecture components |

Prohibited interactions:

| Component A | Prohibited interaction | Component B |
|---|---|---|
| Formula Layer | direct dependence on | source adapters or source-specific fields |
| Formula Layer | constructs or optimizes | Comparator Context Layer |
| Formula Layer | performs | validation or discovery |
| Measurement Layer | retrieves data from | external sources |
| Measurement Layer | creates | peer groups |
| Comparator Context Layer | promotes comparator repair into | Alpha Information |
| Decomposition Layer | creates | candidates or production signals |
| Result Layer | modifies | governance or survivor status |
| Validation | feeds back into | Measurement Layer or Formula Layer without separate lifecycle review |
| Future detailed design | changes | scientific boundary or formula specification |
| Fixture Acceptance Boundary | becomes | executable code or implementation benchmark in this note |

## 13. Engineering Invariants

Every future implementation design must preserve:

- source independence;
- reproducibility;
- deterministic behavior;
- scientific traceability;
- implementation independence from vendor, schema, language, and storage choices;
- bounded responsibilities;
- no hidden optimization;
- no hidden prediction;
- no hidden learning;
- no hidden peer construction;
- no hidden source fallback;
- no current-state metadata in historical interpretation;
- no future leakage;
- no validation feedback into formula behavior;
- no expansion beyond repair decomposition;
- deterministic unresolved-state behavior;
- compliance with synthetic fixtures and acceptance-test expectations.

## 14. Extensibility Assessment

The architecture can support future modules by adding new scientifically approved components adjacent to, not inside, the first-module core.

Future extension principles:

| Future work | Extension approach | Protection for first module |
|---|---|---|
| Asymmetry | Add a separate asymmetry interpretation component after scientific approval. | Do not modify v1 decomposition status logic. |
| Macro conditioning | Add a deferred macro-context layer after authority and known-date review. | Keep macro outside v1 comparator and formula. |
| VoV | Add as a separate contextual or alpha-family component only after contamination review. | Do not import VoV into repair formula. |
| Stabilization | Add a stabilization-specific module if scientifically distinct. | Preserve stabilization as confounder in v1. |
| Participation | Add participation context or control only under separate specification. | Do not make participation an implicit repair input. |
| Liquidity | Add liquidity context or control only under separate specification. | Do not make liquidity an implicit repair input. |
| Additional contextual layers | Add new context layers through validity and traceability gates. | Do not bypass comparator validity or source authority. |

The first module remains stable because formula logic, comparator context, validity gates, result interpretation, and traceability are separated. Future modules may reuse the architecture pattern without rewriting the first-module scientific meaning.

## 15. Implementation Boundary

Outside this architecture:

- code;
- APIs;
- class hierarchies;
- database schemas;
- package structures;
- filenames;
- file formats;
- concrete algorithms;
- source adapters;
- source access;
- data retrieval;
- dataset construction;
- real peer construction;
- formula optimization;
- parameter estimation;
- discovery;
- validation;
- production;
- candidates;
- registries;
- panels;
- IC;
- governance modifications;
- scientific conclusion changes;
- survivor-status changes;
- ML.

This note defines architecture only.

## 16. Readiness Conclusion

Project Underdog now has a complete pre-coding implementation architecture for the first module.

Repository support:

- the first-module boundary defines the scientific scope;
- the measurement specification defines approved observations;
- the formula specification defines mathematical relationships and unresolved-state logic;
- the synthetic fixture and acceptance-test specification defines expected conceptual behavior;
- contamination, falsification, traceability, reproducibility, and lifecycle governance define guardrails;
- this note defines architecture components, responsibilities, information flow, validity, traceability, failure behavior, interactions, invariants, extensibility, and implementation boundaries.

This conclusion does not authorize implementation. It supports only moving to detailed implementation design in a separate lifecycle note.

Final classification restated: `IMPLEMENTATION_ARCHITECTURE_DEFINED`

## 17. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - First Module Detailed Implementation Design v1`

This next step may define a detailed non-coding implementation design under the approved architecture. It must not write code, define production APIs, construct real peers, retrieve data, perform discovery, perform validation, optimize formulas, create candidates, create registries, create panels, compute IC, modify governance, modify scientific conclusions, create production artifacts, alter survivor status, or introduce ML.
