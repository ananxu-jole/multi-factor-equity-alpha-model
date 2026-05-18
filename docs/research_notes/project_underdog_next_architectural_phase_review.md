# Project Underdog Next Architectural Phase Review

## Executive Summary

Project Underdog has reached a useful strategic inflection point. The platform has moved from broad signal discovery into a validation-first research system with modular engines, orchestration runners, cache-aware scoring, parity checks, and increasingly rich diagnostic artifacts.

The recent Batch 1-4 sequence clarified the core research reality:

- Universal signals are rare and weak under strict WFV.
- Conditional edges exist, but many are sparse, episodic, or directionally unstable.
- LOW_BREADTH selectively improved trend-quality behavior enough to pass the signal research stack.
- `smooth_trend_persistence_60_low_breadth` reached the alpha pool and entered constructed alphas.
- The downstream stress/survivor path still did not produce a `PROMOTE_CORE` survivor.

The recommended next architectural phase is **Conditional-Alpha Framework Design**.

This should not relax current gates or replace official WFV. It should add a research-only construction and diagnostic layer that studies how conditional signals behave after blending, activation, inactive-date handling, smoothing, turnover control, stress testing, and survivor review.

## Current Platform Architecture

Project Underdog is now organized around extracted modular engines and stage-specific runners rather than monolithic notebooks.

Current strengths:

- `src/scoring/` contains extracted engines for signal scoring, WFV, decay, regime IC, health, reproducibility, diversity, diagnostics, panel caching, and daily IC caching.
- `pipelines/` contains orchestration runners for stages 03 through 09 and sidecar research diagnostics.
- `pipelines/checks/` provides parity checks across major extracted stages, preserving confidence that modularized engines match expected behavior.
- Panel cache and daily IC cache reduce repeated compute cost for iterative scoring and diagnostics.
- Research artifacts are now first-class outputs under `artifacts/research/`.
- `docs/research_notes/` has become the research memory layer, capturing Batch 1-4, WFV diagnostics, Conditional Edge Atlas, active-state WFV, alpha-pool admission, and survivor-freeze diagnostics.

The architecture has good separation between official validation tables and research-only diagnostic artifacts. That separation should be preserved.

## Research Model Taxonomy

### Universal Signal Path

Universal signals are expected to be broadly active and robust across standard WFV windows. They follow the official path:

- structural quality
- 03 scoring
- 03C decay
- 03D regime diagnostics
- 03E health
- 03F reproducibility
- 03G diversity
- alpha pool
- alpha construction
- constructed-alpha WFV
- stress
- survivor freeze
- portfolio construction

This path remains appropriate for broad, persistent signals. It should remain conservative.

### Conditional Signal Path

Conditional signals depend on explicit OHLCV-only market states such as downtrend, high drawdown, high volatility, LOW_BREADTH, or low participation.

The current system can implement and evaluate conditional signals, but the official path still largely interprets them through universal-signal assumptions. Batch 4 showed that a conditional signal can pass signal-level WFV and reach alpha construction, yet still fail to become part of a core survivor after construction and stress.

### Sparse Episodic Edge Path

Sparse episodic edges show strong behavior only in rare states or isolated windows. Active-state diagnostics can make them look compelling, but they often lack enough active-window coverage to support robust promotion.

These should remain research watchlist items unless a future conditional-alpha framework defines explicit active-date, active-window, and one-window-dominance standards.

### Active-State WFV Diagnostics

Active-state WFV is a sidecar diagnostic that evaluates conditional signals only during active-condition dates while preserving official WFV as the formal gate.

Its value is explanatory:

- identifies inactive-window dilution
- measures active-window coverage
- separates sparse conditional edges from unstable edges
- detects one-window dominance

It should remain research-only until a formal conditional-alpha governance model exists.

### Alpha Construction Path

The current alpha construction path blends selected signals into constructed alphas using broad research recipes, dynamic weighting, smoothing, and turnover-aware variants.

Batch 4 showed that this layer can absorb conditional signals, but it does not yet explicitly preserve or evaluate conditional activation logic as a first-class alpha construction concept. Conditional signal behavior can be diluted, transformed, or paired with unrelated components.

### Stress / Survivor / Portfolio Path

The current 07/08/09 path is correctly conservative:

- constructed alphas must survive stress
- stress survivors must meet pass-rate, turnover, degradation, and score standards
- survivor freeze promotes only sufficiently strong core candidates
- portfolio construction expects final `PROMOTE_CORE` survivors

