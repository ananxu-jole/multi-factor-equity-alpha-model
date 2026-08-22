# Project Underdog - Phase 5 Scientific Module Intake Reference Implementation v1

## 1. Executive classification

Final classification: `SCIENTIFIC_MODULE_INTAKE_REFERENCE_IMPLEMENTATION_COMPLETE`.

This classification applies only to the bounded, synthetic, deterministic Scientific Module Intake reference implementation. It does not imply scientific support, predictive value, formula readiness, candidate readiness, panel readiness, IC readiness, validation readiness, production readiness, optimization readiness, or machine-learning usefulness.

## 2. Purpose

This implementation answers the bounded implementation question: whether a Prepared Observation package can be deterministically evaluated against a declared scientific-module intake contract while preserving inherited diagnostics, roles, limitations, temporal metadata, traces, reproducibility metadata, and artifact lineage.

The implemented meaning of intake success is structural only: the package satisfies the declared metadata-only requirements of one scientific module and may proceed to later scientific evaluation. Passing intake is not evidence that a hypothesis is valid, predictive, economically meaningful, useful, validated, or production-ready.

## 3. Files created

Created exactly:

- `pipelines/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py`
- `tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py`
- `docs/research_notes/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.md`

## 4. Files modified

No pre-existing repository files were modified. The implementation touched only the three files listed above.

## 5. Authoritative design

The immutable design input was `docs/research_notes/project_underdog_phase5_prepared_observations_platform_integration_and_scientific_module_intake_design_v1.md`.

Compatibility was checked against:

- `pipelines/project_underdog_phase5_prepared_observations_reference_implementation_v1.py`
- `tests/test_project_underdog_phase5_prepared_observations_reference_implementation_v1.py`
- `docs/research_notes/project_underdog_phase5_prepared_observations_reference_implementation_v1.md`
- `docs/research_notes/project_underdog_phase5_prepared_observations_executable_conformance_review_v1.md`
- upstream Source Authority, PIT Identity and Context Evidence, Comparator Construction, First Module, information-role, artifact-lineage, reproducibility, contamination, negative-evidence, falsification, and frozen-horizon materials identified by repository search.

The design states that intake is a metadata evaluator between Prepared Observations and scientific modules, not a scientific execution layer.

## 6. Architectural position

Implemented only:

```text
Prepared Observation Package
        ->
Scientific Module Intake Evaluation
        ->
Scientific Module Handoff Contract
```

The implementation does not execute a scientific module, query upstream internals, retrofit the First Module, or create scientific outputs.

## 7. Implementation scope

The implementation provides synthetic metadata-only support for intake contract registration, scientific module registration, Prepared Observation package intake, admission evaluation, contract and version compatibility, role matching, attachment binding checks, target/context/comparator compatibility, temporal compatibility, coverage, missingness, inherited diagnostics and limitations, artifact-lineage sufficiency, reproducibility sufficiency, duplicate/conflict/supersession checks, deterministic diagnostics and limitations, compatibility classification, bounded handoff contract, stable serialization, canonical fixtures, and tests.

## 8. Explicit non-responsibilities

The implementation does not perform acquisition, retrieval, APIs, database access, vendor access, authority evaluation, identity construction, identity resolution, context construction, context interpretation, comparator construction, peer discovery, scientific similarity, value transformation, normalization, winsorization, imputation, interpolation, filling, resampling, ranking, scoring, formula execution, return calculation, lag construction, signal calculation, factor construction, candidate generation, panel construction, IC calculation, statistical testing, hypothesis evaluation, validation, portfolio construction, optimization, production decisions, ML feature creation, ML label creation, model fitting, model prediction, or model training.

These prohibitions are represented by false-valued guardrail flags in the result contract and guardrail manifest.

## 9. Intake contract model

`ModuleIntakeContract` is a module-owned structural declaration. It includes contract id/version, module id/version, module specification version, accepted Prepared Observation contract and implementation versions, schema versions, accepted readiness states, conditional readiness policy, target observation requirements, accepted time forms, temporal-alignment requirements, required/optional/prohibited roles, role cardinality, context requirements, comparator requirements, coverage rules, missingness rules, prohibited inherited diagnostics, required traces, reproducibility fields, lineage fields, output contract id, and governing design version.

