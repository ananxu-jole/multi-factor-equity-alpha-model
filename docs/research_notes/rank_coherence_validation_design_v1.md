# Project Underdog - Rank-Coherence Validation Design v1

Date: 2026-06-19

Project: Project Underdog

Primary candidate: `rank_coherence_churn_avoidance_02_overlap_adjusted`

Representative signal: `relative_rank_turnover_resilience_overlap_adjusted_20`

Family: Rank-Coherence

Status entering this design: `READY FOR VALIDATION REVIEW` per `docs/research_notes/rank_coherence_validation_eligibility_audit_v1.md`

Scope: design-only formal validation package. No validation, refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

`rank_coherence_churn_avoidance_02_overlap_adjusted` reached validation-review eligibility as the strongest refined rank-coherence candidate. Its lineage begins with `rank_coherence_churn_avoidance_02` / `relative_rank_turnover_resilience_20`, the strongest h20 candidate from the rank-coherence IC discovery pass. The original discovery anchor had h20 mean IC 0.011587, h20 IC IR 0.064884, and h20 positive IC rate 0.549587.

The approved refinement program was deliberately small: two eligible parent candidates, two anchors, four variants, and a maximum of six scored candidates. The refined successor, `relative_rank_turnover_resilience_overlap_adjusted_20`, improved both primary horizons:

- h10 mean IC improved from 0.003643 to 0.004783.
- h10 IC IR improved from 0.019919 to 0.026354.
- h10 positive IC rate improved from 0.522267 to 0.532389.
- h20 mean IC improved from 0.011587 to 0.012843.
- h20 IC IR improved from 0.064884 to 0.072299.
- h20 positive IC rate improved from 0.549587 to 0.561983.

Validation-readiness conclusion: the candidate is ready for formal validation review design, not validation success. The rationale for validation design is that the candidate improved within the approved refinement space, preserved the rank-turnover-resilience hypothesis, reduced persistence correlation versus the anchor, and remained distinct enough from dispersion and hostile/stress-repair references to merit a frozen validation test.

The unresolved risks are still material. Evidence is candidate-level rather than family-level, the candidate remains close to its anchor, the effect is h20-led, and stress-proxy correlation is moderate. Validation should therefore test robustness, distinctiveness, and concentration rather than continue tuning.

## SECTION 2 - Candidate Freeze Definition

Frozen candidate:

- `candidate_id`: `rank_coherence_churn_avoidance_02_overlap_adjusted`
- `hypothesis`: `relative_rank_turnover_resilience_overlap_adjusted_20`
- `family`: `rank_coherence`
- `theme`: Rank Churn Avoidance
- `declared horizon`: h10-h20
- `variant role`: regime-independent overlap diagnostic
- `parent candidate`: `rank_coherence_churn_avoidance_02`
- `parent signal`: `relative_rank_turnover_resilience_20`
- `artifact source`: `artifacts/research/rank_coherence_refinement_v1/`

Feature structure to freeze:

The candidate should be validated exactly as produced by the refinement execution. Its economic structure is rank-turnover resilience adjusted to reduce overlap with the regime-independent rank-coherence anchor. It should remain a rank-coherence signal using rank-churn and rank-structure behavior, not a persistence, stress-repair, dispersion, volatility, liquidity, participation, or ML signal.

Horizon focus:

- Report h1, h5, h10, and h20 for continuity with discovery and refinement.
- Treat h10 and h20 as the primary validation horizons.
- Treat h1 and h5 as supporting diagnostics and horizon-concentration checks.

Refinement lineage:

`rank_coherence_churn_avoidance_02` -> `relative_rank_turnover_resilience_20` -> approved narrow refinement -> `rank_coherence_churn_avoidance_02_overlap_adjusted` / `relative_rank_turnover_resilience_overlap_adjusted_20`

Freeze confirmations:

- No additional variants.
- No additional refinement.
- No formula changes.
- No new horizons.
- No new feature inputs.
- No post-validation candidate selection.
- No governance or threshold changes.
- No production registration.
- No ML.
- No candidate promotion or demotion.

## SECTION 3 - Validation Scope

