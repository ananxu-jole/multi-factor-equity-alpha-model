# Project Underdog - Dispersion Path-Dependence Formula Implementation v1

## SECTION 1 - Executive Summary

Classification: `IMPLEMENTATION_READY_WITH_SCIENTIFIC_NOTES`

This note documents the implementation of exactly the four approved Dispersion Path-Dependence candidates from `dispersion_path_dependence_formula_and_panel_specification_v1.md`.

Implemented files:

- `pipelines/dispersion_path_dependence_research_module_v1.py`
- `tests/test_dispersion_path_dependence_research_module_v1.py`

Implemented candidates:

| candidate_id | candidate_name | mechanism family | primary horizon | expected sign |
| --- | --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Relapse Resilience After Temporary Calm | Disagreement Relapse Resilience | h10 | positive |
| `dpath_02_disagreement_vol_stress_divergence` | Disagreement Path Divergence From Volatility/Stress | Disagreement Path Divergence | h10 | positive |
| `dpath_03_elevated_disagreement_stabilization` | Elevated Disagreement Stabilization | Elevated Disagreement Stabilization | h10 | positive |
| `dpath_04_consensus_without_crowding` | Consensus Formation Without Crowding | Consensus Formation Without Crowding | h10 | positive |

Explicitly not implemented:

- Smooth Versus Burst Resolution.
- Any `dpath_05` or higher candidate.
- VoV candidates.
- Event-clustering candidates.
- Refinement variants.
- Validation, IC scoring, governance changes, production registration, threshold changes, or ML.

## SECTION 2 - Materials Reviewed

Reviewed:

- `docs/research_notes/dispersion_path_dependence_formula_and_panel_specification_v1.md`
- `docs/research_notes/dispersion_path_dependence_candidate_allocation_and_formula_planning_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_mechanism_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_research_module_design_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`

## SECTION 3 - Implementation Summary

The implementation adds a research-only module at `pipelines/dispersion_path_dependence_research_module_v1.py`.

Implemented public functions:

- `candidate_registry()`
- `validate_dpath_registry()`
- `prepare_ohlcv_frame()`
- `compute_dpath_features()`
- `build_dpath_candidate_panel()`
- `expected_panel_columns()`
- `implemented_candidate_ids()`
- `blocked_candidate_ids()`
- `module_guardrail_manifest()`

The implementation produces an in-memory canonical long-form panel compatible with the specification. It does not write panel files or create artifacts.

Canonical grain:

- one row per `date` x `ticker` x `candidate_id`;
- exactly four candidate IDs;
- after-close timing metadata preserved;
- research-only status preserved.

## SECTION 4 - Scientific Lineage Preservation

Each candidate registry row and panel row preserves:

- `candidate_id`
- `candidate_name`
- `mechanism_family`
- `hypothesis`
- `scientific_question`
- `expected_evidence`
- `primary_falsification_criterion`
- `observable_implication`
- `expected_orthogonality`
- `contamination_controls`
- `anchor_comparators`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `formula_text`
- `activation_text`
- `timing_policy`
- `created_by_spec`

Each candidate maps to exactly one approved scientific mechanism.

## SECTION 5 - Implemented Feature Coverage

Implemented OHLCV-derived rolling features:

- `ret_1`, `ret_5`, `ret_10`, `ret_20`, `ret_60`
- `range_1`, `range_20`
- `vol_5`, `vol_20`
- `vov_5_20`
- `drawdown_20`
- `dollar_volume_20`

Implemented cross-sectional and path features:

- `disp_1`
- `disp_5`, `disp_10`, `disp_20`
- `disp_z_20`
- `disp_slope_5`, `disp_slope_10`
- `disp_accel_5_10`
- `mkt_vol_20`, `mkt_vol_slope_10`
- `mkt_stress_20`, `mkt_stress_slope_10`
- `vov_path_10`
- `divergence_intensity`
- `rank_ret_5`
- `low_extension_20`
- `rank_churn_5`
- `low_churn_5`
- `liquidity_rank_20`
- `leadership_crowding_60`
- `emerging_improvement_5_20`

Warmup handling:

- security-level warmup requires at least 60 observations;
- date-level state warmup requires 252 observations;
- warmup-incomplete rows retain null signals and `missing_reason = rolling_warmup`.

Inactive handling:

- inactive but feature-valid rows receive neutral `signal_value = 0.5`;
- inactive rows carry `is_active = false`;
- inactive rows carry `missing_reason = inactive_neutralized`.

Missing-data handling:

- raw OHLCV gaps are not imputed;
- nonfinite formulas are not converted to zero;
- insufficient cross-section is tracked through controlled reason codes.

## SECTION 6 - Registry and Guardrail Checks

Registry consistency checks enforce:

- exactly four implemented candidate IDs;
- no Smooth Versus Burst candidate;
- no `dpath_05` or higher candidate;
- no `vov_` candidate;
- no `ecluster_` candidate;
- h10 as primary horizon for all candidates;
- `RESEARCH_ONLY` status for all candidates;
- one approved mechanism per candidate.

The module guardrail manifest reports:

- `smooth_burst_implemented = false`
- `extra_dpath_candidates_implemented = false`
- `vov_candidates_implemented = false`
- `event_clustering_implemented = false`
- `panel_generation_executed = false`
- `ic_scoring_executed = false`
- `validation_executed = false`
- `governance_modified = false`
- `production_registration = false`
- `thresholds_modified = false`
- `ml_integration = false`

## SECTION 7 - Tests Added

Added focused tests in `tests/test_dispersion_path_dependence_research_module_v1.py`.

Test coverage:

- registry contains exactly the four approved candidates;
- registry rejects deferred or extra candidates;
- long-form panel schema is compatible with the specification;
- no VoV, event-clustering, or Smooth/Burst candidate appears;
- warmup, missing-data, and inactive-neutralization states remain distinct;
- `dpath_04_consensus_without_crowding` formula recomputes exactly on an active date;
- guardrail manifest confirms no execution pathways;
- required OHLCV input schema is enforced.

Relevant existing registry tests were also run.

## SECTION 8 - Verification

Commands run:

```bash
python -m py_compile pipelines/dispersion_path_dependence_research_module_v1.py
pytest -q tests/test_dispersion_path_dependence_research_module_v1.py tests/test_registry_validation.py
```

Results:

- Python compile: passed.
- Focused implementation and registry tests: 12 passed.

Confirmed:

- Exactly four dpath candidates implemented.
- No deferred Smooth/Burst candidate implemented.
- No extra dpath candidates implemented.
- No panels generated.
- No IC work performed.
- No validation performed.
- No governance decision modified.
- No production registry modified.
- No thresholds changed.
- No ML introduced.

## SECTION 9 - Remaining Notes Before Implementation Review

The implementation is ready for implementation review with scientific notes.

Review should verify:

- formula text in code matches the specification;
- activation conditions match the specification;
- long-form panel schema matches the specification;
- warmup and inactive handling are acceptable for later panel audit;
- lineage fields are complete enough for downstream artifact manifests;
- contamination controls remain metadata and are not weakened before IC discovery.

No panel generation or IC discovery should begin until implementation review is complete.

## SECTION 10 - Final Classification

Final classification:

- `IMPLEMENTATION_READY_WITH_SCIENTIFIC_NOTES`

The implementation is ready for review. It remains research-only and does not authorize panel generation, IC discovery, validation, governance changes, production registration, threshold changes, or ML.
