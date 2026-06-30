# Metadata Source Inspection And Ingestion Planning v1

Date: 2026-05-24

Status: `INSPECTION_PLANNING_ONLY`

## Objective

Inspect potential source strategies for adding sector / industry / peer classifications and market-cap / size metadata to Project Underdog.

This note does not fetch, ingest, persist, or validate any external metadata. It is a planning artifact for deciding what source path is safe enough to inspect in a future step.

Core question:

Can any available metadata source support trustworthy research use without introducing look-ahead, survivorship, stale classification, or ticker-mapping contamination?

## Local Context Reviewed

Reviewed local project context:

- `docs/research_notes/sector_industry_peer_metadata_layer_design_v1.md`
- `docs/research_notes/sector_relative_residual_metadata_inspection.md`
- `docs/research_notes/research_capability_gap_review_v1.md`
- existing references to `universe_metadata_current/history`
- existing Track B research notes and proxy-relative batch conventions
- existing SQLite current/history storage pattern

Relevant local conclusion:

The repo has universe membership metadata and research artifact conventions, but no trusted sector, industry, GICS, SIC, security-master, peer-group, or point-in-time market-cap classification layer.

## Sources Inspected Conceptually

No external source was queried or downloaded. The following source options were evaluated as planning candidates only.

| Source option | Available fields likely relevant | Historical availability | Static snapshot risk | Look-ahead risk | Survivorship risk | Ticker mapping risk | Coverage expectation | Update cadence | Reproducibility | Licensing/access practicality | Research-only v1 suitability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `yfinance` ticker info | ticker, company name, exchange, sector, industry, market cap, profile fields | generally current snapshot, not point-in-time | high | high if applied historically | high | medium to high, especially ticker changes/classes | potentially broad but uneven | depends on upstream availability | weak unless raw snapshot is frozen with timestamps | convenient but terms/availability should be reviewed before durable use | suitable only for coverage inspection or static-snapshot exploratory metadata |
| NASDAQ/NYSE public symbol directories | ticker, company name, exchange, listing status, security type; usually not sector/industry | current or date-specific file if frozen manually | medium | medium if historical files unavailable | medium | medium | good for listed symbols/exchange mapping, weak for sector | periodic | moderate if downloaded files are frozen and hashed | practical for exchange/name/listing support | useful as ticker/exchange cross-check, not enough for peer metadata |
| SEC company tickers / company facts metadata | CIK, ticker, company title, filings identity; not reliable sector/industry | filings history exists, but classification fields are limited | medium | lower for identity if as-of controlled, weak for sector | medium | medium; ticker-to-CIK changes matter | decent for SEC registrants, not all traded instruments | periodic | good if source files are frozen | public and practical, but parsing burden exists | useful for identity lineage, not sufficient as sector/industry source |
| Wikipedia / S&P or index lists | ticker, company name, sector/industry for index constituents | often current page state, history possible but messy | very high | high | very high index membership survivorship | medium | limited to index constituents | ad hoc | weak unless page snapshot archived | practical for reference only, not research-grade | reference only; not trusted v1 research metadata |
| Paid/professional security master or classification feed | ticker, company name, exchange, sector, industry, subindustry, market cap, effective dates, corporate actions | best option if point-in-time available | low to medium depending on product | lowest if effective/as-of dates supplied | lowest if survivorship-free universe available | lower, if security identifiers included | potentially strongest | vendor-defined | strong if licensed and versioned | requires procurement/license review | best long-term path; not immediate unless already available |
| Manual reviewed CSV seed | ticker, company name, exchange, sector, industry, peer group, source notes, collection timestamp, optional market cap snapshot | static unless manually versioned | high | high if used historically | high | medium | controllable but labor-bound | manual | strong lineage if frozen, hashed, reviewed | practical if scope is small | safest immediate controlled v1 for inspection, not validation-quality historical research |

## Source-Specific Assessment

### `yfinance` Ticker Info

Potentially useful fields:

- ticker
- company name
- exchange
- sector
- industry
- market cap
- possibly quote type and other profile fields

Main concerns:

- generally current snapshot rather than point-in-time history
- classifications may change without source-level effective dates
- market cap is time-varying and would be especially unsafe to apply historically
- upstream availability and field definitions may be inconsistent
- ticker mapping may fail for delisted names, share classes, renamed tickers, or special listings

