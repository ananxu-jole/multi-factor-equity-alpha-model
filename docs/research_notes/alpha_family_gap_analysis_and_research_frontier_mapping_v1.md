# Alpha Family Gap Analysis and Research Frontier Mapping v1

Date: 2026-06-17

## SECTION 1 – Current Alpha Family Inventory

### Family 1: Conditional Hostile/Stress Repair
- Family name: Conditional Hostile/Stress Repair.
- Economic intuition: securities that show improving participation, liquidity, or breadth inside hostile, weak-breadth, or stress regimes can offer conditional recovery alpha before full market stabilization.
- Representative candidates:
  - `participation_liquidity_state_shift_20_60`
  - `participation_breadth_repair_under_hostile_trend`
  - `volatility_compression_after_stress_stabilization`
- Evidence strength: moderate. The family is supported by multiple conditional candidates and explicit guardrails, but the strongest evidence is still watch-monitor level and state-dependent.
- Validation status: research-validated at the conditional level; only `participation_liquidity_state_shift_20_60` has reached conditional alpha review readiness with guardrails.
- Research maturity: medium-low. The family has been explored extensively, but it still requires consolidation and rebuild/equivalence testing.
- Library share estimate: ~60–70% of the current active candidate library, based on the dominance of hostile/stress state hypotheses and h20 focus.

### Family 2: Volatility Compression / Stabilization
- Family name: Volatility Compression / Stabilization.
- Economic intuition: securities that move from high stress or panic into volatility compression may have stopped falling and are better positioned for conditional outperformance.
- Representative candidate:
  - `volatility_compression_after_stress_stabilization`
- Evidence strength: low-moderate. The candidate has comparable h20 IC to the other family but weaker recent-window behavior and explicit watch-monitor caution.
- Validation status: research-only watch-monitor with guardrails.
- Research maturity: low. It is a plausible separate family, but the current evidence is insufficient to prove it is truly independent of the hostile/stress repair family.
- Library share estimate: ~20–25% of the current candidate focus, as it is the main non-participation-family concept still active.

### Family 3: Non-price Liquidity Repair
- Family name: Non-price Liquidity Repair.
- Economic intuition: improving liquidity metrics without price extension may signal a distinct repair path that is not simply price-based or participation-based.
- Representative candidates:
  - `nonprice_liquidity_repair_without_price_extension`
  - `nonprice_liquidity_persistence_20_60`
- Evidence strength: low. Existing metrics are weak and the family remains conditional-only or ingredient-status.
- Validation status: not validation-ready; only research evidence exists.
- Research maturity: low. The family is under-explored and not yet proven independent.
- Library share estimate: ~10–15% of current candidates, accounting for the two liquidity-focused signals.

### Family 4: Reference / Historical Reversal Diagnostics
- Family name: Reversal and Historical Diagnostic References.
- Economic intuition: earlier candidates and Track A references provide historical context for latent reversal exposure and help define failure modes.
- Representative candidates:
  - `volume_shock_reversal_stable_20`
  - earlier v2/v3 watchlist names and abandoned candidates
- Evidence strength: not intended for alpha; evidence is diagnostic.
- Validation status: not applicable for current alpha research.
- Research maturity: archival.
- Library share estimate: primarily contextual; not part of the active alpha candidate count.

## SECTION 2 – Alpha Family Concentration Analysis

### Concentration risk
- High. The surviving active library is concentrated in hostile/stress conditionals with h20 as the dominant horizon.
- The majority of current candidate effort is a single broad family (conditional repair) with a narrow secondary family (volatility compression).

### Redundancy risk
- High. `participation_breadth_repair_under_hostile_trend` appears strongly related to `participation_liquidity_state_shift_20_60`, and the non-price liquidity signals likely overlap with the broader liquidity/participation family.
- The current library has multiple expressions of conditional repair, which raises the risk of re-labeling the same edge rather than adding new families.

### Family-level diversification
- Low. Family diversification is weak because most candidates belong to the same economic intuition and share state-regime dependence.
- The only meaningful candidate-level variation is between participation repair and volatility compression, but the governing regime and horizon are similar.

