# Project Underdog - OHLCV Volatility-of-Volatility Validation Design Review v1

## SECTION 1 - Design Objective

This note designs the validation plan for the two approved OHLCV Volatility-of-Volatility bounded refinement candidates.

Current status:

- `REFINEMENT_STATE_SYNCHRONIZED`

Validation-design classification:

- `VALIDATION_DESIGN_READY_FOR_IMPLEMENTATION`

This is validation-design only. No validation was executed, no IC was recomputed, no panels were regenerated, no formulas were modified, no production registry files were changed, no thresholds were changed, and no ML was introduced.

## SECTION 2 - Inputs Reviewed

Reviewed notes:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_master_state_update_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_governance_decision_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_research_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_ic_discovery_v1.md`
- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`

Evidence roots referenced but not modified:

- Refinement panels: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
- Refinement IC discovery: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

## SECTION 3 - Validation Scope

Approved validation candidates:

| candidate_id | validation role | branch | primary horizon | secondary horizons |
| --- | --- | --- | --- | --- |
| `vov_03_ref_strict_chop` | validation candidate | `vov_03` | h10 | h5, h20 |
| `vov_01_ref_smoothed_calm` | validation candidate | `vov_01` | h20 | h5, h10 |

Baseline comparators:

| candidate_id | comparator role | branch | allowed use |
| --- | --- | --- | --- |
| `vov_03_ref_anchor` | branch baseline comparator | `vov_03` | Compare preservation and improvement versus original refined anchor only. |
| `vov_01_ref_anchor` | branch baseline comparator | `vov_01` | Compare preservation and improvement versus original refined anchor only. |

Explicitly excluded from validation design:

- `vov_01_ref_longer_memory`
- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`
- original rejected or parked VoV candidates: `vov_02`, `vov_04`
- original watch-only VoV candidate: `vov_05`
- `dpath_*`
- `ecluster_*`

Comparator policy:

- Anchors may be included in validation artifacts only to provide branch-level baseline metrics.
- Anchors must not receive pass/fail validation candidate status.
- Anchors must not be promoted, production-registered, or treated as alternative validation targets from this design.

## SECTION 4 - Candidate-Specific Validation Hypotheses

### vov_03_ref_strict_chop

Hypothesis:

- A stricter prior-chop requirement improves the original `vov_03` range-chop exhaustion mechanism by isolating cleaner medium-horizon dislocations without becoming a plain reversal, stress-repair, or slow volatility-compression proxy.

Validation expectation:

- h10 should remain the primary evidence horizon.
- h20 should provide supportive confirmation but must not be the only source of evidence.
- The candidate should improve or preserve h10 evidence versus `vov_03_ref_anchor` after validation-time stability and contamination checks.

Key failure concern:

- The stricter chop filter may simply select stress-repair, plain reversal, or volume-shock reversal states instead of a distinct volatility-of-volatility mechanism.

### vov_01_ref_smoothed_calm

Hypothesis:

- Smoothed VoV calm improves the original `vov_01` calm-after-VoV-dislocation mechanism by reducing slope noise while preserving the branch's medium-horizon volatility-structure signal.

Validation expectation:

- h20 should remain the primary evidence horizon.
- h10 should remain constructive enough to reduce single-horizon concentration risk.
- The candidate should improve or preserve h20 evidence versus `vov_01_ref_anchor` after validation-time stability and contamination checks.

Key failure concern:

- Smoothing may convert the candidate into a generic volatility-compression, longer-memory stabilization, or `vov_05`-like behavior proxy.

## SECTION 5 - Validation Methodology

Validation execution should be implemented only after this design is approved for implementation.

Required input artifacts:

- Audited bounded refinement panels from `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`.
- Approved close-price or forward-return source used by the existing IC discovery stack.
- Existing IC discovery artifacts for benchmark comparison only.
- Predeclared contamination reference panels or fixed candidate references for volatility compression, hostile/stress repair, persistence/rank stability, rank-coherence, plain reversal, volume-shock reversal, and `vov_05`-like behavior.

Timing policy:

- Signal date `t` remains after-close on `t`.
- Forward returns must begin strictly after `t`.
- No same-bar, same-close, restated, or future information may enter the validation signal or return construction.

Recommended validation split:

| component | design |
| --- | --- |
| Full-sample confirmation | Recompute candidate and comparator diagnostics from audited panels using the frozen validation runner. |
| Walk-forward windows | Use chronological rolling or expanding windows with no future leakage; recommended checkpoints are 63, 126, and 252 trading-day rolling diagnostics plus coarse calendar subperiods. |
| Stability slices | Evaluate early/middle/late sample, recent-window behavior, and stress/non-stress regimes if regime labels already exist as approved references. |
| Candidate isolation | Validate only the two approved candidates; carry anchors and contamination references as comparators only. |

Validation should be deterministic and rerunnable from fixed inputs and manifests.

## SECTION 6 - Required Horizons And Metrics

Required horizons:

- h1: diagnostic only.
- h5: secondary.
- h10: primary for `vov_03_ref_strict_chop`; secondary for `vov_01_ref_smoothed_calm`.
- h20: primary for `vov_01_ref_smoothed_calm`; secondary for `vov_03_ref_strict_chop`.

Required IC metrics:

- mean IC.
- IC IR.
- positive IC rate.
- daily IC count.
- daily IC standard deviation.
- rolling 63, 126, and 252 mean IC.
- rolling 63, 126, and 252 positive IC rate.
- worst rolling-window mean IC.
- recent-window mean IC and positive IC rate.
- primary-horizon delta versus branch anchor.

Required operational metrics:

- active coverage by date and overall.
- ticker coverage.
- missing-data rate.
- inactive-neutralized rate.
- warmup-trimmed observations.
- duplicate `(date, ticker, candidate_id)` keys.
- turnover proxy or rank-churn proxy where available.
- signal distribution diagnostics by candidate and horizon.

Required comparator metrics:

- branch anchor deltas.
- correlation to branch anchor.
- correlation and co-activation with contamination references.
- primary-horizon evidence versus original VoV watch-only `vov_05` behavior where an approved reference exists.

## SECTION 7 - Pass/Fail Criteria

No single metric should be sufficient for a validation pass. The validation decision should combine primary-horizon strength, stability, robustness versus anchor, and contamination control.

Candidate-level pass conditions:

| requirement | `vov_03_ref_strict_chop` | `vov_01_ref_smoothed_calm` |
| --- | --- | --- |
| Primary horizon | h10 remains positive and economically interpretable. | h20 remains positive and economically interpretable. |
| Secondary support | h20 is positive or not materially contradictory. | h10 is positive or not materially contradictory. |
| Anchor comparison | h10 is equal to or better than `vov_03_ref_anchor` on mean IC or IC IR without worse hit-rate quality. | h20 is equal to or better than `vov_01_ref_anchor` on mean IC or IC IR without worse hit-rate quality. |
| Stability | Rolling 126 and 252 primary-horizon means are positive or explainably stable. | Rolling 126 and 252 primary-horizon means are positive or explainably stable. |
| Hit rate | Primary-horizon positive IC rate is directionally constructive and not materially below anchor. | Primary-horizon positive IC rate is directionally constructive and not materially below anchor. |
| Coverage | Active coverage is sufficient and not concentrated in a tiny event slice. | Active coverage is sufficient and not concentrated in a tiny event slice. |
| Contamination | No blocking redundancy or co-activation with known references. | No blocking redundancy or co-activation with known references. |

Fail conditions:

- Primary-horizon mean IC becomes non-positive or materially weaker than anchor without compensating stability.
- Primary-horizon positive IC rate collapses below anchor in a way that suggests event concentration.
- Rolling diagnostics show single-window dominance or recent-window failure.
- Coverage is too sparse to interpret.
- Turnover or rank churn is inconsistent with the mechanism.
- Candidate behavior is mostly explained by volatility compression, hostile/stress repair, persistence/rank stability, rank-coherence, plain reversal, volume-shock reversal, or `vov_05`-like behavior.
- Any look-ahead, panel lineage, timing, duplicate-key, or formula-drift issue appears.

## SECTION 8 - Stability And Coverage Requirements

Stability checks:

- Full-sample h10/h20 IC profile.
- Rolling 63/126/252 primary-horizon mean IC.
- Rolling positive IC rate.
- Recent-window behavior.
- Calendar subperiod behavior.
- Single-window dominance review.
- Worst-window review.

Coverage checks:

- Total active observations.
- Active dates.
- Median active tickers per active date.
- Coverage by early/middle/late sample.
- Missing-data rates by candidate.
- Inactive neutralization rate.
- Warmup loss rate.

Turnover/rank-churn checks:

- Confirm the candidate is not creating impractical rank churn.
- Compare turnover proxy versus branch anchor.
- Flag any large turnover increase that is not compensated by stronger stability.

## SECTION 9 - Redundancy And Contamination Checks

Required reference families:

- volatility compression and stabilization;
- hostile/stress repair;
- persistence/rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- original `vov_05`-like longer-memory VoV behavior;
- branch anchors.

Required diagnostics:

- Cross-sectional signal correlation by date and aggregate summary.
- Candidate/reference co-activation overlap where both signals are active.
- Rank-correlation of active signal values.
- Primary-horizon IC comparison after excluding or controlling for reference activation where feasible.
- Redundancy table listing maximum absolute correlation and strongest overlapping reference.
- Narrative contamination assessment for each candidate.

Blocking contamination examples:

- `vov_03_ref_strict_chop` mostly behaves like plain reversal after chop.
- `vov_03_ref_strict_chop` mostly activates in hostile/stress repair windows and loses evidence outside them.
- `vov_01_ref_smoothed_calm` mostly behaves like volatility compression or longer-memory `vov_05` stabilization.
- Either candidate is highly redundant with rank-coherence or persistence/rank-stability references.

## SECTION 10 - Failure Modes And Stop Conditions

Failure modes to monitor:

- Single-horizon overfit.
- Single-window dominance.
- Weak recent-window behavior.
- Hit-rate deterioration despite positive mean IC.
- Sparse activation.
- Excess turnover or rank churn.
- Anchor underperformance.
- Contamination by existing stronger families.
- Formula or panel lineage drift.
- Same-bar timing or look-ahead leakage.

Stop conditions before or during validation implementation:

- Any candidate outside `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` is included as a validation target.
- Any baseline comparator is treated as a validation candidate.
- Watch or parked variants are promoted into validation scope.
- Panel manifests do not reconcile to the approved refinement panels.
- Candidate IDs, formulas, or metadata differ from the approved refinement specification.
- Duplicate panel keys are found.
- Forward-return timing is not strictly after signal date `t`.
- Contamination references are unavailable and the validation cannot make a meaningful redundancy assessment.
- Validation implementation requires formula modification or panel regeneration.

If a stop condition is triggered, validation implementation should halt and produce a blocked review note rather than executing partial validation.

## SECTION 11 - Artifact Plan

Suggested validation artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/validation_design_v1/`

