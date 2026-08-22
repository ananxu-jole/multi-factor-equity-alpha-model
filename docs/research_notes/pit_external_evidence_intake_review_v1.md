# Project Underdog
# PIT External Evidence Intake Review v1
# Peer-Relative / Economic-Context Research Frontier
# Platform v2

Date: 2026-07-11

Final classification: EXTERNAL_EVIDENCE_PATH_BLOCKED_BY_SOURCE_OR_GOVERNANCE_GAPS

This note performs a bounded evidence-readiness, source-governance, and dependency review for future point-in-time peer-relative and economic-context research. It does not approve the peer-relative alpha family, begin implementation, access external data, ingest sources, construct PIT metadata, build a security master, construct ticker lineage, construct peer groups, define formulas, assign candidate identifiers, register candidates, generate panels, compute IC, validate, mutate governance, alter production, change thresholds, or introduce ML.

## 1. Executive Classification

Final classification: EXTERNAL_EVIDENCE_PATH_BLOCKED_BY_SOURCE_OR_GOVERNANCE_GAPS

Interpretation:

- A credible conceptual evidence pathway exists.
- The strongest documented source family remains CRSP security master / stock names / delisting data, complemented by WRDS CRSP-Compustat linkage and Compustat company/security metadata after license and entitlement evidence are supplied.
- Current repository evidence does not establish license rights, actual entitlements, official table inventory, field-level documentation, retention rights, archive policy, source-hash permission, publication-date semantics, or known-date semantics.
- Therefore the project may continue evidence-readiness review, vendor/license documentation collection, and source-independent acceptance-test design, but may not proceed to ingestion, PIT construction, peer-group construction, formulas, panels, IC, validation, governance promotion, or production.

This classification does not classify the peer-relative alpha family as approved, validated, implementable, or discovery-ready.

## 2. Current-State Reconstruction

Authoritative current state:

- The peer-relative / economic-context frontier is the selected next scientific frontier after the completed cross-module meta-analysis in `docs/research_notes/project_underdog_cross_module_scientific_meta_analysis_v1.md`.
- The readiness reassessment in `docs/research_notes/peer_relative_economic_context_readiness_reassessment_and_scientific_program_framing_v1.md` classifies the frontier as `FRONTIER_READY_FOR_LIMITED_DESIGN_ONLY`.
- The recommended first future module is the Peer-Relative Post-Stress Repair and Stabilization Asymmetry Module.
- Platform v2 requires one primary mechanism per module, hypothesis-first discipline, frozen horizons, no broad search, no target hacking, no horizon shopping, and one bounded refinement cycle maximum.
- PIT readiness remains `PIT_READY_PENDING_EXTERNAL_LICENSE`, as recorded in `docs/research_notes/pit_external_dependency_closeout_v1.md`.
- Source-evidence status remains `SOURCE_EVIDENCE_READY_WITH_LICENSE_BLOCKERS`.
- Source-gate scaffold status remains `SOURCE_GATE_SCAFFOLD_READY_WITH_EXTERNAL_DEPENDENCIES`, from `docs/research_notes/security_master_and_ticker_lineage_pit_source_gate_scaffold_v1.md`.
- Security-master and ticker-lineage source candidates are not approved for ingestion design. The strongest conceptual path is CRSP stock names / security master / delisting data, but it is conditional on license, entitlement, official fields, retention, archive, reproducibility, and known-date review.
- Existing static economic metadata is diagnostic-only. It cannot be silently elevated into authoritative PIT metadata.

Current implementation versus design-only state:

| Area | Current repository state | Authority level |
|---|---|---|
| Source-gate scaffold | Implemented scaffold and synthetic dry-run modes exist. | Governance scaffold only; does not approve real sources. |
| CRSP/security-master planning | Design and evaluation notes exist. | Planning only; no licensed source accepted. |
| Economic-context enrichment | Static diagnostic substrate exists in older notes. | Diagnostic-only; superseded for alpha use by PIT dependency closeout. |
| Peer-relative program design | Scientific design exists. | Design-only; blocked by PIT metadata. |
| PIT metadata construction | Not constructed. | Blocked. |
| Security master | Not constructed from authoritative external source. | Blocked. |
| Ticker lineage | Not constructed from authoritative external source. | Blocked. |
| Peer groups | Not constructed point-in-time. | Blocked. |
| Candidate formulas | Not authorized. | Blocked. |
| Panels and IC | Not authorized. | Blocked. |

Currently permitted work:

