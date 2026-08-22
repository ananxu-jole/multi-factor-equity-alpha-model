# Project Underdog - Phase 5 Selected Scientific Module Adapter Reference Implementation v1

Date: 2026-08-08

## 1. Executive classification

Final classification: `SELECTED_SCIENTIFIC_MODULE_ADAPTER_REFERENCE_IMPLEMENTATION_COMPLETE`

This note records the bounded, deterministic, synthetic reference implementation of the selected Phase 5 scientific-module adapter. The implementation maps an execution-authorized Scientific Module Intake handoff into a frozen module input contract without executing the scientific module or producing scientific outputs.

## 2. Purpose

The implementation answers the structural question: can an authorized intake handoff be converted into a frozen module input while preserving governed metadata, lineage, roles, diagnostics, limitations, temporal metadata, reproducibility, and scope boundaries?

## 3. Files created

- `pipelines/project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1.py`
- `tests/test_project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1.py`
- `docs/research_notes/project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1.md`

## 4. Files modified

Only the three new files above were modified by this task. No existing implementation, test, governance, research, or production file was changed.

## 5. Authoritative design

The normative design is `docs/research_notes/project_underdog_phase5_selected_scientific_module_adapter_and_frozen_activation_specification_design_v1.md`, classification `SELECTED_MODULE_ADAPTER_AND_FROZEN_ACTIVATION_SPECIFICATION_DESIGN_DEFINED`.

## 6. Architectural position

Implemented position:

```text
Execution Authorization
        -> Scientific Module Intake Handoff
        -> Selected Module Adapter
        -> Frozen Module Input Contract
```

The adapter does not implement Scientific Module Execution, Scientific Measurement, Scientific Result Generation, Validation, Production, or Machine Learning.

## 7. Scientific-boundary separation

The implementation preserves:

```text
Execution authorized
        != Adapter compatible
        != Frozen module input produced
        != Scientific execution
        != Scientific support
        != Validation success
```

No state collapses those concepts.

## 8. Selected research program

Preserved exactly:

`Peer-Relative Post-Stress Repair And Stabilization Asymmetry`

## 9. Narrow activation specification

Preserved exactly:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

The broad program label cannot replace or expand the narrow specification.

## 10. Adapter registration model

Implemented immutable `AdapterRegistrationMetadata` with adapter registration id, adapter id/version, module id/version, research program id/version, activation specification id/version, intake and handoff contract ids/versions, module input contract id/version, scientific specification id/version, frozen horizon id/version, schema versions, adapter status, artifact reference, governing versions, and `scientific_transformation_permitted=False`.

## 11. Frozen activation specification model

Implemented immutable `FrozenActivationSpecification` with frozen and narrow specification identities, permitted/prohibited roles, target/context/comparator contracts, temporal policies, coverage and missingness policies, frozen horizon binding, negative-evidence, falsification, contamination policy references, module input contract binding, schema versions, and governing versions.

## 12. Adapter invariant

Every evaluation references execution authorization, activation declaration, module id/version, research program, activation specification, intake evaluation, Prepared Observation package, handoff contract, adapter, module input contract, scientific specification, frozen horizon, Source Authority lineage, PIT lineage, Comparator lineage, Prepared Observation lineage, Intake lineage, Activation lineage, Execution Authorization lineage, reproducibility metadata, and governing versions.

## 13. Authoritative-chain validation

The adapter verifies one consistent chain:

```text
Execution Authorization
        -> Activation
        -> Intake Evaluation
        -> Prepared Observation
        -> Handoff Contract
        -> Adapter Registration
        -> Frozen Module Input
```

Wrong-but-nonblank activation, intake, handoff, adapter, module, specification, horizon, and input-contract references fail closed.

## 14. Execution-authorization requirement

Only `EXECUTION_AUTHORIZED` can produce `FROZEN_MODULE_INPUT_READY`. Blocked, unresolved, excluded, insufficient, or conditional authorization states remain distinct and cannot be silently promoted.

## 15. Structural mapping

The adapter maps only admitted metadata: target observation metadata, context attachments, comparator attachments, role bindings, observation-time metadata, temporal metadata, coverage metadata, missingness metadata, inherited diagnostics, inherited limitations, lineage, reproducibility metadata, and governing versions.

## 16. Information-role preservation

The required role is `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION`. Diagnostic, explanatory, negative, validated-alpha, comparator-to-alpha, context-to-signal, alias, and inferred role promotion are refused.

## 17. Temporal preservation

Observation time and temporal metadata are copied exactly from the intake handoff. The adapter performs no interpolation, synchronization, filling, carry-forward, resampling, temporal repair, horizon selection, or horizon expansion.

## 18. Frozen-horizon binding

The frozen horizon must match the activation-authorized frozen horizon id and version. Missing, wrong, alternate, broader, runtime-selected, or post hoc horizon references fail closed.

## 19. Scientific-specification binding

The scientific specification id and version must match the authorized chain and adapter registration. Missing, wrong, superseded, broad-program-substituted, or synthetic convenience specifications fail closed.

## 20. Version compatibility

Version checks fail closed across adapter version, handoff contract version, module input contract version, scientific specification version, frozen activation specification version, frozen horizon version, information-role schema, diagnostic schema, lineage schema, and reproducibility schema.

## 21. Adapter states

Implemented exact adapter-state inventory:

- `SELECTED_MODULE_ADAPTER_COMPATIBLE`
- `SELECTED_MODULE_ADAPTER_CONDITIONALLY_COMPATIBLE`
- `SELECTED_MODULE_ADAPTER_UNRESOLVED`
- `SELECTED_MODULE_ADAPTER_INCOMPATIBLE`
- `SELECTED_MODULE_ADAPTER_EXCLUDED`
- `INSUFFICIENT_SELECTED_MODULE_ADAPTER_EVIDENCE`

## 22. Frozen-input states

Implemented exact frozen-input-state inventory:

- `FROZEN_MODULE_INPUT_READY`
- `FROZEN_MODULE_INPUT_CONDITIONALLY_READY`
- `FROZEN_MODULE_INPUT_UNRESOLVED`
- `FROZEN_MODULE_INPUT_INCOMPLETE`
- `FROZEN_MODULE_INPUT_EXCLUDED`
- `INSUFFICIENT_FROZEN_MODULE_INPUT_EVIDENCE`

## 23. Decision precedence

The implementation accumulates diagnostics and then applies deterministic precedence: excluded activation/module, execution not authorized, bypass, chain mismatch, broad/narrow mismatch, scientific transformation enabled, missing or mismatched references, version mismatch, frozen activation mismatch, scientific specification mismatch, frozen horizon mismatch, lineage and reproducibility failure, role mismatch, target/context/comparator mapping failure, temporal incompatibility, coverage insufficiency, required missingness, unresolved, insufficient, conditional, then compatible.

## 24. Adapter diagnostics

Implemented deterministic structural diagnostics including all required codes: execution not authorized, activation/intake/Prepared Observation/handoff/adapter/module/research-program/activation-specification/input-contract/scientific-specification/frozen-horizon mismatches, scientific transformation prohibited, version incompatibilities, lineage/reproducibility incompleteness, prohibited or missing roles, target/context/comparator mapping failure, temporal incompatibility, coverage insufficiency, missingness failure, direct upstream bypass, and raw Prepared Observation bypass.

## 25. Adapter limitations

Implemented deterministic limitations:

- `REFERENCE_IMPLEMENTATION_ONLY`
- `SYNTHETIC_ADAPTER_ONLY`
- `SYNTHETIC_AUTHORIZED_EXECUTION_ONLY`
- `REAL_SELECTED_MODULE_EXECUTION_BLOCKED_UPSTREAM`
- `REAL_ADAPTER_NOT_PLATFORM_INTEGRATED`
- `REAL_MODULE_EXECUTION_NOT_IMPLEMENTED`

Limitations do not mask blockers.

## 26. Frozen module input contract

Implemented immutable `FrozenModuleInputContract` with the requested structural fields, inherited diagnostics and limitations, adapter diagnostics and limitations, artifact lineage, reproducibility metadata, governing versions, and metadata-only information contract.

## 27. Deterministic frozen-input identity

`deterministic_frozen_input_identity()` derives identity from governance-relevant stable fields: execution authorization id, activation id, intake evaluation id, Prepared Observation package id, handoff id, adapter id/version, module input contract version, scientific specification version, frozen activation specification version, and frozen horizon version.

Requester metadata does not affect identity. Governance changes alter identity.

## 28. Artifact lineage

The frozen input preserves lineage for Source Authority, PIT, Comparator, Prepared Observation, Intake Contract, Intake Evaluation, Handoff Contract, Module Registration, Activation Declaration, Execution Authorization, Adapter Registration, Frozen Activation Specification, Module Input Contract, Scientific Specification, Frozen Horizon, and Frozen Module Input.

It creates no Scientific Execution, Scientific Result, Measurement, or Validation artifact.

## 29. Reproducibility

Implemented reproducibility metadata includes governing design version, adapter implementation version, fixture identifier, module version, intake and handoff contract versions, activation specification version, adapter version, module input contract version, scientific specification version, frozen activation specification version, frozen horizon version, Prepared Observation version, schema versions, stable serialization version, deterministic serialization, and controlled reference flags.

## 30. Stable serialization

`stable_json()` uses sorted keys, deterministic tuple/list ordering through immutable contracts, enum value serialization, no memory addresses, no random identifiers, no current timestamps, no absolute paths, and no environment-specific values.

## 31. Information-contract boundaries

The information contract exposes structural/governance metadata only. It explicitly refuses formulas, repair outputs, peer-common repair, idiosyncratic repair, decomposition output, stabilization outputs, asymmetry outputs, signals, factors, ranks, scores, candidates, panels, IC, Sharpe, predictions, validation results, portfolio decisions, production outputs, ML features, ML labels, and model training.

## 32. Synthetic fixture coverage

Implemented 47 canonical fixtures covering valid target-only, target+comparator, target+context, target+context+comparator, alternate valid handoff, deterministic repeat, accepted conditional mapping, real selected-module blocked behavior, authorization failures, chain mismatches, version failures, role failures, mapping failures, lineage, reproducibility, scientific transformation, bypass, temporal, coverage, and missingness failures.

## 33. Combined-failure coverage

Tests include combined diagnostic accumulation for adapter mismatch, input-contract mismatch, scientific transformation enabled, target mapping incomplete, and context mapping incomplete. The fixture matrix also includes combined upstream-blocked and mapping-failure cases.

## 34. Acceptance-test coverage

Focused test suite covers exact state inventories, fixture expectations, real selected-module blocked behavior, synthetic ready behavior, authorization requirement, authoritative chain requirement, wrong references, broad/narrow boundary, no scientific transformation, role preservation, temporal and horizon preservation, scientific specification, versions, lineage, reproducibility, target/context/comparator mapping, coverage, missingness, diagnostic accumulation, limitation ordering, deterministic identity, stable serialization, alternate chains, information-contract refusals, scientific-artifact absence, and upstream compatibility imports.

## 35. Real selected-module blocked behavior

The real selected-module scenario returns nonready states because upstream activation and execution remain blocked. It does not produce `FROZEN_MODULE_INPUT_READY`.

## 36. Synthetic positive behavior

Only synthetic authorized fixtures with active activation, authorized execution, matching handoff chain, matching adapter registration, matching frozen activation specification, matching module input contract, matching scientific specification, matching frozen horizon, valid roles, lineage, and reproducibility reach `SELECTED_MODULE_ADAPTER_COMPATIBLE` and `FROZEN_MODULE_INPUT_READY`.

## 37. Upstream compatibility

The implementation imports and consumes public reference contracts from Prepared Observations, Scientific Module Intake, and Activation Registry/Execution Authorization. It does not modify or recompute those layers.

## 38. Determinism results

Repeated same-process evaluation produced identical result objects and stable JSON. Separate-process SHA-256 checks produced the same frozen input id and stable JSON hash:

- frozen input id: `frozen_module_input_8734f6da6e7ee76079db01d6`
- SHA-256: `83222892f245904770263a876b55348599dd2e807630c67899974834bc1518f4`

## 39. Scope-boundary verification

Boundary searches found no prohibited dependency imports, file writes, network access, random ids, runtime timestamps, dynamic imports, model fitting, prediction, or training behavior. Scientific terms appear only as frozen labels, refusal fields, diagnostics, guardrail flags, and negative assertions.

## 40. Known limitations

This is a synthetic reference implementation. It is not platform-integrated, does not run the real selected scientific module, does not prove empirical information, and does not authorize formula, panel, IC, validation, production, threshold, survivor-status, or ML work.

## 41. Implementation conclusion

The selected scientific-module adapter reference implementation is complete within its bounded scope. It proves that an execution-authorized package can be mapped into a frozen module input without changing the science, that wrong-but-nonblank governance references fail closed, that the adapter does not recompute upstream governance, that the broad research-program label cannot expand the narrow activation specification, and that a frozen module input is structurally ready without containing a scientific result.

Final classification restated: `SELECTED_SCIENTIFIC_MODULE_ADAPTER_REFERENCE_IMPLEMENTATION_COMPLETE`

## 42. Exactly one recommended next lifecycle step

`Project Underdog - Phase 5 Selected Scientific Module Adapter Executable Conformance Review v1`
