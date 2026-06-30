# Candidate Overlap and Redundancy Audit v1

Date: 2026-06-17

## SECTION 1 – Candidate Universe

This audit covers the surviving Project Underdog candidates from the current Track B conditional-alpha inventory, the v5 focused discovery, and the active watch-monitor pool. It is research-only and uses only documented summary metrics from the current notes.

### Candidate inventory

| Candidate | Status | Primary horizon | Mean IC | IC IR | Turnover proxy | Active coverage | Originating research family |
|---|---|---|---|---|---|---|---|
| `participation_liquidity_state_shift_20_60` | WATCH_MONITOR, `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | h20 | 0.0284 | not explicitly reported in current summary | 0.0964 | 34.7% | Track B v4 conditional diagnostics / conditional alpha closeout |
| `participation_breadth_repair_under_hostile_trend` | HEALTHY_ACTIVE_RESEARCH, `CONDITIONAL_REFINEMENT_CANDIDATE` | h20 | 0.0307 | not explicitly reported in current summary | 0.0136 | 14.3% | Track B v5 focused discovery |
| `volatility_compression_after_stress_stabilization` | WATCH_MONITOR, `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` | h20 | 0.0284 | not explicitly reported in current summary | 0.0221 | 18.9% | Track B v4 inventory research / conditional inventory monitoring |
| `nonprice_liquidity_repair_without_price_extension` | `CONDITIONAL_ONLY_RESEARCH` | h20 | -0.0016 | not explicitly reported in current summary | 0.0515 | 38.8% | Track B v5 focused discovery |
| `nonprice_liquidity_persistence_20_60` | `CONDITIONAL_ONLY_KEEP` | not explicitly reported | weaker standalone evidence | not reported | not reported | not reported | earlier Track B / v4 non-price liquidity research |

> Note: IC IR is not available for all candidates in the referenced summary documents. The audit uses the available metrics and a qualitative assessment where numeric values are absent.

## SECTION 2 – Hypothesis Mapping

### `participation_liquidity_state_shift_20_60`
- Underlying economic intuition: improving participation and liquidity during hostile trend or weak breadth states signals a conditional repair edge.
- Expected behavioral mechanism: state-shift activation where liquidity/participation repair occurs before price leadership or broad market stabilization.
- Closest neighboring candidates: `participation_breadth_repair_under_hostile_trend`, `nonprice_liquidity_repair_without_price_extension`.
- Similarity classification: statistical and structural overlap with `participation_breadth_repair_under_hostile_trend`; conceptual distinctness is moderate but likely not strong.

### `participation_breadth_repair_under_hostile_trend`
- Underlying economic intuition: in hostile trend states, breadth repair precedes durable reversal; the signal captures improving participation without chasing mature momentum.
- Expected behavioral mechanism: participation breadth improves while the market remains hostile, suggesting a nascent recovery rather than momentum continuation.
- Closest neighboring candidates: `participation_liquidity_state_shift_20_60`, `volatility_compression_after_stress_stabilization`.
- Similarity classification: primarily statistical overlap with `participation_liquidity_state_shift_20_60` and structural similarity through state-conditioned repair; likely related if not redundant.

### `volatility_compression_after_stress_stabilization`
- Underlying economic intuition: volatility compression after stress indicates a stabilization transition that can support a conditional return edge.
- Expected behavioral mechanism: securities that stabilize from panic/liquidity stress into lower-volatility states recover more coherently than those that remain volatile.
- Closest neighboring candidates: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`.
- Similarity classification: conceptual similarity through stress-state dependence, but structural difference in emphasis on volatility and stabilization rather than participation/breadth; related.

### `nonprice_liquidity_repair_without_price_extension`
- Underlying economic intuition: non-price liquidity improvement can precede relative performance gains if it is not driven by recent price extension.
- Expected behavioral mechanism: a liquidity repair transition under low or moderate price extension, isolating liquidity flow from price momentum.
- Closest neighboring candidates: `participation_liquidity_state_shift_20_60`, `nonprice_liquidity_persistence_20_60`.
- Similarity classification: conceptual and structural overlap with other liquidity repair ideas; statistical overlap is unknown but likely moderate.

### `nonprice_liquidity_persistence_20_60`
- Underlying economic intuition: persistent non-price liquidity strength may be a distinct conditional ingredient separate from price rank.
- Expected behavioral mechanism: a durable liquidity persistence signal rather than an always-on price or participation bias.
- Closest neighboring candidates: `nonprice_liquidity_repair_without_price_extension`, `participation_liquidity_state_shift_20_60`.
- Similarity classification: conceptual similarity in liquidity focus; structural similarity is moderate but evidence is weak, making redundancy more likely.

## SECTION 3 – Redundancy Audit

### Pairwise assessment

