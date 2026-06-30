# Project Underdog - Source-Gate Semantic Validation Design v1

## SECTION 1 - Executive Summary

Semantic validation is needed because schema validation can confirm that a source acceptance manifest has the right columns, legal enum values, and numeric score ranges, but it cannot determine whether the source is actually eligible for downstream use. A row can be syntactically valid while still being unsafe: for example, a source could be marked `accepted` while also requiring manual review, carrying a blocking PIT quality class, lacking a rejection rationale, or claiming a usage level that exceeds its source status.

The risk of missing semantic controls is direct historical-integrity contamination. A weak or ambiguous identity source could enter lineage construction, then leak into sector history, industry history, peer reconstruction, economic-context panels, and eventually discovery. That would allow point-in-time work to inherit the same current-snapshot and survivorship risks that the PIT infrastructure is being built to prevent.

Relationship to schema validation:

- Schema validation checks structure.
- Semantic validation checks meaning.
- Both are required before real source integration.

Relationship to policy validation:

- Policy validation confirms controlled vocabularies exist and remain aligned with approved design.
- Semantic validation enforces how those vocabulary values interact.
- Policy values without semantic enforcement are advisory; semantic validation makes them operational.

This design is review/design only. No code, ingestion, source loading, metadata construction, lineage construction, reconstruction, discovery, refinement, validation, governance mutation, threshold change, production registration, or ML was performed.

## SECTION 2 - Source Status Semantics

| source status | meaning | downstream eligibility | blocking behavior | review requirements | audit requirements |
| --- | --- | --- | --- | --- | --- |
| `accepted` | Source passes the source gate for the declared domain, source version, and date range. | Eligible for the explicitly allowed use, subject to row-level PIT quality, confidence, stale, inferred-window, and continuity checks. | Not blocking by status alone. Blocks if paired with `manual_review_required = True`, blocking PIT quality, insufficient scores, or unsupported use. | Requires completed source-gate review, non-empty review timestamp, source hash/reference, and reviewer notes. | Must retain source version, snapshot date, source hash/reference, score summary, usage scope, and review notes. |
| `conditional` | Source passes only for a constrained subset, date range, domain, or use case. | Eligible only inside machine-readable conditions. Outside conditions, source is blocked. | Partially blocking. Unsupported rows/domains/date ranges receive `unsupported_domain` or a more specific blocked reason. | Requires condition statement, supported domain/date fields, blocked diagnostics for excluded use, and periodic review. | Must record condition rationale, condition scope, review timestamp, and decision history. |
| `rejected` | Source fails a blocking source-gate requirement. | No downstream use. Audit record only. | Always blocks source loading, lineage construction, PIT table construction, reconstruction, discovery support, and production use. | Requires explicit rejection rationale and reviewer notes. | Must retain rejection reason, failed requirements, source id/version/snapshot/hash if available, and review timestamp. |
| `deprecated` | Source or source version was previously usable or inspected but is superseded, withdrawn, or no longer eligible for new builds. | Historical reproducibility only. No new construction from deprecated source versions. | Blocks new source loading and new lineage construction. Existing derived artifacts require provenance retention and migration review. | Requires deprecation rationale, replacement source/version if any, and effective deprecation date. | Must retain prior acceptance state, deprecation reason, replacement mapping if any, and transition history. |
| `manual_review_required` | Source has unresolved lineage, licensing, PIT-quality, coverage, identifier, or usage issues. | Source-gate diagnostics only. | Blocks all construction and downstream use until review closes. | Requires open review item, trigger reason, owner/reviewer, and expiration or next review date. | Must retain review trigger, impacted domains/date ranges, reviewer notes, and final disposition. |
| `diagnostic_only` | Source is useful for inspection or coverage diagnostics but not safe for PIT construction. | Diagnostics only. | Blocks lineage construction, PIT table construction, reconstruction, discovery support, and production use. | Requires explanation of why source is diagnostic-only. | Must retain diagnostic purpose, limitations, and blocked downstream use. |

Mandatory semantic controls:

- `accepted` cannot coexist with `manual_review_required = True`.
- `accepted` cannot coexist with `point_in_time_quality` in `static_snapshot_only`, `unresolved`, or `blocked` if PIT quality is present.
- `accepted` requires allowed use no broader than its reviewed scope.
- `conditional` requires machine-readable conditions before it can support any construction.
- `rejected`, `deprecated`, `manual_review_required`, and `diagnostic_only` always block construction.

## SECTION 3 - Allowed Use Semantics

Canonical allowed-use categories:

| allowed use | permitted actions | prohibited actions | escalation path | interaction with source status |
| --- | --- | --- | --- | --- |
| `diagnostics_only` | Coverage inspection, source profiling, rejection reporting, manual review triage. | Lineage construction, PIT table construction, reconstruction, discovery support. | Escalate to `lineage_only` only after source status becomes `accepted` or valid `conditional`. | Compatible with any status except it remains non-construction use. Required for `rejected`, `diagnostic_only`, and unresolved manual review. |
| `lineage_only` | Security master and ticker lineage construction for approved identity/ticker scope. | Sector/industry/size reconstruction, peer reconstruction, discovery support. | Escalate to reconstruction only after lineage diagnostics pass in a separate review. | Requires `accepted` or in-scope `conditional`. |
| `reconstruction_allowed` | May support later sector, industry, size, or peer reconstruction after identity/ticker lineage is certified. | Direct discovery support without a readiness review. | Escalate to `discovery_allowed` only after PIT diagnostics and readiness review. | Requires accepted source, lineage certification, and no blocking diagnostics. |
| `discovery_allowed` | May support research-only discovery panels after PIT readiness is certified. | Production routing, governance mutation, validation shortcut, ML use. | Escalate to production only through separate governance path; out of scope here. | Not available in the current source-gate phase. Must remain blocked until future readiness review. |
| `research_only` | Research-only diagnostic or construction use, depending on paired status and use subtype. | Production registration, trading use, governance mutation. | Must be narrowed to a concrete action category before source acceptance. | This is an umbrella label, not sufficient alone for eligibility decisions. |
| `blocked` | Audit retention only. | All source loading, construction, reconstruction, discovery, production, and ML use. | Requires new source-gate review to leave blocked state. | Required for rejected or unresolved sources. |

Mapping from current scaffold labels:

- `identity_ticker_lineage` maps to canonical `lineage_only`.
- `diagnostic_only` maps to canonical `diagnostics_only`.
- `rejected` maps to canonical `blocked`.
- `manual_review_only` maps to canonical `diagnostics_only` plus source-status block.
- `deprecated_no_new_builds` maps to canonical `blocked` for new construction and historical audit only.

Required semantic behavior:

- Source status controls whether any use is possible.
- Allowed use controls what type of use is possible.
- The effective permission is the strictest intersection of source status, allowed use, PIT quality, confidence, and review state.

## SECTION 4 - Conditional Source Rules

Conditional sources may be used only when all of the following are true:

- The condition is machine-readable.
- The supported domain is explicit, such as identity only, ticker lineage only, exchange history only, or diagnostics only.
- The supported date range is explicit.
- The supported security universe or exchange namespace is explicit if coverage is partial.
- The allowed use is no broader than `lineage_only` in this PIT identity phase.
- Confidence after all penalties remains at least `0.70`.
- PIT quality is not `static_snapshot_only`, `unresolved`, or `blocked`.
- Manual review is not open for the affected use.
- Unsupported rows produce blocked diagnostics rather than silent omission.

Required safeguards:

- explicit condition fields or condition document reference
- blocked reason `unsupported_domain` for out-of-scope rows
- stale-age diagnostics
- inferred-window diagnostics when windows are inferred
- coverage diagnostics for supported versus unsupported scope
- review timestamp and reviewer notes

Required confidence levels:

- Identity/ticker use requires minimum confidence tier `medium`.
- Any confidence equivalent below `0.70` blocks the affected source/date/domain.
- Conditional use with inferred windows must include the inference confidence penalty.

Required review steps:

- initial source-gate review
- condition-scope review
- diagnostic review after first build attempt, before downstream reconstruction
- re-review if source version, coverage, taxonomy, or data structure changes

Downstream restrictions:

- Conditional sources cannot directly support sector history, industry history, peer reconstruction, or discovery.
- They may support identity/ticker lineage only inside their approved scope.
- Any later reconstruction use requires a separate readiness review.

## SECTION 5 - Rejected Source Rules

Required rejection rationale:

- Every `rejected` source row must have non-empty `rejection_reason`.
- The reason must map to a controlled blocked reason where applicable, such as `static_snapshot_only`, `missing_effective_date`, `missing_as_of_date`, `source_rejected`, `low_confidence_lineage`, or `unresolved_security_identity`.

Required documentation:

- source name
- source type
- source version
- source snapshot date if available
- source hash or controlled reference if available
- failed source-gate requirements
- reviewer notes
- review timestamp

Reuse restrictions:

- Rejected sources cannot be used for lineage construction, PIT table construction, reconstruction, discovery support, production registration, or ML.
- Rejected sources may remain in diagnostics and rejection inventory only.
- Derived artifacts cannot cite rejected sources as accepted lineage.

