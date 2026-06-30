# Alpha Family Diversification Refinement Execution v1

Date: 2026-06-18

Run id: `alpha_family_diversification_refinement_v1`

Scope: research-only refinement execution for the two eligible candidates approved in `alpha_family_diversification_refinement_design_v1.md`. No validation, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

Artifact directory:
- `artifacts/research/alpha_family_diversification_refinement_v1/`

Primary outputs:
- `candidate_inventory.csv`
- `panel_manifest.csv`
- `candidate_horizon_scores.csv`
- `daily_ic_by_candidate_horizon.csv`
- `refinement_candidate_scores.csv`
- `family_summary.csv`
- `redundancy_context.csv`
- `manifest.json`

## SECTION 1 - Executive Summary

Refinement scope was kept inside the approved design:
- Eligible parent candidates: 2
- Original anchors retained: 2
- New persistence variants: 4
- New dispersion variants: 4
- Total scored refinement candidates: 10
- Scored horizons: h1, h5, h10, h20

The strongest refinement result was `rank_stability_after_drawdown_02_churn_adjusted` / `post_drawdown_persistence_churn_adjusted_20`, with h10 mean IC 0.0172, h10 IC IR 0.1734, h10 positive IC rate 0.6012, and h20 mean IC 0.0099. The similar `post_drawdown_persistence_core_20` result was nearly as strong, with h10 mean IC 0.0171 and h10 positive IC rate 0.6032.

The weakest refinement result was `dispersion_expansion_transition_04_rising_state` / `dispersion_transition_acceleration_rising_state_20`, with h10 mean IC -0.0084, h20 mean IC -0.0193, and h20 positive IC rate 0.4459. Narrowing the dispersion candidate to rising-dispersion states damaged evidence quality and reduced usable h10/h20 dates.

Family-level read:
- Persistence improved materially versus the original anchor and remains strongest at h5/h10.
- Dispersion remained distinct but weak; the original anchor and neutralized variant retained modest h10 evidence, while h20 continued to fade.
- Stress-repair proxy correlations were low across the refinement set, so there was no artifact-level evidence of direct drift into hostile/stress-repair behavior.

## SECTION 2 - Persistence Candidate Results

| Candidate ID | Signal | h10 mean IC | h10 IC IR | h10 positive IC rate | h20 mean IC | Interpretation |
|---|---|---:|---:|---:|---:|---|
| `rank_stability_after_drawdown_02_anchor` | `post_drawdown_persistence_20` | 0.0125 | 0.1208 | 0.5951 | 0.0059 | Original anchor remains positive and coherent at h5/h10, with expected h20 decay. |
| `rank_stability_after_drawdown_02_core` | `post_drawdown_persistence_core_20` | 0.0171 | 0.1730 | 0.6032 | 0.0099 | Best clean simplification. Removing the smooth-downtrend layer improved h5/h10 and h20 while preserving the rank-persistence thesis. |
| `rank_stability_after_drawdown_02_churn_adjusted` | `post_drawdown_persistence_churn_adjusted_20` | 0.0172 | 0.1734 | 0.6012 | 0.0099 | Strongest overall refinement result. Penalizing rank churn improved evidence without introducing stress-repair inputs. |
| `rank_stability_after_drawdown_02_smoothed` | `post_drawdown_persistence_smoothed_20` | 0.0102 | 0.0950 | 0.5630 | 0.0034 | Light smoothing weakened the signal; useful as a diagnostic that daily rank information may matter. |
| `rank_stability_after_drawdown_02_strict` | `post_drawdown_persistence_strict_20` | 0.0128 | 0.1229 | 0.6012 | 0.0058 | Stricter downtrend-rank context preserved the anchor profile but did not improve it materially. |

Persistence family summary:
- h5 family mean IC: 0.0154
- h10 family mean IC: 0.0139
- h20 family mean IC: 0.0070
- h10 mean positive IC rate: 0.5928

