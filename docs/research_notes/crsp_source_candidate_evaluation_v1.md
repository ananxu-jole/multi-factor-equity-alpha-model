# Project Underdog - CRSP Source Candidate Evaluation v1

## SECTION 1 - Executive Summary

Evaluation scope:

- `security_master_pit`
- `ticker_lineage_pit`

Candidate source:

`CRSP US Stock Databases`

Evaluation outcome:

`ACCEPTED_FOR_LINEAGE_EVALUATION`

This means CRSP appears eligible for deeper lineage-design work. It does not mean CRSP is accepted, approved, loaded, ingested, integrated, or authorized for metadata construction.

Key strengths:

- CRSP publicly describes the US Stock Databases as covering daily and monthly market data plus corporate actions for more than 32,000 active and inactive U.S. securities.
- CRSP identifies the database as survivor-bias-free and appropriate for longitudinal research and back-testing.
- CRSP permanent identifiers `PERMNO` and `PERMCO` are designed to track securities and companies over time.
- Product materials explicitly include security delisting information, corporate actions, identifiers, descriptors, supplemental data items, release notes, metadata guides, and flat-file delivery formats.
- Exchange coverage is publicly documented for NYSE, NYSE American, NASDAQ, NYSE Arca, and Cboe BZX.

Key concerns:

- No CRSP source files were loaded or inspected, so exact field-level mapping remains unverified.
- Licensing, retention, redistribution, and audit-artifact rights must be reviewed before any source acceptance.
- Exact ticker-window representation, name history fields, exchange-history fields, event as-of dates, and source hash retention must be confirmed.
- CRSP is U.S.-equity focused; any non-U.S. or non-equity scope would require separate source evaluation.

## SECTION 2 - Candidate Source Profile

Source category:

Professional/institutional historical U.S. equity security database with permanent identifiers, active/inactive coverage, delisting information, and corporate-action history.

Intended PIT use:

CRSP is being evaluated only as a candidate source for future `security_master_pit` and `ticker_lineage_pit` design. It is not being evaluated for sector history, industry history, size history, peer reconstruction, economic-context discovery, alpha discovery, validation, production, or ML.

Expected security-master support:

- Strong expected support for stable security identity through `PERMNO`.
- Strong expected company continuity through `PERMCO`.
- Strong expected active/inactive coverage for U.S. listed securities.
- Potential support for company/security identifying information, descriptors, exchange coverage, delisting information, and corporate actions.

Expected ticker-lineage support:

- Strong expected support because CRSP identifiers are built for time-series and corporate-event continuity.
- Formal field review must confirm ticker effective windows, name windows, exchange windows, ticker reuse behavior, and event known-date fields.

Expected identifier support:

- `PERMNO`: permanent issue identifier.
- `PERMCO`: permanent company identifier.
- Public product descriptions also reference identifiers, descriptors, and supplemental data items.

Expected historical coverage:

CRSP publicly documents exchange coverage beginning on:

- NYSE: December 31, 1925.
- NYSE American: July 2, 1962.
- NASDAQ: December 14, 1972.
- NYSE Arca: March 8, 2006.
- Cboe BZX: January 24, 2012.

No source data was loaded for this evaluation.

## SECTION 3 - Framework Assessment

| framework criterion | assessment | preliminary score |
| --- | --- | ---: |
| Effective-date support | Strong expected support from historical databases, corporate actions, delisting information, release files, and time-series identifiers. Exact effective/as-of field mapping remains unverified. | 2 |
| PIT integrity | Strong public evidence: survivor-bias-free historical database, active/inactive securities, release cadence, and longitudinal research orientation. | 3 |
| Identifier continuity | Strong: `PERMNO` and `PERMCO` are permanent identifiers intended to track securities and companies over time. | 3 |
| Ticker-lineage support | Strong expected support, but exact ticker-window, ticker-reuse, and exchange-window mechanics require field-level review. | 2 |
| Corporate-action support | Strong: corporate actions are an explicit product feature. | 3 |
| Auditability | Strong expected support through user guide, metadata guide, release notes, delivery formats, and subscription process. Exact artifact retention rights require licensing review. | 2 |
| Reproducibility | Strong expected support through monthly/quarterly/annual releases and flat-file formats. Source file hash retention and license terms remain unresolved. | 2 |
| Coverage | Strong for U.S. listed equities, including active and inactive securities across major exchanges. | 3 |
| Lineage transparency | Strong expected support through permanent identifiers and product documentation, but source record-level lineage must be verified. | 2 |
| Maintenance burden | Moderate. Professional release cadence and flat files help, but integration and schema migration from CRSP formats require care. | 2 |
| Implementation complexity | Moderate. CRSP is rich and research-oriented, but mapping CRSP fields into project schemas will require careful design. | 2 |
| Licensing considerations | Manual review required. Subscription, retention, audit, and redistribution terms must be checked before source acceptance. | 1 |

