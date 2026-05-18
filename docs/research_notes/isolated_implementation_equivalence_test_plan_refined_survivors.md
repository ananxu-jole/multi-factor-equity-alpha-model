# Isolated Implementation-Equivalence Test Plan: Refined Survivors

## 1. Executive Takeaway

This note defines a research-only isolated implementation-equivalence test plan for two refined survivor draft signals:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

It follows `docs/research_notes/isolated_draft_signal_definitions_refined_survivors.md`, which preserved the research semantics of both candidates without registering them.

The purpose of this plan is to verify, in a future isolated test, that any implementation faithfully reproduces the original research meaning, data handling, sign convention, window logic, and diagnostic behavior before production registration is considered.

Final recommendation:

`Run isolated implementation-equivalence tests in a separate research namespace.`

Do not implement the signals from this note. Do not register either signal. Do not modify production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, notebooks, ML layers, or Conditional-Alpha paths.

## 2. Scope and Exclusions

In scope:

- Define what implementation-equivalence means for these two draft signals.
- Specify required inputs and reference outputs.
- Define signal-specific formula, window, sign, coverage, turnover, and baseline checks.
- Define sidecar-vs-implementation comparison requirements.
- Define drift review expectations and failure criteria.
- Define isolation and reproducibility requirements for a later test run.

Out of scope:

- Signal implementation.
- Production signal-factory registration.
- Official scoring integration.
- WFV bridge execution.
- 04A+ execution.
- Portfolio construction.
- Survivor/watchlist mutation.
- Gate, threshold, or schema changes.
- ML feature inclusion.
- Conditional-Alpha framework usage.

This is a design artifact only.

## 3. Implementation-Equivalence Definition

For this research step, an implementation is "implementation-equivalent" when it preserves the original research definition closely enough that later validation results can be interpreted as testing the same candidate, not a changed formula.

Equivalence includes:

| Equivalence Area | Required Meaning |
| --- | --- |
| Formula equivalence | The implemented expression matches the draft formula semantics and sidecar research intent. |
| Data-input equivalence | The implementation uses the same OHLCV-derived inputs and does not introduce new data dependencies. |
| Lookback/window equivalence | Rolling return, volume, realized-volatility, and smoothing windows match the locked draft assumptions. |
| Smoothing equivalence | Smoothing method, window endpoint, minimum periods, and NaN behavior are consistent with research semantics. |
| Ranking/normalization equivalence | Cross-sectional scoring matches intended rank/z-score conventions and date-level grouping. |
| NaN handling equivalence | Missing input data, zero volume, insufficient rolling history, and inf values are handled consistently. |
| Sign convention equivalence | Higher and lower scores retain the intended reversal interpretation. |
| Horizon behavior equivalence | h20 remains the primary diagnostic horizon; h10 remains secondary only where specified. |
| Metric reproduction equivalence | IC, IC IR, turnover, coverage, and stress/regime summaries broadly reproduce sidecar conclusions. |
| No look-ahead equivalence | All rolling, smoothing, ranking, and forward-return alignment avoid target leakage. |

Equivalence does not require bit-for-bit equality if the sidecar reference used temporary scripts or slightly different storage conventions. It does require that any differences be explainable, bounded, and not directionally favorable by accident.

## 4. Required Input Data

The future isolated test should use a fixed data snapshot and a separate research run namespace.

Required shared inputs:

- date/ticker panel with stable alignment
- adjusted close or close prices
- daily returns derived from close prices
- volume data
- forward returns for h1, h5, h10, and h20 diagnostics
- existing sidecar reference outputs or regenerated research reference outputs
- universe membership used by the sidecar diagnostics
- current scoring version identifier
- benchmark/context data only if required for stress/regime attribution, not for formula construction

Signal-specific inputs:

| Signal | Required Inputs |
| --- | --- |
| `volume_shock_reversal_stable_20` | close/adjusted close, daily returns, volume, rolling volume baseline, recent return, sidecar reference values if available |
| `volatility_surprise_reversal_20_60_smooth` | close/adjusted close, daily returns, 20-day realized volatility, 60-day realized volatility, recent return, sidecar reference values if available |

Panel requirements:

