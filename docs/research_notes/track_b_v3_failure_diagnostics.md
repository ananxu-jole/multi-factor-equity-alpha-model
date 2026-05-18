# Track B v3 Failure Diagnostics

## Executive Takeaway

This research-only diagnostics pass analyzed Track B v3 outputs under `track_b_v3_failure_diagnostics` before any v4 candidate creation.

The v3 continuation/quality candidates did not fail because the discovery machinery broke. They mostly failed because the intended positive continuation direction was empirically negative at the relevant horizons, especially h20, and many candidates remained highly correlated with existing price-rank, momentum, or reversal-like baselines.

There is no broad evidence of a simple implementation sign error. The formulas match their documented continuation or quality intent. The stronger interpretation is that, in this universe and period, high leadership/participation/relative-strength states often behaved like overextended entries whose subsequent h10-h20 returns favored the opposite side. Inverting the signals would usually create a reversal-like proxy rather than a genuinely orthogonal standalone mechanism.

No production logic, gates, schemas, survivor/watchlist status, ML logic, portfolio logic, or Conditional-Alpha paths were changed.

## Inputs Used

- v3 artifact directory: `artifacts/research/robustness_first_discovery_expansion_v3`
- Candidate panels, registry, structural diagnostics, multi-horizon IC scoring, WFV-style diagnostics, stress/regime attribution, and orthogonality audit.
- Track A `volume_shock_reversal_stable_20` remained a baseline only.

## Candidate Set

| signal_name                                   | family                       | intuition                                                                                       | expected_horizon   |
|:----------------------------------------------|:-----------------------------|:------------------------------------------------------------------------------------------------|:-------------------|
| trend_leadership_persistence_20_60            | trend_persistence            | Continuation in names with persistent 20-day leadership confirmed by 60-day trend.              | h10-h20            |
| multi_horizon_trend_agreement_5_20_60         | multi_horizon_agreement      | Continuation when short, medium, and longer momentum ranks agree.                               | h10-h20            |
| rank_persistence_quality_20_60                | rank_stability               | Stable cross-sectional leadership measured by low rank volatility and positive rank level.      | h20                |
| breadth_participation_quality_20              | breadth_participation        | Continuation in names participating consistently in up days over the last month.                | h10-h20            |
| relative_strength_acceleration_20_60          | relative_strength            | Acceleration of benchmark-relative strength from 60-day baseline to 20-day behavior.            | h10-h20            |
| relative_strength_deceleration_risk_20_60     | relative_strength            | Penalizes names whose relative strength is decelerating despite still-positive longer trend.    | h10-h20            |
| vol_regime_transition_momentum_20_60          | volatility_transition        | Continuation when volatility normalizes from elevated 20-day volatility toward 60-day baseline. | h10-h20            |
| range_compression_breakout_continuation_20    | volatility_transition        | Continuation after price exits compressed range with supportive close location.                 | h10-h20            |
| dispersion_transition_leadership_20_60        | dispersion_transition        | Leadership continuation during rising cross-sectional dispersion transitions.                   | h10-h20            |
| dispersion_compression_quality_20_60          | dispersion_transition        | Quality continuation when dispersion compresses and rank leadership remains stable.             | h20                |
| liquidity_improvement_momentum_20_60          | liquidity_persistence        | Momentum confirmed by improving dollar-volume liquidity over medium-term baseline.              | h10-h20            |
| liquidity_deterioration_warning_20_60         | liquidity_persistence        | Avoids names with deteriorating liquidity participation and weakening price behavior.           | h10-h20            |
| gap_continuation_confirmation_5_20            | gap_continuation             | Continuation after overnight gap that is confirmed by intraday close strength and volume.       | h5-h10             |
| relative_volume_confirmed_leadership_20       | relative_volume_confirmation | Continuation where price leadership is confirmed by relative volume participation.              | h10-h20            |
| participation_trend_quality_interaction_20_60 | interaction                  | Continuation when participation quality and trend persistence agree.                            | h10-h20            |

## Direction Mismatch Summary

All 15 candidates were rejected. The dominant pattern was negative empirical IC for formulas intended to express positive continuation, participation quality, liquidity improvement, or leadership persistence.

