# Rank-Coherence IC Discovery Pass v1

Date: 2026-06-18

Project: Project Underdog

Run id: `rank_coherence_ic_discovery_v1`

Scope: research-only IC discovery pass for the approved six-candidate rank-coherence subset. No refinement, validation, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Scoring scope:
- Approved candidates scored: 6.
- Held-back candidates not scored: 4.
- Horizons scored: h1, h5, h10, h20.
- Outputs written under `artifacts/research/rank_coherence_family_discovery_v1/ic_discovery/`.

Completion status: completed. The pass produced approved subset metadata, horizon IC scores, daily IC rows, candidate summaries, coverage diagnostics, family/theme summaries, horizon summaries, approved-subset redundancy context, and a research-only manifest.

Strongest candidates:
- `rank_coherence_regime_independent_02` / `nonhostile_transition_rank_coherence_20`: best broad profile, with h5 mean IC 0.0118, h10 mean IC 0.0082, h20 mean IC 0.0100, and positive h5/h10/h20 IC behavior.
- `rank_coherence_churn_avoidance_02` / `relative_rank_turnover_resilience_20`: strongest h20 candidate, with h20 mean IC 0.0116, h20 IC IR 0.0649, and h20 positive IC rate 0.5496.
- `rank_coherence_reversal_pressure_01` / `rank_shock_reversion_pressure_5_20`: useful h1/h10 evidence, but h20 fades to slightly negative.

Strongest themes:
- Regime-Independent Rank Coherence showed the cleanest h5/h10/h20 profile.
- Rank Churn Avoidance showed the strongest h20 evidence.
- Rank Reversal Pressure was mixed: one candidate was useful, while the second was adverse.

Overall family assessment:

Rank-coherence produced useful candidate-level evidence, but not broad family-level evidence. The family-level mean IC was slightly negative at h1, h5, h10, and h20 because weak/adverse candidates offset the two constructive h10/h20 candidates. The discovery result supports a refinement-review discussion for selected candidates, not a claim that rank-coherence is already an established alpha family.

## SECTION 2 - Candidate Results

| Candidate ID | Signal | h1 mean IC | h5 mean IC | h10 mean IC | h20 mean IC | Best h10/h20 | Interpretation |
|---|---|---:|---:|---:|---:|---:|---|
| `rank_coherence_leadership_stability_02` | `cross_window_rank_agreement_10_20` | -0.0009 | 0.0037 | -0.0016 | -0.0095 | h20 -0.0095 | Weak. h5 positive-rate behavior is acceptable, but h10/h20 evidence is not supportive. |
| `rank_coherence_churn_avoidance_02` | `relative_rank_turnover_resilience_20` | 0.0020 | 0.0057 | 0.0036 | 0.0116 | h20 0.0116 | Useful. Positive across all horizons, strongest at h20, with h20 positive IC rate 0.5496. |
| `rank_coherence_reversal_pressure_01` | `rank_shock_reversion_pressure_5_20` | 0.0091 | 0.0009 | 0.0075 | -0.0007 | h10 0.0075 | Mixed but useful. h1/h10 are positive, h20 fades slightly negative. |
| `rank_coherence_reversal_pressure_02` | `rank_acceleration_disagreement_5_20` | -0.0032 | -0.0157 | -0.0197 | -0.0207 | h20 -0.0207 | Reject. Adverse across horizons, with weak h10/h20 positive IC rates. |
| `rank_coherence_concentration_02` | `leadership_broadening_entry_20` | -0.0133 | -0.0084 | -0.0105 | 0.0011 | h10 -0.0105 | Weak/adverse. h20 is barely positive, while h1/h5/h10 are negative. |
| `rank_coherence_regime_independent_02` | `nonhostile_transition_rank_coherence_20` | 0.0016 | 0.0118 | 0.0082 | 0.0100 | h20 0.0100 | Strongest broad profile. Positive h5/h10/h20, best IC IR at h5, and supportive h20 durability. |

