# Project Underdog - Phase 5 Scientific Module Activation Registry And Execution Authorization Reference Implementation v1

## 1. Executive classification

Final classification: `SCIENTIFIC_MODULE_ACTIVATION_REGISTRY_AND_EXECUTION_AUTHORIZATION_REFERENCE_IMPLEMENTATION_COMPLETE`.

This classification applies only to the bounded synthetic governance reference implementation. It does not imply real module activation, scientific execution, formula readiness, signal readiness, factor readiness, candidate readiness, panel readiness, IC readiness, validation readiness, production readiness, optimization, or ML readiness.

## 2. Purpose

The implementation proves that Project Underdog can deterministically register, assess, block, authorize, suspend, deactivate, retire, and trace scientific-module activations and execution-authorization requests without executing a scientific hypothesis.

## 3. Files created

- `pipelines/project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1.py`
- `tests/test_project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1.py`
- `docs/research_notes/project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1.md`

## 4. Files modified

No existing repository files were modified.

## 5. Authoritative design

Primary design authority: `docs/research_notes/project_underdog_phase5_scientific_module_intake_platform_integration_readiness_and_first_scientific_module_activation_design_v1.md`.

Compatibility evidence was checked against Scientific Module Intake, Prepared Observations, Comparator Construction, PIT Identity and Context Evidence, Source Authority, First Module, Phase 5 scientific philosophy, information-role governance, artifact-lineage governance, reproducibility governance, contamination, falsification, negative-evidence, frozen-horizon, and integrated-inventory materials.

## 6. Architectural position

Implemented position:

Scientific Module Registration -> Activation Declaration -> Activation Readiness Evaluation -> Activation State -> Execution Authorization Request -> Execution Authorization State.

Scientific execution, scientific measurement, scientific result generation, and validation remain unimplemented.

## 7. Scientific-boundary separation

The implementation preserves:

Module registered != activation ready != module active != execution authorized != scientific execution completed != scientific support established != validation passed != production ready != ML ready.

No result object collapses these concepts.

## 8. Selected research program

The broad selected research program is represented explicitly as:

`Peer-Relative Post-Stress Repair And Stabilization Asymmetry`.

This broad label is metadata only. It does not authorize stabilization as a separate mechanism, asymmetry as a family, macro conditioning, volatility normalization, participation/liquidity integration, rank persistence, transition timing, leadership, dispersion, or event absorption.

## 9. Narrow activation specification

The activation declaration binds to the narrow specification:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.

The broad program label cannot substitute for the narrow activation specification. A mismatch fails closed with `RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH`.

## 10. Implementation scope

The reference layer supports immutable synthetic metadata for registration, activation declarations, adapter metadata, module input/output contract metadata, frozen specification and horizon binding, activation invariant checks, activation readiness, execution authorization, deterministic execution identity, duplicate/rerun/supersession classification, lifecycle metadata, lineage, reproducibility, stable serialization, canonical fixtures, and tests.

## 11. Explicit non-responsibilities

The implementation does not retrieve data, evaluate source authority, construct PIT evidence, construct identities, construct comparators, construct Prepared Observations, recompute Scientific Module Intake, transform scientific values, define formulas, create measurements, generate signals or factors, create candidates, create panels, calculate IC or Sharpe, validate, make portfolio or production decisions, optimize, or introduce ML.

## 12. Module registration

`ScientificModuleRegistration` records module identity, version, research-program identity, activation-specification identity, intake contract, adapter, input/output contracts, status, artifact reference, and governing versions.

Research-program identity and activation-specification identity are separate required fields.

## 13. Activation declaration

`ActivationDeclaration` records activation id/version, module binding, research-program binding, narrow activation-specification binding, intake/adapter/input/output contracts, scientific specification, frozen horizon specification, accepted intake states, policies, artifact-lineage requirements, reproducibility requirements, effective interval, requested activation state, governing designs, and explicit activation authorization.

It contains no scientific results.

## 14. Activation invariant

Activation evaluation binds declaration, registration, research-program identity, narrow activation specification, intake contract, adapter, input contract, output contract, scientific specification, frozen horizon specification, version schemas, effective interval, negative-evidence policy, falsification policy, contamination-control policy, lineage, and reproducibility.

Missing mandatory elements fail closed through `ACTIVATION_INVARIANT_INCOMPLETE` and specific missing-field diagnostics.

## 15. Activation prerequisites

`ActivationPrerequisiteState` represents source authority, PIT identity/context, comparator evidence, Prepared Observations, intake platform, adapter, input/output contracts, scientific specification freeze, frozen horizon, negative evidence, falsification, contamination controls, lineage, reproducibility, and version compatibility.

For the real selected-module fixture, source authority, PIT identity/context, comparator evidence, and Prepared Observations are false.

