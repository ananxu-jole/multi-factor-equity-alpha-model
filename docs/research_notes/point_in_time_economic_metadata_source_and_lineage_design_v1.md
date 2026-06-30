# Project Underdog - Point-in-Time Economic Metadata Source and Lineage Design v1

## SECTION 1 - Architecture Overview

This note designs the point-in-time economic metadata architecture required before Project Underdog can safely run peer-relative or economic-context alpha research.

Classification: `DESIGN_READY_WITH_EXTERNAL_DATA_DEPENDENCIES`.

The architecture is ready to guide a research-only implementation phase, but implementation cannot produce discovery-ready metadata unless an acceptable external or historical source is identified, licensed or otherwise approved for research use, and accepted through a source gate.

Core principle:

Security and issuer identity must be authoritative before economic classifications, size context, peer groups, or candidate panels can be trusted. Sector, industry, peer, and size metadata must never be backfilled from current static snapshots into historical signal dates.

This design supports future peer-relative repair and stabilization asymmetry research while preserving strict point-in-time correctness. It does not implement ingestion, create databases, generate panels, compute IC, validate candidates, modify governance, register production outputs, change thresholds, or introduce ML.

## SECTION 2 - Materials Reviewed

Reviewed CRSP/security-master and lineage notes:

- `docs/research_notes/security_master_and_ticker_lineage_pit_design_review_v1.md`
- `docs/research_notes/security_master_and_ticker_lineage_pit_implementation_readiness_review_v1.md`
- `docs/research_notes/point_in_time_economic_metadata_source_gate_and_schema_plan_v1.md`
- `docs/research_notes/point_in_time_economic_metadata_source_gate_review_v1.md`

Reviewed economic-context notes:

- `docs/research_notes/economic_context_enrichment_design_v1.md`
- `docs/research_notes/economic_context_enrichment_v1_implementation.md`
- `docs/research_notes/metadata_source_lineage_consistency_review_v1.md`
- `docs/research_notes/point_in_time_economic_context_readiness_audit_v1.md`

Reviewed alpha-frontier and governance context:

- `docs/research_notes/main_alpha_inventory_consolidation_and_non_crsp_frontier_selection_v1.md`
- `docs/research_notes/peer_relative_repair_stabilization_asymmetry_discovery_program_design_v1.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`

## SECTION 3 - Source Hierarchy

Authoritative source priority should be separated by domain. No single source should be treated as authoritative for every metadata type unless it passes every domain-specific gate.

| domain | primary authority | secondary authority | diagnostic-only source | fail-closed condition |
| --- | --- | --- | --- | --- |
| Security master | Accepted PIT security-master source with stable security identifiers and effective windows | Exchange/listing history source with reproducible ticker windows | Current ticker universe | Missing stable identity or unresolved active window |
| Issuer identifiers | Accepted issuer/security source with issuer id, security id, and share-class mapping | Vendor/entity mapping source with dated snapshots | Company name matching | Ambiguous issuer/security relation |
| Ticker lineage | Accepted dated ticker history with exchange/namespace and prior/next ticker links | Security-master event file | Current ticker symbols | Recycled ticker or overlapping ticker windows |
| Listing dates | Accepted listing history from security master or exchange source | Dated vendor snapshots | Current listing flag | Missing listing start for historical use |
| Delisting | Accepted delisting/event source | Security-master inactive windows | Current inactive flag | Missing delisting date where security disappears |
| Corporate actions | Accepted event lineage source for ticker changes, mergers, spin-offs, split-offs, acquisitions, share-class changes, and relistings | Security-master predecessor/successor mapping | Manual notes | Unresolved event or low event confidence |
| Sector | Accepted PIT classification source with effective dates or dated snapshots | Accepted vendor taxonomy snapshots | Static sector seed | Static-only classification |
| Industry | Accepted PIT classification source with effective dates or dated snapshots | Accepted vendor taxonomy snapshots | Static industry seed | Missing industry history |
| Subindustry | Accepted PIT classification source when coverage is sufficient | Vendor taxonomy snapshots | Static subindustry labels | Missing/unstable subindustry; fallback to industry if allowed |
| Peer group | Derived from accepted PIT classification, active universe, size context if available, and peer hierarchy rules | Accepted vendor peer group history if reproducible | Static peer labels | Group below minimum size or stale classification |
| Market capitalization | Accepted historical market-cap source with as-of dates | Reconstructed from PIT price and shares outstanding if lineage-safe | Static market-cap bucket | Missing date-safe market cap when size-aware grouping is required |
| Size bucket | Derived from accepted historical market cap using frozen bucket rules | Accepted dated size classification | Static size bucket | Missing date-safe size when size-aware fallback is required |
| Economic classifications | Accepted PIT taxonomy source, versioned and effective-dated | Date-stamped snapshots with inference policy | Manual static labels | Unknown taxonomy version or future-dated label |

