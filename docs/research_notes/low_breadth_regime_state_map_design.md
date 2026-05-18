# LOW_BREADTH Regime / State Map Design

## Objective

This note designs a research-only regime/state mapping framework for Project Underdog using `smooth_trend_persistence_60_low_breadth` as the initial Conditional-Alpha Framework prototype.

The purpose is to learn how a conditional component behaves across market environments, activation states, transitions, blends, and stress conditions. The goal is not to prove that LOW_BREADTH is deployable. The goal is to establish a reusable methodology for conditional-alpha regime/state mapping.

This is a methodology-design phase only. It does not modify pipelines, gates, schemas, thresholds, survivor lists, notebooks, production logic, alpha construction, or portfolio construction.

## Context

Prior LOW_BREADTH attribution research found that `smooth_trend_persistence_60_low_breadth`:

- contains genuine conditional information,
- improves active-period IC across several constructed alphas,
- does not yet behave as a standalone persistent alpha,
- can be diluted or hidden after blending,
- did not become part of the sole 07 stress-approved survivor,
- and should be isolated into a separate Conditional-Alpha Framework rather than forced through the universal-alpha path.

The next research need is a state map: under what environments does LOW_BREADTH help, hurt, stabilize, become redundant, activate correctly, activate incorrectly, or fail structurally?

## Core Research Question

The regime/state map should answer:

> When LOW_BREADTH is active, what market state is it really describing, and does the conditional component behave in a way that is useful, stable, interpretable, and robust enough for further conditional-alpha research?

The answer should be observational. It should not create promotion, rejection, or portfolio rules.

## 1. LOW_BREADTH Behavioral Hypotheses

### Hypothesis 1: LOW_BREADTH Helps During Breadth Deterioration

Expected behavior:

- The component should become more informative when participation weakens.
- Active-period IC should improve when breadth is falling or already low.
- The component should help distinguish resilient names from vulnerable names during narrowing markets.

Confirmation evidence:

- Higher active-period mean IC during weakening or collapsed breadth than during strong breadth.
- Positive active-period directional consistency.
- Better active-state WFV behavior when low breadth overlaps with deteriorating breadth.

Failure evidence:

- Similar or worse IC during weak breadth compared with normal breadth.
- Strong behavior only after breadth has already collapsed.
- Direction flips during breadth deterioration.

### Hypothesis 2: LOW_BREADTH Improves Defensive Positioning During Fragile Trends

Expected behavior:

- LOW_BREADTH should be most useful when trend quality is fragile, not during smooth risk-on rallies.
- It should behave like a defensive cross-sectional ranking layer.

Confirmation evidence:

- Stronger IC in downtrend, choppy, or trend-transition regimes.
- Better drawdown contribution during fragile trend periods.
- Lower left-tail loss in active LOW_BREADTH windows.

Failure evidence:

- Positive behavior only in stable uptrends.
- Poor behavior during sideways/choppy regimes.
- No improvement in drawdown contribution.

### Hypothesis 3: LOW_BREADTH Is A Stress Stabilizer Rather Than A Return Engine

Expected behavior:

- LOW_BREADTH may not maximize average return.
- Its value may be avoiding worse cross-sectional exposure during fragile states.

Confirmation evidence:

- Improved max drawdown or tail behavior during active periods.
- Lower stress degradation in conditional sleeves compared with broad blends.
- Better performance in volatility spike or drawdown acceleration regimes.

Failure evidence:

- No left-tail improvement.
- High active-period turnover overwhelms stress benefits.
- Stress pass rate remains low despite active-state IC.

### Hypothesis 4: LOW_BREADTH May Reduce Left-Tail Risk

Expected behavior:

- During weak breadth, the component should reduce exposure to names most vulnerable to continued deterioration.

Confirmation evidence:

- Better downside quantile behavior during active states.
- Reduced worst daily/weekly diagnostic spread returns.
- Better stress behavior during drawdown acceleration and volatility spike windows.