| signal_name                                   |   best_horizon |     mean_ic |   persistence |   max_abs_baseline_corr | inverse_reversal_proxy_risk   | diagnosis                                              | recommended_action                                                                              |
|:----------------------------------------------|---------------:|------------:|--------------:|------------------------:|:------------------------------|:-------------------------------------------------------|:------------------------------------------------------------------------------------------------|
| liquidity_deterioration_warning_20_60         |             20 | -0.0176588  |          0.25 |                0.874198 | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| multi_horizon_trend_agreement_5_20_60         |             20 | -0.0173314  |          0.25 |                0.866103 | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| vol_regime_transition_momentum_20_60          |             20 | -0.0166397  |          0.25 |                0.982599 | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| trend_leadership_persistence_20_60            |             20 | -0.0145526  |          0.25 |                0.827186 | MODERATE                      | direction_mismatch_without_clean_robustness            | redesign_before_retest; inversion needs separate economic thesis                                |
| participation_trend_quality_interaction_20_60 |             20 | -0.0143194  |          0.25 |                0.824701 | MODERATE                      | direction_mismatch_without_clean_robustness            | redesign_before_retest; inversion needs separate economic thesis                                |
| liquidity_improvement_momentum_20_60          |             20 | -0.0137547  |          0.25 |                0.939264 | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| breadth_participation_quality_20              |             20 | -0.0131231  |          0.25 |                0.95268  | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| relative_volume_confirmed_leadership_20       |             20 | -0.0129298  |          0.25 |                0.946133 | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| dispersion_transition_leadership_20_60        |             20 | -0.0121978  |          0    |                0.750829 | LOW                           | direction_mismatch_without_clean_robustness            | redesign_before_retest; inversion needs separate economic thesis                                |
| relative_strength_acceleration_20_60          |             20 | -0.011374   |          0.25 |                1        | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| relative_strength_deceleration_risk_20_60     |             20 | -0.011374   |          0.25 |                1        | HIGH                          | continuation_collapsed_into_reversal_or_momentum_proxy | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| rank_persistence_quality_20_60                |             20 | -0.0107812  |          0.25 |                0.747214 | LOW                           | direction_mismatch_without_clean_robustness            | redesign_before_retest; inversion needs separate economic thesis                                |
| dispersion_compression_quality_20_60          |             20 | -0.0104348  |          0.25 |                0.747629 | LOW                           | direction_mismatch_without_clean_robustness            | redesign_before_retest; inversion needs separate economic thesis                                |
| gap_continuation_confirmation_5_20            |              1 | -0.00609112 |          0    |                0.322287 | LOW                           | structurally_orthogonal_but_noisy_event_signal         | discard_current_form; redesign only if cleaner event coverage and lower turnover are available  |
| range_compression_breakout_continuation_20    |             20 | -0.00469198 |          0.5  |                0.450169 | LOW                           | orthogonal_but_weak_and_unstable_breakout_continuation | redesign_or_conditional_only; do not simply invert                                              |

## Horizon-Specific Behavior

| signal_name                                |   horizon | intended_direction               | empirical_direction   | direction_matches_intent   |      mean_ic |        ic_ir |   positive_ic_rate |   n_dates |
|:-------------------------------------------|----------:|:---------------------------------|:----------------------|:---------------------------|-------------:|-------------:|-------------------:|----------:|
| trend_leadership_persistence_20_60         |         1 | positive_continuation_or_quality | negative              | False                      | -7.12841e-05 | -0.000353342 |           0.529035 |      2032 |
| relative_strength_acceleration_20_60       |         1 | positive_continuation_or_quality | negative              | False                      | -0.00567556  | -0.029163    |           0.493857 |      2035 |
| range_compression_breakout_continuation_20 |         1 | positive_continuation_or_quality | negative              | False                      | -0.00220038  | -0.0164417   |           0.495571 |      2032 |
| liquidity_improvement_momentum_20_60       |         1 | positive_continuation_or_quality | negative              | False                      | -0.00317535  | -0.0167884   |           0.508285 |      2052 |
| gap_continuation_confirmation_5_20         |         1 | positive_continuation_or_quality | negative              | False                      | -0.00609112  | -0.0354603   |           0.49245  |      2053 |
| trend_leadership_persistence_20_60         |         5 | positive_continuation_or_quality | negative              | False                      | -0.0088351   | -0.0470971   |           0.491124 |      2028 |
| relative_strength_acceleration_20_60       |         5 | positive_continuation_or_quality | negative              | False                      | -0.00644195  | -0.0342466   |           0.483998 |      2031 |
| range_compression_breakout_continuation_20 |         5 | positive_continuation_or_quality | negative              | False                      | -0.00336327  | -0.0262404   |           0.486686 |      2028 |
| liquidity_improvement_momentum_20_60       |         5 | positive_continuation_or_quality | negative              | False                      | -0.0098556   | -0.0558577   |           0.485352 |      2048 |
| gap_continuation_confirmation_5_20         |         5 | positive_continuation_or_quality | negative              | False                      | -0.00328984  | -0.0199919   |           0.491459 |      2049 |
| trend_leadership_persistence_20_60         |        10 | positive_continuation_or_quality | negative              | False                      | -0.0136353   | -0.0747388   |           0.483935 |      2023 |
| relative_strength_acceleration_20_60       |        10 | positive_continuation_or_quality | negative              | False                      | -0.00690092  | -0.0393158   |           0.474334 |      2026 |
| range_compression_breakout_continuation_20 |        10 | positive_continuation_or_quality | negative              | False                      | -0.0027033   | -0.0217366   |           0.490855 |      2023 |
| liquidity_improvement_momentum_20_60       |        10 | positive_continuation_or_quality | negative              | False                      | -0.0135102   | -0.0816904   |           0.472834 |      2043 |
| gap_continuation_confirmation_5_20         |        10 | positive_continuation_or_quality | negative              | False                      | -0.00183041  | -0.0112791   |           0.502935 |      2044 |
| trend_leadership_persistence_20_60         |        20 | positive_continuation_or_quality | negative              | False                      | -0.0145526   | -0.0809824   |           0.505216 |      2013 |
| relative_strength_acceleration_20_60       |        20 | positive_continuation_or_quality | negative              | False                      | -0.011374    | -0.0685914   |           0.462302 |      2016 |
| range_compression_breakout_continuation_20 |        20 | positive_continuation_or_quality | negative              | False                      | -0.00469198  | -0.039584    |           0.483855 |      2013 |
| liquidity_improvement_momentum_20_60       |        20 | positive_continuation_or_quality | negative              | False                      | -0.0137547   | -0.0847988   |           0.484014 |      2033 |
| gap_continuation_confirmation_5_20         |        20 | positive_continuation_or_quality | negative              | False                      | -0.00460029  | -0.0294961   |           0.490167 |      2034 |

