# Project Underdog - PIT Security Master and Ticker Lineage Source Evidence and License Review v1

## SECTION 1 - Executive Summary

This documentation-only review evaluated public source documentation and existing Project Underdog notes to determine whether candidate metadata sources have enough public evidence to support future ingestion design.

Overall classification: `SOURCE_EVIDENCE_READY_WITH_LICENSE_BLOCKERS`.

No source data was accessed. No downloads, API calls, external database connections, ingestion, PIT table construction, alpha implementation, panel generation, IC computation, governance mutation, production change, or ML work was performed.

Result:

- CRSP Stock Names / Security Master / Delisting is the strongest first ingestion-design target, but only after license, subscription entitlement, retention, archive/hash, known-date, and official field evidence are supplied.
- WRDS CRSP-Compustat Link is a strong complement for CRSP-to-Compustat issuer linkage, but not a standalone ticker-lineage source.
- Compustat security/company metadata is useful for issuer and company attributes, but not sufficient as a primary security master or ticker-lineage source.
- Exchange/vendor listing-delisting datasets are potentially useful supplements, but public documentation is too fragmented for primary-source ingestion design.
- OpenFIGI is useful for identifier crosswalk diagnostics, but public documentation does not establish historical PIT ticker lineage.
- yfinance metadata remains diagnostic-only because it is current/API-oriented, externally rate/terms dependent, and explicitly tied to Yahoo data-use constraints.

## SECTION 2 - Materials Reviewed

Existing project notes reviewed:

- `docs/research_notes/pit_security_master_ticker_lineage_source_candidate_evaluation_v1.md`
- `docs/research_notes/security_master_ticker_lineage_source_candidate_evaluation_framework_v1.md`
- `docs/research_notes/security_master_ticker_lineage_source_candidate_survey_v1.md`
- `docs/research_notes/crsp_external_evidence_verification_v1.md`
- `docs/research_notes/crsp_external_verification_requirements_package_v1.md`
- `artifacts/research/crsp_security_master_ticker_lineage_pit_v1/assumptions/crsp_license_retention_review.csv`
- `artifacts/research/crsp_security_master_ticker_lineage_pit_v1/assumptions/crsp_field_availability_review.csv`

Public documentation reviewed:

- CRSP public product documentation and CRSP/Compustat Merged Database descriptions, including CRSP US Stock Database coverage, permanent identifiers, active/inactive securities, corporate actions, and CRSP/Compustat link descriptions.
- WRDS/CRSP/Compustat public descriptions available through CRSP product-level documentation.
- OpenFIGI API and overview documentation, including mapping API behavior, static outputs, permanent FIGI behavior, open-data positioning, and API usage model.
- yfinance PyPI/project documentation, including Yahoo affiliation disclaimer, research/educational framing, and Yahoo data-use caveats.
- Exchange public documentation examples, including NYSE market status / symbol distribution references and public exchange data-policy pages.

Public URLs used as evidence references:

- `https://www.crsp.org/`
- `https://www.openfigi.com/about/overview`
- `https://www.openfigi.com/api/overview`
- `https://pypi.org/project/yfinance/`
- `https://www.nyse.com/market-status/history`

## SECTION 3 - Source Readiness Summary

| source_id | classification | ingestion-design sufficiency | main blockers |
| --- | --- | --- | --- |
| `crsp_stocknames_delisting_security_master` | `READY_PENDING_LICENSE` | Public evidence is sufficient to begin an ingestion-design outline once license and entitlement evidence are supplied. | License, retention, subscription scope, archive/hash rights, official field dictionary, known-date semantics. |
| `wrds_crsp_compustat_link` | `READY_PENDING_LICENSE` | Sufficient as a complementary design target after CRSP primary-source gating. | License, WRDS/CRSP/Compustat entitlements, link-history field semantics, date-window interpretation. |
| `compustat_security_company_metadata` | `READY_PENDING_LICENSE` | Sufficient for secondary issuer/company metadata design, not primary ticker lineage. | License, table entitlement, field dictionary, PIT/security-history semantics, dependence on CRSP or another identity source. |
| `exchange_vendor_listing_delisting_datasets` | `DOCUMENTATION_INSUFFICIENT` | Not sufficient for primary ingestion design; can support future supplemental-source evaluation. | Fragmented public docs, vendor-specific licensing, historical depth, stable identifier continuity, reproducible archives. |
| `openfigi_identifier_documentation` | `DIAGNOSTIC_ONLY` | Sufficient for crosswalk diagnostic design only. | Static/current mapping posture, no complete PIT ticker lineage, no delisting/listing event history guarantee. |
| `yfinance_metadata` | `DIAGNOSTIC_ONLY` | Sufficient only for diagnostic/current-profile comparison. | Yahoo data-use terms, personal-use caveat, current API behavior, no authoritative PIT lineage. |

