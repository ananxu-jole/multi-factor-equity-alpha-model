# Robustness-First Orthogonal Discovery Batch

## 1. Executive Takeaway

This note documents a research-only robustness-first orthogonal standalone discovery batch for Project Underdog.

The batch followed the restart plan after the LOW_BREADTH Conditional-Alpha cycle. It explored nine temporary OHLCV-only candidate formulas across:

- liquidity-flow structures
- volatility-structure signals
- residual / relative-value structures

Final batch outcome:

- 3 research survivor candidates
- 0 production survivor changes
- 0 gate/schema/threshold changes
- 0 Conditional-Alpha implementation changes

Research survivor candidates:

| Candidate | Family | Best Horizon | Sidecar WFV Effective Test IC | Sidecar WFV IR | Primary Reason |
| --- | --- | ---: | ---: | ---: | --- |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | h20 | 0.026315 | 0.921072 | strongest orthogonal liquidity-flow window stability |
| `residual_momentum_stability_60` | `residual_relative_value` | h20 | 0.050378 | 0.559240 | strongest stress/downtrend residual behavior |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | h20 | 0.044034 | 0.628899 | highly orthogonal volatility-structure WFV behavior |

Important caveat:

These are research survivor candidates only. They were evaluated in a sidecar batch, not registered into the production signal factory, not admitted into official WFV, and not promoted into any survivor/watchlist table.

Final recommendation:

`Run a targeted robustness refinement and controlled implementation pass for the three research survivor candidates only.`

## 2. Discovery Philosophy Summary

The batch prioritized:

- robustness over novelty
- orthogonality over raw IC
- persistence over unstable responsiveness
- stress coherence over headline in-sample IC
- attribution clarity over blend camouflage

The batch avoided:

- conditional-alpha semantics
- LOW_BREADTH reuse
- production gate changes
- schema changes
- ML layers
- portfolio construction changes
- broad speculative candidate sprawl

The design goal was to find standalone candidates that could plausibly complement the current trend-quality/conditional-heavy alpha pool.

## 3. Candidate Families Explored

Nine temporary candidates were generated.

| Candidate | Family | Intended Behavior | Expected Horizon | Expected Failure Mode |
| --- | --- | --- | --- | --- |
| `liquidity_adjusted_reversal_persistence_10` | `liquidity_flow` | liquidity-adjusted short reversal with persistence smoothing | h5-h10 | high turnover / cost sensitivity |
| `price_impact_decay_10_20` | `liquidity_flow` | reversal in decaying price impact between 10d and 20d windows | h10-h20 | noisy impact proxy |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | smoothed reversal after return-volume shock | h5-h20 | shock timing instability |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | reversal of 20d returns when realized volatility is elevated vs 60d | h10-h20 | generic risk-off duplication |
| `range_compression_quality_20_60` | `volatility_structure` | stable range compression without breakout chasing | h10-h20 | over-smoothing / low IC |
| `vol_of_vol_residual_stability_20` | `volatility_structure` | low vol-of-vol stability as defensive standalone structure | h10-h20 | defensive exposure mistaken for alpha |
| `beta_adjusted_residual_reversal_20` | `residual_relative_value` | benchmark beta-adjusted residual reversal | h10-h20 | beta leakage / direction flips |
| `residual_momentum_stability_60` | `residual_relative_value` | stabilized residual momentum over 60d | h20 | slow response |
| `relative_value_stability_20_60` | `residual_relative_value` | relative under/over-performance mean reversion with stability anchor | h10-h20 | reversal redundancy / crowding |

All candidates were evaluated as standalone temporary panels. None were added to production signal definitions.

## 4. Structural Review Summary

Structural quality was acceptable for research-sidecar evaluation, but not uniformly production-ready.

| Candidate | Missing % | Active Date Ratio | Turnover Proxy | Structural Comment |
| --- | ---: | ---: | ---: | --- |
| `liquidity_adjusted_reversal_persistence_10` | 40.28% | 99.52% | 0.175947 | usable but turnover-sensitive |
| `price_impact_decay_10_20` | 43.05% | 99.05% | 0.192119 | usable but noisy/high turnover |
| `volume_shock_reversal_stable_20` | 40.29% | 99.48% | 0.200726 | highest turnover among survivors |
| `volatility_surprise_reversal_20_60_smooth` | 43.60% | 98.47% | 0.085515 | structurally cleanest survivor |
| `range_compression_quality_20_60` | 43.35% | 98.62% | 0.154901 | structurally acceptable, weak score |
| `vol_of_vol_residual_stability_20` | 41.94% | 97.62% | 0.068339 | low turnover, weak IC |
| `beta_adjusted_residual_reversal_20` | 43.33% | 98.52% | 0.083176 | low turnover, weak WFV |
| `residual_momentum_stability_60` | 47.16% | 95.76% | 0.085346 | lower coverage but stable enough for research |
| `relative_value_stability_20_60` | 45.52% | 97.66% | 0.142277 | strongest full-sample IC but WFV failed |

