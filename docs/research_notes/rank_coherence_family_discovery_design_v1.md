# Rank-Coherence Family Discovery Design v1

Date: 2026-06-18

Project: Project Underdog

Status: `DESIGN_ONLY`

Scope: design-only discovery program for the rank-coherence alpha-family frontier. No discovery execution, refinement execution, validation execution, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Strategic Context

Project Underdog's alpha inventory remains too narrow:
- Established: hostile/stress-repair.
- Conditional: persistence, represented by `post_drawdown_persistence_churn_adjusted_20`.
- Exploratory: dispersion.
- Next frontier: rank-coherence.

Persistence was frozen as a `CONDITIONAL VALIDATION CANDIDATE` because it survived validation directionally but appeared to reach a practical current limit. The h10 profile remained credible, while h20 was positive but thin and the best horizon remained h5. A final persistence refinement was not recommended because it would likely chase validation diagnostics rather than test a fresh hypothesis.

Rank-coherence is the right next frontier because it preserves the useful lesson from persistence, namely that cross-sectional rank structure may contain alpha, while shifting away from post-drawdown conditioning. The prior diversification batch included a `Rank Coherence Regime Transition` theme, but redundancy review showed material overlap with `Rank Stability After Drawdown`. This design must therefore treat rank-coherence as a cleaner family, not as an extension of the frozen persistence lineage.

The strategic goal is to determine whether rank ordering, leadership agreement, churn, concentration, and rotation contain alpha outside hostile/stress-repair and outside post-drawdown persistence.

## SECTION 2 - Rank-Coherence Family Definition

Rank-coherence means the degree to which cross-sectional ranks are orderly, stable, internally consistent, or meaningfully rotating across related measurements. A rank-coherent market or security set has interpretable leadership structure: leaders remain leaders, laggards remain laggards, rankings across related windows agree, or leadership changes occur in a structured rather than noisy way.

Candidate signals in this family should score securities by their position inside that rank structure. The family is about rank organization, not simple momentum, stress repair, volatility collapse, or post-drawdown resilience.

Difference from persistence:

Persistence asks whether a security maintains or improves rank after a drawdown or adverse event. Rank-coherence asks whether a security participates in a broader orderly rank structure regardless of drawdown context. Persistence is event-conditioned and lineage-specific; rank-coherence should be cross-sectional and structure-conditioned.

Difference from dispersion:

Dispersion studies the width, acceleration, compression, or anomaly shape of cross-sectional return distributions. Rank-coherence studies order within the cross-section. A high-dispersion market can be rank-coherent if leadership is stable; a low-dispersion market can be rank-incoherent if leadership churns randomly.

Difference from hostile/stress repair:

Hostile/stress repair identifies improvement inside weak, hostile, liquidity-impaired, or breadth-impaired regimes. Rank-coherence must not define its signal around recovery, repair, weak breadth, participation rebound, or liquidity normalization. Stress states may be used only as exclusion or attribution diagnostics, not as primary activation logic.

Difference from volatility compression:

Volatility compression focuses on falling realized volatility or stabilization after turbulent behavior. Rank-coherence may coexist with volatility compression, but it should be measured through rank order, leadership concentration, rank agreement, and rank churn rather than volatility level or volatility decline.

## SECTION 3 - Economic Intuition

Cross-sectional rank structure can contain alpha because investors do not observe or react to leadership changes uniformly. Durable leaders may continue attracting incremental demand, while noisy leaders may mean-revert. A market with coherent leadership may reward securities that hold high ranks across windows; a market with unstable leadership may reward securities that avoid churn or that rotate into leadership before broad recognition.

Rank churn may be informative because frequent rank movement can indicate unstable sponsorship, transient price pressure, or uncertainty about relative fundamentals. Low churn among improving names can indicate durable demand, while extreme churn can identify reversal pressure or crowded short-term overreaction.

Leadership concentration may matter because concentrated leadership can create continuation among true leaders but fragility among marginal followers. Conversely, leadership broadening can identify securities newly gaining relative sponsorship before aggregate breadth or participation repair becomes obvious.

Leadership rotation may contain alpha when the market is reorganizing around a new cross-sectional ordering. The goal is not to buy recovery after damage; it is to identify whether the rank map itself is becoming more ordered, more concentrated, or constructively rotating.

## SECTION 4 - Candidate Theme Design

This discovery program should test five rank-coherence themes. The batch should be intentionally small, with two candidates per theme and at most one optional diagnostic candidate for the highest-priority theme after pre-launch review.

