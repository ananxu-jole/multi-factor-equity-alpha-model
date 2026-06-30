# Project Underdog - OHLCV Volatility-of-Volatility Research Module Implementation v1

## SECTION 1 - Executive Summary

This note documents the implementation of the Family A Volatility-of-Volatility research module from:

`docs/research_notes/ohlcv_vov_dpd_event_clustering_formula_and_panel_specification_v1.md`

Classification: `IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`.

Implemented module:

- `pipelines/ohlcv_volatility_of_volatility_research_module_v1.py`

Focused tests:

- `tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`

Scope boundary:

- Implemented only Family A: Volatility-of-Volatility.
- Implemented exactly five candidates: `vov_01`, `vov_02`, `vov_03`, `vov_04`, and `vov_05`.
- Family B Dispersion Path-Dependence remains frozen.
- Family C Event Clustering remains frozen.
- No panel artifacts were generated.
- No IC, discovery, redundancy screening, refinement, validation, governance mutation, production change, threshold change, or ML work was performed.

## SECTION 2 - Implemented Candidate List

| candidate_id | signal_name | primary horizon | formula status |
| --- | --- | --- | --- |
| `vov_01` | `vov_01_instability_calm_after_chop` | h10 | Implemented as registry-derived formula function. |
| `vov_02` | `vov_02_low_extension_vov_rise` | h10 | Implemented as registry-derived formula function. |
| `vov_03` | `vov_03_range_chop_exhaustion` | h10 | Implemented as registry-derived formula function. |
| `vov_04` | `vov_04_vov_slope_divergence` | h10 | Implemented as registry-derived formula function. |
| `vov_05` | `vov_05_churn_controlled_vov_stabilization` | h10 | Implemented as registry-derived formula function. |

No `dpath_*` or `ecluster_*` candidates were implemented.

## SECTION 3 - Formula Summary

The module implements the five approved formulas from the specification using in-memory pandas operations:

- `vov_01`: calming volatility-of-volatility after elevated chop and low extension.
- `vov_02`: rising volatility-of-volatility with low extension and dollar-volume support.
- `vov_03`: range-chop exhaustion with low extension.
- `vov_04`: divergence between volatility-level slope and volatility-of-volatility slope.
- `vov_05`: volatility-of-volatility stabilization with low rank churn.

Final candidate scores use same-date cross-sectional percentile ranking and preserve h10 as the primary horizon for all five candidates.

## SECTION 4 - Implementation Assumptions

Assumptions:

- Input data are existing project-standard OHLCV rows with `date`, `ticker`, `open`, `high`, `low`, `close`, and `volume`.
- Signal values use data available through signal date `t`.
- Forward-return alignment is intentionally not implemented here because this module does not compute IC.
- Cross-sectional ranking requires a configurable finite-count minimum, defaulting to 50 names per date.
- Missing rolling features remain missing and are not backfilled.
- Inactive formula states are neutralized only where the candidate formula requires activation handling.
- Same-bar timing remains a future execution-review item because formulas use close/high/low/volume through date `t`.

## SECTION 5 - Supported Rolling Features

Implemented derived features:

- `ret_1`, `ret_5`, `ret_10`, `ret_20`
- `abs_ret_1`
- `range_1`
- `dollar_volume`
- `vol_5`, `vol_10`, `vol_20`
- `vov_5_20`, `vov_10_40`
- `vov_slope_5`, `vov_slope_10`
- `range_chop_20`, `range_chop_slope_5`
- `low_extension_20`
- `rank_churn_5`, `low_churn_5`

Supported module outputs:

- candidate registry;
- registry validation;
- derived feature frame;
- in-memory expected candidate panel schema;
- in-memory candidate panel construction function for later runner use;
- guardrail manifest dictionary confirming no execution path was taken.

## SECTION 6 - Registry And Schema Checks

Registry checks enforce:

- exactly five implemented candidates;
- candidate ids must equal `vov_01` through `vov_05`;
- all candidates must use `family = volatility_of_volatility`;
- all candidates must use `research_status = RESEARCH_ONLY`;
- all candidates must preserve h10 as primary horizon;
- `dpath_*` and `ecluster_*` candidate ids are blocked.

Panel schema support includes:

- `date`
- `ticker`
- shared diagnostic rolling features
- `{candidate_id}_raw_score`
- `{candidate_id}_signal`
- `{candidate_id}_active`
- `{candidate_id}_family`
- `{candidate_id}_primary_horizon`
- `{candidate_id}_missing_reason`

## SECTION 7 - Tests Added

Focused tests added:

- registry contains exactly Family A candidates;
- registry rejects attempted Dispersion/Event candidates;
- in-memory panel has expected schema;
- no Family B or Family C panel columns are produced;
- warmup and missing data remain missing rather than backfilled;
- `vov_04` formula matches the frozen specification on a synthetic panel;
- guardrail manifest confirms no panel generation, IC, discovery, redundancy screening, refinement, validation, governance, production, threshold, or ML execution;
- input schema enforcement rejects missing OHLCV columns.

## SECTION 8 - Verification Summary

Commands run:

- `python -m py_compile pipelines/ohlcv_volatility_of_volatility_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`
- `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py -q`
- `python -m pytest tests/test_rank_coherence_discovery_scaffold.py -q`
- `python -m pytest tests/test_registry_validation.py -q`

Results:

- VoV focused tests: 7 passed.
- Rank-coherence scaffold regression tests: 3 passed.
- Generic registry validation tests: 5 passed.
- Python compile check passed.

Full suite:

- Not run. Several existing tests are panel-generation or broader research-flow tests; running them would be inappropriate for this module task's no-panel-generation guardrail.

## SECTION 9 - Remaining Work

Before module review:

- Review whether short candidate ids `vov_01` through `vov_05` should remain canonical in code while preserving full `source_spec_id` values from the specification.
- Confirm whether future execution should output wide or long candidate panels.
- Confirm same-bar timing convention before any production-adjacent review.
- Confirm whether candidate panel generation should live in a separate runner task.

Before discovery:

- Implement only an explicitly approved runner or scaffold.
- Add artifact writing only under a future execution task.
- Add IC scoring only under a future discovery task.
- Add redundancy and contamination screening only under the approved discovery/review task.

## SECTION 10 - Explicit Non-Goals

This implementation did not:

- implement Family B Dispersion Path-Dependence;
- implement Family C Event Clustering;
- generate panels;
- compute IC;
- perform discovery;
- perform redundancy screening;
- perform refinement;
- perform validation;
- modify governance;
- modify production registry;
- change thresholds;
- introduce ML;
- access external data;
- use PIT metadata.
