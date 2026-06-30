# Event-Defined Liquidity / Turnover Exhaustion Alpha v1 Design

Date: 2026-05-23

Status: `DESIGN_ONLY`

Research label: `event_defined_liquidity_turnover_exhaustion_alpha_v1`

## Design Objective

Recent broad continuous research branches were structurally clean but weak:

- `structural_interaction_alpha_expansion_v2`: `CLOSED_WEAK_RESEARCH`
- `proxy_relative_residual_alpha_batch_v1`: `CLOSED_WEAK_RESEARCH`

The recurring failure mode was broad activation with weak standalone IC. This design pivots toward discrete, recurring liquidity and turnover exhaustion events where the trigger, exhaustion confirmation, and post-event repair window are explicitly separated.

Core research question:

Can discrete turnover/liquidity stress events followed by exhaustion, repair, or normalization produce cleaner h10/h20 alpha behavior than broad continuous structures?

This is a design-only note. It does not implement candidates, create a runner, change production paths, or alter validation/governance.

## Event Framework

Each candidate should be built from three interpretable pieces:

1. Event trigger
2. Exhaustion confirmation
3. Repair / recovery scoring window

The event trigger should identify abnormal pressure. The exhaustion confirmation should test whether that pressure is fading or being absorbed. The repair score should measure whether the post-event behavior is constructive without collapsing into reversal, momentum, or liquidity-factor duplication.

## Event Trigger Definitions

Candidate triggers should be discrete enough to avoid broad activation but recurring enough for reliable diagnostics.

Potential trigger families:

- abnormal turnover spike relative to recent baseline
- abnormal volume participation relative to medium-term liquidity
- liquidity demand shock, measured by dollar-volume expansion plus unstable price/range behavior
- liquidity vacuum behavior, where price/range pressure is high but participation quality deteriorates
- abnormal range/volume pressure, where realized range and turnover expand together
- failed liquidity support, where volume expands but price/range behavior remains disorderly

Design principle:

The trigger should define an event, not a continuous always-on factor. A candidate should have a clear answer to: "What happened on this date that makes it eligible?"

## Exhaustion Confirmation

Exhaustion is the key distinction from simple stress, reversal, or momentum. A turnover/liquidity event should not be scored as useful just because pressure was large.

Possible confirmation signals:

- turnover fades after a stress spike
- volume intensity decays after abnormal participation
- range compresses after range/volume expansion
- realized volatility stabilizes after liquidity stress
- participation normalizes without renewed price instability
- post-event dollar-volume remains adequate but no longer disorderly
- high-turnover names stop making new adverse range/pressure extremes

Useful confirmation should occur after the trigger and before the primary forward horizon measurement. Avoid definitions that simply rank the same-day rebound.

## Repair / Recovery Window

Primary evaluation horizons:

- h10
- h20

Diagnostic-only horizon:

- h5

Avoid treating h1 or h5-led behavior as a primary success. Short-horizon behavior can help diagnose whether the event is too noisy, but a candidate should not advance unless h10/h20 behavior is meaningfully positive and persistent.

The intended timing is:

1. stress / liquidity event occurs
2. turnover or volume pressure fades
3. range, volatility, or participation normalizes
4. medium-horizon forward behavior is evaluated

## Candidate Family Ideas

### `turnover_shock_exhaustion_repair_20`

Thesis: extreme turnover events may become informative only when turnover fades afterward and price/range behavior stops deteriorating.

Differentiation: not raw turnover, not reversal after a down day, not volume-confirmed momentum.

### `liquidity_vacuum_repair_after_turnover_stress_20`

Thesis: names experiencing liquidity vacuum behavior may recover only when turnover stress is followed by adequate liquidity and narrower range behavior.

Differentiation: focuses on repair after a liquidity vacuum, not broad liquidity quality.

### `high_participation_stress_fade_quality_20`

Thesis: high participation during stress is not enough; the useful event may be high participation followed by fading disorder and stable participation quality.

Differentiation: avoids existing participation/breadth repair clones by requiring post-event fade quality rather than active hostile-state repair.

### `event_volume_exhaustion_vol_stabilization_20`

