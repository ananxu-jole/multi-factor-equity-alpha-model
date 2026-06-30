# Conditional Alpha Inventory Monitoring v2

## Executive Takeaway

This research-only monitoring refresh evaluated the current three-candidate Conditional Alpha Inventory under `conditional_alpha_inventory_monitoring_v2` after the Expansion v3/v4 research cycle.

Monitoring classifications: `{"HEALTHY_ACTIVE_RESEARCH": 1, "WATCH_MONITOR": 2}`

Expansion v4 did not change the governance interpretation of the current inventory: Project Underdog's strongest evidence remains active repair/stabilization, while post-repair and resolved-state extensions were structurally clean but empirically weaker.

The inventory remains usable for research and stable enough to support a future Expansion v5 design screen, but not enough for construction-layer work. Expansion v5 should wait until the WATCH_MONITOR risks are explicitly accepted and should target active repair/stabilization diversification rather than post-repair calm persistence.

No new alpha candidates, discovery, validation/refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.

## Sources Reviewed

- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- `docs/research_notes/inventory_ecosystem_review_v1.md`
- `docs/research_notes/track_b_expansion_v3_midcycle_review.md`
- `docs/research_notes/track_b_expansion_v4_closeout_review.md`
- `docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md`
- `docs/research_notes/participation_breadth_repair_conditional_validation.md`
- `docs/research_notes/volatility_compression_stress_stabilization_integration_review.md`

## Candidate Health Summary

| signal_name                                       | family                             | inventory_status                               | primary_variant                          |   h20_mean_ic |   h20_positive_ic_rate |   turnover_proxy |   active_coverage |   persistence |   sign_consistency |   rolling_h20_ic_latest |   rolling_positive_rate_latest |   recent_window_ic |   recent_window_positive_rate |   one_window_dominance_recomputed |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr | monitoring_classification   | failed_guardrails                                      | caution_flags                     |
|:--------------------------------------------------|:-----------------------------------|:-----------------------------------------------|:-----------------------------------------|--------------:|-----------------------:|-----------------:|------------------:|--------------:|-------------------:|------------------------:|-------------------------------:|-------------------:|------------------------------:|----------------------------------:|---------------------:|--------------------:|--------------------:|:----------------------------|:-------------------------------------------------------|:----------------------------------|
| participation_liquidity_state_shift_20_60         | participation_liquidity_repair     | INVENTORY_ACTIVE_RESEARCH                      | rank_persist_10_state_TREND_HOSTILE_zero |     0.0284181 |               0.568681 |        0.096397  |          0.346997 |             1 |                  1 |             0.000826855 |                       0.52381  |         0.00917071 |                      0.527473 |                          0.568812 |            0.0578586 |           0.282948  |          0.166802   | WATCH_MONITOR               | none                                                   | rolling_ic_below_half_full_sample |
| participation_breadth_repair_under_hostile_trend  | breadth_repair_under_hostile_trend | CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE | strict_weak_breadth_rebalance_10         |     0.0307203 |               0.580537 |        0.0136189 |          0.142993 |             1 |                  1 |             0.0687654   |                       0.746032 |         0.0475733  |                      0.635135 |                          0.421774 |            0.0578586 |           0.0462923 |          0.0793583  | HEALTHY_ACTIVE_RESEARCH     | none                                                   | none                              |
| volatility_compression_after_stress_stabilization | volatility_stress_transition       | INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS      | rebalance_5                              |     0.0283914 |               0.574413 |        0.0220924 |          0.189704 |             1 |                  1 |             0.0174861   |                       0.396825 |         0.00229807 |                      0.357895 |                          0.652705 |            0.0172333 |           0.067874  |          0.00517082 | WATCH_MONITOR               | one_window_dominance_ceiling; recent_positive_rate_min | positive_ic_window_concentration  |

## Drift Versus Monitoring v1

