# Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Governance Decision v1

## SECTION 1 - Governance Objective

This note records the official governance decision for the completed bounded OHLCV Volatility-of-Volatility refinement research module.

Current input classification:

- `VALIDATION_DESIGN_APPROVED`

Governance classification:

- `REFINEMENT_GOVERNANCE_APPROVED`

This governance decision authorizes validation-design work only. It does not execute validation, recompute IC, regenerate panels, modify formulas, change governance thresholds, modify production registry entries, or introduce ML.

## SECTION 2 - Inputs Reviewed

Reviewed inputs:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_research_review_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_ic_discovery_v1.md`

Evidence reviewed:

- Bounded refinement IC discovery classification: `REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`.
- Bounded refinement research review classification: `VALIDATION_DESIGN_APPROVED`.
- Approved panel lineage: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`.
- IC discovery evidence: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`.

## SECTION 3 - Official Candidate Decisions

Official refinement governance outcomes:

| candidate_id | official outcome | authorized use |
| --- | --- | --- |
| `vov_03_ref_strict_chop` | VALIDATION_DESIGN_APPROVED | Validation-design target. |
| `vov_01_ref_smoothed_calm` | VALIDATION_DESIGN_APPROVED | Validation-design target. |
| `vov_01_ref_anchor` | BASELINE_COMPARATOR | Comparator only. |
| `vov_03_ref_anchor` | BASELINE_COMPARATOR | Comparator only. |
| `vov_01_ref_longer_memory` | WATCH | Archive and monitor; no validation-design work authorized. |
| `vov_01_ref_strict_calm` | PARK | Archive evidence; no further work authorized. |
| `vov_03_ref_longer_chop` | PARK | Archive evidence; no further work authorized. |
| `vov_03_ref_extension_controlled` | PARK | Archive evidence; no further work authorized. |

## SECTION 4 - Authorized Validation-Design Targets

Validation-design work is authorized only for:

- `vov_03_ref_strict_chop`
- `vov_01_ref_smoothed_calm`

Rationale:

- `vov_03_ref_strict_chop` produced the strongest vov_03 branch improvement, with h10 mean IC of 0.012030, h10 IC IR of 0.102764, h10 positive IC rate of 0.549903, and h10 mean IC improvement of 0.003826 versus `vov_03_ref_anchor`.
- `vov_01_ref_smoothed_calm` produced the cleanest vov_01 branch improvement, with h20 mean IC of 0.011976, h20 IC IR of 0.107079, h20 positive IC rate of 0.540303, and h20 mean IC improvement of 0.001571 versus `vov_01_ref_anchor`.

Validation-design scope should include:

- h10/h20 persistence checks;
- time-window and rolling IC stability checks;
- redundancy versus original VoV anchors;
- volatility-compression contamination checks;
- hostile/stress-repair contamination checks;
- persistence/rank-stability contamination checks;
- plain-reversal and volume-shock reversal contamination checks;
- relationship to watch-only `vov_05` behavior;
- sensitivity to inactive neutralization and warmup handling.

## SECTION 5 - Baseline Comparator Policy

Baseline comparators:

- `vov_01_ref_anchor`
- `vov_03_ref_anchor`

Comparator policy:

- Anchors may be included in validation-design review only as branch baselines.
- Anchors are not the preferred refined candidates.
- Anchors must not be promoted, validated, or production-registered from this governance note.
- Anchor evidence should be used to measure whether the approved refinement targets preserve or improve the original approved mechanisms.

## SECTION 6 - Watch And Park Decisions

WATCH:

- `vov_01_ref_longer_memory`

Watch rationale:

- It had the highest h20 mean IC in the refinement batch, but its h20 positive IC rate was only 0.510154 and trailed the vov_01 anchor by 0.025230.
- It may be more exposed to longer-memory VoV stabilization or `vov_05`-like behavior.
- It is not authorized for validation-design work.

PARK:

- `vov_01_ref_strict_calm`
- `vov_03_ref_longer_chop`
- `vov_03_ref_extension_controlled`

Park rationale:

- `vov_01_ref_strict_calm` was too close to the vov_01 anchor in mean IC improvement.
- `vov_03_ref_longer_chop` improved h20 but weakened the h10 primary mechanism versus anchor.
- `vov_03_ref_extension_controlled` did not improve the primary-horizon anchor comparison.

Parked variants should remain archived as research evidence but should not receive additional refinement, validation-design work, validation execution, or production consideration without a separate governance override.

## SECTION 7 - Non-Authorized Work

This governance decision does not authorize:

- additional refinement cycles;
- validation execution;
- validation-design work for `vov_01_ref_longer_memory`;
- validation-design work for `vov_01_ref_strict_calm`;
- validation-design work for `vov_03_ref_longer_chop`;
- validation-design work for `vov_03_ref_extension_controlled`;
- production registration;
- formula modification;
- panel regeneration;
- IC recomputation;
- governance threshold changes;
- ML introduction.

## SECTION 8 - Archived Refinement Evidence

Archived evidence roots:

- Panel artifacts: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
- IC discovery artifacts: `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

Archived notes:

- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_formula_and_panel_specification_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_panel_audit_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_ic_discovery_v1.md`
- `docs/research_notes/ohlcv_volatility_of_volatility_bounded_refinement_research_review_v1.md`

Evidence retention policy:

- Keep all panels, manifests, IC outputs, rolling diagnostics, and review notes as research evidence.
- Do not overwrite approved panel or IC artifacts during validation-design work.
- Any future validation-design artifact should reference these roots rather than mutate them.

## SECTION 9 - Explicit Non-Goals

This governance decision does not:

- run validation;
- recompute IC;
- regenerate panels;
- modify formulas;
- change governance thresholds;
- modify production registry entries;
- introduce ML;
- authorize another refinement cycle;
- promote any candidate to production.

## SECTION 10 - Recommended Master State Update

Recommended next task:

**Project Underdog - OHLCV Volatility-of-Volatility Bounded Refinement Master State Update v1**

The master state update should record:

- bounded refinement governance classification: `REFINEMENT_GOVERNANCE_APPROVED`;
- validation-design approved targets: `vov_03_ref_strict_chop`, `vov_01_ref_smoothed_calm`;
- baseline comparators: `vov_01_ref_anchor`, `vov_03_ref_anchor`;
- watch variant: `vov_01_ref_longer_memory`;
- parked variants: `vov_01_ref_strict_calm`, `vov_03_ref_longer_chop`, `vov_03_ref_extension_controlled`;
- evidence archive references for panel and IC artifacts;
- explicit note that no validation execution, production registration, threshold change, or ML work has occurred.

## SECTION 11 - Verification Summary

Verification performed:

- Confirmed research review classification: `VALIDATION_DESIGN_APPROVED`.
- Confirmed official decisions match the requested governance outcomes.
- Confirmed no implementation files were changed.
- Confirmed no panel files were changed.
- Confirmed no IC artifact files were changed.
- Confirmed no validation was executed.
- Confirmed no production files were changed.
- Confirmed no governance thresholds were changed.
- Confirmed no ML files were changed.

Final classification:

- `REFINEMENT_GOVERNANCE_APPROVED`
