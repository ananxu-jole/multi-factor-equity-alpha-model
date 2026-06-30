# Metadata Source Lineage Consistency Review v1

Date: 2026-05-25

Status: `STATIC_SNAPSHOT_LINEAGE_REVIEW_COMPLETE`

Metadata status reviewed: `METADATA_DIAGNOSTIC_READY_STATIC_SNAPSHOT`

## Objective

Review the 360-row static-snapshot metadata seed for source-lineage and classification consistency before broader diagnostic use.

This review is audit-only. It does not modify the seed, does not claim point-in-time validity, and does not approve alpha, validation, production, portfolio, ML, blending, or optimization use.

Reviewed seed:

`data/metadata/ticker_classification_seed_v1.csv`

## Current Metadata State

| item | value |
| --- | ---: |
| seed rows | 360 |
| distinct seed tickers | 360 |
| universe tickers | 489 |
| matched universe tickers | 360 |
| missing universe tickers | 129 |
| extra seed tickers | 0 |
| coverage ratio | 0.736196 |
| duplicate tickers | 0 |
| key-field missingness | 0 |
| static warning violations | 0 |
| inventory metadata coverage | 0.734310 |

All rows retain:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

## Source Distribution

| source | ticker_count |
| --- | ---: |
| `manual_static_coverage_expansion_v3_review` | 110 |
| `manual_static_coverage_expansion_review` | 109 |
| `manual_static_coverage_expansion_v2_review` | 100 |
| `manual_static_pilot_review` | 41 |

Source references:

| source_url_or_reference | ticker_count |
| --- | ---: |
| `manual_metadata_coverage_expansion_v3_internal_review_no_external_fetch` | 110 |
| `manual_metadata_coverage_expansion_v1_internal_review_no_external_fetch` | 109 |
| `manual_metadata_coverage_expansion_v2_internal_review_no_external_fetch` | 100 |
| `manual_metadata_pilot_population_v1_internal_review_no_external_fetch` | 41 |

Source/date matrix:

| source | as_of_date | effective_date | collection_timestamp | rows |
| --- | --- | --- | --- | ---: |
| `manual_static_pilot_review` | 2026-05-24 | 2026-05-24 | 2026-05-24T23:00:00Z | 41 |
| `manual_static_coverage_expansion_review` | 2026-05-24 | 2026-05-24 | 2026-05-24T23:30:00Z | 109 |
| `manual_static_coverage_expansion_v2_review` | 2026-05-24 | 2026-05-24 | 2026-05-24T23:50:00Z | 100 |
| `manual_static_coverage_expansion_v3_review` | 2026-05-25 | 2026-05-25 | 2026-05-25T14:00:00Z | 110 |

Assessment:

- Source batches are internally coherent.
- Each row has non-empty `source` and `source_url_or_reference`.
- Collection timestamps are batch-consistent.
- Universe version and metadata version are consistent across all rows.
- No external data fetch was performed by the audit runners.

Caveat:

The source lineage is internally auditable, but not externally source-auditable yet. `source_url_or_reference` contains internal review labels, not a row-level external source citation, source document, or source snapshot hash.

## Required Field Completeness

Required-field missingness:

| field | missing_rows |
| --- | ---: |
| ticker | 0 |
| company_name | 0 |
| sector | 0 |
| industry | 0 |
| peer_group_label | 0 |
| market_cap_bucket | 0 |
| size_bucket | 0 |
| source | 0 |
| source_url_or_reference | 0 |
| as_of_date | 0 |
| effective_date | 0 |
| collection_timestamp | 0 |
| universe_version | 0 |
| metadata_version | 0 |
| snapshot_warning | 0 |

Assessment:

The seed is complete enough for descriptive metadata diagnostics.

## Classification Consistency

Sector count:

`11`

Industry count:

`115`

Sector distribution:

| sector | ticker_count |
| --- | ---: |
| Financials | 54 |
| Information Technology | 47 |
| Health Care | 46 |
| Industrials | 43 |
| Consumer Discretionary | 33 |
| Consumer Staples | 27 |
| Utilities | 27 |
| Real Estate | 26 |
| Materials | 23 |
| Communication Services | 17 |
| Energy | 17 |

Checks performed:

| check | issue_count |
| --- | ---: |
| leading/trailing or double-space issues in ticker/company/sector/industry/source fields | 0 |
| peer labels not starting with `industry:` | 0 |
| peer labels not equal to `industry:` + `industry` | 0 |
| duplicate company names | 0 |

Assessment:

The sector, industry, and peer label fields are mechanically consistent. The peer-group construction is simple and transparent: `peer_group_label = industry:<industry>`.

Caveat:

Industry granularity is uneven. Some labels are broad (`Hotels Restaurants and Leisure`, `Diversified Support Services`), while others are narrower (`Hotels Resorts and Cruise Lines`, `Technology Hardware Storage and Peripherals`, `Paper and Plastic Packaging Products and Materials`). This is acceptable for descriptive diagnostics, but it is not yet strong enough for peer-relative transforms.

## Market-Cap And Size Bucket Consistency

Market-cap bucket distribution:

| market_cap_bucket | ticker_count |
| --- | ---: |
| `large_cap` | 215 |
| `mid_large_cap` | 84 |
| `mega_cap` | 61 |

Size bucket distribution:

| size_bucket | ticker_count |
| --- | ---: |
| `large` | 215 |
| `mid_large` | 84 |
| `mega` | 61 |

Bucket mapping checks:

| expected mapping | mismatch_count |
| --- | ---: |
| `mega_cap` -> `mega` | 0 |
| `large_cap` -> `large` | 0 |
| `mid_large_cap` -> `mid_large` | 0 |

Assessment:

The static market-cap and size buckets are internally consistent.

Caveat:

They remain current static-snapshot approximations. They are not historical market-cap data and cannot support historical size-neutral validation, point-in-time size buckets, or size-relative alpha claims.

## Static Snapshot Warning Audit

| warning_check | result |
| --- | --- |
| rows carrying `STATIC_SNAPSHOT_RESEARCH_ONLY` | 360 / 360 |
| point-in-time validity | False |
| historical alpha validation allowed | False |
| external data fetched by audit runner | False |
| SQLite modified | False |

Assessment:

The static-snapshot boundary is intact.

## Issues Found

No blocking mechanical issues were found for descriptive diagnostic use.

Non-blocking consistency warnings:

1. `source_url_or_reference` is an internal review reference, not an external source citation.
2. Source naming is mostly consistent, but `manual_static_coverage_expansion_review` does not include `_v1` while the reference field does.
3. Industry labels use mixed granularity.
4. Market-cap and size buckets are static approximations.
5. The layer has no point-in-time sector, industry, market-cap, ticker-change, or corporate-action lineage.

These warnings do not block descriptive diagnostics, but they continue to block validation-safe use.

## Fixes Recommended Before Broader Diagnostic Use

Recommended before materially broader diagnostic use:

1. Create a compact lineage dictionary that maps each internal source label to:
   - review note
   - reviewer/process owner if available
   - collection date
   - source policy
   - external-source status
   - no-fetch confirmation
2. Normalize the v1 source label in future metadata versions, preferably to `manual_static_coverage_expansion_v1_review`.
3. Add a metadata audit checklist artifact for future population passes.
4. Review industry granularity for the 9 peer groups currently at or above the 8-name threshold.
5. Keep a row-level exception log if future source review finds classification disputes.

Do not edit historical seed rows casually. If these fixes are applied, they should happen through a controlled metadata versioning step or a dedicated lineage audit artifact.

## Required Before Point-In-Time Or Validation Use

Before any point-in-time or validation use, the project would still need:

- point-in-time sector and industry history
- historical effective dates from a trusted source
- source timestamps tied to source snapshots
- ticker change and corporate action lineage
- delisting and survivorship controls
- historical market-cap or size bucket reconstruction
- source licensing/access review
- reproducible ingestion/audit scripts
- database current/history tables with immutable lineage
- explicit governance approval for validation use

The current seed does not satisfy these requirements.

## Allowed / Blocked Usage Update

Allowed:

- descriptive sector distribution diagnostics
- descriptive inventory metadata coverage checks
- descriptive inventory sector exposure summaries
- static size-bucket distribution diagnostics
- peer-group thinness warnings
- lineage and missingness audits
- source-batch coverage review

Still blocked:

- sector-relative alpha research
- peer-relative transforms
- sector-neutral residualization
- sector-conditioned validation claims
- point-in-time historical claims
- production metadata usage
- survivor/watchlist decisions
- portfolio, ML, blending, or optimization routing

## Decision

Decision:

`SOURCE_LINEAGE_INTERNALLY_CONSISTENT_STATIC_SNAPSHOT_ONLY`

The 360-row seed is internally consistent enough for broader descriptive diagnostic use. It is not externally source-audited and remains unsuitable for point-in-time, validation, sector-relative alpha, or production use.

## Recommended Next Step

Recommended immediate next step:

Create a lightweight `metadata_lineage_dictionary_v1` artifact or note that documents the four internal manual review source labels, their review notes, collection timestamps, and static-snapshot limitations.

Recommended follow-on:

Perform a targeted industry-granularity review for peer groups that are now at or near the 8-name threshold before any exploratory peer diagnostics are expanded.

## Intentional Non-Changes

This review did not:

- modify the seed CSV
- fetch external data
- write SQLite tables
- create alpha candidates
- create sector-relative signals
- make validation claims
- claim point-in-time validity
- modify universe definitions
- change gates, schemas, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
