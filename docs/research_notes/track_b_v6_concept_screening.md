# Track B v6 Concept Screening

## Executive Takeaway

This is a design-only Track B v6 concept screen. It identifies the next conditional-alpha discovery frontier beyond the current participation/liquidity/breadth repair inventory.

No candidates were implemented. No validation was run. No production registration, survivor/watchlist promotion, portfolio construction, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.

Current Conditional Alpha Inventory:

| candidate | inventory status | primary variant | mechanism family |
|:--|:--|:--|:--|
| `participation_liquidity_state_shift_20_60` | `INVENTORY_ACTIVE_RESEARCH` | `rank_persist_10_state_TREND_HOSTILE_zero` | participation/liquidity state shift |
| `participation_breadth_repair_under_hostile_trend` | `INVENTORY_ACTIVE_RESEARCH` | `strict_weak_breadth_rebalance_10` | participation breadth repair |

The v6 search should be focused, not broad. It should test a small number of non-participation mechanisms first, centered on volatility/dispersion stabilization, event quality, and temporal asymmetry.

Recommended first implementation set for a later research-only batch:

1. `volatility_compression_after_stress_stabilization`
2. `dispersion_peak_to_cross_sectional_stability`
3. `event_gap_quality_continuation_filter`

## Source Context Reviewed

Reviewed context:

- `docs/research_notes/conditional_alpha_inventory_v1.md`
- `docs/research_notes/track_b_v5_concept_screening.md`
- `docs/research_notes/track_b_v5_focused_discovery.md`
- `docs/research_notes/participation_breadth_repair_refinement.md`
- `docs/research_notes/participation_breadth_repair_conditional_validation.md`
- `docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md`
- `docs/research_notes/track_b_conditional_alpha_cycle_closeout.md`

Key interpretation:

- The current inventory is already concentrated in participation, liquidity, weak breadth, and hostile-trend repair.
- v6 should not create more participation repair variants.
- The next useful question is whether other market-state transition families can produce conditional structure with low overlap to inventory candidates.

## v6 Screening Principles

v6 concepts should:

- test structurally distinct mechanisms
- remain OHLCV-only
- use simple state-transition semantics
- avoid price-rank momentum and raw continuation
- avoid simple reversal or inverted failed signals
- explicitly test baseline similarity to current inventory candidates
- preserve active-window and turnover discipline
- freeze candidate count early if implementation is later approved

v6 concepts should avoid:

- more participation repair variants
- raw continuation after mature leadership
- simple price-shock reversal
- broad nonlinear state scores
- pseudo-orthogonal formula variants
- large parameter grids
- production, portfolio, or ML integration

## Concept Screen Summary

| priority | recommendation | concept name | mechanism family | expected horizon | expected turnover |
|:--|:--|:--|:--|:--|:--|
| HIGH | IMPLEMENT_NEXT | `volatility_compression_after_stress_stabilization` | volatility / dispersion stabilization | h10-h20 | low-medium |
| HIGH | IMPLEMENT_NEXT | `dispersion_peak_to_cross_sectional_stability` | dispersion state transition | h10-h20 | low-medium |
| HIGH | IMPLEMENT_NEXT | `event_gap_quality_continuation_filter` | event-quality structure | h5-h20 | medium |
| HIGH | IMPLEMENT_NEXT | `temporal_range_asymmetry_stabilization` | temporal asymmetry | h10-h20 | medium |
| MEDIUM | HOLD_FOR_LATER | `drawdown_deceleration_quality_repair` | market-state transition | h10-h20 | low-medium |
| MEDIUM | HOLD_FOR_LATER | `volatility_expansion_without_directional_break` | event-quality / volatility | h5-h10 | medium |
| MEDIUM | HOLD_FOR_LATER | `liquidity_state_persistence_without_participation_breadth` | non-price liquidity transition follow-up | h10-h20 | medium-low |
| MEDIUM | HOLD_FOR_LATER | `range_efficiency_state_transition` | market-state transition | h10-h20 | medium |
| MEDIUM | HOLD_FOR_LATER | `post_stress_dispersion_normalization_without_breadth` | volatility / dispersion stabilization | h10-h20 | low-medium |
| LOW | HOLD_FOR_LATER | `overnight_intraday_temporal_divergence` | temporal asymmetry | h5-h20 | medium-high |
| LOW | DISCARD_CONCEPT | `state_transition_meta_score` | nonlinear activation structure | h20 | low-medium |
| LOW | DISCARD_CONCEPT | `raw_breakout_reacceleration_after_compression` | breakout continuation | h5-h10 | medium-high |

