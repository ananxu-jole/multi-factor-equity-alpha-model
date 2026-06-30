# Project Underdog - Source-Gate Semantic Validation Patch Design v1

## SECTION 1 - Executive Summary

The semantic validation review classified the framework as `IMPLEMENTATION READY WITH CHANGES`. The design is conceptually sound, but three remaining implementation-facing gaps must be frozen before coding:

1. Canonical `allowed_use` mapping.
2. Machine-readable conditional-source scope representation.
3. Explicit `diagnostic_only` transition rules.

Patching is required before implementation because the current source-gate scaffold can verify structure and enum legality, but cannot yet enforce whether a source is genuinely eligible for lineage construction or should remain diagnostic-only, blocked, rejected, deprecated, or under manual review. Without these patch rules, a syntactically valid manifest row could still overstate source eligibility.

This patch design remains design-only. No code, ingestion, source loading, metadata construction, lineage construction, reconstruction, discovery, refinement, validation, governance mutation, threshold change, production registration, or ML was performed.

## SECTION 2 - Canonical Allowed-Use Mapping

Canonical allowed-use categories:

| canonical name | description | permitted actions | prohibited actions | downstream eligibility |
| --- | --- | --- | --- | --- |
| `diagnostics_only` | Source may be inspected, profiled, scored, rejected, or triaged, but cannot feed construction. | Source profiling, coverage inspection, rejection reports, manual review queue, source-gate diagnostics. | Security lineage, ticker lineage, PIT tables, sector/industry/peer reconstruction, discovery support, production use, ML. | No downstream construction eligibility. |
| `lineage_only` | Source may support security master or ticker lineage construction if source status and semantic checks pass. | Identity/ticker-lineage source use, source lineage records, lineage diagnostics, blocked/eligible diagnostics. | Sector history, industry history, peer reconstruction, discovery support, production use, ML. | Eligible only for the security/ticker lineage phase after acceptance. |
| `reconstruction_allowed` | Source may support later reconstruction layers after identity/ticker lineage is certified. | Later sector, industry, size, or peer reconstruction after separate readiness review. | Direct discovery support, production use, ML. | Not available in the first identity/ticker source-gate phase. |
| `discovery_allowed` | Source may support research discovery panels after PIT readiness is certified. | Research-only discovery support after future readiness approval. | Production use, validation shortcut, governance mutation, ML. | Explicitly blocked in current phase. |
| `research_only` | Umbrella research label requiring a narrower action category before eligibility. | Research notes, source inspection, non-production diagnostics. | Any construction unless mapped to a concrete eligible category. | Not sufficient alone for source acceptance. |
| `blocked` | Source is retained only for audit or historical reference. | Audit retention, rejection inventory, transition history. | All loading, construction, reconstruction, discovery support, production use, ML. | No downstream eligibility. |

Legacy/non-canonical mapping rules:

| raw `allowed_use` value | canonical value | semantic interpretation | construction eligible |
| --- | --- | --- | --- |
| `identity_ticker_lineage` | `lineage_only` | Existing scaffold label for identity/ticker lineage use. | Yes, only with `accepted` or in-scope `conditional` status and all other checks passing. |
| `diagnostic_only` | `diagnostics_only` | Existing scaffold label for source diagnostics. | No. |
| `rejected` | `blocked` | Existing scaffold label for rejected-source audit retention. | No. |
| `manual_review_only` | `diagnostics_only` | Existing scaffold label for manual review triage only. | No while review remains open. |
| `deprecated_no_new_builds` | `blocked` | Existing scaffold label for deprecated source versions. | No new construction. |
| `diagnostics_only` | `diagnostics_only` | Canonical label. | No. |
| `lineage_only` | `lineage_only` | Canonical label. | Yes, only after all source/status checks pass. |
| `reconstruction_allowed` | `reconstruction_allowed` | Canonical label. | Not in current phase. |
| `discovery_allowed` | `discovery_allowed` | Canonical label. | Not in current phase. |
| `research_only` | `research_only` | Canonical umbrella label. | No until narrowed. |
| `blocked` | `blocked` | Canonical blocked label. | No. |

Implementation rule:

The semantic patch should preserve current scaffold labels and add a canonical mapping layer first. A future schema cleanup may replace legacy labels directly, but that should not be required before semantic validation can be implemented.

Unknown allowed-use values:

- Any unrecognized `allowed_use` value must produce decision `blocked`.
- Blocked reason should be `unsupported_domain` or `source_rejected` depending on source status.
- Diagnostic output should include raw value and canonical mapping failure.

## SECTION 3 - Machine-Readable Conditional Scope Model

Conditional sources require explicit structured scope. The recommended representation is a JSON object stored as a manifest field or sidecar record keyed by `source_gate_run_id`, `source`, `source_version`, and `source_snapshot_date`.

Required fields:

| field | required | description |
| --- | --- | --- |
| `conditional_scope_id` | yes | Stable id for the conditional-scope record. |
| `source_gate_run_id` | yes | Links to source acceptance manifest row. |
| `source` | yes | Source name. |
| `source_version` | yes | Source version. |
| `source_snapshot_date` | yes | Snapshot/as-of date. |
| `status` | yes | Must be `active`, `expired`, `superseded`, or `revoked`. |
| `permitted_uses` | yes | List of canonical allowed-use values permitted by this condition. |
| `prohibited_uses` | yes | List of canonical allowed-use values explicitly blocked. |
| `permitted_domains` | yes | List such as `security_identity`, `ticker_lineage`, `exchange_history`, `name_history`, `diagnostics`. |
| `prohibited_domains` | yes | List such as `sector_history`, `industry_history`, `peer_reconstruction`, `discovery_support`, `production`. |
| `effective_start` | yes | First source date or metadata date covered by condition. |
| `effective_end` | yes | Last source date or open-ended marker. |
| `supported_universe` | yes | Universe scope, exchange namespace, country, asset class, or explicit `all_declared_universe`. |
| `unsupported_universe` | yes | Known exclusions or `none_declared`. |
| `required_confidence_floor` | yes | Numeric floor; default minimum for identity/ticker use is `0.70`. |
| `required_review_flags` | yes | Review flags that must be closed before use. Empty list allowed. |
| `expiration_or_review_date` | yes | Date by which condition must be reviewed or expires. |
| `rationale` | yes | Human-readable reason for conditional acceptance. |
| `blocked_reason_if_violated` | yes | Default blocked reason, usually `unsupported_domain` or `manual_review_required`. |
| `review_timestamp` | yes | Timestamp of conditional scope approval. |
| `reviewer_notes` | yes | Review notes. |

Example 1:

```json
{
  "conditional_scope_id": "scope_identity_ticker_2020_2025_v1",
  "source_gate_run_id": "pit_source_gate_v1",
  "source": "example_identity_source",
  "source_version": "2026-06",
  "source_snapshot_date": "2026-06-21",
  "status": "active",
  "permitted_uses": ["lineage_only"],
  "prohibited_uses": ["reconstruction_allowed", "discovery_allowed"],
  "permitted_domains": ["security_identity", "ticker_lineage"],
  "prohibited_domains": ["sector_history", "industry_history", "peer_reconstruction", "discovery_support", "production"],
  "effective_start": "2020-01-01",
  "effective_end": "2025-12-31",
  "supported_universe": "declared_us_equity_universe",
  "unsupported_universe": "non_us_equities;options;fixed_income",
  "required_confidence_floor": 0.70,
  "required_review_flags": [],
  "expiration_or_review_date": "2026-12-31",
  "rationale": "Dated identity and ticker rows available only for declared US equity universe.",
  "blocked_reason_if_violated": "unsupported_domain",
  "review_timestamp": "2026-06-21T00:00:00Z",
  "reviewer_notes": "Eligible only for identity and ticker lineage source-gate evaluation."
}
```

Example 2:

```json
{
  "conditional_scope_id": "scope_diagnostics_only_static_snapshot_v1",
  "source_gate_run_id": "pit_source_gate_v1",
  "source": "example_static_profile_source",
  "source_version": "2026-06",
  "source_snapshot_date": "2026-06-21",
  "status": "active",
  "permitted_uses": ["diagnostics_only"],
  "prohibited_uses": ["lineage_only", "reconstruction_allowed", "discovery_allowed"],
  "permitted_domains": ["diagnostics"],
  "prohibited_domains": ["security_identity", "ticker_lineage", "sector_history", "industry_history", "peer_reconstruction", "discovery_support"],
  "effective_start": "2026-06-21",
  "effective_end": "2026-06-21",
  "supported_universe": "source_snapshot_universe",
  "unsupported_universe": "historical_pit_use",
  "required_confidence_floor": 1.00,
  "required_review_flags": ["static_snapshot_only"],
  "expiration_or_review_date": "2026-09-30",
  "rationale": "Current snapshot source useful only for diagnostics.",
  "blocked_reason_if_violated": "static_snapshot_only",
  "review_timestamp": "2026-06-21T00:00:00Z",
  "reviewer_notes": "Cannot support PIT construction."
}
```

Representation rule:

The implementation may use either:

- a `conditional_scope_json` field in the source acceptance manifest, or
- a `conditional_scope_manifest.json` / `conditional_scope_manifest.csv` sidecar keyed to the source acceptance manifest.

For the first patch, a sidecar is preferred because it avoids expanding the source acceptance schema too aggressively.

## SECTION 4 - Conditional Source Enforcement Rules

Conditional scope evaluation:

1. Normalize raw `allowed_use` to canonical allowed use.
2. Confirm source status is `conditional`.
3. Confirm conditional scope record exists and has `status = active`.
4. Confirm requested use is in `permitted_uses`.
5. Confirm requested use is not in `prohibited_uses`.
6. Confirm requested domain is in `permitted_domains`.
7. Confirm requested domain is not in `prohibited_domains`.
8. Confirm source date or intended metadata date is between `effective_start` and `effective_end`.
9. Confirm universe/security namespace is within `supported_universe`.
10. Confirm confidence meets `required_confidence_floor`.
11. Confirm all `required_review_flags` are closed or not triggered.
12. Confirm current date has not passed `expiration_or_review_date` without review.

Violations:

- Missing conditional scope record.
- Scope status not active.
- Requested use outside `permitted_uses`.
- Requested domain outside `permitted_domains`.
- Requested date outside scope.
- Requested universe outside scope.
- Confidence below floor.
- Open required review flag.
- Expired condition.
- Missing rationale or review timestamp.

Downstream blocking behavior:

- Any violation blocks lineage construction and all downstream construction.
- The default blocked reason should be the conditional scope's `blocked_reason_if_violated`.
- If no blocked reason is provided, use `unsupported_domain`.
- Conditional-source violations must not silently downgrade to diagnostics-only unless the source's canonical allowed use already permits only diagnostics.

Audit requirements:

- Record evaluated source, source version, snapshot date, requested use, requested domain, requested date range, requested universe, decision, blocked reason, and condition scope id.
- Retain both accepted and blocked conditional decisions.
- Emit conditional-source inventory and conditional-scope violation diagnostics.

Escalation path:

- Conditional -> accepted requires new review showing the condition is resolved.
- Conditional -> manual review required is triggered by ambiguity, expired condition, or conflicting source evidence.
- Conditional -> rejected is triggered by unresolvable condition failure.

## SECTION 5 - Diagnostic-Only Transition Rules

Legal transitions involving `diagnostic_only`:

| transition | legal when | required approvals | required diagnostics |
| --- | --- | --- | --- |
| `diagnostic_only` -> `manual_review_required` | Source is reopened for possible construction review but unresolved issues remain. | Source-gate review owner or approved review process. | Diagnostic-only transition report, manual-review queue entry. |
| `diagnostic_only` -> `rejected` | Diagnostic inspection confirms blocking defects. | Source-gate review. | Rejection rationale, failed-check report, rejected-source inventory. |
| `diagnostic_only` -> `conditional` | Review identifies a narrow, machine-readable, safe scope. | Full source-gate review plus conditional scope record. | Conditional-source inventory, scope record, transition history. |
| `diagnostic_only` -> `accepted` | Only after full source-gate review proves all construction requirements are met. | Full source-gate review and semantic eligibility pass. | Accepted-source inventory, eligibility decision report, transition history. |
| `accepted` -> `diagnostic_only` | Source is no longer safe for construction but remains useful for diagnostics. | Source-gate review. | Diagnostic-only inventory, prior accepted-source deactivation, transition history. |
| `conditional` -> `diagnostic_only` | Conditional scope expires or is narrowed to diagnostics only. | Source-gate review or expiration rule. | Conditional expiration report, diagnostic-only transition report. |
| `manual_review_required` -> `diagnostic_only` | Review finds source useful only for diagnostics. | Manual review closure. | Manual-review resolution, diagnostic-only inventory. |
| `deprecated` -> `diagnostic_only` | Deprecated source remains useful for inspection but not new builds. | Source-gate review or deprecation review. | Deprecated-source transition report. |

