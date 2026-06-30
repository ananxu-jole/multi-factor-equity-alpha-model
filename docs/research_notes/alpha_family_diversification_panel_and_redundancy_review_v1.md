# Alpha Family Diversification Panel and Redundancy Review v1

Date: 2026-06-17

Run id: `alpha_family_diversification_discovery_v1`

Review scope: research-only panel and redundancy artifact review. No validation, IC scoring, governance mutation, threshold change, production registration, ML, promotion, or demotion was performed.

## SECTION 1 - Executive Summary

Panel generation completed successfully.

The artifact set is complete for this stage:
- 17 approved candidates in `panel_manifest.csv`
- 17 candidate parquet panels in `candidate_panels/`
- 17 candidate metadata JSON files in `candidate_panels/`
- 17 panel-generation summary rows
- 17 metadata redundancy rows
- 272 directional statistical redundancy rows, equal to 17 candidates x 16 comparisons

Statistical redundancy diagnostics are usable. All 272 rows have `diagnostic_status = computed`; none report `missing_candidate_panel`. The diagnostic table contains value correlations, rank correlations, overlap observations, overlap dates, overlap tickers, and source panel paths.

The batch is ready for a first IC/discovery scoring pass only after applying the review-only candidate triage below. The full 17-candidate set is too redundant to score as-is without cluttering the first scoring pass. A reduced representative set should proceed first, while high-redundancy clusters should be held for manual formula review.

## SECTION 2 - Candidate Panel Review

Candidate count:
- Total candidates: 17
- Dispersion candidates: 11
- Persistence candidates: 6

Families represented:
- `dispersion`
- `persistence`

Themes represented:
- Dispersion Expansion Transition: 4 candidates
- Dispersion Compression Reversal: 4 candidates
- Dispersion Structure Anomalies: 3 candidates
- Rank Stability After Drawdown: 3 candidates
- Rank Coherence Regime Transition: 3 candidates

Horizons represented:
- `h10-h20`: 17 candidates

Panel completeness:
- Row count range: 141,541 to 240,649 observations per candidate
- Median row count: 215,116 observations
- Ticker count range: 349 to 478 tickers per candidate
- Median ticker count: 429 tickers
- Earliest panel start: 2024-05-03
- Latest panel start: 2024-06-03
- Common panel end date: 2026-05-07
- Generation status: all 17 rows are `generated`

Required panel columns are present:
- `date`
- `ticker`
- `candidate_id`
- `signal_value`
- `family`
- `theme`
- `horizon`

Missing or invalid panel issues:
- No missing candidate panel files were observed.
- No statistical redundancy rows report missing candidate panels.
- No invalid panel schema issue was observed from the reviewed artifacts.
- Panel metadata timestamps are not populated in `statistical_redundancy_screening.csv`, but panel paths and generated metadata files exist. This is a minor provenance improvement item, not a blocker for redundancy review.

## SECTION 3 - Metadata Redundancy Review

Advisory redundancy classes:
- `HIGH_METADATA_REDUNDANCY`: 17 candidates

Manual review flags:
- `review_required = False`: 17 candidates
- `review_required = True`: 0 candidates

Triggered metadata checks:
- `candidate_id_prefix_overlap`: 17
- `family_overlap`: 17
- `feature_group_overlap`: 17
- `horizon_overlap`: 17
- `theme_overlap`: 17
- `flagged_high_redundancy_risk`: 4

Interpretation:
- The metadata screen is intentionally conservative and flags the full batch because every candidate shares at least one family, theme, feature group, horizon, and candidate-id prefix pattern with another candidate.
- This is expected for a structured 17-candidate family-diversification batch.
- The metadata screen does not identify direct stress/participation contamination requiring manual review.
- The main metadata concern is intra-theme crowding, especially in Dispersion Compression Reversal and the rank-coherence/rank-stability boundary.

Stress/participation contamination:
- No candidate was marked `REVIEW_REQUIRED`.
- No stress/participation keyword review flag was triggered in the output.
- Based on artifacts only, there is no direct sign that candidates are simply renamed participation/liquidity repair candidates.
- Some generated formulas use failed-breakout or downtrend-stability source panels as secondary ingredients; those should be inspected in the next formula-review pass to ensure they remain rank/dispersion context rather than hostile/stress-repair proxies.

