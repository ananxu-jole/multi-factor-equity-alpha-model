# Project Underdog - CRSP External Evidence Verification v1

## SECTION 1 - Executive Summary

This note attempted to verify the remaining CRSP implementation assumptions using external evidence. The review used the existing Project Underdog CRSP verification package, the prior assumption verification execution, the implementation design, the implementation specification, and publicly available CRSP product-level documentation.

No CRSP datasets were accessed. No CRSP files were loaded. No subscribed datasets were inspected. No source data was ingested. No metadata was constructed. No security lineage or ticker lineage was built. No discovery, refinement, validation, governance mutation, production registration, or ML work was performed.

Evidence reviewed:

- `docs/research_notes/crsp_external_verification_requirements_package_v1.md`
- `docs/research_notes/crsp_assumption_verification_execution_v1.md`
- `docs/research_notes/crsp_security_master_ticker_lineage_implementation_specification_v1.md`
- `docs/research_notes/crsp_security_master_ticker_lineage_implementation_design_v1.md`
- Public CRSP product-level documentation previously identified during the documentary verification pass.

Evidence not provided:

- Institutional subscription documentation.
- Institutional license agreement.
- Legal/compliance retention memo.
- Official CRSP data dictionary.
- Official CRSP release/version documentation.
- CRSP support clarification.
- Authorized schema inspection artifact.
- Source-file manifest, checksum policy, or archive policy.

Assumptions resolved:

- None fully resolved.

Assumptions still unresolved:

- Subscription scope.
- Licensing rights.
- Retention rights.
- Archival rights.
- Source-file hashing feasibility.
- Release/version tracking.
- Known-date semantics.
- Exact field availability.
- Event-date support.
- Ticker-history/window support.
- Source reproducibility.
- Source-gate eligibility.

Implementation impact:

The project is not ready to advance to CRSP Metadata Implementation Design. Public product documentation supports CRSP's broad plausibility, but it does not satisfy the external evidence requirements defined by the requirements package.

Final classification: `EXTERNAL_EVIDENCE_INCOMPLETE`.

## SECTION 2 - Evidence Inventory

| source | version | publication/release information | evidence type | confidence | assumptions supported |
| --- | --- | --- | --- | --- | --- |
| `crsp_external_verification_requirements_package_v1.md` | v1 | Internal Project Underdog note | Verification requirement package | High for project requirements | All remaining blockers and decision gates |
| `crsp_assumption_verification_execution_v1.md` | v1 | Internal Project Underdog note | Prior documentary verification execution | High for prior status | Current partial verification baseline |
| `crsp_security_master_ticker_lineage_implementation_specification_v1.md` | v1 | Internal Project Underdog note | Implementation specification | High for required schema and scaffold controls | Schema, diagnostics, assumption gates, non-goals |
| `crsp_security_master_ticker_lineage_implementation_design_v1.md` | v1 | Internal Project Underdog note | Implementation architecture | High for architecture assumptions | Identifier strategy, PIT design, known-date/source-lineage requirements |
| CRSP public product-level documentation | Public/current page state not version-pinned | Public web documentation; no account-specific release metadata | Public product documentation | Medium for broad product plausibility; low for implementation verification | Broad subscription-scope fit, broad field/event/ticker plausibility |
| Institutional subscription documentation | Not provided | Not provided | Required external evidence | None | Subscription scope remains unresolved |
| Institutional license agreement or compliance memo | Not provided | Not provided | Required external evidence | None | Licensing, retention, archival rights remain unresolved |
| Official CRSP data dictionary | Not provided | Not provided | Required external evidence | None | Exact field availability, event-date, ticker-window, known-date support remain unresolved |
| Official release/version documentation | Not provided | Not provided | Required external evidence | None | Release/version tracking remains unresolved |
| Authorized schema inspection artifact | Not provided | Not provided | Future-only authorized evidence | None | Field/schema verification remains unresolved |

## SECTION 3 - Assumption Verification Matrix

