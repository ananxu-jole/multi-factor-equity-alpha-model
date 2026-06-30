# Project Underdog - OHLCV Volatility-of-Volatility Research Module Panel Specification v1

## SECTION 1 - Specification Objective

This note freezes the panel-generation contract for the OHLCV Volatility-of-Volatility research module before any panel-writing implementation.

This is a specification-only closeout of the minor review items from `ohlcv_volatility_of_volatility_research_module_implementation_review_v1.md`. It does not implement a panel writer, generate panels, compute IC, run discovery, run redundancy screening, run refinement, run validation, modify governance, modify production registry, change thresholds, or introduce ML.

Reviewed notes:

- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_implementation_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_implementation_v1.md`
- `docs/research_notes/ohlcv_vov_dpd_event_clustering_formula_and_panel_specification_v1.md`

Input implementation status:

- `MODULE_IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`

Panel specification classification:

- `PANEL_SPEC_READY_FOR_IMPLEMENTATION`

## SECTION 2 - Canonical Long-Form Panel Schema

The canonical research artifact must be long-form by `date`, `ticker`, and `candidate_id`.

Required grain:

- One row per `date` x `ticker` x `candidate_id`.
- Exactly five candidate IDs are allowed: `vov_01`, `vov_02`, `vov_03`, `vov_04`, and `vov_05`.
- No `dpath_*` or `ecluster_*` rows are allowed.

Canonical panel file:

- `vov_signal_panel_long.parquet`

Required sort order:

1. `date`
2. `candidate_id`
3. `ticker`

Duplicate key:

- The tuple `date`, `ticker`, `candidate_id` must be unique.

Wide-form outputs:

- Wide-form output is diagnostic only.
- Any wide diagnostic file must be clearly named with `_diagnostic_wide`.
- Wide output must not be treated as the canonical research panel.

## SECTION 3 - Required Columns

Canonical long-form panel columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Signal date using after-close availability. |
| `ticker` | string | yes | Existing OHLCV research ticker identifier. |
| `candidate_id` | string | yes | One of `vov_01` through `vov_05`. |
| `source_spec_id` | string | yes | Full formula-spec ID. |
| `module_id` | string | yes | `ohlcv_volatility_of_volatility_research_module_v1`. |
| `family` | string | yes | `volatility_of_volatility`. |
| `research_status` | string | yes | `RESEARCH_ONLY`. |
| `primary_horizon` | string | yes | `h10` for all five candidates. |
| `secondary_horizons` | string | yes | Pipe-delimited list, expected `h5|h20`. |
| `signal_value` | float | yes | Final cross-sectional rank signal after activation handling. |
| `raw_score` | float | yes | Formula score before final cross-sectional rank. |
| `pre_activation_raw_score` | float | yes | Formula score before inactive-state neutralization. |
| `is_active` | bool | yes | Activation flag. Continuous candidates use true when required inputs are finite. |
| `feature_warmup_complete` | bool | yes | True only when required rolling features are mature. |
| `finite_cross_section_count` | integer | yes | Finite candidate count used for same-date ranking. |
| `rank_min_count` | integer | yes | Minimum finite count required for ranking, expected 50. |
| `missing_reason` | string | yes | Null or controlled reason code. |
| `timing_policy` | string | yes | `after_close_t_forward_returns_after_t`. |
| `created_by_spec` | string | yes | `ohlcv_volatility_of_volatility_research_module_panel_specification_v1`. |

Optional diagnostic columns may be emitted in the canonical panel only if they are stable, scalar, and documented in the manifest. Preferred diagnostic handling is a separate feature panel.

Allowed optional diagnostic columns:

- `ret_1`
- `ret_5`
- `ret_10`
- `ret_20`
- `vol_5`
- `vol_20`
- `vov_5_20`
- `vov_10_40`
- `vov_slope_5`
- `vov_slope_10`
- `range_chop_20`
- `range_chop_slope_5`
- `low_extension_20`
- `rank_churn_5`
- `low_churn_5`

## SECTION 4 - Candidate Identifier Policy

Canonical code IDs:

- `vov_01`
- `vov_02`
- `vov_03`
- `vov_04`
- `vov_05`

Required source-spec lineage:

| candidate_id | source_spec_id |
| --- | --- |
| `vov_01` | `vov_01_instability_calm_after_chop` |
| `vov_02` | `vov_02_low_extension_vov_rise` |
| `vov_03` | `vov_03_range_chop_exhaustion` |
| `vov_04` | `vov_04_vov_slope_divergence` |
| `vov_05` | `vov_05_churn_controlled_vov_stabilization` |

Module ID:

- `ohlcv_volatility_of_volatility_research_module_v1`

Identifier decisions:

- `candidate_id` is the canonical code and panel ID.
- `source_spec_id` is the immutable formula-spec lineage ID.
- `module_id` identifies the implementation module that generated candidate values.
- No panel writer may rename, expand, or alias candidate IDs without a new specification note.

## SECTION 5 - Metadata JSON Schema

The panel writer must emit `metadata.json` at the artifact root.

Required JSON fields:

```json
{
  "run_id": "string",
  "module_id": "ohlcv_volatility_of_volatility_research_module_v1",
  "spec_id": "ohlcv_volatility_of_volatility_research_module_panel_specification_v1",
  "implementation_note": "ohlcv_volatility_of_volatility_research_module_implementation_v1",
  "implementation_review_note": "ohlcv_volatility_of_volatility_research_module_implementation_review_v1",
  "classification": "PANEL_SPEC_READY_FOR_IMPLEMENTATION",
  "candidate_ids": ["vov_01", "vov_02", "vov_03", "vov_04", "vov_05"],
  "blocked_candidate_prefixes": ["dpath_", "ecluster_"],
  "family": "volatility_of_volatility",
  "research_status": "RESEARCH_ONLY",
  "timing_policy": "after_close_t_forward_returns_after_t",
  "rank_min_count": 50,
  "activation_neutralization": "inactive_pre_rank_raw_score_zero",
  "panel_shape": "long",
  "created_at_utc": "ISO-8601 timestamp",
  "source_data_access": "existing_local_ohlcv_only",
  "external_data_accessed": false,
  "panel_generation_executed": true,
  "ic_scoring_executed": false,
  "discovery_executed": false,
  "validation_executed": false,
  "governance_modified": false,
  "production_registration": false,
  "ml_integration": false
}
```

The value `panel_generation_executed` must be false in specification notes and true only in the future panel-generation run metadata after a writer is explicitly authorized.

## SECTION 6 - Panel Manifest Schema

The panel writer must emit `panel_manifest.json`.

Required fields:

| field | type | rule |
| --- | --- | --- |
| `artifact_root` | string | Root directory for this panel run. |
| `canonical_panel_path` | string | Path to `vov_signal_panel_long.parquet`. |
| `feature_diagnostic_path` | string or null | Path to optional feature diagnostics. |
| `candidate_registry_path` | string | Path to frozen candidate registry CSV. |
| `row_count` | integer | Total canonical panel rows. |
| `date_min` | date | Earliest signal date emitted. |
| `date_max` | date | Latest signal date emitted. |
| `ticker_count` | integer | Distinct ticker count. |
| `candidate_count` | integer | Must equal 5. |
| `candidate_ids` | list[string] | Must equal approved VoV candidate IDs. |
| `duplicate_key_count` | integer | Must equal 0. |
| `invalid_candidate_count` | integer | Must equal 0. |
| `missing_signal_count` | integer | Count of missing `signal_value` rows. |
| `inactive_row_count` | integer | Count of rows with `is_active = false`. |
| `warmup_incomplete_count` | integer | Count of rows with `feature_warmup_complete = false`. |
| `rank_min_count` | integer | Expected 50. |
| `dates_below_rank_min_count` | integer | Count of candidate-dates below rank minimum. |
| `timing_policy` | string | Must match metadata JSON. |
| `checksum_policy` | string | Required if local tooling supports checksums. |
| `stop_condition_triggered` | bool | True only if writer halted before producing canonical panel. |
| `stop_condition_reason` | string or null | Required when stopped. |

## SECTION 7 - Artifact Directory Structure

Future artifact root:

`artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1/`

Required future artifacts:

- `metadata.json`
- `panel_manifest.json`
- `candidate_registry.csv`
- `candidate_formula_manifest.csv`
- `input_schema.csv`
- `derived_feature_manifest.csv`
- `vov_signal_panel_long.parquet`
- `panel_integrity_summary.csv`
- `missing_data_summary.csv`
- `activation_summary.csv`
- `warmup_summary.csv`
- `duplicate_key_report.csv`

Optional diagnostic artifacts:

- `vov_feature_diagnostics_long.parquet`
- `vov_signal_panel_diagnostic_wide.parquet`

This specification does not create the artifact root or any artifact files.

## SECTION 8 - Activation-Neutralization Semantics

Activation handling is frozen as follows:

1. Compute `pre_activation_raw_score` from the candidate formula using OHLCV-only trailing features.
2. Compute `is_active` from the candidate activation condition.
3. If `is_active = true`, set `raw_score = pre_activation_raw_score`.
4. If `is_active = false`, set `raw_score = 0.0` before final cross-sectional ranking.
5. If required raw OHLCV or formula features are missing or nonfinite, keep `pre_activation_raw_score`, `raw_score`, and `signal_value` missing rather than zeroing.
6. Compute `signal_value` as same-date cross-sectional percentile rank of `raw_score` for finite rows only.
7. Preserve `is_active` and `missing_reason` so inactive zeroing can be audited.

Inactive zeroing is not a missing-data fill. It is a pre-rank neutral state for observations whose formula features are available but whose activation condition is false.

Candidates with no explicit activation condition:

- Treat `is_active = true` when required features are finite and warmup is complete.

## SECTION 9 - After-Close Timing Policy

Timing policy:

- `after_close_t_forward_returns_after_t`

Rules:

- A signal dated `t` may use OHLCV fields through the close of date `t`.
- The signal is considered available only after the close of date `t`.
- Any future forward return label must begin strictly after `t`.
- Same-day intraday execution is not authorized.
- No future return, future volume, future volatility, future rank, future universe, or future metadata field may enter a signal dated `t`.

Manifest requirement:

- Both `metadata.json` and `panel_manifest.json` must include the timing policy string.

## SECTION 10 - Warmup Trimming Rules

Warmup policy:

- No backfill is allowed.
- Rolling features remain missing until their trailing windows are complete.
- `feature_warmup_complete` must be false when any formula-required rolling feature is unavailable.
- Rows may remain in the panel during warmup only if `signal_value` is missing and `missing_reason = rolling_warmup`.

Preferred canonical panel policy:

- Retain warmup rows with explicit missing reason for auditability.
- Discovery and IC tasks may later trim warmup rows, but trimming is not part of the panel writer unless separately specified.

Minimum rolling-history expectations:

| candidate_id | expected limiting feature | minimum practical history |
| --- | --- | ---: |
| `vov_01` | `lag(vov_5_20,5)`, `range_chop_20` | at least 30 trading days |
| `vov_02` | `vov_slope_5`, `ret_20` | at least 30 trading days |
| `vov_03` | `lag(range_chop_20,5)`, `ret_10` | at least 30 trading days |
| `vov_04` | `vov_slope_10`, `delta(vol_20,10)` | at least 70 trading days |
| `vov_05` | `lag(vov_10_40,10)`, `vov_slope_10` | at least 70 trading days |

The implementation may compute exact warmup readiness from finite feature availability rather than hard-coded day counts.

## SECTION 11 - Missing-Data Rules

Missing reason vocabulary:

- `raw_ohlcv_missing`
- `rolling_warmup`
- `insufficient_cross_section`
- `nonfinite_feature`
- `inactive_zeroed`
- `invalid_candidate_id`
- `duplicate_key`
- `schema_violation`

Rules:

- Missing raw `open`, `high`, `low`, `close`, or `volume` makes candidate outputs missing for that ticker-date.
- Infinite values must be converted to missing.
- Missing rolling features make formula-specific outputs missing.
- Missing values must not be converted to zero except for active-condition false states with finite formula inputs.
- `inactive_zeroed` may be used only when required inputs are finite, warmup is complete, and `is_active = false`.
- Dates with fewer than 50 finite candidate values must have `signal_value` missing for that candidate-date and `missing_reason = insufficient_cross_section`.

## SECTION 12 - Duplicate Prevention

Duplicate prevention rules:

- The canonical panel key is `date`, `ticker`, `candidate_id`.
- The writer must fail before saving the canonical panel if duplicate keys are present.
- `candidate_registry.csv` must contain exactly one row per candidate ID.
- `source_spec_id` must be one-to-one with `candidate_id`.
- `module_id` must be constant across the panel.
- The manifest must report `duplicate_key_count = 0`.

No append-in-place behavior is allowed for the canonical panel. A future rerun must write to a fresh run directory or replace a draft directory only under an explicitly approved non-production research workflow.

## SECTION 13 - Validation Rules

Pre-write validation rules:

- Required input columns are present.
- Candidate registry contains exactly `vov_01` through `vov_05`.
- No blocked candidate prefix appears.
- All candidate metadata fields are non-missing.
- Required derived feature columns exist before formula scoring.
- Timing policy is recorded.
- Activation-neutralization policy is recorded.
- Finite cross-sectional rank counts are computed by `date` and `candidate_id`.
- No duplicate canonical keys exist.

Post-write validation rules:

- Canonical panel file exists at the manifest path.
- Manifest row count equals canonical panel row count.
- Candidate count equals 5.
- Candidate IDs match the approved set exactly.
- Duplicate key count equals 0.
- No Family B or Family C candidate rows exist.
- `module_id`, `family`, `research_status`, and `timing_policy` contain only approved values.
- Metadata JSON confirms no IC, discovery, validation, governance, production, threshold, or ML action occurred.

Recommended test additions before implementation approval:

- Formula drift tests for `vov_01`, `vov_02`, `vov_03`, and `vov_05`.
- Long-form schema test.
- Duplicate-key rejection test.
- Metadata and manifest schema tests.
- After-close timing metadata test.
- Activation-neutralization test distinguishing inactive zeroing from missing-data propagation.

## SECTION 14 - Stop Conditions Before Panel Generation

The future panel-generation task must stop before writing any canonical panel if any condition below is true:

- Candidate registry is not exactly the five approved VoV candidates.
- Any `dpath_*` or `ecluster_*` candidate appears.
- Required input schema is missing any OHLCV field.
- Candidate formulas cannot be matched to `source_spec_id`.
- Activation-neutralization metadata is absent.
- Timing policy metadata is absent or not equal to `after_close_t_forward_returns_after_t`.
- Duplicate keys appear before write.
- Fewer than 50 finite candidate values are available for all dates for any candidate.
- Missing-data reason codes fall outside the approved vocabulary.
- The artifact root would overwrite a non-draft research artifact without explicit approval.
- The writer attempts to compute IC, discovery summaries, redundancy metrics, validation outputs, governance changes, production registry changes, threshold changes, or ML outputs.

## SECTION 15 - Explicit Non-Goals

This specification does not:

- implement panel generation;
- create artifact directories;
- write panel files;
- compute IC;
- run discovery;
- run redundancy screening;
- run refinement;
- run validation;
- modify governance;
- modify production registry;
- change thresholds;
- introduce ML;
- implement Family B;
- implement Family C;
- access external data;
- change the OHLCV universe.

## SECTION 16 - Verification Summary

Verification requirements for this specification:

- Required sections exist.
- `PANEL_SPEC_READY_FOR_IMPLEMENTATION` appears in the note.
- No implementation files are changed by this task.
- No research artifacts are created or modified by this task.
- No panel generation, IC, discovery, refinement, validation, governance, production, threshold, or ML work is performed.

Final classification:

- `PANEL_SPEC_READY_FOR_IMPLEMENTATION`
