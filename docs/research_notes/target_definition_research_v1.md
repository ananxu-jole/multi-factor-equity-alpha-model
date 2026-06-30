# Target Definition Research v1

Date: 2026-05-25

Status: `REVIEW_DESIGN_ONLY`

## Objective

Review whether Project Underdog should expand its research target vocabulary beyond raw h10/h20 forward-return IC.

This is not a proposal to loosen validation. It is a proposal to make the research question more precise before more discovery batches. Recent research suggests that some signals may be trying to measure repair, stabilization, resilience, downside control, or context usefulness while being judged only as standalone raw-return predictors.

This note does not implement targets, create runners, change validation logic, alter scoring gates, modify candidate statuses, touch production, route anything into portfolio/ML/blending/optimization, or change detector, metadata, or governance paths.

## Background

Recent OHLCV-only alpha branches were clean, diagnosable, and well governed, but mostly underpowered against raw h10/h20 forward-return IC.

Current strongest themes:

- repair
- stabilization
- resilience
- liquidity and participation recovery
- breadth repair
- volatility normalization
- drawdown avoidance
- conditional persistence

Current healthiest inventory evidence remains raw-return positive at h20, especially `participation_breadth_repair_under_hostile_trend`. However, recent rejected or weak branches often showed structural differentiation, persistence, or context relevance without enough raw IC.

Core question:

Are the features weak, or is the target too narrow for some of the mechanisms Project Underdog is studying?

Likely answer:

Both. Raw forward-return IC should remain the primary target for standalone alpha candidates, but the project needs separate research targets for risk reduction, recovery quality, and context layers so useful non-alpha evidence is neither overclaimed nor discarded incorrectly.

## Target Family Review

### 1. Raw Forward Return Targets

What it measures:

Cross-sectional relationship between signal scores and forward returns over horizons such as h1, h5, h10, h15, and h20.

Fit with current evidence:

This is still the cleanest target for standalone alpha. The current inventory candidates were selected because they showed meaningful h20 raw-return IC, persistence, and controlled overlap.

Risks:

- may reject useful downside-control or context signals
- may overweight average-return behavior and miss asymmetric payoff quality
- can favor stress-window winners if not paired with concentration diagnostics

Data requirements:

Existing OHLCV return panels are sufficient.

Implementation complexity:

Low. Already supported.

Recommended use:

Primary validation target for standalone alpha candidates. Discovery can still use it, but should not force every research artifact into this target class.

### 2. Drawdown-Adjusted Forward Return

What it measures:

Forward return adjusted for interim drawdown or adverse excursion during the holding window. A candidate can score well if it earns return with less path damage.

Fit with current evidence:

Strong fit. Repair and stabilization signals may be more about avoiding collapse after stress than maximizing raw forward return. Current volatility/stress and breadth-repair themes naturally imply path quality.

Risks:

- can become a disguised low-volatility or defensive factor
- may reward low-beta names rather than true repair
- drawdown definitions can be overfit
- needs careful separation from simple volatility carry

Data requirements:

Existing OHLCV data can support approximate forward max drawdown or adverse excursion. Better point-in-time benchmark/sector metadata would improve interpretation.

Implementation complexity:

Medium. Requires target construction and diagnostics for low-volatility overlap.

Recommended use:

Research-only target experiment first. Not validation until guardrails are designed.

### 3. Downside-Controlled Return

What it measures:

Forward return with explicit penalty for negative tail outcomes, such as lower-tail return, probability of severe loss, or return conditional on avoiding a drawdown threshold.

Fit with current evidence:

Good fit. Many Project Underdog themes are about hostile/stress repair and stabilization, where avoiding continued deterioration may be the economic edge.

Risks:

- can relabel risk control as alpha
- can favor low-volatility or large-cap defensiveness
- threshold choices can become brittle
- may reduce comparability to existing alpha IC standards

Data requirements:

OHLCV is enough for basic downside outcomes. Sector/size metadata would help detect defensive-factor duplication.

Implementation complexity:

Medium.

Recommended use:

Diagnostics and research notes initially. Potential future validation supplement, not primary standalone alpha target.

### 4. Recovery-Quality Targets

What it measures:

How cleanly a stock recovers after stress: return recovery, drawdown repair, volatility normalization, breadth/participation improvement, or reduced instability over a defined post-stress window.

Fit with current evidence:

Very strong conceptual fit. The strongest inventory identity is active repair/stabilization, and failed post-repair branches suggest the useful phase may be during repair rather than after completion.

Risks:

- target may overlap mechanically with signal features
- recovery state definitions can leak future information if not carefully anchored
- can become a narrow stress-slice target
- may produce context usefulness rather than tradable alpha

Data requirements:

OHLCV can support a first experiment. Better sector/peer metadata and richer event data would improve economic meaning.

Implementation complexity:

Medium to high, because event anchoring and leakage controls matter.

Recommended use:

Highest-priority research-only target experiment. Do not use for validation until definitions are frozen and leakage-reviewed.

### 5. Post-Stress Stabilization Targets