Failure evidence:

- The component improves average IC but worsens tail outcomes.
- Maximum drawdown remains similar or worse than non-LOW_BREADTH variants.
- Tail performance is dominated by one window.

### Hypothesis 5: LOW_BREADTH May Become Noisy During Broad Risk-On Rallies

Expected behavior:

- In strong breadth and broad risk-on environments, LOW_BREADTH should be inactive or less useful.
- If active during broad rallies, it may rank defensive or lagging names incorrectly.

Confirmation evidence:

- Inactive or low-weight behavior during strong breadth and persistent uptrends.
- Weak or negative IC when LOW_BREADTH activates during risk-on rallies.

Failure evidence:

- Frequent false activation during broad rallies.
- Direction flips in HIGH_BREADTH or breadth-recovery states.
- Excess turnover from false defensive signaling.

### Hypothesis 6: LOW_BREADTH May Activate Too Late During Fast Regime Shifts

Expected behavior:

- Breadth measures may lag rapid deterioration.
- The component may activate after the highest-risk transition has already occurred.

Confirmation evidence:

- Performance is strongest after activation and remains stable through deterioration.
- Pre-activation windows show limited missed opportunity.

Failure evidence:

- Large losses before activation.
- Better IC in pre-activation windows than active windows.
- Poor behavior immediately after activation, suggesting late entry.

## 2. Regime / State Axes

The LOW_BREADTH state map should use OHLCV-only, research-defined states. These states are diagnostics, not trading rules.

### A. Breadth States

| State | Why It Matters | Expected LOW_BREADTH Behavior | Likely Failure Modes |
| --- | --- | --- | --- |
| Strong breadth | Broad participation often supports risk-on behavior. | LOW_BREADTH should usually be inactive or unimportant. | False defensive activation; negative IC in rallies. |
| Weakening breadth | Participation is deteriorating but may not have fully collapsed. | Potentially strongest early warning state. | Delayed activation; noisy transition signals. |
| Collapsed breadth | Market participation is already weak. | Should stabilize rankings if weak breadth persists. | Activation too late; one-window dominance; high turnover. |
| Breadth recovery | Participation is improving after stress. | Component should decay or deactivate cleanly. | Persisting too long; fighting recovery; direction flip. |

### B. Trend States

| State | Why It Matters | Expected LOW_BREADTH Behavior | Likely Failure Modes |
| --- | --- | --- | --- |
| Persistent uptrend | Broad trend strength may make defensive filters unnecessary. | Low signal value; ideally inactive. | False defensive signaling; opportunity cost. |
| Persistent downtrend | Weak breadth may reinforce trend fragility. | Better IC and drawdown protection. | Crowded defensive exposure; late activation. |
| Sideways/choppy | Trend signals often whipsaw. | Could stabilize if breadth identifies participation quality. | Direction flips; transition churn. |
| Trend transition | Highest timing risk. | Should detect deterioration early enough to matter. | Activation lag; deactivation lag; whipsaw. |

### C. Volatility States

| State | Why It Matters | Expected LOW_BREADTH Behavior | Likely Failure Modes |
| --- | --- | --- | --- |
| Low volatility | Weak breadth may be hidden under calm index behavior. | Mixed; may detect quiet fragility. | Overfitting quiet weakness; low signal dispersion. |
| Rising volatility | Breadth deterioration may become more actionable. | Improved defensive ranking and stress awareness. | Turnover spike; signal instability. |
| Volatility spike | Stress regime; tail behavior matters. | Possible stabilizer if already active. | Activation too late; stress collapse. |
| Volatility normalization | Post-stress recovery or mean reversion. | Should reduce influence if breadth improves. | Persisting too long; missing rebound. |

### D. Stress States

