# Track B Expansion v3 Design Screening

## Executive Takeaway

Track B Expansion v3 should be a design-only, inventory-aware screening package. Its purpose is to identify candidate concepts that diversify the Conditional Alpha Inventory ecosystem, not to reward isolated signal novelty.

The current inventory is useful but clustered:

| candidate | monitoring status | main watch item |
| --- | --- | --- |
| `participation_liquidity_state_shift_20_60` | `WATCH_MONITOR` | Latest rolling h20 IC is much weaker than full-sample h20 IC. |
| `participation_breadth_repair_under_hostile_trend` | `HEALTHY_ACTIVE_RESEARCH` | Cleanest current monitoring profile, but sparse and co-active with participation/liquidity repair. |
| `volatility_compression_after_stress_stabilization` | `WATCH_MONITOR` | Weak recent-window positive rate and one-window concentration guardrail issue. |

Expansion v3 should deliberately look outside hostile/stress h20 repair. The strongest roadmap is calmer-state, neutral-state, medium-coverage, and non-h20 conditional mechanisms that can later be implemented one-by-one.

No candidates were implemented. No discovery, validation, refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production logic change was performed.

## Sources Reviewed

- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `docs/research_notes/inventory_ecosystem_review_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v1.md`
- `docs/research_notes/track_b_expansion_v2_inventory_aware_screening.md`
- `docs/research_notes/dispersion_recovery_stability_after_stress_v1.md`
- `docs/research_notes/event_quality_persistence_after_gap_settlement_v1.md`
- `docs/research_notes/temporal_asymmetry_stress_absorption_v1.md`
- `docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md`
- `docs/research_notes/participation_breadth_repair_conditional_validation.md`
- `docs/research_notes/volatility_compression_stress_stabilization_integration_review.md`

## Current Inventory Concentration Risks

| risk | current evidence | v3 design implication |
| --- | --- | --- |
| h20 concentration | All three inventory candidates are h20-centered. | Prefer h5, h10, or h10-h15 concepts; h20 can remain diagnostic, not the design anchor. |
| hostile/stress dependence | Current positive state slices cluster around hostile trend, weak breadth, drawdown, panic/liquidity stress, volatility spike, and post-stress stabilization. | Prefer neutral, calm, low-volatility, normalized, and non-hostile states. |
| participation/breadth co-activation | Monitoring v1 showed concentrated co-activation between the participation/liquidity and breadth-repair candidates. | Avoid new weak-breadth repair clones; require lower expected co-activation with those candidates. |
| recent-window fragility | Liquidity state shift has weak latest rolling h20 IC; volatility compression has weak recent positive rate. | Avoid concepts whose thesis depends on older stress windows or one exceptional validation window. |
| one-window dominance risk | Volatility/stress candidate remains under guardrail watch. | Prefer mechanisms with medium active coverage and routine active-window support. |
| hidden mechanism clustering | Low value correlation does not guarantee ecosystem diversity. | Screen for state, horizon, activation, and semantic diversity, not just low pairwise correlation. |

## Screening Principles

Expansion v3 concepts should answer:

- Which inventory concentration risk does this reduce?
- Why should it activate away from hostile/stress repair states?
- Why is the expected horizon not just h20?
- Why is it not raw continuation, simple reversal, or price-rank momentum?
- What would falsify it as a useful inventory complement?
- How would it improve future construction-layer optionality without implementing construction logic now?

Concepts below are design candidates only. Names are stable research handles, not implemented signal names.

## Concept Screen