- External evidence intake review.
- License and entitlement documentation collection.
- Official field/table documentation review.
- Retention, archive, and reproducibility policy review.
- Source-independent conceptual schema review.
- Synthetic-fixture acceptance-test design.
- Evidence-backed source-gate manifest preparation after documentation exists.

Currently blocked work:

- Source access, downloads, API calls, external database connections, ingestion, source loading, metadata table construction, security-master construction, ticker-lineage construction, economic metadata construction, peer-group reconstruction, candidate formula specification, candidate registration, panel generation, IC discovery, validation, governance promotion, production integration, threshold changes, and ML.

Unresolved assumptions:

- Whether the project has or can obtain the needed CRSP, WRDS, Compustat, exchange/vendor, and documentation entitlements.
- Whether license terms permit raw retention, controlled references, hashes, row counts, derived metadata, and audit artifacts.
- Whether official documentation contains field-level effective-date, publication-date, revision, corporate-action, and delisting semantics sufficient for fail-closed PIT use.

## 3. External Evidence Requirement Matrix

| Requirement | Scientific necessity | Contamination risk if absent | Preferred source type | Minimum acceptable evidence | First module or later | Current architecture/governance expectation |
|---|---|---|---|---|---|---|
| Stable security identifiers | Anchor returns, metadata, events, and ticker history to the same security through time. | Ticker reuse, issuer confusion, false continuity. | CRSP-like security master with permanent security ids. | Licensed field dictionary, id definitions, coverage, examples, source lineage. | First module. | Yes, required by PIT architecture. |
| Ticker history and ticker reuse handling | Resolve historical ticker-date identity before peer assignment. | Current ticker applied historically; unrelated securities joined. | Security master / stock names with dated ticker windows. | Start/end windows, exchange namespace, reuse rules, known-date evidence. | First module. | Yes, fail-closed if unresolved. |
| Company/security mapping | Separate issuer continuity from security/share-class identity. | Merged share classes, wrong issuer peers, false persistence. | Security master plus issuer/company bridge such as CCM. | Company id, security id, link dates, link quality, link-type documentation. | First module for identity; richer issuer logic later. | Yes. |
| Listing and delisting history | Define eligible active universe and prevent survivorship bias. | Survivor-only panels; missing terminal events. | CRSP delisting/listing or equivalent authoritative source. | Listing date, delisting date, inactive coverage, delisting reason if available. | First module. | Yes. |
| Exchange history | Preserve ticker namespace and venue-specific security identity. | Same symbol across venues merged; exchange migration mishandled. | Security master or exchange/vendor listing history. | Exchange codes, effective windows, date semantics. | First module. | Yes. |
| Sector history | Construct economically valid peer context. | Current sector backfilled into past. | PIT classification source or dated taxonomy snapshots. | Sector code/name, taxonomy version, effective/as-of dates, source lineage. | First module if sector fallback allowed. | Yes. |
| Industry history | Primary economic peer construction layer. | Invalid peer groups and false idiosyncratic repair claims. | PIT industry classification source. | Industry code/name, taxonomy version, effective/as-of dates, revision policy. | First module. | Yes. |
| Industry-reclassification history | Preserve historical classification changes without look-ahead. | Future industry membership assigned to prior dates. | Classification history with effective and publication dates. | Reclassification events, effective dates, source publication timing. | First module. | Yes. |
| Company-name history | Support diagnostic lineage and event review. | False issuer continuity via current names or name similarity. | Security master / company metadata. | Name windows, source ids, effective/as-of dates. | Later, except event diagnostics. | Yes, diagnostic support. |
| Market-cap or size information | Support size-aware peer fallback and avoid comparing structurally unlike firms. | Size exposure mistaken for peer-relative repair. | Historical shares and price source or licensed market-cap source. | Historical market cap or reconstructable inputs with date-safe semantics. | First module if size fallback used; otherwise later. | Yes, required for size-aware grouping. |
| Shares outstanding | Needed for historical market cap and corporate-action consistency. | Incorrect size buckets and event discontinuities. | CRSP/Compustat or equivalent dated shares source. | Shares definition, adjustment basis, effective/as-of dates, revision behavior. | Conditional for first module; mandatory before size-aware use. | Yes. |
| Price and corporate-action consistency | Ensure size and event interpretation align with return history. | Split, merger, or distribution distortions treated as repair. | CRSP-like market data and corporate-action source. | Adjustment policy, event fields, date semantics, source version. | First module for event exclusions; later for richer size. | Yes. |
| Mergers and acquisitions | Exclude or lineage-map discontinuous securities. | Post-event leakage, false repair after acquisition news. | Corporate-action/event lineage source. | Event type, effective date, known/publication date where available, predecessor/successor ids. | First module exclusion logic. | Yes. |
| Spinoffs | Avoid confusing new securities or parent/child continuity. | Peer assignment and rank history contaminated. | Corporate-action lineage source. | Event links, security ids, dates, listing start, issuer relation. | First module exclusion logic. | Yes. |
| Bankruptcies | Identify terminal stress and delisting paths. | Distressed terminal names treated as recoverable peers. | Delisting/event source. | Bankruptcy/delisting event classification where available, date fields. | First module. | Expected, source dependent. |
| Reorganizations | Preserve identity continuity through structural events. | False break or false continuity in repair history. | Security master event lineage. | Event codes, predecessor/successor ids, effective/as-of dates. | First module exclusion or block policy. | Yes. |
| Share-class relationships | Select primary security and avoid duplicate issuer exposure. | Multiple share classes counted as independent peers. | Security master plus issuer mapping. | Share class, primary listing flag, issuer relation, active windows. | First module. | Yes. |
| ADR or foreign-listing treatment | Bound universe and peer comparability. | Non-comparable securities enter peer groups. | Security master with security type/country/listing fields. | ADR/foreign/listing flags, country, exchange, security type. | First module eligibility. | Expected. |
| Primary-security selection | Prevent duplicate issuer representation. | Peer counts and ranks distorted by duplicate securities. | Security master / exchange primary listing source. | Primary listing flag or deterministic documented rule. | First module. | Yes. |
| Security-start and security-end dates | Define active eligibility and warmup scope. | Pre-listing or post-delisting metadata leakage. | Security master / listing source. | Start/end dates with source lineage and date semantics. | First module. | Yes. |
| Metadata effective dates | Ensure historical metadata validity. | Future classification used on past signal dates. | PIT source with effective windows or snapshots. | Effective start/end or documented snapshot inference policy. | First module. | Yes. |
| Source publication dates | Prevent using records before they were knowable. | Look-ahead via delayed publication or retroactive updates. | Source with publication/release/as-of dates. | Publication date or conservative snapshot date fallback. | First module if available; otherwise conservative blocking. | Yes, known-date blocker. |
| Restatement or revision behavior | Control historical corrections and metadata rewrites. | Research artifacts silently reinterpreted. | Source with version/revision documentation. | Revision policy, source version, correction records, archive strategy. | First module. | Yes. |
| Source lineage | Make all metadata auditable. | Untraceable metadata provenance. | Licensed source manifests and row-level lineage. | Provider, source, version, record id, hash/control reference, row counts. | First module. | Yes. |
| Coverage | Confirm peer groups and active universe are sufficient. | Sparse or biased peer groups. | Source coverage reports. | Date range, universe coverage, null rates, inactive coverage. | First module. | Yes. |
| Update cadence | Define reproducible snapshots and refresh policy. | Mixed versions and unstated source timing. | Vendor release notes or snapshot schedule. | Update frequency, release id, extraction timestamp. | First module. | Yes. |
| Historical depth | Cover research lookback and delisted names. | Truncated history and survivorship bias. | Longitudinal professional database. | Start/end coverage and inactive coverage evidence. | First module. | Yes. |
| License constraints | Determine allowed research, retention, sharing, and derived artifacts. | License violation or unusable audit trail. | Executed license or entitlement memo. | Written confirmation of allowed use, retention, hashes, row counts, derived metadata. | First module. | Yes, current blocker. |
| Reproducibility constraints | Permit rebuilding or auditing metadata. | Non-reproducible panels and IC. | Archive/controlled-reference policy. | Source snapshot id, checksum permission or controlled references, row counts. | First module. | Yes, current blocker. |
| Auditability | Support future research review, validation, and governance. | Evidence cannot be traced or challenged. | Source manifest and governance review package. | Manifest, source gate outcome, lineage registration, review sign-off. | First module. | Yes. |

