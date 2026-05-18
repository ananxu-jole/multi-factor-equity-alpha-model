# Isolated Draft Signal Definitions: Refined Sidecar Survivors

## 1. Executive Takeaway

This note preserves isolated, research-only draft definitions for two refined sidecar survivor candidates:

- `volume_shock_reversal_stable_20`
- `volatility_surprise_reversal_20_60_smooth`

It follows the controlled registration plan in `docs/research_notes/controlled_registration_plan_refined_sidecar_survivors.md` and the robustness refinement evidence in `docs/research_notes/robustness_refinement_three_sidecar_survivors.md`.

These definitions are not production registrations. They are auditable research specifications intended to prevent formula drift before any future isolated implementation-equivalence testing.

Final recommendation:

`Proceed next with an isolated implementation-equivalence test plan for the two draft signals.`

Do not register either signal yet. Do not modify production signal-factory logic, schemas, gates, thresholds, survivor/watchlist lists, portfolio logic, validation logic, notebooks, ML layers, or Conditional-Alpha paths.

## 2. Scope and Exclusions

In scope:

- Define precise research identity and formula semantics for `volume_shock_reversal_stable_20`.
- Define precise research identity and formula semantics for `volatility_surprise_reversal_20_60_smooth`.
- Draft metadata required before any future isolated testing.
- Define isolation and future integration-test requirements.

Out of scope:

- Production signal registration.
- Official scoring integration.
- WFV bridge execution.
- 04A+ execution.
- Portfolio construction.
- Survivor/watchlist mutation.
- Schema changes.
- Gate or threshold changes.
- ML feature inclusion.
- Conditional-Alpha framework implementation.

Excluded candidate:

- `residual_momentum_stability_60`

It remains in redesign research because the refinement diagnostic found excessive entanglement with plain momentum and trend-quality exposure.

## 3. Candidate Identity Summary

| Signal | Family | Version | Intended Horizon | Expected Direction | Research Status | Registration Status |
| --- | --- | --- | --- | --- | --- | --- |
| `volume_shock_reversal_stable_20` | `liquidity_flow` | `draft_v1_sidecar_refined` | h20 primary | Reversal | `SIDECAR_RESEARCH_SURVIVOR` | `DRAFT_RESEARCH_ONLY` |
| `volatility_surprise_reversal_20_60_smooth` | `volatility_structure` | `draft_v1_sidecar_refined` | h20 primary, h10 diagnostic | Reversal under volatility surprise | `SIDECAR_RESEARCH_SURVIVOR` | `DRAFT_RESEARCH_ONLY` |

Common intended behavior:

- Both candidates are standalone alpha-signal candidates, not conditional-alpha components.
- Both are OHLCV-only.
- Both should remain cross-sectional signals.
- Both should preserve reversal semantics.
- Both require official scoring, WFV, stress, turnover, and orthogonality testing before any registration decision.

Common expected failure modes:

- Weak official full-sample IC despite positive sidecar evidence.
- Sidecar-to-production formula mismatch.
- Horizon instability.
- Stress-state sign flip.
- Redundancy with simpler reversal, volatility, volume, or liquidity proxies.

## 4. Draft Definition for `volume_shock_reversal_stable_20`

### Identity

| Field | Draft Definition |
| --- | --- |
| `signal_name` | `volume_shock_reversal_stable_20` |
| `signal_family` | `liquidity_flow` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `SIDECAR_RESEARCH_SURVIVOR` |
| `registration_status` | `DRAFT_RESEARCH_ONLY` |
| `intended_horizon` | h20 primary |
| `expected_direction` | Reversal after abnormal volume participation |

### Economic Intuition

Large price moves that occur alongside abnormal volume can reflect forced flow, crowding, liquidity demand, or short-term overreaction. The research hypothesis is that some of those moves mean-revert over a medium horizon when the raw shock measure is smoothed enough to avoid one-day volume noise.

This is a liquidity-flow reversal candidate, not a momentum candidate.

### Conceptual Formula

Research semantics to preserve:

1. Compute recent asset return over a short reversal window.
2. Compute abnormal volume participation using a rolling volume baseline.
3. Emphasize reversal when the return move is accompanied by elevated volume participation.
4. Smooth the resulting expression to reduce churn and one-day shock noise.
5. Convert to a cross-sectional score on each date.

Draft formula intent:

```text
return_reversal_component = -1 * recent_return
volume_shock_component = current_or_recent_volume / rolling_volume_baseline
raw_signal = return_reversal_component * stabilized_volume_shock_component
signal = rolling_smooth(raw_signal)
cross_sectional_score = rank_or_zscore(signal by date)
```

The sidecar refinement favored a lower-turnover long-lookback/smoothed construction. The implementation-equivalence plan should treat the refined research shape as:

- volume shock lookback: approximately 40 trading days
- smoothing window: approximately 10 trading days
- primary evaluation horizon: h20

The canonical name remains `volume_shock_reversal_stable_20` because the intended research horizon is h20. The implementation should not interpret the trailing `20` as a required volume-shock lookback.

### Required Input Data

Required OHLCV fields:

- adjusted close or close
- volume
- date
- asset identifier

Derived fields:

- recent return
- rolling volume baseline
- volume shock ratio or normalized volume surprise
- rolling smoothed signal value

No fundamental, sector, analyst, option, borrow, macro, or external data should be required.

### Lookback and Transformation Logic

Draft parameter lock for the next isolated test plan:

| Component | Draft Research Setting | Purpose |
| --- | --- | --- |
| Return reversal window | short-term recent return, implementation to match sidecar definition | Captures overreaction direction. |
| Volume shock baseline | about 40 trading days | Stabilizes volume abnormality and reduces churn. |
| Smoothing window | about 10 trading days | Reduces turnover and one-day noise. |
| Scoring transform | cross-sectional rank or z-score by date, consistent with existing signal conventions | Makes the signal comparable across assets. |

The next implementation-equivalence plan must recover the exact sidecar construction before any official run.

### Ranking and Sign Convention

Expected sign convention:

- Higher score should favor names whose recent negative return occurred with elevated volume shock, consistent with reversal.
- Lower score should penalize names whose recent positive return occurred with elevated volume shock, consistent with reversal.

If the implementation produces the opposite interpretation, the sign must be corrected before testing. Sign should not be chosen after seeing official scoring results.

### Stability Filter / Condition

The "stable" part of the name should be represented by smoothing and stabilized volume normalization, not by adding a new conditional regime gate.

Do not add:

- LOW_BREADTH activation.
- regime gates.
- sector dependencies.
- beta-neutral overlays.
- new stress filters.
- extra confirmation layers.

### Why It Appears Robust

Evidence from refinement:

- 7 of 9 nearby variants passed sidecar robustness checks.
- Longer volume-shock lookbacks and stronger smoothing reduced turnover.
- Best refined variant had effective test IC 0.037534, effective test IC IR 0.765515, positive window rate 0.75, and turnover proxy 0.128510.
- Plain reversal failed as a counterfactual.
- Simple volume-spike reversal showed some evidence but had extreme turnover.

Interpretation:

The candidate appears to preserve useful liquidity-flow reversal information while reducing the churn of a naive volume-spike reversal.

### Likely Failure Modes

- Turnover remains too high in official implementation.
- The official formula accidentally resembles high-churn simple volume-spike reversal.
- Volume normalization is unstable for thinly traded names.
- Missingness increases because of longer rolling windows.
- Official h20 scoring is weaker than sidecar WFV-style evidence.
- Correlation with generic reversal becomes too high.
- Stress behavior degrades under panic/liquidity regimes.

### Baseline Comparisons Required Later

Required future comparisons:

- `simple_volume_spike_reversal_20`
- `plain_reversal_5_smooth5`
- existing reversal-family signals
- existing liquidity-flow or volume-family signals
- current alpha-pool signals

### What Should Not Change During Implementation

- Do not convert it into a momentum signal.
- Do not remove reversal sign.
- Do not use the high-turnover raw volume-spike version as the registered candidate.
- Do not add regime gating.
- Do not add sector or fundamental dependencies.
- Do not choose parameters after viewing official scoring results.
- Do not relax thresholds if the official stack rejects it.

## 5. Draft Definition for `volatility_surprise_reversal_20_60_smooth`

### Identity

| Field | Draft Definition |
| --- | --- |
| `signal_name` | `volatility_surprise_reversal_20_60_smooth` |
| `signal_family` | `volatility_structure` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `SIDECAR_RESEARCH_SURVIVOR` |
| `registration_status` | `DRAFT_RESEARCH_ONLY` |
| `intended_horizon` | h20 primary; h10 diagnostic |
| `expected_direction` | Reversal weighted by short-vs-long realized volatility surprise |

### Economic Intuition

Short-term realized volatility that rises relative to a longer-term baseline can indicate unstable price discovery, crowded positioning, or temporary risk repricing. When paired with recent return reversal, the signal tests whether volatility-surprise environments make short-term reversals more persistent than plain reversal alone.

This is a volatility-structure reversal candidate. It should not collapse into generic volatility reversal or plain reversal.

### Conceptual Formula

Research semantics to preserve:

1. Compute short-window realized volatility.
2. Compute long-window realized volatility baseline.
3. Measure volatility surprise as short realized volatility relative to long realized volatility.
4. Compute recent return reversal.
5. Weight or interact the reversal component with volatility surprise.
6. Smooth the combined expression.
7. Convert to a cross-sectional score on each date.

Draft formula intent:

```text
short_realized_vol = rolling_volatility(returns, 20)
long_realized_vol = rolling_volatility(returns, 60)
volatility_surprise = short_realized_vol / long_realized_vol
return_reversal_component = -1 * recent_return
raw_signal = return_reversal_component * stabilized_volatility_surprise
signal = rolling_smooth(raw_signal)
cross_sectional_score = rank_or_zscore(signal by date)
```

Draft parameter lock for the next isolated test plan:

- short realized volatility window: 20 trading days
- long realized volatility window: 60 trading days
- smoothing: retain the smoothed sidecar construction, with 5-day smoothing as the initial equivalence target unless the sidecar definition proves otherwise
- primary evaluation horizon: h20
- secondary diagnostic horizon: h10

### Required Input Data

Required OHLCV fields:

- adjusted close or close
- date
- asset identifier

Derived fields:

- daily returns
- recent return
- 20-day realized volatility
- 60-day realized volatility
- volatility surprise ratio or normalized volatility spread
- smoothed combined reversal signal

No options-implied volatility, macro data, sector data, fundamentals, or external risk model should be required.

### Lookback and Transformation Logic

| Component | Draft Research Setting | Purpose |
| --- | --- | --- |
| Short realized volatility | 20 trading days | Captures recent volatility surprise. |
| Long realized volatility | 60 trading days | Provides stable volatility baseline. |
| Reversal component | recent return, implementation to match sidecar definition | Captures mean-reversion direction. |
| Smoothing window | smoothed sidecar construction, initial target 5 trading days | Reduces noise while preserving responsiveness. |
| Scoring transform | cross-sectional rank or z-score by date, consistent with existing signal conventions | Makes scores comparable across assets. |

The 20/60 structure is part of the candidate identity and should not be replaced by a generic volatility reversal without a separate research note.

### Ranking and Sign Convention

Expected sign convention:

- Higher score should favor names with reversal potential under elevated short-vs-long realized volatility.
- Lower score should penalize names where the volatility-surprise-weighted reversal expression is unfavorable.

The signal should express reversal, not continuation. Sign must be specified before official scoring and should not be flipped opportunistically.

### Intended h20 / h10 Behavior

The controlled plan treats h20 as the primary horizon because the candidate was originally framed as a medium-horizon standalone signal and h20 remained credible in refinement.

h10 remains useful as a diagnostic because some nearby volatility-surprise variants showed credible h10 strength. That does not mean the signal should be optimized to h10 before implementation. The initial isolated draft should preserve h20 primary metadata and record h10 only as a secondary horizon-sensitivity check.

### Why It Appears Robust

Evidence from refinement:

- 5 of 5 nearby volatility-surprise variants passed sidecar robustness checks.
- Median effective test IC was 0.044312.
- Median sidecar WFV IR was 0.704639.
- Median turnover proxy was 0.083101.
- Simple volatility reversal failed.
- Plain reversal failed.
- Correlations to broad reversal, LOW_BREADTH, and trend-quality proxies remained low.

Interpretation:

The interaction between volatility surprise and reversal appears to matter. The candidate is not explained well by simple volatility reversal or plain reversal baselines.

### Likely Failure Modes

- Official full-sample IC is too weak.
- h20 and h10 results disagree materially.
- Formula drifts into simple volatility reversal.
- The volatility surprise denominator becomes unstable during very low-volatility periods.
- Stress-state performance reflects generic risk-off exposure rather than unique volatility structure.
- Recovery regimes produce sign instability.
- Smoothing suppresses the useful part of the signal.

### Baseline Comparisons Required Later

Required future comparisons:

- `simple_volatility_reversal_20`
- `plain_reversal_20_smooth5`
- existing volatility-family signals
- existing reversal-family signals
- LOW_BREADTH/trend-quality components
- current alpha-pool signals

### What Should Not Change During Implementation

- Do not remove the 20/60 volatility-surprise structure.
- Do not reduce the signal to plain reversal.
- Do not reduce the signal to generic volatility reversal.
- Do not add regime gating.
- Do not add options-implied volatility or external risk data.
- Do not pick h10 opportunistically unless a separate note justifies a horizon change before official testing.
- Do not relax gates if official validation rejects it.

## 6. Metadata Draft

### `volume_shock_reversal_stable_20`

| Metadata Field | Draft Value |
| --- | --- |
| `signal_name` | `volume_shock_reversal_stable_20` |
| `signal_family` | `liquidity_flow` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `SIDECAR_RESEARCH_SURVIVOR` |
| `registration_status` | `DRAFT_RESEARCH_ONLY` |
| `intended_horizon` | h20 |
| `expected_direction` | reversal |
| `input_data_requirements` | OHLCV: close/adjusted close, volume, date, asset identifier |
| `formula_description` | Smoothed abnormal-volume-weighted return reversal using a stabilized rolling volume baseline. |
| `transformation_notes` | Cross-sectional rank or z-score by date, consistent with existing signal conventions. |
| `smoothing_notes` | Use longer lookback and stronger smoothing from refinement; initial target approximately 40-day volume baseline and 10-day smoothing. |
| `known_risks` | Turnover, generic reversal redundancy, volume normalization instability, weak official full-sample IC. |
| `failure_modes` | Turnover explosion, sign flip, stress collapse, implementation mismatch, hidden reversal duplication. |
| `validation_requirements` | Structural quality, h1/h5/h10/h20 scoring, h20 primary review, turnover sanity, WFV compatibility, stress/regime attribution, orthogonality audit, baseline comparison. |
| `research_source_notes` | `robustness_refinement_three_sidecar_survivors.md`; `controlled_registration_plan_refined_sidecar_survivors.md` |

### `volatility_surprise_reversal_20_60_smooth`

| Metadata Field | Draft Value |
| --- | --- |
| `signal_name` | `volatility_surprise_reversal_20_60_smooth` |
| `signal_family` | `volatility_structure` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `SIDECAR_RESEARCH_SURVIVOR` |
| `registration_status` | `DRAFT_RESEARCH_ONLY` |
| `intended_horizon` | h20 primary; h10 diagnostic |
| `expected_direction` | volatility-surprise-weighted reversal |
| `input_data_requirements` | OHLCV: close/adjusted close, date, asset identifier |
| `formula_description` | Smoothed return reversal interacted with 20-day versus 60-day realized volatility surprise. |
| `transformation_notes` | Cross-sectional rank or z-score by date, consistent with existing signal conventions. |
| `smoothing_notes` | Preserve smoothed sidecar construction; initial target 5-day smoothing unless equivalence review identifies the exact sidecar value differently. |
| `known_risks` | Weak official full-sample IC, h10/h20 ambiguity, volatility proxy duplication, recovery sign instability. |
| `failure_modes` | Horizon instability, formula drift into simple volatility reversal, stress-state sign flip, implementation mismatch. |
| `validation_requirements` | Structural quality, h1/h5/h10/h20 scoring, h20 primary with h10 sensitivity, WFV compatibility, stress/regime attribution, orthogonality audit, baseline comparison. |
| `research_source_notes` | `robustness_refinement_three_sidecar_survivors.md`; `controlled_registration_plan_refined_sidecar_survivors.md` |

## 7. Isolation Requirements

These definitions must remain isolated until a later explicit implementation task authorizes further work.

Isolation rules:

- Treat definitions as research-only.
- Do not register either signal in the production signal factory.
- Do not add either signal to official candidate lists.
- Do not mutate survivor/watchlist artifacts.
- Do not add automatic scoring integration.
- Do not overwrite production tables.
- Do not add portfolio construction usage.
- Do not add ML feature usage.
- Do not route either signal into Conditional-Alpha paths.
- Use a separate future `run_id` and candidate version for any isolated testing.
- Preserve clear separation between sidecar research artifacts and official production outputs.

Recommended future labels:

- `research_only = true`
- `registration_status = DRAFT_RESEARCH_ONLY`
- `source_note = isolated_draft_signal_definitions_refined_survivors`
- `candidate_version = draft_v1_sidecar_refined`

## 8. Future Integration Test Requirements

Before any production signal-factory registration, a later isolated implementation-equivalence plan should verify:

| Test Area | Requirement |
| --- | --- |
| Implementation equivalence | Candidate outputs match the research definition and sidecar semantics. |
| No look-ahead bias | Rolling returns, volume baselines, realized volatility, smoothing, and ranking use only available historical data. |
| Multi-horizon scoring compatibility | h1, h5, h10, and h20 can be evaluated without schema or gate changes. |
| WFV compatibility | Candidate can pass through existing WFV windows, purge/embargo, thresholds, and schemas without special handling. |
| Stress/regime compatibility | Behavior is interpretable in drawdown acceleration, volatility spike, panic/liquidity stress, recovery, trend transition, and rotation regimes. |
| Turnover sanity | Turnover is consistent with sidecar expectations and does not explode after implementation. |
| Orthogonality audit | Correlation to current pool, family proxies, simple reversal, volume, volatility, and LOW_BREADTH/trend signals remains acceptable. |
| Counterfactual attribution | Candidate improves on simpler baselines, not just by relabeling them. |
| Baseline comparison | Required baselines are generated in the same isolated environment. |
| Reproducibility | Results reproduce under the same run ID/version and under cache-enabled reruns. |

The future test plan should explicitly compare:

- draft formula output versus sidecar-intended formula output
- raw versus smoothed variants
- candidate versus simple family baseline
- candidate versus plain reversal baseline
- h20 primary versus h10 sensitivity

The test plan should not define new promotion paths or relaxed thresholds.

## 9. Exclusion Note for `residual_momentum_stability_60`

`residual_momentum_stability_60` is excluded from these draft definitions.

Reason:

- It was classified as `needs redesign`.
- Sidecar evidence was numerically strong but insufficiently unique.
- The refinement diagnostic found high correlation with plain momentum and meaningful overlap with trend-quality/LOW_BREADTH-adjacent exposure.

Current status:

`REDESIGN_RESEARCH_ONLY`

Required before reconsideration:

- mandatory plain momentum baseline control
- stronger residual/relative-value uniqueness test
- reduced trend-quality overlap
- clearer standalone economic distinction

This exclusion is intentional. The project should not create draft production definitions for a candidate whose core information content is not yet distinct.

## 10. Recommended Next Step

Final recommendation:

`isolated implementation-equivalence test plan`

This is the best next move because the candidate semantics are now defined, but the formulas have not yet been proven equivalent to any future implementation.

The next note should specify:

- exact isolated test environment
- expected input artifacts
- output comparison tables
- formula parity checks
- sidecar equivalence checks
- look-ahead checks
- baseline comparison design
- h20/h10 scoring plan
- turnover and orthogonality checks
- pass/fail interpretation for research purposes only

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Deeper robustness testing | Not primary | The immediate need is implementation-equivalence design; robustness testing follows once formulas are isolated. |
| Additional sidecar validation | Not primary | Sidecar evidence is sufficient for draft definition; additional validation without formula parity risks ambiguity. |
| Production registration | Rejected | No official integration should occur before isolated equivalence testing. |
| Pause onboarding research | Rejected | Two candidates remain strong enough to continue controlled onboarding design. |

## Final Definition Conclusion

The two refined survivor candidates now have isolated research definitions:

- `volume_shock_reversal_stable_20`: a smoothed abnormal-volume-weighted reversal candidate with h20 primary intent.
- `volatility_surprise_reversal_20_60_smooth`: a smoothed 20/60 realized-volatility-surprise reversal candidate with h20 primary and h10 diagnostic review.

Both remain research-only. The next step is not registration; it is an isolated implementation-equivalence test plan.
