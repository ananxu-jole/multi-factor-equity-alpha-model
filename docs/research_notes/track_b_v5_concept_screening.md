# Track B v5 Concept Screening

## Executive Takeaway

This note defines a design-only Track B v5 concept screen. It does not create new signals, implement formulas, run validation, register production signals, mutate survivor/watchlist status, alter gates or schemas, use ML, change portfolio logic, or wire production Conditional-Alpha paths.

The prior Track B cycle produced the first governed conditional-alpha review candidate:

`participation_liquidity_state_shift_20_60` -> `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

The v5 frontier should not be another broad search. The next wave should be a small focused discovery batch built from concept theses that are structurally distant from reversal, simple continuation, and price-rank redundancy.

Recommended v5 shape: small focused batch, not broad discovery.

Recommended first implementation set, if and only if implementation is later approved:

1. `participation_breadth_repair_under_hostile_trend`
2. `nonprice_liquidity_repair_without_price_extension`
3. `stress_to_normalization_participation_repair`

These are concept names only. They are not implemented candidates.

## Source Context Reviewed

Inputs reviewed:

- `docs/research_notes/track_b_conditional_alpha_cycle_closeout.md`
- `artifacts/research/track_b_conditional_alpha_cycle_closeout_v1/next_phase_discovery_roadmap.csv`
- `artifacts/research/track_b_conditional_alpha_cycle_closeout_v1/research_inventory.csv`
- lifecycle notes for `participation_liquidity_state_shift_20_60`

Relevant lifecycle outcome:

| role | validated representation |
|:--|:--|
| Primary | `rank_persist_10_state_TREND_HOSTILE_zero` |
| Backup / state confirmation | `rebalance_10_state_WEAK_BREADTH_zero` |
| Stress confirmation | `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero` |
| Broad fallback / control | `rebalance_20` |

## What Worked

The successful Track B path was not a raw alpha search. It was a disciplined narrowing process:

- state-shift mechanism rather than price-rank continuation
- participation and liquidity primitives rather than price-only behavior
- hostile-trend and weak-breadth activation
- stress / weak-breadth confirmation
- turnover reduction through rank persistence, rebalance cadence, and smoothing
- fixed representation after refinement, rather than open-ended parameter search
- explicit guardrails before any further integration review

The most important technical lesson is that turnover improvement was largely rank-churn reduction, not simple exposure suppression. That makes rebalance and rank-persistence logic credible tools for v5, provided they are used conservatively and frozen early.

## What Repeatedly Failed

The following should be treated as known anti-patterns:

- naive continuation after mature leadership
- simple reversal inversion
- price-rank redundancy
- pseudo-orthogonal variants that differ in formula but share latent reversal exposure
- raw breakout continuation without state and event-quality controls
- liquidity multiplied by price momentum
- excessive refinement search without a small fixed candidate set
- overly fragmented state slicing with weak active-window coverage

## v5 Screening Principles

Each v5 concept must answer four questions before implementation:

1. Why is this not a reversal proxy?
2. Why is this not simple momentum or mature continuation?
3. What market-state transition should activate the edge?
4. What failure mode from v2-v4 does it directly avoid?

Concepts should prefer:

- OHLCV-only primitives
- high or adequate active coverage
- low parameter sprawl
- explicit turnover discipline
- interpretable state-transition semantics
- modest candidate count
- early rejection when the thesis is vague

## Concept Screen

| priority | recommendation | concept name | bucket | mechanism family | expected horizon | expected turnover | expected active coverage |
|:--|:--|:--|:--|:--|:--|:--|:--|
| HIGH | IMPLEMENT_NEXT | `participation_breadth_repair_under_hostile_trend` | A | participation / breadth transition | h10-h20 | medium-low with rebalance or rank persistence | moderate |
| HIGH | IMPLEMENT_NEXT | `nonprice_liquidity_repair_without_price_extension` | B | non-price liquidity transition | h10-h20 | medium-low with smoothing | broad-to-moderate |
| HIGH | IMPLEMENT_NEXT | `stress_to_normalization_participation_repair` | C | stress normalization / participation repair | h10-h20 | medium | moderate |
| HIGH | IMPLEMENT_NEXT | `weak_breadth_liquidity_confirmation_pair` | F | conditional liquidity x breadth interaction | h20 | medium-low | moderate |
| MEDIUM | HOLD_FOR_LATER | `temporal_up_down_participation_asymmetry` | E | temporal asymmetry | h10-h20 | medium | broad |
| MEDIUM | HOLD_FOR_LATER | `dispersion_compression_participation_rotation` | D | dispersion transition | h10-h20 | low-medium | moderate |
| MEDIUM | HOLD_FOR_LATER | `rank_stability_repair_after_drawdown` | E | cross-sectional stability transition | h10-h20 | low-medium | moderate |
| MEDIUM | HOLD_FOR_LATER | `volatility_spike_to_range_stabilization` | D | volatility state transition | h10-h20 | low-medium | moderate |
| MEDIUM | HOLD_FOR_LATER | `low_extension_state_gated_participation_followthrough` | F | conditional interaction / low-extension participation | h5-h20 | medium | moderate |
| LOW | HOLD_FOR_LATER | `nonlinear_hostile_state_activation_score` | F | nonlinear activation semantics | h20 | low-medium | moderate-to-sparse |
| LOW | HOLD_FOR_LATER | `regime_aware_rank_persistence_system` | F | regime-aware ranking system | h20 | low | broad-to-moderate |
| LOW | DISCARD_CONCEPT | `state_gated_breakout_continuation_layer` | D | breakout continuation layer | h5-h10 | medium-high risk | sparse-to-moderate |

## Concept Details

### participation_breadth_repair_under_hostile_trend

- Mechanism family: participation / breadth transition.
- Economic intuition: during hostile trend states, early repair in market participation may indicate that selling pressure is becoming less broad before price leadership is obvious.
- State-transition thesis: transition from broad weakness toward improving participation under `TREND_HOSTILE`.
- Structurally different from reversal: does not fade a large prior price move; it looks for breadth repair while the market state remains hostile.
- Structurally different from momentum: does not chase mature leaders; price extension should be neutral or controlled.
- Expected activation condition: hostile trend plus improving participation breadth.
- Expected horizon: h10-h20.
- Expected turnover profile: medium-low if rank persistence or rebalance cadence is fixed.
- Expected active coverage: moderate.
- Likely failure mode: repair may be too late or may only identify brief bear-market rallies.
- Orthogonality hypothesis: should be less correlated to reversal than price-shock signals because the primary primitive is participation transition.
- Implementation complexity: medium.
- Priority ranking: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### nonprice_liquidity_repair_without_price_extension

- Mechanism family: non-price liquidity transition.
- Economic intuition: improving liquidity conditions may precede more stable relative performance when they are not merely a consequence of recent price strength.
- State-transition thesis: liquidity repair under neutral or low price extension.
- Structurally different from reversal: avoids abnormal price shock and does not fade recent winners or losers.
- Structurally different from momentum: explicitly limits price-rank dependence and focuses on liquidity improvement.
- Expected activation condition: improving dollar-volume or participation liquidity with low-to-moderate price extension.
- Expected horizon: h10-h20.
- Expected turnover profile: medium-low with smoothing.
- Expected active coverage: broad-to-moderate.
- Likely failure mode: liquidity improvement may be generic size/liquidity exposure rather than alpha.
- Orthogonality hypothesis: should retain the non-price identity of `nonprice_liquidity_persistence_20_60` while improving state specificity.
- Implementation complexity: medium.
- Priority ranking: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### stress_to_normalization_participation_repair

- Mechanism family: stress normalization / participation repair.
- Economic intuition: after panic or liquidity stress, securities with improving participation and stabilizing liquidity may recover more coherently than noisy rebound candidates.
- State-transition thesis: transition from stress to early normalization, not pure recovery momentum.
- Structurally different from reversal: requires participation repair and stress-state transition, not simply prior underperformance.
- Structurally different from momentum: avoids mature post-stress leaders and focuses on repair quality.
- Expected activation condition: recent panic/liquidity stress or drawdown acceleration followed by improving participation/liquidity state.
- Expected horizon: h10-h20.
- Expected turnover profile: medium.
- Expected active coverage: moderate.
- Likely failure mode: activation may lag fast rebounds or overfit crisis windows.
- Orthogonality hypothesis: should be distinct from simple reversal if price rank is neutralized and state transition drives activation.
- Implementation complexity: medium.
- Priority ranking: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### weak_breadth_liquidity_confirmation_pair

- Mechanism family: conditional liquidity x breadth interaction.
- Economic intuition: weak breadth alone is not enough; liquidity repair inside weak breadth may identify securities where participation is improving despite fragile market internals.
- State-transition thesis: weak breadth plus improving non-price liquidity confirmation.
- Structurally different from reversal: the edge comes from state confirmation, not fading a price shock.
- Structurally different from momentum: does not require strong price leadership.
- Expected activation condition: `WEAK_BREADTH` with improving liquidity participation.
- Expected horizon: h20.
- Expected turnover profile: medium-low with rebalance cadence.
- Expected active coverage: moderate.
- Likely failure mode: high similarity to the existing validated weak-breadth backup if not designed carefully.
- Orthogonality hypothesis: should be an adjacent confirmation of the successful candidate, not an independent alpha sleeve unless similarity is low.
- Implementation complexity: medium.
- Priority ranking: HIGH.
- Recommendation: IMPLEMENT_NEXT.

### temporal_up_down_participation_asymmetry

- Mechanism family: temporal asymmetry.
- Economic intuition: persistent asymmetry between participation on up-days and down-days may reveal accumulation or distribution quality without relying on simple price rank.
- State-transition thesis: change in up/down participation balance across short and medium windows.
- Structurally different from reversal: not a fade of prior return; uses directional participation composition.
- Structurally different from momentum: does not require absolute price leadership.
- Expected activation condition: improving up-participation relative to down-participation, ideally under weak or transitional market states.
- Expected horizon: h10-h20.
- Expected turnover profile: medium.
- Expected active coverage: broad.
- Likely failure mode: may become a disguised momentum or reversal proxy depending on sign convention.
- Orthogonality hypothesis: potentially orthogonal if price-rank neutrality is explicit.
- Implementation complexity: medium.
- Priority ranking: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### dispersion_compression_participation_rotation

- Mechanism family: dispersion transition.
- Economic intuition: falling dispersion with improving participation may indicate healthier cross-sectional rotation rather than unstable leader chasing.
- State-transition thesis: high-to-lower dispersion transition plus participation repair.
- Structurally different from reversal: focuses on market structure and participation, not individual price overreaction.
- Structurally different from momentum: avoids selecting mature leaders; seeks stabilization after dispersion stress.
- Expected activation condition: dispersion compression after elevated dispersion, with participation improvement.
- Expected horizon: h10-h20.
- Expected turnover profile: low-medium.
- Expected active coverage: moderate.
- Likely failure mode: may be too market-state driven and weak cross-sectionally.
- Orthogonality hypothesis: could diversify the participation/liquidity family if dispersion is the activation driver.
- Implementation complexity: medium.
- Priority ranking: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### rank_stability_repair_after_drawdown

- Mechanism family: cross-sectional stability transition.
- Economic intuition: after drawdown stress, improving rank stability may distinguish durable repair from noisy rebound.
- State-transition thesis: unstable-to-stable cross-sectional rank behavior after drawdown.
- Structurally different from reversal: does not simply favor prior losers; requires stability repair.
- Structurally different from momentum: does not chase acceleration; it waits for rank stabilization.
- Expected activation condition: drawdown or trend-hostile state followed by improving rank persistence and controlled price extension.
- Expected horizon: h10-h20.
- Expected turnover profile: low-medium.
- Expected active coverage: moderate.
- Likely failure mode: rank stability may still inherit price-rank redundancy.
- Orthogonality hypothesis: useful only if stability is measured independently from raw return rank.
- Implementation complexity: medium.
- Priority ranking: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### volatility_spike_to_range_stabilization

- Mechanism family: volatility state transition.
- Economic intuition: after volatility spikes, securities whose ranges stabilize without broad price extension may have better forward behavior than noisy high-volatility names.
- State-transition thesis: volatility spike to range stabilization.
- Structurally different from reversal: focuses on volatility normalization and range quality, not price fade.
- Structurally different from momentum: does not chase breakout direction.
- Expected activation condition: recent volatility spike followed by lower jumpiness or tighter realized range.
- Expected horizon: h10-h20.
- Expected turnover profile: low-medium.
- Expected active coverage: moderate.
- Likely failure mode: may duplicate volatility reversal or become too defensive.
- Orthogonality hypothesis: moderate only if price-rank neutrality and volatility-baseline comparison are explicit.
- Implementation complexity: medium.
- Priority ranking: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### low_extension_state_gated_participation_followthrough

- Mechanism family: conditional interaction / low-extension participation.
- Economic intuition: participation follow-through may work only before price overextension, not after mature leadership.
- State-transition thesis: participation improvement under low overextension, preferably in trend-hostile or weak-breadth states.
- Structurally different from reversal: does not fade price moves.
- Structurally different from momentum: requires low extension rather than strong realized momentum.
- Expected activation condition: low overextension plus participation improvement.
- Expected horizon: h5-h20.
- Expected turnover profile: medium.
- Expected active coverage: moderate.
- Likely failure mode: could recreate failed low-overextension breakout behavior if price confirmation dominates.
- Orthogonality hypothesis: promising only if participation is primary and price follow-through is secondary.
- Implementation complexity: medium.
- Priority ranking: MEDIUM.
- Recommendation: HOLD_FOR_LATER.

### nonlinear_hostile_state_activation_score

- Mechanism family: nonlinear activation semantics.
- Economic intuition: weak breadth, hostile trend, liquidity stress, and low dispersion may interact nonlinearly; a simple single-state trigger may be too blunt.
- State-transition thesis: activation only when two or more independent fragile-state conditions align.
- Structurally different from reversal: state activation is market-structure based, not price-shock based.
- Structurally different from momentum: ranking primitive should remain participation/liquidity quality, not price strength.
- Expected activation condition: hostile trend plus one of weak breadth, stress, or low dispersion.
- Expected horizon: h20.
- Expected turnover profile: low-medium.
- Expected active coverage: moderate-to-sparse.
- Likely failure mode: over-fragmented state slicing and sample-size illusion.
- Orthogonality hypothesis: potentially useful as an activation layer, but not as a standalone signal concept.
- Implementation complexity: medium-high.
- Priority ranking: LOW.
- Recommendation: HOLD_FOR_LATER.

### regime_aware_rank_persistence_system

- Mechanism family: regime-aware ranking system.
- Economic intuition: rank-persistence controls may need different cadences by market state, but this is closer to research architecture than a single candidate.
- State-transition thesis: persistence and rebalance cadence adapt to state stability.
- Structurally different from reversal: it is an execution/representation semantic, not a return-fade signal.
- Structurally different from momentum: it manages churn rather than selecting price leaders.
- Expected activation condition: state-specific cadence rules.
- Expected horizon: h20.
- Expected turnover profile: low.
- Expected active coverage: broad-to-moderate.
- Likely failure mode: accidental optimization of turnover and state labels.
- Orthogonality hypothesis: should be treated as a construction diagnostic, not an alpha source.
- Implementation complexity: high.
- Priority ranking: LOW.
- Recommendation: HOLD_FOR_LATER.

### state_gated_breakout_continuation_layer

- Mechanism family: breakout continuation layer.
- Economic intuition: clean breakouts may work only in carefully filtered states.
- State-transition thesis: state-gated breakout follow-through after compression.
- Structurally different from reversal: would not fade moves, but prior evidence shows this family is fragile.
- Structurally different from momentum: only if event quality dominates price rank.
- Expected activation condition: low overextension, clean range expansion, and supportive market state.
- Expected horizon: h5-h10.
- Expected turnover profile: medium-high risk.
- Expected active coverage: sparse-to-moderate.
- Likely failure mode: repeats raw breakout continuation, high turnover, and narrow state fit.
- Orthogonality hypothesis: uncertain despite potentially low measured correlation.
- Implementation complexity: medium-high.
- Priority ranking: LOW.
- Recommendation: DISCARD_CONCEPT for v5.

## Highest-Priority Concepts For Future Implementation

The 5-8 highest-priority concepts are:

1. `participation_breadth_repair_under_hostile_trend`
2. `nonprice_liquidity_repair_without_price_extension`
3. `stress_to_normalization_participation_repair`
4. `weak_breadth_liquidity_confirmation_pair`
5. `temporal_up_down_participation_asymmetry`
6. `dispersion_compression_participation_rotation`
7. `rank_stability_repair_after_drawdown`

The first 2-3 to implement later should be:

1. `participation_breadth_repair_under_hostile_trend`
2. `nonprice_liquidity_repair_without_price_extension`
3. `stress_to_normalization_participation_repair`

These three best match the successful Track B evidence while still moving beyond the exact v4 validated representation.

## Concepts To Avoid For v5

Avoid:

- `state_gated_breakout_continuation_layer`
- raw breakout continuation variants
- gap continuation unless event coverage and turnover controls are solved first
- mature leadership continuation
- relative strength acceleration
- simple inversions of failed continuation ideas
- liquidity multiplied by price-rank momentum
- broad nonlinear state scores with many fragile conditions

## v5 Batch Shape Recommendation

v5 should be a small focused batch, not a broad discovery batch.

Recommended future implementation size: 5-8 concepts, with only 2-3 implemented first if the project wants an even tighter phase. The first implementation wave should prioritize participation/breadth repair, non-price liquidity repair, and stress-to-normalization participation repair.

Before implementation, each concept should receive:

- frozen intended direction
- explicit non-reversal thesis
- explicit non-momentum thesis
- expected active-state coverage range
- turnover-control plan
- baseline similarity risks
- rejection criteria before refinement

## Final Recommendation

Proceed next with a small Track B v5 design-to-implementation plan for the top three concepts only. Do not launch a broad candidate batch yet.

Keep `participation_liquidity_state_shift_20_60` frozen as `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`. Any rebuild/equivalence or integration-review work for that candidate should remain separate from v5 discovery.