Detailed horizon diagnostics:

| Candidate ID | h10 IC IR | h10 positive IC rate | h20 IC IR | h20 positive IC rate | Notable strengths | Notable weaknesses |
|---|---:|---:|---:|---:|---|---|
| `rank_coherence_leadership_stability_02` | -0.0110 | 0.5223 | -0.0719 | 0.5041 | h5 positive-rate signal. | h10/h20 mean IC negative; no refinement-quality evidence. |
| `rank_coherence_churn_avoidance_02` | 0.0199 | 0.5223 | 0.0649 | 0.5496 | Best h20 result; positive across horizons. | h10 is modest; moderate redundancy with regime-independent candidate. |
| `rank_coherence_reversal_pressure_01` | 0.0423 | 0.5385 | -0.0047 | 0.5062 | Good h1/h10 behavior; theme-distinct from most other candidates. | h20 fades; h5 is nearly flat. |
| `rank_coherence_reversal_pressure_02` | -0.1510 | 0.3968 | -0.1537 | 0.3864 | Low redundancy versus subset. | Directionally adverse; likely wrong orientation or invalid construction. |
| `rank_coherence_concentration_02` | -0.0574 | 0.4777 | 0.0065 | 0.4979 | Only h20 slightly positive. | Negative h1/h5/h10; not useful as scored. |
| `rank_coherence_regime_independent_02` | 0.0603 | 0.5202 | 0.0759 | 0.5269 | Best h5/h10/h20 consistency; strongest refinement candidate. | Moderate redundancy with churn avoidance; h10/h20 positive rates are supportive but not high. |

Coverage diagnostics:
- All six scored candidates had 504 active signal dates.
- Active date ratio was 0.2402 versus the full close-price index.
- Mean active ticker count ranged from 457.8 to 471.6.
- Candidate panels had sufficient coverage for h1/h5/h10/h20 IC scoring.

## SECTION 3 - Theme Assessment

Leadership Stability:

Evidence was weak. The representative candidate had h5 mean IC 0.0037 but h10 mean IC -0.0016 and h20 mean IC -0.0095. This theme should not be eliminated permanently, but this construction should not proceed to refinement.

Rank Churn Avoidance:

Evidence was useful. `relative_rank_turnover_resilience_20` was positive across all horizons and strongest at h20. This is the best evidence that rank-coherence may extend beyond short-horizon effects. The main caveat is possible overlap with the persistence lineage because churn concepts are naturally adjacent to persistence.

Rank Reversal Pressure:

Evidence was mixed. `rank_shock_reversion_pressure_5_20` had useful h1 and h10 evidence, while `rank_acceleration_disagreement_5_20` was materially adverse across horizons. The theme should not be eliminated, but it needs formula-level diagnosis before any refinement design.

Leadership Concentration and Broadening:

Evidence was weak/adverse. `leadership_broadening_entry_20` was negative at h1/h5/h10 and only slightly positive at h20. This theme should be rejected for the current rank-coherence discovery track unless later diagnostics reveal a sign or construction issue.

Regime-Independent Rank Coherence:

Evidence was the strongest. `nonhostile_transition_rank_coherence_20` had positive h5/h10/h20 evidence, with h20 mean IC 0.0100 and h20 IC IR 0.0759. This theme is eligible for refinement-review consideration.

Themes that showed evidence:
- Regime-Independent Rank Coherence.
- Rank Churn Avoidance.
- Rank Reversal Pressure, but only through `rank_shock_reversion_pressure_5_20`.

Themes that showed weak evidence:
- Leadership Stability.
- Leadership Concentration and Broadening.

Themes that should be eliminated for now:
- Leadership Concentration and Broadening, as represented by `leadership_broadening_entry_20`.

## SECTION 4 - Family Assessment

1. Does rank-coherence appear distinct from persistence?