No coverage, contractual right, entitlement, or field availability is inferred beyond repository evidence.

## 4. Candidate Source-Family Assessment

### CRSP stock names / security master / delisting family

Known project conclusions:

- It is the strongest conceptual first source family for security identity, ticker lineage, listing/delisting, active/inactive coverage, and recycled ticker control.
- It is not approved for ingestion design or PIT construction.

Likely capabilities requiring confirmation:

- Stable security and issuer identifiers.
- Dated ticker/name windows.
- Listing, delisting, exchange, and security-type fields.
- Corporate-action continuity sufficient for research exclusions and lineage.

Required labels:

- License, entitlement, retention, archive, and hash rights: `REQUIRES_VENDOR_OR_LICENSE_CONFIRMATION`.
- Official table and field inventory: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.
- Known-date or publication-date semantics: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.

Suitability:

- Security master: high conceptual suitability, blocked.
- Ticker lineage: high conceptual suitability, blocked.
- Company-security linkage: partial, likely complemented by linkage products.
- Sector/industry history: not sufficient by itself.
- Size construction: possible only if required fields and semantics are licensed and documented.
- Corporate-event interpretation: likely useful but field semantics must be confirmed.
- Peer-group membership: indirect; supports identity and active universe, not economic classification alone.
- PIT effective dating: likely directionally aligned, but not established for project use.

