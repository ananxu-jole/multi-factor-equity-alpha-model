# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Discovery Specification v1

## SECTION 1 - Executive Summary

This note freezes the formal specification for the next OHLCV-only alpha discovery program centered on non-hostile market transitions and leadership rotation. It converts the design in `ohlcv_non_hostile_transition_and_leadership_rotation_discovery_design_v1.md` into a bounded discovery specification suitable for later implementation planning.

This is a specification-only task. No code was implemented, no candidate panels were generated, no discovery was executed, no refinement was run, no validation was run, no governance was modified, no thresholds were changed, nothing was registered to production, and no ML was implemented.

Discovery objective:

- Test whether orderly leadership emergence, healthy leadership persistence, smooth trend handoff, gradual participation expansion, and broad non-hostile transition behavior can form a new OHLCV-only alpha family.
- Expand Project Underdog beyond its established hostile/stress-repair concentration and its conditional persistence/rank-coherence candidate-lineages.
- Preserve strict separation from CRSP/PIT metadata, sector labels, industry labels, peer-relative calculations, and economic-context dependencies.

Economic hypothesis:

Capital can migrate gradually from mature or weakening leaders into newer leadership candidates while market conditions remain neutral, orderly, or improving. OHLCV behavior may reveal this migration through smooth rank improvement, volume-confirmed accumulation, controlled trend handoff, participation expansion, and healthy breadth contribution before the transition becomes obvious as simple momentum.

Scope:

- OHLCV-only discovery specification.
- High-level candidate categories only.
- Pre-implementation research boundaries and workflow.
- Anti-redundancy and risk-control requirements.

Expected contribution:

- A potential new family axis focused on healthy transitions rather than repair after stress.
- A non-CRSP route to alpha-family diversification.
- A disciplined discovery frame that avoids formula mining and prevents accidental repetition of prior stress-repair, persistence, rank-coherence, or transition-state work.

Relationship to existing alpha families:

- Hostile/stress repair remains the strongest established family and the primary contamination benchmark.
- Persistence and rank-coherence remain conditional candidate-lineages, not broad family proof.
- Dispersion remains exploratory and weak but useful as a redundancy reference.
- Prior transition-state standalone alpha discovery failed when it centered on stress absorption; this specification narrows the transition idea to non-hostile leadership rotation.

## SECTION 2 - Discovery Scope

The discovery program must remain strictly OHLCV-only.

Allowed information set:

- Open, high, low, close, adjusted price behavior, returns, realized volatility, range behavior, volume behavior, universe-level breadth proxies, and cross-sectional ranks derived from OHLCV fields.
- Existing research infrastructure for panel generation, candidate scoring, redundancy review, active coverage review, horizon review, and state attribution.

Explicitly excluded:

- No PIT metadata.
- No CRSP/PIT work.
- No sector metadata.
- No industry metadata.
- No peer-relative calculations.
- No economic-context dependency.
- No static snapshot metadata as a substitute for PIT metadata.
- No source loading.
- No metadata construction.
- No security lineage or ticker lineage construction.
- No ML.

Conceptual scope:

- Focus on non-hostile, orderly, neutral, or improving transitions.
- Avoid primary dependence on hostile trend, panic, weak breadth, drawdown, stress repair, or post-damage recovery gates.
- Treat any future use of broad market state as context only; the alpha thesis must remain leadership transition, not repair.

Operational scope:

- This specification authorizes later implementation design only.
- It does not authorize candidate creation, panel generation, IC scoring, refinement, validation, governance mutation, threshold changes, production registration, or ML.

## SECTION 3 - Discovery Candidate Categories

The future candidate panel should draw from high-level concept categories only. This specification does not define formulas, transformations, parameters, implementation details, or candidate IDs.

Orderly leadership emergence:

- Concepts that identify securities moving from neutral or middling standing toward stronger leadership through smooth, sustained OHLCV improvement.
- The intended mechanism is early leadership emergence, not oversold rebound.

Healthy leadership persistence:

- Concepts that identify securities that become leaders after a non-hostile transition and maintain that leadership without excessive churn or disorderly volatility.
- The intended mechanism is durable leadership after a healthy transition, not post-drawdown rank persistence.

Smooth trend handoff:

- Concepts that identify a controlled handoff from consolidation or neutral trend behavior into leadership participation.
- The intended mechanism is trend transition quality, not raw trend-following strength.

Gradual participation expansion:

- Concepts that identify rising participation, volume quality, or accumulation-like behavior without panic rebound or stress-repair conditions.
- The intended mechanism is orderly demand formation.

Rotation acceleration:

- Concepts that identify increasing pace of leadership migration before it becomes broad momentum.
- The intended mechanism is early capital migration acceleration.

Rotation deceleration:

- Concepts that identify mature or slowing leadership migration where late-stage leadership may be weakening or handoff quality changes.
- The intended mechanism is rotation-phase awareness, not short reversal.

Volume-confirmed leadership shifts:

- Concepts that require leadership improvement to be supported by volume or participation quality.
- The intended mechanism is confirmation of capital migration rather than one-day shock behavior.

Healthy breadth transitions:

- Concepts that identify securities contributing to broad participation or breadth improvement in non-hostile environments.
- The intended mechanism is broadening leadership, not weak-breadth repair.

Category caveat:

- These categories are intended to guide later candidate selection.
- They are not formulas and should not be treated as implementation-ready candidates.

## SECTION 4 - Candidate Inventory Plan

Approximate exploratory concept count:

- Target range: 8 to 12 exploratory concepts.
- Preferred initial scope: 10 concepts if implementation capacity permits clean auditability.
- Maximum early panel size: 12 concepts unless a separate review justifies expansion.

Balance across categories:

- Use 4 to 6 of the high-level categories from SECTION 3.
- Avoid overconcentration in any single category.
- Avoid more than 2 close siblings per category.
- Include at least one concept focused on leadership emergence, one on participation or volume confirmation, one on trend handoff, and one on rotation pace or breadth transition.

Expected diversity:

- Concepts should differ by economic mechanism, activation context, and expected horizon behavior.
- The panel should include both early-transition and post-transition-persistence ideas, but should not become a rank-coherence sibling batch.
- The panel should include participation or volume-supported ideas, but should not become participation repair.

Anti-redundancy objectives:

- Minimize overlap with hostile/stress repair.
- Minimize overlap with post-drawdown persistence.
- Minimize overlap with rank-coherence churn-avoidance.
- Minimize overlap with ordinary momentum or trend continuation.
- Avoid internal duplicate clusters before IC scoring.

Candidate inventory review requirement:

- A future candidate-panel generation task must include a pre-scoring panel and redundancy review.
- Any highly redundant sibling cluster should be reduced before IC discovery scoring.
- Any concept that depends on stress-repair language or state activation should be rejected or rewritten before scoring.

## SECTION 5 - Discovery Methodology

Panel generation philosophy:

- Generate a small, interpretable, economically partitioned panel.
- Prefer clean concept breadth over many close variants.
- Preserve one candidate per distinct concept wherever possible.
- Include diagnostic controls only when they clarify redundancy, momentum overlap, or stress-repair contamination.

Economic-first hypothesis generation:

- Each future concept must begin with a plain-language economic hypothesis.
- The hypothesis must explain why leadership transition or capital migration might predict future returns.
- The hypothesis must identify why the concept is not merely stress repair, post-drawdown persistence, rank-coherence, or ordinary momentum.

Anti-overfitting principles:

- Predeclare concept categories and candidate count before scoring.
- Avoid parameter sweeps.
- Avoid broad state-exclusion searches.
- Avoid selecting candidates based only on h20 behavior.
- Avoid post-hoc changes after observing IC results.
- Treat weak or noisy results as information, not as prompts for immediate formula tuning.

Candidate independence requirements:

- Candidate concepts should differ in primary mechanism.
- Candidate concepts should not be close formula siblings unless a diagnostic reason is predeclared.
- Candidate concepts should be reviewed against known family anchors before IC scoring.

Redundancy screening approach:

- Perform metadata/conceptual redundancy review before scoring.
- Perform statistical redundancy review after panel generation and before IC scoring where feasible.
- Compare later outputs against hostile/stress repair, persistence, rank-coherence, dispersion, volatility-compression, and momentum-like references.
- Review co-activation and state concentration to detect hidden stress-repair dependence.

No implementation details:

- This specification does not define formulas, field transformations, candidate IDs, runner behavior, artifact schemas, or code paths.

## SECTION 6 - Success Criteria

Success should be judged by research contribution and family distinctiveness, not by fixed numeric thresholds in this specification.

Conceptual uniqueness:

- The candidate family must represent non-hostile leadership transition or leadership rotation.
- The mechanism should be explainable as capital migration, leadership emergence, trend handoff, or orderly participation expansion.
- The mechanism should remain distinct from repair, persistence, rank-coherence, and simple trend-following.

Economic plausibility:

- Each successful concept must have a credible market behavior behind it.
- The evidence should be interpretable as healthy transition behavior rather than damage repair.
- The family should make sense without sector, industry, peer, or PIT metadata.

Low redundancy:

- Successful concepts should not be dominated by hostile/stress repair references.
- Successful concepts should not be close duplicates of persistence or rank-coherence conditional candidates.
- Successful concepts should not be explainable solely as raw momentum.

Feasibility using current infrastructure:

- The future program must run with current OHLCV data and existing research workflows.
- It must not require metadata lineage, CRSP access, new asset classes, alternative data, or ML.

Potential diversification benefit:

- A successful discovery result should improve family breadth.
- It should activate in contexts not already saturated by hostile/stress repair.
- It should create a plausible path to later refinement and validation without needing CRSP/PIT evidence.

This specification intentionally does not set IC thresholds.

## SECTION 7 - Risk Controls

Overlap with momentum:

- Risk: leadership emergence may become simple trend-following.
- Mitigation: require economic framing around transition quality, handoff, participation confirmation, or rotation phase rather than recent strength alone.

Overlap with persistence:

- Risk: healthy leadership persistence may become another rank-stability lineage.
- Mitigation: compare against persistence candidates and avoid post-drawdown activation as the primary mechanism.

