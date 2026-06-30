# Project Underdog - Peer-Relative Repair and Stabilization Asymmetry Discovery Program Design v1

## SECTION 1 - Design Objective

This note defines a design-only research program for **Peer-Relative Repair and Stabilization Asymmetry Discovery v1**.

The objective is to specify the next alpha-family frontier after the OHLCV Non-Hostile Transition and Leadership Rotation family was parked as `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`. The proposed frontier asks whether repair, stabilization, liquidity recovery, volatility normalization, persistence, dispersion, and leadership recovery contain stronger information when measured relative to economically comparable peers rather than only against the full equity universe.

Readiness classification: `DESIGN_READY_WITH_METADATA_DEPENDENCIES`.

Interpretation:

- The design is ready to become a formal specification.
- Candidate implementation, panel generation, IC discovery, refinement, validation, governance changes, production registration, threshold changes, and ML remain blocked.
- The main blocker is not concept quality. It is point-in-time economic metadata, including sector, industry, peer-group, size, market-cap, and ticker/security lineage.

## SECTION 2 - Materials Reviewed

Reviewed state and inventory notes:

- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_family_inventory_and_diversification_review_v1.md`
- `docs/research_notes/main_alpha_inventory_consolidation_and_non_crsp_frontier_selection_v1.md`

Reviewed economic-context and metadata notes:

- `docs/research_notes/economic_context_enrichment_design_v1.md`
- `docs/research_notes/economic_context_enrichment_v1_implementation.md`
- `docs/research_notes/metadata_readiness_review_v1.md`
- `docs/research_notes/peer_relative_and_economic_context_discovery_readiness_review_v1.md`
- `docs/research_notes/point_in_time_economic_context_readiness_audit_v1.md`

Reviewed negative-result note:

- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`

No research execution was performed for this design.

## SECTION 3 - Prior Evidence Motivating the Pivot

The project has three broad lessons that motivate this frontier.

First, the strongest established evidence remains hostile/stress repair. Candidates such as `participation_breadth_repair_under_hostile_trend`, `participation_liquidity_state_shift_20_60`, and `volatility_compression_after_stress_stabilization` show that repair and stabilization behavior can matter, but the inventory is concentrated in stress, weak-breadth, drawdown, and h20 stabilization states.

Second, persistence and rank-coherence provide conditional candidate-lineage diversification, but not broad family proof. Both remain candidate-level threads and still require careful contamination review against hostile/stress repair and rank-structure redundancy.

Third, the OHLCV-only Non-Hostile Transition and Leadership Rotation cycle failed broadly. All nine approved candidates were classified `REJECT`; the least weak candidate was `nhlr_05` with h10 mean IC -0.000173, and family-level mean IC weakened from h1 to h20. That negative result suggests broad OHLCV-only leadership and non-hostile transition transforms are not enough as currently designed.

Strategic implication:

The next frontier should not be another broad OHLCV-only transformation family. It should test whether repair and stabilization behavior is idiosyncratic relative to economically comparable names.

## SECTION 4 - Research Motivation

Universe-relative signals can confuse three effects:

- a stock repairing after stress;
- an entire sector or industry repairing after a common shock;
- a stock merely moving with broad market, sector, or size effects.

Peer-relative repair and stabilization asymmetry tries to separate those effects. The central question is:

Does a security that repairs, stabilizes, or persists better than its true peers have forward-return information that is not captured by hostile/stress repair, persistence, rank-coherence, or broad OHLCV leadership behavior?

This frontier is attractive because it can preserve what Project Underdog has learned about repair and stabilization while changing the information domain from broad cross-sectional state behavior to economic-cohort-relative behavior.

## SECTION 5 - Metadata and PIT Readiness Assessment

Current metadata state:

- The economic-context substrate is diagnostically strong.
- Static coverage is complete in enrichment artifacts: `488 / 488` stock-universe tickers covered.
- Peer-quality diagnostics exist, including high-confidence industry peers and fallback peer assignments.
- Current implementation status remains `ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY`.

Current blockers:

- Static sector, industry, peer, and size labels cannot be used for historical alpha discovery.
- Peer-relative transforms are explicitly blocked.
- Alpha validation using sector, industry, size, or peer groups is explicitly blocked.
- Security-master lineage, ticker changes, corporate actions, mergers, spin-offs, delistings, historical market-cap, and historical classification changes are not approved for discovery use.

