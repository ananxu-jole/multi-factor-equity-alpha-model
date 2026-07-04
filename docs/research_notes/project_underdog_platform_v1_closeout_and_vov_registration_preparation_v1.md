# Project Underdog - Platform v1 Closeout and VoV Registration Preparation v1

## SECTION 1 - Executive Summary

Classification: `PLATFORM_V1_CLOSED_READY_FOR_REGISTRATION_REVIEW`

Project Underdog Platform v1 is closed as a research-platform milestone. The platform established a standard research module lifecycle, used it to pause externally blocked PIT work, parked the Non-Hostile Transition family after negative evidence, completed the OHLCV Volatility-of-Volatility research module through discovery, bounded refinement, validation design, runner review, and real validation execution, and completed research integrity and IC hardening reviews before candidate registration recommendation.

This note prepares registration-review metadata for exactly two validated VoV refinement candidates:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Both candidates are recommended for active research inventory registration review, not production deployment. Both must carry `contamination-review-pending` metadata because the validation contamination artifacts are placeholder-only.

No active research registry, production registry, formulas, panels, historical IC artifacts, validation results, thresholds, governance decisions, or ML components were modified by this closeout.

## SECTION 2 - Inputs Reviewed

- `docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_validation_results_review_and_candidate_registration_recommendation_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_real_validation_execution_v1.md`
- `docs/research_notes/project_underdog_research_integrity_and_anti_fabrication_audit_v1.md`
- `docs/research_notes/project_underdog_vov_ic_integrity_hardening_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_governance_decision_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_master_state_update_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_governance_decision_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_master_research_state_update_v1.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`

## SECTION 3 - Platform v1 Milestones

1. Standard research module lifecycle approved.

`project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md` established the standard gated lifecycle for future research modules. The standard separated formula design, implementation review, panel specification, panel generation, panel audit, IC discovery, research review, governance, state synchronization, validation design, and validation execution.

2. PIT governance branch responsibly paused.

The CRSP/PIT branch was kept at an externally blocked planning boundary. PIT-dependent research was not forced forward without verified point-in-time source metadata, survivorship handling, and licensing clarity.

3. Non-Hostile Transition parked after negative evidence.

The Non-Hostile Transition and Leadership Rotation family completed its research cycle and was parked after weak or inverted evidence. This prevented extra refinement pressure after the family failed to justify continuation.

4. VoV module completed discovery, refinement, and validation.

The OHLCV Volatility-of-Volatility module completed the standard lifecycle from formula specification through real validation execution. Original discovery identified `vov_01` and `vov_03` as the only eligible refinement parents. The bounded refinement cycle generated and audited exactly eight variants, ran research-only IC discovery, advanced two variants, and completed real validation.

5. Research integrity and IC hardening completed.

The anti-fabrication audit classified recent VoV evidence as integrity-confirmed with minor notes. Follow-up IC hardening added known-answer Spearman coverage, summary-grain protections, checksum expectations, and stable classification-threshold documentation without changing prior results or rankings.

6. Two validated VoV candidates recommended for registration review.

