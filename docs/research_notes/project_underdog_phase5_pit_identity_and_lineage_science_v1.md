# Project Underdog - Phase 5 PIT Identity And Lineage Science v1

Date: 2026-07-14

Scientific workstream: `PIT Identity And Lineage Science`

Phase 5 roadmap position: Workstream 2

Final classification: `PIT_IDENTITY_AND_LINEAGE_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

This note defines the scientific identity and lineage framework required before Project Underdog may construct or use point-in-time security identity and lineage evidence. It is a scientific-framework artifact only. It is not a security-master implementation, ticker-lineage implementation, source-specific mapping design, database schema, source-selection exercise, vendor review, field-mapping task, data-construction task, source-ingestion task, peer-construction task, formula task, candidate task, panel task, IC task, validation task, governance mutation, production change, threshold change, survivor-status change, or ML task.

The classification applies only to the scientific framework. It does not imply source acceptance, identity construction, ticker-lineage construction, schema approval, field-mapping approval, PIT readiness, peer-group readiness, implementation authorization, or validation readiness.

## Repository Evidence Reviewed

Current authoritative state:

- `docs/research_notes/project_underdog_strategic_program_reassessment_v1.md`: final classification `PROJECT_READY_FOR_NEXT_MAJOR_PHASE`; broad OHLCV-only discovery is no longer the primary frontier; peer/economic context is blocked by authoritative PIT metadata requirements; ML remains deferred.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: final classification `PHASE_5_PROGRAM_DEFINED`; Phase 5 extends Platform v2 discipline to external information; security identity, ticker lineage, company-security lineage, and source authority are core prerequisites.
- `docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md`: final classification `PHASE_5_SCIENTIFIC_ROADMAP_DEFINED`; WS2 PIT Identity And Lineage Science follows WS1 and enables WS3 Economic Context Validity Science.
- `docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md`: final classification `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`; external information authority is role-specific; no source is accepted; identity authority must precede classification and peer authority.
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md` and `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`: hypothesis-first discipline, falsifiability, frozen expectations, lifecycle separation, contamination controls, and negative-evidence preservation remain governing scientific norms.

Identity, PIT, source-gate, and economic-context materials:

- `docs/research_notes/security_master_and_ticker_lineage_pit_design_review_v1.md`: identity before classification; stable security identity, ticker lineage, source lineage, blocked/eligible diagnostics, and fail-closed treatment are required before downstream sector, industry, size, or peer reconstruction.
- `docs/research_notes/security_master_and_ticker_lineage_pit_policy_and_vocab_design_v1.md`: source status, PIT quality, confidence floors, event types, blocked reasons, inferred-window policy, stale-age policy, and manual override rules were defined as implementation-oriented planning vocabulary.
- `docs/research_notes/security_master_and_ticker_lineage_pit_source_gate_scaffold_v1.md` and `docs/research_notes/source_gate_semantic_validation_implementation_v1.md`: source-gate scaffolds and semantic checks exist, but no real source rows, source acceptance, ingestion, metadata construction, security lineage, or ticker lineage exists.
- `docs/research_notes/pit_external_dependency_closeout_v1.md` and `docs/research_notes/pit_external_evidence_intake_review_v1.md`: PIT readiness remains blocked by external evidence, license/entitlement, official documentation, retention, archive, reproducibility, known-date, and source-gate gaps.
- `docs/research_notes/point_in_time_economic_metadata_source_and_lineage_design_v1.md` and `docs/research_notes/point_in_time_economic_context_readiness_audit_v1.md`: security and issuer identity must be authoritative before economic classifications, size context, peer groups, or candidate panels can be trusted.
- `docs/research_notes/peer_relative_economic_context_readiness_reassessment_and_scientific_program_framing_v1.md`: peer-relative work remains design-only and depends on PIT security identity, ticker lineage, listing history, corporate-action lineage, historical classification, and size context.
- Static metadata notes such as `docs/research_notes/manual_metadata_coverage_expansion_v3.md` and `docs/research_notes/metadata_source_lineage_consistency_review_v1.md`: useful descriptive diagnostics remain `STATIC_SNAPSHOT_RESEARCH_ONLY`.

Validation, contamination, registry authority, and reproducibility evidence:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`: validation-quality work requires scope control, manifests, checksums, artifact lineage, contamination artifacts, and fail-closed guardrail flags.
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`: negative evidence must be preserved and not rescued through post-hoc reinterpretation.
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry_implementation_v1.md`: a metadata surface can be authoritative for a bounded role without authorizing formulas, panels, IC, validation, production, or ML.
- `src/universe.py`: explicitly notes that fully survivorship-free testing requires historical constituent membership or a point-in-time security master.

Source-specific and superseded material:

- Prior source-specific notes, including source-candidate evaluations and external-verification packages, are treated only as evidence of requirement categories such as stable identifiers, ticker windows, delisting coverage, corporate-action evidence, known-date semantics, retention, and reproducibility. They do not rank, select, accept, or authorize any source in this workstream.
- Prior implementation architecture and schema notes remain useful as planning history, but this note does not approve schemas, fields, construction, mapping, or source-specific design.
- Static/current-state identity or classification evidence remains diagnostic-only unless later accepted through the external authority process.

## 1. Executive Scientific Classification

Final classification: `PIT_IDENTITY_AND_LINEAGE_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

Rationale:

- Repository evidence is sufficient to define a Project Underdog scientific framework for PIT identity and lineage.
- The framework can define identity types, lineage concepts, temporal requirements, ambiguity classes, failure conditions, acceptance logic, synthetic scenarios, and downstream constraints.
- Open gaps remain because no authoritative source is accepted, no real identity evidence has been reviewed, no historical identity records exist, and publication/availability, source-conflict, relisting, primary-security, share-class, ADR, and economic-company continuity questions remain unresolved.

This classification does not imply source acceptance, identity construction, ticker-lineage construction, schema approval, field-mapping approval, PIT readiness, peer-group readiness, implementation authorization, or validation readiness.

## 2. Scientific Meaning Of Identity

Identity is the scientifically defensible answer to "what object is this historical observation about?" A valid identity model prevents ticker-only, current-only, survivor-biased, and false-continuity joins from entering external-information research.

Identity types:

- Security identity: the tradable security as a continuing financial instrument with its own lifecycle, rights, listing relationships, and return history.
- Listing identity: the security's presence on a venue or exchange, including listing start/end, exchange namespace, and active/inactive state.
- Issuer identity: the entity that issued the security; one issuer may have multiple securities or share classes.
- Legal-entity identity: the legally incorporated entity, which may change through mergers, reincorporations, reorganizations, or name changes.
- Operating-company identity: the business operation whose assets, strategy, employees, and revenue activities generate economic exposure.
- Economic-company identity: the economically comparable company concept used for sector, industry, peer, size, and business-context reasoning.
- Ticker identity: a symbol label used by a venue or vendor for trading or reporting; it is not stable identity.
- Share-class identity: a class-specific security identity with distinct voting, liquidity, economic rights, or float.
- Instrument identity: the specific instrument type, such as common share, preferred share, ADR, warrant, right, tracking stock, or foreign ordinary.
- Research-universe identity: Project Underdog's research-eligible observation unit after applying identity, listing, activity, and role-specific eligibility constraints.

These identities must not be interchangeable. A ticker can change while security identity continues. A company can continue while one security delists. A legal entity can survive while operating economics change materially. An ADR and ordinary share can represent the same economic company but remain distinct securities. Peer-relative and economic-context research must know which identity level is being used, because each level has different temporal behavior and contamination risk.

## 3. Scientific Meaning Of Lineage

Lineage is a temporally ordered relationship among identity states. It explains how a security, listing, ticker, issuer, company, or research entity changes, continues, terminates, or transforms through time.

Lineage types:

- Identity continuity: the same security or entity persists across events.
- Ticker continuity: a symbol label persists or changes; ticker continuity alone is not identity continuity.
- Listing continuity: a listing remains active, migrates venue, suspends, delists, or relists.
- Company continuity: the operating or legal company remains substantially continuous.
- Economic continuity: the economic exposure remains sufficiently comparable for peer or context interpretation.
- Ownership continuity: rights to assets, cash flows, or residual claims continue or change.
- Successor/predecessor relationships: one identity state follows, absorbs, replaces, or descends from another.
- Transformation relationships: merger, spinoff, split-off, reorganization, reverse merger, or recapitalization changes identity relationships.
- Termination relationships: delisting, liquidation, acquisition, bankruptcy, or inactive state ends an identity or listing.

Continuity is valid when dated, role-specific evidence shows that the relevant identity level persists for the intended research use. Continuity is partial when some identity levels continue and others do not, such as same economic company but new security. Continuity is ambiguous when evidence is incomplete or sources conflict. Continuity is broken when the security, listing, issuer, or economic exposure terminates or transforms enough that historical observations cannot be safely joined as one object for the intended role.

## 4. Identity Hierarchy

