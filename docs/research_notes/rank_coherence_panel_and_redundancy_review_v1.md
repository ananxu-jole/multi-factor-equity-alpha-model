# Rank-Coherence Panel and Redundancy Review v1

Date: 2026-06-18

Project: Project Underdog

Run id reviewed: `rank_coherence_family_discovery_v1`

Scope: review-only panel and redundancy review. No IC scoring, refinement, validation, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Panel generation completed successfully. The rank-coherence runner produced 10 candidate panels, 10 metadata files, a panel manifest, generation summary, source input diagnostics, metadata redundancy screening, and statistical redundancy screening.

The artifact set is complete and usable for pre-IC review. All 10 panels have required long-form columns, non-null signal values, finite signal values, and usable date/ticker coverage. Source inputs loaded successfully from `artifacts/panels/signals/`.

Redundancy diagnostics are usable. The statistical redundancy table contains 90 directional rows, equal to 10 candidates x 9 comparisons, and every row has `diagnostic_status = computed`. No missing candidate panels were reported.

The full 10-candidate set is too redundant to score as-is. A reduced six-candidate subset should proceed to first IC discovery scoring, while four high-overlap candidates should be excluded from the first scoring pass due to duplicate-cluster risk.

## SECTION 2 - Candidate Panel Review

Candidate count:
- Registry candidates: 10.
- Generated panel rows in manifest: 10.
- Generated parquet panel files: 10.
- Generated metadata JSON files: 10.

Families represented:
- `rank_coherence`: 10 candidates.

Themes represented:
- Leadership Stability: 2 candidates.
- Rank Churn Avoidance: 2 candidates.
- Rank Reversal Pressure: 2 candidates.
- Leadership Concentration and Broadening: 2 candidates.
- Regime-Independent Rank Coherence: 2 candidates.

Horizons represented:
- `h10-h20`: 8 candidates.
- `h5-h10`: 2 candidates, both rank reversal pressure candidates.

Panel completeness:
- Date range: 2024-05-03 to 2026-05-07.
- Date count: 504 dates for each reviewed panel.
- Ticker count range: 462 to 478 tickers.
- Row count range: 230,685 to 240,163 observations.
- Required columns present in all panels: `date`, `ticker`, `candidate_id`, `signal_value`, `family`, `theme`, `horizon`.
- Null signal values: 0 in all generated long-form panels.
- Finite signal coverage: 100% in all generated long-form panels.

Missing or invalid panel issues:
- No missing panel files were observed.
- No missing metadata files were observed.
- No invalid panel schema issues were observed.
- No statistical redundancy rows reported missing panels.

## SECTION 3 - Metadata Redundancy Review

Advisory redundancy classes:
- `HIGH_METADATA_REDUNDANCY`: 10 candidates.

Candidates requiring manual review:
- `review_required = False`: 10 candidates.
- `review_required = True`: 0 candidates.

Triggered metadata checks:
- `family_overlap`: 10 candidates.
- `theme_overlap`: 10 candidates.
- `feature_group_overlap`: 10 candidates.
- `horizon_overlap`: 10 candidates.
- `candidate_id_prefix_overlap`: 10 candidates.
- `flagged_high_redundancy_risk`: 4 candidates.

Interpretation:
- The metadata screen flags high redundancy because the batch is intentionally one family with paired candidates per theme and shared rank-coherence naming.
- This is expected for a structured rank-coherence batch and is not by itself a blocker.
- No metadata candidate was marked `REVIEW_REQUIRED`.

Persistence duplication signs:
- The two rank-churn candidates carry declared high redundancy risk versus persistence lineage.
- No candidate uses the persistence family label.
- No candidate is framed as post-drawdown persistence or drawdown repair in the registry.
- Later IC scoring should still include persistence-lineage redundancy context before any refinement recommendation.

Hostile/stress-repair contamination signs:
- No metadata review flag fired for stress/participation contamination.
- No candidate is labeled as hostile/stress-repair, participation repair, liquidity repair, weak-breadth repair, or recovery.
- Source-input review shows rank, trend, smooth-trend, residual, and reversal panels were used; prohibited repair labels were not introduced into the registry.

