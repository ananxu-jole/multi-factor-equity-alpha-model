# Project Underdog - Event Clustering Formula Implementation Review v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 4 - Formula Implementation Review

Classification: `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`

Recommendation: `ADVANCE_TO_PANEL_SPECIFICATION`

Scope: independent review of the completed Event Clustering implementation before panel specification or panel generation.

This is a review-only lifecycle note. It does not recreate the research module design, recreate the formula and panel specification, generate panels, compute IC, run validation, modify governance, change production files, change thresholds, introduce ML, expand candidates, or add mechanisms.

## SECTION 1 - Materials Reviewed

Implementation artifacts reviewed:

- `pipelines/event_clustering_research_module_v1.py`
- `tests/test_event_clustering_research_module_v1.py`
- `docs/research_notes/event_clustering_formula_implementation_v1.md`

Cross-check references:

- `docs/research_notes/event_clustering_formula_and_panel_specification_v1.md`
- `docs/research_notes/event_clustering_research_module_design_v1.md`
- `docs/research_notes/event_clustering_scientific_review_v1.md`

## SECTION 2 - Review Findings

### Finding 1 - Approved Candidate Set Preserved

Status: PASS.

The implementation contains exactly five Event Clustering candidates:

- `ecluster_01_concentrated_absorption`
- `ecluster_02_aligned_pressure_resolution`
- `ecluster_03_fragmented_event_absorption`
- `ecluster_04_deteriorating_cluster_avoidance`
- `ecluster_05_aging_cluster_memory`

No additional `ecluster_*` candidates were found.

### Finding 2 - Foreign Candidate Guardrails Preserved

Status: PASS.

No VoV, DPath, refinement, validation, production, or ML candidates are implemented in the Event Clustering module. Registry validation rejects foreign candidate IDs and extra Event Clustering IDs.

### Finding 3 - Formula Drift Found And Corrected

Status: FIXED.

The review found one implementation/specification drift:

- Frozen specification: `price_event = 1 if abs(z_ts(ret_1, 60)) >= 1.5`.
- Frozen specification: `gap_event = 1 if abs(z_ts(gap_1, 60)) >= 1.5`.
- Original implementation computed z-scores of absolute values for these two event flags.

Fix applied:

- `price_event` now uses `abs(z_ts(ret_1, 60)) >= 1.5`.
- `gap_event` now uses `abs(z_ts(gap_1, 60)) >= 1.5`.
- A focused test now independently recomputes the frozen event semantics.

This was a small review fix because it corrected formula drift without reinterpreting the formula, changing candidate count, adding mechanisms, or expanding scope.

### Finding 4 - Epsilon Denominator Guard Corrected

Status: FIXED.

The frozen specification defines `close_loc_1` using a guarded denominator. The implementation now applies an explicit epsilon lower bound to the high-low denominator before computing `close_loc_1`.

This was a small implementation/specification alignment fix and does not change candidate design.

### Finding 5 - Candidate Formulas And Activations Match Specification

Status: PASS AFTER FIX.

All five candidate formulas and activation conditions now match the frozen specification. Focused tests recompute every candidate formula and activation condition from exposed feature fields and compare them with panel-compatible implementation output.

### Finding 6 - Scientific And Mechanism Metadata Preserved

Status: PASS.

The implementation preserves:

- module id;
- specification id;
- candidate names;
- approved mechanism labels;
- scientific questions;
- expected evidence;
- expected sign;
- primary horizon metadata;
- secondary horizon metadata;
- research-only status;
- formula text;
- activation text.

### Finding 7 - Contamination And Anchor Metadata Preserved

Status: PASS.

The implementation preserves required contamination metadata for:

- VoV;
- volatility compression;
- hostile/stress repair;
- volume shock reversal;
- rank coherence;
- persistence;
- dispersion path-dependence;
- non-hostile transition;
- static dispersion;
- isolated-event anchors.

Static event anchors, isolated-event anchor fields, anchor-comparator metadata, and diagnostic contamination fields are present in the long-form compatible output surface.

### Finding 8 - Warmup, Missing Data, And Inactive Neutralization

Status: PASS.

Warmup handling is explicit and conservative. Rows before feature maturity produce null signal values with `rolling_warmup` where applicable. Raw OHLCV defects produce controlled missing reasons. Inactive but otherwise mature rows are neutralized to `0.5` and labeled `inactive_neutralized`.

### Finding 9 - Timing And Long-Form Compatibility

Status: PASS.

After-close timing metadata is preserved as `after_close_t_forward_returns_after_t`. The output surface is long-form compatible with one row per `date`, `ticker`, and `candidate_id`, and includes lineage, activation, missing-data, signal, anchor, diagnostic, and contamination fields.

### Finding 10 - Test Adequacy

Status: PASS WITH NOTES.

Tests adequately detect:

- formula drift;
- activation drift;
- registry drift;
- lineage drift;
- guardrail violations;
- foreign candidate leakage;
- missing-data regressions;
- inactive neutralization regressions;
- event definition drift for price and gap event flags.

Notes:

- Tests use synthetic OHLCV data and implementation-level recomputation. They do not constitute panel audit, IC discovery, validation, or empirical evidence.
- Future panel audit should independently inspect generated artifacts and manifest checksums once panel generation is authorized.

### Finding 11 - No Unauthorized Execution Paths

Status: PASS.

No panel generation path, IC logic, validation logic, governance logic, production logic, threshold tuning, or ML integration was found. The module exposes a panel-compatible builder for future authorized phases, but no artifact-writing behavior is present.

The artifact check found no Event Clustering research artifact root.

## SECTION 3 - Review Checklist

| item | status |
| --- | --- |
| Exactly five approved Event Clustering candidates are implemented. | PASS |
| No additional Event Clustering candidates exist. | PASS |
| No VoV, DPath, refinement, or foreign candidates appear. | PASS |
| Every implemented formula matches the frozen specification. | PASS AFTER FIX |
| Every activation condition matches the frozen specification. | PASS |
| Scientific lineage metadata is preserved. | PASS |
| Mechanism metadata is preserved. | PASS |
| Expected horizon metadata is preserved. | PASS |
| Contamination metadata is preserved. | PASS |
| Isolated-event anchor metadata is preserved. | PASS |
| Warmup handling is correct. | PASS |
| Missing-data handling is correct. | PASS |
| Inactive neutralization is correct. | PASS |
| After-close timing metadata is correct. | PASS |
| Long-form panel compatibility is preserved. | PASS |
| Registry validation is meaningful. | PASS |
| Tests detect formula drift. | PASS |
| Tests detect activation drift. | PASS |
| Tests detect registry drift. | PASS |
| Tests detect lineage drift. | PASS |
| Tests detect guardrail violations. | PASS |
| No panel generation paths exist. | PASS |
| No IC logic exists. | PASS |
| No validation logic exists. | PASS |
| No governance logic exists. | PASS |
| No production logic exists. | PASS |
| No threshold tuning exists. | PASS |
| No ML exists. | PASS |

## SECTION 4 - Fixes Made During Review

Files changed during review:

- `pipelines/event_clustering_research_module_v1.py`
- `tests/test_event_clustering_research_module_v1.py`
- `docs/research_notes/event_clustering_formula_implementation_review_v1.md`

Fixes:

1. Corrected `price_event` to use absolute z-score of return, not z-score of absolute return.
2. Corrected `gap_event` to use absolute z-score of gap, not z-score of absolute gap.
3. Added explicit epsilon denominator guard for `close_loc_1`.
4. Added a focused test that independently verifies price and gap event semantics against the frozen specification.

No formulas were reinterpreted. No candidates, mechanisms, panel generation, IC, validation, governance, production, threshold, or ML logic were added.

## SECTION 5 - Verification Results

Commands run:

- `python -m py_compile pipelines/event_clustering_research_module_v1.py tests/test_event_clustering_research_module_v1.py`
- `pytest -q tests/test_event_clustering_research_module_v1.py`
- `pytest -q tests/test_event_clustering_research_module_v1.py tests/test_registry_validation.py tests/test_dispersion_path_dependence_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`

Results:

- Python compilation passed.
- Focused Event Clustering implementation tests passed: 13 passed.
- Registry/scaffold and adjacent regression tests passed: 36 passed.
- Artifact check: `artifacts/research/event_clustering_research_module_v1` does not exist, confirming no Event Clustering panel or IC artifacts were created.

## SECTION 6 - Remaining Notes

The implementation is review-approved for panel specification, not for panel generation, IC discovery, validation, governance, production registration, threshold changes, or ML.

Remaining risks to carry forward:

- empirical activation adequacy remains unknown until authorized panel generation and panel audit;
- contamination risk remains high against volume shock reversal, hostile/stress repair, VoV, volatility compression, rank coherence, persistence, dispersion behavior, and isolated-event anchors;
- long-form compatibility is implementation-level only until generated panel artifacts are audited.

## SECTION 7 - Classification

Classification: `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`

Rationale:

- A real formula drift was found and corrected within review scope.
- After the correction, the implementation matches the frozen candidate set, formulas, activations, metadata, timing policy, anchors, contamination requirements, warmup semantics, missing-data semantics, and registry guardrails.
- Focused and relevant regression tests pass.
- Notes remain because no panel artifact has been generated or audited, and empirical contamination cannot be assessed in this phase.

## SECTION 8 - Final Recommendation

Recommended next lifecycle phase:

- Event Clustering Panel Specification v1.

The Event Clustering implementation is ready for Panel Specification. It is not authorized for panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
