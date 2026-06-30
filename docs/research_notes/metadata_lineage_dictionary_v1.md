# Metadata Lineage Dictionary v1

Date: 2026-05-25

Status: `STATIC_SNAPSHOT_LINEAGE_DICTIONARY`

Metadata layer: `ticker_classification_seed_v1`

## Objective

Define the field meanings, expected formats, source conventions, and usage boundaries for the current static-snapshot metadata seed.

This is documentation only. It does not modify the metadata CSV, fetch data, create database tables, authorize alpha research, or claim point-in-time validity.

Current reviewed layer:

- seed rows: `360`
- universe tickers: `489`
- coverage ratio: `0.736196`
- status: `SOURCE_LINEAGE_INTERNALLY_CONSISTENT_STATIC_SNAPSHOT_ONLY`
- required row warning: `STATIC_SNAPSHOT_RESEARCH_ONLY`

## Core Principle

This metadata is a manually reviewed current/static snapshot for descriptive diagnostics.

It is not:

- point-in-time metadata
- validation-safe sector metadata
- a security master
- a production classification table
- a historical market-cap dataset
- authorization for sector-relative or peer-relative alpha research

## Field Dictionary

| field | meaning | expected format | current usage |
| --- | --- | --- | --- |
| `ticker` | Project ticker identifier aligned to the local universe and OHLCV panels. | Uppercase ticker string, matching project universe ticker conventions. | Join key for diagnostics. |
| `company_name` | Human-readable company name used for manual review and audit readability. | Non-empty string. | Descriptive only; not a join key. |
| `sector` | Broad economic sector classification. | Non-empty title-case sector label. | Descriptive sector distribution and exposure diagnostics. |
| `industry` | More specific economic activity label. | Non-empty title-case industry label. | Descriptive industry and peer-group diagnostics. |
| `peer_group_label` | Peer grouping label derived from industry. | `industry:<industry>` | Thinness diagnostics only; no peer-relative transforms. |
| `market_cap_bucket` | Static approximate market-cap category. | One of `mega_cap`, `large_cap`, `mid_large_cap`. | Descriptive static size diagnostics only. |
| `size_bucket` | Simplified static size label aligned to `market_cap_bucket`. | One of `mega`, `large`, `mid_large`. | Descriptive static size diagnostics only. |
| `source` | Internal manual review batch label. | Controlled internal source string. | Source-batch lineage and coverage audit. |
| `source_url_or_reference` | Internal reference for the manual review/population step. | Controlled internal reference string. | Internal audit reference, not external source citation. |
| `as_of_date` | Date the metadata snapshot should be considered reviewed/known to the research process. | `YYYY-MM-DD` | Static-snapshot audit date; not historical effective dating. |
| `effective_date` | Date assigned as effective for the static row. | `YYYY-MM-DD` | Equal to `as_of_date` in the current seed. Not source-provided historical effective date. |
| `collection_timestamp` | Timestamp when the manual batch was frozen into the seed. | UTC ISO-like timestamp, for example `2026-05-25T14:00:00Z`. | Batch lineage and reproducibility. |
| `universe_version` | Universe definition used for coverage checks. | Controlled universe version string. | Current value: `dynamic_top300_from_current_large_liquid_pool_v1`. |
| `metadata_version` | Version label for the metadata seed. | Controlled metadata version string. | Current value: `ticker_classification_seed_v1`. |
| `snapshot_warning` | Required warning that blocks point-in-time, validation, and production use. | Must equal `STATIC_SNAPSHOT_RESEARCH_ONLY`. | Hard interpretability and usage boundary. |

## Source And Reference Conventions

Current allowed source values:

| source | interpretation |
| --- | --- |
| `manual_static_pilot_review` | Initial manually reviewed pilot population batch. |
| `manual_static_coverage_expansion_review` | First coverage expansion batch. This is effectively the v1 expansion label, though the value does not include `_v1`. |
| `manual_static_coverage_expansion_v2_review` | Second coverage expansion batch. |
| `manual_static_coverage_expansion_v3_review` | Third coverage expansion batch. |

Current source reference values:

| source_url_or_reference | interpretation |
| --- | --- |
| `manual_metadata_pilot_population_v1_internal_review_no_external_fetch` | Internal reference for pilot population. |
| `manual_metadata_coverage_expansion_v1_internal_review_no_external_fetch` | Internal reference for first coverage expansion. |
| `manual_metadata_coverage_expansion_v2_internal_review_no_external_fetch` | Internal reference for second coverage expansion. |
| `manual_metadata_coverage_expansion_v3_internal_review_no_external_fetch` | Internal reference for third coverage expansion. |

Convention:

- `source` identifies the internal manual review batch.
- `source_url_or_reference` identifies the internal review step or note family.
- Current references are internal, not external URLs.
- The suffix `no_external_fetch` means the project did not automatically fetch external metadata during the population or audit runner.

Caveat:

These values provide internal lineage only. They do not prove external source lineage, licensing, or point-in-time correctness.

Future preferred source convention:

- Use explicit versioned source names, for example `manual_static_coverage_expansion_v1_review`.
- Preserve old source labels for historical rows unless a controlled metadata-version migration is created.
- If external source snapshots are later used, include source file path/hash, source timestamp, and source license notes in a separate audit artifact or table.

