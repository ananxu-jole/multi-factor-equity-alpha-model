# Track B v4 Conditional Diagnostics

## Executive Takeaway

This research-only pass analyzed the four v4 `CONDITIONAL_ONLY_RESEARCH` candidates under `track_b_v4_conditional_diagnostics`.

The candidates are not ready for promotion or registration. The useful evidence is narrower: v4 did produce several mechanisms with materially lower reversal/price-rank similarity, but their edges appear state-dependent, weak, or turnover-sensitive rather than standalone robust.

No production logic, gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, or Conditional-Alpha production paths were changed.

## Candidates Reviewed

- `participation_liquidity_state_shift_20_60`
- `conditional_low_overextension_breakout_20`
- `gap_followthrough_low_churn_10`
- `nonprice_liquidity_persistence_20_60`

## Base v4 Diagnostics

| signal_name                               | family                |   best_horizon |     mean_ic |   abs_mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   missing_pct |   max_abs_baseline_corr |   wfv_persistence |   wfv_sign_consistency |   positive_regime_count |   best_regime_ic | status                    | review_issues                                                                                                    |
|:------------------------------------------|:----------------------|---------------:|------------:|--------------:|-----------:|-------------------:|-----------------:|--------------:|------------------------:|------------------:|-----------------------:|------------------------:|-----------------:|:--------------------------|:-----------------------------------------------------------------------------------------------------------------|
| participation_liquidity_state_shift_20_60 | state_shift           |             20 |  0.00842118 |    0.00842118 |  0.072874  |           0.509564 |        0.216332  |     0.0306089 |                0.469409 |              0.75 |                   0.75 |                       5 |        0.0199288 | CONDITIONAL_ONLY_RESEARCH | high_turnover; weak_positive_ic_rate                                                                             |
| conditional_low_overextension_breakout_20 | conditional_breakout  |             20 | -0.00628854 |    0.00628854 | -0.068343  |           0.450806 |        0.0553322 |     0.0362858 |                0.340879 |              0.25 |                   0.75 |                       2 |        0.0323855 | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_positive_ic_rate; weak_wfv_persistence                                                  |
| gap_followthrough_low_churn_10            | gap_structure         |             10 | -0.00251565 |    0.00251565 | -0.0263586 |           0.485535 |        0.101866  |     0.0183329 |                0.109793 |              0.5  |                   0.5  |                       4 |        0.0176821 | CONDITIONAL_ONLY_RESEARCH | direction_mismatch; weak_best_horizon_ic; weak_positive_ic_rate; weak_wfv_persistence; weak_wfv_sign_consistency |
| nonprice_liquidity_persistence_20_60      | liquidity_persistence |             20 |  0.00231258 |    0.00231258 |  0.0271643 |           0.510837 |        0.142576  |     0.0349027 |                0.271689 |              0.5  |                   0.5  |                       2 |        0.0176455 | CONDITIONAL_ONLY_RESEARCH | weak_best_horizon_ic; weak_wfv_persistence; weak_wfv_sign_consistency                                            |

## Orthogonality

| signal_name                               | top_baseline                                  |   max_abs_baseline_corr |   top_value_corr |   mean_rank_corr_by_date |
|:------------------------------------------|:----------------------------------------------|------------------------:|-----------------:|-------------------------:|
| conditional_low_overextension_breakout_20 | v3_range_compression_breakout_continuation_20 |                0.340879 |         0.340879 |                 0.41471  |
| gap_followthrough_low_churn_10            | v2_vol_compression_range_expansion_20_60      |                0.109793 |        -0.109793 |                -0.109825 |
| nonprice_liquidity_persistence_20_60      | v3_range_compression_breakout_continuation_20 |                0.271689 |        -0.271689 |                -0.27011  |
| participation_liquidity_state_shift_20_60 | unweighted_reversal_20                        |                0.469409 |         0.469409 |                 0.469651 |

## Turnover / Active-Date Diagnostics

| signal_name                               |   turnover_proxy |   turnover_p95 |   turnover_max |   activation_transition_turnover_share |   mean_rank_autocorr |   rank_churn |   active_dates |   active_date_ratio |   activation_transitions |   mean_active_coverage |
|:------------------------------------------|-----------------:|---------------:|---------------:|---------------------------------------:|---------------------:|-------------:|---------------:|--------------------:|-------------------------:|-----------------------:|
| participation_liquidity_state_shift_20_60 |        0.216332  |       0.336642 |       0.969147 |                               0        |             0.767282 |    0.232718  |           2059 |            0.981411 |                        1 |               0.987753 |
| conditional_low_overextension_breakout_20 |        0.0553322 |       0.16926  |       0.5      |                               0.351187 |             0.968136 |    0.031864  |           1242 |            0.591992 |                       88 |               0.989242 |
| gap_followthrough_low_churn_10            |        0.101866  |       0.127352 |       0.214054 |                               0        |             0.964848 |    0.0351525 |           2084 |            0.993327 |                        1 |               0.988262 |
| nonprice_liquidity_persistence_20_60      |        0.142576  |       0.355926 |       0.804679 |                               0        |             0.879188 |    0.120812  |           2050 |            0.977121 |                        1 |               0.987695 |

## Best Conditional Slices

| signal_name                               |   horizon | state                           |   active_state_dates |    mean_ic |     ic_ir |   positive_ic_rate |   n_dates |
|:------------------------------------------|----------:|:--------------------------------|---------------------:|-----------:|----------:|-------------------:|----------:|
| conditional_low_overextension_breakout_20 |        20 | STRESS_volatility_spike         |                  404 | 0.0323855  | 0.376086  |           0.636364 |        44 |
| participation_liquidity_state_shift_20_60 |        20 | TREND_HOSTILE                   |                  749 | 0.0235599  | 0.180488  |           0.555252 |       733 |
| participation_liquidity_state_shift_20_60 |        20 | LOW_DISPERSION                  |                  640 | 0.0203438  | 0.164459  |           0.554688 |       640 |
| conditional_low_overextension_breakout_20 |        20 | HIGH_OVEREXTENSION              |                  517 | 0.0202098  | 0.194017  |           0.557692 |       104 |
| participation_liquidity_state_shift_20_60 |        20 | STRESS_drawdown_acceleration    |                  375 | 0.0199288  | 0.141398  |           0.53352  |       358 |
| participation_liquidity_state_shift_20_60 |        20 | STRESS_panic_liquidity_stress   |                  187 | 0.0191612  | 0.128804  |           0.491979 |       187 |
| conditional_low_overextension_breakout_20 |        20 | HIGH_MARKET_VOL                 |                  503 | 0.0181665  | 0.232788  |           0.554054 |        74 |
| gap_followthrough_low_churn_10            |        10 | STRESS_recovery_phase           |                  196 | 0.0176821  | 0.178408  |           0.530612 |       196 |
| nonprice_liquidity_persistence_20_60      |        20 | STRESS_trend_transition         |                  580 | 0.0176455  | 0.216552  |           0.572451 |       559 |
| participation_liquidity_state_shift_20_60 |        20 | LOW_PARTICIPATION_BREADTH       |                  687 | 0.0168851  | 0.120577  |           0.530612 |       686 |
| conditional_low_overextension_breakout_20 |        20 | STRESS_panic_liquidity_stress   |                  187 | 0.0147179  | 0.240606  |           0.541667 |        24 |
| nonprice_liquidity_persistence_20_60      |        20 | HIGH_DISPERSION                 |                  584 | 0.0101477  | 0.112897  |           0.515789 |       570 |
| nonprice_liquidity_persistence_20_60      |        20 | STRESS_high_dispersion_rotation |                  584 | 0.0101477  | 0.112897  |           0.515789 |       570 |
| gap_followthrough_low_churn_10            |        10 | HIGH_MARKET_VOL                 |                  503 | 0.00690948 | 0.0712026 |           0.530938 |       501 |
| gap_followthrough_low_churn_10            |        10 | LIQUIDITY_IMPROVING             |                  815 | 0.00611933 | 0.0663689 |           0.517791 |       815 |
| conditional_low_overextension_breakout_20 |        20 | LIQUIDITY_DETERIORATING         |                  739 | 0.00580588 | 0.0560467 |           0.501018 |       491 |
| gap_followthrough_low_churn_10            |        10 | HIGH_DISPERSION                 |                  584 | 0.00575739 | 0.0609844 |           0.527875 |       574 |
| gap_followthrough_low_churn_10            |        10 | STRESS_high_dispersion_rotation |                  584 | 0.00575739 | 0.0609844 |           0.527875 |       574 |
| nonprice_liquidity_persistence_20_60      |        20 | TREND_HOSTILE                   |                  749 | 0.00506383 | 0.0536506 |           0.515818 |       727 |
| nonprice_liquidity_persistence_20_60      |        20 | LIQUIDITY_DETERIORATING         |                  739 | 0.00414914 | 0.0437714 |           0.531944 |       720 |

## Turnover Refinement Tests

| signal_name                               | variant             |   horizon |     mean_ic |      ic_ir |   positive_ic_rate |   turnover_proxy |   turnover_reduction_pct |   missing_pct |
|:------------------------------------------|:--------------------|----------:|------------:|-----------:|-------------------:|-----------------:|-------------------------:|--------------:|
| conditional_low_overextension_breakout_20 | smooth_5            |        20 | -0.00384323 | -0.040383  |           0.472868 |        0.0442887 |               0.199585   |     0.0372371 |
| conditional_low_overextension_breakout_20 | rebalance_10        |        20 | -0.00403333 | -0.041042  |           0.460094 |        0.032577  |               0.411246   |     0.0404749 |
| conditional_low_overextension_breakout_20 | smooth_3            |        20 | -0.00479496 | -0.0511942 |           0.461654 |        0.0486532 |               0.120707   |     0.0367615 |
| conditional_low_overextension_breakout_20 | threshold_0p35_nan  |        20 | -0.00487348 | -0.0419773 |           0.477759 |        0.0411364 |               0.256556   |     0.637031  |
| gap_followthrough_low_churn_10            | rebalance_5         |        10 | -0.00168533 | -0.0181157 |           0.501688 |        0.0828006 |               0.187163   |     0.0188065 |
| gap_followthrough_low_churn_10            | smooth_5            |        10 | -0.00224465 | -0.0239589 |           0.492761 |        0.0828174 |               0.186998   |     0.0192842 |
| gap_followthrough_low_churn_10            | low_churn_filter    |        10 | -0.00227917 | -0.0241629 |           0.500241 |        0.101576  |               0.00285136 |     0.0188115 |
| gap_followthrough_low_churn_10            | threshold_0p35_zero |        10 | -0.00228565 | -0.0246401 |           0.491321 |        0.0960012 |               0.0575753  |     0         |
| nonprice_liquidity_persistence_20_60      | threshold_0p35_nan  |        20 |  0.00413211 |  0.0428325 |           0.518719 |        0.101438  |               0.288535   |     0.372315  |
| nonprice_liquidity_persistence_20_60      | rebalance_5         |        20 |  0.00297907 |  0.0350173 |           0.519724 |        0.0753165 |               0.471746   |     0.0358381 |
| nonprice_liquidity_persistence_20_60      | rebalance_10        |        20 |  0.00295031 |  0.033489  |           0.505424 |        0.0524977 |               0.631792   |     0.035868  |
| nonprice_liquidity_persistence_20_60      | threshold_0p35_zero |        20 |  0.00251713 |  0.0305676 |           0.50936  |        0.131878  |               0.0750327  |     0         |
| participation_liquidity_state_shift_20_60 | rebalance_10        |        20 |  0.0165177  |  0.147513  |           0.561335 |        0.0591847 |               0.726418   |     0.0311115 |
| participation_liquidity_state_shift_20_60 | rebalance_5         |        20 |  0.0119698  |  0.103587  |           0.535819 |        0.0907861 |               0.58034    |     0.0310766 |
| participation_liquidity_state_shift_20_60 | smooth_5            |        20 |  0.01069    |  0.0884943 |           0.522828 |        0.0902081 |               0.583011   |     0.0315602 |
| participation_liquidity_state_shift_20_60 | smooth_3            |        20 |  0.00979506 |  0.0813875 |           0.512267 |        0.120698  |               0.44207    |     0.0310846 |

