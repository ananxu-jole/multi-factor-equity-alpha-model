# Project Underdog - Main Alpha Inventory Consolidation and Non-CRSP Frontier Selection v1

## SECTION 1 - Executive Summary

This note consolidates Project Underdog's alpha-family research inventory after the CRSP/PIT metadata track was paused at `EXTERNAL_EVIDENCE_INCOMPLETE`. It is review and planning only. No code was implemented, no alpha candidates were created, no discovery was run, no refinement was run, no validation was run, no governance was modified, no thresholds were changed, no production registration occurred, and no ML was implemented.

Current research state:

- The strongest established alpha-family umbrella remains hostile/stress repair.
- Persistence and rank-coherence have both reached `CONDITIONAL VALIDATION CANDIDATE` status as candidate-lineages, not broad validated families.
- Dispersion remains conceptually independent but empirically weak.
- Transition-state research remains useful as a mechanism/context layer, but prior standalone transition-state alpha batches were mostly rejected or stress-adjacent.
- Economic-context and peer-relative research remain strategically important but blocked from validation-quality use until PIT metadata evidence resumes.
- CRSP/PIT work is paused and should not be reopened without external evidence.

Strongest validated or validation-adjacent families:

- Hostile/stress repair: established research umbrella and strongest evidence base.
- Persistence: conditional validation candidate lineage with low stress-repair contamination.
- Rank-coherence: conditional validation candidate lineage with meaningful h20 evidence but stress-repair similarity and sibling redundancy risk.

Exploratory families:

- Dispersion and cross-sectional instability.
- Non-hostile transition-state dynamics.
- Volatility adaptation beyond compression.
- Event-quality structure.
- Participation/liquidity behavior outside repair.

Major bottlenecks:

- Alpha-family concentration remains high.
- The inventory is still dominated by hostile/stress repair, h20 stabilization, drawdown, and repair-adjacent states.
- Peer-relative/context-aware discovery is blocked by PIT metadata.
- ML remains premature.
- Options, fixed income, macro, and alternative-data expansion remain future-phase.

Recommended next frontier:

**OHLCV-only non-hostile transition and leadership-rotation discovery.**

This is the best non-CRSP frontier because it is unblocked by PIT metadata, meaningfully different from the established stress-repair family if designed carefully, and capable of testing whether leadership rotation, neutral accumulation, calm-to-expansion, and non-hostile regime transitions contain alpha without relying on static metadata or new asset classes.

Post-cycle status update:

This recommended frontier has now been executed through implementation, panel generation, IC discovery, and negative-result review. The final family classification is `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`. All nine approved candidates were classified `REJECT`, no refinement is recommended, and generated panels/IC artifacts remain archived as research evidence. The original frontier recommendation is therefore superseded for active research execution; direction inversion is optional only as a future design diagnostic.

VoV module status update:

The OHLCV Volatility-of-Volatility Research Module v1 has now completed the full standard research module lifecycle through Phase 11 and is synchronized as `MODULE_STATE_SYNCHRONIZED`. Phase 10 governance classification was `MODULE_GOVERNANCE_APPROVED`. Official outcomes were `ADVANCE` for `vov_01` and `vov_03`, `WATCH` for `vov_05`, and `PARK` for `vov_02` and `vov_04`.

VoV bounded refinement status update:

