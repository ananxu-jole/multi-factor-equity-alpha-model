# Track B Expansion v5 Mini-Closeout Review

Date: 2026-05-21

Status: RESEARCH_CLOSEOUT_REVIEW

## Executive Takeaway

Expansion v5 was designed to preserve Project Underdog's active repair/stabilization identity while reducing inventory concentration in h20, hostile/stress activation, and participation/breadth co-activation.

The cycle did not find a validation-ready strict h10 repair mechanism. It did, however, identify one live short-horizon thread: `short_horizon_volatility_shock_absorption_10`, which is h5-led, positive at h10, weak at h20, structurally differentiated, and capable of reducing the current inventory's h20 concentration risk.

Recommendation: pause immediate v5 refinement and redesign the next short-horizon research thread around `h5-to-h10 shock absorption` rather than forcing every repair/stabilization concept to be h10-primary. h10 should remain the validation target for promotion, but h5 should be accepted as a legitimate research target when the mechanism thesis is explicitly fast shock absorption and h10 carry-through remains positive.

No new candidate implementation, validation/refinement run, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.

## Sources Reviewed

- `docs/research_notes/track_b_expansion_v5_design_screening.md`
- `docs/research_notes/drawdown_pressure_stabilization_10_v1.md`
- `docs/research_notes/idiosyncratic_stress_containment_10_v1.md`
- `docs/research_notes/short_horizon_volatility_shock_absorption_10_v1.md`
- `docs/research_notes/short_horizon_volatility_shock_absorption_10_refinement.md`
- `docs/research_notes/conditional_alpha_inventory_monitoring_v2.md`
- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`

## Current Inventory Context

Monitoring v2 keeps the active Conditional Alpha Inventory in a research-usable but concentration-aware state:

| Candidate | Monitoring state | Main risk |
| --- | --- | --- |
| `participation_liquidity_state_shift_20_60` | `WATCH_MONITOR` | Recent rolling h20 IC much weaker than full-sample h20 IC. |
| `participation_breadth_repair_under_hostile_trend` | `HEALTHY_ACTIVE_RESEARCH` | Cleanest inventory anchor. |
| `volatility_compression_after_stress_stabilization` | `WATCH_MONITOR` | One-window dominance and recent positive-rate weakness. |

Inventory-level risks remain:

- Pairwise correlations are low, with max absolute correlation near `0.057859`.
- Co-activation remains concentrated between participation/liquidity and breadth repair, with max co-activation near `0.803333`.
- The inventory remains h20-centered.
- The inventory remains hostile/stress-state dependent.
- Expansion v4 reinforced that active repair/stabilization is stronger than post-repair calm persistence.

Expansion v5 therefore had the right design objective: keep the repair/stabilization identity, but diversify horizon, state semantics, and co-activation topology.

## Concept Results

### `drawdown_pressure_stabilization_10`

Mechanism thesis: downside-pressure containment during active drawdown-pressure regimes may identify stocks where repair begins before broad participation or breadth recovery dominates.

Result: `REJECT_RESEARCH`

Key metrics:

| Metric | Value |
| --- | ---: |
| h5 mean IC | `-0.006244` |
| h10 mean IC | `-0.010492` |
| h15 mean IC | `-0.010220` |
| h20 mean IC | `-0.010026` |
| WFV persistence / sign consistency | `0.00 / 1.00` |
| active date ratio | `0.100095` |
| max inventory corr | `0.109334` |

Structural differentiation was acceptable: it did not obviously collapse into reversal, momentum, breadth/participation repair, or current inventory duplication. The failure was empirical. IC was negative across every tested horizon, drawdown-state support was weak, and WFV persistence was absent.

Reason it did not advance: broad drawdown pressure appears to describe stress intensity more than repair quality. Inverting the signal would likely become a rebound/reversal proxy rather than a clean stabilization mechanism.

### `idiosyncratic_stress_containment_10`

Mechanism thesis: stock-specific residual stress containment may identify repair behavior that is less tied to broad market drawdown or breadth-repair gates.

Result: `CONDITIONAL_ONLY_RESEARCH`

Key metrics:

| Metric | Value |
| --- | ---: |
| h5 mean IC | `0.005390` |
| h10 mean IC | `0.005415` |
| h15 mean IC | `0.005298` |
| h20 mean IC | `0.009046` |
| WFV persistence / sign consistency | `0.75 / 0.75` |
| active date ratio | `0.729266` |
| max inventory corr | `0.094707` |
| max drawdown-pressure corr | `0.049517` |

Structural differentiation was also acceptable. It was cleaner than drawdown pressure and did not show obvious broad drawdown, reversal, momentum, or current-inventory duplication.

Reason it did not advance: the edge was h20-led rather than h10-led, and activation was too broad for a conditional repair candidate. The stock-level stress gate behaved more like a persistent broad residual-stress screen than a precise short-horizon containment event.

### `short_horizon_volatility_shock_absorption_10`

Mechanism thesis: after volatility or range shocks, stocks that absorb the shock without disorderly follow-through may stabilize over h5-to-h10 before slower h20 compression signals dominate.

V1 result: `CONDITIONAL_REFINEMENT_CANDIDATE`

V1 key metrics:

| Metric | Value |
| --- | ---: |
| h5 mean IC | `0.011045` |
| h10 mean IC | `0.008558` |
| h15 mean IC | `0.006034` |
| h20 mean IC | `0.003522` |
| WFV persistence / sign consistency | `0.75 / 0.75` |
| active date ratio | `0.190658` |
| max inventory corr | `0.117222` |
| max volatility/stress corr | `0.117222` |

Refinement result: `CONDITIONAL_REFINEMENT_CANDIDATE`

Best refinement variant: `rebalance_5_zero`

| Metric | Value |
| --- | ---: |
| h5 mean IC | `0.012639` |
| h10 mean IC | `0.010260` |
| h10 positive IC rate | `0.600515` |
| h15 mean IC | `0.005333` |
| h20 mean IC | `0.003243` |
| WFV persistence / sign consistency | `1.00 / 1.00` |
| active date ratio | `0.185891` |
| one-window dominance | `0.351775` |
| max inventory corr | `0.123023` |
| max volatility/stress corr | `0.123023` |

Structural differentiation remained controlled. Reversal and momentum similarity were very low, participation/breadth repair similarity remained low, and volatility/stress similarity rose only modestly. The signal did not become h20-dependent.

Reason it did not advance: h10 improved but remained below validation quality, and the best horizon stayed h5. The candidate is a promising short-horizon research candidate, not yet a conditional validation candidate.

## What Expansion v5 Found

### Strict h10 repair mechanism

Expansion v5 did not find a true strict h10 repair mechanism. The two concepts built explicitly around h10 either failed outright (`drawdown_pressure_stabilization_10`) or became h20-led (`idiosyncratic_stress_containment_10`).

The h10 evidence in `short_horizon_volatility_shock_absorption_10` is positive and improved under `rebalance_5_zero`, but h10 is still not the dominant or validation-quality horizon.

Assessment: not found.

### Short-horizon h5-to-h10 repair mechanism

Expansion v5 did find a credible h5-to-h10 shock absorption thread. `short_horizon_volatility_shock_absorption_10` has the only desirable horizon slope in the cycle:

- h5 strongest.
- h10 positive.
- h15 weaker.
- h20 weakest and still small.

This is exactly the opposite of the existing inventory's h20 concentration, which gives it real ecosystem value even without validation readiness.

Assessment: found as a research thread, not as a validation candidate.

### Weak or noisy short-horizon behavior

The refinement pass reduced the risk that the h5 result is pure noise. The best variant improved h5 to `0.012639`, improved h10 to `0.010260`, produced h10 positive rate of `0.600515`, and raised WFV persistence/sign consistency to `1.00 / 1.00`.

However, the behavior is still h5-led. That means it should be treated as a fast shock-absorption effect with h10 carry-through, not as a clean h10 repair signal.

Assessment: not merely noisy, but not validation-ready.

## Interpretation

### Why drawdown pressure failed

Drawdown pressure was too blunt. It captured broad downside environment and stress intensity, but the stabilization confirmation did not identify forward repair. The negative IC profile across h5, h10, h15, and h20 suggests the mechanism was not simply mistimed; it was directionally wrong in the tested formulation.

This should not be repeated by inversion. Inverting a failed drawdown-pressure score would likely reward rebound/reversal behavior and violate the goal of finding differentiated repair/stabilization mechanisms.

### Why idiosyncratic stress was too broad

Idiosyncratic stress containment was conceptually cleaner and empirically less bad, but activation covered too much of the sample. With an active date ratio of `0.729266`, it behaved less like a conditional shock event and more like a broad residual-stress regime screen.

Its best horizon was h20, which means it did not solve the v5 horizon problem. The result is useful as evidence that asset-level stress may contain information, but not in this broad h10 formulation.

### Why volatility shock absorption is the live thread

Volatility shock absorption is the only v5 concept that did all of the following:

- Produced positive IC across h5 and h10.
- Reduced h20 dependence.
- Preserved acceptable active coverage.
- Maintained low reversal and momentum similarity.
- Kept inventory and volatility/stress similarity controlled.
- Improved WFV persistence/sign consistency under a narrow refinement.

It is also the only tested concept where the economic timing matches the empirical horizon. Shock absorption plausibly happens quickly; requiring it to be h10-primary may be less natural than evaluating it as h5-led with h10 confirmation.

## Horizon Policy Implication

h5 should become an accepted research target for fast absorption mechanisms, but not a blanket validation shortcut.

Recommended distinction:

| Research type | Acceptable target horizon | Validation posture |
| --- | --- | --- |
| Fast shock absorption | h5 primary with h10 carry-through | Requires h5 stability, positive h10, low h20 dependence, and controlled similarity. |
| Repair/stabilization continuation | h10 or h15 primary | Requires h10/h15 dominance or at least validation-quality h10 behavior. |
| Existing inventory replacement or construction input | h10/h20 evidence depending on role | Requires governance review and monitoring refresh. |

h10 should remain the validation target for `short_horizon_volatility_shock_absorption_10` if the candidate is framed as a h10 repair mechanism. If the concept is reframed as h5-to-h10 shock absorption, future governance should require explicit h5 rules rather than silently using h5 because it is the best-performing horizon.

## Recommendation

Recommended path: run one more targeted h5/h10 design screen later, after documenting that the objective has shifted from strict h10 repair to h5-to-h10 shock absorption.

Near-term actions:

- Pause Expansion v5 implementation/refinement immediately.
- Keep `short_horizon_volatility_shock_absorption_10` as `CONDITIONAL_REFINEMENT_CANDIDATE`.
- Do not advance it to conditional validation.
- Do not refine it again until the next design note defines h5-to-h10 acceptance rules.
- Treat h10 as the key carry-through test, not necessarily the only valid primary horizon for fast shock absorption.

Future design screen should focus narrowly on:

- h5-to-h10 volatility/range shock absorption.
- Faster activation decay after volatility shocks.
- Co-activation control versus `volatility_compression_after_stress_stabilization`.
- Evidence that h10 remains positive without forcing a h10-only formulation.
- Avoiding h5-only microstructure noise or transient shock artifacts.

## What Should Not Be Repeated

- Broad drawdown-pressure stabilization in its current form.
- Simple inversion of drawdown-pressure failure.
- Overly broad idiosyncratic stress containment with high active-date coverage.
- Forcing h10 when the mechanism is economically fast and empirically h5-led.
- Immediate validation of `short_horizon_volatility_shock_absorption_10` without stronger h10 evidence.
- Additional refinement passes before the h5-to-h10 research objective is formally redesigned.
- Adding another volatility/stress candidate without monitoring similarity to `volatility_compression_after_stress_stabilization`.

## Closeout Decision

Expansion v5 should shift its next short-horizon research framing from `h10 repair` to `h5-to-h10 shock absorption`.

This is not a validation promotion. It is a roadmap correction. The live insight from v5 is that shorter-horizon repair may exist, but it appears to mature first at h5 and only partially carries into h10. The next useful step is not another immediate refinement; it is a small design-only h5/h10 screen that makes this horizon thesis explicit before any new implementation.