Planning conclusion:

`yfinance` may be acceptable for a future coverage inspection snapshot if the raw response is frozen, timestamped, hashed, and labeled `STATIC_SNAPSHOT_NOT_VALIDATION_QUALITY`. It should not be used to make historical sector-neutral alpha claims.

### Public Exchange Symbol Directories

Potentially useful fields:

- ticker
- company/security name
- exchange/listing venue
- ETF/common-stock/security-type flags if available

Main concerns:

- usually insufficient sector/industry detail
- not a peer classification source by itself
- current symbol directories can omit delisted or historical names

Planning conclusion:

Useful as a ticker identity and exchange cross-check. Not sufficient for sector/industry/peer metadata. Could support a future audit layer alongside another classification source.

### SEC Company Tickers / Company Facts

Potentially useful fields:

- ticker
- CIK
- company title
- filing identity

Main concerns:

- does not directly solve sector/industry classification
- ticker-to-CIK mapping changes require care
- market-cap and peer labels would need other sources

Planning conclusion:

Useful for identity lineage and future event/fundamental enrichment. Not sufficient as the first sector/industry source.

### Wikipedia / S&P Lists

Potentially useful fields:

- current index constituent names
- sector labels for some index pages

Main concerns:

- index membership survivorship
- current page state is not historical classification
- coverage is index-limited
- source structure can change
- licensing and reproducibility are weaker than frozen vendor/security-master files

Planning conclusion:

Reference only. Do not use as trusted research metadata for Project Underdog v1.

### Paid / Professional Sources

Potentially useful fields:

- stable security identifiers
- ticker
- company name
- exchange
- sector
- industry
- subindustry
- market cap
- effective dates
- corporate-action and ticker-history data

Main concerns:

- procurement, cost, and licensing
- integration burden
- need to confirm actual point-in-time coverage and redistribution rules

Planning conclusion:

Best long-term path if available. The project should prefer a point-in-time vendor or security-master source before making validation-quality sector-relative historical claims.

### Manual Reviewed CSV Seed

Potentially useful fields:

- ticker
- company name
- exchange
- sector
- industry
- peer group label
- source name
- source notes
- as-of date
- collection timestamp
- reviewer
- metadata version

Main concerns:

- static snapshot only unless repeated and versioned
- manual error risk
- stale classifications
- no true historical effective dates
- coverage may be incomplete

Planning conclusion:

This is the safest immediate v1 path if the goal is controlled metadata coverage inspection, not historical validation. A manually reviewed CSV can be frozen, hashed, audited, and explicitly labeled as static snapshot metadata.

## Recommended v1 Source Strategy

Recommended safest v1 path:

Use a controlled current-snapshot metadata layer for inspection only, preferably built as a manually reviewed CSV seed that may use one or more sources as references, with explicit source notes and static-snapshot warnings.

The v1 strategy should separate three concepts:

1. `classification_coverage_inspection`
   - allowed with static snapshot metadata
   - purpose is to measure coverage, missingness, group sizes, and ticker-mapping quality

2. `exploratory_current_snapshot_research`
   - allowed only with strong warnings
   - no validation-quality claims
   - no historical sector-neutral conclusions

3. `historical_sector_relative_research`
   - deferred until point-in-time or date-stamped metadata is available
   - requires as-of/effective dates and survivorship controls

Preferred immediate source path:

1. Build a manually reviewed CSV seed in a future step.
2. Include source references per record or per batch.
3. Freeze the raw file.
4. Compute a file hash.
5. Load only after a separate ingestion implementation is approved.
6. Label the metadata version as static snapshot unless point-in-time source dates are present.

`yfinance` should not be the sole trusted source for historical research. It can be considered for a future coverage probe or as one reference input into a manual review process, but only if responses are frozen and audited.

## Fields To Collect In Future v1

Minimum v1 classification fields:

- `ticker`
- `company_name`
- `exchange`
- `sector`
- `industry`
- `peer_group_label`
- `source`
- `source_detail`
- `as_of_date`
- `effective_date`
- `collection_timestamp`
- `metadata_version`
- `universe_version`
- `review_status`
- `missing_reason`
- `notes`

Recommended v1 size fields, if available:

- `market_cap`
- `market_cap_currency`
- `market_cap_as_of_date`
- `market_cap_source`
- `market_cap_collection_timestamp`
- `size_bucket`

