# Project Underdog - Point-in-Time Economic Context Infrastructure Design v1

Date: 2026-06-20

Scope: design-only. No implementation, data ingestion, metadata mutation, governance mutation, threshold change, discovery, refinement, validation, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Current state:

Project Underdog has a strong diagnostic economic-context substrate, but it remains `STATIC_SNAPSHOT_RESEARCH_ONLY`. Diagnostic coverage is complete in the latest enrichment artifacts, with `488 / 488` stock-universe tickers covered, `1.000000` coverage, `0` blocked tickers without metadata, and `27` diagnostically ready peer groups. The current infrastructure can support coverage review, peer-quality diagnostics, fallback analysis, and inventory exposure monitoring. It cannot support peer-relative discovery execution.

Blocker summary:

- Sector and industry labels are static current snapshots.
- Peer groups are fallback-based and not reconstructed by signal date.
- Size and market-cap buckets are static and not safe for historical size-relative research.
- Security-master lineage is missing for ticker changes, corporate actions, delistings, mergers, and spin-offs.
- Effective-date metadata lineage is absent for the populated classification layer.

Design objective:

Design the smallest viable point-in-time infrastructure that can answer, for every signal date and ticker: what sector, industry, size bucket, and peer group would have been known at that time, from which source, with what confidence, and under what stale-data constraints?

Expected research impact:

If implemented later under separate approval, this infrastructure would unlock peer-relative and economic-context alpha-family discovery while preserving Project Underdog's leakage discipline. It would create the first credible path beyond primarily OHLCV-derived transformations into a genuinely new information domain.

## SECTION 2 - Point-in-Time Requirements

| component | discovery readiness priority | point-in-time requirement | rationale |
| --- | --- | --- | --- |
| Sector classification | Mandatory | Historical sector records with `effective_start`, `effective_end`, `as_of_date`, source, and version. | Sector-relative baselines and fallback peer groups require date-safe sector membership. |
| Industry classification | Mandatory | Historical industry records with effective-date lineage and source audit. | Industry is the minimum economically meaningful peer-group layer. |
| Stable security identifier | Mandatory | Identifier mapping across tickers, share classes, corporate actions, mergers, spin-offs, and delistings. | Prevents historical observations from being assigned to the wrong economic entity. |
| Ticker history | Mandatory | Date-safe ticker-to-identifier mapping. | Peer-relative panels must join metadata to historical signal panels safely. |
| Peer assignment | Mandatory | Peer groups reconstructed by signal date using active classifications and active group-size rules. | Peer-relative discovery cannot use static current peer groups. |
| Source lineage | Mandatory | Source name, source version, source timestamp, collection timestamp, file hash or controlled source reference. | Every metadata record must be reproducible and auditable. |
| Effective-date framework | Mandatory | Explicit `effective_start`, `effective_end`, `as_of_date`, `snapshot_date`, and stale-record flags. | This is the core control against future-information leakage. |
| Coverage diagnostics by date | Mandatory | Active universe coverage and dynamic top-300 coverage by date or window. | Discovery readiness depends on historical active coverage, not only current coverage. |
| Size classification | Recommended | Historical market-cap or rolling date-derived size buckets with as-of constraints. | Size controls improve peer quality but are not the first alpha blocker if sector/industry history is available. |
| Market-cap history | Recommended | Date-safe market cap with source and currency lineage. | Required for size-aware peer groups and size-neutral diagnostics. |
| Subindustry classification | Recommended | Historical subindustry records where coverage is adequate. | Useful later, but industry can be the minimum viable peer layer. |
| Inventory exposure metadata | Recommended | Exposure audits joined to point-in-time context, still diagnostic-only. | Helps detect hidden sector/peer concentration in existing candidates. |
| Economic-context metadata | Recommended | Versioned context panels with point-in-time quality flags. | Enables controlled context diagnostics and future design. |
| Behavioral buckets | Optional for initial readiness | Liquidity, volatility, beta, or turnover buckets computed only from pre-signal data. | Useful controls, but not required to lift the static metadata blocker. |
| External fundamentals | Optional | Point-in-time fundamentals only if separately sourced and audited. | Not needed for the first peer-relative discovery frontier. |

