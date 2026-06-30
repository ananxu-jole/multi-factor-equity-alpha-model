# Alpha Family Diversification IC Discovery Pass v1

Date: 2026-06-17

Run id: `alpha_family_diversification_ic_discovery_v1`

Source run id: `alpha_family_diversification_discovery_v1`

Review scope: research-only IC discovery scoring for the 8-candidate subset recommended in `alpha_family_diversification_panel_and_redundancy_review_v1.md`. No validation, refinement, governance mutation, threshold change, production registration, ML, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

Scoring scope:
- 8 candidates only
- 5 dispersion candidates
- 3 persistence / rank-stability candidates
- Scored horizons: h1, h5, h10, h20
- Primary declared candidate horizon: h10-h20
- IC method: daily cross-sectional rank IC versus forward close-to-close returns

Scoring completed successfully. Outputs were written only under:
- `artifacts/research/alpha_family_diversification_discovery_v1/ic_discovery/`

Output files:
- `approved_scoring_subset.csv`
- `candidate_horizon_ic_scores.csv`
- `daily_ic_by_candidate_horizon.csv`
- `approved_subset_redundancy_context.csv`
- `candidate_ic_summary.csv`
- `family_ic_summary.csv`
- `horizon_ic_summary.csv`
- `manifest.json`

Strongest family:
- At the family-average level, dispersion is less negative and more stable than persistence.
- At the individual-candidate level, persistence contains the strongest candidate: `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`.

Weakest family:
- Persistence is weakest at the family-average level because `rank_stability_after_drawdown_01` is materially negative across all horizons.

Diversification evidence:
- There is limited but real early evidence of diversification at the candidate level, not at the full-family level.
- `post_drawdown_persistence_20` shows the cleanest positive IC evidence and low approved-subset redundancy.
- `dispersion_transition_acceleration_20` shows modest positive short-to-medium horizon evidence with very low approved-subset redundancy.
- The full subset does not yet show broad h10-h20 alpha-family strength.

Aggregate horizon behavior:
- h1 mean IC: -0.0026
- h5 mean IC: -0.0056
- h10 mean IC: -0.0096
- h20 mean IC: -0.0132

The aggregate horizon profile weakens as horizon extends, which is not ideal for an h10-h20-oriented batch.

## SECTION 2 - Candidate Scoring Results

| Candidate ID | Family | Theme | Horizon | Mean IC | IC IR | Positive IC Rate | Redundancy context | Preliminary interpretation |
|---|---|---|---:|---:|---:|---:|---|---|
| dispersion_expansion_transition_02 | dispersion | Dispersion Expansion Transition | h20 | -0.0237 | -0.2246 | 0.4246 | moderate approved-subset redundancy | Weak. Negative IC strengthens with horizon; do not refine now. |
| dispersion_expansion_transition_04 | dispersion | Dispersion Expansion Transition | h10 | 0.0082 | 0.0933 | 0.5464 | low approved-subset redundancy | Modest positive evidence and highly distinct; best dispersion refinement candidate. |
| dispersion_compression_reversal_02 | dispersion | Dispersion Compression Reversal | h10 | -0.0097 | -0.0724 | 0.4555 | moderate approved-subset redundancy | Weak. Compression representative does not show positive h10-h20 evidence. |
| dispersion_structure_anomalies_01 | dispersion | Dispersion Structure Anomalies | h20 | -0.0145 | -0.0867 | 0.5000 | moderate approved-subset redundancy | Weak/diagnostic. Negative mean IC despite balanced positive rate. |
| dispersion_structure_anomalies_03 | dispersion | Dispersion Structure Anomalies | h20 | -0.0119 | -0.0819 | 0.4897 | moderate approved-subset redundancy | Weak. h1 is positive but h10-h20 fades/inverts. |
| rank_stability_after_drawdown_01 | persistence | Rank Stability After Drawdown | h20 | -0.0593 | -0.2680 | 0.4013 | moderate approved-subset redundancy | Clearly weak in current orientation; strongest exclusion candidate. |
| rank_stability_after_drawdown_02 | persistence | Rank Stability After Drawdown | h10 | 0.0125 | 0.1208 | 0.5951 | low approved-subset redundancy | Strongest early evidence. Positive h5/h10 profile and low redundancy. |
| rank_coherence_regime_transition_02 | persistence | Rank Coherence Regime Transition | h20 | 0.0060 | 0.0408 | 0.5124 | moderate approved-subset redundancy | Mild h20 evidence, but modest and redundant with compression stability. Diagnostic/refinement watchlist. |

Candidate horizon notes:
- `post_drawdown_persistence_20`: h5 mean IC 0.0137, h10 mean IC 0.0125, h20 mean IC 0.0059. This is the only candidate with a convincing h5/h10 positive-rate profile.
- `dispersion_transition_acceleration_20`: h1 0.0078, h5 0.0099, h10 0.0082, h20 -0.0007. This is short-to-medium horizon evidence, not h20 evidence.
- `transition_rank_stability_20`: h20 0.0060 after negative h1/h5/h10. This may be horizon-specific but is weak.
- `drawdown_rank_stability_20`: h10 -0.0585 and h20 -0.0593. Current orientation appears adverse.

## SECTION 3 - Family-Level Results

Dispersion family:
- Candidate count: 5
- h1 mean IC: 0.0008
- h5 mean IC: -0.0025
- h10 mean IC: -0.0053
- h20 mean IC: -0.0117
- h20 mean positive IC rate: 0.4842

