# Project Underdog - Phase 5 Scientific Module Intake Platform Integration Readiness And First Scientific Module Activation Design v1

## 1. Executive classification

Final classification: `SCIENTIFIC_MODULE_INTAKE_PLATFORM_INTEGRATION_AND_FIRST_MODULE_ACTIVATION_DESIGN_DEFINED`.

This classification applies only to the design boundary between the completed Scientific Module Intake reference layer, future platform ownership, and first scientific-module activation governance. It does not imply platform deployment, scientific execution, formula readiness, signal readiness, factor readiness, candidate readiness, registry mutation, panel readiness, validation readiness, production readiness, threshold change, survivor-status change, optimization, or ML readiness.

The design conclusion is that Project Underdog can now describe how module intake should be owned by the platform, how modules should be activated, and which Phase 5 module should be the first activation target. Actual module execution remains blocked until a later lifecycle step supplies the required authority, identity, context, contamination, falsification, reproducibility, and governance evidence.

## 2. Purpose

This note defines the integration design needed after the Scientific Module Intake reference implementation and before any future scientific module can be treated as activated within the Platform v2 lifecycle.

The design answers three questions:

- what must move from bounded reference behavior into platform-owned intake responsibility;
- how Project Underdog should declare, suspend, rerun, supersede, deactivate, or retire a scientific module without confusing those states with scientific support;
- which first scientific module should be selected for activation design once the platform boundary exists.

## 3. Scope

In scope:

- platform-integration readiness definitions;
- runtime, registry, persistence, configuration, environment, versioning, observability, and failure ownership;
- activation states and execution authorization states;
- adapter boundaries between intake contracts and module-local input contracts;
- first-module selection among the historical First Module, the selected Phase 5 module, and other inventory families;
- conceptual module input and output boundaries;
- lineage, reproducibility, frozen-horizon, contamination, falsification, and negative-evidence controls.

Out of scope:

- data retrieval;
- source selection;
- source access;
- field mapping;
- peer construction;
- formula design;
- signal or factor generation;
- candidate ID creation;
- registry mutation;
- panel generation;
- IC calculation;
- validation;
- production wiring;
- threshold changes;
- survivor-status changes;
- architecture mutation;
- optimization;
- ML.

## 4. Authoritative references

Primary repository evidence:

- `docs/research_notes/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.md`: final classification `SCIENTIFIC_MODULE_INTAKE_REFERENCE_IMPLEMENTATION_COMPLETE`; intake consumes Prepared Observations, preserves upstream diagnostics, roles, limitations, traces, reproducibility metadata, and artifact lineage, and refuses scientific output.
- `docs/research_notes/project_underdog_phase5_scientific_module_intake_executable_conformance_review_v1.md`: final classification `SCIENTIFIC_MODULE_INTAKE_IMPLEMENTATION_CONFORMANT_WITH_MINOR_OBSERVATIONS`; minor observations are shallow nested mutability, duplicate reproducibility diagnostics in one adversarial combined case, and test reliance on private synthetic helpers.
- `docs/research_notes/project_underdog_phase5_prepared_observations_platform_integration_and_scientific_module_intake_design_v1.md`: Prepared Observation structural readiness is distinct from module intake compatibility, scientific admissibility, scientific support, validation success, and production readiness.
- `docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md`: no external source is accepted as authoritative; authority is role-specific; static/current-state metadata remains diagnostic-only.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_lineage_science_v1.md`: identity and lineage are defined with open gaps; ticker is not a stable identity; no identity or lineage construction is authorized.
- `docs/research_notes/project_underdog_phase5_economic_context_validity_science_v1.md`: no historical sector, industry, size, or peer evidence is accepted for empirical Phase 5 use; peer construction remains blocked.
- `docs/research_notes/project_underdog_phase5_peer_relative_hypothesis_science_v1.md`: the selected first future peer-relative module is `Peer-Relative Post-Stress Repair And Stabilization Asymmetry`.
- `docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md`: the selected module has a plausible but unproven path to incremental information and major contamination risks.
- `docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md`: the selected module currently `CONCEPTUALLY_SURVIVES_WITH_OPEN_GAPS`; no formula, panel, IC, validation, or execution is authorized.
- `docs/research_notes/project_underdog_phase5_existing_family_reinterpretation_science_v1.md`: the leading interpretation is `LEADING_INTERPRETATION_COMMON_IDIOSYNCRATIC_DECOMPOSITION_CANDIDATE`, with existing repair-family refinement as the strongest alternative.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: the selected module is `HYPOTHESIS_DEFINED` and `BLOCKED_PENDING_EXTERNAL_EVIDENCE`; the primary bottleneck is `EXTERNAL_AUTHORITY_EVIDENCE_ABSENT`.
- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: the first Phase 5 module should be narrowed to `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.
- `docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md`: the historical First Module conforms to its frozen implementation stack but does not imply scientific validation, peer readiness, production readiness, or ML readiness.
- `docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md`: final classification `PHASE_5_SCIENTIFIC_ROADMAP_DEFINED`; formulas, candidates, panels, IC, validation, production, thresholds, and ML remain outside the roadmap.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: final classification `PHASE_5_PROGRAM_DEFINED`; Phase 5 is scientific external-information integration and ML remains deferred.
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`: Project Underdog remains ready for the next major phase while peer-relative transforms and peer-conditioned alpha research remain blocked until point-in-time metadata exists.

Superseded or lower-authority material includes prior static economic metadata enrichments, peer fallback diagnostics, vendor-specific source notes, and historical implementation concepts. They may supply diagnostic context, not authority for activation.

## 5. Architectural position

The platform position is:

Prepared Observations -> Scientific Module Intake -> Platform Activation -> Module Adapter -> Module Runtime -> Scientific Output Review.

Scientific Module Intake is a compatibility and handoff layer. Platform Activation is a governance and runtime-control layer. Module Runtime is the module-owned measurement or interpretation layer once separately authorized. Scientific Output Review is a later evidence-evaluation layer. These positions must not collapse into one another.

## 6. Core separation

The following meanings remain separate:

| Concept | Meaning | Must not imply |
| --- | --- | --- |
| Prepared Observation structural readiness | The upstream evidence package is structurally complete under Prepared Observations rules. | Module compatibility or scientific admissibility. |
| Module intake compatibility | The package satisfies a declared module intake contract. | Module activation or evidence support. |
| Platform integration readiness | Runtime ownership, registry authority, persistence, versioning, and failure controls are defined well enough for bounded reference platform work. | Platform integration has occurred. |
| Platform integrated | A later platform layer actually owns intake execution, persistence, registry state, and observability. | Scientific activation or empirical success. |
| Scientifically activated | A module has a governed active state and execution authorization path. | Formula approval, evidence support, validation, or production. |
| Scientific support | Future evidence supports the claim under predeclared controls. | Intake compatibility or execution success alone. |
| Validation success | Later validation evidence meets governance standards. | Production readiness. |

## 7. Reference implementation status

Scientific Module Intake is `REFERENCE_IMPLEMENTATION_READY` as a synthetic, metadata-only, deterministic reference layer. It is not yet `PLATFORM_INTEGRATED` and it has not activated any scientific module.

The conformance review found no architectural drift. The minor observations should inform future platform hardening but do not block this design:

- nested result dictionaries should be treated as a future deep-immutability hardening point;
- duplicate reproducibility diagnostics in a combined failure case should be normalized by a future platform diagnostic layer;
- private synthetic helper builders should not become public platform API.

## 8. Platform-integration readiness definition

Platform-integration readiness means Project Underdog has enough repository-defined design evidence to specify how the platform would own scientific-module intake decisions, activation state, execution authorization, persistence, registry records, failure handling, reproducibility, and version compatibility without moving scientific logic into the intake layer.

It is a design state. It does not mean code exists, execution is allowed, a module is active, or a scientific result is accepted.

Minimum design properties:

- one platform-owned activation registry concept;
- one platform-owned execution authorization decision concept;
- stable boundaries between intake, adapter, module runtime, and scientific review;
- deterministic artifact identity and lineage requirements;
- explicit duplicate, rerun, supersession, suspension, deactivation, and retirement semantics;
- fail-closed precedence when activation evidence conflicts with intake or scientific prerequisites.

## 9. Platform-integration readiness states

| State | Meaning | Permitted use |
| --- | --- | --- |
| `PLATFORM_INTEGRATION_READY` | Design evidence is sufficient for bounded platform reference work. | Build synthetic platform integration controls in a later authorized task. |
| `PLATFORM_INTEGRATION_CONDITIONALLY_READY` | Design is mostly sufficient but explicit limitations must be carried. | Limited reference work with limitations preserved. |
| `PLATFORM_INTEGRATION_UNRESOLVED` | Material design questions remain. | Continue design review. |
| `PLATFORM_INTEGRATION_BLOCKED` | A required governance or boundary property is missing. | No platform reference work. |
| `PLATFORM_INTEGRATION_EXCLUDED` | The proposed integration route violates scope or governance. | Reject the route. |
| `INSUFFICIENT_PLATFORM_INTEGRATION_EVIDENCE` | Repository evidence is too thin to classify. | Gather repository evidence only. |

Current design-state conclusion: `PLATFORM_INTEGRATION_READY` for bounded reference platform integration design, not for live platform operation or scientific execution.

## 10. Reference versus platform implementation

The reference layer demonstrates deterministic behavior. A platform layer would own durability, authorization, lifecycle state, and execution identity.

| Concern | Reference layer | Future platform owner |
| --- | --- | --- |
| Synthetic fixtures | May own. | Should not depend on private fixture helpers as API. |
| Intake compatibility logic | Demonstrates. | Owns stable execution and persistence. |
| Module activation state | Does not own. | Owns. |
| Execution identity | Does not own. | Owns. |
| Durable registry records | Does not own. | Owns. |
| Observability | Diagnostic fields only. | Owns event records and failure visibility. |
| Scientific interpretation | Refuses. | Still not platform-owned; belongs to module/review layers. |

## 11. Runtime ownership model

Runtime ownership should be divided as follows:

| Owner | Owns | Does not own |
| --- | --- | --- |
| Prepared Observations | Upstream package formation and inherited traces. | Module compatibility or scientific claims. |
| Scientific Module Intake | Structural compatibility evaluation and bounded handoff contract. | Activation, formulas, measurement, or evidence support. |
| Platform Activation | Module state, execution authorization, execution identity, duplicate/rerun/supersession policy, persistence, and observability. | Scientific formula behavior or empirical interpretation. |
| Module Adapter | Translation from intake handoff to module-local input contract. | Upstream recomputation or source authority decisions. |
| Scientific Module | Module-local scientific computation or interpretation once authorized. | Source selection, peer construction, or activation governance. |
| Scientific Review | Support, falsification, negative evidence, and validation interpretation. | Runtime scheduling. |

## 12. Registry authority model

A future activation registry should be platform-owned and append-only in scientific meaning. It should record declarations, not silently overwrite them.

Required registry concepts:

- module identity;
- module version;
- module specification version;
- intake contract identity and version;
- adapter identity and version;
- activation state;
- execution authorization state;
- frozen specification reference;
- frozen horizon reference where applicable;
- accepted upstream contract versions;
- required role bindings;
- governing scientific notes;
- lineage and reproducibility requirements;
- suspension, deactivation, retirement, and supersession records.

The registry must not be a candidate registry, formula registry, validation registry, or production registry.

## 13. Persistence ownership model

Platform persistence should preserve:

- activation declaration artifacts;
- intake compatibility artifacts;
- adapter compatibility artifacts;
- execution authorization artifacts;
- execution identity records;
- deterministic handoff contracts;
- diagnostics and limitations;
- artifact-lineage records;
- reproducibility metadata;
- supersession, rerun, failure, suspension, deactivation, and retirement decisions.

Persistence must not create scientific authority. It only makes decisions reconstructable.

## 14. Configuration and environment ownership

Platform configuration may later govern:

- allowed contract versions;
- allowed module versions;
- allowed adapter versions;
- accepted readiness states;
- authorization policy;
- diagnostic schema versions;
- lineage schema versions;
- reproducibility schema versions.

Environment metadata should be captured for reproducibility, but environment convenience must not decide scientific authority. A source or module cannot become admissible because a local environment can run it.

## 15. Public interface stability

Stable public interfaces should be:

- Prepared Observation result contract;
- Scientific Module Intake result and handoff contract;
- activation declaration record;
- adapter compatibility record;
- execution authorization record;
- artifact-lineage record;
- reproducibility record.

Private helper builders, synthetic fixture constructors, and module-internal transformations should not become platform interfaces.

## 16. Platform versioning and migration

Version compatibility should be evaluated across:

- Prepared Observation contract version;
- Prepared Observation implementation version;
- Scientific Module Intake contract version;
- Scientific Module Intake implementation version;
- module id and module version;
- module specification version;
- adapter id and adapter version;
- information-role schema version;
- diagnostic schema version;
- artifact-lineage schema version;
- reproducibility schema version.

Migration must be explicit. If a module declaration references an older intake or adapter version, the platform should either preserve it, supersede it through a recorded decision, or fail closed. Silent migration is not permitted.

## 17. Platform failure and observability model

Platform failures should be observable without being converted into scientific findings.

Failure classes:

- missing registry declaration;
- missing intake contract;
- incompatible versions;
- missing adapter;
- incompatible adapter;
- missing frozen specification;
- missing horizon freeze;
- missing lineage;
- incomplete reproducibility;
- duplicate execution identity;
- superseded artifact use;
- suspended module use;
- retired module use;
- prohibited output-role request.

Each failure should produce deterministic diagnostics and preserve inherited upstream limitations.

## 18. Scientific module activation definition

Scientific module activation means a platform-governed declaration that a named module and version may receive compatible intake handoff packages under a frozen scientific specification and execution authorization policy.

Activation does not mean:

- the module is scientifically supported;
- formulas are approved;
- candidates exist;
- panels exist;
- validation is ready;
- production is ready;
- ML is ready.

## 19. Activation-state model

| State | Meaning |
| --- | --- |
| `MODULE_REGISTERED` | Module identity exists in a registry but is not ready for activation. |
| `MODULE_ACTIVATION_READY` | Activation declaration is complete and prerequisites are satisfied for the authorized scope. |
| `MODULE_ACTIVATION_CONDITIONALLY_READY` | Activation can proceed only with explicit limitations. |
| `MODULE_ACTIVATION_UNRESOLVED` | Required activation evidence is ambiguous. |
| `MODULE_ACTIVATION_BLOCKED` | A required prerequisite is absent or failed. |
| `MODULE_ACTIVE` | Platform activation has been declared for a bounded scope. |
| `MODULE_SUSPENDED` | Active or ready state is paused pending issue resolution. |
| `MODULE_DEACTIVATED` | Activation has ended without permanent scientific retirement. |
| `MODULE_RETIRED` | The module or version is no longer eligible except under reopening rules. |

## 20. Activation invariant

Activation must satisfy this invariant:

`MODULE_ACTIVE` requires a compatible intake contract, compatible adapter, frozen scientific specification, frozen horizon policy where relevant, execution authorization, artifact-lineage preservation, reproducibility preservation, contamination controls, falsification policy, and registry decision record.

If any required component is missing, superseded without migration, unresolved, or failed, the state must be `MODULE_ACTIVATION_BLOCKED`, `MODULE_ACTIVATION_UNRESOLVED`, or `MODULE_ACTIVATION_CONDITIONALLY_READY`, not `MODULE_ACTIVE`.

## 21. First scientific module candidate assessment

| Candidate | Repository status | Activation-design fit | Blocking issue |
| --- | --- | --- | --- |
| Historical First Module | Frozen source-independent reference module exists and conforms to its own stack. | Good evidence for module-local boundaries, but it predates generalized intake and would need an adapter. | It is not the current Phase 5 external-information frontier and should not be retrofitted by this task. |
| `Peer-Relative Post-Stress Repair And Stabilization Asymmetry` | Selected WS4 module; WS6 says it `CONCEPTUALLY_SURVIVES_WITH_OPEN_GAPS`; WS8 says it is `HYPOTHESIS_DEFINED` and `BLOCKED_PENDING_EXTERNAL_EVIDENCE`. | Best Phase 5 activation target because it exercises the missing external context, comparator, authority, and intake boundaries. | Scientific execution remains blocked by authority, identity, context, peer, contamination, falsification, and reproducibility evidence. |
| Existing OHLCV families | Some have stronger empirical histories. | Useful as controls and reinterpretation baselines. | They do not test the external-information intake and comparator boundary that Phase 5 exists to define. |

## 22. Historical First Module assessment

The historical First Module remains an important reference artifact, not the selected first Phase 5 activation target.

It demonstrates:

- a source-independent module input concept;
- frozen contract identifiers;
- module-local gates;
- refusal of candidate, panel, validation, and production outputs;
- deterministic reference behavior.

It also predates generalized Prepared Observations and Scientific Module Intake. The repository already states that an adapter would likely be required for future direct Prepared Observation consumption, and that retrofitting the completed First Module is not necessary now. This note preserves that conclusion.

## 23. Selected Phase 5 module assessment

The selected Phase 5 module remains:

- conceptual;
- highest-value for testing external peer-relative context;
- narrowed by later boundary work toward `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`;
- inventoried as `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION` with secondary `FAMILY_REFINEMENT_INFORMATION` and `CONDITIONING_INFORMATION`;
- `HYPOTHESIS_DEFINED`;
- `BLOCKED_PENDING_EXTERNAL_EVIDENCE`.

The selected module is suitable as the first activation target for platform-design purposes because it forces the platform to carry authority, identity, context, comparator, contamination, falsification, lineage, and reproducibility boundaries explicitly.

## 24. First activation target selection

First activation target: `Peer-Relative Post-Stress Repair And Stabilization Asymmetry`, bounded for future design by `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.

