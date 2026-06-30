# Recent Alpha Research Meta-Review

Date: 2026-05-23

Status: `RESEARCH_META_REVIEW`

## Objective

This note reviews recent Project Underdog alpha research after several branches produced weak or rejected standalone candidates. The goal is to identify what genuinely failed, what remains useful as research evidence, what should be parked, and whether the next best move is another alpha batch or a pause for data, metadata, target, and roadmap work.

This review is intentionally conservative. It does not promote candidates, create new runners, alter detector usage, mutate inventory status, or change validation/governance.

## Branches Reviewed

- Transition-State Alpha Discovery Batch
- Transition-State Composite Detector v1
- Transition-State Conditional Attribution v1
- Transition-State Detector Monitoring v1 and after-inventory-cycle rerun
- `structural_interaction_alpha_discovery_batch_v1`
- `volatility_participation_asymmetry_20_refinement_v1`
- `structural_interaction_alpha_expansion_v2`
- `proxy_relative_residual_alpha_batch_v1`
- `event_defined_liquidity_turnover_exhaustion_alpha_v1`
- Conditional Alpha Inventory Monitoring v2

## Clear Alpha Failures

### Transition-State Standalone Alpha

The standalone transition-state batch tested 10 simple structures around shock absorption, liquidity recovery, dispersion/breadth normalization, and propagation versus absorption. All 10 were `REJECT_RESEARCH`.

The best partial clue, `volatility_spike_decay_absorption_5_10`, was too weak at h5/h10. The branch showed that transition-state micro-signals were not strong standalone alphas in their simple form.

### Passive Or Broad Event Liquidity / Turnover Exhaustion

`event_defined_liquidity_turnover_exhaustion_alpha_v1` rejected all 6 candidates. Event definitions were interpretable, but most triggers still fired too broadly. More selective candidates were negative, sparse, unstable, or overlapped with liquidity / low-volatility behavior.

The strongest weak clue, `turnover_shock_exhaustion_repair_20`, had h20 IC around `0.00493`, but that is not enough to justify refinement.

### Proxy-Relative Residual Structures

`proxy_relative_residual_alpha_batch_v1` was feasible and structurally cleaner than broad absolute-state designs, but it did not produce strong standalone medium-horizon alpha.

The branch confirmed that internal proxy buckets can be built, but liquidity, volatility, residual-volatility, turnover, beta-like, and market-relative proxies were not enough to replace true peer/sector metadata.

### Structural Interaction v2

`structural_interaction_alpha_expansion_v2` showed that smoother interaction design reduced brittleness but did not solve standalone predictive weakness. Seven of eight candidates were rejected, and the only conditional-only clue remained too weak and broad.

## Weak But Meaningful Research Clues

### `volatility_participation_asymmetry_20`

This was the clearest standalone clue from recent discovery:

- h10 IC around `0.00584`
- h20 IC around `0.01215` to `0.01225`
- WFV persistence / sign consistency: `1.00 / 1.00`
- interaction label: `true_interaction_behavior`
- low inventory, reversal, and momentum overlap

However, activation was too broad. Refinement damaged the interaction behavior: tighter participation filters weakened h20 and collapsed the interaction into single-component dominance. Final status: `CONDITIONAL_ONLY_RESEARCH`.

Interpretation: the interaction idea is real enough to preserve, but the current formulation should not be tuned again. Any future return must be a redesign of activation semantics, not threshold tightening.

### `volatility_structure_curvature_stabilization_20`

From structural interaction v2:

- h10 IC: `0.003114`
- h20 IC: `0.006066`
- WFV persistence / sign consistency: `1.00 / 1.00`
- true interaction behavior preserved
- low inventory/reversal/momentum overlap

This is weak research evidence only. It supports the idea that volatility structure shape may matter, but it is too weak and broad for refinement.

### `liquidity_volatility_peer_residual_quality_20`

From proxy-relative residual alpha batch v1:

- h20 IC around `0.00542`
- WFV persistence / sign consistency: `0.75 / 0.75`
- low inventory overlap
- no obvious crisis-only dependency

This supports proxy-relative feasibility but not standalone alpha quality.

### `turnover_shock_exhaustion_repair_20`

From event-defined liquidity/turnover exhaustion:

- h10 IC: `0.002872`
- h20 IC: `0.004927`
- WFV persistence / sign consistency: `0.75 / 0.75`
- low overlap

The clue is too weak and too broad. Preserve only as evidence that event diagnostics are useful; do not refine immediately.

## Useful Context Layers, Not Alphas

### Transition-State Composite Detector

The detector is behaviorally meaningful as a research context layer:

- state labels differentiate benchmark forward returns
- inventory candidate behavior differs by state
- drawdown clustering differs by state
- conditional IC ranges differ by state

But it is not deployment-ready:

- state frequency drift is a watch item
- thin-window warnings remain high
- sign instability remains high
- persistence has only been confirmed inside the same research history, not a genuinely new out-of-sample period

Current status should remain:

`RESEARCH_CONTEXT_LAYER_OBSERVE`

Retain the detector, attribution pass, and monitoring framework as context infrastructure. Do not route it into validation, production, portfolio, ML, blending, or optimization.

## Recurring Failure Modes

1. Broad activation with weak IC.

Many candidates were structurally clean but active on too many dates. Broad activation repeatedly diluted any conditional edge.

2. Sparse events with unstable evidence.

When filters became selective enough to look event-like, IC samples often became too thin or unstable.

