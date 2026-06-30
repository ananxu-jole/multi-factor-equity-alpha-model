# Alpha Family Diversification Discovery Program Design v1

Date: 2026-06-17

## SECTION 1 – Strategic Objective

Project Underdog needs alpha-family diversification before metadata-enriched research, ML modeling, or portfolio-level construction because the current library is concentrated in a narrow conditional hostile/stress repair family with limited horizon and regime diversification. A deliberately designed discovery program should establish structurally distinct families first, so that future metadata or ML work is built on truly orthogonal sources rather than a deeper exploration of the same underlying edge.

Key strategic reasons:
- Avoid overfitting to the current conditional repair regime.
- Prevent metadata and ML from being applied to a library that is not yet structurally diverse.
- Build a clean research frontier around new economic intuitions rather than extend the current participation/stress cluster.
- Create a stronger foundation for future construction by finding candidates with different horizons, different state dependencies, and lower pairwise redundancy.

This program is research-design only: it is meant to define the next structured discovery phase without generating signals, changing thresholds, or modifying governance or code.

## SECTION 2 – Target Family A: Dispersion Behavior

### Economic intuition
Dispersion alpha seeks opportunities where cross-sectional differences widen or compress in ways that signal future relative performance. It is based on the idea that when dispersion behavior changes, the market is reorganizing and some securities are likely to outperform while others underperform.

### Why it is distinct from hostile/stress repair
- Hostile/stress repair is primarily about recovery inside a weak or stressed regime.
- Dispersion behavior is about cross-sectional structure and market differentiation, not just a return to stability after stress.
- Dispersion candidates can work in both stressed and neutral regimes, depending on whether dispersion is expanding or compressing.

### Expected market conditions where it may matter
- Periods of rising or falling cross-sectional dispersion.
- Regime shifts where dispersion transitions from low to high or high to low.
- Environments where market internals diverge from broad index behavior.

### Expected horizon behavior
- Medium-term, with a likely focus at h10-h20 but with scope for h5/h10 if dispersion transitions are sharp.
- Unlike the current library, a dispersion family can also include shorter reaction horizons if the dispersion shift is rapid.

### Possible signal ingredients already available
- Cross-sectional return dispersion metrics.
- Realized volatility dispersion.
- Breadth dispersion proxies.
- Dispersion of participation or volume metrics.
- Cross-sectional rank variance and cross-sectional volatility of candidate scores.

### Risks of accidentally recreating existing stress-repair candidates
- Using dispersion measures conditioned solely on stress states can drift back into stress repair.
- Designing a dispersion theme around low-dispersion recovery can overlap with the current `participation_breadth_repair_under_hostile_trend` family.
- To avoid this, the family should emphasize cross-sectional structural change rather than simple stress normalization.

## SECTION 3 – Target Family B: Persistence / Rank Stability Behavior

### Economic intuition
Persistence / rank stability alpha is based on the idea that securities with stable, improving rank behavior after a disruption may be more durable winners than those with noisy rank trajectories. This family rewards structural stability rather than state repair.

### Why it is distinct from hostile/stress repair
- Hostile/stress repair is defined by regime or state activation.
- Persistence/rank stability is defined by the internal dynamics of a security’s cross-sectional rank movement and its consistency over time.
- It is about stability in the signal/market structure, not about the market being weak or stressed.

### Expected market conditions where it may matter
- Periods following drawdowns or regime changes where rank coherence improves.
- Situations where market leadership is uncertain but some securities show stable cross-sectional ordering.
- Environments where turnover and rank churn are informative about future relative performance.

### Expected horizon behavior
- Medium-term to longer-term, likely h10-h20, with an emphasis on sustained behavior rather than transient spikes.
- Could also include shorter h5/h10 tests for early rank stabilization signals, but the core family is about longer structural persistence.

### Possible signal ingredients already available
- Cross-sectional rank histories.
- Rank churn and turnover proxies.
- Stability of rank changes over multiple windows.
- Longitudinal consistency of signal scores or active exposure.
- Comparison of recent rank stability to prior volatility in rank.

### Risks of accidentally recreating existing participation/breadth repair candidates
- If the persistence family is defined using the same hostile/stress states, it may become a variant of participation repair.
- If it uses participation/volume metrics as stability inputs, it may overlap with the existing liquidity/participation family.
- To avoid this, the family should use explicit rank and stability metrics rather than state-activated participation repair.

## SECTION 4 – Discovery Theme Candidates

