# Conditional Construction Semantics Design

## Objective

This note defines research-only Conditional Construction Semantics for Project Underdog's Conditional-Alpha Framework.

The core question is:

> How should contextual or conditional information modify alpha behavior?

This is not a promotion proposal and not a production implementation plan. It does not change production code, schemas, gates, thresholds, survivor lists, portfolio construction, notebooks, validation logic, or ML layers.

The immediate design case is:

- `smooth_trend_persistence_60_low_breadth`

Recent diagnostics classify LOW_BREADTH as a `context filter`, not a standalone conditional alpha or survivor component. The purpose of this note is to define how context filters should be represented, tested, and eventually integrated if future evidence supports doing so.

## 1. Conditional Construction Semantics

Conditional components can play several operational roles. These roles should be explicitly labeled before construction because each role implies different behavior, risks, and diagnostics.

| Role | Meaning | Difference From Standalone Alpha |
| --- | --- | --- |
| Alpha signal | Directly ranks assets and is expected to produce return spread on its own. | Must prove signal-level and constructed-alpha robustness independently. |
| Context filter | Identifies market states where other signals behave better or worse. | Value comes from conditioning, not direct ranking strength. |
| Exposure modifier | Scales gross, net, or sleeve exposure up/down based on state. | Modifies risk allocation rather than security ranking. |
| Stress stabilizer | Intended to reduce degradation, drawdown, or left-tail behavior during stress. | Success is measured by robustness and damage control, not headline IC. |
| Regime gate | Turns a signal or alpha sleeve on only during confirmed states. | Creates episodic activation and must be judged by active-state diagnostics. |
| Blend-only stabilizer | Remains inside constructed alphas but is not evaluated as a standalone sleeve. | Its usefulness is marginal contribution and interaction quality. |
| Risk suppressor | Reduces fragile alpha exposure when the context implies poor forward conditions. | May lower returns intentionally to reduce bad-tail exposure. |
| Activation overlay | Adds state awareness above existing alpha selection or weighting. | Operates on existing alphas instead of creating a new signal family. |
| Transition smoother | Reduces turnover around activation/deactivation boundaries. | Primarily addresses implementation stability rather than predictive power. |

The central design rule is simple: a conditional component should not be assumed to be an alpha. A context filter can be valuable even if it is not independently promotable as a core alpha.

## 2. LOW_BREADTH's Current Role

Current evidence from Batch 4 attribution and the LOW_BREADTH regime/state map:

- LOW_BREADTH contains real conditional information.
- It is strongest at h20, with h10 also useful but weaker.
- It is most useful during collapsed breadth, persistent downtrends, volatility spikes, and panic/liquidity stress.
- It improves active-period behavior inside v4 smoothed constructed alphas.
- It aligns well with intended stress/breadth states.
- It is not robust enough as a standalone constructed alpha.
- It did not become part of the sole 07 stress-approved survivor.
- It is best classified as a `context filter`.

Important supporting facts:

- Isolated h20 signal WFV passed with effective mean test IC 0.051455, effective test IC IR 0.225597, persistence 0.75, and sign consistency 0.75.
- Active dates represented roughly 30% of observed dates.
- Activation was concentrated in collapsed breadth and stress states.
- Median activation episode length was only three trading days, creating transition risk.
- v4 smoothed blends had much stronger IC during LOW_BREADTH-active dates than inactive dates.
- Pure LOW_BREADTH sleeves were too sparse or high-turnover under current construction standards.

Interpretation:

LOW_BREADTH should be treated as contextual information that may improve alpha behavior under fragile market states. It should not be treated as a standalone alpha until a separate conditional construction prototype proves that role.

## 3. Candidate Construction Styles

The next research step should compare multiple construction semantics. Each style answers a different question about what LOW_BREADTH is allowed to do.

### A. Neutral Inactive

Inactive periods become neutral, zero, or flat.

Intended use:

- Baseline compatibility with current signal panels.
- Preserve full-date coverage for standard diagnostics.
- Keep official-style behavior easy to compare.

Expected benefits:

- Simple and interpretable.
- Compatible with existing scoring and construction assumptions.
- Avoids dropping dates from broad evaluation.

Risks:

- Inactive neutral values can still affect cross-sectional ranks.
- Active-state behavior may be diluted.
- Pure conditional sleeves can become no-dispersion rows on inactive dates.

Failure modes:

- Neutral inactive smoothing illusion.
- Inactive-state leakage.
- Weak official WFV despite strong active-state behavior.

Diagnostics required before implementation:

- Active vs inactive IC.
- Inactive-date rank dispersion.
- Exposure rate during inactive dates.
- No-dispersion row count.
- Comparison with masked active-only diagnostic.

