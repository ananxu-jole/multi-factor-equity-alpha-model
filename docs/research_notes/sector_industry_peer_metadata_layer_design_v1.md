# Sector / Industry / Peer Metadata Layer Design v1

Date: 2026-05-24

Status: `DESIGN_ONLY`

## Objective

Design a trustworthy research-only sector / industry / peer metadata layer for Project Underdog.

The goal is to support future sector-relative, industry-relative, and peer-relative research without introducing look-ahead, stale classification, or survivorship errors that would contaminate alpha discovery.

This is a design note only. It does not fetch external data, create tables, implement loaders, change universe definitions, or alter any production, validation, governance, detector, survivor/watchlist, portfolio, ML, blending, or optimization path.

## Why This Layer Is Needed

Recent research established that the current bottleneck is likely information content and metadata richness, not research discipline.

Current limitations:

- true sector-relative research is not feasible
- no usable sector, industry, GICS, SIC, security-master, or peer-group table exists
- proxy-relative buckets are diagnosable but economically weak
- OHLCV-only branches repeatedly produced clean diagnostics but weak standalone alpha
- liquidity, volatility, turnover, and residual-volatility proxies do not reliably identify business peers

This layer is needed so future research can ask better questions:

- Is a stock resilient relative to its actual sector or industry peers?
- Is repair behavior idiosyncratic or just sector rebound?
- Are liquidity/volatility effects really company-specific or sector-wide?
- Does an alpha survive sector-relative residualization?
- Are current inventory candidates concentrated in specific sectors or peer groups?

## Required Metadata Fields

Minimum viable v1 fields:

- `ticker`
- `sector`
- `industry`
- `peer_group_label`
- `source`
- `as_of_date`
- `effective_date`
- `collection_timestamp`
- `universe_version`
- `metadata_version`

Recommended additional fields:

- `subindustry`
- `classification_system`
- `source_version`
- `source_url_or_file`
- `source_record_id`
- `effective_start`
- `effective_end`
- `is_current`
- `classification_confidence`
- `manual_override_flag`
- `missing_reason`
- `stale_metadata_flag`
- `notes`
- `run_id`

Field semantics:

- `ticker`: project ticker identifier aligned to existing OHLCV/universe tickers.
- `sector`: broad economic sector label.
- `industry`: narrower economic industry label.
- `peer_group_label`: research grouping label used for peer-relative transforms. For v1 this can equal industry when available, or sector when industry coverage is insufficient.
- `source`: source name, such as vendor, curated file, exchange dataset, or manual seed file.
- `as_of_date`: date the metadata should be considered known to the research process.
- `effective_date`: date the classification is reported as effective by the source, if available.
- `collection_timestamp`: timestamp when Project Underdog collected or froze the record.
- `universe_version`: universe version the coverage was evaluated against.
- `metadata_version`: version of the classification dataset within Project Underdog.

## Source Options To Consider Later

No source should be fetched during this design step. Future source options should be evaluated by coverage, licensing, point-in-time quality, lineage, and update process.

Possible source categories:

- existing internal curated file, if one exists outside the current repo tables
- vendor sector/industry feed with point-in-time effective dates
- public company profile data, only if licensing and update lineage are acceptable
- exchange/security-master data with sector/industry fields
- ETF or index constituent classification files
- manually curated seed file for research-only inspection, clearly labeled as non-point-in-time if static

Source preference order:

1. point-in-time vendor or security-master classification
2. date-stamped vendor snapshots with repeatable collection
3. current snapshot with strong stale-data warnings
4. manual research seed file for coverage inspection only

A current snapshot can be useful for exploratory research, but it should not be treated as validation-quality historical metadata.

## Storage Design

Use the existing project pattern of current and history tables in SQLite, plus diagnostics and lineage tables.

Recommended tables:

1. `ticker_classification_current`
2. `ticker_classification_history`
3. `ticker_classification_coverage_diagnostics_current`
4. `ticker_classification_coverage_diagnostics_history`
5. `ticker_classification_source_audit_current`
6. `ticker_classification_source_audit_history`

### `ticker_classification_current`

Purpose:

Hold the latest frozen classification record per ticker, metadata version, and source.

Suggested columns:

- `ticker`
- `sector`
- `industry`
- `subindustry`
- `peer_group_label`
- `classification_system`
- `source`
- `source_version`
- `source_record_id`
- `as_of_date`
- `effective_date`
- `effective_start`
- `effective_end`
- `is_current`
- `classification_confidence`
- `manual_override_flag`
- `missing_reason`
- `stale_metadata_flag`
- `universe_name`
- `universe_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `notes`

Suggested uniqueness:

- one current row per `ticker`, `source`, `metadata_version`, and `universe_version`

### `ticker_classification_history`

Purpose:

Append every collected/frozen classification record to preserve lineage and support point-in-time reconstruction.

Suggested columns should match the current table, plus:

- `history_insert_timestamp`
- `superseded_by_run_id`
- `record_hash`

Suggested uniqueness:

- no destructive overwrite requirement
- allow multiple records per ticker across sources, as-of dates, and metadata versions

### Coverage Diagnostics Tables

Purpose:

Store coverage and quality summaries for each metadata freeze.

Suggested columns:

- `run_id`
- `metadata_version`
- `universe_name`
- `universe_version`
- `diagnostic_date`
- `classification_source`
- `total_universe_tickers`
- `classified_tickers`
- `missing_tickers`
- `coverage_ratio`
- `sector_count`
- `industry_count`
- `peer_group_count`
- `min_sector_group_size`
- `median_sector_group_size`
- `min_industry_group_size`
- `median_industry_group_size`
- `thin_sector_group_count`
- `thin_industry_group_count`
- `missing_ticker_list`
- `stale_record_count`
- `manual_override_count`
- `notes`

For dynamic top-300 membership, diagnostics should also be computed by date or date window:

- classified active names per date
- missing active names per date
- thin peer groups per date
- sector share drift over time

### Source Audit Tables

Purpose:

Record provenance and reproducibility for each metadata ingestion/freeze.

Suggested columns:

- `run_id`
- `metadata_version`
- `source`
- `source_version`
- `source_file_path`
- `source_url`
- `source_download_timestamp`
- `source_file_hash`
- `record_count_raw`
- `record_count_clean`
- `ticker_match_count`
- `ticker_unmatched_count`
- `normalization_rules`
- `manual_override_count`
- `license_or_usage_notes`
- `created_by`
- `collection_timestamp`
- `notes`

## Temporal Integrity Rules

The metadata layer must avoid future leakage.

Rules:

1. Research transforms must use only metadata with `as_of_date <= signal_date`.
2. If `effective_start` and `effective_end` are available, use the record active on the signal date.
3. If only a current snapshot is available, label outputs as static-snapshot research and block validation-quality claims.
4. Collection timestamps must be stored so the project knows when a classification was actually obtained.
5. Classification changes must be append-only in history.
6. Current tables may be replaced by a new freeze, but history must preserve prior records.
7. No alpha runner should silently fill missing historical classification with future classifications.
8. Any forward-filled classification should require explicit stale-metadata flags and maximum staleness diagnostics.

Temporal hierarchy:

- Prefer `effective_start/effective_end` when source provides it.
- Else use `as_of_date`.
- Else use `collection_timestamp` and mark as static snapshot.

## Handling Classification Changes

Classification changes should be first-class records, not silent overwrites.

Design expectations:

- keep both old and new classification records in history
- mark latest record in current table
- include effective dates when known
- preserve source and source version
- detect ticker classification changes between metadata versions
- produce change diagnostics by ticker, sector, industry, and peer group

Change diagnostics should include:

- number of tickers with changed sector
- number of tickers with changed industry
- number of tickers with changed peer group
- old/new labels
- first observed change date
- source responsible for change

## Survivorship And Stale Metadata Risks

Known risks:

- The current raw ticker pool is not fully survivorship-free.
- Dynamic top-300 liquidity membership reduces same-day liquidity look-ahead but does not solve raw-pool survivorship.
- Static current classification applied historically can introduce stale or future classification leakage.
- Mergers, ticker changes, spin-offs, and reclassifications can distort historical peer groups.
- Missing sector data may cluster in newer listings or special cases.

Risk controls:

- clearly distinguish point-in-time metadata from static snapshot metadata
- store coverage against both current universe and dynamic membership dates
- flag missing and stale classifications
- avoid validation-quality conclusions from static current snapshots
- require minimum group sizes for sector/industry transforms
- keep ticker matching and unmatched ticker diagnostics

## Coverage And Quality Diagnostics

Required diagnostics before any alpha research uses this layer:

- total ticker coverage
- dynamic top-300 active coverage by date
- missing classification count and ratio
- missing ticker list
- sector group counts and group sizes
- industry group counts and group sizes
- peer group counts and group sizes
- thin group warnings
- sector/industry concentration by universe date
- stale metadata count
- classification change count
- source coverage by ticker
- unmatched ticker count
- duplicate ticker/classification records
- current/history consistency checks

Suggested minimum coverage thresholds for research use:

- at least 95% coverage of current universe tickers for exploratory research
- at least 90% coverage of dynamic top-300 active names by date
- minimum 10 active names per sector group/date for sector-relative ranks
- minimum 8 active names per industry or peer group/date for industry-relative ranks
- if group sizes are thinner, fall back to sector-level grouping or mark date/group inactive

These are design thresholds, not production gates.

## Peer-Group Construction Logic

Peer groups should be simple and auditable in v1.

Recommended hierarchy:

1. Use `industry` as peer group when coverage and group size are adequate.
2. Fall back to `sector` when industry group is too thin.
3. Use `subindustry` only after coverage is proven adequate.
4. Do not mix proxy buckets with economic peer labels in the same peer-group field.
5. Store fallback logic explicitly, e.g. `peer_group_method = industry_or_sector_fallback`.

Possible peer group fields:

- `peer_group_label`
- `peer_group_level`
- `peer_group_method`
- `peer_group_min_size`
- `peer_group_source`

Peer group diagnostics:

- active names per peer group/date
- peer group fallback rate
- peer group turnover over time
- missing peer group rate
- one-peer-group dominance

## Integration With Existing Project Infrastructure

SQLite:

- follow current/history table pattern used by universe and price data
- use `src.db.table_exists`, `load_table`, and future loaders consistent with `load_universe_metadata`
- keep classification tables separate from existing universe tables

Universe:

- do not change universe definitions
- join metadata to universe tickers and dynamic top-300 membership as a research overlay
- compute coverage against `universe_metadata_current/history` and dynamic membership tables

Track B research:

- future research runners should load classification panels or date/ticker tables as inputs
- group-relative ranks/z-scores should require minimum group size
- sector-relative results should always compare against universe-relative and proxy-relative baselines
- metadata version and source should be written into manifests

Research notes:

- every sector/industry/peer-relative batch should state metadata version, source, coverage, and point-in-time quality

## Minimal Viable v1 Layer

The minimal viable v1 should be research-only and should prioritize coverage, lineage, and diagnostics over alpha use.

Minimum viable fields:

- `ticker`
- `sector`
- `industry`
- `peer_group_label`
- `source`
- `as_of_date`
- `effective_date`
- `collection_timestamp`
- `universe_version`
- `metadata_version`
- `run_id`
- `notes`

Minimum viable artifacts/tables:

- `ticker_classification_current`
- `ticker_classification_history`
- `ticker_classification_coverage_diagnostics_current`
- `ticker_classification_source_audit_current`

Minimum viable diagnostics:

- current universe coverage
- dynamic top-300 coverage by date
- missing ticker list
- group-size distribution
- thin group warnings
- source audit and file hash
- static-snapshot warning if no point-in-time dates exist

Minimum viable use:

- inspection and coverage reporting
- design of future sector-relative research
- no validation-quality alpha claims until temporal quality is established

## Recommended v1 Implementation Plan

This is a future implementation plan, not executed by this note.

1. Identify candidate metadata source.
   - Prefer point-in-time classification.
   - If unavailable, use a current snapshot only for research inspection.

2. Create a staging artifact.
   - Normalize tickers.
   - Preserve raw source labels.
   - Compute source file hash.

3. Match to current universe.
   - Report matched and unmatched tickers.
   - Do not silently drop unmatched tickers.

4. Write current/history classification tables.
   - Current table contains latest frozen records.
   - History table appends all records.

5. Write source audit table.
   - Include source, timestamp, version, hash, and normalization notes.

6. Write coverage diagnostics.
   - Current universe coverage.
   - Dynamic membership coverage by date/window.
   - Sector/industry/peer group sizes.

7. Produce an inspection note.
   - State whether the layer is point-in-time or static snapshot.
   - State whether sector-relative research is exploratory-only or validation-eligible.

8. Only after the inspection passes, design a sector-relative residual alpha batch.

## Out Of Scope For v1

Do not include in v1:

- alpha candidates
- sector-relative signal runners
- production registration
- survivor/watchlist changes
- validation routing
- portfolio, ML, blending, or optimization integration
- automatic external data fetching without explicit approval
- complex security-master reconstruction
- ticker change history beyond what the source provides
- fundamentals or market-cap enrichment unless separately scoped
- options, borrow, short interest, or ETF-flow data

## Explicit Guardrails

This design does not:

- fetch external data
- implement code
- create metadata tables
- modify universe definitions
- change schemas, gates, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization

