# Track B Expansion v4 Design Screening

## Executive Takeaway

Track B Expansion v4 should move Project Underdog from "repair during hostile states" toward "what happens after repair completes." Expansion v3 showed that passive calmer-state diversification is not enough: neutral accumulation and quiet non-hostile liquidity were structurally orthogonal but not predictive, while calm relative stability remains promising but unresolved and still h20-dominant.

Expansion v4 should therefore focus on post-repair, resolved-stress, and post-normalization mechanisms. The goal is not to fight the current inventory identity. It is to extend that identity into the next state of the market cycle: after weak breadth improves, after panic exits, after volatility normalizes, after hostile trend pressure relaxes, and after dislocation repair stops being the active driver.

Recommended first one-by-one sequence:

1. `post_repair_continuation_after_breadth_recovery`
2. `resolved_stress_relative_stability_15`
3. `hostile_to_neutral_transition_quality`

Secondary high-value concept:

- `liquidity_normalization_after_panic_exit`

No candidates were implemented. No discovery, validation/refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production logic change was performed.

## Sources Reviewed

- `docs/research_notes/track_b_expansion_v3_midcycle_review.md`
- `docs/research_notes/inventory_ecosystem_review_v1.md`
- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- Current inventory notes for:
  - `participation_liquidity_state_shift_20_60`
  - `participation_breadth_repair_under_hostile_trend`
  - `volatility_compression_after_stress_stabilization`

## Current Inventory And v3 Lessons

Current Conditional Alpha Inventory:

1. `participation_liquidity_state_shift_20_60`
2. `participation_breadth_repair_under_hostile_trend`
3. `volatility_compression_after_stress_stabilization`

Current inventory identity:

- h20-centered.
- strongest in hostile, weak-breadth, drawdown, panic/liquidity, stress, and post-stress stabilization states.
- useful but concentrated around repair and stabilization.
- low pairwise correlations, but material co-activation between participation/liquidity and breadth repair.
- two candidates remain `WATCH_MONITOR`, so expansion must remain governed and one-by-one.

Expansion v3 taught:

- Calm accumulation failed: `neutral_accumulation_without_breakout` was orthogonal but not predictive.
- Quiet non-hostile liquidity failed: `quiet_liquidity_accumulation_non_hostile` avoided duplication but had negative h5/h10 behavior and negative quiet-state attribution.
- Calm relative stability remains unresolved: `calm_regime_relative_stability_10` had positive h10 and stronger h20 behavior, but stayed sparse, h20-dominant, and not validation-ready.
- Repair/stabilization remains the strongest research identity.

Expansion v4 implication: do not force generic calm-state concepts. Instead, test whether repair creates a follow-through state that is distinct from active repair.

## Design Principles

Expansion v4 concepts should:

- activate after repair or stress has resolved, not during the primary hostile/stress trigger;
- define explicit repair-completion or stress-exit conditions;
- avoid raw continuation, price-rank momentum, simple reversal, and simple low-volatility beta;
- compare against all three current inventory candidates for similarity and co-activation;
- target h10-h15 where plausible, while preserving h20 as an inventory diagnostic;
- prefer medium coverage over tiny event slices;
- improve future construction optionality by creating a state after active repair rather than another active repair clone.

Concepts should be rejected at design level if they are just hostile repair with a delayed label, low-vol beta, raw winner continuation, broad nonlinear state scoring, or over-fragmented state slicing.

## Concept Screen

| concept | family | gap addressed | horizon | active coverage | turnover | complementarity | priority | recommendation |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| `post_repair_continuation_after_breadth_recovery` | resolved breadth repair persistence | after weak-breadth repair without active hostile clone | h10-h15 | medium | low-medium | 5 | HIGH | `IMPLEMENT_NEXT` |
| `resolved_stress_relative_stability_15` | post-dislocation relative stability | stability after stress exits and lower overlap with active repair | h10-h15 | medium | low | 5 | HIGH | `IMPLEMENT_NEXT` |
| `liquidity_normalization_after_panic_exit` | post-panic liquidity normalization | liquidity normalization after panic rather than hostile liquidity repair | h10-h15 | medium | medium | 4 | HIGH | `IMPLEMENT_NEXT` |
| `volatility_stabilization_durability_10` | post-normalization volatility durability | tests stabilization durability after stress candidate's active window | h10 | medium | low | 4 | HIGH | `HOLD_FOR_LATER` |
| `low_vol_quality_after_repair_10` | low-volatility quality after repair | calm quality only after repair completion, not passive low-vol beta | h10 | medium | low | 4 | HIGH | `HOLD_FOR_LATER` |
| `hostile_to_neutral_transition_quality` | hostile-to-neutral transition quality | state transition from hostile to neutral without active repair clone | h10-h15 | medium | medium | 5 | HIGH | `IMPLEMENT_NEXT` |
| `repair_completion_breadth_confirmation_10` | repair-completion confirmation | confirmation after breadth repair rather than weak-breadth repair itself | h10 | medium | medium | 3 | MEDIUM | `HOLD_FOR_LATER` |
| `post_dislocation_range_quality_10` | post-dislocation range quality | range order after dislocation without reversal or raw continuation | h10 | medium | medium | 4 | MEDIUM | `HOLD_FOR_LATER` |
| `resolved_volatility_compression_without_panic` | non-panic resolved volatility normalization | normalization after stress flags clear while avoiding current volatility candidate clone | h10-h15 | medium-high | low-medium | 3 | MEDIUM | `HOLD_FOR_LATER` |
| `stabilized_participation_quality_after_repair` | stabilized participation quality | participation quality after repair completion, not hostile participation repair | h10 | medium | medium | 3 | MEDIUM | `HOLD_FOR_LATER` |
| `post_repair_low_dispersion_leadership_quality` | post-repair low-dispersion leadership | leadership quality after repair with momentum controls | h10 | medium | medium | 3 | LOW | `HOLD_FOR_LATER` |
| `resolved_event_quality_after_gap_settlement` | event quality after resolved dislocation | revisits event family only after settlement and normalization | h10-h15 | sparse-medium | medium | 2 | LOW | `DISCARD_CONCEPT` |

## Concept Details

### 1. `post_repair_continuation_after_breadth_recovery`

| Field | Assessment |
| --- | --- |
| Mechanism family | Resolved breadth repair persistence |
| Inventory gap addressed | Tests whether breadth repair has follow-through after weak breadth improves, rather than adding another weak-breadth repair clone. |
| Economic intuition | After a hostile/weak-breadth repair phase succeeds, stocks that participated cleanly in the repair may continue as forced selling fades and cross-sectional quality becomes easier to distinguish. |
| Post-repair / resolved-stress thesis | Activate only after weak breadth and hostile repair conditions have recently been present and then cleared for a short confirmation period. |
| Expected activation semantics | Recent weak-breadth repair completed; current breadth is no longer weak; benchmark trend no longer deteriorating; no active panic/liquidity stress. |
| Expected horizon | h10-h15, h20 diagnostic. |
| Expected active coverage | Medium. |
| Expected turnover profile | Low-medium with rebalance control. |
| Why it differs from current inventory | Current breadth candidate activates during weak-breadth/hostile repair; this activates after that condition resolves. |
| Why it differs from raw continuation/reversal/momentum | Requires repair-completion state and participation/breadth normalization; should neutralize price-rank continuation and reversal baselines. |
| How it improves ecosystem diversification | Adds a post-repair state that may co-activate less with the current participation/breadth pair while still respecting the durable repair identity. |
| Likely failure mode | Could become delayed momentum or simply the same breadth-repair candidate shifted forward. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 4 |
| Future construction optionality | 5 |