The OHLCV Volatility-of-Volatility Bounded Refinement v1 has completed one bounded refinement cycle and is synchronized as `REFINEMENT_STATE_SYNCHRONIZED`. Refinement governance classification is `REFINEMENT_GOVERNANCE_APPROVED`. Validation-design review is authorized only for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`; `vov_01_ref_anchor` and `vov_03_ref_anchor` are baseline comparators; `vov_01_ref_longer_memory` is watch-only; `vov_01_ref_strict_calm`, `vov_03_ref_longer_chop`, and `vov_03_ref_extension_controlled` are parked. No further refinement cycle, validation execution, production action, threshold change, or ML is authorized.

## SECTION 2 - Alpha Family Inventory

| family | research objective | current maturity | strongest candidate(s) | validation status | evidence strength | redundancy risk | future potential | classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hostile/stress repair | Identify securities that repair participation, liquidity, breadth, volatility, or stability inside hostile or fragile regimes. | Mature core umbrella. | `participation_breadth_repair_under_hostile_trend`; related participation/liquidity and volatility-compression threads. | Active research inventory; strongest family evidence. | Strongest in project, but state-dependent. | High within repair/stabilization expressions. | Still useful as core family and contamination benchmark. | Established |
| Participation/breadth repair | Capture improving participation or breadth under weak, hostile, or stress regimes. | Mature sub-family inside stress repair. | `participation_breadth_repair_under_hostile_trend`. | Conditional inventory with healthy/watch-monitor distinctions in prior notes. | Strong within its state niche. | High overlap with hostile/stress repair and liquidity repair. | Maintain and monitor; do not overexpand. | Established |
| Volatility compression/stabilization | Detect stabilization after stress, volatility spikes, or range compression. | Conditional but repair-adjacent. | `volatility_compression_after_stress_stabilization`. | Conditional refinement candidate/watch-monitor style evidence. | Moderate h20 evidence but weak WFV consistency. | Medium-high; often stress-repair expression. | Useful diagnostic and possible sub-family, not independent core yet. | Conditional |
| Volatility-of-volatility | Test volatility-of-volatility structure as a medium-horizon OHLCV-only alpha mechanism. | Completed module plus one bounded refinement cycle. | `vov_03_ref_strict_chop`, `vov_01_ref_smoothed_calm`; anchors as baseline comparators. | Completed Phase 11 under `PROJECT_STANDARD_APPROVED`; bounded refinement synchronized as `REFINEMENT_STATE_SYNCHRONIZED`. | Candidate-level h10/h20 evidence improved enough for validation-design review of two variants only. | Medium-high until checked against volatility compression, stress repair, persistence, rank-coherence, reversal, volume-shock, and `vov_05`-like references. | Next authorized work is validation-design review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`; no further refinement. | Conditional |
| Persistence/rank stability | Test whether post-drawdown rank persistence and low rank churn predict forward returns. | Conditional candidate-lineage. | `post_drawdown_persistence_churn_adjusted_20`; `post_drawdown_persistence_core_20`. | `CONDITIONAL VALIDATION CANDIDATE`. | Good h10 validation behavior; h20 weaker. | Medium; sibling/lineage redundancy expected. | Worth preserving and integration-reviewing. | Conditional |
| Rank-coherence | Test whether coherent rank structure and turnover resilience contain alpha. | Conditional candidate-lineage. | `rank_coherence_churn_avoidance_02_overlap_adjusted`. | `CONDITIONAL VALIDATION CANDIDATE`. | Positive h20 validation evidence; weak h10 WFV and concentration risks. | High sibling redundancy; moderate stress-repair similarity. | Worth preserving but should seek broader non-overlapping rank-family evidence later. | Conditional |
| Dispersion/cross-sectional instability | Test dispersion transitions, acceleration, normalization, and instability states. | Explored but weak. | `dispersion_transition_acceleration_20`; `dispersion_transition_acceleration_neutralized_20`. | Discovery/refinement only; no validation pass. | Distinct but modest h5/h10 and h20 decay. | Low versus core families but high fragility. | Valuable diagnostic axis; revisit only with tight design. | Exploratory |
| Transition-state dynamics | Study alpha around regime transitions outside static stress labels. | Diagnostic/exploratory. | Transition-state detector; prior transition-state batch had no viable standalone alpha. | Prior 10-candidate batch rejected; detector framing recommended. | Weak as standalone alpha so far. | High if framed as stress absorption; lower if non-hostile transitions are isolated. | Good next frontier if redesigned away from repair states. | Exploratory |
| Volatility adaptation beyond compression | Explore volatility structure, realized-vol shifts, range behavior, and adaptation to changing volatility. | Exploratory. | Volatility shock absorption and volatility compression threads. | Refinement/diagnostic only. | Mixed and often repair-adjacent. | Medium-high with stabilization family. | Useful inside non-hostile transition design if not stress-gated. | Exploratory |
| Participation/liquidity outside repair | Test participation and liquidity shifts without hostile/stress repair framing. | Underdeveloped. | Non-price liquidity repair clues; relative participation shift concepts. | Not validation-ready. | Weak to modest. | High with participation repair unless constraints change. | Possible future path, but not first choice. | Exploratory |
| OHLCV non-hostile transition / leadership rotation | Test orderly non-hostile leadership rotation, neutral accumulation, and breadth contribution without PIT metadata. | Completed and parked. | `nhlr_05` as least weak reference only. | IC discovery complete; all nine approved candidates `REJECT`. | Negative: best primary result `nhlr_05` h10 mean IC -0.000173; family h10 mean IC -0.011925; family h20 mean IC -0.014564. | Medium conceptual overlap risk with hostile-transition, stress-repair, and rank-coherence if redesigned. | Archive current panels/IC artifacts; optional future inversion diagnostic design only. | Parked |
| Structural interaction | Test smooth interaction terms among volatility, participation, liquidity, and stabilization ingredients. | Mostly exhausted. | Weak curvature/stabilization clues. | No refinement or validation candidate. | Weak. | High; recombines existing repair ingredients. | Low unless a new theory emerges. | Retired |
| Recovery-quality targets | Diagnose repair and stabilization quality through alternate targets. | Diagnostic sidecar. | Recovery-quality target experiments. | Diagnostic only. | Useful interpretively, not alpha-family evidence. | High target-feature proximity risk. | Keep as diagnostics, not alpha family. | Retired |
| Economic-context/peer-relative | Build peer, sector, industry, and size-relative alpha families. | Strategically important but blocked. | No validation-quality candidate. | Static-only diagnostic substrate. | High theoretical value, no PIT-valid alpha evidence. | Depends on metadata; static labels risk false diversification. | Highest future value once PIT evidence resumes. | Exploratory |
| Event-quality structure | Test orderly event-gap behavior and continuation/containment after events. | Weak exploratory. | `event_gap_quality_continuation_filter`. | Rejected in focused discovery due weak IC/high turnover. | Weak. | Low with repair, but low alpha evidence. | Park unless new event-quality theory improves. | Retired |

