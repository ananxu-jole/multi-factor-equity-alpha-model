# Track B v6 Focused Discovery

## Executive Takeaway

This research-only run implemented the three shortlisted concepts from the Track B v6 concept screen under `track_b_v6_focused_discovery`.

This was a small focused batch: one simple formulation per concept, no parameter grid, no broad discovery, and no production wiring.

Candidates tested: 3
Status counts: `{"CONDITIONAL_REFINEMENT_CANDIDATE": 1, "REJECT_RESEARCH": 2}`

No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.

## Source Context

- Concept screen: `docs/research_notes/track_b_v6_concept_screening.md`
- Conditional Alpha Inventory v1: `docs/research_notes/conditional_alpha_inventory_v1.md`
- Current inventory candidates used as similarity baselines: `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend`.

## Candidate Set

| signal_name                                       | family                              | mechanism_thesis                                                                                                                                 | state_transition_logic                                                                               | differs_from_inventory                                                                              | differs_from_reversal_momentum                                                                         | expected_activation_state                                                 | expected_horizon   | expected_turnover_profile   | expected_active_coverage   | run_id                       | research_status          |
|:--------------------------------------------------|:------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------|:-------------------|:----------------------------|:---------------------------|:-----------------------------|:-------------------------|
| volatility_compression_after_stress_stabilization | volatility_dispersion_stabilization | After stress or volatility spike, names whose realized range compresses without price extension may show cleaner forward behavior.               | Recent volatility/panic stress followed by individual range compression and low price extension.     | Uses volatility/range normalization rather than participation, liquidity repair, or breadth repair. | Does not fade prior returns or chase price rank; price rank is neutralized and extension is capped.    | Recent volatility spike or panic/liquidity stress with range compression. | h10-h20            | Low-medium after smoothing. | moderate                   | track_b_v6_focused_discovery | TRACK_B_V6_RESEARCH_ONLY |
| dispersion_peak_to_cross_sectional_stability      | dispersion_state_transition         | Cross-sectional dispersion peaks followed by stabilizing rank dispersion may identify healthier rotation after unstable markets.                 | Market dispersion transitions from elevated to stabilizing while individual rank churn declines.     | Uses dispersion and cross-sectional stability, not participation or weak-breadth repair.            | Selects stabilization after dispersion stress rather than prior underperformance or mature leadership. | High recent dispersion with current dispersion normalization.             | h10-h20            | Low-medium.                 | moderate                   | track_b_v6_focused_discovery | TRACK_B_V6_RESEARCH_ONLY |
| event_gap_quality_continuation_filter             | event_quality_structure             | Large gaps followed by orderly range containment and non-extreme volume may identify event quality rather than noisy reversal or chase behavior. | Material gap event with contained intraday range, close-location confirmation, and controlled churn. | Event-quality focused; not participation, liquidity, or breadth repair.                             | Requires post-event quality and range containment rather than fading or chasing raw price moves.       | Material gap event with orderly post-gap behavior.                        | h5-h20             | Medium.                     | moderate-to-sparse         | track_b_v6_focused_discovery | TRACK_B_V6_RESEARCH_ONLY |

## Structural Quality And Active Coverage

| signal_name                                       |   missing_pct |   finite_pct |   date_coverage |   turnover_proxy |   turnover_p95 |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:--------------------------------------------------|--------------:|-------------:|----------------:|-----------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| volatility_compression_after_stress_stabilization |     0.0316849 |     0.968315 |        0.979981 |        0.0591406 |       0.5      |            0.187321 |                      162 |               0.98995  |
| dispersion_peak_to_cross_sectional_stability      |     0.0449522 |     0.955048 |        0.966635 |        0.0199737 |       0        |            0.262154 |                       70 |               0.989806 |
| event_gap_quality_continuation_filter             |     0.0215477 |     0.978452 |        0.990467 |        0.602771  |       0.828688 |            0.990467 |                        1 |               0.98787  |

## Multi-Horizon IC

