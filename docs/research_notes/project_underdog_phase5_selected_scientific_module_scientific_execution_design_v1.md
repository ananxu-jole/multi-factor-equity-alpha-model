# Project Underdog - Phase 5 Selected Scientific Module Scientific Execution Design v1

Date: 2026-08-09

Final classification: `SELECTED_MODULE_SCIENTIFIC_EXECUTION_DESIGN_DEFINED`

This note defines the scientific execution design for exactly one frozen mechanism: `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`. It is not an implementation task, validation task, production task, optimization task, or ML task.

Repository basis:

- `docs/research_notes/project_underdog_phase5_selected_scientific_module_adapter_executable_conformance_review_v1.md`: adapter implementation is conformant with minor observations; `FROZEN_MODULE_INPUT_READY` is structural only and does not imply scientific execution or support.
- `docs/research_notes/project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1.md`: only synthetic authorized fixtures reach `FROZEN_MODULE_INPUT_READY`; real selected-module execution remains blocked upstream.
- `docs/research_notes/project_underdog_phase5_selected_scientific_module_adapter_and_frozen_activation_specification_design_v1.md`: the adapter is a structural bridge and does not execute formulas or science.
- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: the broad research program is too wide; the first frozen module is the common-versus-idiosyncratic repair decomposition only.
- `docs/research_notes/project_underdog_first_module_formula_specification_v1.md`: the approved source-independent formula specification defines the common component, idiosyncratic component, unresolved behavior, and approved decomposition states; stabilization, asymmetry, macro conditioning, VoV, participation/liquidity, rank, transition, leadership, dispersion, and event clustering remain outside scope.
- `docs/research_notes/project_underdog_first_module_reference_implementation_v1.md`: historical first-module reference implementation evidence exists, but this note does not modify or run it.

## 1. Purpose

Scientific execution is the layer that applies the already-approved frozen scientific specification to an authorized `Frozen Module Input` and emits a deterministic `Scientific Execution Result`.

Lifecycle distinctions:

| Concept | Meaning | Status in this design |
| --- | --- | --- |
| Structural readiness | Upstream governance and adapter contracts produced a complete frozen input. | Required precondition, not science. |
| Execution readiness | The frozen input is admissible for the scientific execution layer. | Checked before formula invocation. |
| Scientific execution | Approved formulas and decomposition logic run deterministically. | Designed here. |
| Scientific evidence | The execution result records the module's decomposition outcome, diagnostics, limitations, and lineage. | Produced by execution, not validated here. |
| Validation | Later assessment of empirical usefulness, IC, robustness, or out-of-sample behavior. | Excluded. |
| Production | Any operational trading, registry promotion, portfolio, threshold, or deployment decision. | Excluded. |

## 2. Scientific ownership boundary

The execution layer owns:

- formula execution for the approved decomposition formula only;
- scientific decomposition into approved common, idiosyncratic, mixed, or unresolved states;
- unresolved handling when scientific preconditions fail;
- deterministic scientific outputs;
- scientific diagnostics;
- scientific limitations;
- scientific lineage.

The execution layer explicitly does not own:

- data acquisition;
- source authority;
- PIT identity;
- ticker or security lineage;
- economic-context authority;
- comparator construction;
- Prepared Observation construction;
- Intake;
- Activation;
- Adapter behavior;
- execution authorization;
- validation;
- optimization;
- production;
- ML.

## 3. Frozen scientific scope

Execution is bound exactly to:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

The broader research program remains:

`Peer-Relative Post-Stress Repair And Stabilization Asymmetry`

The broader label is not the execution boundary. This design does not introduce execution for stabilization, repair asymmetry, macro conditioning, leadership transition, participation transition, volatility-of-volatility, dispersion, event clustering, ranking, validation, portfolio construction, production, or machine learning.

## 4. Execution invariant

Execution may begin only when all invariant elements are present and mutually consistent:

- `Frozen Module Input`;
- frozen activation specification;
- scientific specification;
- frozen horizon;
- reproducibility metadata;
- complete Source Authority, PIT, Comparator, Prepared Observations, Intake, Activation, Adapter, and Frozen Module Input lineage;
- deterministic execution identity;
- approved formula version;
- approved decomposition-state inventory;
- no upstream blocking diagnostics that make scientific execution inadmissible.

