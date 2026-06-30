# Project Underdog - Security Master and Ticker Lineage Source Candidate Survey v1

## SECTION 1 - Executive Summary

Current PIT readiness state: the source-gate framework is ready for source evaluation, but the first placeholder source evaluation ended as `DEFERRED_PENDING_SOURCE_INFO` because no real source candidate description was available. The project has source-gate scaffolding, semantic validation, allowed-use controls, and evaluation artifacts, but it has not accepted, loaded, ingested, or constructed metadata from any source.

Purpose of this survey: identify and compare source categories that could potentially support `security_master_pit` and `ticker_lineage_pit` before selecting a first real source candidate for formal source-gate evaluation.

Evaluation constraints:

- Category-level survey only.
- No source ingestion.
- No source loading.
- No real source acceptance or rejection.
- No metadata construction.
- No security or ticker lineage construction.
- No sector/industry/size/peer reconstruction.
- No discovery, refinement, validation, governance mutation, production registration, or ML.

Expected outcome: recommend a `FIRST_SOURCE_CANDIDATE_CLASS` for formal source evaluation. This recommendation is not a source acceptance decision and does not select a vendor.

## SECTION 2 - Candidate Source Category Inventory

| source category | description | survey status |
| --- | --- | --- |
| Exchange/reference-data sources | Exchange, listing, security reference, symbol-change, and delisting-oriented records. | Candidate category; potentially strong for listing/ticker events if historical depth is available. |
| Security master providers | Professional or institutional security master products with stable identifiers, active/inactive windows, corporate-action handling, and ticker mappings. | Candidate category; likely strongest first candidate class if PIT and audit features are available. |
| Historical ticker-history providers | Sources focused on ticker changes, symbol history, exchange changes, delistings, and reuse. | Candidate category; strong complement to security master, but may lack full identity fields. |
| Historical corporate-action datasets | Event datasets covering mergers, acquisitions, spin-offs, delistings, name changes, exchange changes, and share-class events. | Candidate category; valuable for continuity repair and diagnostics, less likely sufficient alone. |
| Classification/taxonomy providers | Sector/industry classification history and taxonomy-version sources. | Deferred for this phase; relevant later after identity/ticker lineage is credible. |
| Public reference datasets | Public security/ticker/reference snapshots or registries. | Candidate category for diagnostics; often weaker for PIT lineage, reproducibility, and historical depth. |
| Manually curated datasets | Human-maintained event or mapping files. | Diagnostic or repair category only unless bounded, dated, reviewed, and reproducible. |
| Internally reconstructed datasets | Deterministic reconstruction from archived dated inputs. | Potentially acceptable if raw inputs, dates, hashes, and rules are auditable; high implementation burden. |

No specific vendor is selected by this survey.

## SECTION 3 - Evaluation Criteria

Comparison criteria for source categories:

| criterion | evaluation meaning |
| --- | --- |
| Effective-date support | Whether records provide effective start/end, event date, known-as-of date, or repeatable dated snapshots. |
| Historical depth | Whether the source can cover the research period needed for later PIT discovery readiness. |
| Identifier continuity | Whether stable identifiers, issuer identifiers, exchange, share class, and status history support continuity. |
| Ticker-history support | Whether ticker changes, reuse, exchange changes, relistings, and delistings are represented. |
| Auditability | Whether source version, snapshot date, source hash/reference, review timestamp, and lineage can be retained. |
| Reproducibility | Whether raw source references and transformations can be rerun or independently reviewed. |
| Coverage | Whether active ticker-date coverage is broad enough for the research universe and measurable by date. |
| Lineage transparency | Whether security identity, ticker mapping, event lineage, and manual overrides are explainable. |
| Maintenance burden | Expected recurring update, normalization, event repair, and review effort. |
| Licensing uncertainty | Risk that source retention, redistribution, or research use is restricted. |
| Implementation complexity | Effort required to map the source into `security_master_pit`, `ticker_lineage_pit`, and `metadata_source_lineage`. |

## SECTION 4 - Candidate Category Assessment

