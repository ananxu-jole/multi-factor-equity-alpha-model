# Project Underdog - Rank-Coherence Refinement Eligibility and Design v1

## SECTION 1 - Executive Summary

The first rank-coherence IC discovery pass produced useful evidence, but the evidence is candidate-level rather than family-level. The strongest support came from `rank_coherence_regime_independent_02` (`nonhostile_transition_rank_coherence_20`) and `rank_coherence_churn_avoidance_02` (`relative_rank_turnover_resilience_20`). Both candidates showed positive h10/h20 behavior with modest but usable IC IR and positive IC rates, while the broader six-candidate scored batch did not show consistent family-wide strength.

Refinement is justified, but only as a small controlled research program. The family-level averages were weak, including negative mean IC at h10 and h20, so the correct interpretation is not that rank-coherence has already proven itself as a broad alpha family. The correct interpretation is that two rank-coherence threads earned a narrow refinement test to determine whether the signal is durable, distinct, and not merely persistence under another name.

The main risks refinement must avoid are parameter mining, h20-only horizon chasing, accidental recreation of persistence, and hidden contamination from hostile/stress-repair behavior. The refinement batch should therefore be limited to the two eligible candidates, preserve the original economic hypotheses, report all variants, and require redundancy and contamination diagnostics before any later validation consideration.

## SECTION 2 - IC Discovery Review

The strongest horizons were concentrated in the two primary candidates under review:

| candidate_id | signal | strongest evidence |
| --- | --- | --- |
| `rank_coherence_regime_independent_02` | `nonhostile_transition_rank_coherence_20` | Positive h5/h10/h20, strongest mean IC at h5, durable h20 support |
| `rank_coherence_churn_avoidance_02` | `relative_rank_turnover_resilience_20` | Positive all horizons, strongest mean IC at h20 |

`rank_coherence_regime_independent_02` had mean IC of 0.011849 at h5, 0.008151 at h10, and 0.010040 at h20. Its IC IR was strongest at h5 at 0.091804, with h10 at 0.060306 and h20 at 0.075927. Positive IC rate was 0.553106 at h5, 0.520243 at h10, and 0.526860 at h20. This is the cleanest rank-coherence result because it is explicitly framed around non-hostile transition rank coherence rather than post-drawdown persistence.

`rank_coherence_churn_avoidance_02` had mean IC of 0.002049 at h1, 0.005683 at h5, 0.003643 at h10, and 0.011587 at h20. Its h20 IC IR was 0.064884, and its h20 positive IC rate was 0.549587. This candidate has the strongest h20 result in the scored subset, but it also carries the highest persistence-duplication risk because rank-turnover resilience can overlap economically with persistence behavior.

Other scored candidates were weaker. `rank_coherence_reversal_pressure_01` showed useful h1 and h10 evidence, but its h20 mean IC turned slightly negative. `rank_coherence_leadership_stability_02` was weak and adverse at h20. `rank_coherence_concentration_02` and `rank_coherence_reversal_pressure_02` were adverse across important horizons and do not justify refinement.

Family-level consistency was not established. The rank-coherence family summary was slightly negative at h10 and h20, with family mean IC of -0.002087 at h10 and -0.001364 at h20. Positive IC rates were also near or below neutral at h10 and h20. This argues for candidate-level refinement only, not broad family expansion.

The main weaknesses observed were:

- evidence concentrated in two candidates rather than distributed across themes;
- modest IC IR values rather than decisive robustness;
- moderate redundancy between the two eligible candidates, with maximum approved-subset correlation around 0.52049;
- unresolved persistence overlap risk, especially for churn avoidance;
- no validation-stage state attribution or stress-repair contamination review yet;
- several rank-coherence themes produced adverse or diagnostic-only behavior.

## SECTION 3 - Candidate Eligibility Assessment

