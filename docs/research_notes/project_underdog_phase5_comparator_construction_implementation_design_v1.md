# Project Underdog - Phase 5 Comparator Construction Implementation Design v1

Date: 2026-07-20

## 1. Executive Classification

Final classification: `COMPARATOR_CONSTRUCTION_IMPLEMENTATION_DESIGN_DEFINED`

This note defines the implementation architecture for the Project Underdog Phase 5 Comparator Construction platform layer. The layer sits after Source Authority and PIT Identity and Context Evidence, and before Prepared Observations and scientific modules. Its purpose is to deterministically represent comparator relationships from already-authorized, already-identified, and already-time-qualified metadata.

This is an implementation-design document only. It does not implement code, retrieve data, define vendors, define APIs, define databases, construct real identities, interpret context, define scientific similarity, rank entities, score entities, define measurements, define formulas, generate candidates, run validation, define production architecture, optimize, or introduce ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_source_authority_executable_conformance_rereview_v1.md`: final classification `SOURCE_AUTHORITY_IMPLEMENTATION_FULLY_CONFORMANT`; Source Authority can provide upstream source-role trust metadata.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_executable_conformance_review_v1.md`: final classification `PIT_IDENTITY_AND_CONTEXT_EVIDENCE_IMPLEMENTATION_CONFORMANT_WITH_MINOR_OBSERVATIONS`; PIT Identity and Context Evidence can provide upstream identity, temporal, context-applicability, diagnostic, and traceability metadata.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1.md`: Comparator Construction must still perform its own eligibility, membership, missingness, duplicate exposure, fallback, and peer-count responsibilities.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: comparator or benchmark information is a distinct information role and must not be treated as alpha merely because a benchmark exists.
- `docs/research_notes/project_underdog_first_module_implementation_architecture_specification_v1.md`: scientific modules must receive prepared observations and must not construct comparator sets inside formula logic.
- Platform v2, artifact-lineage, reproducibility, contamination, and falsification governance remain authoritative.

## 2. Purpose

Comparator Construction determines whether a target identity and another identity may be represented as a comparator relationship for a defined role, interval, and metadata context.

It answers:

- Which target identity interval is being evaluated?
- Which comparator identity interval is being evaluated?
- Which context-applicability evidence supports the relationship?
- During what temporal interval is the comparator relationship applicable?
- Is the relationship eligible, ineligible, unresolved, excluded, conflicting, or limited?
- What coverage, limitations, diagnostics, and traceability must be preserved?
- What information contract can be safely passed to Prepared Observations or later scientific modules?

It does not answer:

- Is the source authoritative?
- Is the identity true?
- What is the raw context value?
- Are the entities scientifically similar?
- Which comparator is best?
- What measurement should be computed?
- What formula should use the comparator?
- Whether the comparator relationship has alpha value.

## 3. Platform Position

Conceptual flow:

```text
External Information
        |
        v
Source Authority
        |
        v
PIT Identity & Context Evidence
        |
        v
Comparator Construction
        |
        v
Prepared Observations
        |
        v
Scientific Modules
```

Comparator Construction assumes:

- Source Authority has already established role-specific trust metadata.
- PIT Identity and Context Evidence has already established identity applicability and context applicability metadata.
- Comparator Construction consumes those outputs and does not repeat those responsibilities.

Downstream layers must still perform their own responsibilities. Prepared Observations must package observations separately. Scientific modules must consume prepared observations and must not infer comparator validity from ungoverned metadata.

## 4. Comparator Philosophy

Comparator Construction represents relationships.

It does not determine scientific similarity. It does not rank entities. It does not score entities. It does not measure alpha. It does not choose the best comparator or optimize membership.

A comparator relationship is a governed metadata object stating that a target identity interval and comparator identity interval are eligible, conditionally eligible, unresolved, or excluded for a defined comparator role over a defined interval.

Comparator validity is therefore not the same as:

- economic similarity;
- correlation;
- peer quality;
- relative strength;
- alpha usefulness;
- formula input readiness;
- candidate readiness;
- validation readiness;
- production readiness.

Comparator Construction must preserve uncertainty rather than converting unresolved metadata into usable relationships.

## 5. Architecture Overview

Major conceptual components:

| Component | Primary responsibility |
|---|---|
| Upstream Intake Boundary | Accept only Source Authority trace and PIT Identity and Context Evidence applicability metadata. |
| Comparator Registration Layer | Register target and comparator metadata as a proposed relationship object. |
| Eligibility Layer | Represent eligible, conditionally eligible, unresolved, ineligible, or excluded comparator states. |
| Relationship Layer | Represent target-comparator relationship role, direction, lineage, and context basis. |
| Temporal Applicability Layer | Represent overlap, non-overlap, open interval, discontinuity, supersession, expiration, and unresolved applicability. |
| Coverage And Limitation Layer | Preserve missing comparator coverage, incomplete coverage, duplicate exposure limits, sparse support, and governed exclusions. |
| Diagnostics Layer | Emit deterministic diagnostics for comparator metadata failures. |
| Traceability Layer | Preserve target, comparator, context, source authority, PIT identity, interval, diagnostic, limitation, and design lineage. |
| Information Contract Layer | Expose only comparator metadata, eligibility metadata, diagnostics, limitations, and traceability. |

This is a conceptual architecture. It does not define classes, APIs, schemas, source queries, storage tables, selection algorithms, scoring models, formulas, or validation logic.

## 6. Comparator Responsibilities

| Responsibility | Purpose | Inputs | Outputs | Dependencies | Prohibited responsibilities |
|---|---|---|---|---|---|
| Comparator registration | Record a proposed target-comparator relationship. | Accepted PIT identity/context metadata for target and comparator. | Comparator relationship metadata or diagnostic. | PIT Identity and Context Evidence. | Real peer discovery, source retrieval, identity resolution. |
| Comparator eligibility representation | Represent whether a relationship is eligible, conditional, unresolved, ineligible, or excluded. | Identity applicability, context applicability, coverage, relationship support. | Eligibility metadata and limitations. | Source Authority and PIT traces. | Scientific similarity scoring or ranking. |
| Comparator relationship representation | Preserve target, comparator, role, relationship direction, lineage, and context basis. | Target and comparator metadata. | Relationship metadata. | Information role definitions. | Selecting best comparator or optimizing groups. |
| Temporal comparator applicability | Represent when comparator relationship is applicable. | Identity intervals, context intervals, comparator interval metadata. | Comparator applicability interval and diagnostics. | PIT temporal metadata. | Inferring missing dates or constructing PIT panels. |
| Comparator coverage representation | Preserve sufficient, insufficient, partial, missing, or duplicate coverage metadata. | Coverage metadata from upstream identity/context and comparator relationship. | Coverage metadata and restrictions. | Reproducibility and contamination governance. | Imputation or fallback peer grouping. |
| Comparator limitations | Communicate bounded use and restrictions. | Conditional states, sparse support, open intervals, supersession, duplication. | Limitation metadata. | Platform v2 fail-closed discipline. | Alpha interpretation or formula decisions. |
| Comparator diagnostics | Explain metadata failures. | Comparator, interval, coverage, traceability, and relationship states. | Stable diagnostic codes and messages. | Platform v2 diagnostics discipline. | Silent repair or unsupported overrides. |
| Comparator traceability | Preserve why relationship was or was not eligible. | Source Authority trace, PIT trace, identity/context metadata, diagnostics. | Traceability package. | Artifact lineage and reproducibility. | Decorative trace without decision lineage. |
| Comparator information contract | Bound downstream outputs to approved metadata. | Relationship metadata, diagnostics, limitations, traceability. | Restricted contract. | Integrated information inventory. | Raw values, formulas, candidates, validation, production, ML. |

## 7. Comparator Model

Conceptual comparator representations:

| Concept | Design meaning |
|---|---|
| Comparator candidate | A proposed comparator relationship object built from accepted metadata. Candidate here means relationship candidate only, not an alpha candidate. |
| Eligible comparator | A comparator relationship whose metadata satisfies identity, context, temporal, coverage, relationship, and traceability gates for the defined role. |
| Conditionally eligible comparator | A comparator relationship with explicit limitations that downstream layers must preserve. |
| Ineligible comparator | A comparator relationship that fails role, interval, coverage, or relationship conditions. |
| Unresolved comparator | A comparator relationship that cannot be safely accepted or rejected because required metadata is ambiguous or incomplete. |
| Excluded comparator | A comparator relationship explicitly excluded by metadata, coverage, duplicate exposure, terminal state, or governed restriction. |
| Comparator relationship | A metadata object linking target identity applicability to comparator identity applicability for a defined role and interval. |
| Comparator lineage | Relationship lineage preserving why the comparator relationship exists, changes, expires, or is superseded. |
| Comparator applicability interval | The interval over which the comparator relationship may be considered applicable. |
| Synthetic comparator record | A non-real relationship object used only for future reference implementation fixtures and acceptance tests. |

The design must not define algorithms for selecting the best comparator. It must not optimize membership, weights, ranks, or thresholds.

## 8. Comparator Eligibility Model

Comparator eligibility is metadata-only.

Minimum eligibility inputs:

- target identity applicability is accepted or conditionally accepted for the role;
- comparator identity applicability is accepted or conditionally accepted for the role;
- target and comparator context applicability are valid for the intended comparator role;
- target and comparator intervals overlap as required by the comparator role;
- comparator relationship support is explicit and traceable;
- coverage is sufficient or conditionally governed;
- duplicate exposure, share-class overlap, or same-economic-entity overlap is either absent or explicitly governed;
- relationship conflicts are absent or governed;
- Source Authority and PIT Identity traces are present;
- comparator traceability is complete.

Conceptual eligibility states:

- `COMPARATOR_ELIGIBLE`
- `COMPARATOR_CONDITIONALLY_ELIGIBLE`
- `COMPARATOR_UNRESOLVED`
- `COMPARATOR_INELIGIBLE`
- `COMPARATOR_EXCLUDED`
- `INSUFFICIENT_COMPARATOR_EVIDENCE`

Eligibility must not be derived from return behavior, correlation, performance, rank, similarity score, formula result, or validation outcome.

## 9. Temporal Applicability Model

Comparator temporal applicability represents whether target and comparator relationship metadata overlap safely for the intended interval.

Required temporal concepts:

| Temporal concept | Design meaning | Required behavior |
|---|---|---|
| Comparator applicability interval | Interval over which the relationship may be used as comparator metadata. | Preserve start and end metadata. |
| Target identity interval | Target applicability interval inherited from PIT Identity and Context Evidence. | Must remain traceable. |
| Comparator identity interval | Comparator applicability interval inherited from PIT Identity and Context Evidence. | Must remain traceable. |
| Context applicability interval | Context interval supporting relationship role. | Must remain separate from relationship interval. |
| Overlap | Required temporal intersection exists. | Represent explicitly; no formula use implied. |
| Non-overlap | Required temporal intersection is absent. | Emit diagnostic and mark unresolved or ineligible. |
| Open interval | Start known, end unknown. | Conditional at most; downstream must preserve limitation. |
| Unknown interval | Required interval boundary is unknown. | Unresolved; do not infer. |
| Discontinuity | Relationship applicability has a gap. | Preserve gap and limitation. |
| Supersession | Relationship or context is replaced. | Preserve lineage; do not silently merge. |
| Expiration | Relationship no longer applies after an end condition. | Preserve terminal relationship metadata. |
| Unresolved applicability | Timing cannot be safely established. | Emit diagnostic and block eligible use. |

This layer does not construct historical panels, infer missing dates, choose observation windows, or execute PIT logic beyond metadata applicability checks.

## 10. Diagnostic Model

Deterministic diagnostic categories:

| Diagnostic | Meaning | Required behavior |
|---|---|---|
| `UNRESOLVED_COMPARATOR` | Comparator relationship cannot be safely established. | Block eligible downstream use. |
| `CONFLICTING_COMPARATOR` | Relationship metadata conflicts across target, comparator, context, or role. | Preserve conflict and mark unresolved or excluded. |
| `MISSING_COMPARATOR_APPLICABILITY` | Required comparator interval or relationship metadata is absent. | Unresolved; do not infer. |
| `INVALID_TEMPORAL_OVERLAP` | Target, comparator, or context intervals do not overlap as required. | Fail closed or mark ineligible. |
| `INSUFFICIENT_COMPARATOR_COVERAGE` | Coverage is too incomplete for the defined relationship role. | Preserve missingness and restrictions. |
| `UNSUPPORTED_COMPARATOR_RELATIONSHIP` | Relationship is asserted without sufficient metadata support. | Block eligibility. |
| `EXCLUDED_COMPARATOR` | Comparator is explicitly excluded by governed metadata. | Preserve exclusion and prevent eligible use. |
| `INCOMPLETE_COMPARATOR_TRACEABILITY` | Relationship lacks source, PIT, interval, or design traceability. | Reject or mark ineligible for authoritative downstream use. |
| `UNRESOLVED_COMPARATOR_LINEAGE` | Relationship continuity, replacement, or supersession is unresolved. | Block continuous relationship use. |
| `DUPLICATE_EXPOSURE_UNRESOLVED` | Same economic exposure, share-class duplication, or self-comparison cannot be governed. | Exclude or unresolved. |
| `COMPARATOR_CONTEXT_INSUFFICIENT` | Context applicability exists but is insufficient for comparator role. | Unresolved; do not substitute fallback. |

Diagnostics describe metadata conditions only. They do not correct identity, interpret context, rank comparators, measure repair, execute formulas, create candidates, or validate hypotheses.

## 11. Information Contract

Approved downstream outputs:

- comparator relationship metadata;
- comparator applicability metadata;
- eligibility metadata;
- coverage metadata;
- limitations;
- diagnostics;
- Source Authority trace;
- PIT Identity and Context Evidence trace;
- comparator traceability metadata;
- governing design version;
- reproducibility or artifact-lineage reference where available.

The contract must refuse:

- raw source values;
- retrieval instructions;
- authority evaluation;
- identity construction or identity-resolution results;
- contextual interpretation;
- context measurements;
- formulas;
- rankings;
- similarity scores;
- optimized weights;
- alpha claims;
- scientific interpretations;
- candidates;
- panels;
- IC;
- validation outcomes;
- production decisions;
- ML inputs.

Downstream limitations must remain explicit:

- unresolved comparator;
- missing comparator applicability;
- invalid temporal overlap;
- insufficient coverage;
- duplicate exposure;
- excluded relationship;
- open interval;
- superseded relationship;
- discontinuity;
- unresolved lineage;
- incomplete traceability;
- conditional eligibility.

## 12. Traceability Model

Traceability must be sufficient to reconstruct:

- evaluated target identity;
- evaluated comparator identity;
- target identity applicability interval;
- comparator identity applicability interval;
- target context applicability metadata;
- comparator context applicability metadata;
- comparator relationship role;
- comparator applicability interval;
- comparator lineage, replacement, or supersession metadata;
- inherited Source Authority trace;
- inherited PIT Identity and Context Evidence trace;
- coverage metadata;
- limitations;
- diagnostics;
- eligibility state;
- governing implementation-design version;
- fixture id if synthetic;
- reproducibility or controlled-reference handle where applicable.

Traceability is mandatory. A comparator relationship without complete traceability must not become eligible for authoritative downstream use.

## 13. Compatibility Assessment

Source Authority:

Comparator Construction consumes Source Authority trace and authority-state metadata only through upstream PIT Identity and Context Evidence outputs. It does not re-evaluate source authority, inspect raw sources, choose vendors, or create source-role trust.

PIT Identity and Context Evidence:

Comparator Construction consumes identity applicability, context applicability, diagnostics, limitations, coverage, and traceability. It must not reconstruct identity, repair intervals, reinterpret context, or promote conditionally applicable open or superseded intervals into peer eligibility by itself.

Completed First Module:

The First Module expects prepared source-independent observations and fails closed for invalid identity, PIT, comparator, observation, coverage, formula, and traceability states. Comparator Construction may eventually provide governed comparator relationship metadata to Prepared Observations, but it must not enter formula logic or generate first-module quantities.

Future scientific modules:

Future modules may consume prepared comparator-observation packages. Comparator Construction must provide relationship metadata only; modules remain responsible for their own measurement, hypothesis, contamination, falsification, and validation boundaries.

Future Prepared Observations:

Prepared Observations should convert eligible comparator relationships and governed observations into source-independent observation packages. Comparator Construction does not measure observations and does not decide scientific meaning.

## 14. Scope Boundaries

This design does not perform or define:

- code implementation;
- data retrieval;
- acquisition;
- vendor integration;
- entitlement handling;
- source authority evaluation;
- APIs;
- databases;
- schemas;
- real-world identity resolution;
- identity construction;
- security-master construction;
- ticker-lineage construction;
- historical classification construction;
- contextual interpretation;
- economic similarity;
- comparator scoring;
- comparator ranking;
- best-comparator selection;
- optimized membership;
- peer construction from real data;
- context measurement;
- factor construction;
- formulas;
- candidate generation;
- panels;
- IC;
- discovery;
- validation;
- production architecture;
- optimization;
- ML.

It remains strictly an implementation design for deterministic comparator relationship metadata after Source Authority and PIT Identity and Context Evidence, and before Prepared Observations or scientific modules.

## 15. Known Limitations

- No executable code, fixtures, or tests are created by this design.
- No real comparator relationships, peers, classifications, size records, listings, identities, or contexts are created.
- No source is evaluated or accepted.
- No comparator-selection algorithm is defined.
- No scientific similarity standard is defined here; economic-context science remains the upstream scientific foundation.
- Conditional open or superseded identity/context intervals remain limitations and must not be treated as peer eligibility without future comparator governance.
- Duplicate exposure, multiple share classes, same economic company, self-comparison, sparse support, and fallback rules will require careful future synthetic fixture coverage.

## 16. Implementation Readiness Assessment

Final readiness assessment: `READY_FOR_BOUNDED_COMPARATOR_REFERENCE_IMPLEMENTATION`

Rationale:

- Source Authority is fully conformant and can provide upstream source-role trust metadata.
- PIT Identity and Context Evidence is conformant with minor observations and can provide identity/context applicability metadata, diagnostics, limitations, and traceability.
- The integrated scientific inventory separates comparator or benchmark information from alpha information.
- The completed First Module preserves formula logic separately from comparator construction.
- This design defines comparator responsibilities, model, eligibility states, temporal applicability, diagnostics, information contract, traceability, compatibility, and boundaries without changing governance.

Reference implementation readiness is bounded:

- synthetic comparator metadata only;
- no real source use;
- no source ingestion;
- no real identity construction;
- no context interpretation;
- no scientific similarity scoring;
- no measurement;
- no formulas;
- no discovery, validation, production, optimization, or ML.

## 17. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - Phase 5 Comparator Construction Reference Implementation v1`

