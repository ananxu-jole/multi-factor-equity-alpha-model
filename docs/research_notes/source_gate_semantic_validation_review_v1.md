# Project Underdog - Source-Gate Semantic Validation Review v1

## SECTION 1 - Executive Summary

The source-gate semantic validation design is directionally sound and substantially complete. It correctly separates schema validation from semantic validation, makes source eligibility fail-closed, and defines how source status, allowed use, manual review, PIT quality, confidence, blocked reasons, conditional scope, and audit completeness should interact before any real metadata source enters the PIT infrastructure.

Semantic design quality: strong. The design addresses the exact gap identified in the source-gate post-implementation review: a syntactically valid manifest row can still be unsafe if it combines accepted status with manual review, blocking PIT quality, inadequate scores, missing rejection rationale, or overbroad allowed use.

Completeness: high, but not perfect. The design is complete enough to implement semantic checks, but implementation should resolve two practical details first:

- The design introduces canonical allowed-use categories such as `diagnostics_only`, `lineage_only`, `reconstruction_allowed`, `discovery_allowed`, `research_only`, and `blocked`, while the current scaffold schema uses labels such as `identity_ticker_lineage`, `diagnostic_only`, `rejected`, `manual_review_only`, and `deprecated_no_new_builds`.
- Conditional-source scope and source-status transition history are well specified conceptually, but their machine-readable fields are not yet present in the source acceptance manifest scaffold.

Implementation readiness: ready with changes.

Final classification: `IMPLEMENTATION READY WITH CHANGES`.

## SECTION 2 - Source Status Semantics Review

`accepted`:

- Definition is clear.
- Downstream eligibility is correctly limited to the explicitly allowed use.
- Blocking behavior is appropriately conditional on manual review, PIT quality, confidence, scores, stale/inferred-window issues, and unsupported use.
- Review and audit requirements are sufficient.

`conditional`:

- Definition is clear and appropriately fail-closed.
- The design correctly requires machine-readable conditions before any construction use.
- The biggest implementation gap is that the current scaffold does not yet contain condition fields such as supported domain, supported date range, supported universe, condition rationale, or condition document reference.

`rejected`:

- Definition and blocking behavior are clear.
- Required rejection rationale is appropriate.
- Override path is appropriately restricted to a new source-gate review.

`deprecated`:

- Definition is clear.
- The design correctly allows historical reproducibility but blocks new construction.
- Requires transition history and deprecation effective date before implementation can fully audit it.

`manual_review_required`:

- Definition and blocking behavior are clear.
- Trigger and clearance rules are appropriately strict.
- Expiration policy is useful and should be implemented before real source acceptance.

Assessment:

Source status semantics are clear and safe. No conceptual blocker remains.

## SECTION 3 - Allowed Use Semantics Review

The allowed-use categories are conceptually strong:

- `diagnostics_only`
- `lineage_only`
- `reconstruction_allowed`
- `discovery_allowed`
- `research_only`
- `blocked`

Permitted and prohibited actions are unambiguous. The design correctly prevents source status from directly granting discovery support, and it correctly treats effective permission as the strictest intersection of source status, allowed use, PIT quality, confidence, and review state.

Main gap:

The current scaffold schema uses earlier source-gate labels:

- `identity_ticker_lineage`
- `diagnostic_only`
- `rejected`
- `manual_review_only`
- `deprecated_no_new_builds`

The semantic design includes a mapping from scaffold labels to canonical allowed-use categories, which is good. However, implementation must choose one of two paths:

- Preserve current scaffold labels and implement a mapping layer to canonical categories.
- Update the scaffold schema to use canonical categories directly.

Recommendation:

Use a mapping layer first. It avoids unnecessary scaffold churn while still enforcing the semantic design.

## SECTION 4 - Conditional / Rejected / Manual Review Rule Review

Conditional source safeguards:

- Safeguards are sufficient.
- Required confidence floor of `0.70` is consistent with prior policy.
- Downstream restrictions are appropriately strict.
- Missing implementation detail: condition scope needs concrete fields or a structured sidecar before conditional sources can be accepted.

Rejected source rules:

- Rejection rationale, documentation, reuse restrictions, override conditions, and audit requirements are sufficient.
- Rejected sources are correctly limited to audit and diagnostics.

Manual review rules:

- Trigger rules are comprehensive.
- Clearance rules are strong because they exclude downstream alpha performance, discovery results, and validation outcomes as clearance signals.
- Expiration policy is appropriate.
- Audit trail requirements are sufficient.

Downstream blocking behavior:

- Clear and fail-closed across lineage construction, PIT table construction, sector/industry history, peer reconstruction, and discovery support.

Assessment:

Rules are sufficient for implementation, with the caveat that conditional-source scope fields must be represented concretely.

## SECTION 5 - Source Status Transition Review

Legal transitions are well defined:

- `manual_review_required` -> `accepted`
- `manual_review_required` -> `conditional`
- `manual_review_required` -> `rejected`
- `conditional` -> `accepted`
- `conditional` -> `rejected`
- `accepted` -> `conditional`
- `accepted` -> `deprecated`
- `accepted` -> `manual_review_required`
- `deprecated` -> `accepted` through reacceptance
- `rejected` -> `manual_review_required`
- `rejected` -> `accepted` through new review

Illegal transitions are appropriate:

- `rejected` -> `accepted` without new review
- `deprecated` -> `accepted` without reacceptance
- `manual_review_required` -> `accepted` without review closure
- `conditional` -> `accepted` without condition resolution
- `accepted` -> `discovery_allowed` directly through source status
- any transition based on alpha results, IC scores, validation outcomes, or production utility

Missing transition cases:

- `diagnostic_only` is not explicitly covered in the transition table. It should be added before implementation.
- Potential legal transitions should include `diagnostic_only` -> `manual_review_required`, `diagnostic_only` -> `rejected`, and `diagnostic_only` -> `accepted` only through a full source-gate review.
- Potential illegal transition should include `diagnostic_only` -> construction-eligible use without review.

Assessment:

Transition rules are sufficient with a small addition for `diagnostic_only`.

## SECTION 6 - Eligibility Engine Review

Lineage construction:

- The decision framework is sufficient.
- Eligibility requires accepted or in-scope conditional status, lineage-compatible allowed use, closed manual review, non-blocking PIT quality, sufficient confidence, and audit completeness.

PIT table construction:

- Correctly requires lineage construction eligibility plus future source-specific field mapping and row-level validation.
- Correctly remains outside the source-gate semantic implementation itself.

Sector history:

- Correctly blocked in this phase.
- Requires certified identity/ticker lineage and separate sector/industry source gate later.

Industry history:

- Correctly blocked in this phase.

Peer reconstruction:

- Correctly blocked in this phase.

Discovery support:

- Correctly blocked in this phase.
- Requires PIT readiness review and explicit discovery-design authorization later.

Eligibility precedence:

- The fail-closed precedence order is sensible.
- Missing evidence leads to blocked or manual-review-required decisions.

Assessment:

The eligibility engine design is sufficient for a source-gate semantic validation patch.

## SECTION 7 - Diagnostics Review

Required diagnostics are strong:

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

Missing or recommended diagnostics:

- allowed-use mapping report, showing raw scaffold allowed-use value and canonical allowed-use category.
- diagnostic-only transition report.
- overbroad-use report, identifying sources whose allowed use exceeds source status eligibility.
- accepted-with-low-score-component report by individual score field.
- expired-manual-review report.
- transition-without-prior-state report.

Assessment:

Diagnostics are sufficient for implementation if the recommended additions are included or explicitly deferred.

## SECTION 8 - Implementation Risk Assessment

| risk | severity | assessment |
| --- | --- | --- |
| Highest semantic risk: canonical allowed-use mismatch | High | The design and scaffold use different labels. A mapping layer or schema update is required before semantic checks are reliable. |
| Highest policy risk: conditional source scope ambiguity | High | Conditional sources require machine-readable scope, but scaffold fields do not yet encode it. |
| Highest downstream eligibility risk: accidental lineage eligibility | High | Accepted status must not automatically authorize lineage construction without allowed-use, confidence, review, audit, and PIT-quality checks. |
| Highest future integration risk: transition history not represented | Moderate-high | Transition rules are well designed, but transition storage/reporting fields need concrete representation. |
| Highest test risk: semantic combinations | Moderate | Existing tests cover enum validity, but the next implementation needs tests for status/use/review/quality/score combinations. |

Overall risk:

Implementation risk is manageable if the patch is explicitly limited to semantic source-gate checks and diagnostics. No architectural redesign is needed.

## SECTION 9 - Final Classification

Classification: `IMPLEMENTATION READY WITH CHANGES`.

Rationale:

The semantic rules are complete enough to implement, and the design directly addresses the source-gate scaffold's known gaps. The required changes are practical rather than conceptual: reconcile allowed-use labels, add or sidecar conditional-source scope representation, add `diagnostic_only` transition cases, and define concrete semantic diagnostics/tests. These should be resolved inside the implementation patch rather than through another broad design cycle.

## SECTION 10 - Final Recommendation

1. Are semantic rules complete enough to implement?

Yes, with targeted changes. The rules are complete enough for a source-gate semantic validation patch.

2. Are blocking statuses clear?

Yes. `rejected`, `deprecated`, `manual_review_required`, and `diagnostic_only` block construction. `conditional` blocks unsupported domains, dates, and uses. `accepted` can still be blocked by manual review, blocking PIT quality, low confidence, stale/inferred-window failures, missing audit fields, or overbroad allowed use.

3. Are allowed-use rules clear?

Conceptually yes. Implementation must reconcile canonical allowed-use categories with the current scaffold labels through either a mapping layer or a schema update.

4. Are transition rules sufficient?

Mostly. Add explicit `diagnostic_only` transitions before or during implementation.

5. Are diagnostics sufficient?

Yes for the core semantic layer. Add an allowed-use mapping report, diagnostic-only transition report, overbroad-use report, expired-manual-review report, and transition-without-prior-state report if feasible.

6. What must change before implementation?

The implementation patch must define:

- canonical allowed-use mapping from scaffold labels
- concrete conditional-source scope representation
- explicit `diagnostic_only` transition behavior
- semantic eligibility output fields
- tests for status/use/review/quality/score combinations

7. What should the next Codex task be?

The next Codex task should be **Security Master and Ticker Lineage PIT Source-Gate Semantic Validation Patch v1**. It should implement semantic manifest checks, diagnostics, and tests while remaining source-gate-only. It must not ingest data, load real sources, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.
