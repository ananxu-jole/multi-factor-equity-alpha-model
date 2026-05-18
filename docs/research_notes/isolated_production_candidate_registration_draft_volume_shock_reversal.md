# Isolated Production-Candidate Registration Draft: Volume Shock Reversal

## 1. Executive Takeaway

This note creates a research-only isolated production-candidate registration draft for:

`volume_shock_reversal_stable_20`

It follows `docs/research_notes/controlled_registration_design_update_volume_only.md`, which recommended advancing only the volume candidate while explicitly pausing `volatility_surprise_reversal_20_60_smooth`.

This is not production registration. The signal is not added to the production signal factory, not added to official survivor/watchlist lists, and not routed into portfolio, ML, validation, or Conditional-Alpha paths.

Final recommendation:

`Run an isolated production-candidate scoring and revalidation test for volume_shock_reversal_stable_20 only.`

## 2. Scope and Exclusions

In scope:

- create a controlled production-candidate draft for `volume_shock_reversal_stable_20`
- preserve final signal semantics
- define candidate identity and metadata
- summarize the evidence chain
- carry forward known review items
- define isolated scoring/revalidation requirements
- define safety, rollback, and pause criteria

Out of scope:

- production signal registration
- production code changes
- schema changes
- gate or threshold changes
- survivor/watchlist mutation
- portfolio construction
- ML integration
- Conditional-Alpha implementation
- official WFV writes
- 04A+ execution

Explicitly excluded:

- `volatility_surprise_reversal_20_60_smooth`
- `residual_momentum_stability_60`
- LOW_BREADTH Conditional-Alpha work
- any portfolio or ML usage

## 3. Candidate Registration Identity

| Field | Draft Value |
| --- | --- |
| `signal_name` | `volume_shock_reversal_stable_20` |
| `signal_family` | `liquidity_flow` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `ISOLATED_INTEGRATION_COMPATIBLE_WITH_REVIEW_ITEMS` |
| `proposed_registration_status` | `PRODUCTION_CANDIDATE_DRAFT_NOT_REGISTERED` |
| `intended_horizon` | h20 |
| `expected_direction` | reversal |
| `primary_research_source_notes` | `robustness_first_orthogonal_discovery_batch.md`; `robustness_refinement_three_sidecar_survivors.md`; `isolated_draft_signal_definitions_refined_survivors.md`; `isolated_implementation_equivalence_tests_refined_survivors.md`; `isolated_signal_factory_integration_tests_refined_survivors.md`; `controlled_registration_design_update_volume_only.md` |

Candidate status:

`draft only`

The status should not trigger any automatic scoring, promotion, WFV bridge, survivor/watchlist mutation, or portfolio inclusion.

## 4. Final Signal Semantics

### Conceptual Identity

`volume_shock_reversal_stable_20` is a smoothed abnormal-volume-weighted reversal signal in the liquidity-flow family.

The research thesis:

Large recent return moves that occur with abnormal volume may reflect temporary forced flow, crowding, liquidity demand, or short-term overreaction. When smoothed enough to avoid one-day volume noise, those moves may mean-revert over a medium horizon.

This is a standalone alpha-signal candidate, not a Conditional-Alpha component.

### Required Inputs

Required OHLCV inputs:

- close or adjusted close
- volume
- date
- asset identifier

No required inputs:

- fundamentals
- sector classifications
- options data
- analyst data
- macro data
- borrow data
- external risk model data

### Formula Semantics

The candidate must preserve the following conceptual formula:

```text
recent_return = trailing asset return over the short reversal window
return_reversal_component = -1 * recent_return

volume_baseline = trailing rolling average volume over approximately 40 trading days
volume_shock_component = current_or_recent_volume / volume_baseline
stabilized_volume_shock_component = finite, bounded abnormal-volume measure

raw_signal = return_reversal_component * stabilized_volume_shock_component
stable_signal = trailing rolling smooth(raw_signal, approximately 10 trading days)
cross_sectional_score = rank_or_zscore(stable_signal by date)
```

### Abnormal Volume Logic

The abnormal-volume component should:

- compare current or recent volume against a trailing rolling volume baseline
- use approximately a 40-trading-day baseline
- avoid division by zero
- convert invalid or non-finite values to missing
- avoid allowing extreme volume ratios to dominate the score

The volume component should not become a raw turnover-heavy volume spike formula.

### Reversal Logic

The reversal component should:

- use recent trailing return
- apply a negative sign to express reversal
- favor names whose recent negative return occurred with elevated volume
- penalize names whose recent positive return occurred with elevated volume

The candidate should not be converted into a momentum or continuation signal.

### Stability / Smoothing Logic

The "stable" element should come from:

- stabilized volume normalization
- trailing smoothing of the raw abnormal-volume-weighted reversal expression
- approximately 10 trading days of smoothing

It should not come from:

- regime gating
- LOW_BREADTH activation
- sector filters
- beta overlays
- stress filters
- confirmation layers

### Ranking / Scoring Interpretation

The final signal should be a cross-sectional score by date.

Expected scoring convention:

- higher score: stronger reversal opportunity after elevated-volume negative return
- lower score: weaker or unfavorable elevated-volume reversal setup

The sign convention must be fixed before scoring. It should not be flipped after observing validation results.

### What Must Not Change

Future implementation must not:

- remove the reversal sign
- change the candidate into momentum
- use the high-churn raw volume-spike baseline
- add regime gating
- add sector or fundamental dependencies
- add Conditional-Alpha semantics
- change h20 primary horizon opportunistically
- tune parameters after viewing official validation results
- relax gates or thresholds if the candidate fails

## 5. Evidence Chain Summary

### Robustness-First Orthogonal Discovery

The candidate emerged as a research survivor in the robustness-first orthogonal discovery batch.

Evidence:

- family: `liquidity_flow`
- best horizon: h20
- sidecar WFV effective test IC: 0.026315
- sidecar WFV IR: 0.921072
- positive window rate: 0.75
- strongest orthogonal liquidity-flow candidate
- very low correlation to the then-current pool in discovery review

### Robustness Refinement

The candidate was classified as:

`refined survivor candidate`

Evidence:

- 9 nearby volume-shock/smoothing variants tested
- 7 variants passed sidecar robustness checks
- longer volume-shock lookbacks and stronger smoothing improved turnover behavior
- preferred refined shape: 40-day volume baseline with 10-day smoothing
- best refined effective test IC: 0.037534
- best refined effective test IC IR: 0.765515
- positive window rate: 0.75
- turnover proxy: 0.128510

### Isolated Draft Definitions

The draft definition established:

- OHLCV-only construction
- abnormal-volume-weighted reversal
- h20 primary horizon
- 40-day volume baseline
- 10-day trailing smoothing
- cross-sectional scoring
- no regime gating
- no Conditional-Alpha role

### Implementation-Equivalence Testing

Classification:

`near-equivalent with minor review items`

Evidence:

- formula semantics preserved
- sign convention preserved
- h20 remained strongest
- h20 mean IC: 0.011798
- h20 IC IR: 0.070228
- turnover proxy: 0.098531
- no direct look-ahead found in isolated formula construction

Review item:

- raw sidecar matrices were unavailable, so original raw-value/rank-level parity could not be proven

### Isolated Signal-Factory Integration Testing

Classification:

`integration-compatible with review items`

Evidence:

- metadata complete
- isolated factory-style generation completed
- panel shape: 2098 x 478
- finite pct: 0.965455
- turnover proxy: 0.098531
- value correlation versus equivalence artifact: 1.000000
- mean rank correlation by date versus equivalence artifact: 1.000000
- h20 remained primary
- stress/regime attribution remained coherent

Review item:

- meaningful overlap with unweighted reversal remained, with value correlation around 0.721718

### Volume-Only Controlled Registration Design Update

The design update recommended:

`isolated production-candidate registration draft for volume_shock_reversal_stable_20`

It also paused the volatility candidate and reinforced that this step is not production registration.

## 6. Carried-Forward Review Items

| Review Item | Current Interpretation | Required Future Handling |
| --- | --- | --- |
| Missing raw sidecar matrices | Original raw-value/rank-level sidecar parity cannot be proven. | Compare future draft outputs to isolated equivalence and integration artifacts. |
| Universe/missingness mismatch | Older sidecar summaries had higher missingness than isolated broad-panel outputs. | Document universe and mask assumptions in candidate-only scoring. |
| Reversal overlap | Integration audit found correlation around 0.721718 with unweighted reversal. | Re-audit against reversal proxies and current pool. |
| Turnover sensitivity | Raw/simple volume-spike variants were high churn. | Preserve 40-day baseline and 10-day smoothing; compare to raw spike baseline. |
| WFV compatibility mixed | Isolated h20 WFV compatibility showed persistence/sign consistency around 0.50. | Revalidate in candidate-only WFV diagnostics before any registration. |
| Stress behavior | Stress slices were coherent, but volatility spike positive rate was below 0.50. | Monitor stress windows and avoid overclaiming. |
| Liquidity-flow identity | Candidate must stay more than plain reversal. | Confirm abnormal-volume contribution remains distinct. |
| Same-bar timing | Formula uses same-date close/volume inputs. | Align with platform timing assumptions, likely after-close or next-rebalance usage. |

These are review items, not reasons to relax validation.

## 7. Candidate Metadata Draft