### 2. `resolved_stress_relative_stability_15`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-dislocation relative stability |
| Inventory gap addressed | Extends the only promising v3 calm-state idea into a resolved-stress setting instead of passive calm accumulation. |
| Economic intuition | After stress exits, names with stable relative ranks and orderly residual behavior may be better positioned because the dislocation has cleared but uncertainty has not fully normalized. |
| Post-repair / resolved-stress thesis | Activate after volatility spike, drawdown acceleration, or panic/liquidity stress has cleared, then select names with relative stability rather than raw rebound. |
| Expected activation semantics | Stress recently present; stress flags inactive now; dispersion and breadth no longer deteriorating; relative rank churn is low. |
| Expected horizon | h10-h15, with h20 monitored. |
| Expected active coverage | Medium. |
| Expected turnover profile | Low. |
| Why it differs from current inventory | Current volatility candidate focuses on stabilization after stress; this focuses on cross-sectional relative stability after stress has resolved. |
| Why it differs from raw continuation/reversal/momentum | Selection is based on rank stability, residual orderliness, and neutralized return ranks rather than rebound magnitude. |
| How it improves ecosystem diversification | Bridges v3 relative-stability evidence with the inventory's stress-transition identity. |
| Likely failure mode | Could duplicate `volatility_compression_after_stress_stabilization` or remain h20-dominant. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 5 |
| Horizon diversification | 4 |
| Co-activation diversification | 5 |
| Mechanism diversification | 5 |
| Future construction optionality | 5 |

### 3. `liquidity_normalization_after_panic_exit`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-panic liquidity normalization |
| Inventory gap addressed | Tests liquidity normalization after panic exits, avoiding both quiet-liquidity failure and active hostile liquidity repair. |
| Economic intuition | Panic can distort liquidity. Once panic exits, names whose liquidity normalizes without price chase may have more durable follow-through than names still in repair mode. |
| Post-repair / resolved-stress thesis | Activate after panic/liquidity stress has recently been present and is now inactive, with dollar-volume and range impact normalizing. |
| Expected activation semantics | Panic/liquidity stress cleared; dollar-volume no longer shocked; spread/range proxy contained; no breakout pressure. |
| Expected horizon | h10-h15. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | Existing liquidity candidate is hostile trend/repair oriented; this requires panic exit and normalization after stress. |
| Why it differs from raw continuation/reversal/momentum | Liquidity normalization and impact containment are primary; price-rank extension should be neutralized or vetoed. |
| How it improves ecosystem diversification | Keeps liquidity as a useful project identity while shifting activation to the post-panic state. |
| Likely failure mode | May collapse into the existing participation/liquidity candidate or fail like quiet non-hostile liquidity if panic-exit semantics are weak. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 3 |
| Mechanism diversification | 4 |
| Future construction optionality | 4 |

### 4. `volatility_stabilization_durability_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-normalization volatility durability |
| Inventory gap addressed | Tests whether volatility stabilization persists after the current volatility/stress candidate's active repair window. |
| Economic intuition | Some volatility compression events may be transient, while durable stabilization after stress can support cleaner cross-sectional differentiation. |
| Post-repair / resolved-stress thesis | Require prior stress/volatility compression, then wait for volatility/range conditions to remain stable after the initial stabilization window. |
| Expected activation semantics | Stress recently resolved; volatility normal for multiple observations; range no longer expanding; breadth not weak. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Low. |
| Why it differs from current inventory | It is a durability check after stabilization, not the stabilization event itself. |
| Why it differs from raw continuation/reversal/momentum | Uses volatility durability and range stability, not price rebound direction. |
| How it improves ecosystem diversification | Could provide a lower-turnover post-stress sleeve, but must be monitored for duplication with the volatility candidate. |
| Likely failure mode | High duplication risk with `volatility_compression_after_stress_stabilization`. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 3 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 3 |
| Future construction optionality | 4 |

