# Project Underdog - CRSP Security Master and Ticker Lineage Implementation Design v1

## SECTION 1 - Executive Summary

This note defines the assumption-bound implementation architecture for CRSP-backed `security_master_pit`, `ticker_lineage_pit`, `metadata_source_lineage`, and `source_acceptance_manifest` integration. It is design-only. No CRSP data was ingested, no CRSP files were loaded, no subscribed datasets were accessed, no metadata was constructed, and no security or ticker lineage was built.

Design scope:

- Define the CRSP-backed security identity architecture.
- Define the CRSP-backed ticker lineage architecture.
- Define the CRSP identifier strategy around `PERMNO`, `PERMCO`, ticker symbols, and internal PIT identifiers.
- Define effective-date, event-date, known-date, release-date, and source-version handling.
- Define required metadata source lineage, diagnostics, governance blockers, and future verification gates.

Implementation-design objectives:

- Preserve CRSP's expected permanent identifier strengths without treating CRSP as an accepted source.
- Make all unverified field, license, archive, subscription, and known-date assumptions explicit.
- Require fail-closed behavior for missing dates, missing source lineage, low confidence, unresolved events, ambiguous ticker reuse, and unresolved manual review.
- Keep sector history, industry history, peer reconstruction, discovery, validation, production registration, governance mutation, and ML fully blocked.

Assumptions:

- CRSP `PERMNO` and `PERMCO` are available in the subscribed product scope and retain the publicly documented meaning of permanent issue and company identifiers.
- The subscribed CRSP scope includes enough historical identifying, ticker, exchange, delisting, and corporate-action evidence to support design-level mapping.
- CRSP release, snapshot, documentation, and file-reference metadata can be used to create reproducible source-lineage records.
- License terms permit at least enough source references, hashes, redacted references, or equivalent audit evidence to satisfy Project Underdog reproducibility requirements.
- Event effective dates and known/as-of dates can be separated or conservatively represented through source release or snapshot dates.

Architecture compatibility:

CRSP remains architecturally compatible with the PIT metadata framework. The design uses `PERMNO` as the expected security identity anchor, `PERMCO` as the expected company identity anchor, ticker symbols as dated attributes, and CRSP release/snapshot metadata as required source lineage. The architecture is compatible only if the later implementation specification verifies field availability, licensing, source-version evidence, and known-date semantics before execution.

Final recommendation:

Proceed to a CRSP implementation specification only under explicit assumptions and verification gates. Do not proceed to implementation, source acceptance, source loading, ingestion, metadata construction, or lineage construction.

Final classification: `IMPLEMENTATION_ARCHITECTURE_DEFINED_WITH_ASSUMPTIONS`.

## SECTION 2 - Assumption Register

| assumption area | assumption | rationale | verification requirement | risk level |
| --- | --- | --- | --- | --- |
| Subscription scope | The available CRSP package includes U.S. Stock Database components needed for identity, ticker, exchange, delisting, corporate-action, and release metadata. | Prior reviews identify CRSP as a strong candidate, but exact subscription scope is unverified. | User/subscription confirmation of products, files, tables, documentation, and update cadence. | Critical |
| Licensing | License terms permit research use of derived metadata artifacts and enough audit evidence to support reproducibility. | Source acceptance requires license-compatible lineage and usage notes. | Review CRSP license for local retention, derived artifacts, hashes, documentation references, and audit records. | Critical |
| Archival | Source files, release references, or license-compliant controlled references can be retained. | PIT reproducibility requires source lineage, versioning, and hash or equivalent evidence. | Confirm permitted archive/hash/reference strategy before any build mode. | Critical |
| Field availability | `PERMNO`, `PERMCO`, ticker, exchange/listing context, name/security descriptors, delisting information, and corporate-action evidence are available. | These concepts are required for `security_master_pit` and `ticker_lineage_pit` architecture. | Documentation-level field inventory before implementation specification; source-file inspection only in a later authorized task. | Critical |
| Release/version | CRSP release, snapshot, or extract metadata can be mapped to `source_version` and `source_snapshot_date`. | `metadata_source_lineage` and `source_acceptance_manifest` require version and snapshot fields. | Define deterministic version policy using CRSP release or controlled extract metadata. | High |
| Known-date | Source known dates can be assigned from event-level known dates or conservative release/snapshot dates. | `as_of_date` must be date-safe and cannot use future knowledge. | Verify event-level known-date support; otherwise require release/snapshot fallback and block unsupported rows. | Critical |
| Identifier stability | `PERMNO` is stable enough for security identity and `PERMCO` is stable enough for company identity. | Public CRSP characteristics and prior reviews support this at design level. | Verify identifier semantics in CRSP documentation and subscribed data dictionaries. | High |
| Ticker windows | Historical ticker evidence can support explicit or conservatively inferred ticker windows. | `ticker_lineage_pit` requires `ticker_effective_start` and `ticker_effective_end`. | Verify ticker date fields, exchange fields, and adjacent-window rules. | Critical |
| Event windows | Delisting and corporate-action evidence can support event lineage or be blocked when ambiguous. | Event-dependent continuity needs dates, type, predecessor/successor evidence, and confidence. | Verify event fields and map CRSP event concepts to controlled event types. | Critical |
| Source hashing | Raw source or source-bundle hashes can be stored, or a compliant equivalent can be defined. | Source-gate artifacts require `source_file_hash` or equivalent reproducibility evidence. | License review plus source-lineage policy decision. | High |

