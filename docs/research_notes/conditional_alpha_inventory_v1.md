# Conditional Alpha Inventory Layer v1

## Executive Takeaway

Project Underdog now has two validated conditional-alpha research candidates. This note creates a research-only inventory layer so future construction research can consume governed conditional-alpha building blocks instead of raw discovery outputs.

This is not production registration, portfolio construction, ML integration, survivor/watchlist promotion, alpha-pool mutation, or production Conditional-Alpha wiring. It does not modify gates, schemas, thresholds, production logic, or trading logic.

The initial inventory contains:

| candidate | inventory status | current research status | primary variant |
|:--|:--|:--|:--|
| `participation_liquidity_state_shift_20_60` | `INVENTORY_ACTIVE_RESEARCH` | `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | `rank_persist_10_state_TREND_HOSTILE_zero` |
| `participation_breadth_repair_under_hostile_trend` | `INVENTORY_ACTIVE_RESEARCH` | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` | `strict_weak_breadth_rebalance_10` |

## Purpose

The Conditional Alpha Inventory Layer is a governed research registry for conditional-alpha candidates that have moved beyond raw discovery. Its purpose is to preserve evidence, state semantics, guardrails, and review obligations before any future construction layer is designed.

The intended architecture remains:

`Discovery -> Validation -> Refinement -> Conditional Validation -> Integration Review -> Research Inventory -> Future Construction Layer -> Portfolio/Execution Layer`

The inventory is deliberately between integration review and future construction. It is a holding and governance layer, not a promotion mechanism.

## Candidate Lifecycle Stages

| status | meaning | allowed use |
|:--|:--|:--|
| `RESEARCH_ONLY` | Early research artifact with no validation standing. | Documentation and reference only. |
| `CONDITIONAL_VALIDATION_CANDIDATE` | Candidate has passed refinement and is ready for fixed-shortlist conditional validation. | Formal validation only; no integration planning. |
| `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` | Candidate passed formal conditional validation and can enter integration-review design. | Research-only integration review planning. |
| `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | Candidate has completed integration review and has a fixed representation plus guardrails. | Eligible for inventory active research. |
| `INVENTORY_ACTIVE_RESEARCH` | Candidate is tracked as a governed conditional-alpha building block. | Monitoring, future construction design input, and equivalence planning only. |
| `INVENTORY_MONITOR_ONLY` | Candidate remains informative but is not currently suitable for integration/construction research. | Periodic decay/overlap monitoring. |
| `RETIRED_RESEARCH` | Candidate is removed from active inventory due to decay, redundancy, instability, or semantic drift. | Historical reference only. |

## Required Metadata

Every inventory candidate should carry:

| field | requirement |
|:--|:--|
| `canonical_candidate_name` | Stable candidate identifier from the research cycle. |
| `current_status` | Latest research classification. |
| `inventory_status` | Inventory-layer classification. |
| `primary_variant` | Single preferred representation, if one exists. |
| `backup_control_variants` | Confirmation, stress, or broad fallback variants. |
| `mechanism_family` | Economic or structural family. |
| `activation_state` | Market state or activation semantics. |
| `expected_horizon` | Intended validation horizon and any diagnostic horizon flags. |
| `h20_mean_ic` | Primary h20 evidence unless another horizon is explicitly justified. |
| `positive_ic_rate` | Directional consistency at the primary horizon. |
| `turnover` | Turnover proxy from validation/integration artifacts. |
| `active_coverage` | Active-date coverage or active-state coverage. |
| `wfv_persistence` | WFV-style persistence from validation artifacts. |
| `wfv_sign_consistency` | WFV-style sign consistency. |
| `effective_test_ic_ir` | WFV-style effective test IC IR. |
| `similarity_to_reversal` | Reversal-proxy similarity or nearest available baseline proxy. |
| `similarity_to_other_inventory_candidates` | Inventory overlap estimate. |
| `known_risks` | Main reasons the candidate is not production-ready. |
| `guardrails` | Required controls before any future construction research. |
| `next_required_step` | Next research action. |
| `source_artifact` | CSV/note used as the evidence source. |

## Activation Semantics

Conditional-alpha candidates must document why and when they activate. The activation definition is part of the candidate identity, not an implementation detail to tune later.

Acceptable activation semantics include:

| activation type | description |
|:--|:--|
| hostile trend | Market trend conditions are adverse or fragile. |
| weak breadth | Participation breadth is weak, deteriorating, or below a validated state threshold. |
| stress or weak breadth | Drawdown, panic/liquidity stress, or weak breadth confirms fragile market participation. |
| broad fallback/control | Always-available or high-coverage reference used to check whether conditional activation is adding value. |

Inactive handling must be explicit. Current inventory candidates use zero/neutral inactive handling or broad fallback/control variants as research references. Future construction research must not silently reinterpret inactive dates.

## Initial Inventory Table

| canonical_candidate_name | current_status | inventory_status | primary_variant | backup_control_variants | mechanism_family | activation_state | expected_horizon | h20_mean_ic | positive_ic_rate | turnover | active_coverage | WFV persistence/sign | effective_test_ic_ir | reversal similarity | inventory similarity | next_required_step |
|:--|:--|:--|:--|:--|:--|:--|:--|--:|--:|--:|--:|:--|--:|:--|:--|:--|
| `participation_liquidity_state_shift_20_60` | `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS` | `INVENTORY_ACTIVE_RESEARCH` | `rank_persist_10_state_TREND_HOSTILE_zero` | `rebalance_10_state_WEAK_BREADTH_zero`; `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero`; `rebalance_20` | participation/liquidity state shift | `TREND_HOSTILE`; backup `WEAK_BREADTH`; stress confirmation `STRESS_OR_WEAK_BREADTH` | h20 primary with h10 review flag | 0.028418 | 0.568681 | 0.096397 | 0.346997 | 1.00 / 1.00 | 2.623031 | max baseline corr 0.269307 | 0.034492 to breadth-repair primary by reciprocal audit | Hold in inventory; require research-only rebuild/equivalence planning before any future construction-layer design. |
| `participation_breadth_repair_under_hostile_trend` | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` | `INVENTORY_ACTIVE_RESEARCH` | `strict_weak_breadth_rebalance_10` | `smooth_5`; `smooth_3`; `strict_breadth_repair_recent_stress_zero` | participation breadth repair | `WEAK_BREADTH` plus hostile-trend participation repair; smooth variants as broader confirmation; recent-stress variant as stress confirmation | h20 | 0.030720 | 0.580537 | 0.013619 | 0.142993 | 1.00 / 1.00 | 1.503675 | max reversal corr 0.015265 | 0.034492 to liquidity state-shift primary | Run research-only Conditional-Alpha integration review design with fixed four-variant package. |

