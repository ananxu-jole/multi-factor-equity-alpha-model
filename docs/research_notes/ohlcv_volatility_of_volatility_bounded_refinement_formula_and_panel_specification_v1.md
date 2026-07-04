# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Formula and Panel Specification v1

## SECTION 1 - Specification Objective

This note freezes the exact formula and panel specification for the approved OHLCV Volatility-of-Volatility bounded refinement.

Current input classification:

- `REFINEMENT_DESIGN_READY_FOR_SPECIFICATION`

Specification classification:

- `REFINEMENT_SPEC_READY_FOR_IMPLEMENTATION`

This is a specification-only artifact. It does not implement formulas, generate panels, compute IC, run refinement, modify original candidates, modify governance decisions, modify production registry, change thresholds, or introduce ML.

Refinement scope:

- Include only the `vov_01` refinement family.
- Include only the `vov_03` refinement family.
- Specify exactly 8 variants.
- Preserve anchor variants for both approved parents.

## SECTION 2 - Inputs Reviewed

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_design_v1.md`
- `docs/research_notes/ohlcv_vov_dpd_event_clustering_formula_and_panel_specification_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_implementation_v1.md`

Governance context:

- Governance standard: `PROJECT_STANDARD_APPROVED`.
- VoV module state: `MODULE_STATE_SYNCHRONIZED`.
- Approved refinement targets: `vov_01` and `vov_03`.
- Blocked candidates: `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*`.

## SECTION 3 - Formula Notation

All formulas are OHLCV-only and use information available through signal date `t`.

Operators:

- `lag(x,n)`: value of `x` n trading days before `t`.
- `ts_mean(x,n)`: trailing n-day mean through `t`.
- `ts_std(x,n)`: trailing n-day standard deviation through `t`.
- `delta(x,n)`: `x - lag(x,n)`.
- `rank_cs(x)`: cross-sectional percentile rank by date, scaled 0 to 1.
- `safe_div(a,b)`: `a / b` when `b` is finite and nonzero, otherwise missing.
- `neutral_if_inactive(score, active)`: `score` if active, otherwise 0 before final cross-sectional ranking.
- `date_quantile(x,q)`: same-date cross-sectional quantile threshold for feature `x`.

Ranking convention:

- Higher score should predict higher forward return.
- Each variant computes `pre_activation_raw_score`.
- If a variant has an activation condition, inactive finite observations are neutralized to `raw_score = 0.0`.
- Final `signal_value` is `rank_cs(raw_score)` using the same-date finite cross-section.

## SECTION 4 - Required Raw Input Schema

Required raw OHLCV input columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Trading date. |
| `ticker` | string | yes | Current research ticker identifier from the existing OHLCV universe. |
| `open` | float | yes | Existing project-standard open. |
| `high` | float | yes | Existing project-standard high. |
| `low` | float | yes | Existing project-standard low. |
| `close` | float | yes | Existing project-standard close. |
| `volume` | float | yes | Existing project-standard volume. |

Universe and timing rules:

- Use the same currently available OHLCV research universe as the original VoV module.
- Do not add external licensed metadata, PIT metadata, sector/industry fields, peer labels, fundamentals, options, macro, or alternative data.
- Signal at date `t` may use OHLCV data through the close of `t`.
- Future returns for IC must start strictly after `t`.
- Timing policy must be `after_close_t_forward_returns_after_t`.

## SECTION 5 - Allowed Derived Features

Only the following derived features are allowed for this refinement specification:

| feature | definition |
| --- | --- |
| `ret_1` | `close / lag(close,1) - 1` |
| `ret_10` | `close / lag(close,10) - 1` |
| `ret_20` | `close / lag(close,20) - 1` |
| `abs_ret_10` | `abs(ret_10)` |
| `abs_ret_20` | `abs(ret_20)` |
| `range_1` | `safe_div(high - low, close)` |
| `vol_5` | `ts_std(ret_1,5)` |
| `vol_10` | `ts_std(ret_1,10)` |
| `vov_5_20` | `ts_std(vol_5,20)` |
| `vov_10_40` | `ts_std(vol_10,40)` |
| `vov_slope_5` | `delta(vov_5_20,5)` |
| `vov_slope_10` | `delta(vov_10_40,10)` |
| `vov_slope_5_smooth_3` | `ts_mean(vov_slope_5,3)` |
| `range_chop_20` | `ts_std(range_1,20)` |
| `range_chop_40` | `ts_std(range_1,40)` |
| `range_chop_slope_5` | `delta(range_chop_20,5)` |
| `range_chop_slope_10` | `delta(range_chop_40,10)` |
| `low_extension_20` | `1 - rank_cs(abs_ret_20)` |

No rank-churn, event-cluster, dispersion, sector, peer, metadata, or target-derived features are allowed in this refinement specification.

## SECTION 6 - Frozen Variant Registry

Exactly 8 variants are specified.

| refinement_id | parent_candidate | source_spec_id | refinement purpose | expected sign | primary horizon | secondary horizons |
| --- | --- | --- | --- | --- | --- | --- |
| `vov_01_ref_anchor` | `vov_01` | `vov_01_instability_calm_after_chop__ref_anchor` | Preserve original anchor. | positive | h20 | h10, h5 |
| `vov_01_ref_strict_calm` | `vov_01` | `vov_01_instability_calm_after_chop__ref_strict_calm` | Test stricter prior instability activation. | positive | h20 | h10 |
| `vov_01_ref_longer_memory` | `vov_01` | `vov_01_instability_calm_after_chop__ref_longer_memory` | Test longer-memory VoV calm. | positive | h20 | h10 |
| `vov_01_ref_smoothed_calm` | `vov_01` | `vov_01_instability_calm_after_chop__ref_smoothed_calm` | Test slope-noise reduction. | positive | h20 | h10, h5 |
| `vov_03_ref_anchor` | `vov_03` | `vov_03_range_chop_exhaustion__ref_anchor` | Preserve original anchor. | positive | h10 | h20, h5 |
| `vov_03_ref_strict_chop` | `vov_03` | `vov_03_range_chop_exhaustion__ref_strict_chop` | Test stricter prior chop activation. | positive | h10 | h20 |
| `vov_03_ref_longer_chop` | `vov_03` | `vov_03_range_chop_exhaustion__ref_longer_chop` | Test longer-memory chop exhaustion. | positive | h10 | h20, h5 |
| `vov_03_ref_extension_controlled` | `vov_03` | `vov_03_range_chop_exhaustion__ref_extension_controlled` | Strengthen extension/reversal contamination control. | positive | h10 | h20 |

## SECTION 7 - Exact Formula Table

For each formula:

- `pre_activation_raw_score` is the multiplicative component score before activation neutralization.
- `is_active` is the frozen activation condition.
- `raw_score = neutral_if_inactive(pre_activation_raw_score, is_active)`.
- `signal_value = rank_cs(raw_score)`.

| refinement_id | hypothesis | parameter values | exact pre-activation formula | activation condition |
| --- | --- | --- | --- | --- |
| `vov_01_ref_anchor` | Original elevated VoV and chop calming should predict h20 forward strength. | `vov_window=5/20`, `slope_window=5`, `lag=5`, `extension=20`, `activation=median`. | `rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) * rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)` | `lag(vov_5_20,5) > date_quantile(lag(vov_5_20,5),0.50) and vov_slope_5 < 0` |
| `vov_01_ref_strict_calm` | Stronger prior instability should improve signal cleanliness if the calm-after-chop thesis is real. | `vov_window=5/20`, `slope_window=5`, `lag=5`, `extension=20`, `activation=upper_tercile`. | `rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) * rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)` | `lag(vov_5_20,5) > date_quantile(lag(vov_5_20,5),0.667) and vov_slope_5 < 0` |
| `vov_01_ref_longer_memory` | Longer-memory VoV calming should preserve h20 behavior if the edge is not short-window noise. | `vov_window=10/40`, `slope_window=10`, `lag=10`, `extension=20`, `activation=median`. | `rank_cs(lag(vov_10_40,10)) * rank_cs(-vov_slope_10) * rank_cs(lag(range_chop_40,10)) * rank_cs(low_extension_20)` | `lag(vov_10_40,10) > date_quantile(lag(vov_10_40,10),0.50) and vov_slope_10 < 0` |
| `vov_01_ref_smoothed_calm` | Light smoothing of the VoV calm component should reduce single-day slope noise without changing the mechanism. | `vov_window=5/20`, `slope_window=5`, `lag=5`, `smooth=3`, `extension=20`, `activation=median`. | `rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5_smooth_3) * rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20)` | `lag(vov_5_20,5) > date_quantile(lag(vov_5_20,5),0.50) and vov_slope_5_smooth_3 < 0` |
| `vov_03_ref_anchor` | Original elevated range chop that begins compressing should predict h10 forward strength. | `chop_window=20`, `slope_window=5`, `lag=5`, `extension=ret10_and_ret20`, `activation=median`. | `rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) * rank_cs(-abs_ret_10) * rank_cs(low_extension_20)` | `lag(range_chop_20,5) > date_quantile(lag(range_chop_20,5),0.50) and range_chop_slope_5 < 0` |
| `vov_03_ref_strict_chop` | Stronger prior chop should improve h10 signal cleanliness if the range-exhaustion thesis is real. | `chop_window=20`, `slope_window=5`, `lag=5`, `extension=ret10_and_ret20`, `activation=upper_tercile`. | `rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) * rank_cs(-abs_ret_10) * rank_cs(low_extension_20)` | `lag(range_chop_20,5) > date_quantile(lag(range_chop_20,5),0.667) and range_chop_slope_5 < 0` |
| `vov_03_ref_longer_chop` | Longer-memory chop compression should preserve the exhaustion mechanism if h10 evidence is not a short-window artifact. | `chop_window=40`, `slope_window=10`, `lag=10`, `extension=ret10_and_ret20`, `activation=median`. | `rank_cs(lag(range_chop_40,10)) * rank_cs(-range_chop_slope_10) * rank_cs(-abs_ret_10) * rank_cs(low_extension_20)` | `lag(range_chop_40,10) > date_quantile(lag(range_chop_40,10),0.50) and range_chop_slope_10 < 0` |
| `vov_03_ref_extension_controlled` | Stronger extension control should preserve range-chop exhaustion while reducing plain-reversal contamination. | `chop_window=20`, `slope_window=5`, `lag=5`, `extension=ret10_and_ret20_double_control`, `activation=median`. | `rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) * rank_cs(-abs_ret_10) * rank_cs(low_extension_20) * rank_cs(1 - rank_cs(abs_ret_10))` | `lag(range_chop_20,5) > date_quantile(lag(range_chop_20,5),0.50) and range_chop_slope_5 < 0` |

## SECTION 8 - Contamination Checks And Stop Conditions

Required contamination checks for every variant:

- volatility compression / stress stabilization;
- hostile/stress repair;
- persistence / rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- watch-only `vov_05`.

Branch-specific checks:

| branch | additional contamination focus |
| --- | --- |
| `vov_01` | Must not become a simple volatility compression or post-stress stabilization proxy. |
| `vov_03` | Must not become a plain reversal, stress-repair, or panic/liquidity-stress proxy. |

Stop conditions:

| scope | condition |
| --- | --- |
| `vov_01` branch | Stop if anchor h20 evidence is not positive in the refinement run. |
| `vov_01` branch | Stop if all variants weaken h20 evidence versus anchor and do not reduce contamination. |
| `vov_03` branch | Stop if anchor h10 evidence is not positive in the refinement run. |
| `vov_03` branch | Stop if all variants weaken h10 evidence versus anchor and do not reduce contamination. |
| family | Stop if both branches become h1/h5-only. |
| family | Stop if any excluded candidate or family appears in the refinement universe. |
| family | Stop if refined variants become indistinguishable from contamination references. |

## SECTION 9 - Panel Schema

Panel format:

- Canonical long-form panel.
- One parquet panel per refinement variant in future implementation.
- One row per `date`, `ticker`, `candidate_id`.

Required columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Signal date. |
| `ticker` | string | yes | Research ticker. |
| `candidate_id` | string | yes | One of the 8 frozen refinement IDs. |
| `source_spec_id` | string | yes | Frozen source lineage ID from Section 6. |
| `parent_candidate_id` | string | yes | `vov_01` or `vov_03`. |
| `module_id` | string | yes | `ohlcv_volatility_of_volatility_refinement_v1`. |
| `family` | string | yes | `volatility_of_volatility`. |
| `research_status` | string | yes | `RESEARCH_ONLY`. |
| `primary_horizon` | string | yes | Frozen primary horizon. |
| `secondary_horizons` | string | yes | Comma-separated frozen secondary horizons. |
| `signal_value` | float | yes | Final ranked signal value. |
| `raw_score` | float | yes | Score after activation neutralization. |
| `pre_activation_raw_score` | float | yes | Score before activation neutralization. |
| `is_active` | bool | yes | Frozen activation flag. |
| `feature_warmup_complete` | bool | yes | True only when all required rolling features are available. |
| `finite_cross_section_count` | integer | yes | Same-date finite count used for ranking. |
| `rank_min_count` | integer | yes | Minimum cross-section count, fixed at 50 unless later implementation standard requires stricter. |
| `missing_reason` | string | yes | Null or reason code. |
| `timing_policy` | string | yes | `after_close_t_forward_returns_after_t`. |
| `created_by_spec` | string | yes | `ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1`. |

Canonical key:

- `date`, `ticker`, `candidate_id`.

Duplicate keys are not allowed.

## SECTION 10 - Warmup, Missing Data, Ranking, And Alignment

Warmup:

- Minimum warmup is the maximum required lookback for each formula plus its lag and slope window.
- For `vov_01_ref_longer_memory` and `vov_03_ref_longer_chop`, warmup must cover 40-day measurement, 10-day slope, and 10-day lag requirements.
- Warmup rows may be retained for auditability, but `signal_value`, `raw_score`, and `pre_activation_raw_score` must be missing when required features are incomplete.

Missing data:

- Missing OHLCV inputs make all dependent features missing.
- Infinite values must be treated as missing.
- Missing pre-activation scores must remain missing and must not be neutralized to zero.
- Inactive finite observations are neutralized to `raw_score = 0.0` before final ranking.

Ranking:

- Cross-sectional ranks are computed within date.
- A date must have at least 50 finite candidate values to produce final ranks.
- Dates below the finite-count threshold must set `signal_value` missing and record `missing_reason`.

Alignment:

- Signal date `t` may use OHLCV data through the close of `t`.
- IC forward returns must start strictly after `t`.
- No intraday execution assumption is authorized.

## SECTION 11 - Artifact Naming And Directory Contract

Future artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/`

