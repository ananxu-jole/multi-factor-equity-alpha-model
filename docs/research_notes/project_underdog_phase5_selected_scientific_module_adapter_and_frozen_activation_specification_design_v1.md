# Project Underdog - Phase 5 Selected Scientific Module Adapter And Frozen Activation Specification Design v1

Date: 2026-08-07

Final classification: `SELECTED_MODULE_ADAPTER_AND_FROZEN_ACTIVATION_SPECIFICATION_DESIGN_DEFINED`

This note defines the design-only boundary for the selected Phase 5 module adapter and its frozen activation specification. The design does not implement code, modify existing implementations, activate a scientific module, authorize scientific execution, define formulas, compute measurements, construct peers, generate candidates, create panels, calculate IC, validate, productionize, change thresholds, alter survivor status, or introduce ML.

Repository evidence reviewed:

- `docs/research_notes/project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_executable_conformance_rereview_v2.md`: the Activation Registry and Execution Authorization implementation is fully conformant, the broad selected program remains distinct from the narrow activation specification, and handoff-chain mismatches fail closed.
- `docs/research_notes/project_underdog_phase5_scientific_module_intake_platform_integration_readiness_and_first_scientific_module_activation_design_v1.md`: the current Platform v2 path is Prepared Observations -> Scientific Module Intake -> Platform Activation -> Module Adapter -> Module Runtime -> Scientific Output Review, with module adapter ownership limited to translation from intake handoff to module-local input contract.
- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: the broad program `Peer-Relative Post-Stress Repair And Stabilization Asymmetry` is too wide for first activation, and the narrow first-module boundary is `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.
- `docs/research_notes/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.md`: Scientific Module Intake is a metadata evaluator that preserves Prepared Observation diagnostics, roles, limitations, temporal metadata, traces, reproducibility metadata, and artifact lineage, and its handoff is bounded structural metadata only.
- `docs/research_notes/project_underdog_phase5_prepared_observations_reference_implementation_v1.md`: Prepared Observations assembles synthetic, metadata-qualified, temporally aligned, traceable packages and forbids interpolation, filling, resampling, role promotion, or raw evidence bypass.
- `docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md`: Comparator Construction emits restricted comparator relationship metadata and diagnostics, not formulas, peer rankings, similarity scores, or scientific measurements.

## 1. Purpose

The Selected Scientific Module Adapter exists to provide platform compatibility between an execution-authorized intake handoff and the frozen input contract required by the first selected scientific module.

It has four distinct meanings:

| Concept | Meaning | Adapter implication |
| --- | --- | --- |
| Platform compatibility | The upstream Platform v2 chain has produced the required governance artifacts in the required order. | The adapter may only accept an authorized intake handoff after Activation Registry and Execution Authorization have accepted it. |
| Structural compatibility | The handoff fields, versions, roles, diagnostics, lineage, and reproducibility metadata can be represented in the frozen module input contract without reinterpretation. | The adapter may map fields and metadata only when all mandatory references and versions match. |
| Scientific compatibility | The input is scientifically suitable for a future module to evaluate under a frozen hypothesis boundary. | The adapter does not establish this by itself; it preserves evidence needed for later scientific review. |
| Scientific execution | The module performs measurement, decomposition, scoring, interpretation, or hypothesis evaluation. | The adapter never executes science and must not produce scientific outputs. |

The adapter therefore answers one bounded design question: can an authorized and intake-compatible Prepared Observation package be structurally transformed into a frozen module input package without altering scientific meaning?

## 2. Architectural position

The required path is:

```text
Prepared Observations
        ↓
Scientific Module Intake
        ↓
Activation Registry
        ↓
Execution Authorization
        ↓
Selected Module Adapter
        ↓
Frozen Module Input
        ↓