| concept | family | gap addressed | horizon | active coverage | turnover | complementarity | priority | recommendation |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| `neutral_accumulation_without_breakout` | neutral-state accumulation | neutral/calm state, non-h20, lower co-activation | h5-h10 | medium | low-medium | 5 | HIGH | `IMPLEMENT_NEXT` |
| `calm_regime_relative_stability_10` | calm-regime relative stability | calm regime, h10, medium coverage | h10 | medium-high | low | 5 | HIGH | `IMPLEMENT_NEXT` |
| `quiet_liquidity_accumulation_non_hostile` | quiet liquidity accumulation | non-hostile participation quality, medium coverage | h5-h10 | medium | medium | 5 | HIGH | `IMPLEMENT_NEXT` |
| `low_volatility_quality_persistence_10` | low-vol quality persistence | low-volatility calm state, h10 | h10 | medium | low | 4 | HIGH | `IMPLEMENT_NEXT` |
| `post_normalization_continuation_resolved_stress` | post-normalization continuation | after stress has resolved, h10-h15 | h10-h15 | medium | low-medium | 4 | HIGH | `IMPLEMENT_NEXT` |
| `non_hostile_participation_quality_10` | non-hostile participation quality | participation quality without hostile repair | h10 | medium | medium | 4 | MEDIUM | `IMPLEMENT_NEXT` |
| `low_dispersion_leadership_quality_10` | low-dispersion leadership quality | calm leadership, non-stress | h10 | medium | medium | 4 | MEDIUM | `HOLD_FOR_LATER` |
| `volatility_normalization_without_panic_trigger` | volatility normalization | normalized vol without panic/stress trigger | h5-h10 | medium-high | low-medium | 4 | MEDIUM | `HOLD_FOR_LATER` |
| `cross_sectional_stability_outside_hostile_states` | cross-sectional stability | neutral-state rank stability | h10-h15 | medium | low | 4 | MEDIUM | `HOLD_FOR_LATER` |
| `medium_horizon_fundamental_proxy_stability` | medium-horizon stability proxy | h15/h30 horizon diversity | h15-h30 | medium-high | low | 3 | MEDIUM | `HOLD_FOR_LATER` |
| `range_compression_quality_in_calm_regime` | calm range quality | low-vol range quality, non-stress | h5-h10 | medium | medium | 3 | LOW | `HOLD_FOR_LATER` |
| `redesigned_event_quality_low_turnover` | redesigned event quality | event family redesigned away from v2 flaws | h5-h10 | sparse-medium | medium | 2 | LOW | `DISCARD_CONCEPT` |

### 1. `neutral_accumulation_without_breakout`

| Field | Assessment |
| --- | --- |
| Mechanism family | Neutral-state accumulation mechanisms |
| Inventory gap addressed | Reduces hostile/stress dependence, adds h5-h10 horizon diversity, and targets lower co-activation with current repair candidates. |
| Economic intuition | Some names may accumulate quietly during neutral market states before visible breakout or stress repair. Controlled volume participation and stable closes can indicate informed accumulation without relying on price-rank momentum. |
| State/activation thesis | Activate during non-hostile, non-panic, non-weak-breadth market states with contained range behavior and improving quiet participation. |
| Expected horizon | h5-h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Low to medium if accumulation confirmation uses smoothing or rebalance control. |
| Why it differs from current inventory | It is not hostile trend, weak breadth, drawdown, panic, or post-stress stabilization; it is a neutral-state accumulation thesis. |
| Why it differs from reversal/momentum | It should not buy losers or chase leaders; price extension should be a veto or neutral control, while quiet participation quality is the mechanism. |
| Why it improves ecosystem diversification | Adds calm/neutral activation and shorter horizon optionality with likely lower co-activation against the two participation/breadth repair candidates. |
| Likely failure mode | Can become disguised low-volume drift or price breakout continuation if the no-breakout constraint is weak. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

### 2. `calm_regime_relative_stability_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Calm-regime relative stability mechanisms |
| Inventory gap addressed | Adds calm-state, h10-centered, medium-to-high coverage exposure. |
| Economic intuition | In calm regimes, stable relative ordering and low cross-sectional rank churn may carry information because capital can differentiate quality without stress-driven noise. |
| State/activation thesis | Activate in non-hostile, low-to-normal volatility regimes where rank stability is high and broad market participation is neither weak nor euphoric. |
| Expected horizon | h10 |
| Expected active coverage | Medium-high |
| Expected turnover profile | Low |
| Why it differs from current inventory | Current candidates are repair/stabilization under fragile states; this tests relative stability when the market is already orderly. |
| Why it differs from reversal/momentum | It focuses on persistence of relative order and low churn, not price return rank or recent overextension. |
| Why it improves ecosystem diversification | Provides a calm-regime anchor and future construction optionality for non-stress allocation windows. |
| Likely failure mode | Could be too weak because calm regimes have lower dispersion and less cross-sectional opportunity. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

