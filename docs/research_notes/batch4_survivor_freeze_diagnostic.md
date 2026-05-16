# Batch 4 Survivor Freeze Diagnostic

## Objective

This note documents a focused diagnostic of the `08_survivor_freeze` stage to explain why the current surviving alpha candidates were classified as `REVIEW_SATELLITE` rather than `PROMOTE_CORE`.

The diagnostic is research-only. No gates, schemas, alpha construction logic, promotion logic, or upstream stages were modified or rerun.

## Tables Reviewed

The diagnostic reviewed the current persisted outputs for:

- `survivor_alpha_registry_current`
- `survivor_freeze_report_current`
- `survivor_validation_report_current`
- `survivor_cluster_summary_current`
- `survivor_alpha_correlation_current`
- `alpha_stress_gate_current`
- `alpha_stress_summary_current`
- `alpha_stress_audit_summary_current`
- Current portfolio construction thresholds and downstream portfolio tables

The current survivor freeze run is:

- `run_id`: `phase8_cluster_aware_survivor_20260515_224443`
- `survivor_version`: `phase8_cluster_aware_survivor_v5`
- `date_frozen`: `2026-05-15`

## Executive Finding

No alpha reached `PROMOTE_CORE` because the only alpha that survived 07 stress was not a core-quality survivor under the current stress and survivor-freeze rules.

The sole `APPROVED_STRESS` alpha was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth`
- horizon: `h20`
- stress status: `APPROVED_STRESS`
- survivor tier: `WATCH_STRESS_SURVIVOR`
- original promotion decision: `REVIEW_SATELLITE`
- final promotion decision: `REVIEW_SATELLITE`
- final status: `SATELLITE_WATCHLIST`

The primary blockers were:

1. Stress pass rate was below the core survivor threshold.
2. Turnover risk was moderate, not low.
3. Survivor selection score was below the cluster-aware freeze threshold.
4. Worst degradation was close to the catastrophic degradation boundary.

This was not primarily caused by portfolio exposure, concentration, or downstream portfolio construction metrics.

## 07 Stress Survivor Analysis

The current stress gate produced six tracked constructed alpha rows. Only one was `APPROVED_STRESS`:

| Alpha | Horizon | Stress Status | Survivor Tier | Promotion Decision | Pass Rate | Worst Degradation | Avg Turnover Proxy | Turnover Risk |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| `alpha_orthogonal_diversifier_v2_score_weighted_smooth` | 20 | `APPROVED_STRESS` | `WATCH_STRESS_SURVIVOR` | `REVIEW_SATELLITE` | 0.777778 | 0.788569 | 1.937273 | `MODERATE_TURNOVER_RISK` |

The stress survivor-tier logic requires:

- `APPROVED_STRESS`
- pass rate at least `0.90` before a survivor can become a core or balanced stress survivor
- `LOW_TURNOVER_RISK` for `CORE_STRESS_SURVIVOR`
- `MODERATE_TURNOVER_RISK` for `BALANCED_STRESS_SURVIVOR`

Because the approved alpha had pass rate `0.777778`, it was assigned `WATCH_STRESS_SURVIVOR`, not `CORE_STRESS_SURVIVOR` or `BALANCED_STRESS_SURVIVOR`.

This directly prevented `PROMOTE_CORE`.

## 08 Survivor Freeze Results

The current `survivor_alpha_registry_current` contains five tracked rows:

| Alpha | Horizon | Final Decision | Final Status | Score | Cluster Role | Cluster Reason |
| --- | ---: | --- | --- | ---: | --- | --- |
| `alpha_orthogonal_diversifier_v2_score_weighted_smooth` | 20 | `REVIEW_SATELLITE` | `SATELLITE_WATCHLIST` | 28.377197 | `WEAK_SCORE_WATCHLIST` | `Score below MIN_CLUSTER_SCORE 40.` |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `REVIEW_SATELLITE` | `SATELLITE_WATCHLIST` | 13.005864 | `WEAK_SCORE_WATCHLIST` | `Score below MIN_CLUSTER_SCORE 40.` |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `REVIEW_SATELLITE` | `SATELLITE_WATCHLIST` | 11.871447 | `WEAK_SCORE_WATCHLIST` | `Score below MIN_CLUSTER_SCORE 40.` |
| `alpha_persistence_blend_v2` | 10 | `REJECT_HIGH_TURNOVER` | `REJECTED_HIGH_TURNOVER` | -155.493455 | `HIGH_TURNOVER_TRACKING_ONLY` | High-turnover tracking only |
| `alpha_diversified_research_v2` | 20 | `REJECT_HIGH_TURNOVER` | `REJECTED_HIGH_TURNOVER` | -162.044211 | `HIGH_TURNOVER_TRACKING_ONLY` | High-turnover tracking only |

The freeze report states:

- `n_survivors`: `0`
- survivor names: empty
- note: no stress-approved survivor alphas were frozen

The validation report explicitly failed:

- `at_least_one_final_core`
- detail: `Final PROMOTE_CORE rows: 0`

All other survivor-freeze validation checks passed.

## Exact PROMOTE_CORE Blockers

### 1. Stress pass rate below core threshold

The only `APPROVED_STRESS` alpha had pass rate `0.777778`.

The stress survivor-tier logic assigns `WATCH_STRESS_SURVIVOR` when pass rate is below `0.90`. Therefore, despite passing stress overall, the alpha did not qualify for `CORE_STRESS_SURVIVOR`.

This is the main reason the alpha entered 08 as `REVIEW_SATELLITE`.

### 2. Moderate turnover risk

The same alpha had:

- `avg_turnover_proxy`: `1.937273`
- `turnover_risk_flag`: `MODERATE_TURNOVER_RISK`

Moderate turnover was not a hard rejection. However, even with a pass rate above `0.90`, moderate turnover would route the alpha toward `BALANCED_STRESS_SURVIVOR`, not `CORE_STRESS_SURVIVOR`.

Therefore turnover was a secondary blocker for `PROMOTE_CORE`, but not the reason the alpha was rejected from the registry.

### 3. Survivor selection score below cluster threshold

The 08 survivor selection score penalizes weak stress strength, degradation, turnover, and satellite status:

```text
score =
  100 * pass_rate
  - 25 * worst_degradation
  - 5 * avg_turnover_proxy
  + 20 if PROMOTE_CORE
  - 20 if REVIEW_SATELLITE
  - 50 if HIGH_TURNOVER_RISK
