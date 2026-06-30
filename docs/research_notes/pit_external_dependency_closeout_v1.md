# Project Underdog - PIT External Dependency Closeout v1

## SECTION 1 - Executive Summary

This note formally closes the current point-in-time metadata planning phase and documents the external dependencies that must be satisfied before implementation resumes.

Classification: `PIT_READY_PENDING_EXTERNAL_LICENSE`.

Current source-evidence status: `SOURCE_EVIDENCE_READY_WITH_LICENSE_BLOCKERS`.

The project has completed the internal planning, architecture, source-gate scaffold, candidate evaluation, and public documentation review needed to identify the correct future implementation path. The next blocker is not design imagination or implementation effort. The blocker is external evidence: licensing, entitlement, official source documentation, retention permissions, archive policy, and reproducibility policy.

No implementation was performed. No ingestion, external access, metadata table construction, research pipeline change, governance mutation, production change, or ML work was performed.

Closeout conclusion:

- The PIT planning phase is complete enough to pause.
- Implementation must not resume until external license and source-evidence requirements are satisfied.
- The first future implementation target should be CRSP-backed Security Master, followed by Ticker Lineage, then Economic Metadata, Peer Groups, and only then Alpha Discovery.

## SECTION 2 - Completed Design Work

Completed architecture and planning work:

- Point-in-time metadata architecture.
- Security master and ticker lineage architecture.
- Source-gate policy and controlled vocabulary design.
- Source-gate scaffold implementation planning.
- Source candidate survey and evaluation framework.
- Candidate source evaluation.
- CRSP assumption verification scaffold and evidence requirements.
- CRSP external evidence verification review.
- PIT security master and ticker lineage source evidence and license review.
- Documentation-only source readiness artifacts.

Completed conceptual design areas:

| area | status | closeout assessment |
| --- | --- | --- |
| Metadata architecture | Complete for planning | Architecture correctly prioritizes date-safe identity, ticker lineage, source lineage, and fail-closed eligibility. |
| Source gate scaffold | Complete for planning | Acceptance criteria, rejection criteria, policy vocabularies, and diagnostics are defined. |
| Candidate evaluation | Complete for current phase | Candidate sources are ranked and classified without source access. |
| Documentation review | Complete for current phase | Public documentation supports source plausibility but not implementation authorization. |
| External evidence requirements | Complete for current phase | Required license, entitlement, field, retention, and reproducibility evidence is explicit. |

Prior readiness note:

Earlier PIT implementation-readiness work classified the scaffold path as implementation-ready for a controlled source-gate layer. The later source-evidence review narrowed the current operational posture: no implementation should resume until external license and entitlement evidence is available, because the remaining blockers are external and source-specific.

## SECTION 3 - Remaining External Blockers

The remaining blockers are external dependencies, not internal design gaps.

| blocker | required evidence | current status | implementation impact |
| --- | --- | --- | --- |
| Licensing | Institutional license agreement, legal/compliance memo, or vendor clarification covering research use, derived metadata, audit artifacts, and redistribution restrictions. | Not provided. | Blocks source access, source loading, ingestion design finalization, metadata construction, and production use. |
| Entitlement | Account-specific confirmation of accessible products, tables/files, date ranges, documentation, delivery formats, and update cadence. | Not provided. | Blocks table inventory, field mapping, and implementation planning beyond assumptions. |
| Field inventory | Official data dictionary or authorized schema evidence for identifiers, dates, ticker windows, exchange/listing fields, delisting fields, security type, source metadata, and event fields. | Not provided. | Blocks schema mapping and PIT construction rules. |
| Table inventory | Official list of accessible CRSP, WRDS CCM, Compustat, or other source tables/files, with intended roles and date coverage. | Not provided. | Blocks source manifest design and extraction planning. |
| Retention policy | Permission to retain raw files, controlled references, source hashes, row counts, source snapshots, normalized staging, derived metadata, and review notes. | Not provided. | Blocks reproducible audit trail and metadata source lineage. |
| Archive requirements | Approved archive, controlled-reference, or no-archive policy compatible with source license. | Not provided. | Blocks source versioning, reproducibility, and rebuild evidence. |
| Reproducibility policy | Source-version, snapshot/extract date, hash/checksum, row-count, normalization-rule, and rerun policy. | Not provided. | Blocks source acceptance and future validation eligibility. |
| Known-date semantics | Documentation for event known dates or conservative source release/snapshot fallback dates. | Not provided. | Blocks PIT safety and look-ahead controls. |

## SECTION 4 - Required Evidence Before Implementation

Implementation may resume only after an external evidence intake package supplies the following:

1. License and allowed-use evidence

- Research-use permission.
- Derived metadata permission.
- Audit artifact permission.
- Source documentation reference permission.
- Redistribution and sharing restrictions.
- Production-use restrictions.
- Any restrictions on committing manifests, hashes, row counts, or derived metadata.

2. Entitlement evidence

- Available products and modules.
- Accessible tables, files, or views.
- Historical coverage dates.
- Delivery mechanism.
- Update cadence.
- Documentation access.
- Whether CRSP Stock Names / Security Master / Delisting, WRDS CRSP-Compustat Link, and Compustat security/company metadata are actually available.

3. Field and table inventory

- Security identifiers, including PERMNO/PERMCO or source equivalents.
- Company identifiers, including GVKEY or source equivalents where applicable.
- Ticker and ticker-window fields.
- Listing and delisting fields.
- Exchange and share-class fields.
- Name-history fields.
- Corporate-action and event fields.
- Source version, source record id, snapshot date, extract date, and source metadata fields.
- Table/file roles and join keys.

4. Retention and archive policy