Failure of any invariant element must produce a non-executed or unresolved scientific result, not a partial scientific computation.

## 5. Scientific execution stages

Deterministic stages:

1. Frozen Input Verification: confirm frozen input readiness, identity, version, lineage, reproducibility, and no prohibited scientific-output carryover.
2. Scientific Preconditions: confirm post-stress eligibility, target observation availability, comparator observation availability, temporal ordering, coverage, and unresolved-state gates.
3. Formula Invocation: invoke only the approved frozen formula specification.
4. Common Component Computation: execute only the approved peer-common component.
5. Idiosyncratic Component Computation: execute only the approved target-minus-common component.
6. Decomposition Classification: assign only approved decomposition states.
7. Scientific Diagnostics: emit deterministic execution diagnostics for execution-layer conditions.
8. Scientific Result Packaging: package decomposition result, diagnostics, limitations, lineage, reproducibility, and execution identity.
9. Scientific Lineage: bind result lineage to all upstream artifacts and the scientific execution artifact.
10. Scientific Reproducibility: emit stable serialization and version metadata.

No additional scientific mechanism is introduced.

## 6. Formula ownership

Approved formulas execute only inside the scientific execution layer after frozen input verification passes.

Execution must preserve:

- no alternative formulas;
- no optimization;
- no adaptive thresholds;
- no hidden weighting;
- no normalization;
- no ranking;
- no prediction.

The execution layer may call or implement the approved formula semantics from `docs/research_notes/project_underdog_first_module_formula_specification_v1.md`. It must not redefine the formula, change signs, select horizons, estimate coefficients, add controls, or transform results into alpha claims.

## 7. Common component

The execution layer owns the computation of the approved common component only after comparator evidence has already been authorized, prepared, admitted, and frozen upstream.

Execution does not construct peer groups, select comparators, alter membership, repair missing comparator observations, weight comparators adaptively, or infer economic comparability. It computes the approved peer-common component from already-frozen comparator repair observations.

## 8. Idiosyncratic component

The execution layer owns the approved idiosyncratic component only as the deterministic contrast between already-approved own repair and the approved common component.

It must not interpret this component as causal idiosyncrasy, predictive alpha, regression residual, validation evidence, ranking input, or production signal.

## 9. Decomposition outputs

Execution may emit only approved decomposition states:

- `common`;
- `idiosyncratic`;
- `mixed`;
- `unresolved`.

No additional states, confidence labels, ranks, scores, alpha labels, candidate labels, portfolio labels, validation labels, or ML labels are permitted.

## 10. Scientific diagnostics

Scientific diagnostics describe execution behavior only. They may include:

- frozen input not ready;
- scientific specification mismatch;
- formula version mismatch;
- frozen horizon mismatch;
- post-stress context unresolved;
- target repair unavailable;
- common component unavailable;
- idiosyncratic component unavailable;
- comparator observations insufficient;
- decomposition unresolved;
- scientific lineage incomplete;
- scientific reproducibility incomplete.

Diagnostics must not include Sharpe, IC, p-values, validation outcome, production readiness, candidate status, portfolio effect, model score, or predictive support.

## 11. Scientific limitations

Deterministic scientific limitations may include:

- `SYNTHETIC_EXECUTION_ONLY`;
- `REFERENCE_IMPLEMENTATION_ONLY`;
- `UNRESOLVED_DECOMPOSITION`;
- `INSUFFICIENT_SCIENTIFIC_EVIDENCE`;
- `REAL_SELECTED_MODULE_BLOCKED_UPSTREAM`;
- `VALIDATION_NOT_PERFORMED`;
- `PRODUCTION_NOT_AUTHORIZED`;

Limitations must not mask blockers or convert unresolved evidence into supported evidence.

## 12. Determinism

Scientific execution must be deterministic:

- identical frozen inputs produce identical outputs;
- identical frozen inputs produce identical diagnostics;
- identical frozen inputs produce identical limitations;
- identical frozen inputs produce identical lineage;
- identical frozen inputs produce identical serialization.

Runtime timestamps, random identifiers, environment-dependent paths, process-order effects, adaptive thresholds, and data-dependent optimization are prohibited.

## 13. Scientific result contract

