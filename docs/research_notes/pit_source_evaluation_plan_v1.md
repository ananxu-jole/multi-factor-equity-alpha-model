# Project Underdog - PIT Source Evaluation Plan v1

## SECTION 1 - Executive Summary

Current readiness state: `READY FOR SOURCE EVALUATION`.

The source-gate scaffold and semantic validation layer are structurally ready to evaluate a candidate source description and candidate source manifest. Source evaluation comes before ingestion because Project Underdog must first determine whether a source is eligible, auditable, point-in-time safe, and limited to an approved allowed use. Loading source files before this review would risk importing static snapshots, weak ticker identity, unclear licensing, or incomplete effective-date lineage into the PIT infrastructure.

This plan authorizes only a review-first source evaluation process for future candidate metadata sources. It authorizes creation of candidate evaluation artifacts and source-gate decision reports in a future task. It does not authorize source ingestion, real source loading, source acceptance/rejection of an actual vendor or file, PIT table construction, security lineage construction, ticker lineage construction, sector/industry reconstruction, peer reconstruction, discovery, refinement, validation, governance mutation, production registration, or ML.

What remains blocked:

- real source loading
- metadata ingestion
- real source acceptance or rejection
- security master construction
- ticker lineage construction
- PIT table construction
- sector/industry/peer reconstruction
- discovery, refinement, validation
- governance mutation, threshold changes, production registration, ML

## SECTION 2 - First Source Evaluation Scope

Initial source-evaluation scope is limited to:

- security identity suitability
- ticker lineage suitability
- source metadata completeness
- source auditability
- allowed-use eligibility
- source-gate scoreability
- semantic eligibility decisioning
- manual-review triage

Evaluation should focus on whether the source could plausibly support future `security_master_pit`, `ticker_lineage_pit`, and `metadata_source_lineage` work after separate approval.

Explicitly excluded:

- source ingestion
- source file loading
- source acceptance or rejection of a real source as a final project decision
- PIT table construction
- lineage construction
- sector history
- industry history
- size history
- peer reconstruction
- alpha discovery
- refinement
- validation
- production use
- ML

## SECTION 3 - Candidate Source Intake Requirements

A candidate source must provide enough descriptive and audit information to populate a candidate source manifest before evaluation. Required intake information:

| intake item | requirement |
| --- | --- |
| source name | Human-readable source name or controlled placeholder id. |
| source category | Examples: exchange/reference data, security master, ticker history, classification provider, historical snapshot archive, manual audit source. |
| source type | Vendor, internal archive, manual curated diagnostic, public reference, controlled snapshot, or other declared type. |
| historical depth | Date range covered, including earliest and latest available source dates. |
| effective-date support | Whether the source provides effective start/end dates, event dates, or only snapshot/as-of dates. |
| as-of/snapshot support | Whether every record or file has a known-as-of date or source snapshot date. |
| identifier support | Stable security id, issuer id, ticker, exchange, share class, CUSIP/ISIN/FIGI or equivalent if available. |
| ticker-history support | Ticker changes, prior/next ticker, delisting, exchange changes, ticker reuse, relisting, share-class continuity. |
| name-history support | Company/security name changes if available. |
| source timestamp support | Source version, snapshot date, collection timestamp, file hash or controlled reference. |
| licensing/manual-use notes | Research retention, redistribution, manual-use limits, reproducibility constraints. |
| reproducibility notes | Raw file retention, controlled references, update process, normalization notes. |
| expected coverage | Expected active ticker/date coverage, universe limits, exchange/country/security-type scope. |
| known limitations | Static-snapshot risk, missing dates, partial ticker lineage, unresolved corporate actions, stale records, manual repair burden. |
| expected allowed use | Candidate intended use such as diagnostics-only or identity/ticker lineage evaluation. |
| confidence rationale | Basis for expected confidence tier and any required manual review. |

Candidate intake can use descriptive fields, mock/source-gate manifest rows, or controlled metadata summaries. It must not require loading the real source.

## SECTION 4 - Source-Gate Evaluation Workflow

1. Create candidate source manifest.

The future evaluation task should prepare a `candidate_source_manifest.csv` from descriptive source information. This manifest should follow the existing source acceptance manifest fields and may include semantic fields such as PIT quality, confidence tier, requested use, requested domain, and conditional scope id.

2. Run schema validation.

Validate required fields, allowed enum columns, source-gate score ranges, source snapshot date presence, review timestamp presence, and manifest structure.

3. Run policy/vocab validation.

Check source status values, PIT quality values, confidence tiers, blocked reason codes, event type values where relevant, and allowed-use raw labels against the controlled vocabularies.