Future panel root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`

Required future files:

| artifact | required path / naming |
| --- | --- |
| candidate registry | `candidate_registry.csv` |
| formula manifest | `candidate_formula_manifest.csv` |
| derived feature manifest | `derived_feature_manifest.csv` |
| input schema | `input_schema.csv` |
| metadata JSON | `metadata.json` |
| panel manifest | `panel_manifest.csv` |
| generation manifest | `panel_generation_manifest.json` |
| schema validation report | `schema_validation_report.csv` |
| per-variant panel | `{candidate_id}_signal_panel.parquet` |

Required panel files:

- `vov_01_ref_anchor_signal_panel.parquet`
- `vov_01_ref_strict_calm_signal_panel.parquet`
- `vov_01_ref_longer_memory_signal_panel.parquet`
- `vov_01_ref_smoothed_calm_signal_panel.parquet`
- `vov_03_ref_anchor_signal_panel.parquet`
- `vov_03_ref_strict_chop_signal_panel.parquet`
- `vov_03_ref_longer_chop_signal_panel.parquet`
- `vov_03_ref_extension_controlled_signal_panel.parquet`

## SECTION 12 - Metadata JSON Schema

Required metadata fields:

| field | value / rule |
| --- | --- |
| `module_id` | `ohlcv_volatility_of_volatility_refinement_v1` |
| `created_by_spec` | `ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1` |
| `research_status` | `RESEARCH_ONLY` |
| `family` | `volatility_of_volatility` |
| `variant_count` | `8` |
| `candidate_ids` | ordered list of the 8 frozen refinement IDs |
| `parent_candidates` | `vov_01`, `vov_03` |
| `blocked_candidates` | `vov_05`, `vov_02`, `vov_04`, `dpath_*`, `ecluster_*` |
| `timing_policy` | `after_close_t_forward_returns_after_t` |
| `panel_schema_version` | `v1` |
| `formula_spec_classification` | `REFINEMENT_SPEC_READY_FOR_IMPLEMENTATION` |
| `guardrail_flags` | object of fail-closed booleans listed below |

Required guardrail flags:

- `formulas_implemented`: false for this specification note.
- `panels_generated`: false for this specification note.
- `ic_computed`: false for this specification note.
- `refinement_executed`: false for this specification note.
- `validation_executed`: false for this specification note.
- `governance_modified`: false for this specification note.
- `production_registration`: false for this specification note.
- `thresholds_modified`: false for this specification note.
- `ml_integration`: false for this specification note.

## SECTION 13 - Refinement Manifest Schema

Future refinement manifest must include:

| field | rule |
| --- | --- |
| `manifest_version` | `v1` |
| `module_id` | `ohlcv_volatility_of_volatility_refinement_v1` |
| `specification_note` | this note path |
| `source_design_note` | bounded refinement design note path |
| `variant_count` | exactly 8 |
| `candidate_ids` | ordered list of the 8 frozen refinement IDs |
| `parent_candidate_map` | mapping from each refinement ID to `vov_01` or `vov_03` |
| `formula_hashes` | implementation-time hashes of frozen formula strings |
| `artifact_root` | future artifact root |
| `panel_root` | future panel root |
| `timing_policy` | `after_close_t_forward_returns_after_t` |
| `excluded_candidate_check` | must pass for `vov_05`, `vov_02`, `vov_04`, `dpath_*`, `ecluster_*` |
| `schema_validation_status` | future panel validation status |
| `duplicate_key_status` | future duplicate-key status |
| `guardrail_flags` | fail-closed booleans for forbidden actions |

## SECTION 14 - Blocked Candidate Enforcement

The following are blocked from formulas, panels, IC, refinement execution, and candidate registry inclusion:

- `vov_05`
- `vov_02`
- `vov_04`
- `dpath_*`
- `ecluster_*`

`vov_05` may appear only as a future contamination/reference comparator in review artifacts. It must not be implemented as a refinement variant.

Any candidate registry containing a blocked ID must fail validation.

## SECTION 15 - Explicit Non-Goals

This specification does not:

- implement formulas;
- generate panels;
- compute IC;
- run refinement;
- modify original candidates;
- modify original panels;
- modify governance decisions;
- modify production registry;
- change thresholds;
- introduce ML.

## SECTION 16 - Verification Summary

Verification status:

- Exactly 8 variants are specified.
- Anchor variants are preserved: `vov_01_ref_anchor` and `vov_03_ref_anchor`.
- Only `vov_01` and `vov_03` refinement families are included.
- Blocked candidates are explicitly excluded: `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*`.
- No implementation was performed.
- No panels were generated.
- No IC was computed.
- No refinement was executed.
- No governance decision was modified.
- No production registry files were changed.
- No thresholds were changed.
- No ML was introduced.

Final classification:

- `REFINEMENT_SPEC_READY_FOR_IMPLEMENTATION`