The scientific result contract is metadata-and-result-only. It may include:

- scientific execution id;
- deterministic execution identity;
- module id/version;
- frozen module input id;
- frozen activation specification id/version;
- scientific specification id/version;
- formula version;
- frozen horizon version;
- decomposition result;
- approved component values if produced by the approved formula;
- scientific diagnostics;
- scientific limitations;
- scientific lineage;
- reproducibility metadata;
- stable serialization metadata.

It must exclude:

- Sharpe;
- IC;
- alpha approval;
- ranking;
- candidate selection;
- portfolio decision;
- prediction;
- validation result;
- production decision;
- optimization result;
- ML feature, label, fit, or training output.

## 14. Scientific lineage

Scientific lineage must preserve the chain:

```text
Source Authority
PIT
Comparator
Prepared Observations
Intake
Activation
Adapter
Frozen Module Input
Scientific Execution
Scientific Result
```

Execution may add scientific execution and scientific result artifacts. It must not mutate upstream lineage and must not create validation, candidate, panel, IC, production, or ML artifacts.

## 15. Reproducibility

Execution reproducibility metadata must include:

- execution version;
- scientific specification version;
- formula version;
- frozen horizon version;
- frozen activation specification version;
- frozen input contract version;
- adapter version;
- reproducibility version;
- stable serialization version;
- deterministic execution identity;
- fixture or controlled-reference identifier for synthetic runs.

Reproducibility failure must block ready scientific output or force unresolved status.

## 16. Negative evidence

Unresolved, unavailable, insufficient, or negative scientific outcomes are preserved as scientific evidence. They must not be reinterpreted, removed, renamed into a positive result, or used to tune formulas.

The execution layer may record a negative or unresolved result, but it does not decide module retirement, validation failure, or production exclusion. Those remain later falsification and validation responsibilities.

## 17. Falsification boundary

Execution exposes information that future falsification work may use:

- decomposition result;
- unresolved reason;
- diagnostic inventory;
- limitation inventory;
- formula version;
- frozen horizon version;
- lineage;
- reproducibility metadata.

Execution itself must not perform validation, IC analysis, negative-control testing, ablation testing, retirement decisions, or anti-resurrection decisions.

## 18. Contamination controls

Execution must prohibit:

- upstream mutation;
- downstream mutation;
- hidden measurements;
- adaptive execution;
- dynamic thresholds;
- runtime optimization;
- formula substitution;
- horizon substitution;
- comparator re-selection;
- role promotion;
- output ranking;
- prediction;
- validation leakage.

If contamination is detected inside the frozen input or execution context, execution must fail closed or produce unresolved diagnostics.

## 19. Compatibility

Compatibility:

| Component | Compatibility claim | No-modification boundary |
| --- | --- | --- |
| Frozen Module Input | Execution consumes only a ready frozen input. | Does not alter adapter output. |
| First Module | Execution preserves the approved common-versus-idiosyncratic formula and states. | Does not modify historical First Module files. |
| Future validation | Result contract exposes lineage, diagnostics, and reproducibility that validation can later consume. | Does not define validation metrics or run validation. |
| Future production | Result contract can be audited before any future production discussion. | Does not create production logic or decisions. |

## 20. Known limitations

Deferred capabilities:

- implementation code;
- synthetic execution fixtures;
- executable acceptance tests;
- real source access;
- real PIT identity construction;
- real comparator construction;
- real Prepared Observation construction;
- live module activation;
- scientific execution run;
- validation;
- production;
- optimization;
- ML.

The design also inherits the adapter conformance review's minor observations around future platform-integration ergonomics; they do not block design readiness.

## 21. Implementation readiness

Implementation-readiness conclusion:

`READY_FOR_BOUNDED_SCIENTIFIC_EXECUTION_REFERENCE_IMPLEMENTATION`

This means the design is sufficient for a bounded synthetic scientific execution reference implementation. It does not authorize live execution, real data, validation, production, optimization, or ML.

## 22. Exactly one recommended next lifecycle step

`Project Underdog - Phase 5 Selected Scientific Module Scientific Execution Reference Implementation v1`

This next step should implement only bounded synthetic scientific execution for the frozen mechanism. It must not implement validation, production, optimization, machine learning, peer construction, source retrieval, or any broader module.