Early structural rejection was not applied solely on missingness because the missingness comes largely from rolling-window requirements and the sidecar universe has enough active dates for research scoring.

Production implementation would still need normal structural gates.

## 5. Multi-Horizon Findings

Absolute mean IC by horizon:

| Candidate | h1 | h5 | h10 | h20 | Best Horizon |
| --- | ---: | ---: | ---: | ---: | ---: |
| `beta_adjusted_residual_reversal_20` | 0.000219 | 0.003507 | 0.006137 | 0.010162 | h20 |
| `liquidity_adjusted_reversal_persistence_10` | 0.007332 | 0.010505 | 0.004961 | 0.004757 | h5 |
| `price_impact_decay_10_20` | 0.000102 | 0.004244 | 0.009863 | 0.012747 | h20 |
| `range_compression_quality_20_60` | 0.000023 | 0.001931 | 0.002115 | 0.002502 | h20 |
| `relative_value_stability_20_60` | 0.007499 | 0.009059 | 0.011929 | 0.017296 | h20 |
| `residual_momentum_stability_60` | 0.004089 | 0.002960 | 0.007820 | 0.008709 | h20 |
| `vol_of_vol_residual_stability_20` | 0.001030 | 0.001915 | 0.001601 | 0.003909 | h20 |
| `volatility_surprise_reversal_20_60_smooth` | 0.000370 | 0.000917 | 0.000343 | 0.002292 | h20 |
| `volume_shock_reversal_stable_20` | 0.000656 | 0.004518 | 0.007918 | 0.009036 | h20 |

Main observations:

- h20 dominated the batch, consistent with the restart-plan expectation that robust standalone structures should avoid very short-lived IC bursts.
- `liquidity_adjusted_reversal_persistence_10` was the only best h5 candidate, but sidecar WFV did not support it.
- `relative_value_stability_20_60` had the strongest full-sample IC but failed WFV, a useful warning against raw IC chasing.
- `volatility_surprise_reversal_20_60_smooth` had weak full-sample IC but strong WFV-style window behavior, making it a classic "moderate edge, robust windows" candidate.

Direction stability:

- `volume_shock_reversal_stable_20` and `relative_value_stability_20_60` were directionally consistent across horizons.
- `residual_momentum_stability_60` flipped between h1 and longer horizons but was coherent at h10/h20.
- volatility-structure candidates had more sign instability, especially at short horizons.
- `range_compression_quality_20_60` showed sign inconsistency and weak IC.

## 6. WFV Findings

The sidecar WFV-style review used existing WFV windows and direction-adjusted test IC for each candidate's best horizon. This was not official WFV and did not write production tables.

| Candidate | Best Horizon | Effective Test IC | Effective Test IC IR | Positive Window Rate | Sidecar Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `volume_shock_reversal_stable_20` | h20 | 0.026315 | 0.921072 | 0.75 | `ROBUSTNESS_APPROVED_CANDIDATE` |
| `residual_momentum_stability_60` | h20 | 0.050378 | 0.559240 | 0.75 | `ROBUSTNESS_APPROVED_CANDIDATE` |
| `volatility_surprise_reversal_20_60_smooth` | h20 | 0.044034 | 0.628899 | 0.75 | `ROBUSTNESS_APPROVED_CANDIDATE` |
| `vol_of_vol_residual_stability_20` | h20 | 0.009541 | 0.212623 | 0.25 | `REJECT` |
| `beta_adjusted_residual_reversal_20` | h20 | 0.006370 | 0.068326 | 0.50 | `REJECT` |
| `range_compression_quality_20_60` | h20 | 0.000853 | 0.022014 | 0.50 | `REJECT` |
| `liquidity_adjusted_reversal_persistence_10` | h5 | -0.001818 | -0.069280 | 0.50 | `REJECT` |
| `price_impact_decay_10_20` | h20 | -0.004365 | -0.076587 | 0.50 | `REJECT` |
| `relative_value_stability_20_60` | h20 | -0.016057 | -0.176215 | 0.50 | `REJECT` |

Interpretation:

- The strongest full-sample IC candidate was not the strongest WFV candidate.
- Three candidates showed stable moderate-to-strong window evidence.
- The batch successfully separated raw IC candidates from robustness candidates.

## 7. Orthogonality Findings

Correlation was measured against current alpha-pool signal panels using cross-sectional rank panels.

Key observations:

- `volume_shock_reversal_stable_20` had very low maximum absolute correlation to current pool signals: 0.081847.
- `volatility_surprise_reversal_20_60_smooth` also had very low maximum absolute correlation: 0.084469.
- `residual_momentum_stability_60` had higher correlation to LOW_BREADTH trend-quality exposure: 0.528787, but still below a hard redundancy concern.

Largest observed correlations:

| Candidate | Reference Signal | Correlation | Abs Correlation |
| --- | --- | ---: | ---: |
| `residual_momentum_stability_60` | `smooth_trend_persistence_60_low_breadth` | 0.528787 | 0.528787 |
| `residual_momentum_stability_60` | `smooth_trend_persistence_60_downtrend` | 0.354987 | 0.354987 |
| `liquidity_adjusted_reversal_persistence_10` | `index_relative_reversal_5_high_drawdown` | 0.328735 | 0.328735 |
| `beta_adjusted_residual_reversal_20` | `smooth_trend_persistence_60_low_breadth` | -0.306764 | 0.306764 |
| `range_compression_quality_20_60` | `vol_of_vol_20` | -0.274976 | 0.274976 |
| `volatility_surprise_reversal_20_60_smooth` | `smooth_trend_persistence_60_low_breadth` | -0.084469 | 0.084469 |
| `volume_shock_reversal_stable_20` | `smooth_trend_persistence_60_low_breadth` | -0.081847 | 0.081847 |

Orthogonality ranking:

1. `volume_shock_reversal_stable_20`: strongest orthogonality.
2. `volatility_surprise_reversal_20_60_smooth`: strongest low-correlation volatility-structure candidate.
3. `residual_momentum_stability_60`: useful but partially overlaps with trend-quality/LOW_BREADTH behavior.

## 8. Stress / Regime Findings

Top regime findings by effective IC:

| Candidate | State Axis | State | Effective Mean IC | Interpretation |
| --- | --- | --- | ---: | --- |
| `residual_momentum_stability_60` | stress | `PANIC_LIQUIDITY_STRESS` | 0.104310 | strongest stress-state result |
| `relative_value_stability_20_60` | trend | `PERSISTENT_DOWNTREND` | 0.078038 | strong state result despite WFV failure |
| `residual_momentum_stability_60` | trend | `SIDEWAYS_CHOPPY` | 0.074340 | residual behavior not only trend-state dependent |
| `residual_momentum_stability_60` | trend | `PERSISTENT_DOWNTREND` | 0.069437 | coherent under downtrend |
| `price_impact_decay_10_20` | stress | `PANIC_LIQUIDITY_STRESS` | 0.063408 | stress state works but WFV failed |
| `beta_adjusted_residual_reversal_20` | stress | `PANIC_LIQUIDITY_STRESS` | 0.057801 | stress behavior not enough for WFV |
| `liquidity_adjusted_reversal_persistence_10` | volatility | `VOLATILITY_SPIKE` | 0.057008 | h5 stress-volatility edge but unstable |
| `volatility_surprise_reversal_20_60_smooth` | trend | `PERSISTENT_DOWNTREND` | 0.053463 | volatility structure works in downtrend |

Stress/regime interpretation:

- Residual momentum stability is the best stress-coherent candidate, but it has nontrivial overlap with existing trend-quality behavior.
- Volume shock reversal is the cleanest orthogonal candidate, but its top regime behavior is less spectacular and turnover is higher.
- Volatility surprise reversal is the best low-correlation defensive structure, but full-sample IC is weak.
- Several rejected candidates show strong regime slices but fail WFV, reinforcing the decision to keep Conditional-Alpha semantics paused.

## 9. Survivor Candidates

These are research survivor candidates, not production survivors.

### `volume_shock_reversal_stable_20`

Family:

- `liquidity_flow`

Strengths:

- sidecar WFV effective test IC 0.026315
- sidecar WFV IR 0.921072
- positive window rate 0.75
- very low correlation to current pool, max abs correlation 0.081847
- represents the highest-value orthogonal liquidity-flow direction

Weaknesses:

- full-sample h20 abs mean IC only 0.009036
- turnover proxy 0.200726, highest among the three survivors
- likely cost/stress sensitivity
- may require smoothing or turnover-aware refinement before official implementation

Orthogonality contribution:

- strongest diversification candidate in the batch.

Major risk:

- fragile under transaction costs or high turnover.

### `residual_momentum_stability_60`

Family:

- `residual_relative_value`

Strengths:

- sidecar WFV effective test IC 0.050378
- sidecar WFV IR 0.559240
- positive window rate 0.75
- strongest stress-state result: 0.104310 in panic/liquidity stress
- low turnover proxy 0.085346

Weaknesses:

- full-sample h20 abs mean IC only 0.008709
- direction differs between short and longer horizons
- max abs correlation 0.528787 to LOW_BREADTH trend-quality component
- may be partially trend-quality adjacent despite residual framing

