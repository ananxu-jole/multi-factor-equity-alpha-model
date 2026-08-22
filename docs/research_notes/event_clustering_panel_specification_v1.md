# Project Underdog - Event Clustering Panel Specification v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 5 - Panel Specification

Classification: `PANEL_SPEC_READY_WITH_NOTES`

Recommendation: `ADVANCE_TO_PANEL_GENERATION`

Scope: specification-only freeze of the Event Clustering research panel contract before any panel generation.

This note does not implement code, generate panels, compute IC, run validation, modify governance, change production files, change thresholds, introduce ML, or create artifacts.

## SECTION 1 - Inputs And Lifecycle Boundary

Inputs reviewed:

- `docs/research_notes/event_clustering_formula_implementation_review_v1.md`
- `docs/research_notes/event_clustering_formula_implementation_v1.md`
- `docs/research_notes/event_clustering_formula_and_panel_specification_v1.md`

Current lifecycle status:

- Formula Implementation Review classification: `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`
- Approved next phase: Event Clustering Panel Specification v1

This document advances exactly one lifecycle phase, from implementation review to panel specification. It does not advance to panel generation, panel audit, IC discovery, validation, governance, production, threshold changes, or ML.

## SECTION 2 - Panel Scope

The future panel generation phase is authorized to specify panels only for the five reviewed Event Clustering candidates:

| candidate_id | candidate_name | mechanism | primary horizon | expected sign |
| --- | --- | --- | --- | --- |
| `ecluster_01_concentrated_absorption` | Concentrated Event Absorption | Event Concentration | h10 | positive |
| `ecluster_02_aligned_pressure_resolution` | Aligned Event Pressure Resolution | Event Alignment And Fragmentation | h10 | positive |
| `ecluster_03_fragmented_event_absorption` | Fragmented Event Absorption | Event Alignment And Fragmentation | h5 | positive |
| `ecluster_04_deteriorating_cluster_avoidance` | Deteriorating Cluster Avoidance | Cluster Absorption Versus Deterioration | h5 | positive |
| `ecluster_05_aging_cluster_memory` | Aging Cluster Memory | Cluster Aging And Market Memory | h10 | positive |

No additional Event Clustering candidates are authorized. No VoV, DPath, refinement, validation, production, or ML candidates are authorized.

## SECTION 3 - Canonical Long-Form Schema

The future panel must be canonical long-form with one row per:

`(date, ticker, candidate_id)`

Primary key:

- `date`
- `ticker`
- `candidate_id`

Required fields:

| field | required content |
| --- | --- |
| `date` | After-close signal date. |
| `ticker` | Security identifier. |
| `candidate_id` | One of the five approved Event Clustering candidate IDs. |
| `signal_value` | Candidate signal value; active ranked value, inactive neutral value, or null for missing/unavailable rows. |
| `activation_state` | Candidate activation state; must distinguish active, inactive neutralized, warmup, missing, and insufficient cross-section states. |
| `warmup_state` | Feature maturity status and warmup reason where applicable. |
| `missing_data_state` | Controlled missing-data state; must distinguish raw OHLCV missing, nonfinite feature, insufficient cross-section, and inactive neutralization. |
| `scientific_lineage` | Source lineage linking review, implementation, implementation review, and this panel specification. |
| `mechanism` | Approved mechanism label for the candidate. |
| `contamination_metadata` | Required contamination-reference metadata. |
| `isolated_event_anchor` | Isolated-event anchor field or anchor metadata required for candidate comparison. |
| `timing_metadata` | Timing lineage and signal-date policy metadata. |
| `after_close_policy` | `after_close_t_forward_returns_after_t`. |
| `source_spec_id` | `event_clustering_panel_specification_v1` plus formula specification linkage. |
| `module_id` | `event_clustering_research_module_v1`. |
| `candidate_version` | `v1`. |

Required implementation-compatible fields:

- `candidate_name`
- `platform_version`
- `research_status`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `raw_score`
- `pre_activation_raw_score`
- `is_active`
- `feature_warmup_complete`
- `finite_cross_section_count`
- `rank_min_count`
- `missing_reason`
- `formula_version`
- `formula_text`
- `activation_text`
- `source_specification`
- `source_review`
- `source_design`
- `anchor_comparators`
- `contamination_reference_set`
- `scientific_question`
- `expected_evidence`
- `stop_conditions`
- `created_by_spec`