CSV artifact: `artifacts/research/track_b_v6_concept_screening/concept_screening.csv`

## Concept Details

### `volatility_compression_after_stress_stabilization`

- Mechanism family: volatility / dispersion stabilization.
- State-transition thesis: after stress or volatility spike, names whose realized range compresses without price extension may show cleaner forward behavior.
- Why it differs from current inventory: it uses volatility/range normalization rather than participation, liquidity repair, or breadth repair.
- Why it differs from reversal/momentum: it does not fade prior return or chase price rank; it requires volatility state normalization and low price-extension confirmation.
- Expected activation state: recent volatility spike or panic/liquidity stress followed by range compression and low price extension.
- Expected horizon: h10-h20.
- Expected turnover: low-medium.
- Likely failure mode: generic low-volatility/defensive exposure or volatility reversal proxy.
- Orthogonality hypothesis: should be orthogonal if price-rank neutrality and volatility-only baselines are enforced.
- Implementation complexity: medium.
- Priority: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### `dispersion_peak_to_cross_sectional_stability`

- Mechanism family: dispersion state transition.
- State-transition thesis: cross-sectional dispersion peaks followed by stabilizing rank dispersion may identify healthier rotation after unstable markets.
- Why it differs from current inventory: it uses market-wide dispersion transition, not participation or weak-breadth repair.
- Why it differs from reversal/momentum: selection is based on stabilization after dispersion stress, not prior underperformance or mature leadership.
- Expected activation state: high dispersion transitioning toward lower dispersion with stable cross-sectional ranks.
- Expected horizon: h10-h20.
- Expected turnover: low-medium.
- Likely failure mode: too market-state-driven and weak cross-sectionally; may duplicate broad risk-on normalization.
- Orthogonality hypothesis: could diversify inventory by using dispersion states as the primary activation driver.
- Implementation complexity: medium.
- Priority: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### `event_gap_quality_continuation_filter`

- Mechanism family: event-quality structure.
- State-transition thesis: large gaps followed by orderly range containment and non-extreme volume may identify event quality rather than noisy reversal or chase behavior.
- Why it differs from current inventory: it is event-quality focused, not a participation or liquidity-state repair mechanism.
- Why it differs from reversal/momentum: it separates gap continuation from gap reversal by requiring post-event quality, not fading or chasing the raw gap.
- Expected activation state: material gap event followed by contained intraday range, limited wick noise, and non-explosive churn.
- Expected horizon: h5-h20.
- Expected turnover: medium.
- Likely failure mode: gap sparsity, high turnover, and event-window overfitting; may recreate v3 gap issues if too broad.
- Orthogonality hypothesis: could be orthogonal if event quality and range containment dominate price direction.
- Implementation complexity: medium-high.
- Priority: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### `temporal_range_asymmetry_stabilization`

- Mechanism family: temporal asymmetry.
- State-transition thesis: asymmetry between upside-range days and downside-range days may reveal stabilizing demand without relying on return rank.
- Why it differs from current inventory: it uses intraday/range temporal asymmetry, not participation, liquidity, or breadth repair.
- Why it differs from reversal/momentum: it is based on range behavior and direction balance instead of cumulative return rank.
- Expected activation state: improving upside/downside range balance after choppy or trend-hostile periods.
- Expected horizon: h10-h20.
- Expected turnover: medium.
- Likely failure mode: can collapse into momentum if sign convention follows recent returns too closely; can become noisy in sideways markets.
- Orthogonality hypothesis: potentially orthogonal if range asymmetry is neutralized against price rank and reversal baselines.
- Implementation complexity: medium.
- Priority: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### `drawdown_deceleration_quality_repair`