| signal_name                                       |   horizon |      mean_ic |   abs_mean_ic |       ic_ir |   positive_ic_rate |   n_dates | is_best_horizon   |
|:--------------------------------------------------|----------:|-------------:|--------------:|------------:|-------------------:|----------:|:------------------|
| volatility_compression_after_stress_stabilization |         1 | -0.00030666  |   0.00030666  | -0.00203101 |           0.478372 |       393 | False             |
| dispersion_peak_to_cross_sectional_stability      |         1 | -0.000778111 |   0.000778111 | -0.00580213 |           0.487273 |       550 | False             |
| event_gap_quality_continuation_filter             |         1 | -0.00145876  |   0.00145876  | -0.0119545  |           0.498796 |      2077 | False             |
| volatility_compression_after_stress_stabilization |         5 | -0.00079617  |   0.00079617  | -0.00503269 |           0.502564 |       390 | False             |
| dispersion_peak_to_cross_sectional_stability      |         5 | -0.00193351  |   0.00193351  | -0.0145181  |           0.489091 |       550 | False             |
| event_gap_quality_continuation_filter             |         5 |  0.00123131  |   0.00123131  |  0.0107077  |           0.501206 |      2073 | False             |
| volatility_compression_after_stress_stabilization |        10 |  0.00762096  |   0.00762096  |  0.0480148  |           0.507772 |       386 | False             |
| dispersion_peak_to_cross_sectional_stability      |        10 | -0.00242091  |   0.00242091  | -0.0201869  |           0.487226 |       548 | False             |
| event_gap_quality_continuation_filter             |        10 |  0.0026844   |   0.0026844   |  0.0243647  |           0.507253 |      2068 | True              |
| volatility_compression_after_stress_stabilization |        20 |  0.0110712   |   0.0110712   |  0.0702201  |           0.53562  |       379 | True              |
| dispersion_peak_to_cross_sectional_stability      |        20 | -0.00653093  |   0.00653093  | -0.0555876  |           0.472119 |       538 | True              |
| event_gap_quality_continuation_filter             |        20 |  0.0020079   |   0.0020079   |  0.0186099  |           0.51895  |      2058 | False             |

## h20 Behavior

| signal_name                                       |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   n_dates |
|:--------------------------------------------------|------------:|--------------:|-----------:|-------------------:|----------:|
| volatility_compression_after_stress_stabilization |  0.0110712  |    0.0110712  |  0.0702201 |           0.53562  |       379 |
| event_gap_quality_continuation_filter             |  0.0020079  |    0.0020079  |  0.0186099 |           0.51895  |      2058 |
| dispersion_peak_to_cross_sectional_stability      | -0.00653093 |    0.00653093 | -0.0555876 |           0.472119 |       538 |

## WFV-Style Diagnostics

| signal_name                                       |   horizon |   n_windows |   effective_mean_test_ic |   effective_test_ic_ir |   persistence |   sign_consistency |   one_window_dominance |
|:--------------------------------------------------|----------:|------------:|-------------------------:|-----------------------:|--------------:|-------------------:|-----------------------:|
| event_gap_quality_continuation_filter             |        10 |           4 |               0.0026844  |               0.513446 |          0.75 |               0.75 |               0.511542 |
| volatility_compression_after_stress_stabilization |        20 |           4 |               0.0109317  |               0.303031 |          0.5  |               0.5  |               0.355608 |
| dispersion_peak_to_cross_sectional_stability      |        20 |           4 |              -0.00657659 |              -0.251666 |          0.25 |               0.75 |               0.363214 |

## Orthogonality / Redundancy