Source-gate score preview:

| score field | preliminary score | rationale |
| --- | ---: | --- |
| `pit_integrity_score` | 3 | Public product description supports survivor-bias-free historical research use. |
| `coverage_score` | 3 | Active and inactive U.S. securities across major exchanges. |
| `historical_depth_score` | 3 | Long exchange coverage back to 1925 for NYSE and later for additional venues. |
| `identifier_quality_score` | 3 | `PERMNO` and `PERMCO` are strong permanent identifiers. |
| `update_feasibility_score` | 2 | Product has release cadence; operational access still needs subscription setup. |
| `source_stability_score` | 3 | CRSP is an established institutional research-data source. |
| `implementation_complexity_score` | 2 | Rich data model and schema mapping need design work. |
| `cost_manual_burden_score` | 2 | Likely manageable but requires licensing/access and mapping work. |
| `leakage_risk_score` | 3 | Survivor-bias-free orientation and permanent identifiers reduce leakage risk. |

Weighted framework result:

CRSP meets the threshold for `STRONG_CANDIDATE`, subject to licensing and field-level review. The appropriate source-gate decision is `ACCEPTED_FOR_LINEAGE_EVALUATION`, not source acceptance.

## SECTION 4 - Historical Integrity Review

Survivorship-bias risk:

Low expected risk. CRSP explicitly describes the US Stock Databases as survivor-bias-free and including active and inactive U.S. securities.

Identifier continuity risk:

Low expected risk. `PERMNO` and `PERMCO` are designed to support historical continuity for securities and companies. Formal evaluation must still confirm how these map into Project Underdog's `security_id`, issuer id, predecessor/successor fields, and event lineage fields.

Ticker-history quality:

Medium-low expected risk. Public CRSP materials strongly support historical identifying information and corporate-event continuity, but exact ticker effective-window fields and ticker reuse handling must be reviewed in product documentation or candidate manifest materials before acceptance.

Delisting support:

Strong expected support. Security delisting information is an explicit CRSP US Stock Databases key data item.

Merger/spin-off continuity support:

Strong expected support at the identifier-continuity level because CRSP describes `PERMNO` as supporting tracking across corporate restructurings, including mergers, acquisitions, spin-offs, and other business events. Exact event fields and as-of-date treatment must be verified.

## SECTION 5 - Source-Gate Evaluation

Schema compatibility:

Likely compatible for candidate evaluation. CRSP appears capable of filling core source acceptance manifest concepts: source name, source version/release, source snapshot/release date, source file reference, historical depth, identifiers, coverage, corporate actions, delisting information, and review notes. Exact source file hash and source record id strategy remain unresolved.

Policy compatibility:

Likely compatible with the PIT policy layer if CRSP source terms allow research retention and reproducible audit artifacts. Licensing review is mandatory before any source acceptance.

Semantic compatibility:

Likely compatible with `lineage_only` as the intended allowed use. CRSP should remain blocked from sector/industry/size/peer/economic-context discovery use in this phase.

Allowed-use compatibility:

Recommended allowed use for formal evaluation:

`identity_ticker_lineage`

Canonical allowed use:

`lineage_only`

Confidence expectations:

Expected confidence tier: `high` for source category and public product fit, pending licensing and field-level documentation. Candidate manifest should use a conservative confidence note until exact field mapping is reviewed.

Manual-review triggers:

- Licensing and retention rights.
- Exact field mapping to `security_master_pit`.
- Exact field mapping to `ticker_lineage_pit`.
- Source file hash and release artifact retention process.
- Ticker effective windows and ticker reuse handling.
- Event effective date versus event known/as-of date distinction.
- Treatment of name changes, exchange changes, share classes, predecessor/successor relationships, and delisting codes.

No ingestion, source loading, or source-file access was performed.

## SECTION 6 - Risks and Unknowns

Missing information:

- Exact subscribed CRSP product/package and release format.
- License terms for local retention, source hashing, derived artifacts, and research audit notes.
- Candidate source manifest row.
- Field-level mapping to `security_master_pit`.
- Field-level mapping to `ticker_lineage_pit`.
- Name-history and exchange-history fields.
- Ticker effective-window fields.
- Event as-of-date and effective-date separation.
- Source record id strategy.
- Raw file hash strategy.

Unresolved questions:

- Does the available CRSP package expose all required security identity fields for the aligned scaffold schema?
- Does the available CRSP package expose ticker lineage as explicit windows or as name/history records requiring deterministic transformation?
- How should CRSP `PERMNO` and `PERMCO` map to internal `security_id` and issuer fields?
- Can CRSP releases be retained in a way compatible with Project Underdog's reproducibility policy?
- Are there any constraints on storing derived security master and ticker lineage artifacts?

Licensing unknowns:

- Subscription scope.
- Research retention rights.
- Redistribution restrictions.
- Derived artifact retention.
- Source file hashing and archive retention.
- Use in future research/discovery artifacts.

Implementation risks:

- Misinterpreting `PERMNO`/`PERMCO` versus issuer/security/share-class semantics.
- Treating historical name or ticker records as full ticker effective windows without confirming date semantics.
- Failing to distinguish event effective dates from known/as-of dates.
- Overextending CRSP beyond U.S. equity scope.

Reproducibility concerns:

- Raw release files must be retained or referenced reproducibly.
- Source version, release date, source file hash, and normalization rules must be captured.
- Any transformation into internal PIT windows must be deterministic and audited.

## SECTION 7 - Preliminary Decision

Decision:

`ACCEPTED_FOR_LINEAGE_EVALUATION`

Decision meaning:

CRSP appears credible enough to proceed to deeper lineage-evaluation design for `security_master_pit` and `ticker_lineage_pit`.

Decision non-meaning:

This does not mean:

- accepted source
- approved source
- source integration authorized
- CRSP ingestion authorized
- CRSP file loading authorized
- metadata construction authorized
- security lineage construction authorized
- ticker lineage construction authorized
- discovery or validation authorized

Allowed next step:

Prepare a formal CRSP source-gate evaluation design and candidate manifest plan using public/source documentation only unless a later task explicitly authorizes access review.

Blocked next steps:

- source loading
- ingestion
- source acceptance
- metadata construction
- security lineage construction
- ticker lineage construction
- sector/industry/peer reconstruction
- discovery
- refinement
- validation
- governance mutation
- threshold changes
- production registration
- ML

## SECTION 8 - Recommendation

1. Does CRSP appear suitable for `security_master_pit`?

Yes. CRSP appears suitable for deeper `security_master_pit` lineage-design work because its permanent identifiers, active/inactive coverage, historical depth, delisting information, corporate actions, and documented exchange coverage align strongly with the identity foundation Project Underdog needs.

2. Does CRSP appear suitable for `ticker_lineage_pit`?

Yes, with field-level review required. CRSP appears suitable for deeper `ticker_lineage_pit` design because of its permanent identifiers, identifying information, corporate-event orientation, and delisting support. Exact ticker-window, ticker-reuse, exchange-change, and event-as-of mechanics must be verified before source acceptance.

3. What are the largest remaining unknowns?

The largest remaining unknowns are licensing/retention rights, exact subscribed product scope, field-level mapping to `security_master_pit` and `ticker_lineage_pit`, ticker effective-window representation, event known-date treatment, and source-file hash/archive feasibility.

4. What must be verified before source acceptance?

Before source acceptance, the project must verify:

- license allows research retention and audit artifacts
- source release files can be retained or referenced reproducibly
- source versions, release dates, hashes, and record counts can be captured
- `PERMNO`/`PERMCO` mapping rules are correct for internal identity
- ticker history can be represented as PIT windows
- delisting and corporate-action events can be represented with effective/as-of logic
- coverage can be measured by active ticker-date
- manual overrides are unnecessary or explicitly bounded

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - CRSP Source-Gate Evaluation Design and Manifest Plan v1**. It should design the CRSP candidate manifest, field-mapping questions, licensing checklist, source-lineage artifact plan, and formal evaluation workflow. It should not ingest data, load CRSP source files, accept or reject CRSP as a source, construct metadata, build security lineage, build ticker lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.

## Source References

- CRSP US Stock Databases: `https://www.crsp.org/research/crsp-us-stock-databases/`
- CRSP Research Data Products: `https://www.crsp.org/research/`
