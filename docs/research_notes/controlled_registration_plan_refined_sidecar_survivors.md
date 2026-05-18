# Controlled Registration Plan: Refined Sidecar Survivors

## 1. Executive Takeaway

This note defines a research-only controlled production-registration plan for two refined sidecar survivor candidates:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

The plan follows the robustness refinement documented in `docs/research_notes/robustness_refinement_three_sidecar_survivors.md`, where both candidates were classified as `refined survivor candidate`.

This is not a registration step. No production signal factory entries, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction logic, validation logic, ML layers, or Conditional-Alpha implementation paths are changed by this note.

Final recommendation:

`Proceed next with isolated draft signal definitions for the two refined candidates, still research-only, without registering them into production logic.`

Production registration should remain blocked until formula definitions, metadata, horizon assumptions, turnover expectations, WFV compatibility, stress compatibility, and orthogonality checks are explicitly locked.

## 2. Candidate Evidence Summary

| Candidate | Family | Intuition | Strongest Evidence | Weaknesses | Expected Horizon | Orthogonality Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | Large return moves amplified by abnormal volume may mean-revert when smoothed enough to avoid one-day noise. | 7 of 9 nearby variants passed sidecar robustness checks; best long-lookback/smoothed variant had effective test IC 0.037534 and positive window rate 0.75. | Turnover sensitivity; simple volume-spike baseline had high churn; needs careful formula lock. | h20 primary; h10 secondary only as diagnostic. | Adds liquidity-flow/reversal information with low current-pool overlap. |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | Return reversal may be more durable when conditioned by short-vs-long realized volatility surprise and smoothed. | 5 of 5 nearby variants passed sidecar robustness checks; simple volatility reversal and plain reversal baselines failed. | Full-sample IC is modest; h10/h20 ambiguity must be resolved before registration. | h20 primary candidate with h10 sensitivity review. | Cleanest orthogonal candidate; low correlation to broad reversal and LOW_BREADTH/trend components. |

Why these deserve controlled registration planning:

- Both survived parameter sensitivity checks better than simple baselines.
- Both showed sidecar WFV-style persistence without requiring gate relaxation.
- Both appear more orthogonal than recent trend-quality and conditional-context candidates.
- Both remain interpretable and OHLCV-compatible.
- Both still need controlled onboarding because sidecar evidence is not the same as official production-stack validation.

Known shared failure modes:

- Official 03 scoring may be weaker than sidecar WFV evidence.
- Formula implementation details may differ from sidecar construction.
- Stress behavior could degrade once evaluated through the full production stack.
- Hidden correlation may appear against a broader registered signal set.
- A candidate could pass isolated IC tests but fail turnover, reproducibility, or diversity requirements.

## 3. Registration Preconditions

Before either candidate can be registered into the production signal factory, all of the following must be true:

| Precondition | Requirement |
| --- | --- |
| Stable formula definition | Exact formula must be written in implementation-ready terms and match the sidecar research definition. |
| Parameter lock | Lookbacks, smoothing windows, ranking/normalization, and clipping behavior must be fixed before official scoring. |
| Horizon lock or metadata | Intended horizon must be declared up front, with h20 primary unless explicitly justified. |
| Metadata completeness | Signal metadata must include family, version, source note, intended horizon, expected direction, risks, and registration status. |
| Quality checks | Missingness, coverage, finite values, cross-sectional variation, and structural stability must pass existing structural review. |
| WFV compatibility | Signal must be compatible with existing WFV windows, purge/embargo settings, thresholds, and schemas. |
| Stress-test compatibility | Signal must be interpretable under drawdown, volatility spike, panic/liquidity stress, recovery, and trend-transition states. |
| Turnover sanity | Turnover must be measured before promotion and compared against sidecar expectations. |
| No look-ahead risk | All rolling inputs must use only information available at or before signal date. |
| No duplicate family exposure | Candidate must not duplicate existing stronger registered signals or pool members. |
| Reproducibility | Official outputs must reproduce under cache-enabled and clean-run conditions. |

No gate should be relaxed to accommodate either signal. Passing sidecar research is a reason to plan controlled onboarding, not a reason to reduce validation discipline.

## 4. Required Metadata

