# Persistence Validation Execution v1

Date: 2026-06-18

Run id: `persistence_validation_v1`

Primary candidate: `post_drawdown_persistence_churn_adjusted_20`

Scope: research-only validation execution using the fixed package from `persistence_validation_design_v1.md`. No new variants, additional refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Validation scope:
- Primary candidate: `post_drawdown_persistence_churn_adjusted_20`.
- Fixed lineage controls: `post_drawdown_persistence_20` and `post_drawdown_persistence_core_20`.
- Horizons: h1, h5, h10, h20, with h10/h20 as primary validation horizons.
- Diagnostics: WFV-style windows, horizon review, robustness review, active coverage, window concentration, state attribution, redundancy review, and stress-repair contamination review.

Validation completion status: completed. Artifacts were written under `artifacts/research/persistence_validation_v1/`.

Overall outcome: `CONDITIONAL VALIDATION CANDIDATE`.
Decision rationale: Primary candidate retained positive h10/h20 evidence and low contamination risk, but review guardrails remain.
Review risks: `primary_positive_ic_rate_weak`.

Primary findings:
- h10 mean IC was `0.010952` with IC IR `0.138566` and positive IC rate `0.570850`.
- h20 mean IC was `0.006532` with IC IR `0.089364` and positive IC rate `0.518595`.
- h10 WFV persistence/sign consistency were `0.750000` / `0.750000`.
- h20 WFV persistence/sign consistency were `0.750000` / `0.750000`.
- Maximum stress-repair reference correlation was `0.117322`.

## SECTION 2 - Core Validation Results

Validation summary:

| signal_name                                 | role              |   best_horizon |   h10_mean_ic |   h10_ic_ir |   h10_positive_ic_rate |   h20_mean_ic |   h20_ic_ir |   h20_positive_ic_rate |   active_date_ratio |   h10_wfv_persistence |   h20_wfv_persistence |   max_stress_repair_abs_corr |   max_inventory_corr |   max_reversal_corr |
|:--------------------------------------------|:------------------|---------------:|--------------:|------------:|-----------------------:|--------------:|------------:|-----------------------:|--------------------:|----------------------:|----------------------:|-----------------------------:|---------------------:|--------------------:|
| post_drawdown_persistence_20                | lineage_anchor    |              5 |    0.00606477 |   0.0715874 |               0.57085  |    0.00250528 |   0.0323619 |               0.516529 |            0.240229 |                  0.75 |                  0.75 |                     0.106749 |                  nan |           0.0769623 |
| post_drawdown_persistence_core_20           | lineage_control   |              5 |    0.0108311  |   0.135342  |               0.578947 |    0.00657389 |   0.088449  |               0.524793 |            0.240229 |                  0.75 |                  0.75 |                     0.10652  |                  nan |           0.0749032 |
| post_drawdown_persistence_churn_adjusted_20 | primary_candidate |              5 |    0.0109522  |   0.138566  |               0.57085  |    0.00653179 |   0.0893636 |               0.518595 |            0.240229 |                  0.75 |                  0.75 |                     0.117322 |                  nan |           0.0754211 |

Primary candidate horizon behavior:

| signal_name                                 |   horizon |    mean_ic |     ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------------------------------------|----------:|-----------:|----------:|-------------------:|----------:|:------------------|
| post_drawdown_persistence_churn_adjusted_20 |         1 | 0.00376877 | 0.0483916 |           0.512922 |       503 | False             |
| post_drawdown_persistence_churn_adjusted_20 |         5 | 0.0127801  | 0.163326  |           0.589178 |       499 | True              |
| post_drawdown_persistence_churn_adjusted_20 |        10 | 0.0109522  | 0.138566  |           0.57085  |       494 | False             |
| post_drawdown_persistence_churn_adjusted_20 |        20 | 0.00653179 | 0.0893636 |           0.518595 |       484 | False             |

Consistency versus refinement: h10/h20 remained positive under the validation runner. The validation h10 and h20 values should be interpreted as fixed-scope validation measurements, not additional refinement targets.

## SECTION 3 - Robustness Assessment

WFV window results for the primary candidate:

| signal_name                                 |   horizon |   window | start_date   | end_date   |   mean_test_ic |   test_ic_ir |   positive_ic_rate |   valid_ic_dates |
|:--------------------------------------------|----------:|---------:|:-------------|:-----------|---------------:|-------------:|-------------------:|-----------------:|
| post_drawdown_persistence_churn_adjusted_20 |        10 |        1 | 2024-05-03   | 2024-10-29 |    -0.0133358  |    -0.163223 |           0.41129  |              124 |
| post_drawdown_persistence_churn_adjusted_20 |        10 |        2 | 2024-10-30   | 2025-04-30 |     0.0171719  |     0.22447  |           0.604839 |              124 |
| post_drawdown_persistence_churn_adjusted_20 |        10 |        3 | 2025-05-01   | 2025-10-24 |     0.0276452  |     0.348755 |           0.617886 |              123 |
| post_drawdown_persistence_churn_adjusted_20 |        10 |        4 | 2025-10-27   | 2026-04-23 |     0.0124745  |     0.171953 |           0.650407 |              123 |
| post_drawdown_persistence_churn_adjusted_20 |        20 |        1 | 2024-05-03   | 2024-10-24 |    -0.0132968  |    -0.228162 |           0.380165 |              121 |
| post_drawdown_persistence_churn_adjusted_20 |        20 |        2 | 2024-10-25   | 2025-04-22 |     0.0122615  |     0.134397 |           0.570248 |              121 |
| post_drawdown_persistence_churn_adjusted_20 |        20 |        3 | 2025-04-23   | 2025-10-14 |     0.0212596  |     0.270417 |           0.619835 |              121 |
| post_drawdown_persistence_churn_adjusted_20 |        20 |        4 | 2025-10-15   | 2026-04-09 |     0.00590296 |     0.111038 |           0.504132 |              121 |

Window concentration diagnostics:

| signal_name                                 |   horizon |   positive_window_count |   negative_window_count |   min_window_ic |   max_window_ic |   window_ic_range |   positive_ic_sum |   largest_positive_window_share |   recent_window_ic |   recent_window_positive_ic_rate |   valid_ic_dates_min |   valid_ic_dates_max |
|:--------------------------------------------|----------:|------------------------:|------------------------:|----------------:|----------------:|------------------:|------------------:|--------------------------------:|-------------------:|---------------------------------:|---------------------:|---------------------:|
| post_drawdown_persistence_churn_adjusted_20 |        10 |                       3 |                       1 |      -0.0133358 |       0.0276452 |         0.040981  |         0.0572916 |                        0.482535 |         0.0124745  |                         0.650407 |                  123 |                  124 |
| post_drawdown_persistence_churn_adjusted_20 |        20 |                       3 |                       1 |      -0.0132968 |       0.0212596 |         0.0345564 |         0.039424  |                        0.539255 |         0.00590296 |                         0.504132 |                  121 |                  121 |

State attribution snapshot:

| signal_name                                 |   horizon | state                           |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:--------------------------------------------|----------:|:--------------------------------|----------:|------------:|-----------:|-------------------:|
| post_drawdown_persistence_churn_adjusted_20 |        10 | RANGE_NORMALIZING               |       257 |  0.0163614  |  0.195798  |           0.560311 |
| post_drawdown_persistence_churn_adjusted_20 |        10 | DISPERSION_ELEVATED_RECENT      |       388 |  0.0125607  |  0.151005  |           0.590206 |
| post_drawdown_persistence_churn_adjusted_20 |        10 | EVENT_GAP_DAY                   |       494 |  0.0109522  |  0.138566  |           0.57085  |
| post_drawdown_persistence_churn_adjusted_20 |        10 | VOL_NORMALIZING                 |       200 |  0.0105409  |  0.147473  |           0.53     |
| post_drawdown_persistence_churn_adjusted_20 |        10 | RECENT_VOL_STRESS               |       244 |  0.0100497  |  0.111996  |           0.545082 |
| post_drawdown_persistence_churn_adjusted_20 |        20 | DISPERSION_ELEVATED_RECENT      |       378 |  0.00706209 |  0.0931483 |           0.510582 |
| post_drawdown_persistence_churn_adjusted_20 |        20 | RANGE_NORMALIZING               |       250 |  0.00654509 |  0.0881945 |           0.504    |
| post_drawdown_persistence_churn_adjusted_20 |        20 | EVENT_GAP_DAY                   |       484 |  0.00653179 |  0.0893636 |           0.518595 |
| post_drawdown_persistence_churn_adjusted_20 |        20 | VOL_NORMALIZING                 |       200 |  0.00570197 |  0.0828635 |           0.495    |
| post_drawdown_persistence_churn_adjusted_20 |        10 | DISPERSION_STABILITY_TRANSITION |       158 | -0.00243562 | -0.0274147 |           0.474684 |
| post_drawdown_persistence_churn_adjusted_20 |        20 | RECENT_VOL_STRESS               |       234 | -0.00424163 | -0.0501545 |           0.42735  |
| post_drawdown_persistence_churn_adjusted_20 |        10 | DISPERSION_NORMALIZING          |       183 | -0.00669974 | -0.0784889 |           0.442623 |

