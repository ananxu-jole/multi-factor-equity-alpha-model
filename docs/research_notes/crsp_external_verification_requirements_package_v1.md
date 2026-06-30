# Project Underdog - CRSP External Verification Requirements Package v1

## SECTION 1 - Executive Summary

Project Underdog's CRSP-backed Security Master and Ticker Lineage PIT program is currently classified as `ASSUMPTIONS_PARTIALLY_VERIFIED`. Internal planning, architecture design, implementation specification, scaffold implementation, assumption verification design, assumption verification scaffold, post-scaffold review, and the first documentary assumption verification execution are complete.

Current readiness:

- The implementation architecture is defined at a planning level.
- The scaffold and verification controls are present.
- Public documentation supports CRSP as a plausible source category for security identity and ticker lineage work.
- No assumption is fully verified.
- External evidence is required before the project can move beyond the current planning boundary.

Verified assumptions:

- None.

Partially verified assumptions:

- `crsp_subscription_scope`: public product documentation supports broad CRSP fit, but local entitlement is unconfirmed.
- `crsp_field_availability`: public documentation supports broad field expectations, but exact field availability is unconfirmed.
- `crsp_event_date_semantics`: public documentation supports event/corporate-action plausibility, but field-level event-date mapping is unconfirmed.
- `crsp_ticker_window_semantics`: public identifier/product descriptions support ticker-lineage plausibility, but ticker-window fields and reuse controls are unconfirmed.

Unresolved blockers:

- Subscription entitlement confirmation.
- Licensing rights.
- Retention policy.
- Archival policy.
- Source-file hashing feasibility.
- Source-file reproducibility.
- Release/version tracking.
- Known-date semantics.
- Exact field availability.
- Source-gate eligibility confirmation.

Objective of this package:

Freeze the complete external evidence requirement set needed to move from assumption-bound planning to evidence-backed implementation design readiness.

Final classification: `EXTERNAL_VERIFICATION_REQUIRED`.

This package does not authorize CRSP access, source loading, ingestion, metadata construction, lineage construction, reconstruction, discovery, validation, governance mutation, production registration, or ML.

## SECTION 2 - Remaining Blocker Inventory

| blocker | current status | why unresolved | downstream impact | risk level |
| --- | --- | --- | --- | --- |
| Subscription scope | Partially verified | Public CRSP descriptions do not prove Project Underdog's actual subscription products, files, date ranges, modules, or documentation access. | Blocks source loading, implementation design finalization, schema mapping, and source-gate advancement. | Critical |
| Licensing rights | Blocked | No institutional license, usage policy, or compliance summary has been reviewed. | Blocks source access, retention, derived artifact use, source acceptance, metadata construction, and lineage construction. | Critical |
| Retention policy | Blocked | No evidence confirms whether raw files, source references, hashes, row counts, derived metadata, or review notes may be retained. | Blocks archive/hash design, reproducibility, source-lineage auditability, and source acceptance. | Critical |
| Archival policy | Blocked | No evidence confirms whether source archives, controlled references, redacted references, or source-bundle records are permitted. | Blocks `metadata_source_lineage`, reproducible rebuilds, and source-gate acceptance. | Critical |
| Source-file hashing feasibility | Blocked | No evidence confirms whether direct file hashes, bundle hashes, or controlled reference hashes are permitted and feasible. | Blocks source-file traceability, row-count reconciliation, and reproducibility diagnostics. | Critical |
| Release/version tracking | Unverified | Public documentation reviewed does not define a Project Underdog-ready release id, extract id, snapshot date, or versioning rule. | Blocks `source_version`, `source_snapshot_date`, source lineage, known-date fallback, and source acceptance. | High |
| Known-date semantics | Unverified | No evidence confirms event-level known dates or a conservative release/snapshot-date fallback. | Blocks PIT safety, look-ahead controls, historical metadata use, and downstream validation eligibility. | Critical |
| Exact field availability | Partially verified | Public documentation supports broad field expectations but not exact columns, data dictionaries, schema names, or required lineage fields. | Blocks schema alignment, implementation specification finalization, metadata construction, and lineage construction. | Critical |
| Event-date and ticker-window field details | Partially verified | Product-level evidence supports plausibility but not precise event-date, ticker start/end, exchange/listing, share-class, or reuse fields. | Blocks ticker lineage, event lineage, ambiguity controls, and confidence diagnostics. | Critical |
| Source-gate eligibility confirmation | Blocked | Source status cannot advance without subscription, license, retention, field, date, reproducibility, and allowed-use evidence. | Blocks all work beyond diagnostics and planning. | Critical |