The survivor-freeze diagnostic showed the latest sole stress-approved alpha became `REVIEW_SATELLITE`, not `PROMOTE_CORE`, because it had pass rate `0.777778`, moderate turnover, survivor score `28.377197`, and degradation near the catastrophic boundary.

This is evidence that the platform is behaving as intended.

## Recent Research History

### Batch 1 Broad Expansion

Batch 1 tested seven proposed signals. Six passed structural quality and one, `downside_vol_asymmetry_20`, failed due to insufficient finite coverage. The strongest broad candidates included `trend_consistency_20_60`, `index_relative_reversal_5`, `percentile_rank_stability_20`, and `smooth_trend_persistence_60`.

Controlled WFV rejected the two primary bridge candidates:

- `trend_consistency_20_60`: weak effective IC, low persistence, low sign consistency
- `index_relative_reversal_5`: direction flip, weak effective IC, weak effective IC IR

No Batch 1 signal reached 04A eligibility.

### Batch 2 Refinement

Batch 2 refined the strongest failed Batch 1 ideas using simple variants:

- `trend_consistency_20_60_persistent`
- `index_relative_reversal_5_vol_adj`
- `index_relative_reversal_5_confirmed`

All passed structural quality, but only the trend variant reached `WATCHLIST`. Controlled WFV rejected it for weak effective IC, weak effective IC IR, low persistence, and low sign consistency.

Batch 2 showed that small mechanical refinements did not solve the core WFV failure modes.

### Batch 3 Conditional Diagnostics

Batch 3 changed the research question from "Which signal works universally?" to "Where does each signal work or fail?"

The diagnostics identified promising conditional contexts, especially:

- downtrend trend-quality behavior
- high-drawdown trend and reversal behavior
- stress-like conditions with stronger effective IC

The follow-on active-state diagnostics showed that some apparent conditional edges were sparse, inactive-window diluted, or one-window dominated. That clarified the difference between conditional promise and promotable robustness.

### LOW_BREADTH Audit

Conditional Edge Atlas v1 showed that LOW_BREADTH was a recurring conditional state with enough evidence to justify a narrow Batch 4 test. The LOW_BREADTH audit treated it as a primary conditional research state, not a promotion shortcut.

The audit supported testing trend-quality behavior under weak participation while keeping candidate count small.

### Batch 4 LOW_BREADTH Validation

Batch 4 implemented:

- `failed_breakout_reversal_20_low_breadth`
- `smooth_trend_persistence_60_low_breadth`

Both passed structural quality and reached `APPROVED_FOR_WFV` at h20 in 03 scoring. Controlled signal WFV rejected failed-breakout reversal but approved `smooth_trend_persistence_60_low_breadth`.

The smooth trend LOW_BREADTH candidate then:

- passed 03E health with score 87 at h20
- passed 03F reproducibility as `GLOBAL_PASS`
- passed 03G diversity selection
- reached `alpha_signal_pool_current`
- entered 14 constructed alpha definitions

This validated the conditional research path at the signal-to-alpha-construction boundary.

### Alpha Pool And Survivor Diagnostics

The alpha-pool diagnostic clarified that `smooth_trend_persistence_60_low_breadth` did reach the alpha pool and entered constructed alphas. It was not blocked at signal admission.

The survivor-freeze diagnostic then showed that the sole 07 stress-approved survivor was:

- `alpha_orthogonal_diversifier_v2_score_weighted_smooth h20`

That alpha did not include `smooth_trend_persistence_60_low_breadth`, and it became `REVIEW_SATELLITE`, not `PROMOTE_CORE`.

Batch 4 therefore validated the conditional research path but did not produce a core survivor.

## Key Lessons Learned

- Universal signals are rare and weak under strict validation.
- Conditional edges exist, but they must be interpreted with active-window and direction-stability context.
- Sparse conditional edges require separate diagnostics and should not be forced through universal promotion logic.
- LOW_BREADTH selectively stabilizes trend-quality behavior, especially for `smooth_trend_persistence_60`.
- Direction flip risk remains the dominant signal-level failure mode.
- Weak effective IC IR, low persistence, and low sign consistency remain important WFV rejection signals.
- Strict WFV, health, reproducibility, stress, and survivor gates are working as intended.
- Current alpha construction can include conditional signals, but it remains mostly universal-alpha oriented.
- Stress and survivor-freeze layers correctly require more than signal-level promise.
- Failed signals have been useful evidence, not wasted experiments.

## Current Bottlenecks

### Research Bottlenecks

