# Project Underdog - Security Master and Ticker Lineage PIT Implementation Design v1

## SECTION 1 - Executive Summary

Security identity comes first because every future point-in-time economic-context artifact depends on correctly answering one question: which historical economic entity did a ticker represent on a given signal date? If that answer is unstable, sector history, industry history, peer groups, context panels, and future discovery panels all inherit identity leakage.

Ticker lineage comes first because Project Underdog's historical signal panels are ticker/date oriented. A ticker can change, disappear, move exchanges, represent a different issuer later, or be reused. Without point-in-time ticker lineage, historical observations can be joined to current identity and contaminate every downstream context-aware research step.

This phase should accomplish only the identity foundation:

- Define accepted source requirements for security identity and ticker lineage.
- Build future design requirements for `security_master_pit`, `ticker_lineage_pit`, `source_acceptance_manifest`, and `metadata_source_lineage`.
- Define continuity rules for ticker, name, exchange, delisting, merger, spin-off, and recycled-ticker events.
- Define schema-level and record-level validation expectations.
- Define blocked/eligible ticker-date diagnostics that downstream sector, industry, and peer reconstruction must obey.

Explicitly out of scope:

- sector history
- industry history
- size history
- peer reconstruction
- economic-context panel construction
- alpha discovery
- refinement
- validation
- governance mutation
- threshold changes
- production use
- ML

## SECTION 2 - Scope Definition

Included:

- `security_master_pit`
- `ticker_lineage_pit`
- `source_acceptance_manifest` for identity/lineage sources
- `metadata_source_lineage`
- lineage diagnostics
- ticker/security continuity diagnostics
- stale/missing diagnostics
- blocked/eligible ticker-date diagnostics for identity readiness

Excluded:

- `sector_industry_history_pit`
- `size_bucket_history_pit`
- `peer_group_history_pit`
- `pit_economic_context_panel`
- sector, industry, size, or peer reconstruction
- candidate generation
- alpha discovery
- IC scoring
- refinement
- validation
- governance or production integration

MVP phase boundary:

The output of this phase should be a research-only identity and ticker-lineage layer that can support a later sector/industry source integration task. It should not certify Project Underdog as `POINT_IN_TIME_DISCOVERY_READY`.

## SECTION 3 - Source Requirements

Security identifiers:

- Must provide stable security identifiers or enough auditable fields to construct `security_id`.
- Should provide issuer identifiers where available.
- Must distinguish share classes where applicable.
- Must support active/inactive windows or enough status history to infer them.
- Must provide identity confidence or enough evidence to assign confidence.

Ticker history:

- Must provide ticker, exchange/listing venue, ticker namespace, and ticker validity windows.
- Must represent ticker changes, prior ticker, next ticker, and ticker status where available.
- Must identify primary listing status where available.
- Must distinguish recycled tickers and ticker reuse.

Name history:

- Recommended but not blocking if stable identifiers and ticker lineage are strong.
- If available, name changes should be represented as identity lineage events or dated attributes.
- Missing name history should reduce confidence only when it prevents identity continuity.

Exchange history:

- Strongly recommended.
- Exchange/listing changes must be dated where available.
- Same ticker on different exchanges must not be treated as the same identity without explicit linkage.

Effective dates:

- Required: `effective_start` for security identity windows.
- Required: `ticker_effective_start` for ticker lineage windows.
- Required where available: `effective_end` and `ticker_effective_end`.
- If only snapshots are available, inferred windows must be marked as inferred and confidence-adjusted.

Source timestamps:

- Source snapshot date or known-as-of date is mandatory.
- Collection timestamp, source version, source file hash, and metadata version are mandatory for auditability.

Lineage confidence:

- Every row should carry confidence fields: `identity_confidence`, `ticker_mapping_confidence`, `event_confidence`, and `point_in_time_quality` where applicable.
- Manual overrides must be explicitly flagged.

Source reproducibility:

- Raw source file or controlled source reference must be retained.
- Normalization rules, record hashes, raw/clean row counts, and source-gate score summary must be recorded.

No source is selected by this design.

## SECTION 4 - Schema Finalization

### 1. `security_master_pit`

Mandatory fields:

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
- `security_event_id`
- `event_type`
- `event_effective_date`
- `event_as_of_date`
- `predecessor_security_id`
- `successor_security_id`
- `prior_ticker`
- `next_ticker`
- `event_confidence`
- `notes`

Optional fields:

- None in the aligned scaffold template. If a source lacks a field, future implementation should populate explicit null/unknown values and lower confidence or block affected rows as appropriate.

Primary key logic:

- Conceptual key: `security_id`, `effective_start`, `source`, `metadata_version`.
- Event lineage should be uniquely identifiable by `security_event_id` where available.

Effective-date logic:

- `effective_start` defines the start of a security identity window.
- `effective_end` defines the end of a window or open-ended current state.
- `as_of_date` must be less than or equal to any downstream signal date using the record.
- Event effective dates and event as-of dates must be kept separate.

Confidence fields:

- `identity_confidence`
- `event_confidence`
- `point_in_time_quality`
- `manual_override_flag`

Lineage fields:

- `source`
- `source_version`
- `source_record_id`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- predecessor/successor fields
- prior/next ticker fields

Validation fields:

- `is_active`
- `manual_override_flag`
- `point_in_time_quality`
- `event_type`

### 2. `ticker_lineage_pit`

Mandatory fields:

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

Optional fields:

- None in the aligned scaffold template. Missing source values must be represented explicitly and must affect confidence or blocking.

Primary key logic:

- Conceptual key: `security_id`, `ticker`, `exchange`, `ticker_effective_start`.
- Same ticker may map to different securities across non-overlapping windows.
- Same ticker may map to multiple securities only when exchange/share-class fields make the mapping unambiguous.

Effective-date logic:

- `ticker_effective_start` is mandatory.
- `ticker_effective_end` must be populated, inferred, or explicitly open-ended.
- `as_of_date` must not be after the downstream signal date using the mapping.

Confidence fields:

- `ticker_mapping_confidence`
- `point_in_time_quality`
- `manual_override_flag`

Lineage fields:

- `source`
- `source_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `prior_ticker`
- `next_ticker`

Validation fields:

- `ticker_status`
- `primary_listing_flag`
- `manual_override_flag`
- `point_in_time_quality`

### 3. `source_acceptance_manifest`

Mandatory fields:

- `source_gate_run_id`
- `source`
- `source_type`
- `source_version`
- `source_snapshot_date`
- `source_file_hash`
- all source-gate score fields
- `source_gate_status`
- `allowed_use`
- `rejection_reason`
- `manual_review_required`
- `license_or_usage_notes`
- `review_timestamp`
- `reviewer_notes`

Primary key logic:

- `source_gate_run_id`, `source`, `source_version`.

Acceptance logic:

- Identity/lineage sources must not proceed unless status is accepted for PIT implementation or explicitly diagnostic-only for non-build review.
- Rejected sources must not be ingested.

### 4. `metadata_source_lineage`

Mandatory fields:

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

Primary key logic:

- `source_lineage_id`.

Lineage logic:

- Every generated identity/ticker row must link back to an accepted source lineage record or be blocked from downstream use.

## SECTION 5 - Identity Continuity Rules

Ticker changes:

- Represent as a dated event with `prior_ticker`, `next_ticker`, event effective date, event as-of date, and linked ticker windows.
- Old ticker window must end before or on the new ticker window start unless source explicitly documents overlap.

Name changes:

- Represent as a security identity event or dated attribute.
- Name changes alone should not create a new `security_id` unless source identity indicates a new economic entity.

Exchange changes:

- Represent as event lineage and ticker lineage change.
- Same ticker on a new exchange must not silently inherit prior exchange mapping without an event or continuity record.

Delistings:

- End active security and ticker windows.
- Preserve historical mapping for past dates.
- Future dates after delisting should be blocked unless successor lineage exists.

Mergers:

- End predecessor security windows.
- Link predecessor and successor security ids where available.
- Block ambiguous historical rows if merger effective date or successor mapping is unresolved.

Spin-offs:

- Represent predecessor and successor/new security ids.
- Do not assume child entity inherits parent ticker/sector/industry context.
- Block affected rows until event lineage is explicit.

Recycled tickers:

- Treat as separate security identities with non-overlapping ticker windows.
- Same ticker reused by a different entity must receive a distinct `security_id`.
- Any overlap in ticker windows without clear exchange/share-class separation should block downstream use.

Missing history:

- Represent missing event or lineage fields explicitly.
- Reduce confidence and block downstream rows when missingness affects identity continuity.
- Do not fill missing history from current static labels.

## SECTION 6 - Validation and Diagnostics

Required checks:

- No overlapping ticker windows for the same `security_id`, ticker, exchange, and namespace unless explicitly permitted by share-class logic.
- No missing `effective_start` for security records.
- No missing `ticker_effective_start` for ticker records.
- No future-dated `as_of_date` relative to downstream signal dates.
- Ticker continuity: each ticker/date/exchange maps to one eligible security unless share-class logic explicitly permits more.
- Security continuity: active security windows do not overlap or conflict for the same `security_id`.
- Duplicate active security records are detected and blocked.
- Ambiguous ticker mappings are detected and blocked.
- Recycled ticker cases are flagged and separated by security id.
- Stale record age is computed from source snapshot/as-of date.
- Blocked and eligible ticker-date status is produced with reason codes.

Required diagnostics:

- source acceptance summary
- source lineage summary
- security identity coverage by date/window
- ticker lineage coverage by date/window
- unresolved ticker/security report
- duplicate active record report
- overlapping window report
- future-dated record report
- stale-age distribution
- manual override report
- blocked/eligible ticker-date report

No alpha validation is implied by these checks. They are metadata integrity diagnostics only.

## SECTION 7 - Blocking Criteria

Block downstream sector/industry/peer reconstruction when:

- ticker identity is unresolved for a ticker-date
- ticker maps to multiple active securities without unambiguous share-class/exchange resolution
- security identity has overlapping active windows
- ticker lineage has overlapping windows that cannot be explained
- `effective_start` or `ticker_effective_start` is missing
- `as_of_date` or source snapshot date is after the signal date
- source lineage is missing or not accepted
- source is `STATIC_SNAPSHOT` or diagnostic-only for historical use
- identity confidence or ticker mapping confidence is below accepted source-gate floor
- event lineage is unresolved for mergers, spin-offs, delistings, ticker changes, or recycled tickers
- stale records exceed the accepted stale-age policy
- manual override dominates a date/window or cannot be reproduced

Blocked rows must remain visible in diagnostics. They must not be silently dropped if that would hide coverage weakness.

## SECTION 8 - Artifact and Runner Expectations

Expected future runner:

- `pipelines/run_security_master_ticker_lineage_pit_v1.py`

Expected modes:

- `--dry-run`: validate configuration, schemas, source-gate inputs, and planned artifacts without data construction.
- `--validate-inputs`: check accepted source manifests, source files/references, hashes, schemas, date fields, and required columns.
- `--build-lineage`: construct research-only `security_master_pit`, `ticker_lineage_pit`, and `metadata_source_lineage` artifacts from accepted sources.
- `--validate-lineage`: run continuity, duplicate, stale, blocked/eligible, and lineage diagnostics.

Expected artifact root:

- `artifacts/research/security_master_ticker_lineage_pit_v1/`

Expected artifact groups:

- `source_gate/`
- `schemas/`
- `lineage/`
- `diagnostics/`
- `manifests/`
- `readiness_review/`

Expected outputs:

- `source_acceptance_manifest.csv`
- `metadata_source_lineage.csv`
- `security_master_pit.csv`
- `ticker_lineage_pit.csv`
- `security_identity_diagnostics.csv`
- `ticker_lineage_diagnostics.csv`
- `overlapping_window_diagnostics.csv`
- `ambiguous_mapping_diagnostics.csv`
- `stale_age_diagnostics.csv`
- `blocked_eligible_ticker_date_diagnostics.csv`
- `manifest.json`

This section is design-only. No runner or artifacts should be created by this task.

## SECTION 9 - Test Plan

Future implementation tests should cover:

- schema conformance for `security_master_pit`, `ticker_lineage_pit`, `source_acceptance_manifest`, and `metadata_source_lineage`
- source-gate rejection of static snapshots for historical use
- required effective-date fields
- no overlapping ticker windows for the same security
- duplicate active security detection
- ambiguous ticker-to-security mapping detection
- recycled ticker separation
- missing date blocking
- future-dated record blocking
- stale-age diagnostic creation
- manual override flag propagation
- blocked/eligible ticker-date diagnostics
- dry-run does not build lineage
- validate-inputs does not construct metadata
- build-lineage writes only research artifact paths
- no discovery, refinement, validation, governance mutation, threshold change, production registration, ML, or alpha candidate creation

No test should require sector, industry, size, peer-group, alpha, validation, or production artifacts.

## SECTION 10 - Final Recommendation

1. Is this first implementation phase sufficiently narrow?

Yes. Limiting the first phase to security master and ticker lineage is the correct minimum foundation. It prevents Project Underdog from building sector, industry, peer, or context-aware discovery on unstable identity joins.

2. What is the minimum source requirement?

The minimum source requirement is a reproducible, date-stamped or effective-dated identity source that can support stable security ids, ticker history, exchange/listing context, source timestamps, source hashes, and confidence/lineage diagnostics. A ticker-only static source is insufficient.

3. What should block implementation?

Implementation should be blocked if no source can pass the identity/ticker source gate, if effective or snapshot dates are missing, if source lineage cannot be reproduced, if ticker/security mappings are ambiguous, or if the proposed task expands into sector/industry reconstruction, peer reconstruction, discovery, validation, governance, production, or ML.

4. What should remain deferred?

Defer sector history, industry history, size history, peer reconstruction, economic-context panel construction, alpha discovery, refinement, validation, governance actions, production routing, options, fixed income, macro, alternative data, and ML.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Security Master and Ticker Lineage PIT Source Gate Implementation v1**. It should implement source-gate evaluation and manifest handling for identity/ticker sources only, with dry-run and input validation support. It should not ingest data into PIT tables, build lineage artifacts, reconstruct sector or industry history, reconstruct peer groups, run discovery, run refinement, run validation, mutate governance, change thresholds, register production outputs, implement ML, or create alpha candidates.
