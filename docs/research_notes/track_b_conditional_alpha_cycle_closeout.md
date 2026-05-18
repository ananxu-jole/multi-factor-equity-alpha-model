# Track B Conditional-Alpha Cycle Closeout

## Executive Takeaway

Track B completed its first successful robustness-first conditional-alpha research cycle. The cycle did not produce a universal standalone alpha, but it did produce the first formally governed conditional-alpha review candidate from the Track B discovery process:

`participation_liquidity_state_shift_20_60` -> `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

The approved research representation is intentionally narrow:

| role | variant |
|:--|:--|
| Primary | `rank_persist_10_state_TREND_HOSTILE_zero` |
| Backup / state confirmation | `rebalance_10_state_WEAK_BREADTH_zero` |
| Stress confirmation | `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero` |
| Broad fallback / control | `rebalance_20` |

No production registration occurred. No survivor/watchlist promotion occurred. No portfolio integration, ML integration, gate change, schema change, or production Conditional-Alpha wiring occurred.

The central research lesson is that discovery can now move faster without becoming loose: the platform rejected reversal clones, diagnosed continuation failures, redesigned mechanisms instead of simply inverting them, isolated a conditional liquidity/participation state-shift edge, and carried it through refinement, validation, and integration review with explicit guardrails.

## Scope And Non-Changes

This closeout is a research milestone document only. It consolidates the Track B cycle and defines the next conceptual frontier.

The following were not changed:

- production signal factory registration
- official gates, thresholds, or schemas
- survivor/watchlist state
- alpha construction or portfolio logic
- ML logic
- production Conditional-Alpha paths
- Track A governance status for `volume_shock_reversal_stable_20`

## Track B Chronology

| stage | artifact / note | outcome | main lesson |
|:--|:--|:--|:--|
| v2 robustness-first discovery | `robustness_first_discovery_expansion_v2` | 11 candidates tested; 4 `WATCHLIST_RESEARCH`; 7 `REJECT_RESEARCH`; no clean further-validation promotions | Many apparently new ideas collapsed into a latent reversal-like manifold. |
| v3 orthogonal redesign | `robustness_first_discovery_expansion_v3` | 15 candidates tested; all `REJECT_RESEARCH` | Naive continuation, leadership, and rank-quality structures did not survive empirical direction checks. |
| v3 failure diagnostics | `track_b_v3_failure_diagnostics` | No broad construction sign bug found | Direction mismatch was mostly overextension / late-entry momentum decay plus price-rank redundancy; simple inversion would create reversal proxies. |
| v4 mechanism redesign | `robustness_first_discovery_expansion_v4` | 12 candidates tested; 4 `CONDITIONAL_ONLY_RESEARCH`; 8 `REJECT_RESEARCH` | Mechanism redesign reduced reversal similarity but did not create a standalone alpha. |
| v4 conditional diagnostics | `track_b_v4_conditional_diagnostics` | `participation_liquidity_state_shift_20_60` became `CONDITIONAL_REFINEMENT_CANDIDATE` | The useful structure was conditional, especially in hostile trend, weak breadth, drawdown, and liquidity-stress states. |
| focused refinement | `participation_liquidity_state_shift_refinement` | 68 variants tested; 18 met the internal research-ready profile | Turnover was mostly rank churn; smoothing, rebalance, and rank-persistence controls improved behavior without merely suppressing exposure. |
| conditional validation | `participation_liquidity_conditional_validation` | 18 selected variants tested; 4 passed stricter validation | The edge survived stricter review, but as a state-dependent candidate rather than a universal standalone alpha. |
| integration review | `participation_liquidity_conditional_alpha_integration_review` | Final classification: `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | A fixed four-variant package is ready for research-only conditional-alpha integration review, not production use. |

## Major Discoveries

The reversal manifold is real and powerful. v2 showed that liquidity shocks, residual/value decay, turnover decay, volatility surprise, and some interaction ideas can look different in formula form while still behaving like the same underlying reversal exposure.

Continuation failed for structural reasons, not because the code was broadly signed wrong. v3 failure diagnostics showed that long-continuation intent often produced negative h20 IC because the signals entered after overextension or after momentum had already decayed.

Mechanism redesign improved structural distance. v4 reduced price-rank and reversal similarity for several gap, liquidity, range-expansion, and non-price designs. That was progress even though standalone alpha strength was not sufficient.

