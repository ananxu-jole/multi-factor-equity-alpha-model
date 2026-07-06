# Project Underdog - Dispersion Path-Dependence Panel Specification v1

## SECTION 1 - Executive Summary

Classification: `PANEL_SPEC_READY_WITH_SCIENTIFIC_NOTES`

This note freezes the panel-generation contract for the Dispersion Path-Dependence research module before any panel writing.

Current lifecycle status:

- Formula implementation review classification: `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`
- Current phase: Panel Specification
- Next eligible phase: Panel Generation, after this specification is accepted

This is a specification-only document. It does not implement panel writing, generate panels, compute IC, run validation, modify formulas, modify governance, modify the production registry, change thresholds, or introduce ML.

Panel contract scope:

| candidate_id | candidate_name | mechanism family | primary horizon |
| --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Relapse Resilience After Temporary Calm | Disagreement Relapse Resilience | h10 |
| `dpath_02_disagreement_vol_stress_divergence` | Disagreement Path Divergence From Volatility/Stress | Disagreement Path Divergence | h10 |
| `dpath_03_elevated_disagreement_stabilization` | Elevated Disagreement Stabilization | Elevated Disagreement Stabilization | h10 |
| `dpath_04_consensus_without_crowding` | Consensus Formation Without Crowding | Consensus Formation Without Crowding | h10 |

Explicit exclusions:

- Smooth Versus Burst Resolution remains excluded.
- No `dpath_05` or higher candidate is allowed.
- No VoV candidate is allowed.
- No event-clustering candidate is allowed.
- No refinement variant is allowed.

Artifact root:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

This note does not create that directory.

## SECTION 2 - Materials Reviewed

Reviewed:

- `docs/research_notes/dispersion_path_dependence_formula_implementation_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_implementation_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_and_panel_specification_v1.md`
- `pipelines/dispersion_path_dependence_research_module_v1.py`

Implementation-review note carried forward:

- Preserve the neutral zero-variance z-score convention: when a trailing z-score denominator is zero and the centered value is also zero, the z-score is neutral `0.0`, not missing. Panel audit must verify this convention is preserved.

## SECTION 3 - Candidate ID Policy

Allowed candidate IDs are frozen:

```text
dpath_01_relapse_resilience_after_calm
dpath_02_disagreement_vol_stress_divergence
dpath_03_elevated_disagreement_stabilization
dpath_04_consensus_without_crowding
```

Rules:

- Candidate count must equal 4.
- Candidate IDs must appear exactly as listed.
- Candidate order in manifests must follow the order above.
- Candidate IDs must not be aliased, shortened, renamed, or expanded.
- Any `dpath_05`, Smooth/Burst, `vov_`, `ecluster_`, or refinement candidate must fail panel-generation precheck.
- All rows must have `research_status = RESEARCH_ONLY`.

## SECTION 4 - Canonical Long-Form Panel Schema

Canonical panel shape:

- Long form.
- One row per `date` x `ticker` x `candidate_id`.
- The tuple `date`, `ticker`, `candidate_id` must be unique.
- Exactly four candidate IDs are allowed.

Canonical panel file:

- `dpath_signal_panel_long.parquet`

Required sort order:

1. `date`
2. `candidate_id`
3. `ticker`

Wide-form outputs:

- Wide-form outputs are diagnostic only.
- Any wide output must include `_diagnostic_wide` in the file name.
- Wide output must not be used for IC discovery.

## SECTION 5 - Required Panel Columns