Each draft candidate should include the following metadata before any production registration is considered:

| Field | Purpose |
| --- | --- |
| `signal_name` | Stable canonical name. |
| `signal_family` | Research family, such as `liquidity_flow` or `volatility_structure`. |
| `signal_version` | Candidate version used for controlled registration planning. |
| `formula_description` | Plain-language and implementation-level description of the formula. |
| `input_data_requirements` | Required OHLCV fields and any benchmark inputs. |
| `intended_horizon` | Primary horizon, expected to be h20 unless locked otherwise. |
| `secondary_horizon_review` | Optional diagnostic horizon, such as h10 for volatility surprise. |
| `expected_direction` | Expected IC direction and interpretation. |
| `transformation_details` | Ranking, smoothing, normalization, clipping, neutralization, and lag conventions. |
| `known_risks` | Main structural and validation risks. |
| `failure_modes` | Expected ways the signal can fail. |
| `turnover_expectation` | Expected turnover class based on sidecar diagnostics. |
| `orthogonality_expectation` | Expected relationship to current pool, family proxies, and simple baselines. |
| `research_source_note` | Link to the refinement note and supporting sidecar artifacts. |
| `registration_status` | Must remain `DRAFT_RESEARCH_ONLY` until explicitly promoted by a later task. |

Recommended status values:

- `SIDECAR_RESEARCH_SURVIVOR`
- `DRAFT_RESEARCH_ONLY`
- `ISOLATED_TEST_READY`
- `OFFICIAL_REGISTRATION_CANDIDATE`
- `REGISTRATION_REJECTED`

These statuses are descriptive planning labels only and should not create any promotion path.

## 5. Safe Registration Workflow

### Stage 0 - Research Survivor Only

Current state.

The candidate exists only as a sidecar research survivor. Evidence comes from temporary diagnostic construction, parameter sensitivity checks, sidecar WFV-style review, counterfactual baselines, and orthogonality review.

Exit condition:

- Candidate has a written formula proposal, metadata draft, and explicit failure-mode list.

### Stage 1 - Candidate Registration Draft

Create isolated draft definitions outside production registration.

Allowed:

- Draft formula text.
- Research-only candidate specs.
- Unit-style formula parity checks against sidecar outputs.
- Naming and metadata review.

Not allowed:

- Production signal-factory registration.
- Automatic inclusion in official 03 scoring.
- Any schema, threshold, or gate changes.

Exit condition:

- Formula and metadata are locked for an isolated integration test.

### Stage 2 - Isolated Signal-Factory Integration Test

Test whether the formula can run inside the signal-factory environment without being admitted to the production candidate set.

Required checks:

- Output shape and index parity.
- Coverage and missingness.
- Cross-sectional variation.
- No look-ahead from rolling windows.
- Reproduction against sidecar formula.

Exit condition:

- Isolated outputs are stable and match the intended research definition.

### Stage 3 - Multi-Horizon Scoring Compatibility Test

Evaluate the candidate through existing scoring logic in an isolated run.

Required horizons:

- h1
- h5
- h10
- h20

Primary focus:

- h20 IC and IR.
- Sign stability.
- Horizon decay.
- Whether h10 strength is supportive or distracting.

Exit condition:

- Official scoring reproduces the broad sidecar direction without sign flip or horizon luck.

### Stage 4 - WFV / Stress Compatibility Test

Run controlled WFV only if the candidate earns admission through existing scoring and health logic.

Required discipline:

- Preserve existing WFV windows.
- Preserve purge/embargo.
- Preserve thresholds.
- Preserve gates and schemas.
- No widened admission.

Exit condition:

- Candidate either passes existing WFV expectations or is rejected with a documented reason.

### Stage 5 - Attribution and Orthogonality Audit

Compare candidate against:

- Current alpha-pool signals.
- Existing survivor/watchlist candidates.
- Simple family baselines.
- Broad market/trend proxies.
- Reversal, volume, volatility, and liquidity proxies.

Exit condition:

- Candidate adds distinct information, or is rejected as redundant.

### Stage 6 - Production Candidate Approval Decision

Only after the prior stages should a later task decide whether the signal is eligible for actual production signal-factory registration.

Allowed outcomes:

- Approve for controlled production registration.
- Keep in research watchlist.
- Send back for redesign.
- Reject.

This stage still should not mutate survivor/watchlist production lists unless a separate explicit implementation task authorizes it.

## 6. Isolation Rules

The registration research must not contaminate current production results.

Isolation requirements:

- Use a separate `run_id` for any future isolated execution.
- Use a separate candidate version label.
- Keep `registration_status = DRAFT_RESEARCH_ONLY` until an explicit later decision.
- Do not overwrite current production tables.
- Do not overwrite current alpha pool, survivor registry, or watchlist artifacts.
- Do not enable automatic promotion.
- Do not include these candidates in portfolio construction.
- Do not include these candidates in ML feature sets.
- Do not backfill historical production reports as if the signals had always existed.
- Keep sidecar and official outputs clearly separated.

Recommended run labeling:

- `sidecar_survivor_registration_draft_v1`
- `research_only = true`
- `source_note = robustness_refinement_three_sidecar_survivors`

Any future comparison against production artifacts should be read-only.

## 7. Regression / Rollback Criteria

Registration research should stop or roll back if any of the following occurs:

| Failure Condition | Stop / Rollback Reason |
| --- | --- |
| Parameter instability | Nearby variants no longer support the chosen formula. |
| Horizon instability | h20 evidence disappears or flips direction in official scoring. |
| Turnover explosion | Official turnover is materially worse than sidecar expectations. |
| Stress collapse | Candidate fails sharply in drawdown, volatility spike, panic/liquidity stress, or recovery states. |
| Hidden redundancy | Candidate becomes highly correlated with existing stronger signals or simple baselines. |
| Sign flip | IC direction changes across WFV windows or horizons. |
| Weak out-of-sample WFV | Existing WFV rejects for weak effective IC, weak IC IR, low persistence, or low sign consistency. |
| Reproducibility failure | Cache-enabled and clean runs disagree materially. |
| Implementation mismatch | Official formula does not match the sidecar research definition. |
| Look-ahead risk | Rolling or normalization logic uses unavailable future information. |
| Schema pressure | Candidate requires schema changes to be represented. |
| Gate pressure | Candidate only works if thresholds are relaxed. |

Rollback does not mean deleting research evidence. It means the candidate returns to sidecar research or redesign, with the rejection reason documented.

## 8. Candidate-Specific Registration Notes

### `volume_shock_reversal_stable_20`

Conceptual formula to preserve:

- Identify return reversal after abnormal volume participation.
- Use a longer volume-shock lookback than the naive version.
- Smooth the reversal expression enough to control churn.
- Keep the signal OHLCV-only and cross-sectionally interpretable.

Preferred research shape from refinement:

- Long volume-shock lookback.
- Stronger smoothing.
- h20 primary.
- Lower-turnover variant favored over higher-churn raw volume spike reversal.

Likely implementation risks:

- Accidentally registering the high-turnover volume-spike baseline instead of the smoothed stable version.
- Using an unstable volume normalization denominator.
- Creating excessive missingness from long rolling windows.
- Overfitting to the `s40_sm10` result without confirming official 03 behavior.
- Direction ambiguity if reversal sign is implemented inconsistently.

Required validation checks:

- Formula parity against sidecar definition.
- Missingness and coverage review.
- Turnover review versus `simple_volume_spike_reversal_20`.
- h20 primary scoring.
- h10/h20 decay sanity check.
- Orthogonality versus plain reversal and liquidity-flow proxies.
- Stress behavior under volatility spike and panic/liquidity stress states.

Expected comparison baselines:

- `simple_volume_spike_reversal_20`
- `plain_reversal_5_smooth5`
- Existing reversal-family signals.
- Current alpha-pool signals.
- Volume/liquidity proxies.

Likely failure modes during registration:

- Turnover fragility.
- Transaction-cost sensitivity.
- Overlap with generic reversal.
- Weak official full-sample IC.
- Sidecar-to-official implementation mismatch.

Registration planning view:

`Proceed to isolated draft signal definition, but use the lower-turnover refined form rather than the raw sidecar name literally.`

### `volatility_surprise_reversal_20_60_smooth`

Conceptual formula to preserve:

- Measure realized volatility surprise using short-vs-long volatility structure.
- Combine volatility surprise with return reversal.
- Smooth the combined expression.
- Avoid reducing the candidate to simple volatility reversal or plain reversal.

Preferred research shape from refinement:

- Preserve volatility-surprise interaction.
- Keep smoothing.
- Treat h20 as primary unless the isolated draft explicitly chooses h10.
- Use h10 as a sensitivity diagnostic because some longer-window variants showed h10 strength.

Likely implementation risks:

- Formula drift into generic volatility reversal.
- Inconsistent realized-volatility windowing.
- Horizon ambiguity between h10 and h20.
- Weak full-sample IC despite good WFV-style behavior.
- Hidden risk-off exposure during stress windows.

Required validation checks:

- Formula parity against sidecar definition.
- Volatility-window and smoothing lock.
- h20 official scoring with h10 sensitivity.
- Comparison against simple volatility reversal and plain reversal.
- Orthogonality versus volatility, reversal, LOW_BREADTH, and trend-quality proxies.
- Stress behavior under downtrend, volatility spike, panic/liquidity stress, and recovery states.

Expected comparison baselines:

- `simple_volatility_reversal_20`
- `plain_reversal_20_smooth5`
- Existing volatility-family signals.
- Existing reversal-family signals.
- Current alpha-pool signals.

Likely failure modes during registration:

- Weak official IC even if WFV-style evidence remains positive.
- h10/h20 instability.
- Volatility proxy duplication.
- Sign flip in recovery regimes.
- Stress strength caused by broad risk-off exposure rather than unique structure.

Registration planning view:

`Proceed to isolated draft signal definition with explicit h20 primary metadata and h10 diagnostic metadata.`

## 9. Exclusion Note for `residual_momentum_stability_60`

`residual_momentum_stability_60` should not enter controlled production-registration planning yet.

Reason:

- It was numerically strong in sidecar refinement.
- It had low turnover and strong stress-state behavior.
- But it was too entangled with plain 60-day momentum and trend-quality/LOW_BREADTH-adjacent exposure.

Research classification remains:

`needs redesign`

Recommended redesign direction:

- Make plain momentum a mandatory baseline control.
- Strengthen residualization if the family is meant to be relative-value.
- Test whether residual reversal is more orthogonal than residual momentum.
- Require a clearer uniqueness test before any registration planning.

This exclusion is intentional, not incidental. The project should avoid registering a candidate whose edge may be a disguised version of an already known family exposure.

## 10. Recommended Next Step

Final recommendation:

`isolated draft signal definitions`

This is the best next move because it advances the two refined candidates without admitting them into production logic.

The next task should create research-only draft specifications for:

1. `volume_shock_reversal_stable_20`, using the lower-turnover long-lookback/smoothed construction.
2. `volatility_surprise_reversal_20_60_smooth`, preserving the volatility-surprise reversal interaction.

The draft step should produce:

- exact formula definitions
- locked parameters
- metadata draft
- expected horizon declaration
- implementation risks
- comparison baselines
- official validation plan

It should not:

- register the signals
- modify the production signal factory
- alter gates or thresholds
- mutate survivor/watchlist lists
- run portfolio construction
- run 04A+
- add ML features

Alternative next moves rejected:

| Option | Decision | Reason |
| --- | --- | --- |
| Deeper robustness testing | Not primary | Enough sidecar evidence exists to define draft formulas; deeper testing should follow formula lock. |
| Additional sidecar validation | Not primary | Useful later, but risks delaying the necessary formula and metadata discipline. |
| Production registration | Rejected for now | Sidecar evidence is not official production-stack validation. |
| Reject / pause registration research | Rejected | Two candidates are sufficiently durable to justify controlled onboarding design. |

## Final Planning Conclusion

The controlled path is deliberately narrow:

- Advance `volume_shock_reversal_stable_20`.
- Advance `volatility_surprise_reversal_20_60_smooth`.
- Exclude `residual_momentum_stability_60` until redesigned.
- Keep all work isolated and research-only.
- Preserve existing gates, schemas, thresholds, promotion logic, and portfolio logic.

This keeps Project Underdog moving back toward robust standalone alpha discovery while maintaining the strict validation discipline that prevented earlier unstable signals from being forced through the pipeline.
