# Core Alpha Research Restart After LOW_BREADTH

## 1. Executive Takeaway

Project Underdog has completed its first full Conditional-Alpha research cycle. The cycle was valuable: LOW_BREADTH was shown to contain genuine conditional information, especially in collapsed breadth and stress environments, and the platform now has a reusable methodology for conditional diagnostics, regime/state mapping, construction semantics, and exposure-modifier sidecars.

The final LOW_BREADTH conclusion is conservative:

- primary role: `context filter only`
- not standalone robust enough as an alpha
- not part of a core stress survivor
- exposure-modifier behavior mostly explained by generic de-risking
- Conditional-Alpha Framework should remain available as a side research framework, not the active implementation target

The next research frontier should return to core alpha discovery.

Final recommendation:

`Run a robustness-first orthogonal discovery batch focused on liquidity-flow, volatility-structure, and residual/relative-value families.`

The goal should be standalone alpha evidence that can survive WFV, constructed-alpha WFV, stress, and survivor review without relying on conditional activation semantics.

This note is research/planning only. It does not modify production pipelines, schemas, gates, thresholds, survivor lists, portfolio logic, notebooks, ML layers, or validation logic.

## 2. LOW_BREADTH Research Cycle Summary

The LOW_BREADTH cycle answered an important question: conditional information can be real without being a promotable alpha.

Key conclusions:

- LOW_BREADTH contains genuine conditional information.
- Its strongest signal-level evidence is at h20.
- It is most useful during collapsed breadth, persistent downtrend, volatility spike, and panic/liquidity stress states.
- It improved active-period behavior inside v4 smoothed constructed alphas.
- It reached the alpha pool and entered constructed alphas.
- It did not become part of the sole 07 stress-approved survivor.
- It is best classified as `context filter only`.
- Exposure-modifier behavior improved drawdown and left-tail proxies, but mostly through generic lower exposure.
- Exposure-modifier implementation research is paused.

Strategic implication:

The Conditional-Alpha Framework is now a mature diagnostic side framework. It should remain available for future candidates, but the active research frontier should move back to standalone alpha discovery and orthogonal expansion.

## 3. Current Core Alpha Landscape

### Survivor Status

Current survivor-freeze state:

- final `PROMOTE_CORE` survivors: 0
- sole `APPROVED_STRESS` alpha: `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`
- final decision for the stress-approved alpha: `REVIEW_SATELLITE`
- final status: `SATELLITE_WATCHLIST`

The stress-approved satellite:

| Alpha | Horizon | Stress Status | Final Decision | Pass Rate | Worst Degradation | Turnover Risk |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `alpha_orthogonal_diversifier_v2_score_weighted_smooth` | 20 | `APPROVED_STRESS` | `REVIEW_SATELLITE` | 0.777778 | 0.788569 | `MODERATE_TURNOVER_RISK` |

Primary blockers to `PROMOTE_CORE`:

- stress pass rate below the core threshold
- moderate turnover risk
- survivor selection score below the cluster-aware threshold
- degradation close to the catastrophic boundary

### Watchlist And Rejected Constructed Alphas

Current survivor registry watchlist/rejected structure:

| Alpha | Horizon | Final Decision | Final Status | Key Issue |
| --- | ---: | --- | --- | --- |
| `alpha_hybrid_adaptive_v4_smooth` | 5 | `REVIEW_SATELLITE` | `SATELLITE_WATCHLIST` | weak stress pass rate |
| `alpha_decay_aware_dynamic_v4_smooth` | 5 | `REVIEW_SATELLITE` | `SATELLITE_WATCHLIST` | weak stress pass rate |
| `alpha_persistence_blend_v2` | 10 | `REJECT_HIGH_TURNOVER` | `REJECTED_HIGH_TURNOVER` | high turnover |
| `alpha_diversified_research_v2` | 20 | `REJECT_HIGH_TURNOVER` | `REJECTED_HIGH_TURNOVER` | high turnover |

Stress table summary:

- one `APPROVED_STRESS`
- two `WATCHLIST_STRESS`
- three `REJECTED_STRESS`
- zero final core survivors

