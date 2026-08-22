# Project Underdog - Event Clustering IC Discovery v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 8 - IC Discovery

Classification: `IC_DISCOVERY_COMPLETE`

Recommendation: `ADVANCE_TO_RESEARCH_REVIEW`

Scope: IC Discovery using only the audited Event Clustering panel snapshot.

This lifecycle note records IC evidence only. It does not regenerate panels, implement formulas, refine candidates, run research validation, modify governance, change production files, change thresholds, introduce ML, add candidates, or alter the audited panel snapshot.

## SECTION 1 - Inputs

Approved inputs:

- `artifacts/research/event_clustering_research_module_v1/panel_v1/`
- `docs/research_notes/event_clustering_panel_audit_v1.md`

Audited candidate scope:

- `ecluster_01_concentrated_absorption`
- `ecluster_02_aligned_pressure_resolution`
- `ecluster_03_fragmented_event_absorption`
- `ecluster_04_deteriorating_cluster_avoidance`
- `ecluster_05_aging_cluster_memory`

No additional Event Clustering, VoV, Dispersion Path-Dependence, refinement, parked, validation, governance, production, threshold, or ML candidates were used.

## SECTION 2 - Artifacts Created

Artifact root:

- `artifacts/research/event_clustering_research_module_v1/ic_discovery_v1/`

Generated IC Discovery artifacts:

- `daily_ic.csv`
- `candidate_ic_summary.csv`
- `candidate_horizon_summary.csv`
- `candidate_rankings.csv`
- `rolling_stability_summary.csv`
- `ic_discovery_manifest.json`

Total daily IC rows:

- 41,960

The IC manifest records input SHA-256 checksums for the audited panel manifest, panel generation manifest, approved panel parquets, approved audit note, and close-price source.

## SECTION 3 - Methodology

Standard Project Underdog IC metrics were computed for:

- `h1`
- `h5`
- `h10`
- `h20`

Metrics generated:

- daily cross-sectional rank IC;
- mean IC;
- IC IR;
- positive IC rate;
- rolling stability summaries for 63, 126, and 252 trading-day windows;
- candidate ranking;
- horizon ranking;
- expected primary horizon versus observed strongest horizon consistency.

Forward returns were computed from close prices after the signal date, consistent with the audited after-close timing policy.

Mechanical recommendation thresholds:

- `ADVANCE_TO_RESEARCH_REVIEW`: expected-primary mean IC >= 0.005, IC IR >= 0.030, positive IC rate >= 0.530, and coverage ratio >= 0.300.
- `WATCH`: expected-primary mean IC > 0, positive IC rate >= 0.500, and coverage ratio >= 0.250.
- `PARK`: activation rate below 0.020, or positive best-any evidence that does not meet expected-primary WATCH criteria.
- `REJECT`: no predefined advance, watch, or park evidence.

No manual promotion was applied.

## SECTION 4 - Candidate Rankings

| rank | candidate_id | expected primary | observed strongest | expected-primary mean IC | expected-primary IC IR | positive IC rate | best-any mean IC | recommendation |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `ecluster_02_aligned_pressure_resolution` | h10 | h1 | -0.004602 | -0.059535 | 0.474906 | -0.000285 | `REJECT` |
| 2 | `ecluster_03_fragmented_event_absorption` | h5 | h1 | -0.006978 | -0.095080 | 0.476244 | -0.002812 | `REJECT` |
| 3 | `ecluster_04_deteriorating_cluster_avoidance` | h5 | h1 | -0.008526 | -0.078322 | 0.465738 | -0.005733 | `REJECT` |
| 4 | `ecluster_05_aging_cluster_memory` | h10 | h1 | -0.009069 | -0.090786 | 0.457278 | -0.001604 | `REJECT` |
| 5 | `ecluster_01_concentrated_absorption` | h10 | h1 | -0.010535 | -0.085312 | 0.454848 | -0.005969 | `REJECT` |

All candidates were mechanically rejected.

## SECTION 5 - Best Horizon Results

Best `h5`:

- `ecluster_02_aligned_pressure_resolution`
- mean IC: -0.003024
- IC IR: -0.039403
- positive IC rate: 0.487313

Best `h10`:

- `ecluster_02_aligned_pressure_resolution`
- mean IC: -0.004602
- IC IR: -0.059535
- positive IC rate: 0.474906

Best `h20`:

- `ecluster_02_aligned_pressure_resolution`
- mean IC: -0.005290
- IC IR: -0.071074
- positive IC rate: 0.477376

Best `h1`:

- `ecluster_02_aligned_pressure_resolution`
- mean IC: -0.000285
- IC IR: -0.003574
- positive IC rate: 0.507440

