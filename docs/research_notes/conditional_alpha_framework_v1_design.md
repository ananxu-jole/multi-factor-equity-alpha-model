# Conditional-Alpha Framework v1 Design

## 1. Objective

Project Underdog needs a conditional-alpha framework because recent research has shown that some useful signal behavior is state-dependent rather than universal.

Batch 1 and Batch 2 showed that broad universal signals are rare and often weak under strict WFV. Batch 3 showed that several failed universal signals have stronger behavior in specific market states. Batch 4 showed that LOW_BREADTH can selectively stabilize trend-quality behavior: `smooth_trend_persistence_60_low_breadth` passed 03 scoring, controlled 03B WFV, 03E health, 03F reproducibility, and 03G diversity. It reached the alpha pool and entered constructed alphas.

However, it did not become part of the sole 07 stress-approved survivor, and the sole stress survivor became `REVIEW_SATELLITE`, not `PROMOTE_CORE`.

The purpose of this framework is to design how Project Underdog should evaluate conditional signals after they enter alpha construction. It should explain whether conditional edges survive blending, smoothing, inactive-date handling, WFV, stress, and survivor review.

This is a research design only. It does not modify gates, schemas, pipelines, notebooks, promotion rules, or thresholds.

## 2. Current Problem

The current platform has a strong universal validation path:

- signals are scored across standard horizons
- official WFV uses fixed train/test windows
- health, reproducibility, and diversity decide signal research eligibility
- alpha construction combines eligible signals
- constructed alphas must pass WFV, stress, and survivor-freeze standards

That architecture is working as intended. The gap is that conditional signals behave differently from universal signals.

The current problem has four parts:

1. Universal validation asks whether a signal works broadly across all windows.
2. Conditional signal behavior asks whether a signal works during specific market states.
3. Alpha construction can blend or dilute conditional behavior after the signal reaches the alpha pool.
4. Stress and survivor logic currently evaluate constructed alphas as broad candidates for core promotion.

Batch 4 exposed this gap clearly. `smooth_trend_persistence_60_low_breadth` was valid at the signal level and entered constructed alphas, but downstream stress survival came from a different alpha sleeve that did not include it. The current system can say the conditional signal was admitted, but it does not yet fully explain how the conditional component helped, hurt, or disappeared inside constructed-alpha stress outcomes.

## 3. Signal Categories

### Universal Signals

Universal signals are expected to be broadly active and robust across standard WFV windows. They are the natural fit for the existing signal-to-alpha-to-core path.

Expected traits:

- high coverage
- stable sign
- acceptable IC IR
- broad WFV persistence
- reasonable turnover
- suitable for standard alpha construction

### Conditional Signals

Conditional signals are active or meaningful only under defined OHLCV-derived market states, such as LOW_BREADTH, DOWNTREND, HIGH_DRAWDOWN, HIGH_VOL, or LOW_PARTICIPATION.

Expected traits:

- clear activation rule
- sufficient active-date count
- sufficient active-window count
- stronger active-state behavior than unconditional behavior
- interpretable inactive-state handling

Conditional signals should not be judged only by headline unconditional IC, but they also should not bypass official validation.

### Sparse Episodic Signals

Sparse episodic signals are conditional signals with too few active windows or too much one-window dominance. They may show strong active-state IC, but the sample is not broad enough to support promotion.

Expected treatment:

- research watchlist only
- useful for hypothesis generation
- not suitable for core alpha construction under current rules

### Satellite Candidates

Satellite candidates are signals or constructed alphas that show credible but incomplete evidence. They may be directionally useful, conditional, diversifying, or stress-relevant, but they do not meet core promotion standards.

Satellite status should mean "monitor and study," not "quietly promote."

### Core Candidates

Core candidates are broad, stress-resilient, low-fragility alphas that can meet strict survivor and portfolio standards.

Expected traits:

- robust official WFV
- strong stress pass rate
- acceptable degradation
- acceptable turnover
- no excessive concentration or correlation concern
- final survivor-freeze eligibility

Core standards should remain strict.

## 4. Conditional Alpha Lifecycle

The proposed lifecycle is:

1. Conditional signal discovery
2. Conditional diagnostics
3. Active-state WFV diagnostics
4. Controlled bridge
5. Alpha pool eligibility
6. Conditional alpha construction
7. Conditional alpha WFV
8. Conditional stress testing
9. Survivor classification
10. Satellite/core decision