| Metadata Field | Draft Value |
| --- | --- |
| `signal_name` | `volume_shock_reversal_stable_20` |
| `signal_family` | `liquidity_flow` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `formula_description` | Smoothed abnormal-volume-weighted return reversal using a stabilized 40-day rolling volume baseline and 10-day trailing smoothing. |
| `input_data_requirements` | OHLCV: close/adjusted close, volume, date, asset identifier |
| `intended_horizon` | h20 |
| `expected_direction` | reversal |
| `transformation_notes` | Compute abnormal-volume-weighted reversal, apply trailing smoothing, then cross-sectionally rank or z-score by date. |
| `smoothing_notes` | Preserve approximately 40-day volume baseline and 10-day trailing smoothing; no regime gate. |
| `known_risks` | turnover, reversal overlap, universe/missingness mismatch, same-bar timing assumptions, WFV instability |
| `failure_modes` | h20 degradation, turnover increase, stress deterioration, WFV weakening, collapse into plain reversal, implementation drift, suspicious metric improvement |
| `validation_requirements` | isolated production-candidate scoring, h1/h5/h10/h20 review, h20 primary confirmation, WFV/stress revalidation, turnover sanity, orthogonality audit, implementation drift review, no look-ahead/alignment review |
| `research_source_notes` | `robustness_first_orthogonal_discovery_batch.md`; `robustness_refinement_three_sidecar_survivors.md`; `isolated_draft_signal_definitions_refined_survivors.md`; `isolated_implementation_equivalence_tests_refined_survivors.md`; `isolated_signal_factory_integration_tests_refined_survivors.md`; `controlled_registration_design_update_volume_only.md` |
| `proposed_registration_status` | `PRODUCTION_CANDIDATE_DRAFT_NOT_REGISTERED` |
| `rollback_requirements` | preserve draft artifacts, record run ID, formula version, metadata version, validation outputs, drift findings, and pause/rejection reason if onboarding fails |

## 8. Isolated Production-Candidate Test Requirements

Before any actual production registration, the candidate must pass through an isolated production-candidate scoring and revalidation test.

Required test elements:

- isolated production-candidate scoring run
- h20 primary confirmation
- h1/h5/h10/h20 diagnostic review
- WFV/stress revalidation
- turnover sanity check
- orthogonality/redundancy audit
- implementation drift review
- no look-ahead/alignment review
- reproducibility under isolated run ID
- comparison against prior integration artifacts

Suggested future run ID:

`volume_shock_reversal_stable_20_candidate_scoring_v1`

Suggested future artifact namespace:

`artifacts/research/volume_shock_reversal_stable_20_candidate_scoring_v1/`

The future test should remain candidate-only and research-only.

## 9. Safety and Isolation Rules

Required:

- candidate-only research flag
- separate run ID
- isolated artifact directory
- no current-table overwrite
- no automatic promotion
- no survivor/watchlist mutation
- no portfolio integration
- no ML integration
- no Conditional-Alpha integration
- full rollback trail

Strict prohibitions:

- no production registration
- no production signal-factory mutation
- no schema changes
- no gate changes
- no threshold changes
- no validation-logic changes
- no portfolio construction changes
- no 04A+ execution unless a later explicit task authorizes it after standard eligibility

Read-only comparison to existing production artifacts is acceptable only if clearly labeled.

## 10. Failure / Pause Criteria

Pause or reject onboarding if:

- h20 behavior fails to reproduce
- formula drifts from this draft definition
- 40-day volume baseline or 10-day smoothing changes without prior approval
- turnover increases materially
- stress behavior weakens
- WFV behavior deteriorates
- liquidity-flow identity disappears
- signal collapses into plain reversal
- redundancy with existing signals increases
- suspicious metric improvement appears
- unexplained metric degradation appears
- NaN/inf handling creates artificial scores
- same-bar timing introduces alignment risk
- implementation introduces look-ahead risk
- production contamination risk appears
- any step requires gate, threshold, or schema changes

The correct response to failure is pause, redesign, or reject. It is not gate relaxation.

## 11. Exclusion Note for Paused Candidates

`volatility_surprise_reversal_20_60_smooth` does not advance in this draft.

Reasons:

- unresolved h20 drift
- high similarity to simple volatility reversal
- high similarity to plain 20-day smoothed reversal
- persistent redundancy risk
- additional drift/redundancy review is required before any onboarding consideration

Also excluded:

- `residual_momentum_stability_60`
- LOW_BREADTH Conditional-Alpha work
- portfolio construction
- ML usage
- any Conditional-Alpha path

This exclusion is intentional and should remain in force unless a later research note changes the evidence.

## 12. Recommended Next Step

Final recommendation:

`isolated production-candidate scoring and revalidation test`

The next task should run a candidate-only, isolated scoring/revalidation test for:

`volume_shock_reversal_stable_20`

The next test should include:

- h1/h5/h10/h20 scoring
- h20 primary confirmation
- structural quality review
- turnover review
- WFV/stress revalidation
- reversal and liquidity-flow orthogonality audit
- drift comparison against prior integration artifacts
- look-ahead/alignment review
- reproducibility check
- final candidate-only recommendation

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Additional integration review | Not primary | Integration compatibility was already established with review items. |
| Revise candidate definition | Not primary | The definition is stable enough for isolated scoring. |
| Pause onboarding research | Rejected | The evidence chain supports one more controlled candidate-only step. |
| Production registration | Rejected | No production registration should occur before isolated scoring and revalidation. |
| Advance volatility candidate | Rejected | Volatility redundancy remains unresolved. |

## Final Draft Conclusion

`volume_shock_reversal_stable_20` now has a controlled production-candidate draft.

The candidate is not registered. The next step is a candidate-only isolated scoring and revalidation test. The project should continue to advance carefully, preserving validation discipline and keeping the volatility candidate paused.