Interpretation:

The source universe is ready for a first ingestion-design planning pass only if the design is explicitly license-gated and assumption-bound. It is not ready for source loading, source inspection, ingestion, PIT construction, or alpha use.

## SECTION 4 - Source-by-Source Evidence Review

### `crsp_stocknames_delisting_security_master`

Intended purpose:

Primary security identity, ticker history, listing/delisting state, permanent security/company identifiers, and survivor-bias control.

Publicly documented coverage:

CRSP public product material describes the CRSP US Stock Database as daily and monthly market data and corporate actions for more than 32,000 active and inactive U.S. securities, covering NYSE, NYSE American, NYSE Arca, NASDAQ, and Cboe BZX securities. It also identifies PERMNO and PERMCO as permanent identifiers and describes CRSP history as supporting longitudinal research and backtesting.

PIT suitability:

High conceptual suitability. Active/inactive coverage, permanent identifiers, and corporate-action framing are directionally aligned with PIT security master needs. However, public documentation alone does not prove field-level effective windows, source release dates, event known dates, or the project's actual subscribed table access.

Identifier support:

Strong. Public documentation supports PERMNO as a permanent security identifier and PERMCO as a permanent company identifier.

Lineage support:

Strong but not fully verified. Public materials support name/security continuity, corporate actions, and active/inactive securities. Official field dictionaries or authorized schema evidence are still required for ticker start/end windows, delisting fields, exchange history, share-class handling, and ticker reuse diagnostics.

Licensing model:

Professional/subscription source. Public documentation describes CRSP as a subscribed research data product; it does not resolve the project's license, retention, archival, redistribution, or hash rights.

Reproducibility considerations:

Future ingestion design must require source version or extract date, file/table manifest, row counts, archive or controlled-reference policy, and license-approved hashing or controlled source references.

Known limitations:

Public docs are supportive but not enough to prove local entitlement, exact fields, known-date semantics, retention rights, or raw-file audit rights.

Documentation sufficiency:

`READY_PENDING_LICENSE`. Sufficient to prepare a license-gated ingestion-design outline, not sufficient to load, ingest, or construct.

### `wrds_crsp_compustat_link`

Intended purpose:

Issuer/company bridge between CRSP security identifiers and Compustat company/fundamental identifiers.

Publicly documented coverage:

CRSP public descriptions of the CRSP/Compustat Merged Database state that it links CRSP stock data with Compustat data and maps complex relationships between CRSP and Compustat identifiers over time. The described key identifiers include CRSP PERMNO/PERMCO and Compustat GVKEY.

PIT suitability:

Moderate to high as a bridge if link history date windows and link types are available and license-approved. It is not a standalone PIT ticker-lineage source.

Identifier support:

Strong for CRSP-to-Compustat linkage. Expected identifier concepts include PERMNO, PERMCO, and GVKEY, with possible link metadata requiring official documentation.

Lineage support:

Strong for issuer/company bridge lineage, weak as primary security/ticker lineage. Link history can support date-bounded joins, but it must not replace CRSP stock-name/ticker lineage.

Licensing model:

Professional/subscription source, likely dependent on both CRSP/WRDS and Compustat entitlement terms.

Reproducibility considerations:

Requires versioned link-table documentation, link date-window semantics, link type/priority rules, and reproducible source references.

Known limitations:

Not all securities may link cleanly to Compustat. Link windows and link quality require careful interpretation. It cannot provide delisting or recycled ticker controls by itself.

Documentation sufficiency:

`READY_PENDING_LICENSE`. Sufficient to include as a secondary ingestion-design target after CRSP primary identity scope is license-cleared.

### `compustat_security_company_metadata`

Intended purpose:

Company and security metadata, issuer identifiers, company attributes, and future support for financial or classification joins.

Publicly documented coverage:

Public descriptions identify Compustat as company/security and fundamentals-oriented data with global companies, active/inactive coverage references in secondary public descriptions, and identifiers such as GVKEY, CUSIP, ISIN, SEDOL, and ticker-like fields. The strongest public evidence available in this pass was product/category-level rather than official field-level documentation.

PIT suitability:

Moderate for company/security metadata when point-in-time or dated table semantics are verified. Weak as a primary ticker-lineage source.