### B. Active-State-Only

LOW_BREADTH is evaluated or used only during activation windows.

Intended use:

- Diagnose whether the component has true active-state value.
- Separate active-state edge from inactive-state dilution.
- Understand sparse conditional behavior without changing official gates.

Expected benefits:

- Cleanest view of the conditional edge.
- Reduces noise from irrelevant dates.
- Helps classify sparse episodic versus repeatable conditional behavior.

Risks:

- Active-only survivorship bias.
- Smaller samples and one-window dominance.
- Not directly comparable to always-on alphas.

Failure modes:

- Strong result driven by a few windows.
- Active-window coverage too low.
- Transition timing dominates apparent edge.

Diagnostics required before implementation:

- Active-date count.
- Active-window count.
- Active-window coverage ratio.
- One-window dominance.
- Active-only IC IR.
- Active-only stress overlap.

### C. State-Gated

LOW_BREADTH applies only during confirmed stress, breadth, trend, or volatility regimes.

Intended use:

- Require contextual confirmation before activation.
- Reduce false defensive activation.
- Align the component with economically interpretable states.

Expected benefits:

- More robust activation semantics.
- Lower risk of acting during broad risk-on rallies.
- Better interpretability for conditional-alpha research.

Risks:

- May activate too late.
- Added conditions can overfit.
- Could suppress useful early-warning periods.

Failure modes:

- Delayed activation during fast regime shifts.
- False deactivation during still-fragile recoveries.
- State overfitting to historical stress windows.

Diagnostics required before implementation:

- Lag between original activation and gated activation.
- Performance lost before confirmation.
- False activation rate.
- Missed opportunity rate.
- Stress-window coverage.

### D. Exposure Modifier

LOW_BREADTH modifies exposure instead of ranking assets directly.

Intended use:

- Scale exposure to existing alphas when breadth/stress context changes.
- Treat LOW_BREADTH as risk context rather than asset-selection signal.
- Explore whether it improves left-tail behavior.

Expected benefits:

- Better aligned with context-filter identity.
- May reduce drawdown without requiring standalone IC.
- Avoids forcing LOW_BREADTH to carry security selection.

Risks:

- Lower average returns from over-suppression.
- Accidental beta reduction mistaken for alpha.
- Scaling can hide whether the underlying alpha still works.

Failure modes:

- Reduced return without material drawdown improvement.
- Hidden beta exposure.
- Exposure cliff around activation boundaries.

Diagnostics required before implementation:

- Gross and net exposure by state.
- Sharpe and max drawdown by state.
- Drawdown contribution.
- Left-tail return behavior.
- Benchmark beta before/after scaling.
- Marginal contribution versus no-LOW_BREADTH counterfactual.

### E. Risk Suppressor

LOW_BREADTH suppresses fragile alphas during weak breadth or stress states.

Intended use:

- Reduce exposure to alphas that historically degrade in LOW_BREADTH states.
- Use the context filter defensively.
- Test whether LOW_BREADTH is more useful as a "do less" signal than a "rank better" signal.

Expected benefits:

- Directly addresses stress weakness.
- Could reduce left-tail risk and turnover in fragile environments.
- May be useful even with weak standalone IC.

Risks:

- Over-suppression during recoveries.
- Removes exposure during profitable rebound windows.
- Requires careful attribution to avoid mistaking lower risk for alpha.

Failure modes:

- Lower total return with no drawdown benefit.
- Poor performance after false defensive signaling.
- Deactivation too late or too early.

Diagnostics required before implementation:

- Suppressed alpha IC by state.
- Pre/post suppression drawdown contribution.
- Missed rebound return.
- Stress pass-rate change.
- Exposure recovery timing.

### F. Blend-Only Stabilizer

LOW_BREADTH remains inside constructed alphas but is never treated as standalone.

Intended use:

- Preserve current construction compatibility.
- Use LOW_BREADTH as a modest stabilizing component.
- Avoid overinterpreting sparse standalone behavior.

Expected benefits:

- Lowest design disruption.
- Builds on evidence that active periods improve inside v4 blends.
- Allows counterfactual attribution against no-LOW_BREADTH blends.

Risks:

- Blending can camouflage instability.
- Marginal contribution can become too small to matter.
- Stronger components may carry the blend.

Failure modes:

- LOW_BREADTH becomes a passenger.
- Apparent improvement comes from smoothing or other components.
- Active-state value is diluted away.

Diagnostics required before implementation:

- Full vs no-LOW_BREADTH counterfactual.
- LOW_BREADTH component-alone attribution.
- Dynamic weight audit.
- State-specific marginal IC.
- Blend interaction analysis.

