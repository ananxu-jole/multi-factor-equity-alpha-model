# Alpha Family Diversification Framework Implementation v1

Date: 2026-06-17

## Files created

- `pipelines/run_alpha_family_diversification_discovery_v1.py`
- `artifacts/research/alpha_family_diversification_discovery_v1/candidate_inventory/candidate_registry.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/manifest.json`
- `artifacts/research/alpha_family_diversification_discovery_v1/discovery_summary/framework_scaffold_summary.md`
- `artifacts/research/alpha_family_diversification_discovery_v1/diagnostics/panel_diagnostics_placeholder.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/redundancy_screening/redundancy_screening_placeholder.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/governance_review/framework_governance_review.csv`

## Artifact structure

The artifact scaffold includes:

- `candidate_inventory/` for the approved candidate registry and inventory outputs
- `discovery_summary/` for notes and implementation summaries
- `diagnostics/` for panel diagnostics and related inspection files
- `redundancy_screening/` for overlap and contamination diagnostics
- `governance_review/` for governance checklist and audit support

## Candidate registry structure

The runner defines a static registry of approved diversification candidates with the following metadata fields:

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

The registry is separated into:

- Dispersion family candidates (three themes)
- Persistence family candidates (two themes)

## Safety guardrails

The runner is explicitly research-only:

- It contains a `RESEARCH_ONLY_GUARDRAIL` string.
- It does not implement production candidate registration.
- It does not mutate survivor/watchlist state.
- It does not change validation thresholds or governance.
- It does not route outputs into portfolio, ML, or optimization.
- The `--run` flag is intentionally disabled and returns an explanatory error.

## Dry-run readiness

Supported modes:

- `--list-candidates`: inspect the approved candidate registry without running discovery
- `--describe`: summarize the framework and artifact layout
- `--dry-run`: create scaffold artifact directories and placeholder outputs

This scaffold is ready for a dry-run review once the runner is validated.

## What remains before discovery execution

- implement signal construction and candidate scoring logic inside `pipelines/run_alpha_family_diversification_discovery_v1.py`
- implement redundancy screening logic that compares new candidate panels to existing participation/stress families
- implement summary report generation and result note creation
- implement validation-friendly metric collection and candidate decision support
- enable a safe `--run` path after the above work is complete