4. Run semantic validation.

Normalize allowed use, apply source status precedence, check manual-review conflicts, enforce rejected/deprecated/diagnostic-only blocking behavior, evaluate PIT quality and confidence, and enforce minimum source-gate score expectations.

5. Evaluate allowed-use eligibility.

Determine whether the candidate source is limited to diagnostics, can proceed to lineage evaluation, requires conditional scope, or must remain blocked. Discovery, reconstruction, and production allowed-use categories remain blocked in this phase.

6. Generate diagnostics.

Produce schema pass/fail, policy pass/fail, semantic pass/fail, allowed-use decision, conditional-scope decision, blocked reason, and manual-review queue diagnostics.

7. Produce source evaluation decision.

Produce a decision artifact using one of the approved decision classes. This decision should authorize only the next review/planning step, not source ingestion or metadata construction.

No ingestion is performed at any workflow step.

## SECTION 5 - Decision Classes

| decision | meaning | allowed next step | blocked next step | required documentation |
| --- | --- | --- | --- | --- |
| `ACCEPTED_FOR_LINEAGE_EVALUATION` | Candidate appears eligible for a future lineage-focused source evaluation or controlled mock/source-gate review. This is not final source acceptance. | Prepare a future source-specific evaluation or implementation design for identity/ticker lineage source handling. | Real source loading, ingestion, metadata construction, source acceptance, lineage construction. | Completed candidate manifest, source-gate scores, semantic eligibility decision, audit notes, allowed-use rationale. |
| `CONDITIONAL_FOR_DIAGNOSTICS_ONLY` | Candidate may support diagnostics or inspection only, or may support a narrow conditional scope not yet construction-safe. | Prepare diagnostics-only review or conditional-scope clarification. | Lineage construction, PIT tables, reconstruction, discovery support. | Conditional scope record or diagnostics-only rationale, blocked reason for construction use. |
| `MANUAL_REVIEW_REQUIRED` | Candidate has unresolved lineage, licensing, PIT-quality, coverage, identifier, or usage issues. | Open manual-review queue item and request missing information. | Source loading, ingestion, construction, reconstruction, discovery support. | Review trigger, missing information, reviewer notes, expiration/review date. |
| `REJECTED_FOR_PIT_USE` | Candidate fails a blocking PIT source-gate requirement for historical use. | Retain rejection audit record; optionally use only as non-PIT context if separately reviewed. | PIT source loading, ingestion, construction, reconstruction, discovery support. | Rejection rationale, failed checks, blocked reason, source summary. |
| `DEFERRED_PENDING_SOURCE_INFO` | Candidate cannot be evaluated because intake information is incomplete. | Request missing source description, licensing, date, identifier, coverage, or reproducibility information. | Source status upgrade, loading, ingestion, construction. | Missing information list, required next documents, review timestamp. |

Decision semantics:

- No decision class authorizes ingestion.
- No decision class authorizes real source acceptance as production or research infrastructure.
- `ACCEPTED_FOR_LINEAGE_EVALUATION` authorizes only deeper evaluation/design, not construction.

## SECTION 6 - Required Diagnostics

Required evaluation diagnostics:

- `schema_pass_fail_report`: required fields, enum columns, score ranges, missing manifest fields.
- `policy_pass_fail_report`: controlled vocabulary compliance, PIT quality classification, confidence tier compliance.
- `semantic_pass_fail_report`: semantic status/use/review/quality/score compatibility.
- `allowed_use_decision_report`: raw allowed use, canonical allowed use, requested use, eligibility decision.
- `confidence_decision_report`: confidence tier, required floor, low-confidence blocks.
- `conditional_scope_decision_report`: scope id, status, permitted/prohibited uses, domain/date/universe checks.
- `blocked_reason_report`: blocked reason, severity, source/date/domain affected.
- `manual_review_queue`: review trigger, missing information, reviewer notes, expiration/review date.
- `source_evaluation_summary`: final decision class, allowed next step, blocked next step, rationale.

Recommended diagnostic fields:

- source
- source category/type
- source version
- source snapshot date
- expected historical depth
- raw allowed use
- canonical allowed use
- source status
- requested use
- requested domain
- PIT quality
- confidence tier
- source-gate score summary
- manual review flag
- blocked reason
- decision class
- reviewer notes

## SECTION 7 - Blocking Rules

Block any further source work when:

- source is static snapshot only for historical use
- source has no effective dates and no as-of/snapshot dates
- source lacks stable identifier continuity
- source has unclear ticker lineage
- source has unresolved ticker reuse or corporate-action ambiguity
- source status is `rejected`, `deprecated`, `diagnostic_only`, or unresolved `manual_review_required`
- allowed use is unsupported or maps to `blocked`
- confidence tier is `low`, `blocked`, or `unknown` for construction use
- PIT quality is `static_snapshot_only`, `unresolved`, or `blocked`
- manual review is unresolved
- source-gate score is below required floor for PIT integrity, identifier quality, historical depth, or leakage risk
- licensing or reproducibility notes are missing
- source file hash/reference cannot be retained or reproduced
- coverage cannot be estimated or is materially unstable
- conditional source lacks a machine-readable conditional scope record

Blocking outcome:

- construction remains blocked
- ingestion remains blocked
- source loading remains blocked
- decision should be `MANUAL_REVIEW_REQUIRED`, `REJECTED_FOR_PIT_USE`, `CONDITIONAL_FOR_DIAGNOSTICS_ONLY`, or `DEFERRED_PENDING_SOURCE_INFO`

## SECTION 8 - Artifact Plan

Expected future artifact root:

`artifacts/research/point_in_time_economic_metadata_v1/source_evaluation/`

Suggested outputs:

- `candidate_source_manifest.csv`
- `source_evaluation_report.csv`
- `source_evaluation_decision.json`
- `semantic_validation_report.csv`
- `allowed_use_decision_report.csv`
- `manual_review_queue.csv`
- `blocked_reason_report.csv`
- `schema_pass_fail_report.csv`
- `policy_pass_fail_report.csv`
- `confidence_decision_report.csv`
- `conditional_scope_decision_report.csv`
- `source_evaluation_summary.json`
- `source_evaluation_manifest.json`

Manifest guardrail flags:

- `real_sources_loaded = false`
- `metadata_ingested = false`
- `source_accepted = false`
- `metadata_constructed = false`
- `lineage_constructed = false`
- `sector_history_reconstructed = false`
- `industry_history_reconstructed = false`
- `peer_groups_reconstructed = false`
- `discovery_executed = false`
- `validation_executed = false`
- `governance_modified = false`
- `production_registration = false`
- `ml_integration = false`

## SECTION 9 - Source Evaluation Success Criteria

Before moving to any source loading or lineage implementation, all of the following must be true:

- Candidate source manifest is complete.
- Schema validation passes.
- Controlled vocabulary validation passes.
- Semantic validation passes or explicitly classifies the source as manual review, rejected, conditional, or deferred.
- Allowed-use decision is no broader than `lineage_only`.
- Source status does not imply construction unless paired with accepted semantic eligibility.
- Effective-date or snapshot-date support is documented.
- Identifier and ticker-history support are documented.
- Reproducibility and licensing/manual-use notes are documented.
- Expected coverage and historical depth are documented.
- Blocking risks and manual review items are explicit.
- Source evaluation decision artifact is created.
- Guardrail manifest confirms no ingestion, no source loading, no source acceptance, no construction, no lineage build, no reconstruction, no discovery, no validation, no governance mutation, no production registration, and no ML.

Even if all success criteria pass, the result only supports a future source-loading or lineage-implementation design task. It does not authorize source loading or ingestion.

## SECTION 10 - Final Recommendation

1. Is the source-gate ready to evaluate a candidate source?

Yes. The source-gate is ready to evaluate candidate source descriptions and candidate manifest rows. It is not authorized to load or ingest real source files.

2. What information must the first source candidate provide?

The first candidate must provide source identity, category/type, historical depth, effective-date or snapshot-date support, identifier support, ticker-history support, timestamp/source-version support, licensing/manual-use notes, reproducibility notes, expected coverage, known limitations, expected allowed use, and confidence rationale.

3. What decisions can the evaluation produce?

Approved decision classes are `ACCEPTED_FOR_LINEAGE_EVALUATION`, `CONDITIONAL_FOR_DIAGNOSTICS_ONLY`, `MANUAL_REVIEW_REQUIRED`, `REJECTED_FOR_PIT_USE`, and `DEFERRED_PENDING_SOURCE_INFO`.

4. What remains blocked even after evaluation?

Real source loading, ingestion, source acceptance/rejection as final project state, metadata construction, security lineage construction, ticker lineage construction, sector/industry history, peer reconstruction, discovery, refinement, validation, governance mutation, threshold changes, production registration, ML, and alpha candidate creation remain blocked.

5. What should the next Codex task be?

The next Codex task should be **PIT Source Candidate Evaluation Scaffold v1**. It should create a source-evaluation artifact scaffold and runner modes for candidate manifest evaluation only. It should not ingest data, load real sources, accept or reject real sources, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run refinement, run validation, mutate governance, register production outputs, or implement ML.
