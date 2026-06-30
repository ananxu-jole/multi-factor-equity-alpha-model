# Project Underdog - CRSP Track Checkpoint and Main Research Resume v1

## SECTION 1 - CRSP Track Checkpoint

The CRSP/PIT metadata track is now cleanly paused.

Completed CRSP/PIT work:

- PIT metadata source-gate planning, scaffold design, and semantic validation planning.
- Security Master and Ticker Lineage PIT architecture planning.
- Candidate source survey, framework design, real-source identification, and CRSP source-candidate evaluation.
- CRSP lineage design review, integration design, integration planning gap-closure review, implementation architecture, implementation specification, and scaffold implementation.
- CRSP assumption verification design, scaffold implementation, post-scaffold review, documentary assumption verification execution, external verification requirements package, and external evidence verification review.

Current classification:

- `EXTERNAL_EVIDENCE_INCOMPLETE`.

Why the track is paused:

- Internal planning is complete.
- Public documentation has been exhausted for responsible inference.
- No institutional subscription documentation, license agreement, retention memo, official CRSP data dictionary, release/version documentation, CRSP support clarification, authorized schema inspection artifact, source-file manifest, checksum policy, or archive policy is available.
- No remaining blocker can be resolved by more internal CRSP planning.

Evidence required to resume:

- Institutional CRSP subscription entitlement summary.
- License and allowed-use confirmation.
- Retention rights for raw files, source references, hashes, row counts, derived metadata, documentation references, and review notes.
- Archive/hash or controlled-reference policy.
- Official CRSP data dictionary or authorized schema-level evidence.
- Release/version or snapshot/extract documentation.
- Known-date or conservative source release/snapshot fallback semantics.
- Event-date, ticker-window, exchange/listing, share-class, and ticker reuse documentation.
- Source-file reproducibility evidence.

First task upon resume:

**Project Underdog - CRSP External Evidence Intake Checklist v1** or, if the evidence package is already available, **Project Underdog - CRSP External Evidence Intake Review v1**. Either task should remain evidence-review-only unless a later explicit task authorizes scaffold patching or source-loading design.

## SECTION 2 - Completed PIT/CRSP Artifacts

Major completed CRSP/PIT notes:

- `pit_source_evaluation_plan_v1.md`
- `pit_source_evaluation_plan_review_v1.md`
- `first_pit_source_candidate_evaluation_v1.md`
- `security_master_ticker_lineage_source_candidate_survey_v1.md`
- `security_master_ticker_lineage_source_candidate_evaluation_framework_v1.md`
- `security_master_ticker_lineage_source_candidate_identification_v1.md`
- `crsp_source_candidate_evaluation_v1.md`
- `crsp_lineage_design_review_v1.md`
- `crsp_integration_design_v1.md`
- `crsp_integration_planning_gap_closure_review_v1.md`
- `crsp_security_master_ticker_lineage_implementation_design_v1.md`
- `crsp_security_master_ticker_lineage_implementation_specification_v1.md`
- `crsp_security_master_ticker_lineage_scaffold_implementation_v1.md`
- `crsp_assumption_verification_design_v1.md`
- `crsp_assumption_verification_scaffold_implementation_v1.md`
- `crsp_assumption_verification_post_scaffold_review_v1.md`
- `crsp_assumption_verification_execution_v1.md`
- `crsp_external_verification_requirements_package_v1.md`
- `crsp_external_evidence_verification_v1.md`

Major scaffolds and runners:

- `pipelines/run_point_in_time_economic_metadata_scaffold_v1.py`
- `pipelines/run_crsp_security_master_ticker_lineage_pit_v1.py`

Major CRSP artifact root:

- `artifacts/research/crsp_security_master_ticker_lineage_pit_v1/`

Completed CRSP artifact subfolders:

- `source_gate/`
- `schemas/`
- `assumptions/`
- `diagnostics/`
- `lineage_design/`
- `validation_reports/`
- `manifests/`
- `review/`

Key assumption artifacts:

- `crsp_assumption_register.csv`
- `crsp_assumption_verification_checklist.csv`
- `crsp_assumption_evidence_register.csv`
- `crsp_assumption_status_placeholder.csv`
- `crsp_source_gate_eligibility_update.json`
- `crsp_subscription_scope_review.csv`
- `crsp_license_retention_review.csv`
- `crsp_field_availability_review.csv`
- `crsp_date_semantics_review.csv`
- `crsp_archive_hash_feasibility_review.csv`