```

For `alpha_orthogonal_diversifier_v2_score_weighted_smooth`, this produced:

- survivor selection score: `28.377197`
- required cluster-aware threshold: `MIN_CLUSTER_SCORE = 40`

The resulting cluster role was:

- `WEAK_SCORE_WATCHLIST`

This confirms that 08 did not have enough evidence to upgrade the alpha into a final core survivor.

### 4. Drawdown / stress degradation near the boundary

The approved stress survivor had:

- `worst_degradation`: `0.788569`

This was below the catastrophic degradation rejection boundary, but close enough to materially reduce the survivor selection score.

The alpha survived 07, but the degradation profile supports satellite treatment rather than core promotion.

## Turnover, Drawdown, Exposure, and Concentration Assessment

### Turnover

Turnover mattered in two ways:

- The surviving alpha carried `MODERATE_TURNOVER_RISK`, which prevents core-tier classification under the stress survivor-tier model.
- Two other tracked alphas were explicitly rejected as `REJECT_HIGH_TURNOVER`:
  - `alpha_persistence_blend_v2`
  - `alpha_diversified_research_v2`

Turnover was therefore a meaningful contributor, but the exact primary blocker for the surviving alpha was pass rate below `0.90`.

### Drawdown / degradation

The surviving alpha did not fail catastrophic degradation, but its `worst_degradation` of `0.788569` was high enough to reduce the 08 selection score materially.

`alpha_regime_blend_dynamic_v4_smooth` had `worst_degradation = 0.803514` and was rejected by stress, despite a pass rate of `0.722222`.

### Exposure and concentration

Exposure and concentration did not directly block `PROMOTE_CORE` in 08. The survivor-freeze stage uses stress status, survivor tier, turnover risk, selection score, behavior cluster, and alpha correlations.

Portfolio construction thresholds are:

- `MAX_ABS_WEIGHT = 0.05`
- `TOP_QUANTILE = 0.20`
- `BOTTOM_QUANTILE = 0.20`
- `GROSS_EXPOSURE = 1.0`
- `REBALANCE_FREQUENCY = 5`
- `COST_BPS = 5`
- `EXECUTION_LAG = 1`

Current persisted portfolio tables are older than the latest survivor freeze run, so they should be treated as historical portfolio context rather than the causal source of the 08 decision.

### Stress audit summary

The stress audit summary confirms the same classification:

- one `APPROVED_STRESS` alpha
- two `WATCHLIST_STRESS` alphas
- three `REJECTED_STRESS` alphas, including two high-turnover rejects

The 08 registry retained this structure rather than forcing a core survivor.

## Correlation and Cluster Review

The 08 correlation-aware registry did not fail because of an overcrowded core set. There were no final core alphas.

Observed review-satellite correlations:

- `alpha_decay_aware_dynamic_v4_smooth` vs `alpha_hybrid_adaptive_v4_smooth`: abs correlation `0.972319`
- both had low absolute correlation with `alpha_orthogonal_diversifier_v2_score_weighted_smooth`, around `0.04` to `0.05`

The surviving alpha was not blocked by correlation. It was retained as a weak-score satellite.

## Relationship to `smooth_trend_persistence_60_low_breadth`

The current `alpha_signal_pool_current` does include `smooth_trend_persistence_60_low_breadth`, including an eligible and selected `h20` row.

However, the sole 07 stress-approved alpha was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth`