Important size caveat:

Market cap is time-varying. A current market-cap snapshot should be used only for current coverage diagnostics or exploratory size-bucket inspection. It should not be backfilled into historical alpha research.

## Lineage And Audit Requirements

Any future ingestion must produce source audit information before research use.

Required audit items:

- metadata version
- run id
- source name
- source type
- source file path or controlled source reference
- collection timestamp
- source timestamp when available
- as-of date assigned by Project Underdog
- file hash
- raw record count
- cleaned record count
- matched ticker count
- unmatched ticker count
- duplicate ticker count
- manual override count
- reviewer or process owner
- license/usage notes
- static-snapshot warning flag

Suggested warning fields:

- `static_snapshot_flag`
- `point_in_time_available`
- `validation_quality_allowed`
- `stale_metadata_flag`
- `lookahead_risk_level`
- `survivorship_risk_level`

## Coverage Diagnostics Needed

Future coverage diagnostics should be generated before any alpha research uses the metadata.

Required diagnostics:

- total ticker coverage versus current universe metadata
- coverage against dynamic active universe by date or date window
- missing ticker list
- unmatched ticker list
- duplicate ticker list
- sector count
- industry count
- peer group count
- sector group size distribution
- industry group size distribution
- peer group size distribution
- thin group warnings
- one-sector or one-industry concentration
- missingness by liquidity rank or active membership
- market-cap availability ratio if size is included
- exchange coverage distribution
- current/history consistency checks after tables exist

Minimum decision checks:

- Is coverage high enough for inspection?
- Are missing tickers concentrated in hard-to-map names?
- Are peer groups large enough for group-relative transforms?
- Does the source label enough active top-300 names by date?
- Are classifications static snapshots or point-in-time records?

## Look-Ahead And Survivorship Caveats

The safest interpretation for v1 is conservative:

- A current classification snapshot can describe current coverage.
- It cannot safely reconstruct historical peer groups.
- It cannot support validation-quality historical sector-neutral alpha claims.
- It may leak future classifications into older signal dates.
- It may omit delisted names or historical ticker identities.
- It may misclassify companies that changed business lines, sector labels, or tickers.
- Current market cap is especially unsafe for historical size research.

Required future rule:

Any research note using this metadata must state whether the source is point-in-time, date-stamped snapshot, or static current snapshot.

## Future Ingestion Plan

This is a future plan only, not executed here.

1. Select a controlled source strategy.
   - Prefer point-in-time vendor/security-master if available.
   - Otherwise use a manually reviewed static CSV seed for inspection.

2. Create a staging file.
   - Include minimum fields, source details, and reviewer notes.
   - Do not overwrite raw source labels.

3. Normalize tickers.
   - Match to project ticker format.
   - Preserve unmatched and ambiguous mappings.

4. Freeze and hash the source artifact.
   - Record file hash and collection timestamp.

5. Run coverage diagnostics without alpha research.
   - Current universe coverage.
   - Dynamic membership coverage.
   - group-size adequacy.
   - missing/unmatched diagnostics.

6. Only after inspection, create approved ingestion code.
   - Populate current/history tables.
   - Populate source audit and coverage diagnostics.
   - Keep metadata separate from universe definitions.

7. Produce a metadata ingestion inspection note.
   - State whether the layer is research-only, exploratory, or validation-quality.

8. Defer sector-relative alpha design until metadata quality is known.

## Explicit Out Of Scope

This planning step does not:

- fetch external data
- persist metadata
- create ingestion scripts
- create SQLite tables
- modify existing SQLite tables
- modify universe definitions
- change schemas, gates, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
- start sector-relative alpha research

## Recommendation

Proceed next with a metadata source coverage inspection plan, not ingestion.

Best immediate path:

1. Define a controlled manual CSV schema for current-snapshot sector/industry/peer and optional market-cap fields.
2. Identify candidate references for filling that CSV, with licensing and lineage notes.
3. Freeze a small pilot file in a future approved step.
4. Run coverage and ticker-mapping diagnostics only.
5. Treat the result as `STATIC_SNAPSHOT_RESEARCH_ONLY` unless a point-in-time source is obtained.

Historical sector-relative alpha research should remain paused until the project has point-in-time or date-stamped metadata with acceptable coverage and lineage.