| level | scientific purpose | temporal behavior | common ambiguity | contamination risk | downstream Phase 5 dependency |
|---|---|---|---|---|---|
| Source record | Evidence atom from an external source. | Versioned, revised, corrected, or overwritten. | Duplicate records, stale records, conflicting versions. | Treating source rows as facts without authority. | WS1, WS2, WS8. |
| Instrument | Define financial instrument type and rights. | Can be issued, converted, redeemed, expired, or delisted. | Common versus preferred, ADR, warrant, right, tracking stock. | Mixing non-comparable instruments in peer or return panels. | WS2, WS3, WS4. |
| Security | Anchor historical returns and metadata. | Continues through cosmetic changes but can terminate or transform. | Identifier changes, share classes, event continuity. | False joins and duplicate exposure. | WS2, WS3, WS4, WS5. |
| Listing | Determine venue-specific active eligibility. | Starts, migrates, suspends, delists, relists. | Venue migration versus new listing. | Survivorship and inactive-universe contamination. | WS2, WS3, WS4. |
| Ticker | Human/vendor label for trading. | Can change, recycle, overlap across venues, normalize differently. | Ticker reuse and suffix handling. | Current ticker backfill and wrong-security joins. | WS2, WS3, WS4. |
| Issuer | Link securities to issuing entity. | Can issue multiple securities and change legal structure. | Parent/subsidiary and share-class relationships. | Duplicate issuer exposure or wrong company link. | WS2, WS3, WS4. |
| Legal entity | Define incorporated entity. | Can merge, reincorporate, reorganize, liquidate. | Legal continuity versus economic break. | Misreading legal survival as economic continuity. | WS2, WS3, WS7. |
| Operating company | Define operating business. | Can divest, acquire, spin off, become shell, or transform. | Reverse mergers and shell transformations. | Peer labels reflect wrong business history. | WS3, WS4, WS7. |
| Economic company | Define peer/economic comparability. | Changes with business mix, taxonomy, size, and structure. | Conglomerates, tracking stocks, changed business model. | False peer groups and context leakage. | WS3, WS4, WS5. |
| Research entity | Define Project Underdog observation unit. | Derived from accepted identity and eligibility rules. | Multiple securities for one company or one security across events. | Panels overcount, omit, or merge exposures. | WS4, WS5, WS8, WS9. |

This is a conceptual hierarchy, not a database schema.

## 5. Temporal Identity Requirements

Identity evidence requires temporal properties that answer both "when did the relationship exist?" and "when could Project Underdog have known it?"

Required date concepts:

- identity start date: when the security/entity identity begins for the role;
- identity end date: when it ends or becomes inactive;
- relationship start date: when issuer-security, listing-security, ticker-security, predecessor-successor, or peer-relevant relation starts;
- relationship end date: when that relation ends;
- ticker effective date: when a ticker label becomes valid;
- listing effective date: when a listing becomes valid;
- delisting date: when listing or active status terminates;
- event date: when a transformation occurs;
- announcement date: when the event is announced;
- publication or availability date: when the source makes the identity fact knowable;
- revision date: when the source changes a prior identity fact;
- project-known date: when Project Underdog records the evidence;
- uncertainty interval: bounded date range when exact timing is unavailable.

Essential dates by role:

- Security identity: identity start/end, event dates, revision dates, source as-of or availability dates.
- Listing identity: listing effective date, suspension/delisting date, venue change date, source availability date.
- Ticker identity: ticker effective start/end, exchange namespace, source-known date, revision date for corrections.
- Issuer/company relationship: relationship start/end, event date for corporate transformations, source-known date.
- Terminal states: delisting/liquidation/acquisition/bankruptcy dates and source-known or publication dates.
- Peer/economic context readiness: all upstream identity, active-listing, issuer, classification, and size dates must be compatible before downstream use.

Uncertainty intervals can support diagnostic review or conditional acceptance only if they are bounded, retained, confidence-adjusted, and fail closed when they cross event-sensitive or signal-date boundaries. This note does not define executable PIT logic.

## 6. Ticker Science

Ticker is a label, not a stable identity. It is venue-specific, vendor-normalized, and historically mutable. It should help locate records only after identity is resolved through accepted security/listing evidence.

Ticker issues:

- Ticker changes: same security may receive a new symbol.
- Ticker reuse: a later unrelated company may use an old symbol.
- Simultaneous ticker use across exchanges: the same symbol can refer to different securities by venue.
- Temporary ticker changes: bankruptcy, reorganization, when-issued, or special status labels can appear briefly.
- Reserved or inactive tickers: a symbol may not correspond to an active eligible security.
- Recycled tickers: reuse across time must be separated by security identity and date windows.
- Class suffixes: ticker suffixes can encode share classes, but vendor normalization can erase them.
- Exchange-qualified tickers: exchange namespace is part of ticker interpretation.
- Relisted tickers: the same symbol can return after inactivity, sometimes for the same entity and sometimes not.
- Vendor-normalized tickers: normalized symbols may collapse dots, suffixes, exchanges, or special flags.

Fail-closed ticker ambiguity:

- unresolved ticker reuse;
- overlapping ticker windows without share-class or exchange explanation;
- ticker-date maps to multiple active securities without accepted disambiguation;
- ticker maps to a security after delisting without successor evidence;
- vendor-normalized ticker erases class or venue distinction;
- current ticker applied historically;
- missing ticker effective start where ticker is used for a historical join.

## 7. Security And Listing Continuity

Security or listing continuity may survive cosmetic changes but must not be assumed through scientifically meaningful breaks.

Usually cosmetic or non-breaking if documented:

- ticker changes;
- legal-name changes;
- company-name changes;
- stock splits and reverse splits where ownership continuity is preserved;
- identifier changes that are explicitly cross-referenced;
- exchange changes or venue migrations with continuous security evidence;
- temporary suspensions where same security later resumes;
- recapitalizations that preserve same security rights sufficiently for the intended role.