| signal_name                                       | top_comparison                           |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |
|:--------------------------------------------------|:-----------------------------------------|------------------------:|---------------------------:|-------------------------:|---------------------:|--------------------:|--------------------:|
| dispersion_peak_to_cross_sectional_stability      | v2_vol_compression_range_expansion_20_60 |               0.233806  |                  0.0174599 |               0.012885   |            0.0174599 |           0.0061837 |           0.0125981 |
| event_gap_quality_continuation_filter             | plain_smoothed_reversal_20               |               0.0378815 |                  0.0171275 |               0.00757587 |            0.0171275 |           0.0378815 |           0.0214991 |
| volatility_compression_after_stress_stabilization | v2_vol_compression_range_expansion_20_60 |               0.208555  |                  0.0582247 |               0.00406553 |            0.0582247 |           0.0606091 |           0.0044578 |

## Stress / Regime Attribution

| signal_name                                       |   horizon | state                    |   n_dates |      mean_ic |       ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:-------------------------|----------:|-------------:|------------:|-------------------:|
| volatility_compression_after_stress_stabilization |        20 | panic_liquidity_stress   |        43 |  0.104573    |  0.482121   |           0.674419 |
| volatility_compression_after_stress_stabilization |        20 | drawdown_acceleration    |        44 |  0.0994455   |  0.45818    |           0.659091 |
| volatility_compression_after_stress_stabilization |        20 | weak_breadth             |        74 |  0.0732431   |  0.402745   |           0.635135 |
| volatility_compression_after_stress_stabilization |        20 | volatility_spike         |       182 |  0.0321338   |  0.178555   |           0.598901 |
| event_gap_quality_continuation_filter             |        10 | high_dispersion_rotation |       574 |  0.00296587  |  0.0250987  |           0.510453 |
| event_gap_quality_continuation_filter             |        10 | recovery_phase           |       196 |  0.00214354  |  0.0205432  |           0.55102  |
| event_gap_quality_continuation_filter             |        10 | trend_transition         |       572 |  0.00175539  |  0.0150027  |           0.508741 |
| event_gap_quality_continuation_filter             |        10 | panic_liquidity_stress   |       187 |  0.000587583 |  0.00402949 |           0.481283 |
| dispersion_peak_to_cross_sectional_stability      |        20 | volatility_spike         |       157 | -0.00325274  | -0.0260253  |           0.44586  |
| dispersion_peak_to_cross_sectional_stability      |        20 | recovery_phase           |        46 | -0.00751802  | -0.0586751  |           0.434783 |
| dispersion_peak_to_cross_sectional_stability      |        20 | weak_breadth             |       150 | -0.0244566   | -0.235996   |           0.42     |
| dispersion_peak_to_cross_sectional_stability      |        20 | high_dispersion_rotation |        60 | -0.0264517   | -0.193097   |           0.4      |

## Concept State Attribution

| signal_name                                       |   horizon | state                      |   n_dates |     mean_ic |      ic_ir |   positive_ic_rate |
|:--------------------------------------------------|----------:|:---------------------------|----------:|------------:|-----------:|-------------------:|
| volatility_compression_after_stress_stabilization |        20 | DISPERSION_ELEVATED_RECENT |       330 |  0.013574   |  0.0829198 |           0.551515 |
| volatility_compression_after_stress_stabilization |        20 | RANGE_NORMALIZING          |       379 |  0.0110712  |  0.0702201 |           0.53562  |
| volatility_compression_after_stress_stabilization |        20 | EVENT_GAP_DAY              |       379 |  0.0110712  |  0.0702201 |           0.53562  |
| volatility_compression_after_stress_stabilization |        20 | RECENT_VOL_STRESS          |       379 |  0.0110712  |  0.0702201 |           0.53562  |
| event_gap_quality_continuation_filter             |        10 | EVENT_GAP_DAY              |      2068 |  0.0026844  |  0.0243647 |           0.507253 |
| event_gap_quality_continuation_filter             |        10 | RANGE_NORMALIZING          |      1186 |  0.00256508 |  0.0238482 |           0.510118 |
| event_gap_quality_continuation_filter             |        10 | VOL_NORMALIZING            |       817 |  0.00177783 |  0.0179002 |           0.50918  |
| event_gap_quality_continuation_filter             |        10 | DISPERSION_NORMALIZING     |       781 |  0.00138546 |  0.0133473 |           0.501921 |
| dispersion_peak_to_cross_sectional_stability      |        20 | RANGE_NORMALIZING          |       341 | -0.00396629 | -0.0328392 |           0.469208 |
| dispersion_peak_to_cross_sectional_stability      |        20 | EVENT_GAP_DAY              |       538 | -0.00653093 | -0.0555876 |           0.472119 |
| dispersion_peak_to_cross_sectional_stability      |        20 | RECENT_VOL_STRESS          |       232 | -0.00789647 | -0.0651904 |           0.443966 |
| dispersion_peak_to_cross_sectional_stability      |        20 | VOL_NORMALIZING            |       238 | -0.0108994  | -0.0893053 |           0.504202 |