## 16. Activation states

The exact implemented state inventory is:

`MODULE_REGISTERED`, `MODULE_ACTIVATION_READY`, `MODULE_ACTIVATION_CONDITIONALLY_READY`, `MODULE_ACTIVATION_UNRESOLVED`, `MODULE_ACTIVATION_BLOCKED`, `MODULE_ACTIVE`, `MODULE_SUSPENDED`, `MODULE_DEACTIVATED`, `MODULE_RETIRED`.

## 17. Activation decision precedence

Activation fails closed through deterministic precedence: missing or conflicting identity/specification, missing invariant components, version incompatibility, incomplete lineage/reproducibility, absent authority/PIT/comparator/Prepared Observation evidence, unavailable intake platform, unresolved contamination/falsification/negative-evidence policy, suspension, deactivation, retirement, unresolved readiness, conditional readiness, ready, and active only with explicit authorization.

Ready state does not auto-transition to active.

## 18. Activation diagnostics

Implemented activation diagnostics include missing registration, missing research program, missing activation specification, broad/narrow mismatch, missing intake/adapter/input/output/scientific/frozen-horizon contracts, invariant incomplete, version incompatibilities, incomplete lineage/reproducibility, absent source/PIT/comparator/Prepared Observation evidence, intake platform unavailable, unresolved contamination/negative/falsification policies, already active, suspended, deactivated, retired, invalid effective interval, and missing explicit activation authorization.

No scientific-performance diagnostics are present.

## 19. Activation limitations

Implemented limitations include `REFERENCE_IMPLEMENTATION_ONLY`, `SYNTHETIC_REGISTRY_ONLY`, `SYNTHETIC_PREREQUISITE_STATE`, `REAL_EXTERNAL_EVIDENCE_UNAVAILABLE`, `REAL_PREPARED_OBSERVATIONS_UNAVAILABLE`, conditional readiness, adapter transformation prohibition, and historical First Module adapter deferral where applicable.

Limitations are sorted deterministically and do not mask blockers.

## 20. Adapter metadata

`AdapterRegistration` records adapter id/version, module id/version, intake contract, input contract, mapping specification, adapter status, artifact reference, governing versions, and `scientific_transformation_permitted`.

All reference fixtures keep `scientific_transformation_permitted=False` except the explicit adversarial transformation fixture.

## 21. Adapter compatibility

The exact implemented adapter states are:

`ADAPTER_COMPATIBLE`, `ADAPTER_CONDITIONALLY_COMPATIBLE`, `ADAPTER_UNRESOLVED`, `ADAPTER_INCOMPATIBLE`, `ADAPTER_EXCLUDED`, `INSUFFICIENT_ADAPTER_EVIDENCE`.

Adapter compatibility is structural only.

## 22. Execution authorization request

`ExecutionAuthorizationRequest` records request id, activation id, module/specification ids and versions, intake evaluation id, Prepared Observation package id, handoff contract, adapter, input/output contracts, scientific specification, frozen horizon, requested interval, requesting execution identity, duplicate policy, rerun reason, governing versions, explicit authorization, intake state, handoff state, lineage/reproducibility state, blocking diagnostics, bypass flags, and conditional/unresolved/insufficient authorization flags.

## 23. Execution authorization states

The exact implemented execution states are:

`EXECUTION_AUTHORIZED`, `EXECUTION_CONDITIONALLY_AUTHORIZED`, `EXECUTION_UNRESOLVED`, `EXECUTION_BLOCKED`, `EXECUTION_EXCLUDED`, `INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE`.

No scientific-result states are exposed.

## 24. Execution authorization precedence

Execution authorization fails closed through retired/excluded module, non-active module, suspended/deactivated module, invalid or expired activation, superseded activation, direct upstream bypass, raw Prepared Observation bypass, incompatible intake, incomplete handoff, incompatible adapter, adapter scientific transformation, missing contracts/specifications, version mismatch, incomplete lineage/reproducibility, blocking inherited or intake diagnostics, duplicate/conflicting execution, unresolved/insufficient authorization, conditional authorization, and finally authorization.

## 25. Execution diagnostics

Implemented execution diagnostics include `MODULE_NOT_ACTIVE`, `ACTIVATION_EXPIRED`, `ACTIVATION_SUPERSEDED`, `INTAKE_STATE_NOT_ACCEPTED`, `HANDOFF_INCOMPLETE`, `ADAPTER_INCOMPATIBLE`, `SCIENTIFIC_TRANSFORMATION_IN_ADAPTER`, missing input/output/scientific/frozen-horizon contracts, version incompatibility, incomplete lineage/reproducibility, blocking inherited/intake diagnostics, duplicate execution, conflicting execution, direct upstream bypass, raw Prepared Observation bypass, insufficient evidence, and missing explicit execution authorization.