Potentially meaningful breaks or conditional cases:

- CUSIP or identifier changes without source cross-reference;
- reincorporations tied to mergers, domicile changes, or changed legal entity;
- recapitalizations that materially alter voting, economic rights, or share-class structure;
- venue migrations that terminate one listing and create another listing;
- suspensions followed by reorganization or relisting under uncertain continuity.

Minimum continuity evidence:

- stable security id or documented predecessor/successor relation;
- effective dates for old and new states;
- exchange/listing context;
- event type and source-known date where event-sensitive;
- confidence and conflict status;
- retained source lineage.

## 8. Company-Security Relationships

Companies and securities are related but not identical. Peer-relative and economic-context research often cares about the operating/economic company, while return panels observe securities.

Relevant relationship patterns:

- one company with multiple securities;
- one issuer with multiple share classes;
- parent-subsidiary relationships;
- tracking stocks with business-segment exposure;
- preferred shares with different rights from common equity;
- rights and warrants with derivative-like exposure;
- ADRs representing foreign ordinary shares;
- foreign ordinary shares listed or traded in different venues;
- dual listings of the same economic company;
- changing primary-security status.

Peer-relative and economic-context relevance:

- issuer-security links are required to avoid duplicate company exposure;
- share classes may need separate return identity but shared economic-company context;
- preferreds, warrants, rights, and tracking stocks may be unsuitable for common-equity peer comparisons unless explicitly scoped;
- ADRs and ordinary shares may share economic-company identity but differ as securities and listings;
- primary-security concepts affect duplicate exposure and market-cap/size interpretation, but must remain conceptual until accepted evidence exists.

## 9. Corporate Transformations

| transformation | predecessor-successor possibilities | continuity interpretations | contamination risks | minimum evidence required | fail-closed condition |
|---|---|---|---|---|---|
| Merger | One or more predecessors into survivor or new entity. | Security may terminate; issuer/economic company may partially continue. | False pre/post continuity; event leakage. | Event type, effective date, successor id, announcement/known date if used. | Successor or dates unresolved. |
| Acquisition | Acquired security ends or maps to acquirer. | Acquired company may cease as public security. | Treating acquired name as recoverable peer. | Acquired/acquirer ids, delisting date, consideration/effective event evidence if relevant. | Continued identity ambiguous. |
| Spinoff | Parent continues; child new security/entity begins. | Parent and child distinct securities; economic continuity split. | Child inherits parent history or peers incorrectly. | Parent/child ids, listing start, event date, relationship evidence. | Child/parent mapping unresolved. |
| Split-off | Parent and split-off identity separate. | New or separated exposure; parent may continue. | False shared history. | Event relation, effective dates, security ids. | Source cannot distinguish identities. |
| Divestiture | Operating-company economics change without necessarily changing security. | Security may continue; economic-company comparability may change. | Historical peer context becomes stale. | Event description, date, business effect if used. | Economic continuity required but unsupported. |
| Bankruptcy | Security may continue, suspend, delist, reorganize, or terminate. | Often terminal or discontinuous. | Distressed terminal state omitted; survivor bias. | Bankruptcy/event date, listing status, delisting or relisting evidence. | Terminal/reorganized state unresolved. |
| Reorganization | Predecessor may become successor through legal restructuring. | Continuity can be valid, partial, or broken. | Unjustified linking across new capital structure. | Plan/event evidence, effective date, successor/predecessor ids. | Rights/entity continuity unknown. |
| Reverse merger | Public shell and operating company combine. | Legal shell may continue; economic company often changes. | Shell history assigned to new operating company. | Shell/acquirer roles, effective date, operating-company change evidence. | Economic-company continuity ambiguous. |
| Take-private event | Public security terminates. | Company may continue privately; listed security ends. | Post-event public-market history invented. | Delisting date, acquisition/private status evidence. | Missing terminal listing state. |
| Relisting | Prior entity may re-enter public market or new entity may use old label. | Same economic company possible; same security not automatic. | Old security history joined to new listing incorrectly. | Same-entity evidence, delisting/relisting dates, new security/listing ids. | Same-entity continuity not proven. |
| Shell-company transformation | Legal listing remains; operating economics change. | Security/listing may continue, economic company breaks. | Peer/economic labels backfilled through shell period. | Business-change evidence, dates, identity roles. | Economic continuity required but unsupported. |
| Liquidation | Security and company rights wind down. | Terminal state. | Survivorship and missing terminal losses. | Liquidation/delisting dates, terminal status. | Missing final state. |

## 10. Delisting And Terminal-State Science

Delisting and terminal states determine when a security leaves the active research universe and prevent survivor-only histories.

Terminal-state cases:

- voluntary delisting;
- exchange delisting;
- acquisition-related delisting;
- bankruptcy;
- liquidation;
- migration to OTC;
- temporary suspension;
- missing final records;
- return after delisting.

Scientific requirements:

- delisting date or bounded terminal interval;
- active/inactive state before and after terminal event;
- delisting reason when it affects interpretation;
- successor/predecessor relation where applicable;
- source-known or publication date where event timing matters;
- policy for post-delisting returns or terminal observations if later empirical work uses returns.

Missing or mishandled terminal states create survivorship bias, false peer histories, invalid active-universe membership, and misleading repair/persistence interpretation. A company that disappeared, merged, liquidated, or migrated can otherwise be treated as if it remained a normal peer.

## 11. Share-Class Science

Multiple share classes can represent the same issuer or economic company while remaining distinct securities.

Issues:

- voting and non-voting classes;
- economically equivalent classes;
- materially different classes;
- class conversions;
- class consolidations;
- class-specific liquidity;
- class-specific market capitalization;
- duplicate economic exposure;
- primary-security selection.

Scientific approach:

- Treat each share class as a distinct security unless accepted evidence proves a combined research entity is appropriate for a defined role.
- Treat issuer/economic-company context as shared only when company-security relation evidence supports it.
- Treat liquidity, market cap, price behavior, and active eligibility as class-specific unless a future role-specific rule is accepted.
- Primary-security designation is a downstream research-entity concept, not a fact that can be assumed from current market convention.

No selection code or production policy is defined here.

## 12. ADR And Foreign-Listing Science

ADRs, foreign ordinary shares, and dual listings can share economic-company identity while remaining distinct securities and listings.

Issues:

- sponsored ADRs;
- unsponsored ADRs;
- foreign ordinary shares;
- dual-listed companies;
- depositary-ratio changes;
- home-market versus U.S.-listed instruments;
- currency differences;
- trading-hours differences;
- delisting of one venue while another remains active.

Scientific interpretation:

- Same economic company does not imply same security.
- ADR/listing identity must include instrument type, depositary ratio where relevant, venue, currency, active dates, and relationship to ordinary shares.
- Home-market and local listing evidence may be relevant to company context but cannot replace security/listing identity for U.S.-listed research observations.
- If one venue delists while another remains active, the listing identity ends while economic-company identity may continue.

Treat ADRs and ordinary shares as distinct securities unless a future accepted role explicitly permits economic-company aggregation for a bounded diagnostic or peer role.

## 13. Identity Ambiguity Taxonomy

| ambiguity class | scientific meaning | minimum evidence required | permitted use | prohibited use | downstream effect |
|---|---|---|---|---|---|
| Resolvable identity ambiguity | Initial uncertainty can be resolved by accepted evidence. | Dated source evidence, conflict log, confidence above role threshold. | Authoritative use after resolution. | Use before resolution. | Downstream may proceed for resolved window. |
| Conditionally resolvable ambiguity | Resolution works only for a scope/date/domain. | Machine-readable condition and blocked outside-scope rule. | Conditional use in scope. | Broad use or silent fallback. | WS3/WS4 inherit conditions. |
| Source-conflict ambiguity | Credible sources disagree. | Conflict assessment and role-specific evidence hierarchy. | Diagnostic or resolved use only. | Unlogged choice by convenience. | Affected rows block if unresolved. |
| Temporal ambiguity | Exact start/end/known date uncertain. | Bounded interval, inference method, confidence penalty. | Diagnostic or conditional if not event-sensitive. | Use across signal/event boundary. | Can block PIT context. |
| Entity-level ambiguity | Security, issuer, legal entity, or economic company relation unclear. | Relationship evidence and role statement. | Diagnostic or restricted role. | Peer/economic-company use. | Blocks WS3 substantive evidence. |
| Transformation ambiguity | Merger/spinoff/reorg/relisting continuity unclear. | Event records, predecessor/successor ids, dates. | Diagnostic event review. | Continuous history joins. | Blocks affected periods. |
| Ticker-reuse ambiguity | Same ticker may refer to different securities. | Exchange-qualified dated windows and stable ids. | None for authoritative ticker-date until resolved. | Historical joins by ticker. | Fatal for affected ticker windows. |
| Share-class ambiguity | Multiple classes may duplicate or diverge. | Class definitions, issuer relation, active windows, liquidity/economic rights if used. | Separate-security diagnostics. | Combined peer/security use. | Blocks duplicate-sensitive research entities. |
| Fatal ambiguity | Material uncertainty cannot be resolved for intended role. | Rejection rationale only. | Rejection/negative evidence. | Authoritative or conditional use. | Affected relationship rejected or quarantined. |

## 14. Identity And Lineage Evidence Hierarchy