## SECTION 3 - Evidence Requirement Matrix

| blocker | required evidence | acceptable evidence source | minimum evidence quality | verification owner | verification method | expected outcome |
| --- | --- | --- | --- | --- | --- | --- |
| Subscription scope | Entitlement summary naming available CRSP products, modules/files/tables, date ranges, documentation access, and delivery format. | Institutional subscription documentation, CRSP support communication, official product entitlement summary. | Direct evidence tied to the actual institution/account. | User or institutional data administrator. | Document review and entitlement checklist completion. | Confirm whether required CRSP scope exists or identify missing modules. |
| Licensing rights | Terms covering research use, derived metadata, audit artifacts, documentation references, and redistribution restrictions. | Institutional license agreement, legal/compliance summary, CRSP support/legal clarification. | Direct license/legal evidence, not public marketing material. | User, legal/compliance owner, or data administrator. | License review against Project Underdog allowed-use checklist. | Determine allowed use and blocked uses. |
| Retention policy | Permission status for raw files, source references, hashes, checksums, row counts, derived metadata, and review notes. | License terms, institutional retention policy, compliance memo, CRSP clarification. | Direct retention policy evidence. | Legal/compliance owner or data administrator. | Retention matrix review. | Determine whether source archive, hashes, and audit records may be retained. |
| Archival policy | Approved archive or controlled-reference approach for CRSP source materials. | Institutional archive policy, license-compatible source-reference plan, compliance approval. | Written policy or approval tied to CRSP data. | Data administrator and compliance owner. | Archive feasibility review. | Select archive, hash, controlled-reference, or blocked strategy. |
| Source-file hashing feasibility | Evidence that direct hashes, bundle hashes, or controlled reference identifiers are permitted. | License/legal confirmation, file manifest policy, CRSP support clarification. | Explicit permission or explicit prohibition. | Data administrator and compliance owner. | Hash feasibility checklist. | Define reproducibility strategy or keep source loading blocked. |
| Release/version tracking | Release identifiers, snapshot dates, extract dates, file production dates, or product-version documentation. | Official release documentation, CRSP data dictionary, institutional extract process documentation, CRSP support clarification. | Official or account-specific release/version evidence. | Data administrator or CRSP documentation reviewer. | Release/version mapping review. | Define deterministic `source_version` and `source_snapshot_date`. |
| Known-date semantics | Evidence for event known dates or conservative release/snapshot-date fallback. | Official CRSP documentation, data dictionary, release documentation, CRSP support clarification. | Explicit date-semantics evidence. | PIT metadata reviewer and data administrator. | Date-semantics review. | Define `as_of_date` and `event_as_of_date` rules or block PIT use. |
| Exact field availability | Field inventory for identity, ticker, exchange, name, security type, delisting, corporate actions, dates, and source metadata. | Official data dictionary, official documentation, future authorized schema inspection. | Official data dictionary or controlled schema evidence. | Data administrator and implementation reviewer. | Field inventory checklist. | Confirm mappings or mark missing fields. |
| Event-date and ticker-window field details | Fields for event dates, delisting dates, action codes, ticker dates, exchange/listing context, share classes, and ticker reuse behavior. | Official data dictionary, official documentation, CRSP support clarification, future authorized schema inspection. | Official documentation or controlled schema evidence. | Data administrator and ticker-lineage reviewer. | Event/ticker-window field review. | Confirm ticker-lineage feasibility and blockers. |
| Source-gate eligibility confirmation | Completed evidence-backed source-gate manifest, allowed-use review, confidence notes, manual-review disposition, and blocked reason report. | Project source-gate artifacts populated from external evidence. | Evidence-backed internal decision package. | Project reviewer after external evidence collection. | Source-gate review. | Keep blocked, classify conditional, or allow deeper loading-design review. |

## SECTION 4 - Evidence Source Classification