Rationale:

The implementation design is defined and bounded. The next smallest platform step is a synthetic-only reference implementation that realizes deterministic comparator registration, eligibility metadata, relationship metadata, temporal applicability metadata, diagnostics, traceability, and information-contract behavior. It must not retrieve data, select vendors, define APIs or databases, resolve real identities, interpret context, score similarity, rank comparators, construct real peer groups, measure context, execute formulas, generate candidates, run discovery, run validation, create production logic, optimize, or introduce ML.

## Verification Commands Executed

```text
sed -n '1,220p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_executable_conformance_review_v1.md
sed -n '1,240p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1.md
sed -n '1,220p' docs/research_notes/project_underdog_phase5_source_authority_executable_conformance_rereview_v1.md
sed -n '1,220p' docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md
rg -n "Comparator Construction|comparator construction|Prepared Observations|prepared observations|comparator|peer eligibility|future Comparator" docs/research_notes/project_underdog_phase5_*.md docs/research_notes/project_underdog_first_module_*.md docs/research_notes/project_underdog_master_status_recap_2026-06-17.md
sed -n '1,220p' docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md
sed -n '220,420p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_executable_conformance_review_v1.md
sed -n '240,420p' docs/research_notes/project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1.md
rg -n "implementation code|import requests|read_csv\\(|to_csv\\(|urlopen|httpx|sqlite3|sqlalchemy|RandomForest|fit\\(|predict\\(|IC computation|production architecture defined|ML model|vendor selected|API endpoint|database table" docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
rg -n "source selection|vendor selection|real-world identity resolution|scientific similarity score|formula specification|validation framework|production architecture|machine learning model|retrieved data|constructed peer group|ranked comparator|optimized membership" docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
git diff --check -- docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
git status --short docs/research_notes/project_underdog_phase5_comparator_construction_implementation_design_v1.md
git status --short
```