Its construction metadata lists these component signals:

- `vol_surprise_20_60`
- `price_impact_proxy_20`
- `range_expansion_failure_5`
- `liquidity_adjusted_reversal_5`

It does not include `smooth_trend_persistence_60_low_breadth`.

Some other constructed alphas did include `smooth_trend_persistence_60_low_breadth`, including dynamic and smooth variants, but those did not become the final stress-approved survivor that drove the 08 freeze result.

Therefore, the surviving 07 stress alpha does not include `smooth_trend_persistence_60_low_breadth`.

## Conditional Activation Sparsity

Conditional activation sparsity was not the direct reason the current 08 survivor was classified as `REVIEW_SATELLITE`, because the only stress-approved survivor did not include the LOW_BREADTH conditional signal.

That said, the downstream architecture remains oriented toward broad constructed alphas:

- 08 freezes constructed alpha candidates, not raw conditional signal activation profiles.
- 09 portfolio construction selects only final `PROMOTE_CORE` survivor rows.
- The portfolio layer expects a continuous enough alpha panel to support top/bottom quantile selection and stable gross exposure.

This means sparse conditional alphas may be structurally disadvantaged unless they are first translated into constructed alphas that meet broad survivor and portfolio requirements, or unless a separate conditional-alpha framework is introduced later.

## Portfolio-Construction Philosophy

The current portfolio construction path is implicitly designed for broad universal or broad constructed alphas.

Evidence:

- 09 selects only `promotion_decision_final == PROMOTE_CORE`.
- It raises an error if `survivor_alpha_registry_current` has no final `PROMOTE_CORE` alpha rows.
- It uses broad top-quantile and bottom-quantile portfolio formation.
- It does not treat sparse conditional activation metadata as a first-class portfolio input.

This philosophy is conservative and consistent with the rest of the validation stack. It avoids allowing a stress-approved but weak-score satellite to become a portfolio core alpha.

## Diagnostic Classification

| Potential Cause | Finding |
| --- | --- |
| Turnover | Secondary contributor. The surviving alpha had `MODERATE_TURNOVER_RISK`; two other alphas were rejected for high turnover. |
| Concentration | Not causal in 08. No evidence that concentration blocked promotion. |
| Instability | Meaningful. Pass rate was below core threshold and degradation was high. |
| Stress weakness | Primary driver. The only stress-approved alpha had pass rate `0.777778`, below the `0.90` core-tier threshold. |
| Conditional activation sparsity | Not directly causal for the surviving alpha. The survivor did not include `smooth_trend_persistence_60_low_breadth`. |
| Portfolio philosophy | Important downstream context. Current portfolio construction requires final `PROMOTE_CORE` rows and is broad-alpha oriented. |

## Conceptual Assessment

`REVIEW_SATELLITE` appears conceptually correct.

The surviving alpha passed stress, but it did not show enough consistency, turnover quality, or degradation resilience to justify core promotion:

- pass rate was materially below `0.90`
- turnover risk was moderate
- worst degradation was close to the catastrophic threshold
- survivor selection score was below `MIN_CLUSTER_SCORE = 40`

The framework is behaving as intended. It preserved the candidate for monitoring while refusing to promote it into a core portfolio survivor.

The outcome is conservative, but not incidental. It reflects the intended portfolio-construction philosophy: core alpha promotion requires robust, broad, stress-resilient evidence, not merely a single stress-approved candidate.

## Final Conclusion

The 08 survivor-freeze stage classified the surviving alpha as `REVIEW_SATELLITE` because it was a stress survivor only in a watchlist sense. It passed 07 stress but failed the stricter core-survivor profile required for portfolio promotion.

The exact conditions preventing `PROMOTE_CORE` were:

1. `pass_rate = 0.777778`, below the `0.90` core survivor-tier threshold.
2. `turnover_risk_flag = MODERATE_TURNOVER_RISK`, not `LOW_TURNOVER_RISK`.
3. `survivor_selection_score = 28.377197`, below `MIN_CLUSTER_SCORE = 40`.
4. `worst_degradation = 0.788569`, close to the catastrophic degradation boundary and score-negative.

The surviving alpha was `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`. It did not include `smooth_trend_persistence_60_low_breadth`.

No gate relaxation or forced promotion is recommended. Future conditional-alpha work remains justified, but it should be handled as a separate research framework rather than by weakening the current universal/core survivor path.