Identifier support:

Strong for company identifiers such as GVKEY and security-level identifiers where licensed tables provide them. CRSP or another security master is still needed for robust market-security identity.

Lineage support:

Moderate for company/security attributes and issuer linkage. Weak for listing/delisting and recycled ticker handling as a standalone source.

Licensing model:

Professional/subscription source through S&P Global/WRDS-style institutional access. Public evidence does not resolve license or retention rights.

Reproducibility considerations:

Requires official table inventory, release/version semantics, date-field review, and license-approved source manifest strategy.

Known limitations:

Ticker lineage and listing/delisting coverage are not sufficiently established from public docs. It should not be used as the first primary source for security master PIT construction.

Documentation sufficiency:

`READY_PENDING_LICENSE` for secondary issuer/company metadata design; not sufficient for primary ticker-lineage design.

### `exchange_vendor_listing_delisting_datasets`

Intended purpose:

Supplement listing status, exchange membership, symbol distribution, listing/delisting events, and exchange-specific ticker changes.

Publicly documented coverage:

Public exchange sites expose some listing, market-status, symbol-distribution, data-product, and data-policy pages. NYSE public pages reference symbol distribution and market-status history. Public documentation reviewed in this pass did not establish a single comprehensive, historical, auditable, multi-exchange security master.

PIT suitability:

Conditional as a supplement if dated historical records, stable identifiers, and reproducible archives are licensed and retained. Insufficient as a primary source from public documentation alone.

Identifier support:

Variable. Exchange records may support tickers, exchange symbols, MICs, and listing venues, but often require additional security identifiers and corporate-action context.

Lineage support:

Potentially useful for exchange-specific listing/delisting events, but public evidence does not prove full security continuity, share-class continuity, ticker reuse protection, or corporate-action lineage.

Licensing model:

Exchange/vendor specific. Public pages do not resolve data redistribution, retention, archive, or historical dataset rights.

Reproducibility considerations:

Future evaluation must require vendor/exchange dataset versioning, historical depth, file manifests, update cadence, and retention permissions.

Known limitations:

Fragmentation across exchanges, inconsistent identifiers, and possible lack of issuer/security continuity make this unsuitable as first primary source.

Documentation sufficiency:

`DOCUMENTATION_INSUFFICIENT` for ingestion design as a primary source. Potential future supplemental evaluation only.

### `openfigi_identifier_documentation`

Intended purpose:

Identifier crosswalk diagnostics and instrument identifier enrichment.

Publicly documented coverage:

OpenFIGI documentation describes FIGI as an open standard, a permanent identifier, and an API for mapping to market identifiers, data, and standards. The API documentation states that static output returns FIGI and related Open Symbology metadata and can be narrowed by descriptive filters.

PIT suitability:

Low for primary PIT lineage. FIGI permanence helps identity crosswalks, but the public API documentation reviewed here describes mapping/static output rather than complete historical ticker windows, delisting events, and known-date semantics.

Identifier support:

Strong for FIGI, composite FIGI, and Open Symbology-style mappings.

Lineage support:

Moderate for identifier relationships, insufficient for primary ticker lineage. It can help detect mapping conflicts or enrich diagnostics.

Licensing model:

Open-data oriented. Public OpenFIGI overview states that FIGI is an open data standard and emphasizes free use, reuse, and redistribution. API operational terms and attribution/usage details still need review before any automated workflow.

Reproducibility considerations:

For diagnostics, future design would need query manifesting, request parameters, response timestamps, API version references, and rate-limit/availability handling. No API calls were made in this review.

Known limitations:

Not a delisting database, not a CRSP-equivalent security master, and not proven to provide complete historical PIT ticker lineage.

Documentation sufficiency:

`DIAGNOSTIC_ONLY`. Sufficient for future crosswalk diagnostic design, not primary ingestion design.

### `yfinance_metadata`

Intended purpose:

Diagnostic-only current-profile comparison and lightweight sanity checks.

Publicly documented coverage:

yfinance project documentation describes the package as a Pythonic way to fetch market and financial data from Yahoo Finance. It identifies current package capabilities such as ticker data, downloads, search, sector/industry information, screeners, and market data access.

PIT suitability:

Low. The documentation reviewed does not establish PIT ticker lineage, delisting history, stable security identifiers, effective-date windows, or source versioning suitable for historical alpha metadata.

Identifier support:

Weak for security-master purposes. The interface is ticker-centric and does not provide a licensed institutional identity spine.