The contract contains no formulas, coefficient signs, expected returns, expected IC, alpha thresholds, Sharpe thresholds, ranking rules, portfolio rules, optimization objectives, or model parameters.

## 10. Scientific module registration model

`ScientificModuleRegistration` represents module metadata only: module id, module version, module specification version, intake contract id/version, module status, governing versions, and artifact reference.

The registration does not execute the module and does not authorize scientific measurement.

## 11. Prepared Observation input model

The implementation directly consumes the existing Prepared Observations public result contract: `po.PreparedObservationResult` from `pipelines/project_underdog_phase5_prepared_observations_reference_implementation_v1.py`.

The intake layer does not recompute Prepared Observation readiness. It inherits `readiness_state`, diagnostics, limitations, target metadata, context attachments, comparator attachments, temporal metadata, coverage metadata, missingness metadata, upstream traces, reproducibility metadata, and artifact lineage from the supplied package.

## 12. Intake invariant

Each `ScientificModuleIntakeResult` references one Prepared Observation package id, one Prepared Observation artifact-lineage record, one Prepared Observation contract version, one Prepared Observation implementation version, one intake contract id/version, one scientific module id/version, one module specification version, one inherited readiness state, inherited diagnostics, inherited limitations, declared role records, actual role availability, attachment requirement records, actual attachment availability, temporal compatibility, traceability sufficiency, reproducibility sufficiency, one compatibility state, and one intake artifact-lineage record.

Missing invariant elements fail closed through deterministic diagnostics such as `MISSING_INTAKE_CONTRACT`, `UNKNOWN_SCIENTIFIC_MODULE`, `MISSING_PREPARED_OBSERVATION_LINEAGE`, `MISSING_MODULE_LINEAGE`, `INCOMPLETE_REPRODUCIBILITY_METADATA`, or version mismatch diagnostics.

## 13. Prepared Observation admission model

Admission behavior is deterministic:

- `PREPARED_OBSERVATION_EXCLUDED` -> `INTAKE_EXCLUDED`
- `PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE` -> `INTAKE_INCOMPATIBLE`
- `PREPARED_OBSERVATION_UNRESOLVED` -> `INTAKE_UNRESOLVED`
- `INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE` -> `INSUFFICIENT_INTAKE_EVIDENCE`
- `PREPARED_OBSERVATION_CONDITIONALLY_READY` -> accepted only when the contract explicitly allows conditional readiness
- `PREPARED_OBSERVATION_STRUCTURALLY_READY` -> still evaluated against module-specific requirements

This preserves the rule that Prepared Observation structural readiness is not equivalent to module intake compatibility.

## 14. Compatibility-state model

The implementation exposes exactly these states:

- `INTAKE_COMPATIBLE`
- `INTAKE_CONDITIONALLY_COMPATIBLE`
- `INTAKE_UNRESOLVED`
- `INTAKE_INCOMPATIBLE`
- `INTAKE_EXCLUDED`
- `INSUFFICIENT_INTAKE_EVIDENCE`

No hidden fallback states or scientific-performance states are exposed.

## 15. Information-role matching

Role matching is exact against the Prepared Observations information-role vocabulary:

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

The implementation supports required roles, optional roles, prohibited roles, unsupported roles, role cardinality, and attachment binding. It prevents undeclared substitution, alias fallback, diagnostic-to-alpha promotion, explanatory-to-alpha promotion, negative-to-alpha promotion, comparator-to-target-alpha substitution, context-to-signal substitution, and role inference from attachment type alone.

## 16. Target compatibility

Target checks are structural and metadata-only. The implementation checks target presence, accepted target observation type, accepted observation-time form, applicability interval status, target role binding, target trace, target lineage through artifact metadata, target coverage, and required missingness.

The target value is not interpreted.

## 17. Context compatibility

Context requirements are represented by `AttachmentRequirement`. Evaluation checks required/optional/prohibited status, allowed roles, minimum and maximum count, accepted status, accepted temporal state, trace presence, lineage presence, coverage, missingness, duplicate state, conflict state, and supersession state.

The implementation does not create, search for, reinterpret, replace, transform, rank, or score context.

## 18. Comparator compatibility