The validation package should evaluate the frozen candidate under the existing Project Underdog validation conventions. It should create a research-only validation namespace and must not alter validation rules, schemas, thresholds, governance gates, or production wiring.

Candidate evaluation structure:

- Primary validation candidate: `rank_coherence_churn_avoidance_02_overlap_adjusted`.
- Required lineage controls: `rank_coherence_churn_avoidance_02_anchor` and `rank_coherence_churn_avoidance_02_penalized`, for interpretation only.
- Required rank-coherence context controls: `rank_coherence_regime_independent_02_anchor`, `rank_coherence_regime_independent_02_strict`, and `rank_coherence_regime_independent_02_smoothed`, for sibling and family-context review only.
- No variant reselection.
- No tuning based on validation outputs.

Horizons:

- h1
- h5
- h10
- h20

Primary emphasis:

- h10
- h20

Core metrics:

- mean IC;
- IC standard deviation;
- IC IR;
- positive IC rate;
- valid IC date count;
- daily IC distribution;
- horizon-by-horizon degradation profile.

Coverage diagnostics:

- active date count;
- active date ratio;
- mean active tickers;
- minimum and maximum active tickers;
- missingness and finite-value coverage;
- date/ticker alignment versus close-price data;
- activation persistence and activation gaps where supported by existing utilities.

Concentration diagnostics:

- window-level contribution to aggregate IC;
- largest positive-window share;
- recent-window behavior;
- concentration by active date cluster;
- concentration by ticker coverage;
- sensitivity to sparse activation windows.

Robustness diagnostics:

- multi-horizon IC profile;
- WFV-style aggregate summary;
- WFV window diagnostics;
- sign consistency across windows;
- degradation versus refinement result;
- state/regime attribution;
- redundancy and contamination review against reference families.

## SECTION 4 - Walk-Forward Validation Design

Validation should reuse the existing Project Underdog validation conventions used for prior Track B and persistence-family candidates. This design does not alter the walk-forward methodology, thresholds, or governance standards.

Walk-forward framework:

- Use the existing WFV-style validation windowing convention.
- Evaluate the frozen signal panel against forward returns at h1, h5, h10, and h20.
- Treat h10/h20 windows as primary.
- Report all windows, not only aggregate results.
- Include valid date counts and active coverage per window.

Train/test review process:

- Use fixed train/test or WFV-style splits from the existing validation framework.
- Do not use training windows to adjust the signal.
- Do not select among variants using validation results.
- Use lineage controls only as diagnostics, not as replacement candidates.

Sign consistency review:

- Report mean test IC by window.
- Report positive IC rate by window.
- Count positive, negative, and near-flat windows.
- Flag any horizon where aggregate positive IC is driven by too few windows.

Stability review:

- Compare h10 and h20 stability across windows.
- Review whether h20 strength survives outside the strongest refinement-era window.
- Review whether h10 remains supportive or collapses during validation.
- Report recent-window behavior separately.

Degradation review:

- Compare validation metrics against refinement metrics for h10 and h20.
- Treat moderate degradation as expected; classify severity using existing validation standards.
- Flag material degradation if h10/h20 mean IC, IC IR, or positive IC rate weaken enough to undermine the original refinement thesis.
- Do not compensate for degradation by changing horizons or formulas.

## SECTION 5 - Distinctiveness Review Requirements

Validation must determine whether the candidate is truly rank-coherence behavior rather than a renamed persistence, stress-repair, dispersion, or sibling rank-coherence artifact.

Persistence contamination:

Required comparisons:

- `post_drawdown_persistence_20`
- `post_drawdown_persistence_churn_adjusted_20`
- `post_drawdown_persistence_core_20`
- `post_drawdown_persistence_smoothed_20`
- `post_drawdown_persistence_strict_20`
- any current persistence-family validation or active research inventory references available to the validation framework

Required outputs:

- value correlation;
- rank correlation;
- activation overlap where available;
- horizon-specific IC comparison;
- top persistence peer;
- interpretation of whether the candidate is rank-turnover resilience or delayed persistence.

Hostile/stress-repair contamination:

Required comparisons:

- failed-breakout and hostile-reversal references;
- weak-breadth or participation-repair references where available;
- liquidity-repair and stress-stabilization references where available;
- existing validated or conditional hostile/stress-repair inventory references.

