# Project Underdog - CRSP Integration Planning Gap Closure Review v1

## SECTION 1 - Executive Summary

This note reviews the unresolved CRSP integration-planning gaps identified in `crsp_integration_design_v1.md` and determines whether Project Underdog can advance from `READY_FOR_INTEGRATION_PLANNING_WITH_GAPS` to implementation design.

Current CRSP readiness status:

- CRSP has completed source-candidate evaluation with `ACCEPTED_FOR_LINEAGE_EVALUATION`.
- CRSP has completed lineage design review with `SUITABLE_FOR_INTEGRATION_DESIGN`.
- CRSP integration design classified the state as `READY_FOR_INTEGRATION_PLANNING_WITH_GAPS`.
- CRSP is not accepted as a source, not authorized for ingestion, and not authorized for metadata or lineage construction.

Unresolved gaps:

- Field-level mapping uncertainty.
- Known-date and effective-date semantics.
- Source lineage and version tracking.
- Licensing, retention, and archival constraints.
- Subscription product scope.
- Event-window and ticker-window representation.
- Source-file hash and archive feasibility.

Readiness conclusion:

The remaining gaps do not prevent a CRSP-specific implementation design from being drafted, provided the design is explicitly assumption-bound, fail-closed, and does not access or load source files. They do prevent implementation execution, source acceptance, ingestion, PIT construction, and downstream use. The implementation design must include verification gates for licensed documentation, subscription scope, date semantics, license/retention rights, and source-lineage reproducibility before any build step.

Final readiness classification: `READY_FOR_IMPLEMENTATION_DESIGN_WITH_ASSUMPTIONS`.

## SECTION 2 - Gap Inventory

| gap | prior severity | closure classification | rationale |
| --- | --- | --- | --- |
| Field-level mapping uncertainty | Critical | Implementation-design blocker unless handled as a design assumption | Exact fields are required before implementation execution, but an implementation design can define expected mapping slots, unresolved fields, and fail-closed validation gates without loading CRSP data. |
| Known-date semantics | Critical | Implementation-design blocker unless handled as a design assumption | Look-ahead protection is central. Design may proceed only if it requires conservative `as_of_date` handling and blocks rows where known-date semantics cannot be verified. |
| Source lineage and version tracking | Moderate/Critical adjacent | Implementation-time risk | The source-gate framework already requires `source_version`, `source_snapshot_date`, `source_file_hash`, lineage references, and license notes. CRSP-specific design must specify how these will be populated or blocked. |
| Licensing / retention / archival constraints | Critical | Implementation-time blocker, not design blocker | License terms must be verified before source acceptance, local retention, hashing, or execution. A design can include license-review requirements and alternate redacted-reference paths. |
| Subscription scope | Critical | Implementation-time blocker, not design blocker | Product/table availability must be confirmed before execution. Design can list required product components and fail if unavailable. |
| Event-window representation | Critical | Implementation-design blocker unless handled as a design assumption | Design must define allowed event-window strategies, including explicit, inferred, and blocked cases. Execution cannot proceed until actual CRSP event semantics are verified. |
| Ticker-window representation | Critical | Implementation-design blocker unless handled as a design assumption | Ticker windows are essential to `ticker_lineage_pit`. Design can proceed if it requires exact field verification and blocks ambiguous windows. |
| Source-file hash/archive feasibility | Critical | Implementation-time blocker, not design blocker | Hash/archive feasibility must be verified before source acceptance and reproducible builds. Design can specify required fields and fallback audit references. |
| Internal id namespace policy | Moderate | Non-blocking | A design can freeze `crsp_permno` and `crsp_permco` namespace conventions without source access. |
| Share-class and primary listing policy | Moderate | Implementation-design risk | Design should include policy and diagnostics; exact mapping remains source-documentation dependent. |
| Exchange-code normalization | Moderate | Implementation-design risk | Design can specify normalization workflow and unresolved mapping table requirements. |
| Null and unknown representation | Minor | Documentation-only risk | Existing PIT policy already requires explicit null/unknown handling with confidence reduction or blocking. |

No reviewed gap supports moving directly to implementation execution. Several gaps can be closed inside the implementation design document as explicit assumptions and verification gates.

## SECTION 3 - Field Mapping Gap Review

Expected CRSP entities:

- `PERMNO` as the expected source-native security or issue continuity identifier.
- `PERMCO` as the expected source-native company or issuer continuity identifier.
- Historical ticker, name, exchange, active/inactive, delisting, and corporate-action records or descriptors.
- Release, guide, metadata, and flat-file references sufficient to support source-lineage planning.

Expected identifier fields:

- `PERMNO` should map conceptually to a namespaced internal `security_id`.
- `PERMCO` should map conceptually to a namespaced internal `issuer_id`.
- Ticker symbols should map only into dated ticker windows.
- Supporting identifiers should remain source evidence and should not override permanent identifiers without review.

Expected ticker/date fields:

- Ticker value.
- Exchange or listing context.
- Security identifier link to `PERMNO`.
- Start and end date evidence for ticker windows.
- Source release, snapshot, or known-date evidence for `as_of_date`.

