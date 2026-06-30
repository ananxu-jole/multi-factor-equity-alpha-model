# Project Underdog - Point-in-Time Economic Metadata Implementation Readiness Patch v1

Date: 2026-06-20

Scope: planning/design patch only. No code implementation, schema creation, data ingestion, metadata mutation, discovery, validation, governance mutation, threshold change, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Prior review classification: `IMPLEMENTATION READY WITH CHANGES`.

The source-gate architecture review found the point-in-time economic metadata architecture sound, but required several pre-implementation changes before a research-only implementation task should begin.

Required changes incorporated by this patch:

1. Explicit source acceptance manifest.
2. Derived `pit_economic_context_panel`.
3. Taxonomy-version tracking.
4. Security event lineage support.
5. Fallback dominance reporting.
6. Stale-age distribution diagnostics.
7. Blocked/eligible ticker-date diagnostics.

Implementation remains justified after this patch. The changes reduce ambiguity, make the MVP more fail-closed, and clarify what future discovery runners may consume. They do not authorize implementation or discovery.

Updated conclusion:

The architecture is now ready to be converted into a precise implementation specification. Implementation should still remain blocked until a separate implementation task is approved and until an acceptable point-in-time or date-stamped historical source passes the source gate.

## SECTION 2 - Required Architecture Changes

| required change | what changes | why needed | MVP or deferred | implementation implication | downstream discovery impact |
| --- | --- | --- | --- | --- | --- |
| Source acceptance manifest | Add a formal manifest recording source-gate scores, pass/fail status, source class, lineage completeness, and allowed use. | Prevents weak or static sources from silently entering PIT infrastructure. | MVP, required before implementation start. | Implementation spec must define manifest fields and require source acceptance before ingestion. | Discovery remains blocked unless manifest certifies `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` quality. |
| Derived `pit_economic_context_panel` | Add an explicit date/ticker context output built from source history, ticker lineage, and peer reconstruction. | Future discovery runners need one certified context surface rather than joining raw tables ad hoc. | MVP, required during implementation. | Implementation spec must include output schema and fail-closed eligibility fields. | Enables later discovery design to consume PIT context safely. |
| Taxonomy-version tracking | Add taxonomy/source classification version fields to sector/industry history. | Separates vendor taxonomy changes from true company classification changes. | MVP when source provides taxonomy version; otherwise tracked as missing. | Add fields such as `taxonomy_version` and `classification_provider_taxonomy_id`. | Reduces false classification drift and peer migration errors. |
| Security event lineage support | Add event lineage or event-link fields for ticker changes, mergers, spin-offs, delistings, share-class changes, and successor/predecessor relationships where available. | Security identity is the highest-risk join layer. | MVP as supported-by-source; unresolved events must be blocked. | Add event fields or linked event table to implementation spec. | Prevents historical signal rows from mapping to the wrong current ticker/security. |
| Fallback dominance reporting | Add explicit fallback-level share, broad-fallback share, and fallback dominance reports by date/window. | Peer-relative discovery may be PIT-safe but economically weak if fallback dominates. | MVP diagnostic. | Coverage diagnostics must include fallback distribution and dominance summaries. | Discovery can be blocked when peer groups are too coarse. |
| Stale-age distribution diagnostics | Add stale-age percentiles and stale-record distribution, not only stale counts. | A few stale records and a systemically stale source have different risk profiles. | MVP diagnostic. | Diagnostics must report min/median/p90/max stale age where applicable. | Discovery readiness can assess whether source freshness is adequate. |
| Blocked/eligible ticker-date diagnostics | Add counts and shares of eligible and blocked ticker-date observations with reasons. | Discovery readiness depends on usable historical observations, not just ticker coverage. | MVP diagnostic. | Coverage diagnostics must report blocked and eligible ticker-date counts by reason. | Future discovery batches can size the valid research universe before panel generation. |

## SECTION 3 - Updated MVP Scope

Required before implementation:

- Source-gate rubric finalized.
- Source acceptance manifest fields finalized.
- Required schemas and derived output schemas finalized.
- Blocking criteria finalized.
- Implementation task explicitly scoped as research-only.
- No data source accepted without documented point-in-time or date-stamped historical quality.

Required during implementation:

- `security_master_pit`
- `ticker_lineage_pit`
- `sector_industry_history_pit`
- `peer_group_history_pit`
- `metadata_source_lineage`
- `pit_metadata_coverage_diagnostics`
- source acceptance manifest
- derived `pit_economic_context_panel`
- taxonomy-version fields where available
- security event lineage support where available
- fallback dominance diagnostics
- stale-age distribution diagnostics
- blocked/eligible ticker-date diagnostics
- readiness manifest with fail-closed discovery eligibility

Recommended during implementation if source-ready:

- `size_bucket_history_pit`
- historical market-cap or date-safe size buckets
- subindustry fields
- point-in-time inventory exposure audit using the derived context panel

Deferred:

- options
- fixed income
- macro data
- alternative data
- full fundamentals
- production integration
- portfolio/blending/optimization routing
- ML use
- peer-relative candidate formulas
- discovery runners
- sector-conditioned validation methodology
- multi-vendor master reconciliation beyond the accepted MVP source

Updated MVP interpretation:

The MVP must prove that Project Underdog can produce a date-safe, source-certified, fail-closed context panel. It does not need to prove a peer-relative alpha signal.

## SECTION 4 - Updated Schema Requirements

### Source Acceptance Manifest

Purpose:

Record whether a candidate source is accepted, rejected, or diagnostic-only before ingestion.

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

Required status values:

- `ACCEPTED_FOR_PIT_IMPLEMENTATION`
- `DIAGNOSTIC_ONLY`
- `REJECTED`
- `NEEDS_MANUAL_REVIEW`

### Taxonomy Version Fields

Add to `sector_industry_history_pit` where available:

- `taxonomy_version`
- `classification_provider_taxonomy_id`
- `taxonomy_effective_date`
- `taxonomy_change_flag`
- `taxonomy_change_reason`

Requirement:

If taxonomy version is unavailable, the implementation must set a missing taxonomy flag rather than silently assuming stability.

### Security Event Lineage

Add either fields in `security_master_pit` or a linked event artifact/table.

Minimum event fields:

- `security_event_id`
- `security_id`
- `event_type`
- `event_effective_date`
- `event_as_of_date`
- `predecessor_security_id`
- `successor_security_id`
- `prior_ticker`
- `next_ticker`
- `source`
- `source_version`
- `event_confidence`
- `event_notes`

Expected event types:

- `ticker_change`
- `share_class_change`
- `merger`
- `spin_off`
- `delisting`
- `listing_change`
- `identifier_change`
- `unknown_or_unresolved`

Requirement:

Unresolved event lineage must create blocked ticker-date diagnostics, not silent joins.

### Derived `pit_economic_context_panel`

Purpose:

Provide the single research-facing date/ticker economic-context output for future discovery design.

Minimum fields:

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

Requirement:

Future discovery design may reference this panel, not raw static metadata. If `discovery_eligible` is false, the ticker-date is blocked from peer-relative discovery.

### Fallback, Stale, and Blocked Diagnostics

Add or require diagnostics with these fields:

Fallback dominance:

- `diagnostic_start_date`
- `diagnostic_end_date`
- `fallback_level`
- `ticker_date_count`
- `ticker_date_share`
- `broad_fallback_share`
- `dominant_fallback_level`
- `fallback_dominance_flag`

Stale-age distribution:

- `diagnostic_start_date`
- `diagnostic_end_date`
- `stale_age_min`
- `stale_age_median`
- `stale_age_p75`
- `stale_age_p90`
- `stale_age_max`
- `stale_record_count`
- `stale_record_share`

Blocked/eligible ticker-date diagnostics:

- `diagnostic_start_date`
- `diagnostic_end_date`
- `total_ticker_dates`
- `eligible_ticker_dates`
- `blocked_ticker_dates`
- `eligible_ticker_date_share`
- `blocked_ticker_date_share`
- `blocked_reason`
- `blocked_reason_count`
- `blocked_reason_share`