The strongest horizon for every candidate was `h1`, but the best `h1` mean IC was still negative and did not support promotion.

## SECTION 6 - Scientific Surprises

Primary surprise:

- The expected primary horizons did not hold. Every candidate's observed strongest horizon was `h1`, while the frozen scientific expectations were `h5` or `h10`.

Secondary surprise:

- No candidate produced positive mean IC at its expected primary horizon.

Mechanism-level implication:

- Event Alignment And Fragmentation was the least negative mechanism family in this pass, led by `ecluster_02_aligned_pressure_resolution`, but it still failed all predefined advance and watch criteria.

Contamination implication:

- The IC pass did not produce enough positive evidence to justify a deeper contamination attribution claim. Contamination metadata was preserved for future Research Review, but no candidate advanced to validation or production analysis.

## SECTION 7 - Recommendations

| candidate_id | recommendation | rationale |
| --- | --- | --- |
| `ecluster_01_concentrated_absorption` | `REJECT` | Expected-primary h10 mean IC was negative and positive IC rate was below WATCH criteria. |
| `ecluster_02_aligned_pressure_resolution` | `REJECT` | Best-ranked candidate, but expected-primary h10 mean IC and IC IR were negative. |
| `ecluster_03_fragmented_event_absorption` | `REJECT` | Expected-primary h5 mean IC was negative and observed strongest horizon was h1. |
| `ecluster_04_deteriorating_cluster_avoidance` | `REJECT` | Expected-primary h5 mean IC was negative and positive IC rate was below WATCH criteria. |
| `ecluster_05_aging_cluster_memory` | `REJECT` | Expected-primary h10 mean IC was negative and horizon consistency failed. |

No candidate is recommended for direct validation, governance mutation, production registration, threshold change, refinement, or ML.

## SECTION 8 - Verification

Commands run:

- `python -m py_compile pipelines/run_event_clustering_ic_discovery_v1.py tests/test_event_clustering_ic_discovery_v1.py`
- `python -m py_compile pipelines/event_clustering_research_module_v1.py pipelines/run_event_clustering_panel_generation_v1.py pipelines/run_event_clustering_ic_discovery_v1.py tests/test_event_clustering_research_module_v1.py tests/test_event_clustering_panel_generation_v1.py tests/test_event_clustering_ic_discovery_v1.py`
- `python pipelines/run_event_clustering_ic_discovery_v1.py`
- `pytest -q tests/test_event_clustering_ic_discovery_v1.py tests/test_event_clustering_panel_generation_v1.py tests/test_event_clustering_research_module_v1.py tests/test_registry_validation.py`
- independent SHA-256 checksum recomputation against `panel_generation_manifest.json`
- IC artifact inventory scan

Results:

- Python compilation passed.
- IC Discovery runner completed and wrote the six requested artifacts.
- Focused IC, panel-generation regression, implementation regression, and registry/scaffold tests passed: 28 passed.
- Panel checksum reconciliation passed: 7 records, 0 mismatches.
- IC artifact inventory contains only the six requested IC Discovery artifacts.

Warnings:

- NumPy emitted divide-by-zero/invalid-value warnings for constant rank vectors on some daily cross-sections. The IC scorer records those cases as missing IC where applicable; this did not block scoring or artifact generation.
- Local Arrow emitted CPU sysctl warnings during parquet reads in this sandbox. These are environmental warnings and did not affect artifact output.

## SECTION 9 - Guardrails

Confirmed:

- Only the audited Event Clustering panel snapshot was used.
- Exactly five approved candidates were scored.
- No panels were regenerated.
- No panel files were modified.
- No formulas were changed.
- No refinement was performed.
- No research validation artifacts were generated.
- No governance files were changed.
- No production files were changed.
- No thresholds were changed.
- No ML was introduced.

## SECTION 10 - Classification

Classification: `IC_DISCOVERY_COMPLETE`

Rationale:

- Required IC artifacts were generated.
- Standard IC metrics were computed across h1, h5, h10, and h20.
- Candidate and horizon rankings were produced.
- Mechanical recommendations were assigned.
- All candidates failed predefined IC evidence thresholds and were assigned `REJECT`.

## SECTION 11 - Recommended Next Lifecycle Phase

Recommended next lifecycle phase:

- Event Clustering Research Review v1.

The Research Review should adjudicate the Phase 8 IC evidence and close or archive the rejected candidate set unless a separately approved future lifecycle authorizes a new bounded research question. IC Discovery does not authorize validation, governance mutation, production registration, threshold changes, refinement, or ML.
