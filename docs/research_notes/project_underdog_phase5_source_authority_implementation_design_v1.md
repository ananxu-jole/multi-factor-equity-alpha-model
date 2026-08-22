# Project Underdog - Phase 5 Source Authority Implementation Design v1

Date: 2026-07-18

## 1. Executive Classification

Final classification: `SOURCE_AUTHORITY_IMPLEMENTATION_DESIGN_DEFINED`

This note defines the bounded implementation design for Project Underdog's reusable Phase 5 Source Authority layer. The design translates the Phase 5 external-information authority science into an implementation-ready governance and architecture contract without writing code, defining schemas, retrieving data, selecting vendors, constructing identities, constructing peers, running discovery, running validation, changing production artifacts, optimizing formulas, or introducing ML.

The classification refers only to implementation design readiness for the Source Authority layer. It does not imply source acceptance, acquisition approval, access approval, data availability, PIT identity readiness, economic-context readiness, comparator readiness, empirical validation, production readiness, governance change, or ML readiness.

Repository basis:

- `docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md`: final classification `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`; authority is role-specific, evidence-backed, PIT-sensitive, reproducible, and fail-closed; no source is accepted.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_lineage_science_v1.md`: final classification `PIT_IDENTITY_AND_LINEAGE_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`; identity and lineage require authority before construction.
- `docs/research_notes/project_underdog_phase5_economic_context_validity_science_v1.md`: final classification `ECONOMIC_CONTEXT_VALIDITY_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`; economic context is a PIT comparison structure, not static metadata.
- `docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md`: final classification `CONTAMINATION_AND_ORTHOGONALITY_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`; source, identity, temporal, peer-definition, and interpretation contamination must remain visible.
- `docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md`: final classification `NEGATIVE_EVIDENCE_AND_FALSIFICATION_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`; source failure, contamination failure, redundancy, and null evidence must be preserved.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: final classification `INTEGRATED_SCIENTIFIC_INFORMATION_INVENTORY_DEFINED_WITH_OPEN_GAPS`; information role and evidence maturity must be separated.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: final classification `PHASE_5_PROGRAM_DEFINED`; external information must earn authority before feature use.
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`: Platform v2 scientific discipline remains authoritative.
- `docs/research_notes/project_underdog_first_module_implementation_architecture_specification_v1.md`: source-independent downstream architecture requires authority and validity evidence before formula use.
- `docs/research_notes/project_underdog_first_module_executable_implementation_conformance_review_v1.md`: final classification `REFERENCE_IMPLEMENTATION_CONFORMANT_WITH_MINOR_OBSERVATIONS`; the first module is compatible with a future authority layer that supplies source-independent authorized evidence roles.

## 2. Purpose Of Source Authority

Source Authority is the implementation-layer answer to whether a source-role may provide authoritative evidence to Project Underdog. It decides whether a named source evidence package is authorized for a defined scientific concept, role, time relationship, and downstream use boundary.

Source Authority is distinct from:

| Concept | Distinction |
|---|---|
| Acquisition | Acquisition concerns how information is obtained. Source Authority only evaluates whether evidence is authorized and scientifically fit for a role. |
| Storage | Storage preserves artifacts or records. Source Authority records authority status, provenance expectations, diagnostics, and lineage requirements; it does not design databases. |
| Identity | Identity determines the historical object being described. Source Authority determines whether a source may support identity evidence for a defined role. |
| Contextual information | Contextual information may describe sector, industry, size, listing, event, or comparator context. Source Authority determines whether the source-role is allowed to provide that context. |
| Measurement | Measurement defines what a module observes. Source Authority does not calculate values or define measurement formulas. |
| Scientific interpretation | Scientific interpretation decides what evidence means for a hypothesis. Source Authority does not infer alpha, peer validity, repair, decomposition, or causal meaning. |

The layer answers only:

- Is this source authorized for this role?
- What scientific concepts may it satisfy?
- What evidence accompanies the authority claim?
- What temporal guarantees exist?
- What authority level does it possess?
- What lineage accompanies it?
- What limitations or fail-closed diagnostics must downstream layers preserve?

It refuses to answer:

- What is the value?
- How should the value be interpreted?
- How should the value be measured?
- How should it affect alpha?
- Which peers should be selected?
- Whether a hypothesis is valid.

## 3. High-Level Architecture

The conceptual Source Authority layer contains these major responsibilities:

| Component | Primary responsibility |
|---|---|
| Source Authority Boundary | Preserve the boundary between authority evaluation and acquisition, ingestion, identity construction, context measurement, formula execution, discovery, validation, and production. |
| Source Registration Boundary | Register source candidates and source-role claims as governance objects without accepting them by default. |
| Evidence Intake Boundary | Accept only evidence descriptors and controlled references; do not retrieve data or proprietary documentation. |
| Authority Evaluation Layer | Deterministically evaluate source-role authority against provenance, temporal, coverage, revision, reproducibility, auditability, and fitness requirements. |
| Authority Metadata Layer | Record authority class, authority level, supported roles, unsupported roles, limitations, decision state, and open assumptions. |
| Provenance Layer | Preserve origin, version, publication identity, acquisition identity where known, evidence lineage, and source versioning semantics. |
| PIT Guarantee Layer | Communicate role-specific temporal guarantees and unresolved temporal gaps to downstream systems. |
| Conflict And Limitation Layer | Represent source conflicts, unsupported evidence, unresolved authority, missingness, coverage limits, and fail-closed constraints. |
| Diagnostics Layer | Emit deterministic diagnostics for authority failure, insufficiency, conflict, missing provenance, missing temporal guarantees, unsupported evidence, and unresolved authority. |
| Downstream Information Contract Layer | Provide authorized evidence roles and authority diagnostics to identity, context, comparator, and module layers without providing values, formulas, peers, or interpretations. |
| Traceability And Reproducibility Layer | Preserve authority decision lineage, evidence references, retention expectations, checksums or controlled references where available, and audit metadata. |

This architecture is conceptual. It defines responsibilities and allowed information flow, not code, APIs, schemas, file formats, databases, or connectors.

## 4. Responsibility Allocation

| Responsibility | Purpose | Inputs | Outputs | Dependencies | Prohibited responsibilities |
|---|---|---|---|---|---|
| Authority evaluation | Decide whether a source-role has sufficient evidence for a defined scientific role. | Source-role claim, evidence matrix, provenance references, temporal semantics, coverage and revision evidence. | Authority decision state, role scope, limitations, diagnostics. | WS1 authority science, Platform v2, integrated inventory. | Retrieving data, choosing vendors, calculating values, validating hypotheses. |
| Source registration | Represent a source candidate and requested role without granting authority. | Source identity descriptor, role request, evidence references, project-known metadata. | Registered source-role object in design terms. | Authority science and artifact-lineage discipline. | Source selection, acquisition, entitlement claims, connectors. |
| Authority metadata | Record what authority means for each source-role. | Authority decision, supported concepts, unsupported concepts, evidence strength. | Authority class, level, use boundary, open assumptions, expiration or review status. | Evidence hierarchy and information-role taxonomy. | Scientific interpretation, field mapping, formulas, production flags. |
| Provenance capture | Preserve origin and lineage of the authority evidence. | Source origin, source version, documentation references, evidence references, extraction/project-known references where applicable. | Provenance summary and lineage references. | Reproducibility and artifact lineage. | Data ingestion, row construction, hidden source fallback. |
| Lineage registration | Link authority decisions to evidence packages and downstream role permissions. | Authority decision, evidence ids or references, source-role scope, limitations. | Decision lineage and downstream trace handle. | Platform v2 traceability and first-module traceability expectations. | Identity lineage construction or company/security mapping. |
| Temporal guarantees | State what date semantics are supported and what remains unknown. | Effective-date evidence, publication/availability semantics, revision policy, snapshot/project-known references. | PIT guarantee status, known-date limitations, required delays or fail-closed markers. | WS1 temporal framework, WS2 identity timing, WS3 historical context. | Executable PIT logic or date repair. |
| Evidence documentation | Preserve evidence strength, evidence type, and permitted use. | Official definitions, dictionaries, methodology, revision policy, coverage evidence, sample evidence, controlled references. | Evidence matrix and permitted-use summary. | WS1 evidence hierarchy. | Treating informal or current-state evidence as authoritative. |
| Authority diagnostics | Explain failed, unresolved, insufficient, conflicting, or unsupported authority states. | Evaluation outcomes and missing evidence. | Deterministic diagnostics. | Contamination and falsification frameworks. | Silent acceptance, imputation, automatic resolution. |
| Conflict handling | Represent disagreements among source-role claims. | Competing authority claims, conflicting evidence, temporal conflicts, coverage conflicts. | Conflict status, blocked role, conditional limitation, diagnostic. | WS1 conflict science and WS5 contamination science. | Vendor precedence, production resolution code, manual override without evidence. |
| Retention and reproducibility status | State whether evidence can be preserved or reconstructed. | Snapshot references, version ids, checksums, controlled references, retention limitations. | Reproducibility sufficiency or insufficiency status. | Artifact lineage, validation artifact contracts, WS1 reproducibility requirements. | Creating retention infrastructure or bypassing restrictions. |

