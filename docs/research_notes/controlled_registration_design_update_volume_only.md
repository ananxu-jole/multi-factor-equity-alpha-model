# Controlled Registration Design Update: Volume Candidate Only

## 1. Executive Takeaway

This note updates the controlled production-registration design for one candidate only:

`volume_shock_reversal_stable_20`

The update follows the asymmetric evidence from the isolated signal-factory integration tests. `volume_shock_reversal_stable_20` remains the cleaner onboarding candidate and is suitable for a controlled production-candidate registration draft, still without production registration.

Do not advance:

`volatility_surprise_reversal_20_60_smooth`

That candidate remains paused because high baseline similarity and suspicious h20 improvement are unresolved.

Final recommendation:

`Create an isolated production-candidate registration draft for volume_shock_reversal_stable_20 only.`

This is not production registration. No production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha paths should be changed.

## 2. Evidence Chain Summary

### Robustness-First Orthogonal Discovery

`volume_shock_reversal_stable_20` emerged from the robustness-first orthogonal standalone discovery batch as the strongest liquidity-flow survivor candidate.

Key evidence:

- family: `liquidity_flow`
- best horizon: h20
- sidecar WFV effective test IC: 0.026315
- sidecar WFV IR: 0.921072
- positive window rate: 0.75
- max observed correlation to current pool: about 0.081847
- primary reason: strongest orthogonal liquidity-flow window stability

The signal was not registered into production and did not mutate any survivor/watchlist table.

### Robustness Refinement

The refinement diagnostic classified the candidate as:

`refined survivor candidate`

Key evidence:

- 9 nearby volume-shock/smoothing variants tested
- 7 variants passed sidecar robustness checks
- median effective test IC: 0.024214
- median sidecar WFV IR: 0.893190
- longer volume-shock lookbacks and stronger smoothing reduced turnover
- best refined form: `volume_shock_reversal_stable_s40_sm10`
- best refined effective test IC: 0.037534
- best refined effective test IC IR: 0.765515
- best refined positive window rate: 0.75
- best refined turnover proxy: 0.128510

The refinement also showed that the raw simple volume-spike reversal baseline had high churn, so the stable/smoothed form should be preserved.

### Isolated Draft Definition

The isolated draft definition preserved the intended research semantics:

- abnormal-volume-weighted reversal
- OHLCV-only
- 40-day volume baseline as the refined research shape
- 10-day trailing smoothing
- h20 primary horizon
- higher score favors reversal after elevated-volume negative return
- no regime gating
- no Conditional-Alpha semantics
- no sector or fundamental dependencies

The draft status remains:

`DRAFT_RESEARCH_ONLY`

### Implementation-Equivalence Testing

The implementation-equivalence test classified the candidate as:

`near-equivalent with minor review items`

Key evidence:

- formula semantics preserved
- sign convention preserved
- h20 remained strongest
- h20 mean IC: 0.011798
- h20 IC IR: 0.070228
- h20 positive IC rate: 0.513300
- turnover proxy: 0.098531
- no direct look-ahead found in formula construction

Review item:

- raw sidecar matrices were unavailable, so raw-value/rank-level parity against the original sidecar could not be proven
- missingness differed materially versus old sidecar summaries, likely due universe/mask differences

### Isolated Signal-Factory Integration

The isolated signal-factory integration test classified the candidate as:

`integration-compatible with review items`

Key evidence:

- metadata complete
- isolated factory-style generation completed
- panel shape: 2098 rows x 478 tickers
- missing pct: 0.034545
- finite pct: 0.965455
- date coverage: 0.977121
- turnover proxy: 0.098531
- value correlation versus equivalence artifact: 1.000000
- mean rank correlation by date versus equivalence artifact: 1.000000
- max absolute panel difference: 0.000000
- h20 remained primary
- stress slices remained coherent

Main review item:

- meaningful overlap with unweighted reversal, with value correlation around 0.721718

Interpretation:

The evidence chain is not perfect, but it is coherent enough to justify a controlled production-candidate registration draft. It does not justify production registration yet.

## 3. Volatility Candidate Pause Rationale

`volatility_surprise_reversal_20_60_smooth` should not advance in this design update.

Pause reasons:

- suspicious h20 metric improvement versus older sidecar reference
- persistent high similarity to simple volatility reversal
- persistent high similarity to plain 20-day smoothed reversal
- value correlation with plain 20-day smoothed reversal around 0.986812
- value correlation with simple volatility reversal around 0.895941
- unresolved redundancy risk
- h10 WFV diagnostic looked stronger than h20, creating horizon ambiguity
- additional drift/redundancy review is required before any onboarding consideration

This pause is intentional. The candidate remains viable for research, but it should not enter controlled production-registration design until its independent information content is clearer.

## 4. Registration Preconditions

Before any future production registration of `volume_shock_reversal_stable_20`, all of the following must be true:

| Precondition | Required State |
| --- | --- |
| Stable formula definition | The production-candidate draft must preserve abnormal-volume-weighted reversal with 40-day volume baseline and 10-day trailing smoothing. |
| Locked parameters | Volume baseline, reversal window, smoothing window, clipping, ranking, and NaN handling must be fixed before any official run. |
| h20 primary horizon | h20 must remain the primary horizon and must not be changed opportunistically. |
| Validated metadata | Required metadata package must be complete and marked as research / draft until explicit approval. |
| Isolated integration behavior | Factory-style isolated generation must remain reproducible against the current artifacts. |
| No look-ahead risk | Rolling volume, returns, smoothing, ranking, and forward-return alignment must use only available data. |
| Manageable turnover | Turnover must remain closer to the stable refined form than the raw simple volume-spike baseline. |
| Liquidity-flow identity | Candidate must retain abnormal-volume reversal content and not collapse into plain reversal. |
| Reproducible scoring/WFV behavior | Scoring and WFV-style diagnostics must reproduce under a fixed run ID and version. |
| Orthogonality review | Reversal overlap must be measured against existing signals and simple baselines. |
| Rollback path | A documented rollback/pause path must exist before any production-adjacent draft is tested. |

No gate should be relaxed for this candidate. Failure at any stage is valid research evidence.

## 5. Candidate Metadata Package

Draft metadata package:

| Metadata Field | Draft Value |
| --- | --- |
| `signal_name` | `volume_shock_reversal_stable_20` |
| `signal_family` | `liquidity_flow` |
| `signal_version` | `draft_v1_sidecar_refined` |
| `research_status` | `ISOLATED_INTEGRATION_COMPATIBLE_WITH_REVIEW_ITEMS` |
| `intended_horizon` | h20 |
| `expected_direction` | reversal |
| `input_data_requirements` | OHLCV: close/adjusted close, volume, date, asset identifier |
| `formula_description` | Smoothed abnormal-volume-weighted return reversal using a stabilized rolling volume baseline. |
| `smoothing_notes` | 40-day rolling volume baseline; 10-day trailing smoothing; no regime gate. |
| `known_risks` | turnover, reversal overlap, universe/missingness mismatch versus sidecar reference, same-bar timing assumptions |
| `failure_modes` | turnover increase, h20 degradation, WFV instability, stress deterioration, collapse into plain reversal, implementation drift, suspicious metric improvement |
| `validation_requirements` | structural quality, h1/h5/h10/h20 scoring, h20 primary review, turnover sanity, WFV/stress revalidation, orthogonality audit, reproducibility check |
| `research_source_notes` | `robustness_first_orthogonal_discovery_batch.md`; `robustness_refinement_three_sidecar_survivors.md`; `isolated_draft_signal_definitions_refined_survivors.md`; `isolated_implementation_equivalence_tests_refined_survivors.md`; `isolated_signal_factory_integration_tests_refined_survivors.md` |
| `registration_status` | `PRODUCTION_CANDIDATE_DRAFT_NOT_REGISTERED` |