Selection rationale:

- it is the selected first future peer-relative module in WS4;
- it conceptually survives WS6 with open gaps;
- it is the leading common-versus-idiosyncratic decomposition candidate in WS7 and WS8;
- it is more aligned with Phase 5 than reactivating older OHLCV-only modules;
- it exposes the platform boundaries that Scientific Module Intake was designed to serve.

This selection is an activation-design selection only. It does not authorize formulas, peer construction, execution, candidates, panels, IC, validation, production, thresholds, survivor-status changes, or ML.

## 25. Activation declaration

A future activation declaration should contain:

- activation declaration id;
- module id;
- module version;
- bounded module name;
- module specification version;
- intake contract id and version;
- adapter id and version;
- accepted Prepared Observation versions;
- required information roles;
- prohibited information roles;
- frozen specification reference;
- frozen horizon reference where applicable;
- execution authorization state;
- activation state;
- governing references;
- diagnostic limitations;
- lineage requirements;
- reproducibility requirements;
- contamination and falsification references;
- supersession policy.

The declaration must be durable and reconstructable.

## 26. Adapter ownership and boundaries

The adapter translates a compatible intake handoff into a module-local input structure. It must not:

- recompute Source Authority;
- recompute PIT identity;
- recompute context validity;
- construct comparators;
- select peers;
- create source records;
- define formulas;
- infer missing scientific evidence;
- downgrade upstream diagnostics;
- discard limitations;
- alter frozen horizons.