Interpretation:
- Dispersion is not broadly positive.
- The family average weakens as horizon extends.
- The useful signal is concentrated in `dispersion_transition_acceleration_20`, with some short-to-medium horizon evidence and low redundancy.
- Dispersion still has diversification value because at least one candidate is statistically distinct and nonduplicative, but family-level IC evidence is not yet strong.

Persistence / rank-stability family:
- Candidate count: 3
- h1 mean IC: -0.0084
- h5 mean IC: -0.0107
- h10 mean IC: -0.0166
- h20 mean IC: -0.0158
- h20 mean positive IC rate: 0.4816

Interpretation:
- Persistence is polarized.
- `post_drawdown_persistence_20` is the best single candidate in the batch.
- `drawdown_rank_stability_20` is strongly negative and drags down the family.
- `transition_rank_stability_20` has mild h20 evidence but is not strong enough to carry the family.

Distinctiveness:
- Dispersion has broader structural variety.
- Persistence has the strongest individual IC result but weaker family-level consistency.

Diversification value:
- The batch moves the project closer to diversification if refinement focuses on the two useful candidates rather than the whole family set.
- Evidence supports candidate-level exploration, not family-level adoption.

## SECTION 4 - Redundancy-Adjusted Findings

Prior redundancy diagnostics were used only to interpret discovery IC results. No threshold, governance, or promotion decision was applied.

Promising and distinct:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`
  - h10 mean IC: 0.0125
  - h10 positive IC rate: 0.5951
  - max approved-subset redundancy: 0.1815
  - Interpretation: strongest refinement candidate; useful persistence-family evidence.
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`
  - h10 mean IC: 0.0082
  - h10 positive IC rate: 0.5464
  - max approved-subset redundancy: 0.0455
  - Interpretation: modest but very distinct dispersion evidence; worth formula refinement or robustness-oriented redesign.

Promising but redundant:
- `rank_coherence_regime_transition_02` / `transition_rank_stability_20`
  - h20 mean IC: 0.0060
  - h20 positive IC rate: 0.5124
  - max approved-subset redundancy: 0.5202
  - Interpretation: mild evidence, but redundancy with `dispersion_compression_stability_20` weakens the case.

Weak:
- `dispersion_expansion_transition_02` / `dispersion_expansion_momentum_20`
  - h20 mean IC: -0.0237
  - Interpretation: negative h10/h20 behavior; exclude from refinement.
- `dispersion_compression_reversal_02` / `dispersion_compression_stability_20`
  - h10 mean IC: -0.0097
  - Interpretation: negative primary-horizon IC and moderate redundancy; exclude from refinement.
- `dispersion_structure_anomalies_01` / `dispersion_skew_anomaly_20`
  - h20 mean IC: -0.0145
  - Interpretation: structurally interesting but weak; diagnostic-only.
- `dispersion_structure_anomalies_03` / `cross_sectional_asymmetry_20`
  - h20 mean IC: -0.0119
  - Interpretation: h1 positive but h10/h20 weak; diagnostic-only.
- `rank_stability_after_drawdown_01` / `drawdown_rank_stability_20`
  - h20 mean IC: -0.0593
  - Interpretation: current signal orientation is adverse; exclude from refinement.

Diagnostic-only candidates:
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_coherence_regime_transition_02`

These may still be useful for understanding family structure, but the current IC pass does not justify direct refinement priority.

## SECTION 5 - Readiness Decision

1. Did either new family show useful IC evidence?

Yes, but only at the candidate level.

Persistence showed the clearest individual evidence through `post_drawdown_persistence_20`.

Dispersion showed weaker but more distinct evidence through `dispersion_transition_acceleration_20`.

Neither family showed broad, family-level h10-h20 strength across the scored subset.

2. Which candidates deserve refinement consideration?

Primary refinement consideration:
- `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`

Secondary refinement consideration:
- `dispersion_expansion_transition_04` / `dispersion_transition_acceleration_20`

Diagnostic/watchlist only:
- `rank_coherence_regime_transition_02` / `transition_rank_stability_20`

3. Which candidates should be excluded from refinement?

Exclude from refinement based on this discovery-only IC pass:
- `dispersion_expansion_transition_02`
- `dispersion_compression_reversal_02`
- `rank_stability_after_drawdown_01`

Keep diagnostic-only rather than refine directly:
- `dispersion_structure_anomalies_01`
- `dispersion_structure_anomalies_03`
- `rank_coherence_regime_transition_02`

4. Is the project closer to alpha-family diversification?

Yes, modestly. The project now has evidence that at least one persistence/rank-stability candidate may carry positive IC with low redundancy, and one dispersion-transition candidate may offer distinct short-to-medium-horizon behavior.

However, the batch does not yet establish a robust new alpha family. It narrows the search from 8 scored candidates to 2 refinement candidates plus one diagnostic watchlist candidate.

5. What should the next Codex task be?

Implement a research-only refinement design for:
- `post_drawdown_persistence_20`
- `dispersion_transition_acceleration_20`

The next task should not run validation or governance. It should inspect formula construction, sign orientation, horizon targeting, active coverage, and redundancy context, then propose or generate limited diagnostic variants for a second discovery pass.

## Research Caveat

This was a discovery-only IC scoring pass. Results are not validation evidence, are not production evidence, and do not authorize candidate promotion, demotion, governance action, threshold changes, ML integration, or production registration.
