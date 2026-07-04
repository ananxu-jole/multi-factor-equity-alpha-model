# Project Underdog - OHLCV Volatility-of-Volatility Real Validation Execution v1

## SECTION 1 - Executive Summary

This note records the approved real validation execution for the two OHLCV Volatility-of-Volatility bounded refinement candidates.

Input classification:

- `VALIDATION_EXECUTION_APPROVED`

Validation execution classification:

- `VALIDATION_EXECUTION_COMPLETE_PASS`

Validation candidates:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Comparator-only anchors:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

Both approved validation candidates passed the validation execution checks used in this run. The pass conclusion is based on positive primary-horizon evidence, positive primary-horizon anchor deltas, positive stability slices, sufficient coverage, constructive turnover proxies, and positive secondary-horizon support. Contamination diagnostics remain placeholder-only because reference contamination panels were not provided to this runner; therefore this execution should proceed to validation research review before any governance advancement.

No formulas were modified, no panels were regenerated, no historical discovery IC artifacts were recomputed, no watch/park candidates were included, no governance decisions were changed, no production registry files were changed, no thresholds were changed, no ML was introduced, and no candidate was promoted to production.

## SECTION 2 - Inputs Reviewed

Reviewed:

- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_execution_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_design_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_readiness_after_integrity_hardening_v1.md`

Execution runner:

- `pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py`

Input artifacts:

- Panel root: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
- Panel manifest: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/panel_manifest.csv`
- Close source: `data/processed/phase2/nb01_data_foundation/close_prices.parquet`

Input checksums recorded in `validation_manifest.json` and `reproducibility_lock.json`:

| input | sha256 |
| --- | --- |
| panel manifest | `a3883ebe9664a63e2147ea8db3877b182b802c59b7963c036b688cee18b1212c` |
| close source | `9fff711ed9f7edbb12873857dfa5d607eaa8f3e3d8a40a272e78559c65706534` |

## SECTION 3 - Reproducibility Lock

Reproducibility lock artifact:

- `artifacts/research/ohlcv_volatility_of_volatility_validation_v1/reproducibility_lock.json`

Recorded fields include:

- current git commit hash: `6d61c26963d9ea3c9e0445c9c44bd0849c8b64b8`
- git working tree status;
- Python version: `Python 3.13.9`;
- selected package versions for `numpy`, `pandas`, `pyarrow`, and `pytest`;
- runner path and runner SHA-256;
- input artifact paths;
- input manifest/checksum metadata;
- execution timestamp from the validation manifest;
- validation configuration;
- random seed field with `None` and `unused_deterministic_validation` policy.

The working tree was not clean before execution because previous Project Underdog research notes, pipeline files, and tests were already present as modified or untracked local work. This validation execution did not require reverting or mutating unrelated work.

## SECTION 4 - Execution Command

Validation command:

```bash
python pipelines/run_ohlcv_volatility_of_volatility_validation_v1.py --out-dir artifacts/research/ohlcv_volatility_of_volatility_validation_v1
```

Execution completed successfully. The runtime emitted local CPU feature probing warnings from dependency initialization, but the process exited successfully and wrote the validation artifact package.

## SECTION 5 - Artifacts Generated

Artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_validation_v1/`

Required artifacts generated:

- `validation_manifest.json`
- `validation_config.json`
- `reproducibility_lock.json`
- `candidate_validation_summary.csv`
- `candidate_horizon_validation_scores.csv`
- `daily_validation_ic.csv`
- `rolling_stability_diagnostics.csv`
- `anchor_delta_summary.csv`
- `coverage_turnover_summary.csv`
- `contamination_placeholder_summary.csv`
- `validation_decision_summary.csv`

Additional runner-contract artifacts retained:

- `anchor_comparison.csv`
- `approved_panel_manifest_copy.csv`
- `contamination_correlation_matrix.csv`
- `contamination_overlap_summary.csv`
- `coverage_turnover_diagnostics.csv`
- `reference_manifest.csv`
- `rolling_validation_diagnostics.csv`
- `stability_window_summary.csv`
- `validation_decision_inputs.csv`

## SECTION 6 - Candidate Validation Outcomes

| candidate_id | outcome | primary horizon | primary mean IC | primary IC IR | primary positive IC rate | primary mean IC delta vs anchor | primary IC IR delta vs anchor |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `vov_03_ref_strict_chop` | `VALIDATION_PASS` | h10 | 0.012030 | 0.102764 | 0.549903 | 0.003826 | 0.028661 |
| `vov_01_ref_smoothed_calm` | `VALIDATION_PASS` | h20 | 0.011976 | 0.107079 | 0.540303 | 0.001571 | 0.013882 |

Both candidates passed the run-level checks:

- positive primary-horizon mean IC;
- primary positive IC rate above the run threshold;
- positive primary-horizon anchor delta on mean IC and IC IR;
- positive recent and second-half primary-horizon stability slices;
- sufficient primary coverage and active coverage;
- positive secondary-horizon support.

## SECTION 7 - Anchor Delta Interpretation

### vov_03_ref_strict_chop

Primary h10 result:

- candidate h10 mean IC: 0.012030
- anchor h10 mean IC: 0.008204
- h10 mean IC delta: 0.003826
- candidate h10 IC IR: 0.102764
- anchor h10 IC IR: 0.074103
- h10 IC IR delta: 0.028661
- h10 positive IC rate delta: 0.002907

Supporting h20 result:

- h20 mean IC: 0.010626
- h20 mean IC delta versus anchor: 0.003302
- h20 IC IR delta versus anchor: 0.025502

Interpretation:

`vov_03_ref_strict_chop` improved the branch anchor at the primary h10 horizon and retained constructive h20 support. This is a clean validation pass within the current runner's available diagnostics.

### vov_01_ref_smoothed_calm

Primary h20 result:

- candidate h20 mean IC: 0.011976
- anchor h20 mean IC: 0.010405
- h20 mean IC delta: 0.001571
- candidate h20 IC IR: 0.107079
- anchor h20 IC IR: 0.093197
- h20 IC IR delta: 0.013882
- h20 positive IC rate delta: 0.004920

Supporting h10 result:

- h10 mean IC: 0.005958
- h10 mean IC delta versus anchor: -0.000160
- h10 IC IR delta versus anchor: -0.001919

Interpretation:

`vov_01_ref_smoothed_calm` improved the branch anchor at the primary h20 horizon and retained positive h10 support, though h10 was slightly below the anchor. This remains a validation pass because h20 is the predeclared primary horizon and h10 stayed positive rather than contradictory.

## SECTION 8 - Stability, Coverage, And Turnover

| candidate_id | recent 252 primary mean IC | second-half primary mean IC | active coverage ratio | mean rank-turnover proxy |
| --- | ---: | ---: | ---: | ---: |
| `vov_03_ref_strict_chop` | 0.025962 | 0.012521 | 0.190024 | 0.051569 |
| `vov_01_ref_smoothed_calm` | 0.046586 | 0.012959 | 0.261458 | 0.047727 |

Interpretation:

- Both candidates retained positive recent-window and second-half primary-horizon mean IC.
- `vov_03_ref_strict_chop` is more selective than its anchor, with active coverage ratio of 0.190024.
- `vov_01_ref_smoothed_calm` retained broader active coverage of 0.261458.
- Rank-turnover proxies were moderate and did not trigger a stop condition.

## SECTION 9 - Contamination Placeholders

The validation runner emitted contamination placeholder artifacts for:

- volatility compression;
- hostile/stress repair;
- persistence/rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- `vov_05`-like behavior.

Contamination status:

- `PLACEHOLDER_REFERENCE_NOT_PROVIDED`

Interpretation:

The placeholder artifacts confirm contract coverage but do not constitute computed contamination evidence. The next validation review must not treat placeholder rows as proof that contamination risk is absent. The appropriate interpretation is: validation IC, stability, coverage, turnover, and anchor-delta evidence passed, while contamination reference scoring remains a review item.

## SECTION 10 - Stop Conditions

Stop-condition review:

| condition | status |
| --- | --- |
| Candidate outside approved validation targets included | PASS |
| Comparator anchor treated as validation candidate | PASS |
| WATCH/PARK candidates included | PASS |
| `dpath_*` or `ecluster_*` included | PASS |
| Panel regeneration required | PASS |
| Historical IC artifacts recomputed | PASS |
| Formula modification required | PASS |
| Duplicate or blocked candidate issue found | PASS |
| Manifest output missing | PASS |
| Reproducibility lock missing | PASS |

No fail-closed stop condition triggered.

## SECTION 11 - Verification

Post-execution verification performed:

- Validation artifact integrity check passed.
- Required artifact files are present.
- Manifest output paths resolve.
- Validation candidates are exactly:
  - `vov_03_ref_strict_chop`
  - `vov_01_ref_smoothed_calm`
- Comparator anchors are exactly:
  - `vov_03_ref_anchor`
  - `vov_01_ref_anchor`
- Metric artifacts contain only approved validation-scope IDs.
- `candidate_validation_summary.csv` and `validation_decision_summary.csv` contain only the two approved validation candidates.
- Validation outcomes are within the approved vocabulary:
  - `VALIDATION_PASS`
  - `VALIDATION_WATCH`
  - `VALIDATION_FAIL`
  - `VALIDATION_INCONCLUSIVE`
- Reproducibility lock is present.
- No tracked status changes appeared under:
  - `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/`
  - `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
  - `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

Guardrail confirmation:

- No formula changes.
- No panel regeneration.
- No historical discovery IC artifact recomputation.
- No governance decision changes.
- No production registry changes.
- No threshold value changes.
- No ML introduction.
- No production promotion.

## SECTION 12 - Final Recommendation

Validation execution completed successfully with both approved candidates passing:

- `vov_03_ref_strict_chop`: `VALIDATION_PASS`
- `vov_01_ref_smoothed_calm`: `VALIDATION_PASS`

Final classification:

- `VALIDATION_EXECUTION_COMPLETE_PASS`

Recommended next phase:

- **Project Underdog - OHLCV Volatility-of-Volatility Validation Results Review v1**

The next review should interpret the validation evidence, explicitly handle contamination placeholder limitations, decide whether additional contamination-reference scoring is required, and determine whether either passed candidate should proceed to post-validation governance review. No production promotion should occur from this execution note alone.