Lineage support:

Weak. It can provide current metadata diagnostics but should not be used for historical security identity or ticker lineage.

Licensing model:

yfinance itself is open-source software, but its documentation explicitly points users to Yahoo terms for rights to downloaded data and states the Yahoo Finance API is intended for personal use only.

Reproducibility considerations:

Changing API behavior, no controlled source versioning, and unclear data-rights posture make reproducibility unsuitable for research lineage construction.

Known limitations:

Current-profile bias, ticker-only ambiguity, external API instability, and data-use restrictions.

Documentation sufficiency:

`DIAGNOSTIC_ONLY`. Not sufficient for ingestion design.

## SECTION 5 - Licensing and Reproducibility Assessment

License blockers:

- CRSP, WRDS CCM, and Compustat remain blocked by institutional license and entitlement evidence.
- Public CRSP/Compustat descriptions prove product plausibility but do not prove local rights to access, retain, hash, archive, redistribute, or derive audit artifacts.
- Exchange/vendor sources require vendor-specific terms before any ingestion design can assume retention or reproducibility.
- OpenFIGI has favorable public open-data documentation, but any automated workflow still needs API terms and reproducibility controls.
- yfinance is blocked from lineage use by Yahoo data-use constraints and the package's own warnings to consult Yahoo terms.

Reproducibility blockers:

- No source file, source table, source snapshot, release id, source hash, row count, or archive policy was reviewed.
- No official data dictionary was reviewed for CRSP, WRDS CCM, or Compustat.
- No account-specific entitlement or delivery-format evidence was reviewed.
- No source can advance to source loading or ingestion from this review.

## SECTION 6 - Readiness Classification

Classification counts:

- `READY_FOR_INGESTION_DESIGN`: 0
- `READY_PENDING_LICENSE`: 3
- `DOCUMENTATION_INSUFFICIENT`: 1
- `DIAGNOSTIC_ONLY`: 2

Overall classification: `SOURCE_EVIDENCE_READY_WITH_LICENSE_BLOCKERS`.

Rationale:

The public evidence is strong enough to identify the first target and design the shape of a future license-gated ingestion plan, but it is not enough to authorize source access, loading, ingestion, PIT table construction, or implementation changes. License, retention, entitlement, source-version, known-date, and official field evidence are blocking for every professional source.

## SECTION 7 - Recommended First Ingestion-Design Target

Recommended first target:

`crsp_stocknames_delisting_security_master`.

Reason:

It has the best public evidence for the exact problem: permanent security identity, active/inactive coverage, U.S. exchange coverage, corporate actions, and historical research/backtesting use. It should be designed first, with WRDS CRSP-Compustat Link as the first secondary bridge only after the primary CRSP identity/ticker scope is license-cleared.

Required preconditions before ingestion design moves beyond assumption-bound planning:

- Institutional CRSP entitlement summary.
- License/legal review covering research use, retention, derived metadata, audit artifacts, documentation references, redistribution restrictions, and production restrictions.
- Archive/hash or controlled-reference policy.
- Official CRSP data dictionary or authorized schema evidence for stock names, security master fields, ticker windows, delisting fields, exchange/listing fields, share-class fields, and source metadata.
- Release/version or source snapshot semantics.
- Known-date or conservative source release-date fallback semantics.
- Evidence-backed source-gate manifest update.

## SECTION 8 - Artifacts Produced

Artifacts created under:

`artifacts/research/crsp_security_master_ticker_lineage_pit_v1/source_evidence_review/`

Files:

- `source_documentation_inventory.csv`
- `source_field_inventory.csv`
- `source_license_summary.csv`
- `source_readiness_summary.csv`
- `source_evidence_manifest.json`

These are manifest-only documentation artifacts. They do not contain source data.

## SECTION 9 - Explicit Guardrail Confirmation

Confirmed:

- Only documentation/evidence artifacts were produced.
- No source data was accessed.
- No downloads were performed.
- No API calls were made.
- No external database connections were made.
- No PIT tables were created.
- No alpha implementation, panel generation, IC computation, validation, governance mutation, production change, or ML work was performed.
- No implementation files were changed.

## SECTION 10 - Final Recommendation

Proceed with a future **CRSP Stock Names / Security Master / Delisting ingestion-design package** only after license and entitlement evidence is available. The design should remain fail-closed, should not inspect or load source data, and should treat WRDS CCM, Compustat, exchange/vendor feeds, OpenFIGI, and yfinance as secondary or diagnostic sources according to the classifications in this review.
