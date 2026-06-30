# Project Underdog - Point-in-Time Economic Metadata Implementation Specification v1

Date: 2026-06-20

Scope: implementation specification only. No code implementation, schema creation, data ingestion, metadata mutation, discovery, refinement, validation, governance mutation, threshold change, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Implementation objective:

Define the minimum viable point-in-time economic metadata infrastructure required to move Project Underdog from `STATIC_SNAPSHOT_RESEARCH_ONLY` diagnostics toward a future `POINT_IN_TIME_DISCOVERY_READY` state for peer-relative and economic-context alpha-family research.

MVP definition:

The MVP is a research-only point-in-time metadata layer that can produce a fail-closed, date/ticker `pit_economic_context_panel` from accepted source metadata, stable security identity, ticker lineage, sector/industry history, peer reconstruction, source lineage, and coverage diagnostics.

Readiness status:

The architecture is `IMPLEMENTATION READY WITH CHANGES`, and those changes have been incorporated into this specification. Implementation may be scoped from this document, but discovery remains blocked until a separate implementation, diagnostics audit, and readiness review prove point-in-time quality.

Implementation boundaries:

- Build research-only metadata infrastructure.
- Do not generate alpha candidates.
- Do not run discovery, refinement, or validation.
- Do not mutate governance, thresholds, production paths, ML, or candidate status.

## SECTION 2 - Deliverable Inventory

| deliverable | purpose | required status | dependencies |
| --- | --- | --- | --- |
| `source_acceptance_manifest` | Records source-gate scoring, accepted/rejected/diagnostic-only status, allowed use, and pass/fail rationale. | Required before ingestion or construction. | Source-gate rubric and candidate source metadata. |
| `security_master_pit` | Stores stable security identity windows for historical joins. | Required MVP. | Accepted source with security identifiers or reconstructable identity fields. |
| `ticker_lineage_pit` | Maps tickers to securities over time. | Required MVP. | `security_master_pit`, ticker history source. |
| `sector_industry_history_pit` | Stores sector/industry classification history with PIT lineage. | Required MVP. | Accepted classification source and security/ticker mapping. |
| `size_bucket_history_pit` | Stores date-safe size/market-cap bucket history. | Recommended, not blocking if size-aware fallback is disabled. | PIT market-cap or size source. |
| `peer_group_history_pit` | Stores derived peer assignments by signal date and peer construction method. | Required MVP. | `sector_industry_history_pit`, ticker/security lineage, active universe dates. |
| `metadata_source_lineage` | Stores source references, hashes, versions, timestamps, and usage notes. | Required MVP. | Raw source archive or controlled source references. |
| `pit_metadata_coverage_diagnostics` | Stores date/window coverage, fallback, stale, and blocked/eligible diagnostics. | Required MVP. | All PIT history outputs and active universe membership. |
| `pit_economic_context_panel` | Research-facing date/ticker context panel with discovery eligibility flags. | Required MVP. | Classification history, ticker lineage, peer reconstruction, diagnostics. |
| `readiness_manifest` | Declares whether artifacts are diagnostic-only, discovery-design-ready, or PIT discovery ready. | Required MVP. | All diagnostics and source manifest. |

## SECTION 3 - Canonical Schema Specification

### `source_acceptance_manifest`

Key:

- `source_gate_run_id`
- `source`
- `source_version`

Required fields:

- `source_gate_run_id`
- `source`
- `source_type`
- `source_version`
- `source_snapshot_date`
- `source_file_hash`
- `pit_integrity_score`
- `coverage_score`
- `historical_depth_score`
- `identifier_quality_score`
- `update_feasibility_score`
- `source_stability_score`
- `implementation_complexity_score`
- `cost_manual_burden_score`
- `leakage_risk_score`
- `source_gate_status`
- `allowed_use`
- `rejection_reason`
- `manual_review_required`
- `license_or_usage_notes`
- `review_timestamp`
- `reviewer_notes`

Validation fields:

- `source_gate_status`
- `allowed_use`
- `manual_review_required`
- `rejection_reason`

### `security_master_pit`

