# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Research Review v1

## SECTION 1 - Review Objective

This note reviews the bounded OHLCV Volatility-of-Volatility refinement IC discovery results and determines which candidates should proceed to validation-design review.

Current input classification:

- `REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`

Research review classification:

- `VALIDATION_DESIGN_APPROVED`

This is a review-only phase. It does not run validation, recompute IC, regenerate panels, modify formulas, change governance, modify production registry entries, change thresholds, or introduce ML.

## SECTION 2 - Inputs Reviewed

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_ic_discovery_v1.md`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_panel_audit_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md`

Reviewed artifact files:

- `candidate_rankings.csv`
- `candidate_horizon_ic_scores.csv`
- `candidate_ic_summary.csv`
- `horizon_summary.csv`
- `family_summary.csv`
- `rolling_ic_diagnostics.csv`
- `manifest.json`

## SECTION 3 - Refinement Ranking Interpretation

Candidate rankings by best primary-horizon mean IC:

| rank | candidate_id | best horizon | mean IC | IC IR | positive IC rate | delta vs anchor | IC discovery label | review decision |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 1 | `vov_01_ref_longer_memory` | h20 | 0.013444 | 0.112031 | 0.510154 | 0.003039 | WATCH | WATCH |
| 2 | `vov_03_ref_strict_chop` | h10 | 0.012030 | 0.102764 | 0.549903 | 0.003826 | ADVANCE_TO_VALIDATION_DESIGN | ADVANCE |
| 3 | `vov_01_ref_smoothed_calm` | h20 | 0.011976 | 0.107079 | 0.540303 | 0.001571 | ADVANCE_TO_VALIDATION_DESIGN | ADVANCE |
| 4 | `vov_01_ref_strict_calm` | h20 | 0.010820 | 0.096723 | 0.549048 | 0.000414 | WATCH | PARK |
| 5 | `vov_01_ref_anchor` | h20 | 0.010405 | 0.093197 | 0.535383 | 0.000000 | ADVANCE_TO_VALIDATION_DESIGN | VALIDATION-DESIGN REVIEW ELIGIBLE |
| 6 | `vov_03_ref_longer_chop` | h20 | 0.010121 | 0.080855 | 0.519126 | 0.002797 | WATCH | PARK |
| 7 | `vov_03_ref_anchor` | h10 | 0.008204 | 0.074103 | 0.546996 | 0.000000 | ADVANCE_TO_VALIDATION_DESIGN | VALIDATION-DESIGN REVIEW ELIGIBLE |
| 8 | `vov_03_ref_extension_controlled` | h10 | 0.007910 | 0.071819 | 0.546027 | -0.000294 | WATCH | PARK |

Ranking interpretation:

- `vov_03_ref_strict_chop` is the cleanest refinement improvement in the vov_03 branch: it improves h10 mean IC, IC IR, and positive IC rate versus anchor.
- `vov_01_ref_smoothed_calm` is the cleanest refinement improvement in the vov_01 branch: it improves h20 mean IC, IC IR, and positive IC rate versus anchor while preserving the original mechanism.
- `vov_01_ref_longer_memory` has the highest primary-horizon mean IC, but its h20 positive IC rate is only 0.510154 and trails the anchor by 0.025230. The high mean IC is not enough to justify validation-design review.
- The two anchors remain eligible as baseline validation-design references, but they should not displace the two refined improvements.

## SECTION 4 - vov_01 Family Interpretation

The `vov_01` branch is h20-led.

Primary-horizon evidence:

| candidate_id | h10 mean IC | h10 pos rate | h20 mean IC | h20 pos rate | review interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `vov_01_ref_anchor` | 0.006118 | 0.529383 | 0.010405 | 0.535383 | Baseline remains credible. |
| `vov_01_ref_strict_calm` | 0.006897 | 0.527441 | 0.010820 | 0.549048 | Too close to anchor in mean IC. |
| `vov_01_ref_longer_memory` | 0.012856 | 0.522425 | 0.013444 | 0.510154 | Strong mean IC, weak hit rate. |
| `vov_01_ref_smoothed_calm` | 0.005958 | 0.527467 | 0.011976 | 0.540303 | Best validation-design refinement. |

Family interpretation:

- `vov_01_ref_smoothed_calm` is the preferred vov_01 refinement because it improves the h20 mean IC by 0.001571 and h20 IC IR by 0.013882 versus anchor while also improving positive IC rate.
- `vov_01_ref_longer_memory` is useful evidence that longer-memory VoV calming can produce stronger mean IC, but its weak h20 positive IC rate suggests event concentration or uneven payoff distribution.
- `vov_01_ref_strict_calm` is not sufficiently differentiated from anchor. It improves h20 positive IC rate, but mean IC improvement is only 0.000414.
- `vov_01_ref_anchor` remains a validation-design eligible baseline and should be carried as a reference in any validation design.

