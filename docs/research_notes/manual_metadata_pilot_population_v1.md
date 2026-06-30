# Manual Metadata Pilot Population v1

Date: 2026-05-24

Status: `STATIC_SNAPSHOT_RESEARCH_ONLY_PILOT`

## Objective

Populate a small manually reviewed pilot in `data/metadata/ticker_classification_seed_v1.csv` and run the research-only metadata seed audit.

This is not full-universe metadata population, not point-in-time metadata, not alpha research, and not validation-quality sector-relative data.

## Pilot Scope

Rows added: `41`

Universe tickers audited: `489`

Coverage ratio: `0.083845`

Matched universe tickers: `41`

Extra seed tickers not in universe: `0`

Missing universe tickers: `448`

The pilot intentionally covers recognizable large/liquid names across multiple sectors. It is large enough to test the seed schema and audit runner, but far below the coverage needed for broad research use.

## Source And Lineage

Source label:

- `manual_static_pilot_review`

Source reference:

- `manual_metadata_pilot_population_v1_internal_review_no_external_fetch`

Metadata version:

- `ticker_classification_seed_v1`

Universe version:

- `dynamic_top300_from_current_large_liquid_pool_v1`

Snapshot warning:

- `STATIC_SNAPSHOT_RESEARCH_ONLY`

All rows carry the static-snapshot warning. No external data was fetched automatically. No SQLite tables were written.

Important caveat:

This pilot is manually populated for scaffold and coverage-audit testing. The labels should be source-reviewed before the seed is expanded or used for any exploratory research diagnostics.

## Fields Populated

Every pilot row includes:

- `ticker`
- `company_name`
- `sector`
- `industry`
- `peer_group_label`
- `market_cap_bucket`
- `size_bucket`
- `source`
- `source_url_or_reference`
- `as_of_date`
- `effective_date`
- `collection_timestamp`
- `universe_version`
- `metadata_version`
- `snapshot_warning`

## Sector Coverage

Sector representation:

| sector | ticker_count |
| --- | ---: |
| Information Technology | 10 |
| Consumer Staples | 5 |
| Financials | 5 |
| Health Care | 5 |
| Consumer Discretionary | 4 |
| Communication Services | 4 |
| Energy | 3 |
| Industrials | 3 |
| Materials | 1 |
| Utilities | 1 |

The pilot satisfies the manual plan's pilot diversity goal of at least five sectors represented.

## Market-Cap And Size Buckets

Market-cap bucket representation:

| bucket | ticker_count |
| --- | ---: |
| `mega_cap` | 36 |
| `large_cap` | 5 |

Size bucket representation:

| bucket | ticker_count |
| --- | ---: |
| `mega` | 36 |
| `large` | 5 |

These are static-snapshot buckets only. They must not be backfilled into historical alpha research.

## Diagnostics Review

Generated artifact directory:

- `artifacts/research/research_only_metadata_seed_layer_v1/`

Key diagnostic files:

- `coverage_summary.csv`
- `missingness_summary.csv`
- `group_size_distribution.csv`
- `thin_peer_groups.csv`
- `duplicate_ticker_checks.csv`
- `ticker_mismatch_checks.csv`
- `static_snapshot_warnings.csv`
- `lineage_source_audit.csv`
- `seed_validation_summary.csv`
- `manifest.json`

### Coverage

Coverage is intentionally low:

- coverage ratio: `0.083845`
- pilot rows: `41`
- missing universe tickers: `448`

This is acceptable for pilot scaffold testing, but not sufficient for broad metadata research or ingestion review.

### Missingness

Required classification and bucket fields had zero missingness across the 41 pilot rows:

- sector missingness: `0.0`
- industry missingness: `0.0`
- peer group missingness: `0.0`
- market-cap bucket missingness: `0.0`
- size bucket missingness: `0.0`

### Duplicate And Mismatch Checks

Duplicate ticker check:

- duplicate rows: `0`
- passed: `True`

Ticker mismatch check:

- seed tickers not in universe: `0`
- passed: `True`

The large missing-universe count is expected because this is a pilot, not a full seed.

### Thin Peer Groups

Thin group warnings are expected and active.

All sector, industry, and peer-group labels remain thin under the current thresholds because the pilot covers only 41 names across many categories.

This means the seed layer is usable for diagnostics and workflow testing, but not yet usable for peer-relative transforms or sector-relative research.

### Static Snapshot Warnings

Active warning:

- `static_snapshot_research_only`

Inactive warning:

- `snapshot_warning_field_check` reported `0` rows missing `STATIC_SNAPSHOT_RESEARCH_ONLY`.

## Usability Assessment

Current usability:

- schema smoke test: usable
- lineage/audit smoke test: usable
- coverage diagnostic smoke test: usable
- ticker mismatch diagnostic: usable
- duplicate diagnostic: usable

Not yet usable for:

- full-universe coverage claims
- historical sector-relative validation
- size-relative validation
- alpha discovery
- alpha validation
- portfolio, ML, blending, or optimization routing
- production registration

## Decision

The pilot population is accepted as a controlled static-snapshot metadata seed pilot.

It should remain:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

No point-in-time validity is claimed.

## Recommended Next Step

Before any ingestion or alpha research:

1. Source-review the 41 pilot rows.
2. Decide whether the labels should remain manual-only or be tied to frozen source files.
3. Expand toward at least 50% universe coverage in controlled batches.
4. Rerun `python pipelines/run_metadata_seed_layer_v1.py` after each batch.
5. Do not start sector-relative research until coverage, source audit, and peer-group adequacy pass.

## Intentional Non-Changes

This pilot did not:

- fetch external data automatically
- write SQLite tables
- create metadata current/history tables
- create alpha candidates
- start sector-relative alpha research
- claim point-in-time validity
- modify universe definitions
- change gates, schemas, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