### 1. Conditional Signal Discovery

Identify candidate signals and market states using OHLCV-only definitions. Discovery should remain small and hypothesis-driven.

### 2. Conditional Diagnostics

Evaluate signal x state behavior:

- active-date count
- mean IC by state
- positive IC rate
- sign consistency
- active-window coverage
- degradation versus unconditional behavior
- direction-flip risk

### 3. Active-State WFV Diagnostics

Reuse official WFV windows, but evaluate only active-condition dates as a research-only sidecar. This explains whether official WFV failures reflect true instability, inactive-window dilution, sparsity, or one-window dominance.

### 4. Controlled Bridge

Only tightly scoped candidates should enter controlled signal WFV bridge runs. Existing WFV windows, purge/embargo, gates, and thresholds remain unchanged.

### 5. Alpha Pool Eligibility

Conditional signals may enter the standard alpha pool only if they pass the existing 03E/03F/03G process. No special conditional admission shortcut should exist in v1.

### 6. Conditional Alpha Construction

Once a conditional signal reaches the alpha pool, research should evaluate whether it should be:

- blended into broad alphas
- isolated into a state-gated alpha sleeve
- treated as a satellite component
- evaluated in a state-specific alpha pool

This is the primary new research area.

### 7. Conditional Alpha WFV

Constructed alphas containing conditional components should be evaluated under standard constructed-alpha WFV and a research-only active-state sidecar.

The goal is to separate:

- broad constructed-alpha robustness
- conditional component contribution
- inactive-state dilution
- state-specific performance

### 8. Conditional Stress Testing

Stress diagnostics should identify whether conditional components help or hurt during:

- active-state periods
- inactive-state periods
- high-turnover periods
- drawdown periods
- degradation-heavy stress cases

### 9. Survivor Classification

Survivor classification should remain conservative. Conditional alphas may be classified as:

- rejected
- watchlist
- satellite candidate
- balanced candidate
- core candidate

The v1 framework should document these categories, not change promotion rules.

### 10. Satellite/Core Decision

Core decisions should remain governed by existing survivor-freeze and portfolio standards. Satellite decisions can become a research taxonomy, but should not imply portfolio use.

## 5. Active vs Inactive State Handling

Conditional alpha design depends heavily on how inactive dates are handled.

### Neutral Inactive Dates

The signal emits a neutral value, often zero, when the condition is inactive.

Benefits:

- simple
- high coverage
- compatible with current panels
- avoids dropping dates

Risks:

- inactive dates can dilute active-state behavior
- neutral values may still affect ranks depending on cross-sectional processing
- official WFV may understate active-state behavior

Recommended v1 use: default for current signal compatibility and baseline research.

### Masked Inactive Dates

The signal emits missing values when inactive.

Benefits:

- cleaner separation between active and inactive states
- better active-only diagnostics

Risks:

- missingness can conflict with structural quality expectations
- cross-sectional ranks may change in subtle ways
- comparability with universal signals becomes harder

Recommended v1 use: diagnostics only.

### Zero Exposure Inactive Dates

The alpha sleeve carries no portfolio exposure when inactive.

Benefits:

- conceptually aligned with conditional deployment
- avoids forcing signals to act outside their intended state

Risks:

- creates episodic turnover around activation boundaries
- requires portfolio-level design
- can produce sparse exposure histories

Recommended v1 use: future portfolio research only, not current official path.

### Research Default

For v1 research, use neutral inactive dates as the official compatibility baseline and active-state/masked diagnostics as sidecars. Do not change official scoring or WFV behavior.

For future portfolio use, zero exposure inactive dates may be conceptually cleaner, but should wait until conditional-alpha validation and turnover diagnostics are mature.

## 6. Conditional Alpha Construction Concepts

### Always-On Alpha Using Conditional Signal Inputs

Conditional signals are blended into a normal constructed alpha. This is closest to the current architecture.

Benefits:

- compatible with current alpha construction
- easy to compare against existing constructed alphas

Risks:

- conditional behavior may be diluted
- inactive-state values may dominate rank behavior
- stress attribution can become unclear

### State-Gated Alpha

The constructed alpha activates only when the market state is active.

Benefits:

- preserves conditional intent
- easier active-state interpretation

Risks:

- sparse active windows
- high activation turnover
- harder standard WFV interpretation

