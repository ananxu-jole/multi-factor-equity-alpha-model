# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation IC Discovery v1

## SECTION 1 - Executive Summary

This note documents the first research-only IC discovery pass for the approved OHLCV Non-Hostile Transition and Leadership Rotation panels.

Scope:

- Approved panels only.
- Candidates scored: 9.
- Horizons scored: `h1`, `h5`, `h10`, `h20`.
- IC method: daily cross-sectional Spearman rank IC versus forward close-to-close returns.
- Artifact root: `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/`.

Overall result: the family did not produce supportive primary-horizon IC evidence in this first pass. Every candidate had negative best primary-horizon (`h10`/`h20`) mean IC, so every candidate is classified `REJECT` for this discovery pass.

No refinement, validation, governance mutation, production registration, threshold change, formula change, panel rewrite, or ML work was performed.

## SECTION 2 - Artifacts Generated

Generated artifacts:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/daily_ic.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_ic_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_horizon_ic_scores.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/horizon_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/family_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/candidate_rankings.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/rolling_ic_diagnostics.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/approved_panel_manifest.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1/manifest.json`

Artifact dimensions:

- `daily_ic.csv`: 75528 rows.
- `rolling_ic_diagnostics.csv`: 75528 rows.
- `candidate_ic_summary.csv`: 36 rows.
- `candidate_rankings.csv`: 9 rows.

## SECTION 3 - Candidate Rankings

Ranking uses best primary-horizon mean IC across `h10` and `h20`.

| rank | candidate_id | working_name | best primary horizon | best primary mean IC | best primary IC IR | positive IC rate | classification |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| 1 | `nhlr_05` | Broadening Participation Without Stress | h10 | -0.000173 | -0.001277 | 0.533333 | `REJECT` |
| 2 | `nhlr_10` | Healthy Breadth Contributor | h20 | -0.003871 | -0.023637 | 0.502459 | `REJECT` |
| 3 | `nhlr_08` | Mature Leadership Deceleration Avoidance | h10 | -0.009261 | -0.050130 | 0.508888 | `REJECT` |
| 4 | `nhlr_07` | Rotation Acceleration Leader | h20 | -0.011374 | -0.063963 | 0.479837 | `REJECT` |
| 5 | `nhlr_09` | Volume-Confirmed Leadership Shift | h10 | -0.012459 | -0.066920 | 0.492128 | `REJECT` |
| 6 | `nhlr_02` | Quiet Accumulation Before Leadership | h10 | -0.015638 | -0.085143 | 0.474860 | `REJECT` |
| 7 | `nhlr_03` | Post-Transition Leadership Durability | h10 | -0.015651 | -0.078634 | 0.495175 | `REJECT` |
| 8 | `nhlr_01` | Emerging Leadership From Neutral Base | h10 | -0.016849 | -0.088545 | 0.474352 | `REJECT` |
| 9 | `nhlr_04` | Smooth Trend Handoff | h10 | -0.017945 | -0.085231 | 0.473337 | `REJECT` |

Classification basis:

- `ADVANCE_TO_REFINEMENT` required positive, nontrivial `h10`/`h20` evidence with supportive IC IR and positive IC rate.
- `WATCH` required at least positive primary-horizon evidence with minimally supportive hit rate.
- All candidates failed the primary-horizon positive-mean requirement.

## SECTION 4 - Candidate IC Summary

Mean IC by candidate and horizon:

| candidate_id | h1 | h5 | h10 | h20 |
| --- | ---: | ---: | ---: | ---: |
| `nhlr_01` | -0.007162 | -0.012745 | -0.016849 | -0.017085 |
| `nhlr_02` | 0.002453 | -0.007696 | -0.015638 | -0.022263 |
| `nhlr_03` | 0.000771 | -0.008645 | -0.015651 | -0.016558 |
| `nhlr_04` | -0.005442 | -0.012177 | -0.017945 | -0.025668 |
| `nhlr_05` | 0.004618 | 0.004466 | -0.000173 | -0.004271 |
| `nhlr_07` | -0.007093 | -0.010556 | -0.014466 | -0.011374 |
| `nhlr_08` | 0.002693 | -0.003760 | -0.009261 | -0.015146 |
| `nhlr_09` | -0.003874 | -0.007991 | -0.012459 | -0.014840 |
| `nhlr_10` | 0.001173 | -0.000379 | -0.004884 | -0.003871 |

IC IR by candidate and horizon:

| candidate_id | h1 | h5 | h10 | h20 |
| --- | ---: | ---: | ---: | ---: |
| `nhlr_01` | -0.033043 | -0.062854 | -0.088545 | -0.093979 |
| `nhlr_02` | 0.012505 | -0.039939 | -0.085143 | -0.126947 |
| `nhlr_03` | 0.003500 | -0.041392 | -0.078634 | -0.086416 |
| `nhlr_04` | -0.023291 | -0.054881 | -0.085231 | -0.127885 |
| `nhlr_05` | 0.029503 | 0.031465 | -0.001277 | -0.033206 |
| `nhlr_07` | -0.035633 | -0.054850 | -0.079108 | -0.063963 |
| `nhlr_08` | 0.013206 | -0.019193 | -0.050130 | -0.086142 |
| `nhlr_09` | -0.018178 | -0.039974 | -0.066920 | -0.081415 |
| `nhlr_10` | 0.005738 | -0.002049 | -0.027615 | -0.023637 |

Positive IC rate by candidate and horizon:

| candidate_id | h1 | h5 | h10 | h20 |
| --- | ---: | ---: | ---: | ---: |
| `nhlr_01` | 0.495450 | 0.493921 | 0.474352 | 0.472180 |
| `nhlr_02` | 0.506067 | 0.488855 | 0.474860 | 0.480347 |
| `nhlr_03` | 0.523761 | 0.504053 | 0.495175 | 0.499745 |
| `nhlr_04` | 0.494439 | 0.488855 | 0.473337 | 0.464012 |
| `nhlr_05` | 0.515738 | 0.527935 | 0.533333 | 0.508197 |
| `nhlr_07` | 0.489383 | 0.492401 | 0.471305 | 0.479837 |
| `nhlr_08` | 0.527806 | 0.504053 | 0.508888 | 0.503828 |
| `nhlr_09` | 0.502528 | 0.508105 | 0.492128 | 0.487494 |
| `nhlr_10` | 0.515738 | 0.527935 | 0.520325 | 0.502459 |

## SECTION 5 - Horizon Summary

| horizon | candidate count | mean IC | median IC | mean IC IR | mean positive IC rate | mean coverage ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| h1 | 9 | -0.001318 | 0.000771 | -0.005077 | 0.507879 | 0.631015 |
| h5 | 9 | -0.006609 | -0.007991 | -0.031519 | 0.504013 | 0.617535 |
| h10 | 9 | -0.011925 | -0.014466 | -0.062512 | 0.493745 | 0.604899 |
| h20 | 9 | -0.014564 | -0.015146 | -0.080399 | 0.488678 | 0.586749 |

Strongest horizon:

- h1 was least negative at the family level, but h1 is not the primary economic horizon for most of the family.
- h10/h20, the primary review horizons, were negative across the batch.

## SECTION 6 - Family Summary

The family-level result is weak in this discovery pass.

Family-level mean IC:

- h1: -0.001318
- h5: -0.006609
- h10: -0.011925
- h20: -0.014564

Interpretation:

- The expected medium-horizon non-hostile transition / leadership rotation mechanism did not appear in this first IC pass.
- `nhlr_05` and `nhlr_10` were the least weak candidates, but neither produced positive primary-horizon mean IC.
- The family should not advance to refinement on the current evidence.

## SECTION 7 - Rolling IC Diagnostics

Rolling diagnostics were written to:

- `rolling_ic_diagnostics.csv`

Windows:

- 63 trading days
- 126 trading days
- 252 trading days

The latest rolling diagnostics show some recent positive rolling h10 behavior for `nhlr_05` and `nhlr_10`, but the full-sample primary-horizon evidence remains negative. This is a monitoring note only and does not justify refinement.

## SECTION 8 - Coverage and Observation Counts

Coverage was computed after aligning approved panels to the available close-price matrix.

Observation count totals by horizon:

- h1: 4871850
- h5: 4768143
- h10: 4671031
- h20: 4531712

Mean coverage ratio by horizon:

- h1: 0.631015
- h5: 0.617535
- h10: 0.604899
- h20: 0.586749

Coverage declines with horizon because forward-return availability declines near the end of the sample and because the approved panels include some tickers not present in the close-price target matrix.

## SECTION 9 - Guardrails

This pass did not:

- refine candidates;
- modify formulas;
- modify panels;
- perform validation;
- promote or demote candidates;
- change governance;
- register production candidates;
- change thresholds;
- introduce ML.

The manifest records:

- `ic_discovery_executed = true`
- `ir_calculated = true`
- `refinement_executed = false`
- `validation_executed = false`
- `governance_modified = false`
- `production_registered = false`
- `thresholds_modified = false`
- `ml_implemented = false`
- `formulas_modified = false`
- `panels_modified = false`

## SECTION 10 - Verification

Commands executed:

- `python -m py_compile pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1.py pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py` - passed
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --validate-candidate-panels` - passed before IC execution
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation.py` - 5 passed
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1.py` - completed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery.py` - 2 passed after implementation patch
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1.py` - reran after summary-order patch
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --validate-candidate-panels` - passed after IC execution
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_formula_implementation.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py` - 33 passed
- `pytest` - 81 passed

Warnings:

- Existing pandas `FutureWarning` remains in the panel-generation wide-source normalization test path. It is not part of IC scoring and did not affect this discovery pass.

## SECTION 11 - Recommendation

Recommendation: do not advance any candidate to refinement from this IC discovery pass.

Candidate classifications:

- `ADVANCE_TO_REFINEMENT`: 0
- `WATCH`: 0
- `REJECT`: 9

The appropriate next step is a research review, not refinement. The review should decide whether the family should be parked, whether the target direction is economically inverted, or whether the candidate formulas are too close to crowded/anti-predictive leadership behavior. No additional execution should occur until that review is complete.
