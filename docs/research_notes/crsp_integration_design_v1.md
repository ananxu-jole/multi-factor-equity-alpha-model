# Project Underdog - CRSP Integration Design v1

## SECTION 1 - Executive Summary

This note designs how CRSP would conceptually map into Project Underdog's Security Master and Ticker Lineage PIT architecture. The scope is architecture mapping only. No CRSP data was ingested, no subscribed CRSP files were loaded or inspected, no metadata was constructed, and no security or ticker lineage was built.

Intended PIT role:

- CRSP would be evaluated as a candidate source for `security_master_pit`.
- CRSP would be evaluated as a candidate source for `ticker_lineage_pit`.
- CRSP would require source-lineage records in `metadata_source_lineage`.
- CRSP would require source-gate status and allowed-use documentation in `source_acceptance_manifest`.

Architecture compatibility:

CRSP appears architecturally compatible with the PIT identity and ticker-lineage design. Public CRSP materials describe the U.S. Stock Databases as covering active and inactive securities, historical identifying information, delisting information, distribution and corporate-action data, and permanent issue and company identifiers. The prior CRSP source evaluation and lineage design review classified CRSP as suitable for deeper lineage design, with `PERMNO` and `PERMCO` as the central conceptual identifiers.

Major strengths:

- `PERMNO` appears suitable as the source-native permanent security or issue identifier.
- `PERMCO` appears suitable as the source-native company or issuer continuity identifier.
- CRSP's active and inactive security coverage directly supports survivorship-bias controls.
- CRSP's ticker, name, exchange, delisting, and corporate-action concepts are aligned with the required PIT lineage domains.
- CRSP documentation, release notes, and controlled data products appear compatible with reproducible source-lineage tracking, subject to license verification.

Major unknowns:

- Exact field-level mappings from CRSP files into `security_master_pit` and `ticker_lineage_pit`.
- Exact effective-date, event-date, and known-date semantics for ticker, name, exchange, delisting, and corporate-action records.
- Whether source record identifiers, raw file hashes, source versions, and release references can be retained in Project Underdog artifacts under license.
- How ticker reuse, share-class changes, relistings, and predecessor/successor links should be represented when CRSP provides implicit rather than explicit event windows.
- Whether the subscribed CRSP product scope includes every table required for complete identity and ticker-lineage construction.

Final design classification: `READY_FOR_INTEGRATION_PLANNING_WITH_GAPS`.

This classification means CRSP is strong enough to justify a CRSP-specific integration planning and field-mapping design, but not yet ready for implementation design, source acceptance, ingestion, or PIT construction.

## SECTION 2 - CRSP Entity Inventory

The following entity inventory is conceptual and based on public CRSP characteristics plus prior Project Underdog review notes. It does not extract fields or inspect CRSP source files.

Security identity:

- Source-native permanent issue identifier: `PERMNO`.
- Expected role: stable source identifier for a security or issue across name, ticker, exchange, and corporate-action changes.
- PIT relevance: primary candidate input for Project Underdog `security_id` derivation.

Company identity:

- Source-native permanent company identifier: `PERMCO`.
- Expected role: stable source identifier for issuer or company continuity.
- PIT relevance: primary candidate input for `issuer_id` derivation, subject to share-class and multi-security company rules.

Ticker history:

- Expected CRSP concepts: historical ticker symbols, exchange or listing context, security identifiers, and date ranges or dated observations.
- PIT relevance: candidate source for `ticker_lineage_pit` windows.
- Design caution: ticker symbols must be treated as dated attributes, not stable identifiers.

Corporate actions:

- Expected CRSP concepts: distributions, capital actions, share changes, mergers, acquisitions, spin-offs, and other corporate events.
- PIT relevance: candidate support for `security_event_id`, `event_type`, `event_effective_date`, predecessor/successor links, and event confidence.
- Design caution: the integration design must determine whether corporate-action records directly express lineage events or only provide evidence for inferred lineage.

Delistings:

- Expected CRSP concepts: delisting information for inactive securities.
- PIT relevance: supports `is_active`, `ticker_status`, `effective_end`, `ticker_effective_end`, and survivorship-bias diagnostics.
- Design caution: delisting date, delisting reason, final trading date, and known-date semantics must be separated.

Exchange continuity:

- Expected CRSP concepts: listing exchange or exchange code history.
- PIT relevance: supports `exchange`, `ticker_namespace`, ticker reuse controls, and listing-window validation.
- Design caution: exchange changes should not create new security identities unless accompanied by source evidence of an entity change.

## SECTION 3 - Security Master PIT Mapping

`security_master_pit` requires stable identity windows with effective dates, as-of dates, source lineage, confidence fields, and event lineage fields. CRSP appears conceptually capable of supporting this table, but field mapping remains unresolved.

Likely mapping concepts:

| Project Underdog field or concept | CRSP conceptual source support | Design status |
| --- | --- | --- |
| `security_id` | Derived from `PERMNO`, likely namespace-prefixed such as `crsp_permno:<value>` | Likely, pending id policy |
| `issuer_id` | Derived from `PERMCO`, likely namespace-prefixed | Likely, pending company/share-class policy |
| `company_name` | Historical company or security name descriptors | Likely, pending field/date review |
| `security_type` | Share/security type descriptors or share codes | Likely, pending field review |
| `exchange` | Historical exchange/listing code | Likely, pending exchange-code mapping |
| `country` | Product universe and/or security descriptors | Unresolved |
| `currency` | Product or market data currency assumptions and fields | Unresolved |
| `is_active` | Active/inactive status inferred from listing/delisting windows | Likely, pending rule design |
| `effective_start` | Earliest reliable identity-window start from CRSP date fields | Critical unresolved mapping |
| `effective_end` | Delisting/end-of-window or open-ended state | Likely, pending delisting/window rules |
| `as_of_date` | Source availability or release/known date | Critical unresolved mapping |
| `source_version` | CRSP product release, snapshot, or file version | Likely, pending archival policy |
| `source_record_id` | Source table/key/file-row reference | Critical unresolved mapping |
| `record_hash` | Hash of source record or normalized evidence bundle | License and archive dependent |
| `identity_confidence` | Derived from identifier quality, date quality, and conflict diagnostics | Design required |
| `point_in_time_quality` | Derived from explicit dates, inferred windows, and source status | Design required |
| `event_type` | Mapped from ticker/name/exchange/delisting/corporate-action events | Design required |
| `predecessor_security_id` / `successor_security_id` | Derived from explicit or inferred corporate-action continuity | Critical unresolved mapping |

Security identity continuity:

`PERMNO` should be the dominant security-continuity anchor. The design should prohibit ticker-only identity joins. A security identity window should be created only when the CRSP evidence supports a stable `PERMNO`-based identity and supplies enough dating evidence for `effective_start`, `as_of_date`, and `point_in_time_quality`.

Company continuity:

`PERMCO` should be evaluated as the dominant company-continuity anchor. The integration design must decide whether `PERMCO` maps directly to `issuer_id` or whether Project Underdog needs a separate issuer namespace. Multi-class companies, reorganizations, and mergers require explicit rules so that company continuity does not overwrite security-level continuity.

Name continuity:

Name changes should generally update `company_name` and create event lineage but should not create a new `security_id` by themselves. The implementation design must verify whether CRSP provides direct date windows for names or whether name windows must be inferred from dated observations.

Exchange continuity:

Exchange values should be represented as dated attributes. Exchange changes should update `exchange` and may also affect `ticker_namespace`, but should not create a new `security_id` unless source evidence indicates a new security identity.

Effective-date support:

The most important unresolved design question is how CRSP dates should map into `effective_start`, `effective_end`, and `as_of_date`. Effective dates describe when an identity or ticker state was economically true. As-of dates describe when Project Underdog could have known that state. Those must remain separate.

## SECTION 4 - Ticker Lineage PIT Mapping