Required canonical columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Signal date using after-close availability. |
| `ticker` | string | yes | Existing OHLCV research ticker identifier. |
| `candidate_id` | string | yes | Must be one of the four allowed IDs. |
| `candidate_name` | string | yes | Must match this specification. |
| `module_id` | string | yes | `dispersion_path_dependence_research_module_v1`. |
| `spec_id` | string | yes | `dispersion_path_dependence_formula_and_panel_specification_v1`. |
| `mechanism_family` | string | yes | One approved mechanism per candidate. |
| `research_status` | string | yes | `RESEARCH_ONLY`. |
| `primary_horizon` | string | yes | `h10`. |
| `secondary_horizons` | string | yes | `h5|h20`. |
| `expected_sign` | string | yes | `positive`. |
| `signal_value` | float | yes | Final candidate signal after activation handling. |
| `raw_score` | float | yes | Raw score after activation neutralization semantics are applied. |
| `pre_activation_raw_score` | float | yes | Formula score before inactive-state neutralization. |
| `is_active` | bool | yes | True only when activation condition is satisfied and required features are finite. |
| `feature_warmup_complete` | bool | yes | True only when security and date-level warmups are complete. |
| `finite_cross_section_count` | integer | yes | Finite active score count used for same-date ranking. |
| `rank_min_count` | integer | yes | Must equal 50 unless a future panel-spec amendment changes it before generation. |
| `missing_reason` | string or null | yes | Null or controlled reason code. |
| `timing_policy` | string | yes | `after_close_t_forward_returns_after_t`. |
| `formula_text` | string | yes | Exact formula text from implementation registry. |
| `activation_text` | string | yes | Exact activation text from implementation registry. |
| `anchor_comparators` | string | yes | Pipe-delimited comparator IDs. |
| `contamination_controls` | string | yes | Pipe-delimited contamination families. |
| `hypothesis` | string | yes | Candidate scientific hypothesis. |
| `scientific_question` | string | yes | Candidate scientific question. |
| `expected_evidence` | string | yes | Predeclared expected evidence. |
| `primary_falsification_criterion` | string | yes | Candidate primary falsification criterion. |
| `observable_implication` | string | yes | Candidate observable implication. |
| `expected_orthogonality` | string | yes | Predeclared orthogonality expectation. |
| `created_by_spec` | string | yes | `dispersion_path_dependence_formula_and_panel_specification_v1`. |

Required diagnostic columns:

| column | type | rule |
| --- | --- | --- |
| `disp_20` | float | Static dispersion diagnostic. |
| `disp_z_20` | float | Date-level normalized dispersion. |
| `disp_slope_5` | float | Short disagreement path slope. |
| `disp_slope_10` | float | Medium disagreement path slope. |
| `divergence_intensity` | float | Divergence-path diagnostic for `dpath_02`. |
| `mkt_vol_20` | float | Market volatility state reference. |
| `mkt_vol_slope_10` | float | Volatility path reference. |
| `mkt_stress_20` | float | OHLCV stress state reference. |
| `mkt_stress_slope_10` | float | Stress path reference. |
| `vov_5_20` | float | VoV contamination diagnostic. |
| `rank_churn_5` | float | Rank movement diagnostic. |
| `low_churn_5` | float | Rank-stability control. |
| `low_extension_20` | float | Extension/crowding control. |
| `leadership_crowding_60` | float | Leadership crowding diagnostic. |
| `emerging_improvement_5_20` | float | Consensus candidate improvement diagnostic. |

## SECTION 6 - Scientific Lineage Fields

Every panel row must preserve:

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

Every manifest must include lineage-note references:

- `scientific_review_note`: `dispersion_path_dependence_scientific_review_v1.md`
- `module_design_note`: `dispersion_path_dependence_research_module_design_v1.md`
- `mechanism_review_note`: `dispersion_path_dependence_scientific_mechanism_review_v1.md`
- `allocation_note`: `dispersion_path_dependence_candidate_allocation_and_formula_planning_v1.md`
- `formula_spec_note`: `dispersion_path_dependence_formula_and_panel_specification_v1.md`
- `implementation_note`: `dispersion_path_dependence_formula_implementation_v1.md`
- `implementation_review_note`: `dispersion_path_dependence_formula_implementation_review_v1.md`
- `panel_spec_note`: `dispersion_path_dependence_panel_specification_v1.md`