Scientific Module
```

No bypass is permitted.

The adapter must not consume raw Source Authority records directly. It must not consume PIT Identity and Context Evidence directly. It must not consume Comparator Construction records directly. It must not consume Prepared Observation packages that have not passed through Scientific Module Intake. It must not consume intake output that has not been bound to an Activation Registry declaration and an Execution Authorization decision. It must not self-authorize execution.

## 3. Responsibility boundary

The adapter owns only:

- structural mapping;
- metadata translation;
- contract verification;
- lineage preservation;
- reproducibility metadata preservation;
- version compatibility checks;
- frozen activation verification.

The adapter explicitly refuses:

- formulas;
- measurements;
- factors;
- alpha computation;
- comparator construction;
- peer discovery;
- ranking;
- optimization;
- validation;
- production;
- ML.

The adapter is neither part of Prepared Observations nor part of Scientific Module Intake. It is a downstream structural bridge. It is also not part of the scientific module itself. The future module may consume a frozen input package, but the adapter may not decide what the package means scientifically.

## 4. Frozen activation specification

The immutable activation specification is:

| Field | Frozen value or rule |
| --- | --- |
| Specification identity | `project_underdog_phase5_selected_scientific_module_adapter_and_frozen_activation_specification_design_v1` |
| Specification version | `v1` |
| Selected broad module | `Peer-Relative Post-Stress Repair And Stabilization Asymmetry` |
| Narrow activation boundary | `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition` |
| Primary information role | `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION` |
| Permitted scientific scope | Structural preparation for a future module that may distinguish common post-stress repair from security-specific repair using historically valid economic peers and pre-defined post-stress context. |
| Prohibited scope | Stabilization as a co-primary module, asymmetry expansion, peer leadership, deterioration, VoV reinterpretation, participation repair reinterpretation, volatility compression reinterpretation, formulas, scoring, ranking, candidate generation, panel construction, IC, validation, production, optimization, and ML. |
| Frozen horizon references | Inherited from Execution Authorization and the authoritative activation/handoff chain; the adapter may verify horizon reference identity but must not select, alter, rescue, or expand horizons. |
| Required upstream artifacts | Source Authority lineage, PIT lineage, Comparator lineage, Prepared Observation package, Scientific Module Intake evaluation, authorized intake handoff, Activation Registry declaration, Execution Authorization decision. |
| Required contracts | Prepared Observation contract, Scientific Module Intake contract, authorized handoff contract, adapter design contract, frozen activation specification, frozen module input contract. |
| Required versions | Exact version compatibility for module id/version, activation specification, frozen horizon reference, adapter version, contract version, lineage schema, role schema, diagnostic schema, and reproducibility schema. |
| Governance bindings | Platform v2 fail-closed discipline, frozen-horizon discipline, role-preservation discipline, diagnostic-preservation discipline, artifact-lineage discipline, reproducibility discipline, contamination and falsification governance, and no-scientific-execution boundary. |

The broad research program and the narrow frozen activation specification are intentionally distinct. The adapter must fail closed if a request uses the broad program title to widen the frozen input scope beyond `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.

## 5. Adapter invariant

Every adapter result must reference all of the following:

- activation declaration;
- execution authorization;
- intake evaluation;
- prepared observation package;
- Source Authority lineage;
- PIT lineage;
- Comparator lineage;
- module specification;
- frozen activation specification;
- module input contract;
- reproducibility metadata.

Missing mandatory references fail closed.

The invariant is stronger than a truthy handoff flag. A result may not be adapted simply because `handoff_complete` or an equivalent field is true. It must match the authoritative activation declaration, execution authorization, intake evaluation, Prepared Observation package, handoff contract, adapter contract, input/output contract, scientific specification, and frozen horizon chain.

## 6. Structural mapping model

The structural mapping model is source-independent and metadata-only:

