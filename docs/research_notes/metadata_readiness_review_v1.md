# Metadata Readiness Review v1

Date: 2026-05-24

Status: `METADATA_DIAGNOSTIC_READY_STATIC_SNAPSHOT`

Action: diagnostic use allowed; alpha and validation use remain blocked.

## Objective

Review whether the expanded static-snapshot metadata seed is ready for broader diagnostic use while preserving strict blocks on alpha research, validation claims, production use, and point-in-time claims.

Current metadata state:

- seed rows: `250`
- universe tickers: `489`
- coverage ratio: `0.511247`
- extra seed tickers: `0`
- duplicate tickers: `0`
- key-field missingness: `0`
- static warning: all rows retain `STATIC_SNAPSHOT_RESEARCH_ONLY`
- inventory metadata coverage: `0.518828`
- sectors represented: `11`
- sectors with at least 10 names: `11`
- peer groups meeting 8-name threshold: `5`

## Allowed / Blocked Decision Table

| Use case | Decision | Rationale |
| --- | --- | --- |
| Metadata coverage dashboard | ALLOWED | Coverage is above 50%, with no duplicate or extra seed tickers. |
| Sector distribution diagnostics | ALLOWED | All 11 represented sectors have at least 10 names. |
| Inventory metadata coverage checks | ALLOWED | Current inventory panels have about 51.9% metadata coverage. |
| Descriptive inventory sector exposure | ALLOWED | Descriptive-only exposure summaries are useful for monitoring concentration. |
| Missingness and lineage audits | ALLOWED | Key-field missingness is zero and source labels are tracked. |
| Thin peer-group warnings | ALLOWED | Peer groups remain uneven; warning diagnostics are valuable. |
| Sector-relative alpha research | BLOCKED | Static snapshot and incomplete coverage are not sufficient for alpha design. |
| Peer-relative transforms | BLOCKED | Only 5 peer groups meet the 8-name threshold; most remain thin. |
| Sector-conditioned IC or return attribution claims | BLOCKED | Would create validation-like interpretation from non-point-in-time metadata. |
| Historical sector-relative validation | BLOCKED | No point-in-time sector/industry history exists. |
| Production use | BLOCKED | The layer is research-only and not ingested into production metadata tables. |
| Portfolio / ML / blending / optimization routing | BLOCKED | The layer is not approved for downstream routing or model conditioning. |

## Sector-Level Readiness

Sector-level diagnostics are now partially ready for descriptive use.

Current sector counts:

| sector | ticker_count |
| --- | ---: |
| Financials | 41 |
| Health Care | 37 |
| Information Technology | 28 |
| Utilities | 26 |
| Real Estate | 24 |
| Materials | 20 |
| Communication Services | 17 |
| Consumer Discretionary | 16 |
| Industrials | 16 |
| Consumer Staples | 15 |
| Energy | 10 |

Allowed sector-level uses:

- sector distribution review
- sector coverage monitoring
- descriptive inventory signal exposure by sector
- sector concentration warnings
- missingness and source coverage by sector

Blocked sector-level uses:

- sector-relative ranking
- sector-neutral residualization
- sector-conditioned IC claims
- sector-conditioned validation decisions
- claims about historical sector exposures

Reason:

The sector layer is still a current/static snapshot. It can describe the current reviewed metadata sample, but it cannot safely reconstruct historical sector memberships.

## Industry / Peer-Group Readiness

Peer-group diagnostics improved but remain limited.