The useful Track B edge was conditional. `participation_liquidity_state_shift_20_60` was not strong enough as an always-on standalone signal, but improved materially in hostile trend, weak breadth, drawdown, panic/liquidity stress, and low-dispersion states.

Turnover can be diagnosed more precisely now. For the successful candidate, high turnover was traced mainly to rank churn rather than activation noise. This made rebalance, smoothing, and rank-persistence variants credible refinements rather than cosmetic de-risking.

## Major Failures

Naive continuation and mature leadership structures failed repeatedly. `trend_leadership_persistence_20_60`, `relative_strength_acceleration_20_60`, and related v3/v4 leadership concepts generally showed direction mismatch, especially around h20.

Simple inversion was rejected as a research shortcut. Inverting failed continuation candidates would mostly recreate reversal-like exposures rather than create a new mechanism.

Several orthogonal-looking signals were still too weak. `gap_followthrough_low_churn_10` and `nonprice_liquidity_persistence_20_60` were more structurally distinct, but did not yet provide enough stable standalone evidence.

Breakout and range-expansion structures remained fragile. Cleaner confirmation reduced some noise, but these mechanisms still showed weak persistence, narrow state dependency, or wrong always-on direction.

Over-refinement risk became visible. The successful Track B candidate required a focused refinement search, so the final package must remain fixed and small. Related variants should be treated as confirmation, not as independent alpha sleeves.

## Candidate Lifecycle: `participation_liquidity_state_shift_20_60`

The candidate began in v4 as a mechanism redesign around joint participation and liquidity improvement, neutralized against 20-day return rank. It was designed to avoid the v3 failure mode where liquidity improvement was effectively multiplied by price-rank momentum.

### v4 Base Discovery

Initial v4 status: `CONDITIONAL_ONLY_RESEARCH`.

Key base evidence:

- best horizon: h20
- h20 mean IC: `0.008421`
- WFV-style persistence / sign consistency: `0.75 / 0.75`
- max baseline correlation: `0.469409`
- turnover proxy: `0.216332`
- main issue: high turnover and weak always-on strength

### v4 Conditional Diagnostics

Status upgraded to `CONDITIONAL_REFINEMENT_CANDIDATE`.

Conditional slices improved meaningfully in:

- `TREND_HOSTILE`
- `LOW_DISPERSION`
- drawdown acceleration
- panic / liquidity stress
- weak participation breadth

Turnover diagnostics showed rank churn rather than activation noise. The broad `rebalance_10` variant improved h20 mean IC to `0.016518` and reduced turnover by about `72.6%`.

### Focused Refinement

Status upgraded to `CANDIDATE_FOR_CONDITIONAL_VALIDATION`.

The refinement pass tested 68 variants. Eighteen variants met the internal research-ready profile. The strongest variants included:

| variant | h20 mean IC | turnover | notes |
|:--|--:|--:|:--|
| `rank_persist_10_state_TREND_HOSTILE_zero` | `0.028418` | `0.096397` | strongest conditional variant; WFV-style persistence/sign consistency `1.00 / 1.00` |
| `smooth_5_state_TREND_HOSTILE_zero` | `0.027996` | `0.059567` | strong hostile-trend behavior with lower turnover |
| `rebalance_10_state_WEAK_BREADTH_zero` | `0.024410` | `0.054555` | clean weak-breadth semantics; baseline corr `0.198669` |
| `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero` | `0.024213` | `0.059223` | stress/weak-breadth confirmation |
| `rebalance_20` | `0.021234` | `0.032973` | broad fallback/control; active coverage `0.980934` |

### Formal Conditional Validation

Status upgraded to `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`.

Eighteen selected variants were tested under stricter validation. Four passed:

1. `rank_persist_10_state_TREND_HOSTILE_zero`
2. `rebalance_10_state_WEAK_BREADTH_zero`
3. `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero`
4. `rebalance_20`

Strongest validated variant:

- `rank_persist_10_state_TREND_HOSTILE_zero`
- h20 mean IC: `0.028418`
- turnover: `0.096397`
- active coverage: `0.346997`
- WFV-style effective IC IR: `2.623031`
- persistence / sign consistency: `1.00 / 1.00`
- baseline corr: `0.269307`

### Integration Review