What it measures:

Whether a stock stabilizes after a stress event: lower realized volatility, lower range expansion, reduced downside gaps, improved close location, or lower instability persistence.

Fit with current evidence:

Strong fit for volatility compression and shock absorption themes. It may explain why some candidates show weak raw IC but meaningful state differentiation.

Risks:

- can become a volatility target rather than an alpha target
- may duplicate low-volatility exposure
- stabilization without return can be useful for risk, not alpha
- event start/end definitions are sensitive

Data requirements:

OHLCV supports basic implementation. Options/implied volatility would materially improve quality later.

Implementation complexity:

Medium.

Recommended use:

Diagnostics and context/risk research first. Potential validation supplement only if linked to return or drawdown-adjusted payoff.

### 6. Continuation-vs-Collapse Targets

What it measures:

Binary or ordinal outcome distinguishing names that continue recovering/stabilizing from names that relapse, break down, or propagate stress.

Fit with current evidence:

Good fit for transition-state and repair-completion questions. The Transition-State Composite Detector may be more useful for explaining collapse versus absorption than for predicting raw returns.

Risks:

- classification labels can be arbitrary
- binary outcomes can hide payoff magnitude
- high risk of tuning event definitions
- may be sample-size sensitive

Data requirements:

OHLCV can support a research version. Event metadata and sector context would make it stronger.

Implementation complexity:

Medium to high.

Recommended use:

Research diagnostics and context-layer evaluation. Not primary validation.

### 7. Volatility-Normalized Return

What it measures:

Forward return scaled by realized volatility, residual volatility, or adverse path risk. This asks whether return is efficient relative to risk.

Fit with current evidence:

Moderate fit. It may help separate weak raw return from better risk-adjusted behavior, especially for stabilization candidates.

Risks:

- can over-reward low-volatility names
- denominator instability in calm periods
- may duplicate quality/defensive exposures
- can obscure economically meaningful raw payoff weakness

Data requirements:

OHLCV is enough for realized volatility normalization. Residual volatility requires benchmark or peer residual definitions.

Implementation complexity:

Low to medium.

Recommended use:

Supplementary diagnostics. Not a replacement for raw-return validation.

### 8. Hit-Rate / Consistency Targets

What it measures:

Probability of positive forward return, positive relative return, or correct sign over repeated windows rather than average magnitude.

Fit with current evidence:

Moderate fit. Current monitoring already uses positive IC rate and WFV sign consistency. Some candidates may be more consistent than strong in magnitude.

Risks:

- small positive outcomes can look better than economically meaningful payoff
- ignores magnitude and tail risk
- can reward low-volatility drift
- may create false comfort in broad weak signals

Data requirements:

Existing panels are sufficient.

Implementation complexity:

Low.

Recommended use:

Diagnostics and guardrails. Not a standalone discovery target unless paired with payoff magnitude and drawdown controls.

### 9. Regime-Conditioned Targets

What it measures:

Signal performance within predefined market states, stress regimes, detector states, or inventory-relevant contexts.

Fit with current evidence:

Strong fit for explaining current inventory behavior. The Transition-State Composite Detector is behaviorally meaningful as a context layer, not a tradable alpha.

Risks:

- thin slices
- state-selection bias
- tuning labels to performance
- sample-size instability
- accidental conversion of context into alpha claim

Data requirements:

Existing state labels and detector artifacts can support research. More out-of-sample monitoring is needed before stronger claims.

Implementation complexity:

Medium.

Recommended use:

Context diagnostics and conditional attribution. Do not use as primary alpha validation without strict pre-registration and sample-size rules.

### 10. Asymmetric Payoff Targets

What it measures:

Whether a signal improves upside capture, downside avoidance, convexity, tail loss avoidance, or payoff skew, rather than mean return alone.

Fit with current evidence:

Good fit for repair/stabilization themes. A repair signal may be valuable if it avoids collapse while retaining moderate upside.

Risks:

- complex definitions invite overfitting
- tail metrics are sample-hungry
- can become crisis-window dependent
- harder to compare across candidates

Data requirements:

OHLCV can support basic tail and quantile metrics. Longer history, richer regime labels, and sector/size metadata would improve reliability.

Implementation complexity:

Medium to high.

Recommended use:

Research notes and diagnostics first. Potential later validation supplement if definitions remain stable.

## Ranked Target Families

| rank | target family | priority | recommended role |
| ---: | --- | --- | --- |
| 1 | Recovery-quality targets | HIGH | First research-only target experiment |
| 2 | Drawdown-adjusted forward return | HIGH | Research target and possible future validation supplement |
| 3 | Post-stress stabilization targets | HIGH | Diagnostics/context/risk target |
| 4 | Downside-controlled return | MEDIUM_HIGH | Research and risk diagnostics |
| 5 | Continuation-vs-collapse targets | MEDIUM_HIGH | Context and event-outcome research |
| 6 | Regime-conditioned targets | MEDIUM | Conditional attribution, not standalone validation |
| 7 | Asymmetric payoff targets | MEDIUM | Research diagnostics, sample-size sensitive |
| 8 | Volatility-normalized return | MEDIUM | Supplementary diagnostic |
| 9 | Hit-rate / consistency targets | MEDIUM_LOW | Guardrail, not primary target |
| 10 | Raw forward return targets | KEEP_PRIMARY | Primary standalone alpha validation target |

