# Track B Priority With Track A Governance Loop

## 1. Executive Takeaway

Project Underdog should make Track B the active execution frontier while keeping Track A alive as a lightweight governance loop.

Final immediate execution recommendation:

`run Track B robustness-first discovery batch`

Track A remains important, but it should not block discovery unless a critical governance issue appears. `volume_shock_reversal_stable_20` has been approved for controlled registration consideration with review items, not for clean production use, portfolio deployment, survivor promotion, or ML usage.

Track B should now restart broader robustness-first standalone alpha discovery using the discipline learned from the onboarding cycle: preserve semantics, test implementation equivalence, treat suspicious improvement as a warning, take redundancy seriously, and require rollback logic before registration.

This note is research/planning only. It does not modify production code, schemas, gates, thresholds, survivor/watchlist lists, portfolio construction, validation logic, ML layers, or Conditional-Alpha paths.

## 2. Current Two-Track Status

### Track A Status

Track A governs:

`volume_shock_reversal_stable_20`

Current decision:

`approve controlled registration with review items`

Track A boundaries:

- no portfolio use
- no ML use
- no clean production promotion
- no survivor/watchlist mutation
- no threshold or gate changes
- no automatic 04A+ execution
- no Conditional-Alpha integration

Primary review items:

- mixed WFV persistence at 0.50
- mixed WFV sign consistency at 0.50
- elevated overlap with unweighted reversal at 0.721718 correlation
- same-bar timing review
- turnover monitoring
- rollback requirements

### Track B Status

Track B resumes broad standalone alpha research.

Current mandate:

- restart robustness-first discovery
- focus on orthogonal standalone candidates
- avoid conditional-alpha semantics
- prioritize candidates that can eventually pass the same onboarding discipline used for the volume candidate

Track B is now the main workstream because the onboarding protocol has been validated enough to run in the background while discovery expands.

## 3. Track B Priority Rationale

Track B should be prioritized for four reasons.

First, Project Underdog still needs more orthogonal standalone candidates. The current research history shows that universal signals are rare, conditional edges can be useful but limited, and the platform needs broader standalone evidence before portfolio or survivor work becomes more meaningful.

Second, the volume candidate decision memo resolved the immediate process question. The candidate is not cleanly deployed, but the onboarding path is now clear enough that it does not require all research capacity.

Third, the strongest current bottleneck is candidate diversity. Track A manages one signal. Track B can create a wider research surface across liquidity-flow, residual/relative-value, volatility-structure redesign, interaction, dispersion-aware, and turnover-aware ideas.

Fourth, discovery can proceed without contaminating Track A. New candidates should not inherit the volume candidate's approval status, and the volume candidate should not be treated as production-ready.

Track B should therefore become the active execution queue, while Track A stays on a periodic governance cadence.

## 4. Track B Discovery Batch Design

### Batch Objective

Run a robustness-first standalone discovery batch that searches for interpretable, orthogonal candidates with:

- persistence
- stress robustness
- horizon stability
- turnover discipline
- attribution clarity
- low baseline redundancy

The batch should not chase raw IC or produce blended constructions. It should produce standalone research candidates that can later enter the validated onboarding protocol if they survive.

### Target Families

Recommended families:

| Family | Candidate Target | Research Goal |
|---|---:|---|
| liquidity-flow | 2 to 3 | Find flow/reversal structures with less plain-reversal overlap than `volume_shock_reversal_stable_20`. |
| residual / relative-value redesign | 2 to 3 | Rebuild residual candidates without excessive trend or momentum entanglement. |
| volatility-structure redesign | 2 | Explore volatility-structure ideas while avoiding simple volatility-reversal duplication. |
| interaction structures | 1 to 2 | Test simple interpretable two-input structures with clear marginal attribution. |
| dispersion-aware standalone signals | 1 to 2 | Evaluate whether dispersion context can stabilize standalone behavior without becoming a conditional gate. |
| turnover-aware standalone signals | 1 to 2 | Search for slower, smoother h10/h20 candidates with controlled churn. |

