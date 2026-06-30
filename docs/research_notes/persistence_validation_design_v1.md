# Persistence Validation Design v1

Date: 2026-06-18

Project: Project Underdog

Primary candidate: `post_drawdown_persistence_churn_adjusted_20`

Family: Persistence

Status entering this design: `READY FOR VALIDATION REVIEW` per `docs/research_notes/persistence_validation_eligibility_audit_v1.md`

Scope: design-only formal validation program. No validation, refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.

## SECTION 1 - Executive Summary

`post_drawdown_persistence_churn_adjusted_20` reached validation-review eligibility because it improved the strongest diversification discovery candidate while preserving the approved persistence-family thesis. The original candidate, `post_drawdown_persistence_20`, showed the cleanest IC discovery profile in the diversification subset: h10 mean IC 0.0125, h10 IC IR 0.1208, h10 positive IC rate 0.5951, and low approved-subset redundancy. The refinement successor improved the h10 profile to mean IC 0.0172, IC IR 0.1734, and positive IC rate 0.6012, while h20 mean IC improved from 0.0059 to 0.0099.

Validation consideration is supported by four pieces of evidence:
- The improvement was meaningful at h10 and h20.
- The nearby `post_drawdown_persistence_core_20` control produced nearly identical h10/h20 evidence.
- Stress-proxy redundancy remained low, with maximum stress-proxy absolute correlation of 0.0633.
- The economic story remained rank persistence after drawdown, not participation repair, liquidity repair, weak-breadth recovery, or ML-driven pattern selection.

The unresolved risks are still material. The refinement evidence is in-sample to the discovery/refinement workflow, the successful variants are highly correlated with each other, h20 remains weaker than h5/h10, and the broader persistence family is not yet established by multiple independent candidates. Formal validation should therefore test robustness and distinctiveness, not continue tuning.

## SECTION 2 - Candidate Lineage Review

The lineage begins with `rank_stability_after_drawdown_02` / `post_drawdown_persistence_20`, a Rank Stability After Drawdown candidate from the alpha-family diversification discovery batch. It was selected for refinement because it was the strongest individual candidate in the 8-candidate IC discovery subset and combined positive h5/h10 evidence with low redundancy.

Original discovery profile:
- h1 mean IC: 0.0047
- h5 mean IC: 0.0137
- h10 mean IC: 0.0125
- h20 mean IC: 0.0059
- h10 IC IR: 0.1208
- h10 positive IC rate: 0.5951
- max approved-subset absolute correlation: 0.1815

The approved refinement design allowed a small persistence variant set only. It permitted small changes to rank-persistence definition, rank-churn treatment, light smoothing, and drawdown-context strictness while keeping family, theme, directional thesis, and h10-h20 research orientation fixed. Broad parameter search was explicitly prohibited.

The refinement successor, `post_drawdown_persistence_churn_adjusted_20`, penalized post-drawdown rank churn while preserving the core thesis that stable/improving ranks after drawdown identify more durable securities.

Refinement successor profile:
- h1 mean IC: 0.0063
- h5 mean IC: 0.0184
- h10 mean IC: 0.0172
- h20 mean IC: 0.0099
- h10 IC IR: 0.1734
- h10 positive IC rate: 0.6012
- h20 positive IC rate: 0.5372

Major metric changes versus original anchor:
- h10 mean IC improved by roughly 0.0047.
- h20 mean IC improved by roughly 0.0040.
- h10 IC IR improved from 0.1208 to 0.1734.
- h10 positive IC rate remained strong, moving from 0.5951 to 0.6012.

Diversification significance:
- The candidate is the first persistence-family candidate to earn formal validation-review eligibility.
- It strengthens the persistence thread as a candidate lineage.
- It does not yet prove a broad persistence alpha family because the successful refinement variants are close siblings and the original broader persistence family was mixed.

## SECTION 3 - Validation Objectives

Primary validation objective:

Determine whether `post_drawdown_persistence_churn_adjusted_20` retains robust, economically interpretable h10/h20 IC evidence under Project Underdog's existing validation framework when parameters are frozen and no additional refinement is allowed.

Secondary objectives:
- Test walk-forward stability across fixed validation windows.
- Measure active coverage, ticker/date concentration, and window concentration.
- Confirm that h10/h20 evidence is not driven by one market episode.
- Test whether the candidate remains distinct from existing active candidates, hostile/stress-repair signals, reversal baselines, momentum baselines, and its own parent lineage.
- Compare the primary candidate to fixed lineage controls without selecting a new winner.

Diversification objectives:
- Determine whether persistence adds a genuinely new alpha-family axis.
- Confirm the signal is rank-persistence-driven rather than stress-repair-driven.
- Assess whether persistence diversifies away from participation/liquidity/breadth repair and dispersion-transition research threads.