## Inverse Direction Test

The inverse direction mechanically flips IC signs, but this is not sufficient evidence to invert the candidates. The key question is whether the inverse is robust and structurally distinct. For most candidates, inversion raises reversal-proxy risk because the original panels were already strongly anti-correlated with reversal-like baselines or strongly correlated with momentum-like baselines.

| signal_name                                |   inverse_best_horizon |   horizon |   inverse_mean_ic |   inverse_ic_ir |   inverse_positive_ic_rate |   n_dates |
|:-------------------------------------------|-----------------------:|----------:|------------------:|----------------:|---------------------------:|----------:|
| gap_continuation_confirmation_5_20         |                      1 |         1 |        0.00609112 |       0.0354603 |                   0.50755  |      2053 |
| trend_leadership_persistence_20_60         |                     20 |        20 |        0.0145526  |       0.0809824 |                   0.494784 |      2013 |
| relative_strength_acceleration_20_60       |                     20 |        20 |        0.011374   |       0.0685914 |                   0.537698 |      2016 |
| range_compression_breakout_continuation_20 |                     20 |        20 |        0.00469198 |       0.039584  |                   0.516145 |      2013 |
| liquidity_improvement_momentum_20_60       |                     20 |        20 |        0.0137547  |       0.0847988 |                   0.515986 |      2033 |

## Similarity After Sign Inversion

Absolute similarity is unchanged by sign inversion, while signed correlation flips. High inverted correlation to reversal-like baselines means the inverse is likely another reversal proxy rather than a new mechanism.

| signal_name                                | top_abs_similarity_baseline              |   top_abs_similarity |   top_inverted_value_corr | top_reversal_like_baseline                 |   top_reversal_like_abs_similarity |   top_reversal_like_inverted_corr | inverse_reversal_proxy_risk   |
|:-------------------------------------------|:-----------------------------------------|---------------------:|--------------------------:|:-------------------------------------------|-----------------------------------:|----------------------------------:|:------------------------------|
| gap_continuation_confirmation_5_20         | track_a_volume_shock_reversal_stable_20  |             0.322287 |                  0.322287 | track_a_volume_shock_reversal_stable_20    |                           0.322287 |                          0.322287 | LOW                           |
| liquidity_improvement_momentum_20_60       | simple_volatility_reversal               |             0.939264 |                  0.939264 | simple_volatility_reversal                 |                           0.939264 |                          0.939264 | HIGH                          |
| range_compression_breakout_continuation_20 | v2_vol_compression_range_expansion_20_60 |             0.450169 |                 -0.450169 | plain_smoothed_reversal_20                 |                           0.352702 |                          0.352702 | LOW                           |
| relative_strength_acceleration_20_60       | v2_relative_value_mispricing_decay_20_60 |             1        |                  1        | plain_smoothed_reversal_20                 |                           0.755963 |                          0.755963 | HIGH                          |
| trend_leadership_persistence_20_60         | v2_dispersion_stable_leadership_60       |             0.827186 |                 -0.827186 | v2_flow_volatility_interaction_reversal_20 |                           0.729445 |                          0.729445 | MODERATE                      |

