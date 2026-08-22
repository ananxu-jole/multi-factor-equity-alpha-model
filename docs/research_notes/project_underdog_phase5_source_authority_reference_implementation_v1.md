# Project Underdog - Phase 5 Source Authority Reference Implementation v1

Date: 2026-07-18

## 1. Executive Classification

Final classification: `SOURCE_AUTHORITY_REFERENCE_IMPLEMENTATION_COMPLETE`

This note documents the bounded reference implementation of:

`Project Underdog - Phase 5 Source Authority Reference Implementation v1`

The implementation realizes `docs/research_notes/project_underdog_phase5_source_authority_implementation_design_v1.md` as deterministic, source-independent code that evaluates synthetic authority metadata only. It does not retrieve data, contact vendors, connect APIs, select sources, perform acquisition, construct identities, construct comparator sets, measure context, execute formulas, create candidates, generate panels, compute IC, run discovery, run validation, create production logic, optimize, or introduce ML.

Authoritative foundation preserved:

- `docs/research_notes/project_underdog_phase5_source_authority_implementation_design_v1.md`
- `docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md`
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`
- `docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md`
- `docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`
- `docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md`

## 2. Files Created

Created implementation file:

- `pipelines/project_underdog_phase5_source_authority_reference_implementation_v1.py`

Created test file:

- `tests/test_project_underdog_phase5_source_authority_reference_implementation_v1.py`

Created documentation file:

- `docs/research_notes/project_underdog_phase5_source_authority_reference_implementation_v1.md`

Modified existing files:

- None.

## 3. Implementation Scope

Implemented:

- source registration records;
- authority evaluation;
- authority-state determination;
- provenance metadata representation;
- temporal-guarantee metadata representation;
- authority diagnostics;
- role authorization;
- traceability packaging;
- information-contract packaging;
- canonical synthetic authority fixtures;
- executable acceptance tests.

Not implemented:

- external source retrieval;
- vendor APIs or connectors;
- acquisition or downloads;
- source selection or ranking;
- identity construction;
- ticker-lineage construction;
- company-security mapping;
- comparator or peer construction;
- contextual measurement;
- formula execution;
- scientific module execution;
- candidate, registry, panel, IC, validation, production, optimization, or ML behavior.

## 4. Authority Implementation Summary

The implementation centers on `evaluate_source_authority(record)`, which accepts a prepared `SourceAuthorityRecord` and returns a deterministic `SourceAuthorityResult`.

The evaluator checks, in order:

1. contract conformance;
2. source registration and synthetic-record boundary;
3. role scope;
4. provenance completeness;
5. temporal guarantee sufficiency;
6. authority conflict status;
7. evidence strength;
8. unresolved authority status;
9. coverage sufficiency or governed conditional limitation;
10. revision reconstructability;
11. reproducibility sufficiency;
12. diagnostic-only scope;
13. traceability completeness;
14. unconditional or conditional authority state.

The implementation uses only supplied metadata flags and descriptors. No evaluation step reads external files, contacts networks, queries sources, inspects data samples, infers values, or resolves missing authority through defaults.

## 5. Authority-State Implementation

Implemented authority states:

- `AUTHORITATIVE_FOR_DEFINED_ROLE`
- `CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE`
- `DIAGNOSTIC_ONLY`
- `INSUFFICIENT_EVIDENCE`
- `REJECTED_FOR_DEFINED_ROLE`

State behavior:

| State | Implementation condition |
|---|---|
| `AUTHORITATIVE_FOR_DEFINED_ROLE` | All required registration, provenance, temporal, evidence, coverage, revision, reproducibility, and traceability gates pass with no limitations. |
| `CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE` | Core authority gates pass but explicit limitations or governed coverage conditions must be preserved. |
| `DIAGNOSTIC_ONLY` | Evidence is explicitly unsupported for authority or scoped to diagnostic use. |
| `INSUFFICIENT_EVIDENCE` | Required evidence, provenance, temporal guarantee, conflict resolution, coverage, or reproducibility support is missing. |
| `REJECTED_FOR_DEFINED_ROLE` | Source is unauthorized, role scope is violated, revisions are unreconstructable, traceability is incomplete, or the implementation contract is mismatched. |

No additional authority classifications were introduced.

## 6. Diagnostic Implementation

Implemented diagnostics:

- `UNAUTHORIZED_SOURCE`
- `INSUFFICIENT_AUTHORITY`
- `CONFLICTING_AUTHORITY`
- `MISSING_PROVENANCE`
- `MISSING_TEMPORAL_GUARANTEE`
- `UNSUPPORTED_EVIDENCE`
- `UNRESOLVED_AUTHORITY`
- `ROLE_SCOPE_VIOLATION`
- `COVERAGE_INSUFFICIENT`
- `REVISION_UNRECONSTRUCTABLE`
- `REPRODUCIBILITY_INSUFFICIENT`
- `TRACEABILITY_INCOMPLETE`
- `CONTRACT_MISMATCH`

The first eleven diagnostics correspond to the approved implementation design. `TRACEABILITY_INCOMPLETE` and `CONTRACT_MISMATCH` are implementation guardrail diagnostics required to preserve traceability and frozen-design conformance. They do not expand scientific authority.

Diagnostics are deterministic and explanatory only. They do not repair metadata, choose sources, infer roles, construct identities, build peers, run formulas, validate hypotheses, or produce production decisions.

## 7. Provenance Implementation

`ProvenanceMetadata` represents:

- origin;
- source version;
- publication identity;
- evidence references;
- lineage reference;
- acquisition identity as a synthetic controlled reference only;
- retention status.

Provenance is complete only when origin, source version, publication identity, evidence references, and lineage reference are present. Missing provenance fails closed to `INSUFFICIENT_EVIDENCE` with `MISSING_PROVENANCE`.

## 8. Temporal Guarantee Implementation

`TemporalGuaranteeMetadata` represents:

- effective-date support;
- publication or availability support;
- revision-date support;
- snapshot or project-known support;
- historical reconstruction support;
- temporal scope;
- optional uncertainty interval;
- optional conservative delay rule descriptor.

Temporal guarantees are sufficient only when all required PIT support flags are true and temporal scope is present. Missing temporal support fails closed to `INSUFFICIENT_EVIDENCE` with `MISSING_TEMPORAL_GUARANTEE`.

The implementation does not construct PIT identity, infer missing dates, calculate known-date rules, or create historical records.

## 9. Information Contract

The implementation exposes only:

- authority state;
- supported roles;
- unsupported roles;
- provenance metadata;
- temporal guarantee metadata;
- limitations;
- diagnostics;
- traceability.

The implementation explicitly refuses:

- raw values;
- retrieval;
- queries;
- identity construction;
- peer construction;
- formulas;
- candidates;
- panels;
- IC;
- validation;
- production decisions;
- ML inputs.

These refusals are represented by false flags in `InformationContract` and `SourceAuthorityResult`, and are checked by tests.

## 10. Synthetic Fixture Coverage

Canonical fixtures:

| Fixture | Purpose | Expected state |
|---|---|---|
| `SA1_authoritative` | Fully authoritative synthetic source-role. | `AUTHORITATIVE_FOR_DEFINED_ROLE` |
| `SA2_conditional` | Authority with explicit limitation. | `CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE` |
| `SA3_diagnostic_only` | Diagnostic-only source-role. | `DIAGNOSTIC_ONLY` |
| `SA4_rejected` | Rejected source-role due to unreconstructable revision history. | `REJECTED_FOR_DEFINED_ROLE` |
| `SA5_insufficient_evidence` | Missing required evidence strength. | `INSUFFICIENT_EVIDENCE` |
| `SA6_conflict` | Conflicting authority. | `INSUFFICIENT_EVIDENCE` |
| `SA7_missing_provenance` | Missing provenance. | `INSUFFICIENT_EVIDENCE` |
| `SA8_missing_temporal` | Missing temporal guarantee. | `INSUFFICIENT_EVIDENCE` |
| `SA9_role_scope_violation` | Requested role outside registered role scope. | `REJECTED_FOR_DEFINED_ROLE` |
| `SA10_unreconstructable_revision` | Unreconstructable revision history. | `REJECTED_FOR_DEFINED_ROLE` |
| `SA11_insufficient_reproducibility` | Insufficient reproducibility. | `INSUFFICIENT_EVIDENCE` |

Each fixture uses synthetic metadata only.

## 11. Acceptance-Test Results

Executed:

`pytest -q tests/test_project_underdog_phase5_source_authority_reference_implementation_v1.py`

Result:

`15 passed in 0.03s`

Acceptance tests verify:

- canonical fixture state correctness;
- diagnostic correctness;
- role authorization;
- provenance fail-closed behavior;
- temporal guarantee fail-closed behavior;
- role-scope rejection;
- non-synthetic source rejection;
- information-contract refusals;
- boundary flags;
- traceability completeness;
- deterministic repeated execution and serialization;
- frozen contract mismatch rejection;
- guardrail manifest.

## 12. Determinism Verification

Determinism is verified by `test_deterministic_repeated_execution_and_serialization`.

The test confirms that repeated evaluation of the same synthetic authority record produces identical:

- result dataclass;
- authority state;
- diagnostics;
- supported roles;
- limitations;
- ordered dictionary;
- stable JSON serialization.

The implementation contains no random number generation, current-time access, external calls, filesystem reads, network calls, database access, model fitting, or hash-order-dependent output.

## 13. Scope-Boundary Verification

Boundary flags in the result and information contract remain false for all fixtures:

- external retrieval;
- vendor integration;
- acquisition;
- identity construction;
- comparator construction;
- contextual measurement;
- formula execution;
- discovery execution;
- validation execution;
- production logic;
- optimization;
- ML integration.

The guardrail manifest also records:

- `source_independent: True`
- `synthetic_records_only: True`
- all prohibited operational, research, production, and ML paths as `False`.

## 14. Known Limitations

- The implementation evaluates synthetic authority records only.
- No real source, vendor, data product, documentation package, entitlement, license, table, field, or sample is evaluated.
- No source becomes authoritative because this implementation exists.
- The evaluator is intentionally conservative and fail-closed.
- It does not implement databases, schemas, connectors, source-specific evidence stores, retention infrastructure, or production authority services.
- It does not construct PIT identity, historical context, comparator memberships, formulas, candidates, panels, IC, validation, production artifacts, or ML inputs.
- Additional conformance review should independently compare this executable implementation to the design before it becomes a reusable upstream contract for later reference implementations.

## 15. Readiness Conclusion

Final classification: `SOURCE_AUTHORITY_REFERENCE_IMPLEMENTATION_COMPLETE`

The bounded Source Authority reference implementation is complete and verified against synthetic authority fixtures. It proves that Project Underdog can evaluate source authority as a deterministic, source-independent governance layer using metadata alone.

This conclusion does not authorize real source acceptance, acquisition, retrieval, identity construction, context construction, comparator construction, formulas, discovery, validation, production, optimization, or ML.

## 16. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - Phase 5 Source Authority Executable Conformance Review v1`

Rationale:

The Source Authority reference implementation now exists and passes executable tests. The smallest justified next step is an independent conformance review against the frozen Source Authority implementation design, similar to the first-module executable conformance review. This should verify that the implementation realizes every approved behavior and only approved behavior before any later PIT Identity, Context Evidence, or Comparator Construction reference implementation depends on it.