| required item | public documentation | institutional subscription information | license/legal confirmation | dataset inspection | vendor clarification |
| --- | --- | --- | --- | --- | --- |
| Subscription scope | Supportive only | Required | Optional | Optional future | Optional or required if entitlement unclear |
| Licensing rights | Insufficient | Optional | Required | Not sufficient | Optional or required |
| Retention policy | Insufficient | Optional | Required | Not sufficient | Optional or required |
| Archival policy | Insufficient | Optional | Required | Optional future | Optional or required |
| Source-file hashing feasibility | Insufficient | Optional | Required | Optional future | Optional or required |
| Release/version tracking | Supportive only | Required if extract-specific | Optional | Future only if authorized | Optional or required |
| Known-date semantics | Supportive only | Optional | Optional | Future only if authorized | Required if documentation is ambiguous |
| Exact field availability | Supportive only | Optional | Optional | Future only if authorized | Optional |
| Event-date and ticker-window fields | Supportive only | Optional | Optional | Future only if authorized | Optional or required |
| Source-gate eligibility | Not sufficient | Required input | Required input | Not required for first eligibility update | Optional |

Dataset inspection is future-only. It must not occur until subscription, license, retention, archive/hash, and source-access controls are externally verified.

## SECTION 5 - Verification Priority

| priority | items | rationale |
| --- | --- | --- |
| Critical | Licensing rights, retention policy, subscription scope, archival policy, source-file hashing feasibility, known-date semantics, exact field availability, source-gate eligibility. | These directly determine whether source access, source loading design, PIT safety, reproducibility, and source-gate advancement can proceed. |
| High | Release/version tracking, event-date field details, ticker-window field details, source-file reproducibility. | These are required for deterministic source lineage and trustworthy ticker/security lineage design. |
| Medium | Vendor clarification for ambiguous field semantics or controlled-reference alternatives. | Needed only if official documentation and institutional evidence do not resolve the question. |
| Low | Public documentation refresh. | Public evidence already supports broad plausibility; remaining blockers require account-specific, legal, vendor, or data-dictionary evidence. |

The first external verification pass should prioritize license/retention and subscription entitlement evidence. Without those, future schema inspection and source loading design remain blocked.

## SECTION 6 - Decision Gates

| blocker | blocks implementation design? | blocks source loading? | blocks ingestion? | blocks metadata construction? | blocks lineage construction? | blocks production use? |
| --- | --- | --- | --- | --- | --- | --- |
| Subscription scope | Yes, beyond assumption-bound design | Yes | Yes | Yes | Yes | Yes |
| Licensing rights | Yes | Yes | Yes | Yes | Yes | Yes |
| Retention policy | Yes | Yes | Yes | Yes | Yes | Yes |
| Archival policy | Yes | Yes | Yes | Yes | Yes | Yes |
| Source-file hashing feasibility | Yes | Yes | Yes | Yes | Yes | Yes |
| Release/version tracking | Yes | Yes | Yes | Yes | Yes | Yes |
| Known-date semantics | Yes | Yes | Yes | Yes | Yes | Yes |
| Exact field availability | Yes | Yes | Yes | Yes | Yes | Yes |
| Event-date and ticker-window details | Yes for ticker-lineage design | Yes | Yes | Yes | Yes | Yes |
| Source-gate eligibility confirmation | Yes | Yes | Yes | Yes | Yes | Yes |

Current gate result:

- Implementation design may continue only as external-evidence planning.
- Source loading is blocked.
- Ingestion is blocked.
- Metadata construction is blocked.
- Lineage construction is blocked.
- Production use is blocked.

## SECTION 7 - Exit Criteria

To advance from `ASSUMPTIONS_PARTIALLY_VERIFIED` to `ASSUMPTIONS_VERIFIED_FOR_IMPLEMENTATION_DESIGN`, all of the following must be true:

- Subscription scope is confirmed for the required CRSP products, files/tables, documentation, and date ranges.
- Licensing and retention rights are reviewed and documented.
- Archive/hash or controlled-reference strategy is confirmed as allowed or explicitly replaced by a documented compliant alternative.
- Release/version or snapshot/extract metadata rules are documented.
- Known-date or conservative source release/snapshot fallback semantics are documented.
- Required field availability is confirmed from official documentation or approved non-data schema evidence.
- Event-date and ticker-window field availability are confirmed at documentation level.
- Source-gate eligibility remains fail-closed but can be updated from evidence rather than placeholders.

