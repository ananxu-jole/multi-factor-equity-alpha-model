# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Formula Implementation Review v1

## SECTION 1 - Executive Summary

This review assessed the OHLCV Non-Hostile Transition and Leadership Rotation formula implementation before enabling any panel-writing runner mode.

Review classification: `FORMULA_IMPLEMENTATION_READY_FOR_PANEL_WRITING`.

The formula implementation is registry-derived, covers all nine approved candidates, preserves `nhlr_06` exclusion, matches the formula and panel specification, returns the expected in-memory long-form output schema, and keeps panel writing, discovery, IC scoring, redundancy screening, refinement, validation, governance changes, production registration, threshold changes, and ML blocked.

One small review fix was applied: invalid OHLCV rows are now excluded from moving-average breadth/universe calculations instead of being treated as below-moving-average observations. This aligns the implementation with the specified universe rule that invalid rows should be excluded from eligible same-date tickers.

No candidate panels were generated.

## SECTION 2 - Files Reviewed

Reviewed implementation files:

- `pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py`
- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation.py`

Reviewed research notes:

- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation_v1.md`
- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_candidate_formula_and_panel_specification_v1.md`

Reviewed artifact state:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/`

Confirmed no `candidate_panels/` directory exists under the OHLCV Non-Hostile Transition and Leadership Rotation research artifact root.

## SECTION 3 - Formula and Specification Consistency

Formula coverage is complete:

- `nhlr_01`: `neutral_base_emergence_score`
- `nhlr_02`: `quiet_accumulation_before_leadership_score`
- `nhlr_03`: `post_transition_leadership_durability_score`
- `nhlr_04`: `smooth_trend_handoff_score`
- `nhlr_05`: `broadening_participation_without_stress_score`
- `nhlr_07`: `rotation_acceleration_leader_score`
- `nhlr_08`: `mature_leadership_deceleration_avoidance_score`
- `nhlr_09`: `volume_confirmed_leadership_shift_score`
- `nhlr_10`: `healthy_breadth_contributor_score`

Specification consistency findings:

- Candidate IDs match the authoritative registry order.
- `nhlr_06` is not present in formula specs, manifests, or outputs.
- Formula names, primary horizons, secondary review horizons, and panel roles match the specification.
- Fixed formula weights are implemented directly; no parameter optimization or threshold tuning was introduced.
- Formula outputs use trailing OHLCV features and same-date cross-sectional ranks/z-scores.
- Registry metadata is joined from registry-derived helpers rather than redeclared in formula output construction.

## SECTION 4 - Schema Consistency

The in-memory formula output schema matches the panel specification:

- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `family`
- `theme`
- `horizon`
- `working_name`
- `economic_mechanism`
- `implementation_priority`
- `panel_role`
- `formula_name`
- `formula_version`
- `dependency_class`
- `required_input_family`
- `component_coverage_count`
- `warmup_complete`
- `non_hostile_market_state`
- `source_close_column`
- `missing_data_reason`

Schema findings:

- Required long-form fields are present.
- Registry-derived metadata fields are present.
- Diagnostic fields are present.
- `dependency_class` remains `OHLCV_ONLY`.
- `required_input_family` remains `OHLCV_DERIVED_ONLY`.
- Output construction is in memory only and does not write panel parquet or metadata JSON files.

## SECTION 5 - Warmup, Missing-Data, Date-Alignment, and Universe Findings

Warmup:

- `WARMUP_WINDOW = 120` is implemented.
- Early rows are assigned null `signal_value`.
- Early rows report `missing_data_reason = warmup_incomplete`.

Missing data:

- Invalid OHLCV rows produce null signals.
- Invalid OHLCV rows report `missing_data_reason = invalid_or_missing_ohlcv`.
- Formula component coverage is tracked and fewer than three components produces null output.
- No future fills or cross-ticker fills are used.

Date alignment:

- Rolling features are trailing by ticker.
- Rank velocity and acceleration use lagged values.
- Cross-sectional ranks and z-scores are grouped by signal date.
- No forward returns or target variables are introduced.

Universe handling:

- Cross-sectional ranks and z-scores require at least 30 non-null same-date observations.
- Universe breadth is computed from eligible same-date rows.
- Review fix applied: invalid OHLCV rows are excluded from `above_ma_50`, `above_ma_100`, and therefore same-date breadth calculations.

## SECTION 6 - Test Coverage Assessment

The focused formula tests are meaningful for the current implementation layer. They cover:

- formula manifest registry alignment;
- `nhlr_06` exclusion;
- formula metadata drift detection;
- expected output columns;
- warmup behavior;
- invalid OHLCV NaN handling;
- invalid-row exclusion from breadth eligibility;
- exact weighted-sum consistency for `nhlr_07`;
- trailing date alignment for rank velocity and acceleration.

Remaining test coverage should be added in the future panel-writing task:

- parquet file creation;
- per-candidate metadata JSON creation;
- panel manifest creation;
- dry-run no-rewrite behavior;
- no governance/production path writes during panel generation.

## SECTION 7 - Blocking Issues

No blocking issues remain for panel writing.

Panel writing may begin next as a separate, explicitly scoped task. That task should write panel artifacts only and should continue to block discovery, IC scoring, redundancy screening, refinement, validation, governance mutation, threshold changes, production registration, and ML.

## SECTION 8 - Minor Risks

- The formula implementation is currently exercised on synthetic OHLCV data only. Real-data panel writing should include source-data availability diagnostics before writing outputs.
- The formula engine returns in-memory candidate outputs for all candidates at once. The panel-writing task should write one artifact per candidate and preserve no-rewrite dry-run checks.
- Cross-sectional z-scores can be null on dates with too few eligible observations or zero cross-sectional variance; this is expected but should be surfaced in panel-generation diagnostics.

## SECTION 9 - Review Fix Applied

Review fix:

- Updated `above_ma_50` and `above_ma_100` construction so invalid OHLCV rows remain null rather than becoming `0`.
- Added a focused test confirming invalid OHLCV rows are excluded from same-date breadth eligibility.

This did not change candidate identities, formula definitions, formula weights, horizons, roles, or registry metadata.

## SECTION 10 - Verification Commands

Commands executed:

- `python -m py_compile pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py` - passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation.py` - 6 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py` - 6 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py` - 16 passed
- `pytest` - 76 passed

## SECTION 11 - Recommended Next Step

The next task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Candidate Panel Writing v1**.

That task may:

- add a panel-writing runner mode;
- generate one candidate panel per approved formula candidate;
- write per-candidate metadata JSON files;
- write panel manifest and generation summary artifacts;
- add panel-writing tests.

That task must not execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, change thresholds, register production artifacts, or implement ML.

Final classification: `FORMULA_IMPLEMENTATION_READY_FOR_PANEL_WRITING`.