## SECTION 5 - Updated Readiness Gates

`IMPLEMENTATION START`

Requirements:

- Source-gate rubric finalized.
- Source acceptance manifest schema finalized.
- Implementation spec includes all seven review-required changes.
- No unresolved decision about whether size history is mandatory.
- Implementation task remains research-only and non-production.

`IMPLEMENTATION COMPLETE`

Requirements:

- Schemas or artifacts are created under approved research paths.
- Source acceptance manifest is written.
- PIT history tables or artifacts are populated only from accepted source(s).
- Derived `pit_economic_context_panel` is produced.
- Fail-closed eligibility fields are present.
- No discovery, validation, governance, production, or ML paths are touched.

`DIAGNOSTIC READY`

Requirements:

- Date-level coverage diagnostics are produced.
- Fallback dominance diagnostics are produced.
- Stale-age distribution diagnostics are produced.
- Blocked/eligible ticker-date diagnostics are produced.
- Security/ticker unresolved cases are reported.
- Static metadata remains separated and cannot be used to fill historical dates.

`DISCOVERY DESIGN READY`

Requirements:

- PIT diagnostics are reviewed.
- Eligible ticker-date coverage is sufficient for design planning.
- Peer fallback does not dominate the usable universe or is explicitly scoped.
- Discovery remains design-only; no panels or IC scoring are generated.

`POINT_IN_TIME_DISCOVERY_READY`

Requirements:

- Post-implementation readiness review confirms source, lineage, coverage, fallback, stale-age, and blocked/eligible diagnostics.
- `pit_economic_context_panel` certifies usable ticker-date rows with `discovery_eligible = true`.
- Future discovery runners can fail closed from metadata manifests.
- A separate discovery design task is approved.

## SECTION 6 - Remaining Risks

Data availability:

The largest remaining risk is that no available source can satisfy the point-in-time source gate for the required lookback period.

Lineage ambiguity:

Ticker changes, share classes, mergers, spin-offs, and delistings may remain unresolved even if classification data exists.

Stale records:

Periodic snapshots may leave long stale intervals. The stale-age distribution diagnostics reduce this risk but do not eliminate it.

Peer fallback dominance:

Even PIT-safe peer groups may be economically weak if most ticker-dates rely on sector or broad fallback rather than industry peers.

Taxonomy drift:

Vendor taxonomy revisions can create apparent classification changes that are not company-level economic changes.

Security identity mismatch:

Incorrect security identifiers can contaminate every downstream table. This remains the highest-integrity implementation risk.

Scope creep:

There is still a risk of overbuilding toward fundamentals, production routing, or ML. Those must remain deferred.

## SECTION 7 - Final Recommendation

1. Are the review-required changes incorporated?

Yes. This patch incorporates the explicit source acceptance manifest, derived `pit_economic_context_panel`, taxonomy-version tracking, security event lineage support, fallback dominance reporting, stale-age distribution diagnostics, and blocked/eligible ticker-date diagnostics.

2. Is the architecture now ready for implementation?

Yes, for a research-only implementation specification. Actual implementation should begin only after a separate task translates this patch into precise files, paths, commands, artifacts, and tests. No data ingestion or schema creation is authorized by this note.

3. What is the first implementation task?

The first implementation task should be a research-only scaffold that creates schema definitions, source-gate manifest structure, diagnostic artifact layout, and fail-closed validation checks without ingesting external data or enabling discovery.

4. What must still be blocked?

Peer-relative discovery, candidate panel generation, IC scoring, validation, governance mutation, threshold changes, production registration, ML, portfolio routing, and candidate promotion/demotion must remain blocked.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Implementation Specification v1**. It should remain planning/design-only and should define exact implementation files, research artifact paths, schemas, manifest fields, diagnostics, dry-run behavior, tests, and guardrails. It should not implement code, create schemas, ingest data, modify metadata, run discovery, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This patch updates the implementation plan only. Current economic-context metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY`, and no point-in-time infrastructure has been built or authorized for discovery use.