Required Event Clustering feature and anchor fields:

- `cluster_count_5`
- `cluster_count_10`
- `event_type_count_5`
- `alignment_score_5`
- `fragmentation_score_5`
- `absorption_5`
- `deterioration_5`
- `cluster_age_state`
- `fresh_cluster_5`
- `persistent_cluster_10`
- `decaying_cluster_10`
- `static_event_anchor_20`
- `isolated_event_anchor_20`
- `price_event`
- `gap_event`
- `range_event`
- `volume_event`
- `vol_event`
- `event_any`
- `volume_intensity_5`
- `range_intensity_5`
- `price_intensity_5`
- `gap_intensity_5`
- `vol_intensity_5`

Required contamination diagnostic fields:

- `low_extension_20`
- `low_churn_5`
- `liquidity_rank_20`
- `stress_proxy_20`
- `security_vov_20`
- `vol_compression_20`
- `rank_coherence_proxy_20`
- `persistence_proxy_20`
- `static_dispersion_20`
- `dispersion_path_proxy_10`
- `non_hostile_transition_proxy_20`

## SECTION 4 - Field Semantics

Signal value semantics:

- Active rows with finite raw scores must contain ranked `signal_value`.
- Inactive but otherwise mature rows must use neutral `signal_value = 0.5`.
- Warmup, raw missing, nonfinite feature, or insufficient cross-section rows must use null `signal_value`.

Activation state semantics:

- `active`: candidate activation condition is true and all required features are available.
- `inactive_neutralized`: candidate activation condition is false after warmup and required features are available.
- `rolling_warmup`: required rolling features are immature.
- `raw_ohlcv_missing`: required OHLCV input is missing, invalid, or nonpositive where positive price is required.
- `nonfinite_feature`: raw OHLCV exists but a required derived feature is nonfinite.
- `insufficient_cross_section`: active raw score exists but same-date finite active cross-section is insufficient for ranking.

Warmup state semantics:

- Must report whether the row is mature under the implemented warmup rules.
- Must not backfill from future observations.
- Must not use same-date forward returns.

Timing semantics:

- All signals are after-close signals.
- Signal date `t` may use OHLCV data only through close `t`.
- Forward returns, IC, and validation are outside this phase.

## SECTION 5 - Scientific Lineage Contract

Every future panel row must carry enough lineage to reconstruct the approved lifecycle:

| lineage item | required value |
| --- | --- |
| `module_id` | `event_clustering_research_module_v1` |
| `source_spec_id` | `event_clustering_panel_specification_v1` |
| `formula_spec_id` | `event_clustering_formula_and_panel_specification_v1` |
| `implementation_note` | `docs/research_notes/event_clustering_formula_implementation_v1.md` |
| `implementation_review` | `docs/research_notes/event_clustering_formula_implementation_review_v1.md` |
| `candidate_version` | `v1` |
| `research_status` | `RESEARCH_ONLY` |
| `after_close_policy` | `after_close_t_forward_returns_after_t` |

Scientific lineage must include candidate name, mechanism, scientific question, expected evidence, expected sign, primary horizon, secondary horizons, formula text, activation text, anchor comparators, contamination controls, and stop conditions.

## SECTION 6 - Contamination Metadata Contract

Every candidate row must include contamination metadata sufficient for later panel audit and IC discovery setup.

Required contamination references:

- VoV.
- Volatility compression.
- Hostile/stress repair.
- Volume shock reversal.
- Rank coherence.
- Persistence.
- Dispersion path-dependence.
- Non-hostile transition.
- Static dispersion.
- Isolated-event anchors.

Required candidate-specific anchor metadata:

| candidate_id | required anchor metadata |
| --- | --- |
| `ecluster_01_concentrated_absorption` | `static_event_anchor_20`, `isolated_event_anchor_20`, isolated absorption anchor metadata. |
| `ecluster_02_aligned_pressure_resolution` | same-event-type mix without clustering, `static_event_anchor_20`, isolated aligned one-day event anchor metadata. |
| `ecluster_03_fragmented_event_absorption` | isolated fragmented one-day event anchor, static high event-count anchor metadata. |
| `ecluster_04_deteriorating_cluster_avoidance` | isolated deterioration anchor, static stress anchor, static event-count anchor metadata. |
| `ecluster_05_aging_cluster_memory` | fresh-only cluster anchor, static event-count anchor, isolated-event anchor, volatility-compression anchor metadata. |

## SECTION 7 - Artifact Contract

Future panel generation must use the frozen artifact root:

`artifacts/research/event_clustering_research_module_v1/panel_v1/`

This specification does not create the artifact root.

Required future artifacts:

| artifact | purpose |
| --- | --- |
| `metadata.json` | Module-level and candidate-level metadata, lineage, timing, and guardrails. |
| `panel_manifest.csv` | Panel file inventory, candidate IDs, row counts, date ranges, ticker counts, schema version, and checksums. |
| `panel_generation_summary.csv` | Summary of generated rows, activation counts, missing-data states, warmup states, and neutralization counts by candidate. |
| `panel_generation_manifest.json` | Audit manifest reconciling inputs, outputs, schemas, checksums, code entry point, source notes, and generation timestamp. |
| `schema_validation_report.csv` | Schema, primary-key, required-field, type, nullability, and controlled-state validation report. |
| `registry_manifest.csv` | Frozen candidate registry as used for generation. |
| `formula_manifest.csv` | Frozen formula and activation text by candidate. |
| `feature_manifest.csv` | Feature definitions, dependencies, rolling windows, and timing policies. |
| `input_schema_manifest.csv` | Input OHLCV schema, date range, row count, identifier policy, and point-in-time assumptions. |

Future panel parquet files may be emitted only in the panel generation phase. Their exact file names must be recorded in `panel_manifest.csv` and `panel_generation_manifest.json`.

## SECTION 8 - Metadata JSON Schema

`metadata.json` must include:

- `module_id`
- `panel_version`
- `platform_version`
- `source_spec_id`
- `formula_spec_id`
- `implementation_review_classification`
- `artifact_root`
- `candidate_ids`
- `candidate_count`
- `candidate_version`
- `after_close_policy`
- `research_status`
- `guardrails`
- `source_documents`
- `contamination_controls`
- `checksum_policy`

Each candidate object must include:

- `candidate_id`
- `candidate_name`
- `mechanism`
- `scientific_question`
- `expected_evidence`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `formula_text`
- `activation_text`
- `required_fields`
- `anchor_metadata`
- `contamination_metadata`
- `stop_conditions`

## SECTION 9 - Manifest Schemas

### 9.1 `panel_manifest.csv`

Required columns:

- `panel_file`
- `panel_file_type`
- `module_id`
- `panel_version`
- `candidate_count`
- `candidate_ids`
- `row_count`
- `date_min`
- `date_max`
- `ticker_count`
- `duplicate_key_count`
- `schema_version`
- `schema_validation_status`
- `lineage_validation_status`
- `registry_validation_status`
- `checksum_sha256`
- `created_at_utc`
- `source_spec_id`

### 9.2 `panel_generation_summary.csv`

Required columns:

- `candidate_id`
- `candidate_name`
- `mechanism`
- `row_count`
- `active_row_count`
- `inactive_neutralized_row_count`
- `warmup_row_count`
- `missing_row_count`
- `insufficient_cross_section_row_count`
- `date_min`
- `date_max`
- `ticker_count`
- `primary_horizon`
- `secondary_horizons`

### 9.3 `panel_generation_manifest.json`

Required keys:

- `module_id`
- `panel_version`
- `artifact_root`
- `generation_phase`
- `source_spec_id`
- `formula_spec_id`
- `implementation_review`
- `candidate_ids`
- `candidate_count`
- `input_schema_manifest`
- `registry_manifest`
- `formula_manifest`
- `feature_manifest`
- `panel_manifest`
- `metadata_json`
- `schema_validation_report`
- `checksums`
- `validation_results`
- `guardrail_results`
- `created_at_utc`

