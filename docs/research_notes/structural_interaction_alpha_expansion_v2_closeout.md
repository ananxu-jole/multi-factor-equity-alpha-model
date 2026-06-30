# Structural Interaction Alpha Expansion v2 Closeout

Date: 2026-05-22
Run id: `structural_interaction_alpha_expansion_v2`
Final status: `CLOSED_WEAK_RESEARCH`

## Batch Objective

`structural_interaction_alpha_expansion_v2` tested whether smoother, less brittle structural interaction formulations could improve on the earlier `volatility_participation_asymmetry_20` evidence. The batch deliberately avoided harder threshold tuning and focused on continuous scores, interaction persistence, component balance, and medium-horizon h10/h20 behavior.

## Candidates Tested

1. `relative_participation_quality_instability_adjusted_20`
2. `asymmetric_stabilization_balance_20`
3. `structural_recovery_efficiency_15_20`
4. `dispersion_constrained_recovery_quality_20`
5. `participation_persistence_quality_20`
6. `volatility_structure_curvature_stabilization_20`
7. `liquidity_adjusted_volatility_normalization_20`
8. `moderate_interaction_persistence_score_20`

## Classification Outcome

- `CONDITIONAL_ONLY_RESEARCH`: 1
- `REJECT_RESEARCH`: 7
- `CONDITIONAL_REFINEMENT_CANDIDATE`: 0
- `CANDIDATE_FOR_CONDITIONAL_VALIDATION`: 0

No candidate advanced to refinement or conditional validation.

## Best Weak Clue

The only retained research clue was `volatility_structure_curvature_stabilization_20`.

- h10 mean IC: `0.003114`
- h20 mean IC: `0.006066`
- h20 positive IC rate: `0.576313`
- WFV persistence/sign consistency: `1.00 / 1.00`
- Interaction behavior: `true_interaction_behavior`
- Interaction persistence: supported
- Inventory, reversal, and momentum overlap: low

This was structurally cleaner than most rejected candidates, but the standalone predictive signal was too weak and activation remained too broad. It is not refinement-ready or validation-ready.

## Why Nothing Advanced

The batch improved one failure mode from prior work: smoother interaction logic reduced activation brittleness and avoided some single-threshold collapse. However, that did not translate into enough medium-horizon alpha strength.

Most candidates either had weak h10/h20 IC, broad undifferentiated activation, insufficient positive-rate support, or no compelling evidence that the interaction added tradable structure beyond a clean research pattern. Component balance was generally not the primary problem; the stronger issue was that balanced interactions still lacked standalone predictive power.

## Key Lesson

Smoother interaction design helped brittleness, but not standalone predictive strength. The useful evidence is methodological: true interaction behavior can be preserved without hard threshold escalation, but the current structural-interaction family does not yet produce robust enough medium-horizon candidates.

## Decision

Park structural-interaction refinement for now.

Do not refine `volatility_structure_curvature_stabilization_20` immediately. Do not run another structural-interaction expansion immediately. Treat this branch as weak research evidence and pivot to a genuinely different alpha family.

## Intentional Non-Changes

- No detector changes.
- No production registration.
- No survivor/watchlist mutation.
- No validation, gate, schema, or governance changes.
- No portfolio, ML, blending, or optimization routing.

## Recommended Next Research Direction

The next alpha family should move away from transition-state micro-signals and broad structural-interaction composites. The most promising next direction is a sector-relative or peer-relative residual/relative-value redesign.

Rationale:

- It is structurally different from recent failed or weak paths.
- It can test medium-horizon cross-sectional behavior without relying on hostile/stress repair or short-horizon shock absorption.
- It can separate company-relative behavior from broad market and sector moves.
- It can include explicit anti-momentum and anti-reversal diagnostics.
- It may produce broader, more stable active coverage than transition-state slices.

Before implementation, the next step should be a small design/inspection pass to confirm whether sector, industry, or other peer-group metadata is available in the existing research data. If peer metadata is available, prioritize sector-relative residual resilience, residual exhaustion, and peer-relative stabilization concepts. If not, fall back to market-relative or volatility-bucket-relative residual designs, or document a data enrichment requirement.
