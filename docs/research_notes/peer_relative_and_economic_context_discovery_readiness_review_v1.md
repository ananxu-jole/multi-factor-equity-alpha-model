# Project Underdog - Peer-Relative and Economic-Context Discovery Readiness Review v1

Date: 2026-06-20

Scope: review-only readiness assessment. No discovery, refinement, validation, governance mutation, threshold change, production registration, ML implementation, or candidate promotion/demotion was performed.

## SECTION 1 - Executive Summary

Project Underdog's economic-context infrastructure has advanced materially, but it is not yet mature enough for peer-relative alpha discovery execution. The substrate is strong for diagnostics, coverage review, exposure monitoring, and discovery design. It remains blocked for peer-relative transforms, sector-relative alpha candidates, industry-relative z-scores, validation-quality sector-conditioned claims, and production use because the current metadata layer is static-snapshot research metadata rather than point-in-time historical metadata.

Readiness classification: `PARTIALLY READY`.

Interpretation:

- Ready for: discovery design, metadata hardening review, descriptive exposure audits, peer-group quality diagnostics, and roadmap planning.
- Not ready for: discovery execution, candidate panels, IC scoring, validation, governance use, production routing, ML, or candidate status changes.

Economic-context substrate maturity:

- Coverage is now diagnostically complete in the enrichment artifacts: `488 / 488` stock-universe tickers covered, coverage ratio `1.000000`, and no blocked tickers without metadata.
- The substrate includes schema scaffolds, static metadata loaders, use-case blocking helpers, peer fallback reports, source-lineage artifacts, and current-inventory exposure audits.
- The implementation status remains `ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY`.

Peer-group infrastructure maturity:

- Peer-group diagnostics are useful but uneven.
- The current enrichment artifacts report `127` peer groups, `110` thin groups, and `27` ready peer groups at the diagnostic threshold.
- Peer quality is mostly fallback-based: `182` tickers are high-confidence industry peers, `280` are medium-confidence sector x size peers, and `26` are medium-confidence sector peers.
- All peer outputs remain diagnostic-only, with validation usage and peer-relative transforms explicitly set to `False`.

Suitability for future alpha discovery:

Peer-relative and economic-context behavior remains the highest-priority diversification frontier, but the next step should be readiness hardening and design, not alpha discovery execution. Success here would expand the project beyond primarily OHLCV-derived transformations, but using static metadata for historical alpha discovery would create unacceptable leakage and false-diversification risk.

## SECTION 2 - Metadata Coverage Review

Coverage has improved across successive metadata work:

| stage | coverage state | interpretation |
| --- | --- | --- |
| `metadata_readiness_review_v1` | `250 / 489` seed rows; coverage ratio `0.511247`; inventory coverage `0.518828`; 5 peer groups above threshold | Useful for descriptive diagnostics only. |
| `manual_metadata_coverage_expansion_v3` | `360 / 489` matched universe tickers; coverage ratio `0.736196`; inventory coverage `0.734310`; 9 peer groups above threshold | Stronger static-snapshot diagnostic coverage, still blocked for alpha. |
| `economic_context_enrichment_v1` | `488 / 488` covered tickers; coverage ratio `1.000000`; fallback coverage `1.000000`; blocked tickers `0` | Complete diagnostic substrate after controlled overrides, still static-only. |

Coverage is sufficient for discovery planning and diagnostic review. It is not sufficient for discovery execution because historical point-in-time validity is not established.

Remaining weaknesses:

- Current coverage is static-snapshot coverage, not point-in-time historical coverage.
- Manual overrides repair diagnostic coverage but are not alpha inputs.
- Historical sector, industry, subindustry, peer-group, market-cap, ticker-change, and corporate-action lineage remain unavailable or unapproved for validation-quality use.
- Static sector and size labels can describe current exposure but cannot safely reconstruct historical peer groups.
- Peer-relative transform allowed remains `False`.
- Alpha validation allowed remains `False`.
- Production use allowed remains `False`.