## Regime-Specific Behavior

No focus candidate showed a clean regime rescue. Stress regimes generally made the continuation direction more negative, especially panic/liquidity stress, volatility spikes, weak breadth, and drawdown acceleration.

| signal_name                                |   drawdown_acceleration |   high_dispersion_rotation |   panic_liquidity_stress |   recovery_phase |   trend_transition |   volatility_spike |   weak_breadth |
|:-------------------------------------------|------------------------:|---------------------------:|-------------------------:|-----------------:|-------------------:|-------------------:|---------------:|
| gap_continuation_confirmation_5_20         |               -0.005752 |                  -0.017162 |                -0.014994 |        -0.021773 |          -0.009366 |          -0.016345 |      -0.005738 |
| liquidity_improvement_momentum_20_60       |               -0.034879 |                  -0.005006 |                -0.053632 |        -0.013392 |          -0.004169 |          -0.027963 |      -0.031364 |
| range_compression_breakout_continuation_20 |               -0.017608 |                  -0.006696 |                -0.015621 |        -0.003054 |          -0.032122 |          -0.009176 |       0.001803 |
| relative_strength_acceleration_20_60       |               -0.015709 |                   0.013313 |                -0.012412 |        -0.000338 |           0.012559 |           0.006708 |      -0.005931 |
| trend_leadership_persistence_20_60         |               -0.033576 |                  -0.014663 |                -0.056589 |        -0.034905 |          -0.010169 |          -0.043963 |      -0.037133 |

## Turnover And Missingness

| signal_name                                |   missing_pct |   date_coverage |   turnover_proxy |   turnover_p95 |
|:-------------------------------------------|--------------:|----------------:|-----------------:|---------------:|
| trend_leadership_persistence_20_60         |     0.0426437 |        0.969018 |        0.0374141 |      0.0575191 |
| relative_strength_acceleration_20_60       |     0.0412158 |        0.970448 |        0.0704519 |      0.0983705 |
| range_compression_breakout_continuation_20 |     0.0331128 |        0.978551 |        0.0749345 |      0.131628  |
| liquidity_improvement_momentum_20_60       |     0.0334708 |        0.978551 |        0.0655714 |      0.0907341 |
| gap_continuation_confirmation_5_20         |     0.598506  |        0.98999  |        0.24093   |      0.419218  |

## Focus Candidate Findings

### gap_continuation_confirmation_5_20

- Most structurally distant from reversal by baseline correlation, but not usable in current form.
- Best horizon shifted to h1 rather than intended h5-h10, with negative IC.
- Missingness was very high and turnover was the highest in the batch.
- Inversion is not the main issue; the current event definition is sparse, noisy, and operationally unstable.
- Recommendation: discard current form; redesign only with cleaner event coverage, lower turnover, and explicit gap-continuation/gap-reversal separation.

### range_compression_breakout_continuation_20

- Structurally more distant than most candidates, with moderate/low baseline similarity.
- IC was weak, negative, and WFV-style sign consistency was poor.
- This looks less like a sign bug and more like false-breakout/late-entry decay.
- Recommendation: redesign or move to conditional-only research; do not simply invert.

### trend_leadership_persistence_20_60

- Formula matches continuation intent but behaved negatively at h20.
- Strong similarity to plain momentum and existing trend-quality references suggests limited orthogonality.
- Failure likely reflects overextension/crowding and late-entry momentum decay rather than a coding sign error.
- Recommendation: discard current standalone form; future work should avoid raw price-rank leadership as the primary signal.

### relative_strength_acceleration_20_60

- Negative across the main horizons and perfectly redundant with the deceleration-risk sibling in v3 construction.
- Max baseline similarity was effectively 1.0, so inversion would not create a clean new alpha.
- Recommendation: discard current form; any future acceleration work needs a fundamentally different design, such as sector-relative acceleration with explicit persistence controls.

### liquidity_improvement_momentum_20_60

- Liquidity improvement confirmed momentum did not separate from the price-rank manifold.
- Stress/regime slices were also negative, arguing against a conditional rescue in current form.
- Inversion would mostly behave like fading liquidity-confirmed leadership.
- Recommendation: redesign around non-price liquidity persistence or participation quality rather than using liquidity as a multiplier on momentum.