| signal_name                                       | monitoring_classification_v2   |   h20_mean_ic_v2 |   h20_positive_ic_rate_v2 |   rolling_h20_ic_latest_v2 |   recent_window_ic_v2 |   recent_window_positive_rate_v2 |   turnover_proxy_v2 |   active_coverage_v2 |   max_inventory_corr_v2 | monitoring_classification_v1   |   h20_mean_ic_v1 |   h20_positive_ic_rate_v1 |   rolling_h20_ic_latest_v1 |   recent_window_ic_v1 |   recent_window_positive_rate_v1 |   turnover_proxy_v1 |   active_coverage_v1 |   max_inventory_corr_v1 |   h20_mean_ic_delta |   h20_positive_ic_rate_delta |   rolling_h20_ic_latest_delta |   recent_window_ic_delta |   recent_window_positive_rate_delta |   turnover_proxy_delta |   active_coverage_delta |   max_inventory_corr_delta | direction_vs_v1   |
|:--------------------------------------------------|:-------------------------------|-----------------:|--------------------------:|---------------------------:|----------------------:|---------------------------------:|--------------------:|---------------------:|------------------------:|:-------------------------------|-----------------:|--------------------------:|---------------------------:|----------------------:|---------------------------------:|--------------------:|---------------------:|------------------------:|--------------------:|-----------------------------:|------------------------------:|-------------------------:|------------------------------------:|-----------------------:|------------------------:|---------------------------:|:------------------|
| participation_liquidity_state_shift_20_60         | WATCH_MONITOR                  |        0.0284181 |                  0.568681 |                0.000826855 |            0.00917071 |                         0.527473 |           0.096397  |             0.346997 |               0.0578586 | WATCH_MONITOR                  |        0.0284181 |                  0.568681 |                0.000826855 |            0.00917071 |                         0.527473 |           0.096397  |             0.346997 |               0.0578586 |         4.51028e-17 |                            0 |                   2.60209e-18 |              4.85723e-17 |                         0           |            8.32667e-17 |             5.55112e-17 |                1.38778e-17 | stable            |
| participation_breadth_repair_under_hostile_trend  | HEALTHY_ACTIVE_RESEARCH        |        0.0307203 |                  0.580537 |                0.0687654   |            0.0475733  |                         0.635135 |           0.0136189 |             0.142993 |               0.0578586 | HEALTHY_ACTIVE_RESEARCH        |        0.0307203 |                  0.580537 |                0.0687654   |            0.0475733  |                         0.635135 |           0.0136189 |             0.142993 |               0.0578586 |         4.51028e-17 |                            0 |                   2.77556e-17 |              6.245e-17   |                         0           |            2.08167e-17 |             5.55112e-17 |                1.38778e-17 | stable            |
| volatility_compression_after_stress_stabilization | WATCH_MONITOR                  |        0.0283914 |                  0.574413 |                0.0174861   |            0.00229807 |                         0.357895 |           0.0220924 |             0.189704 |               0.0172333 | WATCH_MONITOR                  |        0.0283914 |                  0.574413 |                0.0174861   |            0.00229807 |                         0.357895 |           0.0220924 |             0.189704 |               0.0172333 |         2.77556e-17 |                            0 |                   6.245e-17   |              2.60209e-18 |                         5.55112e-17 |            3.46945e-18 |             5.55112e-17 |                6.93889e-18 | stable            |

## Specific Monitoring Questions

1. Did the two `WATCH_MONITOR` candidates improve, degrade, or remain stable?

- `participation_liquidity_state_shift_20_60`: remains `WATCH_MONITOR`; no downgrade review is triggered, but rolling/recent-window weakness remains the key watch reason.
- `volatility_compression_after_stress_stabilization`: remains `WATCH_MONITOR`; recent-window and concentration guardrails still require explicit acceptance before future use.

2. Does `participation_breadth_repair_under_hostile_trend` remain the cleanest inventory candidate?

- Yes. It remains `HEALTHY_ACTIVE_RESEARCH` and continues to be the cleanest current inventory anchor.

3. Is inventory correlation still low?

- Yes. Max pairwise absolute correlation is `0.057859`.

4. Is co-activation still concentrated between participation/breadth candidates?

- Yes. Max pairwise co-activation is `0.803333`, and the main concentration remains participation/liquidity with breadth repair.

5. Is h20 concentration still the main horizon risk?

- Yes. All three current inventory candidates remain monitored around h20 behavior.

6. Is hostile/stress-state dependence still the main state risk?

- Yes. State concentration remains hostile/stress, weak-breadth, drawdown, panic/liquidity, or stabilization oriented.

7. Does Expansion v4 evidence change the governance interpretation of the current inventory?

- No. Expansion v4 strengthens the interpretation that active repair/stabilization is the durable project identity. It does not justify downgrading the current inventory, but it argues against more post-repair expansion before monitoring and redesign.

## Inventory-Level Overlap

### Co-Activation Matrix

|                                                   |   participation_liquidity_state_shift_20_60 |   participation_breadth_repair_under_hostile_trend |   volatility_compression_after_stress_stabilization |
|:--------------------------------------------------|--------------------------------------------:|---------------------------------------------------:|----------------------------------------------------:|
| participation_liquidity_state_shift_20_60         |                                    1        |                                           0.331044 |                                             0.18956 |
| participation_breadth_repair_under_hostile_trend  |                                    0.803333 |                                           1        |                                             0.25    |
| volatility_compression_after_stress_stabilization |                                    0.346734 |                                           0.188442 |                                             1       |

### Co-Activation Drift

