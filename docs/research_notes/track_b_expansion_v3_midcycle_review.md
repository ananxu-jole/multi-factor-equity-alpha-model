# Track B Expansion v3 Mid-Cycle Review

## Executive Takeaway

Expansion v3 has not yet solved the Conditional Alpha Inventory's concentration risks. The program successfully tested calmer-state, non-hostile, non-h20 concepts one by one without production contamination, but the empirical evidence is mixed:

| concept | final classification | mid-cycle interpretation |
| --- | --- | --- |
| `neutral_accumulation_without_breakout` | `REJECT_RESEARCH` | Structurally orthogonal, but no usable neutral-state edge. |
| `calm_regime_relative_stability_10` | `CONDITIONAL_REFINEMENT_CANDIDATE` | Only promising calm-state result; h10 is positive, but h20 dominates and active coverage remains sparse. |
| `quiet_liquidity_accumulation_non_hostile` | `REJECT_RESEARCH` | Cleanly avoided hostile liquidity repair, momentum, reversal, and breakout continuation, but h5/h10 were negative and quiet-state attribution failed. |

Recommendation: `redesign calm-state concepts before testing more`.

Do not continue immediate one-by-one tests of passive accumulation, quiet liquidity, or generic non-hostile participation concepts. Do not pivot wholesale back to hostile/stress repair yet. The current evidence says calm/non-hostile alpha is not broadly available through passive accumulation or liquidity quality, but it may still exist through relative stability, low-volatility quality, or resolved-transition mechanisms.

No new candidate implementation, validation/refinement run, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.

## Sources Reviewed

- `docs/research_notes/track_b_expansion_v3_design_screening.md`
- `docs/research_notes/neutral_accumulation_without_breakout_v1.md`
- `docs/research_notes/calm_regime_relative_stability_10_v1.md`
- `docs/research_notes/calm_regime_relative_stability_10_refinement.md`
- `docs/research_notes/quiet_liquidity_accumulation_non_hostile_v1.md`
- `docs/research_notes/conditional_alpha_inventory_monitoring_v1.md`
- `docs/research_notes/conditional_alpha_inventory_v2_governance_update.md`
- `docs/research_notes/inventory_ecosystem_review_v1.md`

## Current Inventory Context

Current Conditional Alpha Inventory:

1. `participation_liquidity_state_shift_20_60`
2. `participation_breadth_repair_under_hostile_trend`
3. `volatility_compression_after_stress_stabilization`

The inventory identity remains clear:

- It is h20-centered.
- It is strongest in hostile, weak-breadth, drawdown, panic/liquidity, stress, or post-stress stabilization states.
- It contains a participation/breadth/liquidity repair cluster plus one volatility/stress-transition candidate.
- Pairwise correlations are low, but co-activation and state topology are not fully diversified.
- Two candidates remain under `WATCH_MONITOR`, so expansion should not assume the current inventory is static or fully stable.

Expansion v3 was designed to challenge that identity by looking for calmer-state, non-hostile, shorter-horizon or medium-horizon mechanisms.

## What Expansion v3 Has Learned

### Calm-State Accumulation Evidence

`neutral_accumulation_without_breakout` rejected the first passive neutral-accumulation thesis.

Key facts:

- h5 mean IC: `-0.004963`
- h10 mean IC: `-0.000487`
- h20 mean IC: `0.000644`
- WFV persistence/sign consistency: `0.25 / 0.75`
- active date ratio: `0.376549`
- max inventory corr: `0.047560`
- max breakout-continuation corr: `0.108226`
- positive neutral-state count: `0`

Interpretation: the formulation successfully avoided breakout continuation, momentum, reversal, and current inventory overlap. That makes the rejection informative. The failure was not because the signal duplicated something obvious; it failed because neutral accumulation did not predict returns in the tested structure.

### Calm Relative Stability Evidence

`calm_regime_relative_stability_10` remains the only promising Expansion v3 concept so far.

Original v1:

- h10 mean IC: `0.013559`
- h10 positive IC rate: `0.546429`
- h20 mean IC: `0.022079`
- WFV persistence/sign consistency: `0.75 / 0.75`
- active date ratio: `0.133460`
- max inventory corr: `0.032238`
- max low-volatility corr: `0.247124`

Best refinement variant, `smooth_3_rebalance_10_zero`:

- h10 mean IC: `0.013765`
- h10 positive IC rate: `0.546429`
- h20 mean IC: `0.023395`
- WFV persistence/sign consistency: `0.75 / 0.75`
- active date ratio: `0.133460`
- max inventory corr: `0.031758`
- max low-volatility corr: `0.249905`
- one-window dominance: `0.609014`

Interpretation: calm-state edge may exist through ordered relative stability rather than passive accumulation. But this still does not solve the inventory's h20 concentration. The best behavior is h20, the active window is sparse, and one-window dominance remains high enough to block validation readiness.

### Quiet Liquidity Evidence

`quiet_liquidity_accumulation_non_hostile` rejected the non-hostile liquidity accumulation thesis in this formulation.

Key facts:

- h5 mean IC: `-0.004866`
- h10 mean IC: `-0.002841`
- h20 mean IC: `0.003278`
- WFV persistence/sign consistency: `0.25 / 0.75`
- active date ratio: `0.116778`
- max inventory corr: `0.002310`
- max liquidity-repair corr: `0.002310`
- max price momentum corr: `0.034308`
- max breakout-continuation corr: `0.026798`
- positive quiet-state count: `0`

Interpretation: this was a clean falsification of the intended mechanism. It did not copy hostile liquidity repair, current inventory, momentum, reversal, or breakout continuation. But the quiet-state slices were negative, while stronger attribution appeared only in tiny hostile/stress slices. That is semantically wrong for the concept.

### h10 Versus h20 Behavior

Expansion v3 has not yet found a clean h10-centered candidate.

| concept | intended horizon | observed behavior |
| --- | --- | --- |
| `neutral_accumulation_without_breakout` | h5-h10 | h5 was most negative; h10/h20 flat. |
| `calm_regime_relative_stability_10` | h10 | h10 positive, but h20 materially stronger. |
| `quiet_liquidity_accumulation_non_hostile` | h5-h10 | h5/h10 negative; h20 only weakly positive. |

The project should treat h10 diversification as unresolved, not solved. The clearest evidence continues to appear at h20, even for the best calm-state result.

### State Dependence

The two rejected concepts failed inside their intended calm/neutral states. Their most positive state slices were either tiny, hostile/stress-adjacent, or not useful enough to support the thesis.

The relative-stability concept is different: it showed positive calm/normal-dispersion attribution, but still with sparse activation and h20 dominance. That suggests calm-state mechanisms may need cross-sectional order or stability structure, not passive liquidity or accumulation features.

### Orthogonality Versus Predictive Value

Expansion v3 strongly reinforces an older inventory lesson: orthogonality is necessary, but not sufficient.

The rejected concepts were structurally useful as diagnostics because they avoided common duplication traps. But low similarity did not create alpha. The current inventory should not accept candidates merely because they reduce correlation, co-activation, or semantic overlap. They must also show predictive behavior in the intended states.

## Calm / Non-Hostile Diversification Assessment

| question | assessment |
| --- | --- |
| Is calm/non-hostile diversification genuinely weak? | Passive calm accumulation and quiet liquidity look weak in the tested forms. Broad calm/non-hostile diversification is not yet empirically supported. |
| Is it under-specified? | Partly. The rejected concepts may be too generic: accumulation and liquidity quality without a sharper quality/stability selection layer did not work. |
| Is it too sparse? | Sparsity is not the only issue. Neutral accumulation had medium coverage but still failed. Quiet liquidity and calm stability were sparse, but calm stability still showed edge. |
| Is it horizon-misaligned? | Yes. The best calm-state evidence remains h20-heavy. The hoped-for h5/h10 diversification has not appeared. |
| Is it still promising only through relative stability? | Current evidence says yes. Relative stability is the only live calm-state thread, and even that is unresolved. |

## Comparison To Current Inventory Identity

The current inventory is not diversified in the way Expansion v3 wanted, but it is coherent:

- Hostile/stress repair has repeatedly produced stronger evidence than passive calm-state accumulation.
- Participation/breadth repair remains the cleanest monitored profile through `participation_breadth_repair_under_hostile_trend`.
- Liquidity repair seems more useful when attached to hostile or weak-breadth transitions than when moved into quiet non-hostile states.
- Volatility/stress stabilization remains useful but under monitoring watch because of recent-window fragility and one-window concentration.

Expansion v3 so far suggests the inventory's repair/stabilization identity is not an accident. It may reflect where the current universe/framework has the most exploitable conditional structure. But the relative-stability result prevents a full retreat from calm-state research.

## Updated Research Beliefs

### What Seems Durable

- Conditional repair/stabilization under hostile or stressed transitions remains the strongest inventory pattern.
- State semantics matter more than signal novelty.
- Turnover control through rebalance, smoothing, or rank persistence remains useful when the underlying state mechanism is valid.
- Low pairwise correlation does not prove ecosystem value.
- Relative stability in calm regimes is more promising than passive accumulation or quiet liquidity.

### What Repeatedly Fails

- Passive neutral accumulation without a stronger selection layer.
- Quiet non-hostile liquidity accumulation.
- Attempts to force liquidity/participation logic into calm regimes without repair semantics.
- Shorter-horizon h5/h10 calm mechanisms, at least in the tested forms.
- Structurally orthogonal concepts that lack supportive state attribution.

### What Remains Unresolved

- Whether calm relative stability can become validation-ready after monitoring, not immediate further tuning.
- Whether h10 diversification is feasible in this framework.
- Whether low-volatility quality persistence is genuinely different from calm relative stability or just a softer duplicate.
- Whether post-normalization behavior after stress has fully resolved can bridge stress repair and calm-state selection.
- Whether active-window fragility in current inventory should be addressed before further expansion.

## Recommended Path

Recommendation: `redesign calm-state concepts before testing more`.

This means:

- Do not continue immediate Expansion v3 one-by-one implementation.
- Do not run another refinement pass on `calm_regime_relative_stability_10` right now.
- Do not pivot fully back to hostile/stress repair while two inventory candidates are already under `WATCH_MONITOR`.
- Do not add more non-hostile liquidity, passive accumulation, or participation-quality concepts in their current design family.
- Use this mid-cycle point to revise the remaining Expansion v3 queue around more selective mechanisms.

The next research cycle should begin only after a short design update that separates three families:

1. Passive calm-state accumulation: deprioritize.
2. Calm-state relative stability / quality persistence: keep alive, but require h10 and active-window evidence.
3. Resolved-transition stabilization: allow one carefully designed bridge concept if it is not active-stress repair.

## If Expansion v3 Continues

Continue only after redesign. The next 1-2 concepts should be:

| priority | concept | reason |
| --- | --- | --- |
| 1 | `post_normalization_continuation_resolved_stress` | Best bridge between current inventory strength and diversification goal. It does not pretend calm alpha is passive; it waits for stress to resolve and tests whether stabilization continues after the repair window. |
| 2 | `low_volatility_quality_persistence_10` | Closest conceptual neighbor to the only successful calm-state evidence, but must be explicitly separated from low-vol beta and `calm_regime_relative_stability_10`. |

Concepts to defer:

- `non_hostile_participation_quality_10`: too close to the failed quiet-liquidity and neutral-accumulation evidence unless redesigned.
- `low_dispersion_leadership_quality_10`: possible future test, but leadership definitions risk drifting into momentum.
- `volatility_normalization_without_panic_trigger`: hold until the current volatility/stress candidate receives another monitoring pass.

## If Pausing

A pause is also defensible. If the team pauses Expansion v3, the next required work should be monitoring/governance, not discovery.

Monitor first:

- Rolling h20 IC drift for `participation_liquidity_state_shift_20_60`.
- Recent positive-rate and one-window dominance for `volatility_compression_after_stress_stabilization`.
- Active-window drift for all three inventory candidates.
- Co-activation drift between participation/liquidity and breadth repair.
- Whether `calm_regime_relative_stability_10` remains stable as research evidence without being promoted.
- Rebuild/equivalence checks for candidate panels and monitoring artifacts.

Expansion should resume only if the inventory remains research-usable and the next concept has an explicit diversification thesis that does not repeat failed passive calm-state logic.

## If Pivoting

Do not pivot to more generic hostile/stress repair variants. The inventory already has enough repair concentration.

A responsible pivot frontier would be:

- resolved-stress normalization after the active stress window is over,
- quality persistence after state stabilization,
- repair mechanisms with materially different active windows from participation/breadth repair,
- lower-turnover transition mechanisms that are not weak-breadth clones,
- h10-h15 state transitions that do not depend on raw continuation or simple reversal.

The pivot should be from passive calm-state mechanisms toward resolved-transition stabilization, not toward more active-stress repair clones.

## Mid-Cycle Decision

Expansion v3 should not treat the current rejection pattern as proof that calm states are useless. It should treat it as proof that passive calm accumulation and quiet non-hostile liquidity are not enough.

Current decision:

- Keep `neutral_accumulation_without_breakout` rejected.
- Keep `quiet_liquidity_accumulation_non_hostile` rejected.
- Keep `calm_regime_relative_stability_10` as `CONDITIONAL_REFINEMENT_CANDIDATE`, not validation-ready.
- Pause immediate one-by-one implementation.
- Redesign the remaining Expansion v3 queue around relative stability, low-volatility quality, and resolved-transition mechanisms.
- Require an inventory monitoring refresh before any future construction-layer work.

The current alpha inventory still appears structurally stronger in repair/stabilization regimes than in passive calm/non-hostile regimes. Expansion v3 should accept that as the working research prior, while preserving one narrow live path for calm-state relative stability.
