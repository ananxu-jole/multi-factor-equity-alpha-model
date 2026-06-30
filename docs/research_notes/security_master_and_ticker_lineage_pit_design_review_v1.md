# Project Underdog - Security Master and Ticker Lineage PIT Design Review v1

## SECTION 1 - Executive Summary

The security master and ticker lineage PIT implementation design is directionally strong and appropriately prioritizes identity lineage before sector, industry, size, peer reconstruction, or economic-context discovery. The design correctly recognizes that every later PIT metadata artifact depends on stable security identity, historical ticker mapping, source lineage, and blocked/eligible ticker-date diagnostics.

Scope quality is strong. The design includes `security_master_pit`, `ticker_lineage_pit`, `source_acceptance_manifest`, `metadata_source_lineage`, identity continuity diagnostics, stale/missing diagnostics, and blocked/eligible diagnostics. It explicitly excludes sector history, industry history, size history, peer reconstruction, alpha discovery, validation, production use, governance mutation, thresholds, and ML.

Readiness classification: `IMPLEMENTATION READY WITH CHANGES`.

The design is ready to proceed to a source-gate implementation subphase, but not directly to `--build-lineage`. Before lineage construction is implemented, the project should define controlled vocabularies and thresholds for source-gate statuses, confidence classes, event types, stale-age policy, blocked reason codes, and accepted manual-override handling.

Major risks:

- identity-source availability
- ticker/security ambiguity
- recycled tickers
- corporate-action incompleteness
- static source leakage
- manual repair becoming unreproducible

## SECTION 2 - Scope Review

Included scope:

- `security_master_pit`: appropriate and mandatory.
- `ticker_lineage_pit`: appropriate and mandatory.
- `source_acceptance_manifest`: appropriate and required before source use.
- `metadata_source_lineage`: appropriate and required for reproducibility.
- identity continuity diagnostics: appropriate and central to this phase.
- blocked/eligible diagnostics: appropriate and necessary for downstream gating.

Excluded scope:

- sector history: correctly excluded.
- industry history: correctly excluded.
- size history: correctly excluded.
- peer reconstruction: correctly excluded.
- alpha discovery: correctly excluded.
- validation: correctly excluded.
- production use: correctly excluded.

Scope conclusion:

The design is sufficiently narrow. It preserves the correct dependency order: identity first, classifications later, peer reconstruction last.

## SECTION 3 - Schema Review

### `security_master_pit`

Required fields:

The design matches the aligned schema template and includes identity fields, activity windows, effective dates, source lineage, confidence fields, validation flags, security event lineage, predecessor/successor identifiers, and notes.

Effective-date logic:

The design correctly separates `effective_start`, `effective_end`, `as_of_date`, `event_effective_date`, and `event_as_of_date`. This is critical for avoiding future-information leakage.

Source-lineage support:

Source, source version, source record id, metadata version, run id, collection timestamp, and record hash are present.

Confidence fields:

`identity_confidence`, `event_confidence`, `point_in_time_quality`, and `manual_override_flag` are present. The design should still define allowed values and minimum confidence floors before build-lineage implementation.

Identity continuity support:

The schema supports ticker changes, mergers, spin-offs, delistings, predecessor/successor mapping, and prior/next ticker links.

### `ticker_lineage_pit`

Required fields:

The design matches the aligned schema template and includes ticker, exchange, namespace, share class, primary listing flag, ticker effective dates, ticker status, change reason, prior/next ticker, source lineage, confidence, and validation fields.

Effective-date logic:

The design correctly treats `ticker_effective_start` as mandatory and requires `ticker_effective_end` to be populated, inferred, or explicitly open-ended.

Identity continuity support:

The design handles same ticker across non-overlapping windows and allows multiple active mappings only when share-class/exchange logic is explicit.

### `source_acceptance_manifest`

The design includes the required source-gate fields and correctly blocks rejected sources from ingestion. It should define the accepted status vocabulary exactly before implementation, for example `ACCEPTED_FOR_PIT_IMPLEMENTATION`, `DIAGNOSTIC_ONLY`, `REJECTED`, and `NEEDS_MANUAL_REVIEW`.