The registration status is descriptive only. It must not trigger automatic inclusion in production scoring or promotion paths.

## 6. Controlled Onboarding Workflow

### Stage 0 - Research Survivor

Status:

- discovered in sidecar research
- survived robustness-first discovery
- not registered
- not promoted

Exit condition:

- research evidence supports a controlled draft path

### Stage 1 - Isolated Integration-Compatible Candidate

Current state.

Evidence:

- isolated implementation-equivalence test completed
- isolated signal-factory integration test completed
- candidate classified as `integration-compatible with review items`

Exit condition:

- production-candidate draft package is created, still outside production registration

### Stage 2 - Production-Candidate Draft

Create a production-candidate draft for `volume_shock_reversal_stable_20` only.

Allowed:

- draft metadata package
- draft candidate specification
- isolated candidate-only run plan
- rollback criteria

Not allowed:

- production signal registration
- mutation of official candidate lists
- automatic scoring integration
- survivor/watchlist mutation

Exit condition:

- candidate-only draft is ready for isolated production-candidate scoring

### Stage 3 - Isolated Production-Candidate Scoring Run

Run candidate-only scoring in a separate namespace.

Required:

- h1/h5/h10/h20 scoring
- h20 primary interpretation
- structural quality review
- turnover review
- sidecar/equivalence/integration drift comparison

Exit condition:

- scoring reproduces the intended direction and does not show unexplained drift

### Stage 4 - WFV / Stress Revalidation

Run candidate-only WFV/stress revalidation in isolation.

Required:

- preserve existing WFV windows
- preserve purge/embargo assumptions
- preserve thresholds and gates as references only
- no official WFV table writes unless explicitly authorized later
- stress slices for drawdown acceleration, volatility spike, panic/liquidity stress, trend transition, recovery, and high dispersion / rotation

Exit condition:

- WFV/stress behavior is documented and compatible with the research thesis

### Stage 5 - Orthogonality / Redundancy Re-Audit

Re-audit against:

- unweighted reversal
- simple volume-spike reversal
- no-stability volume version
- existing alpha-pool signals
- current survivor/watchlist signals as read-only references
- major liquidity-flow, reversal, volatility, and trend-quality families

Exit condition:

- distinct liquidity-flow contribution is still plausible

### Stage 6 - Production Registration Decision Review

Only after the prior stages should a separate decision review consider whether to authorize actual production registration.

Possible outcomes:

- approve controlled production registration
- keep as research candidate
- request formula/metadata revision
- run deeper sidecar validation
- reject onboarding

No stage should mutate official survivor/watchlist lists until explicitly approved by a later implementation task.

## 7. Isolation and Safety Rules

Future onboarding work must use:

- separate `run_id`
- candidate-only research flag
- isolated namespace
- isolated output artifacts
- `registration_status = PRODUCTION_CANDIDATE_DRAFT_NOT_REGISTERED`
- explicit rollback trail

Strict prohibitions:

- no production registration
- no automatic promotion
- no portfolio integration
- no ML integration
- no Conditional-Alpha integration
- no overwriting current production tables
- no survivor/watchlist mutation
- no threshold changes
- no gate changes
- no schema changes
- no 04A+ run unless a later explicit task authorizes it after standard eligibility

Suggested future namespace:

`artifacts/research/volume_shock_reversal_stable_20_registration_draft_v1/`

Suggested future run ID:

`volume_shock_reversal_stable_20_registration_draft_v1`

Rollback requirements:

- record formula version
- record metadata version
- record input snapshot
- record scoring/stress/WFV artifacts
- record rejection or pause reason if any stage fails

## 8. Review Items Carried Forward

Remaining review items:

| Review Item | Why It Matters | Required Future Handling |
| --- | --- | --- |
| Near-equivalence status | Raw sidecar matrices were unavailable, so original raw-value parity cannot be proven. | Compare future draft output to isolated equivalence and integration artifacts. |
| Universe/missingness mismatch | Sidecar summaries had materially higher missingness than isolated broad-panel outputs. | Document universe/mask assumptions in candidate-only scoring. |
| Reversal overlap | Integration audit found value correlation around 0.721718 with unweighted reversal. | Re-audit against reversal proxies and current pool before registration. |
| Turnover sensitivity | Raw/simple volume-spike versions were high churn. | Preserve 40-day baseline and 10-day smoothing; compare against raw spike baseline. |
| WFV compatibility mixed | Isolated h20 WFV compatibility showed persistence/sign consistency of 0.50. | Revalidate with controlled candidate-only WFV diagnostics. |
| Stress consistency | Stress slices were coherent, but volatility spike positive rate was below 0.50. | Review stress windows and avoid overclaiming robustness. |
| Same-bar timing | Formula uses same-date close/volume inputs. | Match platform timing assumptions, likely after-close or next-rebalance usage. |

These review items should accompany the candidate into the next draft stage. They are not reasons to relax gates.

## 9. Failure / Pause Criteria

Pause or reject future onboarding if:

- h20 behavior cannot be reproduced
- formula drifts from the draft definition
- 40-day volume baseline or 10-day smoothing changes without prior approval
- turnover increases materially
- WFV behavior weakens
- stress behavior deteriorates
- liquidity-flow identity disappears
- candidate collapses into plain reversal
- redundancy with existing signals increases
- implementation introduces suspicious metric improvement
- implementation introduces unexplained metric degradation
- NaN/inf handling creates artificial scores
- same-bar timing cannot be reconciled with platform execution assumptions
- production contamination risk appears
- any future stage requires gate, threshold, or schema changes

Failure should be documented, not worked around.

## 10. Expected Future Artifacts

Before actual production registration is considered, the following artifacts should exist:

- production-candidate metadata draft
- isolated candidate registry row
- isolated candidate scoring report
- structural quality report
- h1/h5/h10/h20 scoring comparison
- WFV/stress revalidation report
- orthogonality audit
- reversal-baseline comparison
- turnover comparison
- drift review log
- look-ahead/alignment review
- registration decision memo
- rollback note

Suggested artifact namespace:

`artifacts/research/volume_shock_reversal_stable_20_registration_draft_v1/`

The artifacts should remain research-only unless a later explicit production-registration task authorizes a different path.

## 11. Recommended Next Step

Final recommendation:

`isolated production-candidate registration draft for volume_shock_reversal_stable_20`

The next task should create a candidate-only draft package containing:

- locked formula specification
- metadata package
- isolated run plan
- validation checklist
- drift comparison plan
- rollback criteria
- explicit non-registration statement

Do not include:

- `volatility_surprise_reversal_20_60_smooth`
- `residual_momentum_stability_60`
- LOW_BREADTH or Conditional-Alpha components

Rejected next moves:

| Option | Decision | Reason |
| --- | --- | --- |
| Additional integration review | Not primary | Integration compatibility was sufficient for the volume candidate. |
| Deeper sidecar validation | Not primary | Useful only if the next draft stage exposes drift or redundancy failure. |
| Pause onboarding research | Rejected | The volume candidate has a coherent enough evidence chain for the next draft layer. |
| Production registration | Rejected | This note is design-only; compatibility is not registration approval. |
| Advance volatility candidate | Rejected | Volatility redundancy and suspicious h20 drift remain unresolved. |

## Final Design Conclusion

`volume_shock_reversal_stable_20` is now the only refined survivor candidate suitable for a controlled production-candidate draft.

The project should move one step forward, not jump to registration:

- draft the volume candidate package
- keep all work isolated
- preserve h20 primary behavior
- monitor turnover, WFV, stress, and reversal overlap
- keep volatility paused

This keeps Project Underdog aligned with its validation-first philosophy: promising evidence can advance, but unresolved redundancy does not get waved through.
