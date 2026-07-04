# Project Underdog - OHLCV Volatility-of-Volatility Research Module IC Discovery v1

## SECTION 1 - Executive Summary

This note documents Phase 8 - IC Discovery for the approved OHLCV Volatility-of-Volatility research module.

Lifecycle reference:

- Phase 8 - IC Discovery from `project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`.

Input status:

- Governance standard: `PROJECT_STANDARD_APPROVED`.
- Panel audit classification: `PANELS_APPROVED_FOR_IC_DISCOVERY`.
- Candidate universe: approved VoV panels only.

IC discovery classification:

- `IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`

Summary result:

- `vov_01` and `vov_03` are classified `ADVANCE_TO_REFINEMENT`.
- `vov_05` is classified `WATCH`.
- `vov_02` and `vov_04` are classified `REJECT`.

This was a research-only IC discovery pass. It did not modify formulas, regenerate panels, use Family B/C candidates, perform refinement, perform validation, change governance, modify production registry, change thresholds, or introduce ML.

## SECTION 2 - Inputs Reviewed

Approved panel root:

- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1/`

Approved input panels:

| candidate_id | source_spec_id | panel |
| --- | --- | --- |
| `vov_01` | `vov_01_instability_calm_after_chop` | `vov_01_signal_panel.parquet` |
| `vov_02` | `vov_02_low_extension_vov_rise` | `vov_02_signal_panel.parquet` |
| `vov_03` | `vov_03_range_chop_exhaustion` | `vov_03_signal_panel.parquet` |
| `vov_04` | `vov_04_vov_slope_divergence` | `vov_04_signal_panel.parquet` |
| `vov_05` | `vov_05_churn_controlled_vov_stabilization` | `vov_05_signal_panel.parquet` |

Panel validation:

- Approved panel validation was run before IC execution.
- Panel validation passed.

Blocked families:

- No `dpath_*` candidates were used.
- No `ecluster_*` candidates were used.

## SECTION 3 - IC Methodology

Forward-return source:

- `data/processed/phase2/nb01_data_foundation/close_prices.parquet`

Horizons evaluated:

- h1
- h5
- h10
- h20

Primary review horizons:

- h10
- h20

Method:

- For each candidate and horizon, forward returns were computed as `close[t+h] / close[t] - 1`.
- Daily cross-sectional rank IC was computed between candidate `signal_value[t]` and forward returns starting after signal date `t`.
- Signal timing follows the audited panel policy: `after_close_t_forward_returns_after_t`.
- Dates with fewer than 25 valid signal/return observations were treated as missing IC.
- h1 and h5 were interpreted as diagnostic horizons only and do not override weak h10/h20 evidence.

Candidate recommendation rules were conservative:

- `ADVANCE_TO_REFINEMENT` requires positive primary-horizon evidence with mean IC at least 0.005, IC IR at least 0.030, positive IC rate at least 0.530, and sufficient coverage.
- `WATCH` requires positive primary-horizon mean IC with acceptable positive-rate and coverage evidence but not enough evidence for refinement.
- `REJECT` applies to weak, noisy, or negative primary-horizon evidence.

## SECTION 4 - Generated Artifacts

Artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/ic_discovery_v1/`

Generated artifacts:

- `daily_ic.csv`
- `candidate_horizon_ic_scores.csv`
- `candidate_ic_summary.csv`
- `horizon_summary.csv`
- `family_summary.csv`
- `candidate_rankings.csv`
- `rolling_ic_diagnostics.csv`
- `approved_panel_manifest.csv`
- `manifest.json`

## SECTION 5 - Candidate-Level Results

Candidate rankings by best primary horizon:

| rank | candidate_id | best primary horizon | best primary mean IC | best primary IC IR | best primary positive IC rate | best any horizon | best any mean IC | recommendation |
| ---: | --- | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1 | `vov_05` | h20 | 0.012620 | 0.111840 | 0.518574 | h20 | 0.012620 | `WATCH` |
| 2 | `vov_01` | h20 | 0.010405 | 0.093197 | 0.535383 | h20 | 0.010405 | `ADVANCE_TO_REFINEMENT` |
| 3 | `vov_03` | h10 | 0.008204 | 0.074103 | 0.546996 | h5 | 0.009007 | `ADVANCE_TO_REFINEMENT` |
| 4 | `vov_02` | h10 | -0.001241 | -0.012829 | 0.516756 | h1 | 0.002299 | `REJECT` |
| 5 | `vov_04` | h10 | -0.010251 | -0.082759 | 0.458847 | h1 | 0.001060 | `REJECT` |