Source priority rule:

If authorities disagree, the source with stronger PIT evidence wins only after disagreement is logged. If disagreement cannot be resolved, the affected ticker-date is blocked from discovery eligibility rather than filled by convenience.

## SECTION 4 - Source Acceptance Gate

Before any source can populate PIT metadata tables, it must pass a source gate.

Required source-gate evidence:

- source name and provider;
- source version or snapshot identifier;
- source file path, controlled reference, or archived raw extract;
- source hash and row counts;
- source collection timestamp;
- licensing and research-use notes;
- coverage by research date range;
- stable identifiers or explicit mapping fields;
- effective dates or snapshot dates;
- taxonomy version for classification sources;
- normalization rules;
- missing-field report;
- source-gate status and rejection reasons where applicable.

Accepted source statuses:

- `ACCEPTED_FOR_PIT_IMPLEMENTATION`
- `CONDITIONAL_ACCEPTED_WITH_BLOCKING_RULES`
- `DIAGNOSTIC_ONLY`
- `MANUAL_REVIEW_REQUIRED`
- `REJECTED`
- `DEPRECATED`

Discovery-eligible source statuses:

- `ACCEPTED_FOR_PIT_IMPLEMENTATION`
- `CONDITIONAL_ACCEPTED_WITH_BLOCKING_RULES`, only for ticker-dates not affected by the condition.

All other source statuses are blocked from discovery.

## SECTION 5 - Point-in-Time Rules

Effective dating:

- Each historical metadata row must have `effective_start`.
- Each row must have `effective_end`, or an explicit open-ended value for current records.
- Rows are valid for a signal date only when `effective_start <= signal_date < effective_end`.
- If a source provides dated snapshots rather than effective windows, inferred windows must be explicitly marked `inferred_window` and confidence must be reduced.

As-of dating:

- No metadata row can be used unless `as_of_date <= signal_date`.
- If `as_of_date` is later than the signal date, the row is future information and must be blocked.
- `collection_timestamp` is required for reproducibility but does not replace `as_of_date`.

Historical lookup behavior:

- Lookups must join by stable `security_id` first, not ticker text alone.
- Ticker-to-security mapping must be resolved as of the signal date.
- Classification and size metadata must be looked up after identity resolution.
- Peer groups must be constructed from active, eligible securities as of the signal date.

Late-arriving corrections:

- Corrections are appended as new metadata versions, not destructive edits.
- Corrected rows must retain original source lineage and correction lineage.
- If a correction changes historical metadata, downstream artifacts must record the metadata version used.
- Existing research artifacts should not be silently reinterpreted under newer metadata.

Missing metadata handling:

- Missing mandatory identity data blocks ticker-date eligibility.
- Missing sector or industry blocks peer-relative discovery for that ticker-date.
- Missing size blocks only size-aware grouping; non-size peer hierarchy may proceed if otherwise eligible.
- Missing optional subindustry triggers fallback to industry.
- Missing values must be explicit and reported, not silently imputed.

Confidence hierarchy:

- `point_in_time_verified`: usable for discovery after coverage review.
- `date_stamped_snapshot`: usable only under approved inferred-window rules.
- `inferred_window`: conditionally usable with confidence downgrade and diagnostics.
- `static_snapshot_only`: diagnostic only, blocked from discovery.
- `unresolved`: blocked.
- `blocked`: blocked.

Minimum confidence floors:

- identity confidence: 0.70
- ticker mapping confidence: 0.70
- classification confidence: 0.70
- event confidence for event-dependent continuity: 0.70
- peer assignment confidence: derived from source confidence and fallback level; blocked if below implementation floor.

## SECTION 6 - Lineage Architecture

Security lineage:

- `security_id` is the canonical identity key for historical joins.
- Security records carry activity windows, listing status, exchange, share class, predecessor/successor identifiers, and event lineage.
- A ticker-date must resolve to one and only one eligible `security_id` unless explicit share-class rules allow multiple mappings.

Issuer lineage:

- `issuer_id` groups securities belonging to the same issuer where source evidence supports it.
- Issuer lineage must handle mergers, acquisitions, spin-offs, split-offs, and company name changes.
- Issuer continuity cannot be inferred from name similarity alone.

Ticker lineage:

- Ticker mappings are effective-dated and exchange/namespace-aware.
- Ticker reuse creates separate security identities unless source evidence proves continuity.
- Same ticker on different exchanges must not be silently merged.
- Prior/next ticker links are diagnostic aids, not substitutes for effective windows.

