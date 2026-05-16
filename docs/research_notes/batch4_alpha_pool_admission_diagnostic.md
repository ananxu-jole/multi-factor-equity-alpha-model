# Batch 4 Alpha-Pool Admission Diagnostic

## Objective

This note traces `smooth_trend_persistence_60_low_breadth` at horizon `h20` after the Batch 4 LOW_BREADTH bridge to determine why it passed the signal research stack but did not appear in `alpha_signal_pool_current`.

This is a research-only diagnostic. No gates, schemas, thresholds, alpha construction logic, promotion logic, or pool outputs were modified.

## Signal Under Review

- Signal: `smooth_trend_persistence_60_low_breadth`
- Horizon: `20`
- Expansion batch: `phase2_expansion_batch_v4`
- Conditional context: `breadth_level_state=LOW_BREADTH`
- Bridge source: `conditional_edge_atlas_v1_low_breadth_audit`

## Trace Summary

| Stage | Table | Result |
|---|---|---|
| 03 scoring | `signal_scoring_gate_current` | `APPROVED_FOR_WFV` |
| 03B WFV bridge | `wfv_gate_current` | `APPROVED_WFV` |
| 03E health | `signal_health_score_current` | `APPROVED_FOR_RESEARCH` |
| 03F reproducibility | `signal_reproducibility_gate_current` | `APPROVED_FOR_ALPHA_RESEARCH` |
| 03G diversity | `signal_diversity_selection_current` | selected, `selected_flag = 1` |
| Alpha pool current | `alpha_signal_pool_current` | not present |

The signal completed the expected research path through 03G. The exclusion occurs after 03G, at the persisted alpha-pool artifact boundary.

## Stage Evidence

### 03 Scoring

`signal_scoring_gate_current` shows:

- `mean_ic`: `-0.050074`
- `abs_mean_ic`: `0.050074`
- `ic_ir`: `-0.241726`
- `abs_ic_ir`: `0.241726`
- `signal_direction`: `NEGATIVE_EDGE_REVERSE_SIGNAL`
- `signal_strength`: `STRONG`
- `status`: `APPROVED_FOR_WFV`

### 03B WFV Bridge

`wfv_gate_current` shows:

- `status`: `APPROVED_WFV`
- `effective_mean_test_ic`: `0.051455`
- `effective_test_ic_ir`: `0.225597`
- `persistence_ratio`: `0.75`
- `sign_consistency`: `0.75`
- `wfv_gate_notes`: `Meets strict direction-adjusted WFV thresholds.`

### 03E Health

`signal_health_score_current` shows:

- `signal_health_score`: `87`
- `signal_health_gate`: `APPROVED_FOR_RESEARCH`
- `wfv_status`: `APPROVED_WFV`
- `recommended_use`: `CONDITIONAL`
- `decay_status`: `INSUFFICIENT_DATA`
- `decay_risk_flag`: `LOW_DECAY_RISK`
- `regime_fragility_flag`: `HIGH_REGIME_FRAGILITY`
- `health_notes`: `Strong multi-diagnostic research candidate`

The signal is not blocked by health scoring.

### 03F Reproducibility

`signal_reproducibility_gate_current` shows:

- `reproducibility_status`: `GLOBAL_PASS`
- `final_research_gate`: `APPROVED_FOR_ALPHA_RESEARCH`
- `n_tests`: `14`
- `n_passed`: `12`
- `pass_rate`: `0.857143`
- `avg_effective_mean_ic`: `0.049249`
- `worst_effective_mean_ic`: `0.024262`

The signal is not blocked by reproducibility.

### 03G Diversity

`signal_diversity_selection_current` shows:

- `selected_flag`: `1`
- `selection_rank`: `1`
- `diversity_group`: `CORE_SELECTED`
- `diversity_candidate_tier`: `CORE_APPROVED`
- `selection_reason`: `Selected within correlation threshold 0.85.`

The signal is not blocked by diversity or redundancy limits.

## Exact Exclusion Stage

The exact exclusion stage is the persisted alpha-pool artifact, `alpha_signal_pool_current`.

The current alpha pool was last written by:

- `phase4a_alpha_construction_20260511_075950`

The Batch 4 LOW_BREADTH downstream stages were written later:

- WFV bridge: `phase2_signal_wfv_bridge_20260515_211744`
- 03E: `phase2_nb03e_signal_health_20260515_211800`
- 03F: `phase2_nb03f_signal_reproducibility_20260515_211809`
- 03G: `phase2_signal_diversity_20260515_212013`

Therefore, `alpha_signal_pool_current` is stale relative to the latest 03G output. The signal is absent because 04A alpha construction has not been rerun after the Batch 4 03G selection.

## Pool Logic Check

The alpha-pool builder in `src/alpha_construction.py` constructs the pool from:

- `signal_reproducibility_gate_current`
- `signal_health_score_current`
- `signal_decay_summary_current`
- `signal_regime_opportunity_summary_current`
- `signal_diversity_selection_current`
- `signal_diversity_similarity_current`

The core inclusion condition is:

- include rows where `final_research_gate == APPROVED_FOR_ALPHA_RESEARCH`, or
- include rows where `selected_flag == 1`

`smooth_trend_persistence_60_low_breadth` h20 satisfies both:

- `final_research_gate = APPROVED_FOR_ALPHA_RESEARCH`
- `selected_flag = 1`

A research-only in-memory evaluation of `build_alpha_signal_pool` using the current post-03G tables includes the signal as:

- `source_role`: `DIVERSITY_SELECTED`
- `pool_eligible_flag`: `1`
- `pool_reason`: `Selected by 03G diversity engine.`
- `pool_weight_base`: approximately `0.172902`

This confirms the current code path would admit the signal if 04A were refreshed against the latest inputs.

## Comparison To Current Alpha Pool

The persisted `alpha_signal_pool_current` contains four rows from an older 04A run:

| Signal | Horizon | Source Role | Pool Reason |
|---|---:|---|---|
| `vol_of_vol_20` | h10 | `DIVERSITY_SELECTED` | Selected by 03G diversity engine. |
| `range_expansion_failure_5` | h20 | `WATCHLIST_DIVERSIFIER` | Watchlist diversifier with stable decay and acceptable redundancy. |
| `residual_return_vs_universe_20` | h20 | `WATCHLIST_DIVERSIFIER` | Watchlist diversifier with stable decay and acceptable redundancy. |
| `vol_of_vol_20` | h20 | `WATCHLIST_DIVERSIFIER` | Watchlist diversifier with stable decay and acceptable redundancy. |

Those rows predate the Batch 4 bridge and post-bridge 03E/03F/03G refresh. They are not evidence that the Batch 4 signal failed an alpha-pool rule.

## Exclusion Cause Analysis

### Exact Exclusion Condition

The signal did not enter `alpha_signal_pool_current` because the current alpha-pool table was not regenerated after the signal became eligible. The exclusion is artifact-staleness, not a failed eligibility condition.

### Missing Metadata

No missing metadata was identified as the exclusion cause. The signal has the required downstream metadata:

- signal name and horizon
- family
- direction
- health score
- final research gate
- reproducibility status
- diversity selection metadata
- regime opportunity metadata
- decay metadata

### Family Or Diversity Limits

Family or diversity limits did not exclude the signal. 03G selected it with `selected_flag = 1`, `selection_rank = 1`, and `CORE_SELECTED`.

### Downstream WFV Expectations

Downstream WFV expectations did not exclude the signal. The signal has `APPROVED_WFV` and receives WFV credit in 03E.

### Conditional-Signal Disadvantage

The alpha-pool builder does not explicitly reject conditional signals. It does not inspect `conditional_context`, `conditional_source`, or `expansion_batch` as exclusion criteria.

However, the broader architecture is still universal-signal-oriented in two important ways:

- The pool is a global alpha-signal pool. It does not represent active-state eligibility, sparse-state coverage, or conditional activation windows as first-class pool concepts.
- Conditional signals can pass the current pool logic if they clear universal-style 03F/03G gates, but the pool does not yet distinguish universal alpha components from conditional alpha components.

So this specific exclusion was incidental/stale, not structural. The architecture remains mostly universal-signal-oriented once a signal enters alpha construction.

## Interpretation

The exclusion appears operationally incidental rather than conceptually intentional. The platform correctly withheld 04A+ because it was not requested after the Batch 4 03G result, and the persisted pool therefore still reflects the older 04A state.

Conceptually, `smooth_trend_persistence_60_low_breadth` h20 would be admitted by the current alpha-pool logic if 04A were rerun. That does not mean it should automatically be promoted into a live alpha. It means the research stack has advanced it to the point where alpha-construction research would be the next controlled step.

## Conclusion

Exact reason for exclusion:

- `alpha_signal_pool_current` is stale relative to the latest Batch 4 WFV, 03E, 03F, and 03G outputs.
- The current persisted alpha pool was written on `2026-05-11`.
- The Batch 4 LOW_BREADTH signal reached 03G selection on `2026-05-15`.
- No refreshed 04A alpha-construction run has written a new alpha pool since then.

Whether exclusion is conceptually correct:

- As an operational artifact, yes: without a 04A refresh, the current alpha pool should not silently update.
- As an eligibility judgment on the signal, no: the current input tables and pool logic would admit the signal.

Whether current alpha-pool architecture is universal-signal-oriented:

- Yes, broadly. The pool can include conditional signals, but it does not yet model conditional-alpha state activation as a separate research object.

Whether future conditional-alpha framework research is justified:

- Yes. Batch 4 shows that a sparse conditional signal can pass the universal-style research stack, but the next research layer should distinguish conditional activation, active-state coverage, and conditional alpha construction from universal signal pooling.
