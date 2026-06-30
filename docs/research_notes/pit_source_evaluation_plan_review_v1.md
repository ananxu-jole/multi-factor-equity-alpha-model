# Project Underdog - PIT Source Evaluation Plan Review v1

## SECTION 1 - Executive Summary

This review audited `pit_source_evaluation_plan_v1.md` against the completed source-gate scaffold, semantic-validation implementation, semantic patch design, source-gate post-implementation review, runner behavior, tests, and source-gate artifacts.

Plan completeness: strong. The plan defines a bounded candidate-source evaluation process with intake requirements, workflow order, decision classes, diagnostics, blocking rules, artifact expectations, and success criteria.

Auditability: strong. The plan requires candidate manifests, schema/policy/semantic reports, allowed-use decisions, confidence decisions, conditional-scope reports, blocked-reason reports, manual-review queues, decision artifacts, and guardrail flags.

Readiness for real source evaluation: ready, with strict interpretation. The plan is ready to evaluate a candidate source description or manifest row. It is not authorization to load source files, ingest metadata, accept/reject a real source as final project state, construct lineage, or build PIT tables.

Major risks:

- Decision-class naming risk: `ACCEPTED_FOR_LINEAGE_EVALUATION` could be misread as source acceptance unless every downstream artifact preserves the stated caveat.
- Scope-creep risk: a successful evaluation could be mistaken for permission to ingest or construct metadata.
- Intake-quality risk: candidate sources with incomplete licensing, reproducibility, date, or identifier evidence must be deferred rather than manually inferred.

Final classification: `READY FOR SOURCE EVALUATION`.

## SECTION 2 - Scope Review

The plan is correctly limited to source evaluation only. It authorizes future evaluation artifacts and candidate manifest review, not real source ingestion or construction.

Confirmed exclusions:

| excluded activity | review assessment |
| --- | --- |
| ingestion | Explicitly blocked. |
| source loading | Explicitly blocked. |
| source acceptance/rejection of real sources | Explicitly blocked as final project state; decision classes are evaluation outcomes only. |
| metadata construction | Explicitly blocked. |
| security lineage construction | Explicitly blocked. |
| ticker lineage construction | Explicitly blocked. |
| sector/industry history | Explicitly blocked. |
| peer reconstruction | Explicitly blocked. |
| discovery | Explicitly blocked. |
| validation | Explicitly blocked. |
| production | Explicitly blocked. |

Scope quality is strong. The only caution is terminology: evaluation outputs should avoid any wording that implies a candidate source has been accepted for use, loaded, or trusted.

## SECTION 3 - Candidate Source Intake Review

The intake requirements are sufficient for first-pass source evaluation.

Reviewed intake coverage:

| requirement area | assessment |
| --- | --- |
| source identity | Covered through source name, category, and source type. |
| source category | Covered with examples and controlled descriptive use. |
| historical depth | Covered through earliest/latest available source dates. |
| effective-date support | Covered through effective dates, event dates, and snapshot/as-of dates. |
| identifier support | Covered through stable security id, issuer id, ticker, exchange, share class, and standard identifiers if available. |
| ticker-history support | Covered through ticker changes, delistings, exchange changes, ticker reuse, relisting, and share-class continuity. |
| source timestamp support | Covered through version, snapshot date, collection timestamp, file hash, and controlled references. |
| reproducibility | Covered through raw file retention, references, update process, and normalization notes. |
| expected coverage | Covered through active ticker/date coverage, universe limits, exchange/country/security-type scope. |
| known limitations | Covered through static snapshot risk, missing dates, partial lineage, stale records, and manual repair burden. |

No critical intake fields are missing.

Recommended non-blocking additions for the future scaffold:

- `candidate_source_contact_or_owner` for audit routing.
- `license_review_status` to distinguish notes from an actual licensing clearance state.
- `expected_update_frequency` to support stale-age and maintenance planning.
- `source_sample_allowed_flag` to distinguish descriptive evaluation from any future permitted sample inspection.

These additions are useful but not required before source evaluation begins.

## SECTION 4 - Source-Gate Workflow Review

The workflow ordering is correct:

1. Candidate source manifest.
2. Schema validation.
3. Policy/vocab validation.
4. Semantic validation.
5. Allowed-use eligibility.
6. Diagnostics.
7. Source evaluation decision.

This order is safe because structural validation happens before semantic interpretation, and semantic interpretation happens before any allowed-use decision. The final decision is explicitly downstream of diagnostics, which preserves auditability and fail-closed behavior.

The workflow is complete for the first evaluation phase. It does not need ingestion, row-level PIT checks, source parsing, lineage construction, or discovery hooks.

Review finding:

- The plan should continue to treat schema, policy, and semantic failures as evaluation outcomes, not as reasons to hand-edit a candidate into eligibility.

## SECTION 5 - Decision Class Review

| decision | clarity | allowed next step | blocked next step | documentation assessment |
| --- | --- | --- | --- | --- |
| `ACCEPTED_FOR_LINEAGE_EVALUATION` | Clear with caveat. Name carries acceptance-risk but meaning states it is not final source acceptance. | Future source-specific evaluation or implementation design. | Loading, ingestion, construction, real source acceptance, lineage construction. | Sufficient if audit notes preserve caveat. |
| `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` | Clear. | Diagnostics-only review or conditional-scope clarification. | Lineage construction, PIT tables, reconstruction, discovery support. | Sufficient; should require conditional scope or diagnostics rationale. |
| `MANUAL_REVIEW_REQUIRED` | Clear. | Manual-review queue and missing-information request. | Loading, ingestion, construction, reconstruction, discovery support. | Sufficient. |
| `REJECTED_FOR_PIT_USE` | Clear as evaluation result, not final vendor rejection. | Retain audit record; possible non-PIT context only after separate review. | PIT loading, ingestion, construction, reconstruction, discovery support. | Sufficient. |
| `DEFERRED_PENDING_SOURCE_INFO` | Clear. | Request missing information. | Status upgrade, loading, ingestion, construction. | Sufficient. |