### Theme 1: Leadership Stability

Economic hypothesis:

Securities that remain in the upper cross-sectional rank group across multiple non-identical windows outperform because leadership persistence reflects durable sponsorship rather than transient price pressure.

Feature ingredients:
- Cross-sectional return ranks over short and medium windows.
- Rank agreement between adjacent windows, such as h5 versus h10 or h10 versus h20 rank consistency.
- Top-quintile or top-decile retention indicators.
- Rank volatility or rank standard deviation over rolling windows.

Horizon focus:
- Primary: h10.
- Secondary: h20.
- h5 should be reported as a diagnostic only, not used to redefine the theme.

Expected alpha behavior:
- Positive IC when stable leaders continue to outperform.
- Stronger behavior in ordinary or constructive markets than in panic repair states.
- Lower activation dependence than post-drawdown persistence.

Expected failure modes:
- May become simple momentum if rank agreement is defined only by recent returns.
- May fail when leadership rotation dominates continuation.
- May select low-volatility mega-cap leadership rather than true rank-coherence alpha.

Redundancy risk:
- Moderate risk versus momentum and persistence lineage controls.
- Low-to-moderate risk versus hostile/stress-repair if no repair states are used.

### Theme 2: Rank Churn Avoidance

Economic hypothesis:

Securities with lower rank churn among otherwise improving names outperform because stable improvement is more reliable than noisy cross-sectional jumping.

Feature ingredients:
- Rolling absolute rank change.
- Rank turnover relative to universe rank turnover.
- Improvement slope adjusted by rank churn.
- Churn penalty applied to improving rank trajectories.

Horizon focus:
- Primary: h10-h20.
- h5 should be used only to identify short-lived churn artifacts.

Expected alpha behavior:
- Positive IC for securities with improving but not erratic rank paths.
- More robust than raw leadership stability if it avoids buying exhausted leaders.

Expected failure modes:
- Highest overlap risk with `post_drawdown_persistence_churn_adjusted_20`.
- May become a near-duplicate of persistence if drawdown context or post-drawdown windows are used.
- May underperform in fast leadership rotations.

Redundancy risk:
- High versus persistence lineage controls.
- Must be included because churn is central to rank-coherence, but candidate definitions must avoid drawdown conditioning and must be screened tightly against persistence panels.

### Theme 3: Rank Reversal Pressure

Economic hypothesis:

Extreme rank deterioration or abrupt rank ascent can create reversal pressure when rank moves are incoherent with medium-window rank structure. The alpha is not classical price reversal; it is the mismatch between short-window rank movement and broader rank order.

Feature ingredients:
- Short-window rank shock.
- Medium-window rank anchor.
- Rank acceleration or deceleration.
- Cross-window rank disagreement.
- Optional clipping of extreme one-day rank moves to avoid pure event reversal.

Horizon focus:
- Primary: h5-h10.
- Secondary: h20 as a durability diagnostic.

Expected alpha behavior:
- Positive IC when incoherent rank shocks mean-revert toward the broader rank structure.
- May diversify horizon exposure because the effect can be shorter than persistence.

Expected failure modes:
- May collapse into classic reversal diagnostics.
- May overreact to earnings gaps or one-day events.
- May be noisy if rank disagreement is too sensitive.

Redundancy risk:
- Moderate-to-high versus reversal baselines.
- Moderate versus hostile/stress repair if negative rank shocks coincide with stress recovery.

### Theme 4: Leadership Concentration and Broadening

Economic hypothesis:

The concentration or broadening of leadership contains information about which securities benefit from a coherent market structure. In concentrated leadership regimes, durable top-ranked securities may continue outperforming; in broadening regimes, new entrants into leadership may offer early alpha.

Feature ingredients:
- Cross-sectional leadership concentration measures, such as top-quintile rank share or rank entropy.
- Breadth of rank improvement, excluding participation-repair metrics.
- Security-level entry into stable leadership groups.
- Distance from crowding in the top leadership group.

Horizon focus:
- Primary: h10-h20.

Expected alpha behavior:
- Positive IC for durable leaders in concentrated regimes or high-quality new entrants during broadening.
- Could identify a family-level structure not tied to drawdown or stress repair.

Expected failure modes:
- May become a breadth or participation repair proxy if broadening is measured through volume, liquidity, or advancing-count repair.
- May overweight crowded leadership if concentration persists too long.
- May struggle when leadership is fragmented.

