# Project Underdog - Dispersion Path-Dependence Panel Audit v1

## SECTION 1 - Executive Summary

This document is an independent audit of the generated Dispersion Path-Dependence research panels before any IC discovery.

Current input classification:

`PANEL_GENERATION_READY_WITH_SCIENTIFIC_NOTES`

Audit classification:

**PANELS_APPROVED_WITH_NOTES**

The generated panels pass the panel audit checks and may advance to IC discovery after this audit is accepted. The notes are non-blocking:

- The generated artifact contract is four per-candidate long-form panels, matching the panel-generation task and generated manifests. The earlier panel specification also contained wording for a single canonical long-form file; this did not create row/schema drift in the accepted generated artifacts.
- Panel checksums are not stored in the generation manifests. Audit-side SHA256 values were computed and recorded below, but there are no manifest checksum fields to reconcile against.
- Scientific contamination risks for `dpath_03` and `dpath_04` remain audit-facing notes for later IC discovery and research review.

No panel regeneration, IC discovery, validation, refinement, governance mutation, production registration, threshold change, or ML work was performed during this audit.

## SECTION 2 - Materials Reviewed

Reviewed:

- `docs/research_notes/dispersion_path_dependence_panel_generation_v1.md`
- `docs/research_notes/dispersion_path_dependence_panel_specification_v1.md`
- `pipelines/run_dispersion_path_dependence_panel_generation_v1.py`
- `artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

Audited panel files:

- `dpath_01_signal_panel.parquet`
- `dpath_02_signal_panel.parquet`
- `dpath_03_signal_panel.parquet`
- `dpath_04_signal_panel.parquet`

## SECTION 3 - Artifact Inventory Audit

Expected panel artifacts were present:

| artifact | status |
| --- | --- |
| `dpath_01_signal_panel.parquet` | PASS |
| `dpath_02_signal_panel.parquet` | PASS |
| `dpath_03_signal_panel.parquet` | PASS |
| `dpath_04_signal_panel.parquet` | PASS |

Expected manifest/report artifacts were present:

| artifact | status |
| --- | --- |
| `metadata.json` | PASS |
| `panel_manifest.csv` | PASS |
| `panel_generation_summary.csv` | PASS |
| `panel_generation_manifest.json` | PASS |
| `schema_validation_report.csv` | PASS |
| `registry_manifest.csv` | PASS |
| `formula_manifest.csv` | PASS |
| `feature_manifest.csv` | PASS |
| `input_schema_manifest.csv` | PASS |

Blocked artifacts:

| blocked artifact class | status |
| --- | --- |
| Smooth/Burst panel | PASS - absent |
| `dpath_05+` panel | PASS - absent |
| VoV panel | PASS - absent |
| Event Clustering / `ecluster` panel | PASS - absent |
| refinement panel | PASS - absent |
| IC artifact | PASS - absent |
| validation artifact other than `schema_validation_report.csv` | PASS - absent |

The artifact directory contains exactly the expected generated files.

## SECTION 4 - Row Count and Manifest Reconciliation

| candidate_id | panel file | panel rows | manifest rows | duplicate keys |
| --- | --- | ---: | ---: | ---: |
| `dpath_01_relapse_resilience_after_calm` | `dpath_01_signal_panel.parquet` | 1,025,922 | 1,025,922 | 0 |
| `dpath_02_disagreement_vol_stress_divergence` | `dpath_02_signal_panel.parquet` | 1,025,922 | 1,025,922 | 0 |
| `dpath_03_elevated_disagreement_stabilization` | `dpath_03_signal_panel.parquet` | 1,025,922 | 1,025,922 | 0 |
| `dpath_04_consensus_without_crowding` | `dpath_04_signal_panel.parquet` | 1,025,922 | 1,025,922 | 0 |

Total panel rows: 4,103,688.

Reconciliation status:

- Panel files reconcile with `panel_manifest.csv`: PASS.
- `panel_generation_summary.csv` candidate IDs reconcile: PASS.
- `registry_manifest.csv` candidate IDs reconcile: PASS.
- `formula_manifest.csv` candidate IDs reconcile: PASS.
- `schema_validation_report.csv` candidate IDs reconcile: PASS.
- `metadata.json` candidate IDs reconcile: PASS.
- `panel_generation_manifest.json` candidate IDs reconcile: PASS.
- JSON row count reconciles to manifest total: PASS.

## SECTION 5 - Schema Audit

Schema status: PASS.

The panels preserve the frozen long-form columns:

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

Canonical key audit:

- Key: `date`, `ticker`, `candidate_id`.
- Duplicate key count: 0.

Timing policy:

`after_close_t_forward_returns_after_t`

Timing status: PASS.

## SECTION 6 - Scientific Lineage Audit

Scientific lineage status: PASS.

Every panel row preserves:

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
- `formula_text`
- `activation_text`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `research_status`

Candidate ID freeze status:

| candidate_id | status |
| --- | --- |
| `dpath_01_relapse_resilience_after_calm` | PASS |
| `dpath_02_disagreement_vol_stress_divergence` | PASS |
| `dpath_03_elevated_disagreement_stabilization` | PASS |
| `dpath_04_consensus_without_crowding` | PASS |

Formula metadata status:

- `formula_text` matches formula manifest for each candidate: PASS.
- `activation_text` matches formula manifest for each candidate: PASS.
- Candidate primary horizon remains `h10`: PASS.
- Secondary horizons remain `h5|h20`: PASS.
- Expected sign remains `positive`: PASS.

Scientific drift assessment:

No scientific drift was found between formula specification, implementation, and generated panels. The generated panels retain hypothesis traceability, mechanism lineage, contamination metadata, comparator metadata, and formula/activation text.

## SECTION 7 - Activation, Warmup, and Missing-Data Audit

Activation-neutralization status: PASS.

Specification requirement:

`inactive_signal_value_0_5_with_is_active_false`

Observed behavior:

- Mature inactive rows with available `pre_activation_raw_score` have `raw_score = 0.5`.
- Mature inactive rows with available `pre_activation_raw_score` have `signal_value = 0.5`.
- Mature inactive neutralized rows use `missing_reason = inactive_neutralized`.

Warmup status: PASS.

Observed behavior:

- Warmup-incomplete rows retain null `signal_value`.
- Warmup handling is distinct from inactive neutralization.

Missing-data semantics status: PASS.

Observed missing-reason vocabulary:

- `inactive_neutralized`
- `nonfinite_feature`
- `raw_ohlcv_missing`
- `rolling_warmup`

All observed values are within the approved missing-reason vocabulary.

## SECTION 8 - Checksum Audit

Generation manifests do not include checksum fields for panel parquet files. Therefore, checksum reconciliation against manifests is not available.

Audit-side SHA256 values were computed:

| artifact | audit SHA256 |
| --- | --- |
| `dpath_01_signal_panel.parquet` | `273b2f80530b8e0b38fb59b46988162000c2b7cf70ce4e57a6b9bc879310c0ff` |
| `dpath_02_signal_panel.parquet` | `4d98e0b912d49faf0877078eedfb2fee04e8c266b6db9e2b50a987c58bf074da` |
| `dpath_03_signal_panel.parquet` | `09d99dc0fbfbf38f27f478dbd8ac0ccc66c1139515bff6b9171387bf9b41f1c0` |
| `dpath_04_signal_panel.parquet` | `be4be73518f9761cf74bc04f6e81291e6110aeaa8d31583b28981d1eaaecbae8` |

Recommendation for future panel generations:

- Add panel-level SHA256 fields to `panel_manifest.csv` or `panel_generation_manifest.json` so future audits can perform direct checksum reconciliation.

This is documentation debt, not a regeneration requirement for this batch.

## SECTION 9 - Blocked Work Confirmation

This audit confirms no execution of:

- IC discovery
- discovery
- refinement
- validation
- governance mutation
- production registration
- threshold changes
- ML integration

The fail-closed metadata fields in `panel_generation_manifest.json` confirm all blocked execution paths remained false.

## SECTION 10 - Verification

Commands run:

- `python pipelines/run_dispersion_path_dependence_panel_generation_v1.py --validate-only`
- `pytest -q tests/test_dispersion_path_dependence_panel_generation_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_research_module_v1.py`
- `pytest -q tests/test_registry_validation.py`

Results:

- Validate-only mode: PASS.
- Focused panel-generation tests: 7 passed.
- Implementation regression tests: 11 passed.
- Registry/scaffold validation tests: 5 passed.

Runtime warnings:

- PyArrow emitted sandbox-local CPU cache probing warnings. These did not affect validation, schema checks, or manifest reconciliation.

## SECTION 11 - Remaining Notes

Non-blocking notes:

1. The panel specification retained wording for a single canonical long-form panel file, while the accepted panel-generation task and generated artifacts use four per-candidate long-form panels. The generated artifacts are internally consistent and match the current phase request, so no regeneration is recommended.
2. Panel manifests lack checksum fields. Audit-side SHA256 values were computed, but direct manifest checksum reconciliation is unavailable.
3. `dpath_03` and `dpath_04` retain the scientific contamination risks noted in prior phases. IC discovery and research review should test contamination against volatility compression, hostile/stress repair, rank coherence, persistence, and parked non-hostile transition comparators.

## SECTION 12 - Final Recommendation

Classification: **PANELS_APPROVED_WITH_NOTES**

The generated Dispersion Path-Dependence panels are approved to advance to IC discovery. The next lifecycle phase should be **Dispersion Path-Dependence IC Discovery v1**.

IC discovery should use the audited panels as-is and should not regenerate panels, revise formulas, run validation, modify governance, register production candidates, change thresholds, or introduce ML.
