# Project Underdog - OHLCV Volatility-of-Volatility Validation Runner and Artifact Contract v1

## SECTION 1 - Executive Summary

This note records the implementation of validation-runner infrastructure and the artifact contract for the two approved OHLCV Volatility-of-Volatility bounded refinement validation candidates.

Implementation classification:

- `VALIDATION_RUNNER_READY_FOR_EXECUTION_REVIEW`

Implemented validation candidates only:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Baseline comparators only:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

The runner is infrastructure-only until separately executed as a validation task. It includes fail-closed scope checks, input panel validation, h1/h5/h10/h20 validation metrics, h10/h20 primary-horizon support, anchor delta metrics, rolling stability diagnostics, coverage and turnover proxies, contamination-check placeholder artifacts, hardened checksum and threshold metadata, and validate-only/dry-run mode.

No formulas were modified, no panels were regenerated, no historical IC discovery artifacts were recomputed, no watch/park candidates were included, no governance decisions were changed, no production registry files were changed, no thresholds were changed, no ML was introduced, and no candidates were promoted.

## SECTION 2 - Inputs Reviewed

Reviewed notes:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_readiness_after_integrity_hardening_v1.md`
- `docs/research_notes/project_underdog_vov_ic_integrity_hardening_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_design_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_master_state_update_v1.md`

Reviewed implementation patterns:

- `pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`
- `pipelines/run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py`
- existing VoV/refinement implementation and panel-validation tests.

## SECTION 3 - Files Created Or Modified

Created:

- `pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_validation_v1.py`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`

No research artifacts under the VoV panel or IC artifact roots were modified.

## SECTION 4 - Runner Capabilities

The validation runner implements:

1. Validation runner entry point.
2. Artifact contract for future validation execution.
3. Audited refinement panel validation before scoring.
4. Candidate/comparator inclusion checks.
5. Walk-forward-style rolling stability metrics using 63, 126, and 252 trading-day windows.
6. h1/h5/h10/h20 validation metrics, with h10/h20 primary-horizon emphasis.
7. Anchor delta metrics for approved candidates versus branch anchors.
8. Coverage and rank-turnover proxy diagnostics.
9. Contamination-check artifact placeholders for required reference families.
10. Hardened panel-manifest and close-source checksum metadata.
11. Stable validation-threshold metadata in the manifest.
12. Validate-only and dry-run mode.
13. Focused tests using synthetic temporary panels.

The runner uses strictly forward returns:

- `close.shift(-horizon) / close - 1.0`

This preserves the after-close timing rule: signal date `t` is after-close on `t`, and return measurement begins strictly after `t`.

## SECTION 5 - Scope Enforcement

Approved validation candidates:

| candidate_id | role | primary horizon | secondary horizons |
| --- | --- | --- | --- |
| `vov_03_ref_strict_chop` | validation candidate | h10 | h5, h20 |
| `vov_01_ref_smoothed_calm` | validation candidate | h20 | h5, h10 |

Comparator-only anchors:

| candidate_id | role | allowed use |
| --- | --- | --- |
| `vov_03_ref_anchor` | baseline comparator | Compare `vov_03_ref_strict_chop` against the `vov_03` branch anchor. |
| `vov_01_ref_anchor` | baseline comparator | Compare `vov_01_ref_smoothed_calm` against the `vov_01` branch anchor. |

Excluded candidates:

- `vov_01_ref_longer_memory`
- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`
- `vov_02`
- `vov_04`
- `vov_05`
- `dpath_*`
- `ecluster_*`

Scope rules:

- The runner preflights the full audited eight-variant refinement panel package.
- It then selects only the two approved validation candidates and two comparator anchors.
- Any missing approved candidate/comparator fails preflight.
- Any blocked candidate ID or blocked family prefix fails preflight.
- WATCH and PARK variants cannot appear in validation metric outputs.
- Anchors are marked `baseline_comparator` and are not emitted as validation decision candidates.

## SECTION 6 - Artifact Contract

Default future validation artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/validation_design_v1/`