Redundancy risk:
- Moderate versus participation/breadth repair if not carefully feature-controlled.
- Moderate versus momentum if top-rank retention dominates the formula.

### Theme 5: Regime-Independent Rank Coherence

Economic hypothesis:

Securities whose ranks are coherent across benign, neutral, and transition states outperform because the rank structure reflects durable relative information rather than one regime's repair dynamics.

Feature ingredients:
- Rank agreement across state slices.
- Stability of rank relationship before, during, and after non-hostile transitions.
- Rank coherence measured without hostile/stress labels as activation triggers.
- State attribution diagnostics used after scoring, not as formula ingredients.

Horizon focus:
- Primary: h10.
- Secondary: h20.

Expected alpha behavior:
- Positive IC across multiple ordinary states, with no single stress-repair state dominating.
- Useful as a family-distinctness test even if raw IC is modest.

Expected failure modes:
- May be underpowered if states are too broad.
- May accidentally recreate the prior `Rank Coherence Regime Transition` theme if transition definitions are too similar.
- May produce diagnostic evidence rather than a strong candidate.

Redundancy risk:
- Moderate versus prior `transition_rank_stability_20`.
- Moderate versus transition-state dynamics if state labels dominate the candidate construction.

## SECTION 5 - Anti-Redundancy Controls

Controls against recreating persistence:
- Do not use drawdown depth, post-drawdown windows, downtrend repair windows, or the frozen persistence candidate as direct formula ingredients.
- Require redundancy diagnostics versus `post_drawdown_persistence_churn_adjusted_20`, `post_drawdown_persistence_core_20`, and `post_drawdown_persistence_20`.
- Any candidate with high similarity to the persistence lineage should be diagnostic-only unless it has a distinct non-drawdown mechanism and materially different horizon/state behavior.
- Rank churn candidates must be universe-rank-structure candidates, not post-drawdown churn variants.

Controls against recreating hostile/stress repair:
- Do not use hostile trend, weak breadth, liquidity repair, participation repair, failed-breakout recovery, panic repair, or stress-stabilization variables as primary features.
- Stress states may be used only for contamination review and state attribution.
- Require correlation and co-activation checks versus known hostile/stress-repair candidates and references.
- Reject candidates whose alpha is concentrated primarily in recovery, liquidity-repair, weak-breadth repair, or hostile-normalization states.

Controls against recreating participation repair:
- Do not use volume participation, liquidity normalization, turnover repair, or breadth repair as the main signal.
- If breadth-like counts are needed for leadership concentration, define them from rank membership rather than trading participation or liquidity.
- Require review of leadership broadening formulas to ensure they measure rank map broadening, not market participation repair.

Controls against recreating dispersion compression/expansion:
- Do not use cross-sectional return dispersion, volatility dispersion, pairwise correlation compression, or dispersion acceleration as primary ingredients.
- Rank concentration or rank entropy may be used only when computed from rank membership/order, not return dispersion magnitude.
- Require redundancy diagnostics versus `dispersion_transition_acceleration_20` and remaining dispersion diagnostics.

Review controls:
- Pre-launch: inspect every candidate formula against the prohibited feature list.
- Panel-level review: screen pairwise redundancy before IC scoring and reduce the scoring subset if intra-theme crowding appears.
- IC discovery review: evaluate distinctiveness before any refinement recommendation.
- Post-discovery: classify at family and theme level, not by raw IC alone.

## SECTION 6 - Discovery Batch Scope

Recommended candidate count:
- Minimum: 8 candidates.
- Target: 10 candidates.
- Maximum: 12 candidates.

Recommended theme allocation:
- Leadership Stability: 2 candidates.
- Rank Churn Avoidance: 2 candidates.
- Rank Reversal Pressure: 2 candidates.
- Leadership Concentration and Broadening: 2 candidates.
- Regime-Independent Rank Coherence: 2 candidates.
- Optional reserve: up to 2 diagnostic candidates only if pre-launch formula review shows the base 10 do not cover a theme cleanly.

Horizons:
- Score h1, h5, h10, and h20 for continuity with the existing discovery framework.
- Treat h10 as the central discovery horizon.
- Treat h20 as durability evidence.
- Treat h5 as a useful secondary diagnostic, especially for rank reversal pressure.
- Do not reinterpret rank-coherence as an h5-only family unless a later review explicitly designs a separate short-horizon program.