## SECTION 4 - Statistical Redundancy Review

Statistical redundancy coverage:
- Directional rows: 90.
- Unique unordered candidate pairs: 45.
- Diagnostic status: all rows `computed`.

Descriptive correlation profile:
- Mean absolute value correlation: 0.414.
- Median absolute value correlation: 0.441.
- Maximum absolute value correlation: 0.875.
- Mean absolute rank correlation: 0.414.
- Median absolute rank correlation: 0.441.
- Maximum absolute rank correlation: 0.877.

Review-only descriptive bands used in this memo:
- Statistically distinct: max absolute value/rank correlation below roughly 0.35.
- Moderately related: roughly 0.35 to 0.60.
- Highly redundant: roughly 0.60 to 0.80.
- Likely duplicate: above roughly 0.80.

These are review labels only, not governance thresholds or validation gates.

Highest redundancy pairs:

| Candidate A | Candidate B | Value corr | Rank corr | Review read |
|---|---|---:|---:|---|
| `rank_coherence_leadership_stability_01` | `rank_coherence_concentration_01` | 0.875 | 0.877 | likely duplicate |
| `rank_coherence_churn_avoidance_01` | `rank_coherence_concentration_02` | 0.860 | 0.861 | likely duplicate |
| `rank_coherence_leadership_stability_02` | `rank_coherence_regime_independent_01` | 0.860 | 0.860 | likely duplicate |
| `rank_coherence_concentration_01` | `rank_coherence_regime_independent_01` | 0.833 | 0.833 | likely duplicate |
| `rank_coherence_concentration_01` | `rank_coherence_regime_independent_02` | 0.738 | 0.738 | highly redundant |
| `rank_coherence_leadership_stability_01` | `rank_coherence_regime_independent_01` | 0.713 | 0.715 | highly redundant |
| `rank_coherence_leadership_stability_01` | `rank_coherence_regime_independent_02` | 0.691 | 0.693 | highly redundant |
| `rank_coherence_churn_avoidance_02` | `rank_coherence_regime_independent_01` | 0.693 | 0.693 | highly redundant |

Lowest redundancy pairs:

| Candidate A | Candidate B | Value corr | Rank corr | Review read |
|---|---|---:|---:|---|
| `rank_coherence_reversal_pressure_01` | `rank_coherence_concentration_01` | 0.008 | 0.008 | distinct |
| `rank_coherence_reversal_pressure_02` | `rank_coherence_concentration_02` | 0.014 | 0.014 | distinct |
| `rank_coherence_churn_avoidance_02` | `rank_coherence_reversal_pressure_01` | 0.026 | 0.026 | distinct |
| `rank_coherence_reversal_pressure_02` | `rank_coherence_regime_independent_01` | 0.032 | 0.032 | distinct |
| `rank_coherence_leadership_stability_02` | `rank_coherence_reversal_pressure_01` | -0.068 | -0.068 | distinct |
| `rank_coherence_reversal_pressure_02` | `rank_coherence_concentration_01` | -0.072 | -0.072 | distinct |
| `rank_coherence_reversal_pressure_01` | `rank_coherence_regime_independent_02` | 0.076 | 0.076 | distinct |
| `rank_coherence_reversal_pressure_02` | `rank_coherence_regime_independent_02` | -0.077 | -0.077 | distinct |

Candidate-level redundancy classification:

| Candidate ID | Max abs corr | Top redundancy peer | Classification |
|---|---:|---|---|
| `rank_coherence_reversal_pressure_02` | 0.294 | `rank_coherence_reversal_pressure_01` | statistically distinct |
| `rank_coherence_reversal_pressure_01` | 0.453 | `rank_coherence_concentration_02` | moderately related |
| `rank_coherence_churn_avoidance_02` | 0.693 | `rank_coherence_regime_independent_01` | highly redundant |
| `rank_coherence_regime_independent_02` | 0.738 | `rank_coherence_concentration_01` | highly redundant |
| `rank_coherence_leadership_stability_02` | 0.860 | `rank_coherence_regime_independent_01` | likely duplicate |
| `rank_coherence_regime_independent_01` | 0.860 | `rank_coherence_leadership_stability_02` | likely duplicate |
| `rank_coherence_churn_avoidance_01` | 0.861 | `rank_coherence_concentration_02` | likely duplicate |
| `rank_coherence_concentration_02` | 0.861 | `rank_coherence_churn_avoidance_01` | likely duplicate |
| `rank_coherence_leadership_stability_01` | 0.877 | `rank_coherence_concentration_01` | likely duplicate |
| `rank_coherence_concentration_01` | 0.877 | `rank_coherence_leadership_stability_01` | likely duplicate |