Minimum readiness requirement before implementation:

The project must be able to answer, for every signal date and ticker:

What sector, industry, size bucket, market-cap context, and peer group would have been known and usable on that date without look-ahead?

Until that answer is auditable, this program remains design/specification only.

## SECTION 6 - PIT Metadata Requirements

Required classification fields:

- `ticker`
- stable security identifier, if available
- `company_name`
- `sector`
- `industry`
- `subindustry`, if available
- `peer_group_label`
- `peer_group_level`
- `classification_system`
- `source`
- `source_version`
- `source_record_id`, if available
- `as_of_date`
- `effective_start`
- `effective_end`
- `collection_timestamp`
- `universe_version`
- `metadata_version`
- `record_hash`
- `point_in_time_quality`

Required size and liquidity context:

- historical `market_cap`
- `market_cap_bucket`
- `size_bucket`
- market-cap source and source version
- market-cap `as_of_date`
- date-derived liquidity bucket using only pre-signal history
- date-derived volatility bucket using only pre-signal history
- date-derived turnover bucket using only pre-signal history

Required lineage controls:

- ticker-change mapping
- security identifier continuity
- corporate-action handling
- merger, spin-off, and delisting handling
- stale-record flags
- missing-history flags
- effective-date join policy
- source hash and version audit

## SECTION 7 - Peer Hierarchy Design

Peer hierarchy should be date-aware and fail closed.

Preferred hierarchy:

1. Subindustry peer group, if available and sufficiently populated.
2. Industry peer group, if active group size meets the minimum threshold.
3. Industry x size bucket, if industry alone is too broad or too size-skewed.
4. Sector x size bucket, only as a medium-confidence fallback.
5. Sector peer group, only for broad diagnostic context.
6. Blocked, if no peer group meets minimum quality and group-size rules.

Minimum peer-group rules:

- Minimum active peer count should be specified before implementation; prior diagnostics use 8 as a useful threshold.
- The peer count must be measured as of the signal date, not from current membership.
- A candidate panel row should carry peer-group level, peer count, fallback distance, and peer-quality status.
- Candidates should be able to fail closed by date/ticker if peer assignment is stale, missing, or below threshold.

Peer-quality labels:

- `HIGH_CONFIDENCE_SUBINDUSTRY_PEER`
- `HIGH_CONFIDENCE_INDUSTRY_PEER`
- `MEDIUM_CONFIDENCE_INDUSTRY_SIZE_PEER`
- `MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER`
- `LOW_CONFIDENCE_SECTOR_PEER`
- `BLOCKED_INSUFFICIENT_PEER_CONTEXT`

## SECTION 8 - Economic-Context Conditioning Options

Allowed for design:

- sector-relative diagnostic framing;
- industry-relative diagnostic framing;
- peer-group-relative candidate concepts;
- size-aware peer fallback design;
- liquidity and volatility bucket controls if date-derived from pre-signal data;
- universe-relative baseline comparisons;
- existing-candidate contamination controls.

Blocked until PIT readiness:

- peer-relative candidate implementation;
- sector-relative alpha candidates;
- industry-relative z-scores;
- peer-neutral residualization;
- sector-conditioned IC claims;
- validation decisions based on peer or sector slices;
- governance or production use of context features;
- ML conditioning on economic metadata.

Recommended initial conditioning:

Use peer-relative measures as primary candidate features only after PIT metadata is approved. Use universe-relative versions as mandatory baselines in discovery review to prove the peer-relative transform adds information rather than simply renaming an existing OHLCV signal.

## SECTION 9 - Hypothesis Family

The program should test six mechanism families:

1. Peer-relative repair strength
   - A stock repairing faster than peers after stress may contain idiosyncratic recovery information.

2. Industry-relative liquidity stabilization
   - Liquidity or participation stabilization may matter more when it is unusual inside an industry cohort.

3. Sector-relative volatility normalization
   - Volatility compression may be informative only when a stock stabilizes more cleanly than its sector context.

4. Peer-group rank persistence after drawdown
   - Persistence may be stronger when a stock maintains rank inside its peer group after drawdown.