Interpretation:

- `vov_01` has clean h20 evidence and clears the refinement threshold. Its h10 result is also positive, which reduces single-horizon concern.
- `vov_03` clears the refinement threshold at h10 and remains positive at h20. Its best any-horizon result is h5, but the h10 result is strong enough for primary-horizon consideration.
- `vov_05` has the strongest h20 mean IC and IC IR, but its h20 positive IC rate is below the advance threshold. It should be watched, not refined immediately.
- `vov_02` shows only weak short-horizon behavior and negative h10/h20 mean IC. It should be rejected.
- `vov_04` is negative at h5/h10/h20 and should be rejected.

## SECTION 6 - Candidate-Horizon Results

| candidate_id | h1 mean IC / IR / pos | h5 mean IC / IR / pos | h10 mean IC / IR / pos | h20 mean IC / IR / pos |
| --- | --- | --- | --- | --- |
| `vov_01` | 0.000919 / 0.007974 / 0.506770 | 0.004906 / 0.042134 / 0.517442 | 0.006118 / 0.053418 / 0.529383 | 0.010405 / 0.093197 / 0.535383 |
| `vov_02` | 0.002299 / 0.022552 / 0.515957 | -0.000198 / -0.001975 / 0.513081 | -0.001241 / -0.012829 / 0.516756 | -0.004617 / -0.050176 / 0.483651 |
| `vov_03` | 0.004270 / 0.036603 / 0.514713 | 0.009007 / 0.075870 / 0.526341 | 0.008204 / 0.074103 / 0.546996 | 0.007324 / 0.066417 / 0.522882 |
| `vov_04` | 0.001060 / 0.007960 / 0.497547 | -0.005586 / -0.042966 / 0.487709 | -0.010251 / -0.082759 / 0.458847 | -0.012392 / -0.104205 / 0.466568 |
| `vov_05` | 0.002769 / 0.023570 / 0.499509 | 0.007313 / 0.062947 / 0.508358 | 0.011795 / 0.103657 / 0.519961 | 0.012620 / 0.111840 / 0.518574 |

Primary-horizon read:

- h10/h20 evidence is strongest for `vov_05`, `vov_01`, and `vov_03`.
- `vov_01` has the cleanest advance profile because h20 mean IC, IC IR, and positive IC rate all clear the conservative threshold.
- `vov_03` has the cleanest h10 positive-rate profile.
- `vov_05` is economically interesting but does not clear the positive-rate threshold.

## SECTION 7 - Horizon-Level Results

| horizon | candidate count | family mean IC | mean positive IC rate | mean coverage ratio |
| --- | ---: | ---: | ---: | ---: |
| h1 | 5 | 0.002264 | 0.506899 | 0.631681 |
| h5 | 5 | 0.003089 | 0.510586 | 0.618416 |
| h10 | 5 | 0.002925 | 0.514388 | 0.606000 |
| h20 | 5 | 0.002668 | 0.505411 | 0.588206 |

Horizon interpretation:

- Family-level evidence is positive across all four horizons, but modest.
- The strongest family mean IC is h5, followed closely by h10 and h20.
- Primary-horizon evidence is not broad across all candidates; it is concentrated in `vov_01`, `vov_03`, and `vov_05`.
- h1 evidence is diagnostic only and does not drive recommendations.

## SECTION 8 - Family-Level Assessment

The VoV family produced a constructive first-pass result, but not broad family proof.

Positive evidence:

- Family mean IC is positive across h1/h5/h10/h20.
- Two candidates clear conservative refinement-readiness thresholds.
- One additional candidate has strong h20 mean IC and IC IR but weaker positive-rate support.

Risks:

- Evidence is candidate-concentrated.
- `vov_02` and `vov_04` are not supported at the primary horizons.
- The best family behavior may still overlap with volatility compression or stress stabilization and must be reviewed in Phase 9 before any refinement.

Conclusion:

- VoV is a credible research module after first-pass IC discovery.
- Candidate-level advancement is justified for `vov_01` and `vov_03`.
- Family-level validation or production readiness is not implied.

## SECTION 9 - Rolling IC Interpretation

Latest rolling 252-day mean IC highlights:

| candidate_id | h10 rolling 252 mean IC | h20 rolling 252 mean IC | h20 rolling 252 positive IC rate | interpretation |
| --- | ---: | ---: | ---: | --- |
| `vov_01` | 0.021965 | 0.045991 | 0.626984 | Supportive recent h10/h20 behavior. |
| `vov_02` | -0.018664 | -0.033617 | 0.289683 | Recent medium-horizon behavior is adverse. |
| `vov_03` | 0.011816 | 0.031769 | 0.579365 | Supportive recent medium-horizon behavior. |
| `vov_04` | -0.040280 | -0.058783 | 0.269841 | Recent medium-horizon behavior is strongly adverse. |
| `vov_05` | 0.043184 | 0.060650 | 0.503968 | Strong recent mean IC but weaker hit-rate profile. |

Rolling interpretation:

- Rolling diagnostics support `vov_01` and `vov_03` as refinement candidates.
- `vov_05` remains watch-worthy because recent h10/h20 mean IC is strong, but the h20 rolling positive-rate profile is not as clean as the mean.
- `vov_02` and `vov_04` show adverse rolling medium-horizon behavior and should not continue.

## SECTION 10 - Candidate Recommendations

| candidate_id | recommendation | rationale |
| --- | --- | --- |
| `vov_01` | `ADVANCE_TO_REFINEMENT` | Positive h10/h20 profile, h20 mean IC 0.010405, h20 IC IR 0.093197, h20 positive IC rate 0.535383, and supportive rolling h20 behavior. |
| `vov_03` | `ADVANCE_TO_REFINEMENT` | Positive h5/h10/h20 profile, h10 mean IC 0.008204, h10 IC IR 0.074103, h10 positive IC rate 0.546996, and supportive rolling h10/h20 behavior. |
| `vov_05` | `WATCH` | Strongest h20 mean IC and IC IR, but h20 positive IC rate of 0.518574 does not clear the advance threshold. Requires Phase 9 review before any refinement consideration. |
| `vov_02` | `REJECT` | Negative h10/h20 mean IC despite mild h1 behavior. Short-horizon diagnostics do not rescue weak medium-horizon evidence. |
| `vov_04` | `REJECT` | Negative h5/h10/h20 evidence and adverse rolling medium-horizon behavior. |

Recommended Phase 9 focus:

- Review `vov_01`, `vov_03`, and `vov_05` against volatility compression, stress repair, persistence, rank-coherence, and reversal references before authorizing any refinement.

## SECTION 11 - Guardrail Confirmation

Confirmed:

- No formulas were modified.
- No panels were regenerated.
- Approved panel artifacts were not modified.
- No `dpath_*` candidates were used or implemented.
- No `ecluster_*` candidates were used or implemented.
- No refinement was performed.
- No validation was performed.
- No governance files were modified.
- No production registry files were modified.
- No thresholds were changed.
- No ML was introduced.

Manifest guardrail flags:

- `panel_generation_executed`: false.
- `panels_modified`: false.
- `formulas_modified`: false.
- `family_b_or_c_used`: false.
- `refinement_executed`: false.
- `validation_executed`: false.
- `governance_modified`: false.
- `production_registration`: false.
- `thresholds_modified`: false.
- `ml_integration`: false.

## SECTION 12 - Verification Summary

Verification commands run:

| command | result |
| --- | --- |
| `python pipelines/run_ohlcv_volatility_of_volatility_panel_generation_v1.py --validate-only` | passed |
| `python -m py_compile pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py pipelines/run_ohlcv_volatility_of_volatility_panel_generation_v1.py pipelines/ohlcv_volatility_of_volatility_research_module_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py -q` | passed, 5 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_panel_generation_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py tests/test_rank_coherence_discovery_scaffold.py tests/test_registry_validation.py -q` | passed, 22 tests |
| `python pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py` | generated Phase 8 IC discovery artifacts |

Runtime note:

- PyArrow emitted local CPU feature warnings during parquet reads. These warnings did not block panel validation or IC discovery.

## SECTION 13 - Recommended Phase 9 Next Step

Proceed to:

**Project Underdog - OHLCV Volatility-of-Volatility Research Review v1**

Phase 9 should review the IC discovery artifacts, candidate concentration, rolling behavior, horizon stability, contamination risk, and redundancy against existing families.

Phase 9 should not perform refinement, validation, governance mutation, production registration, threshold changes, or ML.

Final classification:

- `IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`
