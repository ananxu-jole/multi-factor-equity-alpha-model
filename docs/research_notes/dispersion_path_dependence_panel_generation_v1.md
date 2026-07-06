# Project Underdog - Dispersion Path-Dependence Panel Generation v1

## SECTION 1 - Executive Summary

Dispersion Path-Dependence panel generation v1 completed one lifecycle phase after the approved panel specification. The run generated research-only long-form signal panels for exactly the four approved first-batch candidates under:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

Generated candidates:

- `dpath_01_relapse_resilience_after_calm`
- `dpath_02_disagreement_vol_stress_divergence`
- `dpath_03_elevated_disagreement_stabilization`
- `dpath_04_consensus_without_crowding`

Excluded candidates and families remained blocked:

- Smooth Versus Burst Resolution / `dpath_05+`
- VoV candidates
- event-clustering / `ecluster` candidates
- refinement variants

Classification: **PANEL_GENERATION_READY_WITH_SCIENTIFIC_NOTES**

The scientific notes are inherited from the approved specification and implementation review. They do not block independent panel audit, but they should remain visible during audit because `dpath_03` and `dpath_04` retain higher contamination risk versus volatility compression, stress repair, rank coherence, persistence, and parked non-hostile transition.

## SECTION 2 - Materials Reviewed

- `docs/research_notes/dispersion_path_dependence_panel_specification_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_implementation_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_implementation_v1.md`
- `pipelines/dispersion_path_dependence_research_module_v1.py`
- `pipelines/run_dispersion_path_dependence_panel_generation_v1.py`

## SECTION 3 - Source Data

Source OHLCV file:

`data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet`

Source normalization:

- Existing wide OHLCV parquet was normalized to canonical long-form OHLCV.
- Canonical columns: `date`, `ticker`, `open`, `high`, `low`, `close`, `volume`.
- Source rows after normalization: 1,025,922.
- Ticker count: 489.
- Date range: 2018-01-02 through 2026-05-07.

No external data was accessed.

## SECTION 4 - Generated Artifacts

Generated panel files:

| artifact | candidate_id | rows |
| --- | --- | ---: |
| `dpath_01_signal_panel.parquet` | `dpath_01_relapse_resilience_after_calm` | 1,025,922 |
| `dpath_02_signal_panel.parquet` | `dpath_02_disagreement_vol_stress_divergence` | 1,025,922 |
| `dpath_03_signal_panel.parquet` | `dpath_03_elevated_disagreement_stabilization` | 1,025,922 |
| `dpath_04_signal_panel.parquet` | `dpath_04_consensus_without_crowding` | 1,025,922 |

Generated manifest and report files:

- `metadata.json`
- `panel_manifest.csv`
- `panel_generation_summary.csv`
- `panel_generation_manifest.json`
- `schema_validation_report.csv`
- `registry_manifest.csv`
- `formula_manifest.csv`
- `feature_manifest.csv`
- `input_schema_manifest.csv`

Total generated panel rows: 4,103,688.

No additional panel parquet files were generated.

## SECTION 5 - Panel Contract Confirmation

The generated panels preserve the frozen long-form schema from the panel specification and implementation:

- `date`
- `ticker`
- `candidate_id`
- `candidate_name`
- `module_id`
- `spec_id`
- `mechanism_family`
- `research_status`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `signal_value`
- `raw_score`
- `pre_activation_raw_score`
- `is_active`
- `feature_warmup_complete`
- `finite_cross_section_count`
- `rank_min_count`
- `missing_reason`
- `timing_policy`
- `formula_text`
- `activation_text`
- `anchor_comparators`
- `contamination_controls`
- `hypothesis`
- `scientific_question`
- `expected_evidence`
- `primary_falsification_criterion`
- `observable_implication`
- `expected_orthogonality`
- `created_by_spec`

Timing policy:

`after_close_t_forward_returns_after_t`

Activation-neutralization policy:

`inactive_signal_value_0_5_with_is_active_false`

Warmup policy:

- Warmup-incomplete rows retain null `signal_value`.
- Mature inactive rows with available pre-activation scores are neutralized to `raw_score = 0.5` and `signal_value = 0.5`.
- Missing reasons are restricted to the approved vocabulary.

Duplicate prevention:

- Canonical key: `date`, `ticker`, `candidate_id`.
- Duplicate key count: 0.

## SECTION 6 - Manifest Reconciliation

| check | result |
| --- | --- |
| Approved candidate count | 4 |
| Generated panel count | 4 |
| Smooth/Burst excluded | PASS |
| `dpath_05+` excluded | PASS |
| VoV excluded | PASS |
| `ecluster` excluded | PASS |
| Refinement variants excluded | PASS |
| Schema validation | PASS |
| Duplicate key count | 0 |
| Blocked candidate count | 0 |
| Manifest row count total | 4,103,688 |
| JSON manifest row count | 4,103,688 |
| Panel files reconcile to manifest | PASS |
| Registry manifest reconciles | PASS |
| Formula manifest reconciles | PASS |
| Schema validation report reconciles | PASS |

## SECTION 7 - Guardrail Confirmation

The generation run was panel-only.

Confirmed not executed:

- IC scoring
- discovery
- redundancy screening
- refinement
- validation
- governance mutation
- production registration
- threshold changes
- ML integration

No production registry or governance files were modified.

## SECTION 8 - Verification

Commands run:

- `python -m py_compile pipelines/run_dispersion_path_dependence_panel_generation_v1.py pipelines/dispersion_path_dependence_research_module_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_panel_generation_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_research_module_v1.py`
- `pytest -q tests/test_registry_validation.py`
- `python pipelines/run_dispersion_path_dependence_panel_generation_v1.py`
- `python pipelines/run_dispersion_path_dependence_panel_generation_v1.py --validate-only`

Verification results:

- Py compile: PASS.
- Focused panel-generation tests: 7 passed.
- Implementation regression tests: 11 passed.
- Registry validation tests: 5 passed.
- Panel generation: PASS.
- Validate-only mode: PASS.

Runtime warnings:

- PyArrow emitted sandbox-local CPU cache probing warnings.
- Pandas emitted a future warning for the current `stack(dropna=False)` behavior used in wide-to-long OHLCV normalization.

These warnings did not affect generated artifact reconciliation or schema validation.

## SECTION 9 - Remaining Work Before Independent Panel Audit

The next lifecycle phase should be **Dispersion Path-Dependence Independent Panel Audit v1**.

Audit should independently review:

- exact artifact set;
- schema completeness;
- duplicate-key prevention;
- candidate lineage preservation;
- activation-neutralization semantics;
- warmup and missing-data behavior;
- manifest reconciliation;
- blocked-candidate exclusion;
- absence of IC, validation, governance, production, threshold, and ML artifacts.

Panel audit should not compute IC, run validation, revise formulas, modify governance, register production candidates, change thresholds, or introduce ML.

## SECTION 10 - Final Classification

Classification: **PANEL_GENERATION_READY_WITH_SCIENTIFIC_NOTES**

Panel generation is ready for independent panel audit. The scientific notes are not generation defects; they are audit-facing risk context inherited from Platform v2 mechanism review, formula specification, and implementation review.
