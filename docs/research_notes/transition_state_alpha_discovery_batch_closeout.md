# Transition-State Alpha Discovery Batch Closeout

Date: 2026-05-21

Status: RESEARCH_CLOSEOUT

## Summary

The Transition-State Alpha Discovery Batch tested 10 simple, interpretable candidate structures focused on identifying when short-horizon stress, volatility, or dislocation is absorbed rather than propagated.

Final batch result: no viable alpha candidate was found.

All 10 candidates were classified as `REJECT_RESEARCH`:

- `volatility_spike_decay_absorption_5_10`
- `range_expansion_to_containment_5_10`
- `shock_return_normalization_5_10`
- `liquidity_recovery_after_vol_shock_5_10`
- `volume_shock_exhaustion_stabilization_5_10`
- `participation_repair_after_instability_5_10`
- `dispersion_spike_normalization_5_10`
- `breadth_stabilization_after_panic_diffusion_5_10`
- `shock_absorption_vs_propagation_quality_5_10`
- `instability_resolution_to_stabilization_5_10`

The transition-state hypothesis is not dead, but this first simple implementation did not find a standalone tradable candidate. The strongest partial evidence came from `volatility_spike_decay_absorption_5_10`, but its h5 and h10 ICs were too weak to justify refinement.

## Interpretation

The negative result suggests that transition-state behavior may be too broad, noisy, or context-dependent to express as a single standalone alpha signal in this formulation.

The more useful next framing is not:

> Can one transition-state signal directly become an alpha?

It is:

> Can a composite transition-state detector identify market contexts where other alphas should be interpreted differently?

This shifts the research objective from alpha discovery to state/context detection.

## Pivot

Recommended next direction: design a `Transition-State Composite Detector`.

Purpose: build a research-only state label/context layer that combines:

- volatility shock
- liquidity recovery
- dispersion normalization
- breadth stabilization
- propagation versus absorption flags

The detector should not be treated as a tradable alpha. Its intended role is to become a future conditioning layer for alpha diagnostics, monitoring, and candidate interpretation.

## Guardrails

No candidate from the Transition-State Alpha Discovery Batch should be promoted, registered, added to survivor/watchlist, routed into portfolio/ML/blending logic, or used to change gates, schemas, thresholds, or validation logic.

Do not spend another immediate cycle refining the 10 rejected standalone structures. Any next work should be design-only or detector-focused, with explicit research-only scope.
