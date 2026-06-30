# Project Underdog - Point-in-Time Economic Metadata Source Integration Plan v1

## SECTION 1 - Executive Summary

Current readiness status: `READY FOR SOURCE INTEGRATION WITH CAUTIONS`.

The PIT economic metadata scaffold is structurally aligned with the frozen implementation specification, but the project still lacks accepted point-in-time source data. Source integration is needed because the current economic-context substrate remains `STATIC_SNAPSHOT_RESEARCH_ONLY`; static sector, industry, size, and peer labels cannot support historical peer-relative discovery without look-ahead, survivorship, ticker-lineage, and classification-drift risk.

Integration goals:

- Identify acceptable source categories before any ingestion.
- Define source acceptance and rejection criteria.
- Preserve auditability through source lineage, hashes, timestamps, taxonomy versions, and allowed-use status.
- Sequence integration so identity lineage is established before classification history and peer reconstruction.
- Keep discovery blocked until populated diagnostics and a readiness audit prove point-in-time integrity.

Major risks:

- Source availability and licensing.
- Weak security and ticker lineage.
- Static or backfilled classifications masquerading as PIT data.
- Taxonomy drift and vendor classification changes.
- Size-history false precision.
- Manual-curation leakage or unreproducibility.

This plan does not select a vendor, ingest data, integrate sources, construct metadata, reconstruct peer groups, run discovery, run refinement, run validation, modify governance, change thresholds, register production outputs, or implement ML.

## SECTION 2 - Required Metadata Domains

| domain | MVP status | rationale |
| --- | --- | --- |
| Security lineage | Mandatory | Stable `security_id` history is required before any dated classification or ticker mapping can be trusted. |
| Ticker lineage | Mandatory | Historical ticker-to-security mapping prevents current ticker identity from leaking into past signal dates. |
| Sector history | Mandatory | Sector labels must be known as of each signal date for sector-relative diagnostics and fallback grouping. |
| Industry history | Mandatory | Industry is the minimum economically meaningful peer grouping for first peer-relative discovery readiness. |
| Size history | Recommended | Date-safe size improves peer construction, but size-aware grouping must remain disabled until accepted PIT size data exists. |
| Peer-group history | Mandatory derived output | Peer groups should be reconstructed from accepted identity, classification, active universe, and optional size history. |
| Source lineage | Mandatory | Every source row must be versioned, timestamped, hashed, reproducible, and linked to source-gate acceptance. |
| Coverage diagnostics | Mandatory | Discovery readiness requires date-level active coverage, fallback, stale-age, and blocked/eligible ticker-date diagnostics. |
| Subindustry history | Deferred / recommended later | Useful after sector/industry integrity is proven; not required for MVP readiness. |
| Inventory exposure metadata | Deferred / diagnostic | Useful for future exposure audits but not required for the first PIT metadata integration phase. |
| Full fundamentals | Deferred | Outside MVP; not needed for peer-relative metadata readiness. |
| Options, fixed income, macro, alternative data | Deferred | Future-domain work; not part of equity PIT economic metadata MVP. |

Minimum MVP principle:

Security lineage, ticker lineage, sector history, industry history, source lineage, peer reconstruction inputs, and coverage diagnostics are blocking. Size history is valuable but should not block a sector/industry-only MVP if size-aware fallback is explicitly disabled.

## SECTION 3 - Source Category Framework

Preferred source categories:

- Professional point-in-time security master plus sector/industry classification history.
- Date-stamped historical vendor snapshots with stable identifiers, ticker history, source versions, and repeatable raw files.
- Exchange/reference-data identity sources paired with separate PIT classification history, if linkage is auditable.

Acceptable source categories:

- Repeatable historical snapshots from controlled files, if source snapshot dates, hashes, identifiers, and effective windows can be reconstructed without look-ahead.
- Internally reconstructed metadata using archived date-stamped inputs, if reconstruction logic is deterministic and fully auditable.
- Manual event-lineage corrections for unresolved ticker/security cases, if they are explicitly flagged, reviewed, and limited to identity repair rather than alpha-conditioning.

Discouraged source categories:

- Current profile APIs used as current coverage diagnostics only.
- Manual static CSVs without historical snapshot dates.
- Classification sources that provide sector and industry but weak security identifiers.
- Sources with incomplete update history, unstable schemas, or high manual burden.

Unacceptable source categories:

- Static current snapshots used to populate historical dates.
- Sources with no effective dates, no snapshot dates, and no reproducible raw history.
- Sources with ticker-only identity and no exchange/share-class/corporate-action resolution.
- Sources whose licensing or usage terms prevent controlled research retention and reproducibility.
- Sources that cannot be audited by date against the dynamic research universe.

No specific vendor is selected by this plan.

## SECTION 4 - Source Acceptance Criteria

Minimum acceptance criteria:

| criterion | required expectation |
| --- | --- |
| Effective dates | Must provide `effective_start`, preferably `effective_end`, or repeatable dated snapshots from which windows can be inferred. |
| As-of / snapshot dates | Must provide source snapshot date or known-as-of date so joins can be evaluated relative to `signal_date`. |
| Historical depth | Must cover the research lookback needed for future discovery; partial coverage must be explicitly blocked by date. |
| Reproducibility | Must preserve raw files or controlled references, source versions, hashes, normalization rules, and run manifests. |
| Identifier stability | Must provide stable identifiers or enough fields to build `security_id`, ticker, exchange, and share-class lineage. |
| Coverage | Preferred minimum: 95%+ active ticker-date coverage by date for mandatory domains. Acceptable provisional floor: 80-95% with blocked-date diagnostics. Below 80% should be diagnostic-only unless scope is explicitly narrowed. |
| Lineage transparency | Must record source, source version, source record id when available, source file hash, collection timestamp, metadata version, and allowed use. |
| Update process | Must have a repeatable update process or controlled historical archive process. |
| Auditability | Must support date-level coverage, stale-age, fallback, unresolved ticker/security, duplicate active record, and blocked/eligible diagnostics. |
| PIT quality label | Must be classifiable as `POINT_IN_TIME` or acceptable `DATE_STAMPED_SNAPSHOT` for future discovery readiness. `STATIC_SNAPSHOT` remains diagnostic-only. |

Scoring expectations:

- A source scoring `0` on PIT integrity or identifier quality fails the gate.
- A source scoring below `2` on historical depth or coverage cannot support discovery readiness without a documented block policy.
- A source with high leakage risk may be used only for diagnostics.
- Manual intervention must be reviewable, bounded, and recorded in lineage fields.

Acceptance output:

Every evaluated source must produce a `source_acceptance_manifest` entry with pass/fail status, source-gate scores, allowed use, rejection reason if applicable, manual-review flag, usage notes, review timestamp, and reviewer notes.

## SECTION 5 - Source Rejection Criteria

Blockers:

- Static snapshots only.
- Missing effective dates and missing source snapshot/as-of dates.
- Unclear or unverifiable lineage.
- Unreproducible historical files or transformations.
- Ticker-only identity with unresolved corporate actions, ticker changes, delistings, mergers, spin-offs, or share-class changes.
- Excessive manual intervention that cannot be repeated or audited.
- Coverage instability that cannot be measured by date.
- Historical depth insufficient for the future discovery period.
- Licensing, retention, or usage restrictions that prevent reproducible research artifacts.
- Classification history that silently backfills current taxonomy or current sector/industry labels.
- Taxonomy version changes that cannot be identified or flagged.
- Inability to produce blocked/eligible ticker-date diagnostics.

Rejection classifications:

- `REJECTED`: cannot be used in the PIT metadata layer.
- `DIAGNOSTIC_ONLY`: may be used for current/static context diagnostics but not discovery.
- `NEEDS_MANUAL_REVIEW`: cannot proceed until unresolved lineage, licensing, coverage, or PIT-quality questions are closed.

## SECTION 6 - Integration Sequencing

Stage 1: Security master and ticker lineage.

- Evaluate identity sources first.
- Establish `security_master_pit` and `ticker_lineage_pit` source suitability before classification integration.
- Confirm corporate-action and ticker-change support, or define blocked unresolved cases.
- Do not ingest into PIT tables in the planning phase.

Stage 2: Sector and industry history.

- Evaluate classification history sources only after identity linkage is credible.
- Require effective dates or date-stamped snapshots.
- Require taxonomy version tracking or explicit missing-taxonomy flags.
- Confirm sector and industry coverage by active ticker-date.

Stage 3: Size history.

- Evaluate market-cap or size history separately.
- Keep `size_bucket_history_pit` recommended, not blocking.
- Disable size-aware peer fallback until accepted size history exists.

Stage 4: Peer-group reconstruction inputs.

- Define peer construction inputs from accepted identity and classification history.
- Confirm active universe membership by signal date.
- Define minimum peer-group size, fallback hierarchy, and blocked rules.
- Do not reconstruct peer groups until a separate implementation task.

Stage 5: Diagnostics and readiness review.

- Populate coverage, stale-age, fallback dominance, lineage, blocked/eligible ticker-date, and taxonomy diagnostics in a future implementation phase.
- Run a review-only readiness audit after diagnostics are populated.
- Only a successful readiness audit can consider `POINT_IN_TIME_DISCOVERY_READY`.

## SECTION 7 - Lineage and Audit Requirements

Source acceptance manifest:

- `source_gate_run_id`
- source name, type, version, and snapshot date
- source file hash or controlled source reference
- PIT integrity, coverage, historical depth, identifier quality, update feasibility, source stability, implementation complexity, cost/manual burden, and leakage risk scores
- source-gate status
- allowed use
- rejection reason
- manual-review flag
- licensing/manual-use notes
- review timestamp and reviewer notes

Ingestion lineage for future implementation:

- source file path or source reference
- source version
- source snapshot date
- collection timestamp
- raw and normalized record hashes
- normalization rules
- run id
- metadata version
- row counts before and after cleaning
- manual override flags