### G. Overlay Layer

LOW_BREADTH acts above alpha selection as a contextual overlay.

Intended use:

- Influence alpha weights, candidate tiers, or sleeve-level research interpretation.
- Keep context separate from raw signal construction.
- Study whether conditional state awareness belongs at the alpha-management layer.

Expected benefits:

- Clean conceptual separation between signal ranking and context.
- Easier to apply consistently across multiple alphas later.
- Good fit for context-filter identity.

Risks:

- More architectural complexity.
- Could become an implicit promotion path if not kept research-only.
- Overlay decisions may be harder to validate than raw signal behavior.

Failure modes:

- State overlay overfits historical stress regimes.
- Overlay improves diagnostics only by reducing exposure.
- Hard-to-explain interaction with existing alpha construction.

Diagnostics required before implementation:

- Overlay-on versus overlay-off attribution.
- State-level alpha selection changes.
- Exposure and turnover changes.
- Stress case deltas.
- Sleeve-level degradation analysis.

## 4. Evaluation Criteria

The next prototype should evaluate construction semantics without creating production gates or thresholds.

Recommended observational metrics:

- active-period IC
- inactive-period IC
- inactive-period leakage
- mean IC by state
- IC IR by state
- positive IC rate by state
- Sharpe
- max drawdown
- drawdown contribution
- turnover
- exposure rate
- active-window coverage
- transition instability
- stress-window behavior
- left-tail behavior
- one-window dominance
- marginal contribution versus no-LOW_BREADTH counterfactual
- beta / benchmark exposure by state
- blend interaction effect

Recommended comparisons:

- active versus inactive periods
- stress versus non-stress windows
- transition versus stable states
- isolated LOW_BREADTH versus blended LOW_BREADTH
- LOW_BREADTH-containing alpha versus no-LOW_BREADTH counterfactual
- neutral inactive versus masked active-only
- state-gated versus original activation
- exposure modifier versus direct ranking

These metrics should describe evidence. They should not become production thresholds in this phase.

## 5. Side-Effect Diagnostics

Conditional construction can improve diagnostics for the wrong reason. The prototype must explicitly look for side effects.

| Side Effect | Description | Diagnostic Question |
| --- | --- | --- |
| False defensive activation | LOW_BREADTH activates during healthy risk-on periods. | Does activation overlap with strong breadth/uptrend and hurt IC? |
| Delayed activation | LOW_BREADTH turns on after the useful warning period. | Is pre-activation behavior stronger than active behavior? |
| Transition whipsaw | Short episodes create unstable exposure changes. | Do first/last active days have poor IC or high turnover? |
| Reduced returns from over-suppression | Risk controls cut profitable exposure. | Does drawdown improve enough to justify lower return? |
| Hidden beta exposure | Apparent value is market beta or stress beta. | Does benefit survive benchmark beta/state attribution? |
| Accidental risk reduction mistaken for alpha | Lower exposure improves drawdown but not selection. | Is improvement due to lower exposure rather than better ranks? |
| Neutral inactive smoothing illusion | Zero/neutral inactive rows make metrics look stable. | Do inactive dates still affect ranks or dispersion? |
| Active-only survivorship bias | Only favorable active periods are measured. | Is performance concentrated in one window or episode? |
| Blend camouflage | Other components carry the constructed alpha. | Does no-LOW_BREADTH counterfactual perform similarly or better? |
| State overfitting | State definition is too tailored to history. | Does behavior survive across windows and adjacent states? |
| Turnover explosion | Activation/deactivation costs overwhelm edge. | Does transition turnover erase active-state benefit? |

## 6. Recommended Prototype Test

The next evidence-generating prototype should compare seven research-only variants:

| Variant | Question Answered |
| --- | --- |
| Neutral inactive version | Does current-compatible inactive handling preserve useful behavior? |
| Masked active-only version | What is the clean active-state edge without inactive dilution? |
| State-gated version | Does confirmed breadth/stress context improve activation quality? |
| Exposure modifier version | Is LOW_BREADTH better as a scaler than a rank signal? |
| Risk suppressor version | Does LOW_BREADTH reduce fragile-alpha drawdowns or left-tail loss? |
| Blended version | Does LOW_BREADTH add value inside broad constructed alphas? |
| No-LOW_BREADTH counterfactual | What behavior remains without the context filter? |

The prototype should be observational. It should write research artifacts and a research note only. It should not modify official construction, validation, WFV, stress, survivor, or portfolio paths.

Recommended prototype scope:

- Component: `smooth_trend_persistence_60_low_breadth`
- Primary horizon: h20
- Secondary horizon: h10
- Comparison alphas:
  - `alpha_decay_aware_dynamic_v4_smooth`
  - `alpha_regime_blend_dynamic_v4_smooth`
  - `alpha_hybrid_adaptive_v4_smooth`
  - `alpha_rolling_ic_dynamic_v4_smooth`
- Context states:
  - collapsed breadth
  - weakening breadth
  - persistent downtrend
  - volatility spike
  - panic/liquidity stress
  - recovery phase
  - strong breadth / persistent uptrend as false-activation checks

Expected output:

- construction-style comparison table
- state attribution table
- activation diagnostics
- transition diagnostics
- stress diagnostics
- side-effect findings
- recommended semantics label

## 7. Reusable Output Template

Future Conditional Construction Semantics notes should use the following structure.

### Component Identity

- component name
- signal family
- horizon(s)
- current research status
- source batch
- known direction convention

### Classified Role

- alpha signal
- context filter
- exposure modifier
- stress stabilizer
- regime gate
- blend-only stabilizer
- risk suppressor
- activation overlay
- transition smoother

### Intended State / Regime

- target state labels
- activation rule
- inactive handling
- expected active frequency
- expected active-window coverage

### Candidate Construction Styles

- neutral inactive
- active-state-only
- state-gated
- exposure modifier
- risk suppressor
- blend-only stabilizer
- overlay layer
- other project-specific style if justified

### Expected Behavior

- expected active-period behavior
- expected inactive-period behavior
- expected stress behavior
- expected transition behavior
- expected interaction with other components

### State Attribution Summary

- mean IC by state
- IC IR by state
- positive IC rate by state
- active-date count by state
- active-window count by state
- degradation versus unconditional behavior

### Activation Behavior

- active dates
- inactive dates
- active ratio
- episode count
- average episode length
- median episode length
- transition count
- delayed activation risk
- false activation risk

### Stress Behavior

- stress-window overlap
- stress-window IC
- drawdown contribution
- worst degradation
- stress pass/fail interpretation
- left-tail behavior

### Transition Behavior

- pre-activation behavior
- first active days
- late active days
- post-deactivation behavior
- transition turnover
- whipsaw evidence

### Side Effects

- false defensive activation
- delayed activation
- transition whipsaw
- over-suppression
- hidden beta exposure
- neutral inactive leakage
- active-only survivorship bias
- blend camouflage
- state overfitting
- turnover explosion

### Recommended Semantics

Choose one primary semantics label:

- `DIRECT_ALPHA_SIGNAL`
- `CONTEXT_FILTER`
- `EXPOSURE_MODIFIER`
- `RISK_SUPPRESSOR`
- `BLEND_ONLY_STABILIZER`
- `STATE_GATE`
- `OVERLAY_LAYER`
- `REJECT_AS_UNSTABLE_CONTEXT`
- `INCONCLUSIVE`

### Next Research Step

State a specific next diagnostic or prototype. Avoid broad recommendations that cannot be tested.

## 8. Final Recommendation

The next concrete diagnostic should be:

`LOW_BREADTH Conditional Construction Semantics Prototype`

It should compare:

- neutral inactive version
- masked active-only version
- state-gated version
- exposure modifier version
- risk suppressor version
- blended version
- no-LOW_BREADTH counterfactual

Recommended initial classification to test:

`CONTEXT_FILTER`

Secondary semantics to test:

- `EXPOSURE_MODIFIER`
- `RISK_SUPPRESSOR`
- `BLEND_ONLY_STABILIZER`

The prototype should determine whether LOW_BREADTH's context-filter identity is best expressed as:

- a direct conditional sleeve,
- an exposure scaler,
- a fragile-alpha suppressor,
- a blend stabilizer,
- or an overlay that should remain separate from alpha ranking.

## Non-Goals

This design note is not:

- a production implementation,
- a schema proposal,
- a gate proposal,
- a threshold proposal,
- a survivor-list change,
- a portfolio-construction change,
- an ML preparation step,
- a new alpha promotion path,
- or an expansion to other conditional alphas.

## Closing Summary

LOW_BREADTH's strongest evidence is contextual, not standalone. It identifies fragile states where constructed alphas behave better, especially around collapsed breadth, downtrends, volatility spikes, and panic/liquidity stress. But it is transition-heavy, construction-sensitive, and not stress-approved as a survivor component.

Conditional Construction Semantics should therefore separate "predictive rank signal" from "contextual modifier." Project Underdog should next test how LOW_BREADTH behaves under several construction semantics before deciding whether the Conditional-Alpha Framework needs a dedicated context-filter layer, exposure-modifier layer, or satellite-only research path.