Comparator requirements use the same structural requirement model. Evaluation checks required presence, exact role, cardinality, inherited eligibility, applicability, temporal compatibility, trace presence, lineage presence, coverage, missingness, duplicate state, conflict state, supersession state, and expired comparator state.

The implementation does not construct comparators, discover peers, rank comparators, score similarity, recompute eligibility, or replace expired comparators.

## 19. Temporal compatibility

The implementation handles point observations, interval observations, open intervals, partial alignment, unknown alignment, non-overlap, stale context, superseded context, expired comparator applicability, discontinuous identity applicability, mixed frequency, and incomplete temporal traceability according to the module contract.

It does not repair time data, define executable PIT logic, calculate lags, resample, synchronize, or select horizons.

## 20. Coverage compatibility

Coverage is evaluated against declared metadata dimensions: target, context, comparator, temporal, information-role, and traceability coverage. Required dimensions must be present and sufficient unless the contract explicitly accepts a limitation.

The implementation does not calculate scientific coverage metrics or infer coverage from real data.

## 21. Missingness compatibility

Missingness checks distinguish required missingness, optional missingness, accepted optional missingness, unavailable evidence, and intentionally excluded evidence. Required missingness may not be silently waived.

The implementation does not impute, zero-fill, drop, repair, synthesize, fill, interpolate, or reinterpret missing values.

## 22. Inherited diagnostics and limitations

The result preserves the complete inherited Prepared Observation diagnostic collection and limitation collection. Intake diagnostics are added separately. Inherited diagnostics are not deleted, renamed, downgraded, normalized, replaced, or semantically reinterpreted.

The contract supports prohibited inherited diagnostics. The current synthetic fatal-diagnostic convention is compatible with Prepared Observations' `fatal_diagnostics` trace key and maps to `INHERITED_FATAL_DIAGNOSTIC` at intake.

## 23. Version compatibility

Fail-closed version checks cover Prepared Observation contract version, Prepared Observation implementation version, intake contract version, module version, module specification version, information-role schema version, diagnostic schema version, artifact-lineage schema version, and reproducibility schema version.

No automatic migration or ambiguous version mapping is implemented.

## 24. Decision precedence

Diagnostics accumulate before final classification. The final state reflects the highest-precedence applicable condition:

1. Prepared Observation exclusion, raw-package bypass, direct-upstream bypass, prohibited role/context/comparator, and superseded package -> `INTAKE_EXCLUDED`.
2. Structural incompleteness, fatal inherited diagnostics, missing lineage, incomplete reproducibility, version incompatibility, missing required roles or attachments, binding conflicts, temporal incompatibility, required missingness, duplicate/conflicting intake, and rejected conditional readiness -> `INTAKE_INCOMPATIBLE`.
3. Prepared Observation unresolved or inherited unresolved diagnostics -> `INTAKE_UNRESOLVED`.
4. Prepared Observation insufficient or missing intake contract evidence -> `INSUFFICIENT_INTAKE_EVIDENCE`.
5. Accepted limitations -> `INTAKE_CONDITIONALLY_COMPATIBLE`.
6. Otherwise -> `INTAKE_COMPATIBLE`.

Applicable diagnostics are preserved; early returns do not erase later diagnostic context.

## 25. Intake diagnostics

The implementation exposes deterministic metadata diagnostics covering admission, contract and version failures, role failures, target failures, context failures, comparator failures, temporal failures, coverage failures, missingness failures, inherited diagnostics, duplicate/conflict/supersession failures, traceability failures, raw Prepared Observation bypass, and direct upstream bypass.

No diagnostics represent weak alpha, low IC, failed hypothesis, low Sharpe, insignificant return, unstable factor, or any other scientific-performance result.

## 26. Intake limitations

Limitations are deterministic and non-blocking only where the contract accepts them. Covered limitations include accepted conditional Prepared Observation readiness, accepted partial temporal alignment, accepted stale context, accepted optional missingness, accepted optional attachment absence, accepted conditional coverage, accepted superseded nonrequired attachment, and inherited informational limitations.

Limitations never mask blocking diagnostics.

## 27. Scientific-module handoff contract