### 3. `quiet_liquidity_accumulation_non_hostile`

| Field | Assessment |
| --- | --- |
| Mechanism family | Quiet liquidity accumulation |
| Inventory gap addressed | Adds non-hostile liquidity/participation quality without another weak-breadth repair clone. |
| Economic intuition | Liquidity quality can improve quietly outside stress. Names with stable dollar participation, lower impact proxy, and contained range may represent accumulation rather than reactive repair. |
| State/activation thesis | Activate when market trend is neutral or constructive, breadth is not weak, and asset-level liquidity quality improves without large price extension. |
| Expected horizon | h5-h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Medium |
| Why it differs from current inventory | It uses liquidity quality in normal states, not hostile-state participation repair. |
| Why it differs from reversal/momentum | It should be volume/liquidity-quality led with explicit guards against price-rank continuation and reversal. |
| Why it improves ecosystem diversification | Keeps the useful liquidity intuition but moves it into a different state, horizon, and activation topology. |
| Likely failure mode | May collapse into the existing participation/liquidity family if non-hostile state controls are too loose. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

### 4. `low_volatility_quality_persistence_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Low-volatility quality persistence |
| Inventory gap addressed | Adds low-volatility calm-state behavior and h10 horizon diversity. |
| Economic intuition | Sustained low realized volatility with stable rank behavior may mark names where information is being incorporated smoothly rather than through stress compression. |
| State/activation thesis | Activate in low-to-normal volatility regimes, excluding panic/stress and excluding recent volatility spike transitions. |
| Expected horizon | h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Low |
| Why it differs from current inventory | It avoids post-stress volatility compression and studies low-volatility persistence when stress is absent. |
| Why it differs from reversal/momentum | It is volatility-quality and stability based, not directionally price-rank based. |
| Why it improves ecosystem diversification | Gives future construction a lower-turnover calm-state candidate with low expected co-activation against stress candidates. |
| Likely failure mode | Could be a low-beta or defensive-quality proxy with weak standalone alpha. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

### 5. `post_normalization_continuation_resolved_stress`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-normalization continuation after stress has resolved |
| Inventory gap addressed | Separates post-stress resolved-normalization behavior from active stress repair; adds h10-h15 optionality. |
| Economic intuition | After stress has already normalized, some names may continue through quality stabilization rather than through panic reversal or volatility compression. |
| State/activation thesis | Activate only after stress and volatility-spike flags have turned off for a short confirmation period, with stable range and moderate participation. |
| Expected horizon | h10-h15 |
| Expected active coverage | Medium |
| Expected turnover profile | Low to medium |
| Why it differs from current inventory | Existing stress candidate activates around stabilization after stress; this concept waits until stress is resolved and tests continuation of normalized quality. |
| Why it differs from reversal/momentum | It should not chase raw price continuation; continuation must be conditional on resolved state quality and low overextension. |
| Why it improves ecosystem diversification | Bridges stress and calm states without adding another active-stress mechanism. |
| Likely failure mode | Could become late-cycle momentum or duplicate volatility normalization if the resolved-state condition is weak. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

### 6. `non_hostile_participation_quality_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Non-hostile participation quality |
| Inventory gap addressed | Uses participation information outside hostile or weak-breadth repair states. |
| Economic intuition | Participation quality may matter in constructive or neutral markets when improving breadth is not a repair event but a confirmation of broad support. |
| State/activation thesis | Activate when trend is not hostile, breadth is not weak, and participation quality improves without broad euphoria or price extension. |
| Expected horizon | h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Medium |
| Why it differs from current inventory | It is explicitly non-hostile and avoids weak-breadth repair activation. |
| Why it differs from reversal/momentum | The mechanism is participation quality confirmation, not price-rank leadership or mean reversion. |
| Why it improves ecosystem diversification | Tests whether the participation family can provide a calmer-state complement rather than another co-active repair signal. |
| Likely failure mode | Hidden overlap with current participation/breadth candidates or raw breadth beta. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | `IMPLEMENT_NEXT` |