- Mechanism family: market-state transition.
- State-transition thesis: a slowing drawdown with improving realized range quality may indicate repair before broad participation confirms.
- Why it differs from current inventory: it is market-state and range-quality repair, not participation/breadth repair.
- Why it differs from reversal/momentum: it does not buy prior losers mechanically; it requires drawdown deceleration plus stability quality.
- Expected activation state: drawdown acceleration transitioning to drawdown deceleration with lower realized range noise.
- Expected horizon: h10-h20.
- Expected turnover: low-medium.
- Likely failure mode: generic drawdown filter or late stress recovery signal; sample concentration around crises.
- Orthogonality hypothesis: should be partly orthogonal to participation inventory if quality is range/drawdown based.
- Implementation complexity: medium.
- Priority: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### `volatility_expansion_without_directional_break`

- Mechanism family: event-quality / volatility.
- State-transition thesis: volatility expansion without directional price break may signal unresolved pressure; the edge may be in avoiding or penalizing unstable names.
- Why it differs from current inventory: it focuses on instability avoidance rather than participation repair.
- Why it differs from reversal/momentum: it need not fade direction, and directional break is absent or penalized.
- Expected activation state: volatility expansion with low directional efficiency and high intraday noise.
- Expected horizon: h5-h10.
- Expected turnover: medium.
- Likely failure mode: risk filter rather than alpha; sign may flip by regime.
- Orthogonality hypothesis: useful as a possible context/risk ingredient, but standalone alpha evidence may be weak.
- Implementation complexity: medium.
- Priority: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### `liquidity_state_persistence_without_participation_breadth`

- Mechanism family: non-price liquidity transition follow-up.
- State-transition thesis: persistent improvement in non-price liquidity after prior deterioration may matter even without breadth repair semantics.
- Why it differs from current inventory: it removes breadth/participation repair activation and tests liquidity state persistence alone.
- Why it differs from reversal/momentum: it excludes price extension and uses non-price liquidity state transitions.
- Expected activation state: liquidity deterioration to liquidity stability/improvement with price-extension cap.
- Expected horizon: h10-h20.
- Expected turnover: medium-low.
- Likely failure mode: too close to the prior participation/liquidity candidate or generic size/liquidity exposure.
- Orthogonality hypothesis: potentially orthogonal only if overlap with inventory candidates remains low.
- Implementation complexity: medium.
- Priority: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### `range_efficiency_state_transition`

- Mechanism family: market-state transition.
- State-transition thesis: transition from noisy range expansion to efficient range movement may indicate improving price discovery quality.
- Why it differs from current inventory: it uses range efficiency/quality rather than participation, liquidity, or breadth repair.
- Why it differs from reversal/momentum: efficient movement is evaluated as state quality, not return rank; it does not fade shocks.
- Expected activation state: high noise/range state transitioning to higher directional efficiency with controlled extension.
- Expected horizon: h10-h20.
- Expected turnover: medium.
- Likely failure mode: drift into momentum or breakout continuation; vulnerable to trend-chasing failure mode.
- Orthogonality hypothesis: could diversify if efficiency is orthogonal to price-rank momentum and reversal.
- Implementation complexity: medium.
- Priority: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### `post_stress_dispersion_normalization_without_breadth`

- Mechanism family: volatility / dispersion stabilization.
- State-transition thesis: after stress, dispersion normalization may be more informative than breadth repair for identifying stable cross-sectional behavior.
- Why it differs from current inventory: it explicitly removes breadth repair and participation state as primary drivers.
- Why it differs from reversal/momentum: it uses dispersion normalization and stability, not prior underperformance.
- Expected activation state: recent stress with high-to-normalizing dispersion and low rank churn.
- Expected horizon: h10-h20.
- Expected turnover: low-medium.
- Likely failure mode: sparse stress windows and one-window dominance; may duplicate broad fallback behavior.
- Orthogonality hypothesis: potentially useful as a non-participation conditional state layer.
- Implementation complexity: medium.
- Priority: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### `overnight_intraday_temporal_divergence`

- Mechanism family: temporal asymmetry.
- State-transition thesis: persistent divergence between overnight and intraday behavior may capture investor-flow timing asymmetry.
- Why it differs from current inventory: it is a temporal flow-timing proxy, not participation/breadth/liquidity repair.
- Why it differs from reversal/momentum: it is based on session composition rather than cumulative return rank.
- Expected activation state: stable overnight/intraday asymmetry after volatility or trend-state transitions.
- Expected horizon: h5-h20.
- Expected turnover: medium-high.
- Likely failure mode: data-quality sensitivity, hidden momentum/reversal, same-bar timing risk, and turnover risk.
- Orthogonality hypothesis: potentially orthogonal, but only after a careful session-alignment audit.
- Implementation complexity: high.
- Priority: LOW.
- Recommendation: HOLD_FOR_LATER.