### `metadata_source_lineage`

The schema expectations are sufficient for auditability: source file path/reference, hash, raw/clean counts, collection timestamp, normalization rules, source confidence, manual source flag, and source-gate score summary.

Schema conclusion:

Schemas are sufficient for the source-gate and identity-lineage phase. Required changes are not structural; they are controlled vocabulary and threshold definitions.

## SECTION 4 - Source Requirement Review

Security identifiers:

Requirements are sufficient. The design correctly demands stable identifiers or auditable fields to construct `security_id`, issuer identifiers where available, share-class distinction, active/inactive status, and identity confidence.

Ticker history:

Requirements are sufficient. The design requires ticker, exchange/listing venue, namespace, validity windows, ticker changes, status, and recycled ticker handling.

Name history:

Requirements are realistic. Name history is recommended but not blocking if stable identifiers and ticker lineage are strong.

Exchange history:

Requirements are sufficient and appropriately strong. Same ticker on different exchanges must not be silently treated as one identity.

Effective dates:

Requirements are sufficient. The design allows inferred windows from snapshots but requires confidence adjustment.

Source timestamps:

Requirements are sufficient. Snapshot/known-as-of date, collection timestamp, source version, source hash, and metadata version are mandatory.

Lineage confidence:

Conceptually sufficient, but the design should specify accepted confidence values and floors before build implementation.

Reproducibility:

Requirements are sufficient. Raw source or controlled reference, normalization rules, hashes, and counts are required.

Missing or unrealistic requirements:

- The design requires all aligned schema fields, including fields some real sources may not provide. This is acceptable if missing values are explicitly represented and affected rows are downgraded or blocked, but implementation must not treat required template fields as evidence that a source fully supports every lineage dimension.
- Event lineage may be difficult for cheaper or ad hoc sources. The source gate must allow `NEEDS_MANUAL_REVIEW` or `DIAGNOSTIC_ONLY` rather than forcing unsafe acceptance.

## SECTION 5 - Identity Continuity Review

Ticker changes:

Sufficiently specified. Requires dated prior/next ticker links and aligned ticker windows.

Name changes:

Sufficient for MVP. Correctly avoids creating a new `security_id` from name change alone.

Exchange changes:

Sufficiently specified. Requires event lineage or continuity record.

Delistings:

Sufficiently specified. Ends active windows and blocks future dates absent successor lineage.

Mergers:

Mostly sufficient. Requires predecessor/successor linkage and blocks ambiguous cases. Future implementation should define merger reason codes and successor confidence levels.

Spin-offs:

Mostly sufficient. Correctly avoids assuming child entity inherits parent context. Future implementation should define event type and blocked reason codes.

Recycled tickers:

Sufficiently specified and correctly treated as separate security identities.

Missing history:

Sufficiently specified. Missing lineage is explicit and can reduce confidence or block downstream use.

Continuity conclusion:

Rules are sufficient for MVP design. Implementation should add enumerated event types, blocked reason codes, and confidence status values before lineage construction.

## SECTION 6 - Validation and Diagnostics Review

Planned checks are appropriate:

- no overlapping ticker windows
- no missing effective start dates
- no future-dated records
- ticker continuity
- security continuity
- duplicate active security records
- ambiguous ticker mappings
- recycled ticker separation
- stale record age
- blocked/eligible ticker-date status

Planned diagnostics are appropriate:

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

Missing diagnostics:

- event-type distribution report
- recycled ticker report as its own output or explicit category
- manual override dominance by date/window
- inferred-window share report
- confidence distribution report for identity and ticker mapping

Over-complexity:

No material over-complexity. The diagnostic set is appropriately strict for a foundational identity layer.

## SECTION 7 - Blocking Criteria Review

Blocking rules are sufficient to prevent unsafe downstream sector, industry, and peer reconstruction. The design correctly blocks when ticker identity is unresolved, mappings are ambiguous, effective dates are missing, source lineage is missing or rejected, static snapshots are used for historical dates, confidence is below accepted floor, event lineage is unresolved, stale records exceed policy, or manual overrides dominate unreproducibly.