Orthogonality contribution:

- useful residual/stress behavior, but not as orthogonal as liquidity or volatility survivors.

Major risk:

- hidden trend-quality or stress beta exposure.

### `volatility_surprise_reversal_20_60_smooth`

Family:

- `volatility_structure`

Strengths:

- sidecar WFV effective test IC 0.044034
- sidecar WFV IR 0.628899
- positive window rate 0.75
- very low max abs correlation to current pool, 0.084469
- clean turnover proxy 0.085515

Weaknesses:

- full-sample h20 abs mean IC only 0.002292
- short-horizon sign instability
- risk of generic defensive exposure

Orthogonality contribution:

- best volatility-structure diversifier candidate.

Major risk:

- WFV result may reflect stress-window concentration rather than broad standalone alpha.

## 10. Watchlist Candidates

No candidate was assigned a formal watchlist classification in this sidecar because the batch produced a clean split:

- three research survivor candidates with strong sidecar WFV evidence
- six rejected candidates with failed WFV-style behavior

However, two rejected candidates deserve hypothesis watchlist tracking, not implementation:

| Candidate | Reason To Track | Reason Not To Advance |
| --- | --- | --- |
| `relative_value_stability_20_60` | strongest full-sample IC; coherent h20 slope | WFV failed badly; likely unstable relative-value edge |
| `price_impact_decay_10_20` | strong stress-state behavior | WFV failed; noisy impact proxy |

These should not be implemented next. They are useful as lessons for future formula refinement.

## 11. Rejected Candidates

| Candidate | Primary Rejection Reason |
| --- | --- |
| `relative_value_stability_20_60` | strong full-sample IC but negative sidecar WFV effective test IC |
| `price_impact_decay_10_20` | stress slices looked good but WFV failed |
| `liquidity_adjusted_reversal_persistence_10` | h5 full-sample IC did not persist in WFV |
| `beta_adjusted_residual_reversal_20` | moderate full-sample IC but weak WFV |
| `vol_of_vol_residual_stability_20` | low IC and poor positive window rate |
| `range_compression_quality_20_60` | weak IC, sign instability, no WFV support |

The main lesson from the rejected set is that raw IC and attractive regime slices are not enough. Window persistence remains the key differentiator.

## 12. Failure Modes Observed

Recurring failure modes:

- full-sample IC without WFV persistence
- stress-state performance that did not generalize across windows
- sign instability across horizons
- liquidity/impact signals with turnover risk
- volatility structures with weak raw IC
- residual structures with hidden trend or stress exposure
- relative-value ideas that looked good in aggregate but failed direction-adjusted WFV

Most important bottleneck:

`candidate robustness is now more limiting than candidate generation`

The platform can generate plausible standalone formulas. The harder problem is finding formulas that remain coherent across windows without becoming hidden conditional signals.

## 13. Strategic Implications

The restart thesis was correct:

- the next useful evidence came from orthogonal standalone families, not Conditional-Alpha semantics
- the batch produced candidates in liquidity-flow, volatility-structure, and residual/relative-value families
- h20 remains the most credible robustness horizon
- sidecar WFV separated true robustness candidates from raw IC candidates

Implications:

- Orthogonal discovery should continue, but with smaller batches.
- Candidate formulas should be refined before production registration.
- Official implementation should be limited to the three research survivor candidates.
- Conditional-Alpha Framework should remain paused.
- Stress and transaction-cost awareness should enter earlier for liquidity-flow candidates.

## 14. Recommended Next Step

Recommended next direction:

`robustness refinement`

Concrete next task:

Design a narrow refinement pass for only the three research survivor candidates:

1. `volume_shock_reversal_stable_20`
2. `residual_momentum_stability_60`
3. `volatility_surprise_reversal_20_60_smooth`

Refinement goals:

- reduce turnover for the liquidity-flow candidate
- verify residual candidate is not hidden trend/LOW_BREADTH exposure
- verify volatility candidate is not generic risk-off exposure
- preserve h20 window stability
- avoid parameter sprawl
- keep formulas standalone and OHLCV-only

Do not do yet:

- do not run 04A+
- do not implement Conditional-Alpha semantics
- do not expand universe
- do not launch ML
- do not promote sidecar survivors into production survivor/watchlist tables
- do not broaden to another discovery batch before refining this one

## Final Recommendation

The highest-value next research direction is:

`robustness refinement of the three sidecar survivor candidates`

This should precede official implementation. The batch found promising evidence, but the evidence is not yet clean enough to push directly into the production signal factory. A focused refinement step can test whether the observed WFV-style robustness survives small formula improvements, turnover controls, and hidden exposure audits.

If that refinement holds, the next controlled implementation batch should add only those three candidates to the official research pipeline.