Override conditions:

- A rejected source can only leave rejected state through a new source-gate review.
- The new review must reference a corrected source version, corrected source lineage, or resolved licensing/coverage issue.
- Manual overrides cannot bypass `rejected` status.

Audit requirements:

- retain rejected-source inventory
- retain failed checks
- retain transition history if the source is later reconsidered
- report rejected-source count and rejection reasons by source type

## SECTION 6 - Manual Review Semantics

Manual review is triggered when:

- source status is `manual_review_required`
- `manual_review_required = True`
- accepted and blocking values conflict
- source has missing effective/as-of dates
- source has ambiguous identifier lineage
- source has unresolved ticker reuse
- source has conflicting source versions
- source has static snapshot risk
- source has licensing or reproducibility ambiguity
- manual override dominance exceeds thresholds

Who or what can clear review:

- A future implementation may encode reviewer identity or review authority, but the semantic requirement is that clearance must be explicit, dated, and auditable.
- Automated checks may recommend clearance only when all blocking checks pass.
- Manual review cannot be cleared by downstream alpha performance, discovery results, or validation outcomes.

Downstream blocking behavior:

- Open manual review blocks lineage construction.
- Open manual review blocks PIT table construction.
- Open manual review blocks sector/industry/peer reconstruction.
- Open manual review blocks discovery support.

Expiration policy:

- Manual review decisions must expire when source version changes.
- Manual review decisions must expire when source coverage changes materially.
- Manual review decisions must expire when a corrected source replaces a reviewed workaround.
- Open review items without review timestamp or owner should block immediately.

Audit trail requirements:

- review trigger
- affected source/domain/date range
- reviewer or review authority
- review timestamp
- decision
- rationale
- expiration or next review date
- resulting source status and allowed use

## SECTION 7 - Source Status Transition Rules

Legal transitions:

| transition | allowed when | required audit |
| --- | --- | --- |
| `manual_review_required` -> `accepted` | All review blockers are cleared and source passes score/PIT requirements. | Review resolution, reviewer notes, timestamp, source-gate score summary. |
| `manual_review_required` -> `conditional` | Review clears only a subset, date range, domain, or use case. | Condition scope, unsupported-domain behavior, reviewer notes. |
| `manual_review_required` -> `rejected` | Review confirms blocking issue remains. | Rejection reason and failed checks. |
| `conditional` -> `accepted` | Conditions are resolved or source version improves enough for full scope. | Prior condition closure, new review timestamp, updated score summary. |
| `conditional` -> `rejected` | Supported subset is no longer safe or conditions cannot be enforced. | Rejection reason and affected scope. |
| `accepted` -> `conditional` | New evidence limits source scope or source version coverage changes. | Scope reduction reason and date of effect. |
| `accepted` -> `deprecated` | Source version is superseded, withdrawn, or no longer used for new builds. | Deprecation reason, effective deprecation date, replacement if any. |
| `accepted` -> `manual_review_required` | New ambiguity, conflict, licensing issue, or lineage defect appears. | Review trigger and affected scope. |
| `deprecated` -> `accepted` | Only through a new source-gate review of the same or restored source version. | Full reacceptance record. |
| `rejected` -> `manual_review_required` | Source is reopened for inspection but not yet accepted. | Reopen reason and review trigger. |
| `rejected` -> `accepted` | Only through a new source-gate review with corrected evidence/version. | Full reacceptance record and prior rejection reference. |

Illegal transitions:

- `rejected` -> `accepted` without new review.
- `deprecated` -> `accepted` without reacceptance.
- `manual_review_required` -> `accepted` without review closure.
- `conditional` -> `accepted` without condition resolution.
- `accepted` -> `discovery_allowed` directly through source status alone.
- Any transition based on downstream alpha results, IC scores, validation outcomes, or production utility.

Transition invariants:

- Every transition must preserve prior state history.
- Every transition must carry timestamp, reviewer/review authority, rationale, and source version.
- Transitions change source eligibility only prospectively unless a review explicitly documents corrected historical interpretation.

## SECTION 8 - Eligibility Engine Design

The eligibility engine should return both a decision and a reason. It should be fail-closed: missing evidence means blocked.

Decision outputs:

- `eligible`
- `eligible_with_conditions`
- `diagnostics_only`
- `manual_review_required`
- `blocked`

Required decision dimensions:

- source status
- allowed use
- manual review flag
- source-gate scores
- PIT quality class
- confidence tier or confidence score
- blocked reason
- conditional scope
- source version and snapshot date
- audit completeness

