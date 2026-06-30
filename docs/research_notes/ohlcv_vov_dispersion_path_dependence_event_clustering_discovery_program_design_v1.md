# Project Underdog - OHLCV Volatility-of-Volatility, Dispersion Path-Dependence, and Event-Clustering Discovery Program Design v1

## SECTION 1 - Executive Summary

This note designs the next executable OHLCV-only alpha research program selected by `alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`.

Program:

**OHLCV Volatility-of-Volatility, Dispersion Path-Dependence, and Event-Clustering Discovery Program v1**.

Classification: `DESIGN_READY_WITH_RESEARCH_RISKS`.

This is a design task only. No formulas were implemented, no panels were generated, no IC was computed, no candidates were generated in code, no validation was performed, no governance was modified, no production registry was modified, no thresholds were changed, and no ML was introduced.

The program is organized into three coordinated mechanism groups:

- Family A: Volatility-of-Volatility.
- Family B: Dispersion Path-Dependence.
- Family C: Event Clustering.

The intended discovery pass should be small, predeclared, and mechanism-led. The core goal is to determine whether instability path shape contains alpha beyond the established hostile/stress-repair family, persistence/rank-stability lineages, rank-coherence, simple dispersion acceleration, volume-shock reversal, and the parked non-hostile leadership-rotation family.

## SECTION 2 - Design Context

Inputs reviewed:

- `docs/research_notes/alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_family_inventory_and_diversification_review_v1.md`
- `docs/research_notes/main_alpha_inventory_consolidation_and_non_crsp_frontier_selection_v1.md`
- `docs/research_notes/participation_breadth_repair_conditional_validation.md`
- `docs/research_notes/volatility_compression_stress_stabilization_refinement.md`
- `docs/research_notes/volatility_participation_asymmetry_20_refinement_closeout.md`
- `docs/research_notes/volume_shock_reversal_isolated_production_candidate_revalidation.md`
- `docs/research_notes/alpha_family_diversification_refinement_execution_v1.md`
- `docs/research_notes/persistence_validation_execution_v1.md`
- `docs/research_notes/rank_coherence_validation_execution_v1.md`
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`

Current research boundaries:

- Hostile/stress repair remains the strongest established umbrella.
- Participation/breadth/liquidity repair is saturated enough that more variants are likely redundant.
- Volatility compression/stress stabilization is useful but repair-adjacent.
- Persistence and rank-coherence are conditional candidate-lineages, not broad validated families.
- Dispersion is structurally distinct but empirically weak and h20-decaying in the prior formulation.
- OHLCV non-hostile transition/leadership rotation is parked after broad negative h10/h20 evidence.
- PIT peer-relative/economic-context alpha is blocked pending external license evidence.

Design implication:

The next program should not ask whether volatility or dispersion is simply high, low, or repairing after stress. It should ask whether the *path* of instability, dispersion, and event arrival creates cross-sectional information.

## SECTION 3 - Program Thesis

Primary thesis:

Cross-sectional alpha may arise from the recent path of instability: volatility becoming unstable or calming, dispersion normalizing or relapsing, and price/volume/range events arriving as isolated shocks or clusters. These mechanisms may reveal crowding, fragility, forced adjustment, early stabilization, or delayed repricing that simple level-based volatility, dispersion, or leadership signals miss.

What is new:

- Volatility-of-volatility focuses on instability of volatility, not volatility level.
- Dispersion path-dependence focuses on state sequence, not one-period dispersion acceleration.
- Event clustering focuses on shock arrival topology, not a single volume shock, gap, or reversal event.

What must remain out of scope:

- Broad stress-repair gating.
- Static sector, industry, peer, or metadata conditioning.
- Direction-inversion rescue of the parked OHLCV leadership family.
- More participation/breadth repair variants.
- ML-driven feature search.

## SECTION 4 - Family A: Volatility-of-Volatility

### Research Motivation

Prior volatility work has mostly focused on compression, stabilization, and stress states. Volatility-of-volatility asks whether unstable realized volatility dynamics themselves identify names whose future returns differ from names with similar volatility levels but smoother volatility paths.

### Economic Intuition

When volatility changes erratically, investors may be uncertain about risk, liquidity providers may widen participation asymmetrically, and crowded positions may de-risk unevenly. Conversely, declining volatility-of-volatility after instability may indicate stabilizing risk perception before price leadership is obvious.

### Candidate Design Space

Use OHLCV-derived primitives only:

- realized volatility level;
- change in realized volatility;
- volatility-of-volatility over short and medium windows;
- range instability;
- gap/range instability;
- volatility path slope and curvature;
- low-extension controls;
- optional rebalance/low-churn controls.

The family should avoid direct hostile/drawdown activation as a primary input. Stress states may be used only as diagnostics or exclusions.

### Expected Orthogonality

Expected orthogonality is medium-high versus participation repair and volume shock reversal, medium versus volatility compression, and medium versus rank-coherence. The family may be most distinct when it compares securities with similar volatility levels but different volatility instability paths.

### Overlap Risks

- Can collapse into volatility compression/stress stabilization.
- Can become a panic/liquidity stress proxy.
- Can become a short-horizon reversal signal after volatility spikes.
- Can overlap rank-coherence if low volatility-of-volatility simply rewards stable ranks.

### State Dependence

Allowed primary states:

- volatility instability rising;
- volatility instability calming;
- range instability rising;
- low-extension instability;
- post-instability stabilization without explicit hostile repair.

Blocked primary states:

- panic/liquidity stress only;
- drawdown acceleration only;
- weak breadth only;
- explicit recovery phase only.

### Horizons of Interest

Primary horizons: h5, h10, h20.

Interpretation:

- h5 is useful for instability repricing.
- h10 is the preferred primary horizon for volatility-of-volatility.
- h20 is useful only if the effect is not a delayed stress-repair proxy.

### Expected Failure Modes

- h1-only behavior with no medium-horizon persistence.
- strong h20 only during panic/drawdown windows.
- high overlap with volatility compression after stress.
- excessive turnover from noisy volatility instability.
- sparse activation after anti-stress exclusions.

### Mechanism-Led Candidate Concepts

| concept_id | concept name | mechanism | intended distinction |
| --- | --- | --- | --- |
| `vov_01_instability_calm_after_chop` | Volatility instability calming after choppy risk | Names whose volatility-of-volatility falls after elevated range instability, without requiring drawdown repair. | Tests whether risk uncertainty resolution predicts h10/h20 returns. |
| `vov_02_low_extension_vov_rise` | Low-extension volatility-of-volatility rise | Names with rising volatility instability but limited price extension. | Tests early instability repricing without mature momentum or reversal dominance. |
| `vov_03_range_chop_exhaustion` | Range-chop exhaustion | Names with repeated high-low range instability that begins to compress. | Distinguishes intraday range disorder from close-to-close volatility compression. |
| `vov_04_vov_slope_divergence` | Volatility level versus volatility-instability divergence | Names where volatility level and volatility-of-volatility move in opposite directions. | Tests whether instability path adds information beyond vol level. |
| `vov_05_churn_controlled_vov_stabilization` | Low-churn volatility-instability stabilization | Stabilizing volatility-of-volatility with rank-churn or rebalance discipline. | Tests whether VOV signal quality improves when noisy churn is controlled. |

## SECTION 5 - Family B: Dispersion Path-Dependence

### Research Motivation

Prior dispersion work was distinct but weak, especially at h20. The next design should not repeat simple dispersion acceleration. It should test whether sequences of dispersion elevation, normalization, relapse, or stabilization carry information.

### Economic Intuition

Cross-sectional dispersion is not only a market state; it is a path. A market moving from high dispersion to orderly normalization may reward different names than a market that repeatedly relapses into dispersion. Names resilient through dispersion paths may differ from names that only look strong during one static dispersion state.

### Candidate Design Space

Use OHLCV-derived cross-sectional primitives:

- cross-sectional return dispersion;
- dispersion change and acceleration;
- dispersion persistence;
- dispersion relapse after normalization;
- dispersion stabilization after elevation;
- range/volatility dispersion spread;
- rank behavior inside dispersion states;
- low-extension and low-churn controls.

### Expected Orthogonality

Expected orthogonality is high versus participation/breadth repair and medium-high versus volume shock reversal. It has moderate overlap risk with rank-coherence because both may reward stable cross-sectional structure.

### Overlap Risks

- Can recreate rank-coherence if it rewards stable rank paths.
- Can recreate persistence if it rewards names that simply remain strong after drawdown.
- Can repeat the prior weak dispersion acceleration family.
- Can become stress repair if high-dispersion periods are mostly panic/drawdown windows.

### State Dependence

Allowed primary states:

- dispersion elevated then stabilizing;
- dispersion normalizing without broad stress gate;
- dispersion relapse after temporary calm;
- dispersion path divergence from volatility path;
- low-extension behavior within dispersion path transitions.

Blocked primary states:

- simple rising dispersion only;
- high-dispersion panic only;
- broad hostile trend gate;
- pure rank-coherence without dispersion-path conditioning.

### Horizons of Interest

Primary horizons: h5 and h10.

Secondary horizon: h20 only as durability evidence.

Interpretation:

Prior dispersion evidence decayed at h20, so h20 should not be the sole success anchor. A clean h5/h10 dispersion-path effect with low stress-repair contamination may be useful even if h20 is modest.

### Expected Failure Modes

- repeats prior h20 decay;
- positive h10 but fragile window concentration;
- high sibling correlation among concepts;
- direct overlap with rank-coherence candidate;
- hidden stress-state dependence.

### Mechanism-Led Candidate Concepts

| concept_id | concept name | mechanism | intended distinction |
| --- | --- | --- | --- |
| `dpath_01_elevated_dispersion_stabilizing` | Elevated dispersion stabilizing | Names with constructive behavior as dispersion remains elevated but becomes less chaotic. | Moves beyond simple dispersion acceleration. |
| `dpath_02_dispersion_relapse_resilience` | Dispersion relapse resilience | Names that avoid rank/return degradation when dispersion relapses after a calming period. | Tests path resilience rather than static rank stability. |
| `dpath_03_normalization_without_leadership_crowding` | Dispersion normalization without crowding | Names improving during dispersion normalization but with low extension and low crowding proxies. | Learns from parked leadership rotation failure. |
| `dpath_04_vol_dispersion_path_divergence` | Volatility-dispersion path divergence | Names favored when realized volatility path and cross-sectional dispersion path diverge. | Tests whether dispersion adds information beyond volatility states. |
| `dpath_05_low_churn_dispersion_transition` | Low-churn dispersion transition | Dispersion transition signal with rebalance or rank-churn discipline. | Controls noisy timing while avoiding pure rank-coherence. |
| `dpath_06_dispersion_after_event_absorption` | Dispersion after event absorption | Names stabilizing after market-level event clusters while dispersion remains elevated. | Bridge concept with Family C, but still dispersion-path led. |

## SECTION 6 - Family C: Event Clustering

### Research Motivation

Earlier event-quality and gap-followthrough concepts were weak, while volume shock reversal remains a controlled reference with high reversal overlap. Event clustering asks a different question: whether the topology of recent events, isolated versus clustered shocks, matters for future cross-sectional returns.

### Economic Intuition

One shock can be noise. Repeated shocks can indicate forced flows, information arrival, liquidity withdrawal, position crowding, or delayed repricing. Clustered events may produce continuation, exhaustion, or stabilization depending on whether price, volume, range, and volatility shocks align or diverge.

### Candidate Design Space

Use OHLCV-derived event primitives:

- abnormal volume events;
- large range events;
- gap events;
- large close-to-close return events;
- volatility shock events;
- event count over rolling windows;
- event spacing and recency;
- cluster intensity and decay;
- event alignment versus event divergence;
- low-extension and reversal contamination controls.

### Expected Orthogonality

Expected orthogonality is medium. Event clustering can be distinct from simple volume shock reversal if it uses multi-event topology rather than one abnormal-volume reversal. It is less orthogonal if concepts are dominated by volume shock or gap reversal.

### Overlap Risks

- Can become disguised volume shock reversal.
- Can become plain reversal after large negative returns.
- Can become panic/liquidity stress repair.
- Can become too sparse if requiring several event types to cluster.
- Can inherit same-bar timing concerns from volume and close inputs.

### State Dependence

Allowed primary states:

- clustered events with low extension;
- event cluster fading;
- mixed event clusters with range/volume divergence;
- isolated event versus clustered event contrast;
- event clusters outside explicit panic/drawdown windows.

Blocked primary states:

- single volume shock reversal only;
- single gap followthrough only;
- panic/liquidity stress only;
- high-magnitude event with no cluster context.

### Horizons of Interest

Primary horizons: h5 and h10.

Secondary horizon: h20 if clusters represent slow repricing rather than immediate reversal.

Interpretation:

Event clustering likely has shorter information half-life than stress-repair candidates. h20 strength is welcome but should not be forced as the only success criterion.

### Expected Failure Modes

- sparse activation;
- one-window crisis dominance;
- high overlap with volume shock reversal;
- h1/h5 noise with no h10 support;
- accidental use of same-bar assumptions that require later timing review;
- ambiguity between continuation and reversal direction.

### Mechanism-Led Candidate Concepts

| concept_id | concept name | mechanism | intended distinction |
| --- | --- | --- | --- |
| `ecluster_01_multi_shock_absorption` | Multi-shock absorption | Names absorbing clustered volume/range/volatility shocks without extreme price extension. | Tests repeated shock absorption rather than single volume reversal. |
| `ecluster_02_cluster_decay_stabilization` | Event-cluster decay stabilization | Names stabilizing as recent event clusters decay. | Tests whether cluster exhaustion predicts h5/h10 returns. |
| `ecluster_03_isolated_vs_clustered_volume_shock` | Isolated versus clustered volume shock | Contrasts single abnormal-volume events with repeated volume/range events. | Explicitly separates from volume shock reversal. |
| `ecluster_04_gap_range_cluster_containment` | Gap-range cluster containment | Names containing repeated gap/range shocks without followthrough deterioration. | Revisits event quality through cluster containment, not one gap. |
| `ecluster_05_event_cluster_low_churn_rebalance` | Low-churn event cluster rebalance | Cluster signal with holding/rebalance discipline to reduce noisy event churn. | Tests whether cluster information survives turnover control. |
| `ecluster_06_cross_event_divergence` | Cross-event divergence | Names where volume events cluster but range/return shocks do not, or vice versa. | Tests event-type disagreement rather than event magnitude. |

## SECTION 7 - Coordinated Candidate Budget

Recommended discovery batch size:

- Family A: 5 concepts.
- Family B: 6 concepts.
- Family C: 6 concepts.
- Total concept budget: 17 maximum.

Execution recommendation:

The first executable specification may reduce this to 12 concepts if implementation cost or redundancy concerns are high. Preserve at least three concepts per family so the batch can distinguish family failure from one bad formula expression.

Concepts are not implemented candidates yet. A later specification note must translate concepts into exact formulas, parameters, and artifact names before any code work begins.

## SECTION 8 - Anti-Redundancy Controls

Required contamination references:

- `participation_liquidity_state_shift_20_60`
- `participation_breadth_repair_under_hostile_trend`
- `volatility_compression_after_stress_stabilization`
- `volume_shock_reversal_stable_20`
- `post_drawdown_persistence_churn_adjusted_20`
- `rank_coherence_churn_avoidance_02_overlap_adjusted`
- `dispersion_transition_acceleration_20`
- `dispersion_transition_acceleration_neutralized_20`
- plain reversal reference
- momentum / trend reference
- simple volatility level reference
- simple dispersion level reference

Required anti-redundancy checks in the future IC pass:

- pairwise signal correlation;
- active-period co-activation;
- top/bottom overlap if existing infrastructure supports it;
- state attribution overlap;
- maximum correlation to stress-repair, persistence, rank-coherence, volume shock reversal, and dispersion anchors;
- one-window dominance;
- horizon concentration;
- active coverage and activation transition counts.

Design constraints:

- No concept may be justified solely because it works in panic, drawdown, weak breadth, or hostile trend states.
- No concept may use PIT metadata, sector labels, peer groups, company metadata, or external licensed source fields.
- No concept may be a direct inversion of the parked OHLCV leadership formulas.
- No concept may be a single-ingredient threshold variant of an existing successful candidate.

## SECTION 9 - Candidate Inclusion Criteria

To enter a future formula specification, a concept must:

- have a clear mechanism label tied to volatility-of-volatility, dispersion path-dependence, or event clustering;
- use only OHLCV-derived inputs and existing state primitives;
- specify why it should differ from stress repair, persistence, rank-coherence, and volume shock reversal;
- identify primary horizon expectations before IC is run;
- define expected active coverage risk;
- include at least one anti-extension, anti-churn, or anti-single-event rationale where relevant;
- avoid broad parameter grids;
- be interpretable if it fails.

## SECTION 10 - Candidate Exclusion Criteria

Exclude concepts that:

- primarily reproduce hostile/stress repair;
- depend on external metadata;
- require sector, industry, peer, market-cap, fundamental, options, macro, or alternative data;
- are direct refinements of `participation_breadth_repair_under_hostile_trend`;
- are direct refinements of `volatility_compression_after_stress_stabilization`;
- are direct refinements or inversions of the parked OHLCV leadership candidates;
- only rename simple reversal, momentum, volatility level, or dispersion level;
- require many tunable thresholds before the first IC pass;
- cannot be assigned a clear primary family;
- would be uninterpretable under a negative result.

## SECTION 11 - Refinement Policy

No refinement is allowed during the first discovery execution.

After first-pass IC and diagnostics:

- `REJECT`: archive concepts with negative or flat evidence and no diagnostic value.
- `DIAGNOSTIC_ONLY`: retain concepts that clarify state behavior but lack candidate strength.
- `WATCH`: retain concepts with positive evidence but material concentration, redundancy, or horizon risk.
- `REFINEMENT_ELIGIBLE`: allow only if a concept has positive primary-horizon evidence, acceptable active coverage, interpretable state behavior, and manageable redundancy.

Permitted later refinement types:

- light smoothing;
- rebalance/holding interval controls;
- low-churn controls;
- anti-extension controls;
- bad-state exclusion if predeclared by the first-pass diagnosis;
- simplified variants that reduce, not increase, formula complexity.

Blocked refinement types:

- broad parameter search;
- adding PIT metadata;
- adding ML;
- post-hoc horizon switching as the main thesis;
- direct inversion of failed concepts without a separate inversion diagnostic design;
- combining all three families into one opaque composite.

## SECTION 12 - Governance Checkpoints

Checkpoint 1 - Design approval:

- Approve or revise this design note.
- Confirm `DESIGN_READY_WITH_RESEARCH_RISKS`.
- Confirm no implementation is authorized by this note.

Checkpoint 2 - Formula specification:

- Translate concepts into exact formulas.
- Freeze candidate ids, inputs, horizons, and artifact paths.
- Predeclare contamination references and stop conditions.

Checkpoint 3 - Implementation scaffold:

- Implement only the approved specification.
- No extra formulas.
- No dynamic candidate generation.
- No governance or production changes.

Checkpoint 4 - First-pass discovery:

- Generate panels and compute IC only after explicit execution authorization.
- Score h1/h5/h10/h20.
- Produce candidate, family, redundancy, state, and manifest artifacts.

Checkpoint 5 - Discovery result review:

- Interpret evidence.
- Classify candidates.
- Decide whether refinement eligibility exists.
- Do not refine or validate in the same review.

## SECTION 13 - IC Evaluation Plan

Future first-pass discovery should evaluate:

- horizons: h1, h5, h10, h20;
- primary horizons: h5/h10 for event clustering and dispersion path-dependence, h10 for volatility-of-volatility, h20 only as durability evidence;
- daily cross-sectional IC by candidate and horizon;
- candidate horizon summary;
- family-level horizon summary;
- WFV-style window diagnostics;
- active coverage and activation transition diagnostics;
- turnover proxy and rank-churn diagnostics;
- state attribution using existing OHLCV state labels;
- redundancy and contamination review against required references;
- one-window dominance and recent-window behavior.

Interpretation rules:

- h1-only evidence is diagnostic, not refinement-eligible.
- h20-only evidence must pass stress-repair contamination review before it is treated as promising.
- h5/h10 evidence can be meaningful for this program if it is robust and distinct.
- A family can be valuable as negative evidence if it cleanly rejects a mechanism.

## SECTION 14 - Artifact Plan

Future execution artifact root:

`artifacts/research/ohlcv_vov_dispersion_path_dependence_event_clustering_discovery_v1/`

Suggested future artifacts:

- `candidate_registry.csv`
- `candidate_formula_manifest.csv`
- `panel_manifest.csv`
- `panel_integrity_summary.csv`
- `candidate_horizon_ic_scores.csv`
- `daily_ic_by_candidate_horizon.csv`
- `family_horizon_summary.csv`
- `candidate_rankings.csv`
- `state_attribution_summary.csv`
- `redundancy_contamination_summary.csv`
- `coactivation_summary.csv`
- `turnover_churn_summary.csv`
- `window_diagnostics.csv`
- `design_guardrail_manifest.json`
- `manifest.json`

This design note does not create those artifacts.

## SECTION 15 - Staged Execution Roadmap

Stage 1 - Specification:

- Create a formula and panel specification note.
- Select final candidate count.
- Freeze concept-to-formula mapping.
- Define exact artifact paths and manifest schema.

Stage 2 - Implementation:

- Implement the approved formulas and runner.
- Include fail-closed guardrails for candidate count, horizons, and artifact paths.
- Do not include any unapproved exploratory formulas.

Stage 3 - Panel generation and integrity audit:

- Generate candidate panels only after explicit execution authorization.
- Audit missingness, finite coverage, active coverage, turnover proxy, and candidate count.

Stage 4 - First-pass IC discovery:

- Compute h1/h5/h10/h20 IC.
- Produce candidate rankings, family summaries, and redundancy/context diagnostics.

Stage 5 - Negative-result or refinement-eligibility review:

- If no concept is positive and distinct, close the family as negative evidence.
- If one or more concepts are promising, run a review-only refinement eligibility audit.
- Do not validate directly from first-pass discovery.

## SECTION 16 - Explicit Non-Goals

This design does not:

- implement formulas;
- generate candidates in code;
- generate panels;
- compute IC;
- run discovery;
- run validation;
- run refinement;
- modify governance;
- modify thresholds;
- modify production registry;
- introduce ML;
- access external data;
- use PIT metadata;
- use static sector, industry, or peer metadata;
- create portfolio or construction logic;
- promote or demote any existing candidate.

## SECTION 17 - Verification

Documentation-only verification:

- Required mechanism groups are present: Family A Volatility-of-Volatility, Family B Dispersion Path-Dependence, and Family C Event Clustering.
- Each family includes research motivation, economic intuition, candidate design space, expected orthogonality, overlap risks, state dependence, horizons of interest, expected failure modes, and 4-6 mechanism-led candidate concepts.
- Anti-redundancy controls, candidate inclusion criteria, candidate exclusion criteria, refinement policy, governance checkpoints, IC evaluation plan, artifact plan, staged execution roadmap, and explicit non-goals are included.
- Classification appears as `DESIGN_READY_WITH_RESEARCH_RISKS`.
- No implementation or research execution was performed.