Required improvement:

The design refers to accepted confidence floors and stale-age policy, but does not define them. That is acceptable for this design review, but implementation should not proceed to lineage construction until those floors/policies are explicitly established in the source-gate implementation.

## SECTION 8 - Implementation Risk Assessment

| risk | severity | assessment |
| --- | --- | --- |
| Identity source availability | Critical | A source may not provide enough stable identifiers, event lineage, and historical ticker windows to pass the gate. |
| Ticker/security ambiguity | Critical | Ambiguous mapping can contaminate every downstream sector, industry, peer, and discovery artifact. |
| Static source leakage | Critical | Current ticker/security identity cannot be backfilled into historical dates. |
| Corporate-action incompleteness | High | Mergers, spin-offs, delistings, and share-class changes may be incomplete or require manual review. |
| Recycled ticker handling | High | Reused tickers can silently map historical observations to the wrong entity if not blocked. |
| Manual override maintenance | Medium-high | Manual repairs may be necessary, but can become unreproducible or dominant if not constrained. |
| Stale snapshot handling | Medium-high | Historical snapshots can be usable, but stale windows must be measured and blocked where needed. |
| Schema/source mismatch | Medium | The aligned schema is strict; sources may require explicit unknown values and confidence downgrades. |

Highest-risk implementation component:

- ticker-to-security mapping across corporate actions and recycled ticker windows.

Highest-risk data dependency:

- accepted source availability with both historical ticker lineage and stable security identity.

Highest-risk leakage issue:

- applying current ticker/security identity to past signal dates.

Highest-risk maintenance burden:

- keeping event lineage and manual repairs reproducible over repeated updates.

## SECTION 9 - Final Readiness Classification

Classification: `IMPLEMENTATION READY WITH CHANGES`.

Rationale:

The design is correctly scoped, schema-aware, and strict enough to protect downstream PIT metadata work. It is ready for a source-gate implementation task. However, it should not proceed directly to full lineage construction until the next task defines controlled vocabularies and thresholds for source statuses, point-in-time quality, confidence levels, event types, blocked reason codes, stale-age policy, inferred-window flags, and manual override dominance.

These are implementation-readiness changes, not architectural blockers.

## SECTION 10 - Final Recommendation

1. Is the first PIT implementation phase sufficiently narrow?

Yes. It focuses on security master, ticker lineage, source acceptance, metadata source lineage, continuity diagnostics, and blocked/eligible diagnostics only.

2. Are the schemas sufficient?

Yes. The schemas are sufficient after the alignment patch. Implementation must handle missing source values explicitly through unknown/null values, confidence downgrades, or blocking rather than weakening the schema contract.

3. Are the identity continuity rules sufficient?

Yes for MVP design. Ticker changes, name changes, exchange changes, delistings, mergers, spin-offs, recycled tickers, and missing history are all addressed. Implementation should add controlled event and blocked-reason vocabularies.

4. Are the blocking rules sufficient?

Yes. The rules are strong enough to prevent unsafe downstream sector, industry, and peer reconstruction, provided confidence floors and stale-age policies are defined before lineage construction.

5. What must change before implementation?

Before full lineage construction, define source-gate status vocabulary, point-in-time quality values, identity/ticker confidence floors, event type vocabulary, blocked reason codes, inferred-window handling, stale-age policy, and manual override dominance rules.

6. Is implementation justified?

Yes. Implementation is justified as a staged identity/ticker source-gate task. It is not yet justified as a full PIT lineage build unless a source passes the gate and the controlled policies above are finalized.

7. What should the next Codex task be?

The next Codex task should be **Project Underdog - Security Master and Ticker Lineage PIT Source Gate Specification Patch v1**. It should finalize controlled vocabularies, confidence thresholds, stale-age policy, blocked reason codes, inferred-window policy, and manual override dominance rules for the identity/ticker phase. It should remain design/specification-only or source-gate-scaffold-only, and should not ingest data, build lineage artifacts, reconstruct sector or industry history, reconstruct peer groups, run discovery, run refinement, run validation, mutate governance, change thresholds, register production outputs, implement ML, or create alpha candidates.