Metadata lineage:

- Every classification, size, market-cap, and peer row carries source, version, run id, metadata version, collection timestamp, record hash, PIT quality, confidence, and manual override flag.
- Derived peer-group rows must link back to input classification and universe versions.
- Manual overrides must be bounded, reviewed, versioned, and prevented from dominating discovery coverage.

Source lineage:

- Raw source or controlled references must be retained.
- Source hashes and normalized row hashes must be recorded.
- Normalization rules must be reproducible.
- Source-gate scoring and pass/fail reasons must be archived with each metadata version.

## SECTION 7 - Metadata Schema Proposal

The schema below is a proposal only. This task does not create tables.

### `security_master_pit`

Purpose: canonical security identity and activity windows.

Required fields:

- `security_id`
- `issuer_id`
- `company_name`
- `security_type`
- `share_class`
- `exchange`
- `ticker_namespace`
- `country`
- `currency`
- `primary_listing_flag`
- `is_active`
- `listing_date`
- `delisting_date`
- `effective_start`
- `effective_end`
- `as_of_date`
- `event_type`
- `event_effective_date`
- `event_as_of_date`
- `predecessor_security_id`
- `successor_security_id`
- `identity_confidence`
- `event_confidence`
- `point_in_time_quality`
- `manual_override_flag`
- `source`
- `source_version`
- `source_record_id`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `blocked_reason`
- `notes`

### `ticker_lineage_pit`

Purpose: dated ticker-to-security mapping.

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
- `ticker_mapping_confidence`
- `point_in_time_quality`
- `manual_override_flag`
- `source`
- `source_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `blocked_reason`

### `economic_classification_history_pit`

Purpose: dated sector, industry, subindustry, and taxonomy history.

Required fields:

- `security_id`
- `ticker_at_source`
- `sector`
- `industry`
- `subindustry`
- `classification_system`
- `taxonomy_version`
- `classification_provider_taxonomy_id`
- `classification_level`
- `effective_start`
- `effective_end`
- `as_of_date`
- `source_snapshot_date`
- `classification_confidence`
- `point_in_time_quality`
- `stale_metadata_flag`
- `manual_override_flag`
- `source`
- `source_version`
- `source_record_id`
- `metadata_version`
- `universe_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `raw_record_hash`
- `blocked_reason`
- `notes`

### `market_cap_size_history_pit`

Purpose: historical size and market-cap context.

Required fields:

- `security_id`
- `market_cap`
- `market_cap_currency`
- `market_cap_as_of_date`
- `shares_outstanding`
- `price_source`
- `market_cap_source`
- `market_cap_bucket`
- `size_bucket`
- `bucket_rule_version`
- `effective_start`
- `effective_end`
- `as_of_date`
- `size_confidence`
- `point_in_time_quality`
- `manual_override_flag`
- `source`
- `source_version`
- `metadata_version`
- `run_id`
- `collection_timestamp`
- `record_hash`
- `blocked_reason`

### `peer_group_history_pit`

Purpose: derived date-level peer group assignment.

Required fields:

- `signal_date`
- `security_id`
- `ticker`
- `peer_group_label`
- `peer_group_level`
- `peer_group_method`
- `peer_group_size`
- `peer_group_min_size`
- `fallback_level`
- `fallback_distance`
- `peer_quality_status`
- `peer_assignment_confidence`
- `input_classification_version`
- `input_size_version`
- `input_universe_version`
- `construction_rule_version`
- `point_in_time_quality`
- `discovery_eligible`
- `blocked_reason`
- `run_id`
- `collection_timestamp`
- `record_hash`

### `pit_economic_context_panel`

Purpose: fail-closed, date-level research context consumed by future candidate runners.

Required fields:

- `signal_date`
- `security_id`
- `ticker`
- `sector`
- `industry`
- `subindustry`
- `market_cap_bucket`
- `size_bucket`
- `peer_group_label`
- `peer_group_level`
- `peer_group_size`
- `fallback_level`
- `fallback_distance`
- `peer_quality_status`
- `point_in_time_quality`
- `metadata_version`
- `universe_version`
- `discovery_eligible`
- `blocked_reason`
- `stale_metadata_flag`
- `manual_override_flag`

### `metadata_source_lineage`

Purpose: source reproducibility and audit trail.

Required fields:

- `source`
- `source_version`
- `source_reference`
- `source_hash`
- `raw_row_count`
- `clean_row_count`
- `rejected_row_count`
- `collection_timestamp`
- `normalization_rules_hash`
- `source_gate_status`
- `source_gate_score_summary`
- `license_or_usage_notes`
- `metadata_version`
- `run_id`
- `record_hash`