- Too many candidate ideas can be generated faster than they can be interpreted.
- Conditional evidence is not yet organized into construction-ready hypotheses.
- Direction flips remain common, especially in reversal and conditional stress signals.
- The platform needs better attribution from conditional signal behavior to constructed-alpha behavior.

### Architecture Bottlenecks

- Conditional activation metadata is not yet first-class in alpha construction.
- Active-state diagnostics exist at the signal level but not as a full constructed-alpha research layer.
- There is no explicit conditional-alpha object or sidecar table that records active state, inactive-date treatment, and conditional construction intent.
- Research artifacts are rich but increasingly fragmented across separate notes and CSV outputs.

### Validation Bottlenecks

- Official WFV is correctly conservative but not explanatory enough for sparse conditional edges on its own.
- Active-state WFV remains diagnostic-only and has no connection to constructed-alpha stress attribution.
- 07/08 outputs do not yet explain how much a conditional component helped or hurt a constructed alpha during stress.
- There is no formal distinction between broad-core candidates and conditional-satellite candidates.

### Runtime Bottlenecks

- Panel cache and daily IC cache help, but broad diagnostics across signal x horizon x state remain expensive.
- Full downstream runs from signal research through alpha construction and stress can become costly when repeated frequently.
- Conditional atlas and active-state diagnostics should be used selectively rather than rerun after every small idea.

### Portfolio / Survivor Bottlenecks

- The survivor path is intentionally designed around broad `PROMOTE_CORE` alphas.
- `REVIEW_SATELLITE` is tracked but does not yet have a dedicated research or portfolio framework.
- Portfolio construction expects final core survivors and broad continuous alpha panels.
- Conditional or episodic alphas are structurally disadvantaged unless converted into robust broad constructed alphas.

## Architectural Options

### A. More Conditional Signal Expansion

Pros:

- Easy to continue.
- Can explore additional states and formulas.
- Uses existing 03 stack.

Cons:

- Risk of generating more watchlist candidates without solving the construction bottleneck.
- Does not explain why conditional signal success disappears downstream.
- May increase research clutter.

Assessment: useful later, but not the primary next phase.

### B. Conditional-Alpha Framework Design

Pros:

- Directly addresses the Batch 4 result.
- Studies how conditional signals should be combined, activated, neutralized, and stress-tested.
- Keeps official gates intact while creating a research-native path for conditional alphas.
- Provides the missing bridge between signal-level conditional evidence and constructed-alpha survival.

Cons:

- Requires careful design to avoid becoming an implicit promotion bypass.
- Needs clear separation from production portfolio logic.

Assessment: best primary next phase.

### C. More Active-State WFV Tooling

Pros:

- Improves understanding of sparse active states.
- Helps classify one-window dominated and inactive-window diluted edges.

Cons:

- Signal-level active-state diagnostics already exist.
- More tooling without construction attribution may not answer the next strategic question.

Assessment: important supporting work inside the conditional-alpha phase.

### D. Moderate Universe Expansion

Pros:

- More names may improve cross-sectional IC estimation.
- Could reduce sample noise in conditional states.

Cons:

- Expands runtime and data-quality burden.
- May obscure current architecture questions.
- Should wait until conditional-alpha evaluation is cleaner.

Assessment: premature as the primary next phase.

### E. Portfolio / Satellite Framework

Pros:

- Directly addresses `REVIEW_SATELLITE` outputs.
- Could formalize non-core research candidates.

Cons:

- Risks moving too close to allocation before conditional-alpha validation is mature.
- Satellite portfolio logic could become a backdoor around strict core-survivor discipline.

Assessment: valuable after conditional-alpha diagnostics mature.

### F. Dashboard / Reporting Layer

Pros:

- Would improve navigation and operational awareness.
- Useful as artifacts multiply.

Cons:

- Does not solve the core research bottleneck.
- Better reporting is helpful but secondary.

Assessment: useful support work, not primary phase.

### G. ML Preparation

Pros:

- ML may eventually help model interactions, regimes, and nonlinear conditional behavior.

Cons:

- Current signal taxonomy and conditional-alpha target definition are not mature enough.
- ML would risk overfitting unless labels, validation, and feature lineage are stabilized first.

Assessment: not yet.

## Recommended Next Phase

The recommended next architectural phase is:

## Conditional-Alpha Framework Design

This phase should design a research-only framework for constructing, diagnosing, and stress-attributing conditional alphas without changing official promotion gates.

The reason is simple: Batch 4 proved that a conditional signal can pass the signal stack and enter alpha construction, but the current architecture cannot yet clearly answer how that conditional signal helps or hurts constructed-alpha survival.

