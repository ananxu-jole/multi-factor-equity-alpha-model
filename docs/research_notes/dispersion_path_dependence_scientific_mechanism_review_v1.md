# Project Underdog - Dispersion Path-Dependence Scientific Mechanism Review v1

## SECTION 1 - Executive Summary

Classification: `MECHANISM_REVIEW_READY_WITH_NOTES`

This note inserts a Platform v2 scientific mechanism review between research module design and formula and panel specification for Dispersion Path-Dependence.

This is a science and design review only. It does not write formulas, create candidate IDs, specify panels, implement code, generate artifacts, compute IC, run validation, modify governance decisions, register production candidates, change thresholds, or introduce ML.

Review conclusion:

The Dispersion Path-Dependence module may proceed to formula and panel specification with notes. The scientific vocabulary is now frozen, and all five proposed mechanism concepts are acceptable for formula-specification translation if the future specification preserves the path-dependence requirement and predeclares contamination controls.

Mechanism-level decisions:

| mechanism concept | decision |
| --- | --- |
| Elevated Disagreement Stabilization | `ACCEPT_WITH_NOTES` |
| Disagreement Relapse Resilience | `ACCEPT_FOR_FORMULA_SPEC` |
| Consensus Formation Without Crowding | `ACCEPT_WITH_NOTES` |
| Disagreement Path Divergence | `ACCEPT_FOR_FORMULA_SPEC` |
| Smooth Versus Burst Resolution | `ACCEPT_WITH_NOTES` |

No concept is rejected. Three concepts carry notes because their natural language can drift into volatility compression, parked non-hostile transition, event clustering, volume shock reversal, or rank coherence if the future formula specification is careless.

## SECTION 2 - Lifecycle Placement

This document sits between:

- Research Module Design: `docs/research_notes/dispersion_path_dependence_research_module_design_v1.md`
- Formula and Panel Specification: future task, not performed here.

Lifecycle purpose:

- sharpen scientific vocabulary before formulas are written;
- challenge each proposed mechanism concept;
- decide whether each concept is precise enough to translate into a future formula;
- define mapping rules so every future formula maps to one clearly defined scientific mechanism.

This review is not:

- formula specification;
- candidate ID creation;
- panel specification;
- implementation;
- IC discovery;
- validation;
- governance decision;
- production registration.

## SECTION 3 - Materials Reviewed

Reviewed:

- `docs/research_notes/dispersion_path_dependence_scientific_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_research_module_design_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_family_diversification_refinement_execution_v1.md`
- `docs/research_notes/rank_coherence_refinement_execution_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_results_review_and_candidate_registration_recommendation_v1.md`
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_negative_result_review_v1.md`

Key constraint inherited from Platform v2:

Every future formula must map to one clearly defined scientific mechanism, not merely to a convenient indicator.

## SECTION 4 - Scientific Vocabulary Freeze

| term | accepted meaning | excluded meaning | contamination risk |
| --- | --- | --- | --- |
| disagreement | Cross-sectional disagreement in realized security outcomes or repricing behavior. | Generic uncertainty, single-name volatility, or market-wide fear. | Can become VoV, volatility level, or stress repair if not explicitly cross-sectional. |
| dispersion | The observable footprint of cross-sectional disagreement across securities. | A standalone alpha thesis or simple high/low state. | Can collapse into static dispersion level or prior dispersion anchors. |
| path dependence | The idea that the sequence leading to the current disagreement state changes its forward meaning. | A one-period change or static state label. | Can become simple acceleration, momentum, or level timing. |
| memory | Information contained in prior disagreement states that affects interpretation of the current state. | Long lookback persistence for its own sake. | Can become persistence or rank coherence. |
| persistence | Continued presence of disagreement across time. | Prior winners continuing or stable ranks. | Can become rank persistence if security rank behavior dominates disagreement path. |
| decay | Orderly fading of disagreement. | Volatility compression or simple reduction in risk. | Can become volatility compression if volatility level is the true driver. |
| stabilization | Disagreement remains elevated or recently elevated but becomes less chaotic. | Calm market state or low volatility alone. | Can become stress repair, VoV calming, or volatility compression. |
| normalization | Disagreement moves toward a more ordinary cross-sectional state after prior disorder. | Leadership continuation or broad recovery. | Can become parked non-hostile transition, stress repair, or momentum. |
| relapse | Disagreement re-expands after temporary calm or partial normalization. | Simple rising dispersion from any starting point. | Can become static dispersion acceleration or crisis-state detection. |
| consensus formation | Gradual convergence of investor beliefs or relative security repricing after disagreement. | Price momentum, stable rank leadership, or crowded leadership. | Can become rank coherence, persistence, or non-hostile leadership continuation. |
| leadership crowding | Mature or over-owned leadership behavior that may masquerade as orderly transition. | Any strong security or any winner. | Can contaminate consensus concepts and recreate parked non-hostile transition. |
| burst resolution | Abrupt reduction or reorganization of disagreement after a sharp repricing episode. | Volume shock reversal or one-day event reversal. | High risk of event clustering, volume shock reversal, or plain reversal contamination. |
| smooth resolution | Gradual convergence of disagreement without abrupt event dominance. | Low volatility, low churn, or calm market behavior alone. | Can become volatility compression or rank coherence. |
| divergence | Separation between disagreement path and another market-state path such as volatility, stress, or rank stability. | Any difference between two indicators. | Can become indicator engineering unless tied to a precise economic interpretation. |

Vocabulary rule:

Any future formula specification must use these meanings. If a proposed formula cannot explain which frozen term it operationalizes, it should not be included.

## SECTION 5 - Mechanism Concept Review

### 5.1 Elevated Disagreement Stabilization

Scientific question:

Do securities that remain orderly while market disagreement is elevated but stabilizing carry positive h5/h10 information?

Economic interpretation:

Elevated disagreement may reflect unresolved repricing. Stabilization while disagreement remains elevated may indicate that liquidity and consensus are improving before the full cross-section normalizes.

Behavioral interpretation:

Institutions and liquidity providers may gradually restore risk appetite or liquidity provision while disagreement remains above normal. Securities that do not deteriorate during that process may be earlier beneficiaries of orderly repricing.

Observable implication:

Future formula specification must identify an elevated disagreement state and a subsequent reduction in disorder. It must not rely on low current dispersion alone.

Why it is path-dependent:

The current state matters only because it follows prior elevated disagreement and shows stabilization.

Why it is not static dispersion:

Static dispersion observes the level. This concept requires the relationship between prior elevated disagreement and current stabilization.

Why it is not VoV:

VoV concerns instability of realized volatility. This concept concerns cross-sectional disagreement and its stabilization path.

Why it is not volatility compression:

Volatility compression is about volatility decline. This concept must remain tied to cross-sectional disagreement stabilization, even if volatility is separately monitored.

Why it is not stress repair:

The mechanism should not require panic, drawdown, or recovery labels as the primary state.

Why it is not rank coherence or persistence:

Orderly behavior can be a control, but stable ranks cannot be the mechanism.

Likely failure mode:

The concept may become volatility compression or stress repair if stabilization is defined too broadly.

Decision:

`ACCEPT_WITH_NOTES`

Notes:

Proceed only if the future formula specification includes static dispersion and volatility-compression controls.

### 5.2 Disagreement Relapse Resilience

Scientific question:

Do securities resilient during a relapse of disagreement after temporary calm differ from securities that only appeared strong during calm?

Economic interpretation:

A relapse after calm can reveal whether prior normalization was genuine or fragile. Securities that remain resilient during relapse may indicate durable repricing or superior absorption of renewed disagreement.

Behavioral interpretation:

Institutions and discretionary investors may test positions as disagreement returns. Liquidity providers may ration depth again. Securities that absorb this relapse without adverse behavior may reveal genuine demand.

Observable implication:

Future formula specification must identify a prior calm or partial normalization state followed by renewed disagreement. A simple rising-disagreement condition is not sufficient.

Why it is path-dependent:

Relapse is defined by sequence: disagreement falls or normalizes, then re-expands.

Why it is not static dispersion:

The current re-expansion matters only because it follows temporary calm.

Why it is not VoV:

The concept is about renewed cross-sectional disagreement, not renewed volatility instability.

Why it is not volatility compression:

The concept is not a volatility-compression thesis because it focuses on relapse after calm, not volatility decline.

Why it is not stress repair:

Relapse must not be limited to panic or drawdown recovery windows.

Why it is not rank coherence or persistence:

Resilience must be conditional on disagreement relapse, not simply prior winners continuing.

Likely failure mode:

The concept may collapse into persistence if resilience is measured mostly by prior rank strength.

Decision:

`ACCEPT_FOR_FORMULA_SPEC`

Notes:

This is the cleanest path-dependent concept because relapse cannot be defined without sequence.

### 5.3 Consensus Formation Without Crowding

Scientific question:

Does orderly disagreement normalization identify securities benefiting from delayed consensus formation without rewarding crowded leadership?

Economic interpretation:

As investors converge on a new relative valuation map, disagreement may normalize. Securities that benefit from this process without already being crowded leaders may capture delayed consensus formation.

Behavioral interpretation:

Discretionary investors, institutions, and passive-flow effects may produce gradual convergence. Crowded leaders may underperform if they represent mature consensus rather than emerging consensus.

Observable implication:

Future formula specification must distinguish normalization from mature leadership. It must include an anti-crowding interpretation without becoming a leadership-rotation formula.

Why it is path-dependent:

The signal depends on movement from disagreement toward consensus, not on a static calm or leadership state.

Why it is not static dispersion:

Static low dispersion is insufficient. The concept requires prior disagreement and subsequent normalization.

Why it is not VoV:

VoV is about volatility instability, while this concept is about cross-sectional consensus formation.

Why it is not volatility compression:

Volatility can decline while disagreement remains unresolved. This concept should target cross-sectional consensus, not volatility decline.

Why it is not stress repair:

Consensus formation must not be equivalent to broad recovery after panic.

Why it is not rank coherence or persistence:

Consensus formation cannot simply reward stable ranks or prior winners.

Likely failure mode:

The concept can recreate parked non-hostile transition, momentum, or leadership continuation if crowding is not controlled.

Decision:

`ACCEPT_WITH_NOTES`

Notes:

Proceed only if the future formula specification explicitly blocks parked non-hostile transition and momentum contamination.

### 5.4 Disagreement Path Divergence

Scientific question:

Does a divergence between cross-sectional disagreement path and broader volatility or stress behavior reveal information that static volatility or VoV misses?

Economic interpretation:

The cross-section can disagree even when volatility is calm, or normalize while volatility remains elevated. This divergence may reveal uneven repricing, sector/style rotation, or delayed consensus that volatility-only measures miss.

Behavioral interpretation:

Different investor groups may respond to volatility and relative-value disagreement on different schedules. Liquidity providers and institutions may normalize cross-sectional exposures before volatility fully calms, or vice versa.

Observable implication:

Future formula specification must demonstrate that disagreement path is not merely a re-labeling of volatility path or stress state.

Why it is path-dependent:

Divergence requires comparing paths through time, not comparing one static observation.

Why it is not static dispersion:

Static dispersion does not ask whether disagreement is moving differently from volatility or stress behavior.

Why it is not VoV:

The concept is explicitly distinct only if disagreement path contains information beyond volatility-instability path.

Why it is not volatility compression:

The concept must show cross-sectional disagreement behavior that is not explained by volatility stabilization.

Why it is not stress repair:

The divergence must persist outside simple stress recovery windows.

Why it is not rank coherence or persistence:

The concept should not rely on stable ranks; it should rely on divergence between disagreement path and other market-state paths.

Likely failure mode:

The concept may become indicator engineering if divergence is not economically interpretable.

Decision:

`ACCEPT_FOR_FORMULA_SPEC`

Notes:

This concept has strong orthogonality value because it directly tests whether dispersion path adds information beyond VoV and volatility compression.

### 5.5 Smooth Versus Burst Resolution

Scientific question:

Does smooth convergence of disagreement differ from abrupt burst-like resolution in forward return behavior?

Economic interpretation:

Smooth resolution may indicate gradual consensus formation and orderly liquidity restoration. Burst resolution may indicate forced repositioning, event absorption, or short-lived reversal pressure.

Behavioral interpretation:

Institutions and discretionary investors may create smooth convergence through gradual allocation changes. Burst resolution may reflect event traders, liquidity shocks, or forced one-off adjustment.

Observable implication:

Future formula specification must separate smooth resolution from event shocks and volume-driven reversal.

Why it is path-dependent:

The concept depends on the shape of resolution through time: smooth versus abrupt.

Why it is not static dispersion:

Static dispersion level cannot distinguish smooth convergence from burst-like resolution.

Why it is not VoV:

The resolution shape concerns cross-sectional disagreement, not volatility instability.

Why it is not volatility compression:

Smooth disagreement resolution must not be defined as low or falling volatility alone.

Why it is not stress repair:

Burst resolution after stress may be stress repair unless the design separates the two.

Why it is not rank coherence or persistence:

Smooth resolution must not simply be stable ranks or low churn.

Likely failure mode:

This concept has the highest risk of drifting into event clustering, volume shock reversal, or plain reversal.

Decision:

`ACCEPT_WITH_NOTES`

Notes:

Proceed only if formula specification treats burst behavior as diagnostic or tightly separated from volume shock reversal. If clean separation is not possible, this concept should be revised before implementation.

## SECTION 6 - Mechanism Acceptance Criteria

A mechanism may proceed to formula specification only if:

- it depends on sequence, path, or transition, not level alone;
- it has a plausible economic interpretation;
- it has a plausible behavioral interpretation;
- it can be falsified before research review;
- it has a clear contamination boundary;
- it can be measured with OHLCV-derived cross-sectional data;
- it can state why h5/h10 is the expected primary horizon;
- it can define why any h20 evidence is durability evidence rather than the primary rescue horizon.

## SECTION 7 - Mechanism Rejection Criteria

Reject or revise any concept that:

- collapses into static dispersion level;
- duplicates VoV;
- duplicates volatility compression;
- duplicates hostile/stress repair;
- duplicates plain rank persistence;
- duplicates rank coherence;
- duplicates volume shock reversal or plain reversal;
- revives parked non-hostile transition or leadership continuation;
- cannot be measured without external PIT metadata;
- requires broad parameter search;
- lacks a falsifiable prediction;
- requires h1-only strength to rescue a failed h5/h10 thesis without predeclared justification.

## SECTION 8 - Formula Mapping Rules

No formulas are written in this review. Future formula specification must follow these rules:

- one formula maps to one scientific mechanism concept;
- every formula must cite exactly one primary mechanism concept from this review;
- secondary controls must be labeled as controls, not hidden mechanisms;
- anchor/static-dispersion controls must be included later;
- VoV, volatility compression, stress repair, volume shock reversal, rank coherence, persistence, and parked non-hostile transition contamination checks must be predeclared;
- h5/h10 must remain the primary evidence horizon family unless a later design amendment is approved before scoring;
- h20 evidence cannot rescue a failed h5/h10 mechanism unless h20 was predeclared as primary for that mechanism before formula specification;
- h1-only strength cannot rescue a failed h5/h10 mechanism unless explicitly justified before formula specification;
- no formula may be included only because it is a convenient indicator;
- no formula may combine multiple accepted concepts without naming one primary mechanism and explaining why the others are only controls.

## SECTION 9 - Recommendation

Overall classification:

- `MECHANISM_REVIEW_READY_WITH_NOTES`

Overall recommendation:

- Proceed to formula and panel specification with notes.

Mechanism-level recommendations:

| mechanism concept | decision | formula-specification instruction |
| --- | --- | --- |
| Elevated Disagreement Stabilization | `ACCEPT_WITH_NOTES` | Must control for volatility compression and stress repair. |
| Disagreement Relapse Resilience | `ACCEPT_FOR_FORMULA_SPEC` | Cleanest sequential mechanism; preserve relapse-after-calm definition. |
| Consensus Formation Without Crowding | `ACCEPT_WITH_NOTES` | Must block momentum and parked non-hostile transition contamination. |
| Disagreement Path Divergence | `ACCEPT_FOR_FORMULA_SPEC` | Strong orthogonality concept; must test against VoV and volatility compression. |
| Smooth Versus Burst Resolution | `ACCEPT_WITH_NOTES` | Must be separated from event clustering, volume shock reversal, and plain reversal. |

No mechanism concept is rejected at this stage. The module is scientifically precise enough to proceed to formula specification if the future task obeys the vocabulary freeze and formula mapping rules.

## SECTION 10 - Explicit Non-Goals

This review does not:

- write formulas;
- create candidate IDs;
- finalize candidate code IDs;
- specify panels;
- implement code;
- generate artifacts;
- compute IC;
- run validation;
- refine candidates;
- modify governance decisions;
- modify registry files;
- change thresholds;
- make production changes;
- introduce ML;
- reopen parked candidates;
- promote or demote any candidate.

## SECTION 11 - Verification

Verification:

- Required sections exist: lifecycle placement, scientific vocabulary freeze, mechanism concept review, mechanism acceptance criteria, mechanism rejection criteria, formula mapping rules, recommendation, explicit non-goals, and classification.
- All five mechanism concepts are reviewed.
- Vocabulary freeze is present.
- No formulas are written.
- No candidate IDs are finalized.
- No panel specification is included.
- No implementation files were changed.
- No panel files were changed.
- No IC work was performed.
- No validation was performed.
- No governance decision was modified.
- No production files were changed.
- No threshold files were changed.
- No ML files were changed.

## SECTION 12 - Final Classification

Final classification:

- `MECHANISM_REVIEW_READY_WITH_NOTES`

The next phase may be formula and panel specification, subject to this review's vocabulary freeze, concept decisions, and formula mapping rules.