Interpretation: persistence refinement improved evidence quality. The core and churn-adjusted variants show that the candidate does not depend on the full original construction and that rank-churn discipline improves the result. The main remaining weakness is still horizon concentration: the signal is strongest at h5/h10 and weaker at h20.

## SECTION 3 - Dispersion Candidate Results

| Candidate ID | Signal | h10 mean IC | h10 IC IR | h10 positive IC rate | h20 mean IC | Interpretation |
|---|---|---:|---:|---:|---:|---|
| `dispersion_expansion_transition_04_anchor` | `dispersion_transition_acceleration_20` | 0.0080 | 0.0916 | 0.5460 | -0.0004 | Original anchor remains the best clean dispersion result, but evidence is still h5/h10 rather than h20. |
| `dispersion_expansion_transition_04_alt_accel` | `dispersion_transition_acceleration_alt_20` | -0.0008 | -0.0093 | 0.5207 | -0.0020 | Alternative acceleration definition did not preserve the effect. Diagnostic-only. |
| `dispersion_expansion_transition_04_smoothed` | `dispersion_transition_acceleration_smoothed_20` | 0.0022 | 0.0221 | 0.5257 | -0.0026 | Light smoothing weakened the useful signal, suggesting the transition effect is sensitive to timing. |
| `dispersion_expansion_transition_04_rising_state` | `dispersion_transition_acceleration_rising_state_20` | -0.0084 | -0.0973 | 0.4598 | -0.0193 | Weakest result. Narrow rising-state activation damaged h10/h20 behavior and should be rejected for now. |
| `dispersion_expansion_transition_04_neutralized` | `dispersion_transition_acceleration_neutralized_20` | 0.0077 | 0.0697 | 0.5243 | -0.0000 | Preserved modest h10 evidence while separating acceleration from raw dispersion level, but did not improve conviction. |

Dispersion family summary:
- h5 family mean IC: 0.0059
- h10 family mean IC: 0.0017
- h20 family mean IC: -0.0049
- h10 mean positive IC rate: 0.5153

Interpretation: dispersion remains interesting for distinctiveness, not strength. The anchor and neutralized variant justify continued diagnostic attention, but the refinement set did not produce a robust improvement. h20 decay remains unresolved.

## SECTION 4 - Diversification Assessment

Does persistence still appear distinct?

Yes, at the artifact level. Persistence variants are highly correlated with each other and with the original anchor, which is expected for a small refinement around one candidate. More importantly, stress-repair proxy correlations remained low: the strongest persistence stress-proxy correlations were roughly 0.04-0.06. That does not prove full family orthogonality, but it supports the view that this refinement did not simply recreate hostile/stress-repair behavior.

Does dispersion still appear distinct?

Yes, but the evidence is mostly distinctiveness rather than improved alpha strength. Dispersion stress-proxy correlations remained low, with the highest around 0.13 for the neutralized variant. The dispersion anchor remains conceptually and statistically separate from the persistence candidate, but the variants were highly related to the anchor and did not create a stronger family result.

Did refinement improve evidence quality?

For persistence, yes. The core and churn-adjusted variants improved h10 mean IC from 0.0125 to roughly 0.0171-0.0172 and improved h20 mean IC from 0.0059 to roughly 0.0099. The result is still not validation evidence, but it is a better research candidate than the original anchor.

For dispersion, no clear improvement. The original anchor remained the best interpretable candidate. The neutralized variant preserved similar h10 evidence but lower positive-rate quality. Other variants weakened or inverted the effect.

Did any candidate drift toward hostile/stress-repair behavior?

No direct artifact-level drift was observed. No hostile, weak-breadth, participation-repair, liquidity-repair, or ML features were added. Stress-repair proxy correlations were low across the set. Persistence still requires later formula-level review because it uses downtrend rank context, but this refinement did not add hostile/stress-repair machinery.

## SECTION 5 - Refinement Outcome Classification

