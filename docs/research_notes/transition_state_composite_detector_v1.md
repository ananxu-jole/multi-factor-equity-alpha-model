# Transition-State Composite Detector v1

Date: 2026-05-21

Run id: `transition_state_composite_detector_v1`

Status: RESEARCH_ONLY_CONTEXT_DETECTOR

## Research-Only Guardrail

This detector is a research-only market/context label. It may identify useful transition-state regimes, but no output from this run should be promoted, registered, added to survivor/watchlist, or routed into portfolio/ML/blending/optimization logic from this detector alone. Useful findings should only motivate future conditional validation, attribution, or detector refinement.

This run does not claim alpha discovery. It creates a date-level context layer for future conditional diagnostics.

## Objective

The standalone Transition-State Alpha Discovery Batch rejected all 10 simple transition-state alpha structures. This detector pivots the same ingredients away from tradable signal construction and toward market-state inference:

- volatility shock intensity
- volatility decay / absorption
- liquidity recovery
- volume shock exhaustion
- dispersion normalization
- breadth stabilization
- propagation pressure
- instability persistence / resolution

## Label Semantics

- `ABSORPTION`: recent stress or volatility shock with improving absorption, liquidity, breadth, and instability-resolution scores.
- `PROPAGATION`: stress with elevated propagation pressure, range/volatility pressure, dispersion pressure, or rank churn.
- `NORMALIZATION`: post-stress normalization where dispersion, breadth, and volatility decay improve without high propagation pressure.
- `UNRESOLVED_STRESS`: stress remains elevated without enough absorption or normalization evidence.
- `NEUTRAL`: no strong transition-state condition.

## State Distribution

| state_label       |   date_count |   date_ratio |
|:------------------|-------------:|-------------:|
| ABSORPTION        |          354 |       0.1687 |
| PROPAGATION       |          230 |       0.1096 |
| NORMALIZATION     |          293 |       0.1397 |
| UNRESOLVED_STRESS |          123 |       0.0586 |
| NEUTRAL           |         1098 |       0.5234 |

## Benchmark Forward Returns By State

| asset_scope   | state_label       |   horizon |   mean_forward_return |   median_forward_return |   positive_forward_return_rate |   n_dates |
|:--------------|:------------------|----------:|----------------------:|------------------------:|-------------------------------:|----------:|
| benchmark     | ABSORPTION        |         5 |              0.005938 |                0.006743 |                       0.646893 |       354 |
| benchmark     | NEUTRAL           |         5 |              0.002427 |                0.004903 |                       0.616651 |      1093 |
| benchmark     | NORMALIZATION     |         5 |              0.003416 |                0.004874 |                       0.624573 |       293 |
| benchmark     | PROPAGATION       |         5 |             -0.000291 |                0.004130 |                       0.565217 |       230 |
| benchmark     | UNRESOLVED_STRESS |         5 |              0.004249 |                0.006831 |                       0.560976 |       123 |
| benchmark     | ABSORPTION        |        10 |              0.012288 |                0.017025 |                       0.683616 |       354 |
| benchmark     | NEUTRAL           |        10 |              0.004368 |                0.008243 |                       0.650459 |      1090 |
| benchmark     | NORMALIZATION     |        10 |              0.005945 |                0.009486 |                       0.702055 |       292 |
| benchmark     | PROPAGATION       |        10 |             -0.001811 |                0.000662 |                       0.508696 |       230 |
| benchmark     | UNRESOLVED_STRESS |        10 |              0.014773 |                0.022515 |                       0.704918 |       122 |
| benchmark     | ABSORPTION        |        20 |              0.021585 |                0.026856 |                       0.723343 |       347 |
| benchmark     | NEUTRAL           |        20 |              0.006264 |                0.012812 |                       0.653211 |      1090 |
| benchmark     | NORMALIZATION     |        20 |              0.009060 |                0.021771 |                       0.722603 |       292 |
| benchmark     | PROPAGATION       |        20 |              0.013128 |                0.026235 |                       0.660870 |       230 |
| benchmark     | UNRESOLVED_STRESS |        20 |              0.032790 |                0.033119 |                       0.756303 |       119 |

## Existing Alpha Context Attribution

This attribution is diagnostic only. It asks whether existing inventory/research panels behave differently inside detector labels; it does not promote or route the detector.

| signal_name                                                 | state_label       |   horizon |   mean_ic |   positive_ic_rate |   n_ic_dates |   active_overlap_dates |
|:------------------------------------------------------------|:------------------|----------:|----------:|-------------------:|-------------:|-----------------------:|
| inventory_participation_breadth_repair_under_hostile_trend  | ABSORPTION        |         5 |  0.016602 |           0.548387 |          155 |                    354 |
| inventory_participation_breadth_repair_under_hostile_trend  | NEUTRAL           |         5 |  0.007298 |           0.520000 |           25 |                   1068 |
| inventory_participation_breadth_repair_under_hostile_trend  | NORMALIZATION     |         5 | -0.009320 |           0.422222 |           45 |                    293 |
| inventory_participation_breadth_repair_under_hostile_trend  | PROPAGATION       |         5 |  0.017505 |           0.512195 |           41 |                    230 |
| inventory_participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS |         5 |  0.027844 |           0.529412 |           34 |                    123 |
| inventory_participation_breadth_repair_under_hostile_trend  | ABSORPTION        |        10 |  0.005704 |           0.483871 |          155 |                    354 |
| inventory_participation_breadth_repair_under_hostile_trend  | NEUTRAL           |        10 |  0.019426 |           0.520000 |           25 |                   1068 |
| inventory_participation_breadth_repair_under_hostile_trend  | NORMALIZATION     |        10 |  0.006996 |           0.488889 |           45 |                    293 |
| inventory_participation_breadth_repair_under_hostile_trend  | PROPAGATION       |        10 |  0.024709 |           0.609756 |           41 |                    230 |
| inventory_participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS |        10 |  0.030944 |           0.500000 |           34 |                    123 |
| inventory_participation_breadth_repair_under_hostile_trend  | ABSORPTION        |        20 |  0.016848 |           0.542484 |          153 |                    354 |
| inventory_participation_breadth_repair_under_hostile_trend  | NEUTRAL           |        20 |  0.042740 |           0.680000 |           25 |                   1068 |
| inventory_participation_breadth_repair_under_hostile_trend  | NORMALIZATION     |        20 |  0.006196 |           0.533333 |           45 |                    293 |
| inventory_participation_breadth_repair_under_hostile_trend  | PROPAGATION       |        20 |  0.088171 |           0.780488 |           41 |                    230 |
| inventory_participation_breadth_repair_under_hostile_trend  | UNRESOLVED_STRESS |        20 |  0.047489 |           0.500000 |           34 |                    123 |
| inventory_participation_liquidity_state_shift_20_60         | ABSORPTION        |         5 |  0.008748 |           0.528249 |          354 |                    354 |
| inventory_participation_liquidity_state_shift_20_60         | NEUTRAL           |         5 | -0.003440 |           0.481973 |         1054 |                   1059 |
| inventory_participation_liquidity_state_shift_20_60         | NORMALIZATION     |         5 |  0.010977 |           0.559727 |          293 |                    293 |
| inventory_participation_liquidity_state_shift_20_60         | PROPAGATION       |         5 |  0.001553 |           0.508696 |          230 |                    230 |
| inventory_participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS |         5 |  0.024143 |           0.552846 |          123 |                    123 |
| inventory_participation_liquidity_state_shift_20_60         | ABSORPTION        |        10 |  0.008498 |           0.500000 |          354 |                    354 |
| inventory_participation_liquidity_state_shift_20_60         | NEUTRAL           |        10 |  0.002183 |           0.512845 |         1051 |                   1059 |
| inventory_participation_liquidity_state_shift_20_60         | NORMALIZATION     |        10 |  0.008605 |           0.517123 |          292 |                    293 |
| inventory_participation_liquidity_state_shift_20_60         | PROPAGATION       |        10 | -0.006915 |           0.504348 |          230 |                    230 |
| inventory_participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS |        10 |  0.031420 |           0.598361 |          122 |                    123 |
| inventory_participation_liquidity_state_shift_20_60         | ABSORPTION        |        20 |  0.012485 |           0.472622 |          347 |                    354 |
| inventory_participation_liquidity_state_shift_20_60         | NEUTRAL           |        20 |  0.005938 |           0.519505 |         1051 |                   1059 |
| inventory_participation_liquidity_state_shift_20_60         | NORMALIZATION     |        20 |  0.005460 |           0.465753 |          292 |                    293 |
| inventory_participation_liquidity_state_shift_20_60         | PROPAGATION       |        20 |  0.007549 |           0.530435 |          230 |                    230 |
| inventory_participation_liquidity_state_shift_20_60         | UNRESOLVED_STRESS |        20 |  0.027450 |           0.596639 |          119 |                    123 |
| inventory_volatility_compression_after_stress_stabilization | ABSORPTION        |         5 |  0.030808 |           0.605634 |          142 |                    354 |
| inventory_volatility_compression_after_stress_stabilization | NEUTRAL           |         5 |  0.009112 |           0.566667 |          120 |                   1053 |
| inventory_volatility_compression_after_stress_stabilization | NORMALIZATION     |         5 |  0.004231 |           0.506329 |           79 |                    293 |
| inventory_volatility_compression_after_stress_stabilization | PROPAGATION       |         5 |  0.004484 |           0.461538 |           13 |                    230 |
| inventory_volatility_compression_after_stress_stabilization | UNRESOLVED_STRESS |         5 |  0.011159 |           0.512821 |           39 |                    123 |
| inventory_volatility_compression_after_stress_stabilization | ABSORPTION        |        10 |  0.063981 |           0.683099 |          142 |                    354 |
| inventory_volatility_compression_after_stress_stabilization | NEUTRAL           |        10 |  0.012191 |           0.576271 |          118 |                   1053 |
| inventory_volatility_compression_after_stress_stabilization | NORMALIZATION     |        10 | -0.016219 |           0.448718 |           78 |                    293 |
| inventory_volatility_compression_after_stress_stabilization | PROPAGATION       |        10 |  0.021632 |           0.384615 |           13 |                    230 |
| inventory_volatility_compression_after_stress_stabilization | UNRESOLVED_STRESS |        10 | -0.014187 |           0.384615 |           39 |                    123 |

