# Project Underdog - Event Clustering Research Review v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 9 - Research Review

Classification: `RESEARCH_REVIEW_RECOMMEND_PARK`

Research recommendation: `PARK_MODULE`

Scope: independent scientific review of the completed Event Clustering IC Discovery.

This is a review-only lifecycle note. It does not recompute IC, regenerate panels, modify formulas, implement code, propose candidates, perform refinement, run validation, mutate governance, modify production systems, change thresholds, or introduce ML.

## SECTION 1 - Inputs Reviewed

Reviewed documents and artifacts:

- `docs/research_notes/event_clustering_ic_discovery_v1.md`
- `docs/research_notes/event_clustering_scientific_review_v1.md`
- `docs/research_notes/event_clustering_research_module_design_v1.md`
- `docs/research_notes/event_clustering_formula_and_panel_specification_v1.md`
- `artifacts/research/event_clustering_research_module_v1/ic_discovery_v1/`

Reviewed saved IC Discovery artifacts:

- `daily_ic.csv`
- `candidate_ic_summary.csv`
- `candidate_horizon_summary.csv`
- `candidate_rankings.csv`
- `rolling_stability_summary.csv`
- `ic_discovery_manifest.json`

Candidate scope:

- `ecluster_01_concentrated_absorption`
- `ecluster_02_aligned_pressure_resolution`
- `ecluster_03_fragmented_event_absorption`
- `ecluster_04_deteriorating_cluster_avoidance`
- `ecluster_05_aging_cluster_memory`

Current empirical result:

- All five candidates were mechanically classified `REJECT`.

## SECTION 2 - Candidate-Level Review

### `ecluster_01_concentrated_absorption`

Original hypothesis:

- Concentrated nearby events with controlled response should behave differently from isolated-event names.

Expected primary horizon:

- h10, with h5 support and h20 durability only.

Observed horizon behavior:

- Observed strongest horizon was h1, not h10.
- Best-any mean IC was still negative at -0.005969.

Mean IC evidence:

- Expected-primary h10 mean IC: -0.010535.
- Expected-primary h10 IC IR: -0.085312.
- Expected-primary positive IC rate: 0.454848.

Rolling stability evidence:

- Rolling h10 evidence was not stable enough to rescue the candidate. The saved rolling summary shows negative 126-day and 252-day latest h10 mean IC, and the rolling ranges include materially negative regimes.
- h5 had a mildly positive latest rolling mean in the saved 63/126/252-day windows, but the full-sample h5 and expected-primary h10 evidence remained negative. This cannot rescue an h10 candidate.

Hypothesis consistency:

- `MISMATCH`.

Scientific interpretation:

- Event Concentration did not show that clustered events add information beyond isolated event structure. The observed h1 dominance is weaker than the frozen h10 expectation and remains negative.

Recommended research status:

- `REJECT`; include in module-level park recommendation.

### `ecluster_02_aligned_pressure_resolution`

Original hypothesis:

- Coherent multi-event alignment followed by controlled response should identify resolved event pressure.

Expected primary horizon:

- h10, with h5 support and h20 durability only.

Observed horizon behavior:

- Observed strongest horizon was h1, not h10.
- It was the least negative candidate overall, but the best-any h1 mean IC was still -0.000285.

Mean IC evidence:

- Expected-primary h10 mean IC: -0.004602.
- Expected-primary h10 IC IR: -0.059535.
- Expected-primary positive IC rate: 0.474906.

Rolling stability evidence:

- The saved rolling h10 stability fields show negative latest 63-day, 126-day, and 252-day mean IC. h5 had a positive latest 252-day rolling mean, but this did not overcome the negative expected-primary h10 full-sample evidence.

Hypothesis consistency:

- `MISMATCH`.

Scientific interpretation:

- Alignment and pressure resolution was the most diagnostic candidate in relative terms, but only because it was least negative. It did not generate positive h10 evidence and cannot be promoted on h1 or h5 fragments.

Recommended research status:

- `REJECT`; note as the least negative expression if a future independent hypothesis revisits event topology.

### `ecluster_03_fragmented_event_absorption`

Original hypothesis:

- Fragmented event clusters that are absorbed should carry short-to-medium horizon information distinct from noisy disagreement.

Expected primary horizon:

- h5, with h10 support and h20 durability only.

Observed horizon behavior:

- Observed strongest horizon was h1, not h5.
- Best-any mean IC was -0.002812.

Mean IC evidence:

- Expected-primary h5 mean IC: -0.006978.
- Expected-primary h5 IC IR: -0.095080.
- Expected-primary positive IC rate: 0.476244.

Rolling stability evidence:

- Rolling h5, h10, and h20 summaries were negative in the latest 63/126/252-day windows. Longer horizons deteriorated further in the saved rolling stability table.

Hypothesis consistency:

- `MISMATCH`.

Scientific interpretation:

- Fragmentation did not separate absorbed disagreement from noise. The predeclared stop condition for h1-only evidence is directionally relevant, and h1 itself was still negative.

Recommended research status:

- `REJECT`; include in module-level park recommendation.

### `ecluster_04_deteriorating_cluster_avoidance`

Original hypothesis:

- Avoiding securities with deteriorating repeated-event pressure should add information beyond stress repair and reversal.

Expected primary horizon:

- h5, with h10 support and h20 durability only.

Observed horizon behavior:

- Observed strongest horizon was h1, not h5.
- Best-any mean IC was -0.005733.

Mean IC evidence:

- Expected-primary h5 mean IC: -0.008526.
- Expected-primary h5 IC IR: -0.078322.
- Expected-primary positive IC rate: 0.465738.

Rolling stability evidence:

- Rolling h5 latest means were mildly negative across 63/126/252-day windows, and h10/h20 rolling evidence was more negative. The saved evidence does not support a stable avoidance effect.

Hypothesis consistency:

- `MISMATCH`.

Scientific interpretation:

- The deterioration-avoidance concept did not add information beyond the likely stress/reversal reference space. Its strongest internal diagnostic correlation was with `stress_proxy_20`, which strengthens the concern that this mechanism is not independently expressed.

Recommended research status:

- `REJECT`; include in module-level park recommendation.

### `ecluster_05_aging_cluster_memory`

Original hypothesis:

- Cluster age should change the interpretation of repeated events beyond volatility compression or stress repair.

Expected primary horizon:

- h10, with h5 support and h20 durability only.

Observed horizon behavior:

- Observed strongest horizon was h1, not h10.
- Best-any mean IC was -0.001604.

Mean IC evidence:

- Expected-primary h10 mean IC: -0.009069.
- Expected-primary h10 IC IR: -0.090786.
- Expected-primary positive IC rate: 0.457278.

Rolling stability evidence:

- Latest rolling h10 and h20 means were negative across 63/126/252-day windows. h5 latest rolling means were also negative. The aging/memory state did not show durable positive behavior.

Hypothesis consistency:

- `MISMATCH`.

Scientific interpretation:

- Cluster memory was not observed at h10. The result suggests that event memory either decays too quickly to be captured by this OHLCV-only cluster-aging design or is already absorbed by existing persistence, volatility, stress, or transition-state proxies.

Recommended research status:

- `REJECT`; include in module-level park recommendation.

## SECTION 3 - Mechanism-Level Review

| mechanism | review conclusion | interpretation |
| --- | --- | --- |
| Event Concentration | contradicted | The sole concentration candidate had negative h10 evidence and h1 was only less negative. Concentration did not show a cluster increment over isolated-event logic. |
| Event Alignment And Fragmentation | weakly diagnostic but unsupported | Alignment was least negative, and fragmentation had sparse activation, but both failed their expected primary horizons. The mechanism is diagnostic only, not promotable. |
| Cluster Absorption Versus Deterioration | contradicted and likely contaminated | The deterioration-avoidance candidate had negative h5 evidence and its strongest diagnostic association pointed toward stress. |
| Cluster Aging And Market Memory | horizon-mismatched and unsupported | Aging/memory did not hold at h10. The best horizon was h1 and remained negative, suggesting no durable market-memory effect. |

Contamination judgment:

- The saved IC evidence does not justify a positive contamination attribution because no candidate produced positive primary-horizon evidence. However, the direction of failure is consistent with the family collapsing into short-lived event/reversal noise, stress state, non-hostile transition proxies, volatility behavior, persistence, or isolated-event effects rather than establishing a distinct event-topology family.

## SECTION 4 - Horizon Interpretation

All candidates were strongest at h1.

This does not rescue the family because:

- every h1 best-any mean IC was still negative;
- h1 was not the frozen primary horizon for any candidate;
- h1 evidence was explicitly diagnostic only in the design;
- Platform v2 prohibits horizon shopping after observing results.

Interpretation of the h1 pattern:

- The h1 pattern is best read as rapid information decay or immediate event-noise absorption, not as usable evidence.
- Because h1 is merely less negative, it does not indicate an actionable short-horizon effect.
- The pattern is compatible with isolated-event/reversal contamination: event topology may be capturing the immediate aftermath of event shocks without durable h5/h10 structure.
- The h5/h10 scientific hypothesis is falsified for this candidate set because expected-primary evidence was negative for all five candidates.

h20 interpretation:

- h20 was weaker than h5/h10 in the family-level interpretation and cannot rescue failed primary horizons. The frozen design allowed h20 only as durability evidence.

## SECTION 5 - Family-Level Interpretation

Clustered events did not add positive information beyond isolated events under this OHLCV-only design.

Temporal concentration:

- Not supported. Concentrated event absorption failed at h10 and did not produce a positive best-any horizon.

Alignment and fragmentation:

- Not supported for advancement. Alignment was the least negative result, but still negative at h10. Fragmentation was negative at h5 and showed no stable medium-horizon absorption effect.

Absorption and deterioration:

- Not supported. Avoiding deteriorating clusters did not produce positive h5 evidence and appears vulnerable to stress/reversal contamination.

Aging and memory:

- Not supported. Aging cluster memory failed at h10 and did not show durable rolling stability.

Family collapse risk:

- The family does not currently stand as an independent alpha-family frontier. The empirical evidence suggests that OHLCV-only event topology is either too noisy, too rapidly absorbed, or already represented by existing volatility, stress, reversal, persistence, rank, volume, dispersion, or transition-state references.

## SECTION 6 - Scientific Learning

Project Underdog learned the following:

1. Event topology is scientifically plausible but was not predictive in this frozen OHLCV-only implementation.
2. Clustered events did not produce durable h5/h10 cross-sectional evidence.
3. The least negative behavior appeared at h1, but h1 remained negative and is not a valid rescue horizon.
4. Event memory appears too short-lived, too noisy, or too entangled with existing families to support this module.
5. Alignment may be diagnostically interesting, but the evidence is insufficient for advancement or refinement.
6. The negative result is useful: Event Clustering should remain a contamination reference or archived hypothesis space, not an active candidate family.
7. A future revisit should require a new independent scientific hypothesis, not formula tinkering around these rejected candidates.

Scientific closeout:

- The current Event Clustering hypothesis space should be treated as closed for now.
- The appropriate research action is `PARK_MODULE`.

## SECTION 7 - Platform v2 Assessment

Platform v2 process assessment:

| process requirement | assessment |
| --- | --- |
| Frozen hypotheses preserved | PASS. Candidate hypotheses and primary horizons were frozen before IC. |
| Horizon shopping prevented | PASS. h1 was not used to rescue h5/h10 candidates. |
| Manual promotion prevented | PASS. All recommendations were mechanically assigned from predefined IC evidence. |
| Audited-panel reproducibility preserved | PASS. IC Discovery used the approved panel snapshot and recorded checksums. |
| Trustworthy negative result produced | PASS. The process generated a clear negative result without threshold changes, target hacking, or refinement. |

The most important process success is that the module was allowed to fail cleanly. The negative result is scientifically trustworthy because the platform did not reinterpret h1 as success, did not weaken the primary horizon requirement, and did not create post-hoc variants.

## SECTION 8 - Future Recommendation

Chosen recommendation:

- `PARK_MODULE`

Rationale:

- All five candidates were rejected.
- All expected-primary horizons failed.
- All observed strongest horizons were h1 and still negative.
- No mechanism generated enough evidence for advancement.
- No refinement is authorized by this review.
- Any future revisit must begin with a new independent scientific hypothesis and a new lifecycle entry point.

This recommendation does not itself perform governance. The following lifecycle phase may conduct the governance decision, archival action, or formal module parking process.

## SECTION 9 - Verification

Confirmed:

- No IC recomputation was performed.
- No panel regeneration was performed.
- No formula changes were made.
- No implementation changes were made.
- No new candidates were proposed.
- No refinement was performed.
- No validation was performed.
- No governance mutation was performed.
- No production changes were made.
- No thresholds were changed.
- No ML was introduced.

## SECTION 10 - Classification

Classification: `RESEARCH_REVIEW_RECOMMEND_PARK`

Final research judgment:

- The Event Clustering Research Module produced a trustworthy negative IC Discovery result.
- The module should not proceed to validation, refinement, production, threshold adjustment, or ML.
- The recommended next lifecycle phase is Governance Review v1 to adjudicate the `PARK_MODULE` research recommendation. The governance decision is not made in this review.