5. Cross-peer dispersion compression or re-expansion
   - Economic cohorts may reveal useful dispersion transitions that are weak at the broad-universe level.

6. Economically conditioned leadership recovery
   - Leadership recovery may be meaningful when a stock regains leadership relative to true peers rather than through broad OHLCV leadership.

## SECTION 10 - Candidate Concept Matrix

| concept_id | working name | mechanism | peer context | intended horizon | expected distinction | implementation status |
| --- | --- | --- | --- | --- | --- | --- |
| `prrsa_01` | peer-relative post-stress repair | Measures whether post-stress price/participation repair is stronger than active peers after a shared stress episode. | industry or industry x size | h10/h20 | Separates idiosyncratic repair from sector-wide rebound. | design only |
| `prrsa_02` | industry-relative liquidity stabilization | Tests liquidity or volume participation stabilization relative to industry peers. | industry | h10/h20 | Extends liquidity repair beyond universe-relative participation signals. | design only |
| `prrsa_03` | sector-relative volatility normalization | Tests whether realized volatility normalizes faster than sector peers without relying only on broad stress gates. | sector x size or industry | h5/h10/h20 | Distinguishes idiosyncratic stabilization from market-wide volatility compression. | design only |
| `prrsa_04` | peer-group rank persistence after drawdown | Measures persistence of rank inside a peer group after drawdown or adverse peer-relative move. | industry or subindustry | h10/h20 | Tests whether persistence survives economic-cohort normalization. | design only |
| `prrsa_05` | cross-peer dispersion compression and re-expansion | Tests whether a stock benefits when its peer group dispersion compresses or re-expands and the stock has favorable relative position. | industry and sector x size fallback | h5/h10/h20 | Re-enters dispersion through economic cohorts rather than broad cross-sectional dispersion. | design only |
| `prrsa_06` | economically conditioned leadership recovery | Tests leadership recovery inside peer cohorts after controlled underperformance or stabilization. | industry or high-confidence peer group | h10/h20 | Redesigns leadership recovery away from failed broad OHLCV non-hostile rotation. | design only |
| `prrsa_07` | peer-relative downside containment asymmetry | Tests whether stocks with less downside participation than peers during adverse windows outperform later. | industry x size | h5/h10 | Links stabilization asymmetry to peer-relative resilience, not absolute repair. | design only |
| `prrsa_08` | peer-relative nonprice participation repair | Tests whether nonprice participation improves relative to peers without price extension. | industry or sector x size | h10/h20 | Attempts to rescue nonprice liquidity repair using economic comparison. | design only |

Initial batch recommendation:

The first specification should select 4 to 6 concepts from this matrix, prioritizing `prrsa_01` through `prrsa_06`. `prrsa_07` and `prrsa_08` should remain optional alternates unless the implementation scope is still small and predeclared.

## SECTION 11 - Candidate Inclusion and Exclusion Criteria

Inclusion criteria:

- Mechanism must be economic-cohort-relative, not only universe-relative.
- Candidate must specify peer hierarchy level and fallback policy.
- Candidate must include a universe-relative baseline for comparison.
- Candidate must use only metadata available as of signal date.
- Candidate must define missing-peer and thin-peer fail-closed behavior.
- Candidate must preserve h1/h5/h10/h20 discovery visibility while declaring primary horizons up front.
- Candidate must include contamination references to hostile/stress repair, persistence, rank-coherence, and OHLCV non-hostile transition.

Exclusion criteria:

- No candidate may use static snapshot metadata for historical scoring.
- No candidate may silently backfill current sector, industry, peer, or size labels.
- No candidate may be a simple parameter variant of `participation_breadth_repair_under_hostile_trend`, `participation_liquidity_state_shift_20_60`, or `volatility_compression_after_stress_stabilization`.
- No candidate may reuse the rejected `nhlr_*` formulas as tuning seeds.
- No candidate may optimize thresholds during first-pass discovery.
- No candidate may use recovery-quality targets as validation labels.

## SECTION 12 - Anti-Overlap Strategy

Required contamination references:

- hostile/stress repair anchors;
- participation/breadth repair candidates;
- liquidity repair candidates;
- volatility compression/stabilization candidate;
- persistence validation candidates;
- rank-coherence validation candidates;
- parked OHLCV non-hostile transition panels;
- broad universe-relative versions of each peer-relative candidate.

Required anti-redundancy checks for future execution:

- signal correlation versus existing candidate panels;
- co-activation overlap with hostile/stress repair candidates;
- peer-relative value-added versus universe-relative baseline;
- sector and industry concentration diagnostics;
- horizon concentration diagnostics;
- one-window dominance diagnostics;
- active coverage and peer-coverage diagnostics;
- fallback-level sensitivity diagnostics.

Interpretation rule:

A peer-relative candidate should not advance if its evidence disappears after comparing it to the universe-relative baseline or if its behavior is mostly explained by existing hostile/stress repair candidates.

## SECTION 13 - Panel-Generation Requirements

Future candidate panels should contain one row per `date`, `ticker`, and `candidate_id`.

Required identity columns:

- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `primary_horizon`
- `candidate_family`
- `candidate_role`

Required peer-context columns:

- `sector`
- `industry`
- `subindustry`, if available
- `peer_group_label`
- `peer_group_level`
- `peer_group_size`
- `peer_group_min_size`
- `peer_quality_status`
- `fallback_distance`
- `metadata_version`
- `metadata_as_of_date`
- `metadata_effective_start`
- `metadata_effective_end`
- `point_in_time_quality`

Required diagnostic columns:

- `universe_relative_baseline_value`
- `peer_relative_component`
- `raw_repair_component`
- `stabilization_component`
- `liquidity_component`, when applicable
- `volatility_component`, when applicable
- `rank_persistence_component`, when applicable
- `missing_data_flag`
- `thin_peer_group_flag`
- `stale_metadata_flag`
- `blocked_peer_context_flag`

Fail-closed panel behavior:

- Rows with blocked peer context should not receive usable peer-relative signal values.
- Missing metadata should produce explicit flags rather than silent imputation.
- Peer counts should be computed as of the signal date.
- Warmup windows should be based only on pre-signal OHLCV history.

## SECTION 14 - IC Discovery Requirements

Future IC discovery should evaluate:

- h1;
- h5;
- h10;
- h20.

Required outputs:

- daily IC by candidate and horizon;
- candidate IC summary;
- horizon summary;
- peer-context coverage summary;
- family summary;
- candidate rankings;
- rolling IC diagnostics;
- universe-relative baseline comparison;
- peer-quality sensitivity report;
- fallback-distance sensitivity report;
- sector and industry concentration report.

Primary interpretation should focus on h10/h20 unless a candidate is explicitly declared as short-horizon. h1/h5 should be used to diagnose information decay, sign inversion, and microstructure-like behavior.

## SECTION 15 - Validation Guardrails

No validation should occur during discovery. A candidate can become validation-review eligible only after:

- PIT metadata readiness is proven;
- panel integrity passes;
- peer-context coverage is adequate;
- h10/h20 evidence is positive and not one-window dominated;
- peer-relative evidence exceeds the universe-relative baseline;
- contamination against existing repair/stabilization candidates is acceptable;
- static metadata is not used in the scoring path;
- candidate identity and formulas are frozen.

Validation review must remain separate from validation execution.

## SECTION 16 - Governance Checkpoints

Required gates:

1. Metadata source and lineage gate
   - Confirms PIT sector, industry, peer, size, and security lineage.

2. Candidate specification gate
   - Freezes concept IDs, mechanisms, formulas, primary horizons, peer hierarchy, and fail-closed rules.

3. Implementation readiness gate
   - Confirms implementation can consume PIT metadata without duplicating metadata definitions.

4. Panel-generation readiness gate
   - Confirms schemas, row keys, warmup rules, missing-data rules, peer coverage, and artifact paths.

5. IC discovery readiness gate
   - Confirms approved panels and no validation/governance side effects.

6. Post-discovery review gate
   - Classifies candidates as `ADVANCE_TO_REFINEMENT`, `WATCH`, or `REJECT` without promoting anything.

Blocked governance actions:

- production registration;
- threshold changes;
- candidate promotion or demotion in production registry;
- ML introduction;
- portfolio routing;
- validation execution without separate approval.

## SECTION 17 - Artifact Plan

