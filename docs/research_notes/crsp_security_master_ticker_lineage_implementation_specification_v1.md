# Project Underdog - CRSP Security Master and Ticker Lineage Implementation Specification v1

## SECTION 1 - Executive Summary

This note freezes the implementation specification for a future CRSP-backed scaffold supporting `security_master_pit`, `ticker_lineage_pit`, `metadata_source_lineage`, and source-gate integration. It is specification-only. No code was implemented, no CRSP data was accessed, no CRSP files were loaded, no metadata was constructed, and no lineage was built.

Specification scope:

- Define CRSP-specific scaffold deliverables.
- Define the future CRSP runner surface.
- Define artifact folders and expected placeholder outputs.
- Freeze schema expectations and diagnostic requirements.
- Define assumption verification gates.
- Preserve fail-closed controls before any source loading or PIT construction.

Implementation objective:

The first implementation should create a CRSP-specific scaffold and verification framework only. It should let Project Underdog list assumptions, validate source-gate readiness, validate schema alignment, validate assumption state, and produce diagnostic placeholders without accepting CRSP as a source or touching CRSP data.

Assumptions:

- CRSP remains `ACCEPTED_FOR_LINEAGE_EVALUATION`, not accepted for source ingestion.
- CRSP architecture is defined with assumptions through `crsp_security_master_ticker_lineage_implementation_design_v1.md`.
- `PERMNO` and `PERMCO` remain conceptual identifiers only until field availability and license terms are verified.
- Source version, source snapshot date, known-date semantics, source hash/archive feasibility, and subscription scope remain unverified.

Non-goals:

- No source access.
- No CRSP file loading.
- No ingestion.
- No source acceptance.
- No metadata construction.
- No security lineage construction.
- No ticker lineage construction.
- No sector, industry, or peer reconstruction.
- No discovery, refinement, validation, governance mutation, production routing, or ML.

Readiness status:

The CRSP scope is ready for scaffold implementation, not data implementation.

Final classification: `READY_FOR_SCAFFOLD_IMPLEMENTATION`.

## SECTION 2 - Deliverable Inventory

| deliverable | purpose | required fields or outputs | dependencies | blocking assumptions |
| --- | --- | --- | --- | --- |
| CRSP source acceptance manifest scaffold | Provide a CRSP-specific source-gate manifest template without source acceptance. | `source_gate_run_id`, `source`, `source_type`, `source_version`, `source_snapshot_date`, `source_file_hash`, score fields, `source_gate_status`, `allowed_use`, `rejection_reason`, `manual_review_required`, `license_or_usage_notes`, `review_timestamp`, `reviewer_notes`. | Existing source-gate schema and semantic validation framework. | License, source version, source hash, product scope, and manual-review status remain unverified. |
| CRSP source-lineage registry | Define placeholder lineage requirements for future CRSP source references. | `source_lineage_id`, `run_id`, `metadata_version`, `source`, `source_type`, `source_version`, `source_snapshot_date`, `source_file_path`, `source_url_or_reference`, `source_file_hash`, record counts, `collection_timestamp`, `license_or_usage_notes`, `normalization_rules`, `source_confidence`, `point_in_time_quality`, notes. | `metadata_source_lineage` schema. | Archive/hash/reference feasibility and license retention rights. |
| CRSP security master PIT schema alignment | Verify future CRSP scaffold fields align to `security_master_pit`. | Required field checklist, lineage field checklist, effective-date checklist, confidence checklist, blocking field checklist. | PIT schema specification and CRSP implementation architecture. | CRSP field availability, known-date semantics, and source-record id strategy. |
| CRSP ticker lineage PIT schema alignment | Verify future CRSP scaffold fields align to `ticker_lineage_pit`. | Required field checklist, ticker-window checklist, ticker reuse controls, confidence checklist, blocking field checklist. | PIT schema specification and CRSP implementation architecture. | Ticker-window fields, exchange/share-class fields, ticker reuse evidence, and known-date semantics. |
| CRSP diagnostics scaffold | Produce placeholder diagnostics for later source evaluation and implementation readiness. | Source-gate report, schema-alignment report, assumption-status report, field-mapping coverage report, effective-date readiness report, known-date readiness report, ticker-window readiness report, lineage-confidence readiness report, blocked-reason report. | Existing diagnostic vocabulary and CRSP architecture. | No real rows; all diagnostics remain scaffold-only until source acceptance. |
| CRSP runner scaffold | Provide a command-line surface for scaffold validation only. | `--dry-run`, `--list-assumptions`, `--validate-source-gate`, `--validate-schema-alignment`, `--validate-assumptions`, `--validate-diagnostics`. | Future `pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py`. | No ingestion or build modes permitted. |
| CRSP assumption verification checklist | Freeze assumptions and evidence requirements. | Assumption id, area, requirement, required evidence, status, risk level, blocking status, fail-closed behavior, review notes. | Assumption register from architecture note. | User/subscription/license verification not yet complete. |
| CRSP implementation review note | Document scaffold implementation outcome in a later task. | Files created, artifacts created, runner modes, tests, guardrails, classification, next task. | Future scaffold implementation. | Should not claim source acceptance or construction readiness. |