### `state_transition_meta_score`

- Mechanism family: nonlinear activation structure.
- State-transition thesis: combine several market-state transitions into a single activation score for candidate gating.
- Why it differs from current inventory: it would be a broad activation system rather than a distinct economic mechanism.
- Why it differs from reversal/momentum: it might differ superficially, but the score could hide reversal/momentum exposure behind state weights.
- Expected activation state: composite of volatility, dispersion, drawdown, and breadth transition states.
- Expected horizon: h20.
- Expected turnover: low-medium.
- Likely failure mode: overfit nonlinear state score, weak interpretability, and broad parameter sprawl.
- Orthogonality hypothesis: not credible until several simple state mechanisms are validated independently.
- Implementation complexity: high.
- Priority: LOW.
- Recommendation: DISCARD_CONCEPT.

### `raw_breakout_reacceleration_after_compression`

- Mechanism family: breakout continuation.
- State-transition thesis: compression followed by breakout reacceleration may look attractive after v3/v4, but it likely repeats continuation failures.
- Why it differs from current inventory: it differs mechanically, but does not add a clean non-participation conditional thesis.
- Why it differs from reversal/momentum: it probably does not; it risks becoming price-rank momentum and raw continuation.
- Expected activation state: range compression followed by price breakout.
- Expected horizon: h5-h10.
- Expected turnover: medium-high.
- Likely failure mode: price-rank redundancy, late-entry overextension, and turnover.
- Orthogonality hypothesis: weak; this is a known anti-pattern unless redesigned around event quality.
- Implementation complexity: low-medium.
- Priority: LOW.
- Recommendation: DISCARD_CONCEPT.

## Promising Concepts

The 5-8 concepts worth preserving for future research are:

1. `volatility_compression_after_stress_stabilization`
2. `dispersion_peak_to_cross_sectional_stability`
3. `event_gap_quality_continuation_filter`
4. `temporal_range_asymmetry_stabilization`
5. `drawdown_deceleration_quality_repair`
6. `volatility_expansion_without_directional_break`
7. `range_efficiency_state_transition`
8. `post_stress_dispersion_normalization_without_breadth`

The first four are the highest-priority concepts. The medium-priority group should remain held until the first implementation set shows whether volatility/dispersion/event-quality mechanics can remain orthogonal to the inventory candidates.

## Top Implementation Candidates For Later

If implementation is later approved, v6 should start with only:

1. `volatility_compression_after_stress_stabilization`
2. `dispersion_peak_to_cross_sectional_stability`
3. `event_gap_quality_continuation_filter`

`temporal_range_asymmetry_stabilization` is a strong alternate if one of the first three proves infeasible or too data-sensitive during design review.

## Concepts To Avoid

Avoid implementing:

- `state_transition_meta_score`: too broad, too nonlinear, and too easy to overfit.
- `raw_breakout_reacceleration_after_compression`: repeats raw continuation and price-rank momentum failure modes.
- additional participation repair variants: the current inventory already covers this family.
- non-price liquidity follow-ups unless they explicitly demonstrate low inventory overlap before implementation.

## Recommended v6 Batch Shape

v6 should be a small focused batch, not broad discovery.

Recommended implementation size later: 3 concepts, with at most one simple formulation per concept and no parameter grid. The research goal should be to test whether a third mechanism family exists outside participation/liquidity/breadth repair, not to optimize within a family.

Required future diagnostics if implementation is later approved:

- structural quality
- multi-horizon IC, especially h10/h20
- turnover and active coverage
- WFV-style persistence/sign consistency
- one-window dominance
- stress/regime attribution
- similarity to reversal, momentum, and price-rank baselines
- similarity to both inventory candidates
- explicit check that each concept remains outside participation repair semantics

## Final Recommendation

Proceed next with a focused research-only v6 implementation batch only after approval. The best starting set is `volatility_compression_after_stress_stabilization`, `dispersion_peak_to_cross_sectional_stability`, and `event_gap_quality_continuation_filter`. Do not create a broad batch, do not tune parameters, and do not add production, portfolio, ML, survivor/watchlist, or Conditional-Alpha production wiring.