3. h5-led or short-lived behavior.

Several transition/shock ideas had any hint of behavior at h5, but h10/h20 carry was weak or negative. h5 evidence should remain diagnostic only.

4. Hidden single-component collapse.

Refinement of `volatility_participation_asymmetry_20` showed that tightening a single component can damage true interaction behavior.

5. Liquidity / low-volatility duplication.

Event and proxy-relative branches often drifted toward liquidity quality, low-volatility/range-volatility, or volatility carry behavior rather than distinct alpha structure.

6. Crisis or state-slice temptation.

Some state slices looked interesting, but were thin, unstable, or confined to known stress windows. These are not enough for promotion.

7. OHLCV-only feature limits.

The most recent branches suggest OHLCV-only data may not distinguish liquidity demand, forced selling, informed participation, real peer-relative behavior, and passive liquidity/volatility effects cleanly enough.

## Healthiest Current Candidates

Conditional Alpha Inventory Monitoring v2 remains the best evidence base.

Current inventory:

1. `participation_breadth_repair_under_hostile_trend`
   - `HEALTHY_ACTIVE_RESEARCH`
   - h20 IC: `0.030720`
   - recent IC: `0.047573`
   - cleanest current inventory anchor

2. `participation_liquidity_state_shift_20_60`
   - `WATCH_MONITOR`
   - h20 IC: `0.028418`
   - recent IC: `0.009171`
   - issue: latest rolling h20 IC much weaker than full-sample h20 IC

3. `volatility_compression_after_stress_stabilization`
   - `WATCH_MONITOR`
   - h20 IC: `0.028391`
   - issue: recent positive-rate weakness and one-window dominance

Inventory-level risks remain:

- h20 horizon concentration
- hostile/stress-state dependence
- participation/breadth co-activation
- two WATCH_MONITOR candidates

The current inventory is still healthier than the recent discovery branches.

## What Should Be Parked

Park these as alpha discovery branches:

- transition-state standalone alpha signals
- structural interaction v2
- proxy-relative residual alpha batch v1
- event-defined liquidity/turnover exhaustion v1
- exact `volatility_participation_asymmetry_20` formulation
- current `volatility_structure_curvature_stabilization_20` formulation
- current proxy-relative residual bucket approach

Retain their artifacts as negative and weak-evidence research history.

## What Should Not Be Refined Again Soon

Do not immediately refine:

- the 10 transition-state standalone structures
- `volatility_participation_asymmetry_20` via stricter thresholds
- structural interaction v2 candidates
- `proxy_relative_residual_alpha_batch_v1`
- `event_defined_liquidity_turnover_exhaustion_alpha_v1`
- h5/h10 micro-shock formulations as standalone alphas

The repeated pattern is not "almost there." It is "diagnosable but structurally underpowered."

## Infrastructure To Retain But Not Deploy

Retain:

- Transition-State Composite Detector
- Transition-State Conditional Attribution runner/artifacts
- Transition-State Detector Monitoring framework
- interaction decomposition diagnostics
- fragility/concentration diagnostics
- proxy bucket construction diagnostics
- event quality diagnostics
- inventory monitoring v2 governance workflow

Do not deploy or route any of these into production, validation, portfolio construction, ML, blending, or optimization yet.

## Most Likely Bottleneck

The bottleneck is not candidate quantity. It is feature and target separability.

Recent work repeatedly built interpretable OHLCV-only mechanisms that were orthogonal and diagnosable, but still too weak. This suggests the current feature set may not cleanly identify:

- true peer-relative behavior
- informed versus uninformed liquidity demand
- forced selling versus ordinary volume expansion
- sector/industry-relative dislocation
- quality or fundamental resilience
- ownership/flow pressure
- event types with distinct economic causes

The second bottleneck is target definition. Many recent candidates asked for standalone cross-sectional IC from subtle state transitions. That may be too demanding without better context or richer data.

## Best Next Research Direction

The best next move is not another immediate alpha batch.

Recommended sequence:

1. Pause broad alpha discovery temporarily.
2. Run or review the next regular inventory monitoring cycle when new or rebuilt data is available.
3. Design a data/metadata enrichment roadmap before launching another discovery batch.
4. Prioritize a trustworthy metadata layer:
   - sector / industry / peer group classifications
   - stable universe membership history
   - liquidity/size cohorts with stronger lineage
   - optional fundamental or quality proxies if available internally
5. Revisit research target definitions:
   - whether future candidates should be standalone alphas
   - whether some context layers should only condition existing inventory behavior
   - whether validation should explicitly separate active repair, stabilization, and post-event continuation targets

If a new alpha family must be designed later, the strongest justification would be a metadata-enabled sector/peer-relative residual framework or a fundamentally enriched repair/stabilization framework. Without that enrichment, another OHLCV-only batch is likely to repeat the same failure modes.

## Final Recommendation

Preserve the current Conditional Alpha Inventory and monitor it. Keep the Transition-State Detector as `RESEARCH_CONTEXT_LAYER_OBSERVE`. Park recent weak alpha branches.

Before more alpha discovery, improve the research substrate: metadata, data enrichment, and target definitions. The project has enough negative evidence to justify a research pause rather than another forced batch.

## Intentional Non-Changes

This meta-review did not:

- implement alpha candidates
- create runners
- modify detector files
- mutate production registration
- change survivor/watchlist state
- alter validation logic, gates, schemas, thresholds, or governance
- route anything into portfolio, ML, blending, or optimization