### Alpha Sleeve Active Only During State

A dedicated sleeve exists for a conditional state such as LOW_BREADTH. The sleeve may be inactive outside that state.

Benefits:

- clean research object
- easier attribution
- natural satellite candidate structure

Risks:

- requires careful inactive exposure handling
- not compatible with current core portfolio assumptions without further design

### Satellite Alpha Sleeve

Conditional alphas are treated as satellite research objects, separate from core alpha survivors.

Benefits:

- avoids weakening core standards
- gives conditional edges a research home

Risks:

- could become a shadow promotion path if governance is unclear
- needs explicit non-portfolio status in v1

### Conditional Blending Weights

Weights vary based on market state. For example, a LOW_BREADTH trend-quality component receives higher weight only during LOW_BREADTH.

Benefits:

- retains broad alpha structure while respecting state dependence

Risks:

- increases complexity
- easy to overfit
- can hide lookahead or leakage if state labels are not carefully lagged

### State-Specific Alpha Pools

Separate alpha pools are maintained by market state.

Benefits:

- clear state-level research organization
- supports comparing which signals work in each context

Risks:

- requires more metadata and governance
- can fragment samples
- may encourage too many state-specific variants

## 7. Validation Philosophy

The standard WFV path remains the official baseline. Conditional-alpha research should explain conditional behavior without weakening the existing promotion structure.

Core principles:

- No gate relaxation.
- Active-state WFV remains diagnostic until explicitly governed later.
- Official WFV, stress, and survivor gates remain binding for core promotion.
- Conditional alpha diagnostics must be additive, not substitutive.
- Strong active-state results are hypotheses, not promotion evidence by themselves.

Conditional alphas must prove:

- active-state performance
- enough active dates
- enough active WFV windows
- acceptable active-window coverage ratio
- no one-window dominance
- sign consistency in active states
- acceptable turnover around activation boundaries
- stress robustness
- limited degradation during inactive or transition periods

Suggested research thresholds from active-state WFV should remain diagnostic:

- minimum active test dates per eligible window: 20
- minimum eligible active WFV windows: 2
- minimum active-window coverage ratio: 0.50
- one-window dominance above 60% of positive effective IC should be a warning

These are not official gates in v1.

## 8. Stress and Survivor Interpretation

Conditional alphas may fail core thresholds for valid reasons:

- active states are sparse
- turnover spikes around activation changes
- performance is concentrated in one stress window
- inactive-date behavior dilutes broad stress results
- constructed-alpha blending weakens the original conditional edge
- degradation can remain too high even if active-state IC is strong

`REVIEW_SATELLITE` may be appropriate when an alpha has useful but incomplete evidence. It can mean:

- monitor as a conditional research object
- retain for diagnostics
- compare against future conditional sleeves
- do not use as a core survivor

A future satellite taxonomy could distinguish:

- `CONDITIONAL_SATELLITE_RESEARCH`
- `SPARSE_EPISODIC_WATCHLIST`
- `DIVERSIFYING_STRESS_SATELLITE`
- `BALANCED_ALPHA_ALTERNATE`
- `CORE_ALPHA_CANDIDATE`

This taxonomy should not change current `PROMOTE_CORE` standards. Core portfolio standards should remain strict because they protect the platform from overfitted, sparse, or unstable alphas.

## 9. Data / Metadata Requirements

Conditional-alpha research needs explicit metadata. Proposed fields:

| Field | Purpose |
| --- | --- |
| `conditional_state` | Named state being evaluated, such as `LOW_BREADTH` or `DOWNTREND`. |
| `activation_rule` | Human-readable rule defining active dates. |
| `active_date_count` | Number of active dates in the evaluation sample. |
| `active_window_count` | Number of WFV windows with enough active dates. |
| `active_window_coverage_ratio` | Share of WFV windows with sufficient active-state evidence. |
| `inactive_handling` | `neutral_zero`, `masked_nan`, `zero_exposure`, or other explicit handling. |
| `conditional_family` | Research family such as `trend_quality_low_breadth` or `stress_reversal`. |
| `satellite_candidate_flag` | Research flag for candidates that are not core-promotable but deserve monitoring. |
| `conditional_alpha_version` | Version string for reproducibility. |

Additional useful metadata:

- `source_signal_name`
- `source_signal_horizon`
- `conditional_source`
- `active_state_wfv_status`
- `one_window_dominance_flag`
- `activation_turnover_proxy`
- `component_weighting_method`
- `state_lag_policy`
- `lookahead_risk_reviewed`

## 10. Risks

### Overfitting Regimes

Market states can be over-selected after observing outcomes. The framework should require small candidate sets and documented hypotheses.

### Sparse Sample Illusion

Strong IC during rare states can be statistical noise. Active-date and active-window counts must be visible in every diagnostic.

### One-Window Dominance

A signal may appear strong because one WFV window dominates the average. This should remain a warning even when active-state IC is high.

### Hidden Lookahead In Regime Labels

State labels must be constructed with information available at or before the signal date. Any rolling or benchmark-derived state must have a clear lag policy.

### Excessive Conditional Complexity

Stacking many conditions can create fragile rules. v1 should prefer one condition at a time and simple state definitions.

### Turnover Spikes

State-gated alphas may rebalance aggressively when conditions turn on or off. Turnover around activation boundaries needs explicit diagnostics.

### Weak Live Applicability

Some states are easy to label historically but hard to act on cleanly in real time. The framework must remain research-first and avoid live-trading claims.

## 11. Recommended v1 Implementation Path

No implementation is requested in this design note. A phased path is recommended.

### Phase 1: Diagnostics Only

Create research-only diagnostics for constructed alphas that contain conditional components.

Outputs should include:

- component contribution by active state
- constructed-alpha active-date counts
- active-window coverage
- active versus inactive performance
- one-window dominance
- stress case attribution

### Phase 2: Conditional Alpha Construction Prototype

Prototype conditional alpha construction in a sidecar research namespace.

Prototype options:

- always-on alpha with conditional components
- state-gated alpha sleeve
- LOW_BREADTH satellite sleeve
- conditional blending weight experiment

No outputs should write to official alpha promotion tables.

### Phase 3: Active-State WFV Evaluation

Extend active-state WFV diagnostics from raw signals to constructed conditional alphas.

Key comparisons:

- official WFV result
- active-only WFV result
- inactive-only behavior
- transition-period behavior
- active-window sufficiency

### Phase 4: Satellite Classification

Define research-only satellite classifications:

- conditional satellite candidate
- sparse episodic watchlist
- diversifying stress satellite
- rejected conditional alpha

These classifications should support interpretation, not portfolio inclusion.

### Phase 5: Later Portfolio Integration

Portfolio integration should be considered only after:

- conditional-alpha diagnostics are stable
- active-window thresholds are governed
- turnover around activation is acceptable
- stress results are interpretable
- satellite classification has been validated over multiple research cycles

## 12. Non-Goals

This framework is not:

- live trading
- automatic promotion
- ML preparation
- a gate relaxation mechanism
- a replacement for official WFV
- a replacement for the universal alpha framework
- a portfolio allocation framework
- a way to force sparse edges into production

The universal alpha framework remains the official core path.

## 13. Open Questions

- What active-date threshold is sufficient for constructed alphas, and should it differ from raw signal diagnostics?
- Should LOW_BREADTH be the first dedicated conditional sleeve, or should v1 support multiple states from the start?
- How should inactive dates be represented in constructed-alpha panels without confusing structural quality checks?
- Should conditional alpha WFV measure active-only returns, active-only IC, or both?
- How should turnover around state transitions be scored?
- Can component contribution be measured reliably when dynamic weights and smoothing are used?
- Should `REVIEW_SATELLITE` remain a single label, or should it be split into explicit conditional and diversifying categories?
- How should conditional alphas be compared against orthogonal diversifier alphas?
- What is the minimum evidence needed before a satellite framework can be connected to portfolio research?
- How should the project prevent regime-label overfitting as more conditional states are tested?

## 14. Final Recommendation

The next concrete step should be a research-only constructed-alpha attribution diagnostic focused on Batch 4 alphas that included `smooth_trend_persistence_60_low_breadth`.

That diagnostic should answer:

- where the LOW_BREADTH trend-quality component contributed
- whether it helped or hurt during constructed-alpha WFV windows
- whether it degraded during stress cases
- whether inactive-date handling diluted the original signal edge
- why constructed alphas containing it failed to become the sole stress-approved survivor

This is the most direct follow-up to the Batch 4 milestone. It keeps the project research-first, preserves all gates, and builds the missing bridge between conditional signal validation and conditional alpha construction.