What validation is attempting to prove:
- The candidate has repeatable h10/h20 evidence after freezing the refined formulation.
- The effect survives walk-forward review and is not dominated by a single window.
- The signal remains economically tied to post-drawdown rank persistence.
- The candidate has low enough redundancy to contribute diversification value.

What validation is attempting to falsify:
- That the refinement improvement was sample-specific noise.
- That the candidate is merely a renamed hostile/stress-repair signal.
- That the apparent edge is concentrated in one date regime, one active subset, or one refinement artifact.
- That h10/h20 evidence disappears when evaluated under the existing validation framework.

## SECTION 4 - Validation Methodology

Validation should use the existing Project Underdog research-only validation pattern used for prior Track B candidates. The program should create an isolated validation artifact namespace and a fixed validation registry. It must not alter validation rules, governance gates, schemas, thresholds, or production wiring.

Datasets:
- Frozen signal panel for `post_drawdown_persistence_churn_adjusted_20` from `artifacts/research/alpha_family_diversification_refinement_v1/`.
- Fixed lineage-control panels for `post_drawdown_persistence_20` and `post_drawdown_persistence_core_20`.
- Existing close-price panel used by the scoring stack.
- Existing Project Underdog state/regime inputs used by prior validation runners, where available.
- Existing baseline/reference panels for active candidates, hostile/stress-repair candidates, reversal baselines, momentum baselines, dispersion candidates, and discovery/refinement peers.

Candidate evaluation structure:
- Primary validation candidate: `post_drawdown_persistence_churn_adjusted_20`.
- Lineage controls only: `post_drawdown_persistence_20` and `post_drawdown_persistence_core_20`.
- No new variants.
- No parameter tuning.
- No re-selection among controls.

Horizons:
- Score h1, h5, h10, and h20 for continuity with discovery/refinement.
- Treat h10 and h20 as the primary validation horizons.
- Treat h5 as a horizon-concentration diagnostic, not a basis for changing the candidate objective.

Robustness tests:
- Multi-horizon rank IC summary.
- Daily IC distribution and positive IC rate.
- WFV-style persistence and sign consistency using existing window conventions.
- WFV window detail with start date, end date, mean test IC, test IC IR, positive IC rate, and valid IC dates.
- Window-concentration diagnostics, including largest positive-window share and recent-window behavior.
- Active coverage diagnostics, including active date ratio, mean active coverage, minimum active-window dates, and activation transitions if applicable.
- Structural quality diagnostics, including missingness, finite value share, date coverage, signal distribution, and turnover proxy.
- Regime/state attribution using existing state definitions.
- Redundancy and orthogonality checks versus the full current research inventory and known hostile/stress-repair references.

Walk-forward requirements:
- Use the existing WFV-style validation windowing convention from prior Track B validation runners.
- Report all windows, not only aggregate WFV summary.
- Require enough valid IC dates per window to support interpretation under existing standards.
- Flag any one-window dominance or weak recent-window positive IC rate.

Required outputs:
- `validation_registry.csv`
- `validation_summary.csv`
- `multi_horizon_scoring.csv`
- `daily_ic_by_candidate_horizon.csv`
- `wfv_style_summary.csv`
- `wfv_window_diagnostics.csv`
- `window_concentration_diagnostics.csv`
- `structural_quality_summary.csv`
- `active_coverage_summary.csv`
- `regime_state_attribution.csv`
- `orthogonality_redundancy_audit.csv`
- `orthogonality_summary.csv`
- `lineage_control_comparison.csv`
- `manifest.json`
- A research note summarizing validation results and classification.

Expected artifact namespace:
- `artifacts/research/persistence_validation_v1/`

## SECTION 5 - Anti-Leakage Controls

Refinement leakage controls:
- Freeze `post_drawdown_persistence_churn_adjusted_20` exactly as produced by the refinement execution.
- Include `post_drawdown_persistence_20` and `post_drawdown_persistence_core_20` only as lineage controls.
- Do not use validation results to choose between variants.
- Do not create any new variants, filters, smoothing choices, thresholds, horizons, or activation rules.

Horizon-chasing controls:
- Pre-declare h10/h20 as primary validation horizons.
- Report h1/h5/h10/h20, but do not reinterpret the candidate as an h5 signal if h5 is strongest.
- Treat h20 weakness as a validation risk, not as a prompt for further tuning.

Overfitting controls:
- Use fixed WFV-style windows and report every window.
- Require window concentration diagnostics.
- Require recent-window diagnostics.
- Report active coverage and concentration even if aggregate IC is positive.

