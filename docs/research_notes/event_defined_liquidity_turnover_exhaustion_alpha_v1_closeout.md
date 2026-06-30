# Event-Defined Liquidity / Turnover Exhaustion Alpha v1 Closeout

Date: 2026-05-23

Run id: `event_defined_liquidity_turnover_exhaustion_alpha_v1`

Final status: `CLOSED_WEAK_RESEARCH`

## Objective

This research-only batch tested whether discrete liquidity and turnover stress events, followed by exhaustion, repair, or normalization behavior, could produce cleaner h10/h20 alpha behavior than recent broad continuous structures.

The branch was a strategic pivot away from weak broad activation in:

- `structural_interaction_alpha_expansion_v2`
- `proxy_relative_residual_alpha_batch_v1`

## Candidates Tested

1. `turnover_shock_exhaustion_repair_20`
2. `liquidity_vacuum_repair_after_turnover_stress_20`
3. `high_participation_stress_fade_quality_20`
4. `event_volume_exhaustion_vol_stabilization_20`
5. `failed_propagation_after_liquidity_shock_20`
6. `turnover_stress_recovery_efficiency_10_20`

Primary evaluation remained h10/h20. h1/h5 behavior was diagnostic only.

## Classification Outcome

All six candidates were classified as `REJECT_RESEARCH`.

No candidate reached:

- `CONDITIONAL_ONLY_RESEARCH`
- `CONDITIONAL_REFINEMENT_CANDIDATE`
- `CANDIDATE_FOR_CONDITIONAL_VALIDATION`

## Strongest Weak Clue

The strongest weak clue was `turnover_shock_exhaustion_repair_20`.

Observed behavior:

- h10 IC: `0.002872`
- h20 IC: `0.004927`
- WFV-style persistence / sign consistency: `0.75 / 0.75`
- low inventory overlap
- low reversal and momentum overlap

However, the candidate remained too weak and too broadly active. The event trigger fired on most dates, which means the formulation did not truly escape the broad activation problem.

## Why Nothing Advanced

The event definitions were diagnosable, but they did not produce usable standalone medium-horizon alpha.

Main failure modes:

- most event triggers still fired too broadly
- h10/h20 IC was weak or negative
- selective candidates often became sparse, unstable, or negative
- `event_volume_exhaustion_vol_stabilization_20` had hidden low-volatility / range-volatility overlap
- `failed_propagation_after_liquidity_shock_20` had liquidity-factor duplication and sparse effective IC support
- liquidity vacuum repair was strongly negative at h10/h20
- no candidate combined event recurrence, controlled activation, positive medium-horizon IC, WFV support, and low duplication

## Key Lesson

With the current OHLCV-only data, liquidity/turnover exhaustion did not separate enough from broad liquidity, volatility, and low-volatility behavior.

The batch did improve observability: trigger frequency, confirmation conversion, sparsity, broad activation, low-vol overlap, and liquidity-factor duplication were all visible. But that better diagnostic resolution did not translate into a viable alpha candidate.

## Decision

Do not refine this branch immediately.

Preserve `turnover_shock_exhaustion_repair_20` only as weak research evidence. Do not promote any candidate, do not run a threshold-tuning pass, and do not treat h5 or sparse state evidence as alpha evidence.

## Intentional Non-Changes

This closeout did not introduce:

- detector changes
- production registration
- survivor/watchlist mutation
- validation, gate, schema, or governance changes
- portfolio, ML, blending, or optimization routing