To later advance from `ASSUMPTIONS_VERIFIED_FOR_IMPLEMENTATION_DESIGN` to `READY_FOR_SOURCE_LOADING_DESIGN`, all of the following must also be true:

- Source access is explicitly authorized under verified license/subscription controls.
- File/table inventory and source manifest requirements are defined.
- Source-file hash, controlled-reference, or archive policy is executable.
- No-ingestion and no-construction guardrails remain in place for source-loading design.
- Manual review resolves any remaining allowed-use or retention concerns.

Neither status authorizes ingestion. Neither status authorizes metadata construction, lineage construction, validation, production use, governance mutation, or ML.

## SECTION 8 - Deferred Work Register

The following work is intentionally deferred until external verification is complete:

- CRSP source access.
- CRSP source loading.
- CRSP file/table inspection.
- CRSP schema mapping from subscribed data.
- Field-level implementation.
- `security_master_pit` construction.
- `ticker_lineage_pit` construction.
- `metadata_source_lineage` construction from real CRSP evidence.
- Source-file hashing or archive creation.
- Ticker-window construction.
- Security identity continuity construction.
- Event lineage construction.
- Sector history reconstruction.
- Industry history reconstruction.
- Peer reconstruction.
- Alpha discovery.
- Refinement.
- Validation.
- Governance mutation.
- Production registration.
- ML.

## SECTION 9 - Project Pause Assessment

Project Underdog has reached the natural planning boundary for CRSP-backed Security Master and Ticker Lineage PIT work.

Reasoning:

- Internal architecture and scaffold design are complete.
- The first documentary verification pass exhausted what can be responsibly inferred from public documentation.
- Remaining blockers are external evidence questions, not design questions.
- Public documentation cannot prove local subscription entitlements, license rights, retention permissions, source-file hash feasibility, known-date semantics, release/version metadata, or exact field mappings.
- Proceeding without external evidence would convert assumptions into implementation risk.

Therefore the CRSP integration effort should pause at `EXTERNAL_VERIFICATION_REQUIRED` until user/institution/vendor evidence is available.

## SECTION 10 - Final Recommendation

1. Which remaining assumptions require external evidence?

Subscription scope, licensing rights, retention policy, archival policy, source-file hashing feasibility, release/version tracking, known-date semantics, exact field availability, event-date fields, ticker-window fields, source-file reproducibility, and source-gate eligibility all require external evidence.

2. Which require actual CRSP subscription access?

Subscription scope confirmation, official data dictionary access, exact field availability, release/version documentation, event-date field details, ticker-window field details, and any future schema inspection require CRSP subscription access or institutional documentation access. Dataset inspection remains future-only and unauthorized by this package.

3. Which require license confirmation?

Licensing rights, retention policy, archival policy, source-file hashing feasibility, derived metadata use, source-reference retention, row-count retention, documentation-reference retention, and source-file reproducibility require license/legal or compliance confirmation.

4. Which require future dataset inspection?

Exact source schema verification, file/table inventory, row-count policy, source-file manifest feasibility, field-level mapping, event-date mapping, ticker-window mapping, duplicate/reuse diagnostics, and source-file hash execution may require future dataset or schema inspection after source access is explicitly authorized. No dataset inspection is authorized now.

5. Has the planning phase reached a natural stopping point?

Yes. Project Underdog has completed the internal planning and public-documentary verification cycle. The remaining work cannot be resolved safely without external subscription, license, documentation, vendor, or future authorized schema evidence.

6. What should the next Codex task be once external evidence becomes available?

The next task should be **Project Underdog - CRSP External Evidence Intake Review v1**. It should review the provided subscription, license, retention, data dictionary, release/version, known-date, archive/hash, and source-gate evidence against this package. It should remain review-only unless a later explicit task authorizes scaffold patching or source-loading design. It should not access CRSP datasets, load source files, ingest data, construct metadata, build lineage, run validation, mutate governance, register production outputs, or implement ML.