## 26. Execution limitations

Execution limitations are deterministic and include reference-only, synthetic-registry-only, and conditional authorization where applicable. They do not create scientific support.

## 27. Deterministic execution identity

`deterministic_execution_identity()` hashes stable scientific-governance fields: activation id, module id/version, activation specification version, scientific specification version, frozen horizon version, intake evaluation id, Prepared Observation package id, adapter version, input contract version, and output contract version.

Operational requesting identity is intentionally excluded.

## 28. Duplicate execution

`DuplicateExecutionState` represents `NO_DUPLICATE`, `EXACT_RERUN`, `AUTHORIZED_RERUN`, `ACCIDENTAL_DUPLICATE`, `CONFLICTING_DUPLICATE`, `SUPERSEDING_EXECUTION`, `CORRECTED_RERUN`, `SPECIFICATION_CHANGED_RERUN`, and `HORIZON_CHANGED_RERUN`.

Duplicates never silently overwrite prior records.

## 29. Rerun semantics

`RerunClassification` represents identical deterministic, environment-only, code-version, adapter-version, input-contract, output-contract, scientific-specification, horizon-version, corrected-upstream-data, diagnostic-schema, and reproducibility-schema reruns.

Reruns are metadata-only classifications; no rerun execution is performed.

## 30. Supersession

`SupersessionRecord` preserves superseded id, superseding id, reason, and negative-evidence preservation. Superseded records remain traceable.

## 31. Suspension

`LifecycleRecord` supports suspension reasons such as schema incompatibility, adapter drift, incomplete lineage, reproducibility failure, contamination concern, horizon conflict, or governance action. Suspended modules cannot authorize execution.

## 32. Deactivation

Deactivation is represented as lifecycle metadata. It ends activity without deleting prior artifacts or converting the state into scientific retirement.

## 33. Retirement

Retirement is represented as lifecycle metadata and preserves negative evidence. Retired modules produce `MODULE_RETIRED` at activation and `EXECUTION_EXCLUDED` at execution authorization.

## 34. Registry snapshots

`RegistrySnapshot` is an immutable in-memory synthetic snapshot containing module registrations, activation declarations, adapters, intake contracts, module input/output contracts, scientific specifications, frozen horizon specifications, execution authorizations, execution identities, suspension, deactivation, retirement, and supersession records.

There is no mutable global registry service.

## 35. Registry authority diagnostics

Registry diagnostics cover missing snapshot, duplicate registry key, conflicting registry version, missing authoritative record, ambiguous authoritative record, superseded record selected, and inactive record selected.

## 36. Version compatibility

`VersionCompatibility` fails closed for module, module specification, intake contract, activation declaration, adapter, input contract, output contract, scientific specification, frozen horizon, information-role schema, diagnostic schema, artifact-lineage schema, and reproducibility schema incompatibility.

No automatic migration is performed.

## 37. Negative-evidence preservation

Negative-evidence policy is represented as a bound activation policy. Lineage metadata records that negative-evidence artifacts are preserved. Supersession and retirement records also preserve negative evidence.

No scientific negative evidence is generated.

## 38. Falsification-policy binding

The activation declaration binds a versioned falsification policy string and activation evaluation checks the falsification prerequisite. Missing policy yields `FALSIFICATION_POLICY_UNRESOLVED`.

No falsification is executed.

## 39. Contamination-control binding

The activation declaration binds a contamination-control policy string and activation evaluation checks contamination-control readiness. Execution authorization blocks direct upstream bypass, raw Prepared Observation bypass, and scientific transformation in adapters.

No scientific contamination testing is performed.

## 40. Artifact lineage

`ArtifactLineage` reconstructs Source Authority, PIT, Comparator, Prepared Observation, Intake Contract, Module Registration, Intake Evaluation, Handoff, Activation Declaration, Adapter, Module Input Contract, Module Output Contract, Scientific Specification, Frozen Horizon, Execution Authorization, and Deterministic Execution Identity artifacts.

Scientific Execution and Scientific Output artifacts are explicitly empty.

## 41. Reproducibility

`ReproducibilityMetadata` records governing design version, implementation version, fixture identifier, module version, intake contract version, activation declaration version, adapter version, input/output contract versions, scientific specification version, frozen horizon version, Prepared Observation version, information-role schema version, diagnostic schema version, lineage schema version, reproducibility schema version, and stable serialization format version.

## 42. Stable serialization

Activation evaluations, execution authorizations, and registry snapshots expose deterministic `stable_json()` using sorted keys, explicit enum values, deterministic tuple ordering, no random UUIDs, no runtime timestamps, no absolute paths, no memory addresses, and no environment-specific values.

