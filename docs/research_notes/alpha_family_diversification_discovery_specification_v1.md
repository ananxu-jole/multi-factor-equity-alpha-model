# Alpha Family Diversification Discovery Specification v1

Date: 2026-06-17

## SECTION 1 – Strategic Context

Project Underdog currently has a narrow alpha library concentrated in a conditional hostile/stress repair family, with only a possible secondary volatility compression family. The candidate pool is dominated by h20, state-conditioned outcomes and carries high redundancy risk between participation/liquidity and breadth repair hypotheses.

Diversification objectives:
- discover structurally distinct alpha families before metadata-enriched or ML-driven research,
- reduce reliance on stress/hostile regime repair as the primary research axis,
- improve horizon and regime coverage while keeping the candidate set auditable.

This batch exists to execute the first deliberate diversification discovery effort focused on Dispersion behavior and Persistence / Rank Stability behavior, using the current infrastructure without code or governance changes.

## SECTION 2 – Discovery Batch Structure

Batch design:
- target family count: 2 families (Dispersion, Persistence / Rank Stability)
- target themes: 5 themes (3 dispersion, 2 persistence)
- target candidate count per theme: 3–5 candidates
- expected total candidate count: 15–20 candidates
- preferred execution order: Dispersion themes first, then Persistence themes, with a combined but partitioned batch
- governance checkpoints: pre-launch theme review, mid-batch redundancy review, post-batch family-distinctness evaluation

Rationale:
- 2 families keep the batch focused while addressing the primary diversification gap.
- 3–5 themes offer a broad enough search space without brute-force expansion.
- 15–20 candidates is large enough to explore hypothesis variation but small enough to audit and compare.

## SECTION 3 – Dispersion Family Specification

### Theme 1: Dispersion Expansion Transition
- Economic hypothesis: securities that lead or emerge early in a widening cross-sectional dispersion phase outperform as the market reorganizes.
- Required feature inputs: return dispersion, cross-sectional volatility, breadth dispersion, relative volatility measures, pairwise dispersion metrics.
- Transformation candidates: change-in-dispersion signals, dispersion momentum, dispersion trend acceleration, cross-sectional standard deviation of returns, dispersion rank changes.
- Ranking approaches: score securities by positive dispersion leadership, rising relative dispersion, or outlier moves in dispersion-based rankings.
- Conditioning approaches: condition on periods of rising cross-sectional dispersion, regime transition flags, and non-panic directional dispersion expansion.
- Horizon focus: h10-h20 primarily; h5 explored as a secondary short-term reaction test.
- Expected behavior: candidate alpha is triggered by structural cross-sectional widening rather than stress repair, with early dispersion leaders showing outperformance.
- Expected failure modes: may capture panic-only stress behavior, become too similar to volatility compression after stress, or overfit to noisy dispersion spikes.
- Minimum candidate count: 3
- Maximum candidate count: 5

### Theme 2: Dispersion Compression Reversal
- Economic hypothesis: securities that stabilize earlier than peers during dispersion compression outperform as the market rotates from divergent to more coherent behavior.
- Required feature inputs: dispersion trend, change in pairwise return correlation, cross-sectional volatility decline, normalization rate.
- Transformation candidates: dispersion compression momentum, compression confirmation scores, relative stabilization rank, peer volatility convergence metrics.
- Ranking approaches: rank equities by the speed or quality of dispersion compression relative to the universe.
- Conditioning approaches: condition on transitions from high dispersion to falling dispersion, and on regimes with active compression but not yet broad recovery.
- Horizon focus: h10-h20 primarily.
- Expected behavior: the alpha should emerge from early stabilization rather than from simple stress exit, identifying securities that compress ahead of the market.
- Expected failure modes: overlaps with stress recovery if compression is interpreted as simple de-stressing; may also be dominated by low-volatility securities.
- Minimum candidate count: 3
- Maximum candidate count: 5

### Theme 3: Dispersion Structure Anomalies
- Economic hypothesis: persistent cross-sectional dispersion anomalies such as skewed dispersion, clustering, or asymmetry reveal securities with non-reversion or momentum potential.
- Required feature inputs: dispersion skewness/kurtosis, cluster dispersion measures, cross-sectional tail dispersion, sector-relative dispersion deviations.
- Transformation candidates: dispersion anomaly scores, asymmetric dispersion ranks, cluster vs market dispersion ratios.
- Ranking approaches: rank securities by their contribution to dispersion anomalies or by their position within dispersion clusters.
- Conditioning approaches: condition on anomalous dispersion states, such as high tail dispersion or cluster divergence, rather than stress recovery.
- Horizon focus: h10-h20 with possible h5 exploratory tests.
- Expected behavior: alpha may come from securities that are structurally mispriced during unusual cross-sectional dispersion patterns.
- Expected failure modes: may be hard to distinguish from broad volatility or stress effects; may be data-sparse.
- Minimum candidate count: 2
- Maximum candidate count: 4