### WRDS CRSP-Compustat link family

Known project conclusions:

- It is a strong complement for linking CRSP security identity to Compustat company identifiers.
- It is not a standalone security master or ticker-lineage source.

Required labels:

- Entitlement to WRDS/CRSP/Compustat products: `REQUIRES_VENDOR_OR_LICENSE_CONFIRMATION`.
- Link date windows, link quality, link type, and field semantics: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.

Suitability:

- Security master: no, complementary only.
- Ticker lineage: no, complementary only.
- Company-security linkage: high conceptual suitability, blocked.
- Sector/industry history: only through linked secondary metadata, not by itself.
- Peer-group membership: indirect.
- PIT effective dating: depends on link-window documentation.

### Compustat security/company metadata family

Known project conclusions:

- It may support company attributes, issuer identifiers, and economic classification work.
- It is not sufficient as primary security master or ticker-lineage source.

Required labels:

- Table entitlement and license terms: `REQUIRES_VENDOR_OR_LICENSE_CONFIRMATION`.
- Field dictionaries for company/security attributes, industry classifications, dates, and revisions: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.

Suitability:

- Security master: secondary only.
- Ticker lineage: weak as standalone.
- Company-security linkage: useful if linked and date-safe.
- Sector/industry history: possible but unproven without official dated field semantics.
- Size construction: possible if dated shares or market-cap fields are available and permitted.
- Corporate-event interpretation: partial, not primary without event evidence.
- Peer-group membership: possible after date-safe classification evidence.
- PIT effective dating: unresolved.

### Exchange or vendor listing/delisting families

Known project conclusions:

- Potentially useful as supplemental listing/delisting evidence.
- Public documentation is too fragmented for primary-source ingestion design.

Required labels:

- Dataset access and license rights: `REQUIRES_VENDOR_OR_LICENSE_CONFIRMATION`.
- Historical file layout, identifiers, date fields, and archive policy: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.

Suitability:

- Security master: usually insufficient alone.
- Ticker lineage: possible supplement.
- Listing/delisting: possible supplement.
- Corporate-event interpretation: source dependent.
- PIT effective dating: unresolved.

### OpenFIGI or comparable identifier crosswalks

Known project conclusions:

- Diagnostic-only support for identifier crosswalk review.
- Not authoritative PIT ticker lineage.

Required labels:

- Historical lineage and license suitability for any expanded role: `REQUIRES_VENDOR_OR_LICENSE_CONFIRMATION`.
- Mapping-date behavior and coverage: `REQUIRES_EXTERNAL_DOCUMENTATION_REVIEW`.

Suitability:

- Security master: diagnostic only.
- Ticker lineage: diagnostic only.
- Company-security linkage: diagnostic only.
- Peer-group membership: no.

### yfinance or current static metadata

Known project conclusions:

- Diagnostic-only current profile metadata.
- Not authoritative for PIT identity, ticker lineage, economic classification, or alpha discovery.

Suitability:

- Security master: no.
- Ticker lineage: no.
- Sector/industry history: no.
- Size construction: no for authoritative PIT use.
- Peer-group membership: no.

No prohibited speculation is used here. Potential capabilities remain conditional until license, entitlement, official documentation, and source-gate evidence are available.

## 5. Source Hierarchy And Authority Model

Proposed conceptual authority hierarchy for future evidence intake:

| Domain | Primary authority class | Secondary authority class | Diagnostic-only fallback | Fail-closed condition |
|---|---|---|---|---|
| Security identity | Licensed PIT security master with stable security ids. | Exchange/vendor listing history with stable ids and dated records. | Current ticker universe or crosswalk diagnostics. | Missing or ambiguous stable security id. |
| Ticker lineage | Licensed dated ticker/name history tied to security ids. | Security-master event files or exchange dated symbols. | Current ticker text or static crosswalk. | Reused ticker, overlapping windows, missing exchange namespace. |
| Company-security linkage | Licensed issuer/security bridge with date windows. | Company metadata with dated identifiers. | Company-name matching. | Ambiguous issuer/security relation. |
| Historical industry classification | Licensed PIT taxonomy or dated classification snapshots. | Vendor taxonomy snapshots with approved inferred windows. | Static sector/industry labels. | Static-only, future-dated, or missing industry. |
| Size | Licensed historical market cap or reconstructable price/shares with PIT semantics. | Dated size classifications. | Current market-cap bucket. | Missing date-safe size where size conditioning is required. |

Conflict resolution:

- Security identity resolves before all other metadata.
- Ticker text never overrides stable security identity.
- If primary and secondary sources disagree, the stronger PIT evidence wins only after disagreement is logged.
- If disagreement cannot be resolved, the ticker-date is blocked from discovery eligibility.
- Fallback sources are allowed only when their diagnostic or conditional status is explicitly carried into lineage.
- Diagnostic-only fallback cannot produce discovery-eligible peer-relative features.

Forced fail-closed conditions:

- License or entitlement unknown.
- Source is static snapshot only.
- Ticker-only identity.
- Missing effective dates or approved snapshot inference policy.
- Missing source lineage.
- Missing active-universe or delisting evidence where required.
- Peer group below future frozen minimum count.
- Publication or known-date semantics imply post-signal availability.

This hierarchy is conceptual only. No production source-priority code is created.

## 6. Point-In-Time Contamination Review

| Pathway | Failure mechanism | Expected scientific distortion | Minimum control | Represented in current architecture |
|---|---|---|---|---|
| Current classification applied retrospectively | Current sector/industry labels assigned to past dates. | False peer-relative signal and look-ahead. | Effective/as-of dates or blocked static labels. | Yes. |
| Current ticker applied historically | Historical records joined by current symbol. | False continuity and incorrect returns/metadata. | Date-stamped ticker lineage by security id. | Yes. |
| Ticker reuse | Same ticker maps to different companies over time. | Unrelated securities joined. | Exchange-aware ticker windows and stable ids. | Yes. |
| Stale company-security mappings | Old or overwritten links used without dates. | Wrong issuer lineage and duplicate exposure. | Dated issuer/security bridge with link quality. | Yes. |
| Survivor-only universe | Delisted/inactive names omitted. | Overstated repair quality and biased peer groups. | Active and inactive coverage, delisting history. | Yes. |
| Missing delisted securities | Terminal failures disappear before measurement. | False positive stability and repair. | Delisting dates and inactive security inclusion. | Yes. |
| Post-event metadata leakage | Merger, bankruptcy, or reclassification info used before known. | Event outcome leaks into signal date. | Known-date/publication-date controls or conservative blocking. | Yes, but evidence unavailable. |
| Retrospective peer assignment | Future peer membership used for historical date. | False economic comparability. | Peer groups built from date-valid classifications and active universe. | Yes. |
| Corporate-action misalignment | Splits, mergers, spinoffs, or share-class changes not handled. | Artificial repair, deterioration, rank shifts, or size jumps. | Corporate-action lineage and exclusion/block rules. | Yes. |
| Industry-code restatements | Revised taxonomy overwrites historical classification. | Backfilled industry knowledge. | Versioned records and revision lineage. | Yes. |
| Revised shares outstanding | Later restated shares used for historical size. | Look-ahead size bucket and peer fallback. | As-of dated shares or conservative source snapshot policy. | Yes, but evidence unavailable. |
| Source publication timing | Source update known after signal date. | Look-ahead through delayed publication. | Publication date, release date, or conservative as-of fallback. | Yes, current blocker. |
| Future membership in peer groups | Peer groups include securities not active or classified then. | Survivor and membership contamination. | Active-universe and classification filters as of signal date. | Yes. |
| Silent fallback to diagnostic metadata | Static or manual labels fill missing PIT rows. | Diagnostic metadata becomes false authority. | Explicit source status and blocked discovery eligibility. | Yes. |

## 7. First-Module Dependency Review

Recommended first future module:

Peer-Relative Post-Stress Repair and Stabilization Asymmetry Module

This section remains conceptual. It defines no formulas, candidate identifiers, thresholds, or panels.