## Failure Mode Interpretation

- Signal construction sign error: not supported as the primary explanation. The formulas generally represent their documented intent.
- Crowding / overextension effect: strongly supported for leadership, participation, relative strength, liquidity-confirmed leadership, and volatility-normalization momentum.
- Late-entry momentum decay: supported by increasingly negative h10-h20 behavior for many candidates.
- Universe-specific behavior: plausible, but not proven without a broader universe comparison.
- Horizon mismatch: important for gap continuation and partly relevant for breakout continuation.
- Turnover/noise: severe for gap continuation; moderate but not primary for most others.
- Missingness/data quality: severe for gap continuation; acceptable for most others.
- Regime dependency: present, but not helpful; stress regimes mostly amplified negative direction.

## Recommendations Before v4

- Do not create v4 as a simple inversion batch.
- Do not refine v3 leadership/participation candidates by small parameter changes.
- Move away from raw price-rank leadership and price-confirmed participation as the main primitive.
- If sector or peer group data are available, test sector/peer-relative mechanisms that neutralize broad momentum/reversal exposure.
- For liquidity, use non-price persistence primitives before multiplying by momentum.
- For gap/breakout concepts, separate event detection quality from directional scoring and require lower missingness/turnover before IC testing.
- Treat conditional-only research as appropriate only for candidates with clear state-specific positive behavior; v3 did not show that pattern.

## Final Classification

| signal_name                                   | diagnosis                                              | primary_failure_drivers                                                                                                                               | recommended_action                                                                              |
|:----------------------------------------------|:-------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------|
| liquidity_deterioration_warning_20_60         | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; no_positive_regime_rescue                        | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| multi_horizon_trend_agreement_5_20_60         | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; no_positive_regime_rescue                        | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| vol_regime_transition_momentum_20_60          | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; no_positive_regime_rescue                        | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| trend_leadership_persistence_20_60            | direction_mismatch_without_clean_robustness            | broad_direction_mismatch; baseline_redundancy; weak_wfv_persistence; no_positive_regime_rescue                                                        | redesign_before_retest; inversion needs separate economic thesis                                |
| participation_trend_quality_interaction_20_60 | direction_mismatch_without_clean_robustness            | broad_direction_mismatch; baseline_redundancy; weak_wfv_persistence; no_positive_regime_rescue                                                        | redesign_before_retest; inversion needs separate economic thesis                                |
| liquidity_improvement_momentum_20_60          | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; no_positive_regime_rescue                        | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| breadth_participation_quality_20              | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; regime_dependency_negative_bias                  | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| relative_volume_confirmed_leadership_20       | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; regime_dependency_negative_bias                  | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| dispersion_transition_leadership_20_60        | direction_mismatch_without_clean_robustness            | horizon_specific_direction_mismatch; baseline_redundancy; weak_wfv_persistence; no_positive_regime_rescue                                             | redesign_before_retest; inversion needs separate economic thesis                                |
| relative_strength_acceleration_20_60          | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; regime_dependency_negative_bias                  | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| relative_strength_deceleration_risk_20_60     | continuation_collapsed_into_reversal_or_momentum_proxy | broad_direction_mismatch; baseline_redundancy; inverse_is_reversal_like_proxy; weak_wfv_persistence; regime_dependency_negative_bias                  | discard_or_rebuild_farther_from_price_rank_manifold; inversion is likely another reversal proxy |
| rank_persistence_quality_20_60                | direction_mismatch_without_clean_robustness            | horizon_specific_direction_mismatch; weak_wfv_persistence; no_positive_regime_rescue                                                                  | redesign_before_retest; inversion needs separate economic thesis                                |
| dispersion_compression_quality_20_60          | direction_mismatch_without_clean_robustness            | horizon_specific_direction_mismatch; weak_wfv_persistence; no_positive_regime_rescue                                                                  | redesign_before_retest; inversion needs separate economic thesis                                |
| gap_continuation_confirmation_5_20            | structurally_orthogonal_but_noisy_event_signal         | broad_direction_mismatch; weak_wfv_persistence; missingness_data_quality; turnover_noise; no_positive_regime_rescue; expected_h5_h10_horizon_mismatch | discard_current_form; redesign only if cleaner event coverage and lower turnover are available  |
| range_compression_breakout_continuation_20    | orthogonal_but_weak_and_unstable_breakout_continuation | broad_direction_mismatch; regime_dependency_negative_bias                                                                                             | redesign_or_conditional_only; do not simply invert                                              |
