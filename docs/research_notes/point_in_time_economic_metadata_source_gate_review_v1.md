# Project Underdog - Point-in-Time Economic Metadata Source Gate Review v1

Date: 2026-06-20

Scope: review-only architecture audit. No implementation, schema creation, data ingestion, metadata mutation, governance mutation, threshold change, discovery, refinement, validation, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Architecture quality: strong. The proposed point-in-time economic metadata architecture correctly identifies the core blocker: the project does not need more static coverage; it needs date-safe sector, industry, peer, and identity lineage. The source gate, effective-date model, and canonical schemas are directionally sufficient to move from `STATIC_SNAPSHOT_RESEARCH_ONLY` toward `POINT_IN_TIME_DISCOVERY_READY`.

Scope quality: good, with a few needed changes before implementation. The MVP is mostly disciplined: it includes security identity, ticker lineage, sector/industry history, peer-group reconstruction, source lineage, and coverage diagnostics. It appropriately defers options, fixed income, fundamentals, ML, production integration, and candidate discovery. The main scope issue is that the design should make the date-level research context panel and implementation approval checklist more explicit.

Readiness for implementation: not yet fully ready, but close. The architecture should move to implementation only after the changes listed in this review are incorporated into the implementation task specification.

Final classification: `IMPLEMENTATION READY WITH CHANGES`.

Overall recommendation: proceed toward a research-only implementation scaffold after tightening the plan around source acceptance, date-level context-panel outputs, security-master event lineage, and hard discovery-blocking manifests. Do not run discovery or ingest data until a separate implementation task is approved.

## SECTION 2 - Source Gate Review

The proposed source-gate framework is strong and correctly prioritizes point-in-time integrity over convenience.

PIT integrity requirements:

- Sufficient. The plan requires `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` quality for discovery use.
- The rejection of current-only classifications is necessary and should remain hard-blocking.

Effective-date requirements:

- Sufficient, with one clarification needed. The plan requires `effective_start`, preferably `effective_end`, or repeatable snapshots. The implementation spec should require an explicit rule for converting date-stamped snapshots into inferred effective windows.

Lineage requirements:

- Mostly sufficient. Source, version, snapshot date, collection timestamp, source hash, record hashes, and normalization rules are included.
- Missing or underemphasized: lineage should include taxonomy version or classification-system version whenever sector/industry labels come from a vendor taxonomy.

Coverage requirements:

- Sufficient conceptually. The plan requires date-level active coverage rather than current coverage.
- Needed change: define minimum reporting outputs even if thresholds are not governance thresholds, including active coverage by date/window, dynamic universe coverage, unresolved ticker count, and blocked ticker/date count.

Reproducibility requirements:

- Sufficient. Raw source archive, source file hash, normalized staging, and manifests are appropriate.
- Needed change: source acceptance should require a source freeze manifest before any ingestion implementation proceeds.

Leakage protections:

- Strong. The plan blocks static labels, future-dated classifications, broad fallback usage, and missing effective-date data.
- Needed change: explicitly require discovery runners to fail closed if metadata manifests do not certify discovery eligibility.

Are requirements sufficient?

Yes, after minor tightening. The gate is adequate to prevent static metadata from entering discovery.

Are any critical requirements missing?

Two requirements should be added before implementation:

- A source acceptance manifest with source-gate scores and pass/fail reasons.
- A fail-closed discovery eligibility flag that future runners can read from metadata manifests.

Are any requirements unrealistic?

No. The requirements are demanding, but they match the risk. The only potentially difficult requirement is full corporate-action lineage. For MVP, it can be scoped as "sufficient security/ticker lineage for the research universe and lookback window," while unresolved cases remain blocked.

## SECTION 3 - Schema Review

| schema | necessity | completeness | overlap / risk | required changes |
| --- | --- | --- | --- | --- |
| `security_master_pit` | Mandatory | Mostly complete | Could become too broad if it attempts full vendor-grade security master in MVP. | Add event fields or linked event table: `event_type`, `event_effective_date`, `predecessor_security_id`, `successor_security_id` where available. |
| `ticker_lineage_pit` | Mandatory | Strong | Some overlap with `security_master_pit`, but acceptable because ticker lineage is a separate join risk. | Add `share_class`, `primary_listing_flag`, and `ticker_namespace` or equivalent exchange/source namespace if available. |
| `sector_industry_history_pit` | Mandatory | Strong | No major overlap. | Add `taxonomy_version` and `classification_provider_taxonomy_id` if source provides them. |
| `size_bucket_history_pit` | Recommended | Adequate | Correctly optional for MVP if size-aware fallback is disabled. | Keep out of hard MVP unless point-in-time market-cap source is available. |
| `peer_group_history_pit` | Mandatory | Strong as a derived output | Risk of being mistaken for source data. | Mark as derived, include `input_classification_version`, `input_universe_version`, and `construction_rule_version`. |
| `metadata_source_lineage` | Mandatory | Strong | No major overlap. | Add explicit `source_gate_score_summary` or link to source gate artifact. |
| `pit_metadata_coverage_diagnostics` | Mandatory | Strong | Could grow large, but diagnostics are essential. | Add `blocked_ticker_date_count` and `eligible_ticker_date_count`. |

