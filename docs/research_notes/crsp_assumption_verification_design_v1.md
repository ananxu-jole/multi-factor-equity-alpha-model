# Project Underdog - CRSP Assumption Verification Design v1

## SECTION 1 - Executive Summary

The CRSP Security Master and Ticker Lineage scaffold is complete and classified as `READY_FOR_ASSUMPTION_VERIFICATION`. The scaffold created a source-free runner, artifact tree, assumption register, source-gate manifest template, schema-alignment placeholders, diagnostics placeholders, and guardrail tests. It did not access CRSP data, load files, ingest data, construct metadata, or build lineage.

Assumption verification is required because the scaffold intentionally leaves all critical CRSP dependencies unverified. The project cannot safely move from scaffold work to source loading, ingestion, metadata construction, or lineage construction until subscription scope, licensing, field availability, date semantics, release/version lineage, and reproducibility evidence are explicitly reviewed.

What remains blocked:

- CRSP source access.
- CRSP source loading.
- Data ingestion.
- Source acceptance.
- `security_master_pit` construction.
- `ticker_lineage_pit` construction.
- `metadata_source_lineage` construction from real source evidence.
- Sector history reconstruction.
- Industry history reconstruction.
- Peer reconstruction.
- Discovery.
- Refinement.
- Validation.
- Governance mutation.
- Production registration.
- ML.

Verification objective:

Define a fail-closed review process that can move assumptions from `unverified` to `verified`, `partially_verified`, or `failed` using documented evidence only. Verification does not authorize ingestion. It only determines whether a later source-loading or ingestion-design task may be considered.

## SECTION 2 - Assumption Inventory

| assumption area | assumption | risk level | downstream dependency | blocking impact |
| --- | --- | --- | --- | --- |
| CRSP subscription scope | Subscribed CRSP scope includes identity, ticker, exchange, delisting, corporate-action, and release metadata components. | Critical | Source-gate manifest, schema alignment, security identity, ticker lineage, event lineage. | Blocks source acceptance, source loading, metadata construction, and lineage construction. |
| Licensing and retention rights | License permits research use of derived metadata artifacts and enough audit evidence for reproducibility. | Critical | Source archive/reference policy, hash strategy, metadata source lineage, audit trail. | Blocks archive, hash, source manifest acceptance, and lineage construction. |
| Archival/hash feasibility | Source hashes, source archive, or compliant controlled references can support reproducibility. | Critical | `source_file_hash`, source references, reproducible rebuilds, source-lineage diagnostics. | Blocks reproducibility, source acceptance, and lineage construction. |
| Field availability | `PERMNO`, `PERMCO`, ticker, exchange/listing context, name/security descriptors, delisting data, corporate actions, dates, and source metadata are available. | Critical | `security_master_pit`, `ticker_lineage_pit`, schema-alignment validation. | Blocks schema acceptance and PIT construction. |
| Release/version tracking | CRSP release, snapshot, or extract metadata can populate `source_version` and `source_snapshot_date`. | High | `source_acceptance_manifest`, `metadata_source_lineage`, known-date fallback. | Blocks source lineage and source acceptance. |
| Known-date semantics | Known dates can be assigned from event-level known dates or conservative release/snapshot dates. | Critical | `as_of_date`, `event_as_of_date`, stale-age policy, look-ahead prevention. | Blocks historical PIT use and downstream eligibility. |
| Event-date semantics | Event effective dates for ticker changes, delistings, mergers, acquisitions, spin-offs, relistings, and corporate actions can be identified or blocked. | High | `event_type`, `event_effective_date`, predecessor/successor fields, event confidence. | Blocks event-dependent lineage and affected ticker/security windows. |
| Ticker-window semantics | Ticker start/end evidence, exchange context, reuse behavior, and share-class/listing support can be documented. | Critical | `ticker_lineage_pit`, ticker reuse diagnostics, duplicate active mapping checks. | Blocks ticker lineage construction. |
| Source-file reproducibility | Source file references, controlled paths, checksums, row-count policy, or compliant equivalents can support reproducible review. | Critical | `metadata_source_lineage`, source-gate audit, rebuild diagnostics. | Blocks source acceptance and any reproducible PIT build. |
| Source-gate eligibility | CRSP can be assigned a source status and allowed use based on verified evidence. | Critical | Source acceptance manifest, semantic eligibility, manual-review queue. | Blocks all source work beyond diagnostics until status is no longer unresolved. |