| Handoff element | Frozen module input placement | Allowed operation | Prohibited operation |
| --- | --- | --- | --- |
| Target observation | Target observation reference slot | Copy identifier, role, time, readiness, diagnostics, limitations, and lineage references. | Compute repair, infer decomposition, fill missing observations, or create measurement values. |
| Comparator metadata | Comparator context slot | Copy eligible comparator relationship metadata, restrictions, exclusions, duplication flags, temporal applicability, and lineage references. | Construct peers, rank comparators, score similarity, infer economic comparability, or synthesize comparator sets. |
| Context metadata | Context/control slot | Preserve declared context roles, temporal status, limitations, and diagnostics. | Promote context labels into factors, signals, or ungoverned peer definitions. |
| Observation time | Temporal coordinate slot | Copy observation date/time metadata and frozen-horizon references exactly. | Interpolate, resample, align by convenience, backfill, forward-fill, or reconstruct history. |
| Roles | Role-binding slot | Preserve exact role names and declared cardinality. | Alias roles, substitute roles, infer roles from attachment type, or promote diagnostic/negative roles. |
| Diagnostics | Diagnostic collection slot | Copy inherited diagnostics and adapter diagnostics deterministically. | Delete, downgrade, rename, normalize, or reinterpret diagnostics. |
| Limitations | Limitation collection slot | Copy limitations exactly and add adapter limitations separately if needed. | Treat limitations as acceptance evidence or repair them. |
| Lineage | Artifact-lineage slot | Propagate Source Authority, PIT, Comparator, Prepared Observations, Intake, Activation, Execution Authorization, Adapter, Frozen Specification, and Frozen Input Contract references. | Create scientific execution lineage or hide upstream provenance. |
| Reproducibility | Reproducibility slot | Preserve stable version and serialization metadata. | Add nondeterministic enrichment, external retrieval, source queries, or mutable references. |

No scientific transformation is permitted.

## 7. Information-role preservation

Information roles must be preserved exactly.

Diagnostic evidence cannot become alpha input. Comparator metadata cannot become measurements. Context metadata cannot become factors. Negative evidence cannot be promoted. Explanatory metadata cannot become a target observation. A comparator attachment cannot substitute for target evidence. A context attachment cannot substitute for peer membership evidence. A limitation cannot substitute for authority.

The frozen first-module role is `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION`. The adapter may only map handoff evidence into that role when the authorized intake handoff already accepted that role under the frozen module contract. It may not infer the role from file names, title strings, field shape, current metadata, or apparent relevance.

## 8. Temporal preservation

Observation times remain unchanged.

The adapter must preserve:

- observation time;
- event or stress-context time where supplied by the authorized handoff;
- effective-date metadata already present in upstream artifacts;
- source-known or project-known metadata already present in upstream artifacts;
- frozen horizon reference;
- temporal compatibility diagnostics;
- temporal limitations.

The adapter performs no:

- interpolation;
- repair;
- fill;
- smoothing;
- resampling;
- reconstruction.

The adapter must not create point-in-time logic, conservative lag rules, availability-date assumptions, or horizon choices. Temporal incompatibility, missing temporal references, or horizon mismatch must fail closed or remain explicitly diagnostic according to the failure-precedence model.

## 9. Frozen contract verification

Frozen contract verification is deterministic and metadata-only. It must verify:

- module version;
- activation specification;
- frozen horizon;
- adapter version;
- contract version;
- Source Authority lineage;
- PIT lineage;
- Comparator lineage;
- Prepared Observation lineage;
- Intake lineage;
- Activation lineage;
- Execution Authorization lineage;
- reproducibility metadata;
- role schema;
- diagnostic schema.

Verification has no scientific fallback. A semantically plausible package with a version mismatch is not structurally acceptable. A package with the correct module title but wrong narrow activation boundary is not structurally acceptable. A package with complete Prepared Observation metadata but missing execution authorization is not structurally acceptable.

## 10. Adapter output contract

The adapter output is a metadata-only frozen module input package.

It may include:

- adapter result id;
- adapter design version;
- frozen activation specification id/version;
- module id/version;
- module input contract id/version;
- authorized handoff reference;
- activation declaration reference;
- execution authorization reference;
- Prepared Observation package reference;
- copied target observation metadata;
- copied comparator metadata;
- copied context metadata;
- copied temporal metadata;
- copied diagnostics and limitations;
- adapter diagnostics and limitations;
- artifact-lineage references;
- reproducibility metadata;
- compatibility state.

It must include no:

- signals;
- factors;
- scores;
- predictions;
- measurements;
- candidates;
- validation.

The adapter output is not a scientific result. It is only the frozen structural input boundary that a separately authorized scientific module could later consume.