Note:

Raw forward return is ranked last only as a "new target" because it already exists. It should remain the primary standard for standalone alpha validation.

## Key Interpretation Questions

### Are signals failing because features are weak, or because the target is too narrow?

Recent evidence suggests both.

The repeated weak raw IC across clean OHLCV-only branches is real negative evidence. Many features are probably underpowered. But the strongest themes also point toward path quality, repair, and downside containment, which raw mean IC may not fully capture.

The correct response is not to relabel weak alpha as success. The correct response is to separate object types:

- standalone alpha
- recovery/risk target
- context layer
- diagnostic signal

### Do repair/stabilization signals map better to drawdown-adjusted or recovery-quality targets?

Yes, plausibly.

Repair and stabilization mechanisms naturally ask:

- did stress stop propagating?
- did drawdown repair begin?
- did volatility normalize without collapse?
- did participation or breadth recover cleanly?
- did the name avoid renewed downside?

Those questions are not identical to raw h20 return prediction.

### Should discovery separate return prediction, risk reduction, recovery quality, and context usefulness?

Yes.

Recommended object-type separation:

| object type | primary question | target family | promotion standard |
| --- | --- | --- | --- |
| Standalone alpha | Does the signal predict forward return? | raw h10/h20 return IC | Existing strict alpha gates |
| Risk/recovery candidate | Does the signal improve path quality after stress? | recovery-quality or drawdown-adjusted target | Future research-only target protocol |
| Context layer | Does it explain when alphas work or fail? | regime-conditioned attribution | Monitoring persistence, not alpha validation |
| Diagnostic flag | Does it identify fragility or concentration? | descriptive diagnostics | Governance/monitoring use only |

This separation prevents weak raw-return signals from being promoted while preserving useful context evidence.

## Recommended First Target Experiment

Recommended first experiment:

`recovery_quality_target_experiment_v1`

Purpose:

Compare existing inventory candidates and selected parked weak clues against a recovery-quality target, without changing their statuses or validation interpretation.

Suggested target definition, design-only:

- Anchor on dates with pre-existing stress/repair state labels.
- Measure h10/h20 recovery quality using:
  - forward return
  - interim max drawdown or adverse excursion
  - volatility/range stabilization
  - close-location improvement or downside containment
- Report raw return IC beside recovery-quality IC.
- Explicitly test whether recovery-quality strength exists when raw return IC is weak.

Initial targets to compare:

- raw h10/h20 forward return
- h10/h20 drawdown-adjusted return
- h10/h20 recovery-quality composite
- post-stress stabilization score

Initial candidate set:

- current Conditional Alpha Inventory candidates
- `volatility_participation_asymmetry_20`
- `volatility_structure_curvature_stabilization_20`
- `liquidity_volatility_peer_residual_quality_20`
- `turnover_shock_exhaustion_repair_20`

Important:

This experiment should be diagnostic only. It should not promote candidates, change validation gates, or create a new easier approval path.

## Required Guardrails For Any Future Target Experiment

Before implementation:

- predefine target formulas
- predefine candidate set
- report raw h10/h20 IC side by side
- preserve existing candidate statuses
- include low-volatility, reversal, momentum, and inventory overlap diagnostics
- include one-window dominance and crisis concentration diagnostics
- include sample-size and state-slice warnings
- classify outputs as target research only
- block production, validation, portfolio, ML, blending, and optimization use

## Risks And Caveats

Primary risks:

- target proliferation can become implicit overfitting
- weak alpha can be rebranded as "risk reduction" without evidence
- recovery targets can leak future state definitions
- drawdown-adjusted targets can duplicate low-volatility exposure
- regime-conditioned targets can become thin-slice cherry-picking
- asymmetric payoff targets can be sample-hungry

Controls:

- keep raw forward return as the standalone alpha standard
- make new targets research-only until separately governed
- compare all new targets against raw IC
- require anti-duplication diagnostics
- require pre-registered formulas and candidate sets
- avoid candidate-by-candidate target tuning

## Final Recommendation

Project Underdog should expand target research, but not validation targets yet.

Recommended next move:

Design, then later implement, a research-only `recovery_quality_target_experiment_v1`.

The first target experiment should test whether existing repair/stabilization evidence looks stronger under recovery-quality and drawdown-adjusted definitions while preserving raw h10/h20 forward-return IC as the primary standalone alpha benchmark.

Do not change validation gates, candidate statuses, production routing, or governance based on this review.

## Intentional Non-Changes

This review did not:

- implement targets
- create runners
- change validation logic
- modify scoring gates
- alter candidate statuses
- touch production paths
- route anything into portfolio, ML, blending, or optimization
- change detector paths
- change metadata paths
- change governance paths