- Whether raw source files can be retained.
- Whether controlled references can replace raw archives.
- Whether source hashes, bundle hashes, or source reference ids can be retained.
- Whether normalized staging artifacts can be retained.
- Whether row counts and validation summaries can be retained.
- Whether derived PIT metadata can be retained.

5. Reproducibility policy

- Deterministic source snapshot or extract identifiers.
- Source versioning rules.
- File/table manifest rules.
- Hash/checksum or controlled-reference rules.
- Row-count reconciliation rules.
- Normalization-rule documentation.
- Rerun and audit-review process.

## SECTION 5 - Implementation Resume Criteria

Implementation should resume only when all criteria below are met:

| criterion | required state |
| --- | --- |
| License review | Complete and documented. |
| Entitlement review | Complete and tied to actual available products/tables/files. |
| Retention review | Complete, including raw files, references, hashes, row counts, derived metadata, and audit notes. |
| Archive/reproducibility policy | Approved or explicitly replaced by a compliant controlled-reference strategy. |
| Official field/table inventory | Available from official documentation or authorized non-data schema evidence. |
| Known-date semantics | Defined through event known dates or conservative source release/snapshot fallback. |
| Source-gate manifest update | Evidence-backed source status can be assigned without placeholders. |
| Implementation scope | Limited to source-gate and identity/ticker lineage scaffolding before any broader metadata work. |

Minimum resume classification:

`EXTERNAL_EVIDENCE_ACCEPTED_FOR_SOURCE_GATE_DESIGN`.

This resume classification would allow implementation design to restart. It would not by itself authorize ingestion, PIT table construction, discovery, validation, governance mutation, production registration, or ML.

## SECTION 6 - Future Implementation Order

Recommended future order:

1. Security Master
2. Ticker Lineage
3. Economic Metadata
4. Peer Groups
5. Alpha Discovery

Detailed sequencing:

| phase | target | prerequisite | allowed work after approval |
| --- | --- | --- | --- |
| 1 | Security Master | CRSP or equivalent source license, entitlement, field/table, retention, and reproducibility evidence. | Source-gate implementation, schema mapping, dry-run validation, and later controlled construction if separately authorized. |
| 2 | Ticker Lineage | Accepted security identity spine and documented ticker-window/listing/delisting fields. | Ticker-window logic, ambiguity diagnostics, recycled ticker checks, and blocked ticker-date reporting. |
| 3 | Economic Metadata | Stable security/ticker identity plus licensed sector/industry/company metadata source evidence. | Sector, industry, company metadata, and source lineage construction. |
| 4 | Peer Groups | PIT economic metadata and classification history with adequate coverage diagnostics. | Date-safe peer-group reconstruction and fallback diagnostics. |
| 5 | Alpha Discovery | Certified PIT metadata manifests with discovery eligibility flags. | Peer-relative and economic-context alpha research only after fail-closed metadata eligibility is established. |

The first future starting point should remain:

`crsp_stocknames_delisting_security_master`.

WRDS CRSP-Compustat Link and Compustat metadata should follow as secondary bridge and company metadata layers after the primary security identity and ticker lineage path is evidence-backed.

## SECTION 7 - Risks If Implementation Begins Prematurely

Premature implementation would create material research and governance risk.

| risk | severity | consequence |
| --- | --- | --- |
| License violation | Critical | Source data, derived artifacts, hashes, or metadata could be retained or used outside permitted rights. |
| Entitlement mismatch | Critical | Implementation could target unavailable tables, wrong products, or unsupported date ranges. |
| Look-ahead leakage | Critical | Current or backfilled identity/classification records could enter historical signal dates. |
| Survivorship bias | Critical | Delisted, inactive, merged, or renamed securities could be omitted or misrepresented. |
| Ticker reuse contamination | Critical | Recycled tickers could connect unrelated securities across time. |
| Unreproducible metadata | High | Future audits or validations could not recreate the source state that produced metadata. |
| False readiness | High | Downstream discovery could treat assumption-bound metadata as PIT-safe. |
| Governance drift | High | Source-gate placeholder assumptions could become de facto accepted policy. |
| Pipeline contamination | High | Research runners could begin relying on incomplete identity or peer metadata. |

Most important failure mode:

Starting implementation without license and field evidence would convert known external blockers into hidden assumptions. That would weaken every downstream alpha result, even if the code itself appeared to run cleanly.

## SECTION 8 - Closeout State

Current closed phase:

`PIT_PLANNING_PHASE_CLOSED_PENDING_EXTERNAL_EVIDENCE`.

Current classification:

`PIT_READY_PENDING_EXTERNAL_LICENSE`.

Allowed next work:

- External evidence intake review.
- License and entitlement review.
- Official field/table documentation review.
- Retention and archive policy review.
- Reproducibility policy review.
- Evidence-backed source-gate manifest update.

Blocked work:

- Source data access.
- Downloads.
- API calls.
- External database connections.
- Source loading.
- Ingestion.
- Metadata table construction.
- Security master construction.
- Ticker lineage construction.
- Economic metadata construction.
- Peer-group reconstruction.
- Alpha discovery, refinement, validation, or IC computation.
- Governance threshold changes.
- Production registration.
- ML.

## SECTION 9 - Verification

Verified for this closeout:

- Documentation-only artifact created.
- No implementation files changed.
- No ingestion performed.
- No metadata tables created.
- No research pipeline changes made.
- No governance changes made.
- No external access performed.
- No source data accessed.

## SECTION 10 - Final Recommendation

Pause PIT implementation work until external evidence is available.

The next appropriate task is **Project Underdog - PIT External Evidence Intake Review v1**. It should review license, entitlement, field inventory, table inventory, retention policy, archive requirements, reproducibility policy, and known-date semantics. It should remain review-only unless a later explicit task authorizes implementation-design updates.
