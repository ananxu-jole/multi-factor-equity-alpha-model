# Project Underdog - Phase 5 Economic Context Validity Science v1

Date: 2026-07-14

Scientific workstream: `Economic Context Validity Science`

Phase 5 roadmap position: Workstream 3

Final classification: `ECONOMIC_CONTEXT_VALIDITY_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

This note defines the scientific framework required before Project Underdog may treat securities or economic companies as economically comparable at a historical time. It is a scientific-framework artifact only. It is not a peer-group implementation, sector or industry mapping exercise, classification-system selection, source-selection exercise, vendor review, field-mapping task, PIT metadata construction task, alpha-formula task, empirical discovery task, source-ingestion task, panel task, IC task, validation task, governance mutation, architecture change, production change, threshold change, survivor-status change, or ML task.

The classification applies only to the scientific framework. It does not imply source acceptance, classification-system acceptance, historical metadata acceptance, peer-group construction, PIT construction, formula readiness, candidate readiness, empirical validation, or implementation authorization.

## Repository Evidence Reviewed

Current authoritative state:

- `docs/research_notes/project_underdog_strategic_program_reassessment_v1.md`: final classification `PROJECT_READY_FOR_NEXT_MAJOR_PHASE`; peer/economic context is the highest-value next frontier, but implementation remains blocked by authoritative PIT metadata requirements; ML remains deferred.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: final classification `PHASE_5_PROGRAM_DEFINED`; Phase 5 is `External Information Integration`; static metadata cannot answer peer-relative scientific questions.
- `docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md`: final classification `PHASE_5_SCIENTIFIC_ROADMAP_DEFINED`; WS3 Economic Context Validity Science follows source authority and PIT identity/lineage science.
- `docs/research_notes/project_underdog_phase5_external_information_authority_science_v1.md`: final classification `EXTERNAL_INFORMATION_AUTHORITY_FRAMEWORK_DEFINED_WITH_OPEN_SCIENTIFIC_GAPS`; authority is role-specific and no source is accepted.
- `docs/research_notes/project_underdog_phase5_pit_identity_and_lineage_science_v1.md`: final classification `PIT_IDENTITY_AND_LINEAGE_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`; security identity remains distinct from economic-company identity, ticker is not stable identity, and identity must precede classification and peer authority.
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md` and `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`: Platform v2 hypothesis-first discipline, orthogonality, falsifiability, frozen expectations, and negative-evidence preservation remain governing standards.

Economic context, peer, PIT, source-gate, and metadata evidence:

- `docs/research_notes/point_in_time_economic_context_readiness_audit_v1.md`: economic-context substrate is diagnostically strong but not PIT discovery ready; current metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY`; historical integrity is the blocker.
- `docs/research_notes/economic_context_enrichment_design_v1.md`: prior design distinguished diagnostic static metadata, future PIT classifications, size context, and date-derived behavioral buckets; it did not authorize validation or peer-relative use.
- `docs/research_notes/economic_context_enrichment_v1_implementation.md`: implementation produced diagnostic-only coverage, fallback peer-quality reports, inventory exposure audits, and explicit blocks on peer-relative transforms, validation, production, portfolio, ML, blending, and optimization.
- `docs/research_notes/metadata_source_lineage_consistency_review_v1.md` and `docs/research_notes/manual_metadata_coverage_expansion_v3.md`: static metadata is internally consistent enough for descriptive diagnostics but not externally source-audited, not PIT-valid, and not suitable for historical alpha or validation.
- `docs/research_notes/peer_relative_economic_context_readiness_reassessment_and_scientific_program_framing_v1.md`: peer-relative work is `FRONTIER_READY_FOR_LIMITED_DESIGN_ONLY`; peer construction, formulas, panels, IC, validation, governance, production, thresholds, and ML remain blocked.
- `docs/research_notes/pit_external_dependency_closeout_v1.md`, `docs/research_notes/pit_external_evidence_intake_review_v1.md`, and source-gate notes: no authoritative source, entitlement, field inventory, retention, archive, reproducibility, known-date, or source-gate acceptance exists.
- `src/universe.py`: fully survivorship-free testing requires historical constituent membership or a point-in-time security master.

Validation, contamination, reproducibility, and negative-evidence materials:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`: validation-quality work requires scoped artifacts, manifests, checksums, contamination placeholders, and fail-closed guardrail flags.
- Existing OHLCV family notes and the Phase 5 roadmap identify stress repair, participation repair, volatility compression, VoV, persistence, rank behavior, reversal, dispersion, event, and transition evidence as future contamination references and comparators.
- Negative-evidence notes for Event Clustering, Dispersion Path-Dependence, and Non-Hostile Transition show that conceptual novelty must remain falsifiable and cannot be rescued after weak evidence.

