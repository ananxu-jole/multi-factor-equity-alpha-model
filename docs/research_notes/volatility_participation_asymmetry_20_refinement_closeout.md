# Volatility Participation Asymmetry 20 Refinement Closeout

Date: 2026-05-22

Source refinement run: `volatility_participation_asymmetry_20_refinement_v1`

Final status: `CONDITIONAL_ONLY_RESEARCH`

## Refinement Objective

The refinement pass tested whether `volatility_participation_asymmetry_20` could become more selective without losing the behavior that made it the only live candidate from `structural_interaction_alpha_discovery_batch_v1`: positive h20 behavior, modest h10 support, stable WFV diagnostics, true interaction structure, low inventory overlap, and low reversal/momentum similarity.

This was a filter/refinement pass only, not a redesign or promotion step.

## Variants Tested

- `volatility_participation_asymmetry_20_original`
- `volatility_participation_asymmetry_20_participation_q60`
- `volatility_participation_asymmetry_20_vol_stab_q60`
- `volatility_participation_asymmetry_20_dual_q55`
- `volatility_participation_asymmetry_20_dual_close_q55`
- `volatility_participation_asymmetry_20_balanced_selective_q60`
- `volatility_participation_asymmetry_20_rebalance_20_dual_q55`

## Best Retained Behavior

The original formulation remained the strongest version:

- h10 mean IC: `0.005843`
- h20 mean IC: `0.012154`
- h20 positive IC rate: `0.585233`
- WFV behavior stayed stable in the refinement pass.
- Interaction label remained `true_interaction_behavior`.
- Max inventory correlation remained low at `0.052717`.
- Reversal and momentum overlap remained low.

## Why No Variant Advanced

No refined variant improved activation while preserving the original interaction behavior.

Participation tightening reduced raw filter coverage, but h20 weakened to `0.008490` and the interaction diagnostic collapsed into `single_component_ic_dominates`.

Dual confirmation filters became too sparse and weak. The dual q55 variants had very low material raw activation coverage and did not preserve h10 or h20 behavior.

Volatility-only confirmation did not preserve predictive behavior. Its best horizon shifted to h1 with negative best-horizon IC.

Balanced selectivity preserved some h20 support, but it did not preserve true interaction behavior and remained below refinement quality.

## Key Lesson

The current edge appears to require the broader interaction among volatility stabilization, participation asymmetry, close support, and low extension. Tightening around a single component damaged the interaction structure rather than cleanly improving activation quality.

This suggests the idea is not dead, but the current activation definition is brittle. Further progress should come from a redesigned activation thesis, not repeated threshold tightening on this exact formulation.

## Decision

Park the current formulation as research evidence.

Do not refine this exact version again immediately. Revisit only through a future redesign that changes the activation definition while preserving the interaction thesis.

Do not advance to conditional validation.

## Intentional Non-Changes

- No production registration.
- No survivor/watchlist mutation.
- No detector code or label changes.
- No gate/schema/governance changes.
- No portfolio, ML, blending, or optimization routing.
