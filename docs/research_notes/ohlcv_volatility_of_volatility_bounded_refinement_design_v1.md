# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Design v1

## SECTION 1 - Design Objective

This note defines a bounded refinement design for the two approved OHLCV Volatility-of-Volatility candidates only:

- `vov_01`
- `vov_03`

Lifecycle reference:

- Follows the completed standard research module lifecycle through Phase 11 - Master Research State Update.
- This is a post-governance refinement-design task authorized by `MODULE_GOVERNANCE_APPROVED` and `MODULE_STATE_SYNCHRONIZED`.

Readiness classification:

- `REFINEMENT_DESIGN_READY_FOR_SPECIFICATION`

This is a design/specification note only. It does not implement formulas, generate panels, compute IC, run refinement, modify approved original panels, modify original formulas, change governance decisions, perform validation, modify production registry, change thresholds, or introduce ML.

## SECTION 2 - Inputs Reviewed

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_governance_decision_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_master_research_state_update_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_research_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_ic_discovery_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_panel_audit_v1.md`
- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`
- `docs/research_notes/ohlcv_vov_dpd_event_clustering_formula_and_panel_specification_v1.md`

Relevant governance state:

- Governance standard: `PROJECT_STANDARD_APPROVED`.
- VoV module state: `MODULE_STATE_SYNCHRONIZED`.
- Phase 10 governance classification: `MODULE_GOVERNANCE_APPROVED`.
- Authorized refinement targets: `vov_01` and `vov_03` only.

## SECTION 3 - Refinement Scope

Approved refinement targets:

| candidate_id | source_spec_id | Phase 10 outcome | refinement status |
| --- | --- | --- | --- |
| `vov_01` | `vov_01_instability_calm_after_chop` | `ADVANCE` | Approved for bounded refinement design. |
| `vov_03` | `vov_03_range_chop_exhaustion` | `ADVANCE` | Approved for bounded refinement design. |

Explicitly excluded candidates:

| candidate_id / family | status | refinement rule |
| --- | --- | --- |
| `vov_05` | `WATCH` | Blocked from refinement; may be used only as a watch/reference comparator. |
| `vov_02` | `PARK` | Blocked from refinement. |
| `vov_04` | `PARK` | Blocked from refinement. |
| `dpath_*` | frozen Family B | Blocked from implementation, refinement, and panel generation. |
| `ecluster_*` | frozen Family C | Blocked from implementation, refinement, and panel generation. |

Candidate count cap:

- Maximum approved refinement variants: 8 total.
- `vov_01` family: 4 variants including the original anchor.
- `vov_03` family: 4 variants including the original anchor.
- No additional variants may be added without a separate governance exception.

## SECTION 4 - Original Mechanism Interpretations

### `vov_01` - Instability Calm After Chop

Original mechanism:

- Names with previously elevated volatility-of-volatility and range chop may outperform when volatility instability begins to calm, especially when price extension is low.

Original specification:

- Source formula: `rank_cs(rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) * rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20))`
- Activation: `lag(vov_5_20,5)` above date median and `vov_slope_5 < 0`.
- Primary evidence: h20 mean IC 0.010405, h20 IC IR 0.093197, h20 positive IC rate 0.535383.
- Refinement objective: test whether the h20-led signal is robust to modest changes in lookback, activation strictness, and smoothing while preserving the same calming-instability mechanism.

### `vov_03` - Range-Chop Exhaustion

Original mechanism:

- Names with elevated repeated range chop may outperform when range disorder begins to compress, especially when recent return extension is low.

Original specification:

- Source formula: `rank_cs(rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) * rank_cs(-abs(ret_10)) * rank_cs(low_extension_20))`
- Activation: `lag(range_chop_20,5)` above date median and `range_chop_slope_5 < 0`.
- Primary evidence: h10 mean IC 0.008204, h10 IC IR 0.074103, h10 positive IC rate 0.546996.
- Refinement objective: test whether the h10-led signal is robust to modest changes in chop window, activation strictness, and extension control while preserving the range-chop exhaustion mechanism.

## SECTION 5 - Allowed Parameter Ranges

Allowed parameter ranges are intentionally narrow and mechanism-preserving.