## SECTION 7 - Metadata JSON Schema

Future panel generation must emit `metadata.json` at the artifact root.

Required JSON fields:

```json
{
  "run_id": "string",
  "module_id": "dispersion_path_dependence_research_module_v1",
  "spec_id": "dispersion_path_dependence_panel_specification_v1",
  "formula_spec_id": "dispersion_path_dependence_formula_and_panel_specification_v1",
  "implementation_note": "dispersion_path_dependence_formula_implementation_v1.md",
  "implementation_review_note": "dispersion_path_dependence_formula_implementation_review_v1.md",
  "classification": "PANEL_SPEC_READY_WITH_SCIENTIFIC_NOTES",
  "candidate_ids": [
    "dpath_01_relapse_resilience_after_calm",
    "dpath_02_disagreement_vol_stress_divergence",
    "dpath_03_elevated_disagreement_stabilization",
    "dpath_04_consensus_without_crowding"
  ],
  "blocked_candidate_ids": ["dpath_05_smooth_versus_burst_resolution", "dpath_05"],
  "blocked_candidate_prefixes": ["vov_", "ecluster_"],
  "blocked_mechanisms": ["smooth_versus_burst_resolution", "event_clustering"],
  "candidate_count": 4,
  "family": "dispersion_path_dependence",
  "research_status": "RESEARCH_ONLY",
  "timing_policy": "after_close_t_forward_returns_after_t",
  "rank_min_count": 50,
  "activation_neutralization": "inactive_signal_value_0_5_with_is_active_false",
  "zero_variance_z_score_policy": "centered_zero_and_std_zero_maps_to_0_0",
  "panel_shape": "long",
  "artifact_root": "artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/",
  "source_data_access": "existing_local_ohlcv_only",
  "external_data_accessed": false,
  "panel_generation_executed": true,
  "ic_scoring_executed": false,
  "validation_executed": false,
  "governance_modified": false,
  "production_registration": false,
  "threshold_changed": false,
  "ml_integration": false,
  "created_at_utc": "ISO-8601 timestamp"
}
```

Specification-note clarification:

- In this note, `panel_generation_executed` remains false because no generation is performed.
- In future panel-generation metadata, `panel_generation_executed` must be true only after the panel writer completes successfully.

## SECTION 8 - Panel Manifest Schema

Future panel generation must emit `panel_manifest.json`.

Required fields:

| field | type | rule |
| --- | --- | --- |
| `artifact_root` | string | Must equal frozen artifact root. |
| `canonical_panel_path` | string | Must point to `dpath_signal_panel_long.parquet`. |
| `metadata_path` | string | Must point to `metadata.json`. |
| `candidate_registry_path` | string | Must point to `candidate_registry.csv`. |
| `candidate_formula_manifest_path` | string | Must point to `candidate_formula_manifest.csv`. |
| `feature_manifest_path` | string | Must point to `feature_manifest.csv`. |
| `input_schema_manifest_path` | string | Must point to `input_schema_manifest.csv`. |
| `contamination_manifest_path` | string | Must point to `contamination_control_manifest.csv`. |
| `row_count` | integer | Total canonical panel rows. |
| `date_min` | date | Earliest signal date emitted. |
| `date_max` | date | Latest signal date emitted. |
| `ticker_count` | integer | Distinct ticker count. |
| `candidate_count` | integer | Must equal 4. |
| `candidate_ids` | list[string] | Must equal allowed IDs in frozen order. |
| `duplicate_key_count` | integer | Must equal 0. |
| `invalid_candidate_count` | integer | Must equal 0. |
| `blocked_deferred_candidate_count` | integer | Must equal 0 emitted rows. |
| `missing_signal_count` | integer | Count of null `signal_value` rows. |
| `inactive_row_count` | integer | Count of `is_active = false` rows. |
| `warmup_incomplete_count` | integer | Count of `feature_warmup_complete = false` rows. |
| `rank_min_count` | integer | Must equal 50. |
| `dates_below_rank_min_count` | integer | Count of candidate-dates below finite rank minimum. |
| `date_level_warmup_min` | integer | Must equal 252. |
| `security_warmup_min` | integer | Must equal 60. |
| `timing_policy` | string | Must equal `after_close_t_forward_returns_after_t`. |
| `zero_variance_z_score_policy` | string | Must match metadata JSON. |
| `checksum_policy` | string | Required if local tooling supports checksums. |
| `input_data_checksum` | string or null | Required if source-data checksum is available. |
| `canonical_panel_checksum` | string or null | Required if checksum tooling is available. |
| `candidate_registry_checksum` | string or null | Required if checksum tooling is available. |
| `formula_manifest_checksum` | string or null | Required if checksum tooling is available. |
| `stop_condition_triggered` | bool | True only if writer halted or emitted a fail-closed panel. |
| `stop_condition_reason` | string or null | Required when stopped. |