- identical date index between reference and implementation outputs
- identical ticker universe where possible
- explicit logging of dropped dates/tickers
- no silent forward-filling of missing prices or volume
- no hidden survivorship changes between sidecar and implementation comparison

Reference artifacts should be treated as research references only, not production truth tables.

## 5. Test Plan for `volume_shock_reversal_stable_20`

### Objective

Verify that the future implementation preserves the smoothed abnormal-volume-weighted reversal semantics documented in the draft definition.

### Formula Checks

Required checks:

- abnormal volume calculation matches the intended rolling volume baseline
- volume shock ratio or normalized volume surprise is stable and finite
- recent return component is calculated with the intended return window
- reversal sign is applied before smoothing and ranking
- raw signal combines reversal and volume shock as intended
- smoothing uses the intended long-lookback/stable construction
- cross-sectional score is computed by date

Initial draft parameters to verify:

- volume shock baseline: approximately 40 trading days
- smoothing window: approximately 10 trading days
- primary horizon: h20

The test must explicitly confirm whether these are exact sidecar parameters or approximations from the refinement note. Any mismatch should be documented before further testing.

### Stability Filter Checks

The "stable" element should come from smoothing and stabilized volume normalization.

Do not accept an implementation that adds:

- regime gating
- LOW_BREADTH activation
- sector dependencies
- beta overlays
- confirmation layers
- extra stress filters

### Missing-Volume and NaN Handling

Review:

- zero volume handling
- missing volume handling
- insufficient rolling-history dates
- inf values from division by zero
- thinly traded names if present
- cross-sectional dates with too few valid names

Expected behavior:

- invalid values should become NaN, not arbitrary large scores
- early rolling-window dates should be missing until enough history exists
- missingness should be comparable to sidecar output

### Direction and Horizon Checks

Expected sign:

- high score: negative recent return with elevated abnormal volume, consistent with reversal
- low score: positive recent return with elevated abnormal volume, consistent with reversal

Expected horizon:

- h20 primary
- h10 only as supporting sensitivity, not as optimization target

### Turnover and Baseline Checks

Required comparisons:

- turnover versus sidecar `volume_shock_reversal_stable_s40_sm10`-style reference
- turnover versus simple volume-spike reversal
- turnover versus plain reversal baseline
- h20 mean IC and IC IR versus sidecar reference
- stress/regime behavior versus sidecar reference

Required baseline:

- `simple_volume_spike_reversal_20`
- `plain_reversal_5_smooth5`

Failure concern:

If the implementation resembles the high-turnover simple volume-spike baseline more than the smoothed stable reference, the equivalence test should fail.

## 6. Test Plan for `volatility_surprise_reversal_20_60_smooth`

### Objective

Verify that the future implementation preserves the smoothed 20/60 realized-volatility-surprise reversal semantics documented in the draft definition.

### Formula Checks

Required checks:

- 20-day realized volatility is calculated from historical returns only
- 60-day realized volatility baseline is calculated from historical returns only
- volatility surprise reflects short-vs-long realized-volatility structure
- recent return reversal component is calculated consistently
- reversal and volatility surprise are interacted or weighted as intended
- smoothing is applied consistently
- cross-sectional score is computed by date

Initial draft parameters to verify:

- short realized volatility window: 20 trading days
- long realized volatility window: 60 trading days
- smoothing: sidecar smoothed construction, initial target 5 trading days unless exact reference differs
- primary horizon: h20
- diagnostic horizon: h10

### Volatility-Window NaN Handling

Review:

- insufficient 20-day history
- insufficient 60-day history
- zero or near-zero long volatility denominator
- inf values from volatility ratios
- volatility normalization during very quiet periods
- date-level coverage after rolling windows

Expected behavior:

- early rolling-window periods should be NaN
- invalid ratios should not be clipped into artificial signals without documentation
- NaN/inf handling should match reference output

### Direction and Horizon Checks

Expected sign:

- high score: reversal potential under elevated short-vs-long realized volatility
- low score: unfavorable volatility-surprise-weighted reversal expression

Expected horizon:

- h20 primary
- h10 diagnostic only

The implementation should not be re-optimized to h10 unless a separate research note changes the intended horizon before official testing.

### Baseline Checks