## SECTION 3 - Security Master PIT Architecture

Target artifact: `security_master_pit`.

Security identity model:

- Internal `security_id` should be derived from CRSP `PERMNO` using a stable namespace such as `crsp_permno:<PERMNO>`.
- `PERMNO` should remain available as source-native lineage evidence through source references, supporting identifiers, or source-record references.
- Ticker symbols must not create or override `security_id`.
- If `PERMNO` is missing, ambiguous, duplicated across conflicting active windows, or not license-verifiable, the affected row must be blocked.

Company identity model:

- Internal `issuer_id` should be derived from CRSP `PERMCO` using a stable namespace such as `crsp_permco:<PERMCO>`.
- `PERMCO` represents company-level continuity and must not collapse separate security/share-class identities.
- Multi-security companies, multiple share classes, reorganizations, mergers, and spin-offs must preserve separate `security_id` values even when `issuer_id` remains shared.
- If company continuity is unclear, `issuer_id` should be explicit unknown or manual-review only, with confidence reduction or blocking where identity continuity depends on it.

Continuity model:

- Identity continuity is `PERMNO`-first.
- Company continuity is `PERMCO`-first.
- Name changes update `company_name` and event notes but do not create new `security_id` values by themselves.
- Exchange changes update exchange/listing attributes and may update ticker namespace, but do not create new `security_id` values unless source evidence indicates a distinct security.
- Mergers, acquisitions, spin-offs, split-offs, and relistings require event-specific continuity handling and must not be inferred solely from ticker disappearance.

Active/inactive status model:

- `is_active` should be derived from dated active/inactive, delisting, and listing-window evidence.
- Delisting evidence should close active windows only when date semantics are verified.
- Open-ended active records must be represented explicitly and tied to source version and `as_of_date`.
- Any post-delisting active state requires successor, relisting, or correction evidence.

Effective-date model:

- `effective_start` is the start of the security identity or attribute window.
- `effective_end` is the end of that window or an explicit open-ended state.
- `as_of_date` is the date the source state was known to Project Underdog, not necessarily the event effective date.
- Event effective dates and event as-of dates must be kept separate.
- Missing `effective_start`, missing `as_of_date`, future-dated `as_of_date`, or unverified known-date semantics block downstream use.

Confidence model:

- `identity_confidence` starts from source-gate identifier quality and PIT integrity.
- Confidence is reduced for inferred windows, unresolved dates, ambiguous exchange/share-class context, missing `PERMCO` where issuer continuity matters, manual overrides, and event ambiguity.
- Minimum downstream eligibility is `0.70`.
- `point_in_time_quality` must be `point_in_time_verified`, `date_stamped_snapshot`, or policy-compliant `inferred_window` for eligible rows.
- `static_snapshot_only`, `unresolved`, and `blocked` rows are not eligible.

Source lineage model:

- Every `security_master_pit` row must reference `source`, `source_version`, `source_record_id`, `metadata_version`, `run_id`, `collection_timestamp`, and `record_hash` or a compliant equivalent.
- Rows without accepted source lineage remain blocked.
- Rows derived from inferred evidence must record the inference rule in source lineage or notes.