## SECTION 3 - Runner Specification

Future runner:

`pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py`

Allowed scaffold modes:

- `--dry-run`: report planned CRSP scaffold artifacts, blocked phases, and current classification without writing source-derived data.
- `--list-assumptions`: list CRSP assumptions, risk levels, required evidence, and fail-closed behavior.
- `--validate-source-gate`: validate CRSP manifest scaffold shape, allowed source status values, allowed-use values, manual-review fields, and blocked status defaults.
- `--validate-schema-alignment`: validate that scaffold schema checklists cover all required `security_master_pit`, `ticker_lineage_pit`, `metadata_source_lineage`, and `source_acceptance_manifest` fields.
- `--validate-assumptions`: validate assumption register completeness and ensure unverified critical assumptions remain blocking.
- `--validate-diagnostics`: validate that diagnostic placeholder files exist and contain required columns.

Prohibited modes:

- No `--ingest`.
- No `--load-source`.
- No `--build-lineage`.
- No `--construct-metadata`.
- No `--reconstruct-sector-history`.
- No `--reconstruct-industry-history`.
- No `--reconstruct-peer-groups`.
- No `--run-discovery`.
- No `--run-validation`.

Runner behavior:

- All modes must be deterministic and source-free.
- Any attempt to provide CRSP source file paths should fail or be ignored with a blocking diagnostic.
- Validation may inspect only scaffold artifacts and project schemas, not CRSP source files.
- Exit success is allowed only for scaffold completeness, not source readiness.

## SECTION 4 - Artifact Structure

Future artifact root:

`artifacts/research/crsp_security_master_ticker_lineage_pit_v1/`

Required subfolders:

- `source_gate/`
- `schemas/`
- `assumptions/`
- `diagnostics/`
- `lineage_design/`
- `validation_reports/`
- `manifests/`
- `review/`

Expected scaffold artifacts:

| path | purpose |
| --- | --- |
| `source_gate/crsp_source_acceptance_manifest_template.csv` | CRSP-specific source-gate manifest template. |
| `source_gate/crsp_source_gate_status_report.csv` | Placeholder report showing source-gate readiness and blocked assumptions. |
| `schemas/security_master_pit_alignment_checklist.csv` | Required field and validation checklist for security master alignment. |
| `schemas/ticker_lineage_pit_alignment_checklist.csv` | Required field and validation checklist for ticker lineage alignment. |
| `schemas/metadata_source_lineage_alignment_checklist.csv` | Required source-lineage field checklist. |
| `schemas/source_acceptance_manifest_alignment_checklist.csv` | Required manifest field checklist. |
| `assumptions/crsp_assumption_register.csv` | Machine-readable assumption register. |
| `assumptions/crsp_assumption_verification_checklist.csv` | Evidence and verification checklist. |
| `diagnostics/crsp_diagnostic_manifest.json` | Inventory of expected diagnostics. |
| `diagnostics/field_mapping_coverage_report.csv` | Placeholder field-mapping coverage diagnostics. |
| `diagnostics/effective_date_readiness_report.csv` | Placeholder effective-date readiness diagnostics. |
| `diagnostics/known_date_readiness_report.csv` | Placeholder known-date readiness diagnostics. |
| `diagnostics/ticker_window_readiness_report.csv` | Placeholder ticker-window readiness diagnostics. |
| `diagnostics/lineage_confidence_readiness_report.csv` | Placeholder confidence diagnostics. |
| `diagnostics/blocked_reason_report.csv` | Placeholder blocked reason diagnostics. |
| `lineage_design/identifier_strategy_manifest.json` | Namespaced `PERMNO`/`PERMCO` strategy declaration. |
| `validation_reports/scaffold_validation_report.csv` | Runner scaffold validation output. |
| `manifests/crsp_scaffold_manifest.json` | Top-level scaffold manifest. |
| `review/crsp_scaffold_implementation_review_template.md` | Template for later implementation review. |