### 7. `low_dispersion_leadership_quality_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Low-dispersion leadership quality |
| Inventory gap addressed | Adds low-dispersion, non-stress leadership quality while avoiding the rejected stress-dispersion recovery shape. |
| Economic intuition | In low-dispersion regimes, leadership quality may be about stable contribution and low churn rather than aggressive price rank. |
| State/activation thesis | Activate in low-to-normal dispersion regimes with stable leadership participation, excluding high-dispersion recovery and panic states. |
| Expected horizon | h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Medium |
| Why it differs from current inventory | It is calm/low-dispersion leadership, not hostile repair or post-stress dispersion recovery. |
| Why it differs from reversal/momentum | Leadership must be quality-weighted and low-churn, not raw winner chasing. |
| Why it improves ecosystem diversification | Provides a possible calm leadership sleeve and avoids the rejected Expansion v2 dispersion-recovery formulation. |
| Likely failure mode | Hidden momentum exposure if leadership is defined too close to price rank. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

### 8. `volatility_normalization_without_panic_trigger`

| Field | Assessment |
| --- | --- |
| Mechanism family | Volatility normalization without panic/stress trigger |
| Inventory gap addressed | Adds normal volatility transition behavior that does not require panic or recent stress. |
| Economic intuition | Volatility can normalize from routine noise without a panic trigger; orderly normalization may support short-to-medium cross-sectional differentiation. |
| State/activation thesis | Activate when realized volatility declines from moderately elevated to normal levels, while panic, drawdown acceleration, and volatility-spike states are inactive. |
| Expected horizon | h5-h10 |
| Expected active coverage | Medium-high |
| Expected turnover profile | Low to medium |
| Why it differs from current inventory | It is not post-panic stabilization and should be less co-active with the volatility/stress candidate. |
| Why it differs from reversal/momentum | The thesis is volatility-state quality, not return direction. |
| Why it improves ecosystem diversification | Tests whether the volatility family can contribute outside hostile/stress windows. |
| Likely failure mode | Redundant with the existing volatility-compression candidate if panic exclusions are not strict. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

### 9. `cross_sectional_stability_outside_hostile_states`

| Field | Assessment |
| --- | --- |
| Mechanism family | Cross-sectional stability outside hostile states |
| Inventory gap addressed | Adds neutral-state cross-sectional stability with h10-h15 horizon. |
| Economic intuition | Stable cross-sectional rank relationships outside hostile states may indicate persistent stock-specific information without relying on repair after market damage. |
| State/activation thesis | Activate in neutral/non-hostile states when rank churn is low, dispersion is normal, and price extension is contained. |
| Expected horizon | h10-h15 |
| Expected active coverage | Medium |
| Expected turnover profile | Low |
| Why it differs from current inventory | It is explicitly outside hostile/stress states and focuses on cross-sectional order. |
| Why it differs from reversal/momentum | It should use rank stability and churn, not high or low price rank. |
| Why it improves ecosystem diversification | Adds a low-turnover neutral-state building block for future construction optionality. |
| Likely failure mode | Too generic and low signal-to-noise if stability alone lacks economic bite. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

### 10. `medium_horizon_fundamental_proxy_stability`

| Field | Assessment |
| --- | --- |
| Mechanism family | Medium-horizon/non-h20 stability proxy |
| Inventory gap addressed | Directly targets h20 concentration through h15-h30 monitoring. |
| Economic intuition | Medium-horizon stability in non-price proxies, such as liquidity consistency or volatility-adjusted quality persistence, may carry slower information than the current h20 repair candidates. |
| State/activation thesis | Activate across neutral and calm regimes with stable proxy behavior; hostile/stress states are diagnostic exclusions rather than activation drivers. |
| Expected horizon | h15-h30 |
| Expected active coverage | Medium-high |
| Expected turnover profile | Low |
| Why it differs from current inventory | It is slower, calmer, and not repair-state dependent. |
| Why it differs from reversal/momentum | It should be constructed around non-price proxy stability rather than return rank. |
| Why it improves ecosystem diversification | Gives the inventory a possible longer medium-horizon complement instead of another h20-only mechanism. |
| Likely failure mode | Weak alpha if the proxy is too broad or collapses into generic defensive quality. |
| Implementation complexity | Medium-high |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