Expected delisting/corporate-action fields:

- Delisting date and status/reason evidence.
- Corporate-action event type or action code evidence.
- Event effective date evidence.
- Evidence sufficient to decide whether predecessor/successor links are explicit, inferred, or blocked.

Mapping uncertainty:

Field mapping uncertainty remains real and material. It blocks implementation execution and source acceptance. It does not fully block implementation design because the next design can be written as a mapping specification with required CRSP documentation inputs, expected fields, unresolved mapping placeholders, confidence rules, and failure modes.

Decision:

Field mapping uncertainty is an implementation-design blocker only if the next task attempts to produce executable mappings. It is not a blocker to a review-only or design-only implementation specification that explicitly marks unknown fields and requires source-documentation verification before execution.

## SECTION 4 - Known-Date and Effective-Date Gap Review

Event date:

Event dates describe the economic date of ticker changes, delistings, mergers, acquisitions, spin-offs, name changes, exchange changes, and related corporate actions. They cannot be used as known dates unless documentation proves they were available as of that date.

Effective date:

Effective dates define when a security, ticker, exchange, name, or event state became economically true. `security_master_pit.effective_start`, `security_master_pit.effective_end`, `ticker_lineage_pit.ticker_effective_start`, and `ticker_lineage_pit.ticker_effective_end` require this concept.

Source release date:

Source release date may be the safest known-date proxy if event-level known dates are not available. If release date is used as `as_of_date`, the design must treat earlier event-effective dates as historical facts only known at the release date.

Known date:

Known date is the earliest date Project Underdog can safely say the source information was available for use. It may be event-level, file-level, release-level, or source-snapshot-level, depending on CRSP documentation and license-compatible archival evidence.

Backfill risk:

Backfill risk is high if a current or later CRSP extract supplies historical event dates without explicit source-known dates. The implementation design must require conservative known-date assignment and block downstream eligibility where `as_of_date` cannot be determined.

Required assumptions for implementation design:

- `as_of_date` must never be earlier than the source release or snapshot date unless CRSP documentation supports event-level known dates.
- Effective dates and known dates must be stored separately.
- Inferred windows must receive confidence penalties and diagnostics.
- Rows with missing `as_of_date` must be blocked from downstream historical use.
- Rows with ambiguous event windows must be `diagnostic_only`, `manual_review_required`, or blocked.

Decision:

Known-date and effective-date gaps are true blockers to execution, but can be addressed during implementation design through explicit conservative assumptions and fail-closed rules.

## SECTION 5 - Licensing and Archival Gap Review

Licensing uncertainty:

Licensing remains a critical unresolved dependency. CRSP terms must be reviewed before source files, row-level hashes, raw extracts, retained documentation, or derived audit artifacts are stored or shared.

Retention rights:

The project must verify whether it may retain raw files, transformed intermediate files, record-level evidence bundles, source hashes, source documentation snapshots, and derived PIT artifacts.

Source archive feasibility:

Reproducible PIT metadata requires either a controlled archive of source files or stable controlled references to source versions. If raw file archival is not allowed, the implementation design must define a compliant reference-only lineage strategy.

Source hash feasibility:

`source_acceptance_manifest` and `metadata_source_lineage` expect source-file hash support. If hashing raw files is prohibited or impractical, the design must define an approved alternative such as redacted hash notes, source-bundle checksums retained only locally, or controlled reference identifiers.

Reproducibility risk:

Reproducibility risk remains high until license-compatible archive and hash rules are known. Without reproducible source lineage, CRSP cannot be accepted for PIT construction.

Decision:

Licensing and archival gaps block source acceptance and implementation execution. They do not block implementation design if the design includes a mandatory license-verification gate and a fallback path that blocks all build modes when retention rights are insufficient.

## SECTION 6 - Subscription Scope Review

Product scope to confirm:

- The specific CRSP U.S. Stock Database products available.
- Whether the subscription includes daily, monthly, event, delisting, distribution, identifying, and metadata components needed for identity and ticker lineage.
- Whether release notes, user guides, metadata guides, and data dictionaries are accessible.
- Whether source releases or snapshots can be referenced consistently.

Files/tables that may be required:

- Security identifying information.
- Company and issue identifiers.
- Historical ticker and name information.
- Exchange/listing history.
- Delisting information.
- Corporate-action and distribution information.
- Source metadata, release, and documentation files.

Missing subscription components that would block later implementation:

- Missing `PERMNO` or equivalent permanent issue identifier.
- Missing `PERMCO` or equivalent company identifier if issuer continuity is required.
- Missing historical ticker records.
- Missing delisting records.
- Missing source release or snapshot metadata.
- Missing documentation sufficient to define date semantics.
- Missing license permission to retain source-lineage evidence.

Decision:

Subscription scope verification is an implementation-time blocker and a design assumption. Implementation design may proceed if it lists required components and marks unavailable components as blocking conditions.

## SECTION 7 - Source Lineage and Versioning Review

Required lineage fields:

- `source`.
- `source_type`.
- `source_version`.
- `source_snapshot_date`.
- `source_file_path` or controlled source reference.
- `source_url_or_reference`.
- `source_file_hash` or approved equivalent.
- Raw and clean record counts.
- `collection_timestamp`.
- `license_or_usage_notes`.
- `normalization_rules`.
- `source_confidence`.
- `point_in_time_quality`.

Source-version tracking:

The current source-gate framework is sufficient at the schema and semantic level. It already requires source manifest status, allowed use, manual-review flags, source version, source snapshot date, source hash, confidence support, and semantic eligibility decisions. What remains is CRSP-specific: defining a deterministic `source_version` convention from product, release, snapshot, extract, and source-bundle evidence.

Current framework sufficiency:

The source-gate framework is sufficient for implementation design. It is not sufficient to accept CRSP without a populated CRSP source manifest, license notes, source-version policy, and hash/archive decision.

Decision:

Source lineage and versioning are not blockers to implementation design. They are required design outputs and later execution gates.

## SECTION 8 - Readiness Decision

Can Project Underdog begin CRSP implementation design without accessing CRSP source files?

Yes, with assumptions.

Implementation design can begin without source-file access if it is constrained to:

- Field mapping specification using expected CRSP entities and documented project requirements.
- Source manifest design.
- Identifier namespace policy for `PERMNO` and `PERMCO`.
- Date semantics policy for event, effective, source release, and known dates.
- Ticker-window and event-window construction rules.
- Source-lineage and source-versioning requirements.
- License and subscription verification checklist.
- Fail-closed diagnostics and blocking conditions.

Required assumptions:

- CRSP documentation can be reviewed before execution.
- The subscribed CRSP package includes the tables needed for identity, ticker, delisting, corporate-action, and source-release lineage.
- `PERMNO` and `PERMCO` are available and usable as source-native identifiers.
- Source release or snapshot metadata can support conservative `as_of_date` assignment.
- Licensing permits at least enough source reference, hash, or audit evidence to satisfy reproducibility requirements.
- Any field or date semantics not verified during design must remain blocked from execution.

Exact blockers to execution:

- No accepted CRSP source manifest.
- No verified license/retention policy.
- No verified subscription scope.
- No finalized field mapping.
- No finalized known-date policy.
- No approved source hash/archive or equivalent reference policy.
- No executable source-gate decision permitting PIT construction.

## SECTION 9 - Final Classification

Final classification: `READY_FOR_IMPLEMENTATION_DESIGN_WITH_ASSUMPTIONS`.

Rationale:

CRSP has cleared enough planning uncertainty to justify a CRSP-specific implementation design. The remaining gaps are now well-scoped design assumptions, verification gates, or implementation-time blockers rather than reasons to stop design work. However, those same gaps still prevent source acceptance, source loading, ingestion, metadata construction, lineage construction, validation, downstream reconstruction, and discovery.

The implementation design must be explicit that it is conditional. It should define required CRSP fields, date policies, source-lineage requirements, diagnostics, and blocking behavior, but it must not assume source acceptance or execution readiness.

The classification is not `READY_FOR_IMPLEMENTATION_DESIGN` because license, subscription, field-level, known-date, and archive/hash issues remain unverified. It is not `NOT_READY_FOR_IMPLEMENTATION_DESIGN` because the existing architecture, source-gate scaffold, semantic validation framework, and CRSP lineage review provide enough structure to design safely under assumptions.

## SECTION 10 - Final Recommendation

1. Which gaps are true blockers?

True blockers to implementation execution and source acceptance are licensing/retention rights, subscription scope, finalized field mapping, known-date semantics, event/ticker-window semantics, and source hash/archive or equivalent lineage feasibility. None of these should be bypassed.

2. Which gaps can be handled during implementation design?

Field mapping, identifier namespace policy, event-window rules, ticker-window rules, known-date fallback logic, source-version conventions, source manifest structure, diagnostics, confidence rules, and null/unknown handling can be handled during implementation design as long as unresolved items remain explicit and fail closed.

3. Which gaps require user/subscription verification?

User or subscription verification is required for exact CRSP product scope, available files/tables, licensed documentation access, data dictionary access, release/snapshot metadata, retention rights, source hashing rights, source archive rights, and permitted derived artifact retention.

4. Is implementation design justified now?

Yes. A CRSP-specific implementation design is justified now under assumptions. It must remain design-only and cannot authorize ingestion, source acceptance, metadata construction, lineage construction, or downstream use.

5. What should remain blocked?

Source acceptance, source loading, CRSP data ingestion, `security_master_pit` construction, `ticker_lineage_pit` construction, sector/industry history reconstruction, peer reconstruction, discovery, validation, governance mutation, production registration, and ML remain blocked.

6. What should the next Codex task be?

The next task should be **Project Underdog - CRSP Implementation Design v1**. It should define the CRSP-specific implementation design under explicit assumptions: schema mapping plan, required source manifest fields, `PERMNO`/`PERMCO` namespace rules, date and known-date policy, ticker-window and event-window construction rules, source-lineage/version/hash policy, diagnostics, blocking rules, and verification checklist. It should not ingest CRSP data, load source files, access subscribed datasets, construct metadata, build lineage, run validation, mutate governance, or register production outputs.