Final status: `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

Recommended representation:

- use `rank_persist_10_state_TREND_HOSTILE_zero` as the primary conditional variant
- use `rebalance_10_state_WEAK_BREADTH_zero` as state confirmation
- use `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero` as stress confirmation
- use `rebalance_20` only as a broad fallback/control

Required guardrails include parameter lock, semantic preservation, rebuild/equivalence testing, active-state coverage review, turnover ceiling, similarity ceiling, peer-similarity review, one-window dominance monitoring, rollback triggers, and a hard production boundary.

## Research Inventory

| item | current research status | role | next action |
|:--|:--|:--|:--|
| `participation_liquidity_state_shift_20_60` | `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | First governed Track B conditional-alpha review candidate | Freeze fixed four-variant package; next step is design-only rebuild/equivalence planning if integration review continues. |
| `nonprice_liquidity_persistence_20_60` | `CONDITIONAL_ONLY_KEEP` | Secondary non-price liquidity ingredient | Hold for future conditional design; do not broaden without a stronger state thesis. |
| `conditional_low_overextension_breakout_20` | `REDESIGN` | Breakout/low-overextension concept | Redesign only if activation semantics and persistence can be improved. |
| `gap_followthrough_low_churn_10` | `REDESIGN` | Gap-followthrough concept | Redesign only with cleaner event coverage and lower turnover. |
| v2 watchlist names | `WATCHLIST_RESEARCH` only | Earlier robustness-first references | Keep as reference/baseline material; do not promote from this closeout. |
| `volume_shock_reversal_stable_20` | Track A governed candidate with review items | Controlled registration governance baseline | Remains separate from Track B; no portfolio use or survivor/watchlist mutation. |

## Research Maturity Assessment

### What The Framework Can Now Do Reliably

- Run isolated discovery batches with separate artifacts and research notes.
- Identify when candidate novelty is superficial because of high baseline similarity.
- Diagnose direction mismatch before creating the next batch.
- Distinguish sign bugs from empirical direction failure.
- Avoid simple inversion when inversion would recreate reversal exposure.
- Separate activation noise from rank churn in turnover diagnostics.
- Move from broad discovery to conditional diagnostics, refinement, validation, and integration review.
- Carry forward guardrails without relaxing official gates or production logic.

### Remaining Weaknesses

- Conditional-alpha construction remains research-only and is not a production pathway.
- Refinement search can create selection risk unless fixed candidate sets are frozen early.
- Peer similarity among conditional variants can make an ensemble look more diversified than it is.
- State labels need semantic preservation and rebuild/equivalence testing before any deeper integration work.
- The current evidence is still universe- and period-specific.
- Some mechanisms have improved orthogonality but insufficient standalone strength.

### Remaining Unknowns

- Whether the participation/liquidity state-shift edge survives a clean rebuild from frozen definitions.
- Whether active-state behavior remains robust under a broader universe.
- Whether conditional-alpha construction can preserve the edge after blending, stress testing, and portfolio constraints.
- Whether future non-price liquidity and participation-breadth mechanisms can produce a second independent conditional edge.
- Whether state-gated alpha layers can be designed without over-fragmented regime slicing.

## Architectural Lessons

The discovery architecture is now mature enough to accelerate, but only when acceleration is paired with evidence triage. The most useful architecture pattern was not a larger search; it was a loop:

Discover -> diagnose failure -> redesign mechanism -> isolate conditional behavior -> refine turnover -> validate fixed variants -> govern representation.

This loop is now a reusable Track B template.

The system also showed that governance can remain separate from discovery. Track A kept `volume_shock_reversal_stable_20` under controlled governance while Track B explored new standalone and conditional mechanisms. That separation should continue.

## Reversal-Manifold Lessons

Many candidates that appear economically different are statistically close to reversal once scored cross-sectionally. This includes residual mispricing decay, volume-shock structures, turnover-decay quality, volatility-reversal variants, and some interaction candidates.

Future discovery should treat high reversal similarity as a default risk, not an occasional exception. Candidate design should begin with a statement of why the mechanism is not simply:

- price moved too much, so fade it
- rank is high, so continuation should work
- rank is high, so invert it
- liquidity changed after price moved, so fade it

## Conditional-Alpha Lessons

Conditional edges can be real without being universal alphas. `participation_liquidity_state_shift_20_60` became interesting only after hostile-trend, weak-breadth, and stress-style state conditioning.