### `pit_metadata_coverage_diagnostics`

Purpose: readiness and coverage audit.

Required fields:

- `metadata_version`
- `date_start`
- `date_end`
- `active_security_count`
- `eligible_security_count`
- `blocked_security_count`
- `eligible_ticker_date_count`
- `blocked_ticker_date_count`
- `sector_coverage_ratio`
- `industry_coverage_ratio`
- `peer_group_coverage_ratio`
- `size_coverage_ratio`
- `fallback_distribution`
- `stale_record_count`
- `manual_override_share`
- `low_confidence_count`
- `run_id`
- `created_at`

## SECTION 8 - Peer Hierarchy

Peer groups are derived, not source authority. They should be constructed from accepted PIT classifications, active universe membership, and optional PIT size context.

Authoritative hierarchy:

1. `subindustry`
   - Highest economic specificity.
   - Use only if coverage and active peer count are sufficient.

2. `industry`
   - Default preferred MVP peer grouping.
   - Requires active peer count above the minimum threshold.

3. `industry x size`
   - Use when industry is broad and PIT size history is available.
   - Block if size history is not PIT safe.

4. `sector x size`
   - Medium-confidence fallback only.
   - Block if size history is not PIT safe.

5. `sector`
   - Broad fallback for diagnostics and limited discovery only if explicitly approved.

6. `broad size`
   - Diagnostic fallback, not preferred for alpha discovery.

7. `blocked`
   - Required if no level meets quality, count, and PIT requirements.

Confidence rules:

- Peer-group size is measured on active eligible securities as of `signal_date`.
- Minimum peer count should default to the existing diagnostic threshold of 8 until a separate implementation note changes it.
- Fallback distance must be recorded.
- High-confidence peers require PIT industry or subindustry assignment.
- Sector-only and broad-size peers should never be interpreted as true economic peers without explicit caveats.
- Fallback dominance must be reported before discovery can proceed.

## SECTION 9 - Economic-Context Framework

Future peer-relative research needs metadata for:

- peer-relative comparisons;
- industry-relative signals;
- sector-relative signals;
- cross-peer dispersion;
- economic conditioning;
- universe-relative baseline comparisons;
- contamination review against existing repair and rank families.

Minimum context package for future discovery:

- date-safe `security_id`;
- signal-date ticker mapping;
- sector and industry as of signal date;
- derived peer group as of signal date;
- active peer group size;
- PIT quality label;
- discovery eligibility flag;
- blocked reason;
- metadata version;
- source lineage version.

Recommended context package:

- subindustry where available;
- PIT market cap and size bucket;
- fallback distance;
- peer assignment confidence;
- stale metadata flag;
- manual override flag;
- date-derived liquidity and volatility buckets built only from pre-signal OHLCV history.

Blocked until this framework exists:

- peer-relative alpha candidates;
- industry-relative z-scores;
- sector-neutral residuals;
- sector-conditioned IC;
- peer-conditioned validation;
- context-aware ML.

## SECTION 10 - Governance Requirements

Audit requirements:

- source acceptance manifest for every source;
- source lineage manifest for every metadata version;
- date-level coverage diagnostics;
- blocked ticker-date report;
- unresolved identity report;
- recycled ticker report;
- classification-change report;
- taxonomy-version change report;
- stale-age distribution;
- fallback dominance report;
- manual override dominance report;
- discovery eligibility manifest.

Reproducibility requirements:

- raw source hashes;
- normalized source hashes;
- record hashes;
- immutable metadata versions;
- run manifests;
- normalization rule versions;
- peer construction rule versions;
- source gate status history.

Validation requirements:

- No candidate validation may use metadata unless the metadata version is certified discovery eligible and validation-use eligible.
- Discovery eligibility does not imply validation eligibility.
- Validation review must explicitly cite metadata version, source versions, PIT quality distribution, blocked-date handling, and fallback distribution.

Versioning requirements:

- Metadata versions are append-only.
- Corrections create new versions.
- Candidate artifacts must record the metadata version used.
- Research notes must not reinterpret older results under newer metadata without a rerun and review.

Metadata freeze rules:

- Each candidate discovery run uses a frozen metadata version.
- Source changes after the freeze do not affect existing artifacts.
- Frozen versions must include source gate status and discovery eligibility flags.

Change management:

- Source upgrades require a source-gate review.
- Taxonomy changes require old/new mapping diagnostics.
- Manual overrides require reason, reviewer, expiration/review date, and dominance diagnostics.
- Any change that alters discovery eligibility must trigger a readiness review.

