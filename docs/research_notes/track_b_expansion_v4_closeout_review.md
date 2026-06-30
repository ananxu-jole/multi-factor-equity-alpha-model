# Track B Expansion v4 Closeout Review

## Executive Takeaway

Expansion v4 tested whether Project Underdog's active repair/stabilization identity extends into post-repair, resolved-stress, or hostile-to-neutral transition mechanisms. The answer from the three one-by-one v4 tests is: structurally, yes; empirically, not enough yet.

All three v4 candidates were cleanly differentiated from the current Conditional Alpha Inventory, from active breadth-repair proxies, and from simple momentum/reversal/low-volatility baselines. None advanced beyond `CONDITIONAL_ONLY_RESEARCH` because the predictive edge was weaker than active repair/stabilization behavior, horizon targets were not met, or WFV stability was insufficient.

Recommended closeout decision: pause Expansion v4 implementation now, run the next inventory monitoring/governance pass, and pivot future discovery back toward active repair/stabilization mechanisms with explicit ecosystem-diversification constraints. Post-repair concepts should not be retested until their state definitions are redesigned.

No new candidate implementation, validation/refinement run, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed for this closeout review.

## Sources Reviewed

- `docs/research_notes/track_b_expansion_v4_design_screening.md`
- `docs/research_notes/post_repair_continuation_after_breadth_recovery_v1.md`
- `docs/research_notes/resolved_stress_relative_stability_15_v1.md`
- `docs/research_notes/hostile_to_neutral_transition_quality_v1.md`
- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- `docs/research_notes/inventory_ecosystem_review_v1.md`
- Current inventory notes for:
  - `participation_liquidity_state_shift_20_60`
  - `participation_breadth_repair_under_hostile_trend`
  - `volatility_compression_after_stress_stabilization`

## Current Inventory Baseline

Current Conditional Alpha Inventory:

1. `participation_liquidity_state_shift_20_60`
2. `participation_breadth_repair_under_hostile_trend`
3. `volatility_compression_after_stress_stabilization`

Monitoring v1 showed the inventory is research-usable but concentrated:

- all three candidates are h20-centered;
- all three depend materially on hostile/stress, weak-breadth, drawdown, panic/liquidity, or stabilization states;
- pairwise signal correlations are low, with max abs corr around `0.0579`;
- co-activation is concentrated between the two participation/breadth candidates;
- `participation_breadth_repair_under_hostile_trend` is the cleanest active research candidate;
- `participation_liquidity_state_shift_20_60` and `volatility_compression_after_stress_stabilization` remain `WATCH_MONITOR`.

Expansion v4 was designed to reduce this concentration by testing what happens after repair or stress resolution. The tests did not find a validation-ready post-repair extension.

## Tested Concept Summary

| concept | mechanism thesis | result | best horizon | key IC profile | WFV persistence/sign | active coverage | max inventory corr | reason not advanced |
| --- | --- | --- | ---: | --- | --- | ---: | ---: | --- |
| `post_repair_continuation_after_breadth_recovery` | Breadth repair may have a second phase after weak breadth and hostile pressure clear. | `CONDITIONAL_ONLY_RESEARCH` | h15 | h10 `0.003406`, h15 `0.004510`, h20 `0.003048` | `0.75 / 0.75` | `0.138227` | `0.030634` | Primary IC too weak; active repair/stress attribution still stronger than post-repair continuation. |
| `resolved_stress_relative_stability_15` | Stable cross-sectional behavior after stress normalization may preserve a repair/stabilization edge. | `CONDITIONAL_ONLY_RESEARCH` | h10 | h10 `0.008831`, h15 `0.002207`, h20 `-0.001400` | `0.50 / 0.50` | `0.135844` | `0.013454` | Intended h15 failed, h20 turned negative, WFV stability was weak. |
| `hostile_to_neutral_transition_quality` | The boundary transition from hostile/stress into neutral/resolved conditions may contain usable alpha information. | `CONDITIONAL_ONLY_RESEARCH` | h20 | h10 `0.001760`, h15 `0.003097`, h20 `0.006425` | `0.75 / 0.75` | `0.095329` | `0.035563` | Best horizon drifted to h20 and active hostile/stress attribution was materially stronger than transition attribution. |

## Concept-Level Interpretation

### `post_repair_continuation_after_breadth_recovery`

The formulation cleanly avoided existing inventory overlap and did not collapse into breadth repair, momentum, or reversal. It also shifted best horizon to h15, which was useful from a diversification perspective.

It did not advance because the absolute edge was too weak. Best h15 mean IC was only `0.004510`, h10 was `0.003406`, and h20 was `0.003048`. The resolved/post-repair slices were positive but not compelling. Active/stress slices still showed better attribution than the intended post-repair continuation state.

Research lesson: breadth repair appears more useful while repair is active than after repair completion.

### `resolved_stress_relative_stability_15`

This was the cleanest structural diversification result. It had max inventory corr `0.013454`, max breadth-repair corr `0.003533`, and max low-volatility corr `0.049715`. It also showed genuine resolved-state support, with best resolved-state IC `0.011505`, slightly above best active-stress-state IC `0.011287`.

It did not advance because the intended h15 mechanism failed. Best horizon was h10 with mean IC `0.008831`; h15 was only `0.002207`; h20 was negative at `-0.001400`. WFV persistence/sign consistency were only `0.50 / 0.50`.