Quality classification:

The correct quality label remains `STATIC_SNAPSHOT_RESEARCH_ONLY`. This is strong enough for descriptive concentration and coverage diagnostics. It is not strong enough for historical alpha claims.

## SECTION 3 - Peer-Group Quality Review

Peer assignment methodology:

The current peer assignment uses a diagnostic fallback hierarchy:

1. industry group when peer count is sufficient
2. sector x size group when industry is thin
3. sector group when sector x size is unavailable or thin
4. broad size bucket if needed
5. blocked / insufficient context

Peer confidence from the refined artifacts:

| peer quality status | assigned level | ticker count | median peer group size | median fallback distance | median confidence | validation usage |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `HIGH_CONFIDENCE_INDUSTRY_PEER` | industry | 182 | 11.0 | 0.0 | 1.00 | False |
| `MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER` | sector_size | 280 | 20.0 | 2.0 | 0.65 | False |
| `MEDIUM_CONFIDENCE_SECTOR_PEER` | sector | 26 | 36.0 | 1.0 | 0.50 | False |

Are peer groups economically meaningful?

Partially. The industry peers are economically meaningful enough for diagnostics. Sector x size peers are a useful fallback, but they are coarser and may mix businesses with different economics. Broad sector peers are weaker and should be treated as exposure context rather than true peer groups.

Are they stable enough for alpha discovery?

Not yet. The peer groups are stable enough for descriptive diagnostics and discovery design, but not stable enough for historical alpha discovery. The blocker is not current coverage; it is the absence of point-in-time classification and market-cap history. Without that, a peer-relative discovery pass would risk applying today's business classifications to past observations.

Industry integrity:

Industry integrity is acceptable for the 182 high-confidence industry-peer tickers, but many industry groups remain thin. The enrichment diagnostics still report `110` thin original peer groups.

Sector integrity:

Sector-level coverage is broad across 11 sectors and useful for descriptive exposure monitoring. Sector labels alone are too coarse for peer-relative discovery.

Size-group integrity:

Size grouping is useful as a diagnostic fallback, but static size buckets are not safe for historical size-neutral alpha claims. Point-in-time market-cap or date-derived size controls are required before size-aware discovery execution.

## SECTION 4 - Information Domain Assessment

Peer-relative and economic-context information would constitute a genuinely new information domain if implemented with point-in-time controls. It is not merely another OHLCV transformation: it adds business-context structure, sector/industry membership, peer comparability, and possible residual behavior relative to economically comparable names.

Independence from persistence:

- Persistence currently asks whether rank stability after drawdown predicts returns.
- Peer-relative context would ask whether persistence or resilience is unusual relative to economic peers.
- This could separate market-wide rank persistence from company-specific or industry-relative persistence.

Independence from rank-coherence:

- Rank-coherence currently uses universe-level rank-turnover resilience.
- Peer-relative context could test rank coherence inside sectors, industries, or peer groups, which may reveal whether current rank-coherence evidence is broad cross-sectional structure or hidden economic-cohort behavior.

Independence from hostile/stress-repair:

- Hostile/stress-repair is state-driven and repair-oriented.
- Peer-relative behavior can be neutral, positive, negative, or state-conditioned without requiring hostile/stress states.
- It may also diagnose whether repair candidates are truly idiosyncratic or simply sector-wide rebounds.

Expected diversification value:

High. Success would meaningfully expand the project's information universe beyond OHLCV-only transforms and state-repair mechanics. The caveat is severe: without point-in-time metadata, the same frontier could create false diversification through look-ahead contamination.

Would success here meaningfully expand the project's information universe?

Yes. A validation-safe peer-relative family would be the first material move into economic-context-aware alpha behavior and could support several future families: peer-relative strength, peer-relative weakness, sector-relative persistence, industry leadership rotation, and peer-relative dispersion.

