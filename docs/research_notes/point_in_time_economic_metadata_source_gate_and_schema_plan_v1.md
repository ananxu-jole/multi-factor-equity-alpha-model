# Project Underdog - Point-in-Time Economic Metadata Source Gate and Schema Plan v1

Date: 2026-06-20

Scope: planning only. No code implementation, data ingestion, metadata mutation, discovery, validation, governance mutation, threshold change, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Point-in-time economic metadata is needed because the current economic-context layer is complete only as `STATIC_SNAPSHOT_RESEARCH_ONLY`. Static current-sector, industry, size, and peer labels cannot safely support historical peer-relative alpha discovery because they can leak future business classifications, current size, current peer membership, and survivor-only identity information into past signal dates.

Minimum viable scope:

- security identifier lineage
- ticker lineage
- sector history
- industry history
- date-safe peer-group reconstruction
- source lineage and reproducibility
- date-level coverage diagnostics

Size bucket history is recommended for richer peer grouping, but peer-relative discovery can reach an initial readiness gate if sector and industry history are point-in-time safe and if size-aware fallback is disabled until size history is ready.

Source-gate purpose:

The source gate defines the minimum evidence a metadata source must provide before it can be used in future peer-relative discovery infrastructure. It prevents static snapshots, undocumented manual labels, or weak lineage from being mistaken for point-in-time metadata.

Schema-plan purpose:

The schema plan defines the canonical research-only tables required to store identity lineage, classification history, size history, peer-group history, source lineage, and coverage diagnostics before any future implementation begins.

## SECTION 2 - Minimum Required Data Domains

| domain | readiness class | rationale |
| --- | --- | --- |
| Security identifier lineage | Mandatory | Stable security identity is required to link historical signal panels, ticker changes, corporate actions, mergers, spin-offs, and delistings. |
| Ticker lineage | Mandatory | Historical ticker-to-security mapping is required so old signal rows are not joined to current ticker identity. |
| Sector history | Mandatory | Sector membership must be known as of each signal date for sector-relative diagnostics and fallback groups. |
| Industry history | Mandatory | Industry is the minimum economically meaningful peer grouping for the first peer-relative frontier. |
| Peer-group history | Mandatory | Peer groups must be reconstructed by signal date from active sector/industry records and active universe membership. |
| Source lineage | Mandatory | Every source row must be reproducible, dated, versioned, and auditable. |
| Coverage diagnostics | Mandatory | Discovery readiness depends on date-level active coverage, not only current coverage. |
| Size bucket history | Recommended | Date-safe size improves peer quality and enables sector x size fallback, but initial discovery readiness can proceed without size-aware fallback. |
| Market-cap history | Recommended | Needed for robust size history and size-neutral diagnostics. |
| Subindustry history | Deferred / recommended later | Useful for finer peers after coverage is proven; not required for MVP. |
| Inventory exposure metadata | Recommended | Useful for diagnostic exposure audits after PIT context exists; not required to build the core layer. |
| Behavioral context buckets | Deferred | Date-derived OHLCV buckets can be added later as controls if computed strictly from pre-signal data. |
| Full fundamentals | Deferred | Not needed for the first point-in-time economic-context layer. |

MVP rule:

Do not block the first point-in-time gate on subindustry, full fundamentals, options, fixed income, macro, alternative data, or ML. Do block it on missing sector/industry history, missing identity lineage, or missing source lineage.

## SECTION 3 - Source Gate Requirements

A source may enter the point-in-time metadata layer only if it can satisfy the source gate below.

Required source properties:

| requirement | source-gate expectation |
| --- | --- |
| Effective dates | Must provide `effective_start` and preferably `effective_end`, or provide repeatable date-stamped snapshots from which effective windows can be inferred. |
| Source timestamps | Must provide source snapshot date, source version, collection timestamp, and source file hash or controlled source reference. |
| Historical availability | Must cover the research lookback period needed for candidate discovery, not only the current universe. |
| Security identifiers | Must provide stable identifiers or enough mapping fields to build `security_id` lineage. |
| Ticker identifiers | Must include ticker, exchange/listing venue when available, and date ranges for ticker validity. |
| Coverage rate | Must support date-level active coverage diagnostics against the dynamic research universe. |
| Update process | Must have a repeatable update cadence or explicit static historical archive process. |
| Reproducibility | Must preserve raw source files, hashes, normalization rules, and run manifests. |
| Licensing/manual-use notes | Must document allowed research use, redistribution constraints, and manual-review limitations where relevant. |
| Point-in-time quality label | Must be classifiable as `POINT_IN_TIME` or `DATE_STAMPED_SNAPSHOT` for discovery use. `STATIC_SNAPSHOT` remains diagnostic-only. |

Source rejection conditions:

- only current classifications are available
- source timestamps cannot be recorded
- ticker/security identity cannot be reconciled
- historical source files cannot be reproduced
- licensing or manual-use terms prevent controlled research use
- effective dates or snapshot dates are missing
- coverage cannot be measured by signal date

## SECTION 4 - Candidate Source Evaluation Framework

No source is selected by this plan unless already available in the repo. Existing repo metadata remains static diagnostic metadata and does not pass the point-in-time source gate.

Scoring rubric:

| dimension | score 0 | score 1 | score 2 | score 3 |
| --- | --- | --- | --- | --- |
| PIT integrity | Current snapshot only | Date-stamped snapshots but sparse | Historical snapshots with usable dates | Full effective-date history |
| Coverage | Cannot measure active coverage | Under 80% active coverage | 80-95% active coverage | 95%+ active coverage by date |
| Historical depth | Current only | Partial lookback | Covers most research period | Covers full required research period |
| Identifier quality | Ticker only | Ticker plus exchange | Stable identifier plus ticker history | Stable identifier, ticker history, and corporate-action lineage |
| Update feasibility | Manual one-off only | Manual but repeatable | Periodic controlled files | Automated or vendor-defined repeatable process |
| Source stability | Unstable or ad hoc | Some field instability | Stable files with versioning | Stable taxonomy and versioned releases |
| Implementation complexity | Unknown or high friction | High | Medium | Low to medium |
| Cost / manual burden | Prohibitive | High | Moderate | Low or already available |
| Leakage risk | High | Medium-high | Medium | Low |

Interpretation:

- A source scoring `0` on PIT integrity or identifier quality fails the gate.
- A source scoring below `2` on coverage or historical depth cannot support discovery readiness without a documented limitation and blocked-date policy.
- A source with high leakage risk may be used for diagnostics only, not discovery execution.
- Manual static CSVs can score well on reproducibility but fail PIT integrity unless they contain date-stamped historical snapshots.

Source categories to evaluate in a future task:

- professional point-in-time sector/industry/security-master source
- exchange or security-master identity source plus separate classification history source
- historical date-stamped vendor snapshots
- SEC/company identity data for identifier support only
- current profile APIs for diagnostic coverage only
- manual reviewed CSVs for diagnostics only unless historically snapshotted

## SECTION 5 - Canonical Schema Plan

The schemas below are planning artifacts. They should not be implemented by this task.

### 1. `security_master_pit`

Primary key concept:

- one row per `security_id` and effective identity window

Required fields:

- `security_id`
- `issuer_id`
- `company_name`
- `security_type`
- `exchange`
- `country`
- `currency`
- `is_active`
- `effective_start`
- `effective_end`
- `as_of_date`
- `source`
- `source_version`
- `source_record_id`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `notes`

Date fields:

- `effective_start`
- `effective_end`
- `as_of_date`
- `collection_timestamp`

Lineage fields:

- `source`, `source_version`, `source_record_id`, `metadata_version`, `run_id`, `record_hash`

Confidence fields:

- `identity_confidence`
- `manual_override_flag`
- `point_in_time_quality`

Validation checks:

- no overlapping active windows per `security_id`
- no missing `effective_start`
- no duplicate current rows
- no future `as_of_date` relative to discovery signal dates