## 5. Authority Model

The Source Authority model is role-specific and evidence-backed.

Authority classes:

| Class | Meaning | Allowed downstream use |
|---|---|---|
| `AUTHORITATIVE_FOR_DEFINED_ROLE` | Evidence is sufficient for a defined role and boundary. | May supply authorized contextual or governance evidence to downstream layers for that role only. |
| `CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE` | Evidence is sufficient only under stated limits, such as date range, universe, role, delay rule, or coverage boundary. | May supply evidence only with limitations and diagnostics preserved. |
| `DIAGNOSTIC_ONLY` | Evidence is useful for exploration, sanity checks, or documentation but lacks authority. | May not supply authoritative PIT research input. |
| `INSUFFICIENT_EVIDENCE` | Evidence is too weak, missing, ambiguous, or incomplete. | Must block authoritative downstream use. |
| `REJECTED_FOR_DEFINED_ROLE` | Evidence fails a role-specific authority requirement. | Must not be used for the rejected role unless reopened under a later high-standard evidence process. |

Authority levels:

| Level | Meaning |
|---|---|
| Role-level authority | Source may satisfy a bounded information role, such as ticker lineage or historical classification, but not unrelated roles. |
| Field/concept-level authority | Evidence is sufficient for a specific concept or field meaning inside a role. |
| Temporal authority | Effective, publication, availability, revision, or snapshot semantics are sufficient for PIT use. |
| Coverage authority | Universe, history, inactive/delisted, exchange, security-type, or missingness evidence is sufficient for scoped use. |
| Reproducibility authority | Evidence can be preserved, reconstructed, or controlled-referenced for future audit. |
| Conflict-resolved authority | Known conflicts have been resolved or bounded for the role. |

Supported evidence:

- official source definitions;
- official data dictionaries;
- official historical-methodology documentation;
- source-provided date semantics;
- source-provided revision policy;
- source-provided coverage evidence;
- reproducible sample evidence;
- controlled references, checksums, row counts, version ids, or retained snapshots where allowed;
- independent corroboration as diagnostic or supporting evidence.

Unsupported evidence:

- popularity, convenience, commercial reputation, or broad industry usage by itself;
- current-state profiles for historical roles;
- informal descriptions without source definitions;
- inferred behavior where critical authority evidence is missing;
- manually curated records without retained dated evidence;
- architecture assumptions treated as source facts.

Conflict handling:

- Conflicts are represented explicitly as authority states or diagnostics.
- The design does not select vendor precedence.
- A conflict may be resolvable, conditionally tolerable, diagnostic-only, or fatal depending on role materiality.
- Unresolved material conflict blocks authority.

Unresolved authority:

Authority remains unresolved when required provenance, temporal, identity, coverage, revision, reproducibility, or conflict evidence is missing. Unresolved authority is a valid scientific outcome and must not be silently converted into diagnostic or authoritative use.

## 6. Provenance Architecture

Provenance responsibilities:

| Provenance element | Required design meaning |
|---|---|
| Origin | Who or what produced the source evidence and what domain the source claims to cover. |
| Version | Source product, documentation, schema, snapshot, release, or source-version identity where available. |
| Acquisition identity | How the evidence package became known to Project Underdog, represented only as a controlled reference or project-known descriptor, not an acquisition path. |
| Publication identity | The published documentation, release, or source-defined artifact that establishes field and role semantics. |
| Effective dates | Dates when facts, records, classifications, identities, listings, or events become economically or legally effective. |
| Expiration | Date or condition after which authority must be reviewed, such as documentation version change, coverage change, source revision, or role expansion. |
| Lineage | Relationship from evidence reference to authority decision to downstream authorized role. |
| Revision history | Whether source records are versioned, corrected, overwritten, backfilled, or restated. |
| Retention status | Whether raw snapshots, controlled references, checksums, row counts, documentation references, and decision records can support later audit. |