#### `participation_liquidity_state_shift_20_60` vs `participation_breadth_repair_under_hostile_trend`
- Classification: Strongly Related.
- Reasoning: Both are state-activated repair signals in hostile/weak breadth regimes. The documented co-activation matrix shows a high pairwise co-activation (`0.803333`) and the same dominant state family. Their hypotheses differ only in emphasis on liquidity versus breadth, making them likely partial variants of the same alpha family.

#### `participation_liquidity_state_shift_20_60` vs `volatility_compression_after_stress_stabilization`
- Classification: Related.
- Reasoning: Both depend on stress-state behavior and conditional recovery, but one emphasizes participation/liquidity repair and the other emphasizes volatility stabilization. Correlation is low (`~0.0073`) and co-activation is moderate (`0.346734`), suggesting shared regime exposure with distinct mechanics.

#### `participation_breadth_repair_under_hostile_trend` vs `volatility_compression_after_stress_stabilization`
- Classification: Related.
- Reasoning: They share hostile/stress activation contexts, but the breadth repair hypothesis is distinct from volatility compression. Correlation is low (`~0.0172`) and co-activation is moderate (`0.25`), supporting related but not duplicate status.

#### `participation_liquidity_state_shift_20_60` vs `nonprice_liquidity_repair_without_price_extension`
- Classification: Related.
- Reasoning: Both focus on liquidity and participation improvement, but the latter explicitly excludes price extension. This may be a narrower liquidity variant; current evidence is weak, so the pair is related with potential redundancy if the non-price thesis does not hold.

#### `participation_breadth_repair_under_hostile_trend` vs `nonprice_liquidity_repair_without_price_extension`
- Classification: Related.
- Reasoning: Breadth repair is adjacent to liquidity repair against a hostile market; the main difference is whether the signal is grounded in breadth or pure non-price liquidity. Current metrics do not prove independence.

#### `nonprice_liquidity_repair_without_price_extension` vs `nonprice_liquidity_persistence_20_60`
- Classification: Potential Duplicate.
- Reasoning: Both are liquidity-focused, non-price hypotheses. With weak evidence for the latter and only conditional research status for the former, they are likely overlapping and should be treated as largely redundant until one receives stronger independent support.

## SECTION 4 – Coverage Comparison

### Active coverage
- `participation_liquidity_state_shift_20_60`: 34.7% active coverage.
- `participation_breadth_repair_under_hostile_trend`: 14.3% active coverage.
- `volatility_compression_after_stress_stabilization`: 18.9% active coverage.
- `nonprice_liquidity_repair_without_price_extension`: 38.8% active coverage.

### Universe participation
- `participation_liquidity_state_shift_20_60` and `nonprice_liquidity_repair_without_price_extension` have the highest raw participation, indicating broader signal availability.
- `participation_breadth_repair_under_hostile_trend` has the lowest participation, making it more state-specific and narrower.
- `volatility_compression_after_stress_stabilization` is intermediate.

### Regime applicability
- All examined surviving candidates are primarily active in hostile/stress or weak-breadth regimes.
- `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend` both show strong low-dispersion and weak-breadth state activation.
- `volatility_compression_after_stress_stabilization` is strongest in panic/liquidity stress and drawdown acceleration states.
- `nonprice_liquidity_repair_without_price_extension` is documented as a low-extension liquidity repair idea, but its specific regime slices are not fully detailed in the current summary.

### Expected deployment conditions
- `participation_liquidity_state_shift_20_60`: hostile trend + weak breadth / stress confirmation states.
- `participation_breadth_repair_under_hostile_trend`: hostile trend + breadth repair with participation stabilization.
- `volatility_compression_after_stress_stabilization`: volatility stress easing and market stabilization.
- `nonprice_liquidity_repair_without_price_extension`: liquidity repair under low price-extension conditions.

### Similar environment activation
- `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend` activate in highly similar environments and should be audited for overlapping regime triggers.
- `volatility_compression_after_stress_stabilization` overlaps the stress region but may offer a partially orthogonal volatility-based activation.
- `nonprice_liquidity_repair_without_price_extension` overlaps the liquidity environment and likely shares regime exposure with the participation/liquidity cluster.

## SECTION 5 – Horizon Analysis

### Horizon overlap
- All surviving candidates are centered on h20.
- `participation_breadth_repair_under_hostile_trend` and `participation_liquidity_state_shift_20_60` are both strongest at h20, with only the latter showing watch-monitor exposure.
- `volatility_compression_after_stress_stabilization` is also h20-focused, making the current surviving library heavily concentrated on the same horizon.
- `nonprice_liquidity_repair_without_price_extension` is also referenced as h20 in the current notes, though its best-horizon evidence is weak.

### h5 / h10 / h20 evidence
- `participation_breadth_repair_under_hostile_trend` has positive signals across h5/h10/h20 in the v5 focused discovery, but h20 is its best documented horizon.
- `volatility_compression_after_stress_stabilization` is only documented at h20 in the current audit summary.
- `participation_liquidity_state_shift_20_60` is explicitly a conditional h20 candidate.
- The current library is therefore not diversified across horizons; it is effectively a set of h20 conditional candidates with adjacent stress/hypothesis variation.