### 2. `ticker_lineage_pit`

Primary key concept:

- one row per `security_id`, `ticker`, exchange, and ticker-validity window

Required fields:

- `security_id`
- `ticker`
- `exchange`
- `ticker_effective_start`
- `ticker_effective_end`
- `as_of_date`
- `ticker_status`
- `change_reason`
- `prior_ticker`
- `next_ticker`
- `source`
- `source_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`

Date fields:

- `ticker_effective_start`
- `ticker_effective_end`
- `as_of_date`
- `collection_timestamp`

Lineage fields:

- `source`, `source_version`, `metadata_version`, `run_id`, `record_hash`

Confidence fields:

- `ticker_mapping_confidence`
- `manual_override_flag`
- `point_in_time_quality`

Validation checks:

- no overlapping ticker windows for the same `security_id` on the same exchange
- no ticker mapped to multiple active securities on the same date unless share-class metadata explicitly permits it
- historical signal tickers must map to exactly one active security or be flagged unresolved

### 3. `sector_industry_history_pit`

Primary key concept:

- one row per `security_id`, classification system, and effective classification window

Required fields:

- `security_id`
- `ticker_at_source`
- `sector`
- `industry`
- `subindustry`
- `classification_system`
- `classification_level`
- `effective_start`
- `effective_end`
- `as_of_date`
- `source_snapshot_date`
- `source`
- `source_version`
- `source_record_id`
- `metadata_version`
- `universe_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `raw_record_hash`
- `notes`

Date fields:

- `effective_start`
- `effective_end`
- `as_of_date`
- `source_snapshot_date`
- `collection_timestamp`

Lineage fields:

- `source`, `source_version`, `source_record_id`, `metadata_version`, `run_id`, `record_hash`, `raw_record_hash`

Confidence fields:

- `classification_confidence`
- `manual_override_flag`
- `point_in_time_quality`
- `stale_metadata_flag`

Validation checks:

- no overlapping effective windows per `security_id` and classification system
- no missing sector or industry for mandatory records
- no `as_of_date` after the signal date for any discovery context panel
- classification changes produce old/new diagnostics

### 4. `size_bucket_history_pit`

Primary key concept:

- one row per `security_id` and size-effective window

Required fields:

- `security_id`
- `ticker_at_source`
- `market_cap`
- `market_cap_currency`
- `market_cap_as_of_date`
- `market_cap_source`
- `size_bucket`
- `market_cap_bucket`
- `effective_start`
- `effective_end`
- `as_of_date`
- `source`
- `source_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`

Date fields:

- `market_cap_as_of_date`
- `effective_start`
- `effective_end`
- `as_of_date`
- `collection_timestamp`

Lineage fields:

- `market_cap_source`, `source`, `source_version`, `metadata_version`, `run_id`, `record_hash`

Confidence fields:

- `size_confidence`
- `point_in_time_quality`
- `stale_metadata_flag`
- `manual_override_flag`

Validation checks:

- no static current market cap backfilled into historical dates
- no missing market-cap date when market cap is populated
- size buckets must be computed from date-safe market cap or disabled

### 5. `peer_group_history_pit`

Primary key concept:

- one row per `signal_date`, `security_id`, metadata version, and peer-group method

Required fields:

- `signal_date`
- `security_id`
- `ticker`
- `sector`
- `industry`
- `size_bucket`
- `peer_group_label`
- `peer_group_level`
- `peer_group_method`
- `peer_group_size`
- `peer_group_min_size`
- `fallback_level`
- `fallback_reason`
- `blocked_for_peer_relative`
- `blocked_reason`
- `source_metadata_version`
- `metadata_version`
- `run_id`
- `created_at`

Date fields:

- `signal_date`
- `created_at`

Lineage fields:

- `source_metadata_version`, `metadata_version`, `run_id`

Confidence fields:

- `peer_confidence_score`
- `point_in_time_quality`
- `fallback_quality_status`

Validation checks:

- peer group must be reconstructed from records known on `signal_date`
- minimum peer-group size must be met or candidate date/ticker blocked
- fallback usage must be reported
- broad fallback cannot silently enter peer-relative discovery

### 6. `metadata_source_lineage`

Primary key concept:

- one row per source, source version, source file/reference, and collection run

Required fields:

- `source_lineage_id`
- `run_id`
- `metadata_version`
- `source`
- `source_type`
- `source_version`
- `source_snapshot_date`
- `source_file_path`
- `source_url_or_reference`
- `source_file_hash`
- `record_count_raw`
- `record_count_clean`
- `collection_timestamp`
- `license_or_usage_notes`
- `normalization_rules`
- `created_by`
- `notes`

Date fields:

- `source_snapshot_date`
- `collection_timestamp`

Lineage fields:

- all fields in this table are lineage controls

Confidence fields:

- `source_confidence`
- `point_in_time_quality`
- `manual_source_flag`

Validation checks:

- source hash present for local files
- source version or snapshot date present
- license/manual-use notes present
- record counts reconcile with staging outputs

### 7. `pit_metadata_coverage_diagnostics`

Primary key concept:

- one row per run, metadata version, diagnostic date/window, and coverage scope

Required fields:

- `run_id`
- `metadata_version`
- `universe_version`
- `diagnostic_scope`
- `diagnostic_start_date`
- `diagnostic_end_date`
- `total_active_tickers`
- `covered_active_tickers`
- `missing_active_tickers`
- `coverage_ratio`
- `sector_count`
- `industry_count`
- `peer_group_count`
- `thin_peer_group_count`
- `fallback_usage_rate`
- `broad_fallback_usage_rate`
- `stale_record_count`
- `unresolved_ticker_count`
- `duplicate_active_record_count`
- `point_in_time_quality`
- `created_at`
- `notes`

Date fields:

- `diagnostic_start_date`
- `diagnostic_end_date`
- `created_at`

Lineage fields:

- `run_id`, `metadata_version`, `universe_version`

Confidence fields:

- `coverage_quality_status`
- `point_in_time_quality`

Validation checks:

- coverage computed by date/window, not only current universe
- unresolved tickers reported
- fallback usage reported
- thin groups reported
- stale records reported

## SECTION 6 - Integrity and Validation Rules

Integrity rules:

- No overlapping effective windows for a given `security_id` and metadata domain.
- No missing `effective_start` for point-in-time classification records.
- No missing `as_of_date` for discovery-eligible records.
- No future-dated classifications relative to `signal_date`.
- No static current classification may populate a historical context panel.
- Ticker/security mapping must be one-to-one for a given ticker/date unless explicit share-class rules exist.
- Peer groups must meet minimum active group size or be blocked.
- Stale records must be flagged and excluded if they exceed the allowed stale age.
- Missing coverage must be reported by signal date or window.
- Fallback usage must be reported by level and blocked when too broad for peer-relative use.

Validation outputs required before discovery:

- source lineage report
- effective-window overlap report
- missing effective-date report
- future-dated classification report
- ticker continuity report
- unresolved ticker report
- active coverage by date/window
- peer group size report
- fallback usage report
- stale record report
- readiness manifest

These are metadata integrity checks only. They do not constitute alpha validation.

## SECTION 7 - MVP vs Deferred Scope

MVP scope:

- `security_master_pit`
- `ticker_lineage_pit`
- `sector_industry_history_pit`
- `peer_group_history_pit`
- `metadata_source_lineage`
- `pit_metadata_coverage_diagnostics`
- source gate review
- date-level active coverage diagnostics
- minimum peer-group size checks
- stale-record detection
- fallback usage reporting
- discovery block/allow readiness manifest

Recommended but not blocking for first MVP:

- `size_bucket_history_pit`
- market-cap history
- subindustry fields where source coverage is strong
- inventory exposure audit joined to point-in-time context

Deferred:

- options
- fixed income
- full fundamentals
- macro data
- alternative data
- production integration
- ML use
- portfolio/blending/optimization routing
- sector-conditioned validation methodology
- peer-relative candidate formulas
- discovery runners
- multi-vendor master reconciliation beyond the accepted MVP source

MVP principle:

The MVP should prove that the project can build a date-safe context panel. It should not try to build the entire future economic-data platform in one pass.

## SECTION 8 - Blocking Criteria

Peer-relative discovery should remain blocked if any of the following conditions occur:

- no source passes the source gate
- sector or industry history lacks effective dates or date-stamped snapshots
- source lineage is missing hashes, versions, or collection timestamps
- security identifiers cannot be reconciled to historical signal tickers
- unresolved ticker rate is material and unexplained
- active coverage by date is insufficient or cannot be measured
- peer groups are unstable or dominated by fallback assignments
- minimum peer-group size is not met for the intended discovery universe
- stale-record counts exceed the planned tolerance
- static snapshot rows are required to fill historical dates
- broad sector or size fallback is required for most active names
- licensing or manual-use constraints prevent reproducible research use
- readiness manifest cannot certify `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` quality

Blocking interpretation:

If a blocker is triggered, the project may continue diagnostics and source review, but must not generate peer-relative candidate panels, run IC scoring, run refinement, run validation, modify governance, register production outputs, or route metadata into ML.

## SECTION 9 - Recommended Implementation Sequence

Stage 1: schema scaffold and source gate.

- Finalize schema definitions.
- Define source-gate checklist.
- Compare available source classes using the scoring rubric.
- Produce a source acceptance or rejection note.
- Do not ingest data.

Stage 2: PIT metadata ingestion / construction.

- Only after separate approval, ingest or construct records from an accepted source.
- Write raw source archive, staging outputs, current/history tables, and source lineage artifacts.
- Preserve all raw labels and hashes.

Stage 3: diagnostics and coverage audit.

- Run date-level active coverage diagnostics.
- Produce unresolved ticker, missing classification, stale record, duplicate active record, and effective-window overlap reports.
- Classify readiness by date/window.

Stage 4: peer-group reconstruction.

- Reconstruct peer groups by signal date from active classification records and active universe membership.
- Compute group sizes, fallback levels, confidence scores, and blocked reasons.
- Produce peer-group stability and fallback diagnostics.

Stage 5: discovery readiness review.

- Review all PIT metadata artifacts.
- Decide whether the layer reaches `POINT_IN_TIME_DISCOVERY_READY`.
- If ready, authorize a separate design-only peer-relative discovery program.
- Do not run discovery as part of the readiness review.

## SECTION 10 - Final Recommendation

1. What is the minimum viable source requirement?

The minimum viable source requirement is a reproducible point-in-time or date-stamped historical source for sector and industry classification tied to stable security identifiers and ticker lineage, with source timestamps, effective dates or reconstructable snapshot dates, source versioning, collection timestamps, and date-level coverage measurement.

2. What schemas are required first?

Required first: `security_master_pit`, `ticker_lineage_pit`, `sector_industry_history_pit`, `peer_group_history_pit`, `metadata_source_lineage`, and `pit_metadata_coverage_diagnostics`. `size_bucket_history_pit` is recommended but can be deferred if size-aware fallback is disabled.

3. What should block discovery?

Discovery should be blocked by missing effective dates, missing source lineage, unresolved ticker/security mapping, insufficient active coverage, excessive fallback usage, unstable or thin peer groups, stale records beyond tolerance, or any need to use static current labels for historical dates.

4. What should remain deferred?

Defer options, fixed income, full fundamentals, macro data, alternative data, production integration, ML, portfolio routing, sector-conditioned validation methodology, peer-relative candidate formulas, and discovery runners.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Source Gate Review v1**. It should be review-only and should evaluate available local or proposed metadata sources against the source-gate rubric in this plan. It should not implement schemas, ingest data, modify metadata, run discovery, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This plan does not change the current metadata status. Project Underdog remains on `STATIC_SNAPSHOT_RESEARCH_ONLY` economic-context metadata until a separate source gate, implementation, diagnostics audit, and readiness review establish point-in-time discovery readiness.