| parameter | `vov_01` allowed range | `vov_03` allowed range | restriction |
| --- | --- | --- | --- |
| short volatility window | 5 or 10 days | not applicable unless inherited from shared diagnostics | Do not introduce new volatility families. |
| VoV/chop measurement window | 20 or 40 days | 20 or 40 days for range chop only | No window below 5 or above 40. |
| slope window | 5 or 10 days | 5 or 10 days | Must preserve negative slope/calm condition. |
| lag before calm/chop confirmation | 3, 5, or 10 trading days | 3, 5, or 10 trading days | Must avoid same-bar activation look-ahead. |
| extension control | `low_extension_20`, `rank_cs(-abs(ret_10))`, or both | `low_extension_20`, `rank_cs(-abs(ret_10))`, or both | No momentum or breakout replacement. |
| activation threshold | date median or upper-tercile prior instability/chop | date median or upper-tercile prior chop | Thresholds are predeclared; do not tune after IC. |
| smoothing | one light 3-day trailing mean of raw components or no smoothing | one light 3-day trailing mean of raw components or no smoothing | No multi-stage smoothing stack. |

Disallowed parameter changes:

- No new raw inputs beyond OHLCV-derived fields already specified.
- No sector, industry, peer, fundamental, options, macro, alternative-data, or external licensed metadata inputs.
- No target-conditioned parameter selection.
- No horizon-specific tuning after seeing IC results.
- No candidate variants that optimize thresholds to maximize IC.

## SECTION 6 - Bounded Variant Matrix

The variant matrix below freezes the allowed refinement design space. Formulas are conceptual specifications for the next formula-specification task; they are not implemented here.

### `vov_01` Variants

| proposed_id | role | mechanism-preserving change | conceptual formula sketch | primary horizon | secondary horizons |
| --- | --- | --- | --- | --- | --- |
| `vov_01_ref_anchor` | anchor | Preserve original discovery formula. | Original `vov_01` formula unchanged. | h20 | h10, h5 |
| `vov_01_ref_strict_calm` | strict activation | Require stronger prior instability and confirmed negative VoV slope. | Original components with prior `lag(vov_5_20,5)` upper-tercile activation and `vov_slope_5 < 0`. | h20 | h10 |
| `vov_01_ref_longer_memory` | memory sensitivity | Replace short VoV state with longer `vov_10_40`/`vov_slope_10` analog while preserving calm-after-chop. | Rank prior elevated `vov_10_40`, negative `vov_slope_10`, prior range chop, and low extension. | h20 | h10 |
| `vov_01_ref_smoothed_calm` | noise control | Apply one light 3-day smoothing layer to the calm component only. | Original components with lightly smoothed `-vov_slope_5` before cross-sectional rank. | h20 | h10, h5 |

### `vov_03` Variants

| proposed_id | role | mechanism-preserving change | conceptual formula sketch | primary horizon | secondary horizons |
| --- | --- | --- | --- | --- | --- |
| `vov_03_ref_anchor` | anchor | Preserve original discovery formula. | Original `vov_03` formula unchanged. | h10 | h20, h5 |
| `vov_03_ref_strict_chop` | strict activation | Require stronger prior range chop and confirmed negative chop slope. | Original components with prior `lag(range_chop_20,5)` upper-tercile activation and `range_chop_slope_5 < 0`. | h10 | h20 |
| `vov_03_ref_longer_chop` | memory sensitivity | Use longer chop memory while preserving exhaustion interpretation. | Prior elevated longer range-chop proxy, negative longer chop slope, low `abs(ret_10)`, and low extension. | h10 | h20, h5 |
| `vov_03_ref_extension_controlled` | reversal contamination control | Strengthen low-extension control without introducing reversal as the mechanism. | Original chop-exhaustion components with both `rank_cs(-abs(ret_10))` and `low_extension_20`. | h10 | h20 |

Total proposed refinement variants: 8.

## SECTION 7 - Allowed And Disallowed Formula Changes

Allowed changes:

- Preserve original anchor formulas exactly for comparison.
- Adjust only predeclared window lengths inside the original VoV or range-chop mechanism.
- Tighten activation using predeclared median or upper-tercile prior-instability thresholds.
- Apply one light smoothing step to reduce single-day slope noise.
- Strengthen low-extension controls only to reduce reversal/momentum contamination.

Disallowed changes:

- Add `vov_05` low-churn mechanics to `vov_01` or `vov_03`.
- Add `vov_02` rising-VoV mechanics.
- Add `vov_04` divergence mechanics.
- Add Family B `dpath_*` dispersion path-dependence mechanics.
- Add Family C `ecluster_*` event-clustering mechanics.
- Add hostile/stress repair gates as signal ingredients.
- Add rank-coherence, persistence, volume-shock reversal, plain reversal, momentum, or breakout ingredients as primary signal drivers.
- Tune thresholds after IC results.
- Select variants based on h1/h5 only.

## SECTION 8 - Anti-Overfitting Controls

Required controls:

- Preserve anchors for `vov_01` and `vov_03`.
- Keep total candidate count at 8 or fewer.
- Use one bounded refinement cycle only unless separately approved.
- Treat h10/h20 as primary review horizons.
- Treat h1/h5 as diagnostics only.
- Require variant interpretation before any IC execution.
- Predeclare all activation thresholds and windows.
- Compare refined variants to original anchors, not just to each other.
- Require redundancy diagnostics against:
  - volatility compression / stress stabilization;
  - hostile/stress repair;
  - persistence / rank stability;
  - rank-coherence;
  - plain reversal;
  - volume-shock reversal;
  - watch-only `vov_05`.
- Reject variants that improve mean IC only through much weaker positive IC rate or concentrated single-window behavior.

## SECTION 9 - Stop Conditions

Family-level stop conditions:

- Stop if neither `vov_01` nor `vov_03` anchor remains positive at its primary review horizon in the refinement run.
- Stop if all non-anchor variants fail to improve or preserve primary-horizon evidence versus anchors.
- Stop if family-level h10 and h20 mean IC are both materially weaker than the Phase 8 discovery family summary.
- Stop if the refinement set becomes indistinguishable from volatility compression, stress repair, rank-coherence, persistence, plain reversal, or volume-shock reversal references.

Candidate-level stop conditions:

| candidate branch | stop condition |
| --- | --- |
| `vov_01` | Stop branch if h20 mean IC, IC IR, or positive IC rate falls materially below the anchor without reducing contamination. |
| `vov_01` | Stop branch if best behavior is h1/h5 only and h10/h20 are weak or negative. |
| `vov_03` | Stop branch if h10 mean IC, IC IR, or positive IC rate falls materially below the anchor without reducing contamination. |
| `vov_03` | Stop branch if extension control makes the signal a plain reversal proxy. |

Operational stop conditions:

- Stop before implementation if formulas are ambiguous.
- Stop before panel generation if panel schema cannot preserve `source_spec_id`, anchor lineage, and activation state.
- Stop before IC if panel audit fails.
- Stop before research review if any excluded candidate appears in the refinement universe.

## SECTION 10 - Expected Panel Schema

The refinement panels should use the same canonical long-form contract as the approved VoV panels.

Required columns:

- `date`
- `ticker`
- `candidate_id`
- `source_spec_id`
- `module_id`
- `family`
- `research_status`
- `primary_horizon`
- `secondary_horizons`
- `signal_value`
- `raw_score`
- `pre_activation_raw_score`
- `is_active`
- `feature_warmup_complete`
- `finite_cross_section_count`
- `rank_min_count`
- `missing_reason`
- `timing_policy`
- `created_by_spec`

Required lineage fields:

- `candidate_id`: proposed refinement ID from Section 6.
- `source_spec_id`: original source lineage plus refinement suffix.
- `module_id`: `ohlcv_volatility_of_volatility_refinement_v1`.
- `family`: `volatility_of_volatility`.
- `research_status`: `RESEARCH_ONLY`.
- `timing_policy`: `after_close_t_forward_returns_after_t`.

Warmup, missing-data, duplicate prevention, and date-alignment rules should match the approved VoV panel specification.

## SECTION 11 - IC Evaluation Plan

Evaluation horizons:

- h1
- h5
- h10
- h20

Primary review horizons:

- `vov_01` branch: h20 primary, h10 secondary.
- `vov_03` branch: h10 primary, h20 secondary.

Required outputs for any future refinement execution:

- daily IC series;
- candidate-horizon IC scores;
- candidate IC summary;
- branch summary for `vov_01` and `vov_03`;
- family summary;
- candidate rankings;
- rolling IC diagnostics;
- anchor-versus-variant deltas;
- redundancy and contamination summary;
- approved panel manifest copy;
- refinement execution manifest.