## Static Snapshot Warning

Required value:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

Meaning:

- the row is manually reviewed current/static metadata
- the row is not point-in-time
- the row must not be backfilled into historical alpha validation as if it were known historically
- the row must not be used for production registration, routing, optimization, or trading
- every derived diagnostic should preserve the warning

Any row without this exact value should block use of the affected metadata batch until fixed through a controlled review.

## As-Of Date, Effective Date, And Collection Timestamp

### `as_of_date`

Meaning:

The date the project treats the static row as reviewed and available for research diagnostics.

Current limitation:

It is not a historical classification date.

### `effective_date`

Meaning:

The date assigned as effective for this static snapshot row.

Current limitation:

In the current seed, `effective_date` equals `as_of_date`. It is not source-provided historical effective dating.

### `collection_timestamp`

Meaning:

The timestamp when the batch was frozen into the seed.

Current use:

Batch reproducibility and audit sequencing.

Interpretation rule:

If a future task needs historical correctness, this seed is insufficient. `as_of_date`, `effective_date`, and `collection_timestamp` do not create point-in-time validity.

## Metadata Versioning Convention

Current metadata version:

`ticker_classification_seed_v1`

Meaning:

The manually reviewed seed CSV version used for static-snapshot diagnostics.

Expected rules:

- Do not silently overwrite semantics under the same version.
- If fields, source conventions, or classification policy materially change, create a new metadata version.
- If rows are corrected, record the correction in a review note or audit artifact.
- Current rows should not be edited casually without a controlled lineage note.

## Universe Versioning Convention

Current universe version:

`dynamic_top300_from_current_large_liquid_pool_v1`

Meaning:

The local universe definition used for coverage diagnostics against the current project universe.

Expected rules:

- Coverage ratios are only meaningful relative to the stated `universe_version`.
- A future universe change requires rerunning coverage diagnostics.
- Metadata coverage does not imply point-in-time membership coverage.

## Peer Group Label Convention

Current convention:

`peer_group_label = industry:<industry>`

Examples:

- `industry:Semiconductors`
- `industry:Application Software`
- `industry:Electric Utilities`

Interpretation:

Peer labels are simple industry-derived diagnostic groups. They are useful for group-size and thinness warnings.

Blocked:

- peer-relative ranking
- peer z-scores
- peer neutralization
- peer residualization
- peer-conditioned validation claims

Reason:

The labels are static, manually reviewed, and many groups remain thin or uneven in granularity.

## Market-Cap And Size Bucket Conventions

Allowed `market_cap_bucket` values:

- `mega_cap`
- `large_cap`
- `mid_large_cap`

Allowed `size_bucket` values:

- `mega`
- `large`
- `mid_large`

Expected mapping:

| market_cap_bucket | size_bucket |
| --- | --- |
| `mega_cap` | `mega` |
| `large_cap` | `large` |
| `mid_large_cap` | `mid_large` |

Interpretation:

These are static approximate size categories for descriptive diagnostics.

Blocked:

- historical market-cap claims
- size-neutral alpha validation
- size-relative transforms
- market-cap backfills
- production sizing or optimization use

## Allowed Uses

Allowed under the current static-snapshot status:

- metadata coverage dashboards
- source-batch coverage review
- missingness and lineage audits
- sector distribution diagnostics
- descriptive inventory metadata coverage checks
- descriptive inventory sector exposure summaries
- static size-bucket distribution diagnostics
- peer-group size diagnostics
- thin peer-group warnings
- readiness reviews for future metadata work

All outputs should preserve:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

## Blocked Uses

Blocked under the current status:

- alpha research
- sector-relative alpha candidates
- peer-relative alpha candidates
- sector-neutral residualization
- peer-relative transforms
- size-relative transforms
- sector-conditioned validation claims
- point-in-time historical claims
- production registration
- survivor/watchlist mutation
- validation routing
- gates, schemas, thresholds, or governance changes
- portfolio, ML, blending, or optimization routing

## Future Point-In-Time Upgrade Requirements

Before this metadata can support point-in-time or validation-quality work, the project would need:

- trusted source with sector and industry history
- historical effective start/end dates
- source collection timestamps tied to immutable source snapshots
- source file hashes or source snapshot identifiers
- ticker-change and corporate-action lineage
- delisting and survivorship controls
- historical market-cap or size data
- licensing/access review
- database current/history tables
- append-only source audit history
- missingness and stale-record diagnostics by date
- explicit governance approval for validation use

Until those requirements are met, this layer remains static-snapshot diagnostic metadata only.

## Decision

Current dictionary decision:

`LINEAGE_DICTIONARY_ESTABLISHED_STATIC_SNAPSHOT_ONLY`

The current metadata fields and conventions are sufficiently documented for descriptive diagnostic use. They are not sufficient for point-in-time, validation, alpha, production, or routing use.

## Intentional Non-Changes

This dictionary did not:

- modify the CSV
- fetch data
- write SQLite tables
- start alpha research
- create sector-relative signals
- make validation claims
- claim point-in-time validity
- modify universe definitions
- change gates, schemas, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
