# Manual Metadata Population Plan v1

Date: 2026-05-24

Status: `PLANNING_ONLY`

## Objective

Define a safe manual workflow for populating `data/metadata/ticker_classification_seed_v1.csv` without contaminating Project Underdog's research layer.

The current seed layer is scaffold-ready but empty:

- seed rows: `0`
- universe tickers: `489`
- coverage ratio: `0.000000`
- status: `SCAFFOLD_READY_EMPTY_SEED`

This plan does not populate the CSV, fetch external data, write SQLite tables, create alpha runners, or start sector-relative research.

## Source Priority

### Preferred Source Hierarchy

Use the most lineage-controlled source available. For v1, the source path should be conservative:

1. Point-in-time professional security master or classification source, if already licensed and available.
2. Date-stamped vendor or exchange classification snapshots, if source dates and usage rights are clear.
3. Manual reviewed current-snapshot CSV built from controlled reference sources.
4. `yfinance` or public profile data only as a reference input for manual review, not as a trusted historical source.
5. Wikipedia / index constituent pages only as reference material, never as the sole trusted research source.

### Acceptable Source Types For Static v1

Acceptable for `STATIC_SNAPSHOT_RESEARCH_ONLY` coverage inspection:

- manually reviewed CSV rows
- frozen source files with source timestamps
- company profile references with collection timestamps
- exchange or SEC identity references for ticker/company-name confirmation
- paid/professional source extracts if available and license permits internal research use

### Not Acceptable For Historical Claims

The following are not acceptable for historical sector-relative or size-relative alpha claims:

- current profile snapshots without effective dates
- manually curated rows without point-in-time source history
- current market cap snapshots applied backward
- current index membership pages applied historically
- any source without collection timestamp or source reference
- any row missing `snapshot_warning = STATIC_SNAPSHOT_RESEARCH_ONLY`

## Field Population Rules

Every populated row must include the required columns below. Empty values are allowed only when a reviewed value is genuinely unavailable and should be audited by the seed runner.

### Required Fields

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

### Field Rules

- `ticker`: must match the project ticker format exactly after normalization to uppercase. Do not invent ticker aliases.
- `company_name`: use the reviewed source name. Do not optimize names for matching after the fact.
- `sector`: broad economic sector label. Use consistent naming across rows.
- `industry`: narrower industry label. If unavailable, leave blank and document missingness through diagnostics.
- `peer_group_label`: use industry when adequate; otherwise use sector fallback according to the peer-group rules below.
- `market_cap_bucket`: use a reviewed static-snapshot bucket only. Do not store raw market cap unless separately approved.
- `size_bucket`: use a simplified size label derived from the same static snapshot logic.
- `source`: source family or reviewed source package name.
- `source_url_or_reference`: controlled reference, file name, source extract id, or manual review reference.
- `as_of_date`: date the row is treated as known to Project Underdog.
- `effective_date`: source-provided classification effective date if available; otherwise leave blank or match `as_of_date` only with a clear static-snapshot caveat.
- `collection_timestamp`: timestamp when the row/source was collected or frozen.
- `universe_version`: should match the audited universe target, initially `dynamic_top300_from_current_large_liquid_pool_v1`.
- `metadata_version`: initially `ticker_classification_seed_v1`.
- `snapshot_warning`: must equal `STATIC_SNAPSHOT_RESEARCH_ONLY` for every row unless a separate point-in-time data process is approved.

## Review Workflow

Manual population should be done in small batches. Do not attempt to fill all 489 tickers in one unreviewed pass.

Recommended workflow:

1. Select a pilot subset.
   - Start with 30 to 50 high-confidence tickers from the current universe.
   - Include multiple sectors and industries.

2. Fill required fields.
   - Use consistent sector and industry vocabulary.
   - Preserve source references.
   - Set `snapshot_warning` to `STATIC_SNAPSHOT_RESEARCH_ONLY`.

3. Run `pipelines/run_metadata_seed_layer_v1.py`.
   - Review coverage, missingness, duplicate, mismatch, group-size, source-audit, and warning artifacts.

4. Review ticker matching.
   - Resolve tickers not in the current universe.
   - Do not silently drop mismatches.
   - Document unresolved tickers through missingness or source notes.

5. Review duplicates.
   - Each ticker should have one active v1 seed row.
   - Duplicates should block use until resolved.

6. Review missingness.
   - Missing sector, industry, peer group, market-cap bucket, and size bucket should be intentional and visible.

7. Review source audit.
   - Check source count, source references, and file hash.
   - Confirm every row has a usable source reference.