Minimum readiness principle:

Sector, industry, peer assignment, source lineage, security identity, and effective-date controls are mandatory. Size and subindustry improve quality but should not delay the first infrastructure gate if core peer history is otherwise credible.

## SECTION 3 - Metadata Source Architecture

The design should separate source categories instead of forcing all metadata through one table.

| metadata category | source type | expected availability | update frequency | historical availability | lineage requirements |
| --- | --- | --- | --- | --- | --- |
| Sector / industry classification | Preferred: point-in-time vendor or security-master classification feed. Secondary: date-stamped frozen snapshots. | Medium, depending on vendor/access. | Monthly, quarterly, or vendor-defined; snapshot cadence must be recorded. | Required. Must include effective dates or reconstructable snapshot dates. | Source, version, source file/hash, as-of date, effective dates, collection timestamp, taxonomy. |
| Subindustry classification | Same as sector/industry, if source supports it. | Lower than sector/industry. | Vendor-defined. | Recommended, not mandatory. | Same as classification lineage, plus coverage and thin-group diagnostics. |
| Ticker / security-master lineage | Preferred: security-master feed or exchange/identifier source with historical mappings. | Medium-high difficulty. | Event-driven or periodic. | Required for robust discovery. | Stable identifier, ticker, exchange, start/end dates, corporate action notes, source audit. |
| Market cap / size | Preferred: point-in-time market-cap feed. Secondary: date-derived market cap from price and shares outstanding if point-in-time shares are available. | Medium difficulty. | Daily, monthly, quarterly, or snapshot-based. | Recommended. | Market cap date, source, currency, split/corporate-action handling, collection timestamp. |
| Peer group | Derived internally from point-in-time classifications and active universe membership. | High once classifications exist. | Recomputed by signal date or metadata snapshot. | Required as derived history. | Peer method, group label, group level, group size, fallback reason, confidence. |
| Inventory exposure metadata | Derived internally from candidate active panels and PIT context panels. | High once context panels exist. | On demand per review. | Diagnostic only. | Candidate id, metadata version, run id, context version, diagnostic-only flag. |
| Behavioral context buckets | Derived internally from OHLCV history. | High. | Rolling/date-derived. | Available if computed only from pre-signal windows. | Formula version, lookback window, signal-date availability, no future data. |

Source model:

1. Raw source archive.
   - Stores immutable source extracts or references, source hashes, collection timestamps, and license/usage notes.

2. Normalized staging layer.
   - Normalizes tickers, identifiers, sectors, industries, market-cap fields, and effective dates without discarding raw source labels.

3. Point-in-time history layer.
   - Appends all effective-date records and all collected snapshots.

4. Current view layer.
   - Exposes latest known record per ticker/security for diagnostics only.

5. Date-level context panel.
   - Materializes or generates signal-date-safe classification, size, and peer assignments for research runners.

No source selection is made by this design. The preferred source class is a professional point-in-time classification/security-master source; static sources remain diagnostic only.

## SECTION 4 - Effective-Date Framework

The point-in-time model must support two temporal concepts:

- when the classification was economically effective
- when Project Underdog or the source knew the classification

Required fields:

| field | purpose |
| --- | --- |
| `security_id` | Stable internal or source identifier across ticker changes. |
| `ticker` | Project ticker as used by signal panels. |
| `exchange` | Listing venue where available. |
| `company_name` | Name associated with the record. |
| `sector` | Broad economic classification. |
| `industry` | Minimum viable peer classification. |
| `subindustry` | Optional finer classification. |
| `classification_system` | GICS, SIC, NAICS, vendor taxonomy, manual taxonomy, or internal mapping. |
| `source` | Source name. |
| `source_version` | Version or release identifier. |
| `source_record_id` | Vendor/source row identifier if available. |
| `source_snapshot_date` | Date the source snapshot represents. |
| `as_of_date` | Date the record is allowed to become known to research. |
| `effective_start` | First date classification is economically effective. |
| `effective_end` | First date classification is no longer effective; null for active records. |
| `collection_timestamp` | Timestamp when Project Underdog collected or froze the source. |
| `metadata_version` | Project metadata version. |
| `universe_version` | Universe version used for coverage diagnostics. |
| `point_in_time_quality` | `POINT_IN_TIME`, `DATE_STAMPED_SNAPSHOT`, `STATIC_SNAPSHOT`, or `UNKNOWN`. |
| `classification_confidence` | Confidence score or class from source/coverage diagnostics. |
| `manual_override_flag` | Whether the row was manually edited or repaired. |
| `stale_metadata_flag` | Whether the row is older than allowed staleness rules. |
| `max_staleness_days` | Maximum allowed staleness for discovery use. |
| `record_hash` | Hash of normalized record fields. |
| `raw_record_hash` | Hash of raw source row where available. |
| `notes` | Review notes and limitations. |

Temporal selection rule:

For a given `signal_date`, the context panel may use only records satisfying:

- `as_of_date <= signal_date`
- `effective_start <= signal_date`
- `signal_date < effective_end` when `effective_end` is available
- stale-record rule passes
- security identifier maps to the ticker active on the signal date

If no record satisfies those rules, the ticker should be marked missing or blocked for that date. It should not be filled with current metadata.

Confidence tracking:

Confidence should be attached at three levels:

- record confidence, based on source and manual override status
- peer confidence, based on peer-group level and fallback distance
- date confidence, based on active group size, missingness, and staleness

## SECTION 5 - Historical Integrity Controls

Future-information leakage controls:

- Disallow static current labels in discovery runners.
- Require `as_of_date <= signal_date`.
- Require effective-date compatibility when effective dates exist.
- Preserve source snapshot dates and collection timestamps.
- Write metadata version and point-in-time quality into every future manifest.

Survivorship controls:

- Join metadata through stable security identifiers, not only current ticker strings.
- Report active universe coverage by date.
- Track delisted, renamed, merged, and spun-off securities where source data supports it.
- Do not silently drop unmatched historical tickers.

Classification drift controls:

- Store classification changes as append-only history.
- Produce change diagnostics by ticker, sector, industry, peer group, source, and date.
- Flag high-change-rate categories for manual review.
- Compare current and prior classifications before using them in discovery.

Peer-group contamination controls:

- Reconstruct peer groups from records active on each signal date.
- Require minimum active group sizes before computing peer-relative ranks or z-scores.
- Record fallback level and fallback reason for every date/ticker peer assignment.
- Block peer-relative transforms when only broad fallback is available.

Economic-context leakage controls:

- Keep inventory exposure audits diagnostic-only.
- Do not use sector-conditioned IC or peer-conditioned IC as validation evidence until a separate validation design approves it.
- Require universe-relative and proxy-relative baselines in future discovery design.
- Keep static snapshot metadata blocked from alpha, validation, governance, production, and ML use.

Validation requirements for the infrastructure:

- Current/history consistency checks.
- Duplicate identifier and duplicate active-record checks.
- Missing ticker and unmatched ticker reports.
- Date-level active coverage reports.
- Peer-group size and fallback-rate reports.
- Stale-record and point-in-time-quality summaries.
- Source audit with hashes and collection timestamps.

These are infrastructure validation requirements only, not alpha validation.

## SECTION 6 - Peer-Group Historical Framework

Peer groups should be derived from point-in-time records rather than stored as permanent static labels.

Historical reconstruction process:

1. Resolve active security identity for each `ticker` and `signal_date`.
2. Select the active sector and industry record using the effective-date framework.
3. Select the active size bucket if date-safe size data exists.
4. Count active names by industry, sector, and sector x size for the same signal date and universe.
5. Assign peer group by the approved hierarchy.
6. Write fallback level, group size, confidence, and blocked reason.

Peer reassignment:

- If a company changes industry, the peer group should change on the first signal date where the new classification is known and effective.
- The old peer group should remain available historically for dates before the change.

Classification changes:

- Sector and industry changes should be explicit records.
- The system should report old label, new label, source, first effective date, first known date, and affected signal-date range.

Sector migration:

- Sector migration should trigger a high-severity review flag because it can materially alter peer-relative history.
- Peer-relative calculations should use the sector known on the signal date, not the latest sector.

Industry migration:

- Industry migration should trigger peer-group reassignment and group-size recalculation by date.
- Thin-group fallback should be recalculated after migration.

Size migration:

- Size migration should be date-derived or source-dated.
- If size history is unavailable, sector x size fallback should be disabled for discovery and replaced by industry or sector fallback only.

Historical peer-group fields:

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
- `peer_confidence_score`
- `point_in_time_quality`
- `metadata_version`
- `blocked_for_peer_relative`

## SECTION 7 - Minimum Viable Implementation

Smallest implementation capable of reaching `POINT_IN_TIME_DISCOVERY_READY`:

Required components:

1. Point-in-time classification history.
   - Sector and industry records with `security_id`, ticker mapping, effective dates, as-of dates, source lineage, metadata version, and record hashes.

2. Security identity and ticker lineage.
   - Stable identifier mapping sufficient to join historical signal panels without relying only on current ticker labels.

3. Date-level context panel generator.
   - Produces sector, industry, peer group, and point-in-time quality for each ticker/date used in research.

4. Peer-group reconstruction diagnostics.
   - Reports group sizes, fallback rates, missingness, blocked peer groups, and date-level coverage.

5. Source audit and lineage artifacts.
   - Records raw source references, hashes, collection timestamps, source versions, normalization rules, and manual overrides.

6. Use-case blocking layer.
   - Blocks discovery if required point-in-time fields are absent or coverage/group-size rules fail.

7. Readiness manifest.
   - Writes metadata version, universe version, point-in-time quality, active coverage, peer fallback rate, stale-record count, and allowed use case.

Deferred components:

- Subindustry-level peer groups.
- Full fundamentals.
- Options, fixed income, macro, alternative data, ETF flow, short interest, and borrow data.
- ML or portfolio integration.
- Production metadata routing.
- Complex multi-vendor reconciliation beyond the first accepted source.
- Peer-relative alpha candidates or discovery runners.
- Sector-conditioned validation methodology.

Implementation sequence:

1. Source and lineage design gate.
2. Research-only ingestion design.
3. Point-in-time metadata staging and history implementation under separate approval.
4. Date-level coverage and peer reconstruction diagnostics.
5. Post-implementation readiness audit.
6. Only then, peer-relative discovery design.

Practical minimum:

The first implementation does not need perfect subindustry or full market-cap history. It must have date-safe sector and industry history, stable identity mapping, source lineage, and date-level peer reconstruction. Without those, it is still static-diagnostic infrastructure.

## SECTION 8 - Research Readiness Gates

These are infrastructure readiness gates only. They do not modify governance or alpha thresholds.

`NOT READY`

- Static snapshot only.
- Missing source lineage.
- No date-level coverage diagnostics.
- Peer-relative transforms blocked.
- Alpha validation allowed false.

`PARTIALLY READY`

- Diagnostic coverage is useful.
- Source lineage exists for static records.
- Peer fallback diagnostics exist.
- No point-in-time effective-date history.
- Discovery design may proceed, but discovery execution remains blocked.

`READY FOR DISCOVERY DESIGN`

- Candidate point-in-time source or source strategy is identified.
- Required schema and controls are designed.
- Expected coverage and peer-group feasibility are understood.
- No ingestion or candidate generation has occurred.
- A separate implementation task can be scoped.

