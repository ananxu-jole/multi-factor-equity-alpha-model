# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Panel Specification v1

## SECTION 1 - Specification Objective

This note freezes the panel-generation contract for the bounded OHLCV Volatility-of-Volatility refinement variants before any refinement panel writing.

Current input classification:

- `REFINEMENT_IMPLEMENTATION_READY_FOR_PANEL_SPEC`

Panel specification classification:

- `REFINEMENT_PANEL_SPEC_READY_FOR_IMPLEMENTATION`

This is a specification-only task. It does not implement panel writing, generate panels, compute IC, execute refinement, modify original VoV panels, modify original VoV formulas, modify governance decisions, modify production registry, change thresholds, or introduce ML.

## SECTION 2 - Inputs Reviewed

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_implementation_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_implementation_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_panel_specification_v1.md`

Implementation status reviewed:

- The bounded refinement implementation is classified `REFINEMENT_IMPLEMENTATION_READY_FOR_PANEL_SPEC`.
- The implementation exposes a long-form in-memory panel contract for exactly eight variants.
- No blocking implementation-review issues remain before panel specification.

## SECTION 3 - Variant Scope

Exactly eight refinement variants are approved for the panel contract:

| refinement_id | parent_candidate_id | refinement_family | source_spec_id | primary_horizon | secondary_horizons |
| --- | --- | --- | --- | --- | --- |
| `vov_01_ref_anchor` | `vov_01` | `vov_01_refinement` | `vov_01_instability_calm_after_chop__ref_anchor` | h20 | h10, h5 |
| `vov_01_ref_strict_calm` | `vov_01` | `vov_01_refinement` | `vov_01_instability_calm_after_chop__ref_strict_calm` | h20 | h10 |
| `vov_01_ref_longer_memory` | `vov_01` | `vov_01_refinement` | `vov_01_instability_calm_after_chop__ref_longer_memory` | h20 | h10 |
| `vov_01_ref_smoothed_calm` | `vov_01` | `vov_01_refinement` | `vov_01_instability_calm_after_chop__ref_smoothed_calm` | h20 | h10, h5 |
| `vov_03_ref_anchor` | `vov_03` | `vov_03_refinement` | `vov_03_range_chop_exhaustion__ref_anchor` | h10 | h20, h5 |
| `vov_03_ref_strict_chop` | `vov_03` | `vov_03_refinement` | `vov_03_range_chop_exhaustion__ref_strict_chop` | h10 | h20 |
| `vov_03_ref_longer_chop` | `vov_03` | `vov_03_refinement` | `vov_03_range_chop_exhaustion__ref_longer_chop` | h10 | h20, h5 |
| `vov_03_ref_extension_controlled` | `vov_03` | `vov_03_refinement` | `vov_03_range_chop_exhaustion__ref_extension_controlled` | h10 | h20 |

Blocked candidates and families:

- `vov_05`
- `vov_02`
- `vov_04`
- `dpath_*`
- `ecluster_*`

Any candidate registry, manifest, or panel containing a blocked candidate must fail validation.

## SECTION 4 - Canonical Long-Form Panel Schema

Canonical panel shape:

- Long-form by `date`, `ticker`, and `candidate_id`.
- One row per `date` x `ticker` x `candidate_id`.
- One parquet file per refinement variant.
- No wide-form canonical artifact is authorized.

Canonical key:

- `date`
- `ticker`
- `candidate_id`

The canonical key must be unique. Duplicate keys must fail validation.

Required sort order inside each per-variant panel:

1. `date`
2. `ticker`
3. `candidate_id`

Required global variant order in manifests:

1. `vov_01_ref_anchor`
2. `vov_01_ref_strict_calm`
3. `vov_01_ref_longer_memory`
4. `vov_01_ref_smoothed_calm`
5. `vov_03_ref_anchor`
6. `vov_03_ref_strict_chop`
7. `vov_03_ref_longer_chop`
8. `vov_03_ref_extension_controlled`

## SECTION 5 - Required Columns

Each per-variant panel must contain exactly the following required columns unless a future panel-generation review explicitly adds diagnostic columns in a separate artifact.

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Signal date. |
| `ticker` | string | yes | Existing OHLCV research ticker identifier. |
| `candidate_id` | string | yes | One of the eight frozen refinement IDs. |
| `source_spec_id` | string | yes | Frozen formula lineage ID. |
| `parent_candidate_id` | string | yes | `vov_01` or `vov_03`. |
| `module_id` | string | yes | `ohlcv_volatility_of_volatility_refinement_v1`. |
| `refinement_family` | string | yes | `vov_01_refinement` or `vov_03_refinement`. |
| `family` | string | yes | `volatility_of_volatility`. |
| `research_status` | string | yes | `RESEARCH_ONLY`. |
| `primary_horizon` | string | yes | Frozen primary horizon. |
| `secondary_horizons` | string | yes | Pipe-delimited secondary horizons. |
| `signal_value` | float | yes | Final same-date cross-sectional rank signal. |
| `raw_score` | float | yes | Score after activation neutralization and before final rank. |
| `pre_activation_raw_score` | float | yes | Formula score before inactive-state neutralization. |
| `is_active` | bool | yes | Activation flag. |
| `feature_warmup_complete` | bool | yes | True only when all required rolling features are available. |
| `finite_cross_section_count` | integer | yes | Same-date finite count used for ranking. |
| `rank_min_count` | integer | yes | Minimum finite count required for rank generation, fixed at 50. |
| `missing_reason` | string | yes | Null or controlled reason code. |
| `timing_policy` | string | yes | `after_close_t_forward_returns_after_t`. |
| `created_by_spec` | string | yes | `ohlcv_volatility_of_volatility_bounded_refinement_panel_specification_v1`. |

Allowed `missing_reason` values:

- null / missing
- `rolling_warmup`
- `inactive_zeroed`
- `insufficient_cross_section`
- `missing_input`
- `nonfinite_feature`

## SECTION 6 - Identifier Policy

Identifier policy:

| identifier | rule |
| --- | --- |
| `refinement_id` | Conceptual name for each frozen refinement variant; stored in panel column `candidate_id`. |
| `candidate_id` | Canonical panel ID; must equal one of the eight frozen refinement IDs. |
| `parent_candidate_id` | Must equal `vov_01` or `vov_03`. |
| `source_spec_id` | Immutable formula lineage from the formula specification. |
| `module_id` | Must equal `ohlcv_volatility_of_volatility_refinement_v1`. |
| `refinement_family` | Must equal `vov_01_refinement` for `vov_01_*` variants and `vov_03_refinement` for `vov_03_*` variants. |
| `family` | Must equal `volatility_of_volatility`. |

No aliasing, renaming, shortened IDs, or extra refinement IDs are allowed.

## SECTION 7 - Anchor-Handling Policy

Anchor variants:

- `vov_01_ref_anchor`
- `vov_03_ref_anchor`

Anchor policy:

- Anchor variants must be generated from the same implementation path as non-anchor variants, not copied from the original VoV panel artifacts.
- Anchor formulas must remain equivalent to original `vov_01` and `vov_03` implementation outputs.
- Anchor rows must use refinement IDs, refinement metadata, and refinement artifact paths.
- Original VoV module panels must not be modified, copied into, overwritten, or used as canonical refinement panels.
- Future panel audit must verify anchor equivalence after artifact writing.

Anchor metadata:

- `parent_candidate_id` must record `vov_01` or `vov_03`.
- `source_spec_id` must include the `__ref_anchor` suffix.
- `refinement_family` must identify the parent refinement branch.

## SECTION 8 - Activation-Neutralization Semantics

Activation handling is frozen:

1. Compute `pre_activation_raw_score` from the frozen formula.
2. Compute `is_active` from the frozen activation condition.
3. If required raw OHLCV fields or derived features are missing or nonfinite, keep `pre_activation_raw_score`, `raw_score`, and `signal_value` missing.
4. If `pre_activation_raw_score` is finite and `is_active = false`, set `raw_score = 0.0` before final ranking.
5. If `pre_activation_raw_score` is finite and `is_active = true`, set `raw_score = pre_activation_raw_score`.
6. Compute `signal_value` as same-date cross-sectional percentile rank of finite `raw_score`.
7. Preserve `is_active`, `pre_activation_raw_score`, `raw_score`, and `missing_reason`.

Inactive zeroing is not a missing-data fill. It is a neutral pre-rank state for finite observations outside the activation condition.

## SECTION 9 - After-Close Timing Policy

Timing policy:

- `after_close_t_forward_returns_after_t`

Rules:

- A signal dated `t` may use OHLCV data through the close of date `t`.
- The signal is considered available only after the close of date `t`.
- Any future IC or refinement scoring must align forward returns strictly after `t`.
- Same-day intraday execution is not authorized.
- No future return, future volume, future volatility, future rank, future universe, or future metadata field may enter a signal dated `t`.

Both metadata JSON and panel manifests must include the timing policy.

## SECTION 10 - Warmup And Missing-Data Rules

Warmup policy:

- Retain warmup rows for auditability.
- Set `feature_warmup_complete = false` until all required rolling features for the variant are available.
- For warmup-incomplete rows, `signal_value`, `raw_score`, and `pre_activation_raw_score` must be missing.
- `missing_reason` must be `rolling_warmup` for warmup-incomplete rows.

Warmup requirements:

- `vov_01_ref_anchor`, `vov_01_ref_strict_calm`, `vov_01_ref_smoothed_calm`, `vov_03_ref_anchor`, `vov_03_ref_strict_chop`, and `vov_03_ref_extension_controlled` require the original short-window feature maturity.
- `vov_01_ref_longer_memory` requires maturity for `vov_10_40`, `vov_slope_10`, `range_chop_40`, and their 10-day lags.
- `vov_03_ref_longer_chop` requires maturity for `range_chop_40`, `range_chop_slope_10`, and the 10-day lag.

Missing-data policy:

- Missing raw OHLCV input causes dependent feature and score fields to remain missing.
- Infinite values must be treated as missing.
- Missing scores must not be converted to zero.
- Only inactive finite observations may be neutralized to zero.

## SECTION 11 - Duplicate Prevention

Duplicate prevention rules:

- Each per-variant panel must have zero duplicate `date`, `ticker`, `candidate_id` keys.
- The panel manifest must record `duplicate_key_count`.
- `duplicate_key_count` must equal 0.
- Candidate IDs must appear only in their own per-variant parquet files.
- No panel may contain blocked candidate IDs or prefixes.

Validation must fail if any duplicate key is found.

## SECTION 12 - Artifact Directory Structure

Artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`

Required files:

| file | purpose |
| --- | --- |
| `metadata.json` | Run-level metadata and guardrail flags. |
| `panel_manifest.csv` | One row per per-variant parquet panel. |
| `panel_generation_summary.csv` | Aggregate row counts, date ranges, candidate counts, and validation status. |
| `panel_generation_manifest.json` | Full generation manifest and fail-closed guardrail flags. |
| `schema_validation_report.csv` | Column, type, ID, duplicate-key, and timing-policy validation results. |
| `candidate_registry.csv` | Frozen refinement registry. |
| `candidate_formula_manifest.csv` | Frozen formula strings and formula hashes. |
| `derived_feature_manifest.csv` | Derived features used by each variant. |
| `input_schema.csv` | Required raw OHLCV input schema. |

Required per-variant parquet files:

- `vov_01_ref_anchor_signal_panel.parquet`
- `vov_01_ref_strict_calm_signal_panel.parquet`
- `vov_01_ref_longer_memory_signal_panel.parquet`
- `vov_01_ref_smoothed_calm_signal_panel.parquet`
- `vov_03_ref_anchor_signal_panel.parquet`
- `vov_03_ref_strict_chop_signal_panel.parquet`
- `vov_03_ref_longer_chop_signal_panel.parquet`
- `vov_03_ref_extension_controlled_signal_panel.parquet`