Robustness interpretation: the candidate's validation strength depends on whether h10/h20 WFV windows remain consistently positive and whether recent-window behavior is acceptable. Any negative or concentrated window should be treated as validation risk rather than a reason to tune the formula.

## SECTION 4 - Diversification Assessment

Stress-repair contamination review:

| signal_name                                 |   max_stress_repair_abs_corr | top_stress_repair_reference                         |   positive_stress_state_count | strongest_stress_state   |   strongest_stress_state_mean_ic | strongest_concept_state   |   strongest_concept_state_mean_ic | contamination_flag   |
|:--------------------------------------------|-----------------------------:|:----------------------------------------------------|------------------------------:|:-------------------------|---------------------------------:|:--------------------------|----------------------------------:|:---------------------|
| post_drawdown_persistence_churn_adjusted_20 |                     0.117322 | stress_proxy_percentile_rank_stability_20_downtrend |                             6 | recovery_phase           |                         0.162643 | RANGE_NORMALIZING         |                         0.0163614 | False                |

Persistence-family distinctiveness: the candidate is highly related to its lineage controls, as expected, so validation supports a candidate lineage rather than broad independent family breadth. Stress-repair correlation remained `0.117322`, which supports distinctiveness from hostile/stress-repair references at the artifact level.

Overlap with hostile/stress-repair family: no governance or production stress-repair feature was added. Contamination risk is assessed through stress-reference correlations and state attribution; low correlation supports distinctiveness, while any stress-state-only IC concentration remains a review risk.

Redundancy with existing candidates: full redundancy outputs are in `redundancy_review.csv` and summarized in `orthogonality_summary.csv`. Parent/sibling redundancy is expected and should not be misread as independent family breadth.

Does this appear to represent a genuinely different alpha family? Yes, conditionally. The evidence supports a distinct persistence candidate thread if h10/h20 robustness and low stress-repair overlap are accepted under existing standards; it does not by itself prove a broad persistence family.

## SECTION 5 - Validation Outcome

Classification: `CONDITIONAL VALIDATION CANDIDATE`

This classification uses the fixed validation package and existing-style diagnostics. It does not alter thresholds, register the candidate, or make a governance decision.

## SECTION 6 - Recommendation

1. Did the candidate pass validation?

No. The fixed-scope outcome is `CONDITIONAL VALIDATION CANDIDATE`.

2. Did the persistence family survive validation?

Yes, as a candidate lineage. The result should not be overread as broad family validation because the evidence remains concentrated in one lineage.

3. Does this improve alpha-family diversification?

Yes, modestly. The diversification value depends on low stress-repair overlap and stable h10/h20 behavior.

4. What are the primary risks?

`primary_positive_ic_rate_weak`. Additional qualitative risks remain: family concentration, sibling redundancy, and possible stress-adjacent activation.

5. What should the next Codex task be?

The next Codex task should be a research-only validation interpretation and integration-readiness design if the user accepts this validation outcome. It should not modify governance, change thresholds, register production candidates, add variants, implement ML, or promote/demote candidates.

## Research Caveat

This was a research-only validation execution. It does not register production artifacts, modify governance, change thresholds, implement ML, or promote/demote any candidate.