## SECTION 4 - Statistical Redundancy Review

The statistical table contains 136 unique unordered candidate pairs after de-duplicating the 272 directional comparisons.

Descriptive correlation profile:
- Mean absolute value correlation: 0.229
- Median absolute value correlation: 0.183
- Maximum absolute value correlation: 0.879
- Mean absolute rank correlation: 0.234
- Median absolute rank correlation: 0.186
- Maximum absolute rank correlation: 0.840

Review-only descriptive bands used in this memo:
- Statistically distinct: max absolute value/rank correlation below roughly 0.35
- Moderately related: roughly 0.35 to 0.60
- Highly redundant: roughly 0.60 to 0.80
- Likely duplicate: above roughly 0.80

These are review labels only, not governance thresholds or validation gates.

Highest redundancy pairs:

| Candidate A | Candidate B | Value corr | Rank corr | Review read |
|---|---:|---:|---:|---|
| dispersion_compression_reversal_01 | dispersion_compression_reversal_03 | 0.879 | 0.840 | likely duplicate |
| rank_stability_after_drawdown_03 | rank_coherence_regime_transition_01 | 0.718 | 0.743 | highly redundant |
| rank_stability_after_drawdown_03 | rank_coherence_regime_transition_03 | 0.695 | 0.725 | highly redundant |
| dispersion_compression_reversal_01 | dispersion_compression_reversal_02 | 0.679 | 0.679 | highly redundant |
| dispersion_expansion_transition_03 | dispersion_structure_anomalies_02 | 0.640 | 0.640 | highly redundant |
| dispersion_compression_reversal_02 | dispersion_compression_reversal_03 | 0.630 | 0.651 | highly redundant |
| dispersion_compression_reversal_02 | dispersion_compression_reversal_04 | 0.603 | 0.637 | highly redundant |
| dispersion_expansion_transition_01 | dispersion_expansion_transition_04 | -0.574 | -0.597 | moderately/highly related, inverse |

Lowest redundancy pairs:

| Candidate A | Candidate B | Value corr | Rank corr | Review read |
|---|---:|---:|---:|---|
| dispersion_compression_reversal_03 | dispersion_structure_anomalies_03 | -0.002 | -0.001 | distinct pair |
| dispersion_expansion_transition_02 | rank_stability_after_drawdown_02 | 0.003 | 0.003 | distinct pair |
| dispersion_expansion_transition_02 | dispersion_expansion_transition_03 | 0.001 | -0.004 | distinct pair |
| dispersion_expansion_transition_02 | rank_stability_after_drawdown_01 | 0.004 | 0.005 | distinct pair |
| dispersion_expansion_transition_01 | dispersion_expansion_transition_02 | -0.009 | -0.009 | distinct pair |
| dispersion_compression_reversal_04 | rank_stability_after_drawdown_02 | 0.007 | 0.010 | distinct pair |

Family-level redundancy:
- Within dispersion: mean max absolute correlation 0.229; median 0.146; max 0.879
- Within persistence: mean max absolute correlation 0.342; median 0.321; max 0.743
- Cross-family: mean max absolute correlation 0.216; median 0.185; max 0.565

Theme-level redundancy:
- Within-theme pairs are meaningfully more redundant than cross-theme pairs.
- Within-theme mean max absolute correlation: 0.360
- Cross-theme mean max absolute correlation: 0.212

Most redundant theme clusters:
- Dispersion Compression Reversal is the highest redundancy theme cluster, with mean max absolute correlation 0.619 and max 0.879.
- Rank Coherence Regime Transition is internally moderate, with mean max absolute correlation 0.401, but it overlaps materially with Rank Stability After Drawdown.
- Rank Coherence Regime Transition versus Rank Stability After Drawdown has mean max absolute correlation 0.380 and max 0.743.

Statistically distinct candidates:
- `rank_stability_after_drawdown_01` has the lowest candidate-level max correlation at 0.353.
- `dispersion_structure_anomalies_01` and `dispersion_structure_anomalies_03` are moderately related to each other but remain meaningfully distinct from the highest redundancy clusters.
- `dispersion_expansion_transition_02` has many very low pairwise correlations, though one moderate/high inverse relationship with `relative_correlation_compression_20`.