### MANDATORY_BEFORE_IMPLEMENTATION

- Executed license or documented entitlement for the primary security identity source.
- Official table and field inventory for stable security identifiers, ticker windows, listing dates, delisting dates, exchange history, security type, share class, and source lineage.
- PIT date semantics for effective dates, as-of dates, source release dates, or conservative publication-date fallback.
- Security eligibility rules covering active windows, delisted names, ADR or foreign-listing treatment, primary-security selection, share classes, and corporate-event exclusions.
- Historical sector and industry classification evidence sufficient to construct peer groups without current backfill.
- Source lineage policy covering provider, source version, extract/snapshot reference, row counts, hashes or controlled references, and retention rights.
- Fail-closed missing-metadata behavior.

### MANDATORY_BEFORE_IC_DISCOVERY

- Approved PIT security master and ticker lineage construction from accepted sources.
- Approved date-safe economic classification history.
- Approved peer-definition hierarchy, including sector-versus-industry fallback behavior.
- Frozen minimum peer-count policy, measured as of signal date.
- Peer-membership lineage for every eligible ticker-date.
- Missing metadata, corporate-event, and low-peer-count exclusion reports.
- Benchmark or market-state alignment policy using only information available by the signal date.
- Audited panel-generation process for the future module.

### MANDATORY_BEFORE_VALIDATION

- Reproducible source manifests and checksums or controlled references.
- Coverage, null-rate, duplicate-key, and lineage reports.
- Evidence that peer-relative features were built only from eligible historical peer membership.
- Contamination review against own OHLCV, market/sector state, validated VoV, participation/breadth behavior, stress repair, rank, and persistence families.
- Research review and governance review of IC evidence.

### OPTIONAL_FOR_LATER_REFINEMENT

- Size conditioning if not required by the first frozen module design.
- Subindustry peer groups if coverage supports them.
- Richer corporate-event subtyping.
- More granular share-class handling.
- Vendor peer-group history, if licensed and reproducible.
- Economic-cycle overlays, only after core PIT identity and peer construction are approved.

## 8. Evidence Intake Checklist

Future intake package checklist:

- Executed license or confirmed entitlement.
- Exact dataset names and product modules.
- Provider and delivery channel.
- Version, release, extract, or snapshot identification.
- Field-level data dictionaries.
- Historical coverage start and end dates.
- Coverage by exchange, security type, active/inactive status, and country.
- Effective-date semantics.
- Publication-date, release-date, or as-of-date semantics.
- Restatement and revision behavior.
- Stable security identifier definitions.
- Company/issuer identifier definitions.
- Ticker namespace and reuse definitions.
- Corporate-action treatment.
- Delisting coverage.
- Listing and exchange-history coverage.
- Share-class and primary-security fields.
- Sector, industry, and taxonomy documentation.
- Historical market-cap, shares, and price field definitions if used.
- Sample extracts or authorized schema examples.
- Expected row counts by table and date range.
- Expected date ranges by table.
- Null-rate review plan.
- Duplicate-key review plan.
- Source checksum capture or controlled-reference policy.
- Raw-data immutability or approved no-raw-retention alternative.
- Lineage registration plan.
- Source-gate evaluation plan.
- Synthetic-fixture comparison plan.
- Governance sign-off.

No checklist action is performed now.

## 9. Synthetic-Fixture Acceptance-Test Design

These are conceptual scenarios only. No fixtures, source files, test scripts, or implementation artifacts are created.

