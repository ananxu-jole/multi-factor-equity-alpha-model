# Inventory Ecosystem Review v1

## Executive Takeaway

Project Underdog's conditional-alpha research layer now contains a small governed inventory of three research candidates:

1. `participation_liquidity_state_shift_20_60`
2. `participation_breadth_repair_under_hostile_trend`
3. `volatility_compression_after_stress_stabilization`

The ecosystem is no longer just a collection of isolated signal tests. It is beginning to express a coherent research view: conditional repair and stabilization during hostile or stressed market states has been more durable than naive continuation, simple reversal inversion, abstract topology, or raw novelty.

The main lesson is not that every conditional idea works. The Expansion v2 one-by-one tests showed the opposite: dispersion recovery, event-quality persistence, and temporal asymmetry were structurally distinct, but only the event-quality concept retained enough information to remain a future research family. Structural orthogonality is necessary, but not sufficient. A candidate also needs useful state semantics, adequate active coverage, manageable turnover, and evidence that predictive behavior is not concentrated in one window.

The recommended next step is to strengthen inventory monitoring before launching another discovery wave. The inventory is useful, but it is concentrated around h20, hostile/stress activation, and repair-style behavior. Future discovery should remain one-by-one and inventory-aware.

## Scope And Non-Changes

This review is a synthesis-only research artifact. It does not implement new candidates, run validation, change gates, alter schemas, update survivor/watchlist status, add portfolio construction, introduce ML logic, or wire any production Conditional-Alpha path.

Sources reviewed include:

- `conditional_alpha_inventory_v1.md`
- Track B closeout and roadmap notes
- Track B v5 focused discovery, refinement, and validation notes
- Track B v6 focused discovery, refinement, validation, and integration review notes
- Expansion v2 inventory-aware screening
- One-by-one tests for dispersion recovery, event-quality persistence, and temporal asymmetry

## Current Inventory Composition

| Candidate | Mechanism Family | Current Research Status | Primary Representation | Activation Semantics | Expected Horizon | h20 Mean IC | Positive IC Rate | Turnover | Active Coverage | WFV-Style Persistence / Sign | Key Overlap | Main Risks |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| `participation_liquidity_state_shift_20_60` | Participation / liquidity state repair | `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` / `INVENTORY_ACTIVE_RESEARCH` | `rank_persist_10_state_TREND_HOSTILE_zero` | Hostile trend primary; weak breadth and stress/weak breadth as confirmation | h20 primary, h10 review flag | 0.028418 | 0.568681 | 0.096397 | 0.346997 | 1.00 / 1.00 | Max baseline corr 0.269307 | Turnover near monitoring ceiling; related variants; state labels and inactive handling must remain fixed |
| `participation_breadth_repair_under_hostile_trend` | Breadth repair under hostile trend | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` | `strict_weak_breadth_rebalance_10` | Weak breadth under hostile trend; stress confirmation via recent-stress variant | h20 | 0.030720 | 0.580537 | 0.013619 | 0.142993 | 1.00 / 1.00 | Corr to prior participation/liquidity 0.034492; max reversal corr 0.015265 | Lower active coverage; peer variants are related; needs integration-review confirmation |
| `volatility_compression_after_stress_stabilization` | Volatility / stress-transition stabilization | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`; recommended `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` | `rebalance_5` | Post-stress volatility compression and stabilization | h20 | 0.028391 | 0.574413 | 0.022092 | 0.189704 | 1.00 / 1.00 | Max inventory corr 0.047430; max reversal corr 0.057781 | Window concentration; recent-window fragility; controls have weaker recent-window behavior |

## Ecosystem Map

The current inventory has three distinct but related functions:

- `participation_liquidity_state_shift_20_60` identifies repair in participation and liquidity behavior under hostile trend or weak-breadth states.
- `participation_breadth_repair_under_hostile_trend` isolates a narrower breadth-repair mechanism with very low overlap to the first inventory candidate.
- `volatility_compression_after_stress_stabilization` adds a new volatility/stress-transition mechanism that is structurally distinct from the participation cluster.

The inventory is not yet broad. It remains concentrated in conditional repair and stabilization, mostly at h20, with activation states that cluster around hostile trend, weak breadth, drawdown, panic/liquidity stress, and post-stress stabilization.

