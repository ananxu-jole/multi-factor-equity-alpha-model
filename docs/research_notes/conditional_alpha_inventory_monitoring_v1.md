# Conditional Alpha Inventory Monitoring v1

## Executive Takeaway

This research-only monitoring pass evaluated the current three-candidate Conditional Alpha Inventory under `conditional_alpha_inventory_monitoring_v1`.

Monitoring classifications: `{"HEALTHY_ACTIVE_RESEARCH": 1, "WATCH_MONITOR": 2}`

The inventory remains research-usable, but it should be treated as a monitored ecosystem rather than a static candidate list. The main risks are h20 concentration, shared hostile/stress state dependence, active-coverage fragility, and candidate-specific recent-window or window-concentration guardrails.

No new alpha candidates, discovery, validation/refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.

## Scope

This runner uses existing research panels and artifacts where available. If a full panel is unavailable, the candidate is documented as missing rather than guessed. The `participation_liquidity_state_shift_20_60` primary representation is rebuilt from its v4 base panel and documented refinement transformation because the final primary panel was not stored as a standalone parquet artifact.

## Inventory Health Summary

| signal_name                                       | family                             | inventory_status                               | primary_variant                          |   h20_mean_ic |   h20_positive_ic_rate |   turnover_proxy |   active_coverage |   persistence |   sign_consistency |   rolling_h20_ic_latest |   recent_window_ic |   recent_window_positive_rate |   max_inventory_corr |   max_reversal_corr | monitoring_classification   | failed_guardrails                                      | caution_flags                     |
|:--------------------------------------------------|:-----------------------------------|:-----------------------------------------------|:-----------------------------------------|--------------:|-----------------------:|-----------------:|------------------:|--------------:|-------------------:|------------------------:|-------------------:|------------------------------:|---------------------:|--------------------:|:----------------------------|:-------------------------------------------------------|:----------------------------------|
| participation_liquidity_state_shift_20_60         | participation_liquidity_repair     | INVENTORY_ACTIVE_RESEARCH                      | rank_persist_10_state_TREND_HOSTILE_zero |     0.0284181 |               0.568681 |        0.096397  |          0.346997 |             1 |                  1 |             0.000826855 |         0.00917071 |                      0.527473 |            0.0578586 |           0.282948  | WATCH_MONITOR               | none                                                   | rolling_ic_below_half_full_sample |
| participation_breadth_repair_under_hostile_trend  | breadth_repair_under_hostile_trend | CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE | strict_weak_breadth_rebalance_10         |     0.0307203 |               0.580537 |        0.0136189 |          0.142993 |             1 |                  1 |             0.0687654   |         0.0475733  |                      0.635135 |            0.0578586 |           0.0462923 | HEALTHY_ACTIVE_RESEARCH     | none                                                   | none                              |
| volatility_compression_after_stress_stabilization | volatility_stress_transition       | INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS      | rebalance_5                              |     0.0283914 |               0.574413 |        0.0220924 |          0.189704 |             1 |                  1 |             0.0174861   |         0.00229807 |                      0.357895 |            0.0172333 |           0.067874  | WATCH_MONITOR               | one_window_dominance_ceiling; recent_positive_rate_min | positive_ic_window_concentration  |

## Candidate-Level Monitoring Interpretation

### participation_liquidity_state_shift_20_60

- Classification: `WATCH_MONITOR`
- Activation semantics: TREND_HOSTILE primary; WEAK_BREADTH and STRESS_OR_WEAK_BREADTH confirmation
- h20 mean IC / positive IC rate: `0.028418` / `0.568681`
- Turnover / active coverage: `0.096397` / `0.346997`
- WFV-style persistence/sign consistency: `1.00` / `1.00`
- Latest rolling h20 IC / rolling positive rate: `0.000827` / `0.523810`
- Recent window IC / positive rate: `0.009171` / `0.527473`
- Guardrail failures: `none`
- Caution flags: `rolling_ic_below_half_full_sample`

### participation_breadth_repair_under_hostile_trend

- Classification: `HEALTHY_ACTIVE_RESEARCH`
- Activation semantics: strict weak breadth under hostile trend
- h20 mean IC / positive IC rate: `0.030720` / `0.580537`
- Turnover / active coverage: `0.013619` / `0.142993`
- WFV-style persistence/sign consistency: `1.00` / `1.00`
- Latest rolling h20 IC / rolling positive rate: `0.068765` / `0.746032`
- Recent window IC / positive rate: `0.047573` / `0.635135`
- Guardrail failures: `none`
- Caution flags: `none`

### volatility_compression_after_stress_stabilization

- Classification: `WATCH_MONITOR`
- Activation semantics: recent volatility or panic stress followed by range/volatility stabilization
- h20 mean IC / positive IC rate: `0.028391` / `0.574413`
- Turnover / active coverage: `0.022092` / `0.189704`
- WFV-style persistence/sign consistency: `1.00` / `1.00`
- Latest rolling h20 IC / rolling positive rate: `0.017486` / `0.396825`
- Recent window IC / positive rate: `0.002298` / `0.357895`
- Guardrail failures: `one_window_dominance_ceiling; recent_positive_rate_min`
- Caution flags: `positive_ic_window_concentration`

## Inventory-Level Overlap

### Co-Activation Matrix

|                                                   |   participation_liquidity_state_shift_20_60 |   participation_breadth_repair_under_hostile_trend |   volatility_compression_after_stress_stabilization |
|:--------------------------------------------------|--------------------------------------------:|---------------------------------------------------:|----------------------------------------------------:|
| participation_liquidity_state_shift_20_60         |                                    1        |                                           0.331044 |                                             0.18956 |
| participation_breadth_repair_under_hostile_trend  |                                    0.803333 |                                           1        |                                             0.25    |
| volatility_compression_after_stress_stabilization |                                    0.346734 |                                           0.188442 |                                             1       |