The adapter may map names, preserve role bindings, check required fields, and fail closed when module input cannot be produced from accepted intake evidence.

## 27. Adapter compatibility states

| State | Meaning |
| --- | --- |
| `ADAPTER_COMPATIBLE` | Handoff can be translated into the module input contract without loss of required evidence. |
| `ADAPTER_CONDITIONALLY_COMPATIBLE` | Translation is possible only with explicit limitations. |
| `ADAPTER_UNRESOLVED` | Required mapping evidence is ambiguous. |
| `ADAPTER_INCOMPATIBLE` | Required module input cannot be produced from the handoff. |
| `ADAPTER_EXCLUDED` | Adapter use violates scope, state, or governance. |
| `INSUFFICIENT_ADAPTER_EVIDENCE` | Evidence is too thin to classify compatibility. |

Current selected-module adapter readiness: `ADAPTER_UNRESOLVED` for actual execution, because the bounded module input contract is not yet frozen; `ADAPTER_CONDITIONALLY_COMPATIBLE` for future reference-design exploration under this note's boundaries.

## 28. Intake-to-module mapping model

Conceptual mapping for the selected module:

| Intake evidence | Future module input role | Required? | Boundary |
| --- | --- | --- | --- |
| Package identity | Prepared Observation package reference | Yes | Identity only; no data expansion. |
| Intake compatibility result | Admission evidence | Yes | Must be compatible or conditionally compatible under declared policy. |
| Target observation metadata | Target-security observation context | Yes | Does not define formula inputs by itself. |
| Observation-time metadata | Point-in-time anchor | Yes | Must preserve known-date and horizon discipline. |
| Accepted context attachments | Economic context and conditioning evidence | Yes for peer module | Only accepted, role-specific, date-valid context may pass. |
| Accepted comparator attachments | Comparator or peer-substrate evidence | Yes for peer module | Must not construct peers inside adapter. |
| Role bindings | Module role assignment | Yes | Exact role matching; no semantic substitution. |
| Coverage and missingness metadata | Eligibility constraints | Yes | Missingness remains visible. |
| Inherited diagnostics and limitations | Blocking or conditional evidence | Yes | Must not be dropped. |
| Artifact lineage and reproducibility | Reconstructability evidence | Yes | Required for any later scientific interpretation. |