Research lesson: resolved-state relative stability may contain a small h10 effect, but not a robust h15 post-stress persistence mechanism in this formulation.

### `hostile_to_neutral_transition_quality`

This formulation directly tested the boundary between active hostile/stress and neutral/resolved states. It was structurally clean: max inventory corr `0.035563`, max active-repair corr `0.035563`, max resolved-stability corr `0.019087`, and max low-volatility corr `0.024498`.

It did not advance because the intended h10-h15 behavior was weak and active repair attribution dominated. Best horizon drifted to h20 with mean IC `0.006425`; h10 was `0.001760`; h15 was `0.003097`. Best transition-state IC was `0.004926`, while best active-state IC was `0.020037`.

Research lesson: the hostile-to-neutral boundary, as defined here, did not isolate the durable part of the edge. It mostly confirmed that the stronger information remains in active hostile/stress states.

## Active Repair Versus Post-Repair Behavior

Expansion v4 was intentionally not a search for another active repair clone. It asked whether repair creates an exploitable after-state.

The evidence says the after-state is weaker:

- post-repair continuation was orthogonal but too low-IC;
- resolved-stress stability was orthogonal and had some state support, but unstable across WFV windows;
- hostile-to-neutral transition quality was orthogonal but its active-stress attribution was much stronger than its transition attribution;
- none of the three created a compelling h10-h15 alternative to the current h20-centered inventory;
- none reduced the case for the current inventory identity around active repair, participation/breadth recovery, liquidity normalization, and volatility/stress stabilization.

This does not mean post-repair mechanisms are impossible. It means the simple v4 state definitions did not capture them strongly enough.

## Liquidity Normalization After Panic Exit

`liquidity_normalization_after_panic_exit` remains conceptually relevant, but it should be held rather than tested immediately.

Reasons to hold:

- Expansion v3 already rejected quiet non-hostile liquidity accumulation.
- Expansion v4 repeatedly showed that post-repair/resolved-state effects weaken after active repair.
- The current inventory already includes a WATCH_MONITOR participation/liquidity repair candidate, so another liquidity-adjacent concept carries ecosystem overlap risk.
- The volatility/stress candidate already needs monitoring for recent-window and one-window concentration issues.

Conditions for reconsideration:

- a monitoring pass confirms the existing liquidity and volatility candidates remain healthy enough for adjacent research;
- the concept is redesigned as active panic-exit normalization rather than passive post-panic calm liquidity;
- implementation includes hard checks against `participation_liquidity_state_shift_20_60`, `volatility_compression_after_stress_stabilization`, panic/stress attribution, and co-activation drift.

Closeout recommendation: keep `liquidity_normalization_after_panic_exit` as `HOLD_FOR_LATER`, not the next implementation.

## Updated Research Beliefs

- Active repair/stabilization remains stronger than post-repair persistence.
- The project identity is still repair dynamics, stabilization behavior, hostile/stress transitions, participation/breadth recovery, liquidity normalization, and volatility/stress stabilization.
- Structural orthogonality is necessary but not sufficient; all three v4 tests were clean but not strong enough.
- Resolved-state continuation is empirically weak in simple formulations.
- Transition-boundary concepts may need stronger state definitions before retesting.
- h10-h15 diversification remains desirable, but forcing post-repair semantics did not solve horizon concentration.
- The cleanest current inventory candidate remains `participation_breadth_repair_under_hostile_trend`; future work should learn from its active repair semantics.

## Strategic Recommendation

Pause Expansion v4 now.

Before any more expansion:

1. Run the next inventory monitoring pass.
2. Recheck WATCH_MONITOR candidates for recent-window fragility and one-window dominance.
3. Reassess co-activation drift between participation/liquidity and breadth repair.
4. Confirm rebuild/equivalence lineage for all current inventory panels.
5. Only then open a new design screen.

Future discovery should pivot back toward active repair/stabilization mechanisms, but with stricter ecosystem-diversification requirements:

- different state triggers than weak breadth plus hostile trend;
- lower co-activation with the participation/breadth pair;
- h10 or h15 intent only if supported by mechanism, not imposed by design;
- medium active coverage without tiny event slicing;
- explicit turnover-profile diversity;
- explicit similarity controls against the three current inventory candidates.

## What Should Not Be Repeated

Do not repeat near-term:

- passive post-repair continuation after breadth recovery;
- simple resolved-state stability after stress clears;
- hostile-to-neutral boundary signals with broad recent-hostile and neutral-entry gates;
- quiet liquidity accumulation without active panic/repair semantics;
- calm accumulation without a stronger catalyst;
- low-volatility quality unless anchored to active repair completion with clear non-beta controls;
- raw continuation, simple reversal, price-rank momentum, broad nonlinear state scoring, or over-fragmented state slicing.

Do not implement another post-repair candidate until the state definition is materially redesigned around a sharper event, a clearer market microstructure transition, or stronger active repair lineage.

## Closeout Decision

Expansion v4 should be closed as a useful negative/conditional research cycle.

No v4 concept should be promoted, refined immediately, registered, added to survivor/watchlist inventory, or used in construction-layer design. The next useful step is monitoring/governance, followed by a new design screen focused on active repair/stabilization diversification rather than post-repair persistence.