Theme-level redundancy:
- Within-theme pairs: mean max absolute correlation 0.469, median 0.479, max 0.605.
- Cross-theme pairs: mean max absolute correlation 0.407, median 0.437, max 0.877.
- The highest redundancy is cross-theme, not within-theme, especially between leadership stability, leadership concentration, and regime-independent coherence.
- Rank Reversal Pressure is the most statistically distinct theme, with low correlations versus most other themes.

## SECTION 5 - Rank-Coherence Family Assessment

Does the batch appear to represent rank-coherence rather than persistence?

Yes, at the panel and registry level. The candidates are built around leadership retention, cross-window agreement, rank churn, rank reversal pressure, leadership concentration/broadening, and state-neutral rank coherence. They are not labeled as persistence and do not use post-drawdown persistence framing.

Are any candidates just renamed persistence variants?

No direct artifact-level evidence shows simple renamed persistence variants. However, rank-churn candidates are conceptually closest to persistence and should be evaluated carefully in later redundancy review versus `post_drawdown_persistence_churn_adjusted_20`, `post_drawdown_persistence_core_20`, and `post_drawdown_persistence_20`. The current statistical screen only covers the 10 rank-coherence panels against each other, so persistence-lineage comparison remains a required next diagnostic before refinement decisions.

Are any candidates contaminated by stress/repair behavior?

No metadata-level contamination was observed. No candidate was marked review-required for stress/participation keywords, and the registry does not include hostile, stress, participation-repair, liquidity-repair, weak-breadth, or recovery framing. Later scoring review should still include state attribution and stress-repair reference comparisons.

Is the candidate set sufficiently diversified to justify IC scoring?

Yes, but not as the full 10-candidate set. The full set contains several likely duplicate pairs. A reduced subset can preserve the family breadth while avoiding the worst duplicate clusters.

## SECTION 6 - Candidate-Level Recommendations

| Candidate ID | Theme | Horizon | Redundancy status | Review status | Recommended next action |
|---|---|---|---|---|---|
| `rank_coherence_leadership_stability_01` | Leadership Stability | h10-h20 | likely duplicate with concentration quality | duplicate-cluster risk | exclude from next scoring pass due to redundancy |
| `rank_coherence_leadership_stability_02` | Leadership Stability | h10-h20 | likely duplicate with state-neutral coherence, but useful pure rank-agreement representative | usable with caution | proceed to IC scoring |
| `rank_coherence_churn_avoidance_01` | Rank Churn Avoidance | h10-h20 | likely duplicate with leadership broadening entry | duplicate-cluster risk | exclude from next scoring pass due to redundancy |
| `rank_coherence_churn_avoidance_02` | Rank Churn Avoidance | h10-h20 | highly redundant with state-neutral coherence, but best churn-specific representative | usable with caution | proceed to IC scoring |
| `rank_coherence_reversal_pressure_01` | Rank Reversal Pressure | h5-h10 | moderately related; low overlap with most candidates | strong distinct representative | proceed to IC scoring |
| `rank_coherence_reversal_pressure_02` | Rank Reversal Pressure | h5-h10 | statistically distinct | strong distinct representative | proceed to IC scoring |
| `rank_coherence_concentration_01` | Leadership Concentration and Broadening | h10-h20 | likely duplicate with leadership retention | duplicate-cluster risk | exclude from next scoring pass due to redundancy |
| `rank_coherence_concentration_02` | Leadership Concentration and Broadening | h10-h20 | likely duplicate with churn-adjusted improvement, but lower overlap versus selected subset | usable concentration/broadening representative | proceed to IC scoring |
| `rank_coherence_regime_independent_01` | Regime-Independent Rank Coherence | h10-h20 | likely duplicate with cross-window agreement and concentration quality | duplicate-cluster risk | exclude from next scoring pass due to redundancy |
| `rank_coherence_regime_independent_02` | Regime-Independent Rank Coherence | h10-h20 | highly redundant with concentration quality, but usable versus selected subset | usable regime-independent representative | proceed to IC scoring |