Peer groups meeting the 8-name threshold:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Electric Utilities` | 15 |
| `industry:Health Care Equipment` | 12 |
| `industry:Semiconductors` | 10 |
| `industry:Specialty Chemicals` | 8 |
| `industry:Multi Utilities` | 8 |

Near-threshold peer groups:

| peer_group_label | ticker_count |
| --- | ---: |
| `industry:Biotechnology` | 7 |
| `industry:Application Software` | 7 |
| `industry:Residential REITs` | 6 |
| `industry:Financial Exchanges and Data` | 6 |
| `industry:Systems Software` | 6 |
| `industry:Retail REITs` | 5 |
| `industry:Property and Casualty Insurance` | 5 |
| `industry:Regional Banks` | 5 |
| `industry:Aerospace and Defense` | 5 |
| `industry:Asset Management and Custody Banks` | 5 |

Allowed peer-level uses:

- peer-group size diagnostics
- thin-group warnings
- tracking which peer groups are approaching readiness
- descriptive coverage review for candidate exposures

Blocked peer-level uses:

- peer-relative alpha transforms
- industry-relative z-scores
- peer-neutral residualization
- peer-conditioned validation claims

Reason:

Most peer groups remain thin, and the labels are still manually reviewed static-snapshot labels.

## Market-Cap / Size Bucket Readiness

Current bucket counts:

| bucket_type | bucket | ticker_count |
| --- | --- | ---: |
| market_cap_bucket | `large_cap` | 136 |
| market_cap_bucket | `mega_cap` | 60 |
| market_cap_bucket | `mid_large_cap` | 54 |
| size_bucket | `large` | 136 |
| size_bucket | `mega` | 60 |
| size_bucket | `mid_large` | 54 |

Allowed uses:

- descriptive size-bucket distribution
- metadata coverage by static size bucket
- inventory exposure diagnostics by static size bucket
- missingness and lineage checks

Blocked uses:

- historical size-relative validation
- size-neutral alpha research
- market-cap backfills
- claims about historical market-cap state

Reason:

Market-cap and size buckets are static current-snapshot approximations. They are useful for metadata diagnostics but not historical claims.

## Inventory Metadata Coverage Readiness

Current inventory coverage:

| signal_name | panel_tickers | metadata_covered_tickers | metadata_coverage_ratio |
| --- | ---: | ---: | ---: |
| `participation_liquidity_state_shift_20_60` | 478 | 248 | 0.518828 |
| `participation_breadth_repair_under_hostile_trend` | 478 | 248 | 0.518828 |
| `volatility_compression_after_stress_stabilization` | 478 | 248 | 0.518828 |

Allowed inventory uses:

- metadata coverage checks by candidate
- descriptive sector exposure by candidate
- identifying concentration warnings
- tracking coverage drift as metadata expands

Blocked inventory uses:

- sector-conditioned IC conclusions
- sector-relative candidate scoring
- downgrade/upgrade decisions based on sector slices
- validation routing based on sector metadata

Reason:

Coverage is now high enough to make descriptive diagnostics informative, but not enough to support statistical claims or governance decisions.

## Remaining Thin-Group Risks

Risks:

- Most industry and peer groups remain below the 8-name threshold.
- Several sectors may be dominated by one or two peer groups.
- Manual labels may contain inconsistent industry granularity.
- Sparse peer groups can create false concentration signals.
- Static labels may not reflect historical business classification.

Controls:

- keep peer-level output diagnostic-only
- display thin-group warnings beside every peer summary
- do not compute peer-relative scores
- prioritize near-threshold peer groups in future expansion
- require source-lineage review before database ingestion

## Static-Snapshot Limitations

The metadata layer is explicitly static snapshot research metadata.

Limitations:

- It describes a current reviewed classification sample.
- It may not represent historical classifications.
- It may encode current business classifications into past periods if misused.
- It may miss delisted, renamed, or historically reclassified names.
- It does not provide historical market cap.

Required label:

`STATIC_SNAPSHOT_RESEARCH_ONLY`

Every note, artifact, and diagnostic using this layer must preserve that label.

## Point-In-Time Limitations

Point-in-time validity is blocked.

The current layer does not include:

- historical effective classification dates
- source-provided point-in-time sector histories
- corporate action history
- ticker change history
- historical market-cap snapshots
- survivorship-free security-master lineage

Therefore, it cannot support:

- historical sector-relative validation
- sector-aware alpha claims
- point-in-time peer-group reconstruction
- production metadata routing

## Decision Tree For Future Use

1. Is the use diagnostic-only?
   - If yes, continue.
   - If no, block.

2. Does the output preserve `STATIC_SNAPSHOT_RESEARCH_ONLY`?
   - If yes, continue.
   - If no, block.

3. Is the output descriptive coverage, distribution, exposure, or missingness?
   - If yes, allow.
   - If it computes alpha IC, returns, ranking, residualization, or validation, block.

4. Is the analysis sector-level?
   - Descriptive sector exposure is allowed.
   - Sector-relative signal construction is blocked.

5. Is the analysis peer-level?
   - Thinness diagnostics are allowed.
   - Peer-relative transforms are blocked until broader coverage and peer-group adequacy improve.

6. Does the use require historical correctness?
   - If yes, block until point-in-time metadata exists.

7. Does the use affect production, survivor/watchlist, validation, gates, portfolio, ML, blending, or optimization?
   - If yes, block.

## Recommended Next Step

Recommended next step:

Continue controlled metadata expansion toward `350+` rows and at least `70%` universe coverage before considering any sector-aware alpha design.

Priority expansion targets:

- near-threshold peer groups:
  - `industry:Application Software`
  - `industry:Biotechnology`
  - `industry:Residential REITs`
  - `industry:Financial Exchanges and Data`
  - `industry:Systems Software`
  - `industry:Regional Banks`
- lower-coverage sectors and industries
- additional mid-large and large names to improve size-bucket diversity

Before sector-aware alpha design, the project should require:

- broader coverage, preferably 70%+ of universe
- more peer groups above the minimum size threshold
- source-lineage review of manual classifications
- explicit approval that the work remains exploratory static-snapshot research
- ideally, a point-in-time metadata source for validation-quality work

## Final Decision

Current status:

`METADATA_DIAGNOSTIC_READY_STATIC_SNAPSHOT`

Allowed:

- descriptive metadata diagnostics
- coverage dashboards
- inventory metadata coverage checks
- sector distribution review
- descriptive sector exposure monitoring
- missingness and lineage audits
- thin peer-group warnings

Blocked:

- alpha research
- sector-relative signals
- peer-relative transforms
- validation claims
- point-in-time historical claims
- production use
- portfolio / ML / blending / optimization routing

## Intentional Non-Changes

This review did not:

- modify the metadata CSV
- fetch data
- write SQLite tables
- create alpha candidates
- create sector-relative signals
- change universe definitions
- change gates, schemas, validation logic, or governance
- change production registration
- mutate survivor/watchlist state
- touch detector files
- route anything into portfolio, ML, blending, or optimization