Artifact outputs:
- `artifacts/research/rank_coherence_family_discovery_v1/candidate_registry.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/panel_manifest.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/panel_diagnostics.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/statistical_redundancy_screening.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/approved_scoring_subset.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/candidate_ic_summary.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/family_theme_summary.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/redundancy_context.csv`
- `artifacts/research/rank_coherence_family_discovery_v1/manifest.json`

Expected review notes:
- `docs/research_notes/rank_coherence_family_discovery_panel_and_redundancy_review_v1.md`
- `docs/research_notes/rank_coherence_family_discovery_ic_review_v1.md`

Review checkpoints:
- Design approval before runner implementation.
- Pre-launch formula and candidate registry review.
- Panel and redundancy review before IC scoring.
- IC discovery review before any refinement design.
- Family-distinctness review before any validation-design discussion.

Runner recommendation:

Reuse the existing diversification discovery framework and helper patterns, but create a dedicated rank-coherence runner, for example `pipelines/run_rank_coherence_family_discovery_v1.py`. A dedicated runner is preferred because the family needs explicit guardrails against the prior persistence overlap. The runner should still follow existing research-only candidate registry and artifact conventions from `run_alpha_family_diversification_discovery_v1.py` and related Track B discovery runners.

The runner must remain research-only and must not modify production registries, validation standards, governance thresholds, survivor state, portfolio routing, or ML workflows.

## SECTION 7 - Success Criteria

Useful discovery evidence:
- At least one candidate has positive h10 evidence with supportive h5 or h20 context.
- Positive IC rate is directionally supportive, not just mean IC.
- Redundancy versus hostile/stress-repair, persistence lineage controls, and dispersion references is low enough to support a distinct-family interpretation.
- The candidate's economic story remains rank-coherence, not repair, compression, or post-drawdown persistence.
- The theme produces interpretable diagnostics even if not immediately refinement-worthy.

Diagnostic-only evidence:
- A theme reveals meaningful rank-structure behavior but weak or inconsistent IC.
- Evidence is horizon-limited, state-limited, or concentrated in one window.
- Redundancy is moderate but informative enough to map why rank-coherence overlaps with an existing family.
- The result helps prune future rank-family research without advancing a candidate.

Rejection:
- Candidate evidence is negative across h10/h20 without useful diagnostic interpretation.
- The signal is highly redundant with persistence, hostile/stress-repair, participation repair, or dispersion candidates.
- The formula depends on prohibited repair, stress, participation, liquidity, or dispersion inputs.
- The theme creates duplicate candidates or requires broad parameter expansion to look promising.

Validation-worthy evidence later:
- A candidate or theme shows positive h10 and supportive h20 behavior.
- IC IR and positive IC rate are consistent enough to survive a later refinement review.
- Evidence is not dominated by one state, one window, or one active subset.
- Stress-repair and persistence-lineage redundancy are low.
- The candidate has a clear formula lineage and does not rely on post-discovery tuning.
- A small refinement design can be written without expanding the candidate space or changing the family thesis.

Raw IC alone is insufficient. Rank-coherence should only advance if robustness, consistency, and distinctiveness all support the family claim.

## SECTION 8 - Final Recommendation

1. Is rank-coherence meaningfully distinct from persistence?

Yes, if it is designed as rank-structure behavior rather than post-drawdown rank survival. The prior `Rank Coherence Regime Transition` theme was too close to rank stability, so this program must prohibit drawdown conditioning and require explicit redundancy checks against the frozen persistence lineage.

2. Should rank-coherence be tested now?

Yes. Persistence has been frozen as conditional, dispersion remains exploratory, and the alpha inventory still needs a non-repair family. Rank-coherence is feasible with current OHLCV/rank infrastructure and does not require point-in-time metadata or ML.

3. What is the smallest disciplined discovery batch?

The smallest disciplined batch is 10 candidates across five themes, with a hard maximum of 12 if pre-launch review requires up to two diagnostic reserves. This is small enough to audit and large enough to test whether rank-coherence is broader than one near-duplicate persistence formula.

4. What should the next Codex task be?

The next Codex task should be an implementation-only plan for `rank_coherence_family_discovery_v1`. It should define the exact candidate registry, formula ingredients, runner structure, artifact paths, dry-run checks, and panel/redundancy review process. It should not execute discovery, run validation, run refinement, modify governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.

## Design Caveat

This document only designs the rank-coherence family discovery program. It does not execute discovery, produce panels, score IC, run validation, run refinement, change governance, change thresholds, register production artifacts, implement ML, or promote/demote candidates.
