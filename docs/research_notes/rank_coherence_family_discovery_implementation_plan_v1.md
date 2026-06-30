# Rank-Coherence Family Discovery Implementation Plan v1

Date: 2026-06-18

Project: Project Underdog

Run id: `rank_coherence_family_discovery_v1`

Status: `PLAN_ONLY`

Scope: implementation-only plan for the approved rank-coherence family discovery program. No code changes, discovery execution, candidate panel generation, IC scoring, refinement, validation, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Strategic Context

Rank-coherence is the next alpha-family frontier because the current inventory remains concentrated in hostile/stress-repair, with persistence frozen as a conditional candidate and dispersion still exploratory. The persistence validation sequence showed that cross-sectional rank structure can contain alpha, but the post-drawdown persistence lineage appears to have reached its practical current limit. The next step should therefore test rank structure without extending the same post-drawdown formula family.

This implementation plan turns `rank_coherence_family_discovery_design_v1.md` into a concrete, auditable path for a small discovery batch. The program should test whether leadership stability, rank churn, rank reversal pressure, leadership concentration, and regime-independent rank coherence represent a genuinely new alpha family.

The implementation must preserve Project Underdog's research discipline:
- Use current OHLCV/rank infrastructure.
- Reuse existing diversification discovery conventions where possible.
- Keep rank-coherence independent from frozen persistence lineage controls.
- Prevent hostile/stress-repair, participation-repair, dispersion, or volatility-compression contamination.
- Produce research artifacts only.

## SECTION 2 - Candidate Registry Plan

Registry schema:
- `candidate_id`
- `signal_name`
- `family`
- `theme`
- `feature_group`
- `horizon`
- `redundancy_risk`
- `research_status`
- `mechanism_thesis`
- `run_id`
- `expected_panel_path`

Required constants:
- `family`: `rank_coherence` for all primary candidates.
- `research_status`: `RESEARCH_ONLY`.
- `run_id`: `rank_coherence_family_discovery_v1`.
- Candidate count: exactly 10 for the initial implementation.
- Hard maximum: 12 candidates if a later pre-launch review approves no more than two diagnostic reserve candidates.

Initial 10-candidate registry:

| candidate_id | family | theme | horizon | feature_group | intended economic hypothesis | redundancy risk | expected artifact path |
|---|---|---|---|---|---|---|---|
| `rank_coherence_leadership_stability_01` | `rank_coherence` | Leadership Stability | h10-h20 | `leadership_stability` | Durable top-ranked securities outperform when leadership remains orderly across adjacent windows. | medium versus momentum and persistence controls | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/leadership_rank_retention_10_20.parquet` |
| `rank_coherence_leadership_stability_02` | `rank_coherence` | Leadership Stability | h10-h20 | `leadership_stability` | Securities with high cross-window rank agreement outperform because leadership is not transient. | medium versus momentum and persistence controls | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/cross_window_rank_agreement_10_20.parquet` |
| `rank_coherence_churn_avoidance_01` | `rank_coherence` | Rank Churn Avoidance | h10-h20 | `rank_churn` | Improving securities with low rank churn outperform noisy improvers. | high versus persistence lineage | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/churn_adjusted_rank_improvement_20.parquet` |
| `rank_coherence_churn_avoidance_02` | `rank_coherence` | Rank Churn Avoidance | h10-h20 | `rank_churn` | Securities with rank turnover below universe rank turnover retain more durable sponsorship. | high versus persistence lineage | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/relative_rank_turnover_resilience_20.parquet` |
| `rank_coherence_reversal_pressure_01` | `rank_coherence` | Rank Reversal Pressure | h5-h10 | `rank_reversal_pressure` | Short-window rank shocks that disagree with medium-window rank structure mean-revert. | medium-high versus reversal baselines | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/rank_shock_reversion_pressure_5_20.parquet` |
| `rank_coherence_reversal_pressure_02` | `rank_coherence` | Rank Reversal Pressure | h5-h10 | `rank_reversal_pressure` | Abrupt rank acceleration unsupported by broader rank order creates reversal pressure. | medium-high versus reversal baselines | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/rank_acceleration_disagreement_5_20.parquet` |
| `rank_coherence_concentration_01` | `rank_coherence` | Leadership Concentration and Broadening | h10-h20 | `leadership_concentration` | Durable leaders outperform in concentrated leadership regimes when top-rank membership remains coherent. | medium versus momentum and breadth repair | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/leadership_concentration_quality_20.parquet` |
| `rank_coherence_concentration_02` | `rank_coherence` | Leadership Concentration and Broadening | h10-h20 | `leadership_concentration` | New entrants into coherent leadership groups outperform during rank-map broadening. | medium versus breadth and participation repair | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/leadership_broadening_entry_20.parquet` |
| `rank_coherence_regime_independent_01` | `rank_coherence` | Regime-Independent Rank Coherence | h10-h20 | `regime_independent_coherence` | Securities with stable rank agreement across ordinary states outperform without requiring stress repair. | medium versus prior transition-rank stability | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/state_neutral_rank_coherence_20.parquet` |
| `rank_coherence_regime_independent_02` | `rank_coherence` | Regime-Independent Rank Coherence | h10-h20 | `regime_independent_coherence` | Rank coherence that persists before and after non-hostile transitions identifies durable relative leadership. | medium versus transition-state dynamics | `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/nonhostile_transition_rank_coherence_20.parquet` |

Reserve policy:
- Reserve capacity is limited to two candidates.
- Reserve candidates may only fill a documented theme coverage gap found during pre-launch formula review.
- Reserve candidates must not introduce new themes, new families, or new horizons.
- Reserve candidates must be added only in a separate approved implementation change, not during discovery execution.

## SECTION 3 - Feature and Formula Ingredient Plan

This section defines implementation ingredients only. It does not execute formulas.

Base rank measures:
- Cross-sectional return rank over short and medium windows, such as 5, 10, and 20 trading days.
- Relative return rank versus the active universe.
- Rank percentile scaled consistently with existing discovery runners.
- Rank difference between adjacent windows.
- Rank agreement between independently computed windows.

Rank stability measures:
- Rolling rank standard deviation.
- Top-quintile or top-decile retention.
- Cross-window rank correlation at the security level.
- Stability of rank membership across h5/h10 and h10/h20 windows.
- Rank persistence without drawdown conditioning.

Rank churn measures:
- Rolling absolute rank change.
- Rank turnover relative to universe-level rank turnover.
- Improvement slope divided by or penalized by rank churn.
- Churn-adjusted rank improvement.
- Churn resilience measured without post-drawdown windows, downtrend repair windows, or frozen persistence formula components.

Rank reversal pressure measures:
- Short-window rank shock relative to medium-window rank anchor.
- Rank acceleration minus rank agreement.
- Rank disagreement between h5 and h20 structure.
- Clipped one-day rank shock to reduce event-gap dominance.
- Directional mismatch between abrupt ascent/deterioration and broader rank order.

Leadership concentration measures:
- Top-rank membership stability.
- Rank-map concentration based on rank membership, not volume participation or liquidity repair.
- Rank entropy or leadership share computed from cross-sectional rank membership.
- Entry into stable leadership groups.
- Distance from crowded top-leadership membership.

Regime-dependent rank-coherence measures:
- State-neutral rank agreement across ordinary, benign, and transition states.
- Rank coherence around non-hostile transitions.
- State labels used only as attribution or non-hostile context, not stress-repair activation.
- No hostile trend, weak breadth, liquidity repair, participation repair, panic repair, or failed-breakout recovery input as a primary formula feature.

Formula guardrails:
- Do not use `post_drawdown_persistence_churn_adjusted_20`, `post_drawdown_persistence_core_20`, or `post_drawdown_persistence_20` as source features.
- Do not use drawdown depth or post-drawdown event windows.
- Do not use dispersion acceleration, pairwise correlation compression, volatility compression, participation repair, liquidity repair, or weak-breadth repair as primary inputs.
- All formulas should be auditable, deterministic, and based on existing panel-style feature transformations.

## SECTION 4 - Runner Structure

Suggested runner: `pipelines/run_rank_coherence_family_discovery_v1.py`.

The runner should be dedicated to rank-coherence while reusing existing diversification discovery patterns. It should follow the structure of `run_alpha_family_diversification_discovery_v1.py`, including registry validation, research-only guardrails, artifact directories, metadata redundancy screening, statistical redundancy screening compatibility, and manifest flags.

Required modes:
- `--describe`: print run id, research-only scope, artifact layout, and guardrails.
- `--list-candidates`: print the candidate registry without writing artifacts.
- `--dry-run`: validate registry and create scaffold/placeholder artifacts only; do not generate candidate panels.
- `--run`: later research-only mode for candidate panel generation after implementation approval; not part of this planning task.

Registry validation:
- Use `pipelines.utils.registry_validation.validate_registry_df`.
- Enforce required fields: `candidate_id`, `signal_name`, `family`, `theme`, `feature_group`, `horizon`, `redundancy_risk`, `research_status`, and `run_id`.
- Enforce unique `candidate_id` and `signal_name`.
- Enforce candidate count between 8 and 12, with initial implementation count exactly 10.
- Enforce `family = rank_coherence`.
- Enforce `research_status = RESEARCH_ONLY`.

Metadata redundancy screening:
- Use the existing `pipelines.utils.redundancy_screening.screen_registry_df` pattern.
- Write metadata screening outputs before any IC scoring.
- Flag theme overlap, candidate-id prefix overlap, feature-group overlap, horizon overlap, and known contamination keywords.

Statistical redundancy screening compatibility:
- Use long candidate panel format compatible with the existing statistical redundancy utility.
- After panel generation in a later task, compute pairwise value correlation, rank correlation, overlap observations, overlap dates, overlap tickers, candidate panel paths, and comparison panel paths.
- Include comparison references for persistence lineage, hostile/stress-repair references, and dispersion references where available.

Artifact writing:
- Write artifacts only under `artifacts/research/rank_coherence_family_discovery_v1/`.
- Write manifest guardrail flags that explicitly record no validation, no refinement, no governance mutation, no threshold mutation, no production registration, no ML, and no promotion/demotion.
- Do not write to production registries, survivor/watchlist tables, governance folders outside the research artifact namespace, portfolio outputs, or ML outputs.

## SECTION 5 - Artifact Structure

Planned artifact root:

`artifacts/research/rank_coherence_family_discovery_v1/`

Planned folders:

`candidate_inventory/`
- `candidate_registry.csv`
- `candidate_registry_schema_check.csv`
- `candidate_registry_readme.md`

`candidate_panels/`
- One parquet panel per generated signal in a later execution task.
- One metadata JSON per generated signal in a later execution task.
- No files should be created here during dry-run unless the implementation explicitly writes a placeholder schema.

`discovery_summary/`
- `framework_scaffold_summary.md`
- `panel_manifest.csv`
- `candidate_panel_generation_summary.csv`
- `family_theme_summary.csv`

`diagnostics/`
- `source_panel_inputs.csv`
- `panel_diagnostics.csv`
- `structural_quality_diagnostics.csv`
- `prohibited_feature_review.csv`
- `guardrail_checklist.csv`

`redundancy_screening/`
- `metadata_redundancy_screening.csv`
- `statistical_redundancy_screening.csv`
- `persistence_lineage_redundancy.csv`
- `stress_repair_redundancy.csv`
- `dispersion_reference_redundancy.csv`
- `approved_scoring_subset_recommendation.csv`

`ic_discovery/`
- `approved_scoring_subset.csv`
- `candidate_horizon_ic_scores.csv`
- `candidate_ic_summary.csv`
- `daily_ic_by_candidate_horizon.csv`
- `family_theme_ic_summary.csv`
- `horizon_ic_summary.csv`
- `manifest.json`

`governance_review/`
- `research_only_guardrail_review.csv`
- `no_governance_mutation_confirmation.csv`
- `no_production_registration_confirmation.csv`

Root-level files:
- `manifest.json`
- `README.md`, optional.

## SECTION 6 - Dry-Run and Safety Checks

Required dry-run checks before any discovery execution:

Registry schema validation:
- Required columns present.
- Unique `candidate_id` and `signal_name`.
- No missing `family`, `theme`, `feature_group`, `horizon`, `redundancy_risk`, `research_status`, or `run_id`.
- Allowed redundancy risk labels only: `low`, `medium`, `medium-high`, `high`, or `unknown`.

Candidate count cap:
- Initial registry must contain exactly 10 candidates.
- Runner must fail if candidate count exceeds 12.
- Runner must require explicit implementation-plan update if reserve candidates are added.

Family/theme labeling:
- All candidates must use `family = rank_coherence`.
- Themes must be one of:
  - Leadership Stability
  - Rank Churn Avoidance
  - Rank Reversal Pressure
  - Leadership Concentration and Broadening
  - Regime-Independent Rank Coherence
- Each theme should have exactly two candidates in the initial implementation.

No production paths:
- Artifact writes must be confined to `artifacts/research/rank_coherence_family_discovery_v1/`.
- No writes to production registry, survivor registry, portfolio outputs, ML outputs, or validation outputs.

No governance mutation:
- Runner must only write research-only confirmation files under the planned `governance_review/` folder.
- No governance config, thresholds, survivor state, or production review files may be changed.

No threshold mutation:
- Runner must read existing standards only where necessary for compatibility.
- No validation gates, discovery thresholds, schema rules, or governance criteria may be modified.

No ML integration:
- No model training, feature learning, prediction model, optimizer, or portfolio construction should be included.

No validation execution:
- Dry-run and panel-generation modes must not compute validation windows, WFV validation classifications, or validation outcomes.

## SECTION 7 - Panel and Redundancy Review Process

Pre-IC process:

1. Panel generation.

After implementation approval, run the dedicated runner in research-only `--run` mode to generate candidate panels. Panels should use the long format:
- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `family`
- `theme`
- `horizon`

2. Panel completeness checks.

Review:
- Row counts.
- Ticker counts.
- Date coverage.
- Missingness.
- Finite value share.
- Minimum active observations per date.
- Signal distribution bounds.
- Panel path and metadata presence.

3. Metadata redundancy review.

Before IC scoring, review:
- Candidate-id prefix crowding.
- Theme overlap.
- Feature-group overlap.
- Horizon overlap.
- Prohibited feature keywords.
- Any accidental persistence, hostile/stress-repair, participation-repair, dispersion, or volatility-compression framing.

4. Statistical redundancy review.

After panels exist, compute:
- Pairwise value correlation among rank-coherence candidates.
- Pairwise rank correlation among rank-coherence candidates.
- Redundancy versus frozen persistence lineage controls.
- Redundancy versus hostile/stress-repair references.
- Redundancy versus dispersion references.
- Overlap observations, dates, and tickers.

5. Candidate subset selection for IC scoring.

Select a reduced IC subset only after panel and redundancy review. The subset should:
- Preserve at least one representative from each viable theme when possible.
- Exclude likely duplicates.
- Hold high-overlap persistence-like candidates for manual review.
- Exclude candidates that show prohibited repair or dispersion contamination.
- Document all excluded and held candidates before IC scoring.

## SECTION 8 - Discovery Execution Sequence

After this implementation plan is approved, the work should proceed in this order:

1. Scaffold implementation.

Create `pipelines/run_rank_coherence_family_discovery_v1.py` with registry, guardrails, modes, artifact paths, and dry-run scaffold writing. Do not execute discovery during implementation unless the task explicitly approves it.

2. Dry-run review.

Run `--describe`, `--list-candidates`, and `--dry-run` only after implementation approval. Review registry validation, artifact paths, guardrail files, and metadata redundancy outputs.

3. Panel generation.

Run research-only `--run` only after dry-run review approves the registry and formula definitions. Generate candidate panels and panel manifest.

4. Redundancy review.

Create `rank_coherence_family_discovery_panel_and_redundancy_review_v1.md` from generated panel and redundancy artifacts. Select the approved IC scoring subset.

5. Approved subset IC scoring.

Run a separate IC discovery pass only for the approved subset. Score h1, h5, h10, and h20, with h10 as central discovery horizon and h20 as durability evidence.

6. IC review.

Create `rank_coherence_family_discovery_ic_review_v1.md`. Classify candidates as useful discovery evidence, diagnostic-only, rejection, or potential refinement-design candidate.

7. Refinement eligibility audit.

Only if IC review supports it, create a review-only refinement eligibility audit. Do not proceed automatically to refinement.

## SECTION 9 - Risks and Mitigations

Accidental persistence duplication:
- Risk: rank churn and rank stability features can recreate `post_drawdown_persistence_churn_adjusted_20`.
- Mitigation: prohibit drawdown/post-drawdown ingredients and require redundancy checks against the full persistence lineage.

Hostile/stress-repair contamination:
- Risk: rank structure may look useful only in recovery or hostile-normalization states.
- Mitigation: prohibit stress-repair features as primary inputs and require state attribution/redundancy diagnostics against hostile/stress references.

Rank-coherence/persistence overlap:
- Risk: the family becomes a relabeled persistence extension.
- Mitigation: define rank-coherence around universe rank structure, leadership agreement, concentration, and rotation rather than event-conditioned survival.

Discovery sprawl:
- Risk: rank variants can multiply quickly.
- Mitigation: initial batch is exactly 10 candidates with hard maximum 12; reserves require a separate approved change.

Horizon chasing:
- Risk: h5 may look best and pull the program away from the h10/h20 diversification goal.
- Mitigation: score h1/h5/h10/h20 but pre-declare h10 as central and h20 as durability; h5 remains diagnostic except for the rank reversal pressure theme.

False diversification:
- Risk: candidates appear new by name but are redundant with momentum, reversal, participation repair, dispersion, or persistence.
- Mitigation: require redundancy context before IC scoring and assess distinctiveness before any refinement recommendation.

## SECTION 10 - Final Recommendation

1. Is rank-coherence implementation justified now?

Yes. Persistence is frozen as conditional, dispersion remains exploratory, and the inventory still needs a non-repair alpha-family test. Rank-coherence is feasible with current infrastructure and has a clear design mandate.

2. Should it reuse the diversification framework or have a dedicated runner?

It should reuse the diversification framework patterns but have a dedicated runner. A dedicated `run_rank_coherence_family_discovery_v1.py` is justified because the main implementation risk is accidental overlap with frozen persistence, and that guardrail should be explicit in the runner.

3. What is the minimum viable implementation?

The minimum viable implementation is a research-only runner with a 10-candidate registry, registry validation, `--describe`, `--list-candidates`, `--dry-run`, future `--run` panel generation support, artifact scaffolding under `artifacts/research/rank_coherence_family_discovery_v1/`, metadata redundancy screening, and statistical redundancy compatibility.

4. What should the next Codex task be?

The next Codex task should be to scaffold `pipelines/run_rank_coherence_family_discovery_v1.py` and its research-only artifact layout exactly from this plan. That task should include code implementation and dry-run capability only; it should not execute discovery, generate candidate panels, run IC scoring, run refinement, run validation, modify governance, change thresholds, register production candidates, implement ML, or promote/demote candidates.

## Planning Caveat

This document is an implementation plan only. It does not change code, execute discovery, generate candidate panels, score IC, run refinement, run validation, modify governance, register production artifacts, change thresholds, implement ML, or promote/demote any candidate.
