# Project Underdog - Dispersion Path-Dependence Formula Implementation Review v1

## SECTION 1 - Executive Summary

Classification: `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`

This note reviews the Dispersion Path-Dependence formula implementation before any panel specification, panel generation, IC discovery, validation, governance action, production registry change, threshold change, or ML work.

Reviewed implementation:

- `pipelines/dispersion_path_dependence_research_module_v1.py`
- `tests/test_dispersion_path_dependence_research_module_v1.py`
- `docs/research_notes/dispersion_path_dependence_formula_implementation_v1.md`
- `docs/research_notes/dispersion_path_dependence_formula_and_panel_specification_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_mechanism_review_v1.md`

Review conclusion:

The implementation is approved for the next lifecycle phase with notes. Exactly four approved candidates are implemented, scientific lineage is preserved, blocked mechanisms remain blocked, formulas and activation rules now have focused drift tests, and no research execution or artifact generation occurred.

One small review fix was applied:

- `z_ts` handling now returns neutral `0.0` when the trailing standard deviation is zero and the centered value is also zero. This prevents a constant date-level path, especially the market stress path, from making the divergence candidate entirely nonfinite. This is an implementation-stability fix for the specified z-score operation, not a formula change.

The next lifecycle phase may begin: panel specification. Panel generation should remain blocked until panel specification and panel-generation authorization are complete.

## SECTION 2 - Candidate Count and Scope Review

Implemented candidate IDs:

| candidate_id | status |
| --- | --- |
| `dpath_01_relapse_resilience_after_calm` | implemented |
| `dpath_02_disagreement_vol_stress_divergence` | implemented |
| `dpath_03_elevated_disagreement_stabilization` | implemented |
| `dpath_04_consensus_without_crowding` | implemented |

Scope checks:

- Exactly four candidates are implemented.
- No Smooth Versus Burst Resolution candidate is implemented.
- No `dpath_05` or higher candidate is implemented.
- No VoV candidate is implemented.
- No event-clustering candidate is implemented.
- No refinement variant is implemented.

Classification for scope:

- Pass.

## SECTION 3 - Formula and Activation Review

Formula review:

| candidate_id | formula status | activation status |
| --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Matches frozen specification. | Matches relapse-after-calm activation. |
| `dpath_02_disagreement_vol_stress_divergence` | Matches frozen specification. | Matches divergence-intensity activation after z-score stability fix. |
| `dpath_03_elevated_disagreement_stabilization` | Matches frozen specification. | Matches elevated-then-stabilizing activation. |
| `dpath_04_consensus_without_crowding` | Matches frozen specification. | Matches normalization-without-crowding activation. |

The formulas preserve the approved mechanism mapping:

- one candidate to one mechanism;
- no multi-mechanism candidate;
- no target-hacking or parameter grid;
- no horizon shopping;
- no deferred mechanism included.

Classification for formula match:

- Pass with note on z-score zero-variance handling.

## SECTION 4 - Scientific Lineage and Metadata Review

The implementation preserves required lineage fields in candidate registry and long-form panel rows:

- `candidate_id`
- `candidate_name`
- `mechanism_family`
- `hypothesis`
- `scientific_question`
- `expected_evidence`
- `primary_falsification_criterion`
- `observable_implication`
- `expected_orthogonality`
- `contamination_controls`
- `anchor_comparators`
- `primary_horizon`
- `secondary_horizons`
- `expected_sign`
- `formula_text`
- `activation_text`
- `timing_policy`
- `created_by_spec`

The lineage is sufficient for downstream panel manifests and implementation review traceability.

Classification for lineage:

- Pass.

## SECTION 5 - Registry and Guardrail Review

Registry validation is meaningful because it checks:

- exact candidate ID order and count;
- blocked VoV and event prefixes;
- blocked Smooth/Burst IDs;
- family identity;
- h10 primary horizon;
- research-only status;
- one distinct approved mechanism per candidate.

Guardrail manifest correctly reports:

- no Smooth/Burst implementation;
- no extra dpath candidates;
- no VoV candidates;
- no event-clustering candidates;
- no panel generation;
- no IC scoring;
- no validation;
- no governance modification;
- no production registration;
- no threshold changes;
- no ML integration.

Classification for registry and guardrails:

- Pass.

## SECTION 6 - Feature, Warmup, and Timing Review

Rolling and cross-sectional features reviewed:

- OHLCV-derived returns, ranges, volatility, drawdown, and dollar volume are trailing-only.
- Cross-sectional disagreement uses same-date return MAD and trailing date-level path features.
- Security-level ranks are same-date cross-sectional ranks.
- Dispersion z-scores, slopes, divergence intensity, and market-state path features use only data through signal date `t`.
- No forward return or target data are used in feature construction.

Warmup and missing-data rules:

- Security warmup requires at least 60 observations.
- Date-level state warmup requires at least 252 observations.
- Warmup-incomplete rows remain null and carry `rolling_warmup`.
- Raw OHLCV gaps are not imputed.
- Nonfinite formula rows remain null.
- Inactive but feature-valid rows receive neutral `0.5` and `is_active = false`.

Timing:

- After-close timing policy is preserved as `after_close_t_forward_returns_after_t`.
- No intraday assumption is introduced.

Classification for feature and timing integrity:

- Pass with note: the zero-variance z-score convention should be preserved in panel-generation review.

## SECTION 7 - Long-Form Panel Compatibility Review

The implementation returns an in-memory long-form panel compatible with the frozen specification:

- one row per `date` x `ticker` x `candidate_id`;
- unique canonical key is test-covered;
- four allowed candidate IDs only;
- required lineage, formula, timing, activation, and contamination fields are present;
- optional diagnostic fields are present and scalar.

No panel file is written by the implementation. No artifact directory was created.

Classification for panel compatibility:

- Pass.

## SECTION 8 - Test Review and Review Fixes

Existing tests already covered:

- exact four-candidate registry;
- blocked deferred candidates;
- blocked VoV and event candidates;
- long-form schema compatibility;
- warmup, missing-data, and inactive-neutralization separation;
- guardrail manifest;
- input schema enforcement.

Review fix applied to tests:

- Formula and activation drift tests were expanded from one candidate to all four implemented candidates.
- The synthetic fixture was extended for formula-drift testing so long-horizon date-level features are mature enough to test the divergence candidate.

Review fix applied to implementation:

- `_date_level_z` now emits neutral `0.0` when trailing standard deviation is zero and the centered value is zero. This keeps constant path references from becoming permanently nonfinite.

Classification for test sufficiency:

- Pass after review fixes.

## SECTION 9 - Verification

Commands run:

```bash
python -m py_compile pipelines/dispersion_path_dependence_research_module_v1.py
pytest -q tests/test_dispersion_path_dependence_research_module_v1.py tests/test_registry_validation.py
```

Results:

- Python compile: passed.
- Focused implementation and registry/scaffold tests: 16 passed.

Additional guardrail checks:

- Confirmed no panel artifact directory exists at `artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`.
- Confirmed Smooth/Burst, VoV, and event-clustering strings appear only in blocked candidate/guardrail/test contexts.

## SECTION 10 - Final Decision

Final classification:

- `IMPLEMENTATION_REVIEW_APPROVED_WITH_NOTES`

Panel specification may begin.

Notes carried forward:

- Preserve the neutral zero-variance z-score convention in panel specification and panel audit.
- Panel generation must remain blocked until the next lifecycle phase explicitly authorizes it.
- Future panel audit should inspect active-date ratios, missing reasons, finite cross-section counts, duplicate keys, and candidate-specific activation distributions before IC discovery.

No IC discovery, validation, governance mutation, production registry change, threshold change, or ML work is authorized by this review.