Taxonomy version tracking:

- classification system
- taxonomy version
- provider taxonomy id
- taxonomy effective date
- taxonomy change flag
- taxonomy change reason
- missing taxonomy flag where version data is absent

Stale-age reporting:

- stale record count and share
- stale-age min, median, p75, p90, and max
- stale-age by source and metadata domain
- stale record flags at the ticker-date level

Fallback reporting:

- fallback level
- fallback reason
- ticker-date count and share
- broad fallback share
- fallback dominance flag
- dominant fallback level by date/window

Blocked/eligible reporting:

- total ticker-dates
- eligible ticker-dates
- blocked ticker-dates
- blocked reason counts and shares
- unresolved ticker/security counts
- thin peer-group counts
- discovery eligibility flag in `pit_economic_context_panel`

## SECTION 8 - Risk Assessment

| risk | severity | assessment |
| --- | --- | --- |
| Source availability risk | Critical | The project may not have access to a source with both historical classifications and usable identity lineage. |
| Identifier mismatch risk | Critical | Incorrect ticker/security mapping can corrupt every downstream peer and classification join. |
| Static look-ahead risk | Critical | Static labels cannot populate historical dates under any discovery-ready interpretation. |
| Taxonomy drift risk | High | Vendor taxonomy changes can look like issuer classification changes unless versioned and flagged. |
| Security event lineage risk | High | Mergers, spin-offs, delistings, share-class changes, and ticker changes may require manual review and blocked rows. |
| Maintenance burden | Medium-high | PIT metadata requires repeatable updates, hashes, lineage, and diagnostics, not one-time enrichment. |
| Manual-curation risk | Medium-high | Manual repairs can improve coverage but may introduce leakage or unreproducibility if not tightly bounded. |
| Size-history false precision | Medium | Size-aware fallback can create false confidence unless size data is date-safe. |
| Future leakage risk | Medium | Future source integration must ensure `as_of_date <= signal_date` and fail closed on missing dates. |

Highest-risk item: identity lineage quality. Without stable security and ticker lineage, even a strong classification source cannot safely support historical discovery.

## SECTION 9 - Discovery Readiness Path

Current state:

- `READY FOR SOURCE INTEGRATION WITH CAUTIONS`
- Schema scaffold aligned.
- No source accepted.
- No metadata ingested.
- No PIT panel constructed.
- Discovery remains blocked.

Gated path to `POINT_IN_TIME_DISCOVERY_READY`:

1. Source acceptance framework implemented.
2. Candidate sources evaluated through source-gate scoring.
3. At least one mandatory-domain source accepted for identity lineage and classification history, or an accepted multi-source combination is documented.
4. Research-only PIT ingestion/construction task approved separately.
5. `security_master_pit`, `ticker_lineage_pit`, `sector_industry_history_pit`, `metadata_source_lineage`, and diagnostics populated from accepted sources.
6. Peer reconstruction task approved separately and `peer_group_history_pit` plus `pit_economic_context_panel` produced.
7. Coverage, stale-age, fallback dominance, taxonomy, lineage, and blocked/eligible diagnostics populated.
8. Post-implementation readiness audit performed.
9. Only if the audit confirms PIT integrity can `POINT_IN_TIME_DISCOVERY_READY` be considered.

Discovery remains blocked until the final readiness audit. This plan authorizes no candidate design and no discovery execution.

## SECTION 10 - Final Recommendation

1. What should the first integrated metadata domain be?

Security master and ticker lineage should be first. Identity lineage is the foundation; sector/industry history should not be integrated before historical ticker/security continuity is credible.

2. What source categories are preferred?

Preferred categories are professional PIT security-master/classification sources, date-stamped historical vendor snapshots with stable identifiers, and exchange/reference identity sources paired with auditable PIT classification history.

3. What source categories should be rejected?

Reject static snapshots for historical use, unreproducible manual files, sources without effective or snapshot dates, sources with ticker-only identity and unresolved events, and sources whose usage terms prevent reproducible research retention.

4. What is the largest source-integration risk?

The largest risk is identifier mismatch across time. A flawed ticker/security lineage layer would contaminate classification history, peer-group reconstruction, diagnostics, and any later discovery panel.

5. What should remain deferred?

Defer size-aware peer fallback until date-safe size history passes the source gate. Also defer subindustry peers, full fundamentals, options, fixed income, macro, alternative data, ML, production integration, portfolio construction, alpha candidates, discovery, refinement, and validation.

6. What should the next Codex task be?

The next Codex task should be **Project Underdog - Point-in-Time Economic Metadata Source Acceptance Framework v1**. It should implement source-gate scoring, source acceptance manifest writing, source-gate validation, and source diagnostics only. It should not ingest metadata into PIT tables, integrate sources into historical panels, reconstruct sector or industry history, reconstruct peer groups, run discovery, run refinement, run validation, mutate governance, change thresholds, register production outputs, implement ML, or create alpha candidates.
