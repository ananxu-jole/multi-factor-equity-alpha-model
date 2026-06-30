# Project Underdog - OHLCV Volatility-of-Volatility Research Module Implementation Review v1

## SECTION 1 - Review Objective

This note performs a focused implementation review of the Volatility-of-Volatility research module before any panel writing, IC scoring, discovery execution, redundancy screening, refinement, validation, governance mutation, production registration, threshold change, or ML work.

Reviewed files:

- `pipelines/ohlcv_volatility_of_volatility_research_module_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_research_module_v1.py`
- `docs/research_notes/ohlcv_volatility_of_volatility_research_module_implementation_v1.md`
- `docs/research_notes/ohlcv_vov_dpd_event_clustering_formula_and_panel_specification_v1.md`

Current implementation classification entering review:

- `IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`

Review classification:

- `MODULE_IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`

## SECTION 2 - Readiness Conclusion

The VoV-only module is suitable to proceed to panel-specification review, subject to minor review items being resolved before any artifact-writing runner is authorized.

No blocking implementation issues were found. The module implements only the five approved Family A candidates, preserves the full formula-spec identifiers as `source_spec_id`, excludes Family B and Family C candidates, and exposes guardrail metadata confirming that panel generation, IC scoring, discovery, redundancy screening, refinement, validation, governance changes, production registration, threshold changes, and ML integration are not part of the module.

The main remaining review items are specification-level rather than code-blocking:

- Freeze activation-neutralization semantics before panel writing.
- Select canonical future panel artifact shape.
- Add broader formula drift checks before artifact-writing execution.
- Document the after-close timing assumption in the future panel manifest.

## SECTION 3 - Review Findings

| finding_id | severity | finding | disposition |
| --- | --- | --- | --- |
| `VOV_REVIEW_001` | blocking | None. The implementation scope is limited to `vov_01` through `vov_05`. | No action required. |
| `VOV_REVIEW_002` | minor | Activated candidates are neutralized by setting inactive raw scores to zero before final cross-sectional ranking. The formula specification lists activation conditions separately rather than explicitly wrapping formulas in `neutral_if_inactive`. | Confirm and freeze this semantic in the next panel specification. |
| `VOV_REVIEW_003` | minor | Tests include direct formula equivalence for `vov_04` but do not yet include direct formula equivalence tests for every candidate. | Add candidate-level formula drift tests before artifact-writing execution. |
| `VOV_REVIEW_004` | minor | Same-bar OHLCV timing is safe only under an after-close signal formation convention. | Document after-close formation and next-period return alignment in the future panel manifest. |

## SECTION 4 - Candidate Scope Review

The implementation defines exactly five canonical code candidates:

| candidate_id | source_spec_id | status |
| --- | --- | --- |
| `vov_01` | `vov_01_instability_calm_after_chop` | implemented |
| `vov_02` | `vov_02_low_extension_vov_rise` | implemented |
| `vov_03` | `vov_03_range_chop_exhaustion` | implemented |
| `vov_04` | `vov_04_vov_slope_divergence` | implemented |
| `vov_05` | `vov_05_churn_controlled_vov_stabilization` | implemented |

Family B and Family C remain unimplemented. The module blocks `dpath_` and `ecluster_` prefixes through registry consistency checks.

## SECTION 5 - Canonical ID Decision

Short IDs `vov_01` through `vov_05` are acceptable canonical code IDs.

Rationale:

- The formula specification assigned the short IDs as the executable Family A candidate namespace.
- The implementation preserves full descriptive spec lineage in `source_spec_id`.
- The registry exposes both `candidate_id` and `source_spec_id`, allowing compact code references without losing auditability.
- The tests assert that only the five short IDs are implemented and that Family B and Family C prefixes are rejected.

Decision:

- Use `candidate_id` as the canonical code ID.
- Use `source_spec_id` as the immutable formula-spec lineage reference.
- Do not rename the candidates before panel-specification work.

## SECTION 6 - Formula and Schema Review

The implementation follows the Family A scope and uses OHLCV-only derived rolling features. Required raw inputs are limited to:

- `date`
- `ticker`
- `open`
- `high`
- `low`
- `close`
- `volume`

The module derives rolling returns, rolling volatility, volatility-of-volatility measures, range-chop measures, low-extension measures, and rank-churn measures using trailing observations. No future returns or IC targets are computed.

The in-memory output schema includes:

- Identity columns: `date`, `ticker`
- Candidate signal columns: `vov_01`, `vov_02`, `vov_03`, `vov_04`, `vov_05`
- Candidate raw-score columns
- Candidate active-flag columns
- Shared diagnostic feature columns

Warmup and missing-data handling are appropriate for module review:

- Rolling features remain missing until sufficient trailing observations exist.
- Missing raw OHLCV fields propagate through derived features.
- Missing candidate raw scores remain missing in final ranked signals.
- No backfill is applied.

## SECTION 7 - Same-Bar Timing Review

The module uses OHLCV information available through bar date `t`, including `close`, `high`, `low`, and `volume`, to form signals for date `t`.

This does not introduce look-ahead under the required future execution convention:

- Signals are formed after the close of date `t`.
- Forward return labels begin after date `t`.
- No same-day intraday execution assumption is permitted.
- No future returns, future volatility, future volume, future ranks, or future universe information are used in this module.

Required panel-specification follow-up:

- The future panel manifest should state that `signal_date = t` means after-close availability on `t`.
- IC evaluation should align `h1`, `h5`, `h10`, and `h20` labels strictly after `t`.

## SECTION 8 - Panel Shape Recommendation

Recommended canonical future panel artifact shape:

- Long-form.

Recommended canonical columns:

- `date`
- `ticker`
- `candidate_id`
- `source_spec_id`
- `family`
- `primary_horizon`
- `signal_value`
- `raw_score`
- `is_active`
- `feature_warmup_complete`
- optional diagnostic feature columns or a separate diagnostics artifact

Rationale:

- Long-form panels are easier to append, partition, validate, and score across candidate families.
- Candidate metadata can travel with each signal row.
- Downstream IC, redundancy, and family summaries can group by `candidate_id` without reshaping.
- The current wide-form in-memory output is acceptable as a module-local diagnostic representation, but should not be the canonical research artifact unless a later panel spec explicitly chooses that contract.

## SECTION 9 - Blocking Issues

No blocking issues were found.

## SECTION 10 - Minor Review Items

1. Freeze activation-neutralization semantics.

The module currently sets inactive raw candidate values to zero before final cross-sectional ranking, while retaining explicit active flags and missing raw-score masks. This is a reasonable interpretation of activation conditions, but the future panel specification should explicitly authorize it.

2. Expand formula drift coverage.

The tests currently include one direct formula-equivalence check for `vov_04` and broader schema/guardrail checks. Before artifact-writing execution, add candidate-level drift tests for `vov_01`, `vov_02`, `vov_03`, and `vov_05`.

3. Document after-close timing.

Same-bar OHLCV usage is acceptable only as after-close signal formation. This should be documented in the future panel manifest and IC evaluation plan.

4. Select artifact panel shape before execution.

The review recommends long-form as canonical and wide-form as optional diagnostic output. This decision should be frozen before any panel artifact is generated.

## SECTION 11 - Recommended Next Step

Proceed to:

**Project Underdog - OHLCV Volatility-of-Volatility Panel Specification v1**

The next task should remain specification-only unless explicitly authorized otherwise. It should freeze:

- Long-form panel schema.
- Activation-neutralization semantics.
- Date alignment and after-close timing.
- Candidate metadata fields.
- Diagnostic feature artifact policy.
- Warmup and missing-data manifest fields.
- Formula drift test requirements before panel writing.

Panel writing, IC scoring, discovery execution, redundancy screening, refinement, validation, governance changes, production registration, threshold changes, and ML should remain out of scope until that panel specification is approved.

## SECTION 12 - Verification Summary

Verification commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/ohlcv_volatility_of_volatility_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_research_module_v1.py -q` | passed, 7 tests |
| `python -m pytest tests/test_rank_coherence_discovery_scaffold.py tests/test_registry_validation.py -q` | passed, 8 tests |

Verification confirmations:

- Only `vov_01` through `vov_05` are implemented in the VoV module.
- No Dispersion Path-Dependence candidates were implemented.
- No Event Clustering candidates were implemented.
- No panel generation was executed.
- No IC scoring was executed.
- No discovery was executed.
- No redundancy screening was executed.
- No refinement was executed.
- No validation was executed.
- No governance files were modified.
- No production registry files were modified.
- No threshold files were modified.
- No ML files or integrations were introduced.

Artifact note:

- An older volatility-of-volatility-named parquet exists under a prior discovery batch path, but this review did not create or update any panel artifact.

Final classification:

- `MODULE_IMPLEMENTATION_READY_WITH_MINOR_REVIEW_ITEMS`
