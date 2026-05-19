# Track B Expansion v2 Inventory-Aware Concept Screening

## Executive Takeaway

Track B Expansion v2 should remain a design-only, inventory-aware screening phase. The current Conditional Alpha Inventory has progressed beyond raw discovery and now contains three governed research candidates:

| Candidate | Mechanism | Current Role |
| --- | --- | --- |
| `participation_liquidity_state_shift_20_60` | Participation/liquidity repair under hostile or weak-breadth states | `INVENTORY_ACTIVE_RESEARCH` |
| `participation_breadth_repair_under_hostile_trend` | Breadth repair under hostile trend | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` |
| `volatility_compression_after_stress_stabilization` | Volatility/stress-transition stabilization | `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` |

The next research frontier should not be another broad alpha search. It should be a small, focused inventory-expansion batch that tests mechanisms the inventory does not yet represent: dispersion recovery, temporal asymmetry, event-quality persistence, topology transitions, and volatility-dispersion interaction repair.

Recommended next implementation style: **small/focused**, with 2-3 concepts, one simple formulation per concept, no parameter grid.

## Current Inventory Concentration Risks

The inventory is more mature than the raw discovery stack, but it has visible concentration risks:

| Risk | Current Evidence | Why It Matters |
| --- | --- | --- |
| Participation/liquidity clustering | Two of three candidates are participation, liquidity, or breadth repair mechanisms | Future construction could overstate diversification if both candidates respond to related hostile-market participation states |
| Hostile-state dependence | Existing candidates mostly activate during hostile trend, weak breadth, stress, or post-stress states | The inventory lacks mechanisms for neutral-state transition, event-quality persistence, and recovery topology |
| h20 concentration | Validated candidates are primarily h20-oriented | Future construction may become horizon-concentrated even if signal mechanisms differ |
| Conditional activation overlap | Weak breadth, trend-hostile, stress, and stabilization states recur across candidates | Co-activation should be monitored before any construction layer is designed |
| Recent-window fragility | The volatility/stress candidate is structurally distinct, but still carries recent-window and window-concentration guardrails | New volatility-adjacent concepts must not simply repackage the same stabilization behavior |
| Repair/stabilization bias | Current candidates mostly describe repair after adverse states | The inventory lacks event-quality, temporal asymmetry, and cross-sectional topology mechanisms |

## Missing Inventory Dimensions

The strongest gaps are not more participation repair variants. The missing dimensions are:

- **Dispersion recovery:** cross-sectional dispersion moving from disordered stress toward stable opportunity structure.
- **Temporal asymmetry:** different behavior between fast deterioration, absorption, and recovery timing.
- **Event-quality persistence:** gaps or event shocks that settle into durable quality rather than raw continuation or reversal.
- **Topology-transition behavior:** changes in the structure of cross-sectional ranks, tails, and stability rather than level-only signals.
- **Nonlinear stabilization:** simple multi-stage state logic that distinguishes stress, stabilization, and overextension without creating a giant state score.
- **Post-stress normalization:** behavior after stress begins to normalize, separate from volatility compression alone.
- **Volatility-dispersion interaction:** cases where volatility normalization and cross-sectional dispersion repair jointly identify a cleaner state.

## Screening Principles

Every concept below is screened by one central question:

> Why does the Conditional Alpha Inventory need this mechanism family?

Screening constraints:

- Design only; no formulas, no validation, no production registration.
- Prefer one simple future formulation per concept.
- Avoid raw continuation, reversal inversion, price-rank variants, generic momentum, and pseudo-orthogonal variants.
- Prefer mechanisms that improve future construction-layer optionality by filling a distinct inventory gap.
- Treat high conceptual overlap with existing participation/liquidity candidates as a reason to hold or discard.

## Concept Screen

### 1. `dispersion_recovery_stability_after_stress`

| Field | Assessment |
| --- | --- |
| Mechanism family | Dispersion-transition / cross-sectional recovery topology |
| Inventory gap addressed | Dispersion recovery and topology-transition behavior |
| Economic intuition | After stress, the market may move from broad disorder to a more stable cross-sectional opportunity set. Assets showing improved rank stability during dispersion normalization may represent cleaner recovery structure than simple price continuation. |
| State-transition thesis | Elevated dispersion followed by dispersion stabilization and reduced rank churn may create a more reliable conditional edge. |
| Why inventory needs this mechanism | Current inventory has participation and volatility repair, but not cross-sectional dispersion recovery. |
| Difference from current inventory | Does not rely primarily on breadth repair, liquidity repair, or volatility compression; it studies cross-sectional order after stress. |
| Difference from reversal/momentum | Avoids fading price extremes or chasing leaders; focuses on stabilization of cross-sectional structure. |
| Expected activation semantics | Recent high dispersion followed by dispersion normalization and improving rank stability. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Low to moderate if rank-stability confirmation is used |
| Expected active coverage | Moderate |
| Expected orthogonality | High |
| Likely failure mode | Could collapse into volatility compression if dispersion is defined too broadly; may be weak in fast recoveries. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | IMPLEMENT_NEXT |

### 2. `event_quality_persistence_after_gap_settlement`

| Field | Assessment |
| --- | --- |
| Mechanism family | Event-quality state transition |
| Inventory gap addressed | Event-quality persistence |
| Economic intuition | Not all gaps are continuation or reversal events. Some settle into controlled range, stable volume, and clean follow-through, which may distinguish durable event quality from noisy event chase. |
| State-transition thesis | A large event move followed by contained volatility, controlled turnover, and non-chaotic follow-through may produce a cleaner conditional edge. |
| Why inventory needs this mechanism | The inventory has no event-quality candidate and no mechanism that explicitly handles discrete shocks. |
| Difference from current inventory | It is event-anchored rather than participation-repair or stress-normalization anchored. |
| Difference from reversal/momentum | It should not fade the gap or chase the gap mechanically; the edge comes from post-event settlement quality. |
| Expected activation semantics | Gap/event shock, followed by 2-5 day settlement quality and acceptable volume/range behavior. |
| Expected horizon | h5-h20 |
| Expected turnover profile | Moderate |
| Expected active coverage | Moderate to sparse |
| Expected orthogonality | High if missingness and event sparsity are controlled |
| Likely failure mode | Sparse activation, high turnover around event clusters, or accidental gap-continuation exposure. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | IMPLEMENT_NEXT |

### 3. `temporal_asymmetry_stress_absorption`

| Field | Assessment |
| --- | --- |
| Mechanism family | Temporal asymmetry / stress absorption |
| Inventory gap addressed | Temporal asymmetry and post-stress behavior |
| Economic intuition | The timing of stress absorption may matter more than the price level. Assets that absorb stress intraperiod or across short windows without disorder may behave differently from simple reversal or momentum names. |
| State-transition thesis | During market stress, repeated absorption followed by stable closes or controlled overnight/intraday behavior may indicate resilient structure. |
| Why inventory needs this mechanism | Current candidates identify hostile or stabilizing states, but not the timing asymmetry of stress absorption. |
| Difference from current inventory | It focuses on time-path quality, not participation breadth, liquidity repair, or volatility compression. |
| Difference from reversal/momentum | It should not require buying losers or leaders; it studies how stress is absorbed. |
| Expected activation semantics | Stress or volatility spike state with evidence of absorption and reduced same-window disorder. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Low to moderate |
| Expected active coverage | Moderate |
| Expected orthogonality | High |
| Likely failure mode | Can accidentally become a reversal proxy if defined around large negative moves rather than absorption behavior. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | IMPLEMENT_NEXT |

### 4. `volatility_dispersion_interaction_repair`

| Field | Assessment |
| --- | --- |
| Mechanism family | Volatility-dispersion interaction |
| Inventory gap addressed | Interaction between volatility normalization and dispersion repair |
| Economic intuition | Volatility compression alone may be too broad. A cleaner transition may occur when volatility stabilizes while cross-sectional dispersion also repairs, indicating lower systemic stress and more coherent stock selection. |
| State-transition thesis | Joint volatility stabilization and dispersion repair may define a more robust post-stress state than either state alone. |
| Why inventory needs this mechanism | It tests whether the current volatility/stress candidate can be complemented by an interaction mechanism rather than another standalone vol variant. |
| Difference from current inventory | It extends beyond pure volatility compression and beyond participation repair by requiring cross-sectional structure recovery. |
| Difference from reversal/momentum | It is state-topology based, not price-extreme based. |
| Expected activation semantics | Recent volatility stress plus elevated dispersion, followed by both volatility and dispersion stabilization. |
| Expected horizon | h20 |
| Expected turnover profile | Low |
| Expected active coverage | Moderate to sparse |
| Expected orthogonality | Medium-high; overlap with the volatility candidate must be monitored. |
| Likely failure mode | Could be redundant with `volatility_compression_after_stress_stabilization` or too sparse if both gates are strict. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | IMPLEMENT_NEXT |

### 5. `cross_sectional_recovery_topology_without_breadth`

| Field | Assessment |
| --- | --- |
| Mechanism family | Cross-sectional recovery topology |
| Inventory gap addressed | Topology-transition behavior independent of breadth repair |
| Economic intuition | Some recoveries may be visible in rank distribution, tail compression, and cross-sectional order before broad breadth improves. |
| State-transition thesis | Improving cross-sectional topology after drawdown may identify recovery quality without relying on weak-breadth activation. |
| Why inventory needs this mechanism | It would diversify away from breadth and participation repair while still addressing recovery states. |
| Difference from current inventory | Uses topology and rank-distribution structure rather than breadth activation or liquidity participation. |
| Difference from reversal/momentum | Should not be based on price winners or losers; the target is improving cross-sectional order. |
| Expected activation semantics | Drawdown or high-dispersion state followed by reduced tail disorder and improving rank stability. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Low |
| Expected active coverage | Moderate |
| Expected orthogonality | Medium-high |
| Likely failure mode | May be difficult to distinguish from broad market recovery or dispersion repair. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | HOLD_FOR_LATER |

### 6. `post_stress_normalization_without_risk_on_chase`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-stress normalization |
| Inventory gap addressed | Post-stress normalization separate from volatility compression |
| Economic intuition | After panic or drawdown acceleration, some names normalize without entering broad risk-on chase behavior. This may capture stabilization quality without late momentum exposure. |
| State-transition thesis | Stress-to-normalization behavior can be useful if it avoids overextension and broad risk-on beta. |
| Why inventory needs this mechanism | The current inventory has stress stabilization, but not a dedicated normalization-without-chase mechanism. |
| Difference from current inventory | Separates recovery normalization from participation repair and pure volatility compression. |
| Difference from reversal/momentum | Avoids buying price extension or fading stress directly; focuses on stabilization without chase. |
| Expected activation semantics | Panic or drawdown acceleration followed by range normalization and low overextension. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Low |
| Expected active coverage | Moderate |
| Expected orthogonality | Medium |
| Likely failure mode | Could overlap with the volatility/stress candidate or become too defensive during fast recoveries. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | HOLD_FOR_LATER |

### 7. `event_aftershock_decay_quality`

| Field | Assessment |
| --- | --- |
| Mechanism family | Event-quality / temporal decay |
| Inventory gap addressed | Event aftershock decay and quality persistence |
| Economic intuition | After a discrete event, excess range and volatility aftershocks may decay at different speeds. Controlled aftershock decay may indicate cleaner information absorption. |
| State-transition thesis | Event shock followed by orderly volatility decay and stable volume participation may be more useful than raw gap continuation. |
| Why inventory needs this mechanism | It would create a second event-quality angle if event settlement proves promising. |
| Difference from current inventory | Event-time based, not hostile-state or breadth repair based. |
| Difference from reversal/momentum | Focuses on post-event quality and decay, not the direction of the event move itself. |
| Expected activation semantics | Event/gap shock followed by declining range aftershocks and stable participation. |
| Expected horizon | h5-h20 |
| Expected turnover profile | Moderate |
| Expected active coverage | Sparse to moderate |
| Expected orthogonality | High if event sparsity is manageable |
| Likely failure mode | Sparse samples and unstable event definitions. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | HOLD_FOR_LATER |

### 8. `state_gated_relative_stability_without_price_rank`

| Field | Assessment |
| --- | --- |
| Mechanism family | State-gated relative stability |
| Inventory gap addressed | Relative stability without price-rank dependence |
| Economic intuition | During hostile or dispersive states, stable relative ordering may be valuable even when raw price rank is misleading. |
| State-transition thesis | A state-gated stability feature may identify names with durable relative structure during disorder. |
| Why inventory needs this mechanism | It could add a low-turnover stability sleeve if it avoids price-rank redundancy. |
| Difference from current inventory | Stability-first rather than participation/breadth/volatility transition first. |
| Difference from reversal/momentum | Must be constructed from rank stability or non-price cross-sectional stability, not price leadership. |
| Expected activation semantics | High dispersion, trend-hostile, or stress states with stable relative ordering. |
| Expected horizon | h20 |
| Expected turnover profile | Low |
| Expected active coverage | Moderate |
| Expected orthogonality | Medium |
| Likely failure mode | Hidden momentum/trend-quality exposure or weak standalone economics. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | HOLD_FOR_LATER |

### 9. `activation_topology_transition_map`

| Field | Assessment |
| --- | --- |
| Mechanism family | Activation topology / diagnostics-first |
| Inventory gap addressed | Co-activation, state overlap, and inventory construction optionality |
| Economic intuition | Before construction, the inventory needs to understand how conditional mechanisms co-activate across states. This may be more useful as a diagnostic layer than as a signal. |
| State-transition thesis | The topology of activation transitions may identify when inventory candidates are complementary or redundant. |
| Why inventory needs this mechanism | It would support future construction-layer design by mapping co-activation risk. |
| Difference from current inventory | It is not a raw alpha mechanism; it is an inventory governance and construction-readiness concept. |
| Difference from reversal/momentum | Not a price signal. |
| Expected activation semantics | Derived from candidate activation transitions and state overlap. |
| Expected horizon | Not horizon-specific |
| Expected turnover profile | Not applicable |
| Expected active coverage | Not applicable |
| Expected orthogonality | High as a governance diagnostic |
| Likely failure mode | Not directly testable as alpha; should not be forced into candidate discovery. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | HOLD_FOR_LATER |

### 10. `nonlinear_stabilization_two_stage_gate`

| Field | Assessment |
| --- | --- |
| Mechanism family | Nonlinear stabilization / multi-stage transition |
| Inventory gap addressed | Nonlinear state transition without giant state scores |
| Economic intuition | Some conditional edges may require a simple sequence: stress first, stabilization second, no overextension third. |
| State-transition thesis | A two-stage gate can separate noisy stress from actionable stabilization without broad nonlinear scoring. |
| Why inventory needs this mechanism | It could reduce false activation and improve semantic clarity for future conditional candidates. |
| Difference from current inventory | Focuses on activation semantics rather than a new raw alpha input. |
| Difference from reversal/momentum | The mechanism is state sequence quality, not price direction. |
| Expected activation semantics | Explicit two-stage state transition with a simple overextension veto. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Low |
| Expected active coverage | Sparse to moderate |
| Expected orthogonality | Medium |
| Likely failure mode | Over-fragmented state slicing and overfit if too many stages are added. |
| Implementation complexity | Medium-high |
| Inventory-complementarity score | 3/5 |
| Priority | LOW |
| Recommendation | HOLD_FOR_LATER |

### 11. `range_efficiency_recovery_without_price_rank`

| Field | Assessment |
| --- | --- |
| Mechanism family | Range efficiency / temporal structure |
| Inventory gap addressed | Temporal quality and non-price-rank recovery |
| Economic intuition | Recovery quality may appear as improving range efficiency and reduced noisy range expansion, not just price strength. |
| State-transition thesis | Names with improving range efficiency after disorder may be cleaner candidates than names with price extension. |
| Why inventory needs this mechanism | It could add an OHLCV temporal-structure mechanism distinct from breadth and volatility repair. |
| Difference from current inventory | Uses range-quality transition rather than participation, breadth, or volatility state alone. |
| Difference from reversal/momentum | Must avoid ranking by price move; focuses on quality of range behavior. |
| Expected activation semantics | Recent disorder or choppy trend followed by improving range efficiency and stable closes. |
| Expected horizon | h10-h20 |
| Expected turnover profile | Moderate |
| Expected active coverage | Moderate |
| Expected orthogonality | Medium |
| Likely failure mode | Hidden trend-quality exposure or weak signal-to-noise. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 3/5 |
| Priority | LOW |
| Recommendation | HOLD_FOR_LATER |

### 12. `dispersion_breakdown_avoidance_filter`

| Field | Assessment |
| --- | --- |
| Mechanism family | Dispersion risk suppressor |
| Inventory gap addressed | Defensive avoidance rather than alpha generation |
| Economic intuition | Avoiding names during dispersion breakdown may reduce drawdown, but this is more likely a future risk overlay than a conditional alpha candidate. |
| State-transition thesis | Dispersion breakdown can signal fragile cross-sectional opportunity. |
| Why inventory needs this mechanism | It may be useful later for construction-layer risk control, but it does not justify candidate inventory space now. |
| Difference from current inventory | Risk suppressor, not alpha mechanism. |
| Difference from reversal/momentum | Not price-directional. |
| Expected activation semantics | Rapid dispersion expansion and tail disorder. |
| Expected horizon | h5-h20 |
| Expected turnover profile | Low |
| Expected active coverage | Sparse |
| Expected orthogonality | Medium |
| Likely failure mode | Accidental de-risking mistaken for alpha, sparse activation, and poor standalone interpretation. |
| Implementation complexity | Low |
| Inventory-complementarity score | 2/5 |
| Priority | LOW |
| Recommendation | DISCARD_CONCEPT |

## Promising Inventory-Expansion Concepts

The 5-8 most promising concepts are:

1. `dispersion_recovery_stability_after_stress`
2. `event_quality_persistence_after_gap_settlement`
3. `temporal_asymmetry_stress_absorption`
4. `volatility_dispersion_interaction_repair`
5. `cross_sectional_recovery_topology_without_breadth`
6. `post_stress_normalization_without_risk_on_chase`
7. `event_aftershock_decay_quality`
8. `state_gated_relative_stability_without_price_rank`

Top 2-3 future implementation candidates:

1. `dispersion_recovery_stability_after_stress`
2. `event_quality_persistence_after_gap_settlement`
3. `temporal_asymmetry_stress_absorption`

`volatility_dispersion_interaction_repair` is also attractive, but should be considered only after checking whether it is too close to `volatility_compression_after_stress_stabilization`.

## Still-Underrepresented Mechanism Families

The inventory remains underrepresented in:

- Event-quality and event-settlement mechanisms.
- Temporal asymmetry and stress-absorption mechanisms.
- Dispersion recovery and cross-sectional topology mechanisms.
- Post-stress normalization that is not simply volatility compression.
- Conditional state interaction logic that remains interpretable and low-dimensional.

## Future Discovery Recommendation

Future discovery should remain **small and focused**. The next implementation batch should test at most 2-3 concepts, with one simple formulation per concept:

1. `dispersion_recovery_stability_after_stress`
2. `event_quality_persistence_after_gap_settlement`
3. `temporal_asymmetry_stress_absorption`

Do not run a broad v7-style search yet. The inventory now has enough governance maturity that candidate count is less important than mechanism diversity and clean state semantics.

## Inventory Risks To Monitor Before Further Expansion

Before adding more candidates to the inventory, monitor:

- Co-activation overlap between hostile trend, weak breadth, stress, and volatility stabilization states.
- h20 concentration across all inventory candidates.
- Whether new dispersion concepts duplicate the volatility/stress candidate.
- Whether event-quality concepts become raw gap continuation or gap reversal.
- Whether temporal asymmetry concepts become disguised short-term reversal.
- Active coverage and window concentration, especially for sparse event or stress mechanisms.
- Baseline similarity drift versus reversal, momentum, and existing inventory candidates.
- Excessive refinement search after a first promising result.

## Final Recommendation

Track B Expansion v2 should proceed as a design-only inventory expansion screen, then later move into a small focused implementation batch only if approved. The strongest next frontier is not another participation-repair family. It is a targeted test of **dispersion recovery**, **event-quality persistence**, and **temporal asymmetry/stress absorption** as distinct conditional mechanism families.

No production logic, gates, schemas, thresholds, survivor/watchlist state, portfolio construction, ML logic, or production Conditional-Alpha paths should change from this screening phase.
