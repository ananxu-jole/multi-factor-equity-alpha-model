# Project Underdog - Security Master and Ticker Lineage Source Candidate Identification v1

## SECTION 1 - Executive Summary

Objective: identify real-world candidate sources that could plausibly support `security_master_pit` and `ticker_lineage_pit`, then compare them using the approved source candidate evaluation framework.

Evaluation scope:

- security identity
- security continuity
- exchange continuity
- name continuity
- ticker changes
- ticker reuse detection
- delistings
- mergers, spin-offs, and other corporate-action continuity

Candidate sources identified: 6.

Major findings:

- `CRSP US Stock Databases` is the strongest first candidate for formal evaluation because it explicitly covers active and inactive U.S. securities, provides survivor-bias-free history, corporate actions, delisting information, exchange coverage, and permanent identifiers `PERMNO` and `PERMCO`.
- `LSEG Entity and Reference Data` is a strong enterprise backup because it advertises broad reference data, symbol cross-reference, corporate actions, and major identifier systems, but formal evaluation would need to confirm historical snapshot/effective-date availability for the exact product/package.
- `CUSIP Global Services` is strong as an identifier and reference-data supplement, including issuer/instrument identifiers and corporate-action attributes, but it is not enough by itself for full ticker lineage unless paired with historical ticker windows.
- `Norgate Data US Stocks` is useful as a secondary/diagnostic candidate because it offers survivorship-bias-free historical stock data and delisted securities, but it has platform, licensing, and security-master-depth questions.
- `OpenFIGI` is useful for open identifier mapping and governance checks, but it is not a PIT ticker-lineage source.
- `S&P Global / Compustat-style company/security data` remains a potential secondary institutional candidate, especially for company identifiers and corporate data, but should not outrank a true security/ticker lineage source without formal evidence of ticker-window and PIT identity support.

This note does not accept, reject, load, ingest, or integrate any source. It recommends only an evaluation order.

## SECTION 2 - Candidate Inventory

| source name | source category | public/commercial status | expected PIT support | expected ticker-lineage support |
| --- | --- | --- | --- | --- |
| `CRSP US Stock Databases` | Professional/institutional historical security database | Commercial/research subscription | High expected PIT suitability for U.S. listed equities because it provides survivor-bias-free history, active/inactive securities, exchange coverage, release cadence, flat files, and permanent identifiers. | High expected ticker/security lineage support through `PERMNO`, `PERMCO`, corporate actions, delisting information, and identifying information. |
| `LSEG Entity and Reference Data` | Enterprise entity/reference-data provider | Commercial enterprise source | Medium-high expected PIT suitability, pending confirmation of historical snapshots/effective windows for the subscribed content. | Medium-high expected support through symbol cross-reference, instrument reference data, corporate actions, and identifiers such as ISIN, CUSIP, SEDOL, RIC, and PermID. |
| `CUSIP Global Services` | Identifier/reference-data provider | Commercial identifier and data services | Medium expected PIT support for identifiers/reference attributes; formal evaluation must confirm historical event/effective-date availability. | Medium expected support as an identifier/corporate-action supplement; weak as standalone ticker-lineage source. |
| `Norgate Data US Stocks` | Historical stock database with delisted securities | Commercial subscription | Medium expected PIT support for price/history and survivorship-bias mitigation; lower security-master confidence until identity/ticker fields are inspected. | Medium expected ticker/history usefulness; formal evaluation must verify ticker-change, reuse, exchange, and corporate-action detail. |
| `OpenFIGI` | Open identifier mapping and symbology service | Free/open API and dataset under open license | Low PIT support; useful for identifier mapping and diagnostics, not historical lineage. | Low as standalone ticker lineage; useful for mapping to FIGI identifiers and cross-checking instrument identity. |
| `S&P Global / Compustat-style company and security datasets` | Institutional company/security/fundamental data | Commercial/institutional | Medium expected PIT support if point-in-time products and identifier history are available. | Medium-low as standalone ticker lineage; potentially useful when paired with CRSP or another ticker-history source. |

Sources reviewed publicly:

- CRSP Research Data Products and CRSP US Stock Databases.
- LSEG Entity and Reference Data.
- CUSIP Global Services.
- Norgate Data Overview and US stock packages.
- OpenFIGI.
- Public Compustat/S&P Global descriptive material.

## SECTION 3 - Candidate Capability Assessment