The broad fallback `rebalance_20` is useful as a control, but should not be treated as proof that the signal is a universal alpha. The primary evidence remains state-dependent.

Conditional variants should be represented as one primary plus confirmations, not as a large ensemble. The variants are related and high peer similarity is expected.

## Turnover And Rank-Churn Lessons

High turnover is not always caused by activation transitions. For `participation_liquidity_state_shift_20_60`, rank churn was the central issue. This made rebalance, smoothing, and rank-persistence controls economically coherent.

Turnover refinement should be judged by whether it preserves direction and state semantics. The best refinements reduced churn while maintaining or improving h20 behavior, suggesting that the original signal contained information but expressed it noisily.

## Orthogonality Findings

Orthogonality improved when v4 moved away from direct price-rank continuation. Gap, non-price liquidity, clean range, and participation/liquidity mechanisms showed lower baseline similarity than many v2 structures.

However, orthogonality alone was not enough. Several structurally distinct candidates were too weak, too noisy, too turnover-sensitive, or too state-specific to qualify as standalone alphas.

The strongest path combined moderate-low baseline similarity with a coherent conditional state thesis and turnover control.

## Mechanisms That Repeatedly Failed

- naive long continuation after mature leadership
- relative strength acceleration after price extension
- breakout follow-through without enough state filtering
- gap continuation without strong event-quality controls
- volatility compression or expansion features that behaved like delayed reversal
- price-rank-heavy liquidity improvement
- dispersion transition features that still mapped to broad price-rank behavior

## Mechanisms That Survived

- participation/liquidity state shift under hostile trend, weak breadth, and stress-style states
- non-price liquidity persistence as a weak but orthogonal conditional-only ingredient
- gap and breakout concepts only as redesign candidates, not as current alphas
- broad rebalance/smoothing controls when used as churn reduction rather than exposure suppression

## Recommended Next Research Frontier

Do not launch a broad v5 search immediately. The next step should be a design-only mechanism thesis map that narrows future discovery before implementation.

Recommended frontier priorities:

1. Conditional participation breadth structures  
   Closest to the successful Track B mechanism. Focus on participation quality before price extension and on state-specific activation rather than always-on continuation.

2. Non-price liquidity state transitions  
   Build around liquidity persistence, deterioration, and improvement without multiplying by price rank. Preserve the non-price identity explicitly.

3. Market-state transition signals  
   Study transitions into and out of hostile trend, weak breadth, drawdown, panic/liquidity stress, and low-dispersion states. Avoid excessive slicing.

4. Cross-sectional stability transitions  
   Look for changes in rank stability, dispersion, and participation before acceleration. Avoid mature leadership chasing.

5. Event-quality structures  
   Revisit gaps and breakouts only when missingness, event quality, and turnover controls are designed first.

6. Temporal asymmetry signals  
   Explore whether up/down participation, liquidity, or range behavior has asymmetric information across windows without collapsing into reversal.

7. Conditional interaction mechanisms  
   Combine two simple primitives only when each contributes a distinct mechanism. Avoid blend camouflage.

8. Regime-aware ranking systems and state-gated orthogonal alpha layers  
   Treat these as architecture design topics before implementation. Do not convert them into production paths without separate review.

## Do Not Repeat

- Do not repeat naive continuation after overextended leadership.
- Do not simply invert failed continuation signals.
- Do not use price-rank redundancy and call it orthogonality.
- Do not create pseudo-orthogonal variants that differ in formula but share the same latent reversal exposure.
- Do not over-fragment state slices until sample size and active-window coverage are proven.
- Do not run excessive refinement searches without freezing a small candidate set afterward.
- Do not treat a broad fallback/control as a validated universal alpha.
- Do not treat highly correlated conditional variants as independent ensemble members.
- Do not merge Track A governance artifacts with Track B discovery artifacts.

## Recommended Next Step

Create a Track B v5 concept-screening note before implementing any new candidates. The concept screen should define a small set of mechanism theses around conditional participation breadth, non-price liquidity state transitions, and market-state transitions, then reject weak theses on paper before any code is written.

If the `participation_liquidity_state_shift_20_60` integration path continues, the next step should be a separate research-only rebuild/equivalence test plan for the fixed four-variant package. That work should remain separate from new Track B discovery.

The correct posture after this milestone is: freeze the successful conditional package, preserve the guardrails, and design the next discovery frontier deliberately rather than launching a large search immediately.