### 5. `low_vol_quality_after_repair_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Low-volatility quality after repair |
| Inventory gap addressed | Reuses v3's relative-stability clue without becoming passive low-vol beta. |
| Economic intuition | Low volatility may matter only after repair has removed forced-selling pressure; stable names after repair could reflect quality rather than defensiveness. |
| Post-repair / resolved-stress thesis | Activate after hostile/weak-breadth or stress conditions clear, then select low residual volatility plus quality/stability confirmation. |
| Expected activation semantics | Repair recently completed; low-to-normal volatility; stable residual ranks; no momentum extension. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Low. |
| Why it differs from current inventory | Current inventory is active repair/stabilization; this tests quality persistence after repair. |
| Why it differs from raw continuation/reversal/momentum | Requires volatility quality and stability; explicitly controls for return ranks and low-vol beta similarity. |
| How it improves ecosystem diversification | Could add a calmer post-repair quality sleeve with lower co-activation. |
| Likely failure mode | May become simple low-volatility beta or duplicate `calm_regime_relative_stability_10`. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | HIGH |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 5 |
| Mechanism diversification | 4 |
| Future construction optionality | 4 |

### 6. `hostile_to_neutral_transition_quality`

| Field | Assessment |
| --- | --- |
| Mechanism family | Hostile-to-neutral transition quality |
| Inventory gap addressed | Targets state transition quality rather than hostile-state repair itself. |
| Economic intuition | The transition from hostile to neutral can reveal which names remain orderly after the market stops deteriorating. |
| Post-repair / resolved-stress thesis | Activate when hostile trend state recently existed but current trend, breadth, and stress flags no longer confirm hostility. |
| Expected activation semantics | Hostile state exited; breadth improved; drawdown pressure reduced; candidate names show stable path and relative support. |
| Expected horizon | h10-h15. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | Current participation and breadth candidates fire during hostile/weak-breadth repair; this fires after the hostile state exits. |
| Why it differs from raw continuation/reversal/momentum | The signal is transition quality conditioned on state exit, with controls against rebound chasing and loser inversion. |
| How it improves ecosystem diversification | Creates a distinct bridge state useful for future construction sequencing. |
| Likely failure mode | State exit may be too noisy or may simply lag the current repair candidates. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 5/5 |
| Priority | HIGH |
| Recommendation | `IMPLEMENT_NEXT` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 5 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 5 |
| Future construction optionality | 5 |

### 7. `repair_completion_breadth_confirmation_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Repair-completion confirmation |
| Inventory gap addressed | Tests whether breadth repair completion has predictive value separate from breadth repair activation. |
| Economic intuition | Once breadth repair is confirmed, market participation may become more stable; names aligned with that transition may benefit. |
| Post-repair / resolved-stress thesis | Activate after weak breadth improves and remains above a confirmation threshold without euphoria. |
| Expected activation semantics | Weak breadth recently present; breadth no longer weak; participation balanced; no stress spike. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | It should not fire during weak breadth; it requires breadth repair completion. |
| Why it differs from raw continuation/reversal/momentum | Breadth confirmation and stability are primary; return ranks are controls. |
| How it improves ecosystem diversification | Adds a possible construction signal for transition from repair to normalized participation. |
| Likely failure mode | Could be too close to breadth repair or become a broad market beta proxy. |
| Implementation complexity | Low-medium |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 3 |
| Horizon diversification | 4 |
| Co-activation diversification | 3 |
| Mechanism diversification | 3 |
| Future construction optionality | 4 |

### 8. `post_dislocation_range_quality_10`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-dislocation range quality |
| Inventory gap addressed | Adds range/path quality after dislocation without relying on volatility-compression alone. |
| Economic intuition | After a dislocation, cleaner range behavior may indicate lower residual uncertainty and better follow-through quality. |
| Post-repair / resolved-stress thesis | Activate after stress or high dispersion clears, then select contained range, stable closes, and low path noise. |
| Expected activation semantics | Dislocation recently present; range expansion cooled; no active panic; price extension controlled. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | Current volatility candidate is stress-stabilization; this is post-dislocation range quality with stricter no-continuation controls. |
| Why it differs from raw continuation/reversal/momentum | It should not reward rebound size, only range quality after dislocation. |
| How it improves ecosystem diversification | Adds a path-quality lens that may complement volatility and participation repair. |
| Likely failure mode | Could duplicate volatility compression or become another range-compression control. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 4/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 4 |
| Future construction optionality | 4 |