## SECTION 3 - Verification Evidence Requirements

CRSP subscription scope:

- Acceptable evidence: subscription documentation, product entitlement summary, contract scope summary, or user-provided subscription confirmation listing available CRSP products and modules.
- Required detail: identity records, ticker history, exchange/listing history, delisting information, corporate-action/distribution data, release metadata, data dictionaries, and documentation access.
- Not acceptable: general public product descriptions alone.

Licensing and retention rights:

- Acceptable evidence: license terms, usage policy notes, internal legal/compliance summary, or user-provided retention policy confirmation.
- Required detail: whether Project Underdog may retain raw files, source references, hashes/checksums, derived metadata, row-level audit references, documentation references, and review notes.
- Not acceptable: informal assumption that research use is permitted.

Archival/hash feasibility:

- Acceptable evidence: file manifest policy, checksum strategy, controlled reference policy, approved source archive path policy, or license-compliant redacted-reference approach.
- Required detail: whether `source_file_hash` can be populated directly, replaced by controlled references, or marked unavailable with blocking status.
- Not acceptable: storing hashes without confirming license compatibility.

Field availability:

- Acceptable evidence: CRSP documentation, data dictionary references, metadata guide references, field inventory notes, or a future sample schema inspection plan.
- Required detail: `PERMNO`, `PERMCO`, ticker, exchange/listing context, company/security names, security type, delisting evidence, corporate-action evidence, date fields, and source metadata.
- Not acceptable: inspecting source files in this design phase.

Release/version tracking:

- Acceptable evidence: release note references, product version identifiers, snapshot metadata description, extract-date convention, or user-confirmed release cadence.
- Required detail: rule for deterministic `source_version` and `source_snapshot_date`.
- Not acceptable: ad hoc run timestamp as the only version.

Known-date semantics:

- Acceptable evidence: documentation identifying event-level known dates, release/snapshot dates, file production dates, or explicit policy that source release date is the conservative known-date fallback.
- Required detail: mapping rule for `as_of_date` and `event_as_of_date`.
- Not acceptable: using event effective dates as known dates without proof.

Event-date semantics:

- Acceptable evidence: documentation of event effective dates, delisting dates, corporate-action dates, and event/action codes.
- Required detail: event-type crosswalk into Project Underdog controlled event types and rules for ambiguous predecessor/successor events.
- Not acceptable: inferring mergers, acquisitions, or spin-offs solely from ticker disappearance.

Ticker-window semantics:

- Acceptable evidence: data dictionary or documentation showing ticker values, ticker date fields, exchange/listing context, share-class/listing support, and ticker reuse behavior.
- Required detail: start/end window construction rule and blocking rule for ambiguous or overlapping windows.
- Not acceptable: ticker-only joins or current ticker snapshots.

Source-file reproducibility:

- Acceptable evidence: future file manifest design, checksum policy, source bundle naming convention, row-count policy, or controlled source-reference strategy.
- Required detail: how `source_file_path`, `source_url_or_reference`, `source_file_hash`, `record_count_raw`, and `record_count_clean` can be populated or blocked.
- Not acceptable: untracked local files or undocumented manual references.

Source-gate eligibility:

- Acceptable evidence: completed source-gate manifest, semantic allowed-use review, manual-review disposition, confidence notes, and blocked reason report.
- Required detail: source status, allowed use, conditional scope if any, manual-review flag, and license notes.
- Not acceptable: treating `ACCEPTED_FOR_LINEAGE_EVALUATION` as source acceptance.

## SECTION 4 - Verification Workflow

1. Document review.

Review CRSP documentation, metadata guide references, data dictionaries, release notes, and public/project notes. The review should list evidence references but not load source files.

2. Subscription/scope confirmation.

Confirm available CRSP products, files, tables, date ranges, update cadence, and documentation access. If identity, ticker, delisting, corporate-action, or release metadata is missing, the workflow remains blocked.

3. License/retention confirmation.

Confirm rights for source references, raw files, derived artifacts, checksums, documentation references, audit notes, and retained review artifacts. If retention rights are unclear, source loading and source acceptance remain blocked.

4. Field availability confirmation.

Create a documentation-level field availability review for required security master, ticker lineage, metadata source lineage, and source acceptance manifest concepts. No source file inspection is allowed in this design.

5. Date semantics confirmation.

Review effective-date, event-date, known-date, release-date, and snapshot-date semantics. Define conservative fallback behavior. If known-date support cannot be proven, historical PIT construction remains blocked.

