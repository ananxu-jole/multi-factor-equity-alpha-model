# Project Underdog - PIT Security Master and Ticker Lineage Source Candidate Evaluation v1

## SECTION 1 - Executive Summary

This note evaluates plausible source candidates for future point-in-time security master and ticker lineage work using manifest rows only.

Classification: `SOURCE_CANDIDATES_READY_WITH_LICENSE_DEPENDENCIES`.

No ingestion, external source access, downloads, WRDS/CRSP/Compustat/OpenFIGI/yfinance connections, PIT table creation, peer-group creation, alpha pipeline modification, panel generation, IC computation, validation, governance threshold change, production registry mutation, or ML work was performed.

The strongest conceptual source path is CRSP security master / stock names / delisting data, potentially complemented by WRDS CRSP/Compustat linking and Compustat company/security metadata. However, all professional-source candidates remain conditional because subscribed table availability, licensing, source retention, field mapping, and reproducibility evidence have not been reviewed.

## SECTION 2 - Materials Reviewed

Reviewed:

- `docs/research_notes/security_master_and_ticker_lineage_pit_source_gate_scaffold_v1.md`
- `docs/research_notes/point_in_time_economic_metadata_source_and_lineage_design_v1.md`
- `pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py`

Context:

- PIT source-gate scaffold classification: `SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES`.
- PIT economic metadata source and lineage design classification: `DESIGN_READY_WITH_EXTERNAL_DATA_DEPENDENCIES`.

## SECTION 3 - Source Candidate List

Evaluated manifest-only candidates:

| source_id | source | intended role | decision group |
| --- | --- | --- | --- |
| `crsp_stocknames_delisting_security_master` | CRSP stock names / security master / delisting files | Primary security identity, ticker lineage, listing/delisting, recycled ticker handling. | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` |
| `wrds_crsp_compustat_link` | WRDS CRSP/Compustat linking | Issuer/company linkage and CRSP-Compustat bridge. | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` |
| `compustat_security_company_metadata` | Compustat company/security metadata | Company attributes and possible economic classification support. | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` |
| `exchange_listing_delisting_history` | Exchange or vendor listing/delisting history | Secondary listing/delisting support. | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` |
| `existing_project_static_metadata` | Current project static metadata seed/overrides | Diagnostic baseline only. | `DIAGNOSTIC_ONLY` |
| `openfigi_identifier_mapping` | OpenFIGI or comparable identifier mapping | Identifier crosswalk diagnostics only. | `DIAGNOSTIC_ONLY` |
| `yfinance_static_metadata` | Static yfinance profile metadata | Current-profile diagnostic baseline only. | `DIAGNOSTIC_ONLY` |

No candidate is currently classified `APPROVED_FOR_FUTURE_INGESTION_DESIGN` because no source has been license-reviewed, source-file-reviewed, field-mapped, or accepted through an evidence-backed source gate.

## SECTION 4 - Gate Scoring Summary

