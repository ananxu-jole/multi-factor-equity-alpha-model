# Project Underdog - Phase 5 Comparator Construction Reference Implementation v1

Date: 2026-07-20

## 1. Executive Classification

Final classification: `COMPARATOR_CONSTRUCTION_REFERENCE_IMPLEMENTATION_COMPLETE`

This note records the bounded reference implementation of the Phase 5 Comparator Construction platform layer. The implementation deterministically represents synthetic comparator relationships, target identity applicability references, comparator identity applicability references, eligibility states, temporal applicability, coverage metadata, context-support metadata, exclusions, duplicate exposure, limitations, diagnostics, inherited Source Authority trace, inherited PIT Identity trace, traceability, and a restricted information contract.

The implementation realizes `docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md` without introducing scientific similarity, ranking, peer discovery, measurement, validation, production behavior, optimization, or ML.

## 2. Files Created And Modified

Created:

- `pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py`
- `tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py`
- `docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md`

Modified:

- None.

## 3. Implementation Scope

The implementation is synthetic metadata only. It implements:

- comparator record registration;
- comparator relationship metadata;
- comparator eligibility-state determination;
- target identity applicability reference validation;
- comparator identity applicability reference validation;
- temporal-overlap evaluation;
- context-support metadata;
- coverage metadata;
- exclusion metadata;
- duplicate-exposure metadata;
- limitations;
- deterministic diagnostics;
- Source Authority trace propagation;
- PIT Identity trace propagation;
- comparator traceability packaging;
- information-contract packaging;
- canonical fixtures;
- executable acceptance tests.

It does not implement acquisition, retrieval, vendor integration, APIs, databases, entitlement handling, real security masters, real identity resolution, Source Authority evaluation, PIT Identity construction, scientific similarity, peer discovery, nearest-neighbor logic, clustering, ranking, weighting, contextual measurement, factor construction, formulas, candidate generation, panel generation, discovery, empirical validation, IC, optimization, productionization, or ML.

## 4. Comparator-Model Summary

The implementation defines immutable dataclasses for:

- `IdentityApplicabilityReference`;
- `ComparatorIntervalMetadata`;
- `ComparatorRelationshipMetadata`;
- `ComparatorCoverageMetadata`;
- `ComparatorContextSupportMetadata`;
- `ComparatorConstructionRecord`;
- `ComparatorConstructionResult`;
- `ComparatorInformationContract`;
- `ComparatorConstructionFixture`.

The model records exactly one target side and one comparator side. Each side contains identity id, applicability interval id metadata, interval metadata, and inherited PIT trace metadata. Relationship metadata records relationship id, relationship type, target/comparator identity ids, target/comparator interval ids, relationship support, unresolved/conflicting/excluded flags, self-comparison prohibition, and lineage-unresolved state.

## 5. Eligibility-State Implementation

Implemented approved states:

- `COMPARATOR_ELIGIBLE`
- `COMPARATOR_CONDITIONALLY_ELIGIBLE`
- `COMPARATOR_UNRESOLVED`
- `COMPARATOR_INELIGIBLE`
- `COMPARATOR_EXCLUDED`
- `INSUFFICIENT_COMPARATOR_EVIDENCE`

No additional eligibility states are implemented. Eligibility is based only on supplied synthetic metadata. It is not a statement of economic similarity, quality, rank, peer strength, alpha expectation, validation readiness, or production approval.

## 6. Comparator Relationship Invariant

The implementation enforces:

Every comparator relationship must reference exactly one target identity applicability interval and exactly one comparator identity applicability interval.

Deterministic failure conditions include:

- missing target interval reference;
- missing comparator interval reference;
- multiple target interval references;
- multiple comparator interval references;
- interval reference mismatch;
- declared identity and interval-owner mismatch;
- relationship interval mismatch;
- prohibited self-comparison or duplicate interval exposure.

Violations emit `MISSING_COMPARATOR_APPLICABILITY`, `CONFLICTING_COMPARATOR`, or `DUPLICATE_EXPOSURE_UNRESOLVED` as appropriate and prevent eligible use.

## 7. Temporal-Applicability Implementation

Temporal states:

- `valid_overlap`
- `partial_overlap`
- `no_overlap`
- `unresolved`

Implemented temporal metadata:

- effective start;
- effective end;
- valid overlap;
- no overlap;
- partial overlap;
- open interval;
- unknown interval;
- superseded interval;
- expired interval;
- discontinuity.

Invalid or absent temporal overlap emits `INVALID_TEMPORAL_OVERLAP`. Unknown interval applicability emits `MISSING_COMPARATOR_APPLICABILITY`. Partial, open, superseded, expired, and discontinuous intervals remain limitations rather than inferred validity.

## 8. Coverage And Context-Support Implementation

Coverage is represented through `ComparatorCoverageMetadata`:

- sufficient;
- conditionally governed;
- coverage gap.

Context support is represented through `ComparatorContextSupportMetadata`:

- sufficient;
- conditionally governed;
- context missing.

Insufficient coverage emits `INSUFFICIENT_COMPARATOR_COVERAGE`. Insufficient or missing context emits `COMPARATOR_CONTEXT_INSUFFICIENT`. Conditional coverage and conditional context are preserved as limitations and cannot bypass fatal conditions.

## 9. Exclusion And Duplicate-Exposure Handling

Explicit exclusion is represented by `excluded_relationship` and emits `EXCLUDED_COMPARATOR`. Exclusion has highest final-state precedence and yields `COMPARATOR_EXCLUDED`.

Duplicate exposure is represented by `duplicate_exposure` or prohibited self-comparison through the same interval on both sides. It emits `DUPLICATE_EXPOSURE_UNRESOLVED` and yields `COMPARATOR_INELIGIBLE`.

The implementation does not deduplicate, merge, rank, prioritize, or choose among relationships.

## 10. Diagnostic Implementation

Implemented exact design diagnostics:

- `UNRESOLVED_COMPARATOR`
- `CONFLICTING_COMPARATOR`
- `MISSING_COMPARATOR_APPLICABILITY`
- `INVALID_TEMPORAL_OVERLAP`
- `INSUFFICIENT_COMPARATOR_COVERAGE`
- `UNSUPPORTED_COMPARATOR_RELATIONSHIP`
- `EXCLUDED_COMPARATOR`
- `INCOMPLETE_COMPARATOR_TRACEABILITY`
- `UNRESOLVED_COMPARATOR_LINEAGE`
- `DUPLICATE_EXPOSURE_UNRESOLVED`
- `COMPARATOR_CONTEXT_INSUFFICIENT`

Diagnostics are emitted in deterministic evaluator order and describe metadata conditions only. They do not repair metadata or infer comparator eligibility.

## 11. Decision-Precedence Implementation

Final-state precedence:

1. `EXCLUDED_COMPARATOR` -> `COMPARATOR_EXCLUDED`
2. fatal ineligibility diagnostics -> `COMPARATOR_INELIGIBLE`
3. missing applicability, unresolved lineage, insufficient coverage, or insufficient context -> `INSUFFICIENT_COMPARATOR_EVIDENCE`
4. unresolved relationship -> `COMPARATOR_UNRESOLVED`
5. limitations without diagnostics -> `COMPARATOR_CONDITIONALLY_ELIGIBLE`
6. no diagnostics or limitations -> `COMPARATOR_ELIGIBLE`

Fatal conditions cannot be masked by conditional coverage, conditional context, partial overlap, open intervals, supersession, expiration, or other limitations. Diagnostics are collected before final state assignment, so combined failures preserve all applicable diagnostics.

## 12. Information Contract

The information contract exposes only:

- comparator relationship metadata;
- target applicability metadata;
- comparator applicability metadata;
- eligibility state;
- temporal applicability metadata;
- coverage metadata;
- context-support metadata;
- limitations;
- diagnostics;
- Source Authority trace;
- PIT Identity trace;
- comparator traceability metadata.

It explicitly refuses raw source values, retrieval instructions, authority evaluation, real identity construction, identity resolution, comparator ranking, similarity scores, peer discovery, contextual measurements, formulas, scientific interpretations, candidate generation, panel construction, IC, validation outcomes, production decisions, ML features, and ML labels.

## 13. Source Authority Trace Propagation

Source Authority trace metadata is carried in `source_authority_trace` and passed into traceability and the information contract. The implementation does not call or re-evaluate Source Authority when evaluating comparator eligibility.

## 14. PIT Identity Trace Propagation

