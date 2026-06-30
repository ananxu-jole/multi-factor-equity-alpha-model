# Project Underdog - Security Master and Ticker Lineage PIT Policy and Controlled Vocabulary Design v1

## SECTION 1 - Executive Summary

The security master and ticker lineage PIT phase needs a frozen policy and controlled vocabulary layer before implementation because the aligned schemas deliberately require strict fields, but real identity sources may provide incomplete, inferred, conflicting, or stale lineage. Without controlled values, future implementation could accept ambiguous sources, silently downgrade point-in-time quality, or inconsistently block ticker-date rows.

This design removes ambiguity around:

- source acceptance status
- point-in-time quality
- confidence tiers and floors
- security event types
- blocked reason codes
- inferred window handling
- stale-age thresholds
- manual override usage

It reduces implementation risk by making identity lineage fail closed. Sources and rows that are reproducible, dated, and high-confidence can proceed to research-only lineage construction. Sources and rows that are static, ambiguous, stale beyond policy, or manually unresolved remain diagnostic-only or blocked from downstream sector, industry, peer, and discovery use.

This is design-only. No code, source integration, metadata construction, discovery, validation, governance mutation, threshold change, production registration, ML, or alpha candidate creation was performed.

## SECTION 2 - Source Status Vocabulary

| value | definition | allowed use | blocking impact |
| --- | --- | --- | --- |
| `accepted` | Source passes identity/ticker source gate for the declared domain and may be used in research-only PIT lineage construction. | May feed `security_master_pit`, `ticker_lineage_pit`, and `metadata_source_lineage` in a separately approved build task. | Not blocking, but row-level validation can still block specific records. |
| `conditional` | Source passes only with documented limits such as partial dates, inferred windows, partial coverage, or manual-review dependencies. | May be used only for the approved subset/date range/domain with explicit blocked diagnostics. | Blocks unsupported domains, date ranges, and rows outside accepted conditions. |
| `manual_review_required` | Source has unresolved lineage, licensing, coverage, PIT-quality, or identifier issues. | Source-gate diagnostics only. No build-lineage use until review closes. | Blocks lineage construction. |
| `diagnostic_only` | Source is useful for inspection or static coverage diagnostics but not safe for PIT construction. | Diagnostic reports only. | Blocks PIT lineage construction and downstream reconstruction. |
| `rejected` | Source fails a blocking source-gate requirement. | May be retained only in rejection manifest. | Blocks all use except audit record. |
| `deprecated` | Previously accepted source version is superseded or withdrawn. | Historical reproducibility only; no new builds unless explicitly reaccepted. | Blocks new lineage construction from that source version. |

Required source-gate behavior:

- `accepted` is the only status that permits full identity/ticker lineage construction.
- `conditional` permits construction only where the condition is machine-readable and fail-closed.
- `manual_review_required`, `diagnostic_only`, `rejected`, and `deprecated` block new PIT lineage construction.

## SECTION 3 - PIT Quality Vocabulary

| value | definition | downstream eligibility | discovery blocking rule |
| --- | --- | --- | --- |
| `point_in_time_verified` | Record has effective/as-of dates, accepted source lineage, reproducible raw/source reference, and sufficient confidence. | Eligible for downstream sector/industry/peer reconstruction if other checks pass. | Not blocking. |
| `date_stamped_snapshot` | Record comes from a dated source snapshot; windows may be inferred from snapshots but are auditable. | Eligible only if inferred-window policy and stale-age policy pass. | Warning unless stale, ambiguous, or low-confidence. |
| `inferred_window` | Effective window inferred from dated snapshots or adjacent source records rather than explicit effective dates. | Eligible only with confidence penalty, lineage notes, and inferred-window flag. | Blocking when inferred span exceeds policy or continuity is ambiguous. |
| `static_snapshot_only` | Record reflects current/static metadata without historical as-of integrity. | Diagnostic only. | Always blocks historical PIT lineage construction. |
| `unresolved` | Record lacks enough evidence to determine identity, dates, source lineage, or event continuity. | Not eligible. | Always blocks downstream use. |
| `blocked` | Record is explicitly excluded by validation or policy. | Not eligible. | Always blocks downstream use. |

Discovery blocking principle:

No row with `static_snapshot_only`, `unresolved`, or `blocked` PIT quality may support sector/industry/peer reconstruction or future discovery panels. `date_stamped_snapshot` and `inferred_window` rows require additional diagnostics and can be blocked by stale-age, confidence, or continuity rules.

## SECTION 4 - Confidence Policy

Confidence tiers:

| tier | numeric band | definition | downstream use |
| --- | ---: | --- | --- |
| `high` | `0.90-1.00` | Stable source identifier, dated lineage, no conflict, no manual dependency. | Eligible if other checks pass. |
| `medium` | `0.70-0.8999` | Dated and reproducible, but inferred, partially manual, or missing non-critical fields. | Eligible with warning and diagnostics. |
| `low` | `0.50-0.6999` | Material uncertainty in dates, event lineage, identifier continuity, or source support. | Diagnostic-only unless manually elevated through review. |
| `blocked` | `<0.50` | Insufficient confidence for PIT use. | Blocks downstream use. |
| `unknown` | null/unscored | Confidence cannot be assigned. | Blocks downstream use until scored. |

Confidence floors:

- Minimum `identity_confidence` for downstream eligibility: `0.70`.
- Minimum `ticker_mapping_confidence` for downstream eligibility: `0.70`.
- Minimum `event_confidence` for event-dependent continuity: `0.70`.
- Any confidence below `0.70` should set blocked reason `low_confidence_lineage` unless a review-specific exception is documented.

Assignment rules:

- Start from source-gate identifier quality and PIT integrity scores.
- Penalize inferred windows, missing event dates, manual overrides, stale snapshots, ambiguous exchange/share-class fields, and unresolved predecessor/successor links.
- Raise confidence only with documented source evidence, never with downstream alpha results.

Conflict resolution:

- If multiple sources conflict, use the record with higher accepted PIT quality and stronger source lineage.
- If confidence differs between identity, ticker mapping, and event lineage, the row inherits the lowest relevant confidence for downstream eligibility.
- If two accepted sources conflict with similar confidence, mark `manual_review_required` or block affected ticker-dates.

## SECTION 5 - Security Event Type Vocabulary

| event type | required fields | effective-date handling | lineage impact | blocking impact |
| --- | --- | --- | --- | --- |
| `ticker_change` | prior ticker, next ticker, event effective date, event as-of date, security id | End prior ticker window and start next ticker window. | Same `security_id` unless source indicates new entity. | Block if either date or successor ticker is unresolved. |
| `name_change` | prior name or notes, event effective/as-of dates, security id | Preserve security window unless source indicates entity change. | No new `security_id` by name change alone. | Warning unless name ambiguity affects identity. |
| `exchange_change` | prior exchange, next exchange, ticker, dates, security id | End old exchange/ticker window and open new exchange/ticker window. | Same `security_id` if continuity is documented. | Block if same ticker/exchange mapping becomes ambiguous. |
| `delisting` | ticker, exchange, event dates, security id, ticker status | End active security and ticker windows. | Historical mapping preserved; future rows blocked absent successor. | Block post-delisting ticker-dates unless successor lineage exists. |
| `merger` | predecessor id, successor id, event dates, event confidence | End predecessor window; link successor. | Creates predecessor/successor lineage. | Block if successor or dates are unresolved. |
| `acquisition` | acquired security id, acquirer/successor id, event dates | End acquired security if no independent listing remains. | Link acquired to acquirer/successor where source supports it. | Block if continued identity is ambiguous. |
| `spin_off` | parent id, child/successor id, event dates, ticker(s) | Create/activate child security window; parent may continue. | Separate parent and child identities. | Block child/parent affected rows if mapping is unresolved. |
| `split_off` | parent id, split-off id, event dates, ticker(s) | Create separate identity window for split-off entity. | Do not inherit parent identity automatically. | Block if source cannot distinguish identities. |
| `relisting` | prior ticker/exchange/status, new ticker/exchange/status, dates | End inactive/delisted window and open relisted window if same entity is proven. | Same `security_id` only with source evidence. | Block if same-entity continuity is not proven. |
| `ticker_reuse` | reused ticker, old security id, new security id, non-overlapping dates | Separate windows across different `security_id`s. | Explicitly prevents current identity backfill. | Block if reuse windows overlap or old/new identity is unresolved. |
| `unknown_event` | event notes, source, available dates, affected ticker/security | No automatic window change unless source supports it. | Diagnostic placeholder until resolved. | Blocks affected ticker-dates. |

