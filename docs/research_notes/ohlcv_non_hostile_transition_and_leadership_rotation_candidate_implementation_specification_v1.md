# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Candidate Implementation Specification v1

## SECTION 1 - Executive Summary

This note freezes the implementation specification for the approved OHLCV Non-Hostile Transition and Leadership Rotation candidate concepts. It is specification-only. No formulas were defined, no code was implemented, no candidate panels were generated, no discovery was executed, no IC was calculated, no redundancy screening was run, no refinement was run, no validation was run, no governance was modified, no thresholds were changed, nothing was registered to production, and no ML was implemented.

Approved concept inventory:

- The concept-generation phase created 10 exploratory concepts.
- `nhlr_06` was removed as a standalone candidate due conceptual overlap with quiet accumulation and volume-confirmed leadership-shift concepts.
- The approved implementation inventory contains 9 concepts: `nhlr_01`, `nhlr_02`, `nhlr_03`, `nhlr_04`, `nhlr_05`, `nhlr_07`, `nhlr_08`, `nhlr_09`, and `nhlr_10`.

Implementation objective:

- Define how the approved concepts should be represented during future implementation.
- Freeze candidate identifiers, working names, categories, responsibilities, metadata expectations, artifact expectations, independence controls, and workflow boundaries.
- Preserve conceptual independence from hostile/stress repair, persistence, rank-coherence, participation/liquidity repair, volatility compression, transition-state stress absorption, and ordinary momentum.

Implementation scope:

- Candidate registry specification.
- Candidate responsibility specification.
- Metadata and artifact expectations.
- Conceptual independence and risk-control specification.
- Future workflow only.

Expected deliverables in a later implementation task:

- candidate registry scaffold;
- candidate metadata records;
- candidate implementation manifest;
- candidate responsibility diagnostics;
- guardrail diagnostics;
- pre-panel implementation review artifact.

No candidate panels are authorized by this note.

## SECTION 2 - Approved Candidate Inventory

| identifier | working name | concept category | economic mechanism | implementation priority |
| --- | --- | --- | --- | --- |
| `nhlr_01` | Emerging Leadership From Neutral Base | orderly leadership emergence | gradual leadership emergence | High |
| `nhlr_02` | Quiet Accumulation Before Leadership | orderly leadership emergence | orderly capital migration | High |
| `nhlr_03` | Post-Transition Leadership Durability | healthy leadership persistence | participation persistence / leadership confirmation | Medium-high |
| `nhlr_04` | Smooth Trend Handoff | smooth trend handoff | trend handoff | High |
| `nhlr_05` | Broadening Participation Without Stress | gradual participation expansion | healthy participation expansion | Medium-high |
| `nhlr_07` | Rotation Acceleration Leader | rotation acceleration | rotation acceleration | High |
| `nhlr_08` | Mature Leadership Deceleration Avoidance | rotation deceleration | rotation deceleration | Medium |
| `nhlr_09` | Volume-Confirmed Leadership Shift | volume-confirmed leadership shifts | leadership confirmation | High |
| `nhlr_10` | Healthy Breadth Contributor | healthy breadth transitions | healthy participation expansion / breadth transition | High |

Removed or merged concept:

| identifier | working name | disposition | rationale |
| --- | --- | --- | --- |
| `nhlr_06` | Participation Persistence After Emergence | removed as standalone | Overlaps with `nhlr_02` and `nhlr_09`; may remain as a secondary diagnostic idea only. |

No formulas or implementation logic are defined by this inventory.

## SECTION 3 - Candidate Responsibilities

