# Project Underdog - Dispersion Path-Dependence IC Discovery v1

## SECTION 1 - Executive Summary

Classification: **IC_DISCOVERY_COMPLETE_WITH_NOTES**

The first IC Discovery for the Dispersion Path-Dependence research module was completed using only the audited panel snapshot:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

No panels were regenerated. No formulas, implementation logic, governance state, production registry, thresholds, validation workflow, refinement workflow, or ML integration were modified.

Evaluated candidates:

- `dpath_01_relapse_resilience_after_calm`
- `dpath_02_disagreement_vol_stress_divergence`
- `dpath_03_elevated_disagreement_stabilization`
- `dpath_04_consensus_without_crowding`

Overall result: the family did not produce broad positive h10/h20 evidence. The only constructive primary-horizon result was `dpath_01_relapse_resilience_after_calm`, with h10 mean IC of 0.005919 and IC IR of 0.043167, but its h10 positive IC rate was only 0.493976 and h20 was negative. No candidate is recommended to advance to research review from this first discovery pass.

## SECTION 2 - Artifact Outputs

Generated under:

`artifacts/research/dispersion_path_dependence_research_module_v1/ic_discovery_v1/`

| artifact | status |
| --- | --- |
| `daily_ic.csv` | generated |
| `candidate_horizon_ic_scores.csv` | generated |
| `candidate_ic_summary.csv` | generated |
| `horizon_summary.csv` | generated |
| `family_summary.csv` | generated |
| `candidate_rankings.csv` | generated |
| `rolling_ic_diagnostics.csv` | generated |
| `approved_panel_manifest.csv` | generated |
| `manifest.json` | generated |

The manifest records the audited panel checksums from the panel audit, the copied panel manifest checksum, the close-price source checksum, and research-only guardrail fields.

## SECTION 3 - Candidate Results

| candidate_id | h1 mean IC / IR / pos | h5 mean IC / IR / pos | h10 mean IC / IR / pos | h20 mean IC / IR / pos |
| --- | --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | -0.007530 / -0.067207 / 0.409639 | 0.003713 / 0.029773 / 0.493976 | 0.005919 / 0.043167 / 0.493976 | -0.001747 / -0.012971 / 0.469880 |
| `dpath_02_disagreement_vol_stress_divergence` | -0.003563 / -0.019158 / 0.500000 | -0.014437 / -0.079044 / 0.444293 | -0.022556 / -0.137782 / 0.414966 | -0.023558 / -0.157030 / 0.418157 |
| `dpath_03_elevated_disagreement_stabilization` | -0.009583 / -0.052702 / 0.462687 | 0.008365 / 0.048794 / 0.541353 | -0.009952 / -0.061098 / 0.469697 | -0.016816 / -0.108689 / 0.507812 |
| `dpath_04_consensus_without_crowding` | -0.011720 / -0.068164 / 0.464646 | -0.009601 / -0.055226 / 0.515152 | -0.008041 / -0.048668 / 0.481481 | -0.025330 / -0.163569 / 0.456081 |

Family horizon summary:

| horizon | family mean IC | mean IC IR | mean positive IC rate | mean coverage |
| --- | ---: | ---: | ---: | ---: |
| h1 | -0.008099 | -0.051808 | 0.459243 | 0.629999 |
| h5 | -0.002990 | -0.013926 | 0.498694 | 0.616730 |
| h10 | -0.008658 | -0.051095 | 0.465030 | 0.604349 |
| h20 | -0.016863 | -0.110565 | 0.462982 | 0.586665 |

## SECTION 4 - Scientific Evaluation

| candidate_id | lineage / mechanism | scientific question | expected primary horizon | observed strongest horizon | expected activation | observed activation | observed contamination indicator | hypothesis consistency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Disagreement Relapse Resilience | Do securities resilient during renewed disagreement after temporary calm differ from securities that only appeared strong during calm? | h5/h10, implemented primary h10 | h10 | Episodic relapse-after-calm, not all rising-dispersion dates | 4.36% active; turnover proxy 0.012632 | max internal diagnostic corr 0.082191 vs `low_churn_5` | PARTIAL_MATCH |
| `dpath_02_disagreement_vol_stress_divergence` | Disagreement Path Divergence | Does disagreement path add information when volatility and stress paths tell a different story? | h5/h10, implemented primary h10 | h1 | Moderate to low divergence states only | 38.82% active; turnover proxy 0.075839 | max internal diagnostic corr 0.338411 vs `low_extension_20` | MISMATCH |
| `dpath_03_elevated_disagreement_stabilization` | Elevated Disagreement Stabilization | Do orderly securities during elevated but stabilizing disagreement carry positive forward information? | h5/h10, implemented primary h10 | h5 | Moderate elevated-but-stabilizing disagreement paths | 7.10% active; turnover proxy 0.018044 | max internal diagnostic corr 0.127906 vs `low_extension_20` | PARTIAL_MATCH |
| `dpath_04_consensus_without_crowding` | Consensus Formation Without Crowding | Does normalization identify delayed consensus without rewarding crowded leadership? | h5/h10, implemented primary h10 | h10 | Moderate normalization paths after prior disagreement | 15.58% active; turnover proxy 0.030596 | max internal diagnostic corr 0.176567 vs `low_extension_20` | MISMATCH |

