# Alpha Family Diversification IC Discovery Review and Refinement Eligibility v1

Date: 2026-06-17

Source run id: `alpha_family_diversification_ic_discovery_v1`

Review scope: research-only audit of the completed 8-candidate IC discovery pass. No refinement, validation, governance mutation, threshold change, production registration, ML, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

The IC discovery pass found useful early evidence, but it is candidate-level evidence rather than broad family-level evidence.

Useful evidence:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20` has the cleanest IC profile: h10 mean IC 0.0125, h10 IC IR 0.1208, h10 positive IC rate 0.5951, and low approved-subset redundancy.
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20` has weaker but distinct evidence: h10 mean IC 0.0082, h10 IC IR 0.0933, h10 positive IC rate 0.5464, and very low approved-subset redundancy.

Family-level evidence:
- Neither family is broadly strong at the h10-h20 level.
- Dispersion is less negative on average and more structurally diverse, but only one dispersion candidate looks refinement-worthy.
- Persistence is weaker on average because `drawdown_rank_stability_20` is materially negative, but it contains the strongest individual candidate.

Further work:
- A small refinement design is justified now.
- Refinement should be limited to `post_drawdown_persistence_20` and `dispersion_transition_acceleration_20`.
- `transition_rank_stability_20` may remain diagnostic/watchlist only, not a primary refinement candidate.

This is enough to say alpha-family diversification is improving modestly, but not enough to claim a robust new family has been established.

## SECTION 2 - Candidate-Level Audit

| Candidate ID | Best horizon | Mean IC | IC IR | Positive IC rate | Redundancy context | Weakness | Recommendation |
|---|---:|---:|---:|---:|---|---|---|
| dispersion_expansion_transition_02 | h20 | -0.0237 | -0.2246 | 0.4246 | moderate approved-subset redundancy | Negative IC worsens into h10/h20; redundancy with compression stability is not offset by performance. | reject for now |
| dispersion_expansion_transition_04 | h5 overall / h10 primary | 0.0099 overall; 0.0082 at h10 | 0.1071 overall; 0.0933 at h10 | 0.5365 overall; 0.5464 at h10 | low approved-subset redundancy | h20 fades to -0.0007; evidence is short-to-medium horizon, not clean h20. | refinement candidate |
| dispersion_compression_reversal_02 | h10 by absolute IC | -0.0097 | -0.0724 | 0.4555 | moderate approved-subset redundancy | Negative h10/h20 behavior; top redundancy peer is `transition_rank_stability_20`. | reject for now |
| dispersion_structure_anomalies_01 | h20 by absolute IC | -0.0145 | -0.0867 | 0.5000 | moderate approved-subset redundancy | Negative mean IC despite balanced positive IC rate; anomaly structure is not translating into edge. | diagnostic-only |
| dispersion_structure_anomalies_03 | h20 by absolute IC | -0.0119 | -0.0819 | 0.4897 | moderate approved-subset redundancy | h1 is positive but h10/h20 fades and inverts; paired redundancy with skew anomaly. | diagnostic-only |
| rank_stability_after_drawdown_01 | h20 | -0.0593 | -0.2680 | 0.4013 | moderate approved-subset redundancy | Strongly adverse orientation across horizons; only 152 h10/h20 dates in best rows. | reject for now |
| rank_stability_after_drawdown_02 | h5 overall / h10 primary | 0.0137 overall; 0.0125 at h10 | 0.1322 overall; 0.1208 at h10 | 0.5992 overall; 0.5951 at h10 | low approved-subset redundancy | h20 decays to 0.0059; may be a h5-h10 persistence effect rather than full h20 family behavior. | refinement candidate |
| rank_coherence_regime_transition_02 | h5 overall / h20 primary evidence | -0.0071 overall; 0.0060 at h20 | -0.0474 overall; 0.0408 at h20 | 0.5090 overall; 0.5124 at h20 | moderate approved-subset redundancy | Mild h20 evidence only; negative h1/h5/h10 and redundant with compression stability. | hold for more evidence |

## SECTION 3 - Top Candidate Deep Review

### `rank_stability_after_drawdown_02`

Signal name: `post_drawdown_persistence_20`

Why it stood out:
- It is the strongest candidate in the 8-candidate scoring subset.
- h5 mean IC is 0.0137 with positive IC rate 0.5992.
- h10 mean IC is 0.0125 with positive IC rate 0.5951.
- Approved-subset redundancy is low: max absolute approved-subset correlation 0.1815.
- It is the only candidate combining positive primary-horizon evidence with low redundancy.

Distinctness from hostile/stress-repair family:
- The reviewed artifacts frame the candidate as rank persistence after drawdown, not participation or liquidity repair.
- The redundancy context is favorable versus the approved subset.
- However, the formula source stack includes downtrend/drawdown ingredients, so it still requires a later formula-level inspection to ensure it is not simply capturing recovery after stress.

What refinement should test later:
- Sign orientation and whether the effect is truly persistence rather than delayed reversal.
- h5 versus h10 concentration, because h20 evidence decays.
- Active coverage and whether the candidate depends on a small number of post-drawdown dates.
- Robustness of rank-stability definitions, including rank churn, drawdown depth, and post-drawdown observation windows.
- Redundancy against existing hostile/stress-repair inventory, not only against this diversification subset.

Key risks:
- The signal may be a short-lived h5-h10 effect rather than an h10-h20 family anchor.
- Drawdown conditioning may accidentally recreate stress-repair logic.
- The positive IC profile may be concentrated in a narrow market episode.

### `dispersion_expansion_transition_04`