### Horizon effect conclusion
- Multiple candidates are capturing the same horizon effect: h20 is the dominant and likely shared horizon among the surviving candidates.
- This increases the risk that the library is capturing variant expressions of the same h20 state-dependent edge rather than separate horizons.

## SECTION 6 – Consolidation Recommendations

### Candidate-level recommendations
- `participation_liquidity_state_shift_20_60`: Keep but monitor overlap. It remains the strongest current Track B anchor, but it must undergo rebuild/equivalence and overlap testing with `participation_breadth_repair_under_hostile_trend`.
- `participation_breadth_repair_under_hostile_trend`: Keep but monitor overlap. It is the cleanest active candidate and a useful follow-up, but its high co-activation suggests it may be a strong related variant rather than an independent family.
- `volatility_compression_after_stress_stabilization`: Keep but monitor overlap. It appears to offer a partially distinct stress/volatility mechanism, but it remains within the same hostile/stress regime family and should be validated for orthogonality.
- `nonprice_liquidity_repair_without_price_extension`: Requires additional evidence. It is a useful liquidity hypothesis, but the current h20 evidence is too weak to support a strong candidate status; it should remain conditional-only until its state semantics are clarified.
- `nonprice_liquidity_persistence_20_60`: Requires additional evidence or archive as redundant. With only conditional-ingredient status and limited metrics, it is likely redundant with the broader liquidity/participation family unless a sharper independence case is established.

### Consolidation tag assignment
- Independent: none of the surviving candidates can be declared fully independent based on the current audit. All are related through hostile/stress state dependence and h20 focus.
- Keep but monitor overlap: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`, `volatility_compression_after_stress_stabilization`.
- Requires additional evidence: `nonprice_liquidity_repair_without_price_extension`, `nonprice_liquidity_persistence_20_60`.
- Archive as redundant: not recommended automatically; only after overlap and evidence tests.

## SECTION 7 – Portfolio-Level Implications

### Diversity of surviving alpha sources
- Low. The surviving candidates are concentrated in a single broad conditional family: hostile/stress state repair around h20.
- The apparent diversity is primarily in hypothesis wording (participation vs breadth vs volatility), not in horizon or regime segmentation.

### Concentration risk
- High. All surviving candidates share h20 as the primary horizon and a similar stress activation set, increasing the chance of a common drawdown or regime failure.
- The high co-activation between the two participation-style candidates raises the risk that the library is effectively a single alpha source expressed in two variants.

### Research concentration risk
- High. Current research is focused on participation/liquidity/breadth repair and volatility/stress stabilization, with little diversification into horizon, sector, or peer-relative hypothesis space.
- The current inventory does not yet provide a robust basis for metadata-enriched research because the candidate family itself is narrow.

### Potential benefits of future ensemble construction
- Only moderate. A future ensemble would benefit if `volatility_compression_after_stress_stabilization` proves sufficiently distinct and if `nonprice_liquidity_repair_without_price_extension` can be strengthened into a non-overlapping liquidity family.
- Today’s library is better treated as a research pool for consolidation than as a production ensemble candidate set.

## SECTION 8 – Final Conclusion

1. How many genuinely distinct alpha families currently exist?
- One primary family: conditional hostile/stress repair anchored on h20.
- A second potential family exists in volatility compression/stabilization, but it is not yet proven independent and should be treated as related.

2. Which candidate is strongest within each family?
- Primary family: `participation_liquidity_state_shift_20_60` is the strongest documented anchor, with formal conditional alpha review readiness.
- Secondary potential family: `volatility_compression_after_stress_stabilization` is the best candidate for a distinct volatility/stress stabilization hypothesis.

3. Which candidates appear most redundant?
- `participation_breadth_repair_under_hostile_trend` appears most redundant relative to `participation_liquidity_state_shift_20_60` due to high co-activation and similar state dependence.
- `nonprice_liquidity_persistence_20_60` appears most redundant with the broader liquidity repair cluster because it lacks independent strength.

4. Is the library sufficiently diversified to justify metadata-enriched research?
- No. The library is too concentrated in a single conditional/h20 family to justify a broader metadata-enriched research push. Metadata-enriched research should wait until the surviving pool is consolidated and at least one candidate family proves structurally distinct from the participation/breadth/stress cluster.

5. What should be the next consolidation test after this audit?
- The next test should be the participation/breadth overlap and correlation audit between `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend`, including state activation similarity and regime trigger overlap. This will determine whether the library contains two distinct hypotheses or a single family with variant labels.

---

### Audit caveat
This is a documented research assessment based solely on existing summaries. No new discovery runs, threshold changes, governance actions, production modifications, or ML modeling were performed.