## SECTION 3 - Alpha Family Map

Hostile/stress repair:

- Includes participation repair, breadth repair, liquidity repair, volatility compression after stress, shock absorption, and many normalization threads.
- This is the established core, but also the biggest source of concentration.

Persistence:

- Includes post-drawdown rank stability and churn-adjusted persistence.
- Distinct from stress repair at artifact level, but still drawdown-adjacent.

Rank coherence:

- Includes rank-turnover resilience, overlap-adjusted churn avoidance, and non-hostile transition rank-coherence siblings.
- Distinct from persistence in validation, but has stress-repair similarity and sibling duplicate risk.

Volatility adaptation:

- Includes volatility compression, shock absorption, range normalization, and volatility structure behavior.
- Most current evidence is stress-adjacent; non-hostile volatility adaptation remains underexplored.
- The completed VoV bounded refinement adds two validation-design approved volatility-structure variants, `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`, but this remains candidate-level evidence until anti-redundancy and contamination review is completed.

Participation/liquidity:

- Mature only inside repair.
- Outside-repair participation shifts remain underexplored and should be treated as a future feature family, not a proven standalone group.

Dispersion:

- Includes dispersion transition acceleration, neutralized dispersion acceleration, dispersion stability, and dispersion normalization clues.
- Structurally independent but empirically weak.

Transition-state:

- Prior standalone transition-state alpha discovery failed.
- Transition-state remains valuable if reframed around context detection or non-hostile leadership/rotation transitions.

Structural interaction:

- Mostly recombinations of existing stress-repair ingredients.
- Should not count as an active family.

Economic-context dependent:

- Strategically important but paused with PIT metadata.
- Peer-relative discovery should remain waitlisted until CRSP/PIT evidence resumes.

Other emerging themes:

- Event quality, neutral accumulation, leadership rotation, calm-to-expansion behavior, and non-hostile volatility participation changes.
- These are the best raw material for a non-CRSP OHLCV frontier.

Key overlaps:

- Participation repair, liquidity repair, volatility compression, shock absorption, and stress-to-normal transition work overlap heavily with hostile/stress repair.
- Persistence and rank-coherence overlap through cross-sectional rank behavior, though validation shows they are not the same candidate.
- Rank-coherence and dispersion overlap in some state attribution around dispersion stability/normalization.
- Transition-state work frequently overlaps with stress repair unless explicitly constrained away from hostile/stress regimes.

