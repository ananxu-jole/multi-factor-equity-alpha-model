# Project Underdog - Phase 5 PIT Identity And Context Evidence Implementation Design v1

Date: 2026-07-18

## 1. Executive Classification

Final classification: `PIT_IDENTITY_AND_CONTEXT_EVIDENCE_IMPLEMENTATION_DESIGN_DEFINED`

This note defines the implementation architecture for the Project Underdog Phase 5 PIT Identity and Context Evidence platform layer. It sits immediately after Source Authority and before Comparator Construction. Its purpose is to deterministically represent who externally authorized contextual information belongs to, what identity state it applies to, and when it is point-in-time applicable.

This is an implementation-design document only. It does not implement code, retrieve data, select vendors, define databases, define APIs, define schemas, construct identities, construct peers, define contextual measurements, execute formulas, generate candidates, run discovery, run validation, define production architecture, optimize, or introduce ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_source_authority_executable_conformance_rereview_v1.md`: final classification `SOURCE_AUTHORITY_IMPLEMENTATION_FULLY_CONFORMANT`; Source Authority is now suitable as the upstream authority gate.
- `docs/research_notes/project_underdog_phase5_source_authority_implementation_design_v1.md`: Source Authority provides authority state, provenance, temporal guarantees, limitations, diagnostics, and traceability, but not values, identities, peers, or formulas.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_lineage_science_v1.md`: identity and lineage must distinguish security, listing, issuer, legal entity, operating company, economic company, ticker, share class, instrument, and research-universe identity.
- `docs/research_notes/project_underdog_phase5_economic_context_validity_science_v1.md`: economic context must be PIT-valid, role-specific, identity-linked, and not reduced to static labels.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: information role and evidence maturity must remain separate.
- `docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md`: the completed First Module consumes prepared source-independent observations and must not receive ungoverned identity/context evidence.
- Platform v2, artifact-lineage, reproducibility, contamination, and falsification governance remain authoritative.

## 2. Purpose

The PIT Identity and Context Evidence layer determines how externally authorized information is attached to the correct conceptual identity and valid time interval before downstream components can use it.

It answers:

- Which entity does this contextual evidence belong to?
- Which identity level is being referenced?
- During what effective interval is the evidence applicable?
- What lineage, transition, gap, ambiguity, or limitation affects applicability?
- What diagnostic should be emitted when identity or context cannot be applied safely?
- What traceability links the application decision to Source Authority and the governing design?

It does not answer:

- Is the source authoritative?
- What is the raw source value?
- How should context be measured?
- Which securities are peers?
- What formula should use the context?
- Whether a hypothesis is scientifically valid.

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

This layer assumes incoming source-role evidence has already passed Source Authority. It does not re-evaluate source trust. It verifies applicability: identity, lineage, valid time, context interval, coverage, limitations, diagnostics, and traceability.

Downstream layers must still perform their own approved responsibilities. Comparator Construction must build comparator eligibility separately. Scientific modules must consume only prepared observations and must not infer identity or context validity from raw metadata.

## 4. Identity Philosophy

Identity is the answer to what historical object the evidence describes. This design preserves the scientific distinctions established by PIT Identity and Lineage Science:

- A ticker is a label, not a stable identity.
- A security is not automatically the issuer, company, or economic company.
- A listing is not automatically the security.
- An ADR and ordinary share may share economic-company identity while remaining distinct securities and listings.
- Multiple share classes may share issuer or economic-company context while retaining security-specific return identity.
- Corporate transformations can preserve, split, terminate, or ambiguously alter identity.

The implementation design must represent identity states and lineage relationships without constructing real identity records. It must preserve unresolved or ambiguous identity rather than selecting a convenient identity level.

## 5. Context Evidence Philosophy

Context evidence is externally authorized metadata about economic, listing, classification, size, security-type, event, or other context that may later inform comparison or interpretation.

This layer represents context. It does not interpret context.

Context evidence must be:

- linked to an accepted conceptual identity level;
- bounded by effective, valid, or applicability intervals;
- traceable to Source Authority;
- explicit about replacement, revision, expiration, gaps, overlap, and limitations;
- diagnostic when incomplete, ambiguous, missing, or conflicting.

A sector, industry, size, exchange, listing, or event context is not a peer group. It is not a formula input by itself. It becomes eligible for downstream use only after identity and temporal applicability are represented safely and later layers accept their own responsibilities.

## 6. Architecture Overview

Major conceptual components:

| Component | Primary responsibility |
|---|---|
| Source Authority Intake Boundary | Accept only Source Authority-cleared governance metadata and authorized context-role references. |
| Identity Representation Layer | Represent canonical identity, aliases, identity levels, ambiguity, retirement, and synthetic identities for testing. |
| Lineage Representation Layer | Represent continuity, predecessor/successor relationships, transitions, termination, and unresolved lineage. |
| Context Evidence Registration Layer | Register authorized contextual evidence as metadata associated with an identity role and interval. |
| Temporal Applicability Layer | Evaluate effective intervals, valid intervals, open intervals, unknown intervals, supersession, discontinuities, and non-reconstructable history. |
| Identity-Context Association Layer | Attach context evidence to the appropriate identity state and block mismatched associations. |
| Coverage And Limitation Layer | Preserve coverage gaps, incomplete intervals, missing context, limitations, and downstream restrictions. |
| Diagnostics Layer | Emit deterministic diagnostics for identity, lineage, interval, coverage, and context-applicability failures. |
| Information Contract Layer | Provide only identity/context applicability metadata, diagnostics, limitations, and traceability. |
| Traceability Layer | Preserve Source Authority reference, identity decision, lineage decision, interval decision, context registration, diagnostics, and governing design version. |

This is a conceptual architecture. It does not define classes, APIs, schemas, storage, source queries, field mappings, or database tables.

## 7. Component Responsibilities

| Responsibility | Purpose | Inputs | Outputs | Dependencies | Prohibited responsibilities |
|---|---|---|---|---|---|
| Identity representation | Represent the target identity level and canonical identity state. | Source-authorized role metadata, identity evidence reference, requested identity role. | Identity applicability metadata or diagnostic. | Source Authority; PIT Identity science. | Constructing real security masters or resolving identities from raw source data. |
| Identity lineage | Represent continuity, transition, predecessor/successor, retirement, or unresolved lineage. | Identity state metadata, transition references, effective intervals. | Lineage metadata and limitations. | PIT Identity science. | Creating lineage records or deciding corporate event truth from raw data. |
| Effective-date representation | Preserve when a context or identity relation becomes effective. | Effective interval metadata from authorized evidence. | Effective start/end or unknown/open interval metadata. | Source Authority temporal guarantees. | PIT calculation, known-date inference, or date repair. |
| Valid-time representation | Represent when evidence may be used for historical applicability. | Effective dates, source-known/project-known references, revision status. | Valid-time applicability metadata. | Source Authority and temporal governance. | Constructing historical panels. |
| Context-evidence representation | Represent context as authorized metadata. | Context role, identity role, interval, evidence lineage, limitation metadata. | Context evidence record concept. | Economic Context science. | Measuring context values or interpreting economic meaning. |
| Context-evidence registration | Register context evidence as an applicability object. | Authorized context evidence metadata. | Registered context-applicability metadata. | Source Authority authority state. | Source selection, data ingestion, schema definition. |
| Identity-to-context association | Link context evidence to an identity state and level. | Identity metadata, context metadata, interval metadata. | Association status, limitations, diagnostics. | PIT identity and economic context frameworks. | Peer construction or company-security mapping construction. |
| Temporal applicability | Determine whether the interval relationship is safe, bounded, open, missing, overlapping, or invalid. | Effective start/end, valid time, supersession, discontinuity markers. | Applicability status and diagnostics. | Temporal authority framework. | Executable PIT logic or formula timing. |
| Coverage representation | Preserve where context evidence is present, missing, incomplete, or not applicable. | Coverage metadata and interval status. | Coverage metadata, gap markers, downstream restrictions. | Source Authority coverage status. | Imputation or fallback peer grouping. |
| Context limitations | Communicate bounded use and unresolved applicability. | Limitations from Source Authority and identity/context evaluation. | Limitation metadata. | Source Authority and context science. | Alpha interpretation or validation decision. |
| Traceability | Preserve why evidence was or was not applicable. | Source authority trace, identity metadata, interval metadata, diagnostics. | Traceability package. | Artifact lineage and reproducibility. | Decorative trace without decision lineage. |
| Deterministic diagnostics | Explain metadata failures. | Identity, lineage, context, interval, coverage, and association states. | Stable diagnostic codes and messages. | Platform v2 fail-closed governance. | Silent repair, defaults, or unsupported overrides. |

## 8. Identity Model

Conceptual identity representations:

| Concept | Design meaning |
|---|---|
| Canonical identity | The identity state accepted for applicability within a defined identity role and interval. |
| Identity aliases | Labels, tickers, names, or source aliases attached to an identity; never sufficient as stable identity by themselves. |
| Lineage | Ordered relationship among identity states, including continuity, transitions, successors, predecessors, and termination. |
| Successor/predecessor relationship | Dated relationship between identity states created by transformation, event, or continuity evidence. |
| Identity continuity | Evidence that the same identity persists for the intended identity role. |
| Identity ambiguity | Evidence cannot determine whether identities are the same, distinct, continuous, or transformed. |
| Unresolved identity | Identity is not safe for downstream context application. |
| Retired identity | Identity state has terminated, become inactive, or is no longer applicable after an end interval. |
| Synthetic identity | A non-real identity object used only for fixtures and acceptance tests. |