Required comparisons:

- `simple_volatility_reversal_20`
- `plain_reversal_20_smooth5`
- existing volatility-family signals
- existing reversal-family signals
- LOW_BREADTH/trend-quality references where available

Failure concern:

If the implementation behaves like generic volatility reversal or plain reversal, rather than volatility-surprise-weighted reversal, the equivalence test should fail.

## 7. Sidecar-vs-Implementation Comparison Plan

The future isolated test should compare implementation outputs to research reference outputs at multiple levels.

Required output comparisons:

| Comparison Area | Required Review |
| --- | --- |
| Raw signal values | Distribution, correlation, sign, date/ticker alignment. |
| Rank values | Cross-sectional rank correlation and ordering stability by date. |
| Cross-sectional ordering | Top/bottom basket overlap and rank drift. |
| Sign consistency | Same intended direction versus forward returns and sidecar reference. |
| Active date count | Non-null date counts; active-condition counts only if applicable, though these two signals are not conditional. |
| Non-null coverage | Date-level and ticker-level coverage versus reference. |
| Turnover | Average turnover, turnover spikes, and transition instability. |
| Mean IC | h1/h5/h10/h20 comparison versus sidecar conclusions. |
| IC IR | Horizon-level IC IR comparison. |
| Sharpe proxy | If available, compare simple long/short proxy behavior. |
| Max drawdown proxy | If available, compare simple long/short drawdown behavior. |
| Horizon behavior | h20 primary and h10 diagnostic behavior where applicable. |
| Stress/regime attribution | Direction and relative strength across stress/regime states. |

Suggested artifact outputs for a later test:

- `implementation_equivalence_summary.csv`
- `signal_value_comparison.csv`
- `rank_correlation_by_date.csv`
- `coverage_comparison.csv`
- `turnover_comparison.csv`
- `horizon_metric_comparison.csv`
- `stress_regime_comparison.csv`
- `baseline_comparison.csv`
- `equivalence_review.md`

These artifacts should live in a separate research namespace, not production output locations.

## 8. Tolerance / Drift Review Expectations

This plan does not define production gates or thresholds. It defines research review expectations that should trigger investigation.

Flag for review:

- sign flips relative to the draft definition
- large rank drift versus reference output
- material IC drift versus sidecar conclusions
- h20-to-h10 behavior change that alters the intended horizon
- turnover materially higher than sidecar expectation
- coverage materially lower or higher than reference without explanation
- NaN/inf differences that change score distribution
- date alignment mismatch
- ticker alignment mismatch
- suspicious metric improvement
- suspiciously lower turnover caused by accidental smoothing or stale values
- stronger results caused by forward-looking alignment

Interpretation guidance:

- Worse results are not automatically failure if the implementation is faithful and sidecar reference was noisy.
- Better results are not automatically good; unexplained improvement can indicate leakage, sign errors, or alignment mistakes.
- Small numerical differences are acceptable only if rank ordering, sign convention, coverage, and horizon behavior remain coherent.

Any drift review should be documented before a candidate proceeds to isolated scoring.

## 9. Look-Ahead and Alignment Tests

The future implementation-equivalence run must include explicit leakage and alignment checks.

Required tests:

| Test | Purpose |
| --- | --- |
| Historical-window check | Confirm rolling returns, volume baselines, realized volatility, and smoothing use only current/past data. |
| Forward-return alignment check | Confirm IC uses future returns relative to signal date, not overlapping target information. |
| Window-end timing check | Confirm rolling windows end on the signal date, not after it. |
| Same-bar leakage check | Confirm same-day close/volume usage is compatible with the assumed signal timestamp and forward return convention. |
| Ranking alignment check | Confirm cross-sectional ranks use only same-date signal values. |
| Smoothing leakage check | Confirm smoothing is trailing, not centered. |
| Universe alignment check | Confirm universe membership is applied consistently across reference and implementation. |
| Ticker/date join check | Confirm no shifted ticker or date joins. |
| Baseline parity check | Confirm baselines use the same return and horizon alignment as candidates. |

Lagged execution compatibility:

- The plan should document whether the signal is assumed tradable after the close, next open, or next rebalance convention.
- Any future production registration must use the existing platform convention, not a special timing rule.