### 9. `resolved_volatility_compression_without_panic`

| Field | Assessment |
| --- | --- |
| Mechanism family | Non-panic resolved volatility normalization |
| Inventory gap addressed | Tests lower-drama volatility normalization after stress flags clear, but not generic passive calm. |
| Economic intuition | Some names may normalize volatility after routine dislocation without requiring a panic trigger; that may create more frequent medium-coverage signals. |
| Post-repair / resolved-stress thesis | Activate only after elevated volatility or dispersion normalizes and panic/liquidity stress is inactive. |
| Expected activation semantics | Resolved volatility; no panic; breadth not weak; range no longer expanding. |
| Expected horizon | h10-h15. |
| Expected active coverage | Medium-high. |
| Expected turnover profile | Low-medium. |
| Why it differs from current inventory | It avoids requiring panic/stress trigger, but still requires a resolved normalization transition. |
| Why it differs from raw continuation/reversal/momentum | Volatility normalization is primary; return ranks should be neutralized. |
| How it improves ecosystem diversification | Could improve coverage and add non-panic normalization states. |
| Likely failure mode | May become simple low-volatility beta or duplicate the volatility/stress candidate. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 3 |
| Horizon diversification | 4 |
| Co-activation diversification | 3 |
| Mechanism diversification | 3 |
| Future construction optionality | 4 |

### 10. `stabilized_participation_quality_after_repair`

| Field | Assessment |
| --- | --- |
| Mechanism family | Stabilized participation quality |
| Inventory gap addressed | Keeps participation semantics but moves from active repair to post-repair stabilization. |
| Economic intuition | After repair completes, sustainable participation may matter more than the initial participation rebound. |
| Post-repair / resolved-stress thesis | Activate after hostile/weak-breadth repair exits, requiring participation quality to remain stable without volume shock. |
| Expected activation semantics | Recent repair state; current non-hostile state; stable participation and contained range. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | It is post-repair participation stability, not hostile participation repair. |
| Why it differs from raw continuation/reversal/momentum | Participation stability and state exit are primary; price ranks are controls. |
| How it improves ecosystem diversification | Could become a bridge from participation repair into normalized participation states. |
| Likely failure mode | High semantic overlap with `participation_liquidity_state_shift_20_60`. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 3/5 |
| Priority | MEDIUM |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 3 |
| Horizon diversification | 4 |
| Co-activation diversification | 2 |
| Mechanism diversification | 3 |
| Future construction optionality | 4 |

### 11. `post_repair_low_dispersion_leadership_quality`

| Field | Assessment |
| --- | --- |
| Mechanism family | Post-repair low-dispersion leadership |
| Inventory gap addressed | Tests leadership quality after repair in low-dispersion conditions, avoiding rejected dispersion-recovery framing. |
| Economic intuition | After repair, leadership in low dispersion may reflect quality stability rather than panic rebound. |
| Post-repair / resolved-stress thesis | Activate after repair exits and dispersion normalizes, then select leadership quality with anti-momentum controls. |
| Expected activation semantics | Low-to-normal dispersion after repair; leadership is stable, not extended. |
| Expected horizon | h10. |
| Expected active coverage | Medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | It is post-repair leadership quality, not active weak-breadth or stress repair. |
| Why it differs from raw continuation/reversal/momentum | Leadership must be stable, low-churn, and neutralized against price-rank momentum. |
| How it improves ecosystem diversification | Could add a post-repair leadership sleeve if momentum leakage is controlled. |
| Likely failure mode | High risk of hidden momentum exposure. |
| Implementation complexity | Medium |
| Inventory-complementarity score | 3/5 |
| Priority | LOW |
| Recommendation | `HOLD_FOR_LATER` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 4 |
| Future construction optionality | 4 |

### 12. `resolved_event_quality_after_gap_settlement`