| candidate_id | signal | classification | rationale |
| --- | --- | --- | --- |
| `rank_coherence_regime_independent_02` | `nonhostile_transition_rank_coherence_20` | eligible for refinement design | Strongest all-around candidate. Positive h5/h10/h20 behavior, best IC IR profile, and cleanest economic separation from persistence and hostile/stress-repair framing. |
| `rank_coherence_churn_avoidance_02` | `relative_rank_turnover_resilience_20` | eligible for refinement design | Strongest h20 mean IC and positive all-horizon profile. Eligible only with strict controls against persistence duplication. |
| `rank_coherence_reversal_pressure_01` | `rank_shock_reversion_pressure_5_20` | watchlist only | Useful h1/h10 behavior but weak h20 durability. Not ready for refinement because the effect appears horizon-fragile. |
| `rank_coherence_leadership_stability_02` | `cross_window_rank_agreement_10_20` | diagnostic only | Some h5 support but negative h10/h20 behavior. Useful for understanding failed leadership-stability framing, not for refinement. |
| `rank_coherence_concentration_02` | `leadership_broadening_entry_20` | reject | Broadly adverse behavior, including negative h1/h5/h10 results and weak h20 support. |
| `rank_coherence_reversal_pressure_02` | `rank_acceleration_disagreement_5_20` | reject | Adverse h5/h10/h20 behavior and weak positive IC rates. No refinement case. |

No held-back, unscored candidates should enter refinement through this review. They were not part of the approved IC scoring subset and should remain outside the refinement program.

## SECTION 4 - Family Distinctiveness Assessment

Rank-coherence appears partially distinct from persistence, but the distinction is not yet fully proven. The regime-independent candidate is the better diversification thread because it focuses on non-hostile transition rank agreement rather than post-drawdown persistence. The churn-avoidance candidate is more ambiguous: it may represent rank turnover resilience, but it could also drift into a persistence-like effect if refinement rewards stable winners across h20 without preserving the rank-coherence mechanism.

Separation from hostile/stress-repair appears clean at the discovery-design and metadata levels. The rank-coherence candidates do not use explicit hostile, repair, participation, or stress-state inputs. However, formal state attribution and stress-repair contamination diagnostics have not yet been run, so refinement must include explicit checks before any validation-review claim.

Separation from dispersion is stronger. These candidates are based on cross-sectional rank structure, rank agreement, churn, and transition coherence rather than dispersion expansion or compression. Refinement should still prohibit dispersion-derived ingredients so the family boundary remains clean.

Rank-coherence remains a legitimate diversification frontier, but only in a narrow sense. The current evidence supports two promising candidate threads, not a mature family. A disciplined refinement pass is warranted to determine whether the phenomenon is genuine or whether the discovery pass found two isolated, partially redundant effects.

## SECTION 5 - Refinement Scope Design

### Eligible Candidate A: `rank_coherence_regime_independent_02`

Representative signal: `nonhostile_transition_rank_coherence_20`

Refinement objective:

Confirm whether non-hostile transition rank coherence has durable h10/h20 predictive value without depending on hostile/stress-repair states, persistence inputs, or a single favorable horizon.

Allowable modifications:

- small reweighting of existing rank-coherence components already implied by the candidate;
- one stricter non-hostile transition definition using existing non-hostile gating logic;
- one smoother rank-agreement variant using the same rank windows and source inputs;
- optional diagnostic neutralization against churn-avoidance overlap, if implemented as a fixed pre-declared diagnostic rather than a fitted optimizer.

Prohibited modifications:

- adding post-drawdown, drawdown-recovery, stress, repair, participation, or hostile-state inputs;
- adding dispersion, volatility compression, or volatility expansion ingredients;
- adding new horizons beyond the approved discovery horizons;
- optimizing directly to the best observed h5 or h20 result;
- changing thresholds, governance rules, validation standards, or production registries;
- introducing ML, fitted ensembles, or learned weights.

Candidate count cap:

`rank_coherence_regime_independent_02` may contribute the original anchor plus at most two refinement variants.

Expected outputs:

- fixed candidate inventory with anchor and variants;
- candidate panel artifacts under a research-only refinement artifact tree;
- candidate-level h1/h5/h10/h20 IC scoring;
- horizon, coverage, and positive IC rate diagnostics;
- redundancy context versus rank-coherence, persistence, hostile/stress-repair, and dispersion references;
- refinement review note with no validation or governance action.

### Eligible Candidate B: `rank_coherence_churn_avoidance_02`

Representative signal: `relative_rank_turnover_resilience_20`

Refinement objective:

Test whether rank-turnover resilience is a true rank-coherence signal rather than a persistence duplicate, while preserving the useful h20 behavior and improving confidence in h10/h20 consistency.

Allowable modifications:

- one slight rank-turnover measurement adjustment using the same rank universe and source inputs;
- one conservative churn-penalty strength adjustment, pre-declared and symmetric around the existing design;
- one diagnostic variant that reduces direct overlap with `rank_coherence_regime_independent_02`;
- fixed h10/h20 reporting with h5 treated as supporting context only.

Prohibited modifications:

- adding post-drawdown persistence, recovery persistence, or drawdown-conditioned inputs;
- adding hostile, stress-repair, participation repair, or regime-repair state variables;
- adding dispersion or volatility-compression ingredients;
- expanding the horizon set to search for a better fit;
- adding more churn windows after seeing IC results;
- using ML, fitted weights, or production registration paths.

Candidate count cap:

`rank_coherence_churn_avoidance_02` may contribute the original anchor plus at most two refinement variants.

Expected outputs:

- fixed candidate inventory with anchor and variants;
- research-only panels for each candidate;
- refinement candidate score summary;
- horizon behavior table;
- redundancy review with special attention to persistence-lineage candidates;
- contamination review against hostile/stress-repair behavior;
- final refinement execution review with no promotion, demotion, or validation execution.

Explicit broad expansion prohibition:

No other rank-coherence themes should be refined in this pass. No held-back candidates should be reintroduced. No new themes, new horizon families, new source datasets, or additional candidate families should be added. The maximum refinement batch is six scored candidates total: two anchors plus four variants.

## SECTION 6 - Anti-Optimization Controls

The refinement program should use the following safeguards:

- Maximum refinement scope: two eligible candidates, each with the original anchor plus at most two variants, for a maximum of six scored candidates.
- Fixed horizons: h1, h5, h10, and h20 may be reported; h10/h20 must remain the primary interpretation horizons. h5 may support `rank_coherence_regime_independent_02` but must not become the sole success basis.
- No candidate expansion after results: the refinement inventory must be frozen before scoring.
- No horizon chasing: variants may not be selected or interpreted solely because they improve the best discovery horizon.
- No parameter mining: allowable changes must be pre-declared and economically motivated, with all variants reported.
- Anchor comparison required: every variant must be compared against its original discovery anchor.
- Family contamination controls: variants must not add persistence, hostile/stress-repair, participation repair, dispersion, or volatility-compression ingredients.
- Persistence duplication controls: churn-avoidance variants must be reviewed against persistence lineage artifacts, especially `post_drawdown_persistence_churn_adjusted_20` and related post-drawdown persistence candidates.
- Redundancy controls: refinement outputs must include pairwise redundancy within the refined batch and context against prior persistence, hostile/stress-repair, and dispersion research artifacts where available.
- Review checkpoints: formula inventory review before execution, panel/redundancy review after generation, IC refinement review after scoring, and a separate validation eligibility audit before any validation design.

Prohibited modifications include governance edits, threshold edits, validation execution, refinement beyond the approved variants, production registration, candidate promotion/demotion, and ML integration.

## SECTION 7 - Success Criteria

Refinement should not be judged by raw IC alone. A candidate may justify later validation-review consideration only if it demonstrates robustness, consistency, and distinctiveness.

Continuation toward validation-review eligibility would require:

- h10/h20 behavior that remains positive and economically interpretable versus the original anchor;
- IC IR and positive IC rate that are maintained or improved without sacrificing coverage;
- no material collapse outside the single best discovery horizon;
- stable enough active coverage to support a real research candidate;
- redundancy that remains moderate or lower versus persistence-lineage candidates and existing hostile/stress-repair references;
- no evidence that the refined signal is merely a stress-repair, participation-repair, or post-drawdown persistence proxy;
- at least one refinement variant that improves evidence quality while preserving the original rank-coherence hypothesis.

Additional refinement would be justified only if results are directionally positive but unresolved in a narrow, diagnosable way, such as modest h10 weakness with stable h20 behavior and clean redundancy. It should not be used to rescue adverse or highly redundant results.

Diagnostic-only classification would be appropriate if the candidates remain economically interesting but fail to improve robustness, show weak positive IC rates, or remain too redundant with persistence to support independent validation.

Rejection would be appropriate if h10/h20 results deteriorate, positive IC rates fall toward noise, redundancy with persistence or stress-repair becomes high, or refinement gains are isolated to one mined parameter choice.

## SECTION 8 - Recommended Refinement Batch

Recommended candidates entering refinement:

| candidate_id | representative signal | refinement status |
| --- | --- | --- |
| `rank_coherence_regime_independent_02` | `nonhostile_transition_rank_coherence_20` | enter controlled refinement |
| `rank_coherence_churn_avoidance_02` | `relative_rank_turnover_resilience_20` | enter controlled refinement with persistence-duplication controls |

Maximum number of variants:

- two original anchors;
- at most two variants for `rank_coherence_regime_independent_02`;
- at most two variants for `rank_coherence_churn_avoidance_02`;
- maximum six scored candidates total.

Expected artifact tree:

`artifacts/research/rank_coherence_refinement_v1/`

Expected artifacts:

- `candidate_inventory.csv`;
- `refinement_candidate_scores.csv`;
- `candidate_horizon_ic_scores.csv`;
- `daily_ic_by_candidate_horizon.csv`;
- `family_theme_summary.csv`;
- `redundancy_context.csv`;
- `contamination_review.csv`;
- `manifest.json`.

Expected review checkpoints:

- pre-execution inventory and guardrail confirmation;
- panel generation and redundancy review;
- research-only refinement IC review;
- separate validation eligibility audit if, and only if, refinement produces robust and distinct evidence.

This batch should remain intentionally small. The purpose is to decide whether rank-coherence has a credible refinement-worthy core, not to search for a better member of a large parameter grid.

## SECTION 9 - Final Recommendation

1. Did rank-coherence produce useful evidence?

Yes. Rank-coherence produced useful candidate-level evidence, especially in `rank_coherence_regime_independent_02` and `rank_coherence_churn_avoidance_02`. It did not yet produce broad family-level proof.

2. Which candidate is strongest?

`rank_coherence_regime_independent_02` is the strongest overall candidate because it combines positive h5/h10/h20 behavior with the cleanest economic separation from persistence and hostile/stress-repair behavior. `rank_coherence_churn_avoidance_02` has the strongest h20 mean IC but higher persistence-duplication risk.

3. Is refinement justified?

Yes, but only a narrow controlled refinement is justified. The approved scope should be two eligible candidates, their original anchors, and at most four total variants.

4. How many candidates should enter refinement?

Two candidates should enter refinement: `rank_coherence_regime_independent_02` and `rank_coherence_churn_avoidance_02`. The maximum scored refinement batch should be six candidates total including anchors.

5. Does rank-coherence remain a viable new family?

Yes. Rank-coherence remains viable as a diversification frontier, but it is still an emerging candidate-level research thread rather than an established alpha family.

6. What should the next Codex task be?

The next task should be **Project Underdog - Rank-Coherence Refinement Execution v1**: execute only the approved two-candidate, six-candidate-maximum research refinement batch, produce refinement artifacts under `artifacts/research/rank_coherence_refinement_v1/`, and create a refinement execution review note. The task should continue to prohibit validation, governance mutation, threshold changes, production registration, ML, and candidate promotion/demotion.