Superseded or limited material:

- Prior peer-group fallback implementations are diagnostic practices, not authoritative peer logic.
- Static sector, industry, market-cap, size, and peer labels are descriptive metadata only.
- Source-specific assessments are requirement examples only; this note does not select, rank, or accept any source, vendor, classification taxonomy, or acquisition path.

## 1. Executive Scientific Classification

Final classification: `ECONOMIC_CONTEXT_VALIDITY_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

Rationale:

- Repository evidence is sufficient to define the scientific meaning, dimensions, validity requirements, temporal properties, ambiguity classes, acceptance outcomes, failure conditions, and downstream constraints for economic context.
- Open gaps remain because no authoritative historical sector, industry, subindustry, size, market-cap, business-model, revenue, geographic, peer-membership, or classification-system evidence is accepted for Phase 5 empirical use.
- Current static/current-state metadata remains diagnostic-only; peer construction remains blocked; ML remains deferred.

This classification does not imply source acceptance, classification-system acceptance, historical metadata acceptance, peer-group construction, PIT construction, formula readiness, candidate readiness, empirical validation, or implementation authorization.

## 2. Scientific Meaning Of Economic Context

`Economic context` is the source-authorized, point-in-time, role-specific comparison structure used to reason about whether two or more securities or economic companies were meaningfully comparable at a historical time.

Economic context is distinct from:

- security identity: the tradable instrument whose returns are observed;
- company identity: the issuer, legal entity, operating company, or economic company;
- descriptive metadata: current or static labels useful for diagnostics;
- current sector or industry labels: present-state classifications that can leak future information;
- correlation groups or statistical clusters: empirical similarity that may not reflect business comparability;
- market regimes: broad market state that can condition behavior without defining economic peers;
- benchmark membership: index or portfolio membership that may reflect construction rules rather than economic comparability;
- portfolio categories: implementation groupings that may optimize operations rather than science;
- implementation convenience: labels that are easy to join are not automatically valid.

Economic context is a scientific comparison structure because it states why observations should be compared. A sector label, industry label, size bucket, liquidity state, or regime state is only useful if it supports a falsifiable comparison claim with valid temporal, identity, coverage, and authority evidence.

## 3. Context Dimensions

| dimension | scientific purpose | likely information contribution | temporal behavior | contamination risk | authority requirement | Phase 5 relevance |
|---|---|---|---|---|---|---|
| Sector | Broad economic grouping. | Separates industry-wide and market-wide effects. | Changes with taxonomy and business evolution. | Static sector backfill, broad false comparability. | Historical classification authority and taxonomy version. | WS3, WS4, WS5. |
| Industry | More specific business cohort. | Stronger peer hypothesis than sector. | Reclassifications and taxonomy drift. | Thin groups, mixed granularity. | Historical industry membership and effective/known dates. | WS3, WS4. |
| Sub-industry | Granular operating similarity. | Highest business specificity when coverage exists. | Sparse and taxonomy-sensitive. | Too few peers, unstable groupings. | High-coverage historical taxonomy evidence. | WS3, WS4. |
| Business model | How company generates economics. | May explain repair, liquidity, and persistence differences. | Evolves gradually or abruptly. | Subjective labels, retrospective narratives. | Documented historical business-context evidence. | WS3, WS4, WS7. |
| Revenue exposure | Economic source of revenue. | Tests exposure similarity beyond labels. | Changes with business mix and reporting periods. | Reporting lag, restatements, segment changes. | Historical revenue/segment authority if ever used. | Future WS3/WS4. |
| Product-market exposure | Competitive market exposure. | Supports true competitor comparability. | Changes with product mix and industry structure. | Manual/inferred peer bias. | Source-authorized historical product/market evidence. | Future WS4/WS5. |
| Geographic exposure | Region or country exposure. | Separates domestic/global macro and currency effects. | Changes with sales mix and listings. | Current geography backfill. | Historical geographic exposure evidence. | Future WS3/WS4. |
| Size | Scale and capitalization context. | Controls size/liquidity/coverage effects. | Can change rapidly. | Current size leakage, arbitrary bands. | PIT market-cap or approved size evidence. | WS3, WS4, WS5. |
| Liquidity | Trading capacity and market microstructure. | Distinguishes tradability and participation states. | Date-varying and computable from OHLCV if lagged. | Confusing liquidity state with economic peer identity. | Pre-signal calculation lineage or accepted source evidence. | WS3, WS5. |
| Volatility | Risk and uncertainty state. | Controls for risk similarity and VoV overlap. | Highly date-varying. | Duplicates volatility compression or VoV. | Pre-signal calculation lineage if used. | WS3, WS5. |
| Leverage | Balance-sheet risk where future evidence may permit. | May explain stress sensitivity. | Reporting-lagged and restated. | Look-ahead via financial statement revisions. | Future authoritative accounting/date semantics. | Future WS3/WS5. |
| Lifecycle stage | Growth, mature, distressed, restructuring. | May explain repair and deterioration. | Evolves and can break at events. | Subjective post-hoc labels. | Documented historical stage evidence or predeclared derivation. | WS3, WS4. |
| Listing venue | Market access and trading environment. | Controls venue, exchange, and eligibility effects. | Changes with listing/delisting/migration. | Venue confused with company economics. | Accepted listing lineage. | WS2, WS3. |
| Security type | Common, preferred, ADR, warrant, right, etc. | Prevents non-comparable instruments. | Changes via conversions or issuance. | Mixing instrument economics. | Accepted instrument/security identity. | WS2, WS3. |
| Market regime | Broad market state. | Conditions behavior outside peer identity. | Date-varying. | Confounds peer effect with broad regime. | Existing OHLCV-derived regime lineage if used. | WS3, WS5. |
| Stress state | Market or security stress. | Controls repair/deterioration mechanisms. | Date-varying. | Duplicates core stress-repair family. | Predeclared OHLCV state lineage. | WS3, WS5, WS7. |
| Participation state | Breadth/liquidity participation context. | Explains participation repair and liquidity recovery. | Date-varying. | Duplicates participation family. | Pre-signal OHLCV calculation lineage. | WS3, WS5. |
| Macroeconomic environment | Broad economy/interest/inflation/credit context. | May condition sector/industry outcomes. | Date-varying and release-lagged. | Macro look-ahead and overbroad conditioning. | Future authoritative macro release-date evidence. | Future WS3/WS9. |

No dimension is approved for empirical use by this note.

## 4. Economic Comparability

Economic comparability means that two securities or economic companies are similar enough along explicitly defined dimensions to make a scientific comparison meaningful for a stated role and historical date.

Comparability may involve:

- structural similarity;
- exposure similarity;
- business similarity;
- size similarity;
- liquidity similarity;
- risk similarity;
- regime similarity;
- event similarity;
- temporal similarity;
- market-state similarity.

No single dimension necessarily establishes valid comparability. Same sector can be too broad. Same industry can be too sparse or classification-dependent. Similar size can pair unrelated businesses. Similar volatility can reflect temporary stress rather than economics. Correlation can reflect common shocks rather than shared business exposure.

Comparability classes:

- Strong comparability: multiple authoritative, date-valid dimensions agree and support the intended role.
- Conditional comparability: valid only under bounded role, date range, universe, or fallback condition.
- Weak comparability: partial similarity, insufficient for authoritative peer research but useful for questions.
- Diagnostic comparability: useful for descriptive exposure or sanity checks only.
- Invalid comparability: identity, timing, coverage, taxonomy, or conflict failures make the comparison scientifically unsafe.

## 5. Security-Level Versus Company-Level Context

Economic context may attach to different identity levels:

- Security: appropriate for return measurement, instrument type, share-class behavior, liquidity, and active trading status.
- Listing: appropriate for exchange, venue, currency, trading calendar, active eligibility, and delisting treatment.
- Issuer: appropriate for multiple securities issued by the same entity.
- Operating company: appropriate for business model and product-market exposure.
- Economic company: appropriate for peer/economic comparability when legally or instrument-distinct observations represent the same economic business.
- Research entity: derived observation unit for future research after accepted identity and context rules.

Company-level context may be appropriate while return measurement remains security-level when multiple securities represent the same economic company, such as multiple share classes, ADRs and ordinary shares, dual listings, or reorganized entities. It is not automatically appropriate for tracking stocks, preferred shares, warrants, rights, subsidiaries, spinoffs, reverse mergers, or economically linked but legally distinct entities.

Identity science from WS2 controls this relationship: security identity remains distinct from economic-company identity, and ticker is not a stable identity.

## 6. Sector And Industry Science

Sector, industry, and sub-industry classifications are hypotheses about economic comparability. They are not automatically valid peer definitions.

Scientific roles:

- hierarchical classification can express broad-to-specific comparability;
- overlapping classifications may capture different business realities;
- evolving classification systems can alter historical meaning;
- classification-system revisions can split, merge, rename, or redefine groups;
- company reclassification can reflect business evolution or taxonomy change;
- diversified companies and conglomerates may fit multiple contexts;
- multi-industry firms can make single-label peer groups weak;
- missing or ambiguous classifications must be explicit;
- retrospective relabeling can leak future business knowledge into past dates.

A classification label is a compact claim that a company belongs to a comparable economic group at a date. It requires authority, taxonomy version, temporal validity, coverage, revision transparency, and conflict handling before it can support peer-relative research.

## 7. Historical Classification Validity

Historical classification evidence must establish both historical applicability and historical knowability.

Required properties:

- classification effective date;
- announcement date where relevant;
- publication date;
- availability date;
- revision date;
- historical version or source snapshot;
- treatment of overwritten history;
- treatment of retrospective backfills;
- taxonomy changes;
- renamed categories;
- split or merged categories;
- project-known date.

A historical classification can be treated as point-in-time valid only when:

- the classification is linked to accepted identity and listing evidence;
- the taxonomy version and category definition are known;
- the classification was effective for the historical date;
- the source availability or project-known date does not introduce look-ahead;
- revisions and backfills are versioned or reconstructable;
- coverage and missingness are measured;
- conflicts are resolved or blocked.

This note does not define executable PIT logic.

## 8. Classification-System Comparability

Multiple classification systems may differ in taxonomy, hierarchy depth, assignment method, diversified-company treatment, update cadence, historical depth, and conflict behavior.

Possible relationships among systems:

- Complementary: systems capture different useful aspects, but each remains role-specific.
- Role-specific: one system may be suitable for broad sector diagnostics while another is suitable for industry comparability.
- Diagnostic: useful for conflict discovery or sensitivity review only.
- Conditionally reconcilable: mappings may work for bounded groups, dates, or hierarchy levels.
- Scientifically incompatible: definitions differ enough that combining or substituting them would alter the comparison claim.

Project Underdog should not collapse systems by name similarity alone. Category mappings must preserve date, taxonomy version, definition, and uncertainty. No real classification system is ranked or selected here.

## 9. Size Context Science

Size helps distinguish economically comparable peers from superficially similar but structurally different securities or companies.

Size concepts:

- market capitalization;
- float-adjusted market capitalization;
- enterprise scale where future evidence may permit;
- revenue scale where future evidence may permit;
- asset scale where future evidence may permit;
- liquidity scale;
- capitalization bands;
- continuous versus categorical size;
- size transitions;
- rapidly changing size;
- missing shares evidence.

Size may affect comparability because scale influences liquidity, investor base, volatility, capacity, index membership, information diffusion, and stress response. Size can also contaminate peer research if current market cap is backfilled, if shares are missing or restated, if share classes are double counted, or if bands create artificial discontinuities.

No size thresholds, formulas, or buckets are approved here.

## 10. Market And Regime Context

Market context is distinct from economic peer context. It describes the broad state in which securities trade, not necessarily which securities are economically comparable.

Relevant market contexts:

- broad market state;
- volatility regime;
- liquidity regime;
- stress regime;
- participation state;
- trend state;
- transition state;
- benchmark state.

Existing Project Underdog OHLCV-derived state evidence may act as:

- a control for broad-market conditions;
- a conditioning variable for hypotheses;
- a confounder that explains apparent peer behavior;
- a comparator or contamination reference;
- a separate scientific context from external economic context.

Validated or diagnostic own-market context must remain distinct from unvalidated external economic context. A future peer-relative claim must show it is not merely stress repair, participation repair, volatility compression, VoV, persistence, rank behavior, reversal, or broad market-state exposure under a new label.

## 11. Context Stability And Drift

Economic context changes through time.

Change channels:

- gradual business-model evolution;
- abrupt strategic changes;
- acquisitions;
- divestitures;
- spinoffs;
- restructurings;
- sector migration;
- industry migration;
- size migration;
- geographic exposure changes;
- classification lag.

Context states:

- Valid context continuity: the comparison remains scientifically meaningful across time with evidence.
- Context drift: economic similarity changes gradually and may require stale-age or review controls.
- Context break: event or business transformation invalidates prior context continuity.
- Ambiguous context transition: evidence is incomplete or timing is uncertain.
- Retrospective context reassignment: later source labels rewrite history and must not be silently used as PIT evidence.

## 12. Peer Eligibility Science

A future peer candidate would require:

- valid identity;
- active listing status;
- historical classification validity;
- economic comparability;
- size comparability if size is part of the role;
- sufficient data coverage;
- temporal overlap;
- corporate-event status;
- security-type compatibility;
- absence of fatal ambiguity.

Peer eligibility is not the same as peer construction. This note defines scientific properties only and does not create peer groups or numeric peer-count rules.

## 13. Peer Hierarchy Science

Possible hierarchical peer structures:

- sub-industry;
- industry;
- sector-and-size;
- sector;
- broad size;
- market-wide;
- no valid peer context.

Hierarchical fallback may be defensible when the fallback dimension still matches the scientific question, the change in meaning is explicit, missingness is governed, and downstream claims are narrowed. Fallback changes the comparison's meaning: industry-relative repair is not the same as sector-size-relative repair, and sector fallback is not a substitute for true peer comparability.

Fallback becomes diagnostic-only when it exists to preserve coverage rather than support the original comparison claim. The system must fail closed when fallback would silently convert missing, sparse, stale, or conflicting context into apparent authority. Prior diagnostic fallback hierarchies are not approved for authoritative use.

## 14. Peer-Count Validity

Peer-set breadth matters scientifically because a peer comparison with too few, unstable, duplicated, or concentrated members can create false precision.

Conceptual risks:

- too few peers;
- unstable peer counts;
- changing peer counts;
- dominant large peers;
- duplicate economic exposure;
- multiple share classes;
- sparse industries;
- concentrated industries;
- peer collapse during historical periods.

Peer-count validity requires date-level reporting, duplicate exposure controls, active eligibility, security-type compatibility, and explicit treatment of sparse periods. No minimum numeric peer count is defined here.

## 15. Peer Membership Timing

Peer membership requires temporal alignment across:

- membership effective date;
- classification effective date;
- availability date;
- security eligibility date;
- listing date;
- delisting date;
- transformation date;
- size-context date;
- project-known date.

Retrospective peer assignment creates look-ahead contamination because it can assign a company to a peer group based on future classification, future business evolution, future size, future survival, or a later taxonomy revision. A peer set must represent what was knowable and eligible at the historical signal date for the intended role.

## 16. Economic Context Ambiguity Taxonomy

| ambiguity class | scientific meaning | minimum evidence required | permitted use | prohibited use | downstream effect |
|---|---|---|---|---|---|
| Classification ambiguity | Label uncertain or disputed. | Dated classification evidence and source-role assessment. | Diagnostic or resolved role-specific use. | Authoritative peer assignment before resolution. | Blocks WS4 empirical use. |
| Taxonomy ambiguity | Category definition/version unclear. | Taxonomy version and methodology. | Diagnostic sensitivity. | Cross-system substitution. | Blocks classification validity. |
| Temporal ambiguity | Effective/known date uncertain. | Bounded interval, source snapshot, confidence penalty. | Conditional use if not signal-sensitive. | Historical use across event/signal boundary. | May block PIT validity. |
| Diversified-company ambiguity | Multiple business exposures. | Historical segment/business evidence if used. | Diagnostic or multi-context question. | Single-label peer authority. | Weakens comparability. |
| Size ambiguity | Market cap, float, shares, or scale uncertain. | Date-safe size evidence and definition. | Diagnostic size review. | Size-controlled peer claim. | Blocks size context. |
| Peer-membership ambiguity | Peer eligibility unclear. | Accepted inputs and membership timing. | Quarantine/diagnostic. | Peer-relative transforms. | Blocks WS4 empirical work. |
| Identity-context mismatch | Context attached to wrong security/company level. | WS2 identity relationship evidence. | Diagnostic only until resolved. | Company-context joins to wrong security. | Fatal for affected rows. |
| Corporate-transformation ambiguity | Event changes context continuity. | Event evidence and context treatment. | Diagnostic event review. | Continuous peer context across break. | Blocks affected period. |
| Missing-context ambiguity | Required context absent. | Missingness classification and coverage report. | Diagnostic missingness. | Silent fallback. | Blocks or narrows claims. |
| Source-conflict ambiguity | Credible context evidence disagrees. | Conflict assessment. | Resolved/conditional/diagnostic. | Convenience choice. | Quarantine if material. |
| Fatal comparability ambiguity | Material comparability cannot be supported. | Rejection rationale. | Negative evidence. | Authoritative or conditional use. | Rejects context relation. |

## 17. Evidence Hierarchy For Economic Context

| evidence type | scientific strength | permitted use |
|---|---|---|
| Authoritative historical classifications | Very strong after source-role acceptance. | Context acceptance for defined role/scope. |
| Official classification methodology | Very strong. | Category meaning and assignment interpretation. |
| Official effective-date history | Very strong. | PIT classification timing. |
| Authoritative company-security relationships | Very strong after WS2 acceptance. | Attach context to the correct identity level. |
| Official corporate-event evidence | Strong. | Context break/drift/continuity decisions. |
| Source-provided size history | Strong if date-safe and reproducible. | Size context after authority review. |
| Independent corroboration | Moderate. | Conflict diagnosis and confidence support. |
| Current-state profiles | Diagnostic only. | Descriptive exposure and question generation. |
| Manually curated labels | Diagnostic or conditional. | Bounded review only with retained evidence. |
| Inferred business similarity | Weak. | Hypothesis generation. |
| Return correlation | Weak for economics; moderate for statistical diagnostics. | Confounder or comparator, not peer authority. |
| Statistical clustering | Diagnostic. | Exploratory grouping and contamination review. |
| Heuristic grouping | Weak. | Manual review queue or synthetic scenario design. |

## 18. Context Conflict Science

Credible context evidence can disagree across sector, industry, taxonomy, size, company/security level, business model, timing, and corporate-event treatment.

Conflict outcomes:

- Resolved: role-specific evidence supports one interpretation and conflict is logged.
- Conditionally accepted: one interpretation is valid only for bounded dates, hierarchy level, identity level, or use.
- Diagnostic-only: disagreement is useful evidence of uncertainty but cannot support authority.
- Quarantined: affected context relationship is withheld pending evidence.
- Rejected: relationship fails comparability or temporal validity requirements.

Project Underdog should reason by role, evidence strength, temporal semantics, and scientific consequence. No vendor or taxonomy precedence is defined.

## 19. Economic Context Acceptance Framework

Future context assignments or relationships should be assessed for:

- identity validity;
- role-specific authority;
- temporal precision;
- classification validity;
- taxonomy validity;
- comparability;
- coverage;
- revision transparency;
- reproducibility;
- conflict status;
- downstream-use fitness.

Possible outcomes:

| outcome | meaning |
|---|---|
| `ECONOMIC_CONTEXT_ACCEPTED` | Evidence is sufficient for the context role, date range, identity level, and downstream use. |
| `ECONOMIC_CONTEXT_CONDITIONALLY_ACCEPTED` | Evidence is sufficient only under explicit conditions. |
| `ECONOMIC_CONTEXT_DIAGNOSTIC_ONLY` | Useful for descriptive review but not authoritative PIT use. |
| `ECONOMIC_CONTEXT_QUARANTINED` | Withheld pending missing evidence or conflict resolution. |
| `ECONOMIC_CONTEXT_REJECTED` | Fails a fatal scientific condition. |
| `INSUFFICIENT_EVIDENCE` | Current evidence cannot support a decision. |

No outcome is applied to real securities or classifications.

## 20. Fail-Closed Conditions

Economic context must fail closed under:

- current classifications applied historically;
- missing required effective dates;
- missing source-known dates;
- unresolved identity-context mismatch;
- retrospective peer assignment;
- unknown taxonomy version;
- overwritten classification history;
- unresolved diversified-company classification where material;
- unsupported size context;
- missing delisted entities;
- peer-set duplication through share classes;
- silent fallback;
- insufficient comparable entities for the intended role;
- source conflicts without resolution;
- corporate-event transitions without context treatment;
- context relationships outside accepted source roles;
- static/current-state metadata used for historical claims;
- missing classification coverage that is outcome, size, sector, event, or distress related;
- classification-system mapping by name similarity alone.

## 21. Synthetic Context Scenarios

| scenario | setup | expected context interpretation | expected peer eligibility | ambiguity status | downstream restriction | fail-closed behavior |
|---|---|---|---|---|---|---|
| Stable company and stable industry | Identity and industry unchanged. | Context continuity possible if authority/dates exist. | Eligible conceptually. | Resolvable. | Use only after source acceptance. | Block without historical evidence. |
| Industry reclassification | Company moves from industry A to B. | Context changes at effective/known date. | Eligible only by date window. | Temporal/classification ambiguity. | No retrospective assignment. | Block missing effective/known date. |
| Sector reclassification | Sector label changes. | Broad context changes. | Conditional by taxonomy/date. | Taxonomy ambiguity. | No sector-relative claim across unresolved change. | Quarantine affected interval. |
| Diversified company | Multi-business firm. | Single context may be weak. | Conditional or diagnostic. | Diversified-company ambiguity. | Avoid strong peer claims. | Fail closed if material and unresolved. |
| Company changing primary business | Business model shifts. | Context drift or break. | Eligible only after context treatment. | Context transition ambiguity. | No continuous peer context by old label. | Block across break if unsupported. |
| Acquisition changing context | Company acquires different business. | Possible context drift/break. | Conditional after event evidence. | Corporate-transformation ambiguity. | Require event-aware context. | Quarantine if event untreated. |
| Spinoff creating new context | Child begins distinct business. | New context begins with child. | Child eligible only from start date. | Resolvable with event evidence. | No inherited parent peer history. | Block pre-spinoff child context. |
| Rapid size transition | Market cap changes sharply. | Size context changes. | Size peers conditional by date. | Size ambiguity. | No static size bucket. | Block missing date-safe size. |
| Missing industry but known sector | Broad context known, specific unknown. | Sector-only comparison changes meaning. | Diagnostic or conditional fallback. | Missing-context ambiguity. | No industry-relative claim. | Fail closed for industry role. |
| Sparse industry | Few valid peers. | Comparison may lack breadth. | Diagnostic or conditional. | Peer-count ambiguity. | No strong peer conclusion. | Block if comparability insufficient. |
| Peer-count collapse | Historical delistings reduce group. | Peer set unstable. | Conditional by period. | Peer-membership ambiguity. | No stable peer claim. | Block collapsed periods if needed. |
| Conflicting classifications | Two sources disagree. | Conflict must be assessed. | Quarantine until resolved. | Source-conflict ambiguity. | No convenience choice. | Diagnostic-only or reject. |
| Classification published after effective date | Effective date precedes availability. | Known-date controls required. | Eligible only after availability or accepted lag. | Temporal ambiguity. | No pre-availability peer use. | Block if availability unknown. |
| Taxonomy revision | Categories split/merge. | Historical category meaning changes. | Conditional by taxonomy version. | Taxonomy ambiguity. | No cross-version merge by name only. | Quarantine mapped categories. |
| Dual-listed company | Same economic company, distinct listings. | Company context may be shared; security/listing context distinct. | Conditional after WS2 identity. | Identity-context mismatch risk. | Avoid duplicate exposure. | Block unsupported aggregation. |
| Multiple share classes | Same issuer has classes A/B. | Company context shared; security context distinct. | Conditional with duplicate control. | Share-class/peer duplication ambiguity. | No double-counted peers. | Block primary choice if unsupported. |
| Delisted peer | Peer exits universe. | Peer eligibility ends at delisting. | Eligible only before terminal state. | Terminal-state ambiguity if missing. | No survivor-only peers. | Block if delisting missing. |

These are conceptual scenarios. No fixtures or tests are implemented.

## 22. Relationship To Existing OHLCV Context

Future external economic context should relate to existing OHLCV evidence as:

- an independent feature family only if future evidence shows it adds non-redundant information;
- conditioning context for hypotheses after PIT validity exists;
- control variable for sector, industry, size, or market-wide effects;
- benchmark for peer-relative interpretation;
- peer-definition substrate if classifications and identity are accepted;
- interpretive layer for existing family evidence.

Relevant Project Underdog contexts include market state, stress state, participation breadth, transition state, volatility compression, VoV, persistence, rank behavior, and repair behavior. External context must be tested conceptually against these as contamination references before formulas or panels exist. This note defines no formulas.

## 23. Context Versus Statistical Similarity

Economic comparability is not the same as empirical statistical similarity.

Statistical similarities include:

- return correlation;
- volatility similarity;
- beta similarity;
- trend similarity;
- drawdown similarity;
- liquidity similarity;
- clustering;
- learned embeddings in future phases.

Statistically similar securities may not be economically comparable because common market shocks, factor exposure, stress regimes, liquidity conditions, or index flows can create temporary co-movement. Economically comparable securities may exhibit different returns because of idiosyncratic news, balance-sheet differences, management quality, geography, capital structure, or event timing.

Statistical similarity can support diagnostics, controls, contamination review, or future ML-readiness questions. It cannot substitute for economic context authority.

## 24. Downstream Scientific Consequences

Economic-context validity affects:

- peer-relative hypothesis framing;
- relative repair;
- relative stabilization;
- relative deterioration;
- relative persistence;
- relative leadership;
- contamination review;
- orthogonality assessment;
- validation;
- negative-evidence interpretation;
- integrated feature inventory;
- future ML readiness.

Invalid context can convert static labels, survivorship, size leakage, taxonomy drift, peer-count instability, or broad market regimes into false alpha evidence. Valid context can clarify whether own-security OHLCV behavior is idiosyncratic, peer-wide, sector-wide, size-driven, regime-conditioned, or contaminated.

## 25. Minimum Prerequisites For Workstream 4

Workstream 4 `Peer-Relative Hypothesis Science` may proceed substantively after the following are clear.

Conceptual prerequisites satisfiable now:

- definition of economic context and comparability;
- distinction between security-level and company-level context;
- context dimensions and ambiguity taxonomy;
- peer eligibility and hierarchy science;
- fail-closed conditions;
- synthetic context scenarios;
- relationship to existing OHLCV contexts.

Prerequisites requiring future authoritative evidence:

- accepted historical classifications;
- accepted taxonomy and date semantics;
- accepted identity/context relationships;
- accepted size or market-cap context if used;
- accepted listing/delisting and survivorship evidence;
- reproducibility, retention, and revision evidence.

Prerequisites blocking empirical work only:

- PIT economic metadata construction;
- historical classification construction;
- size record construction;
- peer-group construction;
- formulas, candidates, panels, IC, validation.

Questions that may remain open during hypothesis framing:

- whether industry is always better than sector;
- whether size is mandatory for every peer definition;
- how diversified firms should be represented;
- whether fallback is ever more than diagnostic;
- how market regime should interact with peer definitions.

## 26. Open Scientific Question Register

| question | why it matters | affected downstream workstream | current repository evidence | required future evidence |
|---|---|---|---|---|
| Is industry always superior to sector? | Industry is more specific but can be sparse or inconsistent. | WS4, WS5 | Static diagnostics show many thin industry groups. | Historical coverage, peer-count stability, classification authority. |
| Must size be part of every peer definition? | Size can control comparability but may reduce coverage or add leakage. | WS4 | Size is identified as important but static-only. | PIT size/market-cap evidence and role-specific tests. |
| Do diversified firms require multiple contexts? | Single labels may misrepresent conglomerates. | WS3, WS4 | Prior notes flag mixed granularity and broad labels. | Historical segment/business exposure evidence. |
| Are fallback peer groups scientifically comparable? | Fallback may change the question. | WS4 | Current fallback hierarchy is diagnostic-only. | Role-specific fallback meaning and validation after authority. |
| Should market regime alter peer definitions? | Regimes may condition behavior but not define economics. | WS4, WS5 | OHLCV states are existing context and contamination references. | Source-independent hypothesis design and contamination plan. |
| How should classification lag be handled? | Effective and publication dates may diverge. | WS3, WS4 | Known-date semantics remain unresolved. | Official availability/revision evidence or accepted lag rules. |
| How should context uncertainty propagate? | Validation and peer claims need uncertainty flags. | WS5, WS8 | WS1/WS2 require fail-closed ambiguity. | Artifact design carrying confidence and blocked context. |
| Can statistical similarity supplement economic context? | It may improve diagnostics but risks replacing economics with clusters. | WS4, WS9 | Existing evidence uses statistical correlations as contamination diagnostics. | Explicit role definitions and future validation design. |
| How do changing business models affect peer continuity? | Context drift can invalidate peer history. | WS3, WS4, WS7 | Current static labels cannot represent drift. | Historical business-change and classification evidence. |
| Can macro context become part of economic context? | Macro releases have separate known-date risks. | Future WS3, WS9 | Macro is deferred in Phase 5. | Release-date authority and role-specific scope. |

## 27. Recommended Next Scientific Step

Recommended next Project Underdog lifecycle step:

`Project Underdog - Phase 5 Workstream 4 Peer-Relative Hypothesis Science v1`

Scope:

- conceptual scientific requirements only;
- define source-agnostic, falsifiable peer-relative hypotheses that consume WS1 authority, WS2 identity/lineage, and WS3 economic-context frameworks;
- preserve all source, taxonomy, access, implementation, PIT construction, historical classification construction, peer construction, formula, candidate, panel, IC, validation, governance, production, threshold, survivor-status, and ML blocks.

Rationale:

Workstream 4 is the next step in the Phase 5 roadmap. WS3 defines what economic comparability must mean before empirical peer work can exist. WS4 can now frame peer-relative scientific questions conceptually while all construction and empirical work remains blocked.

## Conclusion

Final classification: `ECONOMIC_CONTEXT_VALIDITY_SCIENCE_FRAMEWORK_DEFINED_WITH_OPEN_GAPS`

Project Underdog can now define economic context as a role-specific, point-in-time scientific comparison structure rather than a metadata label. The framework defines context dimensions, comparability classes, security-versus-company attachment, historical classification validity, classification-system conflict science, size and market-state roles, context drift, peer eligibility, hierarchy and count concepts, ambiguity classes, evidence hierarchy, acceptance outcomes, fail-closed conditions, synthetic scenarios, and downstream constraints. No source, taxonomy, historical metadata, peer group, formula, candidate, panel, validation, production, threshold, survivor-status, or ML work is authorized.

Recommended next scientific step: `Project Underdog - Phase 5 Workstream 4 Peer-Relative Hypothesis Science v1`.

## Verification And Boundary Check

Repository searches and checks used:

- `rg -n 'economic context|sector|industry|subindustry|peer|size|market.cap|market cap|classification|taxonomy|fallback|STATIC_SNAPSHOT|diagnostic-only|diagnostic only|PIT|point-in-time|context validity|peer-relative|metadata|source lineage|survivorship|delisting|universe|volatility compression|VoV|persistence|rank|repair' docs/research_notes src`
- Direct review of WS1 authority science, WS2 identity and lineage science, Phase 5 roadmap and program notes, strategic reassessment, Platform v2 standards, PIT/source-gate notes, point-in-time economic-context readiness audit, economic-context enrichment design and implementation notes, metadata source-lineage review, peer-relative readiness note, validation artifact contract, and negative-evidence materials.

Boundary verification:

- No institution or vendor was contacted.
- No source, taxonomy, classification vendor, or acquisition path was selected.
- No access, data retrieval, proprietary documentation retrieval, source inspection, connector creation, source query, implementation, PIT construction, historical classification construction, size-record construction, peer construction, peer formula, alpha formula, candidate assignment, panel generation, IC calculation, validation, governance change, architecture change, production change, threshold change, survivor-status change, or ML work was performed.