### Signal Correlation Matrix

|                                                   |   participation_liquidity_state_shift_20_60 |   participation_breadth_repair_under_hostile_trend |   volatility_compression_after_stress_stabilization |
|:--------------------------------------------------|--------------------------------------------:|---------------------------------------------------:|----------------------------------------------------:|
| participation_liquidity_state_shift_20_60         |                                  1          |                                          0.0578586 |                                         -0.00725845 |
| participation_breadth_repair_under_hostile_trend  |                                  0.0578586  |                                          1         |                                          0.0172333  |
| volatility_compression_after_stress_stabilization |                                 -0.00725845 |                                          0.0172333 |                                          1          |

### Inventory-Level Summary

|   inventory_candidate_count |   max_pairwise_abs_corr |   max_pairwise_coactivation | h20_concentration                    |   hostile_or_stress_positive_state_candidate_count |   turnover_concentration_max |   active_coverage_min |   recent_window_negative_count |
|----------------------------:|------------------------:|----------------------------:|:-------------------------------------|---------------------------------------------------:|-----------------------------:|----------------------:|-------------------------------:|
|                           3 |               0.0578586 |                    0.803333 | all_inventory_candidates_primary_h20 |                                                  3 |                     0.096397 |              0.142993 |                              0 |

## Shared Regime / State Dependence

Top positive h20 state slices by candidate:

| signal_name                                       | state                  |   state_dates |   valid_ic_dates |   mean_ic |   positive_ic_rate |
|:--------------------------------------------------|:-----------------------|--------------:|-----------------:|----------:|-------------------:|
| participation_breadth_repair_under_hostile_trend  | low_dispersion         |           640 |               81 | 0.071467  |           0.703704 |
| participation_breadth_repair_under_hostile_trend  | volatility_spike       |           404 |              163 | 0.0527585 |           0.638037 |
| participation_breadth_repair_under_hostile_trend  | panic_liquidity_stress |           187 |               86 | 0.0392347 |           0.627907 |
| participation_breadth_repair_under_hostile_trend  | weak_breadth           |           687 |              204 | 0.0362962 |           0.588235 |
| participation_breadth_repair_under_hostile_trend  | stress_or_weak_breadth |           734 |              204 | 0.0362962 |           0.588235 |
| participation_liquidity_state_shift_20_60         | low_dispersion         |           640 |              214 | 0.0455908 |           0.626168 |
| participation_liquidity_state_shift_20_60         | weak_breadth           |           687 |              511 | 0.0302451 |           0.561644 |
| participation_liquidity_state_shift_20_60         | stress_or_weak_breadth |           734 |              536 | 0.029158  |           0.559701 |
| participation_liquidity_state_shift_20_60         | trend_hostile          |           749 |              728 | 0.0284181 |           0.568681 |
| participation_liquidity_state_shift_20_60         | drawdown_acceleration  |           375 |              348 | 0.0271912 |           0.554598 |
| volatility_compression_after_stress_stabilization | panic_liquidity_stress |           187 |               48 | 0.170419  |           0.791667 |
| volatility_compression_after_stress_stabilization | drawdown_acceleration  |           375 |               49 | 0.165135  |           0.77551  |
| volatility_compression_after_stress_stabilization | weak_breadth           |           687 |              100 | 0.100257  |           0.69     |
| volatility_compression_after_stress_stabilization | stress_or_weak_breadth |           734 |              100 | 0.100257  |           0.69     |
| volatility_compression_after_stress_stabilization | trend_hostile          |           749 |              138 | 0.0789598 |           0.688406 |

## Current Ecosystem Risks

- h20 remains the dominant inventory horizon.
- Hostile, weak-breadth, drawdown, panic/liquidity, or post-stress states explain much of the current inventory's useful behavior.
- The participation and breadth candidates are intentionally distinct, but they still occupy adjacent repair semantics.
- The volatility/stress candidate adds mechanism diversity, but requires recent-window and one-window-dominance monitoring.
- Active coverage is adequate for research but not yet sufficient for construction-layer assumptions.
- Rebuilt primary representations need semantic preservation and rebuild-equivalence checks before any future integration work.

## Candidates Needing Extra Monitoring

`participation_liquidity_state_shift_20_60`, `volatility_compression_after_stress_stabilization`

## Missing Or Partial Inputs

All current inventory panels were available or rebuildable from existing research artifacts.

## Before Expansion v3

Expansion v3 should wait for at least one additional inventory monitoring pass or a formal Inventory v2 governance update. The next monitoring package should add active-window drift, co-activation drift, and rebuild-equivalence checks as first-class artifacts.

If Expansion v3 proceeds later, it should remain one-by-one and inventory-aware. New concepts should be required to fill a clear inventory gap and pass overlap checks against all three current candidates.

## Monitoring Framework Definition

Candidate-level monitoring dimensions:

- rolling h20 IC and positive IC rate
- rolling turnover
- rolling active coverage
- recent-window health
- one-window dominance
- WFV-style persistence and sign consistency drift
- baseline similarity drift
- semantic/state activation stability
- candidate-specific guardrail status

Inventory-level monitoring dimensions:

- co-activation matrix
- signal correlation matrix
- inventory overlap map
- shared regime/state dependence
- horizon concentration
- state concentration
- turnover concentration
- hidden mechanism clustering
- recent-window fragility across inventory

Monitoring classifications:

- `HEALTHY_ACTIVE_RESEARCH`
- `WATCH_MONITOR`
- `DEGRADED_RESEARCH`
- `REVIEW_FOR_DOWNGRADE`
- `RETIREMENT_CANDIDATE`

No classification changes production status. They are research governance labels only.
