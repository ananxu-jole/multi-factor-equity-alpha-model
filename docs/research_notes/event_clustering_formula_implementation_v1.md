# Project Underdog - Event Clustering Formula Implementation v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 3 - Formula Implementation

Classification: `IMPLEMENTATION_READY_WITH_NOTES`

Recommendation: `ADVANCE_TO_IMPLEMENTATION_REVIEW`

Scope: implementation of exactly the five Event Clustering candidates frozen in `docs/research_notes/event_clustering_formula_and_panel_specification_v1.md`.

This note does not recreate the formula and panel specification. It does not generate panels, compute IC, run validation, modify governance, change production files, change thresholds, introduce ML, add mechanisms, add candidates, or reinterpret formulas.

## SECTION 1 - Inputs

Reviewed inputs:

- `docs/research_notes/event_clustering_formula_and_panel_specification_v1.md`
- `docs/research_notes/event_clustering_research_module_design_v1.md`
- `docs/research_notes/event_clustering_scientific_review_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`

Current approved input classification:

- `FORMULA_SPEC_READY_WITH_NOTES`

## SECTION 2 - Files Created

Created:

- `pipelines/event_clustering_research_module_v1.py`
- `tests/test_event_clustering_research_module_v1.py`
- `docs/research_notes/event_clustering_formula_implementation_v1.md`

No panel, IC, validation, governance, production, threshold, or ML artifacts were created.

## SECTION 3 - Implemented Candidates

Exactly five Event Clustering candidates were implemented:

| candidate_id | candidate_name | mechanism | primary horizon | expected sign |
| --- | --- | --- | --- | --- |
| `ecluster_01_concentrated_absorption` | Concentrated Event Absorption | Event Concentration | h10 | positive |
| `ecluster_02_aligned_pressure_resolution` | Aligned Event Pressure Resolution | Event Alignment And Fragmentation | h10 | positive |
| `ecluster_03_fragmented_event_absorption` | Fragmented Event Absorption | Event Alignment And Fragmentation | h5 | positive |
| `ecluster_04_deteriorating_cluster_avoidance` | Deteriorating Cluster Avoidance | Cluster Absorption Versus Deterioration | h5 | positive |
| `ecluster_05_aging_cluster_memory` | Aging Cluster Memory | Cluster Aging And Market Memory | h10 | positive |

Not implemented:

- additional `ecluster_*` candidates;
- `dpath_*` candidates;
- `vov_*` candidates;
- refinement variants;
- validation logic;
- production logic;
- ML.

## SECTION 4 - Implementation Summary

The implementation adds a research-only pipeline module with:

- exact frozen formula text in candidate metadata;
- scientific lineage metadata;
- mechanism metadata;
- candidate metadata;
- contamination metadata;
- OHLCV-derived event and cluster features;
- isolated-event anchor fields;
- static event anchor fields;
- warmup handling;
- missing-data handling;
- activation semantics;
- after-close timing metadata;
- long-form panel compatibility;
- registry/spec consistency checks;
- a guardrail manifest confirming no research execution phase was run.

Public implementation entry points:

- `candidate_registry()`
- `validate_event_clustering_registry()`
- `compute_event_clustering_features()`
- `build_event_clustering_candidate_panel()`
- `expected_panel_columns()`
- `implemented_candidate_ids()`
- `module_guardrail_manifest()`

The panel builder is an implementation surface only. This lifecycle phase did not call it to create files or artifacts.

## SECTION 5 - Scientific Lineage Preservation

The implementation preserves:

- module id: `event_clustering_research_module_v1`;
- specification id: `event_clustering_formula_and_panel_specification_v1`;
- research status: `RESEARCH_ONLY`;
- timing policy: `after_close_t_forward_returns_after_t`;
- approved mechanism labels;
- h5/h10 primary horizon assignments;
- h20 durability-only secondary horizon metadata;
- expected positive sign;
- required contamination controls;
- required static and isolated-event anchor metadata;
- formula and activation text from the frozen specification.

## SECTION 6 - Guardrail Confirmation

The implementation guardrail manifest reports:

- exactly five implemented candidates;
- no extra Event Clustering candidates;
- no DPath candidates;
- no VoV candidates;
- no refinement variants;
- no panel generation;
- no IC scoring;
- no validation;
- no governance mutation;
- no production registration;
- no threshold changes;
- no ML integration.

## SECTION 7 - Tests Added

Focused tests were added in `tests/test_event_clustering_research_module_v1.py`.

Coverage includes:

- exact five-candidate registry enforcement;
- rejection of extra or foreign candidates;
- long-form panel schema compatibility;
- after-close timing metadata;
- scientific lineage and contamination metadata;
- warmup handling;
- raw missing-data handling;
- inactive neutralization;
- exact formula and activation recomputation for all five candidates;
- anchor and cluster-age feature exposure;
- guardrail manifest checks;
- input schema enforcement.

## SECTION 8 - Verification Results

Commands run:

- `python -m py_compile pipelines/event_clustering_research_module_v1.py`
- `python -m py_compile pipelines/event_clustering_research_module_v1.py tests/test_event_clustering_research_module_v1.py`
- `pytest -q tests/test_event_clustering_research_module_v1.py`
- `pytest -q tests/test_event_clustering_research_module_v1.py tests/test_registry_validation.py tests/test_dispersion_path_dependence_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`

Results:

- Python compilation passed.
- Focused Event Clustering implementation tests passed: 12 passed.
- Registry/scaffold and adjacent Platform v2 module guardrail tests passed: 35 passed.
- Artifact check confirmed no Event Clustering research artifact root was created.

## SECTION 9 - Remaining Risks

Remaining implementation-review risks:

- The formula specification carries high contamination risk from volume shock reversal, hostile/stress repair, VoV, volatility compression, rank coherence, persistence, dispersion behavior, and isolated-event anchors.
- Event z-score thresholds and activation semantics are implemented exactly as specified, but empirical activation adequacy is unknown until later panel generation and audit.
- The implementation exposes panel-building functions, but no generated panel has been audited in this phase.
- No IC or validation evidence exists and none is claimed.

## SECTION 10 - Classification

Classification: `IMPLEMENTATION_READY_WITH_NOTES`

Rationale:

- Exactly the five frozen Event Clustering candidates are implemented.
- No unapproved candidates or mechanisms are implemented.
- Formula text, activation text, lineage, mechanisms, contamination controls, anchors, timing policy, warmup, missing-data handling, and long-form compatibility are present.
- Focused implementation tests pass.
- Notes remain because formal implementation review and future panel audit have not yet occurred.

## SECTION 11 - Verification

Confirmed:

- Exactly five Event Clustering candidates implemented.
- No extra candidates.
- No panel artifacts created.
- No IC artifacts created.
- No validation files changed.
- No governance files changed.
- No production files changed.
- No threshold files changed.
- No ML files changed.

## SECTION 12 - Final Recommendation

Recommended next lifecycle phase:

- Event Clustering Formula Implementation Review v1.

Event Clustering may advance exactly one lifecycle phase to implementation review. It may not advance directly to panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