Lineage construction eligibility:

- Allowed only when source status is `accepted`, or `conditional` inside supported scope.
- Allowed use must map to `lineage_only` or narrower approved identity/ticker lineage use.
- Manual review must be false/closed.
- PIT quality must not be blocking if present.
- Confidence must be at least medium or equivalent to `0.70`.
- Required audit fields must be populated.

PIT table construction eligibility:

- Requires lineage construction eligibility.
- Requires source-specific field mapping and row-level validation in a later implementation task.
- Blocks if identity/ticker date windows cannot be represented point-in-time.

Sector history eligibility:

- Remains blocked in this phase.
- Later eligibility requires certified security/ticker lineage and a separate sector/industry source gate.

Industry history eligibility:

- Remains blocked in this phase.
- Later eligibility requires certified security/ticker lineage and a separate classification source gate.

Peer reconstruction eligibility:

- Remains blocked in this phase.
- Later eligibility requires certified identity lineage, sector/industry history, coverage diagnostics, and peer-group readiness review.

Discovery support eligibility:

- Remains blocked in this phase.
- Later eligibility requires PIT readiness review and explicit discovery-design authorization.

Eligibility precedence:

1. If source status is `rejected`, `deprecated`, `diagnostic_only`, or open `manual_review_required`, decision is blocked or diagnostics-only.
2. If allowed use is `blocked`, decision is blocked.
3. If allowed use is `diagnostics_only`, decision is diagnostics-only.
4. If conditional scope is missing or unsupported, decision is blocked.
5. If PIT quality is blocking, decision is blocked.
6. If confidence is below floor, decision is blocked.
7. If audit fields are missing, decision is manual-review-required or blocked.
8. Otherwise, source is eligible only for the narrowest requested use.

## SECTION 9 - Diagnostics and Reporting

Required semantic diagnostics:

- accepted-source inventory
- conditional-source inventory
- rejected-source inventory
- deprecated-source inventory
- diagnostic-only source inventory
- manual-review queue
- source-status transition history
- allowed-use inventory
- eligibility decision report
- blocked-source report
- missing audit-field report
- rejected-without-rationale report
- accepted-with-manual-review-conflict report
- accepted-with-blocking-quality report
- conditional-without-scope report
- source-gate score distribution
- low-score accepted-source report
- source version and snapshot-date inventory

Required report fields:

- source
- source type
- source version
- source snapshot date
- source file hash or controlled reference
- source status
- allowed use
- eligibility decision
- blocked reason
- manual review flag
- review timestamp
- reviewer notes
- score summary
- condition scope if applicable
- prior status and new status for transition reports

Reporting principles:

- Diagnostics should retain blocked and rejected sources rather than dropping them.
- Every non-eligible decision should have a reason.
- Every status transition should be reproducible.
- Discovery-facing readiness reports should include only eligibility summaries, not raw source integration side effects.

## SECTION 10 - Final Recommendation

1. What semantic controls are mandatory?

Mandatory controls are source status/allowed-use compatibility, `allowed_use` membership, manual-review blocking, rejected-source rationale, deprecated-source blocking, conditional-source scope enforcement, accepted-source score/quality/confidence requirements, audit-field completeness, and eligibility decisions with explicit blocked reasons.

2. What source statuses are blocking?

`rejected`, `deprecated`, `manual_review_required`, and `diagnostic_only` block construction. `conditional` blocks unsupported domains/date ranges/uses. `accepted` is not blocking by status alone, but can still be blocked by manual review, PIT quality, confidence, stale, inferred-window, or audit failures.

3. What transitions are allowed?

Allowed transitions include `manual_review_required` to `accepted`, `conditional`, or `rejected`; `conditional` to `accepted` or `rejected`; `accepted` to `conditional`, `deprecated`, or `manual_review_required`; and rejected/deprecated reopening only through explicit review. All transitions require timestamped audit records and rationale.

4. What should remain blocked?

Real source ingestion, source loading, PIT metadata construction, security lineage construction, ticker lineage construction, sector history, industry history, peer reconstruction, discovery support, validation, governance mutation, production registration, and ML should remain blocked until semantic validation is implemented and reviewed.

5. What should the next Codex task be?

The next Codex task should be **Security Master and Ticker Lineage PIT Source-Gate Semantic Validation Patch v1**. It should implement the semantic manifest checks defined here, add focused tests for blocking combinations and legal transitions, and remain source-gate-only with no ingestion, no real source loading, no metadata construction, no lineage construction, no reconstruction, no discovery, no validation, no governance mutation, no production registration, and no ML.