Required outputs:

- value and rank correlation;
- state/regime attribution;
- stress-state conditional IC;
- activation overlap with hostile/stress-repair references;
- top stress-repair peer;
- conclusion on whether positive IC is concentrated in stress-repair states.

Dispersion contamination:

Required comparisons:

- `dispersion_transition_acceleration_20`;
- `dispersion_transition_acceleration_smoothed_20`;
- `dispersion_transition_acceleration_neutralized_20`;
- relevant dispersion discovery/refinement references available to the validation framework.

Required outputs:

- value and rank correlation;
- top dispersion peer;
- assessment of whether the candidate is independent from dispersion expansion/transition behavior.

Sibling rank-coherence contamination:

Required comparisons:

- `relative_rank_turnover_resilience_20`;
- `relative_rank_turnover_resilience_penalized_20`;
- `nonhostile_transition_rank_coherence_20`;
- `nonhostile_transition_rank_coherence_strict_20`;
- `nonhostile_transition_rank_coherence_smoothed_20`;
- scored rank-coherence discovery candidates where available.

Required outputs:

- sibling redundancy table;
- lineage-control comparison;
- determination of whether the refined candidate is a cleaner successor or merely a duplicate;
- family-breadth interpretation that does not count close siblings as independent evidence.

Interpretation standards:

- Low contamination plus stable validation evidence supports diversification value.
- High persistence or stress-repair overlap weakens any validation pass interpretation.
- High sibling overlap is acceptable for lineage continuity but cannot be used as family-level proof.
- Distinctiveness must be judged alongside IC robustness, not separately from it.

## SECTION 6 - Risk Review Requirements

Overfitting risk:

- Compare validation results to refinement results.
- Review whether improvement survives out-of-sample or WFV-style windows.
- Report whether the validation result appears weaker than expected for a sample-tuned candidate.

Refinement leakage risk:

- Confirm the validation package uses the frozen refined candidate only.
- Confirm no validation output is used to adjust the candidate.
- Include lineage controls without allowing post-hoc reselection.

Horizon concentration risk:

- Treat h10/h20 as primary horizons.
- Report h1/h5 but do not reinterpret the candidate as a short-horizon signal.
- Flag a result that passes only at h20 while h10 is weak or unstable.
- Compare h20 evidence across windows to detect one-window dominance.

False diversification risk:

- Require redundancy and state-attribution review against persistence, hostile/stress-repair, and dispersion references.
- Require explicit economic interpretation after validation results.
- Treat correlation, activation overlap, or state dependence as material risks even if aggregate IC is positive.

Family concentration risk:

- Identify whether validation evidence is one-candidate-only.
- Avoid treating lineage controls or close sibling variants as independent family breadth.
- Require the validation note to distinguish candidate validation from rank-coherence family validation.

## SECTION 7 - Validation Success and Failure Framework

This design does not modify governance standards, validation thresholds, schemas, or candidate-status rules. It defines interpretation language to be applied using existing Project Underdog standards.

Pass interpretation:

A validation pass would mean the frozen candidate retains positive, economically coherent h10/h20 evidence under the standard validation framework, with supportive WFV behavior, acceptable coverage, no unacceptable window concentration, and no disqualifying persistence, hostile/stress-repair, dispersion, or active-inventory redundancy. A pass would support further research review. It would not by itself imply production registration, governance approval, threshold change, or candidate promotion.

Conditional interpretation:

A conditional validation candidate outcome would apply if aggregate h10/h20 evidence remains positive but one or more risks remain unresolved, such as window concentration, recent-window weakness, moderate stress-repair overlap, h20-only strength, active coverage concerns, or incomplete distinctiveness. Conditional status should trigger a review decision, not tuning inside validation.

Fail interpretation:

A validation failure would apply if h10/h20 evidence weakens materially, turns unstable across WFV windows, is dominated by one window, shows poor positive IC behavior under existing standards, has inadequate active coverage, or appears to be a renamed persistence/stress-repair/dispersion signal. Failure should prevent validation advancement and should not route the candidate to production, governance, ML, portfolio, or registration workflows.

Diagnostic-only interpretation:

If the candidate remains economically interesting but fails robustness or distinctiveness standards, it should be preserved as diagnostic evidence for rank-coherence research only. Diagnostic-only outcome should not lead to additional refinement unless a later review identifies a narrow, non-mining research question.

## SECTION 8 - Artifact Plan

Expected artifact namespace:

`artifacts/research/rank_coherence_validation_v1/`

Required outputs:

- `validation_candidate_inventory.csv`: frozen candidate and fixed lineage/control references.
- `validation_summary.csv`: aggregate validation classification metrics and interpretation fields.
- `horizon_validation_metrics.csv`: h1/h5/h10/h20 mean IC, IC IR, positive IC rate, and valid date counts.
- `daily_ic_by_candidate_horizon.csv`: daily IC rows for auditability.
- `walk_forward_diagnostics.csv`: WFV-style window results and sign-consistency diagnostics.
- `walk_forward_summary.csv`: aggregate WFV review by horizon.
- `coverage_review.csv`: active date, ticker, missingness, and finite-value diagnostics.
- `concentration_review.csv`: window, date, and coverage concentration diagnostics.
- `state_attribution.csv`: regime/state conditional IC and activation diagnostics.
- `contamination_review.csv`: persistence, hostile/stress-repair, dispersion, and sibling rank-coherence comparisons.
- `redundancy_review.csv`: value/rank correlations versus reference inventory.
- `lineage_control_comparison.csv`: comparison versus anchor and sibling controls.
- `manifest.json`: research-only execution manifest and guardrail confirmations.

Expected review note:

`docs/research_notes/rank_coherence_validation_execution_v1.md`

The execution note should report validation completion status, core validation results, robustness findings, distinctiveness and contamination findings, validation outcome classification, and recommendations. It must not register the candidate, modify governance, change thresholds, implement ML, promote/demote any candidate, or make production decisions.

## SECTION 9 - Governance Boundaries

This validation design explicitly preserves the following boundaries:

- Validation only.
- No refinement.
- No additional variants.
- No formula changes.
- No governance mutation.
- No threshold changes.
- No production registration.
- No ML.
- No candidate promotion or demotion.
- No portfolio construction change.
- No survivor-freeze or inventory mutation.

The validation package may produce a research classification such as validation pass, conditional validation candidate, diagnostic-only, or validation failure under existing standards. That classification is a research review output only unless a separate governance task later authorizes an action.

## SECTION 10 - Final Recommendation

1. Is the candidate appropriately frozen?

Yes. `rank_coherence_churn_avoidance_02_overlap_adjusted` should enter validation as the exact refined signal `relative_rank_turnover_resilience_overlap_adjusted_20`, with no additional variants, no additional refinement, no formula changes, and no horizon expansion.

2. Is the lineage sufficiently clean?

Yes. The lineage is clean and auditable from `rank_coherence_churn_avoidance_02` through the approved refinement design and research-only refinement execution. The candidate remains a close sibling of its anchor, so validation must treat it as one refined lineage rather than independent family breadth.

3. What are the key risks validation must test?

Validation must test h20 horizon concentration, h10 durability, WFV stability, recent-window behavior, active coverage, window concentration, persistence contamination, stress-repair contamination, dispersion overlap, sibling redundancy, overfitting, refinement leakage, and false diversification risk.

4. What evidence would justify a pass?

A pass would require positive and economically coherent h10/h20 validation evidence, supportive WFV sign consistency, acceptable degradation versus refinement, adequate active coverage, no excessive window concentration, and no disqualifying contamination from persistence, hostile/stress-repair, dispersion, or sibling rank-coherence references under existing Project Underdog standards.

5. What should the next Codex task be?

The next Codex task should be **Project Underdog - Rank-Coherence Validation Execution v1**. It should execute only the validation package defined here for the frozen candidate `rank_coherence_churn_avoidance_02_overlap_adjusted`, produce artifacts under `artifacts/research/rank_coherence_validation_v1/`, and create `docs/research_notes/rank_coherence_validation_execution_v1.md`. It should not run refinement, modify governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.

## Design Caveat

This document designs a validation package only. It does not execute validation, establish validation success, authorize production registration, alter governance, change thresholds, implement ML, or promote/demote any candidate.
