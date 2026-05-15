# Phase 2 Expansion Batch v2 Research Log

## Objective

Batch 2 refined the strongest failed Batch 1 ideas without relaxing gates or changing downstream eligibility standards. The goal was to test whether simple, OHLCV-only variants could improve persistence, sign consistency, regime stability, and effective IC robustness.

This batch focused on refinement rather than broad exploration. The intent was to learn whether conservative adjustments to trend consistency and index-relative reversal could survive the existing evidence stack.

## Batch 2 Candidates

| Signal | Family | Refinement Source | Targeted Failure Mode |
| --- | --- | --- | --- |
| `trend_consistency_20_60_persistent` | `trend_quality` | `trend_consistency_20_60` | Low persistence, low sign consistency, weak effective IC |
| `index_relative_reversal_5_vol_adj` | `residual_relative_value` | `index_relative_reversal_5` | Direction flip, weak effective IC IR, regime instability |
| `index_relative_reversal_5_confirmed` | `residual_relative_value` | `index_relative_reversal_5` | Direction flip, low sign consistency, weak effective IC |

All three candidates were tagged with `expansion_batch = phase2_expansion_batch_v2`.

## Why These Variants Were Chosen

Batch 1 showed that the base trend and reversal ideas had some preliminary signal evidence but failed under walk-forward validation. The refinements were chosen to address those failure modes directly:

- `trend_consistency_20_60_persistent` added a minimal recent confirmation layer to reduce unstable trend-consistency readings.
- `index_relative_reversal_5_vol_adj` scaled index-relative reversal by realized volatility to reduce noisy high-volatility reversals.
- `index_relative_reversal_5_confirmed` added a small delayed-entry confirmation to avoid ranking names most strongly while relative underperformance was still worsening.

The designs remained OHLCV-only, high coverage, computationally reasonable, and low parameter-sprawl.

## Structural Quality Results

All three Batch 2 signals passed structural quality.

| Signal | Missingness | Finite % | Structural Result | Best Discovery Horizon | Discovery Mean IC |
| --- | ---: | ---: | --- | ---: | ---: |
| `index_relative_reversal_5_confirmed` | 0.029225 | 0.970775 | Passed | 5 | 0.011738 |
| `index_relative_reversal_5_vol_adj` | 0.029225 | 0.970775 | Passed | 5 | 0.011611 |
| `trend_consistency_20_60_persistent` | 0.044531 | 0.955469 | Passed | 20 | 0.012815 |

The final integration report recorded `3` Batch 2 signals, `3` structural passes, and `3` promoted signals.

## 03 Scoring Results

Only `trend_consistency_20_60_persistent` reached `WATCHLIST`, at horizon 20.

| Signal | Best Horizon | Mean IC | Abs Mean IC | 03 Outcome |
| --- | ---: | ---: | ---: | --- |
| `index_relative_reversal_5_confirmed` | 5 | 0.011738 | 0.011738 | `REJECTED_LOW_SIGNAL` |
| `index_relative_reversal_5_vol_adj` | 5 | 0.011611 | 0.011611 | `REJECTED_LOW_SIGNAL` |
| `trend_consistency_20_60_persistent` | 20 | 0.012815 | 0.012815 | `WATCHLIST` |

Batch 2 scoring gate counts across all candidate horizons:

- `WATCHLIST`: 1
- `APPROVED`: 0
- `REJECTED_LOW_SIGNAL`: 11

The reversal refinements remained below preliminary predictive scoring thresholds despite passing structural quality.

## Decay / Regime Observations

At the scored horizons, all three candidates generally showed stable decay behavior at shorter horizons. The two reversal variants were `STABLE` and `LOW_DECAY_RISK` at horizons 1, 5, and 10, but became `UNSTABLE` with `MODERATE_DECAY_RISK` at horizon 20.

`trend_consistency_20_60_persistent` was `STABLE` and `LOW_DECAY_RISK` across horizons 1, 5, 10, and 20. However, regime results remained mostly conditional rather than broadly robust. The h20 trend variant had conditional regime opportunity, with high or moderate fragility depending on the regime cut.

