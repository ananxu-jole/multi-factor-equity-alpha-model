# Project Underdog - Event Clustering Research Module Design v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 1B - Research Module Design

Classification: `DESIGN_READY_WITH_NOTES`

Recommendation: `ADVANCE_TO_FORMULA_AND_PANEL_SPECIFICATION_REVIEW`

Scope: design-only transformation of the approved Event Clustering scientific review into a disciplined Platform v2 research module.

This note does not recreate the scientific review. It does not implement code, write formulas, create candidate IDs, specify panels, generate panels, compute IC, run validation, modify governance, change production files, change thresholds, introduce ML, or modify Platform v2 methodology.

## SECTION 1 - Inputs And Boundary

Inputs reviewed:

- `docs/research_notes/event_clustering_scientific_review_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`
- prior Project Underdog research inventory as contamination context.

This design advances exactly one lifecycle phase after the approved scientific review:

- from Platform v2 Phase 1A - Scientific Hypothesis And Orthogonality Review;
- to Platform v2 Phase 1B - Research Module Design.

It does not advance to formula specification, panel specification, implementation, panel generation, IC discovery, validation, governance, production, threshold changes, or ML.

## SECTION 2 - Primary Scientific Objective

Frozen primary scientific objective:

Determine whether the temporal topology of clustered market events changes forward cross-sectional behavior beyond isolated events and beyond existing Project Underdog families.

The research object is market-event sequence structure: whether nearby related events create market memory that changes how the current event should be interpreted. The module should not become a broad event library, a volatility-state variant, a stress-repair variant, a volume-shock reversal variant, a rank-persistence variant, or a parked-family rescue.

The scientific question is:

Do nearby related events create market memory that changes the meaning of subsequent observed market behavior?

## SECTION 3 - Principal Scientific Mechanisms

The research program is narrowed to four principal mechanisms. These are scientific mechanisms only, not formulas, candidate IDs, panels, or implementation specifications.

### 1. Event Concentration

Event Concentration asks whether nearby related events differ from isolated events. One event may be noise; repeated nearby events may reveal a latent market process such as forced flow, staged information diffusion, liquidity withdrawal, or crowding.

Expected observable implication:

Clustered events should behave differently from otherwise similar isolated events. If concentrated events cannot be distinguished from isolated shocks, the primary mechanism fails.

Expected activation characteristic:

Activation should be episodic, tied to identifiable event bursts, and not so continuous that it becomes a proxy for ordinary volatility or volume.

### 2. Event Alignment And Fragmentation

Event Alignment And Fragmentation asks whether event types arriving together carry different information from event types arriving in conflict. Alignment suggests a coherent market process. Fragmentation suggests disagreement, absorption, false signal, or unsettled repricing.

Expected observable implication:

Aligned clusters and fragmented clusters should not be interchangeable. The distinction should matter because event-type structure, not just event count, is part of the hypothesis.

Expected activation characteristic:

Activation should occur when multiple event types are close enough in time to form a coherent or conflicted sequence. It should not be driven only by a single dominant event type.

### 3. Cluster Absorption Versus Deterioration

Cluster Absorption Versus Deterioration asks whether securities that withstand repeated event pressure differ from securities that degrade through repeated events. The mechanism is the response to repeated activation, not the existence of a cluster alone.

Expected observable implication:

Absorbed clusters should separate from deteriorating clusters in a scientifically interpretable way. If absorption is just rank coherence or deterioration is just stress persistence, the mechanism is contaminated.

Expected activation characteristic:

Activation should be concentrated around repeated event pressure where the security's behavior after the pressure can be interpreted as resilient, unresolved, or deteriorating.

### 4. Cluster Aging And Market Memory

Cluster Aging And Market Memory asks whether a fresh cluster, a persistent cluster, and a decaying cluster carry different implications. The age and decay of a cluster may reveal whether pressure remains unresolved, has been absorbed, or is exhausting.

Expected observable implication:

Cluster formation, persistence, and decay should have distinguishable behavior at the predeclared primary horizons. h20-only evidence would be suspect unless h5/h10 behavior is coherent.