## SECTION 4 – Persistence / Rank Stability Family Specification

### Theme 4: Rank Stability After Drawdown
- Economic hypothesis: securities that maintain or improve cross-sectional rank stability after drawdowns are more durable performers than those with volatile rank paths.
- Required feature inputs: rank history, rank churn, turnover proxies, drawdown extent and duration, active coverage consistency.
- Transformation candidates: rank stability scores, post-drawdown rank persistence, volatility of rank change, rank churn decay measures.
- Ranking approaches: rank securities by stability of rank relative to peers after a drawdown event, rewarding consistent upward or steady ranking.
- Conditioning approaches: condition on recent drawdown periods and on signals with improving rank stability rather than on regime state.
- Horizon focus: h10-h20 primarily.
- Expected behavior: outperformance arises from structural stability rather than state-based recovery; low-rank-churn securities persist.
- Expected failure modes: may select low-volatility or large-cap securities, or may overlap with low-turnover passive behavior.
- Minimum candidate count: 3
- Maximum candidate count: 5

### Theme 5: Rank Coherence Regime Transition
- Economic hypothesis: securities that exhibit improved cross-sectional rank coherence during regime transitions are more likely to thrive in the new regime.
- Required feature inputs: rank coherence metrics, regime transition labels, cross-sectional rank dispersion, transition-state persistence.
- Transformation candidates: coherence improvement scores, regime transition adjusted rank stability, rank dispersion compression measures.
- Ranking approaches: rank securities by the degree of improved rank coherence during regime transitions, favoring those that stabilize ahead of peers.
- Conditioning approaches: condition on documented regime transitions and on securities whose rank coherence improves regardless of stress orientation.
- Horizon focus: h10-h20 primarily.
- Expected behavior: alpha emerges from relative stability around regime boundaries rather than from hostile/stress repair.
- Expected failure modes: may collapse into stress repair if regime transitions are defined too narrowly as hostile-to-normal, or may underperform in non-transition environments.
- Minimum candidate count: 2
- Maximum candidate count: 4

## SECTION 5 – Candidate Matrix Design

| Theme | Feature group | Conditioning approach | Horizon | Expected family | Minimum candidates | Maximum candidates |
|---|---|---|---|---|---|---|
| Dispersion Expansion Transition | dispersion / cross-sectional variance | rising dispersion regimes | h10-h20 | Dispersion | 3 | 5 |
| Dispersion Compression Reversal | dispersion / correlation compression | compression transitions | h10-h20 | Dispersion | 3 | 5 |
| Dispersion Structure Anomalies | dispersion skew / clustering | anomalous dispersion states | h10-h20 | Dispersion | 2 | 4 |
| Rank Stability After Drawdown | rank churn / persistence | post-drawdown stability | h10-h20 | Persistence | 3 | 5 |
| Rank Coherence Regime Transition | rank coherence / regime shift | regime transitions | h10-h20 | Persistence | 2 | 4 |

Estimated total candidate inventory: 13–23 candidates.
Recommended initial scope: 15–18 candidates. This is large enough to explore meaningful variation while remaining auditable and aligned with the goal of diversity over brute-force count.

## SECTION 6 – Anti-Redundancy Controls

### Conceptual controls
- Do not accept themes defined as “repair,” “recovery,” “weakness correction,” or “post-stress stabilization.”
- Require a primary family axis of either cross-sectional dispersion structure or rank stability, not participation/volume repair.
- Reject candidate themes that are described as “participation repair under hostile trend” or “low extension liquidity repair.”

### Feature controls
- Dispersion themes must use dispersion or cross-sectional correlation features, not participation or volume metrics as primary inputs.
- Persistence themes must use explicit rank and stability measures, not raw participation or liquidity features.
- If a theme uses participation or liquidity inputs, they must be secondary and explicitly framed as stability or dispersion context, not the core signal.

### Conditioning controls
- Dispersion themes should condition on dispersion transitions and anomalies, not on stress/hostile state labels alone.
- Persistence themes should condition on rank behavior and regime transitions, not on stress recovery or low-breadth states.
- Do not require themes to use current hostile/stress state triggers unless the state is incidental to dispersion or rank behavior.