`POINT_IN_TIME_DISCOVERY_READY`

- Sector and industry history are point-in-time safe.
- Stable security/ticker lineage is available for research joins.
- Date-level context panels can be produced.
- Active coverage by date meets documented readiness requirements.
- Peer groups are reconstructed by signal date with minimum group-size checks.
- Stale-record, missingness, fallback, and source-lineage diagnostics pass.
- Future discovery runners can load metadata with manifests proving point-in-time quality.

Readiness should be revoked or downgraded if source lineage is incomplete, if static labels are used for historical dates, or if peer-group fallback dominates the active universe beyond accepted design limits.

## SECTION 9 - Strategic Value Assessment

Diversification benefit:

High. This infrastructure would enable peer-relative, sector-relative, industry-relative, and economic-context alpha-family research. Those families could reduce dependence on hostile/stress repair, persistence, rank-coherence, and other OHLCV-only transformations.

Expected independence from existing families:

- High versus hostile/stress repair if context-aware discovery avoids stress-state gates.
- Medium-high versus persistence if peer-relative resilience is evaluated after controlling for universe-level rank persistence.
- Medium-high versus rank-coherence if peer-relative behavior is framed as economic cohort structure rather than broad cross-sectional churn.
- High versus dispersion if peer-relative dispersion uses industry or sector cohorts instead of universe-wide dispersion states.

Expected research value:

High. A point-in-time economic-context layer would let Project Underdog ask better questions:

- Is a signal idiosyncratic or sector-wide?
- Does repair outperform peers or merely rebound with an industry?
- Does persistence survive industry-relative normalization?
- Are rank-coherence effects concentrated in certain sectors or peer groups?
- Does dispersion matter more within economic cohorts?

Expected long-term importance:

Very high. This is infrastructure for multiple future research cycles, not a one-off candidate family. It can improve candidate discovery, contamination review, exposure audit, and eventual validation design.

Would this unlock a genuinely new information domain?

Yes. Point-in-time economic context would move the project from purely price/volume/state-derived alpha families toward business-context-aware alpha research. That is the most credible next information-domain expansion currently available.

## SECTION 10 - Final Recommendation

1. What is the minimum viable point-in-time infrastructure?

The minimum viable infrastructure is a research-only point-in-time classification and peer-context layer with sector and industry history, stable security/ticker lineage, effective-date controls, source lineage, date-level context panels, peer-group reconstruction, active coverage diagnostics, stale-record checks, and use-case blocking.

2. What should be deferred?

Defer subindustry breadth, full fundamentals, options, fixed income, macro, alternative data, ML, production routing, portfolio integration, complex multi-vendor reconciliation, peer-relative candidate design, and sector-conditioned validation methodology.

3. What is the highest-risk component?

The highest-risk component is source and identity lineage: obtaining reliable point-in-time sector/industry history tied to stable security identifiers across ticker changes, mergers, spin-offs, and delistings. If this is weak, the rest of the infrastructure can look polished while still leaking future information.

4. What is the expected implementation difficulty?

Medium-high. The project already has strong diagnostic scaffolding and current/history design patterns, but the source, lineage, and date-level reconstruction requirements are nontrivial.

5. Is the effort justified?

Yes. It is justified because it is the clearest path toward a genuinely new alpha information domain and because additional OHLCV-only refinements are showing diminishing diversification returns.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Source Gate and Schema Plan v1**. It should be design-only. It should compare acceptable source classes, define the required current/history schemas, specify source-audit artifacts, define date-level coverage diagnostics, and produce an implementation approval checklist. It should not implement ingestion, modify metadata, run discovery, run refinement, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This design does not change the current readiness state. Project Underdog remains on `STATIC_SNAPSHOT_RESEARCH_ONLY` economic-context metadata until a separately approved implementation and readiness audit demonstrate point-in-time discovery readiness.