| assumption | evidence examined | conclusion | verification status | remaining uncertainty |
| --- | --- | --- | --- | --- |
| Subscription scope | Public CRSP product-level documentation and internal requirements package. | Public documentation supports broad product plausibility but does not prove Project Underdog's actual entitlement, files, modules, date ranges, or documentation access. | `PARTIALLY_VERIFIED` | Institutional subscription documentation or CRSP entitlement confirmation is required. |
| Licensing rights | Internal requirements package; no license text supplied. | No objective license evidence was available. | `BLOCKED` | Need institutional license agreement, legal/compliance memo, or CRSP clarification. |
| Retention rights | Internal requirements package; no retention policy supplied. | No evidence confirms whether raw files, source references, hashes, derived metadata, or audit notes may be retained. | `BLOCKED` | Need retention policy and compliance approval. |
| Archival rights | Internal requirements package; no archive policy supplied. | No evidence confirms whether source archives, controlled references, or redacted references are allowed. | `BLOCKED` | Need archive/reference policy tied to CRSP license. |
| Source-file hashing feasibility | Internal requirements package; no file/hash policy supplied. | No evidence confirms direct hashes, bundle hashes, or controlled-reference hashes are permitted. | `BLOCKED` | Need license/legal confirmation and file manifest strategy. |
| Release/version tracking | Public product documentation and internal requirements package. | No deterministic release id, extract id, snapshot date, or source-version rule was verified. | `NOT_VERIFIED` | Need official release documentation or account-specific extract/version metadata. |
| Known-date semantics | Public product documentation and PIT requirements. | Public documentation does not prove event-level known dates or an approved release/snapshot fallback for `as_of_date`. | `NOT_VERIFIED` | Need official date-semantics documentation or CRSP support clarification. |
| Exact field availability | Public product-level documentation and internal schema requirements. | Broad field plausibility remains, but exact columns, source schemas, and required lineage fields are not verified. | `PARTIALLY_VERIFIED` | Need official data dictionary or authorized schema inspection. |
| Event-date support | Public product-level documentation and internal event-lineage requirements. | Corporate-action/event plausibility remains, but event-date fields and event-code crosswalks are not verified. | `PARTIALLY_VERIFIED` | Need official data dictionary, event-code documentation, or vendor clarification. |
| Ticker-history support | Public product-level documentation and internal ticker-lineage requirements. | Ticker-lineage plausibility remains, but ticker start/end windows, reuse behavior, and exchange/share-class support are not verified. | `PARTIALLY_VERIFIED` | Need official data dictionary or authorized schema inspection. |
| Source reproducibility | Internal requirements package; no manifest/hash/row-count evidence supplied. | No source-file reproducibility evidence was available. | `BLOCKED` | Need file manifest, checksum policy, row-count policy, archive/reference strategy, and license confirmation. |
| Source-gate eligibility | Internal source-gate requirements and unresolved evidence state. | Source-gate eligibility cannot advance because critical external evidence is missing. | `BLOCKED` | Need subscription, license, retention, date, field, reproducibility, and allowed-use evidence. |

## SECTION 4 - License and Subscription Review

Subscription scope:

- Status: `PARTIALLY_VERIFIED`.
- Public documentation supports CRSP's broad relevance to U.S. stock data and historical research.
- Missing evidence: actual institutional CRSP entitlement, available product modules, files/tables, coverage dates, documentation access, delivery format, and update cadence.

Licensing rights:

- Status: `BLOCKED`.
- No license agreement or usage-rights memo was provided.
- Missing evidence: permitted research use, derived metadata rights, audit artifact rights, documentation reference rights, and restrictions on downstream outputs.

Retention rights:

- Status: `BLOCKED`.
- No retention policy was provided.
- Missing evidence: whether raw files, source references, file hashes, bundle hashes, checksums, row counts, derived metadata, review notes, and source-lineage artifacts may be retained.

Archival rights:

- Status: `BLOCKED`.
- No archive policy was provided.
- Missing evidence: whether source archives, controlled references, redacted references, or source-bundle manifests are allowed.

Redistribution restrictions:

- Status: `BLOCKED`.
- No redistribution language was reviewed.
- Missing evidence: whether any derived metadata, diagnostics, row-level references, or documentation references may be shared, committed, exported, or used in production contexts.

License/subscription conclusion:

The license and subscription evidence is insufficient. This alone blocks source loading, ingestion, metadata construction, lineage construction, source-gate advancement, and production use.

## SECTION 5 - Schema and Field Verification

Required identifiers:

- `PERMNO` and `PERMCO` remain architecturally expected but not externally verified from an official data dictionary or authorized schema artifact.
- Status: `PARTIALLY_VERIFIED`.

Expected fields:

- Public documentation supports broad plausibility for market data, identifiers, corporate actions, and active/inactive coverage.
- Exact field names, tables/files, schemas, source-record ids, exchange fields, name-history fields, security-type fields, and source metadata fields were not verified.
- Status: `PARTIALLY_VERIFIED`.

Release/version metadata:

- No official release id, snapshot date, extract date, file production date, or documentation version evidence was provided.
- Status: `NOT_VERIFIED`.

Event-date support:

- Public documentation supports corporate-action/event plausibility.
- Event effective dates, delisting dates, action codes, predecessor/successor fields, and event-code crosswalks were not verified.
- Status: `PARTIALLY_VERIFIED`.

Known-date support:

- No evidence proves event known dates or a conservative source release/snapshot fallback.
- Status: `NOT_VERIFIED`.

Ticker-history support:

- Public documentation supports ticker-lineage plausibility.
- Ticker start/end fields, exchange/listing context, share-class support, ticker reuse controls, and overlapping-window diagnostics were not verified.
- Status: `PARTIALLY_VERIFIED`.

Schema and field conclusion:

The project is not ready for metadata implementation design. A formal CRSP data dictionary review or authorized schema inspection artifact is still required before field-level mapping can be specified.

## SECTION 6 - Architecture Impact

Implementation architecture:

- No architecture changes are required from the evidence reviewed.
- The existing assumption-bound architecture remains appropriate.
- The architecture must remain fail-closed because critical external evidence is missing.

Implementation specification:

- No implementation specification changes are required yet.
- The specification should not advance to metadata implementation design until license/subscription/date/field/reproducibility evidence is supplied.

Assumption register:

- No assumption should be promoted to fully verified.
- `crsp_subscription_scope`, `crsp_field_availability`, `crsp_event_date_semantics`, and `crsp_ticker_window_semantics` may remain partially verified from public documentation.
- `crsp_release_version_tracking` and `crsp_known_date_semantics` remain not verified.
- `crsp_licensing_rights`, retention, archival/hash feasibility, source-file reproducibility, and source-gate eligibility remain blocked.

Architecture impact conclusion:

The evidence reviewed confirms the current architecture boundary rather than changing it. The next movement requires evidence intake, not design revision.

## SECTION 7 - Remaining Blockers

| blocker | severity | missing evidence |
| --- | --- | --- |
| Licensing rights | Critical | Institutional license agreement, legal/compliance memo, or CRSP clarification. |
| Retention rights | Critical | Policy for retaining raw files, references, hashes, row counts, derived metadata, documentation references, and review notes. |
| Archival rights | Critical | License-compatible archive or controlled-reference policy. |
| Source-file hashing feasibility | Critical | Permission and method for direct hashes, bundle hashes, or controlled-reference hashes. |
| Subscription scope | Critical | Account-specific entitlement summary naming products, files/tables, date ranges, modules, and documentation access. |
| Known-date semantics | Critical | Official documentation or support clarification for event known dates or release/snapshot fallback. |
| Exact field availability | Critical | Official data dictionary or authorized schema inspection artifact. |
| Source reproducibility | Critical | File manifest, checksum, row-count, and archive/reference strategy. |
| Source-gate eligibility | Critical | Evidence-backed source-gate manifest and allowed-use decision. |
| Release/version tracking | Moderate | Official release, snapshot, extract, or documentation version evidence. |
| Event-date support | Moderate | Event-date fields, delisting-date fields, action codes, and event-code crosswalk. |
| Ticker-history support | Moderate | Ticker date fields, exchange/listing context, share-class support, and ticker reuse controls. |

No blocker is classified as minor because all unresolved items affect PIT safety, source lineage, source acceptance, or implementation readiness.

## SECTION 8 - Readiness Assessment

Project Underdog is not ready to advance to CRSP Metadata Implementation Design.

Reasoning:

- No assumption is fully verified.
- License and retention rights remain blocked.
- Subscription scope remains unconfirmed.
- Known-date semantics remain unverified.
- Exact field availability is not proven by official data dictionary or schema evidence.
- Release/version tracking is unresolved.
- Source-file reproducibility is blocked.
- Source-gate eligibility cannot advance from the current manual-review/diagnostics-only posture.

Current allowed posture:

- Continue evidence collection.
- Continue documentation review.
- Prepare an evidence intake checklist.
- Do not access CRSP datasets.
- Do not load source files.
- Do not ingest data.
- Do not construct metadata.
- Do not build lineage.
- Do not run validation.

Readiness classification for CRSP Metadata Implementation Design:

- Not ready.

## SECTION 9 - Final Recommendation

1. Which assumptions are fully verified?

None.

2. Which assumptions remain blocked?

Licensing rights, retention rights, archival rights, source-file hashing feasibility, source-file reproducibility, and source-gate eligibility remain blocked. Subscription scope, exact field availability, event-date support, and ticker-history support remain only partially verified. Release/version tracking and known-date semantics are not verified.

3. Are any architecture changes required?

No. The existing assumption-bound architecture remains appropriate. The required action is external evidence intake, not architecture change.

4. Is the project ready for CRSP Metadata Implementation Design?

No. The project remains blocked pending external subscription, license, retention, archival/hash, data dictionary, release/version, known-date, and reproducibility evidence.

5. What should the next Codex task be?

The next task should be **Project Underdog - CRSP External Evidence Intake Checklist v1**. It should create a concrete checklist for the user or institution to provide the required license, subscription, retention, data dictionary, release/version, known-date, archive/hash, and source reproducibility evidence. It should remain documentation-only and should not access CRSP datasets, load files, ingest data, construct metadata, build lineage, run validation, mutate governance, register production outputs, or implement ML.
