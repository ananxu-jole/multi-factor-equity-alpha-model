# Project Underdog - Rank-Coherence Validation Execution v1

Date: 2026-06-19

Run id: `rank_coherence_validation_v1`

Primary candidate: `rank_coherence_churn_avoidance_02_overlap_adjusted`

Representative signal: `relative_rank_turnover_resilience_overlap_adjusted_20`

Scope: research-only validation execution using the frozen package from `rank_coherence_validation_design_v1.md`. No new variants, refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Validation scope:
- Primary frozen candidate: `rank_coherence_churn_avoidance_02_overlap_adjusted`.
- Diagnostic controls: churn anchor, churn penalized sibling, and regime-independent rank-coherence siblings.
- Horizons: h1, h5, h10, h20, with h10/h20 as primary validation horizons.
- Diagnostics: WFV-style windows, horizon review, active coverage, concentration, state attribution, redundancy, and contamination review.

Completion status: completed. Artifacts were written under `artifacts/research/rank_coherence_validation_v1/`.

Overall outcome: `CONDITIONAL VALIDATION CANDIDATE`.
Decision rationale: Primary candidate retained positive h10/h20 validation evidence, but contamination or concentration risks prevent a pass.
Review risks: `h10_wfv_persistence_weak; h10_window_concentration; h20_window_concentration; stress_repair_similarity; sibling_duplicate_risk`.

Primary findings:
- h10 mean IC `0.002311`, IC IR `0.016820`, positive IC rate `0.530364`.
- h20 mean IC `0.008670`, IC IR `0.064635`, positive IC rate `0.543388`.
- h10 WFV persistence/sign consistency `0.500000` / `0.500000`.
- h20 WFV persistence/sign consistency `0.750000` / `0.750000`.
- Persistence/stress/dispersion max correlations `0.130705` / `0.393906` / `0.251877`.

## SECTION 2 - Core Validation Results

Primary candidate horizon metrics:

| signal_name                                           |   horizon |    mean_ic |     ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:------------------------------------------------------|----------:|-----------:|----------:|-------------------:|----------:|:------------------|
| relative_rank_turnover_resilience_overlap_adjusted_20 |         1 | 0.00202283 | 0.0130715 |           0.514911 |       503 | False             |
| relative_rank_turnover_resilience_overlap_adjusted_20 |         5 | 0.00208216 | 0.0145866 |           0.521042 |       499 | False             |
| relative_rank_turnover_resilience_overlap_adjusted_20 |        10 | 0.00231084 | 0.0168196 |           0.530364 |       494 | False             |
| relative_rank_turnover_resilience_overlap_adjusted_20 |        20 | 0.00867028 | 0.064635  |           0.543388 |       484 | True              |

Validation summary across candidate and controls:

| candidate_id                                       | signal_name                                           | role              |   best_horizon |   h10_mean_ic |   h10_ic_ir |   h10_positive_ic_rate |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   active_date_ratio |   mean_active_coverage |
|:---------------------------------------------------|:------------------------------------------------------|:------------------|---------------:|--------------:|------------:|-----------------------:|--------------:|------------:|-----------------------:|--------------------:|-----------------------:|
| rank_coherence_churn_avoidance_02_anchor           | relative_rank_turnover_resilience_20                  | lineage_anchor    |             20 |    0.00287665 |   0.0209006 |               0.52834  |    0.00721165 |   0.0541487 |               0.528926 |            0.240229 |               0.957839 |
| rank_coherence_churn_avoidance_02_penalized        | relative_rank_turnover_resilience_penalized_20        | lineage_control   |             20 |    0.00292772 |   0.0213113 |               0.534413 |    0.00723544 |   0.0544036 |               0.530992 |            0.240229 |               0.957839 |
| rank_coherence_churn_avoidance_02_overlap_adjusted | relative_rank_turnover_resilience_overlap_adjusted_20 | primary_candidate |             20 |    0.00231084 |   0.0168196 |               0.530364 |    0.00867028 |   0.064635  |               0.543388 |            0.240229 |               0.961675 |
| rank_coherence_regime_independent_02_anchor        | nonhostile_transition_rank_coherence_20               | sibling_context   |              5 |    0.00578469 |   0.058698  |               0.516194 |    0.00575979 |   0.0601751 |               0.539256 |            0.240229 |               0.961675 |
| rank_coherence_regime_independent_02_smoothed      | nonhostile_transition_rank_coherence_smoothed_20      | sibling_context   |              5 |    0.00393082 |   0.0382922 |               0.526423 |    0.004894   |   0.0497215 |               0.53112  |            0.239276 |               0.961676 |
| rank_coherence_regime_independent_02_strict        | nonhostile_transition_rank_coherence_strict_20        | sibling_context   |              5 |    0.00608421 |   0.0576363 |               0.532389 |    0.00852009 |   0.0823193 |               0.543388 |            0.240229 |               0.965186 |

