# Recovery Quality Target Experiment v1 Closeout

Date: 2026-05-25

Status: `TARGET_DIAGNOSTIC_SIDECAR_USEFUL`

Action: retain recovery-quality targets as a research diagnostic sidecar only. This closeout does not change validation anchors, gates, thresholds, candidate statuses, production registration, portfolio logic, ML routing, blending, optimization, detector usage, metadata usage, or governance.

## Objective

`recovery_quality_target_experiment_v1` tested whether current inventory candidates and selected parked weak clues express clearer behavior under recovery-oriented target definitions than under raw h10/h20 forward-return IC alone.

The experiment was research-only and diagnostic-only. Raw h10/h20 forward-return IC remained the benchmark anchor throughout the review.

Targets compared:

- raw h10 forward return
- raw h20 forward return
- drawdown-adjusted forward return
- downside-controlled return
- recovery-quality composite
- post-stress stabilization target

## Key Findings By Candidate

| Candidate | Raw-return anchor | Alternative-target behavior | Interpretation |
| --- | ---: | --- | --- |
| `participation_breadth_repair_under_hostile_trend` | raw h20 IC `0.022875` | Alternative targets did not materially improve the profile; best alternative was drawdown-adjusted h20 IC `0.024256`. | Remains the cleanest raw alpha anchor in the current inventory. |
| `participation_liquidity_state_shift_20_60` | raw h20 IC `0.008421` | Recovery/post-stress targets showed much stronger diagnostic lift, led by post-stress stabilization h20 IC `0.109989`. | Better interpreted as recovery/stabilization behavior than as a pure raw-return leader. |
| `volatility_compression_after_stress_stabilization` | raw h20 IC `0.011071` | Improved under drawdown-adjusted h20 IC `0.029107` and downside-controlled h20 IC `0.027090`. | More consistent with drawdown/downside-control structure than broad recovery-composite behavior. |
| `short_horizon_volatility_shock_absorption_10` | raw h10 IC `0.010260`; raw h20 IC `0.003243` | Strongest recovery/post-stress diagnostic lift, led by post-stress stabilization h20 IC `0.163104` and recovery-quality h20 IC `0.135203`. | Useful diagnostic clue for shock absorption and stabilization behavior, but not validation evidence. |
| `volatility_participation_asymmetry_20_original` | raw h20 IC `0.012154` | Only modest drawdown-adjusted improvement, best alternative h20 IC `0.016036`. | Remains parked weak research evidence. |
| `turnover_shock_exhaustion_repair_20` | raw h20 IC `0.004927` | Only modest drawdown-adjusted improvement, best alternative h20 IC `0.009653`. | Remains weak and not revived by alternative targets. |

## Candidate Role Interpretation

Raw alpha anchor:

- `participation_breadth_repair_under_hostile_trend` remains the strongest candidate on raw h20 forward-return IC. Its role is still best understood as the primary raw-return anchor among the current inventory candidates.

Recovery/stabilization behavior:

- `participation_liquidity_state_shift_20_60` and `short_horizon_volatility_shock_absorption_10` showed the clearest lift under recovery-quality and post-stress stabilization targets.
- This suggests their behavior may be tied to repair, absorption, and stabilization quality, but the evidence should be used only to interpret mechanism fit.

Drawdown/downside-control structure:

- `volatility_compression_after_stress_stabilization` improved more under drawdown-adjusted and downside-controlled returns than under recovery-composite targets.
- Its role is better described as downside-control or path-quality behavior, not a new raw-return validation candidate.

Parked weak clues:

- `volatility_participation_asymmetry_20_original` and `turnover_shock_exhaustion_repair_20` did not become compelling under alternative targets.
- Their status should remain parked research evidence.

## Why Raw h10/h20 IC Remains The Validation Anchor

Alternative targets helped explain some mechanisms, but they are not clean substitutes for standalone return prediction. Recovery-quality and post-stress stabilization targets intentionally include path-quality, stabilization, and downside behavior, so strong correlations with repair-style signals can reflect target-feature proximity rather than independent alpha.

Raw h10/h20 forward-return IC remains the cleanest primary validation anchor because it is simpler, harder to game, easier to compare across candidates, and less likely to reward signals merely for matching the target construction.

## Target Hacking Warning

This experiment should not be used to lower standards or promote weak candidates through friendlier targets. A candidate that looks materially better only under an alternative target should be treated as mechanism evidence, not as validation evidence.

Future research should avoid repeatedly redesigning targets until parked candidates look acceptable. Alternative targets are useful only when they clarify candidate behavior and failure modes.

## Target-Feature Proximity Caveats

The strongest recovery/post-stress lifts appeared in candidates whose mechanisms already include repair, stabilization, shock absorption, or liquidity recovery semantics. That proximity is informative, but it also raises the risk that the target is partially rewarding the same behavior used to define the signal.

The post-stress and recovery-quality results therefore require skepticism. They can support interpretation and future diagnostic design, but they do not establish standalone tradable alpha.

## Low-Volatility Check

No alternative target crossed the low-volatility reward warning threshold. The highest observed low-volatility overlaps were below the warning line, led by post-stress stabilization h20 and recovery-quality h20.

This reduces, but does not remove, the risk that alternative targets are quietly rewarding low-volatility or passive downside exposure. Low-volatility overlap should remain part of any future target-sidecar diagnostics.

## Final Decision

Final status: `TARGET_DIAGNOSTIC_SIDECAR_USEFUL`

The recovery-quality target experiment is useful as a diagnostic sidecar. It helps separate raw-return alpha behavior from recovery quality, stabilization quality, downside containment, and context usefulness.

It does not justify any validation change, candidate promotion, status mutation, or production routing.

## Recommended Future Use

Use recovery-quality and post-stress targets only as research diagnostics:

- interpret why repair/stabilization candidates work or fail
- compare whether a signal is raw-return predictive, downside-controlling, recovery-sensitive, or context-like
- flag target-feature proximity risk
- monitor low-volatility overlap and passive-risk reward
- inform future target-definition research notes

Do not use these targets as replacement validation gates or as standalone promotion criteria.

## Intentional Non-Changes

- No validation logic changes
- No gate or threshold changes
- No candidate status changes
- No production registration changes
- No portfolio, ML, blending, or optimization routing
- No detector changes
- No metadata changes
- No governance changes