No target leakage through smoothing or ranking should be tolerated.

## 10. Reproducibility Requirements

The future isolated test should be reproducible and auditable.

Required identifiers:

- fixed `run_id`
- fixed candidate version
- reference research source note
- input data snapshot identifier
- universe version
- scoring version
- date range
- code version or commit hash if applicable
- cache setting declaration
- output artifact directory

Recommended run labels:

- `run_id = refined_survivor_equivalence_v1`
- `candidate_version = draft_v1_sidecar_refined`
- `research_only = true`
- `source_note = isolated_draft_signal_definitions_refined_survivors`

Required logs:

- input artifact list
- reference output source
- formula parameters used
- missingness summary
- coverage summary
- rank comparison summary
- metric comparison summary
- drift review notes
- final research-only equivalence decision

Suggested output location:

- `artifacts/research/refined_survivor_equivalence_v1/`

The future test should not overwrite existing production artifacts.

## 11. Isolation Rules

The implementation-equivalence test must remain isolated.

Rules:

- no production registration
- no official survivor/watchlist mutation
- no production table overwrite
- no automatic scoring integration
- no portfolio usage
- no ML usage
- no Conditional-Alpha usage
- no schema changes
- no gate changes
- no threshold changes
- separate research run namespace only
- read-only comparison to production artifacts where needed

The test should answer whether the implementation preserves research semantics. It should not decide official promotion.

## 12. Failure / Rollback Criteria

The implementation-equivalence test should fail, pause, or roll back to draft-definition review if any of the following are observed:

| Failure Condition | Interpretation |
| --- | --- |
| Formula mismatch | Implementation does not represent the draft research formula. |
| Sign mismatch | Score direction is opposite or opportunistically flipped. |
| Window mismatch | Lookbacks, smoothing, or realized-volatility windows differ without documentation. |
| Metric drift | IC/IR/stress behavior no longer resembles sidecar conclusions and drift is unexplained. |
| Turnover drift | Turnover materially increases or decreases due to implementation differences. |
| Coverage drift | Non-null coverage differs materially without a data or window explanation. |
| NaN/inf mismatch | Missingness and invalid-value handling changes signal distribution. |
| Look-ahead risk | Any rolling, smoothing, ranking, or target alignment may use future data. |
| Sidecar evidence not reproducible | Reference behavior cannot be reproduced or reconciled. |
| Suspicious improvement | Metrics improve materially without a structural explanation. |
| Suspicious degradation | Metrics degrade materially because of implementation mismatch. |
| Hidden dependency | Formula requires sidecar-only artifacts not available in production-style data. |
| Isolation breach | Test writes to production tables or mutates official lists. |

Rollback means:

- keep the research notes
- document the mismatch
- return the candidate to draft-definition review or sidecar validation
- do not proceed to production registration planning

## 13. Recommended Next Step

Final recommendation:

`run isolated implementation-equivalence tests`

This is the appropriate next move because the draft signal definitions are now documented and the next risk is implementation drift.

The next task should:

1. Create a separate research namespace for the equivalence run.
2. Implement the two formulas only in an isolated test context.
3. Generate reference-vs-implementation comparison artifacts.
4. Evaluate formula, sign, window, coverage, turnover, horizon, and stress/regime equivalence.
5. Produce a research note with pass/fail findings.

It should not:

- register the signals
- add them to the production signal factory
- modify official scoring or WFV logic
- mutate survivor/watchlist lists
- run portfolio construction
- run 04A+
- add ML features

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Revise draft signal definitions | Not needed now | Definitions are sufficient for an equivalence test plan. |
| Perform deeper sidecar validation | Not primary | Formula equivalence must be established before more diagnostics are meaningful. |
| Proceed to production registration | Rejected | Registration before equivalence testing would risk formula drift and research contamination. |
| Pause onboarding research | Rejected | The two candidates remain suitable for controlled isolated testing. |

## Final Planning Conclusion

The next step should be a research-only isolated implementation-equivalence test for:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

The test should prove that future implementations preserve formula semantics, sign direction, rolling-window timing, smoothing, ranking, coverage, turnover, and horizon behavior before any production registration is considered.