| State | Why It Matters | Expected LOW_BREADTH Behavior | Likely Failure Modes |
| --- | --- | --- | --- |
| Drawdown acceleration | Tests whether component anticipates or reacts to losses. | Should improve defensive ranking if active early enough. | Late activation; large pre-activation losses. |
| Panic / liquidity stress | Liquidity and crowding dominate. | May stabilize if it avoids weak names. | Component overwhelmed by liquidity stress. |
| Recovery phase | Defensive signals can underperform. | Should deactivate or lose influence. | Fighting recovery; direction flip. |
| Post-stress stabilization | Tests decay after crisis. | Should normalize cleanly. | Lingering stale defensive exposure. |

### E. Dispersion States

| State | Why It Matters | Expected LOW_BREADTH Behavior | Likely Failure Modes |
| --- | --- | --- | --- |
| Low dispersion | Cross-sectional signal opportunity may be compressed. | Weak or noisy IC. | False precision; low rank spread. |
| High dispersion | More cross-sectional opportunity, often during stress. | Better ranking opportunity. | High variance; one-window dominance. |
| Rotational market | Leadership changes rapidly. | May help if breadth detects narrowing leadership. | Whipsaw; stale rank persistence. |

## 3. Activation Diagnostics

Activation diagnostics should describe when LOW_BREADTH turns on, how long it stays active, and whether activation aligns with intended states.

Required activation outputs:

- total active dates
- total inactive dates
- active-date ratio
- number of activation episodes
- average episode length
- median episode length
- maximum episode length
- number of active/inactive transitions
- transition density per year
- active dates by WFV window
- active dates by stress window
- activation overlap with breadth deterioration, trend transition, volatility spike, and drawdown acceleration

Key questions:

- Does activation align with intended weak-breadth regimes?
- Does it activate too often?
- Does it activate too rarely?
- Does it lag structural deterioration?
- Does it deactivate during useful periods?
- Does it remain active into recovery phases where it becomes harmful?

### Delayed Activation Risk

Measure pre-activation windows:

- 5 trading days before activation
- 10 trading days before activation
- 20 trading days before activation

Research question:

- Did alpha behavior already improve before LOW_BREADTH became active?

If yes, the condition may lag the useful part of the regime.

### False Activation Risk

Measure activation periods that overlap with:

- strong breadth
- persistent uptrend
- breadth recovery
- low volatility risk-on regimes

Research question:

- Did LOW_BREADTH activate during environments where it should not have been useful?

If yes, the component may create false defensive signals.

### Transition Instability

Measure behavior around:

- activation day
- first 5 active days
- final 5 active days
- first 5 inactive days after deactivation

Research question:

- Is most instability concentrated around activation boundaries?

If yes, future construction should consider hysteresis, confirmation, or slower state transitions.

## 4. State-Based Attribution Metrics

All metrics are observational. They should not become promotion thresholds in this design phase.

For each state, compute:

- mean IC
- median IC
- IC IR
- positive IC rate
- directional stability
- active-period effectiveness
- turnover proxy
- exposure rate
- diagnostic rank-spread Sharpe
- diagnostic max drawdown
- drawdown contribution
- stress-period behavior
- active-window count
- active-window coverage ratio
- one-window dominance

Comparisons:

- active versus inactive periods
- isolated LOW_BREADTH component versus blended constructed alpha
- stress versus non-stress windows
- transition versus stable-state windows
- LOW_BREADTH-only sleeve versus no-LOW_BREADTH counterfactual

Interpretation rules:

- Strong isolated behavior plus strong blended behavior suggests true conditional alpha potential.
- Strong isolated behavior but weak blended behavior suggests dilution or construction mismatch.
- Weak isolated behavior but strong blended behavior suggests LOW_BREADTH may be a passenger or context filter.
- Strong active behavior but poor stress behavior suggests incomplete robustness.
- Strong average behavior with one-window dominance suggests sparse episodic evidence, not robust conditional alpha.

## 5. Regime Transition Analysis

The regime map should explicitly study how LOW_BREADTH behaves before, during, and after state transitions.

### Pre-Stress Activation

Questions:

- Does LOW_BREADTH activate before drawdown acceleration?
- Does it activate before volatility spikes?
- Does it identify fragile participation before benchmark trend breaks?

Evidence to review:

- IC and spread-return behavior in 5/10/20 days before activation.
- Overlap between activation and future drawdown acceleration.
- Whether active dates precede stress or only follow stress.

### Activation During Deterioration

Questions:

- Does the component become useful immediately when active?
- Is the first activation segment noisy?
- Does it require confirmation or persistence?

Evidence to review:

- first 5 active days
- first 10 active days
- first active WFV window segment
- turnover around activation

### Activation During Recovery

Questions:

- Does LOW_BREADTH remain active too long?
- Does it fight recovery rallies?
- Does it flip direction after stress troughs?

Evidence to review:

- final active days before deactivation
- first inactive days after deactivation
- breadth recovery overlap
- strong breadth overlap after activation

### Activation Decay After Normalization

Questions:

- Does LOW_BREADTH's IC decay after volatility and breadth normalize?
- Does the component become redundant after the market stabilizes?

Evidence to review:

- active-period IC split by early/middle/late episode segment
- active-period IC conditional on volatility normalization
- component contribution after drawdown recovery begins

## 6. Conditional Failure Taxonomy

The regime map should classify failures into reusable categories.

| Failure Type | Description | Diagnostic Evidence |
| --- | --- | --- |
| Correct regime idea, delayed timing | State is conceptually right, but activation starts too late. | Pre-activation performance exceeds active-period performance. |
| Activation instability | Signal is noisy around on/off boundaries. | Poor first/last active days, high transition turnover. |
| Sparse but excessively costly | Active state is valid but too episodic or high-turnover. | Low active-window count, high turnover around transitions. |
| Stress collapse | Active-state IC does not survive actual stress cases. | Poor stress pass rate, high degradation, bad drawdown contribution. |
| Works only blended | Component helps only when mixed with other components. | Weak isolated behavior, better blended behavior. |
| Inactive-state leakage | Neutral inactive handling affects ranks or coverage unexpectedly. | Inactive dates influence constructed alpha behavior. |
| Hidden beta exposure | Apparent conditional alpha is broad market exposure. | Behavior disappears after beta/benchmark conditioning. |
| Regime overfitting | State definition fits history but lacks stability. | One-window dominance, unstable state-specific IC. |
| Transition whipsaw | Rapid state changes create turnover and unstable ranks. | High transition density and poor transition returns. |
| False defensive signaling | Component activates during healthy risk-on periods. | Active overlap with strong breadth/uptrend and negative IC. |

## 7. Standardized Regime Map Output

Every conditional regime/state map should produce the same research structure.

### A. Regime Definitions

Document each state axis, label definition, lag policy, and data source.

Required fields:

- `state_axis`
- `state_label`
- `definition`
- `data_inputs`
- `lag_policy`
- `known_limitations`

### B. Activation Profile

Summarize activation behavior.

Required fields:

- active-date count
- inactive-date count
- active-date ratio
- activation episode count
- average episode length
- transition count
- active WFV windows
- active stress windows

### C. State Attribution Table

One row per signal/alpha variant x state.

Recommended fields:

- `variant`
- `state_axis`
- `state_label`
- `active_date_count`
- `mean_ic`
- `ic_ir`
- `positive_ic_rate`
- `directional_stability`
- `turnover_proxy`
- `exposure_rate`
- `diagnostic_sharpe`
- `max_drawdown`
- `stress_overlap_flag`
- `one_window_dominance_flag`
- `interpretation`

### D. Stress Behavior Summary

Summarize performance during stress windows.

Required fields:

- stress window label
- active flag
- active-date count
- mean IC
- degradation contribution
- turnover proxy
- drawdown contribution
- interpretation

### E. Transition Analysis

Summarize behavior before and after activation/deactivation.

Required fields:

- transition type
- lookback/lookforward window
- mean IC
- turnover proxy
- diagnostic spread return
- activation timing assessment

### F. Interaction Observations

Compare:

- LOW_BREADTH isolated
- LOW_BREADTH blended
- no-LOW_BREADTH counterfactual
- LOW_BREADTH inside smoothed constructed alpha

### G. Structural Strengths

Examples:

- repeatable active-period IC
- useful context filtering
- improved active-state Sharpe
- good overlap with fragile regimes

### H. Structural Weaknesses

Examples:

- sparse exposure
- high transition turnover
- stress weakness
- direction instability
- blend dilution

### I. Conditional Recommendation

Use one of:

- `CONTINUE_RESEARCH`
- `WATCHLIST_CONDITIONAL_LAYER`
- `ISOLATE_IN_CONDITIONAL_FRAMEWORK`
- `REJECT_AS_NOISY`
- `REQUIRE_ADDITIONAL_STRESS_VALIDATION`

### J. Next Research Step

State the next specific diagnostic or prototype, not a broad direction.

## 8. Initial LOW_BREADTH Prototype Design

The first regime map should evaluate:

### Variants

- LOW_BREADTH component alone at h20
- LOW_BREADTH component alone at h10
- `alpha_decay_aware_dynamic_v4_smooth`
- `alpha_regime_blend_dynamic_v4_smooth`
- `alpha_hybrid_adaptive_v4_smooth`
- no-LOW_BREADTH counterfactuals for those constructed alphas

### Primary State Axes

- breadth level
- breadth change
- benchmark trend
- benchmark volatility
- drawdown depth
- volatility change
- dispersion

### Primary Transition Windows

- 20 days before activation
- 10 days before activation
- first 10 active days
- final 10 active days
- 10 days after deactivation
- 20 days after deactivation

### Primary Stress Windows

Use existing 07 stress windows and constructed-alpha WFV windows as diagnostic anchors. Do not create new official stress cases.

## 9. Final Research Recommendation

The next LOW_BREADTH diagnostic should be a research-only regime/state map that applies this design to:

- isolated LOW_BREADTH h20 and h10 components,
- the v4 smoothed constructed alphas that contained LOW_BREADTH,
- and their no-LOW_BREADTH counterfactuals.

The diagnostic should focus first on whether LOW_BREADTH is:

- an early deterioration signal,
- a stabilizer during weak breadth,
- a stress reducer,
- or a context filter that only works when blended carefully.

Additional conditional components should enter mapping research only after the LOW_BREADTH prototype produces a clear and reusable output structure. The next candidates should be limited to components with prior conditional evidence and enough active-window coverage, not broad exploratory ideas.

Evidence that would justify future Conditional-Alpha Framework expansion:

- LOW_BREADTH shows repeatable active-state benefit across multiple state axes.
- Activation timing is interpretable and not systematically late.
- Transition turnover can be controlled without erasing the edge.
- Stress behavior is explainable, even if not yet promotable.
- Isolated and blended behavior can be decomposed consistently.
- The state map distinguishes stabilizer, passenger, and true conditional alpha behavior without changing gates.

## 10. Non-Goals

This regime/state map is not:

- a deployment study,
- a promotion path,
- a survivor-freeze change,
- a portfolio construction change,
- a gate relaxation mechanism,
- a replacement for official WFV,
- or a proof that LOW_BREADTH should be traded.

The framework is meant to improve understanding before any future Conditional-Alpha implementation work.

## Closing Summary

LOW_BREADTH is a useful prototype because it has enough evidence to be interesting and enough downstream failure to require discipline. It passed the signal stack, entered constructed alphas, improved active-period IC, but did not become a core survivor.

That makes it an ideal first case for regime/state mapping. The framework should reveal whether LOW_BREADTH is a true conditional alpha, a stabilizer, a context filter, a blended passenger, or an unstable defensive signal. The answer should guide future Conditional-Alpha Framework research without weakening Project Underdog's validation standards.