`ticker_lineage_pit` requires dated ticker windows keyed by `security_id`, `ticker`, `exchange`, and `ticker_effective_start`. CRSP appears conceptually well suited because permanent identifiers can disambiguate ticker changes and ticker reuse.

Likely mapping concepts:

| Project Underdog field or concept | CRSP conceptual source support | Design status |
| --- | --- | --- |
| `security_id` | Derived from `PERMNO` | Likely |
| `ticker` | Historical ticker symbol | Likely |
| `exchange` | Historical exchange/listing context | Likely |
| `ticker_namespace` | Derived from exchange, country, and listing context | Design required |
| `share_class` | Derived from CRSP share/security descriptors where available | Unresolved |
| `primary_listing_flag` | Derived from listing context if available, otherwise unresolved | Unresolved |
| `ticker_effective_start` | Start of ticker window from dated ticker evidence | Critical unresolved mapping |
| `ticker_effective_end` | End of ticker window from next ticker, delisting, or inferred close | Critical unresolved mapping |
| `as_of_date` | Source known date or release date | Critical unresolved mapping |
| `ticker_status` | Active, inactive, changed, delisted, reused, or inferred | Design required |
| `change_reason` | Ticker change, delisting, merger, spin-off, relisting, exchange change, unknown | Design required |
| `prior_ticker` / `next_ticker` | Adjacent ticker windows for same `security_id` | Likely, pending window design |
| `ticker_mapping_confidence` | Derived from date quality, identifier continuity, and ambiguity checks | Design required |

Ticker changes:

Ticker changes should create adjacent ticker windows linked to the same `security_id` when CRSP permanent identifiers show continuity. The design must distinguish ordinary ticker changes from identity changes, exchange changes, and share-class changes.

Ticker reuse controls:

Ticker reuse must be detected by comparing ticker, exchange, date window, and `PERMNO`-derived `security_id`. Reuse is acceptable only when windows are non-overlapping or when exchange/share-class context makes the mapping unambiguous. Overlapping reuse without disambiguating context must block the affected rows.

Mergers and acquisitions:

Merger and acquisition evidence should be mapped into event lineage only after field-level CRSP review confirms event semantics. The design should not infer successor links solely from ticker disappearance or price termination.

Spin-offs:

Spin-offs likely require special predecessor/successor handling because one company event can create multiple securities. The design should allow one-to-many event relationships through `security_event_id` or a linked event artifact rather than forcing a single successor field to carry all lineage.

Relistings:

Relistings should be treated as high-risk ticker-lineage events. The design must determine whether a relisting preserves the same `PERMNO` or creates a new source identity, and whether the inactive interval should be represented as a closed ticker window followed by a new window.

Delistings:

Delisting evidence should close ticker and security activity windows where appropriate. Delisting support is a major CRSP strength, but delisting status must not be confused with source availability or known-date timing.

## SECTION 5 - Identifier Strategy Review

`PERMNO`:

- Primary source-native security or issue continuity identifier.
- Strongest candidate basis for internal `security_id`.
- Should be namespace-prefixed to avoid collision with future source identifiers.
- Should remain stored in source lineage or supporting identifier fields for auditability.

`PERMCO`:

- Primary source-native company continuity identifier.
- Strongest candidate basis for internal `issuer_id`.
- Should be namespace-prefixed.
- Requires policy for multi-security companies, share classes, reorganizations, and company-level corporate actions.

Ticker symbols:

- Useful historical labels and join aids only within dated, exchange-scoped windows.
- Not stable identifiers.
- Must never be used as the sole identity key.
- Should be blocked when ticker-date windows overlap ambiguously across multiple securities.

Company identifiers:

- `PERMCO` appears to satisfy the company-identifier requirement at a conceptual level.
- Any additional identifiers, such as CUSIP-like or exchange-specific identifiers, should be treated as supporting evidence unless field review proves stronger continuity.

Supporting identifiers:

- Supporting identifiers may help audit field-level mappings, resolve conflicts, and improve confidence.
- They should not override `PERMNO` and `PERMCO` without explicit review.

PIT suitability:

The identifier strategy is PIT-suitable if each derived internal identifier is reproducible from source-native CRSP identifiers, namespaced, immutable across rebuilds, and tied to source version plus source record lineage.

## SECTION 6 - Effective-Date and Known-Date Review

Effective-date requirements:

- `security_master_pit.effective_start` must describe when the security identity state became effective.
- `security_master_pit.effective_end` must describe when the state ended or became open-ended.
- `ticker_lineage_pit.ticker_effective_start` must describe when a ticker mapping became effective.
- `ticker_lineage_pit.ticker_effective_end` must describe when the ticker mapping ended or became open-ended.

Event-date requirements:

- `event_effective_date` must describe the economic event date.
- `event_as_of_date` must describe when the event was known or included in the source.
- Corporate actions, delistings, ticker changes, name changes, exchange changes, mergers, acquisitions, and spin-offs must not collapse these concepts into a single date unless the source only provides one date and the row is marked accordingly.

Known-date requirements:

- `as_of_date` must be no later than any downstream signal date using the metadata row.
- If CRSP provides only release-level known dates, the integration design must use release/snapshot dates conservatively.
- If CRSP provides event-level known dates, those should be preferred over release-level fallback dates.
- If known-date support cannot be verified, affected rows should remain `diagnostic_only`, `inferred_window`, or blocked.

Release and version considerations:

- Each future CRSP build must record product name, release date or snapshot date, source version, file references, and source hashes where licensing permits.
- Rebuilds must be reproducible from the same versioned source inputs.
- Source versions must be separated from economic effective dates.

Design risks:

- Using an event effective date as a known date would create look-ahead risk.
- Using a current CRSP extract without source snapshot tracking would weaken PIT integrity.
- Inferring ticker windows from adjacent observations may be acceptable only under the inferred-window policy with confidence penalties and diagnostics.
- Delisting and corporate-action dates may require separate treatment from ordinary ticker-window dates.

## SECTION 7 - Source Lineage Mapping

CRSP integration must create `metadata_source_lineage` records before any research-only PIT construction can be considered. This note does not construct those records.

Required source-lineage design elements:

| Required lineage concept | CRSP design requirement |
| --- | --- |
| `source` | Use a stable source label such as `crsp_us_stock_databases` after source-gate approval |
| `source_type` | Professional/institutional security master and ticker-lineage source |
| `source_version` | CRSP release, product version, or controlled snapshot identifier |
| `source_snapshot_date` | Date of source snapshot or release used for the build |
| `source_file_path` | Controlled internal path or redacted reference, subject to license |
| `source_url_or_reference` | Product documentation, release note, or internal subscription reference |
| `source_file_hash` | Hash of raw source file or source bundle where allowed |
| `record_count_raw` | Raw record counts by table/file in a future build |
| `record_count_clean` | Cleaned record counts by output artifact in a future build |
| `collection_timestamp` | Timestamp of controlled source collection or extraction |
| `license_or_usage_notes` | Explicit license and retention constraints |
| `normalization_rules` | Rules for namespace prefixes, dates, event mapping, and null handling |
| `source_confidence` | Derived from source-gate and semantic validation |
| `point_in_time_quality` | Derived from field-level PIT date support |

Source version tracking:

CRSP source lineage should use a deterministic source-version identifier that survives rebuilds. If CRSP release identifiers are not sufficient, Project Underdog should define a local version composed of product name, subscription dataset, extract date, release date, and a source-bundle hash where allowed.

Release tracking:

Release notes and metadata guides should be retained as source references when licensing permits. If external documentation cannot be archived, the lineage record should store stable references and manual review notes.

Audit lineage:

Every output row should trace back to a source version, source table or file, source record id, run id, metadata version, and record hash or equivalent controlled evidence bundle.

Reproducibility controls:

Future integration should fail closed if raw source references, source hashes, source version identifiers, or licensing notes are missing. A source cannot be promoted from evaluation to construction without reproducible source lineage.

