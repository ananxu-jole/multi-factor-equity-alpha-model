# Alpha Family Diversification Refinement Design v1

Date: 2026-06-18

Project: Project Underdog

Scope: research-design only. This memo designs a small refinement program for the two diversification candidates that passed the IC discovery review. No refinement execution, validation, governance mutation, threshold change, candidate promotion/demotion, production registration, or ML implementation is performed or authorized.

Eligible candidates only:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`

## SECTION 1 - Executive Summary

The two candidates were selected because they are the only reviewed candidates that combine positive discovery IC evidence with low approved-subset redundancy.

`rank_stability_after_drawdown_02` / `post_drawdown_persistence_20` is the stronger raw candidate. It showed h5 mean IC 0.0137, h10 mean IC 0.0125, h10 IC IR 0.1208, h10 positive IC rate 0.5951, and low approved-subset redundancy with max absolute correlation 0.1815. It is the best individual result in the scored diversification subset.

`dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20` is the more distinct dispersion representative. It showed h5 mean IC 0.0099, h10 mean IC 0.0082, h10 IC IR 0.0933, h10 positive IC rate 0.5464, and very low approved-subset redundancy with max absolute correlation 0.0455. Its h20 evidence fades to roughly flat/slightly negative, so it should be treated as a short-to-medium horizon dispersion-transition candidate, not as proven h20 alpha.

The evidence supports refinement because the project needs alpha-family diversification away from the existing hostile/stress-repair concentration, and these two candidates offer the cleanest candidate-level evidence for the persistence and dispersion families. The evidence does not yet support family-level adoption: dispersion family averages were negative at h10 and h20, while persistence family averages were dragged down by the adverse `drawdown_rank_stability_20` result.

Refinement must avoid three major risks:
- Parameter mining: do not expand into a broad grid of windows, horizons, filters, and nonlinear transforms.
- False diversification: do not allow drawdown or dispersion logic to become a renamed hostile/stress-repair mechanism.
- Horizon chasing: do not force h20 improvement by repeatedly modifying the signal until a single horizon looks better.

The recommended program is intentionally small: 3-4 variants for Candidate A and 3-4 variants for Candidate B, with the original representatives retained as anchors. The goal is to determine whether the persistence and dispersion effects are robust, interpretable, and distinct enough to justify a later validation-design task.

## SECTION 2 - Candidate A Refinement Design

Candidate: `rank_stability_after_drawdown_02`

Representative signal: `post_drawdown_persistence_20`

### Economic Intuition

The economic hypothesis is that securities that preserve or improve cross-sectional rank stability after a drawdown are more durable than peers whose ranks churn or deteriorate. The desired effect is persistence after stress, not recovery from stress. The signal should reward stable relative quality of rank behavior after a drawdown event, rather than simply buying names that were recently damaged and then repaired.

### Current Strengths

- Strongest individual candidate in the discovery subset.
- Positive h5 and h10 evidence: h5 mean IC 0.0137 and h10 mean IC 0.0125.
- Strong positive-rate profile: h5 positive IC rate 0.5992 and h10 positive IC rate 0.5951.
- Low approved-subset redundancy: max approved-subset absolute correlation 0.1815.
- Cross-candidate diversification is favorable versus Candidate B: `post_drawdown_persistence_20` and `dispersion_transition_acceleration_20` had low pairwise panel correlation in the reviewed redundancy table.

### Current Weaknesses

- h20 evidence decays materially to mean IC 0.0059 and positive IC rate 0.5310.
- The broader persistence family was not strong at the family-average level.
- Drawdown conditioning creates contamination risk because it may accidentally recreate hostile/stress-repair behavior.
- The useful effect may be concentrated in h5-h10 rather than h10-h20.
- Active coverage and date concentration still need diagnostic inspection before any validation decision.

### Refinement Objectives

The refinement objective is to test whether the candidate is a robust persistence/rank-stability effect, not to maximize IC.

Specific objectives:
- Preserve the post-drawdown rank-stability economic story.
- Confirm sign orientation: persistence should be rewarded, not delayed reversal or damaged-name recovery.
- Test whether h5/h10 evidence remains stable under small, pre-specified formula changes.
- Evaluate whether h20 decay is tolerable, structural, or a warning sign.
- Check active coverage and concentration by date, ticker, and drawdown state.
- Confirm distinctiveness against approved subset candidates and existing hostile/stress-repair inventory in a later review step.

### Small Refinement Space

The refinement space should be limited to 3-4 research variants plus the original representative.

What may vary:
- Rank-stability measurement: one alternative rank-churn definition and one alternative rank-persistence definition.
- Drawdown context strictness: one modestly looser and/or one modestly stricter post-drawdown eligibility definition, if both are pre-specified.
- Stabilization of the rank signal: one light smoothing or clipping choice designed to reduce rank-noise sensitivity.
- Observation window alignment: one small adjustment around the existing post-drawdown observation window, only if it preserves the same h10-h20 declared research horizon.

What must remain fixed:
- Family: persistence / rank stability.
- Theme: Rank Stability After Drawdown.
- Core signal identity: post-drawdown rank persistence, not stress repair, rebound strength, volume repair, or liquidity repair.
- Primary research horizon orientation: h10-h20, with h5 allowed only as a secondary diagnostic because existing evidence is strongest at h5/h10.
- Directional thesis: stable/improving ranks after drawdown should be favorable.
- Research-only status.

Candidate count range:
- Minimum: 3 variants plus original anchor.
- Maximum: 4 variants plus original anchor.

Expected refinement outputs:
- A variant design table with formula intent, fixed components, varied component, and expected failure mode.
- A sign-orientation diagnostic plan.
- A coverage and concentration diagnostic plan.
- A horizon-concentration diagnostic plan covering h5, h10, and h20.
- A redundancy-review plan versus both the diversification subset and hostile/stress-repair inventory.
- A recommendation class for each variant after future execution: continue to validation design, additional refinement, diagnostic-only, or reject.

Broad parameter expansion is explicitly prohibited. The design must not create a grid over many drawdown thresholds, rank windows, smoothing windows, horizons, sector neutralization choices, or nonlinear transforms. The allowed variants should each answer a named diagnostic question.

## SECTION 3 - Candidate B Refinement Design

Candidate: `dispersion_expansion_transition_04`

Representative signal: `dispersion_transition_acceleration_20`

### Economic Intuition

The economic hypothesis is that securities positioned favorably during an acceleration in cross-sectional dispersion can outperform as the market reorganizes. The desired effect is early leadership or resilience during dispersion expansion, not panic response, volatility compression, or broad stress repair. The candidate should identify useful transition behavior when security-level return dispersion is widening in a structured way.

### Current Strengths

- Best dispersion candidate after redundancy-adjusted IC review.
- Positive h5 and h10 evidence: h5 mean IC 0.0099 and h10 mean IC 0.0082.
- Positive h10 rate of 0.5464, which is modest but directionally useful.
- Very low approved-subset redundancy: max approved-subset absolute correlation 0.0455.
- Strong conceptual fit with the diversification objective because it is built on dispersion transition behavior rather than participation, liquidity, or breadth repair.

### Current Weaknesses

- IC evidence is weaker than Candidate A.
- h20 evidence fades to -0.0007, so the candidate does not currently establish a durable h20 dispersion effect.
- Dispersion acceleration can be noisy and may overreact to transient cross-sectional volatility spikes.
- The broader dispersion family had negative h10 and h20 family-average IC.
- It has a notable inverse relation to `dispersion_expansion_leadership_20` in the broader panel review, which should be understood before any family-level conclusion.

### Refinement Objectives

The refinement objective is to test whether the candidate is a genuine dispersion-transition alpha, not to force an h20 result.

Specific objectives:
- Preserve the dispersion-expansion-transition economic story.
- Stabilize noisy acceleration measurement without masking the transition effect.
- Determine whether h10 evidence remains positive under small, pre-specified variants.
- Diagnose whether h20 decay reflects true effect horizon, noise, or formula fragility.
- Confirm the signal does not become volatility-compression, panic, or hostile/stress repair.
- Preserve very low redundancy as a core reason for considering the candidate.

### Small Refinement Space

The refinement space should be limited to 3-4 research variants plus the original representative.

What may vary:
- Acceleration measurement: one alternative first-difference or second-difference construction of dispersion transition.
- Noise control: one light smoothing, winsorization, or clipping variant.
- Transition-state definition: one modestly narrower or broader rising-dispersion state definition.
- Leadership/ranking layer: one variant that separates dispersion acceleration from raw high-dispersion exposure.

What must remain fixed:
- Family: dispersion.
- Theme: Dispersion Expansion Transition.
- Core signal identity: dispersion-transition acceleration.
- Primary research horizon orientation: h10-h20, with h5 allowed only as a secondary diagnostic.
- Prohibition on direct stress, hostile, liquidity-repair, participation-repair, or breadth-repair triggers.
- Research-only status.

Candidate count range:
- Minimum: 3 variants plus original anchor.
- Maximum: 4 variants plus original anchor.

Expected refinement outputs:
- A variant design table with transition definition, dispersion input, noise control, and expected diagnostic purpose.
- A horizon-concentration diagnostic plan for h5/h10/h20.
- A transition-state activation diagnostic plan.
- A redundancy-review plan against dispersion peers, persistence peers, and hostile/stress-repair candidates.
- A family-distinctness assessment template comparing dispersion-transition behavior with volatility compression and stress-repair behavior.

Broad parameter expansion is explicitly prohibited. The design must not sweep many lookbacks, dispersion definitions, transition thresholds, smoothing windows, sector groupings, or horizon targets. Variants must be sparse, interpretable, and tied to named failure modes.

## SECTION 4 - Anti-Optimization Controls

Maximum refinement scope:
- Total eligible candidates: 2.
- Total new research variants: 6-8 across both candidates.
- Maximum variants for Candidate A: 4 plus original anchor.
- Maximum variants for Candidate B: 4 plus original anchor.
- No additional families, themes, or candidates may be added to this refinement batch.

Safeguards against parameter mining:
- Every variant must have a written diagnostic purpose before execution.
- No grid search over lookbacks, thresholds, smoothing parameters, clipping bounds, or horizons.
- No variant should be kept merely because it improves one metric.
- The original representative must remain in the comparison set as the anchor.

Safeguards against horizon chasing:
- h10 remains the primary review horizon for both candidates because current evidence is strongest at h5/h10 and declared research orientation is h10-h20.
- h20 may be diagnosed, but not optimized into existence.
- h5 may be used only to understand short-to-medium concentration, not to redefine the candidates as short-horizon alphas.

Safeguards against overfitting:
- Prefer one-change variants over compound variants.
- Require consistent sign, positive-rate behavior, and coverage stability, not only improved mean IC.
- Require variant-level explanation before any future scoring.
- Treat narrow date/ticker concentration as a warning even if mean IC improves.

Safeguards against family contamination:
- Persistence variants must remain rank-stability variants, not participation, liquidity, breadth, or rebound variants.
- Dispersion variants must remain dispersion-transition variants, not volatility-compression or panic-response variants.
- Any variant whose activation is dominated by hostile/stress-repair states should be classified as diagnostic-only or rejected.

Safeguards against recreating hostile/stress-repair behavior:
- Do not add hostile-state labels, stress-state labels, weak-breadth triggers, liquidity-repair inputs, or participation-repair inputs.
- Do not select damaged securities because they are recovering.
- Do not reward simple post-stress normalization unless the rank-stability or dispersion-transition mechanism remains primary.
- Require a later redundancy check versus the existing hostile/stress-repair inventory before any validation-design step.

Prohibited modifications:
- No governance or threshold changes.
- No production registration.
- No validation execution.
- No ML.
- No promotion or demotion language.
- No broad candidate generation outside the two eligible candidates.
- No new family definitions.
- No conversion of either candidate into a portfolio construction or risk model feature.

Review checkpoints:
- Pre-refinement design review: confirm every proposed variant has one diagnostic purpose and remains inside family scope.
- Post-generation artifact review: confirm panels, metadata, and formulas match the approved design before any scoring interpretation.
- Post-discovery scoring review: evaluate robustness, consistency, distinctiveness, coverage, and contamination risk.
- Pre-validation-design review: decide whether any candidate has earned a validation-design task. This is a research workflow checkpoint, not a governance gate.

## SECTION 5 - Refinement Success Criteria

Continuation to validation design would be justified only if a candidate shows:
- Robustness: positive or near-positive behavior is not isolated to one fragile variant, date cluster, or ticker subset.
- Consistency: sign orientation and positive-rate behavior remain coherent across h5/h10/h20 diagnostics, with h10 remaining credible.
- Distinctiveness: redundancy remains low versus the diversification subset and acceptable versus hostile/stress-repair inventory.
- Economic clarity: the result still reads as persistence or dispersion, not as repaired stress exposure.
- Coverage quality: active coverage is adequate and not dominated by sparse post-event observations.

Additional refinement would be justified if:
- The original candidate remains interesting but one failure mode is unresolved.
- Variants disagree in an interpretable way that points to a narrow diagnostic follow-up.
- Distinctiveness remains strong but horizon behavior is ambiguous.
- Coverage diagnostics reveal fixable construction issues without requiring broad parameter search.

Diagnostic-only classification would be appropriate if:
- The candidate provides useful structural evidence about persistence or dispersion but lacks robust IC support.
- The signal remains distinct but too weak or horizon-limited for validation design.
- Results explain why a family axis may matter without producing a credible candidate.

Rejection would be appropriate if:
- Positive discovery evidence disappears under small pre-specified variants.
- IC or positive-rate behavior is concentrated in one date regime or small active subset.
- Redundancy rises materially or the candidate maps onto hostile/stress-repair behavior.
- The economic story requires post hoc explanation after scoring.
- Improving the candidate would require broad parameter expansion or horizon chasing.

Raw IC alone is not sufficient. A higher-IC variant with worse redundancy, weaker coverage, unclear sign orientation, or stress-repair contamination should not be considered a successful refinement outcome.

## SECTION 6 - Diversification Impact Assessment

Does Candidate A appear to strengthen the persistence family?

Yes, but only at the candidate level. `post_drawdown_persistence_20` is the best evidence that persistence/rank stability can contribute to the alpha library. It does not yet rescue the full persistence family, because the family-average result is weak and another rank-stability candidate was materially adverse. Successful refinement would strengthen the persistence family by showing that post-drawdown rank persistence is robust and not just a single formula artifact.

Does Candidate B appear to strengthen the dispersion family?

Yes, modestly and mainly through distinctiveness. `dispersion_transition_acceleration_20` is the best dispersion candidate because it combines modest h5/h10 IC with extremely low approved-subset redundancy. It does not yet prove that dispersion is a strong family. Successful refinement would strengthen the dispersion family if it preserves low redundancy while improving confidence that the h10 effect is stable and economically tied to dispersion transitions.

Would successful refinement meaningfully improve alpha-family diversity?

Yes. If both candidates survive small refinement, Project Underdog would have evidence for two research axes outside the dominant hostile/stress-repair family: post-drawdown rank persistence and dispersion-transition acceleration. Even one successful candidate would improve diversity if it remains low-redundancy and economically distinct. Two successful candidates would provide a stronger basis for a later family-distinctness and validation-design task.

## SECTION 7 - Recommended Refinement Batch

Recommended order:
1. Refine Candidate A first: `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`.
2. Refine Candidate B second: `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`.

Rationale:
- Candidate A has the stronger raw discovery evidence and the clearest h5/h10 positive-rate profile.
- Candidate B has higher structural distinctiveness but weaker and more horizon-limited evidence.
- Running Candidate A first tests whether the best observed candidate can survive contamination and robustness review before the more fragile dispersion candidate is expanded.

Candidate counts:
- Candidate A: 3-4 variants plus original anchor.
- Candidate B: 3-4 variants plus original anchor.
- Total batch: 6-8 new variants plus 2 original anchors.

Expected artifacts:
- Refinement variant specification memo.
- Candidate variant metadata table.
- Formula-intent and fixed-vs-varied component table.
- Planned diagnostic checklist for sign orientation, active coverage, horizon concentration, and redundancy.
- Future scoring manifest limited to these variants and anchors.

Expected review outputs after future execution:
- Candidate-level refinement review for Candidate A.
- Candidate-level refinement review for Candidate B.
- Cross-candidate diversification and redundancy memo.
- Family-distinctness recommendation: validation-design eligible, further-refinement eligible, diagnostic-only, or reject.

The batch should remain intentionally small. The correct outcome is not a large set of tuned variants; it is a clear answer about whether persistence and dispersion are genuine diversification families worth testing further.

## SECTION 8 - Final Recommendation

1. Which candidate should be refined first?

`rank_stability_after_drawdown_02` / `post_drawdown_persistence_20` should be refined first because it has the strongest discovery evidence: h10 mean IC 0.0125, h10 positive IC rate 0.5951, and low approved-subset redundancy.

2. Which candidate has higher diversification value?

`dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20` has higher pure diversification value because its approved-subset redundancy is extremely low and its economic axis is most distinct from the existing hostile/stress-repair concentration. Candidate A has stronger alpha evidence; Candidate B has stronger family-diversification value.

3. Which candidate has higher failure risk?

`dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20` has higher failure risk because its effect is weaker, h20 fades to slightly negative, and dispersion acceleration can be noisy. Candidate A's main failure risk is contamination by stress-repair behavior, but its raw h5/h10 evidence is stronger.

4. What is the minimum acceptable refinement outcome?

The minimum acceptable outcome is one candidate that remains economically interpretable, low-redundancy, robust enough across small pre-specified variants, and free of hostile/stress-repair contamination. If neither candidate meets that standard, the batch should still produce a diagnostic-only conclusion explaining why persistence and dispersion did or did not represent genuinely new alpha-family axes.

5. What should the next Codex task be after this design is reviewed?

The next Codex task should be to create the research-only refinement variant specification for the two approved candidates, including exact variant definitions, metadata fields, diagnostic checklists, and artifact paths. That task should still avoid validation, governance mutation, threshold changes, production registration, ML, and promotion/demotion decisions.

## Research Caveat

This memo is a refinement design only. It does not execute refinement, run validation, change governance, modify thresholds, promote or demote candidates, register production artifacts, or implement ML.