Coverage and concentration:

| signal_name                                           | candidate_id                                       |   horizon |   positive_window_count |   negative_window_count |   min_window_ic |   max_window_ic |   window_ic_range |   positive_ic_sum |   largest_positive_window_share |   recent_window_ic |   recent_window_positive_ic_rate |   valid_ic_dates_min |   valid_ic_dates_max |
|:------------------------------------------------------|:---------------------------------------------------|----------:|------------------------:|------------------------:|----------------:|----------------:|------------------:|------------------:|--------------------------------:|-------------------:|---------------------------------:|---------------------:|---------------------:|
| relative_rank_turnover_resilience_overlap_adjusted_20 | rank_coherence_churn_avoidance_02_overlap_adjusted |        10 |                       2 |                       2 |      -0.0204845 |       0.0282145 |         0.048699  |         0.0347937 |                        0.810907 |         0.00657924 |                         0.528455 |                  123 |                  124 |
| relative_rank_turnover_resilience_overlap_adjusted_20 | rank_coherence_churn_avoidance_02_overlap_adjusted |        20 |                       3 |                       1 |      -0.0178913 |       0.0392541 |         0.0571453 |         0.0525724 |                        0.746667 |         0.00678132 |                         0.528926 |                  121 |                  121 |

## SECTION 3 - Walk-Forward Review

WFV-style window results for the primary candidate:

|   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
|        10 |        1 | 2024-05-03   | 2024-10-29 |    -0.00482251 |   -0.0329226 |           0.516129 |              124 |
|        10 |        2 | 2024-10-30   | 2025-04-30 |    -0.0204845  |   -0.122668  |           0.403226 |              124 |
|        10 |        3 | 2025-05-01   | 2025-10-24 |     0.0282145  |    0.260334  |           0.674797 |              123 |
|        10 |        4 | 2025-10-27   | 2026-04-23 |     0.00657924 |    0.0575783 |           0.528455 |              123 |
|        20 |        1 | 2024-05-03   | 2024-10-24 |     0.00653698 |    0.0475335 |           0.504132 |              121 |
|        20 |        2 | 2024-10-25   | 2025-04-22 |    -0.0178913  |   -0.102868  |           0.471074 |              121 |
|        20 |        3 | 2025-04-23   | 2025-10-14 |     0.0392541  |    0.396078  |           0.669421 |              121 |
|        20 |        4 | 2025-10-15   | 2026-04-09 |     0.00678132 |    0.0636728 |           0.528926 |              121 |

Walk-forward interpretation: stability is judged by sign consistency, persistence across windows, recent-window behavior, and one-window dominance. Any weak window is treated as a validation risk, not a prompt to tune the formula.

State attribution snapshot:

|   horizon | state                           |   n_dates |    mean_ic |     ic_ir |   positive_ic_rate |
|----------:|:--------------------------------|----------:|-----------:|----------:|-------------------:|
|        20 | DISPERSION_STABILITY_TRANSITION |       155 | 0.0292614  | 0.224872  |           0.632258 |
|        20 | RANGE_NORMALIZING               |       250 | 0.0275848  | 0.213385  |           0.652    |
|        10 | RANGE_NORMALIZING               |       257 | 0.0194245  | 0.147386  |           0.59144  |
|        20 | DISPERSION_NORMALIZING          |       180 | 0.0192328  | 0.148755  |           0.605556 |
|        10 | DISPERSION_STABILITY_TRANSITION |       158 | 0.0176054  | 0.125754  |           0.613924 |
|        20 | VOL_NORMALIZING                 |       200 | 0.016202   | 0.1299    |           0.56     |
|        20 | DISPERSION_ELEVATED_RECENT      |       378 | 0.0158276  | 0.1142    |           0.571429 |
|        10 | VOL_NORMALIZING                 |       200 | 0.0151916  | 0.144166  |           0.615    |
|        10 | DISPERSION_NORMALIZING          |       183 | 0.00922656 | 0.0672962 |           0.584699 |
|        20 | EVENT_GAP_DAY                   |       484 | 0.00867028 | 0.064635  |           0.543388 |
|        10 | DISPERSION_ELEVATED_RECENT      |       388 | 0.00350954 | 0.0239771 |           0.536082 |
|        10 | EVENT_GAP_DAY                   |       494 | 0.00231084 | 0.0168196 |           0.530364 |