Signal name: `dispersion_transition_acceleration_20`

Why it stood out:
- It is the best dispersion candidate after redundancy adjustment.
- h5 mean IC is 0.0099 with positive IC rate 0.5365.
- h10 mean IC is 0.0082 with positive IC rate 0.5464.
- Approved-subset redundancy is extremely low: max absolute approved-subset correlation 0.0455.
- It provides the clearest evidence that a dispersion-transition signal can be distinct from the rest of the scored subset.

Distinctness from hostile/stress-repair family:
- The candidate is conceptually tied to dispersion acceleration, not participation, liquidity, breadth repair, or hostile recovery.
- The low approved-subset redundancy supports statistical distinctness.
- There is no direct evidence from the reviewed outputs that it recreates the old hostile/stress-repair family.

What refinement should test later:
- Whether the useful effect is h5-h10 only or can be stabilized at h10.
- Whether h20 decay can be reduced without optimizing directly to a target metric.
- Whether dispersion acceleration should be smoothed, lagged, clipped, or separated into expansion versus compression states.
- Whether the signal remains distinct versus current production/watchlist stress-repair candidates.

Key risks:
- The effect is modest.
- h20 is approximately flat/slightly negative.
- Dispersion acceleration may overreact to noisy cross-sectional volatility changes.
- Refinement could accidentally overfit if it tries to force h20 performance.

## SECTION 4 - Family-Level Interpretation

### Persistence / Rank Stability

The persistence family is not broadly strong, but it contains the best individual candidate.

Evidence:
- Family h10 mean IC: -0.0166
- Family h20 mean IC: -0.0158
- Family h10 positive IC rate: 0.4710
- `post_drawdown_persistence_20` is positive and low-redundancy.
- `drawdown_rank_stability_20` is materially negative and overwhelms family averages.
- `transition_rank_stability_20` is weakly positive only at h20 and has moderate redundancy.

Interpretation:
- Persistence is promising as an isolated candidate effect.
- It is not yet a validated or broadly demonstrated alpha family.
- The next useful question is whether `post_drawdown_persistence_20` can be made more robust without becoming stress-repair.

### Dispersion

The dispersion family is broader and more distinct, but IC evidence is thin.

Evidence:
- Family h10 mean IC: -0.0053
- Family h20 mean IC: -0.0117
- Family h10 positive IC rate: 0.4851
- `dispersion_transition_acceleration_20` is the only dispersion candidate with positive h5/h10 evidence and very low subset redundancy.
- Compression and structure anomaly candidates are weak in the current pass.

Interpretation:
- Dispersion remains valuable as a diversification research axis because it is structurally distinct.
- Current IC evidence is isolated to one transition-acceleration candidate.
- A small refinement design is justified for that one candidate, not for the whole dispersion family.

Overall answer:
- Neither family is genuinely promising at the family level yet.
- Results are isolated candidate effects.
- The two isolated effects are still valuable enough to justify a small, constrained refinement design.

## SECTION 5 - Refinement Eligibility Decision

Proceed to a small refinement design: yes.

Eligible candidates:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`

Watchlist only:
- `rank_coherence_regime_transition_02` / `transition_rank_stability_20`

Refinement should aim to test:
- Sign orientation.
- h5/h10 versus h20 horizon concentration.
- Active coverage and date concentration.
- Robustness of rank-stability and dispersion-acceleration definitions.
- Whether evidence survives simple, pre-specified formula variants.
- Whether redundancy remains low versus existing hostile/stress-repair candidates.

Refinement must not optimize:
- Validation thresholds.
- Governance gates.
- Production registration status.
- Portfolio or ML integration.
- Candidate promotion/demotion decisions.
- Exhaustive parameter search.
- Direct h20 metric fitting.
- Any rule that implicitly converts the signal into hostile/stress-repair.

Candidates not eligible for refinement now:
- `dispersion_expansion_transition_02`
- `dispersion_compression_reversal_02`
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_stability_after_drawdown_01`

## SECTION 6 - Next Step Recommendation

1. Which candidates deserve refinement consideration?

Primary:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`

Secondary:
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`

Watchlist, not primary refinement:
- `rank_coherence_regime_transition_02` / `transition_rank_stability_20`

2. Which candidates should be excluded?

Exclude from refinement for now:
- `dispersion_expansion_transition_02`
- `dispersion_compression_reversal_02`
- `rank_stability_after_drawdown_01`

Keep diagnostic-only:
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`

Hold for more evidence:
- `rank_coherence_regime_transition_02`

3. Is this evidence enough to say alpha-family diversification is improving?

Yes, modestly. The project has moved from conceptual family diversification to actual panel-level and IC-level evidence for two distinct candidate effects. The evidence is not enough to claim a new robust family, but it is enough to justify a controlled second discovery/refinement design.

4. Should the next task be refinement design or another discovery pass?

The next task should be refinement design, not another broad discovery pass. The current evidence is narrow but actionable; a broad pass would likely add more redundancy before the two best signals are understood.

5. What should the next Codex task be?

Create a research-only refinement design for `post_drawdown_persistence_20` and `dispersion_transition_acceleration_20`. The design should specify limited diagnostic variants, active-coverage checks, sign/orientation checks, horizon-concentration diagnostics, and redundancy checks versus existing hostile/stress-repair inventory. It should not execute validation, mutate governance, modify thresholds, register production candidates, implement ML, or promote/demote any candidate.

## Audit Caveat

This is a review-only refinement eligibility audit. It does not establish production readiness, validation robustness, or governance eligibility. All recommendations are research workflow recommendations only.