Design and specification artifacts:

- `docs/research_notes/peer_relative_repair_stabilization_asymmetry_discovery_program_design_v1.md`
- future candidate specification note;
- future metadata readiness gate note;
- future implementation readiness review.

Future research artifacts, if execution is later approved:

- `artifacts/research/peer_relative_repair_stabilization_asymmetry_discovery_v1/candidate_registry/`
- `artifacts/research/peer_relative_repair_stabilization_asymmetry_discovery_v1/candidate_panels/`
- `artifacts/research/peer_relative_repair_stabilization_asymmetry_discovery_v1/panel_generation/`
- `artifacts/research/peer_relative_repair_stabilization_asymmetry_discovery_v1/ic_discovery/`
- `artifacts/research/peer_relative_repair_stabilization_asymmetry_discovery_v1/redundancy_diagnostics/`

This note does not create those artifact directories.

## SECTION 18 - Staged Execution Roadmap

Stage 1: Metadata dependency closure.

- Identify acceptable PIT sources for sector, industry, subindustry, market-cap, size, security-master lineage, and ticker history.
- Define source lineage and record-hash requirements.
- Produce a metadata source/readiness gate.

Stage 2: Candidate specification.

- Select 4 to 6 candidate concepts from the matrix.
- Freeze concept IDs, formulas, horizons, peer hierarchy, fallback rules, and fail-closed behavior.
- Specify universe-relative baselines and contamination references.

Stage 3: Implementation-only phase.

- Implement formulas after specification approval.
- Preserve registry-derived metadata.
- Do not generate panels or compute IC.

Stage 4: Panel-generation readiness review.

- Review schema, PIT joins, peer-context coverage, and metadata failure modes.
- Approve or block panel writing.

Stage 5: Panel generation.

- Serialize candidate panels only after readiness approval.
- Produce manifests, schema reports, and peer-coverage artifacts.

Stage 6: IC discovery.

- Run first-pass IC discovery across h1/h5/h10/h20.
- Compare peer-relative evidence against universe-relative baselines and existing candidate references.

Stage 7: Negative/positive result review.

- Classify each candidate.
- Decide whether the family is a true diversification path, a diagnostic-only context layer, or a parked frontier.

## SECTION 19 - Risks and Assumptions

Major risks:

- static metadata leakage;
- survivorship and ticker-lineage gaps;
- false diversification from peer transforms;
- overfitting through too many context dimensions;
- fallback groups that are too broad to be economically meaningful;
- hidden overlap with existing hostile/stress-repair candidates;
- h20 concentration that repeats current inventory risks;
- insufficient peer coverage after date-level PIT filters.

Assumptions:

- Raw h10/h20 forward-return IC remains the validation anchor.
- Recovery-quality targets remain diagnostic only.
- Static snapshot metadata remains blocked for alpha execution.
- Peer-relative discovery is worth designing because it is the most credible path to a new information domain.
- Current OHLCV non-hostile transition formulas are archived negative evidence, not refinement seeds.

## SECTION 20 - Explicit Non-Goals

This design does not:

- implement candidate formulas;
- generate candidate panels;
- run IC discovery;
- run redundancy screening;
- run refinement;
- run validation;
- modify production registry;
- modify governance;
- change thresholds;
- introduce ML;
- create executable research code;
- reopen CRSP/PIT work without separate source-readiness approval;
- change the status of existing candidates;
- use static metadata for alpha claims.

## SECTION 21 - Readiness Classification

Classification: `DESIGN_READY_WITH_METADATA_DEPENDENCIES`.

Rationale:

- The research motivation is strong and aligned with the project's largest diversification gap.
- The candidate design space is clear enough for a formal specification.
- The economic-context substrate is mature enough for design, diagnostics, and artifact planning.
- The program is not execution-ready because populated metadata remains static-snapshot and peer-relative transforms remain blocked.

Required next step:

Create **Project Underdog - Peer-Relative Repair and Stabilization Asymmetry Candidate Specification v1** only after a metadata dependency gate confirms whether PIT sector, industry, peer, size, market-cap, and security-lineage requirements can be satisfied. If the metadata gate remains unresolved, the next task should instead be **Point-in-Time Economic Metadata Source and Lineage Design v1**.