Interpretation rules:

- h1 and h5 are diagnostic and cannot rescue weak h10/h20 evidence.
- A variant must preserve mechanism interpretation and improve either evidence quality or contamination profile.
- Improvements must be judged versus the branch anchor, not versus parked or watch candidates.
- `vov_05` may appear only as a comparator in redundancy diagnostics, not as a refinement candidate.

## SECTION 12 - Success And Rejection Criteria

Refinement success criteria:

- At least one variant in a branch improves primary-horizon mean IC, IC IR, or positive IC rate versus the anchor without increasing contamination.
- Or, a variant preserves primary-horizon evidence while materially reducing redundancy versus volatility compression, stress repair, persistence/rank stability, rank-coherence, plain reversal, or volume-shock reversal references.
- Rolling IC diagnostics do not show severe recent-window collapse.
- Active coverage remains broad enough for stable cross-sectional IC.
- Candidate interpretation remains clearly VoV or range-chop exhaustion.

Refinement rejection criteria:

- Primary-horizon evidence weakens materially versus the anchor.
- Any variant is h1/h5-only.
- Positive IC rate deteriorates while mean IC improves.
- Redundancy exceeds predeclared contamination limits without compensating evidence.
- Formula behavior becomes a disguised reversal, momentum, volatility compression, rank-coherence, persistence, volume-shock reversal, or stress-repair signal.
- Active coverage becomes too sparse for reliable daily IC.

## SECTION 13 - Validation Boundary

This design does not authorize validation.

Validation boundary:

- Future refinement execution may classify candidates only for refinement-review outcomes.
- No refined candidate may proceed to validation without a separate research review and governance decision.
- No candidate may be promoted to production, registered in a production registry, or used for ML from this design.
- No threshold changes are authorized.

## SECTION 14 - Governance Checkpoints

Required next checkpoints:

1. Refinement formula and panel specification.
2. Refinement implementation.
3. Refinement implementation review.
4. Refinement panel specification.
5. Refinement panel generation.
6. Refinement panel audit.
7. Refinement IC execution.
8. Refinement research review.
9. Refinement governance decision.
10. Master research state update.

Checkpoint rules:

- Any attempt to include `vov_05`, `vov_02`, `vov_04`, `dpath_*`, or `ecluster_*` blocks the task.
- Any implementation before formula specification blocks the task.
- Any IC execution before panel audit blocks the task.
- Any validation claim before a separate validation governance decision blocks the task.

## SECTION 15 - Artifact Plan

Suggested future artifact root for refinement execution:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/`

Suggested subdirectories:

- `specification/`
- `panel_v1/`
- `panel_audit_v1/`
- `ic_refinement_v1/`
- `research_review_v1/`

Suggested future manifest files:

- `refinement_candidate_registry.csv`
- `refinement_formula_manifest.csv`
- `panel_manifest.csv`
- `panel_generation_manifest.json`
- `schema_validation_report.csv`
- `daily_ic.csv`
- `candidate_horizon_ic_scores.csv`
- `anchor_variant_delta_summary.csv`
- `redundancy_contamination_summary.csv`
- `refinement_manifest.json`

No artifacts were generated by this design note.

## SECTION 16 - Explicit Non-Goals

This note does not:

- implement refinement formulas;
- generate panels;
- compute IC;
- run refinement;
- modify approved original panels;
- modify original formulas;
- modify governance decisions;
- refine `vov_05`, `vov_02`, or `vov_04`;
- use or implement `dpath_*`;
- use or implement `ecluster_*`;
- run validation;
- modify production registry;
- change thresholds;
- introduce ML.

## SECTION 17 - Verification Summary

Verification status:

- Required sections are present.
- Only `vov_01` and `vov_03` are included for refinement.
- Excluded candidates are explicitly blocked: `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*`.
- Total proposed refinement variants: 8.
- No implementation files were changed by this design note.
- No panel artifacts were changed.
- No IC artifacts were changed.
- No validation was performed.
- No governance decision was modified.
- No production registry changes were made.
- No thresholds were changed.
- No ML was introduced.

Final classification:

- `REFINEMENT_DESIGN_READY_FOR_SPECIFICATION`