This specification does not create the artifact root or any artifact files.

## SECTION 13 - Metadata JSON Schema

Future `metadata.json` must include:

| field | value / rule |
| --- | --- |
| `run_id` | Future panel generation run identifier. |
| `module_id` | `ohlcv_volatility_of_volatility_refinement_v1`. |
| `spec_id` | `ohlcv_volatility_of_volatility_bounded_refinement_panel_specification_v1`. |
| `formula_spec_id` | `ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1`. |
| `implementation_note` | `ohlcv_volatility_of_volatility_bounded_refinement_implementation_v1`. |
| `implementation_review_note` | `ohlcv_volatility_of_volatility_bounded_refinement_implementation_review_v1`. |
| `classification` | `REFINEMENT_PANEL_SPEC_READY_FOR_IMPLEMENTATION`. |
| `candidate_ids` | ordered list of the eight frozen refinement IDs. |
| `parent_candidate_ids` | `vov_01`, `vov_03`. |
| `blocked_candidates` | `vov_05`, `vov_02`, `vov_04`, `dpath_*`, `ecluster_*`. |
| `family` | `volatility_of_volatility`. |
| `refinement_families` | `vov_01_refinement`, `vov_03_refinement`. |
| `research_status` | `RESEARCH_ONLY`. |
| `timing_policy` | `after_close_t_forward_returns_after_t`. |
| `rank_min_count` | 50. |
| `activation_neutralization` | `inactive_pre_rank_raw_score_zero`. |
| `panel_shape` | `long_per_variant`. |
| `created_at_utc` | ISO-8601 timestamp from future panel run. |
| `source_data_access` | `existing_local_ohlcv_only`. |
| `external_data_accessed` | false. |
| `formula_hashes` | mapping of refinement ID to formula hash. |
| `guardrail_flags` | object of fail-closed booleans. |