6. Archive/hash feasibility confirmation.

Define whether direct hashes, source-bundle hashes, controlled references, or redacted reference identifiers are permitted. Any missing reproducibility route blocks source acceptance.

7. Source-gate eligibility update.

Update CRSP source-gate eligibility from unresolved scaffold status to an evidence-backed status such as `manual_review_required`, `conditional`, `diagnostic_only`, or eligible for a future source-gate evaluation. This step does not accept the source.

8. Readiness review.

Create a review note classifying whether assumptions are `ASSUMPTIONS_UNVERIFIED`, `PARTIALLY_VERIFIED_BLOCKED`, `VERIFIED_FOR_SOURCE_LOADING_DESIGN`, or `VERIFIED_FOR_INGESTION_DESIGN`.

## SECTION 5 - Fail-Closed Rules

If CRSP subscription scope is unresolved:

- Source loading remains blocked.
- Ingestion remains blocked.
- Metadata and lineage construction remain blocked.
- Source-gate status cannot advance beyond unresolved/manual review.

If licensing or retention rights are unresolved:

- Source archive, source hash, and source manifest acceptance remain blocked.
- Source loading and ingestion remain blocked.
- Reproducible PIT construction remains blocked.

If archival/hash feasibility is unresolved:

- `metadata_source_lineage` construction remains blocked.
- Any source acceptance remains blocked.
- Rebuild/reproducibility claims remain blocked.

If field availability is unresolved:

- Schema alignment remains blocked.
- `security_master_pit` and `ticker_lineage_pit` construction remain blocked.

If release/version tracking is unresolved:

- `source_version`, `source_snapshot_date`, and lineage registry readiness remain blocked.
- Any source use beyond diagnostics remains blocked.

If known-date semantics are unresolved:

- Historical PIT use remains blocked.
- Downstream sector/industry work remains blocked.
- Peer reconstruction, discovery, and validation remain blocked.

If event-date semantics are unresolved:

- Event-dependent continuity remains blocked.
- Merger/acquisition/spin-off/relisting lineage remains blocked.

If ticker-window semantics are unresolved:

- `ticker_lineage_pit` construction remains blocked.
- Ticker reuse detection remains diagnostic-only.

If source-file reproducibility is unresolved:

- Source acceptance remains blocked.
- PIT build reproducibility remains blocked.

If source-gate eligibility is unresolved:

- Source loading, ingestion, metadata construction, lineage construction, downstream reconstruction, discovery, and validation remain blocked.

Universal fail-closed rule:

Any critical assumption that is not verified blocks source loading, ingestion, metadata construction, lineage construction, sector/industry work, peer reconstruction, discovery, and validation.

## SECTION 6 - Verification Artifacts

Expected future artifacts under `artifacts/research/crsp_security_master_ticker_lineage_pit_v1/assumptions/` or a dedicated verification subfolder:

- `crsp_assumption_verification_checklist.csv`
- `crsp_assumption_evidence_register.csv`
- `crsp_subscription_scope_review.csv`
- `crsp_license_retention_review.csv`
- `crsp_field_availability_review.csv`
- `crsp_date_semantics_review.csv`
- `crsp_archive_hash_feasibility_review.csv`
- `crsp_source_gate_eligibility_update.json`

Recommended fields for `crsp_assumption_evidence_register.csv`:

- `evidence_id`
- `assumption_id`
- `assumption_area`
- `evidence_type`
- `evidence_reference`
- `evidence_summary`
- `reviewer`
- `review_timestamp`
- `verification_status`
- `blocking_status`
- `notes`

Recommended fields for review CSVs:

- `review_item`
- `required_evidence`
- `observed_evidence`
- `verification_status`
- `risk_level`
- `blocking_status`
- `fail_closed_behavior`
- `review_notes`

The eligibility update JSON should include:

- `source`
- `source_version`
- `source_gate_status`
- `allowed_use`
- `manual_review_required`
- `verified_assumptions`
- `unverified_assumptions`
- `blocking_reasons`
- `ingestion_authorized`
- `metadata_construction_authorized`
- `lineage_construction_authorized`

The authorization flags must remain false unless a later approved task changes the project state.

## SECTION 7 - Runner / Scaffold Expectations

Expected future runner additions:

- `--list-verification-requirements`
- `--validate-assumption-evidence`
- `--update-assumption-status`
- `--export-verification-checklist`

Mode expectations:

- `--list-verification-requirements` should print required evidence by assumption id and risk level.
- `--validate-assumption-evidence` should validate evidence-register structure and ensure every critical assumption has evidence or remains blocking.
- `--update-assumption-status` should update scaffold assumption statuses only from approved evidence files, never from source data or alpha results.
- `--export-verification-checklist` should write a fresh checklist without touching CRSP source files.

Restrictions for future runner additions:

- No source loading mode.
- No ingestion mode.
- No metadata construction mode.
- No lineage construction mode.
- No discovery or validation mode.
- No production or ML mode.

Any status update that marks a critical assumption as verified without evidence must fail closed.

## SECTION 8 - Readiness Gates

`ASSUMPTIONS_UNVERIFIED`:

- Default scaffold state.
- One or more critical assumptions have no acceptable evidence.
- Source loading, ingestion, metadata construction, and lineage construction are blocked.

`PARTIALLY_VERIFIED_BLOCKED`:

- Some assumptions have acceptable evidence, but at least one critical blocker remains.
- Diagnostic review may continue.
- Source loading, ingestion, construction, discovery, and validation remain blocked.

`VERIFIED_FOR_SOURCE_LOADING_DESIGN`:

- Subscription scope, license/retention rights, archive/hash approach, and documentation access are verified enough to design a source-loading process.
- This does not authorize source loading.
- A separate source-loading design task is required.

`VERIFIED_FOR_INGESTION_DESIGN`:

- Source-loading design prerequisites, field availability, date semantics, source versioning, ticker-window semantics, event-date semantics, and source-gate eligibility are verified enough to design ingestion.
- This does not authorize ingestion.
- A separate ingestion design and review task is required.

Verification never authorizes CRSP ingestion by itself.

## SECTION 9 - Risk Assessment

License risk: Critical.

The largest non-technical blocker is whether CRSP license terms permit the required retention, hashing, derived artifacts, and audit references. If not resolved, source acceptance and construction must remain blocked.

Subscription scope risk: Critical.

The implementation depends on access to the right CRSP components. If the subscription lacks identity, ticker, delisting, corporate-action, or release metadata, the architecture cannot proceed as designed.

Field mapping risk: Critical.

Public CRSP characteristics are not enough to map strict PIT schemas. Documentation-level field availability is required before source loading or ingestion can be designed.

Known-date risk: Critical.

If known dates cannot be separated from effective dates or conservatively assigned from release/snapshot dates, historical PIT metadata would risk look-ahead contamination.

Archive/reproducibility risk: Critical.

Without source hashes, source archives, or compliant controlled references, `metadata_source_lineage` cannot support reproducible PIT construction.

False readiness risk: High.

The existence of a scaffold and prior `ACCEPTED_FOR_LINEAGE_EVALUATION` classification could be mistaken for source acceptance. This design explicitly prevents that interpretation. Assumption verification is a gate to later design, not authorization to load or ingest CRSP.

## SECTION 10 - Final Recommendation

1. Which assumptions must be verified first?

Verify licensing/retention rights, subscription scope, and archival/hash feasibility first. These determine whether source evidence can be legally and reproducibly handled at all. Field availability and date semantics should follow immediately because they determine whether the PIT schemas can be populated safely.

2. Which assumptions are critical blockers?

Critical blockers are subscription scope, licensing and retention rights, archival/hash feasibility, field availability, known-date semantics, ticker-window semantics, source-file reproducibility, and source-gate eligibility. Event-date semantics are at least high risk and become critical for event-dependent lineage.

3. What evidence is acceptable?

Acceptable evidence includes subscription documentation, license terms or usage policy notes, CRSP documentation, data dictionary references, metadata guide references, release/version metadata, documentation-level field inventory, file manifest/checksum strategy, controlled source-reference policy, and completed source-gate evidence registers. Source-file inspection is not part of this design task.

4. What remains blocked until verification?

CRSP source access, source loading, ingestion, source acceptance, metadata construction, security lineage construction, ticker lineage construction, sector/industry work, peer reconstruction, discovery, refinement, validation, governance mutation, production registration, and ML remain blocked.

5. What should the next Codex task be?

The next task should be **Project Underdog - CRSP Assumption Verification Scaffold Patch v1**. It should implement only verification-scaffold additions: evidence-register templates, verification review templates, runner modes for listing requirements and validating evidence structure, and tests. It should not access CRSP data, load source files, ingest data, accept CRSP as a source, construct metadata, build lineage, run validation, mutate governance, register production outputs, or implement ML.