## Time-Window Stability

|   window_id | start_date   | end_date   |   n_dates |   absorption_ratio |   propagation_ratio |   normalization_ratio |   unresolved_stress_ratio |   neutral_ratio |   mean_absorption_score |   mean_normalization_score |   mean_propagation_score |   mean_stress_score |
|------------:|:-------------|:-----------|----------:|-------------------:|--------------------:|----------------------:|--------------------------:|----------------:|------------------------:|---------------------------:|-------------------------:|--------------------:|
|           1 | 2018-01-02   | 2020-02-03 |       525 |             0.1124 |              0.0648 |                0.0819 |                    0.0171 |          0.7238 |                  0.5070 |                     0.4967 |                   0.5044 |              0.2727 |
|           2 | 2020-02-04   | 2022-03-02 |       524 |             0.2061 |              0.1469 |                0.1660 |                    0.0515 |          0.4294 |                  0.5662 |                     0.5512 |                   0.5061 |              0.4175 |
|           3 | 2022-03-03   | 2024-04-03 |       524 |             0.1660 |              0.0954 |                0.1374 |                    0.0706 |          0.5305 |                  0.5178 |                     0.5138 |                   0.4941 |              0.3626 |
|           4 | 2024-04-04   | 2026-05-07 |       525 |             0.1905 |              0.1314 |                0.1733 |                    0.0952 |          0.4095 |                  0.5535 |                     0.5461 |                   0.5052 |              0.4255 |

## Interpretation

The detector should be read as a context map, not an alpha. A useful result would be stable, interpretable state labels with differentiated forward-return and alpha-attribution profiles. A weak result would be unstable labels, tiny state samples, or context slices that do not distinguish absorption from propagation.

## Recommendation

Keep `transition_state_composite_detector_v1` as a research artifact only. The appropriate next step is a future conditional attribution pass that tests whether existing inventory candidates and future repair/stabilization candidates behave differently under these labels. Do not promote, register, blend, optimize, or validate this detector as a signal from this run alone.

## Artifacts

- `component_scores.csv`
- `composite_state_labels.csv`
- `state_distribution.csv`
- `state_transition_counts.csv`
- `state_transition_matrix.csv`
- `state_component_profile.csv`
- `forward_returns_by_state.csv`
- `alpha_context_attribution.csv`
- `stress_regime_attribution.csv`
- `sample_size_sanity.csv`
- `time_window_stability.csv`
- `manifest.json`