## SECTION 9 - Formula Manifest Schema

Future panel generation must emit `candidate_formula_manifest.csv`.

Required fields:

| field | rule |
| --- | --- |
| `candidate_id` | One of four allowed IDs. |
| `candidate_name` | Must match frozen registry. |
| `mechanism_family` | One approved mechanism. |
| `formula_text` | Exact formula text from implementation registry. |
| `activation_text` | Exact activation text from implementation registry. |
| `primary_horizon` | h10. |
| `secondary_horizons` | h5|h20. |
| `expected_sign` | positive. |
| `required_raw_inputs` | Pipe-delimited OHLCV inputs. |
| `derived_features` | Pipe-delimited features used by the candidate. |
| `cross_sectional_features` | Pipe-delimited same-date rank or cross-sectional features. |
| `anchor_comparators` | Pipe-delimited anchors. |
| `contamination_controls` | Pipe-delimited controls. |
| `hypothesis` | Candidate-specific hypothesis. |
| `scientific_question` | Candidate-specific question. |
| `primary_falsification_criterion` | Candidate-specific criterion. |
| `created_by_spec` | `dispersion_path_dependence_panel_specification_v1`. |

Validation rule:

- Formula manifest candidate IDs must exactly match canonical panel candidate IDs.
- Formula text must not be rewritten during panel generation.

## SECTION 10 - Feature Manifest Schema

Future panel generation must emit `feature_manifest.csv`.

Required fields:

| field | rule |
| --- | --- |
| `feature_name` | Feature column name. |
| `feature_scope` | `raw`, `security_rolling`, `cross_sectional`, `date_level`, `diagnostic`, or `lineage`. |
| `definition` | Plain-language definition. |
| `lookback_window` | Integer or null. |
| `min_periods` | Integer or null. |
| `uses_cross_section` | Boolean. |
| `uses_date_level_history` | Boolean. |
| `uses_future_data` | Must be false. |
| `required_for_candidates` | Pipe-delimited candidate IDs. |
| `missing_policy` | Controlled missing behavior. |
| `warmup_policy` | Security/date warmup requirement if applicable. |
| `timing_policy` | Must equal after-close policy. |

Minimum required feature entries:

- raw OHLCV: `date`, `ticker`, `open`, `high`, `low`, `close`, `volume`
- returns and rolling security features: `ret_1`, `ret_5`, `ret_10`, `ret_20`, `ret_60`, `range_1`, `range_20`, `vol_5`, `vol_20`, `vov_5_20`, `drawdown_20`, `dollar_volume_20`
- dispersion/path features: `disp_1`, `disp_5`, `disp_10`, `disp_20`, `disp_z_20`, `disp_slope_5`, `disp_slope_10`, `disp_accel_5_10`
- market path features: `mkt_vol_20`, `mkt_vol_slope_10`, `mkt_stress_20`, `mkt_stress_slope_10`, `vov_path_10`, `divergence_intensity`
- security controls: `rank_ret_5`, `low_extension_20`, `rank_churn_5`, `low_churn_5`, `liquidity_rank_20`, `leadership_crowding_60`, `emerging_improvement_5_20`