### 11. `range_compression_quality_in_calm_regime`

| Field | Assessment |
| --- | --- |
| Mechanism family | Calm range quality |
| Inventory gap addressed | Adds calm low-vol/range behavior at h5-h10. |
| Economic intuition | Range compression in calm regimes can indicate orderly price discovery, but it must avoid becoming another breakout setup or volatility-compression clone. |
| State/activation thesis | Activate in calm regimes with contained ranges, stable closes, and no recent panic/stress precondition. |
| Expected horizon | h5-h10 |
| Expected active coverage | Medium |
| Expected turnover profile | Medium |
| Why it differs from current inventory | It excludes post-stress volatility compression and does not require hostile market states. |
| Why it differs from reversal/momentum | It is range-quality based, not price-direction based. |
| Why it improves ecosystem diversification | Potentially adds a shorter-horizon calm-state behavior, but overlap with volatility compression must be watched. |
| Likely failure mode | Becomes a range-breakout continuation concept, which prior research has warned against. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 3/5 |
| Priority | LOW |
| Recommendation | `HOLD_FOR_LATER` |

### 12. `redesigned_event_quality_low_turnover`

| Field | Assessment |
| --- | --- |
| Mechanism family | Event-quality, redesigned |
| Inventory gap addressed | Event-quality remains underrepresented, but v2 exposed high turnover, high missingness, weak h20 behavior, and raw-gap similarity risk. |
| Economic intuition | A redesigned event concept could require lower-turnover settlement and cleaner post-event quality, but this should not be the first v3 implementation path. |
| State/activation thesis | Event shock followed by longer settlement, lower turnover, and explicit raw-gap baseline separation. |
| Expected horizon | h5-h10 |
| Expected active coverage | Sparse to medium |
| Expected turnover profile | Medium after redesign; high if redesign fails. |
| Why it differs from current inventory | Event-time mechanism rather than state-repair mechanism. |
| Why it differs from reversal/momentum | Must separate materially from raw gap continuation/reversal before any implementation. |
| Why it improves ecosystem diversification | In principle it adds event-time diversity, but v2 evidence says the family needs more design discipline first. |
| Likely failure mode | Repeats v2 failure: high turnover, high missingness, weak IC, and raw-gap similarity. |
| Implementation complexity | Medium-high |
| Inventory-complementarity score | 2/5 |
| Priority | LOW |
| Recommendation | `DISCARD_CONCEPT` |

## Diversification Scorecard

| concept | horizon diversification | state diversification | co-activation diversification | mechanism diversification | construction optionality |
| --- | --- | --- | --- | --- | --- |
| `neutral_accumulation_without_breakout` | 5 | 5 | 5 | 5 | 5 |
| `calm_regime_relative_stability_10` | 4 | 5 | 5 | 4 | 5 |
| `quiet_liquidity_accumulation_non_hostile` | 5 | 5 | 4 | 4 | 5 |
| `low_volatility_quality_persistence_10` | 4 | 5 | 5 | 4 | 4 |
| `post_normalization_continuation_resolved_stress` | 4 | 4 | 4 | 4 | 4 |
| `non_hostile_participation_quality_10` | 4 | 4 | 3 | 3 | 4 |
| `low_dispersion_leadership_quality_10` | 4 | 4 | 4 | 4 | 4 |
| `volatility_normalization_without_panic_trigger` | 5 | 4 | 4 | 3 | 4 |
| `cross_sectional_stability_outside_hostile_states` | 4 | 5 | 5 | 4 | 4 |
| `medium_horizon_fundamental_proxy_stability` | 5 | 4 | 5 | 3 | 4 |
| `range_compression_quality_in_calm_regime` | 5 | 4 | 4 | 3 | 3 |
| `redesigned_event_quality_low_turnover` | 5 | 4 | 5 | 4 | 2 |