Total target:

`8 to 12 standalone candidates`

### Horizon Coverage

Primary horizons:

- h10
- h20

Diagnostic horizons:

- h1
- h5

Expected behavior:

- h20 can dominate, but adjacent horizons should remain directionally coherent.
- h1 spikes should not drive candidate selection.
- h10 strength is acceptable if h20 is not directionally contradictory.
- single-horizon outliers should be treated as review items, not evidence of robustness.

### Scoring Approach

For every candidate, compute:

- mean IC by horizon
- absolute mean IC by horizon
- IC IR by horizon
- positive IC rate
- sign consistency
- valid date count
- missingness and finite coverage
- turnover proxy
- concentration proxy if available

Scoring interpretation:

- Favor stable moderate edges over sharp but unstable IC bursts.
- Require coherent sign behavior across adjacent horizons.
- Penalize high turnover unless it clearly preserves signal identity.
- Treat suspicious improvement versus baselines as a warning.

### WFV Approach

Use WFV-style research diagnostics, not production promotion.

Measure:

- effective mean test IC
- effective test IC IR
- persistence
- sign consistency
- window-level train/test degradation
- one-window dominance
- direction flips

WFV expectations:

- Candidates with low persistence should not advance.
- Candidates with weak sign consistency should be rejected or redesigned.
- Stable moderate WFV behavior is better than high average IC from one window.

### Stress / Regime Attribution Approach

Evaluate promising candidates across:

- drawdown acceleration
- volatility spike
- panic/liquidity stress
- trend transition
- recovery phase
- high dispersion / rotation

Interpretation:

- Stress coherence supports candidate interpretation.
- State-specific strength is useful but should not quietly convert the signal into a conditional-alpha candidate.
- Candidates that only work in a sparse state should be routed to side diagnostics, not the standalone path.

### Orthogonality Review

Every candidate should be compared against:

- current pool/watchlist signals
- `volume_shock_reversal_stable_20` as a research baseline only
- unweighted reversal
- plain smoothed reversal
- plain momentum
- simple volume-spike reversal
- simple volatility reversal
- benchmark-relative proxies where relevant

Orthogonality expectations:

- Low correlation alone is not enough; the candidate must have interpretable marginal behavior.
- High baseline similarity requires a clear marginal contribution story.
- Redundant candidates should be rejected early or redesigned.

### Rejection Philosophy

Reject or redesign candidates for:

- direction flips
- weak persistence
- weak sign consistency
- one-window dominance
- suspicious metric improvement
- excessive turnover
- weak interpretability
- hidden trend or momentum duplication
- generic reversal duplication
- generic volatility-reversal duplication
- conditional behavior masquerading as standalone robustness
- blend dependence

Failures should be preserved as research evidence.

### Artifact Outputs

Track B should write isolated research artifacts under a dedicated namespace such as:

`artifacts/research/robustness_first_discovery_expansion_v2/`

Expected artifact outputs:

- candidate registry
- formula/metadata summary
- structural quality summary
- multi-horizon scoring table
- WFV-style diagnostic summary
- WFV window diagnostics
- stress/regime attribution table
- turnover/tradability summary
- orthogonality/redundancy audit
- baseline comparison table
- candidate classification summary
- research note summarizing findings

Suggested research note:

`docs/research_notes/robustness_first_discovery_expansion_v2.md`

## 5. Track A Governance Loop

Track A should stay active, but lightweight.

Purpose:

Keep `volume_shock_reversal_stable_20` governed while Track B proceeds. Track A should only escalate if one of its review items becomes urgent.

### Governance Checkpoints

Track A should periodically review:

- same-bar timing status
- turnover stability
- overlap with unweighted reversal
- WFV/stress behavior
- rollback triggers
- readiness for future controlled registration execution

### Same-Bar Timing Review