| rank | source_id | score / max | decision group | primary blockers |
| ---: | --- | ---: | --- | --- |
| 1 | `crsp_stocknames_delisting_security_master` | 12 / 15 | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` | licensing, subscribed tables, field mapping, known-date semantics |
| 2 | `wrds_crsp_compustat_link` | 10 / 15 | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` | licensing, incomplete standalone ticker lineage |
| 3 | `compustat_security_company_metadata` | 9 / 15 | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` | licensing, ticker lineage, delisting/event coverage |
| 4 | `exchange_listing_delisting_history` | 9 / 15 | `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW` | licensing, stable identifiers, corporate-action continuity |
| 5 | `existing_project_static_metadata` | 5 / 15 | `DIAGNOSTIC_ONLY` | static snapshot, ticker-only lineage, current labels |
| 6 | `openfigi_identifier_mapping` | 5 / 15 | `DIAGNOSTIC_ONLY` | current/static mapping, incomplete PIT lineage, coverage |
| 7 | `yfinance_static_metadata` | 1 / 15 | `DIAGNOSTIC_ONLY` | static current profile, ticker-only identity, unknown licensing |

Decision counts:

- `APPROVED_FOR_FUTURE_INGESTION_DESIGN`: 0
- `CONDITIONALLY_ACCEPTABLE_WITH_LICENSE_OR_COVERAGE_REVIEW`: 4
- `DIAGNOSTIC_ONLY`: 3
- `REJECTED_FOR_ALPHA_USE`: 0

Interpretation:

The candidate set is ready for a source-evidence and licensing review. It is not ready for ingestion design until at least one professional PIT source is evidence-backed.

## SECTION 5 - Source-by-Source Interpretation

### `crsp_stocknames_delisting_security_master`

This is the best conceptual candidate for security master and ticker lineage. It is expected to be strongest on PIT identity, ticker history, delistings, and recycled ticker handling if the appropriate subscribed CRSP tables are available.

Current status:

- Strongest future source candidate.
- Not approved yet because no subscribed table inventory, license/retention review, field mapping, or known-date semantics review has been performed.

Expected failure modes:

- missing subscription scope;
- licensing/retention restrictions;
- insufficient event known-date semantics;
- incomplete corporate-action or share-class mapping for the research universe.

### `wrds_crsp_compustat_link`

This is useful as an issuer/company bridge and may help connect CRSP security identity to Compustat company metadata. It should not be treated as a standalone ticker lineage source.

Current status:

- Conditional complement, not primary source.

Expected failure modes:

- licensing uncertainty;
- link-history ambiguity;
- date-window interpretation issues;
- incomplete coverage for non-linked securities.

### `compustat_security_company_metadata`

This may support issuer identity, company attributes, and future classification work. It is not enough by itself for ticker lineage, delisting history, or recycled ticker protection.

Current status:

- Conditional secondary source.

Expected failure modes:

- weak ticker lineage;
- missing delisting/listing event coverage;
- classification effective-date ambiguity;
- dependency on CRSP or another source for security identity.

### `exchange_listing_delisting_history`

Exchange or vendor listing/delisting history could complement CRSP, especially for listing windows and delisting checks. It is unlikely to replace a security master without stable identifiers and corporate-action lineage.

Current status:

- Conditional complementary source.

Expected failure modes:

- inconsistent security identifiers;
- weak issuer linkage;
- incomplete corporate-action history;
- licensing and reproducibility limits.

### `existing_project_static_metadata`

The current project metadata seed and overrides have good diagnostic coverage, but they are explicitly static snapshot metadata. They must remain blocked from historical alpha, peer-relative transforms, and PIT lineage.

Current status:

- Diagnostic-only baseline.

Expected failure modes:

- look-ahead through current classifications;
- no ticker lineage;
- no historical sector/industry/size history.

### `openfigi_identifier_mapping`

OpenFIGI or similar identifier mapping may help with crosswalk diagnostics or manual review, but it is not a PIT ticker lineage source in this evaluation.

Current status:

- Diagnostic-only support source.

Expected failure modes:

- current/query-date mapping rather than historical lineage;
- incomplete listing/delisting history;
- no corporate-action continuity;
- coverage and licensing ambiguity.

### `yfinance_static_metadata`

yfinance-style static profile metadata is useful only as a current-profile diagnostic baseline. It is not acceptable for PIT identity, ticker lineage, or alpha use.

Current status:

- Diagnostic-only baseline.

Expected failure modes:

- static current metadata;
- ticker-only identity;
- unclear licensing/reproducibility;
- no delisting, listing, event, or corporate-action lineage.

## SECTION 6 - External Dependency Checklist

Before any ingestion design:

- Confirm subscription/source availability.
- Confirm license allows research use, retention, hashing, derived artifacts, and reproducible audit records.
- Confirm source version and snapshot/release metadata.
- Confirm source can be archived or referenced in a controlled reproducible way.
- Confirm stable security identifiers.
- Confirm ticker history with effective windows.
- Confirm listing and delisting coverage.
- Confirm recycled ticker handling.
- Confirm corporate-action event lineage.
- Confirm issuer/company linkage.
- Confirm known-date or conservative as-of-date semantics.
- Confirm field mapping to source-gate manifest and future PIT schemas.
- Confirm active coverage across the research lookback.

## SECTION 7 - Licensing and Reproducibility Risks

Most serious risks:

- Professional PIT sources may be available only under license terms that restrict retention, redistribution, or artifact sharing.
- Source hashes may not be permitted if raw source files cannot be retained.
- WRDS/CRSP/Compustat source access may differ by subscription.
- Source documentation may not provide known-date semantics sufficient for conservative PIT use.
- Crosswalks may be reproducible but insufficient as primary identity lineage.
- Current/static APIs may be easy to access but unsafe for historical use.

Control:

No source should move from this review to ingestion design until licensing and reproducibility are documented in a source evidence register.

## SECTION 8 - Artifacts Produced

Artifacts created under:

`artifacts/research/crsp_security_master_ticker_lineage_pit_v1/source_candidate_evaluation/`

Files:

- `source_candidate_manifest.csv`
- `source_candidate_gate_scores.csv`
- `source_candidate_decision_summary.csv`
- `source_candidate_evaluation_manifest.json`

These artifacts are manifest/scoring artifacts only. They do not contain source data.

## SECTION 9 - Recommended Future Ingestion-Design Path

Do not start ingestion design immediately.

Recommended next task:

**Project Underdog - PIT Security Master and Ticker Lineage Source Evidence and License Review v1**.

That task should:

- collect evidence for the conditional candidates;
- verify licensing and retention rights;
- map available fields to the source-gate manifest;
- document known-date semantics;
- document reproducibility and source hashes or controlled references;
- decide whether CRSP, WRDS-linked CRSP/Compustat, Compustat, or exchange/vendor listing history can move into an ingestion design.

It should still not ingest data or build PIT tables.

## SECTION 10 - Explicit Non-Goals

This evaluation did not:

- ingest data;
- access external sources;
- download files;
- connect to WRDS;
- connect to CRSP;
- connect to Compustat;
- connect to OpenFIGI;
- connect to yfinance;
- create PIT tables;
- create peer groups;
- modify alpha pipelines;
- generate panels;
- compute IC;
- run validation;
- modify governance thresholds;
- modify production registry;
- introduce ML.

## SECTION 11 - Verification

Verification commands:

- `python pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py --dry-run-source-gates`
- `python pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py --validate-source-gates`
- `python -m pytest tests/test_crsp_security_master_ticker_lineage_pit_scaffold.py -q`

Verification status:

- Source-gate dry-run evaluator passed.
- Source-gate scaffold validation passed.
- Focused scaffold tests passed.

Manifest guardrails confirm:

- no external data access;
- no downloads;
- no source files loaded;
- no metadata ingestion;
- no PIT tables;
- no peer groups;
- no alpha pipeline modification;
- no panel generation;
- no IC computation;
- no validation;
- no governance threshold change;
- no production registry modification;
- no ML.

## SECTION 12 - Readiness Classification

Final classification: `SOURCE_CANDIDATES_READY_WITH_LICENSE_DEPENDENCIES`.

Rationale:

- Plausible source candidates have been organized and scored through the source-gate rubric.
- CRSP-style security master and delisting data appear to be the strongest primary path.
- WRDS CRSP/Compustat linking and Compustat metadata are useful complements.
- Static/current profile sources remain diagnostic-only.
- No source is approved for ingestion design until licensing, source availability, field mapping, and reproducibility evidence are reviewed.