Scores are design-screening judgments from 1 to 5. They are not validation results.

## Promising Expansion v3 Concepts

The 5-8 most promising concepts are:

1. `neutral_accumulation_without_breakout`
2. `calm_regime_relative_stability_10`
3. `quiet_liquidity_accumulation_non_hostile`
4. `low_volatility_quality_persistence_10`
5. `post_normalization_continuation_resolved_stress`
6. `non_hostile_participation_quality_10`
7. `low_dispersion_leadership_quality_10`
8. `cross_sectional_stability_outside_hostile_states`

Top 2-3 concepts to implement one-by-one later:

1. `neutral_accumulation_without_breakout`
2. `calm_regime_relative_stability_10`
3. `quiet_liquidity_accumulation_non_hostile`

These three best match the v3 objective: calmer-state activation, shorter horizon, medium coverage, low expected co-activation, and useful future construction optionality.

## Direct Gap Coverage

Concepts that directly address h20 concentration:

- `neutral_accumulation_without_breakout`
- `quiet_liquidity_accumulation_non_hostile`
- `volatility_normalization_without_panic_trigger`
- `range_compression_quality_in_calm_regime`
- `calm_regime_relative_stability_10`
- `low_volatility_quality_persistence_10`
- `medium_horizon_fundamental_proxy_stability`

Concepts that directly address hostile/stress-state dependence:

- `neutral_accumulation_without_breakout`
- `calm_regime_relative_stability_10`
- `quiet_liquidity_accumulation_non_hostile`
- `low_volatility_quality_persistence_10`
- `non_hostile_participation_quality_10`
- `low_dispersion_leadership_quality_10`
- `volatility_normalization_without_panic_trigger`
- `cross_sectional_stability_outside_hostile_states`

Concepts most likely to reduce participation/breadth co-activation:

- `neutral_accumulation_without_breakout`
- `calm_regime_relative_stability_10`
- `low_volatility_quality_persistence_10`
- `cross_sectional_stability_outside_hostile_states`
- `medium_horizon_fundamental_proxy_stability`

## Implementation Recommendation

Implementation should remain one-by-one, not a batch. The inventory has two `WATCH_MONITOR` candidates, unresolved rebuild/equivalence work, and a known co-activation concentration. A small focused batch would add avoidable ambiguity about which concept actually diversifies the ecosystem.

Recommended later sequence:

1. Implement `neutral_accumulation_without_breakout` as the first v3 test.
2. If it fails as a price-rank or breakout proxy, implement `calm_regime_relative_stability_10` next.
3. If a liquidity-family concept is still desired, implement `quiet_liquidity_accumulation_non_hostile` with strict non-hostile and no-price-extension controls.

## Required Monitoring Before Implementation

Before any v3 concept is implemented, the next research note should acknowledge:

- Current `WATCH_MONITOR` status for `participation_liquidity_state_shift_20_60` and `volatility_compression_after_stress_stabilization`.
- Co-activation concentration between participation/liquidity and breadth repair.
- h20 concentration across all current inventory candidates.
- Shared hostile/stress-state dependence across all current inventory candidates.
- Recent-window fragility and one-window dominance risk.
- Need for active-window drift and co-activation drift monitoring in the next inventory refresh.
- Need for rebuild/equivalence checks before construction-layer design.

Every implemented v3 candidate should later be checked against:

- all three current inventory primary panels
- reversal and momentum baselines
- price-rank continuation baselines
- co-activation against current inventory states
- active-window support and coverage
- turnover drift
- recent-window behavior
- one-window dominance

## Final Recommendation

Adopt this design-screening package as the Track B Expansion v3 roadmap. The next implementation should be one-by-one and should start with `neutral_accumulation_without_breakout`, followed by `calm_regime_relative_stability_10` or `quiet_liquidity_accumulation_non_hostile` depending on whether the first test fails through price-rank duplication, weak calm-state behavior, or turnover.

Do not run broad discovery. Do not add more hostile/stress h20 repair variants. Do not begin construction-layer, portfolio, ML, blending, weighting, optimization, or production work from this package.
