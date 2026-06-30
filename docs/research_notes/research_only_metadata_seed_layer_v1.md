# Research-Only Metadata Seed Layer v1

Date: 2026-05-24

Status: `STATIC_SNAPSHOT_RESEARCH_ONLY`

## Objective

Implement a small research-only seed layer scaffold for sector / industry / peer and market-cap / size coverage inspection.

This note documents the seed CSV template and coverage-audit runner. It does not create point-in-time metadata and does not authorize historical sector-relative alpha validation.

## Guardrail

This metadata layer is static-snapshot research scaffolding only. It must not be used for production registration, survivor/watchlist mutation, validation routing, gates, schemas, governance, detector logic, portfolio, ML, blending, optimization, or alpha research claims.

## Files

- `data/metadata/ticker_classification_seed_v1.csv`
- `pipelines/run_metadata_seed_layer_v1.py`
- `artifacts/research/research_only_metadata_seed_layer_v1/`

## Seed Fields

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

## Coverage Result

- Seed rows: `360`
- Seed distinct tickers: `360`
- Universe distinct tickers: `489`
- Matched universe tickers: `360`
- Coverage ratio: `0.736196`

If this is the empty template run, zero coverage is expected. Coverage becomes meaningful only after reviewed metadata rows are added in a separately approved step.

## Missingness Summary

| field             |   missing_rows |   total_rows |   missing_ratio |
|:------------------|---------------:|-------------:|----------------:|
| sector            |              0 |          360 |               0 |
| industry          |              0 |          360 |               0 |
| peer_group_label  |              0 |          360 |               0 |
| market_cap_bucket |              0 |          360 |               0 |
| size_bucket       |              0 |          360 |               0 |

## Active Warnings

- `static_snapshot_research_only`: This seed layer is not point-in-time and must not be used for historical sector-relative alpha validation.
- `no_external_fetch_performed`: The runner reads only the local seed CSV and local universe metadata.

## Diagnostics Produced

- `coverage_summary.csv`
- `duplicate_ticker_checks.csv`
- `field_completeness.csv`
- `group_size_distribution.csv`
- `lineage_source_audit.csv`
- `manifest.json`
- `missingness_summary.csv`
- `seed_normalized_preview.csv`
- `seed_validation_summary.csv`
- `static_snapshot_warnings.csv`
- `thin_peer_groups.csv`
- `ticker_mismatch_checks.csv`

## Interpretation

The scaffold is ready for controlled metadata coverage inspection. It is not an ingested classification layer, not point-in-time, and not suitable for historical sector-relative or size-relative alpha validation.

## Recommended Next Step

Populate a small manually reviewed pilot seed in a future approved step, then rerun this audit to inspect coverage, ticker mismatches, group sizes, missingness, and lineage quality before any database ingestion is considered.

## Intentional Non-Changes

- no external data fetched
- no SQLite writes or metadata tables created
- no universe definition changes
- no gate, schema, validation, governance, production, survivor/watchlist, detector, portfolio, ML, blending, or optimization changes
- no sector-relative alpha research started
