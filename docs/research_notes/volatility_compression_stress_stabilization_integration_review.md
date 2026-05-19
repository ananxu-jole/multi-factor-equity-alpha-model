# Volatility Compression Stress Stabilization Integration Review

## Executive Takeaway

`volatility_compression_after_stress_stabilization` should be added to the Conditional Alpha Inventory as `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS`.

This is a research-only recommendation. No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.

The recommended representation is:

| role | variant |
|:--|:--|
| Primary | `rebalance_5` |
| Confirmation/control | `smooth_5` |
| Confirmation/control | `smooth_3` |

The candidate is structurally distinct from the current participation/liquidity/breadth inventory cluster and from reversal/momentum baselines. The main reason to include it is mechanism diversity: it is the first validated volatility/stress-transition candidate to survive conditional validation. The main reason to require guardrails is validation fragility: `rebalance_5` is positive in all WFV-style windows, but window 3 contributes a large share of the positive-window IC and the recent window is only barely positive.

## Scope

Source evidence:

- Validation note: `docs/research_notes/volatility_compression_stress_stabilization_conditional_validation.md`
- Validation artifacts: `artifacts/research/volatility_compression_stress_stabilization_conditional_validation_v1/`
- Current inventory note: `docs/research_notes/conditional_alpha_inventory_v1.md`
- Current inventory CSV: `artifacts/research/conditional_alpha_inventory_v1/conditional_alpha_inventory.csv`

This review does not update the inventory CSV. It recommends a future research-only inventory update that adds this candidate with guardrails.

## Candidate Identity