## SECTION 11 - Implementation Phases

Phase 1: Source inventory and acceptance design.

- Identify candidate sources for security identity, ticker lineage, classifications, size, market cap, listing/delisting, and corporate actions.
- Produce source-gate scoring and licensing/reproducibility review.
- No ingestion.

Phase 2: Source-gate scaffold.

- Implement manifests, controlled vocabularies, schema validation, and dry-run checks only.
- No PIT table build.
- No classification or peer reconstruction.

Phase 3: Security and ticker lineage scaffold.

- Build research-only identity/ticker schemas and diagnostics after a source passes gate.
- Produce blocked/eligible ticker-date diagnostics.
- Do not build economic classifications yet.

Phase 4: Economic classification history scaffold.

- Add PIT sector/industry/subindustry history.
- Add taxonomy-version diagnostics and stale-record reporting.

Phase 5: Size and market-cap history scaffold.

- Add PIT market-cap and size buckets if a source passes gate.
- Disable size-aware peer fallback until this phase passes audit.

Phase 6: Peer reconstruction and context panel.

- Derive `peer_group_history_pit` and `pit_economic_context_panel`.
- Produce fallback, peer-size, and discovery-eligibility diagnostics.

Phase 7: Readiness audit.

- Review whether the context panel can support candidate specification.
- Only after this gate may peer-relative candidate specification proceed.

## SECTION 12 - Assumptions

- Current static metadata remains diagnostic-only.
- CRSP/PIT work should not be reopened without source evidence or an approved source-gate task.
- Security identity and ticker lineage are prerequisites for every downstream metadata layer.
- Industry is the minimum economically meaningful peer grouping for first-pass peer-relative research.
- Size-aware fallback is valuable but optional until PIT market-cap history is available.
- Raw h10/h20 forward-return IC remains the validation anchor for future candidate research.
- Recovery-quality targets remain diagnostic sidecars.
- ML remains out of scope.

## SECTION 13 - Risks

PIT leakage risks:

- current classifications applied to past dates;
- vendor taxonomy updates treated as historical truth;
- snapshot dates inferred too aggressively;
- `collection_timestamp` mistaken for historical availability.

Survivorship risks:

- current universe excludes delisted or merged names;
- current metadata omits historical constituents;
- inactive securities lack classification history.

Ticker reuse risks:

- a ticker reused by a different company maps to the wrong security;
- same ticker across exchanges or share classes is merged incorrectly;
- old signal rows join to current ticker identity.

Stale metadata risks:

- old sector/industry records remain open too long;
- inferred windows create false stability;
- stale peer group membership contaminates peer-relative ranks.

Vendor disagreement risks:

- classification systems disagree;
- taxonomy versions change;
- sector/industry labels shift without economic changes;
- market-cap sources differ due to shares outstanding definitions.

Licensing assumptions:

- source retention, redistribution, and derived artifact rights must be reviewed;
- source hashes and raw file retention must be allowed for reproducibility;
- manually reviewed sources must not become hidden vendor-derived data without lineage.

Operational risks:

- manual overrides become too dominant;
- fallback peer groups create false precision;
- unresolved identities are silently dropped instead of reported;
- discovery runners ignore metadata eligibility flags.

## SECTION 14 - Explicit Non-Goals

This design does not:

- ingest metadata;
- build databases;
- modify CRSP implementation;
- implement pipelines;
- generate candidate panels;
- compute IC;
- run redundancy screening;
- run refinement;
- run validation;
- modify production registry;
- modify governance thresholds;
- introduce ML;
- change existing candidate status;
- authorize peer-relative discovery;
- authorize static metadata for alpha use.

## SECTION 15 - Readiness Classification

Classification: `DESIGN_READY_WITH_EXTERNAL_DATA_DEPENDENCIES`.

Rationale:

- The architecture is sufficiently specified for a controlled implementation plan.
- Source hierarchy, PIT rules, lineage model, peer hierarchy, schema proposals, governance requirements, and phased implementation are defined.
- The design depends on external or historically archived data that has not yet been accepted.
- Without an accepted source for security identity, ticker lineage, sector/industry history, and ideally market-cap history, the project cannot reach discovery readiness.

Recommended next implementation phase:

The next implementation phase should be **Security Master and Ticker Lineage PIT Source Gate Scaffold v1** or an equivalent source-gate scaffold. It should implement only controlled vocabularies, manifest validation, source-gate scoring, dry-run/list/validate modes, and tests. It should not ingest data, build lineage, reconstruct sector/industry history, reconstruct peers, generate panels, run discovery, run validation, mutate governance, register production outputs, change thresholds, or introduce ML.
