# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Formula Implementation v1

## SECTION 1 - Executive Summary

The OHLCV Non-Hostile Transition and Leadership Rotation candidate formulas were implemented exactly as executable, in-memory transformations derived from `ohlcv_non_hostile_transition_and_leadership_rotation_candidate_formula_and_panel_specification_v1.md`.

This was a formula implementation task only. No candidate panels were generated. No discovery was executed. No IC scoring, redundancy screening, refinement, validation, governance mutation, threshold change, production registration, or ML work was performed.

Final classification: `IMPLEMENTATION_READY_FOR_PANEL_GENERATION_REVIEW`.

Implemented candidates:

- `nhlr_01`
- `nhlr_02`
- `nhlr_03`
- `nhlr_04`
- `nhlr_05`
- `nhlr_07`
- `nhlr_08`
- `nhlr_09`
- `nhlr_10`

Excluded candidate:

- `nhlr_06`

## SECTION 2 - Files Created or Modified

Modified:

- `pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py`

Created:

- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation.py`
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation_v1.md`

No panel artifacts were created.

## SECTION 3 - Implemented Formula Surface

Implemented formula helpers:

- `formula_manifest_rows()`
- `validate_formula_manifest_rows()`
- `build_ohlcv_formula_features()`
- `build_candidate_formula_outputs()`

Implemented constants:

- `FORMULA_SPECS`
- `FORMULA_VERSION = v1`
- `WARMUP_WINDOW = 120`
- `MIN_CROSS_SECTIONAL_COUNT = 30`
- `REQUIRED_OHLCV_COLUMNS`
- `REQUIRED_PANEL_COLUMNS`

Candidate formula outputs are returned in memory as long-form records with the specified panel schema. The implementation does not write parquet files or metadata JSON files.

## SECTION 4 - Implemented Formulas

| candidate_id | formula_name | primary_horizon | panel_role |
| --- | --- | --- | --- |
| `nhlr_01` | `neutral_base_emergence_score` | `h20` | core early-emergence candidate |
| `nhlr_02` | `quiet_accumulation_before_leadership_score` | `h20` | core accumulation candidate |
| `nhlr_03` | `post_transition_leadership_durability_score` | `h20` | durability support candidate |
| `nhlr_04` | `smooth_trend_handoff_score` | `h20` | core trend-handoff candidate |
| `nhlr_05` | `broadening_participation_without_stress_score` | `h20` | breadth/participation support candidate |
| `nhlr_07` | `rotation_acceleration_leader_score` | `h10` | rotation acceleration candidate |
| `nhlr_08` | `mature_leadership_deceleration_avoidance_score` | `h20` | lower-priority deceleration-avoidance candidate |
| `nhlr_09` | `volume_confirmed_leadership_shift_score` | `h10` | core confirmation candidate |
| `nhlr_10` | `healthy_breadth_contributor_score` | `h20` | core breadth-contribution candidate |

All formulas preserve the registry-derived metadata architecture. Candidate identity and metadata remain sourced from the authoritative registry and registry-derived implementation layer.

## SECTION 5 - Implementation Assumptions

- Raw OHLCV input is a long-form DataFrame with `date`, `ticker`, `open`, `high`, `low`, `close`, and `volume`.
- If `adjusted_close` is present, it is used consistently as the price source for formula construction.
- If `dollar_volume` is absent, it is computed as `close * volume`.
- Rolling features are trailing by ticker and use no future values.
- Cross-sectional ranks and z-scores are grouped by signal date.
- Cross-sectional calculations require at least 30 eligible tickers.
- Warmup requires 120 ticker-level observations.
- Rows with invalid OHLCV values produce null signals and diagnostic missing-data reasons.

## SECTION 6 - Supported Features

Implemented feature groups:

- trailing returns and log returns;
- trailing moving averages;
- rolling volatility and range controls;
- dollar-volume participation z-scores;
- cross-sectional relative strength ranks;
- trend ranks;
- leadership score and leadership deltas;
- rank velocity and rank acceleration;
- moving-average breadth states;
- breadth contribution;
- non-hostile market state gating.

Implemented output diagnostics:

- `component_coverage_count`
- `warmup_complete`
- `non_hostile_market_state`
- `source_close_column`
- `missing_data_reason`

## SECTION 7 - Remaining Work Before Panel Generation

Panel generation still requires a separate review and implementation task.

Remaining items:

- add a panel-generation runner mode only after review approval;
- write one parquet panel per candidate under the approved research artifact namespace;
- write per-candidate metadata JSON files;
- write panel manifest and panel-generation summary artifacts;
- add no-rewrite dry-run checks for generated panels;
- preserve all no-discovery, no-IC, no-redundancy, no-validation, no-governance, no-production, no-threshold, and no-ML guardrails.

## SECTION 8 - Non-Goals

This task did not:

- generate candidate panels;
- execute discovery;
- calculate IC;
- run redundancy screening;
- run refinement;
- run validation;
- modify governance;
- change thresholds;
- register production candidates;
- implement ML;
- promote or demote candidates;
- reopen CRSP/PIT work;
- change candidate identities;
- add or remove candidate concepts.

## SECTION 9 - Verification Summary

Commands executed:

- `python -m py_compile pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py` - passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation.py` - 6 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py` - 6 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py` - 16 passed
- `pytest` - 76 passed

Final classification: `IMPLEMENTATION_READY_FOR_PANEL_GENERATION_REVIEW`.
