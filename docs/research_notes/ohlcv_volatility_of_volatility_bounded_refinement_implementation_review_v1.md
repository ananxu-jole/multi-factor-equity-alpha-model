# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Implementation Review v1

## SECTION 1 - Review Objective

This note reviews the bounded OHLCV Volatility-of-Volatility refinement implementation before any panel specification, panel generation, IC, refinement execution, or validation.

Current input classification:

- `REFINEMENT_IMPLEMENTATION_READY_FOR_REVIEW`

Review classification:

- `REFINEMENT_IMPLEMENTATION_READY_FOR_PANEL_SPEC`

This review did not generate panels, compute IC, execute refinement, perform validation, modify original formulas, modify original panels, modify governance decisions, modify production registry, change thresholds, or introduce ML.

## SECTION 2 - Files Reviewed

Reviewed files:

- `pipelines/ohlcv_volatility_of_volatility_refinement_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_v1.py`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_implementation_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md`
- `pipelines/ohlcv_volatility_of_volatility_research_module_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`

## SECTION 3 - Readiness Conclusion

The bounded VoV refinement implementation is ready for a dedicated refinement panel specification task.

No blocking implementation defects were found. The module implements exactly the eight frozen variants from the specification, preserves the two approved parent families only, blocks watch/park candidates and frozen Family B/C candidates, keeps the original VoV module unchanged, and exposes an auditable long-form in-memory panel contract for future panel writing.

Panel specification may begin after this review.

## SECTION 4 - Variant Coverage Findings

Implemented variants:

| refinement_id | parent candidate | review finding |
| --- | --- | --- |
| `vov_01_ref_anchor` | `vov_01` | Present and aligned with frozen anchor role. |
| `vov_01_ref_strict_calm` | `vov_01` | Present and limited to stricter prior-instability activation. |
| `vov_01_ref_longer_memory` | `vov_01` | Present and limited to longer-memory VoV/range-chop features. |
| `vov_01_ref_smoothed_calm` | `vov_01` | Present and limited to 3-day smoothing of the calm component. |
| `vov_03_ref_anchor` | `vov_03` | Present and aligned with frozen anchor role. |
| `vov_03_ref_strict_chop` | `vov_03` | Present and limited to stricter prior-chop activation. |
| `vov_03_ref_longer_chop` | `vov_03` | Present and limited to longer-memory range-chop features. |
| `vov_03_ref_extension_controlled` | `vov_03` | Present and limited to the specified extension-control addition. |

Coverage conclusion:

- Exactly eight refinement variants are implemented.
- Only `vov_01` and `vov_03` refinement families are included.
- `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*` remain blocked.

## SECTION 5 - Formula And Spec Consistency Findings

The implementation matches the frozen formula specification.

Formula consistency review:

- `vov_01_ref_anchor` uses the original `vov_01` components and median prior-VoV activation.
- `vov_01_ref_strict_calm` reuses the original `vov_01` raw formula and changes only activation to the predeclared upper-tercile threshold.
- `vov_01_ref_longer_memory` uses `vov_10_40`, `vov_slope_10`, `lag(...,10)`, `range_chop_40`, and `low_extension_20` as specified.
- `vov_01_ref_smoothed_calm` uses `vov_slope_5_smooth_3` as the only smoothing change.
- `vov_03_ref_anchor` uses the original `vov_03` components and median prior-chop activation.
- `vov_03_ref_strict_chop` reuses the original `vov_03` raw formula and changes only activation to the predeclared upper-tercile threshold.
- `vov_03_ref_longer_chop` uses `range_chop_40`, `range_chop_slope_10`, `lag(...,10)`, `abs_ret_10`, and `low_extension_20` as specified.
- `vov_03_ref_extension_controlled` adds the specified `rank_cs(1 - rank_cs(abs_ret_10))` extension-control term.

No extra rank-churn, event-cluster, dispersion, sector, peer, metadata, or target-derived features were added.

## SECTION 6 - Anchor Equivalence Findings

Anchor equivalence is covered by focused tests.

Findings:

- `vov_01_ref_anchor` is formula-equivalent to original `vov_01` for exposed signal and post-activation raw score behavior.
- `vov_03_ref_anchor` is formula-equivalent to original `vov_03` for exposed signal and post-activation raw score behavior.
- Original VoV candidate IDs remain unchanged as `vov_01`, `vov_02`, `vov_03`, `vov_04`, and `vov_05`.
- The original VoV implementation file was not modified by this review.

## SECTION 7 - Schema, Timing, And Missing-Data Findings

Schema:

- The implementation exposes the frozen long-form columns: `date`, `ticker`, `candidate_id`, `source_spec_id`, `parent_candidate_id`, `module_id`, `family`, `research_status`, `primary_horizon`, `secondary_horizons`, `signal_value`, `raw_score`, `pre_activation_raw_score`, `is_active`, `feature_warmup_complete`, `finite_cross_section_count`, `rank_min_count`, `missing_reason`, `timing_policy`, and `created_by_spec`.
- Canonical key shape is compatible with `date`, `ticker`, `candidate_id`.
- Focused tests check duplicate-key prevention in the long-form in-memory panel.

Timing:

- Timing metadata is fixed as `after_close_t_forward_returns_after_t`.
- The implementation does not compute forward returns and therefore does not introduce IC alignment risk.

Warmup and missing data:

- Rolling features use fixed minimum periods equal to their window length.
- Missing rolling features remain missing.
- Missing pre-activation scores are not neutralized to zero.
- Inactive finite observations are neutralized to `raw_score = 0.0` before final ranking.
- Dates with insufficient finite cross-section leave `signal_value` missing and record `insufficient_cross_section`.

## SECTION 8 - Test Coverage Assessment

The focused tests are sufficient for implementation review.

Covered:

- Exact eight-variant registry membership.
- Parent-candidate restriction to `vov_01` and `vov_03`.
- Blocked candidate rejection for `vov_05` and Family B/C prefixes.
- Long-form schema compatibility.
- Candidate ID order preservation.
- Duplicate key checks.
- Anchor equivalence to original `vov_01` and `vov_03` outputs.
- Warmup and inactive-neutralization semantics.
- Guardrail manifest checks.
- Original VoV module candidate list preservation.
- Input schema enforcement.

Residual test gap:

- Tests do not yet validate future artifact serialization because panel writing is not authorized in this phase. That should be covered in the future panel specification and panel generation tasks.

## SECTION 9 - Blocking Issues

No blocking issues were found.

## SECTION 10 - Minor Review Items

Minor non-blocking items:

- Future panel specification should decide whether to retain warmup rows with explicit missing reasons, matching the prior VoV panel convention.
- Future panel specification should require a manifest-level hash or exact formula string for each frozen refinement formula.
- Future panel audit should re-check anchor equivalence after artifact writing, not only in-memory output.

These items do not block panel specification.

## SECTION 11 - Recommended Next Step

Recommended next task:

**Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Panel Specification v1**

The next task should freeze:

- panel artifact root;
- per-variant parquet names;
- metadata JSON schema;
- panel manifest schema;
- formula manifest schema;
- schema validation rules;
- duplicate-key rules;
- warmup and missing-data policy;
- activation-neutralization policy;
- timing policy;
- blocked-candidate enforcement.

## SECTION 12 - Verification Summary

Commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/ohlcv_volatility_of_volatility_refinement_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_rank_coherence_discovery_scaffold.py tests/test_registry_validation.py -q` | passed, 8 tests |

Guardrail confirmation:

- No panels were generated.
- No IC was computed.
- No refinement was executed.
- No validation was performed.
- No original formulas were modified.
- No original panels were modified.
- No governance decisions were modified.
- No production registry changes were made.
- No thresholds were changed.
- No ML was introduced.

Final classification:

- `REFINEMENT_IMPLEMENTATION_READY_FOR_PANEL_SPEC`