Overlap with rank coherence:

- Risk: smooth leadership transition may duplicate rank-turnover resilience.
- Mitigation: require transition or leadership-handoff logic, not only low rank churn or coherent rank behavior.

Overlap with stress repair:

- Risk: non-hostile transition concepts may accidentally work only during recovery phases.
- Mitigation: require state attribution and contamination review against hostile/stress-repair anchors before refinement eligibility.

False discovery risk:

- Risk: a small number of concepts may still mine noisy transition states.
- Mitigation: cap candidate count, require predeclared categories, review active coverage, and treat single-window dominance as a risk.

Implementation complexity:

- Risk: leadership rotation concepts can become complex because they combine ranks, trends, volume, breadth, and volatility behavior.
- Mitigation: keep later formulas simple, interpretable, and auditable; reject concepts that require too many moving parts to explain.

Validation challenge:

- Risk: positive discovery evidence may not survive refinement or validation if it is regime-specific.
- Mitigation: require later refinement eligibility review to emphasize window stability, active coverage, redundancy, and economic coherence.

## SECTION 8 - Future Discovery Workflow

The intended workflow is frozen as follows:

1. Discovery implementation

- Implement the discovery framework for this specific OHLCV-only program.
- Define artifact locations, runner behavior, candidate metadata expectations, and guardrails in a later implementation task.
- Do not score candidates during implementation unless separately authorized.

2. Candidate panel generation

- Generate a small predeclared panel based on the categories in this specification.
- Produce candidate metadata, conceptual classification, and panel artifacts.
- Do not interpret panel generation as discovery evidence.

3. Redundancy screening

- Review conceptual, metadata, and statistical redundancy before IC scoring.
- Reduce or hold back duplicate clusters.
- Flag any stress-repair, persistence, rank-coherence, dispersion, or momentum contamination risks.

4. IC discovery

- Score the approved representative panel across the predeclared horizons.
- Evaluate evidence by family mechanism, horizon behavior, active coverage, and state attribution.
- Do not perform refinement during discovery.

5. Refinement eligibility review

- Review whether any discovery candidate merits constrained refinement.
- Require evidence of conceptual distinctiveness and low redundancy, not just positive IC.
- Classify candidates as discovery candidate, diagnostic only, redundant with existing family, or reject research.

6. Constrained refinement

- If justified, refine only predeclared discovery survivors.
- Keep variant count small.
- Avoid post-discovery horizon chasing or state mining.

7. Validation

- Only after refinement and eligibility review, design a separate validation package.
- Validation remains separate from discovery and refinement.
- No governance or production action follows automatically from validation evidence.

No execution is authorized by this specification.

## SECTION 9 - Relationship to Future PIT Work

This discovery remains fully executable today using OHLCV alone.

Current role without PIT metadata:

- Study broad universe-level leadership rotation.
- Use only OHLCV-derived rank, trend, participation, breadth, range, and volatility behavior.
- Avoid sector, industry, peer, or economic-context claims.

Future PIT enrichment:

- If CRSP/PIT metadata later becomes available, the family could be extended to true sector, industry, size, or peer-relative leadership rotation.
- PIT metadata could clarify whether broad universe leadership changes are actually sector rotation, industry rotation, or peer-group migration.
- Security and ticker lineage could improve continuity checks for longer leadership histories.

Boundary until PIT work resumes:

- Do not reopen CRSP/PIT planning.
- Do not use static sector or industry labels.
- Do not infer peer-relative behavior.
- Do not claim sector rotation.

The correct current framing is OHLCV-observable non-hostile leadership rotation.

## SECTION 10 - Final Recommendation

1. Is the discovery scope sufficiently independent?

Yes. The scope is independent enough for implementation planning because it targets non-hostile leadership transition and capital migration, excludes PIT metadata and peer-relative context, and explicitly requires contamination review against stress repair, persistence, rank-coherence, dispersion, and momentum-like behavior.

2. Does the candidate plan minimize redundancy?

Yes, at the specification level. The plan caps early exploratory concepts at 8 to 12, balances concepts across multiple categories, limits close siblings, and requires panel redundancy review before IC scoring.

3. Are the research constraints appropriate?

Yes. The constraints preserve OHLCV-only feasibility, prevent CRSP/PIT reopening, avoid sector or peer leakage, defer ML, and keep the program focused on a distinct economic mechanism.

4. Is the project ready to implement the discovery program?

Yes, for implementation of the discovery scaffold and candidate-panel generation process only. The project is not authorized to execute discovery, refinement, validation, governance mutation, production registration, or ML from this specification alone.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Discovery Implementation Plan v1**. It should define the runner/scaffold, artifact structure, candidate metadata fields, redundancy-review artifacts, fail-closed guardrails, and tests needed to support later candidate panel generation. It should not implement formulas, generate candidates, execute discovery, run refinement, run validation, modify governance, register production artifacts, or implement ML.

## Specification Caveat

This document is specification-only. It does not implement code, create alpha candidates, generate candidate panels, execute discovery, execute refinement, execute validation, modify governance, change thresholds, register production candidates, or implement ML.