### Horizon concentration
- Very high. All surviving candidates are centered on h20, with limited evidence of distinct h5 or h10 families in the current active library.
- This creates a horizon concentration risk that reduces the value of the current candidate diversification.

### Regime concentration
- High. All families are conditioned on hostile, stress, weak-breadth, or low-dispersion states. There is little representation of neutral, positive momentum, or outright recovery regimes.

### Distinct alpha families count
- Genuinely distinct families currently exist: likely 1–2.
- The primary family is the conditional hostile/stress repair family.
- A secondary candidate family in volatility compression/stabilization may exist, but it is not yet proven independent enough to count as a fully distinct alpha family.

## SECTION 3 – Missing Alpha Family Map

The current data assets are strong for OHLCV research, conditional state detection, and metadata-aware diagnostics once point-in-time data is available. Under-explored or unexplored families include:

### 1. Peer-relative / sector-relative behavior
- Status: under-explored.
- Rationale: current work is explicitly static-snapshot-only for metadata, and no active candidate is built around sector-relative behavior.
- Evidence: low; the framework has strong metadata planning but no candidate implementation.

### 2. Industry-relative behavior / peer-group normalization
- Status: under-explored.
- Rationale: peer groups are being assembled, but current alpha candidates avoid peer-relative conditioning.
- Evidence: low; this is a natural next frontier once point-in-time metadata is ready.

### 3. Dispersion behavior
- Status: under-explored.
- Rationale: the current candidate library focuses on stress repair and stabilization, not dispersion transition or compression as a primary family.
- Evidence: low-moderate; the current volatility candidate is related but not a pure dispersion family.

### 4. Persistence dynamics / rank stability
- Status: under-explored.
- Rationale: the work has touchpoints on rank persistence, but no dedicated family built around cross-sectional rank stability after drawdown.
- Evidence: moderate; there is room to build a more explicit persistence/stability family.

### 5. Transition-state dynamics beyond hostile/stress
- Status: under-explored.
- Rationale: the active library targets hostile-to-normal transitions, but not broader regime transitions such as calm-to-stress, trend reversal, or trend transition outside of stress.
- Evidence: moderate.

### 6. Crowd / inventory-cycle proxies
- Status: under-explored.
- Rationale: the project has a research inventory and governance layer but no explicit alpha family around inventory cycle or crowding proxies.
- Evidence: low.

### 7. Volatility structure behavior beyond compression
- Status: under-explored.
- Rationale: volatility compression is present, but other volatility structures like variance regime shifts, volatility momentum, or realized-versus-implied behavior are not represented.
- Evidence: low.

### 8. Cross-sectional leadership changes
- Status: under-explored.
- Rationale: the project has not yet implemented a family focused on leadership rotation or differential sector/industry leadership transitions.
- Evidence: low.

### 9. Relative participation shifts beyond local repair
- Status: under-explored.
- Rationale: current participation work is repair-focused; broader relative participation shift families (e.g. up/down-day participation asymmetry) are not covered.
- Evidence: moderate.

### 10. Normalization dynamics (stress-to-normal transitions)
- Status: partially explored.
- Rationale: the current library includes stress/stabilization, but the broader family of normalization dynamics (including broader trend/accounting normalization) is still only lightly represented.
- Evidence: moderate.

## SECTION 4 – Feasibility Assessment

### Peer-relative / sector-relative behavior
- Required data: point-in-time sector/industry/peer-group labels, historical metadata, universe mapping.
- Infrastructure compatibility: good, once metadata path is validated.
- Metadata compatibility: currently not feasible for validation-quality research; static snapshot only.
- Implementation complexity: medium-high due to point-in-time metadata requirements.
- Expected research value: high, because it addresses a major current gap.
- Priority: Medium Priority for now, High Priority once point-in-time metadata exists.

### Industry-relative behavior / peer-group normalization
- Required data: same as peer-relative; sector/industry/peer group labels and reliable historical classifications.
- Infrastructure compatibility: good if metadata sourcing is completed.
- Metadata compatibility: currently blocked for validation; feasible later.
- Implementation complexity: medium-high.
- Expected research value: high.
- Priority: Medium Priority now, High Priority after metadata readiness.