| category | strengths | weaknesses | PIT suitability | lineage suitability | likely source-gate outcome | major risks |
| --- | --- | --- | --- | --- | --- | --- |
| Exchange/reference-data sources | Primary listing facts; exchange/ticker event authority; useful delisting and symbol-change context. | May be fragmented by exchange; may not provide issuer/security continuity across venues or corporate actions. | Medium to high if historical dated records exist. | Strong for ticker and exchange continuity; moderate for stable security identity. | `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` or `ACCEPTED_FOR_LINEAGE_EVALUATION` depending on dates, identifiers, and reproducibility. | Multi-exchange normalization, ticker reuse, share-class ambiguity. |
| Security master providers | Stable identifiers; security and issuer continuity; ticker mappings; status windows; corporate-action context. | Licensing, cost, schema complexity, and possible opaque vendor logic. | High if point-in-time or dated snapshots are available. | High for identity and ticker lineage if effective windows are explicit. | Most likely `ACCEPTED_FOR_LINEAGE_EVALUATION` after formal evaluation if audit requirements pass. | Licensing, black-box corrections, source retention limits. |
| Historical ticker-history providers | Deep symbol-change focus; useful for ticker changes, reuse, exchange moves, and delistings. | May lack stable security identifiers, issuer linkage, or full corporate-action continuity. | Medium to high for ticker lineage; lower for security master alone. | High for ticker lineage, moderate for identity continuity. | Likely `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` or lineage supplement unless stable ids are present. | Ticker-only identity, recycled tickers, missing share-class resolution. |
| Historical corporate-action datasets | Strong event context for mergers, acquisitions, spin-offs, delistings, name changes, and exchange moves. | Event-centric rather than full-state; may require joining to another identity source. | Medium as supplement; low as standalone source. | High for continuity repair, not enough for complete security master. | Likely conditional or diagnostic supplement. | Event coverage gaps, event-date/as-of-date ambiguity. |
| Classification/taxonomy providers | Important later for sector/industry history and taxonomy drift. | Not a first-phase identity source; may carry weak identifiers. | Deferred for identity/ticker phase. | Low for ticker lineage. | Should remain out of first identity/ticker evaluation unless bundled with security master. | Premature sector/industry focus before identity lineage. |
| Public reference datasets | Accessible; useful for initial diagnostics and cross-checks. | Often static, incomplete, current-biased, or weakly reproducible. | Low to medium; usually diagnostic-only unless dated archive exists. | Low to medium. | Likely `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` or `DEFERRED_PENDING_SOURCE_INFO`. | Survivorship bias, static snapshots, unclear lineage. |
| Manually curated datasets | Can resolve narrow edge cases and known ticker/security breaks. | High leakage and reproducibility risk if not dated and reviewed. | Low as primary; useful as bounded override layer later. | Low to medium for specific repairs only. | Likely diagnostics/manual review only. | Manual bias, incomplete audit trail, dominance risk. |
| Internally reconstructed datasets | Fully controlled logic if based on archived dated inputs; reproducible if manifests are complete. | High engineering effort; quality depends on raw archives; inferred windows can be fragile. | Medium to high if inputs are truly dated and retained. | Medium to high with strong rules and diagnostics. | Likely `MANUAL_REVIEW_REQUIRED` first, then conditional if scope is machine-readable. | Hidden leakage, reconstruction assumptions, maintenance burden. |

## SECTION 5 - Security Master Suitability Review

Best-suited categories for security identity:

1. Security master providers.
2. Exchange/reference-data sources paired with issuer/security identifiers.
3. Internally reconstructed datasets from dated identity archives.
4. Corporate-action datasets as supplementary continuity evidence.

Security continuity:

- Security master providers are strongest if they provide stable identifiers, active/inactive windows, issuer linkage, share-class fields, source versioning, and dated records.
- Exchange/reference sources can help but may require cross-exchange normalization and additional corporate-action linkage.
- Internally reconstructed sources are viable only if raw dated inputs and deterministic rules are retained.

Exchange continuity:

- Exchange/reference-data sources are strongest for listing venue and exchange-change evidence.
- Security master providers may be strong if exchange history is explicit rather than current-state only.

Name continuity:

- Security master providers and corporate-action datasets are best suited.
- Name history is useful but should not outrank stable identifiers and ticker lineage in the first evaluation.

## SECTION 6 - Ticker Lineage Suitability Review

Best-suited categories for ticker changes:

1. Historical ticker-history providers.
2. Security master providers with explicit ticker windows.
3. Exchange/reference-data sources with symbol-change archives.
4. Corporate-action datasets as event supplements.

Ticker reuse detection:

- Historical ticker-history providers and exchange/reference-data sources are strongest if they distinguish exchange, share class, security id, and non-overlapping windows.
- Public reference datasets are risky because current ticker state may obscure historical reuse.

Delisting support:

- Exchange/reference-data sources and security master providers are likely strongest.
- Corporate-action datasets can improve event rationale but may not provide complete active/inactive windows.

Merger support:

- Corporate-action datasets are strongest for event rationale and predecessor/successor links.
- Security master providers are strongest if they combine event references with stable security ids.

Spin-off support:

- Corporate-action datasets are useful for event context.
- Security master providers are required to safely link predecessor and successor securities.

Corporate-action continuity:

- No single category should be assumed sufficient without formal source-gate evaluation.
- The most robust path is security master provider first, then ticker-history and corporate-action supplements if gaps remain.

## SECTION 7 - Risk Ranking