| Scenario | Fixture setup | Expected PIT behavior | Expected peer-membership behavior | Expected lineage result | Required failure status |
|---|---|---|---|---|---|
| Ticker change without company change | One security id changes ticker on a dated window. | Security identity remains continuous; ticker lookup changes by date. | Peer membership follows valid classification, not ticker text. | Prior and next ticker windows recorded. | Fail if current ticker backfills. |
| Ticker reuse by different company | Same symbol assigned to different security ids in non-overlapping periods. | Separate security identities. | Peer groups reflect each security's own dated metadata. | Reuse event recorded. | Fail if histories merge. |
| Multiple share classes | One issuer has two active security ids. | Securities remain distinct unless primary selection rule chooses one. | Peer counts avoid duplicate issuer exposure if rule requires. | Share-class relation recorded. | Fail if duplicates silently enter. |
| Industry reclassification | Security changes industry on a known effective date. | Old industry before date, new industry after date, subject to as-of control. | Peer group changes only when date-valid. | Taxonomy version and record lineage retained. | Fail if future industry backfills. |
| Merger | Security has event and successor relation. | Security blocked or mapped only under approved lineage rule. | Peer membership ends or transitions by rule. | Event lineage recorded. | Fail if post-merger data treated as normal repair. |
| Spinoff | Parent and new child security appear with event link. | New security starts at listing date; parent continuity marked. | Peer membership begins only after child is active and classified. | Parent/child lineage recorded. | Fail if child appears before listing. |
| Delisting | Security delists after a stress period. | Active eligibility ends at delisting date. | Removed from future peer groups; included historically while active. | Delisting lineage retained. | Fail if omitted from past universe. |
| Temporary metadata gap | Industry missing for a date range. | Identity may remain valid; peer-relative eligibility blocked. | No silent fallback to static industry. | Missingness logged. | Blocked missing mandatory peer context. |
| Sector known, industry missing | Sector exists but industry absent. | Sector fallback only if future design explicitly allows it. | Peer quality downgraded or blocked. | Fallback distance recorded. | Blocked unless fallback approved. |
| Size-band transition | Market cap crosses date-safe size bucket. | Size bucket changes only after date-valid input. | Size-aware peer group changes by valid date. | Size source lineage retained. | Fail if revised future size used. |
| Peer-count collapse | Industry peer group falls below minimum active count. | Security identity remains valid. | Peer group blocked or falls back by approved hierarchy. | Peer-count reason recorded. | Blocked insufficient peer context. |
| Source conflict | Primary and secondary source disagree on classification. | Primary wins only if accepted; unresolved conflict blocks. | Peer membership follows resolved source or blocks. | Conflict logged. | Blocked unresolved source conflict. |
| Revised metadata record | Vendor revises past classification in later release. | Original and revised records versioned. | Artifacts use declared metadata version. | Revision lineage retained. | Fail if destructive overwrite occurs. |
| Publication-date delay | Classification effective date precedes publication date. | Row usable only after known/publication date or conservative fallback. | Peer membership delayed or blocked before known date. | Publication semantics recorded. | Fail if effective date alone permits use. |
| Authority unavailable | No accepted source for required field. | Metadata unavailable. | No peer group constructed. | Source status remains unresolved. | Fail-closed authority unavailable. |

## 10. Open-Assumption Register

| Assumption ID | Statement | Why it matters | Current evidence | Required confirmation | Blocking severity | Affected stage |
|---|---|---|---|---|---|---|
| ASSUMP-01 | CRSP-family security master products are accessible to the project. | Primary identity path depends on actual entitlement. | Conceptual candidate notes only. | License and entitlement evidence. | Critical. | License selection, ingestion. |
| ASSUMP-02 | License terms allow research use of derived PIT metadata. | Derived lineage and panels require allowed use. | Not provided. | License/legal confirmation. | Critical. | Ingestion, PIT construction, IC. |
| ASSUMP-03 | Retention terms allow raw archives, hashes, row counts, or controlled references. | Reproducibility requires audit trail. | Not provided. | Retention/archive policy. | Critical. | PIT construction, validation. |
| ASSUMP-04 | Official field dictionaries include ticker windows, listing, delisting, exchange, and security-type fields. | Security and ticker lineage depend on field semantics. | Public docs are supportive but insufficient. | Official documentation review. | Critical. | Ingestion, PIT construction. |
| ASSUMP-05 | Known-date or publication-date semantics can be established. | Prevents look-ahead through delayed updates. | Current blocker. | Documentation or conservative snapshot policy. | Critical. | PIT construction, IC. |
| ASSUMP-06 | Historical industry classifications are date-safe and licensed. | Peer groups require historical economic context. | Not accepted. | Official taxonomy/date documentation and entitlement. | Critical. | Peer-group construction, module implementation. |
| ASSUMP-07 | Corporate-event coverage is sufficient for exclusions and continuity. | Events can mimic repair/deterioration. | Conceptually expected, not field-proven. | Event field documentation and coverage review. | High. | Module implementation, IC. |
| ASSUMP-08 | Historical size can be constructed or licensed date-safely. | Size-aware fallback may be needed. | Not accepted. | Shares/market-cap field evidence and date semantics. | Medium to high. | Peer-group construction, later refinement. |
| ASSUMP-09 | Peer-count coverage is adequate for future modules. | Sparse peers weaken interpretation. | No real PIT peer groups exist. | Coverage diagnostics after accepted metadata. | High. | Peer-group construction, IC. |
| ASSUMP-10 | Diagnostic static metadata will remain blocked from discovery. | Prevents governance drift. | Current governance says diagnostic only. | Continued source-gate enforcement. | High. | All stages. |
| ASSUMP-11 | WRDS CRSP-Compustat link fields can be used for issuer linkage. | Company/security mapping may need bridge. | Conditional notes only. | Entitlement and link-field documentation. | High. | PIT construction. |
| ASSUMP-12 | Compustat classification/company metadata includes usable dated semantics. | Industry and company context may require it. | Public docs insufficient. | Official documentation review. | High. | Peer-group construction. |