### Dispersion behavior
- Required data: cross-sectional returns, volatility/dispersion series, state definitions.
- Infrastructure compatibility: strong; existing OHLCV panels support this.
- Metadata compatibility: no special metadata required.
- Implementation complexity: medium.
- Expected research value: high. Dispersion is an orthogonal family to current stress repair.
- Priority: High Priority.

### Persistence dynamics / rank stability
- Required data: cross-sectional rank histories, turnover, stability metrics.
- Infrastructure compatibility: strong; existing signal panels likely support this.
- Metadata compatibility: not required.
- Implementation complexity: medium.
- Expected research value: high. This can diversify away from state repair to structural stability.
- Priority: High Priority.

### Transition-state dynamics beyond hostile/stress
- Required data: regime labels, trend-transition definitions, state slice history.
- Infrastructure compatibility: strong; existing conditional-state tools are adequate.
- Metadata compatibility: not required.
- Implementation complexity: medium.
- Expected research value: medium-high.
- Priority: High Priority.

### Crowd / inventory-cycle proxies
- Required data: research inventory state, candidate activation flags, crowding metrics.
- Infrastructure compatibility: moderate; may need new inventory analytics.
- Metadata compatibility: not required.
- Implementation complexity: medium.
- Expected research value: medium.
- Priority: Medium Priority.

### Volatility structure behavior beyond compression
- Required data: realized volatility, implied volatility if available, stress markers.
- Infrastructure compatibility: moderate; existing panels support realized volatility, implied vol may not be available.
- Metadata compatibility: not required.
- Implementation complexity: medium-high.
- Expected research value: medium-high.
- Priority: Medium Priority.

### Cross-sectional leadership changes
- Required data: cross-sectional rank leadership metrics, sector/industry groupings, price trend history.
- Infrastructure compatibility: strong, though may need additional feature engineering.
- Metadata compatibility: not required for initial tests.
- Implementation complexity: medium.
- Expected research value: medium.
- Priority: Medium Priority.

### Relative participation shifts beyond local repair
- Required data: participation on up/down days, breadth participation metrics, turnover.
- Infrastructure compatibility: strong.
- Metadata compatibility: none.
- Implementation complexity: medium.
- Expected research value: medium-high.
- Priority: High Priority.

### Normalization dynamics
- Required data: regime labels, trend and breadth measures, stress/normalization state definitions.
- Infrastructure compatibility: strong.
- Metadata compatibility: none.
- Implementation complexity: medium.
- Expected research value: medium.
- Priority: Medium Priority.

## SECTION 5 – Family Diversification Potential

### Most likely to add genuinely new information
- Dispersion behavior: high potential. It is economically distinct from the current stress/repair concepts, likely low correlation, and offers regime diversification.
- Persistence dynamics / rank stability: high potential. This would move beyond state repair to structural stability and low turnover, with a different regime signal.
- Transition-state dynamics beyond hostile/stress: high potential. It broadens beyond the current family of stress-repair transitions and can capture different regime boundaries.
- Relative participation shifts beyond local repair: medium-high potential. It uses participation features in a qualitatively different way and may reduce correlation with current candidates.

### Less likely to add new information
- Non-price liquidity repair (current family): likely extends existing liquidity/participation concepts rather than creating a distinct family.
- Volatility compression/stabilization: partially distinct, but still regime-adjacent to the existing family.
- Crowd / inventory-cycle proxies: interesting, but its value depends on new data and may be more governance/contextual than pure alpha.

## SECTION 6 – Research Frontier Ranking

1. Dispersion behavior
- Rationale: current library lacks a pure dispersion family, and dispersion is orthogonal to stress repair.
- Expected uniqueness: high.
- Implementation difficulty: medium.
- Expected diversification benefit: high.

2. Persistence dynamics / rank stability
- Rationale: the library is currently state repair–centric; rank stability would add structural, low-turnover alpha.
- Expected uniqueness: high.
- Implementation difficulty: medium.
- Expected diversification benefit: high.