| source | effective-date support | identifier continuity | ticker-history support | corporate-action support | historical depth | auditability | reproducibility | coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CRSP US Stock Databases` | Strong expected support through historical databases, release files, delisting data, and corporate-action history; formal field review still required. | Strong: `PERMNO` and `PERMCO` are designed for stable tracking over time. | Strong expected support through historical identifying information and issue/company identifiers. | Strong: corporate actions and delisting information are explicit product features. | Strong for U.S. equities: NYSE history begins in 1925, NYSE American in 1962, NASDAQ in 1972, NYSE Arca in 2006, Cboe BZX in 2012. | Strong: subscription, release notes, user guides, metadata guide, file formats. | Strong expected support through release files and flat-file formats; license review required. | Strong for listed U.S. equities, including active and inactive securities. |
| `LSEG Entity and Reference Data` | Medium-high expected; must confirm historical availability, point-in-time snapshots, and event dates. | Strong expected through ISIN, CUSIP, SEDOL, RIC, PermID, and entity/instrument reference data. | Medium-high expected through symbol cross-reference, subject to historical field review. | Strong expected through corporate actions content. | Broad enterprise coverage; formal evaluation must confirm U.S. equity historical depth. | Strong enterprise audit potential; source version/historical package details require review. | Medium-high if bulk/reference delivery retains snapshots and hashes. | Very broad advertised instrument coverage; active ticker-date coverage must be measured. |
| `CUSIP Global Services` | Medium; identifier issuance and corporate-action attributes exist, but ticker-window PIT use must be proven. | Strong for CUSIP/CINS/ISIN and issuer/instrument identifiers. | Low-medium; not primarily a ticker-history source. | Medium-high: name changes, mergers, acquisitions, reverse splits are listed as event-driven corporate actions. | Broad identifier coverage; historical depth for desired equity ticker windows unknown. | Strong identifier governance; data licensing must be reviewed. | Medium-high if API/data service snapshots can be retained. | Broad identifier coverage, but not necessarily active trading universe coverage. |
| `Norgate Data US Stocks` | Medium; historical packages include current and delisted securities, but event/effective-date fields need inspection. | Medium-low until stable identifier fields are verified. | Medium; likely useful for symbol histories, but not proven as full lineage. | Medium-low; corporate-action details need inspection. | Strong for U.S. history in Diamond package back to 1950 and delisted securities back to 1950. | Medium; proprietary local database and subscription terms need review. | Medium-low if access lapses or non-price features cannot be exported. | Good for U.S. stocks in selected package tiers; universe definitions need review. |
| `OpenFIGI` | Low; mapping service, not historical PIT lineage. | Medium-high for FIGI identity once mapped; not sufficient for historical continuity. | Low; can map instruments but does not provide dated ticker windows. | Low; not a corporate-action source. | Broad identifier universe, but not historical active/inactive panels. | Strong open API/metadata transparency. | Strong for API-based mapping if requests/responses are retained. | Broad mapping coverage; not coverage of historical tradeable universe. |
| `S&P Global / Compustat-style datasets` | Medium if point-in-time products are available; must confirm exact product. | Medium-high for company identifiers and standard market identifiers. | Medium-low unless paired with a security/ticker history product. | Medium through corporate actions and company event data. | Strong company history potential; equity ticker lineage depth must be confirmed. | Strong institutional audit potential, product-specific. | Medium-high if delivered as licensed reproducible files. | Broad company/security coverage, but ticker-date coverage must be tested. |

## SECTION 4 - Framework Scoring Preview

This is a preliminary qualitative preview only. It is not a formal source-gate evaluation.

| source | likely strengths | likely weaknesses | likely manual-review triggers | expected candidate class |
| --- | --- | --- | --- | --- |
| `CRSP US Stock Databases` | PIT history, survivor-bias-free active/inactive securities, permanent identifiers, corporate actions, delisting data, exchange coverage, flat-file delivery. | U.S.-equity focus; license/subscription review; need exact field mapping to `security_master_pit` and `ticker_lineage_pit`. | Licensing, permitted retention, exact ticker-window fields, source-file hash retention. | `STRONG_CANDIDATE` |
| `LSEG Entity and Reference Data` | Broad enterprise reference data, identifiers, symbol cross-reference, corporate actions, entity/instrument coverage. | Exact PIT history and historical snapshot model must be confirmed. | Product/package scope, historical depth, licensing, reproducible bulk delivery. | `CONDITIONAL_CANDIDATE` to `STRONG_CANDIDATE` |
| `CUSIP Global Services` | Identifier authority, security-master backbone role, corporate-action attributes. | Not complete ticker lineage by itself; ticker/exchange windows likely insufficient alone. | Need pairing plan, historical event dating, retention terms. | `CONDITIONAL_CANDIDATE` |
| `Norgate Data US Stocks` | Survivorship-bias-free package, delisted securities, long U.S. history, practical accessibility. | Less clearly an institutional security master; export/access limitations; stable identifier and event-lineage questions. | License, reproducibility, non-price exportability, ticker reuse handling. | `CONDITIONAL_CANDIDATE` |
| `OpenFIGI` | Open identifier mapping, free API, useful FIGI cross-reference. | Not PIT, not active/inactive universe, not corporate-action/ticker-lineage source. | Whether mapping output can support diagnostics only; not construction. | `MANUAL_REVIEW_REQUIRED` or diagnostic-only |
| `S&P Global / Compustat-style datasets` | Institutional company data, identifiers, corporate actions, potential point-in-time products. | Not primarily ticker lineage; exact PIT security/ticker window support must be shown. | Product selection, identifier mapping, ticker history, licensing. | `CONDITIONAL_CANDIDATE` |

## SECTION 5 - Security Master Suitability Ranking

Security identity ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `CUSIP Global Services`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Security continuity ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `CUSIP Global Services`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Exchange continuity ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `Norgate Data US Stocks`
4. `CUSIP Global Services`
5. `OpenFIGI`
6. `S&P Global / Compustat-style datasets`

Name continuity ranking:

1. `CUSIP Global Services`
2. `CRSP US Stock Databases`
3. `LSEG Entity and Reference Data`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Interpretation:

`CRSP US Stock Databases` ranks first overall for Project Underdog's immediate U.S. equity security master foundation because its permanent identifiers and active/inactive history align directly with historical equity research needs.

## SECTION 6 - Ticker Lineage Suitability Ranking

Ticker changes ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `Norgate Data US Stocks`
4. `S&P Global / Compustat-style datasets`
5. `OpenFIGI`
6. `CUSIP Global Services`

Ticker reuse detection ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `Norgate Data US Stocks`
4. `OpenFIGI`
5. `CUSIP Global Services`
6. `S&P Global / Compustat-style datasets`

Mergers ranking:

1. `CRSP US Stock Databases`
2. `CUSIP Global Services`
3. `LSEG Entity and Reference Data`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Spin-offs ranking:

1. `CRSP US Stock Databases`
2. `CUSIP Global Services`
3. `LSEG Entity and Reference Data`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Delistings ranking:

1. `CRSP US Stock Databases`
2. `Norgate Data US Stocks`
3. `LSEG Entity and Reference Data`
4. `S&P Global / Compustat-style datasets`
5. `CUSIP Global Services`
6. `OpenFIGI`

Corporate actions ranking:

1. `CRSP US Stock Databases`
2. `LSEG Entity and Reference Data`
3. `CUSIP Global Services`
4. `S&P Global / Compustat-style datasets`
5. `Norgate Data US Stocks`
6. `OpenFIGI`

Interpretation:

`CRSP US Stock Databases` again ranks first because ticker lineage and corporate actions are tied to permanent security identifiers and active/inactive history, which reduces ticker-only ambiguity.

## SECTION 7 - Risk Review

| source | historical-integrity risk | survivorship-bias risk | identifier ambiguity risk | licensing risk | reproducibility risk | maintenance burden |
| --- | --- | --- | --- | --- | --- | --- |
| `CRSP US Stock Databases` | Low-medium | Low | Low | Medium-high | Low-medium | Medium |
| `LSEG Entity and Reference Data` | Medium until PIT package confirmed | Low-medium | Low-medium | High | Medium | Medium-high |
| `CUSIP Global Services` | Medium for PIT ticker lineage | Medium | Low for identifiers, higher for ticker windows | Medium-high | Medium | Medium |
| `Norgate Data US Stocks` | Medium | Low-medium | Medium-high | Medium | Medium-high | Low-medium |
| `OpenFIGI` | High for PIT use | Medium | Medium | Low | Low | Low |
| `S&P Global / Compustat-style datasets` | Medium until product confirmed | Low-medium | Medium | High | Medium | Medium-high |

Largest risks:

- `CRSP US Stock Databases`: access/licensing and exact retention rights.
- `LSEG Entity and Reference Data`: confirming historical PIT/snapshot structure for the exact licensed product.
- `CUSIP Global Services`: insufficient ticker-window lineage as a standalone source.
- `Norgate Data US Stocks`: reproducibility/export limitations and weaker security-master semantics.
- `OpenFIGI`: not a historical source.
- `S&P Global / Compustat-style datasets`: may be excellent company data but not the first ticker-lineage source.

## SECTION 8 - Recommended First Candidate

Recommended `FIRST_REAL_SOURCE_CANDIDATE`:

`CRSP US Stock Databases`

Rationale:

- Best alignment with Project Underdog's U.S. equity research context.
- Explicit active and inactive U.S. security coverage.
- Survivor-bias-free historical orientation.
- Permanent identifiers `PERMNO` and `PERMCO` are directly relevant to stable security identity.
- Corporate actions and security delisting information are explicit product features.
- Exchange coverage and history depth are publicly documented.
- Flat-file delivery and release documentation suggest strong audit/reproducibility potential.

Important:

This is not source acceptance. It is only a recommendation for the first source to undergo formal PIT source-gate evaluation. No CRSP data was loaded, ingested, inspected, accepted, or integrated.

## SECTION 9 - Alternative Candidates

Backup candidate 1: `LSEG Entity and Reference Data`.

- Use if the project needs a broader enterprise reference-data source or if CRSP access is unavailable.
- Formal evaluation must verify historical snapshot/effective-date support and retention rights.

Backup candidate 2: `CUSIP Global Services`.

- Use as an identifier/reference-data supplement or cross-check.
- Not recommended as the first standalone ticker-lineage source.

Backup candidate 3: `Norgate Data US Stocks`.

- Use as a practical secondary source or diagnostic comparison for active/delisted U.S. stock coverage.
- Formal evaluation must inspect export rights, ticker-change detail, stable identifiers, and reproducibility.

Backup candidate 4: `S&P Global / Compustat-style datasets`.

- Use as a company/security identifier and corporate data supplement.
- Not recommended as the first standalone ticker-lineage source without a specific PIT security/ticker product.

Diagnostic candidate: `OpenFIGI`.

- Use for identifier mapping diagnostics and cross-reference checks.
- Do not use as PIT source or ticker-lineage source.

## SECTION 10 - Final Recommendation

1. Which source should be evaluated first?

`CRSP US Stock Databases` should be evaluated first.

2. Why is it superior to alternatives?

It is the best fit for the identity/ticker-lineage foundation because it combines active/inactive U.S. security coverage, survivor-bias-free history, exchange history, corporate actions, delisting information, permanent identifiers, release documentation, and flat-file delivery. Alternatives are promising but either require more product-scope confirmation, are stronger as supplements, or lack PIT ticker-lineage depth.

3. What are its main risks?

Main risks are access/licensing, research retention permissions, exact field mapping to `security_master_pit` and `ticker_lineage_pit`, and confirming that source artifacts can be retained with hashes, release versions, and audit manifests.

4. Which backup candidates should be retained?

Retain `LSEG Entity and Reference Data` as the strongest enterprise backup, `CUSIP Global Services` as an identifier/corporate-action supplement, `Norgate Data US Stocks` as a practical secondary/diagnostic comparison, `S&P Global / Compustat-style datasets` as a company/security data supplement, and `OpenFIGI` as an open identifier-mapping diagnostic.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - CRSP US Stock Databases PIT Source-Gate Evaluation Design v1**. It should prepare a formal source-gate evaluation design and candidate manifest plan for CRSP only. It should not ingest data, load source files, accept or reject the source, construct metadata, build security lineage, build ticker lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.

## Source References

- CRSP Research Data Products and CRSP US Stock Databases: `https://www.crsp.org/research/`, `https://www.crsp.org/research/crsp-us-stock-databases/`
- LSEG Entity and Reference Data: `https://www.lseg.com/en/data-analytics/financial-data/reference-data`
- CUSIP Global Services: `https://www.cusip.com/`
- Norgate Data Overview and Stock Market Packages: `https://norgatedata.com/`, `https://norgatedata.com/stockmarketpackages.php`
- OpenFIGI: `https://www.openfigi.com/`
- Public S&P/Compustat descriptive source reviewed via web search; formal source evaluation must rely on official product documentation before any decision.
