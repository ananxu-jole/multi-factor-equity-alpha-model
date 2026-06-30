# Rank-Coherence Family Discovery Framework Scaffold v1

Date: 2026-06-18

Project: Project Underdog

Run id: `rank_coherence_family_discovery_v1`

Scope: research-only scaffold implementation. No candidate panels were generated, no discovery was executed, no IC scoring was run, no refinement or validation was run, no governance or threshold mutation was performed, no production registration was performed, no ML was implemented, and no candidate was promoted or demoted.

## Files Created

- `pipelines/run_rank_coherence_family_discovery_v1.py`
- `tests/test_rank_coherence_discovery_scaffold.py`
- `docs/research_notes/rank_coherence_family_discovery_framework_scaffold_v1.md`

## Registry Structure

The runner implements the exact 10-candidate rank-coherence registry from `rank_coherence_family_discovery_implementation_plan_v1.md`.

Registry fields:
- `candidate_id`
- `signal_name`
- `family`
- `theme`
- `horizon`
- `feature_group`
- `intended_economic_hypothesis`
- `mechanism_thesis`
- `redundancy_risk`
- `redundancy_risk_detail`
- `research_status`
- `expected_artifact_path`
- `run_id`

All candidates use:
- `family = rank_coherence`
- `research_status = RESEARCH_ONLY`
- `run_id = rank_coherence_family_discovery_v1`

The runner enforces an initial count of 10 candidates and a hard maximum of 12.

## Artifact Structure

`--dry-run` creates the research-only scaffold under:

`artifacts/research/rank_coherence_family_discovery_v1/`

Required folders:
- `candidate_inventory`
- `candidate_panels`
- `discovery_summary`
- `diagnostics`
- `redundancy_screening`
- `ic_discovery`
- `governance_review`

The `candidate_panels` directory is created only as an empty reserved location. Dry-run does not write parquet panels.

## Dry-Run Behavior

`--dry-run` performs:
- candidate registry validation
- candidate count cap enforcement
- candidate registry artifact writing
- manifest writing
- scaffold summary writing
- metadata-only redundancy screening
- empty statistical redundancy compatibility placeholder writing
- guardrail checklist writing

`--dry-run` does not:
- generate candidate panels
- execute discovery
- run IC scoring
- run refinement
- run validation
- touch production paths
- mutate governance
- change thresholds
- implement ML
- promote or demote candidates

`--run` is intentionally reserved and disabled in scaffold v1.

## Guardrails

The scaffold manifest records:
- `panel_generation_executed: false`
- `discovery_executed: false`
- `ic_scoring_executed: false`
- `refinement_executed: false`
- `validation_executed: false`
- `production_registration: false`
- `governance_modified: false`
- `thresholds_modified: false`
- `ml_integration: false`
- `candidate_promotion_or_demotion: false`

The only artifact namespace used by the runner is:

`artifacts/research/rank_coherence_family_discovery_v1/`

## Next Step

The next Codex task should be a scaffold dry-run review. It should run `--describe`, `--list-candidates`, and `--dry-run`, inspect the registry and metadata-only redundancy artifacts, and confirm the panel directory remains empty before any later panel-generation task is considered.

## Scaffold Caveat

This scaffold prepares the framework only. It does not implement rank-coherence formulas, generate panels, score IC, run discovery, run refinement, run validation, mutate governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.