| risk | severity | highest-risk categories | assessment |
| --- | --- | --- | --- |
| Historical-integrity risk | High | Public reference, manual curated, internally reconstructed | Static snapshots or inferred windows can leak current identity into past dates. |
| Survivorship-bias risk | High | Public reference, classification/taxonomy, manual curated | Current active universes can omit dead/delisted securities. |
| Identifier ambiguity risk | High | Historical ticker-history, exchange/reference, public reference | Ticker-only records can confuse share classes, exchange moves, and recycled tickers. |
| Licensing risk | Moderate-high | Security master providers, corporate-action datasets, exchange/reference | Retention, redistribution, and reproducibility limits may block use. |
| Maintenance burden | Moderate-high | Internally reconstructed, manual curated, exchange/reference | Ongoing updates and event repair can become expensive. |
| Reproducibility risk | High | Manual curated, public reference, internally reconstructed without archives | Missing raw files, hashes, or dated snapshots prevents auditability. |

Largest cross-category risk: confusing ticker history with security identity. A source can know what a ticker did without reliably identifying the economic security behind each ticker/date.

## SECTION 8 - Recommended First Candidate Class

Recommended `FIRST_SOURCE_CANDIDATE_CLASS`:

`professional_or_institutional_security_master_with_point_in_time_or_dated_snapshot_ticker_lineage`

Rationale:

- It is the most likely category to support both `security_master_pit` and `ticker_lineage_pit` in one evaluation path.
- It is best aligned with the first implementation phase: security identity before sector, industry, size, peer reconstruction, or discovery.
- It can potentially provide stable security ids, issuer ids, ticker mappings, active/inactive windows, exchange continuity, share-class information, and event context.
- If the source is truly point-in-time or based on retained dated snapshots, it has the best chance of passing source-gate auditability requirements.

Required caveat:

This is a category recommendation only. No source is accepted, rejected, loaded, ingested, or selected. Any real candidate must still pass formal source-gate evaluation and may still be deferred, rejected, diagnostic-only, conditional, or manual-review-required.

Secondary candidate class:

`historical_ticker_history_source_with_stable_security_identifiers`

This should be considered if no integrated security master candidate is available, but it should be treated as a ticker-lineage candidate first and not assumed sufficient for security identity.

## SECTION 9 - Remaining Unknowns

Missing information:

- Which candidate sources are available to the project.
- Whether candidate sources provide true effective dates or only source snapshots.
- Whether historical raw files can be retained or referenced reproducibly.
- Whether source licensing allows research retention and audit artifacts.
- Whether stable security identifiers are available across delistings, mergers, spin-offs, and share-class changes.
- Whether ticker reuse and exchange changes are represented explicitly.
- Whether source coverage matches the research universe by date.

Unresolved source questions:

- Does the source distinguish event effective date from known-as-of date?
- Does the source track active/inactive security windows?
- Does the source retain predecessor/successor links for corporate actions?
- Does the source expose taxonomy/classification fields bundled with identity, and if so can they be ignored for the identity-only phase?
- Does the source require manual repair, and can manual repair be bounded and audited?

Future evaluation requirements:

- Candidate source description.
- Candidate source manifest row.
- Source category/type.
- Historical depth summary.
- Effective-date/as-of-date support.
- Identifier/ticker-history capability summary.
- Licensing and reproducibility notes.
- Expected coverage and known limitations.
- Intended allowed use, likely `lineage_only` or narrower.
- Confidence rationale and manual-review flags.

## SECTION 10 - Final Recommendation

1. Which source category is most promising?

The most promising category is a professional or institutional security master with point-in-time or retained dated-snapshot ticker lineage.

2. Which source categories should be avoided initially?

Avoid public static reference datasets, manually curated datasets as primary sources, current profile APIs, and classification/taxonomy providers for the first identity/ticker lineage source candidate. These may be useful later for diagnostics or sector/industry work, but they are not the right first identity foundation.

3. Which category best supports security identity?

Security master providers best support security identity, especially when they include stable security ids, issuer ids, share-class handling, active/inactive windows, exchange fields, and source-versioned dated records.

4. Which category best supports ticker lineage?

Historical ticker-history providers best support ticker changes and reuse detection, but the best first candidate class is an integrated security master that also provides explicit ticker lineage. That reduces the risk of ticker-only identity ambiguity.

5. What is the largest remaining uncertainty?

The largest remaining uncertainty is whether an available candidate source can provide both stable security identity and auditable historical ticker windows with effective dates or reproducible dated snapshots, while also satisfying licensing and retention requirements.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Security Master and Ticker Lineage First Source Candidate Intake Package v1**. It should prepare a source description and candidate manifest package for one source in the recommended first candidate class. It should not ingest data, load source files, accept or reject a real source, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.
