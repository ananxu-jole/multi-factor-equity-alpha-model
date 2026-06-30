# Economic Context Enrichment Design v1

Date: 2026-05-26

Status: `DESIGN_ONLY`

Decision scope: prepare Project Underdog for future metadata-enriched conditional structural asymmetry research. This design does not implement code, create tables, fetch data, change validation anchors, alter WFV logic, change candidate status, promote signals, modify production logic, redesign governance, route anything into portfolio/ML/blending/optimization, or replace raw h10/h20 IC.

Raw h10/h20 forward-return IC remains the validation anchor. Recovery/post-stress targets remain diagnostic sidecars only.

## 1. Objective

Project Underdog's recent strategic synthesis concluded that the main bottleneck is economic specificity, not governance or validation discipline. Recent OHLCV-only branches were clean, diagnosable, and well governed, but mostly underpowered.

The next frontier is:

`metadata-enriched conditional structural asymmetry research`

The purpose of this enrichment layer is to let future research test whether repair, stabilization, participation, liquidity, volatility compression, and downside containment behave differently relative to economically comparable names.

The layer should support future questions such as:

- Does a stock repair better than its sector or industry peers after stress?
- Is volatility compression idiosyncratic or just sector-wide stabilization?
- Does participation asymmetry matter only after controlling for size and liquidity?
- Are current inventory signals concentrated in sectors, size buckets, or liquidity regimes?
- Does conditional persistence survive peer-relative normalization?

## 2. Required Economic Metadata

### Core Economic Classifications

Required before any sector/peer-aware research:

- `ticker`
- `company_name`
- `sector`
- `industry`
- `subindustry`, if available
- `peer_group_label`
- `classification_system`, such as GICS, SIC, NAICS, vendor taxonomy, or manual taxonomy
- `source`
- `source_record_id`, if available
- `source_version`
- `source_url_or_reference`
- `as_of_date`
- `effective_start`
- `effective_end`
- `collection_timestamp`
- `universe_version`
- `metadata_version`
- `snapshot_warning`
- `point_in_time_quality`

### Size And Market-Cap Context

Needed to separate liquidity effects from size effects:

- `market_cap`
- `market_cap_bucket`
- `size_bucket`
- `market_cap_as_of_date`
- `market_cap_source`
- `market_cap_source_version`
- `market_cap_collection_timestamp`
- `market_cap_point_in_time_quality`

Minimum useful buckets:

- `mega_cap`
- `large_cap`
- `mid_large_cap`
- `mid_cap`, if universe coverage supports it
- `small_cap`, only if the universe later includes enough names

### Behavioral Context Buckets

These can be built from existing OHLCV panels because they are derived from historical data available inside the project:

- `liquidity_bucket`
- `volatility_bucket`
- `residual_vol_bucket`
- `turnover_bucket`
- `beta_bucket`
- `style_bucket`, optional and only if constructed from pre-signal-date data

Behavioral buckets should be date-aware. They are not substitutes for sector/industry metadata, but they can be useful controls and diagnostics.

## 3. Allowed Use By Metadata Type

| metadata type | current safe use | alpha validation use | peer-relative normalization | candidate design use |
| --- | --- | --- | --- | --- |
| Static sector/industry snapshot | Descriptive diagnostics only | Blocked | Blocked | Design notes only |
| Point-in-time sector/industry | Allowed after coverage and lineage checks | Potentially allowed after explicit approval | Potentially allowed | Allowed for research batches |
| Static size bucket | Descriptive diagnostics only | Blocked | Blocked | Design notes only |
| Point-in-time market cap / size | Allowed after lineage checks | Potentially allowed as diagnostic/control | Potentially allowed | Allowed for size-controlled research |
| Date-derived liquidity bucket | Diagnostics and research controls | Allowed only if computed from pre-signal data and frozen | Allowed as control, not economic peer substitute | Allowed |
| Date-derived volatility bucket | Diagnostics and research controls | Allowed only if computed from pre-signal data and frozen | Allowed as control, not economic peer substitute | Allowed |
| Date-derived beta/style bucket | Diagnostics first | Block until formula is frozen and leakage-reviewed | Possible later | Design cautiously |
| Recovery/post-stress target labels | Diagnostic sidecar only | Blocked as validation replacement | Not applicable | Mechanism interpretation only |

## 4. Point-In-Time Integrity Requirements

### Must Be Point-In-Time For Validation Or Alpha Claims

These fields must be point-in-time safe before they can support alpha validation, peer-relative transforms, sector-relative ranks, or historical conclusions:

- sector
- industry
- subindustry
- peer group
- market cap
- size bucket
- beta/style bucket if sourced externally or reconstructed from rolling history
- any source classification changes
- ticker and corporate-action lineage

Required temporal controls:

- use only records with `as_of_date <= signal_date`
- prefer `effective_start <= signal_date < effective_end` when available
- store `collection_timestamp`
- preserve source snapshots or source file hashes
- append changes into history tables
- never silently backfill a current classification into historical periods

### Can Be Approximate For Diagnostics

Static snapshot metadata can support:

- universe coverage dashboards
- sector/industry distribution summaries
- descriptive inventory exposure checks
- source-lineage audits
- missingness reviews
- peer-group thinness warnings

Every output must preserve:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

### Blocked If Not Point-In-Time Safe

Without point-in-time metadata, block:

- sector-relative alpha candidates
- industry-relative alpha candidates
- peer-relative residualization
- sector-conditioned IC claims
- validation decisions based on sector/peer/size slices
- production routing
- portfolio/ML/blending/optimization usage

## 5. Recommended SQLite Schema

This design extends the existing current/history discipline. The tables below are proposed only; this note does not create them.

### Classification Tables

`economic_context_classification_current`

Latest active economic classification per ticker, metadata version, universe version, and source.

Core columns:

- `ticker`
- `company_name`
- `sector`
- `industry`
- `subindustry`
- `peer_group_label`
- `peer_group_level`
- `classification_system`
- `source`
- `source_version`
- `source_record_id`
- `as_of_date`
- `effective_start`
- `effective_end`
- `is_current`
- `point_in_time_quality`
- `snapshot_warning`
- `universe_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `notes`

`economic_context_classification_history`

Append-only history for every classification freeze or source update. Same columns as current plus:

- `history_insert_timestamp`
- `superseded_by_run_id`
- `change_reason`

### Size Tables

`economic_context_size_current`

Latest size and market-cap context per ticker.

Core columns:

- `ticker`
- `market_cap`
- `market_cap_bucket`
- `size_bucket`
- `currency`
- `market_cap_as_of_date`
- `effective_start`
- `effective_end`
- `source`
- `source_version`
- `point_in_time_quality`
- `snapshot_warning`
- `universe_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `notes`

`economic_context_size_history`

Append-only history for all size records.

### Behavioral Bucket Tables

`economic_context_behavior_bucket_current`

Latest date-aware behavioral bucket assignment.

Core columns:

- `date`
- `ticker`
- `liquidity_bucket`
- `volatility_bucket`
- `residual_vol_bucket`
- `turnover_bucket`
- `beta_bucket`
- `style_bucket`
- `lookback_window`
- `calculation_method`
- `min_history_days`
- `as_of_date`
- `metadata_version`
- `run_id`
- `created_at`
- `notes`

`economic_context_behavior_bucket_history`

Append-only history for bucket generation runs.

### Peer Group Tables

`economic_context_peer_group_current`

Resolved peer group assignment after fallback logic.

Core columns:

- `date`
- `ticker`
- `peer_group_label`
- `peer_group_level`
- `peer_group_method`
- `fallback_used`
- `peer_group_size`
- `peer_group_min_size`
- `source_metadata_version`
- `point_in_time_quality`
- `run_id`
- `created_at`
- `notes`

`economic_context_peer_group_history`

Append-only peer group assignments by date/run.

### Diagnostics And Audit Tables

`economic_context_coverage_diagnostics_current`

Latest coverage and quality summary.

`economic_context_coverage_diagnostics_history`

Append-only diagnostics by run.

`economic_context_source_audit_current`

Latest source lineage summary.

`economic_context_source_audit_history`

Append-only source lineage history.

`economic_context_quality_alerts_current`

Latest quality warnings.

`economic_context_quality_alerts_history`

Append-only warning history.

## 6. Proposed Source Module Structure

No modules are implemented by this design. Proposed future structure:

```text
src/
  economic_context/
    __init__.py
    metadata_loader.py
    metadata_validator.py
    sector_industry_mapper.py
    size_bucket_builder.py
    behavior_bucket_builder.py
    peer_group_builder.py
    enrichment_diagnostics.py
    source_lineage.py
    sqlite_persistence.py
    quality_checks.py
```

### Module Responsibilities

`metadata_loader.py`

- load static seed CSVs
- load future point-in-time source extracts
- normalize ticker strings
- preserve raw source fields
- attach metadata version and universe version

`metadata_validator.py`

- validate required columns
- check date formats
- check `snapshot_warning`
- check source completeness
- block unsafe use cases

`sector_industry_mapper.py`

- standardize sector/industry labels
- preserve raw labels and normalized labels
- identify classification changes
- produce sector/industry distribution diagnostics

`size_bucket_builder.py`

- build market-cap and size buckets
- distinguish static snapshot from point-in-time records
- diagnose size/liquidity overlap

`behavior_bucket_builder.py`

- build date-aware liquidity, volatility, residual-vol, turnover, and beta buckets
- enforce pre-signal lookback windows
- prevent same-day or future leakage

`peer_group_builder.py`

