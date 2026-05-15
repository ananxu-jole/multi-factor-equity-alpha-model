# Phase 2 Expansion Batch v1 Research Log

## Objective

Batch 1 tested a small set of expanded signal ideas against the existing Phase 2 research stack without relaxing gates, changing schemas, or modifying downstream pipeline logic. The purpose was to learn whether new signal families could add robust, low-correlation evidence to the existing alpha research universe.

This was a research iteration, not a survivor-forcing exercise. Failed signals are useful information. Conservative rejection is preferred over unstable alpha, and the goal is robustness rather than forcing candidates through downstream stages.

## Batch Scope

- Expansion batch: `phase2_expansion_batch_v1`
- Discovery version: `phase2_expanded_discovery_v1`
- Run id: `phase2_expansion_batch_v1_20260514_175410`
- Proposed signals: 7
- Structurally passing signals promoted into the main signal universe: 6
- Structurally rejected signals: 1
- Refreshed existing signals: 0
- Integration status: `SUCCESS`

The integration report states: `Structurally passing expansion-batch candidates promoted without changing downstream gates.`

No gates were relaxed during this batch.

## Implemented Signals

| Signal | Family | Structural Quality | Batch Integration Outcome | Discovery Preference Status |
| --- | --- | --- | --- | --- |
| `downside_vol_asymmetry_20` | `volatility_structure` | Failed | Not promoted | `REVIEW_OR_REJECT_EXPANDED_DISCOVERY` |
| `index_relative_reversal_5` | `residual_relative_value` | Passed | Promoted | `PROMOTE_EXPANDED_DISCOVERY` |
| `percentile_rank_stability_20` | `breadth_cross_sectional_context` | Passed | Promoted | `REVIEW_OR_REJECT_EXPANDED_DISCOVERY` |
| `smooth_trend_persistence_60` | `trend_quality` | Passed | Promoted | `REVIEW_OR_REJECT_EXPANDED_DISCOVERY` |
| `trend_consistency_20_60` | `trend_quality` | Passed | Promoted | `PROMOTE_EXPANDED_DISCOVERY` |
| `vol_compression_breakout_20_60` | `volatility_structure` | Passed | Promoted | `REVIEW_OR_REJECT_EXPANDED_DISCOVERY` |
| `volume_flow_ratio_5_20` | `liquidity_flow` | Passed | Promoted | `REVIEW_OR_REJECT_EXPANDED_DISCOVERY` |

The six structurally passing signals were promoted into the main signal universe for downstream research processing. Separately, only `index_relative_reversal_5` and `trend_consistency_20_60` passed the stricter expanded-discovery preference gate.

## Structural Quality Results

| Signal | Missing % | Finite % | First Valid Date | Last Valid Date | Result |
| --- | ---: | ---: | --- | --- | --- |
| `downside_vol_asymmetry_20` | 54.3740% | 45.6260% | 2018-02-08 | 2026-05-07 | Rejected |
| `index_relative_reversal_5` | 2.7018% | 97.2982% | 2018-01-31 | 2026-05-07 | Passed |
| `percentile_rank_stability_20` | 9.0556% | 90.9444% | 2018-03-07 | 2026-05-07 | Passed |
| `smooth_trend_persistence_60` | 9.9164% | 90.0836% | 2018-04-20 | 2026-05-07 | Passed |
| `trend_consistency_20_60` | 8.1739% | 91.8261% | 2018-04-20 | 2026-05-07 | Passed |
| `vol_compression_breakout_20_60` | 6.9487% | 93.0513% | 2018-03-08 | 2026-05-07 | Passed |
| `volume_flow_ratio_5_20` | 3.4922% | 96.5078% | 2018-02-06 | 2026-05-07 | Passed |

`downside_vol_asymmetry_20` was rejected because it failed structural quality: finite coverage was 45.6260% and missingness was 54.3740%, versus the structural gate requirement of finite coverage at or above 90% and missingness at or below 20%.

## Scoring Results

Best horizon and mean IC for the six promoted structural-pass signals:

| Signal | Best Horizon | Mean IC | Scoring Interpretation |
| --- | ---: | ---: | --- |
| `index_relative_reversal_5` | 5 | 0.012174 | Watchlist at horizon 5 |
| `percentile_rank_stability_20` | 20 | -0.017500 | Watchlist at horizons 10 and 20 as a reverse-direction edge |
| `smooth_trend_persistence_60` | 20 | -0.014922 | Watchlist at horizons 10 and 20 as a reverse-direction edge |
| `trend_consistency_20_60` | 20 | 0.018140 | Watchlist at horizons 10 and 20 |
| `vol_compression_breakout_20_60` | 10 | -0.009750 | Rejected low signal at all scored horizons |
| `volume_flow_ratio_5_20` | 1 | 0.002457 | Rejected low signal at all scored horizons |

The strongest raw scoring evidence came from `trend_consistency_20_60`, `percentile_rank_stability_20`, and `smooth_trend_persistence_60`, but scoring strength alone was not sufficient for downstream eligibility.