| evidence type | scientific strength | allowed use |
|---|---|---|
| Authoritative role-specific source evidence | Very strong after WS1 acceptance. | Identity/lineage acceptance for defined role and scope. |
| Official event records | Strong to very strong. | Corporate transformation and terminal-state evidence, subject to date semantics. |
| Official listing records | Strong. | Listing, delisting, exchange, venue, and active-state support. |
| Official identifier history | Strong. | Identifier continuity and change evidence. |
| Official company-security links | Strong. | Issuer/security and company/security relationship evidence. |
| Source-provided historical relationships | Moderate to strong. | Role-specific lineage if definitions, dates, and revisions are documented. |
| Independent corroboration | Moderate. | Conflict diagnosis and confidence support; not sole authority where official evidence is required. |
| Current-state crosswalks | Diagnostic. | Exploratory matching and discrepancy review. |
| Manually curated mappings | Diagnostic or conditional. | Only with retained dated evidence, reviewer record, and bounded scope. |
| Inferred continuity | Weak to conditional. | Only with explicit inference method, confidence penalty, and fail-closed limits. |
| Heuristic matching | Weak. | Hypothesis generation and manual review queue only. |

## 15. Source-Conflict Handling

When credible identity sources disagree, the project must reason by role, dates, source authority, and downstream consequence rather than vendor precedence.

Conflict cases:

- ticker disagreement;
- identifier disagreement;
- company-link disagreement;
- listing-date disagreement;
- delisting-date disagreement;
- merger-successor disagreement;
- share-class disagreement;
- primary-security disagreement.

Decision outcomes:

- Resolved: accepted role-specific evidence supports one interpretation; conflict is logged.
- Conditionally accepted: one interpretation is accepted only for bounded dates, roles, securities, or use levels.
- Diagnostic-only: conflict is useful evidence but cannot support authoritative lineage.
- Quarantined: affected relationship is held out of downstream use pending evidence.
- Rejected: relationship fails identity or lineage requirements for the intended role.

No vendor precedence is defined.

## 16. Identity Acceptance Framework

Future identity or lineage relationships should be assessed across:

- provenance;
- temporal precision;
- role-specific authority;
- continuity logic;
- transformation logic;
- conflict status;
- coverage;
- reproducibility;
- downstream-use fitness.

Possible outcomes:

| outcome | meaning |
|---|---|
| `IDENTITY_RELATIONSHIP_ACCEPTED` | Evidence is sufficient for the relationship, role, date range, and downstream use. |
| `IDENTITY_RELATIONSHIP_CONDITIONALLY_ACCEPTED` | Evidence is sufficient only under explicit conditions. |
| `IDENTITY_RELATIONSHIP_DIAGNOSTIC_ONLY` | Relationship may support review or diagnostics but not authoritative PIT use. |
| `IDENTITY_RELATIONSHIP_QUARANTINED` | Relationship is withheld pending conflict or missing evidence resolution. |
| `IDENTITY_RELATIONSHIP_REJECTED` | Relationship fails a fatal scientific condition. |
| `INSUFFICIENT_EVIDENCE` | Current evidence cannot support a decision. |

No outcome is applied to real securities in this task.

## 17. Fail-Closed Conditions

Identity and lineage must fail closed under:

- unresolved ticker reuse;
- overlapping identity intervals without explanation;
- missing effective dates;
- future-known mappings;
- untraceable predecessor-successor links;
- missing delisting evidence for affected active-universe use;
- retrospective company assignment;
- unresolved multiple-share-class duplication;
- unsupported primary-security designation;
- overwritten history without preserved versions or controlled references;
- manual override without retained dated evidence;
- conflicting terminal states;
- identity relationships outside accepted source roles;
- source status that is manual-review, diagnostic-only, rejected, deprecated, or out of conditional scope;
- static/current-state identity evidence applied historically;
- missing source-known/as-of date where known-date authority is required;
- confidence below accepted role floor;
- event-dependent continuity with unresolved event type, date, or successor.

## 18. Synthetic Identity Scenarios