Key:

- `security_id`
- `effective_start`
- `source`
- `metadata_version`

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
- `identity_confidence`
- `manual_override_flag`
- `point_in_time_quality`
- `notes`

Security event lineage fields, or linked event artifact:

- `security_event_id`
- `event_type`
- `event_effective_date`
- `event_as_of_date`
- `predecessor_security_id`
- `successor_security_id`
- `prior_ticker`
- `next_ticker`
- `event_confidence`

### `ticker_lineage_pit`

Key:

- `security_id`
- `ticker`
- `exchange`
- `ticker_effective_start`

Required fields:

- `security_id`
- `ticker`
- `exchange`
- `ticker_namespace`
- `share_class`
- `primary_listing_flag`
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
- `ticker_mapping_confidence`
- `manual_override_flag`
- `point_in_time_quality`

### `sector_industry_history_pit`

Key:

- `security_id`
- `classification_system`
- `effective_start`
- `metadata_version`

Required fields:

- `security_id`
- `ticker_at_source`
- `sector`
- `industry`
- `subindustry`
- `classification_system`
- `classification_level`
- `taxonomy_version`
- `classification_provider_taxonomy_id`
- `taxonomy_effective_date`
- `taxonomy_change_flag`
- `taxonomy_change_reason`
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
- `classification_confidence`
- `manual_override_flag`
- `point_in_time_quality`
- `stale_metadata_flag`
- `notes`

### `size_bucket_history_pit`

Key:

- `security_id`
- `effective_start`
- `metadata_version`

Required fields if implemented:

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
- `size_confidence`
- `point_in_time_quality`
- `stale_metadata_flag`
- `manual_override_flag`

MVP rule:

If no accepted PIT size source exists, this deliverable is not required and size-aware fallback must be disabled.

### `peer_group_history_pit`

Key:

- `signal_date`
- `security_id`
- `peer_group_method`
- `metadata_version`

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
- `input_classification_version`
- `input_universe_version`
- `construction_rule_version`
- `source_metadata_version`
- `metadata_version`
- `run_id`
- `created_at`
- `peer_confidence_score`
- `point_in_time_quality`
- `fallback_quality_status`

### `metadata_source_lineage`

Key:

- `source_lineage_id`

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
- `source_confidence`
- `point_in_time_quality`
- `manual_source_flag`
- `source_gate_score_summary`
- `notes`

### `pit_metadata_coverage_diagnostics`

Key:

- `run_id`
- `metadata_version`
- `diagnostic_scope`
- `diagnostic_start_date`
- `diagnostic_end_date`

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
- `fallback_dominance_flag`
- `stale_record_count`
- `stale_record_share`
- `stale_age_min`
- `stale_age_median`
- `stale_age_p75`
- `stale_age_p90`
- `stale_age_max`
- `unresolved_ticker_count`
- `duplicate_active_record_count`
- `eligible_ticker_date_count`
- `blocked_ticker_date_count`
- `eligible_ticker_date_share`
- `blocked_ticker_date_share`
- `point_in_time_quality`
- `coverage_quality_status`
- `created_at`
- `notes`

### `pit_economic_context_panel`

Key:

- `signal_date`
- `security_id`
- `ticker`
- `metadata_version`

Required fields:

- `signal_date`
- `security_id`
- `ticker`
- `sector`
- `industry`
- `subindustry`
- `size_bucket`
- `peer_group_label`
- `peer_group_level`
- `peer_group_method`
- `peer_group_size`
- `peer_group_min_size`
- `fallback_level`
- `fallback_reason`
- `peer_confidence_score`
- `point_in_time_quality`
- `classification_metadata_version`
- `peer_group_metadata_version`
- `source_gate_run_id`
- `stale_age_days`
- `stale_record_flag`
- `discovery_eligible`
- `blocked_reason`
- `created_at`

## SECTION 4 - Validation and Integrity Framework

Required checks and pass/fail expectations:

| check | pass expectation | fail behavior |
| --- | --- | --- |
| Overlapping effective windows | No overlapping windows for the same `security_id` and metadata domain. | Fail affected records; block ticker-date rows. |
| Missing effective dates | No missing `effective_start` for discovery-eligible PIT records. | Mark source/records diagnostic-only or block. |
| Missing as-of dates | Discovery-eligible records must include `as_of_date` or source snapshot date. | Block discovery eligibility. |
| Future-dated records | No record with `as_of_date > signal_date` may enter the context panel. | Fail closed; block ticker-date rows. |
| Ticker continuity | Historical ticker/date maps to one active `security_id`, except explicit share-class cases. | Block unresolved ticker-date rows. |
| Security continuity | Security identity windows must not conflict. | Block affected rows and report event ambiguity. |
| Static backfill | Static snapshot rows cannot populate historical context. | Hard fail for discovery eligibility. |
| Stale records | Stale age must be computed and flagged. | Exclude records beyond accepted stale policy; report distribution. |
| Fallback dominance | Fallback level shares must be reported by date/window. | Block discovery design if broad fallback dominates usable rows. |
| Peer group size | Peer groups must meet minimum active size or mark row blocked. | Block peer-relative eligibility for affected rows. |
| Blocked/eligible diagnostics | Eligible and blocked ticker-date counts must be reported with reasons. | Readiness cannot be declared without report. |
| Source acceptance | Accepted source manifest must exist and certify allowed use. | No ingestion or PIT implementation approval. |

Pass/fail principle:

The system must fail closed. Missing lineage, missing dates, unresolved identity, excessive fallback, or stale records should reduce eligible ticker-date coverage, not silently fill from static metadata.

## SECTION 5 - Peer Reconstruction Framework

Sector migration:

- Sector changes must be represented as dated classification records.
- The sector used for `signal_date` must be the sector known and effective on that date.
- Sector migration diagnostics must report old sector, new sector, effective date, as-of date, source, and affected date range.

Industry migration:

- Industry changes trigger peer reassignment.
- Industry migration diagnostics must report old industry, new industry, peer group before/after, and active group-size impact.

Size migration:

- If `size_bucket_history_pit` is implemented, size buckets must be date-safe.
- If not implemented, sector x size fallback must be disabled.
- Static size buckets cannot be used for historical peer reconstruction.

Peer reassignment:

- Peer groups must be reconstructed by signal date using active classifications and active universe membership.
- Peer assignments must include method, group level, group size, fallback reason, confidence score, and blocked flag.

Taxonomy versioning:

- Taxonomy version changes must be tracked separately from company classification changes where available.
- Missing taxonomy version should be flagged, not assumed stable.

Expected outputs:

- `peer_group_history_pit`
- `pit_economic_context_panel`
- peer group size report
- peer migration report
- fallback dominance report
- blocked peer-group report

## SECTION 6 - Diagnostic Output Requirements

Required diagnostics:

Coverage reports:

- active ticker coverage by date/window
- dynamic universe coverage by date/window
- sector coverage
- industry coverage
- peer-group coverage

Fallback reports:

- fallback level counts and shares
- broad fallback share
- fallback dominance flag
- fallback reason distribution

Stale-age reports:

- stale record count and share
- stale-age min, median, p75, p90, max
- stale-age distribution by source and classification domain

Blocked ticker-date reports:

- total ticker-dates
- eligible ticker-dates
- blocked ticker-dates
- blocked reason counts and shares
- unresolved ticker/security counts

Lineage diagnostics:

- source lineage report
- source hash report
- taxonomy version report
- security event lineage report
- ticker continuity report
- effective-window overlap report
- future-dated record report

Source acceptance diagnostics:

- source-gate score summary
- source acceptance/rejection status
- allowed-use classification
- licensing/manual-use notes
- manual review flags

Readiness outputs:

- readiness manifest
- `pit_economic_context_panel` eligibility summary
- discovery block/allow summary

## SECTION 7 - Discovery Readiness Gates

`POINT_IN_TIME_DISCOVERY_READY` may be declared only after all conditions below are satisfied:

- Source acceptance manifest certifies an accepted source for PIT implementation.
- `security_master_pit`, `ticker_lineage_pit`, `sector_industry_history_pit`, `peer_group_history_pit`, `metadata_source_lineage`, `pit_metadata_coverage_diagnostics`, and `pit_economic_context_panel` exist as research artifacts or schemas.
- Static metadata is not used to populate historical dates.
- Date-level active coverage diagnostics are complete.
- Unresolved ticker/security cases are reported and blocked.
- Stale-age diagnostics are complete.
- Fallback dominance diagnostics are complete.
- Blocked/eligible ticker-date diagnostics are complete.
- Peer group size checks are complete.
- `pit_economic_context_panel.discovery_eligible` is present and fail-closed.
- Readiness manifest certifies `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` quality.
- A post-implementation readiness audit approves discovery-design consideration.

Discovery remains blocked if any of the above conditions are missing or fail.

## SECTION 8 - Explicit Non-Goals

This specification excludes:

- alpha discovery
- candidate generation
- candidate panel generation
- IC scoring
- refinement
- validation
- governance mutation
- threshold changes
- production routing
- production metadata registration
- options data
- fixed income data
- macro data
- alternative data
- ML
- full fundamentals expansion
- portfolio construction
- blending or optimization
- candidate promotion/demotion

## SECTION 9 - Implementation Sequence

Step 1: source acceptance framework.

- Implement source-gate scoring structure.
- Define and write source acceptance manifest.
- Do not ingest source data until source is accepted.

Step 2: core PIT schemas.

- Define research-only schemas/artifacts for `security_master_pit`, `ticker_lineage_pit`, `sector_industry_history_pit`, `metadata_source_lineage`, and `pit_metadata_coverage_diagnostics`.
- Keep `size_bucket_history_pit` optional unless a PIT size source is accepted.

Step 3: lineage controls.

- Add source lineage, taxonomy version tracking, ticker continuity, security event lineage, record hashes, and raw source references.

Step 4: peer reconstruction.

- Reconstruct `peer_group_history_pit` by signal date from accepted classification history and active universe membership.
- Produce the derived `pit_economic_context_panel`.

Step 5: diagnostics.

- Produce coverage, fallback, stale-age, blocked/eligible ticker-date, lineage, and source acceptance diagnostics.
- Write readiness manifest.

Step 6: readiness audit.

- Conduct post-implementation readiness audit.
- Determine whether `POINT_IN_TIME_DISCOVERY_READY` can be declared.
- Do not run discovery during the audit.

## SECTION 10 - Final Recommendation

1. Is the MVP now fully specified?

Yes. The MVP is fully specified as a research-only PIT metadata layer centered on source acceptance, security/ticker lineage, sector/industry history, peer reconstruction, diagnostics, and a fail-closed `pit_economic_context_panel`.

2. What remains intentionally deferred?

Deferred: size history unless source-ready, subindustry peer groups, full fundamentals, options, fixed income, macro, alternative data, ML, production routing, portfolio construction, sector-conditioned validation, peer-relative candidate formulas, and discovery runners.

3. What is the highest implementation risk?

The highest implementation risk is accepted source availability and identity lineage quality. Without a source that provides date-safe classifications tied to stable security identifiers, the infrastructure cannot become discovery ready.

4. What should block implementation approval?

Implementation approval should be blocked if the source acceptance framework is not finalized, if no source can be evaluated, if the implementation would rely on static current labels for historical dates, or if the task scope includes discovery, validation, governance mutation, production routing, or ML.

5. What should the first coding task be?

The first coding task should be a research-only PIT metadata scaffold and dry-run framework that defines schemas/artifact layouts, source acceptance manifest handling, fail-closed eligibility checks, and diagnostic output stubs without ingesting external data or enabling discovery.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Scaffold Implementation v1**. It should implement only the research-only scaffold, schemas/artifact definitions, manifest writers, dry-run checks, and tests. It should not ingest external data, generate discovery panels, run IC scoring, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This specification freezes the MVP blueprint only. It does not build point-in-time metadata infrastructure and does not authorize discovery. Current economic-context metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY` until implementation and readiness review prove otherwise.