## SECTION 8 - Diagnostics and Governance Mapping

The CRSP integration design should include diagnostics before any lineage construction is authorized.

Required identity diagnostics:

- Missing `PERMNO` inventory.
- Duplicate `PERMNO` identity-window conflicts.
- `PERMNO` to internal `security_id` stability checks.
- `PERMCO` to `issuer_id` continuity checks.
- Security identity windows with missing `effective_start`.
- Security identity windows with missing or non-conservative `as_of_date`.
- Name continuity gaps and name-change conflicts.
- Exchange continuity gaps and exchange-code conflicts.

Required ticker diagnostics:

- Missing ticker inventory by date range.
- Missing `ticker_effective_start`.
- Missing, inferred, or open-ended `ticker_effective_end`.
- Ticker reuse conflicts by ticker, exchange, share class, and date window.
- Overlapping ticker windows for the same `security_id`.
- One ticker mapping to multiple securities in overlapping windows.
- Ticker disappearance without delisting or event explanation.
- Relisting and inactive-gap diagnostics.

Required event diagnostics:

- Event records missing `event_effective_date`.
- Event records missing `event_as_of_date`.
- Corporate-action records without clear lineage implication.
- Merger/acquisition/spin-off records lacking predecessor or successor evidence.
- Delisting records that do not close expected activity windows.

Required source-lineage diagnostics:

- Missing source version.
- Missing source snapshot date.
- Missing source hash or archive reference.
- Missing license notes.
- Missing source record id.
- Source record count drift across rebuilds.

Required confidence diagnostics:

- Rows below the `0.70` identity, ticker-mapping, or event-confidence floor.
- Rows downgraded for inferred windows.
- Rows downgraded for missing known-date support.
- Rows blocked for ambiguous ticker reuse.
- Rows requiring manual review.

Governance compatibility:

The design remains compatible with current source-gate policy if CRSP is treated as evaluation-only until the source manifest, license notes, field mappings, semantic eligibility, and source-lineage diagnostics pass. `accepted` would be required before any PIT lineage construction. `conditional` would require machine-readable scope. `manual_review_required`, `diagnostic_only`, `rejected`, and `deprecated` block new PIT lineage construction.

## SECTION 9 - Gap Analysis

| Gap | Severity | Rationale | Required resolution |
| --- | --- | --- | --- |
| Field-level CRSP mapping | Critical | The design cannot map rows into strict PIT schemas without exact source fields and table semantics. | CRSP field mapping specification using licensed documentation, without loading data. |
| Known-date handling | Critical | Look-ahead protection depends on separating effective dates from source-known dates. | Define source release, snapshot, and event-known date rules. |
| Event-window representation | Critical | Ticker changes, delistings, mergers, spin-offs, and relistings may require explicit or inferred windows. | Define event window and inferred-window policy for CRSP. |
| Source record id strategy | Critical | Auditability requires row-level traceability. | Define stable source record keys or evidence-bundle references. |
| Licensing and archival constraints | Critical | Reproducibility depends on retaining references, hashes, and usage notes legally. | Review CRSP license terms for hashes, extracts, derived metadata, and documentation retention. |
| Subscription product scope | Critical | Required tables may not all be included in a specific subscription. | Confirm exact CRSP products, tables, and historical coverage available. |
| Source version tracking | Moderate | Rebuild reproducibility requires stable version identifiers. | Define `source_version` and `source_snapshot_date` from CRSP releases or controlled extracts. |
| Internal id namespace policy | Moderate | Internal ids must remain collision-free across future sources. | Freeze `crsp_permno` and `crsp_permco` namespace conventions. |
| Share-class and primary listing policy | Moderate | Multiple share classes and listings can affect ticker lineage. | Define share-class and primary-listing handling from CRSP descriptors. |
| Exchange-code normalization | Moderate | Exchange codes drive ticker namespaces and reuse controls. | Define mapping from CRSP exchange codes to canonical exchange labels. |
| Corporate-action taxonomy mapping | Moderate | Source event types must map into controlled Project Underdog event types. | Create CRSP event-type crosswalk. |
| Manual override protocol | Minor | Manual corrections may be necessary for rare ambiguous events. | Require explicit audit trail and no silent overrides. |
| Null and unknown representation | Minor | Strict schemas require explicit handling of missing fields. | Define null, unknown, inferred, and blocked output conventions. |