No artifact may contain CRSP source rows, CRSP source extracts, constructed PIT rows, or lineage outputs.

## SECTION 5 - Schema Specification

`security_master_pit` expectations:

- Key fields: `security_id`, `effective_start`, `source`, `metadata_version`.
- Required identity fields: `security_id`, `issuer_id`, `company_name`, `security_type`, `exchange`, `country`, `currency`, `is_active`.
- Effective-date fields: `effective_start`, `effective_end`, `as_of_date`.
- Lineage fields: `source`, `source_version`, `source_record_id`, `metadata_version`, `run_id`, `collection_timestamp`, `record_hash`.
- Confidence fields: `identity_confidence`, `event_confidence`, `point_in_time_quality`, `manual_override_flag`.
- Event fields: `security_event_id`, `event_type`, `event_effective_date`, `event_as_of_date`, `predecessor_security_id`, `successor_security_id`, `prior_ticker`, `next_ticker`.
- Blocking fields or derived checks: missing `PERMNO`, missing effective date, missing as-of date, unresolved event lineage, low confidence, missing accepted source lineage.

`ticker_lineage_pit` expectations:

- Key fields: `security_id`, `ticker`, `exchange`, `ticker_effective_start`.
- Required ticker fields: `security_id`, `ticker`, `exchange`, `ticker_namespace`, `share_class`, `primary_listing_flag`, `ticker_status`, `change_reason`.
- Effective-date fields: `ticker_effective_start`, `ticker_effective_end`, `as_of_date`.
- Lineage fields: `source`, `source_version`, `metadata_version`, `run_id`, `collection_timestamp`, `record_hash`, `prior_ticker`, `next_ticker`.
- Confidence fields: `ticker_mapping_confidence`, `point_in_time_quality`, `manual_override_flag`.
- Blocking fields or derived checks: missing ticker start, overlapping ticker windows, duplicate active mapping, recycled ticker ambiguity, unresolved identity link, missing known date.

`metadata_source_lineage` expectations:

- Required source fields: `source_lineage_id`, `run_id`, `metadata_version`, `source`, `source_type`, `source_version`, `source_snapshot_date`.
- Reference fields: `source_file_path`, `source_url_or_reference`, `source_file_hash`.
- Audit fields: `record_count_raw`, `record_count_clean`, `collection_timestamp`, `license_or_usage_notes`, `normalization_rules`, `created_by`, `source_gate_score_summary`, `notes`.
- Confidence fields: `source_confidence`, `point_in_time_quality`, `manual_source_flag`.
- Blocking checks: missing source version, missing snapshot/release date, missing hash/reference strategy, missing license notes, missing normalization rules.

`source_acceptance_manifest` expectations:

- Key fields: `source_gate_run_id`, `source`, `source_version`.
- Source description fields: `source_type`, `source_snapshot_date`, `source_file_hash`.
- Score fields: `pit_integrity_score`, `coverage_score`, `historical_depth_score`, `identifier_quality_score`, `update_feasibility_score`, `source_stability_score`, `implementation_complexity_score`, `cost_manual_burden_score`, `leakage_risk_score`.
- Semantic fields: `source_gate_status`, `allowed_use`, `rejection_reason`, `manual_review_required`.
- Audit fields: `license_or_usage_notes`, `review_timestamp`, `reviewer_notes`.
- Blocking checks: source not accepted, unsupported allowed use, unresolved manual review, missing license notes, missing source hash/reference strategy.

`assumption_register` expectations:

- Required fields: `assumption_id`, `assumption_area`, `assumption`, `rationale`, `required_evidence`, `verification_status`, `risk_level`, `blocking_status`, `fail_closed_behavior`, `review_notes`.
- Valid `verification_status`: `unverified`, `partially_verified`, `verified`, `failed`.
- Valid `risk_level`: `critical`, `high`, `moderate`, `minor`.
- Critical or high assumptions that are not `verified` must remain blocking.

Diagnostics output expectations:

- Required fields: `diagnostic_id`, `diagnostic_scope`, `status`, `severity`, `blocked_reason`, `required_evidence`, `current_evidence`, `next_action`, `review_notes`.
- All placeholder diagnostics must indicate that no CRSP data was evaluated.

## SECTION 6 - Assumption Verification Specification