## SECTION 4 - Redundancy Review

Duplicated concepts:

- Multiple participation, liquidity, breadth, and volatility compression candidates express the same broad repair/stabilization mechanism.
- Persistence variants are deliberately sibling variants around one lineage; they should not be counted as independent family breadth.
- Rank-coherence siblings are highly related; the validation result supports one candidate thread, not a broad rank-coherence family.
- Structural interaction candidates mostly recombine existing volatility/participation/liquidity ingredients.

Highly correlated or saturated research threads:

- Hostile/stress repair is saturated.
- Participation/breadth/liquidity repair is mature enough that more variants would likely add redundancy unless a new non-repair hypothesis is used.
- Volatility compression after stress is useful but should be monitored rather than expanded broadly.
- Rank-coherence needs breadth, not sibling variants.

Underexplored areas:

- Non-hostile transition-state dynamics after the current OHLCV-only formulation has been parked.
- Leadership rotation without PIT metadata, now requiring redesign-level or inversion-diagnostic framing rather than direct continuation.
- Calm-to-expansion and neutral accumulation behavior.
- Volatility adaptation outside stress repair.
- Participation/liquidity shifts outside hostile or drawdown states.
- Dispersion robustness under cleaner anti-repair constraints.
- VoV validation-design review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`, with anchors retained as baseline comparators and all watch/park variants archived.

Consolidation recommendations:

- Consolidate participation, breadth, liquidity, volatility compression, and shock absorption under the hostile/stress-repair umbrella.
- Preserve persistence as a single conditional candidate-lineage.
- Preserve rank-coherence as a single conditional candidate-lineage.
- Keep dispersion exploratory and diagnostic, not validation-ready.
- Retire structural interaction and event-quality structure from active frontier consideration.
- Keep economic-context/peer-relative on a PIT waitlist.

## SECTION 5 - Frontier Gap Analysis

Non-hostile transition and leadership rotation:

- Economic intuition: alpha may arise when leadership changes or broad rank/participation structure shifts in neutral or improving regimes, not only after stress.
- Expected uniqueness: medium-high. This could separate regime-transition alpha from repair alpha.
- Relationship to existing families: adjacent to rank-coherence and transition-state research, but can be constrained away from drawdown/stress repair.
- Feasibility without PIT metadata: high using OHLCV ranks, breadth, trend, participation, and volatility states.

Calm-to-expansion behavior:

- Economic intuition: securities that begin participating before broad volatility or trend expansion may lead in early regime shifts.
- Expected uniqueness: medium-high.
- Relationship to existing families: inverse of stress repair; less dependent on drawdown.
- Feasibility without PIT metadata: high.

Neutral accumulation without breakout:

- Economic intuition: accumulation, liquidity, or participation improvement without price extension may forecast future leadership without being a repair signal.
- Expected uniqueness: medium.
- Relationship to existing families: uses participation/liquidity ingredients but removes hostile/stress gate.
- Feasibility without PIT metadata: high.

Dispersion structure revisit:

- Economic intuition: cross-sectional instability, normalization, or leadership rotation may be predictive if defined more robustly than prior dispersion acceleration.
- Expected uniqueness: high.
- Relationship to existing families: distinct from repair and persistence, but prior empirical evidence is weak.
- Feasibility without PIT metadata: high.

Volatility adaptation outside repair:

- Economic intuition: volatility slope, range compression/expansion, and volatility-of-volatility may identify stability or leadership changes before price response.
- Expected uniqueness: medium.
- Relationship to existing families: high risk of slipping back into volatility compression after stress.
- Feasibility without PIT metadata: high.

Participation asymmetry outside repair:

- Economic intuition: upside/downside participation asymmetry and volume quality may identify early demand without relying on stress states.
- Expected uniqueness: medium.
- Relationship to existing families: shares ingredients with participation repair but can be made non-repair by excluding hostile/drawdown gates.
- Feasibility without PIT metadata: high.

Peer-relative/context-aware behavior:

- Economic intuition: names improving relative to true peers may contain independent alpha.
- Expected uniqueness: very high.
- Relationship to existing families: potentially strongest independent path.
- Feasibility without PIT metadata: low. Blocked until PIT evidence resumes.

## SECTION 6 - Research Prioritization

| frontier | expected information gain | novelty | implementation feasibility | independence from CRSP | diversification benefit | rank |
| --- | --- | --- | --- | --- | --- | ---: |
| OHLCV-only non-hostile transition and leadership rotation | High | High | High | High | High | 1 |
| Dispersion robustness revisit | Medium-high | High | High | High | Medium-high | 2 |
| Neutral accumulation without breakout | Medium-high | Medium | High | High | Medium | 3 |
| Participation asymmetry outside repair | Medium | Medium | High | High | Medium | 4 |
| Volatility adaptation outside repair | Medium | Medium | High | High | Medium | 5 |
| Portfolio/validation consolidation | Medium | Low | High | High | Medium | 6 |
| Peer-relative/context-aware discovery | Very high | Very high | Low now | Low now due PIT dependency | Very high later | Waitlist |
| Options/fixed income expansion | Low now | High | Low | Medium | Unknown | Future phase |
| ML feature/model research | Low now | Medium | Medium | High | Low now | Deferred |

Prioritization conclusion:

Historical prioritization conclusion:

The best next frontier in this note was an OHLCV-only non-hostile transition and leadership-rotation discovery program. That program has now completed and is parked as `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL` after broad negative IC evidence. It should be removed from the active priority queue; the archived panels and IC artifacts should be preserved as negative research evidence.

Current authorized follow-up:

After the completed VoV bounded refinement governance decision and state synchronization, the next authorized non-CRSP OHLCV follow-up is validation-design review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` only. This is not a new broad discovery program, does not authorize another refinement cycle, and does not authorize validation execution, production registration, threshold changes, or ML.

