# Alpha Family Diversification Candidate Panel Generation v1

Date: 2026-06-17

Run id: `alpha_family_diversification_discovery_v1`

## Purpose

This note documents the research-only candidate panel generation stage for the alpha-family diversification discovery framework.

The stage generates candidate signal panels so the statistical redundancy diagnostics can operate on actual candidate outputs instead of reporting missing panel files.

## Method

The runner implements `--run` as candidate panel generation only.

Inputs:
- approved candidate registry embedded in `pipelines/run_alpha_family_diversification_discovery_v1.py`
- existing cached source signal panels under `artifacts/panels/signals/`
- registry schema validation from `pipelines/utils/registry_validation.py`
- metadata and statistical redundancy screening utilities from `pipelines/utils/redundancy_screening.py`

Generation approach:
- Load a fixed, auditable set of existing cached source panels.
- Restrict candidate generation to the latest 504 shared source-panel rows for a lightweight research panel pass.
- Build deterministic cross-sectional transformations aligned to the specification families:
  - dispersion expansion, compression, and anomaly candidates use relative return rank/z-score, residual return, volatility surprise, volatility compression, range compression, and trend consistency source panels.
  - persistence and rank coherence candidates use rank stability, downtrend rank stability, trend persistence, failed-breakout, and range-failure source panels.
- Write one long-form panel per candidate.
- Re-run metadata redundancy screening.
- Re-run statistical value/rank correlation screening against the generated candidate panels.

No alpha validation, target-return scoring, portfolio routing, ML, or candidate decision logic is executed.

## Artifact Outputs

Candidate panels:
- `artifacts/research/alpha_family_diversification_discovery_v1/candidate_panels/{signal_name}.parquet`
- `artifacts/research/alpha_family_diversification_discovery_v1/candidate_panels/{signal_name}.metadata.json`

Each panel contains:
- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `family`
- `theme`
- `horizon`

Discovery summary:
- `artifacts/research/alpha_family_diversification_discovery_v1/discovery_summary/panel_manifest.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/discovery_summary/candidate_panel_generation_summary.csv`

Diagnostics:
- `artifacts/research/alpha_family_diversification_discovery_v1/diagnostics/candidate_panel_source_inputs.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/redundancy_screening/redundancy_screening.csv`
- `artifacts/research/alpha_family_diversification_discovery_v1/redundancy_screening/statistical_redundancy_screening.csv`

## Guardrails

This implementation remains research-only.

It does not:
- run validation
- modify governance
- modify thresholds
- promote or demote candidates
- register candidates to production
- write candidate artifacts outside the research artifact directory
- implement ML
- route panels to portfolio, survivor, watchlist, or production alpha workflows

The generated manifest explicitly records:
- `research_only: true`
- `validation_executed: false`
- `production_registration: false`
- `governance_modified: false`
- `candidate_promotion_or_demotion: false`
- `ml_integration: false`

## Limitations

- Candidate panels are first-pass research transformations from existing cached signal panels, not validated alpha candidates.
- The 504-row source lookback is intentionally lightweight and should be treated as a diagnostic panel-generation pass.
- Statistical redundancy screening now computes candidate-to-candidate value and rank correlations, but it still does not make advancement decisions.
- The generated signal values support redundancy diagnostics only; they are not IC scores, validation outputs, or production signals.
- The implementation does not evaluate forward returns, regime performance, co-activation with production candidates, or portfolio impact.

## Next Step

The next step is a diagnostic review of the generated panels and statistical redundancy output to identify formula bugs, overly duplicated candidates, and missing family coverage. Any validation, thresholding, governance action, or candidate advancement must remain a separate explicitly approved task.
