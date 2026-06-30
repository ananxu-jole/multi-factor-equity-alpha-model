# Manual Metadata Coverage Expansion v1

Date: 2026-05-24

Status: `STATIC_SNAPSHOT_RESEARCH_ONLY_COVERAGE_EXPANSION`

## Objective

Expand `data/metadata/ticker_classification_seed_v1.csv` from the 41-row pilot to approximately 150 manually reviewed static-snapshot rows, then rerun the research-only seed diagnostics.

This is metadata coverage expansion only. It is not point-in-time metadata, not sector-relative alpha research, not validation data, and not production metadata.

## Final Row Count And Coverage

Final seed rows: `150`

Universe tickers audited: `489`

Matched universe tickers: `150`

Missing universe tickers: `339`

Extra seed tickers not in universe: `0`

Coverage ratio: `0.306748`

This improves the seed from pilot smoke-test coverage to early diagnostic coverage, but remains below the manual plan's `50%` inspection-readiness target and far below any broad coverage target.

## Source And Lineage

Sources represented:

- `manual_static_pilot_review`
- `manual_static_coverage_expansion_review`

Source references:

- `manual_metadata_pilot_population_v1_internal_review_no_external_fetch`
- `manual_metadata_coverage_expansion_v1_internal_review_no_external_fetch`

Metadata version:

- `ticker_classification_seed_v1`

Universe version:

- `dynamic_top300_from_current_large_liquid_pool_v1`

Snapshot warning:

- `STATIC_SNAPSHOT_RESEARCH_ONLY`

All rows retain the required static-snapshot warning. No point-in-time validity is claimed.

## Sector Distribution

| sector | ticker_count |
| --- | ---: |
| Information Technology | 28 |
| Financials | 17 |
| Health Care | 17 |
| Consumer Discretionary | 16 |
| Industrials | 16 |
| Consumer Staples | 15 |
| Energy | 10 |
| Communication Services | 9 |
| Utilities | 8 |
| Materials | 7 |
| Real Estate | 7 |

Sector breadth improved materially. Seven sectors now have at least 10 reviewed names, while Communication Services, Utilities, Materials, and Real Estate remain below that threshold.

## Market-Cap And Size Buckets

Market-cap bucket distribution:

| bucket | ticker_count |
| --- | ---: |
| `large_cap` | 93 |
| `mega_cap` | 56 |
| `mid_large_cap` | 1 |

Size bucket distribution:

| bucket | ticker_count |
| --- | ---: |
| `large` | 93 |
| `mega` | 56 |
| `mid_large` | 1 |

The seed is still concentrated in large and mega-cap names, which is expected from the current large/liquid universe and the "recognizable names first" expansion policy.

## Peer-Group Findings

The peer-group distribution remains thin.

Peer groups with at least 8 names:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Semiconductors` | 10 |

Peer groups with at least 5 names:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Semiconductors` | 10 |
| `industry:Application Software` | 7 |
| `industry:Electric Utilities` | 7 |
| `industry:Systems Software` | 6 |
| `industry:Aerospace and Defense` | 5 |

Diagnostic summary:

- total group-size diagnostic rows: `147`
- thin group rows: `132`
- non-thin sector groups: `9`
- non-thin industry groups: `1`
- non-thin peer groups: `1`
- non-thin market-cap buckets: `2`
- non-thin size buckets: `2`

Interpretation:

The expanded seed is now useful for sector distribution diagnostics and basic source/matching audits. It is not yet adequate for broad industry-relative or peer-relative transforms because most industry and peer groups remain below the minimum group-size threshold.

## Missingness And Mismatch Findings

Key-field missingness:

| field | missing_rows | total_rows | missing_ratio |
| --- | ---: | ---: | ---: |
| sector | 0 | 150 | 0.0 |
| industry | 0 | 150 | 0.0 |
| peer_group_label | 0 | 150 | 0.0 |
| market_cap_bucket | 0 | 150 | 0.0 |
| size_bucket | 0 | 150 | 0.0 |

Duplicate ticker check:

- duplicate rows: `0`
- passed: `True`

Ticker mismatch check:

- seed tickers not in universe: `0`
- passed: `True`

Snapshot warning check:

- rows missing `STATIC_SNAPSHOT_RESEARCH_ONLY`: `0`

## Diagnostics Produced

Audit runner:

`python pipelines/run_metadata_seed_layer_v1.py`

Compile check:

`python -m py_compile pipelines/run_metadata_seed_layer_v1.py`

Artifact directory:

- `artifacts/research/research_only_metadata_seed_layer_v1/`

Key artifacts:

- `coverage_summary.csv`
- `missingness_summary.csv`
- `field_completeness.csv`
- `group_size_distribution.csv`
- `thin_peer_groups.csv`
- `duplicate_ticker_checks.csv`
- `ticker_mismatch_checks.csv`
- `static_snapshot_warnings.csv`
- `lineage_source_audit.csv`
- `seed_validation_summary.csv`
- `manifest.json`

## Usability Assessment

Usable now for:

- seed schema diagnostics
- lineage/source audit checks
- static-snapshot warning checks
- duplicate and mismatch diagnostics
- sector distribution review
- market-cap and size bucket distribution review
- identifying which peer groups are still too thin

Not usable for:

- point-in-time historical claims
- sector-relative alpha research
- industry-relative alpha research
- peer-relative transforms
- validation-quality research
- production registration
- portfolio, ML, blending, or optimization routing

## Decision

The coverage expansion is accepted as a controlled static-snapshot metadata diagnostic expansion.

The layer should remain:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

The metadata is now more diagnostically useful than the 41-row pilot, but it is still not ready for sector-relative or peer-relative alpha research.

## Recommended Next Step

Recommended next step:

1. Source-review the 150 rows and correct any naming/classification issues before further expansion.
2. Expand in another controlled batch toward at least `50%` universe coverage.
3. Prioritize underrepresented sectors and thin peer groups:
   - Communication Services
   - Utilities
   - Materials
   - Real Estate
   - non-semiconductor industry groups
4. Continue rerunning `python pipelines/run_metadata_seed_layer_v1.py` after every batch.
5. Do not start sector-relative research until coverage and peer-group adequacy improve materially.

## Intentional Non-Changes

This expansion did not:

- claim point-in-time validity
- start alpha research
- create sector-relative signals
- write SQLite tables
- create metadata current/history tables
- modify universe definitions
- change gates, schemas, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
- remove `STATIC_SNAPSHOT_RESEARCH_ONLY` warnings
