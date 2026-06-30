# Track B Expansion v5 Design Screening

Date: 2026-05-20

Status: DESIGN_ONLY_SCREENING

Scope constraints:
- No candidate implementation.
- No discovery runs.
- No validation or refinement.
- No production registration.
- No survivor/watchlist mutation.
- No portfolio construction, ML integration, blending, weighting, optimization, or gate/schema/threshold changes.

## Objective

Expansion v5 is a design-only roadmap for future repair/stabilization concepts that preserve Project Underdog's strongest empirical identity while reducing inventory concentration. The current inventory remains strongest in active repair/stabilization regimes, but Monitoring v2 shows persistent concentration risks that future expansion must address deliberately rather than adding another hostile h20 participation/breadth clone.

## Reviewed Context

Primary inputs reviewed:
- `conditional_alpha_inventory_monitoring_v2.md`
- `conditional_alpha_inventory_v2_governance_update.md`
- `inventory_ecosystem_review_v1.md`
- `track_b_expansion_v4_closeout_review.md`
- Current inventory and integration notes for the three active research candidates

Monitoring v2 inventory snapshot:

| Candidate | Monitoring Status | h20 IC | Recent Signal | Main Issue |
|---|---:|---:|---:|---|
| `participation_liquidity_state_shift_20_60` | WATCH_MONITOR | 0.028418 | recent h20 IC 0.009171 | recent rolling h20 IC much weaker than full-sample IC |
| `participation_breadth_repair_under_hostile_trend` | HEALTHY_ACTIVE_RESEARCH | 0.030720 | recent h20 IC 0.047573 | cleanest current profile |
| `volatility_compression_after_stress_stabilization` | WATCH_MONITOR | 0.028391 | recent positive rate 0.357895 | one-window dominance and weak recent positive-rate guardrail |

Inventory-level risks from Monitoring v2:
- Pairwise signal correlations remain low; max absolute correlation is 0.057859.
- Co-activation remains concentrated between the participation/liquidity and breadth-repair candidates; max co-activation is 0.803333.
- h20 concentration remains the main horizon risk.
- hostile/stress-state dependence remains the main state risk.
- Expansion v4 reinforced that active repair/stabilization is empirically stronger than post-repair calm persistence.

## Expansion v5 Design Posture

Expansion v5 should not fight the project's observed identity. The goal is not passive calmer-state diversification, post-repair continuation, or generic neutral accumulation. Those paths have repeatedly produced structural orthogonality without enough predictive value.

Instead, v5 should search for active repair/stabilization mechanisms with different activation semantics, horizons, co-activation patterns, and turnover profiles.

Design requirements:
- Prefer h5, h10, or h15 mechanisms when the economic thesis naturally supports them.
- Prefer repair states not defined by participation/breadth recovery.
- Prefer medium-coverage mechanisms over very sparse special cases.
- Prefer active stress containment, absorption, dislocation repair, or stabilization transitions over post-repair persistence.
- Avoid broad nonlinear state scores and over-fragmented state slicing.
- Explicitly screen for similarity to current inventory candidates, reversal, momentum, and simple low-volatility exposure before any future promotion.

## Concept Screen

Scores use a 1 to 5 scale, where 5 indicates stronger expected contribution to that diversification dimension.