## SECTION 6 - Blocked Reason Vocabulary

| blocked reason | trigger condition | severity | downstream impact |
| --- | --- | --- | --- |
| `missing_effective_date` | Required effective start or ticker effective start is missing. | Critical | Blocks row and downstream ticker-date. |
| `missing_as_of_date` | As-of/source snapshot date is missing for a historical row. | Critical | Blocks historical PIT use. |
| `future_dated_record` | As-of/source snapshot date is after signal date. | Critical | Blocks ticker-date. |
| `overlapping_ticker_window` | Same ticker/security/exchange has conflicting active windows. | Critical | Blocks affected windows. |
| `duplicate_active_mapping` | Ticker/date maps to multiple active securities without share-class/exchange clarity. | Critical | Blocks ticker-date. |
| `unresolved_security_identity` | Stable security identity cannot be determined. | Critical | Blocks row and downstream reconstruction. |
| `recycled_ticker_ambiguity` | Ticker reuse cannot be separated into distinct security ids/windows. | Critical | Blocks affected ticker windows. |
| `low_confidence_lineage` | Any required confidence falls below floor. | High | Blocks unless manual review explicitly reclassifies. |
| `stale_record` | Stale age exceeds blocking threshold. | High | Blocks ticker-date or date window. |
| `source_rejected` | Source status is rejected, deprecated, diagnostic-only, or not accepted for PIT use. | Critical | Blocks all rows from source. |
| `manual_review_required` | Source or row has unresolved manual-review flag. | High | Blocks until review closed. |
| `static_snapshot_only` | Source/row is current snapshot only. | Critical | Blocks historical PIT use. |
| `unresolved_event_lineage` | Event-dependent continuity lacks required predecessor/successor/date evidence. | High | Blocks affected ticker-date range. |
| `manual_override_dominance` | Manual overrides exceed dominance threshold in a source/date/window. | Medium-high | Blocks window pending review. |
| `unsupported_domain` | Source is conditionally accepted but row falls outside supported domain/date range. | High | Blocks row. |

Severity interpretation:

- Critical: always blocks.
- High: blocks unless a documented review-specific exception reclassifies the row.
- Medium-high: blocks the affected window pending review.

## SECTION 7 - Inferred Window Policy

Allowed inferred windows:

- Source provides repeatable dated snapshots.
- Adjacent snapshots support an inferred start/end window.
- Source lineage, snapshot dates, hashes, and normalization rules are recorded.
- No conflicting identity/ticker evidence exists.
- Confidence after inference penalty remains at least `0.70`.

Blocked inferred windows:

- Inference uses static current metadata.
- Snapshot cadence is unknown or unreproducible.
- Window spans beyond stale blocking threshold without confirming evidence.
- Inference crosses ticker change, exchange change, merger, delisting, spin-off, split-off, or ticker reuse event without event lineage.
- Confidence after penalty falls below `0.70`.

Required confidence penalty:

- Deduct at least `0.10` from identity or ticker confidence for inferred windows.
- Deduct at least `0.20` when only sparse snapshots support the window.
- Deduct more or block when inference crosses event-sensitive periods.

Required source lineage:

- source
- source version
- snapshot date(s)
- source file hash or controlled reference
- normalization rule
- inferred-window method
- run id and metadata version

Required review flags:

- `point_in_time_quality = inferred_window`
- manual review flag if inference crosses any corporate action or ticker-change boundary
- blocked reason if confidence or stale policy fails

## SECTION 8 - Stale-Age Policy

Stale-age calculation:

- For explicit effective-date records: `signal_date - as_of_date` where `as_of_date` is the known date of the record.
- For dated snapshots: `signal_date - source_snapshot_date`.
- For inferred windows: use the most recent supporting snapshot/as-of date known before or on `signal_date`.
- Future-dated records are invalid and receive `future_dated_record`.

Thresholds:

| threshold | stale age | action |
| --- | ---: | --- |
| Fresh | `0-365` days | Eligible if other checks pass. |
| Warning | `366-730` days | Eligible with `stale_warning` diagnostic if confidence remains above floor. |
| High stale | `731-1095` days | Manual review required for event-sensitive rows; otherwise warning with confidence penalty. |
| Blocking | `>1095` days | Block affected ticker-date unless source explicitly declares durable open-ended identity and review approves. |

Confidence penalties:

- Warning stale: deduct at least `0.05`.
- High stale: deduct at least `0.10`.
- Blocking stale: block unless approved review exception exists.

Reporting requirements:

- stale record count and share
- stale-age min, median, p75, p90, and max
- stale-age by source
- stale-age by metadata domain
- blocked ticker-date count from stale policy

## SECTION 9 - Manual Override Policy

Allowed manual overrides:

- Correcting known ticker/security identity breaks when source evidence is documented.
- Resolving ticker reuse with dated source references.
- Linking predecessor/successor security ids for corporate actions.
- Closing or opening effective windows when a source record is incomplete but external dated evidence is retained.

Manual overrides are not allowed:

- To improve alpha results.
- To fill sector, industry, size, or peer labels in this phase.
- To backfill current identity into historical dates without dated evidence.
- To bypass rejected source status.

Required fields:

- manual override flag
- reviewer or created-by field
- review timestamp
- source/reference used
- rationale
- affected ticker/security/date range
- prior value
- override value
- confidence after override
- expiration or next review date

Required rationale:

Manual overrides must cite dated evidence and explain why automated source lineage was insufficient.

Dominance rules:

- If manual overrides exceed `5%` of ticker-date rows in a source/date window, issue warning.
- If manual overrides exceed `10%`, block the window pending review.
- If manual overrides are concentrated in one event type or ticker group, require event-specific review even below `5%`.

Audit requirements:

- Every override must be reproducible from retained evidence.
- Override counts must be reported by source, date window, event type, and reviewer.
- Overrides must not overwrite raw source records; they should be layered as reviewed corrections.

Expiration/review policy:

- Overrides should be reviewed at least once per metadata source refresh.
- Overrides tied to unresolved source defects expire when a corrected source version becomes available.
- Overrides without reproducible evidence expire immediately and must block affected rows.

## SECTION 10 - Final Recommendation

1. Are controlled vocabularies sufficiently defined for implementation?

Yes. Source status, PIT quality, confidence tiers, event types, blocked reasons, inferred-window policy, stale-age policy, and manual override policy are now sufficiently defined for the first source-gate implementation phase.

2. Which values are blocking?

Blocking source statuses: `manual_review_required`, `diagnostic_only`, `rejected`, and `deprecated`; `conditional` blocks unsupported domains/date ranges.

Blocking PIT quality values: `static_snapshot_only`, `unresolved`, and `blocked`; `inferred_window` blocks when stale, ambiguous, or below confidence floor.

Blocking reasons include `missing_effective_date`, `missing_as_of_date`, `future_dated_record`, `overlapping_ticker_window`, `duplicate_active_mapping`, `unresolved_security_identity`, `recycled_ticker_ambiguity`, `low_confidence_lineage`, `stale_record`, `source_rejected`, `manual_review_required`, `static_snapshot_only`, `unresolved_event_lineage`, `manual_override_dominance`, and `unsupported_domain`.

3. Which values are warning-only?

Warning-only values include `date_stamped_snapshot` when fresh and unambiguous, `inferred_window` when confidence remains above floor and stale policy passes, medium confidence rows, warning stale-age rows, and manual override dominance below the warning threshold.

4. What policies must be enforced in the first implementation?

The first implementation must enforce source status blocking, PIT quality eligibility, confidence floors, event type validation, blocked reason assignment, inferred-window confidence penalties, stale-age thresholds, manual override dominance, and fail-closed ticker-date eligibility.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Security Master and Ticker Lineage PIT Source Gate Scaffold v1**. It should implement the source-gate policy scaffold, controlled vocabulary artifacts, manifest validation, and dry-run/list/validate behavior for identity and ticker lineage sources only. It should not ingest metadata, build lineage artifacts, reconstruct sector or industry history, reconstruct peer groups, run discovery, run validation, mutate governance, change thresholds, register production outputs, implement ML, or create alpha candidates.