## Decay / Regime / Health Summary

At each promoted signal's best horizon:

| Signal | Decay Status | Decay Risk | Regime Fragility Summary | Health Outcome |
| --- | --- | --- | --- | --- |
| `index_relative_reversal_5` | `STABLE` | `LOW_DECAY_RISK` | High fragility across all four regime cuts | Rejected after WFV |
| `percentile_rank_stability_20` | `UNSTABLE` | `MODERATE_DECAY_RISK` | High fragility across all four regime cuts | Watchlist research only |
| `smooth_trend_persistence_60` | `UNSTABLE` | `MODERATE_DECAY_RISK` | High fragility across all four regime cuts | Watchlist research only |
| `trend_consistency_20_60` | `STABLE` | `LOW_DECAY_RISK` | Low to moderate fragility, no regime sign flips | Watchlist research after WFV rejection |
| `vol_compression_breakout_20_60` | `STABLE` | `LOW_DECAY_RISK` | Mostly high fragility | Rejected research |
| `volume_flow_ratio_5_20` | `STABLE` | `LOW_DECAY_RISK` | High fragility across all four regime cuts | Rejected research |

Health scoring did not convert any Batch 1 signal into a downstream-ready candidate. Across promoted signals and horizons, the health layer produced only `WATCHLIST_RESEARCH` or `REJECTED_RESEARCH` outcomes.

## Signal WFV Bridge Results

The controlled signal WFV bridge was applied only to the two primary allowlisted Batch 1 candidates:

- `trend_consistency_20_60`
- `index_relative_reversal_5`

The bridge worked correctly: it admitted the intended allowlisted candidates, applied the existing WFV gates, and rejected unstable edges as intended.

| Signal | Horizon | Windows | Mean Train IC | Mean Test IC | Effective Mean Test IC | Effective Test IC IR | Test Positive IC Rate | Sign Consistency | WFV Status | Exact WFV Rejection Reason |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `index_relative_reversal_5` | 5 | 4 | 0.015458 | -0.001037 | -0.001037 | -0.048619 | 0.750000 | 0.750000 | `REJECTED_WFV` | `direction flip; weak effective IC; weak effective IC IR` |
| `trend_consistency_20_60` | 20 | 4 | 0.021959 | 0.003626 | 0.003626 | 0.054964 | 0.250000 | 0.250000 | `REJECTED_WFV` | `weak effective IC; low persistence; low sign consistency` |

## Downstream Eligibility Outcome

No Batch 1 signal reached 04A eligibility.

The six structurally passing signals were useful research additions, but none survived the full evidence stack strongly enough to enter alpha construction. The WFV bridge rejected both primary bridge candidates, and the remaining promoted structural-pass signals remained research/watchlist or rejected candidates rather than downstream alpha-construction inputs.

## Key Findings

- Batch integration worked as intended: six structurally valid signals were promoted into the main signal universe, and one structurally weak signal was rejected.
- `downside_vol_asymmetry_20` failed for data coverage reasons, not because of a subtle predictive-quality issue.
- `trend_consistency_20_60` had the best positive mean IC among the promoted structural-pass signals, with best horizon 20 and mean IC 0.018140.
- `index_relative_reversal_5` showed a modest horizon-5 watchlist edge in scoring, but WFV exposed a direction flip and weak out-of-sample effective IC.
- The platform rejected unstable edges as intended. The bridge did not create downstream eligibility simply because a signal was promising in earlier scoring.
- No gates were relaxed, and no pipeline logic or schemas were changed for this research log.

## Lessons Learned

Failed signals are useful information. They identify data coverage limits, unstable regimes, weak out-of-sample behavior, and places where a hypothesis needs reformulation rather than promotion.

Conservative rejection is preferable to admitting unstable alpha. Batch 1 shows that preliminary IC strength, even when directionally interesting, must survive decay, regime, health, and WFV checks before it deserves downstream use.

The main research value of Batch 1 is diagnostic: trend-quality ideas appear more promising than pure liquidity-flow or volatility-compression variants, but the evidence is not yet robust enough for construction.

## Recommended Batch 2 Direction

Batch 2 should focus on fewer, more deliberate variants around the most informative Batch 1 areas:

- Refine trend-quality signals around `trend_consistency_20_60`, emphasizing persistence and sign consistency across walk-forward windows.
- Rework relative-reversal ideas to address WFV direction-flip risk before expanding the family further.
- Treat high-regime-fragility signals as diagnostic only unless the next design explicitly conditions on regime context.
- Deprioritize coverage-fragile constructions similar to `downside_vol_asymmetry_20` unless the formula can be redesigned to improve finite coverage materially.
- Avoid forcing weak liquidity-flow or volatility-compression signals into downstream testing until their raw scoring evidence improves.

The recommended Batch 2 posture is robustness-first: improve stability, coverage, and out-of-sample persistence before increasing the number of candidates.