The regime layer did not establish a clean unconditional edge. This was an important warning before WFV.

## Controlled 03B WFV Bridge Result

The controlled 03B WFV bridge tested only `trend_consistency_20_60_persistent` at horizon 20.

The bridge did not include:

- `index_relative_reversal_5_confirmed`
- `index_relative_reversal_5_vol_adj`

Existing WFV windows, purge/embargo, thresholds, gates, and schemas were preserved. No gate was relaxed.

| Signal | Horizon | WFV Status | Mean Train IC | Mean Test IC | Effective Mean Test IC | Effective Test IC IR | Persistence | Sign Consistency |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `trend_consistency_20_60_persistent` | 20 | `REJECTED_WFV` | 0.014645 | 0.000734 | 0.000734 | 0.012460 | 0.250000 | 0.250000 |

Exact WFV rejection reason:

`weak effective IC; weak effective IC IR; low persistence; low sign consistency`

## Health Result After WFV

After rerunning 03E signal health, `trend_consistency_20_60_persistent` remained a watchlist research item, not an approved research signal.

| Signal | Horizon | WFV Status | Health Score | Health Gate | Notes |
| --- | ---: | --- | ---: | --- | --- |
| `trend_consistency_20_60_persistent` | 20 | `REJECTED_WFV` | 58.000 | `WATCHLIST_RESEARCH` | `Mixed evidence; monitor before promotion; WFV rejected` |

It did not become `APPROVED_FOR_RESEARCH`.

## 03F / 03G / Alpha Pool Outcome

After rerunning 03F signal reproducibility:

- `trend_consistency_20_60_persistent` did not enter `signal_reproducibility_gate_current`.
- It did not receive an approved or watchlist alpha-research reproducibility outcome in the current table.

After rerunning 03G signal diversity:

- `trend_consistency_20_60_persistent` did not enter `signal_diversity_selection_current`.

Alpha pool outcome:

- `trend_consistency_20_60_persistent` had `0` rows in `alpha_signal_pool_current`.
- It did not reach alpha pool eligibility.
- 04A+ was not run.

## Final Conclusion

Batch 2 improved structural quality and kept the formulas simple, but it did not produce a downstream-eligible signal. The strongest candidate, `trend_consistency_20_60_persistent`, reached 03 `WATCHLIST` but failed controlled WFV on the same core issues Batch 2 was designed to improve: weak effective IC, weak effective IC IR, low persistence, and low sign consistency.

The platform behaved correctly. It allowed structurally valid refinements into research, scored them, admitted only the watchlist candidate to a controlled bridge, and rejected the unstable out-of-sample edge without relaxing gates.

## Lessons Learned

- Structural quality is necessary but not sufficient. All three candidates had high coverage, but only one reached 03 `WATCHLIST`.
- Simple confirmation and volatility adjustment did not materially fix the reversal family. Both reversal variants remained below scoring thresholds.
- The trend refinement improved presentation enough to reach `WATCHLIST`, but WFV showed that the edge was still not persistent out of sample.
- Regime-conditional evidence should not be mistaken for robust unconditional alpha.
- Conservative rejection prevented a fragile refinement from entering alpha construction.

## Batch 3 Recommendation

Batch 3 should not continue small mechanical tweaks to the same formulas. The next research iteration should either:

- Develop genuinely different trend-quality definitions with stronger out-of-sample persistence tests built into the design, or
- Move to a diagnostic-only regime-context study that explains where the trend-consistency edge appears and why it fails outside those states.

Recommended Batch 3 direction:

- Keep candidate count small.
- Require high structural coverage from the start.
- Favor signals whose expected behavior is stable across WFV windows, not merely strong in aggregate IC.
- Avoid adding regime gates as a shortcut to eligibility.
- Do not bridge reversal refinements unless they first clear 03 scoring thresholds.

The priority remains robustness, not forcing survivors.
