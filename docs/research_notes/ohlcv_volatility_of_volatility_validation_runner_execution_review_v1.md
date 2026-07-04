# Project Underdog - OHLCV Volatility-of-Volatility Validation Runner Execution Review v1

## SECTION 1 - Executive Summary

This note reviews the OHLCV Volatility-of-Volatility validation runner and artifact contract before authorizing real validation execution.

Current input classification:

- `VALIDATION_RUNNER_READY_FOR_EXECUTION_REVIEW`

Execution-review classification:

- `VALIDATION_EXECUTION_APPROVED`

Conclusion:

Real validation execution may begin for the two approved validation candidates only:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

The anchors remain comparator-only:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

No blocking runner, artifact-contract, scope, timing, manifest, or test-coverage issue was found. No fixes were required during this review.

## SECTION 2 - Files Reviewed

Reviewed implementation and tests:

- `pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_validation_v1.py`

Reviewed research notes:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_design_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_readiness_after_integrity_hardening_v1.md`

## SECTION 3 - Scope Review

Approved validation candidates are hardcoded as the only validation candidates:

| candidate_id | role | primary horizon | secondary horizons |
| --- | --- | --- | --- |
| `vov_03_ref_strict_chop` | validation candidate | h10 | h5, h20 |
| `vov_01_ref_smoothed_calm` | validation candidate | h20 | h5, h10 |

Baseline comparators are hardcoded as comparator-only:

| candidate_id | role |
| --- | --- |
| `vov_03_ref_anchor` | baseline comparator |
| `vov_01_ref_anchor` | baseline comparator |

The runner preflights the audited eight-variant refinement panel package, then loads only the four approved validation-scope IDs. It fails closed if an approved candidate or comparator is missing.

Excluded candidates are explicitly listed and not emitted into validation decision inputs:

- `vov_01_ref_longer_memory`
- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`
- `vov_02`
- `vov_04`
- `vov_05`
- `dpath_*`
- `ecluster_*`

Review finding:

- PASS. Scope handling matches the validation design and readiness note.

## SECTION 4 - Candidate And Comparator Role Findings

Candidate roles are assigned through `VALIDATION_CANDIDATE_IDS`, `BASELINE_COMPARATOR_IDS`, and `VALIDATION_SCOPE_IDS`.

Findings:

- `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` are the only rows emitted into `validation_decision_inputs.csv`.
- `vov_03_ref_anchor` and `vov_01_ref_anchor` are emitted as `baseline_comparator` rows in scoring artifacts but not as validation decision candidates.
- Anchor delta logic merges candidate horizon scores to branch anchors by `refinement_family` and `horizon`.
- Primary-horizon decision inputs use `h10` for `vov_03_ref_strict_chop` and `h20` for `vov_01_ref_smoothed_calm`.

Review finding:

- PASS. Anchors remain comparator-only and anchor delta logic is aligned with the design.

## SECTION 5 - Validate-Only And Dry-Run Behavior

Validate-only behavior:

- Runs audited panel validation.
- Checks approved scope availability.
- Writes a fail-closed `validation_manifest.json`.
- Does not write validation metric CSVs.
- Sets `validation_executed` to `false`.
- Sets `panel_validation_executed` to `true`.
- Keeps historical IC recomputation, panel generation, formula modification, governance modification, production registration, threshold modification, and ML flags false.

Review verification used:

- `python pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py --validate-only --out-dir /private/tmp/vov_validation_execution_review_validate_only`

Review finding:

- PASS. Validate-only mode is safe when directed to a review output directory. It wrote only `/private/tmp/vov_validation_execution_review_validate_only/validation_manifest.json`.

## SECTION 6 - Metrics And Artifact Contract Findings

Validation metrics match the design:

- h1, h5, h10, and h20 IC metrics.
- h10 primary handling for `vov_03_ref_strict_chop`.
- h20 primary handling for `vov_01_ref_smoothed_calm`.
- mean IC, median IC, IC standard deviation, IC IR, positive IC rate, coverage ratio, observation counts, scored-date counts, and panel lineage fields.
- rolling 63, 126, and 252 mean IC, IC IR, and positive IC rate.
- branch-anchor deltas for mean IC, IC IR, and positive IC rate.
- coverage and rank-turnover proxy diagnostics.
- stability windows for full sample, first half, second half, and recent 252 dates.

Artifact contract is complete for the approved validation runner:

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

Review finding:

- PASS. The runner can produce the required validation artifact contract when real execution is separately invoked.

## SECTION 7 - Hardened Manifest Findings

Manifest metadata includes:

- validation candidate IDs;
- baseline comparator IDs;
- validation scope IDs;
- excluded candidate IDs;
- anchor mapping;
- primary horizon mapping;
- secondary horizon mapping;
- h1/h5/h10/h20 horizon list;
- rolling windows;
- timing policy;
- validation threshold metadata;
- panel-manifest SHA-256 checksum;
- close-source SHA-256 checksum;
- fail-closed guardrail flags.

Review finding:

- PASS. Hardened checksum and threshold metadata are present.

## SECTION 8 - Contamination Placeholder Note

The runner writes contamination placeholder artifacts for:

- volatility compression;
- hostile/stress repair;
- persistence/rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- `vov_05`-like behavior.

Rows are marked `PLACEHOLDER_REFERENCE_NOT_PROVIDED`.

Interpretation:

This is acceptable for the runner contract because the requested implementation included contamination-check artifact placeholders. Real contamination conclusions must not be drawn from placeholder rows. Any post-validation research review must distinguish placeholder contract coverage from computed contamination evidence.

Review finding:

- PASS with operational note. This does not block validation execution.

## SECTION 9 - Test Coverage Assessment

Focused validation tests cover:

- validate-only mode and fail-closed manifest flags;
- full synthetic execution artifact contract;
- candidate/comparator inclusion scope;
- exclusion of watch/park variants from validation outputs;
- comparator-only anchor handling;
- validation decision inputs limited to the two approved candidates;
- anchor comparison output limited to the two approved candidates;
- manifest checksum and threshold metadata;
- scope-drift rejection;
- known-answer Spearman IC behavior.

Relevant regression tests cover:

- bounded refinement panel generation and implementation;
- original VoV IC discovery and bounded refinement IC discovery;
- original VoV module and panel generation;
- registry validation.

Review finding:

- PASS. Tests are sufficient before real validation execution.

## SECTION 10 - Verification

Verification commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py tests/test_ohlcv_volatility_of_volatility_validation_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_validation_v1.py -q` | passed, 4 tests |
| `python pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py --validate-only --out-dir /private/tmp/vov_validation_execution_review_validate_only` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q` | passed, 15 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py -q` | passed, 16 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_panel_generation_v1.py tests/test_registry_validation.py -q` | passed, 19 tests |

The validate-only command emitted local CPU feature warnings from dependency initialization, but completed successfully.

Artifact-root status:

- No tracked status changes were present under:
  - `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/`
  - `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/`

## SECTION 11 - Guardrail Confirmation

Confirmed:

- Real validation execution was not run in this review.
- No formulas were modified.
- No panels were regenerated.
- No historical IC artifacts were modified.
- No governance decisions were modified.
- No production registry files were modified.
- No threshold values were changed.
- No ML was introduced.
- No candidates were promoted.

## SECTION 12 - Final Decision

Final classification:

- `VALIDATION_EXECUTION_APPROVED`

Real validation execution may begin for:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Comparator-only anchors:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

Recommended next phase:

- Execute the approved VoV validation runner against the audited bounded refinement panels and write the validation artifact package under the approved validation artifact root.