## Candidate Classifications

| signal_name                               |   base_mean_ic |   base_positive_ic_rate |   base_turnover_proxy |   max_abs_baseline_corr | best_conditional_state   |   best_conditional_mean_ic |   best_conditional_dates | best_refinement_variant   |   best_refinement_mean_ic |   best_refinement_turnover_reduction_pct | classification                   | interpretation                                                                                |
|:------------------------------------------|---------------:|------------------------:|----------------------:|------------------------:|:-------------------------|---------------------------:|-------------------------:|:--------------------------|--------------------------:|-----------------------------------------:|:---------------------------------|:----------------------------------------------------------------------------------------------|
| participation_liquidity_state_shift_20_60 |     0.00842118 |                0.509564 |             0.216332  |                0.469409 | TREND_HOSTILE            |                  0.0235599 |                      749 | rebalance_10              |                0.0165177  |                                 0.726418 | CONDITIONAL_REFINEMENT_CANDIDATE | Contains the clearest conditional structure, but turnover remains the main blocker.           |
| conditional_low_overextension_breakout_20 |    -0.00628854 |                0.450806 |             0.0553322 |                0.340879 | STRESS_volatility_spike  |                  0.0323855 |                      404 | smooth_5                  |               -0.00384323 |                                 0.199585 | REDESIGN                         | Has narrow state-specific strength, but always-on direction is wrong and persistence is weak. |
| gap_followthrough_low_churn_10            |    -0.00251565 |                0.485535 |             0.101866  |                0.109793 | STRESS_recovery_phase    |                  0.0176821 |                      196 | rebalance_5               |               -0.00168533 |                                 0.187163 | REDESIGN                         | Coverage improved versus v3, but the edge remains noisy and needs a cleaner event model.      |
| nonprice_liquidity_persistence_20_60      |     0.00231258 |                0.510837 |             0.142576  |                0.271689 | STRESS_trend_transition  |                  0.0176455 |                      580 | threshold_0p35_nan        |                0.00413211 |                                 0.288535 | CONDITIONAL_ONLY_KEEP            | Orthogonal and genuinely non-price, but standalone edge is weak and needs state filtering.    |

## Candidate Notes

### participation_liquidity_state_shift_20_60

This is the strongest v4 conditional ingredient. It had positive base h20 IC, acceptable WFV-style persistence/sign consistency from v4, low baseline similarity, and strong drawdown/panic-liquidity conditional slices. The main issue is turnover: diagnostics point to rank churn and high continuous movement rather than sparse activation transitions. Classification: `CONDITIONAL_REFINEMENT_CANDIDATE`.

### conditional_low_overextension_breakout_20

This candidate has a narrow positive stress/volatility-spike slice, but standalone direction remains negative and WFV persistence is weak. It should not be kept as an alpha signal; if revisited, it needs a redesigned conditional activation model. Classification: `REDESIGN`.

### gap_followthrough_low_churn_10

The v4 redesign materially improved missingness versus v3 and remained highly orthogonal, but the edge is still weak/noisy and turnover remains nontrivial. Some regime slices are positive, especially recovery/high-dispersion style states, but not enough for keep status without redesign. Classification: `REDESIGN`.

### nonprice_liquidity_persistence_20_60

This candidate is genuinely more orthogonal and non-price than the v3 liquidity design, but the base edge is small and WFV-style persistence is not sufficient. It has promising conditional behavior in trend-transition/high-dispersion states. Classification: `CONDITIONAL_ONLY_KEEP`.

## Recommended Next Step

Do not create a broad v5 batch yet. First run a narrow refinement design for `participation_liquidity_state_shift_20_60` focused on turnover reduction and cleaner activation, and keep `nonprice_liquidity_persistence_20_60` as a secondary conditional-only ingredient. Redesign gap and breakout concepts before retesting.