When validation execution is separately authorized, the runner writes:

- `validation_manifest.json`
- `daily_validation_ic.csv`
- `candidate_horizon_validation_scores.csv`
- `rolling_validation_diagnostics.csv`
- `anchor_comparison.csv`
- `coverage_turnover_diagnostics.csv`
- `contamination_correlation_matrix.csv`
- `contamination_overlap_summary.csv`
- `stability_window_summary.csv`
- `validation_decision_inputs.csv`
- `approved_panel_manifest_copy.csv`
- `reference_manifest.csv`

Validate-only/dry-run mode writes only:

- `validation_manifest.json`

Manifest metadata includes:

- `run_id`
- `module_id`
- `validation_design_id`
- `readiness_note_id`
- `validation_candidate_ids`
- `baseline_comparator_ids`
- `validation_scope_ids`
- `excluded_candidate_ids`
- `anchor_by_candidate`
- `primary_horizon_by_candidate`
- `secondary_horizons_by_candidate`
- `horizons`
- `rolling_windows`
- `timing_policy`
- `validation_thresholds`
- `input_lineage_checksums`
- fail-closed guardrail flags.

Guardrail flags include:

- `validation_executed`
- `panel_validation_executed`
- `panel_generation_executed`
- `historical_ic_artifacts_recomputed`
- `approved_panels_modified`
- `formulas_modified`
- `watch_or_park_candidates_included`
- `blocked_candidates_used`
- `baseline_comparators_promoted`
- `governance_modified`
- `production_registration`
- `thresholds_modified`
- `ml_integration`

## SECTION 7 - Contamination Artifact Placeholders

The runner creates placeholder contamination artifacts for:

- volatility compression;
- hostile/stress repair;
- persistence/rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- `vov_05`-like behavior.

Placeholder rows are marked:

- `PLACEHOLDER_REFERENCE_NOT_PROVIDED`

This preserves the artifact contract without fabricating unavailable contamination-reference diagnostics. Actual contamination reference scoring remains a later validation execution/review concern.

## SECTION 8 - Tests Added

Focused validation-runner tests cover:

- validate-only mode writes a fail-closed manifest without scoring;
- full runner execution on synthetic temporary panels writes the expected artifact contract;
- only approved validation candidates and comparator anchors appear in metric outputs;
- validation decision inputs include only the two approved candidates;
- anchors remain comparator-only;
- watch/park scope drift fails preflight;
- daily IC uses a hand-computable known-answer Spearman fixture.

The tests use temporary synthetic panels and do not touch archived research artifacts.

## SECTION 9 - Verification

Verification commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py tests/test_ohlcv_volatility_of_volatility_validation_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_validation_v1.py -q` | passed, 4 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q` | passed, 15 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py -q` | passed, 16 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_panel_generation_v1.py tests/test_registry_validation.py -q` | passed, 19 tests |
| `python pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py --validate-only --out-dir /private/tmp/vov_validation_validate_only_check` | passed |

Verification notes:

- The validate-only command wrote only to `/private/tmp/vov_validation_validate_only_check`.
- No validation metrics were written to the default research artifact root during this implementation task.
- The validate-only command emitted environment warnings from local CPU feature probing, but the command completed successfully.

## SECTION 10 - Guardrail Confirmation

Confirmed:

- Only `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` are validation candidates.
- `vov_03_ref_anchor` and `vov_01_ref_anchor` are comparator-only.
- WATCH and PARK variants are excluded from validation outputs.
- `dpath_*` and `ecluster_*` are blocked.
- No formulas were modified.
- No panels were regenerated.
- No historical IC discovery artifacts were recomputed.
- No governance decisions were changed.
- No production registry files were changed.
- No threshold values were changed.
- No ML was introduced.
- No candidates were promoted.

## SECTION 11 - Final Classification

Final classification:

- `VALIDATION_RUNNER_READY_FOR_EXECUTION_REVIEW`

Recommended next phase:

- Conduct a validation runner execution review, then separately authorize validation execution if the runner and artifact contract are accepted.