False-diversification controls:
- Compare against existing active candidates and known hostile/stress-repair signals.
- Compare against discovery/refinement dispersion candidates to confirm cross-family distinction.
- Report whether the candidate's strongest state attribution is dominated by stress-repair states.
- Treat high overlap with hostile/stress-repair references as a validation risk even if IC is positive.

Hidden stress-repair contamination diagnostics:
- Correlation and rank-correlation against failed-breakout, weak-breadth, participation/liquidity repair, hostile-transition, and stress-stabilization references.
- State attribution in drawdown, panic/liquidity stress, weak breadth, recovery, volatility spike, high dispersion, and neutral/normal regimes where existing definitions support them.
- Conditional IC comparison between post-drawdown rank-persistence states and broader stress-repair states.
- Activation overlap with hostile/stress-repair references.
- Formula lineage review confirming no production stress-repair features were added during refinement.

## SECTION 6 - Success and Failure Criteria

These criteria should use existing governance and validation standards wherever available. This design does not change any threshold, gate, schema, or promotion rule.

### A. Validation Pass

Evidence required:
- Primary h10/h20 IC remains positive and economically coherent.
- WFV-style persistence and sign consistency satisfy existing validation standards.
- Window diagnostics do not show unacceptable one-window dominance.
- Recent-window behavior is not materially adverse under existing standards.
- Active coverage is adequate and not concentrated in a tiny subset.
- Redundancy versus active candidates and hostile/stress-repair references remains acceptable under existing standards.
- State attribution supports rank persistence after drawdown rather than pure stress repair.
- Lineage controls support the same mechanism without becoming a variant-selection exercise.

Outcome language:
- The candidate may proceed to the next research review step defined by existing process.
- No production registration or governance action is implied by the validation pass alone.

### B. Conditional Validation Candidate

Evidence pattern:
- Aggregate h10/h20 evidence remains positive, but one or more risks require review.
- WFV evidence is directionally supportive but has window concentration, recent-window weakness, active-coverage concerns, or residual redundancy risk.
- Stress-repair contamination is not proven but remains unresolved.

Outcome language:
- Hold for integration-style review or targeted diagnostic review under existing process.
- Do not tune the candidate inside validation.

### C. Diagnostic-Only Outcome

Evidence pattern:
- The candidate provides useful information about persistence or rank behavior but lacks sufficient validation robustness.
- IC evidence is horizon-limited, window-limited, or state-limited.
- Distinctiveness remains interesting but not enough for candidate advancement.

Outcome language:
- Preserve as research evidence for persistence-family design.
- Do not carry as a primary validation candidate.

### D. Validation Failure

Evidence pattern:
- h10/h20 evidence weakens materially or turns negative.
- WFV windows are unstable or dominated by one episode.
- Positive IC rate is not supportive under existing standards.
- Active coverage is too sparse or concentrated.
- Redundancy with hostile/stress-repair or existing active candidates is too high.
- State attribution indicates the candidate is mainly delayed stress repair rather than rank persistence.

Outcome language:
- Reject for validation advancement.
- Do not route to production, governance, ML, portfolio, or registration workflows.

## SECTION 7 - Diversification Assessment Plan

Persistence-family distinctiveness checks:
- Compare the primary candidate against `post_drawdown_persistence_20`, `post_drawdown_persistence_core_20`, and other persistence discovery candidates to separate lineage continuity from independent family breadth.
- Evaluate whether rank-churn adjustment improves robustness without changing the economic mechanism.
- Review whether the signal behaves differently from rank-coherence transition candidates.

Overlap with hostile/stress-repair family:
- Run redundancy checks against known hostile/stress-repair references and active candidates.
- Run state attribution against stress and recovery regimes.
- Measure activation overlap with failed-breakout, weak-breadth, liquidity-repair, and participation-repair references where available.
- Flag any result where the candidate's positive IC is concentrated only in hostile/stress-repair states.

Redundancy with existing active candidates:
- Use the current inventory/reference panels used in prior validation runners.
- Report max absolute value/rank correlation and top redundancy peer.
- Include reversal and momentum baselines to avoid accepting a renamed basic price effect.
- Include dispersion candidates to confirm cross-family distinction.

Family-level diversification value:
- Determine whether persistence adds return-ranking information not already captured by hostile/stress-repair or dispersion-transition candidates.
- Require economic interpretation to remain rank persistence after drawdown.
- Treat high sibling correlation as lineage evidence, not as broad family proof.

How validation will determine whether persistence is genuinely a new alpha family:

Validation can support a genuine persistence-family conclusion only if the candidate keeps positive h10/h20 validation evidence, maintains low redundancy to hostile/stress-repair and active candidates, shows stable WFV behavior, and exhibits state attribution consistent with rank persistence rather than simple recovery. Even then, this would establish a validated candidate thread first; broader family status would require later nonduplicative persistence candidates.

## SECTION 8 - Risk Assessment

Overfitting risk: medium.

The candidate was selected through discovery and improved in refinement on the same research history. Mitigation: freeze the formulation and use existing WFV, concentration, and redundancy diagnostics without adding variants.

Refinement sensitivity: medium.

The core and churn-adjusted variants were strong, while smoothing weakened evidence. Mitigation: validate only the churn-adjusted candidate, use controls for interpretation, and avoid selecting a different variant after validation.

Family concentration risk: medium-high.

The persistence evidence is concentrated in one refined lineage. Mitigation: report family breadth explicitly and avoid claiming broad family validation from a single candidate.

Redundancy risk: mixed.

Sibling redundancy is high by design, while stress-proxy redundancy was low in refinement. Full-inventory redundancy remains unresolved. Mitigation: require full inventory, stress-repair, reversal, momentum, dispersion, and parent-lineage redundancy outputs.

False diversification risk: medium.

The drawdown context could mask delayed stress repair. Mitigation: require state attribution, activation-overlap diagnostics, formula lineage review, and hostile/stress-repair redundancy checks.

## SECTION 9 - Recommended Validation Package

Candidate entering validation:
- Primary: `post_drawdown_persistence_churn_adjusted_20`

Controls entering validation as fixed lineage references:
- `post_drawdown_persistence_20`
- `post_drawdown_persistence_core_20`

No other candidates should enter this validation package.

Required artifacts:
- Fixed validation registry.
- Frozen candidate panel references.
- Multi-horizon scoring outputs.
- WFV-style summary and window-level diagnostics.
- Active coverage and structural quality summaries.
- Window concentration diagnostics.
- Regime/state attribution.
- Full redundancy and orthogonality audit.
- Lineage-control comparison.
- Research-only manifest with explicit no-go flags.
- Final validation review note.

Required diagnostics:
- h1/h5/h10/h20 IC and positive-rate profile.
- h10/h20 primary-horizon review.
- WFV persistence and sign consistency.
- Window concentration and recent-window health.
- Active coverage and concentration.
- Stress-repair contamination diagnostics.
- Full-inventory redundancy diagnostics.
- Parent/sibling lineage comparison.
- Diversification contribution assessment.

Expected outputs:
- A classification under existing validation standards: validation pass, conditional validation candidate, diagnostic-only, or validation failure.
- A clear statement of whether persistence remains a candidate-lineage result or supports broader family evidence.
- A next-step recommendation that remains research-only unless existing process later authorizes a separate governance review.

Governance review checkpoints:
- Pre-run scope check: confirm fixed candidate list and no new variants.
- Post-artifact integrity check: confirm validation outputs are isolated and complete.
- Post-validation review: classify evidence without modifying governance or thresholds.
- Pre-integration checkpoint if, and only if, existing validation standards justify a later review step.

## SECTION 10 - Final Recommendation

1. Is validation justified?

Yes. Validation is justified because the candidate is the strongest persistence-family refinement successor, improved h10/h20 evidence, preserved the rank-persistence thesis, and remained low-correlated with stress-repair proxies.

2. What is the strongest argument for validation?

The strongest argument is that the improvement was meaningful and disciplined: h10 mean IC improved from 0.0125 to 0.0172, h20 mean IC improved from 0.0059 to 0.0099, and the core control variant showed nearly the same result without broad parameter expansion.

3. What is the strongest argument against validation?

The strongest argument against validation is that the evidence is still concentrated in one highly related lineage and remains in-sample to the discovery/refinement workflow. It may prove to be a refined candidate artifact rather than a robust new persistence family.

4. What would constitute a meaningful diversification success?

A meaningful diversification success would be a validation result showing stable h10/h20 evidence, acceptable WFV behavior, low full-inventory and hostile/stress-repair redundancy, and state attribution consistent with rank persistence after drawdown. That would establish persistence as a credible new candidate thread and a serious step toward alpha-family diversification, even if broader family validation still requires additional nonduplicative persistence candidates later.

5. What should the next Codex task be after this design is reviewed?

The next Codex task should be to implement and run the isolated research-only validation package for `post_drawdown_persistence_churn_adjusted_20` using the fixed scope in this design. That future task should not create variants, execute refinement, modify governance, change thresholds, register production candidates, implement ML, or promote/demote candidates.

## Design Caveat

This document is a validation design only. It does not execute validation, establish validation success, modify governance, change thresholds, register production candidates, implement ML, or promote/demote any candidate.