### Theme 1: Dispersion Expansion Transition
- Target alpha family: Dispersion behavior.
- Economic hypothesis: securities that lead a widening cross-sectional dispersion phase outperform because they capture early differentiation when the market is reorganizing.
- Expected uniqueness versus current library: high. It focuses on dispersion shifts rather than conditional recovery.
- Required base features: return dispersion, cross-sectional variance, volatility dispersion, rank breadth measures.
- Likely horizon focus: h10-h20.
- Expected failure modes: signal may behave like stressed regime repair if dispersion expansion is driven by market panic; it may also overfit to temporary noise in cross-sectional volatility.
- Why it is worth testing: it addresses a large gap in the current library and uses structurally different information.

### Theme 2: Dispersion Compression Reversal
- Target alpha family: Dispersion behavior.
- Economic hypothesis: securities that benefit from dispersion compression after a high-dispersion period are those that stabilize earlier than peers.
- Expected uniqueness versus current library: medium-high. It is related to volatility stabilization but emphasizes a different cross-sectional mechanism.
- Required base features: dispersion trend, pairwise co-movement compressions, cross-sectional volatility of returns.
- Likely horizon focus: h10-h20.
- Expected failure modes: may overlap with volatility compression after stress or become a disguised stress-repair signal if it is tied too closely to recovery regimes.
- Why it is worth testing: it explores the opposite side of dispersion transitions and may reveal a new alpha path.

### Theme 3: Rank Stability After Drawdown
- Target alpha family: Persistence / rank stability.
- Economic hypothesis: securities that maintain or improve cross-sectional rank stability after a drawdown are more likely to continue outperforming than those with volatile rank paths.
- Expected uniqueness versus current library: high. It focuses on internal rank dynamics, not on state repair or breadth.
- Required base features: rank churn, rank persistence, active coverage, drawdown history.
- Likely horizon focus: h10-h20.
- Expected failure modes: may simply select low-turnover securities that are already large-cap or stable, reducing alpha if not normalized.
- Why it is worth testing: it targets low-turnover, structural alpha and is a direct alternative to the current repair-heavy library.

### Theme 4: Rank Coherence Regime Transition
- Target alpha family: Persistence / rank stability.
- Economic hypothesis: securities that exhibit improved rank coherence during broader regime transitions are likely to benefit from the new regime.
- Expected uniqueness versus current library: high. It is regime-aware but not primarily stress-focused.
- Required base features: rank coherence measures, regime transition markers, cross-sectional rank dispersion.
- Likely horizon focus: h10-h20.
- Expected failure modes: may collapse into stress-repair if regime transitions are defined by hostile/stress exit only.
- Why it is worth testing: it uses a different axis of regime change and can diversify the library beyond stress repair.

### Theme 5: Participation Stability / Low-Churn Leadership
- Target alpha family: Persistence / rank stability.
- Economic hypothesis: securities with stable participation metrics and low rank churn form a distinct leadership subset that can outperform when the market stops re-pricing aggressively.
- Expected uniqueness versus current library: medium. It leverages participation but through a persistence lens rather than repair lens.
- Required base features: participation metrics, rank churn measures, turnover proxies, stability measures.
- Likely horizon focus: h10-h20.
- Expected failure modes: may blur into existing participation repair if the same participation signals are used without a clear stability definition.
- Why it is worth testing: it bridges participation data with persistence logic in a way that could produce a new family if designed carefully.

## SECTION 5 – Guardrails Against Redundancy

### Conceptual guardrails
- Do not define new themes primarily as “repair” or “recovery” from a weak/stress regime.
- Require each theme to have a distinct core axis: dispersion structure or rank stability, not participation improvement.
- Avoid themes that are framed as “repair under hostile trend” or “weak breadth stabilization”.
- Require the candidate family hypothesis to specify whether it is about cross-sectional structure, rank coherence, or regime transition, rather than state-based alpha.

### Statistical guardrails
- Require pairwise correlation and co-activation checks versus `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend` before accepting a theme as distinct.
- Reject theme variants if they show high correlation (>0.15) and high co-activation (>0.30) with the current participation/stress candidates.
- Require a minimum orthogonality test across dispersion and rank stability dimensions, not only within the new theme.

### Explicit redundancy checks
- If a proposed theme uses participation or liquidity metrics, ensure the signal construction is not simply a state-activated participation repair proxy.
- If a proposed theme uses volatility or dispersion, ensure it is not a restatement of `volatility_compression_after_stress_stabilization` by focusing on cross-sectional dispersion rather than stress exit.
- For persistence themes, require the primary ingredient to be rank stability or churn reduction, not low turnover alone.