## SECTION 4 - Distinctiveness Review

Contamination review for the primary candidate:

| signal_name                                           | candidate_id                                       |   max_persistence_abs_corr | top_persistence_reference                          |   max_stress_repair_abs_corr | top_stress_repair_reference               |   max_dispersion_abs_corr | top_dispersion_reference                                      |   max_sibling_rank_coherence_abs_corr | top_sibling_rank_coherence_reference                         | strongest_stress_state   |   strongest_stress_state_mean_ic | strongest_concept_state         |   strongest_concept_state_mean_ic | persistence_contamination_flag   | stress_repair_contamination_flag   | dispersion_contamination_flag   | sibling_duplicate_flag   |
|:------------------------------------------------------|:---------------------------------------------------|---------------------------:|:---------------------------------------------------|-----------------------------:|:------------------------------------------|--------------------------:|:--------------------------------------------------------------|--------------------------------------:|:-------------------------------------------------------------|:-------------------------|---------------------------------:|:--------------------------------|----------------------------------:|:---------------------------------|:-----------------------------------|:--------------------------------|:-------------------------|
| relative_rank_turnover_resilience_overlap_adjusted_20 | rank_coherence_churn_avoidance_02_overlap_adjusted |                   0.130705 | persistence::post_drawdown_persistence_smoothed_20 |                     0.393906 | stress_proxy::failed_breakout_reversal_20 |                  0.251877 | dispersion::dispersion_transition_acceleration_neutralized_20 |                              0.923052 | sibling_rank_coherence::relative_rank_turnover_resilience_20 | recovery_phase           |                        0.0622423 | DISPERSION_STABILITY_TRANSITION |                         0.0292614 | False                            | True                               | False                           | True                     |

Persistence contamination: validation reviewed persistence references from the diversification refinement set. High correlation would indicate a renamed persistence signal; lower correlation supports rank-coherence distinctiveness.

Hostile/stress-repair contamination: validation reviewed source stress proxies and state attribution. Stress similarity remains a key risk if positive IC concentrates in stress-repair states.

Dispersion contamination: validation reviewed dispersion-transition references. Low dispersion overlap supports separation from the exploratory dispersion family.

Sibling contamination: high sibling/anchor correlation is expected for lineage continuity but cannot be counted as independent family-level evidence.

Does the candidate remain a legitimate rank-coherence signal? Yes, conditionally. The mechanism remains rank-turnover resilience, but the result should be interpreted as one refined candidate lineage.

## SECTION 5 - Validation Outcome

Classification: `CONDITIONAL VALIDATION CANDIDATE`

This classification uses existing-style validation diagnostics only. It does not modify governance, change thresholds, register anything, or promote/demote any candidate.

## SECTION 6 - Strategic Interpretation

1. Has rank-coherence survived validation?

Yes, conditionally. The validation outcome is `CONDITIONAL VALIDATION CANDIDATE`.

2. Is rank-coherence a credible alpha-family diversification success?

Yes, at candidate-thread level. The evidence does not yet prove broad family-level success.

3. Is evidence candidate-level or family-level?

Candidate-level. The validated object is one refined rank-churn lineage with sibling controls, not multiple independent rank-coherence themes.

4. What weaknesses remain?

`h10_wfv_persistence_weak; h10_window_concentration; h20_window_concentration; stress_repair_similarity; sibling_duplicate_risk`. Qualitative weaknesses include family concentration, h20-led evidence, and sibling/anchor redundancy.

## SECTION 7 - Final Recommendation

1. Validation outcome?

`CONDITIONAL VALIDATION CANDIDATE`.

2. Key risks?

`h10_wfv_persistence_weak; h10_window_concentration; h20_window_concentration; stress_repair_similarity; sibling_duplicate_risk`.

3. Should rank-coherence remain active research inventory?

Yes. The candidate should remain research-only unless a separate governance process later authorizes any inventory action.

4. What should the next Codex task be?

The next Codex task should be a review-only rank-coherence validation interpretation and integration-readiness review. It should decide whether to freeze the candidate as conditional research inventory, pursue further non-overlapping rank-coherence family breadth, or hold the track as diagnostic. It should not modify governance, change thresholds, register production candidates, add variants, implement ML, or promote/demote candidates.

## Research Caveat

This was a research-only validation execution. It does not register production artifacts, modify governance, change thresholds, implement ML, or promote/demote any candidate.
