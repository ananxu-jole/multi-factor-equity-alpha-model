# Manual Metadata Coverage Expansion v2

Date: 2026-05-24

Status: `STATIC_SNAPSHOT_RESEARCH_ONLY_COVERAGE_EXPANSION`

## Objective

Expand `data/metadata/ticker_classification_seed_v1.csv` from 150 reviewed static-snapshot rows toward approximately 250 rows and rerun the research-only metadata diagnostics.

This is diagnostic metadata expansion only. It is not point-in-time metadata, not sector-relative alpha research, not validation data, and not production metadata.

## Final Coverage

Final seed rows: `250`

Universe tickers audited: `489`

Matched universe tickers: `250`

Missing universe tickers: `239`

Extra seed tickers not in universe: `0`

Coverage ratio: `0.511247`

Inventory panel metadata coverage:

| signal_name | panel_tickers | metadata_covered_tickers | metadata_coverage_ratio |
| --- | ---: | ---: | ---: |
| `participation_liquidity_state_shift_20_60` | 478 | 248 | 0.518828 |
| `participation_breadth_repair_under_hostile_trend` | 478 | 248 | 0.518828 |
| `volatility_compression_after_stress_stabilization` | 478 | 248 | 0.518828 |

The expansion crossed the planned 50% coverage threshold for metadata diagnostics and inventory metadata coverage. It remains static-snapshot only.

## Source And Lineage

Sources represented:

- `manual_static_pilot_review`
- `manual_static_coverage_expansion_review`
- `manual_static_coverage_expansion_v2_review`

Source references:

- `manual_metadata_pilot_population_v1_internal_review_no_external_fetch`
- `manual_metadata_coverage_expansion_v1_internal_review_no_external_fetch`
- `manual_metadata_coverage_expansion_v2_internal_review_no_external_fetch`

Metadata version:

- `ticker_classification_seed_v1`

Snapshot warning:

- `STATIC_SNAPSHOT_RESEARCH_ONLY`

All rows retain the required static-snapshot warning. No point-in-time validity is claimed.

## Sector Distribution

| sector | ticker_count |
| --- | ---: |
| Financials | 41 |
| Health Care | 37 |
| Information Technology | 28 |
| Utilities | 26 |
| Real Estate | 24 |
| Materials | 20 |
| Communication Services | 17 |
| Consumer Discretionary | 16 |
| Industrials | 16 |
| Consumer Staples | 15 |
| Energy | 10 |

All 11 represented sectors now have at least 10 names, improving sector distribution diagnostics materially versus v1.

## Market-Cap And Size Buckets

Market-cap bucket distribution:

| bucket | ticker_count |
| --- | ---: |
| `large_cap` | 136 |
| `mega_cap` | 60 |
| `mid_large_cap` | 54 |

Size bucket distribution:

| bucket | ticker_count |
| --- | ---: |
| `large` | 136 |
| `mega` | 60 |
| `mid_large` | 54 |

Size-bucket diversity improved because the v2 expansion added more utilities, materials, real estate, financials, and mid-large capitalization names.

## Peer-Group Improvements

Peer groups at or above the 8-name threshold:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Electric Utilities` | 15 |
| `industry:Health Care Equipment` | 12 |
| `industry:Semiconductors` | 10 |
| `industry:Specialty Chemicals` | 8 |
| `industry:Multi Utilities` | 8 |

Peer groups at or above 5 names:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Electric Utilities` | 15 |
| `industry:Health Care Equipment` | 12 |
| `industry:Semiconductors` | 10 |
| `industry:Specialty Chemicals` | 8 |
| `industry:Multi Utilities` | 8 |
| `industry:Biotechnology` | 7 |
| `industry:Application Software` | 7 |
| `industry:Residential REITs` | 6 |
| `industry:Financial Exchanges and Data` | 6 |
| `industry:Systems Software` | 6 |
| `industry:Retail REITs` | 5 |
| `industry:Property and Casualty Insurance` | 5 |
| `industry:Regional Banks` | 5 |
| `industry:Aerospace and Defense` | 5 |
| `industry:Asset Management and Custody Banks` | 5 |