`ohlcv_volatility_of_volatility_validation_results_review_and_candidate_registration_recommendation_v1.md` classified the validation review as `VALIDATED_CANDIDATES_READY_FOR_REGISTRATION_REVIEW` and recommended registration review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`.

## SECTION 4 - Lessons Learned

The lifecycle gates that added the most value were implementation review, panel specification, panel audit, IC discovery review, governance decision recording, and state synchronization. Those gates kept research actions narrow and made it clear when a task was specification-only, artifact-generation-only, discovery-only, validation-design-only, or real validation.

Independent review and panel audit mattered because they caught scope drift before scoring. For VoV, the audit trail repeatedly confirmed that blocked families such as `vov_05`, `vov_02`, `vov_04`, `dpath_*`, and `ecluster_*` did not leak into bounded refinement or validation.

Anchor variants improved refinement interpretability. The anchor panels made it possible to compare refined candidates against formula-equivalent parent baselines, which clarified whether improvements came from the bounded refinement or merely repeated the original signal.

The anti-fabrication and integrity audit should remain standard. It confirmed that IC and ranking evidence was computed from panels rather than manually written outcomes, and the follow-up hardening made future IC manifests more reproducible.

Bounded refinement should remain limited. The VoV refinement cycle benefited from being constrained to approved parents, predeclared variants, audited panels, and a single governance-approved cycle. Additional cycles should require new evidence and explicit authorization.

## SECTION 5 - Candidate Registration Preparation

| field | `vov_03_ref_strict_chop` | `vov_01_ref_smoothed_calm` |
| --- | --- | --- |
| candidate_id | `vov_03_ref_strict_chop` | `vov_01_ref_smoothed_calm` |
| parent_candidate_id | `vov_03` | `vov_01` |
| mechanism_family | OHLCV Volatility-of-Volatility / strict chop exhaustion | OHLCV Volatility-of-Volatility / smoothed calm after VoV dislocation |
| primary_horizon | h10 | h20 |
| validation_outcome | `VALIDATION_PASS` | `VALIDATION_PASS` |
| anchor_comparator | `vov_03_ref_anchor` | `vov_01_ref_anchor` |
| validation_ic_summary | h10 mean IC 0.012030 / IC IR 0.102764 / positive IC rate 0.549903 | h20 mean IC 0.011976 / IC IR 0.107079 / positive IC rate 0.540303 |
| anchor_delta | h10 mean IC +0.003826 / IC IR +0.028661 / positive IC rate +0.002907 | h20 mean IC +0.001571 / IC IR +0.013882 / positive IC rate +0.004920 |
| stability_summary | recent 252 primary mean IC 0.025962; second-half primary mean IC 0.012521 | recent 252 primary mean IC 0.046586; second-half primary mean IC 0.012959 |
| coverage_turnover_summary | active coverage 0.190024; mean rank-turnover proxy 0.051569 | active coverage 0.261458; mean rank-turnover proxy 0.047727 |
| lifecycle_evidence_references | validation execution note; validation results review; refinement governance decision; bounded refinement master state update; validation artifact root | validation execution note; validation results review; refinement governance decision; bounded refinement master state update; validation artifact root |
| contamination_review_status | `contamination-review-pending` | `contamination-review-pending` |
| production_status | `not-production` | `not-production` |
| registration_recommendation | `REGISTER_RECOMMENDED` | `REGISTER_RECOMMENDED` |

Prepared registration metadata is manifest-only and does not update the active research registry.

## SECTION 6 - Manifest Artifacts

Optional closeout artifacts were prepared under:

`artifacts/research/project_underdog_platform_v1_closeout/`

Expected files:

- `vov_registration_preparation_manifest.csv`
- `platform_v1_closeout_manifest.json`

These files are registration-preparation artifacts only. They do not constitute active inventory registration, production registration, validation execution, IC recomputation, or governance mutation.

## SECTION 7 - Open Issues Before Full Registration

- Contamination review is still placeholder-only. Both candidates must carry `contamination-review-pending` metadata until dedicated contamination artifacts are produced and reviewed.
- Portfolio interaction has not yet been tested. Registration review should not assume live allocation compatibility or diversification benefit in a combined portfolio.
- Production engineering is not authorized. No production job, live scoring path, alerting, or model deployment should be inferred from this closeout.
- Live monitoring is not established. Monitoring design should be a separate post-registration or production-readiness workstream.
- PIT metadata remains externally blocked. Platform v1 closes with PIT-aware governance discipline in place, but without resolving external PIT source dependencies.

## SECTION 8 - Recommended Next Steps

1. Run a candidate registration review for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`.
2. Prepare a git milestone commit and tag for Project Underdog Platform v1 closeout after registration-review materials are accepted.
3. Begin Dispersion Path-Dependence as the next research module, using the approved standard lifecycle and keeping `dpath_*` work isolated from VoV registration decisions.

## SECTION 9 - Guardrail Confirmation

This closeout did not:

- modify the active research registry;
- promote any candidate to production;
- execute validation;
- recompute IC;
- regenerate panels;
- modify formulas;
- change thresholds;
- introduce ML;
- alter prior governance decisions.

## SECTION 10 - Final Classification

Final classification: `PLATFORM_V1_CLOSED_READY_FOR_REGISTRATION_REVIEW`

Project Underdog Platform v1 is closed with two validated VoV candidates prepared for registration review and with explicit open issues carried forward as registration metadata.