Moderately related candidates:
- `dispersion_expansion_transition_01`
- `dispersion_expansion_transition_02`
- `dispersion_expansion_transition_04`
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_stability_after_drawdown_01`
- `rank_stability_after_drawdown_02`
- `rank_coherence_regime_transition_02`

Highly redundant candidates:
- `dispersion_compression_reversal_01`
- `dispersion_compression_reversal_02`
- `dispersion_compression_reversal_04`
- `dispersion_expansion_transition_03`
- `dispersion_structure_anomalies_02`
- `rank_stability_after_drawdown_03`
- `rank_coherence_regime_transition_01`
- `rank_coherence_regime_transition_03`

Likely duplicate:
- `dispersion_compression_reversal_03` appears to be a likely duplicate of `dispersion_compression_reversal_01` based on value correlation 0.879 and rank correlation 0.840.

## SECTION 5 - Family Diversification Assessment

Does the batch add evidence of new alpha-family diversity?

Yes, at the panel and redundancy-diagnostic level. The batch now contains generated outputs for two non-production research families: dispersion and persistence. Cross-family correlations are lower than the highest within-theme clusters, and several dispersion/persistence pairs are near-zero correlated. That is useful evidence that the generated panels are not all one recycled signal.

Which family appears more distinct?

Dispersion appears broader but uneven. It contains the worst duplicate cluster in Dispersion Compression Reversal, but it also contains the most distinct pair behavior across Expansion and Structure Anomaly candidates. Persistence is more compact and internally more correlated, especially between Rank Stability After Drawdown and Rank Coherence Regime Transition.

On balance:
- Dispersion offers more family breadth.
- Persistence is cleaner conceptually but statistically tighter and more redundant.

Are any candidates simply recreating the old hostile/stress-repair family?

No direct evidence from the reviewed artifacts shows a simple recreation of the old hostile/stress-repair family. No metadata stress/participation review flag fired.

However, the formula ingredients documented in the panel-generation note include failed-breakout/downtrend-stability source panels for some persistence candidates. Those may still be legitimate rank-stability ingredients, but they should be reviewed before scoring to ensure they are not functioning as stress-repair proxies.

Is the candidate set sufficiently diversified to justify IC scoring?

Yes, but not as the full 17-candidate set. The reviewed artifacts support proceeding to IC scoring with a reduced representative subset. Highly redundant candidates should be held back or excluded from the next scoring pass to avoid overweighting duplicate formulas.

## SECTION 6 - Candidate-Level Recommendations

These are research workflow recommendations only. They are not governance decisions.

| Candidate ID | Family | Theme | Redundancy status | Review status | Recommended next action |
|---|---|---|---|---|---|
| dispersion_expansion_transition_01 | dispersion | Dispersion Expansion Transition | moderately/highly related to transition acceleration | needs formula-pair review | hold for manual review |
| dispersion_expansion_transition_02 | dispersion | Dispersion Expansion Transition | moderately related, many low-correlation pairs | usable representative | proceed to IC scoring |
| dispersion_expansion_transition_03 | dispersion | Dispersion Expansion Transition | highly redundant with cluster dispersion tail | needs pair review | hold for manual review |
| dispersion_expansion_transition_04 | dispersion | Dispersion Expansion Transition | moderately/highly inverse-related to expansion leadership | usable representative | proceed to IC scoring |
| dispersion_compression_reversal_01 | dispersion | Dispersion Compression Reversal | highly redundant, duplicate cluster anchor | needs compression-cluster review | hold for manual review |
| dispersion_compression_reversal_02 | dispersion | Dispersion Compression Reversal | highly redundant but usable as compression representative | usable with caution | proceed to IC scoring |
| dispersion_compression_reversal_03 | dispersion | Dispersion Compression Reversal | likely duplicate of compression_reversal_quality_20 | duplicate risk | exclude from next scoring pass due to redundancy |
| dispersion_compression_reversal_04 | dispersion | Dispersion Compression Reversal | highly redundant with compression stability and expansion momentum | needs compression-cluster review | hold for manual review |
| dispersion_structure_anomalies_01 | dispersion | Dispersion Structure Anomalies | moderately related, not in top duplicate cluster | usable representative | proceed to IC scoring |
| dispersion_structure_anomalies_02 | dispersion | Dispersion Structure Anomalies | highly redundant with relative dispersion ranking | needs pair review | hold for manual review |
| dispersion_structure_anomalies_03 | dispersion | Dispersion Structure Anomalies | moderately related, several low-correlation pairs | usable representative | proceed to IC scoring |
| rank_stability_after_drawdown_01 | persistence | Rank Stability After Drawdown | most distinct candidate-level profile | strong representative | proceed to IC scoring |
| rank_stability_after_drawdown_02 | persistence | Rank Stability After Drawdown | moderately related, acceptable breadth | usable representative | proceed to IC scoring |
| rank_stability_after_drawdown_03 | persistence | Rank Stability After Drawdown | highly redundant with rank coherence candidates | needs rank-cluster review | hold for manual review |
| rank_coherence_regime_transition_01 | persistence | Rank Coherence Regime Transition | highly redundant with rank churn resilience | needs rank-cluster review | hold for manual review |
| rank_coherence_regime_transition_02 | persistence | Rank Coherence Regime Transition | moderately/highly related but less duplicated than peers | usable representative | proceed to IC scoring |
| rank_coherence_regime_transition_03 | persistence | Rank Coherence Regime Transition | highly redundant with rank churn resilience | needs rank-cluster review | hold for manual review |

Recommended first IC scoring subset:
- `dispersion_expansion_transition_02`
- `dispersion_expansion_transition_04`
- `dispersion_compression_reversal_02`
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_stability_after_drawdown_01`
- `rank_stability_after_drawdown_02`
- `rank_coherence_regime_transition_02`

