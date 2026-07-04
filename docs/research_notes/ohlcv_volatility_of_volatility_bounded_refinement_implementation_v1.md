# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Implementation v1

## SECTION 1 - Executive Summary

This note documents implementation of the frozen OHLCV Volatility-of-Volatility bounded refinement variants from:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md`

Classification:

- `REFINEMENT_IMPLEMENTATION_READY_FOR_REVIEW`

Implemented module:

- `pipelines/ohlcv_volatility_of_volatility_refinement_v1.py`

Focused tests:

- `tests/test_ohlcv_volatility_of_volatility_refinement_v1.py`

This implementation did not generate panels, compute IC, execute refinement, run validation, modify original VoV formulas, modify original VoV panels, mutate governance, change production registry state, change thresholds, or introduce ML.

## SECTION 2 - Implemented Refinement Variants

Exactly eight frozen refinement variants were implemented.

| refinement_id | parent candidate | role | primary horizon | status |
| --- | --- | --- | --- | --- |
| `vov_01_ref_anchor` | `vov_01` | Original anchor preservation. | h20 | Implemented. |
| `vov_01_ref_strict_calm` | `vov_01` | Stricter prior-instability activation. | h20 | Implemented. |
| `vov_01_ref_longer_memory` | `vov_01` | Longer-memory VoV calm. | h20 | Implemented. |
| `vov_01_ref_smoothed_calm` | `vov_01` | Smoothed calm component. | h20 | Implemented. |
| `vov_03_ref_anchor` | `vov_03` | Original anchor preservation. | h10 | Implemented. |
| `vov_03_ref_strict_chop` | `vov_03` | Stricter prior-chop activation. | h10 | Implemented. |
| `vov_03_ref_longer_chop` | `vov_03` | Longer-memory range-chop exhaustion. | h10 | Implemented. |
| `vov_03_ref_extension_controlled` | `vov_03` | Stronger extension/reversal control. | h10 | Implemented. |

Blocked candidates remain excluded:

- `vov_05`
- `vov_02`
- `vov_04`
- `dpath_*`
- `ecluster_*`

## SECTION 3 - Formula Summary

The implementation follows the frozen specification exactly:

- `vov_01_ref_anchor`: original `vov_01` formula with median prior-VoV activation.
- `vov_01_ref_strict_calm`: original `vov_01` formula with upper-tercile prior-VoV activation.
- `vov_01_ref_longer_memory`: longer-memory `vov_10_40`, `vov_slope_10`, and `range_chop_40` variant.
- `vov_01_ref_smoothed_calm`: original `vov_01` structure with 3-day smoothing of `vov_slope_5`.
- `vov_03_ref_anchor`: original `vov_03` formula with median prior-chop activation.
- `vov_03_ref_strict_chop`: original `vov_03` formula with upper-tercile prior-chop activation.
- `vov_03_ref_longer_chop`: longer-memory `range_chop_40` and `range_chop_slope_10` variant.
- `vov_03_ref_extension_controlled`: original `vov_03` structure with added `abs_ret_10` extension control.

Final output uses canonical long-form rows with `signal_value`, `raw_score`, `pre_activation_raw_score`, `is_active`, lineage metadata, timing policy, and missing-reason fields.

## SECTION 4 - Implementation Assumptions

Assumptions:

- Input data use existing project-standard OHLCV columns: `date`, `ticker`, `open`, `high`, `low`, `close`, `volume`.
- Signals use data available through the close of signal date `t`.
- Future returns are not computed in this module.
- Cross-sectional ranks require a configurable finite-count minimum, defaulting to 50 names per date.
- Missing rolling features remain missing and are not backfilled.
- Inactive finite observations are neutralized to `raw_score = 0.0` before final ranking.
- The original VoV module remains unchanged and is used only for regression comparison of anchor behavior.

## SECTION 5 - Supported Rolling Features

Implemented derived features:

- `ret_1`, `ret_10`, `ret_20`
- `abs_ret_10`, `abs_ret_20`
- `range_1`
- `vol_5`, `vol_10`
- `vov_5_20`, `vov_10_40`
- `vov_slope_5`, `vov_slope_10`, `vov_slope_5_smooth_3`
- `range_chop_20`, `range_chop_40`
- `range_chop_slope_5`, `range_chop_slope_10`
- `low_extension_20`

No rank-churn, event-cluster, dispersion, sector, peer, metadata, or target-derived features were implemented.

## SECTION 6 - Registry And Schema Checks

Registry checks enforce:

- exactly eight refinement variants;
- candidate IDs must match the frozen specification order;
- parent candidates must be only `vov_01` and `vov_03`;
- all candidates must use `family = volatility_of_volatility`;
- all candidates must use `research_status = RESEARCH_ONLY`;
- `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*` are blocked.

Long-form panel compatibility includes:

- `date`
- `ticker`
- `candidate_id`
- `source_spec_id`
- `parent_candidate_id`
- `module_id`
- `family`
- `research_status`
- `primary_horizon`
- `secondary_horizons`
- `signal_value`
- `raw_score`
- `pre_activation_raw_score`
- `is_active`
- `feature_warmup_complete`
- `finite_cross_section_count`
- `rank_min_count`
- `missing_reason`
- `timing_policy`
- `created_by_spec`

## SECTION 7 - Tests Added

Focused tests cover:

- exact registry membership for the eight frozen variants;
- rejection of blocked VoV and Family B/C candidates;
- long-form panel schema compatibility;
- duplicate-key prevention through canonical `date`, `ticker`, `candidate_id` shape;
- anchor variant equivalence to original `vov_01` and `vov_03` module outputs;
- warmup and inactive-neutralization semantics;
- guardrail manifest flags;
- input schema enforcement.

## SECTION 8 - Verification Summary

Commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/ohlcv_volatility_of_volatility_refinement_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_rank_coherence_discovery_scaffold.py tests/test_registry_validation.py -q` | passed, 8 tests |

Verification confirmations:

- Exactly eight refinement variants were implemented.
- Original VoV implementation remained unchanged.
- Blocked candidates remained excluded.
- No panel generation was performed.
- No IC was computed.
- No refinement execution was performed.
- No validation was performed.
- No governance changes were made.
- No production changes were made.
- No threshold changes were made.
- No ML was introduced.

## SECTION 9 - Remaining Work

Before refinement review:

- Perform an implementation review of `pipelines/ohlcv_volatility_of_volatility_refinement_v1.py`.
- Confirm the long-form schema and metadata fields before any panel-generation task.
- Confirm anchor equivalence remains acceptable after review.

Before any refinement execution:

- Complete refinement implementation review.
- Create or approve a dedicated panel-generation specification.
- Generate panels only in a separately authorized panel-generation task.
- Audit panels before any IC/refinement scoring.

## SECTION 10 - Explicit Non-Goals

This implementation did not:

- generate panels;
- compute IC;
- execute refinement;
- modify original VoV formulas;
- modify original VoV panels;
- modify governance decisions;
- modify production registry;
- implement blocked candidates;
- introduce ML;
- access external data;
- use PIT metadata.