Thesis: abnormal volume events may contain medium-horizon information when volume intensity fades and volatility stabilizes instead of propagating.

Differentiation: not broad volatility compression; the volatility stabilization must follow a volume-defined event.

### `failed_propagation_after_liquidity_shock_20`

Thesis: the edge may live in liquidity shocks that fail to propagate into continuing instability.

Differentiation: measures failure of propagation after a discrete shock, not calm-state stability or transition-state detector labels.

### `turnover_stress_recovery_efficiency_10_20`

Thesis: some names recover more efficiently after turnover stress, with less volatility and range cost per unit of normalized liquidity.

Differentiation: evaluates recovery efficiency after a defined stress event, not broad residual quality or low-volatility exposure.

## Event-Quality Requirements

An event-defined candidate should be considered usable only if it satisfies all of the following:

- recurring enough to evaluate across rolling windows
- not crisis-only
- not dominated by one or two windows
- not always active or broad-market active
- not too sparse for h10/h20 diagnostics
- trigger and confirmation are separately interpretable
- post-event behavior is medium-horizon relevant
- event timing does not leak forward information
- signal remains meaningfully different from current inventory candidates

Design-level warning signs:

- event triggers fire on most dates
- event triggers appear only in crisis windows
- post-event confirmation is equivalent to same-day reversal
- candidate ranking is mostly price momentum or price rank
- useful IC appears only in one bucket, one window, or one stress episode

## Anti-Failure Diagnostics

Any future implementation batch should include:

- hidden reversal overlap
- hidden momentum overlap
- crisis-window concentration
- one-window dominance
- stress-only dependency
- event recurrence quality
- sample-size sanity
- broad activation with weak IC
- sparse-event fragility
- inventory similarity
- volatility / low-vol carry overlap
- liquidity factor duplication
- h10/h20 primary scoring
- h5 diagnostic-only behavior
- event trigger frequency by year/window
- trigger-to-confirmation conversion rate
- confirmation-to-signal active coverage
- event half-life / persistence
- post-event turnover drift
- state/regime attribution

## Implementation Risks

Main risks:

- disguised reversal after high-volume selloffs
- disguised momentum after high-volume breakouts
- liquidity-size factor duplication
- volatility carry / low-volatility exposure
- crisis-only dependence
- events too sparse for reliable WFV-style diagnostics
- events too broad, recreating the prior activation problem
- over-fragmenting event definitions until sample size becomes meaningless

The first implementation should avoid a parameter grid. Use a small number of interpretable event definitions, each with one simple trigger and one simple exhaustion confirmation.

## Recommended Future Batch

If implemented later, use a small research-only batch of 5-6 candidates:

1. `turnover_shock_exhaustion_repair_20`
2. `liquidity_vacuum_repair_after_turnover_stress_20`
3. `high_participation_stress_fade_quality_20`
4. `event_volume_exhaustion_vol_stabilization_20`
5. `failed_propagation_after_liquidity_shock_20`
6. `turnover_stress_recovery_efficiency_10_20`

Recommended runner, if approved later:

- `pipelines/run_event_defined_liquidity_turnover_exhaustion_alpha_v1.py`

Recommended artifacts, if approved later:

- `artifacts/research/event_defined_liquidity_turnover_exhaustion_alpha_v1/`

Recommended note, if approved later:

- `docs/research_notes/event_defined_liquidity_turnover_exhaustion_alpha_v1_results.md`

Classification labels should remain conservative:

- `REJECT_RESEARCH`
- `CONDITIONAL_ONLY_RESEARCH`
- `CONDITIONAL_REFINEMENT_CANDIDATE`
- `CANDIDATE_FOR_CONDITIONAL_VALIDATION`

No candidate should advance unless it shows h10/h20 strength, adequate event recurrence, low reversal/momentum overlap, low inventory redundancy, no crisis-only dependence, and acceptable WFV-style persistence.

## Guardrails

This design does not:

- implement candidates
- create a runner
- modify existing code
- touch detector files
- change production registration
- mutate survivor/watchlist state
- change gates, schemas, thresholds, validation logic, or governance
- route anything into portfolio, ML, blending, or optimization