Required guardrail flags:

- `panel_generation_executed`: true only in a future authorized panel-generation run.
- `ic_scoring_executed`: false.
- `refinement_scoring_executed`: false.
- `validation_executed`: false.
- `original_vov_panels_modified`: false.
- `original_vov_formulas_modified`: false.
- `governance_modified`: false.
- `production_registration`: false.
- `thresholds_modified`: false.
- `ml_integration`: false.

## SECTION 14 - Panel Manifest Schema

Future `panel_manifest.csv` must include one row per per-variant parquet file.

Required columns:

| column | rule |
| --- | --- |
| `candidate_id` | One of the eight frozen refinement IDs. |
| `parent_candidate_id` | `vov_01` or `vov_03`. |
| `source_spec_id` | Frozen source lineage ID. |
| `refinement_family` | `vov_01_refinement` or `vov_03_refinement`. |
| `panel_path` | Relative path to `{candidate_id}_signal_panel.parquet`. |
| `row_count` | Number of rows in the parquet file. |
| `date_min` | Earliest signal date. |
| `date_max` | Latest signal date. |
| `ticker_count` | Distinct ticker count. |
| `duplicate_key_count` | Must equal 0. |
| `missing_signal_count` | Count of missing `signal_value` rows. |
| `inactive_row_count` | Count of `is_active = false` rows. |
| `warmup_incomplete_count` | Count of `feature_warmup_complete = false` rows. |
| `rank_min_count` | Must equal 50 unless separately approved. |
| `dates_below_rank_min_count` | Count of dates below rank minimum. |
| `timing_policy` | Must equal `after_close_t_forward_returns_after_t`. |
| `schema_status` | PASS or FAIL. |
| `blocked_candidate_check` | PASS or FAIL. |
| `anchor_equivalence_required` | true for anchor variants, false otherwise. |
| `anchor_equivalence_status` | PASS, FAIL, or NA. |