Identity status values should remain conceptual in this design:

- valid;
- conditionally valid;
- unresolved;
- ambiguous;
- retired;
- rejected.

The design does not define implementation-specific identifiers. It requires that any later implementation preserve identity level, role, interval, lineage reference, ambiguity status, and Source Authority trace.

## 9. Context Evidence Model

Context evidence representation:

| Concept | Design meaning |
|---|---|
| Contextual evidence | Authorized metadata about sector, industry, classification, size, listing, security type, event, or other context role. |
| Evidence applicability | Whether evidence applies to the identity state for a time interval. |
| Effective interval | Interval over which the context is economically or legally effective. |
| Expiration | Date, supersession event, or review condition after which applicability must end or be re-evaluated. |
| Replacement | New context evidence supersedes prior evidence for the same role and identity interval. |
| Revision | Source-authorized correction or restatement of prior context metadata. |
| Incomplete evidence | Evidence lacks some required applicability metadata but may remain diagnostic or conditional. |
| Overlapping evidence | Two or more context records claim applicability over overlapping intervals. |
| Missing evidence | Required context is absent for an identity interval. |

This layer registers context evidence but does not interpret whether an industry is comparable, whether size is sufficient, or whether a context should affect a formula.

## 10. Temporal Model

Required temporal concepts:

| Temporal concept | Design meaning | Fail-closed behavior |
|---|---|---|
| Effective start | First date/time the identity or context relation applies. | Missing start is unresolved when role requires bounded applicability. |
| Effective end | Last date/time the relation applies. | Missing end may be open only when source authority permits open intervals. |
| Open interval | Interval with known start and no known end. | Allowed only with explicit open-interval marker and review/expiration metadata. |
| Unknown interval | Interval boundary is unknown. | Diagnostic or unresolved; must not become authoritative applicability silently. |
| Superseded interval | Prior context interval replaced by later evidence. | Preserve replacement lineage and prevent simultaneous silent applicability. |
| Discontinuity | Gap or break in identity or context applicability. | Preserve gap and downstream restriction. |
| Non-reconstructable history | Historical interval cannot be reconstructed as knowable. | Reject or unresolved for PIT research use. |
| Project-known relationship | The point at which Project Underdog records evidence availability. | Must be traceable; this layer does not infer it. |

Temporal ordering is represented, not computed into historical datasets. Later implementations may create synthetic fixtures to test interval relationships, but this design does not construct real PIT panels.

## 11. Diagnostic Model

Deterministic diagnostic categories:

| Diagnostic | Meaning | Required behavior |
|---|---|---|
| `UNRESOLVED_IDENTITY` | Identity cannot be safely established for the role. | Block authoritative downstream use. |
| `AMBIGUOUS_IDENTITY` | Multiple identity interpretations are possible. | Preserve ambiguity and block or condition downstream use. |
| `MISSING_CONTEXTUAL_EVIDENCE` | Required context evidence is absent for an interval. | Preserve missingness and downstream restriction. |
| `OVERLAPPING_CONTEXT_INTERVALS` | Context intervals overlap without governed replacement or reconciliation. | Unresolved until governed. |
| `INVALID_TEMPORAL_ORDERING` | Start/end/supersession relationships are invalid or contradictory. | Fail closed. |
| `NON_RECONSTRUCTABLE_LINEAGE` | Identity or context history cannot be reconstructed as knowable. | Reject or unresolved for PIT research use. |
| `UNSUPPORTED_CONTINUITY` | Continuity is asserted without sufficient lineage support. | Block continuous downstream use. |
| `INCOMPLETE_APPLICABILITY` | Required applicability metadata is missing or conditional. | Conditional or unresolved depending role materiality. |
| `COVERAGE_GAP` | Evidence is missing over part of a required interval. | Preserve gap; do not impute. |
| `CONFLICTING_IDENTITY_ASSOCIATION` | Context evidence could apply to conflicting identity states. | Unresolved until conflict is governed. |
| `SOURCE_AUTHORITY_NOT_ACCEPTED` | Upstream authority state is not authoritative or conditionally acceptable for the role. | Reject or diagnostic-only. |
| `TRACEABILITY_INCOMPLETE` | Applicability decision lacks lineage to source, identity, interval, or design. | Reject authoritative downstream use. |

Diagnostics describe metadata conditions only. They do not correct identity, select peers, calculate context, execute formulas, or validate hypotheses.

## 12. Information Contract

Approved downstream outputs:

- canonical identity metadata;
- identity level and role;
- identity alias metadata where authorized;
- identity lineage metadata;
- successor/predecessor metadata;
- temporal applicability metadata;
- context evidence metadata;
- context role and evidence status;
- coverage metadata;
- limitations;
- diagnostics;
- Source Authority trace reference;
- governing design version;
- reproducibility and artifact-lineage references.

The contract must refuse:

- raw source values;
- retrieval instructions;
- authority evaluation;
- vendor identifiers as authority substitutes;
- database schemas;
- API contracts;
- comparator sets;
- peer groups;
- contextual measurements;
- formulas;
- scientific interpretations;
- alpha claims;
- candidates;
- panels;
- IC;
- validation outcomes;
- production decisions;
- ML inputs.

The contract should make downstream limitations explicit:

- identity unresolved;
- context missing;
- interval open;
- interval unknown;
- overlap unresolved;
- lineage non-reconstructable;
- coverage incomplete;
- diagnostic-only context;
- conditionally applicable context.

## 13. Traceability Model

Traceability must be sufficient to reconstruct:

- Source Authority decision reference;
- source-role authority state consumed by this layer;
- evaluated identity level;
- canonical identity metadata;
- identity alias metadata where applicable;
- lineage relationship used;
- predecessor/successor relationship if applicable;
- registered context evidence;
- effective interval;
- valid-time interval;
- open, missing, superseded, or discontinuous interval markers;
- limitations;
- diagnostics;
- governing design version;
- fixture id if synthetic;
- reproducibility or controlled-reference handle.

Traceability is mandatory. A context-applicability decision without traceability must be rejected for authoritative downstream use.

## 14. Compatibility Assessment

Source Authority:

This design consumes Source Authority outputs as upstream governance metadata. It does not re-evaluate source authority. Records with `DIAGNOSTIC_ONLY`, `INSUFFICIENT_EVIDENCE`, or `REJECTED_FOR_DEFINED_ROLE` must not silently enter authoritative PIT identity/context applicability.

Future Comparator Construction:

Comparator Construction can later consume identity/context applicability metadata, but must still perform its own comparator eligibility, group membership, missingness, duplicate exposure, fallback, and peer-count responsibilities. This design does not create comparator sets.

Completed First Module:

The First Module accepts prepared source-independent observations and fails closed for invalid identity, PIT, comparator, observation, coverage, formula, and traceability states. This design can feed future prepared observations by ensuring identity and context applicability are established upstream, while preserving that the First Module does not perform identity construction or context interpretation.

Future contextual-information modules:

Future modules may rely on this layer for identity/context applicability metadata, limitations, diagnostics, and traceability. They must still define their own measurement and hypothesis boundaries.

## 15. Scope Boundaries

This design does not perform or define:

- code implementation;
- data retrieval;
- source acquisition;
- vendor selection;
- entitlement management;
- databases;
- APIs;
- schemas;
- source ingestion;
- source authority evaluation;
- security-master construction;
- ticker-lineage construction;
- company-security mapping construction;
- historical classification construction;
- size-record construction;
- comparator construction;
- peer construction;
- contextual measurement;
- formulas;
- candidate generation;
- discovery;
- validation;
- production architecture;
- optimization;
- ML.

It remains strictly an implementation design for representing PIT identity and context applicability after Source Authority and before downstream construction or scientific modules.

## 16. Known Limitations

- No real identities, context evidence, intervals, classifications, size records, listings, events, or peer relationships are created.
- No source is evaluated or accepted by this design.
- No executable fixtures or tests are created here.
- Open questions from PIT Identity and Economic Context science remain scientific constraints for later implementation work.
- Any future reference implementation must use synthetic identity/context evidence until real source-role acceptance and separate construction authority exist.

## 17. Implementation Readiness Assessment

Final readiness assessment: `READY_FOR_BOUNDED_REFERENCE_IMPLEMENTATION`

Rationale:

- Source Authority is fully conformant and can provide upstream authority metadata.
- PIT Identity and Economic Context scientific frameworks define the identity, lineage, context, and temporal requirements this layer must preserve.
- The design defines responsibilities, information contract, diagnostics, traceability, and boundaries without changing governance.
- The completed First Module remains compatible because this layer does not enter formula logic or comparator construction.

Reference implementation readiness is bounded:

- synthetic identity and context evidence only;
- no real source use;
- no source ingestion;
- no identity construction from raw records;
- no context measurement;
- no comparator construction;
- no validation or production behavior.

## 18. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - Phase 5 PIT Identity and Context Evidence Reference Implementation v1`

Rationale:

The implementation design is defined and bounded. The next smallest platform step is a reference implementation that realizes only deterministic synthetic identity/context applicability metadata, diagnostics, traceability, and information-contract behavior. It must not retrieve data, select vendors, define schemas, construct real identities, construct context records from external data, build comparators, measure context, execute formulas, run discovery, run validation, create production logic, optimize, or introduce ML.