Schema necessity:

All schemas except `size_bucket_history_pit` are required for the first implementation. `size_bucket_history_pit` should remain recommended, not mandatory, unless size-aware peer grouping is explicitly included.

Completeness:

The schemas are complete enough to scaffold. The largest missing piece is an explicit date-level context-panel artifact or schema that future discovery runners will consume.

Overlap with other schemas:

Overlap is manageable. `security_master_pit` and `ticker_lineage_pit` overlap by design but serve different risks. `peer_group_history_pit` overlaps classification fields because it is a derived materialization for research use.

Over-engineering risk:

Moderate. The design should resist turning the MVP into a full enterprise security master. The MVP should cover the research universe, lookback period, and required joins, while unresolved identity cases remain blocked.

Recommended additional schema or artifact:

Add a derived `pit_economic_context_panel` artifact or table for future research use. Minimum fields:

- `signal_date`
- `security_id`
- `ticker`
- `sector`
- `industry`
- `peer_group_label`
- `peer_group_level`
- `peer_group_size`
- `fallback_level`
- `point_in_time_quality`
- `metadata_version`
- `discovery_eligible`
- `blocked_reason`

This can be derived from the existing schemas, but it should be named explicitly in implementation planning.

## SECTION 4 - MVP Scope Review

Mandatory components:

- `security_master_pit`
- `ticker_lineage_pit`
- `sector_industry_history_pit`
- `peer_group_history_pit`
- `metadata_source_lineage`
- `pit_metadata_coverage_diagnostics`
- source gate review
- active coverage diagnostics
- stale-record checks
- fallback usage reporting
- readiness manifest

Recommended components:

- `size_bucket_history_pit`
- market-cap history
- subindustry fields where naturally available
- point-in-time inventory exposure audit after the core layer exists

Deferred components:

- options
- fixed income
- full fundamentals
- macro data
- alternative data
- production integration
- ML use
- portfolio/blending/optimization routing
- peer-relative candidate formulas
- discovery runners
- sector-conditioned validation methodology

Is MVP too large?

Slightly, if `size_bucket_history_pit` is treated as required. It should remain recommended and disabled in peer grouping unless source-ready.

Is MVP too small?

No. The MVP contains the core requirements for `POINT_IN_TIME_DISCOVERY_READY`.

Can scope be simplified further?

Yes. The first implementation can simplify by:

- limiting classification to sector and industry, with subindustry nullable
- disabling size-aware fallback until point-in-time size history exists
- limiting security-master reconstruction to the research universe and lookback period
- treating unresolved ticker/security cases as blocked rather than manually repairing them in MVP

Move into MVP:

- explicit source acceptance manifest
- explicit `pit_economic_context_panel` or equivalent derived context-panel output
- fail-closed discovery eligibility manifest

Move out of MVP:

- required size bucket history
- full corporate-action reconstruction beyond the research universe if a sufficient identity source is not available
- subindustry-based peer groups

## SECTION 5 - Historical Integrity Review

Future-information leakage:

The proposed controls are strong. The plan requires `as_of_date <= signal_date`, effective-window compatibility, static-label blocking, and source lineage in manifests.

Weakness:

The plan should explicitly state that if source snapshots are periodic, the system must not infer knowledge before the snapshot date unless the source provides an earlier effective date and a documented availability rule.

Survivorship bias:

The design recognizes survivorship risk and requires security/ticker lineage.

Weakness:

The MVP should define how unresolved historical tickers are handled: blocked, reported, and excluded from discovery eligibility rather than silently dropped.

Classification drift contamination:

The design handles this well through append-only classification history and old/new diagnostics.

Weakness:

Taxonomy changes should be separated from company reclassification changes. A vendor taxonomy version change can alter labels without an economic company change.

Peer-group contamination:

Controls are strong. Peer groups are reconstructed by signal date with minimum group-size checks and fallback reporting.

Weakness:

Fallback dominance should become an explicit readiness diagnostic. The plan currently blocks "excessive fallback usage" but should require a numeric report even if no governance threshold is set.

Stale metadata usage:

Stale-record flags and maximum staleness diagnostics are included.

Weakness:

The implementation plan should require a stale-age distribution report, not only a stale count.

## SECTION 6 - Discovery Readiness Assessment

Assuming implementation succeeds exactly as designed, the resulting system would be sufficient to support:

- peer-relative discovery: yes, if sector/industry history, identity lineage, and peer reconstruction pass coverage and fallback diagnostics.
- sector-relative discovery: yes, with sector history and date-level active coverage.
- industry-relative discovery: yes, if industry group sizes meet date-level minimums or noneligible date/ticker rows are blocked.
- economic-context-conditioned discovery: yes, for diagnostics and discovery design, provided it remains separate from validation and governance use.

Would discovery still remain blocked?

Discovery would remain blocked if any of the following persist after implementation:

- no accepted source passes the source gate
- security/ticker lineage remains unresolved for a material share of active ticker/date rows
- sector or industry history lacks dates sufficient for the research lookback
- peer fallback dominates the active universe
- future discovery runners cannot consume a certified point-in-time context panel
- the readiness manifest cannot certify `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` quality

If the implementation succeeds and the recommended changes are included, discovery should be unblocked only for a separate design task, not automatically executed.

## SECTION 7 - Implementation Risk Assessment

Ranked implementation risks:

1. Highest-risk data dependency: accepted point-in-time source availability.
   - Without a source that provides date-stamped or effective-dated classifications tied to stable identity, the architecture cannot reach discovery readiness.

2. Highest-risk implementation component: security and ticker lineage.
   - Historical joins fail if ticker changes, share classes, delistings, and corporate actions are not handled or explicitly blocked.

3. Highest-risk integrity issue: static or future classification leakage.
   - A polished schema would not protect the project if current labels are backfilled into historical dates.

4. Highest-risk maintenance burden: source updates and taxonomy drift.
   - Periodic source updates require lineage, diff reports, taxonomy-version tracking, and old/new classification diagnostics.

5. Highest-risk scope risk: overbuilding security-master infrastructure.
   - The MVP should block unresolved edge cases rather than attempting full enterprise-grade identity reconstruction in the first pass.

6. Highest-risk peer risk: fallback dominance.
   - If too many active names require broad fallback groups, peer-relative discovery may be formally point-in-time but economically weak.

## SECTION 8 - Gap Analysis

| gap | severity | review |
| --- | --- | --- |
| Accepted source not yet identified | Critical | The architecture cannot be implemented usefully until a source passes the gate. |
| Explicit derived context-panel schema missing | Critical | Future discovery runners need one certified date/ticker context output. |
| Security-master event details under-specified | Moderate | Add event fields or event-link support for mergers, spin-offs, ticker changes, and delistings where source supports it. |
| Taxonomy-version tracking under-specified | Moderate | Vendor taxonomy changes should be separated from company classification changes. |
| Fallback dominance reporting needs hard artifact | Moderate | The plan mentions fallback rates but should require a standard report. |
| Stale-age distribution missing | Moderate | Stale count alone is not enough for readiness review. |
| Size bucket is recommended but still present as schema | Minor | Fine if disabled until source-ready; avoid treating it as mandatory. |
| Source gate score artifact not explicit | Minor | Add a source-gate score summary artifact for review reproducibility. |

Anything still missing between current design and `POINT_IN_TIME_DISCOVERY_READY`:

- a source that passes the source gate
- implementation of source lineage and history tables
- a certified derived context panel
- date-level diagnostics proving coverage, group size, fallback, stale-record, and unresolved-ticker acceptability
- post-implementation readiness review

## SECTION 9 - Final Readiness Classification

Classification: `IMPLEMENTATION READY WITH CHANGES`.

Detailed rationale:

- The architecture is sound and aligned with Project Underdog's research discipline.
- The source gate correctly blocks static metadata from discovery use.
- The schema set is mostly complete and appropriately research-only.
- The MVP is close to the right size, but implementation should not begin until a few changes are added to the task specification.
- The system can plausibly reach `POINT_IN_TIME_DISCOVERY_READY` if a source passes the gate and the implementation remains fail-closed.

Required changes before implementation:

- Add explicit source acceptance manifest.
- Add explicit derived `pit_economic_context_panel` or equivalent date/ticker context output.
- Add taxonomy-version tracking to classification history where available.
- Add security-master event lineage fields or event-link support where available.
- Require fallback dominance, stale-age distribution, blocked ticker/date, and eligible ticker/date diagnostics.
- Keep `size_bucket_history_pit` recommended, not mandatory, unless a point-in-time size source is accepted.

## SECTION 10 - Final Recommendation

1. Is the architecture sound?

Yes. The architecture is sound and correctly focuses on point-in-time lineage, source reproducibility, identity mapping, peer reconstruction, and date-level diagnostics.

2. Is the MVP appropriately scoped?

Mostly yes. The MVP should be slightly tightened: include an explicit derived context panel and source acceptance manifest, while keeping size history and subindustry peer groups outside the mandatory MVP.

3. What is the biggest remaining weakness?

The biggest remaining weakness is source uncertainty. No point-in-time sector/industry/security-master source has yet been accepted, so the architecture is ready to guide implementation but not yet backed by a known data source.

4. What must be changed before implementation?

Add the source acceptance manifest, explicit `pit_economic_context_panel`, taxonomy-version tracking, security event lineage support, fallback dominance reports, stale-age distribution reports, and blocked/eligible ticker-date diagnostics.

5. Is implementation justified?

Yes, after those changes. Implementation is justified because this is the clearest path to peer-relative and economic-context alpha discovery, which remains the highest-value diversification frontier.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Implementation Specification v1**. It should be planning-only or design-only and should convert the reviewed architecture into a precise implementation specification incorporating the required changes above. It should not implement schemas, ingest data, modify metadata, run discovery, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This review does not authorize implementation or discovery. Current economic-context metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY` until a separate implementation, diagnostics audit, and readiness review demonstrate point-in-time discovery readiness.