| assumption | required evidence | blocking status | fail-closed behavior |
| --- | --- | --- | --- |
| CRSP subscription scope | User/subscription confirmation of available CRSP products, files/tables, historical coverage, and documentation. | Critical blocker. | Source-gate status remains `manual_review_required` or `diagnostic_only`; no source loading. |
| License and retention rights | License review covering local retention, derived artifacts, source references, file hashes, documentation references, and audit records. | Critical blocker. | No archive, hash, source manifest acceptance, or lineage construction. |
| Field availability | Documentation-level inventory for `PERMNO`, `PERMCO`, ticker, exchange, name/security descriptors, delisting, corporate actions, dates, and source metadata. | Critical blocker. | Schema alignment remains incomplete; source acceptance blocked. |
| Release/version tracking | Evidence of CRSP release, snapshot, extract, or documentation version identifiers. | High blocker. | `source_version` and `source_snapshot_date` remain unverified; lineage blocked. |
| Known-date semantics | Evidence showing event-level known dates or approved release/snapshot-date fallback. | Critical blocker. | Rows cannot be date-safe; historical PIT use blocked. |
| Event-date semantics | Documentation of event effective dates for ticker changes, delistings, mergers, acquisitions, spin-offs, relistings, or corporate actions. | High blocker. | Event-dependent lineage remains `manual_review_required` or blocked. |
| Ticker-window semantics | Documentation of ticker start/end evidence, exchange context, reuse behavior, and share-class/listing support. | Critical blocker. | `ticker_lineage_pit` construction blocked. |
| Source hash/archive feasibility | License-compatible hash, archive, or controlled-reference policy. | Critical blocker. | Reproducibility blocked; source acceptance blocked. |

## SECTION 7 - Diagnostics Specification

Required diagnostics:

- Source-gate result: reports CRSP source status, allowed use, manual-review state, license notes, and source-gate blocking reasons.
- Schema alignment result: reports whether every required field in each target schema has a planned CRSP mapping, explicit unknown, or blocking rule.
- Assumption status: reports all assumptions by verification status, risk level, and blocking status.
- Field mapping coverage: reports planned coverage by security identity, company identity, ticker, exchange, name, delisting, corporate action, date, and source-lineage domains.
- Effective-date readiness: reports whether effective start/end concepts are verified, inferred, missing, or blocked.
- Known-date readiness: reports whether event-level known dates or release/snapshot fallback are available.
- Ticker-window readiness: reports ticker start/end readiness, exchange/share-class support, reuse controls, and overlap blockers.
- Lineage-confidence readiness: reports confidence floor readiness for identity, ticker mapping, event lineage, source confidence, and PIT quality.
- Blocking reasons: reports blockers using the existing vocabulary, including `missing_effective_date`, `missing_as_of_date`, `overlapping_ticker_window`, `duplicate_active_mapping`, `unresolved_security_identity`, `recycled_ticker_ambiguity`, `low_confidence_lineage`, `source_rejected`, `manual_review_required`, `static_snapshot_only`, `unresolved_event_lineage`, and `unsupported_domain`.

Diagnostics rules:

- Scaffold diagnostics may pass only for file structure and required columns.
- Any unverified critical assumption must appear in blocked diagnostics.
- Diagnostics must never imply CRSP source acceptance.
- Diagnostics must explicitly state that no source rows were evaluated.

## SECTION 8 - Test Specification

Future scaffold tests should verify:

- Runner mode tests: `--dry-run`, `--list-assumptions`, `--validate-source-gate`, `--validate-schema-alignment`, `--validate-assumptions`, and `--validate-diagnostics` execute successfully.
- Artifact structure tests: required folders and placeholder files exist under `artifacts/research/crsp_security_master_ticker_lineage_pit_v1/`.
- Assumption-register tests: required assumption fields exist, critical assumptions default to unverified/blocking, and invalid statuses fail.
- Source-gate schema tests: CRSP source manifest scaffold includes all required source acceptance fields and rejects invalid source status or allowed-use values.
- Diagnostics placeholder tests: each required diagnostic exists, includes required columns, and marks itself scaffold-only.
- Fail-closed behavior tests: unverified critical assumptions block source acceptance, source loading, metadata construction, and lineage construction.
- No-ingestion guardrail tests: runner exposes no ingestion/build modes and rejects or ignores source-file path inputs.
- Schema-alignment tests: security master, ticker lineage, source lineage, and source manifest checklists cover all required fields.