Track A should eventually document whether:

- close and volume are known at signal formation time
- signal calculation occurs after close
- ranking occurs after close
- hypothetical rebalance happens next session or later
- smoothing uses only trailing data
- no target leakage occurs through same-bar assumptions

This audit is required before registration-style implementation, but it is not urgent enough to block Track B.

### Turnover Stability

Track A should monitor whether the turnover proxy remains close to the isolated revalidation baseline of 0.098531.

Escalate only if:

- turnover rises materially
- turnover spikes concentrate around stress windows
- smoothing changes signal identity
- implementation drift creates higher churn

### Unweighted Reversal Overlap

Track A should keep the 0.721718 unweighted-reversal correlation as a review anchor.

Escalate only if:

- overlap rises further
- marginal contribution versus plain reversal disappears
- stress behavior is explained entirely by generic reversal
- the signal can no longer be credibly described as liquidity-weighted reversal

### WFV / Stress Behavior

Track A should monitor:

- WFV persistence
- WFV sign consistency
- effective mean test IC
- effective test IC IR
- panic/liquidity stress behavior
- drawdown acceleration behavior
- trend-transition behavior

Current mixed WFV is a review item, not an immediate Track B blocker.

### Readiness For Future Controlled Registration Execution

Track A is ready for a future implementation plan only after:

- timing semantics are resolved
- rollback checklist exists
- overlap audit is documented
- turnover/stress monitoring plan exists
- artifact comparison baseline is preserved
- no promotion or portfolio usage is implied

## 6. Track Separation Rules

Track A and Track B must remain separate.

Required separation:

- separate run IDs
- separate artifact directories
- separate research notes
- separate candidate registries
- no shared promotion logic
- no survivor/watchlist mutation
- no portfolio use
- no ML use
- no Conditional-Alpha use
- no table overwrites
- no production registration
- no gate, schema, or threshold changes

Suggested namespaces:

| Track | Namespace |
|---|---|
| Track A | `volume_shock_reversal_controlled_governance_v1` |
| Track B | `robustness_first_discovery_expansion_v2` |

Track B discoveries should not inherit Track A approval status. Track A approval also should not imply anything about new Track B candidates.

## 7. Cadence Recommendation

Recommended cadence:

- Track B: primary workstream
- Track A: periodic governance checkpoint
- Track A escalation: only when a review item becomes urgent
- Track B discoveries: independent candidate lifecycle

Practical cadence:

1. Run one Track B discovery batch.
2. Summarize Track B findings and classify candidates.
3. Run a short Track A checkpoint only if the volume candidate is about to move toward controlled registration implementation.
4. Do not interleave Track A governance artifacts into Track B scoring outputs.

The project should avoid making Track A an always-on blocker. Governance should protect the process, not freeze discovery.

## 8. Immediate Execution Recommendation

Final recommendation:

`run Track B robustness-first discovery batch`

The next concrete Codex task should be:

Run the Track B robustness-first standalone discovery expansion batch under an isolated research namespace, likely:

`robustness_first_discovery_expansion_v2`

Track A should remain in the background as a governance loop. Create a short Track A governance checkpoint note only if a specific review item becomes urgent or the project is ready to move toward controlled registration implementation.

Do not run production registration. Do not mutate survivor/watchlist lists. Do not use the volume candidate in portfolio or ML workflows.

## 9. Strategic Outlook

The volume candidate onboarding cycle has done its job: it validated a disciplined pathway from sidecar discovery to controlled registration consideration while preserving rejection discipline and review controls.

Now Project Underdog should reopen the alpha discovery funnel, but with sharper filters:

- candidate semantics must be clear before implementation
- baselines must be defined early
- suspicious improvement must be investigated
- WFV persistence and sign consistency matter more than headline IC
- turnover improvements must preserve identity
- orthogonality must be demonstrated, not assumed

Track B should become the next main research push. Track A should keep the volume signal from drifting into premature deployment.