`IntakeInformationContract` exposes only bounded metadata: package id, immutable package metadata, accepted target metadata, accepted context attachments, accepted comparator attachments, information-role bindings, observation-time metadata, temporal compatibility, coverage metadata, missingness metadata, inherited diagnostics, inherited limitations, intake diagnostics, intake limitations, compatibility state, reproducibility metadata, artifact lineage, and governing versions.

The handoff is metadata-only and does not expose scientific outputs.

## 28. Information-contract boundaries

The information contract carries explicit false-valued refusal fields for prohibited outputs:

- `exposes_scientific_result`
- `exposes_formula_output`
- `creates_signal`
- `creates_factor`
- `creates_rank`
- `creates_score`
- `computes_ic`
- `computes_sharpe`
- `creates_prediction`
- `creates_model_feature`
- `creates_model_label`
- `creates_validation_result`
- `makes_production_decision`

The result contract also carries false-valued non-responsibility flags for acquisition, retrieval, authority evaluation, identity work, context interpretation, comparator construction, transformations, formulas, signals, candidates, panels, IC, validation, production, optimization, and ML.

## 29. Reproducibility

Reproducibility metadata includes governing design version, implementation version, fixture identifier, intake contract version, module version, Prepared Observation version, role schema version, diagnostic schema version, lineage schema version, reproducibility schema version, and stable serialization format version.

Identical inputs produce identical state, diagnostics, limitations, bindings, lineage ordering, result object contents, and `stable_json()` output.

## 30. Stable serialization

`ScientificModuleIntakeResult.stable_json()` serializes with sorted keys and compact separators. Enums serialize explicitly to values; tuples serialize deterministically; no runtime timestamps, random UUIDs, absolute repository paths, memory addresses, or environment-dependent values appear in the decision output.

## 31. Artifact lineage

Artifact lineage reconstructs upstream and intake references:

- Source Authority artifacts inherited through Prepared Observations
- PIT Identity and Context artifacts inherited through Prepared Observations
- Comparator Construction artifacts inherited through Prepared Observations
- Prepared Observation artifact
- module intake declaration artifact
- scientific module specification artifact
- intake evaluation artifact
- handoff contract artifact

No scientific execution artifact is created.

## 32. Synthetic fixture coverage

The implementation provides 66 canonical synthetic fixtures, `SMI01_target_only` through `SMI66_duplicate_comparator`.

The fixture set covers fully compatible packages, accepted conditional states, optional context, required context, required comparator, context-plus-comparator intake, negative evidence without promotion, admission failures, contract and version failures, role failures, attachment failures, temporal failures, coverage/missingness/trace/lineage failures, inherited fatal and unresolved diagnostics, raw and direct bypasses, duplicates, conflicts, and supersession.

Fixture verification result:

```text
66
SMI01_target_only SMI66_duplicate_comparator
bad 0
```

## 33. Combined-failure coverage

The test suite includes combined-failure probes for excluded plus otherwise covered packages, prohibited role plus missing comparator, missing intake contract plus otherwise valid package, inherited fatal plus conditional readiness, missing lineage plus full coverage, temporal non-overlap plus optional missingness, missing target plus prohibited context, missing required role plus duplicate comparator, unsupported version plus unresolved inherited diagnostic, raw bypass plus full coverage, direct upstream bypass plus structurally ready package, insufficient coverage plus required missingness, duplicate intake plus conflicting binding, superseded package plus valid comparator, mixed frequency plus partial alignment, comparator conflict plus missing context, role substitution plus valid package shape, missing reproducibility plus optional context absence, structurally incomplete plus prohibited inherited diagnostic, and multiple fatal failures with deterministic diagnostic preservation.

Sample precedence probe:

```text
SMI11_excluded_po INTAKE_EXCLUDED ['PREPARED_OBSERVATION_EXCLUDED']
SMI25_missing_required_role INTAKE_INCOMPATIBLE ['MISSING_REQUIRED_ROLE']
SMI45_temporal_non_overlap INTAKE_INCOMPATIBLE ['PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE', 'TEMPORAL_NON_OVERLAP']
SMI55_missing_po_lineage INTAKE_INCOMPATIBLE ['MISSING_PREPARED_OBSERVATION_LINEAGE']
SMI58_prohibited_inherited_fatal INTAKE_INCOMPATIBLE ['PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE', 'INHERITED_FATAL_DIAGNOSTIC']
SMI60_raw_bypass INTAKE_EXCLUDED ['RAW_PREPARED_OBSERVATION_BYPASS']
SMI64_superseded_po INTAKE_EXCLUDED ['PREPARED_OBSERVATION_EXCLUDED', 'SUPERSEDED_PREPARED_OBSERVATION']
```