## SECTION 5 - vov_03 Family Interpretation

The `vov_03` branch is strongest at h10, with useful h20 confirmation.

Primary-horizon evidence:

| candidate_id | h10 mean IC | h10 pos rate | h20 mean IC | h20 pos rate | review interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `vov_03_ref_anchor` | 0.008204 | 0.546996 | 0.007324 | 0.522882 | Baseline remains credible. |
| `vov_03_ref_strict_chop` | 0.012030 | 0.549903 | 0.010626 | 0.532619 | Best vov_03 refinement. |
| `vov_03_ref_longer_chop` | 0.006363 | 0.514582 | 0.010121 | 0.519126 | h20 lift but h10 thesis weakens. |
| `vov_03_ref_extension_controlled` | 0.007910 | 0.546027 | 0.007008 | 0.522395 | Does not improve anchor. |

Family interpretation:

- `vov_03_ref_strict_chop` is the strongest validation-design candidate in the branch. It improves h10 mean IC by 0.003826 and h10 IC IR by 0.028661 versus anchor, with positive IC rate slightly above anchor.
- `vov_03_ref_longer_chop` improves h20 but weakens the branch's stated h10 primary mechanism; this makes it unsuitable for validation-design review.
- `vov_03_ref_extension_controlled` does not improve anchor at h10 or h20 and should be parked.
- `vov_03_ref_anchor` remains validation-design eligible as a baseline reference.

## SECTION 6 - Anchor Comparison Interpretation

Anchor comparison conclusions:

- Both anchor variants remain credible and should be retained as baseline references.
- Neither anchor should be treated as the sole forward candidate because each branch has one refined variant with clearer improvement.
- Validation-design review should be centered on `vov_01_ref_smoothed_calm` and `vov_03_ref_strict_chop`, with `vov_01_ref_anchor` and `vov_03_ref_anchor` included as explicit baseline comparators.

Anchor eligibility:

| anchor | eligible role |
| --- | --- |
| `vov_01_ref_anchor` | Validation-design baseline comparator for the vov_01 branch. |
| `vov_03_ref_anchor` | Validation-design baseline comparator for the vov_03 branch. |

## SECTION 7 - Horizon Behavior

Horizon summary:

| horizon | candidate count | mean IC | mean positive IC rate | interpretation |
| --- | ---: | ---: | ---: | --- |
| h1 | 8 | 0.002235 | 0.508273 | Diagnostic only. |
| h5 | 8 | 0.006921 | 0.520571 | Positive but secondary. |
| h10 | 8 | 0.008292 | 0.533028 | Constructive and strongest by hit rate. |
| h20 | 8 | 0.010215 | 0.528989 | Strongest by mean IC. |

Horizon interpretation:

- The refinement remains medium-horizon, not h1-led.
- h20 is strongest for the vov_01 branch.
- h10 is strongest for the vov_03 branch.
- The two approved refined candidates match their intended branch horizons: `vov_01_ref_smoothed_calm` at h20 and `vov_03_ref_strict_chop` at h10.

## SECTION 8 - Rolling IC Stability

Rolling IC review focused on each candidate's best primary horizon.

| candidate_id | horizon | rolling 63 mean | rolling 126 mean | rolling 252 mean | review |
| --- | --- | ---: | ---: | ---: | --- |
| `vov_01_ref_smoothed_calm` | h20 | 0.011275 | 0.011710 | 0.009983 | Acceptable; improves anchor with similar rolling profile. |
| `vov_03_ref_strict_chop` | h10 | 0.011305 | 0.011139 | 0.010957 | Strongest rolling profile among vov_03 candidates. |
| `vov_01_ref_anchor` | h20 | 0.009714 | 0.010133 | 0.008503 | Baseline stable enough for comparator role. |
| `vov_03_ref_anchor` | h10 | 0.007528 | 0.007614 | 0.007598 | Baseline stable enough for comparator role. |
| `vov_01_ref_longer_memory` | h20 | 0.013290 | 0.012745 | 0.011189 | Strong mean but weak recent positive-rate profile. |

Rolling interpretation:

- `vov_03_ref_strict_chop` has the most persuasive rolling profile: all rolling mean IC averages are positive and stronger than the vov_03 anchor.
- `vov_01_ref_smoothed_calm` has a positive rolling profile and improves the vov_01 anchor, though it still shows drawdown windows in rolling minima.
- `vov_01_ref_longer_memory` has high rolling mean IC, but its rolling positive IC rate is less convincing, including weak recent 63-day and 126-day positive-rate readings.
- Rolling minima are negative for all candidates, so validation design should include regime and window-stability checks before any stronger claim.

## SECTION 9 - Contamination Discussion

Contamination risks reviewed:

- volatility compression;
- hostile/stress repair;
- persistence/rank stability;
- plain reversal;
- volume-shock reversal;
- watch-only `vov_05`-like behavior.

Assessment:

- `vov_01_ref_smoothed_calm` preserves the original vov_01 mechanism and changes only the slope-noise component. It is not a broad volatility-compression replacement, but validation design should still include volatility-compression and stress-repair redundancy checks.
- `vov_03_ref_strict_chop` preserves the original range-chop exhaustion mechanism and only tightens prior-chop activation. It does not inject a new reversal or stress-repair mechanism, but validation design should test plain-reversal and stress-repair contamination directly.
- `vov_01_ref_longer_memory` is more exposed to vov_05-like behavior because it leans into longer-memory VoV stabilization. Its weak positive IC rate reinforces watch-only treatment pending redundancy review.
- `vov_01_ref_strict_calm` is not contaminated by design, but its incremental evidence is too small.
- `vov_03_ref_longer_chop` risks becoming a slower volatility/chop state proxy rather than a sharper h10 exhaustion signal.
- `vov_03_ref_extension_controlled` was designed to reduce reversal contamination, but it failed to improve anchor evidence.

No formal redundancy or contamination screen was run in this review. Those checks belong in validation design, not this research-review phase.

## SECTION 10 - Candidate Decisions

Official research-review decisions:

| candidate_id | decision | rationale |
| --- | --- | --- |
| `vov_03_ref_strict_chop` | ADVANCE | Strongest vov_03 refinement; meaningful h10 improvement versus anchor with constructive hit rate and rolling profile. |
| `vov_01_ref_smoothed_calm` | ADVANCE | Best vov_01 refinement; improves h20 mean IC, IC IR, and hit rate versus anchor while preserving mechanism. |
| `vov_01_ref_anchor` | VALIDATION-DESIGN REVIEW ELIGIBLE | Retain as vov_01 baseline comparator, not as the preferred refined variant. |
| `vov_03_ref_anchor` | VALIDATION-DESIGN REVIEW ELIGIBLE | Retain as vov_03 baseline comparator, not as the preferred refined variant. |
| `vov_01_ref_longer_memory` | WATCH | Highest mean IC but weak positive IC rate and potential vov_05-like longer-memory contamination. |
| `vov_01_ref_strict_calm` | PARK | Incremental improvement is too small versus anchor. |
| `vov_03_ref_longer_chop` | PARK | h20 lift does not offset h10 weakening versus anchor. |
| `vov_03_ref_extension_controlled` | PARK | Does not improve the primary-horizon anchor comparison. |

No candidate is recommended for production, validation execution, or registry promotion from this review.

## SECTION 11 - Validation-Design Recommendation

Validation-design review is justified for:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Validation-design review should include baseline comparators:

- `vov_01_ref_anchor`
- `vov_03_ref_anchor`

Validation design should explicitly test:

- h10/h20 persistence across time windows;
- redundancy versus original VoV anchors;
- volatility-compression contamination;
- hostile/stress-repair contamination;
- persistence/rank-stability contamination;
- plain-reversal contamination;
- volume-shock reversal contamination;
- relationship to watch-only `vov_05` behavior;
- sensitivity to inactive neutralization and warmup handling.

WATCH archive:

- `vov_01_ref_longer_memory`

Parked archive:

- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`

## SECTION 12 - Explicit Non-Goals

This review did not:

- run validation;
- recompute IC;
- regenerate panels;
- modify formulas;
- change governance;
- modify production registry entries;
- change thresholds;
- introduce ML;
- promote candidates to production;
- run redundancy screening.

## SECTION 13 - Recommended Governance Decision

Recommended governance decision:

- Approve validation-design review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`.
- Authorize inclusion of `vov_01_ref_anchor` and `vov_03_ref_anchor` as baseline comparators only.
- Keep `vov_01_ref_longer_memory` on watch.
- Park `vov_01_ref_strict_calm`, `vov_03_ref_longer_chop`, and `vov_03_ref_extension_controlled`.

Recommended next task:

**Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Governance Decision v1**

The next task should formally record the Phase 10 governance decision. It should not execute validation, modify formulas, regenerate panels, recompute IC, modify production registry entries, change thresholds, or introduce ML.

Final classification:

- `VALIDATION_DESIGN_APPROVED`

## SECTION 14 - Verification Summary

Verification performed:

- Confirmed review inputs exist.
- Confirmed IC discovery classification: `REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`.
- Confirmed panel audit classification: `REFINEMENT_PANELS_APPROVED_FOR_IC_DISCOVERY`.
- Confirmed no implementation files were changed.
- Confirmed no panel files were changed.
- Confirmed no IC artifact files were changed.
- Confirmed no validation, governance, production, threshold, or ML files were changed.
