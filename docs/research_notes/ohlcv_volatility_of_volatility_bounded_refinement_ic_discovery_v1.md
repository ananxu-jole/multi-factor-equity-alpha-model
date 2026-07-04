# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement IC Discovery v1

## SECTION 1 - Discovery Objective

This note records the research-only IC discovery pass for the approved bounded OHLCV Volatility-of-Volatility refinement panels.

Current input classification:

- `REFINEMENT_PANELS_APPROVED_FOR_IC_DISCOVERY`

IC discovery classification:

- `REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`

This task computed IC diagnostics only. It did not modify formulas, regenerate panels, modify approved panel artifacts, run validation, modify governance, modify production registry entries, change thresholds, introduce ML, or include blocked candidates.

## SECTION 2 - Inputs And Artifact Root

Approved panel root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`

IC discovery artifact root:

- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

Close-price source:

- `data/processed/phase2/nb01_data_foundation/close_prices.parquet`

Approved refinement variants:

- `vov_01_ref_anchor`
- `vov_01_ref_strict_calm`
- `vov_01_ref_longer_memory`
- `vov_01_ref_smoothed_calm`
- `vov_03_ref_anchor`
- `vov_03_ref_strict_chop`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`

Blocked candidates remained excluded:

- `vov_05`
- `vov_02`
- `vov_04`
- `dpath_*`
- `ecluster_*`

## SECTION 3 - Methodology

IC method:

- Signals were loaded only from the audited long-form refinement panels.
- Forward returns were computed from close prices for `h1`, `h5`, `h10`, and `h20`.
- A signal dated `t` was aligned to forward returns strictly after `t`.
- Daily IC was computed as same-date cross-sectional Spearman rank correlation between `signal_value` and the forward return.
- A daily IC was emitted only when at least 25 valid signal/return observations were available.
- Rolling IC diagnostics were computed over 63, 126, and 252 daily windows.

Primary review horizons:

- `h10`
- `h20`

Anchor comparisons:

- `vov_01` family variants were compared against `vov_01_ref_anchor`.
- `vov_03` family variants were compared against `vov_03_ref_anchor`.

Recommendation labels:

- `ADVANCE_TO_VALIDATION_DESIGN`
- `WATCH`
- `REJECT`

## SECTION 4 - Generated Outputs

Generated files:

- `daily_ic.csv`
- `candidate_horizon_ic_scores.csv`
- `candidate_ic_summary.csv`
- `horizon_summary.csv`
- `family_summary.csv`
- `candidate_rankings.csv`
- `rolling_ic_diagnostics.csv`
- `approved_panel_manifest.csv`
- `manifest.json`

Manifest guardrails:

- Panel validation before IC: true.
- IC discovery executed: true.
- Panel generation executed: false.
- Approved panels modified: false.
- Formulas modified: false.
- Blocked candidates used: false.
- Validation executed: false.
- Governance modified: false.
- Production registration: false.
- Thresholds modified: false.
- ML integration: false.

## SECTION 5 - Candidate Rankings

Candidate rankings by best primary-horizon mean IC:

| rank | candidate_id | best primary horizon | mean IC | IC IR | positive IC rate | mean IC delta vs anchor | recommendation |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `vov_01_ref_longer_memory` | h20 | 0.013444 | 0.112031 | 0.510154 | 0.003039 | WATCH |
| 2 | `vov_03_ref_strict_chop` | h10 | 0.012030 | 0.102764 | 0.549903 | 0.003826 | ADVANCE_TO_VALIDATION_DESIGN |
| 3 | `vov_01_ref_smoothed_calm` | h20 | 0.011976 | 0.107079 | 0.540303 | 0.001571 | ADVANCE_TO_VALIDATION_DESIGN |
| 4 | `vov_01_ref_strict_calm` | h20 | 0.010820 | 0.096723 | 0.549048 | 0.000414 | WATCH |
| 5 | `vov_01_ref_anchor` | h20 | 0.010405 | 0.093197 | 0.535383 | 0.000000 | ADVANCE_TO_VALIDATION_DESIGN |
| 6 | `vov_03_ref_longer_chop` | h20 | 0.010121 | 0.080855 | 0.519126 | 0.002797 | WATCH |
| 7 | `vov_03_ref_anchor` | h10 | 0.008204 | 0.074103 | 0.546996 | 0.000000 | ADVANCE_TO_VALIDATION_DESIGN |
| 8 | `vov_03_ref_extension_controlled` | h10 | 0.007910 | 0.071819 | 0.546027 | -0.000294 | WATCH |

## SECTION 6 - Anchor Comparisons

`vov_01` refinement family:

- `vov_01_ref_anchor` remains validation-design eligible on its own h20 evidence: mean IC 0.010405, IC IR 0.093197, and positive IC rate 0.535383.
- `vov_01_ref_smoothed_calm` is the strongest vov_01 refinement upgrade for validation-design consideration. It improved h20 mean IC by 0.001571 versus anchor and preserved positive IC rate above 0.54.
- `vov_01_ref_longer_memory` had the highest h20 mean IC in the family, improving h20 mean IC by 0.003039, but its h20 positive IC rate was only 0.510154. It is therefore watch rather than validation-design ready.
- `vov_01_ref_strict_calm` improved positive IC rate but only marginally improved mean IC versus anchor; it is watch.

`vov_03` refinement family:

- `vov_03_ref_anchor` remains validation-design eligible on h10 evidence: mean IC 0.008204, IC IR 0.074103, and positive IC rate 0.546996.
- `vov_03_ref_strict_chop` is the strongest vov_03 refinement upgrade. It improved h10 mean IC by 0.003826 versus anchor and had h10 positive IC rate of 0.549903.
- `vov_03_ref_longer_chop` improved h20 mean IC versus the h20 anchor comparison, but its h20 positive IC rate was 0.519126 and its h10 result weakened versus anchor. It is watch.
- `vov_03_ref_extension_controlled` did not improve primary-horizon mean IC versus anchor and remains watch.

## SECTION 7 - Horizon-Level Results

Horizon summary:

| horizon | candidate count | mean IC | mean positive IC rate |
| --- | ---: | ---: | ---: |
| h1 | 8 | 0.002235 | 0.508273 |
| h5 | 8 | 0.006921 | 0.520571 |
| h10 | 8 | 0.008292 | 0.533028 |
| h20 | 8 | 0.010215 | 0.528989 |

Interpretation:

- The strongest family-level evidence is concentrated at h20 by mean IC.
- h10 also remains constructive and has the strongest average positive IC rate.
- h1 evidence is weak and diagnostic only.
- h5 is positive but secondary to the h10/h20 review horizons.

## SECTION 8 - Family-Level Assessment

Family summary by refinement branch:

| refinement_family | horizon | candidate count | mean IC | mean positive IC rate |
| --- | --- | ---: | ---: | ---: |
| `vov_01_refinement` | h1 | 4 | 0.000785 | 0.503170 |
| `vov_01_refinement` | h5 | 4 | 0.005427 | 0.516645 |
| `vov_01_refinement` | h10 | 4 | 0.007957 | 0.526679 |
| `vov_01_refinement` | h20 | 4 | 0.011661 | 0.533722 |
| `vov_03_refinement` | h1 | 4 | 0.003686 | 0.513377 |
| `vov_03_refinement` | h5 | 4 | 0.008416 | 0.524498 |
| `vov_03_refinement` | h10 | 4 | 0.008627 | 0.539377 |
| `vov_03_refinement` | h20 | 4 | 0.008770 | 0.524256 |

Family interpretation:

- `vov_01_refinement` is h20-led, with the smoothed-calm variant providing the cleanest improvement over anchor.
- `vov_03_refinement` is strongest around h10/h20, with strict-chop providing the clearest refinement improvement.
- Both branches retain positive medium-horizon evidence after bounded refinement.

## SECTION 9 - Rolling IC Interpretation

Rolling IC diagnostics were generated for 63, 126, and 252 day windows.

Interpretation:

- Rolling diagnostics should be reviewed in Phase 9 before any validation-design authorization.
- The current pass indicates medium-horizon evidence is not isolated to a single daily IC observation because the ranked candidates have nontrivial scored date counts and positive IC rates above 0.53 where advanced.
- The watch candidates require rolling-stability scrutiny, especially `vov_01_ref_longer_memory`, whose mean IC is strong but whose positive IC rate is weak relative to validation-design candidates.

## SECTION 10 - Candidate Recommendations

Candidate recommendations:

| candidate_id | recommendation | rationale |
| --- | --- | --- |
| `vov_01_ref_anchor` | ADVANCE_TO_VALIDATION_DESIGN | Anchor remains strong at h20 and sets the baseline for the vov_01 branch. |
| `vov_01_ref_smoothed_calm` | ADVANCE_TO_VALIDATION_DESIGN | Improves h20 mean IC, IC IR, and positive IC rate versus anchor with a small, interpretable smoothing change. |
| `vov_03_ref_anchor` | ADVANCE_TO_VALIDATION_DESIGN | Anchor remains constructive at h10 and sets the baseline for the vov_03 branch. |
| `vov_03_ref_strict_chop` | ADVANCE_TO_VALIDATION_DESIGN | Strongest vov_03 refinement; improves h10 mean IC and IC IR versus anchor while retaining high positive IC rate. |
| `vov_01_ref_longer_memory` | WATCH | Highest h20 mean IC, but positive IC rate is too weak for validation-design authorization. |
| `vov_01_ref_strict_calm` | WATCH | Good h20 positive IC rate but only marginal mean IC improvement versus anchor. |
| `vov_03_ref_longer_chop` | WATCH | Improves h20 but weakens h10 versus anchor and has lower positive IC rate. |
| `vov_03_ref_extension_controlled` | WATCH | Does not improve primary-horizon mean IC versus anchor. |

Rejected candidates:

- None.

## SECTION 11 - Guardrail Confirmation

Guardrail status:

- Formula changes: no.
- Panel regeneration: no.
- Approved panel artifact mutation: no.
- Candidate validation: no.
- Governance mutation: no.
- Production registry mutation: no.
- Threshold changes: no.
- ML introduced: no.
- Blocked candidates included: no.

## SECTION 12 - Verification Summary

Verification commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py -q` | passed, 5 tests |
| `python pipelines/run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py --validate-only` | passed |
| `python pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py -q` | passed, 8 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_rank_coherence_discovery_scaffold.py tests/test_registry_validation.py -q` | passed, 8 tests |

Runtime warnings:

- Validate-only and IC execution emitted local compute-stack `sysctlbyname` warnings.
- IC execution emitted NumPy invalid-value warnings for degenerate daily rank-correlation slices.
- These warnings did not prevent artifact generation and are reflected as missing daily IC values where correlations could not be computed.

## SECTION 13 - Recommended Next Step

Recommended next task:

**Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Research Review v1**

The next task should review the IC discovery artifacts, rolling IC diagnostics, anchor comparisons, and candidate recommendations before any governance decision or validation-design work.

Final classification:

- `REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`
