# Project Underdog Research Framework v1

## 1. Project Objective

Project Underdog is a validation-first alpha research platform for developing robust, explainable equity signals. The goal is not to maximize in-sample IC or produce the largest possible set of survivors. The goal is to identify signal behavior that remains credible after structural checks, multi-horizon scoring, decay analysis, regime diagnostics, walk-forward validation, reproducibility testing, and diversity controls.

The platform is intentionally conservative. A signal is more valuable if it survives repeated stress and attribution checks than if it shows a strong headline metric in one sample. Survival, robustness, and interpretability are prioritized over short-term discovery speed.

## 2. Core Research Philosophy

Project Underdog uses strict rejection discipline. Gates are not relaxed to force signals through the pipeline, and failures are treated as useful research information rather than wasted effort. A rejected signal can reveal regime dependence, direction instability, sparse sampling, poor persistence, or redundancy with existing factors.

The core philosophy is:

- Robustness is more important than headline performance.
- Reproducibility comes before promotion.
- Walk-forward rejection is a feature, not a problem to bypass.
- Failed signals improve the research map by showing where edges do not generalize.
- Conditional edges may exist even when universal edges fail, but they require separate diagnostics before they can be trusted.

This philosophy keeps the platform from overfitting to attractive but unstable effects.

## 3. Current Research Stack

The current research stack is modular and increasingly diagnostic-oriented:

- Modular orchestration separates research stages and keeps pipeline responsibilities explicit.
- Extracted scoring engines support repeatable 03 scoring, 03C decay, 03D regime diagnostics, 03E health, 03F reproducibility, and 03G diversity.
- The WFV framework provides fixed-window, purge/embargo-aware out-of-sample validation.
- Panel cache and daily IC cache reduce repeated compute cost and make large scoring passes more practical.
- Profiling and optimization work has improved long-running scoring and validation stages.
- Parity validation preserves confidence that extracted engines match notebook-era behavior.
- Research diagnostic layers now include WFV failure diagnostics, conditional signal diagnostics, and active-state WFV diagnostics.

The stack is designed to support careful iteration without changing gates or downstream eligibility rules during exploratory research.

## 4. Signal Taxonomy

### A. Universal Signals

Universal signals are broadly active across the market history and are expected to remain informative across multiple fixed WFV windows. They follow the standard validation path:

- Structural quality
- 03 scoring
- 03C decay
- 03D regime diagnostics
- 03E health
- 03F reproducibility
- 03G diversity
- Alpha signal pool eligibility

Universal signals are the only category currently suited to standard alpha construction if they clear all required checks.

### B. Conditional Signals

Conditional signals are regime- or state-dependent. They may be active only during benchmark downtrends, high drawdown periods, high volatility regimes, low participation regimes, or other OHLCV-derived market states.

These signals require conditional diagnostics before interpretation. Standard WFV remains valid as the official gate, but it may not fully explain why a signal works or fails when active states are sparse. Conditional signals may eventually belong in a separate conditional-alpha framework, but they should not be promoted simply because they perform well in one state.

### C. Sparse Episodic Edges

Sparse episodic edges show strong behavior in rare market states but lack enough active-window coverage to establish persistence. They can look compelling in active-state diagnostics while still failing official WFV because too few windows contain usable active samples.

These edges belong on a research watchlist only. Under the current framework, they are not promotable. They are useful for hypothesis generation and conditional-alpha design, not for immediate alpha construction.

## 5. Validation Framework

The validation framework is layered to catch different failure modes:

- Structural quality verifies coverage, finite values, missingness, and basic data viability.
- 03 scoring measures multi-horizon IC, direction, strength, and preliminary signal quality.
- 03C decay checks whether signal behavior is stable, decaying, or unstable through rolling IC evidence.
- 03D regime diagnostics identify regime fragility, conditional opportunity, and sign flips across market states.
- 03E health combines scoring, decay, regime, and WFV evidence into a research health view.
- 03F reproducibility checks subset and out-of-sample consistency before alpha research eligibility.
- 03G diversity controls redundancy and prevents the pool from being dominated by similar edges.
- WFV tests whether a signal persists across fixed train/test windows under purge and embargo constraints.

Persistence and sign consistency matter because many signals can produce attractive average IC from a small number of favorable periods. A robust signal should show repeatability, not only isolated strength.

## 6. Conditional Research Evolution

Batch 1 expanded the signal library broadly. It produced useful candidates but also showed that several edges were unstable under WFV. Failures included weak effective IC, low persistence, low sign consistency, and direction flips.

Batch 2 refined the strongest failed candidates with simple variants targeting persistence, sign consistency, and effective IC robustness. The refinements improved some in-sample diagnostics but still failed controlled WFV where appropriate.

Batch 3 shifted the research question from universal edges to conditional edges. Instead of asking whether every signal should work across all market states, the diagnostics asked where each signal historically worked or failed. This led to conditional variants such as downtrend-conditioned trend persistence and high-drawdown reversal.

Active-state WFV diagnostics then clarified a key limitation: some conditional signals may look strong only because they are active in very few windows. The framework now distinguishes between conditional promise and sparse episodic evidence.

## 7. Current Interpretation

Unconditional WFV was not wrong. It correctly rejected signals that did not demonstrate persistence across the official fixed windows.

The newer diagnostics add context rather than overturning WFV. Some signals appear conditional rather than universal. Others are sparse episodic edges that need active-state-aware analysis but remain unsuitable for promotion under the current rules.

The current framework is intentionally conservative. It allows conditional research to continue while preventing sparse or unstable signals from entering the alpha pool prematurely.

## 8. Future Research Directions

Future research should focus on:

- Conditional-alpha framework design, separate from standard universal signal promotion.
- Active-state-aware validation methods that remain research-only until formally governed.
- Regime-aware signal design using simple OHLCV-derived conditions.
- Robustness diagnostics that explain failures before generating new variants.
- Larger-universe expansion after validation tools remain stable at current scale.
- Possible ML integration later, after signal taxonomy and validation logic are mature.

Sparse conditional edges should not be promoted immediately. They should be used to guide research design and to test whether conditional-alpha construction can be evaluated without weakening the official validation framework.

## 9. Explicit Non-Goals

Project Underdog is not currently:

- A live trading system.
- A guarantee of outperformance.
- A backtest metric maximization exercise.
- A process for forcing alpha survivors.
- A reason to relax gates when a signal is interesting but unstable.

The platform is a research system, and its first responsibility is disciplined validation.

## 10. Closing Summary

Project Underdog has evolved from broad signal expansion toward a more nuanced research framework. Batch 1 showed which broad signals were unstable. Batch 2 showed that simple refinements do not necessarily fix WFV failure modes. Batch 3 showed that some effects are conditional, but also that sparse active states require different diagnostics and careful interpretation.

The current state is healthy: the platform rejects unstable edges, preserves strict gates, and now has better tools for understanding why signals fail. The next research step is not to force conditional signals into the existing alpha path, but to design a separate conditional-alpha research framework that can evaluate state-dependent behavior without compromising the conservative validation structure.
