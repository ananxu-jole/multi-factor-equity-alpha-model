# Isolated Signal-Factory Integration Test Plan: Refined Survivors

## 1. Executive Takeaway

This note defines a research-only isolated signal-factory integration test plan for two refined survivor candidates:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

It follows `docs/research_notes/isolated_implementation_equivalence_tests_refined_survivors.md`, where both candidates were classified as:

`near-equivalent with minor review items`

The goal of the next test is to determine whether these candidates can run through a signal-factory-style environment in isolation while preserving formula semantics, metadata, panel shape, scoring compatibility, WFV compatibility, stress/regime attribution, reproducibility, and production separation.

Final recommendation:

`run isolated signal-factory integration tests`

This does not authorize production registration. The next run must remain isolated, use a separate research namespace, and carry forward the review flags from the implementation-equivalence test.

No production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha paths should be changed.

## 2. Scope and Exclusions

In scope:

- isolated signal-factory draft integration for `volume_shock_reversal_stable_20`
- isolated signal-factory draft integration for `volatility_surprise_reversal_20_60_smooth`
- metadata and version validation
- candidate signal generation in an isolated namespace
- multi-horizon scoring compatibility review
- WFV compatibility review
- stress/regime attribution compatibility review
- orthogonality and redundancy audit
- integration decision note

Explicitly excluded:

- `residual_momentum_stability_60`
- LOW_BREADTH Conditional-Alpha work
- production signal-factory registration
- production survivor/watchlist updates
- alpha construction
- portfolio construction
- ML layer integration
- schema, gate, threshold, or validation-logic changes
- 04A+ execution

This is planning only. It should not implement the test or register the signals.

## 3. Candidate Review Flags

### `volume_shock_reversal_stable_20`

Current status:

`near-equivalent with minor review items`

Review flags to carry forward:

- raw sidecar matrices were unavailable, so raw-value/rank-level parity remains unproven
- sidecar universe/missingness mask could not be reconstructed exactly
- missingness drift versus sidecar summary was material
- same-date close/volume usage requires explicit after-close or next-rebalance timing assumptions

Lower-concern evidence:

- formula semantics were preserved
- sign convention was preserved
- h20 remained strongest
- h20 mean IC drift versus reference was small
- smoothing reduced turnover versus simple volume-spike and no-stability baselines

Integration posture:

This is the cleaner candidate. It can proceed to isolated signal-factory integration planning with standard drift controls and a specific universe/missingness review.

### `volatility_surprise_reversal_20_60_smooth`

Current status:

`near-equivalent with minor review items`

Review flags to carry forward:

- raw sidecar matrices were unavailable, so raw-value/rank-level parity remains unproven
- h20 metrics improved materially versus the sidecar reference
- missingness drift versus sidecar summary was material
- isolated implementation was highly similar to simple volatility/reversal baselines
- h10 remained coherent but must remain diagnostic, not an optimization target
- same-date close usage requires explicit after-close or next-rebalance timing assumptions

Higher-concern evidence:

- value correlation with simple volatility reversal was high
- value correlation with plain smoothed reversal was very high
- suspicious metric improvement could reflect formula drift, universe-mask drift, or accidental baseline convergence

Integration posture:

This candidate may proceed only with elevated drift and redundancy controls. The isolated signal-factory test should be designed to disprove accidental baseline duplication, not simply reproduce positive IC.

## 4. Integration Objective

Isolated signal-factory integration should prove that the candidates can be represented and generated inside a signal-factory-style environment without changing their research meaning or contaminating production outputs.

The test should prove:

| Objective | Required Evidence |
| --- | --- |
| Signal-factory compatibility | Candidate formulas can be expressed through the factory-style interfaces in isolation. |
| Metadata compatibility | Required metadata can be represented without schema changes. |
| Panel shape compatibility | Output panel aligns with expected date/ticker shape. |
| Multi-horizon scoring compatibility | h1, h5, h10, and h20 can be evaluated without special handling. |
| WFV compatibility | Candidate outputs can be consumed by existing WFV-style logic without schema or threshold changes. |
| Stress/regime attribution compatibility | Candidate behavior can be sliced by existing stress/regime definitions. |
| Reproducibility | Re-running the isolated generation produces stable outputs. |
| No production contamination | No production tables, survivor/watchlist lists, portfolios, or ML features are touched. |

