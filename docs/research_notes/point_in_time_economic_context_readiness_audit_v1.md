# Project Underdog - Point-in-Time Economic Context Readiness Audit v1

Date: 2026-06-20

Scope: review-only audit. No implementation, metadata mutation, governance mutation, threshold change, discovery, refinement, validation, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Current readiness state: `PARTIALLY READY`.

Project Underdog's economic-context substrate is diagnostically strong but not point-in-time discovery ready. Coverage is no longer the primary blocker: the enrichment artifacts report `488 / 488` stock-universe tickers covered, `1.000000` diagnostic coverage, `0` blocked tickers without metadata, and `27` diagnostically ready peer groups. The blocker is historical integrity. The current layer remains `STATIC_SNAPSHOT_RESEARCH_ONLY`, with alpha validation and peer-relative transform usage explicitly blocked.

Major blockers:

1. No point-in-time sector / industry / peer classification history.
2. No historical market-cap / size history approved for discovery use.
3. No security-master lineage for ticker changes, corporate actions, mergers, spin-offs, and delistings.
4. Peer groups are fallback-heavy and not date-stable.
5. Current inventory exposure metadata is descriptive only and cannot support alpha or validation claims.

Estimated distance to discovery readiness: medium to high. The project is close in architecture and diagnostics, but not close in data lineage. Readiness is realistically achievable if a point-in-time source or repeatable historical snapshot process is obtained and audited.

Overall recommendation: invest in point-in-time economic-context readiness as the next major infrastructure initiative, but do not execute peer-relative discovery until the data blockers are resolved. The research value is high enough to justify the effort because this is the clearest path toward a genuinely new information domain.

## SECTION 2 - Current Metadata Architecture

Current metadata sources:

- Manual reviewed static-snapshot metadata seed.
- Controlled manual override rows used to repair diagnostic coverage.
- Static sector, industry, peer-group, market-cap bucket, and size bucket fields.
- Date-derived behavioral buckets for diagnostics, such as liquidity and volatility buckets.
- Source-lineage, validation-check, fallback, and exposure artifacts written under `artifacts/research/economic_context_enrichment_v1/`.

Coverage:

- `metadata_readiness_review_v1`: `250 / 489` seed rows, `0.511247` universe coverage, and 5 peer groups above threshold.
- `manual_metadata_coverage_expansion_v3`: `360 / 489` matched tickers, `0.736196` coverage, and 9 peer groups above threshold.
- `economic_context_enrichment_v1`: `488 / 488` covered tickers, `1.000000` coverage, `0` missing universe tickers after diagnostic overrides, and `27` ready peer groups.

Enrichment process:

- Static metadata is loaded into a diagnostic economic-context substrate.
- Validation and use-case blocking helpers preserve the `STATIC_SNAPSHOT_RESEARCH_ONLY` status.
- The process writes coverage diagnostics, peer-group distributions, fallback reports, source-lineage reports, and current inventory exposure audits.
- The implementation intentionally does not authorize alpha candidates, validation anchors, production paths, ML routing, or governance changes.

Peer assignment process:

The current process assigns diagnostic peer groups using a fallback hierarchy:

1. industry group when peer count is sufficient
2. sector group or sector x size group when industry is thin
3. broad size fallback if needed
4. blocked / insufficient context if no safe diagnostic group exists

The refined peer-quality artifacts show:

- `182` tickers as `HIGH_CONFIDENCE_INDUSTRY_PEER`
- `280` tickers as `MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER`
- `26` tickers as `MEDIUM_CONFIDENCE_SECTOR_PEER`

Fallback hierarchy:

The fallback hierarchy is suitable for descriptive diagnostics. It is not a substitute for point-in-time peer membership because the fallback assignment is static and not dated by signal date.

## SECTION 3 - Point-in-Time Integrity Assessment

| component | point-in-time status | rationale |
| --- | --- | --- |
| Sector classifications | Not point-in-time safe | Current sector labels are static snapshot metadata. No historical effective dates or sector-change history are available for alpha use. |
| Industry classifications | Not point-in-time safe | Industry labels are useful diagnostically, but static labels can leak current business classification into past signal dates. |
| Subindustry / granular peer labels | Not point-in-time safe | Granular peer groups are thin and static; no effective-start/effective-end history exists. |
| Size classifications | Not point-in-time safe | Static market-cap and size buckets cannot support historical size-relative or size-neutral discovery. |
| Market-cap metadata | Not point-in-time safe | No approved historical market-cap snapshots or market-cap effective dates are available. |
| Peer-group assignments | Not point-in-time safe | Assignments are fallback-based and static. They do not reconstruct peer membership by date. |
| Inventory exposure metadata | Partially safe for diagnostics only | Exposure audits are descriptive and labeled `STATIC_SNAPSHOT_RESEARCH_ONLY`; they are not safe for alpha, validation, or governance decisions. |
| Economic-context metadata schema | Partially safe | Schema and current/history design are appropriate, but the populated data is static-only. |
| Date-derived liquidity / volatility buckets | Partially safe | These may become safe if computed only from pre-signal data and frozen by date; current use remains diagnostic. |
| Source lineage and hashing | Partially safe | Lineage artifacts exist, but they document static snapshots rather than point-in-time historical classification records. |
| Ticker and corporate-action lineage | Not point-in-time safe | No survivorship-free security-master lineage is available for peer-relative discovery. |