## 11. Failure precedence

Failure precedence should be deterministic and fail closed in this order:

1. Excluded activation: requested activation is outside the frozen narrow boundary.
2. Invalid authorization: Execution Authorization is missing, denied, expired, superseded, inactive, or mismatched.
3. Missing references: mandatory activation, authorization, intake, Prepared Observation, Source Authority, PIT, Comparator, module, contract, lineage, or reproducibility references are absent.
4. Version mismatch: module, activation specification, frozen horizon, adapter, input contract, role schema, diagnostic schema, lineage schema, or reproducibility schema versions do not match.
5. Lineage mismatch: upstream artifact chain does not match the authoritative handoff chain.
6. Contract mismatch: handoff contract cannot be represented in the frozen module input contract.
7. Role mismatch: required role is absent, unsupported, substituted, duplicated beyond allowed cardinality, prohibited, or promoted from diagnostic/negative/explanatory metadata.
8. Reproducibility failure: required stable serialization, fixture/version reference, or reconstruction metadata is absent or inconsistent.
9. Unresolved: upstream or adapter diagnostics indicate unresolved scientific or structural ambiguity.
10. Conditional: non-fatal limitations remain and must be preserved without promotion.

Fatal failures cannot be masked by later conditional states. Conditional limitations cannot convert a failed result into a usable frozen input.

## 12. Diagnostics

Adapter diagnostics are deterministic metadata diagnostics only.

Examples of adapter diagnostics include:

- `EXCLUDED_ACTIVATION_SCOPE`;
- `INVALID_EXECUTION_AUTHORIZATION`;
- `MISSING_ACTIVATION_DECLARATION`;
- `MISSING_INTAKE_EVALUATION`;
- `MISSING_PREPARED_OBSERVATION_PACKAGE`;
- `MISSING_SOURCE_AUTHORITY_LINEAGE`;
- `MISSING_PIT_LINEAGE`;
- `MISSING_COMPARATOR_LINEAGE`;
- `MODULE_VERSION_MISMATCH`;
- `ACTIVATION_SPECIFICATION_MISMATCH`;
- `FROZEN_HORIZON_MISMATCH`;
- `ADAPTER_VERSION_MISMATCH`;
- `INPUT_CONTRACT_MISMATCH`;
- `ROLE_SCHEMA_MISMATCH`;
- `DIAGNOSTIC_SCHEMA_MISMATCH`;
- `ROLE_SUBSTITUTION_PROHIBITED`;
- `DIAGNOSTIC_PROMOTION_PROHIBITED`;
- `NEGATIVE_EVIDENCE_PROMOTION_PROHIBITED`;
- `TEMPORAL_MUTATION_PROHIBITED`;
- `LINEAGE_CHAIN_MISMATCH`;
- `REPRODUCIBILITY_METADATA_INCOMPLETE`;
- `SCIENTIFIC_EXECUTION_PROHIBITED`.

No diagnostic may represent alpha quality, expected return, IC, Sharpe, predictive support, empirical independence, validation success, or production readiness.

## 13. Artifact lineage

The adapter must propagate the full artifact lineage chain:

- Source Authority;
- PIT;
- Comparator;
- Prepared Observations;
- Intake;
- Activation;
- Execution Authorization;
- Adapter;
- Frozen Specification;
- Frozen Input Contract.

The adapter may create adapter-lineage and frozen-input-lineage records as structural artifacts. It must not create scientific execution artifacts. It must not invent missing upstream lineage. It must not collapse distinct upstream lineages into a single convenience reference.

## 14. Compatibility

The design is compatible with the current Platform v2 stack without modifying it:

| Component | Compatibility requirement | No-modification boundary |
| --- | --- | --- |
| First Module Reference Implementation | The adapter may target a module-local frozen input shape, but must not execute the First Module or change its scientific boundary. | No repair decomposition, formula behavior, or module-runtime change. |
| Source Authority | Source Authority lineage is inherited through Prepared Observations and Intake. | No source acceptance, source selection, source retrieval, or authority reevaluation. |
| PIT Identity and Context Evidence | PIT lineage and diagnostics are inherited. | No identity construction, ticker lineage construction, context construction, or PIT repair. |
| Comparator Construction | Comparator lineage and restricted metadata are inherited. | No peer construction, comparator synthesis, ranking, or similarity scoring. |
| Prepared Observations | Prepared Observation package metadata is consumed only through the authorized handoff chain. | No package recomputation, temporal repair, raw evidence attachment, or role promotion. |
| Scientific Module Intake | Intake evaluation and bounded handoff are required inputs. | No re-intake, bypass, or compatibility reinterpretation. |
| Activation Registry | Activation declaration binds the selected broad program to the narrow frozen activation boundary. | No registry mutation, activation state change, or module selection change. |

The adapter is compatible precisely because it adds no new scientific authority or data behavior.

## 15. Scientific boundary

The adapter is not scientific execution.

It performs no:

- repair decomposition;
- peer analysis;
- stabilization;
- asymmetry;
- measurement;
- formulas;
- scoring;
- alpha generation.

The phrase `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition` names the frozen module input boundary, not an adapter computation. The adapter may preserve references needed by a future module to study that boundary, but it may not evaluate common repair, idiosyncratic repair, relative repair, stabilization, asymmetry, or any alpha implication.

## 16. Implementation readiness

Bounded synthetic reference implementation readiness is achieved at the design level.

This conclusion is narrow. It means a future implementation task could implement deterministic adapter structs, contract checks, fail-closed diagnostics, lineage propagation, reproducibility metadata, stable serialization, synthetic acceptance fixtures, synthetic rejection fixtures, and no-scientific-output refusal flags.

It does not mean:

- scientific execution is authorized;
- the first module is activated;
- the frozen module input contains real evidence;
- formulas are ready;
- peer-relative decomposition is measured;
- candidates or panels are ready;
- IC or validation is ready;
- production is ready;
- thresholds or survivor status may change;
- ML is introduced.

Reference implementation readiness is justified because the upstream governance chain is complete through Execution Authorization, the broad and narrow module identities are already distinguished, and the remaining adapter task is structural rather than scientific.

## 17. Synthetic acceptance scenarios

Future synthetic implementation should include acceptance scenarios such as:

| Scenario | Setup | Expected adapter behavior |
| --- | --- | --- |
| Complete authorized chain | Prepared Observation -> compatible Intake -> active Activation -> valid Execution Authorization -> matching adapter and frozen input contract. | Emit metadata-only frozen input with all mandatory references and no scientific outputs. |
| Conditional upstream limitation | Authorized handoff includes non-fatal limitations. | Preserve limitations exactly; output remains conditional if allowed by contract. |
| Required comparator metadata present | Authorized handoff includes required comparator metadata and lineage. | Copy comparator metadata into frozen comparator slot without ranking or measurement. |
| Required context metadata present | Authorized handoff includes required context/control metadata. | Copy context metadata into frozen context slot without factor promotion. |
| Stable repeated adaptation | Identical authorized handoff adapted twice. | Produce identical diagnostics, limitations, lineage ordering, compatibility state, and stable serialization. |

These are structural acceptance scenarios only. They do not prove scientific validity.

## 18. Synthetic rejection scenarios

Future synthetic implementation should include rejection scenarios such as:

| Scenario | Setup | Required adapter response |
| --- | --- | --- |
| Broad scope requested as frozen input | Request names `Peer-Relative Post-Stress Repair And Stabilization Asymmetry` without the narrow decomposition boundary. | Fail closed with excluded or mismatched activation-scope diagnostic. |
| Missing execution authorization | Intake handoff exists but no valid authorization exists. | Fail closed before mapping. |
| Wrong handoff chain | Handoff references wrong Prepared Observation package or wrong intake evaluation. | Fail closed with lineage or handoff-chain mismatch. |
| Missing Source Authority/PIT/Comparator lineage | Required upstream lineage absent. | Fail closed; no invented lineage. |
| Role promotion attempt | Diagnostic, comparator, context, or negative evidence is used as target decomposition evidence. | Fail closed with prohibited role-use diagnostic. |
| Temporal mutation attempt | Adapter is asked to interpolate, fill, smooth, resample, or reconstruct time metadata. | Fail closed with temporal-mutation diagnostic. |
| Scientific output attempt | Adapter is asked to emit measurements, scores, signals, candidates, panels, or validation metadata. | Fail closed with scientific-execution-prohibited diagnostic. |

