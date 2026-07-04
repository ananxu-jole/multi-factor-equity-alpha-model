# Project Underdog - OHLCV Volatility-of-Volatility Validation Readiness After IC Integrity Hardening v1

## SECTION 1 - Executive Summary

This note reviews whether validation implementation may proceed for the approved OHLCV Volatility-of-Volatility bounded refinement candidates after completion of the IC integrity hardening pass.

Readiness classification:

- `VALIDATION_IMPLEMENTATION_MAY_PROCEED_WITH_NOTES`

Conclusion:

Validation implementation may proceed for the two approved bounded VoV refinement candidates:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

The baseline comparators remain comparator-only:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

The IC integrity hardening work completed the minor corrective actions identified by the research integrity audit without changing prior IC results, rankings, panels, formulas, governance decisions, production registry state, thresholds, or ML scope. The validation design remains valid and should now be implemented using the hardened IC manifest and test expectations.

The readiness classification includes notes because historical IC artifacts were intentionally not regenerated. Future validation artifacts should use the hardened manifest conventions, including input checksums and stable classification-threshold metadata.

## SECTION 2 - Inputs Reviewed

Reviewed notes:

- `docs/research_notes/project_underdog_research_integrity_and_anti_fabrication_audit_v1.md`
- `docs/research_notes/project_underdog_vov_ic_integrity_hardening_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_design_review_v1.md`

Reviewed classifications:

| source | classification | readiness interpretation |
| --- | --- | --- |
| Research integrity and anti-fabrication audit | `RESEARCH_INTEGRITY_CONFIRMED_WITH_MINOR_NOTES` | No blocking integrity defect was found. Minor notes required test and manifest hardening before validation work continued. |
| VoV IC integrity hardening | `IC_INTEGRITY_HARDENING_COMPLETE` | The required integrity-hardening items were completed without changing prior research results. |
| VoV validation design review | `VALIDATION_DESIGN_READY_FOR_IMPLEMENTATION` | The validation plan is implementation-ready for the two approved candidates only. |

## SECTION 3 - Integrity Hardening Assessment

The IC integrity hardening pass is complete.

Completed hardening items:

- Tiny hand-computable Spearman IC known-answer tests were added for original VoV and bounded refinement IC runners.
- Candidate-summary grain regression tests were added so `candidate_ic_summary.csv` is locked to candidate-level grain in future runs.
- Future IC manifests now document expected input checksum fields for panel manifests and close-price inputs.
- Future IC manifests include stable `classification_thresholds` metadata.
- Classification threshold constants are named and tested for manifest consistency.

The hardening note reports:

- No existing IC result changes.
- No existing ranking artifact changes.
- No panel regeneration.
- No research artifact regeneration.
- No threshold value changes.
- Focused IC tests and relevant VoV/refinement regression tests passed.

Interpretation:

The hardening work directly addresses the minor notes from the integrity audit and strengthens validation implementation preconditions. It does not alter the scientific basis of the approved validation candidates.

## SECTION 4 - Prior Results and Artifact Status

Prior VoV and bounded refinement results remain unchanged.

Artifact status:

- Existing panel artifacts were not regenerated.
- Existing IC artifacts were not recomputed.
- Existing candidate rankings were not altered.
- Existing governance decisions were not changed.
- Existing production registry state was not changed.

Important note:

The historical original VoV `candidate_ic_summary.csv` artifact was intentionally not rewritten. The hardening pass fixes future runner behavior and adds tests, but does not mutate archived research evidence. Downstream validation implementation should not rely on the historical original-module `candidate_ic_summary.csv` filename as proof of candidate-level grain unless the artifact is separately regenerated under an approved task.

## SECTION 5 - Validation Candidate Continuity

Validation candidates are unchanged from the approved validation design.

| candidate_id | role | parent | primary validation horizon | secondary horizons | readiness |
| --- | --- | --- | --- | --- | --- |
| `vov_03_ref_strict_chop` | validation candidate | `vov_03` | h10 | h5, h20 | approved for validation implementation |
| `vov_01_ref_smoothed_calm` | validation candidate | `vov_01` | h20 | h5, h10 | approved for validation implementation |

Baseline comparators are unchanged and remain comparator-only.

| candidate_id | role | policy |
| --- | --- | --- |
| `vov_03_ref_anchor` | baseline comparator | May be used only for branch-level comparison against `vov_03_ref_strict_chop`. |
| `vov_01_ref_anchor` | baseline comparator | May be used only for branch-level comparison against `vov_01_ref_smoothed_calm`. |

The following candidates remain excluded from validation implementation:

- `vov_01_ref_longer_memory`
- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`
- `vov_02`
- `vov_04`
- `vov_05`
- `dpath_*`
- `ecluster_*`

## SECTION 6 - Governance and Design Continuity

Governance continuity:

- The bounded refinement governance outcome remains unchanged.
- Validation-design authorization remains limited to `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`.
- Baseline comparators remain diagnostic only.
- WATCH and PARK candidates remain archived and are not validation targets.
- No additional refinement cycle is authorized.

Validation-design continuity:

- The validation objective remains to test whether the two refined VoV candidates retain out-of-sample IC evidence beyond their anchors and beyond likely contamination channels.
- The h10/h20 emphasis remains unchanged.
- Required metrics, stability checks, coverage checks, turnover checks, redundancy checks, contamination checks, stop conditions, and post-validation governance rules remain valid.
- The IC integrity hardening pass strengthens the implementation standard but does not require redesigning candidate hypotheses.

## SECTION 7 - Remaining Notes

Validation implementation may proceed with the following notes:

1. Future validation manifests should include input checksum fields for source panels, close-price inputs, and any approved comparator inputs.
2. Future validation manifests should include stable threshold metadata where classifications or pass/fail decisions are emitted.
3. Validation implementation should include a known-answer or independently recomputed metric fixture analogous to the new IC hardening tests.
4. Historical IC artifacts should remain archived as evidence and should not be silently rewritten to adopt the new manifest conventions.
5. Comparator anchors must remain comparator-only and must not become validation candidates through implementation convenience.

These notes are implementation safeguards, not blockers.

## SECTION 8 - Verification

Verification checks performed:

- Confirmed the integrity audit classification is `RESEARCH_INTEGRITY_CONFIRMED_WITH_MINOR_NOTES`.
- Confirmed the hardening classification is `IC_INTEGRITY_HARDENING_COMPLETE`.
- Confirmed the validation design classification is `VALIDATION_DESIGN_READY_FOR_IMPLEMENTATION`.
- Confirmed the approved validation candidates remain `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`.
- Confirmed baseline comparators remain `vov_03_ref_anchor` and `vov_01_ref_anchor`.
- Confirmed no tracked status changes under:
  - `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/`
  - `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/`

No validation execution was performed.

No panels, IC artifacts, formulas, governance decisions, production registry files, thresholds, or ML files were changed by this readiness review.

## SECTION 9 - Final Readiness Decision

Validation implementation may proceed.

Classification:

- `VALIDATION_IMPLEMENTATION_MAY_PROCEED_WITH_NOTES`

Approved validation implementation targets:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Comparator-only baselines:

- `vov_03_ref_anchor`
- `vov_01_ref_anchor`

Recommended next phase:

- Implement the VoV validation runner and validation artifact contract for the two approved candidates only, with comparator-only anchor handling and hardened manifest/checksum/threshold metadata expectations.