Overall integrity conclusion:

The architecture is partially ready, but the populated metadata is not point-in-time safe. The system knows how to label, audit, and block unsafe usage; it does not yet have the historical data needed to lift the block.

## SECTION 4 - Leakage Risk Assessment

| risk | severity | description |
| --- | --- | --- |
| Static classification look-ahead | Critical | Applying today's sector or industry to past signal dates can leak future business identity and reclassification information. |
| Survivorship bias | Critical | Current universe and current classifications may omit delisted, merged, renamed, or historically relevant securities. |
| Ticker / corporate-action lineage gaps | High | Ticker changes, share-class changes, mergers, and spin-offs can map historical observations to the wrong economic entity. |
| Classification drift | High | Sector and industry labels can change as companies evolve or vendors update taxonomies. |
| Peer-group drift | High | Peer groups can gain or lose members over time; static fallback groups cannot represent historical peer context. |
| Static size leakage | High | Current market-cap or size bucket labels can leak later company scale into earlier dates. |
| Fallback false precision | Medium-high | Sector x size fallback groups look complete but may mix economically different businesses. |
| Sector-conditioned IC misuse | Medium-high | Descriptive sector exposure could be mistaken for sector-conditioned validation evidence. |
| Economic-context overfitting | Medium | Multiple context dimensions can invite parameter mining if discovery is not tightly scoped. |

Ranked risks by severity:

1. Static classification look-ahead.
2. Survivorship and security-master gaps.
3. Missing historical market-cap / size history.
4. Peer-group drift and fallback false precision.
5. Sector-conditioned or peer-conditioned validation leakage.

## SECTION 5 - Discovery Readiness Gap Analysis

Requirements to reach `POINT_IN_TIME_DISCOVERY_READY`:

| requirement | description | importance | implementation complexity | dependency chain |
| --- | --- | --- | --- | --- |
| Point-in-time classification source | Obtain sector, industry, and preferably subindustry records with `as_of_date`, `effective_start`, and `effective_end` or repeatable historical snapshots. | Critical | High | Source selection, licensing/access review, ingestion design, lineage audit. |
| Security-master / ticker lineage | Track ticker changes, corporate actions, mergers, spin-offs, delistings, and identifier continuity. | Critical | High | Source selection, identifier mapping, universe reconciliation. |
| Historical size / market-cap history | Provide date-safe market-cap or size buckets for size-aware peer grouping and residual checks. | High | Medium-high | Market-cap source, split adjustment checks, as-of dating. |
| Current/history storage tables | Populate append-only history and current tables with versioned metadata records. | High | Medium | Schema finalization, ingestion implementation, record hashing. |
| Date-level coverage diagnostics | Compute active coverage by signal date and dynamic universe membership, not only current coverage. | High | Medium | Metadata panels, universe history joins, missingness reports. |
| Date-level peer-group construction | Assign peer groups as of each signal date with minimum active group-size checks. | High | Medium-high | PIT classifications, size history, fallback policy. |
| Staleness controls | Flag stale records and set maximum stale-age diagnostics before a record can be used. | Medium-high | Medium | Effective dates or snapshot cadence, stale-date policy. |
| Fallback policy for discovery | Define when industry, sector, sector x size, or blocked status is allowed. | Medium-high | Medium | Peer-group diagnostics, minimum group sizes. |
| Leakage review checklist | Document blocked uses, allowed uses, and required manifest fields for any future context-aware runner. | High | Low-medium | Governance review note, runner manifest conventions. |
| Baseline comparison design | Require universe-relative and proxy-relative baselines in future discovery review. | Medium | Low-medium | Future design task; no current implementation. |

Minimum discovery-ready condition:

The project needs date-safe metadata panels that can answer: "What sector, industry, size bucket, and peer group would have been known for this ticker on this signal date?" Until that answer is auditable, peer-relative discovery should remain blocked.

## SECTION 6 - Feasibility Assessment

Feasibility classification: difficult but realistic.

Why it is not easy:

- The current project has strong static diagnostics but lacks point-in-time source data.
- Manual static expansion cannot solve historical integrity, no matter how high coverage becomes.
- A reliable source must cover historical classifications, security identifiers, ticker changes, and market-cap or size history.
- Peer-relative discovery requires date-level group membership and group-size diagnostics, not just current labels.

Why it is realistic:

- The architecture already anticipates current/history tables, source lineage, record hashes, snapshot warnings, fallback logic, and use-case blocking.
- The research workflow is disciplined enough to separate diagnostic, discovery, validation, and governance uses.
- The stock universe is manageable in size, making a controlled point-in-time layer feasible if a suitable source exists.
- The expected research value is high enough to justify a focused infrastructure initiative.

Most plausible remediation path:

1. Identify or acquire a point-in-time classification and security-master source.
2. Build an append-only metadata history layer.
3. Run a readiness-only audit on date-level coverage and peer-group stability before any candidate design.

Point-in-time readiness is realistically achievable, but it requires a data/source initiative rather than another static metadata expansion.

## SECTION 7 - Strategic Value Assessment

Assuming readiness can be achieved, the strategic value is high.

Diversification value:

- Peer-relative and economic-context behavior would reduce dependence on hostile/stress-repair, h20 stabilization, persistence, and rank-coherence lineages.
- It could produce families driven by economic cohort behavior rather than broad universe ranks.

Independence from existing families:

- High versus hostile/stress-repair if context-aware discovery avoids stress gates.
- Medium-high versus persistence and rank-coherence if peer-relative residuals are designed as separate context effects rather than re-labeled rank transforms.
- High versus dispersion if peer-relative dispersion is tested as industry or sector cohort behavior.

Expected research value:

- High. It can answer whether current signals are idiosyncratic, sector-wide, industry-wide, or peer-relative.
- It can support new families such as peer-relative resilience, industry leadership rotation, sector-relative persistence, and peer-relative dispersion.
- It can improve contamination reviews for existing candidates.

Expected long-term importance:

Very high. A point-in-time economic-context layer is a foundation for future peer-relative alpha, sector diagnostics, contextual contamination reviews, and eventually richer domain expansion. It is more foundational than another small OHLCV-only discovery batch.

Would this unlock a genuinely new information domain?

Yes. If point-in-time safe, this would be the first major expansion from price/volume/state-derived features into economic-context-aware alpha research.

## SECTION 8 - Recommended Remediation Sequence

Stage 1: Source and lineage readiness review.

- Identify candidate sources for point-in-time sector, industry, subindustry, market-cap, and security-master lineage.
- Determine whether any existing local data can provide historical effective dates or date-stamped snapshots.
- Review licensing, reproducibility, source hashes, and collection rules.
- Define mandatory fields: ticker, stable identifier, sector, industry, source, as-of date, effective-start/end, collection timestamp, metadata version, universe version, and record hash.
- Output should be a review/design note only.

Stage 2: Point-in-time metadata architecture design.

- Design current/history tables for classification, size, source audit, ticker lineage, and coverage diagnostics.
- Define date-level joins to dynamic top-300 membership and signal dates.
- Define stale-record flags, maximum staleness diagnostics, missingness reports, and minimum group-size rules.
- Define allowed/blocked use cases for discovery, validation, governance, production, and ML.
- Keep all work design-only until source readiness is accepted.

Stage 3: Readiness implementation and audit gate.

- After separate approval, implement ingestion and diagnostics in research-only paths.
- Produce date-level coverage, peer-group stability, stale classification, ticker-lineage, and fallback-rate artifacts.
- Run a post-implementation readiness audit before any peer-relative candidate design.
- Only after this gate should a context-aware discovery design be considered.

## SECTION 9 - Readiness Classification

Classification: `READY AFTER REMEDIATION`.

Rationale:

- The current state is not discovery ready because populated metadata remains static snapshot only.
- The architecture and diagnostic scaffolding are advanced enough that remediation is plausible.
- The single biggest missing component is not more diagnostic coverage; it is point-in-time historical lineage.
- If the project obtains or builds reliable point-in-time classification, size, and security-master history, the frontier can become discovery ready.

This classification does not authorize discovery execution. It means the path to `POINT_IN_TIME_DISCOVERY_READY` is credible and worth pursuing through staged remediation.

## SECTION 10 - Final Recommendation

1. What is the single biggest blocker?

The single biggest blocker is the absence of point-in-time sector / industry / peer classification history with effective dates or date-stamped source snapshots. Static current labels cannot be used for historical peer-relative discovery without look-ahead risk.

2. Is point-in-time readiness realistically achievable?

Yes. It is difficult but realistic if the project can obtain or construct a reliable point-in-time metadata source with security-master lineage and historical size context.

3. Is the effort justified?

Yes. The expected research value is high because this is the most credible path toward a genuinely independent information domain beyond OHLCV-derived transformations.

4. Would this materially expand the project's information universe?

Yes. Point-in-time economic context would allow Project Underdog to study peer-relative resilience, industry leadership rotation, sector-relative persistence, peer-relative dispersion, and context-conditioned alpha in a way current OHLCV-only research cannot.

5. Should this become the next major infrastructure initiative?

Yes, with a strict gate. It should become the next major infrastructure initiative only as a staged readiness program. It should not immediately become discovery execution.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Source and Lineage Design v1**. It should be design-only and should identify acceptable source options, required fields, current/history table design, security-master lineage requirements, date-level coverage diagnostics, stale-record controls, and the readiness gate required before peer-relative discovery. It should not implement anything, modify metadata, run discovery, run refinement, run validation, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This audit does not change the status of the economic-context substrate. Current metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY`; peer-relative transforms, sector-relative alpha, industry-relative z-scores, validation claims, production use, portfolio routing, ML, and governance use remain blocked.