| # | Concept | Family | Expected Horizon | Coverage | Turnover | Horizon Div. | State Div. | Co-activation Div. | Mechanism Div. | Construction Optionality | Complementarity | Priority | Recommendation |
|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `drawdown_pressure_stabilization_10` | drawdown repair / downside-pressure containment | h10 | medium | medium | 5 | 4 | 5 | 5 | 5 | 4.8 | HIGH | IMPLEMENT_NEXT |
| 2 | `short_horizon_volatility_shock_absorption_10` | short-horizon volatility shock absorption | h5-h10 | medium | medium-high | 5 | 3 | 4 | 4 | 5 | 4.5 | HIGH | IMPLEMENT_NEXT |
| 3 | `idiosyncratic_stress_containment_10` | stock-level stress containment | h5-h10 | medium-high | medium-high | 5 | 5 | 5 | 5 | 5 | 4.8 | HIGH | IMPLEMENT_NEXT |
| 4 | `dispersion_spike_stabilization_10` | cross-sectional dispersion repair | h10 | medium | medium | 5 | 4 | 5 | 5 | 4 | 4.6 | HIGH | HOLD_FOR_LATER |
| 5 | `turnover_shock_absorption_5_10` | turnover shock stabilization | h5-h10 | medium | high | 5 | 4 | 4 | 4 | 4 | 4.2 | MEDIUM | HOLD_FOR_LATER |
| 6 | `liquidity_impact_containment_10` | liquidity impact repair without breadth gate | h10 | medium | medium | 5 | 3 | 3 | 4 | 4 | 3.8 | MEDIUM | HOLD_FOR_LATER |
| 7 | `range_expansion_failure_stabilization_5_10` | failed range-expansion stabilization | h5-h10 | medium | high | 5 | 4 | 4 | 4 | 4 | 4.1 | MEDIUM | HOLD_FOR_LATER |
| 8 | `residual_volatility_normalization_during_stress_10` | residual volatility normalization | h10 | medium | medium | 5 | 3 | 4 | 3 | 4 | 3.8 | MEDIUM | HOLD_FOR_LATER |
| 9 | `factor_crowding_unwind_stabilization_10` | crowding unwind stabilization | h10-h15 | low-medium | medium | 4 | 5 | 5 | 5 | 4 | 4.3 | MEDIUM | HOLD_FOR_LATER |
| 10 | `low_dispersion_stress_repair_quality_10` | low-dispersion repair under stress | h10 | medium | low-medium | 5 | 3 | 4 | 3 | 4 | 3.7 | MEDIUM | HOLD_FOR_LATER |
| 11 | `intraday_reversal_pressure_absorption_5` | intraday pressure absorption | h5 | medium-high | high | 5 | 4 | 5 | 4 | 4 | 4.2 | MEDIUM | HOLD_FOR_LATER |
| 12 | `credit_like_equity_stress_resilience_10` | balance-sheet-style stress resilience proxy | h10-h15 | low-medium | low | 4 | 5 | 5 | 5 | 4 | 4.4 | LOW | HOLD_FOR_LATER |

## Candidate Concepts

### 1. `drawdown_pressure_stabilization_10`

Mechanism family: drawdown repair / downside-pressure containment.

Inventory gap addressed: non-h20 repair, lower co-activation, non-participation/breadth repair, different state semantics.

Economic intuition: During active market stress, some stocks stop transmitting downside pressure before broad breadth repair is complete. The edge thesis is that names with contained downside pressure after a drawdown shock may recover or stabilize over a shorter medium horizon.

Repair/stabilization thesis: Identify active drawdown-pressure environments and select stocks where recent downside expansion has slowed, residual loss pressure has stabilized, and the signal is not simply buying the worst reversal names.

Expected activation semantics: active drawdown or downside-pressure state; not post-repair and not calm accumulation.

Expected horizon: h10 primary, h5 secondary, h20 only as a diagnostic.

Expected active coverage: medium.

Expected turnover profile: medium.

Why it differs from current inventory: It is not breadth-repair gated, not participation/liquidity repair, and not volatility compression after stress stabilization. It focuses on downside-pressure containment.

Why it differs from reversal/momentum: It should require stabilization quality after pressure, not raw prior loser rank or positive continuation rank.

How it reduces concentration: It targets h10 and a drawdown-pressure repair state with expected low co-activation against the participation/breadth pair.

Likely failure mode: The signal may collapse into short-term reversal or remain strongest only at h20.

Implementation complexity: medium.

Inventory-complementarity score: 4.8.

Priority: HIGH.

Recommendation: IMPLEMENT_NEXT.

### 2. `short_horizon_volatility_shock_absorption_10`

Mechanism family: short-horizon volatility shock absorption.

Inventory gap addressed: shorter-horizon stabilization, non-h20 repair, different turnover profile.

Economic intuition: After sudden volatility expansion, assets that absorb the shock without continued path disorder may exhibit short-horizon stabilization before slower h20 repair signals fully mature.

Repair/stabilization thesis: Detect active volatility shock states and select names with contained follow-through, improving range quality, and lower residual disorder after the shock.

Expected activation semantics: active or very recent volatility shock; not fully resolved calm state.

Expected horizon: h5-h10.

Expected active coverage: medium.

Expected turnover profile: medium-high.

Why it differs from current inventory: It is shorter-horizon and shock-absorption oriented, while `volatility_compression_after_stress_stabilization` is h20-centered and more tied to post-stress compression.

Why it differs from reversal/momentum: It should measure containment after a shock, not raw negative or positive price rank.

How it reduces concentration: It provides a volatility-family concept with shorter horizon and expected lower co-activation with participation/breadth repair.

Likely failure mode: It may duplicate the existing volatility compression candidate or become too noisy at h5.

Implementation complexity: medium.

Inventory-complementarity score: 4.5.

Priority: HIGH.

Recommendation: IMPLEMENT_NEXT.

### 3. `idiosyncratic_stress_containment_10`

Mechanism family: stock-level stress containment.

Inventory gap addressed: lower co-activation repair, different state semantics, medium coverage, non-breadth repair.

Economic intuition: Some opportunities may arise from asset-level stress stabilization even when the broad market state is not the primary driver. This could preserve repair identity while weakening dependence on hostile market-state gates.

Repair/stabilization thesis: Detect stock-level stress events relative to the cross-section and select names where stress is being contained without requiring broad participation repair.

Expected activation semantics: idiosyncratic stress containment; market may be neutral, mixed, or hostile, but activation is stock-centric.

Expected horizon: h5-h10.

Expected active coverage: medium-high.

Expected turnover profile: medium-high.

Why it differs from current inventory: Current candidates are inventory-level or regime-linked. This concept is more asset-level and should not require breadth or participation repair activation.

Why it differs from reversal/momentum: It should rank containment quality conditional on stress, not the magnitude of prior return alone.

How it reduces concentration: It lowers co-activation risk by moving activation from shared hostile/breadth states to stock-level dislocation states.

Likely failure mode: It may become noisy or too close to short-term reversal if containment is under-specified.

Implementation complexity: medium.

Inventory-complementarity score: 4.8.

Priority: HIGH.

Recommendation: IMPLEMENT_NEXT.

### 4. `dispersion_spike_stabilization_10`

Mechanism family: cross-sectional dispersion repair.

Inventory gap addressed: non-participation/breadth repair, lower co-activation, h10 horizon.

Economic intuition: High dispersion regimes can create repair opportunities independent of breadth recovery. Stocks that remain orderly during dispersion shocks may be better positioned as dislocation normalizes.

Repair/stabilization thesis: Activate when cross-sectional dispersion spikes and identify names with improving residual stability or reduced relative disorder.

Expected activation semantics: active dispersion shock, not broad hostile trend alone.

Expected horizon: h10.

Expected active coverage: medium.

Expected turnover profile: medium.

Why it differs from current inventory: It is dispersion-led rather than participation-, breadth-, liquidity-, or volatility-compression-led.

Why it differs from reversal/momentum: It should not reward raw losers or winners; it evaluates relative orderliness during dispersion stress.

How it reduces concentration: It introduces a different stress dimension and should reduce co-activation with participation/breadth repair if the state gate is dispersion-based.

Likely failure mode: Prior rejected dispersion-recovery formulations suggest this must avoid a simple recovery clone.

Implementation complexity: medium.

Inventory-complementarity score: 4.6.

Priority: HIGH.

Recommendation: HOLD_FOR_LATER.

### 5. `turnover_shock_absorption_5_10`

Mechanism family: turnover shock stabilization.

Inventory gap addressed: different turnover profile, shorter horizon, lower h20 dependence.

Economic intuition: Abnormally high turnover can signal forced activity or stress. Stocks absorbing turnover shocks without disorderly price impact may stabilize quickly.

Repair/stabilization thesis: Activate on abnormal turnover shock and select names where price impact, range expansion, and residual instability are contained.

Expected activation semantics: active turnover shock; not breadth/participation repair.

Expected horizon: h5-h10.

Expected active coverage: medium.

Expected turnover profile: high.

Why it differs from current inventory: It uses turnover shock absorption rather than participation trend or broad breadth repair.

Why it differs from reversal/momentum: It requires abnormal activity and containment quality rather than price-rank direction.

How it reduces concentration: It can provide a faster repair dimension and a materially different turnover profile.

Likely failure mode: High turnover may introduce noise and unstable implementation behavior.

Implementation complexity: medium.

Inventory-complementarity score: 4.2.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 6. `liquidity_impact_containment_10`

Mechanism family: liquidity impact repair without breadth gate.

Inventory gap addressed: liquidity repair variant that avoids participation/breadth co-activation.

Economic intuition: Liquidity stress can be informative when abnormal trading pressure stops moving prices as much. The desired mechanism is impact containment, not participation repair.

Repair/stabilization thesis: Activate on liquidity-impact dislocation and select names where impact normalizes while trading remains sufficient.

Expected activation semantics: liquidity impact stress with containment; avoid requiring hostile breadth repair.

Expected horizon: h10.

Expected active coverage: medium.

Expected turnover profile: medium.

Why it differs from current inventory: It is liquidity-impact based rather than participation-liquidity state shift or breadth repair.

Why it differs from reversal/momentum: It should rank impact containment conditional on liquidity dislocation rather than raw price direction.

How it reduces concentration: It may diversify within the liquidity family if it avoids the current participation/breadth activation cluster.

Likely failure mode: It could co-activate too strongly with `participation_liquidity_state_shift_20_60`.

Implementation complexity: medium.

Inventory-complementarity score: 3.8.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 7. `range_expansion_failure_stabilization_5_10`

Mechanism family: failed range-expansion stabilization.

Inventory gap addressed: shorter-horizon stabilization, non-breadth repair, different turnover profile.

Economic intuition: When range expansion fails to produce sustained directional breakdown, the market may be pricing temporary disorder rather than durable deterioration.

Repair/stabilization thesis: Activate after large range expansion and select names with failed follow-through, improving close-location quality, and contained residual pressure.

Expected activation semantics: active range shock with failed continuation.

Expected horizon: h5-h10.

Expected active coverage: medium.

Expected turnover profile: high.

Why it differs from current inventory: It is range-behavior based rather than participation, breadth, or volatility-compression based.

Why it differs from reversal/momentum: It should require failed disorder continuation, not simple prior loss or bounce.

How it reduces concentration: It introduces a path-quality repair mechanism that may be shorter horizon and less co-active with h20 candidates.

Likely failure mode: It may become a disguised reversal signal if path-quality controls are weak.

Implementation complexity: medium.

Inventory-complementarity score: 4.1.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 8. `residual_volatility_normalization_during_stress_10`

Mechanism family: residual volatility normalization.

Inventory gap addressed: shorter-horizon volatility repair, lower h20 dependence.

Economic intuition: Volatility normalization may matter most while stress is still active, not after the full compression window is complete.

Repair/stabilization thesis: During active stress, select names whose residual volatility normalizes faster than peers without becoming simple low-volatility exposures.

Expected activation semantics: active stress with residual volatility normalization.

Expected horizon: h10.

Expected active coverage: medium.

Expected turnover profile: medium.

Why it differs from current inventory: It tests active residual normalization rather than post-stress volatility compression.

Why it differs from reversal/momentum: It is not price-rank directional and should include explicit checks against low-volatility similarity.

How it reduces concentration: It may diversify horizon but could remain state-adjacent to the existing volatility candidate.

Likely failure mode: It may duplicate `volatility_compression_after_stress_stabilization` or load on simple low-volatility beta.

Implementation complexity: medium.

Inventory-complementarity score: 3.8.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 9. `factor_crowding_unwind_stabilization_10`

Mechanism family: crowding unwind stabilization.

Inventory gap addressed: different state semantics, lower co-activation, mechanism diversification.

Economic intuition: Some repair opportunities may come from crowded positioning unwinds rather than breadth or participation stress. Stabilization after crowding pressure can be orthogonal to the current inventory.