| scenario | setup | expected identity interpretation | expected lineage interpretation | ambiguity status | downstream restriction | fail-closed behavior |
|---|---|---|---|---|---|---|
| Simple ticker change | Security changes ticker A to B. | Same security if stable id and dates support it. | Ticker window closes/opens; security continues. | Resolvable. | Downstream may use after accepted dates. | Block if effective date missing. |
| Ticker reuse by new company | Ticker A used by old security, later by unrelated issuer. | Separate securities. | No continuity except symbol reuse. | Fatal until resolved. | No ticker-only joins. | Block reused ticker windows. |
| Merger with surviving ticker | Target merges into acquirer ticker. | Target security ends; acquirer may continue. | Predecessor/successor relation if evidenced. | Conditionally resolvable. | Block target post-event unless successor logic accepted. | Block if successor/date unknown. |
| Merger with new ticker | Two firms combine into new ticker. | Old securities end; new security begins. | Multiple predecessors to successor. | Transformation ambiguity until evidenced. | No continuous single-security history. | Quarantine affected relationships. |
| Spinoff | Parent continues, child lists. | Parent and child distinct securities. | Parent-child relationship, no inherited child return history. | Resolvable with event evidence. | Child peer history begins at accepted start. | Block child before listing start. |
| Bankruptcy and relisting | Security delists after bankruptcy, later symbol reappears. | Same security only if proven; otherwise new security/listing. | Terminal then possible successor/relisting. | High temporal/transformation ambiguity. | Block continuous repair/persistence claims. | Fail closed absent same-entity evidence. |
| Two share classes | Issuer has A and B shares. | Distinct securities, shared issuer if evidenced. | Parallel class relationships. | Share-class ambiguity. | Avoid duplicate company exposure unless governed. | Block primary selection if unsupported. |
| ADR plus ordinary share | ADR trades locally; ordinary trades abroad. | Same economic company, distinct securities/listings. | Depositary relationship if evidenced. | Conditionally resolvable. | Treat separately unless accepted aggregation role exists. | Block if ratio/identity unclear. |
| Exchange migration | Security moves exchange. | Security may continue; listing identity changes. | Old listing ends, new listing begins. | Resolvable with dates. | Venue-specific peer/listing checks need new window. | Block if venue overlap unexplained. |
| Temporary suspension | Security stops trading temporarily. | Security may continue; active listing pauses. | Suspension interval recorded. | Temporal ambiguity if dates missing. | Active universe excludes suspension if required. | Block missing active-status dates. |
| Company name change | Issuer changes name. | Security continues unless event says otherwise. | Name-history update. | Resolvable. | No peer/economic change inferred from name alone. | Block if name match used as sole identity evidence. |
| Reverse merger | Shell becomes operating company. | Legal/listing may continue; economic company may break. | Transformation relation with economic break. | Transformation ambiguity. | Block economic-company continuity unless evidenced. | Quarantine peer history across event. |
| Identifier correction | Source corrects id for prior record. | Depends on revision history. | Correction lineage needed. | Source-conflict or revision ambiguity. | Use metadata version explicitly. | Block if prior/current state not reproducible. |
| Overlapping source records | Two active records conflict for same ticker/date. | Unknown until source conflict resolved. | No accepted continuity. | Source-conflict ambiguity. | No downstream use for affected window. | Quarantine or reject affected relationship. |
| Missing delisting | Security disappears without terminal record. | Active state unknown after last evidence. | Termination relationship missing. | Temporal/terminal ambiguity. | No survivor-free universe claim. | Block post-last-known window. |
| Conflicting successor records | Event source names different successors. | Successor unknown. | Predecessor-successor relationship unresolved. | Fatal if material. | No merged continuity or successor joins. | Quarantine/reject successor relation. |

These scenarios are conceptual. No fixtures or tests are implemented.

## 19. Downstream Scientific Consequences

Identity and lineage quality affects:

- Universe construction: defines active, eligible securities without current-universe leakage.
- Survivorship control: preserves delisted, inactive, merged, bankrupt, or transformed securities.
- Historical classifications: prevents current sector/industry/company assignments from being joined to wrong historical securities.
- Peer membership: determines contemporaneous peers and avoids ticker-only or duplicate issuer peers.
- Market-cap and size context: ensures share class, listing, and issuer relationships are correct before size is interpreted.
- Corporate-event controls: identifies event-sensitive windows and terminal states.
- Relative repair measurement: separates idiosyncratic repair from peer-wide or survivor-only recovery.
- Relative persistence measurement: prevents continuity artifacts from appearing as persistent rank behavior.
- Validation: validation-quality panels require reproducible identity and lineage.
- Cross-sectional comparisons: wrong identity creates false ranks, duplicates, and omitted failures.
- Negative-evidence interpretation: failed ideas remain interpretable only if identity and universe are valid.
- Future ML readiness: ML remains deferred because identity errors would become leakage-prone features or labels.

## 20. Minimum Prerequisites For Workstream 3

Workstream 3 `Economic Context Validity Science` may proceed substantively once the following are clear at the scientific level.

Conceptual prerequisites that can be satisfied now:

- distinction among security, listing, ticker, issuer, legal entity, operating company, economic company, and research entity;
- lineage meanings for continuity, transformation, and termination;
- ambiguity taxonomy and fail-closed rules;
- synthetic scenario set for future acceptance-test design;
- recognition that identity precedes classification, size, and peer authority.

Prerequisites requiring future authoritative evidence:

- accepted source-role evidence for stable security identity;
- accepted ticker-lineage evidence with dated windows and ticker reuse handling;
- listing/delisting evidence with active/inactive coverage;
- company-security relationship evidence;
- corporate-transformation evidence and predecessor/successor semantics;
- reproducibility and retention evidence.

Prerequisites that block empirical work only:

- constructed security master;
- constructed ticker lineage;
- constructed company-security mappings;
- constructed PIT economic metadata;
- peer groups, panels, formulas, IC, validation.

Unresolved questions that may remain open while WS3 begins conceptually:

- exact primary-security concept;
- treatment of ADR/ordinary aggregation for future roles;
- tolerance for bounded temporal uncertainty;
- how share-class duplication should propagate into peer concepts;
- whether economic-company identity can be defined without accepted classification evidence.

## 21. Open Scientific Question Register