## SECTION 5 - Discovery Feasibility Review

The categories below are feasible for future design, but not for immediate discovery execution under the current static-snapshot constraint.

| category | feasibility | rationale |
| --- | --- | --- |
| Peer-relative strength | Medium after point-in-time metadata; low now | Needs stable peer groups and historical peer membership. |
| Peer-relative weakness | Medium after point-in-time metadata; low now | Same peer-history requirement; also needs anti-reversal diagnostics. |
| Industry leadership rotation | Medium | Economically attractive, but requires reliable industry cohorts through time. |
| Sector-relative persistence | Medium | Easier than industry peers because sectors are broader, but still point-in-time blocked. |
| Peer-relative dispersion | Medium-high after metadata readiness | Strong diversification potential; combines underpowered dispersion work with economic cohorts. |
| Inventory exposure behavior | High for diagnostics, low for alpha | Existing exposure audit can monitor hidden concentration, but not drive alpha claims. |
| Economic-context-conditioned alpha | Medium after controls | Useful as a review layer first; alpha use requires clear separation from metadata leakage. |

No candidates should be designed from this note. The appropriate next step is to specify metadata prerequisites and discovery-design boundaries.

## SECTION 6 - Risks and Failure Modes

Metadata contamination risk:

This is the most serious risk. Static current classifications can leak future business identity into past dates. Manual overrides and current snapshots must not be used as historical alpha inputs.

Classification instability:

Sector, industry, and peer labels can change through business model shifts, mergers, spin-offs, ticker changes, and vendor taxonomy updates. Without effective dates, historical peer groups are unreliable.

Peer-group noise:

Many industry groups remain thin. Fallback groups improve coverage but reduce economic precision. Sector x size groups are useful for diagnostics, but they may blend unrelated businesses.

False diversification risk:

Peer-relative features could appear independent simply because they transform the same OHLCV signal through a static metadata lens. Independence should not be claimed until contamination and point-in-time controls are in place.

Over-complexity risk:

Economic context can multiply design choices: sector, industry, subindustry, size, liquidity, volatility, peer fallback, and residualization. Without tight scope, discovery could become parameter mining.

Economic-context leakage risk:

The project must prevent validation-like claims from descriptive metadata slices. Sector-conditioned IC, peer-relative ranks, and industry-neutral residuals are blocked until point-in-time metadata exists.

Most serious risks:

1. point-in-time leakage from static metadata
2. false diversification from coarse fallback groups
3. peer-group thinness and instability
4. over-complex candidate design once context dimensions are introduced

## SECTION 7 - Strategic Position in Roadmap

Economic-context work should move forward in the roadmap, but as readiness hardening and discovery design rather than discovery execution.

Is this frontier arriving earlier than originally expected?

Yes, strategically. The persistence and rank-coherence cycles improved diversification but also showed diminishing returns from purely OHLCV-derived transformations. At the same time, the economic-context substrate has advanced from partial static coverage to complete diagnostic coverage with peer-quality, fallback, and inventory exposure artifacts.

Why it is arriving earlier:

- The alpha-family inventory remains too concentrated in hostile/stress repair.
- Persistence and rank-coherence are conditional lineages, not broad families.
- Dispersion remains distinct but weak.
- Economic-context diagnostics now have enough coverage and structure to support careful design.
- The project's largest remaining diversification gap is information-domain expansion, not another small OHLCV parameter refinement.

Why it is not ready for discovery execution:

- The metadata is still static-snapshot only.
- Peer-relative transform usage remains explicitly blocked.
- Alpha validation usage remains explicitly blocked.
- Sector-conditioned historical claims remain explicitly blocked.

## SECTION 8 - Readiness Classification

Classification: `PARTIALLY READY`.

Detailed rationale:

- The substrate is mature enough for discovery design: coverage is complete diagnostically, artifacts are auditable, peer fallback logic exists, and current-inventory exposure diagnostics are informative.
- The substrate is not mature enough for discovery execution: point-in-time sector, industry, peer-group, size, market-cap, ticker-lineage, and corporate-action controls are not yet available for historical alpha use.
- Peer groups are directionally meaningful but not uniformly high confidence. Only 182 tickers receive high-confidence industry-peer assignment; most covered tickers depend on sector x size fallback.
- Any alpha discovery using the current static layer would violate the existing metadata use-case blocks and risk look-ahead contamination.

Operational interpretation:

`PARTIALLY READY` means ready to design the next frontier and specify data prerequisites. It does not authorize candidate generation, panel generation, IC scoring, refinement, validation, governance changes, production registration, ML, or candidate status changes.

## SECTION 9 - Recommended Next Frontier

Discovery readiness is not confirmed for execution. The highest-priority context-aware frontier remains:

`peer-relative resilience and residual strength`

This should be treated as a future discovery frontier, not an immediate candidate batch.

Rationale:

- It directly addresses the largest diversification gap identified in the alpha-family inventory review.
- It can test whether securities behave unusually relative to comparable businesses rather than only relative to the full universe.
- It can help diagnose whether existing persistence and rank-coherence evidence is genuinely broad or actually cohort-relative.

Diversification value:

High. If implemented with point-in-time peer data, this frontier could add the project's first economically contextual alpha family and reduce dependence on hostile/stress-repair behavior.

Expected independence:

High versus hostile/stress repair if designed without stress-state gates. Medium-high versus persistence and rank-coherence if peer-relative residuals are evaluated as a separate context layer rather than a renamed rank transform.

Expected implementation complexity:

Medium-high. The conceptual frontier is clear, but the data prerequisite is nontrivial: point-in-time peer membership, sector/industry lineage, market-cap or size history, and ticker/corporate-action mapping.

Recommended immediate action:

Do not design candidates yet. First create a point-in-time metadata readiness and source acquisition plan that determines whether validation-safe peer-relative discovery can be supported.

## SECTION 10 - Final Recommendation

1. Is the economic-context substrate mature enough for discovery?

Not for discovery execution. It is mature enough for discovery design and diagnostic planning. The current substrate is `ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY`, with alpha validation and peer-relative transforms still blocked.

2. Are peer groups sufficiently trustworthy?

Partially. Industry peers are useful where high-confidence groups exist, but most tickers rely on sector x size fallback. The peer groups are trustworthy for diagnostics, not yet for historical alpha discovery.

3. Does this represent a genuinely new information domain?

Yes, if implemented with point-in-time controls. Peer-relative and economic-context behavior would expand the project beyond OHLCV-only transformations and could become a genuinely new information domain.

4. Is this the highest-priority diversification frontier?

Yes strategically, but not execution-ready. The next move should harden metadata and design the frontier, not run discovery.

5. Is ML still premature?

Yes. ML remains premature until family diversity improves and point-in-time context data is available. Introducing ML now would likely amplify state exposure, metadata leakage, and false-diversification risk.

6. Are options/fixed-income still future-phase work?

Yes. Options, fixed income, macro, and alternative data should remain future-phase work until the equity alpha-family inventory and context metadata substrate are stronger.

7. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Readiness and Peer-Relative Discovery Design Gate v1**. It should be review-and-design only. It should audit available point-in-time metadata options, define minimum requirements for sector/industry/peer/size history, specify anti-leakage controls, and determine whether a future peer-relative discovery design can proceed. It should not run discovery, create candidates, generate panels, run IC scoring, refine, validate, modify governance, change thresholds, register production outputs, implement ML, or promote/demote candidates.

## Research Caveat

This review does not authorize peer-relative alpha discovery. It preserves the existing block on static metadata for alpha validation, peer-relative transforms, sector-conditioned IC claims, production use, portfolio routing, ML, and governance decisions.
