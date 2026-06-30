# Rank-Coherence Candidate Panel Generation v1

Date: 2026-06-18

Project: Project Underdog

Run id: `rank_coherence_family_discovery_v1`

Scope: research-only candidate panel generation. No IC scoring, refinement, validation, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## Panel Generation Method

The reserved `--run` mode in `pipelines/run_rank_coherence_family_discovery_v1.py` was implemented as panel generation only.

The runner:
- loads the approved 10-candidate rank-coherence registry;
- validates registry schema, family labels, theme labels, and hard max candidate count of 12;
- loads existing source panels from `artifacts/panels/signals/`;
- aligns source panels on common dates and tickers;
- builds deterministic rank-coherence signal panels;
- writes one long-form parquet panel per candidate;
- writes one metadata JSON per candidate;
- refreshes metadata redundancy screening;
- refreshes statistical redundancy screening from generated candidate panels.

Source panels used:
- `relative_return_rank_20`
- `relative_return_zscore_60`
- `percentile_rank_stability_20`
- `trend_consistency_20_60`
- `trend_consistency_20_60_persistent`
- `smooth_trend_persistence_60`
- `residual_return_vs_universe_20`
- `expanded_reversal_5d`
- `close_position_reversal_5`

The generated panels are long-form and include:
- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `family`
- `theme`
- `horizon`

## Artifact Outputs

Artifact root:

`artifacts/research/rank_coherence_family_discovery_v1/`

Generated panel outputs:
- 10 parquet candidate panels under `candidate_panels/`
- 10 candidate metadata JSON files under `candidate_panels/`

Discovery summary outputs:
- `discovery_summary/panel_manifest.csv`
- `discovery_summary/candidate_panel_generation_summary.csv`
- `discovery_summary/source_input_diagnostics.csv`
- `discovery_summary/family_theme_summary.csv`

Diagnostics and redundancy outputs:
- `diagnostics/source_input_diagnostics.csv`
- `diagnostics/source_panel_inputs.csv`
- `diagnostics/guardrail_checklist.csv`
- `redundancy_screening/metadata_redundancy_screening.csv`
- `redundancy_screening/redundancy_screening.csv`
- `redundancy_screening/statistical_redundancy_screening.csv`

Manifest:
- `manifest.json`

Panel generation summary:
- Candidate count: 10.
- Panel generation status: generated for all 10 candidates.
- Date range: 2024-05-03 to 2026-05-07.
- Ticker count range: 462 to 478, depending on formula availability.

## Guardrails

The manifest records:
- `panel_generation_executed: true`
- `discovery_executed: false`
- `ic_scoring_executed: false`
- `refinement_executed: false`
- `validation_executed: false`
- `production_registration: false`
- `governance_modified: false`
- `thresholds_modified: false`
- `ml_integration: false`
- `candidate_promotion_or_demotion: false`

All writes were confined to:

`artifacts/research/rank_coherence_family_discovery_v1/`

The run did not modify production paths, governance standards, validation thresholds, survivor/watchlist state, portfolio outputs, or ML workflows.

## Tests

Verification commands:

```bash
python -m py_compile pipelines/run_rank_coherence_family_discovery_v1.py tests/test_rank_coherence_discovery_scaffold.py tests/test_rank_coherence_candidate_panel_generation.py
pytest tests/test_rank_coherence_discovery_scaffold.py tests/test_rank_coherence_candidate_panel_generation.py -q
```

Focused test result:

`8 passed`

The tests verify:
- `--list-candidates` works.
- `--dry-run` still does not generate or rewrite panels.
- `--run` creates exactly 10 candidate panel files.
- generated panels have required long-form columns.
- candidate cap remains enforced.
- statistical redundancy screening uses generated panels and no longer reports all candidate panels missing.
- guardrail manifest flags remain false for discovery, IC scoring, refinement, validation, governance mutation, threshold mutation, production registration, ML, and promotion/demotion.

## Limitations

This task generated candidate panels only. It does not evaluate alpha quality.

Limitations:
- No IC scoring was performed.
- No approved scoring subset was selected.
- No refinement eligibility classification was made.
- No validation readiness was assessed.
- Redundancy diagnostics are descriptive and diagnostic-only.
- Some rank-coherence candidates are intentionally related by theme, so redundancy review is required before IC scoring.

## Next Step

The next Codex task should be `Rank-Coherence Panel and Redundancy Review v1`.

That task should review:
- panel completeness;
- source-input diagnostics;
- metadata redundancy screening;
- statistical redundancy screening;
- high-redundancy clusters;
- candidate subset eligibility for later IC scoring.

It should not run IC scoring, refinement, validation, governance mutation, threshold changes, production registration, ML, or candidate promotion/demotion.

## Research Caveat

This was a research-only panel generation task. The generated panels are not validation evidence, not production artifacts, not governance decisions, and not candidate promotions or demotions.