This is a healthy conservative outcome. The platform did not force a survivor.

### Alpha Signal Pool

Current alpha pool includes six signal-horizon components:

| Signal | Horizon | Family | Role | Health Score | Pool Weight |
| --- | ---: | --- | --- | ---: | ---: |
| `smooth_trend_persistence_60_low_breadth` | 20 | `trend_quality` | `DIVERSITY_SELECTED` | 87 | 0.172902 |
| `vol_of_vol_20` | 10 | `volatility_structure` | `DIVERSITY_SELECTED` | 62 | 0.152561 |
| `smooth_trend_persistence_60_low_breadth` | 10 | `trend_quality` | `DIVERSITY_SELECTED` | 72 | 0.143091 |
| `index_relative_reversal_5_high_drawdown` | 1 | `residual_relative_value` | `WATCHLIST_DIVERSIFIER` | 60 | 0.201009 |
| `trend_consistency_20_60` | 20 | `trend_quality` | `WATCHLIST_DIVERSIFIER` | 63 | 0.165263 |
| `smooth_trend_persistence_60_downtrend` | 1 | `trend_quality` | `WATCHLIST_DIVERSIFIER` | 68 | 0.165173 |

Interpretation:

- The current pool is still dominated by trend-quality and conditional/stress-derived ideas.
- Volatility structure is represented but not yet deep.
- Residual/relative-value is present but mostly watchlist.
- Liquidity-flow and microstructure appear more promising downstream than their raw signal scores alone suggest, because the stress-approved satellite came from an orthogonal diversifier using several non-trend components.

### Family-Level Signal Landscape

Current scoring-family summary shows strongest raw scoring evidence in:

| Family | Avg Abs Mean IC | Max Abs Mean IC | Best Signal |
| --- | ---: | ---: | --- |
| `trend_quality` | 0.028381 | 0.148629 | `smooth_trend_persistence_60_downtrend` |
| `breadth_cross_sectional_context` | 0.028261 | 0.083434 | `percentile_rank_stability_20_downtrend` |
| `residual_relative_value` | 0.012442 | 0.046983 | `index_relative_reversal_5_high_drawdown` |
| `microstructure_lite` | 0.013548 | 0.041866 | `failed_breakout_reversal_20_low_breadth` |
| `volatility_structure` | 0.007712 | 0.015976 | `vol_of_vol_20` |
| `liquidity_flow` | 0.004108 | 0.011528 | `price_impact_proxy_20` |

This ranking should not be read as "trend-quality is solved." Trend-quality has the highest signal IC, but it also carries regime dependence and conditional fragility. The current stress-approved satellite is orthogonal and includes volatility, impact, range-expansion, and liquidity-adjusted reversal components.

### Phase 1 vs Phase 2 Evolution

Phase 1 established basic signal extraction, multi-factor scoring, and early modeling baselines.

Phase 2 changed the research standard:

- modular scoring engines replaced notebook-only logic
- multi-horizon signal scoring became systematic
- WFV became a central rejection tool
- decay, regime, health, reproducibility, and diversity stages became explicit
- alpha construction and stress testing became stricter
- diagnostics became research artifacts rather than ad hoc observations

Phase 2 has shown that raw IC is not enough. Persistence, sign consistency, turnover, stress degradation, and survivor score now matter more than headline in-sample behavior.

### Multi-Horizon Observations

Observed horizon patterns:

- h20 often produces stronger trend-quality and conditional evidence.
- h5/h10 sometimes survive constructed-alpha WFV after smoothing, but stress remains difficult.
- h1 can appear useful for stress or reversal variants but is often less stable.
- Horizon instability remains a major failure mode.

The next discovery batch should avoid excessive horizon sprawl. It should define expected horizon ranges up front and prioritize candidates that remain directionally coherent across adjacent horizons.

### WFV Lessons Learned

Repeated WFV failure modes:

- direction flips
- weak effective IC
- weak effective IC IR
- low persistence
- low sign consistency
- one-window dominance