| field | value |
|:--|:--|
| canonical candidate name | `volatility_compression_after_stress_stabilization` |
| current status | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` |
| recommended inventory status | `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` |
| primary variant | `rebalance_5` |
| confirmation/control variants | `smooth_5`; `smooth_3` |
| mechanism family | volatility/stress-transition stabilization |
| activation semantics | recent volatility stress, range normalization, dispersion-elevated/stress contexts |
| expected horizon | h20 |
| inactive handling | inherited from validated variant panels; no reinterpretation in this review |

## Primary Evidence

| metric | `rebalance_5` |
|:--|--:|
| h20 mean IC | 0.028391 |
| h20 positive IC rate | 0.574413 |
| turnover proxy | 0.022092 |
| active date ratio | 0.189704 |
| WFV-style persistence | 1.00 |
| WFV-style sign consistency | 1.00 |
| effective test IC IR | 1.008408 |
| max inventory correlation | 0.047430 |
| max reversal correlation | 0.057781 |
| max momentum correlation | 0.005171 |

The h20 profile is strong enough for inventory inclusion as a research candidate. Turnover is low, active coverage is adequate for conditional research, and similarity to the two existing inventory candidates is low.

## Inventory Comparison

| candidate | mechanism family | primary variant | h20 mean IC | turnover | active coverage | WFV persistence/sign | max inventory overlap |
|:--|:--|:--|--:|--:|--:|:--|--:|
| `participation_liquidity_state_shift_20_60` | participation/liquidity state shift | `rank_persist_10_state_TREND_HOSTILE_zero` | 0.028418 | 0.096397 | 0.346997 | 1.00 / 1.00 | 0.034492 to breadth-repair |
| `participation_breadth_repair_under_hostile_trend` | participation breadth repair | `strict_weak_breadth_rebalance_10` | 0.030720 | 0.013619 | 0.142993 | 1.00 / 1.00 | 0.034492 to liquidity state-shift |
| `volatility_compression_after_stress_stabilization` | volatility/stress-transition stabilization | `rebalance_5` | 0.028391 | 0.022092 | 0.189704 | 1.00 / 1.00 | 0.047430 to liquidity state-shift |

Interpretation:

- The candidate is not a participation repair variant.
- Inventory overlap is low enough to justify separate tracking.
- Its turnover is materially lower than the liquidity state-shift candidate and above the breadth-repair candidate, but still acceptable.
- Active coverage sits between the two existing candidates.
- Mechanism diversity is the strongest argument for inclusion.

## Orthogonality Assessment

The validation run reported:

| comparison type | max correlation |
|:--|--:|
| current inventory | 0.047430 |
| reversal baselines | 0.057781 |
| momentum baselines | 0.005171 |
| base v6 volatility compression source | 0.684536 |

The high correlation to the base v6 volatility compression signal is expected and desirable because it confirms semantic continuity. The low correlations to inventory, reversal, and momentum baselines support the view that this is a distinct volatility/stress-transition mechanism rather than a disguised reversal, momentum, or participation/liquidity repair signal.

## WFV And Window Concentration

`rebalance_5` WFV-style windows:

| window | date range | mean test IC | positive IC rate | valid IC dates |
|--:|:--|--:|--:|--:|
| 1 | 2018-11-29 to 2020-05-21 | 0.008408 | 0.614583 | 96 |
| 2 | 2020-05-22 to 2022-06-01 | 0.028640 | 0.562500 | 96 |
| 3 | 2022-06-02 to 2024-09-17 | 0.073948 | 0.760417 | 96 |
| 4 | 2024-09-18 to 2026-04-09 | 0.002298 | 0.357895 | 95 |

The primary variant has no negative WFV-style windows. That is a meaningful improvement over the original v6 formulation.

The caution is real:

- Window 3 contributes about 65% of positive-window IC.
- The recent window is only slightly positive.
- The recent window positive IC rate is weak at 0.357895.
- Confirmation variants `smooth_5` and `smooth_3` retain negative recent WFV-style windows.

This does not invalidate the candidate, but it argues against any clean or unguarded inventory classification.

## State Semantics

The candidate works best in stress-like and fragile-volatility states:

| state | `rebalance_5` mean IC | positive IC rate |
|:--|--:|--:|
| panic/liquidity stress | 0.170419 | 0.791667 |
| drawdown acceleration | 0.165135 | 0.775510 |
| weak breadth | 0.127372 | 0.708861 |
| volatility spike | 0.063342 | 0.649718 |
| high dispersion rotation | 0.004312 | 0.564286 |
| recovery phase | -0.002790 | 0.582524 |
| trend transition | -0.015266 | 0.482270 |

Concept-state attribution is consistent with the mechanism:

- Positive during `RECENT_VOL_STRESS`, `RANGE_NORMALIZING`, and `DISPERSION_ELEVATED_RECENT`.
- Negative during `VOL_NORMALIZING`.
- Weak during dispersion normalization/stability transition states.

The candidate should be treated as a volatility/stress-transition stabilization mechanism, not a general volatility-normalization alpha.

## Confirmation Variants

`smooth_5` and `smooth_3` support the mechanism but should not become primary inventory variants.

| variant | h20 mean IC | WFV persistence/sign | recent window IC | interpretation |
|:--|--:|:--|--:|:--|
| `smooth_5` | 0.020248 | 0.75 / 0.75 | -0.021266 | useful confirmation/control; recent-window weakness remains |
| `smooth_3` | 0.019243 | 0.75 / 0.75 | -0.021719 | useful confirmation/control; recent-window weakness remains |

These variants confirm that the mechanism is not purely an artifact of the five-day rebalance interval. They also show that rebalance timing matters materially, so future integration must preserve the `rebalance_5` semantics exactly.

## Inventory Status Decision

Recommended status: `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS`.

Rejected alternatives:

| option | decision | rationale |
|:--|:--|:--|
| `HOLD_OUTSIDE_INVENTORY` | rejected | The candidate passed formal validation, has low inventory/reversal/momentum similarity, and expands inventory into a new volatility/stress-transition family. |
| `INVENTORY_MONITOR_ONLY` | rejected | Evidence is stronger than monitor-only: h20 IC, WFV persistence/sign consistency, turnover, and active coverage are adequate for governed active research. |
| `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` | recommended | Inclusion is justified, but window concentration and recent-window fragility require explicit controls. |

## Guardrails

Required guardrails before any future construction-layer consideration:

| guardrail | proposed requirement |
|:--|:--|
| fixed representation | `rebalance_5` primary; `smooth_5` and `smooth_3` confirmation/control only |
| no new tuning | no additional smoothing/rebalance/state variants before inventory update |
| recent-window monitoring | flag if recent-window h20 mean IC becomes negative or positive IC rate remains below 0.45 in later refreshes |
| window concentration monitoring | flag if largest positive-window share remains above roughly 0.65 or rises further |
| active coverage minimum | maintain active date ratio near or above 0.15, with enough valid IC dates per window |
| turnover ceiling | keep turnover proxy below 0.05 for the primary variant |
| inventory similarity ceiling | monitor if max inventory correlation rises above 0.15 |
| reversal/momentum similarity ceiling | monitor if max reversal or momentum correlation rises above 0.15 |
| semantic preservation | preserve volatility/stress-transition thesis and five-day rebalance semantics |
| rebuild/equivalence test | require isolated rebuild/equivalence before any construction-layer prototype |
| rollback/removal trigger | downgrade to `INVENTORY_MONITOR_ONLY` if recent-window weakness persists, WFV persistence drops, active coverage collapses, or similarity drifts upward |

## Proposed Inventory Row

This row is proposed for a future research-only inventory update. It was not written to the current inventory CSV in this review.

| field | proposed value |
|:--|:--|
| canonical_candidate_name | `volatility_compression_after_stress_stabilization` |
| current_status | `CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE` |
| inventory_status | `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS` |
| primary_variant | `rebalance_5` |
| backup_control_variants | `smooth_5`; `smooth_3` |
| mechanism_family | volatility/stress-transition stabilization |
| activation_state | recent volatility stress and range normalization; strongest during panic/drawdown/weak breadth/volatility spike |
| expected_horizon | h20 |
| h20_mean_ic | 0.028391 |
| positive_ic_rate | 0.574413 |
| turnover | 0.022092 |
| active_coverage | 0.189704 |
| wfv_persistence | 1.00 |
| wfv_sign_consistency | 1.00 |
| effective_test_ic_ir | 1.008408 |
| similarity_to_reversal | 0.057781 |
| similarity_to_other_inventory_candidates | max inventory corr 0.047430 |
| known_risks | recent-window fragility; window concentration; confirmation variants have negative recent WFV window; weak behavior in trend-transition/recovery/VOL_NORMALIZING states |
| guardrails | fixed representation; no new tuning; recent-window monitoring; window concentration monitoring; active coverage minimum; turnover ceiling; inventory/reversal/momentum similarity ceilings; semantic preservation; rebuild/equivalence; rollback trigger |
| next_required_step | update Conditional Alpha Inventory v2 as research-only, then design isolated integration/rebuild equivalence checks before any construction-layer work |
| source_artifact | `artifacts/research/volatility_compression_stress_stabilization_conditional_validation_v1/validation_summary.csv` |

## Final Recommendation

Add `volatility_compression_after_stress_stabilization` as the third Conditional Alpha Inventory research candidate in a future inventory update, with status `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS`.

Do not productionize it. Do not register it. Do not add it to survivor/watchlist lists. Do not wire it into portfolio, ML, or production Conditional-Alpha paths.

The next concrete step should be a research-only Conditional Alpha Inventory v2 update that adds this candidate and preserves the guardrails above.