Expected activation characteristic:

Activation should allow formation, persistence, and aging states to be interpreted without turning ordinary event recency into a broad timing search.

## SECTION 4 - Orthogonality Summary

Event Clustering is expected to be scientifically distinct only if event-arrival topology adds information beyond existing families.

| reference family | how Event Clustering differs | contamination action if reference explains evidence |
| --- | --- | --- |
| VoV | VoV concerns instability of volatility paths; Event Clustering concerns nearby event arrival structure across event types. | Reclassify or park if evidence is volatility-instability dominance. |
| Volatility Compression | Compression concerns volatility calming or level change; Event Clustering concerns event concentration, absorption, deterioration, and aging. | Reclassify or park if cluster decay is plain volatility compression. |
| Hostile/Stress Repair | Stress repair concerns recovery from damaged market states; Event Clustering asks whether repeated events create memory beyond the hostile state. | Park if evidence exists only inside hostile, panic, drawdown, weak-breadth, or liquidity-stress states. |
| Volume Shock Reversal | Volume shock reversal is shock/reversal oriented; Event Clustering requires sequence context across nearby events. | Reclassify if abnormal volume or single-event reversal explains the result. |
| Rank Coherence | Rank coherence concerns stable rank behavior; Event Clustering concerns repeated event arrival and response to the cluster. | Park or downgrade if stable ranks explain absorbed clusters. |
| Persistence | Persistence concerns prior relative state continuing; Event Clustering asks whether event sequence changes the meaning of that state. | Park or downgrade if prior winners, prior losers, or post-drawdown survivors explain the result. |
| Dispersion Path-Dependence | Dispersion Path-Dependence concerns market-wide disagreement sequence; Event Clustering concerns security-level event topology. | Park or downgrade if dispersion path or static disagreement explains the behavior. |
| Non-Hostile Transition | Non-Hostile Transition concerns orderly leadership or rotation behavior; Event Clustering does not require leadership transition. | Park if leadership-transition language is needed to explain the effect. |

## SECTION 5 - Expected Contamination Risks

Expected contamination risks:

- Volatility persistence or VoV dominance.
- Volatility compression masquerading as cluster aging.
- Hostile/stress repair dominance.
- Volume shock reversal or repeated short-horizon reversal dominance.
- Rank coherence explaining apparent absorption.
- Persistence explaining repeated-event behavior.
- Dispersion path-dependence or static dispersion explaining event clusters.
- Gap-event continuation or reversal dominating the evidence.
- One-window or crisis-window dominance.
- Sparse activation that prevents stable interpretation.
- Continuous activation that turns the design into ordinary volatility, volume, or stress measurement.
- Timing-integrity risk in later phases.

Contamination judgment:

The risk is high but manageable at design stage because the primary objective and four mechanisms are narrow. The next lifecycle phase must carry isolated-event comparators and existing-family contamination references, but this note does not specify panels or formulas.

## SECTION 6 - Expected Learning Objectives

Expected learning objectives:

1. Determine whether clustered events differ from isolated events.
2. Determine whether repeated activation changes expected market behavior.
3. Determine whether event-type alignment or fragmentation matters.
4. Determine whether absorption and deterioration after repeated events are distinct states.
5. Determine whether cluster aging and market memory matter at h5/h10.
6. Determine whether Event Clustering is independent, diagnostic-only, or redundant with existing families.

These objectives remain useful if results are negative. A clean failure would still clarify whether event behavior should remain a contamination reference rather than an active alpha-family frontier.

## SECTION 7 - Expected Observable Implications

If the hypothesis is true, later research should observe:

- clustered events differ from isolated events;
- temporal concentration carries information beyond event count alone;
- aligned and fragmented event sequences have different implications;
- absorbed and deteriorating clusters separate in interpretable ways;
- cluster age changes expected behavior;
- useful activation is not limited to hostile/stress states;
- event topology remains interpretable after comparison to volatility, volume, rank, persistence, dispersion, reversal, and leadership-transition references.

If the hypothesis is false, later research should show that clustered events are noisy, too sparse, too broad, one-window dominated, or explainable by existing families.