## Candidate Decisions

| signal_name                                       | family                              |   best_horizon |     mean_ic |   h20_mean_ic |   h20_positive_ic_rate |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   active_date_ratio |   max_abs_baseline_corr |   inventory_liquidity_corr |   inventory_breadth_corr |   max_inventory_corr |   max_reversal_corr |   max_momentum_corr |   wfv_persistence |   wfv_sign_consistency |   effective_test_ic_ir |   positive_regime_count |   best_regime_ic | status                           | review_issues                                                                |
|:--------------------------------------------------|:------------------------------------|---------------:|------------:|--------------:|-----------------------:|-----------:|-------------------:|-----------------:|--------------:|--------------------:|------------------------:|---------------------------:|-------------------------:|---------------------:|--------------------:|--------------------:|------------------:|-----------------------:|-----------------------:|------------------------:|-----------------:|:---------------------------------|:-----------------------------------------------------------------------------|
| volatility_compression_after_stress_stabilization | volatility_dispersion_stabilization |             20 |  0.0110712  |    0.0110712  |               0.53562  |  0.0702201 |           0.53562  |        0.0591406 |     0.0316849 |            0.187321 |               0.208555  |                  0.0582247 |               0.00406553 |            0.0582247 |           0.0606091 |           0.0044578 |              0.5  |                   0.5  |               0.303031 |                       4 |       0.104573   | CONDITIONAL_REFINEMENT_CANDIDATE | weak_wfv_persistence; weak_wfv_sign_consistency                              |
| event_gap_quality_continuation_filter             | event_quality_structure             |             10 |  0.0026844  |    0.0020079  |               0.51895  |  0.0243647 |           0.507253 |        0.602771  |     0.0215477 |            0.990467 |               0.0378815 |                  0.0171275 |               0.00757587 |            0.0171275 |           0.0378815 |           0.0214991 |              0.75 |                   0.75 |               0.513446 |                       0 |       0.00296587 | REJECT_RESEARCH                  | high_turnover; weak_best_horizon_ic; weak_h20_ic; weak_positive_ic_rate      |
| dispersion_peak_to_cross_sectional_stability      | dispersion_state_transition         |             20 | -0.00653093 |   -0.00653093 |               0.472119 | -0.0555876 |           0.472119 |        0.0199737 |     0.0449522 |            0.262154 |               0.233806  |                  0.0174599 |               0.012885   |            0.0174599 |           0.0061837 |           0.0125981 |              0.25 |                   0.75 |              -0.251666 |                       0 |      -0.00325274 | REJECT_RESEARCH                  | direction_mismatch; weak_h20_ic; weak_positive_ic_rate; weak_wfv_persistence |

## Mechanism-Family Assessment

- The run explicitly tested volatility/dispersion/event-quality mechanisms against the existing participation/liquidity/breadth inventory.
- A concept should be considered a genuinely new family only if it has positive h20 behavior, adequate active coverage, and low similarity to both inventory candidates and reversal/momentum baselines.
- Rejections are expected. The objective is to learn whether a third conditional-alpha family exists, not to force inventory expansion.

## Recommended Next Step

Run a narrow refinement diagnostics pass only for `volatility_compression_after_stress_stabilization`. Keep any refinements pre-declared and small.