### Review controls
- Pre-launch review: confirm each theme is distinct from existing participation/breadth and volatility-stress candidates.
- Mid-batch redundancy review: evaluate candidate-level correlation and co-activation versus current library.
- Post-batch family-diversity review: assess whether any theme has produced a truly distinct family or is merely a variant.

## SECTION 7 – Validation Expectations

### A. Genuine new alpha family
- Evidence of low correlation (<0.15) and low co-activation with existing participation/stress candidates.
- A distinct regime or structural activation pattern not dominated by hostile/stress repair states.
- Robust horizon behavior with positive evidence at h10/h20 and stable persistence.
- A clear economic story tied to dispersion or rank stability.

### B. Variant of an existing family
- High correlation and co-activation with current candidates.
- Activation primarily in the same hostile/stress or weak-breadth states.
- Candidate behavior that can be explained as a renamed or reframed participation repair mechanism.

### C. Diagnostic-only result
- The theme yields useful structural or regime insights but no candidate with distinct or robust alpha evidence.
- Evidence is interesting for research context but insufficient for candidate advancement.
- The result is supported by distinct regime or dispersion observations without repeatable candidate metrics.

### D. Full rejection
- The theme cannot produce candidate evidence that is distinct from the existing library.
- The candidate results are negative or dominated by existing stress/repair patterns.
- The theme lacks horizon robustness and does not add research value beyond diagnostics.

## SECTION 8 – Discovery Governance Plan

### Discovery review checkpoint
- Pre-launch theme approval: senior research review of theme definitions, feature inputs, and redundancy controls.
- Mid-batch progress review: evaluate whether the batch is producing structurally distinct behavior and whether any theme should be pruned.

### Refinement eligibility criteria
- Candidate themes with preliminary positive evidence and low overlap to current candidates may proceed to a second refinement pass.
- Refinement is only eligible if a theme demonstrates distinct regime or structural evidence, not just moderate IC.

### Validation eligibility criteria
- Candidate themes should only move toward validation if they show distinctiveness on family axes, stable horizon behavior, and a defensible economic story.
- Validation eligibility requires a family-distinctness memo plus standard research metrics, not just threshold crossing.

### Family-diversity evaluation criteria
- Evaluate the batch by family axis, not by candidate count.
- Require evidence that at least one dispersion theme and one persistence theme have produced candidates with distinct activation patterns.
- Use family-level correlation and co-activation screens before concluding the batch.

## SECTION 9 – Risk Assessment

### Overfitting risk
- Medium. The batch is deliberately focused on new families, but dispersion and rank features can still overfit if too many variants are created.
- Mitigation: keep candidate count disciplined and require redundancy review.

### Family contamination risk
- Medium-high. Persistence themes may drift into participation repair and dispersion themes may drift into volatility compression.
- Mitigation: enforce the anti-redundancy controls and review feature/conditioning choices strictly.

### Horizon concentration risk
- Medium. The batch remains h10-h20 heavy, which is appropriate for the current project, but there is still risk of missing shorter-horizon differentiation.
- Mitigation: allow h5 exploratory tests as secondary checks within dispersion themes.

### Discovery sprawl risk
- Medium. The proposed batch is large enough to explore variation, but not so large that it becomes unmanageable.
- Mitigation: cap the total candidate inventory at 15–18 and use strict minimum/maximum counts per theme.

### False diversification risk
- High. The biggest danger is producing apparent new families that are actually variants of existing participation/stress repair.
- Mitigation: require early orthogonality screening and family-distinctness evidence before refinement.

## SECTION 10 – Final Recommendation

1. Which theme should be executed first?
- Dispersion Expansion Transition should be executed first because it is the most structurally distinct and the largest current gap.

2. Which theme has highest diversification potential?
- Dispersion Expansion Transition has the highest diversification potential, followed by Rank Stability After Drawdown.

3. Which theme has highest probability of failure?
- Dispersion Structure Anomalies has the highest probability of failure because it is more exploratory and could be difficult to separate from volatility/stress behavior.

4. What is the minimum acceptable outcome for this batch?
- The minimum acceptable outcome is one genuinely distinct new candidate family or a diagnostic result that proves the themes are not merely variants of existing participation/stress repair.

5. What should be the next Codex task after this specification is approved?
- The next task should be to write the operational discovery run plan for the first approved batch, including concrete feature lists, transformation candidates, and implementation-ready candidate generation protocols.

---

### Specification caveat
This document is a research specification only. No discovery execution, code changes, governance changes, threshold changes, or ML work were performed.