| Field | Assessment |
| --- | --- |
| Mechanism family | Event quality after resolved dislocation |
| Inventory gap addressed | Revisits event-quality only after settlement and normalization, not as raw gap continuation. |
| Economic intuition | Some event dislocations may become informative only after the first noisy gap/reversal window clears. |
| Post-repair / resolved-stress thesis | Activate after gap/event dislocation settles, range normalizes, and volume shock fades. |
| Expected activation semantics | Event shock complete; no fresh gap; range and volume normalized; no panic. |
| Expected horizon | h10-h15. |
| Expected active coverage | Sparse-medium. |
| Expected turnover profile | Medium. |
| Why it differs from current inventory | Event-settlement family is outside current participation/breadth/volatility inventory. |
| Why it differs from raw continuation/reversal/momentum | It waits for settlement and controls gap/reversal similarity. |
| How it improves ecosystem diversification | Mechanism-diverse if it works, but prior event evidence was weak and noisy. |
| Likely failure mode | Sparse, noisy, high missingness, and gap/reversal similarity. |
| Implementation complexity | High |
| Inventory-complementarity score | 2/5 |
| Priority | LOW |
| Recommendation | `DISCARD_CONCEPT` |

Scores:

| dimension | score |
| --- | ---: |
| State diversification | 4 |
| Horizon diversification | 4 |
| Co-activation diversification | 4 |
| Mechanism diversification | 4 |
| Future construction optionality | 3 |

## Recommended One-By-One Sequence

Expansion v4 should remain one-by-one. Do not implement concepts as a batch.

Recommended first three:

1. `post_repair_continuation_after_breadth_recovery`
2. `resolved_stress_relative_stability_15`
3. `hostile_to_neutral_transition_quality`

Optional fourth if the first three do not provide enough liquidity/post-panic evidence:

4. `liquidity_normalization_after_panic_exit`

Rationale:

- The first concept directly tests what happens after the cleanest current inventory member completes repair.
- The second concept connects the only live v3 calm-state idea to resolved-stress semantics.
- The third concept directly targets the transition from the current inventory's hostile state to neutral state.
- The fourth keeps liquidity in the research map but avoids repeating failed quiet non-hostile liquidity.

## Required Diagnostics For Future Implementation

Any later one-by-one implementation should check:

- h5/h10/h15/h20 IC and positive IC rate;
- whether h10-h15 improves versus current h20 concentration;
- WFV-style persistence and sign consistency;
- active coverage and active-window adequacy;
- one-window dominance;
- turnover and rank-churn behavior;
- similarity to current inventory candidates;
- co-activation against participation/liquidity and breadth repair;
- similarity to reversal, momentum, raw continuation, low-volatility, and volatility-stabilization baselines;
- state attribution for active repair, resolved repair, and neutral/post-repair windows;
- whether the candidate is secretly active repair, delayed momentum, simple reversal, or low-volatility beta.

## Governance And Readiness

Before implementing any Expansion v4 concept:

- Acknowledge that two current inventory members remain `WATCH_MONITOR`.
- Do not treat Expansion v4 as construction-layer readiness.
- Keep candidate outputs isolated under `artifacts/research/<candidate>_v1/`.
- Preserve run_id/version traceability and manifest artifacts.
- Compare against all three current inventory candidates.
- Do not modify production registration, survivor/watchlist files, gates, schemas, thresholds, or construction logic.

Expansion v4 is justified only as design-level preparation and later one-by-one research. It is not a reason to promote the inventory or add portfolio logic.

## Final Recommendation

Expansion v4 should proceed as a design-only roadmap focused on post-repair and resolved-stress mechanisms. The current research prior is not "calm states do not work"; it is more specific: passive calm accumulation did not work, while repair and stabilization have been the durable identity.

The next useful question is:

What persists after repair succeeds?

That question is narrow enough to respect the current evidence and broad enough to improve the inventory's future state coverage, horizon optionality, co-activation profile, and construction-layer semantics.
