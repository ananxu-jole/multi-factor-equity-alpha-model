# Project Underdog - Phase 5 External Information Authority Science v1

Date: 2026-07-14

Scientific workstream: `External Information Authority Science`

Phase 5 roadmap position: Workstream 1

Final classification: `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`

This note defines the scientific authority framework required before any external information may be used as authoritative point-in-time evidence in Project Underdog. It is a scientific standards artifact only. It is not a vendor review, licensing review, institutional-access review, procurement exercise, data-source selection, implementation specification, software architecture task, source-ingestion task, PIT construction task, security-master construction task, ticker-lineage construction task, peer-construction task, alpha-formula task, candidate-registration task, panel task, IC task, validation task, governance mutation, production change, threshold change, or ML task.

The classification concerns only the scientific authority framework. It does not imply source acceptance, vendor approval, license approval, access approval, data availability, PIT readiness, implementation authorization, empirical validation, or production eligibility.

## Repository Evidence Reviewed

Current authoritative project state:

- `docs/research_notes/project_underdog_strategic_program_reassessment_v1.md`: final classification `PROJECT_READY_FOR_NEXT_MAJOR_PHASE`; broad OHLCV discovery is no longer the primary strategic frontier; ML remains deferred; authoritative PIT metadata is the next bottleneck.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: final classification `PHASE_5_PROGRAM_DEFINED`; Phase 5 is `External Information Integration`; external information must earn authority before feature use.
- `docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md`: final classification `PHASE_5_SCIENTIFIC_ROADMAP_DEFINED`; Workstream 1 is External Information Authority Science and is mandatory before source-dependent conclusions in later workstreams.
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`: Platform v2 requires hypothesis-first science, orthogonality, falsifiability, candidate discipline, predefined success criteria, and negative-evidence learning.
- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`: lifecycle separation between design, implementation, panel generation, IC discovery, research review, governance, validation, and production.

PIT, source-gate, identity, and economic-context evidence:

- `docs/research_notes/pit_external_dependency_closeout_v1.md`: `PIT_READY_PENDING_EXTERNAL_LICENSE`; source evidence status is blocked by license, entitlement, official documentation, retention, archive, reproducibility, and known-date semantics.
- `docs/research_notes/pit_external_evidence_intake_review_v1.md`: `EXTERNAL_EVIDENCE_PATH_BLOCKED_BY_SOURCE_OR_GOVERNANCE_GAPS`; no source is accepted; static economic metadata is diagnostic-only.
- `docs/research_notes/security_master_and_ticker_lineage_pit_policy_and_vocab_design_v1.md`: controlled vocabulary for source status, PIT quality, confidence, event types, blocked reasons, inferred windows, stale-age policy, and manual overrides.
- `docs/research_notes/security_master_and_ticker_lineage_pit_source_gate_scaffold_v1.md`: `SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES`; scaffold is source-free and fail-closed.
- `docs/research_notes/source_gate_semantic_validation_implementation_v1.md`: `READY FOR SOURCE EVALUATION`; canonical allowed-use mapping and semantic eligibility exist, but no real source rows, source acceptance, ingestion, or construction exists.
- `docs/research_notes/security_master_and_ticker_lineage_pit_design_review_v1.md`: identity first, classifications later, peer reconstruction last.
- `docs/research_notes/point_in_time_economic_context_readiness_audit_v1.md`: economic-context substrate is diagnostically strong but not PIT discovery ready; historical integrity is the blocker.
- `docs/research_notes/point_in_time_economic_metadata_source_and_lineage_design_v1.md`: source hierarchy and PIT rules are design-only; current/static labels must not be backfilled.
- `docs/research_notes/manual_metadata_coverage_expansion_v3.md` and `docs/research_notes/metadata_source_lineage_consistency_review_v1.md`: static metadata has useful diagnostic coverage but remains `STATIC_SNAPSHOT_RESEARCH_ONLY`.