Interpretation:

- `dpath_01` matched the expected primary horizon direction at h10, but the positive IC rate was below 0.50 and h20 durability was not present.
- `dpath_03` had the best single positive result at h5, but failed the implemented primary h10 read and weakened at h20.
- `dpath_02` was the clearest empirical mismatch: all primary and secondary horizons were negative, and the strongest horizon was h1 despite h1 also being negative.
- `dpath_04` did not support the consensus-without-crowding hypothesis; h5 positive rate exceeded 0.50, but mean IC was negative across all horizons.

## SECTION 5 - Ranking and Recommendations

| rank | candidate_id | best primary horizon | h10 mean IC | h20 mean IC | hypothesis consistency | recommendation |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 1 | `dpath_01_relapse_resilience_after_calm` | h10 | 0.005919 | -0.001747 | PARTIAL_MATCH | PARK |
| 2 | `dpath_04_consensus_without_crowding` | h10 | -0.008041 | -0.025330 | MISMATCH | REJECT |
| 3 | `dpath_03_elevated_disagreement_stabilization` | h10 | -0.009952 | -0.016816 | PARTIAL_MATCH | PARK |
| 4 | `dpath_02_disagreement_vol_stress_divergence` | h10 | -0.022556 | -0.023558 | MISMATCH | REJECT |

No candidate met the `ADVANCE_TO_RESEARCH_REVIEW` recommendation standard. The two `PARK` decisions preserve weak but nonzero scientific information without promoting candidates to the next lifecycle phase.

## SECTION 6 - Scientific Surprises

The main surprise was that `dpath_01` produced the cleanest primary-horizon mean IC while having the lowest activation rate. This suggests relapse-after-calm may be the least contaminated mechanism in this batch, but the evidence is too thin in positive-rate and h20 durability terms.

The second surprise was `dpath_03`: it produced the best h5 mean IC and positive IC rate, yet reversed at h10 and h20. That is a horizon-consistency concern because the scientific expectation was h5/h10 support, not h5-only behavior.

The broad negative h20 profile is also important. Dispersion Path-Dependence did not show durability evidence in this first pass.

## SECTION 7 - Integrity and Guardrails

Preserved:

- Audited panel snapshot from `panel_v1`.
- Approved four-candidate panel manifest copied to `approved_panel_manifest.csv`.
- Audit-side panel SHA256 references in `manifest.json`.
- Scientific lineage fields in daily and summary outputs.
- Contamination metadata, anchor comparator metadata, activation text, formula text, and timing policy.

Not performed:

- Panel regeneration.
- Formula modification.
- Core formula or panel implementation modification.
- Refinement.
- Validation.
- Governance mutation.
- Production registration.
- Threshold changes.
- ML integration.

## SECTION 8 - Verification

Verification commands run for this phase:

- `python pipelines/run_dispersion_path_dependence_ic_discovery_v1.py`
- `python -m py_compile pipelines/run_dispersion_path_dependence_ic_discovery_v1.py tests/test_dispersion_path_dependence_ic_discovery_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_ic_discovery_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_panel_generation_v1.py`
- `pytest -q tests/test_dispersion_path_dependence_research_module_v1.py`
- `pytest -q tests/test_registry_validation.py`

Results:

- IC discovery execution: PASS.
- `py_compile`: PASS.
- Focused IC tests: 5 passed.
- Panel-generation regression tests: 7 passed.
- Implementation regression tests: 11 passed.
- Registry/scaffold tests: 5 passed.

Runtime notes:

- PyArrow emitted sandbox-local CPU cache probing warnings.
- NumPy emitted invalid-divide warnings for constant/degenerate rank-correlation slices. The run completed and produced finite candidate summary metrics.

## SECTION 9 - Final Recommendation

Classification: **IC_DISCOVERY_COMPLETE_WITH_NOTES**

Recommended next phase: **Dispersion Path-Dependence Research Review v1**, review-only.

The research review should decide whether the parked `dpath_01` and `dpath_03` evidence is worth preserving for future bounded redesign or whether the family should be paused. It should not perform refinement, validation, governance mutation, production registration, threshold changes, or ML work.