CSV artifact: `artifacts/research/conditional_alpha_inventory_v1/conditional_alpha_inventory.csv`

## Candidate Notes

### `participation_liquidity_state_shift_20_60`

Current status: `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.

Primary representation: `rank_persist_10_state_TREND_HOSTILE_zero`.

Backup/control variants:

- `rebalance_10_state_WEAK_BREADTH_zero`
- `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero`
- `rebalance_20`

Mechanism family: participation and liquidity state shift.

Activation semantics: hostile trend primary, weak breadth confirmation, stress/weak-breadth confirmation, broad fallback/control.

Key evidence:

- h20 mean IC: `0.028418`
- h20 positive IC rate: `0.568681`
- turnover proxy: `0.096397`
- active coverage: `0.346997`
- WFV-style effective IC IR: `2.623031`
- WFV-style persistence/sign consistency: `1.00 / 1.00`
- max baseline correlation: `0.269307`

Known risks:

- Primary variant had best horizon h10 while h20 remains the construction-review focus.
- Turnover is near the candidate-level ceiling used in prior guardrails.
- Peer variants are related, so ensemble construction could double-count the same state information.
- State labels and inactive handling must be frozen before any rebuild.

Guardrails:

- parameter lock
- semantic preservation
- rebuild/equivalence test
- active-state coverage review
- turnover ceiling
- similarity ceiling
- peer-similarity review
- one-window dominance monitoring
- rollback trigger
- hard production boundary

Next required step: keep in inventory and design an isolated rebuild/equivalence plan before any future construction-layer prototype.

### `participation_breadth_repair_under_hostile_trend`

Current status: `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE`.

Primary representation: `strict_weak_breadth_rebalance_10`.

Backup/control variants:

- `smooth_5`
- `smooth_3`
- `strict_breadth_repair_recent_stress_zero`

Mechanism family: participation breadth repair under hostile trend.

Activation semantics: weak breadth plus hostile-trend participation repair; smooth variants provide broader confirmation/control; breadth-repair plus recent stress provides stress confirmation.

Key evidence:

- h20 mean IC: `0.030720`
- h20 positive IC rate: `0.580537`
- turnover proxy: `0.013619`
- active coverage: `0.142993`
- WFV-style effective IC IR: `1.503675`
- WFV-style persistence/sign consistency: `1.00 / 1.00`
- prior participation/liquidity correlation: `0.034492`
- max reversal correlation: `0.015265`

Known risks:

- Active coverage is materially lower than the liquidity state-shift candidate and requires active-window discipline.
- The shortlist has high peer similarity, so variants should be treated as representation controls rather than independent alpha sleeves.
- One WFV-style window was weak, though the edge was not one-window dominated.
- State semantics need integration-review confirmation before any guardrail-ready classification.

Guardrails:

- fixed four-variant package
- no new tuning before integration review
- active-window coverage monitoring
- one-window dominance monitoring
- turnover drift monitoring
- baseline and inventory-overlap audit
- semantic preservation
- hard production boundary

Next required step: run a research-only Conditional-Alpha integration review design using the fixed four-variant package.

## Add-To-Inventory Rules

A future candidate may enter this inventory only if all of the following are true:

- It passed formal conditional validation.
- Parameters and state semantics are fixed.
- Primary, backup, stress, and/or broad-control variants are documented.
- h20 behavior or the intended horizon is explicitly justified.
- Turnover guardrails are documented.
- Similarity and orthogonality audits are complete.
- Active coverage and active-window sanity checks are complete.
- Inactive-date handling is explicit.
- Known failure modes and rollback triggers are documented.
- There is no production wiring, survivor/watchlist mutation, alpha-pool mutation, ML usage, or portfolio usage.

## Downgrade Or Removal Rules

An inventory candidate should be downgraded to `INVENTORY_MONITOR_ONLY` or `RETIRED_RESEARCH` if any of the following occur in a later research review:

- IC decays materially at the intended horizon.
- WFV-style persistence or sign consistency decays.
- Turnover drifts above the documented ceiling.
- Active coverage collapses or becomes concentrated in too few windows.
- Baseline similarity drifts upward and the candidate collapses into reversal, momentum, or a prior participation/liquidity proxy.
- State semantics become unstable or require repeated relabeling.
- Inactive-date handling changes the candidate's meaning.
- A newer candidate duplicates the exposure with better evidence and cleaner semantics.
- Rebuild/equivalence testing fails without a clear explanation.

## Monitoring Framework

### Overlap Monitoring

Inventory candidates must be checked against:

- reversal baselines
- momentum or price-rank baselines
- liquidity/participation baselines
- current inventory candidates
- any future construction-layer representations

High peer similarity does not automatically reject a candidate, but it changes how the candidate should be represented. Related variants should support one semantic package, not become independent sleeves.

### Decay Monitoring

Future research reviews should track:

- h20 mean IC
- positive IC rate
- effective WFV-style IC IR
- persistence/sign consistency
- one-window dominance
- active-window coverage
- turnover
- baseline similarity
- inventory-candidate similarity

Decay monitoring is observational. It does not create automatic production promotion or rejection logic.

### Rollback / Removal Triggers

Rollback or removal from active inventory should be considered if:

- primary variant h20 evidence materially deteriorates
- active coverage falls below usable research levels
- turnover rises sharply after rebuild
- state definitions require tuning to preserve results
- similarity to another inventory candidate becomes too high to justify separate representation
- one-window dominance becomes the main source of evidence
- any future rebuild produces unexplained metric improvement or degradation

## Future Construction-Layer Interface

This inventory is intended to feed a future construction layer only after additional design work. A future construction layer may ask:

- Should a candidate be represented as a state-gated alpha, context filter, sleeve, or confirmation layer?
- Should a broad fallback/control variant be included only for diagnostics?
- How should inactive dates be handled?
- How should overlapping conditional candidates be blended or selected?
- How should active-state risk and turnover be monitored?

The inventory does not answer those construction questions. It preserves the evidence and guardrails needed to ask them safely later.

## Non-Goals

This inventory does not:

- register signals for production
- create trading signals
- alter survivor/watchlist status
- mutate alpha pools
- change gates, schemas, or thresholds
- create portfolio construction logic
- create execution logic
- add ML features or labels
- automatically promote candidates

## Final Recommendation

Adopt `conditional_alpha_inventory_v1` as the research-only holding layer for validated conditional-alpha candidates. Keep both current candidates in `INVENTORY_ACTIVE_RESEARCH`, with `participation_liquidity_state_shift_20_60` already guardrail-ready and `participation_breadth_repair_under_hostile_trend` requiring a fixed-package integration review before it can receive the same guardrail-ready status.
