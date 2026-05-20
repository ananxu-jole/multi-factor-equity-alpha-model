# Conditional Alpha Inventory v2 Governance Update

## Executive Takeaway

This note formalizes research-only governance for the current Conditional Alpha Inventory before Expansion v3 or any future construction-layer work.

Current inventory:

1. `participation_liquidity_state_shift_20_60`
2. `participation_breadth_repair_under_hostile_trend`
3. `volatility_compression_after_stress_stabilization`

Monitoring v1 showed that the inventory is research-usable but not clean enough to treat as static. The current state is:

| candidate | monitoring classification | governance interpretation |
| --- | --- | --- |
| `participation_liquidity_state_shift_20_60` | `WATCH_MONITOR` | No hard guardrail failure, but latest rolling h20 IC is much weaker than full-sample h20 IC. |
| `participation_breadth_repair_under_hostile_trend` | `HEALTHY_ACTIVE_RESEARCH` | Cleanest current monitoring profile. |
| `volatility_compression_after_stress_stabilization` | `WATCH_MONITOR` | Recent-window positive rate is weak and one-window concentration remains a guardrail issue. |

Inventory-level risks are also explicit: pairwise correlations are low, but co-activation is concentrated between the participation/liquidity and breadth-repair candidates; all three candidates are h20-centered and hostile/stress-state dependent.

Decision: Expansion v3 is allowed only after these risks are acknowledged in a formal readiness checklist. It should remain one-by-one and inventory-aware. Construction-layer work should wait for rebuild/equivalence testing and at least one additional monitoring refresh.

## Scope And Non-Changes

This is a governance update only. It does not create candidates, run discovery, run validation/refinement, register signals, mutate survivor/watchlist status, change gates or schemas, create portfolio construction, introduce ML logic, blend signals, create a weighting engine, or wire production Conditional-Alpha paths.

Primary sources:

- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `artifacts/research/conditional_alpha_inventory_monitoring_v1/`
- `docs/research_notes/inventory_ecosystem_review_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v1.md`
- `docs/research_notes/participation_liquidity_conditional_alpha_integration_review.md`
- `docs/research_notes/participation_breadth_repair_conditional_validation.md`
- `docs/research_notes/volatility_compression_stress_stabilization_integration_review.md`

Reviewed monitoring artifacts:

- `candidate_health_summary.csv`
- `guardrail_status.csv`
- `h20_wfv_monitor_summary.csv`
- `h20_wfv_monitor_windows.csv`
- `coactivation_matrix.csv`
- `inventory_correlation_matrix.csv`
- `inventory_level_summary.csv`
- `inventory_similarity_detail.csv`
- `regime_overlap_summary.csv`
- `wfv_style_summary.csv`
- `missing_artifacts.csv`
- `manifest.json`

The breadth-repair candidate does not yet have a separate integration-review note in this repository. Its locked conditional-validation note is therefore treated as the current fixed-package source until a dedicated integration-review design is created.

## Candidate-Level Governance States

| monitoring state | meaning | allowed behavior | required action |
| --- | --- | --- | --- |
| `HEALTHY_ACTIVE_RESEARCH` | Candidate passes current research guardrails and has no material monitor caution. | Remain in active research inventory; may be referenced by future design notes. | Continue routine monitoring; no promotion implied. |
| `WATCH_MONITOR` | Candidate remains usable but has one or more caution flags or soft fragility. | Remain in inventory, but any future use must mention the watch reason. | Create candidate-specific action plan before Expansion v3 or construction design. |
| `DEGRADED_RESEARCH` | Candidate has one or more hard guardrail failures or repeated soft failures. | Do not use as a primary input to new inventory expansion assumptions. | Run focused diagnostic or downgrade to monitor-only. |
| `REVIEW_FOR_DOWNGRADE` | Candidate has persistent or severe deterioration. | Freeze as historical evidence until reviewed. | Governance review must decide hold, redesign, monitor-only, or retirement. |
| `RETIREMENT_CANDIDATE` | Candidate no longer supports its inventory role. | Remove from active inventory. | Archive evidence and document replacement or closure rationale. |

These states are research governance labels only. They do not change production status.

## Candidate-Level Downgrade Triggers

A candidate should move from `HEALTHY_ACTIVE_RESEARCH` to `WATCH_MONITOR` when any of the following occur:

- Latest rolling h20 IC falls materially below the full-sample h20 IC.
- Recent-window h20 IC is barely positive or inconsistent.
- Recent-window positive IC rate falls below the candidate's guardrail.
- One-window dominance approaches the candidate's guardrail.
- Active coverage remains adequate but shows deterioration.
- Active-window support drifts toward fewer validation windows or fewer valid active dates per window.
- Turnover rises but remains below the hard ceiling.
- Similarity to inventory, reversal, momentum, or volatility baselines increases but remains below ceiling.
- A primary panel must be rebuilt from source artifacts rather than loaded directly.