## 29. Module input contract

A future module input contract for the selected module should require:

- module id and version;
- frozen scientific specification id;
- frozen horizon policy id;
- package id;
- intake evaluation id;
- adapter evaluation id;
- target security or research-entity reference;
- target observation time;
- accepted context references;
- accepted comparator references;
- role binding map;
- authority trace references;
- identity and lineage trace references;
- context trace references;
- comparator trace references;
- coverage and missingness summaries;
- inherited diagnostics and limitations;
- activation declaration id;
- execution authorization id;
- reproducibility metadata.

It should exclude raw source records, live queries, formulas, candidate ids, panels, validation labels, and production routing fields.

## 30. Module output contract boundary

Scientific Module Intake and Platform Activation may permit only bounded output envelopes, not scientific claims.

Allowed output-envelope concepts:

- execution identity;
- module version;
- input contract reference;
- diagnostics;
- limitations;
- lineage;
- reproducibility metadata;
- module-local output classification placeholder.

Prohibited intake/activation outputs:

- alpha support claims;
- validation claims;
- production decisions;
- candidate registration;
- IC results;
- portfolio guidance;
- ML readiness.

## 31. Scientific specification freeze

Before `MODULE_ACTIVE`, the scientific specification must be frozen enough to identify:

- module scientific question;
- bounded claim;
- included and excluded mechanisms;
- required input roles;
- required context roles;
- required comparator roles;
- contamination controls;
- falsification rules;
- negative-evidence preservation rules;
- horizon governance;
- prohibited reinterpretations.

For the selected module, the current boundary note narrows the scientific question, but formula, measurement, panel, and empirical design remain unauthorized. Therefore scientific-specification readiness for execution is `MODULE_ACTIVATION_BLOCKED`.

## 32. Frozen-horizon governance

Frozen-horizon governance must exist before any future execution that could create interpretable scientific output.

Required properties:

- horizon concepts declared before result observation;
- horizon changes recorded as new versions or supersessions;
- no horizon rescue after weak results;
- horizon mismatch diagnostics;
- negative evidence preserved for weak or unstable horizons.

This note does not choose numerical horizons.

## 33. Execution authorization

Execution authorization is a platform-owned decision that a module version may run for a bounded purpose against compatible inputs.

Authorization requires:

- activation declaration;
- compatible intake result;
- compatible adapter result;
- frozen specification reference;
- frozen horizon reference where applicable;
- no blocking diagnostics;
- complete lineage and reproducibility metadata;
- non-superseded input artifacts;
- allowed output role;
- preserved contamination and falsification boundaries.

Execution authorization must not be inferred from local ability to run code.

## 34. Execution authorization states

| State | Meaning |
| --- | --- |
| `EXECUTION_AUTHORIZED` | All required authorization evidence exists for the bounded scope. |
| `EXECUTION_CONDITIONALLY_AUTHORIZED` | Execution is allowed only with carried limitations. |
| `EXECUTION_UNRESOLVED` | Required authorization evidence is ambiguous. |
| `EXECUTION_BLOCKED` | A required prerequisite is absent or failed. |
| `EXECUTION_EXCLUDED` | The requested execution violates scope or governance. |
| `INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE` | Evidence is too thin to classify. |

Current selected-module execution authorization: `EXECUTION_BLOCKED`.

## 35. Execution identity

Each future execution should have one stable execution identity containing:

- execution id;
- activation declaration id;
- module id/version/specification version;
- adapter id/version;
- intake evaluation id;
- package id;
- frozen horizon id where applicable;
- deterministic input hash;
- deterministic configuration hash;
- execution purpose;
- output role request;
- supersession status.

Execution identity prevents duplicate, ambiguous, and unreconstructable module runs.

## 36. Duplicate-execution control

Duplicate-execution control should classify attempted executions as:

- exact duplicate: same execution identity and same deterministic inputs;
- benign rerun: same inputs under authorized rerun policy;
- superseding rerun: new version or corrected evidence supersedes prior execution;
- conflicting duplicate: same apparent identity with different inputs or configuration;
- prohibited duplicate: duplicate would overwrite or obscure prior scientific evidence.

Conflicting and prohibited duplicates must fail closed.

## 37. Rerun semantics

Reruns should preserve original evidence rather than replace it.

Permitted rerun reasons:

- reproducibility confirmation;
- deterministic platform hardening;
- corrected non-scientific platform defect;
- explicit supersession with versioned evidence;
- diagnostic-only comparison under clear labeling.

Prohibited rerun reasons:

- result shopping;
- horizon rescue;
- peer redefinition after observing results;
- silent source substitution;
- unrecorded configuration drift.

## 38. Supersession model

Supersession should be explicit, one-directional, and reconstructable.

Supersession triggers:

- module specification version changes;
- adapter version changes;
- intake contract version changes;
- upstream evidence version changes;
- corrected lineage or reproducibility records;
- retired or suspended scientific assumptions;
- changed frozen horizon policy.

Superseded artifacts remain part of negative-evidence and lineage history.

## 39. Failure model

Failure classes:

- structural failure: intake or adapter cannot form required input;
- authority failure: required source-role evidence is absent;
- identity failure: identity or lineage evidence is unresolved;
- context failure: economic context or comparator evidence is invalid;
- temporal failure: known-date or horizon evidence is insufficient;
- reproducibility failure: output cannot be reconstructed;
- contamination failure: peer, identity, source, or timing contamination cannot be isolated;
- governance failure: activation, authorization, or registry evidence is missing.

Failure is not automatically falsification. Falsification requires scientific negative evidence under adequate design and controls.

## 40. Suspension model

`MODULE_SUSPENDED` should be used when a module was ready or active but a correctable uncertainty appears.

Suspension triggers:

- source-role authority becomes disputed;
- identity or context assumptions are challenged;
- adapter compatibility changes;
- version migration is unresolved;
- contamination concern emerges;
- reproducibility artifact is incomplete;
- governance record requires clarification.

During suspension, new execution is prohibited. Prior artifacts remain preserved.

## 41. Deactivation model

`MODULE_DEACTIVATED` should be used when the module is no longer active for operational lifecycle reasons without permanent scientific retirement.

Permissible reasons:

- superseded module version;
- replaced adapter;
- completed bounded lifecycle step;
- platform migration;
- scope closure.

Deactivation must not erase prior negative evidence, diagnostics, limitations, or lineage.

## 42. Retirement model

`MODULE_RETIRED` should be used when negative evidence, redundancy, contamination, or governance findings make future use prohibited except under reopening standards.

Retirement can apply to:

- module version;
- hypothesis variant;
- adapter route;
- peer-definition approach;
- output interpretation;
- broader mechanism if warranted.

Retirement must preserve reopening conditions and anti-resurrection constraints.

## 43. Scientific-output classification boundary

Scientific-output classifications belong after module execution and scientific review, not to intake or activation.

Future scientific-layer concepts may include:

- `MEASUREMENT_COMPLETED`;
- `SCIENTIFIC_SUPPORT_NOT_ESTABLISHED`;
- `SCIENTIFIC_SUPPORT_PARTIAL`;
- `SCIENTIFIC_SUPPORT_ESTABLISHED`;
- `FALSIFIED`;
- `UNRESOLVED`;
- `INSUFFICIENT_EVIDENCE`.

Scientific Module Intake and Platform Activation must not emit these as evidence conclusions.

## 44. Negative-evidence preservation

Activation records should preserve negative evidence pathways before any output exists:

- rejected activation attempts;
- blocked authorization attempts;
- incompatible adapters;
- failed intake handoffs;
- source insufficiency;
- identity insufficiency;
- context insufficiency;
- contamination concerns;
- duplicate or rerun refusals;
- supersession rationale.

This prevents future resurrection through new labels, source substitution, peer relabeling, horizon shifting, or adapter relabeling.

## 45. Falsification boundary

Falsification belongs to scientific review, but activation must preserve the conditions needed for falsification.

The platform should carry:

- predeclared claim references;
- predeclared context scope;
- predeclared horizon references;
- required controls;
- required ablations;
- negative-control expectations;
- retirement rules;
- reopening standards.

Activation must fail closed if the module has no falsifiable claim.

## 46. Contamination controls

For the selected module, activation prerequisites must include explicit controls for:

- own-security duplication;
- market-state duplication;
- existing repair-family duplication;
- participation and liquidity overlap;
- volatility-compression overlap;
- VoV overlap;
- persistence and rank overlap;
- transition-state overlap;
- peer-definition leakage;
- identity leakage;
- temporal leakage;
- source leakage;
- survivorship and delisting leakage;
- corporate-event leakage;
- context fragmentation.

These controls are conceptual here. No empirical controls are run.

## 47. Artifact-lineage model

Every activation and execution-adjacent artifact should trace:

- upstream Prepared Observation package;
- intake evaluation;
- adapter compatibility record;
- activation declaration;
- execution authorization decision;
- module input contract;
- module output envelope if later authorized;
- governing scientific notes;
- versions and schema ids;
- diagnostics and limitations;
- supersession, suspension, deactivation, or retirement records.

Lineage must be sufficient to reconstruct why a module was allowed, blocked, suspended, deactivated, or retired.

## 48. Reproducibility model

Reproducibility requires:

- deterministic serialization of declarations and decisions;
- stable hashes for handoff inputs and configuration;
- recorded versions;
- retained diagnostics and limitations;
- retained lineage references;
- recorded environment metadata where relevant;
- no reliance on current mutable metadata for historical claims;
- no silent overwrite of prior records.