| identifier | intended research objective | expected observable behavior | relationship to healthy transitions | expected distinction from existing families |
| --- | --- | --- | --- | --- |
| `nhlr_01` | Test whether names emerging from neutral standing toward leadership contain early leadership alpha. | Orderly improvement from neutral or middling standing into stronger leadership behavior. | Represents the cleanest early-stage non-hostile leadership-emergence concept. | Must not become raw momentum or rank-coherence; should emphasize transition from neutral base. |
| `nhlr_02` | Test whether quiet accumulation before visible leadership forecasts later leadership. | Improving demand quality, restrained extension, and steadier behavior before obvious leadership. | Represents early capital migration before broad recognition. | Must not become participation repair or volume shock reversal. |
| `nhlr_03` | Test whether healthy new leadership remains durable after non-hostile transition. | Sustained leadership quality after emergence without excessive churn or disorder. | Represents post-transition confirmation and durability. | Must not become post-drawdown persistence or rank-turnover resilience. |
| `nhlr_04` | Test whether controlled trend handoff predicts future leadership. | Smooth move from consolidation or neutral trend into orderly trend participation. | Represents transition quality rather than rebound or raw strength. | Must not become simple trend-following or volatility compression. |
| `nhlr_05` | Test whether participation broadens in healthy regimes without stress-repair framing. | Rising participation in neutral or constructive conditions. | Represents broadening demand before or during healthy transition. | Must not become weak-breadth repair or participation/breadth repair under hostile conditions. |
| `nhlr_07` | Test whether early leaders during accelerating rotation outperform. | Earlier improvement during increasing leadership-migration pace. | Represents acceleration in capital migration. | Must not become momentum acceleration or transition-state stress absorption. |
| `nhlr_08` | Test whether avoiding decelerating mature leadership improves leadership quality. | Preference for leadership not showing late-stage sponsorship loss. | Represents rotation-phase quality and avoidance of tiring leadership. | Must not become short reversal, persistence, or rank-coherence duplicate. |
| `nhlr_09` | Test whether leadership shifts confirmed by orderly volume are more credible. | Leadership improvement with non-shock volume or participation confirmation. | Represents confirmation of capital migration and leadership handoff. | Must not become volume momentum, liquidity repair, or volume shock reversal. |
| `nhlr_10` | Test whether healthy breadth contribution identifies new leaders in broadening markets. | Constructive contribution to non-hostile breadth expansion. | Represents broadening leadership without weak-breadth repair. | Must not become weak-breadth repair, stress repair, or static peer/sector rotation. |

## SECTION 4 - Implementation Metadata

Required metadata fields for every future candidate record:

- `candidate_id`
- `working_name`
- `family`
- `concept_category`
- `economic_mechanism`
- `implementation_priority`
- `dependency_class`
- `required_input_family`
- `prohibited_dependencies`
- `expected_artifact_namespace`
- `diagnostic_identifier`
- `research_status`
- `implementation_status`
- `formula_status`
- `panel_status`
- `discovery_status`
- `risk_notes`

Required constants:

- `family`: `ohlcv_non_hostile_transition_leadership_rotation`
- `dependency_class`: `OHLCV_ONLY`
- `required_input_family`: `OHLCV_DERIVED_ONLY`
- `research_status`: `RESEARCH_ONLY`
- `implementation_status`: `SPECIFIED_NOT_IMPLEMENTED`
- `formula_status`: `NO_FORMULA_DEFINED`
- `panel_status`: `NO_PANEL_GENERATED`
- `discovery_status`: `DISCOVERY_NOT_EXECUTED`

Candidate metadata specification:

| candidate_id | dependency_class | required OHLCV inputs | expected artifacts | diagnostic identifiers | prohibited dependencies |
| --- | --- | --- | --- | --- | --- |
| `nhlr_01` | `OHLCV_ONLY` | price, return, rank, trend, breadth-like OHLCV aggregates | registry row, metadata JSON, implementation diagnostic row | `nhlr_01_neutral_emergence_diagnostic` | PIT metadata, sector labels, peer groups, stress-repair gates, raw momentum-only framing |
| `nhlr_02` | `OHLCV_ONLY` | price, return, volume, range, participation-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_02_quiet_accumulation_diagnostic` | PIT metadata, liquidity repair, volume shock reversal, stress recovery |
| `nhlr_03` | `OHLCV_ONLY` | price, return, rank, trend, participation-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_03_leadership_durability_diagnostic` | drawdown windows, post-drawdown persistence, rank-churn-only logic |
| `nhlr_04` | `OHLCV_ONLY` | price, return, trend, range, volatility-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_04_trend_handoff_diagnostic` | trend-following-only logic, stress absorption, volatility compression after stress |
| `nhlr_05` | `OHLCV_ONLY` | volume, participation-like OHLCV proxies, breadth-like OHLCV aggregates | registry row, metadata JSON, implementation diagnostic row | `nhlr_05_participation_expansion_diagnostic` | weak-breadth repair, hostile trend, participation repair gates |
| `nhlr_07` | `OHLCV_ONLY` | price, return, rank, trend, breadth-like OHLCV aggregates | registry row, metadata JSON, implementation diagnostic row | `nhlr_07_rotation_acceleration_diagnostic` | momentum-only acceleration, transition-state stress absorption |
| `nhlr_08` | `OHLCV_ONLY` | price, return, rank, trend, range, participation-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_08_rotation_deceleration_diagnostic` | short reversal, post-drawdown persistence, rank-coherence duplicate |
| `nhlr_09` | `OHLCV_ONLY` | price, return, volume, participation-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_09_volume_confirmation_diagnostic` | volume shock reversal, liquidity repair, volume momentum-only logic |
| `nhlr_10` | `OHLCV_ONLY` | price, return, breadth-like OHLCV aggregates, participation-like OHLCV proxies | registry row, metadata JSON, implementation diagnostic row | `nhlr_10_breadth_contribution_diagnostic` | weak-breadth repair, sector rotation claims, PIT metadata |

No computational logic is specified. Required OHLCV input families are descriptive input classes only, not formulas.

## SECTION 5 - Artifact Expectations

Expected future implementation artifacts:

Candidate manifests:

- `candidate_inventory/candidate_registry.csv`
- `candidate_inventory/candidate_metadata_manifest.csv`
- `candidate_inventory/candidate_category_balance.csv`
- `candidate_inventory/removed_or_merged_concepts.csv`

Panel metadata:

- `candidate_panels/panel_metadata_manifest.csv`
- `candidate_panels/panel_generation_status.csv`
- Panel metadata should remain `NO_PANEL_GENERATED` until panel generation is separately authorized.

Diagnostics:

- `diagnostics/candidate_metadata_completeness.csv`
- `diagnostics/candidate_responsibility_review.csv`
- `diagnostics/prohibited_dependency_review.csv`
- `diagnostics/family_overlap_risk_review.csv`
- `diagnostics/guardrail_checklist.csv`

Implementation logs:

- `implementation_review/candidate_implementation_spec_check.md`
- `implementation_review/pre_panel_generation_review.md`
- `implementation_review/no_formula_confirmation.md`

Discovery summaries:

- `discovery_summary/discovery_readiness_placeholder.json`
- `discovery_summary/candidate_inventory_summary.md`

Artifact principles:

- Candidate implementation may create registry and metadata artifacts.
- Candidate implementation may not create candidate panels unless a later task authorizes panel generation.
- Discovery summaries must remain placeholders until discovery is authorized.
- All artifacts must remain under the research artifact namespace.

## SECTION 6 - Candidate Independence Review

| candidate_id | economic distinctiveness | conceptual independence | residual overlap risk | independence conclusion |
| --- | --- | --- | --- | --- |
| `nhlr_01` | High | Medium-high | Momentum and rank-coherence overlap if framed as rank improvement only. | Keep; core anchor with momentum guardrails. |
| `nhlr_02` | High | Medium-high | Participation/liquidity overlap if framed as volume repair. | Keep; strong capital-migration concept. |
| `nhlr_03` | Medium-high | Medium | Persistence/rank-coherence overlap if framed as low churn. | Keep with explicit no-drawdown and no-rank-churn-only controls. |
| `nhlr_04` | High | Medium-high | Trend-following and volatility-adaptation overlap. | Keep with transition-quality requirement. |
| `nhlr_05` | Medium-high | Medium | Participation/breadth repair drift. | Keep with non-hostile and no-weak-breadth-repair controls. |
| `nhlr_07` | High | Medium | Momentum and transition-state overlap. | Keep with rotation-pace distinction. |
| `nhlr_08` | Medium | Medium | Persistence, rank-coherence, and reversal overlap. | Keep as lower-priority rotation-phase quality concept. |
| `nhlr_09` | High | Medium | Participation/liquidity and volume-momentum overlap. | Keep with confirmation-not-volume-shock framing. |
| `nhlr_10` | High | Medium | Weak-breadth repair and transition-state overlap. | Keep with healthy breadth and non-hostile framing. |

Inventory independence conclusion:

The approved nine-candidate inventory remains economically distinct enough for implementation specification. No additional concept should be removed before implementation, but `nhlr_08` should retain lower priority and `nhlr_05`/`nhlr_10` require explicit stress-repair drift controls.

## SECTION 7 - Risk Controls

Implementation drift:

- Risk: implementation may define formulas that do not match the concept responsibilities.
- Mitigation: require candidate responsibility review before panel generation and record `mechanism_thesis` for each candidate.

Hidden momentum overlap:

- Risk: `nhlr_01`, `nhlr_04`, and `nhlr_07` may become simple momentum or trend continuation.
- Mitigation: require metadata fields documenting expected distinction from raw momentum; later redundancy review must include momentum-like references where available.

Hidden persistence overlap:

- Risk: `nhlr_03` and `nhlr_08` may become post-drawdown persistence or rank-stability duplicates.
- Mitigation: prohibit drawdown windows, post-drawdown gating, and rank-churn-only logic as primary mechanism.

Hidden stress-repair overlap:

- Risk: `nhlr_05`, `nhlr_09`, and `nhlr_10` may drift into participation repair, liquidity repair, weak-breadth repair, or stress recovery.
- Mitigation: prohibit hostile, panic, weak-breadth repair, liquidity repair, and stress-recovery gates as primary activation logic.

Candidate duplication:

- Risk: quiet accumulation, participation expansion, and volume confirmation can converge if implemented too similarly.
- Mitigation: candidate metadata must identify dominant mechanism and expected distinction; pre-panel review should merge or hold back duplicates.

PIT leakage:

- Risk: leadership rotation language may invite sector or peer-relative interpretation.
- Mitigation: require `dependency_class = OHLCV_ONLY`; prohibit sector, industry, peer, and PIT metadata dependencies.

## SECTION 8 - Future Implementation Workflow

The intended workflow is frozen as follows:

1. Candidate implementation

- Implement the candidate registry and metadata records for the nine approved concepts.
- Define candidate responsibilities and placeholders.
- Do not define formulas unless a later implementation task explicitly permits formula-level work.

2. Panel generation

- Generate panels only after candidate implementation review approves registry completeness and formula boundaries.
- Panel generation is not authorized by this note.

3. Redundancy screening

- Run conceptual, metadata, and statistical redundancy screening only after panels exist and the phase is authorized.
- Compare against hostile/stress repair, persistence, rank-coherence, participation/liquidity, volatility adaptation, transition-state, and momentum-like references.

4. IC discovery

- Score approved representative panels only after redundancy review.
- Discovery execution is not authorized by this note.

5. Refinement eligibility review

- Review evidence, coverage, state attribution, and redundancy before any refinement.
- No automatic advancement.

6. Constrained refinement

- Refine only predeclared survivors if a separate review approves.
- Keep variants small and avoid post-discovery mining.

7. Validation

- Validation requires a separate design package after refinement.
- No validation or production action follows automatically from discovery or refinement.

## SECTION 9 - Readiness Assessment

Is the approved inventory ready for implementation?

Yes, for candidate registry and metadata implementation only. The nine approved concepts have stable identifiers, working names, categories, mechanisms, responsibilities, priority labels, prohibited dependencies, and artifact expectations.

Remaining blockers:

- Formula definitions remain blocked.
- Candidate panel generation remains blocked.
- Discovery execution remains blocked.
- IC calculation remains blocked.
- Redundancy screening remains blocked until panels exist and the phase is authorized.
- Refinement remains blocked.
- Validation remains blocked.
- Governance mutation, production registration, and ML remain blocked.

No additional concepts are required before candidate implementation. The inventory should remain at nine concepts unless a later review identifies a coverage gap after candidate registry implementation.

## SECTION 10 - Final Recommendation

1. Is the candidate inventory implementation-ready?

Yes, for registry and metadata implementation. The nine-concept inventory is specific enough to implement candidate records and placeholder metadata without formulas or panels.

2. Are the implementation boundaries sufficiently clear?

Yes. This specification defines required metadata, dependency classes, prohibited dependencies, expected artifacts, candidate responsibilities, workflow order, and blocked activities.

3. Are additional concepts needed?

No. The approved nine concepts provide sufficient category and mechanism coverage. Adding concepts now would increase redundancy and weaken the discipline of the first implementation pass.

4. Is the project ready to begin candidate implementation?

Yes, for scaffold/registry implementation only. The next implementation task should create candidate registry records, metadata manifests, diagnostics placeholders, and guardrail checks. It should not define formulas, generate panels, execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, register production artifacts, or implement ML.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Candidate Registry Implementation v1**. It should implement the nine approved concept records in the existing scaffold, create candidate metadata and manifest artifacts, add registry validation tests, and preserve fail-closed restrictions. It should not define formulas, generate candidate panels, execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, register production artifacts, or implement ML.

## Specification Caveat

This document is specification-only. It does not define mathematical formulas, implement code, generate panels, execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, register production candidates, or implement ML.