WFV has worked correctly. It rejected unstable universal candidates, rejected weak refinements, and allowed only the strongest conditional candidate through signal WFV without automatically producing a core survivor.

### Conditional-Alpha Lessons Learned

The LOW_BREADTH cycle clarified:

- conditional context can improve active-period behavior
- context filters are not the same as alphas
- active-state diagnostics are useful but can overstate sparse edges
- exposure modification can look good because it lowers exposure
- equal-exposure and randomized-timing controls are essential
- current core survivor logic should remain strict

## 4. Current Architecture Assessment

### Mature Components

The following platform components are now mature enough to support the next discovery cycle:

- signal factory and metadata-driven candidate generation
- family organization
- structural quality checks
- multi-horizon IC/IR scoring
- daily IC cache
- panel cache
- WFV bridge and constructed-alpha WFV
- signal health, reproducibility, and diversity
- stress testing and survivor-freeze diagnostics
- research artifact discipline under `docs/research_notes/`
- parity checks for extracted stages
- conditional diagnostics as sidecar research tools

### Fragile Components

Areas that remain fragile:

- alpha construction can still camouflage weak components
- turnover control can improve viability while diluting signal identity
- conditional activation metadata is not first-class in constructed alphas
- stress attribution does not yet fully decompose component-level contribution
- broad candidate generation can outpace interpretation
- universe breadth remains limited enough that findings may be universe-specific

### Potential Future Redesign Areas

Potential redesigns, not immediate tasks:

- component-level stress attribution inside constructed alphas
- explicit satellite research taxonomy
- universe expansion validation
- factor exposure and beta-neutral diagnostics before construction
- standardized redundancy audits before alpha pool admission
- conditional-alpha object model, only if future candidates justify it

## 5. Current Bottlenecks

The most important bottlenecks now are:

1. `Insufficient orthogonal standalone signal families`

The pool still leans heavily on trend-quality and conditional stress variants. The only stress-approved alpha came from an orthogonal diversifier, which argues for more non-trend standalone research.

2. `Stress instability`

Even promising constructed alphas fail or become satellites because stress pass rates, degradation, and turnover do not meet core standards.

3. `Turnover fragility`

High-turnover constructed alphas are repeatedly rejected. Low-turnover smoothing helps but may dilute alpha identity.

4. `Hidden factor exposure`

Some conditional and stress edges may be market beta, volatility beta, or drawdown-state exposure rather than alpha. Future standalone candidates need earlier exposure diagnostics.

5. `Signal redundancy`

Trend-quality candidates cluster tightly. Diversity selection helps, but the discovery process should reduce redundancy before expensive downstream validation.

6. `Horizon instability`

Signals often look strong at one horizon but fail adjacent horizons or downstream WFV. New batches should prefer horizon-stable design.

7. `Blend camouflage`

Constructed alphas can appear viable while individual components add little or introduce fragility. Attribution must happen earlier.

## 6. Orthogonal Discovery Opportunities

### A. Residual / Relative-Value Structures

Why promising:

- Current pool includes residual-relative candidates, but they remain underdeveloped.
- Residualized signals may reduce market-direction dependence.
- Relative-value structures can complement trend-quality behavior.

Orthogonality potential:

- High if residualization is done against benchmark, sector-like proxies, or cross-sectional common return components using OHLCV-only inputs.

Known risks:

- Residual estimates can be noisy.
- Direction flips are common.
- Short-window residuals can become unstable in stress regimes.

Expected failure modes:

- weak persistence
- beta leakage
- unstable signs across drawdown regimes
- high turnover if residual windows are too short

### B. Liquidity-Flow Structures

Why promising:

- The sole stress-approved satellite included `liquidity_adjusted_reversal_5`.
- Liquidity-flow signals may behave differently from trend-quality and breadth context.
- Volume/impact-aware effects can add orthogonality.

Orthogonality potential:

- Strong if signals emphasize volume imbalance, price impact, dollar-volume shocks, and flow persistence rather than simple returns.

Known risks:

- Liquidity proxies can be noisy.
- Turnover and execution-cost sensitivity may be high.
- Volume effects may be universe-specific.

Expected failure modes:

- high turnover
- stress degradation under cost assumptions
- weak raw IC but useful diversification
- correlation with volatility spikes

### C. Volatility-Structure Signals

Why promising:

- `vol_of_vol_20` is already in the alpha pool.
- The stress-approved satellite included `vol_surprise_20_60`.
- Volatility structure may provide orthogonal defensive and timing behavior without explicit conditional semantics.

Orthogonality potential:

- Moderate to strong, especially when paired with range, compression, volatility-of-volatility, and volatility-normalized return concepts.

Known risks:

- Can become generic risk-off exposure.
- May reduce returns if over-defensive.
- May overlap with LOW_BREADTH/stress diagnostics.

Expected failure modes:

- generic de-risking mistaken for alpha
- weak effective IC IR
- poor recovery behavior
- redundancy with volatility filters

### D. Quality-Stability Structures

Why promising:

- Stability/rank persistence showed conditional promise but not universal robustness.
- A less conditional version focused on smooth, robust cross-sectional stability may help reduce turnover.

Orthogonality potential:

- Moderate. It may overlap with trend-quality unless designed around stability rather than trend direction.

Known risks:

- Can become slow-moving and low IC.
- May miss turning points.
- May concentrate in large stable names.

Expected failure modes:

- weak mean IC
- slow decay
- low responsiveness
- hidden size/liquidity exposure

### E. Cross-Sectional Dispersion Structures

Why promising:

- Dispersion states repeatedly appear in conditional diagnostics.
- Dispersion can influence whether trend, reversal, and residual effects work.
- A standalone dispersion-aware signal might capture opportunity-set quality without hard conditioning.

Orthogonality potential:

- Moderate, depending on whether the signal ranks assets by dispersion contribution, range behavior, or idiosyncratic movement.

Known risks:

- May become a volatility proxy.
- Requires careful distinction between market-wide and asset-specific dispersion.

Expected failure modes:

- redundancy with volatility structure
- stress fragility
- weak signs across regimes

### F. Interaction Signals

Why promising:

- Many single signals fail because the edge appears only when another state or feature confirms it.
- Interactions may create standalone robustness without hard conditional activation.

Orthogonality potential:

- Potentially high, but only if interactions are sparse and interpretable.

Known risks:

- Parameter sprawl.
- Overfitting.
- Harder attribution.

Expected failure modes:

- one-window dominance
- poor reproducibility
- unstable sign
- hidden conditionality

## 7. Discovery Philosophy Recommendation

The next discovery cycle should be:

`robustness-first, orthogonality-first, low-sprawl`

Principles:

- prioritize robustness over novelty
- prioritize orthogonality over raw IC
- require clear economic or structural intuition
- prefer h10/h20 candidates unless the hypothesis is explicitly short-horizon
- avoid hard conditional activation in the next core batch
- use regime/context diagnostics as explanatory tools, not construction semantics
- reduce turnover at formula design time, not only after construction
- include attribution earlier, before expensive downstream stages
- test fewer, cleaner candidates rather than broad speculative batches

Concrete design preferences:

- high coverage
- OHLCV-only
- simple rolling windows
- rank/percentile normalization where useful
- volatility or liquidity normalization only when it directly reduces known failure modes
- no sector dependencies yet
- no ML layer yet
- no gate relaxation

## 8. Conditional-Alpha Framework Status

The Conditional-Alpha Framework is now:

- a reusable side research framework
- a future candidate evaluation system
- a diagnostic layer for context filters, sparse episodic edges, and state-dependent behavior
- not the current implementation target
- not the current production research focus

It should be revisited only if a future candidate shows:

- strong active-state behavior
- enough active-window coverage
- robustness beyond equal-exposure or random-timing controls
- component contribution after construction
- stress-window benefit not explained by generic de-risking
- manageable transition behavior
- clear value versus no-condition and no-component counterfactuals

Candidate types that should enter the framework later:

- signals with real WFV evidence but clear state dependence
- components that improve active-period behavior after construction
- context filters that pass equal-exposure and randomized-timing controls
- sparse episodic edges with enough independent active windows

Candidate types that should not enter:

- weak signals looking for a softer path
- state definitions created after seeing results
- exposure reducers that only lower volatility
- one-window stress artifacts

The LOW_BREADTH cycle established a higher standard. Future conditional candidates must clear that standard before Conditional-Alpha research becomes active again.

## 9. Recommended Next Execution Step

Single best next move:

`Run a robustness-first orthogonal discovery batch focused on liquidity-flow, volatility-structure, and residual/relative-value standalone signals.`

Why this is the best next step:

- The current platform has zero core survivors.
- The sole stress-approved satellite came from an orthogonal diversifier, not the conditional LOW_BREADTH path.
- Current alpha pool is still too trend-quality and conditional-context heavy.
- Stress robustness needs families that behave differently under degradation, turnover, and drawdown tests.
- The Conditional-Alpha Framework is now established and can rest as a side framework.

Suggested batch shape:

- 6 to 9 candidates total
- 2 to 3 liquidity-flow candidates
- 2 to 3 volatility-structure candidates
- 2 to 3 residual/relative-value candidates
- no hard conditional activation
- no new schemas or gates
- no WFV admission widening
- no universe expansion yet

Example research themes:

- liquidity-adjusted reversal persistence
- price-impact decay or impact reversal
- volume shock normalization with turnover control
- volatility surprise persistence or reversal
- volatility-compression quality without breakout chasing
- residual return stability versus universe/benchmark
- beta-adjusted residual momentum/reversal with smoother windows

Evaluation posture:

- structural quality first
- 03 scoring across standard horizons
- decay and regime diagnostics
- diversity/redundancy review
- controlled WFV only for candidates that earn it
- downstream 04A+ only if standard eligibility is reached

## 10. Strategic Outlook

Project Underdog should now shift from "Can we rescue conditional edges?" to "Can we discover robust, orthogonal, standalone alpha components?"

Near-term priorities:

1. Launch the robustness-first orthogonal discovery batch.
2. Add early attribution review for any candidate that reaches WATCHLIST or APPROVED scoring.
3. Compare new candidates against current orthogonal satellite components.
4. Keep conditional diagnostics available but inactive unless evidence demands them.
5. Preserve strict WFV, stress, and survivor gates.

What not to do yet:

- do not implement Conditional-Alpha semantics
- do not restart LOW_BREADTH exposure-modifier work
- do not relax gates to produce a core survivor
- do not launch ML
- do not expand the universe until core discovery has a clearer candidate set
- do not run broad speculative signal batches without an orthogonality thesis
- do not promote satellites into core roles

Criteria for future universe expansion:

- at least one robust candidate family demonstrates repeatable WFV/stress evidence
- current universe-specific fragility is understood
- runtime/caching can support wider panels
- liquidity and turnover diagnostics are ready for larger coverage

Criteria for future ML work:

- stable family-level features exist
- alpha labels are not dominated by noise
- WFV and stress frameworks are ready for ML leakage controls
- enough non-redundant standalone candidates exist to justify feature learning

Criteria for returning to Conditional-Alpha research:

- a future component shows state-dependent value that survives equal-exposure, randomized-timing, active-window, and construction-attribution controls
- the candidate adds something beyond generic de-risking
- there is enough active-window coverage to avoid episodic overfitting

## Final Recommendation

Project Underdog should restart core alpha research with a focused orthogonal discovery batch.

Recommended direction:

`robustness-first orthogonal standalone discovery across liquidity-flow, volatility-structure, and residual/relative-value families`

This is the best next move because the latest validated survivor evidence points away from conditional LOW_BREADTH implementation and toward orthogonal diversification. The platform has strong validation discipline; the next challenge is feeding it better standalone candidates.

The LOW_BREADTH cycle should be treated as a success: it produced a reusable conditional research framework and prevented premature implementation. Now the system should use that discipline to search for core-quality alphas again.