Decision classes are usable. The main risk is semantic drift around `ACCEPTED_FOR_LINEAGE_EVALUATION`. Future artifacts should repeat that this means eligible for deeper evaluation/design only.

## SECTION 6 - Diagnostics Review

Required diagnostics are sufficient:

- schema pass/fail
- policy pass/fail
- semantic pass/fail
- allowed-use decision
- confidence decision
- conditional-scope decision
- blocked reason
- manual-review queue
- source evaluation summary

Additional diagnostics already named in the artifact plan strengthen the design:

- `schema_pass_fail_report.csv`
- `policy_pass_fail_report.csv`
- `confidence_decision_report.csv`
- `conditional_scope_decision_report.csv`
- `source_evaluation_summary.json`
- `source_evaluation_manifest.json`

Recommended non-blocking diagnostics:

- `intake_completeness_report.csv` to separate missing intake fields from semantic failures.
- `decision_guardrail_report.csv` to confirm all no-ingestion/no-loading/no-construction flags.
- `source_evaluation_change_log.csv` for repeated candidate reviews over time.

No required diagnostic is missing for the first source evaluation phase.

## SECTION 7 - Blocking Rule Review

The blocking rules are sufficient and appropriately conservative.

Reviewed blockers:

| blocker | assessment |
| --- | --- |
| static snapshot only | Correctly blocks historical PIT use. |
| no effective dates | Correctly blocks unless snapshot/as-of support is sufficient for diagnostics-only treatment. |
| no identifier continuity | Correctly blocks source work beyond diagnostics/manual review. |
| unclear ticker lineage | Correctly blocks lineage evaluation and downstream construction. |
| rejected source status | Correctly blocks PIT source use. |
| unsupported `allowed_use` | Correctly maps to blocked. |
| low confidence | Correctly blocks construction and downstream use. |
| unresolved manual review | Correctly blocks loading, ingestion, construction, and discovery support. |
| missing reproducibility notes | Correctly blocks because auditability is required before source trust. |

The blocker list also covers unresolved ticker reuse, corporate-action ambiguity, deprecated/diagnostic-only/manual-review states, blocking PIT quality, inadequate source-gate scores, missing licensing notes, missing file hash/reference, unstable coverage, and missing conditional scope.

No critical blocking rule is missing.

## SECTION 8 - Artifact Plan Review

The planned artifact root is appropriate:

`artifacts/research/point_in_time_economic_metadata_v1/source_evaluation/`

Reviewed planned artifacts:

| artifact | assessment |
| --- | --- |
| `candidate_source_manifest.csv` | Required and appropriate. |
| `source_evaluation_report.csv` | Required and appropriate. |
| `source_evaluation_decision.json` | Required and appropriate. |
| `semantic_validation_report.csv` | Required and appropriate. |
| `allowed_use_decision_report.csv` | Required and appropriate. |
| `manual_review_queue.csv` | Required and appropriate. |
| `blocked_reason_report.csv` | Required and appropriate. |

Additional planned artifacts such as schema, policy, confidence, conditional-scope, summary, and manifest reports are useful and not unnecessary.

Recommended non-blocking additions:

- `intake_completeness_report.csv`
- `decision_guardrail_report.csv`
- `source_evaluation_change_log.csv`

The artifact plan is complete enough for source evaluation scaffold implementation.

## SECTION 9 - Final Readiness Classification

Final classification: `READY FOR SOURCE EVALUATION`.

Rationale:

- The plan is complete and matches the current source-gate readiness state.
- It is auditable through manifests, diagnostics, decision artifacts, and guardrail flags.
- It correctly sequences schema, policy, semantic, allowed-use, diagnostic, and decision steps.
- It blocks ingestion, source loading, real source acceptance/rejection as final project state, metadata construction, lineage construction, reconstruction, discovery, validation, governance mutation, production registration, and ML.
- Remaining concerns are non-blocking implementation cautions around terminology, guardrail repetition, and intake completeness reporting.

## SECTION 10 - Final Recommendation

1. Is the source evaluation plan complete?

Yes. It is complete for first-pass candidate source evaluation through descriptive intake and manifest-based source-gate review.

2. Is it safe to evaluate a first source candidate?

Yes, provided the evaluation uses only candidate source descriptions or manifest rows and does not load source files, ingest metadata, accept/reject real sources as final project state, construct metadata, or build lineage.

3. What gaps remain?

Only minor, non-blocking gaps remain: decision-class naming should be handled carefully, intake completeness could be reported explicitly, and future artifacts should include guardrail confirmation.

4. What remains blocked after evaluation?

Real source loading, ingestion, source acceptance/rejection as final project state, metadata construction, security lineage construction, ticker lineage construction, PIT table construction, sector/industry history, peer reconstruction, discovery, refinement, validation, governance mutation, threshold changes, production registration, ML, and alpha candidate creation remain blocked.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - PIT Source Candidate Evaluation Scaffold v1**. It should implement a source-evaluation artifact scaffold and runner support for candidate manifest evaluation only. It should not ingest data, load real sources, accept or reject real sources, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.
