# Alpha Family Diversification Implementation Plan v1

Date: 2026-06-17

Run id: `alpha_family_diversification_discovery_v1`

Status: `PLAN_ONLY`

## Scope

This document translates the approved diversification discovery specification in `docs/research_notes/alpha_family_diversification_discovery_specification_v1.md` into an implementation-ready execution plan.

The plan is research-only and intentionally excludes:
- production registration, governance changes, or candidate promotion
- modifications to validation anchors, survivor/watchlist state, or portfolio/ML routing
- threshold, schema, or gate changes
- any use of the results outside disciplined research inspection and redundancy screening

## Implementation Architecture

This execution plan reuses the repo's existing research discovery infrastructure and documented runner patterns.

Key implementation components:
- `pipelines/run_track_b_v6_focused_discovery.py` as the reference Track B discovery engine and guardrail model
- a new dedicated research-only runner script such as `pipelines/run_alpha_family_diversification_discovery_v1.py`
- candidate metadata registry definitions in the runner script with `research_status: RESEARCH_ONLY`
- research artifacts written under `artifacts/research/alpha_family_diversification_discovery_v1/`
- a results note written to `docs/research_notes/alpha_family_diversification_discovery_v1_results.md`
- optional regulated cache use from `artifacts/panels/` and `artifacts/ic/` on a dry-run basis

## Phase 1 – Preparation and Design Approval

1. Confirm the approved themes and anti-redundancy controls in the specification document.
2. Define the initial candidate map for the first execution batch: 15–18 candidates across 5 themes.
3. Document the execution guardrails explicitly in the runner script, including:
   - `RESEARCH_ONLY_GUARDRAIL`
   - family axis labels: `dispersion` and `persistence`
   - no production or portfolio routing
   - explicit rejection of repair/recovery framing
4. Identify required base features and transformation candidates for each theme.
5. Finalize the planned artifact structure and candidate registry metadata.

## Phase 2 – Candidate Generation and Runner Design

1. Create a candidate registry in the runner with:
   - signal names
   - family labels
   - theme names
   - event/thesis descriptions
   - expected horizon focus
   - `framework: alpha_family_diversification_discovery_v1`
2. For each theme, implement candidate construction logic using existing feature inputs and transformations:
   - dispersion themes: cross-sectional dispersion, correlation compression, dispersion anomaly measures
   - persistence themes: rank stability, rank coherence, rank churn, participation stability
3. Keep candidate definitions conservative and clearly aligned to the family axis.
4. Implement explicit candidate-level metadata in the runner:
   - `run_id`
   - `research_status`
   - `framework`
   - `mechanism_thesis`
   - `expected_horizon`
5. Use existing runner helper functions where available, for example from `run_track_b_v6_focused_discovery.py` and `run_track_b_robustness_discovery_v3.py`.

## Phase 3 – Research Execution

1. Execute an initial dry run to validate the runner without writing artifacts:
   - `python pipelines/run_alpha_family_diversification_discovery_v1.py --dry-run --quiet`
2. Confirm the runner does not mutate production state, candidate registry, or validation logic.
3. If the dry run passes, execute the research-only run to generate artifacts:
   - `python pipelines/run_alpha_family_diversification_discovery_v1.py --run --quiet`
4. Use optional cache controls if available and input caches are already valid:
   - `--use-panel-cache`
   - `--use-daily-ic-cache`
   - `--rebuild-panel-cache` / `--rebuild-daily-ic-cache` only when input caches are stale or inconsistent
5. Produce artifact outputs under `artifacts/research/alpha_family_diversification_discovery_v1/`, including:
   - candidate panels and scores
   - daily IC tables
   - redundancy diagnostics
   - summary metadata and manifest files
   - research note draft outputs

## Phase 4 – Orthogonality and Redundancy Screening

1. Perform a pre-launch redundancy review on the candidate matrix:
   - confirm each theme is distinct from existing participation/stress and volatility candidates
   - verify that dispersion themes are not framed as repair/recovery
   - verify that persistence themes are defined by explicit rank behavior
2. After the run, compute candidate-level orthogonality metrics versus current library:
   - pairwise correlation with existing participation/stress candidates
   - co-activation counts with current library and `track_b` reference candidates
   - regime activation overlap with hostile/stress repair states
3. Apply the specification's quantitative control thresholds:
   - reject themes showing correlation > 0.15 and co-activation > 0.30 to the current library
   - require at least one candidate in each family to demonstrate a distinct activation/regime signature
4. Summarize redundancy screening results in:
   - `alpha_family_diversification_discovery_v1_redundancy_report.csv`
   - `alpha_family_diversification_discovery_v1_orthogonality_summary.csv`
   - `alpha_family_diversification_discovery_v1_manifest.json`

## Phase 5 – Result Classification and Next Steps

1. Classify the batch outcomes using the specification categories:
   - Genuine new alpha family
   - Variant of an existing family
   - Diagnostic-only result
   - Full rejection
2. Require a documented family-level decision for each theme:
   - keep for potential refinement
   - archive as diagnostic insight
   - reject as redundant
3. Capture the decision rationale in the result note and in a short closing memo.
4. If a theme is eligible for refinement, define the next implementation step separately; do not automatically advance candidates.
5. If the batch identifies a successful new family, preserve the runner output and candidate registry as research evidence, but do not promote or register the candidate until a separate governance memo is approved.

## Planned Artifacts

- `docs/research_notes/alpha_family_diversification_discovery_v1_results.md`
- `artifacts/research/alpha_family_diversification_discovery_v1/`
- `artifacts/research/alpha_family_diversification_discovery_v1/manifest.json`
- `artifacts/research/alpha_family_diversification_discovery_v1/candidate_registry.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/redundancy_report.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/orthogonality_summary.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/panel_diagnostics.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/daily_ic_summary.csv`

## Governance Checkpoints

- Pre-launch: review and approve candidate themes, feature inputs, and anti-redundancy controls.
- Mid-batch: inspect whether the first subset of candidates preserves family distinction and whether any theme should be pruned.
- Post-batch: classify outcomes and decide whether the batch yields a new family, requires refinement, or should be archived.
- Metadata boundary confirmation: verify that no metadata-enriched research logic or point-in-time metadata has been introduced before the batch is closed.

## Risks and Mitigations

- Overfitting risk: keep candidate count disciplined and favor hypothesis clarity over quantity.
- Family contamination risk: enforce the family axis definitions for dispersion and persistence.
- False diversification risk: use explicit orthogonality screens versus existing participation/stress candidates.
- Horizon concentration risk: preserve h10-h20 focus but allow limited h5 exploratory checks where they help distinguish families.

## Out of Scope

Do not include any of the following in this implementation plan:
- production candidate promotion or registration
- portfolio construction, ML modeling, or blending integration
- changes to existing pipeline validation thresholds, schemas, or survivor lists
- creation of new permanent `configs/` or `sql/` artifacts for the batch
- any research activity that would require external governance approval outside this research-only plan

## Next Task

After this plan is approved, the next operational task is to implement the discovery runner and candidate registry for the first batch, then execute the dry-run review and initial research-only run.