The next phase should therefore focus on:

- conditional activation metadata
- active-state-aware constructed-alpha diagnostics
- inactive-date treatment comparisons
- component attribution during constructed-alpha WFV and stress
- conditional satellite research classification
- clear non-promotion boundaries

This is the narrowest architectural move that directly addresses the latest evidence.

## Phased Roadmap

### Immediate Next Task

Create a research-only design document for a Conditional-Alpha Framework v1.

It should define:

- conditional alpha taxonomy
- required metadata
- inactive-date handling options
- active-state constructed-alpha diagnostics
- component contribution attribution
- stress attribution by active state
- review-only outputs
- explicit non-goals and no-promotion guarantees

No implementation should begin until the design is clear.

### Next 3-5 Engineering / Research Tasks

1. Build a constructed-alpha component attribution diagnostic for Batch 4 alphas that included `smooth_trend_persistence_60_low_breadth`.
2. Extend active-state diagnostics from raw signals to constructed alphas, research-only.
3. Compare inactive-date treatments for conditional components: neutral zero, NaN/exclusion, carry-neutral, and active-only scoring.
4. Create a conditional alpha audit table under `artifacts/research/` that links signal components, active states, WFV windows, stress cases, and survivor outcomes.
5. Write a satellite research classification note distinguishing `CORE_ALPHA`, `REVIEW_SATELLITE`, conditional satellite, and sparse episodic watchlist concepts.

### What Not To Do Yet

- Do not relax WFV, 03E, 03F, 03G, 07, or 08 gates.
- Do not force `REVIEW_SATELLITE` alphas into portfolio construction.
- Do not run broad Batch 5 signal expansion before understanding conditional construction behavior.
- Do not expand the stock universe as the next primary move.
- Do not begin ML modeling yet.
- Do not treat active-state WFV as an official promotion path.
- Do not create live or production portfolio logic for conditional alphas.

### Criteria For Expanding Signal Families

Expand signal families only when:

- conditional-alpha diagnostics can show whether a component survives or is diluted after construction
- at least one conditional state has repeatable active-window coverage across multiple signals
- direction-flip diagnostics are stable enough to avoid generating many avoid/watchlist rows
- research notes and artifacts can summarize the existing state without ambiguity

### Criteria For Expanding Stock Universe

Expand the stock universe only when:

- current-cache performance is stable under the existing universe
- conditional diagnostics have defined active-date and active-window sufficiency standards
- data-quality checks can handle a broader universe without increasing missingness-driven false failures
- runtime budgets for 03 through 08 are predictable
- the research question requires more cross-sectional breadth rather than better architecture

### Criteria For Beginning ML

Begin ML preparation only when:

- signal taxonomy is stable
- conditional-alpha labels are well defined
- active-state diagnostics have clear research labels
- leakage controls are documented
- WFV and stress targets are explicit
- baseline non-ML conditional-alpha diagnostics are already informative

ML should model a mature research problem, not compensate for unclear validation design.

## Top 5 Action Items

1. Write the Conditional-Alpha Framework v1 design note.
2. Build constructed-alpha active-state attribution diagnostics for Batch 4 LOW_BREADTH components.
3. Audit how inactive-date handling changes constructed-alpha WFV and stress interpretation, research-only.
4. Define a satellite research taxonomy that keeps `REVIEW_SATELLITE` separate from `PROMOTE_CORE`.
5. Consolidate Batch 1-4 and Conditional Edge Atlas findings into a compact decision matrix for future Batch 5 candidate selection.

## Explicit Do Not Do Yet List

- Do not relax gates.
- Do not create a promotion path from active-state WFV.
- Do not force conditional alphas into `PROMOTE_CORE`.
- Do not run 04A+ solely to chase a survivor.
- Do not expand to a large universe yet.
- Do not launch broad signal-family expansion yet.
- Do not begin ML until conditional-alpha labels and validation targets are stable.
- Do not build portfolio allocation logic for sparse episodic edges.

## Closing Recommendation

Project Underdog is in a healthy research state. The platform is rejecting unstable edges, preserving strict validation discipline, and producing better explanations for why signals fail.

The most valuable next move is not more raw signals. It is a research-only Conditional-Alpha Framework that explains whether conditional signals can be transformed into robust constructed alphas without weakening the official universal/core survivor path.

That phase aligns with the evidence from Batch 1-4 and preserves the core philosophy of the project: robustness first, no forced survivors, and failed signals as useful information.