## 34. Acceptance-test coverage

The test file contains 19 tests covering the required acceptance areas: state inventory, package admission, structural readiness not equaling intake compatibility, conditional readiness policy, exact role matching, prohibited role conversion, role cardinality, role binding, target/context/comparator compatibility, temporal compatibility, coverage, missingness, inherited diagnostics and limitations, version compatibility, duplicate and supersession behavior, precedence, deterministic diagnostics and limitations, artifact lineage, reproducibility, stable serialization, repeated equality, bounded handoff contract, refusal flags, no scientific outputs, Prepared Observations compatibility, Source Authority/PIT/Comparator trace preservation, First Module conceptual compatibility, and no upstream recomputation.

## 35. Prepared Observations compatibility

The implementation imports and consumes Prepared Observations public types directly. It preserves the inherited readiness state and does not call upstream Source Authority, PIT Identity and Context Evidence, or Comparator Construction components.

The compatibility suite confirms the new layer does not require upstream test changes.

## 36. Upstream trace compatibility

Source Authority traces, PIT traces, and Comparator traces are inherited from the Prepared Observation package and propagated through result traceability, handoff metadata, artifact lineage, and stable serialization.

The intake layer does not re-evaluate Source Authority, reconstruct PIT identity/context evidence, or recompute Comparator Construction eligibility.

## 37. First Module compatibility assessment

The First Module remains unmodified. The intake handoff can conceptually map into `FirstModuleInput` through target id/time bounds, target observation metadata, comparator attachment metadata, qualitative source-independent flags, context flags, PIT membership flags, source-conflict flags, future-leakage flags, traceability flags, and requested output-role metadata.

Fields outside the current First Module include generalized intake diagnostics, generalized intake limitations, role schema/version metadata, full artifact lineage, context attachment metadata beyond the First Module's source-independent shape, and generalized compatibility states.

A future adapter would own any direct mapping. The First Module's formula, decomposition, contamination visibility, traceability, and scientific interpretation responsibilities remain untouched.

## 38. Determinism results

Repeated identical evaluation produced identical compatibility state, diagnostics, limitations, and `stable_json()`:

```text
INTAKE_COMPATIBLE
True
True
True
3371c5dce2006300df4917392071caf425368af361061c38ef3bf2a7c7708b6a
```

Separate-process serialization probe produced the same hash:

```text
INTAKE_COMPATIBLE
[]
3371c5dce2006300df4917392071caf425368af361061c38ef3bf2a7c7708b6a
```

## 39. Boundary verification

Suspicious-term search over implementation and tests found only documentation-like names, information-role names, refusal flags, metadata field names, and negative assertions. The strict executable prohibited-operation search returned no matches for data retrieval, external dependencies, fitting, prediction, ranking, rolling computation, filling, resampling, winsorization, interpolation, or database/API access.

Information-contract refusal probe:

```text
INTAKE_COMPATIBLE
[('computes_ic', False), ('computes_sharpe', False), ('creates_factor', False), ('creates_model_feature', False), ('creates_model_label', False), ('creates_prediction', False), ('creates_rank', False), ('creates_score', False), ('creates_signal', False), ('creates_validation_result', False), ('exposes_formula_output', False), ('exposes_scientific_result', False), ('makes_production_decision', False)]
```

Guardrail manifest probe returned `synthetic_metadata_only: True` and all prohibited-operation flags as `False`.

## 40. Known limitations

This is a synthetic reference implementation only. It does not create a production registry, live module adapter, real source-role acceptance, source access, real PIT evidence, real context evidence, real comparator evidence, formula execution, empirical testing, validation, production behavior, or ML behavior.

The current Prepared Observations fatal-diagnostic convention uses synthetic `fatal_diagnostics` trace keys; future non-synthetic integration should formalize that schema before real evidence use.

## 41. Implementation-readiness conclusion

Final classification: `SCIENTIFIC_MODULE_INTAKE_REFERENCE_IMPLEMENTATION_COMPLETE`.