Repair/stabilization thesis: Use observable cross-sectional proxies for crowding unwind pressure, such as rapid rank churn or factor-like dispersion stress, and select names stabilizing after unwind pressure.

Expected activation semantics: active crowding/unwind stress.

Expected horizon: h10-h15.

Expected active coverage: low-medium.

Expected turnover profile: medium.

Why it differs from current inventory: It is crowding/unwind led rather than participation-, breadth-, liquidity-, or volatility-led.

Why it differs from reversal/momentum: It should measure stabilization after a cross-sectional unwind process, not raw prior return direction.

How it reduces concentration: It could materially diversify state semantics and co-activation if proxies are stable.

Likely failure mode: Proxy quality may be weak or too complex for a first-pass isolated runner.

Implementation complexity: high.

Inventory-complementarity score: 4.3.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 10. `low_dispersion_stress_repair_quality_10`

Mechanism family: low-dispersion repair under stress.

Inventory gap addressed: h10 repair and state diversification within active stress.

Economic intuition: Under stress, low dispersion may indicate indiscriminate pressure or a synchronized market state. Names with better repair quality inside that state may show differentiated stabilization.

Repair/stabilization thesis: Activate under stressed low-dispersion environments and select stocks with cleaner repair quality without using breadth recovery as the primary gate.

Expected activation semantics: active stress with unusually compressed cross-sectional dispersion.

Expected horizon: h10.

Expected active coverage: medium.

Expected turnover profile: low-medium.

Why it differs from current inventory: It is dispersion-state based and not directly participation/breadth repair.

Why it differs from reversal/momentum: It should score repair quality inside a state, not prior price rank.

How it reduces concentration: It may add a stress-state subtype with lower co-activation if not tied to the breadth/participation cluster.

Likely failure mode: It may be too close to volatility/stress stabilization or have weak standalone edge.

Implementation complexity: medium.

Inventory-complementarity score: 3.7.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 11. `intraday_reversal_pressure_absorption_5`

Mechanism family: intraday pressure absorption.

Inventory gap addressed: h5 horizon, different turnover, non-h20 stabilization.

Economic intuition: Repair may begin inside the daily bar when sell pressure is absorbed before close. This is not intended as simple reversal, but as pressure absorption under active stress.

Repair/stabilization thesis: During active pressure states, select names that absorb intraday stress with improved close-location or reduced adverse follow-through.

Expected activation semantics: active short-horizon pressure absorption.

Expected horizon: h5.

Expected active coverage: medium-high.

Expected turnover profile: high.

Why it differs from current inventory: It is faster, more path-quality based, and not participation/breadth h20 repair.

Why it differs from reversal/momentum: It should require intraday pressure absorption and state activation, not buy prior losers or chase winners.

How it reduces concentration: It offers the strongest horizon diversification if stable.

Likely failure mode: It may be noisy, data-quality sensitive, or secretly short-term reversal.

Implementation complexity: medium-high.

Inventory-complementarity score: 4.2.

Priority: MEDIUM.

Recommendation: HOLD_FOR_LATER.

### 12. `credit_like_equity_stress_resilience_10`

Mechanism family: balance-sheet-style stress resilience proxy.

Inventory gap addressed: different state semantics, lower co-activation, construction optionality.

Economic intuition: Some stocks may stabilize better during stress because their equity behavior resembles higher-quality resilience. This can be tested with market-observable proxies rather than external fundamental data.

Repair/stabilization thesis: In active stress, select names with lower residual fragility, contained downside tails, and stable liquidity behavior that does not simply equal low volatility.

Expected activation semantics: active stress resilience, stock-level quality under pressure.

Expected horizon: h10-h15.

Expected active coverage: low-medium.

Expected turnover profile: low.

Why it differs from current inventory: It focuses on resilience quality during stress rather than breadth, participation, liquidity repair, or volatility compression.

Why it differs from reversal/momentum: It should be quality-under-stress rather than directional price rank.

How it reduces concentration: It may create a lower-turnover repair sleeve useful for future construction optionality.

Likely failure mode: It may load on simple low-volatility beta or be underpowered without fundamentals.

Implementation complexity: high.

Inventory-complementarity score: 4.4.

Priority: LOW.

Recommendation: HOLD_FOR_LATER.

## Top One-By-One Test Sequence

Recommended top 2-3 concepts for later isolated testing:

1. `drawdown_pressure_stabilization_10`
   - Best first choice because it directly targets non-h20 repair, lower co-activation, and non-participation/breadth active repair.
   - Highest value question: can downside-pressure containment create h10 repair behavior without collapsing into reversal?

2. `idiosyncratic_stress_containment_10`
   - Best diversification choice because it moves activation from shared market-state repair into stock-level stress containment.
   - Highest value question: can active repair be detected at the asset level with medium coverage and low inventory overlap?

3. `short_horizon_volatility_shock_absorption_10`
   - Best short-horizon stabilization choice, but should be tested with explicit similarity controls against `volatility_compression_after_stress_stabilization`.
   - Highest value question: can the volatility family contribute h5-h10 behavior rather than another h20-dominant candidate?

Implementation should remain one-by-one. A batch would make it harder to isolate whether any improvement comes from true ecosystem diversification or from another variant of the existing active-repair cluster.

## Concepts That Directly Address Current Risks

Direct h20 concentration reducers:
- `drawdown_pressure_stabilization_10`
- `short_horizon_volatility_shock_absorption_10`
- `idiosyncratic_stress_containment_10`
- `turnover_shock_absorption_5_10`
- `range_expansion_failure_stabilization_5_10`
- `intraday_reversal_pressure_absorption_5`

Direct participation/breadth co-activation reducers:
- `drawdown_pressure_stabilization_10`
- `idiosyncratic_stress_containment_10`
- `dispersion_spike_stabilization_10`
- `factor_crowding_unwind_stabilization_10`
- `credit_like_equity_stress_resilience_10`

Direct hostile/stress concentration reducers without abandoning repair identity:
- `idiosyncratic_stress_containment_10`
- `factor_crowding_unwind_stabilization_10`
- `liquidity_impact_containment_10`

Different turnover profile candidates:
- High turnover: `turnover_shock_absorption_5_10`, `range_expansion_failure_stabilization_5_10`, `intraday_reversal_pressure_absorption_5`
- Lower turnover: `credit_like_equity_stress_resilience_10`, `low_dispersion_stress_repair_quality_10`

## What Should Not Be Repeated

Do not repeat:
- Passive neutral accumulation.
- Quiet non-hostile liquidity accumulation without active repair semantics.
- Post-repair continuation after breadth recovery.
- Fully resolved-state stability as a standalone thesis.
- Broad hostile-to-neutral transition gates without sharper state definitions.
- More h20-only participation/breadth repair variants.
- Raw continuation, simple reversal, price-rank momentum, or broad nonlinear state scores.

## Governance Conditions Before Implementation

Before implementing any Expansion v5 concept:
- Inventory Monitoring v2 risks should be explicitly accepted in the implementation note.
- WATCH_MONITOR candidates should remain under observation, especially recent h20 weakness and one-window dominance.
- The new runner should be isolated under a concept-specific artifact directory.
- Similarity checks should include current inventory candidates, reversal, momentum, low-volatility where relevant, and the closest mechanism family baseline.
- Diagnostics should explicitly separate h5/h10/h15/h20 behavior.
- The note should classify whether the result reduces horizon, state, or co-activation concentration.

## Final Recommendation

Expansion v5 is justified as design work and can support future one-by-one implementation, but only if it stays tightly focused on active repair/stabilization mechanisms with clear diversification intent.

Recommended first implementation later: `drawdown_pressure_stabilization_10`.

Recommended second implementation later: `idiosyncratic_stress_containment_10`.

Recommended third implementation later: `short_horizon_volatility_shock_absorption_10`, with strict overlap checks against the existing volatility/stress candidate.

The strategic frontier should be active repair with new state semantics, shorter natural horizons, and lower participation/breadth co-activation. Expansion should not return immediately to passive calmer-state or post-repair persistence concepts unless the state definitions are materially redesigned.