PIT Identity trace metadata is carried in identity applicability references and in the top-level `pit_identity_trace`. It is passed into comparator traceability and the information contract. The implementation does not construct PIT identity, repair identity intervals, or reinterpret context.

## 15. Traceability Implementation

Traceability includes:

- target identity id;
- target interval id;
- comparator identity id;
- comparator interval id;
- relationship id;
- relationship type;
- temporal applicability state;
- Source Authority trace;
- PIT Identity trace;
- fixture id;
- governing design id;
- layer name.

Repeated identical metadata produces identical traceability and stable serialization.

## 16. Synthetic Fixture Coverage

The canonical fixture set contains 20 fixtures:

- `CC1_eligible`
- `CC2_conditionally_eligible`
- `CC3_unresolved`
- `CC4_ineligible`
- `CC5_excluded`
- `CC6_insufficient_evidence`
- `CC7_missing_target_interval`
- `CC8_missing_comparator_interval`
- `CC9_identity_interval_mismatch`
- `CC10_valid_temporal_overlap`
- `CC11_invalid_temporal_overlap`
- `CC12_partial_overlap`
- `CC13_superseded_interval`
- `CC14_expired_interval`
- `CC15_unresolved_lineage`
- `CC16_insufficient_coverage`
- `CC17_insufficient_context`
- `CC18_duplicate_exposure`
- `CC19_conflicting_relationship`
- `CC20_incomplete_traceability`

Acceptance tests additionally cover combined failures: conditional coverage plus invalid temporal overlap, conditional context plus excluded comparator, duplicate exposure plus incomplete traceability, unresolved lineage plus insufficient coverage, conflicting relationship plus missing applicability, and superseded interval plus otherwise eligible relationship.

## 17. Acceptance-Test Results

Comparator-specific suite:

```text
pytest -q tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
20 passed in 0.06s
```

Combined Source Authority, PIT Identity and Context Evidence, First Module, and Comparator suite:

```text
pytest -q tests/test_project_underdog_phase5_source_authority_reference_implementation_v1.py tests/test_project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1.py tests/test_project_underdog_first_module_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
75 passed in 0.07s
```

## 18. Determinism Verification

Repeated execution for `CC19_conflicting_relationship` produced:

```text
True
True
COMPARATOR_INELIGIBLE
['CONFLICTING_COMPARATOR']
```

Diagnostic-ordering probe for duplicate exposure plus incomplete traceability produced:

```text
['DUPLICATE_EXPOSURE_UNRESOLVED', 'INCOMPLETE_COMPARATOR_TRACEABILITY']
```

No hidden timestamps, random values, environment-dependent values, external data, or unordered serialized sets are used.

## 19. Compatibility Verification

Compatibility checks passed with:

- Source Authority reference implementation;
- PIT Identity and Context Evidence reference implementation;
- completed First Module reference implementation.

Source Authority and PIT traces are propagated without re-evaluation. The First Module boundary remains intact: Comparator Construction does not execute formulas or create prepared observations.

## 20. Scope-Boundary Verification

The guardrail manifest reports `synthetic_metadata_only: True` and false for acquisition, retrieval, vendor integration, authority evaluation, identity construction, identity resolution, scientific similarity, comparator ranking, peer discovery, contextual measurement, formula execution, candidate generation, panel generation, discovery, validation, IC computation, production logic, optimization, and ML integration.

Static syntax checks passed:

```text
python -m py_compile pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
```

Prohibited-scope searches found no external-access imports and no true-valued prohibited-operation flags. One search matched expected false refusal fields containing `similarity`; those are boundary-preservation fields, not similarity implementation.

## 21. Known Limitations

This is a reference implementation only. It uses synthetic metadata and has no real securities, vendors, APIs, databases, entitlements, source records, security masters, identity construction, contextual values, comparator algorithms, peer discovery, rankings, weights, similarity scores, formulas, candidates, panels, empirical tests, validation, production logic, optimization, or ML.

It proves deterministic metadata representation and boundary preservation, not scientific comparator quality or production readiness.

## 22. Implementation Readiness Conclusion

Final classification: `COMPARATOR_CONSTRUCTION_REFERENCE_IMPLEMENTATION_COMPLETE`

The Phase 5 Comparator Construction reference implementation is complete within its approved scope. It deterministically evaluates synthetic comparator relationship metadata, enforces the interval-pairing invariant, preserves temporal applicability, emits deterministic diagnostics, applies fail-closed precedence, propagates inherited traces, packages a restricted information contract, and remains compatible with completed upstream and downstream reference components.

