# Project Underdog - Event Clustering Scientific Review v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Classification: `SCIENTIFIC_GATE_APPROVED_WITH_NOTES`

Recommendation: `ADVANCE_TO_DESIGN`

Scope: Platform v2 Phase 1 scientific review for the Event Clustering research module.

This is a scientific review only. It does not implement code, write formulas, create candidate IDs, specify panels, generate panels, compute IC, run validation, modify governance, change production files, change thresholds, or introduce ML.

## SECTION 1 - Scientific Hypothesis

Event Clustering is the hypothesis that clustered sequences of related market events contain predictive information beyond isolated events.

The market behavior being tested is not whether a single shock matters. The hypothesis is that the recent topology of events matters: whether price, volume, range, gap, and volatility events arrive as isolated shocks, clustered bursts, repeated activations, decaying clusters, or mixed sequences. A single event can be noise, but multiple nearby events may reveal forced flows, delayed information diffusion, liquidity withdrawal, crowded repositioning, incomplete absorption, or event fatigue.

Scientific hypothesis:

If market participants respond differently to repeated nearby events than to isolated events, then securities experiencing clustered event sequences should show forward cross-sectional behavior that cannot be explained by single-event reversal, volatility persistence, stress repair, rank persistence, volume persistence, dispersion persistence, or path-dependence alone.

Expected direction:

- Constructive clusters should favor securities that absorb repeated event pressure without disorderly follow-through, excessive extension, or deteriorating participation.
- Adverse clusters should identify securities where repeated activation signals unresolved pressure, crowding, liquidity withdrawal, or delayed repricing.
- The scientific object is the sequence and concentration of events, not the sign or size of one event.

Expected evidence:

- Evidence should initially be candidate-level or diagnostic-level, not family-level.
- Family-level claims would require multiple distinct event-cluster expressions that remain coherent after contamination review.

## SECTION 2 - Economic Intuition

Event Clustering is economically plausible because market events are not always independent. A cluster of related events can reveal a latent market process that a single event cannot identify.

Structural conditions that can create the opportunity:

- large investors may need multiple sessions to adjust positions;
- liquidity providers may reduce risk capacity after repeated shocks;
- news or information may diffuse in stages rather than all at once;
- crowded holders may unwind gradually;
- event-driven traders may overreact to repeated signals;
- passive, ETF, or basket flows may create repeated pressure that is visible through OHLCV event footprints;
- market participants may require repeated confirmations before repricing a name.

The mechanism should create cross-sectional return differences because two securities with similar one-day shocks may be in different event states. One may have experienced an isolated event that is already absorbed. Another may be inside a repeated activation sequence that signals unresolved pressure, information diffusion, liquidity stress, or exhaustion. The clustered sequence changes the interpretation of the current event.

The mechanism is not merely another transformation of OHLCV features if the design preserves the distinction between isolated events and event sequences. The economic claim is about event arrival structure, event memory, and repeated activation, not raw volatility, raw volume, or raw return magnitude.

## SECTION 3 - Behavioral Intuition

The behavioral foundation is that investors often underreact or overreact differently to repeated events than to isolated events.

Plausible actors and behaviors:

- institutions adjust risk and position sizes over multiple trading sessions;
- liquidity providers may become less willing to absorb flow after repeated range, gap, or volume shocks;
- event-driven traders may crowd into repeated signals, creating overshoot or exhaustion;
- short-horizon traders may repeatedly fade or chase event bursts;
- discretionary investors may update beliefs only after multiple confirmations;
- risk-controlled allocators may respond to repeated instability rather than one noisy observation;
- passive and ETF flows may create repeated basket pressure that individual securities absorb unevenly.

The behavioral claim is not that all clusters have the same sign. It is that repeated activation changes the behavioral state of the market. Clustered events can indicate forced adjustment, incomplete absorption, attention concentration, crowded reaction, or exhaustion. The next design phase must preserve this ambiguity and predeclare which cluster states are expected to be constructive versus adverse.

## SECTION 4 - Market Microstructure Rationale

Event clusters can matter at the microstructure level because liquidity supply, inventory limits, and execution constraints are path-dependent.

Microstructure channels:

- liquidity providers may widen spreads, reduce depth, or manage inventory more defensively after repeated shocks;
- large orders may be split over time, creating clustered volume and range events rather than one clean print;
- repeated gap or range events may indicate overnight information digestion or opening-auction imbalance that is not fully settled;
- repeated high-volume events without proportional price deterioration may indicate absorption;
- repeated high-range events with deteriorating closes may indicate fragile liquidity and adverse selection;
- event spacing can matter because short gaps between events leave less time for inventory normalization and belief updating.