8. Review peer-group coverage.
   - Inspect thin groups.
   - Confirm fallback labels are not creating misleading peer groups.

9. Freeze the reviewed seed.
   - Do not proceed to ingestion until the audit artifacts are reviewed and accepted.

## Bucket Rules

Bucket labels should be coarse, stable, and easy to audit. They are static-snapshot labels, not historical size classifications.

### Market-Cap Bucket Definitions

Use these labels if market-cap information is available:

- `mega_cap`: current snapshot market cap above 200B USD
- `large_cap`: 50B to 200B USD
- `mid_large_cap`: 10B to 50B USD
- `small_or_unknown`: below 10B USD or uncertain
- `missing`: no reviewed market-cap reference

These thresholds are design conventions for inspection only. They are not validation gates and must not be backfilled historically.

### Size Bucket Definitions

Use simplified labels derived from `market_cap_bucket`:

- `mega`
- `large`
- `mid_large`
- `small_or_unknown`
- `missing`

Do not use liquidity buckets as size buckets. Liquidity and market capitalization are related but not equivalent.

### Peer-Group Label Fallback Rules

Preferred peer label:

1. Use `industry` when the industry label is available and expected to have adequate group coverage.
2. Fall back to `sector` when industry is missing, inconsistent, or too thin.
3. Use a label format that makes fallback explicit when possible, such as `sector:Information Technology`.
4. Do not mix economic peer labels with proxy buckets like liquidity, volatility, beta, turnover, or residual-vol buckets.

### Thin Peer-Group Handling

Thin peer groups should be flagged, not forced.

Rules:

- Fewer than 8 tickers in a peer group: thin group warning.
- Fewer than 5 tickers: block peer-relative interpretation for that group.
- One-ticker groups: unusable for peer-relative research.
- Excessive fallback to sector labels should trigger review before any research use.

## Quality Thresholds

These thresholds are for coverage inspection readiness, not production or validation.

### Coverage Targets

- Pilot readiness: at least 30 reviewed tickers and at least 5 sectors represented.
- Inspection readiness: at least 50% current universe coverage.
- Broad coverage readiness: at least 90% current universe coverage.
- Pre-ingestion review target: at least 95% current universe coverage, unless missing tickers are documented and accepted.

### Missingness Thresholds

Before any exploratory metadata use:

- sector missingness should be below 5%
- industry missingness should be below 10%
- peer-group missingness should be below 5%
- market-cap bucket missingness should be below 15%
- size bucket missingness should be below 15%
- source reference missingness should be 0%
- snapshot warning missingness should be 0%

### Minimum Peer Group Sizes

Suggested inspection thresholds:

- sector group: at least 10 tickers
- industry or peer group: at least 8 tickers
- groups below threshold should be inactive for group-relative transforms

### Blocking Conditions

Block metadata use if any of these occur:

- any row lacks `snapshot_warning = STATIC_SNAPSHOT_RESEARCH_ONLY`
- duplicate tickers are unresolved
- ticker mismatches are unresolved
- source references are missing
- coverage is below pilot threshold
- peer groups are dominated by one or two large buckets without documented rationale
- market-cap buckets are applied historically
- anyone attempts to use the seed for validation-quality sector-relative alpha claims

## Static Snapshot Safeguards

All rows must carry:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

unless and until a separate point-in-time metadata process is designed and approved.

Safeguards:

- no historical sector-relative validation claims
- no historical size-relative validation claims
- no production registration
- no survivor/watchlist mutation
- no alpha validation routing
- no portfolio, ML, blending, or optimization use
- no assumption that current sector, industry, or market-cap labels were true in the past
- every research note using the seed must state the metadata version and static-snapshot limitation

## Next Implementation Step

Recommended safe next step:

Create a small manually reviewed pilot population in a separate approved step.

Suggested pilot:

- 30 to 50 tickers
- diverse sector coverage
- one reviewed row per ticker
- all required fields present where available
- `snapshot_warning = STATIC_SNAPSHOT_RESEARCH_ONLY` on every row
- `metadata_version = ticker_classification_seed_v1`
- `universe_version = dynamic_top300_from_current_large_liquid_pool_v1`

After the pilot is populated, rerun:

`python pipelines/run_metadata_seed_layer_v1.py`

Then review the generated coverage, missingness, source-audit, duplicate, mismatch, and thin-peer-group artifacts before adding more rows or considering database ingestion.

## Explicit Guardrails

This plan does not:

- populate the CSV
- fetch external data
- write SQLite tables
- create alpha runners
- start sector-relative alpha research
- modify universe definitions
- change schemas, gates, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