The implementation realizes the approved intake design in bounded reference form. It preserves the central separation:

```text
Prepared Observation structural readiness
        !=
Module intake compatibility
        !=
Scientific admissibility
        !=
Scientific support
        !=
Validation success
        !=
Production readiness
```

A package may be structurally ready and still fail module intake because it does not satisfy that module's declared structural requirements. Passing module intake authorizes scientific evaluation only; it does not imply scientific support, predictive value, validation success, production readiness, or machine-learning usefulness.

Verification commands and results:

```text
python -m py_compile pipelines/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
```

Result: passed with no output.

```text
pytest -q tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
```

Result:

```text
...................                                                      [100%]
19 passed in 0.21s
```

```text
pytest -q tests/test_project_underdog_phase5_source_authority_reference_implementation_v1.py tests/test_project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_first_module_reference_implementation_v1.py tests/test_project_underdog_phase5_prepared_observations_reference_implementation_v1.py tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
```

Result:

```text
........................................................................ [ 63%]
..........................................                               [100%]
114 passed in 0.31s
```

Additional searches and checks used:

```text
sed -n '1,1460p' /Users/AnyiXu_1/.codex/attachments/0f5fc73f-8582-492b-a386-ef0396b562e2/pasted-text.txt
rg -n "Scientific Module Intake|Prepared Observation|handoff|intake|structural readiness|module intake|stable serialization|artifact lineage|First Module" docs/research_notes/project_underdog_phase5_prepared_observations_platform_integration_and_scientific_module_intake_design_v1.md
rg -n "class PreparedObservationReadinessState|class InformationRole|class PreparedObservationResult|def evaluate_prepared_observation|def canonical_prepared_observation_fixtures|stable_json|artifact_lineage" pipelines/project_underdog_phase5_prepared_observations_reference_implementation_v1.py
rg -n "FirstModuleInput|MODULE_ID|stable_json|Scientific|result|signal|validation|ML" pipelines/project_underdog_first_module_reference_implementation_v1.py
rg -n "Source Authority|PIT|Comparator|trace|artifact_lineage|reproducibility|frozen|negative|contamination|falsification" docs/research_notes/project_underdog_phase5_prepared_observations_reference_implementation_v1.md docs/research_notes/project_underdog_phase5_prepared_observations_executable_conformance_review_v1.md
rg -n "alpha|signal|factor|rank|score|similarity|formula|return|IC|Sharpe|portfolio|optimize|normalize|winsorize|impute|interpolate|resample|fill|predict|fit|train|model|feature|label|vendor|API|database|SQL|production" pipelines/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
rg -n "(requests|yfinance|sklearn|wrds|sqlite3|sqlalchemy|read_csv\\(|to_csv\\(|urlopen|urllib|httpx|download\\(|RandomForest|KMeans|NearestNeighbors|\\.fit\\(|\\.predict\\(|\\.corr\\(|\\.rank\\(|rolling\\(|fillna\\(|ffill\\(|bfill\\(|resample\\(|winsorize|interpolate)" pipelines/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
rg -n "(acquisition_performed|retrieval_performed|vendor_access_performed|api_access_performed|database_access_performed|authority_evaluation_performed|identity_construction_performed|identity_resolution_performed|context_construction_performed|context_interpretation_performed|comparator_construction_performed|peer_discovery_performed|scientific_similarity_performed|value_transformation_performed|normalization_performed|winsorization_performed|imputation_performed|interpolation_performed|filling_performed|resampling_performed|ranking_performed|scoring_performed|formula_execution_performed|return_calculation_performed|lag_construction_performed|signal_calculation_performed|factor_construction_performed|candidate_generation_performed|panel_construction_performed|ic_calculation_performed|statistical_testing_performed|hypothesis_evaluation_performed|validation_performed|portfolio_construction_performed|optimization_performed|production_decision_performed|ml_feature_created|ml_label_created|model_fit_performed|model_prediction_performed|model_training_performed).*True" pipelines/project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py tests/test_project_underdog_phase5_scientific_module_intake_reference_implementation_v1.py
```

## 42. Exactly one recommended next lifecycle step

`Project Underdog - Phase 5 Scientific Module Intake Executable Conformance Review v1`