Reproducibility proves reconstructability, not scientific validity.

## 49. Registry design

Conceptual registries:

| Registry | Purpose | Must not become |
| --- | --- | --- |
| Module declaration registry | Record module identity and versions. | Candidate registry. |
| Activation registry | Record activation states and declarations. | Scientific support ledger. |
| Adapter registry | Record adapter identity, versions, and compatibility states. | Source mapper. |
| Execution authorization registry | Record bounded permission to run. | Validation scheduler. |
| Failure registry | Preserve blocked, incompatible, and excluded attempts. | Bug-only tracker. |
| Supersession registry | Preserve version lineage. | Silent migration table. |
| Retirement registry | Preserve negative-evidence and anti-resurrection constraints. | Production registry. |

## 50. Version-compatibility model

Compatibility should be declared across versions, not inferred.

Version outcomes:

- compatible: declared and tested by the relevant reference layer;
- conditionally compatible: declared with carried limitations;
- unresolved: version relationship unknown;
- incompatible: declared or detected mismatch;
- excluded: version path violates governance;
- insufficient evidence: no version evidence exists.

Any unresolved or incompatible required version blocks activation.

## 51. Decision precedence

Decision precedence should be fail-closed:

1. Excluded scope or governance violation.
2. Retired module or prohibited resurrection.
3. Suspended module without reinstatement.
4. Missing registry or activation declaration.
5. Missing frozen specification or horizon reference.
6. Missing intake, adapter, lineage, or reproducibility evidence.
7. Version incompatibility.
8. Required authority, identity, context, or comparator prerequisite absent.
9. Contamination or falsification prerequisite absent.
10. Conditional readiness accepted only if policy allows it and limitations are carried.

## 52. Diagnostic model

Activation diagnostics should be deterministic and source-independent.

Core diagnostics:

- `MISSING_ACTIVATION_DECLARATION`;
- `UNKNOWN_MODULE`;
- `MISSING_FROZEN_SPECIFICATION`;
- `MISSING_FROZEN_HORIZON_POLICY`;
- `MISSING_ADAPTER`;
- `ADAPTER_INCOMPATIBLE`;
- `MISSING_INTAKE_EVALUATION`;
- `INTAKE_NOT_COMPATIBLE`;
- `INCOMPLETE_LINEAGE`;
- `INCOMPLETE_REPRODUCIBILITY`;
- `VERSION_INCOMPATIBLE`;
- `MODULE_SUSPENDED`;
- `MODULE_RETIRED`;
- `EXECUTION_DUPLICATE_CONFLICT`;
- `UNAUTHORIZED_OUTPUT_ROLE`;
- `SCIENTIFIC_PREREQUISITES_BLOCKED`.

Diagnostics explain state; they do not provide scientific support.

## 53. Limitation model

Activation limitations should be carried when a state is conditional or unresolved:

- reference-only behavior;
- synthetic-only evidence;
- conditional upstream readiness;
- unresolved adapter mapping;
- missing live platform persistence;
- missing authoritative external evidence;
- missing PIT identity;
- missing historical context;
- missing valid comparators;
- unresolved contamination controls;
- unresolved falsification prerequisites;
- no formula authorization;
- no validation authorization.

Limitations must be visible to later design and cannot be silently cleared.

## 54. First Module compatibility conclusion

Historical First Module compatibility conclusion: `REFERENCE_IMPLEMENTATION_READY`, `ADAPTER_UNRESOLVED`, and not selected as the first Phase 5 activation target.

The historical First Module remains valuable as prior evidence for source-independent module boundaries and deterministic refusal of candidate/panel/validation/production outputs. It should remain unchanged unless a later task explicitly authorizes adapter work.

## 55. Selected module activation readiness conclusion