Validation, reproducibility, candidate authority, contamination, and negative-evidence evidence:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`: validation artifact contracts preserve scope, checksums, manifest flags, contamination placeholders, and fail-closed execution boundaries.
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`: negative evidence must be preserved and cannot be rescued by post-hoc reinterpretation.
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry_implementation_v1.md`: a registry may be authoritative for candidate metadata without authorizing formulas, panels, IC, validation, production, or ML.
- Existing source-specific notes, including `docs/research_notes/crsp_source_candidate_evaluation_v1.md` and `docs/research_notes/crsp_external_verification_requirements_package_v1.md`, are treated only as prior examples of requirement categories such as field semantics, retention, known-date evidence, source-lineage evidence, and reproducibility blockers. They are not treated as source approval, ranking, procurement direction, access evidence, or the scientific objective of this workstream.

Superseded or limited material:

- Static metadata expansion notes remain valid for descriptive diagnostics but are superseded for alpha/validation use by the PIT external dependency and Phase 5 notes.
- Prior source-candidate evaluations remain useful as planning history but do not establish current source authority.
- Source-gate scaffolds and semantic runners are implementation concepts and diagnostic practices, not source acceptance.

## 1. Executive Scientific Classification

Final classification: `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`

Rationale:

- Repository evidence is sufficient to define a source-independent authority framework.
- Current project rules clearly require fail-closed source status, PIT semantics, identity lineage, reproducibility, auditability, and diagnostic/authoritative separation.
- No external source is currently accepted as authoritative for Phase 5 empirical research.
- Several scientific gaps remain open, especially publication-date necessity, conservative lag sufficiency, historical incompleteness tolerance, multi-source role authority, restricted-data reproducibility, and conflict treatment.

This classification does not imply source acceptance, vendor approval, license approval, access approval, data availability, PIT readiness, implementation authorization, or empirical validation.

## 2. Scientific Meaning Of Authority

`Authoritative external information` means external information whose provenance, temporal semantics, identity semantics, coverage, revision behavior, lineage, retention path, and scientific fitness are evidenced well enough that Project Underdog may rely on it for a defined research role without converting hidden assumptions into apparent empirical evidence.

Authority is role-specific, date-specific, evidence-backed, reproducible or reconstructable, and fail-closed. An authoritative source-role must answer: what was known, by whom, from what source version, under what date semantics, for which security or issuer identity, with what coverage and missingness, and with what preserved lineage.

Authority is not the same as:

- availability: a source can be accessible but undocumented or non-retainable;
- popularity or broad industry usage: common use does not prove PIT safety;
- convenience: easy joins can hide ticker reuse and current-label leakage;
- commercial reputation: reputation is not field-level evidence;
- documentation quality: good documentation helps, but authority requires role-specific semantics and reproducibility;
- apparent accuracy: current correctness does not prove historical knowability;
- identifier matching: a crosswalk can match strings without proving identity continuity;
- diagnostic usefulness: useful comparison or enrichment can remain diagnostic-only;
- implementation convenience: code feasibility is not scientific evidence.

A source may be useful yet fail authority if it is static, current-state, overwritten, insufficiently dated, unreproducible, missing delisted names, unable to resolve identity conflicts, or not scientifically fit for the intended role.

## 3. Authority Dimensions

| dimension | scientific purpose | failure risk | minimum evidence needed | failure status | dependent workstreams |
|---|---|---|---|---|---|
| Source provenance | Identify who produced the record and under what source/version. | Untraceable evidence and silent source fallback. | Official source definition, provider/source/version/snapshot id, source-role statement. | Fatal for authoritative use. | All WS2-WS9. |
| Temporal validity | Ensure record use is valid for the signal date. | Look-ahead, stale records, future labels. | Effective/as-of/known-date semantics or governed snapshot inference. | Fatal when role is time-sensitive; conditionally manageable for durable static facts only with evidence. | WS2, WS3, WS4, WS5, WS7, WS9. |
| Identity validity | Bind information to the correct security, issuer, listing, and share class. | Ticker reuse, false continuity, wrong issuer joins. | Stable ids, issuer/security definitions, exchange/share-class namespace, dated mappings. | Fatal for identity-dependent roles. | WS2, WS3, WS4, WS5, WS8, WS9. |
| Historical completeness | Cover the research period and inactive entities. | Truncated history and survivorship bias. | Coverage dates, active/inactive coverage, delisting coverage, known exclusions. | Fatal if missingness biases intended use; conditionally manageable if scope-limited. | WS2, WS3, WS4, WS6, WS8. |
| Effective-date clarity | Define when a fact became economically effective. | Future or stale state assigned to wrong date. | Field definitions for effective start/end or auditable inferred windows. | Fatal for classifications, identity, listings, events. | WS2, WS3, WS4. |
| Publication/availability-date clarity | Define when the project could have known the fact. | Delayed or retroactive data used before knowable. | Announcement/publication/source-availability dates, release notes, or conservative source snapshot policy. | Fatal where known-date matters; open gap for conservative lag rules. | WS2, WS3, WS4, WS5, WS9. |
| Revision transparency | Understand corrections, backfills, and overwrites. | Historical artifacts silently change meaning. | Revision policy, version ids, correction records, preserved prior versions or controlled references. | Fatal if historical knowability cannot be reconstructed. | WS1, WS2, WS3, WS7, WS8. |
| Survivorship control | Include entities that died, merged, delisted, or changed identity. | Survivor-only peers, false repair, missing terminal events. | Active/inactive coverage, delisting dates, security end dates, universe coverage diagnostics. | Fatal for universe, identity, peer, and validation use. | WS2, WS3, WS4, WS5. |
| Delisting coverage | Preserve terminal listing state. | Post-delisting rows, missing failures, biased returns. | Delisting date/reason where available, inactive security treatment, event date semantics. | Fatal for security identity and active universe roles. | WS2, WS3, WS4. |
| Corporate-event treatment | Handle mergers, spinoffs, reorganizations, split-offs, relistings, and share-class changes. | False continuity or false breaks. | Event definitions, predecessor/successor ids, effective/as-of dates, confidence rules. | Fatal for affected records; conditionally manageable by blocking affected windows. | WS2, WS3, WS4, WS5. |
| Classification-history integrity | Preserve historical sector/industry/taxonomy membership. | Current classifications backfilled into the past. | Dated classification history, taxonomy versions, revision policy, source lineage. | Fatal for peer/economic-context authority. | WS3, WS4, WS5, WS7. |
| Identifier continuity | Maintain stable ids through time and across events. | Broken joins and duplicate entities. | Permanent security/issuer ids or documented mapping rules with confidence. | Fatal for lineage and peer construction. | WS2, WS3, WS4, WS8. |
| Universe coverage | Define which securities are included or excluded through time. | Biased peer sets and incomplete panels. | Coverage reports by date, exchange, type, country, active/inactive status. | Fatal if intended universe cannot be represented; conditionally manageable with scoped claims. | WS2, WS3, WS4, WS8. |
| Reproducibility | Rebuild or audit the evidence state. | Findings cannot be challenged or repeated. | Raw snapshot or controlled reference, source version, query/extract record, checksums or allowed substitute. | Fatal for validation-quality authority; conditionally manageable for restricted evidence only with controlled references. | All WS2-WS9. |
| Auditability | Allow later review of decisions and lineage. | Authority becomes unverifiable. | Evidence matrix, source-role assessment, decision record, row-count/hash/reference summaries. | Fatal for authority decision. | All WS2-WS9. |
| Retention capability | Preserve evidence under allowed-use constraints. | Source cannot support long-term scientific claims. | Retention policy for raw data, derived metadata, hashes, row counts, references, notes. | Fatal if no reproducible alternative exists. | WS1, WS2, WS3, WS8, WS9. |
| Lineage traceability | Link derived metadata to source evidence. | Derived fields become unsupported assertions. | Source record ids, metadata version, run id, normalization rules, derived lineage. | Fatal for authoritative derived roles. | WS2, WS3, WS4, WS8. |
| Schema stability | Know whether fields and definitions changed. | Time-varying semantics hidden behind stable names. | Data dictionaries, release/version notes, schema-change policy. | Conditionally manageable if versioned; fatal if reinterpretation is untraceable. | WS2, WS3, WS8. |
| Conflict transparency | Expose disagreements rather than silently choose. | Undetected identity/classification/event conflicts. | Conflict logs, role precedence rules, manual review status, blocked outcomes. | Fatal when unresolved and material. | WS2, WS3, WS4, WS5, WS8. |
| Null and missingness transparency | Distinguish absent, unknown, not covered, not applicable, and withheld. | Silent imputation and biased coverage. | Missingness definitions, null-rate reports, blocked/fallback rules. | Fatal if missingness affects intended use and cannot be governed. | WS3, WS4, WS6, WS8. |
| Scientific fitness for intended use | Match evidence strength to the research claim. | Using good data for the wrong role. | Source-role assessment, role-specific evidence matrix, limits and conditions. | Fatal for overbroad role claims; manageable by narrowing role. | All WS2-WS9. |

## 4. Authority Is Role-Specific

Authority must be evaluated separately for different information roles. A source can be authoritative for one role and unacceptable for another because each role has different identity, temporal, coverage, revision, and reproducibility requirements.

Role framework:

| role | authority question | special requirements | why authority may differ |
|---|---|---|---|
| Security identity | Which security existed on a date? | Stable security id, activity window, type, share class, exchange/listing status. | A source may identify securities well without classifying industries. |
| Ticker lineage | Which ticker mapped to which security on a date? | Dated ticker windows, exchange namespace, ticker reuse rules. | A source may have current tickers but no historical windows. |
| Company-security relationships | Which issuer/company relates to which security? | Issuer ids, link windows, link quality, share-class and entity-event treatment. | Security identity and issuer continuity are not the same fact. |
| Listing history | Was the security listed and eligible? | Listing start/end, exchange, status, security type. | Listing authority may not include economic classification authority. |
| Delisting history | When and how did listing end? | Delisting date, inactive coverage, reason if used, known-date semantics. | Missing delistings create survivorship bias even if active listings are correct. |
| Exchange history | What venue/namespace governed the ticker? | Dated exchange codes and migrations. | Exchange authority may be needed to disambiguate reused tickers. |
| Sector history | What sector applied as of the date? | PIT classification history, taxonomy version, effective and known dates. | Current sector correctness does not prove historical sector authority. |
| Industry history | What industry/subindustry applied as of the date? | Granular taxonomy history, coverage, revision policy. | Industry role is often more demanding than sector role. |
| Classification-system history | Which taxonomy definition existed? | Taxonomy version, reclassification policy, schema history. | A classification code can change meaning over time. |
| Corporate events | What event changed identity or continuity? | Event type, predecessor/successor, effective/as-of dates, correction handling. | Event evidence may be authoritative for exclusion but not for issuer continuity. |
| Shares outstanding | What share count was knowable? | Definition, adjustment basis, effective/as-of dates, revision behavior. | Shares may be restated and differ by basic/diluted/float definitions. |
| Size or market-cap context | What size bucket or market cap was valid? | Date-safe price/shares or accepted market-cap series, known-date policy. | Static size labels leak later company scale into past dates. |
| Peer-membership support | Which contemporaneous peers were eligible? | Accepted identity, classification, active universe, missingness and group-size rules. | Peer authority is derived from multiple upstream roles. |
| Economic-context state | What economic context was knowable? | Sector/industry/size/listing/event inputs, source versions, coverage diagnostics. | Context authority depends on the weakest necessary input. |
| Source-known-date authority | When could the source have made the record available? | Publication, release, availability, snapshot, revision, and extraction semantics. | Accurate facts can be non-authoritative if known-date is unknown. |

No real source is approved or ranked by this framework.

## 5. Evidence Hierarchy

| evidence type | scientific strength | permitted use |
|---|---|---|
| Official source definitions | Very strong | Define source domain, entity definitions, and role scope if current and applicable. |
| Official data dictionaries | Very strong | Establish field meaning, nulls, identifiers, and date fields; necessary for field-level authority. |
| Official historical-methodology documentation | Very strong | Establish historical construction, coverage, survivor treatment, taxonomy changes, and event handling. |
| Source-provided date semantics | Very strong | Establish effective, as-of, publication, availability, revision, and snapshot meaning. |
| Source-provided revision policy | Strong | Determine whether historical knowability can be reconstructed. |
| Source-provided coverage evidence | Strong | Support universe, inactive/delisted, exchange, country, type, and date-range claims. |
| Reproducible sample evidence | Moderate to strong | Test whether documented semantics behave as claimed; cannot replace official definitions. |
| Observed empirical behavior | Moderate | Detect inconsistencies, missingness, or suspicious revisions; cannot alone establish authority. |
| Independent cross-source comparison | Moderate | Diagnose conflicts and coverage gaps; does not automatically decide authority. |
| Repository architecture assumptions | Weak to moderate | Useful for requirement design; not evidence of external facts. |
| Informal descriptions | Weak | May guide questions; not sufficient for authority. |
| Public summaries | Weak | Establish plausibility only; not sufficient for source-role acceptance. |
| Current-state profiles | Diagnostic only | Useful for descriptive checks; blocked for PIT authority unless independently accepted. |
| Manually curated records | Diagnostic or conditional only | May support review or synthetic fixtures; authoritative only if backed by retained dated evidence and governed overrides. |
| Inferred behavior | Weak | Allowed only as a clearly flagged inference under conservative, auditable conditions; never a substitute for missing critical date or identity evidence. |

## 6. Temporal Authority Framework

Temporal authority requires separating multiple date concepts:

- observation date: date of the economic/market observation;
- event date: date an event occurred;
- effective date: date a record becomes economically or legally effective;
- announcement date: date a change was announced;
- publication date: date the source published the record;
- source availability date: date the project or a typical source user could obtain it;
- revision date: date the source changed a prior record;
- restatement date: date a value was restated;
- ingestion date: date Project Underdog ingested or registered evidence;
- extraction date: date a query, file, or snapshot was extracted;
- project-known date: date Project Underdog recorded the evidence as available for research.

Minimum date properties by role:

| role group | required temporal properties |
|---|---|
| Security identity and ticker lineage | effective start/end, as-of or source snapshot date, event effective/as-of dates for continuity events, extraction/project-known dates for lineage. |
| Listing, delisting, exchange history | listing/delisting/exchange effective dates, source availability or as-of dates, revision handling. |
| Classifications and economic context | classification effective dates or dated snapshots, taxonomy version date, publication/availability or conservative snapshot date. |
| Corporate events | event effective date, announcement or known date where relevant, source revision/correction dates. |
| Shares and size | value effective/observation date, publication/availability date or source snapshot date, restatement/revision dates. |
| Peer membership | all upstream identity, active-universe, classification, and size dates plus peer-construction project-known date. |

Conservative delay rules may be scientifically acceptable only when:

- the source has reproducible dated snapshots or releases;
- the lag is predeclared before empirical work;
- the lag is longer than the plausible reporting/release delay;
- missing exact availability dates do not differ systematically by security, event type, or outcome;
- the affected role can tolerate stale information without changing the claim.

Conservative delay remains inadequate when:

- the source overwrites history without versions;
- records may be retroactively inserted with unknown original availability;
- event or classification timing is central to the hypothesis;
- missing availability is correlated with distress, delisting, mergers, size, or peer membership;
- the delay rule would convert unknown historical facts into assumed authority.

This framework does not define executable PIT logic.

## 7. Revision And Restatement Authority

Revisions, corrections, overwrites, restatements, backfills, and retrospective classification changes directly affect authority because they determine whether Project Underdog can reconstruct what was knowable at the relevant time.

Required distinctions:

- Preserved history versus overwritten history: preserved versions can support reconstruction; overwritten-only history is fatal unless controlled snapshots exist.
- Versioned versus unversioned records: version ids support audit; unversioned records require external release or snapshot evidence.
- Corrected errors: corrections may improve accuracy but can destroy known-date validity if prior values and correction dates are not preserved.
- Retroactive classifications: may be valid for current taxonomy research but are not automatically valid for historical PIT peer research.
- Retrospective link changes: issuer/security link corrections must preserve old link, new link, revision date, and rationale.
- Revised shares: shares outstanding may be restated; size authority needs revision and availability semantics.
- Event corrections: event dates and predecessor/successor links require correction history.
- Schema reinterpretations: field meaning changes must be versioned and documented.

Minimum evidence:

- source revision policy;
- source version or snapshot id;
- correction/revision date fields where available;
- retained prior snapshot or controlled reference;
- derived metadata version used in any artifact;
- rule for whether research uses original-knowable, corrected-later, or explicitly delayed versions.

If historical information cannot be reconstructed as it was knowable, it cannot be authoritative for validation-quality PIT research.

## 8. Coverage And Missingness Authority

Coverage affects authority because missingness can create biased universes, false peer groups, and false negative or positive alpha evidence.

Coverage risks:

- missing securities;
- missing dates;
- missing delisted entities;
- missing classifications;
- partial exchange coverage;
- incomplete historical depth;
- selective corporate-event coverage;
- survivorship bias;
- size-related missingness;
- foreign-listing exclusions;
- changing source coverage through time.

Missingness can be governed when:

- it is measured by date, role, and universe segment;
- missing categories distinguish not covered, unknown, not applicable, withheld, and null;
- affected rows are blocked, downgraded, or scoped out before empirical work;
- scientific claims are narrowed to the covered domain;
- missingness is not materially related to the hypothesis outcome.

Missingness invalidates intended scientific use when:

- delisted or inactive entities are missing for universe/peer research;
- classification missingness is concentrated by sector, industry, size, distress, exchange, or event type;
- dates are missing for time-sensitive roles;
- missing rows are filled with static or current-state data;
- source coverage changes through time without date-level diagnostics.

## 9. Identity And Lineage Authority Requirements

Before Workstream 2 may begin substantive design, Workstream 1 requires a role-specific authority framework for:

- stable identifiers and their definitions;
- identifier reuse or deprecation;
- ticker reuse and exchange namespace;
- ticker changes with dated windows;
- company changes and name changes without false identity changes;
- issuer versus security identity;
- multiple share classes and primary-listing treatment;
- ADRs and foreign listings;
- mergers, acquisitions, spinoffs, split-offs, reorganizations, and relistings;
- temporary trading gaps and active/inactive status;
- delistings and terminal events.

Scientific prerequisites for Workstream 2:

- identity authority must be evaluated before classification and peer authority;
- ticker text must never override stable security identity;
- issuer continuity must not be inferred from name similarity alone;
- event-sensitive windows must fail closed when predecessor/successor, effective date, or source-known date is unresolved;
- manual overrides must be evidence-backed, retained, bounded, and prohibited from improving alpha results.

This section does not construct identity or lineage records.

## 10. Source Conflict Science

When credible external sources disagree, Project Underdog should reason by role, evidence strength, temporal semantics, and scientific consequence.

Conflict types:

- source-role precedence conflict: one source is stronger for identity, another for classification;
- temporal disagreement: effective, publication, as-of, or revision dates differ;
- identity disagreement: stable id, ticker window, issuer link, or share class differs;
- classification disagreement: sector/industry/taxonomy membership differs;
- corporate-event disagreement: event date, event type, predecessor/successor, or continuity differs;
- coverage disagreement: one source includes inactive or foreign-listed securities that another omits;
- revision disagreement: one source preserves historical state while another overwrites;
- methodological disagreement: definitions differ even when labels are similar.

Conflict outcomes:

- Resolvable conflict: stronger role-specific evidence and date semantics support one record; conflict is logged.
- Conditionally tolerable conflict: disagreement is outside the intended role, date range, or affected universe, and blocked/fallback rules are explicit.
- Diagnostic conflict: disagreement is useful evidence of uncertainty but cannot support authoritative use.
- Fatal conflict: material disagreement affects the intended role and cannot be resolved through documented authority hierarchy; affected role/date/security must be rejected or diagnostic-only.

This framework does not define vendor priorities or production resolution code.

## 11. Diagnostic Versus Authoritative Use

| use level | permitted conclusions | prohibited conclusions |
|---|---|---|
| Exploratory reference | Generate questions, identify possible fields, inspect concepts. | Authority, PIT validity, empirical support. |
| Diagnostic enrichment | Describe current/static exposure, coverage, missingness, or sanity checks. | Historical alpha claims, validation claims, peer-relative evidence. |
| Hypothesis inspiration | Suggest future source-independent scientific questions. | Candidate approval, formula readiness, source acceptance. |
| Provisional comparison | Compare against alternative labels or sources as uncertainty evidence. | Choosing an authoritative record without source-role decision. |
| Synthetic-fixture support | Test source-gate or PIT logic on artificial cases. | Real-world source acceptance or empirical conclusions. |
| Authoritative research input | Support defined role after evidence-backed acceptance. | Use outside accepted role, date range, universe, or conditions. |
| Validation input | Support validation only after authoritative role, reproducibility, and artifact lineage are accepted. | Validation from diagnostic/static/current-state data. |
| Production input | Out of scope here; would require separate governance beyond research authority. | Any production use from this task. |

Static or current-state metadata must not silently become authoritative PIT evidence. The current static economic metadata layer remains diagnostic-only, even when coverage is high.

## 12. Reproducibility And Retention As Scientific Authority

A source cannot be scientifically authoritative for validation-quality PIT research if its historical evidence cannot be preserved or reconstructed.

Required reproducibility concepts:

- immutable raw snapshots where allowed;
- source versions or controlled references when raw retention is restricted;
- extraction/query records;
- checksums, row counts, or approved substitutes;
- official schema documentation and source definitions;
- controlled references to restricted evidence;
- derived metadata lineage and normalization rules;
- query preservation and parameter records;
- post-access reproducibility plan;
- public-versus-private artifact boundaries.

Distinctions:

- Source accuracy means the source may describe facts correctly.
- Scientific authority means Project Underdog can rely on those facts for a defined role with evidenced semantics and reproducibility.
- Operational accessibility means the source can be accessed or queried.
- Long-term reproducibility means future reviewers can reconstruct or audit the evidence state after access, versions, or licenses change.

Restricted raw data may still support authority only if controlled references, source versions, row counts, permitted hashes or substitute checks, documentation references, and retained decision records are sufficient for future audit.

## 13. Scientific Authority Acceptance Framework

Future source-role decisions should evaluate each role separately across:

- provenance sufficiency;
- temporal sufficiency;
- identity sufficiency;
- historical sufficiency;
- revision sufficiency;
- coverage sufficiency;
- reproducibility sufficiency;
- auditability sufficiency;
- scientific-use fitness.

Decision outcomes:

| outcome | meaning |
|---|---|
| `AUTHORITATIVE_FOR_DEFINED_ROLE` | Evidence is sufficient for the specified role, date range, universe, and use level. |
| `CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE` | Evidence is sufficient only under explicit machine-readable conditions, blocked domains, or date ranges. |
| `DIAGNOSTIC_ONLY` | Useful for inspection, enrichment, or comparison but not authoritative research input. |
| `INSUFFICIENT_EVIDENCE` | Authority cannot be decided with current repository evidence. |
| `REJECTED_FOR_DEFINED_ROLE` | Evidence fails a fatal condition for the role. |

No outcome is applied to a real source in this task.

## 14. Fail-Closed Conditions

The following conditions must force rejection or diagnostic-only use for the affected role:

- unknown effective dates where effective dating is required;
- unknown availability, publication, or source-known dates where known-date authority is required;
- current classifications applied historically;
- unresolved ticker reuse;
- missing delisted securities in identity, universe, peer, or validation roles;
- untraceable company-security mappings;
- retrospective peer assignment without knowable historical inputs;
- overwritten historical records without preserved versions or controlled snapshots;
- irreproducible extracts;
- undocumented revisions;
- silent source fallback;
- insufficient role-specific coverage;
- authority conflicts without resolution;
- static snapshot-only PIT quality for historical use;
- future-dated records relative to signal date;
- missing as-of/source snapshot date for a historical row;
- unresolved event lineage for mergers, spinoffs, reorganizations, relistings, or delistings;
- manual overrides without retained dated evidence;
- manual overrides dominant enough to define the dataset rather than repair bounded exceptions;
- source status `manual_review_required`, `diagnostic_only`, `rejected`, or `deprecated` for construction/authoritative use;
- conditional source use outside accepted scope.

## 15. Authority Decision Artifact Requirements

Before any future source-role acceptance decision, the scientific artifact set should include:

- source-role assessment;
- evidence matrix;
- temporal-semantics assessment;
- coverage assessment;
- revision/restatement assessment;
- identity and lineage assessment where applicable;
- conflict assessment;
- reproducibility and retention assessment;
- contamination assessment;
- null and missingness assessment;
- open-assumption register;
- rejection or diagnostic-only record where applicable;
- governance decision record;
- source-role limitation statement;
- public/private artifact boundary statement;
- affected-workstream dependency statement.

These are conceptual artifact requirements only. This note creates no vendor records, licensed evidence, implementation files, source connectors, or source-specific manifests.

## 16. Relationship To Later Phase 5 Workstreams

| workstream | enabled conceptually | remains blocked until authority evidence exists |
|---|---|---|
| WS2 PIT Identity And Lineage Science | May begin conceptual requirements for identity, ticker lineage, events, and false-continuity risks. | Substantive source-specific design, source acceptance, identity construction, ticker lineage construction. |
| WS3 Economic Context Validity Science | May define what PIT-valid sector, industry, size, listing, and classification context means. | Historical classifications, size panels, economic metadata construction. |
| WS4 Peer-Relative Hypothesis Science | May frame source-agnostic hypotheses and falsification expectations. | Peer groups, formulas, panels, IC, validation. |
| WS5 External-Information Contamination And Orthogonality Science | May define contamination maps and diagnostic boundaries. | Claims that external context is independent information. |
| WS6 Negative Evidence And Falsification Science | May record rejected roles, blocked semantics, and authority failures. | Empirical rejection of real source roles without evidence intake. |
| WS7 Existing-Family Reinterpretation Science | May identify which existing OHLCV conclusions could later be reinterpreted. | Actual reinterpretation using external metadata. |
| WS8 Integrated Scientific Information Inventory | May design inventory categories: accepted, conditional, diagnostic, rejected, unknown. | Populating accepted external information inventory with real sources. |
| WS9 ML Readiness Science | May define why ML remains deferred and what authority would be needed. | ML features, ML experiments, feature stores, model validation. |

Workstream 2 is enabled at a conceptual level because this note defines the authority dimensions and fail-closed conditions that identity and lineage science must satisfy before any later construction can be considered.

## 17. Open Scientific Questions

| question | why it matters | affected workstream | current repository evidence | required future evidence |
|---|---|---|---|---|
| Is publication-date evidence always necessary? | Some roles may need knowability, not merely effective date. | WS1, WS2, WS3, WS4 | PIT notes identify publication/known-date semantics as blockers. | Official source date semantics and role-specific known-date analysis. |
| Can conservative lagging substitute for missing availability dates? | Lagging may reduce look-ahead but can hide retroactive insertion. | WS1, WS3, WS4 | Prior notes allow conservative snapshot fallback only as unresolved concept. | Source release cadence, revision behavior, empirical delay distribution, predeclared lag policy. |
| How much historical incompleteness is acceptable? | Missingness may bias peer groups or universe membership. | WS2, WS3, WS4, WS8 | Coverage diagnostics exist for static metadata, not PIT coverage. | Date-level coverage, inactive/delisted coverage, missingness by sector/size/event. |
| Can role-specific authority rely on multiple complementary sources? | Peer authority may require identity from one role and classification from another. | WS1, WS2, WS3, WS8 | Source hierarchy notes separate authority by domain. | Conflict rules, source-role precedence, reproducible multi-source lineage. |
| How does authority change after source revisions? | Corrected history may differ from original knowable history. | WS1, WS7, WS8 | Revision/restatement is identified as a blocker. | Versioned source snapshots, revision dates, correction policy, artifact version rules. |
| Can reproducibility be maintained with restricted raw data? | License constraints may prevent raw retention. | WS1, WS8, WS9 | Retention and archive policy are unresolved blockers. | Approved controlled-reference strategy, permitted hashes/row counts, private artifact policy. |
| How should conflicting authoritative records affect peer construction? | Peer groups are derived and can be invalidated by classification or identity conflicts. | WS3, WS4, WS5 | Existing notes say unresolved conflicts block. | Role-specific conflict examples, peer missingness impact, blocked/fallback rules. |
| When is inferred-window authority scientifically acceptable? | Some sources may provide snapshots rather than effective windows. | WS2, WS3 | Source-gate policy allows inferred windows with penalties and stale blocking. | Snapshot cadence evidence, conflict checks, stale-age distribution, confidence calibration. |
| Can manually curated evidence ever be authoritative? | Manual records may repair sparse issues but create drift and unreproducibility. | WS1, WS2, WS6 | Manual overrides are bounded and blocked when unsupported or dominant. | Dated retained evidence, reviewer records, override dominance diagnostics, expiration policy. |
| What level of null transparency is enough? | Nulls can mean unknown, not applicable, not covered, or withheld. | WS3, WS4, WS8 | Static metadata checks report missingness, but PIT null semantics are not available. | Official null definitions and role-specific missingness reports. |

## 18. Recommended Next Scientific Step

Recommended next Project Underdog lifecycle step:

`Project Underdog - Phase 5 Workstream 2 PIT Identity And Lineage Science v1`

Scope:

- conceptual scientific requirements only;
- define stable identity, ticker lineage, issuer/security continuity, listing/delisting, event-continuity, and false-continuity requirements using this authority framework;
- preserve all source, access, implementation, construction, peer, formula, panel, IC, validation, governance, production, threshold, and ML blocks.

Rationale:

Workstream 2 is the first downstream science dependency. Security identity and ticker lineage are prerequisites for economic-context validity, peer membership, contamination review, integrated inventory, and any later ML-readiness analysis. Beginning it conceptually advances the Phase 5 roadmap without requiring source access or implementation.

## Conclusion

Final classification: `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`

Project Underdog can now define what must be known, demonstrated, preserved, and governed before external information may become authoritative scientific evidence. Authority is role-specific, temporally governed, identity-safe, reproducible or reconstructable, auditable, coverage-aware, revision-aware, and fail-closed. No external source is currently accepted as authoritative for Phase 5 empirical research, static/current-state metadata remains diagnostic-only, and no implementation is authorized by this task.

Recommended next scientific step: `Project Underdog - Phase 5 Workstream 2 PIT Identity And Lineage Science v1`.

## Verification And Boundary Check

Repository searches and checks used:

- `rg --files docs/research_notes | rg 'project_underdog_(strategic_program_reassessment|phase5_external_information_integration_program|phase5_scientific_research_roadmap)|platform_v2|source_gate|pit_|security_master|ticker|lineage|peer|economic_context|reproducibility|artifact|contamination|frozen|candidate_registry|negative|external|crsp|metadata_source|manual_metadata|identity'`
- `rg -n 'PROJECT_READY_FOR_NEXT_MAJOR_PHASE|PHASE_5_PROGRAM_DEFINED|PHASE_5_SCIENTIFIC_ROADMAP_DEFINED|External Information Authority|Platform v2|source[- ]gate|PIT|point-in-time|ticker lineage|security identity|peer-relative|economic context|reproducibility|artifact lineage|contamination|frozen horizon|candidate registry|negative evidence|external source|authoritative|diagnostic-only|diagnostic only|ML remains deferred|Broad OHLCV' docs src`
- Direct review of the Phase 5 program and roadmap, strategic reassessment, Platform v2 standard, PIT closeout, PIT evidence intake review, source-gate policy/scaffold/semantic validation notes, economic-context readiness notes, static metadata notes, validation artifact contract, negative-result review, and candidate-registry authority note.

Boundary verification:

- No institution or vendor was contacted.
- No acquisition path was selected.
- No external access, data retrieval, source ingestion, connector creation, PIT construction, security-master construction, ticker-lineage construction, peer construction, formula design, candidate assignment, panel generation, IC computation, validation, governance change, production change, threshold change, survivor-status change, or ML work was performed.