## SECTION 8 - Expected Activation Characteristics

Expected activation:

- episodic but not vanishingly rare;
- broad enough for cross-sectional interpretation;
- not continuous;
- not crisis-only;
- able to distinguish clustered from isolated events;
- able to distinguish aligned, fragmented, absorbed, deteriorating, fresh, persistent, and decaying cluster states at the design level;
- not dependent on hostile/stress states as the primary gate.

Activation should support a future 4-6 candidate target without requiring broad search or parameter expansion.

## SECTION 9 - Expected Primary Horizons

Expected primary horizons:

- h5;
- h10.

Expected secondary horizon:

- h20 as durability evidence only.

h20-only success should not rescue failed h5/h10 evidence. h1-only evidence should be treated as diagnostic, not as a basis for module advancement.

## SECTION 10 - Candidate Discipline For Future Phase

Platform v2 discipline preserved:

- one bounded refinement cycle maximum unless separately approved after research review;
- 4-6 future candidate target;
- hypothesis-first discipline;
- no horizon shopping;
- no target hacking;
- no broad search;
- no candidate generation from results;
- no expansion beyond the four principal mechanisms without a separate design amendment.

This note does not create candidate IDs and does not specify formulas, panels, artifacts, thresholds, or implementation details.

## SECTION 11 - Predefined Success Criteria

Predefined success criteria for later phases:

- primary-horizon evidence should align with the predeclared mechanism direction at h5 and/or h10;
- h20 should provide durability context only;
- clustered-event behavior should improve interpretation relative to isolated-event behavior;
- aligned and fragmented clusters should not be interchangeable;
- absorbed and deteriorating clusters should separate in a scientifically interpretable way;
- cluster aging should show market-memory behavior rather than plain volatility compression or stress repair;
- activation should be episodic, interpretable, and not one-window dominated;
- turnover and event churn should remain research-interpretable;
- contamination references should not dominate the mechanism;
- family-level success should require more than one distinct event-cluster expression, not near-duplicates of the same isolated-event effect.

## SECTION 12 - Predefined Stopping Criteria

The module should be parked, downgraded, or redesigned if later evidence shows:

- clustered events do not differ from isolated events;
- useful behavior is explained by VoV, volatility persistence, or volatility compression;
- useful behavior appears only in hostile/stress-repair states;
- volume shock reversal explains the event effect;
- rank coherence or persistence explains apparent absorption or repeated activation;
- dispersion path-dependence or static dispersion explains the cluster effect;
- leadership-transition logic is needed to interpret success;
- h5/h10 evidence fails while h20 is the only positive horizon;
- evidence requires post-hoc horizon switching;
- activation is too sparse, too continuous, or one-window dominated;
- timing integrity cannot be preserved in the later specification phase;
- future specification requires broad parameter search to become plausible.

These criteria must not be weakened after results are known.

## SECTION 13 - Classification

Classification: `DESIGN_READY_WITH_NOTES`

Rationale:

- The module has one frozen primary scientific objective.
- The mechanism set is narrow and suitable for a future 4-6 candidate target.
- Orthogonality risks are explicit against the required reference families.
- Contamination risks are material but predeclared.
- Learning objectives, observable implications, activation characteristics, horizons, success criteria, and stopping criteria are defined before formulas or panels.

Notes attached to readiness:

- Volume shock reversal and hostile/stress repair are the highest contamination risks.
- Rank coherence, persistence, VoV, volatility compression, dispersion path-dependence, and Non-Hostile Transition must remain active reference risks in the next phase.
- The next phase must remain formula and panel specification review only.

## SECTION 14 - Verification

Confirmed:

- No implementation.
- No formulas.
- No candidate IDs.
- No panel specification.
- No panel generation.
- No IC.
- No validation.
- No governance.
- No production.
- No threshold changes.
- No ML.

## SECTION 15 - Final Recommendation

Recommended next lifecycle phase:

- Platform v2 Phase 2 - Formula And Panel Specification Review.

Event Clustering may advance exactly one lifecycle phase to formula and panel specification review. It may not advance directly to implementation, panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