## SECTION 4 - Ticker Lineage PIT Architecture

Target artifact: `ticker_lineage_pit`.

Ticker identity model:

- Ticker symbols are dated attributes scoped by `security_id`, exchange, ticker namespace, and effective window.
- Ticker symbols are not stable identifiers.
- A ticker row must link to a `PERMNO`-derived `security_id`.
- Ticker namespace should be derived from exchange/listing context and product universe rules.

Ticker transition model:

- A ticker transition creates a closed prior ticker window and an opened next ticker window when CRSP evidence supports continuity.
- `prior_ticker` and `next_ticker` should be populated when adjacent windows are known.
- If the transition date is unknown but adjacent dated observations support inference, the row may be `inferred_window` only if policy confidence and stale-age rules pass.
- Ticker transitions with unresolved dates or unresolved identity continuity are blocked.

Ticker reuse controls:

- Reuse is detected by ticker, exchange, namespace, date window, and `security_id`.
- Same ticker across different `security_id` values is allowed only when windows are non-overlapping or disambiguated by exchange/share-class context.
- Overlapping reuse without sufficient context receives `recycled_ticker_ambiguity` or `duplicate_active_mapping`.
- Ticker reuse must never backfill a later identity into an earlier security.

Delisting model:

- Delisting evidence should close ticker windows and active security windows where appropriate.
- Delisting date, final trading date, event effective date, and source known date must remain distinct where source evidence permits.
- Post-delisting ticker-date rows are blocked unless successor, relisting, correction, or explicit continuity evidence exists.

Merger/acquisition handling:

- Merger and acquisition events may close predecessor windows and link successor identities only when source evidence identifies the affected identities and dates.
- If successor/predecessor mapping is incomplete, the affected event window is `manual_review_required` or blocked.
- Ticker disappearance alone is insufficient to infer merger or acquisition lineage.

Spin-off handling:

- Spin-offs may create one-to-many lineage where a parent continues and one or more child securities begin.
- The architecture should allow event lineage through `security_event_id` or a linked event artifact rather than forcing all detail into a single successor field.
- Child and parent ticker windows require separate `security_id` values unless source evidence proves same-entity continuity.

Relisting handling:

- Relistings are high-risk events.
- Same `security_id` continuity requires source evidence that the relisted security is the same `PERMNO` identity.
- If a relisting creates a new `PERMNO` or identity continuity is not proven, a new `security_id` window is required or affected rows are blocked.

Confidence model:

- `ticker_mapping_confidence` starts from ticker-date evidence, identifier continuity, exchange/share-class clarity, and source PIT quality.
- Confidence is reduced for inferred ticker starts/ends, sparse observations, exchange ambiguity, share-class ambiguity, manual overrides, stale source records, and ticker reuse.
- Minimum downstream eligibility is `0.70`.
- Ambiguous active overlaps, missing ticker effective dates, missing `as_of_date`, or unresolved identity links block the affected windows.

## SECTION 5 - Identifier Strategy

`PERMNO`:

- Primary source-native security or issue identifier.
- Expected basis for internal `security_id`.
- Recommended internal namespace: `crsp_permno:<PERMNO>`.
- Highest priority for security continuity.
- Must be preserved in audit/source lineage.

`PERMCO`:

- Primary source-native company identifier.
- Expected basis for internal `issuer_id`.
- Recommended internal namespace: `crsp_permco:<PERMCO>`.
- Highest priority for company continuity.
- Must not override distinct `PERMNO`-level securities.

Ticker symbols:

- Dated labels and ticker-window attributes.
- Never primary identity keys.
- Require exchange/namespace/date context.
- Require reuse controls.

Company-level identifiers:

- `PERMCO` should define issuer/company continuity when available.
- Additional source identifiers, if available, are supporting evidence.
- If company-level identifiers conflict, rows require manual review or confidence reduction.

Internal PIT identifiers:

- Internal identifiers should be deterministic, namespaced, and rebuild-stable.
- Internal identifiers should not encode mutable ticker symbols.
- Internal ids should remain source-specific until a later multi-source identity reconciliation design is approved.

Continuity hierarchy:

1. Source lineage and source version.
2. `PERMNO` for security identity.
3. `PERMCO` for company identity.
4. Dated ticker/exchange/share-class attributes.
5. Supporting identifiers and descriptive fields.
6. Manual override only with explicit audit trail.

Conflict resolution:

- Source-native permanent identifiers dominate ticker and name fields.
- Conflicts with high identity impact are `manual_review_required` or blocked.
- Conflicts between similarly credible records inherit the lower confidence and block event-sensitive windows unless resolved.

## SECTION 6 - Effective-Date and Known-Date Architecture

Effective-date handling:

- Effective dates describe when an identity, ticker, exchange, name, active status, or event state became economically true.
- Required output fields include `effective_start`, `effective_end`, `ticker_effective_start`, and `ticker_effective_end`.
- If explicit effective dates are unavailable, inferred windows may be used only under the inferred-window policy.

Event-date handling:

- Event dates describe the economic event date for ticker changes, name changes, exchange changes, delistings, mergers, acquisitions, spin-offs, split-offs, relistings, and ticker reuse.
- Event dates populate `event_effective_date` only when verified.
- Event lineage must not be inferred from price/data termination alone.

Known-date handling:

- `as_of_date` and `event_as_of_date` must represent when the information was known or available to the project.
- If CRSP event-level known dates are verified, they may be used.
- If event-level known dates are not verified, the conservative fallback is source release or source snapshot date.
- If no known-date proxy is available, the row is blocked from historical PIT use.

Release-date handling:

- Source release date or controlled snapshot date is the minimum required known-date fallback.
- Release dates must remain separate from event effective dates.
- Backfilled historical event facts from later releases must receive later `as_of_date` values.

Source-version handling:

- `source_version` should be deterministic and based on CRSP product, release, snapshot, extract, and source-bundle evidence.
- `source_snapshot_date` should capture the date of the controlled source snapshot or release.
- `metadata_version` should identify the Project Underdog transformation version.

Fail-closed behavior:

- Missing effective start blocks.
- Missing ticker effective start blocks.
- Missing `as_of_date` or source snapshot date blocks.
- Future-dated `as_of_date` relative to downstream use blocks.
- Event effective date used as known date without proof blocks.
- Inferred windows crossing corporate-action or ticker-change boundaries without event lineage block.

## SECTION 7 - Metadata Source Lineage Architecture

Target artifact: `metadata_source_lineage`.

Source identity:

- Source label should be stable, such as `crsp_us_stock_databases`, after source-gate approval.
- Source type should classify CRSP as a professional/institutional security master and ticker-lineage source.
- Source identity must be tied to source-gate status and allowed-use eligibility.

Source version:

- Version convention should include CRSP product scope, release or snapshot identifier, extract date if applicable, and a local source-bundle identifier where license permits.
- Any change to source files, release, product scope, or extraction method should create a new source-version lineage record.

Source release:

- Release notes, user guides, metadata guides, and data dictionaries should be referenced in source lineage where license permits.
- If documentation cannot be archived, a controlled reference plus license note is required.

Source confidence:

- Source confidence should derive from source-gate scores, PIT quality, identifier quality, license/reproducibility support, field availability, and date semantics.
- Source confidence cannot be raised using alpha/discovery results.

Lineage traceability:

- Every output row must trace to source, source version, source record id or equivalent, run id, metadata version, collection timestamp, and record hash or approved equivalent.
- Source record id design must be deterministic and based on source-native keys or source-bundle row references.

Reproducibility controls:

- Missing source version blocks.
- Missing source snapshot date blocks historical use.
- Missing hash/archive/reference strategy blocks source acceptance.
- Missing license notes blocks source acceptance.
- Row-count drift and source-bundle drift require diagnostics.

## SECTION 8 - Diagnostics Architecture

Security continuity diagnostics:

- Missing `PERMNO`.
- Duplicate `PERMNO` identity-window conflict.
- `PERMNO` to `security_id` instability across rebuilds.
- Security windows missing `effective_start`.
- Security windows missing `as_of_date`.
- Security windows with future-dated `as_of_date`.
- Name changes that imply identity ambiguity.
- Exchange changes that imply identity ambiguity.

Company continuity diagnostics:

- Missing `PERMCO`.
- `PERMCO` to `issuer_id` instability across rebuilds.
- One `PERMCO` mapping to unexpected multiple active issuer identities.
- Company continuity conflicts across mergers, acquisitions, and spin-offs.

Ticker continuity diagnostics:

- Missing ticker.
- Missing exchange or ticker namespace.
- Missing `ticker_effective_start`.
- Missing or inferred `ticker_effective_end`.
- Gaps between adjacent ticker windows.
- Overlaps between adjacent ticker windows.
- Ticker disappearance without delisting or event evidence.

Ticker reuse detection diagnostics:

- Same ticker/exchange active across multiple `security_id` values on overlapping dates.
- Reused ticker with insufficient non-overlapping window evidence.
- Ticker reuse crossing source release or known-date boundaries.
- Ticker reuse with missing share-class or exchange clarity.

Orphan record diagnostics:

- Ticker row without matching `security_id`.
- Event row without affected security.
- Company/issuer row without linked security where required.
- Source lineage row without manifest approval.

Duplicate identity diagnostics:

- Multiple internal `security_id` values for same `PERMNO`.
- Multiple internal `issuer_id` values for same `PERMCO`.
- Same source record mapping to multiple identities without event reason.

Stale source record diagnostics:

- Stale age by `as_of_date` or source snapshot date.
- Stale inferred windows.
- Stale event-sensitive rows.
- Rows exceeding stale blocking threshold.

Confidence degradation diagnostics:

- Rows below `0.70` identity confidence.
- Rows below `0.70` ticker mapping confidence.
- Rows below `0.70` event confidence.
- Rows downgraded due to inference, missing dates, manual override, stale age, or ambiguous exchange/share-class context.

Lineage conflict diagnostics:

- Missing source version.
- Missing source file hash or approved equivalent.
- Missing source record id.
- Missing license notes.
- Source record count drift.
- Source version drift.
- Conflicting source evidence for same ticker-date.

## SECTION 9 - Governance and Blocking Rules

Implementation-time blockers:

- No verified CRSP subscription scope.
- No verified CRSP license/retention policy.
- No CRSP source manifest.
- No field mapping specification.
- No source-version policy.
- No source hash/archive/reference policy.
- No known-date policy.

Validation blockers:

- Validation remains out of scope until source acceptance, PIT construction, and a separate validation-readiness review exist.
- Any attempt to treat source-gate or lineage checks as alpha validation is blocked.

Lineage blockers:

- Source status not `accepted` for PIT lineage construction.
- `conditional` source row outside machine-readable allowed scope.
- `manual_review_required`, `diagnostic_only`, `rejected`, or `deprecated` source status.
- Missing accepted `metadata_source_lineage`.
- Missing `PERMNO` for security identity.
- Missing or ambiguous ticker effective dates.
- Ambiguous ticker reuse.
- Unresolved predecessor/successor continuity for event-dependent rows.

Confidence blockers:

- `identity_confidence < 0.70`.
- `ticker_mapping_confidence < 0.70`.
- `event_confidence < 0.70` for event-dependent continuity.
- `point_in_time_quality` equal to `static_snapshot_only`, `unresolved`, or `blocked`.
- Inferred-window confidence below floor after penalty.

Source-lineage blockers:

- Missing source version.
- Missing source snapshot or release date.
- Missing source record id or equivalent.
- Missing source hash/archive/reference strategy.
- Missing license or usage notes.
- Missing normalization rules.
- Missing source-gate score summary.

Preserved governance controls:

- No source may feed PIT construction without accepted source status.
- No row may support downstream historical use without date-safe `as_of_date`.
- No static snapshot may support historical PIT lineage.
- No ticker-only identity construction is allowed.
- No discovery, refinement, validation, governance mutation, production registration, or ML is authorized by this design.

## SECTION 10 - Future Verification Requirements

Before implementation specification:

- Verify CRSP documentation access.
- Verify product/subscription scope.
- Verify field inventory at documentation level.
- Verify license and retention constraints.
- Verify source version and release metadata availability.
- Verify hash/archive/reference feasibility.
- Freeze `PERMNO`/`PERMCO` namespace conventions.
- Freeze known-date fallback rules.
- Freeze ticker-window and event-window design assumptions.

Before source loading:

- Source must pass source-gate evaluation with an approved manifest.
- License review must permit the planned loading mode.
- Source paths, file references, hashes, and retention notes must be defined.
- Runner mode must be explicitly authorized in a future task.

Before metadata construction:

- CRSP source status must be `accepted` or conditionally accepted for a machine-readable domain.
- Field mappings must be implemented and tested.
- Source lineage records must be producible.
- Diagnostics must pass or block affected rows.
- Manual review queue must be empty for construction-eligible rows.

Before lineage construction:

- `security_master_pit` and `ticker_lineage_pit` schema outputs must be validated.
- Identity and ticker confidence floors must pass.
- Effective-date and known-date checks must pass.
- Ticker reuse and duplicate active mapping diagnostics must pass.
- Event-lineage blockers must be resolved or excluded.

## SECTION 11 - Readiness Assessment

If assumptions hold, Project Underdog is ready to create a CRSP implementation specification.

Reasoning:

- The source candidate evaluation established CRSP as a strong candidate for lineage evaluation.
- The lineage design review classified CRSP as suitable for integration design.
- The integration planning gap-closure review classified CRSP as ready for implementation design with assumptions.
- The PIT schemas, source-gate vocabulary, confidence floors, inferred-window policy, stale-age policy, and blocking rules are defined.
- This architecture defines the CRSP-specific identity, ticker, date, source-lineage, diagnostic, and governance design.

The readiness is conditional:

- Implementation specification is justified only if it remains design/specification-only and includes verification gates.
- Implementation execution is not justified.
- Source acceptance is not justified.
- CRSP loading, ingestion, metadata construction, and lineage construction remain blocked.

## SECTION 12 - Final Classification

Final classification: `IMPLEMENTATION_ARCHITECTURE_DEFINED_WITH_ASSUMPTIONS`.

Rationale:

The implementation architecture is now defined at the conceptual and governance level. CRSP can be represented as a source candidate whose expected `PERMNO`/`PERMCO` identifiers anchor security and company identity, whose ticker values become dated lineage attributes, whose event and delisting evidence feeds event-aware windows, and whose release/snapshot metadata supports source lineage. The design preserves fail-closed controls for missing fields, missing dates, missing source lineage, low confidence, ambiguous ticker reuse, and unresolved event continuity.

The classification is not `READY_FOR_IMPLEMENTATION_SPECIFICATION` unconditionally because critical assumptions remain unverified: subscription scope, licensing and retention rights, archival/hash feasibility, exact field availability, release/version evidence, and known-date semantics. It is not `NOT_READY_FOR_IMPLEMENTATION_ARCHITECTURE` because existing project documentation and prior CRSP reviews are sufficient to define the architecture under assumptions.

## SECTION 13 - Final Recommendation

1. Is the CRSP architecture now fully defined?

The architecture is fully defined at the assumption-bound implementation-architecture level. It is not fully defined at executable specification level because exact CRSP fields, license terms, subscription scope, archive/hash policy, and known-date semantics remain unverified.

2. Which assumptions remain unverified?

Unverified assumptions include subscribed product scope, license and retention rights, source archive feasibility, source hash feasibility, field availability, release/version metadata, event-level known-date support, ticker-window fields, event-window fields, share-class/listing fields, and source-record id strategy.

3. What remains blocked?

Source acceptance, CRSP file loading, ingestion, `security_master_pit` construction, `ticker_lineage_pit` construction, `metadata_source_lineage` construction, sector history reconstruction, industry history reconstruction, peer reconstruction, discovery, refinement, validation, governance mutation, threshold changes, production registration, ML, and alpha candidate creation remain blocked.

4. What must be verified next?

Next verification must cover CRSP documentation access, product/subscription scope, license and retention constraints, field inventory, date semantics, release/snapshot metadata, hash/archive/reference feasibility, source-record id strategy, and whether CRSP event/ticker evidence can support required PIT windows without look-ahead.

5. What should the next Codex task be?

The next task should be **Project Underdog - CRSP Implementation Specification Readiness Review v1**. It should review this architecture, verify whether the remaining assumptions are sufficiently bounded for a specification task, and decide whether a CRSP implementation specification can be written. It should remain review-only and should not ingest CRSP data, load source files, access subscribed datasets, construct metadata, build lineage, run validation, mutate governance, register production outputs, or implement ML.