- assign peer groups using industry first, then sector fallback
- enforce minimum group sizes
- record fallback rates
- block peer-relative transforms when point-in-time quality is insufficient

`enrichment_diagnostics.py`

- produce coverage dashboards
- produce distribution and cross-tab reports
- produce inventory exposure summaries
- produce thin-group and concentration warnings

`source_lineage.py`

- hash source files
- track source versions
- track collection timestamps
- record license/access notes when available

`sqlite_persistence.py`

- write current/history tables
- enforce append-only history behavior
- store run manifests

`quality_checks.py`

- centralize missingness, duplicates, stale metadata, invalid dates, mismatch, and concentration checks

## 7. Data Quality Checks

Required checks before any alpha research:

### Coverage And Missingness

- total universe coverage
- dynamic active-universe coverage by date
- missing sector count and ratio
- missing industry count and ratio
- missing peer group count and ratio
- missing market cap and size bucket count
- missing source and timestamp count

### Identity And Mapping

- ticker mismatch against project universe
- duplicate ticker records in current tables
- duplicate active records per ticker/date
- duplicate company names mapped to multiple tickers
- ticker-change or corporate-action warnings if available

### Temporal Integrity

- `as_of_date <= signal_date` for any research transform
- `effective_start <= signal_date < effective_end` where available
- invalid effective date ranges
- missing collection timestamps
- stale classification age
- future classification leakage warnings

### Group Quality

- sector group size by date
- industry group size by date
- peer group size by date
- thin peer groups
- fallback rate from industry to sector
- one-peer-group dominance
- sector concentration
- industry concentration

### Cross-Exposure Diagnostics

- size by sector cross-tab
- liquidity by sector cross-tab
- volatility by sector cross-tab
- size/liquidity overlap
- liquidity/volatility overlap
- sector exposure by current inventory candidate
- size/liquidity exposure by current inventory candidate

### Use-Case Blocking Checks

- block validation use if `point_in_time_quality != POINT_IN_TIME_VALIDATED`
- block peer-relative transforms if peer groups are below minimum size
- block sector-relative alpha research if metadata is static snapshot
- block production/routing usage for all research-only metadata

## 8. Required Diagnostic Reports Before Alpha Research

Before any economically anchored alpha batch, produce these reports:

1. Universe sector distribution
2. Universe industry distribution
3. Peer group size distribution
4. Size bucket distribution
5. Liquidity bucket distribution
6. Volatility bucket distribution
7. Sector x size cross-tab
8. Sector x liquidity cross-tab
9. Sector x volatility cross-tab
10. Size x liquidity overlap
11. Dynamic active-universe metadata coverage by date/window
12. Inventory candidate coverage by sector
13. Inventory candidate coverage by size
14. Inventory candidate coverage by liquidity bucket
15. Inventory candidate co-activation by sector/size/liquidity
16. Thin peer-group warning report
17. Source lineage and static-snapshot warning report
18. Metadata readiness dashboard

These reports are descriptive until point-in-time approval exists.

## 9. Diagnostic Notebook Plan

Suggested future notebooks or notebook-equivalent reports:

`notebooks/economic_context_metadata_readiness_v1.ipynb`

- coverage and missingness
- sector/industry/peer group distribution
- source lineage summary
- static-snapshot warnings

`notebooks/economic_context_inventory_exposure_v1.ipynb`

- current inventory exposure by sector, size, liquidity, and volatility bucket
- candidate active coverage by economic context
- co-activation by economic context
- no sector-conditioned IC claims unless point-in-time safe

`notebooks/economic_context_peer_group_readiness_v1.ipynb`

- peer group sizes by date
- fallback rates
- thin groups
- group turnover
- minimum group-size readiness

`notebooks/economic_context_behavior_bucket_diagnostics_v1.ipynb`

- liquidity/volatility/turnover/beta bucket stability
- bucket drift
- size overlap
- sector overlap

Notebook outputs should be exportable to artifacts under:

`artifacts/research/economic_context_enrichment_v1/`

## 10. Implementation Order

### Phase 0: Design Lock

- finalize this design
- confirm allowed and blocked uses
- keep all alpha research blocked

### Phase 1: Static Diagnostic Consolidation

- use existing static metadata only for descriptive diagnostics
- produce coverage, lineage, and inventory exposure reports
- preserve `STATIC_SNAPSHOT_RESEARCH_ONLY`

### Phase 2: Point-In-Time Source Evaluation

- identify candidate sector/industry/size sources
- inspect licensing, coverage, effective dates, and update cadence
- do not ingest into validation until source lineage is proven

### Phase 3: SQLite Metadata Layer

- implement current/history classification and size tables
- implement source audit and coverage diagnostics tables
- store source hashes and run manifests

### Phase 4: Behavioral Bucket Layer