## 19. Governance artifacts

Before any future adapter implementation, the conceptual governance artifacts should be:

- adapter design record;
- frozen activation specification;
- adapter input contract;
- frozen module input contract;
- output boundary declaration;
- failure-precedence matrix;
- diagnostic inventory;
- lineage propagation map;
- reproducibility metadata map;
- synthetic acceptance scenario inventory;
- synthetic rejection scenario inventory;
- no-scientific-execution declaration;
- open-assumption register.

These are conceptual or synthetic platform artifacts only. They are not source records, identity records, comparator records, peer groups, formulas, candidate registries, panels, validation artifacts, production artifacts, or ML artifacts.

## 20. Relationship to Activation Registry

The Activation Registry defines whether a declared module activation exists, is active, matches the selected module, and binds the broad selected program to the narrow activation specification.

The adapter consumes that declaration. It must not:

- create activation declarations;
- modify activation state;
- supersede activations;
- retire activations;
- reinterpret inactive activations;
- widen the selected scope;
- treat registry metadata as scientific evidence.

If the registry and the adapter request disagree, the registry-bound authoritative declaration controls and the adapter fails closed.

## 21. Relationship to Execution Authorization

Execution Authorization decides whether a specific activation request may proceed to the adapter boundary.

The adapter consumes authorization. It must not:

- self-authorize;
- override denied authorization;
- downgrade authorization diagnostics;
- treat incomplete handoff evidence as sufficient;
- create an execution result;
- declare that the scientific module ran.

The adapter may only operate after valid authorization and only within the authorized request context.

## 22. Relationship to Scientific Module Intake

Scientific Module Intake determines whether a Prepared Observation package is compatible with a module intake contract and emits a bounded handoff.

The adapter consumes the authorized intake handoff. It must not:

- re-evaluate intake compatibility;
- recompute Prepared Observation readiness;
- infer missing required roles;
- repair inherited diagnostics;
- bypass intake with raw Prepared Observation packages;
- consume direct upstream artifacts in place of the intake handoff.

Intake owns compatibility into the module-intake boundary. The adapter owns structural compatibility from the authorized handoff into the frozen module input contract.

## 23. Relationship to Prepared Observations

Prepared Observations owns the source-independent observation package. It preserves upstream Source Authority, PIT, Comparator, temporal, diagnostic, limitation, role, and reproducibility metadata.

The adapter must treat Prepared Observations as upstream evidence packaged through Intake, not as a construction layer to be reopened. It must not:

- construct observations;
- attach raw evidence;
- fill missing observations;
- alter observation time;
- reinterpret comparator attachments;
- delete Prepared Observation diagnostics;
- promote diagnostic Prepared Observation metadata.

## 24. Relationship to first scientific module

