# Rank-Coherence Framework Post-Scaffold Dry-Run Review v1

Date: 2026-06-18

Project: Project Underdog

Run id reviewed: `rank_coherence_family_discovery_v1`

Scope: review-only post-scaffold dry-run review. No candidate panels were generated, no discovery was executed, no IC scoring was run, no refinement or validation was run, no governance or threshold mutation was performed, no production registration was performed, no ML was implemented, and no candidate was promoted or demoted.

## SECTION 1 - Executive Summary

The rank-coherence scaffold is complete for its intended research-only purpose. The runner exists, implements the approved 10-candidate registry, creates the required artifact folder structure, writes scaffold artifacts on `--dry-run`, and explicitly records guardrail flags in the manifest.

Dry-run readiness is satisfactory. The runner supports `--describe`, `--list-candidates`, and `--dry-run`. The reserved `--run` mode is intentionally disabled in scaffold v1 and exits with a clear message that no panel generation or discovery was executed.

Safety status is satisfactory. The manifest and guardrail artifacts state that panel generation, discovery, IC scoring, refinement, validation, governance mutation, threshold mutation, production registration, ML integration, and candidate promotion/demotion were not performed.

Panel generation implementation can proceed as the next implementation task, provided it remains a separate approved task and preserves the same guardrail structure.

## SECTION 2 - Registry Review

Candidate count:
- Confirmed exactly 10 candidates in `candidate_registry.csv`.
- Confirmed hard maximum candidate count of 12 is represented in the runner and manifest.

Required metadata fields:
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

The required task fields are present, including `candidate_id`, `family`, `theme`, `horizon`, `feature_group`, `intended_economic_hypothesis`, `redundancy_risk`, `research_status`, and `expected_artifact_path`.

Family labels:
- All candidates use `family = rank_coherence`.

Theme labels:
- `Leadership Stability`: 2 candidates.
- `Rank Churn Avoidance`: 2 candidates.
- `Rank Reversal Pressure`: 2 candidates.
- `Leadership Concentration and Broadening`: 2 candidates.
- `Regime-Independent Rank Coherence`: 2 candidates.

Horizon labels:
- h10-h20 candidates: 8.
- h5-h10 candidates: 2, both within the rank reversal pressure theme as designed.

Persistence/stress-repair contamination:
- No candidate is labeled as persistence, hostile/stress-repair, participation repair, liquidity repair, dispersion, or volatility compression.
- Two rank-churn candidates correctly carry high redundancy risk versus persistence lineage, which is expected and useful for later screening.
- No accidental production or validation status appears in the registry.

## SECTION 3 - Artifact Review

Required artifact folders exist:
- `candidate_inventory`
- `candidate_panels`
- `discovery_summary`
- `diagnostics`
- `redundancy_screening`
- `ic_discovery`
- `governance_review`

Manifest:
- `artifacts/research/rank_coherence_family_discovery_v1/manifest.json` exists.
- Manifest records `candidate_count: 10`.
- Manifest records `hard_max_candidate_count: 12`.
- Manifest records all major execution/governance flags as false.

Registry artifact:
- `candidate_inventory/candidate_registry.csv` exists and contains the 10-candidate registry.
- `candidate_inventory/candidate_registry_schema_check.csv` exists.
- `candidate_inventory/candidate_registry_readme.md` exists.

Scaffold summary:
- `discovery_summary/framework_scaffold_summary.md` exists and describes scaffold-only behavior.

Candidate panels:
- `candidate_panels/` exists as a reserved directory.
- No files are present in `candidate_panels/` after dry-run review.
- No parquet candidate panels were generated.

## SECTION 4 - Guardrail Review

Confirmed by runner behavior, tests, and manifest:
- No discovery execution.
- No panel generation.
- No IC scoring.
- No validation execution.
- No refinement execution.
- No governance mutation.
- No threshold changes.
- No production registration.
- No ML integration.
- No candidate promotion or demotion.

The reserved `--run` mode returns a refusal message and does not generate candidate panels. This is an appropriate safety feature for scaffold v1.

## SECTION 5 - Test Review

Scaffold tests reviewed:
- `test_candidate_registry_shape_and_required_columns`
- `test_list_candidates_works`
- `test_dry_run_creates_scaffold_artifacts_without_panels`

Current test result:
- `pytest tests/test_rank_coherence_discovery_scaffold.py -q`
- Result: 3 passed.

Dry-run behavior:
- Tests verify dry-run succeeds.
- Tests verify required directories are created.
- Tests verify registry and manifest are written.
- Tests verify manifest guardrail flags are false.
- Tests verify no parquet panels exist in `candidate_panels/`.

List-candidates behavior:
- Tests verify `--list-candidates` succeeds and includes both first and final registry candidates.

Missing coverage:
- Tests do not explicitly assert that `--run` returns the reserved-mode refusal.
- Tests do not explicitly inspect metadata redundancy screening columns.
- Tests do not explicitly inspect guardrail checklist CSV content.

These are recommended improvements, not blockers, because manual review confirmed `--run` refusal and the existing tests cover the primary scaffold safety properties.

## SECTION 6 - Required Fixes

Blocking fixes:
- None.

Recommended improvements:
- Add a lightweight test that `--run` exits nonzero and prints the reserved-mode refusal message.
- Add a lightweight test that `metadata_redundancy_screening.csv` contains the expected advisory screening columns.
- Add a lightweight test that `diagnostics/guardrail_checklist.csv` contains false/not-performed entries for panel generation, discovery, IC scoring, refinement, validation, governance mutation, threshold mutation, production registration, ML, and promotion/demotion.

Optional improvements:
- Add `--describe` coverage to the scaffold test file.
- Add a root-level `README.md` under the scaffold artifact directory during dry-run.
- Add a small note in the runner output that `candidate_panels/` is intentionally empty after dry-run.

## SECTION 7 - Final Recommendation

1. Is the scaffold safe and complete?

Yes. The scaffold is safe and complete for its intended purpose. It implements the approved registry, creates the required artifact structure, writes dry-run artifacts, and prevents panel generation and downstream execution.

2. Is it ready for panel generation implementation?

Yes. It is ready for a separate panel generation implementation task. That task should add formulas and panel-writing logic only under the same research-only namespace and should not run IC scoring, refinement, validation, governance mutation, production registration, threshold mutation, ML, or candidate promotion/demotion.

3. Are any fixes required first?

No blocking fixes are required first. The recommended test additions would improve confidence but are not required before panel generation implementation.

4. What should the next Codex task be?

The next Codex task should be `Rank-Coherence Candidate Panel Generation Implementation v1`. It should implement formula construction and panel generation behind the existing reserved `--run` mode, preserve the dry-run behavior, write panels only under `artifacts/research/rank_coherence_family_discovery_v1/candidate_panels/`, refresh panel manifests and redundancy compatibility artifacts, and explicitly avoid IC scoring, refinement, validation, governance mutation, production registration, threshold changes, ML, and promotion/demotion.

## Review Caveat

This was a review-only assessment. It did not generate panels, execute discovery, score IC, run refinement, run validation, modify governance, register production candidates, change thresholds, implement ML, or promote/demote candidates.