Selected module activation target: `Peer-Relative Post-Stress Repair And Stabilization Asymmetry`, bounded by `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.

Activation readiness conclusion:

- activation-design target selected: yes;
- scientific-specification boundary: partially defined;
- adapter contract: unresolved;
- authority evidence: absent;
- PIT identity evidence: absent;
- historical economic-context evidence: absent;
- valid comparator evidence: absent;
- contamination controls: conceptual only;
- falsification controls: conceptual only;
- execution authorization: `EXECUTION_BLOCKED`;
- module state for actual execution: `MODULE_ACTIVATION_BLOCKED`.

## 56. Platform-integration readiness conclusion

Scientific Module Intake platform-integration readiness conclusion: `PLATFORM_INTEGRATION_READY` for bounded reference platform integration design.

This means a later task may design or build a synthetic reference layer for activation registry, adapter compatibility, execution authorization, duplicate/rerun/supersession controls, and lineage/reproducibility persistence. It does not mean live platform operation, source access, data retrieval, peer construction, formulas, candidate registration, panels, IC, validation, production, thresholds, survivor-status changes, optimization, or ML.

## 57. Implementation sequence

Permitted future sequence, subject to separate authorization:

1. Define or build a synthetic activation-registry and execution-authorization reference layer.
2. Define selected-module adapter contract requirements without formulas or peer construction.
3. Review conformance of activation registry and adapter-state behavior.
4. Only after authority, identity, context, comparator, contamination, falsification, and reproducibility evidence exists, consider a later bounded module design review.

No step in this sequence is authorized by this note.

## 58. Known limitations

Known limitations:

- no live platform persistence exists;
- no activation registry exists;
- no selected-module adapter contract is frozen;
- no authoritative external source exists;
- no PIT identity or lineage evidence exists for real securities;
- no historical economic-context or peer evidence is accepted;
- no formula or measurement specification is authorized;
- no empirical independence is established;
- no validation or production readiness exists;
- ML remains deferred.

These limitations do not block the design classification, but they block activation for execution.

## 59. Exactly one recommended next lifecycle step

Recommended next lifecycle step:

`Project Underdog - Phase 5 Scientific Module Activation Registry And Execution Authorization Reference Implementation v1`.

The step should be synthetic-only and should realize activation declarations, activation states, adapter compatibility states, execution authorization states, duplicate/rerun/supersession controls, suspension/deactivation/retirement records, deterministic diagnostics, lineage, reproducibility metadata, and refusal of scientific-output claims. It must not retrieve data, choose sources, construct identities, construct historical classifications, construct peers, define formulas, assign candidates, create panels, calculate IC, validate, productionize, change thresholds, alter survivor status, optimize, or introduce ML.

## 60. Verification commands

Repository searches and lightweight checks used for this note:

```bash
sed -n '1,260p' /Users/AnyiXu_1/.codex/attachments/2802ccdb-a7eb-44c3-b957-3b2c3920595d/pasted-text.txt
sed -n '261,620p' /Users/AnyiXu_1/.codex/attachments/2802ccdb-a7eb-44c3-b957-3b2c3920595d/pasted-text.txt
sed -n '621,1040p' /Users/AnyiXu_1/.codex/attachments/2802ccdb-a7eb-44c3-b957-3b2c3920595d/pasted-text.txt
sed -n '1041,1460p' /Users/AnyiXu_1/.codex/attachments/2802ccdb-a7eb-44c3-b957-3b2c3920595d/pasted-text.txt
sed -n '1461,1880p' /Users/AnyiXu_1/.codex/attachments/2802ccdb-a7eb-44c3-b957-3b2c3920595d/pasted-text.txt
rg -n "Peer-Relative Post-Stress Repair|selected first module|first module|activation|module activation|First Module|frozen horizon|negative evidence|falsification|intake" docs/research_notes/project_underdog_phase5_peer_relative_hypothesis_science_v1.md docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md docs/research_notes/project_underdog_phase5_existing_family_reinterpretation_science_v1.md docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md
rg -n "class FirstModuleInput|class FirstModuleResult|def run_first_module_reference|MODULE_ID|FROZEN|formula|candidate|panel|validation|production|source_independent|requested_output_roles" pipelines/project_underdog_first_module_reference_implementation_v1.py tests/test_project_underdog_first_module_reference_implementation_v1.py docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md
rg -n "Final classification|CONFORMANT|minor|recommended next|mutable|duplicate|determinism|lineage|refusal" docs/research_notes/project_underdog_phase5_scientific_module_intake_executable_conformance_review_v1.md
rg -n "Final classification|SCIENTIFIC_MODULE_INTAKE_REFERENCE_IMPLEMENTATION_COMPLETE|Prepared Observation|stable_json|artifact lineage|no scientific|recommended next" docs/research_notes/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.md
rg -n "BLOCKED_PENDING_EXTERNAL_EVIDENCE|HYPOTHESIS_DEFINED|COMMON_IDIOSYNCRATIC|EXTERNAL_AUTHORITY_EVIDENCE_ABSENT|selected module" docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md
rg -n "no source|No external source|diagnostic-only|peer construction remains blocked|static|current-state|authoritative|no historical sector|peer evidence" docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md docs/research_notes/project_underdog_phase5_economic_context_validity_science_v1.md
rg -n "negative evidence|falsification|CONCEPTUALLY_SURVIVES_WITH_OPEN_GAPS|cannot advance|blocked|formula|panel" docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md
rg -n "PROJECT_READY_FOR_NEXT_MAJOR_PHASE|PHASE_5_PROGRAM_DEFINED|PHASE_5_SCIENTIFIC_ROADMAP_DEFINED|ML remains deferred|peer-relative|validation-ready|production" docs/research_notes/project_underdog_master_status_recap_2026-06-17.md docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md
rg -n "First Module|Prepared Observation|adapter|compatibility|structural readiness|scientific admissibility|scientific support|validation success|production readiness|boundary" docs/research_notes/project_underdog_phase5_prepared_observations_platform_integration_and_scientific_module_intake_design_v1.md docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md
```

## 61. Non-modification confirmation

This note creates a design artifact only. No institution or vendor was contacted. No source, taxonomy, or acquisition path was selected. No access, data retrieval, proprietary documentation retrieval, source inspection, connector creation, source query, PIT construction, identity construction, lineage construction, classification construction, peer construction, formula definition, regression or residualization procedure, signal generation, factor generation, candidate assignment, registry creation, panel generation, IC calculation, validation, governance change, architecture change, production change, threshold change, survivor-status change, optimization, or ML work was performed.

Final classification: `SCIENTIFIC_MODULE_INTAKE_PLATFORM_INTEGRATION_AND_FIRST_MODULE_ACTIVATION_DESIGN_DEFINED`.