The manifest must contain exactly eight rows.

## SECTION 15 - Refinement Manifest Schema

Future `panel_generation_manifest.json` must include:

| field | rule |
| --- | --- |
| `manifest_version` | `v1`. |
| `module_id` | `ohlcv_volatility_of_volatility_refinement_v1`. |
| `specification_note` | this note path. |
| `formula_specification_note` | formula and panel specification note path. |
| `implementation_review_note` | implementation review note path. |
| `artifact_root` | `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`. |
| `variant_count` | exactly 8. |
| `candidate_ids` | ordered list of eight frozen refinement IDs. |
| `parent_candidate_map` | mapping from each refinement ID to `vov_01` or `vov_03`. |
| `source_spec_map` | mapping from each refinement ID to source spec ID. |
| `refinement_family_map` | mapping from each refinement ID to refinement family. |
| `formula_hashes` | hash of each frozen formula string. |
| `panel_files` | list of required per-variant parquet files. |
| `timing_policy` | `after_close_t_forward_returns_after_t`. |
| `blocked_candidate_check` | PASS or FAIL. |
| `schema_validation_status` | PASS or FAIL. |
| `duplicate_key_status` | PASS or FAIL. |
| `anchor_equivalence_status` | PASS, FAIL, or NOT_RUN. |
| `guardrail_flags` | fail-closed booleans for forbidden actions. |

## SECTION 16 - Validation Rules

Panel generation validation must confirm:

- Exactly eight per-variant parquet files exist.
- Exactly eight manifest rows exist.
- Candidate IDs match the frozen ordered list.
- Parent IDs are only `vov_01` and `vov_03`.
- Source-spec IDs match the formula specification.
- Module ID is `ohlcv_volatility_of_volatility_refinement_v1`.
- Refinement families match parent branches.
- Required columns are present with compatible types.
- Duplicate key count is zero.
- Timing policy is correct.
- Warmup and missing-data rules are followed.
- Inactive finite observations are zeroed before ranking.
- Missing observations are not zero-filled.
- Anchor panels are equivalent to original in-memory anchor behavior.
- No blocked candidates or families are present.

## SECTION 17 - Stop Conditions Before Panel Generation

Stop before panel generation if:

- Any candidate outside the eight frozen refinement IDs is present.
- Any blocked candidate or family appears: `vov_05`, `vov_02`, `vov_04`, `dpath_*`, or `ecluster_*`.
- The implementation no longer passes focused refinement tests.
- Anchor equivalence tests fail before writing.
- Required metadata fields cannot be emitted.
- Formula hashes cannot be recorded.
- The panel root already contains incompatible or stale artifacts and cannot be safely overwritten by an authorized writer.
- The panel writer would modify original VoV panels or original VoV formulas.

## SECTION 18 - Explicit Non-Goals

This specification does not:

- implement panel writing;
- generate panels;
- compute IC;
- execute refinement;
- modify original VoV panels;
- modify original VoV formulas;
- modify governance decisions;
- modify production registry;
- change thresholds;
- introduce ML.

## SECTION 19 - Verification Summary

Verification status:

- Required sections are present.
- Exactly eight refinement variants are included.
- Blocked candidates remain excluded: `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*`.
- Classification appears: `REFINEMENT_PANEL_SPEC_READY_FOR_IMPLEMENTATION`.
- No implementation files were changed by this specification note.
- No panels were generated.
- No IC was computed.
- No validation was performed.
- No governance decisions were modified.
- No production files were changed.
- No thresholds were changed.
- No ML was introduced.

Final classification:

- `REFINEMENT_PANEL_SPEC_READY_FOR_IMPLEMENTATION`