| Candidate ID | Classification | Rationale |
|---|---|---|
| `rank_stability_after_drawdown_02_churn_adjusted` | refinement success | Strongest h10 result, improved h20 behavior, coherent positive-rate profile, and no stress-proxy drift. |
| `rank_stability_after_drawdown_02_core` | refinement success | Clean simplification with nearly identical strength to churn-adjusted; useful evidence that the signal is not dependent on the full original formula. |
| `rank_stability_after_drawdown_02_anchor` | refinement success | Original candidate remains positive and serves as the research comparison anchor, though not a production or governance candidate. |
| `rank_stability_after_drawdown_02_strict` | refinement inconclusive | Preserves evidence but does not clearly improve on the anchor; useful as a context diagnostic. |
| `rank_stability_after_drawdown_02_smoothed` | diagnostic-only | Smoothing weakens evidence; useful for understanding signal timing, not a better refinement candidate. |
| `dispersion_expansion_transition_04_anchor` | refinement inconclusive | Best dispersion result remains modest and h20-limited; worth validation-design consideration only as a distinct diagnostic candidate. |
| `dispersion_expansion_transition_04_neutralized` | refinement inconclusive | Preserves modest h10 evidence and helps diagnose raw-dispersion exposure, but does not improve conviction. |
| `dispersion_expansion_transition_04_alt_accel` | diagnostic-only | Alternative acceleration construction weakens the signal. |
| `dispersion_expansion_transition_04_smoothed` | diagnostic-only | Smoothing weakens the transition effect. |
| `dispersion_expansion_transition_04_rising_state` | reject | Negative h10/h20 behavior and weak positive-rate profile; rising-state narrowing damaged the signal. |

These are research outcome classifications only. They do not promote, demote, register, or govern any candidate.

## SECTION 6 - Readiness Recommendation

1. Which candidates deserve validation consideration?

Validation-design consideration is justified for:
- `rank_stability_after_drawdown_02_churn_adjusted` / `post_drawdown_persistence_churn_adjusted_20`
- `rank_stability_after_drawdown_02_core` / `post_drawdown_persistence_core_20`
- `rank_stability_after_drawdown_02_anchor` / `post_drawdown_persistence_20`

Limited validation-design consideration may be justified for:
- `dispersion_expansion_transition_04_anchor` / `dispersion_transition_acceleration_20`
- `dispersion_expansion_transition_04_neutralized` / `dispersion_transition_acceleration_neutralized_20`

The dispersion candidates should be considered because of diversification value, not because refinement produced strong h20 evidence.

2. Which candidates require more refinement?

`dispersion_expansion_transition_04_anchor` and `dispersion_expansion_transition_04_neutralized` require either one more very small diagnostic pass or a validation-design memo that explicitly treats them as h5/h10-limited dispersion-transition candidates. Broad parameter expansion is not justified.

`rank_stability_after_drawdown_02_strict` does not require more refinement unless later formula review shows the core/churn-adjusted variants have hidden contamination risk.

3. Which candidates should be rejected?

Reject for this refinement track:
- `dispersion_expansion_transition_04_rising_state`

Do not carry forward as primary candidates:
- `dispersion_expansion_transition_04_alt_accel`
- `dispersion_expansion_transition_04_smoothed`
- `rank_stability_after_drawdown_02_smoothed`

These may remain diagnostic references only.

4. Is alpha-family diversification improving?

Yes, modestly. Persistence evidence improved meaningfully and appears to represent a viable rank-stability research axis. Dispersion still contributes distinctiveness, but the refinement did not yet establish robust dispersion-family alpha. The project is closer to diversification because one non-hostile/stress-repair family now has stronger research evidence, while the second family remains a distinct but fragile candidate axis.

5. What should the next Codex task be?

The next Codex task should be a research-only validation-design memo for the persistence refinement winners and the two remaining dispersion diagnostics. It should specify validation scope, robustness checks, family-distinctness checks, and hostile/stress-repair contamination checks without running validation, changing governance, modifying thresholds, registering production candidates, implementing ML, or promoting/demoting candidates.

## Research Caveat

This was a research-only refinement execution. The results are not validation evidence, not production evidence, and not governance evidence. No candidate is promoted, demoted, registered, or threshold-qualified by this memo.