- implement date-aware liquidity, volatility, turnover, residual-vol, and beta buckets
- enforce lookback-only construction
- persist bucket diagnostics

### Phase 5: Peer Group Builder

- implement industry-first peer groups with sector fallback
- enforce minimum group size
- store fallback and thinness diagnostics

### Phase 6: Inventory Exposure Diagnostics

- describe current inventory exposures by sector/size/liquidity/volatility
- evaluate whether inventory concentration risks are economically clustered
- do not use diagnostics for candidate status changes

### Phase 7: Future Alpha Batch Design

Only after readiness checks:

- design a small metadata-enriched alpha batch
- focus on peer-relative repair/stabilization asymmetry
- keep raw h10/h20 IC as validation anchor
- keep recovery-quality targets as sidecars

## 11. What This Phase Should Implement Now

If implementation is approved later, the immediate work should be limited to:

- metadata loaders and validators
- source-lineage/audit utilities
- descriptive diagnostics
- SQLite current/history persistence for metadata only
- readiness dashboard

It should not implement alpha candidates.

## 12. What Remains Diagnostic Only

Until point-in-time quality is established:

- static sector/industry labels
- static market-cap/size buckets
- descriptive inventory exposure by metadata
- peer-group thinness diagnostics
- sector/industry distribution dashboards
- recovery-quality target sidecar interpretation

## 13. What Waits For True Point-In-Time Data

Blocked until point-in-time safe:

- sector-relative ranks
- industry-relative z-scores
- peer-relative residual alphas
- size-neutral alpha claims
- sector-conditioned IC conclusions
- validation based on metadata slices
- production use
- portfolio/ML/blending/optimization routing

## 14. Risks And Safeguards

### Risk: Static Snapshot Leakage

Safeguard:

- label all static outputs `STATIC_SNAPSHOT_RESEARCH_ONLY`
- block validation and historical claims

### Risk: Interaction Explosion

Safeguard:

- allow only small hypothesis-led candidate batches
- require component decomposition and baseline overlap diagnostics

### Risk: Peer Group Thinness

Safeguard:

- enforce minimum active group sizes
- use sector fallback
- report fallback rate and inactive groups

### Risk: Size/Liquidity Confounding

Safeguard:

- report size x liquidity overlap
- require size and liquidity controls before interpreting repair effects

### Risk: Sector Concentration

Safeguard:

- report sector concentration and one-sector dominance
- compare candidate activity with universe distribution

### Risk: Source Lineage Ambiguity

Safeguard:

- require source version, collection timestamp, file hash, and source notes
- block use if source audit is incomplete

### Risk: Target Drift

Safeguard:

- raw h10/h20 IC remains validation anchor
- recovery/post-stress targets remain diagnostic sidecars

### Risk: Premature ML Or Portfolio Use

Safeguard:

- no routing into ML, portfolio, blending, optimization, or production
- context metadata is a research input only until separately governed

## 15. Definition Of Done

Economic Context Enrichment v1 is complete when:

- required metadata fields are defined and documented
- current/history table schemas are approved
- source lineage and audit requirements are explicit
- point-in-time versus static-snapshot usage boundaries are encoded in design
- data quality checks are specified
- diagnostic report list is defined
- module structure is proposed
- implementation order is clear
- alpha research remains blocked until readiness conditions are met

Readiness for future alpha discovery requires an additional decision:

`ECONOMIC_CONTEXT_READY_FOR_RESEARCH_BATCH`

That decision should require:

- sufficient metadata coverage
- point-in-time or explicitly approved exploratory metadata status
- peer group size adequacy
- source lineage audit pass
- inventory exposure diagnostics
- raw h10/h20 validation anchor preserved
- recovery-quality sidecars clearly labeled diagnostic-only

## 16. Future First Alpha Batch, After Readiness

The first economically enriched batch should be small, likely 4-6 candidates, and should test:

- peer-relative repair persistence
- sector-relative stabilization asymmetry
- size-controlled volatility compression
- liquidity repair relative to comparable names
- participation asymmetry relative to peer norms
- downside containment during hostile regimes

Each future candidate should include:

- raw h10/h20 IC
- WFV persistence/sign consistency
- sector/peer/size coverage
- low-volatility overlap
- reversal/momentum overlap
- liquidity duplication check
- one-window dominance
- crisis concentration
- interaction decomposition if applicable
- recovery-quality sidecar diagnostics only

No candidate should be promoted directly from enriched diagnostics without the existing validation discipline.

## 17. Intentional Non-Changes

This design does not:

- implement ML
- implement alpha candidates
- create runners
- create SQLite tables
- fetch external data
- change validation anchors
- change WFV logic
- change gates or thresholds
- change candidate statuses
- promote any signal
- modify production logic
- redesign governance
- use recovery-quality targets as validation targets
- touch detector files
- route anything into portfolio, ML, blending, or optimization