3. Transition-state dynamics beyond hostile/stress
- Rationale: broadens the regime map and avoids over-concentration in only hostile/stress transitions.
- Expected uniqueness: medium-high.
- Implementation difficulty: medium.
- Expected diversification benefit: high.

4. Relative participation shifts beyond local repair
- Rationale: extends participation research to more general asymmetric participation behavior.
- Expected uniqueness: medium-high.
- Implementation difficulty: medium.
- Expected diversification benefit: medium-high.

5. Peer-relative / sector-relative behavior (post-metadata)
- Rationale: the largest structural gap in the current project, but it is currently blocked by metadata readiness.
- Expected uniqueness: high once feasible.
- Implementation difficulty: medium-high.
- Expected diversification benefit: high.

6. Industry-relative / peer-group normalization (post-metadata)
- Rationale: complements peer-relative behavior with sector/industry conditionality.
- Expected uniqueness: high.
- Implementation difficulty: medium-high.
- Expected diversification benefit: high.

7. Volatility structure behavior beyond compression
- Rationale: current volatility research is narrow; broader volatility structure can add a new dimension.
- Expected uniqueness: medium.
- Implementation difficulty: medium-high.
- Expected diversification benefit: medium.

8. Crowd / inventory-cycle proxies
- Rationale: could leverage the repository’s governance/inventory layer in a novel way.
- Expected uniqueness: medium.
- Implementation difficulty: medium.
- Expected diversification benefit: medium.

9. Cross-sectional leadership changes
- Rationale: a different mechanism class focused on leadership rotation rather than repair.
- Expected uniqueness: medium.
- Implementation difficulty: medium.
- Expected diversification benefit: medium.

10. Normalization dynamics
- Rationale: broader than stress compression and may capture different phase changes.
- Expected uniqueness: medium.
- Implementation difficulty: medium.
- Expected diversification benefit: medium.

## SECTION 7 – Recommended Next Discovery Program

### Program themes
1. Dispersion and cross-sectional structure
- Target family: Dispersion behavior.
- Expected contribution: new regime diversification and horizon diversification away from conditional repair.

2. Structural persistence and rank stability
- Target family: Persistence dynamics.
- Expected contribution: low-correlation, low-turnover candidates that do not rely primarily on stress-state repair.

3. Transition-state regime mapping
- Target family: Transition-state dynamics beyond hostile/stress.
- Expected contribution: broader regime coverage and reduced dependence on a single hostile/stress family.

4. Participation-asymmetry and relative participation shifts
- Target family: Relative participation shifts.
- Expected contribution: deeper use of participation features in a distinct family from repair-oriented participation alpha.

5. Metadata-enabled conditional behavior (phase 2)
- Target family: Peer-relative / sector-relative / industry-relative behavior.
- Expected contribution: high-value diversification once point-in-time metadata is validated.

### Program design notes
- Keep each theme at the family level; do not design specific signals yet.
- Use the next discovery program to fill gaps, not to expand the current conditional repair family.
- Prioritize themes that are compatible with current data and do not require metadata until the later phase.
- Reserve peer-relative and industry-relative research for a second phase after metadata readiness is confirmed.

## SECTION 8 – Final Conclusion

1. What is the project's biggest alpha-family gap?
- The biggest gap is a pure dispersion / cross-sectional dispersion behavior family.

2. Which missing family should be researched first?
- Dispersion behavior should be researched first, followed closely by persistence/rank stability.

3. Which current family is overrepresented?
- The conditional hostile/stress repair family is overrepresented.

4. Is metadata-enriched research justified?
- Not yet. The current candidate library is too concentrated and too structurally narrow to justify broad metadata-enriched research now. Metadata-enriched research should come after consolidation and after a clear proof of at least one structurally distinct family outside the current repair cluster.

5. What should be the next major research initiative after consolidation is complete?
- Launch a focused research program on dispersion and persistence families, with a secondary track for transition-state dynamics that broadens the regime map beyond hostile/stress repair.

---

### Audit caveat
This assessment is based on existing research notes and candidate summaries only. No discovery runs, code changes, threshold changes, governance changes, or ML modeling were performed.