These are research workflow recommendations only. They are not governance decisions, promotions, demotions, validation outcomes, or production registrations.

## SECTION 7 - Recommended IC Scoring Subset

Recommended first IC scoring subset: 6 candidates.

Proceed to IC scoring:
- `rank_coherence_leadership_stability_02`
- `rank_coherence_churn_avoidance_02`
- `rank_coherence_reversal_pressure_01`
- `rank_coherence_reversal_pressure_02`
- `rank_coherence_concentration_02`
- `rank_coherence_regime_independent_02`

Rationale:
- Preserves all five rank-coherence themes.
- Includes both reversal-pressure candidates because this is the most statistically distinct theme.
- Avoids the strongest duplicate pairs above 0.80.
- Keeps one representative from leadership stability, rank churn, concentration/broadening, and regime-independent coherence.
- Keeps the selected subset below the worst duplicate-cluster density of the full 10-candidate set.

Excluded from first IC scoring due to redundancy:
- `rank_coherence_leadership_stability_01`: likely duplicate with `rank_coherence_concentration_01`.
- `rank_coherence_churn_avoidance_01`: likely duplicate with `rank_coherence_concentration_02`.
- `rank_coherence_concentration_01`: likely duplicate with `rank_coherence_leadership_stability_01` and highly related to regime-independent candidates.
- `rank_coherence_regime_independent_01`: likely duplicate with `rank_coherence_leadership_stability_02` and `rank_coherence_concentration_01`.

Should all 10 candidates be scored?

No. Scoring all 10 would overweight duplicate formula clusters before the first IC read. The first IC scoring pass should use the six-candidate representative subset above. The excluded candidates can remain diagnostic references for later formula review if the selected subset produces useful evidence.

## SECTION 8 - Final Decision

1. Was panel generation successful?

Yes. All 10 candidate panels and metadata files were generated, and all panel manifest rows report `generation_status = generated`.

2. Is redundancy screening complete and usable?

Yes. Metadata redundancy screening and statistical redundancy screening are complete and usable for pre-IC triage. All 90 statistical redundancy rows computed successfully.

3. Which candidates should proceed to IC scoring?

Proceed with:
- `rank_coherence_leadership_stability_02`
- `rank_coherence_churn_avoidance_02`
- `rank_coherence_reversal_pressure_01`
- `rank_coherence_reversal_pressure_02`
- `rank_coherence_concentration_02`
- `rank_coherence_regime_independent_02`

4. Which candidates should be held back?

Exclude from the first scoring pass due to redundancy:
- `rank_coherence_leadership_stability_01`
- `rank_coherence_churn_avoidance_01`
- `rank_coherence_concentration_01`
- `rank_coherence_regime_independent_01`

No candidate needs diagnostic-only classification yet. Diagnostic-only classification should wait until IC scoring and, where relevant, persistence/stress-repair reference comparisons are reviewed.

5. What should the next Codex task be?

The next Codex task should be `Rank-Coherence IC Discovery Scoring v1`. It should score only the six approved candidates listed above across h1, h5, h10, and h20; produce candidate IC summaries, daily IC outputs, family/theme summaries, and redundancy context; and explicitly avoid refinement, validation, governance mutation, production registration, threshold changes, ML, and candidate promotion/demotion.

## Review Caveat

This review assessed generated panels and redundancy diagnostics only. It did not score forward-return IC, run refinement, run validation, modify governance, register production candidates, change thresholds, implement ML, or promote/demote candidates.