| question | why it matters | affected downstream workstream | current repository evidence | required future evidence |
|---|---|---|---|---|
| Should economic-company identity ever supersede security identity? | Peer context may compare companies, while returns are security-level. | WS3, WS4, WS7 | Notes require security identity before economic context. | Role-specific aggregation evidence and duplicate-exposure policy. |
| How should multiple concurrent listings be treated? | Same company can appear through multiple venues or instruments. | WS3, WS4 | Existing notes flag exchange namespace and ADR/foreign listing issues. | Listing/link evidence, venue scope, active coverage. |
| How is continuity defined after reorganizations? | Legal continuity may differ from economic or security continuity. | WS2, WS3, WS7 | Event lineage is required and unresolved event lineage blocks. | Official event and successor/predecessor evidence. |
| Do relisted securities retain prior lineage? | Relisting can be same entity or new security. | WS2, WS3 | Relisting is recognized as event-sensitive and blockable. | Same-entity evidence, delisting/relisting dates, source-known dates. |
| Does ticker reuse require permanent exclusion? | Reuse can be resolved with evidence, but unresolved reuse is fatal. | WS2, WS4 | Ticker reuse is a critical blocker. | Dated ticker windows, exchange namespace, stable ids. |
| How should primary security be conceptualized? | Peer and size research may need one security per company. | WS3, WS4 | Prior notes identify primary-security selection as required but unaccepted. | Accepted primary-listing evidence or governed conceptual rule. |
| How does share-class duplication affect peer membership? | Multiple classes can overcount same issuer or distort rank. | WS3, WS4 | Share-class distinction is a known requirement. | Class relationship, liquidity, market-cap, issuer-link evidence. |
| How should identity uncertainty propagate into validation? | Validation must not hide uncertain identity joins. | WS5, WS8, WS9 | Validation artifacts require lineage and fail-closed manifests. | Artifact rules carrying identity confidence and blocked rows. |
| Can manual identity corrections become authoritative? | Manual repair may be necessary but can become unreproducible. | WS2, WS6, WS8 | Manual overrides require dated evidence and dominance limits. | Retained evidence, reviewer records, expiration and dominance diagnostics. |
| What publication/availability date is enough for identity events? | Effective dates may be known only after the fact. | WS2, WS3 | Known-date semantics remain open in WS1. | Source date semantics and event-specific release evidence. |

## 22. Recommended Next Scientific Step

Recommended next Project Underdog lifecycle step:

`Project Underdog - Phase 5 Workstream 3 Economic Context Validity Science v1`

Scope:

- conceptual scientific requirements only;
- define what makes sector, industry, subindustry, classification-system history, size, market-cap, listing context, and economic-company context point-in-time valid;
- consume this identity/lineage framework as a prerequisite;
- preserve all source, access, implementation, construction, peer, formula, candidate, panel, IC, validation, governance, production, threshold, survivor-status, and ML blocks.

Rationale:

Workstream 3 is the next step in the Phase 5 roadmap. WS2 has defined the identity and lineage science needed to frame economic-context validity without constructing identity records. WS3 can now proceed conceptually while empirical work remains blocked until future authoritative evidence and separate authorization exist.

## Conclusion

Final classification: `PIT_IDENTITY_AND_LINEAGE_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

Project Underdog can now define the scientific identity model, lineage concepts, temporal requirements, ambiguity taxonomy, fail-closed conditions, acceptance outcomes, synthetic scenarios, and downstream constraints required before point-in-time identity and lineage evidence may support external economic-context or peer-relative research. The framework preserves the current state: no source is accepted as authoritative, no identity or lineage construction is authorized, static/current-state identity evidence remains diagnostic-only unless later accepted, and ML remains deferred.

Recommended next scientific step: `Project Underdog - Phase 5 Workstream 3 Economic Context Validity Science v1`.

## Verification And Boundary Check

Repository searches and checks used:

- `rg -n 'PIT Identity|Identity And Lineage|security identity|ticker lineage|issuer|company-security|share class|ADR|delisting|survivorship|corporate action|predecessor|successor|relisted|relisting|ticker reuse|primary security|Platform v2|frozen horizon|contamination|reproducibility|registry authority|candidate registry|source-gate|source gate' docs/research_notes src`
- Direct review of `project_underdog_phase5_external_information_authority_science_v1.md`, Phase 5 roadmap and program notes, strategic reassessment, source-gate semantic implementation, security-master/ticker-lineage design and vocabulary notes, PIT evidence intake and closeout notes, point-in-time economic metadata source/lineage design, peer-relative readiness, static metadata notes, validation artifact contract, negative-result review, and candidate-registry authority note.

Boundary verification:

- No institution or vendor was contacted.
- No source or acquisition path was selected.
- No access, data retrieval, proprietary documentation retrieval, source inspection, source query, connector creation, implementation, security-master construction, ticker-lineage construction, company-security mapping, PIT construction, peer construction, formula definition, candidate assignment, panel generation, IC calculation, validation, governance change, architecture change, production change, threshold change, survivor-status change, or ML work was performed.