## SECTION 7 - Recommended Next Discovery Program

Recommended frontier:

**OHLCV-only non-hostile transition and leadership rotation.**

Post-cycle supersession:

This recommended discovery program has been completed and should not be continued as an active discovery or refinement path. All nine implemented candidates were rejected in first-pass IC discovery. A direction-inversion diagnostic may be designed later, but only as a separate diagnostic task, not as refinement, validation, governance change, or production registration.

Rationale:

- It is independent of the paused CRSP/PIT track.
- It targets the central bottleneck: family diversification.
- It avoids repeating hostile/stress repair.
- It uses existing infrastructure and data.
- It can absorb lessons from transition-state, rank-coherence, participation, and dispersion research without recreating any one of them.
- It gives dispersion and volatility structure a role as diagnostics or context, not as the whole thesis.

Expected hypotheses:

- Leadership rotation may be detectable through changes in cross-sectional ranks, participation, and breadth outside hostile/stress regimes.
- Neutral or calm regimes may contain early accumulation signals that are not merely repair after drawdown.
- Non-hostile volatility or dispersion transitions may identify rotation quality rather than stress absorption.
- Names that improve participation or stability without price extension may later become leaders.

Success criteria:

- Positive h5/h10 or h10/h20 IC evidence without relying on hostile, weak-breadth, panic, drawdown, or stress-repair gates.
- Low redundancy versus hostile/stress-repair anchors.
- Low redundancy versus persistence and rank-coherence conditional candidates.
- Clear active coverage and no narrow single-window dominance.
- Predeclared small candidate panel and no broad parameter search.
- Evidence of a distinct mechanism, not merely another repair/stabilization label.

Anticipated risks:

- Transition-state definitions may be too broad or noisy.
- Candidate formulas may accidentally rediscover stress repair.
- Leadership rotation without PIT sector/industry context may be only broad-market rank behavior.
- Rank-based definitions may overlap rank-coherence.
- Participation definitions may overlap participation repair.
- Dispersion diagnostics may weaken into previously failed dispersion transition behavior.

Guardrail:

Do not design candidates yet in this note. The next task should be a discovery program design that predeclares a small panel, contamination references, state exclusions, and stop conditions.

## SECTION 8 - ML Readiness Review

ML should remain deferred.

Current alpha diversity is not sufficient to justify ML:

- Only one family is established.
- Persistence and rank-coherence remain conditional candidate-lineages.
- Dispersion is weak.
- Transition-state work is exploratory.
- Peer-relative/context-aware features are blocked by PIT metadata.
- The strongest evidence is still concentrated in h20 repair/stabilization states.

Why ML would be premature:

- It would likely learn hostile/stress repair exposure rather than independent alpha mechanisms.
- It would blur candidate lineage boundaries before the family inventory is broad enough.
- It would create optimization pressure before validation-ready family breadth exists.
- It could create false confidence from redundant candidate variants.

Minimum preconditions before ML:

- At least two established alpha families.
- At least two additional conditional families with distinct mechanisms and contamination reviews.
- More balanced h5/h10/h20 evidence.
- PIT-safe metadata if peer-relative or economic-context features are included.
- Stable monitoring and inventory status for current conditional candidates.

## SECTION 9 - 90-Day Research Roadmap

Phase 1: Consolidation and frontier design.

- Freeze current family inventory and classifications.
- Keep CRSP/PIT paused at `EXTERNAL_EVIDENCE_INCOMPLETE`.
- Record the completed OHLCV Non-Hostile Transition and Leadership Rotation family as parked with classification `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.
- Preserve generated panels and IC artifacts as archived research evidence.
- Treat any direction-inversion work as a future design-only diagnostic.

Phase 2: Discovery program specification.

- Predeclare a small candidate panel.
- Define allowed OHLCV ingredients, horizons, active coverage checks, redundancy references, contamination references, and stop conditions.
- Include rank-coherence, persistence, hostile/stress-repair, and dispersion references as diagnostics only.
- No discovery execution until the design is reviewed.

Phase 3: Controlled discovery execution.

- If the design is accepted, run one small discovery batch.
- Evaluate h1/h5/h10/h20 IC, WFV windows, state attribution, active coverage, redundancy, and contamination.
- No refinement, validation, governance mutation, or production registration in the discovery pass.

Phase 4: Review and refinement eligibility.

- Review whether any candidate shows a distinct non-repair mechanism.
- Reject weak or repair-contaminated candidates.
- If one or two candidates survive, create a small refinement design only.

Phase 5: Validation-readiness discipline.

- Do not validate until discovery and refinement evidence justify it.
- Do not introduce ML.
- Keep portfolio research limited to monitoring and consolidation unless a candidate reaches validation-quality status.

Future ML readiness:

- Reassess only after the new frontier either produces a conditional family candidate or is rejected.
- ML remains out of scope for this 90-day roadmap.

## SECTION 10 - Final Recommendation

1. Which alpha families are strongest today?

Hostile/stress repair is strongest and established. Persistence and rank-coherence are the strongest conditional candidate-lineages. Participation/breadth repair is the cleanest sub-family inside the hostile/stress umbrella.

2. Which should be retired?

Structural interaction and event-quality structure should be retired from active frontier selection. Recovery-quality targets should remain diagnostic only. Weak dispersion variants, rising-state dispersion narrowing, and failed transition-state standalone structures should not be repeated.

3. Which deserve further investment?

Persistence and rank-coherence deserve preservation and integration-review attention as conditional lineages. Dispersion deserves a narrow diagnostic role. The current OHLCV non-hostile transition and leadership-rotation family is parked after broad negative IC evidence. Peer-relative/context-aware alpha deserves future investment only after PIT evidence resumes.

4. What is the single best non-CRSP research frontier?

The prior single best non-CRSP frontier, **OHLCV-only non-hostile transition and leadership rotation**, has now been tested and parked. The next research direction should pivot away from this implemented family: either return to peer-relative/economic-context readiness when PIT metadata evidence resumes, or create a separate design-only direction-inversion diagnostic if the team wants to learn from the negative OHLCV signs.

5. Should ML remain deferred?

Yes. ML remains premature because the family inventory is not broad enough and the strongest evidence is still concentrated in hostile/stress repair and conditional candidate-lineages.

6. What should the next Codex task be?

The next Codex task should not refine the rejected OHLCV family. Recommended next direction is **Project Underdog - Peer-Relative Economic Context Readiness and Alpha Frontier Design v1** once PIT metadata evidence is available. If the research team wants to continue learning from the parked OHLCV family first, the only appropriate task is **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Direction-Inversion Diagnostic Design v1**, design-only and explicitly non-execution.

## Research Caveat

This consolidation is review-only. It does not implement code, create alpha candidates, run discovery, run refinement, run validation, modify governance, change thresholds, register production outputs, promote or demote candidates, or implement ML.