Illegal transitions:

- `diagnostic_only` -> construction eligibility without full source-gate review.
- `diagnostic_only` -> `accepted` based on alpha results, IC results, validation results, or production utility.
- `diagnostic_only` -> `conditional` without machine-readable condition scope.
- `rejected` -> `diagnostic_only` without review reopening the source for audit or inspection.
- Any transition that drops prior `diagnostic_only` status history.

Required approvals:

- Every transition out of `diagnostic_only` requires a review timestamp, rationale, reviewer notes, source version, and prior status reference.
- Transition to `accepted` requires full semantic eligibility pass.
- Transition to `conditional` requires active conditional scope record.

Required diagnostics:

- diagnostic-only source inventory
- diagnostic-only transition report
- source-status transition history
- transition-without-prior-state report
- transition-missing-rationale report
- transition-to-construction-eligible report

## SECTION 6 - Eligibility Engine Patch

Updated decision priorities:

1. Validate schema and controlled enum values.
2. Normalize raw `allowed_use` to canonical allowed use.
3. If allowed-use mapping fails, decision is `blocked`.
4. If source status is `rejected` or `deprecated`, decision is `blocked`.
5. If source status is `diagnostic_only`, decision is `diagnostics_only` unless requested use is construction; then decision is `blocked`.
6. If source status is `manual_review_required` or manual review flag is true/open, decision is `manual_review_required`.
7. If source status is `conditional`, evaluate active conditional scope.
8. If source status is `accepted`, continue to PIT quality, confidence, audit, and score checks.
9. If PIT quality is `static_snapshot_only`, `unresolved`, or `blocked`, decision is `blocked`.
10. If confidence is below floor or tier is `low`, `blocked`, or `unknown`, decision is `blocked`.
11. If required audit fields are missing, decision is `manual_review_required` or `blocked`.
12. If source-gate scores fail threshold, decision is `blocked` or `manual_review_required`.
13. If requested use exceeds canonical allowed use, decision is `blocked`.
14. Otherwise, decision is `eligible` for the narrowest permitted use.

Conflict resolution rules:

- Blocking source status overrides allowed use.
- Blocking PIT quality overrides allowed use.
- Manual review overrides accepted status.
- Conditional scope overrides broad allowed-use claims.
- Unknown allowed-use mapping blocks.
- Diagnostic-only status never permits construction.
- Discovery support remains blocked regardless of source status in this phase.

Semantic eligibility output fields:

- `source`
- `source_version`
- `source_snapshot_date`
- `raw_allowed_use`
- `canonical_allowed_use`
- `source_gate_status`
- `requested_use`
- `requested_domain`
- `eligibility_decision`
- `blocked_reason`
- `conditional_scope_id`
- `manual_review_required`
- `review_timestamp`
- `score_summary`
- `semantic_validation_notes`

Minimum source-gate score rules:

- `pit_integrity_score` must be at least 2 for construction eligibility.
- `identifier_quality_score` must be at least 2 for identity/ticker lineage eligibility.
- `historical_depth_score` must be at least 2 for PIT construction eligibility.
- `leakage_risk_score` must be at least 2 for construction eligibility.
- Any score below 2 in those required fields blocks construction or sends to manual review.
- Diagnostic-only use may retain lower scores if status/use remain non-construction.

## SECTION 7 - Diagnostics Requirements

Additional diagnostics required by this patch:

| diagnostic | purpose |
| --- | --- |
| `allowed_use_mapping_report` | Shows raw allowed-use label, canonical allowed-use category, mapping status, and mapping failure reason. |
| `allowed_use_violation_report` | Captures requested use exceeding canonical allowed use or source status eligibility. |
| `conditional_scope_inventory` | Lists active, expired, superseded, and revoked conditional scope records. |
| `conditional_scope_violation_report` | Captures conditional source uses outside permitted uses/domains/dates/universe/confidence/review requirements. |
| `diagnostic_only_transition_report` | Tracks legal and illegal transitions involving diagnostic-only status. |
| `transition_violation_report` | Captures illegal status transitions, missing prior state, or missing transition rationale. |
| `eligibility_override_report` | Captures any manual or review-based override decision and its rationale. |
| `accepted_source_semantic_conflict_report` | Captures accepted sources with manual review, blocking PIT quality, low confidence, missing audit fields, or low scores. |
| `semantic_eligibility_decision_report` | Master decision table for source semantic eligibility. |

Required fields for diagnostics:

- source
- source version
- source snapshot date
- raw allowed use
- canonical allowed use
- source status
- prior source status where applicable
- requested use
- requested domain
- conditional scope id where applicable
- eligibility decision
- blocked reason
- semantic rule triggered
- review timestamp
- reviewer notes
- source-gate run id

Eligibility override decisions:

- Overrides must not bypass rejected status.
- Overrides must not allow diagnostic-only sources to construct lineage without full re-review.
- Overrides must not use alpha results, validation results, or production utility as rationale.
- Overrides require explicit review timestamp, rationale, affected scope, and expiration/review date.

## SECTION 8 - Risk Assessment

| risk | severity | assessment |
| --- | --- | --- |
| Semantic ambiguity risk | Low after patch | Canonical allowed-use mapping and conditional scope representation remove the main ambiguity. |
| Enforcement risk | Moderate | Implementation must correctly sequence precedence rules and avoid allowing accepted status to override blocking conditions. |
| Future governance drift risk | Moderate | Future phases may be tempted to treat `discovery_allowed` or `reconstruction_allowed` as available too early. Diagnostics should keep those blocked in this phase. |
| Integration risk | Moderate-high | Conditional scope sidecar must remain synchronized with source acceptance manifest rows. |
| Maintenance risk | Moderate | Legacy allowed-use labels and canonical categories must remain mapped until schema cleanup occurs. |
| Audit risk | Low-moderate | Transition and override diagnostics reduce audit risk if implemented as required. |

Most serious risk:

The highest remaining risk is integration mismatch between source acceptance manifest rows and conditional scope records. The implementation should fail closed if a conditional source lacks a matching active scope record.

## SECTION 9 - Final Readiness Assessment

After this patch design is incorporated, semantic validation would be: `IMPLEMENTATION READY`.

Rationale:

The remaining semantic gaps are fully specified at the design level. The canonical allowed-use mapping is frozen, conditional source scope has a machine-readable model, diagnostic-only transitions are explicit, and the eligibility engine has concrete precedence and diagnostic requirements. Implementation can proceed without another design pass, provided the implementation remains source-gate-only and does not ingest data or construct metadata.

## SECTION 10 - Final Recommendation

1. Are the remaining semantic gaps fully addressed?

Yes. The patch closes the allowed-use mapping, conditional-source scope, and diagnostic-only transition gaps.

2. Is canonical allowed_use now frozen?

Yes. Canonical categories are `diagnostics_only`, `lineage_only`, `reconstruction_allowed`, `discovery_allowed`, `research_only`, and `blocked`, with an explicit mapping from current scaffold labels.

3. Is conditional scope sufficiently machine-readable?

Yes. The conditional scope model defines required fields, status values, permitted/prohibited uses, permitted/prohibited domains, date scope, universe scope, confidence floor, review flags, expiration/review date, rationale, blocked reason, and audit fields.

4. Are diagnostic-only transitions fully specified?

Yes. Legal and illegal transitions involving `diagnostic_only` are specified with required approvals and diagnostics.

5. What should the next Codex task be?

The next Codex task should be **Security Master and Ticker Lineage PIT Source-Gate Semantic Validation Patch Implementation v1**. It should implement the semantic mapping layer, conditional scope scaffold/sidecar, diagnostic-only transition checks, semantic eligibility decision framework, and focused tests. It must remain source-gate-only and must not ingest data, load real sources, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.