A candidate should move to `DEGRADED_RESEARCH` when any of the following occur:

- WFV-style persistence or sign consistency drops below the candidate's validation profile.
- Active coverage falls below the documented minimum.
- Active-window support collapses or becomes materially less balanced across validation windows.
- Turnover exceeds the documented ceiling.
- Recent-window h20 IC turns negative in repeated monitoring refreshes.
- One-window dominance exceeds the guardrail and remains concentrated after refresh.
- Baseline similarity drifts above the ceiling.
- State activation no longer matches the documented semantic thesis.
- Rebuild/equivalence testing produces unexplained metric drift.

A candidate should move to `REVIEW_FOR_DOWNGRADE` when:

- Two or more hard guardrails fail in the same monitoring pass.
- The same hard guardrail fails across two consecutive monitoring passes.
- Recent-window weakness persists while full-sample evidence remains dependent on older windows.
- Active windows collapse into too few validation periods.
- A newer candidate duplicates the same mechanism with cleaner monitoring evidence.

A candidate should become a `RETIREMENT_CANDIDATE` when:

- The candidate no longer has a coherent state thesis.
- Rebuild/equivalence fails and cannot be explained.
- It becomes a disguised version of a simpler baseline.
- It loses WFV persistence and sign consistency.
- It is superseded by a cleaner inventory candidate.

## Candidate-Specific Governance Actions

### `participation_liquidity_state_shift_20_60`

Current classification: `WATCH_MONITOR`.

Reason: no hard guardrail failures, but latest rolling h20 IC is much weaker than full-sample h20 IC.

Governance action:

- Keep in active research inventory.
- Require a rolling h20 IC refresh before Expansion v3 references it as a stable anchor.
- Add rebuild/equivalence testing because the monitoring runner rebuilt the primary representation from v4 base artifacts.
- Monitor turnover closely because this candidate remains the highest-turnover inventory member.
- Keep h10/h20 horizon dependency explicit because the primary representation historically had h10 as best horizon while h20 remains the inventory focus.

### `participation_breadth_repair_under_hostile_trend`

Current classification: `HEALTHY_ACTIVE_RESEARCH`.

Reason: cleanest current monitor profile, low turnover, low inventory/reversal overlap, and strong recent-window behavior.

Governance action:

- Keep in active research inventory.
- Do not promote or construction-wire.
- Monitor active coverage because it is the sparsest current inventory candidate.
- Treat confirmation/control variants as controls, not independent inventory members.

### `volatility_compression_after_stress_stabilization`

Current classification: `WATCH_MONITOR`.

Reason: recent-window positive rate is weak and one-window concentration remains a guardrail issue.

Governance action:

- Keep in active research inventory with guardrails.
- Require recent-window refresh before it is used as evidence of stable volatility/stress-transition behavior.
- Require one-window dominance monitoring in every inventory refresh.
- Keep `smooth_5` and `smooth_3` as confirmation/control references, not alternate tuned candidates.
- Do not add new volatility/stress-transition candidates until this candidate's monitoring status is better understood or explicitly accepted as a watch-risk anchor.

## Inventory-Level Governance Rules

### Co-Activation Concentration

Co-activation is a research risk even when value correlations are low. Monitoring v1 showed asymmetric co-activation between the participation/liquidity and breadth-repair candidates:

- `participation_breadth_repair_under_hostile_trend` was active inside `participation_liquidity_state_shift_20_60` active periods at a high rate.
- Pairwise correlations remained low, so this is a state-overlap risk rather than a direct signal-duplication risk.

Governance rule:

- Any pair with co-activation above `0.75` in either direction should be flagged as concentrated.
- If co-activation above `0.75` persists across two monitoring passes, future expansion notes must treat those candidates as sharing activation topology.
- If a pair's co-activation rises materially from the prior monitoring snapshot, it should be flagged as co-activation drift even if the absolute level remains below `0.75`.
- New candidates that primarily activate in the same hostile/weak-breadth window must justify why they add construction optionality.

### State And Horizon Concentration

All three current inventory candidates are h20-centered and perform best in hostile, weak-breadth, drawdown, panic/liquidity, or stress-related states.

Governance rule:

- h20 concentration must be documented before Expansion v3.
- A new candidate should not be favored only because it also works at h20 in the same hostile/stress states.
- Any future construction-layer design must treat the current inventory as conditionally clustered, not diversified by default.

### Hidden Mechanism Clustering

The inventory contains two participation/breadth/liquidity repair candidates and one volatility/stress-transition candidate.

Governance rule:

- Future candidates must be compared against all three current primary panels.
- Low signal correlation is not enough; co-activation, state attribution, and semantic overlap must also be checked.
- Candidate controls should not be counted as independent inventory members.