Tests:

- `tests/test_crsp_security_master_ticker_lineage_pit_scaffold.py`

Prior verification state:

- CRSP scaffold validation modes passed in the scaffold implementation and assumption verification execution cycles.
- The scaffold remains fail-closed and does not authorize CRSP data access, source loading, ingestion, metadata construction, lineage construction, validation, production use, or ML.

## SECTION 3 - Explicit Pause Boundary

No more CRSP planning is useful until external evidence exists.

The CRSP/PIT track should not repeat:

- Candidate source survey.
- CRSP source-candidate evaluation.
- CRSP lineage design review.
- CRSP implementation architecture design.
- CRSP implementation specification.
- CRSP scaffold implementation.
- CRSP assumption verification design.
- CRSP documentary/public evidence verification.
- External verification requirements packaging.

No CRSP work is authorized for:

- CRSP dataset access.
- Source loading.
- Source-file inspection.
- Ingestion.
- Metadata construction.
- Security lineage construction.
- Ticker lineage construction.
- Sector/industry history reconstruction.
- Peer reconstruction.
- Discovery.
- Refinement.
- Validation.
- Governance mutation.
- Production registration.
- ML.

CRSP resume condition:

- Resume only when external evidence is available: subscription, license, retention, data dictionary, release/version, known-date, archive/hash, source reproducibility, and source-gate evidence.

## SECTION 4 - Main Research State

Current alpha-family inventory:

Established:

- Hostile/stress-repair remains the core established research umbrella.
- Participation breadth repair and related stabilization behaviors remain the strongest evidence base.

Conditional validation candidates:

- Persistence: `post_drawdown_persistence_churn_adjusted_20` completed validation as `CONDITIONAL VALIDATION CANDIDATE`, with useful h10/h20 behavior and low stress-repair contamination.
- Rank-coherence: `rank_coherence_churn_avoidance_02_overlap_adjusted` is the strongest rank-coherence thread, with refinement evidence and validation-review path; it remains candidate-level and h20-led.

Exploratory/weak:

- Dispersion remains conceptually independent but empirically weak.
- Transition-state dynamics remain useful but often collapse back toward hostile/stress-repair.
- Structural interaction, recovery-quality targets, volatility shock absorption, and non-price liquidity repair remain diagnostic or exploratory rather than established family axes.

Metadata/PIT:

- PIT metadata and CRSP-backed Security Master/Ticker Lineage work are paused pending external evidence.
- Peer-relative and economic-context alpha remains blocked for validation-quality use until PIT metadata exists.

## SECTION 5 - Main Research Bottleneck

Family diversification remains the main bottleneck.

Rationale:

- The project has one established family umbrella and two conditional candidate-lineages.
- The inventory remains concentrated in hostile/stress repair, h20 stabilization, repair-adjacent states, and post-drawdown behavior.
- Persistence and rank-coherence improve diversification but remain candidate-level rather than broad validated family proof.
- Dispersion is independent in concept but not strong enough yet.

ML remains premature:

- The family inventory is too narrow.
- ML would likely learn stress/repair state exposure rather than independent mechanisms.
- PIT peer-relative/economic-context features are not validation-ready.

Options and fixed income remain future-phase:

- Both would introduce new data quality, mapping, liquidity, calendar, and governance complexity before the equity family inventory is balanced.
- They should wait until at least two established equity alpha families exist and the metadata substrate is stronger.

Peer-relative/context-aware discovery remains blocked pending PIT evidence:

- This remains the largest strategic gap.
- Static metadata or current-ticker peer groups are not sufficient for validation-quality work.
- CRSP/PIT evidence must resume before this frontier can move into execution.

## SECTION 6 - Recommended Next Research Frontier

Possible paths:

New OHLCV family discovery:

- Advantage: unblocked by CRSP/PIT evidence.
- Best use: design a disciplined discovery pass around non-repair mechanisms using only existing OHLCV-safe inputs.
- Risk: may drift back into repair/stabilization unless anti-contamination constraints are explicit.

Transition-state family:

- Advantage: nearby and already has diagnostic infrastructure.
- Best use: focus on non-hostile transitions such as calm-to-expansion, compression-to-dispersion, leadership rotation, or neutral accumulation without breakout.
- Risk: prior transition-state work often became stress-adjacent.

