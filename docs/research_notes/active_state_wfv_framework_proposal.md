# Active-State WFV Framework Proposal

- Run ID: `active_state_wfv_diagnostics_20260515_103306`
- Diagnostics version: `active_state_wfv_diagnostics_v1`
- Run timestamp: `2026-05-15 10:33:06`
- Scope: research-only. No official WFV gates, schemas, promotion rules, or alpha construction logic are changed.

## Motivation

Conditional signals can be active only during sparse market states. Fixed WFV windows remain the official gate, but they can produce undefined IC IR and persistence when most test windows contain zero active-condition dates.

## Proposed Diagnostic Layer

Active-state WFV should be a sidecar diagnostic that reuses official WFV windows but evaluates daily IC only on dates where the signal condition is active. It should write standalone research artifacts, never official WFV tables.

Core outputs:

- Active-condition date counts per WFV train/test window.
- Active-only test IC, effective IC, daily IC IR, sign consistency, and active-window coverage.
- Explicit failure classifications: sparse conditional edge, inactive-window dilution, episodic edge, unstable edge, and one-window dominated edge.

## Initial Signal

- Signal: `smooth_trend_persistence_60_downtrend`
- Horizon: h20
- Conditional context: `benchmark_trend_regime=DOWNTREND`
- Official WFV status: `REJECTED_WFV`
- Failure classification: `sparse conditional edge; inactive-window dilution; one-window dominated edge`

## Window Diagnostics

|   window_id |   train_active_dates |   test_active_dates |   active_only_test_valid_ic_dates |   active_only_effective_test_ic |   active_only_effective_test_ic_ir |   active_window_eligible |   positive_effective_ic_share |
|------------:|---------------------:|--------------------:|----------------------------------:|--------------------------------:|-----------------------------------:|-------------------------:|------------------------------:|
|           1 |                   38 |                   0 |                                 0 |                      nan        |                          nan       |                        0 |                           nan |
|           2 |                   38 |                   0 |                                 0 |                      nan        |                          nan       |                        0 |                           nan |
|           3 |                  188 |                   0 |                                 0 |                      nan        |                          nan       |                        0 |                           nan |
|           4 |                    0 |                  17 |                                17 |                        0.292996 |                            2.20543 |                        0 |                             1 |

## Active Daily IC Distribution

| sample                      |   n_valid_ic_dates |   mean_ic |   effective_mean_ic |   median_ic |   effective_median_ic |   ic_std |     ic_ir |   effective_ic_ir |      skew |    min_ic |     max_ic |    p05_ic |    p95_ic |   winsorized_mean_ic |   winsorized_effective_mean_ic |   positive_ic_rate |   sign_consistency | diagnostics_run_id                           | diagnostics_version             |
|:----------------------------|-------------------:|----------:|--------------------:|------------:|----------------------:|---------:|----------:|------------------:|----------:|----------:|-----------:|----------:|----------:|---------------------:|-------------------------------:|-------------------:|-------------------:|:---------------------------------------------|:--------------------------------|
| all_active_valid_dates      |                281 | -0.148629 |            0.148629 |   -0.136096 |              0.136096 | 0.201786 | -0.736565 |          0.736565 | -0.345719 | -0.733246 |  0.373442  | -0.459911 |  0.159035 |            -0.144337 |                       0.144337 |           0.259786 |           0.740214 | active_state_wfv_diagnostics_20260515_103306 | active_state_wfv_diagnostics_v1 |
| wfv_test_active_valid_dates |                 17 | -0.292996 |            0.292996 |   -0.257109 |              0.257109 | 0.132852 | -2.20543  |          2.20543  | -0.563619 | -0.536661 | -0.0766873 | -0.517732 | -0.117687 |            -0.294294 |                       0.294294 |           0        |           1        | active_state_wfv_diagnostics_20260515_103306 | active_state_wfv_diagnostics_v1 |

## Threshold Recommendations

- Minimum active test dates per eligible window: 20.
- Minimum eligible active WFV windows: 2.
- Minimum active-window coverage ratio: 0.50.
- Treat one-window dominance above 60% of positive effective IC as a warning, not a promotion criterion.
- Require active-only results to remain diagnostic until a conditional-alpha framework defines separate research gates.

## Viability Assessment

Active-state WFV is viable as a research diagnostic for conditional-alpha design. It is not viable as a replacement for official WFV gates without a separate governance decision, because it changes the sampling question from universal fixed-window persistence to state-conditional persistence.

## Recommendation

Use this framework to decide whether conditional edges deserve further conditional-alpha research. Do not use it to promote signals directly. For the initial signal, the diagnosis remains sparse and one-window dominated, so the recommended action is watchlist/defer rather than promotion.

## Artifacts

Standalone CSV artifacts are written under `/Users/AnyiXu_1/Desktop/multi-factor-equity-alpha-model/artifacts/research/active_state_wfv_diagnostics`.