## 43. Information-contract boundaries

Activation results expose registration/declaration metadata, activation state, diagnostics, limitations, prerequisites, adapter metadata, version compatibility, lineage, reproducibility, registry references, and governing versions.

Execution results expose authorization state, deterministic execution identity, diagnostics, limitations, references, duplicate/rerun metadata, lineage, reproducibility, and governing versions.

Both result types refuse scientific measurements, formulas, signals, factors, candidates, panels, IC, Sharpe, predictions, validation results, portfolio decisions, production decisions, ML features, ML labels, and model training.

## 44. Synthetic fixture coverage

`canonical_activation_registry_fixtures()` returns 68 fixtures covering registration/specification, selected real-module blockers, synthetic activation states, policy binding, lineage/reproducibility/version blockers, adapter transformation and bypass controls, execution authorization, duplicates, reruns, supersession, and registry authority diagnostics.

Synthetic active fixtures are clearly synthetic and do not imply real selected-module activation.

## 45. Combined-failure coverage

Tests cover combined activation failures including missing registration plus absent authority, broad/narrow mismatch, missing scientific and horizon specifications, incomplete lineage plus reproducibility, unresolved contamination plus missing negative-evidence policy, and multiple real-evidence blockers.

Tests cover combined execution failures including suspended plus duplicate, retired plus otherwise executable, inactive plus accepted intake, direct upstream bypass, adapter transformation, blocking inherited diagnostic, blocking intake diagnostic, raw Prepared Observation bypass, and multiple fatal execution blockers.

## 46. Acceptance-test coverage

The test suite directly covers exact enum inventories, broad/narrow separation, selected real-module blocked state, no auto-activation, explicit activation, activation invariant, prerequisites, policies, versions, lineage, reproducibility, intervals, suspension, deactivation, retirement, adapter transformation prohibition, active-module execution requirement, intake acceptance, handoff completeness, duplicate/rerun/supersession behavior, deterministic execution identity, stable serialization, diagnostic and limitation ordering, artifact lineage, negative-evidence preservation, falsification policy, contamination controls, registry diagnostics, no scientific output, no formula/signal/factor result, no validation/production/ML output, and upstream compatibility.

## 47. Real selected-module blocked result

The real selected-module scenario produces:

- `MODULE_ACTIVATION_BLOCKED`
- `EXECUTION_BLOCKED`

This is the correct result because external authority evidence, PIT identity/context evidence, comparator evidence, Prepared Observations, and real adapter/input/output contracts remain unavailable for real scientific use.

## 48. Synthetic active-module fixture boundary

The synthetic active fixture requires an explicit active activation declaration and explicit execution authorization. It is synthetic governance evidence only and does not activate the selected module for real scientific use.

## 49. Upstream compatibility

The combined upstream suite passed with Source Authority, PIT Identity and Context Evidence, Comparator Construction, First Module, Prepared Observations, Scientific Module Intake, and the new Activation Registry/Execution Authorization tests.

The new layer imports no upstream runtime objects and does not call upstream construction or intake recomputation.

## 50. Determinism results

Repeated same-process activation and execution evaluations are equal. Same-process stable serialization is stable. A separate-process stable serialization hash matched the local hash.

Deterministic execution identity ignores operational requesting identity and changes when a stable scientific-governance version field changes.

## 51. Scope-boundary verification

Prohibited-scope searches found expected matches in enum names, metadata field names, guardrail flags, diagnostic names, refusal fields, and negative assertions. No source retrieval, database access, network access, scientific library dependency, filesystem write, subprocess use inside the implementation, random UUID generation, runtime timestamp, dynamic import, formula execution, signal generation, factor generation, validation, production, optimization, or ML behavior was found.

The test file uses `subprocess` only for the required separate-process determinism check.

## 52. Known limitations

Known limitations:

- synthetic-only in-memory registry snapshots;
- no durable registry persistence;
- no API, scheduler, orchestration service, or live configuration;
- no real adapter;
- no real module input or output contract;
- no real Prepared Observations for the selected module;
- no authoritative external source;
- no PIT identity/context or comparator evidence;
- no scientific measurement, formula, panel, IC, validation, production, or ML readiness.

## 53. Implementation-readiness conclusion

The reference implementation is complete for bounded activation-governance and execution-authorization behavior. It proves that a module can be selected and registered without being scientifically activated, that a structurally valid activation declaration can remain blocked by missing real evidence, that ready does not auto-promote to active, that execution requires active status and explicit authorization, and that authorization produces no scientific result.

## 54. Exactly one recommended next lifecycle step

Recommended next lifecycle step:

`Project Underdog - Phase 5 Scientific Module Activation Registry And Execution Authorization Executable Conformance Review v1`.