## SECTION 11 - Input Schema Manifest

Future panel generation must emit `input_schema_manifest.csv`.

Required raw input columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Trading date. |
| `ticker` | string | yes | Research ticker identifier. |
| `open` | float | yes | Same-date open. |
| `high` | float | yes | Same-date high. |
| `low` | float | yes | Same-date low. |
| `close` | float | yes | Adjusted close if available in existing dataset; otherwise close. |
| `volume` | float | yes | Same-date volume. |

Input validation rules:

- Required columns must exist.
- Dates must parse as dates.
- Tickers must be non-null strings.
- OHLCV numeric columns must be numeric or coercible to numeric.
- No future returns, labels, validation outcomes, governance labels, sector metadata, PIT metadata, or ML features may be used.
- Missing OHLCV values are not imputed.

## SECTION 12 - Artifact Directory Structure

Frozen artifact root:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

Required future artifacts:

- `metadata.json`
- `panel_manifest.json`
- `candidate_registry.csv`
- `candidate_formula_manifest.csv`
- `feature_manifest.csv`
- `input_schema_manifest.csv`
- `contamination_control_manifest.csv`
- `dpath_signal_panel_long.parquet`
- `dpath_feature_diagnostics_long.parquet`
- `panel_integrity_summary.csv`
- `missing_data_summary.csv`
- `activation_summary.csv`
- `warmup_summary.csv`
- `duplicate_key_report.csv`
- `blocked_candidate_report.csv`
- `stop_condition_precheck.csv`

Optional future artifacts:

- `dpath_signal_panel_diagnostic_wide.parquet`
- `anchor_comparator_panel_long.parquet`
- `contamination_reference_alignment.csv`

This panel specification does not create any directory or artifact.

## SECTION 13 - Activation-Neutralization Semantics

Activation handling is frozen:

1. Compute `pre_activation_raw_score` from the candidate formula using OHLCV-only trailing and same-date cross-sectional features.
2. Compute `is_active` from the candidate activation condition.
3. If features are mature, formula raw score is finite, and `is_active = true`, rank active raw scores cross-sectionally by date and candidate into `signal_value`.
4. If features are mature and formula raw score is finite but `is_active = false`, set `signal_value = 0.5`, `raw_score = 0.5`, and `missing_reason = inactive_neutralized`.
5. If features are immature or required inputs are nonfinite, set `signal_value = null`, preserve reason, and exclude from IC eligibility.

Inactive rows are not missing-data failures. They are neutralized inactive states.

## SECTION 14 - Warmup and Missing-Data Rules

Warmup rules:

- Security-level warmup minimum: 60 observations.
- Date-level state warmup minimum: 252 observations.
- `feature_warmup_complete` must be false until both applicable warmups are satisfied.
- Warmup-incomplete rows must carry `missing_reason = rolling_warmup` unless a raw OHLCV input is missing.

Missing reason vocabulary:

- `raw_ohlcv_missing`
- `rolling_warmup`
- `insufficient_cross_section`
- `nonfinite_feature`
- `inactive_neutralized`
- `date_level_feature_missing`
- `invalid_candidate_id`
- `blocked_deferred_mechanism`

Zero-variance z-score rule:

- If a trailing z-score denominator is zero and the centered value is zero, emit neutral `0.0`.
- If the denominator is zero and the centered value is nonzero, emit null and use the appropriate nonfinite reason.

## SECTION 15 - After-Close Timing Policy

Timing policy:

- `after_close_t_forward_returns_after_t`

Rules:

- Signal date `t` may use OHLCV data through the close of `t`.
- No feature may use data after `t`.
- No forward return may be computed during panel generation.
- Forward returns for future IC discovery must begin after `t`.
- Same-date close usage must be documented in metadata and panel manifest.

## SECTION 16 - Duplicate Prevention

Duplicate-prevention rules:

- Canonical key: `date`, `ticker`, `candidate_id`.
- `duplicate_key_count` must equal 0.
- Candidate count must equal 4.
- `invalid_candidate_count` must equal 0.
- `blocked_deferred_candidate_count` must equal 0.
- Rows with candidate IDs outside the frozen list must fail precheck.
- Rows with Smooth/Burst, VoV, event-clustering, or refinement identifiers must fail precheck.

## SECTION 17 - Validation Rules

Panel-generation validation rules:

- Required columns exist.
- Canonical key is unique.
- Candidate IDs exactly match frozen list.
- Candidate count equals 4.
- Required lineage fields are non-null for all rows.
- `module_id`, `spec_id`, `research_status`, `timing_policy`, and horizon fields match frozen values.
- `rank_min_count` equals 50.
- `signal_value` is finite for active eligible rows.
- Inactive eligible rows have `signal_value = 0.5` and `missing_reason = inactive_neutralized`.
- Warmup-incomplete rows have null `signal_value` and `feature_warmup_complete = false`.
- Missing reason values are drawn only from the controlled vocabulary.
- `metadata.json` and `panel_manifest.json` agree on candidate IDs, artifact root, candidate count, timing policy, and generation flags.
- Checksums are populated when local checksum tooling is available.

Fail-closed rule:

- If any required validation rule fails, panel generation must stop or emit a stopped manifest with `stop_condition_triggered = true`.

## SECTION 18 - Stop Conditions Before Panel Generation

Panel generation must not begin if:

- implementation review classification is not `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES` or stronger;
- candidate IDs differ from the frozen list;
- Smooth/Burst, `dpath_05`, VoV, event-clustering, or refinement candidates appear;
- formula text differs from the reviewed implementation;
- activation text differs from the reviewed implementation;
- required lineage fields are unavailable;
- required raw OHLCV inputs are unavailable;
- after-close timing policy cannot be preserved;
- warmup and missing-data reason codes cannot be emitted;
- duplicate-key prevention cannot be enforced;
- artifact root would overwrite an existing non-draft panel without explicit approval;
- panel generation would also compute IC, run validation, modify governance, modify production registry, change thresholds, or introduce ML.

## SECTION 19 - Explicit Non-Goals

This note does not:

- implement panel writing;
- generate panels;
- create artifact directories;
- compute IC;
- run validation;
- modify formulas;
- modify governance decisions;
- modify the production registry;
- change thresholds;
- introduce ML;
- authorize Smooth/Burst;
- authorize extra candidates;
- authorize panel audit or IC discovery.

## SECTION 20 - Verification

Verification:

- Required sections exist: canonical long-form panel schema, required columns, scientific lineage fields, metadata JSON schema, panel manifest schema, formula manifest schema, feature manifest schema, input schema manifest, artifact directory structure, candidate ID policy, activation-neutralization semantics, warmup and missing-data rules, after-close timing policy, duplicate prevention, validation rules, stop conditions before panel generation, explicit non-goals, and classification.
- Exactly four candidates are included.
- Smooth/Burst remains excluded.
- No implementation files were changed by this panel-specification task.
- No panel files were generated.
- No IC work was performed.
- No validation was performed.
- No governance decision was modified.
- No production registry was modified.
- No threshold file was changed.
- No ML file was changed.

## SECTION 21 - Final Classification

Final classification:

- `PANEL_SPEC_READY_WITH_SCIENTIFIC_NOTES`

Panel generation may begin next, but only as the next lifecycle phase and only under the frozen contract above. This note does not authorize IC discovery, validation, governance changes, production registration, threshold changes, or ML.