Turnover is acceptable only after explicit churn control. The successful candidates improved through rank persistence, rebalance intervals, or mild smoothing. Their improvements did not come from simply suppressing all exposure; they came from reducing rank churn while preserving state-specific behavior.

Active coverage is adequate for research but fragile enough to require monitoring. The breadth candidate is especially conditional, and the volatility/stress candidate has meaningful window-concentration risk.

## Common Traits Of Survivors

The strongest candidates share several traits:

- They are conditional repair or stabilization mechanisms, not universal standalone alphas.
- Their state semantics are interpretable: hostile trend, weak breadth, stress, or stabilization after stress.
- h20 is the most coherent horizon, while shorter horizons are mainly diagnostic or control views.
- Turnover improvement comes from reducing rank churn through rebalance, smoothing, or persistence filters.
- Baseline similarity is low to moderate, especially relative to reversal and momentum baselines.
- They have fixed primary representations and control variants rather than open-ended parameter grids.
- They survived stricter research validation only after the project stopped searching broadly and moved to small fixed candidate sets.

The most important survivor pattern is that state semantics mattered more than raw signal novelty. The candidates that worked had a clear answer to: "What market condition makes this mechanism meaningful?"

## Repeated Failure Modes

Several failure modes have now repeated across Track B:

- Structurally novel but not predictive: `dispersion_recovery_stability_after_stress` and `temporal_asymmetry_stress_absorption` were distinct, but weak or negative.
- Event concepts remain noisy: `event_quality_persistence_after_gap_settlement` introduced a new event-quality angle, but h20 IC was weak, turnover and missingness were high, and raw gap similarity remained moderate.
- Dispersion topology was not enough: the stress-recovery dispersion formulation did not collapse into existing factors, but stress/regime attribution was mostly negative.
- Temporal path-shape was not enough: the temporal asymmetry test avoided reversal, momentum, and volatility-stabilization duplication, but empirical h20 behavior was negative.
- Raw continuation repeatedly failed: earlier v3 diagnostics showed continuation and leadership candidates often suffered from overextension and late-entry momentum decay.
- Simple inversion is not a solution: inverted continuation generally becomes another reversal proxy rather than a new mechanism.
- h20 concentration is real: the inventory's strongest evidence is h20-heavy, which makes horizon-dependency monitoring important.
- Strict state gates can become too sparse: high IC under narrow states is not useful if active coverage and active-window support are inadequate.

## Expansion v2 One-By-One Lessons

| Concept | Final Status | Main Lesson |
| --- | --- | --- |
| `dispersion_recovery_stability_after_stress` | `REJECT_RESEARCH` | Structurally distinct, but h20 IC was negative and stress/regime attribution did not support refinement. |
| `event_quality_persistence_after_gap_settlement` | `CONDITIONAL_ONLY_RESEARCH` | Event-quality remains a plausible future family, but this formulation had weak IC, high turnover, high missingness, and moderate raw gap similarity. |
| `temporal_asymmetry_stress_absorption` | `CONDITIONAL_ONLY_RESEARCH` | Temporal/path-shape behavior was orthogonal, but empirically weak and not ready for refinement. |

The key conclusion is that inventory expansion should not reward novelty by itself. Novelty without predictive evidence, state coherence, and turnover discipline should stay outside the active inventory.

## Inventory Concentration Risks

The current ecosystem has several concentration risks:

- Participation/liquidity/breadth clustering: two of the three inventory candidates live in adjacent repair mechanisms.
- Hostile/stress state dependence: all three candidates are most meaningful in hostile, weak-breadth, stress, or post-stress states.
- h20 horizon concentration: h20 is the dominant validation horizon across the inventory.
- Volatility/stress overlap risk: future volatility or stress-transition concepts may duplicate the third inventory candidate unless overlap monitoring is explicit.
- Active coverage fragility: conditional candidates can look strong while being too sparse for stable future construction.
- Window concentration: the volatility/stress candidate requires monitoring because one validation window contributed a large share of its positive h20 IC.
- Control-variant confusion: confirmation variants should not be mistaken for independent alpha sources.

These risks do not invalidate the inventory. They define what must be monitored before construction-layer research.

## What The Inventory Implicitly Believes

The current inventory expresses several working market beliefs:

- Conditional repair and stabilization appear stronger than naive continuation.
- Participation, breadth, and liquidity repair have been more durable than abstract topology features.
- Orthogonality alone is insufficient; structurally distinct signals can still be empirically weak.
- State semantics matter more than raw signal novelty.
- Turnover quality matters; reducing rank churn can preserve useful conditional behavior.
- Stress and hostile-state activation can reveal useful edges, but also creates sample-size and window-concentration risk.
- Failed signals are useful evidence because they map which parts of the mechanism space are not currently productive.

These beliefs should remain provisional. They are research conclusions, not production assumptions.

## Mechanism Family Implications

Families deserving additional work:

- Participation, breadth, and liquidity repair: continue only if new concepts add genuinely different state semantics or construction roles.
- Volatility/stress transition: keep the current candidate under guardrails before adding more concepts in the same family.
- Event-quality structures: keep as a future family, but redesign around lower turnover, lower missingness, and cleaner separation from raw gap continuation/reversal.
- Non-price liquidity transitions: remain interesting if they avoid becoming price-rank or reversal proxies.

Families to pause:

- Dispersion recovery topology in the tested stress-recovery form.
- Temporal path-shape stress absorption in the tested form.
- Raw continuation, raw breakout continuation, simple inversion, and price-rank variants.
- Broad nonlinear state scores without clear semantics.
- Over-fragmented state slicing that creates attractive but sparse active windows.

## Next Research Implications

Future discovery should remain one-by-one and inventory-aware. Every new concept should answer:

- What inventory gap does this mechanism fill?
- What current inventory candidate could it duplicate?
- What state semantics make it economically plausible?
- How much active coverage is expected?
- What baseline would falsify the concept as redundant?
- What turnover behavior would make it unusable?

Before another discovery wave, the inventory layer should be strengthened with:

- Candidate-level active-window monitoring.
- Co-activation and overlap maps across inventory candidates.
- Recent-window and one-window-dominance monitoring.
- h20/h10 dependency checks.
- Turnover drift tracking.
- Similarity drift against reversal, momentum, volatility, and current inventory candidates.
- Rebuild/equivalence tests for each primary inventory representation.
- A clear downgrade/removal protocol for inventory candidates whose guardrails fail.

## Research Maturity Assessment

The platform can now reliably:

- Run isolated research batches without production contamination.
- Move from broad discovery to focused refinement without forcing survivors.
- Diagnose reversal, momentum, and inventory overlap.
- Evaluate conditional state semantics.
- Track turnover and rank-churn effects.
- Use WFV-style persistence and sign consistency as research filters.
- Preserve candidate lifecycle documentation from discovery through integration review.
- Reject structurally interesting but empirically weak ideas.

Remaining weak points:

- Inventory monitoring is still more documented than operationalized.
- Active-state WFV remains diagnostic rather than a formal promotion path.
- Co-activation across conditional candidates is not yet a first-class artifact.
- Construction-layer semantics are intentionally not implemented.
- Horizon concentration around h20 has not been solved.
- Small-sample and window-concentration risks remain meaningful.
- The inventory has not yet been tested in a construction layer, portfolio layer, or broader universe setting.

Before future construction-layer research, the project should have:

- A Conditional Alpha Inventory v2 with the three current candidates and explicit guardrails.
- Rebuild/equivalence tests for primary variants.
- Monitoring artifacts for activation, overlap, turnover, horizon stability, and recent-window behavior.
- A co-activation matrix that shows whether inventory candidates fire together or diversify state exposure.
- A construction-semantics design that consumes inventory candidates, not raw discovery outputs.
- A continuing hard boundary between research inventory and production/trading logic.

## Recommended Next Step

The next highest-value step is to create a Conditional Alpha Inventory v2 monitoring and governance package before adding more candidates.

Recommended immediate work:

1. Update the inventory documentation and CSV to include all three candidates and their guardrails.
2. Add a research-only monitoring plan for active coverage, recent-window behavior, one-window dominance, turnover drift, and overlap drift.
3. Create a co-activation/overlap diagnostic design for the current three-candidate inventory.

New discovery should resume only after the inventory monitoring layer is clearer. When it resumes, it should remain small, one-by-one, and explicitly tied to missing inventory dimensions rather than isolated candidate excitement.