The provenance layer must preserve the distinction among source accuracy, authority, operational accessibility, and long-term reproducibility. A source can be accurate but non-authoritative for a role if the provenance, temporal semantics, or reproducibility path is insufficient.

## 7. Point-In-Time Guarantees

Source Authority communicates PIT guarantees to downstream layers as authority metadata and diagnostics. It does not implement PIT identity, construct time series, infer unknown dates, or repair records.

Required PIT guarantee concepts:

- effective-date sufficiency;
- publication-date or availability-date sufficiency where role requires known-date evidence;
- revision-date and restatement handling;
- source snapshot or project-known date;
- temporal scope of authority;
- uncertainty interval, if exact dates are unavailable;
- fail-closed marker when timing is insufficient;
- conservative delay rule status, if later authorized by scientific evidence;
- source version or release identity;
- historical reconstruction status.

Downstream communication:

| Downstream layer | PIT information provided by Source Authority |
|---|---|
| PIT Identity | Whether a source-role may supply identity, ticker, listing, delisting, issuer, or event evidence, and which date semantics are authoritative. |
| Context Evidence | Whether a source-role may supply historical sector, industry, size, classification, market-cap, or economic-context evidence. |
| Comparator Construction | Whether upstream identity and context source roles are authorized enough to support later comparator eligibility. |
| First Module implementation | Whether prepared comparator and observation roles came from authority-cleared evidence before entering source-independent formula logic. |
| Future contextual modules | Which roles are authoritative, conditional, diagnostic-only, insufficient, or rejected. |

If a required PIT guarantee is missing, the Source Authority layer must block authoritative downstream use rather than ask downstream formula or context layers to guess.

## 8. Authority Diagnostics

Deterministic diagnostics:

| Diagnostic | Meaning | Required behavior |
|---|---|---|
| `UNAUTHORIZED_SOURCE` | Source-role has not been authorized. | Reject authoritative use. |
| `INSUFFICIENT_AUTHORITY` | Evidence strength is too weak for the requested role. | Block authoritative use; permit diagnostic only if explicitly allowed. |
| `CONFLICTING_AUTHORITY` | Material source-role conflict exists. | Unresolved or rejected until conflict evidence is governed. |
| `MISSING_PROVENANCE` | Origin, source version, evidence reference, or lineage is missing. | Fail closed for authoritative use. |
| `MISSING_TEMPORAL_GUARANTEE` | Required effective, publication, availability, revision, snapshot, or project-known semantics are absent. | Fail closed for PIT-sensitive roles. |
| `UNSUPPORTED_EVIDENCE` | Evidence type is not strong enough for the role, such as current-state profile or informal description. | Downgrade to diagnostic-only or insufficient evidence. |
| `UNRESOLVED_AUTHORITY` | Required authority question remains unanswered. | Preserve unresolved state; do not silently continue. |
| `ROLE_SCOPE_VIOLATION` | Source is being used outside its authorized role. | Reject use for that role. |
| `COVERAGE_INSUFFICIENT` | Coverage, history, inactive/delisted entities, missingness, or universe scope is insufficient. | Conditional, diagnostic-only, unresolved, or rejected depending on materiality. |
| `REVISION_UNRECONSTRUCTABLE` | Historical records cannot be reconstructed as knowable at the relevant time. | Fail closed for validation-quality PIT use. |
| `REPRODUCIBILITY_INSUFFICIENT` | Evidence cannot be retained, reconstructed, or controlled-referenced. | Block validation-quality authority. |

Diagnostics are explanatory governance outputs. They never repair evidence, choose a source, infer a field, construct identity, build context, construct peers, change formulas, or validate hypotheses.

## 9. Information Contract

Source Authority provides downstream layers:

- source-role authority state;
- supported scientific concepts;
- unsupported scientific concepts;
- authority class and level;
- provenance references;
- source version or documentation version where available;
- temporal guarantee status;
- coverage and missingness status;
- revision and reconstruction status;
- reproducibility and retention status;
- conflict status;
- limitations, conditions, expiration, and review status;
- deterministic diagnostics;
- traceability handle from evidence package to authority decision.

Source Authority refuses to provide:

- raw data values;
- calculated feature values;
- source adapters or query logic;
- vendor API behavior;
- field mappings;
- database schemas;
- identity records or ticker-lineage records;
- company-security mappings;
- historical classification records;
- size records;
- peer memberships;
- comparator sets;
- formulas;
- alpha claims;
- candidates, registries, panels, or IC;
- discovery or validation results;
- production decisions;
- thresholds;
- ML features or model inputs.

Contract rule:

Downstream layers may consume Source Authority only as a governance and evidence-authorization service. They must not treat authority metadata as the external information value itself.

## 10. Boundary Audit

Explicitly prohibited in the Source Authority implementation design:

| Prohibited behavior | Status in this note |
|---|---|
| Acquisition | Not designed. |
| Retrieval | Not designed. |
| Vendor APIs | Not designed. |
| Source selection or ranking | Not performed. |
| Identity construction | Not designed. |
| Ticker-lineage construction | Not designed. |
| Company-security mapping | Not designed. |
| Peer construction | Not designed. |
| Contextual measurement | Not designed. |
| Historical classification construction | Not designed. |
| Formula execution | Not designed. |
| Scientific interpretation | Not performed. |
| Discovery | Not performed. |
| Validation | Not performed. |
| Optimization | Not performed. |
| Production behavior | Not designed. |
| Machine learning | Not introduced. |
| Governance change | Not performed. |

The design intentionally stops at the authority contract and does not expand into ingestion, storage, source-specific mapping, source procurement, identity, context construction, peer construction, empirical research, production, or ML.

## 11. Compatibility Assessment

Future PIT Identity:

Source Authority enables PIT Identity by deciding which source-roles may provide security identity, ticker lineage, listing history, delisting history, issuer relationships, corporate events, and source-known-date evidence. It does not construct identity records. Identity remains blocked when authority is diagnostic-only, insufficient, unresolved, conflicted, or rejected.

Context Evidence:

Source Authority enables Context Evidence by deciding whether historical sector, industry, subindustry, classification-system history, shares, size, market-cap, listing venue, security type, and economic-context roles have sufficient authority. It preserves the rule that static or current-state metadata remains diagnostic-only unless separately accepted.

Comparator Construction:

Source Authority enables later Comparator Construction by certifying upstream source roles for identity and economic context. It does not build comparator sets, choose peer counts, define fallback hierarchies, or select taxonomies.

Completed First Module implementation:

The first module reference implementation accepts prepared source-independent observations and fails closed for invalid identity, PIT, comparator, observation, coverage, formula, and traceability states. Source Authority is compatible because it can supply the upstream authority-cleared role status, temporal guarantee status, diagnostics, and traceability handles needed before those prepared observations enter `run_first_module_reference`.

Future contextual scientific modules:

Future modules can depend on Source Authority as a reusable gate for source-role permission and evidence lineage. The layer supports Platform v2 separation by keeping source authority distinct from measurement, formula design, empirical validation, candidate lifecycle, production, and ML.

## 12. Implementation Readiness

Source Authority is ready for bounded reference implementation.

Readiness basis:

- The scientific authority framework is defined with open scientific gaps documented.
- Role-specific authority classes and evidence hierarchy exist.
- PIT identity and economic context frameworks define downstream dependency needs.
- Contamination and falsification frameworks define fail-closed and negative-evidence requirements.
- The integrated scientific inventory separates information role from evidence maturity.
- The first-module implementation stack is source-independent and conformant, creating a compatible downstream consumer.
- This design defines responsibilities, boundaries, authority model, provenance architecture, PIT guarantee contract, diagnostics, and downstream information contract without modifying scientific conclusions.

Open items that must remain bounded during implementation:

- The reference implementation must use synthetic or abstract evidence packages only unless a later source-specific authority decision is separately authorized.
- No source should become accepted by implementation existence.
- No database schema, connector, ingestion path, vendor interface, or field mapping should be introduced in the reference implementation unless separately scoped.
- Diagnostic and authority states must remain deterministic and fail-closed.

## 13. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - Phase 5 Source Authority Reference Implementation v1`

Rationale:

Repository evidence supports a bounded reference implementation because the authority science, information-role inventory, governance principles, downstream first-module conformance, and this implementation design are now defined. The next step should implement only the source-independent authority decision contract, diagnostics, provenance metadata, PIT guarantee metadata, traceability, and synthetic acceptance tests. It must not retrieve data, select vendors, connect APIs, construct identities, construct peers, perform discovery, run validation, optimize, create production behavior, or introduce ML.