Partially. The discovery pass used rank-coherence candidates rather than post-drawdown persistence candidates, and the approved subset avoided the held-back duplicate cluster. However, the best h20 candidate is Rank Churn Avoidance, which is conceptually adjacent to persistence. Rank-coherence appears distinct enough to continue as a research track, but persistence-lineage redundancy must be reviewed before any validation discussion.

2. Does rank-coherence appear distinct from hostile/stress-repair?

Yes at the artifact and registry level. The candidates are not framed around hostile/stress repair, participation repair, liquidity repair, weak-breadth recovery, or volatility compression. This IC pass did not run state attribution or stress-reference contamination diagnostics, so the conclusion is preliminary and must be revisited during any refinement-readiness review.

3. Is there evidence of a new alpha family?

There is early candidate-level evidence, not family-level proof. Two h10/h20 candidates are constructive, but the family-level mean IC is slightly negative at h10 and h20 because weak/adverse candidates remain in the subset.

Family-level summary:
- h1 family mean IC: -0.0008.
- h5 family mean IC: -0.0003.
- h10 family mean IC: -0.0021.
- h20 family mean IC: -0.0014.
- h10 mean positive IC rate: 0.4963.
- h20 mean positive IC rate: 0.4952.

4. Is evidence candidate-level or family-level?

Evidence is candidate-level. The strongest candidates justify refinement-review consideration, but the family is not broadly established.

## SECTION 5 - Refinement Eligibility Review

| Candidate ID | Classification | Rationale |
|---|---|---|
| `rank_coherence_regime_independent_02` | eligible for refinement review | Strongest broad h5/h10/h20 evidence; coherent non-hostile rank-coherence thesis. |
| `rank_coherence_churn_avoidance_02` | eligible for refinement review | Positive across all horizons, strongest h20 evidence, but requires persistence-lineage redundancy review. |
| `rank_coherence_reversal_pressure_01` | watchlist only | h1/h10 evidence is useful, but h20 fades and theme peer is adverse. |
| `rank_coherence_leadership_stability_02` | diagnostic only | h5 positive but h10/h20 weak/negative; useful mainly as rank-agreement diagnostic. |
| `rank_coherence_concentration_02` | reject | Negative h1/h5/h10 and only negligible h20 support. |
| `rank_coherence_reversal_pressure_02` | reject | Adverse across horizons and weak positive IC rates at h10/h20. |

These are research classifications only. They do not refine, validate, promote, demote, register, or govern any candidate.

## SECTION 6 - Final Recommendation

1. Did rank-coherence produce useful evidence?

Yes, but at the candidate level only. `nonhostile_transition_rank_coherence_20` and `relative_rank_turnover_resilience_20` produced useful h10/h20 evidence, while `rank_shock_reversion_pressure_5_20` produced useful h1/h10 evidence.

2. Which candidate is strongest?

`rank_coherence_regime_independent_02` / `nonhostile_transition_rank_coherence_20` is the strongest overall candidate because it is positive at h5, h10, and h20 and has the best broad medium-horizon profile.

3. Which theme is strongest?

Regime-Independent Rank Coherence is the strongest theme. Rank Churn Avoidance is second and may be important, but it carries higher persistence-overlap risk.

4. Is refinement justified?

Yes, a small refinement-review design is justified for `rank_coherence_regime_independent_02` and `rank_coherence_churn_avoidance_02`. Actual refinement should not proceed until a separate design task defines narrow scope, persistence-overlap controls, stress-repair contamination checks, and candidate count limits.

5. What should the next Codex task be?

The next Codex task should be `Rank-Coherence Refinement Eligibility and Design v1`. It should review this IC discovery pass, determine whether the two eligible candidates deserve a small refinement program, define anti-overfitting and anti-contamination controls, and explicitly avoid refinement execution, validation, governance mutation, threshold changes, production registration, ML, and candidate promotion/demotion.

## Research Caveat

This was a research-only IC discovery pass. It does not establish validation readiness, production readiness, governance eligibility, or candidate promotion. No refinement, validation, governance mutation, threshold change, production registration, ML, promotion, or demotion was performed.