This integration test should not prove alpha quality. It should prove isolated stack compatibility and identify any implementation drift.

## 5. Integration Test Stages

### Stage 0 - Isolated Research Definitions Confirmed

Confirm that the test uses:

- `docs/research_notes/isolated_draft_signal_definitions_refined_survivors.md`
- `docs/research_notes/isolated_implementation_equivalence_tests_refined_survivors.md`
- artifacts under `artifacts/research/refined_survivor_equivalence_v1/`

Exit requirement:

- candidate formulas, metadata, and review flags are frozen for the integration test

### Stage 1 - Isolated Signal-Factory Draft Insertion

Create draft signal definitions in an isolated test context only.

Allowed:

- local research-only draft registry
- temporary isolated candidate list
- formula wrappers that mimic signal-factory interfaces

Not allowed:

- production signal-factory registration
- mutation of `src/signals/factory.py` production behavior unless a later task explicitly creates isolated research files
- automatic inclusion in official pipeline runs

Exit requirement:

- both candidates can be addressed by name in the isolated test environment

### Stage 2 - Metadata and Version Validation

Validate metadata:

- `signal_name`
- `signal_family`
- `signal_version`
- `research_status`
- `registration_status`
- `intended_horizon`
- `expected_direction`
- `formula_description`
- `input_data_requirements`
- `known_risks`
- `failure_modes`
- `source_notes`

Exit requirement:

- metadata is complete and marked `DRAFT_RESEARCH_ONLY`

### Stage 3 - Candidate Signal Generation in Isolated Namespace

Generate signal panels using the isolated factory-style path.

Required:

- output date/ticker panel
- finite/missingness summary
- NaN/inf summary
- sign convention check
- output comparison against `refined_survivor_equivalence_v1` artifacts

Exit requirement:

- panels generate cleanly without production writes

### Stage 4 - Multi-Horizon Scoring Compatibility

Run isolated compatibility scoring for:

- h1
- h5
- h10
- h20

Primary focus:

- h20 for both candidates
- h10 diagnostic for `volatility_surprise_reversal_20_60_smooth`

Exit requirement:

- scoring completes without schema/gate changes and preserves expected horizon shape

### Stage 5 - WFV Compatibility Check

Run WFV compatibility diagnostics only if scoring outputs are valid.

Required discipline:

- preserve existing WFV windows
- preserve purge/embargo assumptions
- preserve thresholds and gates as read-only references
- write only isolated research artifacts

Exit requirement:

- candidate outputs can be consumed by WFV-style logic without special handling

### Stage 6 - Stress / Regime Attribution Check

Evaluate behavior across existing stress/regime definitions:

- drawdown acceleration
- volatility spike
- panic/liquidity stress
- recovery phase
- trend transition
- high dispersion / rotation
- low breadth, as a diagnostic state only

Exit requirement:

- stress/regime attribution is coherent and comparable to equivalence-test artifacts

### Stage 7 - Orthogonality and Redundancy Audit

Compare against:

- simple volume spike reversal
- unweighted reversal
- no-stability volume version
- simple volatility reversal
- unsmoothed volatility-surprise reversal
- plain 20-day smoothed reversal
- existing alpha-pool signals if available as read-only references
- current watchlist/survivor candidates if available as read-only references

Special rule:

`volatility_surprise_reversal_20_60_smooth` must receive elevated scrutiny for baseline convergence.

Exit requirement:

- redundancy and hidden-factor risks are explicitly documented

### Stage 8 - Integration Review Decision

Classify each candidate:

- `integration-compatible`
- `integration-compatible with review items`
- `not integration-compatible`
- `inconclusive`