Diagnostic summary:

- total group-size diagnostic rows: `187`
- thin group rows: `160`
- non-thin sector groups: `11`
- non-thin industry groups: `5`
- non-thin peer groups: `5`
- non-thin market-cap buckets: `3`
- non-thin size buckets: `3`

Interpretation:

Peer diagnostics improved meaningfully, especially outside semiconductors. However, most industry and peer groups remain thin, so this still blocks broad peer-relative transforms and any sector-relative alpha validation.

## Missingness And Mismatch Findings

Key-field missingness:

| field | missing_rows | total_rows | missing_ratio |
| --- | ---: | ---: | ---: |
| sector | 0 | 250 | 0.0 |
| industry | 0 | 250 | 0.0 |
| peer_group_label | 0 | 250 | 0.0 |
| market_cap_bucket | 0 | 250 | 0.0 |
| size_bucket | 0 | 250 | 0.0 |

Duplicate ticker check:

- duplicate rows: `0`
- passed: `True`

Ticker mismatch check:

- seed tickers not in universe: `0`
- passed: `True`

Snapshot warning check:

- rows missing `STATIC_SNAPSHOT_RESEARCH_ONLY`: `0`

## Diagnostics Run

Commands run:

- `python pipelines/run_metadata_seed_layer_v1.py`
- `python pipelines/run_metadata_diagnostic_integration_v1.py`
- `python -m py_compile pipelines/run_metadata_seed_layer_v1.py pipelines/run_metadata_diagnostic_integration_v1.py`

Updated artifact directories:

- `artifacts/research/research_only_metadata_seed_layer_v1/`
- `artifacts/research/metadata_diagnostic_integration_v1/`

Key diagnostic outputs:

- `coverage_summary.csv`
- `metadata_coverage_summary.csv`
- `metadata_readiness_dashboard.csv`
- `sector_distribution.csv`
- `industry_distribution.csv`
- `peer_group_thinness.csv`
- `inventory_metadata_coverage.csv`
- `inventory_candidate_sector_exposure_summary.csv`
- `lineage_source_audit.csv`
- `manifest.json`

## Readiness Assessment

Improved:

- overall metadata coverage crossed 50%
- all 11 sectors now have at least 10 covered names
- inventory panel metadata coverage crossed 50%
- non-semiconductor peer groups improved
- no missing key fields
- no duplicate tickers
- no out-of-universe seed tickers

Still blocked:

- no point-in-time validity
- no historical sector-relative validation claims
- no sector-relative alpha research
- peer groups are still too thin for broad peer-relative transforms
- labels remain manual static-snapshot review and should be source-reviewed further

## Decision

The v2 expansion is accepted as a controlled static-snapshot metadata diagnostic expansion.

The metadata is now useful for:

- sector distribution diagnostics
- inventory metadata coverage diagnostics
- descriptive inventory sector exposure review
- peer-group thinness monitoring
- source/lineage audit checks

It is not usable for:

- point-in-time claims
- sector-relative alpha validation
- peer-relative alpha validation
- production, portfolio, ML, blending, or optimization workflows

## Recommended Next Step

Before any sector-relative alpha research:

1. Source-review the 250 rows for classification consistency.
2. Continue controlled expansion toward broader universe coverage, ideally 70%+.
3. Prioritize peer groups near threshold:
   - `industry:Application Software`
   - `industry:Biotechnology`
   - `industry:Residential REITs`
   - `industry:Financial Exchanges and Data`
   - `industry:Systems Software`
   - `industry:Regional Banks`
4. Consider a separate source-lineage review before any database ingestion.
5. Keep all outputs labeled `STATIC_SNAPSHOT_RESEARCH_ONLY`.

## Intentional Non-Changes

This expansion did not:

- claim point-in-time validity
- start alpha research
- create sector-relative signals
- use metadata for validation claims
- write SQLite tables
- create metadata current/history tables
- modify universe definitions
- change gates, schemas, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
- remove `STATIC_SNAPSHOT_RESEARCH_ONLY` warnings