| left_signal                                       | right_signal                                      |   coactivation_v1 |   coactivation_v2 |   coactivation_delta | concentration_flag   |
|:--------------------------------------------------|:--------------------------------------------------|------------------:|------------------:|---------------------:|:---------------------|
| participation_liquidity_state_shift_20_60         | participation_breadth_repair_under_hostile_trend  |          0.331044 |          0.331044 |          5.55112e-17 | False                |
| participation_liquidity_state_shift_20_60         | volatility_compression_after_stress_stabilization |          0.18956  |          0.18956  |          5.55112e-17 | False                |
| participation_breadth_repair_under_hostile_trend  | participation_liquidity_state_shift_20_60         |          0.803333 |          0.803333 |          0           | True                 |
| participation_breadth_repair_under_hostile_trend  | volatility_compression_after_stress_stabilization |          0.25     |          0.25     |          0           | False                |
| volatility_compression_after_stress_stabilization | participation_liquidity_state_shift_20_60         |          0.346734 |          0.346734 |          5.55112e-17 | False                |
| volatility_compression_after_stress_stabilization | participation_breadth_repair_under_hostile_trend  |          0.188442 |          0.188442 |          0           | False                |

### Signal Correlation Matrix

|                                                   |   participation_liquidity_state_shift_20_60 |   participation_breadth_repair_under_hostile_trend |   volatility_compression_after_stress_stabilization |
|:--------------------------------------------------|--------------------------------------------:|---------------------------------------------------:|----------------------------------------------------:|
| participation_liquidity_state_shift_20_60         |                                  1          |                                          0.0578586 |                                         -0.00725845 |
| participation_breadth_repair_under_hostile_trend  |                                  0.0578586  |                                          1         |                                          0.0172333  |
| volatility_compression_after_stress_stabilization |                                 -0.00725845 |                                          0.0172333 |                                          1          |

### Correlation Drift

| left_signal                                      | right_signal                                      |   abs_corr_v1 |   abs_corr_v2 |   abs_corr_delta |
|:-------------------------------------------------|:--------------------------------------------------|--------------:|--------------:|-----------------:|
| participation_liquidity_state_shift_20_60        | volatility_compression_after_stress_stabilization |    0.00725845 |    0.00725845 |      9.54098e-17 |
| participation_breadth_repair_under_hostile_trend | participation_liquidity_state_shift_20_60         |    0.0578586  |    0.0578586  |      1.38778e-17 |
| participation_breadth_repair_under_hostile_trend | volatility_compression_after_stress_stabilization |    0.0172333  |    0.0172333  |      6.93889e-18 |

### Inventory-Level Summary

|   inventory_candidate_count |   max_pairwise_abs_corr |   max_pairwise_coactivation | h20_concentration                    |   hostile_or_stress_positive_state_candidate_count |   turnover_concentration_max |   active_coverage_min |   recent_window_negative_count |
|----------------------------:|------------------------:|----------------------------:|:-------------------------------------|---------------------------------------------------:|-----------------------------:|----------------------:|-------------------------------:|
|                           3 |               0.0578586 |                    0.803333 | all_inventory_candidates_primary_h20 |                                                  3 |                     0.096397 |              0.142993 |                              0 |

## State Concentration

| signal_name                                       |   positive_state_count |   hostile_or_stress_positive_state_count | top_state              |   top_state_mean_ic | hostile_stress_dependence_flag   |
|:--------------------------------------------------|-----------------------:|-----------------------------------------:|:-----------------------|--------------------:|:---------------------------------|
| participation_breadth_repair_under_hostile_trend  |                      8 |                                        6 | low_dispersion         |           0.071467  | True                             |
| participation_liquidity_state_shift_20_60         |                      9 |                                        6 | low_dispersion         |           0.0455908 | True                             |
| volatility_compression_after_stress_stabilization |                      8 |                                        6 | panic_liquidity_stress |           0.170419  | True                             |

Top positive h20 state slices by candidate:

| signal_name                                       | state                  |   state_dates |   valid_ic_dates |   mean_ic |   positive_ic_rate |
|:--------------------------------------------------|:-----------------------|--------------:|-----------------:|----------:|-------------------:|
| participation_breadth_repair_under_hostile_trend  | low_dispersion         |           640 |               81 | 0.071467  |           0.703704 |
| participation_breadth_repair_under_hostile_trend  | volatility_spike       |           404 |              163 | 0.0527585 |           0.638037 |
| participation_breadth_repair_under_hostile_trend  | panic_liquidity_stress |           187 |               86 | 0.0392347 |           0.627907 |
| participation_breadth_repair_under_hostile_trend  | weak_breadth           |           687 |              204 | 0.0362962 |           0.588235 |
| participation_breadth_repair_under_hostile_trend  | stress_or_weak_breadth |           734 |              204 | 0.0362962 |           0.588235 |
| participation_breadth_repair_under_hostile_trend  | drawdown_acceleration  |           375 |              122 | 0.0233196 |           0.590164 |
| participation_liquidity_state_shift_20_60         | low_dispersion         |           640 |              214 | 0.0455908 |           0.626168 |
| participation_liquidity_state_shift_20_60         | weak_breadth           |           687 |              511 | 0.0302451 |           0.561644 |
| participation_liquidity_state_shift_20_60         | stress_or_weak_breadth |           734 |              536 | 0.029158  |           0.559701 |
| participation_liquidity_state_shift_20_60         | trend_hostile          |           749 |              728 | 0.0284181 |           0.568681 |
| participation_liquidity_state_shift_20_60         | drawdown_acceleration  |           375 |              348 | 0.0271912 |           0.554598 |
| participation_liquidity_state_shift_20_60         | panic_liquidity_stress |           187 |              186 | 0.0268966 |           0.516129 |
| volatility_compression_after_stress_stabilization | panic_liquidity_stress |           187 |               48 | 0.170419  |           0.791667 |
| volatility_compression_after_stress_stabilization | drawdown_acceleration  |           375 |               49 | 0.165135  |           0.77551  |
| volatility_compression_after_stress_stabilization | weak_breadth           |           687 |              100 | 0.100257  |           0.69     |
| volatility_compression_after_stress_stabilization | stress_or_weak_breadth |           734 |              100 | 0.100257  |           0.69     |
| volatility_compression_after_stress_stabilization | trend_hostile          |           749 |              138 | 0.0789598 |           0.688406 |
| volatility_compression_after_stress_stabilization | volatility_spike       |           404 |              177 | 0.0633418 |           0.649718 |

## Candidate-Level Interpretation

### `participation_liquidity_state_shift_20_60`

- Classification: `WATCH_MONITOR`
- h20 mean IC / positive IC rate: `0.028418` / `0.568681`
- Rolling h20 IC / rolling positive rate: `0.000827` / `0.523810`
- Recent-window IC / positive rate: `0.009171` / `0.527473`
- WFV persistence/sign consistency: `1.00` / `1.00`
- Turnover / active coverage: `0.096397` / `0.346997`
- One-window dominance: `0.568812`
- Guardrail failures: `none`
- Caution flags: `rolling_ic_below_half_full_sample`

### `participation_breadth_repair_under_hostile_trend`

- Classification: `HEALTHY_ACTIVE_RESEARCH`
- h20 mean IC / positive IC rate: `0.030720` / `0.580537`
- Rolling h20 IC / rolling positive rate: `0.068765` / `0.746032`
- Recent-window IC / positive rate: `0.047573` / `0.635135`
- WFV persistence/sign consistency: `1.00` / `1.00`
- Turnover / active coverage: `0.013619` / `0.142993`
- One-window dominance: `0.421774`
- Guardrail failures: `none`
- Caution flags: `none`

### `volatility_compression_after_stress_stabilization`

- Classification: `WATCH_MONITOR`
- h20 mean IC / positive IC rate: `0.028391` / `0.574413`
- Rolling h20 IC / rolling positive rate: `0.017486` / `0.396825`
- Recent-window IC / positive rate: `0.002298` / `0.357895`
- WFV persistence/sign consistency: `1.00` / `1.00`
- Turnover / active coverage: `0.022092` / `0.189704`
- One-window dominance: `0.652705`
- Guardrail failures: `one_window_dominance_ceiling; recent_positive_rate_min`
- Caution flags: `positive_ic_window_concentration`

## Governance Recommendation

- Inventory stability: research-stable, with `2` WATCH_MONITOR candidates.
- Downgrade review needed now: none.
- Additional monitoring: required before construction-layer work and recommended before any Expansion v5 implementation.
- Expansion v5 design: allowed only as design-screening after explicit acceptance of WATCH_MONITOR risks.
- Expansion v5 implementation: should wait until the design screen identifies an active repair/stabilization mechanism that reduces co-activation, state, horizon, or turnover concentration.

## Future Discovery Targets

- Active repair/stabilization mechanisms outside the current participation/breadth pair.
- h10 or h15 mechanisms only when the state thesis naturally supports that horizon.
- Medium-coverage active repair states with lower co-activation against `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend`.
- Different turnover profiles from the existing liquidity and volatility/stress candidates.
- Stress or repair dimensions not reducible to passive calm accumulation, post-repair continuation, or broad hostile-to-neutral transition gates.

## Missing Or Partial Inputs

All current inventory panels were available or rebuildable from existing research artifacts.