### 9.4 `schema_validation_report.csv`

Required columns:

- `check_name`
- `check_scope`
- `status`
- `observed_value`
- `expected_value`
- `failure_count`
- `notes`

### 9.5 `registry_manifest.csv`

Required columns:

- `candidate_id`
- `candidate_name`
- `module_id`
- `candidate_version`
- `mechanism`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `research_status`
- `formula_version`
- `source_spec_id`

### 9.6 `formula_manifest.csv`

Required columns:

- `candidate_id`
- `candidate_name`
- `formula_version`
- `formula_text`
- `activation_text`
- `after_close_policy`
- `source_spec_id`
- `implementation_review`

### 9.7 `feature_manifest.csv`

Required columns:

- `feature_name`
- `feature_type`
- `definition_text`
- `raw_input_dependencies`
- `rolling_window`
- `cross_sectional_dependency`
- `warmup_requirement`
- `missing_data_policy`
- `used_by_candidate_ids`
- `timing_policy`

### 9.8 `input_schema_manifest.csv`

Required columns:

- `input_field`
- `required`
- `type`
- `point_in_time_policy`
- `missing_data_policy`
- `raw_source`
- `notes`

## SECTION 10 - Future Panel-Generation Validation Rules

The future panel generation phase must run and record these checks:

1. Duplicate keys must equal zero for `(date, ticker, candidate_id)`.
2. Schema validation is required against the canonical long-form schema.
3. Scientific lineage validation is required.
4. Registry validation is required and must confirm exactly five approved candidates.
5. Contamination metadata is required for every candidate row.
6. Activation neutrality is required: inactive mature rows must have neutral `signal_value = 0.5`.
7. Warmup rows must be distinguishable from missing-data and inactive-neutralized rows.
8. Missing-data states must use controlled labels.
9. Manifest reconciliation is required across metadata, panel manifest, registry manifest, formula manifest, feature manifest, and input schema manifest.
10. Artifact checksum reconciliation is required under the checksum policy in Section 11.

Failure of any required validation check must block advancement to panel audit until corrected or explicitly reviewed in a panel-generation exception note.

## SECTION 11 - Checksum Requirement

Platform v2 checksum enhancement:

Future panel generation SHALL emit SHA-256 checksums for:

- every parquet panel;
- `metadata.json`;
- `panel_manifest.csv`.

Those checksums SHALL be included in `panel_generation_manifest.json` for future audit reconciliation.

Required checksum manifest structure:

- `artifact_path`
- `artifact_type`
- `checksum_algorithm`
- `checksum_sha256`
- `byte_size`
- `created_at_utc`
- `source_phase`

This is a specification requirement only. No checksums are generated by this note.

## SECTION 12 - Guardrails

This panel specification does not authorize:

- implementation changes;
- panel generation;
- parquet creation;
- manifest creation;
- checksum generation;
- IC discovery;
- validation;
- governance mutation;
- production changes;
- threshold changes;
- ML;
- additional candidates;
- additional mechanisms.

## SECTION 13 - Verification

Confirmed:

- Exactly five candidates specified.
- No additional candidates specified.
- Artifact root specified but not created.
- Required artifact names specified but not generated.
- Checksum requirement frozen.
- No implementation changes made.
- No panel artifacts created.
- No IC artifacts created.
- No validation files created.
- No governance files changed.
- No production files changed.
- No threshold files changed.
- No ML files changed.

## SECTION 14 - Classification

Classification: `PANEL_SPEC_READY_WITH_NOTES`

Rationale:

- Implementation Review approved the reviewed Event Clustering implementation for panel specification.
- The panel scope is restricted to exactly the five approved candidates.
- The canonical long-form schema, required fields, lineage contract, contamination metadata, anchor requirements, artifact contract, validation rules, and checksum requirements are frozen.
- Notes remain because no panel has been generated or audited, and empirical activation/contamination properties remain unknown until later phases.

## SECTION 15 - Final Recommendation

Recommended next lifecycle phase:

- Event Clustering Panel Generation v1.

Event Clustering may advance exactly one lifecycle phase to panel generation. It may not advance directly to IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