Dispersion revisit:

- Advantage: conceptually independent from repair, persistence, and rank-coherence.
- Best use: narrow diagnostic revisit with robustness-first design and anti-repair controls.
- Risk: prior dispersion evidence was weak and h20-decayed.

Peer-relative waitlist:

- Advantage: highest strategic independence.
- Current state: blocked until PIT evidence exists.
- Recommendation: keep waitlisted, do not execute.

Portfolio/validation consolidation:

- Advantage: reduces ambiguity around conditional candidates and active inventory.
- Best use: consolidate persistence, rank-coherence, and hostile/stress-repair status before more discovery.
- Risk: consolidation alone does not create new family breadth.

Alpha inventory consolidation:

- Advantage: strongest immediate control move after a long CRSP detour.
- Best use: create an up-to-date main-roadmap checkpoint with candidates, families, statuses, blockers, and next-frontier eligibility.
- Risk: too much review can delay discovery if repeated.

Recommended next non-CRSP research move:

**Alpha inventory consolidation followed by a new OHLCV-only non-repair discovery design.**

Why this is best:

- CRSP/PIT is paused.
- Peer-relative discovery is blocked.
- ML and new asset classes are premature.
- The project needs family breadth, but after the CRSP branch, it also needs a clean inventory handoff.
- A short consolidation task can prevent repeated work and then steer into a transition-state or dispersion-aware OHLCV discovery design with anti-stress-repair constraints.

## SECTION 7 - 30-Day Resume Plan

Week 1: Main inventory consolidation.

- Create a current alpha-family status map.
- Freeze candidate classifications: established, conditional, exploratory, diagnostic, paused, rejected.
- Identify which candidates are eligible for monitoring, validation-review design, or future discovery comparison.
- Confirm CRSP/PIT remains paused.

Week 2: Non-CRSP frontier design.

- Design a small OHLCV-only discovery frontier targeting non-repair mechanisms.
- Candidate themes: transition-state dynamics outside hostile/stress repair, dispersion structure revisit, leadership rotation without PIT metadata, neutral accumulation, and volatility/participation behavior outside repair.
- Include anti-contamination rules against hostile/stress-repair, persistence, and rank-coherence.

Week 3: Candidate panel generation plan.

- Predeclare a small candidate panel.
- Define horizons, scoring metrics, redundancy diagnostics, contamination references, and stop conditions.
- Keep the batch small to avoid parameter mining.

Week 4: Review gate.

- Decide whether to execute the small discovery batch.
- Confirm no validation, governance mutation, production registration, or ML is authorized.
- Keep peer-relative/context-aware discovery on the PIT waitlist.

Expected 30-day outcome:

- CRSP/PIT paused cleanly.
- Main alpha roadmap refreshed.
- One disciplined non-CRSP discovery design ready for execution review.
- No accidental restart of metadata or ML work.

## SECTION 8 - Final Recommendation

Is CRSP paused cleanly?

Yes. The CRSP/PIT metadata track is paused at `EXTERNAL_EVIDENCE_INCOMPLETE`. The resume point is clear: external subscription, license, retention, data dictionary, release/version, known-date, archive/hash, and source reproducibility evidence must arrive before the track resumes.

What should not be touched until external evidence appears?

CRSP source access, source loading, source-file inspection, ingestion, metadata construction, security lineage construction, ticker lineage construction, source-gate advancement, PIT peer reconstruction, sector/industry reconstruction, and peer-relative validation-quality discovery should not be touched.

What should Project Underdog focus on next?

Project Underdog should return to main alpha-family research and focus on family diversification. The immediate move should be alpha inventory consolidation, followed by an OHLCV-only non-repair discovery design.

What should the next Codex task be?

The next Codex task should be **Project Underdog - Main Alpha Inventory Consolidation and Non-CRSP Frontier Selection v1**. It should consolidate current family/candidate status, preserve the CRSP pause boundary, compare non-CRSP frontier options, and select the next small research design. It should be review/design-only and should not run discovery, refinement, validation, governance mutation, production registration, or ML.

## Research Caveat

This checkpoint is review-only. It does not implement code, ingest data, construct metadata, build lineage, run discovery, run refinement, run validation, modify governance, register production outputs, promote/demote candidates, or implement ML.