Hold for manual review:
- `dispersion_expansion_transition_01`
- `dispersion_expansion_transition_03`
- `dispersion_compression_reversal_01`
- `dispersion_compression_reversal_04`
- `dispersion_structure_anomalies_02`
- `rank_stability_after_drawdown_03`
- `rank_coherence_regime_transition_01`
- `rank_coherence_regime_transition_03`

Exclude from next scoring pass due to redundancy:
- `dispersion_compression_reversal_03`

Diagnostic-only:
- None required at this stage. Several held candidates may become diagnostic-only after formula review, but the current artifacts do not require that classification yet.

## SECTION 7 - Readiness Decision

1. Is the candidate panel generation successful?

Yes. The panel generation stage produced all 17 candidate panels, required manifest and summary artifacts, and no missing-panel diagnostics.

2. Is statistical redundancy screening complete and usable?

Yes. Statistical redundancy screening is complete and usable for panel-level redundancy review. All 272 directional comparisons computed successfully.

3. Which candidates should proceed to IC scoring?

Proceed with the reduced representative subset:
- `dispersion_expansion_transition_02`
- `dispersion_expansion_transition_04`
- `dispersion_compression_reversal_02`
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_stability_after_drawdown_01`
- `rank_stability_after_drawdown_02`
- `rank_coherence_regime_transition_02`

4. Which candidates should be held back?

Hold for manual review:
- `dispersion_expansion_transition_01`
- `dispersion_expansion_transition_03`
- `dispersion_compression_reversal_01`
- `dispersion_compression_reversal_04`
- `dispersion_structure_anomalies_02`
- `rank_stability_after_drawdown_03`
- `rank_coherence_regime_transition_01`
- `rank_coherence_regime_transition_03`

Exclude from the next scoring pass due to redundancy:
- `dispersion_compression_reversal_03`

5. What should the next Codex task be?

Implement a research-only IC scoring task for the reduced representative subset above, with explicit guardrails: no validation, no governance mutation, no threshold changes, no production registration, no ML, and no candidate promotion or demotion. The task should read the generated candidate panels and produce diagnostic IC outputs only.

## Review Caveat

This review is based only on generated panels and redundancy diagnostics. It does not assess forward-return efficacy, IC stability, walk-forward behavior, regime conditioning, production readiness, or portfolio impact.