## 11. Decision Gates

| Gate | Required evidence | Pass condition | Fail condition | Permitted next action |
|---|---|---|---|---|
| 1. License and entitlement gate | Executed license or entitlement memo for exact products. | Rights and accessible datasets documented. | Missing, ambiguous, or restrictive terms. | Documentation sufficiency review. |
| 2. Documentation sufficiency gate | Official data dictionaries, table inventories, date semantics. | Fields and tables mapped without placeholders. | Unknown fields or unsupported assumptions. | Raw-source integrity planning. |
| 3. Raw-source integrity gate | Source version, extract id, row counts, checksum/control reference policy. | Reproducible source package can be governed. | No archive/hash/reference path. | Identifier-lineage review. |
| 4. Identifier-lineage gate | Stable ids, ticker windows, listing/delisting, exchange namespace. | Date-safe identity and ticker rules can be specified. | Ticker-only or ambiguous identity. | PIT effective-date review. |
| 5. PIT effective-date gate | Effective/as-of/publication-date semantics. | Look-ahead controls can be enforced. | Effective dates absent with no conservative fallback. | Historical classification review. |
| 6. Historical classification gate | Sector/industry taxonomy history and revision behavior. | Date-safe classification is constructable. | Static-only or future-revised labels only. | Corporate-event coverage review. |
| 7. Corporate-event coverage gate | Mergers, spinoffs, delistings, reorganizations, share classes. | Event exclusions/lineage can be specified. | Event gaps create unbounded contamination. | Peer-group constructability review. |
| 8. Peer-group constructability gate | Active universe, classification coverage, peer-count diagnostics. | Peer groups can be formed fail-closed. | Coverage too sparse or fallback unresolved. | Synthetic acceptance-test gate. |
| 9. Synthetic acceptance-test gate | Fixture specifications and expected behavior. | PIT behaviors pass conceptually and later in code when authorized. | Critical scenario cannot be represented. | Source-gate governance approval. |
| 10. Source-gate governance approval | Evidence-backed manifest and review sign-off. | Source accepted for bounded design/implementation phase. | Manual review, diagnostic-only, or rejected status. | Module implementation authorization review. |
| 11. Module implementation authorization | Approved scientific module design and accepted metadata prerequisites. | Implementation scope approved for one module. | Broad, under-specified, or metadata-blocked module. | Formula implementation lifecycle may begin. |
| 12. IC discovery authorization | Audited panels from approved implementation. | IC can use only audited panel snapshot. | Panel audit fails or lineage incomplete. | IC discovery for that module only. |

No gate is marked passed by this review. The current state remains before Gate 1 completion because license and entitlement evidence have not been supplied.

## 12. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

License And Entitlement Evidence Collection v1

Purpose:

- Collect written evidence for available products, subscribed tables/files, allowed research use, retention rights, audit artifacts, documentation access, source hashes or controlled references, delivery formats, coverage, and update cadence.

This is the necessary next step because the current blockers are external and contractual before they are technical. Implementation is not recommended.

## Conclusion

Final classification: EXTERNAL_EVIDENCE_PATH_BLOCKED_BY_SOURCE_OR_GOVERNANCE_GAPS

The project can define a credible external-evidence intake pathway for future PIT peer-relative research, but the pathway is currently blocked by missing license, entitlement, documentation, retention, archive, reproducibility, known-date, and source-gate evidence. The first future peer-relative module remains scientifically attractive only after authoritative PIT identity, ticker lineage, economic classification, corporate-event, and peer-membership evidence is accepted.

Verification:

- No external licensed data was accessed.
- No source ingestion was performed.
- No PIT metadata was constructed.
- No security master was constructed.
- No ticker lineage was constructed.
- No peer groups were constructed.
- No formulas were defined.
- No candidate identifiers were assigned.
- No candidate registry was generated.
- No panels were written.
- No IC was calculated.
- No validation was run.
- No governance decision was changed.
- No production file was changed.
- No threshold was changed.
- No ML was introduced.
