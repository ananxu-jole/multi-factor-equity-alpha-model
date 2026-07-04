# Project Underdog - OHLCV Volatility-of-Volatility Validation Results Review and Candidate Registration Recommendation v1

## SECTION 1 - Executive Summary

This note reviews the completed OHLCV Volatility-of-Volatility validation results and provides a governance recommendation on whether validated candidates should be recommended for registration into the active research candidate inventory.

Current validation classification:

- `VALIDATION_EXECUTION_COMPLETE_PASS`

Review classification:

- `VALIDATED_CANDIDATES_READY_FOR_REGISTRATION_REVIEW`

Candidate registration recommendations:

| candidate_id | validation outcome | registration recommendation |
| --- | --- | --- |
| `vov_03_ref_strict_chop` | `VALIDATION_PASS` | `REGISTER_RECOMMENDED` |
| `vov_01_ref_smoothed_calm` | `VALIDATION_PASS` | `REGISTER_RECOMMENDED` |

Both candidates are recommended for active research candidate inventory registration review. This is not a production deployment recommendation. Registration should preserve the validation evidence, anchor-comparison context, and the unresolved contamination-reference limitation.

## SECTION 2 - Scope and Inputs Reviewed

Reviewed:

- `docs/research_notes/ohlcv_volatility_of_volatility_real_validation_execution_v1.md`
- `artifacts/research/ohlcv_volatility_of_volatility_validation_v1/`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_governance_decision_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_governance_decision_v1.md`
- `docs/research_notes/project_underdog_research_integrity_and_anti_fabrication_audit_v1.md`
- `docs/research_notes/project_underdog_vov_ic_integrity_hardening_v1.md`

Validation artifacts reviewed:

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

## SECTION 3 - Governance Lineage

Original module governance:

- Classification: `MODULE_GOVERNANCE_APPROVED`.
- `vov_01` and `vov_03` advanced to bounded refinement.
- `vov_05` remained WATCH.
- `vov_02` and `vov_04` were PARKED.

Bounded refinement governance:

- Classification: `REFINEMENT_GOVERNANCE_APPROVED`.
- Validation-design approved targets:
  - `vov_03_ref_strict_chop`
  - `vov_01_ref_smoothed_calm`
- Comparator-only anchors:
  - `vov_03_ref_anchor`
  - `vov_01_ref_anchor`
- WATCH:
  - `vov_01_ref_longer_memory`
- PARK:
  - `vov_01_ref_strict_calm`
  - `vov_03_ref_longer_chop`
  - `vov_03_ref_extension_controlled`

Validation execution:

- Classification: `VALIDATION_EXECUTION_COMPLETE_PASS`.
- Both approved validation candidates passed.
- No production promotion was authorized or performed.

## SECTION 4 - Candidate Evidence Summary

| candidate_id | primary horizon | primary mean IC | primary IC IR | primary positive IC rate | mean IC delta vs anchor | IC IR delta vs anchor | recommendation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `vov_03_ref_strict_chop` | h10 | 0.012030 | 0.102764 | 0.549903 | 0.003826 | 0.028661 | `REGISTER_RECOMMENDED` |
| `vov_01_ref_smoothed_calm` | h20 | 0.011976 | 0.107079 | 0.540303 | 0.001571 | 0.013882 | `REGISTER_RECOMMENDED` |

Both candidates show positive primary-horizon IC, constructive IC IR, positive hit-rate behavior, and primary-horizon improvement versus their branch anchors.

## SECTION 5 - Candidate-Level Review

### vov_03_ref_strict_chop

Registration recommendation:

- `REGISTER_RECOMMENDED`

Rationale:

- Passed validation with h10 as the predeclared primary horizon.
- h10 mean IC was 0.012030, above the `vov_03_ref_anchor` h10 mean IC of 0.008204.
- h10 IC IR improved from 0.074103 for the anchor to 0.102764.
- h10 positive IC rate was 0.549903, slightly above the anchor's 0.546996.
- h20 support was constructive, with h20 mean IC of 0.010626 and a positive h20 mean IC delta versus anchor of 0.003302.
- Recent 252-day primary mean IC was 0.025962.
- Second-half primary mean IC was 0.012521.
- Active coverage ratio was 0.190024, reflecting a more selective strict-chop candidate.
- Mean rank-turnover proxy was 0.051569, below the branch anchor's 0.074393.

Interpretation:

`vov_03_ref_strict_chop` is the cleaner registration recommendation. It improves the anchor at the primary h10 horizon, retains h20 support, and appears to reduce turnover proxy versus the anchor while remaining selective.

Registration caveat:

- Contamination diagnostics are placeholder-only. Active research registration should require a future contamination-reference review before any stronger governance action.

### vov_01_ref_smoothed_calm

Registration recommendation:

- `REGISTER_RECOMMENDED`

Rationale:

- Passed validation with h20 as the predeclared primary horizon.
- h20 mean IC was 0.011976, above the `vov_01_ref_anchor` h20 mean IC of 0.010405.
- h20 IC IR improved from 0.093197 for the anchor to 0.107079.
- h20 positive IC rate improved from 0.535383 to 0.540303.
- h10 support remained positive at 0.005958, although it was slightly below the h10 anchor by -0.000160.
- Recent 252-day primary mean IC was 0.046586.
- Second-half primary mean IC was 0.012959.
- Active coverage ratio was 0.261458.
- Mean rank-turnover proxy was 0.047727, lower than the `vov_01_ref_anchor` turnover proxy of 0.053486.

Interpretation:

`vov_01_ref_smoothed_calm` merits registration review because it improves the branch anchor at the predeclared h20 primary horizon, retains positive h10 support, and reduces turnover proxy. Its h10 anchor delta is slightly negative, so the registration note should emphasize h20-led evidence rather than broad horizon dominance.

Registration caveat:

- The mechanism could still overlap with volatility compression or longer-memory `vov_05`-like behavior. Contamination-reference evidence was not computed in this validation run.

## SECTION 6 - Family-Level Interpretation

The validated VoV family now has two registration-worthy research candidates across two branches:

- `vov_03_ref_strict_chop`: h10-led range-chop exhaustion branch.
- `vov_01_ref_smoothed_calm`: h20-led smoothed calm-after-VoV-dislocation branch.

This supports the view that the original VoV module produced genuine candidate-level evidence that survived bounded refinement and validation execution. The evidence is not yet sufficient for production deployment. It is sufficient for active research candidate inventory registration review because both candidates:

- emerged from approved module governance;
- survived bounded refinement governance;
- passed real validation execution;
- improved their branch anchors at their primary horizons;
- retained positive stability slices;
- preserved reproducibility metadata and artifact lineage.

## SECTION 7 - Stability, Coverage, and Turnover Review

| candidate_id | recent 252 primary mean IC | second-half primary mean IC | active coverage ratio | mean rank-turnover proxy | interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| `vov_03_ref_strict_chop` | 0.025962 | 0.012521 | 0.190024 | 0.051569 | Selective but stable; lower turnover proxy than anchor. |
| `vov_01_ref_smoothed_calm` | 0.046586 | 0.012959 | 0.261458 | 0.047727 | Broader active coverage; stable h20-led behavior. |

Both candidates retained positive recent-window and second-half primary-horizon mean IC. Coverage is sufficient for research inventory registration, though `vov_03_ref_strict_chop` should be tracked as a more selective signal.

## SECTION 8 - Contamination Review

The validation execution emitted contamination placeholder artifacts for:

- volatility compression;
- hostile/stress repair;
- persistence/rank stability;
- rank-coherence;
- plain reversal;
- volume-shock reversal;
- `vov_05`-like behavior.

Status:

- `PLACEHOLDER_REFERENCE_NOT_PROVIDED`

Interpretation:

The validation run did not compute actual contamination-reference correlations or overlap diagnostics. This does not block active research inventory registration recommendation because registration is not production deployment and both candidates passed IC/stability/anchor/coverage checks. However, it does block any stronger claim that the candidates are fully contamination-cleared.

Registration should therefore include this status:

- `validated_ic_pass_contamination_review_pending`

Required follow-up before any production or portfolio integration review:

- compute or audit contamination references for volatility compression, stress repair, persistence/rank stability, rank-coherence, plain reversal, volume-shock reversal, and `vov_05`-like behavior.

## SECTION 9 - Reproducibility and Integrity Review

Reproducibility evidence:

- `reproducibility_lock.json` is present.
- Git commit hash was recorded.
- Working tree status was recorded.
- Python version was recorded.
- selected package versions were recorded.
- runner path and runner checksum were recorded.
- input paths and input checksums were recorded.
- validation configuration and random seed policy were recorded.

Integrity history:

- Research integrity audit classification: `RESEARCH_INTEGRITY_CONFIRMED_WITH_MINOR_NOTES`.
- IC hardening classification: `IC_INTEGRITY_HARDENING_COMPLETE`.
- Validation readiness after hardening classification: `VALIDATION_IMPLEMENTATION_MAY_PROCEED_WITH_NOTES`.
- Validation runner execution review classification: `VALIDATION_EXECUTION_APPROVED`.

Interpretation:

The recent VoV/refinement/validation chain has adequate provenance for active research inventory registration review. The worktree was dirty at execution time, but the dirty status was captured in the reproducibility lock and mostly reflects the ongoing Project Underdog research note and pipeline sequence. This is acceptable for research inventory registration, but future validation governance should prefer a clean committed baseline.

## SECTION 10 - Registration Recommendation

Official recommendation:

| candidate_id | recommendation | registration scope | restrictions |
| --- | --- | --- | --- |
| `vov_03_ref_strict_chop` | `REGISTER_RECOMMENDED` | active research candidate inventory | No production deployment. Contamination-reference review pending. |
| `vov_01_ref_smoothed_calm` | `REGISTER_RECOMMENDED` | active research candidate inventory | No production deployment. Contamination-reference review pending. |

Not recommended for registration from this note:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`
- `vov_01_ref_longer_memory`
- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`
- `vov_02`
- `vov_04`
- `vov_05`
- `dpath_*`
- `ecluster_*`

Comparator anchors should remain baseline comparators only.

## SECTION 11 - Explicit Non-Goals

This review does not:

- modify implementation code;
- modify formulas;
- regenerate panels;
- recompute IC;
- rerun validation;
- modify governance decisions;
- modify the production registry;
- register candidates directly;
- recommend production deployment;
- change thresholds;
- introduce ML.

## SECTION 12 - Verification

Verification performed:

- Reviewed validation execution note and artifacts.
- Reviewed original module governance and bounded refinement governance notes.
- Confirmed validation candidates and outcomes:
  - `vov_03_ref_strict_chop`: `VALIDATION_PASS`
  - `vov_01_ref_smoothed_calm`: `VALIDATION_PASS`
- Confirmed comparator anchors remain comparator-only.
- Confirmed contamination artifacts are placeholder-only.
- Confirmed no implementation changes were made by this review.
- Confirmed no formula changes were made by this review.
- Confirmed no panel changes were made by this review.
- Confirmed no IC recomputation was performed by this review.
- Confirmed no registry or production changes were made by this review.

## SECTION 13 - Final Classification

Final classification:

- `VALIDATED_CANDIDATES_READY_FOR_REGISTRATION_REVIEW`

Recommended next phase:

- **Project Underdog - OHLCV Volatility-of-Volatility Candidate Registration Governance Review v1**

That review should decide whether to register `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` into the active research candidate inventory with explicit non-production status and contamination-review-pending metadata.
