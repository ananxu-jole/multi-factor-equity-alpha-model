# Project Underdog - CRSP Lineage Design Review v1

## SECTION 1 - Executive Summary

Review scope:

This note reviews CRSP's design-level suitability for Project Underdog's Security Master and Ticker Lineage PIT architecture. The review is limited to conceptual lineage compatibility for `security_master_pit`, `ticker_lineage_pit`, `metadata_source_lineage`, and `source_acceptance_manifest`.

Lineage suitability:

CRSP appears highly compatible with the lineage architecture. Public CRSP materials describe the US Stock Databases as covering active and inactive U.S. securities, daily and monthly market data, corporate actions, delisting information, permanent issue and company identifiers, release notes, user guides, metadata guides, and flat-file delivery formats. These characteristics align strongly with Project Underdog's requirement for stable identity, dated lineage, active/inactive coverage, and reproducible source lineage.

Major strengths:

- `PERMNO` provides a permanent issue identifier for tracking U.S.-listed equities over time.
- `PERMCO` provides a permanent company identifier.
- CRSP describes `PERMNO` as accounting for name changes, mergers, acquisitions, spin-offs, and other business events.
- The US Stock Databases cover more than 32,000 active and inactive U.S. securities.
- CRSP describes the history as precise and survivor-bias-free.
- CRSP includes security delisting information, corporate actions, identifiers, descriptors, and supplemental data items.
- CRSP provides monthly, quarterly, and annual release notes and CIZ flat-file documentation.

Major unknowns:

- Exact CRSP field mapping into the aligned `security_master_pit` and `ticker_lineage_pit` schemas.
- Exact representation of ticker effective windows, exchange windows, name windows, and ticker reuse.
- Event known-date versus event effective-date handling.
- License and retention terms for source files, hashes, derived artifacts, and audit records.
- Source record id strategy and raw file hash strategy.

Overall conclusion:

CRSP is suitable for a future CRSP-specific integration design effort, but not yet suitable for source acceptance or implementation. The correct next step is integration design and manifest planning, not ingestion or lineage construction.

Final classification: `SUITABLE_FOR_INTEGRATION_DESIGN`.

## SECTION 2 - Security Master Compatibility Review

Security identity continuity:

CRSP appears capable of supporting stable security identity. Public CRSP documentation describes `PERMNO` as a unique and permanent issue identifier. This maps conceptually to Project Underdog's need for a stable `security_id`, though the internal mapping rule must be designed separately.

Company continuity:

CRSP appears capable of supporting company continuity through `PERMCO`, described publicly as a permanent company identification number. This is conceptually aligned with issuer or company-level continuity, but a formal mapping to `issuer_id` remains unresolved.

Name continuity:

CRSP appears likely to support name continuity through identifying information and historical security descriptors. Public CRSP materials also describe `PERMNO` as accounting for name changes. Field-level review must verify how names are represented, whether name windows are explicit, and how name as-of dates should be handled.

Exchange continuity:

CRSP publicly documents exchange coverage for NYSE, NYSE American, NYSE Arca, NASDAQ, and Cboe BZX. This supports exchange continuity conceptually, but integration design must determine how exchange/listing venue changes are represented and whether they can be transformed into dated windows.

Identifier continuity:

Identifier continuity is a major CRSP strength. `PERMNO` and `PERMCO` are explicitly designed for historical continuity where ticker symbols can change. This directly addresses one of Project Underdog's highest lineage risks: confusing ticker history with stable security identity.

Effective-date support:

CRSP appears conceptually compatible with effective-date design because it is historical, release-based, and event-aware. However, exact field-level effective-date and as-of-date semantics are not yet verified. This is a design gap, not a blocker to integration design.

## SECTION 3 - Ticker Lineage Compatibility Review

Ticker changes:

CRSP appears capable of supporting ticker-change lineage through historical identifying information, permanent identifiers, and time-series continuity. Integration design must verify exact ticker fields, name-history records, and window construction rules.

Ticker reuse detection:

CRSP is well positioned to support ticker reuse detection because permanent identifiers are independent of ticker symbols. A reused ticker can conceptually be separated by `PERMNO`, date range, and exchange/listing context. Exact implementation rules remain unresolved.

Delistings:

CRSP explicitly lists security delisting information as a key data item. This is a strong fit for `ticker_lineage_pit` because delistings are central to active/inactive windows and survivorship-bias protection.

Mergers:

CRSP publicly describes `PERMNO` as supporting continuity across mergers and acquisitions. This is conceptually compatible with predecessor/successor and event-lineage requirements, but exact event fields need source documentation review.

Acquisitions:

Acquisitions are covered conceptually through the same corporate-restructuring support. Integration design must determine whether acquisition events can populate `event_type`, `event_effective_date`, `event_as_of_date`, predecessor/successor ids, and confidence fields.

Spin-offs:

CRSP publicly describes `PERMNO` as accounting for spin-offs. This is highly relevant to security continuity and ticker lineage, but field-level successor/predecessor handling must be verified.

Relistings:

CRSP's active/inactive history, exchange coverage, and permanent identifiers suggest possible support for relisting representation. The exact handling of relistings is unknown and should be a formal integration-design question.

Corporate-action continuity:

Corporate-action continuity is a CRSP strength. Public CRSP materials describe comprehensive corporate-action information and list corporate actions as a key US Stock Databases data item. Integration design should treat this as a primary source of event lineage, subject to exact field review.

## SECTION 4 - Identifier Mapping Review

Permanent identifiers:

- `PERMNO`: expected conceptual basis for internal `security_id`.
- `PERMCO`: expected conceptual basis for issuer/company continuity.

Ticker identifiers:

Ticker symbols should not be treated as stable identifiers. CRSP's permanent identifiers should dominate ticker symbols in lineage construction. Ticker values should become dated attributes or ticker windows linked to `PERMNO`-derived identity.

Company identifiers:

`PERMCO` is conceptually aligned with company or issuer continuity. Integration design must decide whether `PERMCO` maps directly to `issuer_id`, whether it requires namespace prefixing, and how company continuity interacts with share classes and corporate events.

Mapping stability:

CRSP's identifier model appears stable enough for integration design. The architecture should preserve CRSP identifiers as source-native lineage fields even if Project Underdog creates internal identifiers.

Historical continuity:

Historical continuity is a major strength because CRSP identifiers are designed for time-series and corporate-event tracking. The main unknown is not whether continuity exists conceptually, but how to represent it in the aligned schemas without losing event/as-of semantics.

## SECTION 5 - PIT Architecture Mapping Review

`security_master_pit`:

CRSP appears architecturally compatible. `PERMNO`, `PERMCO`, identifying information, exchange coverage, active/inactive history, delisting information, and corporate actions could conceptually support stable security identity windows, company continuity, exchange attributes, event lineage, and confidence fields.

Design questions:

- Should internal `security_id` be derived directly from `PERMNO` or namespace-prefixed?
- Should `issuer_id` be derived from `PERMCO`?
- How should CRSP event records populate predecessor/successor fields?
- How should missing name, country, currency, or security-type fields be represented if not directly available?

`ticker_lineage_pit`:

CRSP appears architecturally compatible, but ticker-window design requires the most care. Historical ticker/name records should be transformed only after exact date semantics are understood.

Design questions:

- Which CRSP fields define ticker start and end windows?
- Are ticker windows explicit or inferred from historical name records?
- How should exchange changes and ticker reuse be represented?
- How should open-ended current windows be handled?

`metadata_source_lineage`:

CRSP appears compatible with source lineage requirements because public materials describe release notes, user guides, metadata guides, and flat-file formats. Formal design must specify release version, source snapshot date, source file hash, record counts, normalization rules, and license notes.

`source_acceptance_manifest`:

CRSP appears capable of populating the source acceptance manifest at a candidate/design level. The unresolved items are licensing terms, source-file hash retention, exact source version/snapshot-date policy, and manual-review notes.

No field mapping is finalized in this review.

## SECTION 6 - Historical Integrity Review

Survivorship-bias protection:

CRSP is strong. Public materials describe the US Stock Databases as survivor-bias-free and covering active and inactive securities.

Historical continuity:

CRSP is strong. `PERMNO` and `PERMCO` directly address historical continuity across ticker changes and corporate events.

Effective-date reliability:

CRSP appears compatible, but exact effective-date reliability cannot be concluded until source documentation and field semantics are reviewed. The project must distinguish source release date, event effective date, known/as-of date, and inferred window boundaries.

Corporate-action representation:

CRSP is strong at the conceptual level. Public materials identify corporate actions as a key data item and describe comprehensive corporate-action information. Event-level mapping remains unresolved.

Lineage transparency:

CRSP appears strong due to release notes, user guides, metadata guides, delivery formats, permanent identifiers, and documented data items. Project-specific lineage transparency still requires a source manifest, file hash policy, normalization rules, and row-count audit.

## SECTION 7 - Gap Analysis

| gap | severity | assessment |
| --- | --- | --- |
| Field-level mapping uncertainty | Critical | Integration design cannot proceed to implementation until exact CRSP fields are mapped to required schema fields. |
| Licensing constraints | Critical | Source acceptance is impossible until research retention, derived artifacts, hashing, and audit rights are understood. |
| Archival constraints | Critical | PIT reproducibility requires release files or controlled references, source versioning, and hashes. |
| Known-date handling | Critical | Event effective date and known/as-of date must remain separate to avoid look-ahead. |
| Event-window representation | Critical | Ticker, name, exchange, delisting, merger, spin-off, and relisting windows need exact date semantics. |
| Source-version tracking | Moderate | CRSP has release notes and release cadence; project-specific version fields still need design. |
| Internal id policy | Moderate | Need decide how `PERMNO`/`PERMCO` map to internal namespaced ids. |
| Share-class handling | Moderate | Must verify how share classes and multiple securities per company are represented. |
| Country/currency/security-type fields | Moderate | Required scaffold fields may need explicit unknown/null handling if CRSP does not provide them directly. |
| Manual override policy | Minor | CRSP should reduce manual repair, but unresolved edge cases need override rules. |

## SECTION 8 - Integration Design Readiness

If CRSP access existed today, would the project be ready to begin a CRSP-specific integration design?

Yes. The project is ready to begin CRSP-specific integration design because:

- CRSP has passed source-candidate evaluation as `ACCEPTED_FOR_LINEAGE_EVALUATION`.
- CRSP's public characteristics align strongly with security identity and ticker lineage needs.
- The source-gate framework, policy vocabulary, semantic controls, and PIT schema scaffold are already in place.
- The remaining unknowns are exactly the kinds of questions an integration design should answer: field mapping, known-date semantics, release/source lineage, licensing, and archive policy.

The project is not ready to ingest CRSP data, load CRSP files, construct metadata, build lineage, or accept CRSP as a source.

## SECTION 9 - Final Classification

Final classification: `SUITABLE_FOR_INTEGRATION_DESIGN`.

Rationale:

- CRSP appears highly compatible with the architecture's identity and ticker-lineage requirements.
- Public documentation supports survivor-bias-free history, active/inactive coverage, permanent identifiers, corporate actions, delisting information, exchange coverage, release notes, metadata guides, and flat-file formats.
- Remaining gaps are substantial but design-addressable.
- None of the unresolved issues make CRSP unsuitable for integration design.
- Source acceptance and implementation remain blocked.

## SECTION 10 - Final Recommendation

1. Does CRSP appear capable of supporting `security_master_pit`?

Yes. CRSP appears capable of supporting `security_master_pit` design because `PERMNO`, `PERMCO`, active/inactive coverage, exchange coverage, identifying information, delisting information, and corporate actions align strongly with Project Underdog's identity-continuity requirements.

2. Does CRSP appear capable of supporting `ticker_lineage_pit`?

Yes, with design gaps. CRSP appears capable of supporting `ticker_lineage_pit`, especially because permanent identifiers reduce ticker ambiguity. The largest design work is translating CRSP's historical ticker/name/exchange/event records into explicit ticker windows without look-ahead.

3. What are the largest remaining lineage unknowns?

The largest unknowns are exact ticker-window fields, event effective versus known-date semantics, predecessor/successor event mapping, exchange-change handling, ticker reuse representation, source archive/hash policy, and licensing constraints.

4. What must be verified before integration design?

Before integration design proceeds deeply, the project must verify available CRSP documentation, subscription scope, license/retention constraints, release-file availability, source version policy, exact field inventory, and whether CRSP records can support required as-of/effective-date semantics.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - CRSP Integration Design Specification v1**. It should design CRSP-specific field-mapping questions, lineage architecture choices, source manifest requirements, release/hash policy, known-date handling, ticker-window construction rules, and gap-resolution workflow. It should not ingest data, load CRSP files, accept CRSP as a source, construct metadata, build security lineage, build ticker lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.

## Source References

- CRSP US Stock Databases: `https://www.crsp.org/research/crsp-us-stock-databases/`
- CRSP Research Data Products: `https://www.crsp.org/research/`