No implementation beyond the approved synthetic metadata reference boundary is authorized by this note.

## 23. Exactly One Recommended Next Lifecycle Step

Recommended next lifecycle step:

`Project Underdog - Phase 5 Comparator Construction Executable Conformance Review v1`

This step should independently review the completed reference implementation against the approved comparator construction design, fixture coverage, acceptance tests, Source Authority compatibility, PIT Identity compatibility, First Module compatibility, determinism, traceability, and information-contract restrictions. It must not introduce acquisition, retrieval, authority evaluation, real identity construction, scientific similarity, ranking, peer discovery, contextual measurement, formulas, discovery, validation, production logic, optimization, or ML.

## Verification Commands Executed

```text
sed -n '1,260p' /Users/AnyiXu_1/.codex/attachments/a0eadfea-b0fe-435c-9549-f165065d2062/pasted-text.txt
sed -n '261,620p' /Users/AnyiXu_1/.codex/attachments/a0eadfea-b0fe-435c-9549-f165065d2062/pasted-text.txt
sed -n '1,220p' pipelines/project_underdog_phase5_source_authority_reference_implementation_v1.py
sed -n '1,260p' pipelines/project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1.py
sed -n '1,220p' pipelines/project_underdog_first_module_reference_implementation_v1.py
sed -n '1,220p' docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
pytest -q tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
pytest -q tests/test_project_underdog_phase5_source_authority_reference_implementation_v1.py tests/test_project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1.py tests/test_project_underdog_first_module_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
python -m py_compile pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
python -c "<repeated deterministic execution probe>"
python -c "<targeted combined-failure probe>"
python -c "<information-contract refusal probe>"
python -c "<diagnostic-ordering probe>"
rg -n "import (requests|yfinance|sklearn|wrds|sqlite3|sqlalchemy)|read_csv\\(|to_csv\\(|urlopen|urllib|httpx|download\\(|RandomForest|KMeans|NearestNeighbors|fit\\(|predict\\(|corr\\(|rank\\(|similarity|cosine" pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
rg -n "(acquisition_performed|retrieval_performed|vendor_integration|authority_evaluation_performed|identity_construction|identity_resolution|scientific_similarity|comparator_ranking|peer_discovery|contextual_measurement|formula_execution|candidate_generation|panel_generation|discovery_execution|validation_execution|ic_computation|production_logic|optimization_performed|ml_integration): bool = True|\\\"(acquisition_performed|retrieval_performed|vendor_integration|authority_evaluation|identity_construction|identity_resolution|scientific_similarity|comparator_ranking|peer_discovery|contextual_measurement|formula_execution|candidate_generation|panel_generation|discovery_execution|validation_execution|ic_computation|production_logic|optimization_performed|ml_integration)\\\": True" pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
git diff --check -- pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py
git diff --check -- pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md
rg -n "import (requests|yfinance|sklearn|wrds|sqlite3|sqlalchemy)|read_csv\\(|to_csv\\(|urlopen|urllib|httpx|download\\(|RandomForest|KMeans|NearestNeighbors|fit\\(|predict\\(|corr\\(|rank\\(|cosine" pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md
rg -n "(acquisition_performed|retrieval_performed|vendor_integration|authority_evaluation_performed|identity_construction|identity_resolution|scientific_similarity|comparator_ranking|peer_discovery|contextual_measurement|formula_execution|candidate_generation|panel_generation|discovery_execution|validation_execution|ic_computation|production_logic|optimization_performed|ml_integration): bool = True|\\\"(acquisition_performed|retrieval_performed|vendor_integration|authority_evaluation|identity_construction|identity_resolution|scientific_similarity|comparator_ranking|peer_discovery|contextual_measurement|formula_execution|candidate_generation|panel_generation|discovery_execution|validation_execution|ic_computation|production_logic|optimization_performed|ml_integration)\\\": True" pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md
git status --short pipelines/project_underdog_phase5_comparator_construction_reference_implementation_v1.py tests/test_project_underdog_phase5_comparator_construction_reference_implementation_v1.py docs/research_notes/project_underdog_phase5_comparator_construction_reference_implementation_v1.md
```