## SECTION 6 – Success Criteria

### Useful result for a new family
- The theme produces a candidate or candidates with evidence that is meaningfully distinct from the current library on at least two axes: regime activation, horizon, or structural feature.
- The candidate demonstrates positive h20 (or alternate horizon) evidence with an IC profile and persistence pattern that is not dominated by hostile/stress repair states.
- The candidate passes a first-order redundancy screen versus existing participation/stress candidates.

### Evidence required to reject a family
- Proposed candidate behavior collapses into existing candidates in correlation/co-activation tests.
- The family’s best candidate cannot show meaningful distinctness in regime or feature space relative to the current library.
- The family’s signals are only strong when conditioned on the same hostile/stress states already covered.

### Evidence required to classify a theme as diagnostic-only
- The theme produces interesting regime or state diagnostics but fails to generate candidate-level evidence that is distinct and repeatable.
- It offers useful failure-mode insight without a practical candidate pathway.
- It has low horizon robustness and/or low active coverage.

### Minimum distinctiveness evidence versus existing candidates
- At least one of the following:
  - Lower pairwise correlation (<0.15) to the current participation/stress candidates.
  - Distinct regime activation not dominated by hostile/stress states.
  - A different horizon signature (e.g. a stronger h10 signal when the current library is h20-heavy).
- If a theme cannot deliver one of these, it should be treated as a variant rather than a new family.

## SECTION 7 – Recommended First Discovery Batch

### First batch themes
1. Dispersion Expansion Transition
2. Dispersion Compression Reversal
3. Rank Stability After Drawdown
4. Rank Coherence Regime Transition
5. Participation Stability / Low-Churn Leadership

### Preferred execution order
1. Dispersion Expansion Transition
2. Rank Stability After Drawdown
3. Dispersion Compression Reversal
4. Rank Coherence Regime Transition
5. Participation Stability / Low-Churn Leadership

### Reason for prioritization
- Start with the most structurally distinct families: dispersion first, then persistence.
- Begin with the broadest gap (dispersion) and then test a stability family to broaden beyond state repair.
- Reserve participation-stability themes for later in the batch to ensure they are not accidentally defined as existing repair variants.

### Expected artifacts
- Research design note for each theme with hypothesis, base features, and failure-mode guardrails.
- Candidate theme summary tables comparing regime activation, horizon focus, and expected orthogonality.
- Redundancy screening checklist and initial orthogonality plan.
- A batch-level decision memo documenting why each theme was selected and what structural gap it is intended to fill.

### Expected governance checkpoints
- Design approval checkpoint before the first discovery batch is launched.
- Pre-discovery redundancy review to confirm each theme is distinct from existing candidates.
- Post-batch evaluation checkpoint to decide whether the results warrant continuation, refinement, or archive.
- Metadata boundary confirmation checkpoint to ensure no metadata-enriched work enters this discovery phase.

## SECTION 8 – Final Recommendation

1. Should dispersion or persistence be tested first?
- Dispersion should be tested first because it is the largest current gap and is structurally most distinct from the current hostile/stress repair family.

2. Should both be tested in the same batch or separate batches?
- Both can be tested in the same batch if the batch remains small and disciplined, but they should be executed as separate theme tracks within that batch to preserve clarity.
- A combined batch is acceptable if the themes are clearly partitioned into dispersion and persistence tracks.

3. What is the biggest redundancy risk?
- The biggest redundancy risk is accidentally recreating participation repair in the persistence theme, or recasting volatility compression as dispersion compression.
- The primary guardrail is to enforce distinct core axes: cross-sectional dispersion versus rank stability.

4. What evidence would justify moving to metadata-enriched research later?
- A successful diversification program that produces at least one distinct dispersion family and one distinct persistence family with orthogonal regime or horizon behavior.
- Clear evidence that the candidate library is no longer dominated by hostile/stress repair and has at least one structurally independent alpha family.
- A documented redundancy screen showing low correlation and low co-activation between the new families and the current library.

5. What is the next Codex task after this design document is complete?
- The next task is to write the discovery run design note and candidate theme specification file for the first batch, including concrete theme definitions, feature lists, and redundancy screening protocols.

---

### Design caveat
This document is a research design artifact only. No discovery runs, signal generation, code changes, governance changes, threshold changes, or ML modeling were performed.