## SECTION 10 - Integration Design Readiness

If CRSP access existed today, the project would be ready to begin a CRSP-specific integration planning and field-mapping design. It would not yet be ready to begin implementation design or source construction.

Readiness rationale:

- CRSP has already passed source-candidate evaluation as `ACCEPTED_FOR_LINEAGE_EVALUATION`.
- The lineage design review classified CRSP as `SUITABLE_FOR_INTEGRATION_DESIGN`.
- The PIT schemas and source-gate policies are sufficiently defined to guide a CRSP-specific mapping design.
- The identifier strategy has a strong conceptual basis through `PERMNO` and `PERMCO`.
- The remaining gaps are specific and resolvable through documentation review, source manifest design, license review, and field-mapping design.

Not ready for implementation design because:

- Exact CRSP fields have not been mapped.
- Source license and archival constraints have not been reviewed.
- Known-date and release-date handling has not been frozen.
- CRSP source manifest values have not been produced.
- No source-gate evaluation of an actual CRSP manifest has accepted the source for construction.
- No implementation runner or build-lineage task has been authorized.

## SECTION 11 - Final Classification

Final classification: `READY_FOR_INTEGRATION_PLANNING_WITH_GAPS`.

CRSP appears strong enough to justify the next design step: a CRSP-specific field mapping, source manifest, and lineage-rule specification. The classification is not `READY_FOR_IMPLEMENTATION_DESIGN` because critical source-specific details remain unresolved, especially field mapping, known-date handling, event-window representation, source-record lineage, licensing, and subscription scope.

This note does not authorize source acceptance, source loading, ingestion, metadata construction, lineage construction, reconstruction, discovery, validation, governance mutation, production registration, or ML.

## SECTION 12 - Final Recommendation

1. Does CRSP appear architecturally compatible with `security_master_pit`?

Yes. CRSP appears architecturally compatible with `security_master_pit` because `PERMNO`, `PERMCO`, active/inactive security coverage, identifying information, exchange history, delisting information, and corporate-action concepts align with stable security identity, issuer continuity, activity windows, event lineage, and survivorship-bias controls.

2. Does CRSP appear architecturally compatible with `ticker_lineage_pit`?

Yes, with gaps. CRSP appears compatible with `ticker_lineage_pit` because permanent identifiers can anchor ticker histories and reduce ticker-reuse ambiguity. The largest remaining design work is converting CRSP ticker, exchange, delisting, and corporate-action evidence into explicit PIT ticker windows without look-ahead.

3. What are the largest remaining implementation unknowns?

The largest unknowns are exact CRSP field mappings, known-date semantics, event-window representation, source-record lineage, licensing and archival constraints, subscription product scope, and share-class/listing normalization.

4. What must be verified before implementation design?

Before implementation design, Project Underdog must verify licensed CRSP documentation and product scope, define a CRSP source manifest, map CRSP fields to PIT schemas, freeze `PERMNO`/`PERMCO` namespace rules, define effective-date versus known-date handling, define ticker/event-window rules, document source-version and hash strategy, and confirm license-compatible audit retention.

5. What should the next Codex task be?

The next task should be **Project Underdog - CRSP Field Mapping and Source Manifest Design v1**. It should remain design-only and review CRSP documentation and source-gate requirements to define field-level schema mappings, source manifest values, identifier namespace policy, date semantics, event-window rules, source-lineage requirements, and blocking diagnostics. It should not ingest data, load CRSP files, construct metadata, build lineage, run discovery, run validation, mutate governance, or register anything to production.