Potential next decisions:

- continue to controlled official-registration planning
- revise isolated implementation
- revise draft definition
- perform deeper sidecar validation
- pause onboarding research
- reject candidate

No decision at this stage should mutate production survivor/watchlist lists.

## 6. Isolation Rules

The isolated integration test must use:

- separate `run_id`
- isolated namespace
- isolated output artifact directory
- candidate version label
- `research_only = true`
- `registration_status = DRAFT_RESEARCH_ONLY`

Suggested run metadata:

| Field | Suggested Value |
| --- | --- |
| `run_id` | `refined_survivor_factory_integration_v1` |
| `candidate_version` | `draft_v1_sidecar_refined` |
| `research_only` | `true` |
| `source_note` | `isolated_signal_factory_integration_test_plan_refined_survivors` |
| Output namespace | `artifacts/research/refined_survivor_factory_integration_v1/` |

Strict prohibitions:

- no production signal registration
- no automatic promotion
- no overwrite of current production tables
- no official survivor/watchlist mutation
- no portfolio use
- no ML use
- no Conditional-Alpha use
- no 04A+ run
- no gate relaxation
- no threshold relaxation
- no schema changes

Read-only comparisons to production artifacts are acceptable if clearly labeled.

## 7. Compatibility Checks

Required checks:

| Check | `volume_shock_reversal_stable_20` | `volatility_surprise_reversal_20_60_smooth` |
| --- | --- | --- |
| Formula preservation | abnormal-volume-weighted reversal with 40-day volume baseline and 10-day smoothing | 20/60 realized-volatility-surprise reversal with 5-day smoothing |
| Metadata completeness | required | required |
| Output panel shape | date/ticker panel; compare to equivalence artifact | date/ticker panel; compare to equivalence artifact |
| Date/ticker coverage | carry forward missingness drift review | carry forward missingness drift review |
| NaN/inf handling | zero/missing volume, insufficient rolling history | insufficient vol windows, low denominator, invalid ratios |
| Sign convention | higher score favors reversal after elevated-volume selloff | higher score favors volatility-surprise-weighted reversal |
| h20 primary behavior | must remain primary | must remain primary |
| h10 diagnostic behavior | optional only | required diagnostic, not optimization target |
| Turnover behavior | should remain below raw volume-spike baseline | should remain close to equivalence artifact |
| Scoring compatibility | h1/h5/h10/h20 | h1/h5/h10/h20 |
| WFV compatibility | no special handling | no special handling |
| Stress attribution compatibility | compare to equivalence stress slices | compare to equivalence stress slices |
| Reproducibility | rerun-stable outputs | rerun-stable outputs |

Additional checks:

- no centered rolling windows
- no target leakage
- no future returns in formulas
- no silent forward-fill that changes scores
- no date/ticker join shifts
- no sign flip after scoring
- no hidden dependency on sidecar-only artifacts

## 8. Drift Monitoring Plan

The isolated integration test should flag:

- metric improvements that are too large
- metric degradation
- horizon behavior changes
- h20 no longer primary
- sign flips
- coverage drift
- turnover drift
- suspicious baseline convergence
- WFV behavior mismatch
- stress behavior mismatch
- rank distribution drift versus equivalence artifacts
- suspiciously lower turnover caused by stale or over-smoothed values
- suspiciously better IC caused by universe changes or alignment mistakes

Candidate-specific monitoring:

### `volume_shock_reversal_stable_20`

Monitor:

- missingness drift versus equivalence artifact and sidecar summary
- turnover drift versus 0.098531 equivalence artifact
- baseline convergence toward unweighted reversal
- whether smoothing still reduces churn versus no-stability version
- h20 mean IC relative to 0.011798 equivalence artifact

Primary concern:

Universe/missingness drift, not formula semantics.

### `volatility_surprise_reversal_20_60_smooth`

Monitor:

- h20 metric improvement beyond equivalence artifact
- h20 mean IC relative to 0.016677 equivalence artifact
- h10/h20 relationship
- turnover drift versus 0.067001 equivalence artifact
- high correlation with simple volatility reversal
- high correlation with plain 20-day smoothed reversal
- whether the 20/60 volatility-surprise interaction adds independent information

Primary concern:

The candidate may collapse into a generic smoothed reversal or volatility-reversal proxy in factory-style implementation.

## 9. Failure / Pause Criteria

Pause or fail isolated integration research if:

- signal behavior changes materially from the isolated equivalence artifacts
- formula implementation diverges from draft definitions
- h20 behavior cannot be reproduced
- h20 is no longer the primary horizon without explanation
- sign convention flips
- turnover explodes
- WFV compatibility fails
- stress attribution deteriorates materially
- coverage changes materially without a universe or data explanation
- NaN/inf handling creates artificial scores
- hidden dependency on sidecar-only artifacts appears
- production contamination risk appears
- `volatility_surprise_reversal_20_60_smooth` remains too similar to simple volatility reversal or plain reversal
- suspicious metric improvement cannot be explained

Failure is research information, not a reason to relax gates.

Rollback action:

- keep generated artifacts
- document the mismatch
- return candidate to implementation-equivalence review, draft-definition revision, sidecar validation, or rejection
- do not register production signals

## 10. Expected Output Artifacts

Expected isolated artifacts:

- `manifest.json`
- `isolated_candidate_registry.csv`
- `metadata_validation_summary.csv`
- `generated_signal_panel_summary.csv`
- `signal_generation_log.csv`
- `scoring_compatibility_summary.csv`
- `wfv_compatibility_summary.csv`
- `stress_regime_attribution_summary.csv`
- `orthogonality_redundancy_summary.csv`
- `baseline_comparison_summary.csv`
- `drift_review_log.csv`
- `integration_decision_note.md`

Optional artifacts:

- candidate signal panel parquet files
- rank-correlation-by-date table
- turnover-by-date table
- h20/h10 daily IC tables
- WFV-window diagnostic table

Suggested output namespace:

`artifacts/research/refined_survivor_factory_integration_v1/`

The artifact namespace should be distinct from:

`artifacts/research/refined_survivor_equivalence_v1/`

## 11. Recommended Next Step

Final recommendation:

`run isolated signal-factory integration tests`

The next run should:

1. Create `artifacts/research/refined_survivor_factory_integration_v1/`.
2. Generate both candidate panels through an isolated factory-style path.
3. Validate metadata and panel shape.
4. Compare generated outputs to `refined_survivor_equivalence_v1` artifacts.
5. Run multi-horizon scoring compatibility.
6. Run WFV compatibility diagnostics.
7. Run stress/regime attribution.
8. Run orthogonality and redundancy review.
9. Classify each candidate for isolated integration compatibility.

The next run should not:

- register production signals
- mutate survivor/watchlist lists
- modify production gates, schemas, thresholds, validation logic, portfolio construction, ML layers, or Conditional-Alpha paths
- run 04A+

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Revise implementation-equivalence tests | Not primary | The equivalence tests produced enough evidence to plan factory-style integration. |
| Revise draft signal definitions | Not primary | Definitions remain usable; review items can be monitored during integration. |
| Perform deeper sidecar validation | Not primary | Useful if integration fails, but not needed before isolated factory compatibility testing. |
| Pause onboarding research | Rejected | Both candidates remain viable enough for isolated integration planning. |
| Production registration | Rejected | Near-equivalence is not a production registration basis. |

## Final Planning Conclusion

The integration plan is deliberately cautious:

- advance both candidates into isolated signal-factory integration testing
- treat `volume_shock_reversal_stable_20` as the cleaner candidate
- apply elevated drift and redundancy review to `volatility_surprise_reversal_20_60_smooth`
- preserve strict production separation
- use integration results as evidence, not promotion

Project Underdog should continue the onboarding sequence one controlled layer at a time. The next layer is isolated factory compatibility, not registration.