### Correlation And Similarity Drift

Governance rule:

- Pairwise inventory correlation should be monitored every refresh.
- Similarity to reversal, momentum, volatility, and current inventory baselines should be tracked.
- A candidate should move to `WATCH_MONITOR` if similarity rises materially, even before it crosses a hard ceiling.
- A candidate should move to `DEGRADED_RESEARCH` if similarity breaches its documented ceiling.

### Regime Dependence Drift

Governance rule:

- State attribution must be refreshed before Expansion v3 and before construction-layer design.
- A candidate whose best states migrate away from its documented semantic thesis should be placed in `WATCH_MONITOR`.
- If state labels require repeated reinterpretation to preserve the candidate thesis, the candidate should enter downgrade review.

## Monitoring Cadence

Required monitoring events:

| event | required monitoring |
| --- | --- |
| Before Expansion v3 | Full inventory monitoring refresh, readiness checklist, and explicit risk acceptance. |
| After any candidate is added | Candidate-level health, co-activation matrix, correlation matrix, state overlap, and guardrail status. |
| After major reruns or rebuilds | Rebuild/equivalence test plus monitoring refresh. |
| Before future construction-layer design | Two most recent monitoring snapshots, rebuild/equivalence evidence, and co-activation/state concentration review. |
| After any material data/universe change | Full monitoring refresh and artifact lineage update. |

Routine research cadence should be one monitoring refresh per major research cycle. More frequent monitoring is needed if any candidate is in `DEGRADED_RESEARCH` or `REVIEW_FOR_DOWNGRADE`.

## Rebuild / Equivalence Expectations

Before any candidate feeds future construction-layer design, it must have an isolated rebuild/equivalence record.

Required checks:

- Candidate signal panel reproduction.
- Cross-sectional rank reproduction.
- Date and ticker coverage reproduction.
- NaN/zero inactive handling reproduction.
- State activation reproduction.
- Turnover reproduction.
- h20 IC and positive IC rate reproduction.
- WFV-style persistence/sign consistency reproduction.
- Baseline and inventory similarity reproduction.
- Artifact lineage and run_id/version traceability.

Expected metadata:

- canonical candidate name
- primary variant
- source artifact path
- rebuild run_id
- input data snapshot
- transformation version
- state definition version
- inactive handling convention
- comparison artifact path
- drift summary
- reviewer decision

Failure handling:

- Suspicious metric improvement is a review issue, not a success.
- Unexplained h20 IC, turnover, coverage, or similarity drift should pause construction-layer use.
- Any state-definition change requires semantic review.

## Expansion v3 Readiness Criteria

Expansion v3 may proceed only if all of the following are true:

- No candidate has unresolved hard guardrail failures.
- `WATCH_MONITOR` candidates have documented action plans.
- Co-activation concentration is documented and accepted.
- State and horizon concentration are documented and accepted.
- Rebuild/equivalence plan exists for all current inventory primary variants.
- Expansion v3 concept notes explicitly state which inventory gap is being targeted.
- New concepts are evaluated one-by-one unless a later governance note explicitly approves a batch.
- No candidate is treated as construction-ready.

Current readiness assessment:

| criterion | current status |
| --- | --- |
| no unresolved hard guardrail failures | mostly satisfied; volatility candidate has explicit recent-window / concentration watch items |
| WATCH_MONITOR action plan | satisfied by this note |
| co-activation concentration documented | satisfied by Monitoring v1 and this note |
| state/horizon concentration documented | satisfied by Ecosystem Review v1 and this note |
| rebuild/equivalence plan documented | partially satisfied; design exists here, but tests are not yet run |
| inventory risks explicitly accepted | satisfied for research-only Expansion v3 design; not sufficient for construction-layer work |

Conclusion: Expansion v3 concept design can proceed after this governance update, but implementation should remain one-by-one and should not begin construction-layer work. If Expansion v3 requires using the inventory as a benchmark, run a monitoring refresh first.

## What Must Not Happen Yet

- No production registration.
- No survivor/watchlist mutation.
- No portfolio construction.
- No ML integration.
- No signal blending or weighting engine.
- No optimization engine.
- No production Conditional-Alpha wiring.
- No gate/schema/threshold changes.
- No construction-layer assumptions based only on full-sample IC.

## Final Recommendation

Adopt this v2 governance update as the research-only control layer for Conditional Alpha Inventory monitoring.

Immediate next step: run no new discovery until the team explicitly chooses either:

1. a research-only Expansion v3 concept-screening note that accepts the current inventory risks, or
2. a rebuild/equivalence test plan for the three primary inventory variants.

Construction-layer design should wait for rebuild/equivalence evidence and at least one more monitoring refresh.