Suggested validation-design implementation outputs, when separately authorized:

- `validation_manifest.json`
- `candidate_validation_summary.csv`
- `candidate_horizon_validation_scores.csv`
- `daily_validation_ic.csv`
- `rolling_validation_diagnostics.csv`
- `anchor_comparison.csv`
- `coverage_turnover_diagnostics.csv`
- `contamination_correlation_matrix.csv`
- `contamination_overlap_summary.csv`
- `stability_window_summary.csv`
- `validation_decision_inputs.csv`
- `approved_panel_manifest_copy.csv`
- `reference_manifest.csv`

Manifest fields should include:

- `module_id`
- `validation_design_id`
- `candidate_ids`
- `baseline_comparator_ids`
- `excluded_candidate_ids`
- `panel_root`
- `ic_discovery_root`
- `reference_roots`
- `horizons`
- `primary_horizon_by_candidate`
- `timing_policy`
- `validation_executed`
- `panel_regeneration_executed`
- `formula_modified`
- `production_registry_modified`
- `thresholds_modified`
- `ml_used`
- `created_at`

The artifact root is reserved for future validation-design implementation only. This note did not create or modify validation artifacts.

## SECTION 12 - Governance Decision Rules After Validation

Post-validation governance outcomes should be assigned per candidate:

| outcome | meaning |
| --- | --- |
| `VALIDATION_REVIEW_ADVANCE` | Candidate passes validation-design evidence checks and may proceed to a formal validation eligibility or governance review, as separately scoped. |
| `WATCH` | Candidate has useful evidence but unresolved stability, coverage, turnover, or contamination risk. No promotion. |
| `PARK` | Candidate fails primary evidence, stability, coverage, or contamination requirements. Archive evidence. |
| `DIAGNOSTIC` | Candidate or comparator is useful as a reference but not eligible for advancement. |

Rules:

- `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` are the only candidates eligible for a post-validation `VALIDATION_REVIEW_ADVANCE` decision.
- `vov_01_ref_anchor` and `vov_03_ref_anchor` must remain comparator-only and can receive only diagnostic/comparator interpretation.
- Watch and parked variants cannot be advanced from this validation design.
- Passing validation design does not mean production readiness.
- Any production, registry, threshold, or ML action would require a separate governance process.

## SECTION 13 - Explicit Non-Goals

This validation design does not:

- execute validation;
- recompute IC;
- regenerate panels;
- modify formulas;
- modify production registry entries;
- change governance thresholds;
- introduce ML;
- authorize validation for watch candidates;
- authorize validation for parked candidates;
- authorize validation for original rejected VoV candidates;
- authorize use of `dpath_*` or `ecluster_*` families;
- authorize another refinement cycle.

## SECTION 14 - Verification

Verification performed:

- Required sections are present.
- Only `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` are included as validation candidates.
- `vov_01_ref_anchor` and `vov_03_ref_anchor` are included only as baseline comparators.
- `vov_01_ref_longer_memory`, parked variants, original rejected VoV candidates, `dpath_*`, and `ecluster_*` are explicitly excluded.
- No validation was executed.
- No validation artifacts were created or modified.
- No panels were regenerated.
- No IC was recomputed.
- No formulas were modified.
- No production registry files were modified.
- No thresholds were changed.
- No ML was introduced.

## SECTION 15 - Recommended Next Phase

Recommended next phase:

- Implement the validation-design runner and artifact contract for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` only, subject to the stop conditions in this note.

Final classification:

- `VALIDATION_DESIGN_READY_FOR_IMPLEMENTATION`