The first scientific module boundary is `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.

The adapter prepares a frozen input package for that boundary. It does not decide whether:

- peers are informative;
- common repair is separable;
- idiosyncratic repair exists;
- the module adds incremental information;
- stabilization is distinct;
- asymmetry is meaningful;
- the module survives falsification.

Those questions remain scientific-module or later review responsibilities and require separate authorization.

## 25. Frozen horizon policy

The adapter inherits frozen horizon policy from the authoritative activation and execution authorization chain.

It may verify:

- the frozen horizon reference is present;
- the horizon reference matches the activation declaration;
- the horizon reference matches the execution authorization;
- the horizon reference matches the frozen input contract.

It must not:

- choose horizons;
- widen horizons;
- substitute horizons;
- repair horizon mismatch;
- rescue a module by changing horizons;
- infer horizon intent from data availability or expected results.

Frozen-horizon mismatch fails closed.

## 26. Versioning and immutability

This design is versioned as `v1`. Future implementation should treat the frozen activation specification and frozen module input contract as immutable for a given activation version.

Material changes require a new version and should not silently mutate:

- selected module identity;
- narrow activation boundary;
- accepted roles;
- required upstream artifacts;
- required contracts;
- failure precedence;
- diagnostic schema;
- lineage schema;
- reproducibility schema;
- frozen horizon binding.

Stable serialization should be deterministic. Repeated adaptation of the same authorized handoff under the same versions should produce identical compatibility state, diagnostics, limitations, lineage ordering, and serialized output.

## 27. Future implementation constraints

A future bounded reference implementation should:

- use synthetic fixtures only;
- implement deterministic contract checks;
- preserve inherited roles, diagnostics, limitations, temporal metadata, lineage, and reproducibility metadata;
- emit metadata-only frozen input packages;
- fail closed on mismatch, missing references, prohibited role promotion, temporal mutation, and scientific-output attempts;
- include acceptance and rejection tests;
- include stable-serialization tests;
- include no-scientific-output refusal checks.

It must not:

- retrieve data;
- choose sources;
- construct PIT metadata;
- construct identity or lineage records;
- create historical classifications;
- construct comparators or peer groups;
- define formulas;
- compute measurements;
- generate candidates;
- generate panels;
- calculate IC;
- run validation;
- modify governance;
- modify architecture;
- modify production artifacts;
- change thresholds;
- alter survivor status;
- introduce ML.

## 28. Open design questions

| Question | Why it matters | Current design status | Future evidence needed |
| --- | --- | --- | --- |
| Should the adapter have a standalone contract id distinct from the frozen module input contract? | Separate ids may improve auditability between adapter behavior and module input shape. | Not blocking; this design names both concepts separately. | Future implementation contract inventory. |
| How should duplicate diagnostics be represented when inherited and adapter diagnostics share a code family? | Duplicate preservation can improve traceability but may complicate consumers. | Preserve deterministically; do not deduplicate in a way that hides evidence. | Synthetic implementation tests. |
| Should adapter-lineage records be mandatory even for failed adaptation? | Failed results may need auditability. | Yes conceptually; failures should still emit adapter attempt lineage where possible. | Future result-contract design. |
| How much of the First Module runtime input shape should be frozen now? | Over-freezing could accidentally define scientific runtime behavior. | Freeze only metadata boundary and structural slots, not measurements or formulas. | Future module-runtime design authorization. |
| Should conditional upstream states ever produce a frozen input package? | Conditional packages may be useful only if limitations are explicit and authorized. | Allowed only when the authorized handoff and frozen contract permit conditional input; otherwise fail closed. | Future adapter implementation tests. |

These questions do not block a bounded synthetic reference implementation because they concern implementation detail, not scientific scope.

## 29. Final classification

Final classification: `SELECTED_MODULE_ADAPTER_AND_FROZEN_ACTIVATION_SPECIFICATION_DESIGN_DEFINED`

The adapter and frozen activation specification design is defined. The design establishes the selected module adapter as a deterministic structural bridge from Authorized Intake Handoff to Frozen Module Input Contract. It preserves the broad selected program and narrow activation boundary as separate concepts, enforces mandatory lineage and reproducibility references, defines metadata-only structural mapping, preserves roles and temporal metadata exactly, specifies frozen contract verification, defines metadata-only output, orders fail-closed precedence, and confirms the adapter is not scientific execution.

This classification does not imply source acceptance, module activation, execution authorization, scientific execution, formula readiness, candidate readiness, panel readiness, IC readiness, validation readiness, production readiness, threshold change, survivor-status change, or ML readiness.

## 30. Recommended next lifecycle step

Exactly one recommended next lifecycle step:

`Project Underdog - Phase 5 Selected Scientific Module Adapter Reference Implementation v1`

That future task should implement only the bounded synthetic adapter reference layer described here. It should not retrieve data, choose sources, construct PIT metadata, construct identities, construct historical classifications, construct comparators or peer groups, define formulas, compute measurements, generate candidates, generate panels, calculate IC, run validation, modify governance, modify architecture, modify production artifacts, change thresholds, alter survivor status, or introduce ML.