No future test should require CRSP files, real source rows, subscribed data access, metadata construction, lineage construction, discovery, or validation.

## SECTION 9 - Fail-Closed Controls

The scaffold must block ingestion until:

- CRSP source status is accepted through a later approved source-gate task.
- License and retention rights are verified.
- Source file/reference and hash/archive strategy are approved.

The scaffold must block source loading until:

- A later task explicitly authorizes source loading.
- Source paths and references are validated.
- Source loading mode exists in a separately approved runner.

The scaffold must block metadata construction until:

- Field mappings are finalized.
- Source lineage is accepted.
- Assumptions are verified.
- Schema alignment passes.

The scaffold must block lineage construction until:

- `security_master_pit` and `ticker_lineage_pit` construction modes are explicitly approved.
- Known-date and effective-date rules are verified.
- Ticker-window and event-window rules are verified.
- Confidence and blocking diagnostics are implemented.

The scaffold must block sector, industry, and peer reconstruction until:

- Identity and ticker lineage are constructed, reviewed, and accepted for downstream design.
- Separate sector/industry/peer source design tasks are approved.

The scaffold must block discovery and validation until:

- PIT metadata construction exists.
- Diagnostics pass.
- A separate readiness review authorizes discovery or validation.

The scaffold must block production use until:

- Governance explicitly authorizes production registration in a future task.

## SECTION 10 - Implementation Sequence

Phase 1: CRSP scaffold implementation only.

- Create runner scaffold.
- Create artifact tree.
- Create placeholder manifests, checklists, assumption register, diagnostics, and review template.
- Add guardrail tests.
- No CRSP source access.

Phase 2: Assumption verification framework.

- Implement validation for assumption status, evidence fields, risk levels, and blocking defaults.
- Critical and high assumptions remain blocking until verified.
- No source loading.

Phase 3: Source-gate manifest completion.

- Populate a CRSP manifest scaffold with placeholder/unverified values.
- Validate manifest shape and semantic status.
- Do not accept CRSP as a source.

Phase 4: Schema-alignment validation.

- Validate required field coverage checklists.
- Mark unknown field mappings as blocked or manual-review required.
- Do not construct schemas or PIT rows.

Phase 5: Implementation readiness review.

- Review scaffold implementation, artifact completeness, tests, guardrails, and remaining assumptions.
- Decide whether source-documentation review or source-gate evaluation can proceed.
- No data loading yet.

## SECTION 11 - Explicit Non-Goals

This specification excludes:

- CRSP file loading.
- CRSP ingestion.
- CRSP source acceptance.
- Metadata construction.
- Security lineage construction.
- Ticker lineage construction.
- `metadata_source_lineage` construction from real source evidence.
- Sector history reconstruction.
- Industry history reconstruction.
- Peer reconstruction.
- Alpha discovery.
- Refinement.
- Validation.
- Production routing.
- Governance mutation.
- Threshold changes.
- ML.

## SECTION 12 - Final Recommendation

1. Is the CRSP implementation scope fully specified?

Yes, for scaffold implementation. The scope is fully specified as a CRSP-specific scaffold and assumption verification framework with runner modes, artifact layout, schema checklists, diagnostic placeholders, tests, and fail-closed controls. It is not a specification for source loading or PIT construction.

2. What remains assumption-bound?

Subscription scope, license and retention rights, source archive feasibility, source hash feasibility, field availability, release/version tracking, known-date semantics, event-date semantics, ticker-window semantics, source-record id strategy, and future source-gate acceptance remain assumption-bound.

3. What must remain blocked?

Source access, CRSP file loading, ingestion, source acceptance, metadata construction, security lineage construction, ticker lineage construction, sector/industry/peer reconstruction, discovery, refinement, validation, governance mutation, production registration, and ML must remain blocked.

4. Is scaffold implementation justified?

Yes. Scaffold implementation is justified because the architecture is defined with assumptions and the next safe step is to create source-free structure, manifests, checklists, diagnostics, runner validation modes, and tests.

5. What should the next Codex task be?

The next task should be **Project Underdog - CRSP Security Master and Ticker Lineage Scaffold Implementation v1**. It should implement only the CRSP scaffold, artifact tree, assumption register, source-gate manifest template, schema-alignment checklists, diagnostic placeholders, runner validation modes, tests, and implementation review note. It should not access CRSP data, load files, ingest data, accept CRSP as a source, construct metadata, build lineage, reconstruct sector/industry/peer groups, run discovery, run validation, mutate governance, register production outputs, or implement ML.