This rationale supports the idea that temporal concentration matters. A set of nearby events may represent a single unresolved market process, while the same number of dispersed events may represent unrelated noise.

## SECTION 5 - Expected Mechanism

The unique scientific mechanism is event-arrival topology.

Event Clustering asks whether the arrangement of nearby market events changes forward behavior. The core mechanism is the interaction of:

- temporal concentration;
- repeated activation;
- event-type alignment or disagreement;
- cluster aging or decay;
- absorption versus deterioration after repeated shocks;
- market memory across nearby events.

The expected mechanism is not volatility, stress, rank, volume, dispersion, or reversal by itself. Those features may appear inside event clusters, but the proposed family is only scientifically distinct if the sequence of event arrivals adds information beyond those existing families.

## SECTION 6 - Primary Learning Objective

The primary learning objective is to determine whether market-event sequences contain independent information beyond single-event and state-repair families.

If Event Clustering succeeds, Project Underdog learns that the timing and concentration of events represent a distinct alpha-family frontier. If it fails, the project still learns whether event behavior should remain a diagnostic sidecar rather than an active family, and whether prior event-quality clues were mostly volume shock reversal, gap behavior, stress repair, or short-horizon noise.

Specific learning goals:

- whether clustered events differ from isolated events;
- whether repeated activation changes market behavior;
- whether event sequencing matters beyond event magnitude;
- whether market memory accumulates across nearby events;
- whether event clusters explain behavior not captured by volatility, participation, persistence, rank coherence, dispersion, or volume shock reversal;
- whether event-based research should proceed as a family or remain a contamination reference.

## SECTION 7 - Expected Orthogonality

Expected orthogonality is moderate, with meaningful scientific upside but high contamination risk.

| existing family | expected overlap channel | why Event Clustering should differ | required design implication |
| --- | --- | --- | --- |
| VoV | Event clusters may include volatility-instability bursts. | VoV concerns instability of volatility paths; Event Clustering concerns nearby event arrival structure across event types. | Later design must show that event sequence information is not explained by volatility instability alone. |
| Volatility Compression | Cluster decay can resemble volatility calming. | Compression is about volatility level or stabilization; Event Clustering is about whether repeated events are absorbed, decay, or intensify. | Later design must separate cluster decay from plain volatility compression. |
| Participation / Hostile Stress Repair | Event clusters may activate during hostile or weak-liquidity states. | Stress repair asks whether damaged participation or liquidity improves; Event Clustering asks whether repeated events create memory and absorption effects. | Later design must avoid making hostile/stress state the primary mechanism. |
| Volume Shock Reversal | Clustered events may include abnormal volume events. | Volume shock reversal is single-event or shock-reversal oriented; Event Clustering requires multi-event sequence context. | Later design must compare clustered volume behavior against isolated volume shock behavior. |
| Rank Coherence | Stable names may absorb clusters better. | Rank coherence concerns low churn and consistent rank behavior; Event Clustering concerns repeated event arrival and absorption state. | Later design must prevent low-churn rank stability from becoming the real driver. |
| Persistence | Repeated events may occur in prior winners or post-drawdown survivors. | Persistence rewards continuation of prior relative state; Event Clustering tests whether event concentration changes the interpretation of that state. | Later design must show event sequence adds information beyond prior rank or post-drawdown persistence. |
| Dispersion Path-Dependence (parked) | Event clusters may coincide with cross-sectional disagreement paths. | Dispersion Path-Dependence concerns market-wide disagreement sequence; Event Clustering concerns security-level or event-type activation topology. | Later design must distinguish event clustering from dispersion relapse or normalization. |
| Non-Hostile Transition (parked) | Orderly clusters could be mistaken for leadership transition. | Non-Hostile Transition tested calm leadership or rotation behavior; Event Clustering does not assume leadership rotation. | Later design must not revive parked leadership logic through event language. |
| Static Dispersion | Event clusters may appear during high dispersion. | Static dispersion is a level state; Event Clustering is a sequence-state. | Later design must compare cluster behavior against static disagreement states. |

Orthogonality assessment:

Event Clustering is scientifically distinct in concept because it tests the arrival pattern and memory of events. It is not automatically orthogonal in practice. The next design phase must make the sequence mechanism primary and treat volatility, volume, stress, rank, persistence, dispersion, and reversal channels as contamination references.

## SECTION 8 - Expected Contamination Risks

The primary contamination risk is that Event Clustering becomes a renamed version of an existing family.

Specific risks:

- Volatility persistence: repeated events may simply reflect persistent high volatility.
- Stress persistence: clusters may occur mostly in panic, drawdown, weak-breadth, or liquidity-stress states.
- Path dependence: cluster language may hide dispersion or volatility path-dependence rather than event topology.
- Repeated reversals: repeated event shocks may just create short-horizon reversal behavior.
- Rank persistence: names surviving event clusters may simply be prior winners or low-churn rank leaders.
- Volume persistence: clustered events may reduce to persistent abnormal volume.
- Dispersion persistence: clusters may be a symptom of market-wide disagreement rather than a distinct security-level process.
- Gap-event contamination: cluster evidence may be dominated by raw gap continuation or raw gap reversal.
- Same-period timing risk: event definitions in later phases must preserve strict timing discipline.
- Sparse activation risk: true clusters may be episodic enough that evidence becomes window-dominated.

Contamination judgment:

The contamination risk is high but manageable at the design stage. The family should advance only with notes requiring explicit contamination references, isolated-event comparators, activation diagnostics, and state attribution in later phases.

## SECTION 9 - Falsification Criteria

The Event Clustering hypothesis should be rejected, parked, or redesigned if later evidence shows any of the following:

| falsification condition | qualitative stop condition | interpretation |
| --- | --- | --- |
| No cluster increment | Clustered-event behavior does not add information beyond isolated events. | The scientific mechanism fails. |
| Volatility dominance | Apparent cluster evidence is explained by volatility persistence, volatility instability, or volatility compression. | Reclassify as volatility-family contamination. |
| Stress dominance | Evidence appears only in panic, hostile, drawdown, weak-breadth, or liquidity-stress states. | Reclassify as hostile/stress repair or park. |
| Volume shock dominance | Cluster effects reduce to isolated or repeated abnormal volume reversal. | Reclassify as volume shock reversal contamination. |
| Rank or persistence dominance | Stable ranks, prior winners, or post-drawdown persistence explain the useful behavior. | Reclassify as rank coherence or persistence contamination. |
| Dispersion dominance | Evidence is explained by static dispersion or dispersion path behavior. | Reclassify as dispersion contamination. |
| Reversal-only behavior | Evidence is short-lived reversal with no event-memory interpretation. | Treat as diagnostic only, not a new family. |
| One-window dominance | Apparent success is concentrated in one crisis, macro, or market transition window. | Do not claim a general alpha family. |
| Sparse or unstable activation | Activation is too rare, too broad, or too unstable to interpret. | Park or redesign before implementation expansion. |
| Direction ambiguity unresolved | Later design cannot predeclare when clusters should imply absorption, continuation, exhaustion, or deterioration. | Do not proceed to formula specification until narrowed. |
| Timing integrity risk | Event measurement cannot be made point-in-time safe. | Block execution until timing is resolved. |

These criteria are predefined before implementation. They should not be weakened after results are known.

## SECTION 10 - Observable Implications

If the hypothesis is true, later research should observe:

- clustered events behaving differently from isolated events;
- temporal concentration carrying information beyond event count alone;
- repeated activation changing forward behavior relative to one-off shocks;
- event sequencing affecting whether behavior looks like absorption, continuation, deterioration, or exhaustion;
- cluster decay or persistence having different implications from the initial event burst;
- some event clusters remaining informative outside explicit hostile/stress states;
- event-type alignment or disagreement mattering beyond raw magnitude;
- contamination diagnostics showing that the mechanism is not dominated by volatility, volume, rank, persistence, dispersion, or reversal references.

If the hypothesis is false, later research should show that clustered events are either noisy, redundant, too sparse, or explainable by existing families.

## SECTION 11 - Expected Primary Horizons

Expected primary horizons:

- h5;
- h10.

Expected secondary horizon:

- h20 as durability evidence only.

Rationale:

Event clusters should generally have a shorter information half-life than mature stress-repair or long-memory persistence candidates. If the mechanism is about event absorption, delayed repricing, or cluster exhaustion, h5 and h10 are the cleanest scientific horizons. h20 evidence would be useful, but h20-only success would raise contamination concerns because it may indicate stress repair, persistence, or slow rank effects rather than event clustering.

## SECTION 12 - Expected Activation Profile

Expected activation should be episodic but not vanishingly rare.

The mechanism should activate when nearby related events create a coherent cluster state. It should not be active on nearly every date, because that would imply the design is measuring ordinary volatility, volume, or dispersion levels rather than clusters. It should also not be so sparse that a single crisis or event window dominates interpretation.

Expected activation characteristics:

- event bursts should be distinguishable from isolated events;
- cluster states should have enough cross-sectional breadth for interpretation;
- activation should include both constructive and adverse cluster contexts if the later design supports both;
- activation should not require hostile/stress states as the primary gate;
- cluster aging or decay should be observable as a distinct state from cluster formation.

## SECTION 13 - Potential Weaknesses

Potential weaknesses:

- cluster definitions may become too complex or too tunable;
- true clusters may be sparse;
- event signals may be noisy and turnover-heavy;
- event clusters may be dominated by volume shock reversal;
- repeated shocks may mostly represent stress persistence;
- h20 behavior may be weak or contaminated;
- event sequencing may be hard to interpret without external news or order-flow data;
- OHLCV can observe event footprints but cannot directly identify news, ownership, or dealer inventory causes;
- later implementation could accidentally blur event sequence information with same-period timing assumptions;
- family-level proof may be difficult because event clusters may produce heterogeneous continuation, absorption, and exhaustion behaviors.

These weaknesses argue for approval with notes rather than unconditional approval.

## SECTION 14 - Success Criteria

Success criteria are predefined before implementation and must be carried into the design phase.

Candidate-level success, in qualitative terms:

- primary-horizon evidence should align with the predeclared mechanism direction;
- h5 and h10 should carry the main scientific weight;
- h20 should support durability only, not rescue a failed h5/h10 thesis;
- cluster behavior should improve interpretation versus isolated-event comparators;
- activation should be neither continuous nor crisis-only;
- evidence should not depend on a single calendar window;
- turnover and event churn should remain interpretable at research scale;
- contamination diagnostics should not show dominance by volatility, stress repair, volume shock reversal, rank coherence, persistence, dispersion, or plain reversal.

Family-level success, in qualitative terms:

- more than one event-cluster expression should show coherent behavior;
- successful expressions should not be near-duplicates of the same isolated event effect;
- the family should retain a shared scientific mechanism: event-arrival topology and market memory across nearby events;
- evidence should remain candidate-level unless breadth across distinct event-cluster states is demonstrated.

Scientific success if results are negative:

- the module is still useful if it cleanly determines that event clustering is redundant with existing families;
- the module is useful if it clarifies whether event behavior should remain a contamination reference rather than an active alpha family;
- the module is useful if it identifies whether isolated event research failed because event memory is absent, too sparse, or already captured by volume/stress/rank families.

These criteria must not be optimized after results are known.

## SECTION 15 - Platform v2 Recommendation

Recommendation: `ADVANCE_TO_DESIGN`

Scientific gate classification: `SCIENTIFIC_GATE_APPROVED_WITH_NOTES`

Rationale:

- Event Clustering has a clear scientific hypothesis: clustered sequences of market events may contain information beyond isolated events.
- The economic mechanism is plausible: repeated event arrivals can reveal forced flows, information diffusion, liquidity withdrawal, crowding, delayed repricing, absorption, or exhaustion.
- The behavioral mechanism is plausible: institutions, liquidity providers, event traders, discretionary investors, passive flows, and risk-controlled allocators may respond differently to repeated events.
- The microstructure rationale is credible: liquidity provision, inventory management, execution constraints, and opening/closing imbalances can be path-dependent across nearby events.
- The unique mechanism is identifiable: event-arrival topology and market memory across nearby events.
- The learning objective is meaningful even if the module fails.

Notes attached to approval:

- The design phase must not define formulas until the sequence mechanism, expected directions, activation profile, contamination references, and falsification criteria are preserved.
- The design phase must explicitly distinguish clustered events from isolated events.
- The design phase must not become a volume shock reversal, stress repair, volatility persistence, rank persistence, dispersion persistence, or repeated-reversal module.
- The design phase must treat h5 and h10 as the primary scientific horizons and h20 as durability evidence only.
- The design phase must remain research-only and may not proceed directly to implementation, panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.

## SECTION 16 - Explicit Non-Goals

This review does not:

- implement code;
- write formulas;
- create candidate IDs;
- specify panels;
- generate panels;
- compute IC;
- run validation;
- modify governance;
- change production files;
- register candidates;
- promote or demote candidates;
- change thresholds;
- introduce ML;
- reopen parked families;
- modify the Platform v2 methodology.

## SECTION 17 - Verification

Verified:

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
- Platform v2 methodology was not modified.

## SECTION 18 - Final Classification

Final classification:

- `SCIENTIFIC_GATE_APPROVED_WITH_NOTES`

Recommended next lifecycle phase:

- Platform v2 Phase 1B - Research Module Design.

Event Clustering is scientifically justified as a new independent research frontier, with notes. It may advance exactly one lifecycle phase to research module design. It may not advance directly to formula specification, panel specification, implementation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
